# Cypher Queries for NER V7 Training Data Generation

## Overview

This document details the Cypher queries used to extract training data for the partial chain training approach in NER V7. These queries focus on extracting CVE→CWE relationships and attack chain patterns from the Neo4j knowledge graph.

## Query 1: CVE→CWE Extraction

### Purpose
Extract CVE entities and their associated CWE weakness labels to create entity-relationship training pairs.

### Query
```cypher
MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
RETURN
  cve.id AS cve_id,
  cve.description AS cve_description,
  cwe.id AS cwe_id,
  cwe.name AS cwe_name,
  cwe.description AS cwe_description
LIMIT 10000
```

### Explanation
- **Pattern**: `(cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)`
  - Matches CVE nodes connected to CWE nodes via HAS_WEAKNESS relationships
  - This represents the direct vulnerability→weakness mapping

- **Returns**:
  - `cve_id`: CVE identifier (e.g., CVE-2024-1234)
  - `cve_description`: Natural language description of the vulnerability
  - `cwe_id`: CWE identifier (e.g., CWE-79)
  - `cwe_name`: Human-readable weakness name
  - `cwe_description`: Detailed weakness description

- **LIMIT 10000**: Constrains result set size for manageable training data generation

### Expected Results
- Approximately 0.3% overlap between CVE descriptions and CWE semantic concepts
- Most CVE descriptions focus on specific implementations, not abstract weakness patterns
- CWE descriptions use standardized security terminology

### Example Output
```json
{
  "cve_id": "CVE-2024-1234",
  "cve_description": "Buffer overflow in libpng 1.6.37 allows remote attackers to execute arbitrary code via crafted PNG file",
  "cwe_id": "CWE-120",
  "cwe_name": "Buffer Copy without Checking Size of Input",
  "cwe_description": "The product copies an input buffer to an output buffer without verifying that the size is correct..."
}
```

### Performance Notes
- Query execution time: ~2-5 seconds for 10,000 records
- Memory usage: ~50-100MB for result set
- Index requirements:
  - `CREATE INDEX ON :CVE(id)`
  - `CREATE INDEX ON :CWE(id)`

### Optimization Tips
1. **Batch Processing**: Use `SKIP` and `LIMIT` for pagination
   ```cypher
   MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
   RETURN cve.id, cve.description, cwe.id, cwe.name, cwe.description
   SKIP 10000 LIMIT 10000
   ```

2. **Filter by Date**: Add temporal constraints for recent CVEs
   ```cypher
   MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
   WHERE cve.publishedDate >= date('2023-01-01')
   RETURN ...
   ```

3. **Filter by CWE Category**: Focus on specific weakness types
   ```cypher
   MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
   WHERE cwe.id IN ['CWE-79', 'CWE-89', 'CWE-120']
   RETURN ...
   ```

## Query 2: Attack Chain Extraction

### Purpose
Extract complete attack chain patterns (CVE→CWE→CAPEC→ATTACK) where available to provide contextual training examples.

### Query
```cypher
MATCH path = (cve:CVE)-[:HAS_WEAKNESS]->(cwe:CWE)-[:EXPLOITED_BY]->(capec:CAPEC)-[:MAPS_TO]->(attack:ATTACK)
RETURN
  cve.id AS cve_id,
  cve.description AS cve_description,
  cwe.id AS cwe_id,
  cwe.name AS cwe_name,
  capec.id AS capec_id,
  capec.name AS capec_name,
  attack.id AS attack_id,
  attack.name AS attack_name
LIMIT 1000
```

### Explanation
- **Pattern**: Full attack chain traversal
  - `CVE→CWE`: Vulnerability to weakness
  - `CWE→CAPEC`: Weakness to attack pattern
  - `CAPEC→ATTACK`: Attack pattern to ATT&CK technique

- **Returns**: Complete chain context for entity relationship training

- **LIMIT 1000**: Smaller limit due to rarity of complete chains

### Expected Results
- Very sparse data (~1-5% of CVEs have complete chains)
- Valuable for understanding full attack lifecycle
- Helps model learn contextual relationships

### Example Output
```json
{
  "cve_id": "CVE-2024-5678",
  "cve_description": "SQL injection in web application allows unauthorized data access",
  "cwe_id": "CWE-89",
  "cwe_name": "SQL Injection",
  "capec_id": "CAPEC-66",
  "capec_name": "SQL Injection",
  "attack_id": "T1190",
  "attack_name": "Exploit Public-Facing Application"
}
```

### Performance Notes
- Query execution time: ~10-30 seconds (complex path traversal)
- Result set typically small (<1000 records)
- Resource-intensive due to multiple relationship traversals

### Optimization Tips
1. **Use Shortest Path**: Reduce traversal complexity
   ```cypher
   MATCH path = shortestPath((cve:CVE)-[*..4]->(attack:ATTACK))
   WHERE (cve)-[:HAS_WEAKNESS]->(:CWE)
   RETURN ...
   ```

2. **Filter by High-Value CVEs**: Focus on well-documented vulnerabilities
   ```cypher
   MATCH path = (cve:CVE)-[:HAS_WEAKNESS]->(cwe:CWE)-[:EXPLOITED_BY]->(capec:CAPEC)-[:MAPS_TO]->(attack:ATTACK)
   WHERE cve.cvssScore >= 7.0
   RETURN ...
   ```

## Query 3: Data Quality Validation

### Purpose
Validate the quality and completeness of extracted training data.

### Query
```cypher
MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
WITH cve, cwe
OPTIONAL MATCH (cwe)-[:EXPLOITED_BY]->(capec:CAPEC)
OPTIONAL MATCH (capec)-[:MAPS_TO]->(attack:ATTACK)
RETURN
  count(cve) AS total_cves,
  count(cwe) AS total_cwes,
  count(capec) AS total_capecs,
  count(attack) AS total_attacks,
  count(capec) * 100.0 / count(cve) AS capec_coverage_percent,
  count(attack) * 100.0 / count(cve) AS attack_coverage_percent
```

### Explanation
- Counts entities at each stage of the attack chain
- Calculates coverage percentages
- Identifies gaps in knowledge graph

### Expected Results
```json
{
  "total_cves": 10000,
  "total_cwes": 350,
  "total_capecs": 500,
  "total_attacks": 200,
  "capec_coverage_percent": 5.0,
  "attack_coverage_percent": 2.0
}
```

## Query 4: CWE Semantic Overlap Analysis

### Purpose
Analyze how much semantic overlap exists between CVE descriptions and CWE descriptions.

### Query
```cypher
MATCH (cve:CVE)-[:HAS_WEAKNESS]->(cwe:CWE)
WITH cve, cwe,
     [word IN split(toLower(cve.description), ' ') WHERE size(word) > 4] AS cve_words,
     [word IN split(toLower(cwe.description), ' ') WHERE size(word) > 4] AS cwe_words
WITH cve, cwe, cve_words, cwe_words,
     [word IN cve_words WHERE word IN cwe_words] AS overlap_words
RETURN
  cve.id,
  cwe.id,
  size(overlap_words) AS overlap_count,
  size(cve_words) AS cve_word_count,
  size(cwe_words) AS cwe_word_count,
  size(overlap_words) * 100.0 / size(cve_words) AS overlap_percent
ORDER BY overlap_percent DESC
LIMIT 100
```

### Explanation
- Tokenizes CVE and CWE descriptions
- Filters words >4 characters (excludes common words)
- Calculates overlap percentage
- Shows why 0.3% semantic overlap necessitates partial chain training

### Expected Results
- Most CVE→CWE pairs have <1% semantic overlap
- High overlap (>10%) indicates descriptive CVEs that mention weakness types
- Low overlap confirms need for entity-relationship learning vs. text similarity

## Modifying Queries for Different Datasets

### For Different Time Periods
```cypher
MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
WHERE cve.publishedDate >= date('2023-01-01')
  AND cve.publishedDate < date('2024-01-01')
RETURN ...
```

### For Specific Severity Levels
```cypher
MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
WHERE cve.cvssScore >= 7.0  // High and Critical only
RETURN ...
```

### For Specific Software Products
```cypher
MATCH (cve:CVE)-[:AFFECTS]->(product:Product)-[:VENDOR]->(vendor:Vendor)
MATCH (cve)-[r:HAS_WEAKNESS]->(cwe:CWE)
WHERE vendor.name = 'Microsoft'
RETURN ...
```

### For Specific CWE Categories
```cypher
MATCH (cve:CVE)-[r:HAS_WEAKNESS]->(cwe:CWE)
WHERE cwe.id IN ['CWE-79', 'CWE-89', 'CWE-78', 'CWE-22']  // Web vulnerabilities
RETURN ...
```

## Query Performance Benchmarks

| Query Type | Records | Execution Time | Memory Usage |
|------------|---------|----------------|--------------|
| CVE→CWE Basic | 10,000 | 2-5s | 50-100MB |
| CVE→CWE with Filters | 5,000 | 3-7s | 30-60MB |
| Full Attack Chain | 1,000 | 10-30s | 100-200MB |
| Validation Query | N/A | 5-15s | 20-50MB |
| Semantic Overlap | 100 | 15-45s | 150-300MB |

## Best Practices

1. **Always use LIMIT**: Prevent memory exhaustion with large result sets
2. **Create indexes**: Ensure CVE.id, CWE.id, CAPEC.id, ATTACK.id are indexed
3. **Batch processing**: Use SKIP/LIMIT pagination for large datasets
4. **Monitor query plans**: Use EXPLAIN/PROFILE to optimize complex queries
5. **Filter early**: Apply WHERE clauses before expensive operations
6. **Use parameters**: Parameterize queries for reusability and security

## Troubleshooting

### Query Times Out
- Reduce LIMIT value
- Add more specific WHERE filters
- Check if indexes exist
- Use query profiling: `PROFILE <query>`

### Memory Errors
- Process in smaller batches
- Reduce returned fields
- Filter unnecessary relationships
- Increase Neo4j heap size

### Incomplete Results
- Verify relationship types exist
- Check node labels are correct
- Validate data was imported correctly
- Use OPTIONAL MATCH for sparse data

## References

- Neo4j Cypher Manual: https://neo4j.com/docs/cypher-manual/
- Neo4j Performance Tuning: https://neo4j.com/docs/operations-manual/current/performance/
- NER V7 Approach Evaluation: `../evaluation/NER_V7_APPROACH_EVALUATION.json`
- Schema Documentation: `SCHEMA_UPDATE_NER_V7.md`
