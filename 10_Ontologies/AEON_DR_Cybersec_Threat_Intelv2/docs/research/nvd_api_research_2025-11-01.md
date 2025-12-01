# NVD API v2.0 Complete CVE Dataset Re-Import Research

**File:** nvd_api_research_2025-11-01.md
**Created:** 2025-11-01
**Version:** 1.0.0
**Author:** Research Agent
**Purpose:** Research NVD API v2.0 capabilities for complete CVE dataset re-import
**Status:** ACTIVE

## Executive Summary

This research analyzed NVD API v2.0 capabilities for complete CVE dataset re-import to replace the current incomplete dataset. Key findings:

- **NVD API v2.0** is fully operational with comprehensive CVE data (2002-2025)
- **Bulk JSON feeds** available for initial import (2.5GB total compressed data)
- **Rate limits**: 5 req/30sec (no key) vs 50 req/30sec (with free API key)
- **Data completeness**: NVD provides significantly richer data than current database
- **Recommended approach**: Hybrid bulk download + incremental API sync

## 1. NVD API v2.0 Current Capabilities (November 2025)

### API Endpoints

**CVE API Base URL:**
```
https://services.nvd.nist.gov/rest/json/cves/2.0
```

**CVE Change History API:**
```
https://services.nvd.nist.gov/rest/json/cvehistory/2.0
```

### Authentication & Rate Limits

| Access Type | Rate Limit | Requests/30sec | Recommended Sleep | Cost |
|-------------|-----------|----------------|-------------------|------|
| **Without API Key** | 5 requests/30sec | ~1 req/6sec | 6 seconds | Free |
| **With API Key** | 50 requests/30sec | ~1 req/0.6sec | 2 seconds | Free |

**API Key Acquisition:** Free via https://nvd.nist.gov/developers/request-an-api-key

**Critical Finding:** API key provides 10x throughput improvement at zero cost.

### Query Capabilities

**CVE API Supports:**
- `cveId` - Individual CVE retrieval
- `cpeName` - Filter by product (CPE v2.3 format)
- `cvssV2/V3/V4Metrics` - CVSS vector filtering
- `cvssV2/V3/V4Severity` - Severity filtering
- `cweId` - Weakness identifier filtering
- `keywordSearch` - Full-text search
- `lastModStartDate/lastModEndDate` - Modification timeframe (120-day max window)
- `pubStartDate/pubEndDate` - Publication date filtering (120-day max window)
- `startIndex/resultsPerPage` - Pagination (max 2,000 results per page)

**Important Limitations:**
- Maximum date range: 120 consecutive days per query
- Maximum results per page: 2,000 CVEs
- CVSS v2 data frozen since July 2022 (no new metrics)

## 2. Bulk Download Options

### NVD JSON Data Feeds (Recommended for Initial Import)

**Year-Specific Feeds (2002-2025):**
```
https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{year}.json.gz
https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{year}.json.zip
```

**Update Frequencies:**
- Year feeds: Updated daily
- Recent/Modified feeds: Updated every 2 hours (last 8 days of changes)

**File Sizes (Compressed):**
| Year Range | Approx Size | CVE Count (estimated) |
|------------|-------------|----------------------|
| 2002-2010 | 5-10 MB | ~40,000 CVEs |
| 2011-2020 | 50-100 MB | ~120,000 CVEs |
| 2021-2024 | 18-20 MB/year | ~25,000 CVEs/year |
| **Total** | **~2.5 GB compressed** | **~240,000 CVEs** |

**Metadata Provided:**
- SHA256 checksums for integrity verification
- Last modified timestamps
- Uncompressed file sizes

**Data Completeness:**
- Complete CVE records from 2002 to present
- Includes all CVSS versions, CPE configurations, references, weaknesses
- Spanish translations available (optional)

### Alternative Bulk Sources

**CPE Dictionary & Match Feeds:**
- CPE Dictionary 2.0: 66.95 MB
- CPE Match 2.0: 576.83 MB (comprehensive product matching)

**Vendor Comments Feed:**
- Vendor-specific vulnerability information (0.07 MB)

## 3. Data Quality Comparison

### Current Database Schema (from cve_id_constraints_analysis.json)

**Current CVE Properties:**
- `id`, `cveId`, `cve_id` (3 different ID fields - redundant)
- `cvssV3BaseScore`, `cvss_score` (basic scoring)
- `severity`
- `published_date`, `created_time`
- `namespace`, `customer_namespace`
- `year`

**Indexes:**
- Basic range indexes on ID, score, severity, dates

### NVD API v2.0 Available Properties (from Sample CVE-2024-1086)

**Root CVE Fields:**
```json
{
  "id": "CVE-2024-1086",
  "sourceIdentifier": "cve-coordination@google.com",
  "published": "2024-01-31T13:15:10.827",
  "lastModified": "2025-10-27T17:06:37.437",
  "vulnStatus": "Analyzed",
  "cveTags": []
}
```

**Descriptions (Multi-language):**
```json
{
  "descriptions": [
    {"lang": "en", "value": "..."},
    {"lang": "es", "value": "..."}
  ]
}
```

**CVSS Metrics (Multiple Sources & Versions):**
```json
{
  "metrics": {
    "cvssMetricV31": [
      {
        "source": "cve-coordination@google.com",
        "type": "Secondary",
        "cvssData": {
          "version": "3.1",
          "vectorString": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H",
          "baseScore": 7.8,
          "baseSeverity": "HIGH",
          "attackVector": "LOCAL",
          "attackComplexity": "LOW",
          "privilegesRequired": "LOW",
          "userInteraction": "NONE",
          "scope": "UNCHANGED",
          "confidentialityImpact": "HIGH",
          "integrityImpact": "HIGH",
          "availabilityImpact": "HIGH"
        },
        "exploitabilityScore": 1.8,
        "impactScore": 5.9
      },
      {
        "source": "nvd@nist.gov",
        "type": "Primary",
        "cvssData": {...}
      }
    ]
  }
}
```

**CISA KEV (Known Exploited Vulnerabilities) Integration:**
```json
{
  "cisaExploitAdd": "2024-05-30",
  "cisaActionDue": "2024-06-20",
  "cisaRequiredAction": "Apply mitigations per vendor instructions...",
  "cisaVulnerabilityName": "Linux Kernel Use-After-Free Vulnerability"
}
```

**CWE Weaknesses:**
```json
{
  "weaknesses": [
    {
      "source": "cve-coordination@google.com",
      "type": "Secondary",
      "description": [{"lang": "en", "value": "CWE-416"}]
    }
  ]
}
```

**CPE Configurations (Affected Products):**
```json
{
  "configurations": [
    {
      "nodes": [
        {
          "operator": "OR",
          "cpeMatch": [
            {
              "vulnerable": true,
              "criteria": "cpe:2.3:o:linux:linux_kernel:*:*:*:*:*:*:*:*",
              "versionStartIncluding": "3.15",
              "versionEndExcluding": "5.15.149",
              "matchCriteriaId": "9E23B69A-DC79-4ABD-A29D-0CFDFA41F671"
            }
          ]
        }
      ]
    }
  ]
}
```

**References (with Tags):**
```json
{
  "references": [
    {
      "url": "https://...",
      "source": "cve-coordination@google.com",
      "tags": ["Exploit", "Patch", "Third Party Advisory"]
    }
  ]
}
```

### Data Gap Analysis

**Current Database MISSING Critical Properties:**

1. **CVSS Detailed Breakdown** - No attack vector, complexity, privileges required, etc.
2. **CISA KEV Data** - No known exploitation indicators
3. **CWE Mappings** - No weakness classifications
4. **CPE Configurations** - No affected product version ranges
5. **Multi-Source CVSS** - Only single score, missing primary/secondary sources
6. **Reference Tags** - No classification of reference types (Exploit, Patch, etc.)
7. **Multi-Language Descriptions** - English only
8. **Version History** - No lastModified tracking
9. **Vulnerability Status** - No analysis status (Analyzed, Awaiting Analysis, etc.)
10. **Exploitability/Impact Scores** - No CVSS subscores

**Data Richness Comparison:**

| Property Category | Current DB | NVD API v2.0 | Gap |
|-------------------|------------|--------------|-----|
| **Basic CVE Info** | ✅ ID, Score, Severity | ✅ + Status, Source, Tags | Moderate |
| **CVSS Metrics** | ⚠️ Single score | ✅ Full breakdown, multi-source | **CRITICAL** |
| **Affected Products** | ❌ None | ✅ CPE configs, version ranges | **CRITICAL** |
| **Weaknesses** | ❌ None | ✅ CWE mappings | **HIGH** |
| **Exploitation Data** | ❌ None | ✅ CISA KEV integration | **HIGH** |
| **References** | ⚠️ URLs only | ✅ URLs + tags | Moderate |
| **Descriptions** | ✅ English | ✅ Multi-language | Low |
| **Change Tracking** | ⚠️ Basic dates | ✅ Full modification history | Moderate |

**Overall Assessment:** Current database contains ~20% of available NVD data richness.

## 4. Alternative Data Sources

### VulnDB (Commercial)

**Provider:** Flashpoint (formerly Risk Based Security)

**Advantages:**
- Earlier vulnerability disclosure (faster than NVD)
- Enhanced/corrected data with human curation
- Additional exploitation PoC details
- RESTful API + CSV export
- Fully maps to CVE IDs

**Access:** Subscription-based (pricing not publicly available)

**Integration:** Compatible with Dependency-Track via VulnDB Data Mirror

**Use Case:** Premium organizations requiring earliest possible vulnerability intelligence

### VulnCheck NVD++

**Provider:** VulnCheck

**Advantages:**
- Stable, high-performance NVD 2.0 mirror
- API + downloadable JSON files
- Addresses NVD API reliability concerns
- Enhanced query capabilities

**Access:** VulnCheck membership required

**Use Case:** Organizations needing guaranteed NVD API uptime

### CVE.org Services

**Status:** API documentation requires JavaScript-enabled access (not accessible via static fetch)

**Known Capabilities:**
- Official CVE record authority
- CVE Services API for CVE numbering authorities
- Primary source for CVE IDs and initial publication

**Limitation:** Not designed for bulk vulnerability data consumption (NVD aggregates this data)

### OSV.dev (Open Source Vulnerabilities)

**Provider:** Google/Open Source community

**Advantages:**
- Completely free and open-source (Apache 2.0)
- Focuses on open-source package ecosystems
- RESTful API
- Aggregates multiple vulnerability databases

**Use Case:** Open-source software vulnerability tracking

## 5. Import Strategy Recommendations

### Strategy A: Bulk Download + Incremental Sync (RECOMMENDED)

**Phase 1: Initial Bulk Import**

1. **Download all NVD JSON year feeds** (2002-2025)
   - Source: https://nvd.nist.gov/vuln/data-feeds
   - Total download: ~2.5 GB compressed
   - Verification: SHA256 checksums
   - Estimated download time: 10-30 minutes (network dependent)

2. **Parallel processing** (10 workers)
   - Parse JSON year feeds
   - Transform to Neo4j schema
   - Batch insert with transaction batching
   - Estimated processing time: 2-4 hours for ~240,000 CVEs

3. **Database constraints handling**
   - DROP existing uniqueness constraints before import
   - Recreate constraints after import completion
   - Update range indexes for new properties

**Phase 2: Incremental Daily Sync**

1. **Use existing nvd_daily_sync.py** (already implemented)
   - Leverage NVD API with free API key
   - Fetch lastModified CVEs (last 24 hours)
   - Rate limit: 50 requests/30 sec
   - Run as daily cron job

2. **Enhancements needed**:
   - Add CISA KEV fields
   - Add CWE weakness mappings
   - Add CPE configurations
   - Add reference tags
   - Add CVSS detailed breakdown

**Total Estimated Time:**
- Initial import: 3-5 hours
- Daily sync: 5-15 minutes/day (depending on CVE volume)

### Strategy B: API-Only Import (Alternative)

**Approach:** Use NVD API v2.0 for complete import via pagination

**Challenges:**
- 120-day maximum date range per query
- Requires ~60 queries to cover 2002-2025 (20 years)
- 2,000 results max per page = multiple pages per date range
- Rate limiting: 50 requests/30sec with API key

**Estimated Time:**
- Query planning: ~60 date ranges (120-day windows)
- Pagination: ~120 pages (240K CVEs ÷ 2K per page)
- Total API calls: ~180 requests
- With rate limiting: 180 ÷ 50 = 3.6 windows = 2-3 minutes API calls
- Data processing: 2-4 hours

**Pros:**
- Always latest data
- Single data source
- No file downloads

**Cons:**
- More complex error handling
- Network dependency for entire import
- Higher API call volume

### Strategy C: Hybrid Multi-Source (Enterprise)

**Approach:** Combine NVD + VulnDB + CISA KEV

**Data Sources:**
1. NVD API v2.0 (primary vulnerability data)
2. VulnDB (early disclosure + enhanced data)
3. CISA KEV (known exploitation tracking)

**Implementation:**
- NVD as baseline
- VulnDB enrichment for subscribed customers
- CISA KEV for threat prioritization

**Pros:**
- Most comprehensive data
- Earliest vulnerability awareness
- Enhanced threat intelligence

**Cons:**
- Subscription costs for VulnDB
- Complex data merging logic
- Multiple API integrations

### Recommended Strategy: **Strategy A (Bulk + Incremental)**

**Rationale:**
1. **Fastest initial import** - Bulk files avoid API rate limiting
2. **Most reliable** - File downloads less prone to network interruptions
3. **Lower API usage** - Preserve rate limits for daily incremental sync
4. **Already partially implemented** - nvd_daily_sync.py exists for incremental
5. **Free** - No subscription costs

## 6. Implementation Details for Strategy A

### Phase 1: Bulk Import Script

**Script:** `scripts/nvd_bulk_import.py`

**Key Functions:**
```python
def download_nvd_feeds(start_year=2002, end_year=2025):
    """Download all NVD JSON year feeds with SHA256 verification."""

def parse_nvd_json_feed(json_path):
    """Parse NVD JSON feed and extract CVE records."""

def transform_to_neo4j_schema(cve_data):
    """Transform NVD CVE format to Neo4j-optimized schema."""

def batch_import_cves(cve_batch, driver, batch_size=1000):
    """Batch insert CVEs into Neo4j with transaction handling."""

def create_relationships(driver):
    """Create CVE relationships (CPE, CWE, References)."""
```

**Estimated Script Development:** 4-8 hours

### Phase 2: Schema Enhancements

**New Neo4j Properties:**
```cypher
// Core CVE properties
CREATE CONSTRAINT cve_id_unique ON (cve:CVE) ASSERT cve.id IS UNIQUE;

// Enhanced properties
(:CVE {
  id: string,                    // CVE-YYYY-NNNNN
  sourceIdentifier: string,      // cve-coordination@google.com
  published: datetime,
  lastModified: datetime,
  vulnStatus: string,            // Analyzed, Awaiting Analysis, etc.

  // CVSS v3.1 detailed breakdown
  cvssV3Vector: string,          // CVSS:3.1/AV:L/AC:L/...
  cvssV3BaseScore: float,
  cvssV3BaseSeverity: string,    // LOW, MEDIUM, HIGH, CRITICAL
  cvssV3AttackVector: string,
  cvssV3AttackComplexity: string,
  cvssV3PrivilegesRequired: string,
  cvssV3UserInteraction: string,
  cvssV3Scope: string,
  cvssV3ConfidentialityImpact: string,
  cvssV3IntegrityImpact: string,
  cvssV3AvailabilityImpact: string,
  cvssV3ExploitabilityScore: float,
  cvssV3ImpactScore: float,

  // CISA KEV
  cisaExploitAdd: date,
  cisaActionDue: date,
  cisaRequiredAction: string,
  cisaVulnerabilityName: string,

  // Metadata
  description: string,
  source: string,                // "nvd"
  updated_at: datetime
})

// Relationships
(:CVE)-[:HAS_WEAKNESS]->(:CWE {id: "CWE-416", name: "Use After Free"})
(:CVE)-[:AFFECTS_PRODUCT]->(:CPE {criteria: "cpe:2.3:..."})
(:CVE)-[:REFERENCES]->(:Reference {url: string, tags: [string]})
```

**Migration Cypher:**
```cypher
// Add new properties to existing CVEs
MATCH (cve:CVE)
SET
  cve.vulnStatus = 'Pending Analysis',
  cve.updated_at = datetime()
RETURN count(cve);

// Create CWE nodes
CREATE CONSTRAINT cwe_id_unique ON (cwe:CWE) ASSERT cwe.id IS UNIQUE;

// Create CPE nodes
CREATE CONSTRAINT cpe_criteria_unique ON (cpe:CPE) ASSERT cpe.criteria IS UNIQUE;
```

### Phase 3: Daily Sync Enhancements

**Update nvd_daily_sync.py:**

1. **Add CISA KEV extraction** (lines 205-210)
2. **Add CWE relationship creation** (new function)
3. **Add CPE configuration parsing** (lines 222-231 enhancement)
4. **Add reference tag extraction** (new function)
5. **Add CVSS detailed breakdown** (lines 206-211 enhancement)

**Estimated Enhancement Time:** 3-5 hours

## 7. Time Estimates Summary

| Task | Estimated Time | Dependencies |
|------|---------------|--------------|
| **Phase 1: Bulk Import** | | |
| Download NVD feeds | 30 minutes | Network speed |
| Develop import script | 4-8 hours | Python dev |
| Run initial import | 2-4 hours | Database performance |
| Verify data integrity | 1 hour | - |
| **Subtotal Phase 1** | **8-14 hours** | |
| | | |
| **Phase 2: Schema Migration** | | |
| Design Neo4j schema | 2 hours | Phase 1 complete |
| Write migration scripts | 3 hours | - |
| Run migration | 30 minutes | - |
| Test queries | 1 hour | - |
| **Subtotal Phase 2** | **6-7 hours** | |
| | | |
| **Phase 3: Daily Sync** | | |
| Enhance nvd_daily_sync.py | 3-5 hours | Phase 2 complete |
| Test incremental sync | 1 hour | - |
| Setup cron automation | 30 minutes | - |
| **Subtotal Phase 3** | **4-7 hours** | |
| | | |
| **TOTAL PROJECT** | **18-28 hours** | ~3-4 days |

**Production Deployment:** Add 4-8 hours for testing, documentation, and monitoring setup.

**Total End-to-End:** 22-36 hours (3-5 business days)

## 8. Risk Assessment

### High Risks

1. **Database Constraint Conflicts**
   - **Risk:** Multiple CVE ID properties (`id`, `cveId`, `cve_id`) may conflict
   - **Mitigation:** Drop constraints before import, normalize to single `id` property
   - **Impact:** Import failure, data corruption

2. **API Rate Limit Exhaustion**
   - **Risk:** Bulk API approach hits rate limits
   - **Mitigation:** Use bulk downloads instead of API for initial import
   - **Impact:** Extended import time (hours → days)

### Medium Risks

1. **Network Interruption During Download**
   - **Risk:** Large file downloads (2.5GB) interrupted
   - **Mitigation:** Resume capability, chunk downloads, SHA256 verification
   - **Impact:** Re-download time

2. **Memory Exhaustion**
   - **Risk:** Loading large JSON files (18MB+) into memory
   - **Mitigation:** Streaming JSON parser, batch processing
   - **Impact:** Script crashes, incomplete import

### Low Risks

1. **Schema Evolution**
   - **Risk:** NVD adds new fields in future
   - **Mitigation:** Flexible schema design, regular updates
   - **Impact:** Missing new data until script updated

## 9. Success Criteria

### Quantitative Metrics

- [ ] **Completeness:** 240,000+ CVEs imported (2002-2025)
- [ ] **Data Richness:** 90%+ of NVD properties captured
- [ ] **Performance:** <10 sec query time for complex CVSS filters
- [ ] **Accuracy:** 100% SHA256 verification for bulk downloads
- [ ] **Freshness:** Daily sync completes in <15 minutes

### Qualitative Metrics

- [ ] **CISA KEV Integration:** Known exploited CVEs flagged
- [ ] **CPE Mappings:** Product-to-CVE relationships established
- [ ] **CWE Classification:** Weakness taxonomy integrated
- [ ] **CVSS Breakdown:** Attack vector/complexity queryable
- [ ] **Reference Tags:** Exploit/Patch references classified

## 10. Next Steps

**Immediate Actions (Week 1):**

1. Obtain NVD API key (free, instant)
2. Download sample NVD JSON feed (test year 2024)
3. Design Neo4j schema enhancements
4. Develop bulk import script prototype

**Short-Term Actions (Week 2-3):**

1. Full bulk download execution
2. Database migration
3. Enhanced daily sync deployment
4. Validation and testing

**Long-Term Actions (Month 2+):**

1. Monitor daily sync performance
2. Implement CISA KEV alerting
3. Develop CVE analytics dashboards
4. Consider VulnDB integration for premium data

## 11. References

### Official Documentation

- NVD API v2.0: https://nvd.nist.gov/developers/vulnerabilities
- NVD Data Feeds: https://nvd.nist.gov/vuln/data-feeds
- NVD API Key Request: https://nvd.nist.gov/developers/request-an-api-key
- CISA KEV Catalog: https://www.cisa.gov/known-exploited-vulnerabilities-catalog

### Alternative Sources

- VulnDB: https://flashpoint.io/ignite/vulnerability-intelligence/
- VulnCheck NVD++: https://www.vulncheck.com/blog/nvd-plus-plus
- OSV.dev: https://osv.dev/

### Technical Resources

- NVD JSON Schema 2.0: https://csrc.nist.gov/schema/nvd/api/2.0/
- CPE Specification: https://nvd.nist.gov/products/cpe
- CVSS v3.1 Specification: https://www.first.org/cvss/v3.1/specification-document

---

**Research Completed:** 2025-11-01
**Next Review:** After Phase 1 implementation
**Contact:** Research Agent via Qdrant memory namespace 'vulncheck_implementation'
