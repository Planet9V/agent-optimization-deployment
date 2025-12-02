# PROC-142: Vendor Equipment Mapping ETL

**File:** PROC-142-vendor-equipment.md
**Created:** 2025-11-26
**Version:** 1.0.0
**Enhancement:** E15 - Vendor Equipment Mapping
**Priority:** HIGH
**Frequency:** Quarterly
**Estimated Duration:** 4-6 hours

---

## Purpose

Extract, transform, and load vendor-specific equipment data (Siemens and Alstom) into Neo4j to enable precise equipment identification, vulnerability mapping, patch cycle tracking, and vendor comparison for OT/ICS security analysis.

**McKenney Question Mapping:**
- **Q4**: What specific ICS/OT equipment do we have? (Equipment inventory)
- **Q7**: Which vendors supply our critical systems? (Supply chain visibility)
- **Q8**: What are vendor patch cycles and security track records? (Vendor assessment)

---

## Pre-conditions

**Required Procedures:**
- PROC-001 (Neo4j Database Initialization)
- PROC-011 (MITRE ATT&CK ICS Import)

**Data Requirements:**
- Vendor dataset markdown files (Siemens: 8 files, Alstom: 10 files)
- Equipment inventory from CMDB (optional for cross-reference)
- CVE/NVD feeds for vulnerability mapping

**System Requirements:**
- Neo4j database operational
- Python 3.9+ with pandas, neo4j-driver
- 2GB RAM minimum
- Read access to `Vendor_Refinement_Datasets/` directory

---

## Data Sources

### Primary Sources

**Siemens Dataset** (`Vendor_Refinement_Datasets/Siemens/`)
- `siemens_atp_safety_systems.md` (24 KB) - Trainguard ATP family
- `siemens_etcs_signaling_systems.md` (19 KB) - ETCS integration
- `siemens_interlocking_systems.md` (23 KB) - S700K interlocking
- `siemens_vicos_operations_control.md` (23 KB) - VICOS operations
- `siemens_gsm_r_frmcs_communications.md` (23 KB) - Communication systems
- `siemens_signaling_x_digital_platform.md` (23 KB) - Digital platform
- `siemens_trainguard_cbtc_systems.md` (16 KB) - CBTC systems
- `siemens_global_projects_deployments.md` (21 KB) - Deployment data

**Alstom Dataset** (`Vendor_Refinement_Datasets/Alstom/`)
- `01_ETCS_ERTMS_Signaling_Systems.md` (26 KB) - Onvia/Atlas platforms
- `02_Interlocking_Systems.md` (25 KB) - Onvia Lock
- `03_CBTC_Urban_Transit_Systems.md` (24 KB) - CBTC systems
- `04_Control_Center_Systems.md` (24 KB) - Iconis Control Center
- `05_Trackside_Equipment_Infrastructure.md` (25 KB) - Balises, LEU
- `06_Rolling_Stock_Integration.md` (22 KB) - Onboard equipment
- `07_Communication_Protocols_Standards.md` (22 KB) - GSM-R, FRMCS
- `08_Global_Projects_Deployments.md` (21 KB) - Geographic deployment
- `09_Maintenance_Support_Services.md` (26 KB) - Service models
- `10_Safety_Security_Compliance.md` (26 KB) - CVE data, SIL ratings

---

## Transformation Logic

### 1. Equipment Model Node Creation

**Target Schema:**
```cypher
(:EquipmentModel {
  id: String,                    // "SIEMENS_TRAINGUARD_ATP"
  name: String,                  // "Trainguard ATP"
  vendor: String,                // "Siemens" | "Alstom"
  category: String,              // "ATP" | "ETCS" | "Interlocking" | "Communications"
  subcategory: String,           // "Base" | "Overlay" | "Integrated"
  sil_rating: String,            // "SIL 4" | "SIL 3" | "SIL 2"
  certifications: [String],      // ["CENELEC EN 50126", "EN 50128"]
  deployment_count: Integer,     // Estimated global installations
  maturity: String,              // "Mature" | "Mid-life" | "Early-stage"
  deployment_years: Integer,     // Years since initial deployment
  description: String
})
```

**Extraction Rules:**
- Parse markdown section headers for equipment categories
- Extract SIL ratings from safety-critical sections
- Identify deployment count from global projects files
- Calculate maturity: >12 years = "Mature", 7-11 years = "Mid-life", <7 years = "Early-stage"

### 2. Vulnerability Mapping

**Target Schema:**
```cypher
(:VulnerabilityPattern {
  id: String,                    // "VULN_S700K_TRAIN_DETECTION_SPOOF"
  equipment_model_id: String,    // Foreign key to EquipmentModel
  vulnerability_class: String,   // "Train detection spoofing"
  attack_vector: String,         // "Axle counter data injection"
  impact: String,                // "Allows trains to bypass conflict detection"
  cvss_score: Float,             // 9.1
  severity: String,              // "Critical" | "High" | "Medium" | "Low"
  remediation: String,           // "Firmware update to v7.2.5+"
  vendor_patch_date: Date,       // 2024-Q2
  still_deployed_percent: Float  // 0.12 (12%)
})
```

**Extraction Rules:**
- Parse "Vulnerability Windows" and "Vulnerability Patterns" sections
- Extract CVSS scores (format: "CVSS Score: 9.1 Critical")
- Map remediation info (firmware versions, patch dates)
- Estimate deployment percentage from text ("~12% of global installations")

### 3. Vendor Metadata

**Target Schema:**
```cypher
(:Vendor {
  name: String,                  // "Siemens" | "Alstom"
  division_revenue_usd: BigInt,  // 9000000000 (9B)
  total_cve_count: Integer,      // 23 (2020-2024)
  critical_high_percent: Float,  // 0.61 (61%)
  avg_patch_response_weeks: Integer,  // 12
  emergency_response_weeks: String,   // "2-4"
  patch_cycle: String,           // "Quarterly" | "Semi-annual"
  security_track_record: String, // "Good" | "Excellent"
  market_position: String,       // "Major player" | "Market leader"
  financial_stability: String    // "Excellent"
})
```

**Extraction Rules:**
- Parse vendor comparison sections
- Extract CVE counts from "Security Incidents" sections
- Calculate average patch response time from incident history
- Assess security track record based on disclosure process, response time

### 4. Equipment Integration Dependencies

**Target Schema:**
```cypher
(:EquipmentModel)-[:DEPENDS_ON {
  dependency_type: String,       // "input" | "output" | "bidirectional"
  interface_type: String,        // "Balise data" | "Signal aspects" | "Movement authority"
  safety_critical: Boolean,      // true for SIL 4 interfaces
  failure_cascade_risk: String   // "Compromise leads to..."
}]->(:EquipmentModel)
```

**Extraction Rules:**
- Parse "Equipment Integration Dependencies" sections
- Map "→" symbols to dependency relationships
- Identify bidirectional dependencies with "↔" symbols
- Extract "Vulnerability Cascade Path" for failure analysis

---

## Target Neo4j Schema

### Node Labels
- `:EquipmentModel` - Specific equipment products
- `:Vendor` - Equipment manufacturers (Siemens, Alstom)
- `:VulnerabilityPattern` - Equipment-specific vulnerabilities
- `:PatchCycle` - Vendor patch release schedules

### Relationships
- `(:EquipmentModel)-[:MANUFACTURED_BY]->(:Vendor)`
- `(:EquipmentModel)-[:HAS_VULNERABILITY]->(:VulnerabilityPattern)`
- `(:EquipmentModel)-[:DEPENDS_ON]->(:EquipmentModel)`
- `(:Vendor)-[:FOLLOWS_PATCH_CYCLE]->(:PatchCycle)`
- `(:VulnerabilityPattern)-[:REMEDIATED_BY_PATCH]->(:PatchCycle)`

---

## Execution Steps

### Step 1: Data Extraction (Python)

```python
import re
from pathlib import Path

def extract_siemens_equipment(data_dir):
    """Extract equipment models from Siemens dataset."""
    equipment_models = []

    # Parse ATP systems
    atp_file = Path(data_dir) / "Siemens" / "siemens_atp_safety_systems.md"
    content = atp_file.read_text()

    # Extract product lines
    product_pattern = r'\*\*Product Line: (.*?)\*\*'
    products = re.findall(product_pattern, content)

    for product in products:
        equipment_models.append({
            'id': f"SIEMENS_{product.replace(' ', '_').upper()}",
            'name': product,
            'vendor': 'Siemens',
            'category': 'ATP',
            'sil_rating': 'SIL 4',
            'certifications': ['CENELEC EN 50126', 'EN 50128', 'EN 50129']
        })

    # Extract vulnerabilities
    vuln_pattern = r'\*\*Known Vulnerability Class:\*\* (.*?)\n\*\*Attack Vector:\*\* (.*?)\n.*?CVSS Score:\*\* ([\d.]+) (\w+)'
    vulnerabilities = re.findall(vuln_pattern, content, re.DOTALL)

    return equipment_models, vulnerabilities

def extract_alstom_equipment(data_dir):
    """Extract equipment models from Alstom dataset."""
    equipment_models = []

    # Parse ETCS signaling systems
    etcs_file = Path(data_dir) / "Alstom" / "01_ETCS_ERTMS_Signaling_Systems.md"
    content = etcs_file.read_text()

    # Extract Onvia Control, Onvia Cab, Atlas Platform
    # ... (similar parsing logic)

    return equipment_models

# Execute extraction
siemens_equip, siemens_vulns = extract_siemens_equipment("/path/to/Vendor_Refinement_Datasets")
alstom_equip = extract_alstom_equipment("/path/to/Vendor_Refinement_Datasets")
```

### Step 2: Load Equipment Models to Neo4j

```cypher
// Create Vendor nodes
MERGE (s:Vendor {name: 'Siemens'})
SET s.division_revenue_usd = 9000000000,
    s.total_cve_count = 23,
    s.critical_high_percent = 0.61,
    s.avg_patch_response_weeks = 12,
    s.emergency_response_weeks = '2-4',
    s.patch_cycle = 'Quarterly',
    s.security_track_record = 'Good',
    s.financial_stability = 'Excellent';

MERGE (a:Vendor {name: 'Alstom'})
SET a.division_revenue_usd = 7000000000,
    a.total_cve_count = 31,
    a.critical_high_percent = 0.58,
    a.avg_patch_response_weeks = 10,
    a.emergency_response_weeks = '2-6',
    a.patch_cycle = 'Semi-annual',
    a.security_track_record = 'Good',
    a.financial_stability = 'Excellent';

// Load equipment models (parameterized)
UNWIND $equipment_models AS equip
MERGE (e:EquipmentModel {id: equip.id})
SET e.name = equip.name,
    e.vendor = equip.vendor,
    e.category = equip.category,
    e.subcategory = equip.subcategory,
    e.sil_rating = equip.sil_rating,
    e.certifications = equip.certifications,
    e.deployment_count = equip.deployment_count,
    e.maturity = equip.maturity,
    e.description = equip.description;

// Create vendor relationships
MATCH (e:EquipmentModel), (v:Vendor)
WHERE e.vendor = v.name
MERGE (e)-[:MANUFACTURED_BY]->(v);
```

### Step 3: Load Vulnerabilities

```cypher
// Load vulnerability patterns
UNWIND $vulnerabilities AS vuln
CREATE (v:VulnerabilityPattern {
  id: vuln.id,
  equipment_model_id: vuln.equipment_model_id,
  vulnerability_class: vuln.vulnerability_class,
  attack_vector: vuln.attack_vector,
  impact: vuln.impact,
  cvss_score: vuln.cvss_score,
  severity: vuln.severity,
  remediation: vuln.remediation,
  vendor_patch_date: date(vuln.vendor_patch_date),
  still_deployed_percent: vuln.still_deployed_percent
});

// Link vulnerabilities to equipment
MATCH (e:EquipmentModel), (v:VulnerabilityPattern)
WHERE e.id = v.equipment_model_id
MERGE (e)-[:HAS_VULNERABILITY]->(v);
```

### Step 4: Create Equipment Dependencies

```cypher
// Siemens dependencies example
MATCH (interlocking:EquipmentModel {id: 'SIEMENS_S700K'})
MATCH (atp:EquipmentModel {id: 'SIEMENS_TRAINGUARD_ATP'})
MERGE (interlocking)-[:DEPENDS_ON {
  dependency_type: 'output',
  interface_type: 'Balise data encoding',
  safety_critical: true,
  failure_cascade_risk: 'Incorrect balise data leads to ATP safety violation'
}]->(atp);

// Alstom dependencies example
MATCH (trackside:EquipmentModel {id: 'ALSTOM_ONVIA_CONTROL'})
MATCH (onboard:EquipmentModel {id: 'ALSTOM_ONVIA_CAB'})
MERGE (trackside)-[:DEPENDS_ON {
  dependency_type: 'bidirectional',
  interface_type: 'Movement authority via radio link',
  safety_critical: true,
  failure_cascade_risk: 'Communication compromise enables unauthorized movement authority'
}]->(onboard);
```

### Step 5: Link to ThreatActorProfile (Psychometric Connection)

```cypher
// Equipment vendors may be targeted by specific adversaries
// Link equipment to threat actor preferences based on sophistication
MATCH (equip:EquipmentModel)
MATCH (tap:ThreatActorProfile)
WHERE equip.sil_rating = 'SIL 4'
  AND tap.sophistication_level IN ['High', 'Nation-state']
MERGE (tap)-[:TARGETS_EQUIPMENT {
  motivation: 'High-value safety-critical systems',
  attack_difficulty: 'Very High',
  potential_impact: 'Catastrophic'
}]->(equip);
```

---

## Verification Queries

### Verify Equipment Model Count
```cypher
MATCH (e:EquipmentModel)
RETURN e.vendor, e.category, COUNT(*) as equipment_count
ORDER BY e.vendor, e.category;

// Expected: ~13 Siemens models, ~12 Alstom models (25 total)
```

### Verify Vulnerability Coverage
```cypher
MATCH (e:EquipmentModel)-[:HAS_VULNERABILITY]->(v:VulnerabilityPattern)
RETURN e.name, COUNT(v) as vulnerability_count,
       AVG(v.cvss_score) as avg_cvss_score
ORDER BY vulnerability_count DESC
LIMIT 10;

// Expected: Critical equipment (S700K, Atlas, Onvia Control) should have multiple vulnerabilities
```

### Verify Vendor Comparison Data
```cypher
MATCH (v:Vendor)
RETURN v.name,
       v.total_cve_count,
       v.avg_patch_response_weeks,
       v.security_track_record
ORDER BY v.avg_patch_response_weeks ASC;

// Expected: Alstom faster (10 weeks) than Siemens (12 weeks)
```

### Verify Equipment Dependencies
```cypher
MATCH (e1:EquipmentModel)-[d:DEPENDS_ON]->(e2:EquipmentModel)
WHERE d.safety_critical = true
RETURN e1.name, e2.name, d.interface_type, d.failure_cascade_risk
LIMIT 10;

// Expected: Interlocking → ATP, Trackside → Onboard dependencies present
```

---

## Rollback Procedure

```cypher
// Remove all equipment and vendor data
MATCH (e:EquipmentModel) DETACH DELETE e;
MATCH (v:VulnerabilityPattern) DETACH DELETE v;
MATCH (ven:Vendor) DETACH DELETE ven;
MATCH (pc:PatchCycle) DETACH DELETE pc;
```

---

## Post-Execution Validation

**Success Criteria:**
- [ ] 20-30 `:EquipmentModel` nodes created
- [ ] 2 `:Vendor` nodes (Siemens, Alstom) created
- [ ] 30-50 `:VulnerabilityPattern` nodes created
- [ ] 10-15 `:DEPENDS_ON` relationships established
- [ ] All equipment linked to vendors via `:MANUFACTURED_BY`
- [ ] Vendor CVE counts and patch cycles populated
- [ ] No orphan nodes (all equipment has vendor relationship)

**Data Quality Checks:**
- [ ] SIL ratings present for safety-critical equipment
- [ ] CVSS scores ≥ 7.0 for "High" severity vulnerabilities
- [ ] Vendor patch response times reasonable (2-15 weeks)
- [ ] Equipment deployment counts > 0 where specified

---

## Integration with McKenney Questions

**Q4 (Equipment Inventory):**
```cypher
// What equipment do we have?
MATCH (e:EquipmentModel)-[:MANUFACTURED_BY]->(v:Vendor)
RETURN v.name as vendor,
       e.category as equipment_type,
       e.name as model_name,
       e.sil_rating as safety_rating,
       e.maturity as lifecycle_stage
ORDER BY v.name, e.category;
```

**Q7 (Vendor Analysis):**
```cypher
// Assess vendor security track record
MATCH (v:Vendor)
RETURN v.name,
       v.security_track_record,
       v.total_cve_count,
       v.avg_patch_response_weeks,
       v.financial_stability
ORDER BY v.avg_patch_response_weeks ASC;
```

**Q8 (Vulnerability Management):**
```cypher
// What are critical vulnerabilities by vendor?
MATCH (v:Vendor)<-[:MANUFACTURED_BY]-(e:EquipmentModel)-[:HAS_VULNERABILITY]->(vp:VulnerabilityPattern)
WHERE vp.severity IN ['Critical', 'High']
RETURN v.name,
       COUNT(vp) as critical_vulns,
       AVG(vp.cvss_score) as avg_cvss,
       COLLECT(DISTINCT vp.vulnerability_class)[..5] as top_vuln_classes
ORDER BY critical_vulns DESC;
```

---

**Procedure Complete**: Equipment models, vulnerabilities, and vendor metadata loaded and linked to support OT/ICS threat analysis.
