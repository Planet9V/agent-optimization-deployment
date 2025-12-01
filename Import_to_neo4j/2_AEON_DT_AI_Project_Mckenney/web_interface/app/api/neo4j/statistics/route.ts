import { NextResponse } from 'next/server';
import { Neo4jEnhanced } from '@/lib/neo4j-enhanced';

/**
 * Neo4j Statistics API Endpoint
 *
 * Returns aggregate statistics from Neo4j:
 * - Total customers
 * - Total documents
 * - Total tags
 * - Total shared documents
 */
export async function GET() {
  const neo4j = new Neo4jEnhanced(
    process.env.NEO4J_URI || 'bolt://localhost:7687',
    process.env.NEO4J_USER || 'neo4j',
    process.env.NEO4J_PASSWORD || 'neo4j@openspg'
  );

  try {
    const startTime = Date.now();

    // Test connection first
    const isConnected = await neo4j.testConnection();
    if (!isConnected) {
      return NextResponse.json(
        {
          error: 'Failed to connect to Neo4j',
          totalCustomers: 0,
          totalDocuments: 0,
          totalTags: 0,
          totalSharedDocuments: 0
        },
        { status: 503 }
      );
    }

    // Get statistics
    const stats = await neo4j.getStatistics();
    const responseTime = Date.now() - startTime;

    return NextResponse.json({
      ...stats,
      responseTime,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('Error fetching Neo4j statistics:', error);
    return NextResponse.json(
      {
        error: 'Failed to fetch statistics',
        message: error instanceof Error ? error.message : 'Unknown error',
        totalCustomers: 0,
        totalDocuments: 0,
        totalTags: 0,
        totalSharedDocuments: 0
      },
      { status: 500 }
    );
  } finally {
    await neo4j.close();
  }
}
