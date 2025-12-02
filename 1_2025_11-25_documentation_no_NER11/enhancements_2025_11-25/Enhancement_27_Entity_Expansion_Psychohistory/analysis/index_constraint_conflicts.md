# Index-Constraint Conflict Analysis
**File**: index_constraint_conflicts.md
**Created**: 2025-11-28 22:00:00 UTC
**Purpose**: Identify blocking indexes and resolve constraint creation issues

## Executive Summary

**Current State**:
- **Existing Constraints**: 44 total (many on old labels)
- **Target Constraints**: 16 (for E27 Super Labels)
- **Successfully Created**: 12/16 constraints exist
- **Blocked**: 4 constraints cannot be created due to index conflicts

## Detailed Analysis

### ✅ Successfully Created Constraints (12/16)

| Super Label | Constraint Name | Property | Status |
|-------------|----------------|----------|---------|
| ThreatActor | constraint_338f9f7b | name | ✅ EXISTS |
| AttackPattern | attack_pattern_id | external_id | ✅ EXISTS |
| Vulnerability | vulnerability_id | external_id | ✅ EXISTS |
| Malware | constraint_ce8e6a06 | name | ✅ EXISTS |
| Indicator | indicator_id | indicator_value | ✅ EXISTS |
| Asset | asset_id | asset_id | ✅ EXISTS |
| Organization | org_name | name | ✅ EXISTS |
| Software | constraint_2172d887 | name | ✅ EXISTS |
| EconomicMetric | constraint_60b2f84c | name | ✅ EXISTS |
| Campaign | constraint_9b04054f | name | ✅ EXISTS |
| Event | constraint_f16c28c9 | name | ✅ EXISTS |
| Control | constraint_2c4108aa | name | ✅ EXISTS |

### ❌ Blocked Constraints (4/16)

#### 1. Location - Composite Key Conflict
**Target**: `CREATE CONSTRAINT location_id FOR (n:Location) REQUIRE (n.name, n.locationType) IS NODE KEY;`
**Blocker**: Existing constraint on different property
- **constraint_name**: location_id_unique
- **existing_property**: locationId (single property)
- **target_properties**: (name, locationType) - composite key
- **Issue**: Cannot create NODE KEY when uniqueness constraint exists on different property

#### 2. Protocol - Property Name Mismatch
**Target**: `CREATE CONSTRAINT protocol_id FOR (n:Protocol) REQUIRE n.protocol_name IS UNIQUE;`
**Status**: Constraint exists but on wrong property
- **constraint_name**: constraint_316ea96d
- **existing_property**: name
- **target_property**: protocol_name
- **Issue**: Property name mismatch - need to standardize

#### 3. PsychTrait - Composite Key Conflict
**Target**: `CREATE CONSTRAINT psych_trait_id FOR (n:PsychTrait) REQUIRE (n.traitType, n.subtype) IS NODE KEY;`
**Blocker**: Existing simple uniqueness constraint
- **constraint_name**: constraint_e9b7e8e5
- **existing_property**: name (single property)
- **target_properties**: (traitType, subtype) - composite key
- **Issue**: Cannot create NODE KEY when uniqueness constraint exists on name

#### 4. Role - Missing Constraint
**Target**: `CREATE CONSTRAINT role_id FOR (n:Role) REQUIRE n.role_name IS UNIQUE;`
**Status**: No constraint exists
- **Issue**: Property name needs verification - should be `role_name` or `name`?

## Index Analysis

### Indexes Owned by Constraints (AUTO-CREATED)

These indexes are automatically created and managed by constraints:

```
Software.name → constraint_2172d887 (owned index: id 89)
AttackPattern.name → constraint_24c3e18c (owned index: id 92)
Control.name → constraint_2c4108aa (owned index: id 104)
ThreatActor.stix_id → constraint_30081f1b (owned index: id 85)
Protocol.name → constraint_316ea96d (owned index: id 141)
ThreatActor.name → constraint_338f9f7b (owned index: id 60)
Asset.name → constraint_368ca986 (owned index: id 106)
EconomicMetric.name → constraint_60b2f84c (owned index: id 102)
Indicator.name → constraint_706f01e5 (owned index: id 90)
Software.stix_id → constraint_7efaa4f0 (owned index: id 87)
Vulnerability.name → constraint_903461f9 (owned index: id 108)
Campaign.name → constraint_9b04054f (owned index: id 94)
```

### Independent Indexes (NO CONSTRAINT)

These indexes were created manually and are NOT owned by constraints:

```
Asset:
- asset_class_device (id: 120) - assetClass, deviceType
- asset_purdue (id: 121) - purdue_level

ThreatActor:
- actor_type (id: 136) - actorType
- idx_threat_actor_capability (id: 62) - capabilityLevel
- idx_threat_actor_country (id: 61) - country

Campaign:
- campaign_dates (id: 138) - start_date, end_date
- campaign_type (id: 135) - campaignType

Event:
- event_timestamp (id: 137) - timestamp
- event_type (id: 129) - eventType

Indicator:
- indicator_type (id: 132) - indicatorType

Protocol:
- protocol_type (id: 130) - protocolType

PsychTrait:
- psych_trait_intensity (id: 123) - intensity
- psych_trait_type (id: 122) - traitType, subtype

Vulnerability:
- vuln_cvss (id: 125) - cvss_score
- vuln_discovered (id: 139) - discovered_date
- vuln_type (id: 124) - vulnType

Malware:
- malware_family (id: 127) - malwareFamily

Control:
- control_type (id: 128) - controlType

EconomicMetric:
- metric_type (id: 131) - metricType

Organization:
- org_type (id: 133) - orgType

AttackPattern:
- pattern_type (id: 126) - patternType
- idx_attack_pattern_mitre (id: 63) - mitreId
- idx_attack_pattern_tactic (id: 64) - tacticName
```

**No conflicts detected** - all independent indexes are on different properties than target constraints.

## Resolution Strategy

### Phase 1: Drop Conflicting Constraints

```cypher
// Drop conflicting Location constraint
DROP CONSTRAINT location_id_unique IF EXISTS;

// Drop conflicting Protocol constraint (wrong property)
DROP CONSTRAINT constraint_316ea96d IF EXISTS;

// Drop conflicting PsychTrait constraint
DROP CONSTRAINT constraint_e9b7e8e5 IF EXISTS;
```

### Phase 2: Verify Property Names

Before creating new constraints, verify actual property usage in data:

```cypher
// Check Protocol property names
MATCH (p:Protocol)
RETURN DISTINCT keys(p) AS property_names
LIMIT 5;

// Check Role property names
MATCH (r:Role)
RETURN DISTINCT keys(r) AS property_names
LIMIT 5;

// Check Location property composition
MATCH (l:Location)
RETURN DISTINCT keys(l) AS property_names
LIMIT 5;

// Check PsychTrait property composition
MATCH (pt:PsychTrait)
RETURN DISTINCT keys(pt) AS property_names
LIMIT 5;
```

### Phase 3: Create Corrected Constraints

After verification and cleanup:

```cypher
// Location - Composite NODE KEY
CREATE CONSTRAINT location_id IF NOT EXISTS
FOR (n:Location) REQUIRE (n.name, n.locationType) IS NODE KEY;

// Protocol - Verify property name first
// If data uses 'name':
CREATE CONSTRAINT protocol_id IF NOT EXISTS
FOR (n:Protocol) REQUIRE n.name IS UNIQUE;

// If data uses 'protocol_name':
CREATE CONSTRAINT protocol_id IF NOT EXISTS
FOR (n:Protocol) REQUIRE n.protocol_name IS UNIQUE;

// PsychTrait - Composite NODE KEY
CREATE CONSTRAINT psych_trait_id IF NOT EXISTS
FOR (n:PsychTrait) REQUIRE (n.traitType, n.subtype) IS NODE KEY;

// Role - Verify property name first
// If data uses 'role_name':
CREATE CONSTRAINT role_id IF NOT EXISTS
FOR (n:Role) REQUIRE n.role_name IS UNIQUE;

// If data uses 'name':
CREATE CONSTRAINT role_id IF NOT EXISTS
FOR (n:Role) REQUIRE n.name IS UNIQUE;
```

## Data Verification Queries

### Check for Duplicate Values

Before creating constraints, verify data quality:

```cypher
// Location duplicates on composite key
MATCH (l:Location)
WITH l.name AS name, l.locationType AS type, count(*) AS count
WHERE count > 1
RETURN name, type, count;

// PsychTrait duplicates on composite key
MATCH (pt:PsychTrait)
WITH pt.traitType AS trait, pt.subtype AS sub, count(*) AS count
WHERE count > 1
RETURN trait, sub, count;

// Protocol duplicates
MATCH (p:Protocol)
WITH p.name AS name, count(*) AS count
WHERE count > 1
RETURN name, count;

// Role duplicates
MATCH (r:Role)
WITH r.name AS name, count(*) AS count
WHERE count > 1
RETURN name, count;
```

## Expected Outcome

After successful resolution:

```
SHOW CONSTRAINTS YIELD name, type, entityType, properties
WHERE name LIKE 'location_id%'
   OR name LIKE 'protocol_id%'
   OR name LIKE 'psych_trait_id%'
   OR name LIKE 'role_id%'
RETURN name, type, entityType, properties
ORDER BY name;
```

**Expected**: 4 new constraints matching E27 specification
**Total**: 16 E27 constraints (12 existing + 4 new)

## Risk Assessment

**Low Risk**:
- No index conflicts on independent property indexes
- All independent indexes serve different purposes than uniqueness
- Dropping and recreating constraints on same data (no data loss)

**Medium Risk**:
- Composite keys may expose duplicate data
- Property name mismatches need manual verification
- Role constraint completely missing - need schema validation

**Mitigation**:
1. Run duplicate detection queries before constraint creation
2. Verify actual property names in sample data
3. Test constraint creation on small dataset first
4. Keep backup of current constraint state
