import { NextRequest, NextResponse } from 'next/server';
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://openspg-neo4j:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USER || 'neo4j',
    process.env.NEO4J_PASSWORD || 'neo4j@openspg'
  )
);

interface MonthlyTrend {
  month: string;
  critical: number;
  high: number;
  medium: number;
  low: number;
  avgSystemsAffected?: number;
}

interface CVETrendsResponse {
  monthlyTrends: MonthlyTrend[];
  totalCount: number;
  percentChange: number;
  totalSystemsAffected?: number;
}

function calculateStartDate(params: URLSearchParams): Date {
  const startDateParam = params.get('startDate');
  if (startDateParam) {
    return new Date(startDateParam);
  }

  // Default: 6 months ago
  const date = new Date();
  date.setMonth(date.getMonth() - 6);
  return date;
}

function calculateEndDate(params: URLSearchParams): Date {
  const endDateParam = params.get('endDate');
  if (endDateParam) {
    return new Date(endDateParam);
  }

  // Default: now
  return new Date();
}

export async function GET(request: NextRequest) {
  const session = driver.session();

  try {
    const searchParams = request.nextUrl.searchParams;
    const startDate = calculateStartDate(searchParams);
    const endDate = calculateEndDate(searchParams);

    // Calculate previous period for comparison
    const periodLength = endDate.getTime() - startDate.getTime();
    const previousStartDate = new Date(startDate.getTime() - periodLength);

    // Query 1: Monthly CVE trends by priority tier with system impact
    const trendsQuery = `
      MATCH (c:CVE)
      WHERE c.published_date >= datetime($startDate) AND c.published_date < datetime($endDate)
      OPTIONAL MATCH (c)-[:VULNERABLE_TO]->(system)
      WITH
        toString(substring(toString(c.published_date), 0, 7)) as month,
        CASE c.priority_tier
          WHEN 'NOW' THEN 'critical'
          WHEN 'NEXT' THEN 'high'
          WHEN 'NEVER' THEN 'medium'
          ELSE 'low'
        END as severity,
        c,
        count(DISTINCT system) as system_count
      WITH month, severity, count(c) as cve_count, avg(system_count) as avg_systems
      ORDER BY month, severity
      RETURN month, severity, cve_count as count, toInteger(avg_systems) as avgSystemsAffected
    `;

    const trendsResult = await session.run(trendsQuery, {
      startDate: startDate.toISOString(),
      endDate: endDate.toISOString(),
    });

    // Transform results into monthly trends
    const monthlyMap = new Map<string, MonthlyTrend>();

    let totalSystemsAffected = 0;
    let systemCountEntries = 0;

    trendsResult.records.forEach(record => {
      const month = record.get('month');
      const severity = record.get('severity');
      const count = record.get('count').toNumber();
      const avgSystems = record.get('avgSystemsAffected')?.toNumber() || 0;

      if (!monthlyMap.has(month)) {
        monthlyMap.set(month, {
          month,
          critical: 0,
          high: 0,
          medium: 0,
          low: 0,
          avgSystemsAffected: 0,
        });
      }

      const monthData = monthlyMap.get(month)!;
      monthData[severity as keyof Omit<MonthlyTrend, 'month' | 'avgSystemsAffected'>] = count;

      // Track average systems affected
      if (avgSystems > 0) {
        totalSystemsAffected += avgSystems;
        systemCountEntries++;
      }
    });

    // Calculate overall average systems affected
    const overallAvgSystems = systemCountEntries > 0
      ? Math.round(totalSystemsAffected / systemCountEntries)
      : 0;

    const monthlyTrends = Array.from(monthlyMap.values()).sort(
      (a, b) => a.month.localeCompare(b.month)
    );

    // Query 2: Total count and period comparison
    const comparisonQuery = `
      MATCH (c:CVE)
      WHERE c.published_date >= datetime($previousStartDate) AND c.published_date < datetime($endDate)
      WITH
        CASE
          WHEN c.published_date >= datetime($currentStartDate) THEN 'current'
          ELSE 'previous'
        END as period
      RETURN period, count(*) as count
    `;

    const comparisonResult = await session.run(comparisonQuery, {
      previousStartDate: previousStartDate.toISOString(),
      currentStartDate: startDate.toISOString(),
      endDate: endDate.toISOString(),
    });

    let currentCount = 0;
    let previousCount = 0;

    comparisonResult.records.forEach(record => {
      const period = record.get('period');
      const count = record.get('count').toNumber();

      if (period === 'current') {
        currentCount = count;
      } else {
        previousCount = count;
      }
    });

    // Calculate percent change
    const percentChange = previousCount > 0
      ? Math.round(((currentCount - previousCount) / previousCount) * 100)
      : 0;

    const response: CVETrendsResponse = {
      monthlyTrends,
      totalCount: currentCount,
      percentChange,
      totalSystemsAffected: overallAvgSystems,
    };

    return NextResponse.json(response);
  } catch (error) {
    console.error('Error fetching CVE trends:', error);
    return NextResponse.json(
      { error: 'Failed to fetch CVE trends data' },
      { status: 500 }
    );
  } finally {
    await session.close();
  }
}
