'use client';

import Link from 'next/link';
import { useState, useRef, useEffect } from 'react';
import {
  Shield,
  Database,
  Search,
  Activity,
  BarChart3,
  ChevronDown,
  FileText,
  MessageSquare,
  Upload,
  Users,
  Tag,
  TrendingUp,
  Eye,
  Target,
  Menu,
  X
} from 'lucide-react';
import { SignedIn, SignedOut, UserButton, SignInButton } from '@clerk/nextjs';

export default function ModernNav() {
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const dropdownRefs = useRef<Map<string, HTMLDivElement | null>>(new Map());
  const mobileMenuRef = useRef<HTMLDivElement | null>(null);

  const toggleDropdown = (dropdown: string) => {
    setOpenDropdown(openDropdown === dropdown ? null : dropdown);
  };

  const closeDropdowns = () => {
    setOpenDropdown(null);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
    setOpenDropdown(null);
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
    setOpenDropdown(null);
  };

  // Click outside handler for desktop dropdowns
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      setTimeout(() => {
        if (!openDropdown) return;
        const dropdownElement = dropdownRefs.current.get(openDropdown);
        if (dropdownElement && !dropdownElement.contains(event.target as Node)) {
          setOpenDropdown(null);
        }
      }, 0);
    };

    if (openDropdown) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [openDropdown]);

  // Body scroll lock when mobile menu is open
  useEffect(() => {
    if (isMobileMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }

    return () => {
      document.body.style.overflow = '';
    };
  }, [isMobileMenuOpen]);

  // ESC key handler for mobile menu
  useEffect(() => {
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isMobileMenuOpen) {
        closeMobileMenu();
      }
    };

    if (isMobileMenuOpen) {
      document.addEventListener('keydown', handleEscKey);
    }

    return () => {
      document.removeEventListener('keydown', handleEscKey);
    };
  }, [isMobileMenuOpen]);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-emerald-500/20">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-3 group">
            <div className="relative">
              <Shield className="h-8 w-8 text-emerald-500 group-hover:text-emerald-400 transition-colors duration-300" />
              <div className="absolute inset-0 blur-lg bg-emerald-500/20 group-hover:bg-emerald-500/30 transition-all duration-300" />
            </div>
            <span className="text-xl font-bold text-slate-50 group-hover:text-emerald-400 transition-colors duration-300">
              AEON Digital Twin
            </span>
          </Link>

          {/* Hamburger Menu Button (Mobile Only) */}
          <button
            onClick={toggleMobileMenu}
            className="md:hidden p-2 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
            aria-label="Toggle mobile menu"
            aria-expanded={isMobileMenuOpen}
            aria-controls="mobile-menu"
          >
            {isMobileMenuOpen ? (
              <X className="h-6 w-6" />
            ) : (
              <Menu className="h-6 w-6" />
            )}
          </button>

          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center space-x-1">
            {/* Home/Dashboard */}
            <Link
              href="/dashboard"
              className="flex items-center space-x-2 px-4 py-2 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
              onClick={closeDropdowns}
            >
              <Activity className="h-5 w-5" />
              <span className="font-medium">Home</span>
            </Link>

            {/* Threat Intelligence - Top Level (Flagship Feature) */}
            <Link
              href="/threat-intel"
              className="flex items-center space-x-2 px-4 py-2 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
              onClick={closeDropdowns}
            >
              <Target className="h-5 w-5" />
              <span className="font-medium">Threat Intelligence</span>
            </Link>

            {/* Investigate Dropdown */}
            <div className="relative group">
              <button
                className="flex items-center space-x-2 px-4 py-2 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                onClick={() => toggleDropdown('investigate')}
              >
                <Search className="h-5 w-5" />
                <span className="font-medium">Investigate</span>
                <ChevronDown className={`h-4 w-4 transition-transform duration-200 ${openDropdown === 'investigate' ? 'rotate-180' : ''}`} />
              </button>

              {/* Investigate Dropdown Menu */}
              {openDropdown === 'investigate' && (
                <div
                  className="modern-dropdown"
                  ref={(el) => {
                    dropdownRefs.current.set('investigate', el);
                  }}
                >
                  <Link
                    href="/search"
                    className="modern-dropdown-item"
                    onClick={closeDropdowns}
                  >
                    <Search className="h-4 w-4 text-emerald-400" />
                    <span>Search</span>
                  </Link>
                  <Link
                    href="/graph"
                    className="modern-dropdown-item"
                    onClick={closeDropdowns}
                  >
                    <Database className="h-4 w-4 text-blue-400" />
                    <span>Knowledge Graph</span>
                  </Link>
                  <Link
                    href="/chat"
                    className="modern-dropdown-item"
                    onClick={closeDropdowns}
                  >
                    <MessageSquare className="h-4 w-4 text-purple-400" />
                    <span>AI Assistant</span>
                  </Link>
                </div>
              )}
            </div>

            {/* Analyze Dropdown */}
            <div className="relative group">
              <button
                className="flex items-center space-x-2 px-4 py-2 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                onClick={() => toggleDropdown('analyze')}
              >
                <BarChart3 className="h-5 w-5" />
                <span className="font-medium">Analyze</span>
                <ChevronDown className={`h-4 w-4 transition-transform duration-200 ${openDropdown === 'analyze' ? 'rotate-180' : ''}`} />
              </button>

              {/* Analyze Dropdown Menu */}
              {openDropdown === 'analyze' && (
                <div
                  className="modern-dropdown"
                  ref={(el) => {
                    dropdownRefs.current.set('analyze', el);
                  }}
                >
                  <Link
                    href="/analytics/trends"
                    className="modern-dropdown-item"
                    onClick={closeDropdowns}
                  >
                    <TrendingUp className="h-4 w-4 text-emerald-400" />
                    <span>Trends</span>
                  </Link>
                  <Link
                    href="/analytics"
                    className="modern-dropdown-item"
                    onClick={closeDropdowns}
                  >
                    <FileText className="h-4 w-4 text-blue-400" />
                    <span>Reports</span>
                  </Link>
                  <Link
                    href="/observability"
                    className="modern-dropdown-item"
                    onClick={closeDropdowns}
                  >
                    <Eye className="h-4 w-4 text-purple-400" />
                    <span>Observability</span>
                  </Link>
                </div>
              )}
            </div>

            {/* Manage Dropdown */}
            <div className="relative group">
              <button
                className="flex items-center space-x-2 px-4 py-2 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                onClick={() => toggleDropdown('manage')}
              >
                <Database className="h-5 w-5" />
                <span className="font-medium">Manage</span>
                <ChevronDown className={`h-4 w-4 transition-transform duration-200 ${openDropdown === 'manage' ? 'rotate-180' : ''}`} />
              </button>

              {/* Manage Dropdown Menu */}
              {openDropdown === 'manage' && (
                <div
                  className="modern-dropdown"
                  ref={(el) => {
                    dropdownRefs.current.set('manage', el);
                  }}
                >
                  <Link
                    href="/upload"
                    className="modern-dropdown-item"
                    onClick={closeDropdowns}
                  >
                    <Upload className="h-4 w-4 text-emerald-400" />
                    <span>Documents</span>
                  </Link>
                  <Link
                    href="/customers"
                    className="modern-dropdown-item"
                    onClick={closeDropdowns}
                  >
                    <Users className="h-4 w-4 text-blue-400" />
                    <span>Customers</span>
                  </Link>
                  <Link
                    href="/tags"
                    className="modern-dropdown-item"
                    onClick={closeDropdowns}
                  >
                    <Tag className="h-4 w-4 text-purple-400" />
                    <span>Tags</span>
                  </Link>
                </div>
              )}
            </div>

            {/* Authentication */}
            <div className="ml-4 flex items-center space-x-3">
              <SignedOut>
                <SignInButton mode="modal">
                  <button className="px-4 py-2 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200 font-medium">
                    Sign In
                  </button>
                </SignInButton>
              </SignedOut>
              <SignedIn>
                <UserButton
                  appearance={{
                    elements: {
                      avatarBox: "h-9 w-9 ring-2 ring-emerald-500/20 hover:ring-emerald-500/40 transition-all duration-200"
                    }
                  }}
                />
              </SignedIn>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Menu Panel */}
      {isMobileMenuOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-40 md:hidden"
            onClick={closeMobileMenu}
            aria-hidden="true"
          />

          {/* Mobile Menu Panel */}
          <div
            id="mobile-menu"
            ref={mobileMenuRef}
            role="dialog"
            aria-modal="true"
            aria-label="Mobile navigation menu"
            className="fixed top-0 right-0 bottom-0 w-80 bg-slate-900 border-l border-emerald-500/20 z-50 md:hidden transform transition-transform duration-300 ease-in-out overflow-y-auto"
            style={{
              transform: isMobileMenuOpen ? 'translateX(0)' : 'translateX(100%)',
            }}
          >
            {/* Panel Header */}
            <div className="flex items-center justify-between p-6 border-b border-emerald-500/20">
              <div className="flex items-center space-x-3">
                <Shield className="h-6 w-6 text-emerald-500" />
                <span className="text-lg font-bold text-slate-50">AEON Menu</span>
              </div>
              <button
                onClick={closeMobileMenu}
                className="p-2 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                aria-label="Close mobile menu"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            {/* Navigation Items */}
            <div className="p-4 space-y-2">
              {/* Home/Dashboard */}
              <Link
                href="/dashboard"
                className="flex items-center space-x-3 px-4 py-3 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                onClick={closeMobileMenu}
              >
                <Activity className="h-5 w-5" />
                <span className="font-medium">Home</span>
              </Link>

              {/* Threat Intelligence */}
              <Link
                href="/threat-intel"
                className="flex items-center space-x-3 px-4 py-3 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                onClick={closeMobileMenu}
              >
                <Target className="h-5 w-5" />
                <span className="font-medium">Threat Intelligence</span>
              </Link>

              {/* Investigate Section */}
              <div className="space-y-1">
                <button
                  className="w-full flex items-center justify-between px-4 py-3 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                  onClick={() => toggleDropdown('investigate-mobile')}
                  aria-expanded={openDropdown === 'investigate-mobile'}
                >
                  <div className="flex items-center space-x-3">
                    <Search className="h-5 w-5" />
                    <span className="font-medium">Investigate</span>
                  </div>
                  <ChevronDown
                    className={`h-4 w-4 transition-transform duration-200 ${
                      openDropdown === 'investigate-mobile' ? 'rotate-180' : ''
                    }`}
                  />
                </button>
                {openDropdown === 'investigate-mobile' && (
                  <div className="pl-4 space-y-1">
                    <Link
                      href="/search"
                      className="flex items-center space-x-3 px-4 py-2 text-slate-400 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                      onClick={closeMobileMenu}
                    >
                      <Search className="h-4 w-4 text-emerald-400" />
                      <span>Search</span>
                    </Link>
                    <Link
                      href="/graph"
                      className="flex items-center space-x-3 px-4 py-2 text-slate-400 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                      onClick={closeMobileMenu}
                    >
                      <Database className="h-4 w-4 text-blue-400" />
                      <span>Knowledge Graph</span>
                    </Link>
                    <Link
                      href="/chat"
                      className="flex items-center space-x-3 px-4 py-2 text-slate-400 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                      onClick={closeMobileMenu}
                    >
                      <MessageSquare className="h-4 w-4 text-purple-400" />
                      <span>AI Assistant</span>
                    </Link>
                  </div>
                )}
              </div>

              {/* Analyze Section */}
              <div className="space-y-1">
                <button
                  className="w-full flex items-center justify-between px-4 py-3 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                  onClick={() => toggleDropdown('analyze-mobile')}
                  aria-expanded={openDropdown === 'analyze-mobile'}
                >
                  <div className="flex items-center space-x-3">
                    <BarChart3 className="h-5 w-5" />
                    <span className="font-medium">Analyze</span>
                  </div>
                  <ChevronDown
                    className={`h-4 w-4 transition-transform duration-200 ${
                      openDropdown === 'analyze-mobile' ? 'rotate-180' : ''
                    }`}
                  />
                </button>
                {openDropdown === 'analyze-mobile' && (
                  <div className="pl-4 space-y-1">
                    <Link
                      href="/analytics/trends"
                      className="flex items-center space-x-3 px-4 py-2 text-slate-400 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                      onClick={closeMobileMenu}
                    >
                      <TrendingUp className="h-4 w-4 text-emerald-400" />
                      <span>Trends</span>
                    </Link>
                    <Link
                      href="/analytics"
                      className="flex items-center space-x-3 px-4 py-2 text-slate-400 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                      onClick={closeMobileMenu}
                    >
                      <FileText className="h-4 w-4 text-blue-400" />
                      <span>Reports</span>
                    </Link>
                    <Link
                      href="/observability"
                      className="flex items-center space-x-3 px-4 py-2 text-slate-400 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                      onClick={closeMobileMenu}
                    >
                      <Eye className="h-4 w-4 text-purple-400" />
                      <span>Observability</span>
                    </Link>
                  </div>
                )}
              </div>

              {/* Manage Section */}
              <div className="space-y-1">
                <button
                  className="w-full flex items-center justify-between px-4 py-3 text-slate-300 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                  onClick={() => toggleDropdown('manage-mobile')}
                  aria-expanded={openDropdown === 'manage-mobile'}
                >
                  <div className="flex items-center space-x-3">
                    <Database className="h-5 w-5" />
                    <span className="font-medium">Manage</span>
                  </div>
                  <ChevronDown
                    className={`h-4 w-4 transition-transform duration-200 ${
                      openDropdown === 'manage-mobile' ? 'rotate-180' : ''
                    }`}
                  />
                </button>
                {openDropdown === 'manage-mobile' && (
                  <div className="pl-4 space-y-1">
                    <Link
                      href="/upload"
                      className="flex items-center space-x-3 px-4 py-2 text-slate-400 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                      onClick={closeMobileMenu}
                    >
                      <Upload className="h-4 w-4 text-emerald-400" />
                      <span>Documents</span>
                    </Link>
                    <Link
                      href="/customers"
                      className="flex items-center space-x-3 px-4 py-2 text-slate-400 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                      onClick={closeMobileMenu}
                    >
                      <Users className="h-4 w-4 text-blue-400" />
                      <span>Customers</span>
                    </Link>
                    <Link
                      href="/tags"
                      className="flex items-center space-x-3 px-4 py-2 text-slate-400 hover:text-emerald-400 hover:bg-emerald-500/10 rounded-lg transition-all duration-200"
                      onClick={closeMobileMenu}
                    >
                      <Tag className="h-4 w-4 text-purple-400" />
                      <span>Tags</span>
                    </Link>
                  </div>
                )}
              </div>
            </div>

            {/* Authentication (Bottom of Panel) */}
            <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-emerald-500/20 bg-slate-900">
              <SignedOut>
                <SignInButton mode="modal">
                  <button className="w-full px-4 py-3 text-slate-300 hover:text-emerald-400 bg-emerald-500/10 hover:bg-emerald-500/20 rounded-lg transition-all duration-200 font-medium">
                    Sign In
                  </button>
                </SignInButton>
              </SignedOut>
              <SignedIn>
                <div className="flex items-center justify-center">
                  <UserButton
                    appearance={{
                      elements: {
                        avatarBox: "h-10 w-10 ring-2 ring-emerald-500/20 hover:ring-emerald-500/40 transition-all duration-200"
                      }
                    }}
                  />
                </div>
              </SignedIn>
            </div>
          </div>
        </>
      )}
    </nav>
  );
}
