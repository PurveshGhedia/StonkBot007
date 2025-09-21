#!/usr/bin/env python3
"""
Sentiment Analyzer - Analyzes sentiment of news articles for stock insights
"""

import re
from typing import List, Dict, Tuple
from collections import defaultdict

class SentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analyzer with positive and negative word lists."""
        # Positive sentiment words
        self.positive_words = {
            'strong', 'growth', 'surge', 'rise', 'gain', 'profit', 'increase', 'up', 'positive',
            'bullish', 'optimistic', 'excellent', 'outstanding', 'robust', 'solid', 'record',
            'breakthrough', 'success', 'win', 'victory', 'boom', 'rally', 'soar', 'jump',
            'leap', 'advance', 'improve', 'better', 'best', 'excellent', 'superior', 'premium',
            'dividend', 'bonus', 'acquisition', 'merger', 'partnership', 'expansion', 'launch',
            'innovation', 'breakthrough', 'milestone', 'achievement', 'success', 'outperform',
            'beat', 'exceed', 'surpass', 'outstanding', 'remarkable', 'exceptional', 'stellar',
            'momentum', 'acceleration', 'recovery', 'rebound', 'turnaround', 'transformation',
            'upgrade', 'upward', 'ascending', 'climbing', 'rising', 'growing', 'expanding',
            'thriving', 'flourishing', 'prosperous', 'successful', 'profitable', 'lucrative',
            'promising', 'bright', 'optimistic', 'confident', 'hopeful', 'encouraging',
            'favorable', 'beneficial', 'advantageous', 'positive', 'constructive', 'productive'
        }
        
        # Negative sentiment words
        self.negative_words = {
            'decline', 'fall', 'drop', 'loss', 'decrease', 'down', 'negative', 'bearish',
            'pessimistic', 'poor', 'weak', 'disappointing', 'concerning', 'worrying', 'troubling',
            'crisis', 'crash', 'plunge', 'slump', 'downturn', 'recession', 'depression',
            'bankruptcy', 'default', 'failure', 'collapse', 'breakdown', 'deterioration',
            'decline', 'shrinking', 'contracting', 'reducing', 'cutting', 'slashing', 'trimming',
            'layoff', 'firing', 'job cuts', 'restructuring', 'downsizing', 'closure', 'shutdown',
            'delay', 'postpone', 'cancel', 'suspend', 'halt', 'stop', 'freeze', 'pause',
            'investigation', 'probe', 'scandal', 'corruption', 'fraud', 'illegal', 'violation',
            'penalty', 'fine', 'sanction', 'punishment', 'warning', 'caution', 'risk',
            'uncertainty', 'volatility', 'instability', 'unstable', 'unreliable', 'unpredictable',
            'challenging', 'difficult', 'struggle', 'hardship', 'adversity', 'obstacle',
            'barrier', 'hindrance', 'impediment', 'problem', 'issue', 'concern', 'worry',
            'anxiety', 'fear', 'panic', 'alarm', 'alert', 'danger', 'threat', 'risk',
            'vulnerable', 'exposed', 'susceptible', 'fragile', 'brittle', 'weak', 'failing'
        }
        
        # Market-specific terms
        self.market_positive = {
            'bull market', 'rally', 'surge', 'boom', 'growth', 'expansion', 'recovery',
            'rebound', 'turnaround', 'momentum', 'acceleration', 'breakthrough', 'milestone',
            'record high', 'all-time high', 'new high', 'peak', 'summit', 'top', 'maximum',
            'dividend increase', 'bonus', 'stock split', 'buyback', 'acquisition', 'merger',
            'partnership', 'deal', 'agreement', 'contract', 'order', 'booking', 'revenue',
            'profit', 'earnings', 'margin', 'efficiency', 'productivity', 'innovation'
        }
        
        self.market_negative = {
            'bear market', 'crash', 'plunge', 'slump', 'downturn', 'recession', 'depression',
            'correction', 'volatility', 'uncertainty', 'instability', 'crisis', 'panic',
            'sell-off', 'liquidation', 'bankruptcy', 'default', 'downgrade', 'cut', 'reduction',
            'loss', 'deficit', 'shortfall', 'miss', 'disappointment', 'concern', 'worry',
            'risk', 'threat', 'challenge', 'obstacle', 'barrier', 'problem', 'issue'
        }

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of a text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary with sentiment scores and overall sentiment
        """
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        positive_count = 0
        negative_count = 0
        total_words = len(words)
        
        # Count positive and negative words
        for word in words:
            if word in self.positive_words:
                positive_count += 1
            elif word in self.negative_words:
                negative_count += 1
        
        # Check for market-specific terms
        for phrase in self.market_positive:
            if phrase in text_lower:
                positive_count += 2  # Weight market terms higher
        
        for phrase in self.market_negative:
            if phrase in text_lower:
                negative_count += 2  # Weight market terms higher
        
        # Calculate sentiment scores
        positive_score = positive_count / total_words if total_words > 0 else 0
        negative_score = negative_count / total_words if total_words > 0 else 0
        
        # Determine overall sentiment
        if positive_score > negative_score:
            sentiment = 'positive'
            confidence = positive_score
        elif negative_score > positive_score:
            sentiment = 'negative'
            confidence = negative_score
        else:
            sentiment = 'neutral'
            confidence = 0.5
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'positive_score': positive_score,
            'negative_score': negative_score,
            'positive_count': positive_count,
            'negative_count': negative_count
        }

    def analyze_stock_sentiment(self, articles: List[str], stock_symbols: List[str]) -> Dict[str, Dict]:
        """
        Analyze sentiment for specific stock symbols across articles.
        
        Args:
            articles: List of news articles
            stock_symbols: List of stock symbols to analyze
            
        Returns:
            Dictionary mapping stock symbols to their sentiment analysis
        """
        stock_sentiments = defaultdict(lambda: {
            'positive_articles': 0,
            'negative_articles': 0,
            'neutral_articles': 0,
            'total_mentions': 0,
            'sentiment_scores': [],
            'overall_sentiment': 'neutral',
            'confidence': 0.0
        })
        
        for article in articles:
            article_upper = article.upper()
            sentiment = self.analyze_sentiment(article)
            
            for symbol in stock_symbols:
                if symbol in article_upper:
                    stock_sentiments[symbol]['total_mentions'] += 1
                    stock_sentiments[symbol]['sentiment_scores'].append(sentiment['confidence'])
                    
                    if sentiment['sentiment'] == 'positive':
                        stock_sentiments[symbol]['positive_articles'] += 1
                    elif sentiment['sentiment'] == 'negative':
                        stock_sentiments[symbol]['negative_articles'] += 1
                    else:
                        stock_sentiments[symbol]['neutral_articles'] += 1
        
        # Calculate overall sentiment for each stock
        for symbol, data in stock_sentiments.items():
            if data['total_mentions'] > 0:
                if data['positive_articles'] > data['negative_articles']:
                    data['overall_sentiment'] = 'positive'
                    data['confidence'] = data['positive_articles'] / data['total_mentions']
                elif data['negative_articles'] > data['positive_articles']:
                    data['overall_sentiment'] = 'negative'
                    data['confidence'] = data['negative_articles'] / data['total_mentions']
                else:
                    data['overall_sentiment'] = 'neutral'
                    data['confidence'] = 0.5
                
                # Calculate average confidence
                if data['sentiment_scores']:
                    data['confidence'] = sum(data['sentiment_scores']) / len(data['sentiment_scores'])
        
        return dict(stock_sentiments)

    def get_sentiment_summary(self, stock_sentiments: Dict[str, Dict]) -> Dict[str, List[str]]:
        """
        Get a summary of sentiment analysis results.
        
        Args:
            stock_sentiments: Dictionary of stock sentiment data
            
        Returns:
            Dictionary categorizing stocks by sentiment
        """
        summary = {
            'positive': [],
            'negative': [],
            'neutral': []
        }
        
        for symbol, data in stock_sentiments.items():
            if data['total_mentions'] > 0:
                summary[data['overall_sentiment']].append({
                    'symbol': symbol,
                    'confidence': data['confidence'],
                    'mentions': data['total_mentions'],
                    'positive_articles': data['positive_articles'],
                    'negative_articles': data['negative_articles']
                })
        
        # Sort by confidence within each category
        for sentiment in summary:
            summary[sentiment].sort(key=lambda x: x['confidence'], reverse=True)
        
        return summary


if __name__ == "__main__":
    # Test the sentiment analyzer
    analyzer = SentimentAnalyzer()
    
    # Sample news articles
    sample_articles = [
        "Reliance Industries reports strong Q3 results with 15% growth in revenue",
        "TCS announces disappointing earnings, stock falls 8%",
        "HDFC Bank stock surges 5% on positive earnings beat",
        "Infosys faces challenges in digital transformation projects",
        "ICICI Bank reports record quarterly profits, declares dividend"
    ]
    
    print("📊 Sentiment Analyzer Test")
    print("=" * 40)
    
    # Analyze each article
    for i, article in enumerate(sample_articles, 1):
        sentiment = analyzer.analyze_sentiment(article)
        print(f"\n📰 Article {i}: {article}")
        print(f"   Sentiment: {sentiment['sentiment']} (confidence: {sentiment['confidence']:.2f})")
        print(f"   Positive: {sentiment['positive_count']}, Negative: {sentiment['negative_count']}")
    
    # Test stock-specific sentiment
    print(f"\n📈 Stock-Specific Sentiment Analysis:")
    print("-" * 40)
    
    stock_symbols = ['RELIANCE', 'TCS', 'HDFC', 'INFOSYS', 'ICICI']
    stock_sentiments = analyzer.analyze_stock_sentiment(sample_articles, stock_symbols)
    
    for symbol, data in stock_sentiments.items():
        if data['total_mentions'] > 0:
            print(f"\n{symbol}:")
            print(f"   Overall: {data['overall_sentiment']} (confidence: {data['confidence']:.2f})")
            print(f"   Mentions: {data['total_mentions']}")
            print(f"   Positive: {data['positive_articles']}, Negative: {data['negative_articles']}")
    
    # Get sentiment summary
    summary = analyzer.get_sentiment_summary(stock_sentiments)
    print(f"\n📋 Sentiment Summary:")
    print("-" * 20)
    for sentiment, stocks in summary.items():
        if stocks:
            print(f"\n{sentiment.upper()}:")
            for stock in stocks:
                print(f"   {stock['symbol']}: {stock['confidence']:.2f} confidence ({stock['mentions']} mentions)")
