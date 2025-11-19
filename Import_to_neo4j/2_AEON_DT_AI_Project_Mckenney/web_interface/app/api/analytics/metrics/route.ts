import { NextRequest, NextResponse } from 'next/server';
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://localhost:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USERNAME || 'neo4j',
    process.env.NEO4J_PASSWORD || 'neo4j@openspg'
  )
);

interface MetricsResponse {
  documentGrowth: {
    current: number;
    previous: number;
    percentageChange: number;
  };
  entitiesAdded: {
    current: number;
    previous: number;
    percentageChange: number;
  };
  processSuccess: {
    current: number;
    percentageChange: number;
  };
  avgQuality: {
    current: number;
    previous: number;
    percentageChange: number;
  };
}

function calculateDateRange(timeRange: string): { startDate: Date; previousStartDate: Date; endDate: Date } {
  const endDate = new Date();
  const startDate = new Date();
  const previousStartDate = new Date();

  switch (timeRange) {
    case '7d':
      startDate.setDate(endDate.getDate() - 7);
      previousStartDate.setDate(endDate.getDate() - 14);
      break;
    case '30d':
      startDate.setDate(endDate.getDate() - 30);
      previousStartDate.setDate(endDate.getDate() - 60);
      break;
    case '90d':
      startDate.setDate(endDate.getDate() - 90);
      previousStartDate.setDate(endDate.getDate() - 180);
      break;
    default:
      startDate.setDate(endDate.getDate() - 30);
      previousStartDate.setDate(endDate.getDate() - 60);
  }

  return { startDate, previousStartDate, endDate };
}

export async function GET(request: NextRequest) {
  const session = driver.session();

  try {
    const searchParams = request.nextUrl.searchParams;
    const timeRange = searchParams.get('timeRange') || '30d';
    const customerId = searchParams.get('customerId');

    const { startDate, previousStartDate, endDate } = calculateDateRange(timeRange);

    const startDateStr = startDate.toISOString();
    const previousStartDateStr = previousStartDate.toISOString();
    const endDateStr = endDate.toISOString();

    // Document Growth
    const documentQuery = `
      MATCH (d:Document)
      ${customerId ? 'WHERE d.customerId = $customerId' : ''}
      WITH d,
           CASE
             WHEN datetime(d.createdAt) >= datetime($startDate) THEN 'current'
             WHEN datetime(d.createdAt) >= datetime($previousStartDate) AND datetime(d.createdAt) < datetime($startDate) THEN 'previous'
             ELSE 'other'
           END as period
      WITH period, count(d) as count
      RETURN collect({period: period, count: count}) as periods
    `;

    const documentResult = await session.run(documentQuery, {
      startDate: startDateStr,
      previousStartDate: previousStartDateStr,
      customerId,
    });

    const documentPeriods = documentResult.records[0]?.get('periods') || [];
    const currentDocs = documentPeriods.find((p: any) => p.period === 'current')?.count?.toNumber() || 0;
    const previousDocs = documentPeriods.find((p: any) => p.period === 'previous')?.count?.toNumber() || 0;

    // Entities Added
    const entityQuery = `
      MATCH (e)
      WHERE e:Entity OR e:Person OR e:Organization OR e:Location OR e:Technology
      ${customerId ? 'AND e.customerId = $customerId' : ''}
      WITH e,
           CASE
             WHEN datetime(e.createdAt) >= datetime($startDate) THEN 'current'
             WHEN datetime(e.createdAt) >= datetime($previousStartDate) AND datetime(e.createdAt) < datetime($startDate) THEN 'previous'
             ELSE 'other'
           END as period
      WITH period, count(e) as count
      RETURN collect({period: period, count: count}) as periods
    `;

    const entityResult = await session.run(entityQuery, {
      startDate: startDateStr,
      previousStartDate: previousStartDateStr,
      customerId,
    });

    const entityPeriods = entityResult.records[0]?.get('periods') || [];
    const currentEntities = entityPeriods.find((p: any) => p.period === 'current')?.count?.toNumber() || 0;
    const previousEntities = entityPeriods.find((p: any) => p.period === 'previous')?.count?.toNumber() || 0;

    // Process Success Rate
    const processQuery = `
      MATCH (d:Document)
      WHERE datetime(d.createdAt) >= datetime($startDate)
      ${customerId ? 'AND d.customerId = $customerId' : ''}
      WITH count(d) as total
      MATCH (d:Document)
      WHERE datetime(d.createdAt) >= datetime($startDate)
      ${customerId ? 'AND d.customerId = $customerId' : ''}
      AND (d.processingStatus = 'completed' OR d.status = 'processed')
      WITH total, count(d) as successful
      RETURN total, successful,
             CASE WHEN total > 0 THEN toFloat(successful) / toFloat(total) * 100 ELSE 0 END as successRate
    `;

    const processResult = await session.run(processQuery, {
      startDate: startDateStr,
      customerId,
    });

    const processRecord = processResult.records[0];
    const successRate = processRecord?.get('successRate') || 0;

    // Average Quality Score
    const qualityQuery = `
      MATCH (d:Document)
      ${customerId ? 'WHERE d.customerId = $customerId' : ''}
      WITH d,
           CASE
             WHEN datetime(d.createdAt) >= datetime($startDate) THEN 'current'
             WHEN datetime(d.createdAt) >= datetime($previousStartDate) AND datetime(d.createdAt) < datetime($startDate) THEN 'previous'
             ELSE 'other'
           END as period
      WHERE d.qualityScore IS NOT NULL
      WITH period, avg(d.qualityScore) as avgScore
      RETURN collect({period: period, avgScore: avgScore}) as periods
    `;

    const qualityResult = await session.run(qualityQuery, {
      startDate: startDateStr,
      previousStartDate: previousStartDateStr,
      customerId,
    });

    const qualityPeriods = qualityResult.records[0]?.get('periods') || [];
    const currentQuality = qualityPeriods.find((p: any) => p.period === 'current')?.avgScore || 0;
    const previousQuality = qualityPeriods.find((p: any) => p.period === 'previous')?.avgScore || 0;

    // Calculate percentage changes
    const calculateChange = (current: number, previous: number): number => {
      if (previous === 0) return current > 0 ? 100 : 0;
      return ((current - previous) / previous) * 100;
    };

    const metrics: MetricsResponse = {
      documentGrowth: {
        current: currentDocs,
        previous: previousDocs,
        percentageChange: calculateChange(currentDocs, previousDocs),
      },
      entitiesAdded: {
        current: currentEntities,
        previous: previousEntities,
        percentageChange: calculateChange(currentEntities, previousEntities),
      },
      processSuccess: {
        current: Math.round(successRate * 10) / 10,
        percentageChange: 0, // No historical comparison for success rate
      },
      avgQuality: {
        current: Math.round(currentQuality * 10) / 10,
        previous: Math.round(previousQuality * 10) / 10,
        percentageChange: calculateChange(currentQuality, previousQuality),
      },
    };

    return NextResponse.json(metrics);
  } catch (error) {
    console.error('Error fetching analytics metrics:', error);
    return NextResponse.json(
      { error: 'Failed to fetch analytics metrics' },
      { status: 500 }
    );
  } finally {
    await session.close();
  }
}
