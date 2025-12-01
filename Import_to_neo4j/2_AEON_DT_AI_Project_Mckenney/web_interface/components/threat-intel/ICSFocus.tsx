'use client';

import { Factory, AlertTriangle, Shield, Loader2 } from 'lucide-react';
import { useEffect, useState } from 'react';
import SeverityBadge from './SeverityBadge';

interface ICSVulnerability {
  id: string;
  system: string;
  vendor: string;
  cvss: number;
  description: string;
  affected: number;
}

interface Sector {
  name: string;
  threatScore: number;
  assets: number;
  color: string;
}

interface Mitigation {
  title: string;
  priority: string;
  implemented: number;
  description: string;
}

interface ICSData {
  sectors: Sector[];
  vulnerabilities: ICSVulnerability[];
  mitigations: Mitigation[];
}

export default function ICSFocus() {
  const [data, setData] = useState<ICSData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const response = await fetch('/api/threats/ics');
        if (!response.ok) {
          throw new Error('Failed to fetch ICS data');
        }
        const result = await response.json();
        setData(result);
        setError(null);
      } catch (err) {
        console.error('Error fetching ICS data:', err);
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin" style={{ color: 'var(--primary)' }} />
        <span className="ml-3 text-lg" style={{ color: 'var(--text-secondary)' }}>
          Loading ICS threat data...
        </span>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div
        className="p-4 rounded-lg"
        style={{
          backgroundColor: 'var(--error-50)',
          border: '2px solid var(--error-500)'
        }}
      >
        <AlertTriangle className="inline h-5 w-5 mr-2" style={{ color: 'var(--error-500)' }} />
        <span style={{ color: 'var(--error-900)' }}>
          Failed to load ICS data: {error || 'Unknown error'}
        </span>
      </div>
    );
  }
  return (
    <div className="space-y-6">
      {/* Critical Infrastructure Sectors */}
      <div>
        <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
          <Factory className="inline h-5 w-5 mr-2" style={{ color: 'var(--primary)' }} />
          Sector Threat Assessment
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.sectors.map((sector, index) => (
            <div
              key={index}
              className="p-5 rounded-lg transition-all"
              style={{
                backgroundColor: 'var(--surface)',
                border: '2px solid var(--border-default)',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = sector.color;
                e.currentTarget.style.boxShadow = 'var(--shadow-md)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'var(--border-default)';
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-semibold" style={{ color: 'var(--text-primary)' }}>
                  {sector.name}
                </h4>
                <div
                  className="px-3 py-1 rounded-full text-white font-bold text-sm"
                  style={{ backgroundColor: sector.color }}
                >
                  {sector.threatScore}
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span style={{ color: 'var(--text-secondary)' }}>Exposed Assets:</span>
                  <span className="font-semibold" style={{ color: 'var(--text-primary)' }}>
                    {sector.assets}
                  </span>
                </div>
                <div className="relative h-2 rounded-full" style={{ backgroundColor: 'var(--slate-200)' }}>
                  <div
                    className="absolute top-0 left-0 h-full rounded-full transition-all"
                    style={{
                      width: `${sector.threatScore}%`,
                      backgroundColor: sector.color,
                    }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ICS Vulnerabilities */}
      <div>
        <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
          <AlertTriangle className="inline h-5 w-5 mr-2" style={{ color: 'var(--primary)' }} />
          Critical ICS/SCADA Vulnerabilities
        </h3>
        <div className="space-y-3">
          {data.vulnerabilities.map((vuln, index) => (
            <div
              key={index}
              className="p-4 rounded-lg transition-all"
              style={{
                backgroundColor: 'var(--severity-critical-bg)',
                border: '1px solid var(--severity-critical-border)',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateX(5px)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateX(0)';
              }}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className="font-mono font-bold" style={{ color: 'var(--severity-critical)' }}>
                      {vuln.id}
                    </span>
                    <SeverityBadge severity="critical" score={vuln.cvss} size="sm" />
                  </div>
                  <p className="font-semibold mb-1" style={{ color: 'var(--text-primary)' }}>
                    {vuln.system} ({vuln.vendor})
                  </p>
                  <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                    {vuln.description}
                  </p>
                </div>
                <div className="text-right ml-4">
                  <p className="text-2xl font-bold" style={{ color: 'var(--severity-critical)' }}>
                    {vuln.affected}
                  </p>
                  <p className="text-xs" style={{ color: 'var(--text-tertiary)' }}>
                    affected systems
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommended Mitigations */}
      <div>
        <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
          <Shield className="inline h-5 w-5 mr-2" style={{ color: 'var(--primary)' }} />
          Recommended Security Controls
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.mitigations.map((mitigation, index) => (
            <div
              key={index}
              className="p-4 rounded-lg"
              style={{
                backgroundColor: 'var(--slate-50)',
                border: '1px solid var(--border-default)',
              }}
            >
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-semibold" style={{ color: 'var(--text-primary)' }}>
                  {mitigation.title}
                </h4>
                <span
                  className="px-2 py-1 rounded text-xs font-semibold uppercase"
                  style={{
                    backgroundColor:
                      mitigation.priority === 'critical' ? 'var(--severity-critical-bg)' : 'var(--severity-high-bg)',
                    color: mitigation.priority === 'critical' ? 'var(--severity-critical)' : 'var(--severity-high)',
                  }}
                >
                  {mitigation.priority}
                </span>
              </div>
              <p className="text-sm mb-3" style={{ color: 'var(--text-secondary)' }}>
                {mitigation.description}
              </p>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span style={{ color: 'var(--text-tertiary)' }}>Implementation:</span>
                  <span className="font-semibold" style={{ color: 'var(--text-primary)' }}>
                    {mitigation.implemented}%
                  </span>
                </div>
                <div className="relative h-2 rounded-full" style={{ backgroundColor: 'var(--slate-200)' }}>
                  <div
                    className="absolute top-0 left-0 h-full rounded-full transition-all"
                    style={{
                      width: `${mitigation.implemented}%`,
                      backgroundColor:
                        mitigation.implemented >= 70 ? 'var(--success-500)' : mitigation.implemented >= 50 ? 'var(--warning-500)' : 'var(--error-500)',
                    }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Alert Banner */}
      <div
        className="p-4 rounded-lg flex items-start space-x-3"
        style={{
          backgroundColor: 'var(--warning-50)',
          border: '2px solid var(--warning-500)',
        }}
      >
        <AlertTriangle className="h-6 w-6 flex-shrink-0 mt-1" style={{ color: 'var(--warning-500)' }} />
        <div>
          <h4 className="font-semibold mb-1" style={{ color: 'var(--warning-900)' }}>
            ⚠️ Critical Infrastructure Alert
          </h4>
          <p className="text-sm" style={{ color: 'var(--warning-900)' }}>
            Multiple critical vulnerabilities detected in industrial control systems. Immediate patching and network
            segmentation recommended. Coordinate with CISA for incident response support.
          </p>
        </div>
      </div>
    </div>
  );
}
