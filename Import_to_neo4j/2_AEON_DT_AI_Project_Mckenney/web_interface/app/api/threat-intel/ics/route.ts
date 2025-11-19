import { NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';
import neo4j from 'neo4j-driver';

/**
 * ICS Focus Threat Intelligence API Endpoint
 *
 * Returns critical infrastructure threat intelligence:
 * - Sector threat assessments with risk scoring
 * - ICS/SCADA critical vulnerabilities
 * - Security control coverage analysis
 *
 * Based on Phase 1 Strategy: 6-8 hop graph traversal queries
 *
 * @requires Authentication - Clerk auth required
 */

export async function GET(request: Request) {
  // Verify authentication
  const { userId } = await auth();

  if (!userId) {
    return NextResponse.json(
      { error: 'Unauthorized - Authentication required' },
      { status: 401 }
    );
  }
  const { searchParams } = new URL(request.url);
  const minCVSS = parseFloat(searchParams.get('minCVSS') || '7.0');
  const sectorFilter = searchParams.get('sectorFilter') || null;

  const driver = neo4j.driver(
    process.env.NEO4J_URI || 'bolt://localhost:7687',
    neo4j.auth.basic(
      process.env.NEO4J_USER || 'neo4j',
      process.env.NEO4J_PASSWORD || 'neo4j@openspg'
    )
  );

  const session = driver.session();

  try {
    const startTime = Date.now();

    // Query 4.1: Sector Threat Assessment (6-8 hops)
    // Sector ← ICS_Asset ← CVE ← AttackPattern ← Campaign
    const sectorsResult = await session.run(`
      MATCH (s:Sector)
      WHERE s.name IS NOT NULL
      ${sectorFilter ? 'AND s.name = $sectorFilter' : ''}

      // Find ICS assets in this sector
      OPTIONAL MATCH (s)<-[:BELONGS_TO]-(asset:ICS_Asset)

      // Find CVEs affecting these assets
      OPTIONAL MATCH (asset)-[:VULNERABLE_TO]->(cve:CVE)

      // Find campaigns targeting these CVEs
      OPTIONAL MATCH path = (cve)-[*1..4]-(c:Campaign)

      WITH s,
           count(DISTINCT asset) as exposed_assets,
           count(DISTINCT cve) as vulnerabilities,
           count(DISTINCT c) as campaigns,
           avg(cve.cvss_score) as avg_cvss

      // Calculate threat score (0-100)
      WITH s, exposed_assets, vulnerabilities, campaigns,
           toInteger(COALESCE(avg_cvss, 0.0) * 10) as cvss_component,
           toInteger((toFloat(campaigns) / 10.0) * 30) as campaign_component,
           toInteger((toFloat(vulnerabilities) / 100.0) * 60) as vuln_component

      WITH s, exposed_assets, vulnerabilities, campaigns,
           CASE
             WHEN (cvss_component + campaign_component + vuln_component) > 100 THEN 100
             ELSE cvss_component + campaign_component + vuln_component
           END as threat_score

      RETURN s.name as name,
             threat_score as threatScore,
             exposed_assets as assets,
             CASE
               WHEN threat_score >= 90 THEN 'var(--severity-critical)'
               WHEN threat_score >= 75 THEN 'var(--severity-high)'
               ELSE 'var(--severity-medium)'
             END as color

      ORDER BY threat_score DESC
      LIMIT 10
    `, { sectorFilter });

    // Query 4.2: ICS/SCADA Critical Vulnerabilities (5-7 hops)
    const vulnerabilitiesResult = await session.run(`
      MATCH (cve:CVE)-[*1..3]-(asset:ICS_Asset)
      WHERE cve.cvss_score >= $minCVSS
        AND (asset.type =~ '.*SCADA.*'
             OR asset.type =~ '.*PLC.*'
             OR asset.type =~ '.*HMI.*')

      // Get vendor and system info
      OPTIONAL MATCH (asset)-[:MANUFACTURED_BY]->(vendor:Organization)

      // Find active campaigns
      OPTIONAL MATCH path = (cve)-[*1..4]-(c:Campaign)

      WITH cve, asset, vendor,
           count(DISTINCT c) as campaign_count,
           count(DISTINCT asset) as affected_systems

      RETURN 'ICS-' + cve.id as id,
             COALESCE(asset.type, 'ICS System') as system,
             COALESCE(vendor.name, 'Unknown') as vendor,
             cve.cvss_score as cvss,
             COALESCE(cve.description, 'Critical ICS vulnerability') as description,
             affected_systems as affected

      ORDER BY cve.cvss_score DESC, campaign_count DESC
      LIMIT 10
    `, { minCVSS });

    // Query 4.3: Security Control Coverage (4-5 hops)
    const mitigationsResult = await session.run(`
      MATCH (m:Mitigation)
      WHERE m.name IS NOT NULL

      // Find how many systems have this mitigation
      OPTIONAL MATCH (m)-[*1..3]-(asset:ICS_Asset)

      // Calculate implementation percentage
      WITH m, count(DISTINCT asset) as implemented_count,
           CASE
             WHEN m.priority = 'critical' THEN 'critical'
             WHEN m.priority = 'high' THEN 'high'
             ELSE 'medium'
           END as priority

      // Assume total assets for percentage (or get from count)
      WITH m, implemented_count, priority,
           toInteger((toFloat(implemented_count) / 100.0) * 100) as implemented

      RETURN m.name as title,
             priority,
             CASE
               WHEN implemented > 100 THEN 100
               ELSE implemented
             END as implemented,
             COALESCE(m.description, 'Security control') as description

      ORDER BY priority DESC, implemented ASC
      LIMIT 8
    `);

    // Query: Total Assets Count
    const totalAssetsResult = await session.run(`
      MATCH (asset:ICS_Asset)
      RETURN count(asset) as total
    `);

    // Query: Critical Vulnerabilities Count
    const criticalVulnsResult = await session.run(`
      MATCH (cve:CVE)-[*1..3]-(asset:ICS_Asset)
      WHERE cve.cvss_score >= 9.0
        AND (asset.type =~ '.*SCADA.*'
             OR asset.type =~ '.*PLC.*'
             OR asset.type =~ '.*HMI.*')
      RETURN count(DISTINCT cve) as total
    `);

    const responseTime = Date.now() - startTime;

    // Process sectors data
    const sectors = sectorsResult.records.map((record) => ({
      name: record.get('name'),
      threatScore: record.get('threatScore')?.toNumber() || 0,
      assets: record.get('assets')?.toNumber() || 0,
      color: record.get('color'),
    }));

    // Process vulnerabilities data
    const vulnerabilities = vulnerabilitiesResult.records.map((record) => ({
      id: record.get('id'),
      system: record.get('system'),
      vendor: record.get('vendor'),
      cvss: record.get('cvss')?.toNumber() || 0,
      description: record.get('description'),
      affected: record.get('affected')?.toNumber() || 0,
    }));

    // Process mitigations data
    const mitigations = mitigationsResult.records.map((record) => ({
      title: record.get('title'),
      priority: record.get('priority'),
      implemented: record.get('implemented')?.toNumber() || 0,
      description: record.get('description'),
    }));

    const response = {
      sectors,
      vulnerabilities,
      mitigations,
      totalAssets: totalAssetsResult.records[0]?.get('total')?.toNumber() || 0,
      criticalVulns: criticalVulnsResult.records[0]?.get('total')?.toNumber() || 0,
      responseTime,
      timestamp: new Date().toISOString(),
      params: {
        minCVSS,
        sectorFilter,
      },
    };

    return NextResponse.json(response);

  } catch (error) {
    console.error('Error fetching ICS threat intelligence:', error);
    return NextResponse.json(
      {
        error: 'Failed to fetch ICS threat intelligence',
        message: error instanceof Error ? error.message : 'Unknown error',
        sectors: [],
        vulnerabilities: [],
        mitigations: [],
        totalAssets: 0,
        criticalVulns: 0,
      },
      { status: 500 }
    );
  } finally {
    await session.close();
    await driver.close();
  }
}
