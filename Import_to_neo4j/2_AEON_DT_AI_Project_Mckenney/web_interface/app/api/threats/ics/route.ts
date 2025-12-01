import { NextRequest, NextResponse } from 'next/server';
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://localhost:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USERNAME || 'neo4j',
    process.env.NEO4J_PASSWORD || 'password'
  )
);

export async function GET(request: NextRequest) {
  const session = driver.session();

  try {
    // Query for sector threat data
    const sectorsResult = await session.run(`
      MATCH (t:Threat)-[:TARGETS]->(s:Sector)
      WITH s.name as sector,
           COUNT(DISTINCT t) as threatCount,
           AVG(t.severity) as avgSeverity,
           COUNT(DISTINCT t.affected_assets) as assetCount
      RETURN sector,
             threatCount,
             toInteger(avgSeverity * 10) as threatScore,
             toInteger(assetCount) as assets
      ORDER BY threatScore DESC
      LIMIT 5
    `);

    // Query for ICS vulnerabilities
    const vulnerabilitiesResult = await session.run(`
      MATCH (v:Vulnerability)
      WHERE v.type IN ['ICS', 'SCADA', 'PLC', 'HMI']
      RETURN v.id as id,
             v.system as system,
             v.vendor as vendor,
             v.cvss as cvss,
             v.description as description,
             v.affected_count as affected
      ORDER BY v.cvss DESC
      LIMIT 10
    `);

    // Query for mitigation strategies
    const mitigationsResult = await session.run(`
      MATCH (m:Mitigation)
      WHERE m.category = 'ICS'
      RETURN m.title as title,
             m.priority as priority,
             m.implemented_percentage as implemented,
             m.description as description
      ORDER BY
        CASE m.priority
          WHEN 'critical' THEN 1
          WHEN 'high' THEN 2
          WHEN 'medium' THEN 3
          ELSE 4
        END
      LIMIT 10
    `);

    // Transform sector data
    const sectors = sectorsResult.records.map(record => ({
      name: record.get('sector') || 'Unknown',
      threatScore: record.get('threatScore') || 0,
      assets: record.get('assets') || 0,
      color: getColorBySeverity(record.get('threatScore') || 0)
    }));

    // Transform vulnerability data
    const vulnerabilities = vulnerabilitiesResult.records.map(record => ({
      id: record.get('id') || 'UNKNOWN',
      system: record.get('system') || 'Unknown System',
      vendor: record.get('vendor') || 'Unknown Vendor',
      cvss: record.get('cvss') || 0,
      description: record.get('description') || 'No description available',
      affected: record.get('affected') || 0
    }));

    // Transform mitigation data
    const mitigations = mitigationsResult.records.map(record => ({
      title: record.get('title') || 'Unknown',
      priority: record.get('priority') || 'medium',
      implemented: record.get('implemented') || 0,
      description: record.get('description') || 'No description available'
    }));

    // Use fallback data if Neo4j returns empty results
    const responseData = {
      sectors: sectors.length > 0 ? sectors : getFallbackSectors(),
      vulnerabilities: vulnerabilities.length > 0 ? vulnerabilities : getFallbackVulnerabilities(),
      mitigations: mitigations.length > 0 ? mitigations : getFallbackMitigations()
    };

    return NextResponse.json(responseData);
  } catch (error) {
    console.error('Error fetching ICS data:', error);

    // Return fallback data on error
    return NextResponse.json({
      sectors: getFallbackSectors(),
      vulnerabilities: getFallbackVulnerabilities(),
      mitigations: getFallbackMitigations()
    });
  } finally {
    await session.close();
  }
}

function getColorBySeverity(score: number): string {
  if (score >= 90) return 'var(--severity-critical)';
  if (score >= 70) return 'var(--severity-high)';
  if (score >= 50) return 'var(--severity-medium)';
  return 'var(--severity-low)';
}

function getFallbackSectors() {
  return [
    { name: 'Energy & Utilities', threatScore: 95, assets: 1250, color: 'var(--severity-critical)' },
    { name: 'Manufacturing', threatScore: 82, assets: 890, color: 'var(--severity-high)' },
    { name: 'Water & Wastewater', threatScore: 76, assets: 650, color: 'var(--severity-high)' },
    { name: 'Transportation', threatScore: 68, assets: 540, color: 'var(--severity-medium)' },
    { name: 'Chemical', threatScore: 71, assets: 420, color: 'var(--severity-medium)' },
  ];
}

function getFallbackVulnerabilities() {
  return [
    {
      id: 'ICS-2024-001',
      system: 'SCADA System',
      vendor: 'Siemens',
      cvss: 9.3,
      description: 'Remote code execution in industrial control system',
      affected: 450,
    },
    {
      id: 'ICS-2024-002',
      system: 'PLC Controller',
      vendor: 'Rockwell Automation',
      cvss: 8.8,
      description: 'Authentication bypass in programmable logic controller',
      affected: 320,
    },
    {
      id: 'ICS-2024-003',
      system: 'HMI Interface',
      vendor: 'Schneider Electric',
      cvss: 7.5,
      description: 'Privilege escalation in human-machine interface',
      affected: 280,
    },
  ];
}

function getFallbackMitigations() {
  return [
    {
      title: 'Network Segmentation',
      priority: 'critical',
      implemented: 68,
      description: 'Isolate ICS networks from IT infrastructure',
    },
    {
      title: 'Access Control',
      priority: 'high',
      implemented: 75,
      description: 'Implement role-based access controls',
    },
    {
      title: 'Patch Management',
      priority: 'high',
      implemented: 52,
      description: 'Regular security updates and patches',
    },
    {
      title: 'Monitoring & Detection',
      priority: 'critical',
      implemented: 61,
      description: '24/7 security monitoring and threat detection',
    },
  ];
}
