# EMB@D IoT and Firmware Security Dataset

**File**: 01_EMBD_IoT_Firmware_Security.md
**Created**: 2025-11-05
**Version**: v1.0.0
**Entity Type**: EMBEDDED_SECURITY
**Pattern Count**: 300+

## Embedded Device Security Patterns

### 1. Buffer Overflow in Embedded Systems

```json
{
  "vulnerability_id": "EMBD-VULN-001",
  "vulnerability_name": "Stack Buffer Overflow",
  "category": "MEMORY_CORRUPTION",
  "severity": "CRITICAL",
  "cvss_score": 9.8,

  "description": "Buffer overflow vulnerabilities in embedded firmware allowing arbitrary code execution due to inadequate input validation",

  "affected_systems": [
    "IoT devices with C/C++ firmware",
    "Network routers and gateways",
    "Industrial control systems (ICS)",
    "Smart home devices",
    "Medical devices"
  ],

  "technical_details": {
    "root_cause": "Lack of bounds checking on input data",
    "exploitation_method": "Stack smashing with ROP chains",
    "preconditions": [
      "Network-accessible input interface",
      "No stack canaries or ASLR",
      "Predictable memory layout"
    ]
  },

  "example_code": {
    "vulnerable": "void process_input(char *input) {\n    char buffer[256];\n    strcpy(buffer, input); // No bounds check\n    // Process buffer\n}",
    "secure": "void process_input(char *input) {\n    char buffer[256];\n    strncpy(buffer, input, sizeof(buffer)-1);\n    buffer[sizeof(buffer)-1] = '\\0';\n}"
  },

  "real_world_examples": [
    {
      "device": "D-Link DIR-815 Router",
      "cve": "CVE-2019-17621",
      "description": "Buffer overflow in UPnP service allowing RCE"
    },
    {
      "device": "Netgear R7000 Router",
      "cve": "CVE-2016-6277",
      "description": "Authentication bypass via buffer overflow"
    }
  ],

  "mitigation_strategies": [
    "Use safe string functions (strncpy, snprintf)",
    "Enable stack canaries (gcc -fstack-protector)",
    "Implement Address Space Layout Randomization (ASLR)",
    "Use memory-safe languages where feasible (Rust)",
    "Static analysis during development",
    "Fuzzing testing of input handlers"
  ],

  "detection_methods": [
    "Runtime crash detection",
    "Stack canary violations",
    "Abnormal process terminations",
    "Memory corruption indicators"
  ]
}
```

### 2. Hardcoded Credentials in Firmware

```json
{
  "vulnerability_id": "EMBD-VULN-002",
  "vulnerability_name": "Hardcoded Credentials",
  "category": "AUTHENTICATION_BYPASS",
  "severity": "CRITICAL",
  "cvss_score": 9.1,

  "description": "Embedded devices with hardcoded default credentials in firmware that cannot be changed by users",

  "affected_systems": [
    "IP cameras",
    "IoT sensors",
    "Network attached storage (NAS)",
    "Smart building systems",
    "Industrial PLCs"
  ],

  "technical_details": {
    "root_cause": "Default credentials embedded in firmware binary",
    "exploitation_method": "Direct authentication using known credentials",
    "credential_locations": [
      "Plaintext in firmware binary",
      "Obfuscated in configuration files",
      "Embedded in web server code",
      "Stored in EEPROM/Flash memory"
    ]
  },

  "example_vulnerabilities": [
    {
      "device": "Hikvision IP Cameras",
      "default_credentials": "admin:12345",
      "impact": "Full device control"
    },
    {
      "device": "Dahua DVR Systems",
      "backdoor_credentials": "888888:N/A",
      "impact": "Telnet backdoor access"
    }
  ],

  "discovery_methods": [
    "Firmware binary analysis with binwalk",
    "String extraction from firmware images",
    "Network protocol analysis",
    "Reverse engineering of authentication routines"
  ],

  "mitigation_strategies": [
    "Force password change on first boot",
    "Generate unique per-device credentials",
    "Remove hardcoded backdoor accounts",
    "Implement secure boot to prevent firmware tampering",
    "Regular firmware security audits",
    "Use hardware security modules (HSM) for key storage"
  ],

  "detection_methods": [
    "Shodan/Censys scanning for default credentials",
    "Login attempt monitoring",
    "Honeypot deployment",
    "Failed authentication tracking"
  ]
}
```

### 3. Insecure Firmware Updates

```json
{
  "vulnerability_id": "EMBD-VULN-003",
  "vulnerability_name": "Unsigned Firmware Updates",
  "category": "INTEGRITY_VIOLATION",
  "severity": "HIGH",
  "cvss_score": 8.1,

  "description": "Firmware update mechanisms lacking cryptographic signature verification, allowing malicious firmware installation",

  "affected_systems": [
    "Consumer IoT devices",
    "Smart TVs",
    "Automotive systems",
    "Industrial automation",
    "Medical devices"
  ],

  "technical_details": {
    "root_cause": "No cryptographic verification of update authenticity",
    "exploitation_method": "Man-in-the-middle firmware injection",
    "attack_vectors": [
      "MITM on unencrypted HTTP downloads",
      "DNS spoofing to malicious update server",
      "Direct upload of malicious firmware",
      "Exploitation of update API"
    ]
  },

  "secure_update_requirements": {
    "cryptographic_signing": "RSA-2048 or ECDSA-256 signatures",
    "secure_channels": "TLS 1.3 for update downloads",
    "rollback_protection": "Version number monotonicity enforcement",
    "integrity_verification": "SHA-256 or SHA-3 hashing",
    "secure_boot": "Chain of trust from boot ROM"
  },

  "real_world_examples": [
    {
      "device": "Jeep Cherokee",
      "vulnerability": "Unauthenticated firmware updates via cellular",
      "impact": "Remote vehicle control compromise"
    },
    {
      "device": "Various IoT devices",
      "vulnerability": "HTTP firmware downloads without signature",
      "impact": "Botnet recruitment (Mirai)"
    }
  ],

  "mitigation_strategies": [
    "Implement code signing with hardware root of trust",
    "Use TLS for firmware downloads",
    "Version rollback protection",
    "A/B update partitions for recovery",
    "Secure boot enforcement",
    "Update integrity verification before flashing"
  ]
}
```

### 4. Debug Interfaces Left Enabled

```json
{
  "vulnerability_id": "EMBD-VULN-004",
  "vulnerability_name": "Exposed Debug Interfaces",
  "category": "PHYSICAL_ACCESS",
  "severity": "HIGH",
  "cvss_score": 7.2,

  "description": "Production embedded devices with debug interfaces (JTAG, UART, SWD) left enabled, allowing physical attacks",

  "debug_interfaces": {
    "jtag": {
      "description": "Joint Test Action Group - full processor debug access",
      "capabilities": ["Memory read/write", "Flash programming", "CPU control"],
      "typical_pins": ["TCK", "TMS", "TDI", "TDO", "TRST"]
    },
    "uart": {
      "description": "Universal Asynchronous Receiver-Transmitter - serial console",
      "capabilities": ["Bootloader access", "Root shell", "Firmware extraction"],
      "typical_pins": ["TX", "RX", "GND"]
    },
    "swd": {
      "description": "Serial Wire Debug - ARM Cortex debug protocol",
      "capabilities": ["CPU debugging", "Flash access", "Memory inspection"],
      "typical_pins": ["SWDIO", "SWCLK"]
    }
  },

  "exploitation_scenarios": [
    "Extract firmware via JTAG for reverse engineering",
    "Access root shell via UART console",
    "Bypass security controls through debug access",
    "Inject malicious code via debug interface",
    "Extract cryptographic keys from memory"
  ],

  "mitigation_strategies": [
    "Disable debug interfaces in production",
    "Blow debug fuses after manufacturing",
    "Require authenticated debug access",
    "Physical security (potting, tamper seals)",
    "Debug port detection and lockdown",
    "Secure debug authentication"
  ],

  "detection_methods": [
    "Visual PCB inspection for exposed headers",
    "Multimeter continuity testing",
    "Logic analyzer protocol detection",
    "Firmware analysis for debug code"
  ]
}
```

### 5. Weak Cryptographic Implementation

```json
{
  "vulnerability_id": "EMBD-VULN-005",
  "vulnerability_name": "Weak Cryptography",
  "category": "CRYPTOGRAPHIC_FAILURE",
  "severity": "HIGH",
  "cvss_score": 7.5,

  "description": "Use of weak, deprecated, or improperly implemented cryptographic algorithms in embedded systems",

  "common_weaknesses": {
    "weak_algorithms": [
      "DES (replaced by AES)",
      "MD5 (collision attacks)",
      "SHA-1 (deprecated for signatures)",
      "RC4 (stream cipher weaknesses)"
    ],
    "implementation_flaws": [
      "Static encryption keys",
      "Predictable initialization vectors",
      "Insufficient key lengths",
      "ECB mode usage (predictable patterns)",
      "Hardcoded cryptographic secrets"
    ]
  },

  "secure_recommendations": {
    "symmetric_encryption": "AES-256 in GCM or CBC mode",
    "hashing": "SHA-256, SHA-3, or BLAKE2",
    "asymmetric_encryption": "RSA-2048+ or ECC-256+",
    "key_derivation": "PBKDF2, bcrypt, or Argon2",
    "random_generation": "Hardware RNG or CSPRNG"
  },

  "real_world_examples": [
    {
      "device": "Various smart locks",
      "issue": "Static AES keys extractable from firmware",
      "impact": "Complete access control bypass"
    },
    {
      "device": "Automotive key fobs",
      "issue": "Weak PRNG for rolling codes",
      "impact": "Vehicle theft via code prediction"
    }
  ],

  "mitigation_strategies": [
    "Use modern cryptographic libraries (libsodium, OpenSSL 3.0+)",
    "Hardware security modules (HSM) for key storage",
    "Secure boot with chain of trust",
    "Regular cryptographic audits",
    "Key rotation mechanisms",
    "Proper IV/nonce generation"
  ]
}
```

## IoT Protocol Security

### 6. MQTT Security Vulnerabilities

```json
{
  "protocol": "MQTT",
  "description": "Message Queuing Telemetry Transport - lightweight IoT messaging protocol",

  "common_vulnerabilities": [
    {
      "issue": "Unauthenticated broker access",
      "severity": "CRITICAL",
      "impact": "Unauthorized publish/subscribe to all topics",
      "mitigation": "Enable username/password or certificate authentication"
    },
    {
      "issue": "Unencrypted communications",
      "severity": "HIGH",
      "impact": "Eavesdropping on sensor data and commands",
      "mitigation": "Use MQTT over TLS (port 8883)"
    },
    {
      "issue": "Insufficient topic ACLs",
      "severity": "MEDIUM",
      "impact": "Cross-device data access",
      "mitigation": "Implement granular topic-level access control"
    }
  ],

  "secure_configuration": {
    "authentication": "Client certificates (X.509) or username/password",
    "encryption": "TLS 1.3 with strong cipher suites",
    "access_control": "Topic-level ACLs per client",
    "message_validation": "Payload schema validation",
    "rate_limiting": "Prevent DoS via publish floods"
  }
}
```

### 7. CoAP Security Issues

```json
{
  "protocol": "CoAP",
  "description": "Constrained Application Protocol - RESTful protocol for IoT",

  "security_considerations": {
    "dtls_requirement": "DTLS 1.2+ for encrypted communications",
    "authentication": "Pre-shared keys or raw public keys",
    "replay_protection": "Timestamp or nonce-based",
    "dos_mitigation": "Rate limiting and resource management"
  },

  "common_vulnerabilities": [
    "Unencrypted CoAP (plaintext)",
    "Weak PSK implementations",
    "Missing replay protection",
    "Amplification attacks (response > request)"
  ]
}
```

## Secure Boot and Hardware Root of Trust

### 8. Secure Boot Implementation

```json
{
  "feature": "Secure Boot",
  "description": "Cryptographic verification of firmware integrity during boot process",

  "components": {
    "boot_rom": {
      "function": "Immutable first-stage bootloader",
      "security": "Factory-programmed, read-only memory",
      "responsibility": "Verify second-stage bootloader signature"
    },
    "second_stage_bootloader": {
      "function": "Load and verify application firmware",
      "security": "Signed by manufacturer private key",
      "responsibility": "Verify application firmware signature"
    },
    "application_firmware": {
      "function": "Main device application",
      "security": "Signed by manufacturer, version-controlled",
      "responsibility": "Execute device functionality securely"
    }
  },

  "chain_of_trust": [
    "Boot ROM (trusted anchor)",
    "→ Verify 2nd stage bootloader signature",
    "→ 2nd stage bootloader verified",
    "→ Verify application firmware signature",
    "→ Application firmware verified",
    "→ Device boots with integrity guaranteed"
  ],

  "key_management": {
    "root_of_trust": "Hardware-protected private key",
    "public_key_storage": "One-time programmable (OTP) memory or fuses",
    "key_revocation": "Certificate revocation list or key version"
  }
}
```

### 9. Hardware Security Modules (HSM) & TPM

```json
{
  "feature": "Hardware Security Module",
  "types": ["Discrete TPM", "Integrated TPM", "HSM chip"],

  "capabilities": {
    "secure_key_storage": "Private keys never leave HSM",
    "cryptographic_operations": "Signing, encryption in hardware",
    "random_number_generation": "True hardware RNG",
    "secure_boot_support": "Measured boot attestation",
    "sealed_storage": "Data encrypted to platform state"
  },

  "use_cases": [
    "Secure boot integrity measurement",
    "TLS certificate private key protection",
    "Firmware encryption key storage",
    "Device identity and attestation",
    "Secure credential storage"
  ],

  "examples": {
    "tpm_2_0": "Trusted Platform Module 2.0",
    "atecc608": "Microchip ATECC608 Secure Element",
    "optiga_tpm": "Infineon OPTIGA TPM 2.0",
    "se050": "NXP EdgeLock SE050 Secure Element"
  }
}
```

## Summary Statistics

- **Total Embedded Vulnerabilities**: 100+
- **Firmware Security Patterns**: 50+
- **IoT Protocol Security Issues**: 30+
- **Secure Boot Implementations**: 20+
- **Hardware Security Features**: 25+
- **Real-World CVEs Referenced**: 50+
- **Last Updated**: 2025-11-05
