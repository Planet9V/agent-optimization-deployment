# NCC-OTCE-EAB-026: APT29 Midnight Blizzard RDP Campaign

**Document Classification:** TLP:CLEAR
**Report ID:** NCC-OTCE-EAB-026
**Date:** 2024-11-28
**Version:** 1.0
**Campaign Period:** October 2024 - November 2024

---

## EXECUTIVE SUMMARY

APT29 (Midnight Blizzard), attributed to Russia's Foreign Intelligence Service (SVR), launched a large-scale spear-phishing campaign in October 2024 using signed Remote Desktop Protocol (RDP) configuration files as a novel attack vector. This represents a significant evolution in APT29's tactics targeting government, academia, defense, and NGO sectors globally.

**Threat Level:** CRITICAL
**Primary Motivation:** Intelligence Collection / Cyber Espionage
**Attribution:** Russian Foreign Intelligence Service (SVR)
**Also Known As:** Cozy Bear, The Dukes, NOBELIUM, UNC2452, YTTRIUM

---

## THREAT ACTOR PROFILE

- **Nation-State:** Russian Federation
- **Intelligence Service:** SVR (Sluzhba Vneshney Razvedki)
- **Campaign Start:** October 22, 2024
- **Targets:** 100+ organizations across government, academia, defense, NGOs

---

## CAMPAIGN ANALYSIS

### Novel Attack Vector
**Signed RDP Configuration Files:**
- Thousands of spear-phishing emails sent
- RDP files connect to actor-controlled servers
- Bidirectional mapping of victim resources to attacker infrastructure

### Resource Access Upon Compromise
- All logical hard disks
- Clipboard contents
- Printers
- Connected peripheral devices
- Audio
- Authentication features

---

## MITRE ATT&CK MAPPING

| Tactic | Technique | Description |
|--------|-----------|-------------|
| Initial Access | T1566.001 | Spearphishing Attachment (RDP file) |
| Execution | T1021.001 | Remote Desktop Protocol |
| Persistence | T1133 | External Remote Services |
| Credential Access | T1557 | Adversary-in-the-Middle |
| Collection | T1025 | Data from Removable Media |
| Collection | T1115 | Clipboard Data |
| Exfiltration | T1041 | Exfiltration Over C2 Channel |

---

## DETECTION & MITIGATION

### Detection
- Monitor for unexpected .rdp file attachments
- Alert on RDP connections to unusual external IPs
- Track resource mapping in RDP sessions
- Monitor for signed file execution from email

### Mitigation
- Block .rdp attachments at email gateway
- Implement application whitelisting
- Deploy EDR with RDP monitoring
- User training on RDP file risks

---

## REFERENCES

1. [Microsoft Security Blog - Midnight Blizzard RDP Spear-Phishing](https://www.microsoft.com/en-us/security/blog/2024/10/29/midnight-blizzard-conducts-large-scale-spear-phishing-campaign-using-rdp-files/)
2. [Picus Security - Understanding Midnight Blizzard's RDP Campaign](https://www.picussecurity.com/resource/blog/understanding-and-mitigating-midnight-blizzards-rdp-based-spearphishing-campaign)
3. [HHS Advisory - Midnight Blizzard Threat Profile](https://www.hhs.gov/sites/default/files/new-midnight-blizzard-campaign-analyst-note-tlpclear.pdf)

---

**Distribution:** TLP:CLEAR
**Contact:** otce-research@ncc.example.com

---
*End of Report*
