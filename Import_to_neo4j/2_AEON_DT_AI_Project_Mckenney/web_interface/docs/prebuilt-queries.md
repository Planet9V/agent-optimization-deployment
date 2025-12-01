# Pre-Built Cybersecurity Queries - Graph Explorer

## Overview
Added 10 pre-built, read-only Cypher queries to the Graph Explorer page for common cybersecurity analysis tasks.

## Location
File: `/app/graph/page.tsx`
Lines: 26-78

## Queries Added

### 1. Critical CVEs
```cypher
MATCH (c:CVE) WHERE c.severity = 'CRITICAL' RETURN c LIMIT 25
```
**Description**: Show 25 most recent critical vulnerabilities

### 2. Threat Actor Network
```cypher
MATCH (t:ThreatActor)-[r]-(m:Malware) RETURN t, r, m LIMIT 50
```
**Description**: Threat actors and their associated malware

### 3. Attack Techniques
```cypher
MATCH (a:AttackTechnique)-[:PART_OF]->(t:Tactic) RETURN a, t LIMIT 30
```
**Description**: MITRE ATT&CK techniques by tactic

### 4. Vulnerable ICS Assets
```cypher
MATCH (i:ICSAsset)-[:HAS_VULNERABILITY]->(v:CVE) WHERE v.cvss_score > 7.0 RETURN i, v LIMIT 25
```
**Description**: ICS assets with high-severity vulnerabilities

### 5. CWE Relationships
```cypher
MATCH (cve:CVE)-[:HAS_WEAKNESS]->(cwe:CWE) RETURN cve, cwe LIMIT 50
```
**Description**: CVEs and their associated CWE weaknesses

### 6. High-Severity CVEs
```cypher
MATCH (cve:CVE) WHERE cve.cvss_score > 7.0 RETURN cve LIMIT 100
```
**Description**: All CVEs with CVSS score above 7.0

### 7. Threat Actor Campaigns
```cypher
MATCH (actor:ThreatActor)-[:CONDUCTS]->(campaign:Campaign) RETURN actor, campaign LIMIT 50
```
**Description**: Active threat actor campaigns

### 8. Attack Paths
```cypher
MATCH path=(actor:ThreatActor)-[:USES_TTP]->(technique:AttackTechnique)-[:TARGETS]->(asset) RETURN path LIMIT 50
```
**Description**: Complete attack paths from threat actors to targets

### 9. Malware Families
```cypher
MATCH (malware:Malware) RETURN malware.name, labels(malware) LIMIT 50
```
**Description**: Known malware families and their classifications

### 10. MITRE ATT&CK Techniques
```cypher
MATCH (technique:AttackTechnique) RETURN technique LIMIT 100
```
**Description**: All MITRE ATT&CK techniques in the database

## Safety Features

- **Read-Only**: All queries use `MATCH` and `RETURN` only - no `CREATE`, `DELETE`, or `SET` operations
- **Schema-Compliant**: Queries follow existing Neo4j node labels and relationship types
- **Limited Results**: All queries include `LIMIT` clauses to prevent database overload
- **No Modifications**: Queries only retrieve data, never modify the graph structure

## User Interface

The queries are accessible via:
1. Click "Show Query Builder" button on the Graph Explorer page
2. Select from the "Pre-built Cybersecurity Queries" dropdown
3. Query automatically populates in the custom query textarea
4. Click "Execute Query" to run the selected query

## Implementation Details

- Query array includes `name`, `query`, and `description` fields
- Dropdown shows both query name and description for context
- Tooltip on hover displays full description
- All queries validated against Neo4j schema constraints
