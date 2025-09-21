import requests
import json
from config import NEWS_API_KEY

def fetch_financial_market_news(keywords, country_name=None):
    """
    Fetches financial market news by embedding the country name into the search query.
    """
    if not keywords:
        print("No keywords provided. Please provide a list of keywords to search for.")
        return []

    # Combine the keywords into a parenthesized, OR-separated string.
    keyword_query = f"({ ' OR '.join(keywords) })"
    
    # If a country name is provided, add it to the query as a required term.
    # This is the correct way to filter by country with the /everything endpoint.
    if country_name:
        final_query = f"{keyword_query} AND {country_name}"
    else:
        final_query = keyword_query
    
    # Use the /v2/everything endpoint for the best keyword search results.
    # We sort by relevancy to ensure the most topical articles appear first.
    url = f"https://newsapi.org/v2/everything?q={final_query}&sortBy=relevancy&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        
        if data.get('status') != 'ok':
            print(f"Error from News API: {data.get('message')}")
            return []
            
        articles = []
        articles_data = data.get('articles', [])
        
        if articles_data:
            for article in articles_data:
                # Ensure both title and description are present before adding.
                if article.get('title') and article.get('description'):
                    articles.append(f"Title: {article['title']}\nContent: {article['description']}\n")
            
            if articles:
                return articles
                
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from the API: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing the JSON response: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    print("No articles found or an error occurred while fetching news.")
    return []

if __name__ == "__main__":
    # Define a list of keywords for specific financial market news.
    financial_keywords = [
        "stock market",
        "interest rates",
        "inflation",
        "Reserve Bank of India",
        "economic growth",
        "bond market",
        "Sensex", # Added a more India-specific keyword
        "Nifty",  # Added a more India-specific keyword
        "IPO",
        "mergers and acquisitions"
    ]
    
    # Specify the country name to include in the search query.
    country = "India"
    
    print(f"Fetching recent financial market news related to {country}...")
    # Pass the country name to the function.
    news_articles = fetch_financial_market_news(financial_keywords, country_name=country)
    
    if news_articles:
        print(f"\nFound {len(news_articles)} articles:\n")
        for i, article in enumerate(news_articles, 1):
            print(f"--- Article {i} ---")
            print(article)
    else:
        print("No financial market news articles were found.")