# AEON Frontend Developer Quick Start Guide

**File**: 00_FRONTEND_QUICK_START.md
**Created**: 2025-12-02 05:10:00 UTC
**Purpose**: Get frontend developers productive in 30 minutes
**Status**: ALL OPERATIONAL APIS DOCUMENTED

---

## 🚀 30-Minute Quick Start

### Step 1: Verify API Access (5 minutes)

```bash
# Test all operational endpoints
curl http://localhost:8000/health                    # NER11 API
curl http://localhost:6333/collections              # Qdrant
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 1"  # Neo4j
```

**Expected**: All return 200 OK

### Step 2: Install Dependencies (5 minutes)

```bash
npm install --save \
  neo4j-driver \
  axios \
  @types/node

# Or with yarn
yarn add neo4j-driver axios @types/node
```

### Step 3: Test Entity Extraction (5 minutes)

```typescript
// test-ner11.ts
import axios from 'axios';

const text = "APT29 deployed ransomware targeting Siemens PLCs in energy sector";

const response = await axios.post('http://localhost:8000/ner', { text });
console.log(`Extracted ${response.data.entities.length} entities:`);
response.data.entities.forEach((e: any) => {
  console.log(`  - ${e.text} (${e.label})`);
});
```

**Run**: `ts-node test-ner11.ts`

**Expected Output**:
```
Extracted 8 entities:
  - APT29 (THREAT_ACTOR)
  - ransomware (MALWARE)
  - Siemens (VENDOR)
  - PLCs (DEVICE)
  - energy (SECTORS)
  ...
```

### Step 4: Test Semantic Search (5 minutes)

```typescript
// test-search.ts
import axios from 'axios';

const query = {
  query: "ransomware attacks",
  limit: 5,
  fine_grained_filter: "RANSOMWARE"  // Only ransomware, not all malware
};

const response = await axios.post('http://localhost:8000/search/semantic', query);
console.log(`Found ${response.data.results.length} ransomware entities:`);
response.data.results.forEach((r: any) => {
  console.log(`  - ${r.entity} (score: ${r.score.toFixed(3)})`);
});
```

### Step 5: Test Neo4j Query (5 minutes)

```typescript
// test-neo4j.ts
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  'bolt://localhost:7687',
  neo4j.auth.basic('neo4j', 'neo4j@openspg')
);

const session = driver.session();
const result = await session.run(`
  MATCH (m:Malware)
  WHERE m.fine_grained_type = 'RANSOMWARE'
  RETURN m.name, m.hierarchy_path
  LIMIT 5
`);

console.log('Ransomware in Neo4j:');
result.records.forEach(record => {
  console.log(`  - ${record.get('m.name')}`);
});

await session.close();
await driver.close();
```

### Step 6: Build Your First Component (5 minutes)

```tsx
// ThreatSearch.tsx
import React, { useState } from 'react';
import axios from 'axios';

export const ThreatSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);

  const search = async () => {
    const response = await axios.post('http://localhost:8000/search/semantic', {
      query,
      limit: 10
    });
    setResults(response.data.results);
  };

  return (
    <div>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <button onClick={search}>Search</button>

      {results.map((r, i) => (
        <div key={i}>
          <strong>{r.entity}</strong> - {r.fine_grained_type}
          <span>Score: {(r.score * 100).toFixed(1)}%</span>
        </div>
      ))}
    </div>
  );
};
```

---

## 📚 Complete API Reference

### Operational APIs (Ready to Use Now)

| API | Endpoint | Doc File | Status |
|-----|----------|----------|--------|
| **NER11 Entity Extraction** | POST /ner | 08_NER11_SEMANTIC_SEARCH_API.md | ✅ OPERATIONAL |
| **NER11 Semantic Search** | POST /search/semantic | 09_NER11_FRONTEND_INTEGRATION_GUIDE.md | ✅ OPERATIONAL |
| **NER11 Hybrid Search** | POST /search/hybrid | 09_NER11_FRONTEND_INTEGRATION_GUIDE.md | ✅ OPERATIONAL |
| **Neo4j Cypher Queries** | bolt://localhost:7687 | 10_NEO4J_FRONTEND_QUERY_PATTERNS.md | ✅ OPERATIONAL |
| **Qdrant Direct Access** | http://localhost:6333 | (Optional advanced use) | ✅ OPERATIONAL |

### Planned APIs (Specification Complete, Not Implemented)

| API | Doc File | Implementation Status |
|-----|----------|---------------------|
| GraphQL | API_GRAPHQL.md | 📋 PLANNED (12 weeks) |
| Equipment REST | API_EQUIPMENT.md | 📋 PLANNED (4-6 weeks) |
| Vulnerabilities REST | API_VULNERABILITIES.md | 📋 PLANNED (3-4 weeks) |
| Sectors REST | API_SECTORS.md | 📋 PLANNED (3-4 weeks) |
| Events REST | API_EVENTS.md | 📋 PLANNED (4-6 weeks) |
| Predictions REST | API_PREDICTIONS.md | 📋 PLANNED (6-8 weeks) |
| Psychohistory | E27_PSYCHOHISTORY_API.md | 📋 PLANNED (8-10 weeks) |

---

## 🎯 What You Can Build RIGHT NOW

### Option 1: Threat Intelligence Search App
**Tech Stack**: React + TypeScript + NER11 API + Neo4j
**Features**:
- Live entity extraction from text
- Semantic search over 3,889 threat entities
- Hierarchical filtering (566 types)
- Graph relationship visualization

**Time to Build**: 2-3 weeks

### Option 2: Attack Path Visualizer
**Tech Stack**: React + D3.js + Neo4j
**Features**:
- Query attack chains (actor → malware → target)
- Visualize multi-hop paths
- Filter by relationship types
- Interactive graph exploration

**Time to Build**: 3-4 weeks

### Option 3: Vulnerability Dashboard
**Tech Stack**: React + Material-UI + NER11 + Neo4j
**Features**:
- Search CVEs semantically
- View affected assets via graph
- Risk scoring by sector
- Mitigation recommendations

**Time to Build**: 2-3 weeks

### Option 4: Cognitive Bias Analysis Tool
**Tech Stack**: React + Chart.js + NER11 API
**Features**:
- Extract biases from security incident reports
- Classify by fine-grained type (25 bias types)
- Statistical analysis
- Decision-making improvement recommendations

**Time to Build**: 1-2 weeks

---

## 📖 Documentation Navigation

### For API Integration
1. **Start here**: `00_FRONTEND_QUICK_START.md` (this file)
2. **NER11 APIs**: `09_NER11_FRONTEND_INTEGRATION_GUIDE.md`
3. **Neo4j Patterns**: `10_NEO4J_FRONTEND_QUERY_PATTERNS.md`
4. **API Specs**: `08_NER11_SEMANTIC_SEARCH_API.md`

### For Understanding Data
1. **Data Status**: `00_API_STATUS_AND_ROADMAP.md`
2. **Schema**: `../03_SPECIFICATIONS/07_NER11_HIERARCHICAL_INTEGRATION_COMPLETE_SPECIFICATION.md`
3. **Infrastructure**: `../01_Infrastructure/E30_NER11_INFRASTRUCTURE.md`

### For Advanced Features
1. **GraphQL** (planned): `API_GRAPHQL.md`
2. **Psychohistory** (planned): `E27_PSYCHOHISTORY_API.md`
3. **Equipment**: `API_EQUIPMENT.md`

---

## 🔑 Key Concepts for Frontend Developers

### Three-Tier Hierarchy

**Tier 1**: 60 NER Labels (broad categories)
- Example: `MALWARE`, `THREAT_ACTOR`, `DEVICE`
- Use for: High-level filtering

**Tier 2**: 566 Fine-Grained Types (specific classifications)
- Example: `RANSOMWARE`, `NATION_STATE`, `PLC`
- Use for: Precise queries (most powerful feature!)

**Tier 3**: Specific Instances (actual entity names)
- Example: `WannaCry`, `APT29`, `Siemens_S7-1500`
- Use for: Exact entity lookup

**Path Format**: `{tier1}/{tier2}/{tier3}`
- Example: `MALWARE/RANSOMWARE/WannaCry`

### Search Modes

**Semantic Search**: Find similar entities by meaning
- Uses: Vector similarity (Qdrant)
- Speed: <150ms
- Returns: Ranked by similarity score
- Best for: Text-based discovery

**Hybrid Search**: Combine semantic + graph relationships
- Uses: Qdrant + Neo4j graph traversal
- Speed: <500ms
- Returns: Entities + related entities from graph
- Best for: Comprehensive threat intelligence

---

## 💡 Pro Tips

### Tip 1: Use Fine-Grained Filters
```typescript
// ❌ Don't do this (too broad)
await semanticSearch('attacks', { label_filter: 'MALWARE' });
// Returns: All malware (ransomware, trojans, worms, etc.)

// ✅ Do this (precise)
await semanticSearch('attacks', { fine_grained_filter: 'RANSOMWARE' });
// Returns: Only ransomware
```

### Tip 2: Leverage Graph Expansion
```typescript
// ❌ Don't do this (missing context)
await semanticSearch('APT29');
// Returns: Just APT29 entities

// ✅ Do this (full context)
await hybridSearch('APT29', {
  expand_graph: true,
  hop_depth: 2,
  relationship_types: ['USES', 'TARGETS']
});
// Returns: APT29 + malware they use + targets they attack
```

### Tip 3: Optimize Queries
```typescript
// ❌ Don't fetch everything
await runQuery('MATCH (n) RETURN n');  // Returns 1.1M nodes!

// ✅ Always use LIMIT
await runQuery('MATCH (n) RETURN n LIMIT 20');

// ✅ Use indexes
await runQuery(`
  MATCH (m:Malware)
  WHERE m.fine_grained_type = 'RANSOMWARE'  // Uses index
  RETURN m
  LIMIT 20
`);
```

### Tip 4: Handle Async Properly
```typescript
// ❌ Don't block rendering
function MyComponent() {
  const results = semanticSearch('query');  // Wrong!
  return <div>{results.length}</div>;
}

// ✅ Use useEffect + useState
function MyComponent() {
  const [results, setResults] = useState([]);

  useEffect(() => {
    semanticSearch('query').then(setResults);
  }, []);

  return <div>{results.length} results</div>;
}
```

---

## 🎓 Learning Path

### Week 1: Basic Integration
1. Day 1-2: Setup + test all endpoints
2. Day 3-4: Build entity extraction UI
3. Day 5: Build semantic search component

### Week 2: Advanced Features
1. Day 1-2: Neo4j integration
2. Day 3-4: Hybrid search with graph viz
3. Day 5: Hierarchical filtering UI

### Week 3: Polish & Deploy
1. Day 1-2: Error handling + loading states
2. Day 3-4: Performance optimization
3. Day 5: Testing + documentation

---

## 📞 Support & Resources

**API Documentation**: `/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/`
**Swagger UI**: http://localhost:8000/docs
**Neo4j Browser**: http://localhost:7474

**Common Issues**:
1. CORS errors → Add proxy in dev server
2. Timeout → Increase axios timeout
3. Empty results → Check data loaded in Qdrant/Neo4j

---

**Ready to Build**: ✅ All APIs documented and operational
**Dataset**: 3,889 real threat intelligence entities
**Performance**: <500ms for complex queries

**START HERE** → Then read the detailed integration guides!

**Last Updated**: 2025-12-02 05:10:00 UTC
