# Geopolitical Market Analyzer AI Agent

A sophisticated AI-powered system that analyzes geopolitical events and their impact on financial markets in real-time.

## Features

- **Real-time News Analysis**: Scrapes and analyzes geopolitical news from multiple sources
- **Market Impact Assessment**: Evaluates how geopolitical events affect different market sectors
- **Sentiment Analysis**: Uses NLP to analyze sentiment in news and social media
- **Market Data Integration**: Fetches real-time market data using Yahoo Finance
- **Interactive Dashboard**: Beautiful Streamlit-based web interface
- **AI-Powered Insights**: Uses OpenAI's GPT models for intelligent analysis
- **Risk Assessment**: Provides geopolitical risk scores for different regions and sectors

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
4. Add your API keys to `.env`:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `NEWS_API_KEY`: Your NewsAPI key (optional)

## Usage

Run the application:
```bash
streamlit run app.py
```

## Project Structure

- `app.py`: Main Streamlit application
- `src/`: Core application modules
  - `data_collector.py`: News and market data collection
  - `analyzer.py`: AI-powered analysis engine
  - `visualizer.py`: Data visualization components
  - `risk_assessor.py`: Geopolitical risk assessment
- `data/`: Data storage and caching
- `models/`: Pre-trained models and configurations

## API Keys Required

- **OpenAI API Key**: For AI-powered analysis and insights
- **NewsAPI Key** (optional): For additional news sources

## License

MIT License
