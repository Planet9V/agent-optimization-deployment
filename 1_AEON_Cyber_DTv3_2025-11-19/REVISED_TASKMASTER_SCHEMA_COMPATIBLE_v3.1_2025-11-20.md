# REVISED TASKMASTER - Schema Compatible v3.1

**CRITICAL REVISION**: Match existing database schema pattern
**Date**: 2025-11-20 01:35:00 UTC
**Reason**: Original TASKMASTER used wrong schema (Equipment + SECTOR_ tags)
**Actual Schema**: Sector-specific labels (WaterDevice, EnergyDevice, etc.)

---

## SCHEMA PATTERN DISCOVERED

**Existing Sectors Use**:
- Water: WaterDevice, WATER, Water_Treatment, Water_Distribution labels
- Energy: EnergyDevice, ENERGY, Energy_Transmission, Energy_Distribution labels
- NOT: Equipment node with SECTOR_ tags

**For NEW Sectors, Follow Existing Pattern**:
- Communications: Create CommunicationsDevice, COMMUNICATIONS labels
- Healthcare: Use existing HealthDevice pattern
- Each sector: [Sector]Device + [SECTOR] + subsector labels

---

## REVISED TASK GROUPS (Per Sector)

### TASK GROUP 1: Schema Investigation (1 day)
**TASK X.1.1**: Investigate if sector already exists
- Query: Search for sector-specific labels
- Evidence: List of existing nodes (if any)
- Decision: Extend existing OR create new

### TASK GROUP 2: Schema Design (1 day)
**TASK X.2.1**: Design sector-specific labels matching pattern
- Labels: [Sector]Device, [SECTOR], [Sector]_Subsector
- Match: Existing Water/Energy pattern
- Avoid: Duplicate schema

### TASK GROUP 3: Data Generation (2 days)
**TASK X.3.1**: Generate sector data matching schema
- Python: Create JSON with correct labels
- Test: Validate against existing pattern

### TASK GROUP 4: Deployment & Validation (1 day)
**TASK X.4.1**: Deploy to Neo4j
**TASK X.4.2**: Validate with queries
**Evidence Required**: Actual node counts

### TASK GROUP 5: Documentation (1 day)
**TASK X.5.1**: Document with evidence

---

## GUARD AGAINST MISTAKES

**Before Any Sector Deployment**:
1. ✅ Query database for existing sector data
2. ✅ Identify label pattern used
3. ✅ Match that pattern (don't invent new schema)
4. ✅ Validate compatibility

**Constitutional Compliance**: Check what EXISTS before creating

---

**Version**: 3.1 (revised for schema compatibility)
**Status**: READY FOR PROPER EXECUTION
