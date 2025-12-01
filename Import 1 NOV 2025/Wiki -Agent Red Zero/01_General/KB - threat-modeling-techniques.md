# Threat Modeling Techniques
## Comprehensive Methodologies, Templates, and Workshop Guides

**Version:** 1.0 - October 2025
**Methodologies:** STRIDE, PASTA, OCTAVE, Trike, VAST
**Purpose:** Systematic identification and mitigation of security threats
**Scope:** Complete threat modeling frameworks with n8n automation

## 🎯 Overview

Threat modeling is a structured approach to identifying, quantifying, and addressing security threats in systems, applications, and processes. It enables organizations to proactively identify vulnerabilities and implement appropriate security controls before systems are deployed or significant damage occurs.

**Related Methodologies:**
- [[MITRE ATT&CK Framework]] - Threat actor tactics and techniques
- [[MITRE EMB3D Framework]] - Threat mitigation methodology
- [[IEC 62443 Part 4]] - Secure development threat modeling
- [[Vulnerability Management]] - Threat-informed vulnerability assessment

**Implementation Areas:**
- [[Network Design]] - Network-level threat modeling
- [[Identity Management]] - Authentication threat analysis
- [[Cloud Security]] - Cloud infrastructure threat modeling
- [[Device Management]] - IoT and industrial device threats

### Core Objectives
1. **Identify Assets:** Determine what needs protection
2. **Identify Threats:** Find potential attack vectors
3. **Identify Vulnerabilities:** Discover weaknesses that threats can exploit
4. **Determine Risks:** Assess likelihood and impact of threats
5. **Mitigate Risks:** Implement appropriate security controls

### Benefits
- **Proactive Security:** Address threats before exploitation
- **Cost Efficiency:** Cheaper to fix issues early in development
- **Risk Prioritization:** Focus resources on highest-risk threats
- **Compliance:** Meet regulatory requirements for risk assessment
- **Communication:** Common language for security discussions

## 🏗️ Threat Modeling Methodologies

### STRIDE Framework
**Microsoft-developed framework focusing on six threat categories**

#### STRIDE Categories
1. **Spoofing:** Faking identity to gain unauthorized access
2. **Tampering:** Unauthorized modification of data or systems
3. **Repudiation:** Denying actions that cannot be proven otherwise
4. **Information Disclosure:** Exposure of sensitive information
5. **Denial of Service:** Making systems unavailable
6. **Elevation of Privilege:** Gaining higher access than authorized

#### STRIDE Threat Modeling Process
```javascript
// STRIDE Threat Modeling Implementation
class STRIDEThreatModeler {
  constructor() {
    this.strideCategories = {
      'Spoofing': {
        description: 'Impersonating something or someone else',
        examples: ['Identity spoofing', 'Session hijacking', 'Man-in-the-middle'],
        mitigations: ['Authentication', 'Digital signatures', 'Certificates'],
        riskWeight: 0.8
      },
      'Tampering': {
        description: 'Modifying data or code maliciously',
        examples: ['Data modification', 'Code injection', 'Parameter manipulation'],
        mitigations: ['Integrity checks', 'Hashing', 'Digital signatures'],
        riskWeight: 0.9
      },
      'Repudiation': {
        description: 'Denying an action occurred',
        examples: ['Log manipulation', 'Transaction denial', 'Action repudiation'],
        mitigations: ['Secure logging', 'Digital signatures', 'Timestamps'],
        riskWeight: 0.6
      },
      'Information Disclosure': {
        description: 'Exposing information to unauthorized parties',
        examples: ['Data leakage', 'Privacy violation', 'Information exposure'],
        mitigations: ['Encryption', 'Access controls', 'Data classification'],
        riskWeight: 0.9
      },
      'Denial of Service': {
        description: 'Making a system unavailable',
        examples: ['Resource exhaustion', 'Network flooding', 'Service disruption'],
        mitigations: ['Rate limiting', 'Resource management', 'Redundancy'],
        riskWeight: 0.7
      },
      'Elevation of Privilege': {
        description: 'Gaining higher privileges than authorized',
        examples: ['Privilege escalation', 'Role manipulation', 'Authorization bypass'],
        mitigations: ['Access controls', 'Least privilege', 'Input validation'],
        riskWeight: 0.95
      }
    };

    this.threats = new Map();
    this.mitigations = new Map();
  }

  // Create threat model for system
  async createThreatModel(systemComponents, dataFlows, trustBoundaries) {
    const model = {
      systemName: systemComponents[0]?.systemName || 'Unknown System',
      components: systemComponents,
      dataFlows: dataFlows,
      trustBoundaries: trustBoundaries,
      threats: [],
      mitigations: [],
      riskAssessment: null,
      created: new Date(),
      version: '1.0'
    };

    // Analyze each component
    for (const component of systemComponents) {
      const componentThreats = await this.analyzeComponent(component, systemComponents, dataFlows, trustBoundaries);
      model.threats.push(...componentThreats);
    }

    // Analyze data flows
    for (const flow of dataFlows) {
      const flowThreats = await this.analyzeDataFlow(flow, trustBoundaries);
      model.threats.push(...flowThreats);
    }

    // Generate mitigations
    model.mitigations = this.generateMitigations(model.threats);

    // Calculate risk assessment
    model.riskAssessment = this.calculateRiskAssessment(model.threats);

    return model;
  }

  // Analyze individual component
  async analyzeComponent(component, allComponents, dataFlows, trustBoundaries) {
    const threats = [];

    for (const [category, details] of Object.entries(this.strideCategories)) {
      // Check for applicable threats based on component type and interactions
      const applicableThreats = this.findApplicableThreats(component, category, allComponents, dataFlows, trustBoundaries);

      for (const threat of applicableThreats) {
        const threatId = this.generateThreatId();
        threats.push({
          id: threatId,
          category: category,
          component: component.name,
          title: threat.title,
          description: threat.description,
          impact: threat.impact,
          likelihood: threat.likelihood,
          riskLevel: this.calculateRiskLevel(threat.impact, threat.likelihood, details.riskWeight),
          examples: details.examples,
          mitigations: details.mitigations,
          affectedAssets: threat.affectedAssets,
          attackVectors: threat.attackVectors,
          prerequisites: threat.prerequisites,
          discovered: new Date()
        });

        this.threats.set(threatId, threats[threats.length - 1]);
      }
    }

    return threats;
  }

  // Find applicable threats for component
  findApplicableThreats(component, category, allComponents, dataFlows, trustBoundaries) {
    const threats = [];

    switch (category) {
      case 'Spoofing':
        if (component.type === 'web_service' || component.type === 'api' || component.authenticates) {
          threats.push({
            title: `Identity spoofing of ${component.name}`,
            description: `An attacker could impersonate a legitimate user or system to gain unauthorized access to ${component.name}`,
            impact: component.criticality === 'high' ? 'HIGH' : 'MEDIUM',
            likelihood: 'MEDIUM',
            affectedAssets: [component.name],
            attackVectors: ['Man-in-the-middle', 'Session hijacking', 'Credential theft'],
            prerequisites: ['Network access', 'Weak authentication']
          });
        }
        break;

      case 'Tampering':
        if (component.handlesData || component.type === 'database' || component.processesInput) {
          threats.push({
            title: `Data tampering in ${component.name}`,
            description: `An attacker could modify data processed by ${component.name}, leading to incorrect system behavior or decisions`,
            impact: component.safetyCritical ? 'CRITICAL' : 'HIGH',
            likelihood: 'MEDIUM',
            affectedAssets: [component.name, 'Data integrity'],
            attackVectors: ['SQL injection', 'Parameter manipulation', 'Buffer overflow'],
            prerequisites: ['Input validation weakness', 'Insufficient access controls']
          });
        }
        break;

      case 'Repudiation':
        if (component.logsActions || component.type === 'audit_system') {
          threats.push({
            title: `Action repudiation in ${component.name}`,
            description: `A user could deny performing actions logged by ${component.name}, potentially avoiding accountability`,
            impact: 'MEDIUM',
            likelihood: 'LOW',
            affectedAssets: ['Audit logs', 'Accountability'],
            attackVectors: ['Log manipulation', 'Session impersonation'],
            prerequisites: ['Weak logging', 'No digital signatures on logs']
          });
        }
        break;

      case 'Information Disclosure':
        const relatedFlows = dataFlows.filter(flow =>
          flow.source === component.name || flow.target === component.name
        );

        if (relatedFlows.some(flow => flow.dataType === 'sensitive' || flow.dataType === 'personal')) {
          threats.push({
            title: `Information disclosure from ${component.name}`,
            description: `Sensitive information processed by ${component.name} could be exposed to unauthorized parties`,
            impact: component.dataSensitivity === 'high' ? 'CRITICAL' : 'HIGH',
            likelihood: 'MEDIUM',
            affectedAssets: ['Sensitive data', 'Privacy'],
            attackVectors: ['Eavesdropping', 'Data leakage', 'Misconfiguration'],
            prerequisites: ['Unencrypted communications', 'Weak access controls']
          });
        }
        break;

      case 'Denial of Service':
        if (component.type === 'web_service' || component.type === 'network_device' || component.type === 'api') {
          threats.push({
            title: `Denial of service against ${component.name}`,
            description: `${component.name} could be made unavailable through resource exhaustion or service disruption`,
            impact: component.availabilityCritical ? 'CRITICAL' : 'HIGH',
            likelihood: component.publicFacing ? 'HIGH' : 'MEDIUM',
            affectedAssets: [component.name, 'Service availability'],
            attackVectors: ['Flooding attacks', 'Resource exhaustion', 'Protocol exploitation'],
            prerequisites: ['Insufficient rate limiting', 'No redundancy']
          });
        }
        break;

      case 'Elevation of Privilege':
        if (component.hasPrivileges || component.type === 'authentication_service' || component.managesAccess) {
          threats.push({
            title: `Privilege escalation in ${component.name}`,
            description: `An attacker could gain higher privileges than authorized within ${component.name}`,
            impact: 'CRITICAL',
            likelihood: 'MEDIUM',
            affectedAssets: [component.name, 'Access controls'],
            attackVectors: ['Authorization bypass', 'Role manipulation', 'Exploit chaining'],
            prerequisites: ['Complex authorization logic', 'Input validation weaknesses']
          });
        }
        break;
    }

    return threats;
  }

  // Analyze data flow threats
  async analyzeDataFlow(flow, trustBoundaries) {
    const threats = [];

    // Check if flow crosses trust boundaries
    const crossesBoundary = trustBoundaries.some(boundary =>
      (boundary.includes(flow.source) && !boundary.includes(flow.target)) ||
      (!boundary.includes(flow.source) && boundary.includes(flow.target))
    );

    if (crossesBoundary && (flow.dataType === 'sensitive' || flow.dataType === 'personal')) {
      threats.push({
        id: this.generateThreatId(),
        category: 'Information Disclosure',
        component: `${flow.source} -> ${flow.target}`,
        title: `Data exposure in transit between ${flow.source} and ${flow.target}`,
        description: `Sensitive data flowing from ${flow.source} to ${flow.target} crosses a trust boundary without adequate protection`,
        impact: flow.dataType === 'personal' ? 'CRITICAL' : 'HIGH',
        likelihood: flow.encrypted ? 'LOW' : 'HIGH',
        riskLevel: this.calculateRiskLevel(flow.dataType === 'personal' ? 'CRITICAL' : 'HIGH',
                                         flow.encrypted ? 'LOW' : 'HIGH', 0.9),
        examples: ['Network eavesdropping', 'Man-in-the-middle attacks'],
        mitigations: ['Encryption', 'Secure channels', 'VPN', 'TLS'],
        affectedAssets: ['Data in transit', 'Privacy'],
        attackVectors: ['Network sniffing', 'MITM attacks'],
        prerequisites: ['Unencrypted communication', 'Network access'],
        discovered: new Date()
      });
    }

    return threats;
  }

  // Calculate risk level
  calculateRiskLevel(impact, likelihood, weight = 1.0) {
    const impactScore = { 'LOW': 1, 'MEDIUM': 2, 'HIGH': 3, 'CRITICAL': 4 }[impact] || 2;
    const likelihoodScore = { 'LOW': 1, 'MEDIUM': 2, 'HIGH': 3 }[likelihood] || 2;

    const riskScore = (impactScore * likelihoodScore * weight);

    if (riskScore >= 10) return 'CRITICAL';
    if (riskScore >= 6) return 'HIGH';
    if (riskScore >= 3) return 'MEDIUM';
    return 'LOW';
  }

  // Generate mitigations
  generateMitigations(threats) {
    const mitigationMap = new Map();

    for (const threat of threats) {
      for (const mitigation of threat.mitigations) {
        if (!mitigationMap.has(mitigation)) {
          mitigationMap.set(mitigation, {
            mitigation: mitigation,
            addressesThreats: [],
            priority: 'LOW',
            implementationEffort: 'MEDIUM',
            effectiveness: 'HIGH'
          });
        }

        const mitigationData = mitigationMap.get(mitigation);
        mitigationData.addressesThreats.push(threat.id);

        // Update priority based on threat risk
        if (threat.riskLevel === 'CRITICAL' && mitigationData.priority !== 'CRITICAL') {
          mitigationData.priority = 'CRITICAL';
        } else if (threat.riskLevel === 'HIGH' && mitigationData.priority === 'LOW') {
          mitigationData.priority = 'HIGH';
        } else if (threat.riskLevel === 'MEDIUM' && mitigationData.priority === 'LOW') {
          mitigationData.priority = 'MEDIUM';
        }
      }
    }

    return Array.from(mitigationMap.values()).sort((a, b) => {
      const priorityOrder = { 'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1 };
      return priorityOrder[b.priority] - priorityOrder[a.priority];
    });
  }

  // Calculate risk assessment
  calculateRiskAssessment(threats) {
    const riskLevels = threats.map(t => t.riskLevel);
    const criticalCount = riskLevels.filter(r => r === 'CRITICAL').length;
    const highCount = riskLevels.filter(r => r === 'HIGH').length;
    const mediumCount = riskLevels.filter(r => r === 'MEDIUM').length;
    const lowCount = riskLevels.filter(r => r === 'LOW').length;

    let overallRisk = 'LOW';
    if (criticalCount > 0) overallRisk = 'CRITICAL';
    else if (highCount > 3) overallRisk = 'HIGH';
    else if (highCount > 0 || mediumCount > 5) overallRisk = 'MEDIUM';

    const riskScore = (criticalCount * 10) + (highCount * 5) + (mediumCount * 2) + lowCount;

    return {
      overallRisk: overallRisk,
      riskScore: riskScore,
      threatCounts: {
        total: threats.length,
        critical: criticalCount,
        high: highCount,
        medium: mediumCount,
        low: lowCount
      },
      recommendations: this.generateRiskRecommendations(overallRisk, threatCounts)
    };
  }

  // Generate risk recommendations
  generateRiskRecommendations(overallRisk, threatCounts) {
    const recommendations = [];

    if (overallRisk === 'CRITICAL') {
      recommendations.push({
        priority: 'CRITICAL',
        action: 'Immediate security review and mitigation required',
        timeframe: 'Within 24 hours',
        rationale: `${threatCounts.critical} critical threats identified`
      });
    }

    if (threatCounts.high > 0) {
      recommendations.push({
        priority: 'HIGH',
        action: 'Address high-risk threats in current sprint/iteration',
        timeframe: 'Within 1-2 weeks',
        rationale: `${threatCounts.high} high-risk threats require attention`
      });
    }

    recommendations.push({
      priority: 'MEDIUM',
      action: 'Implement threat modeling in development process',
      timeframe: 'Ongoing',
      rationale: 'Ensure systematic threat identification'
    });

    recommendations.push({
      priority: 'MEDIUM',
      action: 'Conduct security training for development team',
      timeframe: 'Within 1 month',
      rationale: 'Improve security awareness and skills'
    });

    return recommendations;
  }

  // Generate unique threat ID
  generateThreatId() {
    return `STRIDE_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  // Export threat model
  exportThreatModel(model, format = 'json') {
    switch (format) {
      case 'json':
        return JSON.stringify(model, null, 2);
      case 'xml':
        return this.convertToXML(model);
      case 'csv':
        return this.convertToCSV(model);
      default:
        return JSON.stringify(model, null, 2);
    }
  }

  // Convert to XML (simplified)
  convertToXML(model) {
    let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
    xml += '<threat-model>\n';
    xml += `  <system-name>${model.systemName}</system-name>\n`;
    xml += `  <created>${model.created.toISOString()}</created>\n`;

    xml += '  <threats>\n';
    for (const threat of model.threats) {
      xml += '    <threat>\n';
      xml += `      <id>${threat.id}</id>\n`;
      xml += `      <category>${threat.category}</category>\n`;
      xml += `      <title>${threat.title}</title>\n`;
      xml += `      <risk-level>${threat.riskLevel}</risk-level>\n`;
      xml += '    </threat>\n';
    }
    xml += '  </threats>\n';

    xml += '</threat-model>\n';
    return xml;
  }

  // Convert to CSV (simplified)
  convertToCSV(model) {
    let csv = 'ID,Category,Title,Risk Level,Component\n';

    for (const threat of model.threats) {
      csv += `${threat.id},${threat.category},"${threat.title}",${threat.riskLevel},${threat.component}\n`;
    }

    return csv;
  }
}

// Example STRIDE threat modeling
const strideModeler = new STRIDEThreatModeler();

const systemComponents = [
  {
    name: 'WebServer',
    type: 'web_service',
    handlesData: true,
    authenticates: true,
    criticality: 'high',
    publicFacing: true
  },
  {
    name: 'Database',
    type: 'database',
    handlesData: true,
    dataSensitivity: 'high',
    safetyCritical: false
  },
  {
    name: 'AuthService',
    type: 'authentication_service',
    hasPrivileges: true,
    managesAccess: true,
    criticality: 'high'
  }
];

const dataFlows = [
  {
    source: 'WebServer',
    target: 'Database',
    dataType: 'sensitive',
    encrypted: false
  },
  {
    source: 'AuthService',
    target: 'WebServer',
    dataType: 'credentials',
    encrypted: true
  }
];

const trustBoundaries = [
  ['WebServer', 'AuthService'], // Internal network
  ['Database'] // Restricted zone
];

const threatModel = await strideModeler.createThreatModel(systemComponents, dataFlows, trustBoundaries);

console.log('STRIDE Threat Model:');
console.log('===================');
console.log(`System: ${threatModel.systemName}`);
console.log(`Total Threats: ${threatModel.threats.length}`);
console.log(`Overall Risk: ${threatModel.riskAssessment.overallRisk}`);
console.log(`Risk Score: ${threatModel.riskAssessment.riskScore}`);

console.log('\nThreat Summary:');
console.log(threatModel.riskAssessment.threatCounts);

console.log('\nTop Threats:');
threatModel.threats
  .sort((a, b) => {
    const riskOrder = { 'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1 };
    return riskOrder[b.riskLevel] - riskOrder[a.riskLevel];
  })
  .slice(0, 5)
  .forEach(threat => {
    console.log(`- ${threat.category}: ${threat.title} (${threat.riskLevel})`);
  });

console.log('\nRecommended Mitigations:');
threatModel.mitigations.slice(0, 5).forEach(mitigation => {
  console.log(`- ${mitigation.mitigation} (${mitigation.priority}) - Addresses ${mitigation.addressesThreats.length} threats`);
});
```

### STRIDE Threat Modeling Template

#### Template Structure
```markdown
# STRIDE Threat Model: [System Name]

## 1. System Overview
- **System Name:** [Name]
- **Version:** [Version]
- **Date:** [Date]
- **Modeler:** [Name]
- **Reviewers:** [Names]

## 2. System Description
[Brief description of the system and its purpose]

## 3. System Components
| Component | Type | Description | Trust Level |
|-----------|------|-------------|-------------|
| [Name] | [Type] | [Description] | [Level] |

## 4. Data Flows
| Source | Target | Data Type | Protocol | Encrypted |
|--------|--------|-----------|----------|-----------|
| [Source] | [Target] | [Type] | [Protocol] | [Yes/No] |

## 5. Trust Boundaries
- **Boundary 1:** [Description]
  - Components: [List]
- **Boundary 2:** [Description]
  - Components: [List]

## 6. Threats Identified

### Spoofing Threats
| ID | Component | Threat Description | Impact | Likelihood | Risk Level | Mitigations |
|----|-----------|-------------------|--------|------------|------------|-------------|
| STRIDE_S_001 | [Component] | [Description] | [Level] | [Level] | [Level] | [List] |

### Tampering Threats
| ID | Component | Threat Description | Impact | Likelihood | Risk Level | Mitigations |
|----|-----------|-------------------|--------|------------|------------|-------------|
| STRIDE_T_001 | [Component] | [Description] | [Level] | [Level] | [Level] | [List] |

### Repudiation Threats
| ID | Component | Threat Description | Impact | Likelihood | Risk Level | Mitigations |
|----|-----------|-------------------|--------|------------|------------|-------------|
| STRIDE_R_001 | [Component] | [Description] | [Level] | [Level] | [Level] | [List] |

### Information Disclosure Threats
| ID | Component | Threat Description | Impact | Likelihood | Risk Level | Mitigations |
|----|-----------|-------------------|--------|------------|------------|-------------|
| STRIDE_I_001 | [Component] | [Description] | [Level] | [Level] | [Level] | [List] |

### Denial of Service Threats
| ID | Component | Threat Description | Impact | Likelihood | Risk Level | Mitigations |
|----|-----------|-------------------|--------|------------|------------|-------------|
| STRIDE_D_001 | [Component] | [Description] | [Level] | [Level] | [Level] | [List] |

### Elevation of Privilege Threats
| ID | Component | Threat Description | Impact | Likelihood | Risk Level | Mitigations |
|----|-----------|-------------------|--------|------------|------------|-------------|
| STRIDE_E_001 | [Component] | [Description] | [Level] | [Level] | [Level] | [List] |

## 7. Risk Assessment
- **Overall Risk Level:** [Level]
- **Risk Score:** [Score]
- **Critical Threats:** [Count]
- **High Threats:** [Count]
- **Medium Threats:** [Count]
- **Low Threats:** [Count]

## 8. Mitigation Strategy
### Priority 1 (Critical) - Implement Immediately
1. [Mitigation 1]
2. [Mitigation 2]

### Priority 2 (High) - Implement This Sprint
1. [Mitigation 1]
2. [Mitigation 2]

### Priority 3 (Medium) - Plan for Next Sprint
1. [Mitigation 1]
2. [Mitigation 2]

## 9. Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

## 10. Next Steps
- [Step 1]
- [Step 2]
- [Step 3]

## 11. Review and Approval
- **Model Reviewed By:** [Name] on [Date]
- **Approved By:** [Name] on [Date]
- **Next Review Date:** [Date]
```

### PASTA Framework

**Process for Attack Simulation and Threat Analysis - Risk-centric threat modeling**

#### PASTA Methodology
```javascript
// PASTA Threat Modeling Implementation
class PASTAThreatModeler {
  constructor() {
    this.phases = {
      1: 'Define Business Objectives',
      2: 'Define Technical Scope',
      3: 'Application Decomposition',
      4: 'Threat Analysis',
      5: 'Vulnerability Analysis',
      6: 'Attack Modeling',
      7: 'Risk Analysis',
      8: 'Residual Risk Analysis'
    };

    this.riskFactors = {
      likelihood: {
        'Very Low': 1,
        'Low': 2,
        'Medium': 3,
        'High': 4,
        'Very High': 5
      },
      impact: {
        'Very Low': 1,
        'Low': 2,
        'Medium': 3,
        'High': 4,
        'Very High': 5
      },
      exploitability: {
        'Very Difficult': 1,
        'Difficult': 2,
        'Moderate': 3,
        'Easy': 4,
        'Very Easy': 5
      }
    };
  }

  // Execute PASTA methodology
  async executePASTA(applicationData, businessObjectives) {
    const pastaModel = {
      applicationName: applicationData.name,
      businessObjectives: businessObjectives,
      phases: {},
      finalRiskAssessment: null,
      recommendations: [],
      created: new Date()
    };

    // Phase 1: Define Business Objectives
    pastaModel.phases[1] = await this.defineBusinessObjectives(businessObjectives);

    // Phase 2: Define Technical Scope
    pastaModel.phases[2] = await this.defineTechnicalScope(applicationData);

    // Phase 3: Application Decomposition
    pastaModel.phases[3] = await this.applicationDecomposition(applicationData);

    // Phase 4: Threat Analysis
    pastaModel.phases[4] = await this.threatAnalysis(pastaModel.phases[3]);

    // Phase 5: Vulnerability Analysis
    pastaModel.phases[5] = await this.vulnerabilityAnalysis(pastaModel.phases[4], pastaModel.phases[3]);

    // Phase 6: Attack Modeling
    pastaModel.phases[6] = await this.attackModeling(pastaModel.phases[5]);

    // Phase 7: Risk Analysis
    pastaModel.phases[7] = await this.riskAnalysis(pastaModel.phases[6]);

    // Phase 8: Residual Risk Analysis
    pastaModel.phases[8] = await this.residualRiskAnalysis(pastaModel.phases[7]);

    // Generate final assessment
    pastaModel.finalRiskAssessment = this.generateFinalAssessment(pastaModel);
    pastaModel.recommendations = this.generateRecommendations(pastaModel);

    return pastaModel;
  }

  // Phase 1: Define Business Objectives
  async defineBusinessObjectives(objectives) {
    return {
      phase: 1,
      name: this.phases[1],
      objectives: objectives,
      securityObjectives: this.deriveSecurityObjectives(objectives),
      complianceRequirements: this.identifyComplianceRequirements(objectives),
      completed: new Date()
    };
  }

  // Derive security objectives from business objectives
  deriveSecurityObjectives(businessObjectives) {
    const securityObjectives = [];

    for (const objective of businessObjectives) {
      switch (objective.type) {
        case 'confidentiality':
          securityObjectives.push({
            type: 'Protect sensitive data',
            priority: objective.priority,
            rationale: `Business requires ${objective.description}`
          });
          break;
        case 'availability':
          securityObjectives.push({
            type: 'Ensure system availability',
            priority: objective.priority,
            rationale: `Business requires ${objective.description}`
          });
          break;
        case 'integrity':
          securityObjectives.push({
            type: 'Maintain data integrity',
            priority: objective.priority,
            rationale: `Business requires ${objective.description}`
          });
          break;
        case 'compliance':
          securityObjectives.push({
            type: 'Meet compliance requirements',
            priority: objective.priority,
            rationale: `Business requires ${objective.description}`
          });
          break;
      }
    }

    return securityObjectives;
  }

  // Phase 2: Define Technical Scope
  async defineTechnicalScope(applicationData) {
    return {
      phase: 2,
      name: this.phases[2],
      inScope: {
        components: applicationData.components,
        dataFlows: applicationData.dataFlows,
        trustBoundaries: applicationData.trustBoundaries,
        technologies: applicationData.technologies
      },
      outOfScope: applicationData.outOfScope || [],
      assumptions: applicationData.assumptions || [],
      constraints: applicationData.constraints || [],
      completed: new Date()
    };
  }

  // Phase 3: Application Decomposition
  async applicationDecomposition(applicationData) {
    const decomposition = {
      phase: 3,
      name: this.phases[3],
      entryPoints: [],
      exitPoints: [],
      trustLevels: [],
      dataFlows: [],
      privilegeLevels: [],
      completed: new Date()
    };

    // Identify entry points
    decomposition.entryPoints = this.identifyEntryPoints(applicationData);

    // Identify exit points
    decomposition.exitPoints = this.identifyExitPoints(applicationData);

    // Define trust levels
    decomposition.trustLevels = this.defineTrustLevels(applicationData);

    // Analyze data flows
    decomposition.dataFlows = this.analyzeDataFlows(applicationData);

    // Define privilege levels
    decomposition.privilegeLevels = this.definePrivilegeLevels(applicationData);

    return decomposition;
  }

  // Identify entry points
  identifyEntryPoints(applicationData) {
    const entryPoints = [];

    for (const component of applicationData.components) {
      if (component.type === 'web_interface' || component.type === 'api_endpoint') {
        entryPoints.push({
          component: component.name,
          type: component.type,
          authentication: component.authentication || 'none',
          inputValidation: component.inputValidation || 'basic'
        });
      }
    }

    return entryPoints;
  }

  // Identify exit points
  identifyExitPoints(applicationData) {
    const exitPoints = [];

    for (const component of applicationData.components) {
      if (component.outputsData || component.type === 'database' || component.type === 'external_service') {
        exitPoints.push({
          component: component.name,
          type: component.type,
          dataSensitivity: component.dataSensitivity || 'low',
          encryption: component.encryption || false
        });
      }
    }

    return exitPoints;
  }

  // Define trust levels
  defineTrustLevels(applicationData) {
    const trustLevels = [
      {
        level: 'Internet',
        components: applicationData.components.filter(c => c.publicFacing).map(c => c.name),
        permissions: ['anonymous_access']
      },
      {
        level: 'DMZ',
        components: applicationData.components.filter(c => c.inDMZ).map(c => c.name),
        permissions: ['authenticated_access']
      },
      {
        level: 'Internal',
        components: applicationData.components.filter(c => c.internal).map(c => c.name),
        permissions: ['authorized_access']
      },
      {
        level: 'Restricted',
        components: applicationData.components.filter(c => c.restricted).map(c => c.name),
        permissions: ['privileged_access']
      }
    ];

    return trustLevels.filter(tl => tl.components.length > 0);
  }

  // Analyze data flows
  analyzeDataFlows(applicationData) {
    return applicationData.dataFlows.map(flow => ({
      source: flow.source,
      target: flow.target,
      dataType: flow.dataType,
      sensitivity: flow.sensitivity || 'low',
      encryption: flow.encrypted || false,
      authentication: flow.authenticated || false,
      integrity: flow.integrityChecked || false
    }));
  }

  // Define privilege levels
  definePrivilegeLevels(applicationData) {
    return [
      {
        level: 'Anonymous',
        permissions: ['read_public'],
        users: ['unauthenticated_users']
      },
      {
        level: 'User',
        permissions: ['read_public', 'read_private', 'modify_own'],
        users: ['authenticated_users']
      },
      {
        level: 'Administrator',
        permissions: ['read_all', 'modify_all', 'admin_functions'],
        users: ['system_administrators']
      }
    ];
  }

  // Phase 4: Threat Analysis
  async threatAnalysis(decomposition) {
    const threatAnalysis = {
      phase: 4,
      name: this.phases[4],
      threats: [],
      threatActors: [],
      attackVectors: [],
      completed: new Date()
    };

    // Identify threat actors
    threatAnalysis.threatActors = this.identifyThreatActors(decomposition);

    // Identify attack vectors
    threatAnalysis.attackVectors = this.identifyAttackVectors(decomposition);

    // Generate threats
    threatAnalysis.threats = this.generateThreats(decomposition, threatAnalysis.threatActors, threatAnalysis.attackVectors);

    return threatAnalysis;
  }

  // Identify threat actors
  identifyThreatActors(decomposition) {
    const actors = [
      {
        name: 'External Attacker',
        motivation: 'Data theft, disruption',
        capabilities: 'Network access, basic tools',
        access: decomposition.trustLevels.find(tl => tl.level === 'Internet')
      },
      {
        name: 'Insider Threat',
        motivation: 'Data theft, sabotage',
        capabilities: 'Internal access, system knowledge',
        access: decomposition.trustLevels.find(tl => tl.level === 'Internal')
      },
      {
        name: 'Advanced Persistent Threat',
        motivation: 'Espionage, long-term access',
        capabilities: 'Advanced tools, zero-day exploits',
        access: 'All trust levels'
      },
      {
        name: 'Script Kiddie',
        motivation: 'Notoriety, learning',
        capabilities: 'Automated tools, basic skills',
        access: decomposition.trustLevels.find(tl => tl.level === 'Internet')
      }
    ];

    return actors;
  }

  // Identify attack vectors
  identifyAttackVectors(decomposition) {
    const vectors = [];

    // Analyze entry points for attack vectors
    for (const entryPoint of decomposition.entryPoints) {
      vectors.push({
        type: 'Entry Point Attack',
        target: entryPoint.component,
        methods: this.getEntryPointAttackMethods(entryPoint),
        prerequisites: this.getEntryPointPrerequisites(entryPoint)
      });
    }

    // Analyze data flows for attack vectors
    for (const flow of decomposition.dataFlows) {
      if (!flow.encryption || !flow.authentication) {
        vectors.push({
          type: 'Data Flow Interception',
          target: `${flow.source} -> ${flow.target}`,
          methods: ['Man-in-the-middle', 'Eavesdropping', 'Replay attacks'],
          prerequisites: ['Network access', 'Unencrypted communication']
        });
      }
    }

    return vectors;
  }

  // Generate threats
  generateThreats(decomposition, threatActors, attackVectors) {
    const threats = [];

    for (const actor of threatActors) {
      for (const vector of attackVectors) {
        if (this.canActorUseVector(actor, vector)) {
          threats.push({
            id: this.generateThreatId(),
            actor: actor.name,
            vector: vector.type,
            target: vector.target,
            description: `${actor.name} could exploit ${vector.type} against ${vector.target}`,
            impact: this.calculateThreatImpact(actor, vector, decomposition),
            likelihood: this.calculateThreatLikelihood(actor, vector),
            methods: vector.methods,
            prerequisites: vector.prerequisites
          });
        }
      }
    }

    return threats;
  }

  // Check if actor can use vector
  canActorUseVector(actor, vector) {
    // Simplified logic - in practice, this would be more complex
    return actor.access === 'All trust levels' ||
           actor.access?.level === vector.target.split(' ')[0]; // Rough matching
  }

  // Calculate threat impact
  calculateThreatImpact(actor, vector, decomposition) {
    let impact = 'Low';

    // Check if target is critical
    const targetComponent = decomposition.entryPoints.find(ep => ep.component === vector.target) ||
                           decomposition.exitPoints.find(ep => ep.component === vector.target);

    if (targetComponent) {
      if (targetComponent.dataSensitivity === 'high' || targetComponent.critical) {
        impact = 'High';
      } else if (targetComponent.dataSensitivity === 'medium') {
        impact = 'Medium';
      }
    }

    // Increase impact for advanced actors
    if (actor.name === 'Advanced Persistent Threat') {
      impact = impact === 'High' ? 'Critical' : 'High';
    }

    return impact;
  }

  // Calculate threat likelihood
  calculateThreatLikelihood(actor, vector) {
    let likelihood = 'Low';

    // Base likelihood on actor motivation and capabilities
    if (actor.capabilities.includes('Advanced tools')) {
      likelihood = 'High';
    } else if (actor.capabilities.includes('basic tools')) {
      likelihood = 'Medium';
    }

    // Adjust based on prerequisites
    if (vector.prerequisites.includes('Network access')) {
      likelihood = 'High'; // Easy to achieve
    }

    return likelihood;
  }

  // Phase 5: Vulnerability Analysis
  async vulnerabilityAnalysis(threatAnalysis, decomposition) {
    const vulnerabilityAnalysis = {
      phase: 5,
      name: this.phases[5],
      vulnerabilities: [],
      correlations: [],
      completed: new Date()
    };

    // Identify vulnerabilities
    vulnerabilityAnalysis.vulnerabilities = await this.identifyVulnerabilities(decomposition);

    // Correlate threats with vulnerabilities
    vulnerabilityAnalysis.correlations = this.correlateThreatsVulnerabilities(
      threatAnalysis.threats,
      vulnerabilityAnalysis.vulnerabilities
    );

    return vulnerabilityAnalysis;
  }

  // Identify vulnerabilities
  async identifyVulnerabilities(decomposition) {
    const vulnerabilities = [];

    // Check entry points for vulnerabilities
    for (const entryPoint of decomposition.entryPoints) {
      if (!entryPoint.inputValidation || entryPoint.inputValidation === 'none') {
        vulnerabilities.push({
          id: this.generateVulnerabilityId(),
          component: entryPoint.component,
          type: 'Input Validation',
          severity: 'High',
          description: 'Insufficient input validation could allow injection attacks',
          cwe: 'CWE-20'
        });
      }

      if (!entryPoint.authentication || entryPoint.authentication === 'none') {
        vulnerabilities.push({
          id: this.generateVulnerabilityId(),
          component: entryPoint.component,
          type: 'Authentication',
          severity: 'Critical',
          description: 'Missing authentication allows unauthorized access',
          cwe: 'CWE-306'
        });
      }
    }

    // Check data flows for vulnerabilities
    for (const flow of decomposition.dataFlows) {
      if (!flow.encryption) {
        vulnerabilities.push({
          id: this.generateVulnerabilityId(),
          component: `${flow.source} -> ${flow.target}`,
          type: 'Data Transmission',
          severity: 'High',
          description: 'Unencrypted data transmission vulnerable to interception',
          cwe: 'CWE-319'
        });
      }
    }

    return vulnerabilities;
  }

  // Correlate threats with vulnerabilities
  correlateThreatsVulnerabilities(threats, vulnerabilities) {
    const correlations = [];

    for (const threat of threats) {
      for (const vulnerability of vulnerabilities) {
        if (this.threatExploitsVulnerability(threat, vulnerability)) {
          correlations.push({
            threatId: threat.id,
            vulnerabilityId: vulnerability.id,
            exploitability: this.calculateExploitability(threat, vulnerability),
            attackPath: this.describeAttackPath(threat, vulnerability)
          });
        }
      }
    }

    return correlations;
  }

  // Check if threat can exploit vulnerability
  threatExploitsVulnerability(threat, vulnerability) {
    // Simplified correlation logic
    return threat.target === vulnerability.component ||
           vulnerability.component.includes(threat.target);
  }

  // Calculate exploitability
  calculateExploitability(threat, vulnerability) {
    const threatSkill = { 'Low': 1, 'Medium': 2, 'High': 3 }[threat.likelihood] || 2;
    const vulnSeverity = { 'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4 }[vulnerability.severity] || 2;

    const exploitability = threatSkill * vulnSeverity;

    if (exploitability >= 8) return 'Very Easy';
    if (exploitability >= 5) return 'Easy';
    if (exploitability >= 3) return 'Moderate';
    if (exploitability >= 2) return 'Difficult';
    return 'Very Difficult';
  }

  // Phase 6: Attack Modeling
  async attackModeling(vulnerabilityAnalysis) {
    const attackModeling = {
      phase: 6,
      name: this.phases[6],
      attackScenarios: [],
      attackTrees: [],
      completed: new Date()
    };

    // Generate attack scenarios
    attackModeling.attackScenarios = this.generateAttackScenarios(vulnerabilityAnalysis);

    // Build attack trees
    attackModeling.attackTrees = this.buildAttackTrees(attackModeling.attackScenarios);

    return attackModeling;
  }

  // Generate attack scenarios
  generateAttackScenarios(vulnerabilityAnalysis) {
    const scenarios = [];

    for (const correlation of vulnerabilityAnalysis.correlations) {
      const threat = vulnerabilityAnalysis.threats.find(t => t.id === correlation.threatId);
      const vulnerability = vulnerabilityAnalysis.vulnerabilities.find(v => v.id === correlation.vulnerabilityId);

      if (threat && vulnerability) {
        scenarios.push({
          id: this.generateScenarioId(),
          name: `${threat.actor} exploits ${vulnerability.type} in ${threat.target}`,
          threat: threat,
          vulnerability: vulnerability,
          exploitability: correlation.exploitability,
          attackPath: correlation.attackPath,
          prerequisites: [...threat.prerequisites, ...this.getVulnerabilityPrerequisites(vulnerability)],
          successProbability: this.calculateSuccessProbability(correlation.exploitability),
          detectionDifficulty: this.calculateDetectionDifficulty(threat, vulnerability)
        });
      }
    }

    return scenarios;
  }

  // Build attack trees
  buildAttackTrees(scenarios) {
    const trees = [];

    for (const scenario of scenarios) {
      trees.push({
        root: scenario.name,
        children: [
          {
            node: 'Gain Access',
            children: scenario.prerequisites.map(prereq => ({ node: prereq, children: [] }))
          },
          {
            node: 'Exploit Vulnerability',
            children: [
              { node: `Exploit ${scenario.vulnerability.type}`, children: [] },
              { node: `Use ${scenario.threat.vector}`, children: [] }
            ]
          },
          {
            node: 'Achieve Objective',
            children: [
              { node: scenario.threat.description, children: [] }
            ]
          }
        ]
      });
    }

    return trees;
  }

  // Phase 7: Risk Analysis
  async riskAnalysis(attackModeling) {
    const riskAnalysis = {
      phase: 7,
      name: this.phases[7],
      riskAssessments: [],
      riskMetrics: {},
      completed: new Date()
    };

    // Assess risk for each scenario
    for (const scenario of attackModeling.attackScenarios) {
      riskAnalysis.riskAssessments.push(this.assessScenarioRisk(scenario));
    }

    // Calculate aggregate risk metrics
    riskAnalysis.riskMetrics = this.calculateRiskMetrics(riskAnalysis.riskAssessments);

    return riskAnalysis;
  }

  // Assess risk for individual scenario
  assessScenarioRisk(scenario) {
    const likelihoodScore = this.riskFactors.likelihood[scenario.threat.likelihood] || 3;
    const impactScore = this.riskFactors.impact[scenario.threat.impact] || 3;
    const exploitabilityScore = this.riskFactors.exploitability[scenario.exploitability] || 3;

    const riskScore = (likelihoodScore * impactScore * exploitabilityScore) / 27; // Normalize to 0-1

    return {
      scenarioId: scenario.id,
      scenarioName: scenario.name,
      likelihood: scenario.threat.likelihood,
      impact: scenario.threat.impact,
      exploitability: scenario.exploitability,
      riskScore: riskScore,
      riskLevel: this.getRiskLevel(riskScore),
      mitigationPriority: this.getMitigationPriority(riskScore)
    };
  }

  // Get risk level from score
  getRiskLevel(score) {
    if (score >= 0.8) return 'Critical';
    if (score >= 0.6) return 'High';
    if (score >= 0.4) return 'Medium';
    if (score >= 0.2) return 'Low';
    return 'Very Low';
  }

  // Get mitigation priority
  getMitigationPriority(score) {
    if (score >= 0.8) return 'Immediate';
    if (score >= 0.6) return 'High';
    if (score >= 0.4) return 'Medium';
    return 'Low';
  }

  // Calculate aggregate risk metrics
  calculateRiskMetrics(assessments) {
    const metrics = {
      totalScenarios: assessments.length,
      criticalRisks: assessments.filter(a => a.riskLevel === 'Critical').length,
      highRisks: assessments.filter(a => a.riskLevel === 'High').length,
      mediumRisks: assessments.filter(a => a.riskLevel === 'Medium').length,
      lowRisks: assessments.filter(a => a.riskLevel === 'Low').length,
      averageRiskScore: assessments.reduce((sum, a) => sum + a.riskScore, 0) / assessments.length,
      maxRiskScore: Math.max(...assessments.map(a => a.riskScore)),
      overallRiskLevel: this.getOverallRiskLevel(assessments)
    };

    return metrics;
  }

  // Get overall risk level
  getOverallRiskLevel(assessments) {
    const criticalCount = assessments.filter(a => a.riskLevel === 'Critical').length;
    const highCount = assessments.filter(a => a.riskLevel === 'High').length;

    if (criticalCount > 0) return 'Critical';
    if (highCount > 3) return 'High';
    if (highCount > 0) return 'Medium';
    return 'Low';
  }

  // Phase 8: Residual Risk Analysis
  async residualRiskAnalysis(riskAnalysis) {
    const residualAnalysis = {
      phase: 8,
      name: this.phases[8],
      residualRisks: [],
      riskMitigationEffectiveness: {},
      completed: new Date()
    };

    // Analyze residual risks after mitigations
    residualAnalysis.residualRisks = this.analyzeResidualRisks(riskAnalysis.riskAssessments);

    // Assess mitigation effectiveness
    residualAnalysis.riskMitigationEffectiveness = this.assessMitigationEffectiveness(riskAnalysis.riskAssessments, residualAnalysis.residualRisks);

    return residualAnalysis;
  }

  // Analyze residual risks
  analyzeResidualRisks(originalAssessments) {
    // Simulate mitigation effects (in practice, this would be based on actual mitigations)
    return originalAssessments.map(assessment => ({
      ...assessment,
      residualRiskScore: assessment.riskScore * 0.3, // Assume 70% risk reduction
      residualRiskLevel: this.getRiskLevel(assessment.riskScore * 0.3),
      mitigationEffectiveness: 'High'
    }));
  }

  // Assess mitigation effectiveness
  assessMitigationEffectiveness(original, residual) {
    const effectiveness = {
      averageRiskReduction: 0,
      effectiveMitigations: 0,
      ineffectiveMitigations: 0
    };

    for (let i = 0; i < original.length; i++) {
      const reduction = original[i].riskScore - residual[i].residualRiskScore;
      effectiveness.averageRiskReduction += reduction;

      if (reduction > 0.5) {
        effectiveness.effectiveMitigations++;
      } else if (reduction < 0.1) {
        effectiveness.ineffectiveMitigations++;
      }
    }

    effectiveness.averageRiskReduction /= original.length;

    return effectiveness;
  }

  // Generate final assessment
  generateFinalAssessment(pastaModel) {
    const phase7 = pastaModel.phases[7];
    const phase8 = pastaModel.phases[8];

    return {
      overallRiskLevel: phase7.riskMetrics.overallRiskLevel,
      residualRiskLevel: this.getOverallRiskLevel(phase8.residualRisks),
      riskReduction: phase8.riskMitigationEffectiveness.averageRiskReduction,
      keyFindings: this.extractKeyFindings(pastaModel),
      riskTrends: this.analyzeRiskTrends(pastaModel)
    };
  }

  // Generate recommendations
  generateRecommendations(pastaModel) {
    const recommendations = [];
    const assessment = pastaModel.finalRiskAssessment;

    if (assessment.overallRiskLevel === 'Critical') {
      recommendations.push({
        priority: 'Critical',
        category: 'Immediate Action',
        recommendation: 'Implement compensating controls for critical risks',
        timeframe: 'Immediate',
        rationale: 'Critical risks require immediate attention'
      });
    }

    if (assessment.residualRiskLevel !== 'Low') {
      recommendations.push({
        priority: 'High',
        category: 'Risk Mitigation',
        recommendation: 'Enhance mitigation strategies for residual risks',
        timeframe: 'Short-term',
        rationale: 'Residual risks indicate incomplete mitigation'
      });
    }

    recommendations.push({
      priority: 'Medium',
      category: 'Process Improvement',
      recommendation: 'Integrate PASTA threat modeling into development lifecycle',
      timeframe: 'Medium-term',
      rationale: 'Systematic threat modeling improves security posture'
    });

    recommendations.push({
      priority: 'Medium',
      category: 'Training',
      recommendation: 'Provide security awareness training for development teams',
      timeframe: 'Ongoing',
      rationale: 'Knowledge transfer improves threat identification'
    });

    return recommendations;
  }

  // Utility methods
  generateThreatId() {
    return `PASTA_THREAT_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  generateVulnerabilityId() {
    return `PASTA_VULN_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  generateScenarioId() {
    return `PASTA_SCENARIO_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  getEntryPointAttackMethods(entryPoint) {
    const methods = ['SQL Injection', 'XSS', 'CSRF'];

    if (entryPoint.type === 'api_endpoint') {
      methods.push('API Abuse', 'Parameter Tampering');
    }

    return methods;
  }

  getEntryPointPrerequisites(entryPoint) {
    const prerequisites = ['Network access'];

    if (entryPoint.authentication !== 'none') {
      prerequisites.push('Valid credentials or authentication bypass');
    }

    return prerequisites;
  }

  getVulnerabilityPrerequisites(vulnerability) {
    const prerequisites = {
      'Input Validation': ['Malicious input', 'Validation bypass'],
      'Authentication': ['Valid credentials or bypass method'],
      'Data Transmission': ['Network interception capability']
    };

    return prerequisites[vulnerability.type] || [];
  }

  calculateSuccessProbability(exploitability) {
    const probabilities = {
      'Very Easy': 0.9,
      'Easy': 0.7,
      'Moderate': 0.5,
      'Difficult': 0.3,
      'Very Difficult': 0.1
    };

    return probabilities[exploitability] || 0.5;
  }

  calculateDetectionDifficulty(threat, vulnerability) {
    // Simplified calculation
    if (threat.likelihood === 'Low' && vulnerability.severity === 'Low') {
      return 'Easy';
    }
    if (threat.likelihood === 'High' || vulnerability.severity === 'Critical') {
      return 'Difficult';
    }
    return 'Moderate';
  }

  describeAttackPath(threat, vulnerability) {
    return `${threat.actor} uses ${threat.vector} to exploit ${vulnerability.type} vulnerability in ${threat.target}`;
  }

  extractKeyFindings(pastaModel) {
    const findings = [];

    const metrics = pastaModel.phases[7].riskMetrics;

    if (metrics.criticalRisks > 0) {
      findings.push(`${metrics.criticalRisks} critical risk scenarios identified`);
    }

    if (metrics.averageRiskScore > 0.6) {
      findings.push(`High average risk score of ${metrics.averageRiskScore.toFixed(2)}`);
    }

    findings.push(`${metrics.totalScenarios} attack scenarios analyzed`);

    return findings;
  }

  analyzeRiskTrends(pastaModel) {
    // Simplified trend analysis
    const originalRisk = pastaModel.phases[7].riskMetrics.averageRiskScore;
    const residualRisk = pastaModel.finalRiskAssessment.residualRiskLevel;

    return {
      riskReduction: originalRisk - (originalRisk * 0.3), // Based on our simulation
      trend: 'Improving',
      confidence: 'Medium'
    };
  }
}

// Example PASTA threat modeling
const pastaModeler = new PASTAThreatModeler();

const applicationData = {
  name: 'E-Commerce Platform',
  components: [
    { name: 'WebFrontend', type: 'web_interface', publicFacing: true, authentication: 'session', inputValidation: 'basic' },
    { name: 'APIServer', type: 'api_endpoint', internal: true, authentication: 'token', inputValidation: 'advanced' },
    { name: 'Database', type: 'database', restricted: true, dataSensitivity: 'high' },
    { name: 'PaymentService', type: 'external_service', inDMZ: true, critical: true }
  ],
  dataFlows: [
    { source: 'WebFrontend', target: 'APIServer', dataType: 'user_input', sensitivity: 'medium', encrypted: false },
    { source: 'APIServer', target: 'Database', dataType: 'personal', sensitivity: 'high', encrypted: true },
    { source: 'PaymentService', target: 'Database', dataType: 'financial', sensitivity: 'critical', encrypted: true }
  ],
  trustBoundaries: [
    { level: 'Internet', components: ['WebFrontend'] },
    { level: 'DMZ', components: ['PaymentService'] },
    { level: 'Internal', components: ['APIServer'] },
    { level: 'Restricted', components: ['Database'] }
  ],
  technologies: ['React', 'Node.js', 'PostgreSQL', 'Stripe API'],
  outOfScope: ['Third-party services', 'Mobile applications'],
  assumptions: ['Users have modern browsers', 'Network is trusted'],
  constraints: ['Legacy database cannot be changed', 'Budget limitations']
};

const businessObjectives = [
  { type: 'confidentiality', description: 'Protect customer payment information', priority: 'high' },
  { type: 'availability', description: 'Ensure 99.9% uptime for e-commerce operations', priority: 'high' },
  { type: 'integrity', description: 'Maintain accurate order and transaction data', priority: 'medium' },
  { type: 'compliance', description: 'Meet PCI DSS requirements', priority: 'high' }
];

const pastaModel = await pastaModeler.executePASTA(applicationData, businessObjectives);

console.log('PASTA Threat Model Results:');
console.log('===========================');
console.log(`Application: ${pastaModel.applicationName}`);
console.log(`Overall Risk Level: ${pastaModel.finalRiskAssessment.overallRiskLevel}`);
console.log(`Residual Risk Level: ${pastaModel.finalRiskAssessment.residualRiskLevel}`);
console.log(`Risk Reduction: ${(pastaModel.finalRiskAssessment.riskReduction * 100).toFixed(1)}%`);

console.log('\nKey Findings:');
pastaModel.finalRiskAssessment.keyFindings.forEach(finding => {
  console.log(`- ${finding}`);
});

console.log('\nTop Recommendations:');
pastaModel.recommendations.slice(0, 3).forEach(rec => {
  console.log(`- ${rec.priority}: ${rec.recommendation}`);
});
```

### OCTAVE Framework

**Operationally Critical Threat, Asset, and Vulnerability Evaluation - Self-directed risk assessment**

#### OCTAVE Methodology
```javascript
// OCTAVE Threat Modeling Implementation
class OCTAVEThreatModeler {
  constructor() {
    this.phases = {
      1: 'Build Asset-Based Threat Profiles',
      2: 'Identify Infrastructure Vulnerabilities',
      3: 'Develop Security Strategy and Plans'
    };

    this.workshops = {
      1: 'Strategic Assessment',
      2: 'Technology Assessment',
      3: 'Risk Assessment'
    };
  }

  // Execute OCTAVE methodology
  async executeOCTAVE(organizationData, participants) {
    const octaveModel = {
      organizationName: organizationData.name,
      participants: participants,
      phases: {},
      workshops: {},
      finalStrategy: null,
      created: new Date()
    };

    // Phase 1: Build Asset-Based Threat Profiles
    octaveModel.phases[1] = await this.buildAssetProfiles(organizationData);

    // Workshop 1: Strategic Assessment
    octaveModel.workshops[1] = await this.conductStrategicAssessment(octaveModel.phases[1], participants);

    // Phase 2: Identify Infrastructure Vulnerabilities
    octaveModel.phases[2] = await this.identifyInfrastructureVulnerabilities(octaveModel.phases[1]);

    // Workshop 2: Technology Assessment
    octaveModel.workshops[2] = await this.conductTechnologyAssessment(octaveModel.phases[2], participants);

    // Phase 3: Develop Security Strategy and Plans
    octaveModel.phases[3] = await this.developSecurityStrategy(octaveModel.phases[1], octaveModel.phases[2]);

    // Workshop 3: Risk Assessment
    octaveModel.workshops[3] = await this.conductRiskAssessment(octaveModel.phases[3], participants);

    // Generate final security strategy
    octaveModel.finalStrategy = this.generateFinalStrategy(octaveModel);

    return octaveModel;
  }

  // Phase 1: Build Asset-Based Threat Profiles
  async buildAssetProfiles(organizationData) {
    const profiles = {
      phase: 1,
      name: this.phases[1],
      criticalAssets: [],
      threatProfiles: [],
      completed: new Date()
    };

    // Identify critical assets
    profiles.criticalAssets = await this.identifyCriticalAssets(organizationData);

    // Build threat profiles for each asset
    for (const asset of profiles.criticalAssets) {
      const threatProfile = await this.buildThreatProfile(asset, organizationData);
      profiles.threatProfiles.push(threatProfile);
    }

    return profiles;
  }

  // Identify critical assets
  async identifyCriticalAssets(organizationData) {
    const assets = [];

    // Analyze business processes
    for (const process of organizationData.businessProcesses) {
      const processAssets = await this.extractAssetsFromProcess(process);
      assets.push(...processAssets);
    }

    // Analyze information assets
    for (const infoAsset of organizationData.informationAssets) {
      if (this.isCriticalInformationAsset(infoAsset)) {
        assets.push({
          id: this.generateAssetId(),
          name: infoAsset.name,
          type: 'information',
          criticality: infoAsset.criticality,
          value: infoAsset.value,
          dependencies: infoAsset.dependencies || []
        });
      }
    }

    // Remove duplicates and sort by criticality
    const uniqueAssets = this.deduplicateAssets(assets);
    return uniqueAssets.sort((a, b) => b.criticality - a.criticality);
  }

  // Extract assets from business process
  async extractAssetsFromProcess(process) {
    const assets = [];

    // Extract technology assets
    if (process.technologyAssets) {
      for (const techAsset of process.technologyAssets) {
        assets.push({
          id: this.generateAssetId(),
          name: techAsset.name,
          type: 'technology',
          criticality: process.criticality,
          value: techAsset.value,
          process: process.name
        });
      }
    }

    // Extract information assets
    if (process.informationAssets) {
      for (const infoAsset of process.informationAssets) {
        assets.push({
          id: this.generateAssetId(),
          name: infoAsset.name,
          type: 'information',
          criticality: process.criticality,
          value: infoAsset.value,
          process: process.name
        });
      }
    }

    return assets;
  }

  // Check if information asset is critical
  isCriticalInformationAsset(asset) {
    return asset.criticality >= 7 ||
           asset.sensitivity === 'high' ||
           asset.regulatory === true;
  }

  // Build threat profile for asset
  async buildThreatProfile(asset, organizationData) {
    const profile = {
      assetId: asset.id,
      assetName: asset.name,
      threatActors: [],
      threatActions: [],
      impactAreas: [],
      likelihoodFactors: []
    };

    // Identify relevant threat actors
    profile.threatActors = this.identifyThreatActorsForAsset(asset, organizationData);

    // Identify possible threat actions
    profile.threatActions = this.identifyThreatActionsForAsset(asset, profile.threatActors);

    // Assess impact areas
    profile.impactAreas = this.assessImpactAreas(asset);

    // Evaluate likelihood factors
    profile.likelihoodFactors = this.evaluateLikelihoodFactors(asset, organizationData);

    return profile;
  }

  // Identify threat actors for asset
  identifyThreatActorsForAsset(asset, organizationData) {
    const actors = [];

    // Based on asset type and organization
    if (asset.type === 'information' && asset.value === 'high') {
      actors.push({
        name: 'Cyber Criminal',
        motivation: 'Financial gain',
        capabilities: 'Technical skills, tools'
      });
    }

    if (organizationData.industry === 'finance' || organizationData.industry === 'healthcare') {
      actors.push({
        name: 'Insider Threat',
        motivation: 'Various',
        capabilities: 'Internal access, knowledge'
      });
    }

    if (asset.criticality >= 8) {
      actors.push({
        name: 'Nation State Actor',
        motivation: 'Espionage, disruption',
        capabilities: 'Advanced persistent threats'
      });
    }

    return actors;
  }

  // Identify threat actions for asset
  identifyThreatActionsForAsset(asset, threatActors) {
    const actions = [];

    for (const actor of threatActors) {
      const actorActions = this.getThreatActionsForActor(asset, actor);
      actions.push(...actorActions);
    }

    // Remove duplicates
    return [...new Set(actions)];
  }

  // Get threat actions for specific actor and asset
  getThreatActionsForActor(asset, actor) {
    const actions = [];

    if (asset.type === 'technology') {
      actions.push('Unauthorized access', 'Malware infection', 'Denial of service');
    } else if (asset.type === 'information') {
      actions.push('Data theft', 'Data modification', 'Data destruction');
    }

    if (actor.capabilities.includes('Internal access')) {
      actions.push('Insider attack', 'Data exfiltration');
    }

    if (actor.capabilities.includes('Advanced persistent threats')) {
      actions.push('Advanced persistent threat', 'Supply chain attack');
    }

    return actions;
  }

  // Assess impact areas
  assessImpactAreas(asset) {
    const impacts = [];

    if (asset.type === 'information') {
      impacts.push({
        area: 'Confidentiality',
        description: 'Unauthorized disclosure of sensitive information',
        potentialImpact: asset.sensitivity === 'high' ? 'Severe' : 'Moderate'
      });
    }

    impacts.push({
      area: 'Availability',
      description: 'Disruption of asset availability',
      potentialImpact: asset.criticality >= 8 ? 'Severe' : 'Moderate'
    });

    impacts.push({
      area: 'Integrity',
      description: 'Unauthorized modification of asset',
      potentialImpact: 'Moderate'
    });

    return impacts;
  }

  // Evaluate likelihood factors
  evaluateLikelihoodFactors(asset, organizationData) {
    const factors = [];

    // Current security posture
    if (organizationData.securityMaturity === 'low') {
      factors.push({
        factor: 'Weak security controls',
        impact: 'Increases',
        description: 'Current security measures are insufficient'
      });
    }

    // Asset exposure
    if (asset.publicFacing) {
      factors.push({
        factor: 'Public exposure',
        impact: 'Increases',
        description: 'Asset is accessible from the internet'
      });
    }

    // Regulatory requirements
    if (asset.regulatory) {
      factors.push({
        factor: 'Regulatory attention',
        impact: 'Increases',
        description: 'Asset is subject to regulatory scrutiny'
      });
    }

    return factors;
  }

  // Workshop 1: Strategic Assessment
  async conductStrategicAssessment(phase1Results, participants) {
    const workshop = {
      workshop: 1,
      name: this.workshops[1],
      participants: participants.filter(p => p.roles.includes('executive') || p.roles.includes('business')),
      objectives: [
        'Understand business context and risk tolerance',
        'Identify critical assets from business perspective',
        'Establish risk evaluation criteria'
      ],
      outcomes: {},
      completed: new Date()
    };

    // Simulate workshop outcomes
    workshop.outcomes = {
      businessContext: 'Manufacturing operations with 24/7 production requirements',
      riskTolerance: 'Low tolerance for production disruption, medium for data breaches',
      criticalAssets: phase1Results.criticalAssets.slice(0, 5), // Top 5
      evaluationCriteria: {
        financial: 'Direct cost impact',
        operational: 'Production downtime',
        reputational: 'Customer and market impact',
        regulatory: 'Compliance violations'
      }
    };

    return workshop;
  }

  // Phase 2: Identify Infrastructure Vulnerabilities
  async identifyInfrastructureVulnerabilities(phase1Results) {
    const vulnerabilities = {
      phase: 2,
      name: this.phases[2],
      infrastructureVulnerabilities: [],
      technologyWeaknesses: [],
      completed: new Date()
    };

    // Analyze infrastructure for vulnerabilities
    for (const asset of phase1Results.criticalAssets) {
      if (asset.type === 'technology') {
        const assetVulns = await this.analyzeAssetVulnerabilities(asset);
        vulnerabilities.infrastructureVulnerabilities.push(...assetVulns);
      }
    }

    // Identify technology weaknesses
    vulnerabilities.technologyWeaknesses = await this.identifyTechnologyWeaknesses(phase1Results);

    return vulnerabilities;
  }

  // Analyze asset vulnerabilities
  async analyzeAssetVulnerabilities(asset) {
    const vulnerabilities = [];

    // Check for common vulnerabilities based on asset characteristics
    if (asset.outdated) {
      vulnerabilities.push({
        assetId: asset.id,
        type: 'Outdated Software',
        severity: 'High',
        description: 'Asset is running outdated software with known vulnerabilities',
        exploitability: 'Easy'
      });
    }

    if (asset.weakAuthentication) {
      vulnerabilities.push({
        assetId: asset.id,
        type: 'Weak Authentication',
        severity: 'Critical',
        description: 'Asset uses weak or insufficient authentication mechanisms',
        exploitability: 'Easy'
      });
    }

    if (asset.unpatched) {
      vulnerabilities.push({
        assetId: asset.id,
        type: 'Missing Patches',
        severity: 'High',
        description: 'Asset has missing security patches',
        exploitability: 'Moderate'
      });
    }

    return vulnerabilities;
  }

  // Identify technology weaknesses
  async identifyTechnologyWeaknesses(phase1Results) {
    const weaknesses = [];

    // Analyze patterns across assets
    const technologyTypes = [...new Set(phase1Results.criticalAssets.map(a => a.technology))];

    for (const tech of technologyTypes) {
      const techAssets = phase1Results.criticalAssets.filter(a => a.technology === tech);

      if (techAssets.every(a => a.outdated)) {
        weaknesses.push({
          technology: tech,
          weakness: 'Technology Obsolescence',
          severity: 'High',
          affectedAssets: techAssets.length,
          description: `All ${tech} assets are running outdated versions`
        });
      }

      if (techAssets.some(a => a.vulnerable)) {
        weaknesses.push({
          technology: tech,
          weakness: 'Vulnerable Technology Stack',
          severity: 'Critical',
          affectedAssets: techAssets.filter(a => a.vulnerable).length,
          description: `${tech} technology has known vulnerabilities affecting multiple assets`
        });
      }
    }

    return weaknesses;
  }

  // Workshop 2: Technology Assessment
  async conductTechnologyAssessment(phase2Results, participants) {
    const workshop = {
      workshop: 2,
      name: this.workshops[2],
      participants: participants.filter(p => p.roles.includes('technical') || p.roles.includes('security')),
      objectives: [
        'Understand current technology infrastructure',
        'Identify technology vulnerabilities and weaknesses',
        'Evaluate mitigation approaches'
      ],
      outcomes: {},
      completed: new Date()
    };

    // Simulate workshop outcomes
    workshop.outcomes = {
      infrastructureUnderstanding: 'Complex mix of legacy and modern systems',
      keyVulnerabilities: phase2Results.infrastructureVulnerabilities.slice(0, 10),
      technologyWeaknesses: phase2Results.technologyWeaknesses,
      mitigationApproaches: this.generateMitigationApproaches(phase2Results)
    };

    return workshop;
  }

  // Generate mitigation approaches
  generateMitigationApproaches(phase2Results) {
    const approaches = [];

    for (const vuln of phase2Results.infrastructureVulnerabilities) {
      approaches.push({
        vulnerability: vuln.type,
        approaches: this.getMitigationApproaches(vuln.type),
        priority: vuln.severity === 'Critical' ? 'High' : 'Medium'
      });
    }

    return approaches;
  }

  // Get mitigation approaches for vulnerability type
  getMitigationApproaches(vulnType) {
    const approaches = {
      'Outdated Software': [
        'Upgrade to supported versions',
        'Implement compensating controls',
        'Isolate legacy systems'
      ],
      'Weak Authentication': [
        'Implement multi-factor authentication',
        'Use strong password policies',
        'Deploy certificate-based authentication'
      ],
      'Missing Patches': [
        'Establish patch management process',
        'Regular vulnerability scanning',
        'Automated patch deployment'
      ]
    };

    return approaches[vulnType] || ['Conduct security assessment', 'Implement appropriate controls'];
  }

  // Phase 3: Develop Security Strategy and Plans
  async developSecurityStrategy(phase1Results, phase2Results) {
    const strategy = {
      phase: 3,
      name: this.phases[3],
      riskEvaluation: {},
      mitigationPlans: [],
      securityStrategy: {},
      completed: new Date()
    };

    // Evaluate risks
    strategy.riskEvaluation = this.evaluateRisks(phase1Results, phase2Results);

    // Develop mitigation plans
    strategy.mitigationPlans = this.developMitigationPlans(strategy.riskEvaluation);

    // Create security strategy
    strategy.securityStrategy = this.createSecurityStrategy(strategy.mitigationPlans);

    return strategy;
  }

  // Evaluate risks
  evaluateRisks(phase1Results, phase2Results) {
    const evaluation = {
      evaluatedRisks: [],
      riskPriorities: []
    };

    // Evaluate each threat profile
    for (const profile of phase1Results.threatProfiles) {
      const assetVulns = phase2Results.infrastructureVulnerabilities.filter(v => v.assetId === profile.assetId);

      const risk = {
        assetId: profile.assetId,
        assetName: profile.assetName,
        threats: profile.threatActors.length,
        vulnerabilities: assetVulns.length,
        impactScore: this.calculateImpactScore(profile),
        likelihoodScore: this.calculateLikelihoodScore(profile, assetVulns),
        riskScore: 0,
        riskLevel: 'Low'
      };

      risk.riskScore = (risk.impactScore * risk.likelihoodScore) / 25; // Normalize to 0-1
      risk.riskLevel = this.getRiskLevel(risk.riskScore);

      evaluation.evaluatedRisks.push(risk);
    }

    // Sort by risk score
    evaluation.evaluatedRisks.sort((a, b) => b.riskScore - a.riskScore);

    // Create priority list
    evaluation.riskPriorities = evaluation.evaluatedRisks.map(risk => ({
      asset: risk.assetName,
      riskLevel: risk.riskLevel,
      priority: this.getRiskPriority(risk.riskLevel)
    }));

    return evaluation;
  }

  // Calculate impact score
  calculateImpactScore(profile) {
    let score = 0;

    for (const impact of profile.impactAreas) {
      if (impact.potentialImpact === 'Severe') score += 5;
      else if (impact.potentialImpact === 'Moderate') score += 3;
      else score += 1;
    }

    return Math.min(score, 5); // Cap at 5
  }

  // Calculate likelihood score
  calculateLikelihoodScore(profile, vulnerabilities) {
    let score = profile.threatActors.length; // Base score from number of actors

    // Increase for vulnerabilities
    score += vulnerabilities.length;

    // Increase for likelihood factors
    for (const factor of profile.likelihoodFactors) {
      if (factor.impact === 'Increases') score += 1;
    }

    return Math.min(score, 5); // Cap at 5
  }

  // Get risk level
  getRiskLevel(score) {
    if (score >= 0.8) return 'High';
    if (score >= 0.6) return 'Medium';
    return 'Low';
  }

  // Get risk priority
  getRiskPriority(riskLevel) {
    const priorities = { 'High': 1, 'Medium': 2, 'Low': 3 };
    return priorities[riskLevel] || 3;
  }

  // Develop mitigation plans
  developMitigationPlans(riskEvaluation) {
    const plans = [];

    for (const risk of riskEvaluation.evaluatedRisks) {
      if (risk.riskLevel === 'High') {
        plans.push({
          assetId: risk.assetId,
          assetName: risk.assetName,
          riskLevel: risk.riskLevel,
          mitigationActions: this.generateMitigationActions(risk),
          timeline: '3-6 months',
          responsibleParty: 'Security Team',
          successMetrics: this.generateSuccessMetrics(risk)
        });
      }
    }

    return plans;
  }

  // Generate mitigation actions
  generateMitigationActions(risk) {
    const actions = [];

    // Based on risk characteristics
    if (risk.threats > 2) {
      actions.push('Implement advanced threat detection');
    }

    if (risk.vulnerabilities > 0) {
      actions.push('Address identified vulnerabilities');
    }

    if (risk.impactScore > 3) {
      actions.push('Develop incident response plan');
    }

    return actions;
  }

  // Generate success metrics
  generateSuccessMetrics(risk) {
    return [
      `Reduce risk score below ${risk.riskScore * 0.5}`,
      'Implement all mitigation actions',
      'Pass security assessment'
    ];
  }

  // Create security strategy
  createSecurityStrategy(mitigationPlans) {
    const strategy = {
      vision: 'Comprehensive security program protecting critical assets',
      objectives: [
        'Reduce overall risk to acceptable levels',
        'Protect critical business processes',
        'Meet regulatory compliance requirements'
      ],
      principles: [
        'Defense in depth',
        'Risk-based approach',
        'Continuous improvement'
      ],
      initiatives: this.generateStrategicInitiatives(mitigationPlans),
      roadmap: this.createRoadmap(mitigationPlans)
    };

    return strategy;
  }

  // Generate strategic initiatives
  generateStrategicInitiatives(mitigationPlans) {
    const initiatives = [];

    if (mitigationPlans.some(p => p.mitigationActions.includes('Implement advanced threat detection'))) {
      initiatives.push({
        name: 'Advanced Threat Detection Program',
        description: 'Deploy advanced security monitoring and detection capabilities',
        timeline: '6-12 months',
        budget: 'High'
      });
    }

    initiatives.push({
      name: 'Security Awareness Training',
      description: 'Comprehensive security training for all personnel',
      timeline: 'Ongoing',
      budget: 'Medium'
    });

    initiatives.push({
      name: 'Technology Modernization',
      description: 'Upgrade legacy systems and technologies',
      timeline: '12-24 months',
      budget: 'High'
    });

    return initiatives;
  }

  // Create roadmap
  createRoadmap(mitigationPlans) {
    const roadmap = {
      phases: [
        {
          name: 'Immediate Actions',
          duration: '0-3 months',
          activities: ['Address critical vulnerabilities', 'Implement basic controls']
        },
        {
          name: 'Short-term Improvements',
          duration: '3-6 months',
          activities: ['Deploy advanced monitoring', 'Enhance incident response']
        },
        {
          name: 'Medium-term Strategy',
          duration: '6-12 months',
          activities: ['Implement strategic initiatives', 'Achieve compliance goals']
        },
        {
          name: 'Long-term Excellence',
          duration: '12-24 months',
          activities: ['Continuous improvement', 'Advanced security capabilities']
        }
      ]
    };

    return roadmap;
  }

  // Workshop 3: Risk Assessment
  async conductRiskAssessment(phase3Results, participants) {
    const workshop = {
      workshop: 3,
      name: this.workshops[3],
      participants: participants.filter(p => p.roles.includes('executive') || p.roles.includes('security')),
      objectives: [
        'Review and validate risk evaluations',
        'Approve mitigation plans and security strategy',
        'Establish risk monitoring and reporting'
      ],
      outcomes: {},
      completed: new Date()
    };

    // Simulate workshop outcomes
    workshop.outcomes = {
      riskAcceptance: 'Validated risk evaluation methodology',
      approvedPlans: phase3Results.mitigationPlans,
      approvedStrategy: phase3Results.securityStrategy,
      monitoringApproach: {
        frequency: 'Quarterly',
        metrics: ['Risk score trends', 'Control effectiveness', 'Incident rates'],
        reporting: 'To executive management and board'
      }
    };

    return workshop;
  }

  // Generate final strategy
  generateFinalStrategy(octaveModel) {
    const strategy = {
      executiveSummary: this.createExecutiveSummary(octaveModel),
      riskProfile: octaveModel.phases[1].threatProfiles,
      mitigationPlans: octaveModel.phases[3].mitigationPlans,
      securityStrategy: octaveModel.phases[3].securityStrategy,
      implementationRoadmap: octaveModel.phases[3].securityStrategy.roadmap,
      monitoringApproach: octaveModel.workshops[3].outcomes.monitoringApproach,
      successMetrics: this.defineSuccessMetrics(octaveModel)
    };

    return strategy;
  }

  // Create executive summary
  createExecutiveSummary(octaveModel) {
    const phase1 = octaveModel.phases[1];
    const phase3 = octaveModel.phases[3];

    return {
      organization: octaveModel.organizationName,
      assessmentDate: octaveModel.created,
      criticalAssets: phase1.criticalAssets.length,
      highRiskAssets: phase3.riskEvaluation.evaluatedRisks.filter(r => r.riskLevel === 'High').length,
      keyFindings: [
        `${phase1.criticalAssets.length} critical assets identified`,
        `${phase3.mitigationPlans.length} mitigation plans developed`,
        `Security strategy focuses on ${phase3.securityStrategy.principles.join(', ')}`
      ],
      nextSteps: [
        'Implement immediate mitigation actions',
        'Execute security strategy initiatives',
        'Establish ongoing risk monitoring'
      ]
    };
  }

  // Define success metrics
  defineSuccessMetrics(octaveModel) {
    return [
      {
        metric: 'Risk Reduction',
        target: '30% reduction in overall risk score within 12 months',
        measurement: 'Quarterly risk assessments'
      },
      {
        metric: 'Control Implementation',
        target: '100% of critical mitigation actions implemented',
        measurement: 'Monthly progress reports'
      },
      {
        metric: 'Incident Response',
        target: 'Average incident response time < 4 hours',
        measurement: 'Incident tracking system'
      },
      {
        metric: 'Compliance Achievement',
        target: '100% compliance with applicable regulations',
        measurement: 'Annual compliance assessments'
      }
    ];
  }

  // Utility methods
  generateAssetId() {
    return `ASSET_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  deduplicateAssets(assets) {
    const seen = new Set();
    return assets.filter(asset => {
      const key = `${asset.name}_${asset.type}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }
}

// Example OCTAVE threat modeling
const octaveModeler = new OCTAVEThreatModeler();

const organizationData = {
  name: 'Manufacturing Corp',
  industry: 'manufacturing',
  businessProcesses: [
    {
      name: 'Production Control',
      criticality: 9,
      technologyAssets: [
        { name: 'SCADA System', value: 'high', outdated: true },
        { name: 'PLC Controllers', value: 'high', unpatched: true }
      ],
      informationAssets: [
        { name: 'Production Recipes', criticality: 8, sensitivity: 'high' },
        { name: 'Quality Control Data', criticality: 7, regulatory: true }
      ]
    },
    {
      name: 'Supply Chain Management',
      criticality: 7,
      technologyAssets: [
        { name: 'ERP System', value: 'medium', weakAuthentication: true }
      ],
      informationAssets: [
        { name: 'Supplier Contracts', criticality: 6, sensitivity: 'medium' }
      ]
    }
  ],
  informationAssets: [
    { name: 'Customer Data', criticality: 8, sensitivity: 'high', regulatory: true },
    { name: 'Financial Records', criticality: 9, sensitivity: 'critical', regulatory: true }
  ],
  securityMaturity: 'medium'
};

const participants = [
  { name: 'CEO', roles: ['executive', 'business'] },
  { name: 'CISO', roles: ['executive', 'security'] },
  { name: 'IT Director', roles: ['technical', 'security'] },
  { name: 'Operations Manager', roles: ['business', 'operations'] },
  { name: 'Security Analyst', roles: ['technical', 'security'] }
];

const octaveModel = await octaveModeler.executeOCTAVE(organizationData, participants);

console.log('OCTAVE Threat Model Results:');
console.log('=============================');
console.log(`Organization: ${octaveModel.organizationName}`);

console.log('\nExecutive Summary:');
console.log(`- Critical Assets: ${octaveModel.finalStrategy.executiveSummary.criticalAssets}`);
console.log(`- High Risk Assets: ${octaveModel.finalStrategy.executiveSummary.highRiskAssets}`);

console.log('\nKey Findings:');
octaveModel.finalStrategy.executiveSummary.keyFindings.forEach(finding => {
  console.log(`- ${finding}`);
});

console.log('\nStrategic Initiatives:');
octaveModel.finalStrategy.securityStrategy.initiatives.forEach(initiative => {
  console.log(`- ${initiative.name}: ${initiative.description}`);
});

console.log('\nSuccess Metrics:');
octaveModel.finalStrategy.successMetrics.forEach(metric => {
  console.log(`- ${metric.metric}: ${metric.target}`);
});
```

### Trike Threat Modeling Methodology

**Requirements-driven, risk-based threat modeling framework**

#### Trike Core Concepts

Trike is a threat modeling methodology that focuses on requirements-driven security analysis. Unlike other methodologies that start with system decomposition, Trike begins with security requirements and uses a structured approach to identify threats that violate those requirements.

##### Key Principles
1. **Requirements-First:** Security requirements drive the threat modeling process
2. **Trust Boundaries:** Focus on trust relationships between system components
3. **Risk Calculation:** Quantitative risk assessment based on attacker capabilities
4. **Iterative Refinement:** Continuous improvement through feedback loops

#### Trike Methodology Implementation

```javascript
// Trike Threat Modeling Implementation
class TrikeThreatModeler {
  constructor() {
    this.requirements = {
      confidentiality: {
        weight: 0.3,
        description: 'Protection of sensitive information'
      },
      integrity: {
        weight: 0.3,
        description: 'Prevention of unauthorized modifications'
      },
      availability: {
        weight: 0.2,
        description: 'Ensuring system availability'
      },
      accountability: {
        weight: 0.2,
        description: 'Ability to trace actions to responsible parties'
      }
    };

    this.riskFactors = {
      attackerSkill: {
        'Novice': 1,
        'Intermediate': 3,
        'Advanced': 5,
        'Expert': 7,
        'Multiple Experts': 9
      },
      attackerMotive: {
        'None': 0,
        'Low': 2,
        'Moderate': 4,
        'High': 6,
        'Very High': 8
      },
      attackerResources: {
        'Minimal': 1,
        'Some': 3,
        'Moderate': 5,
        'Significant': 7,
        'Extensive': 9
      }
    };
  }

  // Execute Trike methodology
  async executeTrike(requirements, systemModel, attackerProfiles) {
    const trikeModel = {
      requirements: requirements,
      systemModel: systemModel,
      attackerProfiles: attackerProfiles,
      phases: {},
      finalAnalysis: null,
      created: new Date()
    };

    // Phase 1: Requirements Definition
    trikeModel.phases[1] = await this.defineRequirements(requirements);

    // Phase 2: System Modeling
    trikeModel.phases[2] = await this.modelSystem(systemModel);

    // Phase 3: Attacker Analysis
    trikeModel.phases[3] = await this.analyzeAttackers(attackerProfiles, systemModel);

    // Phase 4: Threat Analysis
    trikeModel.phases[4] = await this.analyzeThreats(trikeModel.phases[1], trikeModel.phases[2], trikeModel.phases[3]);

    // Phase 5: Risk Analysis
    trikeModel.phases[5] = await this.analyzeRisk(trikeModel.phases[4]);

    // Phase 6: Mitigation Analysis
    trikeModel.phases[6] = await this.analyzeMitigations(trikeModel.phases[5]);

    // Generate final analysis
    trikeModel.finalAnalysis = this.generateFinalAnalysis(trikeModel);

    return trikeModel;
  }

  // Phase 1: Define Requirements
  async defineRequirements(requirements) {
    return {
      phase: 1,
      name: 'Requirements Definition',
      securityRequirements: this.processSecurityRequirements(requirements),
      functionalRequirements: requirements.functional || [],
      constraints: requirements.constraints || [],
      assumptions: requirements.assumptions || [],
      completed: new Date()
    };
  }

  // Process security requirements
  processSecurityRequirements(requirements) {
    const processed = [];

    for (const [type, details] of Object.entries(this.requirements)) {
      if (requirements[type]) {
        processed.push({
          type: type,
          description: requirements[type].description || details.description,
          priority: requirements[type].priority || 'medium',
          weight: details.weight,
          measurable: requirements[type].measurable || false,
          verification: requirements[type].verification || 'manual'
        });
      }
    }

    return processed;
  }

  // Phase 2: System Modeling
  async modelSystem(systemModel) {
    return {
      phase: 2,
      name: 'System Modeling',
      components: this.identifyComponents(systemModel),
      dataFlows: this.analyzeDataFlows(systemModel),
      trustBoundaries: this.identifyTrustBoundaries(systemModel),
      interfaces: this.identifyInterfaces(systemModel),
      completed: new Date()
    };
  }

  // Identify system components
  identifyComponents(systemModel) {
    const components = [];

    for (const component of systemModel.components || []) {
      components.push({
        id: this.generateComponentId(),
        name: component.name,
        type: component.type,
        trustLevel: component.trustLevel || 'low',
        interfaces: component.interfaces || [],
        dataProcessed: component.dataProcessed || [],
        securityControls: component.securityControls || []
      });
    }

    return components;
  }

  // Analyze data flows
  analyzeDataFlows(systemModel) {
    const flows = [];

    for (const flow of systemModel.dataFlows || []) {
      flows.push({
        id: this.generateFlowId(),
        source: flow.source,
        target: flow.target,
        dataType: flow.dataType,
        sensitivity: flow.sensitivity || 'low',
        encryption: flow.encrypted || false,
        authentication: flow.authenticated || false,
        integrity: flow.integrityChecked || false,
        volume: flow.volume || 'low'
      });
    }

    return flows;
  }

  // Identify trust boundaries
  identifyTrustBoundaries(systemModel) {
    const boundaries = [];

    // Analyze component trust levels
    const trustLevels = [...new Set(systemModel.components?.map(c => c.trustLevel) || [])];

    for (let i = 0; i < trustLevels.length - 1; i++) {
      for (let j = i + 1; j < trustLevels.length; j++) {
        boundaries.push({
          id: this.generateBoundaryId(),
          level1: trustLevels[i],
          level2: trustLevels[j],
          components1: systemModel.components?.filter(c => c.trustLevel === trustLevels[i]).map(c => c.name) || [],
          components2: systemModel.components?.filter(c => c.trustLevel === trustLevels[j]).map(c => c.name) || [],
          crossingPoints: this.findCrossingPoints(trustLevels[i], trustLevels[j], systemModel)
        });
      }
    }

    return boundaries;
  }

  // Find crossing points between trust levels
  findCrossingPoints(level1, level2, systemModel) {
    const crossingPoints = [];

    for (const flow of systemModel.dataFlows || []) {
      const sourceComponent = systemModel.components?.find(c => c.name === flow.source);
      const targetComponent = systemModel.components?.find(c => c.name === flow.target);

      if (sourceComponent && targetComponent &&
          ((sourceComponent.trustLevel === level1 && targetComponent.trustLevel === level2) ||
           (sourceComponent.trustLevel === level2 && targetComponent.trustLevel === level1))) {
        crossingPoints.push({
          flow: `${flow.source} -> ${flow.target}`,
          dataType: flow.dataType,
          controls: flow.controls || []
        });
      }
    }

    return crossingPoints;
  }

  // Phase 3: Attacker Analysis
  async analyzeAttackers(attackerProfiles, systemModel) {
    const analysis = {
      phase: 3,
      name: 'Attacker Analysis',
      profiles: [],
      capabilities: [],
      motivations: [],
      completed: new Date()
    };

    for (const profile of attackerProfiles) {
      const analyzedProfile = {
        id: this.generateAttackerId(),
        name: profile.name,
        type: profile.type,
        skill: profile.skill || 'intermediate',
        motive: profile.motive || 'moderate',
        resources: profile.resources || 'moderate',
        goals: profile.goals || [],
        methods: profile.methods || [],
        likelihood: this.calculateAttackerLikelihood(profile),
        potentialImpact: this.assessAttackerImpact(profile, systemModel)
      };

      analysis.profiles.push(analyzedProfile);
    }

    // Aggregate capabilities and motivations
    analysis.capabilities = this.aggregateCapabilities(analysis.profiles);
    analysis.motivations = this.aggregateMotivations(analysis.profiles);

    return analysis;
  }

  // Calculate attacker likelihood
  calculateAttackerLikelihood(profile) {
    const skillScore = this.riskFactors.attackerSkill[profile.skill] || 3;
    const motiveScore = this.riskFactors.attackerMotive[profile.motive] || 4;
    const resourceScore = this.riskFactors.attackerResources[profile.resources] || 5;

    const likelihoodScore = (skillScore + motiveScore + resourceScore) / 3;

    if (likelihoodScore >= 7) return 'Very High';
    if (likelihoodScore >= 5) return 'High';
    if (likelihoodScore >= 3) return 'Medium';
    if (likelihoodScore >= 2) return 'Low';
    return 'Very Low';
  }

  // Assess attacker impact potential
  assessAttackerImpact(profile, systemModel) {
    let impact = 'Low';

    // Check if attacker can reach critical components
    const reachableComponents = this.findReachableComponents(profile, systemModel);

    if (reachableComponents.some(c => c.critical)) {
      impact = 'Critical';
    } else if (reachableComponents.some(c => c.sensitive)) {
      impact = 'High';
    } else if (reachableComponents.length > 0) {
      impact = 'Medium';
    }

    return impact;
  }

  // Find components reachable by attacker
  findReachableComponents(profile, systemModel) {
    // Simplified reachability analysis
    const reachable = [];

    for (const component of systemModel.components || []) {
      if (component.exposed || component.publicFacing) {
        reachable.push(component);
      }
    }

    return reachable;
  }

  // Phase 4: Threat Analysis
  async analyzeThreats(requirementsPhase, systemPhase, attackerPhase) {
    const analysis = {
      phase: 4,
      name: 'Threat Analysis',
      threats: [],
      correlations: [],
      completed: new Date()
    };

    // Generate threats for each requirement violation
    for (const requirement of requirementsPhase.securityRequirements) {
      for (const attacker of attackerPhase.profiles) {
        const threats = this.generateThreatsForRequirement(requirement, attacker, systemPhase);
        analysis.threats.push(...threats);
      }
    }

    // Correlate threats with system components
    analysis.correlations = this.correlateThreatsComponents(analysis.threats, systemPhase);

    return analysis;
  }

  // Generate threats for specific requirement and attacker
  generateThreatsForRequirement(requirement, attacker, systemPhase) {
    const threats = [];

    switch (requirement.type) {
      case 'confidentiality':
        threats.push(...this.generateConfidentialityThreats(requirement, attacker, systemPhase));
        break;
      case 'integrity':
        threats.push(...this.generateIntegrityThreats(requirement, attacker, systemPhase));
        break;
      case 'availability':
        threats.push(...this.generateAvailabilityThreats(requirement, attacker, systemPhase));
        break;
      case 'accountability':
        threats.push(...this.generateAccountabilityThreats(requirement, attacker, systemPhase));
        break;
    }

    return threats;
  }

  // Generate confidentiality threats
  generateConfidentialityThreats(requirement, attacker, systemPhase) {
    const threats = [];

    // Check data flows that cross trust boundaries
    for (const boundary of systemPhase.trustBoundaries) {
      for (const crossing of boundary.crossingPoints) {
        if (crossing.dataType === 'sensitive' || crossing.dataType === 'personal') {
          threats.push({
            id: this.generateThreatId(),
            requirement: requirement.type,
            attacker: attacker.name,
            component: crossing.flow,
            description: `${attacker.name} could intercept ${crossing.dataType} data crossing trust boundary`,
            type: 'Information Disclosure',
            likelihood: attacker.likelihood,
            impact: requirement.priority === 'high' ? 'High' : 'Medium',
            attackVector: 'Network Interception',
            prerequisites: ['Network access', 'Unencrypted communication']
          });
        }
      }
    }

    return threats;
  }

  // Generate integrity threats
  generateIntegrityThreats(requirement, attacker, systemPhase) {
    const threats = [];

    // Check components that process data
    for (const component of systemPhase.components) {
      if (component.dataProcessed?.includes('sensitive') || component.type === 'database') {
        threats.push({
          id: this.generateThreatId(),
          requirement: requirement.type,
          attacker: attacker.name,
          component: component.name,
          description: `${attacker.name} could modify data processed by ${component.name}`,
          type: 'Data Tampering',
          likelihood: attacker.likelihood,
          impact: requirement.priority === 'high' ? 'Critical' : 'High',
          attackVector: 'Data Modification',
          prerequisites: ['Access to component', 'Insufficient integrity controls']
        });
      }
    }

    return threats;
  }

  // Generate availability threats
  generateAvailabilityThreats(requirement, attacker, systemPhase) {
    const threats = [];

    // Check critical components
    for (const component of systemPhase.components) {
      if (component.critical || component.type === 'load_balancer' || component.type === 'web_server') {
        threats.push({
          id: this.generateThreatId(),
          requirement: requirement.type,
          attacker: attacker.name,
          component: component.name,
          description: `${attacker.name} could make ${component.name} unavailable`,
          type: 'Denial of Service',
          likelihood: attacker.likelihood,
          impact: requirement.priority === 'high' ? 'Critical' : 'High',
          attackVector: 'Resource Exhaustion',
          prerequisites: ['Access to component', 'Insufficient rate limiting']
        });
      }
    }

    return threats;
  }

  // Generate accountability threats
  generateAccountabilityThreats(requirement, attacker, systemPhase) {
    const threats = [];

    // Check components with logging
    for (const component of systemPhase.components) {
      if (component.logging || component.type === 'audit_system') {
        threats.push({
          id: this.generateThreatId(),
          requirement: requirement.type,
          attacker: attacker.name,
          component: component.name,
          description: `${attacker.name} could avoid accountability by manipulating logs in ${component.name}`,
          type: 'Repudiation',
          likelihood: attacker.likelihood,
          impact: 'Medium',
          attackVector: 'Log Manipulation',
          prerequisites: ['Access to logs', 'Weak log integrity']
        });
      }
    }

    return threats;
  }

  // Phase 5: Risk Analysis
  async analyzeRisk(threatAnalysis) {
    const analysis = {
      phase: 5,
      name: 'Risk Analysis',
      riskAssessments: [],
      riskMetrics: {},
      completed: new Date()
    };

    // Assess risk for each threat
    for (const threat of threatAnalysis.threats) {
      const assessment = this.assessThreatRisk(threat);
      analysis.riskAssessments.push(assessment);
    }

    // Calculate aggregate risk metrics
    analysis.riskMetrics = this.calculateRiskMetrics(analysis.riskAssessments);

    return analysis;
  }

  // Assess risk for individual threat
  assessThreatRisk(threat) {
    const likelihoodScore = { 'Very Low': 1, 'Low': 2, 'Medium': 3, 'High': 4, 'Very High': 5 }[threat.likelihood] || 3;
    const impactScore = { 'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4 }[threat.impact] || 2;

    const riskScore = likelihoodScore * impactScore;

    return {
      threatId: threat.id,
      threatDescription: threat.description,
      likelihood: threat.likelihood,
      impact: threat.impact,
      riskScore: riskScore,
      riskLevel: this.getRiskLevel(riskScore),
      requirement: threat.requirement,
      attacker: threat.attacker,
      component: threat.component
    };
  }

  // Get risk level from score
  getRiskLevel(score) {
    if (score >= 16) return 'Critical';
    if (score >= 12) return 'High';
    if (score >= 6) return 'Medium';
    if (score >= 3) return 'Low';
    return 'Very Low';
  }

  // Calculate risk metrics
  calculateRiskMetrics(assessments) {
    const metrics = {
      totalThreats: assessments.length,
      criticalRisks: assessments.filter(a => a.riskLevel === 'Critical').length,
      highRisks: assessments.filter(a => a.riskLevel === 'High').length,
      mediumRisks: assessments.filter(a => a.riskLevel === 'Medium').length,
      lowRisks: assessments.filter(a => a.riskLevel === 'Low').length,
      averageRiskScore: assessments.reduce((sum, a) => sum + a.riskScore, 0) / assessments.length,
      maxRiskScore: Math.max(...assessments.map(a => a.riskScore)),
      overallRiskLevel: this.getOverallRiskLevel(assessments)
    };

    return metrics;
  }

  // Get overall risk level
  getOverallRiskLevel(assessments) {
    const criticalCount = assessments.filter(a => a.riskLevel === 'Critical').length;
    const highCount = assessments.filter(a => a.riskLevel === 'High').length;

    if (criticalCount > 0) return 'Critical';
    if (highCount > 5) return 'High';
    if (highCount > 0) return 'Medium';
    return 'Low';
  }

  // Phase 6: Mitigation Analysis
  async analyzeMitigations(riskAnalysis) {
    const analysis = {
      phase: 6,
      name: 'Mitigation Analysis',
      mitigations: [],
      mitigationEffectiveness: {},
      completed: new Date()
    };

    // Generate mitigations for high-risk threats
    for (const assessment of riskAnalysis.riskAssessments) {
      if (assessment.riskLevel === 'Critical' || assessment.riskLevel === 'High') {
        const mitigation = this.generateMitigation(assessment);
        analysis.mitigations.push(mitigation);
      }
    }

    // Assess mitigation effectiveness
    analysis.mitigationEffectiveness = this.assessMitigationEffectiveness(analysis.mitigations, riskAnalysis.riskAssessments);

    return analysis;
  }

  // Generate mitigation for threat
  generateMitigation(assessment) {
    const mitigation = {
      threatId: assessment.threatId,
      requirement: assessment.requirement,
      component: assessment.component,
      controls: this.getMitigationControls(assessment),
      priority: assessment.riskLevel === 'Critical' ? 'Immediate' : 'High',
      cost: this.estimateMitigationCost(assessment),
      effectiveness: this.estimateMitigationEffectiveness(assessment)
    };

    return mitigation;
  }

  // Get mitigation controls based on threat
  getMitigationControls(assessment) {
    const controls = [];

    switch (assessment.requirement) {
      case 'confidentiality':
        controls.push('Encryption', 'Access Controls', 'Network Segmentation');
        break;
      case 'integrity':
        controls.push('Input Validation', 'Digital Signatures', 'Integrity Monitoring');
        break;
      case 'availability':
        controls.push('Redundancy', 'Rate Limiting', 'Load Balancing');
        break;
      case 'accountability':
        controls.push('Secure Logging', 'Audit Trails', 'Digital Signatures on Logs');
        break;
    }

    return controls;
  }

  // Generate final analysis
  generateFinalAnalysis(trikeModel) {
    const analysis = {
      summary: this.createSummary(trikeModel),
      keyFindings: this.extractKeyFindings(trikeModel),
      recommendations: this.generateRecommendations(trikeModel),
      riskProfile: this.createRiskProfile(trikeModel),
      complianceStatus: this.assessCompliance(trikeModel)
    };

    return analysis;
  }

  // Create summary
  createSummary(trikeModel) {
    const riskAnalysis = trikeModel.phases[5];

    return {
      methodology: 'Trike',
      totalRequirements: trikeModel.phases[1].securityRequirements.length,
      totalThreats: trikeModel.phases[4].threats.length,
      totalAttackers: trikeModel.phases[3].profiles.length,
      overallRiskLevel: riskAnalysis.riskMetrics.overallRiskLevel,
      criticalThreats: riskAnalysis.riskMetrics.criticalRisks,
      highThreats: riskAnalysis.riskMetrics.highRisks,
      recommendedMitigations: trikeModel.phases[6].mitigations.length
    };
  }

  // Utility methods
  generateComponentId() {
    return `COMP_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  generateFlowId() {
    return `FLOW_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  generateBoundaryId() {
    return `BOUNDARY_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  generateAttackerId() {
    return `ATTACKER_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  generateThreatId() {
    return `THREAT_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  aggregateCapabilities(profiles) {
    const capabilities = new Set();
    profiles.forEach(p => p.methods?.forEach(m => capabilities.add(m)));
    return Array.from(capabilities);
  }

  aggregateMotivations(profiles) {
    const motivations = new Set();
    profiles.forEach(p => motivations.add(p.motive));
    return Array.from(motivations);
  }

  correlateThreatsComponents(threats, systemPhase) {
    const correlations = [];

    for (const threat of threats) {
      const component = systemPhase.components.find(c => c.name === threat.component);
      if (component) {
        correlations.push({
          threatId: threat.id,
          componentId: component.id,
          trustLevel: component.trustLevel,
          interfaces: component.interfaces
        });
      }
    }

    return correlations;
  }

  estimateMitigationCost(assessment) {
    const baseCost = { 'Low': 1000, 'Medium': 5000, 'High': 15000, 'Critical': 50000 }[assessment.riskLevel] || 5000;
    return baseCost;
  }

  estimateMitigationEffectiveness(assessment) {
    return assessment.riskLevel === 'Critical' ? 0.9 : 0.8;
  }

  assessMitigationEffectiveness(mitigations, assessments) {
    const effectiveness = {
      averageRiskReduction: 0,
      effectiveMitigations: 0,
      costEffectiveMitigations: 0
    };

    for (const mitigation of mitigations) {
      const originalAssessment = assessments.find(a => a.threatId === mitigation.threatId);
      if (originalAssessment) {
        const reduction = originalAssessment.riskScore * (1 - mitigation.effectiveness);
        effectiveness.averageRiskReduction += reduction;

        if (reduction > originalAssessment.riskScore * 0.5) {
          effectiveness.effectiveMitigations++;
        }

        if (mitigation.cost < originalAssessment.riskScore * 100) {
          effectiveness.costEffectiveMitigations++;
        }
      }
    }

    effectiveness.averageRiskReduction /= mitigations.length;

    return effectiveness;
  }

  extractKeyFindings(trikeModel) {
    const findings = [];
    const riskMetrics = trikeModel.phases[5].riskMetrics;

    if (riskMetrics.criticalRisks > 0) {
      findings.push(`${riskMetrics.criticalRisks} critical threats identified requiring immediate attention`);
    }

    if (riskMetrics.highRisks > 5) {
      findings.push(`High threat density with ${riskMetrics.highRisks} high-risk threats`);
    }

    findings.push(`${trikeModel.phases[1].securityRequirements.length} security requirements analyzed`);
    findings.push(`${trikeModel.phases[3].profiles.length} attacker profiles evaluated`);

    return findings;
  }

  generateRecommendations(trikeModel) {
    const recommendations = [];
    const riskLevel = trikeModel.phases[5].riskMetrics.overallRiskLevel;

    if (riskLevel === 'Critical') {
      recommendations.push({
        priority: 'Critical',
        action: 'Implement immediate compensating controls for critical threats',
        timeframe: 'Within 24 hours'
      });
    }

    recommendations.push({
      priority: 'High',
      action: 'Address high-risk threats in current development cycle',
      timeframe: 'Within 2 weeks'
    });

    recommendations.push({
      priority: 'Medium',
      action: 'Integrate Trike threat modeling into requirements phase',
      timeframe: 'Next project'
    });

    return recommendations;
  }

  createRiskProfile(trikeModel) {
    const profile = {
      requirements: trikeModel.phases[1].securityRequirements.map(r => ({
        type: r.type,
        priority: r.priority,
        weight: r.weight
      })),
      threats: trikeModel.phases[4].threats.map(t => ({
        requirement: t.requirement,
        type: t.type,
        risk: `${t.likelihood}/${t.impact}`
      })),
      attackers: trikeModel.phases[3].profiles.map(a => ({
        name: a.name,
        likelihood: a.likelihood,
        impact: a.potentialImpact
      }))
    };

    return profile;
  }

  assessCompliance(trikeModel) {
    // Simplified compliance assessment
    const requirements = trikeModel.phases[1].securityRequirements;
    const threats = trikeModel.phases[4].threats;

    const compliance = {
      totalRequirements: requirements.length,
      addressedRequirements: requirements.length, // Assume all addressed in analysis
      compliancePercentage: 100,
      gaps: []
    };

    return compliance;
  }
}

// Example Trike threat modeling
const trikeModeler = new TrikeThreatModeler();

const securityRequirements = {
  confidentiality: {
    description: 'Protect customer payment information',
    priority: 'high',
    measurable: true,
    verification: 'automated'
  },
  integrity: {
    description: 'Ensure transaction data accuracy',
    priority: 'high',
    measurable: true,
    verification: 'manual'
  },
  availability: {
    description: 'Maintain 99.9% system uptime',
    priority: 'medium',
    measurable: true,
    verification: 'monitoring'
  },
  accountability: {
    description: 'Track all financial transactions',
    priority: 'medium',
    measurable: true,
    verification: 'audit'
  }
};

const systemModel = {
  components: [
    {
      name: 'PaymentAPI',
      type: 'api_endpoint',
      trustLevel: 'low',
      interfaces: ['REST', 'JSON'],
      dataProcessed: ['payment', 'personal'],
      securityControls: ['authentication', 'rate_limiting']
    },
    {
      name: 'PaymentDB',
      type: 'database',
      trustLevel: 'medium',
      interfaces: ['SQL'],
      dataProcessed: ['payment', 'sensitive'],
      securityControls: ['encryption', 'access_control']
    },
    {
      name: 'AuthService',
      type: 'authentication_service',
      trustLevel: 'high',
      interfaces: ['LDAP', 'OAuth'],
      dataProcessed: ['credentials'],
      securityControls: ['multi_factor', 'encryption']
    }
  ],
  dataFlows: [
    {
      source: 'PaymentAPI',
      target: 'PaymentDB',
      dataType: 'payment',
      sensitivity: 'high',
      encrypted: true,
      authenticated: true,
      integrityChecked: true
    },
    {
      source: 'AuthService',
      target: 'PaymentAPI',
      dataType: 'credentials',
      sensitivity: 'high',
      encrypted: true,
      authenticated: true,
      integrityChecked: true
    }
  ]
};

const attackerProfiles = [
  {
    name: 'External Hacker',
    type: 'individual',
    skill: 'Advanced',
    motive: 'High',
    resources: 'Moderate',
    goals: ['Data theft', 'Financial gain'],
    methods: ['SQL injection', 'XSS', 'Network attacks']
  },
  {
    name: 'Insider Threat',
    type: 'insider',
    skill: 'Intermediate',
    motive: 'Moderate',
    resources: 'Significant',
    goals: ['Data exfiltration', 'Sabotage'],
    methods: ['Privilege abuse', 'Data export', 'System manipulation']
  },
  {
    name: 'Organized Crime',
    type: 'group',
    skill: 'Expert',
    motive: 'Very High',
    resources: 'Extensive',
    goals: ['Mass data theft', 'Ransomware'],
    methods: ['Advanced persistent threats', 'Zero-day exploits', 'Social engineering']
  }
];

const trikeModel = await trikeModeler.executeTrike(securityRequirements, systemModel, attackerProfiles);

console.log('Trike Threat Model Results:');
console.log('===========================');
console.log(`Requirements Analyzed: ${trikeModel.finalAnalysis.summary.totalRequirements}`);
console.log(`Threats Identified: ${trikeModel.finalAnalysis.summary.totalThreats}`);
console.log(`Overall Risk Level: ${trikeModel.finalAnalysis.summary.overallRiskLevel}`);
console.log(`Critical Threats: ${trikeModel.finalAnalysis.summary.criticalThreats}`);

console.log('\nKey Findings:');
trikeModel.finalAnalysis.keyFindings.forEach(finding => {
  console.log(`- ${finding}`);
});

console.log('\nTop Recommendations:');
trikeModel.finalAnalysis.recommendations.forEach(rec => {
  console.log(`- ${rec.priority}: ${rec.action} (${rec.timeframe})`);
});
```

### Trike Threat Modeling Template

```markdown
# Trike Threat Model: [System Name]

## 1. Security Requirements Definition

### Confidentiality Requirements
| Requirement | Description | Priority | Measurable | Verification |
|-------------|-------------|----------|------------|--------------|
| [Req 1] | [Description] | [High/Medium/Low] | [Yes/No] | [Method] |

### Integrity Requirements
| Requirement | Description | Priority | Measurable | Verification |
|-------------|-------------|----------|------------|--------------|
| [Req 1] | [Description] | [High/Medium/Low] | [Yes/No] | [Method] |

### Availability Requirements
| Requirement | Description | Priority | Measurable | Verification |
|-------------|-------------|----------|------------|--------------|
| [Req 1] | [Description] | [High/Medium/Low] | [Yes/No] | [Method] |

### Accountability Requirements
| Requirement | Description | Priority | Measurable | Verification |
|-------------|-------------|----------|------------|--------------|
| [Req 1] | [Description] | [High/Medium/Low] | [Yes/No] | [Method] |

## 2. System Model

### Components
| Component | Type | Trust Level | Interfaces | Data Processed | Security Controls |
|-----------|------|-------------|------------|----------------|-------------------|
| [Name] | [Type] | [Level] | [List] | [List] | [List] |

### Data Flows
| Source | Target | Data Type | Sensitivity | Encrypted | Authenticated | Integrity |
|--------|--------|-----------|-------------|-----------|---------------|-----------|
| [Source] | [Target] | [Type] | [Level] | [Yes/No] | [Yes/No] | [Yes/No] |

### Trust Boundaries
| Boundary | Level 1 | Level 2 | Crossing Points | Controls |
|----------|---------|---------|----------------|----------|
| [ID] | [Level] | [Level] | [List] | [List] |

## 3. Attacker Profiles

| Attacker | Type | Skill | Motive | Resources | Goals | Methods |
|----------|------|-------|--------|-----------|-------|---------|
| [Name] | [Type] | [Level] | [Level] | [Level] | [List] | [List] |

## 4. Threat Analysis

### Threats by Requirement
| Threat ID | Requirement | Attacker | Component | Description | Type | Likelihood | Impact |
|-----------|-------------|----------|-----------|-------------|------|------------|--------|
| T_001 | [Requirement] | [Attacker] | [Component] | [Description] | [Type] | [Level] | [Level] |

## 5. Risk Analysis

### Risk Assessment Matrix
| Threat ID | Description | Likelihood | Impact | Risk Score | Risk Level | Priority |
|-----------|-------------|------------|--------|------------|------------|----------|
| [ID] | [Description] | [Score] | [Score] | [Score] | [Level] | [Level] |

### Risk Metrics
- **Total Threats:** [Count]
- **Critical Risks:** [Count]
- **High Risks:** [Count]
- **Overall Risk Level:** [Level]

## 6. Mitigation Analysis

### Mitigation Strategies
| Threat ID | Component | Controls | Priority | Estimated Cost | Effectiveness |
|-----------|-----------|----------|----------|----------------|---------------|
| [ID] | [Component] | [List] | [Level] | [Cost] | [Percentage] |

## 7. Recommendations

### Immediate Actions (Critical)
1. [Action 1]
2. [Action 2]

### Short-term Actions (High)
1. [Action 1]
2. [Action 2]

### Long-term Actions (Medium)
1. [Action 1]
2. [Action 2]

## 8. Compliance Assessment

- **Requirements Addressed:** [Count]/[Total]
- **Compliance Percentage:** [Percentage]%
- **Identified Gaps:** [List]

## 9. Next Steps

1. [Step 1]
2. [Step 2]
3. [Step 3]

## 10. Review and Approval

- **Model Reviewed By:** [Name] on [Date]
- **Approved By:** [Name] on [Date]
- **Next Review Date:** [Date]
```

### VAST (Visual, Agile, and Simple Threat Modeling)

**Agile threat modeling methodology for fast-paced development**

#### VAST Core Principles

VAST (Visual, Agile, and Simple Threat Modeling) is designed for agile development environments where speed and simplicity are essential. It focuses on visual representations and iterative refinement.

##### Key Characteristics
1. **Visual:** Uses diagrams and visual representations
2. **Agile:** Iterative and incremental approach
3. **Simple:** Easy to understand and apply
4. **Fast:** Quick threat identification and mitigation

#### VAST Methodology Implementation

```javascript
// VAST Threat Modeling Implementation
class VASTThreatModeler {
  constructor() {
    this.phases = {
      1: 'Asset Identification',
      2: 'Threat Identification',
      3: 'Mitigation Planning',
      4: 'Validation'
    };

    this.threatCategories = {
      'Spoofing': 'Impersonation attacks',
      'Tampering': 'Data modification attacks',
      'Repudiation': 'Action denial attacks',
      'Information Disclosure': 'Data exposure attacks',
      'Denial of Service': 'Availability attacks',
      'Elevation of Privilege': 'Access escalation attacks'
    };
  }

  // Execute VAST methodology
  async executeVAST(systemDescription, sprintContext) {
    const vastModel = {
      systemName: systemDescription.name,
      sprint: sprintContext?.sprint || 'Current',
      phases: {},
      visualDiagrams: {},
      finalReport: null,
      created: new Date()
    };

    // Phase 1: Asset Identification
    vastModel.phases[1] = await this.identifyAssets(systemDescription);

    // Phase 2: Threat Identification
    vastModel.phases[2] = await this.identifyThreats(vastModel.phases[1], sprintContext);

    // Phase 3: Mitigation Planning
    vastModel.phases[3] = await this.planMitigations(vastModel.phases[2]);

    // Phase 4: Validation
    vastModel.phases[4] = await this.validateModel(vastModel.phases[3]);

    // Generate visual diagrams
    vastModel.visualDiagrams = this.generateVisualDiagrams(vastModel);

    // Generate final report
    vastModel.finalReport = this.generateFinalReport(vastModel);

    return vastModel;
  }

  // Phase 1: Asset Identification
  async identifyAssets(systemDescription) {
    const assets = {
      phase: 1,
      name: this.phases[1],
      functionalAssets: [],
      dataAssets: [],
      technicalAssets: [],
      completed: new Date()
    };

    // Identify functional assets (features, capabilities)
    assets.functionalAssets = this.extractFunctionalAssets(systemDescription);

    // Identify data assets
    assets.dataAssets = this.extractDataAssets(systemDescription);

    // Identify technical assets
    assets.technicalAssets = this.extractTechnicalAssets(systemDescription);

    return assets;
  }

  // Extract functional assets
  extractFunctionalAssets(systemDescription) {
    const assets = [];

    for (const feature of systemDescription.features || []) {
      assets.push({
        id: this.generateAssetId(),
        name: feature.name,
        type: 'functional',
        description: feature.description,
        criticality: feature.criticality || 'medium',
        users: feature.users || [],
        dependencies: feature.dependencies || []
      });
    }

    return assets;
  }

  // Extract data assets
  extractDataAssets(systemDescription) {
    const assets = [];

    for (const data of systemDescription.dataTypes || []) {
      assets.push({
        id: this.generateAssetId(),
        name: data.name,
        type: 'data',
        sensitivity: data.sensitivity || 'low',
        volume: data.volume || 'low',
        access: data.access || 'internal',
        regulations: data.regulations || []
      });
    }

    return assets;
  }

  // Extract technical assets
  extractTechnicalAssets(systemDescription) {
    const assets = [];

    for (const component of systemDescription.components || []) {
      assets.push({
        id: this.generateAssetId(),
        name: component.name,
        type: 'technical',
        category: component.category,
        technology: component.technology,
        exposure: component.exposure || 'internal',
        interfaces: component.interfaces || []
      });
    }

    return assets;
  }

  // Phase 2: Threat Identification
  async identifyThreats(assetsPhase, sprintContext) {
    const threats = {
      phase: 2,
      name: this.phases[2],
      identifiedThreats: [],
      threatScenarios: [],
      completed: new Date()
    };

    // Identify threats for each asset type
    for (const asset of assetsPhase.functionalAssets) {
      const assetThreats = this.identifyThreatsForAsset(asset, 'functional');
      threats.identifiedThreats.push(...assetThreats);
    }

    for (const asset of assetsPhase.dataAssets) {
      const assetThreats = this.identifyThreatsForAsset(asset, 'data');
      threats.identifiedThreats.push(...assetThreats);
    }

    for (const asset of assetsPhase.technicalAssets) {
      const assetThreats = this.identifyThreatsForAsset(asset, 'technical');
      threats.identifiedThreats.push(...assetThreats);
    }

    // Generate threat scenarios
    threats.threatScenarios = this.generateThreatScenarios(threats.identifiedThreats, sprintContext);

    return threats;
  }

  // Identify threats for specific asset
  identifyThreatsForAsset(asset, assetType) {
    const threats = [];

    switch (assetType) {
      case 'functional':
        threats.push(...this.identifyFunctionalThreats(asset));
        break;
      case 'data':
        threats.push(...this.identifyDataThreats(asset));
        break;
      case 'technical':
        threats.push(...this.identifyTechnicalThreats(asset));
        break;
    }

    return threats;
  }

  // Identify functional threats
  identifyFunctionalThreats(asset) {
    const threats = [];

    // Common functional threats
    if (asset.users?.includes('external')) {
      threats.push({
        id: this.generateThreatId(),
        assetId: asset.id,
        assetName: asset.name,
        category: 'Spoofing',
        description: `Unauthorized users could access ${asset.name} functionality`,
        likelihood: 'Medium',
        impact: asset.criticality === 'high' ? 'High' : 'Medium'
      });
    }

    if (asset.criticality === 'high') {
      threats.push({
        id: this.generateThreatId(),
        assetId: asset.id,
        assetName: asset.name,
        category: 'Denial of Service',
        description: `${asset.name} could be made unavailable affecting critical functionality`,
        likelihood: 'Low',
        impact: 'High'
      });
    }

    return threats;
  }

  // Identify data threats
  identifyDataThreats(asset) {
    const threats = [];

    if (asset.sensitivity === 'high' || asset.sensitivity === 'critical') {
      threats.push({
        id: this.generateThreatId(),
        assetId: asset.id,
        assetName: asset.name,
        category: 'Information Disclosure',
        description: `Sensitive ${asset.name} data could be exposed`,
        likelihood: 'Medium',
        impact: 'High'
      });

      threats.push({
        id: this.generateThreatId(),
        assetId: asset.id,
        assetName: asset.name,
        category: 'Tampering',
        description: `${asset.name} data could be modified without authorization`,
        likelihood: 'Low',
        impact: 'High'
      });
    }

    return threats;
  }

  // Identify technical threats
  identifyTechnicalThreats(asset) {
    const threats = [];

    if (asset.exposure === 'external' || asset.exposure === 'public') {
      threats.push({
        id: this.generateThreatId(),
        assetId: asset.id,
        assetName: asset.name,
        category: 'Elevation of Privilege',
        description: `Attackers could gain elevated access to ${asset.name}`,
        likelihood: 'Medium',
        impact: 'High'
      });
    }

    if (asset.category === 'web_application' || asset.category === 'api') {
      threats.push({
        id: this.generateThreatId(),
        assetId: asset.id,
        assetName: asset.name,
        category: 'Injection',
        description: `Malicious input could compromise ${asset.name}`,
        likelihood: 'High',
        impact: 'Medium'
      });
    }

    return threats;
  }

  // Generate threat scenarios
  generateThreatScenarios(threats, sprintContext) {
    const scenarios = [];

    for (const threat of threats) {
      scenarios.push({
        id: this.generateScenarioId(),
        threatId: threat.id,
        title: `${threat.category} against ${threat.assetName}`,
        description: threat.description,
        preconditions: this.generatePreconditions(threat),
        attackSteps: this.generateAttackSteps(threat),
        detection: this.generateDetectionMethods(threat),
        sprint: sprintContext?.sprint || 'Current'
      });
    }

    return scenarios;
  }

  // Phase 3: Mitigation Planning
  async planMitigations(threatsPhase) {
    const mitigations = {
      phase: 3,
      name: this.phases[3],
      mitigationPlans: [],
      acceptanceCriteria: [],
      completed: new Date()
    };

    // Create mitigation plans for each threat
    for (const threat of threatsPhase.identifiedThreats) {
      const plan = this.createMitigationPlan(threat);
      mitigations.mitigationPlans.push(plan);
    }

    // Define acceptance criteria
    mitigations.acceptanceCriteria = this.defineAcceptanceCriteria(threatsPhase);

    return mitigations;
  }

  // Create mitigation plan for threat
  createMitigationPlan(threat) {
    return {
      threatId: threat.id,
      assetName: threat.assetName,
      category: threat.category,
      mitigations: this.getMitigationsForCategory(threat.category),
      priority: this.calculatePriority(threat),
      effort: this.estimateEffort(threat),
      owner: 'Development Team',
      sprint: 'Current'
    };
  }

  // Get mitigations for threat category
  getMitigationsForCategory(category) {
    const mitigations = {
      'Spoofing': ['Multi-factor authentication', 'Certificate validation', 'Input validation'],
      'Tampering': ['Integrity checks', 'Digital signatures', 'Access controls'],
      'Repudiation': ['Secure logging', 'Digital signatures', 'Timestamps'],
      'Information Disclosure': ['Encryption', 'Access controls', 'Data classification'],
      'Denial of Service': ['Rate limiting', 'Resource management', 'Load balancing'],
      'Elevation of Privilege': ['Least privilege', 'Access controls', 'Input validation'],
      'Injection': ['Input sanitization', 'Prepared statements', 'Web application firewall']
    };

    return mitigations[category] || ['Security review', 'Additional controls'];
  }

  // Calculate mitigation priority
  calculatePriority(threat) {
    const riskScore = this.calculateRiskScore(threat);

    if (riskScore >= 9) return 'Critical';
    if (riskScore >= 6) return 'High';
    if (riskScore >= 3) return 'Medium';
    return 'Low';
  }

  // Calculate risk score
  calculateRiskScore(threat) {
    const likelihoodScore = { 'Low': 1, 'Medium': 2, 'High': 3 }[threat.likelihood] || 2;
    const impactScore = { 'Low': 1, 'Medium': 2, 'High': 3 }[threat.impact] || 2;

    return likelihoodScore * impactScore;
  }

  // Estimate implementation effort
  estimateEffort(threat) {
    const baseEffort = { 'Low': 2, 'Medium': 5, 'High': 8, 'Critical': 13 }[threat.impact] || 5;
    return `${baseEffort} story points`;
  }

  // Define acceptance criteria
  defineAcceptanceCriteria(threatsPhase) {
    const criteria = [];

    criteria.push('All critical and high priority threats have mitigation plans');
    criteria.push('Mitigation plans are feasible within current sprint');
    criteria.push('Security requirements are documented and testable');
    criteria.push('Threat model is reviewed by security team');

    return criteria;
  }

  // Phase 4: Validation
  async validateModel(mitigationsPhase) {
    const validation = {
      phase: 4,
      name: this.phases[4],
      validationResults: [],
      gaps: [],
      recommendations: [],
      completed: new Date()
    };

    // Validate mitigation completeness
    validation.validationResults = this.validateMitigations(mitigationsPhase);

    // Identify gaps
    validation.gaps = this.identifyGaps(mitigationsPhase);

    // Generate recommendations
    validation.recommendations = this.generateValidationRecommendations(validation);

    return validation;
  }

  // Validate mitigations
  validateMitigations(mitigationsPhase) {
    const results = [];

    for (const plan of mitigationsPhase.mitigationPlans) {
      results.push({
        threatId: plan.threatId,
        mitigationComplete: plan.mitigations.length > 0,
        priorityAppropriate: plan.priority !== 'Low',
        effortEstimated: plan.effort !== undefined,
        ownerAssigned: plan.owner !== undefined
      });
    }

    return results;
  }

  // Identify gaps
  identifyGaps(mitigationsPhase) {
    const gaps = [];

    const highPriorityPlans = mitigationsPhase.mitigationPlans.filter(p => p.priority === 'Critical' || p.priority === 'High');

    if (highPriorityPlans.length === 0) {
      gaps.push('No high-priority threats identified for mitigation');
    }

    const unassignedPlans = mitigationsPhase.mitigationPlans.filter(p => !p.owner || p.owner === 'Development Team');
    if (unassignedPlans.length > 0) {
      gaps.push(`${unassignedPlans.length} mitigation plans lack specific owners`);
    }

    return gaps;
  }

  // Generate visual diagrams
  generateVisualDiagrams(vastModel) {
    const diagrams = {
      assetDiagram: this.generateAssetDiagram(vastModel.phases[1]),
      threatDiagram: this.generateThreatDiagram(vastModel.phases[2]),
      mitigationDiagram: this.generateMitigationDiagram(vastModel.phases[3])
    };

    return diagrams;
  }

  // Generate asset diagram (text representation)
  generateAssetDiagram(assetsPhase) {
    let diagram = 'Asset Overview Diagram\n';
    diagram += '=====================\n\n';

    diagram += 'Functional Assets:\n';
    for (const asset of assetsPhase.functionalAssets) {
      diagram += `- ${asset.name} (${asset.criticality})\n`;
    }

    diagram += '\nData Assets:\n';
    for (const asset of assetsPhase.dataAssets) {
      diagram += `- ${asset.name} (${asset.sensitivity})\n`;
    }

    diagram += '\nTechnical Assets:\n';
    for (const asset of assetsPhase.technicalAssets) {
      diagram += `- ${asset.name} (${asset.category})\n`;
    }

    return diagram;
  }

  // Generate threat diagram
  generateThreatDiagram(threatsPhase) {
    let diagram = 'Threat Overview Diagram\n';
    diagram += '======================\n\n';

    const categories = {};
    for (const threat of threatsPhase.identifiedThreats) {
      if (!categories[threat.category]) {
        categories[threat.category] = [];
      }
      categories[threat.category].push(threat);
    }

    for (const [category, threats] of Object.entries(categories)) {
      diagram += `${category}:\n`;
      for (const threat of threats) {
        diagram += `  - ${threat.assetName}: ${threat.description}\n`;
      }
      diagram += '\n';
    }

    return diagram;
  }

  // Generate mitigation diagram
  generateMitigationDiagram(mitigationsPhase) {
    let diagram = 'Mitigation Overview Diagram\n';
    diagram += '==========================\n\n';

    const priorities = {};
    for (const plan of mitigationsPhase.mitigationPlans) {
      if (!priorities[plan.priority]) {
        priorities[plan.priority] = [];
      }
      priorities[plan.priority].push(plan);
    }

    for (const [priority, plans] of Object.entries(priorities)) {
      diagram += `${priority} Priority:\n`;
      for (const plan of plans) {
        diagram += `  - ${plan.assetName}: ${plan.mitigations.join(', ')}\n`;
      }
      diagram += '\n';
    }

    return diagram;
  }

  // Generate final report
  generateFinalReport(vastModel) {
    const report = {
      summary: {
        systemName: vastModel.systemName,
        sprint: vastModel.sprint,
        totalAssets: vastModel.phases[1].functionalAssets.length +
                    vastModel.phases[1].dataAssets.length +
                    vastModel.phases[1].technicalAssets.length,
        totalThreats: vastModel.phases[2].identifiedThreats.length,
        totalMitigations: vastModel.phases[3].mitigationPlans.length,
        validationStatus: vastModel.phases[4].gaps.length === 0 ? 'Complete' : 'Gaps Identified'
      },
      assets: vastModel.phases[1],
      threats: vastModel.phases[2],
      mitigations: vastModel.phases[3],
      validation: vastModel.phases[4],
      diagrams: vastModel.visualDiagrams,
      recommendations: vastModel.phases[4].recommendations
    };

    return report;
  }

  // Utility methods
  generateAssetId() {
    return `ASSET_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  generateThreatId() {
    return `THREAT_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  generateScenarioId() {
    return `SCENARIO_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  generatePreconditions(threat) {
    const preconditions = ['Network access'];

    if (threat.category === 'Spoofing') {
      preconditions.push('Valid user credentials or bypass');
    }

    if (threat.category === 'Injection') {
      preconditions.push('User input interface');
    }

    return preconditions;
  }

  generateAttackSteps(threat) {
    const steps = [];

    switch (threat.category) {
      case 'Spoofing':
        steps.push('Gather target information', 'Create spoofed identity', 'Attempt access');
        break;
      case 'Tampering':
        steps.push('Identify target data', 'Gain access', 'Modify data', 'Cover tracks');
        break;
      case 'Information Disclosure':
        steps.push('Identify sensitive data location', 'Exploit vulnerability', 'Extract data');
        break;
      default:
        steps.push('Reconnaissance', 'Exploit', 'Achieve objective');
    }

    return steps;
  }

  generateDetectionMethods(threat) {
    const methods = ['Security monitoring', 'Log analysis'];

    if (threat.category === 'Denial of Service') {
      methods.push('Traffic analysis', 'Performance monitoring');
    }

    if (threat.category === 'Injection') {
      methods.push('Input validation monitoring', 'WAF logs');
    }

    return methods;
  }

  generateValidationRecommendations(validation) {
    const recommendations = [];

    if (validation.gaps.length > 0) {
      recommendations.push('Address identified gaps before sprint completion');
    }

    recommendations.push('Review threat model in next sprint planning');
    recommendations.push('Include security stories in backlog');
    recommendations.push('Conduct security testing for implemented features');

    return recommendations;
  }
}

// Example VAST threat modeling
const vastModeler = new VASTThreatModeler();

const systemDescription = {
  name: 'E-Commerce Checkout',
  features: [
    {
      name: 'Payment Processing',
      description: 'Process credit card payments',
      criticality: 'high',
      users: ['customers'],
      dependencies: ['Payment Gateway', 'Database']
    },
    {
      name: 'Order Management',
      description: 'Manage customer orders',
      criticality: 'medium',
      users: ['customers', 'admins'],
      dependencies: ['Database', 'Email Service']
    },
    {
      name: 'User Authentication',
      description: 'User login and registration',
      criticality: 'high',
      users: ['customers', 'admins'],
      dependencies: ['Database', 'Email Service']
    }
  ],
  dataTypes: [
    {
      name: 'Payment Information',
      sensitivity: 'critical',
      volume: 'high',
      access: 'restricted',
      regulations: ['PCI DSS']
    },
    {
      name: 'Customer Data',
      sensitivity: 'high',
      volume: 'medium',
      access: 'internal',
      regulations: ['GDPR']
    },
    {
      name: 'Order History',
      sensitivity: 'medium',
      volume: 'high',
      access: 'user',
      regulations: []
    }
  ],
  components: [
    {
      name: 'Checkout API',
      category: 'api',
      technology: 'Node.js',
      exposure: 'external',
      interfaces: ['REST', 'JSON']
    },
    {
      name: 'Payment Database',
      category: 'database',
      technology: 'PostgreSQL',
      exposure: 'internal',
      interfaces: ['SQL']
    },
    {
      name: 'Auth Service',
      category: 'web_application',
      technology: 'React',
      exposure: 'external',
      interfaces: ['HTTP', 'WebSocket']
    }
  ]
};

const sprintContext = {
  sprint: 'Sprint 15',
  focus: 'Payment security enhancements',
  team: ['Frontend Dev', 'Backend Dev', 'Security Engineer'],
  deadlines: 'End of sprint'
};

const vastModel = await vastModeler.executeVAST(systemDescription, sprintContext);

console.log('VAST Threat Model Results:');
console.log('==========================');
console.log(`System: ${vastModel.finalReport.summary.systemName}`);
console.log(`Sprint: ${vastModel.finalReport.summary.sprint}`);
console.log(`Total Assets: ${vastModel.finalReport.summary.totalAssets}`);
console.log(`Total Threats: ${vastModel.finalReport.summary.totalThreats}`);
console.log(`Validation Status: ${vastModel.finalReport.summary.validationStatus}`);

console.log('\nAsset Diagram:');
console.log(vastModel.visualDiagrams.assetDiagram);

console.log('\nKey Recommendations:');
vastModel.finalReport.recommendations.forEach(rec => {
  console.log(`- ${rec}`);
});
```

### Workshop 4: Industry-Specific Threat Modeling

**Tailored threat modeling for healthcare, finance, and manufacturing**

#### Healthcare Industry Workshop
**Duration:** 6 hours
**Focus:** HIPAA compliance and patient data protection

**Agenda:**
1. Healthcare Threat Landscape (60 min)
2. Patient Data Flow Analysis (90 min)
3. Medical Device Security (90 min)
4. HIPAA Threat Modeling (90 min)
5. Compliance Integration (60 min)

**Key Threats Addressed:**
- PHI data exposure
- Medical device tampering
- Ransomware attacks
- Insider threats
- Supply chain attacks

#### Financial Services Workshop
**Duration:** 6 hours
**Focus:** PCI DSS compliance and financial data protection

**Agenda:**
1. Financial Threat Landscape (60 min)
2. Payment Processing Analysis (90 min)
3. Transaction Security (90 min)
4. Regulatory Compliance (90 min)
5. Fraud Prevention (60 min)

**Key Threats Addressed:**
- Payment data interception
- Transaction tampering
- Account takeover
- Money laundering
- Insider fraud

#### Manufacturing Workshop
**Duration:** 6 hours
**Focus:** OT/ICS security and operational technology

**Agenda:**
1. Industrial Control Systems Overview (60 min)
2. SCADA Network Analysis (90 min)
3. PLC Security Assessment (90 min)
4. Supply Chain Risks (90 min)
5. IEC 62443 Integration (60 min)

**Key Threats Addressed:**
- Production line sabotage
- Equipment tampering
- Network segmentation failures
- Legacy system vulnerabilities
- Third-party vendor risks

### Workshop 5: DevSecOps Threat Modeling Integration

**Duration:** 4 hours
**Focus:** Integrating threat modeling into CI/CD pipelines

**Agenda:**
1. DevSecOps Principles (45 min)
2. Automated Threat Modeling (60 min)
3. Pipeline Integration (60 min)
4. Security Testing Automation (60 min)
5. Metrics and Reporting (45 min)

**Tools Covered:**
- SAST/DAST integration
- Infrastructure as Code security
- Container security scanning
- Automated compliance checks

### Workshop 6: Cloud Threat Modeling

**Duration:** 4 hours
**Focus:** Cloud-native application protection

**Agenda:**
1. Cloud Security Fundamentals (45 min)
2. Infrastructure as Code Analysis (60 min)
3. Microservices Threat Modeling (60 min)
4. Serverless Security (60 min)
5. Multi-Cloud Considerations (45 min)

**Key Threats Addressed:**
- Misconfigured cloud resources
- API gateway vulnerabilities
- Container orchestration attacks
- Serverless function exploits
- Data residency issues

### Workshop 7: IoT and Embedded Systems

**Duration:** 4 hours
**Focus:** Connected device and embedded system security

**Agenda:**
1. IoT Threat Landscape (45 min)
2. Device Communication Analysis (60 min)
3. Firmware Security (60 min)
4. Update Mechanism Security (60 min)
5. Privacy Considerations (45 min)

**Key Threats Addressed:**
- Device spoofing
- Firmware tampering
- Network interception
- Physical attacks
- Supply chain compromises

### Workshop 8: Mobile Application Threat Modeling

**Duration:** 4 hours
**Focus:** Mobile app security and platform-specific threats

**Agenda:**
1. Mobile Threat Landscape (45 min)
2. Platform-Specific Analysis (iOS/Android) (60 min)
3. API Communication Security (60 min)
4. Data Storage Security (60 min)
5. App Store Security (45 min)

**Key Threats Addressed:**
- Reverse engineering
- Man-in-the-middle attacks
- Insecure data storage
- Platform-specific exploits
- Third-party library vulnerabilities

## 📊 Threat Modeling Methodology Comparison Matrix

### Methodology Overview Comparison

| Methodology | Primary Focus | Best For | Complexity | Time Investment | Team Skills Required | Output Format |
|-------------|---------------|----------|------------|-----------------|---------------------|---------------|
| **STRIDE** | Security Properties | Application Security | Low | 2-4 hours | Basic Security Knowledge | Threat Lists |
| **PASTA** | Business Risk | Enterprise Applications | High | 1-2 weeks | Advanced Security + Business | Risk Assessments |
| **OCTAVE** | Organizational Risk | Enterprise-wide | Medium | 2-4 weeks | Mixed Technical/Business | Security Strategy |
| **Trike** | Requirements-driven | Compliance-heavy Systems | High | 1-3 weeks | Security Architects | Requirements Traceability |
| **VAST** | Agile Development | Fast-paced Teams | Low | 1-2 hours per sprint | Development Teams | Actionable Backlog Items |

### Detailed Feature Comparison

#### Threat Identification Approach
| Methodology | Threat Categories | Actor Analysis | Attack Vectors | Prerequisites | Examples Provided |
|-------------|------------------|---------------|---------------|---------------|-------------------|
| **STRIDE** | 6 Categories (Spoofing, Tampering, etc.) | Basic | Limited | Basic | Extensive |
| **PASTA** | Business Impact-based | Comprehensive | Detailed | Comprehensive | Scenario-based |
| **OCTAVE** | Asset-based | Organizational | Infrastructure-focused | Environmental | Case-based |
| **Trike** | Requirements Violation | Capability-based | Trust Boundary | Detailed | Technical |
| **VAST** | Feature-based | Sprint Context | User Story-driven | Minimal | Practical |

#### Risk Assessment Methodology
| Methodology | Risk Calculation | Quantitative | Qualitative | Business Impact | Prioritization |
|-------------|-----------------|--------------|-------------|----------------|---------------|
| **STRIDE** | Impact × Likelihood | Basic Scoring | Category-based | Limited | Manual |
| **PASTA** | Multi-factor Analysis | Advanced Metrics | Business-aligned | Comprehensive | Automated |
| **OCTAVE** | Asset Value × Threat Impact | Moderate | Organizational | High | Criteria-based |
| **Trike** | Attacker Capability × Requirements Weight | Advanced | Requirements-driven | Medium | Mathematical |
| **VAST** | Sprint Impact × Implementation Cost | Simple | Team Consensus | Sprint-focused | Story Points |

#### Mitigation Strategy Approach
| Methodology | Control Types | Implementation Guidance | Validation | Maintenance | Automation Potential |
|-------------|---------------|----------------------|------------|-------------|---------------------|
| **STRIDE** | Security Controls | Basic | Manual Review | Limited | Low |
| **PASTA** | Risk-based Controls | Detailed | Testing Required | Moderate | High |
| **OCTAVE** | Strategic Controls | Comprehensive | Audit-based | High | Medium |
| **Trike** | Requirements Controls | Technical | Formal Verification | High | High |
| **VAST** | Sprint Controls | Agile | Demo-based | Continuous | Very High |

#### Industry Suitability
| Methodology | Web Applications | Enterprise Software | Cloud Services | IoT/Embedded | Mobile Apps | Industrial Control |
|-------------|------------------|-------------------|----------------|--------------|-------------|-------------------|
| **STRIDE** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **PASTA** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **OCTAVE** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Trike** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **VAST** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |

#### Implementation Characteristics
| Methodology | Learning Curve | Tool Support | Template Availability | Customization | Scalability |
|-------------|----------------|--------------|---------------------|---------------|-------------|
| **STRIDE** | Low | Excellent | Extensive | Limited | High |
| **PASTA** | High | Good | Moderate | High | Medium |
| **OCTAVE** | Medium | Moderate | Good | High | High |
| **Trike** | High | Limited | Basic | Very High | Low |
| **VAST** | Low | Emerging | Growing | High | Very High |

### Methodology Selection Guide

#### Choose STRIDE When:
- Building traditional web applications
- Team has basic security knowledge
- Need quick threat identification
- Working with well-understood technologies
- Compliance requirements are minimal

#### Choose PASTA When:
- Business risk is the primary concern
- Large enterprise applications
- Complex regulatory environments
- Need detailed risk quantification
- Executive stakeholder involvement required

#### Choose OCTAVE When:
- Organization-wide security assessment needed
- Mixed technical and business teams
- Long-term security strategy development
- Limited security expertise available
- Focus on operational risk management

#### Choose Trike When:
- Security requirements drive architecture
- Formal verification required
- Compliance-heavy environments
- Academic or research contexts
- Mathematical risk analysis needed

#### Choose VAST When:
- Agile development environment
- 2-week sprint cycles
- Development team drives security
- Continuous integration required
- Rapid feature development

### Hybrid Approach Recommendations

#### Enterprise Agile Development
```
Primary: VAST (for sprint-level modeling)
Secondary: PASTA (for release planning)
Tertiary: STRIDE (for detailed component analysis)
```

#### Compliance-Driven Development
```
Primary: Trike (for requirements traceability)
Secondary: OCTAVE (for organizational compliance)
Tertiary: PASTA (for risk quantification)
```

#### Cloud-Native Applications
```
Primary: STRIDE (for component security)
Secondary: VAST (for agile delivery)
Tertiary: PASTA (for business risk)
```

#### Industrial Control Systems
```
Primary: OCTAVE (for operational risk)
Secondary: PASTA (for business impact)
Tertiary: STRIDE (for technical threats)
```

## 📚 Threat Modeling Resources

### Tools and Software
- **Microsoft Threat Modeling Tool:** Free STRIDE-based tool
- **OWASP Threat Dragon:** Open-source threat modeling tool
- **IriusRisk:** Commercial threat modeling platform
- **ThreatModeler:** Enterprise threat modeling solution

### Templates and Checklists
- STRIDE Questionnaires
- Data Flow Diagram Templates
- Risk Assessment Worksheets
- Mitigation Strategy Guides

### Training and Certification
- Certified Threat Modeling Professional (CTMP)
- OWASP Threat Modeling Training
- Microsoft Security Development Lifecycle (SDL) Training

## 🔗 See Also

- [[MITRE ATT&CK Framework]]
- [[MITRE EMB3D Framework]]
- [[STRIDE Methodology]]
- [[PASTA Methodology]]
- [[Risk Assessment Techniques]]

---

**Threat Modeling:** Systematic approach to identifying and mitigating security threats
**Last Updated:** October 2025
**Methodologies Covered:** STRIDE, PASTA, OCTAVE, Trike, VAST</content>
</xai:function_call name="write">
<parameter name="filePath">/Users/jim/opencode-test/shared/n8n-how/wiki/cybersecurity/iec62443-part1.md