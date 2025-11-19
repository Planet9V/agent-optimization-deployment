/**
 * Design Tokens
 * VulnCheck-Inspired Design System for AEON Digital Twin
 *
 * File: design-tokens.ts
 * Created: 2025-11-04
 * Version: 1.0.0
 *
 * Type-safe design tokens for consistent theming across the application.
 * All colors use OKLCH color space for perceptual uniformity.
 */

export const designTokens = {
  /** Color palette using OKLCH color space */
  colors: {
    /** Background colors - Dark slate theme */
    background: {
      primary: 'oklch(12.9% 0.042 264.695)',     // slate-950 - Deepest
      secondary: 'oklch(20.8% 0.042 265.755)',   // slate-900 - Cards
      tertiary: 'oklch(25% 0.042 265)',          // Panels
      elevated: 'oklch(30% 0.042 265)',          // Hover states
    },

    /** Emerald accent colors - Primary brand */
    emerald: {
      400: 'oklch(74.6% 0.17 162.48)',  // Lighter - hover
      500: 'oklch(69.6% 0.17 162.48)',  // Main accent
      600: 'oklch(64.2% 0.17 162.48)',  // Darker
      700: 'oklch(58.8% 0.17 162.48)',  // Darkest
    },

    /** Text colors - High contrast on dark */
    text: {
      primary: 'oklch(98.3% 0.003 264.052)',    // slate-50 - Highest contrast
      secondary: 'oklch(90% 0.012 264)',        // Slightly dimmed
      tertiary: 'oklch(70% 0.018 264)',         // Muted
      muted: 'oklch(55% 0.020 264)',            // Very muted
    },

    /** Border colors */
    border: {
      default: 'oklch(35% 0.015 265)',
      subtle: 'oklch(25% 0.012 265)',
      strong: 'oklch(45% 0.018 265)',
      emerald: 'oklch(69.6% 0.17 162.48)',
    },

    /** Severity levels for CVE/threat indicators */
    severity: {
      critical: {
        color: 'oklch(65% 0.24 25)',
        bg: 'oklch(20% 0.08 25)',
        border: 'oklch(40% 0.15 25)',
      },
      high: {
        color: 'oklch(72% 0.18 45)',
        bg: 'oklch(20% 0.06 45)',
        border: 'oklch(45% 0.12 45)',
      },
      medium: {
        color: 'oklch(78% 0.15 85)',
        bg: 'oklch(22% 0.05 85)',
        border: 'oklch(50% 0.10 85)',
      },
      low: {
        color: 'oklch(72% 0.15 240)',
        bg: 'oklch(20% 0.05 240)',
        border: 'oklch(45% 0.10 240)',
      },
      info: {
        color: 'oklch(70% 0.14 162)',
        bg: 'oklch(20% 0.05 162)',
        border: 'oklch(45% 0.10 162)',
      },
    },

    /** Semantic colors */
    semantic: {
      success: {
        color: 'oklch(69.6% 0.17 162.48)',
        bg: 'oklch(20% 0.06 162)',
        border: 'oklch(45% 0.12 162)',
      },
      warning: {
        color: 'oklch(78% 0.15 75)',
        bg: 'oklch(22% 0.05 75)',
        border: 'oklch(50% 0.10 75)',
      },
      error: {
        color: 'oklch(65% 0.24 25)',
        bg: 'oklch(20% 0.08 25)',
        border: 'oklch(40% 0.15 25)',
      },
    },
  },

  /** Spacing scale */
  spacing: {
    1: '0.25rem',   // 4px
    2: '0.5rem',    // 8px
    3: '0.75rem',   // 12px
    4: '1rem',      // 16px
    6: '1.5rem',    // 24px
    8: '2rem',      // 32px
    12: '3rem',     // 48px
    16: '4rem',     // 64px
  },

  /** Border radius */
  radius: {
    sm: '0.25rem',  // 4px
    md: '0.5rem',   // 8px
    lg: '0.75rem',  // 12px
    xl: '1rem',     // 16px
  },

  /** Box shadows */
  shadows: {
    sm: '0 1px 2px 0 oklch(0% 0 0 / 0.3)',
    md: '0 4px 6px -1px oklch(0% 0 0 / 0.4), 0 2px 4px -1px oklch(0% 0 0 / 0.3)',
    lg: '0 10px 15px -3px oklch(0% 0 0 / 0.5), 0 4px 6px -2px oklch(0% 0 0 / 0.4)',
    xl: '0 20px 25px -5px oklch(0% 0 0 / 0.6), 0 10px 10px -5px oklch(0% 0 0 / 0.5)',
    glowEmerald: '0 0 20px oklch(69.6% 0.17 162.48 / 0.3)',
    glowCritical: '0 0 20px oklch(65% 0.24 25 / 0.3)',
  },

  /** Typography */
  typography: {
    fontFamily: {
      sans: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
      mono: '"SF Mono", "Consolas", "Liberation Mono", "Menlo", monospace',
    },
    fontSize: {
      xs: ['0.75rem', { lineHeight: '1rem', letterSpacing: '0.05em' }],
      sm: ['0.875rem', { lineHeight: '1.25rem' }],
      base: ['1rem', { lineHeight: '1.5rem' }],
      lg: ['1.125rem', { lineHeight: '1.75rem' }],
      xl: ['1.25rem', { lineHeight: '1.75rem' }],
      '2xl': ['1.5rem', { lineHeight: '2rem' }],
      '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
      '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
    },
    fontWeight: {
      normal: '400',
      medium: '500',
      semibold: '600',
      bold: '700',
    },
  },

  /** Transitions */
  transitions: {
    fast: '150ms cubic-bezier(0.4, 0, 0.2, 1)',
    base: '200ms cubic-bezier(0.4, 0, 0.2, 1)',
    slow: '300ms cubic-bezier(0.4, 0, 0.2, 1)',
  },

  /** Z-index scale */
  zIndex: {
    background: -1,
    base: 0,
    dropdown: 1000,
    sticky: 1100,
    fixed: 1200,
    modalBackdrop: 1300,
    modal: 1400,
    popover: 1500,
    tooltip: 1600,
  },
} as const;

/** Severity level type */
export type SeverityLevel = 'critical' | 'high' | 'medium' | 'low' | 'info';

/** Theme variant type */
export type ThemeVariant = 'emerald' | 'cyber' | 'threat' | 'muted';

/** Helper functions for design tokens */
export const designHelpers = {
  /**
   * Get severity colors for a given level
   */
  getSeverityColors(level: SeverityLevel) {
    return designTokens.colors.severity[level];
  },

  /**
   * Get CVSS score severity level
   */
  getCVSSSeverity(score: number): SeverityLevel {
    if (score >= 9.0) return 'critical';
    if (score >= 7.0) return 'high';
    if (score >= 4.0) return 'medium';
    if (score > 0.0) return 'low';
    return 'info';
  },

  /**
   * Format severity text with proper casing
   */
  formatSeverity(level: SeverityLevel): string {
    return level.charAt(0).toUpperCase() + level.slice(1);
  },

  /**
   * Get CSS variable reference
   */
  cssVar(tokenPath: string): string {
    return `var(--vc-${tokenPath})`;
  },
};

/** Component-specific token sets */
export const componentTokens = {
  button: {
    primary: {
      bg: designTokens.colors.emerald[500],
      hover: designTokens.colors.emerald[400],
      active: designTokens.colors.emerald[600],
      text: designTokens.colors.background.primary,
      shadow: designTokens.shadows.sm,
      hoverShadow: designTokens.shadows.glowEmerald,
    },
    secondary: {
      bg: 'transparent',
      hover: 'oklch(20% 0.06 162 / 0.1)',
      active: 'oklch(20% 0.06 162 / 0.2)',
      text: designTokens.colors.text.primary,
      border: designTokens.colors.border.default,
      hoverBorder: designTokens.colors.emerald[500],
    },
  },

  card: {
    bg: designTokens.colors.background.secondary,
    border: designTokens.colors.border.subtle,
    hover: {
      border: designTokens.colors.border.default,
      shadow: designTokens.shadows.md,
      transform: 'translateY(-2px)',
    },
  },

  input: {
    bg: designTokens.colors.background.tertiary,
    border: designTokens.colors.border.default,
    text: designTokens.colors.text.primary,
    placeholder: designTokens.colors.text.muted,
    focus: {
      border: designTokens.colors.emerald[500],
      ring: 'oklch(69.6% 0.17 162.48 / 0.1)',
    },
  },

  badge: {
    padding: `${designTokens.spacing[1]} ${designTokens.spacing[3]}`,
    radius: designTokens.radius.md,
    fontSize: designTokens.typography.fontSize.xs[0],
    fontWeight: designTokens.typography.fontWeight.semibold,
    textTransform: 'uppercase' as const,
    letterSpacing: '0.05em',
  },

  table: {
    header: {
      bg: designTokens.colors.background.tertiary,
      text: designTokens.colors.text.secondary,
      fontSize: designTokens.typography.fontSize.xs[0],
      fontWeight: designTokens.typography.fontWeight.semibold,
    },
    row: {
      border: designTokens.colors.border.subtle,
      hover: designTokens.colors.background.tertiary,
    },
  },
};

/** Animation presets */
export const animations = {
  wave: {
    slow: 'wave 15s ease-in-out infinite',
    normal: 'wave 10s ease-in-out infinite',
    fast: 'wave 7s ease-in-out infinite',
  },
  pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
  skeleton: 'skeleton 1.5s ease-in-out infinite',
  fadeIn: 'fadeIn 0.3s ease-in',
  slideUp: 'slideUp 0.3s ease-out',
  slideDown: 'slideDown 0.3s ease-out',
};

export default designTokens;
