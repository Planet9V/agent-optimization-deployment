# Hybrid Search - Quick Start Guide

## ⚡ Quick Setup (3 steps)

### 1. Environment Variables
```bash
# Create .env.local with:
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j@openspg
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=<your-key>
OPENAI_API_KEY=<your-key>
```

### 2. Create Index
```bash
# In Neo4j browser or cypher-shell:
CREATE FULLTEXT INDEX documentSearch IF NOT EXISTS
FOR (n:Document|Entity|Requirement)
ON EACH [n.title, n.content, n.name, n.description]
```

### 3. Start App
```bash
npm run dev
# Navigate to http://localhost:3000/search
```

## 📁 Files Created

| File | Purpose |
|------|---------|
| `lib/hybrid-search.ts` | Core search engine (RRF, Neo4j, Qdrant) |
| `app/api/search/route.ts` | REST API endpoints |
| `app/search/page.tsx` | Search UI with filters |
| `components/search/SearchResults.tsx` | Result display components |
| `scripts/test-hybrid-search.ts` | Test suite |
| `docs/HYBRID_SEARCH.md` | Full documentation |

## 🔍 Usage Examples

### From UI
1. Go to `/search`
2. Enter query: "system requirements"
3. Select mode: Hybrid (recommended)
4. Add filters (optional)
5. Click Search

### From API
```javascript
// POST /api/search
fetch('/api/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'authentication requirements',
    mode: 'hybrid',
    customer: 'ACME Corp',
    tags: ['security'],
    limit: 10
  })
})
```

### From Code
```typescript
import { hybridSearch } from '@/lib/hybrid-search';

const results = await hybridSearch({
  query: 'system architecture',
  mode: 'hybrid', // or 'fulltext' or 'semantic'
  filters: {
    customer: 'ACME Corp',
    tags: ['requirements', 'design']
  },
  limit: 20
});
```

## 🎯 Search Modes

| Mode | Use When | Speed | Quality |
|------|----------|-------|---------|
| **fulltext** | Exact keyword matching | ⚡ Fast (50-200ms) | Good |
| **semantic** | Natural language queries | 🐢 Slower (200-500ms) | Better |
| **hybrid** | Best overall results | ⚡🐢 Medium (300-700ms) | **Best** |

## 🧪 Testing

```bash
npx ts-node scripts/test-hybrid-search.ts
```

Expected: All checks ✅

## 📊 Architecture

```
User Query
    ↓
API Route (/api/search)
    ↓
Hybrid Search Engine
    ↓
┌───────────┬──────────────┐
│  Neo4j    │   Qdrant     │
│ Full-Text │  Semantic    │
└─────┬─────┴──────┬───────┘
      │            │
      └────→ RRF ←─┘
            ↓
        Merged Results
```

## ✅ Verification Checklist

- [ ] Environment variables set
- [ ] Neo4j running (port 7687)
- [ ] Qdrant running (port 6333)
- [ ] Full-text index created
- [ ] Documents in Neo4j
- [ ] Vectors in Qdrant
- [ ] OpenAI API key valid
- [ ] Test suite passes
- [ ] UI accessible at /search

## 🚨 Troubleshooting

**No results?**
- Check Neo4j has documents
- Verify Qdrant collection populated
- Ensure index exists

**Service errors?**
- Run health check: GET `/api/search/health`
- Verify services running
- Check API keys

**Slow searches?**
- Use `fulltext` mode for speed
- Reduce limit (10-20 results)
- Add filters to narrow scope

## 📚 Documentation

- **Full Guide**: `/docs/HYBRID_SEARCH.md`
- **Implementation**: `/docs/IMPLEMENTATION_COMPLETE.md`
- **API Reference**: See route.ts for endpoint details

---

**Ready to Search!** 🚀
