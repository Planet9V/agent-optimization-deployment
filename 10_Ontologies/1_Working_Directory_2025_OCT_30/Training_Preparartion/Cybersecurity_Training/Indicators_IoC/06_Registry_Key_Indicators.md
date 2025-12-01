# Registry Key Indicators of Compromise

## Persistence Mechanism Registry Keys

The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\WindowsDefender was created by the MALWARE Emotet banking trojan to establish persistence on compromised systems in campaigns by THREAT_ACTOR TA542. The INDICATOR HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\SecurityUpdate was used by the MALWARE TrickBot to maintain persistence across system reboots.

The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce\SystemInit was identified as a persistence mechanism for the MALWARE Dridex banking malware targeting SECTOR financial institutions. The INDICATOR HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders\Startup was modified by the MALWARE QakBot to place malicious executables in startup folders.

The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinDefender was created by the THREAT_ACTOR APT29 to register a malicious service disguised as Windows Defender. The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Shell was modified by the MALWARE Agent Tesla to execute on user login.

## Service Installation Registry Keys

The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MaliciousService was created during the CAMPAIGN targeting SECTOR government agencies with persistent backdoor services. The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UpdaterService\ImagePath pointed to the MALWARE Cobalt Strike beacon executable.

The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\WindowsUpdateService was used by the THREAT_ACTOR APT28 to install persistent services on compromised systems. The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NetTcpPortSharing\Parameters was modified to enable malicious network services.

## Scheduled Task Registry Keys

The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks\{GUID} was created by the MALWARE Ryuk ransomware to schedule encryption tasks. The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree\MicrosoftEdgeUpdateTaskMachine was used by attackers to masquerade scheduled tasks.

The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Plain\{GUID} was identified in campaigns by the THREAT_ACTOR Lazarus Group for scheduled malware execution. The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Boot was modified to execute malware at system startup.

## Browser Extension Registry Keys

The INDICATOR HKEY_CURRENT_USER\Software\Google\Chrome\Extensions\maliciousextensionid was created by the MALWARE browser-based credential stealer targeting VENDOR Google Chrome users. The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Mozilla\Firefox\Extensions was modified to install malicious VENDOR Firefox extensions.

The INDICATOR HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Browser Helper Objects was used by the MALWARE Zeus banking trojan to inject into VENDOR Internet Explorer. The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Internet Explorer\Extensions was created to install malicious IE toolbars.

## Proxy and Network Configuration Keys

The INDICATOR HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ProxyServer was modified by the THREAT_ACTOR APT32 to redirect network traffic through attacker-controlled proxies. The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces was changed to configure malicious DNS servers.

The INDICATOR HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ProxyEnable was set to force proxy usage in man-in-the-middle attacks. The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap was modified to bypass security warnings.

## Malware Configuration Registry Keys

The INDICATOR HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\Hidden stored configuration data for the MALWARE Emotet including C2 server addresses. The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography\RNG\Seed was used by the MALWARE TrickBot to store encrypted command and control information.

The INDICATOR HKEY_CURRENT_USER\Software\Classes\CLSID\{GUID}\InprocServer32 was created by the MALWARE DarkHotel to register malicious COM objects. The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options was modified for debugger persistence techniques.

## Anti-Analysis Registry Keys

The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Disk\Enum was queried by the MALWARE to detect virtualized environments and sandbox analysis. The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Virtual Machine\Guest\Parameters was checked to identify virtual machine execution.

The INDICATOR HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System\SystemBiosVersion was examined by the MALWARE Agent Tesla to detect analysis environments. The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\TimeZoneInformation was modified to evade time-based detection.

## Credential Theft Registry Keys

The INDICATOR HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\Windows Messaging Subsystem\Profiles\Outlook was accessed by the MALWARE to extract VENDOR Microsoft Outlook credentials. The INDICATOR HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Account Manager\Accounts was targeted for email account credential theft.

The INDICATOR HKEY_LOCAL_MACHINE\SECURITY\Policy\Secrets was accessed by the THREAT_ACTOR groups using MALWARE Mimikatz to extract LSA secrets. The INDICATOR HKEY_LOCAL_MACHINE\SAM\SAM\Domains\Account\Users was targeted for local account password hash extraction.

## Firewall and Security Bypass Keys

The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile\AuthorizedApplications was modified by the MALWARE to allow malicious network connections. The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection\DisableRealtimeMonitoring was set to disable VENDOR Windows Defender.

The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\EnableLUA was modified to disable User Account Control in attacks by the THREAT_ACTOR APT41. The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa\DisableRestrictedAdmin was set to enable lateral movement.

## Bootkit and Rootkit Registry Keys

The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\BootExecute was modified by the MALWARE Rovnix bootkit to execute before the operating system loads. The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\{GUID}\Type was set to kernel driver type for rootkit installation.

The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SafeBoot was modified to ensure malicious driver loading in Safe Mode. The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\{GUID}\Start was set to boot start for early malware execution.

## Ransomware Registry Keys

The INDICATOR HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System\Wallpaper was modified by the MALWARE WannaCry ransomware to display ransom notes as desktop wallpaper. The INDICATOR HKEY_CURRENT_USER\Control Panel\Desktop\SCRNSAVE.EXE was changed by the MALWARE Ryuk to display ransom demands.

The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\RansomNote was created by the MALWARE REvil to display payment instructions. The INDICATOR HKEY_CURRENT_USER\Software\CryptoLocker was used to store encryption keys and victim identifiers.

## DLL Hijacking Registry Keys

The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLs was modified to facilitate DLL hijacking attacks by the THREAT_ACTOR APT28. The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows\AppInit_DLLs was used to inject malicious DLLs into processes.

The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\SafeDllSearchMode was disabled to enable DLL search order hijacking. The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\ShellServiceObjectDelayLoad was used for persistent DLL injection.

## COM Hijacking Registry Keys

The INDICATOR HKEY_CURRENT_USER\Software\Classes\CLSID\{GUID}\TreatAs was modified to redirect COM object instantiation to malicious implementations. The INDICATOR HKEY_CURRENT_USER\Software\Classes\CLSID\{GUID}\ProgID was hijacked by the MALWARE to intercept application functionality.

The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID\{GUID}\InprocServer32\ThreadingModel was modified for COM object persistence by the THREAT_ACTOR groups. The INDICATOR HKEY_CURRENT_USER\Software\Classes\CLSID\{GUID}\LocalServer32 was redirected to malicious executables.

## WMI Persistence Registry Keys

The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\WBEM\ESS\NameValueStore was used by the THREAT_ACTOR APT29 to store WMI event subscription data for persistence. The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\WBEM\CIMOM was modified to enable malicious WMI providers.

The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Wbem\Transports\Decoupled\Client was used for WMI-based command and control by advanced persistent threats. The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\WBEM\ESS\Sink was configured for event-driven malware execution.

## Print Spooler Exploitation Keys

The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Print\Environments\Windows x64\Drivers\Version-3 was modified during exploitation of VULNERABILITY PrintNightmare (CVE-2021-34527). The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Print\Printers was targeted in attacks leveraging print spooler vulnerabilities.

## Recent APT Campaign Keys

The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\Credential Providers was modified in the CAMPAIGN SolarWinds supply chain attack by the THREAT_ACTOR APT29. The INDICATOR HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Excel\Security\AccessVBOM was enabled to execute malicious macros.

The INDICATOR HKEY_LOCAL_MACHINE\SOFTWARE\Classes\ms-msdt was exploited in VULNERABILITY Follina (CVE-2022-30190) attacks distributing MALWARE through malicious documents. The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters was modified in SMB relay attacks.

## Cloud and Remote Access Keys

The INDICATOR HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Servers was accessed to extract RDP connection history and credentials. The INDICATOR HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp was modified to enable unauthorized remote access.

The INDICATOR HKEY_CURRENT_USER\Software\Microsoft\OneDrive was targeted for cloud storage credential theft in campaigns against VENDOR Microsoft 365 users. The INDICATOR HKEY_CURRENT_USER\Software\Amazon\AWS was accessed to steal VENDOR Amazon Web Services credentials.
