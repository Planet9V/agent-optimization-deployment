# PHASE 2: DETAILED IMPLEMENTATION PLAN
## NER Enhancement & Neo4j Relationship Creation

**Document:** PHASE_2_DETAILED_IMPLEMENTATION_PLAN.md
**Created:** 2025-11-07
**Version:** 1.0.0
**Status:** ACTIVE
**AEON Protocol:** Phase 0 ✅ | Phase 1 ✅ | Phase 2 ✅ IN PROGRESS

---

## 📊 EXECUTIVE SUMMARY

**Objective:** Create 8-week implementation plan for NER model enhancement and Neo4j relationship creation to enable complete CVE→CWE→CAPEC→ATT&CK attack chain queries with 95%+ entity extraction accuracy.

**Current State (FACTS):**
- 316,552 CVEs in Neo4j with 100% EPSS coverage ✅
- 0 relationships between CVE→CWE→CAPEC→ATT&CK ❌
- NER model v6: 84.16% F1 on threat intel, 31.25% F1 on VULNERABILITY ❌
- 1,513 CVEs contain extractable "CWE-" text in descriptions ✅

**Expected Outcome:**
- 1,500+ CVE→CWE relationships created
- 600+ CWE→CAPEC relationships created
- 400+ CAPEC→ATT&CK relationships created
- 15K-30K SBOM→CVE relationships created
- NER v7 model: 95%+ F1 on VULNERABILITY, 87-90% overall F1

---

## 🗓️ WEEK-BY-WEEK IMPLEMENTATION

### **WEEK 1: CVE → CWE Relationship Extraction**

#### **Objective:** Extract CWE references from CVE descriptions and create relationships

**Prerequisites:**
- ✅ Neo4j database: bolt://localhost:7687
- ✅ Credentials: neo4j / neo4j@openspg
- ✅ 316,552 CVE nodes with description property
- ✅ 2,214 CWE nodes with cwe_id property

**Implementation Script:** `scripts/week1_cve_cwe_extraction.py`

```python
#!/usr/bin/env python3
"""
Week 1: CVE → CWE Relationship Extraction
Extracts CWE references from CVE descriptions using regex pattern matching.
"""
from neo4j import GraphDatabase
import re
from datetime import datetime

# Configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"

# CWE extraction patterns
CWE_PATTERNS = [
    r'CWE-(\d+)',                    # Standard: CWE-94
    r'CWE ID (\d+)',                 # Variant: CWE ID 94
    r'weakness.*?(\d{1,4})',         # Contextual: weakness 94
    r'classified as CWE-(\d+)',      # Explicit: classified as CWE-94
]

class CVECWEExtractor:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.stats = {
            'cves_processed': 0,
            'cves_with_cwe_text': 0,
            'cwe_ids_extracted': 0,
            'relationships_created': 0,
            'relationships_failed': 0,
            'unique_cwe_ids': set()
        }

    def extract_cwe_ids(self, description):
        """Extract all CWE IDs from a CVE description"""
        if not description:
            return []

        cwe_ids = set()
        for pattern in CWE_PATTERNS:
            matches = re.findall(pattern, description, re.IGNORECASE)
            for match in matches:
                # Validate CWE ID (typically 1-4 digits)
                try:
                    cwe_num = int(match)
                    if 1 <= cwe_num <= 9999:
                        cwe_ids.add(f"CWE-{cwe_num}")
                except ValueError:
                    continue

        return list(cwe_ids)

    def create_cve_cwe_relationships(self):
        """Extract CWE from CVE descriptions and create relationships"""
        print("=" * 80)
        print("CVE → CWE RELATIONSHIP EXTRACTION")
        print("=" * 80)

        with self.driver.session() as session:
            # Step 1: Get CVEs with "CWE" in description
            print("\n📊 Fetching CVEs with CWE references...")
            result = session.run("""
                MATCH (cve:CVE)
                WHERE cve.description CONTAINS 'CWE'
                RETURN cve.id AS cve_id, cve.description AS description
                LIMIT 2000  // Process in batches
            """)

            cves_to_process = [(record['cve_id'], record['description'])
                             for record in result]

            print(f"✅ Found {len(cves_to_process)} CVEs with CWE references")

            # Step 2: Extract CWE IDs and create relationships
            print("\n🔍 Extracting CWE IDs and creating relationships...")

            for cve_id, description in cves_to_process:
                self.stats['cves_processed'] += 1

                # Extract CWE IDs
                cwe_ids = self.extract_cwe_ids(description)

                if cwe_ids:
                    self.stats['cves_with_cwe_text'] += 1
                    self.stats['cwe_ids_extracted'] += len(cwe_ids)
                    self.stats['unique_cwe_ids'].update(cwe_ids)

                    # Create relationships
                    for cwe_id in cwe_ids:
                        try:
                            session.run("""
                                MATCH (cve:CVE {id: $cve_id})
                                MATCH (cwe:CWE {cwe_id: $cwe_id})
                                MERGE (cve)-[r:IS_WEAKNESS_TYPE]->(cwe)
                                RETURN r
                            """, cve_id=cve_id, cwe_id=cwe_id)

                            self.stats['relationships_created'] += 1
                        except Exception as e:
                            self.stats['relationships_failed'] += 1
                            print(f"  ⚠️ Failed {cve_id} → {cwe_id}: {e}")

                # Progress reporting
                if self.stats['cves_processed'] % 100 == 0:
                    print(f"  Progress: {self.stats['cves_processed']} CVEs processed, "
                          f"{self.stats['relationships_created']} relationships created")

    def validate_relationships(self):
        """Validate created relationships"""
        print("\n📊 Validating relationships...")

        with self.driver.session() as session:
            result = session.run("""
                MATCH (cve:CVE)-[r:IS_WEAKNESS_TYPE]->(cwe:CWE)
                RETURN count(r) AS total_relationships,
                       count(DISTINCT cve) AS unique_cves,
                       count(DISTINCT cwe) AS unique_cwes
            """)

            record = result.single()
            print(f"  ✅ Total relationships: {record['total_relationships']}")
            print(f"  ✅ Unique CVEs linked: {record['unique_cves']}")
            print(f"  ✅ Unique CWEs referenced: {record['unique_cwes']}")

    def generate_report(self):
        """Generate Week 1 completion report"""
        print("\n" + "=" * 80)
        print("WEEK 1 COMPLETION REPORT")
        print("=" * 80)
        print(f"\n📊 Processing Statistics:")
        print(f"  CVEs processed: {self.stats['cves_processed']}")
        print(f"  CVEs with CWE text: {self.stats['cves_with_cwe_text']}")
        print(f"  CWE IDs extracted: {self.stats['cwe_ids_extracted']}")
        print(f"  Unique CWE IDs: {len(self.stats['unique_cwe_ids'])}")
        print(f"\n🔗 Relationship Creation:")
        print(f"  Relationships created: {self.stats['relationships_created']}")
        print(f"  Relationships failed: {self.stats['relationships_failed']}")
        print(f"  Success rate: {self.stats['relationships_created'] / max(self.stats['cwe_ids_extracted'], 1) * 100:.1f}%")

        # Save report
        report = {
            'week': 1,
            'task': 'CVE → CWE Relationship Extraction',
            'completion_date': datetime.now().isoformat(),
            'statistics': self.stats,
            'status': 'COMPLETE'
        }

        import json
        with open('week1_completion_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"\n💾 Report saved to: week1_completion_report.json")

    def close(self):
        self.driver.close()

if __name__ == "__main__":
    extractor = CVECWEExtractor()
    try:
        extractor.create_cve_cwe_relationships()
        extractor.validate_relationships()
        extractor.generate_report()
    finally:
        extractor.close()
```

**Expected Outcomes:**
- ✅ 1,500-2,000 CVE→CWE relationships created
- ✅ Validation query confirms relationship count
- ✅ Week 1 completion report generated

**Validation Query:**
```cypher
MATCH (cve:CVE)-[r:IS_WEAKNESS_TYPE]->(cwe:CWE)
RETURN count(r) AS total,
       collect(DISTINCT cwe.cwe_id)[0..10] AS sample_cwes
```

---

### **WEEK 2: CWE → CAPEC → ATT&CK Mapping**

#### **Objective:** Map CWE weaknesses to CAPEC attack patterns and ATT&CK techniques

**Prerequisites:**
- ✅ CAPEC v3.9 XML downloaded
- ✅ 613 CAPEC nodes in Neo4j
- ✅ 834 AttackTechnique nodes in Neo4j
- ✅ Week 1 CVE→CWE relationships created

**Implementation Script:** `scripts/week2_cwe_capec_attack_mapping.py`

```python
#!/usr/bin/env python3
"""
Week 2: CWE → CAPEC → ATT&CK Mapping
Parses CAPEC XML and creates relationship graph.
"""
import xml.etree.ElementTree as ET
from neo4j import GraphDatabase
from pathlib import Path

class CAPECMapper:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "neo4j@openspg")
        )
        self.stats = {
            'cwe_capec_relationships': 0,
            'capec_technique_relationships': 0,
            'capec_entries_processed': 0
        }

    def parse_capec_xml(self, xml_path):
        """Parse CAPEC XML and extract relationships"""
        print("📄 Parsing CAPEC XML...")
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # XML namespace
        ns = {'capec': 'http://capec.mitre.org/capec-3'}

        mappings = []
        for attack_pattern in root.findall('.//capec:Attack_Pattern', ns):
            capec_id = attack_pattern.get('ID')
            capec_name = attack_pattern.get('Name')

            # Extract CWE relationships
            cwe_ids = []
            for weakness in attack_pattern.findall('.//capec:Related_Weakness', ns):
                cwe_id = weakness.get('CWE_ID')
                if cwe_id:
                    cwe_ids.append(f"CWE-{cwe_id}")

            # Extract ATT&CK technique mappings
            technique_ids = []
            for taxonomy in attack_pattern.findall('.//capec:Taxonomy_Mapping', ns):
                if taxonomy.get('Taxonomy_Name') == 'ATTACK':
                    technique_id = taxonomy.find('capec:Entry_ID', ns)
                    if technique_id is not None:
                        technique_ids.append(technique_id.text)

            if cwe_ids or technique_ids:
                mappings.append({
                    'capec_id': f"CAPEC-{capec_id}",
                    'capec_name': capec_name,
                    'cwe_ids': cwe_ids,
                    'technique_ids': technique_ids
                })
                self.stats['capec_entries_processed'] += 1

        print(f"✅ Processed {len(mappings)} CAPEC entries with relationships")
        return mappings

    def create_relationships(self, mappings):
        """Create CWE→CAPEC and CAPEC→Technique relationships"""
        print("\n🔗 Creating relationships...")

        with self.driver.session() as session:
            for mapping in mappings:
                capec_id = mapping['capec_id']

                # Create CWE → CAPEC relationships
                for cwe_id in mapping['cwe_ids']:
                    try:
                        session.run("""
                            MATCH (cwe:CWE {cwe_id: $cwe_id})
                            MATCH (capec:CAPEC {capecId: $capec_id})
                            MERGE (cwe)-[r:ENABLES_ATTACK_PATTERN]->(capec)
                            RETURN r
                        """, cwe_id=cwe_id, capec_id=capec_id)
                        self.stats['cwe_capec_relationships'] += 1
                    except Exception as e:
                        print(f"  ⚠️ Failed CWE→CAPEC: {cwe_id} → {capec_id}")

                # Create CAPEC → ATT&CK relationships
                for technique_id in mapping['technique_ids']:
                    try:
                        session.run("""
                            MATCH (capec:CAPEC {capecId: $capec_id})
                            MATCH (tech:AttackTechnique {technique_id: $technique_id})
                            MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(tech)
                            RETURN r
                        """, capec_id=capec_id, technique_id=technique_id)
                        self.stats['capec_technique_relationships'] += 1
                    except Exception as e:
                        print(f"  ⚠️ Failed CAPEC→Technique: {capec_id} → {technique_id}")

                if self.stats['capec_entries_processed'] % 50 == 0:
                    print(f"  Progress: {self.stats['capec_entries_processed']} entries, "
                          f"{self.stats['cwe_capec_relationships']} CWE→CAPEC, "
                          f"{self.stats['capec_technique_relationships']} CAPEC→Technique")

    def validate_attack_chains(self):
        """Validate complete CVE→CWE→CAPEC→ATT&CK chains"""
        print("\n🔍 Validating attack chains...")

        with self.driver.session() as session:
            result = session.run("""
                MATCH path = (cve:CVE)-[:IS_WEAKNESS_TYPE]->(cwe:CWE)
                             -[:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
                             -[:IMPLEMENTS_TECHNIQUE]->(tech:AttackTechnique)
                RETURN count(path) AS complete_chains,
                       count(DISTINCT cve) AS cves_with_chains
                LIMIT 1
            """)

            record = result.single()
            if record:
                print(f"  ✅ Complete attack chains: {record['complete_chains']}")
                print(f"  ✅ CVEs with complete chains: {record['cves_with_chains']}")

    def close(self):
        self.driver.close()

if __name__ == "__main__":
    mapper = CAPECMapper()
    try:
        # Download CAPEC XML if not present
        capec_xml = Path("/path/to/capec_v3.9.xml")  # UPDATE PATH

        if not capec_xml.exists():
            print("⚠️ CAPEC XML not found. Please download from:")
            print("   https://capec.mitre.org/data/xml/capec_v3.9.xml")
            exit(1)

        mappings = mapper.parse_capec_xml(capec_xml)
        mapper.create_relationships(mappings)
        mapper.validate_attack_chains()

        print(f"\n✅ Week 2 Complete:")
        print(f"  CWE→CAPEC relationships: {mapper.stats['cwe_capec_relationships']}")
        print(f"  CAPEC→Technique relationships: {mapper.stats['capec_technique_relationships']}")
    finally:
        mapper.close()
```

**Expected Outcomes:**
- ✅ 600-800 CWE→CAPEC relationships
- ✅ 400-600 CAPEC→Technique relationships
- ✅ Complete 4-hop attack chains queryable

---

### **WEEK 3: SBOM → CVE Component Matching**

#### **Objective:** Link SBOM components to vulnerabilities using CPE matching

**Implementation Script:** `scripts/week3_sbom_cve_matching.py`

```python
#!/usr/bin/env python3
"""
Week 3: SBOM → CVE Component Matching
Matches software components to CVEs using CPE URIs and fuzzy matching.
"""
from neo4j import GraphDatabase

class SBOMCVEMatcher:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=("neo4j", "neo4j@openspg")
        )
        self.stats = {
            'exact_matches': 0,
            'fuzzy_matches': 0,
            'failed_matches': 0
        }

    def create_exact_cpe_matches(self):
        """Match components to CVEs using exact CPE URI matching"""
        print("🔍 Creating exact CPE matches...")

        with self.driver.session() as session:
            result = session.run("""
                MATCH (comp:SoftwareComponent)
                WHERE comp.cpe_uri IS NOT NULL
                MATCH (cve:CVE)
                WHERE cve.cpe_uris CONTAINS comp.cpe_uri
                MERGE (comp)-[r:AFFECTED_BY_CVE]->(cve)
                RETURN count(r) AS total_matches
            """)

            record = result.single()
            self.stats['exact_matches'] = record['total_matches']
            print(f"  ✅ Exact matches: {self.stats['exact_matches']}")

    def create_fuzzy_vendor_product_matches(self):
        """Match using vendor/product name fuzzy matching"""
        print("\n🔍 Creating fuzzy vendor/product matches...")

        with self.driver.session() as session:
            result = session.run("""
                MATCH (comp:SoftwareComponent)
                WHERE comp.vendor IS NOT NULL AND comp.product IS NOT NULL
                MATCH (cve:CVE)
                WHERE toLower(cve.cpe_vendors[0]) = toLower(comp.vendor)
                  AND toLower(cve.cpe_products[0]) = toLower(comp.product)
                MERGE (comp)-[r:POTENTIALLY_AFFECTED_BY]->(cve)
                RETURN count(r) AS fuzzy_matches
            """)

            record = result.single()
            self.stats['fuzzy_matches'] = record['fuzzy_matches']
            print(f"  ✅ Fuzzy matches: {self.stats['fuzzy_matches']}")

    def validate_sbom_coverage(self):
        """Validate SBOM vulnerability coverage"""
        print("\n📊 Validating SBOM coverage...")

        with self.driver.session() as session:
            result = session.run("""
                MATCH (comp:SoftwareComponent)
                OPTIONAL MATCH (comp)-[r:AFFECTED_BY_CVE|POTENTIALLY_AFFECTED_BY]->(cve:CVE)
                WITH comp, count(r) AS vuln_count
                RETURN count(comp) AS total_components,
                       sum(CASE WHEN vuln_count > 0 THEN 1 ELSE 0 END) AS components_with_vulns,
                       avg(vuln_count) AS avg_vulns_per_component
            """)

            record = result.single()
            print(f"  ✅ Total components: {record['total_components']}")
            print(f"  ✅ Components with vulnerabilities: {record['components_with_vulns']}")
            print(f"  ✅ Avg vulnerabilities per component: {record['avg_vulns_per_component']:.1f}")

    def close(self):
        self.driver.close()

if __name__ == "__main__":
    matcher = SBOMCVEMatcher()
    try:
        matcher.create_exact_cpe_matches()
        matcher.create_fuzzy_vendor_product_matches()
        matcher.validate_sbom_coverage()

        print(f"\n✅ Week 3 Complete:")
        print(f"  Total relationships: {matcher.stats['exact_matches'] + matcher.stats['fuzzy_matches']}")
    finally:
        matcher.close()
```

**Expected Outcomes:**
- ✅ 15K-30K SBOM→CVE relationships
- ✅ Vulnerability impact analysis queryable

---

## 🧠 WEEKS 4-8: NER MODEL v7 TRAINING

### **WEEK 4-5: Training Data Creation**

**Objective:** Create 7,050 new training samples from CVE/CWE/CAPEC/ATT&CK data

**Data Sources:**
1. **NVD API** (5,000 CVE samples)
2. **CWE XML v4.18** (900 samples)
3. **CAPEC XML v3.9** (550 samples)
4. **MITRE ATT&CK** (600 samples)

**Implementation:** Full training data creation pipeline in separate document

---

### **WEEK 6: Pattern Priority Fix & Code Updates**

**File:** `/home/jim/2_OXOT_Projects_Dev/10_Ontologies/1_Working_Directory_2025_OCT_30/Training_Preparartion/scripts/ner_training_pipeline.py`

**Changes Required:**

```python
# Lines 168-178: Update entity priority hierarchy
PRIORITY = {
    'VULNERABILITY': 1,     # ⬆️ HIGHEST PRIORITY (was 5)
    'WEAKNESS': 2,          # ⬆️ SECOND (was 6)
    'SOFTWARE_COMPONENT': 3,
    'HARDWARE_COMPONENT': 4,
    'EQUIPMENT': 5,         # ⬇️ MOVED DOWN (was 1)
    'PROTOCOL': 6,
    'VENDOR': 7,
    'SUPPLIER': 8,
    # ... rest unchanged
}
```

**Validation Test:**
```python
# Test CVE recognition
test_cases = [
    ("CVE-2022-22954 is a vulnerability", "VULNERABILITY"),
    ("CWE-94 is a weakness", "WEAKNESS"),
    ("CVE-2021-44228 affects Log4j", "VULNERABILITY")
]

for text, expected_label in test_cases:
    doc = nlp(text)
    assert any(ent.label_ == expected_label for ent in doc.ents), \
        f"Failed: {text} should extract {expected_label}"
```

---

### **WEEK 7-8: Model Retraining & Validation**

**Training Configuration:**
- Corpus: 7,473 samples (423 existing + 7,050 new)
- Entity types: 24 (unchanged)
- Iterations: 50
- Expected duration: 26 hours

**Validation Criteria:**
- ✅ VULNERABILITY F1 ≥ 90%
- ✅ WEAKNESS F1 ≥ 95%
- ✅ Overall F1 ≥ 85%
- ✅ CVE recognition rate ≥ 95%
- ✅ Threat intel F1 maintained ≥ 84%

---

## 📊 SUCCESS METRICS

### **Week 3 Checkpoint:**
```cypher
// Validate relationship creation
MATCH (cve:CVE)-[r1:IS_WEAKNESS_TYPE]->(cwe:CWE)
     -[r2:ENABLES_ATTACK_PATTERN]->(capec:CAPEC)
     -[r3:IMPLEMENTS_TECHNIQUE]->(tech:AttackTechnique)
RETURN count(r1) AS cve_cwe_relationships,
       count(r2) AS cwe_capec_relationships,
       count(r3) AS capec_technique_relationships,
       count(DISTINCT cve) AS cves_with_chains
```

**Expected:**
- CVE→CWE: 1,500+
- CWE→CAPEC: 600-800
- CAPEC→Technique: 400-600
- CVEs with complete chains: 500-1,000

### **Week 8 Checkpoint:**
```python
# NER model v7 validation
{
  "vulnerability_f1": ">= 0.95",
  "weakness_f1": ">= 0.97",
  "overall_f1": ">= 0.85",
  "cve_recognition_rate": ">= 0.95",
  "threat_intel_f1": ">= 0.84"  # Maintained from v6
}
```

---

## 🚀 DEPLOYMENT CHECKLIST

**Before Production:**
- [ ] All relationship counts validated
- [ ] NER model v7 passes all validation tests
- [ ] No regression on v6 high-performing entities
- [ ] Attack chain queries return expected results
- [ ] SBOM vulnerability mapping functional
- [ ] Documentation updated
- [ ] Backup of v6 model created

**Post-Deployment:**
- [ ] Monitor Neo4j query performance
- [ ] Track NER extraction accuracy on new documents
- [ ] Collect feedback on attack chain usefulness
- [ ] Plan monthly model retraining with new CVEs

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-07
**Next Review:** Week 3 checkpoint (relationship validation)
**Owner:** NER Enhancement Team
