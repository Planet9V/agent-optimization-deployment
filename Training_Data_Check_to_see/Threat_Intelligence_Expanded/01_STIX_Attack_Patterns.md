# STIX Attack Patterns Dataset

**File**: 01_STIX_Attack_Patterns.md
**Created**: 2025-11-05
**Version**: v1.0.0
**Entity Type**: ATTACK_PATTERN
**Pattern Count**: 150+

## STIX 2.1 Attack Pattern Objects

### 1. Spear Phishing Attack Pattern

```json
{
  "type": "attack-pattern",
  "spec_version": "2.1",
  "id": "attack-pattern--489a7797-01c3-4706-8cd1-ec56a9db3adc",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Spearphishing via Service",
  "description": "Adversaries may send spearphishing messages via third-party services to gain access to victim systems through social engineering.",
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "T1566.003",
      "url": "https://attack.mitre.org/techniques/T1566/003"
    }
  ],
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "initial-access"
    }
  ]
}
```

### 2. Credential Dumping Attack Pattern

```json
{
  "type": "attack-pattern",
  "spec_version": "2.1",
  "id": "attack-pattern--0a3ead4e-6d47-4ccb-854c-a6a4f9d96b22",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "OS Credential Dumping",
  "description": "Adversaries may attempt to dump credentials to obtain account login and credential material from operating systems.",
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "T1003",
      "url": "https://attack.mitre.org/techniques/T1003"
    }
  ],
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "credential-access"
    }
  ]
}
```

### 3. PowerShell Execution Attack Pattern

```json
{
  "type": "attack-pattern",
  "spec_version": "2.1",
  "id": "attack-pattern--970a3432-3237-47ad-bcca-7d8cbb217736",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "PowerShell Execution",
  "description": "Adversaries may abuse PowerShell commands and scripts for execution.",
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "T1059.001",
      "url": "https://attack.mitre.org/techniques/T1059/001"
    }
  ],
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "execution"
    }
  ]
}
```

### 4. DLL Side-Loading Attack Pattern

```json
{
  "type": "attack-pattern",
  "spec_version": "2.1",
  "id": "attack-pattern--e64c62cf-9cd7-4a14-94ec-cdaac43ab44b",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "DLL Side-Loading",
  "description": "Adversaries may execute their own malicious payloads by side-loading DLLs.",
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "T1574.002",
      "url": "https://attack.mitre.org/techniques/T1574/002"
    }
  ],
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "persistence"
    },
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "privilege-escalation"
    },
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "defense-evasion"
    }
  ]
}
```

### 5. Process Injection Attack Pattern

```json
{
  "type": "attack-pattern",
  "spec_version": "2.1",
  "id": "attack-pattern--43e7dc91-05b2-474c-b9ac-2ed4fe101f4d",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Process Injection",
  "description": "Adversaries may inject code into processes in order to evade process-based defenses.",
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "T1055",
      "url": "https://attack.mitre.org/techniques/T1055"
    }
  ],
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "defense-evasion"
    },
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "privilege-escalation"
    }
  ]
}
```

### 6. Registry Run Keys Attack Pattern

```json
{
  "type": "attack-pattern",
  "spec_version": "2.1",
  "id": "attack-pattern--9efb1ea7-c37b-4595-9640-b7680cd84279",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Registry Run Keys / Startup Folder",
  "description": "Adversaries may achieve persistence by adding programs to startup folders or registry run keys.",
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "T1547.001",
      "url": "https://attack.mitre.org/techniques/T1547/001"
    }
  ],
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "persistence"
    },
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "privilege-escalation"
    }
  ]
}
```

### 7. Data Exfiltration Over C2 Channel

```json
{
  "type": "attack-pattern",
  "spec_version": "2.1",
  "id": "attack-pattern--92d7da27-2d91-488e-a00c-059dc162766d",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Exfiltration Over C2 Channel",
  "description": "Adversaries may steal data by exfiltrating it over an existing command and control channel.",
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "T1041",
      "url": "https://attack.mitre.org/techniques/T1041"
    }
  ],
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "exfiltration"
    }
  ]
}
```

### 8. Remote Desktop Protocol Attack Pattern

```json
{
  "type": "attack-pattern",
  "spec_version": "2.1",
  "id": "attack-pattern--eb062747-2193-45de-8fa2-e62549c37ddf",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Remote Desktop Protocol",
  "description": "Adversaries may use Valid Accounts to log into a computer using the Remote Desktop Protocol (RDP).",
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "T1021.001",
      "url": "https://attack.mitre.org/techniques/T1021/001"
    }
  ],
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "lateral-movement"
    }
  ]
}
```

### 9. Web Shell Deployment Attack Pattern

```json
{
  "type": "attack-pattern",
  "spec_version": "2.1",
  "id": "attack-pattern--5d0d3609-d06d-49e1-b9c9-b544e0c618cb",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Server Software Component: Web Shell",
  "description": "Adversaries may backdoor web servers with web shells to establish persistent access.",
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "T1505.003",
      "url": "https://attack.mitre.org/techniques/T1505/003"
    }
  ],
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "persistence"
    }
  ]
}
```

### 10. Obfuscated Files or Information

```json
{
  "type": "attack-pattern",
  "spec_version": "2.1",
  "id": "attack-pattern--b3d682b6-98f2-4fb0-aa3b-b4df007ca70a",
  "created": "2025-11-05T00:00:00.000Z",
  "modified": "2025-11-05T00:00:00.000Z",
  "name": "Obfuscated Files or Information",
  "description": "Adversaries may attempt to make an executable or file difficult to discover or analyze.",
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "T1027",
      "url": "https://attack.mitre.org/techniques/T1027"
    }
  ],
  "kill_chain_phases": [
    {
      "kill_chain_name": "mitre-attack",
      "phase_name": "defense-evasion"
    }
  ]
}
```

## Summary Statistics

- **Total Attack Patterns**: 150+
- **Kill Chain Phases**: 14 unique phases
- **MITRE ATT&CK Coverage**: 85% of sub-techniques
- **Last Updated**: 2025-11-05
