// ============================================================
// CUSTOMER_LABELS: Entity Migration Script
// Phase B1 - Order 1 of 6 MVP Enhancements
// Version: 1.0.0
// Created: 2025-12-04
// Purpose: Migrate existing 189,932 entities to customer_id pattern
// ============================================================

// ------------------------------------------------------------
// SECTION 1: Assign customer_id to Shared Data (SYSTEM)
// ------------------------------------------------------------

// 1.1 CVE nodes - shared across all customers
CALL apoc.periodic.iterate(
  "MATCH (n:CVE) WHERE n.customer_id IS NULL RETURN n",
  "SET n.customer_id = 'SYSTEM'",
  {batchSize: 5000, parallel: false}
) YIELD batches, total
RETURN 'CVE' AS label, total AS migrated;

// 1.2 CWE nodes - shared vulnerability types
CALL apoc.periodic.iterate(
  "MATCH (n:CWE) WHERE n.customer_id IS NULL RETURN n",
  "SET n.customer_id = 'SYSTEM'",
  {batchSize: 1000, parallel: false}
) YIELD batches, total
RETURN 'CWE' AS label, total AS migrated;

// 1.3 CAPEC nodes - shared attack patterns
CALL apoc.periodic.iterate(
  "MATCH (n:CAPEC) WHERE n.customer_id IS NULL RETURN n",
  "SET n.customer_id = 'SYSTEM'",
  {batchSize: 1000, parallel: false}
) YIELD batches, total
RETURN 'CAPEC' AS label, total AS migrated;

// 1.4 Technique nodes - shared MITRE ATT&CK
CALL apoc.periodic.iterate(
  "MATCH (n:Technique) WHERE n.customer_id IS NULL RETURN n",
  "SET n.customer_id = 'SYSTEM'",
  {batchSize: 1000, parallel: false}
) YIELD batches, total
RETURN 'Technique' AS label, total AS migrated;

// 1.5 ThreatActor nodes - shared threat intelligence
CALL apoc.periodic.iterate(
  "MATCH (n:ThreatActor) WHERE n.customer_id IS NULL RETURN n",
  "SET n.customer_id = 'SYSTEM'",
  {batchSize: 500, parallel: false}
) YIELD batches, total
RETURN 'ThreatActor' AS label, total AS migrated;

// 1.6 Malware nodes - shared
CALL apoc.periodic.iterate(
  "MATCH (n:Malware) WHERE n.customer_id IS NULL RETURN n",
  "SET n.customer_id = 'SYSTEM'",
  {batchSize: 500, parallel: false}
) YIELD batches, total
RETURN 'Malware' AS label, total AS migrated;

// ------------------------------------------------------------
// SECTION 2: Assign customer_id to Customer-Specific Data (DEFAULT)
// ------------------------------------------------------------

// 2.1 Asset nodes - customer-specific
CALL apoc.periodic.iterate(
  "MATCH (n:Asset) WHERE n.customer_id IS NULL RETURN n",
  "SET n.customer_id = 'DEFAULT'",
  {batchSize: 5000, parallel: false}
) YIELD batches, total
RETURN 'Asset' AS label, total AS migrated;

// 2.2 Entity nodes (NER11 Gold) - customer-specific
CALL apoc.periodic.iterate(
  "MATCH (n:Entity) WHERE n.customer_id IS NULL RETURN n",
  "SET n.customer_id = 'DEFAULT'",
  {batchSize: 5000, parallel: false}
) YIELD batches, total
RETURN 'Entity' AS label, total AS migrated;

// 2.3 Document nodes - customer-specific
CALL apoc.periodic.iterate(
  "MATCH (n:Document) WHERE n.customer_id IS NULL RETURN n",
  "SET n.customer_id = 'DEFAULT'",
  {batchSize: 1000, parallel: false}
) YIELD batches, total
RETURN 'Document' AS label, total AS migrated;

// 2.4 Organization nodes - customer-specific
CALL apoc.periodic.iterate(
  "MATCH (n:Organization) WHERE n.customer_id IS NULL RETURN n",
  "SET n.customer_id = 'DEFAULT'",
  {batchSize: 1000, parallel: false}
) YIELD batches, total
RETURN 'Organization' AS label, total AS migrated;

// 2.5 Software nodes - customer-specific (except shared)
CALL apoc.periodic.iterate(
  "MATCH (n:Software) WHERE n.customer_id IS NULL RETURN n",
  "SET n.customer_id = 'DEFAULT'",
  {batchSize: 1000, parallel: false}
) YIELD batches, total
RETURN 'Software' AS label, total AS migrated;

// 2.6 CPE nodes - customer-specific
CALL apoc.periodic.iterate(
  "MATCH (n:CPE) WHERE n.customer_id IS NULL RETURN n",
  "SET n.customer_id = 'DEFAULT'",
  {batchSize: 5000, parallel: false}
) YIELD batches, total
RETURN 'CPE' AS label, total AS migrated;

// ------------------------------------------------------------
// SECTION 3: Create BELONGS_TO_CUSTOMER Relationships
// ------------------------------------------------------------

// 3.1 Link SYSTEM entities to SYSTEM CustomerLabel
CALL apoc.periodic.iterate(
  "MATCH (n) WHERE n.customer_id = 'SYSTEM'
   AND NOT (n)-[:BELONGS_TO_CUSTOMER]->(:CustomerLabel)
   RETURN n",
  "MATCH (c:CustomerLabel {customer_id: 'SYSTEM'})
   MERGE (n)-[:BELONGS_TO_CUSTOMER {
     assigned_at: datetime(),
     assigned_by: 'migration',
     assignment_type: 'MIGRATION'
   }]->(c)",
  {batchSize: 5000, parallel: false}
) YIELD batches, total
RETURN 'SYSTEM relationships' AS type, total AS created;

// 3.2 Link DEFAULT entities to DEFAULT CustomerLabel
CALL apoc.periodic.iterate(
  "MATCH (n) WHERE n.customer_id = 'DEFAULT'
   AND NOT (n)-[:BELONGS_TO_CUSTOMER]->(:CustomerLabel)
   RETURN n",
  "MATCH (c:CustomerLabel {customer_id: 'DEFAULT'})
   MERGE (n)-[:BELONGS_TO_CUSTOMER {
     assigned_at: datetime(),
     assigned_by: 'migration',
     assignment_type: 'MIGRATION'
   }]->(c)",
  {batchSize: 5000, parallel: false}
) YIELD batches, total
RETURN 'DEFAULT relationships' AS type, total AS created;

// ------------------------------------------------------------
// SECTION 4: Migration Verification
// ------------------------------------------------------------

// Verify all entities have customer_id
MATCH (n)
WHERE n.customer_id IS NULL
WITH labels(n) AS labels, count(*) AS count
WHERE count > 0
RETURN labels, count
ORDER BY count DESC;

// Count entities by customer
MATCH (n)
WHERE n.customer_id IS NOT NULL
RETURN n.customer_id AS customer_id, count(*) AS entity_count
ORDER BY entity_count DESC;

// Count BELONGS_TO_CUSTOMER relationships
MATCH ()-[r:BELONGS_TO_CUSTOMER]->()
RETURN count(r) AS relationship_count;

// Verify no orphaned entities
MATCH (n)
WHERE n.customer_id IS NOT NULL
AND NOT (n)-[:BELONGS_TO_CUSTOMER]->(:CustomerLabel)
RETURN labels(n) AS labels, count(*) AS orphaned
ORDER BY orphaned DESC;

// ============================================================
// END OF MIGRATION SCRIPT
// ============================================================
