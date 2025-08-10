from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv

# Import our custom modules
from src.data_collector import NewsCollector, MarketDataCollector
from src.analyzer import GeopoliticalAnalyzer
from src.visualizer import DataVisualizer
from src.risk_assessor import RiskAssessor

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize components
news_collector = NewsCollector()
market_collector = MarketDataCollector()
analyzer = GeopoliticalAnalyzer()
visualizer = DataVisualizer()
risk_assessor = RiskAssessor()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

# News API endpoints
@app.route('/api/news/latest', methods=['GET'])
def get_latest_news():
    """Get latest news for specified regions"""
    try:
        regions = request.args.getlist('regions')
        if not regions:
            regions = ['North America', 'Europe', 'Asia-Pacific']
        
        news_data = news_collector.get_latest_news(regions)
        return jsonify(news_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/news/historical', methods=['GET'])
def get_historical_news():
    """Get historical news data"""
    try:
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        regions = request.args.getlist('regions')
        
        if not start_date or not end_date:
            return jsonify({'error': 'startDate and endDate are required'}), 400
        
        # Convert dates and get historical data
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        
        # Mock historical data for demonstration
        historical_data = []
        current_date = start_dt
        while current_date <= end_dt:
            historical_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'positive': 60 + (current_date.day % 20),
                'negative': 20 + (current_date.day % 15),
                'neutral': 20 + (current_date.day % 10),
                'total': 100
            })
            current_date += timedelta(days=1)
        
        return jsonify(historical_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/news/sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment of text"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        sentiment = analyzer.analyze_sentiment(text)
        return jsonify({'sentiment': sentiment})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Market API endpoints
@app.route('/api/market/data', methods=['GET'])
def get_market_data():
    """Get current market data for specified symbols"""
    try:
        symbols = request.args.getlist('symbols')
        if not symbols:
            symbols = ['AAPL', 'GOOGL', 'MSFT', 'XOM', 'JPM']
        
        market_data = market_collector.get_market_data(symbols)
        return jsonify(market_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/market/indicators', methods=['GET'])
def get_market_indicators():
    """Get market indicators and trends"""
    try:
        # Mock market indicators data
        indicators = [
            { 'date': '2024-01-01', 'technology': 100, 'energy': 100, 'finance': 100 },
            { 'date': '2024-01-02', 'technology': 102, 'energy': 98, 'finance': 101 },
            { 'date': '2024-01-03', 'technology': 105, 'energy': 95, 'finance': 103 },
            { 'date': '2024-01-04', 'technology': 103, 'energy': 97, 'finance': 102 },
            { 'date': '2024-01-05', 'technology': 107, 'energy': 94, 'finance': 105 },
            { 'date': '2024-01-06', 'technology': 110, 'energy': 92, 'finance': 108 },
            { 'date': '2024-01-07', 'technology': 108, 'energy': 96, 'finance': 106 }
        ]
        return jsonify(indicators)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/market/historical', methods=['GET'])
def get_historical_market_data():
    """Get historical market data"""
    try:
        symbol = request.args.get('symbol', 'AAPL')
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        
        if not start_date or not end_date:
            return jsonify({'error': 'startDate and endDate are required'}), 400
        
        # Mock historical market data
        historical_data = []
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        current_date = start_dt
        base_price = 150.0
        
        while current_date <= end_dt:
            # Simulate price movement
            price_change = (current_date.day % 7 - 3) * 2.5
            historical_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'price': base_price + price_change,
                'volume': 1200000 + (current_date.day % 5) * 100000,
                'volatility': 0.02 + (current_date.day % 3) * 0.01
            })
            base_price += price_change
            current_date += timedelta(days=1)
        
        return jsonify(historical_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Analysis API endpoints
@app.route('/api/analysis/generate', methods=['POST'])
def generate_analysis():
    """Generate AI-powered analysis"""
    try:
        data = request.get_json()
        news_data = data.get('newsData', [])
        market_data = data.get('marketData', [])
        
        analysis = analyzer.generate_ai_analysis(news_data, market_data)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/risk', methods=['GET'])
def get_risk_assessment():
    """Get risk assessment for specified regions"""
    try:
        regions = request.args.getlist('regions')
        if not regions:
            regions = ['North America', 'Europe', 'Asia-Pacific']
        
        risk_data = []
        for region in regions:
            risk_score = risk_assessor.assess_region_risk(region)
            risk_data.append({
                'region': region,
                'risk': risk_score,
                'factors': risk_assessor.get_risk_factors(region),
                'trend': risk_assessor.get_risk_trend(region)
            })
        
        return jsonify(risk_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/impact', methods=['GET'])
def get_market_impact():
    """Get market impact analysis for specified sectors"""
    try:
        sectors = request.args.getlist('sectors')
        if not sectors:
            sectors = ['Technology', 'Energy', 'Finance']
        
        impact_data = []
        for sector in sectors:
            impact_data.append({
                'sector': sector,
                'impact': 0.3 + (hash(sector) % 60) / 100,  # Mock impact score
                'volatility': 0.1 + (hash(sector) % 40) / 100,  # Mock volatility
                'sentiment': 0.4 + (hash(sector) % 50) / 100,  # Mock sentiment
                'volume': 500000 + (hash(sector) % 1000000)  # Mock volume
            })
        
        return jsonify(impact_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Dashboard API endpoints
@app.route('/api/dashboard/overview', methods=['GET'])
def get_dashboard_overview():
    """Get dashboard overview data"""
    try:
        overview = {
            'totalNews': 156,
            'riskScore': 0.34,
            'marketVolatility': 0.28,
            'activeRegions': 8
        }
        return jsonify(overview)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/metrics', methods=['GET'])
def get_dashboard_metrics():
    """Get dashboard metrics"""
    try:
        metrics = {
            'sentimentTrend': [
                { 'date': '2024-01', 'positive': 65, 'negative': 20, 'neutral': 15 },
                { 'date': '2024-02', 'positive': 58, 'negative': 25, 'neutral': 17 },
                { 'date': '2024-03', 'positive': 72, 'negative': 18, 'neutral': 10 }
            ],
            'riskByRegion': [
                { 'region': 'Europe', 'risk': 0.25 },
                { 'region': 'Asia-Pacific', 'risk': 0.45 },
                { 'region': 'North America', 'risk': 0.15 },
                { 'region': 'Middle East', 'risk': 0.75 },
                { 'region': 'Africa', 'risk': 0.35 }
            ]
        }
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/activity', methods=['GET'])
def get_recent_activity():
    """Get recent activity feed"""
    try:
        activity = [
            {
                'id': 1,
                'type': 'news',
                'title': 'New geopolitical tension in Eastern Europe',
                'time': '2 hours ago'
            },
            {
                'id': 2,
                'type': 'analysis',
                'title': 'AI analysis completed for Asia-Pacific region',
                'time': '4 hours ago'
            },
            {
                'id': 3,
                'type': 'alert',
                'title': 'High risk alert: Middle East tensions',
                'time': '6 hours ago'
            }
        ]
        return jsonify(activity)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Check for required API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("Warning: OPENAI_API_KEY not found in environment variables")
        print("Some features may not work properly")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
