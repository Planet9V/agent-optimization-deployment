# AEON Cyber Digital Twin - Complete Backend Reference for Frontend Developers

**File**: BACKEND_COMPLETE_REFERENCE.md
**Created**: 2025-12-02 22:00:00 UTC
**Modified**: 2025-12-02 22:00:00 UTC
**Version**: v1.0.0
**Author**: AEON Backend Team
**Purpose**: EVERYTHING a frontend developer needs to access the backend expertly
**Status**: PRODUCTION READY

---

## Table of Contents

1. [Quick Start - Get Running in 5 Minutes](#1-quick-start)
2. [System Overview](#2-system-overview)
3. [Connection Details](#3-connection-details)
4. [NER11 API - Complete Reference](#4-ner11-api)
5. [Neo4j Graph Database - Complete Reference](#5-neo4j-graph-database)
6. [Qdrant Vector Database - Complete Reference](#6-qdrant-vector-database)
7. [Data Models & TypeScript Types](#7-data-models)
8. [Security Taxonomy Data Sources](#8-security-taxonomy)
9. [Query Patterns for Common Use Cases](#9-query-patterns)
10. [React/TypeScript Code Examples](#10-code-examples)
11. [Error Handling](#11-error-handling)
12. [Performance Optimization](#12-performance)

---

## 1. Quick Start

### Verify All Services Are Running

```bash
# Test NER11 API
curl http://localhost:8000/health
# Expected: {"status":"healthy","ner_model":"loaded"}

# Test Neo4j
curl -X POST http://localhost:7474/db/neo4j/tx \
  -H "Content-Type: application/json" \
  -u neo4j:neo4j@openspg \
  -d '{"statements":[{"statement":"RETURN 1"}]}'

# Test Qdrant
curl http://localhost:6333/collections/ner11_entities_hierarchical
# Expected: {"result":{"points_count":49139,...}}
```

### Install Dependencies

```bash
npm install neo4j-driver axios
# or
yarn add neo4j-driver axios
```

### First API Call

```typescript
// Extract entities from text
const response = await fetch('http://localhost:8000/ner', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'APT29 used Cobalt Strike against energy sector systems exploiting CVE-2024-12345'
  })
});
const data = await response.json();
console.log(data.entities);
// Output: [
//   { text: "APT29", label: "THREAT_ACTOR", score: 0.95 },
//   { text: "Cobalt Strike", label: "MALWARE", score: 0.92 },
//   { text: "energy sector", label: "INDUSTRY", score: 0.88 },
//   { text: "CVE-2024-12345", label: "CVE", score: 0.99 }
// ]
```

---

## 2. System Overview

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND APPLICATION                      │
└───────────────────────────┬─────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  NER11 API    │  │    Neo4j      │  │    Qdrant     │
│  :8000        │  │    :7687      │  │    :6333      │
│               │  │               │  │               │
│  • /ner       │  │  • 332K nodes │  │  • 49K vectors│
│  • /search    │  │  • 11M rels   │  │  • Semantic   │
│  • /hybrid    │  │  • Graph      │  │    search     │
└───────────────┘  └───────────────┘  └───────────────┘
```

### What Each Service Provides

| Service | Purpose | Use When |
|---------|---------|----------|
| **NER11 API** | Entity extraction, semantic search | Processing user text input, searching |
| **Neo4j** | Graph queries, relationships, taxonomy | CVE lookups, attack path analysis, taxonomy navigation |
| **Qdrant** | Vector similarity search | Finding similar entities, fuzzy matching |

### Current Data State (2025-12-02)

| Metric | Value |
|--------|-------|
| Total Nodes | 332,750 |
| Total Relationships | 11,232,122 |
| CVE Count | 316,552 |
| EPSS Coverage | 94.9% |
| Extracted Entities | 49,139 |

---

## 3. Connection Details

### NER11 API

```typescript
const NER11_BASE_URL = 'http://localhost:8000';

// Health check
const health = await fetch(`${NER11_BASE_URL}/health`);

// Entity extraction
const ner = await fetch(`${NER11_BASE_URL}/ner`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'your text here' })
});

// Semantic search
const search = await fetch(`${NER11_BASE_URL}/search`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'search query', limit: 10 })
});
```

### Neo4j

```typescript
import neo4j from 'neo4j-driver';

const NEO4J_URI = 'bolt://localhost:7687';
const NEO4J_USER = 'neo4j';
const NEO4J_PASSWORD = 'neo4j@openspg';

const driver = neo4j.driver(
  NEO4J_URI,
  neo4j.auth.basic(NEO4J_USER, NEO4J_PASSWORD)
);

// Run a query
const session = driver.session();
try {
  const result = await session.run('MATCH (c:CVE) RETURN c LIMIT 10');
  const records = result.records.map(r => r.get('c').properties);
} finally {
  await session.close();
}
```

### Qdrant

```typescript
const QDRANT_URL = 'http://localhost:6333';
const COLLECTION_NAME = 'ner11_entities_hierarchical';

// Search by vector
const searchResults = await fetch(
  `${QDRANT_URL}/collections/${COLLECTION_NAME}/points/search`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      vector: [...], // 384-dimensional vector
      limit: 10,
      with_payload: true
    })
  }
);
```

---

## 4. NER11 API - Complete Reference

### 4.1 POST /ner - Entity Extraction

**Purpose**: Extract cybersecurity entities from text

**Request**:
```typescript
interface NERRequest {
  text: string;  // Text to analyze (max recommended: 50KB)
}
```

**Response**:
```typescript
interface NERResponse {
  entities: Array<{
    text: string;      // Entity text (e.g., "APT29")
    label: string;     // Entity type (e.g., "THREAT_ACTOR")
    start: number;     // Start character position
    end: number;       // End character position
    score: number;     // Confidence score (0-1)
  }>;
  processing_time: number;  // Milliseconds
}
```

**Entity Types (Labels)**:

| Label | Description | Examples |
|-------|-------------|----------|
| THREAT_ACTOR | Threat actors/APT groups | APT29, Lazarus Group, FIN7, Cozy Bear |
| MALWARE | Malware families | Cobalt Strike, Emotet, TrickBot, Ryuk |
| CVE | Vulnerability IDs | CVE-2024-12345, CVE-2023-44487 |
| TECHNIQUE | Attack techniques | Phishing, SQL Injection, Buffer Overflow |
| TOOL | Security/attack tools | Mimikatz, BloodHound, Nmap |
| INDUSTRY | Industry sectors | Healthcare, Energy, Financial Services |
| COUNTRY | Geographic locations | Russia, China, United States, Iran |
| CAMPAIGN | Attack campaigns | SolarWinds, NotPetya, WannaCry |
| VULNERABILITY | Vulnerability types | Remote Code Execution, XSS |
| PROTOCOL | Network protocols | HTTP, SMB, RDP |

**Example**:
```typescript
const response = await fetch('http://localhost:8000/ner', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'APT29 deployed Cobalt Strike beacon against healthcare organizations'
  })
});

const data = await response.json();
// data.entities = [
//   { text: "APT29", label: "THREAT_ACTOR", start: 0, end: 5, score: 0.95 },
//   { text: "Cobalt Strike", label: "MALWARE", start: 15, end: 28, score: 0.92 },
//   { text: "healthcare", label: "INDUSTRY", start: 45, end: 55, score: 0.88 }
// ]
```

---

### 4.2 POST /search - Semantic Search

**Purpose**: Find similar entities using semantic similarity

**Request**:
```typescript
interface SearchRequest {
  query: string;   // Search query
  limit?: number;  // Max results (default: 10)
  label?: string;  // Filter by entity type (optional)
}
```

**Response**:
```typescript
interface SearchResponse {
  results: Array<{
    text: string;
    label: string;
    score: number;      // Similarity score
    source_file: string;
  }>;
  query_time: number;
}
```

**Example**:
```typescript
const response = await fetch('http://localhost:8000/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'Russian APT groups',
    limit: 5,
    label: 'THREAT_ACTOR'
  })
});
```

---

### 4.3 POST /hybrid - Hybrid Search

**Purpose**: Combined semantic search + graph expansion

**Request**:
```typescript
interface HybridRequest {
  query: string;
  limit?: number;
  expand_graph?: boolean;  // Include related entities from Neo4j
}
```

**Response**:
```typescript
interface HybridResponse {
  semantic_results: SearchResult[];
  graph_results: GraphEntity[];
  combined_score: number;
}
```

---

### 4.4 GET /health - Health Check

**Response**:
```typescript
interface HealthResponse {
  status: "healthy" | "unhealthy";
  ner_model: "loaded" | "error";
  qdrant: "connected" | "disconnected";
  neo4j: "connected" | "disconnected";
}
```

---

## 5. Neo4j Graph Database - Complete Reference

### 5.1 Node Types (Labels)

#### CVE (Common Vulnerabilities and Exposures)
```typescript
interface CVENode {
  id: string;              // "CVE-2024-12345"
  description: string;     // Vulnerability description
  published: string;       // Publication date
  last_modified: string;   // Last modification date
  epss_score: number;      // EPSS probability (0-1)
  epss_percentile: number; // EPSS percentile (0-1)
  cvss_score: number;      // CVSS base score (0-10)
  cvss_vector: string;     // CVSS vector string
  priority_tier: string;   // "Tier1" | "Tier2" | "Tier3" | "Tier4"
}
```

**Priority Tiers**:
| Tier | Criteria | Urgency |
|------|----------|---------|
| Tier1 | EPSS > 0.5 OR CVSS >= 9.0 | Immediate |
| Tier2 | EPSS > 0.1 OR CVSS >= 7.0 | 30 days |
| Tier3 | EPSS > 0.01 OR CVSS >= 4.0 | 90 days |
| Tier4 | All others | Monitor |

#### CWE (Common Weakness Enumeration)
```typescript
interface CWENode {
  id: string;           // "cwe-79"
  name: string;         // "Cross-site Scripting (XSS)"
  description: string;
  abstraction: string;  // "Pillar" | "Class" | "Base" | "Variant"
  status: string;       // "Stable" | "Draft" | "Deprecated"
}
```

#### CAPEC (Common Attack Pattern Enumeration)
```typescript
interface CAPECNode {
  id: string;           // "capec-86"
  name: string;
  description: string;
  abstraction: string;  // "Meta" | "Standard" | "Detailed"
  likelihood: string;   // "Very Low" to "Very High"
  severity: string;     // "Very Low" to "Very High"
}
```

#### Technique (MITRE ATT&CK)
```typescript
interface TechniqueNode {
  id: string;              // "T1566" or "T1566.001"
  name: string;            // "Phishing"
  description: string;
  domain: string;          // "enterprise-attack" | "mobile-attack" | "ics-attack"
  is_subtechnique: boolean;
  detection: string;
  platforms: string[];
}
```

#### Tactic (MITRE ATT&CK)
```typescript
interface TacticNode {
  id: string;          // "TA0001"
  name: string;        // "Initial Access"
  shortname: string;   // "initial-access"
  domain: string;
}
```

#### EMB3D Nodes
```typescript
interface EMB3DThreatNode {
  id: string;
  name: string;
  description: string;
  type: "vulnerability";  // EMB3D uses 'vulnerability' type
}

interface EMB3DMitigationNode {
  id: string;
  name: string;
  description: string;
}

interface EMB3DPropertyNode {
  id: string;
  name: string;
  description: string;
}
```

#### Entity (NER11 Extracted)
```typescript
interface EntityNode {
  text: string;
  label: string;
  source_file: string;
  created_at: number;
  last_seen: number;
}
```

---

### 5.2 Relationships

| Relationship | From | To | Description |
|--------------|------|-----|-------------|
| HAS_WEAKNESS | CVE | CWE | CVE linked to weakness type |
| EXPLOITS_WEAKNESS | CAPEC | CWE | Attack pattern exploits weakness |
| MAPS_TO_TECHNIQUE | CAPEC | Technique | CAPEC maps to ATT&CK |
| BELONGS_TO | Technique | Tactic | Technique belongs to tactic |
| SUBTECHNIQUE_OF | Technique | Technique | Sub-technique relationship |
| CHILD_OF | CWE | CWE | CWE hierarchy |
| CHILD_OF | CAPEC | CAPEC | CAPEC hierarchy |
| MITIGATED_BY | EMB3DThreat | EMB3DMitigation | Threat mitigation |
| RELATED_TO | Entity | Entity | Entity co-occurrence |

---

### 5.3 Common Cypher Queries

#### Get High-Priority CVEs
```cypher
MATCH (c:CVE)
WHERE c.priority_tier IN ['Tier1', 'Tier2']
RETURN c.id, c.description, c.epss_score, c.cvss_score, c.priority_tier
ORDER BY c.epss_score DESC
LIMIT 20
```

#### Get CVE with Related Weaknesses and Attack Patterns
```cypher
MATCH (c:CVE {id: $cveId})-[:HAS_WEAKNESS]->(w:CWE)
OPTIONAL MATCH (a:CAPEC)-[:EXPLOITS_WEAKNESS]->(w)
OPTIONAL MATCH (a)-[:MAPS_TO_TECHNIQUE]->(t:Technique)
RETURN c, w, a, t
```

#### Get ATT&CK Matrix View
```cypher
MATCH (t:Technique)-[:BELONGS_TO]->(tac:Tactic)
WHERE t.domain = 'enterprise-attack'
RETURN tac.name as tactic, tac.id, collect({id: t.id, name: t.name}) as techniques
ORDER BY tac.id
```

#### Search CVEs by Description
```cypher
CALL db.index.fulltext.queryNodes('cve_search', $searchTerm) YIELD node, score
RETURN node.id, node.description, node.cvss_score, score
ORDER BY score DESC
LIMIT 10
```

#### Get Entity Network
```cypher
MATCH (e:Entity)-[r:RELATED_TO]->(related:Entity)
WHERE e.label = $entityType
RETURN e, r, related
LIMIT 100
```

---

## 6. Qdrant Vector Database - Complete Reference

### 6.1 Collection Details

**Collection Name**: `ner11_entities_hierarchical`

**Vector Configuration**:
- Dimensions: 384
- Distance: Cosine
- Model: sentence-transformers/all-MiniLM-L6-v2

**Payload Schema**:
```typescript
interface QdrantPayload {
  text: string;        // Entity text
  label: string;       // Entity type
  source_file: string; // Source document
  created_at: string;  // ISO timestamp
}
```

### 6.2 Search Endpoints

#### Vector Search
```typescript
// POST /collections/ner11_entities_hierarchical/points/search
const searchBody = {
  vector: number[],  // 384-dimensional vector
  limit: 10,
  with_payload: true,
  filter: {
    must: [
      { key: "label", match: { value: "THREAT_ACTOR" } }
    ]
  }
};
```

#### Get Collection Info
```typescript
// GET /collections/ner11_entities_hierarchical
interface CollectionInfo {
  result: {
    points_count: number;
    vectors_count: number;
    indexed_vectors_count: number;
    status: string;
  }
}
```

---

## 7. Data Models - TypeScript Types

### Complete Type Definitions

```typescript
// ============================================
// NER11 API Types
// ============================================

export interface NEREntity {
  text: string;
  label: EntityLabel;
  start: number;
  end: number;
  score: number;
}

export type EntityLabel =
  | 'THREAT_ACTOR'
  | 'MALWARE'
  | 'CVE'
  | 'TECHNIQUE'
  | 'TOOL'
  | 'INDUSTRY'
  | 'COUNTRY'
  | 'CAMPAIGN'
  | 'VULNERABILITY'
  | 'PROTOCOL';

export interface NERRequest {
  text: string;
}

export interface NERResponse {
  entities: NEREntity[];
  processing_time: number;
}

export interface SearchRequest {
  query: string;
  limit?: number;
  label?: EntityLabel;
}

export interface SearchResult {
  text: string;
  label: EntityLabel;
  score: number;
  source_file: string;
}

export interface SearchResponse {
  results: SearchResult[];
  query_time: number;
}

// ============================================
// Neo4j Node Types
// ============================================

export interface CVE {
  id: string;
  description: string;
  published: string;
  last_modified: string;
  epss_score: number;
  epss_percentile: number;
  cvss_score: number;
  cvss_vector: string;
  priority_tier: 'Tier1' | 'Tier2' | 'Tier3' | 'Tier4';
}

export interface CWE {
  id: string;
  name: string;
  description: string;
  abstraction: 'Pillar' | 'Class' | 'Base' | 'Variant' | 'Compound';
  status: 'Stable' | 'Draft' | 'Incomplete' | 'Deprecated';
}

export interface CAPEC {
  id: string;
  name: string;
  description: string;
  abstraction: 'Meta' | 'Standard' | 'Detailed';
  likelihood: string;
  severity: string;
}

export interface Technique {
  id: string;
  name: string;
  description: string;
  domain: 'enterprise-attack' | 'mobile-attack' | 'ics-attack';
  is_subtechnique: boolean;
  detection: string;
  platforms: string[];
}

export interface Tactic {
  id: string;
  name: string;
  shortname: string;
  domain: string;
}

export interface EMB3DThreat {
  id: string;
  name: string;
  description: string;
  type: 'vulnerability';
}

// ============================================
// Query Result Types
// ============================================

export interface CVEImpactResult {
  cve: CVE;
  weaknesses: CWE[];
  attackPatterns: CAPEC[];
  techniques: Technique[];
}

export interface AttackMatrixResult {
  tactic: string;
  tacticId: string;
  techniques: Array<{
    id: string;
    name: string;
  }>;
}

export interface EntityNetworkResult {
  entity: NEREntity;
  related: Array<{
    entity: NEREntity;
    relationship: string;
    weight: number;
  }>;
}
```

---

## 8. Security Taxonomy Data Sources

### 8.1 Overview

| Source | Nodes | Description | Update Frequency |
|--------|-------|-------------|------------------|
| NVD CVE | 316,552 | Vulnerabilities | Weekly |
| FIRST EPSS | - | Exploit prediction | Daily |
| MITRE CWE | 969 | Weaknesses | Annual |
| MITRE CAPEC | 615 | Attack patterns | Annual |
| MITRE ATT&CK | 1,063 | Techniques + Tactics | Quarterly |
| MITRE EMB3D | 288 | Embedded threats | As released |
| VulnCheck KEV | 10 | Known exploited | Weekly |

### 8.2 Data Source APIs

#### NVD (CVEs)
- **API**: `https://services.nvd.nist.gov/rest/json/cves/2.0`
- **Rate Limit**: 5 requests per 30 seconds (free tier)
- **Data**: CVE ID, description, CVSS scores, CWE links

#### FIRST.org (EPSS)
- **API**: `https://api.first.org/data/v1/epss`
- **Rate Limit**: Reasonable use
- **Data**: EPSS score, percentile per CVE

#### MITRE ATT&CK
- **Source**: GitHub STIX bundles
- **Format**: STIX 2.0 JSON
- **Domains**: Enterprise, Mobile, ICS

#### EMB3D
- **Source**: GitHub STIX bundle
- **Format**: STIX 2.0 JSON
- **Note**: Uses `vulnerability` type, NOT `attack-pattern`

---

## 9. Query Patterns for Common Use Cases

### 9.1 Threat Intelligence Dashboard

```typescript
// Get top threats by EPSS score
async function getTopThreats(limit: number = 10) {
  const session = driver.session();
  try {
    const result = await session.run(`
      MATCH (c:CVE)
      WHERE c.epss_score > 0.1
      RETURN c.id, c.description, c.epss_score, c.cvss_score, c.priority_tier
      ORDER BY c.epss_score DESC
      LIMIT $limit
    `, { limit });
    return result.records.map(r => r.toObject());
  } finally {
    await session.close();
  }
}
```

### 9.2 Attack Path Analysis

```typescript
// Get attack path from technique to weakness
async function getAttackPath(techniqueId: string) {
  const session = driver.session();
  try {
    const result = await session.run(`
      MATCH (t:Technique {id: $techniqueId})<-[:MAPS_TO_TECHNIQUE]-(a:CAPEC)
      MATCH (a)-[:EXPLOITS_WEAKNESS]->(w:CWE)
      MATCH (c:CVE)-[:HAS_WEAKNESS]->(w)
      WHERE c.priority_tier IN ['Tier1', 'Tier2']
      RETURN t, a, w, collect(c.id) as cves
      LIMIT 10
    `, { techniqueId });
    return result.records.map(r => r.toObject());
  } finally {
    await session.close();
  }
}
```

### 9.3 Entity Extraction & Enrichment

```typescript
// Extract entities and enrich with graph data
async function extractAndEnrich(text: string) {
  // 1. Extract entities
  const nerResponse = await fetch('http://localhost:8000/ner', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  const { entities } = await nerResponse.json();

  // 2. Enrich CVEs with graph data
  const cves = entities.filter(e => e.label === 'CVE');
  const enriched = [];

  const session = driver.session();
  try {
    for (const cve of cves) {
      const result = await session.run(`
        MATCH (c:CVE {id: $cveId})
        OPTIONAL MATCH (c)-[:HAS_WEAKNESS]->(w:CWE)
        RETURN c, collect(w) as weaknesses
      `, { cveId: cve.text });

      if (result.records.length > 0) {
        enriched.push({
          entity: cve,
          graphData: result.records[0].toObject()
        });
      }
    }
  } finally {
    await session.close();
  }

  return { entities, enriched };
}
```

### 9.4 Semantic Search with Filtering

```typescript
// Search entities with type filter
async function searchEntities(query: string, type?: string) {
  const body: any = { query, limit: 20 };
  if (type) body.label = type;

  const response = await fetch('http://localhost:8000/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });

  return response.json();
}
```

---

## 10. React/TypeScript Code Examples

### 10.1 API Client Hook

```typescript
// hooks/useAeonAPI.ts
import { useState, useCallback } from 'react';

const NER11_URL = 'http://localhost:8000';

export function useAeonAPI() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const extractEntities = useCallback(async (text: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${NER11_URL}/ner`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      if (!response.ok) throw new Error('NER API failed');
      return await response.json();
    } catch (e) {
      setError(e as Error);
      throw e;
    } finally {
      setLoading(false);
    }
  }, []);

  const searchEntities = useCallback(async (query: string, limit = 10) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${NER11_URL}/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, limit })
      });
      if (!response.ok) throw new Error('Search API failed');
      return await response.json();
    } catch (e) {
      setError(e as Error);
      throw e;
    } finally {
      setLoading(false);
    }
  }, []);

  return { extractEntities, searchEntities, loading, error };
}
```

### 10.2 Neo4j Hook

```typescript
// hooks/useNeo4j.ts
import { useMemo, useCallback, useState } from 'react';
import neo4j, { Driver } from 'neo4j-driver';

const NEO4J_URI = 'bolt://localhost:7687';
const NEO4J_USER = 'neo4j';
const NEO4J_PASSWORD = 'neo4j@openspg';

export function useNeo4j() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const driver = useMemo<Driver>(() => {
    return neo4j.driver(
      NEO4J_URI,
      neo4j.auth.basic(NEO4J_USER, NEO4J_PASSWORD)
    );
  }, []);

  const query = useCallback(async <T>(cypher: string, params: object = {}): Promise<T[]> => {
    setLoading(true);
    setError(null);
    const session = driver.session();
    try {
      const result = await session.run(cypher, params);
      return result.records.map(r => r.toObject() as T);
    } catch (e) {
      setError(e as Error);
      throw e;
    } finally {
      await session.close();
      setLoading(false);
    }
  }, [driver]);

  return { query, loading, error };
}
```

### 10.3 Entity Extraction Component

```tsx
// components/EntityExtractor.tsx
import React, { useState } from 'react';
import { useAeonAPI } from '../hooks/useAeonAPI';

interface Entity {
  text: string;
  label: string;
  score: number;
}

export function EntityExtractor() {
  const [text, setText] = useState('');
  const [entities, setEntities] = useState<Entity[]>([]);
  const { extractEntities, loading, error } = useAeonAPI();

  const handleExtract = async () => {
    try {
      const result = await extractEntities(text);
      setEntities(result.entities);
    } catch (e) {
      console.error(e);
    }
  };

  const labelColors: Record<string, string> = {
    THREAT_ACTOR: 'bg-red-100 text-red-800',
    MALWARE: 'bg-purple-100 text-purple-800',
    CVE: 'bg-yellow-100 text-yellow-800',
    TECHNIQUE: 'bg-blue-100 text-blue-800',
    TOOL: 'bg-gray-100 text-gray-800',
    INDUSTRY: 'bg-green-100 text-green-800',
    COUNTRY: 'bg-indigo-100 text-indigo-800',
  };

  return (
    <div className="p-4">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter threat intelligence text..."
        className="w-full h-32 p-2 border rounded"
      />
      <button
        onClick={handleExtract}
        disabled={loading}
        className="mt-2 px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
      >
        {loading ? 'Extracting...' : 'Extract Entities'}
      </button>

      {error && <p className="text-red-500 mt-2">{error.message}</p>}

      <div className="mt-4 flex flex-wrap gap-2">
        {entities.map((entity, i) => (
          <span
            key={i}
            className={`px-2 py-1 rounded text-sm ${labelColors[entity.label] || 'bg-gray-100'}`}
            title={`Score: ${entity.score.toFixed(2)}`}
          >
            {entity.text} ({entity.label})
          </span>
        ))}
      </div>
    </div>
  );
}
```

### 10.4 CVE Dashboard Component

```tsx
// components/CVEDashboard.tsx
import React, { useEffect, useState } from 'react';
import { useNeo4j } from '../hooks/useNeo4j';

interface CVE {
  id: string;
  description: string;
  epss_score: number;
  cvss_score: number;
  priority_tier: string;
}

export function CVEDashboard() {
  const [cves, setCves] = useState<CVE[]>([]);
  const { query, loading, error } = useNeo4j();

  useEffect(() => {
    loadTopCVEs();
  }, []);

  const loadTopCVEs = async () => {
    const results = await query<{ c: CVE }>(`
      MATCH (c:CVE)
      WHERE c.priority_tier IN ['Tier1', 'Tier2']
      RETURN c
      ORDER BY c.epss_score DESC
      LIMIT 20
    `);
    setCves(results.map(r => r.c.properties));
  };

  const tierColors: Record<string, string> = {
    Tier1: 'bg-red-500',
    Tier2: 'bg-orange-500',
    Tier3: 'bg-yellow-500',
    Tier4: 'bg-green-500',
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="text-red-500">{error.message}</div>;

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">High Priority CVEs</h2>
      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 text-left">CVE ID</th>
            <th className="p-2 text-left">EPSS</th>
            <th className="p-2 text-left">CVSS</th>
            <th className="p-2 text-left">Tier</th>
          </tr>
        </thead>
        <tbody>
          {cves.map((cve) => (
            <tr key={cve.id} className="border-b">
              <td className="p-2 font-mono">{cve.id}</td>
              <td className="p-2">{(cve.epss_score * 100).toFixed(2)}%</td>
              <td className="p-2">{cve.cvss_score.toFixed(1)}</td>
              <td className="p-2">
                <span className={`px-2 py-1 rounded text-white text-sm ${tierColors[cve.priority_tier]}`}>
                  {cve.priority_tier}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

---

## 11. Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `ECONNREFUSED :8000` | NER11 API not running | Start the API service |
| `ECONNREFUSED :7687` | Neo4j not running | Start Neo4j container |
| `ECONNREFUSED :6333` | Qdrant not running | Start Qdrant container |
| `Neo4j auth failed` | Wrong credentials | Use `neo4j/neo4j@openspg` |
| `Timeout` | Large document | Use chunked processing |
| `Empty entities` | No recognized entities | Check input text format |

### Error Handling Pattern

```typescript
async function safeQuery<T>(fn: () => Promise<T>): Promise<{ data: T | null; error: Error | null }> {
  try {
    const data = await fn();
    return { data, error: null };
  } catch (error) {
    console.error('Query failed:', error);
    return { data: null, error: error as Error };
  }
}

// Usage
const { data, error } = await safeQuery(() => extractEntities(text));
if (error) {
  showNotification('Failed to extract entities', 'error');
} else {
  setEntities(data.entities);
}
```

---

## 12. Performance Optimization

### 12.1 Caching

```typescript
// Simple in-memory cache
const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

async function cachedQuery<T>(key: string, fn: () => Promise<T>): Promise<T> {
  const cached = cache.get(key);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }

  const data = await fn();
  cache.set(key, { data, timestamp: Date.now() });
  return data;
}
```

### 12.2 Debouncing Search

```typescript
import { useMemo } from 'react';
import { debounce } from 'lodash';

export function useDebounceSearch() {
  const { searchEntities } = useAeonAPI();

  const debouncedSearch = useMemo(
    () => debounce(searchEntities, 300),
    [searchEntities]
  );

  return debouncedSearch;
}
```

### 12.3 Pagination for Large Results

```cypher
// Paginated CVE query
MATCH (c:CVE)
WHERE c.priority_tier = $tier
RETURN c
ORDER BY c.epss_score DESC
SKIP $skip
LIMIT $limit
```

```typescript
const PAGE_SIZE = 20;

async function loadPage(page: number, tier: string) {
  return query(`
    MATCH (c:CVE)
    WHERE c.priority_tier = $tier
    RETURN c
    ORDER BY c.epss_score DESC
    SKIP $skip
    LIMIT $limit
  `, {
    tier,
    skip: page * PAGE_SIZE,
    limit: PAGE_SIZE
  });
}
```

---

## Summary

This document provides complete reference for frontend developers to integrate with the AEON Cyber Digital Twin backend. Key points:

1. **Three main services**: NER11 API (entity extraction), Neo4j (graph database), Qdrant (vector search)
2. **Rich data**: 332K+ nodes, 11M+ relationships across 9 security taxonomy sources
3. **TypeScript types**: Complete type definitions for all data models
4. **React hooks**: Ready-to-use hooks for API and database access
5. **Query patterns**: Common use cases with working Cypher queries
6. **Error handling**: Comprehensive error handling patterns
7. **Performance**: Caching, debouncing, and pagination strategies

For additional details, refer to:
- `04_APIs/API_DATA_SOURCES_COMPREHENSIVE.md` - Complete API documentation
- `03_SPECIFICATIONS/08_NEO4J_SECURITY_TAXONOMY_SCHEMA_v4.0_2025-12-02.md` - Full schema spec
- `11_EXTRA/DATA_UPDATE_PROCEDURES.md` - Data update procedures
