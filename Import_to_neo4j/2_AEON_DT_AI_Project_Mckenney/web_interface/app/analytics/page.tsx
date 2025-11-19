'use client';

import React, { useState, useEffect } from 'react';
import { Card, Grid, Metric, Text, Flex, Badge, Button, Select, SelectItem } from '@tremor/react';
import {
  TrendingUp,
  TrendingDown,
  FileText,
  Database,
  CheckCircle,
  Star,
  Download,
  Filter,
} from 'lucide-react';
import { ChartCard } from '@/components/analytics/ChartCard';
import { ApexChartCard, LineChartCard, DonutChartCard, BarChartCard, HeatmapChartCard } from '@/components/analytics/ApexChartCard';

interface Metrics {
  documentGrowth: {
    current: number;
    previous: number;
    percentageChange: number;
  };
  entitiesAdded: {
    current: number;
    previous: number;
    percentageChange: number;
  };
  processSuccess: {
    current: number;
    percentageChange: number;
  };
  avgQuality: {
    current: number;
    previous: number;
    percentageChange: number;
  };
}

interface TimeSeriesData {
  documentsOverTime: Array<{ date: string; count: number }>;
  entitiesByType: Array<{ name: string; value: number }>;
  customerActivity: Array<{ name: string; documents: number; entities: number }>;
}

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState('30d');
  const [customerId, setCustomerId] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [timeSeriesData, setTimeSeriesData] = useState<TimeSeriesData | null>(null);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);

  useEffect(() => {
    fetchAnalyticsData();
  }, [timeRange, customerId]);

  const fetchAnalyticsData = async () => {
    setLoading(true);
    try {
      const metricsUrl = `/api/analytics/metrics?timeRange=${timeRange}${
        customerId ? `&customerId=${customerId}` : ''
      }`;
      const timeseriesUrl = `/api/analytics/timeseries?timeRange=${timeRange}${
        customerId ? `&customerId=${customerId}` : ''
      }`;

      const [metricsRes, timeseriesRes] = await Promise.all([
        fetch(metricsUrl),
        fetch(timeseriesUrl),
      ]);

      if (metricsRes.ok && timeseriesRes.ok) {
        const metricsData = await metricsRes.json();
        const timeseriesData = await timeseriesRes.json();
        setMetrics(metricsData);
        setTimeSeriesData(timeseriesData);
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (format: 'csv' | 'json' | 'pdf') => {
    setExporting(true);
    try {
      const response = await fetch('/api/analytics/export', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          format,
          timeRange,
          customerId,
        }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `analytics-${timeRange}-${Date.now()}.${format === 'pdf' ? 'txt' : format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Error exporting analytics:', error);
    } finally {
      setExporting(false);
    }
  };

  const formatChange = (change: number): string => {
    if (change > 0) return `+${change.toFixed(1)}%`;
    return `${change.toFixed(1)}%`;
  };

  const getTrendIcon = (change: number) => {
    if (change > 0) return <TrendingUp className="w-4 h-4 text-green-500" />;
    if (change < 0) return <TrendingDown className="w-4 h-4 text-red-500" />;
    return null;
  };

  return (
    <div className="min-h-screen bg-slate-950 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-50 mb-2">Analytics & Reporting</h1>
          <p className="text-slate-400">
            Monitor system performance and track key metrics over time
          </p>
        </div>

        {/* Filters */}
        <Card className="mb-6">
          <Flex justifyContent="between" alignItems="center">
            <Flex className="gap-4" alignItems="center">
              <div>
                <Text className="mb-2">Time Period</Text>
                <Select value={timeRange} onValueChange={setTimeRange}>
                  <SelectItem value="7d">Last 7 Days</SelectItem>
                  <SelectItem value="30d">Last 30 Days</SelectItem>
                  <SelectItem value="90d">Last 90 Days</SelectItem>
                </Select>
              </div>
              <div>
                <Text className="mb-2">Customer Filter</Text>
                <Select
                  value={customerId || 'all'}
                  onValueChange={(value) => setCustomerId(value === 'all' ? null : value)}
                >
                  <SelectItem value="all">All Customers</SelectItem>
                  {/* Add customer options dynamically */}
                </Select>
              </div>
            </Flex>
            <Flex className="gap-2">
              <Button
                size="xs"
                variant="secondary"
                icon={Download}
                onClick={() => handleExport('csv')}
                disabled={exporting}
              >
                CSV
              </Button>
              <Button
                size="xs"
                variant="secondary"
                icon={Download}
                onClick={() => handleExport('json')}
                disabled={exporting}
              >
                JSON
              </Button>
              <Button
                size="xs"
                variant="secondary"
                icon={Download}
                onClick={() => handleExport('pdf')}
                disabled={exporting}
              >
                PDF
              </Button>
            </Flex>
          </Flex>
        </Card>

        {/* Metrics Cards */}
        <Grid numItemsSm={2} numItemsLg={4} className="gap-6 mb-6">
          <Card decoration="top" decorationColor="blue">
            <Flex alignItems="start">
              <div className="flex-1">
                <Text>Document Growth</Text>
                <Metric>{metrics?.documentGrowth.current || 0}</Metric>
              </div>
              <FileText className="w-8 h-8 text-blue-500" />
            </Flex>
            {metrics && (
              <Flex justifyContent="start" className="mt-4">
                {getTrendIcon(metrics.documentGrowth.percentageChange)}
                <Text className="ml-2">
                  {formatChange(metrics.documentGrowth.percentageChange)}
                </Text>
              </Flex>
            )}
          </Card>

          <Card decoration="top" decorationColor="emerald">
            <Flex alignItems="start">
              <div className="flex-1">
                <Text>Entities Added</Text>
                <Metric>{metrics?.entitiesAdded.current || 0}</Metric>
              </div>
              <Database className="w-8 h-8 text-emerald-500" />
            </Flex>
            {metrics && (
              <Flex justifyContent="start" className="mt-4">
                {getTrendIcon(metrics.entitiesAdded.percentageChange)}
                <Text className="ml-2">
                  {formatChange(metrics.entitiesAdded.percentageChange)}
                </Text>
              </Flex>
            )}
          </Card>

          <Card decoration="top" decorationColor="green">
            <Flex alignItems="start">
              <div className="flex-1">
                <Text>Process Success</Text>
                <Metric>{metrics?.processSuccess.current || 0}%</Metric>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </Flex>
            <Flex justifyContent="start" className="mt-4">
              <Badge color="green" size="xs">
                Success Rate
              </Badge>
            </Flex>
          </Card>

          <Card decoration="top" decorationColor="amber">
            <Flex alignItems="start">
              <div className="flex-1">
                <Text>Avg Quality Score</Text>
                <Metric>{metrics?.avgQuality.current || 0}</Metric>
              </div>
              <Star className="w-8 h-8 text-amber-500" />
            </Flex>
            {metrics && (
              <Flex justifyContent="start" className="mt-4">
                {getTrendIcon(metrics.avgQuality.percentageChange)}
                <Text className="ml-2">{formatChange(metrics.avgQuality.percentageChange)}</Text>
              </Flex>
            )}
          </Card>
        </Grid>

        {/* Charts */}
        <Grid numItemsSm={1} numItemsLg={2} className="gap-6 mb-6">
          <ChartCard
            title="Documents Over Time"
            description="Track document creation trends"
            type="line"
            data={timeSeriesData?.documentsOverTime || []}
            dataKeys={{ x: 'date', y: 'count' }}
            loading={loading}
            height={300}
          />

          <ChartCard
            title="Entity Types Distribution"
            description="Breakdown of extracted entities by type"
            type="pie"
            data={timeSeriesData?.entitiesByType || []}
            dataKeys={{ name: 'name', value: 'value' }}
            loading={loading}
            height={300}
          />
        </Grid>

        <Grid numItemsSm={1} className="gap-6">
          <ChartCard
            title="Customer Activity"
            description="Documents and entities by customer"
            type="bar"
            data={timeSeriesData?.customerActivity || []}
            dataKeys={{ x: 'name' }}
            loading={loading}
            height={300}
          />
        </Grid>

        {/* OpenCTI-Style ApexCharts Visualizations */}
        <div className="mt-8 mb-4">
          <h2 className="text-2xl font-bold text-slate-50 mb-2">Advanced Visualizations</h2>
          <p className="text-slate-400 text-sm">
            OpenCTI-inspired threat intelligence and performance analytics
          </p>
        </div>

        <Grid numItemsSm={1} numItemsLg={2} className="gap-6 mb-6">
          {/* Threat Trend Analysis (Area Chart) */}
          <LineChartCard
            title="Threat Activity Timeline"
            description="Real-time threat detection and response metrics"
            series={[
              {
                name: 'Threats Detected',
                data: [45, 52, 48, 61, 58, 67, 72],
              },
              {
                name: 'Threats Mitigated',
                data: [38, 45, 43, 54, 51, 59, 65],
              },
            ]}
            categories={['Nov 01', 'Nov 02', 'Nov 03', 'Nov 04', 'Nov 05', 'Nov 06', 'Nov 07']}
            colors={['#ef4444', '#10b981']}
            loading={loading}
          />

          {/* Threat Severity Distribution (Donut Chart) */}
          <DonutChartCard
            title="Threat Severity Distribution"
            description="Breakdown of threats by severity level"
            series={[89, 156, 234, 421]}
            labels={['Critical', 'High', 'Medium', 'Low']}
            colors={['#d32f2f', '#f57c00', '#fbc02d', '#388e3c']}
            loading={loading}
          />
        </Grid>

        <Grid numItemsSm={1} numItemsLg={2} className="gap-6 mb-6">
          {/* Attack Vector Analysis (Bar Chart) */}
          <BarChartCard
            title="Top Attack Vectors"
            description="Most common attack techniques observed"
            series={[
              {
                name: 'Incidents',
                data: [342, 289, 234, 198, 167, 143, 128, 95],
              },
            ]}
            categories={[
              'Phishing',
              'Malware',
              'SQL Injection',
              'XSS',
              'DDoS',
              'Brute Force',
              'MITM',
              'Zero-Day',
            ]}
            colors={['#10b981']}
            loading={loading}
          />

          {/* System Performance Heatmap */}
          <HeatmapChartCard
            title="System Performance Matrix"
            description="Service uptime and response time by hour"
            series={[
              {
                name: '00:00 - 04:00',
                data: [98, 95, 97, 99, 96, 98, 100],
              },
              {
                name: '04:00 - 08:00',
                data: [92, 88, 90, 94, 91, 93, 95],
              },
              {
                name: '08:00 - 12:00',
                data: [75, 72, 68, 70, 74, 76, 78],
              },
              {
                name: '12:00 - 16:00',
                data: [82, 80, 78, 85, 83, 87, 90],
              },
              {
                name: '16:00 - 20:00',
                data: [88, 85, 90, 92, 89, 91, 94],
              },
              {
                name: '20:00 - 24:00',
                data: [95, 93, 96, 98, 97, 99, 100],
              },
            ]}
            categories={['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']}
            loading={loading}
          />
        </Grid>
      </div>
    </div>
  );
}
