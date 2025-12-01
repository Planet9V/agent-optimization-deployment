'use client';

import { useState, useEffect } from 'react';
import { Calendar, Download, TrendingUp, Activity, Zap } from 'lucide-react';
import CVETrendChart from '@/components/analytics/CVETrendChart';
import ThreatTimelineChart from '@/components/analytics/ThreatTimelineChart';
import SeasonalityHeatmap from '@/components/analytics/SeasonalityHeatmap';
import DateRangeSelector from '@/components/analytics/DateRangeSelector';

export default function AnalyticsTrendsPage() {
  const [dateRange, setDateRange] = useState({
    start: new Date(new Date().setMonth(new Date().getMonth() - 6)),
    end: new Date(),
  });

  const [loading, setLoading] = useState(false);
  const [cveTotals, setCveTotals] = useState({ total: 0, change: 0 });

  const handleDateRangeChange = (start: Date, end: Date) => {
    setDateRange({ start, end });
    // Trigger data refresh when date range changes
    setLoading(true);
    setTimeout(() => setLoading(false), 500); // Simulated loading
  };

  // Fetch CVE totals when date range changes
  useEffect(() => {
    const fetchCVETotals = async () => {
      try {
        const params = new URLSearchParams({
          startDate: dateRange.start.toISOString(),
          endDate: dateRange.end.toISOString(),
        });

        const response = await fetch(`/api/analytics/trends/cve?${params}`);
        const result = await response.json();

        if (result) {
          setCveTotals({
            total: result.totalCount || 0,
            change: result.percentChange || 0,
          });
        }
      } catch (error) {
        console.error('Error fetching CVE totals:', error);
      }
    };

    fetchCVETotals();
  }, [dateRange]);

  const exportToCSV = () => {
    // CSV export functionality
    console.log('Exporting to CSV...');
    alert('Export functionality will be implemented with real data');
  };

  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1
            className="text-3xl font-bold"
            style={{ color: 'var(--text-primary)' }}
          >
            Analytics & Trends
          </h1>
          <p
            className="mt-2 text-sm"
            style={{ color: 'var(--text-secondary)' }}
          >
            Time-series analysis of CVEs, threat actors, and attack campaigns
          </p>
        </div>
        <button
          onClick={exportToCSV}
          className="btn-primary flex items-center space-x-2"
        >
          <Download className="h-4 w-4" />
          <span>Export to CSV</span>
        </button>
      </div>

      {/* Date Range Selector */}
      <div className="card-modern p-4">
        <div className="flex items-center space-x-4">
          <Calendar className="h-5 w-5" style={{ color: 'var(--primary)' }} />
          <DateRangeSelector
            startDate={dateRange.start}
            endDate={dateRange.end}
            onChange={handleDateRangeChange}
          />
        </div>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card-modern p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                Total CVEs
              </p>
              <p className="text-3xl font-bold mt-2" style={{ color: 'var(--text-primary)' }}>
                {cveTotals.total.toLocaleString()}
              </p>
              <p className="text-sm mt-1" style={{ color: cveTotals.change >= 0 ? 'var(--success-500)' : 'var(--error-500)' }}>
                {cveTotals.change >= 0 ? '+' : ''}{cveTotals.change}% from last period
              </p>
            </div>
            <div
              className="p-3 rounded-lg"
              style={{ backgroundColor: 'var(--severity-critical-bg)' }}
            >
              <TrendingUp className="h-8 w-8" style={{ color: 'var(--severity-critical)' }} />
            </div>
          </div>
        </div>

        <div className="card-modern p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                Active Threat Actors
              </p>
              <p className="text-3xl font-bold mt-2" style={{ color: 'var(--text-primary)' }}>
                247
              </p>
              <p className="text-sm mt-1" style={{ color: 'var(--warning-500)' }}>
                +5% from last period
              </p>
            </div>
            <div
              className="p-3 rounded-lg"
              style={{ backgroundColor: 'var(--severity-high-bg)' }}
            >
              <Activity className="h-8 w-8" style={{ color: 'var(--severity-high)' }} />
            </div>
          </div>
        </div>

        <div className="card-modern p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                Attack Campaigns
              </p>
              <p className="text-3xl font-bold mt-2" style={{ color: 'var(--text-primary)' }}>
                89
              </p>
              <p className="text-sm mt-1" style={{ color: 'var(--error-500)' }}>
                +12% from last period
              </p>
            </div>
            <div
              className="p-3 rounded-lg"
              style={{ backgroundColor: 'var(--severity-medium-bg)' }}
            >
              <Zap className="h-8 w-8" style={{ color: 'var(--severity-medium)' }} />
            </div>
          </div>
        </div>
      </div>

      {/* CVE Discovery Trends */}
      <div className="card-modern p-6">
        <h2 className="text-xl font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
          CVE Discovery Trends
        </h2>
        <p className="text-sm mb-6" style={{ color: 'var(--text-secondary)' }}>
          Monthly CVE discovery rate by severity level
        </p>
        <CVETrendChart loading={loading} dateRange={dateRange} />
      </div>

      {/* Threat Actor Activity Timeline */}
      <div className="card-modern p-6">
        <h2 className="text-xl font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
          Threat Actor Activity Timeline
        </h2>
        <p className="text-sm mb-6" style={{ color: 'var(--text-secondary)' }}>
          Campaign activity over time by threat actor
        </p>
        <ThreatTimelineChart loading={loading} dateRange={dateRange} />
      </div>

      {/* Attack Campaign Seasonality */}
      <div className="card-modern p-6">
        <h2 className="text-xl font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
          Attack Campaign Seasonality
        </h2>
        <p className="text-sm mb-6" style={{ color: 'var(--text-secondary)' }}>
          Heatmap showing campaign frequency by month and year
        </p>
        <SeasonalityHeatmap loading={loading} />
      </div>
    </div>
  );
}
