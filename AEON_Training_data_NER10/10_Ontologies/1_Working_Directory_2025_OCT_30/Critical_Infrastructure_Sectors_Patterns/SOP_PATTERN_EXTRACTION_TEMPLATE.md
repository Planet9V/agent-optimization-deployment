# Pattern Extraction Template SOP
# Standard Operating Procedure for Critical Infrastructure Sector Pattern Extraction

**Version:** 1.0
**Date:** 2025-11-05
**Purpose:** Extract entity patterns from sector markdown files for spaCy EntityRuler
**Target:** 70+ patterns minimum per sector across 7 category files
**Validated:** Dams Sector (298 patterns extracted)

---

## Executive Summary

This SOP defines the procedure for extracting entity patterns from Critical Infrastructure sector documentation files and organizing them into structured YAML files for Natural Language Processing (NLP) entity recognition using spaCy's EntityRuler.

**Key Objectives:**
- Extract 70+ unique entity patterns per sector
- Categorize patterns into 7 standardized files
- Ensure patterns are sector-specific and actionable
- Maintain consistent YAML format for spaCy compatibility
- Enable parallel extraction for efficiency

**Success Metrics:**
- Pattern count: ≥70 total patterns per sector
- Category coverage: All 7 YAML files created
- Pattern quality: Exact entity names (not generic terms)
- Format validation: Valid YAML structure
- Extraction time: 15-20 minutes per sector

---

## 1. Source File Organization

### 1.1 Expected Directory Structure

Each sector should have documentation organized as follows:

```
Critical_Infrastructure_Sectors_Patterns/
├── {sector_name}/
│   ├── documentation/          # Source markdown files (15 files typical)
│   │   ├── standards/         # Industry standards, regulations
│   │   ├── vendors/           # Vendor-specific documentation
│   │   ├── equipment/         # Equipment specifications
│   │   ├── protocols/         # Communication protocols
│   │   ├── architectures/     # System architectures
│   │   ├── operations/        # Operational procedures
│   │   └── security/          # Security vulnerabilities, controls
│   ├── patterns/              # OUTPUT: Generated YAML files (7 files)
│   │   ├── standards.yaml
│   │   ├── vendors.yaml
│   │   ├── equipment.yaml
│   │   ├── protocols.yaml
│   │   ├── architectures.yaml
│   │   ├── operations.yaml
│   │   └── security.yaml
│   └── validation/            # Validation reports, logs
```

### 1.2 File Categories and Expected Content

| Category | Typical File Count | Content Types |
|----------|-------------------|---------------|
| **standards/** | 2-3 files | Industry standards (FEMA, ICOLD, IEEE), regulatory frameworks, compliance requirements |
| **vendors/** | 2-3 files | Vendor names, product lines, manufacturer-specific equipment |
| **equipment/** | 2-3 files | Physical equipment, components, sensors, controllers |
| **protocols/** | 2-3 files | Communication protocols (Modbus, DNP3, IEC 61850), network standards |
| **architectures/** | 2-3 files | System architectures, network topologies, control system layers |
| **operations/** | 2-3 files | Operational procedures, inspection types, emergency response |
| **security/** | 2-3 files | Vulnerabilities, attack vectors, security controls, CVEs |

**Total Expected:** 15 markdown files per sector

---

## 2. Pattern Extraction Procedure

### 2.1 Step-by-Step Process

#### **STEP 1: Identify Sector Directory**
```bash
# Navigate to sector directory
cd /path/to/Critical_Infrastructure_Sectors_Patterns/{sector_name}/documentation
```

#### **STEP 2: Inventory Source Files**
```bash
# List all markdown files
find . -type f -name "*.md" | sort

# Expected output: 15 markdown files organized by category
```

#### **STEP 3: Extract Entity Patterns**

For each markdown file, identify and extract:

**Entity Types to Extract:**
- **STANDARD** - Industry standards, regulations (e.g., "FEMA P-936", "ICOLD Bulletin", "IEEE C37.102")
- **VENDOR** - Company names, manufacturers (e.g., "Andritz", "ABB", "Voith GmbH")
- **EQUIPMENT** - Physical devices, machinery (e.g., "Francis Turbine", "PLC", "Hydroelectric Generator")
- **COMPONENT** - Parts, subassemblies (e.g., "Rotor", "Stator", "Runner Blade")
- **PROTOCOL** - Communication protocols (e.g., "Modbus TCP", "IEC 61850", "DNP3")
- **ARCHITECTURE** - System designs (e.g., "Hierarchical Architecture", "SCADA Network")
- **OPERATION** - Procedures, activities (e.g., "Daily Inspection", "Emergency Shutdown")
- **VULNERABILITY** - Security weaknesses (e.g., "Default Credentials", "PLC Exploit")
- **SECURITY_CONTROL** - Protection measures (e.g., "Network Segmentation", "Multi-factor Authentication")
- **CVE** - Specific vulnerabilities (e.g., "CVE-2021-44228")

**Extraction Rules:**
1. Extract **exact entity names** - not generic terms
2. Include **variants and abbreviations** (e.g., "PLC" and "Programmable Logic Controller")
3. Capture **model numbers** where present (e.g., "ABB RED670", "Voith V-F800")
4. Extract **full names and acronyms** (e.g., "IEC 61850" and "International Electrotechnical Commission 61850")
5. Include **industry-specific terminology** (e.g., "Wicket Gate", "Penstock", "Draft Tube")

#### **STEP 4: Categorize Patterns by Type**

Organize extracted patterns into 7 categories:

| Output File | Entity Types Included | Example Patterns |
|-------------|----------------------|------------------|
| **standards.yaml** | STANDARD, COMPONENT (structural), VENDOR (standards-related) | "FEMA P-936", "ICOLD", "Concrete Arch Dam", "Leica Geosystems" |
| **vendors.yaml** | VENDOR, EQUIPMENT (vendor-specific), PROTOCOL (vendor products) | "Andritz", "ABB", "Francis Turbine", "Modbus TCP" |
| **equipment.yaml** | EQUIPMENT, COMPONENT, VENDOR (manufacturers) | "Hydroelectric Generator", "PLC", "Stator", "Rotor", "ABB" |
| **protocols.yaml** | PROTOCOL, PROTOCOL_FEATURE, COMPONENT (protocol elements), STANDARD | "Modbus RTU", "IEC 61850", "GOOSE", "Holding Registers" |
| **architectures.yaml** | ARCHITECTURE, ARCHITECTURE_LAYER, NETWORK_COMPONENT, CONTROL_SYSTEM | "Hierarchical Architecture", "SCADA Network", "DMZ", "PLC" |
| **operations.yaml** | OPERATION, OPERATIONAL_PROCEDURE, INSPECTION_TARGET, EMERGENCY_TYPE, CORRECTIVE_ACTION | "Daily Inspection", "Emergency Shutdown", "Turbines", "Structural Failure" |
| **security.yaml** | VULNERABILITY, VULNERABILITY_CATEGORY, ATTACK_VECTOR, SECURITY_CONTROL, PHYSICAL_SECURITY, CVE | "PLC Exploit", "Network-based Attack", "Multi-factor Authentication", "CVE-2021-44228" |

#### **STEP 5: Create YAML Files**

For each category, create a YAML file in the `patterns/` directory.

**YAML Structure:**
```yaml
# {Category} Patterns
# Extracted from: {source_files}
# Date: {YYYY-MM-DD}

patterns:
  # {Subcategory or Source Context}
  - label: "{ENTITY_TYPE}"
    pattern: "{Entity Name}"
  - label: "{ENTITY_TYPE}"
    pattern: "{Entity Name Variant}"
```

**Example from standards.yaml:**
```yaml
patterns:
  # FEMA Standards
  - label: "STANDARD"
    pattern: "FEMA P-936"
  - label: "STANDARD"
    pattern: "Dam Safety Program Guidelines"
  - label: "STANDARD"
    pattern: "FEMA National Dam Safety Program"

  # Equipment from Standards Documentation
  - label: "EQUIPMENT"
    pattern: "Piezometers"
  - label: "EQUIPMENT"
    pattern: "Settlement gauges"

  # Vendors from Standards Documentation
  - label: "VENDOR"
    pattern: "Leica Geosystems"
  - label: "VENDOR"
    pattern: "Trimble"
```

#### **STEP 6: Validate Pattern Count**

**Validation Criteria:**
```bash
# Count patterns per file
for file in patterns/*.yaml; do
  echo "$(basename $file): $(grep -c '  - label:' $file) patterns"
done

# Total pattern count
find patterns/ -name "*.yaml" -exec grep -c '  - label:' {} \; | awk '{sum+=$1} END {print "Total patterns:", sum}'
```

**Success Threshold:** ≥70 total patterns across all 7 files

---

## 3. YAML Pattern Format Specification

### 3.1 File Header
```yaml
# {Category} Patterns
# Extracted from: {list of source .md files}
# Date: {YYYY-MM-DD}
```

### 3.2 Pattern Entry Structure
```yaml
patterns:
  - label: "{ENTITY_TYPE}"
    pattern: "{Exact Entity Name}"
```

### 3.3 Pattern Organization

**Group patterns by:**
1. **Source context** (vendor, standard, document type)
2. **Functional category** (equipment type, protocol family)
3. **Logical relationship** (component hierarchy, system layers)

**Example - Organized by Vendor:**
```yaml
patterns:
  # Andritz Vendor
  - label: "VENDOR"
    pattern: "Andritz"
  - label: "VENDOR"
    pattern: "Andritz AG"
  - label: "EQUIPMENT"
    pattern: "Francis Turbine"
  - label: "EQUIPMENT"
    pattern: "Kaplan Turbine"
  - label: "EQUIPMENT"
    pattern: "Andritz HydroControl"

  # ABB Vendor
  - label: "VENDOR"
    pattern: "ABB"
  - label: "EQUIPMENT"
    pattern: "Ability System 800xA"
  - label: "EQUIPMENT"
    pattern: "RED670"
```

### 3.4 Entity Type Examples

#### **STANDARD** - Industry Standards and Regulations
```yaml
- label: "STANDARD"
  pattern: "FEMA P-936"
- label: "STANDARD"
  pattern: "ICOLD Bulletin"
- label: "STANDARD"
  pattern: "IEEE C37.102"
- label: "STANDARD"
  pattern: "IEC 61850"
- label: "STANDARD"
  pattern: "NIST SP 800-82"
```

#### **VENDOR** - Manufacturers and Companies
```yaml
- label: "VENDOR"
  pattern: "Andritz"
- label: "VENDOR"
  pattern: "ABB"
- label: "VENDOR"
  pattern: "Voith GmbH"
- label: "VENDOR"
  pattern: "Siemens"
- label: "VENDOR"
  pattern: "Schneider Electric"
```

#### **EQUIPMENT** - Physical Devices
```yaml
- label: "EQUIPMENT"
  pattern: "Francis Turbine"
- label: "EQUIPMENT"
  pattern: "Programmable Logic Controller"
- label: "EQUIPMENT"
  pattern: "PLC"
- label: "EQUIPMENT"
  pattern: "Hydroelectric Generator"
- label: "EQUIPMENT"
  pattern: "SCADA System"
```

#### **COMPONENT** - Parts and Subassemblies
```yaml
- label: "COMPONENT"
  pattern: "Rotor"
- label: "COMPONENT"
  pattern: "Stator"
- label: "COMPONENT"
  pattern: "Runner Blade"
- label: "COMPONENT"
  pattern: "Wicket Gate"
- label: "COMPONENT"
  pattern: "Penstock"
```

#### **PROTOCOL** - Communication Protocols
```yaml
- label: "PROTOCOL"
  pattern: "Modbus"
- label: "PROTOCOL"
  pattern: "Modbus TCP"
- label: "PROTOCOL"
  pattern: "IEC 61850"
- label: "PROTOCOL"
  pattern: "DNP3"
- label: "PROTOCOL"
  pattern: "OPC UA"
```

#### **ARCHITECTURE** - System Designs
```yaml
- label: "ARCHITECTURE"
  pattern: "Hierarchical Architecture"
- label: "ARCHITECTURE"
  pattern: "Cyber-Physical System"
- label: "ARCHITECTURE_LAYER"
  pattern: "Supervisory Control Layer"
- label: "NETWORK_COMPONENT"
  pattern: "SCADA Network"
```

#### **OPERATION** - Procedures and Activities
```yaml
- label: "OPERATION"
  pattern: "Daily Inspection"
- label: "OPERATION"
  pattern: "Emergency Shutdown"
- label: "OPERATIONAL_PROCEDURE"
  pattern: "Start Sequence"
- label: "EMERGENCY_TYPE"
  pattern: "Structural Failure"
```

#### **VULNERABILITY** - Security Weaknesses
```yaml
- label: "VULNERABILITY"
  pattern: "Default Credentials"
- label: "VULNERABILITY"
  pattern: "PLC Exploit"
- label: "VULNERABILITY_CATEGORY"
  pattern: "SCADA System Vulnerability"
- label: "CVE"
  pattern: "CVE-2021-44228"
```

#### **SECURITY_CONTROL** - Protection Measures
```yaml
- label: "SECURITY_CONTROL"
  pattern: "Network Segmentation"
- label: "SECURITY_CONTROL"
  pattern: "Multi-factor Authentication"
- label: "SECURITY_MITIGATION"
  pattern: "SIEM Solution"
- label: "PHYSICAL_SECURITY"
  pattern: "CCTV Monitoring"
```

---

## 4. Quality Guidelines

### 4.1 Pattern Quality Standards

**DO Extract:**
- Exact entity names: "ABB RED670", "Andritz Francis Turbine"
- Variants and abbreviations: "PLC" + "Programmable Logic Controller"
- Model numbers: "V-F800", "System 800xA"
- Full standard names: "FEMA P-936", "IEEE C37.102"
- Industry-specific terms: "Wicket Gate", "Draft Tube", "GOOSE Protocol"

**DON'T Extract:**
- Generic terms: "device", "system", "network" (unless part of specific name)
- Common words: "control", "monitoring", "safety" (unless part of technical term)
- Descriptive phrases: "high-performance system", "reliable equipment"
- Action verbs: "operate", "inspect", "monitor" (unless part of procedure name)

### 4.2 Labeling Consistency

**Use consistent labels across sectors:**
- **STANDARD** - not "REGULATION", "GUIDELINE", "SPECIFICATION"
- **VENDOR** - not "MANUFACTURER", "COMPANY", "SUPPLIER"
- **EQUIPMENT** - not "DEVICE", "MACHINE", "HARDWARE"
- **PROTOCOL** - not "COMMUNICATION_METHOD", "INTERFACE"

**Exception:** Use specific subtypes when meaningful:
- PROTOCOL_FEATURE (e.g., "GOOSE", "Sampled Values")
- VULNERABILITY_CATEGORY vs. VULNERABILITY
- ARCHITECTURE_LAYER vs. ARCHITECTURE

### 4.3 Pattern Validation Checklist

Before finalizing patterns, verify:

- [ ] Pattern exists in source documentation
- [ ] Pattern is sector-specific (not generic IT term)
- [ ] Label matches entity type accurately
- [ ] Variants included (acronyms, full names)
- [ ] YAML syntax is valid (proper indentation, no syntax errors)
- [ ] Patterns are organized by logical grouping
- [ ] Total pattern count meets minimum threshold (≥70)

---

## 5. Parallel Extraction Strategy

For efficiency, divide extraction work among multiple agents or processors.

### 5.1 File Allocation Strategy

**3-Agent Parallel Extraction:**

```yaml
Extractor_1_Assignment:
  files:
    - standards/*.md (2-3 files)
    - vendors/*.md (2-3 files)
  output:
    - standards.yaml (30-40 patterns)
    - vendors.yaml (40-55 patterns)
  estimated_time: 15 minutes

Extractor_2_Assignment:
  files:
    - equipment/*.md (2-3 files)
    - protocols/*.md (2-3 files)
  output:
    - equipment.yaml (25-35 patterns)
    - protocols.yaml (25-35 patterns)
  estimated_time: 15 minutes

Extractor_3_Assignment:
  files:
    - architectures/*.md (2-3 files)
    - operations/*.md (2-3 files)
    - security/*.md (2-3 files)
  output:
    - architectures.yaml (35-45 patterns)
    - operations.yaml (40-55 patterns)
    - security.yaml (40-55 patterns)
  estimated_time: 20 minutes
```

### 5.2 Merge and Validation Process

1. **Concurrent Extraction:** All extractors work in parallel
2. **Pattern Collection:** Each extractor writes to assigned YAML files
3. **Cross-Reference Check:** Verify no duplicate patterns across files
4. **Consolidation:** Merge patterns if overlap exists between categories
5. **Final Validation:** Run pattern count and YAML syntax validation

**Total Estimated Time:** 20 minutes (parallel) vs. 50 minutes (sequential)

---

## 6. Success Criteria

### 6.1 Quantitative Metrics

| Metric | Target | Validation Method |
|--------|--------|-------------------|
| **Total Patterns** | ≥70 patterns | `find patterns/ -name "*.yaml" -exec grep -c '  - label:' {} \; \| awk '{sum+=$1} END {print sum}'` |
| **Files Created** | 7 YAML files | `ls patterns/*.yaml \| wc -l` |
| **YAML Validity** | 100% valid | `yamllint patterns/*.yaml` |
| **Pattern Uniqueness** | ≥95% unique | Manual inspection |
| **Source Coverage** | ≥80% files used | Compare file list to pattern comments |

### 6.2 Qualitative Standards

- **Relevance:** All patterns are sector-specific and actionable
- **Accuracy:** Patterns match source file content exactly
- **Completeness:** All major entities from source files captured
- **Organization:** Patterns logically grouped within files
- **Documentation:** Each file includes source references and date

### 6.3 Validation Commands

```bash
# Navigate to patterns directory
cd /path/to/{sector_name}/patterns

# Count patterns per file
for file in *.yaml; do
  count=$(grep -c '  - label:' "$file")
  echo "$file: $count patterns"
done

# Total pattern count
total=$(find . -name "*.yaml" -exec grep -c '  - label:' {} \; | awk '{sum+=$1} END {print sum}')
echo "Total patterns extracted: $total"

# Validate YAML syntax (requires yamllint)
yamllint *.yaml

# Check for empty files
for file in *.yaml; do
  if [ ! -s "$file" ]; then
    echo "WARNING: $file is empty"
  fi
done
```

**Success Threshold:**
- Total patterns ≥70
- All 7 YAML files present and non-empty
- No YAML syntax errors

---

## 7. Dams Sector Example (Reference Implementation)

### 7.1 Dams Sector Statistics

**Source Files:** 15 markdown files
**Patterns Extracted:** 298 patterns
**Extraction Time:** 18 minutes (parallel with 3 agents)

**Pattern Distribution:**

| File | Pattern Count | Key Entity Types |
|------|--------------|------------------|
| **standards.yaml** | 40 | STANDARD (FEMA, ICOLD, IEEE), EQUIPMENT (sensors), VENDOR (monitoring vendors), COMPONENT (dam types) |
| **vendors.yaml** | 55 | VENDOR (Andritz, ABB, Voith), EQUIPMENT (turbines, generators, control systems), PROTOCOL |
| **equipment.yaml** | 29 | EQUIPMENT (generators, turbines, PLCs), COMPONENT (stator, rotor, blades), VENDOR |
| **protocols.yaml** | 30 | PROTOCOL (Modbus, IEC 61850), PROTOCOL_FEATURE (GOOSE, MMS), COMPONENT (registers, logical nodes) |
| **architectures.yaml** | 42 | ARCHITECTURE (system designs), ARCHITECTURE_LAYER (control layers), NETWORK_COMPONENT (DMZ, SCADA), CONTROL_SYSTEM (PLC, RTU, HMI) |
| **operations.yaml** | 51 | OPERATION (inspections), OPERATIONAL_PROCEDURE (start/stop sequences), EMERGENCY_TYPE (structural failure), CORRECTIVE_ACTION (repairs) |
| **security.yaml** | 51 | VULNERABILITY (exploits), VULNERABILITY_CATEGORY, ATTACK_VECTOR, SECURITY_CONTROL (segmentation, MFA), CVE references |

**Total:** 298 patterns (424% of minimum requirement)

### 7.2 Sample Pattern Extraction

**Source File:** `facility-hydroelectric-20250102-05.md`

**Extracted Patterns:**
```yaml
# From architectures.yaml
- label: "ARCHITECTURE"
  pattern: "Hydroelectric Dam Facility Architecture"
- label: "FACILITY_COMPONENT"
  pattern: "Water Intake Structure"
- label: "FACILITY_COMPONENT"
  pattern: "Power House Structure"
- label: "FACILITY_COMPONENT"
  pattern: "Turbine Hall"
- label: "FACILITY_COMPONENT"
  pattern: "Control Room"

# From vendors.yaml
- label: "VENDOR"
  pattern: "Andritz"
- label: "EQUIPMENT"
  pattern: "Francis Turbine"
- label: "EQUIPMENT"
  pattern: "Andritz HydroControl"
- label: "PROTOCOL"
  pattern: "IEC 61850"

# From security.yaml
- label: "VULNERABILITY_CATEGORY"
  pattern: "SCADA System Vulnerability"
- label: "SECURITY_CONTROL"
  pattern: "Network Segmentation"
```

### 7.3 Lessons Learned from Dams Sector

**Successful Practices:**
1. **Parallel extraction** reduced time by 62% (50min → 18min)
2. **Vendor-centric organization** captured equipment-vendor relationships
3. **Including variants** (PLC + Programmable Logic Controller) improved recall
4. **Grouping by source context** made patterns easier to review
5. **Cross-category entities** (vendors in standards.yaml) improved completeness

**Challenges Addressed:**
1. **Duplicate patterns** - Resolved by assigning categories to specific extractors
2. **Label inconsistency** - Standardized labels across all files
3. **Generic terms** - Filtered during quality review phase
4. **Missing variants** - Added post-extraction review step

---

## 8. Usage Instructions for Remaining Sectors

### 8.1 Sector Checklist

Apply this SOP to the following 15 remaining sectors:

- [ ] Chemical
- [ ] Commercial Facilities
- [ ] Communications
- [ ] Critical Manufacturing
- [ ] Defense Industrial Base
- [ ] Emergency Services
- [ ] Energy
- [ ] Financial Services
- [ ] Food and Agriculture
- [ ] Government Facilities
- [ ] Healthcare and Public Health
- [ ] Information Technology
- [ ] Nuclear Reactors, Materials, and Waste
- [ ] Transportation Systems
- [ ] Water and Wastewater Systems

### 8.2 Sector-Specific Adaptations

**Adjust extraction focus based on sector:**

- **Energy:** Emphasize power generation equipment, grid protocols
- **Healthcare:** Medical devices, HL7/FHIR protocols, HIPAA standards
- **Transportation:** Vehicle systems, traffic control, GPS protocols
- **Water:** Treatment processes, distribution systems, quality monitoring
- **IT:** Network equipment, cybersecurity tools, enterprise protocols

**Pattern count targets may vary:**
- Complex sectors (Energy, IT): Target 100+ patterns
- Specialized sectors (Nuclear, Defense): Target 80+ patterns
- Smaller sectors (Emergency Services): Target 70+ patterns

### 8.3 Execution Command Template

```bash
# Step 1: Navigate to sector directory
cd /path/to/Critical_Infrastructure_Sectors_Patterns/{sector_name}

# Step 2: Create patterns directory if it doesn't exist
mkdir -p patterns

# Step 3: Spawn 3 parallel extractors (using Claude Code Task tool)
# Extractor 1: standards + vendors
# Extractor 2: equipment + protocols
# Extractor 3: architectures + operations + security

# Step 4: Validate output
cd patterns
for file in *.yaml; do
  count=$(grep -c '  - label:' "$file")
  echo "$file: $count patterns"
done

# Step 5: Total count verification
total=$(find . -name "*.yaml" -exec grep -c '  - label:' {} \; | awk '{sum+=$1} END {print sum}')
echo "Total patterns extracted: $total"

# Success criteria: total >= 70
```

---

## 9. Troubleshooting Guide

### 9.1 Common Issues

**Issue:** Pattern count below 70

**Solutions:**
- Review source files for missed entities
- Include equipment variants and model numbers
- Add protocol features (GOOSE, MMS, function codes)
- Extract component-level patterns (parts, subassemblies)
- Include legacy system names and versions

**Issue:** YAML syntax errors

**Solutions:**
- Validate indentation (2 spaces per level)
- Ensure proper dash and colon placement
- Quote patterns with special characters
- Remove trailing spaces
- Use `yamllint` for detailed error messages

**Issue:** Duplicate patterns across files

**Solutions:**
- Assign clear category ownership to extractors
- Cross-reference check during merge phase
- Consolidate duplicates into most appropriate file
- Document cross-category entities in comments

**Issue:** Generic patterns extracted

**Solutions:**
- Filter during quality review
- Apply "exact entity name" rule strictly
- Remove common IT terms without sector context
- Verify pattern appears in source documentation

### 9.2 Quality Improvement Tips

1. **Read source files completely** - Don't rely on headers/titles only
2. **Extract from code blocks and tables** - Rich source of equipment names
3. **Include abbreviations** - Critical for entity matching
4. **Use consistent casing** - Match source documentation exactly
5. **Group logically** - Organize patterns by vendor, system, or function
6. **Add comments** - Reference source files for traceability

---

## 10. Appendix

### 10.1 YAML Syntax Reference

```yaml
# File Header
# {Category} Patterns
# Extracted from: file1.md, file2.md
# Date: YYYY-MM-DD

patterns:
  # Section Comment
  - label: "ENTITY_TYPE"
    pattern: "Entity Name"
  - label: "ENTITY_TYPE"
    pattern: "Another Entity"

  # Another Section
  - label: "DIFFERENT_TYPE"
    pattern: "Different Entity"
```

**Syntax Rules:**
- Use 2-space indentation (no tabs)
- Each pattern entry starts with `- label:`
- Pattern field on next line with same indentation
- Comments start with `#`
- Quotes around string values (label, pattern)

### 10.2 Validation Script

```bash
#!/bin/bash
# validate_patterns.sh
# Validates pattern extraction for a sector

SECTOR_DIR="$1"

if [ -z "$SECTOR_DIR" ]; then
  echo "Usage: $0 <sector_directory>"
  exit 1
fi

cd "$SECTOR_DIR/patterns" || exit 1

echo "=== Pattern Extraction Validation ==="
echo "Sector: $(basename $(dirname $(pwd)))"
echo "Date: $(date '+%Y-%m-%d')"
echo ""

# Check file count
file_count=$(ls *.yaml 2>/dev/null | wc -l)
echo "YAML Files: $file_count / 7"

if [ "$file_count" -ne 7 ]; then
  echo "WARNING: Expected 7 YAML files, found $file_count"
fi

echo ""
echo "=== Pattern Counts ==="

total=0
for file in *.yaml; do
  if [ -f "$file" ]; then
    count=$(grep -c '^  - label:' "$file")
    total=$((total + count))
    printf "%-25s %3d patterns\n" "$file" "$count"
  fi
done

echo "-----------------------------------"
printf "%-25s %3d patterns\n" "TOTAL" "$total"
echo ""

# Success/failure
if [ "$total" -ge 70 ]; then
  echo "✓ SUCCESS: Pattern count meets minimum requirement (≥70)"
else
  echo "✗ FAILURE: Pattern count below minimum requirement (<70)"
fi

# YAML syntax validation (requires yamllint)
if command -v yamllint &> /dev/null; then
  echo ""
  echo "=== YAML Syntax Validation ==="
  yamllint *.yaml
else
  echo ""
  echo "WARNING: yamllint not installed, skipping syntax validation"
fi
```

### 10.3 Quick Reference Card

**Pattern Extraction Quick Steps:**
1. Navigate to `{sector}/documentation/`
2. Read all 15 markdown files
3. Extract 70+ entity patterns
4. Categorize into 7 YAML files
5. Validate count: `grep -c '  - label:' patterns/*.yaml`
6. Check syntax: `yamllint patterns/*.yaml`

**Common Entity Types:**
- STANDARD, VENDOR, EQUIPMENT, COMPONENT
- PROTOCOL, ARCHITECTURE, OPERATION, VULNERABILITY

**Success Criteria:**
- 7 YAML files created
- ≥70 total patterns
- Valid YAML syntax
- Patterns match source files

---

## Document Control

**Version History:**
- v1.0 (2025-11-05): Initial SOP created based on Dams Sector extraction

**References:**
- spaCy EntityRuler Documentation: https://spacy.io/usage/rule-based-matching
- Dams Sector Patterns: `/Critical_Infrastructure_Sectors_Patterns/dams/patterns/`

**Contact:**
For questions or improvements to this SOP, document feedback in the sector's `validation/` directory.

---

**END OF SOP**
