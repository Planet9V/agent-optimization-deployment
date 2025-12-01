# NCC-OTCE-EAB-027: Mustang Panda ASEAN Targeting

**Document Classification:** TLP:CLEAR
**Report ID:** NCC-OTCE-EAB-027
**Date:** 2024-11-28
**Version:** 1.0
**Campaign Period:** January 2024 - March 2024

---

## EXECUTIVE SUMMARY

Mustang Panda (Stately Taurus), a Chinese state-sponsored APT group, conducted targeted cyber-espionage operations against Southeast Asian government entities during the ASEAN-Australia Special Summit (March 4-6, 2024), targeting Myanmar, Philippines, Japan, and Singapore.

**Threat Level:** HIGH
**Motivation:** Intelligence Collection / Cyber Espionage
**Attribution:** People's Republic of China
**Also Known As:** Stately Taurus, TA416, RedDelta, BRONZE PRESIDENT

---

## KEY CAMPAIGN DETAILS

### Targets
- Government ministries (Foreign Affairs, Defense, Trade)
- High-ranking government officials
- International collaboration entities
- ASEAN summit participants

### Novel TTPs (2024)
- Screensaver (.SCR) file extensions (deviation from typical ZIP/RAR/ISO archives)
- ToneShell backdoor variant deployment
- StarProxy tool for lateral movement
- Paklog and Corklog keyloggers

---

## MITRE ATT&CK MAPPING

| Tactic | Technique |
|--------|-----------|
| Initial Access | T1566.001 - Spearphishing Attachment |
| Execution | T1204.002 - User Execution: Malicious File |
| Persistence | T1547.001 - Registry Run Keys |
| Defense Evasion | T1036.008 - Masquerading: SCR Files |
| Command & Control | T1071.001 - Web Protocols |
| Collection | T1056.001 - Keylogging |

---

## REFERENCES

1. [Unit 42 - Stately Taurus Attacks SE Asian Government](https://unit42.paloaltonetworks.com/stately-taurus-attacks-se-asian-government/)
2. [IMDA Singapore - Chinese APT Groups Target ASEAN Entities](https://www.imda.gov.sg/-/media/imda/files/regulations-and-licensing/regulations/advisories/infocomm-media-cyber-security/chinese-apt-groups-target-asean-entities.pdf)
3. [CYFIRMA - APT Profile: Mustang Panda](https://www.cyfirma.com/research/apt-profile-mustang-panda/)

---

**Distribution:** TLP:CLEAR
**Contact:** otce-research@ncc.example.com
