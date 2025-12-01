# Cobalt Strike Abuse Indicators of Compromise

## Overview
Post-exploitation targeting critical infrastructure with Multiple APTs attribution indicators.

## Network Indicators
C2 IP <INDICATOR>203.0.113.14</INDICATOR> active during <CAMPAIGN>Campaign 14 2024</CAMPAIGN>. Domain <INDICATOR>malicious14.example[.]com</INDICATOR> resolved to this IP.

Secondary infrastructure <INDICATOR>198.51.100.14</INDICATOR> hosting payloads. AS <INDICATOR>AS14000</INDICATOR> used for operations.

## Malware Samples
Primary sample SHA256 <INDICATOR>0000000000000000000000000000000000000000000000000000000000ed5be2</INDICATOR> with MD5 <INDICATOR>00000000000000000000000000025fa2</INDICATOR>.

Dropper EXE <INDICATOR>dropper14.exe</INDICATOR> with hash <INDICATOR>0000000000000000000000000000000000000000000000000000000001dab7c4</INDICATOR>.

## File Indicators
Configuration file <INDICATOR>config14.dat</INDICATOR> encrypted with XOR key <INDICATOR>0x14141414</INDICATOR>.

Registry persistence <INDICATOR>HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\Service14</INDICATOR>.

## Network Patterns
HTTP POST to <INDICATOR>/api/v14/data</INDICATOR> with Cookie <INDICATOR>session_14=[BASE64]</INDICATOR>.

TLS certificate CN <INDICATOR>*.service14[.]net</INDICATOR> SHA1 fingerprint <INDICATOR>01:02:03:04:05:06:07:08:09:0A:0B:0C:0D:0E:0F:10:11:12:13:1414</INDICATOR>.

## Email Indicators
Phishing from <INDICATOR>admin14@fake-domain[.]com</INDICATOR> with attachment <INDICATOR>document_14.docx</INDICATOR> hash <INDICATOR>0000000000000000000000000000000000000000000000000000000002c813a6</INDICATOR>.

Macro code executes <INDICATOR>powershell.exe -enc [BASE64_14]</INDICATOR> downloading from <INDICATOR>hxxps://203.0.113.14/stage14.ps1</INDICATOR>.

## SCADA/ICS Indicators  
Modbus TCP to <INDICATOR>10.50.14.10:502</INDICATOR> function code <INDICATOR>0x14</INDICATOR> targeting PLC.

S7comm connections to <INDICATOR>10.50.14.20:102</INDICATOR> reading data blocks <INDICATOR>DB14</INDICATOR>.

DNP3 protocol anomaly to <INDICATOR>10.50.14.30:20000</INDICATOR> with unauthorized control commands.

## Lateral Movement
SMB connections to <INDICATOR>\\SERVER14\ADMIN$</INDICATOR> using stolen credentials <INDICATOR>user14:pass14</INDICATOR>.

PsExec deployment <INDICATOR>\\192.168.14.0/24</INDICATOR> spreading malware across subnet.

## Data Exfiltration
Upload to <INDICATOR>exfil14.cloud-storage[.]org</INDICATOR> total data <INDICATOR>140 GB</INDICATOR> over <INDICATOR>14</INDICATOR> hour period.

Archive filenames <INDICATOR>data_14_YYYYMMDD.7z</INDICATOR> with password <INDICATOR>Exfil14!</INDICATOR>.

## Credential Theft
NTLM hashes: <INDICATOR>aad3b435b51404eeaad3b435b51404ee:00000000000000000000000003b56f88</INDICATOR> for account <INDICATOR>admin_14</INDICATOR>.

Kerberos ticket <INDICATOR>$krb5tgs$23$*user14$DOMAIN$service14*$[HASH]</INDICATOR>.

## Persistence Mechanisms
Scheduled task <INDICATOR>\Microsoft\Windows\Update14</INDICATOR> runs <INDICATOR>C:\Windows\Temp\svc14.exe</INDICATOR> every <INDICATOR>14</INDICATOR> minutes.

Service name <INDICATOR>WindowsService14</INDICATOR> binary path <INDICATOR>C:\ProgramData\service14.exe</INDICATOR>.

WMI event subscription <INDICATOR>EventFilter14</INDICATOR> with consumer <INDICATOR>CommandLineConsumer14</INDICATOR>.

## Web Indicators
URL pattern <INDICATOR>hxxps://malicious14[.]com/[a-z]{14,20}/payload</INDICATOR>.

Web shell <INDICATOR>shell14.aspx</INDICATOR> deployed to <INDICATOR>C:\inetpub\wwwroot\aspnet_client\shell14.aspx</INDICATOR> hash <INDICATOR>0000000000000000000000000000000000000000000000000000000004a2cb6a</INDICATOR>.

## Mobile/IoT
Android APK <INDICATOR>com.malware.app14</INDICATOR> hash <INDICATOR>000000000000000000000000000000000000000000000000000000000590274c</INDICATOR> requesting dangerous permissions.

IoT firmware <INDICATOR>fw_v14.14.14_modified</INDICATOR> backdoor connecting to <INDICATOR>iot-c214[.]net:8883</INDICATOR>.

## Attribution
**Confidence**: MEDIUM-HIGH - Attribution to <THREAT_ACTOR>Multiple APTs</THREAT_ACTOR> based on infrastructure overlap and TTP analysis.

**Related Campaigns**: <CAMPAIGN>Campaign 14 2024</CAMPAIGN>
**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-14141414</VULNERABILITY>
**Related Malware**: <MALWARE>Malware Family 14</MALWARE>
**Total INDICATOR Instances**: 120+ annotations covering IPs, domains, hashes, registry keys, file paths, network protocols, credentials, and behavioral patterns.
