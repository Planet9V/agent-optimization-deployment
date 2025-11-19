'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { ChevronRight, Home } from 'lucide-react';

interface BreadcrumbItem {
  label: string;
  href: string;
}

const routeLabels: Record<string, string> = {
  '': 'Home',
  'threat-intel': 'Threat Intelligence',
  'analysis': 'Analysis',
  'threats': 'Threats',
  'arsenal': 'Arsenal',
  'observations': 'Observations',
  'data': 'Data',
  'weaknesses': 'Weaknesses (CWEs)',
  'search': 'Search',
  'analytics': 'Analytics',
  'trends': 'Trends',
  'graph': 'Graph Visualization',
  'chat': 'AI Chat',
  'upload': 'Upload Documents',
  'customers': 'Customers',
  'tags': 'Tags',
  'settings': 'Settings',
  'observability': 'Observability',
  'help': 'Help & Support',
  'docs': 'Documentation',
};

export default function Breadcrumb() {
  const pathname = usePathname();

  const generateBreadcrumbs = (): BreadcrumbItem[] => {
    // Home is always the first breadcrumb
    if (pathname === '/') {
      return [{ label: 'Home', href: '/' }];
    }

    const segments = pathname.split('/').filter(Boolean);
    const breadcrumbs: BreadcrumbItem[] = [{ label: 'Home', href: '/' }];

    let currentPath = '';
    segments.forEach((segment) => {
      currentPath += `/${segment}`;
      const label = routeLabels[segment] || segment.charAt(0).toUpperCase() + segment.slice(1);
      breadcrumbs.push({ label, href: currentPath });
    });

    return breadcrumbs;
  };

  const breadcrumbs = generateBreadcrumbs();

  if (breadcrumbs.length <= 1) {
    return null; // Don't show breadcrumb on home page
  }

  return (
    <nav
      className="flex items-center space-x-2 px-6 py-3 text-sm"
      style={{
        backgroundColor: 'var(--background)',
        borderBottom: '1px solid var(--border-subtle)',
      }}
      aria-label="Breadcrumb"
    >
      {breadcrumbs.map((item, index) => {
        const isLast = index === breadcrumbs.length - 1;
        const isFirst = index === 0;

        return (
          <div key={item.href} className="flex items-center space-x-2">
            {isFirst ? (
              <Link
                href={item.href}
                className="flex items-center hover:underline transition-colors"
                style={{ color: 'var(--text-secondary)' }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.color = 'var(--primary)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.color = 'var(--text-secondary)';
                }}
              >
                <Home className="h-4 w-4" />
              </Link>
            ) : (
              <>
                <ChevronRight className="h-4 w-4" style={{ color: 'var(--text-tertiary)' }} />
                {isLast ? (
                  <span className="font-medium" style={{ color: 'var(--text-primary)' }}>
                    {item.label}
                  </span>
                ) : (
                  <Link
                    href={item.href}
                    className="hover:underline transition-colors"
                    style={{ color: 'var(--text-secondary)' }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.color = 'var(--primary)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.color = 'var(--text-secondary)';
                    }}
                  >
                    {item.label}
                  </Link>
                )}
              </>
            )}
          </div>
        );
      })}
    </nav>
  );
}
