# Enhancement Dependency Graph

**File:** 01_ENHANCEMENT_DEPENDENCY_GRAPH.md
**Created:** 2025-12-03
**Purpose:** Visual and structural representation of enhancement dependencies

---

## Dependency Overview

### Tier Structure

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           TIER 1: FOUNDATION (E01-E05)                          │
│                                                                                 │
│  E01 APT Intel ─────┬───────► E02 STIX ─────┬───────► E03 SBOM                  │
│        │            │              │        │              │                    │
│        ▼            │              ▼        │              ▼                    │
│  ThreatActor     STIX Parser    MITRE    SBOM Parser   Dependencies            │
│  Nodes           Integration    Links    CVE-Package   Mapping                  │
│                     │                       │                                   │
│                     └───────────────────────┴──────────► E05 Real-Time Feeds   │
│                                                                   │              │
│  E04 Psychometric ◄────────────────────────────────────────────────┘            │
│        │                                                                        │
│        └─────────────────────► Foundation for E14-E26                           │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                         TIER 2: VISUALIZATION (E06-E09)                         │
│                                                                                 │
│  E06b Wiki Truth ─────► Critical Data Quality                                  │
│        │                       │                                                │
│        ▼                       ▼                                                │
│  E06a Dashboard ◄──────────────┴──────────► E07 IEC 62443                       │
│        │                                         │                              │
│        │                                         ▼                              │
│        │                                    E08 RAMS ───────► E09 FMEA          │
│        └─────────────────────────────────────────┴───────────────┘              │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                          TIER 3: ECONOMIC (E10-E13)                             │
│                                                                                 │
│  E10 Economic ◄───────────────────────────────────────────────────────────────┐ │
│        │                                                                      │ │
│        ▼                                                                      │ │
│  E11 Demographics ─────────────────────────────────────────────────────────┐  │ │
│        │                                                                   │  │ │
│        ▼                                                                   │  │ │
│  E12 NOW/NEXT/NEVER ◄──── CVE Prioritization ◄─────┐                       │  │ │
│        │                                           │                       │  │ │
│        ▼                                           │                       │  │ │
│  E13 Attack Path ─────────────────────────────────┴────────────────────────┴──┘ │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                         TIER 4: PSYCHOMETRIC (E14-E26)                          │
│                                                                                 │
│  ┌─── E14 Lacanian RSI ◄──── E04 Psychometric                                  │
│  │          │                                                                   │
│  │          ▼                                                                   │
│  │    E17 Dyad Analysis ─────────► E18 Triad Dynamics                          │
│  │          │                            │                                      │
│  │          ▼                            ▼                                      │
│  │    E19 Blind Spots ◄──────────────────┤                                     │
│  │          │                            │                                      │
│  │          ▼                            ▼                                      │
│  │    E20 Team Fit ◄──────────── E21 Transcript NER                            │
│  │                                       │                                      │
│  │                                       ▼                                      │
│  │    E15 Vendor Equipment ◄──── E16 Protocol Analysis                         │
│  │                                       │                                      │
│  │                                       ▼                                      │
│  │    E22 Seldon Crisis ◄─────── E23 Population Forecasting                    │
│  │          │                            │                                      │
│  │          ▼                            ▼                                      │
│  │    E24 Cognitive ◄────────── E25 Threat Actor Personality                   │
│  │          │                            │                                      │
│  │          └────────────────────────────┴───────────────────┐                  │
│  │                                                           ▼                  │
│  └───────────────────────────────────────────────► E26 McKenney-Lacan          │
│                                                    (CAPSTONE)                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                          TIER 5: COMPLETE (E27, E30)                            │
│                                                                                 │
│  E27 Entity Expansion ────────────────────────────────────────► COMPLETE       │
│        │                                                                        │
│        ▼                                                                        │
│  E30 NER11 Gold Integration ──────────────────────────────────► COMPLETE       │
│                                                                                 │
│  (These provide foundation for all other enhancements)                          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Critical Path Analysis

### Blocking Dependencies

| Enhancement | Blocked By | Blocking |
|-------------|------------|----------|
| E01 APT Intel | None | E02, E05 |
| E02 STIX | E01 | E03, E05 |
| E03 SBOM | E02 | E05 |
| E04 Psychometric | None | E14-E26 |
| E05 Real-Time | E01-E03 | E06a |
| E06b Wiki Truth | None | E06a (data quality) |
| E07 IEC 62443 | None | E08, E09 |
| E12 NOW/NEXT/NEVER | CVE database | None |
| E14-E21 | E04 | E22-E25 |
| E22-E25 | E14-E21 | E26 |
| E26 McKenney-Lacan | E14-E25 | None (CAPSTONE) |
| E27 Entity Expansion | None | ALL (foundation) |
| E30 NER11 Gold | E27 | ALL (data source) |

### Recommended Implementation Sequence

1. **Phase 1 (Foundation)**: E27 ✅, E30 ✅, E06b, E01, E07
2. **Phase 2 (Core)**: E02, E04, E05, E12
3. **Phase 3 (Technical)**: E03, E15, E16, E13
4. **Phase 4 (Psychometric)**: E14, E17-E21
5. **Phase 5 (Advanced)**: E22-E25
6. **Phase 6 (Capstone)**: E26

---

## Links

- [Master Report](00_MASTER_RATIONALIZATION_REPORT.md)
- [API Roadmap](02_API_IMPLEMENTATION_ROADMAP.md)
- [Procedures Overview](03_PROCEDURES_OVERVIEW.md)
