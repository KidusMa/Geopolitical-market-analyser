import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import RealTimeAnalysis from './pages/RealTimeAnalysis';
import HistoricalAnalysis from './pages/HistoricalAnalysis';
import RiskAssessment from './pages/RiskAssessment';
import MarketImpact from './pages/MarketImpact';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <div className="App">
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/real-time" element={<RealTimeAnalysis />} />
            <Route path="/historical" element={<HistoricalAnalysis />} />
            <Route path="/risk-assessment" element={<RiskAssessment />} />
            <Route path="/market-impact" element={<MarketImpact />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Layout>
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#22c55e',
                secondary: '#fff',
              },
            },
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
      </div>
    </Router>
  );
}

export default App;
