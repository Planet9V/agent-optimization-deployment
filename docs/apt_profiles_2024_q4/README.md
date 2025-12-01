# APT Threat Intelligence Report Collection - Q4 2024

**Research Period:** September 2024 - November 2024
**Report Date:** 2024-11-28
**Classification:** TLP:CLEAR
**Format:** NCC-OTCE-EAB (Modeled after 3_EAB_40 format)

---

## Overview

This directory contains comprehensive threat intelligence profiles for 11 major APT campaigns identified during Q4 2024 (September-November), with particular focus on critical infrastructure targeting including telecommunications, energy, water systems, and healthcare sectors.

**Total Documents:** 12 (11 individual profiles + 1 comprehensive summary)
**Total Size:** ~116 KB
**Format:** Markdown (.md) for Neo4j ingestion compatibility
**Status:** Ready for E01 ingestion pipeline

---

## Document Index

### Summary Report
| Document ID | Title | Description | Size |
|-------------|-------|-------------|------|
| NCC-OTCE-EAB-000 | Q4 2024 APT Activity Summary Report | Comprehensive analysis of all 11 campaigns with strategic recommendations | 24 KB |

### Nation-State Threat Actors

#### People's Republic of China (PRC)
| Document ID | Threat Actor | Campaign Focus | Size |
|-------------|--------------|----------------|------|
| NCC-OTCE-EAB-020 | Salt Typhoon | Telecommunications espionage, U.S. telecom providers | 13 KB |
| NCC-OTCE-EAB-021 | Volt Typhoon | Critical infrastructure pre-positioning, 5-year dwell time | 15 KB |
| NCC-OTCE-EAB-027 | Mustang Panda | ASEAN government targeting, diplomatic espionage | 2.1 KB |

#### Russian Federation
| Document ID | Threat Actor | Campaign Focus | Size |
|-------------|--------------|----------------|------|
| NCC-OTCE-EAB-023 | Sandworm (APT44) | ZEROLOT wiper, Ukrainian energy/grain sectors | 7.7 KB |
| NCC-OTCE-EAB-026 | APT29 (Midnight Blizzard) | RDP-based spear-phishing, government targeting | 3.0 KB |

#### Islamic Republic of Iran
| Document ID | Threat Actor | Campaign Focus | Size |
|-------------|--------------|----------------|------|
| NCC-OTCE-EAB-022 | CyberAv3ngers (IRGC-CEC) | IOCONTROL malware, water/wastewater systems | 14 KB |

#### Democratic People's Republic of Korea (DPRK)
| Document ID | Threat Actor | Campaign Focus | Size |
|-------------|--------------|----------------|------|
| NCC-OTCE-EAB-024 | Lazarus Group | DEV#POPPER campaign, cryptocurrency theft | 4.1 KB |
| NCC-OTCE-EAB-025 | Kimsuky (RGB) | DMARC exploitation, government espionage | 6.6 KB |

### Ransomware and Financial Crime

| Document ID | Threat Actor | Campaign Focus | Size |
|-------------|--------------|----------------|------|
| NCC-OTCE-EAB-028 | Qilin Ransomware | Healthcare targeting, Synnovis attack | 4.0 KB |
| NCC-OTCE-EAB-029 | Akira Ransomware | Manufacturing/education, $244M in ransoms | 2.2 KB |
| NCC-OTCE-EAB-030 | FIN7 | Financial sector, EDR bypass, 4000+ shell domains | 2.9 KB |

---

## Key Statistics

### Threat Landscape
- **Nation-State Actors:** 4 (China, Russia, Iran, North Korea)
- **APT Groups Documented:** 9
- **Ransomware Families:** 3 major operations
- **Financial Impact:** $300+ million in ransoms paid
- **Campaign Duration:** Most ongoing with multi-year persistent access

### Critical Infrastructure Impact
- **Telecommunications:** 56% of observed campaigns
- **Energy:** Pre-positioning and active destruction
- **Water Systems:** Direct cyber-physical attacks
- **Healthcare:** 15+ incidents, patient care disruption

### Technical Indicators
- **CVEs Exploited:** 10+ critical vulnerabilities
- **Custom Malware:** 12+ families documented
- **MITRE ATT&CK Techniques:** 40+ unique techniques
- **Dwell Time:** Up to 5+ years (Volt Typhoon)

---

## Document Structure

Each APT profile follows the NCC-OTCE-EAB format with the following sections:

1. **Executive Summary**
   - Threat level assessment
   - Primary motivation
   - Attribution
   - Key findings

2. **Threat Actor Profile**
   - Nation-state sponsor
   - Target sectors
   - Geographic focus
   - Historical context

3. **Campaign Analysis**
   - Timeline and activity
   - High-profile incidents
   - Victim organizations

4. **Tactics, Techniques, and Procedures (TTPs)**
   - Initial access methods
   - Persistence mechanisms
   - Lateral movement
   - Impact techniques

5. **Malware & Tools**
   - Custom malware analysis
   - Exploited vulnerabilities
   - Attack tools

6. **Indicators of Compromise (IoCs)**
   - Network indicators
   - File indicators
   - Behavioral indicators

7. **MITRE ATT&CK Mapping**
   - Comprehensive technique mapping
   - Tactic coverage analysis

8. **Detection Strategies**
   - Network-based detection
   - Host-based detection
   - Behavioral analytics

9. **Mitigation Recommendations**
   - Immediate actions
   - Strategic mitigations
   - Long-term initiatives

10. **Hunting Guidance**
    - Hunt hypotheses
    - Investigation procedures

11. **Intelligence Gaps**
    - Unknown elements
    - Research priorities

12. **References**
    - Source citations
    - Vendor reports
    - Government advisories

---

## Neo4j Ingestion Readiness

### Format Compatibility
- **File Format:** Markdown (.md)
- **Structure:** Consistent headings for parsing
- **MITRE ATT&CK:** Standardized technique IDs
- **IoCs:** Structured presentation
- **References:** Complete source attribution

### Entity Extraction Ready
The documents are structured for easy extraction of:
- Threat actor entities
- Campaign entities
- Malware families
- CVE identifiers
- MITRE ATT&CK techniques
- Target sectors
- IoC patterns
- Relationship mappings

### Suggested Neo4j Node Types
```cypher
(:ThreatActor)-[:CONDUCTED]->(:Campaign)
(:Campaign)-[:USES]->(:Malware)
(:Campaign)-[:EXPLOITS]->(:Vulnerability)
(:Campaign)-[:EMPLOYS]->(:Technique)
(:Campaign)-[:TARGETS]->(:Sector)
(:Technique)-[:MAPS_TO]->(:MITREAttack)
(:Campaign)-[:HAS_IOC]->(:Indicator)
```

---

## Usage Recommendations

### For Threat Intelligence Teams
1. Review summary report (EAB-000) for landscape overview
2. Deep-dive into sector-relevant profiles
3. Cross-reference IoCs with security monitoring
4. Implement detection strategies
5. Update threat models

### For Security Operations Centers (SOC)
1. Import IoCs into SIEM/threat intelligence platforms
2. Deploy detection rules from profiles
3. Execute hunt hypotheses
4. Monitor for campaign indicators
5. Coordinate incident response

### For Risk Management
1. Assess sector-specific threat exposure
2. Prioritize mitigation investments
3. Update business continuity plans
4. Brief executive leadership
5. Engage with sector ISACs

### For Incident Response
1. Use profiles for attribution analysis
2. Reference TTPs for investigation
3. Apply hunting guidance
4. Leverage mitigation recommendations
5. Document lessons learned

---

## E01 Ingestion Pipeline Integration

### Pre-Processing
```bash
# Verify all markdown files present
ls -1 NCC-OTCE-EAB-*.md | wc -l  # Should return 12

# Check for parsing compatibility
for file in NCC-OTCE-EAB-*.md; do
    echo "Validating: $file"
    # Add your validation logic here
done
```

### Entity Extraction
Recommended extraction patterns:
- **Threat Actors:** Lines matching "**Also Known As:**"
- **Techniques:** MITRE ATT&CK tables with "T####" patterns
- **CVEs:** Lines matching "CVE-####-#####"
- **IoCs:** Sections titled "## INDICATORS OF COMPROMISE"
- **Sectors:** "### Target Sectors" sections

### Relationship Mapping
Key relationships to extract:
- Threat Actor → Campaign
- Campaign → Malware
- Campaign → Technique (MITRE ATT&CK)
- Campaign → Vulnerability (CVE)
- Campaign → Sector
- Technique → MITRE ATT&CK Framework

---

## Update History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-11-28 | Initial release - 11 APT profiles + summary | NCC OTCE Research Team |

---

## Contact Information

**Research Team:** NCC OTCE (Operational Technology Cyber Excellence)
**Email:** otce-research@ncc.example.com
**Distribution:** TLP:CLEAR - May be distributed without restriction
**Next Review:** 2025-02-28 (Quarterly update cycle)

---

## Source Attribution

All research based on open-source intelligence from:
- Government agencies (CISA, FBI, NSA, DoD, HHS)
- Threat intelligence vendors (Microsoft, Palo Alto, ESET, Mandiant, CrowdStrike)
- Cybersecurity research organizations
- Industry sector ISACs (WaterISAC, etc.)

Complete source citations provided in individual profile documents.

---

## License and Usage

**Classification:** TLP:CLEAR
**Distribution:** Unlimited
**Usage:** Authorized for threat intelligence, security research, and defensive cybersecurity purposes
**Attribution:** Please cite as "NCC OTCE Q4 2024 APT Threat Intelligence Report Collection"

---

**END OF README**
**Last Updated:** 2024-11-28
**Document Version:** 1.0
