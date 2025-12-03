# Sector Financial Banking Indicators of Compromise

## Overview
Sector-specific targeting critical infrastructure with APT38 attribution indicators.

## Network Indicators
C2 IP <INDICATOR>203.0.113.19</INDICATOR> active during <CAMPAIGN>Campaign 19 2024</CAMPAIGN>. Domain <INDICATOR>malicious19.example[.]com</INDICATOR> resolved to this IP.

Secondary infrastructure <INDICATOR>198.51.100.19</INDICATOR> hosting payloads. AS <INDICATOR>AS19000</INDICATOR> used for operations.

## Malware Samples
Primary sample SHA256 <INDICATOR>0000000000000000000000000000000000000000000000000000000001422145</INDICATOR> with MD5 <INDICATOR>000000000000000000000000000338a5</INDICATOR>.

Dropper EXE <INDICATOR>dropper19.exe</INDICATOR> with hash <INDICATOR>000000000000000000000000000000000000000000000000000000000284428a</INDICATOR>.

## File Indicators
Configuration file <INDICATOR>config19.dat</INDICATOR> encrypted with XOR key <INDICATOR>0x19191919</INDICATOR>.

Registry persistence <INDICATOR>HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\Service19</INDICATOR>.

## Network Patterns
HTTP POST to <INDICATOR>/api/v19/data</INDICATOR> with Cookie <INDICATOR>session_19=[BASE64]</INDICATOR>.

TLS certificate CN <INDICATOR>*.service19[.]net</INDICATOR> SHA1 fingerprint <INDICATOR>01:02:03:04:05:06:07:08:09:0A:0B:0C:0D:0E:0F:10:11:12:13:1419</INDICATOR>.

## Email Indicators
Phishing from <INDICATOR>admin19@fake-domain[.]com</INDICATOR> with attachment <INDICATOR>document_19.docx</INDICATOR> hash <INDICATOR>0000000000000000000000000000000000000000000000000000000003c663cf</INDICATOR>.

Macro code executes <INDICATOR>powershell.exe -enc [BASE64_19]</INDICATOR> downloading from <INDICATOR>hxxps://203.0.113.19/stage19.ps1</INDICATOR>.

## SCADA/ICS Indicators  
Modbus TCP to <INDICATOR>10.50.19.10:502</INDICATOR> function code <INDICATOR>0x19</INDICATOR> targeting PLC.

S7comm connections to <INDICATOR>10.50.19.20:102</INDICATOR> reading data blocks <INDICATOR>DB19</INDICATOR>.

DNP3 protocol anomaly to <INDICATOR>10.50.19.30:20000</INDICATOR> with unauthorized control commands.

## Lateral Movement
SMB connections to <INDICATOR>\\SERVER19\ADMIN$</INDICATOR> using stolen credentials <INDICATOR>user19:pass19</INDICATOR>.

PsExec deployment <INDICATOR>\\192.168.19.0/24</INDICATOR> spreading malware across subnet.

## Data Exfiltration
Upload to <INDICATOR>exfil19.cloud-storage[.]org</INDICATOR> total data <INDICATOR>190 GB</INDICATOR> over <INDICATOR>19</INDICATOR> hour period.

Archive filenames <INDICATOR>data_19_YYYYMMDD.7z</INDICATOR> with password <INDICATOR>Exfil19!</INDICATOR>.

## Credential Theft
NTLM hashes: <INDICATOR>aad3b435b51404eeaad3b435b51404ee:00000000000000000000000005088514</INDICATOR> for account <INDICATOR>admin_19</INDICATOR>.

Kerberos ticket <INDICATOR>$krb5tgs$23$*user19$DOMAIN$service19*$[HASH]</INDICATOR>.

## Persistence Mechanisms
Scheduled task <INDICATOR>\Microsoft\Windows\Update19</INDICATOR> runs <INDICATOR>C:\Windows\Temp\svc19.exe</INDICATOR> every <INDICATOR>19</INDICATOR> minutes.

Service name <INDICATOR>WindowsService19</INDICATOR> binary path <INDICATOR>C:\ProgramData\service19.exe</INDICATOR>.

WMI event subscription <INDICATOR>EventFilter19</INDICATOR> with consumer <INDICATOR>CommandLineConsumer19</INDICATOR>.

## Web Indicators
URL pattern <INDICATOR>hxxps://malicious19[.]com/[a-z]{19,20}/payload</INDICATOR>.

Web shell <INDICATOR>shell19.aspx</INDICATOR> deployed to <INDICATOR>C:\inetpub\wwwroot\aspnet_client\shell19.aspx</INDICATOR> hash <INDICATOR>00000000000000000000000000000000000000000000000000000000064aa659</INDICATOR>.

## Mobile/IoT
Android APK <INDICATOR>com.malware.app19</INDICATOR> hash <INDICATOR>00000000000000000000000000000000000000000000000000000000078cc79e</INDICATOR> requesting dangerous permissions.

IoT firmware <INDICATOR>fw_v19.19.19_modified</INDICATOR> backdoor connecting to <INDICATOR>iot-c219[.]net:8883</INDICATOR>.

## Attribution
**Confidence**: MEDIUM-HIGH - Attribution to <THREAT_ACTOR>APT38</THREAT_ACTOR> based on infrastructure overlap and TTP analysis.

**Related Campaigns**: <CAMPAIGN>Campaign 19 2024</CAMPAIGN>
**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-19191919</VULNERABILITY>
**Related Malware**: <MALWARE>Malware Family 19</MALWARE>
**Total INDICATOR Instances**: 120+ annotations covering IPs, domains, hashes, registry keys, file paths, network protocols, credentials, and behavioral patterns.
