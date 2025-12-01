# VAST Implementation Guide
## Code Examples and Automation for Agile Threat Modeling

**Version:** 1.0 - October 2025
**Language:** JavaScript/Node.js
**Focus:** Automated VAST methodology execution

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Threat Modeling](../../../index.md) > [Methodologies](../../index.md) > [VAST](../index.md) > Implementation

---

## Table of Contents

### Core Implementation
- [[#vast-threat-modeler-class|VAST Threat Modeler Class]] - Main implementation
- [[#phase-implementations|Phase Implementations]] - Individual phase logic
- [[#utility-methods|Utility Methods]] - Helper functions

### Integration Examples
- [[#system-description-format|System Description Format]] - Input data structure
- [[#sprint-context|Sprint Context]] - Agile context integration
- [[#execution-example|Execution Example]] - Complete usage example

### Advanced Features
- [[#visual-diagram-generation|Visual Diagram Generation]] - Text-based diagrams
- [[#report-generation|Report Generation]] - Final report creation
- [[#validation-logic|Validation Logic]] - Completeness checking

---

## 🎯 Implementation Overview

The VAST implementation provides a complete JavaScript class for automated threat modeling in agile environments. It follows the four-phase VAST methodology with automated analysis, diagram generation, and report creation.

### Key Features
- **Automated Analysis:** Structured threat identification and mitigation planning
- **Visual Diagrams:** Text-based diagrams for quick visualization
- **Sprint Integration:** Context-aware analysis for agile development
- **Validation:** Automated completeness checking and gap identification

---

## VAST Threat Modeler Class

```javascript
/**
 * VAST (Visual, Agile, and Simple Threat Modeling) Implementation
 * Designed for agile development environments with sprint-based analysis
 */
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

  /**
   * Execute complete VAST methodology
   * @param {Object} systemDescription - System components and data
   * @param {Object} sprintContext - Current sprint information
   * @returns {Object} Complete VAST threat model
   */
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
}
```

---

## Phase Implementations

### Phase 1: Asset Identification

```javascript
/**
 * Phase 1: Asset Identification
 * Identify functional, data, and technical assets
 */
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

/**
 * Extract functional assets from system description
 */
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

/**
 * Extract data assets from system description
 */
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

/**
 * Extract technical assets from system description
 */
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
```

### Phase 2: Threat Identification

```javascript
/**
 * Phase 2: Threat Identification
 * Identify threats for each asset using simplified categories
 */
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

/**
 * Identify threats for specific asset
 */
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

/**
 * Identify functional threats
 */
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

/**
 * Identify data threats
 */
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

/**
 * Identify technical threats
 */
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
```

### Phase 3: Mitigation Planning

```javascript
/**
 * Phase 3: Mitigation Planning
 * Develop practical mitigation strategies
 */
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

/**
 * Create mitigation plan for threat
 */
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

/**
 * Get mitigations for threat category
 */
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

/**
 * Calculate mitigation priority
 */
calculatePriority(threat) {
  const riskScore = this.calculateRiskScore(threat);

  if (riskScore >= 9) return 'Critical';
  if (riskScore >= 6) return 'High';
  if (riskScore >= 3) return 'Medium';
  return 'Low';
}

/**
 * Calculate risk score
 */
calculateRiskScore(threat) {
  const likelihoodScore = { 'Low': 1, 'Medium': 2, 'High': 3 }[threat.likelihood] || 2;
  const impactScore = { 'Low': 1, 'Medium': 2, 'High': 3 }[threat.impact] || 2;

  return likelihoodScore * impactScore;
}

/**
 * Estimate implementation effort
 */
estimateEffort(threat) {
  const baseEffort = { 'Low': 2, 'Medium': 5, 'High': 8, 'Critical': 13 }[threat.impact] || 5;
  return `${baseEffort} story points`;
}
```

### Phase 4: Validation

```javascript
/**
 * Phase 4: Validation
 * Validate completeness and identify gaps
 */
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

/**
 * Validate mitigations
 */
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

/**
 * Identify gaps
 */
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
```

---

## Utility Methods

```javascript
/**
 * Generate unique asset ID
 */
generateAssetId() {
  return `ASSET_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Generate unique threat ID
 */
generateThreatId() {
  return `THREAT_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Generate unique scenario ID
 */
generateScenarioId() {
  return `SCENARIO_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Generate preconditions for threat
 */
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

/**
 * Generate attack steps for threat
 */
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

/**
 * Generate detection methods for threat
 */
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
```

---

## Visual Diagram Generation

```javascript
/**
 * Generate visual diagrams for the threat model
 */
generateVisualDiagrams(vastModel) {
  const diagrams = {
    assetDiagram: this.generateAssetDiagram(vastModel.phases[1]),
    threatDiagram: this.generateThreatDiagram(vastModel.phases[2]),
    mitigationDiagram: this.generateMitigationDiagram(vastModel.phases[3])
  };

  return diagrams;
}

/**
 * Generate asset diagram (text representation)
 */
generateAssetDiagram(assetsPhase) {
  let diagram = 'Asset Overview Diagram\\n';
  diagram += '=====================\\n\\n';

  diagram += 'Functional Assets:\\n';
  for (const asset of assetsPhase.functionalAssets) {
    diagram += `- ${asset.name} (${asset.criticality})\\n`;
  }

  diagram += '\\nData Assets:\\n';
  for (const asset of assetsPhase.dataAssets) {
    diagram += `- ${asset.name} (${asset.sensitivity})\\n`;
  }

  diagram += '\\nTechnical Assets:\\n';
  for (const asset of assetsPhase.technicalAssets) {
    diagram += `- ${asset.name} (${asset.category})\\n`;
  }

  return diagram;
}

/**
 * Generate threat diagram
 */
generateThreatDiagram(threatsPhase) {
  let diagram = 'Threat Overview Diagram\\n';
  diagram += '======================\\n\\n';

  const categories = {};
  for (const threat of threatsPhase.identifiedThreats) {
    if (!categories[threat.category]) {
      categories[threat.category] = [];
    }
    categories[threat.category].push(threat);
  }

  for (const [category, threats] of Object.entries(categories)) {
    diagram += `${category}:\\n`;
    for (const threat of threats) {
      diagram += `  - ${threat.assetName}: ${threat.description}\\n`;
    }
    diagram += '\\n';
  }

  return diagram;
}

/**
 * Generate mitigation diagram
 */
generateMitigationDiagram(mitigationsPhase) {
  let diagram = 'Mitigation Overview Diagram\\n';
  diagram += '==========================\\n\\n';

  const priorities = {};
  for (const plan of mitigationsPhase.mitigationPlans) {
    if (!priorities[plan.priority]) {
      priorities[plan.priority] = [];
    }
    priorities[plan.priority].push(plan);
  }

  for (const [priority, plans] of Object.entries(priorities)) {
    diagram += `${priority} Priority:\\n`;
    for (const plan of plans) {
      diagram += `  - ${plan.assetName}: ${plan.mitigations.join(', ')}\\n`;
    }
    diagram += '\\n';
  }

  return diagram;
}
```

---

## Report Generation

```javascript
/**
 * Generate final report
 */
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

/**
 * Generate validation recommendations
 */
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
```

---

## System Description Format

```javascript
// Example system description structure
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
```

---

## Sprint Context

```javascript
// Sprint context for agile integration
const sprintContext = {
  sprint: 'Sprint 15',
  focus: 'Payment security enhancements',
  team: ['Frontend Dev', 'Backend Dev', 'Security Engineer'],
  deadlines: 'End of sprint'
};
```

---

## Execution Example

```javascript
// Complete VAST threat modeling execution
const vastModeler = new VASTThreatModeler();

const vastModel = await vastModeler.executeVAST(systemDescription, sprintContext);

console.log('VAST Threat Model Results:');
console.log('==========================');
console.log(`System: ${vastModel.finalReport.summary.systemName}`);
console.log(`Sprint: ${vastModel.finalReport.summary.sprint}`);
console.log(`Total Assets: ${vastModel.finalReport.summary.totalAssets}`);
console.log(`Total Threats: ${vastModel.finalReport.summary.totalThreats}`);
console.log(`Validation Status: ${vastModel.finalReport.summary.validationStatus}`);

console.log('\\nAsset Diagram:');
console.log(vastModel.visualDiagrams.assetDiagram);

console.log('\\nKey Recommendations:');
vastModel.finalReport.recommendations.forEach(rec => {
  console.log(`- ${rec}`);
});
```

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[./phases|VAST Phases]] | VAST Implementation | [[./template|VAST Template]] |

## See Also

### Related Topics
- [[../stride/implementation|STRIDE Implementation]] - Technical threat modeling code
- [[../pasta/implementation|PASTA Implementation]] - Risk analysis automation
- [[../../../workflows/examples/devsecops|DevSecOps Automation]] - CI/CD integration

### Integration Resources
- [[./template|VAST Template]] - Ready-to-use templates
- [[../../../api|API Integration]] - REST API examples
- [[../../../workflows|Workflow Automation]] - Pipeline integration

---

**Tags:** #vast-implementation #javascript #automation #agile-threat-modeling #code-examples

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 20 minutes
**Difficulty:** Advanced