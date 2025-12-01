import React from 'react';
import { ViewState } from './types';

interface NavigationProps {
  currentView: ViewState;
  onNavigate: (view: ViewState) => void;
}

export const Navigation: React.FC<NavigationProps> = ({ currentView, onNavigate }) => {
  const navItems = [
    { id: ViewState.CONTEXT, label: '01. CONTEXT' },
    { id: ViewState.ARCHITECTURE, label: '02. ARCHITECTURE' },
    { id: ViewState.CALCULUS, label: '03. CALCULUS' },
    { id: ViewState.LOGIC, label: '04. LOGIC' },
    { id: ViewState.FRAMEWORK, label: '05. FRAMEWORK' },
    { id: ViewState.TIMELINE, label: '06. TIMELINE' },
    { id: ViewState.AGENT_RED, label: '07. AGENT RED' },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 p-6 md:p-8 w-full z-50 bg-gradient-to-b from-dark to-transparent pointer-events-none">
      <nav className="flex justify-between items-center text-xs md:text-sm uppercase tracking-widest pointer-events-auto">
        <div className="flex items-center gap-4 cursor-pointer" onClick={() => onNavigate(ViewState.CONTEXT)}>
          <div className="w-8 h-8 md:w-10 md:h-10 border border-primary flex items-center justify-center bg-dark/50 backdrop-blur-sm hover:bg-primary/10 transition-colors">
            <span className="text-primary font-bold text-lg font-mono">Ψ</span>
          </div>
          <div className="hidden sm:block">
            <h1 className="font-bold text-white font-mono">CYBER PSYCHOHISTORY</h1>
            <p className="text-gray-500 font-mono text-[10px]">SYSTEM_V1.0.0</p>
          </div>
        </div>

        <div className="hidden lg:flex items-center gap-8 bg-dark/80 backdrop-blur-md px-6 py-2 border border-white/10 rounded-sm">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={`transition-all duration-300 font-mono ${currentView === item.id
                ? 'text-primary border-b border-primary pb-1'
                : 'text-gray-500 hover:text-white'
                }`}
            >
              {item.label}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-4">
          <div className="border border-primary/30 px-3 py-1 bg-primary/5 text-primary text-[10px] md:text-xs font-mono animate-pulse">
            SYSTEM: ONLINE
          </div>
        </div>
      </nav>

      {/* Mobile Navigation */}
      <div className="lg:hidden fixed bottom-0 left-0 w-full bg-dark/95 border-t border-white/10 p-4 flex justify-between px-8 z-50 backdrop-blur-lg">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => onNavigate(item.id)}
            className={`flex flex-col items-center transition-colors ${currentView === item.id ? 'text-primary' : 'text-gray-600'
              }`}
          >
            <span className="text-lg font-bold">{item.id === ViewState.CONTEXT ? '01' : item.id === ViewState.ARCHITECTURE ? '02' : item.id === ViewState.CALCULUS ? '03' : item.id === ViewState.LOGIC ? '04' : item.id === ViewState.FRAMEWORK ? '05' : '06'}</span>
          </button>
        ))}
      </div>
    </header>
  );
};