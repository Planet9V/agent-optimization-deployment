/**
 * ApexCharts Configuration for AEON Digital Twin
 * Dark theme styling matching OpenCTI and OKLCH color system
 */

import type { ApexOptions } from 'apexcharts';

// OKLCH dark theme colors matching AEON design system
export const CHART_COLORS = {
  primary: '#10b981',     // emerald-500
  secondary: '#06b6d4',   // cyan-500
  danger: '#ef4444',      // red-500
  warning: '#f59e0b',     // amber-500
  success: '#22c55e',     // green-500
  info: '#3b82f6',        // blue-500
  purple: '#a855f7',      // purple-500
  pink: '#ec4899',        // pink-500

  // CVE severity colors (matching CVEDetails integration)
  critical: '#d32f2f',
  high: '#f57c00',
  medium: '#fbc02d',
  low: '#388e3c',
} as const;

// Chart color palettes for different visualization types
export const CHART_PALETTES = {
  threat: [CHART_COLORS.critical, CHART_COLORS.high, CHART_COLORS.medium, CHART_COLORS.low],
  performance: [CHART_COLORS.primary, CHART_COLORS.secondary, CHART_COLORS.info],
  status: [CHART_COLORS.success, CHART_COLORS.warning, CHART_COLORS.danger],
  rainbow: [
    CHART_COLORS.primary,
    CHART_COLORS.secondary,
    CHART_COLORS.purple,
    CHART_COLORS.pink,
    CHART_COLORS.warning,
    CHART_COLORS.danger,
  ],
};

// Base configuration for all ApexCharts (dark theme)
export const BASE_CHART_OPTIONS: ApexOptions = {
  chart: {
    background: 'transparent',
    foreColor: '#cbd5e1', // slate-300
    fontFamily: 'Inter, system-ui, sans-serif',
    toolbar: {
      show: true,
      tools: {
        download: true,
        selection: true,
        zoom: true,
        zoomin: true,
        zoomout: true,
        pan: true,
        reset: true,
      },
      export: {
        csv: {
          filename: 'aeon-data',
        },
        svg: {
          filename: 'aeon-chart',
        },
        png: {
          filename: 'aeon-chart',
        },
      },
    },
    zoom: {
      enabled: true,
    },
    animations: {
      enabled: true,
      speed: 800,
      animateGradually: {
        enabled: true,
        delay: 150,
      },
      dynamicAnimation: {
        enabled: true,
        speed: 350,
      },
    },
  },
  theme: {
    mode: 'dark',
    palette: 'palette1',
  },
  grid: {
    borderColor: '#334155', // slate-700
    strokeDashArray: 2,
    xaxis: {
      lines: {
        show: true,
      },
    },
    yaxis: {
      lines: {
        show: true,
      },
    },
    padding: {
      top: 0,
      right: 10,
      bottom: 0,
      left: 10,
    },
  },
  xaxis: {
    labels: {
      style: {
        colors: '#94a3b8', // slate-400
        fontSize: '12px',
      },
    },
    axisBorder: {
      show: true,
      color: '#475569', // slate-600
    },
    axisTicks: {
      show: true,
      color: '#475569',
    },
  },
  yaxis: {
    labels: {
      style: {
        colors: '#94a3b8',
        fontSize: '12px',
      },
    },
  },
  tooltip: {
    theme: 'dark',
    style: {
      fontSize: '12px',
    },
    x: {
      show: true,
    },
    y: {
      formatter: undefined, // Override per chart type
    },
  },
  legend: {
    labels: {
      colors: '#cbd5e1', // slate-300
    },
    fontSize: '13px',
    fontWeight: 400,
  },
  dataLabels: {
    enabled: false, // Override per chart type
    style: {
      fontSize: '11px',
      fontWeight: 500,
      colors: ['#f8fafc'], // slate-50
    },
  },
  stroke: {
    curve: 'smooth',
    width: 2,
  },
};

// Area chart configuration (for time series data)
export const AREA_CHART_OPTIONS: ApexOptions = {
  ...BASE_CHART_OPTIONS,
  chart: {
    ...BASE_CHART_OPTIONS.chart,
    type: 'area',
    height: 350,
  },
  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 1,
      opacityFrom: 0.7,
      opacityTo: 0.2,
      stops: [0, 90, 100],
    },
  },
  stroke: {
    curve: 'smooth',
    width: 2,
  },
};

// Donut chart configuration (for categorical distribution)
export const DONUT_CHART_OPTIONS: ApexOptions = {
  ...BASE_CHART_OPTIONS,
  chart: {
    ...BASE_CHART_OPTIONS.chart,
    type: 'donut',
    height: 350,
  },
  dataLabels: {
    enabled: true,
    formatter: (val: number) => `${val.toFixed(1)}%`,
    style: {
      fontSize: '12px',
      fontWeight: 600,
      colors: ['#f8fafc'],
    },
    dropShadow: {
      enabled: false,
    },
  },
  plotOptions: {
    pie: {
      donut: {
        size: '65%',
        labels: {
          show: true,
          name: {
            show: true,
            fontSize: '16px',
            fontWeight: 600,
            color: '#cbd5e1',
          },
          value: {
            show: true,
            fontSize: '24px',
            fontWeight: 700,
            color: '#e2e8f0',
            formatter: (val: string) => Number(val).toLocaleString(),
          },
          total: {
            show: true,
            label: 'Total',
            fontSize: '14px',
            fontWeight: 500,
            color: '#94a3b8',
            formatter: (w) => {
              const total = w.globals.seriesTotals.reduce((a: number, b: number) => a + b, 0);
              return total.toLocaleString();
            },
          },
        },
      },
    },
  },
  stroke: {
    width: 0,
  },
};

// Bar chart configuration (for comparisons)
export const BAR_CHART_OPTIONS: ApexOptions = {
  ...BASE_CHART_OPTIONS,
  chart: {
    ...BASE_CHART_OPTIONS.chart,
    type: 'bar',
    height: 350,
  },
  plotOptions: {
    bar: {
      borderRadius: 4,
      horizontal: false,
      columnWidth: '60%',
      dataLabels: {
        position: 'top',
      },
    },
  },
  dataLabels: {
    enabled: false,
  },
};

// Line chart configuration (for trends)
export const LINE_CHART_OPTIONS: ApexOptions = {
  ...BASE_CHART_OPTIONS,
  chart: {
    ...BASE_CHART_OPTIONS.chart,
    type: 'line',
    height: 350,
  },
  stroke: {
    curve: 'smooth',
    width: 3,
  },
  markers: {
    size: 4,
    strokeColors: '#10b981',
    strokeWidth: 2,
    hover: {
      size: 6,
    },
  },
};

// Heatmap chart configuration (for matrix data)
export const HEATMAP_CHART_OPTIONS: ApexOptions = {
  ...BASE_CHART_OPTIONS,
  chart: {
    ...BASE_CHART_OPTIONS.chart,
    type: 'heatmap',
    height: 350,
  },
  dataLabels: {
    enabled: false,
  },
  plotOptions: {
    heatmap: {
      shadeIntensity: 0.5,
      radius: 2,
      colorScale: {
        ranges: [
          {
            from: 0,
            to: 25,
            color: CHART_COLORS.low,
            name: 'Low',
          },
          {
            from: 26,
            to: 50,
            color: CHART_COLORS.medium,
            name: 'Medium',
          },
          {
            from: 51,
            to: 75,
            color: CHART_COLORS.high,
            name: 'High',
          },
          {
            from: 76,
            to: 100,
            color: CHART_COLORS.critical,
            name: 'Critical',
          },
        ],
      },
    },
  },
};

// Helper function to merge custom options with base config
export function mergeChartOptions(
  baseOptions: ApexOptions,
  customOptions: Partial<ApexOptions> = {}
): ApexOptions {
  return {
    ...baseOptions,
    ...customOptions,
    chart: {
      ...baseOptions.chart,
      ...customOptions.chart,
    },
    colors: customOptions.colors || [...CHART_PALETTES.rainbow],
  };
}

// Export all configurations
export default {
  BASE_CHART_OPTIONS,
  AREA_CHART_OPTIONS,
  DONUT_CHART_OPTIONS,
  BAR_CHART_OPTIONS,
  LINE_CHART_OPTIONS,
  HEATMAP_CHART_OPTIONS,
  CHART_COLORS,
  CHART_PALETTES,
  mergeChartOptions,
};
