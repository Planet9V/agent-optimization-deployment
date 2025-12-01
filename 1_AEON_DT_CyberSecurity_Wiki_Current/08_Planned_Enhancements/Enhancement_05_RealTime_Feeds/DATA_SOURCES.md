# DATA_SOURCES.md - Real-Time Threat Feed Sources with APA Citations

**Document**: Threat Intelligence Data Sources Bibliography
**Version**: 1.0.0
**Created**: 2025-11-25
**Last Updated**: 2025-11-25
**Citation Style**: APA 7th Edition

## 1. VulnCheck API - Zero-Day Intelligence

### Overview
VulnCheck is a commercial vulnerability intelligence platform specializing in emerging and zero-day vulnerabilities, exploit intelligence, and threat landscape analysis.

### APA Citation
VulnCheck Inc. (2025). VulnCheck API v3 documentation. Retrieved from https://vulncheck.com/api

### Access Information
- **API Endpoint**: https://api.vulncheck.com/v3/
- **Authentication**: Bearer token (API key)
- **Data Format**: JSON
- **Rate Limits**: 300 req/min (standard), 1,000+ req/min (enterprise)
- **Update Frequency**: Real-time (webhooks available)
- **Cost**: Freemium and commercial tiers

### Data Coverage
- Emerging vulnerabilities (not yet in NVD)
- Exploit intelligence and proof-of-concept code detection
- Threat actor IOCs and infrastructure
- Zero-day vulnerability tracking
- Dark web and underground forum monitoring
- Supply chain vulnerability intelligence

### Available Endpoints
1. `/vulnerabilities` - Comprehensive vulnerability listings
2. `/vulnerabilities/{cveId}` - Detailed CVE information
3. `/vulnerabilities/{cveId}/exploit` - Exploit code intelligence
4. `/threat-intel` - Zero-day threat intelligence
5. `/indicators` - IOC feeds and infrastructure intelligence
6. `/breaches` - Data breach intelligence
7. `/webhooks` - Real-time event subscriptions

### Key Data Fields
```json
{
  "cveId": "CVE-2025-00001",
  "title": "Vulnerability Title",
  "description": "Detailed vulnerability description",
  "cvssScore": 9.8,
  "cvssVersion": "3.1",
  "severity": "CRITICAL",
  "publishedDate": "2025-01-15T00:00:00Z",
  "exploitAvailable": true,
  "exploitDate": "2025-01-16T12:34:56Z",
  "exploitCode": "public",
  "affectedSoftware": [
    {"vendor": "Company", "product": "Product", "version": "1.0"}
  ],
  "references": ["https://..."],
  "threat_intel": {
    "actor": "APT-28",
    "campaign": "Campaign Name",
    "infrastructure": ["10.0.0.1", "domain.com"]
  }
}
```

### Integration Notes
- Webhook receivers recommended for real-time updates
- Batch polling available for incremental updates
- Requires persistent API key management
- Support available via https://vulncheck.com/contact

---

## 2. National Vulnerability Database (NVD) - CVE Repository

### Overview
The National Vulnerability Database is a U.S. government repository of vulnerability information maintained by the National Institute of Standards and Technology (NIST). It is the authoritative source for CVE (Common Vulnerabilities and Exposures) data.

### APA Citation
National Institute of Standards and Technology. (2025). National Vulnerability Database. U.S. Department of Commerce. Retrieved from https://nvd.nist.gov/

### Secondary Citation (API)
National Institute of Standards and Technology. (2025). NVD API 2.0 specification. Retrieved from https://nvd.nist.gov/developers/

### Access Information
- **API Endpoint**: https://services.nvd.nist.gov/rest/json/cves/2.0
- **Authentication**: Optional API key (recommended for higher rate limits)
- **Data Format**: JSON (CVSS v3.1 standard)
- **Rate Limits**: 5 req/30s (public), 30 req/30s (with API key)
- **Update Frequency**: Daily automated feeds
- **Cost**: Free

### Data Coverage
- 240,000+ CVEs (1999-present)
- CVSS v2.0 and v3.x scoring
- CWE mappings (Common Weakness Enumeration)
- CPE references (product identification)
- Affected software and versions
- Published and modified dates
- References and remediation information

### Available Endpoints
1. `/cves` - CVE list with filtering and pagination
2. Query Parameters:
   - `lastModStartDate` / `lastModEndDate` - Modified date range
   - `pubStartDate` / `pubEndDate` - Publication date range
   - `cpeName` - Specific product filtering
   - `cveId` - Specific CVE lookup
   - `resultsPerPage` (max 2,000)

### Key Data Fields
```json
{
  "vulnerabilities": [
    {
      "cve": {
        "id": "CVE-2025-00001",
        "descriptions": [
          {"lang": "en", "value": "Vulnerability description"}
        ],
        "published": "2025-01-15T00:00:00Z",
        "lastModified": "2025-01-20T12:34:56Z",
        "references": [
          {"url": "https://...", "source": "vendor"}
        ]
      },
      "metrics": {
        "cvssV31": {
          "source": "nvd@nist.gov",
          "cvssData": {
            "version": "3.1",
            "baseScore": 9.8,
            "baseSeverity": "CRITICAL",
            "vectorString": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
          }
        }
      }
    }
  ]
}
```

### Integration Notes
- Official government source (high reliability)
- Large dataset (500-1,000+ new CVEs daily)
- Use `lastModStartDate` for incremental updates
- Synchronization recommended daily (after midnight UTC)
- API key obtained via https://nvd.nist.gov/developers/

---

## 3. MITRE ATT&CK Framework - Adversary Tactics & Techniques

### Overview
The MITRE ATT&CK Framework is a globally accessible knowledge base of adversary tactics and techniques based on real-world observations. It provides a structured taxonomy for threat analysis and security control design.

### APA Citation
MITRE ATT&CK®. (2025). Enterprise ATT&CK matrix. Retrieved from https://attack.mitre.org/

### Secondary Citation (Data Source)
MITRE ATT&CK. (2025). ATT&CK STIX data. Retrieved from https://github.com/mitre-attack/attack-stix-data

### Access Information
- **Data Source**: GitHub repository with STIX 2.1 JSON files
- **Format**: STIX 2.1 bundles (JSON)
- **Update Frequency**: Quarterly major releases, monthly patches
- **Cost**: Free (open source)
- **License**: CC Attribution 4.0 International

### Data Coverage
- 200+ Techniques (adversary actions)
- 13 Tactics (attack phases)
- 130+ Threat Groups (intrusion sets)
- 900+ Software (tools and malware)
- 100+ Campaigns (coordinated activities)
- 500+ Relationships and patterns

### Available STIX Objects

1. **attack-pattern** (Techniques)
   - ATT&CK ID (e.g., T1234)
   - Name and description
   - Platforms (Windows, macOS, Linux, etc.)
   - Data sources for detection
   - Mitigations and defenses

2. **x-mitre-tactic** (Tactics)
   - Tactic ID (e.g., TA1001)
   - Name (reconnaissance, initial access, execution, etc.)
   - Shortname
   - Techniques within tactic

3. **intrusion-set** (Threat Groups)
   - Group ID
   - Name and aliases
   - Description
   - First and last seen
   - Techniques and campaigns used

4. **malware** (Malware Families)
   - Malware family ID
   - Name and aliases
   - Description
   - Platforms
   - Techniques

5. **tool** (Attack Tools)
   - Tool ID
   - Name and aliases
   - Description
   - Platforms
   - Techniques

### Key Data Fields
```json
{
  "type": "attack-pattern",
  "id": "attack-pattern--01a5a209-b94c-450b-b7f9-946ce4bffb93",
  "created": "2016-02-17T16:46:23.000Z",
  "modified": "2024-10-15T00:00:00.000Z",
  "name": "Technique Name",
  "description": "Description of the technique",
  "kill_chain_phases": [
    {"kill_chain_name": "mitre-attack", "phase_name": "execution"}
  ],
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "T1234"
    }
  ],
  "x_mitre_platforms": ["Windows", "macOS", "Linux"],
  "x_mitre_data_sources": ["Process creation", "Command execution"],
  "x_mitre_contributors": ["MITRE ATT&CK"]
}
```

### Integration Notes
- Download full framework quarterly
- Use STIX 2.1 parser for structure
- Map CVEs to techniques for correlation
- Track group activities via technique usage
- Community contributions available

---

## 4. CISA KEV - Known Exploited Vulnerabilities Catalog

### Overview
The Cybersecurity and Infrastructure Security Agency (CISA) maintains the Catalog of Known Exploited Vulnerabilities, a curated list of vulnerabilities that are actively exploited by threat actors and pose significant risk to organizations.

### APA Citation
Cybersecurity and Infrastructure Security Agency. (2025). Known exploited vulnerabilities catalog. U.S. Department of Homeland Security. Retrieved from https://www.cisa.gov/known-exploited-vulnerabilities-catalog

### Access Information
- **Format**: CSV (comma-separated values)
- **Download URL**: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv
- **Update Frequency**: Weekly (Thursdays)
- **Data Size**: ~500 KB (1,000+ entries)
- **Cost**: Free

### Data Coverage
- Actively exploited vulnerabilities
- Exploitation timeline (date added to catalog)
- Vendor and product information
- Required action recommendations
- Remediation deadline (due date)
- Ransomware campaign usage tracking
- SSVC scoring (Stakeholder-Specific Vulnerability Scoring)

### CSV Fields
```
cveID:
  Description: CVE identifier
  Format: CVE-YYYY-NNNNN
  Example: CVE-2021-44228

vendor:
  Description: Affected software vendor
  Example: Apache

product:
  Description: Affected software product
  Example: Log4j

vulnerabilityName:
  Description: Descriptive name
  Example: Apache Log4j2 Remote Code Execution

dateAdded:
  Description: Date added to KEV catalog
  Format: YYYY-MM-DD
  Example: 2021-12-10

shortDescription:
  Description: Brief vulnerability summary
  Example: Remote code execution in Log4j JNDI feature

requiredAction:
  Description: Recommended action level
  Values: Patch, Apply Temporary Fix, Disable Feature, etc.

dueDate:
  Description: CISA remediation deadline
  Format: YYYY-MM-DD
  Example: 2022-01-10

notes:
  Description: Additional context
  Example: Exploitation observed in the wild

knownRansomwareCampaignUse:
  Description: Used in ransomware campaigns
  Values: Yes, No, Unknown
```

### Key Statistics
- 1,000+ actively exploited vulnerabilities tracked
- Average dwell time from discovery to exploitation: 3-6 months
- Weekly 15-30 new entries added
- Ransomware usage tracked in 20%+ of entries

### Integration Notes
- Parse CSV weekly (Thursday scheduled task)
- Implement differential tracking (new vs. previous)
- Cross-correlate with NVD for enrichment
- Flag vulnerabilities in organization inventory
- Generate remediation alerts with CISA due dates

---

## 5. STIX 2.1 and TAXII 2.1 Protocol

### Overview
STIX (Structured Threat Information Expression) is a standardized format for threat intelligence information exchange. TAXII (Trusted Automated Exchange of Indicator Information) is the protocol for distributing STIX content.

### APA Citations

**STIX 2.1 Specification**:
OASIS. (2021). Structured Threat Information Expression (STIX) Version 2.1. OASIS Committee Specification 02. Retrieved from https://docs.oasis-open.org/cti/stix/v2.1/os/

**TAXII 2.1 Specification**:
OASIS. (2021). Trusted Automated Exchange of Indicator Information (TAXII) Version 2.1. OASIS Committee Specification 02. Retrieved from https://docs.oasis-open.org/cti/taxii/v2.1/os/

### Access Information
- **Format**: JSON (STIX 2.1)
- **Transport**: HTTPS REST API (TAXII 2.1)
- **Authentication**: OAuth 2.0, API keys, or basic auth (varies by provider)
- **Data Format**: STIX bundles containing objects
- **Cost**: Free to commercial (provider-dependent)

### STIX Object Types
1. **indicator** - Observable characteristics of malicious activity
2. **malware** - Category of tools designed to infiltrate or damage systems
3. **attack-pattern** - Behavior or method of attack
4. **campaign** - Grouping of activities
5. **threat-actor** - Individuals or groups threatening assets
6. **identity** - Individuals or organizations
7. **location** - Geographical location
8. **vulnerability** - Weakness in system design
9. **infrastructure** - Servers, networks, domains
10. **relationship** - Connections between objects

### Key Data Fields
```json
{
  "type": "indicator",
  "id": "indicator--36ffb872-1504-44fb-887d-dfc72b7ae3b5",
  "created": "2025-01-15T00:00:00.000Z",
  "modified": "2025-01-15T00:00:00.000Z",
  "name": "Malicious IP Address",
  "description": "IP address observed in command and control activity",
  "pattern": "[ipv4-addr:value = '192.0.2.1']",
  "pattern_type": "stix",
  "valid_from": "2025-01-15T00:00:00.000Z",
  "labels": ["malicious-activity"],
  "tlp:tlp_level": "tlp:clear",
  "confidence": 95
}
```

### TAXII 2.1 API Endpoints
- `/api/root/` - API root discovery
- `/api/root/collections/` - Collection listing
- `/api/root/collections/{collection_id}/objects/` - Object retrieval
- Supports filtering: `type`, `added_after`, `match[pattern]`

### Common TAXII Providers
1. **Anomali Limo** (Free)
   - URL: https://cti-taxii.mitre.org
   - Collections: MITRE ATT&CK data
   - Authentication: Basic (guest/guest)

2. **CISA TAXII Servers**
   - URL: taxii.cisa.dhs.gov (varies by service)
   - Collections: Government threat intel
   - Authentication: Varies

3. **Commercial Providers**
   - Recorded Future
   - Mandiant (Google Cloud)
   - ThreatStream
   - Others

### Integration Notes
- Use STIX2 Python library for parsing
- Support incremental collection via `added_after`
- Handle TLP (Traffic Light Protocol) restrictions
- Validate confidence levels for correlation
- Subscribe to collections matching organizational needs

---

## 6. Supplementary Intelligence Sources

### Threat Intelligence RSS Feeds

**Krebs on Security**
- URL: https://krebsonsecurity.com/feed/
- Focus: Breaking security news, threat analysis
- Frequency: Daily updates
- Citation: Krebs, B. (2025). Krebs on Security. Retrieved from https://krebsonsecurity.com/

**Bleeping Computer**
- URL: https://www.bleepingcomputer.com/feed/
- Focus: Vulnerability news, ransomware coverage
- Frequency: Multiple updates daily
- Citation: Lawrence, D. (2025). Bleeping Computer. Retrieved from https://www.bleepingcomputer.com/

**SecurityWeek**
- URL: https://www.securityweek.com/feed/
- Focus: Enterprise security news
- Frequency: Daily
- Citation: SecurityWeek. (2025). Retrieved from https://www.securityweek.com/

### Industry-Specific Sources

**Government Advisories (US)**
- CISA Alerts: https://www.cisa.gov/news-events
- NSA Cybersecurity Advisories: https://www.nsa.gov/Press_Room/Press_Releases/

**EU Cybersecurity**
- ENISA Threat Landscape: https://www.enisa.europa.eu/

### Academic & Research

**CVE Details**
- URL: https://www.cvedetails.com/
- Data: Vulnerability statistics, top vulnerabilities
- Citation: Christey-Moore, S. (2025). CVE Details. Retrieved from https://www.cvedetails.com/

---

## 7. Data Quality & Reliability Assessment

### Source Reliability Ranking

| Rank | Source | Reliability | Coverage | Timeliness |
|------|--------|-------------|----------|-----------|
| 1 | NVD | 99%+ | Comprehensive | Daily |
| 1 | CISA KEV | 99%+ | Focused (exploited) | Weekly |
| 2 | VulnCheck | 95%+ | Emerging threats | Real-time |
| 2 | MITRE ATT&CK | 95%+ | Techniques/Groups | Quarterly |
| 2 | STIX/TAXII | 90%+ | Variable by provider | Provider-dependent |
| 3 | News Sources | 80%+ | General interest | Daily/Real-time |

### Confidence Scoring Guidelines

**Tier 1 (High Confidence - 0.9-1.0)**
- Government sources (NVD, CISA)
- Multiple independent confirmations
- Verified exploit code
- Active exploitation confirmed

**Tier 2 (Medium-High Confidence - 0.7-0.9)**
- Reputable security vendors
- MITRE ATT&CK backed
- Single independent source
- Technical analysis supporting

**Tier 3 (Medium Confidence - 0.5-0.7)**
- Security research blogs
- Some corroboration
- Unverified claims
- Limited technical details

**Tier 4 (Low Confidence - <0.5)**
- Rumor or speculation
- Unsourced claims
- Conflicting information
- Preliminary reports

---

## 8. Data Usage & Attribution Requirements

### Creative Commons Licensing

**CISA KEV & Government Sources**
- License: Public Domain (CC0)
- Attribution: Required for CISA logo
- Usage: Unrestricted for non-commercial and commercial

**MITRE ATT&CK**
- License: CC BY 4.0
- Attribution: Required
- Citation Format: See above citations

**NVD**
- License: Public Domain
- Attribution: Recommended
- Usage: Unrestricted

### Proper Attribution Examples

**VulnCheck Usage**:
```
Data sourced from VulnCheck (https://vulncheck.com/)
API v3, accessed [DATE]
```

**NVD Usage**:
```
Data sourced from National Vulnerability Database (NVD),
National Institute of Standards and Technology (NIST),
U.S. Department of Commerce, https://nvd.nist.gov/
```

**MITRE ATT&CK Usage**:
```
MITRE ATT&CK® is a registered trademark of The MITRE Corporation.
Data accessed from https://attack.mitre.org/
Licensed under CC Attribution 4.0 International.
```

---

## 9. Data Privacy & Security Compliance

### GDPR Considerations
- NVD/CISA: No PII, no GDPR concerns
- VulnCheck: May include company information - check terms
- News sources: May reference individuals - anonymization required
- STIX feeds: Verify provider privacy policy

### Data Retention Policies
- Real-time feeds: Archive for 7 days minimum
- Processed records: Retain for 90 days minimum
- Audit logs: Retain for 1 year
- Sensitive intelligence: Destroy per security policy

### Responsible Disclosure
- Do not republish 0-days without vendor agreement
- Respect embargo periods on vulnerability information
- Credit security researchers appropriately
- Follow coordinated disclosure timelines

---

## 10. Integration Timeline & Roadmap

### Phase 1: Foundation (Week 1-2)
- Implement NVD and CISA KEV (free sources)
- Establish database schema
- Create basic ingestion pipeline

### Phase 2: Commercial Intelligence (Week 3)
- Integrate VulnCheck API
- Implement webhook receivers
- Real-time update processing

### Phase 3: Framework Integration (Week 4)
- Incorporate MITRE ATT&CK
- Build technique-to-vulnerability mapping
- Group activity correlation

### Phase 4: Advanced Sources (Week 5+)
- STIX/TAXII provider integration
- Custom feed development
- Advanced analytics and ML

---

## References & Further Reading

### Official Documentation
- [NIST CVE Program](https://www.nist.gov/programs/cve-program)
- [CISA Cybersecurity](https://www.cisa.gov/cybersecurity)
- [MITRE ATT&CK](https://attack.mitre.org)
- [OASIS STIX/TAXII](https://oasis-open.github.io/cti-documentation/)

### Standards & Frameworks
- CVSS v3.1 Scoring: https://www.first.org/cvss/v3.1/
- CWE (Common Weakness Enumeration): https://cwe.mitre.org/
- CPE (Common Platform Enumeration): https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-188.pdf

---

**Document Status**: Complete
**Last Reviewed**: 2025-11-25
**Next Review**: 2025-12-25
**Approval**: Ready for Implementation
