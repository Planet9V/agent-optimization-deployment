import { NextRequest, NextResponse } from 'next/server';
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://localhost:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USERNAME || 'neo4j',
    process.env.NEO4J_PASSWORD || 'neo4j@openspg'
  )
);

interface TimeSeriesData {
  documentsOverTime: Array<{ date: string; count: number }>;
  entitiesByType: Array<{ name: string; value: number }>;
  customerActivity: Array<{ name: string; documents: number; entities: number }>;
}

function getAggregationInterval(timeRange: string): string {
  switch (timeRange) {
    case '7d':
      return 'day';
    case '30d':
      return 'day';
    case '90d':
      return 'week';
    default:
      return 'day';
  }
}

function calculateStartDate(timeRange: string): Date {
  const endDate = new Date();
  const startDate = new Date();

  switch (timeRange) {
    case '7d':
      startDate.setDate(endDate.getDate() - 7);
      break;
    case '30d':
      startDate.setDate(endDate.getDate() - 30);
      break;
    case '90d':
      startDate.setDate(endDate.getDate() - 90);
      break;
    default:
      startDate.setDate(endDate.getDate() - 30);
  }

  return startDate;
}

export async function GET(request: NextRequest) {
  const session = driver.session();

  try {
    const searchParams = request.nextUrl.searchParams;
    const timeRange = searchParams.get('timeRange') || '30d';
    const customerId = searchParams.get('customerId');

    const startDate = calculateStartDate(timeRange);
    const interval = getAggregationInterval(timeRange);
    const startDateStr = startDate.toISOString();

    // Documents over time
    const documentsQuery = `
      MATCH (d:Document)
      WHERE datetime(d.createdAt) >= datetime($startDate)
      ${customerId ? 'AND d.customerId = $customerId' : ''}
      WITH d,
           CASE
             WHEN $interval = 'day' THEN date(d.createdAt)
             WHEN $interval = 'week' THEN date(d.createdAt) - duration({days: date(d.createdAt).dayOfWeek - 1})
             ELSE date(d.createdAt)
           END as dateKey
      WITH dateKey, count(d) as count
      ORDER BY dateKey
      RETURN toString(dateKey) as date, count
    `;

    const documentsResult = await session.run(documentsQuery, {
      startDate: startDateStr,
      interval,
      customerId,
    });

    const documentsOverTime = documentsResult.records.map(record => ({
      date: record.get('date'),
      count: record.get('count').toNumber(),
    }));

    // Entities by type
    const entitiesQuery = `
      MATCH (e)
      WHERE (e:Entity OR e:Person OR e:Organization OR e:Location OR e:Technology)
      ${customerId ? 'AND e.customerId = $customerId' : ''}
      WITH labels(e) as entityLabels
      UNWIND entityLabels as label
      WHERE label IN ['Entity', 'Person', 'Organization', 'Location', 'Technology']
      WITH label, count(*) as count
      RETURN label as name, count as value
      ORDER BY value DESC
    `;

    const entitiesResult = await session.run(entitiesQuery, { customerId });

    const entitiesByType = entitiesResult.records.map(record => ({
      name: record.get('name'),
      value: record.get('value').toNumber(),
    }));

    // Customer activity
    const customerQuery = `
      MATCH (c:Customer)
      ${customerId ? 'WHERE c.id = $customerId' : ''}
      OPTIONAL MATCH (c)-[:OWNS]->(d:Document)
      WHERE datetime(d.createdAt) >= datetime($startDate)
      WITH c, count(DISTINCT d) as docCount
      OPTIONAL MATCH (c)-[:OWNS]->(d:Document)-[:CONTAINS|MENTIONS]->(e)
      WHERE datetime(d.createdAt) >= datetime($startDate)
      AND (e:Entity OR e:Person OR e:Organization OR e:Location OR e:Technology)
      WITH c.name as name, docCount, count(DISTINCT e) as entityCount
      WHERE docCount > 0 OR entityCount > 0
      RETURN name, docCount as documents, entityCount as entities
      ORDER BY documents DESC
      LIMIT 10
    `;

    const customerResult = await session.run(customerQuery, {
      startDate: startDateStr,
      customerId,
    });

    const customerActivity = customerResult.records.map(record => ({
      name: record.get('name'),
      documents: record.get('documents').toNumber(),
      entities: record.get('entities').toNumber(),
    }));

    const data: TimeSeriesData = {
      documentsOverTime,
      entitiesByType,
      customerActivity,
    };

    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching time series data:', error);
    return NextResponse.json(
      { error: 'Failed to fetch time series data' },
      { status: 500 }
    );
  } finally {
    await session.close();
  }
}
