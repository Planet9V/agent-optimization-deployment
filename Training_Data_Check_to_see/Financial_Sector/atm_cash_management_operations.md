# ATM Cash Management Operations

## Overview
Automated Teller Machine (ATM) cash management encompasses the complete lifecycle of currency handling, from vault loading to transaction dispensing, ensuring continuous availability while maintaining security and audit compliance.

## Operational Procedures

### 1. Cash Vault Loading Operations
- **Cash Cassette Preparation**: Armored courier personnel verify currency denominations ($20, $50, $100 bills) against manifest documents before loading into ATM cassettes
- **Bill Authentication**: Each currency note passes through counterfeit detection systems using UV, magnetic ink, and infrared scanning technologies
- **Cassette Capacity Management**: Standard ATM cassettes hold 2,000-3,000 bills per denomination, with dual-cassette configurations supporting high-volume locations
- **Load Balancing Algorithm**: Distribution of denominations follows predictive analytics based on historical withdrawal patterns and day-of-week trends

### 2. Dispensing Logic and Transaction Processing
- **Withdrawal Request Parsing**: ATM controller receives transaction amount from core banking system and determines optimal bill combination
- **Bill Validation Pre-Dispensing**: Each bill passes through double-feed detection sensors and thickness measurement before presentation
- **Jam Detection and Recovery**: Optical sensors detect dispensing failures; system automatically retracts jammed bills and reattempts from alternate cassette
- **Partial Dispense Handling**: If complete amount cannot be dispensed, ATM offers closest available amount or cancels transaction with no account debit

### 3. Cash Balancing and Reconciliation
- **Real-Time Balance Tracking**: ATM maintains running count of bills dispensed per cassette, comparing against physical sensor counts
- **End-of-Day Reconciliation**: Nightly batch process reconciles ATM-reported dispensed amounts against core banking posted withdrawals
- **Variance Investigation**: Discrepancies exceeding $50 trigger automated alerts to cash operations team for physical cassette inspection
- **Replenishment Threshold Monitoring**: Predictive algorithms forecast depletion dates based on current balance and historical velocity

### 4. Out-of-Service Procedures
- **Cash-Out Condition**: When all cassettes fall below minimum threshold (typically 200 bills), ATM displays "Temporarily Unable to Dispense Cash"
- **Emergency Cash Delivery**: Armored courier dispatched based on ATM priority tier (Tier 1: 4-hour SLA, Tier 2: next business day)
- **Alternate ATM Notification**: Mobile banking apps and ATM locator websites updated in real-time to redirect customers
- **Service Restoration Verification**: After replenishment, test transactions confirm proper dispensing before returning to service

### 5. Security and Audit Controls
- **Dual Custody Requirements**: All cash loading operations require two authorized personnel with independent access codes
- **Video Surveillance Integration**: ATM cameras record all servicing activities with synchronized timestamps to cash handling logs
- **Tamper Detection Systems**: Accelerometers detect physical attacks; vibration sensors trigger alarm and automatic cash cassette locking
- **Audit Trail Logging**: Immutable ledger records every cash movement event (load, dispense, removal) with personnel ID and cryptographic signature

## System Integration Points

### Core Banking Integration
- **Real-Time Authorization**: ATM queries core banking system via ISO 8583 messaging for account balance verification before dispensing
- **Transaction Posting**: Successful withdrawals post to customer accounts within 2 seconds; reversals post if dispensing fails after authorization
- **Card Network Routing**: PIN verification and authorization requests route through Visa/Mastercard networks for non-proprietary cards

### Cash Forecasting Analytics
- **Machine Learning Models**: Predictive algorithms analyze 90-day historical data, weather patterns, local events, and payroll cycles
- **Dynamic Replenishment Scheduling**: Armored courier routes optimized daily based on forecasted depletion dates and service cost efficiency
- **Seasonal Adjustment Factors**: Holiday periods and tax refund seasons trigger elevated cash loading to prevent outages

### Monitoring and Alerting Systems
- **SNMP Trap Integration**: ATM devices send real-time status updates to network operations center (NOC) monitoring systems
- **Critical Alert Escalation**: Cash-out conditions, hardware failures, and security events trigger SMS/email to on-call personnel
- **Dashboard Visualization**: Operations teams view real-time ATM fleet status, cash levels, and transaction throughput metrics

## Regulatory Compliance

### PCI-DSS Requirements
- **Cardholder Data Protection**: ATM systems encrypt PIN blocks using Triple-DES with hardware security modules (HSMs)
- **Physical Security Standards**: ATM locations meet PCI-DSS requirements for camera coverage, access controls, and environmental sensors
- **Quarterly Vulnerability Scanning**: Third-party assessors conduct penetration testing and vulnerability assessments

### Bank Secrecy Act (BSA) / Anti-Money Laundering (AML)
- **Transaction Reporting**: Withdrawals exceeding $10,000 automatically generate Currency Transaction Reports (CTRs) filed with FinCEN
- **Structuring Detection**: Pattern analysis identifies customers making multiple withdrawals just below $10,000 threshold
- **Suspicious Activity Monitoring**: Unusual withdrawal patterns (frequency, amount, time-of-day) trigger SAR investigation workflows

### ADA Compliance
- **Accessible Design Requirements**: ATMs must have audible instructions, tactile keypads, and reach ranges compliant with Americans with Disabilities Act
- **Voice Guidance Systems**: Headphone jacks provide step-by-step transaction instructions for visually impaired customers
- **Keyboard Height Standards**: Input devices positioned 48 inches or lower for wheelchair accessibility

## Equipment and Vendors

### ATM Hardware Manufacturers
- **NCR Corporation**: SelfServ series ATMs with cash recycling and deposit automation capabilities
- **Diebold Nixdorf**: DN Series with biometric authentication and contactless card readers
- **Hyosung**: Halo II multi-function ATMs with check imaging and coin dispensing modules

### Cash Cassette Technology
- **Standardized Cassette Format**: Modular cassettes compatible across manufacturer platforms for operational flexibility
- **Anti-Fishing Technology**: Cassettes feature mechanical locks preventing external retrieval of bills through card slot or deposit opening
- **Bill Capacity Sensors**: Optical and ultrasonic sensors provide real-time bill counts accurate to ±5 bills

### Armored Courier Services
- **Brinks**: Cash-in-transit services with GPS-tracked vehicles and dual-guard protocols
- **Loomis**: Integrated cash management including vault services, forecasting, and ATM replenishment
- **GardaWorld**: End-to-end currency handling from Federal Reserve pickup to ATM loading

## Performance Metrics

### Operational KPIs
- **Uptime Availability**: Target 99.5% operational availability excluding scheduled maintenance windows
- **Mean Time to Repair (MTTR)**: Average 4 hours for Tier 1 ATMs, 24 hours for Tier 2 locations
- **Cash-Out Rate**: Goal <2% of ATM-days experiencing zero cash condition during business hours
- **Dispensing Accuracy**: Target >99.95% accuracy between dispensed amount and account debit

### Financial Metrics
- **Cash Carrying Cost**: Interest expense on idle cash inventory balanced against outage costs and customer dissatisfaction
- **Replenishment Cost per Fill**: Armored courier fees ($150-300 per visit) optimized through route efficiency and fill frequency
- **Return on Assets**: Transaction fee revenue and customer retention value compared to ATM capital and operating expenses

---

**Document Control**
- **Version**: 1.0
- **Last Updated**: 2025-11-06
- **Regulatory References**: PCI-DSS v4.0, BSA/AML, ADA Title III, FFIEC IT Examination Handbook
- **Review Cycle**: Quarterly
