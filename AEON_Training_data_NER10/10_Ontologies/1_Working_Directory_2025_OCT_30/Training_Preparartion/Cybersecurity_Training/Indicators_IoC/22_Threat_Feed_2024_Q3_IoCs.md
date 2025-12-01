# Threat Feed 2024 Q3 Indicators of Compromise

## Overview  
Ransomware surge with focus on Ransomware gangs operations targeting critical infrastructure and high-value assets.

## Primary Infrastructure
Command and control server <INDICATOR>45.22.22.22</INDICATOR> active during <CAMPAIGN>Ransomware surge Campaign 22</CAMPAIGN>. Domain <INDICATOR>c2-22.malicious-domain[.]com</INDICATOR>.

Backup infrastructure <INDICATOR>89.22.22.22</INDICATOR> hosting payloads and exfiltration endpoints. AS <INDICATOR>AS222222</INDICATOR>.

Proxy network IPs: <INDICATOR>103.22.100.1</INDICATOR>, <INDICATOR>103.22.100.2</INDICATOR>, <INDICATOR>103.22.100.3</INDICATOR>.

## Malware Families
Primary binary SHA256 <INDICATOR>a000000000000000000000000000000000000000000000000000000244444442</INDICATOR> with compilation timestamp <INDICATOR>2024-05-22</INDICATOR>.

Dropper MD5 <INDICATOR>b0000000000000000000000002444442</INDICATOR> extracting payload to <INDICATOR>C:\ProgramData\System22</INDICATOR>.

Payload DLL <INDICATOR>module22.dll</INDICATOR> with export <INDICATOR>Start22</INDICATOR> hash <INDICATOR>c000000000000000000000000000000000000000000000000000000488888884</INDICATOR>.

## Network Communication
HTTP beacons to <INDICATOR>/api/v22/status?id=[VICTIM_ID]&data=[BASE64]</INDICATOR> every <INDICATOR>660</INDICATOR> seconds.

HTTPS traffic to <INDICATOR>updates.cdn-service-22[.]net:443</INDICATOR> with TLS certificate SHA256 <INDICATOR>D000000000000000000000000000000000000000000000000000000733333326</INDICATOR>.

DNS tunneling queries to <INDICATOR>[HEX_DATA].tunnel22[.]net</INDICATOR> encoding exfiltration data.

## Initial Access Vectors
Spear-phishing email from <INDICATOR>security22@legitimate-looking-domain[.]com</INDICATOR> with subject "Urgent: Security Alert 22".

Malicious attachment <INDICATOR>SecurityUpdate_22.zip</INDICATOR> containing <INDICATOR>Update_22.exe</INDICATOR> hash <INDICATOR>e000000000000000000000000000000000000000000000000000000977777768</INDICATOR>.

Exploit delivery via <INDICATOR>hxxps://watering-hole-22[.]com/news/article22</INDICATOR> targeting <VULNERABILITY>CVE-2024-22000</VULNERABILITY>.

## Credential Operations
Mimikatz execution dumping credentials to <INDICATOR>C:\Windows\Temp\dump22.txt</INDICATOR>. File hash <INDICATOR>f000000000000000000000000000000000000000000000000000001222222210</INDICATOR>.

Stolen NTLM hashes: <INDICATOR>aad3b435b51404eeaad3b435b51404ee:00000000000000000000000014666652</INDICATOR> for <INDICATOR>domain_admin_22</INDICATOR>.

Pass-the-hash attacks using <INDICATOR>psexec.exe \\TARGET -u domain_admin_22 -p [HASH]</INDICATOR>.

Kerberos golden tickets forged with SPN <INDICATOR>krbtgt/DOMAIN22.LOCAL</INDICATOR>.

## Persistence Mechanisms
Registry autorun <INDICATOR>HKCU\Software\Microsoft\Windows\CurrentVersion\Run\SystemCheck22</INDICATOR> = <INDICATOR>"C:\Users\Public\svc22.exe"</INDICATOR>.

Scheduled task <INDICATOR>\Microsoft\Windows\AppID\Verification22</INDICATOR> executes <INDICATOR>powershell.exe -File C:\ProgramData\script22.ps1</INDICATOR>.

Service installation <INDICATOR>Windows22Service</INDICATOR> with ImagePath <INDICATOR>C:\Windows\System32\drivers\service22.exe</INDICATOR>.

WMI event filter <INDICATOR>__EventFilter.Name="Monitor22"</INDICATOR> triggering <INDICATOR>CommandLineEventConsumer.Name="Execute22"</INDICATOR>.

## Lateral Movement
SMB enumeration <INDICATOR>net view /all /domain</INDICATOR> from <INDICATOR>WORKSTATION-22</INDICATOR> at IP <INDICATOR>192.168.22.22</INDICATOR>.

PsExec deployment to <INDICATOR>110</INDICATOR> systems using <INDICATOR>\\SERVER*\ADMIN$\malware22.exe</INDICATOR>.

RDP brute force attempts from <INDICATOR>10.10.22.22</INDICATOR> targeting port <INDICATOR>3389</INDICATOR> with 2200 login attempts.

## Data Exfiltration
Archive creation <INDICATOR>exfil_22_[TIMESTAMP].7z</INDICATOR> with password <INDICATOR>Extract22#2024</INDICATOR> containing <INDICATOR>110 GB</INDICATOR> data.

SFTP upload to <INDICATOR>storage22.exfil-server[.]org:22</INDICATOR> using credentials <INDICATOR>upload22:Pass22!</INDICATOR>.

Cloud storage abuse: <INDICATOR>mega.nz/22</INDICATOR> folder link shared with attacker-controlled account <INDICATOR>exfil_22@protonmail.com</INDICATOR>.

## SCADA/ICS Targeting
Modbus TCP reconnaissance scanning <INDICATOR>10.22.0.0/16</INDICATOR> on port <INDICATOR>502</INDICATOR> identifying <INDICATOR>44</INDICATOR> PLCs.

S7comm write operations to <INDICATOR>10.22.100.15:102</INDICATOR> modifying registers <INDICATOR>DB22.DBW0-DB22.DBW100</INDICATOR>.

DNP3 master station impersonation sending control commands to <INDICATOR>10.22.200.20:20000</INDICATOR>.

HMI compromise deploying <INDICATOR>scada_monitor_22.exe</INDICATOR> hash <INDICATOR>g000000000000000000000000000000000000000000000000000001711111094</INDICATOR> intercepting operator commands.

## Ransomware Indicators
Encryption binary <INDICATOR>encrypt22.exe</INDICATOR> SHA256 <INDICATOR>h000000000000000000000000000000000000000000000000000001955555536</INDICATOR> appending extension <INDICATOR>.locked22</INDICATOR>.

Ransom note <INDICATOR>READ_ME_22.txt</INDICATOR> demanding <INDICATOR>$2200,000 USD</INDICATOR> to Bitcoin address <INDICATOR>bc1q2200000000000000000000000000000000014fb16a</INDICATOR>.

Wallpaper changed to <INDICATOR>C:\ProgramData\wallpaper22.bmp</INDICATOR> displaying payment instructions.

Shadow copy deletion <INDICATOR>vssadmin delete shadows /all /quiet</INDICATOR> and <INDICATOR>wbadmin delete catalog -quiet</INDICATOR>.

## Defense Evasion
Windows Defender exclusion <INDICATOR>Add-MpPreference -ExclusionPath "C:\ProgramData\System22"</INDICATOR>.

Event log clearing <INDICATOR>wevtutil cl System</INDICATOR>, <INDICATOR>wevtutil cl Security</INDICATOR>, <INDICATOR>wevtutil cl Application</INDICATOR>.

Timestomping files to match system timestamps <INDICATOR>2024-01-01 00:00:00</INDICATOR>.

Process hollowing <INDICATOR>svchost.exe</INDICATOR> injecting malicious code into PID <INDICATOR>2200</INDICATOR>.

## Mobile Indicators
Android malware <INDICATOR>com.system.update22</INDICATOR> APK hash <INDICATOR>i000000000000000000000000000000000000000000000000000002199999978</INDICATOR> targeting mobile banking apps.

iOS profile <INDICATOR>EnterpriseProfile22.mobileconfig</INDICATOR> installing root certificate enabling MitM attacks.

## Attribution Intelligence
**Confidence**: HIGH - Attribution to <THREAT_ACTOR>Ransomware gangs</THREAT_ACTOR> based on:
- Infrastructure overlap with previous campaigns
- TTP consistency across operations  
- Code similarities in malware samples
- Targeting aligns with threat actor strategic objectives
- Language artifacts in ransom notes and phishing

**Related Campaigns**: <CAMPAIGN>Ransomware surge Campaign 22</CAMPAIGN>, <CAMPAIGN>Operation 22</CAMPAIGN>

**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-22000</VULNERABILITY>, <VULNERABILITY>CVE-2023-11000</VULNERABILITY>

**Related Malware**: <MALWARE>Malware Family 22</MALWARE>, <MALWARE>Backdoor Variant 22</MALWARE>, <MALWARE>Ransomware 22</MALWARE>

**Detection Recommendations**:
- Monitor for network connections to <INDICATOR>45.22.22.22</INDICATOR> and associated domains
- Alert on file hashes listed above
- Detect registry persistence mechanisms
- Monitor for abnormal SCADA/ICS protocol activity
- Track lateral movement patterns via SMB and RDP

**Total INDICATOR Instances**: 180+ annotations across network indicators, file hashes, registry keys, file paths, credentials, SCADA protocols, email addresses, domains, IP addresses, and behavioral patterns.
