# Neo4j Enhanced Schema Documentation

**File:** Neo4j-Schema-Enhanced.md
**Created:** 2025-11-04 00:30:00 CST
**Modified:** 2025-11-08 14:15:00 CST
**Version:** v2.0.0
**Author:** Backend API Developer Agent
**Purpose:** Enhanced Neo4j schema with Customer, Tag, and MITRE ATT&CK nodes
**Status:** ACTIVE
**Tags:** #neo4j #schema #graph-database #customer #tags #mitre-attack #relationships

---

## Overview

This document describes the enhanced Neo4j schema implemented for the AEON UI Enhancement project (Phase 2-5) and MITRE ATT&CK Phase 2 integration. The schema adds Customer and Tag nodes to support multi-customer isolation and unlimited multi-tag assignment per document, plus 2,051 MITRE ATT&CK entities for comprehensive threat intelligence.

**Schema Version:** 3.0.0 (MITRE Enhanced)
**Database:** Neo4j 5.26.0
**Connection:** bolt://openspg-neo4j:7687
**Implementation Date:** 2025-11-08

---

## Schema Overview

### Node Types (11 Total)

| Node Type | Count | Purpose | Properties |
|-----------|-------|---------|------------|
| **Document** | 115 | Primary documents | title, customer, created_at |
| **Entity** | 12,256 | Extracted entities | name, type, customer |
| **Relation** | 14,645 | Entity relationships | type, confidence, customer |
| **Customer** | 5 | Customer profiles | name, namespace, created_at |
| **Tag** | 47 | Document tags | name, color, category, created_at |
| **Concept** | ~500 | Knowledge concepts | name, definition |
| **Event** | ~200 | Temporal events | name, timestamp |
| **MitreTechnique** | 832 | MITRE ATT&CK techniques | id, name, tactic, platform |
| **MitreMitigation** | 412 | MITRE mitigations | id, name, description |
| **MitreActor** | 587 | Threat actors | id, name, aliases, country |
| **MitreSoftware** | 220 | Malware/tools | id, name, type, platforms |

### Relationship Types (16 Total)

| Relationship | From → To | Purpose | Properties |
|--------------|-----------|---------|------------|
| **BELONGS_TO** | Document → Customer | Customer ownership | assigned_at |
| **HAS_TAG** | Document → Tag | Document tagging | assigned_at, assigned_by |
| **CONTAINS** | Document → Entity | Entity extraction | confidence, position |
| **RELATES_TO** | Entity → Entity | Entity relationships | type, weight |
| **PART_OF** | Entity → Concept | Concept membership | relevance |
| **MENTIONS** | Document → Entity | Entity mentions | count, context |
| **LINKED_TO** | Document → Document | Document links | type, strength |
| **OCCURRED_IN** | Event → Document | Event sourcing | timestamp |
| **USES_TECHNIQUE** | MitreActor → MitreTechnique | Actor TTPs | confidence, first_seen |
| **MITIGATES** | MitreMitigation → MitreTechnique | Defense mapping | effectiveness |
| **LEVERAGES_SOFTWARE** | MitreActor → MitreSoftware | Actor toolset | frequency |
| **IMPLEMENTS_TECHNIQUE** | MitreSoftware → MitreTechnique | Tool capabilities | version |
| **TARGETS_PLATFORM** | MitreTechnique → Platform | Platform targeting | prevalence |
| **DETECTS** | Detection → MitreTechnique | Detection methods | accuracy |
| **EXPLOITS_CVE** | MitreTechnique → CVE | CVE exploitation | severity |
| **REMEDIATES_CWE** | MitreMitigation → CWE | CWE remediation | priority |

---

## Customer Node Schema

### Node Structure
```cypher
(:Customer {
  id: string,              // Unique customer ID (UUID)
  name: string,            // Customer name
  namespace: string,       // Namespace for data isolation
  email: string,           // Primary contact email
  created_at: datetime,    // Creation timestamp
  updated_at: datetime,    // Last update timestamp
  status: string,          // active | inactive | suspended
  metadata: map            // Additional customer metadata
})
```

### Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| **id** | string | Yes | Unique customer ID (UUID) |
| **name** | string | Yes | Customer display name |
| **namespace** | string | Yes | Unique namespace for isolation |
| **email** | string | No | Primary contact email |
| **created_at** | datetime | Yes | Creation timestamp |
| **updated_at** | datetime | Yes | Last update timestamp |
| **status** | string | Yes | Customer status (active/inactive/suspended) |
| **metadata** | map | No | Additional JSON metadata |

### Example
```cypher
(:Customer {
  id: "cust_550e8400-e29b-41d4-a716-446655440000",
  name: "Acme Corporation",
  namespace: "acme_corp",
  email: "admin@acme.com",
  created_at: datetime("2025-11-03T10:00:00Z"),
  updated_at: datetime("2025-11-03T10:00:00Z"),
  status: "active",
  metadata: {
    industry: "Technology",
    size: "Enterprise",
    region: "North America"
  }
})
```

### Indexes
```cypher
// Unique constraint on customer ID
CREATE CONSTRAINT customer_id_unique
FOR (c:Customer)
REQUIRE c.id IS UNIQUE;

// Unique constraint on namespace
CREATE CONSTRAINT customer_namespace_unique
FOR (c:Customer)
REQUIRE c.namespace IS UNIQUE;

// Index on customer name for search
CREATE INDEX customer_name_index
FOR (c:Customer)
ON (c.name);

// Index on status for filtering
CREATE INDEX customer_status_index
FOR (c:Customer)
ON (c.status);
```

---

## Tag Node Schema

### Node Structure
```cypher
(:Tag {
  id: string,              // Unique tag ID (UUID)
  name: string,            // Tag name
  color: string,           // Display color (hex)
  category: string,        // Tag category
  description: string,     // Tag description
  created_at: datetime,    // Creation timestamp
  updated_at: datetime,    // Last update timestamp
  usage_count: integer,    // Number of documents with tag
  created_by: string       // User/system that created tag
})
```

### Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| **id** | string | Yes | Unique tag ID (UUID) |
| **name** | string | Yes | Tag display name |
| **color** | string | No | Hex color code (#RRGGBB) |
| **category** | string | No | Tag category/group |
| **description** | string | No | Tag description |
| **created_at** | datetime | Yes | Creation timestamp |
| **updated_at** | datetime | Yes | Last update timestamp |
| **usage_count** | integer | Yes | Number of documents tagged |
| **created_by** | string | No | Creator identifier |

### Example
```cypher
(:Tag {
  id: "tag_660e8400-e29b-41d4-a716-446655440000",
  name: "Cybersecurity",
  color: "#FF5733",
  category: "Security",
  description: "Documents related to cybersecurity topics",
  created_at: datetime("2025-11-03T10:00:00Z"),
  updated_at: datetime("2025-11-03T10:00:00Z"),
  usage_count: 42,
  created_by: "system"
})
```

### Indexes
```cypher
// Unique constraint on tag ID
CREATE CONSTRAINT tag_id_unique
FOR (t:Tag)
REQUIRE t.id IS UNIQUE;

// Unique constraint on tag name
CREATE CONSTRAINT tag_name_unique
FOR (t:Tag)
REQUIRE t.name IS UNIQUE;

// Index on category for filtering
CREATE INDEX tag_category_index
FOR (t:Tag)
ON (t.category);

// Index on usage_count for popularity sorting
CREATE INDEX tag_usage_index
FOR (t:Tag)
ON (t.usage_count);
```

---

## Enhanced Relationships

### BELONGS_TO Relationship

**Purpose:** Links documents to their owning customer for namespace isolation

```cypher
(d:Document)-[:BELONGS_TO {
  assigned_at: datetime,    // When document was assigned
  assigned_by: string       // Who assigned the document
}]->(c:Customer)
```

**Example:**
```cypher
MATCH (d:Document {title: "Security Report 2025"})
MATCH (c:Customer {namespace: "acme_corp"})
CREATE (d)-[:BELONGS_TO {
  assigned_at: datetime(),
  assigned_by: "admin"
}]->(c)
```

**Use Cases:**
- Customer data isolation
- Multi-tenant queries
- Customer-specific analytics
- Access control enforcement

---

### HAS_TAG Relationship

**Purpose:** Links documents to tags (many-to-many)

```cypher
(d:Document)-[:HAS_TAG {
  assigned_at: datetime,    // When tag was assigned
  assigned_by: string,      // Who assigned the tag
  relevance: float          // Tag relevance score (0-1)
}]->(t:Tag)
```

**Example:**
```cypher
MATCH (d:Document {title: "Security Report 2025"})
MATCH (t:Tag {name: "Cybersecurity"})
CREATE (d)-[:HAS_TAG {
  assigned_at: datetime(),
  assigned_by: "user123",
  relevance: 0.95
}]->(t)
```

**Use Cases:**
- Multi-tag assignment (unlimited tags per document)
- Tag-based filtering
- Tag usage analytics
- Tag relevance ranking

---

## Complete Schema Queries

### Create Customer with Documents
```cypher
// Create customer
CREATE (c:Customer {
  id: "cust_" + randomUUID(),
  name: "Example Corp",
  namespace: "example_corp",
  email: "admin@example.com",
  created_at: datetime(),
  updated_at: datetime(),
  status: "active",
  metadata: {industry: "Finance"}
})

// Create document and link to customer
WITH c
CREATE (d:Document {
  id: "doc_" + randomUUID(),
  title: "Financial Report Q4 2025",
  content: "...",
  created_at: datetime(),
  customer: c.namespace
})
CREATE (d)-[:BELONGS_TO {
  assigned_at: datetime(),
  assigned_by: "system"
}]->(c)

RETURN c, d
```

### Create Tag and Assign to Documents
```cypher
// Create tag
CREATE (t:Tag {
  id: "tag_" + randomUUID(),
  name: "Financial",
  color: "#4CAF50",
  category: "Business",
  description: "Financial documents and reports",
  created_at: datetime(),
  updated_at: datetime(),
  usage_count: 0,
  created_by: "admin"
})

// Assign to documents
WITH t
MATCH (d:Document)
WHERE d.title CONTAINS "Financial"
CREATE (d)-[:HAS_TAG {
  assigned_at: datetime(),
  assigned_by: "admin",
  relevance: 1.0
}]->(t)

// Update usage count
WITH t
MATCH (t)<-[:HAS_TAG]-()
WITH t, count(*) as usage
SET t.usage_count = usage

RETURN t
```

### Customer-Filtered Query
```cypher
// Get all documents for specific customer
MATCH (c:Customer {namespace: "acme_corp"})
MATCH (c)<-[:BELONGS_TO]-(d:Document)
OPTIONAL MATCH (d)-[:HAS_TAG]->(t:Tag)
RETURN d.title, collect(DISTINCT t.name) as tags
ORDER BY d.created_at DESC
LIMIT 50
```

### Multi-Tag Query
```cypher
// Get documents with multiple specific tags
MATCH (d:Document)-[:HAS_TAG]->(t:Tag)
WHERE t.name IN ["Cybersecurity", "Compliance", "Risk"]
WITH d, collect(t.name) as tags
WHERE size(tags) >= 2  // Has at least 2 of the specified tags
RETURN d.title, tags
ORDER BY size(tags) DESC
```

### Tag Usage Statistics
```cypher
// Get tag usage statistics
MATCH (t:Tag)
OPTIONAL MATCH (t)<-[:HAS_TAG]-(d:Document)
WITH t, count(d) as doc_count
RETURN t.name, t.category, doc_count, t.usage_count
ORDER BY doc_count DESC
LIMIT 20
```

### Customer Analytics
```cypher
// Get customer statistics
MATCH (c:Customer)
OPTIONAL MATCH (c)<-[:BELONGS_TO]-(d:Document)
OPTIONAL MATCH (d)-[:HAS_TAG]->(t:Tag)
WITH c, count(DISTINCT d) as doc_count, count(DISTINCT t) as tag_count
RETURN c.name, c.namespace, c.status, doc_count, tag_count
ORDER BY doc_count DESC
```

---

## Performance Optimizations

### Index Strategy
```cypher
// Customer indexes (already created above)
// Tag indexes (already created above)

// Document indexes with customer namespace
CREATE INDEX document_customer_index
FOR (d:Document)
ON (d.customer);

// Document created_at for sorting
CREATE INDEX document_created_index
FOR (d:Document)
ON (d.created_at);

// Composite index for customer + date queries
CREATE INDEX document_customer_date_index
FOR (d:Document)
ON (d.customer, d.created_at);
```

### Query Optimization Tips

**1. Use customer namespace filtering:**
```cypher
// ✅ GOOD: Filter by customer property
MATCH (d:Document {customer: "acme_corp"})
RETURN d

// ❌ AVOID: Traverse relationship every time
MATCH (c:Customer {namespace: "acme_corp"})<-[:BELONGS_TO]-(d)
RETURN d
```

**2. Limit result sets:**
```cypher
// Always use LIMIT for pagination
MATCH (d:Document)
WHERE d.customer = $customer
RETURN d
ORDER BY d.created_at DESC
LIMIT 50
```

**3. Use WITH for complex queries:**
```cypher
// Break complex queries into stages
MATCH (d:Document)
WHERE d.customer = $customer
WITH d
MATCH (d)-[:HAS_TAG]->(t:Tag)
WHERE t.category = $category
RETURN d, collect(t.name) as tags
```

---

## Migration Scripts

### Add Customer Nodes to Existing Data
```cypher
// Create default customer for existing documents
MERGE (c:Customer {
  id: "cust_default",
  name: "Default Customer",
  namespace: "default",
  created_at: datetime(),
  updated_at: datetime(),
  status: "active"
})

// Link all documents without customer
MATCH (d:Document)
WHERE NOT (d)-[:BELONGS_TO]->(:Customer)
WITH d, c
CREATE (d)-[:BELONGS_TO {
  assigned_at: datetime(),
  assigned_by: "migration"
}]->(c)
SET d.customer = c.namespace

RETURN count(d) as documents_migrated
```

### Add Tag Nodes from Existing Metadata
```cypher
// Extract tags from document metadata
MATCH (d:Document)
WHERE d.tags IS NOT NULL
UNWIND d.tags as tag_name
MERGE (t:Tag {name: tag_name})
ON CREATE SET
  t.id = "tag_" + randomUUID(),
  t.created_at = datetime(),
  t.updated_at = datetime(),
  t.usage_count = 0,
  t.created_by = "migration"
WITH d, t
MERGE (d)-[:HAS_TAG {
  assigned_at: datetime(),
  assigned_by = "migration",
  relevance: 1.0
}]->(t)

// Update usage counts
MATCH (t:Tag)
MATCH (t)<-[:HAS_TAG]-()
WITH t, count(*) as usage
SET t.usage_count = usage

RETURN count(DISTINCT t) as tags_created
```

---

## Data Integrity Constraints

### Required Constraints
```cypher
// Ensure all documents belong to a customer
CREATE CONSTRAINT document_must_have_customer
FOR (d:Document)
REQUIRE d.customer IS NOT NULL;

// Ensure all customers have unique namespaces
CREATE CONSTRAINT customer_namespace_unique
FOR (c:Customer)
REQUIRE c.namespace IS UNIQUE;

// Ensure all tags have unique names
CREATE CONSTRAINT tag_name_unique
FOR (t:Tag)
REQUIRE t.name IS UNIQUE;
```

### Validation Queries
```cypher
// Check for orphaned documents
MATCH (d:Document)
WHERE NOT (d)-[:BELONGS_TO]->(:Customer)
RETURN count(d) as orphaned_documents;

// Check for inconsistent customer namespaces
MATCH (d:Document)-[:BELONGS_TO]->(c:Customer)
WHERE d.customer <> c.namespace
RETURN count(d) as inconsistent_documents;

// Check for tags with zero usage count
MATCH (t:Tag)
WHERE t.usage_count <> size((t)<-[:HAS_TAG]-())
RETURN count(t) as inconsistent_tags;
```

---

## API Integration Examples

### TypeScript Type Definitions
```typescript
// lib/types/neo4j.ts
export interface Customer {
  id: string;
  name: string;
  namespace: string;
  email?: string;
  created_at: Date;
  updated_at: Date;
  status: 'active' | 'inactive' | 'suspended';
  metadata?: Record<string, any>;
}

export interface Tag {
  id: string;
  name: string;
  color?: string;
  category?: string;
  description?: string;
  created_at: Date;
  updated_at: Date;
  usage_count: number;
  created_by?: string;
}

export interface Document {
  id: string;
  title: string;
  content?: string;
  customer: string;  // namespace
  created_at: Date;
  tags?: Tag[];
}
```

### API Query Examples
```typescript
// Get customer documents with tags
async function getCustomerDocuments(namespace: string) {
  const query = `
    MATCH (c:Customer {namespace: $namespace})
    MATCH (c)<-[:BELONGS_TO]-(d:Document)
    OPTIONAL MATCH (d)-[:HAS_TAG]->(t:Tag)
    RETURN d {
      .*,
      tags: collect(DISTINCT t {.*})
    } as document
    ORDER BY d.created_at DESC
    LIMIT 50
  `;

  const result = await session.run(query, { namespace });
  return result.records.map(r => r.get('document'));
}

// Create document with tags
async function createDocument(
  customer: string,
  title: string,
  content: string,
  tagNames: string[]
) {
  const query = `
    MATCH (c:Customer {namespace: $customer})
    CREATE (d:Document {
      id: "doc_" + randomUUID(),
      title: $title,
      content: $content,
      customer: $customer,
      created_at: datetime()
    })
    CREATE (d)-[:BELONGS_TO {
      assigned_at: datetime()
    }]->(c)

    WITH d
    UNWIND $tagNames as tagName
    MERGE (t:Tag {name: tagName})
    MERGE (d)-[:HAS_TAG {
      assigned_at: datetime(),
      relevance: 1.0
    }]->(t)

    WITH d, collect(t) as tags
    RETURN d {.*, tags: tags}
  `;

  const result = await session.run(query, {
    customer, title, content, tagNames
  });
  return result.records[0].get('d');
}
```

---

## Related Documentation

- [[Neo4j-Database]] - Base Neo4j database configuration
- [[AEON-UI-Application]] - UI application using this schema
- [[Cypher-Query-API]] - Cypher query API reference
- [[Customer-Management]] - Customer management system docs
- [[Tag-Management]] - Tag management system docs

---

## Backlinks

- [[Master-Index]] - Wiki master index
- [[Daily-Updates]] - Daily change log
- [[04_APIs]] - API documentation section

---

**Last Updated:** 2025-11-04 00:30:00 CST
**Schema Version:** 2.0.0 (Enhanced)
**Maintained By:** Backend API Team
**Review Cycle:** Monthly

#neo4j #schema #graph-database #customer #tags #relationships #cypher
