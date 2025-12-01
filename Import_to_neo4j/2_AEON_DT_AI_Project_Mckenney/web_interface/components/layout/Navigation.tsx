'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronDown, Menu, X } from 'lucide-react';

interface MenuItem {
  label: string;
  href?: string;
  items?: { label: string; href: string; description?: string }[];
}

export default function Navigation() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);
  const pathname = usePathname();

  const menuItems: MenuItem[] = [
    {
      label: 'Dashboard',
      items: [
        { label: 'Home', href: '/', description: 'Main dashboard overview' },
        { label: 'Analytics', href: '/analytics', description: 'Data analytics and insights' },
        { label: 'Observability', href: '/observability', description: 'System monitoring' }
      ]
    },
    {
      label: 'Data',
      items: [
        { label: 'Upload Documents', href: '/upload', description: 'Import and process files' },
        { label: 'Customers', href: '/customers', description: 'Customer management' },
        { label: 'Tags', href: '/tags', description: 'Tag organization' }
      ]
    },
    {
      label: 'Knowledge',
      items: [
        { label: 'Graph Visualization', href: '/graph', description: 'Neo4j knowledge graph' },
        { label: 'AI Chat', href: '/chat', description: 'AI-powered assistant' },
        { label: 'Search', href: '/search', description: 'Search documents' }
      ]
    }
  ];

  const toggleDropdown = (label: string) => {
    setOpenDropdown(openDropdown === label ? null : label);
  };

  return (
    <nav className="bg-[#1a1a1a] border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-white rounded-md flex items-center justify-center">
                <span className="text-[#1a1a1a] font-bold text-lg">A</span>
              </div>
              <span className="text-white font-semibold text-xl">AEON Digital Twin</span>
            </Link>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-1">
            {menuItems.map((item) => (
              <div key={item.label} className="relative">
                {item.items ? (
                  <button
                    onClick={() => toggleDropdown(item.label)}
                    className="px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-md transition-colors duration-150 flex items-center space-x-1"
                  >
                    <span>{item.label}</span>
                    <ChevronDown className={`w-4 h-4 transition-transform ${openDropdown === item.label ? 'rotate-180' : ''}`} />
                  </button>
                ) : (
                  <Link
                    href={item.href!}
                    className="px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-md transition-colors duration-150"
                  >
                    {item.label}
                  </Link>
                )}

                {/* Dropdown Menu */}
                {item.items && openDropdown === item.label && (
                  <div className="absolute top-full left-0 mt-1 w-72 bg-[#1a1a1a] border border-gray-800 rounded-md shadow-2xl z-50">
                    <div className="py-2">
                      {item.items.map((subItem) => (
                        <Link
                          key={subItem.href}
                          href={subItem.href}
                          onClick={() => setOpenDropdown(null)}
                          className={`block px-4 py-3 hover:bg-gray-800 transition-colors duration-150 ${
                            pathname === subItem.href ? 'bg-gray-800' : ''
                          }`}
                        >
                          <div className="text-white font-medium">{subItem.label}</div>
                          {subItem.description && (
                            <div className="text-gray-400 text-sm mt-1">{subItem.description}</div>
                          )}
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
              className="text-gray-300 hover:text-white p-2"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-[#1a1a1a] border-t border-gray-800">
          <div className="px-4 py-4 space-y-2">
            {menuItems.map((item) => (
              <div key={item.label}>
                {item.items ? (
                  <>
                    <button
                      onClick={() => toggleDropdown(item.label)}
                      className="w-full text-left px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-md flex justify-between items-center"
                    >
                      <span>{item.label}</span>
                      <ChevronDown className={`w-4 h-4 transition-transform ${openDropdown === item.label ? 'rotate-180' : ''}`} />
                    </button>
                    {openDropdown === item.label && (
                      <div className="ml-4 mt-2 space-y-2">
                        {item.items.map((subItem) => (
                          <Link
                            key={subItem.href}
                            href={subItem.href}
                            onClick={() => {
                              setMobileMenuOpen(false);
                              setOpenDropdown(null);
                            }}
                            className={`block px-4 py-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-md ${
                              pathname === subItem.href ? 'bg-gray-800 text-white' : ''
                            }`}
                          >
                            {subItem.label}
                          </Link>
                        ))}
                      </div>
                    )}
                  </>
                ) : (
                  <Link
                    href={item.href!}
                    onClick={() => setMobileMenuOpen(false)}
                    className="block px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-md"
                  >
                    {item.label}
                  </Link>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Click outside to close dropdown */}
      {openDropdown && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setOpenDropdown(null)}
        />
      )}
    </nav>
  );
}
