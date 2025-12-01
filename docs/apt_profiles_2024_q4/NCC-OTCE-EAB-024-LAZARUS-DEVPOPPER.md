# NCC-OTCE-EAB-024: Lazarus Group DEV#POPPER Campaign

**Document Classification:** TLP:CLEAR
**Report ID:** NCC-OTCE-EAB-024
**Date:** 2024-11-28
**Version:** 1.0
**Campaign Period:** 2023-2024 (Ongoing)

---

## EXECUTIVE SUMMARY

Lazarus Group's DEV#POPPER campaign represents a sophisticated social engineering operation targeting cryptocurrency developers and technology professionals. The campaign combines advanced social engineering with malicious GitHub repositories to compromise targets in the blockchain, cybersecurity, and online gambling sectors.

**Threat Level:** HIGH
**Primary Motivation:** Financial Gain / Cryptocurrency Theft
**Attribution:** Democratic People's Republic of Korea (DPRK)
**Also Known As:** Hidden Cobra, TEMP.Hermit, Famous Chollima, Gwisin Gang, Tenacious Pungsan, UNC5342, Void Dokkaebi

---

## THREAT ACTOR PROFILE

### Attribution
- **Nation-State:** North Korea (DPRK)
- **Active Since:** At least 2009
- **2024 Financial Impact:** $659 million in cryptocurrency heists

### Target Profile
- Blockchain developers
- Cryptocurrency platform engineers
- Cybersecurity professionals
- Online gambling developers
- DeFi platform developers

---

## TACTICS, TECHNIQUES, AND PROCEDURES (TTPs)

### Social Engineering (T1598)
1. **Recruiter Impersonation**
   - Posing as tech recruiters on LinkedIn
   - Offering lucrative job opportunities
   - Building rapport over weeks

2. **Platform Migration**
   - Initial contact via GitHub, LinkedIn
   - Migration to WhatsApp for private conversations
   - Trust building through extended dialogue

### Delivery Mechanism (T1189)
- Invitation to clone GitHub repositories
- Legitimate-appearing projects (media players, crypto tools)
- Malicious npm dependencies embedded
- Multi-stage payload delivery

### Malware Deployment
- **BeaverTail:** Initial implant for reconnaissance
- **InvisibleFerret:** Advanced backdoor
- **AkdoorTea:** Previously undocumented backdoor
- **GolangGhost:** Go-based backdoor (2024)

---

## MITRE ATT&CK MAPPING

| Tactic | Technique | Description |
|--------|-----------|-------------|
| Initial Access | T1566.001 | Spearphishing Attachment |
| Initial Access | T1189 | Drive-by Compromise |
| Execution | T1059.007 | JavaScript |
| Execution | T1059.006 | Python |
| Persistence | T1543 | Create or Modify System Process |
| Defense Evasion | T1027 | Obfuscated Files or Information |
| Collection | T1005 | Data from Local System |
| Exfiltration | T1041 | Exfiltration Over C2 Channel |

---

## INDICATORS OF COMPROMISE

### Network
- Exfiltration to 86.104.74[.]51:1224
- /pdown/ URL path for Python second stage

### GitHub Repository Patterns
- Crypto trading tool repositories
- Media player projects
- Suspicious npm dependencies
- Recently created repositories with few stars

### Behavioral Indicators
- Unsolicited recruiter contact
- Request to clone and run GitHub code
- WhatsApp communication migration
- Job offers requiring code execution

---

## MITIGATION RECOMMENDATIONS

1. **Developer Education**
   - Train on social engineering tactics
   - Verify recruiter legitimacy
   - Never execute untrusted code

2. **Repository Security**
   - Code review before execution
   - Dependency scanning
   - Sandboxed development environments

3. **Communication Security**
   - Verify identity through official channels
   - Be suspicious of platform migration requests
   - Report suspicious recruitment attempts

---

## REFERENCES

1. [CyberProof - Crypto & Social Engineering: North Korean APTs in 2024](https://www.cyberproof.com/blog/crypto-social-engineering-north-korean-apts-in-2024/)
2. [SOCRadar - APT Profile: Lazarus Group](https://socradar.io/apt-profile-who-is-lazarus-group/)
3. [SlowMist - Cryptocurrency APT Intelligence: Lazarus Group Intrusion Techniques](https://slowmist.medium.com/cryptocurrency-apt-intelligence-unveiling-lazarus-groups-intrusion-techniques-a1a6efda7d34)

---

**Distribution:** TLP:CLEAR
**Contact:** otce-research@ncc.example.com

---
*End of Report*
