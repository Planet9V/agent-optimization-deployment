# Procedures Overview and Analysis

**File:** 03_PROCEDURES_OVERVIEW.md
**Created:** 2025-12-03
**Purpose:** Summary of 34 ETL procedures with implementation status

---

## Procedure Categories

| Category | ID Range | Count | Enhancements Covered |
|----------|----------|-------|---------------------|
| Schema & Setup | PROC-0XX | 1 | Foundation |
| Core ETL | PROC-1XX | 7 | E01-E06 |
| Safety | PROC-12X | 3 | E07-E09 |
| Economic | PROC-13X | 4 | E10-E13 |
| Technical | PROC-14X | 3 | E14-E16 |
| Psychometric | PROC-15X | 5 | E17-E21 |
| Advanced | PROC-16X | 5 | E22-E26 |
| Attack Chain | PROC-2XX-5XX | 4 | Foundation |
| Validation | PROC-9XX | 1 | Final |

**Total**: 34 procedures (+ 1 template)

---

## Implementation Status

**All 34 procedures are DOCUMENTED but NOT IMPLEMENTED**

### Current State vs To Do List

| Category | In To Do List | Gap |
|----------|---------------|-----|
| Schema Setup (PROC-001) | NO | **GAP** |
| Core ETL (7 procedures) | NO | **GAP** |
| Safety (3 procedures) | NO | **GAP** |
| Economic (4 procedures) | NO | **GAP** |
| Technical (3 procedures) | NO | **GAP** |
| Psychometric (5 procedures) | NO | **GAP** |
| Advanced (5 procedures) | NO | **GAP** |
| Attack Chain (4 procedures) | NO | **GAP** |
| Validation (1 procedure) | NO | **GAP** |

---

## Top 10 Priority Procedures

| Rank | Procedure | Enhancement | ICE | Feasibility | Rationale |
|------|-----------|-------------|-----|-------------|-----------|
| 1 | PROC-001 Schema | Foundation | 9.5 | HIGH | Required first |
| 2 | PROC-117 Wiki Truth | E06b | 9.0 | HIGH | Data quality |
| 3 | PROC-121 IEC 62443 | E07 | 8.7 | HIGH | Compliance |
| 4 | PROC-101 CVE | Core | 8.5 | HIGH | Foundation |
| 5 | PROC-111 APT Intel | E01 | 8.5 | HIGH | Threat intel |
| 6 | PROC-133 N/N/N | E12 | 8.5 | HIGH | CVE overload |
| 7 | PROC-115 Feeds | E05 | 8.3 | MEDIUM | Real-time |
| 8 | PROC-112 STIX | E02 | 8.2 | HIGH | Standards |
| 9 | PROC-113 SBOM | E03 | 8.0 | MEDIUM | Supply chain |
| 10 | PROC-131 Economic | E10 | 7.8 | MEDIUM | Business value |

---

## McKenney Questions Coverage

| Question | Primary Procedures |
|----------|-------------------|
| Q1: What equipment? | PROC-113, PROC-121, PROC-142 |
| Q2: Customer equipment? | PROC-121, PROC-132, PROC-142 |
| Q3: Attacker knowledge? | PROC-101, PROC-111, PROC-134, PROC-164 |
| Q4: Attacker motivations? | PROC-111, PROC-112, PROC-141, PROC-151-155 |
| Q5: Defense options? | PROC-101, PROC-121, PROC-133, PROC-143 |
| Q6: Past incidents? | PROC-115, PROC-122, PROC-131 |
| Q7: Future predictions? | PROC-132, PROC-133, PROC-161, PROC-162, PROC-165 |
| Q8: Action priorities? | PROC-101, PROC-121, PROC-133, PROC-153-154, PROC-163 |
| Q9: Communication? | PROC-117, PROC-153, PROC-163 |
| Q10: Population behavior? | PROC-132, PROC-151-154, PROC-161-163 |

**CAPSTONE**: PROC-165 (McKenney-Lacan Calculus) covers ALL 10 questions.

---

## Pipeline Execution Order

### Phase 1: Schema (Run Once)
```bash
./proc_001_schema_migration.sh
```

### Phase 2: Core Data (Parallel)
```bash
./proc_101_cve_enrichment.sh full &
./proc_111_apt_threat_intel.sh &
./proc_112_stix_integration.sh &
./proc_113_sbom_analysis.sh &
wait
```

### Phase 3: Chain Building (Sequential)
```bash
./proc_201_cwe_capec_linker.sh
./proc_301_capec_attack_mapper.sh
./proc_501_threat_actor_enrichment.sh
```

### Phase 4: Enhancement Procedures (Parallel)
```bash
./proc_121_iec62443_safety.sh &
./proc_131_economic_impact.sh &
./proc_141_lacanian_rsi.sh &
./proc_151_lacanian_dyad.sh &
wait
```

### Phase 5: Advanced Analytics (After Dependencies)
```bash
./proc_161_seldon_crisis.sh
./proc_165_mckenney_lacan_calculus.sh
```

### Phase 6: Validation
```bash
./proc_901_attack_chain_builder.sh
```

---

## Links

- [Master Report](00_MASTER_RATIONALIZATION_REPORT.md)
- [Enhancement Dependencies](01_ENHANCEMENT_DEPENDENCY_GRAPH.md)
- [API Roadmap](02_API_IMPLEMENTATION_ROADMAP.md)
- [Procedures JSON](../scraps/procedures_analysis.json)
