import React, { useState, useEffect } from 'react';
import { 
  Clock, 
  Calendar, 
  TrendingUp, 
  RefreshCw,
  Download,
  Filter
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { newsAPI, marketAPI } from '../services/api';
import toast from 'react-hot-toast';

const HistoricalAnalysis = () => {
  const [historicalData, setHistoricalData] = useState([]);
  const [marketHistory, setMarketHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dateRange, setDateRange] = useState({
    startDate: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    endDate: new Date().toISOString().split('T')[0]
  });
  const [selectedRegions, setSelectedRegions] = useState(['North America', 'Europe', 'Asia-Pacific']);

  const regions = ['North America', 'Europe', 'Asia-Pacific', 'Middle East', 'Africa', 'Latin America'];

  useEffect(() => {
    fetchHistoricalData();
  }, [dateRange, selectedRegions]);

  const fetchHistoricalData = async () => {
    try {
      setLoading(true);
      const [newsRes, marketRes] = await Promise.all([
        newsAPI.getHistoricalNews(dateRange.startDate, dateRange.endDate, selectedRegions),
        marketAPI.getHistoricalData('AAPL', dateRange.startDate, dateRange.endDate)
      ]);
      
      setHistoricalData(newsRes.data || []);
      setMarketHistory(marketRes.data || []);
    } catch (error) {
      console.error('Error fetching historical data:', error);
      toast.error('Failed to fetch historical data');
      
      // Mock data for demonstration
      setHistoricalData([
        { date: '2024-01-01', positive: 65, negative: 20, neutral: 15, total: 100 },
        { date: '2024-01-02', positive: 58, negative: 25, neutral: 17, total: 100 },
        { date: '2024-01-03', positive: 72, negative: 18, neutral: 10, total: 100 },
        { date: '2024-01-04', positive: 45, negative: 35, neutral: 20, total: 100 },
        { date: '2024-01-05', positive: 80, negative: 12, neutral: 8, total: 100 },
        { date: '2024-01-06', positive: 62, negative: 22, neutral: 16, total: 100 },
        { date: '2024-01-07', positive: 55, negative: 28, neutral: 17, total: 100 }
      ]);

      setMarketHistory([
        { date: '2024-01-01', price: 150.25, volume: 1250000, volatility: 0.02 },
        { date: '2024-01-02', price: 152.80, volume: 1350000, volatility: 0.03 },
        { date: '2024-01-03', price: 155.45, volume: 1450000, volatility: 0.04 },
        { date: '2024-01-04', price: 153.20, volume: 1200000, volatility: 0.02 },
        { date: '2024-01-05', price: 158.75, volume: 1600000, volatility: 0.05 },
        { date: '2024-01-06', price: 156.30, volume: 1400000, volatility: 0.03 },
        { date: '2024-01-07', price: 159.90, volume: 1500000, volatility: 0.04 }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const exportData = () => {
    const dataStr = JSON.stringify({ historicalData, marketHistory }, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `historical-analysis-${dateRange.startDate}-${dateRange.endDate}.json`;
    link.click();
    URL.revokeObjectURL(url);
    toast.success('Data exported successfully');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Historical Analysis</h1>
          <p className="text-gray-600">Historical geopolitical and market data analysis</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={exportData}
            className="btn-secondary flex items-center gap-2"
          >
            <Download className="h-4 w-4" />
            Export
          </button>
          <button
            onClick={fetchHistoricalData}
            disabled={loading}
            className="btn-primary flex items-center gap-2"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex items-center gap-4 mb-4">
          <Filter className="h-5 w-5 text-gray-500" />
          <h3 className="text-lg font-semibold text-gray-900">Analysis Filters</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Date Range</label>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs text-gray-500 mb-1">Start Date</label>
                <input
                  type="date"
                  value={dateRange.startDate}
                  onChange={(e) => setDateRange({ ...dateRange, startDate: e.target.value })}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-500 mb-1">End Date</label>
                <input
                  type="date"
                  value={dateRange.endDate}
                  onChange={(e) => setDateRange({ ...dateRange, endDate: e.target.value })}
                  className="input-field"
                />
              </div>
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Regions</label>
            <div className="grid grid-cols-2 gap-2">
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
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sentiment Trend */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Sentiment Trend Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={historicalData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Area type="monotone" dataKey="positive" stackId="1" stroke="#22c55e" fill="#22c55e" fillOpacity={0.6} />
              <Area type="monotone" dataKey="negative" stackId="1" stroke="#ef4444" fill="#ef4444" fillOpacity={0.6} />
              <Area type="monotone" dataKey="neutral" stackId="1" stroke="#6b7280" fill="#6b7280" fillOpacity={0.6} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Market Performance */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Market Performance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={marketHistory}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="price" stroke="#3b82f6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Market Volatility */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Market Volatility Analysis</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={marketHistory}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip formatter={(value) => [`${(value * 100).toFixed(2)}%`, 'Volatility']} />
            <Line type="monotone" dataKey="volatility" stroke="#f59e0b" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Summary Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center gap-3 mb-4">
            <Clock className="h-6 w-6 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">Time Period</h3>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Start:</span>
              <span className="font-medium">{dateRange.startDate}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">End:</span>
              <span className="font-medium">{dateRange.endDate}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Duration:</span>
              <span className="font-medium">
                {Math.ceil((new Date(dateRange.endDate) - new Date(dateRange.startDate)) / (1000 * 60 * 60 * 24))} days
              </span>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center gap-3 mb-4">
            <TrendingUp className="h-6 w-6 text-success-600" />
            <h3 className="text-lg font-semibold text-gray-900">Market Summary</h3>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Avg Price:</span>
              <span className="font-medium">
                ${marketHistory.length > 0 ? 
                  (marketHistory.reduce((sum, item) => sum + item.price, 0) / marketHistory.length).toFixed(2) : 
                  '0.00'
                }
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Avg Volume:</span>
              <span className="font-medium">
                {marketHistory.length > 0 ? 
                  (marketHistory.reduce((sum, item) => sum + item.volume, 0) / marketHistory.length / 1000000).toFixed(1) + 'M' : 
                  '0M'
                }
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Avg Volatility:</span>
              <span className="font-medium">
                {marketHistory.length > 0 ? 
                  (marketHistory.reduce((sum, item) => sum + item.volatility, 0) / marketHistory.length * 100).toFixed(2) + '%' : 
                  '0%'
                }
              </span>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center gap-3 mb-4">
            <Calendar className="h-6 w-6 text-warning-600" />
            <h3 className="text-lg font-semibold text-gray-900">News Summary</h3>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Total Articles:</span>
              <span className="font-medium">
                {historicalData.length > 0 ? 
                  historicalData.reduce((sum, item) => sum + item.total, 0) : 
                  0
                }
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Positive:</span>
              <span className="font-medium text-success-600">
                {historicalData.length > 0 ? 
                  Math.round(historicalData.reduce((sum, item) => sum + item.positive, 0) / historicalData.length) + '%' : 
                  '0%'
                }
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Negative:</span>
              <span className="font-medium text-danger-600">
                {historicalData.length > 0 ? 
                  Math.round(historicalData.reduce((sum, item) => sum + item.negative, 0) / historicalData.length) + '%' : 
                  '0%'
                }
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HistoricalAnalysis;
