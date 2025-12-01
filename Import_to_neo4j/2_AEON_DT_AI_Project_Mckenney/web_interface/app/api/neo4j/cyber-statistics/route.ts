import { NextResponse } from 'next/server';
import neo4j from 'neo4j-driver';

/**
 * Cybersecurity Statistics API Endpoint
 *
 * Returns cybersecurity-specific metrics from Neo4j:
 * - Total CVEs (with severity breakdown)
 * - Total Threat Actors
 * - Total Malware families
 * - Total Attack Campaigns
 * - Total Attack Techniques
 * - Total ICS Assets
 */
export async function GET() {
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

    // Query 1: Count CVEs with severity breakdown
    const cveResult = await session.run(`
      MATCH (cve:CVE)
      WITH count(cve) as total,
           count(CASE WHEN cve.cvss_score >= 9.0 THEN 1 END) as critical,
           count(CASE WHEN cve.cvss_score >= 7.0 AND cve.cvss_score < 9.0 THEN 1 END) as high,
           count(CASE WHEN cve.cvss_score >= 4.0 AND cve.cvss_score < 7.0 THEN 1 END) as medium,
           count(CASE WHEN cve.cvss_score < 4.0 THEN 1 END) as low
      RETURN total, critical, high, medium, low
    `);

    // Query 2: Count Threat Actors
    const threatActorResult = await session.run(`
      MATCH (actor:ThreatActor)
      RETURN count(actor) as total
    `);

    // Query 3: Count Malware
    const malwareResult = await session.run(`
      MATCH (malware:Malware)
      RETURN count(malware) as total
    `);

    // Query 4: Count Campaigns
    const campaignResult = await session.run(`
      MATCH (campaign:Campaign)
      RETURN count(campaign) as total
    `);

    // Query 5: Count Attack Techniques
    const techniqueResult = await session.run(`
      MATCH (technique:AttackTechnique)
      RETURN count(technique) as total
    `);

    // Query 6: Count ICS Assets
    const icsAssetResult = await session.run(`
      MATCH (asset:ICS_Asset)
      RETURN count(asset) as total
    `);

    // Query 7: Count CWE weaknesses
    const cweResult = await session.run(`
      MATCH (cwe:CWE)
      RETURN count(cwe) as total
    `);

    const responseTime = Date.now() - startTime;

    // Extract results
    const cveData = cveResult.records[0];
    const stats = {
      cves: {
        total: cveData?.get('total').toNumber() || 0,
        critical: cveData?.get('critical').toNumber() || 0,
        high: cveData?.get('high').toNumber() || 0,
        medium: cveData?.get('medium').toNumber() || 0,
        low: cveData?.get('low').toNumber() || 0,
      },
      threatActors: threatActorResult.records[0]?.get('total').toNumber() || 0,
      malware: malwareResult.records[0]?.get('total').toNumber() || 0,
      campaigns: campaignResult.records[0]?.get('total').toNumber() || 0,
      attackTechniques: techniqueResult.records[0]?.get('total').toNumber() || 0,
      icsAssets: icsAssetResult.records[0]?.get('total').toNumber() || 0,
      cweWeaknesses: cweResult.records[0]?.get('total').toNumber() || 0,
      responseTime,
      timestamp: new Date().toISOString(),
    };

    return NextResponse.json(stats);

  } catch (error) {
    console.error('Error fetching cybersecurity statistics:', error);
    return NextResponse.json(
      {
        error: 'Failed to fetch cybersecurity statistics',
        message: error instanceof Error ? error.message : 'Unknown error',
        cves: { total: 0, critical: 0, high: 0, medium: 0, low: 0 },
        threatActors: 0,
        malware: 0,
        campaigns: 0,
        attackTechniques: 0,
        icsAssets: 0,
        cweWeaknesses: 0,
      },
      { status: 500 }
    );
  } finally {
    await session.close();
    await driver.close();
  }
}
