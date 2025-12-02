# AEON Cyber Digital Twin - Frontend Development Primer

**Created**: 2025-12-02 05:15:00 UTC
**Version**: 1.0.0
**Purpose**: Complete frontend development guide with all operational APIs, documentation references, and implementation patterns
**Status**: READY FOR DEVELOPMENT - All APIs operational and tested

---

## 🚀 EXECUTIVE SUMMARY

This primer provides **everything a frontend developer needs** to build the AEON Cyber Digital Twin user interface. All operational APIs are documented with complete examples, TypeScript types, React components, and direct links to specifications.

**What's Operational RIGHT NOW**:
- ✅ **NER11 Search APIs** - 3 endpoints (entity extraction, semantic search, hybrid search)
- ✅ **Neo4j Knowledge Graph** - 1.1M+ nodes, direct Cypher query access
- ✅ **Qdrant Vector Database** - 3,889 entities with semantic embeddings
- ✅ **Real Production Data** - 18 threat intelligence reports from 2025

**What You Can Build Immediately**:
1. Threat Intelligence Search Application
2. Attack Path Visualization Dashboard
3. Vulnerability Impact Analysis Tool
4. Cognitive Bias Analysis Interface
5. Entity Extraction & Classification UI

---

## 📋 TABLE OF CONTENTS

1. [Quick Start (30 Minutes)](#quick-start-30-minutes)
2. [Operational APIs Reference](#operational-apis-reference)
3. [Data Model & Schema](#data-model--schema)
4. [Complete Code Examples](#complete-code-examples)
5. [Component Architecture](#component-architecture)
6. [Setup & Installation](#setup--installation)
7. [Documentation Index](#documentation-index)
8. [Development Roadmap](#development-roadmap)

---

## Quick Start (30 Minutes)

### Step 1: Verify API Access (5 min)

```bash
# Test NER11 API
curl http://localhost:8000/health
# Expected: {"status":"healthy","ner_model":"loaded"}

# Test Qdrant
curl http://localhost:6333/collections/ner11_entities_hierarchical
# Expected: {"result":{"points_count":3889,...}}

# Test Neo4j
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 1"
# Expected: 1
```

### Step 2: Install Dependencies (5 min)

```bash
npm install --save \
  neo4j-driver \
  axios \
  @types/node \
  react \
  @types/react

# Or create new React app
npx create-react-app aeon-threat-intel --template typescript
cd aeon-threat-intel
npm install neo4j-driver axios
```

### Step 3: Test First API Call (5 min)

Create `test-api.ts`:
```typescript
import axios from 'axios';

async function testNER11() {
  // Test entity extraction
  const response = await axios.post('http://localhost:8000/ner', {
    text: 'APT29 deployed ransomware targeting Siemens PLCs in energy sector'
  });

  console.log(`✅ Extracted ${response.data.entities.length} entities:`);
  response.data.entities.forEach((e: any) => {
    console.log(`  - ${e.text} (${e.label}, confidence: ${e.score})`);
  });
}

testNER11();
```

Run: `ts-node test-api.ts`

### Step 4: Build Your First Component (10 min)

See [Complete Code Examples](#complete-code-examples) section below for ready-to-use React components.

### Step 5: Read Documentation (5 min)

**Essential Reading**:
1. `00_FRONTEND_QUICK_START.md` - This guide expanded
2. `09_NER11_FRONTEND_INTEGRATION_GUIDE.md` - Complete TypeScript/React examples
3. `10_NEO4J_FRONTEND_QUERY_PATTERNS.md` - Cypher query library

---

## Operational APIs Reference

### API 1: NER11 Entity Extraction ✅

**Endpoint**: `POST http://localhost:8000/ner`
**Purpose**: Extract named entities from text (60 production labels)
**Performance**: <200ms for 1000-word documents
**Status**: OPERATIONAL

**Documentation**:
- Full spec: `../1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/08_NER11_SEMANTIC_SEARCH_API.md`
- Integration guide: `../1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/09_NER11_FRONTEND_INTEGRATION_GUIDE.md`

**Request**:
```typescript
interface NERRequest {
  text: string;  // Max 100,000 characters
}
```

**Response**:
```typescript
interface NERResponse {
  entities: Array<{
    text: string;      // Extracted entity text
    label: string;     // One of 60 NER labels
    start: number;     // Character position
    end: number;       // Character position
    score: number;     // Confidence 0.0-1.0
  }>;
  doc_length: number;
}
```

**60 NER Labels Available**:
```typescript
type NERLabel =
  | 'MALWARE' | 'THREAT_ACTOR' | 'ATTACK_TECHNIQUE' | 'CVE' | 'VULNERABILITY'
  | 'DEVICE' | 'PROTOCOL' | 'SOFTWARE_COMPONENT' | 'ORGANIZATION' | 'LOCATION'
  | 'SECTOR' | 'COGNITIVE_BIAS' | 'CONTROLS' | 'MITIGATION' | 'INDICATOR'
  | 'CAMPAIGN' | 'APT_GROUP' | 'TOOL' | 'FACILITY' | 'NETWORK'
  // ... and 40 more (see full list in API docs)
```

**Example Usage**:
```typescript
const response = await axios.post('http://localhost:8000/ner', {
  text: 'CrowdStrike detected APT29 using WannaCry ransomware'
});

// Returns:
// entities: [
//   {text: "CrowdStrike", label: "ORGANIZATION", score: 1.0},
//   {text: "APT29", label: "THREAT_ACTOR", score: 1.0},
//   {text: "WannaCry", label: "MALWARE", score: 1.0},
//   {text: "ransomware", label: "MALWARE", score: 1.0}
// ]
```

---

### API 2: NER11 Semantic Search ✅

**Endpoint**: `POST http://localhost:8000/search/semantic`
**Purpose**: Semantic vector similarity search with hierarchical filtering
**Performance**: <150ms average
**Current Dataset**: **3,889 entities** from threat intelligence reports
**Status**: OPERATIONAL

**Documentation**:
- Full spec: `../1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/08_NER11_SEMANTIC_SEARCH_API.md`
- Integration guide: `../1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/09_NER11_FRONTEND_INTEGRATION_GUIDE.md` (lines 200-500)

**Request**:
```typescript
interface SemanticSearchRequest {
  query: string;                    // Search query text (required)
  limit?: number;                   // Max results (1-100, default 10)
  label_filter?: string;            // Tier 1: NER label filter
  fine_grained_filter?: string;     // Tier 2: 566 types filter (MOST POWERFUL)
  confidence_threshold?: number;    // Min NER confidence (0.0-1.0)
}
```

**Response**:
```typescript
interface SemanticSearchResponse {
  results: Array<{
    score: number;              // Similarity score 0.0-1.0
    entity: string;             // Entity text
    ner_label: string;          // Tier 1 (60 labels)
    fine_grained_type: string;  // Tier 2 (566 types)
    hierarchy_path: string;     // Full path (e.g., "MALWARE/RANSOMWARE/WannaCry")
    confidence: number;         // NER extraction confidence
    doc_id: string;             // Source document
  }>;
  total_found: number;
  query: string;
}
```

**Three-Tier Hierarchical Filtering** (KEY FEATURE):

**Tier 1** - Broad Category (60 NER labels):
```typescript
// Search only in MALWARE category
const results = await searchSemantic('cyber attacks', {
  label_filter: 'MALWARE'  // Returns: ransomware, trojans, worms, etc.
});
```

**Tier 2** - Specific Type (566 fine-grained types) - **MOST POWERFUL**:
```typescript
// Search only for RANSOMWARE (not all malware)
const results = await searchSemantic('encryption attacks', {
  fine_grained_filter: 'RANSOMWARE'  // Returns: ONLY ransomware
});
```

**Tier 3** - Exact Instance (specific entity names):
```typescript
// Implicit in query text
const results = await searchSemantic('WannaCry');
// Returns: WannaCry-specific entities
```

**Common Fine-Grained Filters**:
```typescript
// Malware types
'RANSOMWARE' | 'TROJAN' | 'WORM' | 'ROOTKIT' | 'RAT' | 'BACKDOOR'

// Threat actor types
'NATION_STATE' | 'APT_GROUP' | 'HACKTIVIST' | 'CRIME_SYNDICATE'

// Device types
'PLC' | 'RTU' | 'HMI' | 'DCS' | 'SCADA_SERVER' | 'IED'

// Cognitive biases
'CONFIRMATION_BIAS' | 'NORMALCY_BIAS' | 'AVAILABILITY_HEURISTIC'

// Protocols
'MODBUS' | 'DNP3' | 'IEC_61850' | 'PROFINET' | 'BACNET'
```

**Example Usage**:
```typescript
// Search for ransomware attacks
const ransomware = await axios.post('http://localhost:8000/search/semantic', {
  query: 'encryption malware critical infrastructure',
  fine_grained_filter: 'RANSOMWARE',
  limit: 10
});

// Returns: Only RANSOMWARE entities with semantic similarity
ransomware.data.results.forEach(r => {
  console.log(`${r.entity} - Score: ${r.score.toFixed(3)}`);
  console.log(`  Path: ${r.hierarchy_path}`);
  console.log(`  From: ${r.doc_id}`);
});
```

---

### API 3: NER11 Hybrid Search ✅

**Endpoint**: `POST http://localhost:8000/search/hybrid`
**Purpose**: Combine semantic similarity (Qdrant) with knowledge graph expansion (Neo4j)
**Performance**: <500ms average
**Status**: OPERATIONAL

**Documentation**:
- Full spec: `../1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/08_NER11_SEMANTIC_SEARCH_API.md` (lines 212-390)
- Integration guide: `../1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/09_NER11_FRONTEND_INTEGRATION_GUIDE.md` (lines 500-800)

**Request**:
```typescript
interface HybridSearchRequest {
  query: string;                    // Search query (required)
  limit?: number;                   // Max semantic results (1-100, default 10)
  expand_graph?: boolean;           // Enable Neo4j graph expansion (default true)
  hop_depth?: number;               // Graph traversal depth 1-3 (default 2)
  label_filter?: string;            // Tier 1 filter
  fine_grained_filter?: string;     // Tier 2 filter
  confidence_threshold?: number;    // Min confidence
  relationship_types?: string[];    // Relationship type filter
}
```

**Response**:
```typescript
interface HybridSearchResponse {
  results: Array<{
    score: number;                  // Adjusted score (semantic + graph boost)
    entity: string;
    ner_label: string;
    fine_grained_type: string;
    hierarchy_path: string;
    confidence: number;
    doc_id: string;
    related_entities: Array<{       // ⭐ GRAPH EXPANSION RESULTS
      name: string;
      label: string;                // Neo4j label
      ner_label: string;
      fine_grained_type: string;
      hierarchy_path: string;
      hop_distance: number;         // 1-3 hops from source
      relationship: string;         // Relationship type
      relationship_direction: 'outgoing' | 'incoming';
    }>;
    graph_context: {
      node_exists: boolean;
      outgoing_relationships: number;
      incoming_relationships: number;
      labels: string[];
      properties: object;
    };
  }>;
  query: string;
  total_results: number;
  search_type: 'hybrid';
  qdrant_time_ms: number;           // Semantic search time
  neo4j_time_ms: number;            // Graph expansion time
  total_time_ms: number;            // Total response time
  filters_applied: object;
}
```

**Relationship Types**:
```typescript
type RelationshipType =
  // Attack relationships
  | 'EXPLOITS'        // Malware exploits vulnerabilities
  | 'USES'            // Threat actors use malware/tools
  | 'TARGETS'         // Attacks target assets
  | 'AFFECTS'         // Vulnerabilities affect software/devices
  | 'ATTRIBUTED_TO'   // Attacks attributed to threat actors

  // Defense relationships
  | 'MITIGATES'       // Controls mitigate vulnerabilities
  | 'PROTECTS'        // Controls protect assets
  | 'DETECTS'         // Indicators detect threats

  // Analysis relationships
  | 'INDICATES'       // Indicators signal threats
  | 'EXHIBITS'        // Users exhibit cognitive biases
  | 'CONTRIBUTES_TO'  // Biases contribute to incidents
;
```

**Re-Ranking Algorithm**:
- Base score: Semantic similarity from Qdrant (0.0-1.0)
- Graph boost: +10% per related entity (max 30% boost)
- Final score: min(1.0, base_score + graph_boost)

**Example Usage**:
```typescript
// Search with graph expansion
const results = await axios.post('http://localhost:8000/search/hybrid', {
  query: 'APT29 malware campaigns',
  expand_graph: true,
  hop_depth: 2,
  fine_grained_filter: 'NATION_STATE',
  relationship_types: ['USES', 'TARGETS', 'ATTRIBUTED_TO']
});

// Returns: APT29 entities + malware they use + targets they attack
results.data.results.forEach(r => {
  console.log(`${r.entity} (${r.fine_grained_type}) - Score: ${r.score}`);

  if (r.related_entities.length > 0) {
    console.log('  Related:');
    r.related_entities.forEach(rel => {
      console.log(`    ${rel.relationship} → ${rel.name} (${rel.fine_grained_type})`);
    });
  }
});
```

---

### API 4: Neo4j Direct Access ✅

**Endpoint**: `bolt://localhost:7687`
**Auth**: `neo4j` / `neo4j@openspg`
**Purpose**: Direct Cypher query access to 1.1M+ node knowledge graph
**Performance**: <500ms for 2-hop queries
**Status**: OPERATIONAL

**Documentation**:
- Query patterns: `../1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/10_NEO4J_FRONTEND_QUERY_PATTERNS.md`
- Schema spec: `../1_AEON_DT_CyberSecurity_Wiki_Current/03_SPECIFICATIONS/03_NEO4J_COMPLETE_SCHEMA_v3.0_2025-11-19.md`

**Installation**:
```bash
npm install neo4j-driver
```

**Connection**:
```typescript
import neo4j from 'neo4j-driver';

const driver = neo4j.driver(
  'bolt://localhost:7687',
  neo4j.auth.basic('neo4j', 'neo4j@openspg')
);

const session = driver.session();
```

**Example Query - Find Ransomware**:
```typescript
const result = await session.run(`
  MATCH (m:Malware)
  WHERE m.fine_grained_type = 'RANSOMWARE'
  RETURN m.name, m.hierarchy_path
  LIMIT 20
`);

const ransomware = result.records.map(r => ({
  name: r.get('m.name'),
  path: r.get('m.hierarchy_path')
}));
```

**Example Query - Attack Paths**:
```typescript
const result = await session.run(`
  MATCH path = (ta:ThreatActor)-[:USES]->(m:Malware)-[:TARGETS]->(a:Asset)
  WHERE ta.fine_grained_type = 'NATION_STATE'
    AND m.fine_grained_type = 'RANSOMWARE'
  RETURN ta.name AS actor,
         m.name AS malware,
         a.name AS target
  LIMIT 10
`);

const attackPaths = result.records.map(r => ({
  actor: r.get('actor'),
  malware: r.get('malware'),
  target: r.get('target')
}));
```

**Database Schema**:
- **Total Nodes**: 1,104,389
- **Relationships**: 3,300,000+
- **Labels**: 193 (including 16 Super Labels)
- **Hierarchical Entities**: 331 with NER properties

**16 Super Labels**:
```typescript
type SuperLabel =
  // Threat Intelligence
  | 'ThreatActor' | 'AttackPattern' | 'Vulnerability' | 'Malware'
  | 'Indicator' | 'Campaign' | 'Control'

  // Infrastructure
  | 'Asset' | 'Organization' | 'Location' | 'Protocol' | 'Software'

  // Psychometric
  | 'PsychTrait' | 'Role'

  // Economic & Events
  | 'EconomicMetric' | 'Event'
;
```

---

## Data Model & Schema

### Hierarchical Entity Model

Every entity extracted by NER11 has three tiers of classification:

```typescript
interface HierarchicalEntity {
  // Tier 1: NER Model Output (60 labels)
  ner_label: string;              // Example: "MALWARE"

  // Tier 2: Fine-Grained Type (566 types) ⭐ KEY FEATURE
  fine_grained_type: string;      // Example: "RANSOMWARE"

  // Tier 3: Specific Instance
  specific_instance: string;      // Example: "WannaCry"

  // Hierarchy
  hierarchy_path: string;         // Example: "MALWARE/RANSOMWARE/WannaCry"
  hierarchy_level: number;        // 1, 2, or 3

  // Metadata
  confidence: number;             // NER extraction confidence
  classification_confidence: number;  // Hierarchy classification confidence
  doc_id: string;                 // Source document
  created_at: string;             // ISO timestamp
}
```

**Path Examples**:
```
MALWARE/RANSOMWARE/WannaCry
THREAT_ACTOR/NATION_STATE/APT29
DEVICE/PLC/Siemens_S7-1500
COGNITIVE_BIAS/CONFIRMATION_BIAS/exhibited_in_incident_123
PROTOCOL/MODBUS/Modbus_TCP
SOFTWARE_COMPONENT/LIBRARY/Log4j
```

### Qdrant Data Model

**Collection**: `ner11_entities_hierarchical`
**Vector Size**: 384 dimensions
**Distance Metric**: Cosine similarity
**Total Points**: 3,889

**Payload Schema**:
```typescript
interface QdrantPayload {
  entity: string;
  ner_label: string;
  fine_grained_type: string;
  specific_instance: string;
  hierarchy_path: string;
  hierarchy_level: number;
  confidence: number;
  classification_confidence: number;
  doc_id: string;
  created_at: string;
}
```

**8 Payload Indexes** (for fast filtering):
- `ner_label` (keyword)
- `fine_grained_type` (keyword) ⭐ Most important
- `specific_instance` (keyword)
- `hierarchy_path` (keyword)
- `hierarchy_level` (integer)
- `confidence` (float)
- `doc_id` (keyword)
- `batch_id` (keyword)

### Neo4j Data Model

**Node Properties** (for NER entities):
```typescript
interface Neo4jHierarchicalNode {
  id: string;                      // UUID
  name: string;                    // Entity name
  ner_label: string;              // Tier 1
  fine_grained_type: string;      // Tier 2
  specific_instance: string;      // Tier 3
  hierarchy_path: string;
  hierarchy_level: number;
  confidence: number;
  created_at: string;             // DateTime
  updated_at?: string;            // DateTime

  // Label-specific properties
  // (varies by Neo4j label: Malware, ThreatActor, Asset, etc.)
}
```

**Example Malware Node**:
```cypher
(:Malware {
  id: "uuid-1234",
  name: "WannaCry",
  ner_label: "MALWARE",
  fine_grained_type: "RANSOMWARE",
  specific_instance: "WannaCry",
  hierarchy_path: "MALWARE/RANSOMWARE/WannaCry",
  hierarchy_level: 3,
  malwareFamily: "ransomware",
  platform: "windows",
  confidence: 1.0,
  created_at: "2025-12-02T05:00:00Z"
})
```

---

## Complete Code Examples

### 1. Entity Extraction Component

```tsx
import React, { useState } from 'react';
import axios from 'axios';

interface Entity {
  text: string;
  label: string;
  score: number;
}

export const EntityExtractor: React.FC = () => {
  const [text, setText] = useState('');
  const [entities, setEntities] = useState<Entity[]>([]);
  const [loading, setLoading] = useState(false);

  const extractEntities = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/ner', { text });
      setEntities(response.data.entities);
    } catch (error) {
      console.error('Extraction failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="entity-extractor">
      <h2>NER11 Entity Extraction</h2>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste threat intelligence text here..."
        rows={10}
        style={{ width: '100%', padding: '10px' }}
      />

      <button
        onClick={extractEntities}
        disabled={loading || !text}
        style={{ marginTop: '10px', padding: '10px 20px' }}
      >
        {loading ? 'Extracting...' : 'Extract Entities'}
      </button>

      {entities.length > 0 && (
        <div className="results" style={{ marginTop: '20px' }}>
          <h3>Found {entities.length} Entities:</h3>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ textAlign: 'left', padding: '8px' }}>Entity</th>
                <th style={{ textAlign: 'left', padding: '8px' }}>Type</th>
                <th style={{ textAlign: 'left', padding: '8px' }}>Confidence</th>
              </tr>
            </thead>
            <tbody>
              {entities.map((entity, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid #ddd' }}>
                  <td style={{ padding: '8px' }}><strong>{entity.text}</strong></td>
                  <td style={{ padding: '8px' }}>
                    <span className={`label-${entity.label}`}>
                      {entity.label}
                    </span>
                  </td>
                  <td style={{ padding: '8px' }}>
                    {(entity.score * 100).toFixed(0)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
```

### 2. Semantic Search Component

```tsx
import React, { useState } from 'react';
import axios from 'axios';

interface SearchResult {
  entity: string;
  fine_grained_type: string;
  hierarchy_path: string;
  score: number;
  doc_id: string;
}

export const ThreatSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [filter, setFilter] = useState<string>('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  const search = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/search/semantic', {
        query,
        fine_grained_filter: filter || undefined,
        limit: 20
      });

      setResults(response.data.results);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="threat-search">
      <h2>Threat Intelligence Search</h2>

      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search threats, actors, vulnerabilities..."
          style={{ flex: 1, padding: '10px' }}
          onKeyPress={(e) => e.key === 'Enter' && search()}
        />

        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          style={{ padding: '10px' }}
        >
          <option value="">All Types</option>
          <option value="RANSOMWARE">Ransomware</option>
          <option value="NATION_STATE">Nation States</option>
          <option value="APT_GROUP">APT Groups</option>
          <option value="PLC">PLCs</option>
          <option value="CONFIRMATION_BIAS">Confirmation Bias</option>
          <option value="MODBUS">Modbus Protocol</option>
        </select>

        <button onClick={search} disabled={loading} style={{ padding: '10px 20px' }}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {results.length > 0 && (
        <div className="results">
          <p><strong>Found {results.length} results</strong></p>

          {results.map((result, idx) => (
            <div
              key={idx}
              style={{
                border: '1px solid #ddd',
                padding: '15px',
                marginBottom: '10px',
                borderRadius: '5px'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h4 style={{ margin: 0 }}>{result.entity}</h4>
                <span style={{
                  background: '#007bff',
                  color: 'white',
                  padding: '4px 8px',
                  borderRadius: '3px',
                  fontSize: '12px'
                }}>
                  {result.fine_grained_type}
                </span>
              </div>

              <div style={{ marginTop: '10px', fontSize: '14px', color: '#666' }}>
                <div><strong>Path:</strong> {result.hierarchy_path}</div>
                <div><strong>Similarity:</strong> {(result.score * 100).toFixed(1)}%</div>
                <div><strong>Source:</strong> {result.doc_id}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

### 3. Hybrid Search with Graph Visualization

```tsx
import React, { useState } from 'react';
import axios from 'axios';

interface HybridResult {
  entity: string;
  fine_grained_type: string;
  score: number;
  related_entities: Array<{
    name: string;
    fine_grained_type: string;
    relationship: string;
    relationship_direction: string;
  }>;
  graph_context: {
    outgoing_relationships: number;
    incoming_relationships: number;
  };
}

export const HybridSearchDashboard: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<HybridResult[]>([]);
  const [loading, setLoading] = useState(false);

  const hybridSearch = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/search/hybrid', {
        query,
        expand_graph: true,
        hop_depth: 2,
        relationship_types: ['USES', 'TARGETS', 'ATTRIBUTED_TO'],
        limit: 10
      });

      setResults(response.data.results);
    } catch (error) {
      console.error('Hybrid search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="hybrid-search">
      <h2>Hybrid Search - Semantic + Graph</h2>

      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search with graph expansion..."
          style={{ width: '70%', padding: '10px' }}
          onKeyPress={(e) => e.key === 'Enter' && hybridSearch()}
        />
        <button
          onClick={hybridSearch}
          disabled={loading}
          style={{ padding: '10px 20px', marginLeft: '10px' }}
        >
          {loading ? 'Searching...' : 'Hybrid Search'}
        </button>
      </div>

      {results.map((result, idx) => (
        <div
          key={idx}
          style={{
            border: '2px solid #28a745',
            padding: '15px',
            marginBottom: '15px',
            borderRadius: '8px'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <div>
              <h3 style={{ margin: 0 }}>{result.entity}</h3>
              <span style={{ color: '#666' }}>{result.fine_grained_type}</span>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div><strong>Score:</strong> {(result.score * 100).toFixed(1)}%</div>
              <div style={{ fontSize: '12px', color: '#666' }}>
                ↑{result.graph_context.outgoing_relationships} |
                ↓{result.graph_context.incoming_relationships}
              </div>
            </div>
          </div>

          {result.related_entities.length > 0 && (
            <div style={{ marginTop: '15px', paddingTop: '15px', borderTop: '1px solid #ddd' }}>
              <h4>Related Entities ({result.related_entities.length}):</h4>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '10px' }}>
                {result.related_entities.map((rel, i) => (
                  <div
                    key={i}
                    style={{
                      background: '#f8f9fa',
                      padding: '10px',
                      borderRadius: '5px'
                    }}
                  >
                    <div style={{ fontWeight: 'bold' }}>{rel.name}</div>
                    <div style={{ fontSize: '12px', color: '#666' }}>
                      {rel.fine_grained_type}
                    </div>
                    <div style={{ fontSize: '12px', marginTop: '5px' }}>
                      {rel.relationship_direction === 'outgoing' ? '→' : '←'} {rel.relationship}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};
```

### 4. Neo4j Service Class

```typescript
import neo4j, { Driver, Session } from 'neo4j-driver';

export class AEONNeo4jService {
  private driver: Driver;

  constructor() {
    this.driver = neo4j.driver(
      'bolt://localhost:7687',
      neo4j.auth.basic('neo4j', 'neo4j@openspg')
    );
  }

  async runQuery(cypher: string, params: Record<string, any> = {}): Promise<any[]> {
    const session = this.driver.session();
    try {
      const result = await session.run(cypher, params);
      return result.records.map(record => record.toObject());
    } finally {
      await session.close();
    }
  }

  // Get entities by fine-grained type
  async getByType(fineGrainedType: string, limit: number = 20) {
    return this.runQuery(`
      MATCH (n)
      WHERE n.fine_grained_type = $type
      RETURN n.name AS name,
             n.ner_label AS ner_label,
             n.fine_grained_type AS type,
             n.hierarchy_path AS path
      LIMIT $limit
    `, { type: fineGrainedType, limit });
  }

  // Get attack paths
  async getAttackPaths(actorType: string = 'NATION_STATE', maxHops: number = 3) {
    return this.runQuery(`
      MATCH path = (ta:ThreatActor)-[*1..$maxHops]->(target)
      WHERE ta.fine_grained_type = $actorType
        AND (target:Asset OR target:Organization)
      RETURN [node in nodes(path) | {
        name: node.name,
        type: node.fine_grained_type
      }] AS path,
      [rel in relationships(path) | type(rel)] AS relationships,
      length(path) AS hops
      LIMIT 10
    `, { actorType, maxHops });
  }

  // Get entity connections
  async getConnections(entityName: string, relationshipTypes?: string[]) {
    const relFilter = relationshipTypes ? 'AND type(r) IN $relTypes' : '';

    return this.runQuery(`
      MATCH (n {name: $name})-[r]-(connected)
      WHERE 1=1 ${relFilter}
      RETURN type(r) AS relationship,
             connected.name AS name,
             connected.fine_grained_type AS type,
             labels(connected)[0] AS label
      LIMIT 50
    `, {
      name: entityName,
      relTypes: relationshipTypes
    });
  }

  // Get statistics
  async getHierarchyStats() {
    return this.runQuery(`
      MATCH (n)
      WHERE n.ner_label IS NOT NULL
      RETURN count(n) AS total_hierarchical,
             count(DISTINCT n.ner_label) AS tier1_labels,
             count(DISTINCT n.fine_grained_type) AS tier2_types
    `);
  }

  async close() {
    await this.driver.close();
  }
}

// Usage
const neo4j = new AEONNeo4jService();

// Get all ransomware
const ransomware = await neo4j.getByType('RANSOMWARE', 20);

// Get attack paths from nation-states
const paths = await neo4j.getAttackPaths('NATION_STATE', 3);

// Get what APT29 is connected to
const connections = await neo4j.getConnections('APT29', ['USES', 'TARGETS']);

// Cleanup
await neo4j.close();
```

---

## Component Architecture

### Recommended App Structure

```
src/
├── components/
│   ├── EntityExtractor.tsx       // POST /ner
│   ├── SemanticSearch.tsx        // POST /search/semantic
│   ├── HybridSearch.tsx          // POST /search/hybrid
│   ├── ThreatCard.tsx            // Display threat entity
│   ├── GraphVisualization.tsx    // D3.js graph viz
│   └── AttackPathDiagram.tsx     // Attack chain viz
│
├── hooks/
│   ├── useNER11.ts               // Entity extraction hook
│   ├── useSemanticSearch.ts      // Semantic search hook
│   ├── useHybridSearch.ts        // Hybrid search hook
│   └── useNeo4j.ts               // Neo4j connection hook
│
├── services/
│   ├── ner11.service.ts          // NER11 API client
│   ├── neo4j.service.ts          // Neo4j client
│   └── qdrant.service.ts         // Qdrant client (optional)
│
├── types/
│   ├── ner11.types.ts            // NER11 API types
│   ├── search.types.ts           // Search API types
│   └── neo4j.types.ts            // Neo4j types
│
├── pages/
│   ├── Dashboard.tsx             // Main dashboard
│   ├── ThreatIntel.tsx           // Threat intelligence view
│   ├── AttackPaths.tsx           // Attack path explorer
│   ├── Vulnerabilities.tsx       // CVE analysis
│   └── BiasAnalysis.tsx          // Cognitive bias analysis
│
└── utils/
    ├── hierarchyUtils.ts         // Hierarchy path parsing
    └── cacheUtils.ts             // Result caching
```

### Routing Structure

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/threats" element={<ThreatIntel />} />
        <Route path="/attack-paths" element={<AttackPaths />} />
        <Route path="/vulnerabilities" element={<Vulnerabilities />} />
        <Route path="/biases" element={<BiasAnalysis />} />
        <Route path="/search" element={<HybridSearch />} />
      </Routes>
    </BrowserRouter>
  );
}
```

---

## Setup & Installation

### Prerequisites

**Required**:
- Node.js 18+ or 20+
- npm or yarn
- Docker (for backend services)

**Backend Services Running**:
```bash
docker ps | grep -E "ner11|qdrant|neo4j"
# Should show: ner11-gold-api, openspg-qdrant, openspg-neo4j all Up
```

### Create New React App

```bash
# Create TypeScript React app
npx create-react-app aeon-cybersecurity-ui --template typescript
cd aeon-cybersecurity-ui

# Install dependencies
npm install \
  neo4j-driver \
  axios \
  react-router-dom \
  @types/react-router-dom \
  d3 \
  @types/d3

# Optional: UI libraries
npm install \
  @mui/material \
  @emotion/react \
  @emotion/styled \
  recharts
```

### Project Configuration

**package.json**:
```json
{
  "name": "aeon-cybersecurity-ui",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "neo4j-driver": "^5.15.0",
    "d3": "^7.8.0",
    "@mui/material": "^5.15.0",
    "recharts": "^2.10.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@types/d3": "^7.4.0",
    "typescript": "^5.3.0"
  },
  "proxy": "http://localhost:8000"
}
```

**Note**: The `"proxy"` setting routes API calls through the development server (avoids CORS).

### Environment Variables

Create `.env`:
```bash
REACT_APP_NER11_API_URL=http://localhost:8000
REACT_APP_NEO4J_URI=bolt://localhost:7687
REACT_APP_NEO4J_USER=neo4j
REACT_APP_NEO4J_PASSWORD=neo4j@openspg
REACT_APP_QDRANT_URL=http://localhost:6333
```

**Usage**:
```typescript
const NER11_API = process.env.REACT_APP_NER11_API_URL || 'http://localhost:8000';
const NEO4J_URI = process.env.REACT_APP_NEO4J_URI || 'bolt://localhost:7687';
```

---

## Documentation Index

### Primary Documentation (In Wiki)

**Location**: `/home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/`

#### API Documentation (`04_APIs/`)

| File | Purpose | Lines | Essential Reading |
|------|---------|-------|-------------------|
| **00_FRONTEND_QUICK_START.md** | 30-minute quick start | 200 | ⭐ START HERE |
| **09_NER11_FRONTEND_INTEGRATION_GUIDE.md** | Complete TypeScript/React guide | 400 | ⭐ ESSENTIAL |
| **10_NEO4J_FRONTEND_QUERY_PATTERNS.md** | Cypher query library | 350 | ⭐ ESSENTIAL |
| **08_NER11_SEMANTIC_SEARCH_API.md** | API specification | 530 | Reference |
| **00_API_STATUS_AND_ROADMAP.md** | All APIs status | 760 | Reference |
| **API_GRAPHQL.md** | GraphQL (planned) | 1,937 | Future |

#### Specifications (`03_SPECIFICATIONS/`)

| File | Purpose | Essential For |
|------|---------|---------------|
| **07_NER11_HIERARCHICAL_INTEGRATION_COMPLETE_SPECIFICATION.md** | Complete system spec | Understanding architecture |
| **03_NEO4J_COMPLETE_SCHEMA_v3.0_2025-11-19.md** | Neo4j schema | Database queries |
| **README.md** | Specifications index | Navigation |

#### Infrastructure (`01_Infrastructure/`)

| File | Purpose | Essential For |
|------|---------|---------------|
| **E30_NER11_INFRASTRUCTURE.md** | Deployment & operations | DevOps, troubleshooting |
| **E30_OPERATIONAL_STATUS.md** | Current system state | Understanding what's running |
| **E27_INFRASTRUCTURE.md** | Neo4j infrastructure | Performance tuning |

#### Implementation Tracking (`08_Planned_Enhancements/E30_NER11_Gold_Hierarchical_Integration/`)

| File | Purpose |
|------|---------|
| **blotter.md** | Task tracking (71% complete) |
| **INGESTION_RESULTS_2025_THREAT_INTEL.md** | Data ingestion results |

### Documentation Quick Links

**For Getting Started**:
1. Read: `04_APIs/00_FRONTEND_QUICK_START.md`
2. Then: `04_APIs/09_NER11_FRONTEND_INTEGRATION_GUIDE.md`
3. Then: `04_APIs/10_NEO4J_FRONTEND_QUERY_PATTERNS.md`

**For API Reference**:
1. NER11 APIs: `04_APIs/08_NER11_SEMANTIC_SEARCH_API.md`
2. All APIs: `04_APIs/00_API_STATUS_AND_ROADMAP.md`

**For Understanding Data**:
1. Specification: `03_SPECIFICATIONS/07_NER11_HIERARCHICAL_INTEGRATION_COMPLETE_SPECIFICATION.md`
2. Schema: `03_SPECIFICATIONS/03_NEO4J_COMPLETE_SCHEMA_v3.0_2025-11-19.md`

---

## Development Roadmap

### Week 1: Foundation
**Goal**: Basic UI with entity extraction and search

**Tasks**:
- [ ] Setup React TypeScript project
- [ ] Implement NER11 API client
- [ ] Build EntityExtractor component
- [ ] Build SemanticSearch component
- [ ] Test with real data

**Deliverables**:
- Working entity extraction UI
- Working semantic search UI
- Basic styling

### Week 2: Advanced Search
**Goal**: Hybrid search with graph visualization

**Tasks**:
- [ ] Implement Neo4j connection
- [ ] Build HybridSearch component
- [ ] Add hierarchical filtering UI (dropdowns for 566 types)
- [ ] Basic graph visualization (D3.js or similar)

**Deliverables**:
- Working hybrid search with graph expansion
- Visual display of related entities
- Filter UI for fine-grained types

### Week 3: Dashboards
**Goal**: Threat intelligence dashboards

**Tasks**:
- [ ] Build main dashboard
- [ ] Ransomware threat dashboard
- [ ] Attack path visualization
- [ ] Vulnerability analysis view

**Deliverables**:
- 4 dashboard views
- Real-time data from APIs
- Interactive visualizations

### Week 4: Polish & Deploy
**Goal**: Production-ready application

**Tasks**:
- [ ] Error handling and edge cases
- [ ] Performance optimization (caching, lazy loading)
- [ ] Responsive design
- [ ] Testing suite
- [ ] Deployment configuration

**Deliverables**:
- Production-ready frontend
- Comprehensive tests
- Deployment guide

---

## 🎯 WHAT YOU HAVE ACCESS TO

### Operational APIs (Ready Now)

**NER11 API** (http://localhost:8000):
- ✅ 3 operational endpoints
- ✅ 3,889 real threat intelligence entities
- ✅ 60 NER labels
- ✅ 45 fine-grained types in current dataset
- ✅ Tested and documented

**Neo4j Database** (bolt://localhost:7687):
- ✅ 1,104,389 total nodes
- ✅ 331 hierarchical entities with NER properties
- ✅ 3.3M+ relationships
- ✅ 193 labels (16 Super Labels)
- ✅ Cypher query patterns documented

**Qdrant Vector Database** (http://localhost:6333):
- ✅ 3,889 entity vectors
- ✅ 384-dimensional embeddings
- ✅ 8 payload indexes
- ✅ Optional direct access for advanced use

### Documentation (Complete & Verbose)

**API Integration Guides**: 950+ lines
- Complete TypeScript type definitions
- React component examples
- React hooks ready to use
- Error handling patterns
- Performance optimization

**Neo4j Query Library**: 350+ lines
- Common query patterns
- Attack path queries
- Analytics queries
- JavaScript integration

**System Specifications**: 2,000+ lines
- Complete architecture
- Data models
- Schema definitions
- Performance requirements

---

## 💡 RECOMMENDED FIRST PROJECT

### Build: Threat Intelligence Search Application

**Complexity**: Moderate
**Time**: 2-3 weeks
**Tech Stack**: React + TypeScript + NER11 + Neo4j

**Features**:
1. **Search Interface**:
   - Text input for semantic search
   - Dropdown filters for fine-grained types (RANSOMWARE, PLC, etc.)
   - Results with similarity scores

2. **Entity Details**:
   - Full hierarchy path display
   - Source document reference
   - Related entities from graph

3. **Graph Visualization**:
   - D3.js force-directed graph
   - Show entity relationships
   - Interactive exploration

4. **Analytics Dashboard**:
   - Entity type distribution
   - Most common threat actors
   - Vulnerability statistics

**Starting Point**: Copy the React components from `09_NER11_FRONTEND_INTEGRATION_GUIDE.md` and customize.

---

## 🔗 CRITICAL FILE REFERENCES

**All documentation paths relative to**: `/home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/`

### Must-Read Files (In Order)

1. **`04_APIs/00_FRONTEND_QUICK_START.md`**
   - Quick start guide
   - 30-minute setup
   - First API calls

2. **`04_APIs/09_NER11_FRONTEND_INTEGRATION_GUIDE.md`**
   - Complete integration guide
   - TypeScript types
   - React components
   - Real-world examples

3. **`04_APIs/10_NEO4J_FRONTEND_QUERY_PATTERNS.md`**
   - Cypher query library
   - Neo4j driver setup
   - Common patterns

4. **`04_APIs/08_NER11_SEMANTIC_SEARCH_API.md`**
   - API specification
   - Request/response schemas
   - Performance targets

5. **`03_SPECIFICATIONS/07_NER11_HIERARCHICAL_INTEGRATION_COMPLETE_SPECIFICATION.md`**
   - System architecture
   - Data models
   - Validation rules

---

## 📊 CURRENT PRODUCTION DATA

**Available for Testing & Development**:

**Entities**: 3,889 cybersecurity entities
**Sources**: 18 threat intelligence vendor reports (2025)
**Vendors**: Mandiant, CrowdStrike, Cisco, SANS, Picus, ODNI, ReliaQuest, Trustwave, and 10 more

**Entity Types in Dataset**:
- Ransomware families
- Nation-state actors
- APT groups
- Vulnerabilities (CVEs)
- Industrial control devices (PLCs, RTUs, HMIs)
- Attack techniques
- Cognitive biases
- Security controls
- Protocols (Modbus, DNP3, etc.)

**Sample Queries You Can Run**:
```typescript
// 1. Find all ransomware
searchSemantic('ransomware', { fine_grained_filter: 'RANSOMWARE' })

// 2. Find nation-state actors
searchSemantic('APT groups', { fine_grained_filter: 'NATION_STATE' })

// 3. Find PLC vulnerabilities
searchSemantic('control system security', { fine_grained_filter: 'PLC' })

// 4. Find cognitive biases
searchSemantic('decision errors', { label_filter: 'COGNITIVE_BIAS' })
```

---

## ✅ PRE-FLIGHT CHECKLIST

Before starting development, verify:

- [ ] All backend services running:
  ```bash
  docker ps | grep -E "ner11|qdrant|neo4j"
  # Should show 3 containers: Up (healthy)
  ```

- [ ] NER11 API responding:
  ```bash
  curl http://localhost:8000/health
  # Should return: {"status":"healthy"...}
  ```

- [ ] Qdrant has data:
  ```bash
  curl http://localhost:6333/collections/ner11_entities_hierarchical
  # Should show: points_count: 3889
  ```

- [ ] Neo4j accessible:
  ```bash
  docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 1"
  # Should return: 1
  ```

- [ ] Documentation accessible:
  ```bash
  ls /home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/04_APIs/
  # Should list: 00_FRONTEND_QUICK_START.md, 09_NER11_FRONTEND_INTEGRATION_GUIDE.md, etc.
  ```

---

## 🎓 LEARNING RESOURCES

### Code Examples Available

**React Components**: 10+ complete components in `09_NER11_FRONTEND_INTEGRATION_GUIDE.md`
- EntityExtractor
- SemanticSearch
- HybridSearch
- ThreatCard
- AttackPathViewer
- VulnerabilityExplorer
- BiasAnalyzer
- And more...

**React Hooks**: 3 custom hooks ready to use
- `useSemanticSearch()` - Semantic search with loading/error states
- `useHybridSearch()` - Hybrid search with performance metrics
- `useNeo4j()` - Neo4j connection and query execution

**Service Classes**: 2 complete services
- `Neo4jService` - Complete Neo4j client with common queries
- API client examples with TypeScript types

**TypeScript Types**: Complete type definitions for:
- All request/response schemas
- Entity models
- Search results
- Graph data structures

---

## 🚨 IMPORTANT NOTES

### CORS Configuration

If you encounter CORS errors, add proxy to `package.json`:
```json
{
  "proxy": "http://localhost:8000"
}
```

Or use axios with proper headers:
```typescript
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
```

### Performance Expectations

**API Response Times** (tested with 3,889 entities):
- Entity extraction: <200ms
- Semantic search: <150ms
- Hybrid search: <500ms
- Neo4j simple query: <100ms
- Neo4j 2-hop query: <500ms

### Data Refresh

Current data is static (3,889 entities). To add more data:
```bash
cd /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model
python3 scripts/ingest_wiki_documents.py --wiki-root "[document-directory]" --limit 50
```

---

## 📞 SUPPORT & NEXT STEPS

**Questions About APIs**:
- Read: `04_APIs/README.md` in wiki
- Swagger UI: http://localhost:8000/docs

**Questions About Data**:
- Read: `08_Planned_Enhancements/E30_.../INGESTION_RESULTS_2025_THREAT_INTEL.md`
- Check: `03_SPECIFICATIONS/07_NER11_HIERARCHICAL_INTEGRATION_COMPLETE_SPECIFICATION.md`

**Questions About Infrastructure**:
- Read: `01_Infrastructure/E30_NER11_INFRASTRUCTURE.md`
- Status: `01_Infrastructure/E30_OPERATIONAL_STATUS.md`

**Ready to Start Development**: YES ✅
**All Documentation Complete**: YES ✅
**All APIs Tested**: YES ✅
**Real Data Available**: YES ✅ (3,889 entities)

---

**START BUILDING** → Copy code examples from `09_NER11_FRONTEND_INTEGRATION_GUIDE.md` and customize!

**Last Updated**: 2025-12-02 05:15:00 UTC
