# AI Chat Assistant Documentation

## Overview

The AI Chat Assistant provides intelligent, context-aware responses by orchestrating queries across multiple data sources:
- **Neo4j Graph Database**: Structured project data, relationships, documents
- **Qdrant Vector Database**: Semantic document search
- **Internet Search**: Real-time web information (via Tavily API)

## Features

### 1. Multi-Source Integration
- Toggle data sources on/off per query
- Parallel query execution across all enabled sources
- Intelligent result ranking and deduplication
- Source attribution for transparency

### 2. Streaming Responses
- Real-time response streaming using Vercel AI SDK
- Server-Sent Events (SSE) for smooth user experience
- Source metadata sent before response text
- Progressive content display

### 3. Context Management
- Customer selection for scoped queries
- Project scope filtering (Mechanical, Electrical, etc.)
- Project ID filtering for specific project queries
- Context persists across conversation

### 4. Smart Query Orchestration
- Intent analysis for optimal query routing
- Automatic Cypher query generation for Neo4j
- Semantic embedding generation for Qdrant
- Tavily API integration for internet search
- Result synthesis with OpenAI GPT-4

### 5. Interactive Features
- Suggested actions based on context
- Recent query history (localStorage)
- Quick commands (@customer, @project, @doc)
- Copy, regenerate, export capabilities
- Source citation and expansion

## Architecture

```
User Query
    ↓
/api/chat (route.ts)
    ↓
AIOrchestrator (ai-orchestrator.ts)
    ↓
    ├─→ Neo4j Query (parallel)
    ├─→ Qdrant Search (parallel)
    └─→ Internet Search (parallel)
    ↓
Result Ranking & Deduplication
    ↓
OpenAI Synthesis (streaming)
    ↓
User Interface (page.tsx)
```

## File Structure

```
/app/chat/page.tsx              # Main chat interface
/app/api/chat/route.ts          # API endpoint for chat
/lib/ai-orchestrator.ts         # Multi-source orchestration
/components/chat/
  ├─ ChatMessage.tsx            # Message display component
  └─ SuggestedActions.tsx       # Quick actions sidebar
```

## Setup

### 1. Install Dependencies
```bash
npm install ai @ai-sdk/openai zod
```

### 2. Environment Variables
Create `.env.local`:
```bash
# Required
OPENAI_API_KEY=sk-...

# Optional (for internet search)
TAVILY_API_KEY=tvly-...

# Database connections
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
QDRANT_URL=http://localhost:6333
```

### 3. Start Services
```bash
# Neo4j (Docker)
docker run -p 7687:7687 -p 7474:7474 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest

# Qdrant (Docker)
docker run -p 6333:6333 qdrant/qdrant

# Dev Server
npm run dev
```

### 4. Access Chat
Navigate to: `http://localhost:3000/chat`

## Usage Examples

### Basic Query
```
User: "Show me all projects for McKenney"
```

### Filtered Query
```
Context: Customer = "McKenney", Scope = "Mechanical"
User: "What are the recent mechanical project updates?"
```

### Multi-Source Query
```
Data Sources: Neo4j ✓, Qdrant ✓, Internet ✓
User: "What are the best practices for HVAC system design?"
```

### Quick Commands
```
User: "@customer McKenney show all active projects"
User: "@project 12345 summarize documents"
User: "@doc latest specifications"
```

## API Reference

### POST /api/chat

**Request Body:**
```typescript
{
  messages: Array<{
    role: 'user' | 'assistant';
    content: string;
  }>;
  dataSources: {
    neo4j: boolean;
    qdrant: boolean;
    internet: boolean;
  };
  context: {
    customer?: string;
    scope?: string;
    projectId?: string;
  };
}
```

**Response (SSE):**
```typescript
// Sources metadata
data: {"type":"sources","sources":[...]}

// Streaming text chunks
data: {"type":"text","content":"..."}

// Completion signal
data: [DONE]
```

## AIOrchestrator Methods

### `orchestrateQuery(query, context, dataSources)`
Coordinates parallel queries across enabled data sources.

**Parameters:**
- `query` (string): User's question
- `context` (QueryContext): Customer, scope, project filters
- `dataSources` (DataSource): Enabled sources

**Returns:** `Promise<SourceResult[]>`

### `synthesizeResponse(query, sourceResults, context)`
Generates AI response using OpenAI with source context.

**Parameters:**
- `query` (string): Original question
- `sourceResults` (SourceResult[]): Aggregated sources
- `context` (QueryContext): Query context

**Returns:** `Promise<string>`

## Neo4j Query Patterns

The orchestrator generates different Cypher queries based on intent:

### Customer-Focused
```cypher
MATCH (c:Customer {name: $customerName})
OPTIONAL MATCH (c)-[:HAS_PROJECT]->(p:Project)
OPTIONAL MATCH (p)-[:HAS_DOCUMENT]->(d:Document)
OPTIONAL MATCH (d)-[:HAS_CHUNK]->(ch:Chunk)
WHERE ch.text CONTAINS $searchTerm
RETURN c, p, d, ch
LIMIT 20
```

### Project-Focused
```cypher
MATCH (p:Project)
WHERE p.projectId = $projectId OR p.name CONTAINS $searchTerm
OPTIONAL MATCH (p)-[:HAS_DOCUMENT]->(d:Document)
OPTIONAL MATCH (d)-[:HAS_CHUNK]->(ch:Chunk)
WHERE ch.text CONTAINS $searchTerm
RETURN p, d, ch
LIMIT 20
```

### General Search
```cypher
MATCH (ch:Chunk)
WHERE ch.text CONTAINS $searchTerm
MATCH (ch)<-[:HAS_CHUNK]-(d:Document)<-[:HAS_DOCUMENT]-(p:Project)
RETURN ch, d, p
LIMIT 20
```

## Qdrant Integration

### Embedding Generation
Uses OpenAI `text-embedding-3-small` model for semantic search.

### Vector Search
```javascript
POST http://localhost:6333/collections/documents/points/search
{
  "vector": [embedding_values],
  "limit": 10,
  "with_payload": true,
  "filter": {
    "must": [{"key": "customer", "match": {"value": "McKenney"}}]
  }
}
```

## Internet Search (Tavily)

### API Call
```javascript
POST https://api.tavily.com/search
{
  "query": "user query",
  "search_depth": "basic",
  "max_results": 5
}
```

### Fallback Behavior
If Tavily API key is not configured, returns informative message instead of failing.

## Components

### ChatMessage Component
**Props:**
- `message` (Message): Message data
- `onAction` (Function): Action handler

**Features:**
- Role-based styling (user vs assistant)
- Source expansion/collapse
- Copy to clipboard
- Regenerate response
- Export conversation

### SuggestedActions Component
**Props:**
- `onActionClick` (Function): Action handler
- `recentQueries` (string[]): Query history
- `context` (QueryContext): Current context

**Features:**
- Context-aware suggestions
- Recent query replay
- Quick commands reference
- Context display

## Error Handling

### Neo4j Errors
- Logs error, returns empty results
- Continues with other sources

### Qdrant Errors
- Falls back to Neo4j + Internet
- Graceful degradation

### Internet Search Errors
- Returns informative message
- Doesn't block other sources

### OpenAI Errors
- Returns user-friendly error message
- Removes incomplete assistant message

## Performance Optimizations

### Parallel Execution
All enabled data sources query simultaneously using `Promise.all()`.

### Result Ranking
Sources ranked by relevance score, deduplicated, limited to top 15.

### Streaming
Response streams immediately as generated, no waiting for completion.

### Caching (Future)
- Cache embeddings for repeated queries
- Cache Neo4j results for common patterns
- Cache internet search results (TTL)

## Security Considerations

1. **API Key Protection**: Environment variables, never in client
2. **Input Validation**: Sanitize user queries before database operations
3. **Rate Limiting**: Implement rate limits on /api/chat endpoint
4. **Context Filtering**: Respect data access permissions
5. **SQL Injection Prevention**: Parameterized Cypher queries only

## Testing

### Manual Testing
1. Start all services (Neo4j, Qdrant, dev server)
2. Navigate to /chat
3. Test each data source independently
4. Test multi-source queries
5. Test context filtering
6. Test error scenarios (disable services)

### Unit Tests (Future)
```bash
npm test lib/ai-orchestrator.test.ts
npm test app/api/chat/route.test.ts
```

## Troubleshooting

### "No sources enabled"
Enable at least one data source (Neo4j, Qdrant, or Internet).

### "OpenAI API error"
Check `OPENAI_API_KEY` in `.env.local`.

### "Neo4j connection failed"
Verify Neo4j is running and credentials are correct.

### "Qdrant not responding"
Check Qdrant service status and URL configuration.

### "Streaming not working"
Ensure client properly handles Server-Sent Events (SSE).

## Future Enhancements

1. **Multi-Turn Context**: Maintain conversation memory across turns
2. **Function Calling**: Enable AI to trigger actions (create tags, generate reports)
3. **Advanced Filters**: Date ranges, document types, metadata filters
4. **Voice Input**: Speech-to-text for queries
5. **Collaborative Chat**: Multi-user chat sessions
6. **Export Formats**: PDF, Word, Markdown exports
7. **Analytics Dashboard**: Query patterns, source usage, response quality
8. **Custom Models**: Fine-tuned models for domain-specific queries

## Support

For issues or questions:
1. Check this documentation
2. Review console logs for errors
3. Verify environment configuration
4. Test each component independently
5. Contact development team

## Version History

- **v1.0.0** (2025-01-03): Initial release
  - Multi-source orchestration
  - Streaming responses
  - Context management
  - Suggested actions
