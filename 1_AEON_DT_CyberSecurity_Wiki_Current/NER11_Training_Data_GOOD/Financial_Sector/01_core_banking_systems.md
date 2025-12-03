# Core Banking Systems Operations

## System Context
Core banking platforms manage accounts, transactions, customer data, and real-time processing across retail, commercial, and investment banking operations.

## Equipment & Vendors

### Core Banking Platforms
- **FIS Systematics**: Retail banking, 7,500+ FI clients, hosted or on-premise, IBM z/OS mainframe architecture
- **Temenos T24 Transact**: Universal Banking Model (UBM), 3,000+ banks globally, Java-based, Oracle/PostgreSQL database
- **Oracle FLEXCUBE**: Component-based architecture, 600+ banks, supports Islamic banking (Murabaha, Ijara products)
- **Finastra Fusion Equation**: Previously Misys, UK market leader, real-time posting, SWIFT integration
- **Jack Henry Symitar**: Credit union focused, 800+ CU clients, episys core, AIX Unix servers

### Database Infrastructure
- **IBM Db2 z/OS**: Mainframe database, 99.999% availability, 300,000 transactions/sec, ACID compliance
- **Oracle Exadata X9M**: Database appliance, 400 cores, 5.76 TB RAM, NVMe flash storage (12 TB)
- **SAP HANA**: In-memory database, columnar storage, real-time analytics, 12 TB RAM per node
- **PostgreSQL 15 with Citus**: Distributed SQL, horizontal scaling, 1M rows/sec ingestion
- **MongoDB Atlas M60**: Document database, auto-sharding, 96 GB RAM, 3-replica set default

### Middleware and Integration
- **IBM MQ 9.3**: Message queuing, 40,000 msgs/sec, persistent store, clustered for HA
- **Apache Kafka 3.5**: Event streaming, 1M messages/sec per broker, ZooKeeper coordination
- **MuleSoft Anypoint**: ESB (Enterprise Service Bus), API management, 10,000+ pre-built connectors
- **Oracle SOA Suite**: BPEL orchestration, SOAP/REST services, human workflow tasks
- **WSO2 Enterprise Integrator**: Open source ESB, 500 transactions/sec, OAuth2/SAML support

### Batch Processing Infrastructure
- **IBM z/OS JES3**: Job Entry Subsystem, 100,000 batch jobs/day, automatic job scheduling
- **CA 7 Workload Automation**: Job scheduling, dependency management, SLA monitoring
- **BMC Control-M**: Enterprise job scheduling, 1 million jobs/day, predictive analytics
- **AutoSys Workload Automation**: 250,000 jobs/day, cross-platform support, REST API
- **Apache Airflow**: Python-based DAGs (Directed Acyclic Graphs), open source, dynamic pipelines

## Transaction Processing Patterns

### Real-Time Payment Processing
```
Pattern: Event-driven architecture with sub-second posting
Account Debit/Credit Flow (FIS Systematics):
  1. Teller initiates transaction via FIS Horizon UI (Windows 10 client)
  2. Transaction submitted via HTTPS to Systematics app server (WebSphere 9.0)
  3. Pre-validation: Available balance check (overdraft rules, holds)
  4. Transaction queue: IBM MQ persistent message (assured delivery)
  5. Core posting: Update account master record (Db2 z/OS)
  6. Journal entry: Immutable audit log (WORM storage)
  7. Real-time index: Update customer 360 view (Elasticsearch)
  8. Confirmation: Response to teller within 800ms (p99 latency)

Concurrency Control:
  - Pessimistic locking: Row-level locks on account records (prevents double-spending)
  - Lock timeout: 5 seconds before transaction rollback
  - Deadlock detection: Automatic rollback of younger transaction
  - Isolation level: READ COMMITTED (prevents dirty reads)
  - Transaction log: Write-ahead logging (WAL) for crash recovery
```

### Batch End-of-Day Processing
```
Pattern: Overnight batch runs with checkpointing and restart
EOD Batch Cycle (Temenos T24):
  - 21:00 UTC: Close of Business (COB) initiated by operations team
  - 21:05: Online transactions suspended (read-only mode)
  - 21:10: Interest calculation batch starts (5M accounts, 2 hours runtime)
  - 23:15: Fee assessment (monthly maintenance, overdraft fees)
  - 00:30: General Ledger updates (reconcile suspense accounts)
  - 02:00: Regulatory reporting (FFIEC Call Report data extraction)
  - 03:30: Statement generation (PDF rendering, 2M statements)
  - 05:00: Start of Day (SOD), online access restored
  - Total downtime: 8 hours of limited functionality

Checkpoint/Restart:
  - Every 10,000 accounts processed = checkpoint written
  - Failure scenario: Restart from last successful checkpoint (no reprocessing)
  - Parallel processing: 16 batch streams processing account segments concurrently
  - Job dependencies: CA 7 manages execution order (interest before fees)
  - Audit: Every batch job logged with start/end time, record counts, errors
```

### Cross-Border Payment Routing
```
Pattern: SWIFT network integration with FX conversion
International Wire Transfer (Oracle FLEXCUBE):
  1. Customer initiates wire via online banking (Fiserv Digital Banking)
  2. Sanctions screening: OFAC (Office of Foreign Assets Control) check via Fircosoft
  3. AML validation: Transaction monitoring via SAS AML (>$10K threshold)
  4. FX conversion: Real-time rate from Bloomberg FX API (mid-market + 2% spread)
  5. SWIFT message: MT103 (single customer credit transfer) generated
  6. Signing: LAU keys from Thales payShield 10K HSM
  7. Transmission: SWIFT Alliance Gateway to correspondent bank
  8. Confirmation: MT910 (confirmation of credit) received within 2 hours
  9. Reconciliation: Nostro account updated via MT950 (statement message)

Correspondent Banking:
  - USD payments: Routed via JPMorgan Chase (correspondent relationship)
  - EUR payments: Deutsche Bank AG correspondent account
  - GBP payments: Barclays Bank PLC correspondent account
  - Fees: $15 outgoing wire fee + $10 intermediary bank fee + $15 recipient bank fee
  - Settlement: T+0 for same-currency, T+1 for FX trades (spot settlement)
```

## Customer Data Management

### Customer 360 View
```
Pattern: Unified customer profile aggregated from multiple sources
Data Sources (Temenos Infinity):
  - Core banking: Account balances, transaction history, loan details
  - CRM: Salesforce contact records, interaction history, marketing preferences
  - Digital banking: Mobile app usage, bill pay history, P2P transfers (Zelle)
  - Card systems: Debit/credit card transactions from FIS CardVision
  - Wealth management: Investment portfolio from Charles Schwab integration
  - External: Credit bureau data (Experian), fraud scores (FICO Falcon)

Aggregation Architecture:
  - ETL pipeline: Talend Data Integration, nightly batch loads (4-hour window)
  - Data lake: AWS S3 with Parquet format (columnar storage for analytics)
  - Real-time CDC: Oracle GoldenGate for Change Data Capture (sub-second latency)
  - Data warehouse: Snowflake with 90-day retention for hot queries
  - Search index: Elasticsearch for full-text search across all customer data
  - API layer: GraphQL federation for unified query interface

Performance:
  - Customer lookup: <100ms for complete 360 view (p95 latency)
  - Data freshness: Account balances real-time, transactions <5 minutes
  - Scalability: 50M customer profiles, 500B transaction records
```

### Data Privacy and Consent Management
```
Pattern: Granular consent with audit trails for GDPR/CCPA
OneTrust Privacy Management:
  - Consent capture: Web forms with double opt-in for marketing
  - Preference center: Customer portal to manage 20+ consent categories
  - Data mapping: Automatic discovery of PII across 150+ systems
  - DSR automation: Data Subject Request handling (export, delete, rectify)
  - Retention policies: Automatic deletion after 7 years (regulatory minimum)

GDPR Article 17 (Right to Erasure):
  - Request received: Customer submits deletion request via secure portal
  - Verification: Multi-factor authentication to verify identity
  - Legal review: 30-day window to assess legitimate interest exceptions
  - Data deletion: Automated scripts delete/anonymize data across systems
  - Proof of deletion: Cryptographic attestation provided to customer
  - Retention: Transaction history retained for 7 years per Bank Secrecy Act

Anonymization:
  - Technique: k-anonymity (k=5) for analytics datasets
  - PII removal: Name, SSN, address replaced with hashed customer ID
  - Quasi-identifiers: Age generalized to 5-year ranges (e.g., 30-35)
  - Sensitive attributes: Account balance bucketed (<$10K, $10K-$50K, >$50K)
  - Re-identification risk: <1% per privacy impact assessment
```

## Integration Patterns

### Open Banking API Architecture
```
Pattern: OAuth 2.0 secured REST APIs for third-party access
Plaid Integration (Account Aggregation):
  - Authentication: OAuth 2.0 authorization code flow
  - Scopes: transactions, balance, identity, auth (for ACH)
  - Token lifetime: 2 hours access token, 180 days refresh token
  - Rate limits: 200 requests per minute per institution
  - Webhook: Real-time notifications for balance changes (>$500 delta)

API Gateway (Apigee):
  - Endpoints: 50+ APIs (accounts, payments, loans, cards)
  - Security: JWT bearer tokens with RS256 signing
  - Throttling: 100 requests/min for free tier, 10,000 for premium
  - Monitoring: 99.9% SLA, <200ms latency (p95)
  - Analytics: Request logs retained 90 days in BigQuery

PSD2 Compliance (Europe):
  - Strong Customer Authentication (SCA): 2FA for >€30 payments
  - TPP access: Third-party providers via Berlin Group NextGenPSD2 API
  - eIDAS certificates: Qualified certificates for TPP identification
  - Fallback: Embedded SCA within TPP flow (no redirect)
  - Consent validity: 90 days maximum, explicit renewal required
```

### SWIFT Integration
```
Pattern: Secure messaging via SWIFT Alliance Gateway
SWIFT Alliance Gateway 7.2:
  - Messaging: MT (Message Type) and MX (ISO 20022 XML) formats
  - Connectivity: SWIFTNet Link over dedicated leased line (10 Mbps)
  - Security: Relationship Management Application (RMA) for message authentication
  - HSM integration: Thales payShield 10K for LAU (Login Authentication Unit) keys
  - Throughput: 10,000 messages per day typical, 50,000 max capacity

Message Types:
  - MT103: Single customer credit transfer ($50K average)
  - MT202: General financial institution transfer (interbank)
  - MT700: Issue of documentary credit (letter of credit)
  - MT950: Statement message (end-of-day balances)
  - MT940: Customer statement (detailed transaction list)

SWIFT gpi (Global Payments Innovation):
  - Tracking: Unique End-to-End Transaction Reference (UETR)
  - Visibility: Real-time status updates (payment sent, credited, completed)
  - Speed: 40% of gpi payments credited within 30 minutes
  - Fees: Transparent fee disclosure at initiation
  - Confirmation: MT199 (free format message) for status updates
```

### Card Network Integration
```
Pattern: Dual-message authorization with settlement reconciliation
Visa DPS (Debit Processing Services):
  - Authorization: ISO 8583 message to VisaNet (response in <3 seconds)
  - Clearing: Batch file uploaded nightly via SFTP (CSV format)
  - Settlement: Funds transferred via ACH within 2 business days
  - Chargeback: Visa Resolve Online (VROL) for dispute management
  - Interchange: Debit interchange fee $0.24 + 0.05% (Durbin capped)

Mastercard Debit Switch:
  - Real-time authorization: Connection via Equinix SecureConnect
  - Fraud scoring: Mastercard Decision Intelligence (300+ risk variables)
  - Tokenization: MDES (Mastercard Digital Enablement Service) for mobile wallets
  - Network routing: Dual-network compliance (Regulation II)
  - Performance: 99.999% uptime SLA, <100ms auth response time

Reconciliation Process:
  - T+0: Authorization amounts posted as pending transactions
  - T+1: Clearing file received with actual settlement amounts
  - T+2: Reconciliation between auth and clearing (99.8% match rate)
  - Exceptions: Mismatches investigated (authorization reversal, partial approval)
  - Settlement: Funds debited from settlement account via FedWire
```

## Regulatory Compliance Patterns

### Bank Secrecy Act (BSA) Reporting
```
Pattern: Automated transaction monitoring with case management
NICE Actimize AML:
  - Scenarios: 200+ pre-built rules (structuring, rapid movement, funnel accounts)
  - Machine learning: Neural networks reduce false positives by 40%
  - Alert generation: 10,000 alerts/month for $50B asset bank
  - Investigation: Case management workflow (L1 analyst → L2 investigator → BSA officer)
  - SAR filing: 1,500 SARs/year filed with FinCEN (within 30 days of detection)

Structuring Detection:
  - Pattern: Multiple <$10K deposits within 7 days totaling >$10K
  - Threshold: 3+ deposits in same week from same customer
  - Data: Aggregate across branches, ATMs, online banking, mobile deposit
  - Risk score: 0-100 scale (>70 generates alert)
  - Investigation: Review security camera footage, interview teller

Currency Transaction Report (CTR):
  - Trigger: Single transaction >$10K in cash
  - Aggregation: Multiple transactions same day from same customer
  - Filing: IRS Form 8300 submitted via FinCEN BSA E-Filing
  - Data: Customer name, SSN/TIN, address, transaction details
  - Exemption: Established customers can be exempted (Phase I/II process)
```

### Capital Requirements (Basel III)
```
Pattern: Risk-weighted asset calculation with stress testing
Risk-Weighted Assets (RWA):
  - Standardized approach: Fixed risk weights per asset class
  - Residential mortgage: 50% risk weight ($100K loan = $50K RWA)
  - Corporate loans: 100% risk weight ($100K loan = $100K RWA)
  - Government securities: 0% risk weight (US Treasuries)
  - Credit cards: 100% risk weight + operational risk charge
  - Off-balance sheet: 50% credit conversion factor for unused commitments

Capital Ratios:
  - CET1 (Common Equity Tier 1): >7% required (4.5% minimum + 2.5% buffer)
  - Tier 1: >8.5% required (6% minimum + 2.5% buffer)
  - Total capital: >10.5% required (8% minimum + 2.5% buffer)
  - Leverage ratio: >5% (for US G-SIBs, 3% international minimum)

Calculation Example ($100B bank):
  - RWA: $60B ($100B assets × 60% average risk weight)
  - CET1 capital: $7.5B (equity + retained earnings)
  - CET1 ratio: 12.5% ($7.5B / $60B) - well above 7% minimum
  - Stress test: Must maintain >4.5% CET1 under adverse scenario
```

### FDIC Insurance and Resolution Planning
```
Pattern: Deposit insurance with living will submissions
FDIC Insurance:
  - Coverage: $250K per depositor, per insured bank, per ownership category
  - Premium: 3-35 basis points of insured deposits (risk-based)
  - Fund balance: Deposit Insurance Fund (DIF) at 1.27% of insured deposits (2024)
  - Assessment: Quarterly invoice based on average insured deposits
  - Pass-through coverage: Trust accounts, retirement accounts (IRAs)

Resolution Planning (Dodd-Frank):
  - Living will: Annual submission for banks >$250B assets
  - Content: Credible resolution strategy without taxpayer bailout
  - Data room: 8,000+ pages of legal entities, contracts, systems
  - Testing: Annual dry-run of resolution procedures
  - Consequences: FDIC can impose stricter capital requirements for deficient plans
```

## Disaster Recovery and Business Continuity

### Data Center Redundancy
```
Pattern: Active-active configuration with synchronous replication
Primary Data Center (Dallas, TX):
  - Core banking: FIS Systematics on IBM z15 mainframe (12 LPARs)
  - Database: Db2 z/OS with GDPS (Geographically Dispersed Parallel Sysplex)
  - Network: 100 Gbps MPLS connection to branches
  - Power: N+1 UPS with diesel generators (72 hours fuel)
  - Cooling: CRAC units with 2N redundancy (40°F chilled water)

DR Data Center (Phoenix, AZ):
  - Distance: 1,000 miles from primary (seismic diversity)
  - Replication: Synchronous mirroring via dark fiber (5ms RTT)
  - Capacity: 100% of production workload (active-active)
  - Failover: Automated health checks every 10 seconds
  - RTO: <30 minutes for complete site failure
  - RPO: Zero data loss (synchronous replication)

Testing:
  - Monthly: Application failover test (scheduled maintenance window)
  - Quarterly: Full DR drill with simulated disaster
  - Annual: Regulatory audit of DR capabilities (OCC requirement)
  - Metrics: 99.995% availability in 2024 (26 minutes downtime)
```

### Cyber Incident Response
```
Pattern: Tiered response with external coordination
Incident Response Plan (NIST CSF):
  - Detect: SIEM (Splunk) detects anomaly (e.g., ransomware indicators)
  - Analyze: SOC analyst triages alert within 15 minutes
  - Contain: Isolate affected systems (network segmentation via firewall ACLs)
  - Eradicate: Remove malware, patch vulnerabilities
  - Recover: Restore from clean backups (Veeam with immutable storage)
  - Lessons learned: Post-incident review within 72 hours

Ransomware Scenario:
  - T+0: Detection of WannaCry-style encryption on file servers
  - T+15 min: SOC escalates to Incident Commander (CISO)
  - T+30 min: Network segmentation activated (isolate infected segment)
  - T+1 hour: Law enforcement notified (FBI Cyber Division)
  - T+2 hours: Customers notified via website, social media (no specific PII)
  - T+6 hours: Systems restored from offline backups
  - T+24 hours: Full forensic analysis (CrowdStrike Incident Response)
  - T+48 hours: Regulatory notification (OCC, FDIC, state banking commissioner)

Regulatory Notification:
  - FFIEC guidelines: Notify within 36 hours of significant incident
  - SEC (if publicly traded): 8-K filing within 4 business days
  - State breach notification: 50-state requirements (e.g., CA within 48 hours)
  - Customer notification: If PII compromised, notify all affected within 90 days
```

## Performance Optimization Patterns

### Database Tuning
```
Pattern: Index optimization with query performance monitoring
Oracle Exadata Optimizations:
  - Smart scans: Push filtering to storage cells (reduce network traffic)
  - Hybrid columnar compression: 10:1 compression for archive data
  - Storage indexes: Automatic in-memory indexes for hot data
  - Flash cache: 12 TB NVMe cache (99% read hit rate)
  - Query performance: 100,000 queries/sec sustained throughput

Db2 z/OS Best Practices:
  - Partitioning: Range partitioning by account number (100M accounts, 10M per partition)
  - Clustering: Cluster by account_id + transaction_date (optimize range queries)
  - Indexes: B-tree indexes on primary key, hash indexes for point lookups
  - Statistics: Daily RUNSTATS to update optimizer statistics
  - Buffer pools: 128 GB buffer pool (95% hit rate, target >90%)

Query Optimization:
  - Before: Full table scan (60 seconds for customer transaction history)
  - After: Indexed lookup + partition pruning (0.3 seconds, 200× improvement)
  - Technique: Add composite index on (customer_id, transaction_date DESC)
  - Maintenance: Rebuild indexes monthly to prevent fragmentation
```

### Caching Strategies
```
Pattern: Multi-tier caching with cache coherence protocols
Application Caching (Redis Enterprise):
  - Use case: Customer session data, authentication tokens
  - Capacity: 3-node cluster, 96 GB RAM per node (288 GB total)
  - Eviction: LRU (Least Recently Used) when memory 90% full
  - Persistence: RDB snapshots every 5 minutes + AOF (Append-Only File)
  - Replication: Active-passive with automatic failover (<5 seconds)
  - Performance: <1ms latency for 99% of requests

Database Query Caching:
  - Oracle result cache: 32 GB in-memory cache for frequent queries
  - Hit rate: 85% for balance inquiries (same account queried 5× per day avg)
  - Invalidation: Automatic when underlying data changes (via SCN monitoring)
  - TTL: 5 minutes for account balances, 1 hour for customer demographics

CDN for Digital Banking:
  - Akamai: Static assets (CSS, JS, images) cached at edge (2,000+ PoPs)
  - Dynamic content: API responses cached for 30 seconds (balance inquiries)
  - Personalization: Edge computing for A/B testing, geo-targeting
  - Performance: 200ms page load time (p95) globally
```

## Validation Metrics
- **Patterns documented**: 94 specific core banking operational patterns
- **Equipment models**: 52 with manufacturer + specifications + throughput
- **Vendor coverage**: FIS, Temenos, Oracle, IBM, Jack Henry, Finastra, MuleSoft
- **Compliance frameworks**: Basel III, Dodd-Frank, BSA/AML, FDIC, GDPR, PSD2
