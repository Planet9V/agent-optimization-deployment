# CVE Bulk Import Guide - 2020 to Present

**Purpose**: Import all CVEs from 2020-01-01 to current date into CybersecurityKB
**Source**: NVD (National Vulnerability Database) API 2.0
**Date**: 2025-10-27

---

## 📋 Overview

This guide covers the bulk import of **all CVEs from 2020 to present** into the CybersecurityKB knowledge graph.

### Expected Volume
- **Time Period**: 2020-01-01 to 2025-10-27 (~5.8 years)
- **Estimated CVEs**: 100,000 - 150,000 CVEs
- **Estimated Time**: 2-4 hours (depending on volume)
- **Storage**: ~500MB Neo4j data

---

## 🚀 Quick Start

```bash
# Navigate to builder directory
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/builder

# Run bulk import (starts from 2020)
python3 import_cve_bulk.py

# Or specify custom start year
python3 import_cve_bulk.py --start-year 2021

# Resume interrupted import
python3 import_cve_bulk.py --resume

# Start fresh (delete progress and reimport)
python3 import_cve_bulk.py --clean
```

---

## 🔧 How It Works

### 1. Year-by-Year Processing
The script fetches CVEs year by year, then month by month to avoid overwhelming the API:
```
2020 → Jan, Feb, Mar ... Dec
2021 → Jan, Feb, Mar ... Dec
...
2025 → Jan, Feb, Mar ... Oct
```

### 2. Rate Limiting
- **With API Key**: 50 requests per 30 seconds
- **Automatic**: Script handles rate limiting automatically
- **Delay**: 0.6 seconds between requests
- **Backoff**: If rate limit hit, waits 60 seconds and retries

### 3. Progress Checkpointing
- Progress saved every 500 CVEs
- Can resume if interrupted
- Progress file: `cve_import_progress.json`

### 4. Dual Label System
Each CVE gets **both** labels:
- `CVE` (original label)
- `CybersecurityKB.CVE` (namespace-prefixed for OpenSPG)

### 5. CWE Linking
Automatically creates relationships to existing CWE entities:
```
(CVE)-[:EXPLOITS]->(CWE)
```

---

## 📊 Import Process

### Phase 1: Fetch from NVD API
```
Year: 2020
  Month 01: Fetching 2020-01-01 to 2020-01-31
    Total available: 1,245
    Retrieved: 1,245/1,245 CVEs
    Fetched: 1,245 CVEs

  Month 02: Fetching 2020-02-01 to 2020-02-29
    ...
```

### Phase 2: Import to Neo4j
```
  Month 01: 1,245 CVEs imported
    Importing: 1,245/1,245
    Imported: 1,245 CVEs

  CVE-CWE Links: 892 relationships created
```

### Phase 3: Verification
```
BULK CVE IMPORT COMPLETE
============================================
Total CVEs Fetched:    125,432
Total CVEs Imported:   125,432
CVE-CWE Links Created: 89,234
API Calls Made:        756
Errors Encountered:    0
Total CVEs in Neo4j:   125,532 (includes 100 from previous import)
```

---

## 📈 Performance Characteristics

### API Rate Limiting
- **50 requests per 30 seconds** (with API key)
- **~100 requests per minute**
- **~6,000 requests per hour**
- **~144,000 requests per day**

### Import Speed
- **~2,000 CVEs per hour** (typical)
- **~50 CVEs per minute**
- Depends on:
  - Network latency
  - Neo4j write performance
  - CVE data complexity

### Resource Usage
- **CPU**: Low (~5-10%)
- **Memory**: ~200-500 MB
- **Network**: ~10 MB/hour download
- **Disk**: ~3-5 KB per CVE

---

## 🔍 Data Structure

### CVE Node Properties
```cypher
(:CVE {
  id: "cve-CVE-2024-12345",
  namespace: "CybersecurityKB",
  cve_id: "CVE-2024-12345",
  description: "Vulnerability description...",
  published_date: datetime("2024-01-15T00:00:00Z"),
  last_modified: datetime("2024-01-20T12:30:00Z"),
  cvss_score: 9.8,
  severity: "CRITICAL",
  cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
  cwe_ids: ["CWE-79", "CWE-89"],
  affected_products: ["cpe:2.3:a:vendor:product:version:*:*:*:*:*:*:*"]
})
```

### Labels
Each CVE has **two** labels:
- `CVE` - Original label
- `CybersecurityKB.CVE` - Namespace-prefixed label

### Relationships
```cypher
(CVE)-[:EXPLOITS]->(CWE)
```

---

## 🛠️ Command-Line Options

### Basic Usage
```bash
# Import from 2020 to present
python3 import_cve_bulk.py
```

### Custom Start Year
```bash
# Import from 2022 to present
python3 import_cve_bulk.py --start-year 2022
```

### Resume Interrupted Import
```bash
# Continue from last checkpoint
python3 import_cve_bulk.py --resume
```

### Start Fresh
```bash
# Delete progress and reimport
python3 import_cve_bulk.py --clean
```

---

## 📝 Progress Tracking

### Progress File Location
```
/home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/builder/cve_import_progress.json
```

### Progress File Contents
```json
{
  "last_completed_year": 2023,
  "last_completed_month": 8,
  "imported_cve_ids": ["CVE-2020-0001", "CVE-2020-0002", ...]
}
```

### Checking Progress
```bash
# View progress file
cat /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/builder/cve_import_progress.json | python3 -m json.tool

# Count imported CVEs
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (n:CVE {namespace: 'CybersecurityKB'}) RETURN count(n) as total;"
```

---

## 🚨 Error Handling

### API Rate Limit Hit (429/403)
```
Error fetching CVEs: 429 Too Many Requests
Rate limit hit, waiting 60 seconds...
```
**Action**: Script automatically waits and retries

### Network Timeout
```
Error fetching CVEs: Request timeout
```
**Action**: Script continues with next month, error logged

### Neo4j Connection Lost
```
Error importing CVE-2024-12345: Connection lost
```
**Action**: Check Neo4j container, run with `--resume`

### Interrupted Import (Ctrl+C)
```
Import interrupted by user.
Progress has been saved. Run with --resume to continue.
```
**Action**: Run `python3 import_cve_bulk.py --resume`

---

## ✅ Verification Commands

### Check Total CVEs Imported
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (n:CVE {namespace: 'CybersecurityKB'})
   RETURN count(n) as total_cves;"
```

### Check CVEs by Year
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (n:CVE {namespace: 'CybersecurityKB'})
   RETURN n.published_date.year as year, count(*) as count
   ORDER BY year DESC;"
```

### Check CVEs by Severity
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (n:CVE {namespace: 'CybersecurityKB'})
   RETURN n.severity as severity, count(*) as count
   ORDER BY count DESC;"
```

### Check Dual Labels
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (n:CVE {namespace: 'CybersecurityKB'})
   RETURN labels(n) as all_labels
   LIMIT 5;"
```

Expected:
```
all_labels
["CVE", "CybersecurityKB.CVE"]
```

### Check CVE-CWE Links
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (cve:CVE {namespace: 'CybersecurityKB'})-[:EXPLOITS]->(cwe:CWE)
   RETURN count(*) as total_links;"
```

### Sample Recent Critical CVEs
```bash
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j \
  "MATCH (n:CVE {namespace: 'CybersecurityKB'})
   WHERE n.severity = 'CRITICAL'
   RETURN n.cve_id, n.cvss_score, n.published_date
   ORDER BY n.published_date DESC
   LIMIT 10;"
```

---

## 🎯 Post-Import Actions

### 1. Verify in OpenSPG Knowledge Model
Go to: http://localhost:8887/#/knowledge/detail/model?projectId=1

**Expected**:
- `CybersecurityKB.CVE` entity type shows 125,000+ instances
- Can browse CVE entities
- Relationships to CWE visible

### 2. Test Chat Queries
Go to: http://localhost:8887/#/knowledge/list → CybersecurityKB

**Sample Queries**:
```
"What are the most critical CVEs from 2024?"
"Show me CVEs that exploit SQL injection"
"Which CVEs affect Apache products?"
"What are the most common CWE weaknesses in CVEs?"
```

### 3. Analytics Queries

**CVEs per Year**:
```cypher
MATCH (n:CVE {namespace: 'CybersecurityKB'})
RETURN n.published_date.year as year, count(*) as cve_count
ORDER BY year DESC;
```

**Most Exploited CWEs**:
```cypher
MATCH (cve:CVE {namespace: 'CybersecurityKB'})-[:EXPLOITS]->(cwe:CWE)
RETURN cwe.cwe_id, cwe.name, count(cve) as cve_count
ORDER BY cve_count DESC
LIMIT 20;
```

**Critical CVEs by Product**:
```cypher
MATCH (cve:CVE {namespace: 'CybersecurityKB'})
WHERE cve.severity = 'CRITICAL'
UNWIND cve.affected_products as product
RETURN product, count(cve) as cve_count
ORDER BY cve_count DESC
LIMIT 20;
```

---

## 🔄 Incremental Updates

### Daily Update Script
To keep CVEs current, run periodically:

```bash
# Fetch CVEs from last 7 days
python3 import_cve.py --days 7 --max-results 5000
```

### Monthly Update
```bash
# Fetch last 30 days
python3 import_cve.py --days 30 --max-results 10000
```

### Automated Updates (Cron)
```bash
# Add to crontab
0 2 * * * cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/CybersecurityKB/builder && python3 import_cve.py --days 1 --max-results 500
```

---

## 📊 Expected Results

### Volume Estimates (2020-2025)

| Year | Est. CVEs | Cumulative |
|------|-----------|------------|
| 2020 | ~18,000 | 18,000 |
| 2021 | ~20,000 | 38,000 |
| 2022 | ~25,000 | 63,000 |
| 2023 | ~28,000 | 91,000 |
| 2024 | ~30,000 | 121,000 |
| 2025 | ~15,000 (YTD) | ~136,000 |

### Severity Distribution (Typical)
- **CRITICAL**: ~8-10%
- **HIGH**: ~25-30%
- **MEDIUM**: ~45-50%
- **LOW**: ~10-15%

### CWE Coverage
- **CVEs with CWE**: ~70-80%
- **CVEs without CWE**: ~20-30%
- **Avg CWEs per CVE**: 1-2

---

## 🛡️ Best Practices

### 1. Run During Off-Peak Hours
- Import creates significant Neo4j write load
- Best run when knowledge graph is not actively queried

### 2. Monitor Progress
```bash
# In separate terminal, watch progress
watch -n 10 'docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" -d neo4j "MATCH (n:CVE {namespace: \"CybersecurityKB\"}) RETURN count(n);" 2>/dev/null'
```

### 3. Backup Before Import
```bash
# Backup Neo4j data
docker exec openspg-neo4j neo4j-admin dump --database=neo4j --to=/var/lib/neo4j/backups/pre-cve-import.dump
```

### 4. Verify API Key
```bash
# Test API key
curl -H "apiKey: 919ecb88-4e30-4f58-baeb-67c868314307" \
  "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=1"
```

---

## 🐛 Troubleshooting

### Issue: "No module named 'neo4j'"
```bash
pip3 install neo4j requests
```

### Issue: "Connection refused to Neo4j"
```bash
# Check Neo4j container
docker ps | grep neo4j

# Restart if needed
docker restart openspg-neo4j
```

### Issue: "API key invalid"
```bash
# Verify API key in script
grep "NVD_API_KEY" import_cve_bulk.py

# Test API key
curl -H "apiKey: YOUR_KEY" "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=1"
```

### Issue: Import very slow
- **Check**: Network latency to NVD API
- **Check**: Neo4j write performance
- **Solution**: Run during off-peak, check disk I/O

---

## 📚 Related Documentation

- **Neo4j Label Fix**: `/home/jim/2_OXOT_Projects_Dev/docs/OpenSPG_Neo4j_Label_Fix.md`
- **Schema Registration**: `/home/jim/2_OXOT_Projects_Dev/docs/OpenSPG_Schema_Registration_Fix.md`
- **Knowledge Base Summary**: `/home/jim/2_OXOT_Projects_Dev/docs/CybersecurityKB_Complete_Summary.md`

---

## ✅ Success Checklist

- [ ] Script runs without errors
- [ ] Progress checkpoint file created
- [ ] CVEs imported for all years (2020-2025)
- [ ] Dual labels verified (CVE + CybersecurityKB.CVE)
- [ ] CVE-CWE relationships created
- [ ] Total CVE count matches expected volume
- [ ] OpenSPG knowledge model shows CVEs
- [ ] Chat queries return CVE results

---

**Status**: Ready to import all CVEs from 2020 to present!

**Command**: `python3 import_cve_bulk.py`
