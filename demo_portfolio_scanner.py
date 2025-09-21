#!/usr/bin/env python3
"""
Demo script for StonkBot007 Portfolio Scanner
Shows how to use the portfolio scanner programmatically
"""

from portfolio_scanner import PortfolioScanner
from stock_extractor import StockExtractor
from sentiment_analyzer import SentimentAnalyzer
from insights_generator import InsightsGenerator
import json

def demo_portfolio_analysis():
    """Demonstrate portfolio analysis functionality."""
    print("🤖 StonkBot007 - Portfolio Scanner Demo")
    print("=" * 50)
    
    # Initialize components
    scanner = PortfolioScanner()
    extractor = StockExtractor()
    analyzer = SentimentAnalyzer()
    generator = InsightsGenerator()
    
    # Demo portfolio (similar to frontend demo portfolios)
    demo_portfolios = {
        "Priya Sharma": {
            "RELIANCE": 30,
            "TCS": 25,
            "HDFC": 50,
            "INFOSYS": 100,
            "ICICI": 200,
            "KOTAK": 80,
            "ITC": 60,
            "BHARTIARTL": 40,
            "SUNPHARMA": 80,
            "TATAMOTORS": 150
        },
        "Rohan Kapoor": {
            "RELIANCE": 40,
            "TCS": 75,
            "HDFC": 200,
            "INFOSYS": 120,
            "ICICI": 150,
            "KOTAK": 100,
            "ITC": 80,
            "BHARTIARTL": 60,
            "SUNPHARMA": 100,
            "TATAMOTORS": 200,
            "HINDUNILVR": 60,
            "ASIANPAINT": 40
        }
    }
    
    # Analyze each portfolio
    for client_name, portfolio in demo_portfolios.items():
        print(f"\n📊 Analyzing Portfolio: {client_name}")
        print("-" * 40)
        
        # Get stock symbols
        stocks = list(portfolio.keys())
        print(f"📈 Portfolio contains {len(stocks)} stocks: {', '.join(stocks)}")
        
        # Scan news for these stocks
        print("\n🔍 Scanning news for portfolio stocks...")
        articles, analysis_results = scanner.scan_news_for_stocks(
            keywords=stocks + ["stock market", "earnings", "quarterly results"],
            country="India",
            max_articles=50
        )
        
        if not analysis_results:
            print("❌ No analysis results available")
            continue
        
        # Filter for portfolio stocks
        portfolio_stocks = [s for s in stocks if s in analysis_results.get('stock_sentiments', {})]
        print(f"✅ Found {len(portfolio_stocks)} portfolio stocks in news")
        
        if not portfolio_stocks:
            print("📰 No portfolio stocks found in recent news - using mock analysis")
            # Create mock analysis for demonstration
            stock_data = {}
            for symbol in stocks:
                stock_data[symbol] = {
                    'company': extractor.symbol_to_company.get(symbol, 'Unknown'),
                    'mentions': 1,
                    'sentiment': 'neutral',
                    'confidence': 0.5
                }
        else:
            # Prepare stock data for insights
            stock_data = {}
            for symbol in portfolio_stocks:
                sentiment_data = analysis_results['stock_sentiments'][symbol]
                if sentiment_data['total_mentions'] > 0:
                    stock_data[symbol] = {
                        'company': extractor.symbol_to_company.get(symbol, 'Unknown'),
                        'mentions': sentiment_data['total_mentions'],
                        'sentiment': sentiment_data['overall_sentiment'],
                        'confidence': sentiment_data['confidence']
                    }
        
        # Generate insights
        print("\n💡 Generating investment insights...")
        stock_insights = generator.generate_stock_insights(stock_data)
        portfolio_insights = generator.generate_portfolio_insights(stock_insights)
        
        # Display results
        print(f"\n📋 Portfolio Analysis Results for {client_name}")
        print("=" * 50)
        
        # Portfolio overview
        print(f"Overall Sentiment: {portfolio_insights['portfolio_sentiment'].upper()}")
        print(f"Total Stocks Analyzed: {portfolio_insights['total_stocks_analyzed']}")
        
        breakdown = portfolio_insights['sentiment_breakdown']
        print(f"Sentiment Breakdown:")
        print(f"  • Positive: {breakdown['positive']} stocks")
        print(f"  • Negative: {breakdown['negative']} stocks")
        print(f"  • Neutral: {breakdown['neutral']} stocks")
        
        # Top recommendations
        buy_recs = portfolio_insights.get('top_buy_recommendations', [])
        sell_recs = portfolio_insights.get('top_sell_recommendations', [])
        
        if buy_recs:
            print(f"\n🟢 Top BUY Recommendations:")
            for stock in buy_recs[:3]:
                print(f"  • {stock['symbol']} - {stock['recommendation']}")
        
        if sell_recs:
            print(f"\n🔴 Top SELL Recommendations:")
            for stock in sell_recs[:3]:
                print(f"  • {stock['symbol']} - {stock['recommendation']}")
        
        # Individual stock analysis (show first 5)
        print(f"\n📊 Individual Stock Analysis (Top 5):")
        for i, stock in enumerate(stock_insights[:5]):
            print(f"\n{i+1}. {stock['symbol']} ({stock['company']})")
            print(f"   Sentiment: {stock['sentiment'].upper()} (Confidence: {stock['confidence']:.2f})")
            print(f"   Recommendation: {stock['recommendation']}")
            print(f"   Risk Level: {stock['risk_level'].upper()}")
            print(f"   Price Outlook: {stock['price_outlook']}")
            if stock['key_factors']:
                print(f"   Key Factors: {', '.join(stock['key_factors'])}")
        
        print(f"\n💼 Portfolio Recommendation: {portfolio_insights['portfolio_recommendation']}")
        
        # Portfolio risks and opportunities
        if portfolio_insights.get('key_risks'):
            print(f"\n⚠️ Key Risks:")
            for risk in portfolio_insights['key_risks']:
                print(f"  • {risk}")
        
        if portfolio_insights.get('opportunities'):
            print(f"\n💡 Opportunities:")
            for opportunity in portfolio_insights['opportunities']:
                print(f"  • {opportunity}")
        
        print("\n" + "=" * 50)

def demo_individual_components():
    """Demonstrate individual component functionality."""
    print("\n🔧 Individual Component Demo")
    print("=" * 30)
    
    # Stock Extractor Demo
    print("\n📈 Stock Extractor Demo:")
    extractor = StockExtractor()
    sample_text = "Reliance Industries reports strong Q3 results, TCS announces new digital initiatives, HDFC Bank stock surges 5%"
    stocks = extractor.extract_stocks_from_text(sample_text)
    print(f"Text: {sample_text}")
    print("Found stocks:")
    for stock in stocks:
        print(f"  • {stock['symbol']} ({stock['company']}) - {stock['confidence']} confidence")
    
    # Sentiment Analyzer Demo
    print("\n📊 Sentiment Analyzer Demo:")
    analyzer = SentimentAnalyzer()
    sample_articles = [
        "Reliance Industries reports strong Q3 results with 15% growth in revenue",
        "TCS announces disappointing earnings, stock falls 8%",
        "HDFC Bank stock surges 5% on positive earnings beat"
    ]
    
    for i, article in enumerate(sample_articles, 1):
        sentiment = analyzer.analyze_sentiment(article)
        print(f"Article {i}: {article}")
        print(f"  Sentiment: {sentiment['sentiment']} (Confidence: {sentiment['confidence']:.2f})")
        print(f"  Positive: {sentiment['positive_count']}, Negative: {sentiment['negative_count']}")
    
    # Insights Generator Demo
    print("\n💡 Insights Generator Demo:")
    generator = InsightsGenerator()
    sample_stock_data = {
        'RELIANCE': {
            'company': 'Reliance Industries',
            'mentions': 5,
            'sentiment': 'positive',
            'confidence': 0.8
        },
        'TCS': {
            'company': 'Tata Consultancy Services',
            'mentions': 3,
            'sentiment': 'negative',
            'confidence': 0.6
        }
    }
    
    insights = generator.generate_stock_insights(sample_stock_data)
    for insight in insights:
        print(f"\n{insight['symbol']} ({insight['company']}):")
        print(f"  Recommendation: {insight['recommendation']}")
        print(f"  Risk Level: {insight['risk_level'].upper()}")
        print(f"  Price Outlook: {insight['price_outlook']}")
        print(f"  Action Items: {insight['action_items'][0]}")

def main():
    """Main demo function."""
    try:
        # Run portfolio analysis demo
        demo_portfolio_analysis()
        
        # Run individual components demo
        demo_individual_components()
        
        print("\n🎉 Demo completed successfully!")
        print("\n💡 To use the web interface:")
        print("   1. Run: python start_portfolio_scanner.py")
        print("   2. Open: http://localhost:5000")
        print("   3. Login with: priya/password123, rohan/password123, or ananya/password123")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
