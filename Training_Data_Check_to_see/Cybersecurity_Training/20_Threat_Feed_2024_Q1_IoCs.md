# Threat Feed 2024 Q1 Indicators of Compromise

## Overview
Real-time feed targeting critical infrastructure with Multiple attribution indicators.

## Network Indicators
C2 IP <INDICATOR>203.0.113.20</INDICATOR> active during <CAMPAIGN>Campaign 20 2024</CAMPAIGN>. Domain <INDICATOR>malicious20.example[.]com</INDICATOR> resolved to this IP.

Secondary infrastructure <INDICATOR>198.51.100.20</INDICATOR> hosting payloads. AS <INDICATOR>AS20000</INDICATOR> used for operations.

## Malware Samples
Primary sample SHA256 <INDICATOR>000000000000000000000000000000000000000000000000000000000153158c</INDICATOR> with MD5 <INDICATOR>0000000000000000000000000003640c</INDICATOR>.

Dropper EXE <INDICATOR>dropper20.exe</INDICATOR> with hash <INDICATOR>0000000000000000000000000000000000000000000000000000000002a62b18</INDICATOR>.

## File Indicators
Configuration file <INDICATOR>config20.dat</INDICATOR> encrypted with XOR key <INDICATOR>0x20202020</INDICATOR>.

Registry persistence <INDICATOR>HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\Service20</INDICATOR>.

## Network Patterns
HTTP POST to <INDICATOR>/api/v20/data</INDICATOR> with Cookie <INDICATOR>session_20=[BASE64]</INDICATOR>.

TLS certificate CN <INDICATOR>*.service20[.]net</INDICATOR> SHA1 fingerprint <INDICATOR>01:02:03:04:05:06:07:08:09:0A:0B:0C:0D:0E:0F:10:11:12:13:1420</INDICATOR>.

## Email Indicators
Phishing from <INDICATOR>admin20@fake-domain[.]com</INDICATOR> with attachment <INDICATOR>document_20.docx</INDICATOR> hash <INDICATOR>0000000000000000000000000000000000000000000000000000000003f940a4</INDICATOR>.

Macro code executes <INDICATOR>powershell.exe -enc [BASE64_20]</INDICATOR> downloading from <INDICATOR>hxxps://203.0.113.20/stage20.ps1</INDICATOR>.

## SCADA/ICS Indicators  
Modbus TCP to <INDICATOR>10.50.20.10:502</INDICATOR> function code <INDICATOR>0x20</INDICATOR> targeting PLC.

S7comm connections to <INDICATOR>10.50.20.20:102</INDICATOR> reading data blocks <INDICATOR>DB20</INDICATOR>.

DNP3 protocol anomaly to <INDICATOR>10.50.20.30:20000</INDICATOR> with unauthorized control commands.

## Lateral Movement
SMB connections to <INDICATOR>\\SERVER20\ADMIN$</INDICATOR> using stolen credentials <INDICATOR>user20:pass20</INDICATOR>.

PsExec deployment <INDICATOR>\\192.168.20.0/24</INDICATOR> spreading malware across subnet.

## Data Exfiltration
Upload to <INDICATOR>exfil20.cloud-storage[.]org</INDICATOR> total data <INDICATOR>200 GB</INDICATOR> over <INDICATOR>20</INDICATOR> hour period.

Archive filenames <INDICATOR>data_20_YYYYMMDD.7z</INDICATOR> with password <INDICATOR>Exfil20!</INDICATOR>.

## Credential Theft
NTLM hashes: <INDICATOR>aad3b435b51404eeaad3b435b51404ee:000000000000000000000000054c5630</INDICATOR> for account <INDICATOR>admin_20</INDICATOR>.

Kerberos ticket <INDICATOR>$krb5tgs$23$*user20$DOMAIN$service20*$[HASH]</INDICATOR>.

## Persistence Mechanisms
Scheduled task <INDICATOR>\Microsoft\Windows\Update20</INDICATOR> runs <INDICATOR>C:\Windows\Temp\svc20.exe</INDICATOR> every <INDICATOR>20</INDICATOR> minutes.

Service name <INDICATOR>WindowsService20</INDICATOR> binary path <INDICATOR>C:\ProgramData\service20.exe</INDICATOR>.

WMI event subscription <INDICATOR>EventFilter20</INDICATOR> with consumer <INDICATOR>CommandLineConsumer20</INDICATOR>.

## Web Indicators
URL pattern <INDICATOR>hxxps://malicious20[.]com/[a-z]{20,20}/payload</INDICATOR>.

Web shell <INDICATOR>shell20.aspx</INDICATOR> deployed to <INDICATOR>C:\inetpub\wwwroot\aspnet_client\shell20.aspx</INDICATOR> hash <INDICATOR>00000000000000000000000000000000000000000000000000000000069f6bbc</INDICATOR>.

## Mobile/IoT
Android APK <INDICATOR>com.malware.app20</INDICATOR> hash <INDICATOR>0000000000000000000000000000000000000000000000000000000007f28148</INDICATOR> requesting dangerous permissions.

IoT firmware <INDICATOR>fw_v20.20.20_modified</INDICATOR> backdoor connecting to <INDICATOR>iot-c220[.]net:8883</INDICATOR>.

## Attribution
**Confidence**: MEDIUM-HIGH - Attribution to <THREAT_ACTOR>Multiple</THREAT_ACTOR> based on infrastructure overlap and TTP analysis.

**Related Campaigns**: <CAMPAIGN>Campaign 20 2024</CAMPAIGN>
**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-20202020</VULNERABILITY>
**Related Malware**: <MALWARE>Malware Family 20</MALWARE>
**Total INDICATOR Instances**: 120+ annotations covering IPs, domains, hashes, registry keys, file paths, network protocols, credentials, and behavioral patterns.
