'use client';

import React from 'react';

/**
 * Wave Background Component
 * Animated wave effect for VulnCheck-inspired dashboard
 *
 * File: wave-background.tsx
 * Created: 2025-11-04
 * Version: 1.0.0
 */

export interface WaveBackgroundProps {
  /** Number of wave layers (1-5) */
  layers?: 1 | 2 | 3 | 4 | 5;
  /** Animation speed variant */
  speed?: 'slow' | 'normal' | 'fast';
  /** Wave color theme */
  variant?: 'emerald' | 'cyber' | 'threat' | 'muted';
  /** Additional CSS classes */
  className?: string;
  /** Z-index of the wave container */
  zIndex?: number;
}

const variantColors = {
  emerald: {
    primary: 'rgba(52, 211, 153, 0.08)',    // emerald-500 with low opacity
    secondary: 'rgba(52, 211, 153, 0.05)',
    tertiary: 'rgba(52, 211, 153, 0.03)',
  },
  cyber: {
    primary: 'rgba(52, 211, 153, 0.1)',
    secondary: 'rgba(34, 197, 94, 0.07)',
    tertiary: 'rgba(59, 130, 246, 0.05)',
  },
  threat: {
    primary: 'rgba(239, 68, 68, 0.08)',
    secondary: 'rgba(249, 115, 22, 0.06)',
    tertiary: 'rgba(234, 179, 8, 0.04)',
  },
  muted: {
    primary: 'rgba(148, 163, 184, 0.05)',
    secondary: 'rgba(148, 163, 184, 0.03)',
    tertiary: 'rgba(148, 163, 184, 0.02)',
  },
};

const speedVariants = {
  slow: ['animate-wave-slow', '15s'],
  normal: ['animate-wave', '10s'],
  fast: ['animate-wave-fast', '7s'],
};

export function WaveBackground({
  layers = 3,
  speed = 'normal',
  variant = 'emerald',
  className = '',
  zIndex = 0,
}: WaveBackgroundProps) {
  const colors = variantColors[variant];
  const [animationClass, duration] = speedVariants[speed];

  // Generate SVG paths for wave shapes
  const generateWavePath = (offset: number, amplitude: number) => {
    const points = 100;
    const path = Array.from({ length: points }, (_, i) => {
      const x = (i / points) * 100;
      const y = 50 + Math.sin((i / points) * Math.PI * 4 + offset) * amplitude;
      return `${x},${y}`;
    }).join(' ');

    return `M 0,50 L ${path} L 100,100 L 0,100 Z`;
  };

  const renderWaveLayer = (index: number) => {
    const delay = index * 0.5;
    const offset = index * 0.7;
    const amplitude = 8 - index * 1.5;

    const colorKey = index === 0 ? 'primary' : index === 1 ? 'secondary' : 'tertiary';
    const color = colors[colorKey];

    return (
      <svg
        key={index}
        className={`absolute inset-0 w-full h-full ${animationClass}`}
        style={{
          animationDelay: `${delay}s`,
          opacity: 1 - (index * 0.2),
        }}
        viewBox="0 0 100 100"
        preserveAspectRatio="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d={generateWavePath(offset, amplitude)}
          fill={color}
          className="transition-all duration-1000"
        />
      </svg>
    );
  };

  return (
    <div
      className={`absolute inset-0 overflow-hidden pointer-events-none ${className}`}
      style={{ zIndex }}
      aria-hidden="true"
    >
      {Array.from({ length: Math.min(layers, 5) }, (_, i) => renderWaveLayer(i))}
    </div>
  );
}

/**
 * Radial Gradient Background
 * Subtle radial gradient effect for depth
 */
export interface RadialGradientProps {
  /** Gradient color variant */
  variant?: 'emerald' | 'blue' | 'purple' | 'red';
  /** Gradient position */
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'center';
  /** Opacity (0-1) */
  opacity?: number;
  /** Additional CSS classes */
  className?: string;
}

const gradientPositions = {
  'top-left': 'radial-gradient(circle at top left, var(--gradient-color), transparent 50%)',
  'top-right': 'radial-gradient(circle at top right, var(--gradient-color), transparent 50%)',
  'bottom-left': 'radial-gradient(circle at bottom left, var(--gradient-color), transparent 50%)',
  'bottom-right': 'radial-gradient(circle at bottom right, var(--gradient-color), transparent 50%)',
  'center': 'radial-gradient(circle at center, var(--gradient-color), transparent 60%)',
};

const gradientColors = {
  emerald: 'oklch(69.6% 0.17 162.48 / 0.15)',
  blue: 'oklch(68% 0.18 240 / 0.15)',
  purple: 'oklch(70% 0.18 290 / 0.15)',
  red: 'oklch(65% 0.24 25 / 0.15)',
};

export function RadialGradient({
  variant = 'emerald',
  position = 'top-right',
  opacity = 1,
  className = '',
}: RadialGradientProps) {
  const gradientStyle = gradientPositions[position];
  const color = gradientColors[variant];

  return (
    <div
      className={`absolute inset-0 pointer-events-none ${className}`}
      style={{
        background: gradientStyle.replace('var(--gradient-color)', color),
        opacity,
      }}
      aria-hidden="true"
    />
  );
}

/**
 * Grid Pattern Background
 * Subtle grid pattern for tech aesthetic
 */
export interface GridPatternProps {
  /** Grid size in pixels */
  size?: number;
  /** Grid line color (OKLCH format) */
  color?: string;
  /** Grid line width in pixels */
  strokeWidth?: number;
  /** Additional CSS classes */
  className?: string;
}

export function GridPattern({
  size = 32,
  color = 'oklch(35% 0.015 265 / 0.3)',
  strokeWidth = 1,
  className = '',
}: GridPatternProps) {
  return (
    <div className={`absolute inset-0 pointer-events-none ${className}`} aria-hidden="true">
      <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <pattern id="grid" width={size} height={size} patternUnits="userSpaceOnUse">
            <path
              d={`M ${size} 0 L 0 0 0 ${size}`}
              fill="none"
              stroke={color}
              strokeWidth={strokeWidth}
            />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
      </svg>
    </div>
  );
}

/**
 * Combined Background
 * Composition of multiple background effects
 */
export interface CombinedBackgroundProps {
  /** Include wave animation */
  waves?: boolean;
  /** Wave configuration */
  waveProps?: WaveBackgroundProps;
  /** Include radial gradient */
  gradient?: boolean;
  /** Gradient configuration */
  gradientProps?: RadialGradientProps;
  /** Include grid pattern */
  grid?: boolean;
  /** Grid configuration */
  gridProps?: GridPatternProps;
  /** Additional CSS classes */
  className?: string;
}

export function CombinedBackground({
  waves = true,
  waveProps = {},
  gradient = true,
  gradientProps = {},
  grid = false,
  gridProps = {},
  className = '',
}: CombinedBackgroundProps) {
  return (
    <div className={`relative ${className}`}>
      {grid && <GridPattern {...gridProps} />}
      {gradient && <RadialGradient {...gradientProps} />}
      {waves && <WaveBackground {...waveProps} />}
    </div>
  );
}

export default WaveBackground;
