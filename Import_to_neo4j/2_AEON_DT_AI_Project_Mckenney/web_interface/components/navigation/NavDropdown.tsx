import React, { useState, useRef, useEffect, ReactNode } from 'react';
import { ChevronDown } from 'lucide-react';

interface NavDropdownProps {
  label: string;
  icon: ReactNode;
  items: Array<{
    label: string;
    href: string;
  }>;
}

const NavDropdown: React.FC<NavDropdownProps> = ({ label, icon, items }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        onMouseEnter={() => setIsOpen(true)}
        className="group flex items-center px-3 py-2 rounded-md text-sm font-medium text-slate-100 hover:text-emerald-500 hover:bg-slate-900 transition-all duration-200"
      >
        <span className="mr-2">{icon}</span>
        {label}
        <ChevronDown
          className={`ml-1 w-4 h-4 transition-transform duration-200 ${
            isOpen ? 'rotate-180' : ''
          }`}
        />
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div
          className="absolute left-0 mt-1 w-56 rounded-md shadow-lg bg-slate-900 ring-1 ring-slate-800 ring-opacity-50 divide-y divide-slate-800 animate-in fade-in-0 zoom-in-95 duration-200"
          onMouseLeave={() => setIsOpen(false)}
        >
          <div className="py-1" role="menu" aria-orientation="vertical">
            {items.map((item, index) => (
              <a
                key={index}
                href={item.href}
                className="group flex items-center px-4 py-3 text-sm text-slate-100 hover:text-emerald-500 hover:bg-slate-800 transition-colors duration-150"
                role="menuitem"
              >
                <span className="flex-1">{item.label}</span>
                <svg
                  className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5l7 7-7 7"
                  />
                </svg>
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default NavDropdown;
