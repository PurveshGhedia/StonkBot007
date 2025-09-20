#!/usr/bin/env python3
"""
StonkBot007 - A simple news aggregator for business news from India
"""

from news_fetcher import fetch_recent_business_news

def main():
    """Main function to run the StonkBot007 news aggregator."""
    print("🤖 StonkBot007 - Business News Aggregator")
    print("=" * 50)
    
    # Fetch recent business news
    news_articles = fetch_recent_business_news()
    
    if news_articles:
        print(f"\n📰 Found {len(news_articles)} business news articles from India:\n")
        
        for i, article in enumerate(news_articles, 1):
            print(f"📄 Article {i}:")
            print("-" * 30)
            print(article)
            print()
    else:
        print("\n❌ No articles found or an error occurred.")
        print("Please check your internet connection and API key.")

if __name__ == "__main__":
    main()
