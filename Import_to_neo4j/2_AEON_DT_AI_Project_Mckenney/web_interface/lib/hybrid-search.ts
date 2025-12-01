import { QdrantClient } from '@qdrant/js-client-rest';
import OpenAI from 'openai';
import neo4j, { Driver, Session } from 'neo4j-driver';

// TypeScript interfaces
export interface SearchResult {
  id: string;
  type: 'document' | 'entity' | 'requirement';
  title: string;
  content: string;
  score: number;
  source: 'neo4j' | 'qdrant' | 'hybrid';
  metadata: {
    customer?: string;
    tags?: string[];
    date?: string;
    documentId?: string;
    entityType?: string;
  };
}

export interface SearchFilters {
  customer?: string;
  tags?: string[];
  dateFrom?: string;
  dateTo?: string;
  // Cybersecurity filters
  nodeTypes?: string[];
  cvssSeverity?: {
    min: number;
    max: number;
  };
  mitreTactic?: string;
  // VulnCheck-style facets
  severities?: string[];
  types?: string[];
}

export interface HybridSearchOptions {
  query: string;
  mode: 'fulltext' | 'semantic' | 'hybrid';
  filters?: SearchFilters;
  limit?: number;
  k?: number; // RRF parameter
}

// Initialize clients
const qdrantClient = new QdrantClient({
  url: process.env.QDRANT_URL || 'http://localhost:6333',
  apiKey: process.env.QDRANT_API_KEY,
});

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Neo4j driver instance
let driver: Driver | null = null;

function getNeo4jDriver(): Driver {
  if (!driver) {
    driver = neo4j.driver(
      process.env.NEO4J_URI || 'bolt://localhost:7687',
      neo4j.auth.basic(
        process.env.NEO4J_USER || 'neo4j',
        process.env.NEO4J_PASSWORD || 'neo4j@openspg'
      )
    );
  }
  return driver;
}

function getNeo4jSession(): Session {
  return getNeo4jDriver().session();
}

// Generate embeddings for query
async function generateEmbedding(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text,
    encoding_format: 'float',
  });

  return response.data[0].embedding;
}

// Full-text search in Neo4j
async function fullTextSearch(
  query: string,
  filters?: SearchFilters,
  limit: number = 10
): Promise<SearchResult[]> {
  const session = getNeo4jSession();

  try {
    let cypher = `
      CALL db.index.fulltext.queryNodes('documentSearch', $query)
      YIELD node, score
      WHERE 1=1
    `;

    const params: any = { query };

    if (filters?.customer) {
      cypher += ` AND node.customer = $customer`;
      params.customer = filters.customer;
    }

    if (filters?.tags && filters.tags.length > 0) {
      cypher += ` AND ANY(tag IN node.tags WHERE tag IN $tags)`;
      params.tags = filters.tags;
    }

    if (filters?.dateFrom) {
      cypher += ` AND node.date >= $dateFrom`;
      params.dateFrom = filters.dateFrom;
    }

    if (filters?.dateTo) {
      cypher += ` AND node.date <= $dateTo`;
      params.dateTo = filters.dateTo;
    }

    // Cybersecurity filters
    if (filters?.nodeTypes && filters.nodeTypes.length > 0) {
      cypher += ` AND labels(node)[0] IN $nodeTypes`;
      params.nodeTypes = filters.nodeTypes;
    }

    if (filters?.cvssSeverity) {
      cypher += ` AND node.cvss_score >= $cvssMin AND node.cvss_score <= $cvssMax`;
      params.cvssMin = filters.cvssSeverity.min;
      params.cvssMax = filters.cvssSeverity.max;
    }

    if (filters?.mitreTactic) {
      cypher += ` AND $mitreTactic IN node.mitre_tactics`;
      params.mitreTactic = filters.mitreTactic;
    }

    // VulnCheck-style severity facets (map to CVSS ranges)
    if (filters?.severities && filters.severities.length > 0) {
      const severityConditions = filters.severities.map(sev => {
        switch(sev) {
          case 'CRITICAL': return '(node.cvss_score >= 9.0 AND node.cvss_score <= 10.0)';
          case 'HIGH': return '(node.cvss_score >= 7.0 AND node.cvss_score < 9.0)';
          case 'MEDIUM': return '(node.cvss_score >= 4.0 AND node.cvss_score < 7.0)';
          case 'LOW': return '(node.cvss_score >= 0.0 AND node.cvss_score < 4.0)';
          default: return 'false';
        }
      }).join(' OR ');
      cypher += ` AND (${severityConditions})`;
    }

    // VulnCheck-style type facets
    if (filters?.types && filters.types.length > 0) {
      cypher += ` AND labels(node)[0] IN $types`;
      params.types = filters.types;
    }

    cypher += `
      RETURN node.id AS id,
             labels(node)[0] AS type,
             node.title AS title,
             node.content AS content,
             score,
             node.customer AS customer,
             node.tags AS tags,
             node.date AS date,
             node.documentId AS documentId
      ORDER BY score DESC
      LIMIT $limit
    `;

    params.limit = limit;

    const result = await session.run(cypher, params);

    return result.records.map((record: any) => ({
      id: record.get('id'),
      type: record.get('type')?.toLowerCase() || 'document',
      title: record.get('title') || 'Untitled',
      content: record.get('content') || '',
      score: record.get('score'),
      source: 'neo4j' as const,
      metadata: {
        customer: record.get('customer'),
        tags: record.get('tags') || [],
        date: record.get('date'),
        documentId: record.get('documentId'),
      },
    }));
  } finally {
    await session.close();
  }
}

// Semantic search in Qdrant
async function semanticSearch(
  query: string,
  filters?: SearchFilters,
  limit: number = 10
): Promise<SearchResult[]> {
  // Generate query embedding
  const queryVector = await generateEmbedding(query);

  // Build Qdrant filters
  const qdrantFilters: any = {
    must: [],
  };

  if (filters?.customer) {
    qdrantFilters.must.push({
      key: 'customer',
      match: { value: filters.customer },
    });
  }

  if (filters?.tags && filters.tags.length > 0) {
    qdrantFilters.must.push({
      key: 'tags',
      match: { any: filters.tags },
    });
  }

  if (filters?.dateFrom || filters?.dateTo) {
    const dateFilter: any = { key: 'date' };
    if (filters.dateFrom && filters.dateTo) {
      dateFilter.range = {
        gte: filters.dateFrom,
        lte: filters.dateTo,
      };
    } else if (filters.dateFrom) {
      dateFilter.range = { gte: filters.dateFrom };
    } else if (filters.dateTo) {
      dateFilter.range = { lte: filters.dateTo };
    }
    qdrantFilters.must.push(dateFilter);
  }

  // Cybersecurity filters
  if (filters?.nodeTypes && filters.nodeTypes.length > 0) {
    qdrantFilters.must.push({
      key: 'type',
      match: { any: filters.nodeTypes },
    });
  }

  if (filters?.cvssSeverity) {
    qdrantFilters.must.push({
      key: 'cvss_score',
      range: {
        gte: filters.cvssSeverity.min,
        lte: filters.cvssSeverity.max,
      },
    });
  }

  if (filters?.mitreTactic) {
    qdrantFilters.must.push({
      key: 'mitre_tactics',
      match: { value: filters.mitreTactic },
    });
  }

  // VulnCheck-style severity facets
  if (filters?.severities && filters.severities.length > 0) {
    const severityRanges = filters.severities.map(sev => {
      switch(sev) {
        case 'CRITICAL': return { gte: 9.0, lte: 10.0 };
        case 'HIGH': return { gte: 7.0, lt: 9.0 };
        case 'MEDIUM': return { gte: 4.0, lt: 7.0 };
        case 'LOW': return { gte: 0.0, lt: 4.0 };
        default: return null;
      }
    }).filter(r => r !== null);

    if (severityRanges.length > 0) {
      qdrantFilters.must.push({
        should: severityRanges.map(range => ({
          key: 'cvss_score',
          range,
        })),
      });
    }
  }

  // VulnCheck-style type facets
  if (filters?.types && filters.types.length > 0) {
    qdrantFilters.must.push({
      key: 'type',
      match: { any: filters.types },
    });
  }

  // Search in Qdrant
  const searchResult = await qdrantClient.search('documents', {
    vector: queryVector,
    filter: qdrantFilters.must.length > 0 ? qdrantFilters : undefined,
    limit,
    with_payload: true,
  });

  return searchResult.map((point: any) => ({
    id: point.id.toString(),
    type: point.payload.type || 'document',
    title: point.payload.title || 'Untitled',
    content: point.payload.content || '',
    score: point.score,
    source: 'qdrant' as const,
    metadata: {
      customer: point.payload.customer,
      tags: point.payload.tags || [],
      date: point.payload.date,
      documentId: point.payload.documentId,
      entityType: point.payload.entityType,
    },
  }));
}

// Reciprocal Rank Fusion
function reciprocalRankFusion(
  results: SearchResult[][],
  k: number = 60
): SearchResult[] {
  const scoreMap = new Map<string, { result: SearchResult; score: number }>();

  results.forEach((resultSet) => {
    resultSet.forEach((result, rank) => {
      const rrfScore = 1 / (k + rank + 1);

      const existing = scoreMap.get(result.id);
      if (existing) {
        existing.score += rrfScore;
      } else {
        scoreMap.set(result.id, {
          result: { ...result, source: 'hybrid' as const },
          score: rrfScore,
        });
      }
    });
  });

  return Array.from(scoreMap.values())
    .map(({ result, score }) => ({ ...result, score }))
    .sort((a, b) => b.score - a.score);
}

// Main hybrid search function
export async function hybridSearch(
  options: HybridSearchOptions
): Promise<SearchResult[]> {
  const { query, mode, filters, limit = 10, k = 60 } = options;

  try {
    switch (mode) {
      case 'fulltext': {
        return await fullTextSearch(query, filters, limit);
      }

      case 'semantic': {
        return await semanticSearch(query, filters, limit);
      }

      case 'hybrid': {
        // Execute both searches in parallel
        const [neo4jResults, qdrantResults] = await Promise.all([
          fullTextSearch(query, filters, limit),
          semanticSearch(query, filters, limit),
        ]);

        // Merge results using RRF
        const mergedResults = reciprocalRankFusion(
          [neo4jResults, qdrantResults],
          k
        );

        return mergedResults.slice(0, limit);
      }

      default:
        throw new Error(`Invalid search mode: ${mode}`);
    }
  } catch (error) {
    console.error('Hybrid search error:', error);
    throw error;
  }
}

// Create full-text index in Neo4j (run once during setup)
export async function createFullTextIndex(): Promise<void> {
  const session = getNeo4jSession();

  try {
    await session.run(`
      CREATE FULLTEXT INDEX documentSearch IF NOT EXISTS
      FOR (n:Document|Entity|Requirement)
      ON EACH [n.title, n.content, n.name, n.description]
    `);
    console.log('Full-text index created successfully');
  } catch (error) {
    console.error('Error creating full-text index:', error);
    throw error;
  } finally {
    await session.close();
  }
}

// Health check for search services
export async function checkSearchHealth(): Promise<{
  neo4j: boolean;
  qdrant: boolean;
  openai: boolean;
}> {
  const health = {
    neo4j: false,
    qdrant: false,
    openai: false,
  };

  // Check Neo4j
  const session = getNeo4jSession();
  try {
    await session.run('RETURN 1');
    health.neo4j = true;
  } catch (error) {
    console.error('Neo4j health check failed:', error);
  } finally {
    await session.close();
  }

  // Check Qdrant
  try {
    await qdrantClient.getCollections();
    health.qdrant = true;
  } catch (error) {
    console.error('Qdrant health check failed:', error);
  }

  // Check OpenAI
  try {
    await openai.models.list();
    health.openai = true;
  } catch (error) {
    console.error('OpenAI health check failed:', error);
  }

  return health;
}

// Cleanup function to close Neo4j driver
export async function closeNeo4jDriver(): Promise<void> {
  if (driver) {
    await driver.close();
    driver = null;
  }
}
