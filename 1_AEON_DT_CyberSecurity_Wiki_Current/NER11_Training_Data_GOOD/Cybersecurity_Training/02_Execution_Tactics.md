# MITRE ATT&CK: Execution Tactics

## Overview
The Execution tactic represents techniques that result in adversary-controlled code running on a local or remote system. Techniques that run malicious code are often paired with techniques from all other tactics to achieve broader goals.

## Techniques

### T1059: Command and Scripting Interpreter
**Entity Type:** TECHNIQUE
**Tactic:** Execution
**Platform:** Windows, Linux, macOS, Network

**Description:**
Adversaries may abuse command and script interpreters to execute commands, scripts, or binaries. These interfaces and languages provide ways of interacting with computer systems and are a common feature across many different platforms.

**Sub-techniques:**
- **T1059.001:** PowerShell
- **T1059.002:** AppleScript
- **T1059.003:** Windows Command Shell
- **T1059.004:** Unix Shell
- **T1059.005:** Visual Basic
- **T1059.006:** Python
- **T1059.007:** JavaScript
- **T1059.008:** Network Device CLI

**Detection:**
- Monitor process execution
- Command-line argument analysis
- Script block logging (PowerShell)
- Behavioral analysis

**Mitigation:**
- Execution prevention
- Disable or remove unnecessary interpreters
- Code signing requirements
- Application control policies

**Related CWE:** CWE-94 (Code Injection), CWE-78 (OS Command Injection)
**Related CAPEC:** CAPEC-242 (Code Injection), CAPEC-88 (OS Command Injection)

### T1059.001: PowerShell
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1059
**Tactic:** Execution
**Platform:** Windows

**Description:**
Adversaries may abuse PowerShell commands and scripts for execution. PowerShell is a powerful interactive command-line interface and scripting environment included in Windows.

**Common Uses:**
- Download and execute payloads
- Fileless malware execution
- Reconnaissance commands
- Credential dumping
- Lateral movement

**Detection:**
- Enable PowerShell script block logging
- Monitor PowerShell execution arguments
- Detect obfuscated commands
- Track network connections from PowerShell

**Procedure Examples:**
- **APT29:** Used PowerShell for post-exploitation activities
- **APT32:** Leveraged PowerShell to download additional payloads
- **FIN7:** Used obfuscated PowerShell scripts
- **Empire Framework:** Post-exploitation agent uses PowerShell
- **Mimikatz:** Often executed via PowerShell (Invoke-Mimikatz)

### T1059.003: Windows Command Shell
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1059
**Platform:** Windows

**Description:**
Adversaries may abuse the Windows command shell for execution. The Windows command shell (cmd.exe) is the primary command-line interpreter on Windows systems.

**Common Commands:**
- `net user` - User account enumeration
- `net localgroup` - Group membership
- `ipconfig` - Network configuration
- `systeminfo` - System information
- `tasklist` - Process enumeration
- `wmic` - WMI command-line utility

**Procedure Examples:**
- **APT1:** Used cmd.exe for system enumeration
- **Cobalt Strike:** Beacon executes commands via cmd.exe
- **TA505:** Used batch files with cmd.exe

### T1059.004: Unix Shell
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1059
**Platform:** Linux, macOS

**Description:**
Adversaries may abuse Unix shell commands and scripts for execution. Unix shells are command-line interpreters that provide a traditional user interface for Unix-like systems.

**Common Shells:**
- bash (Bourne Again Shell)
- sh (Bourne Shell)
- zsh (Z Shell)
- csh (C Shell)
- ksh (Korn Shell)

**Detection:**
- Monitor shell execution
- Analyze command history files (.bash_history)
- Track unusual shell spawning
- Monitor script execution

**Procedure Examples:**
- **APT28:** Used bash scripts for Linux malware
- **Rocke:** Used shell scripts for cryptomining
- **TeamTNT:** Leveraged bash for container compromise

### T1059.006: Python
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1059
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may abuse Python commands and scripts for execution. Python is a popular high-level programming language available on various platforms.

**Common Uses:**
- Custom exploitation frameworks
- Data exfiltration scripts
- Network scanning tools
- Credential harvesting

**Procedure Examples:**
- **APT41:** Used Python-based backdoors
- **Machete:** Malware written in Python
- **Pupy RAT:** Python-based remote access tool

### T1053: Scheduled Task/Job
**Entity Type:** TECHNIQUE
**Tactic:** Execution, Persistence, Privilege Escalation
**Platform:** Windows, Linux, macOS, Network

**Description:**
Adversaries may abuse task scheduling functionality to facilitate initial or recurring execution of malicious code. Task scheduling can be used to establish persistence, conduct remote execution, or as a privilege escalation technique.

**Sub-techniques:**
- **T1053.002:** At (Linux/macOS)
- **T1053.003:** Cron
- **T1053.005:** Scheduled Task (Windows)
- **T1053.006:** Systemd Timers
- **T1053.007:** Container Orchestration Job

**Detection:**
- Monitor scheduled task creation
- Track modifications to cron files
- Analyze task trigger patterns
- Correlate with other suspicious activities

**Mitigation:**
- User account management
- Privileged account management
- Operating system configuration
- Audit policy configuration

**Related CWE:** CWE-732 (Incorrect Permission Assignment for Critical Resource)
**Related CAPEC:** CAPEC-557 (Malicious Automated Software Update via Spoofing)

### T1053.005: Scheduled Task
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1053
**Platform:** Windows

**Description:**
Adversaries may abuse the Windows Task Scheduler to perform task scheduling for initial or recurring execution of malicious code.

**Tools:**
- schtasks.exe
- Task Scheduler GUI
- PowerShell (New-ScheduledTask)

**Procedure Examples:**
- **APT29:** Created scheduled tasks for persistence
- **APT41:** Used scheduled tasks to execute malware
- **TA505:** Scheduled tasks for payload execution
- **Emotet:** Created scheduled tasks after initial infection

### T1053.003: Cron
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1053
**Platform:** Linux, macOS

**Description:**
Adversaries may abuse the cron utility to perform task scheduling for initial or recurring execution of malicious code.

**Cron Files:**
- /etc/crontab
- /etc/cron.d/*
- /var/spool/cron/crontabs/*
- User crontabs (crontab -e)

**Procedure Examples:**
- **Rocke:** Modified cron to maintain persistence
- **TeamTNT:** Used cron for cryptomining persistence
- **Hildegard:** Scheduled malicious tasks via cron

### T1204: User Execution
**Entity Type:** TECHNIQUE
**Tactic:** Execution
**Platform:** Windows, Linux, macOS

**Description:**
An adversary may rely upon specific actions by a user in order to gain execution. Users may be subjected to social engineering to get them to execute malicious code.

**Sub-techniques:**
- **T1204.001:** Malicious Link
- **T1204.002:** Malicious File

**Detection:**
- Monitor process execution from user interaction
- Analyze file downloads
- Track browser history and web activity
- Email gateway monitoring

**Mitigation:**
- User training
- Execution prevention
- Network intrusion prevention
- Restrict web-based content

**Related CWE:** CWE-1021 (Improper Restriction of Rendered UI Layers)
**Related CAPEC:** CAPEC-163 (Spear Phishing)

### T1204.002: Malicious File
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1204
**Platform:** Windows, Linux, macOS

**Description:**
An adversary may rely upon a user opening a malicious file in order to gain execution. Malicious files may be attached to emails or delivered via removable media.

**File Types:**
- Microsoft Office documents (DOC, XLS, PPT)
- PDF documents with exploits
- Archive files (ZIP, RAR, 7Z)
- Executables disguised as documents
- Script files (VBS, JS, PS1)

**Procedure Examples:**
- **APT28:** Delivered malicious documents via email
- **TA505:** Used weaponized Office documents
- **Gamaredon:** Distributed malicious files via phishing

### T1569: System Services
**Entity Type:** TECHNIQUE
**Tactic:** Execution
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may abuse system services or daemons to execute commands or programs. Services are used to configure automatic execution of programs at startup or on a scheduled basis.

**Sub-techniques:**
- **T1569.001:** Launchctl
- **T1569.002:** Service Execution

**Detection:**
- Monitor service creation and modification
- Track service execution patterns
- Analyze service configuration files
- Correlate with process execution

**Mitigation:**
- User account management
- Restrict service creation
- Privileged account management

**Related CWE:** CWE-284 (Improper Access Control)
**Related CAPEC:** CAPEC-17 (Using Malicious Files)

### T1569.002: Service Execution
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1569
**Platform:** Windows

**Description:**
Adversaries may abuse the Windows service control manager to execute malicious commands or payloads.

**Tools:**
- sc.exe
- PsExec
- Services.msc
- PowerShell (Start-Service)

**Procedure Examples:**
- **APT32:** Created services for malware execution
- **APT41:** Used service execution for lateral movement
- **Wizard Spider:** Deployed ransomware via services

### T1047: Windows Management Instrumentation
**Entity Type:** TECHNIQUE
**Tactic:** Execution
**Platform:** Windows

**Description:**
Adversaries may abuse Windows Management Instrumentation (WMI) to execute malicious commands and payloads. WMI is a Windows administration feature that provides a uniform environment for access to various management information.

**Detection:**
- Monitor WMI event subscriptions
- Track WMI process execution
- Analyze WMI command-line usage
- Detect unusual WMI queries

**Mitigation:**
- User account management
- Privileged account management
- Execution prevention

**Related CWE:** CWE-94 (Code Injection)
**Related CAPEC:** CAPEC-242 (Code Injection)

**Procedure Examples:**
- **APT29:** Used WMI for lateral movement and execution
- **APT32:** Leveraged WMI for persistence
- **FIN7:** Executed commands via WMI
- **Lazarus Group:** Used WMI for payload execution

### T1106: Native API
**Entity Type:** TECHNIQUE
**Tactic:** Execution
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may interact with the native OS application programming interface (API) to execute behaviors. Native APIs provide a controlled means of calling low-level OS services within the kernel.

**Windows APIs:**
- CreateProcess/CreateProcessAsUser
- VirtualAlloc/VirtualAllocEx
- WriteProcessMemory
- CreateRemoteThread
- NtCreateThreadEx

**Linux APIs:**
- fork/exec
- mmap/mprotect
- ptrace
- dlopen/dlsym

**Detection:**
- Monitor API call patterns
- Detect unusual API sequences
- Track memory allocation patterns
- Analyze process injection behaviors

**Mitigation:**
- Execution prevention
- Behavior prevention on endpoint
- Exploit protection

**Related CWE:** CWE-829 (Inclusion of Functionality from Untrusted Control Sphere)
**Related CAPEC:** CAPEC-588 (DOM-Based XSS)

**Procedure Examples:**
- **APT28:** Used Windows APIs for malware execution
- **Carbanak:** Leveraged CreateRemoteThread for injection
- **Emotet:** Used native APIs for process injection

### T1203: Exploitation for Client Execution
**Entity Type:** TECHNIQUE
**Tactic:** Execution
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may exploit software vulnerabilities in client applications to execute code. Vulnerabilities can exist in software due to improper input validation, memory management issues, or other flaws.

**Target Applications:**
- Web browsers
- Microsoft Office
- Adobe Reader
- Java Runtime Environment
- Media players

**Detection:**
- Exploit protection mechanisms
- Application crash monitoring
- Behavioral analysis
- Memory scanning

**Mitigation:**
- Application isolation and sandboxing
- Exploit protection
- Update software

**Related CWE:** CWE-119 (Buffer Overflow), CWE-416 (Use After Free)
**Related CAPEC:** CAPEC-100 (Overflow Buffers)

**Procedure Examples:**
- **APT28:** Exploited CVE-2017-11882 (Microsoft Office)
- **Darkhotel:** Used Adobe Flash exploits
- **Elderwood:** Exploited Internet Explorer vulnerabilities

### T1559: Inter-Process Communication
**Entity Type:** TECHNIQUE
**Tactic:** Execution
**Platform:** Windows, Linux, macOS

**Description:**
Adversaries may abuse inter-process communication (IPC) mechanisms for local code or command execution. IPC is typically used for communication between processes on the same system.

**Sub-techniques:**
- **T1559.001:** Component Object Model
- **T1559.002:** Dynamic Data Exchange

**Detection:**
- Monitor IPC mechanisms
- Track COM object instantiation
- Analyze DDE execution
- Detect unusual IPC patterns

**Mitigation:**
- Application isolation and sandboxing
- Behavior prevention on endpoint
- Disable or remove feature

**Related CWE:** CWE-829 (Inclusion of Functionality from Untrusted Control Sphere)
**Related CAPEC:** CAPEC-17 (Using Malicious Files)

### T1559.001: Component Object Model
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1559
**Platform:** Windows

**Description:**
Adversaries may use the Windows Component Object Model (COM) for local code execution. COM is an inter-process communication (IPC) component of the Windows API.

**Common COM Objects:**
- WScript.Shell
- Excel.Application
- Word.Application
- Outlook.Application
- InternetExplorer.Application

**Procedure Examples:**
- **APT28:** Used COM for lateral movement
- **Emotet:** Leveraged COM objects for execution
- **TA505:** Abused COM for payload execution

### T1559.002: Dynamic Data Exchange
**Entity Type:** SUB-TECHNIQUE
**Parent Technique:** T1559
**Platform:** Windows

**Description:**
Adversaries may use Windows Dynamic Data Exchange (DDE) to execute arbitrary commands. DDE is a client-server protocol for one-time and/or continuous inter-process communication.

**Applications:**
- Microsoft Office (Word, Excel, Outlook)
- Windows applications supporting DDE

**Procedure Examples:**
- **APT28:** Used DDE in phishing documents
- **FIN7:** Leveraged DDE for execution
- **TA505:** Distributed DDE-based documents

### T1648: Serverless Execution
**Entity Type:** TECHNIQUE
**Tactic:** Execution
**Platform:** SaaS, IaaS

**Description:**
Adversaries may abuse serverless computing, integration, and automation services to execute arbitrary code in cloud environments. Serverless architectures may enable execution with no visible infrastructure to traditional monitoring systems.

**Services:**
- AWS Lambda
- Azure Functions
- Google Cloud Functions
- AWS Step Functions

**Detection:**
- Monitor function invocation logs
- Track function creation/modification
- Analyze execution patterns
- Review IAM policies

**Mitigation:**
- User account management
- Execution prevention
- Network segmentation

**Related CWE:** CWE-94 (Code Injection)
**Related CAPEC:** CAPEC-242 (Code Injection)

**Procedure Examples:**
- **TeamTNT:** Abused AWS Lambda for cryptomining
- Various threat actors: Used serverless for C2 infrastructure

### T1609: Container Administration Command
**Entity Type:** TECHNIQUE
**Tactic:** Execution
**Platform:** Containers

**Description:**
Adversaries may abuse a container administration service to execute commands within a container. Container administration services such as the Docker daemon provide APIs that allow users to interact with containers.

**Tools:**
- docker exec
- kubectl exec
- docker API
- Kubernetes API

**Detection:**
- Monitor container exec commands
- Track API calls to container services
- Analyze container logs
- Detect unusual container activity

**Mitigation:**
- Network segmentation
- User account management
- Privileged account management
- Limit software installation

**Related CWE:** CWE-284 (Improper Access Control)
**Related CAPEC:** CAPEC-558 (Replace Trusted Executable)

**Procedure Examples:**
- **TeamTNT:** Used docker exec for container compromise
- **Hildegard:** Executed commands in Kubernetes containers
- **Kinsing:** Abused container APIs for cryptomining

## Cross-References

### Relationship to Other Tactics
- **Persistence:** T1053 (Scheduled Task/Job)
- **Privilege Escalation:** T1053 (Scheduled Task/Job)
- **Defense Evasion:** T1059 (Command and Scripting Interpreter)

### Common Execution Chains
1. **Initial Access → Execution:** T1566 → T1204 → T1059
2. **Persistence → Execution:** T1053 → T1059
3. **Lateral Movement → Execution:** T1021 → T1047 → T1059

## Threat Actor Mapping
- **APT28:** T1059.001, T1047, T1053.005, T1203
- **APT29:** T1059.001, T1047, T1053.005, T1106
- **APT32:** T1059.001, T1569.002, T1047
- **FIN7:** T1059.001, T1047, T1559.002
- **TA505:** T1059.001, T1053.005, T1204.002

## Total Patterns in File: 400+
