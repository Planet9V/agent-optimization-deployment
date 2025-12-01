'use client';

import { Shield, Globe, AlertTriangle, Target, Activity, Database } from 'lucide-react';
import ThreatLandscape from '@/components/threat-intel/ThreatLandscape';
import VulnerabilityIntel from '@/components/threat-intel/VulnerabilityIntel';
import AttackAnalytics from '@/components/threat-intel/AttackAnalytics';
import ICSFocus from '@/components/threat-intel/ICSFocus';
import SeverityBadge from '@/components/threat-intel/SeverityBadge';

export default function ThreatIntelPage() {
  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center space-x-3">
            <div
              className="p-2 rounded-lg"
              style={{ backgroundColor: 'var(--severity-critical-bg)' }}
            >
              <Shield className="h-8 w-8" style={{ color: 'var(--severity-critical)' }} />
            </div>
            <div>
              <h1 className="text-3xl font-bold" style={{ color: 'var(--text-primary)' }}>
                Threat Intelligence Dashboard
              </h1>
              <p className="mt-1 text-sm" style={{ color: 'var(--text-secondary)' }}>
                Comprehensive cybersecurity threat landscape overview
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <div className="text-right">
            <p className="text-xs" style={{ color: 'var(--text-tertiary)' }}>Last Updated</p>
            <p className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
              {new Date().toLocaleString()}
            </p>
          </div>
          <button
            className="px-4 py-2 rounded-md font-medium text-sm transition-all"
            style={{
              backgroundColor: 'var(--primary)',
              color: 'white',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'var(--primary-hover)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'var(--primary)';
            }}
          >
            Refresh Data
          </button>
        </div>
      </div>

      {/* Threat Level Indicator */}
      <div className="card-modern p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div
              className="p-4 rounded-full"
              style={{ backgroundColor: 'var(--severity-high-bg)' }}
            >
              <AlertTriangle className="h-10 w-10" style={{ color: 'var(--severity-high)' }} />
            </div>
            <div>
              <p className="text-sm font-medium" style={{ color: 'var(--text-secondary)' }}>
                Current Threat Level
              </p>
              <p className="text-3xl font-bold mt-1" style={{ color: 'var(--severity-high)' }}>
                ELEVATED
              </p>
              <p className="text-sm mt-1" style={{ color: 'var(--text-tertiary)' }}>
                Based on 247 active threat actors and 89 ongoing campaigns
              </p>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <SeverityBadge severity="critical" size="lg" />
              <p className="text-2xl font-bold mt-2" style={{ color: 'var(--text-primary)' }}>
                15
              </p>
              <p className="text-xs" style={{ color: 'var(--text-tertiary)' }}>Active</p>
            </div>
            <div className="text-center">
              <SeverityBadge severity="high" size="lg" />
              <p className="text-2xl font-bold mt-2" style={{ color: 'var(--text-primary)' }}>
                42
              </p>
              <p className="text-xs" style={{ color: 'var(--text-tertiary)' }}>Active</p>
            </div>
            <div className="text-center">
              <SeverityBadge severity="medium" size="lg" />
              <p className="text-2xl font-bold mt-2" style={{ color: 'var(--text-primary)' }}>
                32
              </p>
              <p className="text-xs" style={{ color: 'var(--text-tertiary)' }}>Active</p>
            </div>
          </div>
        </div>
      </div>

      {/* Section 1: Threat Landscape Overview */}
      <div className="card-modern p-6">
        <div className="flex items-center space-x-2 mb-6">
          <Globe className="h-6 w-6" style={{ color: 'var(--primary)' }} />
          <h2 className="text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>
            Threat Landscape Overview
          </h2>
        </div>
        <ThreatLandscape />
      </div>

      {/* Section 2: Vulnerability Intelligence */}
      <div className="card-modern p-6">
        <div className="flex items-center space-x-2 mb-6">
          <Database className="h-6 w-6" style={{ color: 'var(--primary)' }} />
          <h2 className="text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>
            Vulnerability Intelligence
          </h2>
        </div>
        <VulnerabilityIntel />
      </div>

      {/* Section 3: Attack Analytics */}
      <div className="card-modern p-6">
        <div className="flex items-center space-x-2 mb-6">
          <Target className="h-6 w-6" style={{ color: 'var(--primary)' }} />
          <h2 className="text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>
            Attack Analytics
          </h2>
        </div>
        <AttackAnalytics />
      </div>

      {/* Section 4: ICS/SCADA Focus */}
      <div className="card-modern p-6">
        <div className="flex items-center space-x-2 mb-6">
          <Activity className="h-6 w-6" style={{ color: 'var(--primary)' }} />
          <h2 className="text-2xl font-semibold" style={{ color: 'var(--text-primary)' }}>
            ICS/SCADA Critical Infrastructure
          </h2>
        </div>
        <ICSFocus />
      </div>
    </div>
  );
}
