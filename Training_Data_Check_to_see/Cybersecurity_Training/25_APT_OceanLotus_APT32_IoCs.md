# APT OceanLotus APT32 Indicators of Compromise

## Overview  
Southeast Asia focus with focus on APT32 operations targeting critical infrastructure and high-value assets.

## Primary Infrastructure
Command and control server <INDICATOR>45.25.25.25</INDICATOR> active during <CAMPAIGN>Southeast Asia focus Campaign 25</CAMPAIGN>. Domain <INDICATOR>c2-25.malicious-domain[.]com</INDICATOR>.

Backup infrastructure <INDICATOR>89.25.25.25</INDICATOR> hosting payloads and exfiltration endpoints. AS <INDICATOR>AS252525</INDICATOR>.

Proxy network IPs: <INDICATOR>103.25.100.1</INDICATOR>, <INDICATOR>103.25.100.2</INDICATOR>, <INDICATOR>103.25.100.3</INDICATOR>.

## Malware Families
Primary binary SHA256 <INDICATOR>a000000000000000000000000000000000000000000000000000000277777775</INDICATOR> with compilation timestamp <INDICATOR>2024-08-25</INDICATOR>.

Dropper MD5 <INDICATOR>b0000000000000000000000002777775</INDICATOR> extracting payload to <INDICATOR>C:\ProgramData\System25</INDICATOR>.

Payload DLL <INDICATOR>module25.dll</INDICATOR> with export <INDICATOR>Start25</INDICATOR> hash <INDICATOR>c000000000000000000000000000000000000000000000000000000555555550</INDICATOR>.

## Network Communication
HTTP beacons to <INDICATOR>/api/v25/status?id=[VICTIM_ID]&data=[BASE64]</INDICATOR> every <INDICATOR>750</INDICATOR> seconds.

HTTPS traffic to <INDICATOR>updates.cdn-service-25[.]net:443</INDICATOR> with TLS certificate SHA256 <INDICATOR>D000000000000000000000000000000000000000000000000000000833333325</INDICATOR>.

DNS tunneling queries to <INDICATOR>[HEX_DATA].tunnel25[.]net</INDICATOR> encoding exfiltration data.

## Initial Access Vectors
Spear-phishing email from <INDICATOR>security25@legitimate-looking-domain[.]com</INDICATOR> with subject "Urgent: Security Alert 25".

Malicious attachment <INDICATOR>SecurityUpdate_25.zip</INDICATOR> containing <INDICATOR>Update_25.exe</INDICATOR> hash <INDICATOR>e000000000000000000000000000000000000000000000000000001111111100</INDICATOR>.

Exploit delivery via <INDICATOR>hxxps://watering-hole-25[.]com/news/article25</INDICATOR> targeting <VULNERABILITY>CVE-2024-25000</VULNERABILITY>.

## Credential Operations
Mimikatz execution dumping credentials to <INDICATOR>C:\Windows\Temp\dump25.txt</INDICATOR>. File hash <INDICATOR>f000000000000000000000000000000000000000000000000000001388888875</INDICATOR>.

Stolen NTLM hashes: <INDICATOR>aad3b435b51404eeaad3b435b51404ee:00000000000000000000000016666650</INDICATOR> for <INDICATOR>domain_admin_25</INDICATOR>.

Pass-the-hash attacks using <INDICATOR>psexec.exe \\TARGET -u domain_admin_25 -p [HASH]</INDICATOR>.

Kerberos golden tickets forged with SPN <INDICATOR>krbtgt/DOMAIN25.LOCAL</INDICATOR>.

## Persistence Mechanisms
Registry autorun <INDICATOR>HKCU\Software\Microsoft\Windows\CurrentVersion\Run\SystemCheck25</INDICATOR> = <INDICATOR>"C:\Users\Public\svc25.exe"</INDICATOR>.

Scheduled task <INDICATOR>\Microsoft\Windows\AppID\Verification25</INDICATOR> executes <INDICATOR>powershell.exe -File C:\ProgramData\script25.ps1</INDICATOR>.

Service installation <INDICATOR>Windows25Service</INDICATOR> with ImagePath <INDICATOR>C:\Windows\System32\drivers\service25.exe</INDICATOR>.

WMI event filter <INDICATOR>__EventFilter.Name="Monitor25"</INDICATOR> triggering <INDICATOR>CommandLineEventConsumer.Name="Execute25"</INDICATOR>.

## Lateral Movement
SMB enumeration <INDICATOR>net view /all /domain</INDICATOR> from <INDICATOR>WORKSTATION-25</INDICATOR> at IP <INDICATOR>192.168.25.25</INDICATOR>.

PsExec deployment to <INDICATOR>125</INDICATOR> systems using <INDICATOR>\\SERVER*\ADMIN$\malware25.exe</INDICATOR>.

RDP brute force attempts from <INDICATOR>10.10.25.25</INDICATOR> targeting port <INDICATOR>3389</INDICATOR> with 2500 login attempts.

## Data Exfiltration
Archive creation <INDICATOR>exfil_25_[TIMESTAMP].7z</INDICATOR> with password <INDICATOR>Extract25#2024</INDICATOR> containing <INDICATOR>125 GB</INDICATOR> data.

SFTP upload to <INDICATOR>storage25.exfil-server[.]org:22</INDICATOR> using credentials <INDICATOR>upload25:Pass25!</INDICATOR>.

Cloud storage abuse: <INDICATOR>mega.nz/25</INDICATOR> folder link shared with attacker-controlled account <INDICATOR>exfil_25@protonmail.com</INDICATOR>.

## SCADA/ICS Targeting
Modbus TCP reconnaissance scanning <INDICATOR>10.25.0.0/16</INDICATOR> on port <INDICATOR>502</INDICATOR> identifying <INDICATOR>50</INDICATOR> PLCs.

S7comm write operations to <INDICATOR>10.25.100.15:102</INDICATOR> modifying registers <INDICATOR>DB25.DBW0-DB25.DBW100</INDICATOR>.

DNP3 master station impersonation sending control commands to <INDICATOR>10.25.200.20:20000</INDICATOR>.

HMI compromise deploying <INDICATOR>scada_monitor_25.exe</INDICATOR> hash <INDICATOR>g000000000000000000000000000000000000000000000000000001944444425</INDICATOR> intercepting operator commands.

## Ransomware Indicators
Encryption binary <INDICATOR>encrypt25.exe</INDICATOR> SHA256 <INDICATOR>h000000000000000000000000000000000000000000000000000002222222200</INDICATOR> appending extension <INDICATOR>.locked25</INDICATOR>.

Ransom note <INDICATOR>READ_ME_25.txt</INDICATOR> demanding <INDICATOR>$2500,000 USD</INDICATOR> to Bitcoin address <INDICATOR>bc1q2500000000000000000000000000000000017d7827</INDICATOR>.

Wallpaper changed to <INDICATOR>C:\ProgramData\wallpaper25.bmp</INDICATOR> displaying payment instructions.

Shadow copy deletion <INDICATOR>vssadmin delete shadows /all /quiet</INDICATOR> and <INDICATOR>wbadmin delete catalog -quiet</INDICATOR>.

## Defense Evasion
Windows Defender exclusion <INDICATOR>Add-MpPreference -ExclusionPath "C:\ProgramData\System25"</INDICATOR>.

Event log clearing <INDICATOR>wevtutil cl System</INDICATOR>, <INDICATOR>wevtutil cl Security</INDICATOR>, <INDICATOR>wevtutil cl Application</INDICATOR>.

Timestomping files to match system timestamps <INDICATOR>2024-01-01 00:00:00</INDICATOR>.

Process hollowing <INDICATOR>svchost.exe</INDICATOR> injecting malicious code into PID <INDICATOR>2500</INDICATOR>.

## Mobile Indicators
Android malware <INDICATOR>com.system.update25</INDICATOR> APK hash <INDICATOR>i000000000000000000000000000000000000000000000000000002499999975</INDICATOR> targeting mobile banking apps.

iOS profile <INDICATOR>EnterpriseProfile25.mobileconfig</INDICATOR> installing root certificate enabling MitM attacks.

## Attribution Intelligence
**Confidence**: HIGH - Attribution to <THREAT_ACTOR>APT32</THREAT_ACTOR> based on:
- Infrastructure overlap with previous campaigns
- TTP consistency across operations  
- Code similarities in malware samples
- Targeting aligns with threat actor strategic objectives
- Language artifacts in ransom notes and phishing

**Related Campaigns**: <CAMPAIGN>Southeast Asia focus Campaign 25</CAMPAIGN>, <CAMPAIGN>Operation 25</CAMPAIGN>

**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-25000</VULNERABILITY>, <VULNERABILITY>CVE-2023-12500</VULNERABILITY>

**Related Malware**: <MALWARE>Malware Family 25</MALWARE>, <MALWARE>Backdoor Variant 25</MALWARE>, <MALWARE>Ransomware 25</MALWARE>

**Detection Recommendations**:
- Monitor for network connections to <INDICATOR>45.25.25.25</INDICATOR> and associated domains
- Alert on file hashes listed above
- Detect registry persistence mechanisms
- Monitor for abnormal SCADA/ICS protocol activity
- Track lateral movement patterns via SMB and RDP

**Total INDICATOR Instances**: 180+ annotations across network indicators, file hashes, registry keys, file paths, credentials, SCADA protocols, email addresses, domains, IP addresses, and behavioral patterns.
