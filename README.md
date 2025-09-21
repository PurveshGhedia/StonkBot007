# StonkBot007 - Business News Aggregator & Portfolio Scanner

A comprehensive Python application that fetches business news from India and provides intelligent portfolio scanning with actionable investment insights.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key:**
   - Copy `config.example.py` to `config.py`
   - Get a free API key from [NewsAPI](https://newsapi.org/)
   - Add your API key to `config.py`

3. **Run the application:**
   ```bash
   # Basic news aggregator
   python agent.py
   
   # Portfolio scanner with insights (command-line)
   python portfolio_scanner.py
   
   # Web interface for portfolio scanning
   python start_portfolio_scanner.py
   
   # Demo the portfolio scanner
   python demo_portfolio_scanner.py
   ```

## Features

### News Aggregator
- Fetches business news from India (with fallback to US business news)
- Clean, formatted output with emojis
- Robust error handling
- Smart fallback system for different news sources

### Portfolio Scanner (NEW!)
- **Stock Symbol Extraction**: Automatically identifies stock symbols and company names from news headlines
- **Sentiment Analysis**: Analyzes news sentiment for each stock (positive, negative, neutral)
- **Actionable Insights**: Generates buy/sell/hold recommendations with confidence levels
- **Risk Assessment**: Evaluates risk levels (low, medium, high) for each stock
- **Portfolio Overview**: Provides portfolio-level analysis and recommendations
- **Comprehensive Reporting**: Detailed reports with key factors, action items, and price outlooks

## Portfolio Scanner Capabilities

### Stock Detection
- Recognizes 100+ major Indian companies and their stock symbols
- Extracts stock mentions from news headlines using pattern matching
- Provides confidence levels for detected symbols

### Sentiment Analysis
- Analyzes positive/negative sentiment in news articles
- Market-specific terminology recognition
- Confidence scoring for sentiment accuracy

### Investment Insights
- **Recommendations**: BUY/SELL/HOLD with detailed reasoning
- **Risk Levels**: Conservative, Moderate, or Aggressive risk assessment
- **Time Horizons**: Short-term (1-3 months), Medium-term (3-12 months), Long-term (1+ years)
- **Action Items**: Specific steps for investors to take
- **Price Outlook**: Bullish, Bearish, or Neutral price expectations

### Portfolio Analysis
- Overall portfolio sentiment assessment
- Risk distribution analysis
- Sector impact evaluation
- Key risks and opportunities identification

## Usage Examples

### Basic Portfolio Scan
```python
from portfolio_scanner import PortfolioScanner

scanner = PortfolioScanner()
scanner.run_full_scan(max_articles=100)
```

### Custom Keywords Scan
```python
custom_keywords = [
    "Reliance", "TCS", "HDFC", "earnings", "IPO", "mergers"
]
scanner.run_full_scan(keywords=custom_keywords, max_articles=150)
```

### Individual Component Usage
```python
from stock_extractor import StockExtractor
from sentiment_analyzer import SentimentAnalyzer
from insights_generator import InsightsGenerator

# Extract stocks from news
extractor = StockExtractor()
stocks = extractor.extract_stocks_from_text("Reliance reports strong Q3 results")

# Analyze sentiment
analyzer = SentimentAnalyzer()
sentiment = analyzer.analyze_sentiment("TCS stock surges 5% on positive earnings")

# Generate insights
generator = InsightsGenerator()
insights = generator.generate_stock_insights(stock_data)
```

## Files

### Core Components
- `agent.py` - Original news aggregator entry point
- `portfolio_scanner.py` - Main portfolio scanner with full analysis pipeline
- `news_fetcher.py` - News fetching logic with API integration
- `stock_extractor.py` - Stock symbol extraction and company name recognition
- `sentiment_analyzer.py` - News sentiment analysis for stocks
- `insights_generator.py` - Investment insights and recommendations generator

### Web Interface
- `frontend_portfolio_scanner.html` - Modern web interface for portfolio scanning
- `api_server.py` - Flask API server for frontend communication
- `start_portfolio_scanner.py` - Easy startup script for the web application

### Demo & Documentation
- `demo_portfolio_scanner.py` - Command-line demo of portfolio scanning
- `README_PORTFOLIO_SCANNER.md` - Detailed documentation for the web interface

### Configuration
- `config.py` - API configuration (not tracked in git)
- `config.example.py` - Example configuration file
- `requirements.txt` - Python dependencies

## Sample Output

The portfolio scanner provides comprehensive reports including:

- **Portfolio Overview**: Total stocks analyzed, overall sentiment, recommendations
- **Top Stock Mentions**: Most frequently mentioned stocks in news
- **Sentiment Breakdown**: Positive, negative, and neutral stock counts
- **Risk Assessment**: High, medium, and low risk stock distribution
- **Buy/Sell Recommendations**: Specific stocks with detailed reasoning
- **Individual Stock Analysis**: Detailed analysis for each detected stock
- **Portfolio Risks & Opportunities**: Key risks and opportunities identified

## Disclaimer

This tool is for educational and informational purposes only. The analysis is based on news sentiment and should not be considered as financial advice. Please consult with a qualified financial advisor before making investment decisions.
