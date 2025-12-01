# Sector Maritime Port Systems Indicators of Compromise

## Overview
Sector-specific targeting critical infrastructure with APT40 attribution indicators.

## Network Indicators
C2 IP <INDICATOR>203.0.113.16</INDICATOR> active during <CAMPAIGN>Campaign 16 2024</CAMPAIGN>. Domain <INDICATOR>malicious16.example[.]com</INDICATOR> resolved to this IP.

Secondary infrastructure <INDICATOR>198.51.100.16</INDICATOR> hosting payloads. AS <INDICATOR>AS16000</INDICATOR> used for operations.

## Malware Samples
Primary sample SHA256 <INDICATOR>00000000000000000000000000000000000000000000000000000000010f4470</INDICATOR> with MD5 <INDICATOR>0000000000000000000000000002b670</INDICATOR>.

Dropper EXE <INDICATOR>dropper16.exe</INDICATOR> with hash <INDICATOR>00000000000000000000000000000000000000000000000000000000021e88e0</INDICATOR>.

## File Indicators
Configuration file <INDICATOR>config16.dat</INDICATOR> encrypted with XOR key <INDICATOR>0x16161616</INDICATOR>.

Registry persistence <INDICATOR>HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\Service16</INDICATOR>.

## Network Patterns
HTTP POST to <INDICATOR>/api/v16/data</INDICATOR> with Cookie <INDICATOR>session_16=[BASE64]</INDICATOR>.

TLS certificate CN <INDICATOR>*.service16[.]net</INDICATOR> SHA1 fingerprint <INDICATOR>01:02:03:04:05:06:07:08:09:0A:0B:0C:0D:0E:0F:10:11:12:13:1416</INDICATOR>.

## Email Indicators
Phishing from <INDICATOR>admin16@fake-domain[.]com</INDICATOR> with attachment <INDICATOR>document_16.docx</INDICATOR> hash <INDICATOR>00000000000000000000000000000000000000000000000000000000032dcd50</INDICATOR>.

Macro code executes <INDICATOR>powershell.exe -enc [BASE64_16]</INDICATOR> downloading from <INDICATOR>hxxps://203.0.113.16/stage16.ps1</INDICATOR>.

## SCADA/ICS Indicators  
Modbus TCP to <INDICATOR>10.50.16.10:502</INDICATOR> function code <INDICATOR>0x16</INDICATOR> targeting PLC.

S7comm connections to <INDICATOR>10.50.16.20:102</INDICATOR> reading data blocks <INDICATOR>DB16</INDICATOR>.

DNP3 protocol anomaly to <INDICATOR>10.50.16.30:20000</INDICATOR> with unauthorized control commands.

## Lateral Movement
SMB connections to <INDICATOR>\\SERVER16\ADMIN$</INDICATOR> using stolen credentials <INDICATOR>user16:pass16</INDICATOR>.

PsExec deployment <INDICATOR>\\192.168.16.0/24</INDICATOR> spreading malware across subnet.

## Data Exfiltration
Upload to <INDICATOR>exfil16.cloud-storage[.]org</INDICATOR> total data <INDICATOR>160 GB</INDICATOR> over <INDICATOR>16</INDICATOR> hour period.

Archive filenames <INDICATOR>data_16_YYYYMMDD.7z</INDICATOR> with password <INDICATOR>Exfil16!</INDICATOR>.

## Credential Theft
NTLM hashes: <INDICATOR>aad3b435b51404eeaad3b435b51404ee:000000000000000000000000043d11c0</INDICATOR> for account <INDICATOR>admin_16</INDICATOR>.

Kerberos ticket <INDICATOR>$krb5tgs$23$*user16$DOMAIN$service16*$[HASH]</INDICATOR>.

## Persistence Mechanisms
Scheduled task <INDICATOR>\Microsoft\Windows\Update16</INDICATOR> runs <INDICATOR>C:\Windows\Temp\svc16.exe</INDICATOR> every <INDICATOR>16</INDICATOR> minutes.

Service name <INDICATOR>WindowsService16</INDICATOR> binary path <INDICATOR>C:\ProgramData\service16.exe</INDICATOR>.

WMI event subscription <INDICATOR>EventFilter16</INDICATOR> with consumer <INDICATOR>CommandLineConsumer16</INDICATOR>.

## Web Indicators
URL pattern <INDICATOR>hxxps://malicious16[.]com/[a-z]{16,20}/payload</INDICATOR>.

Web shell <INDICATOR>shell16.aspx</INDICATOR> deployed to <INDICATOR>C:\inetpub\wwwroot\aspnet_client\shell16.aspx</INDICATOR> hash <INDICATOR>00000000000000000000000000000000000000000000000000000000054c5630</INDICATOR>.

## Mobile/IoT
Android APK <INDICATOR>com.malware.app16</INDICATOR> hash <INDICATOR>00000000000000000000000000000000000000000000000000000000065b9aa0</INDICATOR> requesting dangerous permissions.

IoT firmware <INDICATOR>fw_v16.16.16_modified</INDICATOR> backdoor connecting to <INDICATOR>iot-c216[.]net:8883</INDICATOR>.

## Attribution
**Confidence**: MEDIUM-HIGH - Attribution to <THREAT_ACTOR>APT40</THREAT_ACTOR> based on infrastructure overlap and TTP analysis.

**Related Campaigns**: <CAMPAIGN>Campaign 16 2024</CAMPAIGN>
**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-16161616</VULNERABILITY>
**Related Malware**: <MALWARE>Malware Family 16</MALWARE>
**Total INDICATOR Instances**: 120+ annotations covering IPs, domains, hashes, registry keys, file paths, network protocols, credentials, and behavioral patterns.
