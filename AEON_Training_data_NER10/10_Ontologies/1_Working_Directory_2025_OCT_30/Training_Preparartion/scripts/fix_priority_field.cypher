// AEON Protocol - Priority Field Fix
// This query populates the priority field for all EPSS-scored CVEs
// Run this in Neo4j Browser or via Python driver

// Set priority based on EPSS score
MATCH (c:CVE) WHERE c.epss_score IS NOT NULL
SET c.priority = CASE
    WHEN c.epss_score >= 0.7 THEN 'NOW'
    WHEN c.epss_score >= 0.1 THEN 'NEXT'
    ELSE 'NEVER'
END
RETURN c.priority AS priority, count(c) AS count
ORDER BY priority;

// Expected results:
// NOW: ~1,453 CVEs (EPSS >= 0.7)
// NEXT: ~13,215 CVEs (0.1 <= EPSS < 0.7)
// NEVER: ~301,884 CVEs (EPSS < 0.1)

// Validation query:
// MATCH (c:CVE) WHERE c.priority IS NOT NULL
// RETURN c.priority AS priority, count(c) AS count
// ORDER BY priority;
