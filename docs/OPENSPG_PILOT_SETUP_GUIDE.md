# OpenSPG Pilot Setup Guide
**Created:** 2025-10-29
**Purpose:** Step-by-step guide to launch 2-week OpenSPG/KAG pilot evaluation
**Status:** PENDING - Saved for future implementation

---

## Executive Summary

This guide enables a **2-week proof-of-concept** to evaluate whether OpenSPG/KAG framework adds value over direct Neo4j approach. The pilot processes 10-20 security documents using KAG's LLM-powered extraction and compares results, costs, and developer experience.

**Estimated Time:** 2 weeks (1 week setup, 1 week evaluation)
**Estimated Cost:** $50-200 in OpenAI API calls
**Risk:** Low (parallel to existing Neo4j, no migration required)

---

## Prerequisites Check

### Current State Validation
```bash
# 1. Verify OpenSPG containers running
docker ps --filter "name=openspg"
# Expected: openspg-server, openspg-neo4j, openspg-mysql, openspg-minio

# 2. Check server health
curl http://127.0.0.1:8887/health
# Current status: "unhealthy" - needs fixing

# 3. Verify Neo4j has dual-label nodes (already confirmed)
# 182,992 nodes with format: [Label, "CybersecurityKB.Label"]
```

### Files and Configuration
- ✅ `/home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/kag_config.yaml` - exists
- ✅ `/home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/schema/*.schema` - exists (empty)
- ⚠️ OpenAI API keys in config - need validation
- ⚠️ OpenSPG schema - needs population

---

## Phase 1: Fix OpenSPG Server Health (Day 1)

### Step 1.1: Diagnose Server Issues
```bash
# Check detailed logs
docker logs openspg-server --tail 100

# Common issues:
# - Authentication not configured
# - MySQL connection problems
# - Neo4j connection issues
# - Schema initialization failures
```

### Step 1.2: Fix Authentication
```bash
# Access OpenSPG UI
# URL: http://127.0.0.1:8887
# Default credentials (may need setup):
# Username: openspg
# Password: openspg@kag

# If login fails, reset via MySQL:
docker exec -it openspg-mysql mysql -u root -p
# Password: root (check docker-compose.yml)

# Check/create default user
USE spg_server;
SELECT * FROM user WHERE username = 'openspg';
```

### Step 1.3: Verify Component Connectivity
```bash
# Test Neo4j connection from OpenSPG server
docker exec openspg-server curl http://openspg-neo4j:7474

# Test MySQL connection
docker exec openspg-server curl http://openspg-mysql:3306

# Test MinIO connection
docker exec openspg-server curl http://openspg-minio:9000
```

### Step 1.4: Restart with Clean State (if needed)
```bash
# Nuclear option if above fails
docker-compose -f /path/to/docker-compose.yml down
docker volume prune  # CAREFUL: This deletes data
docker-compose -f /path/to/docker-compose.yml up -d

# Wait for healthy status
watch docker ps --filter "name=openspg"
```

---

## Phase 2: Define Minimal SPG Schema (Day 2-3)

### Step 2.1: Choose ONE Entity Type for Pilot

**Recommended:** `ThreatReport` (easiest to validate)

**Rationale:**
- Clear structure (title, date, findings, CVEs)
- Easy to extract from PDFs
- Measurable quality (did it find the CVEs mentioned?)
- Existing samples available

### Step 2.2: Create SPG Schema Definition

Edit: `/home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/schema/CybersecurityKB.schema`

```python
namespace CybersecurityKB

# ============================================================================
# PILOT SCHEMA - Minimal for 2-week evaluation
# ============================================================================

# Entity Types
entity ThreatReport {
    properties:
        id: string
        title: string
        published_date: datetime
        report_type: string  # ["pentest", "incident", "vulnerability_assessment"]
        severity: string  # ["low", "medium", "high", "critical"]
        summary: text
        findings: text
        recommendations: text
        source_document: string  # File path/URL
    
    relations:
        mentions_cve: CVE[]  # Link to existing CVE nodes
        identifies_weakness: CWE[]  # Link to existing CWE nodes
        recommends_mitigation: CourseOfAction[]  # Link to existing mitigations
}

# Reference existing entities (already in Neo4j via direct import)
entity CVE {
    properties:
        id: string
        cve_id: string
        description: text
        cvss_score: float
}

entity CWE {
    properties:
        id: string
        cwe_id: string
        name: string
}

entity CourseOfAction {
    properties:
        id: string
        name: string
        description: text
}
```

### Step 2.3: Register Schema with OpenSPG

**Option A: Via UI** (Recommended for pilot)
```
1. Login to http://127.0.0.1:8887
2. Navigate to Schema Management
3. Upload CybersecurityKB.schema
4. Click "Publish Schema"
```

**Option B: Via API** (For automation)
```bash
curl -X POST http://127.0.0.1:8887/project/api/v1/schema/publish \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d @schema.json
```

**Option C: Via KNEXT CLI**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG
source venv/bin/activate

knext schema publish \
  --host http://127.0.0.1:8887 \
  --project-id 1 \
  --schema-file kag/examples/CybersecurityKB/schema/CybersecurityKB.schema
```

---

## Phase 3: Configure KAG Builder (Day 4)

### Step 3.1: Validate OpenAI API Keys

Edit: `kag_config.yaml`

```yaml
# Test your API key
openie_llm:
  api_key: sk-proj-VitYxNmBXl...  # VERIFY THIS WORKS
  model: gpt-4o-mini

# Test with simple call
python3 << 'PYEOF'
import openai
openai.api_key = "sk-proj-VitYxNmBXl..."  # Your key
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say 'API key works'"}]
)
print(response.choices[0].message.content)
PYEOF
```

### Step 3.2: Create Custom Builder for ThreatReport

Create: `/home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/builder/threat_report_builder.py`

```python
from kag.builder.component import KGWriter, SPGTypeMapping
from kag.builder.model.sub_graph import SubGraph
from kag.interface import BuilderChainABC

class ThreatReportBuilderChain(BuilderChainABC):
    """
    Pilot builder for security threat reports
    Extracts: Title, Date, Findings, CVE references
    """
    
    def __init__(self):
        super().__init__()
        self.spg_type_name = "CybersecurityKB.ThreatReport"
    
    def build(self, **kwargs):
        # Step 1: PDF/Text extraction (LlamaParse or similar)
        self.reader = PDFReader()
        
        # Step 2: LLM-powered entity extraction
        self.extractor = SchemaFreeExtractor.from_config({
            "llm": self.kag_config.openie_llm,
            "entity_types": ["ThreatReport", "CVE", "CWE"],
            "relationship_types": ["mentions_cve", "identifies_weakness"]
        })
        
        # Step 3: Map to SPG schema
        self.mapping = SPGTypeMapping(spg_type_name=self.spg_type_name)
        
        # Step 4: Write to Neo4j via OpenSPG
        self.writer = KGWriter()
        
        # Build pipeline
        chain = self.reader >> self.extractor >> self.mapping >> self.writer
        return chain
```

### Step 3.3: Test with ONE Document

```python
# Test script: test_pilot.py
from threat_report_builder import ThreatReportBuilderChain

# Pick ONE simple PDF
test_pdf = "/path/to/simple_threat_report.pdf"

# Run builder
builder = ThreatReportBuilderChain()
chain = builder.build()

result = chain.invoke({"file_path": test_pdf})

print(f"Extracted entities: {result}")
```

---

## Phase 4: Pilot Evaluation (Week 2)

### Step 4.1: Process 10-20 Documents

**Document Selection Criteria:**
- Mix of complexity (simple, medium, complex reports)
- Different types (pentest, incident, vuln assessment)
- Known ground truth (you know what CVEs SHOULD be extracted)

**Batch Processing:**
```python
# Process all pilot documents
import os
from threat_report_builder import ThreatReportBuilderChain

docs_dir = "/path/to/pilot_documents"
builder = ThreatReportBuilderChain()
chain = builder.build()

results = []
for pdf in os.listdir(docs_dir):
    if pdf.endswith('.pdf'):
        print(f"Processing {pdf}...")
        result = chain.invoke({"file_path": os.path.join(docs_dir, pdf)})
        results.append({
            "file": pdf,
            "extracted": result,
            "timestamp": datetime.now()
        })

# Save results for comparison
import json
with open("pilot_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

### Step 4.2: Quality Assessment

**Metrics to Collect:**
```yaml
Extraction Quality:
  - Precision: What % of extracted CVEs are correct?
  - Recall: What % of actual CVEs were found?
  - Entity linking accuracy: Did it link to correct existing CVE nodes?
  - Relationship accuracy: Are mentioned_cve links correct?

Cost Analysis:
  - Total tokens used: Track via OpenAI API logs
  - Cost per document: (total cost / # documents)
  - Cost per entity: (total cost / # entities extracted)

Time Analysis:
  - Processing time per document (minutes)
  - Setup time for new document type (hours)
  - Debugging time when extraction fails (hours)

Developer Experience:
  - Lines of code: KAG builder vs direct Neo4j script
  - Ease of debugging: Rate 1-10
  - Documentation quality: Rate 1-10
```

### Step 4.3: Comparison Test

**For 5 documents, do BOTH approaches:**

1. **KAG Approach:** Use builder pipeline (automated)
2. **Direct Neo4j:** Write custom extraction script (manual)

**Compare:**
- Time to implement
- Extraction quality
- Code maintainability
- Flexibility for changes

### Step 4.4: Test Multi-Hop Reasoning

**Query 1: Attack Path Analysis**
```python
# Via KAG Solver
from kag.solver import KAGSolver

solver = KAGSolver.from_config(kag_config.solver_config)
answer = solver.solve_question(
    "What CVEs are mentioned in threat reports that exploit CWE-79 and have critical severity?"
)

print(answer)  # Should show reasoning steps

# Compare to Cypher (manual multi-hop)
query = """
MATCH (report:ThreatReport)-[:mentions_cve]->(cve:CVE)-[:EXPLOITS]->(cwe:CWE {cwe_id: '79'})
WHERE report.severity = 'critical'
RETURN report.title, cve.cve_id, cve.cvss_score
"""
```

**Query 2: Natural Language**
```python
# Can KAG answer questions Direct Neo4j can't?
questions = [
    "What are the most common vulnerabilities in ICS systems according to recent reports?",
    "Which threat actors are associated with CVE-2024-1234?",
    "What mitigations are recommended for ransomware attacks?"
]

for q in questions:
    kag_answer = solver.solve_question(q)
    # Try to replicate in Cypher - is it easier or harder?
```

---

## Phase 5: Decision Criteria (End of Week 2)

### ✅ Continue/Expand OpenSPG If:

1. **Extraction quality >85%** (precision + recall)
2. **Cost <$10 per document** (acceptable for automation)
3. **Time savings >50%** (vs manual scripting)
4. **Reasoning solves real problems** (queries you couldn't easily do)
5. **Team finds it learnable** (<2 days to be productive)

### 🤔 Keep Hybrid If:

1. **Extraction quality 70-85%** (good but not great)
2. **Cost $10-30 per document** (acceptable for complex docs only)
3. **Time savings 20-50%** (marginal benefit)
4. **Reasoning adds some value** (nice to have, not essential)

### ❌ Abandon OpenSPG If:

1. **Extraction quality <70%** (manual is better)
2. **Cost >$30 per document** (too expensive)
3. **Time savings <20% or negative** (slower than manual)
4. **Reasoning doesn't solve real problems** (fancy demo, no utility)
5. **Too complex to maintain** (team can't debug issues)

---

## Phase 6: Next Steps Based on Decision

### If Continuing OpenSPG:

**Month 2-3: Expand Scope**
```yaml
Add Entity Types:
  - NetworkDiagram (extract topology from Visio/images)
  - ComplianceAssessment (IEC 62443 gap analysis)
  - IncidentReport (SOC incident data)

Enhance Schema:
  - Add full UCO ontology mappings
  - Define custom relationship types
  - Add validation rules

Integrate Solver:
  - Build custom reasoning templates
  - Train on domain-specific queries
  - Integrate with security dashboards
```

**Month 4+: Production Migration**
```yaml
Migrate Existing Data:
  - Script to convert 183K direct Neo4j nodes to SPG format
  - Validate dual-label compatibility
  - Test all existing queries work

Training & Ops:
  - Team training on OpenSPG/KAG
  - Monitoring and alerting setup
  - Backup and recovery procedures
```

### If Abandoning OpenSPG:

**Invest in Direct Neo4j Enhancements**
```yaml
Add AI Features:
  - Build custom LLM extraction pipeline (LangChain + Cypher)
  - Implement vector search for semantic queries
  - Create custom reasoning engine for multi-hop

Improve Automation:
  - Generic PDF extraction framework
  - Auto-entity linking with fuzzy matching
  - Scheduled data refresh jobs

Production Hardening:
  - Backup/recovery automation
  - Monitoring dashboards
  - API layer for external access
```

---

## Troubleshooting Guide

### Issue: OpenSPG server stays "unhealthy"

**Solutions:**
1. Check MySQL is initialized: `docker exec openspg-mysql mysql -u root -p -e "SHOW DATABASES;"`
2. Check Neo4j connectivity: `docker exec openspg-server nc -zv openspg-neo4j 7687`
3. Review startup logs: `docker logs openspg-server | grep -i error`
4. Restart in order: MySQL → Neo4j → MinIO → Server

### Issue: Schema publish fails

**Solutions:**
1. Validate schema syntax: Use KNEXT CLI validator
2. Check namespace matches config: `namespace CybersecurityKB`
3. Ensure project ID is correct: Default is `1`
4. Try smaller schema first: Single entity type

### Issue: LLM extraction too expensive

**Solutions:**
1. Switch to `gpt-4o-mini` (8x cheaper)
2. Enable "Lightweight Build" mode: 89% token reduction
3. Reduce chunk size: Smaller context = cheaper
4. Pre-filter documents: Only process if contains keywords

### Issue: Extraction quality poor

**Solutions:**
1. Improve prompts: Add domain-specific examples
2. Use schema-constrained mode: Force adherence to entity types
3. Add custom entity linking: Override automatic linking
4. Post-process results: Validate and correct via rules

### Issue: Can't link to existing Neo4j nodes

**Solutions:**
1. Verify label format matches: `CVE` vs `CybersecurityKB.CVE`
2. Check namespace property: `namespace: "CybersecurityKB"`
3. Use entity linking function: Override with custom search
4. Ensure nodes exist: Query Neo4j directly first

---

## Resources

### Documentation
- KAG Official Docs: https://openspg.yuque.com/ndx6g9/docs_en
- KAG GitHub: https://github.com/OpenSPG/KAG
- OpenSPG Website: https://openspg.github.io/v2/docs_en
- Neo4j + OpenSPG: Check OpenSPG docs on graph store configuration

### Example Projects
- `/home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/supplychain/` - Structured data example
- `/home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/domain_kg/` - Domain knowledge graph
- GitHub: Search "KAG OpenSPG example" for community projects

### Community Support
- Discord: https://discord.gg/PURG77zhQ7
- GitHub Issues: https://github.com/OpenSPG/KAG/issues
- DeepWiki: https://deepwiki.com/Like0x/KAG

---

## Cost Estimation

### Expected Costs (Conservative)

**Setup Phase (One-time):**
- Developer time: 40 hours @ $100/hr = $4,000
- OpenAI API testing: $50
- **Total:** $4,050

**Pilot Phase (2 weeks):**
- Process 20 documents
- Avg 50 pages per document = 1,000 pages
- Avg 500 tokens per page = 500K tokens
- GPT-4o-mini: $0.15 per 1M input tokens = $0.075
- Output tokens (300K): $0.60 per 1M = $0.18
- **Total API Cost:** ~$0.25 per document = $5 for pilot

**If Expanded to 1,000 documents:**
- API costs: $250
- Infrastructure: $100/month (Docker resources)
- Developer maintenance: 10 hours/month @ $100/hr = $1,000/month
- **Monthly Operating Cost:** ~$1,350

**ROI Break-Even:**
- If OpenSPG saves 2 hours per document vs manual
- 1,000 documents = 2,000 hours saved
- @ $100/hr = $200,000 value
- Cost: $1,350/month * 12 = $16,200/year
- **ROI:** 1,133% (if time savings materialize)

---

## Success Criteria Summary

| Metric | Target | Measurement |
|--------|--------|-------------|
| Extraction Precision | >85% | Manual validation of 20 docs |
| Extraction Recall | >80% | Check all CVEs found |
| Cost per Document | <$10 | OpenAI API logs |
| Processing Time | <5 min/doc | Automated timing |
| Developer Setup Time | <2 days | Track learning curve |
| Reasoning Quality | Solves 5/10 test queries | Expert assessment |
| Code Reduction | >50% vs manual | Line count comparison |

**Decision Gate:** If 5+ metrics hit target → Expand pilot
**Decision Gate:** If <3 metrics hit target → Abandon OpenSPG

---

**END OF GUIDE**

This guide provides everything needed to execute a data-driven OpenSPG pilot evaluation when ready.
