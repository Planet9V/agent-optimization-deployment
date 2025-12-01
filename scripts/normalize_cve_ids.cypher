// CVE ID Normalization Script
// Purpose: Normalize "cve-CVE-*" to "CVE-*" format
// EXECUTE AFTER VALIDATION PASSES

// Step 1: Normalize CVE node IDs (179,522 nodes estimated)
// Batch size: 10,000 nodes per transaction for performance
CALL apoc.periodic.iterate(
  "MATCH (c:CVE) WHERE c.id STARTS WITH 'cve-CVE-' RETURN c",
  "SET c.id = REPLACE(c.id, 'cve-', '')",
  {batchSize: 10000, parallel: false}
)
YIELD batches, total, timeTaken, committedOperations, failedOperations, failedBatches, retries, errorMessages
RETURN batches, total, timeTaken, committedOperations, failedOperations, failedBatches, retries, errorMessages;

// Step 2: Verify normalization completed successfully
MATCH (c:CVE)
WITH c,
  CASE
    WHEN c.id STARTS WITH 'cve-CVE-' THEN 'UNNORMALIZED'
    WHEN c.id STARTS WITH 'CVE-' THEN 'NORMALIZED'
    ELSE 'UNEXPECTED'
  END AS status
RETURN status, COUNT(*) AS count;

// Step 3: Report normalization results
MATCH (c:CVE)
WHERE c.id STARTS WITH 'CVE-'
RETURN COUNT(*) AS normalized_cve_count;
