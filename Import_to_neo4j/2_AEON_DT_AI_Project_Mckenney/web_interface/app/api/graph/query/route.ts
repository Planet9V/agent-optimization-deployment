import { NextRequest, NextResponse } from 'next/server';
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://localhost:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USER || 'neo4j',
    process.env.NEO4J_PASSWORD || 'password'
  )
);

// Validate Cypher query for safety
function validateQuery(query: string): { valid: boolean; error?: string } {
  const dangerousKeywords = [
    'DELETE',
    'REMOVE',
    'SET',
    'CREATE',
    'MERGE',
    'DROP',
    'ALTER',
  ];

  const upperQuery = query.toUpperCase();
  for (const keyword of dangerousKeywords) {
    if (upperQuery.includes(keyword)) {
      return {
        valid: false,
        error: `Query contains potentially dangerous keyword: ${keyword}`,
      };
    }
  }

  return { valid: true };
}

export async function POST(request: NextRequest) {
  try {
    const { query } = await request.json();

    if (!query) {
      return NextResponse.json(
        { error: 'Query is required' },
        { status: 400 }
      );
    }

    // Validate query
    const validation = validateQuery(query);
    if (!validation.valid) {
      return NextResponse.json(
        { error: validation.error },
        { status: 400 }
      );
    }

    const session = driver.session();

    try {
      const result = await session.run(query);

      const records = result.records.map(record => {
        const obj: Record<string, any> = {};
        (record.keys as string[]).forEach(key => {
          const value = record.get(key);
          if (value && typeof value === 'object' && value.properties) {
            obj[key] = {
              ...value.properties,
              labels: value.labels,
              identity: value.identity?.toString(),
            };
          } else {
            obj[key] = value;
          }
        });
        return obj;
      });

      return NextResponse.json({
        records,
        summary: {
          counters: result.summary.counters,
          query: result.summary.query.text,
        },
      });
    } finally {
      await session.close();
    }
  } catch (error) {
    console.error('Error executing query:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to execute query' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const nodeTypes = searchParams.get('nodeTypes')?.split(',') || [];
    const relationshipTypes = searchParams.get('relationshipTypes')?.split(',') || [];
    const customers = searchParams.get('customers')?.split(',') || [];
    const tags = searchParams.get('tags')?.split(',') || [];
    const confidenceMin = parseFloat(searchParams.get('confidenceMin') || '0');
    const dateStart = searchParams.get('dateStart');
    const dateEnd = searchParams.get('dateEnd');

    let query = 'MATCH (n)-[r]->(m)';
    const conditions: string[] = [];
    const params: Record<string, any> = {};

    if (nodeTypes.length > 0) {
      conditions.push('ANY(label IN labels(n) WHERE label IN $nodeTypes)');
      params.nodeTypes = nodeTypes;
    }

    if (relationshipTypes.length > 0) {
      conditions.push('type(r) IN $relationshipTypes');
      params.relationshipTypes = relationshipTypes;
    }

    if (customers.length > 0) {
      conditions.push('n.customer IN $customers');
      params.customers = customers;
    }

    if (tags.length > 0) {
      conditions.push('ANY(tag IN n.tags WHERE tag IN $tags)');
      params.tags = tags;
    }

    if (confidenceMin > 0) {
      conditions.push('(r.confidence IS NULL OR r.confidence >= $confidenceMin)');
      params.confidenceMin = confidenceMin;
    }

    if (dateStart && dateEnd) {
      conditions.push('n.created >= datetime($dateStart) AND n.created <= datetime($dateEnd)');
      params.dateStart = dateStart;
      params.dateEnd = dateEnd;
    }

    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }

    query += ' RETURN n, r, m LIMIT 500';

    const session = driver.session();

    try {
      const result = await session.run(query, params);

      const nodes: any[] = [];
      const relationships: any[] = [];
      const nodeMap = new Map();

      result.records.forEach(record => {
        const n = record.get('n');
        const r = record.get('r');
        const m = record.get('m');

        if (n && !nodeMap.has(n.identity.toString())) {
          nodeMap.set(n.identity.toString(), true);
          nodes.push({
            id: n.identity.toString(),
            labels: n.labels,
            properties: n.properties,
          });
        }

        if (m && !nodeMap.has(m.identity.toString())) {
          nodeMap.set(m.identity.toString(), true);
          nodes.push({
            id: m.identity.toString(),
            labels: m.labels,
            properties: m.properties,
          });
        }

        if (r) {
          relationships.push({
            id: r.identity.toString(),
            type: r.type,
            startNode: r.start.toString(),
            endNode: r.end.toString(),
            properties: r.properties,
          });
        }
      });

      return NextResponse.json({ nodes, relationships });
    } finally {
      await session.close();
    }
  } catch (error) {
    console.error('Error fetching subgraph:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to fetch subgraph' },
      { status: 500 }
    );
  }
}
