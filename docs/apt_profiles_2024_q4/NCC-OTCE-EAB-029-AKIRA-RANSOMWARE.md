# NCC-OTCE-EAB-029: Akira Ransomware Critical Infrastructure Campaign

**Document Classification:** TLP:CLEAR
**Report ID:** NCC-OTCE-EAB-029
**Date:** 2024-11-28
**Version:** 1.0

---

## EXECUTIVE SUMMARY

Akira ransomware has emerged as one of the most prolific ransomware families in 2024, accumulating over $244 million in ransom payments since March 2023. The group primarily targets SMBs but has also impacted large organizations across manufacturing, education, healthcare, and financial services.

**Threat Level:** CRITICAL
**Financial Impact:** $244+ million in ransoms
**Q3 2024 Status:** Most-detected ransomware variant in US
**November 2024 Activity:** 73 victims

---

## KEY HIGHLIGHTS

### 2024 Expansion
- First-ever encryption of Nutanix AHV VM disk files (June 2025)
- Exploitation of CVE-2024-40766
- Expanded beyond VMware ESXi and Hyper-V
- Updated CISA advisory (Nov 13, 2025) with new TTPs and IOCs

### Target Sectors
1. Manufacturing (Top target)
2. Legal/Professional Services
3. Construction/Engineering
4. Educational Institutions
5. Healthcare and Public Health
6. Financial Services
7. Food and Agriculture
8. Information Technology

---

## TACTICS

### Initial Access
- Ngrok tunneling utility for encrypted C2 sessions
- Bypassing perimeter monitoring
- VPN exploitation
- Compromised credentials

### Deployment
- VMware ESXi targeting
- Hyper-V environments
- Nutanix AHV (new in 2024)
- Double extortion tactics

---

## MITRE ATT&CK MAPPING

| Tactic | Technique |
|--------|-----------|
| Initial Access | T1133 - External Remote Services |
| Defense Evasion | T1572 - Protocol Tunneling (Ngrok) |
| Impact | T1486 - Data Encrypted for Impact |
| Impact | T1490 - Inhibit System Recovery |

---

## REFERENCES

1. [CISA Advisory AA24-109A - Akira Ransomware](https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-109a)
2. [Rewterz - Akira Ransomware Active IOCs](https://rewterz.com/threat-advisory/akira-ransomware-active-iocs)
3. [CybelAngel - The 2025 Akira Ransomware Playbook](https://cybelangel.com/blog/the-akira-ransomware-playbook-everything-you-need-to-know/)

---

**Distribution:** TLP:CLEAR
**Contact:** otce-research@ncc.example.com
