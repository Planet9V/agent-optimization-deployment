'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Home,
  Upload,
  Search,
  MessageSquare,
  Tag,
  Network,
  BarChart3,
  Activity,
  Settings,
  ChevronLeft,
  ChevronRight,
  HelpCircle,
  FileText,
  Users,
  Shield,
  AlertTriangle,
  Target,
  Eye,
  Database,
  TrendingUp,
  Globe,
  Skull,
  Crosshair,
  Layers,
  BookOpen,
  FileBarChart,
  LineChart
} from 'lucide-react';

interface SidebarItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
  children?: SidebarItem[];
  description?: string;
}

const sidebarItems: SidebarItem[] = [
  {
    name: 'Dashboard',
    href: '/',
    icon: Home,
    description: 'Overview & Metrics',
    children: [
      { name: 'Home', href: '/', icon: Home, description: 'Main dashboard' },
      { name: 'Threat Intelligence', href: '/threat-intel', icon: Shield, description: 'Threat landscape overview', badge: 'NEW' },
    ]
  },
  {
    name: 'Analysis',
    href: '/analysis',
    icon: Target,
    description: 'Threat Analysis',
    children: [
      { name: 'Threats', href: '/analysis/threats', icon: AlertTriangle, description: 'Threat actors & campaigns' },
      { name: 'Arsenal', href: '/analysis/arsenal', icon: Skull, description: 'Malware & attack patterns' },
      { name: 'Observations', href: '/analysis/observations', icon: Eye, description: 'IOCs & observables' },
    ]
  },
  {
    name: 'Data',
    href: '/data',
    icon: Database,
    description: 'Knowledge Base',
    children: [
      { name: 'Vulnerabilities (CVEs)', href: '/graph', icon: Shield, description: 'CVE database' },
      { name: 'Weaknesses (CWEs)', href: '/data/weaknesses', icon: AlertTriangle, description: 'CWE catalog' },
      { name: 'Entities', href: '/search', icon: Layers, description: 'All entities' },
      { name: 'Relationships', href: '/graph', icon: Network, description: 'Graph relationships' },
    ]
  },
  {
    name: 'Search',
    href: '/search',
    icon: Search,
    description: 'Search & Discovery',
    children: [
      { name: 'Global Search', href: '/search', icon: Globe, description: 'Search all data' },
      { name: 'Advanced Filters', href: '/search', icon: Crosshair, description: 'Filter & refine' },
    ]
  },
  {
    name: 'Analytics',
    href: '/analytics',
    icon: TrendingUp,
    description: 'Insights & Trends',
    children: [
      { name: 'Trends', href: '/analytics/trends', icon: LineChart, description: 'Time-series analysis', badge: 'NEW' },
      { name: 'Statistics', href: '/analytics', icon: BarChart3, description: 'Statistical insights' },
      { name: 'Reports', href: '/observability', icon: FileBarChart, description: 'System monitoring' },
    ]
  },
  {
    name: 'Settings',
    href: '/settings',
    icon: Settings,
    description: 'Configuration',
    children: [
      { name: 'Profile', href: '/settings', icon: Users, description: 'User settings' },
      { name: 'Customers', href: '/customers', icon: Users, description: 'Customer management' },
      { name: 'Tags', href: '/tags', icon: Tag, description: 'Tag organization' },
      { name: 'Documents', href: '/upload', icon: Upload, description: 'Document upload' },
      { name: 'AI Chat', href: '/chat', icon: MessageSquare, description: 'AI assistant', badge: 'AI' },
    ]
  },
];

export default function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [expandedItems, setExpandedItems] = useState<string[]>([]);
  const pathname = usePathname();

  const toggleSidebar = () => setIsCollapsed(!isCollapsed);

  const toggleExpanded = (itemName: string) => {
    setExpandedItems(prev =>
      prev.includes(itemName)
        ? prev.filter(name => name !== itemName)
        : [...prev, itemName]
    );
  };

  const isActive = (href: string) => {
    if (href === '/') {
      return pathname === '/';
    }
    return pathname?.startsWith(href);
  };

  return (
    <aside
      className={`fixed left-0 top-16 h-[calc(100vh-4rem)] transition-all duration-300 z-40 ${
        isCollapsed ? 'w-16' : 'w-72'
      }`}
      style={{
        backgroundColor: 'var(--surface)',
        borderRight: '1px solid var(--border-default)',
      }}
    >
      {/* Sidebar Header */}
      <div className="flex items-center justify-between p-4" style={{ borderBottom: '1px solid var(--border-subtle)' }}>
        {!isCollapsed && (
          <h2 className="text-base font-semibold" style={{ color: 'var(--text-primary)' }}>Navigation</h2>
        )}
        <button
          onClick={toggleSidebar}
          className="p-1.5 rounded-md transition-colors"
          style={{
            color: 'var(--text-secondary)',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = 'var(--slate-100)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'transparent';
          }}
          title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {isCollapsed ? (
            <ChevronRight className="h-5 w-5" />
          ) : (
            <ChevronLeft className="h-5 w-5" />
          )}
        </button>
      </div>

      {/* Navigation Items */}
      <nav className="flex-1 overflow-y-auto p-3">
        <ul className="space-y-1">
          {sidebarItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.href);
            const hasChildren = item.children && item.children.length > 0;
            const isExpanded = expandedItems.includes(item.name);

            return (
              <li key={item.name}>
                <div className="relative">
                  <Link
                    href={item.href}
                    className={`flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-all ${
                      active
                        ? ''
                        : ''
                    }`}
                    style={{
                      backgroundColor: active ? 'var(--primary)' : 'transparent',
                      color: active ? 'white' : 'var(--text-secondary)',
                    }}
                    onMouseEnter={(e) => {
                      if (!active) {
                        e.currentTarget.style.backgroundColor = 'var(--slate-100)';
                        e.currentTarget.style.color = 'var(--text-primary)';
                      }
                    }}
                    onMouseLeave={(e) => {
                      if (!active) {
                        e.currentTarget.style.backgroundColor = 'transparent';
                        e.currentTarget.style.color = 'var(--text-secondary)';
                      }
                    }}
                    title={isCollapsed ? item.name : ''}
                  >
                    <Icon className="h-5 w-5 flex-shrink-0" />
                    {!isCollapsed && (
                      <>
                        <div className="flex-1">
                          <div className="text-sm font-medium">{item.name}</div>
                          {item.description && (
                            <div className="text-xs opacity-75 mt-0.5">{item.description}</div>
                          )}
                        </div>
                        {item.badge && (
                          <span
                            className="px-2 py-0.5 text-xs font-semibold rounded-md"
                            style={{
                              backgroundColor: 'var(--emerald-500)',
                              color: 'white',
                            }}
                          >
                            {item.badge}
                          </span>
                        )}
                        {hasChildren && (
                          <button
                            onClick={(e) => {
                              e.preventDefault();
                              toggleExpanded(item.name);
                            }}
                            className="p-0.5 rounded"
                            style={{
                              color: active ? 'white' : 'var(--text-tertiary)',
                            }}
                            onMouseEnter={(e) => {
                              e.currentTarget.style.backgroundColor = 'var(--slate-200)';
                            }}
                            onMouseLeave={(e) => {
                              e.currentTarget.style.backgroundColor = 'transparent';
                            }}
                          >
                            <ChevronRight
                              className={`h-4 w-4 transition-transform ${
                                isExpanded ? 'rotate-90' : ''
                              }`}
                            />
                          </button>
                        )}
                      </>
                    )}
                  </Link>
                </div>

                {/* Children Items */}
                {hasChildren && isExpanded && !isCollapsed && (
                  <ul className="ml-8 mt-1 space-y-0.5">
                    {item.children!.map((child) => {
                      const ChildIcon = child.icon;
                      const childActive = isActive(child.href);
                      return (
                        <li key={child.name}>
                          <Link
                            href={child.href}
                            className="flex items-center space-x-3 px-3 py-2 rounded-lg text-sm transition-all"
                            style={{
                              backgroundColor: childActive ? 'var(--primary)' : 'transparent',
                              color: childActive ? 'white' : 'var(--text-tertiary)',
                            }}
                            onMouseEnter={(e) => {
                              if (!childActive) {
                                e.currentTarget.style.backgroundColor = 'var(--slate-100)';
                                e.currentTarget.style.color = 'var(--text-primary)';
                              }
                            }}
                            onMouseLeave={(e) => {
                              if (!childActive) {
                                e.currentTarget.style.backgroundColor = 'transparent';
                                e.currentTarget.style.color = 'var(--text-tertiary)';
                              }
                            }}
                          >
                            <ChildIcon className="h-4 w-4 flex-shrink-0" />
                            <div className="flex-1">
                              <div className="font-medium">{child.name}</div>
                              {child.description && (
                                <div className="text-xs opacity-75 mt-0.5">{child.description}</div>
                              )}
                            </div>
                            {child.badge && (
                              <span
                                className="px-1.5 py-0.5 text-xs font-semibold rounded"
                                style={{
                                  backgroundColor: 'var(--emerald-500)',
                                  color: 'white',
                                }}
                              >
                                {child.badge}
                              </span>
                            )}
                          </Link>
                        </li>
                      );
                    })}
                  </ul>
                )}
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Sidebar Footer */}
      {!isCollapsed && (
        <div className="p-4" style={{ borderTop: '1px solid var(--border-subtle)' }}>
          <div className="space-y-1">
            <Link
              href="/help"
              className="flex items-center space-x-3 px-3 py-2 rounded-lg transition-all text-sm"
              style={{ color: 'var(--text-tertiary)' }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'var(--slate-100)';
                e.currentTarget.style.color = 'var(--text-primary)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'transparent';
                e.currentTarget.style.color = 'var(--text-tertiary)';
              }}
            >
              <HelpCircle className="h-4 w-4" />
              <span>Help & Support</span>
            </Link>
            <Link
              href="/docs"
              className="flex items-center space-x-3 px-3 py-2 rounded-lg transition-all text-sm"
              style={{ color: 'var(--text-tertiary)' }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'var(--slate-100)';
                e.currentTarget.style.color = 'var(--text-primary)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'transparent';
                e.currentTarget.style.color = 'var(--text-tertiary)';
              }}
            >
              <FileText className="h-4 w-4" />
              <span>Documentation</span>
            </Link>
          </div>
        </div>
      )}
    </aside>
  );
}
