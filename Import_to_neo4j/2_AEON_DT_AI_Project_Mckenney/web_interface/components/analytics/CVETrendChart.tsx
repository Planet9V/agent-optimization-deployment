'use client';

import { useState, useEffect } from 'react';
import { LineChart, TrendingUp } from 'lucide-react';

interface CVETrendChartProps {
  loading: boolean;
  dateRange: { start: Date; end: Date };
}

interface MonthlyTrend {
  month: string;
  critical: number;
  high: number;
  medium: number;
  low: number;
}

export default function CVETrendChart({ loading, dateRange }: CVETrendChartProps) {
  const [data, setData] = useState<MonthlyTrend[]>([]);
  const [fetching, setFetching] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setFetching(true);
      try {
        const params = new URLSearchParams({
          startDate: dateRange.start.toISOString(),
          endDate: dateRange.end.toISOString(),
        });

        const response = await fetch(`/api/analytics/trends/cve?${params}`);
        const result = await response.json();

        if (result.monthlyTrends) {
          setData(result.monthlyTrends);
        }
      } catch (error) {
        console.error('Error fetching CVE trends:', error);
      } finally {
        setFetching(false);
      }
    };

    fetchData();
  }, [dateRange]);

  if (loading || fetching) {
    return (
      <div className="h-80 flex items-center justify-center">
        <div className="skeleton h-full w-full rounded-lg"></div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="h-80 flex items-center justify-center">
        <p style={{ color: 'var(--text-secondary)' }}>No CVE data available for selected date range</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Legend */}
      <div className="flex items-center justify-center space-x-6 text-sm">
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded" style={{ backgroundColor: 'var(--severity-critical)' }}></div>
          <span style={{ color: 'var(--text-secondary)' }}>Critical</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded" style={{ backgroundColor: 'var(--severity-high)' }}></div>
          <span style={{ color: 'var(--text-secondary)' }}>High</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded" style={{ backgroundColor: 'var(--severity-medium)' }}></div>
          <span style={{ color: 'var(--text-secondary)' }}>Medium</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded" style={{ backgroundColor: 'var(--severity-low)' }}></div>
          <span style={{ color: 'var(--text-secondary)' }}>Low</span>
        </div>
      </div>

      {/* Simple Bar Chart Visualization */}
      <div className="h-80 flex items-end justify-around space-x-2">
        {data.map((monthData, index) => {
          const total = monthData.critical + monthData.high + monthData.medium + monthData.low;
          const maxTotal = Math.max(...data.map(d => d.critical + d.high + d.medium + d.low));
          const heightPercent = (total / maxTotal) * 100;

          return (
            <div key={index} className="flex-1 flex flex-col items-center space-y-2">
              <div className="w-full flex flex-col items-stretch" style={{ height: `${heightPercent}%` }}>
                <div
                  className="flex-grow rounded-t"
                  style={{
                    backgroundColor: 'var(--severity-critical)',
                    height: `${(monthData.critical / total) * 100}%`,
                  }}
                  title={`Critical: ${monthData.critical}`}
                ></div>
                <div
                  className="flex-grow"
                  style={{
                    backgroundColor: 'var(--severity-high)',
                    height: `${(monthData.high / total) * 100}%`,
                  }}
                  title={`High: ${monthData.high}`}
                ></div>
                <div
                  className="flex-grow"
                  style={{
                    backgroundColor: 'var(--severity-medium)',
                    height: `${(monthData.medium / total) * 100}%`,
                  }}
                  title={`Medium: ${monthData.medium}`}
                ></div>
                <div
                  className="flex-grow rounded-b"
                  style={{
                    backgroundColor: 'var(--severity-low)',
                    height: `${(monthData.low / total) * 100}%`,
                  }}
                  title={`Low: ${monthData.low}`}
                ></div>
              </div>
              <span className="text-xs" style={{ color: 'var(--text-tertiary)' }}>
                {monthData.month}
              </span>
            </div>
          );
        })}
      </div>

      {/* Data Table */}
      <div className="mt-6 overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr style={{ borderBottom: '1px solid var(--border-default)' }}>
              <th className="text-left py-2 px-4" style={{ color: 'var(--text-secondary)' }}>Month</th>
              <th className="text-right py-2 px-4" style={{ color: 'var(--severity-critical)' }}>Critical</th>
              <th className="text-right py-2 px-4" style={{ color: 'var(--severity-high)' }}>High</th>
              <th className="text-right py-2 px-4" style={{ color: 'var(--severity-medium)' }}>Medium</th>
              <th className="text-right py-2 px-4" style={{ color: 'var(--severity-low)' }}>Low</th>
              <th className="text-right py-2 px-4" style={{ color: 'var(--text-primary)' }}>Total</th>
            </tr>
          </thead>
          <tbody>
            {data.map((monthData, index) => (
              <tr key={index} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                <td className="py-2 px-4" style={{ color: 'var(--text-primary)' }}>{monthData.month}</td>
                <td className="text-right py-2 px-4 font-medium" style={{ color: 'var(--text-secondary)' }}>{monthData.critical}</td>
                <td className="text-right py-2 px-4 font-medium" style={{ color: 'var(--text-secondary)' }}>{monthData.high}</td>
                <td className="text-right py-2 px-4 font-medium" style={{ color: 'var(--text-secondary)' }}>{monthData.medium}</td>
                <td className="text-right py-2 px-4 font-medium" style={{ color: 'var(--text-secondary)' }}>{monthData.low}</td>
                <td className="text-right py-2 px-4 font-bold" style={{ color: 'var(--text-primary)' }}>
                  {monthData.critical + monthData.high + monthData.medium + monthData.low}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
