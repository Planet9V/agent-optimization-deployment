# Core Banking Account Maintenance Operations

## Overview
Core banking systems serve as the central ledger and transaction processing engine for financial institutions, managing customer accounts, processing deposits/withdrawals, calculating interest, and generating statements while maintaining data integrity and regulatory compliance across all banking channels.

## Operational Procedures

### 1. Account Opening and Setup
- **Customer Information Verification**: Collection of personally identifiable information (name, SSN, DOB, address) validated against credit bureaus and government databases
- **CIP/KYC Compliance**: Customer Identification Program requires document verification (driver's license, passport) and OFAC/sanctions screening before account activation
- **Account Type Configuration**: System creates appropriate account structures (checking, savings, money market, CD) with product-specific features and fee schedules
- **Initial Funding Requirements**: Minimum opening deposits verified and posted before account becomes fully operational; source of funds documented for large deposits

### 2. Daily Transaction Posting Cycle
- **Batch Processing Windows**: Overnight batch jobs process day's transactions, typically running 11 PM - 5 AM to minimize customer-facing impact
- **Transaction Sequencing Logic**: Deposits posted first, followed by debits in descending dollar amount order (controversial practice benefiting overdraft fees)
- **Memo Post vs. Ledger Balance**: Real-time transactions update memo balance immediately; official ledger balance updates after nightly posting cycle
- **Cutoff Time Management**: Transactions received after daily cutoff (typically 2-5 PM) dated and processed on next business day

### 3. Interest Calculation and Accrual
- **Daily Interest Accrual**: Savings and CD accounts accrue interest daily using daily balance method or average daily balance methodology
- **APY vs. APR Disclosure**: Annual Percentage Yield (APY) includes compounding effects as required by Regulation DD Truth in Savings Act
- **Tiered Rate Structures**: Interest rates vary by balance tier; system applies blended rates when balance spans multiple tiers
- **Negative Interest Environments**: System supports negative interest rates for certain account types in European banking environments

### 4. Fee Assessment and Waivers
- **Monthly Maintenance Fees**: Recurring fees (typically $5-25) assessed on statement cycle date unless waiver criteria met
- **Minimum Balance Waivers**: Fees waived if average daily balance meets threshold (e.g., $1,500 for basic checking, $5,000 for premium)
- **Direct Deposit Waivers**: Regular direct deposits of specified amount (e.g., $500+ monthly) qualify for fee waivers
- **Fee Reversal Workflow**: Customer service representatives authorized to reverse fees within policy limits (e.g., one courtesy reversal per year)

### 5. Overdraft and NSF Processing
- **Available Balance Calculation**: Core system computes real-time available balance as ledger balance minus holds plus overdraft protection limit
- **Overdraft Fee Assessment**: Each transaction overdrawn charged flat fee (typically $35) subject to daily maximum (e.g., 5 fees per day)
- **Opt-In Requirements**: Reg E requires explicit opt-in for overdraft coverage on ATM and debit card transactions
- **Linked Account Transfers**: Overdraft protection transfers funds from linked savings or line of credit to cover shortfalls, charging transfer fee instead of overdraft fee

### 6. Statement Generation and Delivery
- **Statement Cycle Processing**: Monthly statements generated showing beginning balance, transaction history, ending balance, and accrued interest
- **Electronic Delivery Platforms**: Customers opting for e-statements access PDFs via secure online banking portal, reducing print/mail costs
- **Check Image Retention**: Check 21 Act requires banks retain check images 7 years; displayed on statements and available for customer download
- **Regulatory Disclosures**: Statements include required disclosures for Reg E dispute rights, interest rates, and fee changes

### 7. Account Closure and Escheatment
- **Closure Request Processing**: Customer-initiated closures require balance verification, pending transaction clearance, and final statement generation
- **Dormant Account Monitoring**: Accounts with no customer-initiated activity for 12-24 months classified as dormant and assessed inactivity fees
- **Escheatment to State**: Unclaimed funds in accounts abandoned for state-specific period (typically 3-5 years) transferred to state unclaimed property office
- **Negative Balance Write-Offs**: Accounts with outstanding negative balances >180 days closed and charged off, reported to ChexSystems and credit bureaus

## System Integration Points

### Customer Relationship Management (CRM)
- **360-Degree Customer View**: CRM aggregates data from core banking, lending, investments, and CRM interactions for unified customer profile
- **Cross-Sell Opportunities**: Analytics identify customers likely to benefit from additional products based on account behavior and life stage
- **Service Case Management**: Customer service inquiries linked to core banking records for seamless issue resolution and audit trails

### Online and Mobile Banking
- **Real-Time Balance Queries**: Digital channels query core system API for current available and ledger balances with <2 second response time
- **Bill Payment Integration**: Bill pay service submits payment instructions to core system for debiting customer accounts and crediting merchants
- **Mobile Check Deposit**: Image capture on mobile devices processed through core system's remote deposit module with automatic MICR extraction

### ATM and Debit Card Networks
- **Authorization Requests**: Card networks (Visa, Mastercard) query core system via ISO 8583 messages to approve/decline transactions
- **Authorization Holds**: Pending transactions place temporary holds on available balance until final settlement (typically 1-3 days)
- **Settlement Reconciliation**: Daily settlement files from card networks matched against core system authorization logs to post final transactions

### Fraud Detection Systems
- **Real-Time Transaction Data Feed**: Core system provides millisecond-latency transaction data to fraud monitoring platforms
- **Block Codes and Status Updates**: Fraud systems update account block codes (e.g., fraud hold, legal hold) preventing further transactions
- **Alert Workflow Integration**: Suspicious activity alerts route to investigation queues with deep links to core banking transaction details

## Regulatory Compliance

### Regulation D - Reserve Requirements
- **Savings Withdrawal Limits**: Regulation D historically limited "convenient" withdrawals from savings accounts to 6 per statement cycle (suspended 2020)
- **Reserve Ratio Calculations**: Core system tracks deposit balances by category for Fed reserve requirement reporting (currently 0%)
- **Transaction Reclassification**: Excessive withdrawals from savings may trigger automatic conversion to checking account per account agreement

### Regulation E - Electronic Fund Transfer Act
- **Error Resolution Procedures**: Consumers have 60 days from statement date to dispute electronic transactions; bank has 10 days to investigate
- **Provisional Credit Requirements**: If investigation exceeds 10 days, bank must provisionally credit customer account pending investigation completion
- **Liability Limits**: Consumer liability for unauthorized EFT limited to $50 if reported within 2 days, $500 if reported within 60 days

### Regulation DD - Truth in Savings
- **APY Disclosure Requirements**: Account opening disclosures and advertising must show APY calculated per standardized formula
- **Fee Schedule Transparency**: All account fees must be disclosed upfront with 30-day advance notice required for fee increases
- **Statement Requirements**: Periodic statements must show APY earned, fees charged, and contact information for inquiries

### FDIC Insurance and Recordkeeping
- **Deposit Insurance Coverage**: Core system tracks beneficial ownership for accounts to calculate FDIC insurance coverage ($250,000 per depositor per institution)
- **Joint Account Handling**: Joint accounts receive separate insurance coverage for each co-owner's proportional interest
- **Trust Account Titling**: Payable-on-death (POD) and trust accounts require proper titling for insurance coverage calculation accuracy

## Equipment and Vendors

### Core Banking Platforms
- **FIS Horizon**: Market-leading core system for community banks with integrated lending, deposits, and digital banking modules
- **Jack Henry Symitar**: Episys core platform popular among credit unions with flexible configuration and credit union-specific features
- **Temenos T24**: Global core banking platform supporting 150+ currencies and multi-country operations for international banks
- **Finacle (Infosys)**: Cloud-native core banking with microservices architecture enabling rapid product innovation

### Statement Processing Vendors
- **Fiserv**: Print and mail services for paper statements, notices, and debit cards with 24-48 hour turnaround
- **Harland Clarke**: Check printing, statement processing, and direct mail marketing services for financial institutions
- **DST Output**: Digital statement delivery platform with SMS/email notification and secure document retrieval portals

### Compliance and Reporting Tools
- **Wolters Kluwer Compliance Solutions**: Regulatory change management tracking federal and state compliance requirements
- **AffirmX**: Vendor management and third-party risk assessment platform ensuring service provider compliance
- **Ncontracts**: Integrated compliance suite covering BSA/AML, OFAC, fair lending, and information security compliance

### Database and Infrastructure
- **Oracle Exadata**: High-performance database appliance commonly used for core banking transactional systems
- **IBM Db2**: Mainframe-based database supporting legacy core systems at large national banks
- **PostgreSQL**: Open-source database increasingly adopted by modern core banking platforms for cost efficiency and flexibility

## Performance Metrics

### Operational Efficiency
- **Transactions per Second (TPS)**: Core system must support 500-5,000 TPS depending on institution size during peak periods
- **Batch Processing Window**: Complete overnight batch cycle within allotted 6-hour window (11 PM - 5 AM) to ensure readiness for next day
- **System Availability**: Target 99.9%+ uptime during business hours (8 AM - 8 PM); scheduled maintenance limited to low-traffic hours
- **Transaction Posting Accuracy**: >99.99% accuracy with rigorous exception handling and reconciliation processes

### Customer Experience Metrics
- **Time to Open Account**: Online account opening completed in <10 minutes; branch account opening <20 minutes including CIP compliance
- **Statement Delivery Timeliness**: Electronic statements available within 1 business day of cycle close; paper statements mailed within 3 days
- **Dispute Resolution Time**: Average 7-10 business days to resolve transaction disputes and provide final determination
- **Call Center First Contact Resolution**: 75%+ of account inquiry calls resolved without escalation or follow-up required

### Financial Metrics
- **Cost per Account Maintenance**: Industry benchmark $150-250 annual cost per demand deposit account including personnel, technology, and overhead
- **Fee Revenue per Account**: Overdraft, maintenance, and transaction fees generate $75-150 annual revenue per account on average
- **Net Interest Margin (NIM)**: Spread between interest earned on loans/investments and interest paid on deposits; typical 3-4% for community banks
- **Operating Efficiency Ratio**: Non-interest expense divided by revenue; target <60% indicating efficient operations

### Regulatory Metrics
- **Escheatment Compliance Rate**: 100% of abandoned accounts reported to state unclaimed property offices within statutory deadlines
- **Reg E Error Resolution Timeliness**: >98% of disputes resolved within regulatory 45-day timeframe (90 days for new accounts)
- **FDIC Insurance Accuracy**: 100% of accounts coded with correct ownership type and tax ID for accurate insurance coverage calculation
- **Audit Findings**: Zero material weaknesses or significant deficiencies identified in annual SOC 1 audits or regulatory exams

---

**Document Control**
- **Version**: 1.0
- **Last Updated**: 2025-11-06
- **Regulatory References**: Regulation D (12 CFR 204), Regulation E (12 CFR 1005), Regulation DD (12 CFR 1030), FDIC Part 330
- **Review Cycle**: Quarterly
