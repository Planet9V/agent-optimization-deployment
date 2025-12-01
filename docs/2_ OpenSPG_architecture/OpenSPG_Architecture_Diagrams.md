# OpenSPG Architecture Diagrams

**File:** OpenSPG_Architecture_Diagrams.md
**Created:** 2025-10-26
**Version:** 1.0.0
**Author:** Architecture Analysis Agent
**Status:** ACTIVE

## Overview

This document provides visual representations of OpenSPG's architecture using ASCII diagrams and component relationship charts.

---

## 1. High-Level System Architecture

```
╔═══════════════════════════════════════════════════════════════════════╗
║                         OpenSPG Platform                              ║
║                   Semantic-Enhanced Programmable Graph                ║
╚═══════════════════════════════════════════════════════════════════════╝

                            User Applications
                                    │
                                    ↓
┌───────────────────────────────────────────────────────────────────────┐
│                         REST API Layer                                │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ Query   │  │ Concept │  │ Reason  │  │Retrieval│  │DataSrc  │   │
│  │ API     │  │   API   │  │   API   │  │   API   │  │  API    │   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
└───────────────────────────────────────────────────────────────────────┘
                                    │
                                    ↓
╔═══════════════════════════════════════════════════════════════════════╗
║                    Layer 5: KNext Framework                           ║
║              Programmable, Componentized Abstractions                 ║
╚═══════════════════════════════════════════════════════════════════════╝
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ↓                           ↓                           ↓
┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐
│  Layer 4:         │   │  Layer 3:         │   │  Layer 2:         │
│  SPG-Reasoner     │   │  SPG-Builder      │   │  SPG-Schema       │
│                   │   │                   │   │                   │
│ ┌───────────────┐ │   │ ┌───────────────┐ │   │ ┌───────────────┐ │
│ │ KGDSL Parser  │ │   │ │ Data Ingestion│ │   │ │ Subject Model │ │
│ └───────────────┘ │   │ └───────────────┘ │   │ └───────────────┘ │
│ ┌───────────────┐ │   │ ┌───────────────┐ │   │ ┌───────────────┐ │
│ │ Logic Engine  │ │   │ │ LLM Extract   │ │   │ │Predicate Model│ │
│ └───────────────┘ │   │ └───────────────┘ │   │ └───────────────┘ │
│ ┌───────────────┐ │   │ ┌───────────────┐ │   │ ┌───────────────┐ │
│ │ Query Optim.  │ │   │ │ Entity Linking│ │   │ │Evolution Model│ │
│ └───────────────┘ │   │ └───────────────┘ │   │ └───────────────┘ │
└───────────────────┘   └───────────────────┘   └───────────────────┘
                                    │
                                    ↓
╔═══════════════════════════════════════════════════════════════════════╗
║                    Layer 1: Cloudext                                  ║
║                  Infrastructure Abstraction                           ║
╚═══════════════════════════════════════════════════════════════════════╝
        │                    │                    │
        ↓                    ↓                    ↓
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Graph Store  │    │Search Engine │    │    Cache     │
│              │    │              │    │              │
│ • Neo4j      │    │ •Elasticsearch│   │ • Redis      │
│ • TuGraph    │    │ • Neo4j FT   │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
        │                    │                    │
        └────────────────────┴────────────────────┘
                            ↓
                  ┌─────────────────────┐
                  │  Physical Storage   │
                  │  (Graph + Relational)│
                  └─────────────────────┘
```

---

## 2. Server Module Internal Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Server Module (server/)                      │
└─────────────────────────────────────────────────────────────────┘

                        External Clients
                              │
                              ↓
        ┌─────────────────────────────────────────┐
        │         API Layer (Presentation)        │
        ├─────────────────────────────────────────┤
        │  ┌──────────┐  ┌──────────┐            │
        │  │http-server│  │http-client│           │
        │  │           │  │           │           │
        │  │Controllers│  │ SDK       │           │
        │  └──────────┘  └──────────┘            │
        │          ↑                              │
        │          │                              │
        │  ┌───────┴────────┐                    │
        │  │    facade      │                    │
        │  │ Service Facades│                    │
        │  └────────────────┘                    │
        └─────────────────────────────────────────┘
                        │
                        ↓
        ┌─────────────────────────────────────────┐
        │      Business Logic Layer (biz/)        │
        ├─────────────────────────────────────────┤
        │  ┌──────────┐  ┌──────────┐            │
        │  │biz/common│  │biz/schema│            │
        │  └──────────┘  └──────────┘            │
        │  ┌──────────┐                          │
        │  │biz/service│                         │
        │  └──────────┘                          │
        └─────────────────────────────────────────┘
                        │
                        ↓
        ┌─────────────────────────────────────────┐
        │         Core Domain Layer (core/)       │
        ├─────────────────────────────────────────┤
        │  ┌──────────┐  ┌──────────┐            │
        │  │  schema  │  │scheduler │            │
        │  │          │  │          │            │
        │  │model+svc │  │model+svc │            │
        │  └──────────┘  └──────────┘            │
        │  ┌──────────┐                          │
        │  │ reasoner │                          │
        │  │          │                          │
        │  │model+svc │                          │
        │  └──────────┘                          │
        └─────────────────────────────────────────┘
                        │
                        ↓
        ┌─────────────────────────────────────────┐
        │   Infrastructure Layer (infra/ + common/)│
        ├─────────────────────────────────────────┤
        │  ┌──────────┐  ┌──────────┐            │
        │  │infra/dao │  │  common  │            │
        │  │          │  │          │            │
        │  │ MyBatis  │  │model+svc │            │
        │  └──────────┘  └──────────┘            │
        └─────────────────────────────────────────┘
                        │
                        ↓
        ┌─────────────────────────────────────────┐
        │         Framework Layer (arks/)         │
        ├─────────────────────────────────────────┤
        │  ┌────────────────────────┐             │
        │  │   arks/sofaboot        │             │
        │  │                        │             │
        │  │ SOFA Boot Integration  │             │
        │  └────────────────────────┘             │
        └─────────────────────────────────────────┘
                        │
                        ↓
                ┌───────┴────────┐
                ↓                ↓
        ┌──────────────┐  ┌──────────────┐
        │    MySQL     │  │  Cloudext    │
        │  (Metadata)  │  │  (KG Store)  │
        └──────────────┘  └──────────────┘
```

**Layer Responsibilities:**

| Layer | Responsibility | Key Components |
|-------|----------------|----------------|
| **API** | Request handling, response formatting | Controllers, HTTP server |
| **Business** | Business rules, validation, orchestration | Service implementations |
| **Core** | Domain logic, core algorithms | Schema, scheduler, reasoner |
| **Infrastructure** | Data access, external system integration | DAO, common utilities |
| **Framework** | Cross-cutting concerns, configuration | SOFA Boot setup |

---

## 3. Reasoner Module Query Pipeline

```
┌──────────────────────────────────────────────────────────────┐
│               Reasoner Module (reasoner/)                    │
└──────────────────────────────────────────────────────────────┘

User Query: "MATCH (p:Person)-[:WORKS_AT]->(c:Company) RETURN p.name"
                            │
                            ↓
        ┌───────────────────────────────────┐
        │   KGDSL Parser (kgdsl-parser/)    │
        ├───────────────────────────────────┤
        │  • ANTLR4 Grammar                 │
        │  • Lexical Analysis               │
        │  • Syntax Parsing                 │
        │  • AST Generation                 │
        └───────────────────────────────────┘
                            │
                            ↓
              Abstract Syntax Tree (AST)
                            │
                            ↓
        ┌───────────────────────────────────┐
        │     LUBE-API (lube-api/)          │
        ├───────────────────────────────────┤
        │  • Query Interface Definitions    │
        │  • Operator Abstractions          │
        │  • Pattern Matching API           │
        └───────────────────────────────────┘
                            │
                            ↓
        ┌───────────────────────────────────┐
        │   LUBE-Logical (lube-logical/)    │
        ├───────────────────────────────────┤
        │  • Logical Plan Construction      │
        │  • Rule-Based Optimization        │
        │    - Predicate pushdown           │
        │    - Join reordering              │
        │    - Filter early application     │
        │  • Cost estimation                │
        └───────────────────────────────────┘
                            │
                            ↓
             Optimized Logical Plan
                            │
                            ↓
        ┌───────────────────────────────────┐
        │  LUBE-Physical (lube-physical/)   │
        ├───────────────────────────────────┤
        │  • Physical Plan Generation       │
        │  • Execution Strategy Selection   │
        │    - Index lookup vs scan         │
        │    - Hash join vs nested loop     │
        │    - Parallel vs sequential       │
        │  • Resource allocation            │
        └───────────────────────────────────┘
                            │
                            ↓
              Physical Execution Plan
                            │
                            ↓
        ┌───────────────────────────────────┐
        │      Runner (runner/)             │
        ├───────────────────────────────────┤
        │  • Local Execution Engine         │
        │  • Operator Implementation        │
        │  • Memory management              │
        │  • Result materialization         │
        └───────────────────────────────────┘
                            │
                            ├───→ ┌─────────────────┐
                            │     │ UDF (udf/)      │
                            │     │ User Functions  │
                            │     └─────────────────┘
                            ↓
        ┌───────────────────────────────────┐
        │    Warehouse (warehouse/)         │
        ├───────────────────────────────────┤
        │  • Storage Abstraction            │
        │  • Cloudext Integration           │
        │  • Data source federation         │
        └───────────────────────────────────┘
                            │
                            ↓
        ┌───────────────────────────────────┐
        │     Catalog (catalog/)            │
        ├───────────────────────────────────┤
        │  • Schema Registry                │
        │  • Metadata Management            │
        │  • Type Information               │
        └───────────────────────────────────┘
                            │
                            ↓
                   Query Results
```

**Optimization Stages:**

```
Logical Optimization:
  Input:  SELECT * FROM Person WHERE age > 30 AND city = 'NYC'
  ↓
  Apply predicate pushdown:
  Output: Filter early → reduces data scanned

Physical Optimization:
  Input:  JOIN Person, Company ON Person.company_id = Company.id
  ↓
  Choose join strategy:
  - If small table: Hash join
  - If indexed: Index nested loop
  - If parallel: Partitioned hash join
  ↓
  Output: Optimal physical plan
```

---

## 4. Builder Module Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────┐
│               Builder Module (builder/)                      │
└──────────────────────────────────────────────────────────────┘

                     Data Sources
                          │
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
   ┌────────┐      ┌────────┐      ┌────────┐
   │  CSV   │      │  JSON  │      │   DB   │
   │  Files │      │  Files │      │ Tables │
   └────────┘      └────────┘      └────────┘
        │                 │                 │
        └─────────────────┴─────────────────┘
                          ↓
        ┌─────────────────────────────────────┐
        │  StringSourceNode                   │
        │  • Data loading                     │
        │  • Format detection                 │
        │  • Character encoding               │
        └─────────────────────────────────────┘
                          │
                          ↓
        ┌─────────────────────────────────────┐
        │  LLMBasedExtractNode                │
        │  • Entity extraction                │
        │  • Relation extraction              │
        │  • NLP processing                   │
        │  • Prompt engineering               │
        └─────────────────────────────────────┘
                          │
                          ↓
        ┌─────────────────────────────────────┐
        │  SPGTypeMappingNode                 │
        │  • Schema alignment                 │
        │  • Type inference                   │
        │  • Property mapping                 │
        │  • Constraint validation            │
        └─────────────────────────────────────┘
                          │
                          ↓
        ┌─────────────────────────────────────┐
        │  ConceptReasoner                    │
        │  • Inductive reasoning              │
        │  • Causal reasoning                 │
        │  • Concept standardization          │
        │  • Taxonomy alignment               │
        └─────────────────────────────────────┘
                          │
                          ↓
        ┌─────────────────────────────────────┐
        │  RelationMappingNode                │
        │  • Relationship extraction          │
        │  • Relation type inference          │
        │  • Multi-hop relations              │
        └─────────────────────────────────────┘
                          │
                          ↓
        ┌─────────────────────────────────────┐
        │  VectorizerProcessorNode            │
        │  • Text embedding                   │
        │  • Semantic vectors                 │
        │  • Similarity indexing              │
        └─────────────────────────────────────┘
                          │
                          ↓
        ┌─────────────────────────────────────┐
        │  BuilderIndexNode                   │
        │  • Index creation                   │
        │  • Search optimization              │
        │  • Full-text indexing               │
        └─────────────────────────────────────┘
                          │
                          ↓
        ┌─────────────────────────────────────┐
        │  ExtractPostProcessorNode           │
        │  • Data cleaning                    │
        │  • Duplicate detection              │
        │  • Quality assurance                │
        └─────────────────────────────────────┘
                          │
                          ↓
        ┌─────────────────────────────────────┐
        │  Runner (runner/local/)             │
        │  • Pipeline execution               │
        │  • Error handling                   │
        │  • Progress tracking                │
        └─────────────────────────────────────┘
                          │
                          ↓
                 Knowledge Graph Store
                (via Cloudext abstraction)
```

**Logical Plan Example:**

```
User defines pipeline:
  source → extract → map → reason → store

Builder creates DAG:
  ┌──────────────┐
  │ StringSource │
  └──────┬───────┘
         ↓
  ┌──────┴───────┐
  │ LLMExtract   │
  └──────┬───────┘
         ↓
  ┌──────┴───────┐
  │ TypeMapping  │
  └──────┬───────┘
         ↓
  ┌──────┴───────┐
  │ Reasoner     │
  └──────┬───────┘
         ↓
  ┌──────┴───────┐
  │ Store        │
  └──────────────┘

Runner executes DAG with:
  • Parallel processing where possible
  • Checkpointing for fault tolerance
  • Resource management
```

---

## 5. Cloudext Abstraction Layer

```
┌──────────────────────────────────────────────────────────────┐
│            Cloudext Module (cloudext/)                       │
└──────────────────────────────────────────────────────────────┘

                  Application Code
                        │
                        ↓
        ┌───────────────────────────────────┐
        │   Interface Layer (interface/)    │
        └───────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┬────────────────┬───────────────┐
        ↓               ↓               ↓                ↓               ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│GraphStore    │ │SearchEngine  │ │    Cache     │ │ObjectStorage │ │ComputeEngine │
│Interface     │ │Interface     │ │  Interface   │ │  Interface   │ │  Interface   │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
        │               │               │                │               │
        ↓               ↓               ↓                ↓               ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│              │ │              │ │              │ │              │ │              │
│ Impl Layer   │ │ Impl Layer   │ │ Impl Layer   │ │ Impl Layer   │ │ Impl Layer   │
│   (impl/)    │ │   (impl/)    │ │   (impl/)    │ │   (impl/)    │ │   (impl/)    │
│              │ │              │ │              │ │              │ │              │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
        │               │               │                │               │
┌───────┴─────┐ ┌───────┴──────┐ ┌──────┴──────┐ ┌─────┴───────┐       │
↓             ↓ ↓              ↓ │             │ ↓             ↓       ↓
┌───────┐ ┌───────┐ ┌────────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Neo4j  │ │TuGraph│ │Elastic │ │Neo4j  │ │ Redis │ │ MinIO │ │  OSS  │ │ Local │
│Adapter│ │Adapter│ │Adapter │ │FT Adap│ │Adapter│ │Adapter│ │Adapter│ │ Exec  │
└───────┘ └───────┘ └────────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘
    │         │         │          │          │         │         │         │
    ↓         ↓         ↓          ↓          ↓         ↓         ↓         ↓
┌───────┐ ┌───────┐ ┌────────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Neo4j  │ │TuGraph│ │Elastic │ │Neo4j  │ │ Redis │ │ MinIO │ │Alibaba│ │ Local │
│Server │ │Server │ │Server  │ │Server │ │Server │ │Server │ │ OSS   │ │ FS    │
└───────┘ └───────┘ └────────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘
```

**Interface Example:**

```java
// Application code uses interface only
public interface GraphStoreService {
    void storeVertex(Vertex vertex);
    void storeEdge(Edge edge);
    List<Vertex> queryVertices(Query query);
    void deleteVertex(String vertexId);
}

// Configuration determines implementation
Configuration:
  graph.store.type: neo4j  # or tugraph, or custom

Runtime binding:
  GraphStoreService → Neo4jGraphStoreServiceImpl
                  OR  TuGraphStoreServiceImpl
                  OR  CustomGraphStoreServiceImpl

Benefits:
  ✓ Application code unchanged when switching backends
  ✓ Easy A/B testing of different storage engines
  ✓ Multi-cloud portability
  ✓ Testing with mock implementations
```

---

## 6. Data Flow: End-to-End Knowledge Construction

```
┌────────────────────────────────────────────────────────────────┐
│           Complete Knowledge Construction Flow                 │
└────────────────────────────────────────────────────────────────┘

Step 1: Data Ingestion
━━━━━━━━━━━━━━━━━━━━━━
External Data Sources
    │
    ├─→ CSV Files ──→ StringSourceNode
    ├─→ JSON Data ──→ StringSourceNode
    └─→ Databases ──→ StringSourceNode
              │
              ↓
    [Raw Data in Memory]

Step 2: Knowledge Extraction
━━━━━━━━━━━━━━━━━━━━━━━━━━━
    [Raw Data in Memory]
              │
              ↓
    LLMBasedExtractNode
    • Entity recognition: "Apple Inc." → Company
    • Relation extraction: (Tim Cook, CEO_OF, Apple Inc.)
    • Attribute extraction: founded_year = 1976
              │
              ↓
    [Extracted Entities & Relations]

Step 3: Schema Alignment
━━━━━━━━━━━━━━━━━━━━━━━━
    [Extracted Entities & Relations]
              │
              ↓
    SPGTypeMappingNode
    • Map to SPG-Schema types
    • "Apple Inc." → Type:Company
    • Validate property constraints
    • Type inference and correction
              │
              ↓
    [Schema-Aligned Knowledge]

Step 4: Reasoning & Enrichment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    [Schema-Aligned Knowledge]
              │
              ↓
    ConceptReasoner
    • Inductive: Apple Inc. ∈ TechnologyCompany
    • Causal: headquartered_in_CA → subject_to_CA_law
    • Taxonomic alignment
              │
              ↓
    [Enriched Knowledge Graph]

Step 5: Relation Processing
━━━━━━━━━━━━━━━━━━━━━━━━━━━
    [Enriched Knowledge Graph]
              │
              ↓
    RelationMappingNode
    • Direct relations: (Tim Cook)-[:CEO_OF]->(Apple)
    • Inferred relations: (Apple)-[:EMPLOYS]->(Tim Cook)
    • Multi-hop: (Tim Cook)-[:WORKS_IN]->(Technology Industry)
              │
              ↓
    [Complete Relation Graph]

Step 6: Vectorization
━━━━━━━━━━━━━━━━━━━━━
    [Complete Relation Graph]
              │
              ↓
    VectorizerProcessorNode
    • Text embedding for entities
    • Semantic similarity indexing
    • Vector storage preparation
              │
              ↓
    [Graph + Vector Embeddings]

Step 7: Indexing
━━━━━━━━━━━━━━━━
    [Graph + Vector Embeddings]
              │
              ↓
    BuilderIndexNode
    • Create search indices
    • Full-text indexing
    • Property indexing for queries
              │
              ↓
    [Indexed Knowledge Graph]

Step 8: Quality Assurance
━━━━━━━━━━━━━━━━━━━━━━━━━
    [Indexed Knowledge Graph]
              │
              ↓
    ExtractPostProcessorNode
    • Duplicate detection
    • Consistency validation
    • Data cleaning
              │
              ↓
    [Validated Knowledge]

Step 9: Storage
━━━━━━━━━━━━━━━
    [Validated Knowledge]
              │
              ↓
    Cloudext Abstraction
              │
    ┌─────────┴─────────┐
    ↓                   ↓
[Graph Store]     [Search Engine]
 (Neo4j/TuGraph)   (Elasticsearch)
    ↓                   ↓
[Persistent Knowledge Graph]
```

---

## 7. Query Execution: End-to-End Flow

```
┌────────────────────────────────────────────────────────────────┐
│              Complete Query Execution Flow                     │
└────────────────────────────────────────────────────────────────┘

User Query: "Find all CEOs of technology companies in California"
KGDSL: MATCH (p:Person)-[:CEO_OF]->(c:Company {industry:'Tech'})
       WHERE c.state = 'CA' RETURN p.name, c.name

Phase 1: Parsing
━━━━━━━━━━━━━━━━
User Query Text
      │
      ↓
KGDSL Parser (ANTLR4)
  • Lexical analysis
  • Syntax validation
  • AST construction
      │
      ↓
Abstract Syntax Tree:
  MatchClause(
    Pattern(Person → CEO_OF → Company),
    Filter(industry='Tech', state='CA'),
    Return(p.name, c.name)
  )

Phase 2: Logical Planning
━━━━━━━━━━━━━━━━━━━━━━━
AST
      │
      ↓
Logical Planner
  • Pattern to operator conversion
  • Filter pushdown
  • Join reordering
      │
      ↓
Logical Plan:
  Project(p.name, c.name)
    └─ Filter(c.state='CA')
         └─ Join(CEO_OF)
              ├─ Scan(Person) as p
              └─ Scan(Company, industry='Tech') as c

Optimizations Applied:
  ✓ Push state filter to Company scan
  ✓ Push industry filter to Company scan
  ✓ Reduce join input size

Phase 3: Physical Planning
━━━━━━━━━━━━━━━━━━━━━━━━
Logical Plan
      │
      ↓
Physical Planner
  • Choose execution algorithms
  • Select access methods
  • Estimate costs
      │
      ↓
Physical Plan:
  Project
    └─ HashJoin (build=Company, probe=Person)
         ├─ IndexScan(Company.industry='Tech')
         │    └─ Filter(state='CA')
         └─ IndexScan(Person)
              └─ ExpandOut(CEO_OF)

Cost Estimation:
  Company filtered: 1000 → 50 rows
  Person with CEO_OF: 10000 → 100 rows
  Join cost: O(50 + 100) with hash table

Phase 4: Execution
━━━━━━━━━━━━━━━━━
Physical Plan
      │
      ↓
Local Runner
      │
      ├─→ Warehouse Layer
      │     └─ Cloudext (Neo4j)
      │           │
      │           ↓
      │   [Execute Cypher/Native Queries]
      │           │
      │           ↓
      │   [Fetch filtered companies]
      │   [Fetch persons with CEO_OF relation]
      │           │
      │           ↓
      │   Return partial results
      │
      ├─→ Join Processor
      │     • Build hash table from companies
      │     • Probe with persons
      │     • Match on relationship
      │           │
      │           ↓
      │   Joined tuples
      │
      └─→ Projection
            • Extract p.name, c.name
            • Format results
                  │
                  ↓
            Final Results:
            [
              {person: "Tim Cook", company: "Apple Inc."},
              {person: "Sundar Pichai", company: "Google"},
              ...
            ]

Phase 5: Result Delivery
━━━━━━━━━━━━━━━━━━━━━━━
Final Results
      │
      ↓
Runner → Server
      │
      ↓
QueryController (REST API)
      │
      ↓
HTTP Response (JSON)
      │
      ↓
Client Application
```

---

## 8. Technology Stack Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Technology Stack                         │
└─────────────────────────────────────────────────────────────┘

Application Layer
━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────┐
│ Business Applications & Services        │
│ • Domain-specific KG applications       │
│ • Analytics dashboards                  │
│ • AI/ML integration                     │
└─────────────────────────────────────────┘

API & Framework Layer
━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────┐
│ SOFA Boot 3.17.0                        │
│ ├─ Spring Boot 2.7.8                    │
│ ├─ Spring Framework 5.3.21              │
│ └─ SpringDoc OpenAPI 1.7.0              │
└─────────────────────────────────────────┘

Language & Runtime Layer
━━━━━━━━━━━━━━━━━━━━━━━━
┌───────────────┐  ┌──────────────┐
│ Java 1.8      │  │ Scala 2.11.12│
│ • Server      │  │ • Reasoner   │
│ • Builder     │  │ • KGDSL      │
│ • APIs        │  │ • Functional │
└───────────────┘  └──────────────┘
        │                  │
        └─────────┬────────┘
                  ↓
        ┌─────────────────┐
        │  JVM Runtime    │
        └─────────────────┘

Data Processing Layer
━━━━━━━━━━━━━━━━━━━━━
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ ANTLR4 4.8   │  │ Cats 2.0     │  │ GeoTools 27  │
│ • DSL Parse  │  │ • Functional │  │ • Geospatial │
└──────────────┘  └──────────────┘  └──────────────┘

Persistence Layer
━━━━━━━━━━━━━━━━━
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ MyBatis 3.5  │  │ MySQL 5.1    │  │ Neo4j 4.4.7  │
│ • ORM        │  │ • Metadata   │  │ • Graph DB   │
└──────────────┘  └──────────────┘  └──────────────┘
                                    ┌──────────────┐
                                    │ TuGraph 1.4  │
                                    │ • Graph DB   │
                                    └──────────────┘

Big Data Layer
━━━━━━━━━━━━━━
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Hadoop 2.7.2 │  │ Hive 3.1.0   │  │ Parquet 1.10 │
│ • HDFS       │  │ • Warehouse  │  │ • Columnar   │
└──────────────┘  └──────────────┘  └──────────────┘

Infrastructure Layer
━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────┐
│ Cloudext Abstraction                    │
│ ├─ Graph Store (Neo4j, TuGraph)         │
│ ├─ Search Engine (Elasticsearch)        │
│ ├─ Cache (Redis)                        │
│ ├─ Object Storage (MinIO, OSS)          │
│ └─ Compute Engine (Local, Distributed)  │
└─────────────────────────────────────────┘
```

---

## 9. Deployment Architectures

### 9.1 Single-Node Development Setup

```
┌──────────────────────────────────────────┐
│      Developer Machine / VM              │
│                                          │
│  ┌────────────────────────────────┐     │
│  │   OpenSPG Application          │     │
│  │   (all modules in one JVM)     │     │
│  │                                │     │
│  │  • server-parent               │     │
│  │  • reasoner-parent             │     │
│  │  • builder-parent              │     │
│  │  • cloudext-parent             │     │
│  │                                │     │
│  │  Port: 8080 (REST API)         │     │
│  └────────────────────────────────┘     │
│              │                           │
│              ↓                           │
│  ┌───────────┴───────────┐              │
│  ↓                       ↓              │
│ ┌──────────────┐   ┌──────────────┐    │
│ │   MySQL      │   │    Neo4j     │    │
│ │   5.7+       │   │    4.4+      │    │
│ │              │   │              │    │
│ │ Port: 3306   │   │ Port: 7687   │    │
│ └──────────────┘   └──────────────┘    │
│                                         │
└──────────────────────────────────────────┘

Resource Requirements:
  • CPU: 4+ cores
  • RAM: 8GB+ (4GB for OpenSPG, 2GB for Neo4j, 2GB for MySQL)
  • Disk: 50GB+ SSD
  • Java: JDK 1.8+
```

### 9.2 Production Distributed Deployment

```
┌────────────────────────────────────────────────────────────┐
│                  Production Environment                     │
└────────────────────────────────────────────────────────────┘

                    Internet
                       │
                       ↓
            ┌─────────────────┐
            │  Load Balancer  │
            │   (HAProxy/     │
            │    Nginx)       │
            └────────┬────────┘
                     │
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Server-1 │  │ Server-2 │  │ Server-N │
│          │  │          │  │          │
│ OpenSPG  │  │ OpenSPG  │  │ OpenSPG  │
│ API      │  │ API      │  │ API      │
│ Layer    │  │ Layer    │  │ Layer    │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     └─────────────┼─────────────┘
                   │
       ┌───────────┼───────────┬─────────────┐
       ↓           ↓           ↓             ↓
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Reasoner │ │ Builder  │ │ MySQL    │ │  Redis   │
│ Cluster  │ │ Cluster  │ │ Cluster  │ │  Cluster │
│          │ │          │ │          │ │          │
│ (3 nodes)│ │ (2 nodes)│ │(Master + │ │(Master + │
│          │ │          │ │ Replicas)│ │Replicas) │
└────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │            │
     └────────────┼────────────┴────────────┘
                  ↓
      ┌───────────────────────┐
      │ Neo4j Causal Cluster  │
      │                       │
      │  • 3 Core servers     │
      │  • 2 Read replicas    │
      │  • Distributed writes │
      │  • Scalable reads     │
      └───────────────────────┘
```

### 9.3 Cloud-Native Kubernetes Deployment

```
┌────────────────────────────────────────────────────────────┐
│              Kubernetes Cluster                             │
└────────────────────────────────────────────────────────────┘

        ┌─────────────────────────────┐
        │      Ingress Controller     │
        │    (NGINX/Traefik/Istio)    │
        └─────────────┬───────────────┘
                      │
                      ↓
        ┌─────────────────────────────┐
        │  OpenSPG API Service        │
        │  (LoadBalancer/ClusterIP)   │
        └─────────────┬───────────────┘
                      │
        ┌─────────────┴─────────────┐
        ↓                           ↓
┌────────────────┐          ┌────────────────┐
│  API Pods      │          │  API Pods      │
│  ┌──────────┐  │          │  ┌──────────┐  │
│  │ OpenSPG  │  │          │  │ OpenSPG  │  │
│  │ Server   │  │          │  │ Server   │  │
│  └──────────┘  │          │  └──────────┘  │
│  Replicas: 3+  │          │  Replicas: 3+  │
└────────┬───────┘          └────────┬───────┘
         │                           │
         └───────────┬───────────────┘
                     │
         ┌───────────┼───────────┬────────────┐
         ↓           ↓           ↓            ↓
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Reasoner     │ │ Builder  │ │ MySQL    │ │  Redis   │
│ StatefulSet  │ │ Jobs     │ │ StatefulS│ │ StatefulS│
│              │ │          │ │ et       │ │ et       │
│ Pods: 3      │ │(On-demand│ │          │ │          │
│              │ │ scaling) │ │ Pods: 3  │ │ Pods: 3  │
└──────┬───────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
       │              │            │            │
       └──────────────┼────────────┴────────────┘
                      ↓
            ┌──────────────────┐
            │ Neo4j Operator   │
            │ (StatefulSet)    │
            │                  │
            │ • Core: 3 pods   │
            │ • Read: 2 pods   │
            │ • PVC per pod    │
            └──────────────────┘

Kubernetes Resources:
  • Deployments: API layer (horizontal autoscaling)
  • StatefulSets: Databases (persistent storage)
  • Jobs: Builder pipelines (batch processing)
  • Services: Internal service discovery
  • Ingress: External access routing
  • ConfigMaps: Application configuration
  • Secrets: Credentials management
  • PersistentVolumes: Database storage
```

---

## 10. Component Interaction Sequence Diagrams

### 10.1 Knowledge Construction Sequence

```
User        API         Builder       Reasoner      Schema      Cloudext    Neo4j
 │           │            │              │            │            │          │
 │ Upload    │            │              │            │            │          │
 │ CSV File  │            │              │            │            │          │
 ├──────────>│            │              │            │            │          │
 │           │ Create     │              │            │            │          │
 │           │ Pipeline   │              │            │            │          │
 │           ├───────────>│              │            │            │          │
 │           │            │ Validate     │            │            │          │
 │           │            │ Schema       │            │            │          │
 │           │            ├─────────────────────────>│            │          │
 │           │            │              │            │ Schema OK  │          │
 │           │            │<──────────────────────────┤            │          │
 │           │            │              │            │            │          │
 │           │            │ Load Data    │            │            │          │
 │           │            │ (StringSrc)  │            │            │          │
 │           │            ├──────────────┤            │            │          │
 │           │            │              │            │            │          │
 │           │            │ Extract      │            │            │          │
 │           │            │ (LLM)        │            │            │          │
 │           │            ├──────────────┤            │            │          │
 │           │            │              │            │            │          │
 │           │            │ Type Mapping │            │            │          │
 │           │            ├──────────────┤            │            │          │
 │           │            │              │            │            │          │
 │           │            │ Reasoning    │            │            │          │
 │           │            ├─────────────>│            │            │          │
 │           │            │              │ Infer      │            │          │
 │           │            │              │ Concepts   │            │          │
 │           │            │              ├────────┐   │            │          │
 │           │            │              │        │   │            │          │
 │           │            │              │<───────┘   │            │          │
 │           │            │ Enriched     │            │            │          │
 │           │            │ Knowledge    │            │            │          │
 │           │            │<─────────────┤            │            │          │
 │           │            │              │            │            │          │
 │           │            │ Store Graph  │            │            │          │
 │           │            ├────────────────────────────────────────>│          │
 │           │            │              │            │            │ Write    │
 │           │            │              │            │            ├─────────>│
 │           │            │              │            │            │          │
 │           │            │              │            │            │ OK       │
 │           │            │              │            │            │<─────────┤
 │           │            │ Success      │            │            │          │
 │           │            │<─────────────────────────────────────────┤          │
 │           │ Pipeline   │              │            │            │          │
 │           │ Complete   │              │            │            │          │
 │ <─────────┤            │              │            │            │          │
 │           │            │              │            │            │          │
 │  Result:  │            │              │            │            │          │
 │  200 OK   │            │              │            │            │          │
```

### 10.2 Query Execution Sequence

```
User        API       Reasoner    KGDSL     Logical    Physical   Warehouse  Neo4j
 │           │           │        Parser     Planner    Planner      │        │
 │           │           │          │          │          │          │        │
 │ KGDSL     │           │          │          │          │          │        │
 │ Query     │           │          │          │          │          │        │
 ├──────────>│           │          │          │          │          │        │
 │           │ Execute   │          │          │          │          │        │
 │           ├──────────>│          │          │          │          │        │
 │           │           │ Parse    │          │          │          │        │
 │           │           ├─────────>│          │          │          │        │
 │           │           │          │ AST      │          │          │        │
 │           │           │          ├─────────>│          │          │        │
 │           │           │          │          │ Optimize │          │        │
 │           │           │          │          ├─────────>│          │        │
 │           │           │          │          │          │ Generate │        │
 │           │           │          │          │          │ Physical │        │
 │           │           │          │          │          │ Plan     │        │
 │           │           │          │          │          ├────┐     │        │
 │           │           │          │          │          │    │     │        │
 │           │           │          │          │          │<───┘     │        │
 │           │           │          │          │          │          │        │
 │           │           │ Execute  │          │          │          │        │
 │           │           │ Physical │          │          │          │        │
 │           │           │ Plan     │          │          │          │        │
 │           │           │<─────────────────────────────────┤          │        │
 │           │           │          │          │          │          │        │
 │           │           │ Fetch    │          │          │          │        │
 │           │           │ Data     │          │          │          │        │
 │           │           ├──────────────────────────────────────────>│        │
 │           │           │          │          │          │          │ Cypher │
 │           │           │          │          │          │          ├───────>│
 │           │           │          │          │          │          │        │
 │           │           │          │          │          │          │ Results│
 │           │           │          │          │          │          │<───────┤
 │           │           │ Raw      │          │          │          │        │
 │           │           │ Results  │          │          │          │        │
 │           │           │<─────────────────────────────────────────────┤        │
 │           │           │          │          │          │          │        │
 │           │           │ Process  │          │          │          │        │
 │           │           │ & Format │          │          │          │        │
 │           │           ├────┐     │          │          │          │        │
 │           │           │    │     │          │          │          │        │
 │           │           │<───┘     │          │          │          │        │
 │           │ Final     │          │          │          │          │        │
 │           │ Results   │          │          │          │          │        │
 │           │<──────────┤          │          │          │          │        │
 │  JSON     │           │          │          │          │          │        │
 │  Response │           │          │          │          │          │        │
 │<──────────┤           │          │          │          │          │        │
```

---

## Summary

This document provides comprehensive visual representations of OpenSPG's architecture, including:

1. **High-level system architecture** with five-layer design
2. **Module internal structures** showing component organization
3. **Query processing pipelines** from KGDSL to execution
4. **Knowledge construction flows** from raw data to graph storage
5. **Cloudext abstraction** demonstrating pluggable architecture
6. **Technology stack layers** with version information
7. **Deployment architectures** for various environments
8. **Sequence diagrams** showing component interactions

These diagrams complement the detailed architecture analysis document and provide visual aids for understanding OpenSPG's sophisticated design.

---

**Document Status:** COMPLETE
**Diagrams:** 10 major visualizations
**Coverage:** All core architectural components
