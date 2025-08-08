import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Import our custom modules
from src.data_collector import NewsCollector, MarketDataCollector
from src.analyzer import GeopoliticalAnalyzer
from src.visualizer import DataVisualizer
from src.risk_assessor import RiskAssessor

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Geopolitical Market Analyzer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .risk-high { color: #d62728; }
    .risk-medium { color: #ff7f0e; }
    .risk-low { color: #2ca02c; }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 Geopolitical Market Analyzer</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Configuration")
    
    # API Key Check
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        st.sidebar.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your environment.")
        st.sidebar.info("Add your OpenAI API key to the .env file or environment variables.")
        return
    
    # Analysis Options
    st.sidebar.subheader("Analysis Options")
    analysis_type = st.sidebar.selectbox(
        "Analysis Type",
        ["Real-time Analysis", "Historical Analysis", "Risk Assessment", "Market Impact"]
    )
    
    regions = st.sidebar.multiselect(
        "Regions of Interest",
        ["North America", "Europe", "Asia-Pacific", "Middle East", "Africa", "Latin America"],
        default=["North America", "Europe", "Asia-Pacific"]
    )
    
    sectors = st.sidebar.multiselect(
        "Market Sectors",
        ["Technology", "Energy", "Finance", "Healthcare", "Manufacturing", "Consumer Goods"],
        default=["Technology", "Energy", "Finance"]
    )
    
    # Main content area
    if analysis_type == "Real-time Analysis":
        show_real_time_analysis(regions, sectors)
    elif analysis_type == "Historical Analysis":
        show_historical_analysis(regions, sectors)
    elif analysis_type == "Risk Assessment":
        show_risk_assessment(regions, sectors)
    elif analysis_type == "Market Impact":
        show_market_impact(regions, sectors)

def show_real_time_analysis(regions, sectors):
    st.header("📊 Real-time Geopolitical Analysis")
    
    # Initialize collectors and analyzers
    with st.spinner("Initializing analysis components..."):
        news_collector = NewsCollector()
        market_collector = MarketDataCollector()
        analyzer = GeopoliticalAnalyzer()
        visualizer = DataVisualizer()
    
    # Collect data
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌐 Latest Geopolitical News")
        with st.spinner("Fetching latest news..."):
            news_data = news_collector.get_latest_news(regions)
            
        if news_data:
            for news in news_data[:5]:
                with st.expander(f"📰 {news['title']}"):
                    st.write(f"**Source:** {news['source']}")
                    st.write(f"**Published:** {news['published_at']}")
                    st.write(f"**Summary:** {news['summary']}")
                    
                    # Sentiment analysis
                    sentiment = analyzer.analyze_sentiment(news['content'])
                    sentiment_color = "🟢" if sentiment > 0 else "🔴" if sentiment < 0 else "🟡"
                    st.write(f"**Sentiment:** {sentiment_color} {sentiment:.2f}")
        else:
            st.warning("No recent news found for selected regions.")
    
    with col2:
        st.subheader("📈 Market Indicators")
        with st.spinner("Fetching market data..."):
            market_data = market_collector.get_market_data(sectors)
            
        if market_data:
            # Create market overview
            market_df = pd.DataFrame(market_data)
            fig = px.line(market_df, x='timestamp', y='value', color='symbol',
                         title="Market Performance")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Unable to fetch market data.")
    
    # AI Analysis
    st.subheader("🤖 AI-Powered Insights")
    if st.button("Generate AI Analysis"):
        with st.spinner("Generating AI insights..."):
            analysis = analyzer.generate_ai_analysis(news_data, market_data)
            st.write(analysis)

def show_historical_analysis(regions, sectors):
    st.header("📚 Historical Analysis")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    if st.button("Analyze Historical Data"):
        with st.spinner("Analyzing historical data..."):
            # This would integrate with historical data sources
            st.info("Historical analysis feature would connect to historical news and market databases.")
            
            # Placeholder for historical analysis
            st.subheader("Historical Trends")
            # Add historical analysis visualization here

def show_risk_assessment(regions, sectors):
    st.header("⚠️ Geopolitical Risk Assessment")
    
    risk_assessor = RiskAssessor()
    
    # Risk assessment for each region
    st.subheader("Regional Risk Scores")
    
    risk_data = []
    for region in regions:
        risk_score = risk_assessor.assess_region_risk(region)
        risk_data.append({
            'Region': region,
            'Risk Score': risk_score,
            'Risk Level': 'High' if risk_score > 0.7 else 'Medium' if risk_score > 0.4 else 'Low'
        })
    
    risk_df = pd.DataFrame(risk_data)
    
    # Create risk visualization
    fig = px.bar(risk_df, x='Region', y='Risk Score', color='Risk Level',
                 color_discrete_map={'High': '#d62728', 'Medium': '#ff7f0e', 'Low': '#2ca02c'},
                 title="Geopolitical Risk Assessment by Region")
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed risk analysis
    st.subheader("Detailed Risk Analysis")
    for region in regions:
        with st.expander(f"Risk Analysis: {region}"):
            risk_details = risk_assessor.get_detailed_risk_analysis(region)
            st.write(risk_details)

def show_market_impact(regions, sectors):
    st.header("💹 Market Impact Analysis")
    
    # Market impact analysis
    st.subheader("Sector Impact Assessment")
    
    # Placeholder for market impact analysis
    impact_data = {
        'Sector': sectors,
        'Impact Score': [0.8, 0.6, 0.9, 0.4, 0.7, 0.5][:len(sectors)],
        'Volatility': [0.3, 0.2, 0.4, 0.1, 0.3, 0.2][:len(sectors)]
    }
    
    impact_df = pd.DataFrame(impact_data)
    
    # Create impact visualization
    fig = px.scatter(impact_df, x='Impact Score', y='Volatility', 
                     size='Impact Score', color='Sector',
                     title="Market Impact vs Volatility by Sector")
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("📋 Investment Recommendations")
    st.info("Based on current geopolitical analysis, consider the following:")
    
    recommendations = [
        "🔸 Diversify investments across multiple regions",
        "🔸 Monitor energy sector for geopolitical tensions",
        "🔸 Consider defensive positions in technology sector",
        "🔸 Watch for currency volatility in emerging markets"
    ]
    
    for rec in recommendations:
        st.write(rec)

if __name__ == "__main__":
    main()
