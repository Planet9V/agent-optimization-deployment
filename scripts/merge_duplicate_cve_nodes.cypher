// CVE Node Merge Script - Correct Normalization Strategy
// Purpose: Merge "cve-CVE-*" nodes with existing "CVE-*" nodes
// Handles duplicate conflicts by consolidating properties and relationships

// WARNING: This script is IRREVERSIBLE. Create full backup before execution.

// ========================================
// STEP 1: IDENTIFY DUPLICATE PAIRS
// ========================================
// Count duplicate pairs before merge
MATCH (c1:CVE)
WHERE c1.id STARTS WITH 'cve-CVE-'
WITH c1, REPLACE(c1.id, 'cve-', '') AS normalized_id
MATCH (c2:CVE)
WHERE c2.id = normalized_id
RETURN COUNT(*) AS duplicate_pairs_to_merge;
// Expected: 321 pairs

// ========================================
// STEP 2: MERGE DUPLICATE CVE NODES
// ========================================
// Strategy: Merge "cve-CVE-*" nodes into existing "CVE-*" nodes
// - Keep existing "CVE-*" node (assumed to be authoritative)
// - Merge all relationships from "cve-CVE-*" to "CVE-*"
// - Consolidate properties (prefer non-null values)
// - Delete redundant "cve-CVE-*" node

CALL apoc.periodic.iterate(
  // Find duplicate pairs
  "MATCH (old:CVE)
   WHERE old.id STARTS WITH 'cve-CVE-'
   WITH old, REPLACE(old.id, 'cve-', '') AS normalized_id
   MATCH (new:CVE {id: normalized_id})
   RETURN old, new",

  // Merge logic
  "// Step 1: Merge properties (keep non-null values from both nodes)
   WITH old, new,
        REDUCE(props = {}, key IN KEYS(old) |
          CASE
            WHEN old[key] IS NOT NULL AND (new[key] IS NULL OR new[key] = old[key])
            THEN props + {[key]: old[key]}
            ELSE props
          END
        ) AS merged_props
   SET new += merged_props

   // Step 2: Merge all incoming relationships to new node
   WITH old, new
   MATCH (source)-[r]->(old)
   CALL apoc.refactor.to(r, new) YIELD input, output

   // Step 3: Merge all outgoing relationships to new node
   WITH old, new
   MATCH (old)-[r]->(target)
   CALL apoc.refactor.from(r, new) YIELD input, output

   // Step 4: Delete old redundant node
   WITH old
   DETACH DELETE old",

  {batchSize: 1000, parallel: false, retries: 3}
)
YIELD batches, total, timeTaken, committedOperations, failedOperations, failedBatches, retries, errorMessages
RETURN batches, total, timeTaken, committedOperations, failedOperations, failedBatches, retries, errorMessages;

// ========================================
// STEP 3: NORMALIZE REMAINING CVE NODES
// ========================================
// After merging duplicates, normalize remaining "cve-CVE-*" nodes that have no conflicts

CALL apoc.periodic.iterate(
  // Find remaining unnormalized CVE nodes (no existing "CVE-*" counterpart)
  "MATCH (c:CVE)
   WHERE c.id STARTS WITH 'cve-CVE-'
   WITH c, REPLACE(c.id, 'cve-', '') AS normalized_id
   WHERE NOT EXISTS { MATCH (other:CVE {id: normalized_id}) }
   RETURN c, normalized_id",

  // Simple ID replacement (safe for non-duplicate nodes)
  "SET c.id = normalized_id",

  {batchSize: 10000, parallel: false}
)
YIELD batches, total, timeTaken, committedOperations, failedOperations, failedBatches, retries, errorMessages
RETURN batches, total, timeTaken, committedOperations, failedOperations, failedBatches, retries, errorMessages;

// ========================================
// STEP 4: VERIFY NORMALIZATION SUCCESS
// ========================================
// Count CVE nodes by format after normalization
MATCH (c:CVE)
WITH c,
  CASE
    WHEN c.id STARTS WITH 'cve-CVE-' THEN 'UNNORMALIZED (FAILED)'
    WHEN c.id STARTS WITH 'CVE-' THEN 'NORMALIZED (SUCCESS)'
    ELSE 'OTHER (UNEXPECTED)'
  END AS status
RETURN status, COUNT(*) AS count
ORDER BY count DESC;

// Expected Results:
// - NORMALIZED (SUCCESS): 179,522 - 321 duplicates + 321 existing = 179,522 total
// - UNNORMALIZED (FAILED): 0 (should be 0 if successful)
// - OTHER (UNEXPECTED): 87,644 (unchanged)

// ========================================
// STEP 5: FINAL VALIDATION
// ========================================
// Verify total CVE count decreased by number of merged duplicates
MATCH (c:CVE)
RETURN COUNT(*) AS total_cve_nodes,
       'Expected: 267,487 - 321 = 267,166 (if all duplicates merged)' AS expected_count;

// Verify no duplicate CVE IDs remain
MATCH (c:CVE)
WHERE c.id STARTS WITH 'CVE-'
WITH c.id AS cve_id, COUNT(*) AS duplicate_count
WHERE duplicate_count > 1
RETURN cve_id, duplicate_count;
// Expected: 0 rows (no duplicates)

// ========================================
// NOTES
// ========================================
// 1. This script requires APOC library for relationship refactoring
// 2. Execution time: ~15-30 minutes for 179,522 nodes
// 3. Create full backup before execution (neo4j-admin dump)
// 4. Monitor progress via batch completion logs
// 5. If failures occur, check errorMessages field for details
