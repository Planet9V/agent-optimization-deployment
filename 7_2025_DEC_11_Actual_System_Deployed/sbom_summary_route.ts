import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getNeo4jDriver } from '@/lib/neo4j-enhanced';

/**
 * GET /api/v2/sbom/summary
 * Get aggregate SBOM statistics
 *
 * ICE Score: 8.0
 * Multi-tenant isolation via X-Customer-ID header
 */

export async function GET(request: NextRequest) {
  try {
    // Validate customer ID
    const customerId = request.headers.get('X-Customer-ID');
    if (!customerId) {
      return NextResponse.json(
        { error: 'X-Customer-ID header is required' },
        { status: 401 }
      );
    }

    const driver = getNeo4jDriver();
    const session = driver.session();

    try {
      // Aggregate query for SBOM statistics
      const query = `
        MATCH (s:SBOM {customer_id: $customerId})
        OPTIONAL MATCH (s)-[:CONTAINS]->(c:Component)
        OPTIONAL MATCH (c)-[:HAS_VULNERABILITY]->(v:Vulnerability)

        RETURN
          count(DISTINCT s) as total_sboms,
          count(DISTINCT c) as total_components,
          count(DISTINCT v) as total_vulnerabilities,
          count(DISTINCT CASE WHEN v.severity = 'CRITICAL' THEN v END) as critical_count,
          count(DISTINCT CASE WHEN v.severity = 'HIGH' THEN v END) as high_count,
          count(DISTINCT CASE WHEN v.severity = 'MEDIUM' THEN v END) as medium_count,
          count(DISTINCT CASE WHEN v.severity = 'LOW' THEN v END) as low_count
      `;

      const result = await session.run(query, { customerId });

      if (result.records.length === 0) {
        return NextResponse.json({
          total_sboms: 0,
          total_components: 0,
          total_vulnerabilities: 0,
          critical_vulnerabilities: 0,
          high_vulnerabilities: 0,
          medium_vulnerabilities: 0,
          low_vulnerabilities: 0,
          customer_id: customerId,
          last_updated: new Date().toISOString()
        });
      }

      const record = result.records[0];

      return NextResponse.json({
        total_sboms: record.get('total_sboms').toNumber(),
        total_components: record.get('total_components').toNumber(),
        total_vulnerabilities: record.get('total_vulnerabilities').toNumber(),
        critical_vulnerabilities: record.get('critical_count').toNumber(),
        high_vulnerabilities: record.get('high_count').toNumber(),
        medium_vulnerabilities: record.get('medium_count').toNumber(),
        low_vulnerabilities: record.get('low_count').toNumber(),
        customer_id: customerId,
        last_updated: new Date().toISOString()
      });

    } finally {
      await session.close();
    }

  } catch (error) {
    console.error('SBOM summary error:', error);
    return NextResponse.json(
      {
        error: 'Failed to retrieve SBOM summary',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
