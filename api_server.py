#!/usr/bin/env python3
"""
API Server for StonkBot007 Portfolio Scanner Frontend
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
from typing import List, Dict
import threading
import time

# Import our portfolio scanner components
from portfolio_scanner import PortfolioScanner
from stock_extractor import StockExtractor
from sentiment_analyzer import SentimentAnalyzer
from insights_generator import InsightsGenerator

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize components
portfolio_scanner = PortfolioScanner()
stock_extractor = StockExtractor()
sentiment_analyzer = SentimentAnalyzer()
insights_generator = InsightsGenerator()

# Store analysis results in memory (in production, use a database)
analysis_cache = {}

@app.route('/')
def serve_frontend():
    """Serve the main frontend page."""
    return send_from_directory('.', 'frontend_portfolio_scanner.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files like images, CSS, JS."""
    return send_from_directory('.', filename)

@app.route('/api/scan-portfolio', methods=['POST'])
def scan_portfolio():
    """
    Scan portfolio stocks for news mentions and sentiment analysis.
    
    Expected JSON payload:
    {
        "stocks": ["RELIANCE", "TCS", "HDFC", ...]
    }
    """
    try:
        data = request.get_json()
        if not data or 'stocks' not in data:
            return jsonify({'error': 'No stocks provided'}), 400
        
        stocks = data['stocks']
        if not isinstance(stocks, list) or len(stocks) == 0:
            return jsonify({'error': 'Invalid stocks list'}), 400
        
        print(f"🔍 Scanning portfolio with {len(stocks)} stocks: {stocks}")
        
        # Generate a unique analysis ID
        analysis_id = f"analysis_{int(time.time())}"
        
        # Start analysis in background thread
        thread = threading.Thread(
            target=run_portfolio_analysis,
            args=(analysis_id, stocks)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'analysis_id': analysis_id,
            'status': 'started',
            'message': 'Portfolio analysis started'
        })
        
    except Exception as e:
        print(f"❌ Error in scan_portfolio: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis-status/<analysis_id>')
def get_analysis_status(analysis_id):
    """Get the status of a portfolio analysis."""
    try:
        if analysis_id in analysis_cache:
            result = analysis_cache[analysis_id]
            return jsonify(result)
        else:
            return jsonify({
                'status': 'not_found',
                'message': 'Analysis not found'
            }), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-stocks', methods=['POST'])
def analyze_stocks():
    """
    Analyze specific stocks for sentiment and insights.
    
    Expected JSON payload:
    {
        "stocks": ["RELIANCE", "TCS", "HDFC", ...]
    }
    """
    try:
        data = request.get_json()
        if not data or 'stocks' not in data:
            return jsonify({'error': 'No stocks provided'}), 400
        
        stocks = data['stocks']
        print(f"📊 Analyzing {len(stocks)} stocks: {stocks}")
        
        # Fetch news articles
        keywords = [
            "stock market", "earnings", "quarterly results", "IPO", "mergers",
            "Sensex", "Nifty", "Indian stocks", "dividend", "RBI", "banking"
        ] + stocks  # Add stock symbols as keywords
        
        articles, analysis_results = portfolio_scanner.scan_news_for_stocks(
            keywords=keywords,
            country="India",
            max_articles=100
        )
        
        if not analysis_results:
            return jsonify({'error': 'No analysis results available'}), 500
        
        # Filter analysis for requested stocks
        filtered_stocks = [s for s in stocks if s in analysis_results.get('stock_sentiments', {})]
        
        if not filtered_stocks:
            # If no stocks found in news, create mock analysis
            return jsonify(create_mock_analysis(stocks))
        
        # Generate insights for filtered stocks
        stock_data = {}
        for symbol in filtered_stocks:
            sentiment_data = analysis_results['stock_sentiments'].get(symbol, {})
            if sentiment_data.get('total_mentions', 0) > 0:
                stock_data[symbol] = {
                    'company': stock_extractor.symbol_to_company.get(symbol, 'Unknown'),
                    'mentions': sentiment_data['total_mentions'],
                    'sentiment': sentiment_data['overall_sentiment'],
                    'confidence': sentiment_data['confidence']
                }
        
        # Generate insights
        stock_insights = insights_generator.generate_stock_insights(stock_data)
        portfolio_insights = insights_generator.generate_portfolio_insights(stock_insights)
        
        # Format response
        response = {
            'portfolio_sentiment': portfolio_insights.get('portfolio_sentiment', 'neutral'),
            'total_stocks_analyzed': len(stock_data),
            'sentiment_breakdown': portfolio_insights.get('sentiment_breakdown', {}),
            'stock_insights': []
        }
        
        for insight in stock_insights:
            response['stock_insights'].append({
                'symbol': insight['symbol'],
                'company': insight['company'],
                'mentions': insight['mentions'],
                'sentiment': insight['sentiment'],
                'confidence': insight['confidence'],
                'recommendation': insight['recommendation'],
                'risk_level': insight['risk_level'],
                'price_outlook': insight['price_outlook'],
                'key_factors': insight['key_factors'],
                'action_items': insight['action_items']
            })
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error in analyze_stocks: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/news')
def get_news():
    """Get recent financial news."""
    try:
        keywords = [
            "stock market", "earnings", "quarterly results", "IPO", "mergers",
            "Sensex", "Nifty", "Indian stocks", "dividend", "RBI", "banking"
        ]
        
        articles, _ = portfolio_scanner.scan_news_for_stocks(
            keywords=keywords,
            country="India",
            max_articles=20
        )
        
        news_items = []
        for i, article in enumerate(articles[:10]):  # Limit to 10 articles
            # Extract title and content from article
            lines = article.split('\n')
            title = lines[0].replace('Title: ', '') if lines[0].startswith('Title: ') else f"News Item {i+1}"
            content = lines[1].replace('Content: ', '') if len(lines) > 1 and lines[1].startswith('Content: ') else "No content available"
            
            # Analyze sentiment
            sentiment = sentiment_analyzer.analyze_sentiment(article)
            
            news_items.append({
                'title': title,
                'content': content,
                'sentiment': sentiment['sentiment'],
                'confidence': sentiment['confidence']
            })
        
        return jsonify({
            'articles': news_items,
            'total_articles': len(news_items)
        })
        
    except Exception as e:
        print(f"❌ Error in get_news: {e}")
        return jsonify({'error': str(e)}), 500

def run_portfolio_analysis(analysis_id: str, stocks: List[str]):
    """Run portfolio analysis in background thread."""
    try:
        print(f"🚀 Starting analysis {analysis_id} for stocks: {stocks}")
        
        # Update status to running
        analysis_cache[analysis_id] = {
            'status': 'running',
            'progress': 0,
            'message': 'Fetching news articles...'
        }
        
        # Fetch news articles
        keywords = [
            "stock market", "earnings", "quarterly results", "IPO", "mergers",
            "Sensex", "Nifty", "Indian stocks", "dividend", "RBI", "banking"
        ] + stocks
        
        analysis_cache[analysis_id]['progress'] = 25
        analysis_cache[analysis_id]['message'] = 'Analyzing stock mentions...'
        
        articles, analysis_results = portfolio_scanner.scan_news_for_stocks(
            keywords=keywords,
            country="India",
            max_articles=100
        )
        
        analysis_cache[analysis_id]['progress'] = 50
        analysis_cache[analysis_id]['message'] = 'Generating insights...'
        
        # Generate insights
        stock_data = {}
        for symbol in stocks:
            sentiment_data = analysis_results.get('stock_sentiments', {}).get(symbol, {})
            if sentiment_data.get('total_mentions', 0) > 0:
                stock_data[symbol] = {
                    'company': stock_extractor.symbol_to_company.get(symbol, 'Unknown'),
                    'mentions': sentiment_data['total_mentions'],
                    'sentiment': sentiment_data['overall_sentiment'],
                    'confidence': sentiment_data['confidence']
                }
        
        # If no stocks found in news, create mock analysis
        if not stock_data:
            analysis_cache[analysis_id] = create_mock_analysis(stocks)
            analysis_cache[analysis_id]['status'] = 'completed'
            return
        
        stock_insights = insights_generator.generate_stock_insights(stock_data)
        portfolio_insights = insights_generator.generate_portfolio_insights(stock_insights)
        
        analysis_cache[analysis_id]['progress'] = 75
        analysis_cache[analysis_id]['message'] = 'Finalizing results...'
        
        # Format final results
        analysis_cache[analysis_id] = {
            'status': 'completed',
            'progress': 100,
            'message': 'Analysis completed successfully',
            'portfolio_sentiment': portfolio_insights.get('portfolio_sentiment', 'neutral'),
            'total_stocks_analyzed': len(stock_data),
            'sentiment_breakdown': portfolio_insights.get('sentiment_breakdown', {}),
            'stock_insights': []
        }
        
        for insight in stock_insights:
            analysis_cache[analysis_id]['stock_insights'].append({
                'symbol': insight['symbol'],
                'company': insight['company'],
                'mentions': insight['mentions'],
                'sentiment': insight['sentiment'],
                'confidence': insight['confidence'],
                'recommendation': insight['recommendation'],
                'risk_level': insight['risk_level'],
                'price_outlook': insight['price_outlook'],
                'key_factors': insight['key_factors'],
                'action_items': insight['action_items']
            })
        
        print(f"✅ Analysis {analysis_id} completed successfully")
        
    except Exception as e:
        print(f"❌ Error in analysis {analysis_id}: {e}")
        analysis_cache[analysis_id] = {
            'status': 'error',
            'progress': 0,
            'message': f'Analysis failed: {str(e)}',
            'error': str(e)
        }

def create_mock_analysis(stocks: List[str]) -> Dict:
    """Create mock analysis data for demonstration."""
    import random
    
    stock_insights = []
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    for symbol in stocks:
        sentiment = random.choice(['positive', 'negative', 'neutral'])
        if sentiment == 'positive':
            positive_count += 1
        elif sentiment == 'negative':
            negative_count += 1
        else:
            neutral_count += 1
        
        stock_insights.append({
            'symbol': symbol,
            'company': stock_extractor.symbol_to_company.get(symbol, 'Unknown'),
            'mentions': random.randint(1, 10),
            'sentiment': sentiment,
            'confidence': random.uniform(0.3, 0.9),
            'recommendation': random.choice(['BUY', 'SELL', 'HOLD']),
            'risk_level': random.choice(['low', 'medium', 'high']),
            'price_outlook': random.choice(['Bullish', 'Bearish', 'Neutral']),
            'key_factors': random.choice(['Strong earnings', 'Market volatility', 'Sector growth', 'Regulatory changes']),
            'action_items': random.choice(['Monitor closely', 'Consider adding', 'Hold position', 'Review quarterly results'])
        })
    
    portfolio_sentiment = 'positive' if positive_count > negative_count else 'negative' if negative_count > positive_count else 'neutral'
    
    return {
        'status': 'completed',
        'progress': 100,
        'message': 'Mock analysis completed',
        'portfolio_sentiment': portfolio_sentiment,
        'total_stocks_analyzed': len(stocks),
        'sentiment_breakdown': {
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count
        },
        'stock_insights': stock_insights
    }

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

def find_available_port(start_port=5000, max_attempts=10):
    """Find an available port starting from start_port."""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

if __name__ == '__main__':
    print("🚀 Starting StonkBot007 API Server...")
    
    # Find available port
    port = find_available_port(5000)
    if port is None:
        print("❌ No available ports found in range 5000-5009")
        exit(1)
    
    print(f"📊 Portfolio Scanner API is running on http://localhost:{port}")
    print(f"🌐 Frontend available at http://localhost:{port}")
    print("📚 API Documentation:")
    print("   POST /api/scan-portfolio - Scan portfolio stocks")
    print("   GET  /api/analysis-status/<id> - Get analysis status")
    print("   POST /api/analyze-stocks - Analyze specific stocks")
    print("   GET  /api/news - Get recent financial news")
    print("   GET  /api/health - Health check")
    print("\n" + "="*50)
    
    app.run(debug=True, host='0.0.0.0', port=port)
