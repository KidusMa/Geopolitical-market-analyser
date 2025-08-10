# Geopolitical Market Analyzer AI Agent

A sophisticated AI-powered system that analyzes geopolitical events and their impact on financial markets in real-time.

## Features

- **Real-time News Analysis**: Scrapes and analyzes geopolitical news from multiple sources
- **Market Impact Assessment**: Evaluates how geopolitical events affect different market sectors
- **Sentiment Analysis**: Uses NLP to analyze sentiment in news and social media
- **Market Data Integration**: Fetches real-time market data using Yahoo Finance
- **Modern React UI**: Beautiful, responsive web interface built with React and Tailwind CSS
- **Interactive Dashboard**: Real-time overview with charts and metrics
- **AI-Powered Insights**: Uses OpenAI's GPT models for intelligent analysis
- **Risk Assessment**: Provides geopolitical risk scores for different regions and sectors
- **Historical Analysis**: Time-series analysis with export capabilities
- **Settings Management**: Configurable API keys and preferences

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

### Option 1: React Frontend (Recommended)

1. Start the Flask API backend:
   ```bash
   python api.py
   ```

2. In a new terminal, navigate to the frontend directory and start the React app:
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

### Option 2: Streamlit Interface (Legacy)

Run the original Streamlit application:
```bash
streamlit run app.py
```

## Project Structure

- `api.py`: Flask API backend for React frontend
- `app.py`: Legacy Streamlit application
- `frontend/`: React frontend application
  - `src/pages/`: Page components (Dashboard, Analysis, etc.)
  - `src/components/`: Reusable UI components
  - `src/services/`: API client and services
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
