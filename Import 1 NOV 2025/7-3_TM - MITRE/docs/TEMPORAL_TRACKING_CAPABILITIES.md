# Temporal Tracking Capabilities - Gap Analysis

**File**: TEMPORAL_TRACKING_CAPABILITIES.md
**Created**: 2025-11-11
**Version**: 1.0.0
**Author**: System Architecture Designer
**Purpose**: Document temporal tracking capabilities vs McKenney's requirements
**Status**: ACTIVE

---

## Executive Summary

**McKenney's Requirement**: "Temporal - CVEs change over time - The exploit code that is available within the CVE changes and evolves - The attack patterns that the exploit code represent change in real time"

**Current Status**: ⚠️ **PARTIAL IMPLEMENTATION** - Basic temporal fields exist, but real-time evolution tracking is MISSING.

**Gap Severity**: 🔴 **HIGH** - Core requirement for tracking CVE evolution over time is not implemented.

---

## 1. Current Temporal Capabilities (IMPLEMENTED)

### 1.1 Neo4j Schema Temporal Fields

**Source**: `scripts/neo4j_mitre_import.cypher`

```cypher
// CVE nodes have temporal metadata
{
  modified: '2025-04-15T19:58:00.917Z',  // Last modified timestamp
  publishedDate: datetime,                // Publication date
  lastModifiedDate: datetime              // Last modification date
}

// MITRE Techniques have temporal metadata
{
  modified: '2025-04-15T19:58:01.010Z'   // Last modified timestamp
}
```

**Evidence Found**:
- Line 17: `modified: '2025-04-15T19:58:00.917Z'` in AttackTechnique nodes
- Consistent `modified` field across all MITRE entities
- CVE nodes include `publishedDate` and `lastModifiedDate`

### 1.2 API Query Temporal Filtering

**Source**: `deployment/query_api/queries/cve_impact.py`

```python
# Query CVEs by publication date
WHERE date(cve.publishedDate) = date($today)

# Return temporal metadata
cve.publishedDate AS publishedDate,
cve.lastModified: cve.lastModifiedDate
```

**Capabilities**:
1. ✅ Filter CVEs by publication date ("today's CVEs")
2. ✅ Return modification timestamps in query results
3. ✅ Date-based queries for recent vulnerabilities

**Files with Temporal Queries**:
- `deployment/query_api/queries/cve_impact.py` (Lines 132, 152, 191, 225-226)
- `deployment/query_api/queries/attack_path.py` (Lines 347, 379, 439, 489)
- `deployment/query_api/queries/asset_management.py` (Lines 77, 80-81, 253-254, 260-261)

### 1.3 Equipment Lifecycle Tracking

**Source**: `deployment/query_api/queries/asset_management.py`

```cypher
// Equipment age calculation
duration.between(date(eq.installDate), date()).days AS ageInDays

// Maintenance status temporal logic
CASE
  WHEN date(eq.lastMaintenanceDate) < date() - duration({days: 90}) THEN 'OVERDUE'
  WHEN date(eq.lastMaintenanceDate) < date() - duration({days: 30}) THEN 'DUE_SOON'
  ELSE 'UP_TO_DATE'
END AS maintenanceStatus

// End-of-life tracking
CASE
  WHEN software.endOfLife IS NOT NULL AND date(software.endOfLife) < date() THEN 'EOL'
  WHEN software.endOfLife IS NOT NULL AND date(software.endOfLife) < date() + duration({months: 6}) THEN 'APPROACHING_EOL'
  ELSE 'SUPPORTED'
END AS supportStatus
```

**Capabilities**:
1. ✅ Track equipment installation dates and age
2. ✅ Monitor maintenance schedules with temporal rules
3. ✅ Software end-of-life detection and forecasting
4. ✅ License expiration tracking

---

## 2. MISSING Temporal Capabilities (NOT IMPLEMENTED)

### 2.1 CVE Evolution Tracking ❌

**McKenney's Requirement**: "The exploit code that is available within the CVE changes and evolves"

**What's Missing**:
1. ❌ No version history for CVE descriptions
2. ❌ No tracking of exploit code changes over time
3. ❌ No historical snapshots of CVE severity/CVSS scores
4. ❌ No change log for CVE modifications

**Expected Schema** (FROM DESIGN DOC):
```cypher
// From SEMANTIC_MAPPING_PROBABILISTIC_DESIGN.md Section 9.2
class TemporalAttackModel {
    time_adjusted_probability(cve_id, current_date) {
        days_since_disclosure = (current_date - cve.published_date).days

        // Exploit maturity curve
        exploit_maturity = 1 / (1 + exp(-0.1 * (days_since_disclosure - 30)))

        // Patch adoption decay
        patch_adoption = 0.8 * exp(-days_since_disclosure / 180)

        time_factor = exploit_maturity * (1 - patch_adoption)
    }
}
```

**What SHOULD Exist**:
```cypher
// Temporal CVE version tracking (NOT IMPLEMENTED)
(CVE)-[:HAS_VERSION {
    version: int,
    validFrom: datetime,
    validTo: datetime,
    changes: string
}]->(CVEVersion {
    description: string,
    cvssScore: float,
    exploitCode: string,
    exploitMaturity: string  // ['none', 'poc', 'functional', 'high']
})

// Exploit evolution tracking (NOT IMPLEMENTED)
(CVE)-[:HAS_EXPLOIT_TIMELINE]->(ExploitVersion {
    timestamp: datetime,
    exploitType: string,  // ['poc', 'weaponized', 'malware']
    availability: string,  // ['private', 'public', 'commercial']
    sophistication: string
})
```

### 2.2 Attack Pattern Evolution ❌

**McKenney's Requirement**: "The attack patterns that the exploit code represent change in real time"

**What's Missing**:
1. ❌ No time-series tracking of CAPEC pattern associations
2. ❌ No historical mapping changes between CWE→CAPEC→Technique
3. ❌ No temporal probability adjustments for attack chains
4. ❌ No "trending" attack techniques over time

**Expected Implementation** (FROM DESIGN):
```python
# From SEMANTIC_MAPPING_PROBABILISTIC_DESIGN.md
class TemporalKnowledgeGraph:
    """Track evolving relationships over time"""

    def track_mapping_changes(self, timestamp):
        # Track CWE→CAPEC mappings over time
        # Track CAPEC→Technique associations over time
        # Detect emerging attack patterns

    def temporal_attack_probability(self, cve_id, time_range):
        # Calculate attack probability considering:
        # - Time since disclosure
        # - Exploit maturity progression
        # - Patch adoption rates
        # - Trending attack techniques
```

**What SHOULD Exist**:
```cypher
// Temporal relationship tracking (NOT IMPLEMENTED)
(CWE)-[:ENABLES {
    strength: float,
    validFrom: datetime,
    validTo: datetime,
    historicalStrength: [
        {timestamp: datetime, strength: float}
    ]
}]->(CAPEC)

// Attack technique trending (NOT IMPLEMENTED)
(Technique)-[:TRENDING {
    period: string,  // 'week', 'month', 'quarter'
    frequency: float,
    firstSeen: datetime,
    lastSeen: datetime,
    volumeChange: float  // % change in usage
}]->(TimePeriod)
```

### 2.3 Real-Time Evolution Tracking ❌

**McKenney's Requirement**: "changes in real time"

**What's Missing**:
1. ❌ No event stream for CVE modifications
2. ❌ No change detection system
3. ❌ No notification system for CVE updates
4. ❌ No differential snapshots

**What SHOULD Exist**:
```python
# Real-time change detection (NOT IMPLEMENTED)
class CVEChangeDetector:
    def monitor_nvd_feed(self):
        """Poll NVD API for CVE modifications"""

    def detect_changes(self, old_cve, new_cve):
        """Identify what changed in CVE"""
        changes = {
            'severity_changed': old_cve.cvss != new_cve.cvss,
            'description_changed': old_cve.description != new_cve.description,
            'exploit_added': new_cve.exploitCode and not old_cve.exploitCode,
            'cwe_changed': old_cve.cwe != new_cve.cwe
        }
        return changes

    def create_version_snapshot(self, cve_id, changes):
        """Store historical version in graph"""
```

### 2.4 Time-Series Analysis ❌

**What's Missing**:
1. ❌ No aggregate temporal queries (e.g., "CVEs over time")
2. ❌ No trend analysis capabilities
3. ❌ No temporal graph analytics
4. ❌ No time-window queries

**What SHOULD Exist**:
```cypher
// Time-series aggregation queries (NOT IMPLEMENTED)
MATCH (cve:CVE)
WHERE cve.publishedDate >= datetime($startDate)
  AND cve.publishedDate <= datetime($endDate)
WITH date(cve.publishedDate) AS day, count(cve) AS cveCount
RETURN day, cveCount
ORDER BY day

// Temporal path analysis (NOT IMPLEMENTED)
MATCH path = (cve:CVE)-[:EXPLOITS {
    validFrom: datetime,
    validTo: datetime
}]->(cwe:CWE)
WHERE $queryDate >= validFrom AND $queryDate <= validTo
RETURN path
```

---

## 3. Comparison Table: Designed vs Implemented

| Capability | Designed (SEMANTIC_MAPPING doc) | Implemented (Actual System) | Gap |
|------------|----------------------------------|----------------------------|-----|
| **CVE Version History** | TemporalAttackModel with exploit maturity tracking | Single `modified` timestamp only | 🔴 MAJOR |
| **Exploit Evolution** | Time-adjusted probability curves | None | 🔴 MAJOR |
| **Attack Pattern Trending** | Historical mapping strength tracking | Static relationships only | 🔴 MAJOR |
| **Temporal Probability** | Days-since-disclosure adjustments | None | 🔴 MAJOR |
| **Change Detection** | Real-time monitoring system | None | 🔴 MAJOR |
| **Time-Series Queries** | Aggregate temporal analytics | Date filtering only | 🟡 MODERATE |
| **Historical Snapshots** | Version-based graph traversal | None | 🔴 MAJOR |
| **Publication Date** | ✓ | ✓ | ✅ IMPLEMENTED |
| **Equipment Lifecycle** | Not in design | ✓ Implemented | ✅ BONUS |

---

## 4. Use Cases BLOCKED by Missing Temporal Capabilities

### 4.1 "Show me how this CVE's risk has changed over time"
**Status**: ❌ BLOCKED

**Why**: No historical CVSS scores, no exploit maturity tracking, no temporal probability model.

**User Impact**: Cannot understand if a CVE is becoming more or less dangerous.

### 4.2 "Alert me when a CVE I'm tracking gets exploit code published"
**Status**: ❌ BLOCKED

**Why**: No exploit availability tracking, no change detection, no event notifications.

**User Impact**: Users don't know when theoretical vulnerabilities become actively exploited.

### 4.3 "What attack techniques are trending this month?"
**Status**: ❌ BLOCKED

**Why**: No technique frequency tracking over time, no temporal aggregation.

**User Impact**: Cannot identify emerging attack patterns or shift defensive priorities.

### 4.4 "Replay the attack chain analysis as of 6 months ago"
**Status**: ❌ BLOCKED

**Why**: No historical snapshots, no temporal graph traversal, no time-travel queries.

**User Impact**: Cannot understand how risk assessment would have differed with historical data.

---

## 5. Implementation Roadmap

### Phase 1: Foundational Temporal Schema (2-3 weeks)
**Priority**: 🔴 CRITICAL

```cypher
// Add CVE versioning
CREATE (cve:CVE {id: 'CVE-2024-1234'})
CREATE (version:CVEVersion {
  version: 1,
  validFrom: datetime('2024-01-15T00:00:00Z'),
  validTo: NULL,  // Current version
  description: '...',
  cvssScore: 7.5,
  exploitMaturity: 'poc'
})
CREATE (cve)-[:HAS_VERSION]->(version)

// Add exploit timeline
CREATE (exploit:ExploitEvent {
  timestamp: datetime('2024-02-01T12:00:00Z'),
  type: 'public_exploit',
  source: 'exploit-db',
  sophistication: 'medium'
})
CREATE (cve)-[:EXPLOIT_AVAILABLE]->(exploit)

// Add temporal relationships
MATCH (cwe:CWE)-[r:ENABLES]->(capec:CAPEC)
SET r.validFrom = datetime('2024-01-01T00:00:00Z'),
    r.validTo = NULL,
    r.strengthHistory = []
```

### Phase 2: Change Detection System (3-4 weeks)
**Priority**: 🔴 CRITICAL

```python
# Implement NVD API monitoring
class NVDMonitor:
    def poll_nvd_feed(self, interval='1h'):
        """Poll NVD API for CVE modifications"""

    def detect_changes(self, cve_data):
        """Compare current vs previous state"""

    def create_snapshot(self, cve_id, changes):
        """Store version snapshot in Neo4j"""

    def notify_subscribers(self, cve_id, changes):
        """Send alerts for significant changes"""
```

### Phase 3: Temporal Query API (2 weeks)
**Priority**: 🟡 HIGH

```python
# Add temporal query endpoints
@app.get("/api/v1/query/cve-timeline")
async def cve_timeline_query(
    cveId: str,
    startDate: Optional[str] = None,
    endDate: Optional[str] = None
):
    """Get CVE history over time"""

@app.get("/api/v1/query/attack-trends")
async def attack_trends_query(
    period: str = "month",  # week, month, quarter
    technique: Optional[str] = None
):
    """Get trending attack techniques"""
```

### Phase 4: Time-Series Analytics (2-3 weeks)
**Priority**: 🟡 MEDIUM

```cypher
// Implement temporal aggregation queries
MATCH (cve:CVE)-[:HAS_VERSION]->(v:CVEVersion)
WHERE v.validFrom >= datetime($startDate)
  AND v.validFrom <= datetime($endDate)
WITH date(v.validFrom) AS day,
     avg(v.cvssScore) AS avgCVSS,
     count(cve) AS cveCount
RETURN day, avgCVSS, cveCount
ORDER BY day

// Implement temporal path queries
MATCH path = (cve:CVE)-[r:EXPLOITS]->(cwe:CWE)
WHERE r.validFrom <= datetime($asOfDate)
  AND (r.validTo IS NULL OR r.validTo >= datetime($asOfDate))
RETURN path
```

---

## 6. Data Sources for Temporal Tracking

### 6.1 NVD API (CVE Evolution)
**URL**: https://services.nvd.nist.gov/rest/json/cves/2.0

**Fields to Track**:
- `lastModifiedDate` - When CVE was last updated
- `published` - Initial publication date
- `metrics.cvssMetricV31.cvssData` - CVSS scores (can change)
- `descriptions` - Vulnerability descriptions (can be updated)
- `references` - External references (grow over time)

**Update Frequency**: Poll every 2 hours for modifications

### 6.2 Exploit-DB (Exploit Availability)
**URL**: https://www.exploit-db.com/

**Fields to Track**:
- Exploit publication date
- Exploit type (PoC, weaponized, malware)
- Exploit maturity level

### 6.3 MITRE ATT&CK (Technique Trends)
**URL**: https://attack.mitre.org/

**Fields to Track**:
- `modified` timestamp for techniques
- Technique→Tactic mappings (can change)
- Technique examples and detections (evolve)

---

## 7. Performance Considerations

### 7.1 Storage Impact

**Estimated Growth**:
- Current: ~50 CVEs/day × 365 = 18,250 CVEs/year
- With versioning: Assume 2 versions/CVE average = 36,500 version nodes/year
- Exploit events: ~10% of CVEs get exploits = 1,825 exploit events/year

**Storage Requirements**:
- CVEVersion nodes: ~500 bytes each = 18 MB/year
- ExploitEvent nodes: ~200 bytes each = 365 KB/year
- Temporal relationship history: ~1 KB/relationship = minimal

**Total**: ~20 MB/year additional storage (negligible)

### 7.2 Query Performance

**Temporal Queries**:
```cypher
// Without indexing: O(n) scan of all relationships
MATCH (cwe)-[r:ENABLES]->(capec)
WHERE r.validFrom <= $date AND (r.validTo IS NULL OR r.validTo >= $date)

// With temporal index: O(log n) lookup
CREATE INDEX temporal_enables FOR ()-[r:ENABLES]-() ON (r.validFrom, r.validTo)
```

**Optimization Strategy**:
1. Create composite indexes on `(validFrom, validTo)` for all temporal relationships
2. Use query hints for time-range queries
3. Cache recent temporal queries (1-hour TTL)
4. Partition historical data by year for archive queries

---

## 8. Risks of NOT Implementing Temporal Tracking

### 8.1 Business Risks

1. **Outdated Risk Assessments** 🔴 CRITICAL
   - Users see static CVE data that may be months out of date
   - Cannot detect when vulnerabilities become actively exploited
   - Risk scores don't reflect current threat landscape

2. **Missed Attack Pattern Shifts** 🔴 HIGH
   - Cannot identify emerging attack techniques
   - Defensive strategies based on stale intelligence
   - Competitive disadvantage vs. tools with temporal tracking

3. **Compliance Issues** 🟡 MEDIUM
   - Some regulations require tracking when vulnerabilities were discovered
   - Cannot prove due diligence in vulnerability monitoring
   - Audit trail gaps for security incidents

### 8.2 Technical Debt

1. **Retroactive Implementation** 🔴 HIGH
   - Harder to add temporal tracking to existing data
   - May require full database migration
   - Historical data lost permanently

2. **Integration Complexity** 🟡 MEDIUM
   - Third-party tools expect temporal capabilities
   - API users may need time-travel queries
   - Reporting tools need trend data

---

## 9. Conclusion

### Current State
✅ **BASIC temporal metadata exists** (publishedDate, modified timestamps)
✅ **DATE-BASED filtering works** (today's CVEs, recent vulnerabilities)
✅ **EQUIPMENT lifecycle tracking implemented** (install dates, EOL, maintenance)

### Missing Capabilities
❌ **CVE EVOLUTION TRACKING** - No version history for CVE changes
❌ **EXPLOIT MATURITY TIMELINE** - No tracking of exploit development progression
❌ **ATTACK PATTERN TRENDING** - No time-series analysis of techniques
❌ **REAL-TIME CHANGE DETECTION** - No monitoring system for CVE modifications
❌ **TEMPORAL GRAPH QUERIES** - No time-travel or historical snapshots

### Recommendation
**🔴 PRIORITY 1**: Implement Phase 1 (Foundational Temporal Schema) within next sprint

**Rationale**:
- Core requirement from McKenney explicitly stated
- Designed architecture already exists (SEMANTIC_MAPPING_PROBABILISTIC_DESIGN.md Section 9.2)
- Missing capability blocks critical use cases
- Technical debt increases with delay
- Competitive disadvantage vs. temporal-aware tools

---

**Document Status**: COMPLETE
**Next Steps**: Present gap analysis to stakeholders, prioritize Phase 1 implementation
**Dependencies**: Neo4j 5.x with temporal query support, NVD API access, monitoring infrastructure
