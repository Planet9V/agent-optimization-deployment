# NCC-OTCE-EAB-028: Qilin Ransomware Healthcare Targeting

**Document Classification:** TLP:CLEAR
**Report ID:** NCC-OTCE-EAB-028
**Date:** 2024-11-28
**Version:** 1.0
**Campaign Period:** 2024 (Peak Activity: June 2024)

---

## EXECUTIVE SUMMARY

Qilin (also known as Agenda) ransomware group significantly escalated operations in 2024, particularly targeting healthcare and critical infrastructure. The June 2024 Synnovis attack disrupted London hospitals and demonstrated the group's capability to cause widespread societal impact.

**Threat Level:** CRITICAL
**Motivation:** Financial Gain
**Operational Model:** Ransomware-as-a-Service (RaaS)
**2024 Financial Impact:** $50+ million in ransom payments

---

## HIGH-PROFILE ATTACKS

### Synnovis Healthcare Attack (June 2024)
- **Victim:** UK pathology and diagnostic services provider
- **Ransom Demand:** $50 million
- **Data Compromised:** ~400GB of healthcare data
- **Impact:** 
  - Canceled surgeries and organ transplants at major London hospitals
  - Blood supply disruption
  - 900,000 people data breach
  - £33 million ($44 million) in costs

### 2024 Activity Statistics
- 60+ ransomware attacks claimed since January 2024
- Healthcare victims: 7% of 100+ total victims
- 15 incidents in Healthcare and Public Health Sector since October 2022

---

## TARGET SECTORS

1. Manufacturing (Primary)
2. Healthcare and Public Health
3. Financial Services
4. Legal/Professional Services
5. Construction/Engineering
6. Retail
7. Government Agencies
8. Energy

---

## TACTICS, TECHNIQUES, AND PROCEDURES

### Initial Access
- Exploitation of Fortinet vulnerabilities (critical CVEs)
- Compromised VPN credentials
- Vulnerable public-facing applications

### Lateral Movement
- Active Directory reconnaissance
- Credential theft and privilege escalation
- Network mapping

### Impact
- Double extortion model (encryption + data leak threat)
- Data exfiltration before encryption
- Public data leak site for victim shaming
- Targeting of backup systems

---

## MITRE ATT&CK MAPPING

| Tactic | Technique |
|--------|-----------|
| Initial Access | T1190 - Exploit Public-Facing Application |
| Credential Access | T1003 - OS Credential Dumping |
| Discovery | T1018 - Remote System Discovery |
| Lateral Movement | T1021.001 - RDP |
| Collection | T1560 - Archive Collected Data |
| Exfiltration | T1041 - Exfiltration Over C2 |
| Impact | T1486 - Data Encrypted for Impact |
| Impact | T1490 - Inhibit System Recovery |

---

## INDICATORS OF COMPROMISE

### File Indicators
- .qilin or .agenda file extensions
- Ransom notes (README files)
- Execution via scheduled tasks

### Network Indicators
- Connections to Tor C2 infrastructure
- Large data exfiltration before encryption
- RDP lateral movement patterns

### Behavioral Indicators
- Backup deletion attempts
- Shadow copy removal
- Service termination (databases, security tools)

---

## MITIGATION RECOMMENDATIONS

### Immediate
1. Patch critical Fortinet vulnerabilities
2. Implement MFA on all remote access
3. Segment networks (especially healthcare environments)
4. Offline, immutable backups

### Strategic
1. Deploy EDR with ransomware-specific detection
2. Implement zero-trust architecture
3. Regular backup testing and recovery drills
4. Healthcare-specific incident response plans

---

## REFERENCES

1. [Industrial Cyber - Qilin Ransomware Escalates in 2025](https://industrialcyber.co/ransomware/qilin-ransomware-escalates-rapidly-in-2025-targeting-critical-sectors-with-700-attacks-amid-ransomhub-shutdown/)
2. [AHA/HHS - Qilin Ransomware Threat Profile](https://www.aha.org/system/files/media/file/2024/06/tlp-clear-hc3-threat-profile-qilin-aka-agenda-ransomware-6-18-2024.pdf)
3. [Qualys - Qilin Ransomware Explained](https://blog.qualys.com/vulnerabilities-threat-research/2025/06/18/qilin-ransomware-explained-threats-risks-defenses)
4. [Check Point - Qilin Ransomware Deep Dive](https://www.checkpoint.com/cyber-hub/threat-prevention/ransomware/qilin-ransomware/)

---

**Distribution:** TLP:CLEAR
**Contact:** otce-research@ncc.example.com
