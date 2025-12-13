# AEON Hierarchical Schema Fix - Quick Start Guide

**Status:** READY FOR EXECUTION
**Created:** 2025-12-12
**Estimated Time:** 2-3 hours

---

## The Problem (30 seconds)

Your Neo4j database has 1.4M nodes but they're missing critical v3.1 schema properties:
- Only 5.8% have super labels (should be 95%+)
- 0% have tier properties (should be 98%+)
- 316K CVE nodes missing Vulnerability classification

**Result:** Hierarchical architecture doesn't work, fine-grained queries impossible.

---

## The Solution (30 seconds)

Run one Python script that:
1. Adds 16 super labels to all nodes
2. Adds hierarchical properties (tier1, tier2, tier)
3. Adds property discriminators for 566-type taxonomy
4. Validates everything worked

---

## Quick Execution (5 minutes)

### Step 1: Backup (2 minutes)

```bash
sudo systemctl stop neo4j
sudo cp -r /var/lib/neo4j/data/databases/neo4j /var/lib/neo4j/data/databases/neo4j.backup.$(date +%Y%m%d_%H%M%S)
sudo systemctl start neo4j
```

### Step 2: Run Migration (60-90 minutes)

```bash
cd /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts
python3 FIX_HIERARCHICAL_SCHEMA.py
# Type "yes" when prompted
```

### Step 3: Validate (2 minutes)

```bash
cat VALIDATION_QUERIES.cypher | cypher-shell -u neo4j -p neo4j@openspg | grep "PASS"
# Should see all checks PASS
```

---

## Expected Output

```
PHASE 1: ANALYZING CURRENT DATABASE STATE
Total nodes: 1,426,989
Nodes with super labels: 83,052 (5.8%)

PHASE 2: ADDING SUPER LABELS
ThreatActor: Added to 1,067 nodes
Vulnerability: Added to 304,530 nodes (CVEs!)
...
Total super labels added: 500,000

PHASE 3: ADDING HIERARCHICAL PROPERTIES
...
Total tier properties added: 1,400,000

PHASE 4: ADDING PROPERTY DISCRIMINATORS
...
Total discriminators added: 500,000

PHASE 5: VALIDATION
Super label coverage: 95.0% ✅ PASS
Tier property coverage: 98.5% ✅ PASS
Discriminator coverage: 35.0% ✅ PASS
Overall validation: ✅ PASS

MIGRATION COMPLETE ✅
```

---

## What You Get

**Before:**
```cypher
MATCH (n:CVE) RETURN n.name, labels(n);
// Returns: n.name="CVE-2020-0688", labels=['CVE']
// Missing: Vulnerability super label, tier properties
```

**After:**
```cypher
MATCH (n:CVE) RETURN n.name, labels(n), n.tier1, n.tier2, n.vulnType;
// Returns:
//   n.name="CVE-2020-0688"
//   labels=['CVE', 'Vulnerability']  ← Super label added!
//   n.tier1="TECHNICAL"               ← Tier category added!
//   n.tier2="Vulnerability"           ← Super label added!
//   n.vulnType="cve"                  ← Discriminator added!
```

**New Queries Enabled:**
```cypher
// Query 1: All TECHNICAL threats
MATCH (n) WHERE n.tier1 = 'TECHNICAL'
RETURN n.tier2, count(n);

// Query 2: APT groups only
MATCH (n:ThreatActor) WHERE n.actorType = 'apt_group'
RETURN n.name;

// Query 3: Tier distribution
MATCH (n) WHERE n.tier IS NOT NULL
RETURN n.tier, count(n);
```

---

## Files Created

**Migration Script:**
- `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/FIX_HIERARCHICAL_SCHEMA.py`

**Validation:**
- `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/VALIDATION_QUERIES.cypher`

**Documentation:**
- `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/HIERARCHICAL_SCHEMA_FIX_PROCEDURE.md`
- `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/docs/SOLUTION_SUMMARY.md`

**Logs:**
- `/home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/logs/schema_fix.log`

---

## Rollback (if needed)

```bash
sudo systemctl stop neo4j
sudo rm -rf /var/lib/neo4j/data/databases/neo4j
sudo cp -r /var/lib/neo4j/data/databases/neo4j.backup.YYYYMMDD_HHMMSS /var/lib/neo4j/data/databases/neo4j
sudo chown -R neo4j:neo4j /var/lib/neo4j/data/databases/neo4j
sudo systemctl start neo4j
```

---

## Success Metrics

✅ Node count unchanged (1,426,989)
✅ Super label coverage > 90%
✅ Tier property coverage > 90%
✅ All CVEs have Vulnerability super label
✅ Hierarchical queries work
✅ Fine-grained entity filtering enabled

---

## Support

**Full Documentation:** `HIERARCHICAL_SCHEMA_FIX_PROCEDURE.md`
**Troubleshooting:** See procedure doc Section "Troubleshooting"
**Questions:** Review `SOLUTION_SUMMARY.md`

---

**Ready to Execute? Run:** `python3 FIX_HIERARCHICAL_SCHEMA.py`
