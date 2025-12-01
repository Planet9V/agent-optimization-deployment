/**
 * Observability Dashboard Page
 *
 * Real-time system monitoring with metrics from observability modules
 * Displays charts and graphs for system health, performance, and agent activity
 */

'use client';

import { useEffect, useState } from 'react';
import { Line, Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

interface SystemMetrics {
  timestamp: string;
  memory: {
    heapUsed: number;
    heapTotal: number;
    rss: number;
    external: number;
    percentage: number;
  };
  cpu: {
    user: number;
    system: number;
  };
  uptime: number;
  status: 'healthy' | 'warning' | 'critical';
}

interface AgentMetrics {
  activeAgents: number;
  completedTasks: number;
  failedTasks: number;
  averageDuration: number;
}

interface PerformanceMetrics {
  avgResponseTime: number;
  p95ResponseTime: number;
  throughput: number;
  errorRate: number;
}

export default function ObservabilityPage() {
  const [systemMetrics, setSystemMetrics] = useState<SystemMetrics | null>(null);
  const [agentMetrics, setAgentMetrics] = useState<AgentMetrics | null>(null);
  const [performanceMetrics, setPerformanceMetrics] = useState<PerformanceMetrics | null>(null);
  const [historicalData, setHistoricalData] = useState<SystemMetrics[]>([]);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [refreshInterval, setRefreshInterval] = useState(5000); // 5 seconds

  // Fetch current metrics
  const fetchMetrics = async () => {
    try {
      const [systemRes, agentRes, perfRes] = await Promise.all([
        fetch('/api/observability/system'),
        fetch('/api/observability/agents'),
        fetch('/api/observability/performance')
      ]);

      const systemData = await systemRes.json();
      const agentData = await agentRes.json();
      const perfData = await perfRes.json();

      setSystemMetrics(systemData);
      setAgentMetrics(agentData);
      setPerformanceMetrics(perfData);

      // Add to historical data (keep last 60 data points)
      setHistoricalData(prev => {
        const updated = [...prev, systemData];
        return updated.slice(-60);
      });
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
    }
  };

  // Auto-refresh metrics
  useEffect(() => {
    fetchMetrics();

    if (autoRefresh) {
      const interval = setInterval(fetchMetrics, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [autoRefresh, refreshInterval]);

  // Memory usage chart data
  const memoryChartData = {
    labels: historicalData.map((d, i) => {
      const time = new Date(d.timestamp);
      return `${time.getHours()}:${String(time.getMinutes()).padStart(2, '0')}:${String(time.getSeconds()).padStart(2, '0')}`;
    }),
    datasets: [
      {
        label: 'Heap Used (MB)',
        data: historicalData.map(d => d.memory.heapUsed / 1024 / 1024),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4
      },
      {
        label: 'Heap Total (MB)',
        data: historicalData.map(d => d.memory.heapTotal / 1024 / 1024),
        borderColor: 'rgb(156, 163, 175)',
        backgroundColor: 'rgba(156, 163, 175, 0.1)',
        fill: false,
        tension: 0.4
      }
    ]
  };

  // CPU usage chart data
  const cpuChartData = {
    labels: historicalData.map((d, i) => {
      const time = new Date(d.timestamp);
      return `${time.getHours()}:${String(time.getMinutes()).padStart(2, '0')}:${String(time.getSeconds()).padStart(2, '0')}`;
    }),
    datasets: [
      {
        label: 'User CPU (ms)',
        data: historicalData.map(d => d.cpu.user / 1000),
        borderColor: 'rgb(16, 185, 129)',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        fill: true,
        tension: 0.4
      },
      {
        label: 'System CPU (ms)',
        data: historicalData.map(d => d.cpu.system / 1000),
        borderColor: 'rgb(245, 158, 11)',
        backgroundColor: 'rgba(245, 158, 11, 0.1)',
        fill: true,
        tension: 0.4
      }
    ]
  };

  // Agent activity pie chart
  const agentActivityData = agentMetrics ? {
    labels: ['Completed', 'Active', 'Failed'],
    datasets: [
      {
        data: [
          agentMetrics.completedTasks,
          agentMetrics.activeAgents,
          agentMetrics.failedTasks
        ],
        backgroundColor: [
          'rgba(16, 185, 129, 0.8)',
          'rgba(59, 130, 246, 0.8)',
          'rgba(239, 68, 68, 0.8)'
        ],
        borderColor: [
          'rgb(16, 185, 129)',
          'rgb(59, 130, 246)',
          'rgb(239, 68, 68)'
        ],
        borderWidth: 2
      }
    ]
  } : null;

  // Performance bar chart
  const performanceChartData = performanceMetrics ? {
    labels: ['Avg Response', 'P95 Response', 'Throughput (req/min)'],
    datasets: [
      {
        label: 'Performance Metrics',
        data: [
          performanceMetrics.avgResponseTime,
          performanceMetrics.p95ResponseTime,
          performanceMetrics.throughput
        ],
        backgroundColor: [
          'rgba(59, 130, 246, 0.8)',
          'rgba(245, 158, 11, 0.8)',
          'rgba(16, 185, 129, 0.8)'
        ]
      }
    ]
  } : null;

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'bg-green-500';
      case 'warning': return 'bg-yellow-500';
      case 'critical': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'healthy': return 'Healthy';
      case 'warning': return 'Warning';
      case 'critical': return 'Critical';
      default: return 'Unknown';
    }
  };

  return (
    <div className="container mx-auto p-8 max-w-7xl">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-high-contrast mb-2">Observability Dashboard</h1>
          <p className="text-gray-600">Real-time system monitoring and performance metrics</p>
        </div>

        <div className="flex items-center gap-4">
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="rounded"
            />
            <span className="text-sm text-gray-700">Auto-refresh</span>
          </label>

          <select
            value={refreshInterval}
            onChange={(e) => setRefreshInterval(Number(e.target.value))}
            className="input-professional text-sm py-1.5"
            disabled={!autoRefresh}
          >
            <option value={2000}>2s</option>
            <option value={5000}>5s</option>
            <option value={10000}>10s</option>
            <option value={30000}>30s</option>
          </select>

          <button
            onClick={fetchMetrics}
            className="btn-professional btn-professional-primary text-sm"
          >
            Refresh Now
          </button>
        </div>
      </div>

      {/* System Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {/* System Health Status */}
        <div className="card-professional p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-semibold text-gray-600 uppercase tracking-wide">System Status</h3>
            <div className={`w-3 h-3 rounded-full ${systemMetrics ? getStatusColor(systemMetrics.status) : 'bg-gray-300'} animate-pulse`}></div>
          </div>
          <p className="text-2xl font-bold text-high-contrast">
            {systemMetrics ? getStatusText(systemMetrics.status) : 'Loading...'}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            Uptime: {systemMetrics ? Math.round(systemMetrics.uptime / 60) : 0}m
          </p>
        </div>

        {/* Memory Usage */}
        <div className="card-professional p-6">
          <h3 className="text-sm font-semibold text-gray-600 mb-2 uppercase tracking-wide">Memory Usage</h3>
          <p className="text-2xl font-bold text-high-contrast">
            {systemMetrics ? Math.round(systemMetrics.memory.percentage) : 0}%
          </p>
          <p className="text-xs text-gray-500 mt-1">
            {systemMetrics ? Math.round(systemMetrics.memory.heapUsed / 1024 / 1024) : 0}MB /
            {systemMetrics ? Math.round(systemMetrics.memory.heapTotal / 1024 / 1024) : 0}MB
          </p>
        </div>

        {/* Active Agents */}
        <div className="card-professional p-6">
          <h3 className="text-sm font-semibold text-gray-600 mb-2 uppercase tracking-wide">Active Agents</h3>
          <p className="text-2xl font-bold text-high-contrast">
            {agentMetrics ? agentMetrics.activeAgents : 0}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            Avg Duration: {agentMetrics ? Math.round(agentMetrics.averageDuration) : 0}ms
          </p>
        </div>

        {/* Performance */}
        <div className="card-professional p-6">
          <h3 className="text-sm font-semibold text-gray-600 mb-2 uppercase tracking-wide">Avg Response</h3>
          <p className="text-2xl font-bold text-high-contrast">
            {performanceMetrics ? Math.round(performanceMetrics.avgResponseTime) : 0}ms
          </p>
          <p className="text-xs text-gray-500 mt-1">
            Error Rate: {performanceMetrics ? performanceMetrics.errorRate.toFixed(2) : 0}%
          </p>
        </div>
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Memory Usage Over Time */}
        <div className="card-professional p-6">
          <h3 className="text-lg font-semibold text-high-contrast mb-4">Memory Usage Over Time</h3>
          {historicalData.length > 0 ? (
            <Line
              data={memoryChartData}
              options={{
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                  y: {
                    beginAtZero: true,
                    title: {
                      display: true,
                      text: 'Memory (MB)'
                    }
                  }
                },
                plugins: {
                  legend: {
                    position: 'top' as const
                  }
                }
              }}
            />
          ) : (
            <div className="h-64 flex items-center justify-center text-gray-400">
              Collecting data...
            </div>
          )}
        </div>

        {/* CPU Usage Over Time */}
        <div className="card-professional p-6">
          <h3 className="text-lg font-semibold text-high-contrast mb-4">CPU Usage Over Time</h3>
          {historicalData.length > 0 ? (
            <Line
              data={cpuChartData}
              options={{
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                  y: {
                    beginAtZero: true,
                    title: {
                      display: true,
                      text: 'CPU Time (ms)'
                    }
                  }
                },
                plugins: {
                  legend: {
                    position: 'top' as const
                  }
                }
              }}
            />
          ) : (
            <div className="h-64 flex items-center justify-center text-gray-400">
              Collecting data...
            </div>
          )}
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Agent Activity Distribution */}
        <div className="card-professional p-6">
          <h3 className="text-lg font-semibold text-high-contrast mb-4">Agent Activity Distribution</h3>
          {agentActivityData ? (
            <div className="flex justify-center">
              <div style={{ maxWidth: '300px', maxHeight: '300px' }}>
                <Pie
                  data={agentActivityData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                      legend: {
                        position: 'bottom' as const
                      }
                    }
                  }}
                />
              </div>
            </div>
          ) : (
            <div className="h-64 flex items-center justify-center text-gray-400">
              Loading agent data...
            </div>
          )}
        </div>

        {/* Performance Metrics */}
        <div className="card-professional p-6">
          <h3 className="text-lg font-semibold text-high-contrast mb-4">Performance Metrics</h3>
          {performanceChartData ? (
            <Bar
              data={performanceChartData}
              options={{
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                  y: {
                    beginAtZero: true
                  }
                },
                plugins: {
                  legend: {
                    display: false
                  }
                }
              }}
            />
          ) : (
            <div className="h-64 flex items-center justify-center text-gray-400">
              Loading performance data...
            </div>
          )}
        </div>
      </div>

      {/* Real-time System Details */}
      <div className="mt-6 card-professional p-6">
        <h3 className="text-lg font-semibold text-high-contrast mb-4">System Details</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h4 className="text-sm font-semibold text-gray-600 mb-2">Memory Details</h4>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Heap Used:</span>
                <span className="font-mono">{systemMetrics ? Math.round(systemMetrics.memory.heapUsed / 1024 / 1024) : 0} MB</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Heap Total:</span>
                <span className="font-mono">{systemMetrics ? Math.round(systemMetrics.memory.heapTotal / 1024 / 1024) : 0} MB</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">RSS:</span>
                <span className="font-mono">{systemMetrics ? Math.round(systemMetrics.memory.rss / 1024 / 1024) : 0} MB</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">External:</span>
                <span className="font-mono">{systemMetrics ? Math.round(systemMetrics.memory.external / 1024 / 1024) : 0} MB</span>
              </div>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-gray-600 mb-2">Agent Metrics</h4>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Active:</span>
                <span className="font-mono">{agentMetrics ? agentMetrics.activeAgents : 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Completed:</span>
                <span className="font-mono text-green-600">{agentMetrics ? agentMetrics.completedTasks : 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Failed:</span>
                <span className="font-mono text-red-600">{agentMetrics ? agentMetrics.failedTasks : 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Avg Duration:</span>
                <span className="font-mono">{agentMetrics ? Math.round(agentMetrics.averageDuration) : 0} ms</span>
              </div>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-gray-600 mb-2">Performance</h4>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Avg Response:</span>
                <span className="font-mono">{performanceMetrics ? Math.round(performanceMetrics.avgResponseTime) : 0} ms</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">P95 Response:</span>
                <span className="font-mono">{performanceMetrics ? Math.round(performanceMetrics.p95ResponseTime) : 0} ms</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Throughput:</span>
                <span className="font-mono">{performanceMetrics ? Math.round(performanceMetrics.throughput) : 0} req/min</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Error Rate:</span>
                <span className="font-mono">{performanceMetrics ? performanceMetrics.errorRate.toFixed(2) : 0}%</span>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-4 pt-4 border-t text-xs text-gray-500">
          Last updated: {systemMetrics ? new Date(systemMetrics.timestamp).toLocaleString() : 'N/A'}
        </div>
      </div>
    </div>
  );
}
