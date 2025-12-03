# PASTA Implementation Guide
## Code Examples, Automation, and Practical Application

**Version:** 1.0 - October 2025
**Focus:** Complete PASTA implementation with code examples and automation
**Audience:** Developers and security engineers implementing PASTA methodology

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Threat Modeling](../../../index.md) > [Methodologies](../../index.md) > [PASTA](../index.md) > Implementation Guide

---

## Table of Contents

### Implementation Resources
- [[#pasta-threat-modeler|PASTA Threat Modeler Class]] - Core JavaScript implementation
- [[#phase-implementations|Phase Implementation Details]] - Code for each PASTA phase
- [[#risk-calculations|Risk Calculation Engine]] - Quantitative risk assessment
- [[#n8n-integration|n8n Workflow Integration]] - Automated PASTA execution

---

## PASTA Threat Modeling Implementation

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
      created: new Date(),
      version: '1.0'
    };

    try {
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

    } catch (error) {
      console.error('Error executing PASTA methodology:', error);
      throw new Error(`PASTA execution failed: ${error.message}`);
    }
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

  // Identify compliance requirements
  identifyComplianceRequirements(objectives) {
    const complianceReqs = new Set();

    for (const objective of objectives) {
      if (objective.compliance) {
        objective.compliance.forEach(req => complianceReqs.add(req));
      }
    }

    return Array.from(complianceReqs);
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
      if (component.type === 'database' || component.type === 'external_api') {
        exitPoints.push({
          component: component.name,
          type: component.type,
          dataSensitivity: component.dataSensitivity || 'medium',
          encryption: component.encryption || 'none'
        });
      }
    }

    return exitPoints;
  }

  // Define trust levels
  defineTrustLevels(applicationData) {
    const trustLevels = [];

    for (const boundary of applicationData.trustBoundaries) {
      trustLevels.push({
        name: boundary.name,
        sourceLevel: boundary.sourceLevel || 'untrusted',
        targetLevel: boundary.targetLevel || 'trusted',
        securityControls: boundary.controls || []
      });
    }

    return trustLevels;
  }

  // Analyze data flows
  analyzeDataFlows(applicationData) {
    return applicationData.dataFlows.map(flow => ({
      source: flow.source,
      target: flow.target,
      dataType: flow.dataType,
      sensitivity: flow.sensitivity || 'medium',
      encryption: flow.encryption || 'none',
      authentication: flow.authentication || 'none'
    }));
  }

  // Define privilege levels
  definePrivilegeLevels(applicationData) {
    const privilegeLevels = [
      { level: 'public', permissions: ['read_public'], description: 'Unauthenticated users' },
      { level: 'user', permissions: ['read', 'write_own'], description: 'Authenticated users' },
      { level: 'admin', permissions: ['read', 'write', 'delete', 'admin'], description: 'System administrators' }
    ];

    return privilegeLevels;
  }

  // Phase 4: Threat Analysis
  async threatAnalysis(decomposition) {
    const threatAnalysis = {
      phase: 4,
      name: this.phases[4],
      threatActors: [],
      attackVectors: [],
      motivations: [],
      capabilities: [],
      completed: new Date()
    };

    // Analyze threat actors based on entry points and trust levels
    threatAnalysis.threatActors = this.analyzeThreatActors(decomposition);

    // Identify attack vectors
    threatAnalysis.attackVectors = this.identifyAttackVectors(decomposition);

    // Determine motivations
    threatAnalysis.motivations = this.determineMotivations(decomposition);

    // Assess capabilities
    threatAnalysis.capabilities = this.assessCapabilities(threatAnalysis.threatActors);

    return threatAnalysis;
  }

  // Analyze threat actors
  analyzeThreatActors(decomposition) {
    const threatActors = [];

    // External attackers
    if (decomposition.entryPoints.some(ep => ep.type === 'web_interface')) {
      threatActors.push({
        name: 'External Attacker',
        type: 'external',
        motivation: 'Data Theft',
        capability: 'High',
        resources: 'Moderate',
        likelihood: 'High'
      });
    }

    // Internal attackers
    if (decomposition.privilegeLevels.some(pl => pl.level === 'user')) {
      threatActors.push({
        name: 'Insider Threat',
        type: 'internal',
        motivation: 'Sabotage',
        capability: 'Moderate',
        resources: 'High',
        likelihood: 'Medium'
      });
    }

    return threatActors;
  }

  // Identify attack vectors
  identifyAttackVectors(decomposition) {
    const attackVectors = [];

    for (const entryPoint of decomposition.entryPoints) {
      switch (entryPoint.type) {
        case 'web_interface':
          attackVectors.push({
            name: 'Web Application Attack',
            entryPoint: entryPoint.component,
            techniques: ['SQL Injection', 'XSS', 'CSRF'],
            likelihood: 'High',
            impact: 'High'
          });
          break;
        case 'api_endpoint':
          attackVectors.push({
            name: 'API Attack',
            entryPoint: entryPoint.component,
            techniques: ['Parameter Tampering', 'Authentication Bypass'],
            likelihood: 'Medium',
            impact: 'Medium'
          });
          break;
      }
    }

    return attackVectors;
  }

  // Determine motivations
  determineMotivations(decomposition) {
    const motivations = [];

    // Financial gain
    if (decomposition.dataFlows.some(df => df.sensitivity === 'high')) {
      motivations.push({
        type: 'Financial',
        description: 'Monetary gain from data theft or extortion',
        likelihood: 'High'
      });
    }

    // Espionage
    if (decomposition.dataFlows.some(df => df.dataType === 'intellectual_property')) {
      motivations.push({
        type: 'Espionage',
        description: 'Steal competitive intelligence',
        likelihood: 'Medium'
      });
    }

    return motivations;
  }

  // Assess capabilities
  assessCapabilities(threatActors) {
    return threatActors.map(actor => ({
      actor: actor.name,
      technicalSkills: this.assessTechnicalSkills(actor),
      resources: actor.resources,
      persistence: this.assessPersistence(actor),
      detectionAvoidance: this.assessDetectionAvoidance(actor)
    }));
  }

  // Phase 5: Vulnerability Analysis
  async vulnerabilityAnalysis(threatAnalysis, decomposition) {
    const vulnerabilityAnalysis = {
      phase: 5,
      name: this.phases[5],
      vulnerabilities: [],
      exploitability: [],
      existingControls: [],
      gaps: [],
      completed: new Date()
    };

    // Identify vulnerabilities based on decomposition
    vulnerabilityAnalysis.vulnerabilities = this.identifyVulnerabilities(decomposition);

    // Assess exploitability
    vulnerabilityAnalysis.exploitability = this.assessExploitability(vulnerabilityAnalysis.vulnerabilities, threatAnalysis);

    // Evaluate existing controls
    vulnerabilityAnalysis.existingControls = this.evaluateExistingControls(decomposition);

    // Identify gaps
    vulnerabilityAnalysis.gaps = this.identifyGaps(vulnerabilityAnalysis.vulnerabilities, vulnerabilityAnalysis.existingControls);

    return vulnerabilityAnalysis;
  }

  // Identify vulnerabilities
  identifyVulnerabilities(decomposition) {
    const vulnerabilities = [];

    // Check entry points for common vulnerabilities
    for (const entryPoint of decomposition.entryPoints) {
      if (entryPoint.inputValidation === 'basic' || entryPoint.inputValidation === 'none') {
        vulnerabilities.push({
          id: `VULN-${entryPoint.component}-001`,
          component: entryPoint.component,
          type: 'Input Validation Weakness',
          severity: 'High',
          cwe: 'CWE-20',
          description: 'Insufficient input validation may allow injection attacks'
        });
      }
    }

    // Check data flows for encryption issues
    for (const flow of decomposition.dataFlows) {
      if (flow.sensitivity === 'high' && flow.encryption === 'none') {
        vulnerabilities.push({
          id: `VULN-${flow.source}-${flow.target}-001`,
          component: `${flow.source} → ${flow.target}`,
          type: 'Unencrypted Data Transmission',
          severity: 'Critical',
          cwe: 'CWE-319',
          description: 'Sensitive data transmitted without encryption'
        });
      }
    }

    return vulnerabilities;
  }

  // Assess exploitability
  assessExploitability(vulnerabilities, threatAnalysis) {
    return vulnerabilities.map(vuln => ({
      vulnerabilityId: vuln.id,
      technicalComplexity: this.calculateTechnicalComplexity(vuln),
      resourceRequirements: this.calculateResourceRequirements(vuln, threatAnalysis),
      detectionRisk: this.calculateDetectionRisk(vuln),
      remediationTime: this.calculateRemediationTime(vuln)
    }));
  }

  // Phase 6: Attack Modeling
  async attackModeling(vulnerabilityAnalysis) {
    const attackModeling = {
      phase: 6,
      name: this.phases[6],
      attackTrees: [],
      attackScenarios: [],
      successProbabilities: [],
      criticalPaths: [],
      completed: new Date()
    };

    // Build attack trees
    attackModeling.attackTrees = this.buildAttackTrees(vulnerabilityAnalysis);

    // Develop attack scenarios
    attackModeling.attackScenarios = this.developAttackScenarios(attackModeling.attackTrees);

    // Calculate success probabilities
    attackModeling.successProbabilities = this.calculateSuccessProbabilities(attackModeling.attackScenarios);

    // Identify critical paths
    attackModeling.criticalPaths = this.identifyCriticalPaths(attackModeling.attackTrees);

    return attackModeling;
  }

  // Build attack trees
  buildAttackTrees(vulnerabilityAnalysis) {
    const attackTrees = [];

    // Create attack tree for data breach
    const dataBreachTree = {
      root: 'Data Breach Achieved',
      children: [
        {
          node: 'Initial Access',
          probability: 0.8,
          children: [
            {
              node: 'Exploit Web Vulnerability',
              probability: 0.6,
              vulnerabilities: vulnerabilityAnalysis.vulnerabilities.filter(v => v.type.includes('Web'))
            },
            {
              node: 'Phishing Attack',
              probability: 0.4,
              prerequisites: ['User Training Gap']
            }
          ]
        },
        {
          node: 'Privilege Escalation',
          probability: 0.7,
          children: [
            {
              node: 'Exploit Local Vulnerability',
              probability: 0.5,
              vulnerabilities: vulnerabilityAnalysis.vulnerabilities.filter(v => v.type.includes('Local'))
            }
          ]
        }
      ]
    };

    attackTrees.push(dataBreachTree);
    return attackTrees;
  }

  // Phase 7: Risk Analysis
  async riskAnalysis(attackModeling) {
    const riskAnalysis = {
      phase: 7,
      name: this.phases[7],
      riskScores: [],
      riskMatrix: [],
      prioritization: [],
      businessImpact: [],
      completed: new Date()
    };

    // Calculate risk scores
    riskAnalysis.riskScores = this.calculateRiskScores(attackModeling);

    // Build risk matrix
    riskAnalysis.riskMatrix = this.buildRiskMatrix(riskAnalysis.riskScores);

    // Prioritize risks
    riskAnalysis.prioritization = this.prioritizeRisks(riskAnalysis.riskScores);

    // Assess business impact
    riskAnalysis.businessImpact = this.assessBusinessImpact(riskAnalysis.prioritization);

    return riskAnalysis;
  }

  // Calculate risk scores
  calculateRiskScores(attackModeling) {
    const riskScores = [];

    for (const scenario of attackModeling.attackScenarios) {
      const likelihood = this.riskFactors.likelihood[scenario.likelihood] || 3;
      const impact = this.riskFactors.impact[scenario.impact] || 3;
      const exploitability = this.riskFactors.exploitability[scenario.exploitability] || 3;

      const riskScore = (likelihood * impact * exploitability) / 27; // Normalized to 0-5 scale

      riskScores.push({
        scenario: scenario.name,
        likelihood: likelihood,
        impact: impact,
        exploitability: exploitability,
        riskScore: riskScore,
        riskLevel: this.getRiskLevel(riskScore)
      });
    }

    return riskScores;
  }

  // Get risk level from score
  getRiskLevel(score) {
    if (score >= 4) return 'Critical';
    if (score >= 3) return 'High';
    if (score >= 2) return 'Medium';
    return 'Low';
  }

  // Phase 8: Residual Risk Analysis
  async residualRiskAnalysis(riskAnalysis) {
    const residualAnalysis = {
      phase: 8,
      name: this.phases[8],
      originalRisks: riskAnalysis.riskScores,
      mitigations: [],
      residualRisks: [],
      riskTreatment: [],
      monitoringPlan: [],
      completed: new Date()
    };

    // Identify mitigations
    residualAnalysis.mitigations = this.identifyMitigations(riskAnalysis);

    // Calculate residual risks
    residualAnalysis.residualRisks = this.calculateResidualRisks(riskAnalysis.riskScores, residualAnalysis.mitigations);

    // Determine risk treatment
    residualAnalysis.riskTreatment = this.determineRiskTreatment(residualAnalysis.residualRisks);

    // Develop monitoring plan
    residualAnalysis.monitoringPlan = this.developMonitoringPlan(residualAnalysis.residualRisks);

    return residualAnalysis;
  }

  // Generate final assessment
  generateFinalAssessment(pastaModel) {
    const assessment = {
      overallRiskLevel: 'Low',
      criticalRisks: 0,
      highRisks: 0,
      mediumRisks: 0,
      lowRisks: 0,
      riskTrend: 'Stable',
      recommendations: []
    };

    // Count risks by level
    for (const risk of pastaModel.phases[8].residualRisks) {
      switch (risk.level) {
        case 'Critical': assessment.criticalRisks++; break;
        case 'High': assessment.highRisks++; break;
        case 'Medium': assessment.mediumRisks++; break;
        case 'Low': assessment.lowRisks++; break;
      }
    }

    // Determine overall risk level
    if (assessment.criticalRisks > 0) {
      assessment.overallRiskLevel = 'Critical';
    } else if (assessment.highRisks > 2) {
      assessment.overallRiskLevel = 'High';
    } else if (assessment.highRisks > 0 || assessment.mediumRisks > 3) {
      assessment.overallRiskLevel = 'Medium';
    }

    return assessment;
  }

  // Generate recommendations
  generateRecommendations(pastaModel) {
    const recommendations = [];

    const assessment = pastaModel.finalRiskAssessment;

    if (assessment.criticalRisks > 0) {
      recommendations.push({
        priority: 'Critical',
        action: 'Implement immediate mitigations for all critical risks',
        timeframe: 'Within 30 days',
        rationale: 'Critical risks pose immediate threat to business objectives'
      });
    }

    if (assessment.highRisks > 0) {
      recommendations.push({
        priority: 'High',
        action: 'Address high-risk items in next development cycle',
        timeframe: 'Within 90 days',
        rationale: 'High risks require prompt attention'
      });
    }

    recommendations.push({
      priority: 'Medium',
      action: 'Include PASTA threat modeling in development process',
      timeframe: 'Ongoing',
      rationale: 'Ensure systematic security analysis'
    });

    return recommendations;
  }

  // Export PASTA model
  exportPASTAModel(model, format = 'json') {
    switch (format) {
      case 'json':
        return JSON.stringify(model, null, 2);
      case 'xml':
        return this.convertPASTAToXML(model);
      default:
        return JSON.stringify(model, null, 2);
    }
  }
}

// Example PASTA execution
const pastaModeler = new PASTAThreatModeler();

const applicationData = {
  name: 'E-Commerce Platform',
  components: [
    {
      name: 'WebFrontend',
      type: 'web_interface',
      authentication: 'session_based',
      inputValidation: 'advanced'
    },
    {
      name: 'APIGateway',
      type: 'api_endpoint',
      authentication: 'jwt',
      inputValidation: 'advanced'
    },
    {
      name: 'UserDatabase',
      type: 'database',
      dataSensitivity: 'high',
      encryption: 'at_rest'
    }
  ],
  dataFlows: [
    {
      source: 'WebFrontend',
      target: 'APIGateway',
      dataType: 'user_credentials',
      sensitivity: 'high',
      encryption: 'tls',
      authentication: 'session'
    },
    {
      source: 'APIGateway',
      target: 'UserDatabase',
      dataType: 'user_data',
      sensitivity: 'high',
      encryption: 'tls',
      authentication: 'jwt'
    }
  ],
  trustBoundaries: [
    {
      name: 'Internet-to-App',
      sourceLevel: 'untrusted',
      targetLevel: 'authenticated',
      controls: ['TLS', 'Authentication']
    }
  ]
};

const businessObjectives = [
  {
    type: 'confidentiality',
    description: 'Protect customer PII and payment data',
    priority: 'Critical',
    compliance: ['PCI-DSS', 'GDPR']
  },
  {
    type: 'availability',
    description: 'Ensure 99.9% uptime for customer transactions',
    priority: 'High',
    compliance: ['PCI-DSS']
  }
];

// Execute PASTA
async function runPASTA() {
  try {
    const pastaModel = await pastaModeler.executePASTA(applicationData, businessObjectives);

    console.log('PASTA Analysis Complete:');
    console.log(`Application: ${pastaModel.applicationName}`);
    console.log(`Overall Risk Level: ${pastaModel.finalRiskAssessment.overallRiskLevel}`);
    console.log(`Critical Risks: ${pastaModel.finalRiskAssessment.criticalRisks}`);
    console.log(`High Risks: ${pastaModel.finalRiskAssessment.highRisks}`);

    // Export results
    const jsonExport = pastaModeler.exportPASTAModel(pastaModel, 'json');
    console.log('\nModel exported successfully');

  } catch (error) {
    console.error('PASTA execution failed:', error);
  }
}

// Run the example
runPASTA();
```

---

## n8n Workflow Integration

### PASTA Threat Modeling Automation Workflow

```json
{
  "name": "PASTA Threat Modeling Automation",
  "nodes": [
    {
      "parameters": {
        "values": {
          "string": [
            {
              "name": "applicationName",
              "value": "={{ $json.applicationName }}"
            },
            {
              "name": "businessObjectives",
              "value": "={{ $json.businessObjectives }}"
            }
          ]
        },
        "options": {}
      },
      "name": "Load Application Data",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "functionCode": "
// Phase 1: Define Business Objectives
const objectives = $node['Load Application Data'].json.businessObjectives;
const securityObjectives = [];

for (const obj of objectives) {
  switch (obj.type) {
    case 'confidentiality':
      securityObjectives.push({
        type: 'Protect sensitive data',
        priority: obj.priority,
        compliance: obj.compliance
      });
      break;
    case 'availability':
      securityObjectives.push({
        type: 'Ensure system availability',
        priority: obj.priority,
        compliance: obj.compliance
      });
      break;
  }
}

return { securityObjectives, phase1Complete: true };
        "
      },
      "name": "Phase 1: Business Objectives",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [460, 300]
    },
    {
      "parameters": {
        "functionCode": "
// Phase 3: Application Decomposition
const components = $node['Load Application Data'].json.components || [];
const entryPoints = [];
const trustLevels = [];

for (const component of components) {
  if (component.type === 'web_interface' || component.type === 'api_endpoint') {
    entryPoints.push({
      component: component.name,
      type: component.type,
      authentication: component.authentication || 'none'
    });
  }
}

return { entryPoints, trustLevels, phase3Complete: true };
        "
      },
      "name": "Phase 3: Decomposition",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [680, 300]
    },
    {
      "parameters": {
        "functionCode": "
// Phase 7: Risk Analysis
const entryPoints = $node['Phase 3: Decomposition'].json.entryPoints;
const risks = [];

for (const ep of entryPoints) {
  if (ep.authentication === 'none') {
    risks.push({
      component: ep.component,
      risk: 'Unauthenticated access',
      level: 'High',
      likelihood: 'High',
      impact: 'Critical'
    });
  }
}

return { risks, phase7Complete: true };
        "
      },
      "name": "Phase 7: Risk Analysis",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [900, 300]
    },
    {
      "parameters": {
        "functionCode": "
// Generate Report
const risks = $node['Phase 7: Risk Analysis'].json.risks;
const report = {
  title: 'PASTA Threat Model Report',
  generated: new Date().toISOString(),
  totalRisks: risks.length,
  highRisks: risks.filter(r => r.level === 'High').length,
  summary: risks.length > 0 ? 'Security improvements recommended' : 'No critical issues found'
};

return { report };
        "
      },
      "name": "Generate Report",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [1120, 300]
    }
  ],
  "connections": {
    "Load Application Data": {
      "main": [
        [
          {
            "node": "Phase 1: Business Objectives",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Phase 1: Business Objectives": {
      "main": [
        [
          {
            "node": "Phase 3: Decomposition",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Phase 3: Decomposition": {
      "main": [
        [
          {
            "node": "Phase 7: Risk Analysis",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Phase 7: Risk Analysis": {
      "main": [
        [
          {
            "node": "Generate Report",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

---

## Implementation Best Practices

### Code Integration
1. **Modular Architecture:** Break PASTA phases into separate functions for maintainability
2. **Error Handling:** Implement comprehensive error handling for each phase
3. **Data Validation:** Validate inputs at each phase to ensure data integrity
4. **Logging:** Add detailed logging for audit trails and debugging

### Automation Considerations
1. **Workflow Triggers:** Execute PASTA on application changes or deployments
2. **Integration Points:** Connect with CI/CD pipelines and security tools
3. **Reporting:** Generate automated reports for different stakeholder groups
4. **Approval Workflows:** Include review and approval steps in automation

### Business Alignment
1. **Stakeholder Involvement:** Include business stakeholders in phase reviews
2. **Risk Communication:** Translate technical risks into business impact
3. **Compliance Mapping:** Link security controls to compliance requirements
4. **ROI Analysis:** Demonstrate security investment returns

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[./phases|PASTA Phases]] | Implementation Guide | [[./template|PASTA Template]] |

## See Also

### Related Topics
- [[../index|PASTA Framework]] - Framework overview
- [[./phases|PASTA Phases]] - Detailed methodology
- [[./risk-analysis|Risk Analysis Framework]] - Risk calculation details

### Implementation Resources
- [[./template|PASTA Template]] - Ready-to-use template
- [[../../../workflows/examples/compliance-monitoring|Compliance Workflows]] - Integration examples
- [[../../../resources/tools|Threat Modeling Tools]] - PASTA-compatible tools

---

**Tags:** #pasta-implementation #code-examples #automation #javascript #n8n-workflows #risk-analysis

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 20 minutes
**Difficulty:** Advanced