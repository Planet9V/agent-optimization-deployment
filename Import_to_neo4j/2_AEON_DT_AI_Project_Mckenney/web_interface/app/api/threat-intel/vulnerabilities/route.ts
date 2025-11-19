import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://openspg-neo4j:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USER || 'neo4j',
    process.env.NEO4J_PASSWORD || 'neo4j@openspg'
  )
);

// TypeScript interfaces matching the strategy document
interface CVE {
  id: string;
  cvss: number;
  description: string;
  exploited: boolean;
  patched: boolean;
  attackPatterns: number;
  threatActors: number;
  activeCampaigns: string[];
  attributedActors: string[];
}

interface CVSSDistribution {
  range: string;
  count: number;
}

interface PatchStatus {
  patchedPercent: number;
  availablePercent: number;
  noPatchPercent: number;
}

interface VulnerabilityResponse {
  cves: CVE[];
  distribution: CVSSDistribution[];
  patchStatus: PatchStatus;
  totalCVEs: number;
}

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

    const session = driver.session();

    try {
      // Parse query parameters
      const { searchParams } = new URL(request.url);
    const minCVSS = parseFloat(searchParams.get('minCVSS') || '7.0');
    const exploitedFilter = searchParams.get('exploited');
    const patchedFilter = searchParams.get('patched');
    const limit = parseInt(searchParams.get('limit') || '50');

    // Query 2.1: CVE Exploitation Intelligence (6-8 hops)
    // Optimized with intermediate LIMIT to prevent 2GB transaction limit
    const cveQuery = `
      MATCH (cve:CVE)
      WHERE cve.id IS NOT NULL
        AND cve.cvss_score >= $minCVSS

      OPTIONAL MATCH path1 = (cve)-[:VULNERABLE_TO]->(cwe:CWE)
                                 -[:EXPLOITS_WEAKNESS]-(ap:AttackPattern)
      OPTIONAL MATCH path2 = (ap)-[:USES_ATTACK_PATTERN]-(ta:ThreatActor)
      OPTIONAL MATCH path3 = (ta)-[:ORCHESTRATES_CAMPAIGN]->(c:Campaign)

      WITH cve,
           collect(DISTINCT ap) as patterns,
           collect(DISTINCT ta) as actors,
           collect(DISTINCT c) as campaigns
      LIMIT 100

      RETURN cve.id as id,
             cve.cvss_score as cvss,
             COALESCE(cve.description, 'No description') as description,
             size(campaigns) > 0 as exploited,
             cve.patch_available IS NOT NULL as patched,
             size(patterns) as attack_patterns,
             size(actors) as threat_actors,
             [c in campaigns[0..3] | c.name] as active_campaigns,
             [a in actors[0..5] | a.name] as attributed_actors

      ORDER BY cve.cvss_score DESC, size(campaigns) DESC
      LIMIT $limit
    `;

    // Query 2.2: CVSS Score Distribution
    const distributionQuery = `
      MATCH (cve:CVE)
      WHERE cve.cvss_score IS NOT NULL

      WITH CASE
        WHEN cve.cvss_score >= 9.0 THEN '9.0-10.0'
        WHEN cve.cvss_score >= 7.0 THEN '7.0-8.9'
        WHEN cve.cvss_score >= 4.0 THEN '4.0-6.9'
        ELSE '0.1-3.9'
      END as range, count(*) as count

      RETURN range, count
      ORDER BY range DESC
    `;

    // Query 2.3: Patch Status Analysis
    const patchStatusQuery = `
      MATCH (cve:CVE)
      WHERE cve.id IS NOT NULL

      WITH count(*) as total,
           sum(CASE WHEN cve.patch_available = true THEN 1 ELSE 0 END) as patched,
           sum(CASE WHEN cve.patch_available = false AND cve.patch_planned = true THEN 1 ELSE 0 END) as patch_available,
           sum(CASE WHEN cve.patch_available = false AND cve.patch_planned = false THEN 1 ELSE 0 END) as no_patch

      RETURN toInteger((toFloat(patched) / toFloat(total)) * 100) as patched_percent,
             toInteger((toFloat(patch_available) / toFloat(total)) * 100) as available_percent,
             toInteger((toFloat(no_patch) / toFloat(total)) * 100) as no_patch_percent
    `;

    // Execute all queries in parallel
    const [cveResult, distributionResult, patchStatusResult] = await Promise.all([
      session.run(cveQuery, { minCVSS, limit }),
      session.run(distributionQuery),
      session.run(patchStatusQuery),
    ]);

    // Process CVE results
    let cves: CVE[] = cveResult.records.map(record => ({
      id: record.get('id'),
      cvss: record.get('cvss'),
      description: record.get('description'),
      exploited: record.get('exploited'),
      patched: record.get('patched'),
      attackPatterns: record.get('attack_patterns').toNumber(),
      threatActors: record.get('threat_actors').toNumber(),
      activeCampaigns: record.get('active_campaigns'),
      attributedActors: record.get('attributed_actors'),
    }));

    // Apply filters if specified
    if (exploitedFilter !== null) {
      const exploitedBool = exploitedFilter === 'true';
      cves = cves.filter(cve => cve.exploited === exploitedBool);
    }
    if (patchedFilter !== null) {
      const patchedBool = patchedFilter === 'true';
      cves = cves.filter(cve => cve.patched === patchedBool);
    }

    // Process distribution results
    const distribution: CVSSDistribution[] = distributionResult.records.map(record => ({
      range: record.get('range'),
      count: record.get('count').toNumber(),
    }));

    // Process patch status results
    const patchStatusRecord = patchStatusResult.records[0];
    const patchStatus: PatchStatus = patchStatusRecord ? {
      patchedPercent: patchStatusRecord.get('patched_percent')?.toNumber?.() || 0,
      availablePercent: patchStatusRecord.get('available_percent')?.toNumber?.() || 0,
      noPatchPercent: patchStatusRecord.get('no_patch_percent')?.toNumber?.() || 0,
    } : {
      patchedPercent: 0,
      availablePercent: 0,
      noPatchPercent: 0,
    };

    // Calculate total CVEs
    const totalCVEs = distribution.reduce((sum, d) => sum + d.count, 0);

      const response: VulnerabilityResponse = {
        cves,
        distribution,
        patchStatus,
        totalCVEs,
      };

      return NextResponse.json(response);
    } finally {
      await session.close();
    }
  } catch (error) {
    console.error('Error fetching vulnerability data:', error);
    return NextResponse.json(
      {
        error: 'Failed to fetch vulnerability data',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}
