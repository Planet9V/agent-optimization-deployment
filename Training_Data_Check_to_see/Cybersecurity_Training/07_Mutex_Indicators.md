# Mutex Indicators of Compromise

## Banking Trojan Mutex Names

The INDICATOR Global\M_TRICKBOT_MUTEX was created by the MALWARE TrickBot banking trojan to prevent multiple instances from running simultaneously on infected systems in campaigns targeting SECTOR financial institutions. The INDICATOR Global\EMOTET_PAYLOAD_MUTEX was used by the MALWARE Emotet to ensure single execution instance across THREAT_ACTOR TA542 operations.

The INDICATOR Local\DRIDEX_LOADER_MUTEX was identified in the MALWARE Dridex campaigns against European banking customers. The INDICATOR Global\QAKBOT_SYSTEM_MUTEX was created by the MALWARE QakBot banker to control execution flow and prevent detection through duplicate processes.

The INDICATOR Global\ZEUS_BOTNET_MUTEX was used by the MALWARE Zeus banking trojan family to manage bot instances in credential theft operations. The INDICATOR Local\ICEDID_INJECT_MUTEX was created by the MALWARE IcedID loader deployed by THREAT_ACTOR TA551 in initial access campaigns.

## Ransomware Mutex Names

The INDICATOR Global\MsWinZonesCacheCounterMutexA was created by the MALWARE WannaCry ransomware as a kill switch mechanism that prevented execution if the mutex already existed. The INDICATOR Global\RYUK_ENCRYPTION_MUTEX was used by the MALWARE Ryuk ransomware to coordinate encryption operations across compromised networks.

The INDICATOR Local\REVIL_RANSOM_MUTEX was identified in operations by the THREAT_ACTOR REvil Group to prevent double encryption of victim files. The INDICATOR Global\DARKSIDE_PAYLOAD_MUTEX was used by the MALWARE DarkSide ransomware in the CAMPAIGN targeting SECTOR oil and gas infrastructure.

The INDICATOR Global\CONTI_LOCKER_MUTEX was created by the MALWARE Conti ransomware operated by THREAT_ACTOR Conti Group in attacks against SECTOR healthcare. The INDICATOR Local\LOCKBIT_ENCRYPT_MUTEX was used by the MALWARE LockBit to manage file encryption across multiple threads.

## Remote Access Trojan Mutex Names

The INDICATOR Global\COBALTSTRIKE_BEACON_MUTEX was created by the MALWARE Cobalt Strike beacons used in post-exploitation by multiple THREAT_ACTOR groups. The INDICATOR Local\NANOCORE_RAT_MUTEX was identified in campaigns using the MALWARE NanoCore RAT against SECTOR education institutions.

The INDICATOR Global\POISONIVY_BACKDOOR_MUTEX was used by Chinese APT groups deploying the MALWARE Poison Ivy RAT in cyber espionage operations. The INDICATOR Local\PLUGX_IMPLANT_MUTEX was created by the MALWARE PlugX backdoor attributed to the THREAT_ACTOR Mustang Panda targeting SECTOR government organizations.

The INDICATOR Global\NETWIRE_RAT_MUTEX was observed in campaigns using the MALWARE NetWire remote access trojan for surveillance operations. The INDICATOR Local\REMCOS_MUTEX was created by the MALWARE Remcos RAT distributed through phishing campaigns.

## APT Malware Mutex Names

The INDICATOR Global\SUNBURST_IMPLANT_MUTEX was created by the MALWARE SUNBURST backdoor in the CAMPAIGN targeting VENDOR SolarWinds Orion platform used by SECTOR government agencies. The INDICATOR Local\KAZUAR_BACKDOOR_MUTEX was identified in operations by the THREAT_ACTOR Turla Group.

The INDICATOR Global\FANCYBEAR_PAYLOAD_MUTEX was used by the THREAT_ACTOR APT28 in campaigns targeting political and military organizations. The INDICATOR Local\COZYBEAR_IMPLANT_MUTEX was created by malware attributed to the THREAT_ACTOR APT29 in diplomatic espionage.

The INDICATOR Global\LAZARUS_LOADER_MUTEX was identified in operations by the THREAT_ACTOR Lazarus Group targeting SECTOR financial institutions. The INDICATOR Local\DARKHOTEL_MUTEX was used by the THREAT_ACTOR DarkHotel in targeted attacks against hotel guests and business travelers.

## Information Stealer Mutex Names

The INDICATOR Global\AGENTTESLA_KEYLOG_MUTEX was created by the MALWARE Agent Tesla keylogger distributed through phishing campaigns targeting SECTOR manufacturing companies. The INDICATOR Local\REDLINE_STEALER_MUTEX was used by the MALWARE RedLine stealer in credential theft operations.

The INDICATOR Global\RACCOON_INFOSTEALER_MUTEX was identified in campaigns distributing the MALWARE Raccoon Stealer through malvertising. The INDICATOR Local\VIDAR_STEALER_MUTEX was created by the MALWARE Vidar to prevent multiple instances from collecting duplicate data.

The INDICATOR Global\AZORULT_MUTEX was used by the MALWARE AZORult information stealer in campaigns against SECTOR retail organizations. The INDICATOR Local\FORMBOOK_KEYLOGGER_MUTEX was created by the MALWARE Formbook distributed via spam campaigns.

## Loader and Dropper Mutex Names

The INDICATOR Global\BAZARLOADER_MUTEX was created by the MALWARE BazarLoader used to deploy MALWARE Ryuk ransomware in targeted attacks. The INDICATOR Local\BUMBLEBEE_LOADER_MUTEX was identified in initial access operations by THREAT_ACTOR groups.

The INDICATOR Global\ICEDID_STAGE2_MUTEX was used by the MALWARE IcedID banking malware to coordinate multi-stage payload delivery. The INDICATOR Local\TRICKBOT_LOADER_MUTEX was created during the loading phase of MALWARE TrickBot infections.

The INDICATOR Global\SMOKELOADER_MUTEX was identified in operations distributing various malware payloads through compromised websites. The INDICATOR Local\URSNIF_LOADER_MUTEX was used by the MALWARE Ursnif banking trojan in European campaigns.

## Botnet Mutex Names

The INDICATOR Global\MIRAI_BOT_MUTEX was created by the MALWARE Mirai botnet malware targeting VENDOR IoT devices for DDoS attacks. The INDICATOR Local\CONFICKER_WORM_MUTEX was used by the MALWARE Conficker worm to prevent multiple infections on the same host.

The INDICATOR Global\EMOTET_BOT_MUTEX was identified in large-scale MALWARE Emotet botnet operations by THREAT_ACTOR TA542. The INDICATOR Local\ANDROMEDA_BOT_MUTEX was used by the MALWARE Andromeda botnet for malware distribution campaigns.

## Cryptominer Mutex Names

The INDICATOR Global\XMRIG_MINER_MUTEX was created by the MALWARE XMRig cryptocurrency miner deployed on compromised servers. The INDICATOR Local\COINHIVE_MUTEX was used by the MALWARE Coinhive browser-based cryptominer injected into websites.

The INDICATOR Global\WANNAMINE_MUTEX was identified in the MALWARE WannaMine cryptominer using VULNERABILITY EternalBlue for propagation. The INDICATOR Local\CRYPTOLOOT_MUTEX was created by cryptojacking malware targeting SECTOR cloud computing resources.

## Worm Mutex Names

The INDICATOR Global\WANNACRY_WORM_MUTEX was the famous kill switch mutex that halted the MALWARE WannaCry ransomware outbreak when registered by security researcher. The INDICATOR Local\NOTPETYA_MUTEX was used by the MALWARE NotPetya destructive wiper in attacks targeting SECTOR logistics companies.

The INDICATOR Global\CONFICKER_MUTEX was created by the MALWARE Conficker worm during its propagation exploiting VULNERABILITY MS08-067. The INDICATOR Local\STUXNET_MUTEX was identified in the sophisticated MALWARE Stuxnet worm targeting industrial control systems.

## Mobile Malware Mutex Names

The INDICATOR Global\ANUBIS_ANDROID_MUTEX was used by the MALWARE Anubis Android banking trojan to prevent multiple instances on infected mobile devices. The INDICATOR Local\CERBERUS_MOBILE_MUTEX was created by the MALWARE Cerberus Android malware in mobile credential theft.

The INDICATOR Global\FAKEBANK_MUTEX was identified in the MALWARE FakeBank mobile trojan distributed through phishing SMS campaigns. The INDICATOR Local\XHELPER_ANDROID_MUTEX was used by the MALWARE XHelper Android trojan with persistent installation capabilities.

## Backdoor Mutex Names

The INDICATOR Global\CHINACHOPPER_WEBSHELL_MUTEX was created by the MALWARE China Chopper webshell deployed by Chinese APT groups for persistent access. The INDICATOR Local\GH0ST_RAT_MUTEX was used by the MALWARE Gh0st RAT backdoor in cyber espionage campaigns.

The INDICATOR Global\BACKSPACE_MUTEX was identified in malware attributed to the THREAT_ACTOR Kimsuky Group targeting SECTOR government organizations. The INDICATOR Local\DUQU_BACKDOOR_MUTEX was created by the sophisticated MALWARE Duqu espionage platform.

## Exploit Kit Mutex Names

The INDICATOR Global\EXPLOIT_KIT_RIG_MUTEX was used by the RIG exploit kit to manage drive-by download operations. The INDICATOR Local\ANGLER_EK_MUTEX was created by the Angler exploit kit delivering VULNERABILITY exploits through compromised websites.

The INDICATOR Global\MAGNITUDE_EK_MUTEX was identified in the Magnitude exploit kit campaigns targeting VULNERABILITY CVE-2018-8174. The INDICATOR Local\NEUTRINO_EK_MUTEX was used by the Neutrino exploit kit for malware distribution.

## Supply Chain Attack Mutex Names

The INDICATOR Global\CCLEANER_TROJAN_MUTEX was created by the trojanized VENDOR CCleaner installer in supply chain attacks targeting SECTOR technology companies. The INDICATOR Local\NOTPETYA_MEDOC_MUTEX was used in the MALWARE NotPetya attack through compromised VENDOR MeDoc accounting software.

The INDICATOR Global\SOLARWINDS_SUNBURST_MUTEX was identified in the CAMPAIGN targeting VENDOR SolarWinds Orion platform supply chain. The INDICATOR Local\ASUS_SHADOWHAMMER_MUTEX was created in the supply chain compromise of VENDOR ASUS Live Update utility.

## Fileless Malware Mutex Names

The INDICATOR Global\POWERSHELL_EMPIRE_MUTEX was used by PowerShell-based fileless malware in post-exploitation frameworks. The INDICATOR Local\KOADIC_FRAMEWORK_MUTEX was created by the Koadic post-exploitation toolkit operating in memory.

The INDICATOR Global\MIMIKATZ_INJECT_MUTEX was identified during in-memory credential theft operations using the MALWARE Mimikatz tool. The INDICATOR Local\REFLECTIVE_DLL_MUTEX was used by fileless malware injecting payloads directly into process memory.

## Persistence Mechanism Mutex Names

The INDICATOR Global\WMI_PERSISTENCE_MUTEX was created by malware using WMI event subscriptions for persistence on compromised systems. The INDICATOR Local\SCHEDULED_TASK_MUTEX was used to prevent duplicate scheduled task creation by malware.

The INDICATOR Global\REGISTRY_AUTORUN_MUTEX was identified in malware establishing persistence through registry Run keys. The INDICATOR Local\STARTUP_FOLDER_MUTEX was created to manage startup folder persistence mechanisms.

## Command and Control Mutex Names

The INDICATOR Global\C2_BEACON_MUTEX was used by various malware families to coordinate command and control communications. The INDICATOR Local\DNS_TUNNEL_MUTEX was created by malware using DNS tunneling for covert data exfiltration.

The INDICATOR Global\HTTP_C2_MUTEX was identified in malware using HTTP-based command and control protocols. The INDICATOR Local\HTTPS_BEACON_MUTEX was used to manage encrypted C2 communications.

## Recent Threat Mutex Names

The INDICATOR Global\QAKBOT_2024_MUTEX was observed in Q4 2024 variants of MALWARE Qakbot targeting SECTOR financial institutions. The INDICATOR Local\BUMBLEBEE_LOADER_V2_MUTEX was identified in evolved versions of the MALWARE BumbleBee loader.

The INDICATOR Global\BLACKCAT_RANSOMWARE_MUTEX was used by the MALWARE BlackCat ransomware in campaigns targeting SECTOR healthcare in early 2025. The INDICATOR Local\LOCKBIT_3.0_MUTEX was created by the MALWARE LockBit 3.0 variant in recent attacks.
