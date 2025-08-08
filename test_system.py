#!/usr/bin/env python3
"""
Test script for the Geopolitical Market Analyzer
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

from src.data_collector import NewsCollector, MarketDataCollector
from src.analyzer import GeopoliticalAnalyzer
from src.visualizer import DataVisualizer
from src.risk_assessor import RiskAssessor
from utils import setup_logging, load_config, validate_api_keys

def test_data_collection():
    """Test data collection components"""
    print("🔍 Testing Data Collection...")
    
    # Test news collector
    news_collector = NewsCollector()
    regions = ["North America", "Europe", "Asia-Pacific"]
    news_data = news_collector.get_latest_news(regions, max_articles=5)
    
    print(f"✅ News collection: {len(news_data)} articles retrieved")
    
    # Test market data collector
    market_collector = MarketDataCollector()
    sectors = ["Technology", "Energy", "Finance"]
    market_data = market_collector.get_market_data(sectors)
    
    print(f"✅ Market data collection: {len(market_data)} data points retrieved")
    
    return news_data, market_data

def test_analysis():
    """Test analysis components"""
    print("\n🔍 Testing Analysis Components...")
    
    # Test analyzer
    analyzer = GeopoliticalAnalyzer()
    
    # Test sentiment analysis
    test_text = "Positive geopolitical developments show promising signs for market stability."
    sentiment = analyzer.analyze_sentiment(test_text)
    print(f"✅ Sentiment analysis: {sentiment:.2f}")
    
    # Test news sentiment analysis
    news_data, market_data = test_data_collection()
    sentiment_analysis = analyzer.analyze_news_sentiment(news_data)
    print(f"✅ News sentiment analysis: {sentiment_analysis}")
    
    return news_data, market_data

def test_risk_assessment():
    """Test risk assessment"""
    print("\n🔍 Testing Risk Assessment...")
    
    risk_assessor = RiskAssessor()
    regions = ["North America", "Europe", "Asia-Pacific", "Middle East"]
    
    for region in regions:
        risk_score = risk_assessor.assess_region_risk(region)
        risk_level = "High" if risk_score > 0.7 else "Medium" if risk_score > 0.4 else "Low"
        print(f"✅ {region}: Risk Score {risk_score:.2f} ({risk_level})")
    
    # Test sector risk assessment
    sector_risk = risk_assessor.assess_sector_risk("Technology", "North America")
    print(f"✅ Technology sector risk: {sector_risk}")

def test_visualization():
    """Test visualization components"""
    print("\n🔍 Testing Visualization...")
    
    visualizer = DataVisualizer()
    
    # Test with sample data
    news_data, market_data = test_data_collection()
    
    # Test sentiment chart
    sentiment_data = {
        'positive_count': 3,
        'negative_count': 1,
        'neutral_count': 1
    }
    sentiment_chart = visualizer.create_sentiment_chart(sentiment_data)
    print("✅ Sentiment chart created")
    
    # Test market performance chart
    market_chart = visualizer.create_market_performance_chart(market_data)
    print("✅ Market performance chart created")
    
    # Test risk assessment chart
    risk_data = [
        {'Region': 'North America', 'Risk Score': 0.3, 'Risk Level': 'Low'},
        {'Region': 'Europe', 'Risk Score': 0.5, 'Risk Level': 'Medium'},
        {'Region': 'Middle East', 'Risk Score': 0.8, 'Risk Level': 'High'}
    ]
    risk_chart = visualizer.create_risk_assessment_chart(risk_data)
    print("✅ Risk assessment chart created")

def test_configuration():
    """Test configuration and API keys"""
    print("\n🔍 Testing Configuration...")
    
    # Load configuration
    config = load_config()
    print(f"✅ Configuration loaded: {len(config)} settings")
    
    # Validate API keys
    api_validation = validate_api_keys()
    print(f"✅ API key validation: {api_validation}")
    
    # Setup logging
    setup_logging("INFO")
    print("✅ Logging configured")

def main():
    """Run all tests"""
    print("🚀 Starting Geopolitical Market Analyzer Tests\n")
    
    try:
        # Load environment variables
        load_dotenv()
        
        # Test configuration
        test_configuration()
        
        # Test data collection
        test_data_collection()
        
        # Test analysis
        test_analysis()
        
        # Test risk assessment
        test_risk_assessment()
        
        # Test visualization
        test_visualization()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📋 System Status:")
        print("✅ Data collection: Working")
        print("✅ Analysis engine: Working")
        print("✅ Risk assessment: Working")
        print("✅ Visualization: Working")
        print("✅ Configuration: Working")
        
        print("\n🚀 Ready to run: streamlit run app.py")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
