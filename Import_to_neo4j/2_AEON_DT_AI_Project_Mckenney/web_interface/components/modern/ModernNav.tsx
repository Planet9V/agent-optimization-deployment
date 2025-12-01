'use client';

import Link from 'next/link';
import { Shield, Database, Search, Settings } from 'lucide-react';

export default function ModernNav() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-emerald-500/20">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2 group">
            <Shield className="h-8 w-8 text-emerald-500 group-hover:text-emerald-400 transition-colors" />
            <span className="text-xl font-bold text-slate-50">AEON Digital Twin</span>
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center space-x-6">
            <Link
              href="/knowledge-graph"
              className="flex items-center space-x-2 text-slate-300 hover:text-emerald-400 transition-colors"
            >
              <Database className="h-5 w-5" />
              <span>Knowledge Graph</span>
            </Link>
            <Link
              href="/search"
              className="flex items-center space-x-2 text-slate-300 hover:text-emerald-400 transition-colors"
            >
              <Search className="h-5 w-5" />
              <span>Search</span>
            </Link>
            <Link
              href="/settings"
              className="flex items-center space-x-2 text-slate-300 hover:text-emerald-400 transition-colors"
            >
              <Settings className="h-5 w-5" />
              <span>Settings</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
