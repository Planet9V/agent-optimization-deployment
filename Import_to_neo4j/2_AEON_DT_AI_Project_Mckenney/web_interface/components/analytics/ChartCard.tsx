'use client';

import React from 'react';
import { Card } from '@tremor/react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface ChartCardProps {
  title: string;
  description?: string;
  type: 'line' | 'bar' | 'pie';
  data: any[];
  dataKeys?: {
    x?: string;
    y?: string;
    name?: string;
    value?: string;
  };
  colors?: string[];
  loading?: boolean;
  error?: string;
  height?: number;
}

const COLORS = [
  '#3b82f6', // blue-500
  '#10b981', // emerald-500
  '#f59e0b', // amber-500
  '#ef4444', // red-500
  '#8b5cf6', // violet-500
  '#ec4899', // pink-500
  '#06b6d4', // cyan-500
  '#f97316', // orange-500
];

export function ChartCard({
  title,
  description,
  type,
  data,
  dataKeys = {},
  colors = COLORS,
  loading = false,
  error,
  height = 300,
}: ChartCardProps) {
  if (loading) {
    return (
      <Card className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/3 mb-2"></div>
        {description && <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>}
        <div className="h-64 bg-gray-200 rounded"></div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
        {description && <p className="text-sm text-gray-500 mb-4">{description}</p>}
        <div className="h-64 flex items-center justify-center">
          <div className="text-center">
            <p className="text-red-600 mb-2">Error loading chart</p>
            <p className="text-sm text-gray-500">{error}</p>
          </div>
        </div>
      </Card>
    );
  }

  if (!data || data.length === 0) {
    return (
      <Card>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
        {description && <p className="text-sm text-gray-500 mb-4">{description}</p>}
        <div className="h-64 flex items-center justify-center">
          <p className="text-gray-500">No data available</p>
        </div>
      </Card>
    );
  }

  const renderChart = () => {
    switch (type) {
      case 'line':
        return (
          <ResponsiveContainer width="100%" height={height}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={dataKeys.x || 'name'} />
              <YAxis />
              <Tooltip />
              <Legend />
              {dataKeys.y ? (
                <Line
                  type="monotone"
                  dataKey={dataKeys.y}
                  stroke={colors[0]}
                  strokeWidth={2}
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }}
                />
              ) : (
                Object.keys(data[0])
                  .filter(key => key !== (dataKeys.x || 'name'))
                  .map((key, index) => (
                    <Line
                      key={key}
                      type="monotone"
                      dataKey={key}
                      stroke={colors[index % colors.length]}
                      strokeWidth={2}
                      dot={{ r: 4 }}
                      activeDot={{ r: 6 }}
                    />
                  ))
              )}
            </LineChart>
          </ResponsiveContainer>
        );

      case 'bar':
        return (
          <ResponsiveContainer width="100%" height={height}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={dataKeys.x || 'name'} />
              <YAxis />
              <Tooltip />
              <Legend />
              {dataKeys.y ? (
                <Bar dataKey={dataKeys.y} fill={colors[0]} radius={[8, 8, 0, 0]} />
              ) : (
                Object.keys(data[0])
                  .filter(key => key !== (dataKeys.x || 'name'))
                  .map((key, index) => (
                    <Bar
                      key={key}
                      dataKey={key}
                      fill={colors[index % colors.length]}
                      radius={[8, 8, 0, 0]}
                    />
                  ))
              )}
            </BarChart>
          </ResponsiveContainer>
        );

      case 'pie':
        return (
          <ResponsiveContainer width="100%" height={height}>
            <PieChart>
              <Pie
                data={data}
                dataKey={dataKeys.value || 'value'}
                nameKey={dataKeys.name || 'name'}
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={(entry) => `${entry.name}: ${entry.value}`}
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        );

      default:
        return null;
    }
  };

  return (
    <Card>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      {description && <p className="text-sm text-gray-500 mb-4">{description}</p>}
      {renderChart()}
    </Card>
  );
}
