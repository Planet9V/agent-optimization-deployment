import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getNeo4jDriver } from '@/lib/neo4j-enhanced';
import { getQdrantClient } from '@/lib/qdrant';
import { v4 as uuidv4 } from 'uuid';

/**
 * POST /api/v2/sbom/analyze
 * Analyze SBOM file and store components in graph database
 *
 * ICE Score: 8.1
 * Multi-tenant isolation via X-Customer-ID header
 */

interface Component {
  name: string;
  version: string;
  purl?: string;
  cpe?: string;
  license?: string;
  supplier?: string;
}

interface SBOMAnalyzeRequest {
  project_name: string;
  project_version?: string;
  format: 'cyclonedx' | 'spdx';
  content: any;
}

export async function POST(request: NextRequest) {
  const startTime = Date.now();

  try {
    // Validate customer ID
    const customerId = request.headers.get('X-Customer-ID');
    if (!customerId) {
      return NextResponse.json(
        { error: 'X-Customer-ID header is required' },
        { status: 401 }
      );
    }

    const body: SBOMAnalyzeRequest = await request.json();
    const { project_name, project_version = '1.0.0', format, content } = body;

    // Validate required fields
    if (!project_name || !format || !content) {
      return NextResponse.json(
        { error: 'project_name, format, and content are required' },
        { status: 400 }
      );
    }

    // Generate unique SBOM ID
    const sbomId = uuidv4();
    const components: Component[] = [];

    // Parse components based on format
    if (format === 'cyclonedx') {
      const cycloneDXComponents = content.components || [];
      for (const comp of cycloneDXComponents) {
        components.push({
          name: comp.name || 'unknown',
          version: comp.version || '0.0.0',
          purl: comp.purl,
          cpe: comp.cpe,
          license: comp.licenses?.[0]?.license?.id,
          supplier: comp.supplier?.name
        });
      }
    } else if (format === 'spdx') {
      const spdxPackages = content.packages || [];
      for (const pkg of spdxPackages) {
        components.push({
          name: pkg.name || 'unknown',
          version: pkg.versionInfo || '0.0.0',
          license: pkg.licenseConcluded,
          supplier: pkg.supplier
        });
      }
    }

    // Store in Neo4j
    const driver = getNeo4jDriver();
    const session = driver.session();

    try {
      // Create SBOM node
      const createSBOMQuery = `
        CREATE (s:SBOM {
          sbom_id: $sbomId,
          project_name: $projectName,
          project_version: $projectVersion,
          format: $format,
          customer_id: $customerId,
          created_at: datetime(),
          updated_at: datetime()
        })
        RETURN s
      `;

      await session.run(createSBOMQuery, {
        sbomId,
        projectName: project_name,
        projectVersion: project_version,
        format,
        customerId
      });

      // Create component nodes and relationships
      let componentsCreated = 0;
      for (const comp of components) {
        const componentId = uuidv4();
        const createComponentQuery = `
          MATCH (s:SBOM {sbom_id: $sbomId})
          CREATE (c:Component {
            component_id: $componentId,
            name: $name,
            version: $version,
            purl: $purl,
            cpe: $cpe,
            license: $license,
            supplier: $supplier,
            customer_id: $customerId,
            created_at: datetime()
          })
          CREATE (s)-[:CONTAINS]->(c)
          RETURN c
        `;

        await session.run(createComponentQuery, {
          sbomId,
          componentId,
          name: comp.name,
          version: comp.version,
          purl: comp.purl || null,
          cpe: comp.cpe || null,
          license: comp.license || null,
          supplier: comp.supplier || null,
          customerId
        });

        componentsCreated++;

        // Store component embedding in Qdrant for semantic search
        try {
          const qdrant = getQdrantClient();
          const collectionName = 'sbom_components';

          // Generate embedding text
          const embeddingText = `${comp.name} ${comp.version} ${comp.license || ''} ${comp.supplier || ''}`;

          // Store in Qdrant with metadata
          await qdrant.upsert(collectionName, {
            points: [{
              id: componentId,
              vector: Array(384).fill(0), // Placeholder - use actual embedding service
              payload: {
                component_id: componentId,
                name: comp.name,
                version: comp.version,
                sbom_id: sbomId,
                project_name,
                customer_id: customerId,
                created_at: new Date().toISOString()
              }
            }]
          });
        } catch (qdrantError) {
          console.error('Qdrant error (non-fatal):', qdrantError);
          // Continue even if Qdrant fails
        }
      }

      const responseTime = Date.now() - startTime;

      return NextResponse.json({
        sbom_id: sbomId,
        project_name,
        components_count: componentsCreated,
        vulnerabilities_count: 0,
        created_at: new Date().toISOString(),
        customer_id: customerId,
        response_time_ms: responseTime
      }, { status: 201 });

    } finally {
      await session.close();
    }

  } catch (error) {
    console.error('SBOM analyze error:', error);
    return NextResponse.json(
      {
        error: 'Failed to analyze SBOM',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}
