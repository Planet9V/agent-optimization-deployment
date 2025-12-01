'use client';

import { useState, useEffect } from 'react';
import { Calendar } from 'lucide-react';

interface SeasonalityHeatmapProps {
  loading: boolean;
}

interface SeasonalityCell {
  year: number;
  month: number;
  count: number;
  campaigns: string[];
}

interface SeasonalityData {
  heatmap: SeasonalityCell[];
  years: number[];
  months: number[];
  maxCount: number;
}

const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

export default function SeasonalityHeatmap({ loading }: SeasonalityHeatmapProps) {
  const [data, setData] = useState<SeasonalityData | null>(null);
  const [fetching, setFetching] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setFetching(true);
      try {
        const response = await fetch('/api/analytics/trends/seasonality');
        const result = await response.json();

        if (result.heatmap) {
          setData(result);
        }
      } catch (error) {
        console.error('Error fetching seasonality data:', error);
      } finally {
        setFetching(false);
      }
    };

    fetchData();
  }, []);

  if (loading || fetching) {
    return (
      <div className="h-96 flex items-center justify-center">
        <div className="skeleton h-full w-full rounded-lg"></div>
      </div>
    );
  }

  if (!data || data.heatmap.length === 0) {
    return (
      <div className="h-96 flex items-center justify-center">
        <p style={{ color: 'var(--text-secondary)' }}>No campaign seasonality data available</p>
      </div>
    );
  }

  // Create lookup map for quick access
  const cellMap = new Map<string, SeasonalityCell>();
  data.heatmap.forEach(cell => {
    const key = `${cell.year}-${cell.month}`;
    cellMap.set(key, cell);
  });

  const getHeatColor = (count: number | null) => {
    if (count === null || count === 0) return 'var(--slate-100)';
    const intensity = count / data.maxCount;
    if (intensity > 0.75) return 'var(--severity-critical)';
    if (intensity > 0.5) return 'var(--severity-high)';
    if (intensity > 0.25) return 'var(--severity-medium)';
    return 'var(--severity-low)';
  };

  const getTextColor = (count: number | null) => {
    if (count === null || count === 0) return 'var(--text-tertiary)';
    const intensity = count / data.maxCount;
    return intensity > 0.25 ? '#ffffff' : 'var(--text-primary)';
  };

  // Use most recent 5 years if available
  const displayYears = data.years.slice(0, 5);

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <div className="flex items-center justify-center gap-6 text-sm">
        <div className="flex items-center space-x-2">
          <Calendar className="h-4 w-4" style={{ color: 'var(--primary)' }} />
          <span style={{ color: 'var(--text-secondary)' }}>
            Campaign Seasonality Pattern
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <span
            className="px-2 py-1 rounded text-xs font-semibold"
            style={{
              backgroundColor: 'var(--severity-high-bg)',
              color: 'var(--severity-high)',
            }}
          >
            Peak: {data.maxCount} campaigns/month
          </span>
        </div>
      </div>

      {/* Heatmap Grid */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr>
              <th className="text-left py-3 px-4 text-sm" style={{ color: 'var(--text-secondary)' }}>
                Month
              </th>
              {displayYears.map(year => (
                <th key={year} className="text-center py-3 px-4 text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
                  {year}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map((month) => (
              <tr key={month}>
                <td className="py-2 px-4 text-sm font-medium" style={{ color: 'var(--text-primary)' }}>
                  {monthNames[month - 1]}
                </td>
                {displayYears.map(year => {
                  const key = `${year}-${month}`;
                  const cell = cellMap.get(key);
                  const count = cell?.count || 0;

                  return (
                    <td key={year} className="py-2 px-4">
                      <div
                        className="rounded p-3 text-center font-bold text-sm transition-all hover:scale-105 cursor-pointer"
                        style={{
                          backgroundColor: getHeatColor(count),
                          color: getTextColor(count),
                        }}
                        title={
                          count > 0
                            ? `${monthNames[month - 1]} ${year}: ${count} campaigns\n${cell?.campaigns.slice(0, 3).join(', ') || ''}`
                            : `${monthNames[month - 1]} ${year}: No campaigns`
                        }
                      >
                        {count > 0 ? count : '-'}
                      </div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center gap-4 text-sm">
        <span style={{ color: 'var(--text-secondary)' }}>Intensity:</span>
        <div className="flex items-center space-x-2">
          <div className="w-8 h-4 rounded" style={{ backgroundColor: 'var(--severity-low)' }}></div>
          <span style={{ color: 'var(--text-tertiary)' }}>Low</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-8 h-4 rounded" style={{ backgroundColor: 'var(--severity-medium)' }}></div>
          <span style={{ color: 'var(--text-tertiary)' }}>Medium</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-8 h-4 rounded" style={{ backgroundColor: 'var(--severity-high)' }}></div>
          <span style={{ color: 'var(--text-tertiary)' }}>High</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-8 h-4 rounded" style={{ backgroundColor: 'var(--severity-critical)' }}></div>
          <span style={{ color: 'var(--text-tertiary)' }}>Critical</span>
        </div>
      </div>

      {/* Pattern Insights */}
      {data.heatmap.length > 0 && (
        <div className="mt-4 p-4 rounded-lg" style={{ backgroundColor: 'var(--slate-50)' }}>
          <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
            <strong style={{ color: 'var(--text-primary)' }}>Pattern Analysis:</strong> Analyzing {data.heatmap.length} data points across {displayYears.length} years.
            Peak activity detected with {data.maxCount} campaigns in a single month.
          </p>
        </div>
      )}
    </div>
  );
}
