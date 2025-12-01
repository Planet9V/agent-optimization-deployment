# Standard Sector Deployment Procedure

**Document Type**: Technical Reference & Standard Operating Procedure
**Version**: 1.0 (based on Week 12-14 deployment patterns)
**Last Updated**: 2025-01-13
**Status**: ✅ ESTABLISHED STANDARD

---

## Executive Summary

This document defines the **standard 3-phase deployment procedure** for deploying CISA critical infrastructure sectors to the GAP-004 Universal Location Architecture. The methodology is based on successful deployment patterns from Weeks 1-14, covering 7 sectors and 4,000+ equipment nodes.

### Key Principles

1. **Phased Approach**: Equipment → Relationships → Tagging (distinct phases with validation gates)
2. **Data Quality First**: 100% completion required at each phase before proceeding
3. **Database-Query-First**: Always query for actual node IDs before creating relationships
4. **Comprehensive Tagging**: 5-dimensional tag system applied universally
5. **Automated Validation**: Built-in validation and cleanup at each phase

### Success Metrics (Week 12-14 Benchmark)

- **Deployment Success Rate**: 100%
- **Error Rate**: 0% (post-cleanup)
- **Average Tags per Equipment**: 13.75
- **Relationship Integrity**: 1:1 equipment-facility mapping
- **Processing Rate**: 379-411 tags/minute

---

## Phase 1: Equipment Node Creation

### Objective
Create equipment nodes with complete attributes and base tagging.

### Prerequisites
- [ ] Sector requirements analysis completed
- [ ] Equipment taxonomy defined
- [ ] Equipment ID range allocated (e.g., EQ-HEALTH-30001 to EQ-HEALTH-30500)
- [ ] Equipment count confirmed (must match facility capacity)
- [ ] Neo4j database accessible and operational

### Input Requirements

**Equipment Data Schema**:
```python
{
    'equipmentId': 'EQ-[SECTOR]-[NUMBER]',  # Unique identifier
    'name': 'Equipment Name',                # Human-readable name
    'equipmentType': 'Type Category',        # From sector taxonomy
    'manufacturer': 'Manufacturer Name',     # Vendor information
    'model': 'Model Number',                 # Model designation
    'serial_number': 'Serial Number',        # Unique serial
    'installation_date': 'YYYY-MM-DD',       # Installation date
    'operational_status': 'active|standby|maintenance',  # Current status
    'criticality_level': 'critical|high|medium|low',     # Criticality
    'tags': ['BASE_TAG_1', 'BASE_TAG_2'],    # Initial sector tags
    'created_date': 'datetime()',            # Creation timestamp
    'updated_date': 'datetime()'             # Last update timestamp
}
```

### Equipment Taxonomy Examples

**Healthcare Sector**:
- Medical Imaging (MRI, CT, X-Ray)
- Life Support (Ventilators, Dialysis)
- Laboratory Equipment (Analyzers, Centrifuges)
- Surgical Equipment (Surgical Robots, Lasers)
- Patient Monitoring (Telemetry, Vital Signs)
- Sterilization (Autoclaves, UV Systems)

**Chemical Sector**:
- Reactor Vessels
- Storage Tanks
- Process Control Systems
- Safety Monitoring Systems
- Hazmat Handling Equipment
- Ventilation Systems
- Emergency Shutdown Systems
- Leak Detection Systems

**Manufacturing Sector**:
- CNC Machines
- Industrial Robots
- Welding Equipment
- Assembly Line Systems
- Quality Control Equipment
- Material Handling Systems
- HVAC Systems
- Safety Systems

### Execution Steps

#### Step 1.1: Generate Equipment Records
```python
import subprocess

equipment_types = ['Type1', 'Type2', 'Type3', 'Type4', 'Type5', 'Type6']
equipment_count = 500  # Adjust based on sector requirements

for i in range(1, equipment_count + 1):
    eq_type = equipment_types[(i-1) % len(equipment_types)]
    criticality = ['critical', 'high', 'medium', 'low'][i % 4]
    status = ['active', 'standby', 'maintenance'][i % 3]

    query = f"""
CREATE (eq:Equipment {{
  equipmentId: 'EQ-SECTOR-{30000 + i}',
  name: '{eq_type} Unit {i}',
  equipmentType: '{eq_type}',
  manufacturer: 'Manufacturer-{eq_type}',
  model: '{eq_type}-2024',
  serial_number: 'SN-S-{100000 + i}',
  installation_date: date('2024-01-01'),
  operational_status: '{status}',
  criticality_level: '{criticality}',
  tags: ['SECTOR_EQUIP', 'SECTOR_BASE'],
  created_date: datetime(),
  updated_date: datetime()
}});
"""

    result = subprocess.run(
        ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', query],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        count += 1
        if count % 50 == 0:
            print(f"Created {count}/{equipment_count} equipment...")
    else:
        print(f"ERROR creating equipment {i}: {result.stderr}")
        # Log error and continue or halt based on policy
```

#### Step 1.2: Progress Tracking
- Report progress every 50 equipment (10% increments for 500 equipment)
- Log all errors to `phase1_errors.log`
- Maintain running count of successful creations

#### Step 1.3: Validation Query
```cypher
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-SECTOR-'
RETURN COUNT(eq) AS equipment_count
```

**Expected Result**: `equipment_count` = target count (e.g., 500)

**Validation Criteria**:
- ✅ Equipment count matches target exactly
- ✅ All equipment have required attributes populated
- ✅ Base tags present on all equipment
- ✅ No duplicate equipment IDs

### Phase 1 Completion Checklist
- [ ] All equipment nodes created (count verified)
- [ ] No creation errors logged
- [ ] Base tags applied to all equipment
- [ ] Equipment IDs follow standard format
- [ ] Validation query confirms exact count
- [ ] Phase 1 completion documented

### Common Issues and Resolutions

**Issue**: Equipment creation fails silently (returncode=0 but node not created)
- **Cause**: Syntax error in Cypher query, invalid data types
- **Resolution**: Test query in cypher-shell directly, validate data types

**Issue**: Duplicate equipment IDs
- **Cause**: Script re-run without cleanup
- **Resolution**: Check for existing equipment before creation, use unique constraints

**Issue**: Incomplete attributes
- **Cause**: Missing data in source, incorrect variable substitution
- **Resolution**: Validate all required fields before query execution

---

## Phase 2: LOCATED_AT Relationship Creation

### Objective
Connect equipment nodes to facility nodes with location metadata, establishing 1:1 equipment-facility mapping.

### Prerequisites
- [ ] Phase 1 completed successfully (all equipment nodes created)
- [ ] Facility nodes exist in database (validated)
- [ ] Equipment-to-facility distribution plan defined
- [ ] Location zone/bay naming scheme established

### Critical Anti-Pattern (DO NOT DO)

❌ **WRONG: Hardcoded Facility Lists**
```python
# ANTI-PATTERN - DO NOT USE
facilities = [
    "HEALTH-NY-001", "HEALTH-LA-001", "HEALTH-CHI-001"
]
# Problem: Facility nodes may not exist or IDs may have changed
```

✅ **CORRECT: Database-Query-First Approach**
```python
def get_facilities_from_db(facility_prefix):
    """Query database for actual facility IDs"""
    query = f"""
MATCH (f:Facility)
WHERE f.facilityId STARTS WITH '{facility_prefix}'
RETURN f.facilityId
ORDER BY f.facilityId;
"""
    result = subprocess.run(
        ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', query],
        capture_output=True,
        text=True
    )

    facilities = []
    for line in result.stdout.strip().split('\n')[1:]:  # Skip header
        fac_id = line.strip().strip('"')
        if fac_id and not fac_id.startswith('f.facilityId'):
            facilities.append(fac_id)

    return facilities
```

### Execution Steps

#### Step 2.1: Query Facilities from Database
```python
facilities = get_facilities_from_db('HEALTH-')
print(f"Found {len(facilities)} facilities in database")

if len(facilities) == 0:
    print("❌ ERROR: No facilities found! Cannot proceed with Phase 2.")
    exit(1)
```

#### Step 2.2: Identify Equipment Without Relationships
```python
check_query = f"""
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
  AND NOT (eq)-[:LOCATED_AT]->()
RETURN eq.equipmentId
ORDER BY eq.equipmentId;
"""

result = subprocess.run(
    ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', check_query],
    capture_output=True,
    text=True
)

missing_equipment = []
for line in result.stdout.strip().split('\n')[1:]:
    eq_id = line.strip().strip('"')
    if eq_id and not eq_id.startswith('eq.equipmentId'):
        missing_equipment.append(eq_id)

print(f"Found {len(missing_equipment)} equipment without relationships")
```

#### Step 2.3: Distribute Equipment Across Facilities
```python
relationships_created = 0

for idx, eq_id in enumerate(missing_equipment):
    # Round-robin distribution across facilities
    fac_id = facilities[idx % len(facilities)]

    # Zone assignment (facility-specific logic)
    zone_num = (idx // len(facilities)) + 1

    query = f"""
MATCH (eq:Equipment {{equipmentId: '{eq_id}'}}), (f:Facility {{facilityId: '{fac_id}'}})
CREATE (eq)-[:LOCATED_AT {{
  installation_date: eq.installation_date,
  location: 'Zone {zone_num}',
  exact_coordinates: point({{latitude: f.latitude + 0.0005, longitude: f.longitude + 0.0005}})
}}]->(f);
"""

    result = subprocess.run(
        ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', query],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        relationships_created += 1
        if relationships_created % 50 == 0:
            print(f"Created {relationships_created}/{len(missing_equipment)} relationships...")
    else:
        print(f"ERROR for {eq_id} → {fac_id}: {result.stderr}")

print(f"✅ Relationships created: {relationships_created}/{len(missing_equipment)}")
```

### Relationship Properties

**Required Properties**:
- `installation_date`: Date equipment was installed (from equipment node)
- `location`: Zone, bay, or specific location within facility (e.g., "Zone 1", "Bay A3")
- `exact_coordinates`: Neo4j point type with latitude/longitude (facility coordinates + small offset)

**Optional Properties**:
- `installation_technician`: Technician who performed installation
- `commissioning_date`: Date equipment was commissioned
- `last_maintenance_date`: Most recent maintenance activity
- `access_level`: Required access level for this equipment location

### Validation Queries

#### Validation 2.1: Relationship Count Verification
```cypher
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
RETURN COUNT(r) AS total_relationships,
       COUNT(DISTINCT eq) AS unique_equipment,
       COUNT(DISTINCT f) AS unique_facilities
```

**Expected Result**: `total_relationships` = `unique_equipment` (1:1 mapping)

#### Validation 2.2: Duplicate Relationship Detection
```cypher
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
WITH eq, collect(r) AS rels
WHERE size(rels) > 1
RETURN eq.equipmentId, size(rels) AS duplicate_count
ORDER BY duplicate_count DESC
```

**Expected Result**: 0 rows (no duplicates)

If duplicates detected, proceed to Phase 2.4 (Cleanup).

#### Validation 2.3: Orphaned Equipment Detection
```cypher
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
  AND NOT (eq)-[:LOCATED_AT]->()
RETURN COUNT(eq) AS orphaned_equipment
```

**Expected Result**: `orphaned_equipment` = 0

### Duplicate Relationship Cleanup

**Cleanup Pattern** (if validation 2.2 detects duplicates):
```python
cleanup_script = """
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
WITH eq, r, f
ORDER BY id(r)
WITH eq, collect(r) AS rels
WHERE size(rels) > 1
FOREACH (rel IN tail(rels) | DELETE rel)
"""

result = subprocess.run(
    ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', cleanup_script],
    capture_output=True,
    text=True
)

# Re-run validation 2.2 to confirm cleanup
```

**Cleanup Strategy**: Keep first relationship (by internal ID), delete all subsequent duplicates.

### Phase 2 Completion Checklist
- [ ] All equipment have LOCATED_AT relationships (verified)
- [ ] No duplicate relationships (validated)
- [ ] 1:1 equipment-facility mapping achieved
- [ ] Relationship properties correctly populated
- [ ] No orphaned equipment detected
- [ ] Phase 2 completion documented

### Common Issues and Resolutions

**Issue**: Relationships not created (returncode=0 but relationship missing)
- **Cause**: Equipment or Facility node doesn't exist
- **Resolution**: Verify both nodes exist before MATCH, use database-query-first approach

**Issue**: Duplicate relationships
- **Cause**: Script re-run, parallel execution overlap
- **Resolution**: Run cleanup script (FOREACH pattern), prevent re-runs without cleanup

**Issue**: Uneven distribution (some facilities have 0 equipment)
- **Cause**: Modulo distribution doesn't account for facility capacity
- **Resolution**: Use weighted distribution based on facility size

---

## Phase 3: 5-Dimensional Tagging

### Objective
Apply comprehensive multi-dimensional tags to all equipment for rich querying and analysis.

### Prerequisites
- [ ] Phase 2 completed successfully (all relationships created)
- [ ] 5-dimensional tag schemas defined for sector
- [ ] Geographic state-to-region mapping established
- [ ] Regulatory framework mapping documented
- [ ] Equipment-to-technical-capability mapping defined

### 5-Dimensional Tag System

#### Dimension 1: GEO (Geographic)
**Purpose**: Enable location-based queries and regional analysis

**Tag Structure**:
- `GEO_STATE_[STATE]`: 2-letter state code (e.g., `GEO_STATE_CA`, `GEO_STATE_NY`)
- `GEO_REGION_[REGION]`: Regional grouping (e.g., `GEO_REGION_WEST_COAST`, `GEO_REGION_SOUTH`)

**State-to-Region Mapping** (standardized across all sectors):
```python
state_to_region = {
    'CA': 'WEST_COAST',
    'OR': 'NORTHWEST', 'WA': 'NORTHWEST',
    'TX': 'SOUTH', 'LA': 'SOUTH', 'AL': 'SOUTH', 'MS': 'SOUTH', 'FL': 'SOUTH',
    'GA': 'SOUTH', 'TN': 'SOUTH', 'KY': 'SOUTH', 'SC': 'SOUTH', 'NC': 'SOUTH',
    'VA': 'SOUTH', 'OK': 'SOUTH',
    'MI': 'MIDWEST', 'OH': 'MIDWEST', 'IN': 'MIDWEST', 'IL': 'MIDWEST',
    'MO': 'MIDWEST', 'WI': 'MIDWEST', 'IA': 'MIDWEST', 'KS': 'MIDWEST',
    'NE': 'MIDWEST', 'MN': 'MIDWEST',
    'NY': 'NORTHEAST', 'PA': 'NORTHEAST', 'NJ': 'NORTHEAST', 'MA': 'NORTHEAST',
    'CT': 'NORTHEAST', 'ME': 'NORTHEAST',
    'AZ': 'MOUNTAIN', 'CO': 'MOUNTAIN', 'UT': 'MOUNTAIN', 'NV': 'MOUNTAIN',
    'MT': 'MOUNTAIN'
}
```

#### Dimension 2: OPS (Operational)
**Purpose**: Enable facility-type and functional queries

**Tag Structure**:
- `OPS_FACILITY_[TYPE]`: Facility type classification
- `OPS_FUNCTION_[FUNCTION]`: Operational function

**Sector-Specific Examples**:

**Healthcare**:
- Facility: `OPS_FACILITY_HOSPITAL`, `OPS_FACILITY_MEDICAL_CENTER`, `OPS_FACILITY_URGENT_CARE`
- Function: `OPS_FUNCTION_PATIENT_CARE`, `OPS_FUNCTION_EMERGENCY`, `OPS_FUNCTION_DIAGNOSTICS`

**Chemical**:
- Facility: `OPS_FACILITY_MANUFACTURING`, `OPS_FACILITY_PETROCHEMICAL`, `OPS_FACILITY_PHARMA`
- Function: `OPS_FUNCTION_CHEMICAL_PRODUCTION`, `OPS_FUNCTION_REFINING`, `OPS_FUNCTION_DRUG_PRODUCTION`

**Manufacturing**:
- Facility: `OPS_FACILITY_AUTOMOTIVE`, `OPS_FACILITY_AEROSPACE`, `OPS_FACILITY_STEEL_MILL`
- Function: `OPS_FUNCTION_VEHICLE_ASSEMBLY`, `OPS_FUNCTION_AIRCRAFT_PRODUCTION`, `OPS_FUNCTION_METAL_PRODUCTION`

#### Dimension 3: REG (Regulatory)
**Purpose**: Enable compliance and regulatory framework queries

**Tag Structure**:
- `REG_[AGENCY]_[REGULATION]`: Specific regulation or compliance framework

**Sector-Specific Examples**:

**Healthcare**:
- `REG_HIPAA_COMPLIANCE`: HIPAA privacy and security rules
- `REG_FDA_REGULATION`: FDA oversight and regulations
- `REG_STATE_HEALTH`: State health department regulations
- `REG_CMS_COMPLIANCE`: Medicare/Medicaid compliance
- `REG_JOINT_COMMISSION`: Joint Commission accreditation

**Chemical**:
- `REG_EPA_CAA`: Clean Air Act
- `REG_EPA_RCRA`: Resource Conservation and Recovery Act
- `REG_OSHA_PSM`: Process Safety Management
- `REG_EPA_RMP`: Risk Management Program
- `REG_DHS_CFATS`: Chemical Facility Anti-Terrorism Standards

**Manufacturing**:
- `REG_OSHA_MANUFACTURING`: OSHA manufacturing safety
- `REG_EPA_AIR_QUALITY`: EPA air quality standards
- `REG_DOD_CMMC`: DoD Cybersecurity Maturity Model Certification
- `REG_ITAR_COMPLIANCE`: International Traffic in Arms Regulations
- `REG_ISO_9001`: ISO 9001 quality management

#### Dimension 4: TECH (Technical)
**Purpose**: Enable equipment-type and capability queries

**Tag Structure**:
- `TECH_EQUIP_[TYPE]`: Equipment type classification
- `TECH_[CAPABILITY]`: Technical capability or function

**Equipment-to-Technical Mapping**:
```python
tech_mapping = {
    # Healthcare
    'Medical Imaging': ['TECH_EQUIP_IMAGING', 'TECH_DIAGNOSTICS'],
    'Life Support': ['TECH_EQUIP_LIFE_SUPPORT', 'TECH_CRITICAL_CARE'],
    'Laboratory Equipment': ['TECH_EQUIP_LAB', 'TECH_ANALYSIS'],

    # Chemical
    'Reactor Vessels': ['TECH_EQUIP_REACTOR', 'TECH_PROCESS_CONTROL'],
    'Storage Tanks': ['TECH_EQUIP_STORAGE', 'TECH_CONTAINMENT'],
    'Process Control': ['TECH_EQUIP_CONTROL', 'TECH_AUTOMATION'],

    # Manufacturing
    'CNC Machines': ['TECH_EQUIP_CNC', 'TECH_PRECISION_MACHINING'],
    'Industrial Robots': ['TECH_EQUIP_ROBOTICS', 'TECH_AUTOMATION'],
    'Welding': ['TECH_EQUIP_WELDING', 'TECH_JOINING']
}
```

#### Dimension 5: TIME (Temporal)
**Purpose**: Enable era and maintenance priority queries

**Tag Structure**:
- `TIME_ERA_[ERA]`: Operational era (e.g., `TIME_ERA_CURRENT`)
- `TIME_MAINT_PRIORITY_[LEVEL]`: Maintenance priority level

**Standard TIME Tags**:
- `TIME_ERA_CURRENT`: Current operational era (all equipment)
- `TIME_MAINT_PRIORITY_CRITICAL`: Critical maintenance priority (Healthcare, Chemical)
- `TIME_MAINT_PRIORITY_HIGH`: High maintenance priority (Manufacturing)
- `TIME_MAINT_PRIORITY_MEDIUM`: Medium maintenance priority
- `TIME_MAINT_PRIORITY_LOW`: Low maintenance priority

### Execution Steps

#### Step 3.1: Query Equipment with Facility Context
```python
get_equipment_query = f"""
MATCH (eq:Equipment)-[:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
RETURN eq.equipmentId AS eqId,
       eq.equipmentType AS eqType,
       f.state AS state,
       f.facilityType AS facType
ORDER BY eq.equipmentId;
"""

result = subprocess.run(
    ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', get_equipment_query],
    capture_output=True,
    text=True
)

# Parse results
lines = [l.strip() for l in result.stdout.strip().split('\n')[1:] if l.strip() and not l.startswith('eq')]
```

#### Step 3.2: Build Tag Arrays
```python
for line in lines:
    parts = [p.strip().strip('"') for p in line.split(',')]
    if len(parts) < 4:
        continue

    eq_id, eq_type, state, fac_type = parts[0], parts[1], parts[2], parts[3]

    # Initialize with base tags
    tags = ['HEALTHCARE_EQUIP', 'SECTOR_HEALTHCARE']

    # GEO tags
    if state in state_to_region:
        tags.extend([
            f'GEO_REGION_{state_to_region[state]}',
            f'GEO_STATE_{state}'
        ])

    # OPS tags (sector-specific logic)
    if 'Hospital' in fac_type:
        tags.extend(['OPS_FACILITY_HOSPITAL', 'OPS_FUNCTION_PATIENT_CARE'])
    elif 'Medical Center' in fac_type:
        tags.extend(['OPS_FACILITY_MEDICAL_CENTER', 'OPS_FUNCTION_HEALTHCARE'])

    # REG tags (sector-specific)
    tags.extend(['REG_HIPAA_COMPLIANCE', 'REG_FDA_REGULATION', 'REG_STATE_HEALTH'])
    if 'Hospital' in fac_type or 'Medical Center' in fac_type:
        tags.extend(['REG_CMS_COMPLIANCE', 'REG_JOINT_COMMISSION'])

    # TECH tags (equipment-specific)
    if eq_type in tech_mapping:
        tags.extend(tech_mapping[eq_type])

    # TIME tags
    tags.extend(['TIME_ERA_CURRENT', 'TIME_MAINT_PRIORITY_CRITICAL'])
```

#### Step 3.3: Apply Tags to Equipment
```python
    # Apply complete tag array
    tags_json = json.dumps(tags)
    update_query = f"""
MATCH (eq:Equipment {{equipmentId: '{eq_id}'}})
SET eq.tags = {tags_json};
"""

    result = subprocess.run(
        ['docker', 'exec', 'openspg-neo4j', 'cypher-shell', '-u', 'neo4j', '-p', 'neo4j@openspg', update_query],
        capture_output=True,
        text=True
    )

    tagged_count += 1
    if tagged_count % 50 == 0:
        print(f"Tagged {tagged_count} equipment...")
```

### Validation Queries

#### Validation 3.1: Tag Coverage
```cypher
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
WITH eq, size(eq.tags) AS tag_count
RETURN AVG(tag_count) AS avg_tags,
       MIN(tag_count) AS min_tags,
       MAX(tag_count) AS max_tags,
       COUNT(eq) AS total_equipment
```

**Expected Result** (Healthcare example):
- `avg_tags`: 14.12
- `min_tags`: 11
- `max_tags`: 15
- `total_equipment`: 500

#### Validation 3.2: Equipment Without Tags
```cypher
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
  AND (eq.tags IS NULL OR size(eq.tags) = 0)
RETURN COUNT(eq) AS untagged_equipment
```

**Expected Result**: `untagged_equipment` = 0

#### Validation 3.3: Tag Dimension Coverage
```cypher
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
WITH eq,
     [tag IN eq.tags WHERE tag STARTS WITH 'GEO_'] AS geo_tags,
     [tag IN eq.tags WHERE tag STARTS WITH 'OPS_'] AS ops_tags,
     [tag IN eq.tags WHERE tag STARTS WITH 'REG_'] AS reg_tags,
     [tag IN eq.tags WHERE tag STARTS WITH 'TECH_'] AS tech_tags,
     [tag IN eq.tags WHERE tag STARTS WITH 'TIME_'] AS time_tags
RETURN
  COUNT(CASE WHEN size(geo_tags) = 0 THEN 1 END) AS missing_geo,
  COUNT(CASE WHEN size(ops_tags) = 0 THEN 1 END) AS missing_ops,
  COUNT(CASE WHEN size(reg_tags) = 0 THEN 1 END) AS missing_reg,
  COUNT(CASE WHEN size(tech_tags) = 0 THEN 1 END) AS missing_tech,
  COUNT(CASE WHEN size(time_tags) = 0 THEN 1 END) AS missing_time
```

**Expected Result**: All counts = 0 (all dimensions represented)

### Phase 3 Completion Checklist
- [ ] All equipment tagged (count verified)
- [ ] Average tag count within expected range for sector
- [ ] No equipment without tags
- [ ] All 5 dimensions represented on every equipment
- [ ] Geographic distribution matches sector profile
- [ ] Regulatory tags reflect sector compliance requirements
- [ ] Phase 3 completion documented

### Performance Metrics

**Processing Rate** (Week 12-14 benchmark):
- 379-411 tags/minute
- ~40 minutes for 1,200 equipment
- Sequential processing (for data consistency)

**Tag Count Ranges by Sector**:
- Healthcare: 11-15 tags (avg 14.12)
- Chemical: 11-15 tags (avg 14.18)
- Manufacturing: 12-14 tags (avg 12.96)
- Expected variation: ±1.5 tags from sector average

---

## Cross-Phase Validation

### Final Deployment Validation
Run after Phase 3 completion to verify entire sector deployment.

#### Validation: Complete Deployment Status
```cypher
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
WITH eq, r, f, size(eq.tags) AS tag_count
RETURN
  COUNT(DISTINCT eq) AS total_equipment,
  COUNT(DISTINCT f) AS total_facilities,
  COUNT(r) AS total_relationships,
  AVG(tag_count) AS avg_tags,
  MIN(tag_count) AS min_tags,
  MAX(tag_count) AS max_tags
```

**Expected Results** (Healthcare example):
- `total_equipment`: 500
- `total_facilities`: 60
- `total_relationships`: 500 (1:1 mapping)
- `avg_tags`: 14.12
- `min_tags`: 11
- `max_tags`: 15

#### Validation: Sector-Level Integrity
```cypher
// No orphaned equipment
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
  AND NOT (eq)-[:LOCATED_AT]->()
RETURN COUNT(eq) AS orphaned_equipment

// No duplicate relationships
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
WITH eq, collect(r) AS rels
WHERE size(rels) > 1
RETURN COUNT(eq) AS equipment_with_duplicates

// All equipment tagged
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
  AND (eq.tags IS NULL OR size(eq.tags) = 0)
RETURN COUNT(eq) AS untagged_equipment
```

**Expected Results**: All counts = 0

---

## Tools and Scripts Reference

### Standard Script Structure

**Comprehensive Sector Deployment Script** (PATTERN-7):
```python
#!/usr/bin/env python3
"""
Comprehensive 3-Phase Sector Deployment Script
Established Pattern from Week 12-14
"""

import subprocess
import json

def phase1_create_equipment(sector_name, equipment_prefix, equipment_count):
    """Phase 1: Create equipment nodes"""
    print(f"\n{'='*70}")
    print(f"PHASE 1: Creating {equipment_count} {sector_name} equipment nodes")
    print(f"{'='*70}")

    # Equipment creation logic
    # ... (implementation)

    return created_count

def phase2_create_relationships(sector_name, equipment_prefix, facility_prefix):
    """Phase 2: Create LOCATED_AT relationships"""
    print(f"\n{'='*70}")
    print(f"PHASE 2: Creating LOCATED_AT relationships")
    print(f"{'='*70}")

    # Get facilities from database (database-query-first)
    facilities = get_facilities_from_db(facility_prefix)

    # Relationship creation logic
    # ... (implementation)

    return relationships_count

def phase3_apply_5d_tags(sector_name, equipment_prefix):
    """Phase 3: Apply 5-dimensional tags"""
    print(f"\n{'='*70}")
    print(f"PHASE 3: Applying 5D tags to {sector_name} equipment")
    print(f"{'='*70}")

    # Tag application logic
    # ... (implementation)

    return tagged_count

# Main execution
if __name__ == "__main__":
    sector = "HEALTHCARE"
    eq_prefix = "EQ-HEALTH-"
    fac_prefix = "HEALTH-"
    equipment_target = 500

    # Execute phases sequentially with validation gates
    eq_created = phase1_create_equipment(sector, eq_prefix, equipment_target)
    if eq_created != equipment_target:
        print(f"❌ Phase 1 failed: Expected {equipment_target}, got {eq_created}")
        exit(1)

    rel_created = phase2_create_relationships(sector, eq_prefix, fac_prefix)
    if rel_created != equipment_target:
        print(f"❌ Phase 2 failed: Expected {equipment_target} relationships, got {rel_created}")
        exit(1)

    tagged = phase3_apply_5d_tags(sector, eq_prefix)
    if tagged != equipment_target:
        print(f"❌ Phase 3 failed: Expected {equipment_target} tagged, got {tagged}")
        exit(1)

    print(f"\n✅ {sector} DEPLOYMENT COMPLETE")
```

### Utility Functions

#### Database Query Function
```python
def query_neo4j(cypher_query):
    """Execute Cypher query against Neo4j database"""
    result = subprocess.run(
        ['docker', 'exec', 'openspg-neo4j', 'cypher-shell',
         '-u', 'neo4j', '-p', 'neo4j@openspg', cypher_query],
        capture_output=True,
        text=True
    )
    return result
```

#### Facility Lookup Function
```python
def get_facilities_from_db(facility_prefix):
    """Query database for actual facility IDs"""
    query = f"MATCH (f:Facility) WHERE f.facilityId STARTS WITH '{facility_prefix}' RETURN f.facilityId ORDER BY f.facilityId;"
    result = query_neo4j(query)

    facilities = []
    for line in result.stdout.strip().split('\n')[1:]:
        fac_id = line.strip().strip('"')
        if fac_id and not fac_id.startswith('f.facilityId'):
            facilities.append(fac_id)

    return facilities
```

#### Validation Function
```python
def validate_phase(phase_name, expected_count, validation_query):
    """Generic validation function for any phase"""
    result = query_neo4j(validation_query)
    actual_count = int(result.stdout.strip().split('\n')[1].strip())

    if actual_count == expected_count:
        print(f"✅ {phase_name} validation passed: {actual_count}/{expected_count}")
        return True
    else:
        print(f"❌ {phase_name} validation failed: {actual_count}/{expected_count}")
        return False
```

---

## Quality Assurance

### Pre-Deployment Checklist

**Planning Phase**:
- [ ] Sector requirements document completed
- [ ] Equipment taxonomy defined and reviewed
- [ ] Facility count confirmed
- [ ] Equipment count confirmed and matches facility capacity
- [ ] Equipment ID range allocated
- [ ] 5D tag schemas defined for sector
- [ ] Regulatory framework mapping completed
- [ ] Geographic distribution plan established

**Infrastructure Phase**:
- [ ] Neo4j database accessible and operational
- [ ] Docker container `openspg-neo4j` running
- [ ] Facility nodes exist in database (validated)
- [ ] Database backup completed before deployment
- [ ] Rollback plan documented

**Script Phase**:
- [ ] Deployment scripts written and tested in dev environment
- [ ] Validation queries prepared
- [ ] Cleanup scripts ready (if needed)
- [ ] Progress tracking implemented
- [ ] Error logging implemented

### During-Deployment Monitoring

**Phase 1 Monitoring**:
- Monitor equipment creation rate (should be consistent)
- Watch for errors in stderr output
- Verify progress updates match creation rate
- Check database disk space usage

**Phase 2 Monitoring**:
- Monitor relationship creation rate
- Watch for MATCH failures (indicates missing nodes)
- Check for warning signs of duplicates
- Verify equipment distribution across facilities

**Phase 3 Monitoring**:
- Monitor tagging rate (379-411 tags/minute benchmark)
- Watch for tag count outliers (>2 standard deviations from mean)
- Check for missing dimensions
- Verify sector-specific tag patterns

### Post-Deployment Verification

**Immediate Verification** (run after Phase 3):
1. Equipment count matches target
2. Relationship count matches equipment count (1:1 mapping)
3. No duplicate relationships
4. No orphaned equipment
5. All equipment have tags
6. Tag counts within expected range
7. All 5 dimensions represented

**24-Hour Verification** (next business day):
1. Spot-check sample equipment records
2. Verify tag accuracy against sector requirements
3. Test sample queries across all 5 dimensions
4. Review any warning logs
5. Confirm no database performance degradation

**7-Day Verification** (one week post-deployment):
1. Comprehensive query testing
2. Tag consistency audit
3. Relationship integrity check
4. Performance analysis
5. Documentation completeness review

---

## Troubleshooting Guide

### Phase 1 Issues

**Problem**: Equipment nodes not created despite returncode=0
- **Symptoms**: Validation query shows count < target, no errors logged
- **Diagnosis**: Cypher syntax error, invalid data types, Docker communication failure
- **Resolution**:
  1. Test Cypher query manually in cypher-shell
  2. Validate all data types match Neo4j requirements
  3. Check Docker container status: `docker ps | grep neo4j`
  4. Review Neo4j logs: `docker logs openspg-neo4j --tail 100`

**Problem**: Duplicate equipment IDs
- **Symptoms**: Unique constraint violation, creation fails
- **Diagnosis**: Script re-run without cleanup, ID range conflict
- **Resolution**:
  1. Query for existing equipment: `MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ-SECTOR-' RETURN COUNT(eq)`
  2. Delete existing if testing: `MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ-SECTOR-' DELETE eq`
  3. Adjust ID range to avoid conflicts
  4. Add unique constraint: `CREATE CONSTRAINT ON (eq:Equipment) ASSERT eq.equipmentId IS UNIQUE`

### Phase 2 Issues

**Problem**: Relationships not created (silent failure)
- **Symptoms**: returncode=0 but validation shows 0 relationships
- **Diagnosis**: Equipment or Facility nodes don't exist, MATCH fails silently
- **Resolution**:
  1. Verify equipment exists: `MATCH (eq:Equipment {equipmentId: 'EQ-XXX'}) RETURN eq`
  2. Verify facility exists: `MATCH (f:Facility {facilityId: 'FAC-XXX'}) RETURN f`
  3. Use database-query-first approach instead of hardcoded lists
  4. Add existence checks before CREATE

**Problem**: Duplicate relationships detected
- **Symptoms**: Validation 2.2 shows equipment with multiple relationships
- **Diagnosis**: Script re-run, parallel execution, no deduplication
- **Resolution**:
  1. Run cleanup script: `FOREACH (rel IN tail(rels) | DELETE rel)`
  2. Re-run validation to confirm cleanup
  3. Prevent future duplicates: add check before CREATE
  4. Consider using MERGE instead of CREATE (with caution)

**Problem**: Uneven facility distribution
- **Symptoms**: Some facilities have 0 equipment, others have excessive equipment
- **Diagnosis**: Modulo distribution doesn't account for actual facility count, facility capacity ignored
- **Resolution**:
  1. Calculate optimal distribution: `equipment_per_facility = total_equipment / facility_count`
  2. Use weighted distribution based on facility size/capacity
  3. Validate distribution: `MATCH (f:Facility)<-[:LOCATED_AT]-(eq) RETURN f.facilityId, COUNT(eq)`

### Phase 3 Issues

**Problem**: Low tag counts (< expected range)
- **Symptoms**: avg_tags significantly below benchmark (e.g., 9 vs 14 expected)
- **Diagnosis**: Missing dimensions, incomplete logic, facility context missing
- **Resolution**:
  1. Run dimension coverage query (Validation 3.3)
  2. Identify missing dimensions
  3. Review tagging logic for missing sector-specific rules
  4. Verify facility context available in query

**Problem**: High tag counts (> expected range)
- **Symptoms**: avg_tags significantly above benchmark (e.g., 20 vs 14 expected)
- **Diagnosis**: Duplicate tags, logic error adding tags multiple times
- **Resolution**:
  1. Sample high-count equipment: `MATCH (eq:Equipment) WHERE size(eq.tags) > 18 RETURN eq.equipmentId, eq.tags`
  2. Review tags for duplicates
  3. Fix logic to prevent duplicate tag addition
  4. Consider using sets instead of lists for tag accumulation

**Problem**: Tagging taking excessively long (> 1 hour for 1,200 equipment)
- **Symptoms**: Processing rate < 300 tags/minute
- **Diagnosis**: Database performance degradation, network latency, inefficient queries
- **Resolution**:
  1. Check database load: `docker stats openspg-neo4j`
  2. Optimize query to reduce roundtrips
  3. Consider batch updates (100 equipment at a time)
  4. Check network latency to Docker container

---

## Rollback Procedures

### Emergency Rollback (Complete Sector Removal)

**Use Case**: Critical data quality issue detected, need to start over

**Rollback Steps**:
```cypher
// Step 1: Delete all relationships for sector
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-SECTOR-'
DELETE r;

// Step 2: Delete all equipment nodes
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-SECTOR-'
DELETE eq;

// Step 3: Verify deletion
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-SECTOR-'
RETURN COUNT(eq) AS remaining_equipment;
// Expected: remaining_equipment = 0

// Note: Facility nodes are NOT deleted (reusable for next attempt)
```

**Post-Rollback**:
1. Review rollback logs
2. Identify root cause of data quality issue
3. Fix deployment scripts
4. Test in dev environment
5. Re-run deployment with fixes

### Partial Rollback (Phase-Specific)

**Phase 1 Rollback** (remove equipment, keep nothing):
```cypher
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-SECTOR-'
DELETE eq;
```

**Phase 2 Rollback** (remove relationships, keep equipment):
```cypher
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-SECTOR-'
DELETE r;
```

**Phase 3 Rollback** (remove tags, keep equipment and relationships):
```cypher
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-SECTOR-'
SET eq.tags = [];
```

---

## Appendix A: Complete Script Examples

### Example 1: Healthcare Sector Deployment
See `/home/jim/2_OXOT_Projects_Dev/scripts/healthcare_deployment/create_all.py`

### Example 2: Chemical Sector Deployment
See `/home/jim/2_OXOT_Projects_Dev/scripts/chemical_deployment/create_all.py`

### Example 3: Manufacturing Sector Deployment
See `/home/jim/2_OXOT_Projects_Dev/scripts/manufacturing_deployment/create_all.py`

---

## Appendix B: Validation Query Library

### Equipment Queries
```cypher
// Count by sector
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-' OR eq.equipmentId STARTS WITH 'EQ-CHEM-' OR eq.equipmentId STARTS WITH 'EQ-MFG-'
WITH eq.equipmentId AS eqId
RETURN
  CASE
    WHEN eqId STARTS WITH 'EQ-HEALTH-' THEN 'Healthcare'
    WHEN eqId STARTS WITH 'EQ-CHEM-' THEN 'Chemical'
    WHEN eqId STARTS WITH 'EQ-MFG-' THEN 'Manufacturing'
  END AS sector,
  COUNT(*) AS count
ORDER BY sector;
```

### Relationship Queries
```cypher
// Relationship integrity check
MATCH (eq:Equipment)-[r:LOCATED_AT]->(f:Facility)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
RETURN COUNT(r) AS total_relationships,
       COUNT(DISTINCT eq) AS unique_equipment,
       COUNT(DISTINCT f) AS unique_facilities;
```

### Tag Analysis Queries
```cypher
// Tag distribution
MATCH (eq:Equipment)
WHERE eq.equipmentId STARTS WITH 'EQ-HEALTH-'
WITH eq, size(eq.tags) AS tc
RETURN AVG(tc) AS avg_tags,
       MIN(tc) AS min_tags,
       MAX(tc) AS max_tags,
       COUNT(eq) AS total_equipment;
```

---

**Document Version**: 1.0
**Based On**: Week 12-14 deployment patterns (Healthcare, Chemical, Manufacturing)
**Last Updated**: 2025-01-13
**Status**: ✅ PRODUCTION READY

**END OF SECTOR DEPLOYMENT PROCEDURE**
