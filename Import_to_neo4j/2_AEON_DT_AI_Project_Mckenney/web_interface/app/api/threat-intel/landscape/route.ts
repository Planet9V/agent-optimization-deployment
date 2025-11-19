import { NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  process.env.NEO4J_URI || 'bolt://openspg-neo4j:7687',
  neo4j.auth.basic(
    process.env.NEO4J_USER || 'neo4j',
    process.env.NEO4J_PASSWORD || 'neo4j@openspg'
  )
);

interface ThreatActor {
  name: string;
  location: string;
  campaigns: number;
  status: 'active' | 'monitoring' | 'dormant';
  campaignNames: string[];
  impactedSectors: string[][];
  lastActivity: string | null;
}

interface Industry {
  name: string;
  attacks: number;
  percent: number;
}

interface Campaign {
  name: string;
  actor: string;
  started: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  ttpCount: number;
}

interface LandscapeResponse {
  threatActors: ThreatActor[];
  industries: Industry[];
  campaigns: Campaign[];
  totalActors: number;
  activeCampaigns: number;
}

export async function GET() {
  // Verify authentication
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  let session1, session2, session3;

  try {
    // Query 1.1: Threat Actor Campaign Summary (4-6 hops)
    const actorQuery = `
      MATCH (ta:ThreatActor)
      WHERE ta.name IS NOT NULL

      OPTIONAL MATCH (ta)-[:ORCHESTRATES_CAMPAIGN|RELATED_TO*1..2]->(c:Campaign)

      OPTIONAL MATCH path = (c)-[*1..4]-(s:Sector)
      WHERE s.name IS NOT NULL

      WITH ta,
           collect(DISTINCT c) as campaigns,
           collect(DISTINCT s) as sectors,
           count(DISTINCT c) as campaign_count

      WITH ta, campaigns, sectors, campaign_count,
           [c IN campaigns WHERE c.last_seen IS NOT NULL
            | c] as recent_campaigns

      RETURN ta.name as name,
             COALESCE(ta.location, 'Unknown') as location,
             campaign_count as campaigns,
             CASE
               WHEN size(recent_campaigns) > 0 THEN 'active'
               WHEN campaign_count > 0 THEN 'monitoring'
               ELSE 'dormant'
             END as status,
             [c in campaigns[0..5] | c.name] as campaign_names,
             [s in sectors[0..3] | s.name] as impacted_sectors,
             recent_campaigns[0].last_seen as last_activity

      ORDER BY campaign_count DESC, last_activity DESC
      LIMIT 20
    `;

    // Query 1.2: Industry Targeting Analysis (5-7 hops)
    const industryQuery = `
      MATCH (s:Sector)<-[*1..5]-(c:Campaign)
      WHERE s.name IS NOT NULL AND c.name IS NOT NULL

      WITH s, count(DISTINCT c) as attack_count

      WITH s, attack_count, sum(attack_count) as total
      WITH s, attack_count,
           toInteger((toFloat(attack_count) / toFloat(total)) * 100) as percent

      RETURN s.name as name,
             attack_count as attacks,
             percent

      ORDER BY attack_count DESC
      LIMIT 10
    `;

    // Query 1.3: Recent Campaigns with Attribution (3-4 hops)
    const campaignQuery = `
      MATCH (c:Campaign)-[:RELATED_TO]-(ta:ThreatActor)
      WHERE c.first_seen IS NOT NULL
        AND c.name IS NOT NULL
        AND ta.name IS NOT NULL

      OPTIONAL MATCH (c)-[*1..3]-(ttp:TTP)
      WHERE ttp.technique_id IS NOT NULL

      WITH c, ta, count(DISTINCT ttp) as technique_count

      RETURN c.name as name,
             ta.name as actor,
             toString(c.first_seen) as started,
             CASE
               WHEN technique_count > 10 THEN 'critical'
               WHEN technique_count > 5 THEN 'high'
               ELSE 'medium'
             END as severity,
             technique_count as ttp_count

      ORDER BY c.first_seen DESC
      LIMIT 15
    `;

    // Execute all queries in parallel with separate sessions
    session1 = driver.session();
    session2 = driver.session();
    session3 = driver.session();

    const [actorResult, industryResult, campaignResult] = await Promise.all([
      session1.run(actorQuery),
      session2.run(industryQuery),
      session3.run(campaignQuery),
    ]);

    // Process Threat Actors
    const threatActors: ThreatActor[] = actorResult.records.map(record => ({
      name: record.get('name'),
      location: record.get('location'),
      campaigns: record.get('campaigns').toNumber ? record.get('campaigns').toNumber() : record.get('campaigns'),
      status: record.get('status') as 'active' | 'monitoring' | 'dormant',
      campaignNames: record.get('campaign_names') || [],
      impactedSectors: (record.get('impacted_sectors') || []).map((sector: unknown) =>
        typeof sector === 'string' ? [sector] : Array.isArray(sector) ? sector : []
      ),
      lastActivity: record.get('last_activity') ? record.get('last_activity').toString() : null,
    }));

    // Process Industries
    const industries: Industry[] = industryResult.records.map(record => ({
      name: record.get('name'),
      attacks: record.get('attacks').toNumber ? record.get('attacks').toNumber() : record.get('attacks'),
      percent: record.get('percent').toNumber ? record.get('percent').toNumber() : record.get('percent'),
    }));

    // Process Campaigns
    const campaigns: Campaign[] = campaignResult.records.map(record => ({
      name: record.get('name'),
      actor: record.get('actor'),
      started: record.get('started'),
      severity: record.get('severity') as 'critical' | 'high' | 'medium' | 'low',
      ttpCount: record.get('ttp_count').toNumber ? record.get('ttp_count').toNumber() : record.get('ttp_count'),
    }));

    // Calculate metrics
    const totalActors = threatActors.length;
    const activeCampaigns = threatActors.filter(ta => ta.status === 'active').length;

    const response: LandscapeResponse = {
      threatActors,
      industries,
      campaigns,
      totalActors,
      activeCampaigns,
    };

    return NextResponse.json(response);
  } catch (error) {
    console.error('Error fetching threat landscape data:', error);
    return NextResponse.json(
      { error: 'Failed to fetch threat landscape data', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  } finally {
    if (session1) await session1.close();
    if (session2) await session2.close();
    if (session3) await session3.close();
  }
}
