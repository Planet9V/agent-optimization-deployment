'use client';

import { Calendar } from 'lucide-react';

interface DateRangeSelectorProps {
  startDate: Date;
  endDate: Date;
  onChange: (start: Date, end: Date) => void;
}

export default function DateRangeSelector({
  startDate,
  endDate,
  onChange,
}: DateRangeSelectorProps) {
  const formatDate = (date: Date) => {
    return date.toISOString().split('T')[0];
  };

  const handleStartChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newStart = new Date(e.target.value);
    onChange(newStart, endDate);
  };

  const handleEndChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newEnd = new Date(e.target.value);
    onChange(startDate, newEnd);
  };

  const presetRanges = [
    { label: 'Last 30 days', days: 30 },
    { label: 'Last 90 days', days: 90 },
    { label: 'Last 6 months', days: 180 },
    { label: 'Last year', days: 365 },
  ];

  const handlePresetClick = (days: number) => {
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - days);
    onChange(start, end);
  };

  return (
    <div className="flex items-center flex-wrap gap-4">
      {/* Custom Date Range */}
      <div className="flex items-center space-x-2">
        <label className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          From:
        </label>
        <input
          type="date"
          value={formatDate(startDate)}
          onChange={handleStartChange}
          className="px-3 py-2 rounded-md text-sm transition-all"
          style={{
            backgroundColor: 'var(--surface)',
            border: '1px solid var(--border-default)',
            color: 'var(--text-primary)',
          }}
          onFocus={(e) => {
            e.currentTarget.style.borderColor = 'var(--primary)';
          }}
          onBlur={(e) => {
            e.currentTarget.style.borderColor = 'var(--border-default)';
          }}
        />
      </div>

      <div className="flex items-center space-x-2">
        <label className="text-sm" style={{ color: 'var(--text-secondary)' }}>
          To:
        </label>
        <input
          type="date"
          value={formatDate(endDate)}
          onChange={handleEndChange}
          className="px-3 py-2 rounded-md text-sm transition-all"
          style={{
            backgroundColor: 'var(--surface)',
            border: '1px solid var(--border-default)',
            color: 'var(--text-primary)',
          }}
          onFocus={(e) => {
            e.currentTarget.style.borderColor = 'var(--primary)';
          }}
          onBlur={(e) => {
            e.currentTarget.style.borderColor = 'var(--border-default)';
          }}
        />
      </div>

      {/* Preset Ranges */}
      <div className="flex items-center space-x-2">
        <span className="text-sm" style={{ color: 'var(--text-tertiary)' }}>
          Quick select:
        </span>
        {presetRanges.map((preset) => (
          <button
            key={preset.label}
            onClick={() => handlePresetClick(preset.days)}
            className="px-3 py-1.5 rounded-md text-sm font-medium transition-all"
            style={{
              backgroundColor: 'var(--slate-100)',
              color: 'var(--text-secondary)',
              border: '1px solid var(--border-subtle)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = 'var(--primary)';
              e.currentTarget.style.color = 'white';
              e.currentTarget.style.borderColor = 'var(--primary)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'var(--slate-100)';
              e.currentTarget.style.color = 'var(--text-secondary)';
              e.currentTarget.style.borderColor = 'var(--border-subtle)';
            }}
          >
            {preset.label}
          </button>
        ))}
      </div>
    </div>
  );
}
