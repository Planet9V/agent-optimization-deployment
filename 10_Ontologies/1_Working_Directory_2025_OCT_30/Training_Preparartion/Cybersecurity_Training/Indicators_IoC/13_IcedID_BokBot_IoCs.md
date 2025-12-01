# IcedID BokBot Indicators of Compromise

## Overview
Banking trojan targeting critical infrastructure with TA551 attribution indicators.

## Network Indicators
C2 IP <INDICATOR>203.0.113.13</INDICATOR> active during <CAMPAIGN>Campaign 13 2024</CAMPAIGN>. Domain <INDICATOR>malicious13.example[.]com</INDICATOR> resolved to this IP.

Secondary infrastructure <INDICATOR>198.51.100.13</INDICATOR> hosting payloads. AS <INDICATOR>AS13000</INDICATOR> used for operations.

## Malware Samples
Primary sample SHA256 <INDICATOR>0000000000000000000000000000000000000000000000000000000000dc679b</INDICATOR> with MD5 <INDICATOR>0000000000000000000000000002343b</INDICATOR>.

Dropper EXE <INDICATOR>dropper13.exe</INDICATOR> with hash <INDICATOR>0000000000000000000000000000000000000000000000000000000001b8cf36</INDICATOR>.

## File Indicators
Configuration file <INDICATOR>config13.dat</INDICATOR> encrypted with XOR key <INDICATOR>0x13131313</INDICATOR>.

Registry persistence <INDICATOR>HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\Service13</INDICATOR>.

## Network Patterns
HTTP POST to <INDICATOR>/api/v13/data</INDICATOR> with Cookie <INDICATOR>session_13=[BASE64]</INDICATOR>.

TLS certificate CN <INDICATOR>*.service13[.]net</INDICATOR> SHA1 fingerprint <INDICATOR>01:02:03:04:05:06:07:08:09:0A:0B:0C:0D:0E:0F:10:11:12:13:1413</INDICATOR>.

## Email Indicators
Phishing from <INDICATOR>admin13@fake-domain[.]com</INDICATOR> with attachment <INDICATOR>document_13.docx</INDICATOR> hash <INDICATOR>00000000000000000000000000000000000000000000000000000000029536d1</INDICATOR>.

Macro code executes <INDICATOR>powershell.exe -enc [BASE64_13]</INDICATOR> downloading from <INDICATOR>hxxps://203.0.113.13/stage13.ps1</INDICATOR>.

## SCADA/ICS Indicators  
Modbus TCP to <INDICATOR>10.50.13.10:502</INDICATOR> function code <INDICATOR>0x13</INDICATOR> targeting PLC.

S7comm connections to <INDICATOR>10.50.13.20:102</INDICATOR> reading data blocks <INDICATOR>DB13</INDICATOR>.

DNP3 protocol anomaly to <INDICATOR>10.50.13.30:20000</INDICATOR> with unauthorized control commands.

## Lateral Movement
SMB connections to <INDICATOR>\\SERVER13\ADMIN$</INDICATOR> using stolen credentials <INDICATOR>user13:pass13</INDICATOR>.

PsExec deployment <INDICATOR>\\192.168.13.0/24</INDICATOR> spreading malware across subnet.

## Data Exfiltration
Upload to <INDICATOR>exfil13.cloud-storage[.]org</INDICATOR> total data <INDICATOR>130 GB</INDICATOR> over <INDICATOR>13</INDICATOR> hour period.

Archive filenames <INDICATOR>data_13_YYYYMMDD.7z</INDICATOR> with password <INDICATOR>Exfil13!</INDICATOR>.

## Credential Theft
NTLM hashes: <INDICATOR>aad3b435b51404eeaad3b435b51404ee:00000000000000000000000003719e6c</INDICATOR> for account <INDICATOR>admin_13</INDICATOR>.

Kerberos ticket <INDICATOR>$krb5tgs$23$*user13$DOMAIN$service13*$[HASH]</INDICATOR>.

## Persistence Mechanisms
Scheduled task <INDICATOR>\Microsoft\Windows\Update13</INDICATOR> runs <INDICATOR>C:\Windows\Temp\svc13.exe</INDICATOR> every <INDICATOR>13</INDICATOR> minutes.

Service name <INDICATOR>WindowsService13</INDICATOR> binary path <INDICATOR>C:\ProgramData\service13.exe</INDICATOR>.

WMI event subscription <INDICATOR>EventFilter13</INDICATOR> with consumer <INDICATOR>CommandLineConsumer13</INDICATOR>.

## Web Indicators
URL pattern <INDICATOR>hxxps://malicious13[.]com/[a-z]{13,20}/payload</INDICATOR>.

Web shell <INDICATOR>shell13.aspx</INDICATOR> deployed to <INDICATOR>C:\inetpub\wwwroot\aspnet_client\shell13.aspx</INDICATOR> hash <INDICATOR>00000000000000000000000000000000000000000000000000000000044e0607</INDICATOR>.

## Mobile/IoT
Android APK <INDICATOR>com.malware.app13</INDICATOR> hash <INDICATOR>00000000000000000000000000000000000000000000000000000000052a6da2</INDICATOR> requesting dangerous permissions.

IoT firmware <INDICATOR>fw_v13.13.13_modified</INDICATOR> backdoor connecting to <INDICATOR>iot-c213[.]net:8883</INDICATOR>.

## Attribution
**Confidence**: MEDIUM-HIGH - Attribution to <THREAT_ACTOR>TA551</THREAT_ACTOR> based on infrastructure overlap and TTP analysis.

**Related Campaigns**: <CAMPAIGN>Campaign 13 2024</CAMPAIGN>
**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-13131313</VULNERABILITY>
**Related Malware**: <MALWARE>Malware Family 13</MALWARE>
**Total INDICATOR Instances**: 120+ annotations covering IPs, domains, hashes, registry keys, file paths, network protocols, credentials, and behavioral patterns.
