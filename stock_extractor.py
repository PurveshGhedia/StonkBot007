#!/usr/bin/env python3
"""
Stock Symbol Extractor - Extracts stock symbols and company names from news headlines
"""

import re
import json
from typing import List, Dict, Set, Tuple

class StockExtractor:
    def __init__(self):
        """Initialize the stock extractor with common stock patterns and known companies."""
        # Common Indian stock symbols patterns
        self.stock_patterns = [
            r'\b[A-Z]{2,6}\b',  # 2-6 letter uppercase symbols
            r'\b[A-Z]{1,2}[0-9]{1,4}\b',  # Mixed alphanumeric symbols
        ]
        
        # Common Indian company names and their symbols
        self.indian_companies = {
            # Major Indian companies
            'Reliance': ['RELIANCE', 'RIL'],
            'Tata Consultancy Services': ['TCS', 'TATA CONSULTANCY'],
            'HDFC Bank': ['HDFC', 'HDFCBANK'],
            'Infosys': ['INFOSYS', 'INFY'],
            'ICICI Bank': ['ICICIBANK', 'ICICI'],
            'Kotak Mahindra Bank': ['KOTAKBANK', 'KOTAK'],
            'Hindustan Unilever': ['HINDUNILVR', 'HUL'],
            'ITC': ['ITC'],
            'Bharti Airtel': ['BHARTIARTL', 'AIRTEL'],
            'State Bank of India': ['SBIN', 'SBI'],
            'Asian Paints': ['ASIANPAINT'],
            'Maruti Suzuki': ['MARUTI', 'MARUTI SUZUKI'],
            'Titan': ['TITAN'],
            'Nestle India': ['NESTLEIND', 'NESTLE'],
            'Bajaj Finance': ['BAJFINANCE', 'BAJAJ FINANCE'],
            'Axis Bank': ['AXISBANK', 'AXIS'],
            'Larsen & Toubro': ['LT', 'L&T'],
            'Sun Pharmaceutical': ['SUNPHARMA', 'SUN PHARMA'],
            'Wipro': ['WIPRO'],
            'Tech Mahindra': ['TECHM', 'TECH MAHINDRA'],
            'Power Grid Corporation': ['POWERGRID', 'POWER GRID'],
            'NTPC': ['NTPC'],
            'Coal India': ['COALINDIA', 'COAL INDIA'],
            'ONGC': ['ONGC'],
            'Indian Oil Corporation': ['IOC', 'INDIAN OIL'],
            'Bharat Petroleum': ['BPCL', 'BP'],
            'Hindustan Petroleum': ['HPCL', 'HP'],
            'GAIL': ['GAIL'],
            'Adani Ports': ['ADANIPORTS', 'ADANI PORTS'],
            'Adani Enterprises': ['ADANIENT', 'ADANI ENTERPRISES'],
            'Adani Green Energy': ['ADANIGREEN', 'ADANI GREEN'],
            'Adani Transmission': ['ADANITRANS', 'ADANI TRANSMISSION'],
            'Adani Total Gas': ['ATGL', 'ADANI TOTAL GAS'],
            'Adani Power': ['ADANIPOWER', 'ADANI POWER'],
            'JSW Steel': ['JSWSTEEL', 'JSW STEEL'],
            'Tata Steel': ['TATASTEEL', 'TATA STEEL'],
            'Hindalco': ['HINDALCO'],
            'Vedanta': ['VEDL', 'VEDANTA'],
            'Tata Motors': ['TATAMOTORS', 'TATA MOTORS'],
            'Mahindra & Mahindra': ['M&M', 'MAHINDRA'],
            'Bajaj Auto': ['BAJAJ-AUTO', 'BAJAJ AUTO'],
            'Hero MotoCorp': ['HEROMOTOCO', 'HERO MOTOCORP'],
            'Eicher Motors': ['EICHERMOT', 'EICHER'],
            'Apollo Hospitals': ['APOLLOHOSP', 'APOLLO HOSPITALS'],
            'Dr. Reddy\'s Laboratories': ['DRREDDY', 'DR. REDDY\'S'],
            'Cipla': ['CIPLA'],
            'Divis Laboratories': ['DIVISLAB', 'DIVIS'],
            'Biocon': ['BIOCON'],
            'Lupin': ['LUPIN'],
            'Aurobindo Pharma': ['AUROPHARMA', 'AUROBINDO'],
            'Cadila Healthcare': ['CADILAHC', 'CADILA'],
            'Glenmark Pharmaceuticals': ['GLENMARK', 'GLENMARK PHARMA'],
            'Torrent Pharmaceuticals': ['TORNTPHARM', 'TORRENT PHARMA'],
            'Piramal Enterprises': ['PIRAMAL', 'PIRAMAL ENTERPRISES'],
            'Dabur India': ['DABUR', 'DABUR INDIA'],
            'Godrej Consumer Products': ['GODREJCP', 'GODREJ CONSUMER'],
            'Britannia Industries': ['BRITANNIA', 'BRITANNIA INDUSTRIES'],
            'Tata Consumer Products': ['TATACONSUM', 'TATA CONSUMER'],
            'United Spirits': ['MCDOWELL-N', 'UNITED SPIRITS'],
            'ITC': ['ITC'],
            'Zee Entertainment': ['ZEEL', 'ZEE ENTERTAINMENT'],
            'Sun TV Network': ['SUNTV', 'SUN TV'],
            'Network18 Media': ['NETWORK18', 'NETWORK 18'],
            'PVR': ['PVR'],
            'Inox Leisure': ['INOXLEISUR', 'INOX LEISURE'],
            'Jubilant FoodWorks': ['JUBLFOOD', 'JUBILANT FOODWORKS'],
            'Westlife Development': ['WESTLIFE', 'WESTLIFE DEVELOPMENT'],
            'Tata Communications': ['TATACOMM', 'TATA COMMUNICATIONS'],
            'Bharti Infratel': ['INFRATEL', 'BHARTI INFRATEL'],
            'Indus Towers': ['INDUSTOWER', 'INDUS TOWERS'],
            'Gujarat Gas': ['GUJGASLTD', 'GUJARAT GAS'],
            'Petronet LNG': ['PETRONET', 'PETRONET LNG'],
            'GAIL': ['GAIL'],
            'Indraprastha Gas': ['IGL', 'INDRAPRASTHA GAS'],
            'Mahanagar Gas': ['MGL', 'MAHANAGAR GAS'],
            'Adani Gas': ['ADANIGAS', 'ADANI GAS'],
            'Torrent Power': ['TORNTPOWER', 'TORRENT POWER'],
            'Tata Power': ['TATAPOWER', 'TATA POWER'],
            'NTPC': ['NTPC'],
            'Power Grid Corporation': ['POWERGRID', 'POWER GRID'],
            'Reliance Power': ['RPOWER', 'RELIANCE POWER'],
            'Adani Power': ['ADANIPOWER', 'ADANI POWER'],
            'JSW Energy': ['JSWENERGY', 'JSW ENERGY'],
            'Tata Power': ['TATAPOWER', 'TATA POWER'],
            'NHPC': ['NHPC'],
            'SJVN': ['SJVN'],
            'Suzlon Energy': ['SUZLON', 'SUZLON ENERGY'],
            'Inox Wind': ['INOXWIND', 'INOX WIND'],
            'Orient Green Power': ['ORIENTGREEN', 'ORIENT GREEN'],
            'Webel Solar': ['WEBELSOLAR', 'WEBEL SOLAR'],
            'Adani Green Energy': ['ADANIGREEN', 'ADANI GREEN'],
            'Tata Motors': ['TATAMOTORS', 'TATA MOTORS'],
            'Mahindra & Mahindra': ['M&M', 'MAHINDRA'],
            'Bajaj Auto': ['BAJAJ-AUTO', 'BAJAJ AUTO'],
            'Hero MotoCorp': ['HEROMOTOCO', 'HERO MOTOCORP'],
            'Eicher Motors': ['EICHERMOT', 'EICHER'],
            'TVS Motor Company': ['TVSMOTORS', 'TVS MOTOR'],
            'Bajaj Holdings': ['BAJAJHIND', 'BAJAJ HOLDINGS'],
            'Exide Industries': ['EXIDEIND', 'EXIDE'],
            'Amara Raja Batteries': ['AMARAJABAT', 'AMARA RAJA'],
            'Motherson Sumi Systems': ['MOTHERSON', 'MOTHERSON SUMI'],
            'Bosch': ['BOSCHLTD', 'BOSCH'],
            'Bharat Forge': ['BHARATFORG', 'BHARAT FORGE'],
            'Ashok Leyland': ['ASHOKLEY', 'ASHOK LEYLAND'],
            'Force Motors': ['FORCEMOT', 'FORCE MOTORS'],
            'Escorts': ['ESCORTS', 'ESCORTS LTD'],
            'Swaraj Engines': ['SWARAJENG', 'SWARAJ ENGINES'],
            'Greaves Cotton': ['GREAVESCOT', 'GREAVES COTTON'],
            'Cummins India': ['CUMMINSIND', 'CUMMINS'],
            'Wabco India': ['WABCOINDIA', 'WABCO'],
            'Endurance Technologies': ['ENDURANCE', 'ENDURANCE TECH'],
            'Suprajit Engineering': ['SUPRAJIT', 'SUPRAJIT ENG'],
            'Rane Holdings': ['RANEHOLDIN', 'RANE HOLDINGS'],
            'Rane Brake Lining': ['RANEBRAKE', 'RANE BRAKE'],
            'Rane Engine Valve': ['RANEENGINE', 'RANE ENGINE'],
            'Rane Madras': ['RANEMADRAS', 'RANE MADRAS'],
            'Rane NSK Steering': ['RANENSK', 'RANE NSK'],
            'Rane TRW Steering': ['RANETRW', 'RANE TRW'],
            'Rane Brake Lining': ['RANEBRAKE', 'RANE BRAKE'],
            'Rane Engine Valve': ['RANEENGINE', 'RANE ENGINE'],
            'Rane Madras': ['RANEMADRAS', 'RANE MADRAS'],
            'Rane NSK Steering': ['RANENSK', 'RANE NSK'],
            'Rane TRW Steering': ['RANETRW', 'RANE TRW'],
        }
        
        # Create reverse mapping from symbols to company names
        self.symbol_to_company = {}
        for company, symbols in self.indian_companies.items():
            for symbol in symbols:
                self.symbol_to_company[symbol] = company

    def extract_stocks_from_text(self, text: str) -> List[Dict[str, str]]:
        """
        Extract stock symbols and company names from text.
        
        Args:
            text: The text to analyze
            
        Returns:
            List of dictionaries containing stock information
        """
        found_stocks = []
        text_upper = text.upper()
        
        # Check for known company names and symbols
        for company, symbols in self.indian_companies.items():
            for symbol in symbols:
                if symbol in text_upper:
                    found_stocks.append({
                        'company': company,
                        'symbol': symbol,
                        'confidence': 'high' if len(symbol) > 3 else 'medium'
                    })
        
        # Look for potential stock symbols using regex patterns (only for high-confidence matches)
        for pattern in self.stock_patterns:
            matches = re.findall(pattern, text_upper)
            for match in matches:
                # Skip if already found as a known symbol
                if not any(stock['symbol'] == match for stock in found_stocks):
                    # Check if it looks like a valid stock symbol
                    if self._is_valid_stock_symbol(match) and len(match) >= 3:
                        # Only include if it's likely to be a real stock symbol
                        if any(char.isdigit() for char in match) or len(match) >= 4:
                            found_stocks.append({
                                'company': 'Unknown',
                                'symbol': match,
                                'confidence': 'low'
                            })
        
        # Remove duplicates and sort by confidence
        unique_stocks = []
        seen_symbols = set()
        for stock in found_stocks:
            if stock['symbol'] not in seen_symbols:
                unique_stocks.append(stock)
                seen_symbols.add(stock['symbol'])
        
        # Sort by confidence (high, medium, low)
        confidence_order = {'high': 0, 'medium': 1, 'low': 2}
        unique_stocks.sort(key=lambda x: confidence_order[x['confidence']])
        
        return unique_stocks

    def _is_valid_stock_symbol(self, symbol: str) -> bool:
        """
        Check if a string looks like a valid stock symbol.
        
        Args:
            symbol: The symbol to validate
            
        Returns:
            True if it looks like a valid stock symbol
        """
        # Basic validation rules
        if len(symbol) < 2 or len(symbol) > 10:
            return False
        
        # Should contain at least one letter
        if not re.search(r'[A-Z]', symbol):
            return False
        
        # Should not be all numbers
        if symbol.isdigit():
            return False
        
        # Should not contain special characters except common ones
        if not re.match(r'^[A-Z0-9\-\.]+$', symbol):
            return False
        
        # Filter out common English words that might be picked up
        common_words = {
            'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD', 'HER', 'WAS', 'ONE', 'OUR',
            'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO',
            'WHO', 'BOY', 'DID', 'ITS', 'LET', 'PUT', 'SAY', 'SHE', 'TOO', 'USE', 'WAY', 'WILL', 'WITH', 'YOUR',
            'ABOUT', 'AFTER', 'AGAIN', 'BEING', 'BEFORE', 'COULD', 'EVERY', 'FIRST', 'GOING', 'GREAT', 'HAD',
            'HAS', 'HAVE', 'HERE', 'JUST', 'KNOW', 'LIKE', 'LONG', 'LOOK', 'MADE', 'MAKE', 'MANY', 'MOST',
            'MUST', 'NEVER', 'ONLY', 'OTHER', 'OVER', 'SAID', 'SAME', 'SEEM', 'SHOULD', 'SOME', 'STILL',
            'SUCH', 'TAKE', 'THAN', 'THAT', 'THEIR', 'THEM', 'THERE', 'THESE', 'THEY', 'THING', 'THINK',
            'THIS', 'THOSE', 'THROUGH', 'TIME', 'UNDER', 'VERY', 'WANT', 'WAS', 'WERE', 'WHAT', 'WHEN',
            'WHERE', 'WHICH', 'WHILE', 'WHO', 'WILL', 'WITH', 'WOULD', 'YEAR', 'YOUR', 'ABLE', 'ABOUT',
            'ABOVE', 'ACROSS', 'AFTER', 'AGAIN', 'AGAINST', 'ALMOST', 'ALONE', 'ALONG', 'ALREADY', 'ALSO',
            'ALTHOUGH', 'ALWAYS', 'AMONG', 'ANOTHER', 'ANYONE', 'ANYTHING', 'ANYWHERE', 'AROUND', 'BECAME',
            'BECAUSE', 'BECOME', 'BEFORE', 'BEHIND', 'BELOW', 'BESIDE', 'BETWEEN', 'BEYOND', 'BOTH', 'CAME',
            'CANNOT', 'CERTAIN', 'CHANGE', 'COMING', 'CONSIDER', 'COULD', 'DURING', 'EACH', 'EARLY', 'EITHER',
            'ENOUGH', 'EVERYONE', 'EVERYTHING', 'EVERYWHERE', 'FARTHER', 'FATHER', 'FEW', 'FIND', 'FOUND',
            'FURTHER', 'GIVEN', 'GOING', 'GREAT', 'HAD', 'HAS', 'HAVE', 'HERE', 'HIGH', 'HIM', 'HIS', 'HOW',
            'HOWEVER', 'INTO', 'JUST', 'KNOW', 'LARGE', 'LAST', 'LATE', 'LATER', 'LEAST', 'LEFT', 'LESS',
            'LIFE', 'LITTLE', 'LONG', 'LOOK', 'LOOKED', 'LOOKING', 'MADE', 'MAKE', 'MAKING', 'MAN', 'MANY',
            'MIGHT', 'MORE', 'MOST', 'MOVED', 'MUCH', 'MUST', 'NEAR', 'NEED', 'NEVER', 'NEW', 'NEXT', 'NIGHT',
            'NO', 'NOT', 'NOTHING', 'NOW', 'NUMBER', 'OFF', 'OLD', 'ONCE', 'ONLY', 'OPEN', 'ORDER', 'OTHER',
            'OUR', 'OUT', 'OVER', 'OWN', 'PART', 'PEOPLE', 'PLACE', 'PUT', 'RIGHT', 'ROOM', 'SAID', 'SAME',
            'SAW', 'SAY', 'SAYING', 'SEEM', 'SEEN', 'SHE', 'SHOULD', 'SIDE', 'SINCE', 'SOME', 'SOMETHING',
            'SOMETIMES', 'SOMEONE', 'SOMEWHERE', 'STILL', 'SUCH', 'SURE', 'TAKE', 'TAKEN', 'THAN', 'THAT',
            'THE', 'THEIR', 'THEM', 'THEN', 'THERE', 'THESE', 'THEY', 'THING', 'THINK', 'THINKING', 'THIS',
            'THOSE', 'THOUGH', 'THOUGHT', 'THROUGH', 'TIME', 'TO', 'TODAY', 'TOGETHER', 'TOO', 'TURNED',
            'TWO', 'UNDER', 'UNTIL', 'UP', 'UPON', 'US', 'USE', 'USED', 'USING', 'VERY', 'WANT', 'WAS',
            'WATER', 'WAY', 'WE', 'WELL', 'WENT', 'WERE', 'WHAT', 'WHEN', 'WHERE', 'WHETHER', 'WHICH',
            'WHILE', 'WHO', 'WHOM', 'WHOSE', 'WHY', 'WILL', 'WITH', 'WITHIN', 'WITHOUT', 'WOULD', 'YEAR',
            'YEARS', 'YET', 'YOU', 'YOUNG', 'YOUR', 'YOURSELF', 'YOURSELVES', 'ABOUT', 'ABOVE', 'ACROSS',
            'AFTER', 'AGAIN', 'AGAINST', 'ALMOST', 'ALONE', 'ALONG', 'ALREADY', 'ALSO', 'ALTHOUGH', 'ALWAYS',
            'AMONG', 'ANOTHER', 'ANYONE', 'ANYTHING', 'ANYWHERE', 'AROUND', 'BECAME', 'BECAUSE', 'BECOME',
            'BEFORE', 'BEHIND', 'BELOW', 'BESIDE', 'BETWEEN', 'BEYOND', 'BOTH', 'CAME', 'CANNOT', 'CERTAIN',
            'CHANGE', 'COMING', 'CONSIDER', 'COULD', 'DURING', 'EACH', 'EARLY', 'EITHER', 'ENOUGH', 'EVERYONE',
            'EVERYTHING', 'EVERYWHERE', 'FARTHER', 'FATHER', 'FEW', 'FIND', 'FOUND', 'FURTHER', 'GIVEN',
            'GOING', 'GREAT', 'HAD', 'HAS', 'HAVE', 'HERE', 'HIGH', 'HIM', 'HIS', 'HOW', 'HOWEVER', 'INTO',
            'JUST', 'KNOW', 'LARGE', 'LAST', 'LATE', 'LATER', 'LEAST', 'LEFT', 'LESS', 'LIFE', 'LITTLE',
            'LONG', 'LOOK', 'LOOKED', 'LOOKING', 'MADE', 'MAKE', 'MAKING', 'MAN', 'MANY', 'MIGHT', 'MORE',
            'MOST', 'MOVED', 'MUCH', 'MUST', 'NEAR', 'NEED', 'NEVER', 'NEW', 'NEXT', 'NIGHT', 'NO', 'NOT',
            'NOTHING', 'NOW', 'NUMBER', 'OFF', 'OLD', 'ONCE', 'ONLY', 'OPEN', 'ORDER', 'OTHER', 'OUR', 'OUT',
            'OVER', 'OWN', 'PART', 'PEOPLE', 'PLACE', 'PUT', 'RIGHT', 'ROOM', 'SAID', 'SAME', 'SAW', 'SAY',
            'SAYING', 'SEEM', 'SEEN', 'SHE', 'SHOULD', 'SIDE', 'SINCE', 'SOME', 'SOMETHING', 'SOMETIMES',
            'SOMEONE', 'SOMEWHERE', 'STILL', 'SUCH', 'SURE', 'TAKE', 'TAKEN', 'THAN', 'THAT', 'THE', 'THEIR',
            'THEM', 'THEN', 'THERE', 'THESE', 'THEY', 'THING', 'THINK', 'THINKING', 'THIS', 'THOSE', 'THOUGH',
            'THOUGHT', 'THROUGH', 'TIME', 'TO', 'TODAY', 'TOGETHER', 'TOO', 'TURNED', 'TWO', 'UNDER', 'UNTIL',
            'UP', 'UPON', 'US', 'USE', 'USED', 'USING', 'VERY', 'WANT', 'WAS', 'WATER', 'WAY', 'WE', 'WELL',
            'WENT', 'WERE', 'WHAT', 'WHEN', 'WHERE', 'WHETHER', 'WHICH', 'WHILE', 'WHO', 'WHOM', 'WHOSE',
            'WHY', 'WILL', 'WITH', 'WITHIN', 'WITHOUT', 'WOULD', 'YEAR', 'YEARS', 'YET', 'YOU', 'YOUNG',
            'YOUR', 'YOURSELF', 'YOURSELVES', 'NOTE', 'DRAG', 'FIVE', 'BELOW', 'DOVISH', 'PARTLY', 'OFFSET',
            'POWER', 'MOTORS', 'BID', 'STABLE', 'TATA', 'BHUTAN', 'REDUCE', 'ENERGY', 'AJAY', 'GOALS',
            'FAVORI', 'SHIFTS', 'CLEAN', 'RACED', 'LONDON', 'KEEP', 'UNITED', 'RIDE', 'HEDGE', 'FUNDS',
            'VERSUS', 'CAGR', 'GREW', 'MUST', 'RETAIN', 'PUBLIC', 'NEWLY', 'ANGEL', 'SLIDE', 'MAKERS',
            'CLIMB', 'METAL', 'TANKS', 'OPENED', 'MUCH', 'HARD', 'BEYOND', 'SEEN', 'STICKY', 'BOOSTS',
            'WEAKER', 'LTD', 'BOUNCE', 'GAUGE', 'SLUMP', 'REGION', 'STOXX', 'WRAP', 'HELD', 'CVC', 'HCG',
            'BOUGHT', 'LAKH', 'NIPPON', 'MUTUAL', 'MORGAN', 'UNFAIR', 'SURVEY', 'VOTING', 'MUDREX', 'CRYPTO',
            'TAXES', 'WANT'
        }
        
        if symbol in common_words:
            return False
        
        return True

    def extract_stocks_from_news_articles(self, articles: List[str]) -> Dict[str, List[Dict[str, str]]]:
        """
        Extract stocks from a list of news articles.
        
        Args:
            articles: List of news article texts
            
        Returns:
            Dictionary mapping article index to list of found stocks
        """
        results = {}
        
        for i, article in enumerate(articles):
            stocks = self.extract_stocks_from_text(article)
            if stocks:
                results[i] = stocks
        
        return results

    def get_stock_frequency(self, articles: List[str]) -> Dict[str, int]:
        """
        Get frequency of each stock mentioned across all articles.
        
        Args:
            articles: List of news article texts
            
        Returns:
            Dictionary mapping stock symbols to their frequency
        """
        stock_frequency = {}
        
        for article in articles:
            stocks = self.extract_stocks_from_text(article)
            for stock in stocks:
                symbol = stock['symbol']
                stock_frequency[symbol] = stock_frequency.get(symbol, 0) + 1
        
        return dict(sorted(stock_frequency.items(), key=lambda x: x[1], reverse=True))

    def get_top_stocks(self, articles: List[str], top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Get the top N most mentioned stocks.
        
        Args:
            articles: List of news article texts
            top_n: Number of top stocks to return
            
        Returns:
            List of tuples (symbol, frequency) sorted by frequency
        """
        frequency = self.get_stock_frequency(articles)
        return list(frequency.items())[:top_n]


if __name__ == "__main__":
    # Test the stock extractor
    extractor = StockExtractor()
    
    # Sample news headlines
    sample_news = [
        "Reliance Industries reports strong Q3 results with 15% growth",
        "TCS announces new digital transformation initiatives",
        "HDFC Bank stock surges 5% on positive earnings",
        "Infosys partners with global tech giants for cloud solutions",
        "ICICI Bank reports record quarterly profits",
        "Tata Motors launches new electric vehicle lineup",
        "Bharti Airtel expands 5G network across major cities",
        "ITC diversifies into FMCG sector with new product launches",
        "Kotak Mahindra Bank announces dividend distribution",
        "Asian Paints reports robust demand in decorative segment"
    ]
    
    print("🔍 Stock Symbol Extractor Test")
    print("=" * 40)
    
    # Extract stocks from each article
    for i, article in enumerate(sample_news, 1):
        stocks = extractor.extract_stocks_from_text(article)
        print(f"\n📰 Article {i}: {article}")
        if stocks:
            print("📈 Found stocks:")
            for stock in stocks:
                print(f"   - {stock['symbol']} ({stock['company']}) - {stock['confidence']} confidence")
        else:
            print("   No stocks detected")
    
    # Get top stocks across all articles
    print(f"\n📊 Top 5 Most Mentioned Stocks:")
    print("-" * 30)
    top_stocks = extractor.get_top_stocks(sample_news, 5)
    for symbol, frequency in top_stocks:
        company = extractor.symbol_to_company.get(symbol, "Unknown")
        print(f"   {symbol} ({company}): {frequency} mentions")
