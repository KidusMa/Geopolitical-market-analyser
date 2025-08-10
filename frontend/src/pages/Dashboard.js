import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  AlertTriangle, 
  Globe, 
  Activity,
  RefreshCw
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { dashboardAPI } from '../services/api';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const [overview, setOverview] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [activity, setActivity] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [overviewRes, metricsRes, activityRes] = await Promise.all([
        dashboardAPI.getOverview(),
        dashboardAPI.getMetrics(),
        dashboardAPI.getRecentActivity()
      ]);
      
      setOverview(overviewRes.data);
      setMetrics(metricsRes.data);
      setActivity(activityRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Failed to load dashboard data');
      
      // Set mock data for demonstration
      setOverview({
        totalNews: 156,
        riskScore: 0.34,
        marketVolatility: 0.28,
        activeRegions: 8
      });
      
      setMetrics({
        sentimentTrend: [
          { date: '2024-01', positive: 65, negative: 20, neutral: 15 },
          { date: '2024-02', positive: 58, negative: 25, neutral: 17 },
          { date: '2024-03', positive: 72, negative: 18, neutral: 10 },
        ],
        riskByRegion: [
          { region: 'Europe', risk: 0.25 },
          { region: 'Asia-Pacific', risk: 0.45 },
          { region: 'North America', risk: 0.15 },
          { region: 'Middle East', risk: 0.75 },
          { region: 'Africa', risk: 0.35 },
        ]
      });
      
      setActivity([
        { id: 1, type: 'news', title: 'New geopolitical tension in Eastern Europe', time: '2 hours ago' },
        { id: 2, type: 'analysis', title: 'AI analysis completed for Asia-Pacific region', time: '4 hours ago' },
        { id: 3, type: 'alert', title: 'High risk alert: Middle East tensions', time: '6 hours ago' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk) => {
    if (risk < 0.3) return 'text-success-600';
    if (risk < 0.6) return 'text-warning-600';
    return 'text-danger-600';
  };

  const getRiskLevel = (risk) => {
    if (risk < 0.3) return 'Low';
    if (risk < 0.6) return 'Medium';
    return 'High';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Geopolitical market analysis overview</p>
        </div>
        <button
          onClick={fetchDashboardData}
          className="btn-primary flex items-center gap-2"
        >
          <RefreshCw className="h-4 w-4" />
          Refresh
        </button>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="metric-card">
          <div className="flex items-center">
            <div className="p-2 bg-primary-100 rounded-lg">
              <Globe className="h-6 w-6 text-primary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total News</p>
              <p className="text-2xl font-bold text-gray-900">{overview?.totalNews || 0}</p>
            </div>
          </div>
        </div>

        <div className="metric-card">
          <div className="flex items-center">
            <div className="p-2 bg-warning-100 rounded-lg">
              <AlertTriangle className="h-6 w-6 text-warning-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Global Risk Score</p>
              <p className={`text-2xl font-bold ${getRiskColor(overview?.riskScore)}`}>
                {overview?.riskScore ? (overview.riskScore * 100).toFixed(1) : 0}%
              </p>
            </div>
          </div>
        </div>

        <div className="metric-card">
          <div className="flex items-center">
            <div className="p-2 bg-success-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-success-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Market Volatility</p>
              <p className="text-2xl font-bold text-gray-900">
                {overview?.marketVolatility ? (overview.marketVolatility * 100).toFixed(1) : 0}%
              </p>
            </div>
          </div>
        </div>

        <div className="metric-card">
          <div className="flex items-center">
            <div className="p-2 bg-secondary-100 rounded-lg">
              <Activity className="h-6 w-6 text-secondary-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active Regions</p>
              <p className="text-2xl font-bold text-gray-900">{overview?.activeRegions || 0}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sentiment Trend */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Sentiment Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={metrics?.sentimentTrend || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="positive" stroke="#22c55e" strokeWidth={2} />
              <Line type="monotone" dataKey="negative" stroke="#ef4444" strokeWidth={2} />
              <Line type="monotone" dataKey="neutral" stroke="#6b7280" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Risk by Region */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk by Region</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={metrics?.riskByRegion || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="region" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="risk" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
        <div className="space-y-4">
          {activity.map((item) => (
            <div key={item.id} className="flex items-center p-4 bg-gray-50 rounded-lg">
              <div className={`p-2 rounded-lg ${
                item.type === 'news' ? 'bg-blue-100' :
                item.type === 'analysis' ? 'bg-green-100' :
                'bg-red-100'
              }`}>
                {item.type === 'news' && <Globe className="h-4 w-4 text-blue-600" />}
                {item.type === 'analysis' && <Activity className="h-4 w-4 text-green-600" />}
                {item.type === 'alert' && <AlertTriangle className="h-4 w-4 text-red-600" />}
              </div>
              <div className="ml-4 flex-1">
                <p className="text-sm font-medium text-gray-900">{item.title}</p>
                <p className="text-sm text-gray-500">{item.time}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
