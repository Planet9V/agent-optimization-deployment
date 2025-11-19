// CVE ID Format Validation Queries
// Purpose: Assess current CVE ID formats before normalization

// 1. Count CVE nodes by ID format pattern
MATCH (c:CVE)
WITH c,
  CASE
    WHEN c.id STARTS WITH 'cve-CVE-' THEN 'cve-CVE-* (needs normalization)'
    WHEN c.id STARTS WITH 'CVE-' THEN 'CVE-* (correct format)'
    ELSE 'OTHER (unexpected format)'
  END AS format_type
RETURN format_type, COUNT(*) AS count
ORDER BY count DESC;

// 2. Sample CVE IDs by format
MATCH (c:CVE)
WHERE c.id STARTS WITH 'cve-CVE-'
RETURN c.id AS incorrect_format
LIMIT 10;

// 3. Check for duplicate CVE IDs after normalization
MATCH (c:CVE)
WHERE c.id STARTS WITH 'cve-CVE-'
WITH REPLACE(c.id, 'cve-', '') AS normalized_id, COLLECT(c.id) AS original_ids
WHERE SIZE(original_ids) > 1
RETURN normalized_id, original_ids, SIZE(original_ids) AS duplicate_count
LIMIT 100;

// 4. Check if normalized IDs already exist in database
MATCH (c1:CVE)
WHERE c1.id STARTS WITH 'cve-CVE-'
WITH REPLACE(c1.id, 'cve-', '') AS normalized_id, c1.id AS original_id
MATCH (c2:CVE {id: normalized_id})
RETURN original_id, normalized_id, c2.id AS existing_node
LIMIT 100;

// 5. Count total relationships for CVE nodes to normalize
MATCH (c:CVE)-[r]-()
WHERE c.id STARTS WITH 'cve-CVE-'
RETURN COUNT(DISTINCT c) AS cve_nodes_with_relationships,
       COUNT(r) AS total_relationships;

// 6. Identify relationship types affected by normalization
MATCH (c:CVE)-[r]-()
WHERE c.id STARTS WITH 'cve-CVE-'
RETURN TYPE(r) AS relationship_type, COUNT(r) AS count
ORDER BY count DESC;

// 7. Check for external references to CVE IDs (property values)
MATCH (n)
WHERE ANY(key IN KEYS(n) WHERE toString(n[key]) CONTAINS 'cve-CVE-')
RETURN LABELS(n)[0] AS node_label,
       KEYS(n) AS properties,
       COUNT(*) AS affected_nodes
LIMIT 100;
