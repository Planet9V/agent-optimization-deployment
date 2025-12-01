import { NextRequest, NextResponse } from 'next/server';
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://openspg-neo4j:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USER || 'neo4j',
    process.env.NEO4J_PASSWORD || 'neo4j@openspg'
  )
);

interface SeasonalityCell {
  year: number;
  month: number;
  count: number;
  campaigns: string[];
}

interface SeasonalityResponse {
  heatmap: SeasonalityCell[];
  years: number[];
  months: number[];
  maxCount: number;
}

export async function GET(request: NextRequest) {
  const session = driver.session();

  try {
    // Query: Campaign Seasonality Pattern Analysis
    const seasonalityQuery = `
      MATCH (c:Campaign)
      WHERE c.first_seen IS NOT NULL
      WITH
        toInteger(substring(toString(c.first_seen), 0, 4)) as year,
        toInteger(substring(toString(c.first_seen), 5, 2)) as month,
        c
      WITH year, month,
        count(c) as campaign_count,
        collect(c.name)[0..10] as sample_campaigns
      ORDER BY year, month
      RETURN year, month, campaign_count, sample_campaigns
    `;

    const result = await session.run(seasonalityQuery);

    const heatmap: SeasonalityCell[] = [];
    const yearSet = new Set<number>();
    const monthSet = new Set<number>();
    let maxCount = 0;

    result.records.forEach(record => {
      // Convert BigInt to Number for year/month
      const year = Number(record.get('year'));
      const month = Number(record.get('month'));
      const count = record.get('campaign_count').toNumber();
      const campaigns = record.get('sample_campaigns');

      yearSet.add(year);
      monthSet.add(month);
      maxCount = Math.max(maxCount, count);

      heatmap.push({
        year,
        month,
        count,
        campaigns,
      });
    });

    const response: SeasonalityResponse = {
      heatmap,
      years: Array.from(yearSet).sort((a, b) => b - a), // Most recent first
      months: Array.from(monthSet).sort((a, b) => a - b),
      maxCount,
    };

    return NextResponse.json(response);
  } catch (error) {
    console.error('Error fetching seasonality data:', error);
    return NextResponse.json(
      { error: 'Failed to fetch seasonality data' },
      { status: 500 }
    );
  } finally {
    await session.close();
  }
}
