import React, { useState, useEffect } from 'react';
import { 
  Globe, 
  TrendingUp, 
  RefreshCw, 
  Filter,
  ExternalLink,
  Clock,
  AlertTriangle,
  CheckCircle
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { newsAPI, marketAPI, analysisAPI } from '../services/api';
import toast from 'react-hot-toast';

const RealTimeAnalysis = () => {
  const [news, setNews] = useState([]);
  const [marketData, setMarketData] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedRegions, setSelectedRegions] = useState(['North America', 'Europe', 'Asia-Pacific']);
  const [selectedSectors, setSelectedSectors] = useState(['Technology', 'Energy', 'Finance']);

  const regions = ['North America', 'Europe', 'Asia-Pacific', 'Middle East', 'Africa', 'Latin America'];
  const sectors = ['Technology', 'Energy', 'Finance', 'Healthcare', 'Manufacturing', 'Consumer Goods'];

  useEffect(() => {
    fetchData();
  }, [selectedRegions, selectedSectors]);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      const [newsRes, marketRes] = await Promise.all([
        newsAPI.getLatestNews(selectedRegions),
        marketAPI.getMarketData(selectedSectors.map(s => s.toUpperCase()))
      ]);

      setNews(newsRes.data || []);
      setMarketData(marketRes.data || []);
    } catch (error) {
      console.error('Error fetching data:', error);
      toast.error('Failed to fetch real-time data');
      
      // Mock data for demonstration
      setNews([
        {
          id: 1,
          title: 'New trade agreement between US and EU announced',
          source: 'Reuters',
          published_at: '2024-01-15T10:30:00Z',
          summary: 'Major breakthrough in transatlantic trade relations...',
          content: 'The United States and European Union have announced a new comprehensive trade agreement...',
          sentiment: 0.8,
          region: 'North America'
        },
        {
          id: 2,
          title: 'Tensions rise in South China Sea',
          source: 'BBC News',
          published_at: '2024-01-15T09:15:00Z',
          summary: 'Regional tensions escalate as multiple nations assert territorial claims...',
          content: 'Recent developments in the South China Sea have raised concerns...',
          sentiment: -0.6,
          region: 'Asia-Pacific'
        },
        {
          id: 3,
          title: 'Energy prices stabilize in European markets',
          source: 'Financial Times',
          published_at: '2024-01-15T08:45:00Z',
          summary: 'Positive developments in energy supply chains...',
          content: 'European energy markets show signs of stabilization...',
          sentiment: 0.4,
          region: 'Europe'
        }
      ]);

      setMarketData([
        { symbol: 'AAPL', value: 150.25, change: 2.5, timestamp: '2024-01-15T10:00:00Z' },
        { symbol: 'GOOGL', value: 2750.80, change: -1.2, timestamp: '2024-01-15T10:00:00Z' },
        { symbol: 'MSFT', value: 380.45, change: 1.8, timestamp: '2024-01-15T10:00:00Z' },
        { symbol: 'XOM', value: 95.30, change: 0.5, timestamp: '2024-01-15T10:00:00Z' },
        { symbol: 'JPM', value: 145.75, change: -0.8, timestamp: '2024-01-15T10:00:00Z' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const generateAnalysis = async () => {
    try {
      setLoading(true);
      const response = await analysisAPI.generateAnalysis(news, marketData);
      setAnalysis(response.data);
      toast.success('AI analysis generated successfully');
    } catch (error) {
      console.error('Error generating analysis:', error);
      toast.error('Failed to generate AI analysis');
      
      // Mock analysis
      setAnalysis({
        summary: 'Current geopolitical landscape shows mixed signals with positive developments in trade relations but ongoing tensions in key regions.',
        keyInsights: [
          'US-EU trade agreement provides stability for technology and finance sectors',
          'South China Sea tensions may impact energy supply chains',
          'European energy market stabilization reduces volatility risks'
        ],
        recommendations: [
          'Monitor technology sector for trade agreement benefits',
          'Exercise caution in energy investments due to regional tensions',
          'Consider defensive positions in affected regions'
        ],
        riskLevel: 'Medium'
      });
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment) => {
    if (sentiment > 0.3) return 'text-success-600';
    if (sentiment < -0.3) return 'text-danger-600';
    return 'text-gray-600';
  };

  const getSentimentIcon = (sentiment) => {
    if (sentiment > 0.3) return <CheckCircle className="h-4 w-4 text-success-600" />;
    if (sentiment < -0.3) return <AlertTriangle className="h-4 w-4 text-danger-600" />;
    return <Clock className="h-4 w-4 text-gray-600" />;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Real-time Analysis</h1>
          <p className="text-gray-600">Live geopolitical news and market impact analysis</p>
        </div>
        <button
          onClick={fetchData}
          disabled={loading}
          className="btn-primary flex items-center gap-2"
        >
          <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex items-center gap-4 mb-4">
          <Filter className="h-5 w-5 text-gray-500" />
          <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Regions</label>
            <div className="space-y-2">
              {regions.map((region) => (
                <label key={region} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selectedRegions.includes(region)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedRegions([...selectedRegions, region]);
                      } else {
                        setSelectedRegions(selectedRegions.filter(r => r !== region));
                      }
                    }}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{region}</span>
                </label>
              ))}
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Sectors</label>
            <div className="space-y-2">
              {sectors.map((sector) => (
                <label key={sector} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selectedSectors.includes(sector)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedSectors([...selectedSectors, sector]);
                      } else {
                        setSelectedSectors(selectedSectors.filter(s => s !== sector));
                      }
                    }}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{sector}</span>
                </label>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* News Feed */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Latest News</h3>
          <div className="space-y-4">
            {news.map((item) => (
              <div key={item.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900 mb-2">{item.title}</h4>
                    <p className="text-sm text-gray-600 mb-2">{item.summary}</p>
                    <div className="flex items-center gap-4 text-xs text-gray-500">
                      <span>{item.source}</span>
                      <span>{formatDate(item.published_at)}</span>
                      <span className="capitalize">{item.region}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 ml-4">
                    {getSentimentIcon(item.sentiment)}
                    <span className={`text-sm font-medium ${getSentimentColor(item.sentiment)}`}>
                      {(item.sentiment * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Market Data */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Market Indicators</h3>
          <div className="space-y-4">
            {marketData.map((item) => (
              <div key={item.symbol} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <h4 className="font-medium text-gray-900">{item.symbol}</h4>
                  <p className="text-sm text-gray-500">{formatDate(item.timestamp)}</p>
                </div>
                <div className="text-right">
                  <p className="font-medium text-gray-900">${item.value}</p>
                  <p className={`text-sm ${item.change >= 0 ? 'text-success-600' : 'text-danger-600'}`}>
                    {item.change >= 0 ? '+' : ''}{item.change}%
                  </p>
                </div>
              </div>
            ))}
          </div>
          
          {/* Market Chart */}
          <div className="mt-6">
            <h4 className="font-medium text-gray-900 mb-3">Market Performance</h4>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={marketData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="symbol" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* AI Analysis */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">AI-Powered Analysis</h3>
          <button
            onClick={generateAnalysis}
            disabled={loading}
            className="btn-primary"
          >
            Generate Analysis
          </button>
        </div>
        
        {analysis && (
          <div className="space-y-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Summary</h4>
              <p className="text-gray-700">{analysis.summary}</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Key Insights</h4>
                <ul className="space-y-2">
                  {analysis.keyInsights?.map((insight, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-primary-600 mr-2">•</span>
                      <span className="text-gray-700">{insight}</span>
                    </li>
                  ))}
                </ul>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Recommendations</h4>
                <ul className="space-y-2">
                  {analysis.recommendations?.map((rec, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-warning-600 mr-2">•</span>
                      <span className="text-gray-700">{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-gray-700">Risk Level:</span>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                analysis.riskLevel === 'High' ? 'bg-danger-100 text-danger-800' :
                analysis.riskLevel === 'Medium' ? 'bg-warning-100 text-warning-800' :
                'bg-success-100 text-success-800'
              }`}>
                {analysis.riskLevel}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RealTimeAnalysis;
