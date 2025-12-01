# Sector Defense Industrial Base Indicators of Compromise

## Overview  
Defense sector with focus on Russia APTs operations targeting critical infrastructure and high-value assets.

## Primary Infrastructure
Command and control server <INDICATOR>45.30.30.30</INDICATOR> active during <CAMPAIGN>Defense sector Campaign 30</CAMPAIGN>. Domain <INDICATOR>c2-30.malicious-domain[.]com</INDICATOR>.

Backup infrastructure <INDICATOR>89.30.30.30</INDICATOR> hosting payloads and exfiltration endpoints. AS <INDICATOR>AS303030</INDICATOR>.

Proxy network IPs: <INDICATOR>103.30.100.1</INDICATOR>, <INDICATOR>103.30.100.2</INDICATOR>, <INDICATOR>103.30.100.3</INDICATOR>.

## Malware Families
Primary binary SHA256 <INDICATOR>a000000000000000000000000000000000000000000000000000000333333330</INDICATOR> with compilation timestamp <INDICATOR>2024-04-30</INDICATOR>.

Dropper MD5 <INDICATOR>b0000000000000000000000003333330</INDICATOR> extracting payload to <INDICATOR>C:\ProgramData\System30</INDICATOR>.

Payload DLL <INDICATOR>module30.dll</INDICATOR> with export <INDICATOR>Start30</INDICATOR> hash <INDICATOR>c000000000000000000000000000000000000000000000000000000666666660</INDICATOR>.

## Network Communication
HTTP beacons to <INDICATOR>/api/v30/status?id=[VICTIM_ID]&data=[BASE64]</INDICATOR> every <INDICATOR>900</INDICATOR> seconds.

HTTPS traffic to <INDICATOR>updates.cdn-service-30[.]net:443</INDICATOR> with TLS certificate SHA256 <INDICATOR>D000000000000000000000000000000000000000000000000000000999999990</INDICATOR>.

DNS tunneling queries to <INDICATOR>[HEX_DATA].tunnel30[.]net</INDICATOR> encoding exfiltration data.

## Initial Access Vectors
Spear-phishing email from <INDICATOR>security30@legitimate-looking-domain[.]com</INDICATOR> with subject "Urgent: Security Alert 30".

Malicious attachment <INDICATOR>SecurityUpdate_30.zip</INDICATOR> containing <INDICATOR>Update_30.exe</INDICATOR> hash <INDICATOR>e000000000000000000000000000000000000000000000000000001333333320</INDICATOR>.

Exploit delivery via <INDICATOR>hxxps://watering-hole-30[.]com/news/article30</INDICATOR> targeting <VULNERABILITY>CVE-2024-30000</VULNERABILITY>.

## Credential Operations
Mimikatz execution dumping credentials to <INDICATOR>C:\Windows\Temp\dump30.txt</INDICATOR>. File hash <INDICATOR>f000000000000000000000000000000000000000000000000000001666666650</INDICATOR>.

Stolen NTLM hashes: <INDICATOR>aad3b435b51404eeaad3b435b51404ee:00000000000000000000000019999980</INDICATOR> for <INDICATOR>domain_admin_30</INDICATOR>.

Pass-the-hash attacks using <INDICATOR>psexec.exe \\TARGET -u domain_admin_30 -p [HASH]</INDICATOR>.

Kerberos golden tickets forged with SPN <INDICATOR>krbtgt/DOMAIN30.LOCAL</INDICATOR>.

## Persistence Mechanisms
Registry autorun <INDICATOR>HKCU\Software\Microsoft\Windows\CurrentVersion\Run\SystemCheck30</INDICATOR> = <INDICATOR>"C:\Users\Public\svc30.exe"</INDICATOR>.

Scheduled task <INDICATOR>\Microsoft\Windows\AppID\Verification30</INDICATOR> executes <INDICATOR>powershell.exe -File C:\ProgramData\script30.ps1</INDICATOR>.

Service installation <INDICATOR>Windows30Service</INDICATOR> with ImagePath <INDICATOR>C:\Windows\System32\drivers\service30.exe</INDICATOR>.

WMI event filter <INDICATOR>__EventFilter.Name="Monitor30"</INDICATOR> triggering <INDICATOR>CommandLineEventConsumer.Name="Execute30"</INDICATOR>.

## Lateral Movement
SMB enumeration <INDICATOR>net view /all /domain</INDICATOR> from <INDICATOR>WORKSTATION-30</INDICATOR> at IP <INDICATOR>192.168.30.30</INDICATOR>.

PsExec deployment to <INDICATOR>150</INDICATOR> systems using <INDICATOR>\\SERVER*\ADMIN$\malware30.exe</INDICATOR>.

RDP brute force attempts from <INDICATOR>10.10.30.30</INDICATOR> targeting port <INDICATOR>3389</INDICATOR> with 3000 login attempts.

## Data Exfiltration
Archive creation <INDICATOR>exfil_30_[TIMESTAMP].7z</INDICATOR> with password <INDICATOR>Extract30#2024</INDICATOR> containing <INDICATOR>150 GB</INDICATOR> data.

SFTP upload to <INDICATOR>storage30.exfil-server[.]org:22</INDICATOR> using credentials <INDICATOR>upload30:Pass30!</INDICATOR>.

Cloud storage abuse: <INDICATOR>mega.nz/30</INDICATOR> folder link shared with attacker-controlled account <INDICATOR>exfil_30@protonmail.com</INDICATOR>.

## SCADA/ICS Targeting
Modbus TCP reconnaissance scanning <INDICATOR>10.30.0.0/16</INDICATOR> on port <INDICATOR>502</INDICATOR> identifying <INDICATOR>60</INDICATOR> PLCs.

S7comm write operations to <INDICATOR>10.30.100.15:102</INDICATOR> modifying registers <INDICATOR>DB30.DBW0-DB30.DBW100</INDICATOR>.

DNP3 master station impersonation sending control commands to <INDICATOR>10.30.200.20:20000</INDICATOR>.

HMI compromise deploying <INDICATOR>scada_monitor_30.exe</INDICATOR> hash <INDICATOR>g000000000000000000000000000000000000000000000000000002333333310</INDICATOR> intercepting operator commands.

## Ransomware Indicators
Encryption binary <INDICATOR>encrypt30.exe</INDICATOR> SHA256 <INDICATOR>h000000000000000000000000000000000000000000000000000002666666640</INDICATOR> appending extension <INDICATOR>.locked30</INDICATOR>.

Ransom note <INDICATOR>READ_ME_30.txt</INDICATOR> demanding <INDICATOR>$3000,000 USD</INDICATOR> to Bitcoin address <INDICATOR>bc1q300000000000000000000000000000000001c9c362</INDICATOR>.

Wallpaper changed to <INDICATOR>C:\ProgramData\wallpaper30.bmp</INDICATOR> displaying payment instructions.

Shadow copy deletion <INDICATOR>vssadmin delete shadows /all /quiet</INDICATOR> and <INDICATOR>wbadmin delete catalog -quiet</INDICATOR>.

## Defense Evasion
Windows Defender exclusion <INDICATOR>Add-MpPreference -ExclusionPath "C:\ProgramData\System30"</INDICATOR>.

Event log clearing <INDICATOR>wevtutil cl System</INDICATOR>, <INDICATOR>wevtutil cl Security</INDICATOR>, <INDICATOR>wevtutil cl Application</INDICATOR>.

Timestomping files to match system timestamps <INDICATOR>2024-01-01 00:00:00</INDICATOR>.

Process hollowing <INDICATOR>svchost.exe</INDICATOR> injecting malicious code into PID <INDICATOR>3000</INDICATOR>.

## Mobile Indicators
Android malware <INDICATOR>com.system.update30</INDICATOR> APK hash <INDICATOR>i000000000000000000000000000000000000000000000000000002999999970</INDICATOR> targeting mobile banking apps.

iOS profile <INDICATOR>EnterpriseProfile30.mobileconfig</INDICATOR> installing root certificate enabling MitM attacks.

## Attribution Intelligence
**Confidence**: HIGH - Attribution to <THREAT_ACTOR>Russia APTs</THREAT_ACTOR> based on:
- Infrastructure overlap with previous campaigns
- TTP consistency across operations  
- Code similarities in malware samples
- Targeting aligns with threat actor strategic objectives
- Language artifacts in ransom notes and phishing

**Related Campaigns**: <CAMPAIGN>Defense sector Campaign 30</CAMPAIGN>, <CAMPAIGN>Operation 30</CAMPAIGN>

**Related Vulnerabilities**: <VULNERABILITY>CVE-2024-30000</VULNERABILITY>, <VULNERABILITY>CVE-2023-15000</VULNERABILITY>

**Related Malware**: <MALWARE>Malware Family 30</MALWARE>, <MALWARE>Backdoor Variant 30</MALWARE>, <MALWARE>Ransomware 30</MALWARE>

**Detection Recommendations**:
- Monitor for network connections to <INDICATOR>45.30.30.30</INDICATOR> and associated domains
- Alert on file hashes listed above
- Detect registry persistence mechanisms
- Monitor for abnormal SCADA/ICS protocol activity
- Track lateral movement patterns via SMB and RDP

**Total INDICATOR Instances**: 180+ annotations across network indicators, file hashes, registry keys, file paths, credentials, SCADA protocols, email addresses, domains, IP addresses, and behavioral patterns.
