#!/usr/bin/env python3
"""
Insights Generator - Generates actionable investment insights based on news analysis
"""

from typing import List, Dict, Tuple
from datetime import datetime
import json

class InsightsGenerator:
    def __init__(self):
        """Initialize the insights generator."""
        self.risk_levels = {
            'low': 'Conservative - Suitable for risk-averse investors',
            'medium': 'Moderate - Balanced risk-reward profile',
            'high': 'Aggressive - High risk, high potential reward'
        }
        
        self.time_horizons = {
            'short': '1-3 months',
            'medium': '3-12 months', 
            'long': '1+ years'
        }

    def generate_stock_insights(self, stock_data: Dict[str, Dict]) -> List[Dict]:
        """
        Generate actionable insights for individual stocks.
        
        Args:
            stock_data: Dictionary containing stock sentiment and frequency data
            
        Returns:
            List of insight dictionaries for each stock
        """
        insights = []
        
        for symbol, data in stock_data.items():
            insight = {
                'symbol': symbol,
                'company': data.get('company', 'Unknown'),
                'mentions': data.get('mentions', 0),
                'sentiment': data.get('sentiment', 'neutral'),
                'confidence': data.get('confidence', 0.0),
                'recommendation': self._get_recommendation(data),
                'risk_level': self._assess_risk_level(data),
                'time_horizon': self._get_time_horizon(data),
                'key_factors': self._identify_key_factors(data),
                'action_items': self._generate_action_items(data),
                'price_outlook': self._get_price_outlook(data),
                'sector_impact': self._assess_sector_impact(symbol, data)
            }
            insights.append(insight)
        
        return insights

    def _get_recommendation(self, data: Dict) -> str:
        """Generate buy/sell/hold recommendation based on data."""
        sentiment = data.get('sentiment', 'neutral')
        confidence = data.get('confidence', 0.0)
        mentions = data.get('mentions', 0)
        
        if sentiment == 'positive' and confidence > 0.7 and mentions >= 3:
            return 'BUY - Strong positive sentiment with high confidence'
        elif sentiment == 'positive' and confidence > 0.5:
            return 'BUY - Positive sentiment, consider for portfolio'
        elif sentiment == 'negative' and confidence > 0.7 and mentions >= 3:
            return 'SELL - Strong negative sentiment, consider exiting'
        elif sentiment == 'negative' and confidence > 0.5:
            return 'HOLD - Negative sentiment, monitor closely'
        elif mentions >= 5:
            return 'HOLD - High news volume, wait for clearer direction'
        else:
            return 'HOLD - Neutral sentiment, maintain current position'

    def _assess_risk_level(self, data: Dict) -> str:
        """Assess risk level based on sentiment volatility and mentions."""
        mentions = data.get('mentions', 0)
        confidence = data.get('confidence', 0.0)
        sentiment = data.get('sentiment', 'neutral')
        
        if mentions >= 5 and confidence > 0.8:
            return 'high'  # High attention + high confidence = high risk
        elif mentions >= 3 and confidence > 0.6:
            return 'medium'
        else:
            return 'low'

    def _get_time_horizon(self, data: Dict) -> str:
        """Determine appropriate time horizon for investment."""
        sentiment = data.get('sentiment', 'neutral')
        confidence = data.get('confidence', 0.0)
        
        if sentiment == 'positive' and confidence > 0.7:
            return 'short'  # Strong positive sentiment = short-term opportunity
        elif sentiment == 'negative' and confidence > 0.7:
            return 'short'  # Strong negative sentiment = short-term risk
        else:
            return 'medium'  # Neutral or moderate sentiment = medium-term

    def _identify_key_factors(self, data: Dict) -> List[str]:
        """Identify key factors driving the stock's sentiment."""
        factors = []
        sentiment = data.get('sentiment', 'neutral')
        mentions = data.get('mentions', 0)
        confidence = data.get('confidence', 0.0)
        
        if mentions >= 5:
            factors.append('High media attention')
        
        if confidence > 0.7:
            factors.append('Strong sentiment signal')
        
        if sentiment == 'positive':
            factors.extend(['Positive news flow', 'Potential upside opportunity'])
        elif sentiment == 'negative':
            factors.extend(['Negative news flow', 'Downside risk present'])
        
        if mentions >= 3:
            factors.append('Multiple news sources confirming trend')
        
        return factors

    def _generate_action_items(self, data: Dict) -> List[str]:
        """Generate specific action items for investors."""
        actions = []
        sentiment = data.get('sentiment', 'neutral')
        confidence = data.get('confidence', 0.0)
        mentions = data.get('mentions', 0)
        
        if sentiment == 'positive' and confidence > 0.6:
            actions.append('Consider adding to portfolio if not already held')
            actions.append('Set stop-loss at 5-10% below current price')
            if confidence > 0.8:
                actions.append('Consider increasing position size for high conviction')
        
        elif sentiment == 'negative' and confidence > 0.6:
            actions.append('Review current position and consider reducing exposure')
            actions.append('Set tighter stop-loss to protect capital')
            if confidence > 0.8:
                actions.append('Consider exiting position if risk tolerance is low')
        
        else:
            actions.append('Monitor news flow for clearer direction')
            actions.append('Maintain current position size')
        
        if mentions >= 5:
            actions.append('Set up price alerts for significant moves')
            actions.append('Monitor earnings calendar for upcoming events')
        
        actions.append('Review quarterly results and management commentary')
        actions.append('Check analyst upgrades/downgrades')
        
        return actions

    def _get_price_outlook(self, data: Dict) -> str:
        """Generate price outlook based on sentiment analysis."""
        sentiment = data.get('sentiment', 'neutral')
        confidence = data.get('confidence', 0.0)
        mentions = data.get('mentions', 0)
        
        if sentiment == 'positive' and confidence > 0.7:
            if mentions >= 5:
                return 'Bullish - Strong positive momentum expected'
            else:
                return 'Moderately Bullish - Positive trend developing'
        elif sentiment == 'negative' and confidence > 0.7:
            if mentions >= 5:
                return 'Bearish - Strong negative pressure expected'
            else:
                return 'Moderately Bearish - Negative trend developing'
        else:
            return 'Neutral - Mixed signals, sideways movement likely'

    def _assess_sector_impact(self, symbol: str, data: Dict) -> str:
        """Assess potential sector-wide impact."""
        # Basic sector mapping (can be expanded)
        sector_mapping = {
            'RELIANCE': 'Energy & Petrochemicals',
            'TCS': 'IT Services',
            'HDFC': 'Banking & Financial Services',
            'INFOSYS': 'IT Services',
            'ICICI': 'Banking & Financial Services',
            'KOTAK': 'Banking & Financial Services',
            'ITC': 'FMCG & Tobacco',
            'BHARTI': 'Telecommunications',
            'MARUTI': 'Automotive',
            'TATA': 'Conglomerate'
        }
        
        sector = 'Unknown'
        for key, value in sector_mapping.items():
            if key in symbol.upper():
                sector = value
                break
        
        mentions = data.get('mentions', 0)
        sentiment = data.get('sentiment', 'neutral')
        
        if mentions >= 3:
            if sentiment == 'positive':
                return f'Positive sector impact expected in {sector}'
            elif sentiment == 'negative':
                return f'Negative sector impact possible in {sector}'
        
        return f'Monitor {sector} sector for broader trends'

    def generate_portfolio_insights(self, all_insights: List[Dict]) -> Dict:
        """
        Generate overall portfolio-level insights.
        
        Args:
            all_insights: List of individual stock insights
            
        Returns:
            Dictionary containing portfolio-level analysis
        """
        total_stocks = len(all_insights)
        positive_stocks = len([i for i in all_insights if i['sentiment'] == 'positive'])
        negative_stocks = len([i for i in all_insights if i['sentiment'] == 'negative'])
        neutral_stocks = len([i for i in all_insights if i['sentiment'] == 'neutral'])
        
        # Calculate portfolio sentiment
        if positive_stocks > negative_stocks:
            portfolio_sentiment = 'positive'
        elif negative_stocks > positive_stocks:
            portfolio_sentiment = 'negative'
        else:
            portfolio_sentiment = 'neutral'
        
        # Risk assessment
        high_risk_stocks = len([i for i in all_insights if i['risk_level'] == 'high'])
        medium_risk_stocks = len([i for i in all_insights if i['risk_level'] == 'medium'])
        low_risk_stocks = len([i for i in all_insights if i['risk_level'] == 'low'])
        
        # Top recommendations
        buy_recommendations = [i for i in all_insights if 'BUY' in i['recommendation']]
        sell_recommendations = [i for i in all_insights if 'SELL' in i['recommendation']]
        
        return {
            'portfolio_sentiment': portfolio_sentiment,
            'total_stocks_analyzed': total_stocks,
            'sentiment_breakdown': {
                'positive': positive_stocks,
                'negative': negative_stocks,
                'neutral': neutral_stocks
            },
            'risk_breakdown': {
                'high_risk': high_risk_stocks,
                'medium_risk': medium_risk_stocks,
                'low_risk': low_risk_stocks
            },
            'top_buy_recommendations': buy_recommendations[:5],
            'top_sell_recommendations': sell_recommendations[:5],
            'portfolio_recommendation': self._get_portfolio_recommendation(
                portfolio_sentiment, high_risk_stocks, total_stocks
            ),
            'key_risks': self._identify_portfolio_risks(all_insights),
            'opportunities': self._identify_portfolio_opportunities(all_insights)
        }

    def _get_portfolio_recommendation(self, sentiment: str, high_risk: int, total: int) -> str:
        """Generate overall portfolio recommendation."""
        risk_ratio = high_risk / total if total > 0 else 0
        
        if sentiment == 'positive' and risk_ratio < 0.3:
            return 'Consider increasing equity allocation - positive sentiment with manageable risk'
        elif sentiment == 'negative' and risk_ratio > 0.5:
            return 'Consider reducing equity allocation - negative sentiment with high risk'
        elif risk_ratio > 0.6:
            return 'High risk exposure - consider diversification and risk management'
        else:
            return 'Maintain current allocation - balanced risk-reward profile'

    def _identify_portfolio_risks(self, insights: List[Dict]) -> List[str]:
        """Identify key portfolio risks."""
        risks = []
        
        high_risk_count = len([i for i in insights if i['risk_level'] == 'high'])
        negative_count = len([i for i in insights if i['sentiment'] == 'negative'])
        
        if high_risk_count > 3:
            risks.append('High concentration of high-risk stocks')
        
        if negative_count > len(insights) * 0.4:
            risks.append('High proportion of negative sentiment stocks')
        
        # Check for sector concentration
        sectors = {}
        for insight in insights:
            sector = insight.get('sector_impact', 'Unknown').split(' in ')[-1]
            sectors[sector] = sectors.get(sector, 0) + 1
        
        max_sector_count = max(sectors.values()) if sectors else 0
        if max_sector_count > len(insights) * 0.5:
            risks.append('High sector concentration - consider diversification')
        
        return risks

    def _identify_portfolio_opportunities(self, insights: List[Dict]) -> List[str]:
        """Identify portfolio opportunities."""
        opportunities = []
        
        positive_count = len([i for i in insights if i['sentiment'] == 'positive'])
        high_confidence_count = len([i for i in insights if i['confidence'] > 0.7])
        
        if positive_count > len(insights) * 0.6:
            opportunities.append('Strong positive sentiment across portfolio')
        
        if high_confidence_count > 3:
            opportunities.append('Multiple high-confidence opportunities identified')
        
        # Check for undervalued opportunities
        low_mention_positive = [i for i in insights if i['sentiment'] == 'positive' and i['mentions'] < 3]
        if low_mention_positive:
            opportunities.append('Potential undervalued opportunities with positive sentiment')
        
        return opportunities

    def format_insights_report(self, stock_insights: List[Dict], portfolio_insights: Dict) -> str:
        """
        Format insights into a readable report.
        
        Args:
            stock_insights: List of individual stock insights
            portfolio_insights: Portfolio-level insights
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("📊 PORTFOLIO SCANNER INSIGHTS REPORT")
        report.append("=" * 50)
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Portfolio Overview
        report.append("📈 PORTFOLIO OVERVIEW")
        report.append("-" * 25)
        report.append(f"Total Stocks Analyzed: {portfolio_insights['total_stocks_analyzed']}")
        report.append(f"Overall Sentiment: {portfolio_insights['portfolio_sentiment'].upper()}")
        report.append(f"Portfolio Recommendation: {portfolio_insights['portfolio_recommendation']}")
        report.append("")
        
        # Sentiment Breakdown
        report.append("📊 SENTIMENT BREAKDOWN")
        report.append("-" * 22)
        breakdown = portfolio_insights['sentiment_breakdown']
        report.append(f"Positive: {breakdown['positive']} stocks")
        report.append(f"Negative: {breakdown['negative']} stocks")
        report.append(f"Neutral: {breakdown['neutral']} stocks")
        report.append("")
        
        # Risk Assessment
        report.append("⚠️ RISK ASSESSMENT")
        report.append("-" * 18)
        risk_breakdown = portfolio_insights['risk_breakdown']
        report.append(f"High Risk: {risk_breakdown['high_risk']} stocks")
        report.append(f"Medium Risk: {risk_breakdown['medium_risk']} stocks")
        report.append(f"Low Risk: {risk_breakdown['low_risk']} stocks")
        report.append("")
        
        # Top Recommendations
        if portfolio_insights['top_buy_recommendations']:
            report.append("🟢 TOP BUY RECOMMENDATIONS")
            report.append("-" * 28)
            for stock in portfolio_insights['top_buy_recommendations']:
                report.append(f"• {stock['symbol']} ({stock['company']})")
                report.append(f"  {stock['recommendation']}")
                report.append(f"  Risk: {stock['risk_level'].upper()}, Confidence: {stock['confidence']:.2f}")
                report.append("")
        
        if portfolio_insights['top_sell_recommendations']:
            report.append("🔴 TOP SELL RECOMMENDATIONS")
            report.append("-" * 28)
            for stock in portfolio_insights['top_sell_recommendations']:
                report.append(f"• {stock['symbol']} ({stock['company']})")
                report.append(f"  {stock['recommendation']}")
                report.append(f"  Risk: {stock['risk_level'].upper()}, Confidence: {stock['confidence']:.2f}")
                report.append("")
        
        # Individual Stock Analysis
        report.append("📋 INDIVIDUAL STOCK ANALYSIS")
        report.append("-" * 30)
        for stock in stock_insights:
            report.append(f"\n🔸 {stock['symbol']} ({stock['company']})")
            report.append(f"   Mentions: {stock['mentions']}")
            report.append(f"   Sentiment: {stock['sentiment'].upper()} (Confidence: {stock['confidence']:.2f})")
            report.append(f"   Recommendation: {stock['recommendation']}")
            report.append(f"   Risk Level: {stock['risk_level'].upper()}")
            report.append(f"   Time Horizon: {stock['time_horizon']}")
            report.append(f"   Price Outlook: {stock['price_outlook']}")
            
            if stock['key_factors']:
                report.append(f"   Key Factors: {', '.join(stock['key_factors'])}")
            
            if stock['action_items']:
                report.append("   Action Items:")
                for item in stock['action_items']:
                    report.append(f"     • {item}")
        
        # Portfolio Risks and Opportunities
        if portfolio_insights['key_risks']:
            report.append("\n⚠️ KEY PORTFOLIO RISKS")
            report.append("-" * 25)
            for risk in portfolio_insights['key_risks']:
                report.append(f"• {risk}")
        
        if portfolio_insights['opportunities']:
            report.append("\n💡 PORTFOLIO OPPORTUNITIES")
            report.append("-" * 27)
            for opportunity in portfolio_insights['opportunities']:
                report.append(f"• {opportunity}")
        
        report.append("\n" + "=" * 50)
        report.append("⚠️ DISCLAIMER: This analysis is based on news sentiment and should not be considered as financial advice. Please consult with a financial advisor before making investment decisions.")
        
        return "\n".join(report)


if __name__ == "__main__":
    # Test the insights generator
    generator = InsightsGenerator()
    
    # Sample stock data
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
        },
        'HDFC': {
            'company': 'HDFC Bank',
            'mentions': 4,
            'sentiment': 'positive',
            'confidence': 0.7
        }
    }
    
    print("🔍 Insights Generator Test")
    print("=" * 40)
    
    # Generate individual stock insights
    stock_insights = generator.generate_stock_insights(sample_stock_data)
    
    # Generate portfolio insights
    portfolio_insights = generator.generate_portfolio_insights(stock_insights)
    
    # Format and display report
    report = generator.format_insights_report(stock_insights, portfolio_insights)
    print(report)
