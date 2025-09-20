import requests
import json
import os
import hashlib
from config import NEWS_API_KEY

# --- REQUIRED IMPORTS ---
from langchain_google_vertexai import VertexAIEmbeddings
from google.cloud import storage
from google.cloud import aiplatform  # 👈 ADD THIS IMPORT
# -------------------------

# --- GCP & OUTPUT CONFIGURATION ---
# IMPORTANT: Before running, authenticate with gcloud:
# gcloud auth application-default login

PROJECT_ID = "stonkbot007"        # 👈 Your GCP Project ID
BUCKET_NAME = "stonkbot007"   # 👈 Your GCS Bucket Name
GCS_FOLDER_PATH = "embeddings"            # 👈 The folder inside your bucket
JSONL_FILE_NAME = "news_embeddings.jsonl"  # 👈 The name of the output file

# --- NEW: VERTEX AI VECTOR SEARCH CONFIG ---
REGION = "asia-south1"  # Your GCP region (Mumbai)
# Get this full resource name from the Vertex AI > Vector Search > Index details page.
# 👈 YOUR FULL INDEX ID
INDEX_ID = "projects/1234567890/locations/asia-south1/indexes/1234567890123456789"
# -------------------------------------------


def fetch_financial_market_news(keywords, country_name=None):
    """Fetches financial market news and returns a list of article dictionaries."""
    # (Your existing function - no changes needed here)
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
        articles_data = []
        for article in data.get('articles', []):
            if article.get('title') and article.get('description') and article.get('url'):
                articles_data.append({
                    "content": f"Title: {article['title']}\nDescription: {article['description']}",
                    "url": article['url']
                })
        return articles_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from the API: {e}")
    return []


def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # (Your existing function - no changes needed here)
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

# --- NEW FUNCTION TO TRIGGER THE INDEX UPDATE ---


def trigger_index_update(gcs_folder_uri):
    """
    Triggers a batch update for the Vector Search index using the data in the GCS folder.
    """
    print(
        f"\n🚀 Initiating Vertex AI index update from folder: {gcs_folder_uri}")
    try:
        my_index = aiplatform.MatchingEngineIndex(index_name=INDEX_ID)
        my_index.update_embeddings(
            contents_delta_uri=gcs_folder_uri
        )
        print("✅ Successfully started the index update process.")
        print("   NOTE: It may take 20-60 minutes for the index to fully reflect the new data.")
    except Exception as e:
        print(f"❌ Failed to trigger index update: {e}")
# ---------------------------------------------


if __name__ == "__main__":
    financial_keywords = [
        "stock market", "interest rates", "inflation", "Reserve Bank of India",
        "economic growth", "bond market", "Sensex", "Nifty", "IPO"
    ]
    country = "India"

    print(f"Fetching recent financial market news related to {country}...")
    news_articles = fetch_financial_market_news(
        financial_keywords, country_name=country)

    if news_articles:
        print(
            f"Found {len(news_articles)} articles. Now generating embeddings...")

        embedding_model = VertexAIEmbeddings(
            model_name="textembedding-gecko@003", project=PROJECT_ID)

        with open(JSONL_FILE_NAME, "w") as f:
            for article in news_articles:
                try:
                    embedding = embedding_model.embed_query(article["content"])
                    article_id = hashlib.sha256(
                        article["url"].encode()).hexdigest()
                    record = {"id": article_id, "embedding": embedding}
                    f.write(json.dumps(record) + "\n")
                except Exception as e:
                    print(
                        f"Could not process article {article.get('url', '')}: {e}")

        print(f"✅ Successfully created '{JSONL_FILE_NAME}' with embeddings.")

        # Upload the generated file to GCS
        # IMPORTANT: We need a unique folder for each update. Using a timestamp is a good practice.
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        gcs_update_folder = os.path.join(GCS_FOLDER_PATH, timestamp)
        destination_path = os.path.join(gcs_update_folder, JSONL_FILE_NAME)

        upload_successful = upload_to_gcs(
            BUCKET_NAME, JSONL_FILE_NAME, destination_path)

        # --- OPTIMIZATION: TRIGGER UPDATE AFTER UPLOAD ---
        if upload_successful:
            # The API needs the URI to the FOLDER, not the file itself.
            gcs_folder_uri_for_update = f"gs://{BUCKET_NAME}/{gcs_update_folder}"
            trigger_index_update(gcs_folder_uri_for_update)
        # ------------------------------------------------

    else:
        print("No financial market news articles were found to process.")
