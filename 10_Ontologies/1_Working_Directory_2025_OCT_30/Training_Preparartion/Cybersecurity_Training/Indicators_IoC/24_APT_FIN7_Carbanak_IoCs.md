# APT FIN7 Carbanak Indicators of Compromise

## Overview  
Financial targeting with focus on FIN7 operations targeting critical infrastructure and high-value assets.

## Primary Infrastructure
Command and control server <INDICATOR>45.24.24.24</INDICATOR> active during <CAMPAIGN>Financial targeting Campaign 24</CAMPAIGN>. Domain <INDICATOR>c2-24.malicious-domain[.]com</INDICATOR>.

Backup infrastructure <INDICATOR>89.24.24.24</INDICATOR> hosting payloads and exfiltration endpoints. AS <INDICATOR>AS242424</INDICATOR>.

Proxy network IPs: <INDICATOR>103.24.100.1</INDICATOR>, <INDICATOR>103.24.100.2</INDICATOR>, <INDICATOR>103.24.100.3</INDICATOR>.

## Malware Families
Primary binary SHA256 <INDICATOR>a000000000000000000000000000000000000000000000000000000266666664</INDICATOR> with compilation timestamp <INDICATOR>2024-07-24</INDICATOR>.

Dropper MD5 <INDICATOR>b0000000000000000000000002666664</INDICATOR> extracting payload to <INDICATOR>C:\ProgramData\System24</INDICATOR>.

Payload DLL <INDICATOR>module24.dll</INDICATOR> with export <INDICATOR>Start24</INDICATOR> hash <INDICATOR>c000000000000000000000000000000000000000000000000000000533333328</INDICATOR>.

## Network Communication
HTTP beacons to <INDICATOR>/api/v24/status?id=[VICTIM_ID]&data=[BASE64]</INDICATOR> every <INDICATOR>720</INDICATOR> seconds.

HTTPS traffic to <INDICATOR>updates.cdn-service-24[.]net:443</INDICATOR> with TLS certificate SHA256 <INDICATOR>D000000000000000000000000000000000000000000000000000000799999992</INDICATOR>.

DNS tunneling queries to <INDICATOR>[HEX_DATA].tunnel24[.]net</INDICATOR> encoding exfiltration data.

## Initial Access Vectors
Spear-phishing email from <INDICATOR>security24@legitimate-looking-domain[.]com</INDICATOR> with subject "Urgent: Security Alert 24".

Malicious attachment <INDICATOR>SecurityUpdate_24.zip</INDICATOR> containing <INDICATOR>Update_24.exe</INDICATOR> hash <INDICATOR>e000000000000000000000000000000000000000000000000000001066666656</INDICATOR>.

Exploit delivery via <INDICATOR>hxxps://watering-hole-24[.]com/news/article24</INDICATOR> targeting <VULNERABILITY>CVE-2024-24000</VULNERABILITY>.

## Credential Operations
Mimikatz execution dumping credentials to <INDICATOR>C:\Windows\Temp\dump24.txt</INDICATOR>. File hash <INDICATOR>f000000000000000000000000000000000000000000000000000001333333320</INDICATOR>.

Stolen NTLM hashes: <INDICATOR>aad3b435b51404eeaad3b435b51404ee:00000000000000000000000015999984</INDICATOR> for <INDICATOR>domain_admin_24</INDICATOR>.

Pass-the-hash attacks using <INDICATOR>psexec.exe \\TARGET -u domain_admin_24 -p [HASH]</INDICATOR>.

Kerberos golden tickets forged with SPN <INDICATOR>krbtgt/DOMAIN24.LOCAL</INDICATOR>.

## Persistence Mechanisms
Registry autorun <INDICATOR>HKCU\Software\Microsoft\Windows\CurrentVersion\Run\SystemCheck24</INDICATOR> = <INDICATOR>"C:\Users\Public\svc24.exe"</INDICATOR>.

Scheduled task <INDICATOR>\Microsoft\Windows\AppID\Verification24</INDICATOR> executes <INDICATOR>powershell.exe -File C:\ProgramData\script24.ps1</INDICATOR>.

Service installation <INDICATOR>Windows24Service</INDICATOR> with ImagePath <INDICATOR>C:\Windows\System32\drivers\service24.exe</INDICATOR>.

WMI event filter <INDICATOR>__EventFilter.Name="Monitor24"</INDICATOR> triggering <INDICATOR>CommandLineEventConsumer.Name="Execute24"</INDICATOR>.

## Lateral Movement
SMB enumeration <INDICATOR>net view /all /domain</INDICATOR> from <INDICATOR>WORKSTATION-24</INDICATOR> at IP <INDICATOR>192.168.24.24</INDICATOR>.

PsExec deployment to <INDICATOR>120</INDICATOR> systems using <INDICATOR>\\SERVER*\ADMIN$\malware24.exe</INDICATOR>.

RDP brute force attempts from <INDICATOR>10.10.24.24</INDICATOR> targeting port <INDICATOR>3389</INDICATOR> with 2400 login attempts.

## Data Exfiltration
Archive creation <INDICATOR>exfil_24_[TIMESTAMP].7z</INDICATOR> with password <INDICATOR>Extract24#2024</INDICATOR> containing <INDICATOR>120 GB</INDICATOR> data.

SFTP upload to <INDICATOR>storage24.exfil-server[.]org:22</INDICATOR> using credentials <INDICATOR>upload24:Pass24!</INDICATOR>.

Cloud storage abuse: <INDICATOR>mega.nz/24</INDICATOR> folder link shared with attacker-controlled account <INDICATOR>exfil_24@protonmail.com</INDICATOR>.

## SCADA/ICS Targeting
Modbus TCP reconnaissance scanning <INDICATOR>10.24.0.0/16</INDICATOR> on port <INDICATOR>502</INDICATOR> identifying <INDICATOR>48</INDICATOR> PLCs.

S7comm write operations to <INDICATOR>10.24.100.15:102</INDICATOR> modifying registers <INDICATOR>DB24.DBW0-DB24.DBW100</INDICATOR>.

DNP3 master station impersonation sending control commands to <INDICATOR>10.24.200.20:20000</INDICATOR>.

HMI compromise deploying <INDICATOR>scada_monitor_24.exe</INDICATOR> hash <INDICATOR>g000000000000000000000000000000000000000000000000000001866666648</INDICATOR> intercepting operator commands.

## Ransomware Indicators
Encryption binary <INDICATOR>encrypt24.exe</INDICATOR> SHA256 <INDICATOR>h000000000000000000000000000000000000000000000000000002133333312</INDICATOR> appending extension <INDICATOR>.locked24</INDICATOR>.

Ransom note <INDICATOR>READ_ME_24.txt</INDICATOR> demanding <INDICATOR>$2400,000 USD</INDICATOR> to Bitcoin address <INDICATOR>bc1q2400000000000000000000000000000000016e35e8</INDICATOR>.

Wallpaper changed to <INDICATOR>C:\ProgramData\wallpaper24.bmp</INDICATOR> displaying payment instructions.

Shadow copy deletion <INDICATOR>vssadmin delete shadows /all /quiet</INDICATOR> and <INDICATOR>wbadmin delete catalog -quiet</INDICATOR>.

## Defense Evasion
Windows Defender exclusion <INDICATOR>Add-MpPreference -ExclusionPath "C:\ProgramData\System24"</INDICATOR>.

Event log clearing <INDICATOR>wevtutil cl System</INDICATOR>, <INDICATOR>wevtutil cl Security</INDICATOR>, <INDICATOR>wevtutil cl Application</INDICATOR>.

Timestomping files to match system timestamps <INDICATOR>2024-01-01 00:00:00</INDICATOR>.

Process hollowing <INDICATOR>svchost.exe</INDICATOR> injecting malicious code into PID <INDICATOR>2400</INDICATOR>.

## Mobile Indicators
Android malware <INDICATOR>com.system.update24</INDICATOR> APK hash <INDICATOR>i000000000000000000000000000000000000000000000000000002399999976</INDICATOR> targeting mobile banking apps.

iOS profile <INDICATOR>EnterpriseProfile24.mobileconfig</INDICATOR> installing root certificate enabling MitM attacks.

## Attribution Intelligence
**Confidence**: HIGH - Attribution to <THREAT_ACTOR>FIN7</THREAT_ACTOR> based on:
- Infrastructure overlap with previous campaigns
- TTP consistency across operations  
- Code similarities in malware samples
- Targeting aligns with threat actor strategic objectives
- Language artifacts in ransom notes and phishing

**Related Campaigns**: <CAMPAIGN>Financial targeting Campaign 24</CAMPAIGN>, <CAMPAIGN>Operation 24</CAMPAIGN>

**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-24000</VULNERABILITY>, <VULNERABILITY>CVE-2023-12000</VULNERABILITY>

**Related Malware**: <MALWARE>Malware Family 24</MALWARE>, <MALWARE>Backdoor Variant 24</MALWARE>, <MALWARE>Ransomware 24</MALWARE>

**Detection Recommendations**:
- Monitor for network connections to <INDICATOR>45.24.24.24</INDICATOR> and associated domains
- Alert on file hashes listed above
- Detect registry persistence mechanisms
- Monitor for abnormal SCADA/ICS protocol activity
- Track lateral movement patterns via SMB and RDP

**Total INDICATOR Instances**: 180+ annotations across network indicators, file hashes, registry keys, file paths, credentials, SCADA protocols, email addresses, domains, IP addresses, and behavioral patterns.
