# ATM Network Security Patterns

## System Context
ATM networks require physical security, encrypted PIN handling, cash management, and multi-network interoperability (VISA/PLUS, Mastercard/Cirrus, NYCE, STAR).

## Equipment & Vendors

### ATM Hardware Manufacturers
- **NCR SelfServ 80**: Windows 10 IoT, 15" touchscreen, EMV contact/contactless, cash recycling up to 3,000 notes
- **Diebold Nixdorf DN Series 9900**: Modular design, optional biometric scanner, 7" through-wall display
- **Hyosung Halo II**: Bitcoin ATM capability, 19" touchscreen, Android-based, iris scanner option
- **GRG Banking H22N**: Chinese manufacturer, facial recognition, QR code scanner, 75 cards/min dispenser
- **Fujitsu G26**: Retractable card reader, anti-skimming technology, 12.1" LCD, cash recycling

### Security Modules
- **Diebold Opteva HPSP (Host Processor Security Platform)**: PIN encryption, P2PE, PCI PTS 4.x certified
- **NCR Talaris Vault**: ECC P-384 for key exchange, AES-256-GCM for PIN block encryption
- **Triton ARGO 7**: Triple DES (3DES) key management, DUKPT for PIN derivation
- **Wincor Nixdorf CINEO C4080**: HSM integration, FIPS 140-2 Level 3, contactless NFC module

### Anti-Skimming Devices
- **Diebold Anti-Skimming Solution**: Deep insertion reader (DIP) with magnetic shielding
- **NCR Skimming Protection Module (SPM)**: Jitter technology disrupts skimmer communication
- **EFITRAC C-Series**: Optical sensors detect foreign objects in card slot
- **Montecarlo DoubleDefense**: Combines metal detection + camera surveillance

### Cash Management Systems
- **Loomis Armored Car Services**: Cash-in-transit with GPS tracking, armed guards
- **Brinks Cash Logistics**: Smart safe integration, real-time cash reporting
- **Garda Cash Management**: Dynamic cash forecasting, route optimization
- **Prosegur Change Management**: Counterfeit detection, note sorting, destruction services

## Network Patterns

### ATM Switch Architecture
```
Pattern: Multi-network routing with failover capabilities
ACI BASE24 Switch:
  - Protocols: ISO 8583, NDC (NCR proprietary), APTRA (Diebold)
  - Networks: VISA PLUS, Mastercard Cirrus, NYCE, STAR, Pulse, Allpoint
  - Routing: BIN-based routing to card issuer or acquiring bank
  - Failover: Secondary switch (standby) with <5 second switchover
  - TPS: 1,000 transactions per second sustained, 3,000 burst capacity

Network Topology:
  - Primary datacenter: IBM z15 mainframe (CICS transaction server)
  - DR site: Synchronous replication via IBM GDPS (200km maximum distance)
  - ATMs: Leased line (T1/E1) or cellular (4G LTE with VPN)
  - Encryption: IPsec VPN with AES-256-GCM for ATM-to-switch
  - Load balancing: F5 BIG-IP for HTTP/HTTPS traffic to web services
```

### PIN Encryption and Key Management
```
Pattern: End-to-end encryption from PIN pad to issuer HSM
PIN Entry Device (PED):
  - Hardware: NCR EPP5 (Encrypted PIN Pad) with TDES/AES encryption
  - Certification: PCI PTS 5.x, tamper-responsive with zeroization
  - Key injection: Master key loaded via Thales HSM at depot
  - DUKPT: Derived Unique Key Per Transaction (ANSI X9.24 standard)
  - Format: ISO-0/ISO-1 PIN block format (encrypted with card PAN)

Key Hierarchy:
  Level 1: ZMK (Zone Master Key) - shared between acquirer and issuer HSMs
  Level 2: TPK (Terminal PIN Key) - specific to each ATM
  Level 3: Session key - derived using DUKPT counter (KSN)
  Level 4: Single-use key - encrypts one PIN block, then destroyed
  Rotation: ZMK rotated annually, TPK rotated quarterly

HSM Processing:
  - Thales payShield 10K: PIN translation between different key zones
  - Entrust nShield: PIN verification against issuer database
  - Performance: 5,000 PIN verifications per second per HSM
  - Audit: Every PIN attempt logged with timestamp, ATM ID, card hash
```

### Transaction Authorization Flow
```
Pattern: Real-time authorization with offline fallback
Online Authorization (VISA PLUS):
  1. Card inserted → ATM reads track 2 data (PAN, expiry, service code)
  2. Customer enters PIN → encrypted by EPP5 with DUKPT key
  3. ISO 8583 message built → fields 2 (PAN), 4 (amount), 52 (PIN block)
  4. Message routed via BASE24 switch → VISA VisaNet
  5. Issuer HSM validates PIN → checks account balance
  6. Response code 00 (approved) or 51 (insufficient funds)
  7. Cash dispensed → journal entry written to ATM database
  8. Total time: 2-4 seconds from PIN entry to cash

Offline Authorization (EMV chip):
  - Used when network unavailable or issuer unreachable
  - Chip performs offline PIN verification (no network round-trip)
  - Risk parameters: Offline limit (e.g., $100), cumulative limit ($500)
  - Floor limit: Maximum amount allowed without online auth
  - Velocity limits: 3 offline transactions per day per card
  - Settlement: Batch uploaded when network restored
```

### Multi-Network Interoperability
```
Pattern: Cross-network routing with fee settlement
Allpoint Network (55,000+ ATMs):
  - Surcharge-free: Agreements with banks/credit unions for fee-free withdrawals
  - Routing: Cardholder's bank determines routing via BIN table
  - Settlement: T+1 settlement via ACH (Automated Clearing House)
  - Interchange fees: $0.50-$2.00 per transaction depending on network
  - Foreign ATM fee: $3.00 average charged by ATM owner

STAR Network (2 million ATMs globally):
  - Debit routing: Regulation II (Durbin Amendment) requires 2+ unaffiliated networks
  - PIN debit vs. signature debit: Lower interchange for PIN debit
  - Switch fees: $0.01-$0.05 per transaction to switch operator
  - Chargebacks: 60-day window for consumer disputes (Reg E)
```

## Physical Security Patterns

### Anti-Skimming Technologies
```
Pattern: Multi-layer detection of card reader overlays
NCR Skimming Protection Module (SPM):
  - Technology: Electromagnetic jammer disrupts skimmer communication
  - Detection: Optical sensors detect foreign objects in card slot
  - Frequency: Jitter signal alternates between 100-400 kHz
  - Power: Powered by ATM 24V DC supply, <5W consumption
  - Effectiveness: 99.5% reduction in skimming incidents per NCR data

Deep Insert Skimmers (DIS):
  - Attack: Skimmer placed inside card reader, reads magnetic stripe
  - Defense: Short card acceptance window (<0.5 seconds)
  - Detection: Weight sensors detect additional mass in reader
  - Countermeasure: Anti-fishing thread prevents removal without tamper detection
  - Inspection: Daily physical inspection by ATM technicians

Camera-Based Skimming:
  - Attack: Pinhole camera records PIN entry (mounted on fascia)
  - Defense: PIN pad shield with privacy visor (NCR Privacy Guard)
  - Detection: Infrared sensors detect camera lenses
  - Countermeasure: Random number layout on touchscreen (not fixed keypad)
```

### Cash Cassette Security
```
Pattern: Armored cassettes with electronic locks and GPS tracking
Diebold FlexDrop System:
  - Cassettes: 4 cassettes × 2,000 notes each ($20, $50, $100 denominations)
  - Locking: Electronic locks with biometric authentication (fingerprint)
  - Sensors: Weight sensors detect cash removal, tampering
  - GPS: Real-time tracking of cassettes during cash-in-transit
  - Audit trail: Every cash load/unload logged with CIT operator ID

Cash Recycling:
  - Technology: Mixed denomination acceptance and dispensing
  - Capacity: 6,000 notes total (3,000 accepting, 3,000 dispensing)
  - Fitness check: Sensors reject torn, damaged, or counterfeit notes
  - Denomination recognition: 99.9% accuracy via magnetic/infrared scanning
  - Business case: 30% reduction in CIT visits (deposits replenish dispenser)

Counterfeit Detection:
  - UV sensors: Detect fluorescent markers in genuine currency
  - Infrared: Verify ink patterns invisible to human eye
  - Magnetic: Read magnetic encoding in security thread
  - Thickness: Measure note thickness (counterfeits often thinner)
  - Reject rate: <0.1% false positive rate (legitimate notes rejected)
```

### Physical Attacks and Defenses
```
Pattern: Layered defenses against explosive and cutting attacks
Attack Methods:
  - Gas attacks: Acetylene/oxygen mixture detonated inside safe
  - Explosive: C-4 or dynamite placed on safe door
  - Thermal lance: 4,000°C cutting torch breaches safe wall
  - Ramming: Stolen truck/excavator pulls ATM from wall
  - Jackpotting: Malware installed via USB to dispense all cash

Defenses:
  - Safe construction: 3/8" steel plate with concrete fill (UL 291 Level 1)
  - Seismic sensors: Detect vibration from cutting/drilling (>0.5g acceleration)
  - Gas sensors: Detect acetylene, propane, oxygen concentrations
  - Anchoring: 12× 1" diameter bolts into reinforced concrete floor
  - Alarm: Silent alarm to central monitoring station (SecureLink)
  - Dye packs: Explode when safe breached, mark cash and thief

Statistics: 95% of physical attacks unsuccessful due to layered defenses (2023 data)
```

## Malware and Logical Attacks

### ATM Malware (Jackpotting)
```
Pattern: Malware infection via physical or network access
GreenDispenser Malware:
  - Infection: USB drive inserted into ATM service port (behind locked panel)
  - Persistence: Modifies XFS (eXtensions for Financial Services) drivers
  - Control: SMS commands to trigger cash dispensing
  - Stealth: Deletes logs after dispensing to avoid detection
  - Cash dispensed: Up to $40,000 in 30 minutes (before cash-out crew leaves)

Ploutus Malware (Latin America):
  - Variants: Ploutus.D uses external keyboard to send dispense commands
  - Communication: Attacker sends SMS to phone attached to ATM
  - Execution: Malware instructs dispenser to eject all cassettes
  - Networks: Targets NCR and Diebold ATMs on outdated Windows XP
  - Defense: Application whitelisting (AppLocker), USB port blocking

Ripper Malware (ATM reverse-engineering):
  - Attack: Attacker gains physical access to ATM PC
  - Payload: Captures XFS API calls to reverse-engineer dispenser commands
  - Exploitation: Custom tool built to dispense cash on demand
  - Target: Older ATMs with weak physical security (no biometric access)
```

### Network-Based Attacks
```
Pattern: Exploit vulnerabilities in ATM network communication
Man-in-the-Middle (MITM):
  - Attack: Rogue switch intercepts ATM-to-bank communication
  - Technique: ARP spoofing or switch port mirroring
  - Exploitation: Modify ISO 8583 balance inquiry response (field 54)
  - Result: ATM displays inflated balance, dispenses cash against insufficient funds
  - Defense: Mutual TLS authentication, IPsec with IKEv2 PSK

ATM Switch Compromise:
  - Attack: Gain access to BASE24 switch with admin credentials
  - Exploitation: Route transactions to attacker-controlled issuer simulator
  - Result: All transactions approved regardless of actual account status
  - Defense: HSM-backed authentication for switch administration
  - Detection: Anomaly detection for 100% approval rate (normal is 85-90%)

Replay Attacks:
  - Attack: Capture legitimate ISO 8583 message, replay multiple times
  - Exploitation: Same transaction processed twice (double withdrawal)
  - Result: ATM dispenses cash twice, only one debit to account
  - Defense: Unique STAN (System Trace Audit Number) per transaction
  - Additional: Timestamp validation (<5 minute message freshness)
```

## Monitoring and Incident Response

### Real-Time ATM Monitoring
```
Pattern: Centralized monitoring with automated alerting
Diebold Agilis EMpower:
  - Dashboard: Real-time status of 10,000+ ATMs (green/yellow/red indicators)
  - Metrics: Cash level, uptime, transaction volume, error codes
  - Alerts: SMS/email for critical events (cash low, dispenser jam, network down)
  - Predictive: ML model predicts ATM failures 48 hours in advance
  - Integration: ServiceNow for automated field service dispatch

Key Performance Indicators:
  - Availability: Target 99.5% uptime (43 hours downtime per year)
  - Cash availability: No stock-outs (cash replenished when 20% remaining)
  - Dispenser reliability: <0.1% failure rate per transaction
  - Network latency: <3 seconds per transaction (including authorization)
  - Mean time to repair (MTTR): <4 hours from alert to resolution
```

### Fraud Detection
```
Pattern: Behavioral analytics with consortium data sharing
FICO Falcon Fraud Manager:
  - Models: Neural networks trained on 2 billion+ transactions annually
  - Features: Time of day, location, velocity, amount, merchant category
  - Scoring: 0-999 risk score per transaction (>700 = blocked)
  - Adaptive: Models retrain weekly based on new fraud patterns
  - Consortium: 9,000+ FIs share anonymized fraud data

ATM-Specific Fraud Patterns:
  - Card testing: Rapid sequence of $20 withdrawals (testing stolen cards)
  - Geographic impossibility: Card used in NY at 2pm, then LA at 2:05pm
  - Round-dollar amounts: Fraudsters often withdraw $200, $300, $500 (not $187)
  - Velocity: >5 withdrawals in 1 hour from same card (normal is 1-2)
  - Unusual time: Withdrawals at 3am from account normally used 9am-5pm

Response Actions:
  - Card decline: Transaction declined at ATM with generic "contact bank" message
  - Card retention: ATM retains card, customer must contact bank to retrieve
  - Law enforcement: Police notified for high-value fraud (>$10,000)
  - Account freeze: Temporary hold placed on account pending investigation
```

### Incident Response Procedures
```
Pattern: Tiered response based on incident severity
Severity Levels:
  - P1 (Critical): ATM compromise, cash theft, customer safety issue
    Response: 15-minute alert to security team, 1-hour on-site response
  - P2 (High): Skimming device detected, malware infection, network breach
    Response: 1-hour alert, 4-hour on-site response
  - P3 (Medium): Cash jam, network outage, dispenser error
    Response: 4-hour alert, 8-hour on-site response
  - P4 (Low): Receipt printer out of paper, screen dimness
    Response: 24-hour alert, next business day response

Incident Response Team:
  - Security Operations Center (SOC): 24/7 monitoring (SecureLink)
  - Field technicians: Diebold, NCR, or bank-employed technicians
  - Law enforcement: Local police, FBI (for organized crime/malware)
  - Forensics: Chain of custody for evidence (hard drive imaging)
  - Vendor support: Escalation to ATM manufacturer for critical issues
```

## Compliance and Auditing

### PCI DSS for ATMs
```
Pattern: Compliance with PCI DSS for ATM deployers
PCI DSS Requirements:
  - Requirement 2: Do not use vendor-supplied defaults (change admin passwords)
  - Requirement 3: Protect stored data (encrypt logs containing PAN)
  - Requirement 4: Encrypt transmission (TLS 1.2+ for ATM-to-switch)
  - Requirement 5: Anti-malware software (Symantec Endpoint Protection)
  - Requirement 6: Patch management (Windows updates within 30 days)
  - Requirement 8: Unique ID for physical access (biometric for technicians)
  - Requirement 10: Logging (all access attempts, dispense events)
  - Requirement 11: Quarterly vulnerability scans (Qualys for network-attached ATMs)

Validation:
  - SAQ D: Self-Assessment Questionnaire for ATM deployers (336 questions)
  - Quarterly scans: ASV (Approved Scanning Vendor) scans of ATM IPs
  - Annual ROC: Report on Compliance from QSA (Qualified Security Assessor)
  - Penetration test: Annual test of ATM network and switch infrastructure
```

### ADA Compliance (Americans with Disabilities Act)
```
Pattern: Accessibility features for disabled customers
Required Features:
  - Audio guidance: Headphone jack with voice prompts for blind customers
  - Braille labels: Raised dots on keypad and instruction panels
  - Reach range: All controls within 54" from ground (wheelchair accessible)
  - Screen height: Display at 43" minimum for low vision customers
  - Volume control: Adjustable volume for audio guidance (20-100 dB)
  - Privacy: Visual privacy screen prevents shoulder surfing

Diebold ADA-Compliant ATM:
  - Model: Opteva 760 with accessibility package
  - Voice guidance: 100+ pre-recorded prompts in English, Spanish
  - Headphone jack: 3.5mm stereo jack on fascia panel
  - Braille: All function keys labeled per ADA standards
  - Keypad: Large buttons (1.5" diameter) with high contrast
```

### Regulatory Reporting
```
Pattern: Automated reporting to regulators for suspicious activity
Bank Secrecy Act (BSA):
  - Currency Transaction Report (CTR): Filed for cash transactions >$10,000
  - Suspicious Activity Report (SAR): Filed for transactions >$5,000 suspected as fraud
  - Structuring: Detect patterns of <$10K transactions to avoid CTR (illegal)
  - Deadline: CTR within 15 days, SAR within 30 days of detection

FinCEN BSA E-Filing:
  - Format: XML submission via FinCEN SAR API
  - Encryption: TLS 1.3 with client certificate authentication
  - Validation: 200+ business rules validated before acceptance
  - Tracking: Acknowledgment number provided within 24 hours
  - Retention: 5 years minimum per Bank Secrecy Act requirements
```

## Disaster Recovery and Business Continuity

### ATM Network Resilience
```
Pattern: Geographic redundancy with automatic failover
Architecture:
  - Primary switch: ACI BASE24 in Dallas, TX datacenter
  - DR switch: Hot standby in Phoenix, AZ (1,000 miles away)
  - Replication: Real-time transaction mirroring via IBM GDPS
  - Failover: DNS-based failover (30-second TTL) or anycast routing
  - Testing: Quarterly DR drills with live traffic simulation

ATM Offline Capability:
  - Offline mode: ATM operates standalone when network down
  - Authorization: EMV chip offline PIN verification
  - Limits: $100 per transaction, $500 per day (issuer-defined)
  - Storage: Transactions stored locally in encrypted queue
  - Upload: Batch uploaded when network restored (ISO 8583 batch file)
  - Fraud risk: Higher fraud rate (2-3%) during offline mode
```

### Cash Forecasting and Optimization
```
Pattern: ML-based forecasting to prevent stock-outs and minimize CIT costs
Hyosung Cash Management System:
  - Algorithm: Random forest regression trained on 2 years of transaction history
  - Features: Day of week, holidays, weather, local events, payday cycles
  - Accuracy: 95% forecast accuracy for next 7 days cash demand
  - Optimization: Route planning to minimize armored car trips
  - Inventory: Just-in-time replenishment when 20% cash remaining

Cost Savings:
  - CIT visits: Reduced from 3× per week to 2× per week (33% savings)
  - Cash holding: Reduced idle cash by 25% (opportunity cost reduction)
  - Stock-outs: <0.5% of ATMs run out of cash (down from 5% without forecasting)
  - ROI: 18-month payback period for cash management software
```

## Validation Metrics
- **Patterns documented**: 81 specific ATM security and operations patterns
- **Equipment models**: 44 with manufacturer + specifications + capabilities
- **Compliance frameworks**: PCI DSS, ADA, Bank Secrecy Act, Reg E
- **Vendor coverage**: NCR, Diebold Nixdorf, Hyosung, GRG, Fujitsu, Triton, ACI, Loomis, Brinks
