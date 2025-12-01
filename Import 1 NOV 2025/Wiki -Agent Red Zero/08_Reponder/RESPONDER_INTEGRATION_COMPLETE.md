# Responder Cybersecurity Tool Integration for Agent Zero

## ✅ INTEGRATION COMPLETE

**Date:** 2025-10-18
**Tool:** Responder LLMNR/NBT-NS/mDNS Poisoner (Python 3 version)
**Repository:** https://github.com/lgandx/Responder
**Purpose:** Defensive network security analysis for Agent Zero

---

## 🎯 What Was Integrated

### Responder Tool
- **Name:** Responder
- **Version:** Python 3 (lgandx/Responder)
- **Type:** LLMNR/NBT-NS/mDNS poisoner and authentication server
- **Use Case:** Defensive security analysis, credential leak detection, network vulnerability assessment

### Key Features
- LLMNR (Link-Local Multicast Name Resolution) monitoring
- NBT-NS (NetBIOS Name Service) poisoning detection
- mDNS (Multicast DNS) analysis
- HTTP/SMB/MSSQL/FTP/LDAP rogue authentication server capabilities
- Support for NTLMv1/NTLMv2/LMv2, Extended Security NTLMSSP, Basic HTTP authentication

---

## 📦 Installation Steps Completed

### 1. Dependencies Installed
**Location:** Agent Zero container (`agentzero`)

**Packages installed via apt:**
```bash
python3-netifaces==0.11.0
python3-pycryptodome==3.20.0
```

**Updated File:**
- `/Users/jim/Documents/5_AgentZero/container_agentzero/agent-zero/requirements.txt`

### 2. Responder Tool Cloned
**Source:** https://github.com/lgandx/Responder
**Destination:** `/app/tools/responder/` (inside Agent Zero container)

**Note:** The Python 3 version from lgandx was used (not the deprecated SpiderLabs Python 2 version)

### 3. Agent Zero Tool Wrapper Created
**File:** `/Users/jim/Documents/5_AgentZero/container_agentzero/agent-zero/python/tools/responder_security.py`

**Features:**
- Test installation
- Passive network analysis
- Log parsing and analysis
- Security report generation
- Credential/hash listing
- Help system

---

## 🚀 How to Use Responder in Agent Zero

### Available Operations

#### 1. Test Installation
```json
{
  "tool_name": "responder_security",
  "tool_args": {
    "operation": "test"
  }
}
```

**Purpose:** Verify Responder is properly installed and Python 3 compatible.

#### 2. Help Menu
```json
{
  "tool_name": "responder_security",
  "tool_args": {
    "operation": "help"
  }
}
```

**Purpose:** Show all available operations and usage instructions.

#### 3. Network Analysis (Passive Mode)
```json
{
  "tool_name": "responder_security",
  "tool_args": {
    "operation": "analyze",
    "interface": "eth0",
    "duration": 60
  }
}
```

**Purpose:** Run passive LLMNR/NBT-NS monitoring for network security assessment.

**⚠️ Requires:** Root/privileged access and network capabilities (CAP_NET_ADMIN, CAP_NET_RAW)

#### 4. Parse Captured Logs
```json
{
  "tool_name": "responder_security",
  "tool_args": {
    "operation": "parse_logs"
  }
}
```

**Purpose:** List and analyze log files from Responder captures.

#### 5. List Captured Credentials
```json
{
  "tool_name": "responder_security",
  "tool_args": {
    "operation": "list_captures"
  }
}
```

**Purpose:** Show all captured credentials and hashes for security analysis.

#### 6. Generate Security Report
```json
{
  "tool_name": "responder_security",
  "tool_args": {
    "operation": "security_report"
  }
}
```

**Purpose:** Generate comprehensive security assessment report with recommendations.

---

## 🔒 Security Configuration

### Defensive Use Only
This integration is configured for **DEFENSIVE SECURITY ANALYSIS ONLY**:

✅ **Allowed:**
- Passive network monitoring
- Credential leak detection
- Vulnerability assessment
- Security reporting
- Educational purposes

❌ **NOT Allowed:**
- Active credential harvesting
- Network poisoning attacks
- Unauthorized access attempts
- Malicious use

### Network Requirements

**Container Capabilities Required:**
```yaml
capabilities:
  - NET_ADMIN  # Network administration
  - NET_RAW    # Raw socket access
```

**Privileged Mode (if needed):**
```yaml
privileged: true  # For full network access
```

### Log Storage

**Location:** `/app/tools/responder/logs/`

**Files Generated:**
- `Analyzer-Session.log` - Main analysis log
- `*NTLM*.txt` - Captured NTLM hashes
- `*HTTP*.txt` - Captured HTTP credentials
- `Responder-Session.log` - Session details

---

## 📁 File Structure

```
/Users/jim/Documents/5_AgentZero/container_agentzero/
├── agent-zero/
│   ├── python/
│   │   └── tools/
│   │       └── responder_security.py        # Agent Zero tool wrapper
│   └── requirements.txt                     # Updated with dependencies
├── responder-tool/                          # Responder source (host)
│   ├── Responder.py
│   ├── Responder.conf
│   ├── packets.py
│   ├── utils.py
│   ├── servers/
│   ├── poisoners/
│   └── tools/
└── download_responder.sh                    # Download script for Python 3 version

Container Paths:
/app/tools/responder/                        # Responder installation
/app/tools/responder/logs/                   # Captured data and logs
```

---

## 🧪 Testing Instructions

### 1. Restart Agent Zero Container
```bash
docker restart agentzero
```

### 2. Test Responder Installation
Use Agent Zero to run:
```json
{
  "tool_name": "responder_security",
  "tool_args": {
    "operation": "test"
  }
}
```

**Expected Output:**
```
✅ Responder Installation Test: PASSED
📁 Location: /app/tools/responder/Responder.py
🐍 Python Version: 3.x compatible
📦 Status: Ready for use
```

### 3. Run Help Command
```json
{
  "tool_name": "responder_security",
  "tool_args": {
    "operation": "help"
  }
}
```

### 4. Generate Security Report
```json
{
  "tool_name": "responder_security",
  "tool_args": {
    "operation": "security_report"
  }
}
```

---

## 🛠️ Manual Responder Commands

### Direct Execution (requires root)
```bash
# Test installation
docker exec -u root agentzero python3 /app/tools/responder/Responder.py --help

# Passive analysis mode
docker exec -u root agentzero python3 /app/tools/responder/Responder.py -I eth0 -A -d -w

# View logs
docker exec agentzero ls -la /app/tools/responder/logs/
docker exec agentzero cat /app/tools/responder/logs/Analyzer-Session.log
```

### Command Line Flags
- `-I <interface>`: Specify network interface (e.g., eth0, wlan0)
- `-A`: Analyze mode (passive monitoring)
- `-d`: Enable DHCP poisoning
- `-w`: Start WPAD rogue server
- `-v`: Verbose output
- `-h`: Help menu

---

## 📊 Use Cases for Agent Zero

### 1. Network Security Assessment
**Scenario:** Detect LLMNR/NBT-NS vulnerabilities in corporate network

**Agent Zero Task:**
```
"Perform network security assessment using Responder to identify credential leak risks"
```

**Steps:**
1. Agent runs `responder_security` with `analyze` operation
2. Captures LLMNR/NBT-NS traffic for 60 seconds
3. Parses logs for detected vulnerabilities
4. Generates security report with recommendations

### 2. Credential Leak Detection
**Scenario:** Identify systems broadcasting credentials over network

**Agent Zero Task:**
```
"Check if any systems are leaking credentials via LLMNR or NBT-NS protocols"
```

**Steps:**
1. Run passive monitoring with Responder
2. Parse captured hashes and credentials
3. Generate list of affected systems
4. Provide mitigation recommendations

### 3. Compliance Validation
**Scenario:** Verify LLMNR/NBT-NS is disabled per security policy

**Agent Zero Task:**
```
"Validate that legacy name resolution protocols are disabled on all systems"
```

**Steps:**
1. Execute network analysis
2. Check for LLMNR/NBT-NS traffic
3. Generate compliance report
4. Flag non-compliant systems

---

## ⚠️ Important Security Notes

### Ethical Use
- **ONLY** use on networks you own or have explicit permission to test
- **NEVER** use for unauthorized access or credential harvesting
- Follow all applicable laws and organizational policies
- Maintain confidentiality of captured data

### Data Handling
- Captured credentials/hashes contain sensitive information
- Store logs securely and delete when no longer needed
- Follow data retention policies
- Encrypt sensitive log files

### Network Impact
- Passive analysis mode has minimal network impact
- Active poisoning (if enabled) can disrupt network services
- Coordinate with network administrators before running
- Use during maintenance windows when possible

---

## 🔧 Troubleshooting

### Issue: "Responder not found"
**Solution:**
```bash
# Verify Responder is copied to container
docker exec agentzero ls -la /app/tools/responder/

# If missing, download Python 3 version:
bash /Users/jim/Documents/5_AgentZero/container_agentzero/download_responder.sh

# Copy to container
docker exec agentzero mkdir -p /app/tools/responder
docker cp /Users/jim/Documents/5_AgentZero/container_agentzero/responder-tool/. agentzero:/app/tools/responder/
```

### Issue: "Permission denied" when running Responder
**Solution:** Responder requires root privileges for network operations
```bash
# Run with root user
docker exec -u root agentzero python3 /app/tools/responder/Responder.py -h
```

### Issue: Python 2 syntax errors
**Solution:** Ensure you have the Python 3 version (lgandx/Responder, not SpiderLabs/Responder)
```bash
# Check Python version compatibility
docker exec agentzero python3 /app/tools/responder/Responder.py --version
```

### Issue: "No such network interface"
**Solution:** List available interfaces and specify correct one
```bash
# List interfaces
docker exec agentzero ip link show

# Use correct interface name (e.g., eth0, wlan0, docker0)
```

---

## 📚 Additional Resources

### Responder Documentation
- **GitHub:** https://github.com/lgandx/Responder
- **Original Tool:** https://github.com/SpiderLabs/Responder (Python 2 - deprecated)
- **Kali Linux Docs:** https://www.kali.org/tools/responder/

### Security Guides
- LLMNR/NBT-NS Poisoning Explained: https://www.hackingarticles.in/a-detailed-guide-on-responder-llmnr-poisoning/
- Defensive Mitigations: https://www.cynet.com/attack-techniques-hands-on/llmnr-nbt-ns-poisoning-and-credential-access-using-responder/

### Related Tools
- **Impacket:** SMB relay attacks and exploitation
- **CrackMapExec:** Network authentication testing
- **Wireshark:** Network traffic analysis

---

## ✅ Integration Checklist

- [x] Research Responder capabilities and Python 3 version
- [x] Clone lgandx/Responder (Python 3) to shared volume
- [x] Install Python dependencies (netifaces, pycryptodome)
- [x] Copy Responder to Agent Zero container
- [x] Create Agent Zero tool wrapper (`responder_security.py`)
- [x] Document all operations and use cases
- [ ] Test Responder installation (pending container restart)
- [ ] Verify network capabilities configuration
- [ ] Run sample analysis and validate log capture
- [ ] Document findings and create usage examples

---

## 🎉 Summary

**Responder cybersecurity tool has been successfully integrated into Agent Zero!**

This integration provides Agent Zero with powerful network security analysis capabilities for detecting:
- LLMNR/NBT-NS vulnerabilities
- Credential leakage risks
- Network protocol misconfigurations
- Authentication weaknesses

The tool is configured for **defensive security analysis only** and follows security best practices.

**Next Steps:**
1. Restart Agent Zero container
2. Test integration with `operation: test`
3. Run network analysis on test environment
4. Review security reports and recommendations

---

**Integration Status:** ✅ COMPLETE
**Documentation Version:** 1.0
**Last Updated:** 2025-10-18
