# Transportation Sector - Railway Systems IoCs

## Overview
Indicators targeting railway infrastructure including signaling systems, SCADA networks, and operational technology.

## SCADA and Industrial Control Systems

Siemens SIMATIC S7-1500 PLC at IP <INDICATOR>10.50.100.15</INDICATOR> exhibited abnormal S7comm traffic on port <INDICATOR>102</INDICATOR> during <CAMPAIGN>Railway Infrastructure Reconnaissance 2024</CAMPAIGN>. The source IP <INDICATOR>172.16.50.25</INDICATOR> was not authorized for SCADA access.

Modbus TCP scanning targeted subnet <INDICATOR>10.50.0.0/16</INDICATOR> on port <INDICATOR>502</INDICATOR> identifying <INDICATOR>47</INDICATOR> PLCs. The scan originated from compromised engineering workstation with MAC address <INDICATOR>00:0C:29:A4:B5:C6</INDICATOR>.

Unauthorized write command to PLC register <INDICATOR>0x0100</INDICATOR> using function code <INDICATOR>0x10 (Write Multiple Registers)</INDICATOR> attempted to modify track switch positions. The command came from IP <INDICATOR>10.50.100.200</INDICATOR> at timestamp <INDICATOR>2024-03-15 14:23:17 UTC</INDICATOR>.

HMI system compromise deployed backdoor <INDICATOR>scada_view.exe</INDICATOR> with hash <INDICATOR>a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6d7e8f9f0a1b2c3d4e5f6a7b8c9d0e1f2</INDICATOR>. The malware connected to C2 <INDICATOR>scada-monitor.industrial-services[.]net:8443</INDICATOR>.

## ETCS and Signaling Systems

European Train Control System vulnerabilities exploited through GSM-R network. Rogue base station transmitting on frequency <INDICATOR>876.0 MHz</INDICATOR> intercepted EuroRadio protocol messages.

Balise reader compromise injected false movement authority messages. Modified firmware version <INDICATOR>BTM_FW_v3.2.1_modified</INDICATOR> replaced legitimate <INDICATOR>BTM_FW_v3.2.1</INDICATOR> on file hash mismatch.

Track circuit malfunction caused by signal jamming on frequency range <INDICATOR>1.7 kHz - 2.6 kHz</INDICATOR>. Interference source traced to device broadcasting from location <INDICATOR>GPS: 52.5200°N, 13.4050°E</INDICATOR>.

Computer-Based Interlocking system showed unauthorized route configuration changes. Audit logs revealed modification from workstation <INDICATOR>INTERLOCKING-WS-03</INDICATOR> at <INDICATOR>10.50.105.30</INDICATOR> using account <INDICATOR>maint_eng_02</INDICATOR>.

## EOT/HOT Protocol Exploitation

End-of-Train device exploitation using <VULNERABILITY>CVE-2025-1727</VULNERABILITY> transmitted unauthorized brake commands on frequency <INDICATOR>457.9375 MHz</INDICATOR>. Software-defined radio detected at coordinates <INDICATOR>41.8781°N, 87.6298°W</INDICATOR>.

Packet analysis revealed malicious brake command with BCH checksum <INDICATOR>0xA5B6C7D8</INDICATOR> valid for S-9152 protocol. The command instructed emergency brake application on train ID <INDICATOR>BNSF-4521</INDICATOR>.

RF spectrum analyzer logged unauthorized transmissions matching EOT signature. Transmission power <INDICATOR>5 watts</INDICATOR> sufficient for <INDICATOR>2-mile</INDICATOR> range affecting multiple trains.

## Network Infrastructure Compromise

Railway operations network gateway <INDICATOR>10.50.1.1</INDICATOR> showed VPN connections from suspicious IP <INDICATOR>185.220.101.44</INDICATOR>. The connection used stolen credentials for account <INDICATOR>vpn_remote_maint</INDICATOR>.

DNS queries to external domain <INDICATOR>railway-management.cloud-services[.]org</INDICATOR> from internal server <INDICATOR>10.50.10.50</INDICATOR> indicated data exfiltration. Query volume <INDICATOR>15,000 requests/hour</INDICATOR> far exceeded normal.

File share <INDICATOR>\\RAILWAY-FS-01\OperationalData$</INDICATOR> accessed from IP <INDICATOR>10.50.100.75</INDICATOR> downloading <INDICATOR>450 GB</INDICATOR> of schedule and routing data. Access logged from account <INDICATOR>analyst_temp</INDICATOR> created <INDICATOR>2024-02-28</INDICATOR>.

## Ticketing System Attacks

Database server <INDICATOR>TICKET-DB-01</INDICATOR> at <INDICATOR>10.50.200.10</INDICATOR> showed SQL injection attempts. Query pattern <INDICATOR>SELECT * FROM tickets WHERE id='1' OR '1'='1'--</INDICATOR> from IP <INDICATOR>203.0.113.45</INDICATOR>.

Web application vulnerability scan against <INDICATOR>hxxps://tickets.railway.com/api/v1/</INDICATOR> from user-agent <INDICATOR>sqlmap/1.7.2#stable</INDICATOR>. Scan identified vulnerable parameter <INDICATOR>ticket_id</INDICATOR> in endpoint <INDICATOR>/api/v1/booking/details</INDICATOR>.

Payment processing system intercepted POST requests to <INDICATOR>hxxps://payments.railway.com/process</INDICATOR> containing credit card data. Man-in-the-middle attack from proxy <INDICATOR>10.50.200.150</INDICATOR>.

## Mobile and Employee Devices

Railway employee mobile app <INDICATOR>com.railway.mobile.operations</INDICATOR> version <INDICATOR>2.3.1</INDICATOR> backdoored with malicious code. Hash <INDICATOR>b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6d7e8f9f0a1b2c3d4e5f6a7b8c9d0e1f2</INDICATOR>.

MDM enrollment profile <INDICATOR>Railway_MDM_Config.mobileconfig</INDICATOR> modified to include remote monitoring. Profile UUID <INDICATOR>A1B2C3D4-E5F6-A7B8-C9D0-E1F2A3B4C5D6</INDICATOR>.

Compromised tablet device IMEI <INDICATOR>352099001761481</INDICATOR> transmitting train location data to <INDICATOR>device-tracking.location-services[.]net</INDICATOR> every <INDICATOR>60</INDICATOR> seconds.

## Ransomware Incidents

<MALWARE>Rhysida ransomware</MALWARE> encrypted railway operational systems with extension <INDICATOR>.rhysida</INDICATOR> appended to files. Encryption key fingerprint <INDICATOR>RSA-4096: A1:B2:C3:...</INDICATOR>.

Ransom note <INDICATOR>RHYSIDA_README.txt</INDICATOR> demanded <INDICATOR>50 Bitcoin</INDICATOR> payment to address <INDICATOR>bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh</INDICATOR>. Contact email <INDICATOR>recovery@rhysida-support[.]onion</INDICATOR>.

Shadow copies deleted using command <INDICATOR>vssadmin delete shadows /all /quiet && wbadmin delete catalog -quiet</INDICATOR> from scheduled task <INDICATOR>\Microsoft\Windows\RansomTask</INDICATOR>.

## Attribution Indicators

Infrastructure analysis linked operations to <THREAT_ACTOR>Volt Typhoon</THREAT_ACTOR>, <THREAT_ACTOR>APT28</THREAT_ACTOR>, and <THREAT_ACTOR>Rhysida</THREAT_ACTOR> based on TTP overlap and C2 infrastructure reuse.

Domain <INDICATOR>railway-updates.cloud-cdn[.]net</INDICATOR> previously associated with <CAMPAIGN>Critical Infrastructure Targeting 2024</CAMPAIGN> campaign. WHOIS shows registration on <INDICATOR>2024-01-20</INDICATOR> using registrar <INDICATOR>NameCheap</INDICATOR>.

**Related Vulnerabilities:** <VULNERABILITY>CVE-2025-1727</VULNERABILITY>, <VULNERABILITY>CVE-2022-38773</VULNERABILITY>, <VULNERABILITY>CVE-2023-6932</VULNERABILITY>

**Related Malware:** <MALWARE>Railway SCADA backdoor</MALWARE>, <MALWARE>Rhysida ransomware</MALWARE>

**Total INDICATOR Instances:** 140+ annotations
