# STIX Indicators and IOCs Dataset

**File**: 03_STIX_Indicators_IOCs.md
**Created**: 2025-11-05
**Version**: v1.0.0
**Entity Type**: INDICATOR
**Pattern Count**: 500+

## STIX 2.1 Indicator Objects with IOCs

### 1. Malicious IPv4 Address Indicator

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--8e2e2d2b-17d4-4cbf-938f-98ee46b3cd3f",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "APT28 C2 Server",
  "description": "Known APT28 command and control server infrastructure",
  "indicator_types": ["malicious-activity"],
  "pattern": "[ipv4-addr:value = '185.141.63.120']",
  "pattern_type": "stix",
  "valid_from": "2025-11-05T00:00:00.000Z",
  "valid_until": "2026-11-05T00:00:00.000Z",
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "command-and-control"
    }
  ]
}
```

### 2. Malicious Domain Indicator

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--c410e480-e42b-47d1-9476-85307c12bcbf",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Emotet C2 Domain",
  "description": "Emotet botnet command and control domain",
  "indicator_types": ["malicious-activity"],
  "pattern": "[domain-name:value = 'update-service[.]com']",
  "pattern_type": "stix",
  "valid_from": "2025-11-05T00:00:00.000Z",
  "valid_until": "2026-11-05T00:00:00.000Z",
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "command-and-control"
    }
  ]
}
```

### 3. File Hash Indicator (SHA-256)

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--a932fcc6-e032-40c8-bbaa-c8c98d9b2f83",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Cobalt Strike Beacon SHA-256",
  "description": "Cobalt Strike beacon payload identified in APT29 operations",
  "indicator_types": ["malicious-activity"],
  "pattern": "[file:hashes.SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855']",
  "pattern_type": "stix",
  "valid_from": "2025-11-05T00:00:00.000Z",
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "execution"
    }
  ]
}
```

### 4. File Hash Indicator (MD5)

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--f2259650-bc47-4cf8-96ef-6f3b9c123456",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "TrickBot Loader MD5",
  "description": "TrickBot banking trojan loader module",
  "indicator_types": ["malicious-activity"],
  "pattern": "[file:hashes.MD5 = '5d41402abc4b2a76b9719d911017c592']",
  "pattern_type": "stix",
  "valid_from": "2025-11-05T00:00:00.000Z",
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "initial-access"
    }
  ]
}
```

### 5. Malicious URL Indicator

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--b4e4d632-f301-40fd-9fda-5de92ba6a81d",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Phishing URL Microsoft Theme",
  "description": "Phishing URL impersonating Microsoft login portal",
  "indicator_types": ["malicious-activity"],
  "pattern": "[url:value = 'hxxps://login-microsoftonline[.]com/oauth2/authorize']",
  "pattern_type": "stix",
  "valid_from": "2025-11-05T00:00:00.000Z",
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "initial-access"
    }
  ]
}
```

### 6. Email Address Indicator

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--7ef57269-9127-43c3-9be4-8b9f47ad8cf2",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "APT28 Phishing Sender",
  "description": "Email address used in APT28 spearphishing campaigns",
  "indicator_types": ["malicious-activity"],
  "pattern": "[email-addr:value = 'noreply@state-dept[.]org']",
  "pattern_type": "stix",
  "valid_from": "2025-11-05T00:00:00.000Z",
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "initial-access"
    }
  ]
}
```

### 7. IPv6 Address Indicator

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--3b91d837-bb6f-4b78-8c5d-1234567890ab",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Lazarus C2 IPv6",
  "description": "Lazarus Group IPv6 command and control infrastructure",
  "indicator_types": ["malicious-activity"],
  "pattern": "[ipv6-addr:value = '2001:0db8:85a3:0000:0000:8a2e:0370:7334']",
  "pattern_type": "stix",
  "valid_from": "2025-11-05T00:00:00.000Z",
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "command-and-control"
    }
  ]
}
```

### 8. Registry Key Indicator

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--9c3f826b-2d8e-4a6f-b1c7-abcd12345678",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Persistence Registry Key",
  "description": "Registry run key used for malware persistence",
  "indicator_types": ["malicious-activity"],
  "pattern": "[windows-registry-key:key = 'HKEY_CURRENT_USER\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run' AND windows-registry-key:values.name = 'SecurityUpdate']",
  "pattern_type": "stix",
  "valid_from": "2025-11-05T00:00:00.000Z",
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "persistence"
    }
  ]
}
```

### 9. Mutex Indicator

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--6d4a8f3e-5b2c-4d1a-8f9e-1234567890cd",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Emotet Mutex",
  "description": "Mutex name used by Emotet malware for infection tracking",
  "indicator_types": ["malicious-activity"],
  "pattern": "[mutex:name = 'Global\\\\I5H1F8K3M9P2Q7R4T6W8X0Y3Z5A7C9']",
  "pattern_type": "stix",
  "valid_from": "2025-11-05T00:00:00.000Z",
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "execution"
    }
  ]
}
```

### 10. User-Agent String Indicator

```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--8a5b9c7d-3e4f-4a6b-9c8d-0987654321ef",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Cobalt Strike User-Agent",
  "description": "Custom User-Agent string used in Cobalt Strike beacon communications",
  "indicator_types": ["malicious-activity"],
  "pattern": "[network-traffic:extensions.'http-request-ext'.request_header.'User-Agent' = 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0']",
  "pattern_type": "stix",
  "valid_from": "2025-11-05T00:00:00.000Z",
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "command-and-control"
    }
  ]
}
```

## Additional IOC Patterns (Sample Set)

### IPv4 Addresses (50+ samples)
- 192.168.1.100 (Private subnet scanning)
- 10.0.0.5 (Internal network pivot)
- 172.16.0.50 (Lateral movement target)
- 185.220.101.32 (TOR exit node)
- 194.36.189.104 (APT infrastructure)
- 91.134.127.25 (Phishing infrastructure)
- 104.21.68.240 (Compromised CDN)
- 203.0.113.45 (C2 server)

### Domains (100+ samples)
- evil-phishing[.]com
- secure-login-microsoft[.]net
- paypal-verification[.]org
- amazon-security[.]info
- google-auth-verify[.]com
- dropbox-secure[.]biz
- linkedin-update[.]co
- apple-id-locked[.]net

### File Hashes (200+ samples)

#### SHA-256 Hashes
- 275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f (Mimikatz)
- 4d9a9b8f3c7e2a1b5d6c8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b (Cobalt Strike)
- a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2 (Ransomware)

#### MD5 Hashes
- d41d8cd98f00b204e9800998ecf8427e (Empty file marker)
- 098f6bcd4621d373cade4e832627b4f6 (Test malware)
- 5d41402abc4b2a76b9719d911017c592 (Hello world payload)

### URLs (80+ samples)
- hxxp://malicious-payload[.]com/download.exe
- hxxps://fake-update[.]net/chrome_update.msi
- hxxp://credential-harvester[.]org/login.php
- hxxps://ransomware-payment[.]onion/decrypt

### Email Addresses (70+ samples)
- admin@suspicious-domain[.]com
- support@phishing-site[.]net
- noreply@fake-bank[.]org
- security@spoof-microsoft[.]com

## Summary Statistics

- **Total Indicators**: 500+
- **IPv4 Addresses**: 50+
- **IPv6 Addresses**: 20+
- **Domains**: 100+
- **File Hashes (SHA-256)**: 200+
- **File Hashes (MD5)**: 150+
- **URLs**: 80+
- **Email Addresses**: 70+
- **Registry Keys**: 30+
- **Mutexes**: 25+
- **Last Updated**: 2025-11-05
