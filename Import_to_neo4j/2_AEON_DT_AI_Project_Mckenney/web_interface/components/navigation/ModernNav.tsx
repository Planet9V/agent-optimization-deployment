import React, { useState } from 'react';
import { Home, TrendingUp, Shield, Search, Network, Settings, Menu, X } from 'lucide-react';
import NavDropdown from './NavDropdown';
import MobileMenu from './MobileMenu';

const ModernNav: React.FC = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const analyticsItems = [
    { label: 'Trends', href: '/analytics/trends' },
    { label: 'Metrics', href: '/analytics/metrics' },
    { label: 'Reports', href: '/analytics/reports' },
  ];

  const threatIntelItems = [
    { label: 'Vulnerabilities', href: '/threat-intel/vulnerabilities' },
    { label: 'Threat Actors', href: '/threat-intel/actors' },
    { label: 'Campaigns', href: '/threat-intel/campaigns' },
  ];

  const searchItems = [
    { label: 'Full-text Search', href: '/search/fulltext' },
    { label: 'Semantic Search', href: '/search/semantic' },
    { label: 'Hybrid Search', href: '/search/hybrid' },
  ];

  return (
    <nav className="bg-slate-950 border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo/Brand */}
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <h1 className="text-xl font-bold text-slate-50">
                <span className="text-emerald-500">AEON</span> DT
              </h1>
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-center space-x-1">
              {/* Dashboard */}
              <a
                href="/dashboard"
                className="group flex items-center px-3 py-2 rounded-md text-sm font-medium text-slate-100 hover:text-emerald-500 hover:bg-slate-900 transition-all duration-200"
              >
                <Home className="w-4 h-4 mr-2" />
                Dashboard
              </a>

              {/* Analytics Dropdown */}
              <NavDropdown
                label="Analytics"
                icon={<TrendingUp className="w-4 h-4" />}
                items={analyticsItems}
              />

              {/* Threat Intel Dropdown */}
              <NavDropdown
                label="Threat Intel"
                icon={<Shield className="w-4 h-4" />}
                items={threatIntelItems}
              />

              {/* Search Dropdown */}
              <NavDropdown
                label="Search"
                icon={<Search className="w-4 h-4" />}
                items={searchItems}
              />

              {/* Graph Explorer */}
              <a
                href="/graph"
                className="group flex items-center px-3 py-2 rounded-md text-sm font-medium text-slate-100 hover:text-emerald-500 hover:bg-slate-900 transition-all duration-200"
              >
                <Network className="w-4 h-4 mr-2" />
                Graph Explorer
              </a>

              {/* Settings */}
              <a
                href="/settings"
                className="group flex items-center px-3 py-2 rounded-md text-sm font-medium text-slate-100 hover:text-emerald-500 hover:bg-slate-900 transition-all duration-200"
              >
                <Settings className="w-4 h-4 mr-2" />
                Settings
              </a>
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-slate-100 hover:text-emerald-500 hover:bg-slate-900 transition-colors duration-200"
              aria-expanded={mobileMenuOpen}
            >
              <span className="sr-only">Open main menu</span>
              {mobileMenuOpen ? (
                <X className="block h-6 w-6" aria-hidden="true" />
              ) : (
                <Menu className="block h-6 w-6" aria-hidden="true" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <MobileMenu
        isOpen={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
        analyticsItems={analyticsItems}
        threatIntelItems={threatIntelItems}
        searchItems={searchItems}
      />
    </nav>
  );
};

export default ModernNav;
