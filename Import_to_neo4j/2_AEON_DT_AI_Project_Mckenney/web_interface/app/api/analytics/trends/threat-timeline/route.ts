import { NextRequest, NextResponse } from 'next/server';
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://openspg-neo4j:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USER || 'neo4j',
    process.env.NEO4J_PASSWORD || 'neo4j@openspg'
  )
);

interface CampaignDetail {
  name: string;
  firstSeen: string;
  lastSeen: string;
  durationDays: number;
}

interface ThreatActivity {
  month: string;
  threatActor: string;
  campaigns: number;
  campaignDetails: CampaignDetail[];
}

interface ThreatTimelineResponse {
  timeline: ThreatActivity[];
  totalActors: number;
  totalCampaigns: number;
}

function calculateStartDate(params: URLSearchParams): Date {
  const startDateParam = params.get('startDate');
  if (startDateParam) {
    return new Date(startDateParam);
  }

  // Default: 5 years ago to capture historical campaign data
  const date = new Date();
  date.setFullYear(date.getFullYear() - 5);
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
    // Query: Threat Actor Campaign Timeline (show all historical data)
    // Note: Date filtering removed due to dataset size (only 43 campaigns with actors)
    const timelineQuery = `
      MATCH (ta:ThreatActor)-[:ORCHESTRATES_CAMPAIGN]->(c:Campaign)
      WHERE c.first_seen IS NOT NULL
      WITH
        toString(substring(toString(c.first_seen), 0, 7)) as month,
        COALESCE(ta.name, 'Unknown') as threat_actor,
        c.name as campaign_name,
        c.first_seen as first_seen,
        c.last_seen as last_seen
      WITH month, threat_actor,
        count(*) as campaign_count,
        collect(campaign_name)[0..10] as campaign_names,
        collect(first_seen)[0..10] as first_seens,
        collect(last_seen)[0..10] as last_seens
      ORDER BY month DESC, campaign_count DESC
      RETURN month, threat_actor, campaign_count, campaign_names, first_seens, last_seens
      LIMIT 100
    `;

    const result = await session.run(timelineQuery);

    const timeline: ThreatActivity[] = [];
    const actorSet = new Set<string>();
    let totalCampaigns = 0;

    result.records.forEach(record => {
      const month = record.get('month');
      const threatActor = record.get('threat_actor') || 'Unknown';
      const campaignCount = record.get('campaign_count').toNumber();
      const campaignNames = record.get('campaign_names') || [];
      const firstSeens = record.get('first_seens') || [];
      const lastSeens = record.get('last_seens') || [];

      actorSet.add(threatActor);
      totalCampaigns += campaignCount;

      // Reconstruct campaign details from separate arrays
      const campaignDetails: CampaignDetail[] = campaignNames.map((name: string, idx: number) => {
        const firstSeen = firstSeens[idx];
        const lastSeen = lastSeens[idx];
        let durationDays = 0;

        if (firstSeen && lastSeen) {
          const first = new Date(firstSeen.toString());
          const last = new Date(lastSeen.toString());
          durationDays = Math.floor((last.getTime() - first.getTime()) / (1000 * 60 * 60 * 24));
        }

        return {
          name,
          firstSeen: firstSeen ? firstSeen.toString() : '',
          lastSeen: lastSeen ? lastSeen.toString() : '',
          durationDays,
        };
      });

      timeline.push({
        month,
        threatActor,
        campaigns: campaignCount,
        campaignDetails,
      });
    });

    const response: ThreatTimelineResponse = {
      timeline,
      totalActors: actorSet.size,
      totalCampaigns,
    };

    return NextResponse.json(response);
  } catch (error) {
    console.error('Error fetching threat timeline:', error);
    return NextResponse.json(
      { error: 'Failed to fetch threat timeline data' },
      { status: 500 }
    );
  } finally {
    await session.close();
  }
}
