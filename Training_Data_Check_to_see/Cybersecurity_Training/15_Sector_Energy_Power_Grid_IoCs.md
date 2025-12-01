# Sector Energy Power Grid Indicators of Compromise

## Overview
Sector-specific targeting critical infrastructure with APT33 attribution indicators.

## Network Indicators
C2 IP <INDICATOR>203.0.113.15</INDICATOR> active during <CAMPAIGN>Campaign 15 2024</CAMPAIGN>. Domain <INDICATOR>malicious15.example[.]com</INDICATOR> resolved to this IP.

Secondary infrastructure <INDICATOR>198.51.100.15</INDICATOR> hosting payloads. AS <INDICATOR>AS15000</INDICATOR> used for operations.

## Malware Samples
Primary sample SHA256 <INDICATOR>0000000000000000000000000000000000000000000000000000000000fe5029</INDICATOR> with MD5 <INDICATOR>00000000000000000000000000028b09</INDICATOR>.

Dropper EXE <INDICATOR>dropper15.exe</INDICATOR> with hash <INDICATOR>0000000000000000000000000000000000000000000000000000000001fca052</INDICATOR>.

## File Indicators
Configuration file <INDICATOR>config15.dat</INDICATOR> encrypted with XOR key <INDICATOR>0x15151515</INDICATOR>.

Registry persistence <INDICATOR>HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\Service15</INDICATOR>.

## Network Patterns
HTTP POST to <INDICATOR>/api/v15/data</INDICATOR> with Cookie <INDICATOR>session_15=[BASE64]</INDICATOR>.

TLS certificate CN <INDICATOR>*.service15[.]net</INDICATOR> SHA1 fingerprint <INDICATOR>01:02:03:04:05:06:07:08:09:0A:0B:0C:0D:0E:0F:10:11:12:13:1415</INDICATOR>.

## Email Indicators
Phishing from <INDICATOR>admin15@fake-domain[.]com</INDICATOR> with attachment <INDICATOR>document_15.docx</INDICATOR> hash <INDICATOR>0000000000000000000000000000000000000000000000000000000002faf07b</INDICATOR>.

Macro code executes <INDICATOR>powershell.exe -enc [BASE64_15]</INDICATOR> downloading from <INDICATOR>hxxps://203.0.113.15/stage15.ps1</INDICATOR>.

## SCADA/ICS Indicators  
Modbus TCP to <INDICATOR>10.50.15.10:502</INDICATOR> function code <INDICATOR>0x15</INDICATOR> targeting PLC.

S7comm connections to <INDICATOR>10.50.15.20:102</INDICATOR> reading data blocks <INDICATOR>DB15</INDICATOR>.

DNP3 protocol anomaly to <INDICATOR>10.50.15.30:20000</INDICATOR> with unauthorized control commands.

## Lateral Movement
SMB connections to <INDICATOR>\\SERVER15\ADMIN$</INDICATOR> using stolen credentials <INDICATOR>user15:pass15</INDICATOR>.

PsExec deployment <INDICATOR>\\192.168.15.0/24</INDICATOR> spreading malware across subnet.

## Data Exfiltration
Upload to <INDICATOR>exfil15.cloud-storage[.]org</INDICATOR> total data <INDICATOR>150 GB</INDICATOR> over <INDICATOR>15</INDICATOR> hour period.

Archive filenames <INDICATOR>data_15_YYYYMMDD.7z</INDICATOR> with password <INDICATOR>Exfil15!</INDICATOR>.

## Credential Theft
NTLM hashes: <INDICATOR>aad3b435b51404eeaad3b435b51404ee:00000000000000000000000003f940a4</INDICATOR> for account <INDICATOR>admin_15</INDICATOR>.

Kerberos ticket <INDICATOR>$krb5tgs$23$*user15$DOMAIN$service15*$[HASH]</INDICATOR>.

## Persistence Mechanisms
Scheduled task <INDICATOR>\Microsoft\Windows\Update15</INDICATOR> runs <INDICATOR>C:\Windows\Temp\svc15.exe</INDICATOR> every <INDICATOR>15</INDICATOR> minutes.

Service name <INDICATOR>WindowsService15</INDICATOR> binary path <INDICATOR>C:\ProgramData\service15.exe</INDICATOR>.

WMI event subscription <INDICATOR>EventFilter15</INDICATOR> with consumer <INDICATOR>CommandLineConsumer15</INDICATOR>.

## Web Indicators
URL pattern <INDICATOR>hxxps://malicious15[.]com/[a-z]{15,20}/payload</INDICATOR>.

Web shell <INDICATOR>shell15.aspx</INDICATOR> deployed to <INDICATOR>C:\inetpub\wwwroot\aspnet_client\shell15.aspx</INDICATOR> hash <INDICATOR>0000000000000000000000000000000000000000000000000000000004f790cd</INDICATOR>.

## Mobile/IoT
Android APK <INDICATOR>com.malware.app15</INDICATOR> hash <INDICATOR>0000000000000000000000000000000000000000000000000000000005f5e0f6</INDICATOR> requesting dangerous permissions.

IoT firmware <INDICATOR>fw_v15.15.15_modified</INDICATOR> backdoor connecting to <INDICATOR>iot-c215[.]net:8883</INDICATOR>.

## Attribution
**Confidence**: MEDIUM-HIGH - Attribution to <THREAT_ACTOR>APT33</THREAT_ACTOR> based on infrastructure overlap and TTP analysis.

**Related Campaigns**: <CAMPAIGN>Campaign 15 2024</CAMPAIGN>
**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-15151515</VULNERABILITY>
**Related Malware**: <MALWARE>Malware Family 15</MALWARE>
**Total INDICATOR Instances**: 120+ annotations covering IPs, domains, hashes, registry keys, file paths, network protocols, credentials, and behavioral patterns.
