# Encryption and Key Management - Emergency Services P25 Systems

## Encryption Standards and Algorithms

### AES-256 Encryption (Advanced Encryption Standard)
- **Standard**: FIPS 197 (Federal Information Processing Standard Publication 197)
- **Approval Date**: November 26, 2001 by NIST (National Institute of Standards and Technology)
- **Algorithm**: Rijndael cipher selected from AES competition
- **Key Length**: 256-bit encryption key (32 bytes)
- **Block Size**: 128-bit data blocks (16 bytes)
- **Cipher Rounds**: 14 encryption/decryption rounds for 256-bit keys
- **Key Schedule**: Key expansion from 256-bit key to 15 round keys (240 bytes total)
- **S-Box**: Substitution box for non-linear transformation (16x16 lookup table)
- **Mix Columns**: Column mixing operation in Galois Field GF(2^8)
- **Shift Rows**: Byte transposition for diffusion
- **Add Round Key**: XOR operation with round key
- **Mode of Operation**: OFB (Output Feedback) mode for P25 voice encryption
- **IV (Initialization Vector)**: 128-bit IV transmitted with each call
- **IV Generation**: Random or pseudo-random IV generation
- **IV Transmission**: IV sent in clear at call setup
- **Key Reuse**: Never reuse key-IV pair (cryptographic requirement)
- **Security Margin**: 256-bit AES provides 2^256 possible keys (practically unbreakable)
- **Attack Resistance**: Resistant to brute force, differential, linear cryptanalysis
- **Performance**: Hardware AES-NI instruction support in modern processors
- **Voice Latency**: <10ms encryption/decryption latency
- **Approved Use**: NSA Suite B cryptography, approved for TOP SECRET (with proper key management)

### AES-256 in OFB Mode (Output Feedback)
- **Mode Type**: Stream cipher mode (converts block cipher to stream cipher)
- **Encryption**: Plaintext XOR with keystream (IV encrypted iteratively)
- **Synchronization**: Self-synchronizing after 128-bit error propagation
- **Error Propagation**: Bit errors do not propagate (single-bit error remains single-bit)
- **IV Requirement**: Unique IV for each call/message (never reuse IV with same key)
- **Padding**: No padding required (stream cipher encrypts any length)
- **Parallelization**: Cannot be parallelized (sequential encryption)
- **Advantages**: No error propagation, no padding, same encryption/decryption operation
- **Disadvantages**: Must never reuse IV with same key (security vulnerability)

### DES-OFB Encryption (Data Encryption Standard - Output Feedback)
- **Standard**: FIPS 46-3 (Federal Information Processing Standard, now withdrawn)
- **Approval**: Original DES approved in 1977, withdrawn in 2005
- **Algorithm**: Feistel cipher with 16 rounds
- **Key Length**: 56-bit effective key (64-bit with 8 parity bits)
- **Block Size**: 64-bit data blocks
- **Mode**: OFB (Output Feedback) mode
- **IV**: 64-bit initialization vector
- **Security Level**: Considered cryptographically weak by modern standards
- **Attack**: Vulnerable to brute-force attack (2^56 = 72 quadrillion keys)
- **Crack Time**: Can be cracked in hours with modern computing power
- **Legacy Use**: Maintained in P25 for backward compatibility with older systems
- **Recommendation**: Migrate to AES-256 for all new deployments
- **Retirement**: DES officially withdrawn by NIST in 2005
- **Replacement**: Triple DES (3DES) or AES recommended

### DES-XL Encryption (DVI-XL - Digital Voice Inversion XL)
- **Type**: Proprietary voice encryption (not true DES)
- **Vendor**: Originally Motorola/Harris proprietary
- **Security**: Rolling code inversion, not cryptographically secure
- **Use Case**: Privacy from casual listeners (not secure encryption)
- **Key Length**: Shorter key space than true DES
- **Status**: Legacy encryption, not recommended for sensitive communications
- **Migration**: Replace with AES-256 for secure communications

## Encryption Key Types and Hierarchy

### KEK (Key Encryption Key)
- **Purpose**: Master key used to encrypt TEKs for over-the-air distribution
- **Key Length**: 256-bit for AES-KEK
- **Distribution**: Manual distribution via key fill device (KFD) or secure courier
- **Storage**: Stored in secure key storage in radio (tamper-resistant)
- **Lifetime**: Long-term key (months to years)
- **Change Frequency**: Changed annually or when compromised
- **Access Control**: Restricted to authorized crypto custodians
- **Backup**: Secure backup of KEKs required
- **Destruction**: Secure destruction when superseded or compromised

### TEK (Traffic Encryption Key)
- **Purpose**: Short-term encryption key for voice/data traffic
- **Key Length**: 256-bit for AES-TEK, 56-bit for DES-TEK
- **Distribution**: Distributed over-the-air (OTAR) encrypted with KEK
- **Lifetime**: Short-term key (hours to weeks)
- **Change Frequency**: Changed daily, weekly, or monthly depending on policy
- **Automatic Rekeying**: Scheduled automatic rekeying via OTAR
- **Talk Group Association**: TEKs associated with specific talk groups
- **SLN (Storage Location Number)**: TEK stored in numbered key slots (0-255)
- **Active TEK**: Currently active TEK for encryption/decryption
- **Standby TEK**: Next TEK staged for automatic activation

### Common KEK (CKEK)
- **Purpose**: System-wide KEK for distributing TEKs to all radios
- **Scope**: Used across entire radio system
- **Distribution**: Manual key fill to all subscriber units
- **Use Case**: Simplified key management for systems with single key hierarchy
- **Security Risk**: Compromise of CKEK affects all radios in system

### Individual KEK (IKEK)
- **Purpose**: Individual KEK unique to each radio
- **Scope**: One unique KEK per subscriber unit
- **Distribution**: Manual key fill specific to each radio
- **Use Case**: High-security systems requiring individual key management
- **Advantage**: Compromise of one IKEK does not affect other radios
- **Complexity**: Higher administrative burden for key management

### Group KEK (GKEK)
- **Purpose**: KEK shared by group of radios (e.g., by agency or department)
- **Scope**: Group of subscriber units (e.g., police department, fire department)
- **Distribution**: Manual key fill to group members
- **Use Case**: Multi-agency systems with independent key management
- **Flexibility**: Allows different rekeying schedules per agency

## OTAR (Over-The-Air Rekeying)

### TIA-102.AAAD OTAR Protocol
- **Standard**: TIA-102.AAAD (OTAR Protocol Standard)
- **Purpose**: Secure distribution of encryption keys over radio network
- **Encryption**: TEKs encrypted with KEK for transmission
- **Message Types**: TEK transfer, TEK activation, TEK deletion, status query
- **Addressing**: Unicast (individual radio), multicast (group), broadcast (all radios)
- **Acknowledgment**: Radio sends acknowledgment upon successful TEK receipt
- **Retry**: Automatic retry for failed TEK delivery
- **Audit Trail**: Logging of all OTAR transactions
- **Security**: Encrypted OTAR messages, authenticated sender

### OTAR Message Components
- **Message Indicator (MI)**: 16-bit identifier for TEK being distributed
- **SLN (Storage Location Number)**: Key storage slot number (0-255)
- **Algorithm ID**: Identifies encryption algorithm (AES-256, DES-OFB)
- **Key ID (KID)**: Unique identifier for the key
- **Key Data**: Encrypted TEK (encrypted with KEK)
- **Activation Time**: Scheduled time for automatic TEK activation
- **Expiration Time**: Key expiration date/time
- **CRC**: Cyclic Redundancy Check for message integrity

### OTAR Distribution Methods

#### Unicast OTAR
- **Target**: Single radio (individual addressing)
- **Use Case**: Replace compromised key in specific radio
- **Bandwidth**: Minimal bandwidth usage
- **Time**: Fast distribution to single unit

#### Multicast OTAR
- **Target**: Group of radios (talk group addressing)
- **Use Case**: Rekey specific department or agency
- **Bandwidth**: Efficient for groups (single transmission to multiple radios)
- **Time**: Faster than multiple unicast operations

#### Broadcast OTAR
- **Target**: All radios on system
- **Use Case**: System-wide rekeying
- **Bandwidth**: Efficient for large-scale rekeying
- **Time**: Simultaneous rekeying of all units
- **Limitation**: No acknowledgment from individual radios

### OTAR Timing and Scheduling
- **Staged Distribution**: Distribute TEKs days/weeks before activation
- **Activation Time**: Scheduled activation time (e.g., 00:00 on first of month)
- **Time Synchronization**: GPS time synchronization for coordinated activation
- **Overlap Period**: Old and new TEKs both valid during transition period
- **Grace Period**: 24-48 hour grace period for radios that missed OTAR message

### OTAR Failure Handling
- **Acknowledgment Timeout**: 30-60 second timeout for ACK receipt
- **Retry Mechanism**: Automatic retry up to 3 times
- **Fallback**: Manual key fill for radios that fail OTAR
- **Notification**: Alert crypto custodian of OTAR failures
- **Status Query**: Query radio to verify TEK receipt and activation

## Key Fill Devices (KFD)

### Motorola KVL 4000 Key Variable Loader
- **Product**: KVL 4000 OTAR Manager
- **Vendor**: Motorola Solutions
- **Type**: Portable key fill device with OTAR management
- **Key Capacity**: 500+ keys in internal memory
- **Key Types**: AES-256 KEK/TEK, DES-OFB keys
- **Interface**: USB 2.0 for PC connection, keypad for local operation
- **Display**: Backlit LCD display for status and menus
- **Battery**: Rechargeable Li-Ion battery (8 hour runtime)
- **Charging**: USB charging or AC adapter
- **Encryption**: Encrypted key storage with AES-256
- **Authentication**: PIN-based authentication (4-8 digit PIN)
- **Zeroization**: Automatic key deletion on tamper or excessive PIN failures
- **Tamper Detection**: Tamper-evident seals and intrusion detection
- **Key Fill Methods**: Direct key fill to radio via cable, OTAR message creation
- **Cable**: Key fill cable with proprietary connector to radio
- **Software**: PC software for key management and OTAR scheduling
- **Audit Log**: Complete audit log of key operations
- **Operating Temp**: -20°C to +60°C
- **Dimensions**: 180mm x 80mm x 30mm
- **Weight**: 300 grams
- **Compliance**: FIPS 140-2 Level 2 certified
- **Security**: Secure boot, firmware integrity checking

### Motorola KVL 5000 Advanced Key Loader
- **Product**: KVL 5000 Key Variable Loader
- **Enhanced Features**: Touchscreen interface, increased capacity
- **Key Capacity**: 1000+ keys
- **Display**: Color touchscreen display
- **Network**: Wi-Fi and Ethernet for remote key management
- **Multi-Algorithm**: Support for AES-256, DES, ADP, DVP
- **Bluetooth**: Wireless key fill via Bluetooth (short range)
- **GPS**: Integrated GPS for location logging
- **FIPS Certification**: FIPS 140-2 Level 3

### Harris (L3Harris) KYK-13 Key Fill Device
- **Product**: KYK-13 Electronic Transfer Device
- **Vendor**: L3Harris Technologies
- **Type**: Portable key fill device
- **Key Capacity**: 250 keys
- **Key Types**: AES-256, DES-OFB, DVI-XL
- **Interface**: USB 2.0, serial interface
- **Display**: LCD display with keypad
- **Battery**: Rechargeable battery
- **Encryption**: Encrypted key storage
- **Authentication**: PIN authentication
- **Zeroization**: Automatic zeroization on tamper
- **Key Fill**: Cable-based key fill to radios
- **Dimensions**: Compact handheld form factor
- **Compliance**: NSA-approved for classified key material

### Cisco (Scientific Atlanta) CKR Motorola Key Fill
- **Product**: CKR (Cisco Key Reader)
- **Type**: Legacy key fill device (older generation)
- **Key Types**: DES-OFB, DVI
- **Interface**: Serial port interface
- **Status**: Legacy device, replaced by KVL series
- **Compatibility**: Older Motorola radios

## Key Management Infrastructure (KMI)

### Motorola Over-The-Air Key Management (OAKM)
- **Product**: Motorola OAKM System
- **Architecture**: Centralized key management server
- **Database**: Centralized key database (Oracle or SQL Server)
- **Key Generation**: Cryptographically secure random key generation
- **Key Storage**: Encrypted key storage with HSM (Hardware Security Module)
- **OTAR Scheduling**: Automated OTAR scheduling and distribution
- **Audit Logging**: Comprehensive audit logs of all key operations
- **User Roles**: Crypto custodian, key administrator, auditor roles
- **Access Control**: Role-based access control (RBAC)
- **Backup**: Automated encrypted backups of key database
- **Disaster Recovery**: Geographic redundancy for key management servers
- **Integration**: Integration with P25 trunking system
- **Reporting**: Key distribution reports, compliance reports
- **Notifications**: Email/SMS notifications for key events
- **Web Interface**: Web-based management interface

### Key Management Policies

#### Key Lifecycle Management
- **Generation**: Cryptographically secure random key generation (FIPS 140-2 approved RNG)
- **Distribution**: Secure distribution via OTAR or manual key fill
- **Storage**: Encrypted storage in radio and KMI
- **Activation**: Scheduled activation at specified time
- **Usage**: Encryption/decryption during validity period
- **Rotation**: Periodic rekeying (daily, weekly, monthly)
- **Expiration**: Automatic expiration and deletion
- **Archival**: Secure archival of expired keys (for forensic decryption)
- **Destruction**: Secure deletion/zeroization of compromised keys

#### Key Change Frequency
- **TEK Rotation**: Daily, weekly, or monthly depending on security policy
- **KEK Rotation**: Annually or when compromised
- **Emergency Rekey**: Immediate rekeying upon suspected compromise
- **Scheduled Maintenance**: Planned rekeying during maintenance windows
- **Grace Period**: Overlap period where old and new keys both valid

#### Compromise Response
- **Detection**: Identify potential key compromise (radio theft, insider threat)
- **Notification**: Alert crypto custodian and security officer
- **Immediate Action**: Disable compromised radio via stun/kill command
- **Rekeying**: Emergency OTAR to replace compromised TEK system-wide
- **KEK Replacement**: Replace KEK if compromise severity warrants
- **Investigation**: Forensic investigation of compromise incident
- **Documentation**: Document incident and corrective actions

## Hardware Security Modules (HSM)

### Thales Luna HSM
- **Product**: Thales Luna Network HSM
- **Purpose**: Secure key generation and storage for KMI
- **Certification**: FIPS 140-2 Level 3 certified
- **Key Storage**: Tamper-resistant key storage
- **Key Generation**: Hardware-based true random number generator (TRNG)
- **Cryptographic Operations**: Hardware-accelerated AES, RSA, ECC operations
- **Throughput**: 10,000+ RSA operations per second
- **Network Interface**: Gigabit Ethernet connectivity
- **Redundancy**: Clustered HSM configuration for high availability
- **Backup**: Secure key backup to external storage
- **Tamper Response**: Automatic key zeroization on tamper detection
- **Authentication**: Multi-factor authentication for access
- **Audit Logging**: Tamper-proof audit logs

### IBM Crypto Express HSM
- **Product**: IBM Crypto Express PCIe HSM
- **Form Factor**: PCIe card for server installation
- **Certification**: FIPS 140-2 Level 4 (highest level)
- **Key Storage**: Secure key storage with physical tamper protection
- **Cryptographic Acceleration**: Hardware AES, DES, RSA, ECC
- **Tamper Detection**: Physical intrusion detection with automatic zeroization
- **Performance**: High-performance cryptographic operations

## Key Storage and Protection in Radios

### Secure Key Storage
- **Storage Type**: Flash memory or EEPROM (Electrically Erasable Programmable ROM)
- **Encryption**: Keys encrypted at rest with device-unique key
- **Key Slots**: 256 key storage locations (SLN 0-255)
- **Active Key**: Currently active TEK for encryption
- **Standby Key**: Next TEK staged for activation
- **Archival**: Limited archival of expired keys (forensic use)
- **Zeroization**: Secure deletion of all keys on tamper or command

### Tamper Detection and Response
- **Physical Tamper**: Detection of case opening or intrusion
- **Electronic Tamper**: Detection of power glitching or voltage manipulation
- **Side-Channel Protection**: Protection against side-channel attacks (power analysis, timing)
- **Automatic Zeroization**: Immediate key deletion upon tamper detection
- **Tamper Log**: Logging of tamper attempts
- **PIN Entry**: Excessive failed PIN attempts trigger zeroization

### FIPS 140-2 Compliance Levels
- **Level 1**: Basic security (software encryption)
- **Level 2**: Physical tamper-evidence (seals, coatings)
- **Level 3**: Physical tamper-response (active intrusion detection, key zeroization)
- **Level 4**: Physical envelope protection (complete environmental protection)
- **P25 Requirement**: Typically Level 2 or Level 3 for public safety radios

## Encryption Key Management Best Practices

### Operational Security (OPSEC)
- **Key Custodian**: Designate authorized crypto custodians
- **Training**: Comprehensive training for key management personnel
- **Two-Person Integrity**: Two-person rule for sensitive key operations
- **Separation of Duties**: Separate roles for key generation, distribution, auditing
- **Physical Security**: Secure storage for key fill devices
- **Access Control**: Restricted access to key management systems
- **Background Checks**: Security clearance for crypto custodians
- **Audit Compliance**: Regular audits of key management practices

### Key Distribution Security
- **Courier**: Secure courier for manual KEK distribution
- **Chain of Custody**: Documented chain of custody for key material
- **Encryption**: Encrypted transport of key fill devices
- **Verification**: Verify key receipt and installation
- **Destruction**: Secure destruction of superseded keys
- **Inventory**: Maintain inventory of all keys and key fill devices

### Incident Response
- **Compromise Detection**: Monitoring for potential key compromise
- **Response Plan**: Documented incident response plan
- **Emergency Contacts**: 24/7 contact list for crypto incidents
- **Forensics**: Forensic investigation capability
- **Recovery**: Rapid recovery procedures

### Compliance and Auditing
- **CJIS Security Policy**: Compliance with FBI CJIS Security Policy
- **FIPS 140-2**: Use of FIPS 140-2 certified cryptographic modules
- **NIST Guidelines**: Follow NIST key management guidelines (SP 800-57)
- **Audit Logs**: Comprehensive audit logging
- **Regular Audits**: Annual or semi-annual key management audits
- **Penetration Testing**: Regular security testing of KMI
- **Vulnerability Management**: Patch management for KMI servers
