'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import {
  Database,
  FileText,
  Shield,
  AlertTriangle,
  Bug,
  Target,
  Activity,
  BarChart3,
  ArrowRight,
  GitBranch,
  Zap,
  TrendingUp,
} from 'lucide-react';

interface DashboardStats {
  totalDocuments: number;
  totalEntities: number;
  totalRelationships: number;
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
}

export default function Home() {
  const [stats, setStats] = useState<DashboardStats>({
    totalDocuments: 115,
    totalEntities: 12256,
    totalRelationships: 14645,
  });

  const [cyberStats, setCyberStats] = useState<CyberStats>({
    cves: {
      total: 2847,
      critical: 342,
      high: 891,
      medium: 1205,
      low: 409,
    },
    threatActors: 156,
    malware: 892,
    campaigns: 73,
    attackTechniques: 421,
  });

  useEffect(() => {
    // Fetch real stats from API
    const fetchStats = async () => {
      try {
        const response = await fetch('/api/stats');
        if (response.ok) {
          const data = await response.json();
          setStats(data);
        }
      } catch (error) {
        console.log('Using default stats');
      }
    };
    fetchStats();
  }, []);

  return (
    <div className="max-w-7xl mx-auto py-8">
      {/* Hero Section */}
      <div className="text-center py-16 mb-16 fade-in">
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-500/10 border border-emerald-500/30 rounded-full mb-6">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="text-sm text-emerald-400 font-semibold">Live Intelligence Feed</span>
        </div>
        <h1 className="text-5xl md:text-7xl font-bold text-slate-50 mb-6 tracking-tight">
          AEON Digital Twin
        </h1>
        <p className="text-xl md:text-2xl text-slate-400 max-w-3xl mx-auto mb-10">
          Advanced cybersecurity intelligence platform powered by Neo4j knowledge graphs
        </p>
        <div className="flex items-center justify-center gap-4 flex-wrap">
          <Link href="/dashboard" className="modern-button flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Explore Dashboard
          </Link>
          <Link href="/ai" className="modern-button-secondary flex items-center gap-2">
            <Zap className="h-5 w-5" />
            AI Assistant
          </Link>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
        <div className="modern-card group">
          <div className="flex items-center gap-4">
            <div className="p-4 bg-blue-500/20 rounded-xl group-hover:scale-110 transition-transform duration-300">
              <FileText className="h-8 w-8 text-blue-400" />
            </div>
            <div>
              <p className="text-3xl font-bold text-slate-50">{stats.totalDocuments.toLocaleString()}</p>
              <p className="text-sm text-slate-400">Documents Analyzed</p>
            </div>
          </div>
        </div>

        <div className="modern-card group">
          <div className="flex items-center gap-4">
            <div className="p-4 bg-emerald-500/20 rounded-xl group-hover:scale-110 transition-transform duration-300">
              <Database className="h-8 w-8 text-emerald-400" />
            </div>
            <div>
              <p className="text-3xl font-bold text-slate-50">{stats.totalEntities.toLocaleString()}</p>
              <p className="text-sm text-slate-400">Threat Entities</p>
            </div>
          </div>
        </div>

        <div className="modern-card group">
          <div className="flex items-center gap-4">
            <div className="p-4 bg-purple-500/20 rounded-xl group-hover:scale-110 transition-transform duration-300">
              <GitBranch className="h-8 w-8 text-purple-400" />
            </div>
            <div>
              <p className="text-3xl font-bold text-slate-50">{stats.totalRelationships.toLocaleString()}</p>
              <p className="text-sm text-slate-400">Relationships Mapped</p>
            </div>
          </div>
        </div>
      </div>

      {/* Cybersecurity Intelligence */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold text-slate-50 mb-8 flex items-center gap-3">
          <Shield className="h-8 w-8 text-emerald-500" />
          Cybersecurity Intelligence
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* CVE Card */}
          <Link href="/entities?type=CVE">
            <div className="modern-card group cursor-pointer h-full">
              <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-red-500/20 rounded-xl">
                  <Bug className="h-6 w-6 text-red-400" />
                </div>
                <ArrowRight className="h-5 w-5 text-slate-600 group-hover:text-emerald-400 transition-colors" />
              </div>
              <p className="text-4xl font-bold text-slate-50 mb-2">{cyberStats.cves.total.toLocaleString()}</p>
              <p className="text-slate-400 mb-4">CVE Vulnerabilities</p>
              <div className="flex flex-wrap gap-2">
                <span className="badge-critical">{cyberStats.cves.critical} Critical</span>
                <span className="badge-high">{cyberStats.cves.high} High</span>
              </div>
            </div>
          </Link>

          {/* Threat Actors */}
          <Link href="/entities?type=ThreatActor">
            <div className="modern-card group cursor-pointer h-full">
              <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-orange-500/20 rounded-xl">
                  <Target className="h-6 w-6 text-orange-400" />
                </div>
                <ArrowRight className="h-5 w-5 text-slate-600 group-hover:text-emerald-400 transition-colors" />
              </div>
              <p className="text-4xl font-bold text-slate-50 mb-2">{cyberStats.threatActors}</p>
              <p className="text-slate-400 mb-4">Threat Actors</p>
              <div className="flex items-center gap-2 text-red-400 text-sm">
                <TrendingUp className="h-4 w-4" />
                <span>Active monitoring</span>
              </div>
            </div>
          </Link>

          {/* Malware Families */}
          <Link href="/entities?type=Malware">
            <div className="modern-card group cursor-pointer h-full">
              <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-purple-500/20 rounded-xl">
                  <AlertTriangle className="h-6 w-6 text-purple-400" />
                </div>
                <ArrowRight className="h-5 w-5 text-slate-600 group-hover:text-emerald-400 transition-colors" />
              </div>
              <p className="text-4xl font-bold text-slate-50 mb-2">{cyberStats.malware}</p>
              <p className="text-slate-400 mb-4">Malware Families</p>
              <div className="badge-high">High Priority</div>
            </div>
          </Link>

          {/* Campaigns */}
          <Link href="/entities?type=Campaign">
            <div className="modern-card group cursor-pointer h-full">
              <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-yellow-500/20 rounded-xl">
                  <Activity className="h-6 w-6 text-yellow-400" />
                </div>
                <ArrowRight className="h-5 w-5 text-slate-600 group-hover:text-emerald-400 transition-colors" />
              </div>
              <p className="text-4xl font-bold text-slate-50 mb-2">{cyberStats.campaigns}</p>
              <p className="text-slate-400 mb-4">Active Campaigns</p>
              <div className="badge-medium">Tracking</div>
            </div>
          </Link>

          {/* Attack Techniques */}
          <Link href="/entities?type=AttackTechnique">
            <div className="modern-card group cursor-pointer h-full">
              <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-emerald-500/20 rounded-xl">
                  <Zap className="h-6 w-6 text-emerald-400" />
                </div>
                <ArrowRight className="h-5 w-5 text-slate-600 group-hover:text-emerald-400 transition-colors" />
              </div>
              <p className="text-4xl font-bold text-slate-50 mb-2">{cyberStats.attackTechniques}</p>
              <p className="text-slate-400 mb-4">MITRE ATT&CK Techniques</p>
              <div className="badge-low">Cataloged</div>
            </div>
          </Link>

          {/* Quick Actions Card */}
          <div className="modern-card bg-gradient-to-br from-emerald-500/20 to-blue-500/20 border-emerald-500/40">
            <h3 className="text-xl font-bold text-slate-50 mb-4 flex items-center gap-2">
              <Zap className="h-5 w-5 text-emerald-400" />
              Quick Actions
            </h3>
            <div className="space-y-3">
              <Link
                href="/search"
                className="flex items-center justify-between p-3 bg-slate-900/50 rounded-lg hover:bg-emerald-500/10 transition-colors"
              >
                <span className="text-slate-300">Search Intelligence</span>
                <ArrowRight className="h-4 w-4 text-emerald-400" />
              </Link>
              <Link
                href="/graph"
                className="flex items-center justify-between p-3 bg-slate-900/50 rounded-lg hover:bg-emerald-500/10 transition-colors"
              >
                <span className="text-slate-300">Explore Graph</span>
                <ArrowRight className="h-4 w-4 text-emerald-400" />
              </Link>
              <Link
                href="/ai"
                className="flex items-center justify-between p-3 bg-slate-900/50 rounded-lg hover:bg-emerald-500/10 transition-colors"
              >
                <span className="text-slate-300">Ask AI</span>
                <ArrowRight className="h-4 w-4 text-emerald-400" />
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Connection Status */}
      <div className="modern-card border-emerald-500/30">
        <div className="flex items-center gap-3 mb-4">
          <Database className="h-6 w-6 text-emerald-400" />
          <h3 className="text-xl font-bold text-slate-50">System Health</h3>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="text-slate-300 text-sm">Neo4j</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="text-slate-300 text-sm">Qdrant</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="text-slate-300 text-sm">MySQL</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="text-slate-300 text-sm">MinIO</span>
          </div>
        </div>
      </div>
    </div>
  );
}
