import requests
import json
import os
import hashlib
from datetime import datetime
from config import NEWS_API_KEY

# --- REQUIRED IMPORTS ---
from langchain_google_vertexai import VertexAIEmbeddings
from google.cloud import storage
from google.cloud import aiplatform

# --- GCP & OUTPUT CONFIGURATION ---
PROJECT_ID = "stonkbot007"
BUCKET_NAME = "stonkbot007"
GCS_FOLDER_PATH = "embeddings"
# Best practice is to use the .jsonl extension for JSON Lines files.
JSONL_FILE_NAME = "news_embeddings.json"

# --- VERTEX AI VECTOR SEARCH CONFIG ---
REGION = "asia-south1"
# The full resource name is the most reliable way to identify the index.
INDEX_ID = "projects/stonkbot007/locations/asia-south1/indexes/680870376477032448"


def fetch_financial_market_news(keywords: list, country_name: str = None) -> list:
    """
    Fetches financial market news and returns a list of article dictionaries.
    """
    if not keywords:
        print("No keywords provided.")
        return []

    keyword_query = f"({' OR '.join(keywords)})"

    if country_name:
        final_query = f"{keyword_query} AND {country_name}"
    else:
        final_query = keyword_query

    url = f"https://newsapi.org/v2/everything?q={final_query}&language=en&sortBy=relevancy&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get('status') != 'ok':
            print(f"Error from News API: {data.get('message')}")
            return []

        articles_to_return = []
        for article in data.get('articles', []):
            # Ensure all required fields are present before appending.
            if all(k in article for k in ['title', 'description', 'url']):
                articles_to_return.append({
                    "content": f"Title: {article['title']}\nDescription: {article['description']}",
                    "url": article['url']
                })
        return articles_to_return

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from the API: {e}")
    return []


def generate_and_save_embeddings(articles: list, local_file_path: str) -> bool:
    """
    Generates embeddings for articles and saves them to a local JSONL file.
    Returns True on success, False on failure.
    """
    if not articles:
        print("No articles provided to generate embeddings for.")
        return False

    print(
        f"Generating embeddings for {len(articles)} articles in a single batch...")
    try:
        # UPDATED MODEL NAME: "text-embedding-004" is the latest Gemini embedding model.
        embedding_model = VertexAIEmbeddings(
            model_name="text-embedding-004", project=PROJECT_ID, location=REGION
        )

        content_list = [article["content"] for article in articles]
        all_embeddings = embedding_model.embed_documents(content_list)

        with open(local_file_path, "w") as f:
            for article, embedding in zip(articles, all_embeddings):
                # Use a stable hash of the URL as the unique ID for each vector.
                article_id = hashlib.sha256(
                    article["url"].encode()).hexdigest()
                record = {"id": article_id, "embedding": embedding}
                f.write(json.dumps(record) + "\n")

        # Final sanity check to ensure the file is not empty.
        if os.path.getsize(local_file_path) > 0:
            print(
                f"✅ Successfully created '{local_file_path}' with embeddings.")
            return True
        else:
            print("❌ ERROR: Embedding process resulted in an empty file.")
            return False

    except Exception as e:
        print(f"❌ An error occurred during embedding generation: {e}")
        return False


def upload_to_gcs(bucket_name: str, source_file_name: str, destination_blob_name: str) -> bool:
    """Uploads a file to the bucket. Returns True on success."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        print(
            f"✅ File {source_file_name} uploaded to gs://{bucket_name}/{destination_blob_name}")
        return True
    except Exception as e:
        print(f"❌ Error uploading to GCS: {e}")
        return False


def trigger_index_update(gcs_folder_uri: str):
    """
    Triggers a batch update for the Vector Search index.
    """
    print(
        f"\n🚀 Initiating Vertex AI index update from folder: {gcs_folder_uri}")
    try:
        aiplatform.init(project=PROJECT_ID, location=REGION)
        my_index = aiplatform.MatchingEngineIndex(index_name=INDEX_ID)
        my_index.update_embeddings(
            contents_delta_uri=gcs_folder_uri
        )
        print("✅ Successfully started the index update process.")
        print("   NOTE: It may take 20-60 minutes for the index to fully reflect the new data.")
    except Exception as e:
        print(f"❌ Failed to trigger index update: {e}")


if __name__ == "__main__":
    financial_keywords = [
        "stock market", "interest rates", "inflation", "Reserve Bank of India",
        "RBI", "economic growth", "bond market", "commodities", "IPO",
        "mergers and acquisitions", "Sensex", "Nifty", "BSE", "NSE",
        "Indian economy", "rupee", "Indian stocks"
    ]
    country = "India"

    # --- Step 1: Fetch News ---
    print(f"Fetching recent financial market news related to {country}...")
    news_articles = fetch_financial_market_news(
        financial_keywords, country_name=country)

    if not news_articles:
        print("No financial market news articles were found. Exiting.")
    else:
        # --- Step 2: Generate and Save Embeddings Locally ---
        embeddings_created = generate_and_save_embeddings(
            news_articles, JSONL_FILE_NAME)

        if embeddings_created:
            # --- Step 3: Upload Embeddings to GCS ---
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            gcs_update_folder = os.path.join(GCS_FOLDER_PATH, timestamp)
            destination_path = os.path.join(gcs_update_folder, JSONL_FILE_NAME)

            upload_successful = upload_to_gcs(
                BUCKET_NAME, JSONL_FILE_NAME, destination_path)

            if upload_successful:
                # --- Step 4: Trigger the Index Update ---
                gcs_folder_uri_for_update = f"gs://{BUCKET_NAME}/{gcs_update_folder}"
                trigger_index_update(gcs_folder_uri_for_update)
