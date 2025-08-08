import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import pandas as pd

def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('geopolitical_analyzer.log'),
            logging.StreamHandler()
        ]
    )

def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables"""
    config = {
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'news_api_key': os.getenv('NEWS_API_KEY'),
        'debug': os.getenv('DEBUG', 'False').lower() == 'true',
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'news_update_interval': int(os.getenv('NEWS_UPDATE_INTERVAL', '300')),
        'market_update_interval': int(os.getenv('MARKET_UPDATE_INTERVAL', '60')),
        'max_news_articles': int(os.getenv('MAX_NEWS_ARTICLES', '50')),
        'max_market_symbols': int(os.getenv('MAX_MARKET_SYMBOLS', '20')),
        'sentiment_model': os.getenv('SENTIMENT_ANALYSIS_MODEL', 'textblob'),
        'risk_threshold': float(os.getenv('RISK_ASSESSMENT_THRESHOLD', '0.7')),
        'confidence_threshold': float(os.getenv('CONFIDENCE_THRESHOLD', '0.8'))
    }
    return config

def save_data_to_cache(data: Dict[str, Any], filename: str) -> None:
    """Save data to cache file"""
    try:
        cache_dir = "data/cache"
        os.makedirs(cache_dir, exist_ok=True)
        
        filepath = os.path.join(cache_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, default=str)
    except Exception as e:
        logging.error(f"Error saving data to cache: {e}")

def load_data_from_cache(filename: str) -> Optional[Dict[str, Any]]:
    """Load data from cache file"""
    try:
        cache_dir = "data/cache"
        filepath = os.path.join(cache_dir, filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Error loading data from cache: {e}")
    
    return None

def is_cache_valid(filename: str, max_age_minutes: int = 30) -> bool:
    """Check if cache file is still valid"""
    try:
        cache_dir = "data/cache"
        filepath = os.path.join(cache_dir, filename)
        
        if os.path.exists(filepath):
            file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(filepath))
            return file_age.total_seconds() < (max_age_minutes * 60)
    except Exception as e:
        logging.error(f"Error checking cache validity: {e}")
    
    return False

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format currency amount"""
    if currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "EUR":
        return f"€{amount:,.2f}"
    elif currency == "GBP":
        return f"£{amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"

def format_percentage(value: float) -> str:
    """Format percentage value"""
    return f"{value:.2%}"

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 0.0
    return ((new_value - old_value) / old_value) * 100

def get_risk_color(risk_score: float) -> str:
    """Get color for risk score"""
    if risk_score > 0.7:
        return "#d62728"  # Red
    elif risk_score > 0.4:
        return "#ff7f0e"  # Orange
    else:
        return "#2ca02c"  # Green

def get_sentiment_emoji(sentiment: float) -> str:
    """Get emoji for sentiment score"""
    if sentiment > 0.2:
        return "🟢"
    elif sentiment < -0.2:
        return "🔴"
    else:
        return "🟡"

def validate_api_keys() -> Dict[str, bool]:
    """Validate required API keys"""
    validation = {
        'openai': bool(os.getenv('OPENAI_API_KEY')),
        'news': bool(os.getenv('NEWS_API_KEY'))
    }
    return validation

def get_supported_regions() -> List[str]:
    """Get list of supported regions"""
    return [
        "North America",
        "Europe", 
        "Asia-Pacific",
        "Middle East",
        "Africa",
        "Latin America"
    ]

def get_supported_sectors() -> List[str]:
    """Get list of supported market sectors"""
    return [
        "Technology",
        "Energy",
        "Finance", 
        "Healthcare",
        "Manufacturing",
        "Consumer Goods"
    ]

def create_sample_portfolio() -> List[Dict[str, Any]]:
    """Create a sample portfolio for demonstration"""
    return [
        {
            'symbol': 'AAPL',
            'sector': 'Technology',
            'region': 'North America',
            'allocation': 0.25,
            'price': 150.0,
            'change': 0.02
        },
        {
            'symbol': 'XOM',
            'sector': 'Energy',
            'region': 'North America',
            'allocation': 0.20,
            'price': 80.0,
            'change': 0.05
        },
        {
            'symbol': 'JPM',
            'sector': 'Finance',
            'region': 'North America',
            'allocation': 0.15,
            'price': 140.0,
            'change': -0.02
        },
        {
            'symbol': 'ASML',
            'sector': 'Technology',
            'region': 'Europe',
            'allocation': 0.10,
            'price': 600.0,
            'change': 0.03
        },
        {
            'symbol': 'TSM',
            'sector': 'Technology',
            'region': 'Asia-Pacific',
            'allocation': 0.10,
            'price': 100.0,
            'change': 0.01
        }
    ]

def generate_report_summary(news_data: List[Dict[str, Any]], 
                          market_data: List[Dict[str, Any]], 
                          risk_data: List[Dict[str, Any]]) -> str:
    """Generate a summary report"""
    summary = "=== GEOPOLITICAL MARKET ANALYSIS SUMMARY ===\n\n"
    
    # News summary
    if news_data:
        summary += f"📰 News Analysis:\n"
        summary += f"• Total articles analyzed: {len(news_data)}\n"
        
        # Calculate sentiment
        sentiments = [news.get('sentiment', 0) for news in news_data]
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        summary += f"• Average sentiment: {avg_sentiment:.2f} {get_sentiment_emoji(avg_sentiment)}\n"
        
        # Regional breakdown
        regions = {}
        for news in news_data:
            region = news.get('region', 'Unknown')
            regions[region] = regions.get(region, 0) + 1
        
        summary += f"• Regional coverage: {', '.join([f'{r} ({c})' for r, c in regions.items()])}\n\n"
    
    # Market summary
    if market_data:
        summary += f"📈 Market Analysis:\n"
        summary += f"• Total market symbols: {len(market_data)}\n"
        
        # Sector performance
        sectors = {}
        for data in market_data:
            sector = data.get('sector', 'Unknown')
            if sector not in sectors:
                sectors[sector] = []
            sectors[sector].append(data.get('change', 0))
        
        summary += f"• Sector performance:\n"
        for sector, changes in sectors.items():
            avg_change = sum(changes) / len(changes)
            summary += f"  - {sector}: {format_percentage(avg_change)}\n"
        summary += "\n"
    
    # Risk summary
    if risk_data:
        summary += f"⚠️ Risk Assessment:\n"
        high_risk = [r for r in risk_data if r.get('Risk Level') == 'High']
        medium_risk = [r for r in risk_data if r.get('Risk Level') == 'Medium']
        low_risk = [r for r in risk_data if r.get('Risk Level') == 'Low']
        
        summary += f"• High risk regions: {len(high_risk)}\n"
        summary += f"• Medium risk regions: {len(medium_risk)}\n"
        summary += f"• Low risk regions: {len(low_risk)}\n"
        
        if high_risk:
            summary += f"• High risk areas: {', '.join([r.get('Region', '') for r in high_risk])}\n"
    
    summary += f"\n📅 Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    return summary
