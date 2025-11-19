'use client';

import { useEffect, useState } from 'react';
import {
  Shield,
  AlertTriangle,
  Bug,
  Activity,
  TrendingUp,
  Database,
  FileText
} from 'lucide-react';
import { Card, Title, AreaChart, DonutChart } from '@tremor/react';
import MetricsCard from '@/components/dashboard/MetricsCard';
import RecentActivity from '@/components/dashboard/RecentActivity';
import SystemHealth from '@/components/dashboard/SystemHealth';
import WorldMap from '@/components/threat-map/WorldMap';

interface DashboardMetrics {
  totalEntities: number;
  activeThreats: number;
  recentCVEs: number;
  systemStatus: string;
}

interface ActivityData {
  date: string;
  threats: number;
  vulnerabilities: number;
  incidents: number;
}

interface ThreatDistribution {
  name: string;
  value: number;
}

export default function Dashboard() {
  const [metrics, setMetrics] = useState<DashboardMetrics>({
    totalEntities: 12256,
    activeThreats: 342,
    recentCVEs: 2847,
    systemStatus: 'healthy',
  });

  const [activityData, setActivityData] = useState<ActivityData[]>([
    { date: 'Nov 01', threats: 45, vulnerabilities: 23, incidents: 12 },
    { date: 'Nov 02', threats: 52, vulnerabilities: 31, incidents: 15 },
    { date: 'Nov 03', threats: 48, vulnerabilities: 28, incidents: 11 },
    { date: 'Nov 04', threats: 61, vulnerabilities: 35, incidents: 18 },
  ]);

  const [threatDistribution, setThreatDistribution] = useState<ThreatDistribution[]>([
    { name: 'Malware', value: 892 },
    { name: 'Threat Actors', value: 156 },
    { name: 'Attack Techniques', value: 421 },
    { name: 'Campaigns', value: 73 },
  ]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Fetch metrics from backend
        const metricsResponse = await fetch('/api/dashboard/metrics');
        if (metricsResponse.ok) {
          const metricsData = await metricsResponse.json();
          setMetrics(metricsData);
        }

        // Fetch activity data
        const activityResponse = await fetch('/api/dashboard/activity');
        if (activityResponse.ok) {
          const activityData = await activityResponse.json();
          setActivityData(activityData);
        }

        // Fetch threat distribution
        const distributionResponse = await fetch('/api/dashboard/distribution');
        if (distributionResponse.ok) {
          const distributionData = await distributionResponse.json();
          setThreatDistribution(distributionData);
        }
      } catch (error) {
        console.log('Using default dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Dashboard Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Activity className="h-8 w-8 text-emerald-500" />
            <h1 className="text-3xl font-bold text-slate-50">
              Operational Dashboard
            </h1>
          </div>
          <p className="text-slate-400">
            Real-time cybersecurity intelligence monitoring and analysis
          </p>
        </div>

        {/* Statistics Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricsCard
            title="Total Entities"
            metric={metrics.totalEntities.toLocaleString()}
            icon={Database}
            iconColor="text-emerald-500"
            delta="+12.5% from last month"
            deltaType="increase"
          />
          <MetricsCard
            title="Active Threats"
            metric={metrics.activeThreats.toLocaleString()}
            icon={Shield}
            iconColor="text-red-500"
            delta="+8.2% from last week"
            deltaType="moderateIncrease"
          />
          <MetricsCard
            title="Recent CVEs"
            metric={metrics.recentCVEs.toLocaleString()}
            icon={Bug}
            iconColor="text-amber-500"
            delta="+15.7% from last month"
            deltaType="increase"
          />
          <MetricsCard
            title="System Status"
            metric={metrics.systemStatus === 'healthy' ? 'Healthy' : 'Degraded'}
            icon={TrendingUp}
            iconColor="text-emerald-500"
            delta="99.9% uptime"
            deltaType="unchanged"
          />
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Activity Timeline */}
          <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm">
            <Title className="text-slate-200 mb-4">Activity Timeline</Title>
            {loading ? (
              <div className="h-80 flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500"></div>
              </div>
            ) : (
              <AreaChart
                className="h-80"
                data={activityData}
                index="date"
                categories={['threats', 'vulnerabilities', 'incidents']}
                colors={['red', 'amber', 'emerald']}
                valueFormatter={(value) => value.toString()}
                showLegend={true}
                showGridLines={true}
                showXAxis={true}
                showYAxis={true}
              />
            )}
          </Card>

          {/* Threat Distribution */}
          <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm">
            <Title className="text-slate-200 mb-4">Threat Distribution</Title>
            {loading ? (
              <div className="h-80 flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500"></div>
              </div>
            ) : (
              <DonutChart
                className="h-80"
                data={threatDistribution}
                category="value"
                index="name"
                colors={['red', 'amber', 'emerald', 'blue']}
                valueFormatter={(value) => value.toLocaleString()}
                showLabel={true}
                showAnimation={true}
              />
            )}
          </Card>
        </div>

        {/* Geographic Threat Map */}
        <div className="mb-8">
          <WorldMap loading={loading} />
        </div>

        {/* Recent Activity & System Health */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <RecentActivity />
          <SystemHealth />
        </div>
      </div>
    </div>
  );
}
