'use client';

import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import { Card, Title } from '@tremor/react';
import { MapPin, AlertTriangle } from 'lucide-react';

// Dynamically import Leaflet components (client-side only)
const MapContainer = dynamic(
  () => import('react-leaflet').then((mod) => mod.MapContainer),
  { ssr: false }
);

const TileLayer = dynamic(
  () => import('react-leaflet').then((mod) => mod.TileLayer),
  { ssr: false }
);

const CircleMarker = dynamic(
  () => import('react-leaflet').then((mod) => mod.CircleMarker),
  { ssr: false }
);

const Popup = dynamic(
  () => import('react-leaflet').then((mod) => mod.Popup),
  { ssr: false }
);

// Import Leaflet config (CSS imported dynamically in useEffect)
import {
  fixLeafletIcons,
  DARK_TILE_LAYER,
  getMarkerRadius,
  getMarkerColor,
  type ThreatLevel
} from '@/lib/leaflet-config';

export interface ThreatLocation {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  threatLevel: ThreatLevel;
  count: number;
  types: string[];
}

interface WorldMapProps {
  threats?: ThreatLocation[];
  loading?: boolean;
}

export default function WorldMap({ threats: initialThreats, loading: initialLoading = false }: WorldMapProps) {
  const [threats, setThreats] = useState<ThreatLocation[]>(initialThreats || [
    // Default demo data
    { id: '1', name: 'North America', latitude: 40.7128, longitude: -74.0060, threatLevel: 'high', count: 342, types: ['Malware', 'Phishing'] },
    { id: '2', name: 'Europe', latitude: 51.5074, longitude: -0.1278, threatLevel: 'critical', count: 567, types: ['APT', 'Ransomware'] },
    { id: '3', name: 'Asia-Pacific', latitude: 35.6762, longitude: 139.6503, threatLevel: 'high', count: 423, types: ['DDoS', 'Data Breach'] },
    { id: '4', name: 'Middle East', latitude: 25.2048, longitude: 55.2708, threatLevel: 'medium', count: 234, types: ['State-Sponsored'] },
    { id: '5', name: 'South America', latitude: -23.5505, longitude: -46.6333, threatLevel: 'medium', count: 178, types: ['Banking Trojans'] },
    { id: '6', name: 'Africa', latitude: -1.2921, longitude: 36.8219, threatLevel: 'low', count: 89, types: ['Mobile Malware'] },
  ]);

  const [loading, setLoading] = useState(initialLoading);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);

    // Dynamically load Leaflet CSS only on client-side
    if (typeof window !== 'undefined') {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
      document.head.appendChild(link);
    }

    fixLeafletIcons();

    // Fetch real threat data if not provided
    if (!initialThreats) {
      const fetchThreatData = async () => {
        try {
          const response = await fetch('/api/threats/geographic');
          if (response.ok) {
            const data = await response.json();
            setThreats(data.threats || threats);
          }
        } catch (error) {
          console.log('Using default threat data');
        } finally {
          setLoading(false);
        }
      };

      fetchThreatData();
    }
  }, [initialThreats]);

  if (!isClient) {
    return (
      <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm">
        <div className="flex items-center gap-2 mb-4">
          <MapPin className="h-5 w-5 text-emerald-500" />
          <Title className="text-slate-200">Geographic Threat Map</Title>
        </div>
        <div className="h-[600px] flex items-center justify-center bg-slate-950/50 rounded-lg">
          <div className="text-slate-400 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500 mx-auto mb-4"></div>
            <p>Loading world map...</p>
          </div>
        </div>
      </Card>
    );
  }

  if (loading) {
    return (
      <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm">
        <div className="flex items-center gap-2 mb-4">
          <MapPin className="h-5 w-5 text-emerald-500" />
          <Title className="text-slate-200">Geographic Threat Map</Title>
        </div>
        <div className="h-[600px] flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500"></div>
        </div>
      </Card>
    );
  }

  return (
    <Card className="bg-slate-900/50 border-slate-800 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <MapPin className="h-5 w-5 text-emerald-500" />
          <Title className="text-slate-200">Geographic Threat Map</Title>
        </div>
        <div className="flex items-center gap-2 text-sm text-slate-400">
          <AlertTriangle className="h-4 w-4 text-amber-500" />
          <span>{threats.reduce((sum, t) => sum + t.count, 0).toLocaleString()} threats detected</span>
        </div>
      </div>

      <div className="h-[600px] rounded-lg overflow-hidden border border-slate-700">
        <MapContainer
          center={[20, 0]}
          zoom={2}
          style={{ height: '100%', width: '100%', background: '#0f172a' }}
          zoomControl={true}
          scrollWheelZoom={true}
        >
          <TileLayer
            url={DARK_TILE_LAYER.url}
            attribution={DARK_TILE_LAYER.attribution}
          />

          {threats.map((threat) => (
            <CircleMarker
              key={threat.id}
              center={[threat.latitude, threat.longitude]}
              radius={getMarkerRadius(threat.count)}
              pathOptions={{
                fillColor: getMarkerColor(threat.threatLevel),
                color: '#ffffff',
                weight: 1,
                opacity: 0.8,
                fillOpacity: 0.6,
              }}
            >
              <Popup>
                <div className="p-2 min-w-[200px]">
                  <h3 className="font-bold text-lg mb-2 text-slate-900">{threat.name}</h3>
                  <div className="space-y-1 text-sm">
                    <p>
                      <span className="font-semibold">Threat Level:</span>{' '}
                      <span
                        className="px-2 py-1 rounded text-white text-xs font-bold"
                        style={{ backgroundColor: getMarkerColor(threat.threatLevel) }}
                      >
                        {threat.threatLevel.toUpperCase()}
                      </span>
                    </p>
                    <p>
                      <span className="font-semibold">Incidents:</span> {threat.count.toLocaleString()}
                    </p>
                    <p>
                      <span className="font-semibold">Types:</span> {threat.types.join(', ')}
                    </p>
                  </div>
                </div>
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>

      {/* Legend */}
      <div className="mt-4 flex items-center gap-6 text-sm">
        <span className="text-slate-400 font-semibold">Threat Levels:</span>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#d32f2f' }}></div>
          <span className="text-slate-300">Critical</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#f57c00' }}></div>
          <span className="text-slate-300">High</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#fbc02d' }}></div>
          <span className="text-slate-300">Medium</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#388e3c' }}></div>
          <span className="text-slate-300">Low</span>
        </div>
      </div>
    </Card>
  );
}
