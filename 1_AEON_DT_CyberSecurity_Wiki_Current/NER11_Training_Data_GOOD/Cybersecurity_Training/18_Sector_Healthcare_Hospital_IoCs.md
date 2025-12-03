# Sector Healthcare Hospital Indicators of Compromise

## Overview
Sector-specific targeting critical infrastructure with Ransomware groups attribution indicators.

## Network Indicators
C2 IP <INDICATOR>203.0.113.18</INDICATOR> active during <CAMPAIGN>Campaign 18 2024</CAMPAIGN>. Domain <INDICATOR>malicious18.example[.]com</INDICATOR> resolved to this IP.

Secondary infrastructure <INDICATOR>198.51.100.18</INDICATOR> hosting payloads. AS <INDICATOR>AS18000</INDICATOR> used for operations.

## Malware Samples
Primary sample SHA256 <INDICATOR>0000000000000000000000000000000000000000000000000000000001312cfe</INDICATOR> with MD5 <INDICATOR>00000000000000000000000000030d3e</INDICATOR>.

Dropper EXE <INDICATOR>dropper18.exe</INDICATOR> with hash <INDICATOR>00000000000000000000000000000000000000000000000000000000026259fc</INDICATOR>.

## File Indicators
Configuration file <INDICATOR>config18.dat</INDICATOR> encrypted with XOR key <INDICATOR>0x18181818</INDICATOR>.

Registry persistence <INDICATOR>HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\Service18</INDICATOR>.

## Network Patterns
HTTP POST to <INDICATOR>/api/v18/data</INDICATOR> with Cookie <INDICATOR>session_18=[BASE64]</INDICATOR>.

TLS certificate CN <INDICATOR>*.service18[.]net</INDICATOR> SHA1 fingerprint <INDICATOR>01:02:03:04:05:06:07:08:09:0A:0B:0C:0D:0E:0F:10:11:12:13:1418</INDICATOR>.

## Email Indicators
Phishing from <INDICATOR>admin18@fake-domain[.]com</INDICATOR> with attachment <INDICATOR>document_18.docx</INDICATOR> hash <INDICATOR>00000000000000000000000000000000000000000000000000000000039386fa</INDICATOR>.

Macro code executes <INDICATOR>powershell.exe -enc [BASE64_18]</INDICATOR> downloading from <INDICATOR>hxxps://203.0.113.18/stage18.ps1</INDICATOR>.

## SCADA/ICS Indicators  
Modbus TCP to <INDICATOR>10.50.18.10:502</INDICATOR> function code <INDICATOR>0x18</INDICATOR> targeting PLC.

S7comm connections to <INDICATOR>10.50.18.20:102</INDICATOR> reading data blocks <INDICATOR>DB18</INDICATOR>.

DNP3 protocol anomaly to <INDICATOR>10.50.18.30:20000</INDICATOR> with unauthorized control commands.

## Lateral Movement
SMB connections to <INDICATOR>\\SERVER18\ADMIN$</INDICATOR> using stolen credentials <INDICATOR>user18:pass18</INDICATOR>.

PsExec deployment <INDICATOR>\\192.168.18.0/24</INDICATOR> spreading malware across subnet.

## Data Exfiltration
Upload to <INDICATOR>exfil18.cloud-storage[.]org</INDICATOR> total data <INDICATOR>180 GB</INDICATOR> over <INDICATOR>18</INDICATOR> hour period.

Archive filenames <INDICATOR>data_18_YYYYMMDD.7z</INDICATOR> with password <INDICATOR>Exfil18!</INDICATOR>.

## Credential Theft
NTLM hashes: <INDICATOR>aad3b435b51404eeaad3b435b51404ee:00000000000000000000000004c4b3f8</INDICATOR> for account <INDICATOR>admin_18</INDICATOR>.

Kerberos ticket <INDICATOR>$krb5tgs$23$*user18$DOMAIN$service18*$[HASH]</INDICATOR>.

## Persistence Mechanisms
Scheduled task <INDICATOR>\Microsoft\Windows\Update18</INDICATOR> runs <INDICATOR>C:\Windows\Temp\svc18.exe</INDICATOR> every <INDICATOR>18</INDICATOR> minutes.

Service name <INDICATOR>WindowsService18</INDICATOR> binary path <INDICATOR>C:\ProgramData\service18.exe</INDICATOR>.

WMI event subscription <INDICATOR>EventFilter18</INDICATOR> with consumer <INDICATOR>CommandLineConsumer18</INDICATOR>.

## Web Indicators
URL pattern <INDICATOR>hxxps://malicious18[.]com/[a-z]{18,20}/payload</INDICATOR>.

Web shell <INDICATOR>shell18.aspx</INDICATOR> deployed to <INDICATOR>C:\inetpub\wwwroot\aspnet_client\shell18.aspx</INDICATOR> hash <INDICATOR>0000000000000000000000000000000000000000000000000000000005f5e0f6</INDICATOR>.

## Mobile/IoT
Android APK <INDICATOR>com.malware.app18</INDICATOR> hash <INDICATOR>0000000000000000000000000000000000000000000000000000000007270df4</INDICATOR> requesting dangerous permissions.

IoT firmware <INDICATOR>fw_v18.18.18_modified</INDICATOR> backdoor connecting to <INDICATOR>iot-c218[.]net:8883</INDICATOR>.

## Attribution
**Confidence**: MEDIUM-HIGH - Attribution to <THREAT_ACTOR>Ransomware groups</THREAT_ACTOR> based on infrastructure overlap and TTP analysis.

**Related Campaigns**: <CAMPAIGN>Campaign 18 2024</CAMPAIGN>
**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-18181818</VULNERABILITY>
**Related Malware**: <MALWARE>Malware Family 18</MALWARE>
**Total INDICATOR Instances**: 120+ annotations covering IPs, domains, hashes, registry keys, file paths, network protocols, credentials, and behavioral patterns.
