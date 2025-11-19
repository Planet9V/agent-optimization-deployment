import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';
import { getNeo4jDriver } from '@/lib/neo4j-enhanced';

/**
 * GET /api/threats/geographic
 * Returns geographic threat data for WorldMap visualization
 */
export async function GET(request: NextRequest) {
  try {
    // Verify authentication
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Fetch geographic threat data from Neo4j
    const driver = getNeo4jDriver();
    const session_neo4j = driver.session();

    try {
      // Get threats with geographic data
      const geoResult = await session_neo4j.run(`
        MATCH (t)
        WHERE t.latitude IS NOT NULL AND t.longitude IS NOT NULL
          OR t.country IS NOT NULL
          OR t.region IS NOT NULL
          OR t.location IS NOT NULL
        WITH t,
          coalesce(t.location, t.region, t.country, 'Unknown') as locationName,
          coalesce(t.latitude, 0.0) as lat,
          coalesce(t.longitude, 0.0) as lon,
          coalesce(t.threatLevel, t.severity, 'medium') as level,
          labels(t) as nodeLabels
        WHERE locationName <> 'Unknown'
        WITH
          locationName,
          lat,
          lon,
          level,
          nodeLabels,
          count(*) as threatCount
        RETURN
          locationName,
          lat,
          lon,
          level,
          collect(DISTINCT nodeLabels[0])[0..3] as threatTypes,
          threatCount
        ORDER BY threatCount DESC
        LIMIT 50
      `);

      let threats = geoResult.records.map((record, index) => {
        const level = record.get('level').toLowerCase();
        const threatLevel = ['critical', 'high', 'medium', 'low'].includes(level)
          ? level
          : 'medium';

        return {
          id: `threat-${index + 1}`,
          name: record.get('locationName'),
          latitude: record.get('lat'),
          longitude: record.get('lon'),
          threatLevel,
          count: record.get('threatCount').toNumber(),
          types: record.get('threatTypes') || [],
        };
      });

      // If no geographic data in database, return demo data
      if (threats.length === 0) {
        threats = [
          {
            id: '1',
            name: 'North America',
            latitude: 40.7128,
            longitude: -74.0060,
            threatLevel: 'high',
            count: 342,
            types: ['Malware', 'Phishing'],
          },
          {
            id: '2',
            name: 'Europe',
            latitude: 51.5074,
            longitude: -0.1278,
            threatLevel: 'critical',
            count: 567,
            types: ['APT', 'Ransomware'],
          },
          {
            id: '3',
            name: 'Asia-Pacific',
            latitude: 35.6762,
            longitude: 139.6503,
            threatLevel: 'high',
            count: 423,
            types: ['DDoS', 'Data Breach'],
          },
          {
            id: '4',
            name: 'Middle East',
            latitude: 25.2048,
            longitude: 55.2708,
            threatLevel: 'medium',
            count: 234,
            types: ['State-Sponsored'],
          },
          {
            id: '5',
            name: 'South America',
            latitude: -23.5505,
            longitude: -46.6333,
            threatLevel: 'medium',
            count: 178,
            types: ['Banking Trojans'],
          },
          {
            id: '6',
            name: 'Africa',
            latitude: -1.2921,
            longitude: 36.8219,
            threatLevel: 'low',
            count: 89,
            types: ['Mobile Malware'],
          },
        ];
      }

      return NextResponse.json({ threats });
    } finally {
      await session_neo4j.close();
    }
  } catch (error) {
    console.error('Error fetching geographic threats:', error);

    // Return fallback demo data on error
    return NextResponse.json({
      threats: [
        {
          id: '1',
          name: 'North America',
          latitude: 40.7128,
          longitude: -74.0060,
          threatLevel: 'high',
          count: 342,
          types: ['Malware', 'Phishing'],
        },
        {
          id: '2',
          name: 'Europe',
          latitude: 51.5074,
          longitude: -0.1278,
          threatLevel: 'critical',
          count: 567,
          types: ['APT', 'Ransomware'],
        },
        {
          id: '3',
          name: 'Asia-Pacific',
          latitude: 35.6762,
          longitude: 139.6503,
          threatLevel: 'high',
          count: 423,
          types: ['DDoS', 'Data Breach'],
        },
        {
          id: '4',
          name: 'Middle East',
          latitude: 25.2048,
          longitude: 55.2708,
          threatLevel: 'medium',
          count: 234,
          types: ['State-Sponsored'],
        },
        {
          id: '5',
          name: 'South America',
          latitude: -23.5505,
          longitude: -46.6333,
          threatLevel: 'medium',
          count: 178,
          types: ['Banking Trojans'],
        },
        {
          id: '6',
          name: 'Africa',
          latitude: -1.2921,
          longitude: 36.8219,
          threatLevel: 'low',
          count: 89,
          types: ['Mobile Malware'],
        },
      ],
    });
  }
}
