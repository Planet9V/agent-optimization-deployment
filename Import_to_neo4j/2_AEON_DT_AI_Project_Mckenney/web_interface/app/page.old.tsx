'use client';

import { useEffect, useState } from 'react';
import {
  Database,
  FileText,
  Network,
  Shield,
  AlertTriangle,
  Bug,
  Target,
  Activity,
  Server,
  Upload,
  Search,
  BarChart3,
  ArrowRight
} from 'lucide-react';

interface DashboardStats {
  totalDocuments: number;
  totalEntities: number;
  totalRelationships: number;
  totalCustomers: number;
  totalTags: number;
  totalSharedDocuments: number;
}

interface CyberStats {
  cves: {
    total: number;
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  threatActors: number;
  malware: number;
  campaigns: number;
  attackTechniques: number;
  icsAssets: number;
  cweWeaknesses: number;
}

interface ServiceStatus {
  name: string;
  status: 'healthy' | 'degraded' | 'down';
  responseTime?: number;
  uptime?: string;
  icon: React.ReactNode;
}

interface Activity {
  id: string;
  type: 'upload' | 'edit' | 'delete' | 'processed' | 'error';
  title: string;
  description: string;
  timestamp: Date;
  user?: string;
}

export default function HomePage() {
  const [stats, setStats] = useState<DashboardStats>({
    totalDocuments: 0,
    totalEntities: 0,
    totalRelationships: 0,
    totalCustomers: 0,
    totalTags: 0,
    totalSharedDocuments: 0
  });
  const [cyberStats, setCyberStats] = useState<CyberStats>({
    cves: { total: 0, critical: 0, high: 0, medium: 0, low: 0 },
    threatActors: 0,
    malware: 0,
    campaigns: 0,
    attackTechniques: 0,
    icsAssets: 0,
    cweWeaknesses: 0
  });
  const [services, setServices] = useState<ServiceStatus[]>([]);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dbConnected, setDbConnected] = useState<boolean>(false);

  // Fetch dashboard data
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch Neo4j statistics
        const statsResponse = await fetch('/api/neo4j/statistics');
        if (statsResponse.ok) {
          const statsData = await statsResponse.json();
          setDbConnected(true);
          setStats({
            totalDocuments: statsData.totalDocuments || 0,
            totalEntities: statsData.totalEntities || 0,
            totalRelationships: statsData.totalRelationships || 0,
            totalCustomers: statsData.totalCustomers || 0,
            totalTags: statsData.totalTags || 0,
            totalSharedDocuments: statsData.totalSharedDocuments || 0
          });
        } else {
          setDbConnected(false);
        }

        // Fetch Cybersecurity statistics
        const cyberStatsResponse = await fetch('/api/neo4j/cyber-statistics');
        if (cyberStatsResponse.ok) {
          const cyberStatsData = await cyberStatsResponse.json();
          setCyberStats({
            cves: cyberStatsData.cves || { total: 0, critical: 0, high: 0, medium: 0, low: 0 },
            threatActors: cyberStatsData.threatActors || 0,
            malware: cyberStatsData.malware || 0,
            campaigns: cyberStatsData.campaigns || 0,
            attackTechniques: cyberStatsData.attackTechniques || 0,
            icsAssets: cyberStatsData.icsAssets || 0,
            cweWeaknesses: cyberStatsData.cweWeaknesses || 0
          });
        }

        // Fetch system health
        const healthResponse = await fetch('/api/health');
        if (healthResponse.ok) {
          const healthData = await healthResponse.json();

          const serviceStatuses: ServiceStatus[] = [
            {
              name: 'Neo4j',
              status: healthData.neo4j?.connected ? 'healthy' : 'down',
              responseTime: healthData.neo4j?.responseTime,
              uptime: healthData.neo4j?.uptime || '99.9%',
              icon: <Database className="h-5 w-5" />
            },
            {
              name: 'Qdrant',
              status: healthData.qdrant?.connected ? 'healthy' : 'down',
              responseTime: healthData.qdrant?.responseTime,
              uptime: healthData.qdrant?.uptime || '99.8%',
              icon: <Database className="h-5 w-5" />
            },
            {
              name: 'MySQL',
              status: healthData.mysql?.connected ? 'healthy' : 'down',
              responseTime: healthData.mysql?.responseTime,
              uptime: healthData.mysql?.uptime || '99.9%',
              icon: <Database className="h-5 w-5" />
            },
            {
              name: 'MinIO',
              status: healthData.minio?.connected ? 'healthy' : 'down',
              responseTime: healthData.minio?.responseTime,
              uptime: healthData.minio?.uptime || '99.7%',
              icon: <Database className="h-5 w-5" />
            },
            {
              name: 'API',
              status: healthData.api?.status === 'operational' ? 'healthy' : 'degraded',
              responseTime: healthData.api?.responseTime,
              uptime: '99.9%',
              icon: <Network className="h-5 w-5" />
            },
            {
              name: 'Vector DB',
              status: healthData.vectorDb?.connected ? 'healthy' : 'down',
              responseTime: healthData.vectorDb?.responseTime,
              uptime: '99.8%',
              icon: <Database className="h-5 w-5" />
            }
          ];

          setServices(serviceStatuses);
        }

        // Fetch recent activity
        const activityResponse = await fetch('/api/activity/recent?limit=10');
        if (activityResponse.ok) {
          const activityData = await activityResponse.json();
          setActivities(activityData.activities || []);
        }

      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
        setError('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();

    // Set up polling for real-time updates (every 30 seconds)
    const interval = setInterval(fetchDashboardData, 30000);

    return () => clearInterval(interval);
  }, []);

  // Handle service refresh
  const handleRefreshServices = async () => {
    try {
      const healthResponse = await fetch('/api/health');
      if (healthResponse.ok) {
        const healthData = await healthResponse.json();

        const serviceStatuses: ServiceStatus[] = [
          {
            name: 'Neo4j',
            status: healthData.neo4j?.connected ? 'healthy' : 'down',
            responseTime: healthData.neo4j?.responseTime,
            uptime: healthData.neo4j?.uptime || '99.9%',
            icon: <Database className="h-5 w-5" />
          },
          {
            name: 'Qdrant',
            status: healthData.qdrant?.connected ? 'healthy' : 'down',
            responseTime: healthData.qdrant?.responseTime,
            uptime: healthData.qdrant?.uptime || '99.8%',
            icon: <Database className="h-5 w-5" />
          },
          {
            name: 'MySQL',
            status: healthData.mysql?.connected ? 'healthy' : 'down',
            responseTime: healthData.mysql?.responseTime,
            uptime: healthData.mysql?.uptime || '99.9%',
            icon: <Database className="h-5 w-5" />
          },
          {
            name: 'MinIO',
            status: healthData.minio?.connected ? 'healthy' : 'down',
            responseTime: healthData.minio?.responseTime,
            uptime: healthData.minio?.uptime || '99.7%',
            icon: <Database className="h-5 w-5" />
          },
          {
            name: 'API',
            status: healthData.api?.status === 'operational' ? 'healthy' : 'degraded',
            responseTime: healthData.api?.responseTime,
            uptime: '99.9%',
            icon: <Network className="h-5 w-5" />
          },
          {
            name: 'Vector DB',
            status: healthData.vectorDb?.connected ? 'healthy' : 'down',
            responseTime: healthData.vectorDb?.responseTime,
            uptime: '99.8%',
            icon: <Database className="h-5 w-5" />
          }
        ];

        setServices(serviceStatuses);
      }
    } catch (err) {
      console.error('Failed to refresh service status:', err);
    }
  };

  return (
    <div className="relative">
      {/* Hero Section */}
      <section className="px-6 py-24 max-w-7xl mx-auto">
        <div className="text-center space-y-6 animate-fadeIn">
          <h1 className="text-5xl md:text-6xl font-bold text-slate-50 tracking-tight">
            AEON Digital Twin
          </h1>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto">
            Neo4j-powered cybersecurity knowledge graph for threat intelligence and vulnerability management
          </p>
          {error && (
            <div className="mt-4 p-4 rounded-lg bg-red-900/20 border border-red-500/30 text-red-300 max-w-2xl mx-auto">
              {error}
            </div>
          )}
        </div>
      </section>

      {/* Metrics Grid */}
      <section className="px-6 pb-16 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Documents Card */}
          <div className="group bg-slate-900/80 backdrop-blur-sm rounded-xl p-6 border border-emerald-500/20 hover:border-emerald-500/40 transition-all hover:scale-105 hover:shadow-emerald-500/20 hover:shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <FileText className="h-8 w-8 text-emerald-500" />
              <span className="text-2xl font-bold text-slate-50">
                {loading ? '...' : (dbConnected ? stats.totalDocuments.toLocaleString() : 'N/A')}
              </span>
            </div>
            <h3 className="text-sm font-medium text-slate-400">Documents</h3>
            <p className="text-xs text-slate-500 mt-1">
              {dbConnected && stats.totalDocuments > 0 ? `${stats.totalDocuments} total` : 'Database required'}
            </p>
          </div>

          {/* Entities Card */}
          <div className="group bg-slate-900/80 backdrop-blur-sm rounded-xl p-6 border border-emerald-500/20 hover:border-emerald-500/40 transition-all hover:scale-105 hover:shadow-emerald-500/20 hover:shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <Network className="h-8 w-8 text-emerald-500" />
              <span className="text-2xl font-bold text-slate-50">
                {loading ? '...' : (dbConnected ? stats.totalEntities.toLocaleString() : 'N/A')}
              </span>
            </div>
            <h3 className="text-sm font-medium text-slate-400">Entities</h3>
            <p className="text-xs text-slate-500 mt-1">
              {dbConnected && stats.totalEntities > 0 ? `${stats.totalEntities} total` : 'Database required'}
            </p>
          </div>

          {/* Relationships Card */}
          <div className="group bg-slate-900/80 backdrop-blur-sm rounded-xl p-6 border border-emerald-500/20 hover:border-emerald-500/40 transition-all hover:scale-105 hover:shadow-emerald-500/20 hover:shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <Database className="h-8 w-8 text-emerald-500" />
              <span className="text-2xl font-bold text-slate-50">
                {loading ? '...' : (dbConnected ? stats.totalRelationships.toLocaleString() : 'N/A')}
              </span>
            </div>
            <h3 className="text-sm font-medium text-slate-400">Relationships</h3>
            <p className="text-xs text-slate-500 mt-1">
              {dbConnected && stats.totalRelationships > 0 ? `${stats.totalRelationships} total` : 'Database required'}
            </p>
          </div>
        </div>
      </section>

      {/* Cybersecurity Metrics Section */}
      <section className="px-6 pb-16 max-w-7xl mx-auto">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-slate-50 mb-2">
            Threat Intelligence
          </h2>
          <p className="text-slate-400">
            Real-time cybersecurity metrics from Neo4j database
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* CVE Card */}
          <div className="group bg-slate-900/80 backdrop-blur-sm rounded-xl p-6 border border-red-500/20 hover:border-red-500/40 transition-all hover:scale-105 hover:shadow-red-500/20 hover:shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <Shield className="h-8 w-8 text-red-500" />
              <span className="text-2xl font-bold text-slate-50">
                {loading ? '...' : cyberStats.cves.total.toLocaleString()}
              </span>
            </div>
            <h3 className="text-sm font-medium text-slate-400">CVE Vulnerabilities</h3>
            <p className="text-xs text-slate-500 mt-1">
              {cyberStats.cves.total > 0 ? `${cyberStats.cves.critical} critical` : 'No CVEs'}
            </p>
          </div>

          {/* Threat Actors Card */}
          <div className="group bg-slate-900/80 backdrop-blur-sm rounded-xl p-6 border border-orange-500/20 hover:border-orange-500/40 transition-all hover:scale-105 hover:shadow-orange-500/20 hover:shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <AlertTriangle className="h-8 w-8 text-orange-500" />
              <span className="text-2xl font-bold text-slate-50">
                {loading ? '...' : cyberStats.threatActors.toLocaleString()}
              </span>
            </div>
            <h3 className="text-sm font-medium text-slate-400">Threat Actors</h3>
            <p className="text-xs text-slate-500 mt-1">
              {cyberStats.threatActors > 0 ? `${cyberStats.campaigns} active campaigns` : 'No threats'}
            </p>
          </div>

          {/* Malware Card */}
          <div className="group bg-slate-900/80 backdrop-blur-sm rounded-xl p-6 border border-purple-500/20 hover:border-purple-500/40 transition-all hover:scale-105 hover:shadow-purple-500/20 hover:shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <Bug className="h-8 w-8 text-purple-500" />
              <span className="text-2xl font-bold text-slate-50">
                {loading ? '...' : cyberStats.malware.toLocaleString()}
              </span>
            </div>
            <h3 className="text-sm font-medium text-slate-400">Malware Families</h3>
            <p className="text-xs text-slate-500 mt-1">
              {cyberStats.malware > 0 ? 'Tracked variants' : 'No malware'}
            </p>
          </div>

          {/* Attack Techniques Card */}
          <div className="group bg-slate-900/80 backdrop-blur-sm rounded-xl p-6 border border-blue-500/20 hover:border-blue-500/40 transition-all hover:scale-105 hover:shadow-blue-500/20 hover:shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <Target className="h-8 w-8 text-blue-500" />
              <span className="text-2xl font-bold text-slate-50">
                {loading ? '...' : cyberStats.attackTechniques.toLocaleString()}
              </span>
            </div>
            <h3 className="text-sm font-medium text-slate-400">Attack Techniques</h3>
            <p className="text-xs text-slate-500 mt-1">
              {cyberStats.attackTechniques > 0 ? 'MITRE ATT&CK' : 'No techniques'}
            </p>
          </div>

          {/* CWE Card */}
          <div className="group bg-slate-900/80 backdrop-blur-sm rounded-xl p-6 border border-yellow-500/20 hover:border-yellow-500/40 transition-all hover:scale-105 hover:shadow-yellow-500/20 hover:shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <Activity className="h-8 w-8 text-yellow-500" />
              <span className="text-2xl font-bold text-slate-50">
                {loading ? '...' : cyberStats.cweWeaknesses.toLocaleString()}
              </span>
            </div>
            <h3 className="text-sm font-medium text-slate-400">CWE Weaknesses</h3>
            <p className="text-xs text-slate-500 mt-1">
              {cyberStats.cweWeaknesses > 0 ? 'Common weaknesses' : 'No CWEs'}
            </p>
          </div>

          {/* ICS Assets Card */}
          <div className="group bg-slate-900/80 backdrop-blur-sm rounded-xl p-6 border border-green-500/20 hover:border-green-500/40 transition-all hover:scale-105 hover:shadow-green-500/20 hover:shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <Server className="h-8 w-8 text-green-500" />
              <span className="text-2xl font-bold text-slate-50">
                {loading ? '...' : cyberStats.icsAssets.toLocaleString()}
              </span>
            </div>
            <h3 className="text-sm font-medium text-slate-400">ICS Assets</h3>
            <p className="text-xs text-slate-500 mt-1">
              {cyberStats.icsAssets > 0 ? 'Critical infrastructure' : 'No assets'}
            </p>
          </div>
        </div>
      </section>

      {/* Quick Actions */}
      <section className="px-6 pb-16 max-w-7xl mx-auto">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-slate-50 mb-2">Quick Actions</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <button className="group bg-slate-900/80 backdrop-blur-sm rounded-xl p-6 border border-emerald-500/20 hover:border-emerald-500/40 transition-all hover:scale-105 hover:shadow-emerald-500/20 hover:shadow-xl text-left">
            <Upload className="h-8 w-8 text-emerald-500 mb-4" />
            <h3 className="text-lg font-semibold text-slate-50 mb-2">Upload Documents</h3>
            <p className="text-sm text-slate-400">Import new documents into the knowledge graph</p>
            <ArrowRight className="h-5 w-5 text-emerald-500 mt-4 group-hover:translate-x-2 transition-transform" />
          </button>

          <button className="group bg-slate-900/80 backdrop-blur-sm rounded-xl p-6 border border-emerald-500/20 hover:border-emerald-500/40 transition-all hover:scale-105 hover:shadow-emerald-500/20 hover:shadow-xl text-left">
            <Search className="h-8 w-8 text-emerald-500 mb-4" />
            <h3 className="text-lg font-semibold text-slate-50 mb-2">Search Intelligence</h3>
            <p className="text-sm text-slate-400">Query threat intelligence and vulnerabilities</p>
            <ArrowRight className="h-5 w-5 text-emerald-500 mt-4 group-hover:translate-x-2 transition-transform" />
          </button>

          <button className="group bg-slate-900/80 backdrop-blur-sm rounded-xl p-6 border border-emerald-500/20 hover:border-emerald-500/40 transition-all hover:scale-105 hover:shadow-emerald-500/20 hover:shadow-xl text-left">
            <BarChart3 className="h-8 w-8 text-emerald-500 mb-4" />
            <h3 className="text-lg font-semibold text-slate-50 mb-2">View Analytics</h3>
            <p className="text-sm text-slate-400">Analyze threat trends and patterns</p>
            <ArrowRight className="h-5 w-5 text-emerald-500 mt-4 group-hover:translate-x-2 transition-transform" />
          </button>
        </div>
      </section>

      {/* System Health */}
      <section className="px-6 pb-16 max-w-7xl mx-auto">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-slate-50 mb-2">System Health</h2>
        </div>

        <div className="bg-slate-900/80 backdrop-blur-sm rounded-xl p-6 border border-emerald-500/20">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {services.map((service) => (
              <div key={service.name} className="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg">
                <div className="flex items-center space-x-3">
                  {service.icon}
                  <div>
                    <p className="text-sm font-medium text-slate-300">{service.name}</p>
                    <p className="text-xs text-slate-500">{service.responseTime}ms</p>
                  </div>
                </div>
                <div className={`h-3 w-3 rounded-full ${
                  service.status === 'healthy' ? 'bg-emerald-500' :
                  service.status === 'degraded' ? 'bg-yellow-500' :
                  'bg-red-500'
                }`} />
              </div>
            ))}
          </div>

          <div className="mt-6 pt-6 border-t border-slate-700">
            <div className="flex items-center justify-between">
              <p className="text-sm text-slate-400">
                <span className="font-semibold text-slate-300">System Status:</span>{' '}
                {services.every(s => s.status === 'healthy') ? 'All systems operational' : 'Some services experiencing issues'}
              </p>
              <p className="text-sm text-slate-500">Last updated: {new Date().toLocaleTimeString()}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 py-8 border-t border-slate-800">
        <div className="max-w-7xl mx-auto text-center text-slate-500 text-sm">
          <p>AEON Digital Twin v1.0 • Neo4j-powered Cybersecurity Intelligence Platform</p>
        </div>
      </footer>
    </div>
  );
}
