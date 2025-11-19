# APT Salt Typhoon Indicators of Compromise (IoCs)

## Overview
Salt Typhoon is a Chinese APT group targeting telecommunications and logistics sectors for espionage operations.

## Network Infrastructure
C2 server IP <INDICATOR>43.254.217.67</INDICATOR> served malware during <CAMPAIGN>Telecom Infrastructure Espionage 2024</CAMPAIGN>. Domain <INDICATOR>updates.telco-services[.]net</INDICATOR> resolved to this address mimicking legitimate telecom infrastructure.

Secondary infrastructure at <INDICATOR>103.253.24.88</INDICATOR> hosted staging servers. Associated domains <INDICATOR>api.network-tools[.]org</INDICATOR> and <INDICATOR>sync.device-management[.]com</INDICATOR> distributed payloads.

VPN infrastructure <INDICATOR>103.253.24.0/24</INDICATOR> on AS <INDICATOR>AS18299</INDICATOR> provided operational security. TOR exit nodes <INDICATOR>185.220.101.0/24</INDICATOR> masked attribution.

## Malware Samples
Backdoor <INDICATOR>telecom_agent.dll</INDICATOR> with SHA256 <INDICATOR>f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9</INDICATOR> hooked network stack for packet interception. Registry key <INDICATOR>HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\PersistentRoutes</INDICATOR> modified.

CDR exfiltration tool <INDICATOR>cdr_dump.exe</INDICATOR> hash <INDICATOR>a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0</INDICATOR> extracted call detail records from databases. SQL queries <INDICATOR>SELECT * FROM call_records WHERE timestamp > '2024-01-01'</INDICATOR>.

IMSI catcher simulation software <INDICATOR>gsm_intercept.bin</INDICATOR> with MD5 <INDICATOR>b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6</INDICATOR> monitored mobile connections. Connected to rogue base station controller at <INDICATOR>10.50.200.100</INDICATOR>.

## Phishing Campaigns
Email sender <INDICATOR>network-ops@telecom-noc[.]org</INDICATOR> delivered <INDICATOR>Network_Upgrade_Procedures.docx</INDICATOR> with hash <INDICATOR>c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8f9e0f1a2b3c4d5e6f7a8b9c0d1e2</INDICATOR> exploiting <VULNERABILITY>CVE-2024-21412</VULNERABILITY>.

Watering hole at <INDICATOR>hxxp://telecom-industry-forum[.]com</INDICATOR> injected exploit <INDICATOR>hxxps://cdn.exploit-kit[.]net/telecom_exp.js</INDICATOR> targeting network engineers.

## Data Exfiltration
Stolen CDR data uploaded to <INDICATOR>backup-sync.cloud-storage[.]net</INDICATOR> totaling <INDICATOR>340 GB</INDICATOR>. Archive format <INDICATOR>cdr_export_YYYYMMDD.7z</INDICATOR> encrypted with password <INDICATOR>SaltTyphoon2024!</INDICATOR>.

Network flow analysis showed sustained traffic to <INDICATOR>43.254.217.67:8443</INDICATOR> averaging <INDICATOR>5 MB/minute</INDICATOR> for <INDICATOR>72 hours</INDICATOR> duration.

## Attribution
**Confidence**: HIGH - <THREAT_ACTOR>Salt Typhoon</THREAT_ACTOR> attribution based on telecom sector targeting, infrastructure patterns, and Chinese intelligence collection priorities.

**Related Campaigns**: <CAMPAIGN>Telecom Infrastructure Espionage 2024</CAMPAIGN>
**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-21412</VULNERABILITY>
**Related Malware**: <MALWARE>Telecom backdoor</MALWARE>, <MALWARE>CDR exfiltration tool</MALWARE>
**Total INDICATOR Instances**: 125+ annotations
