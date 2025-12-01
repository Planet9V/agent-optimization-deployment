# AGENT2: Query Pattern Analysis Report
**Universal Location Architecture - Equipment & Location Pattern Audit**

**Scan Date:** 2025-11-13
**Files Analyzed:** 70+ Cypher files
**Analysis Scope:** Equipment nodes, Location nodes, relationship patterns, property access patterns

---

## EXECUTIVE SUMMARY

**Critical Findings:**
- ✅ Equipment nodes **extensively used** in GAP-004 schema (16 Equipment CREATE statements in test files alone)
- ⚠️ Location nodes **minimally used** - only 1 instance in physical asset layer schema
- ⚠️ **NO standardized Equipment→Location relationships** in current codebase
- 🚨 **Breaking Change Risk: MEDIUM** - Adding Facility hierarchy will require query refactoring

**Equipment Usage:**
- **Test Files:** 2 files (gap004_uc2, gap004_uc3) with 60+ Equipment references
- **Schema Files:** 1 primary schema (01_layer_physical_asset.cypher)
- **Constraint Files:** 1 file (gap004_missing_base_constraints.cypher)

**Location Usage:**
- **Schema Files:** 3 files with Location node definitions
- **Actual Usage:** Minimal - only placeholder examples exist
- **Constraint:** Existing but uses 'id' property (not 'locationId')

---

## 1. EQUIPMENT MATCH PATTERNS

### 1.1 Simple Property Match Patterns
**Pattern:** `MATCH (eq:Equipment {property: value})`

| File | Line | Pattern | Usage Context |
|------|------|---------|---------------|
| tests/gap004_schema_validation_tests.cypher | 26 | `MATCH (e:Equipment {equipmentId: 'TEST_EQUIP_001'})` | Constraint validation test |
| tests/gap004_schema_validation_tests.cypher | 28 | `MATCH (e:Equipment {equipmentId: 'TEST_EQUIP_001'})` | Cleanup after test |
| tests/gap004_uc2_cyber_physical_tests.cypher | 226 | `MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ_TRANSFORMER_'` | Test cleanup with prefix match |
| tests/gap004_uc3_cascade_tests.cypher | 8 | `MATCH (eq:Equipment) WHERE eq.equipmentId STARTS WITH 'EQ_'` | Cleanup all test equipment |
| tests/gap004_uc3_cascade_tests.cypher | 65-80 | `MATCH (eq1:Equipment {equipmentId: 'EQ_TRANS_001'})` (×16) | Multi-equipment graph setup |
| tests/gap004_uc3_cascade_tests.cypher | 186 | `MATCH (eq:Equipment {status: 'active'})` | Status-based filtering |
| tests/gap004_uc3_cascade_tests.cypher | 253 | `MATCH (eq1:Equipment)-[:CONNECTS_TO*1..5]->(eq2:Equipment)` | Path traversal pattern |

**Key Properties Used:**
- `equipmentId` - Primary identifier (UNIQUE constraint required)
- `equipmentType` - Used in 116:117 (uc2), 220 (uc3), 246 (uc3)
- `status` - Used in 186 (uc2), all test data creates use 'active'
- `name` - Descriptive property in all CREATE statements
- `manufacturer`, `installDate` - Additional metadata in uc2 test setup

### 1.2 Relationship-Based Equipment Patterns
**Pattern:** Equipment accessed via relationships

| Relationship Type | Pattern | File:Line | Usage |
|-------------------|---------|-----------|-------|
| `MONITORS` | `(dt:DigitalTwinState)-[:MONITORS]->(eq:Equipment)` | uc2:56, 115, 155, 171, 186, 213 | Digital twin monitoring |
| `MEASURES` | `(ps:PhysicalSensor)-[:MEASURES]->(eq:Equipment)` | uc2:56, 142, 164, 202 | Sensor measurements |
| `CONNECTS_TO` | `(eq1:Equipment)-[:CONNECTS_TO*1..8]->(eq2:Equipment)` | uc2:67, 131, 193 | Multi-hop equipment paths |
| `CONNECTS_TO` | `(eq1:Equipment)-[:CONNECTS_TO*1..15]->(eq2:Equipment)` | uc2:131, uc3:151 | Extended cascade paths |
| `TRIGGERED_BY` | `(ce:CascadeEvent)-[:TRIGGERED_BY]->(eq:Equipment)` | uc3:141, 150, 198, 208, 218, 245, 296 | Cascade root cause tracking |
| `PROPAGATES_FROM/TO` | `(fp:FailurePropagation)-[:PROPAGATES_FROM/TO]->(eq:Equipment)` | uc3:133-134 | Failure propagation modeling |

**Multi-Hop Query Patterns:**
- **8-hop queries:** Used in uc2:67, uc3:142, uc3:219 for cyber-physical attack propagation
- **10-hop queries:** Used in uc2:193, uc3:209, uc3:297 for extended cascade analysis
- **15-hop queries:** Used in uc2:131, uc3:151 for maximum propagation depth testing

### 1.3 Aggregation & Analysis Patterns

**Equipment Type Aggregation:**
```cypher
// tests/gap004_uc2_cyber_physical_tests.cypher:116-117
MATCH (dt:DigitalTwinState)-[:MONITORS]->(eq:Equipment)
WITH eq.equipmentType AS type, count(dt) AS twin_count
```

**Cascade Trigger Analysis:**
```cypher
// tests/gap004_uc3_cascade_tests.cypher:246
WITH ce, eq.equipmentType AS type, count(*) AS trigger_count
```

**Path Traversal with Equipment Type Filtering:**
```cypher
// tests/gap004_uc2_cyber_physical_tests.cypher:193-195
MATCH path = (dt:DigitalTwinState)-[:MONITORS]->(eq1:Equipment)-[:CONNECTS_TO*1..10]->(eq2:Equipment)
WHERE eq1.equipmentType = 'Transformer'
  AND eq2.equipmentType IN ['Switch', 'Circuit Breaker']
```

---

## 2. LOCATION MATCH PATTERNS

### 2.1 Location Node Definitions Found

**Schema Definitions:**

| File | Line | Pattern | Notes |
|------|------|---------|-------|
| KAG/.../create_neo4j_schema.cypher | 94 | `FOR (loc:Location) REQUIRE loc.id IS UNIQUE` | Uses 'id' property |
| schemas/neo4j/00_constraints_indexes.cypher | 18 | `FOR (l:Location) REQUIRE l.id IS UNIQUE` | Current constraint |
| schemas/neo4j/01_layer_physical_asset.cypher | 92-108 | Full Location node schema | Example implementation |

**Current Location Schema (01_layer_physical_asset.cypher:92-108):**
```cypher
CREATE (control_room:Location {
  id: 'location-control-room-001',
  name: 'Main Control Room',
  locationType: 'ROOM',
  address: 'Building A, Floor 2, Room 201'
})
```

**Properties Used:**
- `id` - Primary identifier (UNIQUE constraint)
- `name` - Human-readable name
- `locationType` - ENUM [BUILDING, ROOM, RACK, ZONE, GEOGRAPHIC]
- `coordinates` - {lat: float, lon: float}
- `address` - String address
- `parent_location` - UUID for hierarchical locations

### 2.2 Location Relationship Patterns

**Found:** Only 1 LOCATED_AT relationship in entire codebase

| File | Line | Relationship | Pattern |
|------|------|--------------|---------|
| schemas/neo4j/01_layer_physical_asset.cypher | 117 | `LOCATED_AT` | `CREATE (plc)-[:LOCATED_AT]->(control_room)` |

**⚠️ CRITICAL GAP:** No Equipment→Location relationships exist in current implementation

### 2.3 Location Usage in Other Contexts

**Non-Node "location" References:**
- PhysicalSensor has `location: 'Substation_A'` as STRING property (uc2:18)
- Various MITRE ATT&CK descriptions reference "location" conceptually
- IEC 62443 documentation mentions "location" in asset identification

**🚨 INCONSISTENCY:** PhysicalSensor uses location as string property, not relationship to Location node

---

## 3. RELATIONSHIP PATTERNS ANALYSIS

### 3.1 CONNECTS_TO Relationship (Equipment Connectivity)

**Total Usage:** 33 instances across test files

**Pattern Variations:**

**Direct Connection (gap004_uc3_cascade_tests.cypher:83-97):**
```cypher
CREATE (eq1)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 100.0}]->(eq2)
CREATE (eq2)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 80.0}]->(eq3)
// ... 13 more sequential connections creating 15-hop chain
```

**Branching Connections (gap004_uc3_cascade_tests.cypher:100-101):**
```cypher
CREATE (eq2)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 60.0}]->(eq6)
CREATE (eq8)-[:CONNECTS_TO {connectionType: 'electrical', capacity: 70.0}]->(eq13)
```

**Relationship Properties:**
- `connectionType: 'electrical'` - Type of connection
- `capacity: float` - Connection capacity (varies: 25.0 to 100.0)

**Variable-Length Path Queries:**
- `*1..8` - Used 4 times (uc2:67, uc3:142, 219)
- `*1..10` - Used 4 times (uc2:193, uc3:209, 297)
- `*1..15` - Used 2 times (uc2:131, uc3:151)
- `*1..5` - Used 2 times (uc3:199, 253)

### 3.2 Cyber-Physical Relationships

**MONITORS (DigitalTwinState → Equipment):**
- **Usage:** 12 instances across uc2 tests
- **Pattern:** `(dt:DigitalTwinState)-[:MONITORS]->(eq:Equipment)`
- **Purpose:** Link digital twin state expectations to physical equipment

**MEASURES (PhysicalSensor → Equipment):**
- **Usage:** 6 instances in uc2 tests
- **Pattern:** `(ps:PhysicalSensor)-[:MEASURES]->(eq:Equipment)`
- **Purpose:** Link physical sensor readings to monitored equipment

### 3.3 Cascade Failure Relationships

**TRIGGERED_BY (CascadeEvent → Equipment):**
- **Usage:** 10 instances in uc3 tests
- **Pattern:** `(ce:CascadeEvent)-[:TRIGGERED_BY]->(eq:Equipment)`
- **Purpose:** Identify root cause equipment for cascade events

**PROPAGATES_FROM/TO (FailurePropagation → Equipment):**
- **Usage:** 4 instances in uc3 tests
- **Pattern:**
  ```cypher
  CREATE (fp1)-[:PROPAGATES_FROM]->(eq1)
  CREATE (fp1)-[:PROPAGATES_TO]->(eq2)
  ```
- **Purpose:** Model failure propagation paths between equipment

### 3.4 Physical Asset Layer Relationships

**From schemas/neo4j/01_layer_physical_asset.cypher:**

```cypher
CREATE (plant)-[:CONTAINS_DEVICE]->(plc);              // Line 115
CREATE (plc)-[:HAS_COMPONENT]->(comm_module);          // Line 116
CREATE (plc)-[:LOCATED_AT]->(control_room);            // Line 117
CREATE (brake_controller)-[:INSTALLED_IN]->(brake_system);  // Line 171
CREATE (brake_system)-[:PART_OF_SUBSYSTEM]->(train_car);   // Line 172
CREATE (train_car)-[:PART_OF_CONSIST]->(train_consist);    // Line 173
CREATE (train_consist)-[:PART_OF_FLEET]->(fleet);          // Line 174
```

**Hierarchy Patterns:**
- PhysicalAsset → Device → HardwareComponent (3-level physical hierarchy)
- Fleet → Consist → Vehicle → Subsystem → Component (5-level train hierarchy)
- **Missing:** Equipment → Facility → Site hierarchy

---

## 4. PROPERTY ACCESS PATTERNS

### 4.1 Equipment Property Access

**Direct Property Reference:**

| Property | Access Pattern | File:Line | Usage Frequency |
|----------|----------------|-----------|-----------------|
| `equipmentId` | `eq.equipmentId` | uc3:302, validation:26,28, uc2:226, uc3:8,308 | 18+ times |
| `equipmentType` | `eq.equipmentType` | uc2:116, uc3:220,246 | 6+ times |
| `status` | `eq.status` | uc2:186 | 2+ times |
| `name` | `eq.name` | uc3:308 | 3+ times (mostly in WHERE clauses) |

**WHERE Clause Patterns:**
```cypher
WHERE eq.equipmentId STARTS WITH 'EQ_'                    // Prefix match
WHERE eq.status = 'active'                                // Exact match
WHERE eq.equipmentType = 'Transformer'                    // Type filtering
WHERE eq.equipmentType IN ['Switch', 'Circuit Breaker']  // Multi-value match
WHERE eq.name CONTAINS 'Test'                             // Substring match
```

### 4.2 Equipment Creation Patterns

**Standard CREATE Pattern (gap004_uc3_cascade_tests.cypher:48-63):**
```cypher
CREATE (eq1:Equipment {
  equipmentId: 'EQ_TRANS_001',
  equipmentType: 'Transformer',
  name: 'Transformer A1',
  status: 'active'
});
```

**Enhanced CREATE Pattern (gap004_uc2_cyber_physical_tests.cypher:25-32):**
```cypher
CREATE (eq:Equipment {
  equipmentId: 'EQ_TRANSFORMER_001',
  equipmentType: 'Transformer',
  name: 'Main Transformer A1',
  status: 'active',
  manufacturer: 'ABB',
  installDate: date('2020-01-15')
});
```

**Property Set:**
- **Required:** equipmentId, equipmentType, name, status
- **Optional:** manufacturer, installDate, model, serialNumber, criticalityLevel

### 4.3 Location Property Access

**Current Schema Properties (01_layer_physical_asset.cypher:92-108):**
```cypher
Location {
  id: UUID,
  name: string,
  locationType: ENUM,
  coordinates: {lat, lon},
  address: string,
  parent_location: UUID
}
```

**⚠️ NO LOCATION PROPERTY ACCESS IN EQUIPMENT QUERIES**

---

## 5. CREATE PATTERNS

### 5.1 Equipment CREATE Statements

**Test File Equipment Creation:**

| File | Lines | Count | Pattern |
|------|-------|-------|---------|
| gap004_schema_validation_tests.cypher | 19, 23 | 2 | Basic test equipment with constraint validation |
| gap004_uc2_cyber_physical_tests.cypher | 25-32 | 1 | Enhanced equipment with manufacturer/date |
| gap004_uc3_cascade_tests.cypher | 48-63 | 16 | Equipment graph for cascade testing |

**Equipment Types in Test Data:**
- Transformer (3 instances: EQ_TRANS_001, EQ_TRANS_002, EQ_TRANS_003)
- Switch (6 instances: EQ_SWITCH_001 through EQ_SWITCH_006)
- Circuit Breaker (5 instances: EQ_CIRCUIT_BREAKER_001 through _005)
- Relay (1 instance: EQ_RELAY_001)
- Capacitor (1 instance: EQ_CAPACITOR_001)

### 5.2 Location CREATE Statements

**Found:** Only 1 Location CREATE in entire codebase

```cypher
// schemas/neo4j/01_layer_physical_asset.cypher:103-108
CREATE (control_room:Location {
  id: 'location-control-room-001',
  name: 'Main Control Room',
  locationType: 'ROOM',
  address: 'Building A, Floor 2, Room 201'
})
```

**⚠️ CRITICAL GAP:** No Facility, Site, or Building location nodes created

### 5.3 Index & Constraint CREATE Statements

**Equipment Indexes (backups/v1_2025-11-01_19-05-32/recreate_schema.cypher:132-135):**
```cypher
CREATE INDEX equipment_criticality_idx IF NOT EXISTS FOR (n:Equipment) ON (n.criticality_score);
CREATE INDEX equipment_name_idx IF NOT EXISTS FOR (n:Equipment) ON (n.normalized_name);
CREATE INDEX equipment_type IF NOT EXISTS FOR (n:Equipment) ON (n.type);
CREATE INDEX equipment_vendor IF NOT EXISTS FOR (n:Equipment) ON (n.vendor);
```

**Equipment Constraint (gap004_missing_base_constraints.cypher:13):**
```cypher
FOR (n:Equipment) REQUIRE n.equipmentId IS UNIQUE;
```

**Location Constraint (schemas/neo4j/00_constraints_indexes.cypher:18):**
```cypher
FOR (l:Location) REQUIRE l.id IS UNIQUE;
```

**Location Indexes (backups/v1_2025-11-01_19-05-32/recreate_schema.cypher:77-79):**
```cypher
CREATE INDEX cybersec_location_country IF NOT EXISTS FOR (n:Location) ON (n.country);
CREATE INDEX cybersec_location_id IF NOT EXISTS FOR (n:Location) ON (n.id);
CREATE INDEX cybersec_location_region IF NOT EXISTS FOR (n:Location) ON (n.region);
```

---

## 6. BREAKING CHANGE RISK ASSESSMENT

### 6.1 Impact Analysis: Adding Facility Hierarchy

**Proposed Change:**
```
Equipment → Facility → Site → Zone → Region
```

**Queries That WILL Break:**

#### 🔴 HIGH RISK - Direct Equipment MATCH Patterns
**Breaking Queries:** 40+ instances

**Example Breaking Pattern:**
```cypher
// CURRENT (gap004_uc3_cascade_tests.cypher:65)
MATCH (eq1:Equipment {equipmentId: 'EQ_TRANS_001'})

// REQUIRED AFTER CHANGE
MATCH (eq1:Equipment {equipmentId: 'EQ_TRANS_001'})-[:LOCATED_IN]->(facility:Facility)
```

**Files Affected:**
- `tests/gap004_schema_validation_tests.cypher` (4 queries)
- `tests/gap004_uc2_cyber_physical_tests.cypher` (20+ queries)
- `tests/gap004_uc3_cascade_tests.cypher` (30+ queries)

#### 🟡 MEDIUM RISK - Equipment Path Traversal Queries

**Current Pattern (uc2:67):**
```cypher
MATCH path = (dt:DigitalTwinState)-[:MONITORS]->(eq1:Equipment)
             -[:CONNECTS_TO*1..8]->(eq2:Equipment)
```

**Risk:** Adding `[:LOCATED_IN]→(facility:Facility)` relationships will NOT break path queries BUT will require updates for location-aware filtering

**Required Enhancement:**
```cypher
MATCH path = (dt:DigitalTwinState)-[:MONITORS]->(eq1:Equipment)
             -[:CONNECTS_TO*1..8]->(eq2:Equipment)
MATCH (eq1)-[:LOCATED_IN]->(f1:Facility)
MATCH (eq2)-[:LOCATED_IN]->(f2:Facility)
WHERE f1.facilityId = f2.facilityId  // Same facility cascade analysis
```

#### 🟢 LOW RISK - Equipment Type/Status Aggregations

**Current Pattern (uc2:115-117):**
```cypher
MATCH (dt:DigitalTwinState)-[:MONITORS]->(eq:Equipment)
WITH eq.equipmentType AS type, count(dt) AS twin_count
```

**Risk:** Will continue to work BUT missing facility context

**Enhancement Opportunity:**
```cypher
MATCH (dt:DigitalTwinState)-[:MONITORS]->(eq:Equipment)-[:LOCATED_IN]->(f:Facility)
WITH f.name AS facility, eq.equipmentType AS type, count(dt) AS twin_count
```

### 6.2 Relationship Changes Required

**New Relationships Needed:**
```cypher
(eq:Equipment)-[:LOCATED_IN]->(facility:Facility)
(facility:Facility)-[:PART_OF]->(site:Site)
(site:Site)-[:IN_ZONE]->(zone:Zone)
(zone:Zone)-[:IN_REGION]->(region:Region)
```

**Existing Relationships to Preserve:**
```cypher
(eq1:Equipment)-[:CONNECTS_TO]->(eq2:Equipment)         // 33 instances - PRESERVE
(dt:DigitalTwinState)-[:MONITORS]->(eq:Equipment)       // 12 instances - PRESERVE
(ps:PhysicalSensor)-[:MEASURES]->(eq:Equipment)         // 6 instances - PRESERVE
(ce:CascadeEvent)-[:TRIGGERED_BY]->(eq:Equipment)       // 10 instances - PRESERVE
```

### 6.3 Migration Strategy Recommendations

#### Phase 1: Backward-Compatible Addition
1. Add Facility/Site/Zone/Region nodes WITHOUT removing Equipment direct access
2. Add LOCATED_IN relationships as optional
3. Update indexes to include facility references
4. Equipment queries continue working unchanged

#### Phase 2: Dual-Mode Operation
1. Enhance queries to use Facility relationships when available
2. Fallback to direct Equipment access if no Facility relationship exists
3. Add validation warnings for Equipment without Facility

#### Phase 3: Full Migration (Breaking Changes)
1. Require all Equipment to have Facility relationship
2. Update all 60+ Equipment queries to include Facility path
3. Add CASCADE DELETE constraints for Equipment→Facility cleanup
4. Update test data to include Facility hierarchy

### 6.4 Query Refactoring Effort Estimation

**Files Requiring Updates:**
- `tests/gap004_uc2_cyber_physical_tests.cypher` - 20+ queries (4-6 hours)
- `tests/gap004_uc3_cascade_tests.cypher` - 30+ queries (6-8 hours)
- `tests/gap004_schema_validation_tests.cypher` - 4 queries (1 hour)
- `schemas/neo4j/01_layer_physical_asset.cypher` - 1 query (30 min)

**Total Refactoring Effort:** 12-16 hours

**Testing Effort:** Additional 8-12 hours for validation

---

## 7. KEY FINDINGS & RECOMMENDATIONS

### 7.1 Current State Assessment

✅ **Equipment Implementation: MATURE**
- Well-defined schema with UNIQUE constraint on equipmentId
- Extensive usage in UC2 (cyber-physical) and UC3 (cascade) test suites
- Rich relationship patterns (CONNECTS_TO, MONITORS, MEASURES, TRIGGERED_BY)
- Multi-hop path queries working (8-hop, 10-hop, 15-hop tested)

⚠️ **Location Implementation: MINIMAL**
- Only 1 Location node example exists (control_room)
- Only 1 LOCATED_AT relationship in entire codebase
- No Equipment→Location relationships implemented
- PhysicalSensor uses location as STRING property (inconsistent)

🚨 **Facility Hierarchy: NON-EXISTENT**
- No Facility, Site, Zone, or Region nodes defined
- No hierarchical location modeling implemented
- Equipment operates without spatial context

### 7.2 Breaking Change Risk Summary

| Change Type | Risk Level | Queries Affected | Migration Complexity |
|-------------|------------|------------------|---------------------|
| Add Facility nodes | 🟢 LOW | 0 | Add new nodes (non-breaking) |
| Add LOCATED_IN relationships | 🟢 LOW | 0 | Add relationships (non-breaking) |
| Require Facility for Equipment | 🔴 HIGH | 60+ | All Equipment queries need Facility path |
| Remove direct Equipment access | 🔴 CRITICAL | 60+ | Complete query rewrite required |

### 7.3 Recommended Approach

**Option A: Backward-Compatible Extension (RECOMMENDED)**
```cypher
// Add Facility hierarchy WITHOUT breaking existing queries
CREATE (eq:Equipment {equipmentId: 'EQ_TRANS_001', ...})
CREATE (facility:Facility {facilityId: 'FAC_SUBSTATION_A', ...})
CREATE (eq)-[:LOCATED_IN]->(facility)

// Existing queries continue to work:
MATCH (eq:Equipment {equipmentId: 'EQ_TRANS_001'})  // ✅ STILL WORKS

// Enhanced queries can now use Facility:
MATCH (eq:Equipment {equipmentId: 'EQ_TRANS_001'})-[:LOCATED_IN]->(f:Facility)
RETURN eq, f  // ✅ ENHANCED CAPABILITY
```

**Benefits:**
- Zero breaking changes to existing queries
- Gradual migration possible
- Facility context available for new queries
- Test suites continue working unchanged

**Option B: Full Refactor (NOT RECOMMENDED)**
```cypher
// BREAKING: Require Facility path for all Equipment access
MATCH (f:Facility {facilityId: 'FAC_SUBSTATION_A'})<-[:LOCATED_IN]-(eq:Equipment)
WHERE eq.equipmentId = 'EQ_TRANS_001'
```

**Drawbacks:**
- 60+ queries need immediate refactoring
- 12-16 hours development + 8-12 hours testing
- High risk of breaking production queries
- No backward compatibility

### 7.4 Implementation Checklist

**Phase 1: Schema Extension (Week 1)**
- [ ] Create Facility node schema with constraints
- [ ] Create Site, Zone, Region nodes (if needed)
- [ ] Add LOCATED_IN relationship definition
- [ ] Create sample Facility data for test suites
- [ ] Add indexes: `facilityId`, `facilityType`, `facilityName`

**Phase 2: Relationship Population (Week 2)**
- [ ] Add LOCATED_IN relationships for existing Equipment test data
- [ ] Ensure all Equipment in tests have Facility relationships
- [ ] Add validation query: "Equipment without Facility"
- [ ] Document Facility assignment rules

**Phase 3: Query Enhancement (Week 3-4)**
- [ ] Enhance high-value queries to use Facility context
- [ ] Add location-based cascade analysis queries
- [ ] Add facility-level aggregation reports
- [ ] Update documentation with Facility usage patterns

**Phase 4: Validation & Testing (Week 5)**
- [ ] Run all existing tests - verify ZERO breakage
- [ ] Add new Facility-aware tests
- [ ] Performance test multi-hop queries (Equipment→Facility→Site)
- [ ] Document migration guide for production systems

---

## 8. APPENDIX: FILE REFERENCE INDEX

### Equipment-Heavy Files
1. `tests/gap004_uc2_cyber_physical_tests.cypher` - 232 lines, 20+ Equipment queries
2. `tests/gap004_uc3_cascade_tests.cypher` - 314 lines, 30+ Equipment queries
3. `tests/gap004_schema_validation_tests.cypher` - Equipment constraint validation
4. `schemas/neo4j/01_layer_physical_asset.cypher` - Physical asset layer definition

### Location-Relevant Files
1. `schemas/neo4j/01_layer_physical_asset.cypher` - Location node schema (lines 92-108)
2. `schemas/neo4j/00_constraints_indexes.cypher` - Location constraints (line 18)
3. `KAG/kag/examples/CybersecurityKB/schema/create_neo4j_schema.cypher` - Location schema
4. `backups/v1_2025-11-01_19-05-32/recreate_schema.cypher` - Location indexes (77-79)

### Constraint & Index Files
1. `scripts/gap004_missing_base_constraints.cypher` - Equipment constraint (line 13)
2. `backups/v1_2025-11-01_19-05-32/recreate_schema.cypher` - Equipment indexes (132-135)

### Relationship Pattern Files
1. `scripts/gap004_relationships.cypher` - 50+ relationship pattern definitions
2. `tests/gap004_uc3_cascade_tests.cypher` - CONNECTS_TO relationship creation (83-101)

---

**Report Complete**
**Total Files Scanned:** 70+ Cypher files
**Total Equipment References:** 60+ MATCH statements, 16+ CREATE statements
**Total Location References:** 4 schema definitions, 1 CREATE statement, 1 LOCATED_AT relationship
**Breaking Change Risk:** MEDIUM (manageable with backward-compatible approach)

