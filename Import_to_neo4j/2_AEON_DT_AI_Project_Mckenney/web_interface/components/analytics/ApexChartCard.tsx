'use client';

import React from 'react';
import dynamic from 'next/dynamic';
import { Card } from '@tremor/react';
import type { ApexOptions } from 'apexcharts';
import {
  mergeChartOptions,
  AREA_CHART_OPTIONS,
  DONUT_CHART_OPTIONS,
  BAR_CHART_OPTIONS,
  LINE_CHART_OPTIONS,
  HEATMAP_CHART_OPTIONS,
  CHART_PALETTES,
} from '@/lib/apexcharts-config';

// Dynamically import ApexCharts (client-side only, SSR incompatible)
const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

export interface ApexChartCardProps {
  title: string;
  description?: string;
  type: 'area' | 'donut' | 'bar' | 'line' | 'heatmap';
  series: any[];
  categories?: string[];
  labels?: string[];
  customOptions?: Partial<ApexOptions>;
  colors?: string[];
  loading?: boolean;
  error?: string;
  height?: number;
}

export function ApexChartCard({
  title,
  description,
  type,
  series,
  categories,
  labels,
  customOptions = {},
  colors = CHART_PALETTES.rainbow,
  loading = false,
  error,
  height = 350,
}: ApexChartCardProps) {
  // Loading state
  if (loading) {
    return (
      <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm animate-pulse">
        <div className="h-6 bg-slate-700 rounded w-1/3 mb-2"></div>
        {description && <div className="h-4 bg-slate-700 rounded w-1/2 mb-4"></div>}
        <div className="bg-slate-800 rounded" style={{ height }}></div>
      </Card>
    );
  }

  // Error state
  if (error) {
    return (
      <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm">
        <h3 className="text-lg font-semibold text-slate-200 mb-2">{title}</h3>
        {description && <p className="text-sm text-slate-400 mb-4">{description}</p>}
        <div className="flex items-center justify-center" style={{ height }}>
          <div className="text-center">
            <p className="text-red-400 mb-2">Error loading chart</p>
            <p className="text-sm text-slate-500">{error}</p>
          </div>
        </div>
      </Card>
    );
  }

  // No data state
  if (!series || series.length === 0) {
    return (
      <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm">
        <h3 className="text-lg font-semibold text-slate-200 mb-2">{title}</h3>
        {description && <p className="text-sm text-slate-400 mb-4">{description}</p>}
        <div className="flex items-center justify-center" style={{ height }}>
          <p className="text-slate-500">No data available</p>
        </div>
      </Card>
    );
  }

  // Select base options by chart type
  const getBaseOptions = (): ApexOptions => {
    switch (type) {
      case 'area':
        return AREA_CHART_OPTIONS;
      case 'donut':
        return DONUT_CHART_OPTIONS;
      case 'bar':
        return BAR_CHART_OPTIONS;
      case 'line':
        return LINE_CHART_OPTIONS;
      case 'heatmap':
        return HEATMAP_CHART_OPTIONS;
      default:
        return AREA_CHART_OPTIONS;
    }
  };

  // Build chart options
  const chartOptions: ApexOptions = mergeChartOptions(getBaseOptions(), {
    ...customOptions,
    chart: {
      ...getBaseOptions().chart,
      ...customOptions.chart,
      height,
    },
    colors,
    xaxis: {
      ...getBaseOptions().xaxis,
      ...customOptions.xaxis,
      categories: categories || customOptions.xaxis?.categories,
    },
    labels: labels || customOptions.labels,
  });

  return (
    <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm">
      <h3 className="text-lg font-semibold text-slate-200 mb-2">{title}</h3>
      {description && <p className="text-sm text-slate-400 mb-4">{description}</p>}
      <div className="apexcharts-dark-theme">
        <Chart options={chartOptions} series={series} type={type} height={height} />
      </div>
    </Card>
  );
}

// Export individual chart type components for convenience
export function AreaChartCard(props: Omit<ApexChartCardProps, 'type'>) {
  return <ApexChartCard {...props} type="area" />;
}

export function DonutChartCard(props: Omit<ApexChartCardProps, 'type'>) {
  return <ApexChartCard {...props} type="donut" />;
}

export function BarChartCard(props: Omit<ApexChartCardProps, 'type'>) {
  return <ApexChartCard {...props} type="bar" />;
}

export function LineChartCard(props: Omit<ApexChartCardProps, 'type'>) {
  return <ApexChartCard {...props} type="line" />;
}

export function HeatmapChartCard(props: Omit<ApexChartCardProps, 'type'>) {
  return <ApexChartCard {...props} type="heatmap" />;
}
