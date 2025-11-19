/**
 * Leaflet Configuration for Next.js
 * Fixes icon paths and SSR issues
 */

// Conditionally import Leaflet only on client-side
let L: typeof import('leaflet') | undefined;

if (typeof window !== 'undefined') {
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  L = require('leaflet');
}

// Fix Leaflet default icon paths for Next.js
export function fixLeafletIcons() {
  if (typeof window !== 'undefined' && L) {
    // @ts-expect-error - Leaflet type definitions don't include _getIconUrl
    delete L.Icon.Default.prototype._getIconUrl;

    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
      iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
      shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    });
  }
}

// Dark theme tile layer configuration
export const DARK_TILE_LAYER = {
  url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
  attribution: '&copy; <a href="https://carto.com/">CARTO</a>',
};

// Threat severity color mapping (matches CVE severity colors)
export const THREAT_COLORS = {
  critical: '#d32f2f',
  high: '#f57c00',
  medium: '#fbc02d',
  low: '#388e3c',
  info: '#1976d2',
} as const;

export type ThreatLevel = keyof typeof THREAT_COLORS;

// Get marker radius based on threat count
export function getMarkerRadius(count: number): number {
  return Math.min(Math.max(Math.sqrt(count) * 2, 8), 40);
}

// Get marker color based on threat level
export function getMarkerColor(level: ThreatLevel): string {
  return THREAT_COLORS[level];
}
