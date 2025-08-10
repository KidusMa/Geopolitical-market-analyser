import React, { useState, useEffect } from 'react';
import { 
  AlertTriangle, 
  Map, 
  TrendingUp, 
  RefreshCw,
  Info
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { analysisAPI } from '../services/api';
import toast from 'react-hot-toast';

const RiskAssessment = () => {
  const [riskData, setRiskData] = useState([]);
  const [selectedRegions, setSelectedRegions] = useState(['North America', 'Europe', 'Asia-Pacific']);
  const [loading, setLoading] = useState(false);
  const [detailedAnalysis, setDetailedAnalysis] = useState({});

  const regions = ['North America', 'Europe', 'Asia-Pacific', 'Middle East', 'Africa', 'Latin America'];

  useEffect(() => {
    fetchRiskData();
  }, [selectedRegions]);

  const fetchRiskData = async () => {
    try {
      setLoading(true);
      const response = await analysisAPI.getRiskAssessment(selectedRegions);
      setRiskData(response.data || []);
    } catch (error) {
      console.error('Error fetching risk data:', error);
      toast.error('Failed to fetch risk assessment data');
      
      // Mock data for demonstration
      setRiskData([
        { region: 'North America', risk: 0.15, factors: ['Trade tensions', 'Political uncertainty'], trend: 'stable' },
        { region: 'Europe', risk: 0.25, factors: ['Energy security', 'Economic challenges'], trend: 'decreasing' },
        { region: 'Asia-Pacific', risk: 0.45, factors: ['Territorial disputes', 'Supply chain issues'], trend: 'increasing' },
        { region: 'Middle East', risk: 0.75, factors: ['Regional conflicts', 'Oil price volatility'], trend: 'increasing' },
        { region: 'Africa', risk: 0.35, factors: ['Political instability', 'Economic development'], trend: 'stable' },
        { region: 'Latin America', risk: 0.30, factors: ['Economic policies', 'Social unrest'], trend: 'decreasing' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk) => {
    if (risk < 0.3) return '#22c55e';
    if (risk < 0.6) return '#f59e0b';
    return '#ef4444';
  };

  const getRiskLevel = (risk) => {
    if (risk < 0.3) return 'Low';
    if (risk < 0.6) return 'Medium';
    return 'High';
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'increasing':
        return <TrendingUp className="h-4 w-4 text-danger-600" />;
      case 'decreasing':
        return <TrendingUp className="h-4 w-4 text-success-600 transform rotate-180" />;
      default:
        return <div className="h-4 w-4 bg-gray-300 rounded-full" />;
    }
  };

  const COLORS = ['#ef4444', '#f59e0b', '#22c55e', '#3b82f6', '#8b5cf6', '#ec4899'];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Risk Assessment</h1>
          <p className="text-gray-600">Geopolitical risk analysis by region</p>
        </div>
        <button
          onClick={fetchRiskData}
          disabled={loading}
          className="btn-primary flex items-center gap-2"
        >
          <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* Region Selection */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Select Regions</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
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

      {/* Risk Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk by Region</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={riskData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="region" />
              <YAxis />
              <Tooltip 
                formatter={(value) => [`${(value * 100).toFixed(1)}%`, 'Risk Score']}
                labelFormatter={(label) => `Region: ${label}`}
              />
              <Bar dataKey="risk" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Risk Distribution */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={riskData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ region, risk }) => `${region}: ${(risk * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="risk"
              >
                {riskData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${(value * 100).toFixed(1)}%`, 'Risk Score']} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Detailed Risk Analysis */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Detailed Risk Analysis</h3>
        <div className="space-y-4">
          {riskData.map((item) => (
            <div key={item.region} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <Map className="h-5 w-5 text-gray-500" />
                  <h4 className="font-medium text-gray-900">{item.region}</h4>
                </div>
                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-2">
                    {getTrendIcon(item.trend)}
                    <span className="text-sm text-gray-500 capitalize">{item.trend}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div 
                      className="w-4 h-4 rounded-full"
                      style={{ backgroundColor: getRiskColor(item.risk) }}
                    />
                    <span className={`text-sm font-medium ${getRiskColor(item.risk) === '#22c55e' ? 'text-success-600' : getRiskColor(item.risk) === '#f59e0b' ? 'text-warning-600' : 'text-danger-600'}`}>
                      {getRiskLevel(item.risk)} ({(item.risk * 100).toFixed(0)}%)
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="mb-3">
                <h5 className="text-sm font-medium text-gray-700 mb-2">Risk Factors:</h5>
                <div className="flex flex-wrap gap-2">
                  {item.factors?.map((factor, index) => (
                    <span 
                      key={index}
                      className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
                    >
                      {factor}
                    </span>
                  ))}
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-2">
                  <Info className="h-4 w-4 text-gray-500" />
                  <span className="text-sm font-medium text-gray-700">Analysis</span>
                </div>
                <p className="text-sm text-gray-600">
                  {item.region} shows a {getRiskLevel(item.risk).toLowerCase()} risk level with a {item.trend} trend. 
                  Key concerns include {item.factors?.slice(0, 2).join(' and ')}. 
                  {item.risk > 0.5 ? ' Immediate attention recommended.' : ' Monitor for changes.'}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Risk Summary */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-success-50 rounded-lg">
            <div className="text-2xl font-bold text-success-600">
              {riskData.filter(r => r.risk < 0.3).length}
            </div>
            <div className="text-sm text-gray-600">Low Risk Regions</div>
          </div>
          <div className="text-center p-4 bg-warning-50 rounded-lg">
            <div className="text-2xl font-bold text-warning-600">
              {riskData.filter(r => r.risk >= 0.3 && r.risk < 0.6).length}
            </div>
            <div className="text-sm text-gray-600">Medium Risk Regions</div>
          </div>
          <div className="text-center p-4 bg-danger-50 rounded-lg">
            <div className="text-2xl font-bold text-danger-600">
              {riskData.filter(r => r.risk >= 0.6).length}
            </div>
            <div className="text-sm text-gray-600">High Risk Regions</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RiskAssessment;
