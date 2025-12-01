# Sector Aviation ATC Indicators of Compromise

## Overview
Sector-specific targeting critical infrastructure with APT28 attribution indicators.

## Network Indicators
C2 IP <INDICATOR>203.0.113.17</INDICATOR> active during <CAMPAIGN>Campaign 17 2024</CAMPAIGN>. Domain <INDICATOR>malicious17.example[.]com</INDICATOR> resolved to this IP.

Secondary infrastructure <INDICATOR>198.51.100.17</INDICATOR> hosting payloads. AS <INDICATOR>AS17000</INDICATOR> used for operations.

## Malware Samples
Primary sample SHA256 <INDICATOR>00000000000000000000000000000000000000000000000000000000012038b7</INDICATOR> with MD5 <INDICATOR>0000000000000000000000000002e1d7</INDICATOR>.

Dropper EXE <INDICATOR>dropper17.exe</INDICATOR> with hash <INDICATOR>000000000000000000000000000000000000000000000000000000000240716e</INDICATOR>.

## File Indicators
Configuration file <INDICATOR>config17.dat</INDICATOR> encrypted with XOR key <INDICATOR>0x17171717</INDICATOR>.

Registry persistence <INDICATOR>HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\Service17</INDICATOR>.

## Network Patterns
HTTP POST to <INDICATOR>/api/v17/data</INDICATOR> with Cookie <INDICATOR>session_17=[BASE64]</INDICATOR>.

TLS certificate CN <INDICATOR>*.service17[.]net</INDICATOR> SHA1 fingerprint <INDICATOR>01:02:03:04:05:06:07:08:09:0A:0B:0C:0D:0E:0F:10:11:12:13:1417</INDICATOR>.

## Email Indicators
Phishing from <INDICATOR>admin17@fake-domain[.]com</INDICATOR> with attachment <INDICATOR>document_17.docx</INDICATOR> hash <INDICATOR>000000000000000000000000000000000000000000000000000000000360aa25</INDICATOR>.

Macro code executes <INDICATOR>powershell.exe -enc [BASE64_17]</INDICATOR> downloading from <INDICATOR>hxxps://203.0.113.17/stage17.ps1</INDICATOR>.

## SCADA/ICS Indicators  
Modbus TCP to <INDICATOR>10.50.17.10:502</INDICATOR> function code <INDICATOR>0x17</INDICATOR> targeting PLC.

S7comm connections to <INDICATOR>10.50.17.20:102</INDICATOR> reading data blocks <INDICATOR>DB17</INDICATOR>.

DNP3 protocol anomaly to <INDICATOR>10.50.17.30:20000</INDICATOR> with unauthorized control commands.

## Lateral Movement
SMB connections to <INDICATOR>\\SERVER17\ADMIN$</INDICATOR> using stolen credentials <INDICATOR>user17:pass17</INDICATOR>.

PsExec deployment <INDICATOR>\\192.168.17.0/24</INDICATOR> spreading malware across subnet.

## Data Exfiltration
Upload to <INDICATOR>exfil17.cloud-storage[.]org</INDICATOR> total data <INDICATOR>170 GB</INDICATOR> over <INDICATOR>17</INDICATOR> hour period.

Archive filenames <INDICATOR>data_17_YYYYMMDD.7z</INDICATOR> with password <INDICATOR>Exfil17!</INDICATOR>.

## Credential Theft
NTLM hashes: <INDICATOR>aad3b435b51404eeaad3b435b51404ee:0000000000000000000000000480e2dc</INDICATOR> for account <INDICATOR>admin_17</INDICATOR>.

Kerberos ticket <INDICATOR>$krb5tgs$23$*user17$DOMAIN$service17*$[HASH]</INDICATOR>.

## Persistence Mechanisms
Scheduled task <INDICATOR>\Microsoft\Windows\Update17</INDICATOR> runs <INDICATOR>C:\Windows\Temp\svc17.exe</INDICATOR> every <INDICATOR>17</INDICATOR> minutes.

Service name <INDICATOR>WindowsService17</INDICATOR> binary path <INDICATOR>C:\ProgramData\service17.exe</INDICATOR>.

WMI event subscription <INDICATOR>EventFilter17</INDICATOR> with consumer <INDICATOR>CommandLineConsumer17</INDICATOR>.

## Web Indicators
URL pattern <INDICATOR>hxxps://malicious17[.]com/[a-z]{17,20}/payload</INDICATOR>.

Web shell <INDICATOR>shell17.aspx</INDICATOR> deployed to <INDICATOR>C:\inetpub\wwwroot\aspnet_client\shell17.aspx</INDICATOR> hash <INDICATOR>0000000000000000000000000000000000000000000000000000000005a11b93</INDICATOR>.

## Mobile/IoT
Android APK <INDICATOR>com.malware.app17</INDICATOR> hash <INDICATOR>0000000000000000000000000000000000000000000000000000000006c1544a</INDICATOR> requesting dangerous permissions.

IoT firmware <INDICATOR>fw_v17.17.17_modified</INDICATOR> backdoor connecting to <INDICATOR>iot-c217[.]net:8883</INDICATOR>.

## Attribution
**Confidence**: MEDIUM-HIGH - Attribution to <THREAT_ACTOR>APT28</THREAT_ACTOR> based on infrastructure overlap and TTP analysis.

**Related Campaigns**: <CAMPAIGN>Campaign 17 2024</CAMPAIGN>
**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-17171717</VULNERABILITY>
**Related Malware**: <MALWARE>Malware Family 17</MALWARE>
**Total INDICATOR Instances**: 120+ annotations covering IPs, domains, hashes, registry keys, file paths, network protocols, credentials, and behavioral patterns.
