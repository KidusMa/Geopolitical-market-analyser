import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// News API
export const newsAPI = {
  getLatestNews: (regions = []) => 
    api.get('/news/latest', { params: { regions } }),
  
  getHistoricalNews: (startDate, endDate, regions = []) =>
    api.get('/news/historical', { params: { startDate, endDate, regions } }),
  
  analyzeSentiment: (text) =>
    api.post('/news/sentiment', { text }),
};

// Market API
export const marketAPI = {
  getMarketData: (symbols = []) =>
    api.get('/market/data', { params: { symbols } }),
  
  getMarketIndicators: () =>
    api.get('/market/indicators'),
  
  getHistoricalData: (symbol, startDate, endDate) =>
    api.get('/market/historical', { params: { symbol, startDate, endDate } }),
};

// Analysis API
export const analysisAPI = {
  generateAnalysis: (newsData, marketData) =>
    api.post('/analysis/generate', { newsData, marketData }),
  
  getRiskAssessment: (regions = []) =>
    api.get('/analysis/risk', { params: { regions } }),
  
  getMarketImpact: (sectors = []) =>
    api.get('/analysis/impact', { params: { sectors } }),
};

// Dashboard API
export const dashboardAPI = {
  getOverview: () =>
    api.get('/dashboard/overview'),
  
  getMetrics: () =>
    api.get('/dashboard/metrics'),
  
  getRecentActivity: () =>
    api.get('/dashboard/activity'),
};

export default api;
