import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getNeo4jDriver } from '@/lib/neo4j-enhanced';

/**
 * GET /api/v2/sbom/[sbom_id]
 * Retrieve detailed SBOM information
 *
 * ICE Score: 9.0
 * Multi-tenant isolation via X-Customer-ID header
 */

export async function GET(
  request: NextRequest,
  { params }: { params: { sbom_id: string } }
) {
  try {
    // Validate customer ID
    const customerId = request.headers.get('X-Customer-ID');
    if (!customerId) {
      return NextResponse.json(
        { error: 'X-Customer-ID header is required' },
        { status: 401 }
      );
    }

    const { sbom_id } = params;

    const driver = getNeo4jDriver();
    const session = driver.session();

    try {
      // Query SBOM with components
      const query = `
        MATCH (s:SBOM {sbom_id: $sbomId, customer_id: $customerId})
        OPTIONAL MATCH (s)-[:CONTAINS]->(c:Component)
        OPTIONAL MATCH (c)-[:HAS_VULNERABILITY]->(v:Vulnerability)

        WITH s, c, count(DISTINCT v) as vuln_count

        RETURN
          s.sbom_id as sbom_id,
          s.project_name as project_name,
          s.project_version as project_version,
          s.format as format,
          s.created_at as created_at,
          s.customer_id as customer_id,
          count(DISTINCT c) as components_count,
          collect(DISTINCT {
            component_id: c.component_id,
            name: c.name,
            version: c.version,
            purl: c.purl,
            cpe: c.cpe,
            license: c.license,
            supplier: c.supplier
          }) as components,
          sum(vuln_count) as total_vulnerabilities
      `;

      const result = await session.run(query, {
        sbomId: sbom_id,
        customerId
      });

      if (result.records.length === 0) {
        return NextResponse.json(
          { error: `SBOM ${sbom_id} not found for customer ${customerId}` },
          { status: 404 }
        );
      }

      const record = result.records[0];
      const components = record.get('components')
        .filter((c: any) => c.name) // Filter out null components
        .map((c: any) => ({
          component_id: c.component_id,
          name: c.name,
          version: c.version,
          purl: c.purl,
          cpe: c.cpe,
          license: c.license,
          supplier: c.supplier
        }));

      return NextResponse.json({
        sbom_id: record.get('sbom_id'),
        project_name: record.get('project_name'),
        project_version: record.get('project_version'),
        format: record.get('format'),
        components_count: record.get('components_count').toNumber(),
        vulnerabilities_count: record.get('total_vulnerabilities')?.toNumber() || 0,
        high_severity_count: 0, // TODO: Calculate from CVE relationships
        critical_severity_count: 0,
        created_at: record.get('created_at'),
        customer_id: record.get('customer_id'),
        components
      });

    } finally {
      await session.close();
    }

  } catch (error) {
    console.error('SBOM detail error:', error);
    return NextResponse.json(
      {
        error: 'Failed to retrieve SBOM',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
