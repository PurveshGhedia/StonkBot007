#!/usr/bin/env python3
"""
Portfolio Scanner - Main script that scans news for stock mentions and provides actionable insights
"""

import sys
import json
from typing import List, Dict, Tuple
from datetime import datetime

from news_fetcher import fetch_financial_market_news
from stock_extractor import StockExtractor
from sentiment_analyzer import SentimentAnalyzer
from insights_generator import InsightsGenerator

class PortfolioScanner:
    def __init__(self):
        """Initialize the portfolio scanner with all required components."""
        self.news_fetcher = None  # Will use the existing function
        self.stock_extractor = StockExtractor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.insights_generator = InsightsGenerator()
        
        # Default financial keywords for news fetching (shorter list to avoid API limits)
        self.default_keywords = [
            "stock market", "earnings", "quarterly results", "IPO", "mergers",
            "Sensex", "Nifty", "Indian stocks", "dividend", "RBI", "banking"
        ]

    def scan_news_for_stocks(self, keywords: List[str] = None, country: str = "India", 
                           max_articles: int = 100) -> Tuple[List[str], Dict]:
        """
        Scan news articles for stock mentions and analyze sentiment.
        
        Args:
            keywords: List of keywords to search for in news
            country: Country to focus the search on
            max_articles: Maximum number of articles to analyze
            
        Returns:
            Tuple of (articles, analysis_results)
        """
        print("🔍 Starting Portfolio Scanner...")
        print("=" * 40)
        
        # Use default keywords if none provided
        if keywords is None:
            keywords = self.default_keywords
        
        print(f"📰 Fetching news articles for {len(keywords)} keywords...")
        print(f"🌍 Country: {country}")
        print(f"📊 Max articles: {max_articles}")
        print()
        
        # Fetch news articles
        articles = fetch_financial_market_news(keywords, country_name=country)
        
        if not articles:
            print("❌ No articles found. Please check your internet connection and API key.")
            return [], {}
        
        # Limit articles if needed
        if len(articles) > max_articles:
            articles = articles[:max_articles]
            print(f"📝 Limited to first {max_articles} articles")
        
        print(f"✅ Found {len(articles)} articles to analyze")
        print()
        
        # Extract stock symbols from articles
        print("🔍 Extracting stock symbols from articles...")
        stock_results = self.stock_extractor.extract_stocks_from_news_articles(articles)
        
        # Get all unique stock symbols, filtering for known companies and high confidence
        all_stocks = set()
        for article_stocks in stock_results.values():
            for stock in article_stocks:
                # Only include known companies or high-confidence symbols
                if (stock['company'] != 'Unknown' or 
                    stock['confidence'] == 'high' or 
                    (stock['confidence'] == 'medium' and len(stock['symbol']) >= 4)):
                    all_stocks.add(stock['symbol'])
        
        all_stocks = list(all_stocks)
        print(f"📈 Found {len(all_stocks)} unique stock symbols (filtered for quality)")
        
        if not all_stocks:
            print("❌ No stock symbols found in the articles")
            return articles, {}
        
        # Analyze sentiment for each stock
        print("📊 Analyzing sentiment for each stock...")
        stock_sentiments = self.sentiment_analyzer.analyze_stock_sentiment(articles, all_stocks)
        
        # Get stock frequency
        stock_frequency = self.stock_extractor.get_stock_frequency(articles)
        
        # Combine all data
        analysis_results = {
            'articles_analyzed': len(articles),
            'stocks_found': len(all_stocks),
            'stock_frequency': stock_frequency,
            'stock_sentiments': stock_sentiments,
            'top_stocks': self.stock_extractor.get_top_stocks(articles, 10),
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        print("✅ Analysis complete!")
        print()
        
        return articles, analysis_results

    def generate_insights(self, analysis_results: Dict) -> Tuple[List[Dict], Dict]:
        """
        Generate actionable insights from the analysis results.
        
        Args:
            analysis_results: Results from news analysis
            
        Returns:
            Tuple of (stock_insights, portfolio_insights)
        """
        print("💡 Generating actionable insights...")
        
        # Prepare stock data for insights generation
        stock_data = {}
        stock_sentiments = analysis_results.get('stock_sentiments', {})
        stock_frequency = analysis_results.get('stock_frequency', {})
        
        for symbol, sentiment_data in stock_sentiments.items():
            if sentiment_data['total_mentions'] > 0:
                stock_data[symbol] = {
                    'company': self.stock_extractor.symbol_to_company.get(symbol, 'Unknown'),
                    'mentions': sentiment_data['total_mentions'],
                    'sentiment': sentiment_data['overall_sentiment'],
                    'confidence': sentiment_data['confidence']
                }
        
        # Generate individual stock insights
        stock_insights = self.insights_generator.generate_stock_insights(stock_data)
        
        # Generate portfolio-level insights
        portfolio_insights = self.insights_generator.generate_portfolio_insights(stock_insights)
        
        print("✅ Insights generated!")
        print()
        
        return stock_insights, portfolio_insights

    def print_summary_report(self, analysis_results: Dict, stock_insights: List[Dict], 
                           portfolio_insights: Dict):
        """Print a summary report of the analysis."""
        print("📊 PORTFOLIO SCANNER SUMMARY")
        print("=" * 40)
        print(f"Articles Analyzed: {analysis_results.get('articles_analyzed', 0)}")
        print(f"Stocks Found: {analysis_results.get('stocks_found', 0)}")
        print(f"Analysis Time: {analysis_results.get('analysis_timestamp', 'Unknown')}")
        print()
        
        # Top mentioned stocks
        top_stocks = analysis_results.get('top_stocks', [])
        if top_stocks:
            print("📈 TOP 10 MOST MENTIONED STOCKS:")
            print("-" * 35)
            for i, (symbol, frequency) in enumerate(top_stocks[:10], 1):
                company = self.stock_extractor.symbol_to_company.get(symbol, 'Unknown')
                print(f"{i:2d}. {symbol:12s} ({company:25s}) - {frequency} mentions")
            print()
        
        # Portfolio sentiment overview
        sentiment_breakdown = portfolio_insights.get('sentiment_breakdown', {})
        print("📊 SENTIMENT OVERVIEW:")
        print("-" * 22)
        print(f"Positive: {sentiment_breakdown.get('positive', 0)} stocks")
        print(f"Negative: {sentiment_breakdown.get('negative', 0)} stocks")
        print(f"Neutral:  {sentiment_breakdown.get('neutral', 0)} stocks")
        print()
        
        # Top recommendations
        buy_recs = portfolio_insights.get('top_buy_recommendations', [])
        sell_recs = portfolio_insights.get('top_sell_recommendations', [])
        
        if buy_recs:
            print("🟢 TOP BUY RECOMMENDATIONS:")
            print("-" * 28)
            for stock in buy_recs[:3]:
                print(f"• {stock['symbol']} - {stock['recommendation']}")
            print()
        
        if sell_recs:
            print("🔴 TOP SELL RECOMMENDATIONS:")
            print("-" * 30)
            for stock in sell_recs[:3]:
                print(f"• {stock['symbol']} - {stock['recommendation']}")
            print()
        
        print(f"Portfolio Recommendation: {portfolio_insights.get('portfolio_recommendation', 'N/A')}")

    def save_results(self, analysis_results: Dict, stock_insights: List[Dict], 
                    portfolio_insights: Dict, filename: str = None):
        """
        Save analysis results to a JSON file.
        
        Args:
            analysis_results: News analysis results
            stock_insights: Individual stock insights
            portfolio_insights: Portfolio-level insights
            filename: Output filename (optional)
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"portfolio_scan_{timestamp}.json"
        
        results = {
            'analysis_results': analysis_results,
            'stock_insights': stock_insights,
            'portfolio_insights': portfolio_insights,
            'generated_at': datetime.now().isoformat()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"💾 Results saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")

    def run_full_scan(self, keywords: List[str] = None, country: str = "India", 
                     max_articles: int = 100, save_results: bool = True):
        """
        Run a complete portfolio scan.
        
        Args:
            keywords: Keywords to search for
            country: Country to focus on
            max_articles: Maximum articles to analyze
            save_results: Whether to save results to file
        """
        try:
            # Step 1: Scan news for stocks
            articles, analysis_results = self.scan_news_for_stocks(
                keywords, country, max_articles
            )
            
            if not analysis_results:
                print("❌ No analysis results to process")
                return
            
            # Step 2: Generate insights
            stock_insights, portfolio_insights = self.generate_insights(analysis_results)
            
            # Step 3: Print summary report
            self.print_summary_report(analysis_results, stock_insights, portfolio_insights)
            
            # Step 4: Save results if requested
            if save_results:
                self.save_results(analysis_results, stock_insights, portfolio_insights)
            
            # Step 5: Generate detailed report
            print("\n" + "="*60)
            print("📋 DETAILED INSIGHTS REPORT")
            print("="*60)
            detailed_report = self.insights_generator.format_insights_report(
                stock_insights, portfolio_insights
            )
            print(detailed_report)
            
        except Exception as e:
            print(f"❌ Error during portfolio scan: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Main function to run the portfolio scanner."""
    print("🤖 StonkBot007 - Portfolio Scanner")
    print("=" * 40)
    print("Scanning news for stock mentions and generating actionable insights...")
    print()
    
    # Initialize scanner
    scanner = PortfolioScanner()
    
    # Custom keywords (can be modified) - shorter list to avoid API limits
    custom_keywords = [
        "stock market", "earnings", "quarterly results", "IPO", "mergers",
        "Sensex", "Nifty", "Indian stocks", "dividend", "RBI", "banking",
        "Reliance", "TCS", "HDFC", "Infosys", "ICICI", "Kotak", "ITC"
    ]
    
    # Run the full scan
    scanner.run_full_scan(
        keywords=custom_keywords,
        country="India",
        max_articles=150,  # Scan up to 150 articles
        save_results=True
    )

if __name__ == "__main__":
    main()
