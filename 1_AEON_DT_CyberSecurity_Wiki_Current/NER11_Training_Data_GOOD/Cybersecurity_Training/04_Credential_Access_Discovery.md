# MITRE ATT&CK: Credential Access and Discovery Tactics

## Credential Access Overview
Credential Access consists of techniques for stealing credentials like account names and passwords. Techniques used to get credentials include keylogging or credential dumping.

## Discovery Overview
Discovery consists of techniques an adversary may use to gain knowledge about the system and internal network. These techniques help adversaries observe the environment and orient themselves before deciding how to act.

---

## CREDENTIAL ACCESS TECHNIQUES

### T1003: OS Credential Dumping
**Entity Type:** TECHNIQUE
**Tactic:** Credential Access
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may attempt to dump credentials to obtain account login and credential material in the form of a hash or cleartext password from operating systems and software.

**Sub-techniques:**
- **T1003.001:** LSASS Memory
- **T1003.002:** Security Account Manager
- **T1003.003:** NTDS
- **T1003.004:** LSA Secrets
- **T1003.005:** Cached Domain Credentials
- **T1003.006:** DCSync
- **T1003.007:** Proc Filesystem
- **T1003.008:** /etc/passwd and /etc/shadow

**Detection:**
- Monitor process access to LSASS
- Track suspicious tool execution (Mimikatz, ProcDump)
- Analyze access to sensitive files
- Monitor DCSync operations

**Mitigation:**
- Credential Access Protection (Windows Defender)
- Privileged account management
- User account management
- Password policies

**Related CWE:** CWE-522 (Insufficiently Protected Credentials)
**Related CAPEC:** CAPEC-560 (Use of Known Domain Credentials)

**Procedure Examples:**
- **APT28:** Used Mimikatz for credential dumping
- **APT29:** Dumped LSASS process memory
- **APT32:** Extracted credentials from memory
- **FIN6:** Used ProcDump to dump LSASS
- **Carbanak:** Dumped SAM database

### T1003.001: LSASS Memory
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1003
**Platform:** Windows

**Description:**
Adversaries may attempt to access credential material stored in the Local Security Authority Subsystem Service (LSASS) process memory.

**Tools:**
- Mimikatz
- ProcDump
- Comsvcs.dll (MiniDump)
- Task Manager
- Dumpert

**Commands:**
```
mimikatz.exe "sekurlsa::logonpasswords" "exit"
procdump.exe -accepteula -ma lsass.exe lsass.dmp
rundll32.exe C:\windows\System32\comsvcs.dll, MiniDump [LSASS PID] lsass.dmp full
```

**Procedure Examples:**
- **APT28:** Extracted credentials from LSASS using Mimikatz
- **APT29:** Used customized credential dumpers
- **Carbanak:** Dumped LSASS memory multiple times

### T1003.003: NTDS
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1003
**Platform:** Windows

**Description:**
Adversaries may attempt to access or create a copy of the Active Directory domain database (NTDS.dit) to steal credential information.

**Methods:**
- NTDSUtil
- Volume Shadow Copy
- Direct file copy (offline)
- DCSync attack

**Commands:**
```
ntdsutil "ac i ntds" "ifm" "create full c:\temp" q q
vssadmin create shadow /for=C:
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\NTDS.dit
```

**Procedure Examples:**
- **APT28:** Extracted NTDS.dit from domain controllers
- **APT41:** Used volume shadow copies to access NTDS.dit
- **FIN6:** Dumped Active Directory database

### T1003.006: DCSync
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1003
**Platform:** Windows

**Description:**
Adversaries may attempt to abuse Directory Replication Service (DRS) to retrieve password hashes from domain controllers without needing local access.

**Requirements:**
- Domain admin or equivalent privileges
- Replicating Directory Changes permissions

**Tools:**
- Mimikatz
- Impacket secretsdump.py

**Commands:**
```
mimikatz.exe "lsadump::dcsync /domain:domain.com /user:Administrator" "exit"
secretsdump.py domain/user:password@DC01
```

**Procedure Examples:**
- **APT29:** Used DCSync to retrieve credentials
- **APT41:** Executed DCSync attacks
- **Wizard Spider:** Performed DCSync for lateral movement

### T1110: Brute Force
**Entity Type:** TECHNIQUE
**Tactic:** Credential Access
**Platform:** Windows, Linux, macOS, Office 365, SaaS, IaaS, Network, Google Workspace

**Description:**
Adversaries may use brute force techniques to gain access to accounts when passwords are unknown or when password hashes are obtained.

**Sub-techniques:**
- **T1110.001:** Password Guessing
- **T1110.002:** Password Cracking
- **T1110.003:** Password Spraying
- **T1110.004:** Credential Stuffing

**Detection:**
- Monitor failed authentication attempts
- Track account lockouts
- Analyze authentication logs
- Detect unusual login patterns

**Mitigation:**
- Multi-factor authentication
- Account use policies
- Password policies
- User account management

**Related CWE:** CWE-307 (Improper Restriction of Excessive Authentication Attempts)
**Related CAPEC:** CAPEC-49 (Password Brute Forcing), CAPEC-16 (Dictionary-based Password Attack)

**Procedure Examples:**
- **APT28:** Conducted password spray attacks
- **APT29:** Brute forced credentials
- **FIN7:** Used credential stuffing attacks
- **Lazarus Group:** Password guessing against services

### T1110.003: Password Spraying
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1110
**Platform:** Windows, Linux, macOS, Office 365, SaaS, Google Workspace

**Description:**
Adversaries may use a single or small list of commonly used passwords against many different accounts to attempt to acquire valid account credentials.

**Tools:**
- MailSniper
- DomainPasswordSpray
- Spray
- CrackMapExec

**Detection:**
- Multiple failed logins across different accounts
- Failed logins from single IP
- Time-based patterns

**Procedure Examples:**
- **APT28:** Password spraying against Office 365
- **APT29:** Sprayed credentials across cloud services
- **HEXANE:** Password spraying in targeted attacks

### T1555: Credentials from Password Stores
**Entity Type:** TECHNIQUE
**Tactic:** Credential Access
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may search for common password storage locations to obtain user credentials.

**Sub-techniques:**
- **T1555.001:** Keychain
- **T1555.002:** Securityd Memory
- **T1555.003:** Credentials from Web Browsers
- **T1555.004:** Windows Credential Manager
- **T1555.005:** Password Managers

**Detection:**
- Monitor access to credential stores
- Track file access patterns
- Process monitoring
- API monitoring

**Mitigation:**
- Password policies
- User training
- Operating system configuration

**Related CWE:** CWE-522 (Insufficiently Protected Credentials)
**Related CAPEC:** CAPEC-555 (Remote Services with Stolen Credentials)

**Procedure Examples:**
- **APT28:** Extracted browser credentials
- **APT33:** Accessed Windows Credential Manager
- **Lazarus Group:** Dumped browser passwords

### T1056: Input Capture
**Entity Type:** TECHNIQUE
**Tactic:** Collection, Credential Access
**Platform:** Windows, Linux, macOS, Network

**Description:**
Adversaries may use methods of capturing user input to obtain credentials or collect information.

**Sub-techniques:**
- **T1056.001:** Keylogging
- **T1056.002:** GUI Input Capture
- **T1056.003:** Web Portal Capture
- **T1056.004:** Credential API Hooking

**Detection:**
- Monitor for suspicious API calls
- Detect keylogger signatures
- Process monitoring
- Network traffic analysis

**Mitigation:**
- User training
- Multi-factor authentication
- Operating system configuration

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-568 (Capture Credentials via Keylogger)

**Procedure Examples:**
- **APT28:** Deployed keyloggers
- **APT32:** Used keylogging capabilities
- **Carbanak:** Captured credentials via keylogger
- **Gamaredon:** Implemented keylogging

### T1558: Steal or Forge Kerberos Tickets
**Entity Type:** TECHNIQUE
**Tactic:** Credential Access
**Platform:** Windows

**Description:**
Adversaries may attempt to subvert Kerberos authentication by stealing or forging Kerberos tickets to enable Pass the Ticket.

**Sub-techniques:**
- **T1558.001:** Golden Ticket
- **T1558.002:** Silver Ticket
- **T1558.003:** Kerberoasting
- **T1558.004:** AS-REP Roasting

**Detection:**
- Monitor Kerberos ticket requests
- Detect unusual TGT/TGS requests
- Track service ticket encryption types
- Analyze authentication logs

**Mitigation:**
- Active Directory configuration
- Privileged account management
- Password policies

**Related CWE:** CWE-287 (Improper Authentication)
**Related CAPEC:** CAPEC-645 (Use of Captured Tickets)

**Procedure Examples:**
- **APT28:** Created Golden Tickets
- **APT29:** Used Kerberos ticket manipulation
- **FIN7:** Performed Kerberoasting
- **Wizard Spider:** Forged Kerberos tickets

---

## DISCOVERY TECHNIQUES

### T1046: Network Service Discovery
**Entity Type:** TECHNIQUE
**Tactic:** Discovery
**Platform:** Windows, Linux, macOS, Network

**Description:**
Adversaries may attempt to get a listing of services running on remote hosts and local network infrastructure devices, including those that may be vulnerable to remote software exploitation.

**Tools:**
- Nmap
- Masscan
- Nessus
- Angry IP Scanner

**Commands:**
```
nmap -sV -p- target
masscan -p1-65535 target --rate=1000
```

**Detection:**
- Monitor for port scanning activity
- Detect unusual network traffic patterns
- Track service enumeration
- Network IDS alerts

**Mitigation:**
- Network segmentation
- Network intrusion prevention
- Disable unnecessary services
- Filter network traffic

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-300 (Port Scanning)

**Procedure Examples:**
- **APT1:** Scanned networks for open services
- **APT28:** Used Nmap for service discovery
- **APT41:** Performed network reconnaissance
- **FIN6:** Scanned for vulnerable services

### T1057: Process Discovery
**Entity Type:** TECHNIQUE
**Tactic:** Discovery
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may attempt to get information about running processes on a system.

**Commands:**
```
# Windows
tasklist
Get-Process
wmic process list

# Linux/macOS
ps aux
top
htop
```

**Detection:**
- Monitor process enumeration commands
- Track API calls (CreateToolhelp32Snapshot)
- Analyze command execution patterns

**Mitigation:**
- No effective mitigation (detection-focused)

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-569 (Collect Data as Provided by Users)

**Procedure Examples:**
- **APT1:** Enumerated running processes
- **APT28:** Used tasklist for process discovery
- **APT32:** Checked for security tools
- **Carbanak:** Monitored process list

### T1082: System Information Discovery
**Entity Type:** TECHNIQUE
**Tactic:** Discovery
**Platform:** Windows, Linux, macOS

**Description:**
An adversary may attempt to get detailed information about the operating system and hardware, including version, patches, hotfixes, service packs, and architecture.

**Commands:**
```
# Windows
systeminfo
wmic os get /all
ver
hostname
Get-ComputerInfo

# Linux/macOS
uname -a
cat /etc/os-release
hostname
lscpu
```

**Detection:**
- Monitor for system enumeration commands
- Track suspicious command sequences
- Analyze process execution

**Mitigation:**
- No effective mitigation (detection-focused)

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-569 (Collect Data as Provided by Users)

**Procedure Examples:**
- **APT1:** Gathered system information
- **APT28:** Collected OS details
- **APT32:** Enumerated system configuration
- **Emotet:** Checked system information

### T1083: File and Directory Discovery
**Entity Type:** TECHNIQUE
**Tactic:** Discovery
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may enumerate files and directories or may search in specific locations of a host or network share for certain information within a file system.

**Commands:**
```
# Windows
dir /s
tree
Get-ChildItem -Recurse
where /R C:\ filename

# Linux/macOS
ls -la
find / -name filename
locate filename
tree
```

**Detection:**
- Monitor file system enumeration
- Track directory traversal patterns
- Analyze command execution

**Mitigation:**
- No effective mitigation (detection-focused)

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-127 (Directory Indexing)

**Procedure Examples:**
- **APT1:** Searched for specific file types
- **APT28:** Enumerated directories
- **APT32:** Looked for documents
- **FIN6:** Searched for sensitive data

### T1087: Account Discovery
**Entity Type:** TECHNIQUE
**Tactic:** Discovery
**Platform:** Windows, Linux, macOS, Office 365, Azure AD, SaaS, Google Workspace

**Description:**
Adversaries may attempt to get a listing of accounts on a system or within an environment.

**Sub-techniques:**
- **T1087.001:** Local Account
- **T1087.002:** Domain Account
- **T1087.003:** Email Account
- **T1087.004:** Cloud Account

**Commands:**
```
# Windows
net user
net localgroup administrators
Get-LocalUser
Get-ADUser

# Linux/macOS
cat /etc/passwd
cat /etc/group
dscl . list /Users
```

**Detection:**
- Monitor account enumeration commands
- Track LDAP queries
- Analyze authentication logs
- Detect unusual queries

**Mitigation:**
- No effective mitigation (detection-focused)

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-575 (Account Footprinting)

**Procedure Examples:**
- **APT1:** Enumerated domain accounts
- **APT28:** Listed local administrators
- **APT32:** Discovered user accounts
- **FIN7:** Queried Active Directory

### T1135: Network Share Discovery
**Entity Type:** TECHNIQUE
**Tactic:** Discovery
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may look for folders and drives shared on remote systems as a means of identifying sources of information to gather.

**Commands:**
```
# Windows
net view \\computername
Get-SmbShare
net share

# Linux
showmount -e target
smbclient -L target
```

**Detection:**
- Monitor network share enumeration
- Track SMB traffic
- Analyze authentication to shares
- Network IDS signatures

**Mitigation:**
- Network segmentation
- Operating system configuration
- Password policies

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-643 (Identify Shared Files/Directories on System)

**Procedure Examples:**
- **APT1:** Enumerated network shares
- **APT28:** Discovered shared folders
- **APT32:** Mapped network drives
- **FIN6:** Searched for file shares

### T1018: Remote System Discovery
**Entity Type:** TECHNIQUE
**Tactic:** Discovery
**Platform:** Windows, Linux, macOS, Network

**Description:**
Adversaries may attempt to get a listing of other systems by IP address, hostname, or other logical identifier on a network.

**Commands:**
```
# Windows
net view
ping scan
arp -a
nltest /dclist

# Linux/macOS
arp -a
ping sweep
nmap -sn network/24
```

**Detection:**
- Monitor network enumeration commands
- Detect unusual network traffic
- Track DNS queries
- Network IDS alerts

**Mitigation:**
- Network segmentation
- Network intrusion prevention

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-292 (Host Discovery)

**Procedure Examples:**
- **APT1:** Discovered remote systems
- **APT28:** Enumerated network hosts
- **APT32:** Mapped internal networks
- **FIN6:** Identified target systems

### T1069: Permission Groups Discovery
**Entity Type:** TECHNIQUE
**Tactic:** Discovery
**Platform:** Windows, Linux, macOS, Office 365, Azure AD, Google Workspace

**Description:**
Adversaries may attempt to find group and permission settings to identify potential targets.

**Sub-techniques:**
- **T1069.001:** Local Groups
- **T1069.002:** Domain Groups
- **T1069.003:** Cloud Groups

**Commands:**
```
# Windows
net localgroup
net group /domain
Get-LocalGroupMember
Get-ADGroupMember

# Linux/macOS
groups
id
cat /etc/group
```

**Detection:**
- Monitor group enumeration commands
- Track LDAP queries
- Analyze command execution
- Cloud API monitoring

**Mitigation:**
- No effective mitigation (detection-focused)

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-575 (Account Footprinting)

**Procedure Examples:**
- **APT1:** Enumerated domain groups
- **APT28:** Listed local groups
- **APT32:** Discovered permissions
- **FIN7:** Queried group membership

### T1033: System Owner/User Discovery
**Entity Type:** TECHNIQUE
**Tactic:** Discovery
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may attempt to identify the primary user, currently logged in user, set of users that commonly uses a system, or whether a user is actively using the system.

**Commands:**
```
# Windows
whoami
query user
qwinsta
Get-Process -IncludeUserName

# Linux/macOS
whoami
w
who
users
```

**Detection:**
- Monitor user enumeration commands
- Track authentication logs
- Analyze command execution

**Mitigation:**
- No effective mitigation (detection-focused)

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-575 (Account Footprinting)

**Procedure Examples:**
- **APT1:** Identified logged-in users
- **APT28:** Determined system owner
- **APT32:** Checked current user
- **Emotet:** Enumerated user information

### T1007: System Service Discovery
**Entity Type:** TECHNIQUE
**Tactic:** Discovery
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may try to gather information about registered local system services.

**Commands:**
```
# Windows
sc query
Get-Service
tasklist /svc
net start

# Linux/macOS
systemctl list-units --type=service
service --status-all
launchctl list
```

**Detection:**
- Monitor service enumeration commands
- Track API calls (OpenSCManager)
- Analyze command execution

**Mitigation:**
- No effective mitigation (detection-focused)

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-574 (Services Footprinting)

**Procedure Examples:**
- **APT1:** Enumerated services
- **APT28:** Checked security services
- **APT32:** Listed running services
- **Carbanak:** Discovered installed services

## Cross-References

### Techniques Spanning Multiple Tactics
- **T1056:** Collection, Credential Access
- **T1057:** Discovery (supports Credential Access)
- **T1082:** Discovery (supports all tactics)

### Common Discovery Chains
1. **Initial Recon:** T1082 → T1033 → T1057 → T1083
2. **Network Mapping:** T1016 → T1018 → T1046 → T1135
3. **Privilege Mapping:** T1087 → T1069 → T1007

## Threat Actor Mapping
**Credential Access:**
- **APT28:** T1003, T1110.003, T1555, T1558
- **APT29:** T1003, T1110, T1558
- **FIN6:** T1003, T1555
- **Carbanak:** T1003, T1056

**Discovery:**
- **APT1:** T1046, T1057, T1082, T1083, T1087, T1135, T1018
- **APT28:** T1046, T1057, T1082, T1087, T1069
- **APT32:** T1057, T1082, T1083, T1087, T1135
- **FIN6:** T1046, T1083, T1087, T1135, T1018

## Total Patterns in File: 450+
