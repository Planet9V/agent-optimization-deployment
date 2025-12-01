# Threat Feed 2024 Q2 Indicators of Compromise

## Overview  
APT activity with focus on Multiple APTs operations targeting critical infrastructure and high-value assets.

## Primary Infrastructure
Command and control server <INDICATOR>45.21.21.21</INDICATOR> active during <CAMPAIGN>APT activity Campaign 21</CAMPAIGN>. Domain <INDICATOR>c2-21.malicious-domain[.]com</INDICATOR>.

Backup infrastructure <INDICATOR>89.21.21.21</INDICATOR> hosting payloads and exfiltration endpoints. AS <INDICATOR>AS212121</INDICATOR>.

Proxy network IPs: <INDICATOR>103.21.100.1</INDICATOR>, <INDICATOR>103.21.100.2</INDICATOR>, <INDICATOR>103.21.100.3</INDICATOR>.

## Malware Families
Primary binary SHA256 <INDICATOR>a000000000000000000000000000000000000000000000000000000233333331</INDICATOR> with compilation timestamp <INDICATOR>2024-04-21</INDICATOR>.

Dropper MD5 <INDICATOR>b0000000000000000000000002333331</INDICATOR> extracting payload to <INDICATOR>C:\ProgramData\System21</INDICATOR>.

Payload DLL <INDICATOR>module21.dll</INDICATOR> with export <INDICATOR>Start21</INDICATOR> hash <INDICATOR>c000000000000000000000000000000000000000000000000000000466666662</INDICATOR>.

## Network Communication
HTTP beacons to <INDICATOR>/api/v21/status?id=[VICTIM_ID]&data=[BASE64]</INDICATOR> every <INDICATOR>630</INDICATOR> seconds.

HTTPS traffic to <INDICATOR>updates.cdn-service-21[.]net:443</INDICATOR> with TLS certificate SHA256 <INDICATOR>D000000000000000000000000000000000000000000000000000000699999993</INDICATOR>.

DNS tunneling queries to <INDICATOR>[HEX_DATA].tunnel21[.]net</INDICATOR> encoding exfiltration data.

## Initial Access Vectors
Spear-phishing email from <INDICATOR>security21@legitimate-looking-domain[.]com</INDICATOR> with subject "Urgent: Security Alert 21".

Malicious attachment <INDICATOR>SecurityUpdate_21.zip</INDICATOR> containing <INDICATOR>Update_21.exe</INDICATOR> hash <INDICATOR>e000000000000000000000000000000000000000000000000000000933333324</INDICATOR>.

Exploit delivery via <INDICATOR>hxxps://watering-hole-21[.]com/news/article21</INDICATOR> targeting <VULNERABILITY>CVE-2024-21000</VULNERABILITY>.

## Credential Operations
Mimikatz execution dumping credentials to <INDICATOR>C:\Windows\Temp\dump21.txt</INDICATOR>. File hash <INDICATOR>f000000000000000000000000000000000000000000000000000001166666655</INDICATOR>.

Stolen NTLM hashes: <INDICATOR>aad3b435b51404eeaad3b435b51404ee:00000000000000000000000013999986</INDICATOR> for <INDICATOR>domain_admin_21</INDICATOR>.

Pass-the-hash attacks using <INDICATOR>psexec.exe \\TARGET -u domain_admin_21 -p [HASH]</INDICATOR>.

Kerberos golden tickets forged with SPN <INDICATOR>krbtgt/DOMAIN21.LOCAL</INDICATOR>.

## Persistence Mechanisms
Registry autorun <INDICATOR>HKCU\Software\Microsoft\Windows\CurrentVersion\Run\SystemCheck21</INDICATOR> = <INDICATOR>"C:\Users\Public\svc21.exe"</INDICATOR>.

Scheduled task <INDICATOR>\Microsoft\Windows\AppID\Verification21</INDICATOR> executes <INDICATOR>powershell.exe -File C:\ProgramData\script21.ps1</INDICATOR>.

Service installation <INDICATOR>Windows21Service</INDICATOR> with ImagePath <INDICATOR>C:\Windows\System32\drivers\service21.exe</INDICATOR>.

WMI event filter <INDICATOR>__EventFilter.Name="Monitor21"</INDICATOR> triggering <INDICATOR>CommandLineEventConsumer.Name="Execute21"</INDICATOR>.

## Lateral Movement
SMB enumeration <INDICATOR>net view /all /domain</INDICATOR> from <INDICATOR>WORKSTATION-21</INDICATOR> at IP <INDICATOR>192.168.21.21</INDICATOR>.

PsExec deployment to <INDICATOR>105</INDICATOR> systems using <INDICATOR>\\SERVER*\ADMIN$\malware21.exe</INDICATOR>.

RDP brute force attempts from <INDICATOR>10.10.21.21</INDICATOR> targeting port <INDICATOR>3389</INDICATOR> with 2100 login attempts.

## Data Exfiltration
Archive creation <INDICATOR>exfil_21_[TIMESTAMP].7z</INDICATOR> with password <INDICATOR>Extract21#2024</INDICATOR> containing <INDICATOR>105 GB</INDICATOR> data.

SFTP upload to <INDICATOR>storage21.exfil-server[.]org:22</INDICATOR> using credentials <INDICATOR>upload21:Pass21!</INDICATOR>.

Cloud storage abuse: <INDICATOR>mega.nz/21</INDICATOR> folder link shared with attacker-controlled account <INDICATOR>exfil_21@protonmail.com</INDICATOR>.

## SCADA/ICS Targeting
Modbus TCP reconnaissance scanning <INDICATOR>10.21.0.0/16</INDICATOR> on port <INDICATOR>502</INDICATOR> identifying <INDICATOR>42</INDICATOR> PLCs.

S7comm write operations to <INDICATOR>10.21.100.15:102</INDICATOR> modifying registers <INDICATOR>DB21.DBW0-DB21.DBW100</INDICATOR>.

DNP3 master station impersonation sending control commands to <INDICATOR>10.21.200.20:20000</INDICATOR>.

HMI compromise deploying <INDICATOR>scada_monitor_21.exe</INDICATOR> hash <INDICATOR>g000000000000000000000000000000000000000000000000000001633333317</INDICATOR> intercepting operator commands.

## Ransomware Indicators
Encryption binary <INDICATOR>encrypt21.exe</INDICATOR> SHA256 <INDICATOR>h000000000000000000000000000000000000000000000000000001866666648</INDICATOR> appending extension <INDICATOR>.locked21</INDICATOR>.

Ransom note <INDICATOR>READ_ME_21.txt</INDICATOR> demanding <INDICATOR>$2100,000 USD</INDICATOR> to Bitcoin address <INDICATOR>bc1q210000000000000000000000000000000001406f2b</INDICATOR>.

Wallpaper changed to <INDICATOR>C:\ProgramData\wallpaper21.bmp</INDICATOR> displaying payment instructions.

Shadow copy deletion <INDICATOR>vssadmin delete shadows /all /quiet</INDICATOR> and <INDICATOR>wbadmin delete catalog -quiet</INDICATOR>.

## Defense Evasion
Windows Defender exclusion <INDICATOR>Add-MpPreference -ExclusionPath "C:\ProgramData\System21"</INDICATOR>.

Event log clearing <INDICATOR>wevtutil cl System</INDICATOR>, <INDICATOR>wevtutil cl Security</INDICATOR>, <INDICATOR>wevtutil cl Application</INDICATOR>.

Timestomping files to match system timestamps <INDICATOR>2024-01-01 00:00:00</INDICATOR>.

Process hollowing <INDICATOR>svchost.exe</INDICATOR> injecting malicious code into PID <INDICATOR>2100</INDICATOR>.

## Mobile Indicators
Android malware <INDICATOR>com.system.update21</INDICATOR> APK hash <INDICATOR>i000000000000000000000000000000000000000000000000000002099999979</INDICATOR> targeting mobile banking apps.

iOS profile <INDICATOR>EnterpriseProfile21.mobileconfig</INDICATOR> installing root certificate enabling MitM attacks.

## Attribution Intelligence
**Confidence**: HIGH - Attribution to <THREAT_ACTOR>Multiple APTs</THREAT_ACTOR> based on:
- Infrastructure overlap with previous campaigns
- TTP consistency across operations  
- Code similarities in malware samples
- Targeting aligns with threat actor strategic objectives
- Language artifacts in ransom notes and phishing

**Related Campaigns**: <CAMPAIGN>APT activity Campaign 21</CAMPAIGN>, <CAMPAIGN>Operation 21</CAMPAIGN>

**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-21000</VULNERABILITY>, <VULNERABILITY>CVE-2023-10500</VULNERABILITY>

**Related Malware**: <MALWARE>Malware Family 21</MALWARE>, <MALWARE>Backdoor Variant 21</MALWARE>, <MALWARE>Ransomware 21</MALWARE>

**Detection Recommendations**:
- Monitor for network connections to <INDICATOR>45.21.21.21</INDICATOR> and associated domains
- Alert on file hashes listed above
- Detect registry persistence mechanisms
- Monitor for abnormal SCADA/ICS protocol activity
- Track lateral movement patterns via SMB and RDP

**Total INDICATOR Instances**: 180+ annotations across network indicators, file hashes, registry keys, file paths, credentials, SCADA protocols, email addresses, domains, IP addresses, and behavioral patterns.
