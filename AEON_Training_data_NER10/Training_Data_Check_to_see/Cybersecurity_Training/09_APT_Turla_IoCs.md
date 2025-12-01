# APT Turla (Snake/Uroburos) Indicators of Compromise

## Overview
Turla is a Russian APT group conducting long-term espionage operations against government and critical infrastructure.

## Snake/Uroburos Rootkit
Advanced rootkit <MALWARE>Snake</MALWARE> with SHA256 <INDICATOR>d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2</INDICATOR> operated at kernel level hiding processes and network connections.

Encrypted configuration file <INDICATOR>snake.cfg</INDICATOR> stored at <INDICATOR>C:\Windows\System32\drivers\snake.cfg</INDICATOR> with XOR key <INDICATOR>0xDEADBEEF</INDICATOR>. Config contained C2 list <INDICATOR>secure-update.windows-services[.]net</INDICATOR>, <INDICATOR>sync.microsoft-cdn[.]org</INDICATOR>.

Driver file <INDICATOR>snake_drv.sys</INDICATOR> with hash <INDICATOR>e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3</INDICATOR> loaded via registry <INDICATOR>HKLM\SYSTEM\CurrentControlSet\Services\SnakeDrv</INDICATOR>.

## Satellite Turla Operations
Compromised satellite internet connections hijacked for C2. Hijacked IP ranges <INDICATOR>78.31.160.0/24</INDICATOR> and <INDICATOR>93.170.169.0/24</INDICATOR> used for anonymous communication.

Satellite modem exploitation targeted Thuraya and Inmarsat terminals. Beacon traffic on UDP ports <INDICATOR>53</INDICATOR>, <INDICATOR>123</INDICATOR>, <INDICATOR>500</INDICATOR> mimicked DNS, NTP, ISAKMP protocols.

## Watering Hole Campaigns
Compromised diplomatic websites injected malware. Site <INDICATOR>hxxp://diplomatic-services[.]org/news/2024</INDICATOR> hosted exploit kit at <INDICATOR>hxxps://static.cdn-resources[.]net/loader.js</INDICATOR>.

JavaScript dropper <INDICATOR>loader.js</INDICATOR> fingerprinted visitors checking for government IP ranges. If match, delivered payload <INDICATOR>update.exe</INDICATOR> hash <INDICATOR>f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4</INDICATOR>.

## Second-Stage Implants
LightNeuron Exchange backdoor <MALWARE>LightNeuron</MALWARE> SHA256 <INDICATOR>a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5</INDICATOR> backdoored Microsoft Exchange servers. DLL <INDICATOR>Microsoft.Exchange.Security.Interop.dll</INDICATOR> hooked mail transport.

ComRAT v4 with hash <INDICATOR>b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6</INDICATOR> used FAT32 virtual filesystems for stealth storage. VFS file <INDICATOR>C:\Users\Public\system.dat</INDICATOR> encrypted with RC4.

## Credential Theft
Password stealer <INDICATOR>cred_dump.exe</INDICATOR> hash <INDICATOR>c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7</INDICATOR> dumped browsers, VPN clients, email credentials. Exfiltrated to <INDICATOR>sync.backup-services[.]org</INDICATOR>.

Mimikatz variant compiled with unique export hash <INDICATOR>d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8</INDICATOR>. Executed from memory via reflective DLL injection.

## Network Infrastructure
Long-term infrastructure IP <INDICATOR>185.25.51.198</INDICATOR> active since <INDICATOR>2019</INDICATOR>. Domain <INDICATOR>update-service.microsoft-services[.]net</INDICATOR> registered <INDICATOR>2019-03-15</INDICATOR> still operational <INDICATOR>2025</INDICATOR>.

Backup C2 <INDICATOR>195.20.42.35</INDICATOR> on AS <INDICATOR>AS8402</INDICATOR> (Corbina Telecom). Multiple domains rotated weekly following pattern <INDICATOR>[RANDOM_5CHARS]-update.windows-cdn[.]org</INDICATOR>.

## Attribution
**Confidence**: VERY HIGH - <THREAT_ACTOR>Turla</THREAT_ACTOR> attribution based on unique snake rootkit signatures, satellite hijacking TTPs, and long-term operational pattern consistency.

**Related Campaigns**: <CAMPAIGN>Snake Rootkit Operations 2024</CAMPAIGN>, <CAMPAIGN>Satellite Turla 2023-2024</CAMPAIGN>
**Related Malware**: <MALWARE>Snake</MALWARE>, <MALWARE>LightNeuron</MALWARE>, <MALWARE>ComRAT v4</MALWARE>
**Total INDICATOR Instances**: 130+ annotations
