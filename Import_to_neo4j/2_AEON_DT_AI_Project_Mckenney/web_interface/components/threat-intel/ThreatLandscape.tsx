'use client';

import { useState, useEffect } from 'react';
import { MapPin, TrendingUp, Target } from 'lucide-react';

interface ThreatActor {
  name: string;
  location: string;
  campaigns: number;
  status: 'active' | 'monitoring' | 'dormant';
}

interface Industry {
  name: string;
  attacks: number;
  percent: number;
}

interface Campaign {
  name: string;
  actor: string;
  started: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
}

interface LandscapeData {
  threatActors: ThreatActor[];
  industries: Industry[];
  campaigns: Campaign[];
}

export default function ThreatLandscape() {
  const [data, setData] = useState<LandscapeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch('/api/threat-intel/landscape');
        if (!response.ok) {
          throw new Error('Failed to fetch threat landscape data');
        }
        const result = await response.json();
        setData(result);
      } catch (err) {
        console.error('Error fetching threat landscape data:', err);
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="h-96 skeleton rounded-lg"></div>
          <div className="h-96 skeleton rounded-lg"></div>
        </div>
        <div className="h-64 skeleton rounded-lg"></div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="p-6 rounded-lg" style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border-default)' }}>
        <p style={{ color: 'var(--text-secondary)' }}>
          {error || 'No threat landscape data available'}
        </p>
      </div>
    );
  }

  const { threatActors, industries, campaigns } = data;
  return (
    <div className="space-y-6">
      {/* Geographic Distribution */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Threat Actor Locations */}
        <div>
          <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
            <MapPin className="inline h-5 w-5 mr-2" style={{ color: 'var(--primary)' }} />
            Active Threat Actors by Location
          </h3>
          <div className="space-y-3">
            {threatActors.slice(0, 4).map((actor, index) => (
              <div
                key={index}
                className="p-4 rounded-lg transition-all"
                style={{
                  backgroundColor: 'var(--slate-50)',
                  border: '1px solid var(--border-subtle)',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = 'var(--primary)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = 'var(--border-subtle)';
                }}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div
                      className="w-2 h-2 rounded-full"
                      style={{
                        backgroundColor:
                          actor.status === 'active' ? 'var(--severity-critical)' : 'var(--severity-medium)',
                      }}
                    ></div>
                    <div>
                      <p className="font-semibold" style={{ color: 'var(--text-primary)' }}>
                        {actor.name}
                      </p>
                      <p className="text-sm" style={{ color: 'var(--text-tertiary)' }}>
                        {actor.location}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold" style={{ color: 'var(--text-primary)' }}>
                      {actor.campaigns}
                    </p>
                    <p className="text-xs" style={{ color: 'var(--text-tertiary)' }}>
                      campaigns
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Targeted Industries */}
        <div>
          <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
            <Target className="inline h-5 w-5 mr-2" style={{ color: 'var(--primary)' }} />
            Top Targeted Industries
          </h3>
          <div className="space-y-3">
            {industries.slice(0, 5).map((industry, index) => (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-medium" style={{ color: 'var(--text-primary)' }}>
                    {industry.name}
                  </span>
                  <span className="font-semibold" style={{ color: 'var(--text-secondary)' }}>
                    {industry.attacks} attacks
                  </span>
                </div>
                <div className="relative h-3 rounded-full" style={{ backgroundColor: 'var(--slate-200)' }}>
                  <div
                    className="absolute top-0 left-0 h-full rounded-full transition-all"
                    style={{
                      width: `${industry.percent}%`,
                      backgroundColor:
                        industry.percent >= 25
                          ? 'var(--severity-critical)'
                          : industry.percent >= 15
                          ? 'var(--severity-high)'
                          : 'var(--severity-medium)',
                    }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Campaigns Timeline */}
      <div>
        <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
          <TrendingUp className="inline h-5 w-5 mr-2" style={{ color: 'var(--primary)' }} />
          Recent Campaigns
        </h3>
        <div className="space-y-3">
          {campaigns.slice(0, 4).map((campaign, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-4 rounded-lg transition-all"
              style={{
                backgroundColor: 'var(--surface)',
                border: '1px solid var(--border-default)',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.boxShadow = 'var(--shadow-md)';
                e.currentTarget.style.borderColor = 'var(--primary)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.boxShadow = 'none';
                e.currentTarget.style.borderColor = 'var(--border-default)';
              }}
            >
              <div className="flex items-center space-x-4">
                <div
                  className="w-1 h-12 rounded"
                  style={{
                    backgroundColor:
                      campaign.severity === 'critical'
                        ? 'var(--severity-critical)'
                        : campaign.severity === 'high'
                        ? 'var(--severity-high)'
                        : 'var(--severity-medium)',
                  }}
                ></div>
                <div>
                  <p className="font-semibold" style={{ color: 'var(--text-primary)' }}>
                    {campaign.name}
                  </p>
                  <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                    {campaign.actor} • Started {campaign.started}
                  </p>
                </div>
              </div>
              <div>
                <span
                  className="px-3 py-1 rounded-md text-xs font-semibold uppercase"
                  style={{
                    backgroundColor:
                      campaign.severity === 'critical'
                        ? 'var(--severity-critical-bg)'
                        : campaign.severity === 'high'
                        ? 'var(--severity-high-bg)'
                        : 'var(--severity-medium-bg)',
                    color:
                      campaign.severity === 'critical'
                        ? 'var(--severity-critical)'
                        : campaign.severity === 'high'
                        ? 'var(--severity-high)'
                        : 'var(--severity-medium)',
                  }}
                >
                  {campaign.severity}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
