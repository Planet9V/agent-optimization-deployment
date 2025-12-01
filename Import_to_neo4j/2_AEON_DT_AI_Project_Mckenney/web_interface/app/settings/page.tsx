'use client';

import { useState } from 'react';
import { Card } from '@tremor/react';
import {
  Settings as SettingsIcon,
  Database,
  Bell,
  User,
  Shield,
  Palette,
  Globe,
  Save
} from 'lucide-react';

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    // Database Settings
    neo4jUrl: process.env.NEXT_PUBLIC_NEO4J_URI || 'bolt://localhost:7687',
    qdrantUrl: process.env.NEXT_PUBLIC_QDRANT_URL || 'http://localhost:6333',

    // Notifications
    emailNotifications: true,
    systemAlerts: true,
    weeklyReports: false,

    // Display
    theme: 'light',
    compactView: false,
    animationsEnabled: true,

    // Security
    twoFactorAuth: false,
    sessionTimeout: 30,

    // Language & Region
    language: 'en',
    timezone: 'America/New_York',
    dateFormat: 'MM/DD/YYYY',
  });

  const handleSave = async () => {
    // In a real app, this would save to backend
    console.log('Saving settings:', settings);
    alert('Settings saved successfully!');
  };

  return (
    <div className="p-8 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-3">
            <SettingsIcon className="h-8 w-8 text-blue-600" />
            <div>
              <h1 className="text-4xl font-bold text-gray-900">Settings</h1>
              <p className="text-lg text-gray-600 mt-1">
                Configure your AEON Digital Twin platform
              </p>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          {/* Database Configuration */}
          <Card>
            <div className="flex items-center space-x-3 mb-6">
              <Database className="h-6 w-6 text-blue-600" />
              <h2 className="text-2xl font-bold text-gray-900">Database Configuration</h2>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Neo4j Connection URL
                </label>
                <input
                  type="text"
                  value={settings.neo4jUrl}
                  onChange={(e) => setSettings({ ...settings, neo4jUrl: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="bolt://localhost:7687"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Qdrant Vector DB URL
                </label>
                <input
                  type="text"
                  value={settings.qdrantUrl}
                  onChange={(e) => setSettings({ ...settings, qdrantUrl: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="http://localhost:6333"
                />
              </div>
            </div>
          </Card>

          {/* Notifications */}
          <Card>
            <div className="flex items-center space-x-3 mb-6">
              <Bell className="h-6 w-6 text-blue-600" />
              <h2 className="text-2xl font-bold text-gray-900">Notifications</h2>
            </div>

            <div className="space-y-4">
              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={settings.emailNotifications}
                  onChange={(e) => setSettings({ ...settings, emailNotifications: e.target.checked })}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="text-gray-700">Email notifications</span>
              </label>

              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={settings.systemAlerts}
                  onChange={(e) => setSettings({ ...settings, systemAlerts: e.target.checked })}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="text-gray-700">System alerts</span>
              </label>

              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={settings.weeklyReports}
                  onChange={(e) => setSettings({ ...settings, weeklyReports: e.target.checked })}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="text-gray-700">Weekly reports</span>
              </label>
            </div>
          </Card>

          {/* Display Preferences */}
          <Card>
            <div className="flex items-center space-x-3 mb-6">
              <Palette className="h-6 w-6 text-blue-600" />
              <h2 className="text-2xl font-bold text-gray-900">Display Preferences</h2>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Theme
                </label>
                <select
                  value={settings.theme}
                  onChange={(e) => setSettings({ ...settings, theme: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="light">Light</option>
                  <option value="dark">Dark</option>
                  <option value="auto">Auto</option>
                </select>
              </div>

              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={settings.compactView}
                  onChange={(e) => setSettings({ ...settings, compactView: e.target.checked })}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="text-gray-700">Compact view</span>
              </label>

              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={settings.animationsEnabled}
                  onChange={(e) => setSettings({ ...settings, animationsEnabled: e.target.checked })}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="text-gray-700">Enable animations</span>
              </label>
            </div>
          </Card>

          {/* Security */}
          <Card>
            <div className="flex items-center space-x-3 mb-6">
              <Shield className="h-6 w-6 text-blue-600" />
              <h2 className="text-2xl font-bold text-gray-900">Security</h2>
            </div>

            <div className="space-y-4">
              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={settings.twoFactorAuth}
                  onChange={(e) => setSettings({ ...settings, twoFactorAuth: e.target.checked })}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <span className="text-gray-700">Enable two-factor authentication</span>
              </label>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Session timeout (minutes)
                </label>
                <input
                  type="number"
                  value={settings.sessionTimeout}
                  onChange={(e) => setSettings({ ...settings, sessionTimeout: parseInt(e.target.value) })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  min="5"
                  max="120"
                />
              </div>
            </div>
          </Card>

          {/* Language & Region */}
          <Card>
            <div className="flex items-center space-x-3 mb-6">
              <Globe className="h-6 w-6 text-blue-600" />
              <h2 className="text-2xl font-bold text-gray-900">Language & Region</h2>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Language
                </label>
                <select
                  value={settings.language}
                  onChange={(e) => setSettings({ ...settings, language: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="en">English</option>
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                  <option value="de">German</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Timezone
                </label>
                <select
                  value={settings.timezone}
                  onChange={(e) => setSettings({ ...settings, timezone: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="America/New_York">Eastern Time</option>
                  <option value="America/Chicago">Central Time</option>
                  <option value="America/Denver">Mountain Time</option>
                  <option value="America/Los_Angeles">Pacific Time</option>
                  <option value="UTC">UTC</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Date Format
                </label>
                <select
                  value={settings.dateFormat}
                  onChange={(e) => setSettings({ ...settings, dateFormat: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                  <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                  <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                </select>
              </div>
            </div>
          </Card>

          {/* Save Button */}
          <div className="flex justify-end">
            <button
              onClick={handleSave}
              className="flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
            >
              <Save className="h-5 w-5" />
              <span>Save Settings</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
