import { Neo4jEnhanced } from './neo4j-enhanced';
import { openai } from '@ai-sdk/openai';
import { generateText } from 'ai';

export interface DataSource {
  neo4j: boolean;
  qdrant: boolean;
  internet: boolean;
}

export interface QueryContext {
  customer?: string;
  scope?: string;
  projectId?: string;
}

export interface SourceResult {
  source: 'neo4j' | 'qdrant' | 'internet';
  content: string;
  metadata?: Record<string, any>;
  relevance?: number;
}

export class AIOrchestrator {
  async orchestrateQuery(
    query: string,
    context: QueryContext,
    dataSources: DataSource
  ): Promise<SourceResult[]> {
    const results: SourceResult[] = [];

    // Parallel execution of all enabled data sources
    const promises: Promise<void>[] = [];

    if (dataSources.neo4j) {
      promises.push(this.queryNeo4j(query, context).then(r => { results.push(...r); }));
    }

    if (dataSources.qdrant) {
      promises.push(this.queryQdrant(query, context).then(r => { results.push(...r); }));
    }

    if (dataSources.internet) {
      promises.push(this.queryInternet(query).then(r => { results.push(...r); }));
    }

    await Promise.all(promises);

    // Rank and deduplicate results
    return this.rankResults(results);
  }

  private async queryNeo4j(query: string, context: QueryContext): Promise<SourceResult[]> {
    try {
      // Determine query intent and construct appropriate Cypher
      const intent = await this.analyzeIntent(query);

      let cypherQuery = '';
      let params: Record<string, any> = {};

      if (intent.includes('customer') || context.customer) {
        cypherQuery = `
          MATCH (c:Customer {name: $customerName})
          OPTIONAL MATCH (c)-[:HAS_PROJECT]->(p:Project)
          OPTIONAL MATCH (p)-[:HAS_DOCUMENT]->(d:Document)
          OPTIONAL MATCH (d)-[:HAS_CHUNK]->(ch:Chunk)
          WHERE ch.text CONTAINS $searchTerm OR d.name CONTAINS $searchTerm
          RETURN c, p, d, ch
          LIMIT 20
        `;
        params = {
          customerName: context.customer || 'McKenney',
          searchTerm: query.toLowerCase()
        };
      } else if (intent.includes('project') || context.projectId) {
        cypherQuery = `
          MATCH (p:Project)
          WHERE p.projectId = $projectId OR p.name CONTAINS $searchTerm
          OPTIONAL MATCH (p)-[:HAS_DOCUMENT]->(d:Document)
          OPTIONAL MATCH (d)-[:HAS_CHUNK]->(ch:Chunk)
          WHERE ch.text CONTAINS $searchTerm
          RETURN p, d, ch
          LIMIT 20
        `;
        params = {
          projectId: context.projectId || '',
          searchTerm: query.toLowerCase()
        };
      } else {
        // General full-text search across chunks
        cypherQuery = `
          MATCH (ch:Chunk)
          WHERE ch.text CONTAINS $searchTerm
          MATCH (ch)<-[:HAS_CHUNK]-(d:Document)<-[:HAS_DOCUMENT]-(p:Project)
          RETURN ch, d, p
          LIMIT 20
        `;
        params = { searchTerm: query.toLowerCase() };
      }

      const neo4jClient = new Neo4jEnhanced();
      let records: any[] = [];

      try {
        const session = neo4jClient['getSession']();
        const result = await session.run(cypherQuery, params);
        records = result.records;
        await session.close();
      } finally {
        await neo4jClient.close();
      }

      return records.map((record, idx) => {
        const chunk = record.get('ch');
        const doc = record.get('d');
        const project = record.get('p');

        return {
          source: 'neo4j' as const,
          content: chunk?.properties?.text || doc?.properties?.name || 'No content',
          metadata: {
            document: doc?.properties?.name,
            project: project?.properties?.name,
            chunkId: chunk?.properties?.chunkId
          },
          relevance: 1.0 - (idx * 0.05)
        };
      });
    } catch (error) {
      console.error('Neo4j query error:', error);
      return [];
    }
  }

  private async queryQdrant(query: string, context: QueryContext): Promise<SourceResult[]> {
    try {
      // Generate embedding for semantic search
      const embedding = await this.generateEmbedding(query);

      // Query Qdrant vector database
      const response = await fetch('http://localhost:6333/collections/documents/points/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          vector: embedding,
          limit: 10,
          with_payload: true,
          filter: context.customer ? {
            must: [{ key: 'customer', match: { value: context.customer } }]
          } : undefined
        })
      });

      if (!response.ok) {
        throw new Error('Qdrant query failed');
      }

      const data = await response.json();

      return data.result?.map((hit: any) => ({
        source: 'qdrant' as const,
        content: hit.payload?.text || hit.payload?.content || '',
        metadata: {
          document: hit.payload?.document,
          score: hit.score
        },
        relevance: hit.score
      })) || [];
    } catch (error) {
      console.error('Qdrant query error:', error);
      return [];
    }
  }

  private async queryInternet(query: string): Promise<SourceResult[]> {
    try {
      // Use Tavily or fallback to web search
      const tavily_api_key = process.env.TAVILY_API_KEY;

      if (tavily_api_key) {
        const response = await fetch('https://api.tavily.com/search', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${tavily_api_key}`
          },
          body: JSON.stringify({
            query,
            search_depth: 'basic',
            max_results: 5
          })
        });

        if (response.ok) {
          const data = await response.json();
          return data.results?.map((result: any) => ({
            source: 'internet' as const,
            content: result.content || result.snippet || '',
            metadata: {
              url: result.url,
              title: result.title
            },
            relevance: result.score || 0.5
          })) || [];
        }
      }

      // Fallback: generate synthetic internet context
      return [{
        source: 'internet' as const,
        content: 'Internet search is currently unavailable. Configure TAVILY_API_KEY for web search.',
        metadata: {},
        relevance: 0.1
      }];
    } catch (error) {
      console.error('Internet search error:', error);
      return [];
    }
  }

  private async analyzeIntent(query: string): Promise<string> {
    // Simple keyword-based intent detection
    const lower = query.toLowerCase();
    if (lower.includes('customer') || lower.includes('client')) return 'customer';
    if (lower.includes('project')) return 'project';
    if (lower.includes('document') || lower.includes('file')) return 'document';
    return 'general';
  }

  private async generateEmbedding(text: string): Promise<number[]> {
    try {
      const response = await fetch('https://api.openai.com/v1/embeddings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
        },
        body: JSON.stringify({
          model: 'text-embedding-3-small',
          input: text
        })
      });

      const data = await response.json();
      return data.data[0].embedding;
    } catch (error) {
      console.error('Embedding generation error:', error);
      return new Array(1536).fill(0);
    }
  }

  private rankResults(results: SourceResult[]): SourceResult[] {
    // Sort by relevance and deduplicate similar content
    const sorted = results.sort((a, b) => (b.relevance || 0) - (a.relevance || 0));

    const deduplicated: SourceResult[] = [];
    const seen = new Set<string>();

    for (const result of sorted) {
      const key = result.content.substring(0, 100);
      if (!seen.has(key)) {
        seen.add(key);
        deduplicated.push(result);
      }
    }

    return deduplicated.slice(0, 15); // Top 15 results
  }

  async synthesizeResponse(
    query: string,
    sourceResults: SourceResult[],
    context: QueryContext
  ): Promise<string> {
    const contextText = sourceResults
      .map((r, idx) => `[${r.source.toUpperCase()} ${idx + 1}]\n${r.content}`)
      .join('\n\n');

    const systemPrompt = `You are an AI assistant for McKenney's construction project management system.
You have access to:
- Neo4j graph database (project relationships, documents, metadata)
- Qdrant vector database (semantic document search)
- Internet search (general knowledge)

Current context:
- Customer: ${context.customer || 'Not specified'}
- Scope: ${context.scope || 'Not specified'}
- Project: ${context.projectId || 'Not specified'}

Provide helpful, accurate answers based on the context provided. Cite sources when relevant.`;

    try {
      const { text } = await generateText({
        model: openai('gpt-4o-mini'),
        system: systemPrompt,
        messages: [
          {
            role: 'user',
            content: `Based on these sources:\n\n${contextText}\n\nAnswer this question: ${query}`
          }
        ]
      } as any);

      return text;
    } catch (error) {
      console.error('Response synthesis error:', error);
      return 'I apologize, but I encountered an error generating a response. Please try again.';
    }
  }
}

export const aiOrchestrator = new AIOrchestrator();
