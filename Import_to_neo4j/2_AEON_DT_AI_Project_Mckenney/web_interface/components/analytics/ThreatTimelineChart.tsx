'use client';

import { useState, useEffect } from 'react';
import { Activity } from 'lucide-react';

interface ThreatTimelineChartProps {
  loading: boolean;
  dateRange: { start: Date; end: Date };
}

interface CampaignDetail {
  name: string;
  firstSeen: string;
  lastSeen: string;
  durationDays: number;
}

interface ThreatActivity {
  month: string;
  threatActor: string;
  campaigns: number;
  campaignDetails: CampaignDetail[];
}

interface TimelineData {
  timeline: ThreatActivity[];
  totalActors: number;
  totalCampaigns: number;
}

export default function ThreatTimelineChart({ loading, dateRange }: ThreatTimelineChartProps) {
  const [data, setData] = useState<TimelineData | null>(null);
  const [fetching, setFetching] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setFetching(true);
      try {
        const params = new URLSearchParams({
          startDate: dateRange.start.toISOString(),
          endDate: dateRange.end.toISOString(),
        });

        const response = await fetch(`/api/analytics/trends/threat-timeline?${params}`);
        const result = await response.json();

        if (result.timeline) {
          setData(result);
        }
      } catch (error) {
        console.error('Error fetching threat timeline:', error);
      } finally {
        setFetching(false);
      }
    };

    fetchData();
  }, [dateRange]);

  if (loading || fetching) {
    return (
      <div className="h-80 flex items-center justify-center">
        <div className="skeleton h-full w-full rounded-lg"></div>
      </div>
    );
  }

  if (!data || data.timeline.length === 0) {
    return (
      <div className="h-80 flex items-center justify-center">
        <p style={{ color: 'var(--text-secondary)' }}>No threat actor activity for selected date range</p>
      </div>
    );
  }

  // Group by month for visualization
  const monthlyData = new Map<string, { actors: Set<string>; total: number }>();
  data.timeline.forEach(activity => {
    if (!monthlyData.has(activity.month)) {
      monthlyData.set(activity.month, { actors: new Set(), total: 0 });
    }
    const monthData = monthlyData.get(activity.month)!;
    monthData.actors.add(activity.threatActor);
    monthData.total += activity.campaigns;
  });

  const months = Array.from(monthlyData.keys()).sort();
  const maxCampaigns = Math.max(...Array.from(monthlyData.values()).map(d => d.total));

  // Get top actors by total campaigns
  const actorCampaigns = new Map<string, number>();
  data.timeline.forEach(activity => {
    actorCampaigns.set(
      activity.threatActor,
      (actorCampaigns.get(activity.threatActor) || 0) + activity.campaigns
    );
  });
  const topActors = Array.from(actorCampaigns.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  const actorColors = [
    'var(--severity-critical)',
    'var(--severity-high)',
    'var(--severity-medium)',
    'var(--severity-info)',
    'var(--primary)',
  ];

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <div className="flex items-center justify-center gap-6 text-sm">
        <div className="flex items-center space-x-2">
          <Activity className="h-4 w-4" style={{ color: 'var(--primary)' }} />
          <span style={{ color: 'var(--text-secondary)' }}>
            {data.totalActors} Active Threat Actors
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <span
            className="px-2 py-1 rounded text-xs font-semibold"
            style={{
              backgroundColor: 'var(--severity-critical-bg)',
              color: 'var(--severity-critical)',
            }}
          >
            {data.totalCampaigns} Campaigns
          </span>
        </div>
      </div>

      {/* Top Actors Legend */}
      <div className="flex items-center justify-center flex-wrap gap-4 text-sm">
        {topActors.map(([actor, campaigns], index) => (
          <div key={actor} className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: actorColors[index] }}></div>
            <span style={{ color: 'var(--text-secondary)' }}>{actor || 'Unknown'}</span>
            <span
              className="px-2 py-0.5 rounded text-xs font-semibold"
              style={{
                backgroundColor: 'var(--slate-100)',
                color: 'var(--text-tertiary)',
              }}
            >
              {campaigns}
            </span>
          </div>
        ))}
      </div>

      {/* Timeline Bar Chart */}
      <div className="h-64 flex items-end justify-around space-x-1">
        {months.map((month, index) => {
          const monthData = monthlyData.get(month)!;
          const heightPercent = (monthData.total / maxCampaigns) * 100;

          return (
            <div key={index} className="flex-1 flex flex-col items-center space-y-2">
              <div
                className="w-full rounded-t cursor-pointer transition-all hover:opacity-80"
                style={{
                  height: `${heightPercent}%`,
                  backgroundColor: 'var(--severity-high)',
                  minHeight: monthData.total > 0 ? '20px' : '0',
                }}
                title={`${month}: ${monthData.total} campaigns from ${monthData.actors.size} actors`}
              >
                {monthData.total > 0 && (
                  <div className="text-center text-xs font-bold text-white pt-1">
                    {monthData.total}
                  </div>
                )}
              </div>
              <span className="text-xs" style={{ color: 'var(--text-tertiary)' }}>
                {month.substring(5)}
              </span>
            </div>
          );
        })}
      </div>

      {/* Activity Table */}
      <div className="mt-6 overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border-default)' }}>
              <th className="text-left py-2 px-4" style={{ color: 'var(--text-secondary)' }}>Month</th>
              <th className="text-left py-2 px-4" style={{ color: 'var(--text-secondary)' }}>Threat Actor</th>
              <th className="text-center py-2 px-4" style={{ color: 'var(--text-secondary)' }}>Campaigns</th>
              <th className="text-left py-2 px-4" style={{ color: 'var(--text-secondary)' }}>Recent Campaign</th>
              <th className="text-right py-2 px-4" style={{ color: 'var(--text-secondary)' }}>Duration (days)</th>
            </tr>
          </thead>
          <tbody>
            {data.timeline.slice(0, 20).map((activity, index) => {
              const recentCampaign = activity.campaignDetails[0];
              return (
                <tr key={index} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                  <td className="py-2 px-4 font-medium" style={{ color: 'var(--text-primary)' }}>
                    {activity.month}
                  </td>
                  <td className="py-2 px-4" style={{ color: 'var(--text-primary)' }}>
                    {activity.threatActor || 'Unknown'}
                  </td>
                  <td className="text-center py-2 px-4">
                    <span
                      className="px-2 py-1 rounded text-xs font-semibold"
                      style={{
                        backgroundColor: activity.campaigns > 2 ? 'var(--severity-critical-bg)' : 'var(--severity-medium-bg)',
                        color: activity.campaigns > 2 ? 'var(--severity-critical)' : 'var(--severity-medium)',
                      }}
                    >
                      {activity.campaigns}
                    </span>
                  </td>
                  <td className="py-2 px-4 text-sm" style={{ color: 'var(--text-secondary)' }}>
                    {recentCampaign?.name || 'N/A'}
                  </td>
                  <td className="text-right py-2 px-4 font-medium" style={{ color: 'var(--text-secondary)' }}>
                    {recentCampaign?.durationDays || 0}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
