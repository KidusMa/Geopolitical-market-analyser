# Geopolitical Market Analyzer - React Frontend

A modern React-based user interface for the Geopolitical Market Analyzer, providing real-time analysis of geopolitical events and their impact on financial markets.

## Features

- **Modern UI**: Built with React 18, Tailwind CSS, and Lucide React icons
- **Real-time Dashboard**: Live overview of geopolitical risks and market indicators
- **Interactive Charts**: Beautiful data visualizations using Recharts
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Analysis**: Live news feed with sentiment analysis
- **Risk Assessment**: Regional geopolitical risk analysis with detailed breakdowns
- **Market Impact**: Sector-specific impact analysis and recommendations
- **Historical Analysis**: Time-series analysis with export capabilities
- **Settings Management**: Configurable API keys, notifications, and preferences

## Tech Stack

- **React 18**: Modern React with hooks and functional components
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Composable charting library
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client for API communication
- **React Hot Toast**: Toast notifications
- **Date-fns**: Date utility library

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Python backend running (see main README)

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

### Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build` folder.

## Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # Reusable UI components
│   │   └── Layout.js      # Main layout with sidebar
│   ├── pages/             # Page components
│   │   ├── Dashboard.js   # Main dashboard
│   │   ├── RealTimeAnalysis.js
│   │   ├── HistoricalAnalysis.js
│   │   ├── RiskAssessment.js
│   │   ├── MarketImpact.js
│   │   └── Settings.js
│   ├── services/          # API services
│   │   └── api.js        # API client and endpoints
│   ├── App.js            # Main app component
│   ├── index.js          # App entry point
│   └── index.css         # Global styles
├── package.json
├── tailwind.config.js    # Tailwind configuration
└── postcss.config.js     # PostCSS configuration
```

## API Integration

The frontend communicates with the Python backend via REST API endpoints:

- **Dashboard**: `/api/dashboard/*` - Overview metrics and activity
- **News**: `/api/news/*` - Latest and historical news data
- **Market**: `/api/market/*` - Market data and indicators
- **Analysis**: `/api/analysis/*` - AI-powered analysis and risk assessment

## Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:5000/api
```

### API Keys

Configure your API keys in the Settings page:
- OpenAI API Key (required for AI analysis)
- NewsAPI Key (optional, for enhanced news coverage)
- Yahoo Finance API Key (optional, for market data)

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

## Styling

The app uses Tailwind CSS with a custom design system:

- **Primary Colors**: Blue shades for main actions and branding
- **Success Colors**: Green for positive indicators
- **Warning Colors**: Orange for medium-risk items
- **Danger Colors**: Red for high-risk alerts
- **Neutral Colors**: Gray shades for text and backgrounds

## Components

### Layout
- Responsive sidebar navigation
- Mobile-friendly hamburger menu
- Top bar with notifications and user menu

### Charts
- Line charts for time-series data
- Bar charts for comparisons
- Scatter plots for correlations
- Area charts for stacked data
- Pie charts for distributions

### Cards
- Metric cards for key indicators
- Content cards for detailed information
- Interactive cards with hover effects

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Follow the existing code style and patterns
2. Use functional components with hooks
3. Implement proper error handling
4. Add loading states for async operations
5. Test on multiple screen sizes

## License

MIT License - see main project README for details
