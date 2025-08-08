import requests
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
from typing import List, Dict, Any, Optional
import time
from newsapi import NewsApiClient
from bs4 import BeautifulSoup
import json

class NewsCollector:
    """Collects geopolitical news from various sources"""
    
    def __init__(self):
        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.news_api = NewsApiClient(api_key=self.news_api_key) if self.news_api_key else None
        
        # Geopolitical keywords for filtering
        self.geopolitical_keywords = [
            'geopolitical', 'political', 'diplomatic', 'sanctions', 'trade war',
            'election', 'government', 'policy', 'treaty', 'alliance', 'conflict',
            'tension', 'crisis', 'summit', 'negotiation', 'embargo', 'tariff'
        ]
        
        # News sources
        self.news_sources = [
            'reuters.com', 'bloomberg.com', 'cnn.com', 'bbc.com',
            'theguardian.com', 'nytimes.com', 'wsj.com', 'ft.com'
        ]
    
    def get_latest_news(self, regions: List[str], max_articles: int = 20) -> List[Dict[str, Any]]:
        """Fetch latest geopolitical news for specified regions"""
        news_data = []
        
        try:
            # Use NewsAPI if available
            if self.news_api:
                news_data.extend(self._fetch_from_newsapi(regions, max_articles))
            else:
                # Fallback to web scraping
                news_data.extend(self._fetch_from_web(regions, max_articles))
                
        except Exception as e:
            print(f"Error fetching news: {e}")
            # Return sample data for demonstration
            news_data = self._get_sample_news_data(regions)
        
        return news_data[:max_articles]
    
    def _fetch_from_newsapi(self, regions: List[str], max_articles: int) -> List[Dict[str, Any]]:
        """Fetch news using NewsAPI"""
        news_data = []
        
        for region in regions:
            try:
                # Search for geopolitical news in the region
                query = f"geopolitical OR political OR diplomatic AND {region}"
                articles = self.news_api.get_everything(
                    q=query,
                    language='en',
                    sort_by='publishedAt',
                    page_size=min(max_articles, 10)
                )
                
                for article in articles.get('articles', []):
                    if self._is_geopolitical_relevant(article.get('title', '') + ' ' + article.get('description', '')):
                        news_data.append({
                            'title': article.get('title', ''),
                            'content': article.get('description', ''),
                            'summary': article.get('description', '')[:200] + '...',
                            'source': article.get('source', {}).get('name', 'Unknown'),
                            'url': article.get('url', ''),
                            'published_at': article.get('publishedAt', ''),
                            'region': region
                        })
                        
            except Exception as e:
                print(f"Error fetching news for {region}: {e}")
        
        return news_data
    
    def _fetch_from_web(self, regions: List[str], max_articles: int) -> List[Dict[str, Any]]:
        """Fallback web scraping method"""
        # This would implement web scraping from major news sites
        # For now, return sample data
        return self._get_sample_news_data(regions)
    
    def _is_geopolitical_relevant(self, text: str) -> bool:
        """Check if text contains geopolitical keywords"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.geopolitical_keywords)
    
    def _get_sample_news_data(self, regions: List[str]) -> List[Dict[str, Any]]:
        """Return sample news data for demonstration"""
        sample_news = [
            {
                'title': 'US-China Trade Relations Show Signs of Improvement',
                'content': 'Recent diplomatic talks between US and Chinese officials have shown promising signs of improving trade relations, with both sides expressing commitment to resolving ongoing disputes.',
                'summary': 'Recent diplomatic talks between US and Chinese officials have shown promising signs...',
                'source': 'Reuters',
                'url': 'https://reuters.com/sample-article',
                'published_at': datetime.now().isoformat(),
                'region': 'Asia-Pacific'
            },
            {
                'title': 'European Union Announces New Energy Policy Framework',
                'content': 'The EU has unveiled a comprehensive energy policy framework aimed at reducing dependence on foreign energy sources and promoting renewable energy investments.',
                'summary': 'The EU has unveiled a comprehensive energy policy framework...',
                'source': 'Bloomberg',
                'url': 'https://bloomberg.com/sample-article',
                'published_at': datetime.now().isoformat(),
                'region': 'Europe'
            },
            {
                'title': 'Middle East Peace Talks Resume Amid Regional Tensions',
                'content': 'International mediators have facilitated the resumption of peace talks in the Middle East, though significant challenges remain given the complex regional dynamics.',
                'summary': 'International mediators have facilitated the resumption of peace talks...',
                'source': 'CNN',
                'url': 'https://cnn.com/sample-article',
                'published_at': datetime.now().isoformat(),
                'region': 'Middle East'
            }
        ]
        
        # Filter by requested regions
        return [news for news in sample_news if news['region'] in regions]

class MarketDataCollector:
    """Collects market data from various sources"""
    
    def __init__(self):
        self.sector_symbols = {
            'Technology': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
            'Energy': ['XOM', 'CVX', 'COP', 'EOG', 'SLB'],
            'Finance': ['JPM', 'BAC', 'WFC', 'GS', 'MS'],
            'Healthcare': ['JNJ', 'PFE', 'UNH', 'ABBV', 'TMO'],
            'Manufacturing': ['GE', 'CAT', 'DE', 'BA', 'MMM'],
            'Consumer Goods': ['PG', 'KO', 'WMT', 'HD', 'MCD']
        }
        
        # Market indices
        self.indices = {
            'S&P 500': '^GSPC',
            'NASDAQ': '^IXIC',
            'DOW': '^DJI',
            'VIX': '^VIX'
        }
    
    def get_market_data(self, sectors: List[str], days: int = 30) -> List[Dict[str, Any]]:
        """Fetch market data for specified sectors"""
        market_data = []
        
        try:
            # Get sector data
            for sector in sectors:
                if sector in self.sector_symbols:
                    sector_data = self._get_sector_data(sector, days)
                    market_data.extend(sector_data)
            
            # Get index data
            index_data = self._get_index_data(days)
            market_data.extend(index_data)
            
        except Exception as e:
            print(f"Error fetching market data: {e}")
            # Return sample data
            market_data = self._get_sample_market_data(sectors)
        
        return market_data
    
    def _get_sector_data(self, sector: str, days: int) -> List[Dict[str, Any]]:
        """Get market data for a specific sector"""
        sector_data = []
        symbols = self.sector_symbols.get(sector, [])
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=f"{days}d")
                
                if not hist.empty:
                    # Calculate daily returns
                    hist['Returns'] = hist['Close'].pct_change()
                    
                    # Get latest data point
                    latest = hist.iloc[-1]
                    sector_data.append({
                        'symbol': symbol,
                        'sector': sector,
                        'price': latest['Close'],
                        'change': latest['Returns'],
                        'volume': latest['Volume'],
                        'timestamp': hist.index[-1].isoformat(),
                        'value': latest['Close']  # For visualization
                    })
                    
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
        
        return sector_data
    
    def _get_index_data(self, days: int) -> List[Dict[str, Any]]:
        """Get market index data"""
        index_data = []
        
        for index_name, symbol in self.indices.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=f"{days}d")
                
                if not hist.empty:
                    latest = hist.iloc[-1]
                    index_data.append({
                        'symbol': index_name,
                        'sector': 'Index',
                        'price': latest['Close'],
                        'change': hist['Close'].pct_change().iloc[-1],
                        'volume': latest['Volume'],
                        'timestamp': hist.index[-1].isoformat(),
                        'value': latest['Close']
                    })
                    
            except Exception as e:
                print(f"Error fetching index data for {index_name}: {e}")
        
        return index_data
    
    def _get_sample_market_data(self, sectors: List[str]) -> List[Dict[str, Any]]:
        """Return sample market data for demonstration"""
        sample_data = []
        
        for sector in sectors:
            if sector == 'Technology':
                sample_data.extend([
                    {'symbol': 'AAPL', 'sector': sector, 'price': 150.0, 'change': 0.02, 'volume': 1000000, 'timestamp': datetime.now().isoformat(), 'value': 150.0},
                    {'symbol': 'MSFT', 'sector': sector, 'price': 300.0, 'change': -0.01, 'volume': 800000, 'timestamp': datetime.now().isoformat(), 'value': 300.0}
                ])
            elif sector == 'Energy':
                sample_data.extend([
                    {'symbol': 'XOM', 'sector': sector, 'price': 80.0, 'change': 0.05, 'volume': 500000, 'timestamp': datetime.now().isoformat(), 'value': 80.0},
                    {'symbol': 'CVX', 'sector': sector, 'price': 120.0, 'change': 0.03, 'volume': 400000, 'timestamp': datetime.now().isoformat(), 'value': 120.0}
                ])
            elif sector == 'Finance':
                sample_data.extend([
                    {'symbol': 'JPM', 'sector': sector, 'price': 140.0, 'change': -0.02, 'volume': 600000, 'timestamp': datetime.now().isoformat(), 'value': 140.0},
                    {'symbol': 'BAC', 'sector': sector, 'price': 30.0, 'change': 0.01, 'volume': 700000, 'timestamp': datetime.now().isoformat(), 'value': 30.0}
                ])
        
        return sample_data
    
    def get_real_time_quotes(self, symbols: List[str]) -> List[Dict[str, Any]]:
        """Get real-time quotes for specific symbols"""
        quotes = []
        
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                quotes.append({
                    'symbol': symbol,
                    'price': info.get('regularMarketPrice', 0),
                    'change': info.get('regularMarketChangePercent', 0),
                    'volume': info.get('volume', 0),
                    'market_cap': info.get('marketCap', 0)
                })
                
            except Exception as e:
                print(f"Error fetching quote for {symbol}: {e}")
        
        return quotes
