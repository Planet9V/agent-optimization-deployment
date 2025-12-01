# VulnCheck API & Free Vulnerability Intelligence Tools Research

**File**: VULNCHECK_RESEARCH_FINDINGS.md
**Created**: 2025-11-01
**Research Scope**: Free vulnerability intelligence platforms for cybersecurity threat intelligence enhancement
**Status**: COMPLETE

---

## Executive Summary

This research investigated 6+ free vulnerability intelligence platforms and tools to enhance cybersecurity threat intelligence capabilities, with specific focus on CVE enrichment, exploitability scoring, SBOM integration, and CISO prioritization frameworks.

**Key Findings**:
- ✅ **VulnCheck** offers comprehensive free API access to NVD++, KEV catalog, and XDB exploit database
- ✅ **EPSS API** provides free exploitability prediction scoring (no authentication required)
- ✅ **AttackerKB** offers free API access for community-driven exploitability assessments
- ✅ **OpenCTI** provides open-source threat intelligence platform with extensive connector ecosystem
- ✅ **CVEmon** (formerly Intruder CVE Trends) tracks trending CVEs via social media
- ✅ **SOCRadar CVE Radar** offers free real-time vulnerability monitoring

**Critical Insight**: Combining these free tools can enrich existing 267,487 CVEs with exploitability data, trending information, and community assessments without licensing costs.

---

## 1. VulnCheck API

### Overview
VulnCheck is an enterprise vulnerability intelligence platform offering comprehensive free tier access to CVE data, exploit intelligence, and enrichment services.

### Free Tier Capabilities

#### ✅ **API Access**: YES - Free Community Tier
- **Base URL**: `https://api.vulncheck.com/`
- **Authentication**: API token required (free signup)
- **Rate Limits**: Not publicly documented (requires account signup to view)
- **Documentation**: https://docs.vulncheck.com/

#### 📊 **Available Free Indexes**
1. **NVD++ (nist-nvd2)** - Enhanced NVD data with:
   - CVSS v3.1, v3.0, v2.0 scoring
   - CPE enrichment for "Awaiting Analysis" CVEs
   - CVSS v4 scores from multiple sources
   - SSVC (Stakeholder-Specific Vulnerability Categorization) metrics
   - Vulnerability categorizations (ICS/OT, IoMT, IoT, Mobile, Server Software)

2. **VulnCheck KEV** - Enhanced Known Exploited Vulnerabilities catalog:
   - ~80% MORE CVEs than CISA's official KEV catalog
   - Supplementary external links to exploit content
   - References to publicly-available exploits
   - FREE access at: https://www.vulncheck.com/kev

3. **VulnCheck XDB** - Exploit Database:
   - Real-time monitoring of Git repositories (GitHub, Gitee, etc.)
   - Proof-of-concept (PoC) exploit code indexing
   - CVE-to-exploit mapping
   - Human analysis validation
   - Coverage of international repositories
   - FREE search at: https://vulncheck.com/xdb/

#### 🔬 **CVE Enrichment Features**
- **CPE Generation**: VulnCheck generates CPEs from reliable sources for CVEs missing this data (~50% of awaiting analysis CVEs)
- **SSVC Metrics**: Both CISA Vulnrichment SSVC and VulnCheck-generated SSVC metrics
- **CVSS V4 Scores**: Multi-source CVSS V4 collection
- **Categorization**: Automatic classification into ICS/OT, IoMT, IoT, Mobile, Server Software
- **Temporal Scores**: CVSS temporal scoring for time-based risk assessment

#### 📦 **SBOM Support**
- **VulnCheck for SBOM Response**: ServiceNow integration available
- **Real-time SBOM Enrichment**: Maps software components to known vulnerabilities
- **Exploitability Intelligence**: Correlates vulnerabilities with active exploits
- **Supply Chain Risk**: Real-time visibility into software supply chain risks

#### ⚠️ **Limitations**
- Rate limits not publicly documented (requires free account)
- SBOM direct integration requires ServiceNow (paid integration)
- No native Neo4j connector (would require custom development)

### Data Format
- **Format**: JSON via REST API
- **Standards**: Supports CVE, CPE, CVSS standards
- **Response Example**:
```json
{
  "cve": "CVE-2024-XXXXX",
  "cvss_v3": 9.8,
  "epss_score": 0.85,
  "kev_entry": true,
  "exploit_available": true,
  "xdb_references": ["https://github.com/..."]
}
```

### Integration Potential
- **High** for CVE enrichment (267,487 CVEs)
- **Medium** for SBOM node connection (requires custom integration)
- **High** for exploitability scoring
- **Medium** for Neo4j integration (custom ETL required)

### CISO Prioritization Support
- ✅ Exploitability data (XDB database)
- ✅ KEV catalog (actively exploited in wild)
- ✅ SSVC metrics (decision-making framework)
- ✅ Temporal scoring (time-based prioritization)
- **Framework Alignment**: Supports "Now/Next/Never" through KEV (Now) + EPSS (Next) + CVSS base (Never)

---

## 2. EPSS (Exploit Prediction Scoring System)

### Overview
EPSS is a free, open-source framework developed by FIRST.org that predicts the probability of CVE exploitation in the next 30 days using machine learning.

### Free API Access

#### ✅ **API Access**: YES - Completely Free
- **Base URL**: `https://api.first.org/data/v1/epss`
- **Authentication**: **NONE REQUIRED**
- **Rate Limits**: None publicly stated
- **Documentation**: https://www.first.org/epss/api

#### 📊 **API Capabilities**
1. **Single CVE Query**:
   ```
   https://api.first.org/data/v1/epss?cve=CVE-2024-12345
   ```
   Returns: EPSS score (0-1 probability) + percentile ranking

2. **Batch Queries**:
   ```
   https://api.first.org/data/v1/epss?cve=CVE-2022-27225,CVE-2022-27223,CVE-2022-27218
   ```

3. **Time Series (30 days)**:
   ```
   https://api.first.org/data/v1/epss?cve=CVE-2024-12345&scope=time-series
   ```

4. **Top 100 Highest Scores**:
   ```
   https://api.first.org/data/v1/epss?order=!epss
   ```

#### 🎯 **EPSS Score Interpretation**
- **Score**: Probability of exploitation in next 30 days (0.0 - 1.0)
- **Percentile**: Relative ranking against all CVEs
- **Threshold Guidance**: EPSS > 0.2 often used for prioritization

### Data Format
```json
{
  "cve": "CVE-2024-12345",
  "epss": "0.85234",
  "percentile": "0.99123",
  "date": "2025-11-01"
}
```

### Integration Potential
- **VERY HIGH** for all 267,487 CVEs (bulk API available)
- **VERY HIGH** for SBOM enrichment (automate scoring for SBOM components)
- **VERY HIGH** for Neo4j (simple REST API → Cypher ingestion)

### CISO Prioritization Support
- ✅ **PRIMARY TOOL** for "Next" category (predicted exploitation)
- ✅ Complements CVSS (severity) with exploitability (likelihood)
- ✅ Research shows: Of 352 "Critical" CVSS CVEs, only small fraction have high EPSS
- ✅ Enables risk-based prioritization: Impact (CVSS) × Likelihood (EPSS)

### Real-World Usage
- Microsoft Defender integrates EPSS for vulnerability prioritization
- OX Security, Orca Security use EPSS for DevSecOps prioritization
- OWASP Dependency-Track ingests EPSS for SBOM analysis

---

## 3. AttackerKB

### Overview
AttackerKB is a free, community-driven platform by Rapid7 providing exploitability assessments from security researchers and practitioners.

### Free API Access

#### ✅ **API Access**: YES - Free with Registration
- **Base URL**: `https://api.attackerkb.com/v1/`
- **Authentication**: API key (free - generated from profile settings)
- **Rate Limits**: Not specified (assumed reasonable for community use)
- **Documentation**: https://api.attackerkb.com/v1/api-docs/docs
- **Status**: Read-only API (write access planned)

#### 📊 **API Endpoints**
1. **Topics (CVEs/Vulnerabilities)**
   - GET `/topics` - List all vulnerabilities
   - GET `/topics/{id}` - Specific vulnerability details

2. **Assessments (Expert Analysis)**
   - GET `/assessments` - List all assessments
   - GET `/assessments/{id}` - Specific assessment
   - Includes: exploitability scores, difficulty ratings, enterprise impact

3. **Contributors (Community Members)**
   - GET `/contributors` - List contributors
   - GET `/contributors/{id}` - Specific contributor profile

#### 🎯 **Exploitability Metrics**
AttackerKB assessments include:
- **Exploitability Score**: How easily exploitable in real environments
- **Assessment Metadata**:
  - `obscure_configuration`: Requires unusual setup
  - `difficult_to_develop`: Exploit development complexity
  - `common_enterprise`: Prevalence in enterprise environments
  - `high_privilege_access`: Privilege requirements
  - `pre_auth`: Pre-authentication exploitation possible

### Data Format
```json
{
  "id": "assessment_id",
  "topicId": "cve_id",
  "score": 8.5,
  "document": "Full text analysis...",
  "metadata": {
    "obscure_configuration": false,
    "difficult_to_develop": true,
    "common_enterprise": true,
    "high_privilege_access": false,
    "pre_auth": true
  },
  "created": "2025-01-15T10:30:00Z"
}
```

### Python Integration
```python
from attackerkb import AttackerKB

akb = AttackerKB(api_key="your_api_key")
topic = akb.get_single_topic("topic_id")
assessments = akb.get_assessments()
```

### Integration Potential
- **Medium-High** for CVE enrichment (not all CVEs have assessments)
- **Low** for SBOM (no direct component matching)
- **High** for exploitability intelligence (community expertise)
- **Medium** for Neo4j (manual ETL required)

### CISO Prioritization Support
- ✅ Real-world exploitability assessments (practitioner knowledge)
- ✅ Enterprise environment context
- ✅ Exploit development difficulty insights
- ⚠️ Coverage gaps (not all CVEs assessed by community)

---

## 4. CVEmon (Formerly Intruder CVE Trends)

### Overview
CVEmon (formerly Intruder CVE Trends) tracks CVE mentions across social media platforms to identify trending vulnerabilities receiving attention from security community and threat actors.

### Free Access

#### ✅ **Web Interface**: YES - Free
- **URL**: https://cvemon.intruder.io/
- **API**: Not publicly documented (web interface only)
- **Data Export**: RSS feed available

#### 📊 **Key Features**
1. **Top 10 Trending CVEs (24 hours)**
   - Real-time social media monitoring
   - Twitter/X, security blogs, forums

2. **Hype Score System**
   - Score out of 100
   - Benchmarked against year's highest levels
   - Visual "hypemeter" indicator

3. **Expert Analysis**
   - Intruder security team commentary
   - Risk assessment for enterprise environments
   - Context beyond CVSS scores

4. **Data Aggregation**
   - NVD data integration
   - CISA KEV catalog
   - Exploit availability indicators

#### 📡 **RSS Feed**
- **URL**: https://cvemon.intruder.io/feeds
- **Update Frequency**: Hourly
- **Format**: RSS/XML

### Data Access
- **Web Interface**: Browse current top 10
- **RSS**: Programmatic access to trending CVEs
- **Export**: Manual data collection (no API)

### Integration Potential
- **Low** for bulk CVE enrichment (only top trending)
- **Medium** for threat intelligence feeds (RSS integration)
- **Low** for SBOM (no component matching)
- **Medium** for alerting (RSS → monitoring system)

### CISO Prioritization Support
- ✅ Early warning system (social media chatter = potential attack interest)
- ✅ "Now" category indicator (trending = possibly being weaponized)
- ⚠️ Limited to trending vulnerabilities only (~10 at a time)

---

## 5. SOCRadar CVE Radar

### Overview
SOCRadar CVE Radar is a free vulnerability monitoring tool providing real-time CVE search, analysis, and tracking capabilities.

### Free Access

#### ✅ **Web Interface**: YES - Free with Registration
- **URL**: https://socradar.io/labs/app/cve-radar
- **API**: Not publicly documented
- **Registration**: Free SOCRadar Labs account

#### 📊 **Features**
1. **Real-Time CVE Search**
   - Comprehensive CVE database search
   - AI-powered insights
   - Trend analysis

2. **Risk Assessment**
   - Emerging threat tracking
   - Risk trend visualization
   - Dark web monitoring integration

3. **Vulnerability Intelligence**
   - Open-source intelligence aggregation
   - Exploit availability tracking
   - Affected product tracking

### Integration Potential
- **Low** for automated integration (no public API)
- **Medium** for manual research workflows
- **Low** for SBOM automation

### CISO Prioritization Support
- ✅ Trend analysis for emerging threats
- ✅ Dark web monitoring context
- ⚠️ Manual workflow (no API for automation)

---

## 6. OpenCTI (Open Cyber Threat Intelligence Platform)

### Overview
OpenCTI is a comprehensive open-source threat intelligence platform built on STIX 2.1 standards with extensive connector ecosystem.

### Deployment & Architecture

#### ✅ **Open Source**: YES - Fully Free
- **Repository**: https://github.com/OpenCTI-Platform/connectors
- **License**: Open source
- **Deployment**: Docker Compose / Kubernetes

#### 🏗️ **Architecture Components**
1. **Neo4j** - Graph database for relationship modeling
2. **MinIO** - S3-compatible object storage
3. **RabbitMQ** - Message queue orchestration
4. **Redis** - Cache layer
5. **Elasticsearch** - Search functionality

All components available as Docker images with orchestration via Docker Compose.

#### 🔌 **Connector Ecosystem**

**CVE/Vulnerability Connectors**:
1. **CVE Connector**
   - Ingests CVE data from NVD
   - Converts to STIX 2.1 format
   - Filters by CVSS V3.1 base score
   - Configurable date ranges (max 120 days per query)
   - `pull_history` option for historical data

2. **MISP Connector**
   - Bi-directional sync with MISP instances
   - IoC, events, intelligence reports
   - Galaxy/tag conversion to OpenCTI entities
   - Attribute → Indicator conversion

**Configuration Example (docker-compose.yml)**:
```yaml
cve-connector:
  image: opencti/connector-cve:latest
  environment:
    - OPENCTI_URL=http://opencti:8080
    - OPENCTI_TOKEN=${OPENCTI_ADMIN_TOKEN}
    - CONNECTOR_ID=${CONNECTOR_CVE_ID}
    - CONNECTOR_NAME=CVE
    - CVE_INTERVAL=7 # days
    - CVE_MAX_DATE_RANGE=120
    - CVE_PULL_HISTORY=true
    - CVE_HISTORY_START_YEAR=2020
```

### STIX 2.1 Support
- **Full Implementation**: OpenCTI one of few platforms fully leveraging STIX 2.1
- **Data Model**: All threat intelligence represented as STIX objects
- **Interoperability**: Import/export with other STIX-compliant tools

### Integration Potential
- **HIGH** for comprehensive threat intelligence platform
- **HIGH** for CVE relationship modeling (Neo4j graph)
- **VERY HIGH** for existing SBOM if already in graph format
- **HIGH** for connector ecosystem (extensible)
- **COMPLEX** deployment (multiple components required)

### Neo4j Integration
- **Native**: OpenCTI uses Neo4j as core database
- **Graph Modeling**: CVEs, CPEs, products, vendors, relationships
- **Cypher Queries**: Direct graph analysis capabilities
- **Visualization**: Built-in graph visualization tools

### SBOM Integration Approach
If 267,487 CVEs and 200K orphaned SBOM nodes are in Neo4j:

1. **Deploy OpenCTI** with existing Neo4j instance (complex)
2. **Enable CVE Connector** to sync NVD data
3. **Custom Connector** to link SBOM nodes to CVE nodes
4. **STIX Mapping** for SBOM components → Vulnerabilities

**Complexity**: HIGH (requires Neo4j schema alignment)

### CISO Prioritization Support
- ✅ Comprehensive threat context (not just CVEs)
- ✅ Relationship modeling (threat actors → TTPs → vulnerabilities)
- ✅ STIX 2.1 interoperability
- ⚠️ Requires significant deployment effort
- ⚠️ Overkill if only CVE enrichment needed

---

## 7. Additional Free Resources

### CISA KEV (Known Exploited Vulnerabilities)
- **URL**: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- **Format**: JSON, CSV
- **Update Frequency**: Continuous
- **API**: Direct download (no rate limits)
- **Content**: ~1000 CVEs confirmed exploited in wild
- **CISO Value**: "Now" category - immediate action required

### NVD API (National Vulnerability Database)
- **URL**: https://nvd.nist.gov/developers/vulnerabilities
- **Status**: ⚠️ Rate-limited, performance issues (2023-2024)
- **Alternative**: Use VulnCheck NVD++ instead (free, faster)

### CVE Details
- **URL**: https://www.cvedetails.com/
- **Access**: Free web interface
- **API**: Limited/unofficial scrapers available
- **Content**: CVE details, vendor/product statistics, trends

### Exploit-DB
- **URL**: https://www.exploit-db.com/
- **API**: CSV download available
- **Content**: Public exploit code repository
- **Search**: CVE-based search
- **Integration**: Manual or scraping (no official API)

---

## Integration Architecture Recommendations

### For Existing Neo4j Database with 267,487 CVEs

#### Option A: Lightweight Enrichment (RECOMMENDED)
**Components**:
1. **EPSS API** - Primary exploitability scoring (all CVEs)
2. **VulnCheck Free APIs** - KEV + XDB enrichment
3. **AttackerKB API** - Community assessments (where available)
4. **Custom ETL Script** - Python → Neo4j ingestion

**Workflow**:
```python
# Pseudo-code
for cve in neo4j_cve_nodes:
    # EPSS (all CVEs)
    epss_data = requests.get(f"https://api.first.org/data/v1/epss?cve={cve.id}")
    cve.epss_score = epss_data['epss']
    cve.epss_percentile = epss_data['percentile']

    # VulnCheck KEV
    kev_data = vulncheck_api.check_kev(cve.id)
    cve.in_kev = kev_data['is_kev']

    # VulnCheck XDB
    xdb_data = vulncheck_api.check_xdb(cve.id)
    cve.exploit_available = len(xdb_data['exploits']) > 0
    cve.exploit_links = xdb_data['exploits']

    # AttackerKB (if available)
    akb_data = attackerkb_api.get_topic(cve.id)
    if akb_data:
        cve.community_score = akb_data['score']
        cve.exploitability_metadata = akb_data['metadata']

    neo4j.update_node(cve)
```

**Advantages**:
- ✅ All free tools
- ✅ Comprehensive enrichment
- ✅ Low deployment complexity
- ✅ No additional infrastructure

**Estimated Enrichment Coverage**:
- EPSS: 100% (all CVEs scored)
- KEV: ~0.4% (1,000 CVEs)
- XDB: ~5-10% (exploits available)
- AttackerKB: ~2-5% (community assessed)

#### Option B: Full Threat Intelligence Platform
**Components**:
1. **OpenCTI** - Full deployment with Docker
2. **CVE Connector** - NVD integration
3. **Custom SBOM Connector** - Link existing nodes
4. **Neo4j Integration** - Shared or separate instance

**Advantages**:
- ✅ Comprehensive threat intelligence
- ✅ STIX 2.1 interoperability
- ✅ Relationship modeling (CVEs + threat actors + campaigns)
- ✅ Built-in Neo4j support

**Disadvantages**:
- ❌ Complex deployment (6+ Docker containers)
- ❌ High resource requirements
- ❌ Steep learning curve
- ❌ Overkill for CVE enrichment only

### For SBOM Node Connection (200K Orphaned Nodes)

#### Challenge
200K orphaned SBOM nodes likely represent:
- Software components without CVE links
- Products without identified vulnerabilities
- Dependencies without vulnerability mappings

#### Solution: Component → CVE Mapping

**Step 1: CPE Matching**
```cypher
// Match SBOM components to CVE CPEs
MATCH (sbom:Component)
MATCH (cve:CVE)-[:AFFECTS]->(cpe:CPE)
WHERE sbom.name = cpe.product
  AND sbom.vendor = cpe.vendor
  AND sbom.version = cpe.version
CREATE (sbom)-[:VULNERABLE_TO]->(cve)
```

**Step 2: VulnCheck CPE Enrichment**
- Use VulnCheck NVD++ API to get CPE data
- Enrich SBOM nodes with CPE identifiers
- Re-run matching query

**Step 3: EPSS Prioritization**
```cypher
// Add EPSS scores to matched vulnerabilities
MATCH (sbom:Component)-[:VULNERABLE_TO]->(cve:CVE)
WHERE exists(cve.epss_score)
WITH sbom, collect(cve) as cves
WITH sbom, [c in cves WHERE c.epss_score > 0.2] as high_risk_cves
SET sbom.high_risk_vuln_count = size(high_risk_cves)
```

---

## CISO Prioritization Framework: Now/Next/Never

### Framework Implementation with Free Tools

#### NOW (Immediate Action Required)
**Data Sources**:
1. **CISA KEV** - Confirmed wild exploitation
2. **VulnCheck KEV** - Extended KEV with 80% more CVEs
3. **CVEmon** - Trending CVEs (social media signals)
4. **EPSS > 0.7** - Very high exploitation probability

**Query Example**:
```cypher
MATCH (cve:CVE)
WHERE cve.in_cisa_kev = true
   OR cve.in_vulncheck_kev = true
   OR cve.epss_score > 0.7
   OR cve.trending_rank <= 10
RETURN cve
ORDER BY cve.epss_score DESC
```

#### NEXT (Schedule for Patching)
**Data Sources**:
1. **EPSS 0.2 - 0.7** - Moderate-high exploitation probability
2. **AttackerKB Assessments** - Community flagged
3. **VulnCheck XDB** - PoC exploits available

**Query Example**:
```cypher
MATCH (cve:CVE)
WHERE cve.epss_score >= 0.2 AND cve.epss_score < 0.7
   OR cve.exploit_available = true
   OR exists(cve.attackerkb_score)
RETURN cve
ORDER BY cve.epss_score DESC, cve.cvss_score DESC
```

#### NEVER (Monitor, Low Priority)
**Data Sources**:
1. **EPSS < 0.2** - Low exploitation probability
2. **No Exploit Available** - No PoC in XDB
3. **Not Trending** - No social media attention

**Query Example**:
```cypher
MATCH (cve:CVE)
WHERE cve.epss_score < 0.2
  AND cve.exploit_available = false
  AND NOT exists(cve.trending_rank)
  AND cve.in_cisa_kev = false
RETURN cve
ORDER BY cve.cvss_score DESC
```

### Prioritization Score Formula
```python
def calculate_priority_score(cve):
    score = 0

    # KEV = highest priority
    if cve.in_cisa_kev or cve.in_vulncheck_kev:
        score += 100

    # EPSS (0-100 scale)
    score += cve.epss_score * 50

    # CVSS (0-10 → 0-30 scale)
    score += (cve.cvss_score / 10) * 30

    # Exploit availability
    if cve.exploit_available:
        score += 20

    # Trending
    if cve.trending_rank and cve.trending_rank <= 10:
        score += 15

    # Community assessment
    if cve.attackerkb_score:
        score += (cve.attackerkb_score / 10) * 10

    return min(score, 200)  # Cap at 200

# Classification
if score >= 150: priority = "NOW"
elif score >= 75: priority = "NEXT"
else: priority = "NEVER"
```

---

## API Rate Limits & Restrictions Summary

| Tool | Free API | Auth Required | Rate Limit | Bulk Access |
|------|----------|---------------|------------|-------------|
| **EPSS** | ✅ Yes | ❌ No | None stated | ✅ Batch queries |
| **VulnCheck** | ✅ Yes | ✅ API key (free) | Not public | ✅ Index queries |
| **AttackerKB** | ✅ Yes | ✅ API key (free) | Not stated | ✅ List endpoints |
| **CVEmon** | ⚠️ Web only | ❌ No | N/A (RSS only) | ⚠️ RSS feed |
| **SOCRadar** | ⚠️ Web only | ✅ Account | N/A | ❌ No API |
| **OpenCTI** | ✅ Self-hosted | ✅ Local | Self-managed | ✅ Full control |
| **CISA KEV** | ✅ Yes | ❌ No | None | ✅ Full download |

---

## Implementation Complexity Assessment

| Integration Task | Complexity | Effort | Dependencies |
|-----------------|------------|--------|--------------|
| **EPSS Enrichment** | 🟢 Low | 2-4 hours | Python + requests |
| **VulnCheck API** | 🟢 Low | 4-8 hours | API key + Python |
| **AttackerKB API** | 🟢 Low | 3-6 hours | API key + Python |
| **Neo4j Ingestion** | 🟡 Medium | 1-2 days | Neo4j driver + ETL script |
| **SBOM Linking** | 🟡 Medium | 2-4 days | CPE matching + validation |
| **CVEmon RSS** | 🟢 Low | 2-4 hours | RSS parser |
| **OpenCTI Deployment** | 🔴 High | 1-2 weeks | Docker, Neo4j, config |
| **Full Integration** | 🟡 Medium | 1-2 weeks | All above combined |

---

## Recommended Implementation Roadmap

### Phase 1: Quick Wins (Week 1)
1. **EPSS Enrichment** - Add to all 267,487 CVEs
2. **CISA KEV Flagging** - Mark confirmed exploited CVEs
3. **VulnCheck KEV** - Add extended KEV data
4. **Priority Scoring** - Implement Now/Next/Never classification

**Expected Result**: Immediate prioritization capability

### Phase 2: Exploit Intelligence (Week 2)
1. **VulnCheck XDB** - Map exploits to CVEs
2. **AttackerKB API** - Add community assessments
3. **CVEmon RSS** - Setup trending alerts

**Expected Result**: Exploitability context for decision-making

### Phase 3: SBOM Connection (Week 3-4)
1. **CPE Extraction** - From VulnCheck NVD++
2. **Component Matching** - SBOM → CVE linking via CPE
3. **Validation** - Verify match accuracy
4. **Prioritization** - Apply scoring to SBOM components

**Expected Result**: 200K orphaned nodes connected to vulnerability data

### Phase 4: Advanced Features (Optional)
1. **OpenCTI Deployment** - If comprehensive threat intel needed
2. **Custom Connectors** - For proprietary data sources
3. **Automation** - Scheduled refreshes and alerts

---

## Cost Analysis

### Free Tier Limitations
- **EPSS**: Unlimited, no restrictions
- **VulnCheck**: Free tier limits not public (likely adequate for research)
- **AttackerKB**: Community tier (adequate for most use cases)
- **OpenCTI**: Infrastructure costs only (AWS/Azure hosting)

### Estimated Costs
- **Option A (Lightweight)**: $0 for tools + hosting costs for scripts
- **Option B (OpenCTI)**: $0 for tools + $50-200/mo for infrastructure
- **Enterprise Alternatives**: $10K-100K+/year for commercial platforms

---

## Security & Privacy Considerations

### API Key Management
- Store VulnCheck and AttackerKB keys securely (env vars, secrets manager)
- Rotate keys periodically
- Never commit keys to version control

### Data Handling
- EPSS, KEV, NVD data is public (no privacy concerns)
- AttackerKB assessments are community-contributed (public)
- No PII or sensitive data in these APIs

### Rate Limit Respect
- Implement exponential backoff for API calls
- Cache results to minimize requests
- Batch queries where possible

---

## Conclusion

### Key Recommendations

1. **✅ IMMEDIATE**: Implement EPSS enrichment (free, no auth, all CVEs)
2. **✅ HIGH PRIORITY**: Integrate VulnCheck free APIs (KEV + XDB)
3. **✅ RECOMMENDED**: Add AttackerKB for community intelligence
4. **⚠️ CONSIDER**: CVEmon RSS for trending alerts (limited scope)
5. **❌ DEFER**: OpenCTI unless full threat intelligence platform needed

### Expected Outcomes

**CVE Enrichment**:
- 100% of 267,487 CVEs enriched with EPSS scores
- ~1,000 CVEs flagged with KEV status
- ~5-10% CVEs linked to exploit code
- ~2-5% CVEs with community assessments

**SBOM Integration**:
- Significant reduction in orphaned nodes via CPE matching
- Component-level vulnerability prioritization
- Risk-based patching roadmap

**CISO Decision Support**:
- Data-driven Now/Next/Never classification
- Quantifiable risk scores (not just CVSS severity)
- Automated threat intelligence feeds

### Total Cost
**$0 for all recommended tools** + hosting costs for ETL scripts/infrastructure

---

## References & Resources

### Official Documentation
- **EPSS**: https://www.first.org/epss/
- **VulnCheck**: https://docs.vulncheck.com/
- **AttackerKB**: https://api.attackerkb.com/v1/api-docs/docs
- **OpenCTI**: https://docs.opencti.io/
- **CISA KEV**: https://www.cisa.gov/known-exploited-vulnerabilities-catalog

### GitHub Repositories
- **OpenCTI**: https://github.com/OpenCTI-Platform/opencti
- **AttackerKB Python**: https://github.com/kevthehermit/attackerkb-api
- **CVE Prioritizer**: https://github.com/TURROKS/CVE_Prioritizer

### Related Tools
- **OWASP Dependency-Track**: SBOM analysis with EPSS integration
- **Neo4Cyclone**: CycloneDX SBOM → Neo4j ingestion
- **CVE Binary Tool**: SBOM component vulnerability scanning

---

**Research Completed**: 2025-11-01
**Next Steps**: Implement Phase 1 (EPSS + KEV enrichment) and validate results.
