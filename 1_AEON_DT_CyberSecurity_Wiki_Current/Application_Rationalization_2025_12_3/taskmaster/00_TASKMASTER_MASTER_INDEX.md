# TASKMASTER MASTER INDEX

**Version:** 1.0.1
**Created:** 2025-12-03
**Last Updated:** 2025-12-04T03:20:00Z
**Project:** Application Rationalization - AEON DT CyberSecurity Wiki

---

## Decision Record

| Item | Value |
|------|-------|
| **Selected Strategy** | OPTION B - Balanced Foundation MVP |
| **Decision Date** | 2025-12-04T03:15:00Z |
| **MVP Duration** | 62 days |
| **MVP Enhancements** | 6 |
| **Deferred Enhancements** | 13 |
| **Rationale** | Clean architecture, no tech debt, SBOM graphs, real economic data for NOW/NEXT/NEVER |

---

## MVP Overview (Option B)

### Phase Summary

| Phase | Name | Days | Enhancements | Status |
|-------|------|------|--------------|--------|
| **B1** | Structural Foundation | 20 | CUSTOMER_LABELS, E07 | NOT STARTED |
| **B2** | Supply Chain | 24 | E15, E03 | NOT STARTED |
| **B3** | Prioritization | 18 | E10, E12 | NOT STARTED |
| **TOTAL** | **MVP Complete** | **62** | **6** | - |

### MVP Enhancement List

| Order | ID | Name | Phase | Days | Priority | Frontend |
|-------|-----|------|-------|------|----------|----------|
| 1 | CUSTOMER_LABELS | Multi-Tenant Isolation | B1 | 5 | CRITICAL | Yes |
| 2 | E07 | IEC 62443 Industrial Safety | B1 | 15 | CRITICAL | Yes |
| 3 | E15 | Vendor Equipment Tracking | B2 | 12 | HIGH | Yes |
| 4 | E03 | SBOM Dependency Analysis | B2 | 12 | HIGH | Yes |
| 5 | E10 | Economic Impact Analysis | B3 | 10 | HIGH | Yes |
| 6 | E12 | NOW/NEXT/NEVER Prioritization | B3 | 8 | CRITICAL | Yes |

### Frontend-Visible Features (MVP)

1. **Customer Isolation UI** - Multi-tenant dropdowns, data isolation indicators
2. **IEC 62443 Safety Zones** - SL0-SL4 badges, zone hierarchy display
3. **SBOM Dependency Graphs** - npm/PyPI visualization, vulnerability indicators
4. **Economic Impact Dashboard** - ROI calculator, sector comparisons
5. **NOW/NEXT/NEVER CVE Table** - Priority badges, action queue

---

## Deferred Enhancements

### Post-MVP Phase Recommendations

| Phase | Name | Enhancements | Days | Dependencies |
|-------|------|--------------|------|--------------|
| D1 | Safety & Reliability | E08, E09 | 18 | MVP Complete |
| D2 | Advanced Analysis | E11, E13 | 23 | D1 or MVP |
| D3 | Psychometric Core | E19, E20, E21, E24, E25 | 61 | D2 |
| D4 | Experimental Psychohistory | E17, E18, E22, E23 | 60 | D3 |

### Deferred Enhancement Summary (13 total, 162 days)

| ID | Name | Original Phase | Days | Reason |
|----|------|----------------|------|--------|
| E08 | RAMS Reliability | 2 | 10 | Not frontend-visible |
| E09 | Hazard & FMEA | 2 | 8 | Depends on E08 |
| E11 | Psychohistory Demographics | 3 | 8 | Complex, not MVP-critical |
| E13 | Attack Path Modeling | 3 | 15 | Can build on MVP |
| E19 | Organizational Blind Spots | 4 | 12 | Psychometric |
| E20 | Personality-Team Fit | 4 | 12 | Psychometric |
| E21 | Transcript Psychometric NER | 4 | 15 | Requires NER11 |
| E24 | Cognitive Dissonance | 4 | 10 | Advanced intervention |
| E25 | Threat Actor Personality | 4 | 12 | Requires E13, E21 |
| E17 | Lacanian Dyad | 5 | 10 | EXPERIMENTAL |
| E18 | Triad Group Dynamics | 5 | 12 | EXPERIMENTAL |
| E22 | Seldon Crisis Prediction | 5 | 20 | EXPERIMENTAL |
| E23 | Population Forecasting | 5 | 18 | EXPERIMENTAL |

---

## Document Navigation

| Document | Purpose | Status |
|----------|---------|--------|
| [01_IMPLEMENTATION_ORDER.json](./01_IMPLEMENTATION_ORDER.json) | MVP phase structure & dependencies | UPDATED |
| [02_PHASE_DETAILS.md](./02_PHASE_DETAILS.md) | Detailed phase breakdown | UPDATED |
| [03_TASK_SPECIFICATIONS.md](./03_TASK_SPECIFICATIONS.md) | Enhancement specifications | UPDATED |
| [04_PM_CHECKLIST.md](./04_PM_CHECKLIST.md) | Project manager tracking | UPDATED |
| [05_SESSION_HANDOFF.md](./05_SESSION_HANDOFF.md) | Session continuity | UPDATED |
| [../blotter/BLOTTER.md](../blotter/BLOTTER.md) | Activity log | UPDATED |

### Test Framework

| Document | Description | Link |
|----------|-------------|------|
| **Unit Test Template** | Neo4j, data, algorithm tests | [../tests/UNIT_TEST_TEMPLATE.md](../tests/UNIT_TEST_TEMPLATE.md) |
| **Integration Test Template** | Cross-enhancement tests | [../tests/INTEGRATION_TEST_TEMPLATE.md](../tests/INTEGRATION_TEST_TEMPLATE.md) |
| **Acceptance Test Template** | Business requirement tests | [../tests/ACCEPTANCE_TEST_TEMPLATE.md](../tests/ACCEPTANCE_TEST_TEMPLATE.md) |
| **Audit Checklist** | Code/security review | [../tests/AUDIT_CHECKLIST.md](../tests/AUDIT_CHECKLIST.md) |

### Data Sources & Guides

| Document | Description | Link |
|----------|-------------|------|
| **API Research Report** | Kaggle, demographic APIs | [../guides/DATA_SOURCES_GUIDE.md](../guides/DATA_SOURCES_GUIDE.md) |
| **Integration Patterns** | Code examples | [../guides/INTEGRATION_PATTERNS.md](../guides/INTEGRATION_PATTERNS.md) |

---

## Quick Reference

### Start Phase B1 Command
```bash
# Begin CUSTOMER_LABELS implementation
npx claude-flow sparc run architect "Implement CUSTOMER_LABELS multi-tenant isolation in Neo4j"
```

### Check MVP Progress
```bash
# View current phase status
cat taskmaster/04_PM_CHECKLIST.md | grep -E "Phase B[1-3]|IN PROGRESS|COMPLETED"
```

### View Enhancement Details
```bash
# Get detailed specs for any enhancement
cat taskmaster/03_TASK_SPECIFICATIONS.md | grep -A 50 "E07"
```

---

## Timeline Visualization

```
Day 1    Day 5    Day 20   Day 32   Day 44   Day 54   Day 62
|--------|--------|--------|--------|--------|--------|
  CUST     E07       E15      E03      E10      E12
  LABELS   IEC62443  VENDOR   SBOM     ECON     NNN

[========= B1: Foundation =========]
                     [====== B2: Supply Chain ======]
                                      [=== B3: Prioritization ===]
```

---

## Success Criteria

### MVP Completion Requirements
- [ ] All 6 MVP enhancements deployed
- [ ] Customer isolation verified (0 cross-tenant leaks)
- [ ] IEC 62443 zones visible (SL0-SL4)
- [ ] SBOM dependency graphs rendering
- [ ] NOW/NEXT/NEVER reducing CVEs by 99.8%
- [ ] Unit tests passing (>90% coverage)
- [ ] Integration tests passing
- [ ] Acceptance tests signed off

---

## Project Manager Protocol

### Daily Standup Checklist
1. Review BLOTTER.md for previous day's entries
2. Check current task status in PM_CHECKLIST.md
3. Verify test results for completed tasks
4. Update SESSION_HANDOFF.md if session ending
5. Log all activities to BLOTTER.md with timestamp

### Task Completion Requirements
Every task MUST have:
- [ ] All unit tests passing (≥80% coverage)
- [ ] Integration tests passing
- [ ] Acceptance criteria met
- [ ] Audit checklist completed (≥37/41 score)
- [ ] Documentation updated
- [ ] BLOTTER.md entry logged
- [ ] PM_CHECKLIST.md updated
- [ ] Peer review completed

---

## External Data Sources

### MVP Sources (Free Tier)
- World Bank API
- FRED Economic API
- NVD (API key required)
- npm Registry API
- PyPI API
- OSV
- GHSA

### Deferred Sources
- UN Population Division API
- GDELT DOC 2.0 API
- Kaggle Datasets
- VulnCheck API (paid)

See [DATA_SOURCES_GUIDE.md](../guides/DATA_SOURCES_GUIDE.md) for complete details.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-03 | Initial TASKMASTER creation (5 phases, 224 days) |
| 1.0.1 | 2025-12-04 | Option B MVP restructure (3 phases, 62 days, 6 enhancements) |

---

**Generated by Claude-Flow mesh swarm analysis**
**Original Swarm ID:** swarm_1764814789507_ywsdg0lld
**Option B Swarm ID:** swarm_1764818362122_d0cyqviep
