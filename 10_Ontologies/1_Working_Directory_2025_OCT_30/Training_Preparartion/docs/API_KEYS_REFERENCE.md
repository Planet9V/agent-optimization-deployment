# WORKING API KEYS & ENDPOINTS - REFERENCE DOCUMENT
**Date:** 2025-11-07
**Purpose:** Memorizable reference for vulnerability intelligence API integration
**Status:** ✅ ALL KEYS VERIFIED

---

## 1. NVD CVE API (WORKING ✅)

```bash
# API Key
NVD_API_KEY="534786f5-5359-40b8-8e54-b28eb742de7c"

# Endpoint
NVD_API_URL="https://services.nvd.nist.gov/rest/json/cves/2.0"

# Rate Limits
WITH_API_KEY="5 requests per 30 seconds"
WITHOUT_API_KEY="5 requests per 30 seconds (total for all requests from same IP)"

# Example Usage
curl "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-44228" \
  -H "apiKey: 534786f5-5359-40b8-8e54-b28eb742de7c"

# Response Fields
- cve.id: CVE identifier
- cve.descriptions[0].value: CVE description
- cve.metrics.cvssMetricV31[0].cvssData.baseScore: CVSS score
- cve.weaknesses[0].description[0].value: CWE-NNN
```

---

## 2. FIRST.org EPSS API (WORKING ✅ - PRIMARY FOR EPSS)

```bash
# API Endpoint (NO KEY REQUIRED)
EPSS_API_URL="https://api.first.org/data/v1/epss"

# Update Schedule
Updates: "Daily at 00:00 UTC"

# Batch Query Support
Max_CVEs_Per_Request: 1000

# Example Usage - Single CVE
curl "https://api.first.org/data/v1/epss?cve=CVE-2021-44228"

# Example Usage - Multiple CVEs
curl "https://api.first.org/data/v1/epss?cve=CVE-2021-44228,CVE-2024-21762,CVE-2022-22954"

# Example Response
{
  "status": "OK",
  "status-code": 200,
  "data": [
    {
      "cve": "CVE-2021-44228",
      "epss": "0.943580000",      # 94.36% exploitation probability
      "percentile": "0.999570000",  # 99.957th percentile (extremely high)
      "date": "2025-11-07"
    }
  ]
}

# Response Fields
- epss: Exploitation probability (0.0 - 1.0)
- percentile: Percentile rank (0.0 - 1.0)
- date: EPSS calculation date

# Prioritization Logic
IF epss >= 0.7:  priority = "NOW"     # ≥70% exploitation probability
IF epss >= 0.3:  priority = "NEXT"    # 30-70% exploitation probability
IF epss < 0.3:   priority = "NEVER"   # <30% exploitation probability
```

---

## 3. Vulncheck API (VALID KEY, SUBSCRIPTION EXPIRED ⚠️)

```bash
# API Key
VULNCHECK_API_KEY="vulncheck_651eb2056ad525e7d67b05b54169d2b87c0cb1f72dda16fd221d21d83f31b9cc"

# Endpoint
VULNCHECK_API_URL="https://api.vulncheck.com/v3/index/vulncheck-nvd2"

# Current Status
HTTP_Status: 402 (Payment Required)
Error: "This index requires the Exploit & Vulnerability Intelligence subscription or an active trial"

# Example Usage (When Subscription Active)
curl "https://api.vulncheck.com/v3/index/vulncheck-nvd2?cve=CVE-2024-21762" \
  -H "Authorization: Bearer vulncheck_651eb2056ad525e7d67b05b54169d2b87c0cb1f72dda16fd221d21d83f31b9cc"

# Unique Data Provided (When Active)
- relatedAttackPatterns: CAPEC IDs and names
- mitreAttackTechniques: ATT&CK technique mappings
- temporalCVSSV31: CVSS temporal scores
- categorization: ICS/OT, IoMT, IoT, Mobile tags
- vcConfigurations: Faster CPE data than NVD
- epss: EPSS scores (also available from FIRST.org for free)

# Value Proposition
PRIMARY_VALUE: "CAPEC and ATT&CK mappings for CVEs"
ALTERNATIVE: "Can infer CAPEC from CWE → CAPEC relationships in CAPEC XML v3.9"
```

---

## 4. Neo4j Database (CONFIGURED ✅)

```bash
# Connection Details
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="neo4j@openspg"

# Database Statistics
Total_CVEs: 179,859
Attack_Chain_Relationships: 1,168,814
CAPEC_Coverage: 68% (need 95%+ for production)

# Example Connection (Python)
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "neo4j@openspg")
)

with driver.session() as session:
    result = session.run("MATCH (c:CVE) RETURN count(c) AS total")
    print(result.single()["total"])  # 179,859
```

---

## DAILY UPDATE WORKFLOW

```bash
# 1. FETCH NEW CVEs (NVD API)
# Modified in last 24 hours
curl "https://services.nvd.nist.gov/rest/json/cves/2.0?lastModStartDate=2025-11-06T00:00:00.000" \
  -H "apiKey: 534786f5-5359-40b8-8e54-b28eb742de7c"

# Expected Volume: 50-150 CVEs/day

# 2. ENRICH WITH EPSS (FIRST.org API)
# Batch query for all new CVE IDs
curl "https://api.first.org/data/v1/epss?cve=CVE-2025-0001,CVE-2025-0002,CVE-2025-0003"

# 3. EXTRACT ENTITIES (v7 NER Model)
# Use trained spaCy model to extract:
# - VULNERABILITY entities (CVE IDs)
# - WEAKNESS entities (CWE IDs)
# - SOFTWARE_COMPONENT entities
# - VENDOR entities
# - ATTACK_PATTERN entities (CAPEC IDs)

# 4. INSERT INTO NEO4J
# Create CVE nodes with relationships:
# CVE -[:IS_WEAKNESS_TYPE]-> CWE
# CVE -[:ENABLES_ATTACK_PATTERN]-> CAPEC
# CVE -[:HAS_EPSS_SCORE]-> (epss_score, priority)

# 5. CALCULATE ATTACK CHAINS
# Infer missing CAPEC relationships from CWE
# Validate 8-hop paths: CVE → CWE → CAPEC → ATT&CK → ThreatActor
```

---

## API KEY SECURITY

**Storage Locations:**
1. `/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/.env`
2. This reference document (encrypted storage recommended)

**Security Recommendations:**
- ✅ Use environment variables, NOT hardcoded in scripts
- ✅ Add .env to .gitignore
- ✅ Rotate keys periodically
- ⚠️ NVD API key has IP-based rate limiting
- ⚠️ FIRST.org API has NO authentication (public)

---

## TESTING & VALIDATION

### Test 1: NVD API Connectivity
```bash
curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2021-44228" \
  -H "apiKey: 534786f5-5359-40b8-8e54-b28eb742de7c" | jq '.vulnerabilities[0].cve.id'
# Expected: "CVE-2021-44228"
```

### Test 2: FIRST.org EPSS API
```bash
curl -s "https://api.first.org/data/v1/epss?cve=CVE-2021-44228" | jq '.data[0].epss'
# Expected: "0.943580000" (94.36% exploitation probability)
```

### Test 3: Neo4j Connectivity
```cypher
// Run in Neo4j Browser
MATCH (c:CVE {cveId: 'CVE-2021-44228'})
RETURN c.cveId, c.cvssV3BaseScore, c.epss_score
// Expected: CVE-2021-44228, 10.0, 0.943580
```

---

## QUICK REFERENCE CHEAT SHEET

| API | Status | Key Required | Rate Limit | Data Provided |
|-----|--------|--------------|------------|---------------|
| **NVD** | ✅ WORKING | YES | 5 req/30s | CVE, CVSS, CWE, CPE |
| **FIRST.org EPSS** | ✅ WORKING | NO | Unlimited | EPSS scores, percentiles |
| **Vulncheck** | ⚠️ EXPIRED | YES | N/A | CAPEC, ATT&CK, temporal CVSS |
| **Neo4j** | ✅ CONFIGURED | YES | N/A | Graph database |

**PRIMARY DAILY WORKFLOW:**
1. NVD API → Fetch new CVEs
2. v7 NER Model → Extract entities
3. FIRST.org EPSS → Enrich with exploitability
4. Neo4j → Insert with attack chain relationships

---

**Document:** API_KEYS_REFERENCE.md
**Version:** 1.0.0
**Date:** 2025-11-07
**Memorize:** All API keys and endpoints for daily operations
