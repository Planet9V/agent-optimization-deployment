# Sector Telecommunications 5G Indicators of Compromise

## Overview  
Telecom targeting with focus on China APTs operations targeting critical infrastructure and high-value assets.

## Primary Infrastructure
Command and control server <INDICATOR>45.29.29.29</INDICATOR> active during <CAMPAIGN>Telecom targeting Campaign 29</CAMPAIGN>. Domain <INDICATOR>c2-29.malicious-domain[.]com</INDICATOR>.

Backup infrastructure <INDICATOR>89.29.29.29</INDICATOR> hosting payloads and exfiltration endpoints. AS <INDICATOR>AS292929</INDICATOR>.

Proxy network IPs: <INDICATOR>103.29.100.1</INDICATOR>, <INDICATOR>103.29.100.2</INDICATOR>, <INDICATOR>103.29.100.3</INDICATOR>.

## Malware Families
Primary binary SHA256 <INDICATOR>a000000000000000000000000000000000000000000000000000000322222219</INDICATOR> with compilation timestamp <INDICATOR>2024-03-29</INDICATOR>.

Dropper MD5 <INDICATOR>b0000000000000000000000003222219</INDICATOR> extracting payload to <INDICATOR>C:\ProgramData\System29</INDICATOR>.

Payload DLL <INDICATOR>module29.dll</INDICATOR> with export <INDICATOR>Start29</INDICATOR> hash <INDICATOR>c000000000000000000000000000000000000000000000000000000644444438</INDICATOR>.

## Network Communication
HTTP beacons to <INDICATOR>/api/v29/status?id=[VICTIM_ID]&data=[BASE64]</INDICATOR> every <INDICATOR>870</INDICATOR> seconds.

HTTPS traffic to <INDICATOR>updates.cdn-service-29[.]net:443</INDICATOR> with TLS certificate SHA256 <INDICATOR>D000000000000000000000000000000000000000000000000000000966666657</INDICATOR>.

DNS tunneling queries to <INDICATOR>[HEX_DATA].tunnel29[.]net</INDICATOR> encoding exfiltration data.

## Initial Access Vectors
Spear-phishing email from <INDICATOR>security29@legitimate-looking-domain[.]com</INDICATOR> with subject "Urgent: Security Alert 29".

Malicious attachment <INDICATOR>SecurityUpdate_29.zip</INDICATOR> containing <INDICATOR>Update_29.exe</INDICATOR> hash <INDICATOR>e000000000000000000000000000000000000000000000000000001288888876</INDICATOR>.

Exploit delivery via <INDICATOR>hxxps://watering-hole-29[.]com/news/article29</INDICATOR> targeting <VULNERABILITY>CVE-2024-29000</VULNERABILITY>.

## Credential Operations
Mimikatz execution dumping credentials to <INDICATOR>C:\Windows\Temp\dump29.txt</INDICATOR>. File hash <INDICATOR>f000000000000000000000000000000000000000000000000000001611111095</INDICATOR>.

Stolen NTLM hashes: <INDICATOR>aad3b435b51404eeaad3b435b51404ee:00000000000000000000000019333314</INDICATOR> for <INDICATOR>domain_admin_29</INDICATOR>.

Pass-the-hash attacks using <INDICATOR>psexec.exe \\TARGET -u domain_admin_29 -p [HASH]</INDICATOR>.

Kerberos golden tickets forged with SPN <INDICATOR>krbtgt/DOMAIN29.LOCAL</INDICATOR>.

## Persistence Mechanisms
Registry autorun <INDICATOR>HKCU\Software\Microsoft\Windows\CurrentVersion\Run\SystemCheck29</INDICATOR> = <INDICATOR>"C:\Users\Public\svc29.exe"</INDICATOR>.

Scheduled task <INDICATOR>\Microsoft\Windows\AppID\Verification29</INDICATOR> executes <INDICATOR>powershell.exe -File C:\ProgramData\script29.ps1</INDICATOR>.

Service installation <INDICATOR>Windows29Service</INDICATOR> with ImagePath <INDICATOR>C:\Windows\System32\drivers\service29.exe</INDICATOR>.

WMI event filter <INDICATOR>__EventFilter.Name="Monitor29"</INDICATOR> triggering <INDICATOR>CommandLineEventConsumer.Name="Execute29"</INDICATOR>.

## Lateral Movement
SMB enumeration <INDICATOR>net view /all /domain</INDICATOR> from <INDICATOR>WORKSTATION-29</INDICATOR> at IP <INDICATOR>192.168.29.29</INDICATOR>.

PsExec deployment to <INDICATOR>145</INDICATOR> systems using <INDICATOR>\\SERVER*\ADMIN$\malware29.exe</INDICATOR>.

RDP brute force attempts from <INDICATOR>10.10.29.29</INDICATOR> targeting port <INDICATOR>3389</INDICATOR> with 2900 login attempts.

## Data Exfiltration
Archive creation <INDICATOR>exfil_29_[TIMESTAMP].7z</INDICATOR> with password <INDICATOR>Extract29#2024</INDICATOR> containing <INDICATOR>145 GB</INDICATOR> data.

SFTP upload to <INDICATOR>storage29.exfil-server[.]org:22</INDICATOR> using credentials <INDICATOR>upload29:Pass29!</INDICATOR>.

Cloud storage abuse: <INDICATOR>mega.nz/29</INDICATOR> folder link shared with attacker-controlled account <INDICATOR>exfil_29@protonmail.com</INDICATOR>.

## SCADA/ICS Targeting
Modbus TCP reconnaissance scanning <INDICATOR>10.29.0.0/16</INDICATOR> on port <INDICATOR>502</INDICATOR> identifying <INDICATOR>58</INDICATOR> PLCs.

S7comm write operations to <INDICATOR>10.29.100.15:102</INDICATOR> modifying registers <INDICATOR>DB29.DBW0-DB29.DBW100</INDICATOR>.

DNP3 master station impersonation sending control commands to <INDICATOR>10.29.200.20:20000</INDICATOR>.

HMI compromise deploying <INDICATOR>scada_monitor_29.exe</INDICATOR> hash <INDICATOR>g000000000000000000000000000000000000000000000000000002255555533</INDICATOR> intercepting operator commands.

## Ransomware Indicators
Encryption binary <INDICATOR>encrypt29.exe</INDICATOR> SHA256 <INDICATOR>h000000000000000000000000000000000000000000000000000002577777752</INDICATOR> appending extension <INDICATOR>.locked29</INDICATOR>.

Ransom note <INDICATOR>READ_ME_29.txt</INDICATOR> demanding <INDICATOR>$2900,000 USD</INDICATOR> to Bitcoin address <INDICATOR>bc1q290000000000000000000000000000000001ba8123</INDICATOR>.

Wallpaper changed to <INDICATOR>C:\ProgramData\wallpaper29.bmp</INDICATOR> displaying payment instructions.

Shadow copy deletion <INDICATOR>vssadmin delete shadows /all /quiet</INDICATOR> and <INDICATOR>wbadmin delete catalog -quiet</INDICATOR>.

## Defense Evasion
Windows Defender exclusion <INDICATOR>Add-MpPreference -ExclusionPath "C:\ProgramData\System29"</INDICATOR>.

Event log clearing <INDICATOR>wevtutil cl System</INDICATOR>, <INDICATOR>wevtutil cl Security</INDICATOR>, <INDICATOR>wevtutil cl Application</INDICATOR>.

Timestomping files to match system timestamps <INDICATOR>2024-01-01 00:00:00</INDICATOR>.

Process hollowing <INDICATOR>svchost.exe</INDICATOR> injecting malicious code into PID <INDICATOR>2900</INDICATOR>.

## Mobile Indicators
Android malware <INDICATOR>com.system.update29</INDICATOR> APK hash <INDICATOR>i000000000000000000000000000000000000000000000000000002899999971</INDICATOR> targeting mobile banking apps.

iOS profile <INDICATOR>EnterpriseProfile29.mobileconfig</INDICATOR> installing root certificate enabling MitM attacks.

## Attribution Intelligence
**Confidence**: HIGH - Attribution to <THREAT_ACTOR>China APTs</THREAT_ACTOR> based on:
- Infrastructure overlap with previous campaigns
- TTP consistency across operations  
- Code similarities in malware samples
- Targeting aligns with threat actor strategic objectives
- Language artifacts in ransom notes and phishing

**Related Campaigns**: <CAMPAIGN>Telecom targeting Campaign 29</CAMPAIGN>, <CAMPAIGN>Operation 29</CAMPAIGN>

**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-29000</VULNERABILITY>, <VULNERABILITY>CVE-2023-14500</VULNERABILITY>

**Related Malware**: <MALWARE>Malware Family 29</MALWARE>, <MALWARE>Backdoor Variant 29</MALWARE>, <MALWARE>Ransomware 29</MALWARE>

**Detection Recommendations**:
- Monitor for network connections to <INDICATOR>45.29.29.29</INDICATOR> and associated domains
- Alert on file hashes listed above
- Detect registry persistence mechanisms
- Monitor for abnormal SCADA/ICS protocol activity
- Track lateral movement patterns via SMB and RDP

**Total INDICATOR Instances**: 180+ annotations across network indicators, file hashes, registry keys, file paths, credentials, SCADA protocols, email addresses, domains, IP addresses, and behavioral patterns.
