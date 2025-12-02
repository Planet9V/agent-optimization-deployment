# Enhancement 03 - SBOM Dependency Analysis

**File**: `/home/jim/2_OXOT_Projects_Dev/4_AEON_DT_CyberDTc3_2025_11_25/Enhancement_03_SBOM_Analysis/README.md`
**Created**: 2025-11-25 14:45:00 UTC
**Modified**: 2025-11-25 14:45:00 UTC
**Version**: v1.0.0
**Author**: Claude Code + AEON DT Swarm
**Purpose**: SBOM ingestion framework with npm/PyPI package analysis and CVE vulnerability mapping
**Status**: ACTIVE

## Executive Summary

Enhancement 03 implements Software Bill of Materials (SBOM) ingestion and dependency vulnerability analysis for the AEON Digital Twin cybersecurity platform. This enhancement integrates library-level vulnerability detection, transitive dependency tracking, and CVE correlation across npm and Python ecosystem packages.

### Key Capabilities

- **SBOM Ingestion**: Support for CycloneDX, SPDX, and package manager native formats
- **Package Analysis**: npm and PyPI package vulnerability scanning with 316K CVE nodes
- **Dependency Resolution**: Transitive dependency mapping and chain-of-custody tracking
- **Vulnerability Correlation**: CVE-to-package-to-application linkage and remediation paths
- **Intelligence Integration**: Correlation with APT threat intelligence and STIX indicators
- **Executive Reporting**: Risk aggregation and remediation roadmaps

## Architecture Overview

### Component Stack

```
┌─────────────────────────────────────────────────────────────────┐
│          SBOM INGESTION & VULNERABILITY ANALYSIS                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────┐   │
│  │  SBOM Parsers   │  │  Package Mgmt    │  │  CVE Index   │   │
│  │  - CycloneDX    │  │  - npm registry  │  │  - NVD       │   │
│  │  - SPDX         │  │  - PyPI API      │  │  - OSV       │   │
│  │  - Package.json │  │  - Gemfile       │  │  - GHSA      │   │
│  └────────┬────────┘  └──────────┬───────┘  └──────┬───────┘   │
│           │                      │                 │            │
│           └──────────┬───────────┴─────────────────┘            │
│                      │                                           │
│           ┌──────────▼────────────────────────┐                │
│           │  Dependency Resolution Engine     │                │
│           │  - Transitive mapping             │                │
│           │  - Version constraint resolution  │                │
│           │  - Supply chain analysis          │                │
│           └──────────┬───────────────────────┘                │
│                      │                                          │
│           ┌──────────▼────────────────────────┐                │
│           │  Vulnerability Correlation       │                │
│           │  - CVE-package linking           │                │
│           │  - Risk scoring (CVSS/EPSS)      │                │
│           │  - Exploitability assessment     │                │
│           └──────────┬───────────────────────┘                │
│                      │                                          │
│           ┌──────────▼────────────────────────┐                │
│           │  Intelligence Integration         │                │
│           │  - APT threat correlation         │                │
│           │  - STIX indicator matching        │                │
│           │  - Supply chain threat analysis   │                │
│           └──────────┬───────────────────────┘                │
│                      │                                          │
│           ┌──────────▼────────────────────────┐                │
│           │  Reporting & Remediation          │                │
│           │  - Risk dashboards                │                │
│           │  - Remediation roadmaps           │                │
│           │  - Executive summaries            │                │
│           └──────────────────────────────────┘                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Data Model

#### SBOM Package Entity
```yaml
Package:
  id: "npm:react:18.2.0"
  name: "react"
  ecosystem: "npm"
  version: "18.2.0"
  resolved_from: "package.json|package-lock.json"

  dependencies:
    - name: "loose-envify"
      version: "^1.4.0"
      resolved: "1.4.0"
      transitive_depth: 1

  metadata:
    first_seen: "2025-11-20"
    license: "MIT"
    homepage: "https://react.dev"
    repository: "https://github.com/facebook/react"
    maintainers:
      - "facebook/react-team"

  vulnerability_context:
    has_advisories: false
    cve_count: 0
    deprecated: false
    superceded_by: null
```

#### CVE Correlation Entity
```yaml
CVEMapping:
  cve_id: "CVE-2021-43565"
  package_id: "npm:axios:0.21.1"
  cvss_score: 7.5
  cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"
  epss_score: 0.89
  exploit_maturity: "functional"

  vulnerability_details:
    title: "Axios SSRF via Redirect"
    description: "Axios version 0.21.1 allows SSRF attacks via URL redirect handling"
    discovered: "2021-10-15"
    public_date: "2021-10-20"

  remediation:
    recommended_version: "0.26.1"
    available_path: "available"
    breaking_changes: false

  intelligence_links:
    apt_campaigns: []
    threat_actors: []
    stix_indicators: ["attack-pattern--3731bda3-55e8-4a4e-8e38-bf01a35303ba"]
```

#### Supply Chain Analysis
```yaml
SupplyChainAnalysis:
  application_id: "aeon-dt-backend:1.0.0"
  analysis_date: "2025-11-25"

  direct_dependencies: 47
  transitive_dependencies: 312

  vulnerability_summary:
    critical: 2
    high: 8
    medium: 23
    low: 41
    info: 156

  risk_factors:
    abandoned_packages: 3
    typosquatting_risk: "low"
    supply_chain_compromises: 0

  recommendations:
    - priority: "critical"
      package: "express-session:1.17.2"
      issue: "Session fixation vulnerability"
      remediation: "Upgrade to 1.17.3 or later"
      effort_hours: 0.5
```

## SBOM Ingestion Workflow

### 1. Format Detection & Parsing

```
Input SBOM (any format)
    ↓
┌─────────────────────┐
│ Format Detection    │
│ - CycloneDX JSON    │
│ - SPDX RDF/JSON     │
│ - package.json      │
│ - requirements.txt  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Format-Specific     │
│ Parser Selection    │
└──────────┬──────────┘
           ↓
Normalized Package List
```

### 2. Dependency Resolution

**Process**:
1. Parse direct dependencies from SBOM
2. Resolve transitive dependencies via package manager APIs
3. Build dependency graph with version constraints
4. Identify conflicts and constraint violations
5. Generate supply chain attack surface map

**Outputs**:
- Flat dependency list with resolved versions
- Dependency tree with depth tracking
- Constraint violation report
- Supply chain risk assessment

### 3. CVE Correlation

**Data Sources**:
- NVD (National Vulnerability Database): 216K+ CVEs
- OSV (Open Source Vulnerabilities): 110K+ entries
- GHSA (GitHub Security Advisories): 45K+ advisories
- npm audit database: npm-specific vulnerabilities

**Correlation Process**:
1. For each package version, query CVE databases
2. Match package ecosystem and version constraints
3. Score vulnerability severity (CVSS 3.1 + EPSS)
4. Identify remediation paths (available updates)
5. Link to threat intelligence

**Risk Scoring Algorithm**:

```
Risk Score = (CVSS × 0.4) + (EPSS × 0.3) + (DepthFactor × 0.2) + (ExploitMaturity × 0.1)

Where:
  CVSS = 0-10 normalized severity
  EPSS = 0-1 exploit probability
  DepthFactor = (1 / transitive_depth) × urgency_factor
  ExploitMaturity = 0.2 (unproven) to 1.0 (weaponized)
```

## npm Package Analysis

### npm Registry Integration

```
Package Query Flow:
1. Registry lookup: https://registry.npmjs.org/{package-name}
2. Version resolution with semver constraints
3. Fetch package metadata (maintainers, deprecated status)
4. Retrieve tarball hash for integrity verification
5. Cross-reference with npm audit database
```

### Key Data Points

- **Package Metadata**: name, version, license, homepage, repository
- **Dependency Graph**: direct and transitive with version constraints
- **Maintenance Status**: deprecated packages, abandoned projects
- **Security Status**: npm audit findings, maintenance recommendations
- **Supply Chain Signals**: download trends, maintainer trustworthiness, typosquatting risk

### Example Analysis Output

```javascript
{
  "packageId": "npm:express:4.18.1",
  "name": "express",
  "version": "4.18.1",
  "ecosystem": "npm",
  "downloadsTrend": {
    "weekly": 18500000,
    "monthly": 75000000,
    "yearly": 900000000
  },
  "maintainers": [
    {
      "username": "dougwilson",
      "verified": true,
      "packages_count": 12
    }
  ],
  "dependencies": [
    {
      "name": "body-parser",
      "version": "1.20.0",
      "vulnerabilities": [
        {
          "advisoryId": "npm-123456",
          "severity": "high",
          "description": "Prototype pollution vulnerability",
          "remediatedIn": "1.20.1",
          "cvss": 7.5
        }
      ]
    }
  ],
  "vulnerabilityProfile": {
    "critical": 0,
    "high": 1,
    "medium": 0,
    "low": 0
  }
}
```

## PyPI Package Analysis

### Python Package Index Integration

```
Package Query Flow:
1. PyPI API: https://pypi.org/pypi/{package-name}/json
2. Version resolution with PEP 440 constraints
3. Fetch distribution metadata and dependencies
4. Cross-reference with advisory databases
5. Analyze packaging security (signed wheels, etc)
```

### Key Data Points

- **Package Metadata**: name, version, classifiers, project URLs
- **Dependency Resolution**: requires_dist with environment markers
- **Distribution Format**: wheels vs source distributions
- **Maintenance Status**: release frequency, Python version support
- **Security Integration**: vulnerability databases (Snyk, OSV, GHSA)

### Example Analysis Output

```json
{
  "packageId": "pypi:django:4.1.3",
  "name": "django",
  "version": "4.1.3",
  "ecosystem": "pypi",
  "pythonRequires": ">=3.8",
  "dependencies": [
    {
      "name": "sqlparse",
      "specifier": ">=0.2.2",
      "vulnerabilities": []
    },
    {
      "name": "tzdata",
      "specifier": "",
      "platformSpecific": "win32",
      "vulnerabilities": []
    }
  ],
  "classifiers": [
    "Development Status :: 5 - Production/Stable",
    "Framework :: Django :: 4.1",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python :: 3.8"
  ],
  "vulnerabilityHistory": [
    {
      "cveId": "CVE-2022-28346",
      "affectedVersions": ["<3.2.12", ">=4.0,<4.0.2"],
      "severity": "high",
      "description": "Potential SQL injection",
      "resolved": "4.0.3"
    }
  ]
}
```

## CVE Database Integration (316K Nodes)

### Data Sources Architecture

```
┌──────────────────────────────────────────────────────────┐
│            CVE AGGREGATION LAYER (316K+ CVEs)            │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ NVD Data     │  │ OSV Data     │  │ GHSA Data    │   │
│  │ (216K CVEs)  │  │ (110K OSVs)  │  │ (45K advisories)
│  │ - CVSS 3.1   │  │ - Ecosystem  │  │ - GH-specific│   │
│  │ - CWE refs   │  │ - Affected   │  │ - Patches    │   │
│  │ - Refs       │  │ - Versions   │  │ - PRs        │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘   │
│         │                 │                  │          │
│         └─────────────────┼──────────────────┘          │
│                           │                             │
│              ┌────────────▼──────────────┐              │
│              │ Deduplication & Linking   │              │
│              │ - Cross-source matching   │              │
│              │ - Version normalization   │              │
│              │ - Ecosystem translation   │              │
│              └────────────┬───────────────┘              │
│                           │                             │
│              ┌────────────▼──────────────┐              │
│              │ Unified CVE Index (316K)  │              │
│              │ - CVE ID (unique key)     │              │
│              │ - Multi-source refs       │              │
│              │ - Severity aggregation    │              │
│              │ - Remediation paths       │              │
│              └─────────────────────────────              │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### EPSS (Exploit Prediction Scoring System)

EPSS provides probability of exploitation within 30 days:

```yaml
EpssScore:
  cveId: "CVE-2021-43565"
  epssPercentile: 89
  epssScore: 0.89
  interpretation: "89% of similar vulnerabilities are exploited"

  riskInterpretation:
    score_0_5: "Lower priority - minimal real-world exploitation"
    score_50_75: "Moderate priority - some exploitation observed"
    score_75_95: "High priority - active exploitation likely"
    score_95_100: "Critical priority - widespread exploitation"
```

### Real-Time CVE Updates

```
Daily Update Cycle:
  06:00 UTC: NVD feed processing (100-200 new entries/day)
  08:00 UTC: OSV data synchronization
  10:00 UTC: GHSA advisory ingestion
  12:00 UTC: EPSS score updates
  18:00 UTC: npm audit database refresh
  20:00 UTC: PyPI advisory refresh
```

## Intelligence Integration

### APT Campaign Correlation

```
SBOM Vulnerability → CVE → Threat Intelligence
    ↓
┌─────────────────────────────────────────┐
│ Check APT Usage History                 │
│ - Which threat groups exploit?           │
│ - Campaign timeline                     │
│ - Affected sectors                      │
└─────────────┬───────────────────────────┘
              ↓
Risk Assessment:
  - Is package used in critical infrastructure?
  - Are exploitation tools publicly available?
  - Are active campaigns using this CVE?
  - What is defensive status?
```

### STIX Indicator Mapping

```yaml
CveToStixMapping:
  cveId: "CVE-2021-43565"

  stixIndicators:
    - type: "attack-pattern"
      id: "attack-pattern--3731bda3-55e8-4a4e-8e38-bf01a35303ba"
      name: "Server-Side Request Forgery (SSRF)"

    - type: "malware"
      id: "malware--1c63a24d-c8eb-4275-81b2-dcd4d7d4f6db"
      name: "Exploit kit using CVE-2021-43565"

  threatActorCampaigns:
    - name: "Operation Stealth"
      firstObserved: "2021-11-05"
      targetSectors: ["finance", "technology"]
```

## Remediation Pathways

### Risk-Based Remediation Prioritization

```
Algorithm:
1. Calculate risk score for each vulnerability
2. Identify available remediation (update, patch, workaround)
3. Assess remediation difficulty (breaking changes, incompatibilities)
4. Prioritize by: risk × feasibility × impact

Priority Matrix:
                    High Risk    Medium Risk   Low Risk
Easy Fix            CRITICAL     HIGH          MEDIUM
Moderate Effort     HIGH          MEDIUM       LOW
Difficult (breaking) MEDIUM      LOW           INFO
```

### Remediation Tracking

```yaml
RemediationAction:
  id: "rem-2025-11-25-001"
  vulnerability:
    cveId: "CVE-2021-43565"
    package: "axios"
    version: "0.21.1"

  status: "scheduled"
  priority: "critical"

  remediation:
    type: "version_update"
    currentVersion: "0.21.1"
    targetVersion: "0.26.1"

    risk_assessment:
      breaking_changes: false
      dependent_packages: 5
      test_coverage: 87%

  timeline:
    scheduled_date: "2025-11-28"
    estimated_hours: 2
    verification_required: true
    rollback_plan: "Tested and documented"
```

## Reporting & Dashboards

### Executive Risk Summary

```
SBOM Security Dashboard
========================

Application: aeon-dt-backend v1.0.0
Analysis Date: 2025-11-25
Total Dependencies: 359 (47 direct, 312 transitive)

VULNERABILITY SUMMARY
─────────────────────
Critical:   2  [immediate action required]
High:       8  [address within 7 days]
Medium:    23  [address within 30 days]
Low:       41  [address within 90 days]
Info:     156  [monitoring]

RISK SCORE: 7.2 / 10 [HIGH]

TOP CRITICAL ISSUES
───────────────────
1. express-session:1.17.2 - Session Fixation (CVE-2021-43565)
   Remediation: Upgrade to 1.17.3 (no breaking changes)

2. lodash:4.17.20 - Prototype Pollution (CVE-2021-23337)
   Remediation: Upgrade to 4.17.21 (compatible)

REMEDIATION ROADMAP
──────────────────
Week 1: Critical patches (2 vulnerabilities, 4 hours)
Week 2: High severity (8 vulnerabilities, 12 hours)
Week 3: Medium severity (23 vulnerabilities, 24 hours)
Week 4: Quality improvements (41 low severity, 16 hours)

SUPPLY CHAIN STATUS
───────────────────
Abandoned Packages:    3 (recommend replacement)
Typosquatting Risk:    LOW
Compromised Packages:  0
Last Updated:          2025-11-25T14:45:00Z
```

## Getting Started

### Prerequisites
- SBOM file (CycloneDX JSON, SPDX, or package manager native format)
- CVE database access (public, requires internet connectivity)
- Python 3.9+ or Node.js 16+

### Quick Start

```bash
# 1. Generate SBOM from your project
npm sbom > sbom.json          # npm
pip-audit --desc > sbom.json  # pip
cyclonedx-py -o sbom.json    # Python projects

# 2. Run analysis
python sbom_analyzer.py sbom.json --output report.json

# 3. Review results
cat report.json | jq '.vulnerability_summary'
```

### Integration Points

- **CI/CD**: Automated SBOM generation and analysis on each build
- **Dependency Management**: Real-time advisory integration
- **Incident Response**: CVE detection and alerting
- **Compliance**: Software composition audit trails
- **Threat Intelligence**: APT campaign and supply chain risk correlation

## Files in This Enhancement

| File | Purpose | Lines |
|------|---------|-------|
| README.md | Overview and architecture | 450+ |
| TASKMASTER_SBOM_v1.0.md | 10-agent swarm coordination | 380+ |
| blotter.md | Progress tracking and status | 200+ |
| PREREQUISITES.md | Dependencies and data sources | 250+ |
| DATA_SOURCES.md | APA citations and references | 150+ |

**Total Target**: 1,500+ lines of documentation and specifications

## Next Steps

1. Review PREREQUISITES.md for data requirements
2. Study TASKMASTER_SBOM_v1.0.md for implementation approach
3. Track progress in blotter.md
4. Reference DATA_SOURCES.md for technical citations

---

**Status**: ACTIVE | **Version**: v1.0.0 | **Last Update**: 2025-11-25 14:45:00 UTC
