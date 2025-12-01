import { NextRequest, NextResponse } from 'next/server';
import neo4j from 'neo4j-driver';

/**
 * Recent Activity API Endpoint
 *
 * Returns recent activity from the system:
 * - Document uploads
 * - Customer operations
 * - Tag changes
 * - System events
 */
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const limit = parseInt(searchParams.get('limit') || '10', 10);

  const driver = neo4j.driver(
    process.env.NEO4J_URI || 'bolt://localhost:7687',
    neo4j.auth.basic(
      process.env.NEO4J_USER || 'neo4j',
      process.env.NEO4J_PASSWORD || 'neo4j@openspg'
    )
  );

  const session = driver.session();

  try {
    // Query for recent document uploads
    const documentResult = await session.run(
      `
      MATCH (d:Document)
      OPTIONAL MATCH (d)<-[:OWNS]-(c:Customer)
      RETURN d.id as id,
             d.title as title,
             d.createdAt as timestamp,
             c.name as customerName,
             'upload' as type
      ORDER BY d.createdAt DESC
      LIMIT $limit
      `,
      { limit: Math.ceil(limit / 2) }
    );

    // Query for recent customer operations
    const customerResult = await session.run(
      `
      MATCH (c:Customer)
      RETURN c.id as id,
             c.name as name,
             c.createdAt as timestamp,
             'processed' as type
      ORDER BY c.createdAt DESC
      LIMIT $limit
      `,
      { limit: Math.ceil(limit / 2) }
    );

    // Combine and format activities
    const documentActivities = documentResult.records.map(record => ({
      id: `doc-${record.get('id')}`,
      type: 'upload' as const,
      title: `Document uploaded: ${record.get('title') || 'Untitled'}`,
      description: record.get('customerName')
        ? `Uploaded by ${record.get('customerName')}`
        : 'System upload',
      timestamp: record.get('timestamp')
        ? new Date(record.get('timestamp').toString())
        : new Date(),
      user: record.get('customerName') || 'System'
    }));

    const customerActivities = customerResult.records.map(record => ({
      id: `customer-${record.get('id')}`,
      type: 'processed' as const,
      title: `Customer created: ${record.get('name')}`,
      description: 'New customer account created',
      timestamp: record.get('timestamp')
        ? new Date(record.get('timestamp').toString())
        : new Date(),
      user: 'System'
    }));

    // Combine and sort by timestamp
    const allActivities = [...documentActivities, ...customerActivities]
      .sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime())
      .slice(0, limit);

    return NextResponse.json({
      activities: allActivities,
      total: allActivities.length,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('Error fetching recent activity:', error);
    return NextResponse.json(
      {
        error: 'Failed to fetch activity',
        message: error instanceof Error ? error.message : 'Unknown error',
        activities: []
      },
      { status: 500 }
    );
  } finally {
    await session.close();
    await driver.close();
  }
}
