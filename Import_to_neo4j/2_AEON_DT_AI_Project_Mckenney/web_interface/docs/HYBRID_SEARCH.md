# Hybrid Search Implementation

## Overview

This implementation combines **Neo4j full-text search** with **Qdrant semantic search** using **Reciprocal Rank Fusion (RRF)** to provide powerful, accurate search across documents, entities, and requirements.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Search Interface                      │
│                  (app/search/page.tsx)                   │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                  API Route Handler                       │
│               (app/api/search/route.ts)                  │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                 Hybrid Search Engine                     │
│               (lib/hybrid-search.ts)                     │
├─────────────────────┬─────────────────┬─────────────────┤
│   Full-Text Search  │  Semantic Search│  RRF Fusion     │
└──────────┬──────────┴────────┬────────┴────────┬────────┘
           │                   │                  │
           ▼                   ▼                  ▼
    ┌──────────┐        ┌──────────┐      ┌──────────┐
    │  Neo4j   │        │  Qdrant  │      │   Merge  │
    │ Database │        │  Vector  │      │  Results │
    └──────────┘        │    DB    │      └──────────┘
                        └──────────┘
                              ▲
                              │
                        ┌──────────┐
                        │  OpenAI  │
                        │Embeddings│
                        └──────────┘
```

## Components

### 1. Hybrid Search Engine (`lib/hybrid-search.ts`)

Core search functionality with three modes:

#### **Full-Text Search (Neo4j)**
- Keyword-based search using Cypher full-text indexes
- Supports filtering by customer, tags, and date range
- Returns relevance scores based on text matching
- Fast and efficient for exact term matching

```typescript
const results = await hybridSearch({
  query: 'requirements documentation',
  mode: 'fulltext',
  filters: {
    customer: 'ACME Corp',
    tags: ['requirements'],
  },
  limit: 10
});
```

#### **Semantic Search (Qdrant)**
- Vector-based search using OpenAI embeddings
- Understands meaning and context, not just keywords
- Finds semantically similar content
- Ideal for natural language queries

```typescript
const results = await hybridSearch({
  query: 'how to implement user authentication',
  mode: 'semantic',
  limit: 10
});
```

#### **Hybrid Search (RRF)**
- Combines both full-text and semantic search
- Uses Reciprocal Rank Fusion algorithm
- Balances precision and recall
- Best overall search quality

```typescript
const results = await hybridSearch({
  query: 'system architecture requirements',
  mode: 'hybrid',
  limit: 10,
  k: 60 // RRF parameter
});
```

### 2. API Route (`app/api/search/route.ts`)

RESTful API endpoints for search operations:

#### **POST /api/search**
Execute search with parameters:
```json
{
  "query": "search term",
  "mode": "hybrid",
  "customer": "ACME Corp",
  "tags": ["requirements", "specification"],
  "dateFrom": "2024-01-01",
  "dateTo": "2024-12-31",
  "limit": 10
}
```

Response:
```json
{
  "success": true,
  "query": "search term",
  "mode": "hybrid",
  "results": [
    {
      "id": "doc-123",
      "type": "document",
      "title": "System Requirements",
      "content": "...",
      "score": 0.8542,
      "source": "hybrid",
      "metadata": {
        "customer": "ACME Corp",
        "tags": ["requirements"],
        "date": "2024-11-03"
      }
    }
  ],
  "count": 1
}
```

#### **GET /api/search/health**
Check service availability:
```json
{
  "status": "healthy",
  "services": {
    "neo4j": true,
    "qdrant": true,
    "openai": true
  }
}
```

### 3. Search Interface (`app/search/page.tsx`)

Full-featured search UI with:
- **Search modes**: Toggle between full-text, semantic, and hybrid
- **Filters**: Customer, tags, date range
- **Results display**: Highlighted matches, relevance scores
- **Responsive design**: Works on desktop and mobile

### 4. Result Components (`components/search/SearchResults.tsx`)

Display search results with:
- **Highlighted matching terms** in yellow
- **Relevance scores** with source indicators
- **Metadata** (customer, tags, date)
- **Result cards** with hover effects
- **Type and source badges**

## Reciprocal Rank Fusion (RRF)

The RRF algorithm merges results from multiple search sources:

```
RRF Score = Σ (1 / (k + rank))
```

Where:
- `k` = constant (default: 60)
- `rank` = position in result list (1-indexed)

### Example:
```
Document A:
  Neo4j rank: 1  → score = 1/(60+1) = 0.0164
  Qdrant rank: 3 → score = 1/(60+3) = 0.0159
  Total RRF = 0.0323

Document B:
  Neo4j rank: 2  → score = 1/(60+2) = 0.0161
  Qdrant rank: 1 → score = 1/(60+1) = 0.0164
  Total RRF = 0.0325  (Higher score, ranked first)
```

## Setup

### 1. Environment Variables

Create `.env.local`:
```bash
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg

# Qdrant Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-qdrant-api-key

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
```

### 2. Install Dependencies

```bash
npm install @qdrant/js-client-rest openai neo4j-driver
npm install @radix-ui/react-checkbox class-variance-authority
```

### 3. Create Full-Text Index

Run once to create Neo4j full-text index:

```typescript
import { createFullTextIndex } from '@/lib/hybrid-search';

await createFullTextIndex();
```

Or use the Cypher query directly:
```cypher
CREATE FULLTEXT INDEX documentSearch IF NOT EXISTS
FOR (n:Document|Entity|Requirement)
ON EACH [n.title, n.content, n.name, n.description]
```

### 4. Populate Qdrant

Ensure documents are indexed in Qdrant with embeddings. The collection should have:
- **Collection name**: `documents`
- **Vector dimension**: 1536 (for text-embedding-3-small)
- **Payload fields**: title, content, customer, tags, date, type

## Usage

### From UI

1. Navigate to `/search`
2. Enter search query
3. Select mode (hybrid recommended)
4. Apply filters if needed
5. Click search button

### From API

```typescript
// Fetch API
const response = await fetch('/api/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'system architecture',
    mode: 'hybrid',
    limit: 10
  })
});

const data = await response.json();
console.log(data.results);
```

### From Code

```typescript
import { hybridSearch } from '@/lib/hybrid-search';

const results = await hybridSearch({
  query: 'user authentication requirements',
  mode: 'hybrid',
  filters: {
    customer: 'ACME Corp',
    tags: ['security', 'authentication']
  },
  limit: 20
});
```

## Testing

Run the test suite:

```bash
npx ts-node scripts/test-hybrid-search.ts
```

Tests include:
- ✅ Health check for all services
- ✅ Full-text search functionality
- ✅ Semantic search functionality
- ✅ Hybrid search with RRF
- ✅ Filtering capabilities

## Performance

### Typical Response Times

- **Full-text search**: 50-200ms
- **Semantic search**: 200-500ms (includes embedding generation)
- **Hybrid search**: 300-700ms (parallel execution)

### Optimization Tips

1. **Use appropriate mode**:
   - Full-text: Fast, exact matches
   - Semantic: Better for natural language
   - Hybrid: Best quality, slightly slower

2. **Limit result count**:
   - Start with limit=10
   - Increase for comprehensive results

3. **Apply filters early**:
   - Filters reduce search space
   - Faster execution

4. **Cache embeddings**:
   - Reuse embeddings for common queries
   - Reduce OpenAI API calls

## Troubleshooting

### "No results found"

1. Check if full-text index exists
2. Verify data exists in Neo4j
3. Ensure Qdrant collection is populated
4. Check filter constraints

### "Service unavailable"

1. Check service health: GET `/api/search/health`
2. Verify environment variables
3. Ensure services are running:
   - Neo4j: `bolt://localhost:7687`
   - Qdrant: `http://localhost:6333`

### "OpenAI API error"

1. Verify API key is valid
2. Check API quota/limits
3. Ensure internet connectivity

## Future Enhancements

- [ ] Query autocomplete suggestions
- [ ] Search history tracking
- [ ] Advanced filtering UI
- [ ] Export search results
- [ ] Saved searches
- [ ] Search analytics dashboard
- [ ] Multi-language support
- [ ] Custom RRF weights per source
- [ ] Result clustering
- [ ] Related document recommendations

## References

- [Neo4j Full-Text Search](https://neo4j.com/docs/cypher-manual/current/indexes-for-full-text-search/)
- [Qdrant Vector Database](https://qdrant.tech/documentation/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Reciprocal Rank Fusion Paper](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
