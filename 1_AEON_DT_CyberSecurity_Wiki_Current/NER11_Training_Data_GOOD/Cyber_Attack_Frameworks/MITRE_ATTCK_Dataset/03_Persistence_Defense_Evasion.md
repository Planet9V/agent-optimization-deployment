# MITRE ATT&CK: Persistence and Defense Evasion Tactics

## Persistence Overview
Persistence consists of techniques that adversaries use to keep access to systems across restarts, changed credentials, and other interruptions that could cut off their access.

## Defense Evasion Overview
Defense Evasion consists of techniques that adversaries use to avoid detection throughout their compromise. Techniques used for defense evasion include uninstalling/disabling security software or obfuscating/encrypting data and scripts.

---

## PERSISTENCE TECHNIQUES

### T1098: Account Manipulation
**Entity Type:** TECHNIQUE
**Tactic:** Persistence, Privilege Escalation
**Platform:** Windows, Azure AD, Office 365, SaaS, IaaS, Linux, macOS, Google Workspace, Network

**Description:**
Adversaries may manipulate accounts to maintain access to victim systems. Account manipulation may consist of any action that preserves adversary access to a compromised account.

**Sub-techniques:**
- **T1098.001:** Additional Cloud Credentials
- **T1098.002:** Additional Email Delegate Permissions
- **T1098.003:** Additional Cloud Roles
- **T1098.004:** SSH Authorized Keys
- **T1098.005:** Device Registration

**Detection:**
- Monitor account modification events
- Track permission changes
- Analyze authentication logs
- Review access control changes

**Mitigation:**
- Multi-factor authentication
- Privileged account management
- User account management
- Operating system configuration

**Related CWE:** CWE-250 (Execution with Unnecessary Privileges)
**Related CAPEC:** CAPEC-233 (Privilege Escalation)

**Procedure Examples:**
- **APT29:** Added credentials to cloud applications
- **APT41:** Modified user account permissions
- **Dragonfly:** Added SSH keys to compromised systems

### T1136: Create Account
**Entity Type:** TECHNIQUE
**Tactic:** Persistence
**Platform:** Windows, Azure AD, Office 365, SaaS, IaaS, Linux, macOS, Google Workspace, Network

**Description:**
Adversaries may create an account to maintain access to victim systems. Adversaries may create accounts on systems, cloud platforms, or services to maintain access.

**Sub-techniques:**
- **T1136.001:** Local Account
- **T1136.002:** Domain Account
- **T1136.003:** Cloud Account

**Detection:**
- Monitor for account creation events
- Track privilege escalation
- Analyze authentication logs
- Review user management activities

**Mitigation:**
- Multi-factor authentication
- Privileged account management
- Network segmentation
- Operating system configuration

**Related CWE:** CWE-732 (Incorrect Permission Assignment)
**Related CAPEC:** CAPEC-555 (Remote Services with Stolen Credentials)

**Procedure Examples:**
- **APT3:** Created local accounts for persistence
- **APT41:** Established domain accounts on compromised networks
- **FIN6:** Created local administrator accounts

### T1547: Boot or Logon Autostart Execution
**Entity Type:** TECHNIQUE
**Tactic:** Persistence, Privilege Escalation
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may configure system settings to automatically execute a program during system boot or logon to maintain persistence or gain higher-level privileges.

**Sub-techniques:**
- **T1547.001:** Registry Run Keys / Startup Folder
- **T1547.002:** Authentication Package
- **T1547.003:** Time Providers
- **T1547.004:** Winlogon Helper DLL
- **T1547.005:** Security Support Provider
- **T1547.006:** Kernel Modules and Extensions
- **T1547.007:** Re-opened Applications
- **T1547.008:** LSASS Driver
- **T1547.009:** Shortcut Modification
- **T1547.010:** Port Monitors
- **T1547.011:** Plist Modification
- **T1547.012:** Print Processors
- **T1547.013:** XDG Autostart Entries
- **T1547.014:** Active Setup

**Detection:**
- Monitor registry modifications
- Track startup program changes
- Analyze boot sequence
- Review system configuration

**Mitigation:**
- Operating system configuration
- Code signing
- Execution prevention
- Audit

**Related CWE:** CWE-284 (Improper Access Control)
**Related CAPEC:** CAPEC-558 (Replace Trusted Executable)

### T1547.001: Registry Run Keys / Startup Folder
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1547
**Platform:** Windows

**Description:**
Adversaries may achieve persistence by adding a program to a startup folder or referencing it with a Registry run key.

**Registry Keys:**
- `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
- `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce`
- `HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run`
- `HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce`

**Startup Folders:**
- `C:\Users\[Username]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
- `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`

**Procedure Examples:**
- **APT28:** Used Registry run keys for persistence
- **Carbanak:** Modified startup folders
- **Emotet:** Created Registry run keys
- **TrickBot:** Established persistence via Registry

### T1053: Scheduled Task/Job
**Entity Type:** TECHNIQUE
**Tactic:** Execution, Persistence, Privilege Escalation
**Platform:** Windows, Linux, macOS, Network

**Description:**
Adversaries may abuse task scheduling functionality to facilitate initial or recurring execution of malicious code.

**Sub-techniques:**
- **T1053.002:** At (Linux/macOS)
- **T1053.003:** Cron
- **T1053.005:** Scheduled Task (Windows)
- **T1053.006:** Systemd Timers
- **T1053.007:** Container Orchestration Job

**Procedure Examples:**
- **APT29:** Created scheduled tasks for persistence
- **APT41:** Used scheduled tasks across multiple systems
- **Wizard Spider:** Scheduled ransomware execution

### T1543: Create or Modify System Process
**Entity Type:** TECHNIQUE
**Tactic:** Persistence, Privilege Escalation
**Platform:** Windows, Linux, macOS, Network

**Description:**
Adversaries may create or modify system-level processes to repeatedly execute malicious payloads as part of persistence.

**Sub-techniques:**
- **T1543.001:** Launch Agent
- **T1543.002:** Systemd Service
- **T1543.003:** Windows Service
- **T1543.004:** Launch Daemon

**Detection:**
- Monitor service creation/modification
- Track process execution
- Analyze system logs
- Review service configurations

**Mitigation:**
- User account management
- Restrict service installation
- Code signing
- Audit

**Related CWE:** CWE-284 (Improper Access Control)
**Related CAPEC:** CAPEC-17 (Using Malicious Files)

### T1543.003: Windows Service
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1543
**Platform:** Windows

**Description:**
Adversaries may create or modify Windows services to repeatedly execute malicious payloads. Services execute applications or commands at system startup or on a schedule.

**Tools:**
- sc.exe
- New-Service (PowerShell)
- Services.msc

**Procedure Examples:**
- **APT32:** Created malicious Windows services
- **APT41:** Modified service configurations
- **Carbanak:** Installed services for persistence

### T1574: Hijack Execution Flow
**Entity Type:** TECHNIQUE
**Tactic:** Persistence, Privilege Escalation, Defense Evasion
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may execute their own malicious payloads by hijacking the way operating systems run programs.

**Sub-techniques:**
- **T1574.001:** DLL Search Order Hijacking
- **T1574.002:** DLL Side-Loading
- **T1574.004:** Dylib Hijacking
- **T1574.006:** Dynamic Linker Hijacking
- **T1574.007:** Path Interception by PATH Environment Variable
- **T1574.008:** Path Interception by Search Order Hijacking
- **T1574.009:** Path Interception by Unquoted Path
- **T1574.010:** Services File Permissions Weakness
- **T1574.011:** Services Registry Permissions Weakness
- **T1574.012:** COR_PROFILER

**Detection:**
- Monitor DLL loading
- Track file creation in system directories
- Analyze process execution paths
- Review permissions on system files

**Mitigation:**
- Audit
- Execution prevention
- Restrict file and directory permissions
- User account management

**Related CWE:** CWE-427 (Uncontrolled Search Path Element)
**Related CAPEC:** CAPEC-471 (Search Order Hijacking)

---

## DEFENSE EVASION TECHNIQUES

### T1027: Obfuscated Files or Information
**Entity Type:** TECHNIQUE
**Tactic:** Defense Evasion
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may attempt to make an executable or file difficult to discover or analyze by encrypting, encoding, or otherwise obfuscating its contents on the system or in transit.

**Sub-techniques:**
- **T1027.001:** Binary Padding
- **T1027.002:** Software Packing
- **T1027.003:** Steganography
- **T1027.004:** Compile After Delivery
- **T1027.005:** Indicator Removal from Tools
- **T1027.006:** HTML Smuggling
- **T1027.007:** Dynamic API Resolution
- **T1027.008:** Stripped Payloads
- **T1027.009:** Embedded Payloads

**Detection:**
- Entropy analysis
- Signature-based detection
- Behavioral analysis
- Static code analysis
- Network traffic analysis

**Mitigation:**
- Antivirus/antimalware
- Network intrusion prevention

**Related CWE:** CWE-656 (Reliance on Security Through Obscurity)
**Related CAPEC:** CAPEC-267 (Leverage Alternate Encoding)

**Procedure Examples:**
- **APT28:** Used base64 encoding and XOR encryption
- **APT29:** Employed steganography in images
- **Emotet:** Used packed executables
- **TrickBot:** Obfuscated PowerShell commands

### T1036: Masquerading
**Entity Type:** TECHNIQUE
**Tactic:** Defense Evasion
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may attempt to manipulate features of their artifacts to make them appear legitimate or benign to users and/or security tools.

**Sub-techniques:**
- **T1036.001:** Invalid Code Signature
- **T1036.002:** Right-to-Left Override
- **T1036.003:** Rename System Utilities
- **T1036.004:** Masquerade Task or Service
- **T1036.005:** Match Legitimate Name or Location
- **T1036.006:** Space after Filename
- **T1036.007:** Double File Extension

**Detection:**
- File monitoring
- Process monitoring
- Binary reputation analysis
- Code signing verification

**Mitigation:**
- Code signing
- Execution prevention
- Restrict file and directory permissions

**Related CWE:** CWE-451 (User Interface Misrepresentation of Critical Information)
**Related CAPEC:** CAPEC-177 (Create Files with the Same Name as Files Protected by an Application)

**Procedure Examples:**
- **APT28:** Named malware to appear as system files
- **Carbanak:** Masqueraded as legitimate software
- **Lazarus Group:** Used legitimate filenames for malware

### T1055: Process Injection
**Entity Type:** TECHNIQUE
**Tactic:** Defense Evasion, Privilege Escalation
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may inject code into processes in order to evade process-based defenses as well as possibly elevate privileges.

**Sub-techniques:**
- **T1055.001:** Dynamic-link Library Injection
- **T1055.002:** Portable Executable Injection
- **T1055.003:** Thread Execution Hijacking
- **T1055.004:** Asynchronous Procedure Call
- **T1055.005:** Thread Local Storage
- **T1055.008:** Ptrace System Calls
- **T1055.009:** Proc Memory
- **T1055.011:** Extra Window Memory Injection
- **T1055.012:** Process Hollowing
- **T1055.013:** Process Doppelgänging
- **T1055.014:** VDSO Hijacking
- **T1055.015:** ListPlanting

**Detection:**
- Monitor for suspicious API calls
- Analyze memory allocation patterns
- Track cross-process activities
- Detect unusual DLL loads

**Mitigation:**
- Behavior prevention on endpoint
- Privileged account management

**Related CWE:** CWE-94 (Code Injection)
**Related CAPEC:** CAPEC-640 (Inclusion of Code in Existing Process)

**Procedure Examples:**
- **APT28:** Used process injection techniques
- **APT32:** Injected into legitimate processes
- **Emotet:** Process hollowing for execution
- **TrickBot:** DLL injection for persistence

### T1070: Indicator Removal on Host
**Entity Type:** TECHNIQUE
**Tactic:** Defense Evasion
**Platform:** Windows, Linux, macOS, Network

**Description:**
Adversaries may delete or alter generated artifacts on a host system, including logs or captured files such as quarantined malware.

**Sub-techniques:**
- **T1070.001:** Clear Windows Event Logs
- **T1070.002:** Clear Linux or Mac System Logs
- **T1070.003:** Clear Command History
- **T1070.004:** File Deletion
- **T1070.005:** Network Share Connection Removal
- **T1070.006:** Timestomp

**Detection:**
- Monitor for log clearing events
- Track file deletion patterns
- Analyze system logs
- File system monitoring

**Mitigation:**
- Restrict file and directory permissions
- Encrypt sensitive information
- Remote data storage

**Related CWE:** CWE-117 (Improper Output Neutralization for Logs)
**Related CAPEC:** CAPEC-93 (Log Injection-Tampering-Forging)

**Procedure Examples:**
- **APT28:** Cleared Windows event logs
- **APT32:** Deleted files after execution
- **Carbanak:** Removed traces of activity
- **FIN6:** Timestomped files to avoid detection

### T1562: Impair Defenses
**Entity Type:** TECHNIQUE
**Tactic:** Defense Evasion
**Platform:** Windows, Linux, macOS, Office 365, SaaS, IaaS, Network, Google Workspace

**Description:**
Adversaries may maliciously modify components of a victim environment in order to hinder or disable defensive mechanisms.

**Sub-techniques:**
- **T1562.001:** Disable or Modify Tools
- **T1562.002:** Disable Windows Event Logging
- **T1562.003:** Impair Command History Logging
- **T1562.004:** Disable or Modify System Firewall
- **T1562.006:** Indicator Blocking
- **T1562.007:** Disable or Modify Cloud Firewall
- **T1562.008:** Disable Cloud Logs
- **T1562.009:** Safe Mode Boot
- **T1562.010:** Downgrade Attack

**Detection:**
- Monitor security tool status
- Track configuration changes
- Analyze system logs
- Review firewall rules

**Mitigation:**
- User account management
- Restrict registry permissions
- Restrict file and directory permissions

**Related CWE:** CWE-284 (Improper Access Control)
**Related CAPEC:** CAPEC-271 (Schema Poisoning)

**Procedure Examples:**
- **APT28:** Disabled antivirus software
- **APT32:** Modified firewall rules
- **Carbanak:** Terminated security processes
- **Emotet:** Disabled Windows Defender

### T1218: System Binary Proxy Execution
**Entity Type:** TECHNIQUE
**Tactic:** Defense Evasion
**Platform:** Windows

**Description:**
Adversaries may bypass process and/or signature-based defenses by proxying execution of malicious content with signed, or otherwise trusted, binaries.

**Sub-techniques:**
- **T1218.001:** Compiled HTML File
- **T1218.002:** Control Panel
- **T1218.003:** CMSTP
- **T1218.004:** InstallUtil
- **T1218.005:** Mshta
- **T1218.007:** Msiexec
- **T1218.008:** Odbcconf
- **T1218.009:** Regsvcs/Regasm
- **T1218.010:** Regsvr32
- **T1218.011:** Rundll32
- **T1218.012:** Verclsid
- **T1218.013:** Mavinject
- **T1218.014:** MMC

**Detection:**
- Monitor process execution
- Analyze command-line arguments
- Track network connections
- File system monitoring

**Mitigation:**
- Execution prevention
- Exploit protection

**Related CWE:** CWE-94 (Code Injection)
**Related CAPEC:** CAPEC-17 (Using Malicious Files)

**Procedure Examples:**
- **APT28:** Used rundll32 for execution
- **APT32:** Leveraged regsvr32 for bypass
- **Emotet:** Executed via rundll32
- **TrickBot:** Used mshta for script execution

### T1112: Modify Registry
**Entity Type:** TECHNIQUE
**Tactic:** Defense Evasion
**Platform:** Windows

**Description:**
Adversaries may interact with the Windows Registry to hide configuration information within Registry keys, remove information as part of cleaning up, or as part of other techniques to aid in persistence and execution.

**Detection:**
- Monitor Registry key changes
- Track process execution
- Analyze system logs
- Baseline Registry configuration

**Mitigation:**
- Restrict registry permissions
- User account management
- Audit

**Related CWE:** CWE-284 (Improper Access Control)
**Related CAPEC:** CAPEC-203 (Manipulate Registry Information)

**Procedure Examples:**
- **APT28:** Modified Registry for persistence
- **APT32:** Changed Registry settings for defense evasion
- **Carbanak:** Altered Registry keys
- **Emotet:** Modified Registry for autostart

### T1564: Hide Artifacts
**Entity Type:** TECHNIQUE
**Tactic:** Defense Evasion
**Platform:** Windows, Linux, macOS, Office 365

**Description:**
Adversaries may attempt to hide artifacts associated with their behaviors to evade detection.

**Sub-techniques:**
- **T1564.001:** Hidden Files and Directories
- **T1564.002:** Hidden Users
- **T1564.003:** Hidden Window
- **T1564.004:** NTFS File Attributes
- **T1564.005:** Hidden File System
- **T1564.006:** Run Virtual Instance
- **T1564.007:** VBA Stomping
- **T1564.008:** Email Hiding Rules
- **T1564.009:** Resource Forking
- **T1564.010:** Process Argument Spoofing

**Detection:**
- File system monitoring
- Process monitoring
- API monitoring
- User account monitoring

**Mitigation:**
- Limit file and directory permissions
- Operating system configuration

**Related CWE:** CWE-656 (Reliance on Security Through Obscurity)
**Related CAPEC:** CAPEC-168 (Windows ::DATA Alternate Data Stream)

**Procedure Examples:**
- **APT28:** Used hidden files and directories
- **APT32:** Created hidden users
- **Carbanak:** Hid artifacts using NTFS attributes
- **Turla:** Used hidden file systems

### T1140: Deobfuscate/Decode Files or Information
**Entity Type:** TECHNIQUE
**Tactic:** Defense Evasion
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may use obfuscated files or information to hide artifacts of an intrusion from analysis. They may then decode or deobfuscate that information in the course of execution.

**Detection:**
- Process monitoring
- File monitoring
- Network traffic analysis
- Process command-line parameters

**Mitigation:**
- Antivirus/antimalware

**Related CWE:** CWE-656 (Reliance on Security Through Obscurity)
**Related CAPEC:** CAPEC-267 (Leverage Alternate Encoding)

**Procedure Examples:**
- **APT28:** Deobfuscated Base64 encoded commands
- **APT29:** Decoded encrypted payloads at runtime
- **Emotet:** Decrypted configuration data
- **TrickBot:** Deobfuscated PowerShell scripts

### T1222: File and Directory Permissions Modification
**Entity Type:** TECHNIQUE
**Tactic:** Defense Evasion
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may modify file or directory permissions/attributes to evade access control lists (ACLs) and access protected files.

**Sub-techniques:**
- **T1222.001:** Windows File and Directory Permissions Modification
- **T1222.002:** Linux and Mac File and Directory Permissions Modification

**Detection:**
- Monitor for permission changes
- Track file access attempts
- Analyze system logs
- File system monitoring

**Mitigation:**
- Privileged account management
- Restrict file and directory permissions

**Related CWE:** CWE-732 (Incorrect Permission Assignment for Critical Resource)
**Related CAPEC:** CAPEC-1 (Accessing Functionality Not Properly Constrained by ACLs)

**Procedure Examples:**
- **APT32:** Modified file permissions
- **Rocke:** Changed directory permissions
- **TeamTNT:** Altered file attributes

## Cross-References

### Techniques with Multiple Tactics
- **T1053:** Execution, Persistence, Privilege Escalation
- **T1055:** Defense Evasion, Privilege Escalation
- **T1547:** Persistence, Privilege Escalation
- **T1543:** Persistence, Privilege Escalation
- **T1574:** Persistence, Privilege Escalation, Defense Evasion

### Common Attack Chains
1. **Execution → Persistence:** T1059 → T1053 → T1547
2. **Persistence → Defense Evasion:** T1543 → T1055 → T1027
3. **Defense Evasion Chain:** T1562 → T1070 → T1027

## Threat Actor Mapping
**Persistence:**
- **APT29:** T1098, T1136, T1547.001, T1053.005
- **APT32:** T1543.003, T1547.001, T1053.005
- **APT41:** T1098, T1136, T1053.005

**Defense Evasion:**
- **APT28:** T1027, T1036, T1070, T1112, T1218
- **APT32:** T1027, T1055, T1070, T1562
- **Emotet:** T1027, T1055, T1112, T1140, T1562

## Total Patterns in File: 500+
