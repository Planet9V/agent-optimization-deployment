import React, { useState } from 'react';
import { Home, TrendingUp, Shield, Search, Network, Settings, ChevronDown } from 'lucide-react';

interface MenuItem {
  label: string;
  href: string;
}

interface MobileMenuProps {
  isOpen: boolean;
  onClose: () => void;
  analyticsItems: MenuItem[];
  threatIntelItems: MenuItem[];
  searchItems: MenuItem[];
}

const MobileMenu: React.FC<MobileMenuProps> = ({
  isOpen,
  onClose,
  analyticsItems,
  threatIntelItems,
  searchItems,
}) => {
  const [expandedSection, setExpandedSection] = useState<string | null>(null);

  if (!isOpen) return null;

  const toggleSection = (section: string) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  const MobileSection = ({
    title,
    icon,
    items,
    sectionKey,
  }: {
    title: string;
    icon: React.ReactNode;
    items: MenuItem[];
    sectionKey: string;
  }) => {
    const isExpanded = expandedSection === sectionKey;

    return (
      <div className="border-b border-slate-800">
        <button
          onClick={() => toggleSection(sectionKey)}
          className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-slate-100 hover:text-emerald-500 hover:bg-slate-900 transition-colors duration-200"
        >
          <div className="flex items-center">
            {icon}
            <span className="ml-3">{title}</span>
          </div>
          <ChevronDown
            className={`w-4 h-4 transition-transform duration-200 ${
              isExpanded ? 'rotate-180' : ''
            }`}
          />
        </button>

        {isExpanded && (
          <div className="bg-slate-900/50 animate-in fade-in-0 slide-in-from-top-2 duration-200">
            {items.map((item, index) => (
              <a
                key={index}
                href={item.href}
                onClick={onClose}
                className="block px-8 py-2 text-sm text-slate-300 hover:text-emerald-500 hover:bg-slate-800 transition-colors duration-150"
              >
                {item.label}
              </a>
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="md:hidden bg-slate-950 border-t border-slate-800 animate-in slide-in-from-top-5 duration-300">
      <div className="px-2 pt-2 pb-3 space-y-1">
        {/* Dashboard */}
        <a
          href="/dashboard"
          onClick={onClose}
          className="flex items-center px-4 py-3 rounded-md text-sm font-medium text-slate-100 hover:text-emerald-500 hover:bg-slate-900 transition-colors duration-200"
        >
          <Home className="w-4 h-4 mr-3" />
          Dashboard
        </a>

        {/* Analytics Section */}
        <MobileSection
          title="Analytics"
          icon={<TrendingUp className="w-4 h-4" />}
          items={analyticsItems}
          sectionKey="analytics"
        />

        {/* Threat Intel Section */}
        <MobileSection
          title="Threat Intel"
          icon={<Shield className="w-4 h-4" />}
          items={threatIntelItems}
          sectionKey="threatIntel"
        />

        {/* Search Section */}
        <MobileSection
          title="Search"
          icon={<Search className="w-4 h-4" />}
          items={searchItems}
          sectionKey="search"
        />

        {/* Graph Explorer */}
        <a
          href="/graph"
          onClick={onClose}
          className="flex items-center px-4 py-3 rounded-md text-sm font-medium text-slate-100 hover:text-emerald-500 hover:bg-slate-900 transition-colors duration-200"
        >
          <Network className="w-4 h-4 mr-3" />
          Graph Explorer
        </a>

        {/* Settings */}
        <a
          href="/settings"
          onClick={onClose}
          className="flex items-center px-4 py-3 rounded-md text-sm font-medium text-slate-100 hover:text-emerald-500 hover:bg-slate-900 transition-colors duration-200"
        >
          <Settings className="w-4 h-4 mr-3" />
          Settings
        </a>
      </div>
    </div>
  );
};

export default MobileMenu;
