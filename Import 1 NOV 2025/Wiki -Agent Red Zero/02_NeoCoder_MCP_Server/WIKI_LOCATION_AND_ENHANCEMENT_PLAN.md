---
title: NeoCoder Wiki - Location and Enhancement Plan
category: General
last_updated: 2025-10-25
line_count: 288
status: published
tags: [neocoder, mcp, documentation]
---

# NeoCoder Wiki - Location and Enhancement Plan

**Date:** 2025-10-24
**Location:** `/Users/jim/Documents/5_AgentZero/data/NeoCoder/`
**Status:** Foundation Complete + Enhancement Plan Ready

---

## Wiki Location

The NeoCoder wiki has been copied to the AgentZero data directory:

```
/Users/jim/Documents/5_AgentZero/data/NeoCoder/
```

This location integrates the wiki with the AgentZero container platform deployment.

---

## Current Wiki Status

**Completed Notes:** 3
- `INDEX.md` (142 lines) - Master index with live statistics
- `01_Getting_Started/01_Installation.md` (385 lines) - Complete installation guide
- `01_Getting_Started/02_Quick_Start.md` (361 lines) - Quick start tutorial

**Directory Structure:**
```
NeoCoder/
├── INDEX.md
├── 01_Getting_Started/
│   ├── 01_Installation.md ✅
│   ├── 02_Quick_Start.md ✅
│   └── 03_First_Project.md ⏳
├── 02_Core_Concepts/
├── 03_Incarnations/
├── 04_Workflows/
├── 05_Tools_Reference/
├── 06_Advanced_Topics/
├── 07_Development/
└── 08_Reference/
```

---

## Critical Enhancement Recommendations

The Wiki Expert (Documentation Specialist) has completed a comprehensive analysis and identified **critical gaps** that must be addressed. The NeoCoder repository is actually the **AgentZero Container Platform** with cybersecurity intelligence features.

### 🔴 CRITICAL GAPS IDENTIFIED

#### 1. **Container Deployment Missing** (CRITICAL)
**Impact:** Users deploying from the actual repository will be confused

**Add New Category:** `00_Deployment/` (5 notes, ~1,800 lines)
- Container deployment guide (Docker Compose with 7 services)
- Multi-database coordination (Neo4j + Qdrant + PostgreSQL)
- Environment configuration
- Service health verification
- Cross-platform deployment

#### 2. **Cybersecurity Intelligence Features Missing** (CRITICAL)
**Impact:** Massive feature gap - this is a core capability not documented

**Add New Category:** `09_Security_Intelligence/` (5 notes, ~1,800 lines)
- CVE Intelligence Ingestion pipeline
- CWE/CAPEC Integration
- CPE Device Matching
- ICS Entity Extraction
- Threat Intelligence Workflows

#### 3. **PostgreSQL Multi-Database Architecture Missing** (CRITICAL)
**Impact:** Key architectural component completely missing

**Topics to Add:**
- 3-database architecture (agentzero, n8n, graphker)
- Database-specific user permissions
- Cross-database query patterns
- GraphKer schema for CVE metadata

---

## Enhanced Wiki Structure Proposal

**Current Plan:** 33 notes, 8 categories, ~10,000 lines
**Enhanced Plan:** 58 notes, 15 categories, ~17,300 lines

### New Categories to Add

```
00_Deployment/ (5 notes)
└─ Container deployment, multi-service orchestration

09_Security_Intelligence/ (5 notes)
└─ CVE/CWE/CAPEC/CPE/ICS workflows

10_Data_Management/ (4 notes)
└─ Backup, recovery, migration, archival

11_Operations/ (4 notes)
└─ Monitoring, diagnostics, troubleshooting, maintenance

12_Integration_Patterns/ (3 notes)
└─ n8n, external APIs, custom connectors
```

### Expanded Existing Categories

- **05_Tools_Reference:** 5 → 8 notes (add PostgreSQL tools, CVE tools, split API docs)
- **08_Reference:** 4 → 9 notes (expand API docs, add schemas, error codes)
- **06_Advanced_Topics:** 4 → 6 notes (add embedding strategies, performance)
- **04_Workflows:** 3 → 5 notes (add security workflows, diagnostics)

---

## Priority Implementation Phases

### Phase 1: Critical Foundation (12 notes)
**Addresses:** Container deployment, security intelligence, database architecture

1. All 5 notes in `00_Deployment/`
2. `09_Security_Intelligence/01_CVE_Pipeline.md`
3. `09_Security_Intelligence/04_ICS_Entity_Extraction.md`
4. `02_Core_Concepts/05_Multi_Database_Architecture.md`
5. `11_Operations/01_Diagnostics.md`
6. `08_Reference/05_Database_Schemas.md`
7. `05_Tools_Reference/06_PostgreSQL_Tools.md`
8. `01_Getting_Started/04_Container_Quick_Start.md`

### Phase 2: High-Value Features (15 notes)
**Addresses:** Complete security intelligence, operations, data management

- Complete `09_Security_Intelligence/` (4 remaining notes)
- Complete `11_Operations/` (3 remaining notes)
- Complete `10_Data_Management/` (all 4 notes)
- Expand `05_Tools_Reference/` (3 additional notes)
- Expand `08_Reference/` (1 additional note)

### Phase 3: Integration & Advanced (10 notes)
**Addresses:** Integration patterns, advanced topics, development

- Complete `12_Integration_Patterns/` (3 notes)
- Complete `06_Advanced_Topics/` additions (2 notes)
- Complete `04_Workflows/` additions (2 notes)
- Complete `07_Development/` addition (1 note)
- Complete `08_Reference/` additions (2 notes)

### Phase 4: Original Plan Completion (21 notes)
**Addresses:** Complete remaining notes from original 33-note plan

---

## User Persona Coverage Analysis

| Persona | Current Coverage | Gaps | Priority |
|---------|------------------|------|----------|
| **New Users** | ✅ Good (Getting Started) | Missing container quick start | HIGH |
| **Developers** | ✅ Good (Development) | Missing testing guide | MEDIUM |
| **Researchers** | ⚠️ Partial (Research incarnation) | Missing CVE workflows | CRITICAL |
| **System Architects** | ❌ Poor | Missing deployment, scaling, ops | CRITICAL |
| **Security Analysts** | ❌ Poor | Missing entire security intelligence | CRITICAL |
| **Data Scientists** | ⚠️ Partial (Vector tools) | Missing embedding workflows | HIGH |
| **DevOps Engineers** | ❌ Poor | Missing monitoring, backup, CI/CD | CRITICAL |

---

## Key Findings from Wiki Expert Analysis

### What's Actually in the NeoCoder Repository

1. **AgentZero Container Platform**
   - 7 containerized services orchestrated by Docker Compose
   - Multi-database architecture (Neo4j, Qdrant, PostgreSQL)
   - Custom networks and volume management

2. **Cybersecurity Intelligence System**
   - CVE data pipeline with embedding generation
   - CWE/CAPEC integration for weakness/attack patterns
   - CPE device vulnerability matching
   - ICS entity extraction from documents

3. **Hybrid Knowledge Graph System**
   - Neo4j for structured knowledge
   - Qdrant for vector embeddings (5 custom collections)
   - PostgreSQL for metadata and CVE data
   - n8n workflow automation

4. **MCP Server Framework**
   - 7 operational incarnations
   - 100+ tools across all components
   - Workflow templates and guidance hubs

### What's Missing from Current Wiki

1. **No container deployment documentation** - Users can't deploy the system
2. **No security intelligence documentation** - Core feature completely undocumented
3. **No multi-database documentation** - PostgreSQL component missing
4. **No operational documentation** - No monitoring, backup, diagnostics guides
5. **Insufficient API documentation** - 100+ tools need comprehensive coverage

---

## Estimated Effort

| Category | Notes Added | Lines Added | Effort (hours) |
|----------|-------------|-------------|----------------|
| Critical Gaps | 19 | ~7,000 | 40-50 |
| High Priority | 6 | ~2,000 | 12-15 |
| Medium Priority | 5 | ~1,500 | 8-10 |
| **Total New Content** | **30** | **~10,500** | **60-75** |
| Original Plan | 33 | ~10,000 | 50-60 |
| **Grand Total** | **63** | **~20,500** | **110-135** |

---

## Next Steps

### Option 1: Implement Critical Foundation (Recommended)
Focus on the 12 critical notes first:
- Container deployment (5 notes)
- Security intelligence basics (2 notes)
- Database architecture (2 notes)
- Operations basics (3 notes)

**Outcome:** Users can deploy and use core features (estimated 30-40 hours)

### Option 2: Complete Enhanced Plan
Implement all 58 notes systematically:
- Phases 1-4 in sequence
- Complete coverage of all features
- Full user persona support

**Outcome:** Comprehensive, production-ready documentation (estimated 110-135 hours)

### Option 3: Hybrid Approach
Complete critical foundation + selected high-priority items:
- Phase 1 (12 notes)
- Selected Phase 2 items (5-7 notes)
- Original plan completion (remaining 31 notes)

**Outcome:** Balanced coverage with critical gaps addressed (estimated 80-100 hours)

---

## Quality Standards Maintained

All enhancement recommendations maintain established wiki standards:

- ✅ **Maximum 400 lines per note** - No note exceeds limit
- ✅ **5-level hierarchy maximum** - All categories within depth limit
- ✅ **Auto-updating indexes** - Master and category indexes
- ✅ **Clear cross-references** - Related topics linked
- ✅ **Proper frontmatter** - Consistent metadata

---

## Files and Resources

### Planning Documents (Original Location)
- `/Users/jim/1_neoblender/NEOCODER_WIKI_PLAN.md` - Original 33-note plan
- `/Users/jim/1_neoblender/WIKI_CREATION_SUMMARY.md` - Progress summary
- `/Users/jim/1_neoblender/tasks.db` - SQLite task tracking

### Wiki Location (Current)
- `/Users/jim/Documents/5_AgentZero/data/NeoCoder/` - Live wiki
- All future wiki development should occur in this location

### Source Repository
- https://github.com/angrysky56/NeoCoder-neo4j-ai-workflow

---

## Conclusion

The wiki expert analysis has revealed that the NeoCoder wiki needs significant expansion to cover:

1. **Container deployment** - Critical for actual usage
2. **Security intelligence** - Core feature completely missing
3. **Multi-database architecture** - PostgreSQL integration undocumented
4. **Operational concerns** - Monitoring, backup, diagnostics missing

**Recommendation:** Implement Phase 1 (Critical Foundation) to make the wiki immediately useful for real deployments, then expand systematically based on user feedback and priorities.

---

**Last Updated:** 2025-10-24 | **Status:** Enhancement plan complete, ready for implementation
