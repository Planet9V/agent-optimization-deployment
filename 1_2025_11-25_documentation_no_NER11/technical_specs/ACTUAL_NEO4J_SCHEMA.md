# ACTUAL NEO4J SCHEMA - AEON Cyber Digital Twin

**Generated**: 2025-11-26
**Source**: active_neo4j_data volume (1.8GB)
**Database Version**: Neo4j 5.26.14 Community

---

## 1. DATABASE SUMMARY

| Metric | Count |
|--------|-------|
| **Total Nodes** | **1,618,130** |
| **Total Relationships** | **15,599,563** |
| **Node Labels** | 25 |
| **Relationship Types** | 3 |

---

## 2. NODE LABELS AND COUNTS

| Label | Count | Description |
|-------|-------|-------------|
| **CPE** | 1,309,730 | Common Platform Enumeration - Software/hardware identifiers |
| **CVE** | 307,322 | Common Vulnerabilities & Exposures |
| **CAPEC** | 706 | Common Attack Pattern Enumeration & Classification |
| **ThreatReport** | 276 | Threat intelligence reports |
| **Cybersecurity** | 29 | Cybersecurity concepts/entities |
| **Location** | 15 | Geographic locations |
| **Organization** | 11 | Organizations/vendors |
| **Equipment** | 10 | Industrial equipment |
| **CWE** | 10 | Common Weakness Enumeration |
| **TechnicalSpec** | 8 | Technical specifications |
| **AttackPattern** | - | MITRE ATT&CK patterns |
| **Document** | 4 | Reference documents |
| **CIM_Root** | 2 | IEC 61970 CIM ontology root |
| **SAREF_Root** | 2 | Smart Appliances REFerence ontology root |
| **GRID2ONTO_Root** | 2 | Grid ontology root |
| **CIM_PowerSystemResource** | 1 | CIM power system resource |
| **CIM_Equipment** | 1 | CIM equipment node |
| **SAREF_Device** | 1 | SAREF device node |
| **CAPEC_Category** | - | CAPEC attack categories |
| **CAPEC_View** | - | CAPEC hierarchical views |

---

## 3. RELATIONSHIP TYPES AND COUNTS

| Relationship | Count | Pattern |
|--------------|-------|---------|
| **MATCHES** | 15,599,445 | (CVE)-[:MATCHES]->(CPE) - CVE affects CPE |
| **MENTIONED_IN** | 106 | Entity mentioned in document |
| **RELATIONSHIP** | 12 | Generic relationship |

---

## 4. NODE PROPERTY SCHEMAS

### 4.1 CVE (Common Vulnerabilities & Exposures)
```
Properties:
  - cve_id: String           # CVE identifier (e.g., "CVE-2024-12345")
  - descriptions: List       # Vulnerability descriptions
  - severity: String         # CRITICAL, HIGH, MEDIUM, LOW, NONE, or ""
  - base_score: Float        # CVSS base score (0.0 - 10.0)
  - vector_string: String    # CVSS vector string
  - state: String            # Published, Reserved, etc.
  - year: Integer            # Publication year
  - date_published: DateTime # Publication date
  - date_updated: DateTime   # Last modification date
  - affected_products: List  # List of affected products
  - assigner_org: String     # Assigning CNA organization
  - assigner_name: String    # Assigner name
  - loaded_timestamp: DateTime
  - data_hash: String        # Data integrity hash

Constraints:
  - cve_id_unique: CVE.id IS UNIQUE

Indexes:
  - cve_id_idx on CVE.cve_id
  - cve_severity_idx on CVE.cvss31_baseSeverity
  - cve_published_idx on CVE.published
  - cve_modified_idx on CVE.lastModified
  - cve_year_idx on CVE.year
  - cve_state_idx on CVE.state
```

### CVE Severity Distribution
| Severity | Count | Percentage |
|----------|-------|------------|
| (empty/unknown) | 215,780 | 70.2% |
| MEDIUM | 44,812 | 14.6% |
| HIGH | 33,813 | 11.0% |
| CRITICAL | 6,879 | 2.2% |
| LOW | 6,019 | 2.0% |
| NONE | 19 | <0.1% |

### CVE Year Distribution (Top 15)
| Year | Count |
|------|-------|
| 2025 | 23,994 |
| 2024 | 38,594 |
| 2023 | 29,833 |
| 2022 | 26,716 |
| 2021 | 23,076 |
| 2020 | 20,607 |
| 2019 | 17,034 |
| 2018 | 17,495 |
| 2017 | 17,023 |
| 2016 | 10,560 |
| 2015 | 8,766 |
| 2014 | 8,998 |
| 2013 | 6,819 |
| 2012 | 5,936 |
| 2011 | 4,885 |

### 4.2 CPE (Common Platform Enumeration)
```
Properties:
  - cpeNameId: String        # Unique CPE identifier (UUID)
  - uri: String              # CPE URI format (cpe:2.3:...)
  - criteria: String         # Match criteria string
  - matchCriteriaId: String  # Matching criteria ID
  - status: String           # ACTIVE, DEPRECATED
  - vendor: String           # Vendor name
  - product: String          # Product name
  - created: DateTime        # Creation date
  - lastModified: DateTime   # Last modification date
  - cpeLastModified: DateTime

Constraints:
  - cpe_name_unique: CPE.cpeNameId IS UNIQUE
  - recovery_cpe_criteria_unique: CPE.criteria IS UNIQUE

Indexes:
  - cpe_modified_idx on CPE.lastModified
  - recovery_cpe_product_idx on CPE.product
  - recovery_cpe_vendor_idx on CPE.vendor
```

### 4.3 CAPEC (Common Attack Pattern Enumeration)
```
Properties:
  - id: String               # Internal ID
  - capec_id: String         # CAPEC identifier (e.g., "CAPEC-242")
  - attack_id: String        # Attack pattern ID
  - name: String             # Pattern name
  - description: String      # Full description
  - abstraction: String      # META, STANDARD, DETAILED
  - status: String           # Active status
  - severity: String         # Very High, High, Medium, Low
  - likelihood: String       # Likelihood of attack
  - likelihood_of_attack: String
  - typical_severity: String
  - properties_standardized: Map # Standardized properties

Constraints:
  - capec_pattern_id: CAPEC.id IS UNIQUE

Indexes:
  - capec_pattern_capec_id on CAPEC.capec_id
  - capec_pattern_name on CAPEC.name
  - capec_pattern_abstraction on CAPEC.abstraction
  - recovery_capec_id_idx on CAPEC.attack_id
```

### 4.4 CWE (Common Weakness Enumeration)
```
Properties:
  - id: String               # CWE identifier (e.g., "CWE-79")
  - name: String             # Weakness name
  - description: String      # Weakness description
  - source: String           # Data source
  - created: DateTime        # Creation date

Constraints:
  - cwe_id_unique: CWE.id IS UNIQUE
```

### 4.5 ThreatReport
```
Properties:
  - title: String            # Report title
  - summary: String          # Executive summary
  - content: String          # Full report content
  - content_type: String     # Type of content
  - threat_types: List       # Associated threat types
  - severity: String         # Report severity
  - source_file: String      # Source file path
  - processed_date: DateTime # Processing date
```

### 4.6 Equipment
```
Properties:
  - name: String             # Equipment name
  - type: String             # Equipment type
  - description: String      # Description
  - specifications: Map      # Technical specifications
  - security_features: List  # Security features
  - source_documents: List   # Source documentation
  - created: DateTime
  - updated: DateTime
```

### 4.7 Organization
```
Properties:
  - name: String             # Organization name
  - type: String             # Organization type
  - industry: String         # Industry sector
  - role: String             # Role (vendor, customer, etc.)
  - source_documents: List   # Source documentation
  - created: DateTime
  - updated: DateTime
```

### 4.8 Location
```
Properties:
  - name: String             # Location name
  - type: String             # Location type
  - region: String           # Geographic region
  - source_documents: List   # Source documentation
  - created: DateTime
  - updated: DateTime
```

### 4.9 Ontology Root Nodes
```
CIM_Root, SAREF_Root, GRID2ONTO_Root:
  - name: String             # Ontology name
  - version: String          # Ontology version
  - namespace: String        # Namespace URI
```

---

## 5. RELATIONSHIP SCHEMAS

### 5.1 MATCHES (CVE → CPE)
```cypher
(cve:CVE)-[:MATCHES]->(cpe:CPE)
```
**Purpose**: Links CVEs to affected software/hardware products
**Properties**: None (relationship is just a link)
**Count**: 15,599,445 relationships
**Average**: ~50 CPEs per CVE

### 5.2 MENTIONED_IN
```cypher
(:Entity)-[:MENTIONED_IN]->(:Document|ThreatReport)
```
**Purpose**: Links entities to documents that mention them
**Count**: 106 relationships

---

## 6. CONSTRAINTS SUMMARY

| Constraint Name | Entity | Property |
|----------------|--------|----------|
| cve_id_unique | CVE | id |
| cpe_name_unique | CPE | cpeNameId |
| recovery_cpe_criteria_unique | CPE | criteria |
| cwe_id_unique | CWE | id |
| capec_pattern_id | CAPEC | id |
| capec_category_id | CAPEC_Category | id |
| capec_view_id | CAPEC_View | id |

---

## 7. INDEXES SUMMARY

| Index Name | Entity | Property | Type |
|------------|--------|----------|------|
| cve_id_idx | CVE | cve_id | RANGE |
| cve_severity_idx | CVE | cvss31_baseSeverity | RANGE |
| cve_published_idx | CVE | published | RANGE |
| cve_modified_idx | CVE | lastModified | RANGE |
| cve_year_idx | CVE | year | RANGE |
| cve_state_idx | CVE | state | RANGE |
| cpe_name_unique | CPE | cpeNameId | RANGE |
| cpe_modified_idx | CPE | lastModified | RANGE |
| recovery_cpe_vendor_idx | CPE | vendor | RANGE |
| recovery_cpe_product_idx | CPE | product | RANGE |
| capec_pattern_id | CAPEC | id | RANGE |
| capec_pattern_capec_id | CAPEC | capec_id | RANGE |
| capec_pattern_name | CAPEC | name | RANGE |
| cwe_id_unique | CWE | id | RANGE |
| equipment_name_idx | Equipment | name | RANGE |
| organization_name_idx | Organization | name | RANGE |
| location_name_idx | Location | name | RANGE |
| cybersecurity_name_idx | Cybersecurity | name | RANGE |
| document_name_idx | Document | name | RANGE |
| technical_spec_name_idx | TechnicalSpec | name | RANGE |
| recovery_report_title_idx | ThreatReport | title | RANGE |

---

## 8. QUERY EXAMPLES

### Find Critical CVEs with Affected Products
```cypher
MATCH (cve:CVE)-[:MATCHES]->(cpe:CPE)
WHERE cve.severity = 'CRITICAL'
RETURN cve.cve_id, cve.base_score, count(cpe) AS affected_products
ORDER BY cve.base_score DESC
LIMIT 20
```

### Find CVEs by Product Vendor
```cypher
MATCH (cve:CVE)-[:MATCHES]->(cpe:CPE)
WHERE cpe.vendor = 'microsoft'
RETURN cve.cve_id, cve.severity, cpe.product
LIMIT 100
```

### CVE to Attack Pattern Chain (requires CAPEC linkage)
```cypher
MATCH (cve:CVE)
WHERE cve.descriptions CONTAINS 'injection'
WITH cve
MATCH (capec:CAPEC)
WHERE capec.name CONTAINS 'Injection'
RETURN cve.cve_id, capec.capec_id, capec.name
```

---

## 9. DATA QUALITY NOTES

### CVE Severity Gap
- 215,780 CVEs (70%) have empty severity
- These are primarily older CVEs without CVSS v3.1 scores
- Need enrichment from NVD API for cvssV3.1 scores

### Missing Relationships
- CVE → CWE relationships not populated
- CVE → CAPEC relationships not populated
- These need to be loaded from:
  - NVD API (CVE → CWE)
  - CAPEC repository (CWE → CAPEC)

### Ontology Stubs
- CIM, SAREF, GRID2ONTO ontologies have root nodes only
- Equipment hierarchy not fully populated
- Need ontology import for complete coverage

---

## 10. VOLUME INFORMATION

**Docker Volume**: `active_neo4j_data`
**Size**: 1.8 GB
**Created**: 2025-08-28

**Last Read Activity**:
- CVE index: 997,022 reads
- CPE index: 22,864,676 reads
- Relationship lookup: Active

---

**Document Version**: 1.0.0
**Generated By**: AEON Schema Discovery Agent
**Date**: 2025-11-26
