# PASTA Methodology: Stages 4-7 - Threat Analysis to Risk Management

## Entity Type
THREAT_MODEL, RISK_ANALYSIS, ATTACK_SIMULATION

## Overview
PASTA Stages 4-7 focus on threat identification, vulnerability analysis, attack modeling, and risk/impact quantification for informed security decision-making.

## Stage 4: Threat Analysis (250+ threat scenarios)

### Web Application Threats by Asset

#### Threat Scenario: SQL Injection Against Customer Database
- **Asset**: Customer database (PII, credentials)
- **Threat Actor**: External attacker, opportunistic
- **Attack Method**: SQL injection via web form
- **STRIDE**: Information Disclosure + Tampering
- **Attack Vector**: Unsanitized input in search functionality
- **Preconditions**: Public-facing search endpoint, vulnerable parameter
- **Impact**: Customer PII breach, credential theft, data modification
- **Likelihood**: High (automated scanning, known vulnerability class)
- **Business Context**: Data breach notification costs, regulatory fines (GDPR €20M or 4% revenue)
- **PASTA Stage 1 Link**: Violates "Protect customer PII" business objective
- **Existing Controls**: WAF (partial), input validation (incomplete)
- **Control Gaps**: No parameterized queries, insufficient testing

#### Threat Scenario: Authentication Bypass via JWT None Algorithm
- **Asset**: Authentication system, user accounts
- **Threat Actor**: External attacker, skilled
- **Attack Method**: JWT algorithm confusion attack
- **STRIDE**: Spoofing + Elevation of Privilege
- **Attack Vector**: Manipulate JWT to use "none" algorithm
- **Preconditions**: JWT library vulnerability, weak validation
- **Impact**: Account takeover, unauthorized access to any account
- **Likelihood**: Medium (requires specific vulnerability)
- **Business Context**: Account takeover avg cost $12,000, reputation damage
- **PASTA Stage 1 Link**: Violates "Secure authentication" objective
- **Existing Controls**: JWT authentication (flawed implementation)
- **Control Gaps**: Accept "none" algorithm, no signature verification fallback

### ICS/SCADA Threats by Process

#### Threat Scenario: PLC Logic Tampering via Engineering Workstation Compromise
- **Asset**: PLC controlling water chemical dosing, safety-critical process
- **Threat Actor**: Nation-state, disgruntled insider
- **Attack Method**: Compromise engineering workstation, upload malicious logic
- **STRIDE**: Tampering + Elevation of Privilege
- **Attack Vector**: Spear phishing engineer, exploit workstation vulnerability
- **Preconditions**: Network access to engineering station, weak authentication to PLC
- **Impact**: Incorrect chemical dosing, public health hazard, environmental damage
- **Likelihood**: Low (targeted attack) but High Impact (safety-critical)
- **Business Context**: Public health crisis, regulatory shutdown, criminal liability
- **PASTA Stage 1 Link**: Violates "Public health protection" primary objective
- **IEC 62443**: SL 3-4 required, FR 3 (System Integrity) violation
- **Existing Controls**: Antivirus on workstation, firewall between Level 3/2
- **Control Gaps**: No code signing, weak PLC authentication, no change detection

#### Threat Scenario: SCADA Network Flooding DoS
- **Asset**: Industrial network bandwidth, SCADA server availability
- **Threat Actor**: External attacker, hacktivist
- **Attack Method**: Flood industrial network with scan/attack traffic
- **STRIDE**: Denial of Service
- **Attack Vector**: Internet-exposed HMI or VPN, network flooding
- **Preconditions**: Inadequate network segmentation, no rate limiting
- **Impact**: Lost visibility and control, process disruption, safety hazard
- **Likelihood**: Medium (attackers probing ICS networks)
- **Business Context**: Production downtime $50K/hour, potential safety incident
- **PASTA Stage 1 Link**: Violates "Operational availability" objective
- **IEC 62443**: FR 7 (Resource Availability), SR 7.1 (DoS Protection)
- **Existing Controls**: Firewall (minimal rules)
- **Control Gaps**: No IDS/IPS, insufficient segmentation, no traffic prioritization

### Cloud Infrastructure Threats

#### Threat Scenario: IAM Privilege Escalation via iam:PassRole
- **Asset**: AWS account with production workloads
- **Threat Actor**: Compromised developer account, external attacker
- **Attack Method**: Use iam:PassRole to escalate to AdministratorAccess
- **STRIDE**: Elevation of Privilege
- **Attack Vector**: Overly permissive IAM policy allows passing privileged role
- **Preconditions**: Developer compromised (phishing, leaked key), iam:PassRole permission
- **Impact**: Full AWS account compromise, data exfiltration, resource abuse
- **Likelihood**: Medium (common IAM misconfiguration)
- **Business Context**: Multi-tenant SaaS breach affecting all customers, $200/record
- **PASTA Stage 1 Link**: Violates "Tenant isolation" objective
- **Existing Controls**: IAM policies, CloudTrail logging
- **Control Gaps**: Overly permissive policies, no permission boundaries, insufficient monitoring

#### Threat Scenario: S3 Bucket Public Exposure
- **Asset**: S3 buckets containing customer data, application secrets
- **Threat Actor**: External attacker, automated scanning
- **Attack Method**: Discover publicly accessible S3 buckets
- **STRIDE**: Information Disclosure
- **Attack Vector**: Misconfigured bucket ACLs or bucket policy
- **Preconditions**: Public read permission set on bucket
- **Impact**: Customer PII/data breach, secret exposure, compliance violation
- **Likelihood**: Medium (common misconfiguration, automated discovery)
- **Business Context**: GDPR breach notification, regulatory fines, reputation
- **PASTA Stage 1 Link**: Violates "Data confidentiality" objective
- **Existing Controls**: IAM policies (not applied to bucket)
- **Control Gaps**: No bucket policy enforcement, no automated scanning, default-public

### Mobile Application Threats

#### Threat Scenario: Insecure Data Storage on Mobile Device
- **Asset**: Mobile banking app, stored credentials and transaction history
- **Threat Actor**: Opportunistic attacker with physical device access
- **Attack Method**: Extract app data from rooted/jailbroken device or backup
- **STRIDE**: Information Disclosure
- **Attack Vector**: Unencrypted local storage, insecure keychain usage
- **Preconditions**: Device loss/theft, app stores sensitive data locally
- **Impact**: Credential theft, account takeover, transaction exposure
- **Likelihood**: Medium (device loss common, data extraction easy if unencrypted)
- **Business Context**: Account takeover, regulatory breach notification
- **PASTA Stage 1 Link**: Violates "Customer account security" objective
- **Existing Controls**: Device passcode (user-controlled), app binary obfuscation
- **Control Gaps**: No encryption at rest, sensitive data unnecessarily cached

#### Threat Scenario: Man-in-the-Middle via Certificate Validation Bypass
- **Asset**: Mobile app API communication, session tokens
- **Threat Actor**: External attacker on same network (café Wi-Fi)
- **Attack Method**: MITM with self-signed certificate, app accepts invalid cert
- **STRIDE**: Information Disclosure + Tampering
- **Attack Vector**: Weak TLS certificate validation in mobile app
- **Preconditions**: User on untrusted network, app bypass cert validation
- **Impact**: Session hijacking, credential theft, transaction manipulation
- **Likelihood**: Medium (public Wi-Fi common, cert pinning often missing)
- **Business Context**: Account takeover, fraudulent transactions
- **PASTA Stage 1 Link**: Violates "Secure communication" objective
- **Existing Controls**: HTTPS communication (improperly validated)
- **Control Gaps**: No certificate pinning, accepts self-signed certs in debug/prod

## Stage 5: Vulnerability and Weakness Analysis (300+ vulnerability patterns)

### Code-Level Vulnerabilities

#### Vulnerability: Buffer Overflow in C/C++ Application
- **CWE**: CWE-120 (Buffer Copy without Checking Size of Input)
- **CAPEC**: CAPEC-100 (Overflow Buffers)
- **Vulnerability Description**: strcpy() used without bounds checking
- **Affected Component**: Native library called from web service
- **STRIDE Threats Enabled**: Elevation of Privilege, Tampering, DoS
- **Exploitability**: High (well-known exploitation techniques)
- **CVSS Base Score**: 9.8 (Critical) - Network exploitable, no authentication required
- **CVSS Vector**: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
- **Detection Method**: SAST tools (Coverity, Fortify), fuzzing, code review
- **Mitigation**: Use safe functions (strncpy, strlcpy), bounds checking, ASLR, DEP
- **NIST Controls**: SI-16 (Memory Protection), SI-10 (Input Validation)

#### Vulnerability: SQL Injection in ORM-Generated Query
- **CWE**: CWE-89 (SQL Injection)
- **CAPEC**: CAPEC-66 (SQL Injection)
- **Vulnerability Description**: Dynamic ORM query building with unsanitized input
- **Affected Component**: User search API endpoint
- **STRIDE Threats Enabled**: Information Disclosure, Tampering, Elevation of Privilege
- **Exploitability**: High (automated tools, low skill)
- **CVSS Base Score**: 9.1 (Critical)
- **CVSS Vector**: CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N
- **Detection Method**: DAST (SQLMap), code review, WAF logs
- **Mitigation**: Parameterized queries, ORM safe methods, input validation, least privilege DB account
- **NIST Controls**: SI-10, AC-6 (Least Privilege)

### Configuration Vulnerabilities

#### Vulnerability: Kubernetes Pod Running as Root
- **CWE**: CWE-250 (Execution with Unnecessary Privileges)
- **Affected Component**: Microservice containers in production cluster
- **STRIDE Threats Enabled**: Elevation of Privilege, Container Escape
- **Exploitability**: Medium (requires initial container compromise)
- **CVSS Base Score**: 7.5 (High)
- **CVSS Vector**: CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L
- **Detection Method**: Kubernetes security audit, admission controller policies
- **Mitigation**: SecurityContext runAsNonRoot, PodSecurityPolicy/Pod Security Standards
- **NIST Controls**: AC-6, CM-6 (Configuration Settings)
- **IEC 62443**: SR 2.1 (Authorization Enforcement)

#### Vulnerability: Unencrypted S3 Bucket
- **CWE**: CWE-311 (Missing Encryption of Sensitive Data)
- **Affected Component**: S3 buckets storing customer data
- **STRIDE Threats Enabled**: Information Disclosure (if accessed)
- **Exploitability**: Low (requires bucket access) but High Impact
- **CVSS Base Score**: 6.5 (Medium) - depends on access controls
- **Detection Method**: AWS Config rules, Prowler, manual audit
- **Mitigation**: Enable default encryption (AES-256 or KMS), bucket policies
- **NIST Controls**: SC-28 (Protection of Information at Rest)

### Dependency Vulnerabilities

#### Vulnerability: Log4Shell (CVE-2021-44228) in Log4j Dependency
- **CVE**: CVE-2021-44228
- **CWE**: CWE-502 (Deserialization of Untrusted Data)
- **CAPEC**: CAPEC-586 (Object Injection)
- **Vulnerability Description**: JNDI injection in log message processing
- **Affected Component**: Java applications using Log4j 2.0-2.14.1
- **STRIDE Threats Enabled**: Elevation of Privilege, Remote Code Execution
- **Exploitability**: Critical (internet-wide exploitation)
- **CVSS Base Score**: 10.0 (Critical)
- **CVSS Vector**: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H
- **Detection Method**: SCA tools (Snyk, OWASP Dependency-Check), SBOM analysis
- **Mitigation**: Upgrade to Log4j 2.17.1+, disable JNDI, WAF rules, network segmentation
- **NIST Controls**: RA-5 (Vulnerability Scanning), SI-2 (Flaw Remediation)

#### Vulnerability: Prototype Pollution in npm Package
- **CWE**: CWE-1321 (Prototype Pollution)
- **Affected Component**: Node.js application dependencies
- **STRIDE Threats Enabled**: Elevation of Privilege, DoS
- **Exploitability**: Medium (requires vulnerable code path)
- **CVSS Base Score**: 7.3 (High)
- **Detection Method**: npm audit, Snyk, Dependabot alerts
- **Mitigation**: Update to patched version, Object.freeze(Object.prototype), input validation
- **NIST Controls**: SA-11 (Developer Security Testing), SI-2

### ICS-Specific Vulnerabilities

#### Vulnerability: Hardcoded Credentials in PLC Firmware
- **CWE**: CWE-798 (Use of Hard-coded Credentials)
- **Affected Component**: Industrial PLC firmware
- **STRIDE Threats Enabled**: Elevation of Privilege, Spoofing
- **Exploitability**: High (publicly documented default credentials)
- **CVSS Base Score**: 9.8 (Critical)
- **CVSS Vector**: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
- **Detection Method**: Firmware analysis, device configuration review
- **Mitigation**: Change default credentials (if possible), network segmentation, authentication at network level
- **IEC 62443**: SR 1.5 (Authenticator Management), FR 1
- **Note**: May not be patchable; compensating controls required

#### Vulnerability: Unauthenticated Modbus/TCP Protocol
- **CWE**: CWE-306 (Missing Authentication for Critical Function)
- **Affected Component**: Modbus/TCP communication to PLCs
- **STRIDE Threats Enabled**: Elevation of Privilege, Tampering, Spoofing
- **Exploitability**: High (if network access achieved)
- **CVSS Base Score**: 8.8 (High) in OT context
- **Detection Method**: Protocol analysis, ICS security assessment
- **Mitigation**: Network segmentation (primary), TLS wrapper, protocol gateway with authentication
- **IEC 62443**: FR 1 (Identification/Authentication), SR 3.1 (Communication Integrity)
- **Note**: Protocol limitation; requires architectural mitigation

## Stage 6: Attack Modeling (200+ attack scenarios)

### Attack Tree: Web Application Account Takeover

#### Attack Goal: Gain Unauthorized Access to User Account

**Path 1: Credential Compromise**
- **1.1 Phishing Attack**
  - Craft convincing phishing email
  - Host fake login page
  - Harvest credentials
  - Success Probability: 30% (user training dependent)
  - CAPEC-98 (Phishing)

- **1.2 Credential Stuffing**
  - Obtain leaked credentials from breach
  - Automate login attempts
  - Bypass rate limiting (distributed IPs)
  - Success Probability: 15% (password reuse)
  - CAPEC-600 (Credential Stuffing)

**Path 2: Session Hijacking**
- **2.1 XSS to Steal Session Token**
  - Find XSS vulnerability
  - Inject JavaScript to steal cookie
  - Send token to attacker server
  - Use token to impersonate user
  - Success Probability: 20% (if XSS exists)
  - CAPEC-63 (Cross-Site Scripting)

- **2.2 Man-in-the-Middle**
  - Position on network (public Wi-Fi)
  - Intercept HTTP traffic (if not HTTPS)
  - Extract session cookie
  - Success Probability: 5% (HTTPS adoption high)
  - CAPEC-94 (MITM)

**Path 3: Authentication Bypass**
- **3.1 SQL Injection on Login**
  - Find SQL injection in auth query
  - Bypass authentication logic (OR 1=1)
  - Success Probability: 10% (if vulnerability exists)
  - CAPEC-66 (SQL Injection)

- **3.2 JWT Algorithm Confusion**
  - Modify JWT to use "none" algorithm
  - Remove signature
  - Success Probability: 5% (specific vulnerability)
  - CAPEC-463 (Padding Oracle)

**Attack Tree Analysis**:
- Most Likely Path: Phishing (30% × 100% = 30%)
- Highest Impact Path: SQL Injection (full database access)
- Easiest Path: Credential Stuffing (automated, low skill)
- Mitigation Priority: MFA blocks paths 1.1, 1.2, 2.1, 2.2

### Attack Scenario: ICS Ransomware Attack Chain

#### Phase 1: Initial Access
- **Vector**: Spear phishing email to maintenance engineer
- **Payload**: Weaponized PDF exploiting Adobe Reader vulnerability
- **Action**: Download and execute initial malware
- **MITRE ATT&CK**: T1566.001 (Phishing: Spearphishing Attachment)

#### Phase 2: Execution and Persistence
- **Action**: Malware establishes persistence (registry run key)
- **Lateral Movement Prep**: Scan network for ICS assets
- **Credential Harvest**: Mimikatz to extract domain credentials
- **MITRE ATT&CK**: T1547.001 (Boot/Logon: Registry Run Keys), T1003 (Credential Dumping)

#### Phase 3: Lateral Movement to OT Network
- **Action**: Use harvested credentials to access engineering workstation
- **Network Traversal**: Leverage trust relationship Level 3→Level 2
- **Discovery**: Map SCADA network, identify critical PLCs
- **MITRE ATT&CK**: T1021.001 (Remote Desktop Protocol), T1046 (Network Service Scanning)

#### Phase 4: Impact on ICS
- **Action**: Deploy ransomware to SCADA servers and HMIs
- **Backup Destruction**: Delete backups and recovery points
- **PLC Logic Corruption**: Overwrite PLC programs (if possible)
- **Ransom Demand**: $5 million in cryptocurrency
- **MITRE ATT&CK**: T1486 (Data Encrypted for Impact), T1490 (Inhibit System Recovery)

#### Phase 5: Safety Impact
- **Immediate**: Loss of visibility and control over industrial process
- **Operational**: Manual operation required, reduced capacity
- **Safety**: Potential process upsets if automatic safety systems unavailable
- **Business**: Production downtime, ransom decision, recovery costs

**Attack Simulation Results**:
- Time to Initial Access: Hours (phishing response time)
- Time to Lateral Movement: 1-3 days (reconnaissance, credential theft)
- Time to ICS Impact: Hours after OT access
- Total Attack Duration: 3-7 days from initial phishing to ransomware deployment

**Detection Opportunities**:
- Email security (phishing detection)
- EDR on workstations (malware execution, Mimikatz)
- Network monitoring (unusual RDP, OT network scanning)
- ICS IDS (unauthorized PLC access, logic changes)
- Backup integrity monitoring

### Attack Scenario: Cloud Account Takeover and Data Exfiltration

#### Step 1: Compromised Developer Credentials
- **Method**: GitHub commit with AWS access key
- **Discovery**: Automated bot scanning public repos
- **Timeframe**: Minutes after commit
- **CAPEC-191 (Read Sensitive Constants Within an Executable)

#### Step 2: Reconnaissance
- **Action**: aws sts get-caller-identity (identify account)
- **Action**: aws iam list-users, list-roles (map IAM)
- **Action**: aws s3 ls (enumerate buckets)
- **Timeframe**: 5-10 minutes
- **MITRE ATT&CK**: T1526 (Cloud Service Discovery)

#### Step 3: Privilege Escalation
- **Method**: Exploit iam:PassRole permission
- **Action**: Create Lambda function with privileged role
- **Action**: Invoke function to create new access key for admin role
- **Timeframe**: 10-15 minutes
- **MITRE ATT&CK**: T1078.004 (Cloud Accounts)

#### Step 4: Data Exfiltration
- **Action**: aws s3 sync s3://customer-data ./ (download all data)
- **Volume**: 500 GB of customer PII
- **Exfiltration Channel**: Direct S3 download
- **Timeframe**: 2-4 hours (network dependent)
- **MITRE ATT&CK**: T1537 (Transfer Data to Cloud Account)

#### Step 5: Persistence and Covering Tracks
- **Action**: Create backdoor IAM user with console access
- **Action**: Attach policy directly to user (not via group)
- **Action**: Delete CloudTrail logs (if permission available)
- **MITRE ATT&CK**: T1098 (Account Manipulation)

**Total Attack Duration**: 4-6 hours from key discovery to complete exfiltration

**Detection Opportunities**:
- GitHub secret scanning (prevent key commit)
- AWS GuardDuty (unusual API calls, reconnaissance patterns)
- CloudTrail monitoring (iam:PassRole, iam:CreateAccessKey)
- VPC Flow Logs (large data transfer)
- Data exfiltration alerts (GB transferred out)

## Stage 7: Risk and Impact Analysis (150+ risk scenarios)

### Risk Scoring Framework

#### Likelihood Assessment Criteria
**Very High (5)**: Expected to occur multiple times per year, ongoing attacks observed
**High (4)**: Likely to occur at least once per year, frequent targeting
**Medium (3)**: Could occur once every 1-3 years, periodic targeting
**Low (2)**: Unlikely but possible once every 3-10 years, rare targeting
**Very Low (1)**: Extremely rare, theoretically possible

#### Impact Assessment Criteria
**Catastrophic (5)**: >$10M loss, loss of life, business closure, criminal liability
**Critical (4)**: $1-10M loss, major regulatory action, severe reputation damage
**High (3)**: $100K-1M loss, regulatory fines, significant operational disruption
**Medium (2)**: $10K-100K loss, limited business impact, minor compliance issues
**Low (1)**: <$10K loss, negligible business impact

#### Risk Matrix (Likelihood × Impact)
```
         Impact →
L        1    2    3    4    5
i   5    5   10   15   20   25
k   4    4    8   12   16   20
e   3    3    6    9   12   15
l   2    2    4    6    8   10
i   1    1    2    3    4    5
h
o
o
d
```

Risk Levels:
- 20-25: Critical (immediate action required)
- 12-19: High (priority remediation)
- 6-11: Medium (scheduled remediation)
- 3-5: Low (accept or mitigate)
- 1-2: Very Low (accept)

### Risk Scenario: Healthcare EHR SQL Injection

#### Risk Calculation
- **Likelihood**: High (4) - Automated scanning, known vulnerability class, public-facing
- **Impact**: Critical (4) - HIPAA breach, 10,000 patient records @ $429/record = $4.3M + OCR investigation
- **Risk Score**: 4 × 4 = 16 (High Risk)

**Financial Impact Breakdown**:
- Breach notification costs: $50K (letters, call center)
- HIPAA fines: $50,000 × 10,000 violations = $500K (potential)
- OCR investigation: $200K (legal, compliance)
- Credit monitoring (1 year): 10,000 × $20 = $200K
- Reputation/patient loss: $3M (estimated)
- **Total**: $3.95M

**Operational Impact**:
- Incident response: 2 weeks (limited operational capacity)
- Forensic investigation: 1 month
- System hardening and testing: 2 months
- Regulatory compliance activities: 6 months

**Mitigation ROI**:
- Remediation cost: $50K (code review, fix, testing, deployment)
- Risk reduction: 16 → 4 (Low likelihood with parameterized queries + WAF)
- Avoided loss (annual): $3.95M × 80% = $3.16M
- ROI: ($3.16M - $50K) / $50K = 6,220%

### Risk Scenario: ICS Ransomware Attack

#### Risk Calculation
- **Likelihood**: Medium (3) - Targeted attacks increasing but require sophisticated actor
- **Impact**: Catastrophic (5) - $10M+ (downtime $50K/hr × 240 hrs + ransom + recovery)
- **Risk Score**: 3 × 5 = 15 (High Risk, approaching Critical)

**Financial Impact Breakdown**:
- Production downtime: 10 days × 24 hours × $50K/hr = $12M
- Ransom payment: $5M (decision dependent)
- Incident response: $500K (forensics, consultants)
- System recovery/rebuild: $2M (clean slate rebuild)
- Regulatory fines (if safety incident): $1M+
- **Total**: $15.5M - $20.5M (ransom dependent)

**Safety Impact**:
- Loss of automated safety systems
- Manual operation increases incident probability
- Potential environmental release
- Worker safety concerns
- Public health risk (water treatment scenario)

**Reputational/Strategic Impact**:
- Loss of customer confidence
- Regulatory scrutiny intensifies
- Competitor advantage
- Insurance rate increases
- Possible facility shutdown order

**Mitigation Strategy (Defense in Depth)**:
- Layer 1: Email security + training ($100K/year) - Reduce likelihood to Low (2)
- Layer 2: Network segmentation ($500K one-time) - Limit lateral movement
- Layer 3: ICS IDS/IPS ($200K + $50K/year) - Early detection
- Layer 4: Offline backups ($100K setup + $30K/year) - Faster recovery
- Layer 5: Incident response plan ($50K development) - Reduce recovery time

**Post-Mitigation Risk**:
- Likelihood: Low (2) - Email security and segmentation hinder attack
- Impact: Critical (4) - Backups reduce downtime: 3 days vs 10 days = $3.6M vs $12M
- Risk Score: 2 × 4 = 8 (Medium Risk)
- Mitigation Cost: $950K + $180K/year
- Avoided Loss: $15M - $3.6M = $11.4M
- ROI (3-year): ($11.4M × 3 - $1.49M) / $1.49M = 2,196%

### Risk Scenario: Cloud Data Breach via S3 Misconfiguration

#### Risk Calculation
- **Likelihood**: Medium (3) - Common misconfiguration, automated discovery
- **Impact**: Critical (4) - 1M customer records, GDPR €20M fine, reputation
- **Risk Score**: 3 × 4 = 12 (High Risk)

**Financial Impact Breakdown**:
- GDPR fines: €15M (negotiated from €20M max)
- US state breach notifications: $2M (varies by state)
- Credit monitoring: 1M × $15 = $15M
- Legal costs: $5M (class action defense)
- Customer churn: 10% × $50M annual revenue = $5M/year ongoing
- **Total**: $42M + ongoing revenue loss

**Compliance Impact**:
- GDPR: Art. 33 notification (72 hours), Art. 34 individual notification
- CCPA: $750 per consumer (statutory damages)
- SOC 2: Report qualification or adverse opinion
- Customer contract breaches: SLA violations, termination clauses

**Mitigation Strategy**:
- AWS Config rule: s3-bucket-public-read-prohibited (automated)
- S3 Block Public Access (account-level)
- IAM policy review and least privilege
- Automated scanning (Prowler, CloudSploit)
- Security training for developers
- Total cost: $150K setup + $50K/year

**Post-Mitigation Risk**:
- Likelihood: Very Low (1) - Automated prevention and detection
- Impact: Critical (4) - If occurs, impact unchanged
- Risk Score: 1 × 4 = 4 (Low Risk)
- Mitigation Cost: $150K + $50K/year
- Avoided Loss: $42M (one-time) + $5M/year (ongoing)
- ROI (Year 1): ($42M - $150K) / $150K = 27,900%

## Cross-Framework Integration

### STRIDE to PASTA Mapping
- **PASTA Stage 4** maps STRIDE categories to specific threats per asset
- **PASTA Stage 6** models attack chains exploiting STRIDE vulnerabilities
- **PASTA Stage 7** quantifies business impact of STRIDE threat realization

### IEC 62443 to PASTA Mapping
- **PASTA Stage 1** business objectives inform IEC 62443 Security Level determination
- **PASTA Stage 5** vulnerability analysis includes IEC 62443 requirement gaps
- **PASTA Stage 7** risk scores validate IEC 62443 SL selection adequacy

### NIST SP 800-53 to PASTA Mapping
- **PASTA Stage 4** threats map to NIST control families
- **PASTA Stage 5** vulnerability analysis identifies control implementation gaps
- **PASTA Stage 7** risk assessment drives control tailoring and prioritization

## PASTA Outputs

### Threat Report Template
```yaml
threat_id: THR-001
asset: [Asset name]
threat_actor: [Actor profile]
attack_method: [Method description]
stride_category: [STRIDE type(s)]
attack_vector: [Vector details]
business_impact: [Impact description]
likelihood: [1-5 rating]
impact: [1-5 rating]
risk_score: [Likelihood × Impact]
existing_controls: [Current mitigations]
control_gaps: [Identified gaps]
recommended_mitigations: [Prioritized list]
residual_risk: [Post-mitigation score]
```

### Risk Register Template
```yaml
risk_id: RSK-001
threat_scenario: [Scenario description]
assets_affected: [Asset list]
likelihood: [Rating and justification]
impact_financial: [$ amount]
impact_operational: [Description]
impact_regulatory: [Compliance implications]
risk_score: [Calculated score]
risk_level: [Critical/High/Medium/Low]
mitigation_plan: [Action items]
mitigation_cost: [$ amount]
residual_risk: [Post-mitigation]
risk_owner: [Responsible party]
due_date: [Remediation timeline]
```
