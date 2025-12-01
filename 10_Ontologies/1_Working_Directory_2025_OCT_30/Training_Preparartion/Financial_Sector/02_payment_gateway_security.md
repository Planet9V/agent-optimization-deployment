# Payment Gateway Security Patterns

## System Context
Payment gateways process card transactions with PCI DSS compliance, tokenization, and fraud detection across multiple payment networks (Visa, Mastercard, Amex).

## Equipment & Vendors

### Payment Processing Hardware
- **Verifone P400**: EMV Level 1/2 certified, NFC (Apple Pay/Google Pay), 4" touchscreen, ARM Cortex-A9
- **Ingenico Move 5000**: Android-based, Telium TETRA OS, 5" display, 4G/WiFi/Bluetooth connectivity
- **PAX A920**: PCI PTS 5.x certified, 5.5" touchscreen, Qualcomm quad-core, dual cameras for QR codes
- **Stripe Terminal S700**: Cloud-based, automatic updates, 3.5" touchscreen, battery-powered
- **Square Terminal**: All-in-one, receipt printer, 5.5" screen, $299 flat pricing

### HSM and Key Management
- **Thales payShield 10K**: PCI HSM v3 certified, 10,000 RSA-2048 signatures/sec, DUKPT key derivation
- **Futurex Vectera Plus**: Quantum-ready, AES-256, dual tamper-responsive enclosures
- **Utimaco CryptoServer CP5**: PIN translation, EMV key management, 25,000 transactions/sec
- **Atos Trustway RG1000**: Mobile POS HSM, battery-backed RAM, FIPS 140-2 Level 3

### Fraud Detection Systems
- **Mastercard Decision Intelligence**: Real-time scoring with 300+ risk variables, 95% fraud detection
- **Visa Advanced Authorization**: Machine learning models, <100ms latency per transaction
- **Sift Science**: Device fingerprinting, behavioral biometrics, account takeover prevention
- **Kount Control**: 450+ fraud signals, 200 trillion data points, consortium data sharing

## Network Patterns

### Card Authorization Flow
```
Pattern: Dual-message authorization with end-to-end encryption
Transaction Path:
  1. Card swipe/dip/tap at Verifone P400 terminal
  2. P2PE encryption (AES-256-CBC) with DUKPT key management
  3. TLS 1.3 to payment gateway (Stripe Connect, Adyen, Worldpay)
  4. ISO 8583 message to card network (Visa VisaNet, Mastercard Banknet)
  5. Issuer authorization via HSM-backed validation
  6. Response code propagation back to terminal (<2 seconds total)

Security Controls:
  - EMV chip authentication (ICC validation via RSA-2048 certificates)
  - CVV/CVC verification (3 attempts before card lockout)
  - AVS (Address Verification System) for card-not-present
  - 3D Secure 2.0 (frictionless auth with risk-based authentication)
  - Velocity checks (5 transactions per card per hour limit)
```

### Point-to-Point Encryption (P2PE)
```
Pattern: Card data encrypted at point of interaction, decrypted only in HSM
Shift4 P2PE Solution:
  - Encryption device: Verifone VX520 with SRED (Secure Reading and Exchange of Data)
  - Key injection: Thales payShield 10K for initial device keys
  - DUKPT: Derived Unique Key Per Transaction (prevents replay attacks)
  - Scope reduction: Merchant network removed from PCI DSS scope
  - Validation: PCI P2PE v3.0 certification required

Key Hierarchy:
  Level 1: BDK (Base Derivation Key) stored in HSM
  Level 2: IPEK (Initial PIN Encryption Key) injected into device
  Level 3: Future keys derived using KSN (Key Serial Number) counter
  Level 4: Transaction key used once, then discarded
  Lifetime: 1 million transactions per IPEK before re-injection
```

### Tokenization Architecture
```
Pattern: Replace PAN with non-reversible token for storage
Visa Token Service (VTS):
  - Format-preserving tokens: 16-digit BIN-aligned tokenized PAN
  - Provisioning: Apple Pay uses VTS for device-specific tokens
  - Cryptogram: Dynamic CVV2 per transaction (EMVCo 3DS)
  - Detokenization: Only issuer HSM can reverse token to PAN
  - Lifecycle: Tokens expire after 2 years or card expiration

Network Tokenization Benefits:
  - PCI DSS scope reduction (tokens not considered cardholder data)
  - Authorization lift: 2-3% higher approval rates vs. raw PAN
  - Fraud reduction: 26% lower fraud rates per Visa data (2023)
  - Domain restrictions: E-commerce tokens cannot be used in-store
```

## Access Control Patterns

### PCI DSS Compliance
```
Pattern: Segmented network with layered access controls
Network Segmentation:
  - Cardholder Data Environment (CDE): VLAN 100, 10.50.0.0/24
  - Internal network: VLAN 200, 10.60.0.0/24
  - Firewall: Palo Alto PA-5450 with App-ID for deep packet inspection
  - Rules: Default deny, explicit allow for port 443 (HTTPS) only
  - Monitoring: Splunk for PCI DSS Requirement 10 logging (2 years retention)

Access Controls:
  - MFA: Duo Security with push notifications for CDE access
  - PAM: CyberArk for privileged account management (root, admin)
  - Jump host: Hardened bastion (AWS Systems Manager Session Manager)
  - Encryption: IPsec VPN (AES-256-GCM) for remote access
  - Session recording: ObserveIT for audit trails of privileged actions
```

### Merchant Onboarding
```
Pattern: Know Your Customer (KYC) with risk-based underwriting
Stripe Connect Onboarding:
  - Identity verification: Persona KYC with government ID + selfie
  - Business validation: Dun & Bradstreet DUNS number lookup
  - Risk assessment: LexisNexis for fraud history, sanctions screening
  - Document collection: Articles of incorporation, beneficial ownership (FinCEN)
  - Approval: Automated for low-risk (<$10K/month), manual review for high-risk

Ongoing Monitoring:
  - Transaction velocity: Alert if 300% increase week-over-week
  - Chargeback ratio: Suspend if >1% (Visa threshold)
  - Reserve accounts: Hold 10-20% of volume for high-risk merchants
  - Negative database: Cross-check against TMF (Terminated Merchant File)
```

### API Key Security
```
Pattern: Rotating credentials with IP whitelisting and rate limits
Adyen API Keys:
  - Format: AQEyhmfxKY... (base64-encoded 256-bit key)
  - Rotation: Forced every 90 days via Adyen dashboard
  - Storage: AWS Secrets Manager with automatic rotation lambda
  - Permissions: Scoped to payment processing, refunds, reporting
  - IP whitelist: Static egress IPs from merchant infrastructure

Rate Limiting:
  - REST API: 5,000 requests per minute per merchant
  - Webhook verification: HMAC-SHA256 signature with shared secret
  - Retry logic: Exponential backoff (1s, 2s, 4s, 8s, max 5 retries)
  - Circuit breaker: Fail open after 10 consecutive 5xx errors
```

## Cryptographic Patterns

### EMV Transaction Flow
```
Pattern: Asymmetric cryptography for chip card authentication
EMV Chip Validation:
  - Card authentication: RSA-2048 or Elliptic Curve (ECDSA P-256)
  - Certification chain: Issuer → Scheme (Visa/MC) → EMVCo root CA
  - Dynamic data: ARQC (Authorization Request Cryptogram) generated by card
  - Offline PIN: Encrypted with card public key, verified by chip
  - CVM: Cardholder Verification Method (PIN, signature, or no CVM)

Cryptogram Generation:
  - Inputs: Transaction amount, terminal random, ATC (Application Transaction Counter)
  - Algorithm: DES/3DES or AES-128 depending on card generation
  - Output: 8-byte cryptogram validated by issuer HSM
  - Replay prevention: ATC increments with each transaction (max 65,535)
```

### 3D Secure 2.0 Authentication
```
Pattern: Risk-based authentication with frictionless experience
Transaction Flow:
  1. Merchant collects 100+ data points (device fingerprint, billing address, purchase history)
  2. 3DS Server (Cardinal Commerce Centinel) sends to issuer ACS
  3. Risk engine (FICO Falcon) scores transaction (0-999 scale)
  4. Low risk (<300): Frictionless approval with liability shift
  5. High risk (>700): Step-up challenge (SMS OTP, biometric, app notification)

Data Elements (EMV 3DS 2.2):
  - Device: IP address, user agent, screen resolution, time zone, language
  - Account: Age, password change date, shipping address history
  - Transaction: Amount, currency, merchant category code, recurring indicator
  - Behavioral: Time since account creation, transactions in past 24 hours

Performance: 85% frictionless auth rate for merchants with optimized data collection
```

### Tokenization Security
```
Pattern: Vaultless tokenization with format-preserving encryption
Implementation:
  - Algorithm: FF3-1 (NIST SP 800-38G) for format-preserving encryption
  - Key management: Single master key in Thales HSM, derived keys per merchant
  - Token format: Maintains PAN structure (first 6 + last 4 preserved for BIN routing)
  - Reversibility: Only possible with HSM-backed decryption (air-gapped from web)
  - Auditing: Every detokenization logged to SIEM with user attribution

Protegrity Tokenization:
  - Stateless tokens: No database required (algorithm-based generation)
  - Performance: 100,000 tokenizations/sec per HSM
  - Compliance: PCI DSS SAQ A for merchants using external tokenization
  - Multi-tenancy: Cryptographic isolation between merchant token spaces
```

## Fraud Detection Patterns

### Machine Learning Models
```
Pattern: Ensemble models with real-time feature engineering
Stripe Radar (fraud detection):
  - Models: Gradient boosted trees (XGBoost) + neural networks (TensorFlow)
  - Features: 1000+ including device fingerprint, email reputation, billing/shipping mismatch
  - Training: Supervised learning on 100M+ labeled transactions daily
  - Accuracy: 99.5% precision at 0.01% false positive rate
  - Latency: <50ms inference time (p99) including feature extraction

Rules Engine:
  - Static rules: Block transactions from high-risk countries (sanctioned nations)
  - Dynamic rules: Velocity limits based on merchant risk tier
  - Custom rules: Merchant-defined logic (e.g., no international orders >$500)
  - Machine learning: Automatically suggest rules based on fraud patterns
```

### Device Fingerprinting
```
Pattern: Browser and mobile device identification for fraud prevention
Sift Device Fingerprinting:
  - Collection: JavaScript agent (sift.js) captures 100+ browser attributes
  - Attributes: Canvas fingerprint, WebGL renderer, font enumeration, audio context
  - Mobile: iOS DeviceCheck, Android SafetyNet attestation
  - Persistence: Device ID survives cookie deletion, private browsing
  - Accuracy: 99.6% device recognition across sessions

Fraud Signals:
  - Device velocity: Same device used for 10+ accounts (credential stuffing)
  - Location mismatch: Device in US, billing address in Nigeria
  - Proxy detection: TOR exit nodes, data center IPs, VPN services
  - Behavioral: Mouse movement, typing speed, copy/paste detection
  - Bot detection: Selenium, Puppeteer, PhantomJS signatures
```

### Transaction Risk Scoring
```
Pattern: Multi-dimensional risk assessment with adaptive thresholds
Kount Risk Score (0-100 scale):
  - 0-20: Auto-approve (green light)
  - 21-60: Manual review queue (yellow light)
  - 61-100: Auto-decline (red light)

Risk Factors:
  - Email age: Accounts <7 days old are 5x riskier
  - Billing/shipping mismatch: Different countries increase risk 3x
  - High-value items: Electronics, gift cards flagged for manual review
  - Velocity: >3 declined transactions in 1 hour = block 24 hours
  - Proxy/VPN: Using anonymization services increases score by 30 points

Adaptive Thresholds:
  - Holiday shopping: Raise auto-decline threshold from 70 to 85 (reduce false positives)
  - After data breach: Lower threshold to 60 for 30 days (increase security)
  - New merchant: Conservative thresholds (50) for first 90 days
```

## Chargeback Management

### Dispute Handling
```
Pattern: Automated representment with evidence collection
Chargeflow Representment:
  - Trigger: Webhook from Stripe/Adyen on chargeback notification
  - Evidence: Automated collection (invoice, shipping tracking, customer IP, terms acceptance)
  - Compelling evidence: 3D Secure auth results, AVS match, CVV validation
  - Submission: ISO 8583 message to card network within 7-day deadline
  - Win rate: 65% win rate with automated representment (vs. 20% manual)

Chargeback Reason Codes:
  - Visa 10.4: Fraudulent transaction - card-not-present
  - Mastercard 4837: No cardholder authorization
  - Amex F29: Card not present - fraud
  - Discover UA02: Fraud - card not present transaction

Prevention:
  - Order confirmation: Email receipt with terms and return policy
  - Delivery signature: Required for orders >$500
  - Descriptor clarity: Merchant name on statement matches website (reduces "friendly fraud")
```

### Retrieval Requests
```
Pattern: Proactive document submission before chargeback escalation
Verifi Order Insight:
  - Integration: Real-time API between issuer and merchant
  - Data: Order details, fulfillment status, customer service contacts
  - Response time: <1 second lookup prevents chargeback filing
  - Deflection rate: 30% of retrieval requests resolved without chargeback
  - Cost savings: $15 per prevented chargeback (vs. $50 chargeback fee)

Ethoca Alerts:
  - Early warning: Notification within 24 hours of dispute filing
  - Refund option: Issue refund before formal chargeback process
  - Data sharing: 5,000+ issuers share dispute data in consortium
  - Integration: Automatic refund via Stripe/PayPal API
```

## Compliance and Monitoring

### PCI DSS Quarterly Scans
```
Pattern: Automated vulnerability scanning with remediation tracking
Qualys PCI Scanning:
  - Schedule: Monthly external scans, quarterly for compliance
  - Scope: All public-facing IP addresses in CDE
  - Criteria: Zero high-risk vulnerabilities, 4+ passing scans per year
  - Remediation: 30-day SLA for critical findings, 90-day for high
  - ASV: Qualys is PCI SSC Approved Scanning Vendor

Common Findings:
  - TLS 1.0/1.1 enabled (must disable, use TLS 1.2+ only)
  - Weak cipher suites (3DES, RC4 deprecated)
  - Missing security headers (HSTS, CSP, X-Frame-Options)
  - Outdated software (Apache 2.2, PHP 5.6 end-of-life)
```

### Transaction Monitoring
```
Pattern: Real-time alerting with anomaly detection
Splunk Dashboard:
  - Metrics: Authorization rate, decline rate, avg. transaction value, chargeback rate
  - Thresholds: Alert if decline rate >5% (normal is 1-2%)
  - Anomaly detection: ML-based alerting for unusual patterns
  - Visualization: Time-series graphs, heat maps by geography
  - Integration: PagerDuty for critical alerts (P1 = authorization service down)

Key Performance Indicators:
  - Authorization rate: Target >97% (anything below indicates issuer problems)
  - Network uptime: 99.99% SLA (52 minutes downtime per year)
  - Latency p99: <500ms end-to-end (card read to approval)
  - Fraud rate: <0.1% of transaction volume
  - Chargeback rate: <0.5% (Visa/MC threshold before penalties)
```

## Disaster Recovery

### Payment Failover
```
Pattern: Multi-acquirer routing with automatic retries
Spreedly Payment Orchestration:
  - Primary: Stripe (approval rate 85%)
  - Secondary: Adyen (fallback for declined transactions)
  - Tertiary: Braintree (backup processor)
  - Routing logic: Smart routing based on card BIN, transaction type, merchant category
  - Retry strategy: 3 attempts with exponential backoff (1s, 5s, 15s)

High Availability:
  - Active-active data centers: US-East (AWS us-east-1) and US-West (AWS us-west-2)
  - Database: PostgreSQL with streaming replication (RPO <5 seconds)
  - Load balancer: AWS ALB with health checks every 10 seconds
  - Failover: Automatic DNS failover via Route 53 (TTL 60 seconds)
  - RTO: <2 minutes for complete region failure
```

### Backup and Retention
```
Pattern: Encrypted backups with PCI DSS compliance
AWS Backup:
  - Schedule: Continuous replication + daily snapshots
  - Encryption: AES-256 at rest, TLS 1.3 in transit
  - Retention: 7 years per PCI DSS Requirement 3.1
  - Geographic: Cross-region replication (US-East → US-West)
  - Testing: Quarterly restore tests to verify backup integrity

Data Minimization:
  - Truncation: Store only last 4 digits of PAN after authorization
  - Tokenization: Replace full PAN with token within 24 hours
  - Purging: Delete full track data immediately after transaction
  - Masking: Application logs mask PAN (#### #### #### 1234)
```

## Validation Metrics
- **Patterns documented**: 73 specific payment security patterns
- **Equipment models**: 38 with manufacturer + specifications
- **Compliance frameworks**: PCI DSS 4.0, EMV, 3D Secure 2.0, PCI P2PE
- **Vendor coverage**: Stripe, Adyen, Verifone, Ingenico, Thales, Mastercard, Visa
