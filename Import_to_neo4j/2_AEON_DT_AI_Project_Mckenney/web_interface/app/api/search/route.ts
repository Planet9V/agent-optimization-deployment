import { NextRequest, NextResponse } from 'next/server';
import { hybridSearch, checkSearchHealth, type HybridSearchOptions } from '@/lib/hybrid-search';

// POST /api/search - Execute hybrid search
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const {
      query,
      mode = 'hybrid',
      customer,
      tags,
      dateFrom,
      dateTo,
      limit = 10,
      k = 60,
      // Cybersecurity filters
      nodeTypes,
      cvssSeverity,
      mitreTactic,
      // VulnCheck-style facets
      severities,
      types,
    } = body;

    // Validate required fields
    if (!query || typeof query !== 'string' || query.trim().length === 0) {
      return NextResponse.json(
        { error: 'Query parameter is required and must be a non-empty string' },
        { status: 400 }
      );
    }

    // Validate mode
    if (!['fulltext', 'semantic', 'hybrid'].includes(mode)) {
      return NextResponse.json(
        { error: 'Mode must be one of: fulltext, semantic, hybrid' },
        { status: 400 }
      );
    }

    // Build search options
    const searchOptions: HybridSearchOptions = {
      query: query.trim(),
      mode,
      limit: Math.min(limit, 100), // Cap at 100 results
      k,
    };

    // Add filters if provided
    if (customer || tags || dateFrom || dateTo || nodeTypes || cvssSeverity || mitreTactic || severities || types) {
      searchOptions.filters = {};

      if (customer) {
        searchOptions.filters.customer = customer;
      }

      if (tags && Array.isArray(tags) && tags.length > 0) {
        searchOptions.filters.tags = tags;
      }

      if (dateFrom) {
        searchOptions.filters.dateFrom = dateFrom;
      }

      if (dateTo) {
        searchOptions.filters.dateTo = dateTo;
      }

      // Cybersecurity filters
      if (nodeTypes && Array.isArray(nodeTypes) && nodeTypes.length > 0) {
        searchOptions.filters.nodeTypes = nodeTypes;
      }

      if (cvssSeverity) {
        searchOptions.filters.cvssSeverity = cvssSeverity;
      }

      if (mitreTactic) {
        searchOptions.filters.mitreTactic = mitreTactic;
      }

      // VulnCheck-style facets
      if (severities && Array.isArray(severities) && severities.length > 0) {
        searchOptions.filters.severities = severities;
      }

      if (types && Array.isArray(types) && types.length > 0) {
        searchOptions.filters.types = types;
      }
    }

    // Execute search
    const results = await hybridSearch(searchOptions);

    return NextResponse.json({
      success: true,
      query: searchOptions.query,
      mode: searchOptions.mode,
      filters: searchOptions.filters,
      results,
      count: results.length,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Search API error:', error);
    return NextResponse.json(
      {
        error: 'Internal server error',
        message: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}

// GET /api/search/health - Check search services health
export async function GET() {
  try {
    const health = await checkSearchHealth();

    const allHealthy = health.neo4j && health.qdrant && health.openai;

    return NextResponse.json({
      status: allHealthy ? 'healthy' : 'degraded',
      services: health,
      timestamp: new Date().toISOString(),
    }, {
      status: allHealthy ? 200 : 503,
    });
  } catch (error) {
    console.error('Health check error:', error);
    return NextResponse.json(
      {
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString(),
      },
      { status: 500 }
    );
  }
}
