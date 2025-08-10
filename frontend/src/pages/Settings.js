import React, { useState } from 'react';
import { 
  Settings as SettingsIcon, 
  Save, 
  Key, 
  Globe, 
  Bell,
  Shield,
  Database
} from 'lucide-react';
import toast from 'react-hot-toast';

const Settings = () => {
  const [settings, setSettings] = useState({
    apiKeys: {
      openai: '',
      newsapi: '',
      yahoo: ''
    },
    notifications: {
      email: true,
      push: false,
      alerts: true
    },
    regions: ['North America', 'Europe', 'Asia-Pacific'],
    sectors: ['Technology', 'Energy', 'Finance'],
    refreshInterval: 300,
    dataRetention: 30
  });

  const [activeTab, setActiveTab] = useState('api');

  const handleSave = () => {
    // Save settings to localStorage or API
    localStorage.setItem('gma-settings', JSON.stringify(settings));
    toast.success('Settings saved successfully');
  };

  const handleApiKeyChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      apiKeys: {
        ...prev.apiKeys,
        [key]: value
      }
    }));
  };

  const handleNotificationChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      notifications: {
        ...prev.notifications,
        [key]: value
      }
    }));
  };

  const regions = ['North America', 'Europe', 'Asia-Pacific', 'Middle East', 'Africa', 'Latin America'];
  const sectors = ['Technology', 'Energy', 'Finance', 'Healthcare', 'Manufacturing', 'Consumer Goods'];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-600">Configure your geopolitical market analyzer</p>
        </div>
        <button
          onClick={handleSave}
          className="btn-primary flex items-center gap-2"
        >
          <Save className="h-4 w-4" />
          Save Settings
        </button>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'api', name: 'API Keys', icon: Key },
            { id: 'notifications', name: 'Notifications', icon: Bell },
            { id: 'regions', name: 'Regions', icon: Globe },
            { id: 'data', name: 'Data & Storage', icon: Database }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <tab.icon className="h-4 w-4" />
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* API Keys Tab */}
      {activeTab === 'api' && (
        <div className="card">
          <div className="flex items-center gap-3 mb-6">
            <Key className="h-6 w-6 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">API Configuration</h3>
          </div>
          
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                OpenAI API Key
              </label>
              <input
                type="password"
                value={settings.apiKeys.openai}
                onChange={(e) => handleApiKeyChange('openai', e.target.value)}
                placeholder="sk-..."
                className="input-field"
              />
              <p className="text-xs text-gray-500 mt-1">
                Required for AI-powered analysis and insights
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                NewsAPI Key (Optional)
              </label>
              <input
                type="password"
                value={settings.apiKeys.newsapi}
                onChange={(e) => handleApiKeyChange('newsapi', e.target.value)}
                placeholder="Enter your NewsAPI key"
                className="input-field"
              />
              <p className="text-xs text-gray-500 mt-1">
                For additional news sources and enhanced coverage
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Yahoo Finance API Key (Optional)
              </label>
              <input
                type="password"
                value={settings.apiKeys.yahoo}
                onChange={(e) => handleApiKeyChange('yahoo', e.target.value)}
                placeholder="Enter your Yahoo Finance API key"
                className="input-field"
              />
              <p className="text-xs text-gray-500 mt-1">
                For enhanced market data and historical analysis
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Notifications Tab */}
      {activeTab === 'notifications' && (
        <div className="card">
          <div className="flex items-center gap-3 mb-6">
            <Bell className="h-6 w-6 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">Notification Settings</h3>
          </div>
          
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-sm font-medium text-gray-900">Email Notifications</h4>
                <p className="text-sm text-gray-500">Receive analysis updates via email</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.notifications.email}
                  onChange={(e) => handleNotificationChange('email', e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
              </label>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-sm font-medium text-gray-900">Push Notifications</h4>
                <p className="text-sm text-gray-500">Receive real-time alerts in your browser</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.notifications.push}
                  onChange={(e) => handleNotificationChange('push', e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
              </label>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-sm font-medium text-gray-900">High Risk Alerts</h4>
                <p className="text-sm text-gray-500">Get notified of significant geopolitical risks</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.notifications.alerts}
                  onChange={(e) => handleNotificationChange('alerts', e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
              </label>
            </div>
          </div>
        </div>
      )}

      {/* Regions Tab */}
      {activeTab === 'regions' && (
        <div className="card">
          <div className="flex items-center gap-3 mb-6">
            <Globe className="h-6 w-6 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">Region & Sector Configuration</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h4 className="text-sm font-medium text-gray-900 mb-4">Default Regions</h4>
              <div className="space-y-3">
                {regions.map((region) => (
                  <label key={region} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={settings.regions.includes(region)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSettings(prev => ({
                            ...prev,
                            regions: [...prev.regions, region]
                          }));
                        } else {
                          setSettings(prev => ({
                            ...prev,
                            regions: prev.regions.filter(r => r !== region)
                          }));
                        }
                      }}
                      className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                    <span className="ml-3 text-sm text-gray-700">{region}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-900 mb-4">Default Sectors</h4>
              <div className="space-y-3">
                {sectors.map((sector) => (
                  <label key={sector} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={settings.sectors.includes(sector)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSettings(prev => ({
                            ...prev,
                            sectors: [...prev.sectors, sector]
                          }));
                        } else {
                          setSettings(prev => ({
                            ...prev,
                            sectors: prev.sectors.filter(s => s !== sector)
                          }));
                        }
                      }}
                      className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                    <span className="ml-3 text-sm text-gray-700">{sector}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Data & Storage Tab */}
      {activeTab === 'data' && (
        <div className="card">
          <div className="flex items-center gap-3 mb-6">
            <Database className="h-6 w-6 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">Data & Storage Settings</h3>
          </div>
          
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Data Refresh Interval (seconds)
              </label>
              <select
                value={settings.refreshInterval}
                onChange={(e) => setSettings(prev => ({ ...prev, refreshInterval: parseInt(e.target.value) }))}
                className="input-field"
              >
                <option value={60}>1 minute</option>
                <option value={300}>5 minutes</option>
                <option value={600}>10 minutes</option>
                <option value={1800}>30 minutes</option>
                <option value={3600}>1 hour</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">
                How often to refresh real-time data
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Data Retention Period (days)
              </label>
              <select
                value={settings.dataRetention}
                onChange={(e) => setSettings(prev => ({ ...prev, dataRetention: parseInt(e.target.value) }))}
                className="input-field"
              >
                <option value={7}>7 days</option>
                <option value={30}>30 days</option>
                <option value={90}>90 days</option>
                <option value={180}>180 days</option>
                <option value={365}>1 year</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">
                How long to keep historical data
              </p>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <h4 className="text-sm font-medium text-gray-900">Clear All Data</h4>
                <p className="text-sm text-gray-500">Remove all cached and stored data</p>
              </div>
              <button
                onClick={() => {
                  if (window.confirm('Are you sure you want to clear all data? This action cannot be undone.')) {
                    localStorage.clear();
                    toast.success('All data cleared successfully');
                  }
                }}
                className="px-4 py-2 text-sm font-medium text-danger-600 bg-danger-50 border border-danger-200 rounded-lg hover:bg-danger-100"
              >
                Clear Data
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Settings;
