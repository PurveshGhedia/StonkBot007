#!/usr/bin/env python3
"""
StonkBot007 - A simple news aggregator for business news from India
"""

from news_fetcher import fetch_financial_market_news

def main():
    """Main function to run the StonkBot007 financial news aggregator."""
    print("🤖 StonkBot007 - Financial Market News Aggregator")
    print("=" * 55)
    
    # Define financial keywords to search for with India-specific terms
    financial_keywords = [
        "stock market",
        "interest rates", 
        "inflation",
        "Reserve Bank of India",
        "RBI",
        "economic growth",
        "bond market",
        "commodities",
        "IPO",
        "mergers and acquisitions",
        "Sensex",
        "Nifty",
        "BSE",
        "NSE",
        "Indian economy",
        "rupee",
        "Indian stocks"
    ]
    
    # Fetch recent financial market news from India
    news_articles = fetch_financial_market_news(financial_keywords, country_name="India")
    
    if news_articles:
        print(f"\n📰 Found {len(news_articles)} financial market news articles:\n")
        
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
