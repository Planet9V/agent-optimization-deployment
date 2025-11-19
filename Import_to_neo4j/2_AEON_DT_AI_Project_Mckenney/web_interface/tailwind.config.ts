import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: 'class',
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './node_modules/@tremor/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // VulnCheck Dark Theme Colors (OKLCH)
        vulncheck: {
          bg: {
            primary: 'oklch(12.9% 0.042 264.695)',    // slate-950
            secondary: 'oklch(20.8% 0.042 265.755)',  // slate-900
            tertiary: 'oklch(25% 0.042 265)',
            elevated: 'oklch(30% 0.042 265)',
          },
          emerald: {
            400: 'oklch(74.6% 0.17 162.48)',
            500: 'oklch(69.6% 0.17 162.48)',  // Main brand color
            600: 'oklch(64.2% 0.17 162.48)',
            700: 'oklch(58.8% 0.17 162.48)',
          },
          text: {
            primary: 'oklch(98.3% 0.003 264.052)',    // slate-50
            secondary: 'oklch(90% 0.012 264)',
            tertiary: 'oklch(70% 0.018 264)',
            muted: 'oklch(55% 0.020 264)',
          },
          border: {
            default: 'oklch(35% 0.015 265)',
            subtle: 'oklch(25% 0.012 265)',
            strong: 'oklch(45% 0.018 265)',
            emerald: 'oklch(69.6% 0.17 162.48)',
          },
          severity: {
            critical: {
              DEFAULT: 'oklch(65% 0.24 25)',
              bg: 'oklch(20% 0.08 25)',
              border: 'oklch(40% 0.15 25)',
            },
            high: {
              DEFAULT: 'oklch(72% 0.18 45)',
              bg: 'oklch(20% 0.06 45)',
              border: 'oklch(45% 0.12 45)',
            },
            medium: {
              DEFAULT: 'oklch(78% 0.15 85)',
              bg: 'oklch(22% 0.05 85)',
              border: 'oklch(50% 0.10 85)',
            },
            low: {
              DEFAULT: 'oklch(72% 0.15 240)',
              bg: 'oklch(20% 0.05 240)',
              border: 'oklch(45% 0.10 240)',
            },
            info: {
              DEFAULT: 'oklch(70% 0.14 162)',
              bg: 'oklch(20% 0.05 162)',
              border: 'oklch(45% 0.10 162)',
            },
          },
        },
        // Standard Tailwind colors extended with OKLCH
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        slate: {
          50: 'oklch(98.3% 0.003 264.052)',
          100: 'oklch(96.5% 0.007 256.848)',
          200: 'oklch(92.6% 0.013 255.508)',
          300: 'oklch(86.5% 0.016 254.604)',
          400: 'oklch(71.2% 0.019 256.802)',
          500: 'oklch(56.1% 0.016 257.417)',
          600: 'oklch(45.1% 0.017 257.281)',
          700: 'oklch(37.1% 0.015 257.287)',
          800: 'oklch(27.8% 0.013 260.031)',
          900: 'oklch(20.8% 0.042 265.755)',   // VulnCheck secondary bg
          950: 'oklch(12.9% 0.042 264.695)',   // VulnCheck primary bg
        },
        emerald: {
          50: 'oklch(97.5% 0.025 166.11)',
          100: 'oklch(94.4% 0.054 162.48)',
          200: 'oklch(88.7% 0.101 162.48)',
          300: 'oklch(81.3% 0.142 162.48)',
          400: 'oklch(74.6% 0.17 162.48)',     // VulnCheck hover
          500: 'oklch(69.6% 0.17 162.48)',     // VulnCheck primary accent
          600: 'oklch(64.2% 0.17 162.48)',
          700: 'oklch(58.8% 0.17 162.48)',
          800: 'oklch(50.9% 0.141 162.48)',
          900: 'oklch(44.3% 0.107 164.103)',
          950: 'oklch(27.6% 0.079 169.711)',
        },
        blue: {
          500: 'oklch(68% 0.18 240)',
        },
        green: {
          500: 'oklch(70% 0.14 162)',
        },
        yellow: {
          500: 'oklch(78% 0.15 85)',
        },
        red: {
          500: 'oklch(65% 0.24 25)',
        },
      },
      borderRadius: {
        'vc-sm': '0.25rem',
        'vc-md': '0.5rem',
        'vc-lg': '0.75rem',
        'vc-xl': '1rem',
      },
      boxShadow: {
        'vc-sm': '0 1px 2px 0 oklch(0% 0 0 / 0.3)',
        'vc-md': '0 4px 6px -1px oklch(0% 0 0 / 0.4), 0 2px 4px -1px oklch(0% 0 0 / 0.3)',
        'vc-lg': '0 10px 15px -3px oklch(0% 0 0 / 0.5), 0 4px 6px -2px oklch(0% 0 0 / 0.4)',
        'vc-xl': '0 20px 25px -5px oklch(0% 0 0 / 0.6), 0 10px 10px -5px oklch(0% 0 0 / 0.5)',
        'glow-emerald': '0 0 20px oklch(69.6% 0.17 162.48 / 0.3)',
        'glow-critical': '0 0 20px oklch(65% 0.24 25 / 0.3)',
      },
      animation: {
        'wave': 'wave 10s ease-in-out infinite',
        'wave-slow': 'wave 15s ease-in-out infinite',
        'wave-fast': 'wave 7s ease-in-out infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'skeleton': 'skeleton 1.5s ease-in-out infinite',
        'fade-in': 'fadeIn 0.3s ease-in',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
      },
      keyframes: {
        wave: {
          '0%, 100%': {
            transform: 'translateY(0) translateX(0)',
          },
          '25%': {
            transform: 'translateY(-10px) translateX(10px)',
          },
          '50%': {
            transform: 'translateY(-5px) translateX(-5px)',
          },
          '75%': {
            transform: 'translateY(-15px) translateX(5px)',
          },
        },
        skeleton: {
          '0%': {
            backgroundPosition: '200% 0',
          },
          '100%': {
            backgroundPosition: '-200% 0',
          },
        },
        fadeIn: {
          '0%': {
            opacity: '0',
          },
          '100%': {
            opacity: '1',
          },
        },
        slideUp: {
          '0%': {
            transform: 'translateY(10px)',
            opacity: '0',
          },
          '100%': {
            transform: 'translateY(0)',
            opacity: '1',
          },
        },
        slideDown: {
          '0%': {
            transform: 'translateY(-10px)',
            opacity: '0',
          },
          '100%': {
            transform: 'translateY(0)',
            opacity: '1',
          },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-cyber': 'linear-gradient(135deg, oklch(64.2% 0.17 162.48), oklch(69.6% 0.17 162.48))',
        'gradient-threat': 'linear-gradient(135deg, oklch(65% 0.24 25), oklch(72% 0.18 45))',
      },
      spacing: {
        'vc-1': '0.25rem',
        'vc-2': '0.5rem',
        'vc-3': '0.75rem',
        'vc-4': '1rem',
        'vc-6': '1.5rem',
        'vc-8': '2rem',
        'vc-12': '3rem',
        'vc-16': '4rem',
      },
      transitionDuration: {
        'vc-fast': '150ms',
        'vc-base': '200ms',
        'vc-slow': '300ms',
      },
      fontSize: {
        'vc-xs': ['0.75rem', { lineHeight: '1rem', letterSpacing: '0.05em' }],
        'vc-sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'vc-base': ['1rem', { lineHeight: '1.5rem' }],
        'vc-lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'vc-xl': ['1.25rem', { lineHeight: '1.75rem' }],
        'vc-2xl': ['1.5rem', { lineHeight: '2rem' }],
      },
    },
  },
  plugins: [
    // Custom plugin for VulnCheck utilities
    function({ addUtilities, theme }: any) {
      const newUtilities = {
        '.glass-effect': {
          background: 'oklch(25% 0.042 265 / 0.6)',
          backdropFilter: 'blur(12px)',
          WebkitBackdropFilter: 'blur(12px)',
          border: '1px solid oklch(45% 0.018 265 / 0.2)',
        },
        '.text-gradient-cyber': {
          background: 'linear-gradient(135deg, oklch(74.6% 0.17 162.48), oklch(64.2% 0.17 162.48))',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
        },
      };
      addUtilities(newUtilities);
    },
  ],
};

export default config;
