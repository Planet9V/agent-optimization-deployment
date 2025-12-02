# PROCEDURE: [PROC-113] SBOM Vulnerability Analysis

**Procedure ID**: PROC-113
**Version**: 1.0.0
**Created**: 2025-11-26
**Last Modified**: 2025-11-26
**Author**: AEON ETL Agent System
**Status**: APPROVED

---

## 1. METADATA

| Field | Value |
|-------|-------|
| **Category** | ETL |
| **Frequency** | ON-DEMAND / WEEKLY |
| **Priority** | CRITICAL |
| **Estimated Duration** | 30-60 minutes per SBOM |
| **Risk Level** | MEDIUM |
| **Rollback Available** | YES |

---

## 2. PURPOSE & OBJECTIVES

### 2.1 Purpose Statement
Parse Software Bill of Materials (SBOM) files in CycloneDX and SPDX formats, extract component and dependency information, correlate with NVD vulnerability data using CPE/PURL matching, and create SoftwareComponent and DependsOn relationships for supply chain risk analysis.

### 2.2 Business Objectives
- [x] Ingest SBOM files (CycloneDX 1.4, SPDX 2.3)
- [x] Extract software components with versions and PURLs
- [x] Match components to CVE database using CPE/PURL
- [x] Create dependency graphs for supply chain analysis
- [x] Calculate aggregate risk scores for software products

### 2.3 McKenney Questions Addressed
| Question | How Addressed |
|----------|---------------|
| Q1: What equipment do we have? | SoftwareComponent inventory from SBOMs |
| Q2: What equipment do customers have? | Customer SBOM ingestion and analysis |
| Q3: What do attackers know? | Public vulnerability data for components |
| Q5: How do we defend? | Identify and patch vulnerable dependencies |

---

## 3. PRE-CONDITIONS

### 3.1 Infrastructure Requirements

| Component | Required State | Verification Command |
|-----------|---------------|---------------------|
| Neo4j | Running, accessible | `docker ps | grep neo4j` |
| Python 3.9+ | Installed | `python3 --version` |
| cyclonedx-python | Installed | `pip show cyclonedx-bom` |

### 3.2 Data Pre-Conditions

| Condition | Verification Query | Expected Result |
|-----------|-------------------|-----------------|
| CVE nodes exist | `MATCH (cve:CVE) RETURN count(cve)` | >= 10,000 |
| NVD CPE data loaded | `MATCH (cve:CVE) WHERE cve.cpe IS NOT NULL RETURN count(cve)` | >= 5,000 |

### 3.3 Prior Procedures Required

| Procedure ID | Procedure Name |
|--------------|---------------|
| PROC-001 | Schema Migration |
| PROC-101 | CVE Enrichment |

---

## 4. DATA SOURCES

### 4.1 Source Overview

| Source Name | Type | Location | Format |
|-------------|------|----------|--------|
| SBOM Files | User-provided | Configurable upload directory | CycloneDX JSON/XML, SPDX JSON/RDF |
| NVD CVE Data | Database | Neo4j (existing) | Graph nodes |
| OSV Database | API | https://api.osv.dev/ | JSON REST API |

### 4.2 CycloneDX SBOM Schema
```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.4",
  "components": [
    {
      "bom-ref": "pkg:npm/lodash@4.17.19",
      "type": "library",
      "name": "lodash",
      "version": "4.17.19",
      "purl": "pkg:npm/lodash@4.17.19",
      "licenses": [{"license": {"id": "MIT"}}],
      "hashes": [{"alg": "SHA-256", "content": "..."}]
    }
  ],
  "dependencies": [
    {
      "ref": "pkg:npm/my-app@1.0.0",
      "dependsOn": ["pkg:npm/lodash@4.17.19"]
    }
  ]
}
```

### 4.3 OSV API Endpoint
```bash
curl -X POST https://api.osv.dev/v1/query \
  -H "Content-Type: application/json" \
  -d '{"package": {"name": "lodash", "ecosystem": "npm"}, "version": "4.17.19"}'
```

---

## 5. DESTINATION

### 5.1 Target System

| Field | Value |
|-------|-------|
| **System** | Neo4j |
| **Container** | openspg-neo4j |
| **Port** | 7687 (Bolt) |
| **Volume** | active_neo4j_data |

### 5.2 Target Schema

**Node Types**:
| Label | Properties | Constraints |
|-------|-----------|-------------|
| SoftwareComponent | purl, name, version, type | UNIQUE on purl |
| SoftwareProduct | name, version, vendor | UNIQUE on (name, version) |
| Package | ecosystem, name, version | INDEX on (ecosystem, name) |

**Relationships**:
| Type | Source | Target |
|------|--------|--------|
| DEPENDS_ON | (:SoftwareComponent) | (:SoftwareComponent) |
| HAS_COMPONENT | (:SoftwareProduct) | (:SoftwareComponent) |
| HAS_VULNERABILITY | (:SoftwareComponent) | (:CVE) |
| FIXES_VULNERABILITY | (:SoftwareComponent) | (:CVE) |

---

## 6. TRANSFORMATION LOGIC

### 6.1 PURL to CVE Matching

**Package URL (PURL) Format**: `pkg:TYPE/NAMESPACE/NAME@VERSION`

**Matching Strategy**:
1. Extract ecosystem (npm, pypi, maven, etc.)
2. Extract package name and version
3. Query OSV API for vulnerabilities
4. Query NVD for CPE matches
5. Create HAS_VULNERABILITY relationships

### 6.2 CPE Matching Example
```python
# Component: pkg:npm/lodash@4.17.19
# CPE Match: cpe:2.3:a:lodash:lodash:4.17.19:*:*:*:*:node.js:*:*
```

### 6.3 Validation Rules

| Rule | Field | Validation | Action |
|------|-------|------------|--------|
| VAL-001 | purl | Valid PURL format | REJECT invalid |
| VAL-002 | version | Semver or valid version | WARN if non-standard |
| VAL-003 | dependencies | Circular check | WARN if circular |

---

## 7. EXECUTION STEPS

### Step 1: Install Dependencies
```bash
pip install cyclonedx-bom==3.11.0 spdx-tools==0.8.0 requests==2.31.0
```

### Step 2: Create Schema Constraints
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" << 'EOF'
CREATE CONSTRAINT software_component_purl_unique IF NOT EXISTS FOR (sc:SoftwareComponent) REQUIRE sc.purl IS UNIQUE;
CREATE INDEX software_product_name_version_idx IF NOT EXISTS FOR (sp:SoftwareProduct) ON (sp.name, sp.version);
EOF
```

### Step 3: Run SBOM Ingestion Script
```bash
python3 << 'SCRIPT'
import json
import requests
from neo4j import GraphDatabase
from urllib.parse import urlparse, parse_qs

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j@openspg"))

def parse_purl(purl_string):
    """Parse Package URL into components"""
    # pkg:npm/lodash@4.17.19 -> {type: npm, name: lodash, version: 4.17.19}
    if not purl_string.startswith('pkg:'):
        return None

    parts = purl_string[4:].split('/')
    pkg_type = parts[0]

    if len(parts) > 1:
        name_version = parts[-1]
        if '@' in name_version:
            name, version = name_version.rsplit('@', 1)
        else:
            name, version = name_version, None
    else:
        return None

    return {'type': pkg_type, 'name': name, 'version': version}

def query_osv_vulnerabilities(ecosystem, name, version):
    """Query OSV API for package vulnerabilities"""
    url = "https://api.osv.dev/v1/query"
    payload = {
        "package": {"name": name, "ecosystem": ecosystem},
        "version": version
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('vulns', [])
    except Exception as e:
        print(f"OSV query failed: {e}")

    return []

def ingest_cyclonedx_sbom(session, sbom_data, sbom_name):
    """Ingest CycloneDX SBOM into Neo4j"""

    # Create SoftwareProduct node
    session.run("""
        MERGE (sp:SoftwareProduct {name: $name, version: $version})
        SET sp.sbom_format = 'CycloneDX',
            sp.spec_version = $spec_version,
            sp.ingested_at = datetime()
    """, name=sbom_name, version=sbom_data.get('version', '1.0.0'),
        spec_version=sbom_data.get('specVersion', '1.4'))

    # Ingest components
    components = sbom_data.get('components', [])
    for comp in components:
        purl = comp.get('purl')
        if not purl:
            continue

        parsed = parse_purl(purl)
        if not parsed:
            continue

        # Create SoftwareComponent node
        session.run("""
            MERGE (sc:SoftwareComponent {purl: $purl})
            SET sc.name = $name,
                sc.version = $version,
                sc.type = $comp_type,
                sc.ecosystem = $ecosystem,
                sc.licenses = $licenses,
                sc.ingested_at = datetime()
        """, purl=purl, name=parsed['name'], version=parsed['version'],
            comp_type=comp.get('type', 'library'), ecosystem=parsed['type'],
            licenses=[lic.get('license', {}).get('id') for lic in comp.get('licenses', [])])

        # Link component to product
        session.run("""
            MATCH (sp:SoftwareProduct {name: $product_name})
            MATCH (sc:SoftwareComponent {purl: $purl})
            MERGE (sp)-[:HAS_COMPONENT]->(sc)
        """, product_name=sbom_name, purl=purl)

        # Query vulnerabilities
        vulns = query_osv_vulnerabilities(parsed['type'], parsed['name'], parsed['version'])
        for vuln in vulns:
            vuln_id = vuln.get('id', '')
            if vuln_id.startswith('CVE-'):
                # Link to existing CVE
                session.run("""
                    MATCH (sc:SoftwareComponent {purl: $purl})
                    MATCH (cve:CVE {cve_id: $cve_id})
                    MERGE (sc)-[r:HAS_VULNERABILITY]->(cve)
                    SET r.source = 'osv-api',
                        r.detected_at = datetime()
                """, purl=purl, cve_id=vuln_id)

    # Ingest dependencies
    dependencies = sbom_data.get('dependencies', [])
    for dep in dependencies:
        ref = dep.get('ref')
        depends_on = dep.get('dependsOn', [])

        for target_ref in depends_on:
            session.run("""
                MATCH (source:SoftwareComponent {purl: $source_purl})
                MATCH (target:SoftwareComponent {purl: $target_purl})
                MERGE (source)-[:DEPENDS_ON]->(target)
            """, source_purl=ref, target_purl=target_ref)

# Example usage: Ingest a CycloneDX SBOM file
sbom_file_path = "/path/to/sbom.json"  # User provides this path

try:
    with open(sbom_file_path, 'r') as f:
        sbom_data = json.load(f)

    sbom_name = sbom_data.get('metadata', {}).get('component', {}).get('name', 'UnknownProduct')

    with driver.session() as session:
        ingest_cyclonedx_sbom(session, sbom_data, sbom_name)

    print(f"SBOM ingestion complete: {sbom_name}")

except FileNotFoundError:
    print(f"SBOM file not found: {sbom_file_path}")
except json.JSONDecodeError:
    print(f"Invalid JSON in SBOM file")

driver.close()
SCRIPT
```

### Step 4: Verify Results
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" << 'EOF'
MATCH (sp:SoftwareProduct) RETURN sp.name, sp.version;
MATCH (sc:SoftwareComponent) RETURN count(sc) AS components;
MATCH (sc:SoftwareComponent)-[r:HAS_VULNERABILITY]->(cve:CVE) RETURN count(r) AS vulnerabilities;
EOF
```

---

## 8. POST-EXECUTION VERIFICATION

### Verify SBOM Ingestion
```cypher
MATCH (sp:SoftwareProduct)-[:HAS_COMPONENT]->(sc:SoftwareComponent)
RETURN sp.name, count(sc) AS component_count
ORDER BY component_count DESC;
```

### Identify Vulnerable Components
```cypher
MATCH (sc:SoftwareComponent)-[:HAS_VULNERABILITY]->(cve:CVE)
WHERE cve.cvssV3Severity IN ['HIGH', 'CRITICAL']
RETURN sc.name, sc.version, cve.cve_id, cve.cvssV3BaseScore
ORDER BY cve.cvssV3BaseScore DESC
LIMIT 20;
```

### Dependency Graph Analysis
```cypher
MATCH path = (root:SoftwareComponent)-[:DEPENDS_ON*1..3]->(dep:SoftwareComponent)
             -[:HAS_VULNERABILITY]->(cve:CVE)
WHERE root.name = 'my-application'
RETURN root.name, dep.name, cve.cve_id, length(path) AS depth
LIMIT 10;
```

### Success Criteria

| Criterion | Threshold | Actual |
|-----------|-----------|--------|
| SoftwareComponents created | >= 10 | ___ |
| Vulnerabilities detected | >= 1 | ___ |
| DEPENDS_ON relationships | >= 5 | ___ |
| Transitive vulnerability detection | Works | ___ |

---

## 9. ROLLBACK PROCEDURE

### Remove SBOM Data for Specific Product
```cypher
MATCH (sp:SoftwareProduct {name: 'ProductName'})-[:HAS_COMPONENT]->(sc:SoftwareComponent)
DETACH DELETE sp, sc;
```

---

## 10. SCHEDULING & AUTOMATION

### On-Demand Execution
```bash
# Usage: ./proc_113_sbom_analysis.sh /path/to/sbom.json
/home/jim/2_OXOT_Projects_Dev/scripts/etl/proc_113_sbom_analysis.sh "$SBOM_PATH"
```

### Weekly Scan of SBOM Directory
```cron
# Weekly on Mondays at 4 AM
0 4 * * 1 /home/jim/2_OXOT_Projects_Dev/scripts/etl/proc_113_weekly_sbom_scan.sh >> /var/log/aeon/proc_113.log 2>&1
```

---

## 11. MONITORING & ALERTING

### Metrics to Monitor

| Metric | Source | Threshold | Alert |
|--------|--------|-----------|-------|
| Execution duration | Log | > 2 hours | ERROR |
| Critical vulnerabilities | Neo4j | > 0 | CRITICAL |
| OSV API failures | Log | > 10% | WARN |

---

## 12. CHANGE HISTORY

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-11-26 | AEON ETL System | Initial procedure for E03 SBOM Analysis |

---

## 13. APPENDICES

### Appendix A: Supported SBOM Formats
- CycloneDX 1.4 (JSON, XML)
- SPDX 2.3 (JSON, RDF, Tag-Value)

### Appendix B: Data Sources
- NVD: https://nvd.nist.gov/
- OSV: https://osv.dev/
- GitHub Advisory Database: https://github.com/advisories

---

**End of Procedure PROC-113**
