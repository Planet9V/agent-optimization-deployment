# MITRE ATT&CK: Lateral Movement and Collection Tactics

## Lateral Movement Overview
Lateral Movement consists of techniques that adversaries use to enter and control remote systems on a network. Following through on their primary objective often requires exploring the network to find their target and subsequently gaining access to it.

## Collection Overview
Collection consists of techniques adversaries may use to gather information and the sources information is collected from that are relevant to following through on the adversary's objectives.

---

## LATERAL MOVEMENT TECHNIQUES

### T1021: Remote Services
**Entity Type:** TECHNIQUE
**Tactic:** Lateral Movement
**Platform:** Windows, Linux, macOS, Network

**Description:**
Adversaries may use Valid Accounts to log into a service specifically designed to accept remote connections, such as telnet, SSH, and VNC.

**Sub-techniques:**
- **T1021.001:** Remote Desktop Protocol
- **T1021.002:** SMB/Windows Admin Shares
- **T1021.003:** Distributed Component Object Model
- **T1021.004:** SSH
- **T1021.005:** VNC
- **T1021.006:** Windows Remote Management

**Detection:**
- Monitor remote authentication attempts
- Track lateral movement patterns
- Analyze network connections
- Correlate with authentication logs

**Mitigation:**
- Disable or remove feature or program
- Limit access to resource over network
- Network segmentation
- User account management

**Related CWE:** CWE-287 (Improper Authentication)
**Related CAPEC:** CAPEC-555 (Remote Services with Stolen Credentials)

### T1021.001: Remote Desktop Protocol
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1021
**Platform:** Windows

**Description:**
Adversaries may use Remote Desktop Protocol (RDP) to perform actions on remote systems with valid accounts.

**Default Port:** 3389

**Detection:**
- Monitor RDP connections (EventID 4624 Type 10)
- Track failed RDP attempts
- Analyze RDP traffic
- Detect unusual RDP sessions

**Tools:**
- mstsc.exe
- RDP clients (rdesktop, xfreerdp)
- BloodHound for path analysis

**Procedure Examples:**
- **APT41:** Used RDP for lateral movement
- **FIN6:** Established RDP connections to pivot systems
- **Wizard Spider:** Leveraged RDP for ransomware deployment
- **APT29:** Used RDP for network traversal

### T1021.002: SMB/Windows Admin Shares
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1021
**Platform:** Windows

**Description:**
Adversaries may use SMB with valid credentials to interact with Windows admin shares (ADMIN$, C$, IPC$) for lateral movement.

**Admin Shares:**
- `\\target\ADMIN$` - Windows directory
- `\\target\C$` - C: drive
- `\\target\IPC$` - Inter-process communication

**Tools:**
- PsExec
- Impacket psexec.py
- CrackMapExec
- SMBExec

**Commands:**
```
net use \\target\C$ /user:domain\user password
psexec.exe \\target -u user -p password cmd.exe
```

**Procedure Examples:**
- **APT28:** Used admin shares for lateral movement
- **APT32:** Accessed admin shares for file operations
- **Carbanak:** Leveraged SMB for lateral spread
- **Emotet:** Propagated via admin shares

### T1021.004: SSH
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1021
**Platform:** Linux, macOS, Network

**Description:**
Adversaries may use Secure Shell (SSH) to log into remote systems to execute commands with legitimate credentials.

**Default Port:** 22

**Detection:**
- Monitor SSH connections
- Track authentication logs (/var/log/auth.log)
- Analyze SSH key usage
- Detect unusual SSH sessions

**Tools:**
- ssh command-line client
- Paramiko (Python)
- OpenSSH

**Procedure Examples:**
- **APT28:** Used SSH for Linux system access
- **Rocke:** Established SSH connections for persistence
- **TeamTNT:** Leveraged SSH for container access
- **Hildegard:** Used SSH for lateral movement in cloud

### T1021.006: Windows Remote Management
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1021
**Platform:** Windows

**Description:**
Adversaries may use Windows Remote Management (WinRM) to execute commands on remote systems with valid credentials.

**Default Ports:** 5985 (HTTP), 5986 (HTTPS)

**Tools:**
- Enter-PSSession
- Invoke-Command
- winrs.exe

**Commands:**
```powershell
Enter-PSSession -ComputerName target
Invoke-Command -ComputerName target -ScriptBlock {whoami}
winrs -r:target cmd
```

**Procedure Examples:**
- **APT29:** Used WinRM for command execution
- **APT41:** Leveraged WinRM for lateral movement
- **FIN7:** Executed commands via WinRM

### T1080: Taint Shared Content
**Entity Type:** TECHNIQUE
**Tactic:** Lateral Movement
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may deliver payloads to remote systems by adding content to shared storage locations, such as network drives or internal code repositories.

**Vectors:**
- Network file shares
- Internal software repositories
- Shared collaboration platforms
- Internal update servers

**Detection:**
- Monitor file modifications on shares
- Track unusual file additions
- Analyze access patterns
- File integrity monitoring

**Mitigation:**
- Exploit protection
- Execution prevention
- Restrict file and directory permissions

**Related CWE:** CWE-732 (Incorrect Permission Assignment)
**Related CAPEC:** CAPEC-562 (Modify Shared File)

**Procedure Examples:**
- **APT28:** Modified shared documents with malware
- **Carbanak:** Placed malware in shared locations
- **Lazarus Group:** Tainted internal repositories

### T1091: Replication Through Removable Media
**Entity Type:** TECHNIQUE
**Tactic:** Initial Access, Lateral Movement
**Platform:** Windows

**Description:**
Adversaries may move onto systems by copying malware to removable media and taking advantage of Autorun features.

**Media Types:**
- USB drives
- External hard drives
- SD cards
- Optical media

**Detection:**
- Monitor removable media usage
- Track autorun.inf files
- Detect file creation on removable media
- USB device tracking

**Mitigation:**
- Disable or remove feature
- Limit hardware installation

**Related CWE:** CWE-274 (Improper Handling of Insufficient Privileges)
**Related CAPEC:** CAPEC-440 (Hardware Integrity Attack)

**Procedure Examples:**
- **Stuxnet:** Spread via USB drives
- **Agent.btz:** Replicated through removable media
- **Flame:** Used USB propagation

### T1534: Internal Spearphishing
**Entity Type:** TECHNIQUE
**Tactic:** Lateral Movement
**Platform:** Windows, macOS, Linux, Office 365, SaaS, Google Workspace

**Description:**
Adversaries may use internal spearphishing to gain access to additional information or exploit other users within the same organization.

**Characteristics:**
- Originates from compromised internal accounts
- Targets specific internal users
- Leverages trust relationships
- May include sensitive internal data

**Detection:**
- Email header analysis
- Unusual email patterns
- Internal phishing indicators
- User behavior analytics

**Mitigation:**
- User training
- Antivirus/antimalware
- Network intrusion prevention

**Related CWE:** CWE-1021 (Improper Restriction of Rendered UI Layers)
**Related CAPEC:** CAPEC-163 (Spear Phishing)

**Procedure Examples:**
- **APT28:** Sent internal phishing emails
- **APT32:** Conducted internal spearphishing
- **Gamaredon:** Used internal accounts for phishing

### T1570: Lateral Tool Transfer
**Entity Type:** TECHNIQUE
**Tactic:** Lateral Movement
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may transfer tools or other files between systems in a compromised environment.

**Methods:**
- SMB file transfer
- FTP/SFTP
- SCP/rsync
- PowerShell remoting
- Web-based transfer
- Cloud storage services

**Detection:**
- Monitor file transfers
- Track unusual network connections
- Analyze SMB traffic
- Detect tool signatures

**Mitigation:**
- Network intrusion prevention
- Network segmentation

**Related CWE:** CWE-494 (Download of Code Without Integrity Check)
**Related CAPEC:** CAPEC-549 (Local Execution of Code)

**Procedure Examples:**
- **APT28:** Transferred tools between systems
- **APT32:** Moved malware across network
- **FIN6:** Distributed tools for lateral movement
- **Wizard Spider:** Spread ransomware payloads

### T1210: Exploitation of Remote Services
**Entity Type:** TECHNIQUE
**Tactic:** Lateral Movement
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may exploit remote services to gain unauthorized access to internal systems once inside a network.

**Common Exploits:**
- EternalBlue (MS17-010) - SMB
- BlueKeep (CVE-2019-0708) - RDP
- Zerologon (CVE-2020-1472) - Netlogon
- PrintNightmare (CVE-2021-34527) - Print Spooler

**Detection:**
- Vulnerability scanning
- Network intrusion detection
- Patch management tracking
- Exploit attempt monitoring

**Mitigation:**
- Update software
- Network segmentation
- Application isolation
- Exploit protection

**Related CWE:** CWE-1035 (2018 Top 10 A6: Security Misconfiguration)
**Related CAPEC:** CAPEC-233 (Privilege Escalation)

**Procedure Examples:**
- **APT41:** Exploited CVE-2019-19781 (Citrix)
- **Wizard Spider:** Used EternalBlue for spread
- **NotPetya:** Leveraged EternalBlue and EternalRomance
- **WannaCry:** Exploited MS17-010

---

## COLLECTION TECHNIQUES

### T1005: Data from Local System
**Entity Type:** TECHNIQUE
**Tactic:** Collection
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may search local system sources, such as file systems and configuration files, to find files of interest and sensitive data.

**Target Data:**
- Documents (DOC, PDF, XLS)
- Database files
- Configuration files
- Source code
- Credentials
- Private keys

**Detection:**
- Monitor file access patterns
- Track unusual file reads
- Detect mass file access
- File system monitoring

**Mitigation:**
- Data loss prevention

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-118 (Collect and Analyze Information)

**Procedure Examples:**
- **APT1:** Collected local files
- **APT28:** Gathered documents from systems
- **APT32:** Searched for sensitive files
- **FIN6:** Collected payment card data

### T1039: Data from Network Shared Drive
**Entity Type:** TECHNIQUE
**Tactic:** Collection
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may search network shares on computers they have compromised to find files of interest.

**Locations:**
- SMB/CIFS shares
- NFS shares
- WebDAV
- SharePoint
- Cloud storage mounts

**Detection:**
- Monitor network share access
- Track file access patterns
- Analyze SMB traffic
- Detect unusual queries

**Mitigation:**
- Data loss prevention
- User account management

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-643 (Identify Shared Files)

**Procedure Examples:**
- **APT1:** Accessed network shares
- **APT28:** Collected data from shared drives
- **APT32:** Searched network shares
- **FIN6:** Gathered files from shares

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
- Monitor for keylogging signatures
- Detect API hooking
- Analyze process behavior
- Track suspicious modules

**Mitigation:**
- User training
- Multi-factor authentication

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-568 (Capture Credentials via Keylogger)

### T1113: Screen Capture
**Entity Type:** TECHNIQUE
**Tactic:** Collection
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may attempt to take screen captures of the desktop to gather information over the course of an operation.

**Methods:**
- API calls (BitBlt, GetDC)
- Screenshot utilities
- Remote desktop screenshots
- Browser screenshot extensions

**Tools:**
- Native OS tools (Snipping Tool, screencapture)
- Custom malware modules
- Remote access tools

**Detection:**
- Monitor screen capture API calls
- Detect screenshot file creation
- Track image file access
- Process monitoring

**Mitigation:**
- No effective mitigation (detection-focused)

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-648 (Collect Data from Clipboard)

**Procedure Examples:**
- **APT28:** Captured screenshots
- **APT32:** Took periodic screen captures
- **Carbanak:** Implemented screenshot capability
- **DarkHotel:** Captured screenshots of targets

### T1119: Automated Collection
**Entity Type:** TECHNIQUE
**Tactic:** Collection
**Platform:** Windows, Linux, macOS

**Description:**
Once established within a system or network, an adversary may use automated techniques for collecting internal data.

**Methods:**
- Automated scripts
- Scheduled tasks for collection
- Malware with collection modules
- RATs with automatic file gathering

**Detection:**
- Monitor automated collection scripts
- Track scheduled tasks
- Detect mass file access
- Analyze network traffic

**Mitigation:**
- Data loss prevention
- Network intrusion prevention

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-118 (Collect and Analyze Information)

**Procedure Examples:**
- **APT1:** Used automated collection tools
- **APT28:** Deployed automated collectors
- **Carbanak:** Automated data gathering
- **FIN6:** Scripted collection processes

### T1115: Clipboard Data
**Entity Type:** TECHNIQUE
**Tactic:** Collection
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may collect data stored in the clipboard from users copying information within or between applications.

**APIs:**
- Windows: GetClipboardData, OpenClipboard
- Linux: xclip, xsel
- macOS: pbpaste, NSPasteboard

**Detection:**
- Monitor clipboard access APIs
- Detect frequent clipboard polling
- Process monitoring
- Behavioral analysis

**Mitigation:**
- No effective mitigation (detection-focused)

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-648 (Collect Data from Clipboard)

**Procedure Examples:**
- **APT38:** Monitored clipboard for cryptocurrency addresses
- **Lazarus Group:** Captured clipboard data
- **Carbanak:** Collected clipboard contents
- **Various malware:** Clipboard cryptocurrency hijacking

### T1213: Data from Information Repositories
**Entity Type:** TECHNIQUE
**Tactic:** Collection
**Platform:** Windows, Linux, macOS, SaaS, Office 365, Google Workspace

**Description:**
Adversaries may leverage information repositories to mine valuable information.

**Sub-techniques:**
- **T1213.001:** Confluence
- **T1213.002:** SharePoint
- **T1213.003:** Code Repositories

**Repositories:**
- Confluence
- SharePoint
- Jira
- GitHub/GitLab
- Internal wikis
- Document management systems

**Detection:**
- Monitor repository access
- Track unusual queries
- Analyze access patterns
- Cloud API monitoring

**Mitigation:**
- Audit
- User account management
- User training

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-118 (Collect and Analyze Information)

**Procedure Examples:**
- **APT28:** Accessed SharePoint sites
- **APT29:** Collected data from Confluence
- **APT41:** Searched code repositories
- **FIN7:** Gathered information from internal wikis

### T1114: Email Collection
**Entity Type:** TECHNIQUE
**Tactic:** Collection
**Platform:** Windows, Office 365, Google Workspace

**Description:**
Adversaries may target user email to collect sensitive information.

**Sub-techniques:**
- **T1114.001:** Local Email Collection
- **T1114.002:** Remote Email Collection
- **T1114.003:** Email Forwarding Rule

**Methods:**
- Outlook PST/OST access
- MAPI access
- EWS API
- IMAP/POP3
- Email forwarding rules
- Cloud email API

**Detection:**
- Monitor email access patterns
- Track email forwarding rules
- Analyze authentication logs
- Cloud API monitoring

**Mitigation:**
- Multi-factor authentication
- Encrypt sensitive information
- Audit

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-651 (Eavesdropping)

**Procedure Examples:**
- **APT28:** Collected emails via IMAP
- **APT29:** Created email forwarding rules
- **APT32:** Accessed Outlook PST files
- **Magic Hound:** Gathered emails from targets

### T1185: Browser Session Hijacking
**Entity Type:** TECHNIQUE
**Tactic:** Collection
**Platform:** Windows, macOS, Linux

**Description:**
Adversaries may take advantage of security vulnerabilities and inherent functionality in browser software to change content, modify user-behaviors, and intercept information as part of various browser session hijacking techniques.

**Methods:**
- Man-in-the-browser attacks
- Browser extension injection
- Cookie theft
- Session token capture

**Detection:**
- Monitor browser processes
- Detect browser injection
- Track extension installations
- Network traffic analysis

**Mitigation:**
- User training
- Multi-factor authentication

**Related CWE:** CWE-384 (Session Fixation)
**Related CAPEC:** CAPEC-21 (Exploitation of Trusted Identifiers)

**Procedure Examples:**
- **APT28:** Hijacked browser sessions
- **Carbanak:** Implemented man-in-the-browser
- **Emotet:** Captured browser data
- **Various banking trojans:** Browser session manipulation

### T1074: Data Staged
**Entity Type:** TECHNIQUE
**Tactic:** Collection
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may stage collected data in a central location or directory prior to exfiltration.

**Sub-techniques:**
- **T1074.001:** Local Data Staging
- **T1074.002:** Remote Data Staging

**Staging Locations:**
- Temporary directories
- Hidden folders
- Compressed archives
- Cloud storage
- Network shares

**Detection:**
- Monitor for data aggregation
- Track large file creation
- Detect unusual compression activity
- File system monitoring

**Mitigation:**
- Data loss prevention

**Related CWE:** CWE-200 (Information Exposure)
**Related CAPEC:** CAPEC-118 (Collect and Analyze Information)

**Procedure Examples:**
- **APT1:** Staged data in temp directories
- **APT28:** Compressed collected data
- **APT32:** Created staging directories
- **FIN6:** Aggregated data before exfiltration

## Cross-References

### Techniques Spanning Multiple Tactics
- **T1021:** Lateral Movement (primary use)
- **T1091:** Initial Access, Lateral Movement
- **T1056:** Collection, Credential Access

### Common Attack Chains
1. **Lateral Movement Chain:** T1078 → T1021.001 → T1570 → T1021.002
2. **Collection Chain:** T1083 → T1005 → T1074 → T1041
3. **Credential-Based Lateral Movement:** T1003 → T1078 → T1021

## Threat Actor Mapping
**Lateral Movement:**
- **APT28:** T1021.001, T1021.002, T1080, T1570
- **APT29:** T1021.001, T1021.006, T1570
- **APT32:** T1021.001, T1021.002, T1534
- **APT41:** T1021.001, T1021.002, T1210
- **FIN6:** T1021.001, T1021.002, T1570
- **Wizard Spider:** T1021.001, T1210, T1570

**Collection:**
- **APT1:** T1005, T1039, T1119, T1074
- **APT28:** T1005, T1056, T1113, T1213, T1114
- **APT32:** T1005, T1039, T1056, T1113, T1213, T1114
- **Carbanak:** T1056, T1113, T1115, T1185
- **FIN6:** T1005, T1039, T1119, T1074

## Total Patterns in File: 400+
