// CVE ID Normalization Rollback Script
// Purpose: Revert "CVE-*" back to "cve-CVE-*" format
// USE ONLY IF NORMALIZATION CAUSED ISSUES

// WARNING: This rollback assumes:
// 1. All CVE nodes currently have "CVE-*" format
// 2. Original format was "cve-CVE-*" (lowercase prefix)
// 3. No data was deleted during normalization

// Step 1: Create backup of current state before rollback
MATCH (c:CVE)
WHERE c.id STARTS WITH 'CVE-'
RETURN COUNT(*) AS cve_nodes_before_rollback;

// Step 2: Rollback CVE node IDs to original format
CALL apoc.periodic.iterate(
  "MATCH (c:CVE) WHERE c.id STARTS WITH 'CVE-' RETURN c",
  "SET c.id = 'cve-' + c.id",
  {batchSize: 10000, parallel: false}
)
YIELD batches, total, timeTaken, committedOperations, failedOperations, failedBatches, retries, errorMessages
RETURN batches, total, timeTaken, committedOperations, failedOperations, failedBatches, retries, errorMessages;

// Step 3: Verify rollback completed successfully
MATCH (c:CVE)
WITH c,
  CASE
    WHEN c.id STARTS WITH 'cve-CVE-' THEN 'ROLLED_BACK'
    WHEN c.id STARTS WITH 'CVE-' THEN 'STILL_NORMALIZED'
    ELSE 'UNEXPECTED'
  END AS status
RETURN status, COUNT(*) AS count;

// Step 4: Final verification against v1 backup baseline
MATCH (c:CVE)
WHERE c.id STARTS WITH 'cve-CVE-'
RETURN COUNT(*) AS rolled_back_cve_count,
       'Expected: 179,522 (or similar to pre-normalization count)' AS expected_count;
