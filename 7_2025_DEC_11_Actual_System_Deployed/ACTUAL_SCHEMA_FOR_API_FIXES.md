# ACTUAL Neo4j Schema - For API Query Fixes

**Date**: 2025-12-12
**Purpose**: Reference for fixing 31 failing APIs

---

## 🔑 KEY PROPERTY NAMES (ACTUAL)

### **Organization** (55,569 nodes) - For Vendor APIs
**Properties**:
- `id` (NOT vendor_id)
- `name`
- `type` or `role` (NOT orgType)
- `country`
- `super_label` = "Organization"
- `tier1` = "ORGANIZATIONAL"

**Example**: CISA (Cybersecurity and Infrastructure Security Agency)

**Fix vendor APIs**:
```cypher
// WRONG:
MATCH (v:Vendor {vendor_id: $id})

// CORRECT:
MATCH (v:Organization {id: $id})
WHERE v.type = 'VENDOR' OR v.role CONTAINS 'VENDOR'
```

---

### **Asset** (200,275 nodes) - For Equipment APIs
**Properties**:
- `id` (NOT equipment_id)
- `assetClass` (equipment, device, etc.)
- `device_type`
- `manufacturer`
- `model`
- `status`
- `super_label` = "Asset"

**Fix equipment APIs**:
```cypher
// WRONG:
MATCH (e:Equipment {equipment_id: $id})

// CORRECT:
MATCH (e:Asset {id: $id})
WHERE e.assetClass IN ['equipment', 'device']
```

---

### **ThreatActor** (10,599 nodes)
**Properties**:
- `id` (NOT actor_id)
- `name`
- `actorType` (apt_group, nation_state, etc.)
- `aliases`
- `super_label` = "ThreatActor"

**Fix threat APIs**:
```cypher
// WRONG:
MATCH (ta:ThreatActor {actor_id: $id})

// CORRECT:
MATCH (ta:ThreatActor {id: $id})
// Or: MATCH (ta:ThreatActor {name: $name})
```

---

### **SoftwareComponent** (40,000+ nodes) - For SBOM APIs
**Properties**:
- `component_id` ✅ (correct!)
- `name`
- `version`
- Check if also uses `id`

---

## 🔧 FIX PATTERN

**For ALL 31 failing APIs**:
1. Change `{specific}_id` → `id`
2. Add `WHERE super_label = 'X'` if needed
3. Use discriminator properties for filtering

**Timeline**: 32 hours to fix all

---

**Next**: Apply fixes to API code ✅
