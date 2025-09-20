
import requests
import json
from config import NEWS_API_KEY

def fetch_recent_business_news():
    """Fetches top business headlines, trying India first, then US as fallback."""
    # Try India business news first
    urls_to_try = [
        ("India Business", f"https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey={NEWS_API_KEY}"),
        ("India General", f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"),
        ("US Business", f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={NEWS_API_KEY}")
    ]
    
    for source_name, url in urls_to_try:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            
            # Check if the API response is successful
            if data.get('status') != 'ok':
                continue
            
            # Return a list of news articles (title + description)
            articles = []
            articles_data = data.get('articles', [])
            
            if len(articles_data) > 0:
                for article in articles_data:
                    if article.get('title') and article.get('description'):
                        articles.append(f"Title: {article['title']}\nContent: {article['description']}\n")
                
                if articles:  # Only return if we have articles with both title and description
                    return articles
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {source_name} news: {e}")
            continue
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response for {source_name}: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error for {source_name}: {e}")
            continue
    
    print("All news sources failed")
    return []

if __name__ == "__main__":
    print("Fetching recent business news from India...")
    news_articles = fetch_recent_business_news()
    
    if news_articles:
        print(f"\nFound {len(news_articles)} articles:\n")
        for i, article in enumerate(news_articles, 1):
            print(f"--- Article {i} ---")
            print(article)
    else:
        print("No articles found or error occurred.")