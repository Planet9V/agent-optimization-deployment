# AEON ETL Procedures Index

**Version**: 2.1.0
**Created**: 2025-11-26
**Last Modified**: 2025-12-11
**Total Procedures**: 35 (+ 1 template)

---

## Overview

This directory contains **34 standardized, repeatable ETL procedures** for the AEON Cyber Digital Twin platform, covering all 26 enhancement modules plus core pipeline procedures. Each procedure follows the template in `00_PROCEDURE_TEMPLATE.md`.

**Design Principles**:
- **Repeatability**: Execute identically every time
- **Auditability**: Full logging and verification
- **Recoverability**: Rollback capabilities
- **Automation**: Cron scheduling support

---

## Procedure Catalog - Complete

### PROC-0XX: Schema & Setup

| ID | Name | Enhancement | Purpose | Frequency |
|----|------|-------------|---------|-----------|
| [PROC-001](PROC-001-schema-migration.md) | Schema Migration | - | Initialize Neo4j schema, constraints, indexes | ON-DEMAND |

### PROC-1XX: Core ETL Pipeline

| ID | Name | Enhancement | Purpose | Frequency |
|----|------|-------------|---------|-----------|
| [PROC-101](PROC-101-cve-enrichment.md) | CVE Enrichment | - | Enrich CVEs with CVSS/CWE from NVD | DAILY |
| [PROC-102](PROC-102-kaggle-enrichment.md) | Kaggle Dataset Enrichment | - | Enrich CVEs with CVSS v2/v3/v4 + CWE from Kaggle | MONTHLY |
| [PROC-111](PROC-111-apt-threat-intel.md) | APT Threat Intel | E01 | Ingest APT threat intelligence data | WEEKLY |
| [PROC-112](PROC-112-stix-integration.md) | STIX Integration | E02 | Parse STIX 2.1 threat data | WEEKLY |
| [PROC-113](PROC-113-sbom-analysis.md) | SBOM Analysis | E03 | Software bill of materials vulnerability analysis | WEEKLY |
| [PROC-114](PROC-114-psychometric-integration.md) | Psychometric Integration | E04 | Base personality framework integration | MONTHLY |
| [PROC-115](PROC-115-realtime-feeds.md) | Real-Time Feeds | E05 | Continuous threat feed ingestion | HOURLY |
| [PROC-116](PROC-116-executive-dashboard.md) | Executive Dashboard | E06a | Aggregate KPIs for executive view | HOURLY |
| [PROC-117](PROC-117-wiki-truth-correction.md) | Wiki Truth Correction | E06b | Validate and correct documentation claims | MONTHLY |

### PROC-12X: Safety & Reliability (E07-E09)

| ID | Name | Enhancement | Purpose | Frequency |
|----|------|-------------|---------|-----------|
| [PROC-121](PROC-121-iec62443-safety.md) | IEC 62443 Safety | E07 | Map equipment to Purdue zones, calculate SL gaps | MONTHLY |
| [PROC-122](PROC-122-rams-reliability.md) | RAMS Reliability | E08 | Calculate MTBF, MTTR, availability metrics | WEEKLY |
| [PROC-123](PROC-123-hazard-fmea.md) | Hazard & FMEA | E09 | Risk Priority Numbers and hazard analysis | MONTHLY |

### PROC-13X: Economic & Strategic (E10-E13)

| ID | Name | Enhancement | Purpose | Frequency |
|----|------|-------------|---------|-----------|
| [PROC-131](PROC-131-economic-impact.md) | Economic Impact | E10 | Breach cost and ROI modeling | MONTHLY |
| [PROC-132](PROC-132-psychohistory-demographics.md) | Psychohistory | E11 | Population segmentation and Seldon crisis | WEEKLY |
| [PROC-133](PROC-133-now-next-never.md) | NOW/NEXT/NEVER | E12 | Composite priority scoring (315K→127 CVEs) | DAILY |
| [PROC-134](PROC-134-attack-path-modeling.md) | Attack Path Modeling | E13 | 8-hop chain traversal and choke points | DAILY |

### PROC-14X: Technical Analysis (E14-E16)

| ID | Name | Enhancement | Purpose | Frequency |
|----|------|-------------|---------|-----------|
| [PROC-141](PROC-141-lacanian-real-imaginary.md) | Lacanian RSI | E14 | Real/Imaginary/Symbolic register mapping | MONTHLY |
| [PROC-142](PROC-142-vendor-equipment.md) | Vendor Equipment | E15 | Map vendors (Siemens, Alstom) to equipment | WEEKLY |
| [PROC-143](PROC-143-protocol-analysis.md) | Protocol Analysis | E16 | Industrial protocol vulnerability analysis | WEEKLY |

### PROC-15X: Psychometric Extensions (E17-E21)

| ID | Name | Enhancement | Purpose | Frequency |
|----|------|-------------|---------|-----------|
| [PROC-151](PROC-151-lacanian-dyad.md) | Lacanian Dyad | E17 | Defender-attacker psychological mirroring | WEEKLY |
| [PROC-152](PROC-152-triad-group-dynamics.md) | Triad Dynamics | E18 | RSI triad and Borromean knot analysis | WEEKLY |
| [PROC-153](PROC-153-organizational-blind-spots.md) | Blind Spots | E19 | Organizational pathology detection | WEEKLY |
| [PROC-154](PROC-154-personality-team-fit.md) | Team Fit Calculus | E20 | 16D personality vectors for hiring | WEEKLY |
| [PROC-155](PROC-155-transcript-psychometric-ner.md) | Transcript NER | E21 | Extract psychometrics from transcripts | DAILY |

### PROC-16X: Advanced Analytics (E22-E26)

| ID | Name | Enhancement | Purpose | Frequency |
|----|------|-------------|---------|-----------|
| [PROC-161](PROC-161-seldon-crisis-prediction.md) | Seldon Crisis | E22 | Crisis prediction (Ψ×V×E formula) | DAILY |
| [PROC-162](PROC-162-population-event-forecasting.md) | Population Forecasting | E23 | 10-agent swarm for population-level prediction | DAILY |
| [PROC-163](PROC-163-cognitive-dissonance-breaking.md) | Cognitive Dissonance | E24 | Belief-behavior-outcome gap detection | WEEKLY |
| [PROC-164](PROC-164-threat-actor-personality.md) | Threat Actor Personality | E25 | Big Five + Dark Triad profiling | WEEKLY |
| [PROC-165](PROC-165-mckenney-lacan-calculus.md) | McKenney-Lacan Calculus | E26 | **CAPSTONE**: Unified Q1-Q10 + RSI integration | WEEKLY |

### PROC-2XX-5XX: Attack Chain Pipeline

| ID | Name | Enhancement | Purpose | Frequency |
|----|------|-------------|---------|-----------|
| [PROC-201](PROC-201-cwe-capec-linker.md) | CWE-CAPEC Linker | - | Create EXPLOITS_WEAKNESS relationships | MONTHLY |
| [PROC-301](PROC-301-capec-attack-mapper.md) | CAPEC-ATT&CK Mapper | - | Create USES_TECHNIQUE relationships | QUARTERLY |
| [PROC-501](PROC-501-threat-actor-enrichment.md) | Threat Actor Enrichment | - | Load threat actors with psychometrics | MONTHLY |

### PROC-9XX: Validation & Maintenance

| ID | Name | Enhancement | Purpose | Frequency |
|----|------|-------------|---------|-----------|
| [PROC-901](PROC-901-attack-chain-builder.md) | Attack Chain Validator | - | Validate complete 8-hop chain | DAILY |

---

## Pipeline Dependency Graph

```
                              ┌─────────────────────────────────────────────┐
                              │          PROC-001 Schema Migration          │
                              │              (FIRST - RUN ONCE)              │
                              └────────────────────┬────────────────────────┘
                                                   │
          ┌────────────────────────────────────────┼────────────────────────────────────────┐
          │                                        │                                        │
          ▼                                        ▼                                        ▼
┌─────────────────┐                     ┌─────────────────┐                     ┌─────────────────┐
│  PROC-101-117   │                     │  PROC-121-134   │                     │  PROC-141-155   │
│  Core ETL       │                     │  Safety/Econ    │                     │  Psychometric   │
│  (E01-E06)      │                     │  (E07-E13)      │                     │  (E14-E21)      │
└────────┬────────┘                     └────────┬────────┘                     └────────┬────────┘
         │                                       │                                       │
         └───────────────────────────────────────┼───────────────────────────────────────┘
                                                 │
                                                 ▼
                              ┌─────────────────────────────────────────────┐
                              │              PROC-201 CWE-CAPEC             │
                              │           EXPLOITS_WEAKNESS links           │
                              └────────────────────┬────────────────────────┘
                                                   │
                                                   ▼
                              ┌─────────────────────────────────────────────┐
                              │            PROC-301 CAPEC-ATT&CK            │
                              │            USES_TECHNIQUE links             │
                              └────────────────────┬────────────────────────┘
                                                   │
                                                   ▼
                              ┌─────────────────────────────────────────────┐
                              │           PROC-501 Threat Actors            │
                              │           USES + HAS_PROFILE links          │
                              └────────────────────┬────────────────────────┘
                                                   │
         ┌─────────────────────────────────────────┼─────────────────────────────────────────┐
         │                                         │                                         │
         ▼                                         ▼                                         ▼
┌─────────────────┐                     ┌─────────────────┐                     ┌─────────────────┐
│  PROC-161-164   │                     │  PROC-165       │                     │  PROC-901       │
│  Adv Analytics  │                     │  McKenney-Lacan │                     │  Chain Validator│
│  (E22-E25)      │                     │  CAPSTONE (E26) │                     │  (FINAL)        │
└─────────────────┘                     └─────────────────┘                     └─────────────────┘
```

---

## McKenney Question Coverage Matrix

| Procedure | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|-----------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|
| **Core Pipeline** |
| PROC-101 CVE | - | - | ✓ | - | ✓ | ✓ | ✓ | ✓ | - | - |
| PROC-111 APT | - | - | ✓ | ✓ | ✓ | ✓ | ✓ | - | - | - |
| PROC-112 STIX | - | - | ✓ | ✓ | ✓ | - | ✓ | - | - | - |
| PROC-113 SBOM | ✓ | ✓ | - | - | ✓ | - | - | ✓ | - | - |
| PROC-114 Psycho | - | - | - | ✓ | - | - | ✓ | - | - | - |
| PROC-115 Feeds | - | - | ✓ | - | ✓ | ✓ | ✓ | - | - | - |
| PROC-116 Dash | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - | - |
| PROC-117 Wiki | - | - | - | - | - | - | - | - | ✓ | - |
| **Safety/Reliability** |
| PROC-121 IEC | ✓ | ✓ | - | - | ✓ | - | - | ✓ | - | - |
| PROC-122 RAMS | ✓ | - | - | - | ✓ | ✓ | ✓ | ✓ | - | - |
| PROC-123 FMEA | - | - | - | - | ✓ | - | ✓ | ✓ | - | - |
| **Economic/Strategic** |
| PROC-131 Econ | - | - | - | - | - | ✓ | ✓ | ✓ | - | - |
| PROC-132 Demo | - | ✓ | - | - | - | - | ✓ | - | - | ✓ |
| PROC-133 NNN | - | - | ✓ | - | ✓ | - | ✓ | ✓ | - | - |
| PROC-134 Path | - | - | ✓ | ✓ | ✓ | - | ✓ | ✓ | - | - |
| **Technical** |
| PROC-141 RSI | - | - | - | ✓ | - | - | ✓ | - | - | - |
| PROC-142 Vendor | ✓ | ✓ | - | - | ✓ | - | - | ✓ | - | - |
| PROC-143 Proto | ✓ | - | ✓ | ✓ | ✓ | - | - | - | - | - |
| **Psychometric** |
| PROC-151 Dyad | - | - | - | ✓ | - | - | ✓ | - | - | ✓ |
| PROC-152 Triad | - | - | - | ✓ | - | - | ✓ | - | - | ✓ |
| PROC-153 Blind | - | - | - | - | - | - | ✓ | ✓ | ✓ | ✓ |
| PROC-154 Team | - | - | - | ✓ | - | - | ✓ | ✓ | - | ✓ |
| PROC-155 NER | - | - | - | ✓ | - | - | ✓ | - | - | - |
| **Advanced Analytics** |
| PROC-161 Seldon | - | - | - | - | - | - | ✓ | ✓ | - | ✓ |
| PROC-162 Pop | - | ✓ | - | - | - | - | ✓ | - | - | ✓ |
| PROC-163 Cog | - | - | - | - | - | - | ✓ | ✓ | ✓ | ✓ |
| PROC-164 Actor | - | - | ✓ | ✓ | ✓ | - | ✓ | - | - | - |
| **CAPSTONE** |
| PROC-165 MCL | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PROC-901 Valid | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - | - |

**McKenney Questions**:
- Q1: What equipment do we have?
- Q2: What equipment do our customers have?
- Q3: What do attackers know about our vulnerabilities?
- Q4: Who are the attackers and what are their motivations?
- Q5: How can we defend ourselves?
- Q6: What has happened before?
- Q7: What will happen next?
- Q8: What should we do?
- Q9: How do we communicate?
- Q10: How do populations/groups behave?

---

## Enhancement to Procedure Mapping

| Enhancement | ID | Procedure | Category |
|-------------|:--:|-----------|----------|
| APT Threat Intel | E01 | PROC-111 | Core ETL |
| STIX Integration | E02 | PROC-112 | Core ETL |
| SBOM Analysis | E03 | PROC-113 | Core ETL |
| Psychometric Integration | E04 | PROC-114 | Core ETL |
| RealTime Feeds | E05 | PROC-115 | Core ETL |
| Executive Dashboard | E06a | PROC-116 | Core ETL |
| Wiki Truth Correction | E06b | PROC-117 | Core ETL |
| IEC 62443 Safety | E07 | PROC-121 | Safety |
| RAMS Reliability | E08 | PROC-122 | Safety |
| Hazard FMEA | E09 | PROC-123 | Safety |
| Economic Impact | E10 | PROC-131 | Economic |
| Psychohistory Demographics | E11 | PROC-132 | Economic |
| NOW/NEXT/NEVER | E12 | PROC-133 | Economic |
| Attack Path Modeling | E13 | PROC-134 | Economic |
| Lacanian Real/Imaginary | E14 | PROC-141 | Technical |
| Vendor Equipment | E15 | PROC-142 | Technical |
| Protocol Analysis | E16 | PROC-143 | Technical |
| Lacanian Dyad | E17 | PROC-151 | Psychometric |
| Triad Group Dynamics | E18 | PROC-152 | Psychometric |
| Organizational Blind Spots | E19 | PROC-153 | Psychometric |
| Personality Team Fit | E20 | PROC-154 | Psychometric |
| Transcript Psychometric NER | E21 | PROC-155 | Psychometric |
| Seldon Crisis Prediction | E22 | PROC-161 | Advanced |
| Population Event Forecasting | E23 | PROC-162 | Advanced |
| Cognitive Dissonance Breaking | E24 | PROC-163 | Advanced |
| Threat Actor Personality | E25 | PROC-164 | Advanced |
| McKenney-Lacan Calculus | E26 | PROC-165 | **CAPSTONE** |

---

## Quick Reference

### Execution Order (Full Pipeline)

```bash
# Phase 1: Schema Setup
./proc_001_schema_migration.sh

# Phase 2: Core Data (Parallel)
./proc_101_cve_enrichment.sh full &
./proc_111_apt_threat_intel.sh &
./proc_112_stix_integration.sh &
./proc_113_sbom_analysis.sh &
wait

# Phase 3: Chain Building (Sequential)
./proc_201_cwe_capec_linker.sh
./proc_301_capec_attack_mapper.sh
./proc_501_threat_actor_enrichment.sh

# Phase 4: Enhancement Procedures (Parallel by category)
./proc_121_iec62443_safety.sh &
./proc_131_economic_impact.sh &
./proc_141_lacanian_rsi.sh &
./proc_151_lacanian_dyad.sh &
wait

# Phase 5: Advanced Analytics (After dependencies)
./proc_161_seldon_crisis.sh
./proc_165_mckenney_lacan_calculus.sh

# Phase 6: Validation
./proc_901_attack_chain_builder.sh
```

### Environment Variables

```bash
export NEO4J_PASSWORD="neo4j@openspg"
export NEO4J_CONTAINER="openspg-neo4j"
export NVD_API_KEY="your-api-key"
```

---

## Related Documentation

| Document | Location |
|----------|----------|
| Enhancement Index | `../enhancements/README.md` |
| Academic Monograph | `../academic/COMPLETE_ACADEMIC_MONOGRAPH.md` |
| Project Status | `../project_status/00_PROJECT_STATUS_AND_CLARIFICATIONS.md` |
| Schema Analysis | `../technical_specs/SCHEMA_RECONCILIATION_ANALYSIS.md` |
| Gap Analysis | `../GAP_ANALYSIS_COMPREHENSIVE_REPORT.md` |

---

## Template

All procedures follow [00_PROCEDURE_TEMPLATE.md](00_PROCEDURE_TEMPLATE.md).

**ID Ranges**:
- `PROC-0XX`: Schema/Setup
- `PROC-1XX`: Core ETL & Enhancements E01-E06
- `PROC-12X`: Safety (E07-E09)
- `PROC-13X`: Economic (E10-E13)
- `PROC-14X`: Technical (E14-E16)
- `PROC-15X`: Psychometric (E17-E21)
- `PROC-16X`: Advanced Analytics (E22-E26)
- `PROC-2XX`: CWE/CAPEC
- `PROC-3XX`: ATT&CK
- `PROC-5XX`: Threat Intelligence
- `PROC-9XX`: Validation

---

**Version 2.0.0** - Complete with 34 procedures covering all 26 enhancements
