# PASTA Methodology: Stages 1-3 - Definition and Technical Scope

## Entity Type
THREAT_MODEL, METHODOLOGY, ATTACK_VECTOR

## Overview
PASTA (Process for Attack Simulation and Threat Analysis) is a risk-centric threat modeling methodology. Stages 1-3 focus on defining business objectives, technical scope, and application decomposition to establish the foundation for threat analysis.

## Stage 1: Define Business Objectives (100+ patterns)

### Financial Services Business Objectives

#### Pattern: Payment Processing Security Objectives
- **Business Goal**: Protect financial transactions and customer payment data
- **Security Objectives**:
  - Confidentiality of credit card data (PCI DSS compliance)
  - Transaction integrity (prevent modification in-transit)
  - Non-repudiation of transactions (audit trail)
  - Availability of payment gateway (99.99% uptime SLA)
- **Risk Tolerance**: Very Low - Breach cost $250-$500 per record
- **Compliance Requirements**: PCI DSS, GDPR, SOX, state breach notification laws
- **Business Impact of Compromise**: Regulatory fines, brand damage, customer loss, card reissue costs
- **STRIDE Mapping**: Information Disclosure (card data), Tampering (transaction), Repudiation (dispute)
- **NIST Controls**: SC-8 (Transmission Protection), AC-3 (Access Enforcement), AU-10 (Non-repudiation)

#### Pattern: Online Banking Authentication Objectives
- **Business Goal**: Secure user authentication for account access
- **Security Objectives**:
  - Strong multi-factor authentication
  - Session management security
  - Account takeover prevention
  - Fraud detection and prevention
- **Risk Tolerance**: Low - Account takeover avg cost $12,000
- **Compliance Requirements**: FFIEC guidance, GLBA, PSD2 SCA, state regulations
- **Business Impact**: Financial loss, regulatory action, reputation damage, customer trust loss
- **STRIDE Mapping**: Spoofing (identity theft), Elevation of Privilege (account takeover)
- **NIST Controls**: IA-2 (Identification/Authentication), IA-2(1) (MFA), SC-23 (Session Authenticity)

### Healthcare Business Objectives

#### Pattern: Electronic Health Record (EHR) Protection
- **Business Goal**: Protect patient medical records and PHI/ePHI
- **Security Objectives**:
  - PHI confidentiality (HIPAA Privacy Rule)
  - Data integrity for medical decisions
  - Availability for emergency access
  - Audit trail for HIPAA compliance
- **Risk Tolerance**: Very Low - HIPAA penalties up to $50,000 per violation
- **Compliance Requirements**: HIPAA Security Rule, HITECH Act, state privacy laws
- **Business Impact**: HIPAA fines, OCR investigation, malpractice liability, patient harm, reputation damage
- **STRIDE Mapping**: Information Disclosure (PHI), Tampering (medical records), Repudiation (access audit)
- **NIST Controls**: AC-3, AU-2 (Audit Events), SC-28 (Protection at Rest), IA-2(1)

#### Pattern: Medical Device Security Objectives
- **Business Goal**: Ensure safety and effectiveness of networked medical devices
- **Security Objectives**:
  - Patient safety (primary concern)
  - Device integrity and authenticity
  - Protection from unauthorized access/control
  - Continuous availability during use
- **Risk Tolerance**: Critical - Patient safety paramount, regulatory approval at risk
- **Compliance Requirements**: FDA guidance, IEC 62304, IEC 62443-4-1, MDR/IVDR
- **Business Impact**: Patient injury/death, FDA warning letters/recalls, lawsuits, market withdrawal
- **STRIDE Mapping**: Tampering (device software), Elevation of Privilege (unauthorized control), DoS (availability)
- **NIST Controls**: SI-7 (Software Integrity), IA-3 (Device Identification), SC-5 (DoS Protection)

### Critical Infrastructure / ICS Objectives

#### Pattern: Electric Grid SCADA Security Objectives
- **Business Goal**: Maintain reliable electricity generation and distribution
- **Security Objectives**:
  - Safety of personnel and public
  - Operational technology availability
  - Process integrity (prevent unauthorized control)
  - Regulatory compliance (NERC CIP)
- **Risk Tolerance**: Critical - Safety and national security implications
- **Compliance Requirements**: NERC CIP-002 through CIP-011, TSA directives
- **Business Impact**: Power outages, equipment damage, safety incidents, regulatory fines, national security
- **STRIDE Mapping**: Tampering (control commands), DoS (availability), Elevation of Privilege (unauthorized access)
- **NIST Controls**: SC-7 (Boundary Protection), AC-4 (Information Flow), SC-8, SI-4 (Monitoring)
- **IEC 62443**: SL 2-3 requirements, FR 5 (Restricted Data Flow), FR 7 (Resource Availability)

#### Pattern: Water Treatment SCADA Objectives
- **Business Goal**: Provide safe drinking water to population
- **Security Objectives**:
  - Public health protection (primary)
  - Chemical process integrity
  - Safety system availability
  - Environmental compliance
- **Risk Tolerance**: Critical - Public health and safety paramount
- **Compliance Requirements**: EPA regulations, Safe Drinking Water Act, state requirements
- **Business Impact**: Public health crisis, environmental damage, regulatory sanctions, civil/criminal liability
- **STRIDE Mapping**: Tampering (chemical dosing), DoS (treatment process), Elevation of Privilege (control system)
- **NIST Controls**: SI-4, SC-7, CP-2 (Contingency Plan), IR-4 (Incident Handling)
- **IEC 62443**: SL 3-4 requirements, SR 7.6 (Fail-safe), FR 6 (Timely Response to Events)

### E-Commerce Business Objectives

#### Pattern: Online Retail Platform Security
- **Business Goal**: Secure e-commerce transactions and customer data
- **Security Objectives**:
  - Customer PII protection
  - Payment data security (PCI DSS)
  - Transaction integrity
  - Website availability (revenue impact)
- **Risk Tolerance**: Medium - Balance security with customer experience
- **Compliance Requirements**: PCI DSS, GDPR/CCPA, FTC consumer protection
- **Business Impact**: Data breach costs, PCI fines, revenue loss during outages, reputation damage
- **STRIDE Mapping**: Information Disclosure (PII), Tampering (prices/cart), DoS (availability)
- **NIST Controls**: SC-8, AC-3, SC-5, SI-10 (Input Validation)

### Cloud SaaS Business Objectives

#### Pattern: Multi-Tenant SaaS Application Security
- **Business Goal**: Securely serve multiple customers with data isolation
- **Security Objectives**:
  - Tenant data isolation (prevent cross-tenant access)
  - Availability and scalability (SLA commitments)
  - Data confidentiality and integrity
  - Compliance for customer certifications
- **Risk Tolerance**: Low - Breach affects multiple customers simultaneously
- **Compliance Requirements**: SOC 2 Type II, ISO 27001, GDPR, CCPA, industry-specific
- **Business Impact**: Mass customer loss, certification revocation, class action lawsuits
- **STRIDE Mapping**: Elevation of Privilege (tenant isolation breach), Information Disclosure (data leakage)
- **NIST Controls**: AC-3, AC-4 (Information Flow), SC-3 (Security Function Isolation)

## Stage 2: Define Technical Scope (100+ patterns)

### Network Architecture Scoping

#### Pattern: Three-Tier Web Application Architecture
- **In Scope**:
  - Web tier (load balancers, web servers, CDN)
  - Application tier (app servers, APIs, microservices)
  - Data tier (databases, caches, object storage)
  - Supporting infrastructure (DNS, auth services, logging)
- **Out of Scope**: Corporate network, employee endpoints, development environments
- **Trust Boundaries**:
  - Internet ↔ DMZ (web tier)
  - DMZ ↔ Internal (application tier)
  - Application ↔ Data tier
  - Service ↔ Service (microservices mesh)
- **Data Flows**: HTTP/HTTPS requests, API calls, database queries, cache operations
- **Technology Stack**: Nginx, Node.js/Java, PostgreSQL, Redis, AWS/Azure/GCP
- **Attack Surface**: Web interfaces, REST/GraphQL APIs, authentication endpoints

#### Pattern: ICS/SCADA Purdue Model Scoping
- **Level 0 (In Scope)**: Physical processes, sensors, actuators
- **Level 1 (In Scope)**: PLCs, RTUs, IEDs, safety systems
- **Level 2 (In Scope)**: SCADA/DCS, HMI, historian, MES
- **Level 3 (Boundary)**: Manufacturing operations, ERP systems
- **Level 4-5 (Out of Scope)**: Enterprise IT, business planning
- **Trust Boundaries**:
  - Level 3/2 (DMZ/screened subnet between IT/OT)
  - Level 2/1 (supervisory ↔ control)
  - Level 1/0 (control ↔ field devices)
- **Conduits**: Specific network connections between zones
- **Attack Surface**: Engineering workstations, HMIs, network services, field device protocols

### Cloud Architecture Scoping

#### Pattern: AWS Multi-Tier Application
- **In Scope Components**:
  - VPC networking (subnets, security groups, NACLs)
  - Compute (EC2, ECS, Lambda)
  - Load balancing (ALB, NLB)
  - Storage (S3, EBS, EFS)
  - Database (RDS, DynamoDB)
  - IAM (users, roles, policies)
  - API Gateway
  - CloudFront CDN
- **Out of Scope**: AWS infrastructure, other customer tenants, on-premises corporate network
- **Trust Boundaries**:
  - Internet ↔ CloudFront/ALB
  - Public subnet ↔ Private subnet
  - VPC ↔ AWS services (S3, DynamoDB)
  - Account ↔ Account (cross-account access)
- **Data Classification**: Public web content, customer PII, payment data (PCI), authentication credentials
- **Shared Responsibility**: AWS responsible for infrastructure, customer for guest OS and data

### Mobile Application Scoping

#### Pattern: iOS/Android Mobile Banking App
- **In Scope**:
  - Mobile application (client-side code)
  - Backend APIs
  - Authentication services
  - Push notification system
  - Mobile device storage
  - Network communications
- **Out of Scope**: App store infrastructure, mobile OS (partially shared responsibility), carrier networks
- **Trust Boundaries**:
  - Mobile device ↔ Backend API
  - App ↔ Mobile OS
  - App ↔ Third-party SDKs
  - User ↔ App (trusted input)
- **Attack Surface**: App binary (reverse engineering), API endpoints, local storage, inter-app communication
- **Data at Rest**: Encrypted keychain/keystore, SQLite databases, shared preferences, cache

### IoT System Scoping

#### Pattern: Smart Home IoT Ecosystem
- **In Scope**:
  - IoT devices (sensors, cameras, smart locks)
  - Local gateway/hub
  - Cloud backend/control plane
  - Mobile/web management interface
  - Firmware update mechanism
- **Out of Scope**: Home Wi-Fi router (assumed trusted), ISP infrastructure, third-party integrations
- **Trust Boundaries**:
  - Device ↔ Local Network
  - Gateway ↔ Cloud
  - User ↔ Management Interface
  - Device ↔ Device (local mesh)
- **Attack Surface**: Device firmware, network protocols (Zigbee, Z-Wave, Wi-Fi), cloud APIs, update mechanism
- **Constraints**: Limited device resources, long device lifespan, patching challenges

## Stage 3: Application Decomposition (200+ patterns)

### Data Flow Diagram (DFD) Elements

#### Pattern: Web Application Authentication Flow
- **External Entity**: User (Browser)
- **Process 1**: Web Server (receives login request)
- **Process 2**: Authentication Service (validates credentials)
- **Process 3**: Session Manager (creates session token)
- **Data Store 1**: User Credentials Database
- **Data Store 2**: Session Store (Redis)
- **Data Flows**:
  1. User → Web Server: HTTP POST /login {username, password}
  2. Web Server → Auth Service: Validate credentials
  3. Auth Service → Credentials DB: Query user record
  4. Credentials DB → Auth Service: User record with hashed password
  5. Auth Service → Session Manager: Create session (user_id)
  6. Session Manager → Session Store: Store session token
  7. Session Manager → Web Server: Session token (JWT or cookie)
  8. Web Server → User: Set-Cookie or JWT in response
- **Trust Boundaries**: Internet/DMZ (1-2), DMZ/Internal (2-5), Service/Data (3-4, 5-6)

#### Pattern: Payment Processing Data Flow
- **External Entity 1**: Customer
- **External Entity 2**: Payment Gateway (Stripe/PayPal)
- **Process 1**: E-commerce Web Server
- **Process 2**: Order Processing Service
- **Process 3**: Payment Tokenization Service
- **Process 4**: PCI DSS Compliant Payment Processor
- **Data Store 1**: Order Database
- **Data Store 2**: Payment Token Store (PCI scope reduced)
- **Data Flows**:
  1. Customer → Web Server: Submit order with payment details
  2. Web Server → Tokenization Service: Tokenize credit card
  3. Tokenization Service → Payment Gateway: Create payment method
  4. Payment Gateway → Tokenization Service: Payment token
  5. Web Server → Order Service: Process order (with token, no card data)
  6. Order Service → Order DB: Store order (token reference only)
  7. Order Service → Payment Processor: Charge payment (token)
  8. Payment Processor → Payment Gateway: Process charge
- **Trust Boundaries**: External/Internal (1-2), PCI/Non-PCI (2-8)

#### Pattern: ICS SCADA Control Flow
- **External Entity**: Human Operator
- **Process 1**: HMI Workstation
- **Process 2**: SCADA Server
- **Process 3**: PLC/RTU Controller
- **Process 4**: Field Device (valve, pump, sensor)
- **Data Store 1**: Historian Database
- **Data Store 2**: PLC Logic Program
- **Data Flows**:
  1. Operator → HMI: Control command (setpoint change)
  2. HMI → SCADA Server: Command message
  3. SCADA Server → PLC: Control protocol message (Modbus, DNP3)
  4. PLC → Field Device: I/O command
  5. Field Device → PLC: Sensor reading
  6. PLC → SCADA Server: Telemetry data
  7. SCADA Server → Historian: Log telemetry
  8. SCADA Server → HMI: Display update
- **Trust Boundaries**: Corporate/OT (Level 3/2), SCADA/Control (Level 2/1), Control/Field (Level 1/0)

### Entry Points Identification

#### Pattern: Web Application Entry Points
1. **HTTP/HTTPS Endpoints**:
   - User-facing web pages (GET /*, POST /*)
   - REST API endpoints (GET/POST/PUT/DELETE /api/*)
   - GraphQL endpoint (POST /graphql)
   - WebSocket connections (ws://)
2. **Authentication Entry Points**:
   - Login form (POST /login)
   - OAuth callback (GET /auth/callback)
   - API key authentication (Header: X-API-Key)
   - JWT token validation (Header: Authorization)
3. **File Upload Endpoints**:
   - Profile picture upload (POST /api/upload/profile)
   - Document upload (POST /api/documents)
   - Bulk data import (POST /api/import/csv)
4. **External Integrations**:
   - Webhook receivers (POST /webhooks/*)
   - Third-party API callbacks
   - Payment gateway notifications
5. **Administrative Interfaces**:
   - Admin panel (/admin/*)
   - Monitoring dashboards
   - Configuration endpoints

#### Pattern: ICS Entry Points
1. **Human-Machine Interface**:
   - HMI login screen
   - Control interface
   - Configuration screens
2. **Engineering Workstation**:
   - PLC programming interface
   - Logic upload/download
   - Firmware updates
3. **Network Services**:
   - SCADA protocols (Modbus TCP port 502, DNP3 port 20000)
   - OPC UA (port 4840)
   - Proprietary protocols
4. **Remote Access**:
   - VPN connections
   - Remote desktop (RDP)
   - Vendor support access
5. **Physical Access**:
   - Field device local interfaces
   - USB ports on PLCs
   - Serial connections

### Assets and Data Classification

#### Pattern: Healthcare Application Assets
**Critical Assets**:
- Patient medical records (ePHI)
- Prescription data
- Provider credentials
- Appointment schedules
- Billing information

**Data Classification**:
- **High Sensitivity (Red)**:
  - PHI: Diagnosis, treatment, medications, lab results
  - Authentication credentials
  - SSN, insurance information
- **Medium Sensitivity (Yellow)**:
  - Appointment dates/times (without diagnosis)
  - Provider schedules
  - Facility information
- **Low Sensitivity (Green)**:
  - Public health information
  - Marketing materials
  - General contact information

**Asset Valuation**:
- ePHI records: $429 per record average breach cost (Ponemon Institute)
- System downtime: $10,000 per hour (unable to access records)
- Regulatory penalties: Up to $50,000 per HIPAA violation
- Reputation damage: Difficult to quantify, patient loss

#### Pattern: Financial Services Assets
**Critical Assets**:
- Customer account balances
- Transaction history
- Credit card/payment data
- Personal identification information
- Authentication credentials

**Data Classification**:
- **Tier 1 (Critical)**:
  - PCI data (card numbers, CVV, PINs)
  - Account credentials
  - Wire transfer details
- **Tier 2 (Sensitive)**:
  - Account balances
  - Transaction history
  - Customer PII
- **Tier 3 (Internal)**:
  - Aggregated analytics
  - Non-sensitive account metadata

**Compliance Tags**:
- PCI DSS cardholder data
- GLBA financial information
- GDPR personal data
- SOX financial records

### Component Inventory

#### Pattern: Microservices Architecture Components
**Frontend Components**:
- React SPA (client-side rendering)
- Nginx reverse proxy
- CDN (CloudFront/Cloudflare)

**API Gateway**:
- Kong/AWS API Gateway
- Rate limiting
- Authentication middleware

**Microservices**:
- User Service (authentication, profile)
- Order Service (order processing)
- Payment Service (payment processing)
- Inventory Service (product catalog)
- Notification Service (email, SMS)

**Data Stores**:
- PostgreSQL (user data, orders)
- MongoDB (product catalog)
- Redis (caching, sessions)
- Elasticsearch (search)
- S3 (file storage)

**Infrastructure**:
- Kubernetes cluster
- Service mesh (Istio)
- Message queue (RabbitMQ/Kafka)
- Logging (ELK stack)
- Monitoring (Prometheus/Grafana)

#### Pattern: ICS/SCADA Components
**Supervisory Layer (Level 2)**:
- SCADA server software
- HMI workstations (Windows)
- Historian database
- Engineering workstation

**Control Layer (Level 1)**:
- PLCs (Siemens S7, Allen-Bradley, etc.)
- RTUs (remote terminal units)
- Safety instrumented systems (SIS)
- DCS (distributed control system)

**Field Layer (Level 0)**:
- Sensors (temperature, pressure, flow)
- Actuators (valves, pumps, motors)
- Variable frequency drives (VFDs)
- Intelligent electronic devices (IEDs)

**Network Infrastructure**:
- Industrial Ethernet switches
- Firewalls (Level 3/2 boundary)
- Serial communication networks
- Wireless sensors/gateways

### Technology Stack Documentation

#### Pattern: LAMP Stack Application
**Operating System**: Ubuntu 20.04 LTS
**Web Server**: Apache 2.4.41 with mod_security WAF
**Application**: PHP 7.4 with Laravel framework
**Database**: MySQL 8.0 with InnoDB engine
**Caching**: Memcached 1.6
**SSL/TLS**: Let's Encrypt certificates, TLS 1.2/1.3
**Dependencies**: Composer packages (see composer.lock)
**Infrastructure**: AWS EC2 t3.medium instances, RDS for MySQL

**Security Features**:
- mod_security WAF with OWASP Core Rule Set
- PHP security extensions (Suhosin)
- Database stored procedures (parameterized queries)
- XSS protection headers
- CSRF tokens in forms

#### Pattern: Containerized Microservices Stack
**Container Runtime**: Docker 20.10, Kubernetes 1.21
**Service Mesh**: Istio 1.11 (mTLS between services)
**API Gateway**: Kong 2.5 with rate limiting and authentication plugins
**Languages/Frameworks**:
- Node.js 16 (Express.js) for user service
- Java 11 (Spring Boot) for order service
- Python 3.9 (Flask) for payment service
- Go 1.17 for inventory service

**Data Stores**:
- PostgreSQL 13 (user, order data)
- MongoDB 5.0 (product catalog)
- Redis 6.2 (sessions, cache)

**Security**:
- Container image scanning (Trivy)
- Pod Security Policies
- Network Policies (Calico)
- Secret management (Vault)
- mTLS service-to-service communication

## Cross-Framework Integration

### Alignment with STRIDE
- **Business Objectives** inform which STRIDE categories are highest priority
- **Technical Scope** defines trust boundaries for STRIDE analysis
- **Application Decomposition** creates DFDs for systematic STRIDE per element

### Alignment with IEC 62443
- **Business Objectives** drive Security Level (SL) determination
- **Technical Scope** defines zones and conduits
- **Application Decomposition** identifies components for Foundational Requirements

### Alignment with NIST SP 800-53
- **Business Objectives** inform control tailoring and priority
- **Technical Scope** defines system boundary for assessment
- **Asset Classification** drives protection requirements and control selection

## Documentation Templates

### Business Objective Template
```yaml
objective_id: BO-001
business_goal: [High-level business outcome]
security_objectives:
  - confidentiality: [CIA requirement]
  - integrity: [CIA requirement]
  - availability: [CIA requirement]
  - compliance: [Regulatory requirements]
risk_tolerance: [Critical/High/Medium/Low]
business_impact:
  financial: [Quantified cost]
  regulatory: [Fines, sanctions]
  operational: [Downtime, productivity]
  reputational: [Brand damage, customer loss]
```

### Technical Scope Template
```yaml
scope_id: TS-001
architecture: [Architecture pattern]
in_scope_components:
  - [Component list]
out_of_scope:
  - [Excluded components]
trust_boundaries:
  - boundary_1: [Description]
    security_controls: [Controls at boundary]
data_classification:
  - class: [High/Medium/Low]
    data_types: [Specific data]
attack_surface:
  - [Entry points]
technology_stack:
  - [Detailed stack]
```

### DFD Element Template
```yaml
dfd_id: DFD-001
element_type: [Process/Data Store/Data Flow/External Entity]
name: [Element name]
description: [Detailed description]
trust_level: [Trusted/Untrusted/Partially Trusted]
data_sensitivity: [High/Medium/Low]
connections:
  - from: [Source]
    to: [Destination]
    protocol: [Communication protocol]
    authentication: [Auth method]
    encryption: [Encryption yes/no]
threats: [Related threat IDs]
controls: [Mitigating controls]
```
