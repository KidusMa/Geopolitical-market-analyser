import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  BarChart3, 
  RefreshCw,
  DollarSign,
  Activity
} from 'lucide-react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, BarChart, Bar } from 'recharts';
import { analysisAPI, marketAPI } from '../services/api';
import toast from 'react-hot-toast';

const MarketImpact = () => {
  const [impactData, setImpactData] = useState([]);
  const [marketTrends, setMarketTrends] = useState([]);
  const [selectedSectors, setSelectedSectors] = useState(['Technology', 'Energy', 'Finance']);
  const [loading, setLoading] = useState(false);

  const sectors = ['Technology', 'Energy', 'Finance', 'Healthcare', 'Manufacturing', 'Consumer Goods'];

  useEffect(() => {
    fetchImpactData();
  }, [selectedSectors]);

  const fetchImpactData = async () => {
    try {
      setLoading(true);
      const [impactRes, trendsRes] = await Promise.all([
        analysisAPI.getMarketImpact(selectedSectors),
        marketAPI.getMarketIndicators()
      ]);
      
      setImpactData(impactRes.data || []);
      setMarketTrends(trendsRes.data || []);
    } catch (error) {
      console.error('Error fetching impact data:', error);
      toast.error('Failed to fetch market impact data');
      
      // Mock data for demonstration
      setImpactData([
        { sector: 'Technology', impact: 0.8, volatility: 0.3, sentiment: 0.7, volume: 1250000 },
        { sector: 'Energy', impact: 0.6, volatility: 0.4, sentiment: 0.3, volume: 890000 },
        { sector: 'Finance', impact: 0.9, volatility: 0.2, sentiment: 0.6, volume: 2100000 },
        { sector: 'Healthcare', impact: 0.4, volatility: 0.1, sentiment: 0.8, volume: 650000 },
        { sector: 'Manufacturing', impact: 0.7, volatility: 0.3, sentiment: 0.5, volume: 980000 },
        { sector: 'Consumer Goods', impact: 0.5, volatility: 0.2, sentiment: 0.6, volume: 750000 }
      ]);

      setMarketTrends([
        { date: '2024-01-01', technology: 100, energy: 100, finance: 100 },
        { date: '2024-01-02', technology: 102, energy: 98, finance: 101 },
        { date: '2024-01-03', technology: 105, energy: 95, finance: 103 },
        { date: '2024-01-04', technology: 103, energy: 97, finance: 102 },
        { date: '2024-01-05', technology: 107, energy: 94, finance: 105 },
        { date: '2024-01-06', technology: 110, energy: 92, finance: 108 },
        { date: '2024-01-07', technology: 108, energy: 96, finance: 106 }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const getImpactColor = (impact) => {
    if (impact > 0.7) return 'text-danger-600';
    if (impact > 0.4) return 'text-warning-600';
    return 'text-success-600';
  };

  const getImpactLevel = (impact) => {
    if (impact > 0.7) return 'High';
    if (impact > 0.4) return 'Medium';
    return 'Low';
  };

  const getSentimentColor = (sentiment) => {
    if (sentiment > 0.6) return 'text-success-600';
    if (sentiment < 0.4) return 'text-danger-600';
    return 'text-warning-600';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Market Impact Analysis</h1>
          <p className="text-gray-600">Geopolitical impact on market sectors</p>
        </div>
        <button
          onClick={fetchImpactData}
          disabled={loading}
          className="btn-primary flex items-center gap-2"
        >
          <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* Sector Selection */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Select Sectors</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
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

      {/* Impact Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Impact vs Volatility Scatter */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Impact vs Volatility</h3>
          <ResponsiveContainer width="100%" height={300}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                type="number" 
                dataKey="impact" 
                name="Impact Score"
                domain={[0, 1]}
              />
              <YAxis 
                type="number" 
                dataKey="volatility" 
                name="Volatility"
                domain={[0, 0.5]}
              />
              <Tooltip 
                formatter={(value, name) => [
                  name === 'impact' ? `${(value * 100).toFixed(1)}%` : `${(value * 100).toFixed(1)}%`,
                  name === 'impact' ? 'Impact Score' : 'Volatility'
                ]}
                labelFormatter={(label) => `Impact: ${(label * 100).toFixed(1)}%`}
              />
              <Scatter dataKey="volatility" fill="#3b82f6" />
            </ScatterChart>
          </ResponsiveContainer>
        </div>

        {/* Market Trends */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Sector Performance Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={marketTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="technology" stroke="#3b82f6" strokeWidth={2} />
              <Line type="monotone" dataKey="energy" stroke="#ef4444" strokeWidth={2} />
              <Line type="monotone" dataKey="finance" stroke="#22c55e" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Sector Impact Details */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Sector Impact Analysis</h3>
        <div className="space-y-4">
          {impactData.map((item) => (
            <div key={item.sector} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <BarChart3 className="h-5 w-5 text-gray-500" />
                  <h4 className="font-medium text-gray-900">{item.sector}</h4>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-center">
                    <div className={`text-lg font-bold ${getImpactColor(item.impact)}`}>
                      {(item.impact * 100).toFixed(0)}%
                    </div>
                    <div className="text-xs text-gray-500">Impact</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-bold text-gray-900">
                      {(item.volatility * 100).toFixed(0)}%
                    </div>
                    <div className="text-xs text-gray-500">Volatility</div>
                  </div>
                  <div className="text-center">
                    <div className={`text-lg font-bold ${getSentimentColor(item.sentiment)}`}>
                      {(item.sentiment * 100).toFixed(0)}%
                    </div>
                    <div className="text-xs text-gray-500">Sentiment</div>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gray-50 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingUp className="h-4 w-4 text-gray-500" />
                    <span className="text-sm font-medium text-gray-700">Impact Level</span>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    getImpactLevel(item.impact) === 'High' ? 'bg-danger-100 text-danger-800' :
                    getImpactLevel(item.impact) === 'Medium' ? 'bg-warning-100 text-warning-800' :
                    'bg-success-100 text-success-800'
                  }`}>
                    {getImpactLevel(item.impact)}
                  </span>
                </div>
                
                <div className="bg-gray-50 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <Activity className="h-4 w-4 text-gray-500" />
                    <span className="text-sm font-medium text-gray-700">Trading Volume</span>
                  </div>
                  <span className="text-sm font-medium text-gray-900">
                    {(item.volume / 1000).toFixed(0)}K
                  </span>
                </div>
                
                <div className="bg-gray-50 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <DollarSign className="h-4 w-4 text-gray-500" />
                    <span className="text-sm font-medium text-gray-700">Recommendation</span>
                  </div>
                  <span className={`text-sm font-medium ${
                    item.impact > 0.7 ? 'text-danger-600' :
                    item.impact > 0.4 ? 'text-warning-600' :
                    'text-success-600'
                  }`}>
                    {item.impact > 0.7 ? 'Monitor Closely' :
                     item.impact > 0.4 ? 'Watch for Changes' :
                     'Stable'}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Investment Recommendations */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Investment Recommendations</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-3">High Impact Sectors</h4>
            <div className="space-y-2">
              {impactData
                .filter(item => item.impact > 0.7)
                .map((item) => (
                  <div key={item.sector} className="flex items-center justify-between p-3 bg-danger-50 rounded-lg">
                    <span className="font-medium text-gray-900">{item.sector}</span>
                    <span className="text-sm text-danger-600 font-medium">
                      {(item.impact * 100).toFixed(0)}% impact
                    </span>
                  </div>
                ))}
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Stable Sectors</h4>
            <div className="space-y-2">
              {impactData
                .filter(item => item.impact < 0.4)
                .map((item) => (
                  <div key={item.sector} className="flex items-center justify-between p-3 bg-success-50 rounded-lg">
                    <span className="font-medium text-gray-900">{item.sector}</span>
                    <span className="text-sm text-success-600 font-medium">
                      {(item.impact * 100).toFixed(0)}% impact
                    </span>
                  </div>
                ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketImpact;
