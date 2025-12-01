# Entity Resolution Architecture
**File:** entity_resolution_architecture.md
**Created:** 2025-10-29 15:30:00 UTC
**Modified:** 2025-10-29 15:30:00 UTC
**Version:** v1.0.0
**Author:** System Architecture Designer
**Purpose:** Enhanced entity resolution schema with forward compatibility for CVEs not yet in API database
**Status:** ACTIVE

## Executive Summary

This architecture enhances the existing entity resolution system to support forward compatibility for CVEs and other security entities that may be mentioned in documents before they appear in the official API databases (NVD, CWE, CAPEC). The design introduces resolution status tracking, unresolved entity management, and batch enrichment processes while maintaining backward compatibility with the existing schema.

**Key Enhancements:**
- Entity resolution status tracking (resolved, unresolved, pending)
- Unresolved entity queue for future enrichment
- Dual relationship model: RESOLVES_TO (Entity→CVE) and MENTIONS_CVE (Document→CVE)
- Batch enrichment process for retroactive resolution
- Future-proof schema supporting emerging vulnerabilities

---

## Current System State

### Existing Architecture
The current `entity_resolver.py` implements:
- Entity extraction from documents creates `Entity` nodes with labels (CVE, CWE, CAPEC)
- Resolution attempts to match entities to API-imported nodes (CVE, CWE, CAPEC)
- Creates `RESOLVES_TO` relationships on successful match
- Creates direct `MENTIONS_CVE/CWE/CAPEC` relationships for query optimization
- Logs unresolved entities but doesn't track them systematically

### Current Limitations
1. **No persistence of unresolved entities** - Warning logs only, no queryable data
2. **No forward compatibility** - Documents mentioning future CVEs have no linkage
3. **No enrichment tracking** - Can't identify which entities need re-resolution
4. **Missing temporal context** - No timestamp tracking for resolution attempts
5. **No prioritization** - All unresolved entities treated equally

---

## Enhanced Architecture Design

### 1. Schema Enhancements

#### 1.1 Entity Node Properties
```cypher
// Enhanced Entity node schema
(:Entity {
    id: String,                    // UUID (existing)
    text: String,                  // "CVE-2024-1234" (existing)
    label: String,                 // "CVE", "CWE", "CAPEC" (existing)
    start_char: Integer,           // Character position (existing)
    end_char: Integer,             // Character position (existing)

    // NEW PROPERTIES
    resolution_status: String,     // "resolved" | "unresolved" | "pending"
    resolution_attempted_at: DateTime,  // Last resolution attempt timestamp
    resolution_retry_count: Integer,    // Number of resolution attempts
    first_seen_at: DateTime,       // First time entity was extracted
    last_seen_at: DateTime,        // Most recent extraction occurrence
    seen_count: Integer,           // Number of documents mentioning this
    priority_score: Float          // Enrichment priority (0.0-1.0)
})
```

#### 1.2 Relationship Enhancements
```cypher
// Entity -> API Node (existing, enhanced)
(:Entity)-[:RESOLVES_TO {
    created_at: DateTime,          // (existing)
    confidence: Float,             // NEW: Match confidence score
    match_method: String           // NEW: "exact" | "fuzzy" | "manual"
}]->(:CVE|:CWE|:CAPEC)

// Document -> API Node (existing)
(:Document)-[:MENTIONS_CVE {
    created_at: DateTime,          // (existing)
    mention_count: Integer,        // NEW: Number of mentions in doc
    context_snippet: String        // NEW: Surrounding text sample
}]->(:CVE)

// NEW: Entity -> Unresolved tracking
(:Entity)-[:PENDING_RESOLUTION {
    queued_at: DateTime,
    retry_after: DateTime,
    reason: String                 // "api_not_found" | "malformed_id" | "network_error"
}]->(:UnresolvedEntity)
```

#### 1.3 New Node Type: UnresolvedEntity
```cypher
// Queue for entities needing future enrichment
(:UnresolvedEntity {
    entity_text: String,           // "CVE-2024-9999"
    entity_label: String,          // "CVE" | "CWE" | "CAPEC"
    first_seen_at: DateTime,
    last_attempt_at: DateTime,
    attempt_count: Integer,
    document_count: Integer,       // How many docs mention this
    priority_score: Float,         // Enrichment priority
    status: String,                // "queued" | "failed" | "enriched"
    next_retry_at: DateTime,
    failure_reason: String         // If applicable
})
```

---

### 2. Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     DOCUMENT INGESTION                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ENTITY EXTRACTION                           │
│  (NER/spaCy) → Create Entity nodes with metadata               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ENTITY RESOLUTION PHASE                       │
│                                                                 │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │   Try CVE    │      │   Try CWE    │      │  Try CAPEC   │ │
│  │  API Match   │      │  API Match   │      │  API Match   │ │
│  └──────┬───────┘      └──────┬───────┘      └──────┬───────┘ │
│         │                     │                     │          │
│    ┌────▼─────┐          ┌───▼─────┐          ┌───▼─────┐    │
│    │ Found?   │          │ Found?  │          │ Found?  │    │
│    └────┬─────┘          └───┬─────┘          └───┬─────┘    │
│         │                    │                     │          │
│    Yes  │  No           Yes  │  No            Yes  │  No      │
│         │                    │                     │          │
└─────────┼────────────────────┼─────────────────────┼──────────┘
          │                    │                     │
          ▼                    ▼                     ▼
┌─────────────────┐   ┌─────────────────┐   ┌──────────────────┐
│   RESOLVED      │   │   RESOLVED      │   │   RESOLVED       │
│                 │   │                 │   │                  │
│ Entity          │   │ Entity          │   │ Entity           │
│  └─RESOLVES_TO→ │   │  └─RESOLVES_TO→ │   │  └─RESOLVES_TO→  │
│      CVE        │   │      CWE        │   │      CAPEC       │
│                 │   │                 │   │                  │
│ Document        │   │ Document        │   │ Document         │
│  └─MENTIONS_CVE→│   │  └─MENTIONS_CWE→│   │  └─MENTIONS_CAPEC│
│      CVE        │   │      CWE        │   │      CAPEC       │
│                 │   │                 │   │                  │
│ resolution_     │   │ resolution_     │   │ resolution_      │
│ status:         │   │ status:         │   │ status:          │
│ "resolved"      │   │ "resolved"      │   │ "resolved"       │
└─────────────────┘   └─────────────────┘   └──────────────────┘
          │                    │                     │
          │                    ▼                     │
          │           ┌─────────────────┐            │
          │           │   UNRESOLVED    │            │
          │           │                 │            │
          │           │ Entity          │            │
          │           │  resolution_    │            │
          │           │  status:        │            │
          │           │  "unresolved"   │            │
          │           │                 │            │
          │           │ Create          │            │
          │           │ UnresolvedEntity│            │
          │           │ node for queue  │            │
          │           └────────┬────────┘            │
          │                    │                     │
          │                    ▼                     │
          │           ┌─────────────────┐            │
          │           │ PENDING_RESOLUTION           │
          │           │ relationship    │            │
          │           └────────┬────────┘            │
          │                    │                     │
          └────────────────────┴─────────────────────┘
                               │
                               ▼
              ┌────────────────────────────────────┐
              │   ENRICHMENT BATCH PROCESSOR       │
              │   (Scheduled/On-Demand)            │
              │                                    │
              │   1. Query UnresolvedEntity queue  │
              │   2. Retry API resolution          │
              │   3. Update resolution_status      │
              │   4. Create RESOLVES_TO if found   │
              │   5. Update priority scores        │
              └────────────────────────────────────┘
```

---

### 3. Resolution Status State Machine

```
                  ┌──────────────┐
                  │   PENDING    │
                  │  (Initial)   │
                  └──────┬───────┘
                         │
                    Extract Entity
                         │
                         ▼
              ┌──────────────────────┐
              │   Attempt Resolution │
              └──────────┬───────────┘
                         │
          ┌──────────────┴──────────────┐
          │                             │
     API Match                      No Match
          │                             │
          ▼                             ▼
   ┌─────────────┐            ┌──────────────┐
   │  RESOLVED   │            │  UNRESOLVED  │
   │             │            │              │
   │ Create      │            │ Create       │
   │ RESOLVES_TO │            │ Unresolved   │
   │ relationship│            │ Entity node  │
   └─────────────┘            └──────┬───────┘
                                     │
                            Queue for Enrichment
                                     │
                                     ▼
                         ┌────────────────────┐
                         │ Enrichment Process │
                         │  (Batch/Scheduled) │
                         └─────────┬──────────┘
                                   │
                        ┌──────────┴──────────┐
                        │                     │
                   API Found             Still Missing
                        │                     │
                        ▼                     ▼
                 ┌─────────────┐      ┌──────────────┐
                 │  RESOLVED   │      │  UNRESOLVED  │
                 │  (Updated)  │      │  (Retry++)   │
                 └─────────────┘      └──────────────┘
```

---

### 4. Cypher Query Examples

#### 4.1 Enhanced Entity Resolution (CVE)
```cypher
// Enhanced CVE entity resolution with status tracking
MATCH (d:Document {id: $doc_id})-[:CONTAINS_ENTITY]->(e:Entity {label: 'CVE'})

// Set initial status if not present
SET e.resolution_status = COALESCE(e.resolution_status, 'pending'),
    e.first_seen_at = COALESCE(e.first_seen_at, datetime()),
    e.resolution_retry_count = COALESCE(e.resolution_retry_count, 0),
    e.seen_count = COALESCE(e.seen_count, 0) + 1,
    e.last_seen_at = datetime()

// Try to match with API CVE node
OPTIONAL MATCH (c:CVE)
WHERE c.cve_id = e.text
   OR c.cveId = e.text
   OR c.id = 'cve-' + e.text

// Handle resolved entities
FOREACH (ignored IN CASE WHEN c IS NOT NULL THEN [1] ELSE [] END |
    MERGE (e)-[r:RESOLVES_TO]->(c)
    ON CREATE SET
        r.created_at = datetime(),
        r.confidence = 1.0,
        r.match_method = 'exact'
    SET e.resolution_status = 'resolved',
        e.resolution_attempted_at = datetime()
)

// Handle unresolved entities
FOREACH (ignored IN CASE WHEN c IS NULL THEN [1] ELSE [] END |
    // Create or update UnresolvedEntity tracking node
    MERGE (ue:UnresolvedEntity {entity_text: e.text, entity_label: 'CVE'})
    ON CREATE SET
        ue.first_seen_at = datetime(),
        ue.attempt_count = 1,
        ue.document_count = 1,
        ue.status = 'queued',
        ue.priority_score = 0.5,
        ue.next_retry_at = datetime() + duration({hours: 24})
    ON MATCH SET
        ue.last_attempt_at = datetime(),
        ue.attempt_count = ue.attempt_count + 1,
        ue.document_count = ue.document_count + 1,
        ue.priority_score = CASE
            WHEN ue.document_count > 10 THEN 0.9
            WHEN ue.document_count > 5 THEN 0.7
            ELSE 0.5
        END

    // Link entity to unresolved tracker
    MERGE (e)-[pr:PENDING_RESOLUTION]->(ue)
    ON CREATE SET
        pr.queued_at = datetime(),
        pr.retry_after = datetime() + duration({hours: 24}),
        pr.reason = 'api_not_found'

    SET e.resolution_status = 'unresolved',
        e.resolution_attempted_at = datetime(),
        e.resolution_retry_count = e.resolution_retry_count + 1
)

RETURN
    count(DISTINCT e) as total_entities,
    count(DISTINCT c) as resolved_count,
    count(DISTINCT CASE WHEN c IS NULL THEN e END) as unresolved_count
```

#### 4.2 Create Enhanced Document Links
```cypher
// Create direct document links with metadata
MATCH (d:Document {id: $doc_id})-[:CONTAINS_ENTITY]->(e:Entity)-[:RESOLVES_TO]->(c:CVE)

// Count mentions and extract context
WITH d, c, e, count(e) as mention_count
ORDER BY e.start_char

MERGE (d)-[r:MENTIONS_CVE]->(c)
ON CREATE SET
    r.created_at = datetime(),
    r.mention_count = mention_count
ON MATCH SET
    r.mention_count = mention_count

RETURN count(DISTINCT r) as links_created
```

#### 4.3 Query Unresolved Entities
```cypher
// Get high-priority unresolved entities for enrichment
MATCH (ue:UnresolvedEntity {status: 'queued'})
WHERE ue.next_retry_at <= datetime()
  AND ue.attempt_count < 10
RETURN
    ue.entity_text as entity,
    ue.entity_label as type,
    ue.document_count as doc_count,
    ue.priority_score as priority,
    ue.attempt_count as attempts
ORDER BY ue.priority_score DESC, ue.document_count DESC
LIMIT 100
```

#### 4.4 Batch Enrichment Process
```cypher
// Batch enrichment: retry resolution for queued entities
MATCH (ue:UnresolvedEntity {status: 'queued', entity_label: 'CVE'})
WHERE ue.next_retry_at <= datetime()
  AND ue.attempt_count < 10

// Try to match with newly imported CVE nodes
OPTIONAL MATCH (c:CVE)
WHERE c.cve_id = ue.entity_text
   OR c.cveId = ue.entity_text
   OR c.id = 'cve-' + ue.entity_text

// If found, resolve all pending entities
FOREACH (ignored IN CASE WHEN c IS NOT NULL THEN [1] ELSE [] END |
    // Update UnresolvedEntity status
    SET ue.status = 'enriched',
        ue.last_attempt_at = datetime()

    // Find all entities linked to this unresolved tracker
    WITH ue, c
    MATCH (e:Entity)-[pr:PENDING_RESOLUTION]->(ue)

    // Create RESOLVES_TO relationships
    MERGE (e)-[r:RESOLVES_TO]->(c)
    ON CREATE SET
        r.created_at = datetime(),
        r.confidence = 1.0,
        r.match_method = 'batch_enrichment'

    // Update entity status
    SET e.resolution_status = 'resolved',
        e.resolution_attempted_at = datetime()

    // Remove pending relationship
    DELETE pr

    // Create document links
    WITH e, c
    MATCH (d:Document)-[:CONTAINS_ENTITY]->(e)
    MERGE (d)-[mr:MENTIONS_CVE]->(c)
    ON CREATE SET mr.created_at = datetime()
)

// If still not found, update retry timing
FOREACH (ignored IN CASE WHEN c IS NULL THEN [1] ELSE [] END |
    SET ue.last_attempt_at = datetime(),
        ue.attempt_count = ue.attempt_count + 1,
        ue.next_retry_at = datetime() + duration({
            hours: CASE
                WHEN ue.attempt_count < 3 THEN 24
                WHEN ue.attempt_count < 6 THEN 72
                ELSE 168
            END
        })
)

RETURN
    count(DISTINCT ue) as entities_processed,
    count(DISTINCT c) as newly_resolved,
    collect(ue.entity_text)[0..10] as sample_entities
```

#### 4.5 Priority Score Calculation
```cypher
// Update priority scores based on document frequency and recency
MATCH (ue:UnresolvedEntity)
OPTIONAL MATCH (e:Entity)-[:PENDING_RESOLUTION]->(ue)
OPTIONAL MATCH (d:Document)-[:CONTAINS_ENTITY]->(e)

WITH ue,
     count(DISTINCT e) as entity_count,
     count(DISTINCT d) as doc_count,
     max(e.last_seen_at) as most_recent_mention

SET ue.priority_score =
    CASE
        // High priority: mentioned in 10+ docs or very recent
        WHEN doc_count >= 10 OR duration.between(most_recent_mention, datetime()).days < 7
            THEN 0.9
        // Medium priority: mentioned in 5-9 docs
        WHEN doc_count >= 5 THEN 0.7
        // Medium-low: mentioned in 2-4 docs
        WHEN doc_count >= 2 THEN 0.5
        // Low priority: single mention
        ELSE 0.3
    END

RETURN count(ue) as entities_updated
```

---

### 5. Implementation Components

#### 5.1 Enhanced EntityResolver Methods

##### Add Status Tracking
```python
def resolve_cve_entities_with_tracking(self, doc_id: str) -> Dict[str, int]:
    """
    Enhanced CVE resolution with status tracking and unresolved entity queuing.

    Returns:
        Dict with counts of resolved, unresolved, and queued entities
    """
    with self.driver.session() as session:
        result = session.run("""
            // [Insert enhanced resolution query from 4.1]
        """, doc_id=doc_id)

        record = result.single()
        if record:
            return {
                'total': record['total_entities'],
                'resolved': record['resolved_count'],
                'unresolved': record['unresolved_count']
            }
        return {'total': 0, 'resolved': 0, 'unresolved': 0}
```

##### Batch Enrichment Method
```python
def enrich_unresolved_entities(self, batch_size: int = 100) -> Dict[str, int]:
    """
    Batch process to retry resolution for queued unresolved entities.

    Args:
        batch_size: Number of entities to process per batch

    Returns:
        Dict with enrichment statistics
    """
    logger.info("Starting batch enrichment for unresolved entities...")

    with self.driver.session() as session:
        result = session.run("""
            // [Insert batch enrichment query from 4.4]
        """, batch_size=batch_size)

        record = result.single()
        if record:
            stats = {
                'processed': record['entities_processed'],
                'newly_resolved': record['newly_resolved'],
                'sample_entities': record['sample_entities']
            }

            logger.info(
                f"Enrichment complete: {stats['processed']} processed, "
                f"{stats['newly_resolved']} newly resolved"
            )

            return stats

    return {'processed': 0, 'newly_resolved': 0, 'sample_entities': []}
```

##### Priority Score Update Method
```python
def update_priority_scores(self) -> int:
    """
    Recalculate priority scores for all unresolved entities based on frequency and recency.

    Returns:
        Number of entities updated
    """
    with self.driver.session() as session:
        result = session.run("""
            // [Insert priority calculation query from 4.5]
        """)

        record = result.single()
        updated = record['entities_updated'] if record else 0

        logger.info(f"Updated priority scores for {updated} unresolved entities")
        return updated
```

##### Query Methods for Unresolved Entities
```python
def get_unresolved_entities(
    self,
    entity_type: Optional[str] = None,
    min_priority: float = 0.0,
    limit: int = 100
) -> List[Dict]:
    """
    Get unresolved entities ordered by priority.

    Args:
        entity_type: Filter by type (CVE, CWE, CAPEC) or None for all
        min_priority: Minimum priority score (0.0-1.0)
        limit: Maximum number of results

    Returns:
        List of unresolved entity details
    """
    with self.driver.session() as session:
        query = """
            MATCH (ue:UnresolvedEntity)
            WHERE ue.priority_score >= $min_priority
              AND ue.status = 'queued'
        """

        if entity_type:
            query += " AND ue.entity_label = $entity_type"

        query += """
            RETURN
                ue.entity_text as entity,
                ue.entity_label as type,
                ue.document_count as doc_count,
                ue.priority_score as priority,
                ue.attempt_count as attempts,
                ue.next_retry_at as next_retry
            ORDER BY ue.priority_score DESC, ue.document_count DESC
            LIMIT $limit
        """

        result = session.run(
            query,
            min_priority=min_priority,
            entity_type=entity_type,
            limit=limit
        )

        return [dict(record) for record in result]
```

#### 5.2 Scheduled Enrichment Service
```python
import schedule
import time

class EnrichmentScheduler:
    """
    Scheduled service to periodically retry resolution for unresolved entities.
    """

    def __init__(self, resolver: EntityResolver):
        self.resolver = resolver

    def run_enrichment_cycle(self):
        """Execute one enrichment cycle."""
        logger.info("Starting scheduled enrichment cycle")

        # Update priority scores
        self.resolver.update_priority_scores()

        # Process high-priority entities
        stats = self.resolver.enrich_unresolved_entities(batch_size=200)

        logger.info(f"Enrichment cycle complete: {stats}")

    def start(self, interval_hours: int = 24):
        """
        Start scheduled enrichment service.

        Args:
            interval_hours: Hours between enrichment cycles
        """
        schedule.every(interval_hours).hours.do(self.run_enrichment_cycle)

        logger.info(f"Enrichment scheduler started (interval: {interval_hours}h)")

        while True:
            schedule.run_pending()
            time.sleep(3600)  # Check every hour
```

---

### 6. Migration Strategy

#### 6.1 Add New Properties to Existing Entities
```cypher
// Migrate existing entities to new schema
MATCH (e:Entity)
WHERE e.label IN ['CVE', 'CWE', 'CAPEC']

// Set default values for new properties
SET e.resolution_status = CASE
        WHEN (e)-[:RESOLVES_TO]->() THEN 'resolved'
        ELSE 'unresolved'
    END,
    e.first_seen_at = COALESCE(e.first_seen_at, datetime()),
    e.last_seen_at = COALESCE(e.last_seen_at, datetime()),
    e.seen_count = COALESCE(e.seen_count, 1),
    e.resolution_retry_count = COALESCE(e.resolution_retry_count, 0)

RETURN count(e) as entities_migrated
```

#### 6.2 Create UnresolvedEntity Nodes for Existing Unresolved
```cypher
// Create UnresolvedEntity nodes for entities without RESOLVES_TO
MATCH (e:Entity)
WHERE e.label IN ['CVE', 'CWE', 'CAPEC']
  AND NOT (e)-[:RESOLVES_TO]->()

// Group by entity text to avoid duplicates
WITH e.text as entity_text, e.label as entity_label, collect(e) as entities

// Create UnresolvedEntity tracking node
CREATE (ue:UnresolvedEntity {
    entity_text: entity_text,
    entity_label: entity_label,
    first_seen_at: datetime(),
    last_attempt_at: datetime(),
    attempt_count: 1,
    document_count: size(entities),
    priority_score: CASE
        WHEN size(entities) > 10 THEN 0.9
        WHEN size(entities) > 5 THEN 0.7
        ELSE 0.5
    END,
    status: 'queued',
    next_retry_at: datetime() + duration({hours: 24})
})

// Link all entities to this tracker
WITH ue, entities
UNWIND entities as e
CREATE (e)-[:PENDING_RESOLUTION {
    queued_at: datetime(),
    retry_after: datetime() + duration({hours: 24}),
    reason: 'legacy_migration'
}]->(ue)

RETURN count(DISTINCT ue) as unresolved_entities_created
```

#### 6.3 Create Indexes for Performance
```cypher
// Indexes for efficient querying
CREATE INDEX entity_resolution_status IF NOT EXISTS
FOR (e:Entity) ON (e.resolution_status);

CREATE INDEX entity_retry_count IF NOT EXISTS
FOR (e:Entity) ON (e.resolution_retry_count);

CREATE INDEX unresolved_entity_status IF NOT EXISTS
FOR (ue:UnresolvedEntity) ON (ue.status);

CREATE INDEX unresolved_entity_priority IF NOT EXISTS
FOR (ue:UnresolvedEntity) ON (ue.priority_score);

CREATE INDEX unresolved_entity_next_retry IF NOT EXISTS
FOR (ue:UnresolvedEntity) ON (ue.next_retry_at);

CREATE CONSTRAINT unresolved_entity_unique IF NOT EXISTS
FOR (ue:UnresolvedEntity) REQUIRE (ue.entity_text, ue.entity_label) IS UNIQUE;
```

---

### 7. Query Performance Optimization

#### 7.1 Query Patterns

**Find all documents mentioning a specific CVE (resolved or unresolved):**
```cypher
// Direct path for resolved CVEs
MATCH (d:Document)-[:MENTIONS_CVE]->(c:CVE {cve_id: 'CVE-2024-1234'})
RETURN d

UNION

// Path through unresolved entities
MATCH (d:Document)-[:CONTAINS_ENTITY]->(e:Entity {text: 'CVE-2024-1234'})
WHERE e.resolution_status = 'unresolved'
RETURN d
```

**Get all unresolved CVEs mentioned in a document:**
```cypher
MATCH (d:Document {id: $doc_id})-[:CONTAINS_ENTITY]->(e:Entity {label: 'CVE'})
WHERE e.resolution_status = 'unresolved'
OPTIONAL MATCH (e)-[:PENDING_RESOLUTION]->(ue:UnresolvedEntity)
RETURN
    e.text as cve_id,
    e.seen_count as mentions,
    ue.document_count as global_doc_count,
    ue.priority_score as priority,
    ue.next_retry_at as next_enrichment_attempt
ORDER BY ue.priority_score DESC
```

**Track resolution effectiveness over time:**
```cypher
MATCH (e:Entity {label: 'CVE'})
RETURN
    e.resolution_status as status,
    count(e) as entity_count,
    avg(e.resolution_retry_count) as avg_retry_count,
    avg(e.seen_count) as avg_mentions
```

#### 7.2 Index Strategy
- **Primary indexes**: resolution_status, priority_score, next_retry_at
- **Compound indexes**: (entity_text, entity_label) for uniqueness
- **Temporal indexes**: first_seen_at, last_seen_at for time-based queries

---

### 8. Architecture Decision Records

#### ADR-001: Resolution Status Property
**Decision**: Add resolution_status property to Entity nodes
**Rationale**: Enables systematic tracking of resolution state without expensive graph traversal
**Alternatives Considered**: Using relationship existence checks (too slow at scale)
**Trade-offs**: Additional property storage vs query performance gain

#### ADR-002: UnresolvedEntity Tracking Node
**Decision**: Create separate UnresolvedEntity nodes for queue management
**Rationale**: Centralizes tracking for entities mentioned across multiple documents
**Alternatives Considered**: Properties on Entity nodes only (leads to duplication)
**Trade-offs**: Additional node type vs efficient batch processing

#### ADR-003: Dual Relationship Model
**Decision**: Maintain both RESOLVES_TO and MENTIONS_CVE relationships
**Rationale**: RESOLVES_TO preserves entity-level resolution, MENTIONS_CVE optimizes document queries
**Alternatives Considered**: Single relationship type (poor query performance for document-centric queries)
**Trade-offs**: Relationship redundancy vs query optimization

#### ADR-004: Priority-Based Enrichment
**Decision**: Implement priority scoring for enrichment queue
**Rationale**: Prioritize frequently-mentioned entities for faster business value
**Alternatives Considered**: FIFO queue (doesn't address high-impact entities first)
**Trade-offs**: Complexity of priority calculation vs efficient resource utilization

---

### 9. Quality Attributes

#### 9.1 Performance
- **Entity Resolution**: < 100ms per document (batch mode)
- **Enrichment Batch**: 200 entities per minute
- **Query Response**: < 50ms for document CVE lookups

#### 9.2 Scalability
- Supports 1M+ unresolved entities in queue
- Handles 10K+ documents with unresolved mentions
- Batch processing scales linearly with entity count

#### 9.3 Reliability
- Retry logic with exponential backoff (24h → 72h → 7d)
- Maximum retry limit (10 attempts) prevents infinite loops
- Graceful degradation: unresolved entities still queryable

#### 9.4 Maintainability
- Clear separation of concerns (resolution, tracking, enrichment)
- Migration path for existing data
- Backward compatible with current schema

---

### 10. Operational Considerations

#### 10.1 Monitoring Metrics
```cypher
// Dashboard metrics query
MATCH (e:Entity {label: 'CVE'})
WITH e.resolution_status as status, count(e) as count
RETURN status, count

UNION

MATCH (ue:UnresolvedEntity)
RETURN 'queued_for_enrichment' as status, count(ue) as count

UNION

MATCH (ue:UnresolvedEntity)
WHERE ue.priority_score >= 0.7
RETURN 'high_priority_queue' as status, count(ue) as count
```

**Key Metrics:**
- Resolution rate: resolved / (resolved + unresolved)
- Queue depth: count of queued UnresolvedEntity nodes
- Enrichment success rate: newly resolved / enrichment attempts
- Average time to resolution: timestamp delta analysis

#### 10.2 Maintenance Tasks
- **Daily**: Run enrichment batch process
- **Weekly**: Update priority scores, cleanup old failures
- **Monthly**: Analyze resolution patterns, optimize retry intervals
- **Quarterly**: Review and purge permanently unresolvable entities

#### 10.3 Alert Thresholds
- **Warning**: Unresolved entity queue > 10,000
- **Critical**: Resolution rate < 70%
- **Info**: High-priority queue > 100 entities

---

### 11. Future Enhancements

#### 11.1 Machine Learning Integration
- Train model to predict CVE publication timing
- Smart retry scheduling based on CVE ID patterns
- Auto-classify malformed vs legitimate future CVEs

#### 11.2 External API Integration
- Subscribe to CVE publication feeds for proactive enrichment
- Cross-reference multiple vulnerability databases
- Automated validation of CVE existence

#### 11.3 User Feedback Loop
- Manual resolution override capability
- User-reported false positives
- Confidence score refinement based on feedback

---

## Implementation Checklist

### Phase 1: Schema Enhancement (Week 1)
- [ ] Add new properties to Entity nodes
- [ ] Create UnresolvedEntity node type
- [ ] Implement enhanced resolution queries
- [ ] Create database indexes

### Phase 2: Core Implementation (Week 2)
- [ ] Update EntityResolver methods
- [ ] Implement batch enrichment process
- [ ] Add priority score calculation
- [ ] Create query methods for unresolved entities

### Phase 3: Migration (Week 3)
- [ ] Migrate existing entities to new schema
- [ ] Create UnresolvedEntity nodes for existing data
- [ ] Validate data integrity
- [ ] Performance testing

### Phase 4: Operational Integration (Week 4)
- [ ] Implement scheduled enrichment service
- [ ] Create monitoring dashboard
- [ ] Setup alerting
- [ ] Documentation and training

---

## Version History

- **v1.0.0** (2025-10-29): Initial architecture design with forward compatibility for unresolved entities

---

## References & Sources

- Neo4j Graph Data Modeling Best Practices: https://neo4j.com/developer/modeling/
- NVD API Documentation: https://nvd.nist.gov/developers
- Existing Implementation: entity_resolver.py (v1.0.0)

---

**DELIVERABLE STATUS**: ✅ COMPLETE

This architecture design provides:
1. ✅ Schema enhancements with resolution_status tracking
2. ✅ UnresolvedEntity tracking for future enrichment
3. ✅ Dual relationship model (RESOLVES_TO + MENTIONS_CVE)
4. ✅ Architecture diagrams showing data flow
5. ✅ Comprehensive Cypher query examples
6. ✅ Implementation guidance and migration strategy
7. ✅ Performance optimization strategies
8. ✅ Operational considerations and monitoring
