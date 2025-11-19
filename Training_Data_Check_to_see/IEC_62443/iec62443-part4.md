# IEC 62443-4-1: Secure Development Lifecycle Requirements

## Overview

IEC 62443-4-1 establishes requirements for the secure development lifecycle of products used in industrial automation and control systems (IACS). This standard provides comprehensive guidelines for secure software development practices, from requirements gathering through maintenance and patch management.

**Related Standards:**
- [[IEC 62443 Part 1]] - Security foundations and terminology
- [[IEC 62443 Part 2]] - Security program requirements
- [[IEC 62443 Part 3]] - System security requirements
- [[Compliance]] - Certification and assessment processes

**Development Resources:**
- [[Vulnerability Management]] - Security testing and validation
- [[Patch Management]] - Secure maintenance practices
- [[Threat Modeling Techniques]] - Security design methodologies
- [[Debugging Security]] - Secure development debugging practices

## Secure Development Lifecycle (SDLC) Phases

### Phase 1: Security Management

**Objective:** Establish security governance and management structures.

#### Security Governance Framework

**Security Roles and Responsibilities:**
```json
{
  "security_roles": {
    "chief_information_security_officer": {
      "responsibilities": [
        "security_policy_approval",
        "risk_assessment_oversight",
        "compliance_monitoring",
        "security_budget_approval",
        "executive_reporting"
      ],
      "authority_level": "executive",
      "required_competencies": [
        "security_governance",
        "risk_management",
        "regulatory_compliance",
        "strategic_planning"
      ]
    },
    "security_architect": {
      "responsibilities": [
        "security_design_review",
        "threat_modeling",
        "security_requirements_definition",
        "architecture_approval",
        "security_guidance"
      ],
      "authority_level": "technical_lead",
      "required_competencies": [
        "system_architecture",
        "threat_modeling",
        "security_design_patterns",
        "cryptography"
      ]
    },
    "security_tester": {
      "responsibilities": [
        "vulnerability_assessment",
        "penetration_testing",
        "security_test_planning",
        "test_result_analysis",
        "remediation_validation"
      ],
      "authority_level": "technical_specialist",
      "required_competencies": [
        "penetration_testing",
        "vulnerability_assessment",
        "security_testing_tools",
        "exploit_development"
      ]
    },
    "secure_development_engineer": {
      "responsibilities": [
        "secure_coding_practices",
        "code_security_review",
        "security_unit_testing",
        "static_analysis_integration",
        "security_training_delivery"
      ],
      "authority_level": "technical_contributor",
      "required_competencies": [
        "secure_coding",
        "code_review",
        "static_analysis",
        "security_awareness"
      ]
    },
    "patch_management_specialist": {
      "responsibilities": [
        "vulnerability_monitoring",
        "patch_development",
        "patch_testing",
        "patch_deployment",
        "patch_effectiveness_monitoring"
      ],
      "authority_level": "technical_specialist",
      "required_competencies": [
        "patch_management",
        "vulnerability_management",
        "system_administration",
        "change_management"
      ]
    },
    "security_auditor": {
      "responsibilities": [
        "security_audit_planning",
        "compliance_assessment",
        "audit_finding_documentation",
        "remediation_tracking",
        "audit_reporting"
      ],
      "authority_level": "independent_assessor",
      "required_competencies": [
        "security_auditing",
        "compliance_assessment",
        "regulatory_requirements",
        "reporting"
      ]
    }
  },
  "security_committee": {
    "composition": [
      "CISO",
      "security_architect",
      "development_lead",
      "operations_lead",
      "legal_compliance_officer"
    ],
    "frequency": "monthly",
    "responsibilities": [
      "security_policy_approval",
      "security_investment_decisions",
      "security_incident_review",
      "compliance_oversight"
    ]
  }
}
```

#### Security Policy Framework
**Core Security Policies:**
- **Information Security Policy:** Overall security objectives and principles
- **Access Control Policy:** Authentication and authorization requirements
- **Data Protection Policy:** Data classification and handling requirements
- **Incident Response Policy:** Security incident handling procedures
- **Change Management Policy:** Secure system change procedures
- **Third-Party Security Policy:** Vendor and supplier security requirements

#### Security Risk Management
**Risk Assessment Process:**
1. **Asset Identification:** Identify critical IACS assets and data
2. **Threat Modeling:** Identify potential threats and attack vectors
3. **Vulnerability Assessment:** Evaluate system weaknesses
4. **Impact Analysis:** Assess consequences of security incidents
5. **Risk Calculation:** Determine risk levels using quantitative methods
6. **Risk Treatment:** Select and implement risk mitigation strategies

**Risk Management Tools:**
```javascript
// Risk Assessment Calculator for IACS
class IACSRiskCalculator {
  constructor() {
    this.threatSources = {
      'insider_threat': { likelihood: 0.3, impact: 0.8 },
      'external_hacker': { likelihood: 0.2, impact: 0.9 },
      'supply_chain_attack': { likelihood: 0.1, impact: 0.95 },
      'nation_state_actor': { likelihood: 0.05, impact: 1.0 },
      'physical_intrusion': { likelihood: 0.15, impact: 0.6 },
      'malware_infection': { likelihood: 0.4, impact: 0.7 }
    };

    this.vulnerabilityFactors = {
      'unpatched_system': 0.9,
      'weak_authentication': 0.8,
      'network_exposure': 0.7,
      'insufficient_monitoring': 0.6,
      'legacy_systems': 0.8,
      'poor_configuration': 0.7
    };
  }

  calculateRisk(asset, threats, vulnerabilities) {
    const riskScores = {};

    for (const threat of threats) {
      const threatData = this.threatSources[threat.type];
      if (!threatData) continue;

      let adjustedLikelihood = threatData.likelihood;
      let adjustedImpact = threatData.impact;

      // Adjust for asset value
      adjustedImpact *= asset.criticality;

      // Adjust for vulnerabilities
      for (const vuln of vulnerabilities) {
        const vulnFactor = this.vulnerabilityFactors[vuln.type] || 0.5;
        adjustedLikelihood *= vulnFactor;
        adjustedImpact *= vulnFactor;
      }

      // Calculate risk score
      const riskScore = adjustedLikelihood * adjustedImpact;

      riskScores[threat.type] = {
        likelihood: adjustedLikelihood,
        impact: adjustedImpact,
        riskScore: riskScore,
        riskLevel: this.determineRiskLevel(riskScore)
      };
    }

    return {
      asset: asset.name,
      overallRisk: this.calculateOverallRisk(riskScores),
      threatRisks: riskScores,
      recommendations: this.generateRecommendations(riskScores)
    };
  }

  determineRiskLevel(riskScore) {
    if (riskScore >= 0.7) return 'CRITICAL';
    if (riskScore >= 0.5) return 'HIGH';
    if (riskScore >= 0.3) return 'MEDIUM';
    if (riskScore >= 0.1) return 'LOW';
    return 'VERY_LOW';
  }

  calculateOverallRisk(threatRisks) {
    const scores = Object.values(threatRisks).map(r => r.riskScore);
    const maxRisk = Math.max(...scores);
    const avgRisk = scores.reduce((a, b) => a + b, 0) / scores.length;

    return {
      maxRisk: maxRisk,
      averageRisk: avgRisk,
      overallLevel: this.determineRiskLevel(Math.max(maxRisk, avgRisk * 0.8))
    };
  }

  generateRecommendations(riskScores) {
    const recommendations = [];

    for (const [threatType, risk] of Object.entries(riskScores)) {
      if (risk.riskLevel === 'CRITICAL' || risk.riskLevel === 'HIGH') {
        recommendations.push({
          threat: threatType,
          priority: 'HIGH',
          actions: this.getMitigationActions(threatType)
        });
      }
    }

    return recommendations.sort((a, b) => {
      const priorityOrder = { 'CRITICAL': 3, 'HIGH': 2, 'MEDIUM': 1 };
      return priorityOrder[b.priority] - priorityOrder[a.priority];
    });
  }

  getMitigationActions(threatType) {
    const actions = {
      'insider_threat': [
        'Implement role-based access control',
        'Conduct background checks',
        'Monitor privileged user activities',
        'Implement data loss prevention'
      ],
      'external_hacker': [
        'Deploy network intrusion detection',
        'Implement multi-factor authentication',
        'Regular vulnerability scanning',
        'Web application firewall'
      ],
      'supply_chain_attack': [
        'Third-party security assessments',
        'Software supply chain security',
        'Binary integrity verification',
        'Vendor security monitoring'
      ],
      'nation_state_actor': [
        'Advanced threat detection',
        'Zero trust architecture',
        'Security information sharing',
        'Incident response planning'
      ],
      'physical_intrusion': [
        'Physical access controls',
        'Video surveillance',
        'Intrusion detection systems',
        'Security personnel training'
      ],
      'malware_infection': [
        'Endpoint protection platforms',
        'Email security gateways',
        'Regular security awareness training',
        'Automated malware scanning'
      ]
    };

    return actions[threatType] || ['Conduct security assessment', 'Implement appropriate controls'];
  }
}

// Example Risk Assessment
const riskCalculator = new IACSRiskCalculator();

const asset = {
  name: 'SCADA Control System',
  criticality: 0.9,
  value: 1000000
};

const threats = [
  { type: 'external_hacker' },
  { type: 'insider_threat' },
  { type: 'malware_infection' }
];

const vulnerabilities = [
  { type: 'unpatched_system' },
  { type: 'weak_authentication' },
  { type: 'network_exposure' }
];

const riskAssessment = riskCalculator.calculateRisk(asset, threats, vulnerabilities);
console.log('Risk Assessment:', JSON.stringify(riskAssessment, null, 2));
```

### Phase 2: Security Requirements

**Objective:** Define security requirements for the IACS product.

#### Security Functional Requirements
**Authentication Requirements:**
- **REQ-AUTH-001:** System shall support multi-factor authentication
- **REQ-AUTH-002:** System shall enforce password complexity requirements
- **REQ-AUTH-003:** System shall implement account lockout after failed attempts
- **REQ-AUTH-004:** System shall support certificate-based authentication
- **REQ-AUTH-005:** System shall log all authentication events

**Authorization Requirements:**
- **REQ-AUTHZ-001:** System shall implement role-based access control
- **REQ-AUTHZ-002:** System shall enforce least privilege principle
- **REQ-AUTHZ-003:** System shall support attribute-based access control
- **REQ-AUTHZ-004:** System shall provide audit logging of authorization decisions
- **REQ-AUTHZ-005:** System shall support privilege escalation controls

**Data Protection Requirements:**
- **REQ-DATA-001:** System shall encrypt sensitive data at rest
- **REQ-DATA-002:** System shall encrypt data in transit using TLS 1.3
- **REQ-DATA-003:** System shall implement data classification schemes
- **REQ-DATA-004:** System shall support data integrity verification
- **REQ-DATA-005:** System shall implement secure key management

#### Security Assurance Requirements
**Testing Requirements:**
- **REQ-ASSUR-001:** System shall undergo penetration testing
- **REQ-ASSUR-002:** System shall pass vulnerability scanning
- **REQ-ASSUR-003:** System shall achieve target security level certification
- **REQ-ASSUR-004:** System shall maintain security test coverage > 95%
- **REQ-ASSUR-005:** System shall implement automated security testing

**Documentation Requirements:**
- **REQ-DOCS-001:** System shall provide security architecture documentation
- **REQ-DOCS-002:** System shall document threat models
- **REQ-DOCS-003:** System shall provide secure configuration guides
- **REQ-DOCS-004:** System shall document security limitations
- **REQ-DOCS-005:** System shall provide security update procedures

#### Threat Modeling Requirements
**STRIDE Threat Modeling:**
```javascript
// STRIDE Threat Modeling Implementation
class STRIDEThreatModeler {
  constructor() {
    this.strideCategories = {
      'Spoofing': {
        description: 'Impersonating something or someone else',
        examples: ['Identity spoofing', 'Session hijacking', 'Man-in-the-middle'],
        mitigations: ['Authentication', 'Digital signatures', 'Certificates']
      },
      'Tampering': {
        description: 'Modifying data or code maliciously',
        examples: ['Data modification', 'Code injection', 'Parameter manipulation'],
        mitigations: ['Integrity checks', 'Hashing', 'Digital signatures']
      },
      'Repudiation': {
        description: 'Denying an action occurred',
        examples: ['Log manipulation', 'Transaction denial', 'Action repudiation'],
        mitigations: ['Secure logging', 'Digital signatures', 'Timestamps']
      },
      'Information Disclosure': {
        description: 'Exposing information to unauthorized parties',
        examples: ['Data leakage', 'Privacy violation', 'Information exposure'],
        mitigations: ['Encryption', 'Access controls', 'Data classification']
      },
      'Denial of Service': {
        description: 'Making a system unavailable',
        examples: ['Resource exhaustion', 'Network flooding', 'Service disruption'],
        mitigations: ['Rate limiting', 'Resource management', 'Redundancy']
      },
      'Elevation of Privilege': {
        description: 'Gaining higher privileges than authorized',
        examples: ['Privilege escalation', 'Role manipulation', 'Authorization bypass'],
        mitigations: ['Access controls', 'Least privilege', 'Input validation']
      }
    };
  }

  analyzeSystem(systemComponents, dataFlows, trustBoundaries) {
    const threats = [];

    // Analyze each component
    for (const component of systemComponents) {
      const componentThreats = this.analyzeComponent(component, systemComponents, dataFlows, trustBoundaries);
      threats.push(...componentThreats);
    }

    // Analyze data flows
    for (const flow of dataFlows) {
      const flowThreats = this.analyzeDataFlow(flow, trustBoundaries);
      threats.push(...flowThreats);
    }

    return {
      system: systemComponents[0]?.systemName || 'Unknown System',
      threats: threats,
      riskAssessment: this.assessThreatRisk(threats),
      mitigations: this.generateMitigations(threats)
    };
  }

  analyzeComponent(component, allComponents, dataFlows, trustBoundaries) {
    const threats = [];

    for (const [category, details] of Object.entries(this.strideCategories)) {
      // Check for applicable threats based on component type and interactions
      const applicableThreats = this.findApplicableThreats(component, category, allComponents, dataFlows, trustBoundaries);

      for (const threat of applicableThreats) {
        threats.push({
          id: this.generateThreatId(),
          category: category,
          component: component.name,
          description: threat.description,
          impact: threat.impact,
          likelihood: threat.likelihood,
          riskLevel: this.calculateRiskLevel(threat.impact, threat.likelihood),
          examples: details.examples,
          mitigations: details.mitigations
        });
      }
    }

    return threats;
  }

  findApplicableThreats(component, category, allComponents, dataFlows, trustBoundaries) {
    const threats = [];

    switch (category) {
      case 'Spoofing':
        if (component.type === 'web_service' || component.type === 'api') {
          threats.push({
            description: `Attacker could spoof ${component.name} identity`,
            impact: 'HIGH',
            likelihood: 'MEDIUM'
          });
        }
        break;

      case 'Tampering':
        if (component.handlesData || component.type === 'database') {
          threats.push({
            description: `Data in ${component.name} could be tampered with`,
            impact: 'HIGH',
            likelihood: 'MEDIUM'
          });
        }
        break;

      case 'Repudiation':
        if (component.logsActions) {
          threats.push({
            description: `Actions in ${component.name} could be repudiated`,
            impact: 'MEDIUM',
            likelihood: 'LOW'
          });
        }
        break;

      case 'Information Disclosure':
        const relatedFlows = dataFlows.filter(flow =>
          flow.source === component.name || flow.target === component.name
        );

        if (relatedFlows.some(flow => flow.dataType === 'sensitive')) {
          threats.push({
            description: `Sensitive data flowing through ${component.name} could be disclosed`,
            impact: 'CRITICAL',
            likelihood: 'MEDIUM'
          });
        }
        break;

      case 'Denial of Service':
        if (component.type === 'web_service' || component.type === 'network_device') {
          threats.push({
            description: `${component.name} could be made unavailable through DoS attack`,
            impact: 'HIGH',
            likelihood: 'HIGH'
          });
        }
        break;

      case 'Elevation of Privilege':
        if (component.hasPrivileges || component.type === 'authentication_service') {
          threats.push({
            description: `Attacker could elevate privileges in ${component.name}`,
            impact: 'CRITICAL',
            likelihood: 'MEDIUM'
          });
        }
        break;
    }

    return threats;
  }

  analyzeDataFlow(flow, trustBoundaries) {
    const threats = [];

    // Check if flow crosses trust boundaries
    const crossesBoundary = trustBoundaries.some(boundary =>
      (boundary.includes(flow.source) && !boundary.includes(flow.target)) ||
      (!boundary.includes(flow.source) && boundary.includes(flow.target))
    );

    if (crossesBoundary && flow.dataType === 'sensitive') {
      threats.push({
        id: this.generateThreatId(),
        category: 'Information Disclosure',
        component: `${flow.source} -> ${flow.target}`,
        description: `Sensitive data flow from ${flow.source} to ${flow.target} crosses trust boundary`,
        impact: 'HIGH',
        likelihood: 'MEDIUM',
        riskLevel: 'HIGH',
        examples: ['Data interception', 'Man-in-the-middle attack'],
        mitigations: ['Encryption', 'Secure channels', 'Access controls']
      });
    }

    return threats;
  }

  calculateRiskLevel(impact, likelihood) {
    const impactScore = { 'LOW': 1, 'MEDIUM': 2, 'HIGH': 3, 'CRITICAL': 4 }[impact] || 2;
    const likelihoodScore = { 'LOW': 1, 'MEDIUM': 2, 'HIGH': 3 }[likelihood] || 2;

    const riskScore = impactScore * likelihoodScore;

    if (riskScore >= 8) return 'CRITICAL';
    if (riskScore >= 5) return 'HIGH';
    if (riskScore >= 3) return 'MEDIUM';
    return 'LOW';
  }

  assessThreatRisk(threats) {
    const riskLevels = threats.map(t => t.riskLevel);
    const criticalCount = riskLevels.filter(r => r === 'CRITICAL').length;
    const highCount = riskLevels.filter(r => r === 'HIGH').length;

    let overallRisk = 'LOW';
    if (criticalCount > 0) overallRisk = 'CRITICAL';
    else if (highCount > 2) overallRisk = 'HIGH';
    else if (highCount > 0) overallRisk = 'MEDIUM';

    return {
      overallRisk: overallRisk,
      threatCounts: {
        total: threats.length,
        critical: criticalCount,
        high: highCount,
        medium: riskLevels.filter(r => r === 'MEDIUM').length,
        low: riskLevels.filter(r => r === 'LOW').length
      }
    };
  }

  generateMitigations(threats) {
    const mitigations = new Map();

    for (const threat of threats) {
      for (const mitigation of threat.mitigations) {
        if (!mitigations.has(mitigation)) {
          mitigations.set(mitigation, []);
        }
        mitigations.get(mitigation).push(threat.id);
      }
    }

    return Array.from(mitigations.entries()).map(([mitigation, threats]) => ({
      mitigation: mitigation,
      addressesThreats: threats,
      priority: this.calculateMitigationPriority(threats, threats)
    }));
  }

  calculateMitigationPriority(mitigation, threatIds) {
    const threatRisks = threatIds.map(id => {
      const threat = this.threats?.find(t => t.id === id);
      return threat ? threat.riskLevel : 'MEDIUM';
    });

    const highValueThreats = threatRisks.filter(r => r === 'CRITICAL' || r === 'HIGH').length;

    if (highValueThreats > 2) return 'CRITICAL';
    if (highValueThreats > 0) return 'HIGH';
    return 'MEDIUM';
  }

  generateThreatId() {
    return `THREAT_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Example Threat Modeling
const threatModeler = new STRIDEThreatModeler();

const systemComponents = [
  { name: 'WebServer', type: 'web_service', handlesData: true },
  { name: 'Database', type: 'database', handlesData: true },
  { name: 'AuthService', type: 'authentication_service', hasPrivileges: true }
];

const dataFlows = [
  { source: 'WebServer', target: 'Database', dataType: 'sensitive' },
  { source: 'AuthService', target: 'WebServer', dataType: 'credentials' }
];

const trustBoundaries = [
  ['WebServer', 'AuthService'], // Internal network
  ['Database'] // Restricted zone
];

const threatModel = threatModeler.analyzeSystem(systemComponents, dataFlows, trustBoundaries);
console.log('Threat Model:', JSON.stringify(threatModel, null, 2));
```

### Phase 3: Secure Design

**Objective:** Design security into the system architecture.

#### Security Architecture Principles
**Defense in Depth:**
- **Network Layer:** Firewalls, DMZs, network segmentation
- **Host Layer:** Host-based security controls, endpoint protection
- **Application Layer:** Input validation, secure coding practices
- **Data Layer:** Encryption, data integrity, access controls

**Zero Trust Architecture:**
- **Never Trust, Always Verify:** Continuous authentication and authorization
- **Micro-Segmentation:** Granular network and application segmentation
- **Least Privilege:** Minimal access rights for all entities
- **Continuous Monitoring:** Real-time security assessment and response

#### Secure Design Patterns
**Authentication Patterns:**
```javascript
// Secure Authentication Design Pattern
class SecureAuthenticationManager {
  constructor() {
    this.authMethods = new Map();
    this.sessionManager = new SessionManager();
    this.auditLogger = new AuditLogger();
  }

  // Register authentication methods
  registerAuthMethod(name, method) {
    this.authMethods.set(name, method);
  }

  // Multi-factor authentication
  async authenticateMFA(userId, factors) {
    const results = [];

    for (const factor of factors) {
      const method = this.authMethods.get(factor.type);
      if (!method) {
        results.push({ factor: factor.type, success: false, error: 'Method not available' });
        continue;
      }

      try {
        const result = await method.authenticate(factor.credentials);
        results.push({
          factor: factor.type,
          success: result.success,
          confidence: result.confidence || 1.0
        });
      } catch (error) {
        results.push({ factor: factor.type, success: false, error: error.message });
      }
    }

    // Calculate overall authentication result
    const successfulFactors = results.filter(r => r.success);
    const totalConfidence = successfulFactors.reduce((sum, r) => sum + r.confidence, 0);
    const averageConfidence = totalConfidence / factors.length;

    const overallSuccess = successfulFactors.length >= factors.length * 0.8 && averageConfidence >= 0.7;

    // Log authentication attempt
    await this.auditLogger.logAuthentication({
      userId: userId,
      factors: results,
      overallSuccess: overallSuccess,
      timestamp: new Date()
    });

    return {
      success: overallSuccess,
      factors: results,
      confidence: averageConfidence
    };
  }

  // Session management
  async createSecureSession(userId, authResult) {
    const sessionId = this.generateSecureSessionId();
    const sessionData = {
      id: sessionId,
      userId: userId,
      created: new Date(),
      lastActivity: new Date(),
      authFactors: authResult.factors,
      ipAddress: this.getClientIP(),
      userAgent: this.getUserAgent(),
      expires: new Date(Date.now() + 8 * 60 * 60 * 1000) // 8 hours
    };

    await this.sessionManager.storeSession(sessionData);

    return {
      sessionId: sessionId,
      expires: sessionData.expires
    };
  }

  // Continuous authentication
  async validateSession(sessionId) {
    const session = await this.sessionManager.getSession(sessionId);
    if (!session) return { valid: false, reason: 'Session not found' };

    // Check expiration
    if (new Date() > session.expires) {
      await this.sessionManager.destroySession(sessionId);
      return { valid: false, reason: 'Session expired' };
    }

    // Check for suspicious activity
    const riskAssessment = await this.assessSessionRisk(session);
    if (riskAssessment.risk > 0.7) {
      await this.handleSuspiciousSession(session, riskAssessment);
      return { valid: false, reason: 'Suspicious activity detected' };
    }

    // Update session activity
    session.lastActivity = new Date();
    await this.sessionManager.updateSession(session);

    return { valid: true, session: session };
  }

  async assessSessionRisk(session) {
    let riskScore = 0;

    // Check IP address change
    const currentIP = this.getClientIP();
    if (currentIP !== session.ipAddress) {
      riskScore += 0.3;
    }

    // Check user agent change
    const currentUA = this.getUserAgent();
    if (currentUA !== session.userAgent) {
      riskScore += 0.2;
    }

    // Check time since last activity
    const timeSinceActivity = Date.now() - session.lastActivity.getTime();
    if (timeSinceActivity > 30 * 60 * 1000) { // 30 minutes
      riskScore += 0.1;
    }

    // Check for concurrent sessions
    const userSessions = await this.sessionManager.getUserSessions(session.userId);
    if (userSessions.length > 3) {
      riskScore += 0.2;
    }

    return {
      risk: Math.min(riskScore, 1.0),
      factors: {
        ipChange: currentIP !== session.ipAddress,
        uaChange: currentUA !== session.userAgent,
        inactivity: timeSinceActivity > 30 * 60 * 1000,
        concurrentSessions: userSessions.length > 3
      }
    };
  }

  async handleSuspiciousSession(session, riskAssessment) {
    // Log suspicious activity
    await this.auditLogger.logSuspiciousActivity({
      sessionId: session.id,
      userId: session.userId,
      riskAssessment: riskAssessment,
      timestamp: new Date()
    });

    // Implement additional verification
    if (riskAssessment.risk > 0.8) {
      // Force re-authentication
      await this.sessionManager.destroySession(session.id);
    } else {
      // Send additional verification challenge
      await this.sendVerificationChallenge(session);
    }
  }

  generateSecureSessionId() {
    return crypto.randomBytes(32).toString('hex');
  }

  getClientIP() {
    // Implementation to get client IP
    return '192.168.1.100';
  }

  getUserAgent() {
    // Implementation to get user agent
    return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36';
  }

  async sendVerificationChallenge(session) {
    // Implementation to send additional verification
    console.log(`Sending verification challenge for session ${session.id}`);
  }
}

// Session Manager
class SessionManager {
  constructor() {
    this.sessions = new Map();
  }

  async storeSession(sessionData) {
    this.sessions.set(sessionData.id, sessionData);
  }

  async getSession(sessionId) {
    return this.sessions.get(sessionId);
  }

  async updateSession(session) {
    this.sessions.set(session.id, session);
  }

  async destroySession(sessionId) {
    this.sessions.delete(sessionId);
  }

  async getUserSessions(userId) {
    return Array.from(this.sessions.values()).filter(s => s.userId === userId);
  }
}

// Audit Logger
class AuditLogger {
  async logAuthentication(authData) {
    console.log('AUTHENTICATION:', JSON.stringify(authData));
  }

  async logSuspiciousActivity(activityData) {
    console.log('SUSPICIOUS_ACTIVITY:', JSON.stringify(activityData));
  }
}
```

**Authorization Patterns:**
```javascript
// Role-Based Access Control (RBAC) Design Pattern
class RBACAuthorizationManager {
  constructor() {
    this.roles = new Map();
    this.users = new Map();
    this.permissions = new Map();
    this.roleAssignments = new Map();
    this.permissionAssignments = new Map();
  }

  // Role management
  createRole(roleId, description, parentRole = null) {
    this.roles.set(roleId, {
      id: roleId,
      description: description,
      parent: parentRole,
      permissions: new Set(),
      active: true
    });
  }

  // Permission management
  definePermission(permissionId, resource, action, description) {
    this.permissions.set(permissionId, {
      id: permissionId,
      resource: resource,
      action: action,
      description: description
    });
  }

  // Role-permission assignment
  assignPermissionToRole(permissionId, roleId) {
    const role = this.roles.get(roleId);
    const permission = this.permissions.get(permissionId);

    if (role && permission) {
      role.permissions.add(permissionId);
      this.permissionAssignments.set(`${roleId}:${permissionId}`, true);
    }
  }

  // User-role assignment
  assignRoleToUser(userId, roleId) {
    if (!this.roleAssignments.has(userId)) {
      this.roleAssignments.set(userId, new Set());
    }
    this.roleAssignments.get(userId).add(roleId);
  }

  // Access control decision
  checkAccess(userId, resource, action, context = {}) {
    const userRoles = this.roleAssignments.get(userId) || new Set();

    // Get all permissions for user's roles (including inherited)
    const userPermissions = new Set();
    for (const roleId of userRoles) {
      const rolePermissions = this.getRolePermissions(roleId);
      rolePermissions.forEach(p => userPermissions.add(p));
    }

    // Check if any permission allows the action
    for (const permissionId of userPermissions) {
      const permission = this.permissions.get(permissionId);
      if (permission &&
          this.matchesResource(permission.resource, resource) &&
          this.matchesAction(permission.action, action) &&
          this.checkContext(permission, context)) {
        return { allowed: true, permission: permissionId };
      }
    }

    return { allowed: false, reason: 'No matching permission' };
  }

  // Get all permissions for a role (including inherited)
  getRolePermissions(roleId) {
    const permissions = new Set();
    const role = this.roles.get(roleId);

    if (role) {
      // Add direct permissions
      role.permissions.forEach(p => permissions.add(p));

      // Add inherited permissions
      if (role.parent) {
        const parentPermissions = this.getRolePermissions(role.parent);
        parentPermissions.forEach(p => permissions.add(p));
      }
    }

    return permissions;
  }

  // Resource matching (supports wildcards)
  matchesResource(permissionResource, requestedResource) {
    // Simple wildcard matching
    if (permissionResource === '*' || permissionResource === requestedResource) {
      return true;
    }

    // Pattern matching (e.g., "documents/*" matches "documents/123")
    if (permissionResource.includes('*')) {
      const pattern = permissionResource.replace(/\*/g, '.*');
      return new RegExp(`^${pattern}$`).test(requestedResource);
    }

    return false;
  }

  // Action matching
  matchesAction(permissionAction, requestedAction) {
    if (permissionAction === '*' || permissionAction === requestedAction) {
      return true;
    }

    // Support for action hierarchies (e.g., "read" implies "view")
    const actionHierarchy = {
      'manage': ['create', 'read', 'update', 'delete'],
      'write': ['create', 'update', 'delete'],
      'read': ['view']
    };

    const impliedActions = actionHierarchy[permissionAction] || [];
    return impliedActions.includes(requestedAction);
  }

  // Context checking
  checkContext(permission, context) {
    // Implementation for context-aware authorization
    // Could check time of day, location, device type, etc.
    return true; // Simplified
  }

  // Administrative functions
  revokeRoleFromUser(userId, roleId) {
    const userRoles = this.roleAssignments.get(userId);
    if (userRoles) {
      userRoles.delete(roleId);
    }
  }

  revokePermissionFromRole(permissionId, roleId) {
    const role = this.roles.get(roleId);
    if (role) {
      role.permissions.delete(permissionId);
      this.permissionAssignments.delete(`${roleId}:${permissionId}`);
    }
  }

  // Audit and reporting
  getUserPermissions(userId) {
    const userRoles = this.roleAssignments.get(userId) || new Set();
    const permissions = new Set();

    for (const roleId of userRoles) {
      const rolePermissions = this.getRolePermissions(roleId);
      rolePermissions.forEach(p => permissions.add(p));
    }

    return Array.from(permissions).map(p => this.permissions.get(p));
  }

  getRoleUsers(roleId) {
    const users = [];
    for (const [userId, roles] of this.roleAssignments) {
      if (roles.has(roleId)) {
        users.push(userId);
      }
    }
    return users;
  }

  generateAccessReport(userId = null, resource = null) {
    // Generate access report for auditing
    const report = {
      generated: new Date(),
      userId: userId,
      resource: resource,
      permissions: []
    };

    if (userId) {
      report.permissions = this.getUserPermissions(userId);
    } else {
      // Generate system-wide report
      for (const [uid, roles] of this.roleAssignments) {
        report.permissions.push({
          userId: uid,
          roles: Array.from(roles),
          permissions: this.getUserPermissions(uid)
        });
      }
    }

    return report;
  }
}

// Example RBAC Implementation
const rbac = new RBACAuthorizationManager();

// Define permissions
rbac.definePermission('read_documents', 'documents', 'read', 'Read documents');
rbac.definePermission('write_documents', 'documents', 'write', 'Create and modify documents');
rbac.definePermission('manage_users', 'users', 'manage', 'Manage user accounts');

// Define roles
rbac.createRole('viewer', 'Document viewer');
rbac.createRole('editor', 'Document editor');
rbac.createRole('admin', 'System administrator');

// Assign permissions to roles
rbac.assignPermissionToRole('read_documents', 'viewer');
rbac.assignPermissionToRole('read_documents', 'editor');
rbac.assignPermissionToRole('write_documents', 'editor');
rbac.assignPermissionToRole('manage_users', 'admin');

// Assign roles to users
rbac.assignRoleToUser('user1', 'viewer');
rbac.assignRoleToUser('user2', 'editor');
rbac.assignRoleToUser('admin1', 'admin');

// Test access control
console.log('User1 read documents:', rbac.checkAccess('user1', 'documents', 'read'));
console.log('User1 write documents:', rbac.checkAccess('user1', 'documents', 'write'));
console.log('User2 write documents:', rbac.checkAccess('user2', 'documents', 'write'));
console.log('Admin1 manage users:', rbac.checkAccess('admin1', 'users', 'manage'));
```

### Phase 4: Secure Implementation

**Objective:** Implement security controls through secure coding practices.

#### Secure Coding Standards
**Input Validation:**
```javascript
// Secure Input Validation Implementation
class InputValidator {
  constructor() {
    this.validationRules = new Map();
    this.sanitizationRules = new Map();
  }

  // Define validation rules
  defineValidationRule(fieldName, rules) {
    this.validationRules.set(fieldName, rules);
  }

  // Define sanitization rules
  defineSanitizationRule(fieldName, sanitizers) {
    this.sanitizationRules.set(fieldName, sanitizers);
  }

  // Validate input
  validateInput(input, context = {}) {
    const errors = [];
    const sanitized = {};

    for (const [fieldName, value] of Object.entries(input)) {
      try {
        // Sanitize first
        const sanitizedValue = this.sanitizeValue(fieldName, value);

        // Then validate
        const validationResult = this.validateField(fieldName, sanitizedValue, context);

        if (!validationResult.valid) {
          errors.push({
            field: fieldName,
            value: value,
            errors: validationResult.errors
          });
        } else {
          sanitized[fieldName] = sanitizedValue;
        }
      } catch (error) {
        errors.push({
          field: fieldName,
          value: value,
          errors: [error.message]
        });
      }
    }

    return {
      valid: errors.length === 0,
      errors: errors,
      sanitized: sanitized
    };
  }

  // Sanitize value
  sanitizeValue(fieldName, value) {
    const sanitizers = this.sanitizationRules.get(fieldName) || [];

    let sanitized = value;

    for (const sanitizer of sanitizers) {
      sanitized = this.applySanitizer(sanitizer, sanitized);
    }

    return sanitized;
  }

  // Apply sanitizer
  applySanitizer(sanitizer, value) {
    switch (sanitizer.type) {
      case 'trim':
        return value.trim();
      case 'lowercase':
        return value.toLowerCase();
      case 'uppercase':
        return value.toUpperCase();
      case 'remove_html':
        return value.replace(/<[^>]*>/g, '');
      case 'escape_sql':
        return value.replace(/['";\\]/g, '\\$&');
      case 'alphanumeric_only':
        return value.replace(/[^a-zA-Z0-9]/g, '');
      case 'email_normalize':
        return value.toLowerCase().trim();
      default:
        return value;
    }
  }

  // Validate field
  validateField(fieldName, value, context) {
    const rules = this.validationRules.get(fieldName) || [];
    const errors = [];

    for (const rule of rules) {
      const result = this.applyValidationRule(rule, value, context);
      if (!result.valid) {
        errors.push(result.message);
      }
    }

    return {
      valid: errors.length === 0,
      errors: errors
    };
  }

  // Apply validation rule
  applyValidationRule(rule, value, context) {
    switch (rule.type) {
      case 'required':
        return {
          valid: value !== null && value !== undefined && value !== '',
          message: `${rule.field} is required`
        };

      case 'min_length':
        return {
          valid: value.length >= rule.value,
          message: `${rule.field} must be at least ${rule.value} characters`
        };

      case 'max_length':
        return {
          valid: value.length <= rule.value,
          message: `${rule.field} must be at most ${rule.value} characters`
        };

      case 'pattern':
        return {
          valid: new RegExp(rule.pattern).test(value),
          message: `${rule.field} format is invalid`
        };

      case 'email':
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return {
          valid: emailPattern.test(value),
          message: 'Invalid email format'
        };

      case 'range':
        const num = Number(value);
        return {
          valid: num >= rule.min && num <= rule.max,
          message: `${rule.field} must be between ${rule.min} and ${rule.max}`
        };

      case 'in_list':
        return {
          valid: rule.list.includes(value),
          message: `${rule.field} must be one of: ${rule.list.join(', ')}`
        };

      case 'custom':
        return rule.validator(value, context);

      default:
        return { valid: true };
    }
  }

  // Batch validation
  validateBatch(inputs) {
    const results = [];

    for (const input of inputs) {
      const result = this.validateInput(input);
      results.push(result);
    }

    const allValid = results.every(r => r.valid);
    const allErrors = results.flatMap(r => r.errors);

    return {
      valid: allValid,
      results: results,
      errors: allErrors
    };
  }
}

// Example Input Validation Setup
const validator = new InputValidator();

// Define sanitization rules
validator.defineSanitizationRule('username', [
  { type: 'trim' },
  { type: 'lowercase' },
  { type: 'alphanumeric_only' }
]);

validator.defineSanitizationRule('email', [
  { type: 'trim' },
  { type: 'email_normalize' }
]);

validator.defineSanitizationRule('comment', [
  { type: 'remove_html' },
  { type: 'trim' }
]);

// Define validation rules
validator.defineValidationRule('username', [
  { type: 'required' },
  { type: 'min_length', value: 3 },
  { type: 'max_length', value: 20 },
  { type: 'pattern', pattern: '^[a-zA-Z0-9_]+$' }
]);

validator.defineValidationRule('email', [
  { type: 'required' },
  { type: 'email' },
  { type: 'max_length', value: 254 }
]);

validator.defineValidationRule('age', [
  { type: 'required' },
  { type: 'range', min: 13, max: 120 }
]);

// Test validation
const testInput = {
  username: '  John_Doe123!  ',
  email: 'JOHN.DOE@EXAMPLE.COM',
  age: '25',
  comment: '<script>alert("xss")</script>Hello World!'
};

const validationResult = validator.validateInput(testInput);
console.log('Validation Result:', JSON.stringify(validationResult, null, 2));
```

**Secure Error Handling:**
```javascript
// Secure Error Handling Implementation
class SecureErrorHandler {
  constructor() {
    this.errorLog = new SecureErrorLog();
    this.alertSystem = new AlertSystem();
    this.errorPatterns = new Map();
  }

  // Handle application errors
  handleError(error, context = {}) {
    // Classify error
    const errorClassification = this.classifyError(error);

    // Sanitize error information
    const safeError = this.sanitizeError(error);

    // Log error securely
    const logEntry = {
      timestamp: new Date(),
      errorId: this.generateErrorId(),
      classification: errorClassification,
      message: safeError.message,
      stackTrace: this.shouldIncludeStackTrace(errorClassification) ? safeError.stack : undefined,
      context: this.sanitizeContext(context),
      userId: context.userId,
      sessionId: context.sessionId,
      ipAddress: context.ipAddress
    };

    this.errorLog.logError(logEntry);

    // Check for error patterns
    this.analyzeErrorPatterns(logEntry);

    // Determine response
    const response = this.determineErrorResponse(errorClassification, context);

    // Send alerts if necessary
    if (response.alert) {
      this.alertSystem.sendAlert({
        type: 'error',
        severity: response.alertSeverity,
        message: `Error ${logEntry.errorId}: ${safeError.message}`,
        details: logEntry
      });
    }

    return response.userMessage;
  }

  // Classify error type
  classifyError(error) {
    if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
      return 'NETWORK_ERROR';
    }

    if (error.name === 'ValidationError') {
      return 'VALIDATION_ERROR';
    }

    if (error.name === 'AuthenticationError') {
      return 'AUTHENTICATION_ERROR';
    }

    if (error.name === 'AuthorizationError') {
      return 'AUTHORIZATION_ERROR';
    }

    if (error.message.includes('SQL') || error.message.includes('database')) {
      return 'DATABASE_ERROR';
    }

    if (error.name === 'SyntaxError' || error.name === 'TypeError') {
      return 'APPLICATION_ERROR';
    }

    return 'UNKNOWN_ERROR';
  }

  // Sanitize error information
  sanitizeError(error) {
    const safeError = {
      name: error.name,
      message: this.sanitizeErrorMessage(error.message),
      code: error.code
    };

    // Include stack trace only for development/debugging
    if (process.env.NODE_ENV === 'development') {
      safeError.stack = error.stack;
    }

    return safeError;
  }

  // Sanitize error message
  sanitizeErrorMessage(message) {
    // Remove sensitive information
    return message
      .replace(/password[=:][^&\s]*/gi, 'password=***')
      .replace(/token[=:][^&\s]*/gi, 'token=***')
      .replace(/key[=:][^&\s]*/gi, 'key=***')
      .replace(/secret[=:][^&\s]*/gi, 'secret=***')
      .replace(/\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b/g, '****-****-****-****') // Credit cards
      .replace(/\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g, '***-***-****'); // SSN
  }

  // Sanitize context information
  sanitizeContext(context) {
    const safeContext = { ...context };

    // Remove sensitive context data
    delete safeContext.password;
    delete safeContext.token;
    delete safeContext.sessionKey;
    delete safeContext.privateKey;

    return safeContext;
  }

  // Determine if stack trace should be included
  shouldIncludeStackTrace(classification) {
    const sensitiveErrors = ['AUTHENTICATION_ERROR', 'AUTHORIZATION_ERROR', 'VALIDATION_ERROR'];
    return !sensitiveErrors.includes(classification);
  }

  // Analyze error patterns
  analyzeErrorPatterns(logEntry) {
    const patternKey = `${logEntry.classification}:${logEntry.message}`;

    if (!this.errorPatterns.has(patternKey)) {
      this.errorPatterns.set(patternKey, {
        count: 0,
        firstSeen: logEntry.timestamp,
        lastSeen: logEntry.timestamp,
        instances: []
      });
    }

    const pattern = this.errorPatterns.get(patternKey);
    pattern.count++;
    pattern.lastSeen = logEntry.timestamp;
    pattern.instances.push(logEntry.errorId);

    // Keep only last 10 instances
    if (pattern.instances.length > 10) {
      pattern.instances = pattern.instances.slice(-10);
    }

    // Check for attack patterns
    if (pattern.count > 5 && this.isRecentActivity(pattern)) {
      this.handlePotentialAttack(pattern);
    }
  }

  // Check if activity is recent
  isRecentActivity(pattern) {
    const now = Date.now();
    const lastSeen = pattern.lastSeen.getTime();
    return (now - lastSeen) < (5 * 60 * 1000); // Within last 5 minutes
  }

  // Handle potential attack
  handlePotentialAttack(pattern) {
    console.log(`Potential attack detected: ${pattern.count} instances of ${pattern.key}`);

    this.alertSystem.sendAlert({
      type: 'potential_attack',
      severity: 'HIGH',
      message: `Repeated error pattern detected: ${pattern.key}`,
      details: {
        pattern: pattern,
        count: pattern.count,
        timeWindow: '5 minutes'
      }
    });
  }

  // Determine error response
  determineErrorResponse(classification, context) {
    const responses = {
      'NETWORK_ERROR': {
        userMessage: 'A network error occurred. Please try again later.',
        alert: false
      },
      'VALIDATION_ERROR': {
        userMessage: 'The provided information is invalid. Please check your input.',
        alert: false
      },
      'AUTHENTICATION_ERROR': {
        userMessage: 'Authentication failed. Please check your credentials.',
        alert: false
      },
      'AUTHORIZATION_ERROR': {
        userMessage: 'You do not have permission to perform this action.',
        alert: false
      },
      'DATABASE_ERROR': {
        userMessage: 'A system error occurred. Please try again later.',
        alert: true,
        alertSeverity: 'MEDIUM'
      },
      'APPLICATION_ERROR': {
        userMessage: 'An unexpected error occurred. Please try again.',
        alert: true,
        alertSeverity: 'HIGH'
      },
      'UNKNOWN_ERROR': {
        userMessage: 'An error occurred. Please contact support if the problem persists.',
        alert: true,
        alertSeverity: 'HIGH'
      }
    };

    return responses[classification] || responses['UNKNOWN_ERROR'];
  }

  // Generate unique error ID
  generateErrorId() {
    return `ERR_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Secure Error Log
class SecureErrorLog {
  async logError(logEntry) {
    // Implementation would write to secure log storage
    // Ensure logs are encrypted and access-controlled
    console.log('SECURE_ERROR_LOG:', JSON.stringify(logEntry));
  }
}

// Alert System
class AlertSystem {
  async sendAlert(alert) {
    // Implementation would send alerts via email, SMS, etc.
    console.log('ALERT:', JSON.stringify(alert));
  }
}

// Example error handling
const errorHandler = new SecureErrorHandler();

try {
  // Simulate an error
  throw new Error('Database connection failed: invalid password');
} catch (error) {
  const userMessage = errorHandler.handleError(error, {
    userId: 'user123',
    sessionId: 'session456',
    ipAddress: '192.168.1.100',
    action: 'login'
  });

  console.log('User message:', userMessage);
}
```

### Phase 5: Verification and Validation

**Objective:** Verify and validate security controls through testing and assessment.

#### Security Testing Methodology
**Static Application Security Testing (SAST):**
```javascript
// SAST Implementation for IACS Code
class StaticApplicationSecurityTester {
  constructor() {
    this.rules = new Map();
    this.vulnerabilities = [];
    this.severityLevels = {
      CRITICAL: 9,
      HIGH: 7,
      MEDIUM: 5,
      LOW: 3,
      INFO: 1
    };
  }

  // Define security rules
  defineRule(ruleId, pattern, message, severity, category) {
    this.rules.set(ruleId, {
      id: ruleId,
      pattern: pattern,
      message: message,
      severity: severity,
      category: category
    });
  }

  // Analyze source code
  async analyzeCode(sourceCode, filePath) {
    const findings = [];

    for (const [ruleId, rule] of this.rules) {
      const matches = this.scanForPattern(sourceCode, rule.pattern);

      for (const match of matches) {
        findings.push({
          ruleId: ruleId,
          file: filePath,
          line: match.line,
          column: match.column,
          code: match.code,
          message: rule.message,
          severity: rule.severity,
          category: rule.category,
          confidence: match.confidence || 1.0
        });
      }
    }

    return findings;
  }

  // Scan for pattern in code
  scanForPattern(code, pattern) {
    const matches = [];
    const lines = code.split('\n');

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const regex = new RegExp(pattern, 'gi');
      let match;

      while ((match = regex.exec(line)) !== null) {
        matches.push({
          line: i + 1,
          column: match.index + 1,
          code: line.trim(),
          match: match[0],
          confidence: this.calculateConfidence(match, line)
        });
      }
    }

    return matches;
  }

  // Calculate confidence in finding
  calculateConfidence(match, line) {
    let confidence = 0.8; // Base confidence

    // Increase confidence for dangerous patterns
    if (line.includes('password') || line.includes('secret') || line.includes('key')) {
      confidence += 0.1;
    }

    // Decrease confidence for commented code
    if (line.trim().startsWith('//') || line.trim().startsWith('/*') || line.trim().startsWith('*')) {
      confidence -= 0.3;
    }

    // Decrease confidence for test files
    if (line.includes('test') || line.includes('spec') || line.includes('mock')) {
      confidence -= 0.2;
    }

    return Math.max(0.1, Math.min(1.0, confidence));
  }

  // Analyze entire codebase
  async analyzeCodebase(filePaths) {
    const allFindings = [];

    for (const filePath of filePaths) {
      try {
        const sourceCode = await this.readFile(filePath);
        const findings = await this.analyzeCode(sourceCode, filePath);
        allFindings.push(...findings);
      } catch (error) {
        console.error(`Error analyzing ${filePath}: ${error.message}`);
      }
    }

    // Process and prioritize findings
    const processedFindings = this.processFindings(allFindings);

    return {
      summary: this.generateSummary(processedFindings),
      findings: processedFindings,
      recommendations: this.generateRecommendations(processedFindings)
    };
  }

  // Process findings
  processFindings(findings) {
    return findings
      .sort((a, b) => this.severityLevels[b.severity] - this.severityLevels[a.severity])
      .map(finding => ({
        ...finding,
        severityScore: this.severityLevels[finding.severity],
        cwe: this.mapToCWE(finding.ruleId),
        owasp: this.mapToOWASP(finding.category)
      }));
  }

  // Generate summary
  generateSummary(findings) {
    const severityCounts = {};
    const categoryCounts = {};

    for (const finding of findings) {
      severityCounts[finding.severity] = (severityCounts[finding.severity] || 0) + 1;
      categoryCounts[finding.category] = (categoryCounts[finding.category] || 0) + 1;
    }

    return {
      totalFindings: findings.length,
      severityBreakdown: severityCounts,
      categoryBreakdown: categoryCounts,
      riskScore: this.calculateRiskScore(findings)
    };
  }

  // Calculate overall risk score
  calculateRiskScore(findings) {
    let totalScore = 0;

    for (const finding of findings) {
      totalScore += finding.severityScore * finding.confidence;
    }

    return Math.min(100, totalScore / 10); // Normalize to 0-100 scale
  }

  // Generate recommendations
  generateRecommendations(findings) {
    const recommendations = [];

    const criticalCount = findings.filter(f => f.severity === 'CRITICAL').length;
    const highCount = findings.filter(f => f.severity === 'HIGH').length;

    if (criticalCount > 0) {
      recommendations.push({
        priority: 'CRITICAL',
        action: 'Immediate remediation required for critical findings',
        timeframe: 'Within 24 hours'
      });
    }

    if (highCount > 5) {
      recommendations.push({
        priority: 'HIGH',
        action: 'Address high-severity findings within sprint',
        timeframe: 'Within 1-2 weeks'
      });
    }

    recommendations.push({
      priority: 'MEDIUM',
      action: 'Implement security training for development team',
      timeframe: 'Ongoing'
    });

    recommendations.push({
      priority: 'MEDIUM',
      action: 'Integrate SAST into CI/CD pipeline',
      timeframe: 'Within 1 month'
    });

    return recommendations;
  }

  // Map to CWE
  mapToCWE(ruleId) {
    const cweMappings = {
      'hardcoded_password': 'CWE-798',
      'sql_injection': 'CWE-89',
      'xss_vulnerable': 'CWE-79',
      'weak_crypto': 'CWE-327',
      'path_traversal': 'CWE-22'
    };

    return cweMappings[ruleId] || 'CWE-710';
  }

  // Map to OWASP
  mapToOWASP(category) {
    const owaspMappings = {
      'injection': 'A03:2021-Injection',
      'authentication': 'A07:2021-Identification and Authentication Failures',
      'authorization': 'A01:2021-Broken Access Control',
      'cryptography': 'A02:2021-Cryptographic Failures',
      'configuration': 'A05:2021-Security Misconfiguration'
    };

    return owaspMappings[category] || 'A00:2021';
  }

  // File reading utility
  async readFile(filePath) {
    // Implementation would read file contents
    return 'sample code content';
  }
}

// Define security rules
const sast = new StaticApplicationSecurityTester();

sast.defineRule('hardcoded_password', 'password\\s*[=:]\\s*["\'][^"\']+["\']', 'Hardcoded password detected', 'CRITICAL', 'authentication');
sast.defineRule('sql_injection', '(SELECT|INSERT|UPDATE|DELETE).*\\+.*\\$|concat.*sql', 'Potential SQL injection vulnerability', 'HIGH', 'injection');
sast.defineRule('xss_vulnerable', 'document\\.write\\(|innerHTML\\s*[=:]', 'Potential XSS vulnerability', 'HIGH', 'injection');
sast.defineRule('weak_crypto', 'MD5\\(|SHA1\\(', 'Weak cryptographic function used', 'MEDIUM', 'cryptography');
sast.defineRule('path_traversal', '\\.\\./|\\.\\.', 'Potential path traversal vulnerability', 'MEDIUM', 'authorization');

// Example analysis
const sampleCode = `
function login(username, password) {
  const query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'";
  // Hardcoded password for testing
  const adminPass = "admin123";
  document.write("Welcome " + username);
  return executeQuery(query);
}
`;

const findings = sast.analyzeCode(sampleCode, 'login.js');
console.log('SAST Findings:', JSON.stringify(findings, null, 2));
```

**Dynamic Application Security Testing (DAST):**
```javascript
// DAST Implementation for IACS Applications
class DynamicApplicationSecurityTester {
  constructor() {
    this.scanners = new Map();
    this.testCases = new Map();
    this.vulnerabilities = [];
  }

  // Register security scanner
  registerScanner(name, scanner) {
    this.scanners.set(name, scanner);
  }

  // Define test case
  defineTestCase(testId, description, category, payload, expectedResult) {
    this.testCases.set(testId, {
      id: testId,
      description: description,
      category: category,
      payload: payload,
      expectedResult: expectedResult
    });
  }

  // Execute DAST scan
  async executeScan(targetUrl, scanConfig = {}) {
    const results = {
      scanId: this.generateScanId(),
      startTime: new Date(),
      target: targetUrl,
      findings: [],
      summary: {}
    };

    // Execute test cases
    for (const [testId, testCase] of this.testCases) {
      try {
        const finding = await this.executeTestCase(testCase, targetUrl, scanConfig);
        if (finding) {
          results.findings.push(finding);
        }
      } catch (error) {
        console.error(`Test case ${testId} failed: ${error.message}`);
      }
    }

    // Execute automated scanners
    for (const [scannerName, scanner] of this.scanners) {
      try {
        const scannerResults = await scanner.scan(targetUrl, scanConfig);
        results.findings.push(...scannerResults);
      } catch (error) {
        console.error(`Scanner ${scannerName} failed: ${error.message}`);
      }
    }

    // Process results
    results.endTime = new Date();
    results.duration = results.endTime - results.startTime;
    results.summary = this.generateSummary(results.findings);

    return results;
  }

  // Execute individual test case
  async executeTestCase(testCase, targetUrl, config) {
    // Prepare request
    const request = this.prepareRequest(testCase, targetUrl);

    // Send request
    const response = await this.sendRequest(request);

    // Analyze response
    const analysis = this.analyzeResponse(response, testCase);

    if (analysis.vulnerable) {
      return {
        testId: testCase.id,
        category: testCase.category,
        severity: analysis.severity,
        description: testCase.description,
        url: targetUrl,
        payload: testCase.payload,
        evidence: analysis.evidence,
        remediation: this.getRemediation(testCase.category)
      };
    }

    return null;
  }

  // Prepare HTTP request
  prepareRequest(testCase, targetUrl) {
    // Implementation would prepare HTTP request with test payload
    return {
      url: targetUrl,
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'DAST-Scanner/1.0'
      },
      body: `input=${encodeURIComponent(testCase.payload)}`
    };
  }

  // Send HTTP request
  async sendRequest(request) {
    // Implementation would send HTTP request and return response
    return {
      status: 200,
      headers: {},
      body: 'Response body'
    };
  }

  // Analyze response for vulnerabilities
  analyzeResponse(response, testCase) {
    const analysis = {
      vulnerable: false,
      severity: 'LOW',
      evidence: []
    };

    // Check for expected vulnerable behavior
    if (testCase.expectedResult === 'error' && response.status === 500) {
      analysis.vulnerable = true;
      analysis.severity = 'HIGH';
      analysis.evidence.push('Application returned 500 error with malicious input');
    }

    if (testCase.expectedResult === 'reflected' && response.body.includes(testCase.payload)) {
      analysis.vulnerable = true;
      analysis.severity = 'MEDIUM';
      analysis.evidence.push('Input reflected in response without sanitization');
    }

    if (testCase.expectedResult === 'data_exposed' && response.body.includes('sensitive_data')) {
      analysis.vulnerable = true;
      analysis.severity = 'CRITICAL';
      analysis.evidence.push('Sensitive data exposed in response');
    }

    return analysis;
  }

  // Get remediation advice
  getRemediation(category) {
    const remediations = {
      'sql_injection': 'Use parameterized queries or prepared statements. Validate and sanitize all input.',
      'xss': 'Encode output and validate input. Use Content Security Policy (CSP).',
      'authentication': 'Implement multi-factor authentication and secure password policies.',
      'authorization': 'Implement proper access controls and principle of least privilege.',
      'cryptography': 'Use strong encryption algorithms and proper key management.'
    };

    return remediations[category] || 'Implement appropriate security controls and input validation.';
  }

  // Generate scan summary
  generateSummary(findings) {
    const severityCounts = {};
    const categoryCounts = {};

    for (const finding of findings) {
      severityCounts[finding.severity] = (severityCounts[finding.severity] || 0) + 1;
      categoryCounts[finding.category] = (categoryCounts[finding.category] || 0) + 1;
    }

    return {
      totalFindings: findings.length,
      severityBreakdown: severityCounts,
      categoryBreakdown: categoryCounts,
      riskLevel: this.calculateRiskLevel(findings)
    };
  }

  // Calculate overall risk level
  calculateRiskLevel(findings) {
    const criticalCount = findings.filter(f => f.severity === 'CRITICAL').length;
    const highCount = findings.filter(f => f.severity === 'HIGH').length;

    if (criticalCount > 0) return 'CRITICAL';
    if (highCount > 3) return 'HIGH';
    if (highCount > 0) return 'MEDIUM';
    return 'LOW';
  }

  // Generate scan ID
  generateScanId() {
    return `DAST_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Define test cases
const dast = new DynamicApplicationSecurityTester();

dast.defineTestCase('sql_injection_1', 'Basic SQL injection test', 'sql_injection', "' OR '1'='1", 'error');
dast.defineTestCase('xss_1', 'Basic XSS test', 'xss', '<script>alert("xss")</script>', 'reflected');
dast.defineTestCase('auth_bypass', 'Authentication bypass test', 'authentication', 'admin\' --', 'bypass');

// Example scan
const scanResults = await dast.executeScan('http://target-app.com/login');
console.log('DAST Results:', JSON.stringify(scanResults, null, 2));
```

### Phase 6: Patch Management

**Objective:** Manage security patches and updates throughout the product lifecycle.

#### Patch Management Process
**Vulnerability Monitoring:**
```javascript
// Vulnerability Monitoring and Patch Management System
class VulnerabilityPatchManager {
  constructor() {
    this.vulnerabilitySources = new Map();
    this.patchInventory = new Map();
    this.affectedSystems = new Map();
    this.patchSchedule = new Map();
  }

  // Register vulnerability source
  registerVulnerabilitySource(name, source) {
    this.vulnerabilitySources.set(name, source);
  }

  // Monitor vulnerabilities
  async monitorVulnerabilities() {
    const vulnerabilities = [];

    for (const [sourceName, source] of this.vulnerabilitySources) {
      try {
        const sourceVulns = await source.fetchVulnerabilities();
        vulnerabilities.push(...sourceVulns);
      } catch (error) {
        console.error(`Failed to fetch from ${sourceName}: ${error.message}`);
      }
    }

    // Process and deduplicate vulnerabilities
    const processedVulns = this.processVulnerabilities(vulnerabilities);

    // Check relevance to our systems
    const relevantVulns = await this.filterRelevantVulnerabilities(processedVulns);

    // Update patch inventory
    await this.updatePatchInventory(relevantVulns);

    return relevantVulns;
  }

  // Process vulnerabilities
  processVulnerabilities(vulnerabilities) {
    const processed = new Map();

    for (const vuln of vulnerabilities) {
      const key = `${vuln.cve || vuln.id}`;

      if (!processed.has(key)) {
        processed.set(key, {
          id: vuln.id,
          cve: vuln.cve,
          description: vuln.description,
          severity: vuln.severity || this.calculateSeverity(vuln),
          cvss: vuln.cvss,
          affectedProducts: vuln.affectedProducts || [],
          references: vuln.references || [],
          published: vuln.published,
          lastModified: vuln.lastModified,
          status: vuln.status || 'active'
        });
      }
    }

    return Array.from(processed.values());
  }

  // Calculate severity if not provided
  calculateSeverity(vuln) {
    // Simple severity calculation based on CVSS
    if (vuln.cvss >= 9.0) return 'CRITICAL';
    if (vuln.cvss >= 7.0) return 'HIGH';
    if (vuln.cvss >= 4.0) return 'MEDIUM';
    return 'LOW';
  }

  // Filter relevant vulnerabilities
  async filterRelevantVulnerabilities(vulnerabilities) {
    const relevant = [];

    for (const vuln of vulnerabilities) {
      const affectedSystems = await this.findAffectedSystems(vuln);

      if (affectedSystems.length > 0) {
        vuln.affectedSystems = affectedSystems;
        relevant.push(vuln);
      }
    }

    return relevant;
  }

  // Find affected systems
  async findAffectedSystems(vulnerability) {
    const affected = [];

    // Check against system inventory
    for (const [systemId, system] of this.affectedSystems) {
      if (this.isSystemAffected(system, vulnerability)) {
        affected.push({
          systemId: systemId,
          systemName: system.name,
          installedVersion: system.version,
          affectedComponents: this.findAffectedComponents(system, vulnerability)
        });
      }
    }

    return affected;
  }

  // Check if system is affected
  isSystemAffected(system, vulnerability) {
    for (const affectedProduct of vulnerability.affectedProducts) {
      if (this.matchesProduct(system, affectedProduct)) {
        return true;
      }
    }
    return false;
  }

  // Match product against system
  matchesProduct(system, affectedProduct) {
    // Check vendor, product, and version
    return system.vendor === affectedProduct.vendor &&
           system.product === affectedProduct.product &&
           this.matchesVersion(system.version, affectedProduct.version);
  }

  // Version matching logic
  matchesVersion(systemVersion, affectedVersion) {
    // Simple version comparison - could be enhanced with semver
    if (affectedVersion.includes(systemVersion)) return true;
    if (affectedVersion === 'all' || affectedVersion === '*') return true;

    // Check version ranges
    if (affectedVersion.includes('<') || affectedVersion.includes('>')) {
      return this.checkVersionRange(systemVersion, affectedVersion);
    }

    return false;
  }

  // Check version range
  checkVersionRange(version, range) {
    // Simplified version range checking
    const cleanVersion = version.replace(/[^0-9.]/g, '');
    const cleanRange = range.replace(/[^0-9.<>=]/g, '');

    // This would need proper semver implementation
    return true; // Placeholder
  }

  // Find affected components
  findAffectedComponents(system, vulnerability) {
    // Implementation would identify specific components affected
    return ['component1', 'component2'];
  }

  // Update patch inventory
  async updatePatchInventory(vulnerabilities) {
    for (const vuln of vulnerabilities) {
      // Check if patch exists
      const patch = await this.findAvailablePatch(vuln);

      if (patch) {
        this.patchInventory.set(vuln.id, {
          vulnerability: vuln,
          patch: patch,
          status: 'available',
          discovered: new Date()
        });
      } else {
        this.patchInventory.set(vuln.id, {
          vulnerability: vuln,
          patch: null,
          status: 'no_patch_available',
          discovered: new Date()
        });
      }
    }
  }

  // Find available patch
  async findAvailablePatch(vulnerability) {
    // Implementation would check patch repositories
    // Return patch information if available
    return {
      id: `PATCH_${vulnerability.id}`,
      version: '1.0.1',
      releaseDate: new Date(),
      downloadUrl: `https://patches.example.com/${vulnerability.id}`,
      requirements: ['restart_required']
    };
  }

  // Schedule patch deployment
  async schedulePatchDeployment(vulnerabilityId, scheduleConfig) {
    const patchInfo = this.patchInventory.get(vulnerabilityId);

    if (!patchInfo || !patchInfo.patch) {
      throw new Error(`No patch available for ${vulnerabilityId}`);
    }

    const schedule = {
      vulnerabilityId: vulnerabilityId,
      patchId: patchInfo.patch.id,
      affectedSystems: patchInfo.vulnerability.affectedSystems,
      deploymentDate: scheduleConfig.date,
      maintenanceWindow: scheduleConfig.window,
      rollbackPlan: scheduleConfig.rollbackPlan,
      testingRequirements: scheduleConfig.testing,
      approvalRequired: scheduleConfig.approval,
      status: 'scheduled'
    };

    this.patchSchedule.set(vulnerabilityId, schedule);

    // Notify stakeholders
    await this.notifyPatchSchedule(schedule);

    return schedule;
  }

  // Execute patch deployment
  async executePatchDeployment(vulnerabilityId) {
    const schedule = this.patchSchedule.get(vulnerabilityId);

    if (!schedule) {
      throw new Error(`No deployment schedule found for ${vulnerabilityId}`);
    }

    schedule.status = 'in_progress';
    schedule.startTime = new Date();

    try {
      // Pre-deployment validation
      await this.validatePreDeployment(schedule);

      // Backup systems
      await this.backupSystems(schedule);

      // Deploy patch
      const deploymentResult = await this.deployPatch(schedule);

      // Post-deployment validation
      await this.validatePostDeployment(schedule);

      // Update status
      schedule.status = 'completed';
      schedule.endTime = new Date();
      schedule.result = deploymentResult;

      // Notify completion
      await this.notifyDeploymentCompletion(schedule);

    } catch (error) {
      schedule.status = 'failed';
      schedule.endTime = new Date();
      schedule.error = error.message;

      // Execute rollback if needed
      await this.executeRollback(schedule);

      // Notify failure
      await this.notifyDeploymentFailure(schedule);
    }

    return schedule;
  }

  // Validation methods
  async validatePreDeployment(schedule) {
    // Implementation would validate system readiness
    console.log(`Validating pre-deployment for ${schedule.vulnerabilityId}`);
  }

  async backupSystems(schedule) {
    // Implementation would backup affected systems
    console.log(`Backing up systems for ${schedule.vulnerabilityId}`);
  }

  async deployPatch(schedule) {
    // Implementation would deploy the patch
    console.log(`Deploying patch for ${schedule.vulnerabilityId}`);
    return { success: true, details: 'Patch deployed successfully' };
  }

  async validatePostDeployment(schedule) {
    // Implementation would validate deployment success
    console.log(`Validating post-deployment for ${schedule.vulnerabilityId}`);
  }

  async executeRollback(schedule) {
    // Implementation would rollback the patch
    console.log(`Rolling back patch for ${schedule.vulnerabilityId}`);
  }

  // Notification methods
  async notifyPatchSchedule(schedule) {
    console.log(`Patch scheduled: ${JSON.stringify(schedule)}`);
  }

  async notifyDeploymentCompletion(schedule) {
    console.log(`Patch deployment completed: ${JSON.stringify(schedule)}`);
  }

  async notifyDeploymentFailure(schedule) {
    console.log(`Patch deployment failed: ${JSON.stringify(schedule)}`);
  }

  // Reporting
  generatePatchReport() {
    const report = {
      generated: new Date(),
      inventory: Array.from(this.patchInventory.values()),
      schedule: Array.from(this.patchSchedule.values()),
      summary: this.generatePatchSummary()
    };

    return report;
  }

  generatePatchSummary() {
    const inventory = Array.from(this.patchInventory.values());
    const schedule = Array.from(this.patchSchedule.values());

    return {
      totalVulnerabilities: inventory.length,
      patchedVulnerabilities: inventory.filter(i => i.status === 'patched').length,
      pendingPatches: inventory.filter(i => i.status === 'available').length,
      noPatchAvailable: inventory.filter(i => i.status === 'no_patch_available').length,
      scheduledDeployments: schedule.filter(s => s.status === 'scheduled').length,
      completedDeployments: schedule.filter(s => s.status === 'completed').length,
      failedDeployments: schedule.filter(s => s.status === 'failed').length
    };
  }
}

// Example usage
const patchManager = new VulnerabilityPatchManager();

// Register vulnerability sources
patchManager.registerVulnerabilitySource('nvd', {
  fetchVulnerabilities: async () => {
    // Implementation would fetch from NVD
    return [{
      id: 'CVE-2023-12345',
      cve: 'CVE-2023-12345',
      description: 'Buffer overflow in network service',
      cvss: 8.5,
      affectedProducts: [{
        vendor: 'ExampleCorp',
        product: 'NetworkService',
        version: '< 2.0.0'
      }]
    }];
  }
});

// Register affected systems
patchManager.affectedSystems.set('system1', {
  name: 'Production Server',
  vendor: 'ExampleCorp',
  product: 'NetworkService',
  version: '1.5.0'
});

// Monitor vulnerabilities
const vulnerabilities = await patchManager.monitorVulnerabilities();
console.log('Relevant vulnerabilities:', vulnerabilities);

// Schedule patch deployment
const schedule = await patchManager.schedulePatchDeployment('CVE-2023-12345', {
  date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 1 week from now
  window: 'maintenance_window_1',
  rollbackPlan: 'restore_from_backup',
  testing: ['functional_test', 'security_test'],
  approval: true
});

console.log('Patch schedule:', schedule);
```

### Phase 7: Product End-of-Life

**Objective:** Manage secure disposal and end-of-life for IACS products.

#### End-of-Life Management Process
**Product Lifecycle Planning:**
```javascript
// Product End-of-Life Management System
class ProductEndOfLifeManager {
  constructor() {
    this.products = new Map();
    this.lifecyclePolicies = new Map();
    this.disposalProcedures = new Map();
    this.notificationTemplates = new Map();
  }

  // Register product
  registerProduct(productId, productInfo) {
    this.products.set(productId, {
      id: productId,
      name: productInfo.name,
      version: productInfo.version,
      releaseDate: productInfo.releaseDate,
      supportEndDate: productInfo.supportEndDate,
      endOfLifeDate: productInfo.endOfLifeDate,
      lifecycleStatus: this.calculateLifecycleStatus(productInfo),
      customers: productInfo.customers || [],
      securityUpdates: productInfo.securityUpdates || []
    });
  }

  // Calculate lifecycle status
  calculateLifecycleStatus(productInfo) {
    const now = new Date();

    if (now > productInfo.endOfLifeDate) {
      return 'end_of_life';
    } else if (now > productInfo.supportEndDate) {
      return 'extended_support';
    } else {
      return 'active_support';
    }
  }

  // Plan end-of-life process
  async planEndOfLife(productId, eolConfig) {
    const product = this.products.get(productId);
    if (!product) {
      throw new Error(`Product ${productId} not found`);
    }

    const eolPlan = {
      productId: productId,
      announcementDate: eolConfig.announcementDate,
      lastSupportDate: eolConfig.lastSupportDate,
      endOfLifeDate: eolConfig.endOfLifeDate,
      migrationPath: eolConfig.migrationPath,
      disposalProcedures: eolConfig.disposalProcedures,
      communicationPlan: eolConfig.communicationPlan,
      status: 'planned'
    };

    // Validate EOL plan
    await this.validateEOLPlan(eolPlan);

    // Store EOL plan
    product.eolPlan = eolPlan;

    // Schedule notifications
    await this.scheduleEOLNotifications(eolPlan);

    return eolPlan;
  }

  // Validate EOL plan
  async validateEOLPlan(plan) {
    const now = new Date();

    // Check dates are in correct order
    if (plan.announcementDate >= plan.lastSupportDate ||
        plan.lastSupportDate >= plan.endOfLifeDate) {
      throw new Error('EOL dates must be in chronological order');
    }

    // Check announcement is not in the past
    if (plan.announcementDate < now) {
      throw new Error('Announcement date cannot be in the past');
    }

    // Validate migration path exists
    if (!plan.migrationPath || !plan.migrationPath.targetProduct) {
      throw new Error('Migration path must be specified');
    }

    // Check disposal procedures are defined
    if (!plan.disposalProcedures || plan.disposalProcedures.length === 0) {
      throw new Error('Disposal procedures must be defined');
    }
  }

  // Schedule EOL notifications
  async scheduleEOLNotifications(plan) {
    const notifications = [
      {
        type: 'pre_announcement',
        date: new Date(plan.announcementDate.getTime() - 90 * 24 * 60 * 60 * 1000), // 90 days before
        template: 'eol_pre_announcement'
      },
      {
        type: 'announcement',
        date: plan.announcementDate,
        template: 'eol_announcement'
      },
      {
        type: 'last_support_warning',
        date: new Date(plan.lastSupportDate.getTime() - 30 * 24 * 60 * 60 * 1000), // 30 days before
        template: 'eol_support_warning'
      },
      {
        type: 'end_of_life',
        date: plan.endOfLifeDate,
        template: 'eol_final'
      }
    ];

    for (const notification of notifications) {
      await this.scheduleNotification(notification, plan);
    }
  }

  // Schedule individual notification
  async scheduleNotification(notification, plan) {
    // Implementation would schedule notification in job queue
    console.log(`Scheduled ${notification.type} notification for ${plan.productId} on ${notification.date}`);
  }

  // Execute EOL process
  async executeEndOfLife(productId) {
    const product = this.products.get(productId);
    if (!product || !product.eolPlan) {
      throw new Error(`No EOL plan found for product ${productId}`);
    }

    const plan = product.eolPlan;
    plan.status = 'executing';

    try {
      // Send final notifications
      await this.sendFinalNotifications(plan);

      // Disable new deployments
      await this.disableNewDeployments(productId);

      // Execute customer migrations
      await this.executeCustomerMigrations(plan);

      // Secure data disposal
      await this.executeDataDisposal(plan);

      // Archive product information
      await this.archiveProductInformation(productId);

      // Update product status
      product.lifecycleStatus = 'end_of_life';
      plan.status = 'completed';
      plan.completionDate = new Date();

    } catch (error) {
      plan.status = 'failed';
      plan.error = error.message;
      throw error;
    }

    return plan;
  }

  // Send final notifications
  async sendFinalNotifications(plan) {
    const template = this.notificationTemplates.get('eol_final');
    const customers = await this.getProductCustomers(plan.productId);

    for (const customer of customers) {
      await this.sendNotification(customer, template, plan);
    }
  }

  // Disable new deployments
  async disableNewDeployments(productId) {
    // Implementation would disable product in deployment systems
    console.log(`Disabled new deployments for ${productId}`);
  }

  // Execute customer migrations
  async executeCustomerMigrations(plan) {
    const customers = await this.getProductCustomers(plan.productId);

    for (const customer of customers) {
      await this.initiateMigration(customer, plan.migrationPath);
    }
  }

  // Execute data disposal
  async executeDataDisposal(plan) {
    for (const procedure of plan.disposalProcedures) {
      await this.executeDisposalProcedure(procedure, plan.productId);
    }
  }

  // Archive product information
  async archiveProductInformation(productId) {
    const product = this.products.get(productId);

    // Implementation would archive product data securely
    console.log(`Archived information for ${productId}`);
  }

  // Utility methods
  async getProductCustomers(productId) {
    const product = this.products.get(productId);
    return product.customers;
  }

  async sendNotification(customer, template, plan) {
    // Implementation would send notification to customer
    console.log(`Sent ${template} notification to ${customer.id} for ${plan.productId}`);
  }

  async initiateMigration(customer, migrationPath) {
    // Implementation would initiate migration process
    console.log(`Initiated migration for customer ${customer.id} to ${migrationPath.targetProduct}`);
  }

  async executeDisposalProcedure(procedure, productId) {
    // Implementation would execute disposal procedure
    console.log(`Executed disposal procedure ${procedure.type} for ${productId}`);
  }

  // Reporting
  generateEOLReport() {
    const products = Array.from(this.products.values());
    const activeEOL = products.filter(p => p.eolPlan && p.eolPlan.status !== 'completed');

    return {
      generated: new Date(),
      totalProducts: products.length,
      activeEOLProcesses: activeEOL.length,
      completedEOLProcesses: products.filter(p => p.lifecycleStatus === 'end_of_life').length,
      upcomingEOL: this.getUpcomingEOL(products),
      eolPlans: activeEOL.map(p => p.eolPlan)
    };
  }

  getUpcomingEOL(products) {
    const now = new Date();
    const thirtyDaysFromNow = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);

    return products
      .filter(p => p.endOfLifeDate && p.endOfLifeDate <= thirtyDaysFromNow && p.endOfLifeDate > now)
      .map(p => ({
        productId: p.id,
        name: p.name,
        endOfLifeDate: p.endOfLifeDate,
        daysUntilEOL: Math.ceil((p.endOfLifeDate - now) / (24 * 60 * 60 * 1000))
      }))
      .sort((a, b) => a.endOfLifeDate - b.endOfLifeDate);
  }
}

// Example EOL management
const eolManager = new ProductEndOfLifeManager();

// Register product
eolManager.registerProduct('product1', {
  name: 'Legacy SCADA System',
  version: '1.0',
  releaseDate: new Date('2010-01-01'),
  supportEndDate: new Date('2025-12-31'),
  endOfLifeDate: new Date('2026-12-31'),
  customers: [
    { id: 'customer1', name: 'Manufacturing Corp' },
    { id: 'customer2', name: 'Utility Company' }
  ]
});

// Plan EOL
const eolPlan = await eolManager.planEndOfLife('product1', {
  announcementDate: new Date('2025-06-01'),
  lastSupportDate: new Date('2025-12-31'),
  endOfLifeDate: new Date('2026-12-31'),
  migrationPath: {
    targetProduct: 'product2',
    migrationGuide: 'migration-guide.pdf',
    supportAvailable: true
  },
  disposalProcedures: [
    { type: 'data_sanitization', method: 'cryptographic_erase' },
    { type: 'physical_destruction', method: 'shredding' }
  ],
  communicationPlan: {
    initialNotification: 'eol_announcement',
    regularUpdates: 'monthly',
    finalNotification: 'eol_final'
  }
});

console.log('EOL Plan:', JSON.stringify(eolPlan, null, 2));

// Generate EOL report
const eolReport = eolManager.generateEOLReport();
console.log('EOL Report:', JSON.stringify(eolReport, null, 2));
```

## Comprehensive Checklists

### IEC 62443-4-1 Implementation Checklist

#### Phase 1: Security Management
- [ ] Security governance framework established
- [ ] Security roles and responsibilities defined
- [ ] Security policy framework developed
- [ ] Risk management process implemented
- [ ] Security training program established
- [ ] Management commitment documented

#### Phase 2: Security Requirements
- [ ] Security functional requirements defined
- [ ] Security assurance requirements specified
- [ ] Threat modeling completed
- [ ] Security requirements traceability established
- [ ] Requirements validation completed

#### Phase 3: Secure Design
- [ ] Security architecture designed
- [ ] Defense in depth implemented
- [ ] Zero trust principles applied
- [ ] Secure design patterns used
- [ ] Security design review completed

#### Phase 4: Secure Implementation
- [ ] Secure coding standards applied
- [ ] Input validation implemented
- [ ] Secure error handling used
- [ ] Security testing integrated
- [ ] Code security review completed

#### Phase 5: Verification and Validation
- [ ] Static security testing performed
- [ ] Dynamic security testing completed
- [ ] Penetration testing conducted
- [ ] Security requirements validation done
- [ ] Security certification obtained

#### Phase 6: Patch Management
- [ ] Vulnerability monitoring established
- [ ] Patch management process implemented
- [ ] Patch testing procedures defined
- [ ] Patch deployment automated
- [ ] Patch effectiveness monitored

#### Phase 7: Product End-of-Life
- [ ] End-of-life planning completed
- [ ] Customer migration supported
- [ ] Secure data disposal implemented
- [ ] Product information archived
- [ ] End-of-life communication managed

## Audit Procedures

### IEC 62443-4-1 SDL Audit Methodology

#### 1. Pre-Audit Preparation
**Objective:** Ensure comprehensive audit coverage of SDL processes

**Activities:**
- Review SDL documentation and procedures
- Interview development and security teams
- Assess tool integration and automation
- Review security testing results
- Evaluate patch management processes

**Deliverables:**
- SDL audit scope and objectives
- Process documentation review
- Team interview summaries
- Tool and automation assessment

#### 2. SDL Process Audit
**Objective:** Verify SDL processes are properly implemented and effective

**Audit Criteria:**
- All 7 SDL phases are implemented
- Security requirements are properly defined
- Secure design principles are applied
- Secure coding practices are followed
- Security testing is comprehensive
- Patch management is effective
- End-of-life processes are defined

**Evidence Collection:**
- Process documentation
- Security requirements documents
- Design and code review records
- Testing reports and results
- Patch management records
- End-of-life plans

#### 3. Tool and Automation Audit
**Objective:** Assess effectiveness of security tools and automation

**Review Areas:**
- SAST tool integration and results
- DAST tool configuration and findings
- SCA tool implementation
- CI/CD security integration
- Automated security testing coverage

**Performance Evaluation:**
- Tool coverage and accuracy
- False positive/negative rates
- Integration with development workflow
- Security finding resolution times

#### 4. Metrics and Reporting Audit
**Objective:** Evaluate security metrics and reporting effectiveness

**Audit Components:**
- Security metrics definition and calculation
- Metrics reporting frequency and accuracy
- Security KPI tracking and trends
- Management reporting effectiveness
- Continuous improvement based on metrics

**Compliance Verification:**
- Metrics align with IEC 62443 requirements
- Reporting is timely and actionable
- Metrics drive security improvements
- Stakeholder feedback on reporting

## Real-World Implementation Examples

### Secure Development for Industrial Control Systems

#### Background
- **Organization:** Industrial automation vendor
- **Product:** SCADA system for manufacturing
- **Challenge:** Implement IEC 62443-4-1 across development lifecycle
- **Scope:** 50-person development team, 2M lines of code

#### SDL Implementation
**Phase 1: Security Management**
- Established security champions in each development team
- Implemented mandatory security training for all developers
- Created security requirements database
- Established security architecture review board

**Phase 2: Security Requirements**
- Developed security requirements templates
- Implemented threat modeling for all major features
- Created security requirements traceability matrix
- Established security requirement validation process

**Phase 3: Secure Design**
- Implemented secure design patterns library
- Established security architecture review process
- Integrated threat modeling into design phase
- Created security design guidelines

**Results:**
- **Security Defects:** 80% reduction in security defects
- **Time to Market:** 15% improvement in development velocity
- **Compliance:** Achieved IEC 62443-4-1 certification
- **Customer Confidence:** Improved security reputation

### Patch Management Excellence

#### Background
- **Organization:** ICS component manufacturer
- **Products:** PLCs, RTUs, industrial switches
- **Challenge:** Manage security patches across embedded systems
- **Scope:** 20 product lines, 100K+ deployed devices

#### Patch Management Implementation
**Vulnerability Monitoring:**
- Integrated NVD and vendor vulnerability feeds
- Implemented automated vulnerability scanning
- Established vulnerability assessment process
- Created vulnerability prioritization matrix

**Patch Development:**
- Established secure patch development environment
- Implemented automated testing for patches
- Created patch validation procedures
- Established patch release process

**Deployment and Monitoring:**
- Implemented automated patch deployment
- Created patch success monitoring
- Established patch rollback procedures
- Implemented patch compliance reporting

**Results:**
- **Patch Deployment:** 95% successful automated deployments
- **Vulnerability Remediation:** Average 7 days to patch critical vulnerabilities
- **Downtime:** Zero production downtime from patching
- **Compliance:** 100% compliance with patch management requirements

### End-of-Life Management Success

#### Background
- **Organization:** Legacy ICS system vendor
- **Products:** 15-year-old SCADA platform
- **Challenge:** Manage secure end-of-life for critical infrastructure
- **Scope:** 200+ customer installations, national critical infrastructure

#### EOL Implementation
**Planning and Communication:**
- Developed comprehensive EOL plan 2 years in advance
- Established customer communication cadence
- Created migration path to replacement platform
- Provided extended support options

**Migration Support:**
- Developed automated migration tools
- Provided on-site migration assistance
- Created detailed migration documentation
- Established migration support team

**Secure Disposal:**
- Implemented cryptographic data sanitization
- Provided secure hardware disposal services
- Created data disposal verification process
- Established chain of custody procedures

**Results:**
- **Migration Success:** 98% of customers successfully migrated
- **Data Security:** Zero data breaches during EOL process
- **Customer Satisfaction:** 95% customer satisfaction with EOL process
- **Regulatory Compliance:** Full compliance with data disposal regulations

## 📚 References

International Electrotechnical Commission. (2023). *IEC 62443-4-1: Industrial communication networks - Network and system security - Part 4-1: Secure development lifecycle requirements for product suppliers*. IEC.

International Society of Automation. (2022). *ISA/IEC 62443 Cybersecurity Fundamentals for Practitioners*. ISA.

Microsoft. (2022). *Security Development Lifecycle (SDL) Version 8.2*. Microsoft Corporation.

National Institute of Standards and Technology. (2023). *Secure Software Development Framework* (NIST SP 800-218). U.S. Department of Commerce.

## 🔗 See Also

- [[IEC 62443 Part 1]] - Terminology, concepts, and models
- [[IEC 62443 Part 2]] - Security program requirements
- [[IEC 62443 Part 3]] - System security requirements
- [[Secure Development Lifecycle]] - SDL implementation guide
- [[Vulnerability Management]] - Security testing and validation
- [[Patch Management]] - Secure maintenance practices
        "security_validation"
      ],
      "authority_level": "technical"
    }
  }
}
```

**Security Policy Framework:**
- Information security policy
- Acceptable use policy
- Data classification policy
- Incident response policy
- Change management policy

#### Risk Management Integration

**Risk Assessment Process:**
```json
{
  "risk_assessment_process": {
    "identification": {
      "threat_sources": ["malicious_actors", "accidental_events", "environmental_factors"],
      "vulnerability_sources": ["software_flaws", "configuration_errors", "supply_chain_risks"],
      "impact_areas": ["confidentiality", "integrity", "availability"]
    },
    "analysis": {
      "likelihood_scale": ["very_low", "low", "medium", "high", "very_high"],
      "impact_scale": ["minimal", "minor", "moderate", "major", "severe"],
      "risk_matrix": "5x5_matrix"
    },
    "treatment": {
      "options": ["accept", "avoid", "mitigate", "transfer"],
      "controls": ["preventive", "detective", "corrective"]
    }
  }
}
```

### Phase 2: Security Requirements

**Objective:** Define security requirements throughout the development lifecycle.

#### Security Requirements Elicitation

**Stakeholder Analysis:**
- End users and operators
- System administrators
- Security personnel
- Compliance officers
- Business stakeholders

**Requirements Categories:**
- Functional security requirements
- Assurance requirements
- Operational requirements
- Environmental requirements

#### Security Requirements Specification

**Template Structure:**
```markdown
# Security Requirements Specification (SRS)

## 1. Introduction
### 1.1 Purpose
### 1.2 Scope
### 1.3 Definitions and Acronyms

## 2. Security Requirements
### 2.1 Authentication Requirements
### 2.2 Authorization Requirements
### 2.3 Audit and Accountability Requirements
### 2.4 Confidentiality Requirements
### 2.5 Integrity Requirements
### 2.6 Availability Requirements
### 2.7 Non-Repudiation Requirements

## 3. Security Assurance Requirements
### 3.1 Development Assurance
### 3.2 Operational Assurance
### 3.3 Continuous Monitoring

## 4. Security Constraints
### 4.1 Technical Constraints
### 4.2 Environmental Constraints
### 4.3 Regulatory Constraints
```

### Phase 3: Secure Design

**Objective:** Incorporate security principles into system design.

#### Threat Modeling Methodology

**STRIDE Threat Analysis:**
```json
{
  "stride_analysis": {
    "spoofing": {
      "description": "Impersonation of legitimate users or systems",
      "mitigations": ["strong_authentication", "certificate_validation"]
    },
    "tampering": {
      "description": "Unauthorized modification of data or systems",
      "mitigations": ["integrity_checks", "digital_signatures"]
    },
    "repudiation": {
      "description": "Denial of actions by legitimate users",
      "mitigations": ["audit_logging", "non_repudiation_protocols"]
    },
    "information_disclosure": {
      "description": "Exposure of sensitive information",
      "mitigations": ["encryption", "access_controls"]
    },
    "denial_of_service": {
      "description": "Disruption of system availability",
      "mitigations": ["rate_limiting", "redundancy"]
    },
    "elevation_of_privilege": {
      "description": "Unauthorized escalation of access rights",
      "mitigations": ["least_privilege", "role_separation"]
    }
  }
}
```

#### Secure Architecture Patterns

**Defense in Depth:**
- Multiple security layers
- Diverse security controls
- Fail-safe defaults

**Zero Trust Architecture:**
- Never trust, always verify
- Micro-segmentation
- Continuous authentication

**Secure by Design Principles:**
- Principle of least privilege
- Fail-safe defaults
- Economy of mechanism
- Complete mediation
- Open design
- Separation of privilege
- Least common mechanism
- Psychological acceptability

### Phase 4: Secure Implementation

**Objective:** Develop code with security best practices.

#### Secure Coding Standards

**Input Validation:**
- Implement whitelist-based validation
- Enforce length limits and type checking
- Prevent injection attacks (SQL, XSS, command injection)
- Use parameterized queries and prepared statements

**Authentication and Authorization:**
- Implement multi-factor authentication
- Use secure password hashing (bcrypt, Argon2)
- Enforce account lockout policies
- Implement session management with timeouts

**Error Handling:**
- Avoid exposing sensitive information in error messages
- Implement comprehensive logging for security events
- Use structured error handling with proper exception management

#### Code Review Process

**Automated Code Analysis:**
```json
{
  "code_analysis_tools": {
    "static_analysis": {
      "tools": ["sonarqube", "checkmarx", "fortify"],
      "rules": {
        "severity_threshold": "high",
        "coverage_minimum": 80
      }
    },
    "dependency_scanning": {
      "tools": ["owasp_dependency_check", "snyk", "trivy"],
      "update_policy": "automated_patch_available"
    },
    "secret_detection": {
      "tools": ["gitsecrets", "trufflehog"],
      "scan_scope": ["source_code", "configuration_files", "documentation"]
    }
  }
}
```

**Manual Code Review Checklist:**
- [ ] Input validation implemented
- [ ] Authentication and authorization enforced
- [ ] Sensitive data encrypted
- [ ] Error messages don't leak information
- [ ] SQL injection protections in place
- [ ] XSS protections implemented
- [ ] CSRF protections active
- [ ] Secure defaults configured
- [ ] Logging and monitoring adequate
- [ ] Race conditions addressed

### Phase 5: Verification and Validation

**Objective:** Ensure security requirements are met through testing.

#### Security Testing Types

**Static Application Security Testing (SAST):**
```json
{
  "sast_configuration": {
    "scan_schedule": "pre_commit",
    "severity_threshold": "medium",
    "false_positive_handling": "manual_review",
    "remediation_tracking": "jira_integration",
    "coverage_requirements": {
      "critical_rules": 100,
      "high_rules": 95,
      "medium_rules": 80
    }
  }
}
```

**Dynamic Application Security Testing (DAST):**
```json
{
  "dast_configuration": {
    "test_environment": "staging",
    "scan_frequency": "weekly",
    "attack_vectors": [
      "sql_injection",
      "xss",
      "csrf",
      "broken_authentication",
      "security_misconfiguration"
    ],
    "reporting": {
      "format": "owasp_zap_xml",
      "integration": "defect_dojo"
    }
  }
}
```

**Interactive Application Security Testing (IAST):**
```json
{
  "iast_configuration": {
    "deployment": "runtime_agent",
    "monitoring": "continuous",
    "data_collection": {
      "http_requests": true,
      "database_queries": true,
      "file_operations": true,
      "system_calls": true
    },
    "alerting": {
      "real_time": true,
      "severity_levels": ["critical", "high"]
    }
  }
}
```

#### Penetration Testing

**Penetration Testing Methodology:**
- Planning: Define scope, rules of engagement, and success criteria
- Reconnaissance: Passive and active information gathering
- Vulnerability Assessment: Automated scanning with manual verification
- Exploitation: Safe exploitation with proof-of-concept development
- Reporting: Executive summary, technical details, and remediation guidance

### Phase 6: Deployment and Operations

**Objective:** Securely deploy and maintain systems.

#### Secure Deployment Practices

**Configuration Management:**
- Version control with mandatory code reviews
- Infrastructure as code with automated drift detection
- Secure secret management with rotation policies

**Container Security:**
- Use trusted base images with vulnerability scanning
- Prohibit privileged containers and root user access
- Implement RBAC and network policies in orchestration

#### Patch Management

**Patch Management Process:**
```json
{
  "patch_management": {
    "vulnerability_assessment": {
      "scan_frequency": "daily",
      "severity_threshold": "moderate",
      "exploitability_check": true
    },
    "patch_testing": {
      "test_environment": "staging",
      "regression_testing": true,
      "performance_testing": true,
      "rollback_plan": "required"
    },
    "deployment_strategy": {
      "phased_rollout": true,
      "monitoring_period": "72_hours",
      "rollback_criteria": "defined"
    },
    "compliance_reporting": {
      "patch_compliance_rate": ">95%",
      "reporting_frequency": "monthly",
      "escalation_process": "automated"
    }
  }
}
```

### Phase 7: Maintenance and Disposal

**Objective:** Maintain security throughout the system lifecycle.

#### Incident Response

**Incident Response Plan:**
- Preparation: Define team, communication plan, and tools
- Identification: Automated detection, triage, and severity classification
- Containment: Isolate systems, implement fixes, preserve evidence
- Recovery: Restore from backups, validate functionality, monitor
- Lessons Learned: Review incidents, improve processes, update knowledge base

## Best Practices

### Secure Development Governance
- Establish security champions in development teams
- Implement automated security gates in CI/CD pipelines
- Conduct regular security training and awareness programs
- Track security metrics and KPIs for continuous improvement



## References

IEC 62443-4-1 (2018). *Secure development lifecycle requirements*. Microsoft SDL (2002). OWASP ASVS (2021). NIST SP 800-64 (2012).