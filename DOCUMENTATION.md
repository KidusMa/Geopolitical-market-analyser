# Geopolitical Market Analyzer - Documentation

## Overview

The Geopolitical Market Analyzer is a sophisticated AI-powered system that analyzes geopolitical events and their impact on financial markets in real-time. It combines news analysis, market data, sentiment analysis, and risk assessment to provide comprehensive insights for investors and analysts.

## Architecture

### Core Components

1. **Data Collection Layer**
   - `NewsCollector`: Fetches geopolitical news from multiple sources
   - `MarketDataCollector`: Retrieves real-time market data using Yahoo Finance

2. **Analysis Layer**
   - `GeopoliticalAnalyzer`: AI-powered analysis using OpenAI GPT models
   - `RiskAssessor`: Comprehensive risk assessment engine

3. **Visualization Layer**
   - `DataVisualizer`: Interactive charts and dashboards using Plotly

4. **User Interface**
   - Streamlit-based web application with real-time updates

## Features

### Real-time Analysis
- **News Monitoring**: Scrapes and analyzes geopolitical news from multiple sources
- **Market Integration**: Fetches real-time market data for various sectors
- **Sentiment Analysis**: Uses NLP to analyze news sentiment
- **AI Insights**: Generates intelligent analysis using OpenAI's GPT models

### Risk Assessment
- **Regional Risk Scoring**: Assesses geopolitical risk by region
- **Sector-specific Analysis**: Evaluates risk for different market sectors
- **Portfolio Risk Calculation**: Analyzes overall portfolio exposure
- **Risk Mitigation Recommendations**: Provides actionable advice

### Market Impact Analysis
- **Sector Performance**: Tracks performance across different market sectors
- **Volatility Prediction**: Predicts market volatility based on geopolitical events
- **Investment Recommendations**: Generates sector-specific investment advice

### Visualization
- **Interactive Dashboards**: Real-time charts and graphs
- **Risk Heatmaps**: Visual representation of geopolitical risks
- **Market Performance Charts**: Sector and regional performance tracking
- **Sentiment Analysis**: News sentiment distribution visualization

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- NewsAPI key (optional)

### Quick Setup
```bash
# Clone the repository
git clone <repository-url>
cd geopolitical-market-analyzer

# Run setup script
python setup.py

# Edit .env file with your API keys
# Run the application
streamlit run app.py
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp env_example.txt .env
# Edit .env with your API keys

# Run tests
python test_system.py

# Start application
streamlit run app.py
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# News API Configuration (Optional)
NEWS_API_KEY=your_news_api_key_here

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO

# Data Collection Settings
NEWS_UPDATE_INTERVAL=300  # 5 minutes
MARKET_UPDATE_INTERVAL=60  # 1 minute
MAX_NEWS_ARTICLES=50
MAX_MARKET_SYMBOLS=20

# Analysis Settings
SENTIMENT_ANALYSIS_MODEL=textblob
RISK_ASSESSMENT_THRESHOLD=0.7
CONFIDENCE_THRESHOLD=0.8
```

## Usage

### Web Interface

1. **Start the Application**
   ```bash
   streamlit run app.py
   ```

2. **Access the Dashboard**
   - Open your browser to `http://localhost:8501`
   - Configure analysis options in the sidebar
   - Select regions and sectors of interest

3. **Analysis Types**
   - **Real-time Analysis**: Current geopolitical events and market impact
   - **Historical Analysis**: Past trends and patterns
   - **Risk Assessment**: Regional and sector-specific risk evaluation
   - **Market Impact**: Sector performance and investment recommendations

### API Usage

```python
from src.data_collector import NewsCollector, MarketDataCollector
from src.analyzer import GeopoliticalAnalyzer
from src.risk_assessor import RiskAssessor

# Initialize components
news_collector = NewsCollector()
market_collector = MarketDataCollector()
analyzer = GeopoliticalAnalyzer()
risk_assessor = RiskAssessor()

# Collect data
news_data = news_collector.get_latest_news(['North America', 'Europe'])
market_data = market_collector.get_market_data(['Technology', 'Energy'])

# Analyze data
sentiment_analysis = analyzer.analyze_news_sentiment(news_data)
ai_analysis = analyzer.generate_ai_analysis(news_data, market_data)

# Assess risk
risk_score = risk_assessor.assess_region_risk('Middle East')
```

## Data Sources

### News Sources
- Reuters
- Bloomberg
- CNN
- BBC
- The Guardian
- New York Times
- Wall Street Journal
- Financial Times

### Market Data
- Yahoo Finance (real-time stock data)
- Market indices (S&P 500, NASDAQ, DOW, VIX)
- Sector-specific ETFs and stocks

### AI Analysis
- OpenAI GPT-3.5-turbo for intelligent analysis
- TextBlob for sentiment analysis
- Custom risk assessment algorithms

## Risk Assessment Model

### Risk Factors
1. **Political Stability** (25% weight)
2. **Economic Conditions** (20% weight)
3. **Diplomatic Relations** (20% weight)
4. **Regional Conflicts** (15% weight)
5. **Trade Relations** (10% weight)
6. **Regulatory Environment** (10% weight)

### Risk Levels
- **Low Risk**: Score < 0.4
- **Medium Risk**: Score 0.4 - 0.7
- **High Risk**: Score > 0.7

### Sector Sensitivities
- **Energy**: High sensitivity to political and diplomatic factors
- **Technology**: Sensitive to trade relations and regulatory changes
- **Finance**: Affected by economic conditions and regulatory environment
- **Healthcare**: Moderate sensitivity to regulatory changes
- **Manufacturing**: Sensitive to trade relations and economic conditions
- **Consumer Goods**: Affected by economic conditions and trade relations

## Customization

### Adding New Data Sources
1. Extend the `NewsCollector` class
2. Implement the required methods
3. Add configuration options

### Custom Risk Models
1. Modify the `RiskAssessor` class
2. Adjust risk factors and weights
3. Add new risk assessment algorithms

### Additional Visualizations
1. Extend the `DataVisualizer` class
2. Create new chart types
3. Integrate with additional plotting libraries

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure OpenAI API key is set in `.env` file
   - Check API key validity and quota

2. **Data Collection Failures**
   - Verify internet connection
   - Check API rate limits
   - Review error logs

3. **Memory Issues**
   - Reduce `MAX_NEWS_ARTICLES` in configuration
   - Clear cache files in `data/cache/`

4. **Performance Issues**
   - Increase update intervals
   - Reduce number of regions/sectors
   - Use caching for repeated requests

### Debug Mode
Enable debug mode in `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Testing
```bash
# Run all tests
python test_system.py

# Run specific tests
python -m pytest tests/
```

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting section

## Roadmap

### Planned Features
- [ ] Real-time alerts and notifications
- [ ] Advanced machine learning models
- [ ] Integration with additional data sources
- [ ] Mobile application
- [ ] API endpoints for external access
- [ ] Advanced portfolio optimization
- [ ] Historical backtesting capabilities
- [ ] Multi-language support

### Performance Improvements
- [ ] Caching optimization
- [ ] Database integration
- [ ] Asynchronous data collection
- [ ] Distributed processing
- [ ] Real-time streaming

## Acknowledgments

- OpenAI for providing the GPT API
- Yahoo Finance for market data
- NewsAPI for news aggregation
- Streamlit for the web framework
- Plotly for visualization components
