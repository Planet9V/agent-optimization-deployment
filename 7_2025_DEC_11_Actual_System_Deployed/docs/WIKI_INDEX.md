# AEON Knowledge Graph - Complete Wiki Index

**File:** WIKI_INDEX.md
**Created:** 2025-12-12
**Version:** 1.0.0
**Purpose:** Comprehensive wiki-style navigation for all AEON system documentation
**Total Documents:** 21 files

---

## 🧭 Navigation Guide

This wiki index provides **multiple pathways** to find documentation based on your role, task, or learning objective.

**Navigation Methods:**
1. [By User Role](#by-user-role) - Find docs for your job function
2. [By Task Type](#by-task-type) - Find docs for specific activities
3. [By Document Category](#by-document-category) - Browse by topic area
4. [Quick Reference Cards](#quick-reference-cards) - Cheat sheets for common tasks
5. [Learning Paths](#learning-paths) - Structured learning progressions
6. [Search Index](#search-index) - Keyword-based document finder

---

## 🎯 By User Role

### 👤 Database Administrator

**Daily Operations:**
- [System Administration Guide](SYSTEM_ADMINISTRATION_GUIDE.md) - Complete admin manual
- [Maintenance Guide](MAINTENANCE_GUIDE.md) - Daily/weekly/monthly procedures
- `../scripts/quick_diagnostic.sh` - 5-minute health check

**When Things Go Wrong:**
- [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) - Issue resolution procedures
- [Verification Summary](VERIFICATION_SUMMARY_2025-12-12.md) - Database validation

**Understanding the System:**
- [Complete Schema Reference](COMPLETE_SCHEMA_REFERENCE.md) - All 631 labels, 183 relationships
- [Actual Schema Implemented](ACTUAL_SCHEMA_IMPLEMENTED.md) - Neo4j v3.1 hierarchical design

---

### 👤 Data Engineer / Pipeline Operator

**Essential Reading:**
- [Pipeline Usage Guide](PIPELINE_USAGE_GUIDE.md) - **START HERE** - How to use E30 pipeline
- [Pipeline Operations Guide](PIPELINE_OPERATIONS_GUIDE.md) - Operational procedures
- [Pipeline Integration Actual](PIPELINE_INTEGRATION_ACTUAL.md) - Real data flow

**Quick Start:**
- [Quick Start Guide](QUICK_START.md) - 5-minute introduction
- [Solution Summary](SOLUTION_SUMMARY.md) - Architecture overview

**When Pipelines Fail:**
- [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) → Section 3: "Ingestion Pipeline Failures"
- [Maintenance Guide](MAINTENANCE_GUIDE.md) → Section 5: "Adding New Entities Correctly"

---

### 👤 Frontend / Full-Stack Developer

**Integration Guide:**
- [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md) - **START HERE** - Complete integration guide
- [API Complete Reference](API_COMPLETE_REFERENCE.md) - All REST endpoints documented

**Schema Understanding:**
- [Complete Schema Reference](COMPLETE_SCHEMA_REFERENCE.md) - All labels and relationships
- [Relationship Complete Ontology](RELATIONSHIP_COMPLETE_ONTOLOGY.md) - 183 relationship types

**Query Examples:**
- [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md) → Section 4: "Common Query Patterns"
- [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md) → Section 5: "Real Working Examples"

---

### 👤 Architect / Technical Lead

**System Understanding:**
- [Solution Summary](SOLUTION_SUMMARY.md) - **START HERE** - Architecture overview
- [Actual Schema Implemented](ACTUAL_SCHEMA_IMPLEMENTED.md) - Neo4j v3.1 design principles
- [Schema Analysis Summary](SCHEMA_ANALYSIS_SUMMARY.md) - Schema structure analysis

**Migration & Changes:**
- [Final Migration Report](FINAL_MIGRATION_REPORT_2025-12-12.md) - Latest migration status
- [Migration Report](MIGRATION_REPORT.md) - Historical migration details
- [Hierarchical Schema Fix Procedure](HIERARCHICAL_SCHEMA_FIX_PROCEDURE.md) - Schema migration procedure

**Data Model Deep Dive:**
- [Complete Schema Reference](COMPLETE_SCHEMA_REFERENCE.md) - Comprehensive schema documentation
- [Relationship Complete Ontology](RELATIONSHIP_COMPLETE_ONTOLOGY.md) - All relationship types
- [20-Hop Verification](20_HOP_VERIFICATION.md) - Relationship path analysis

---

### 👤 Support Engineer

**First Response:**
- `../scripts/quick_diagnostic.sh` - Run immediately
- [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) → Section 1: "Quick Diagnostic Checklist"

**Issue Categories:**
1. **Schema Issues** → [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) → Section 2
2. **Pipeline Issues** → [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) → Section 3
3. **Performance Issues** → [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) → Section 4
4. **Data Quality Issues** → [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) → Section 5

**Validation Tools:**
- [Verification Summary](VERIFICATION_SUMMARY_2025-12-12.md) - Database health assessment
- `../scripts/VALIDATION_QUERIES.cypher` - 11 validation checks

---

## 📋 By Task Type

### 🚀 Getting Started with AEON

**New to the System?**
1. Read [Quick Start Guide](QUICK_START.md) (5 minutes)
2. Review [Solution Summary](SOLUTION_SUMMARY.md) (15 minutes)
3. Explore [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md) OR [Pipeline Usage Guide](PIPELINE_USAGE_GUIDE.md) based on role

**Setting Up Your Environment:**
- [System Administration Guide](SYSTEM_ADMINISTRATION_GUIDE.md) → Section 3: "Credentials & Access"
- [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md) → Section 2: "Connection Setup"

---

### 📥 Data Ingestion Tasks

**Before You Start:**
- [Pipeline Usage Guide](PIPELINE_USAGE_GUIDE.md) → Section 2: "Prerequisites Check"
- [Pipeline Operations Guide](PIPELINE_OPERATIONS_GUIDE.md) → Section 1: "Pre-Flight Checklist"

**Ingestion Scenarios:**
1. **Single Document** → [Pipeline Usage Guide](PIPELINE_USAGE_GUIDE.md) → Section 3.1
2. **Batch Directory** → [Pipeline Usage Guide](PIPELINE_USAGE_GUIDE.md) → Section 3.2
3. **CSV Data** → [Pipeline Usage Guide](PIPELINE_USAGE_GUIDE.md) → Section 3.3
4. **Re-process Failed** → [Pipeline Usage Guide](PIPELINE_USAGE_GUIDE.md) → Section 3.4
5. **Incremental Daily** → [Pipeline Usage Guide](PIPELINE_USAGE_GUIDE.md) → Section 3.5

**After Ingestion:**
- [Pipeline Usage Guide](PIPELINE_USAGE_GUIDE.md) → Section 4: "Verification Procedures"
- [Maintenance Guide](MAINTENANCE_GUIDE.md) → Section 2: "Daily Health Checks"

---

### 🔍 Querying & Analysis

**Getting Started with Queries:**
- [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md) → Section 4: "Common Query Patterns"
- [API Complete Reference](API_COMPLETE_REFERENCE.md) → Section 3: "Query APIs"

**Schema Reference for Queries:**
- [Complete Schema Reference](COMPLETE_SCHEMA_REFERENCE.md) - All labels and properties
- [Relationship Complete Ontology](RELATIONSHIP_COMPLETE_ONTOLOGY.md) - All relationship types

**Advanced Queries:**
- [20-Hop Verification](20_HOP_VERIFICATION.md) - Multi-hop relationship traversal
- [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md) → Section 5: "Real Working Examples"

---

### 🔧 System Maintenance

**Daily Tasks (5 minutes):**
- Run `../scripts/quick_diagnostic.sh`
- [Maintenance Guide](MAINTENANCE_GUIDE.md) → Section 2: "Daily Health Checks"

**Weekly Tasks (15 minutes):**
- [Maintenance Guide](MAINTENANCE_GUIDE.md) → Section 3: "Weekly Trend Analysis"
- Check ingestion logs for errors

**Monthly Tasks (45 minutes):**
- [Maintenance Guide](MAINTENANCE_GUIDE.md) → Section 4: "Monthly Validation Procedure"
- Run `../scripts/VALIDATION_QUERIES.cypher`
- Review [Verification Summary](VERIFICATION_SUMMARY_2025-12-12.md)

---

### 🐛 Troubleshooting & Debugging

**Quick Diagnosis (5 minutes):**
1. Run `../scripts/quick_diagnostic.sh`
2. [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) → Section 1: "Quick Diagnostic Checklist"

**Issue Resolution by Category:**
- **Schema Drift** → [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) → Section 2
- **Pipeline Failures** → [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) → Section 3
- **Performance Problems** → [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) → Section 4
- **Data Quality** → [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) → Section 5
- **Neo4j Issues** → [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) → Section 6
- **NER11 API Issues** → [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) → Section 7

**Preventive Maintenance:**
- [Maintenance Guide](MAINTENANCE_GUIDE.md) → Section 5: "Schema Drift Detection"
- [Maintenance Guide](MAINTENANCE_GUIDE.md) → Section 6: "Adding New Entities Correctly"

---

### 🔄 Migration & Schema Changes

**Understanding Migrations:**
- [Final Migration Report](FINAL_MIGRATION_REPORT_2025-12-12.md) - Latest migration (Dec 12, 2025)
- [Migration Report](MIGRATION_REPORT.md) - Historical migration details
- [Solution Summary](SOLUTION_SUMMARY.md) - Why migrations were needed

**Executing Migrations:**
- [Hierarchical Schema Fix Procedure](HIERARCHICAL_SCHEMA_FIX_PROCEDURE.md) - Step-by-step procedure
- [Quick Start Guide](QUICK_START.md) - Quick execution (if confident)

**Post-Migration Validation:**
- [Verification Summary](VERIFICATION_SUMMARY_2025-12-12.md) - Validation report
- `../scripts/VALIDATION_QUERIES.cypher` - Run validation checks

---

## 📚 By Document Category

### Category 1: Getting Started

| Document | Purpose | Time | Audience |
|----------|---------|------|----------|
| [Quick Start Guide](QUICK_START.md) | Fast introduction | 5 min | Everyone |
| [Solution Summary](SOLUTION_SUMMARY.md) | Architecture overview | 15 min | Technical leads |
| [System Administration Guide](SYSTEM_ADMINISTRATION_GUIDE.md) | Complete admin manual | 45 min | Admins |

### Category 2: Schema & Data Model

| Document | Purpose | Lines | Audience |
|----------|---------|-------|----------|
| [Complete Schema Reference](COMPLETE_SCHEMA_REFERENCE.md) | All 631 labels, 183 relationships | 2000+ | Architects, Developers |
| [Actual Schema Implemented](ACTUAL_SCHEMA_IMPLEMENTED.md) | Neo4j v3.1 hierarchical design | 800+ | Architects |
| [Relationship Complete Ontology](RELATIONSHIP_COMPLETE_ONTOLOGY.md) | All relationship types documented | 1500+ | Architects, Developers |
| [Relationship Ontology](RELATIONSHIP_ONTOLOGY.md) | Relationship patterns (legacy) | 500+ | Developers |
| [Schema Analysis Summary](SCHEMA_ANALYSIS_SUMMARY.md) | Schema structure analysis | 300+ | Architects |

### Category 3: API & Integration

| Document | Purpose | Lines | Audience |
|----------|---------|-------|----------|
| [API Complete Reference](API_COMPLETE_REFERENCE.md) | All REST endpoints | 1200+ | Frontend Developers |
| [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md) | Complete integration guide | 900+ | Frontend Developers |
| [20-Hop Verification](20_HOP_VERIFICATION.md) | Relationship path analysis | 400+ | Developers, Architects |

### Category 4: Operations & Pipelines

| Document | Purpose | Lines | Audience |
|----------|---------|-------|----------|
| [Pipeline Usage Guide](PIPELINE_USAGE_GUIDE.md) | How to use E30 pipeline | 600+ | Data Engineers |
| [Pipeline Operations Guide](PIPELINE_OPERATIONS_GUIDE.md) | Operational procedures | 500+ | Data Engineers |
| [Pipeline Integration Actual](PIPELINE_INTEGRATION_ACTUAL.md) | Real data flow | 400+ | Data Engineers, Architects |
| [Maintenance Guide](MAINTENANCE_GUIDE.md) | Daily/weekly/monthly tasks | 700+ | Admins, Data Engineers |

### Category 5: Migration & Changes

| Document | Purpose | Lines | Audience |
|----------|---------|-------|----------|
| [Final Migration Report](FINAL_MIGRATION_REPORT_2025-12-12.md) | Latest migration status | 500+ | Architects, Admins |
| [Migration Report](MIGRATION_REPORT.md) | Historical migrations | 400+ | Architects |
| [Hierarchical Schema Fix Procedure](HIERARCHICAL_SCHEMA_FIX_PROCEDURE.md) | Schema migration guide | 500+ | Admins, Data Engineers |
| [Verification Summary](VERIFICATION_SUMMARY_2025-12-12.md) | Database validation | 300+ | Admins |

### Category 6: Troubleshooting & Support

| Document | Purpose | Lines | Audience |
|----------|---------|-------|----------|
| [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) | Complete issue resolution | 800+ | Support, Admins |
| [Documentation Index](DOCUMENTATION_INDEX.md) | Original doc index (legacy) | 435 | Everyone |

---

## 🎴 Quick Reference Cards

### Card 1: Top 10 Most Useful Queries

```cypher
-- 1. Check system health
MATCH (n) WITH count(n) as nodes
MATCH ()-[r]->() RETURN nodes, count(r) as relationships;

-- 2. Super label coverage check
MATCH (n) WHERE n.super_label IS NOT NULL
RETURN count(n) as enriched, (count(n) * 100.0 / 1207032) as coverage_pct;

-- 3. Tier distribution
MATCH (n) WHERE n.tier IS NOT NULL
RETURN n.tier, count(n) ORDER BY count(n) DESC;

-- 4. Top threat actors
MATCH (t:ThreatActor)
RETURN t.name, t.actorType, t.sophistication
ORDER BY t.sophistication DESC LIMIT 10;

-- 5. CVE vulnerability analysis
MATCH (v:CVE)
WHERE v.cvss_score > 7.0
RETURN v.name, v.cvss_score, v.description
ORDER BY v.cvss_score DESC LIMIT 20;

-- 6. Find related entities (1-hop)
MATCH (n {name: "APT28"})-[r]-(m)
RETURN type(r) as relationship, labels(m) as target_labels, count(m) as count
ORDER BY count DESC;

-- 7. Multi-hop threat chain
MATCH path = (threat:ThreatActor)-[*1..3]-(vuln:CVE)
RETURN threat.name, vuln.name, length(path) as hops
LIMIT 10;

-- 8. Asset vulnerability exposure
MATCH (a:Asset)-[:INSTALLED_ON|RUNS_ON*1..2]-(v:CVE)
RETURN a.name, count(DISTINCT v) as vulnerabilities
ORDER BY vulnerabilities DESC LIMIT 20;

-- 9. Schema validation - check for orphan nodes
MATCH (n) WHERE NOT (n)--()
RETURN labels(n), count(n) as orphans;

-- 10. Hierarchical property coverage
MATCH (n) WHERE n.tier1 IS NOT NULL
WITH count(n) as tier1_nodes
MATCH (n) WHERE n.tier2 IS NOT NULL
WITH tier1_nodes, count(n) as tier2_nodes
MATCH (n)
RETURN tier1_nodes, tier2_nodes, count(n) as total_nodes,
       (tier1_nodes * 100.0 / count(n)) as tier1_pct,
       (tier2_nodes * 100.0 / count(n)) as tier2_pct;
```

---

### Card 2: Common Operations Cheat Sheet

**System Health Check (5 minutes):**
```bash
# Quick diagnostic
/home/jim/2_OXOT_Projects_Dev/scripts/quick_diagnostic.sh

# Full validation
cypher-shell -u neo4j -p neo4j@openspg < \
  /home/jim/2_OXOT_Projects_Dev/7_2025_DEC_11_Actual_System_Deployed/scripts/VALIDATION_QUERIES.cypher
```

**Data Ingestion:**
```bash
# Single document
python3 /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_hierarchical.py \
  --file /path/to/document.txt

# Batch directory
python3 /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_hierarchical.py \
  --directory /path/to/docs --pattern "*.txt"

# CSV data
python3 /home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/05_ner11_to_neo4j_hierarchical.py \
  --csv /path/to/data.csv
```

**Database Backup:**
```bash
# Stop Neo4j
sudo systemctl stop neo4j

# Create backup
sudo cp -r /var/lib/neo4j/data/databases/neo4j \
  /var/lib/neo4j/data/databases/neo4j.backup.$(date +%Y%m%d_%H%M%S)

# Start Neo4j
sudo systemctl start neo4j
```

**Check Service Status:**
```bash
# Neo4j status
systemctl status neo4j

# Qdrant status
curl http://localhost:6333/health

# NER11 API status
curl http://localhost:8000/health
```

---

### Card 3: API Quick Reference

**Base URLs:**
- Neo4j: `bolt://localhost:7687`
- Qdrant: `http://localhost:6333`
- NER11 API: `http://localhost:8000`

**Common API Endpoints:**

```bash
# Health checks
GET http://localhost:8000/health
GET http://localhost:6333/health

# NER extraction
POST http://localhost:8000/api/extract
{
  "text": "APT28 exploited CVE-2021-44228",
  "return_embeddings": true
}

# Semantic search
POST http://localhost:6333/collections/cybersecurity_entities/points/search
{
  "vector": [...],
  "limit": 10,
  "with_payload": true
}

# Neo4j query (via Python driver)
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j@openspg"))
with driver.session() as session:
    result = session.run("MATCH (n:ThreatActor) RETURN n.name LIMIT 10")
```

See [API Complete Reference](API_COMPLETE_REFERENCE.md) for full documentation.

---

### Card 4: Troubleshooting Decision Tree

```
ISSUE DETECTED
    ↓
RUN quick_diagnostic.sh
    ↓
┌─────────────────────────────────────────┐
│ What type of issue?                     │
├─────────────────────────────────────────┤
│ 1. Schema drift / missing properties    │ → Section 2 of Troubleshooting Guide
│ 2. Pipeline failure / ingestion error   │ → Section 3 of Troubleshooting Guide
│ 3. Slow queries / performance           │ → Section 4 of Troubleshooting Guide
│ 4. Data quality / incorrect data        │ → Section 5 of Troubleshooting Guide
│ 5. Neo4j service down / won't start     │ → Section 6 of Troubleshooting Guide
│ 6. NER11 API not responding             │ → Section 7 of Troubleshooting Guide
└─────────────────────────────────────────┘
    ↓
Follow specific section procedures
    ↓
VALIDATE FIX
    ↓
Run quick_diagnostic.sh again
```

---

## 🎓 Learning Paths

### Path 1: New Administrator (Week 1)

**Day 1: System Overview**
- [ ] Read [Quick Start Guide](QUICK_START.md) (5 min)
- [ ] Review [Solution Summary](SOLUTION_SUMMARY.md) (15 min)
- [ ] Skim [System Administration Guide](SYSTEM_ADMINISTRATION_GUIDE.md) (30 min)

**Day 2: Daily Operations**
- [ ] Practice running `quick_diagnostic.sh`
- [ ] Read [Maintenance Guide](MAINTENANCE_GUIDE.md) → Daily Health Checks
- [ ] Execute sample validation queries

**Day 3: Schema Understanding**
- [ ] Read [Actual Schema Implemented](ACTUAL_SCHEMA_IMPLEMENTED.md)
- [ ] Explore [Complete Schema Reference](COMPLETE_SCHEMA_REFERENCE.md)
- [ ] Practice querying different label types

**Day 4: Troubleshooting**
- [ ] Read [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md)
- [ ] Practice quick diagnostic procedures
- [ ] Simulate fixing schema drift issue

**Day 5: Validation & Maintenance**
- [ ] Run full validation with VALIDATION_QUERIES.cypher
- [ ] Review [Verification Summary](VERIFICATION_SUMMARY_2025-12-12.md)
- [ ] Practice weekly and monthly maintenance procedures

---

### Path 2: New Data Engineer (Week 1)

**Day 1: Pipeline Overview**
- [ ] Read [Quick Start Guide](QUICK_START.md) (5 min)
- [ ] Read [Pipeline Usage Guide](PIPELINE_USAGE_GUIDE.md) (30 min)
- [ ] Review [Pipeline Integration Actual](PIPELINE_INTEGRATION_ACTUAL.md) (20 min)

**Day 2: First Ingestion**
- [ ] Set up test data directory
- [ ] Practice single document ingestion
- [ ] Verify results with queries

**Day 3: Batch Operations**
- [ ] Practice batch directory ingestion
- [ ] Practice CSV data ingestion
- [ ] Monitor ingestion logs

**Day 4: Troubleshooting Pipelines**
- [ ] Read [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) → Section 3
- [ ] Practice handling ingestion failures
- [ ] Learn to read error logs

**Day 5: Advanced Operations**
- [ ] Read [Pipeline Operations Guide](PIPELINE_OPERATIONS_GUIDE.md)
- [ ] Practice incremental daily ingestion
- [ ] Learn to optimize pipeline performance

---

### Path 3: New Frontend Developer (Week 1)

**Day 1: Integration Basics**
- [ ] Read [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md) → Sections 1-2
- [ ] Set up local development environment
- [ ] Test Neo4j and Qdrant connections

**Day 2: Schema Understanding**
- [ ] Read [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md) → Section 3 (Data Models)
- [ ] Review [Complete Schema Reference](COMPLETE_SCHEMA_REFERENCE.md)
- [ ] Practice basic Cypher queries

**Day 3: Query Patterns**
- [ ] Read [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md) → Section 4
- [ ] Practice common query patterns
- [ ] Test real working examples from Section 5

**Day 4: API Integration**
- [ ] Read [API Complete Reference](API_COMPLETE_REFERENCE.md)
- [ ] Test NER11 API endpoints
- [ ] Practice semantic search with Qdrant

**Day 5: Advanced Queries**
- [ ] Review [20-Hop Verification](20_HOP_VERIFICATION.md)
- [ ] Practice multi-hop relationship queries
- [ ] Build sample application feature

---

## 🔎 Search Index

### By Keyword

**A**
- API: [API Complete Reference](API_COMPLETE_REFERENCE.md)
- Architecture: [Solution Summary](SOLUTION_SUMMARY.md), [Actual Schema Implemented](ACTUAL_SCHEMA_IMPLEMENTED.md)

**B**
- Backup: [System Administration Guide](SYSTEM_ADMINISTRATION_GUIDE.md), [Maintenance Guide](MAINTENANCE_GUIDE.md)

**C**
- CVE: [Complete Schema Reference](COMPLETE_SCHEMA_REFERENCE.md), [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md)
- Cypher Queries: [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md), [Quick Reference Cards](#card-1-top-10-most-useful-queries)

**D**
- Data Ingestion: [Pipeline Usage Guide](PIPELINE_USAGE_GUIDE.md), [Pipeline Operations Guide](PIPELINE_OPERATIONS_GUIDE.md)
- Database: [System Administration Guide](SYSTEM_ADMINISTRATION_GUIDE.md), [Maintenance Guide](MAINTENANCE_GUIDE.md)

**E**
- Entity Extraction: [Pipeline Integration Actual](PIPELINE_INTEGRATION_ACTUAL.md)
- Errors: [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md)

**H**
- Health Check: [Maintenance Guide](MAINTENANCE_GUIDE.md), [Quick Reference Cards](#card-2-common-operations-cheat-sheet)
- Hierarchical Schema: [Actual Schema Implemented](ACTUAL_SCHEMA_IMPLEMENTED.md), [Hierarchical Schema Fix Procedure](HIERARCHICAL_SCHEMA_FIX_PROCEDURE.md)

**I**
- Ingestion: [Pipeline Usage Guide](PIPELINE_USAGE_GUIDE.md), [Pipeline Operations Guide](PIPELINE_OPERATIONS_GUIDE.md)

**M**
- Maintenance: [Maintenance Guide](MAINTENANCE_GUIDE.md), [System Administration Guide](SYSTEM_ADMINISTRATION_GUIDE.md)
- Migration: [Final Migration Report](FINAL_MIGRATION_REPORT_2025-12-12.md), [Migration Report](MIGRATION_REPORT.md)

**N**
- Neo4j: [System Administration Guide](SYSTEM_ADMINISTRATION_GUIDE.md), [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md)
- NER11: [Pipeline Integration Actual](PIPELINE_INTEGRATION_ACTUAL.md), [API Complete Reference](API_COMPLETE_REFERENCE.md)

**P**
- Pipeline: [Pipeline Usage Guide](PIPELINE_USAGE_GUIDE.md), [Pipeline Operations Guide](PIPELINE_OPERATIONS_GUIDE.md)
- Performance: [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md), [Maintenance Guide](MAINTENANCE_GUIDE.md)

**Q**
- Qdrant: [Pipeline Integration Actual](PIPELINE_INTEGRATION_ACTUAL.md), [API Complete Reference](API_COMPLETE_REFERENCE.md)
- Queries: [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md), [Quick Reference Cards](#card-1-top-10-most-useful-queries)

**R**
- Relationships: [Relationship Complete Ontology](RELATIONSHIP_COMPLETE_ONTOLOGY.md), [20-Hop Verification](20_HOP_VERIFICATION.md)

**S**
- Schema: [Complete Schema Reference](COMPLETE_SCHEMA_REFERENCE.md), [Actual Schema Implemented](ACTUAL_SCHEMA_IMPLEMENTED.md)
- Super Labels: [Actual Schema Implemented](ACTUAL_SCHEMA_IMPLEMENTED.md), [Hierarchical Schema Fix Procedure](HIERARCHICAL_SCHEMA_FIX_PROCEDURE.md)

**T**
- Troubleshooting: [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md)
- Threat Actor: [Complete Schema Reference](COMPLETE_SCHEMA_REFERENCE.md), [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md)

**V**
- Validation: [Verification Summary](VERIFICATION_SUMMARY_2025-12-12.md), [Maintenance Guide](MAINTENANCE_GUIDE.md)
- Vulnerability: [Complete Schema Reference](COMPLETE_SCHEMA_REFERENCE.md), [Frontend Developer Guide](FRONTEND_DEVELOPER_GUIDE.md)

---

## 📊 Document Statistics

### By Size (Lines)
1. **Complete Schema Reference**: ~2000+ lines
2. **Relationship Complete Ontology**: ~1500+ lines
3. **API Complete Reference**: ~1200+ lines
4. **Frontend Developer Guide**: ~900+ lines
5. **Actual Schema Implemented**: ~800+ lines

### By Audience

**For Everyone:**
- Quick Start Guide
- Documentation Index (this file)

**For Technical Users:**
- 15 documents covering schema, APIs, operations, troubleshooting

**For Architects Only:**
- 5 documents covering design, migrations, deep schema analysis

### By Frequency of Use

**Daily:**
- Quick Reference Cards
- Maintenance Guide → Daily Checks
- Troubleshooting Guide

**Weekly:**
- Maintenance Guide → Weekly Trend Analysis
- Pipeline Usage Guide

**Monthly:**
- Verification Summary
- Complete Schema Reference
- System Administration Guide

---

## 🔗 External Resources

### Related Repositories
- NER11 Gold Model: `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/`
- Pipeline Scripts: `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/pipelines/`
- Validation Reports: `/home/jim/2_OXOT_Projects_Dev/5_NER11_Gold_Model/validation/`

### Service Documentation
- Neo4j Official Docs: https://neo4j.com/docs/
- Qdrant Official Docs: https://qdrant.tech/documentation/
- spaCy NER: https://spacy.io/usage/linguistic-features#named-entities

---

## 📝 Document Maintenance

**Last Updated:** 2025-12-12
**Next Review:** 2026-03-12 (quarterly)
**Maintained By:** AEON Documentation Team

**Change Log:**
- 2025-12-12: Initial wiki index created
- 2025-12-12: Added 21 documents with full navigation

**To Request Documentation Updates:**
1. Identify missing information
2. Check if it exists in another document
3. Submit documentation request with specific gap description

---

## 🎯 Success Metrics

**Documentation Effectiveness Targets:**
- Time to find relevant doc: < 2 minutes
- Time to resolve common issue: < 15 minutes
- New user onboarding: < 1 week to productivity
- Search success rate: > 90%

---

**Status:** ✅ COMPLETE
**Coverage:** 21 documents indexed
**Navigation Paths:** 6 methods
**Quick References:** 4 cards
**Learning Paths:** 3 structured programs

---

*For a simpler overview, see [README.md](../README.md)*
*For the original index, see [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)*
