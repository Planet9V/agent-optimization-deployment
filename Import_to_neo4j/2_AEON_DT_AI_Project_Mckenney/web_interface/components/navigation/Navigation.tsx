'use client';

import { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronDown, Menu, X } from 'lucide-react';

interface SubMenuItem {
  label: string;
  href: string;
  description: string;
}

interface MenuItem {
  label: string;
  href?: string;
  items?: SubMenuItem[];
}

const menuItems: MenuItem[] = [
  {
    label: 'Dashboard',
    items: [
      { label: 'Home', href: '/', description: 'Main dashboard overview and system status' },
      { label: 'Analytics', href: '/analytics', description: 'Data analytics and insights' },
      { label: 'Observability', href: '/observability', description: 'Real-time system monitoring' }
    ]
  },
  {
    label: 'Data Management',
    items: [
      { label: 'Upload Documents', href: '/upload', description: 'Import and process files with AI pipeline' },
      { label: 'Customers', href: '/customers', description: 'Customer and organization management' },
      { label: 'Tags', href: '/tags', description: 'Tag organization and categorization' }
    ]
  },
  {
    label: 'Knowledge',
    items: [
      { label: 'Graph Visualization', href: '/graph', description: 'Neo4j knowledge graph explorer' },
      { label: 'AI Chat', href: '/chat', description: 'AI-powered assistant with multi-source query' },
      { label: 'Search', href: '/search', description: 'Hybrid search across all documents' }
    ]
  }
];

export default function Navigation() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);
  const pathname = usePathname();
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setOpenDropdown(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const toggleDropdown = (label: string) => {
    setOpenDropdown(openDropdown === label ? null : label);
  };

  return (
    <>
      <nav className="bg-[#1a1a1a] border-b border-[#262626]" ref={dropdownRef}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            {/* Logo */}
            <div className="flex items-center">
              <Link href="/" className="flex items-center space-x-3">
                <div className="w-9 h-9 bg-white rounded flex items-center justify-center">
                  <span className="text-[#1a1a1a] font-bold text-lg">A</span>
                </div>
                <div className="hidden sm:block">
                  <div className="text-white font-semibold text-lg leading-none">AEON Digital Twin</div>
                  <div className="text-gray-400 text-xs mt-0.5">Cybersecurity Platform</div>
                </div>
              </Link>
            </div>

            {/* Desktop Menu */}
            <div className="hidden md:flex items-center space-x-1">
              {menuItems.map((item) => (
                <div key={item.label} className="relative">
                  {item.items ? (
                    <button
                      onClick={() => toggleDropdown(item.label)}
                      className="px-4 py-2 text-gray-300 hover:text-white hover:bg-[#262626] rounded transition-all duration-150 flex items-center space-x-1 font-medium text-sm"
                    >
                      <span>{item.label}</span>
                      <ChevronDown className={`w-4 h-4 transition-transform duration-200 ${openDropdown === item.label ? 'rotate-180' : ''}`} />
                    </button>
                  ) : (
                    <Link
                      href={item.href!}
                      className="px-4 py-2 text-gray-300 hover:text-white hover:bg-[#262626] rounded transition-all duration-150 font-medium text-sm"
                    >
                      {item.label}
                    </Link>
                  )}

                  {/* Dropdown Menu */}
                  {item.items && openDropdown === item.label && (
                    <div className="absolute top-full left-0 mt-2 w-80 bg-[#1a1a1a] border border-[#404040] rounded-lg shadow-2xl z-50 animate-fadeIn">
                      <div className="py-2">
                        {item.items.map((subItem, index) => (
                          <Link
                            key={subItem.href}
                            href={subItem.href}
                            onClick={() => setOpenDropdown(null)}
                            className={`block px-4 py-3 hover:bg-[#262626] transition-all duration-150 ${
                              pathname === subItem.href ? 'bg-[#262626]' : ''
                            } ${index < item.items!.length - 1 ? 'border-b border-[#262626]' : ''}`}
                          >
                            <div className="text-white font-medium text-sm">{subItem.label}</div>
                            <div className="text-gray-400 text-xs mt-1 leading-relaxed">{subItem.description}</div>
                          </Link>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden flex items-center">
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="text-gray-300 hover:text-white p-2 rounded hover:bg-[#262626] transition-colors"
                aria-label="Toggle menu"
              >
                {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-[#1a1a1a] border-t border-[#262626] animate-fadeIn">
            <div className="px-4 py-4 space-y-2">
              {menuItems.map((item) => (
                <div key={item.label}>
                  {item.items ? (
                    <>
                      <button
                        onClick={() => toggleDropdown(item.label)}
                        className="w-full text-left px-4 py-3 text-gray-300 hover:text-white hover:bg-[#262626] rounded flex justify-between items-center font-medium"
                      >
                        <span>{item.label}</span>
                        <ChevronDown className={`w-4 h-4 transition-transform duration-200 ${openDropdown === item.label ? 'rotate-180' : ''}`} />
                      </button>
                      {openDropdown === item.label && (
                        <div className="ml-4 mt-2 space-y-1 animate-fadeIn">
                          {item.items.map((subItem) => (
                            <Link
                              key={subItem.href}
                              href={subItem.href}
                              onClick={() => {
                                setMobileMenuOpen(false);
                                setOpenDropdown(null);
                              }}
                              className={`block px-4 py-3 rounded text-sm ${
                                pathname === subItem.href
                                  ? 'bg-[#262626] text-white'
                                  : 'text-gray-400 hover:text-white hover:bg-[#262626]'
                              }`}
                            >
                              <div className="font-medium">{subItem.label}</div>
                              <div className="text-xs text-gray-500 mt-0.5">{subItem.description}</div>
                            </Link>
                          ))}
                        </div>
                      )}
                    </>
                  ) : (
                    <Link
                      href={item.href!}
                      onClick={() => setMobileMenuOpen(false)}
                      className="block px-4 py-3 text-gray-300 hover:text-white hover:bg-[#262626] rounded font-medium"
                    >
                      {item.label}
                    </Link>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </nav>

      {/* Spacer for fixed nav */}
      <div className="h-16"></div>
    </>
  );
}
