# Responder Quick Reference Card

## 🚀 Quick Start

### Test Installation
```json
{"tool_name": "responder_security", "tool_args": {"operation": "test"}}
```

### Get Help
```json
{"tool_name": "responder_security", "tool_args": {"operation": "help"}}
```

---

## 📋 All Operations

| Operation | Purpose | Example |
|-----------|---------|---------|
| `test` | Verify installation | `{"operation": "test"}` |
| `help` | Show all commands | `{"operation": "help"}` |
| `analyze` | Passive network scan | `{"operation": "analyze", "interface": "eth0", "duration": 60}` |
| `parse_logs` | View captured logs | `{"operation": "parse_logs"}` |
| `list_captures` | Show captured hashes | `{"operation": "list_captures"}` |
| `security_report` | Generate assessment | `{"operation": "security_report"}` |

---

## 🔍 Common Use Cases

### 1. Network Security Scan
```
Agent Task: "Scan the network for LLMNR vulnerabilities"
→ Runs analyze operation for 60 seconds
→ Parses logs for findings
→ Generates security report
```

### 2. Credential Leak Detection
```
Agent Task: "Check if any credentials are leaking over the network"
→ Passive monitoring
→ List captures
→ Report findings
```

### 3. Compliance Check
```
Agent Task: "Verify LLMNR and NBT-NS are disabled"
→ Network analysis
→ Parse logs
→ Validate compliance
```

---

## 💻 Manual Commands

### Inside Container
```bash
# Test Responder
docker exec -u root agentzero python3 /app/tools/responder/Responder.py --help

# Run analysis (60 seconds)
docker exec -u root agentzero python3 /app/tools/responder/Responder.py -I eth0 -A -d -w -t 60

# View logs
docker exec agentzero ls /app/tools/responder/logs/
docker exec agentzero cat /app/tools/responder/logs/Analyzer-Session.log
```

---

## ⚙️ Configuration

### Responder Flags
- `-I eth0`: Network interface
- `-A`: Analyze mode (passive)
- `-d`: DHCP poisoning
- `-w`: WPAD server
- `-v`: Verbose
- `-t 60`: Timeout (seconds)

### Log Locations
- `/app/tools/responder/logs/Analyzer-Session.log`
- `/app/tools/responder/logs/*NTLM*.txt`
- `/app/tools/responder/logs/*HTTP*.txt`

---

## 🛡️ Security Reminders

✅ **Use For:**
- Network security assessments
- Vulnerability detection
- Compliance validation
- Educational purposes

❌ **Don't Use For:**
- Unauthorized access
- Credential theft
- Network attacks
- Malicious purposes

---

## 🔧 Troubleshooting

### Python Syntax Errors
→ Ensure Python 3 version (lgandx/Responder)

### Permission Denied
→ Run with root: `docker exec -u root`

### No Network Interface
→ Check available: `docker exec agentzero ip link show`

### Responder Not Found
→ Copy to container: `docker cp responder-tool/. agentzero:/app/tools/responder/`

---

## 📞 Support

**Documentation:** `/Users/jim/Documents/5_AgentZero/container_agentzero/claudedocs/RESPONDER_INTEGRATION_COMPLETE.md`

**GitHub:** https://github.com/lgandx/Responder

**Kali Tools:** https://www.kali.org/tools/responder/
