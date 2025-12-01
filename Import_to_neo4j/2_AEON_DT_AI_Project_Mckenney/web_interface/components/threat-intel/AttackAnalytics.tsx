'use client';

import { useEffect, useState } from 'react';
import { Target, GitBranch, Network, Skull, Loader2 } from 'lucide-react';

interface MITRETactic {
  tactic: string;
  techniques: number;
  color: string;
}

interface KillChainStage {
  stage: string;
  attacks: number;
  percent: number;
}

interface MalwareFamily {
  name: string;
  instances: number;
  type: string;
  risk: 'critical' | 'high' | 'medium' | 'low';
}


interface IOCStat {
  label: string;
  count: number;
}

interface AnalyticsData {
  mitreTactics: MITRETactic[];
  killChain: KillChainStage[];
  malware: MalwareFamily[];
  iocStats: IOCStat[];
}

export default function AttackAnalytics() {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/threat-intel/analytics');

      if (!response.ok) {
        throw new Error('Failed to fetch analytics data');
      }

      const analyticsData = await response.json();
      setData(analyticsData);
      setError(null);
    } catch (err) {
      console.error('Error fetching analytics:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin" style={{ color: 'var(--primary)' }} />
        <span className="ml-3 text-lg" style={{ color: 'var(--text-secondary)' }}>
          Loading analytics...
        </span>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="text-center py-12">
        <p style={{ color: 'var(--severity-critical)' }}>
          Error loading analytics: {error || 'No data available'}
        </p>
        <button
          onClick={fetchAnalytics}
          className="mt-4 px-4 py-2 rounded"
          style={{ backgroundColor: 'var(--primary)', color: 'white' }}
        >
          Retry
        </button>
      </div>
    );
  }

  const maxTechniques = Math.max(...data.mitreTactics.map(t => t.techniques));

  return (
    <div className="space-y-6">
      {/* MITRE ATT&CK Heatmap */}
      <div>
        <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
          <Target className="inline h-5 w-5 mr-2" style={{ color: 'var(--primary)' }} />
          MITRE ATT&CK Technique Frequency
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {data.mitreTactics.map((tactic, index) => {
            const intensity = tactic.techniques / maxTechniques;
            return (
              <div
                key={index}
                className="p-4 rounded-lg text-center transition-all cursor-pointer"
                style={{
                  backgroundColor: tactic.color,
                  opacity: 0.3 + intensity * 0.7,
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.opacity = '1';
                  e.currentTarget.style.transform = 'scale(1.05)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.opacity = String(0.3 + intensity * 0.7);
                  e.currentTarget.style.transform = 'scale(1)';
                }}
              >
                <div className="text-2xl font-bold text-white mb-1">{tactic.techniques}</div>
                <div className="text-xs font-semibold text-white uppercase">{tactic.tactic}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Kill Chain Progression */}
      <div>
        <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
          <GitBranch className="inline h-5 w-5 mr-2" style={{ color: 'var(--primary)' }} />
          Cyber Kill Chain Analysis
        </h3>
        <div className="space-y-3">
          {data.killChain.map((stage, index) => (
            <div key={index} className="flex items-center space-x-4">
              <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-bold text-white" style={{ backgroundColor: 'var(--primary)' }}>
                {index + 1}
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-semibold" style={{ color: 'var(--text-primary)' }}>
                    {stage.stage}
                  </span>
                  <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                    {stage.attacks} attacks ({stage.percent}%)
                  </span>
                </div>
                <div className="relative h-2 rounded-full" style={{ backgroundColor: 'var(--slate-200)' }}>
                  <div
                    className="absolute top-0 left-0 h-full rounded-full transition-all"
                    style={{
                      width: `${stage.percent * 5}%`,
                      backgroundColor: 'var(--primary)',
                    }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Malware Families */}
      <div>
        <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
          <Skull className="inline h-5 w-5 mr-2" style={{ color: 'var(--primary)' }} />
          Top Malware Families
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.malware.map((malware, index) => (
            <div
              key={index}
              className="p-4 rounded-lg transition-all"
              style={{
                backgroundColor:
                  malware.risk === 'critical' ? 'var(--severity-critical-bg)' : 'var(--severity-high-bg)',
                border:
                  malware.risk === 'critical'
                    ? '2px solid var(--severity-critical)'
                    : '2px solid var(--severity-high)',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateX(5px)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateX(0)';
              }}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <Skull
                    className="h-5 w-5"
                    style={{
                      color: malware.risk === 'critical' ? 'var(--severity-critical)' : 'var(--severity-high)',
                    }}
                  />
                  <span className="font-bold" style={{ color: 'var(--text-primary)' }}>
                    {malware.name}
                  </span>
                </div>
                <span
                  className="px-2 py-1 rounded text-xs font-semibold uppercase"
                  style={{
                    backgroundColor: malware.risk === 'critical' ? 'var(--severity-critical)' : 'var(--severity-high)',
                    color: 'white',
                  }}
                >
                  {malware.risk}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                  {malware.type}
                </span>
                <span className="text-lg font-bold" style={{ color: 'var(--text-primary)' }}>
                  {malware.instances} instances
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* IOC Statistics */}
      <div className="grid grid-cols-4 gap-4">
        {data.iocStats.map((stat, index) => (
          <div
            key={index}
            className="p-4 rounded-lg text-center transition-all"
            style={{ backgroundColor: 'var(--slate-50)', border: '1px solid var(--border-subtle)' }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = 'var(--primary)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = 'var(--border-subtle)';
            }}
          >
            <Network className="h-6 w-6 mx-auto mb-2" style={{ color: 'var(--primary)' }} />
            <p className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>
              {stat.count}
            </p>
            <p className="text-xs mt-1" style={{ color: 'var(--text-tertiary)' }}>
              {stat.label}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
