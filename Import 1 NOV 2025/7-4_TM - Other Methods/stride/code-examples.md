# STRIDE Code Examples
## Complete JavaScript Implementation for Threat Modeling

**Version:** 1.0 - October 2025
**Language:** JavaScript/Node.js
**Focus:** STRIDE threat modeling implementation with examples

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Threat Modeling](../../../index.md) > [Methodologies](../../index.md) > [STRIDE](../index.md) > Code Examples

---

## Table of Contents

### Core Implementation
- [[#stride-threat-modeler-class|STRIDE Threat Modeler Class]] - Main implementation
- [[#component-analysis|Component Analysis]] - Threat identification logic
- [[#data-flow-analysis|Data Flow Analysis]] - Flow-based threat detection
- [[#risk-assessment|Risk Assessment]] - Quantitative risk calculation

### Export & Integration
- [[#export-functions|Export Functions]] - Model serialization
- [[#usage-examples|Usage Examples]] - Complete implementation examples
- [[#error-handling|Error Handling]] - Robust error management

---

## 🎯 STRIDE Implementation Overview

The STRIDE implementation provides a complete JavaScript class for automated threat modeling using Microsoft's STRIDE methodology. It analyzes system components, data flows, and trust boundaries to identify security threats across all six STRIDE categories.

### Key Features
- **Automated Analysis:** Structured threat identification for system components
- **Risk Calculation:** Quantitative risk assessment with impact/likelihood scoring
- **Multiple Formats:** Export threat models in JSON, XML, and CSV formats
- **Extensible Design:** Easy to customize for specific organizational needs

---

## STRIDE Threat Modeler Class

```javascript
/**
 * STRIDE Threat Modeling Implementation
 * Automated threat identification using Microsoft's STRIDE methodology
 */
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
}
```

---

## Component Analysis

### Create Threat Model Method

```javascript
/**
 * Create comprehensive threat model for system
 * @param {Array} systemComponents - System components to analyze
 * @param {Array} dataFlows - Data flows between components
 * @param {Array} trustBoundaries - Trust boundaries in the system
 * @returns {Object} Complete threat model
 */
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

  // Analyze each component for threats
  for (const component of systemComponents) {
    const componentThreats = await this.analyzeComponent(component, systemComponents, dataFlows, trustBoundaries);
    model.threats.push(...componentThreats);
  }

  // Analyze data flows for threats
  for (const flow of dataFlows) {
    const flowThreats = await this.analyzeDataFlow(flow, trustBoundaries);
    model.threats.push(...flowThreats);
  }

  // Generate mitigation strategies
  model.mitigations = this.generateMitigations(model.threats);

  // Calculate overall risk assessment
  model.riskAssessment = this.calculateRiskAssessment(model.threats);

  return model;
}
```

### Component Threat Analysis

```javascript
/**
 * Analyze individual component for STRIDE threats
 * @param {Object} component - Component to analyze
 * @param {Array} allComponents - All system components
 * @param {Array} dataFlows - System data flows
 * @param {Array} trustBoundaries - System trust boundaries
 * @returns {Array} Identified threats for this component
 */
async analyzeComponent(component, allComponents, dataFlows, trustBoundaries) {
  const threats = [];

  // Analyze each STRIDE category
  for (const [category, details] of Object.entries(this.strideCategories)) {
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
        riskLevel: this.calculateRiskLevel(threat.impact, threat.likelihood),
        mitigations: threat.mitigations,
        status: 'identified'
      });
    }
  }

  return threats;
}
```

### Threat Applicability Logic

```javascript
/**
 * Find applicable threats for component based on STRIDE category
 * @param {Object} component - Component being analyzed
 * @param {string} category - STRIDE category (Spoofing, Tampering, etc.)
 * @param {Array} allComponents - All system components
 * @param {Array} dataFlows - System data flows
 * @param {Array} trustBoundaries - System trust boundaries
 * @returns {Array} Applicable threats for this category
 */
findApplicableThreats(component, category, allComponents, dataFlows, trustBoundaries) {
  const threats = [];

  switch (category) {
    case 'Spoofing':
      if (component.authenticates || component.publicFacing) {
        threats.push({
          title: 'Authentication bypass',
          description: `${component.name} could be spoofed to gain unauthorized access`,
          impact: component.criticality === 'high' ? 'high' : 'medium',
          likelihood: component.publicFacing ? 'high' : 'medium',
          mitigations: ['Implement multi-factor authentication', 'Use secure session management', 'Validate input thoroughly']
        });
      }
      break;

    case 'Tampering':
      if (component.handlesData) {
        threats.push({
          title: 'Data modification attack',
          description: `Data processed by ${component.name} could be tampered with`,
          impact: component.dataSensitivity === 'high' ? 'high' : 'medium',
          likelihood: 'medium',
          mitigations: ['Implement input validation', 'Use parameterized queries', 'Add integrity checks']
        });
      }
      break;

    case 'Repudiation':
      if (component.hasTransactions || component.logsActions) {
        threats.push({
          title: 'Action repudiation',
          description: `Actions performed by ${component.name} could be denied`,
          impact: 'medium',
          likelihood: 'low',
          mitigations: ['Implement secure audit logging', 'Use digital signatures for transactions', 'Add timestamping']
        });
      }
      break;

    case 'Information Disclosure':
      if (component.handlesData && component.dataSensitivity) {
        threats.push({
          title: 'Information leakage',
          description: `Sensitive information in ${component.name} could be exposed`,
          impact: component.dataSensitivity === 'high' ? 'high' : 'medium',
          likelihood: component.publicFacing ? 'high' : 'medium',
          mitigations: ['Implement access controls', 'Use encryption', 'Apply data classification policies']
        });
      }
      break;

    case 'Denial of Service':
      if (component.publicFacing || component.processesRequests) {
        threats.push({
          title: 'Service disruption',
          description: `${component.name} could be made unavailable through DoS attacks`,
          impact: component.criticality === 'high' ? 'high' : 'medium',
          likelihood: component.publicFacing ? 'high' : 'medium',
          mitigations: ['Implement rate limiting', 'Add resource monitoring', 'Use redundancy and failover']
        });
      }
      break;

    case 'Elevation of Privilege':
      if (component.hasPrivileges || component.managesAccess) {
        threats.push({
          title: 'Privilege escalation',
          description: `Attackers could gain higher privileges through ${component.name}`,
          impact: 'high',
          likelihood: 'medium',
          mitigations: ['Implement least privilege principle', 'Use role-based access control', 'Regular privilege audits']
        });
      }
      break;
  }

  return threats;
}
```

---

## Data Flow Analysis

```javascript
/**
 * Analyze data flow for potential threats
 * @param {Object} flow - Data flow to analyze
 * @param {Array} trustBoundaries - System trust boundaries
 * @returns {Array} Threats identified in this data flow
 */
async analyzeDataFlow(flow, trustBoundaries) {
  const threats = [];

  // Check if flow crosses trust boundaries
  const crossesBoundary = this.crossesTrustBoundary(flow, trustBoundaries);

  if (crossesBoundary) {
    // Information Disclosure threat for unencrypted sensitive data
    if (flow.dataSensitivity === 'high' && !flow.encrypted) {
      threats.push({
        id: this.generateThreatId(),
        category: 'Information Disclosure',
        component: `${flow.source} → ${flow.target}`,
        title: 'Unencrypted sensitive data transmission',
        description: `Data flow from ${flow.source} to ${flow.target} carries sensitive information without encryption`,
        impact: 'high',
        likelihood: 'high',
        riskLevel: 'critical',
        mitigations: ['Implement TLS encryption', 'Use VPN for transport', 'Encrypt sensitive data at rest'],
        status: 'identified'
      });
    }

    // Tampering threat for flows without integrity checks
    if (!flow.integrityCheck) {
      threats.push({
        id: this.generateThreatId(),
        category: 'Tampering',
        component: `${flow.source} → ${flow.target}`,
        title: 'Data integrity not verified',
        description: `Data flow lacks integrity verification mechanisms`,
        impact: 'medium',
        likelihood: 'medium',
        riskLevel: 'high',
        mitigations: ['Implement message authentication codes', 'Use digital signatures', 'Add checksum validation'],
        status: 'identified'
      });
    }
  }

  return threats;
}

/**
 * Check if data flow crosses trust boundary
 * @param {Object} flow - Data flow to check
 * @param {Array} trustBoundaries - Defined trust boundaries
 * @returns {boolean} True if flow crosses boundary
 */
crossesTrustBoundary(flow, trustBoundaries) {
  for (const boundary of trustBoundaries) {
    if ((flow.source === boundary.source && flow.target === boundary.target) ||
        (flow.source === boundary.target && flow.target === boundary.source)) {
      return true;
    }
  }
  return false;
}
```

---

## Risk Assessment

### Risk Level Calculation

```javascript
/**
 * Calculate risk level based on impact and likelihood
 * @param {string} impact - Impact level (low, medium, high)
 * @param {string} likelihood - Likelihood level (low, medium, high)
 * @returns {string} Risk level (low, medium, high, critical)
 */
calculateRiskLevel(impact, likelihood) {
  const riskMatrix = {
    'high-high': 'critical',
    'high-medium': 'high',
    'high-low': 'medium',
    'medium-high': 'high',
    'medium-medium': 'medium',
    'medium-low': 'low',
    'low-high': 'medium',
    'low-medium': 'low',
    'low-low': 'low'
  };

  return riskMatrix[`${impact}-${likelihood}`] || 'medium';
}
```

### Mitigation Generation

```javascript
/**
 * Generate mitigation strategies for identified threats
 * @param {Array} threats - Identified threats
 * @returns {Array} Mitigation plans
 */
generateMitigations(threats) {
  const mitigations = [];

  for (const threat of threats) {
    const mitigation = {
      threatId: threat.id,
      category: threat.category,
      actions: threat.mitigations,
      priority: this.getPriorityFromRisk(threat.riskLevel),
      status: 'pending',
      assignedTo: null,
      dueDate: null
    };

    mitigations.push(mitigation);
  }

  return mitigations;
}

/**
 * Convert risk level to priority
 * @param {string} riskLevel - Risk level
 * @returns {string} Priority level
 */
getPriorityFromRisk(riskLevel) {
  switch (riskLevel) {
    case 'critical': return 'CRITICAL';
    case 'high': return 'HIGH';
    case 'medium': return 'MEDIUM';
    case 'low': return 'LOW';
    default: return 'MEDIUM';
  }
}
```

### Overall Risk Assessment

```javascript
/**
 * Calculate overall risk assessment for threat model
 * @param {Array} threats - All identified threats
 * @returns {Object} Risk assessment summary
 */
calculateRiskAssessment(threats) {
  const assessment = {
    totalThreats: threats.length,
    criticalCount: 0,
    highCount: 0,
    mediumCount: 0,
    lowCount: 0,
    overallRisk: 'low',
    recommendations: []
  };

  // Count threats by risk level
  for (const threat of threats) {
    switch (threat.riskLevel) {
      case 'critical': assessment.criticalCount++; break;
      case 'high': assessment.highCount++; break;
      case 'medium': assessment.mediumCount++; break;
      case 'low': assessment.lowCount++; break;
    }
  }

  // Determine overall risk
  if (assessment.criticalCount > 0) {
    assessment.overallRisk = 'critical';
  } else if (assessment.highCount > 2) {
    assessment.overallRisk = 'high';
  } else if (assessment.highCount > 0 || assessment.mediumCount > 3) {
    assessment.overallRisk = 'medium';
  }

  // Generate recommendations
  assessment.recommendations = this.generateRecommendations(assessment);

  return assessment;
}

/**
 * Generate risk-based recommendations
 * @param {Object} assessment - Risk assessment
 * @returns {Array} Recommendations
 */
generateRecommendations(assessment) {
  const recommendations = [];

  if (assessment.criticalCount > 0) {
    recommendations.push({
      priority: 'CRITICAL',
      action: 'Address all critical threats immediately',
      timeframe: 'Within 1 week',
      rationale: 'Critical threats pose immediate risk to system security'
    });
  }

  if (assessment.highCount > 0) {
    recommendations.push({
      priority: 'HIGH',
      action: 'Implement mitigations for high-risk threats',
      timeframe: 'Within 1 month',
      rationale: 'High-risk threats require prompt attention'
    });
  }

  recommendations.push({
    priority: 'MEDIUM',
    action: 'Review and address medium-risk threats',
    timeframe: 'Within 3 months',
    rationale: 'Medium-risk threats should be monitored and addressed'
  });

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
```

---

## Export Functions

### Export Threat Model

```javascript
/**
 * Export threat model in various formats
 * @param {Object} model - Threat model to export
 * @param {string} format - Export format (json, xml, csv)
 * @returns {string} Exported model
 */
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
```

### XML Export

```javascript
/**
 * Convert threat model to XML format
 * @param {Object} model - Threat model
 * @returns {string} XML representation
 */
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
```

### CSV Export

```javascript
/**
 * Convert threat model to CSV format
 * @param {Object} model - Threat model
 * @returns {string} CSV representation
 */
convertToCSV(model) {
  let csv = 'ID,Category,Title,Risk Level,Component\n';

  for (const threat of model.threats) {
    csv += `${threat.id},${threat.category},"${threat.title}",${threat.riskLevel},${threat.component}\n`;
  }

  return csv;
}
```

---

## Usage Examples

### Complete Implementation Example

```javascript
// Example STRIDE threat modeling usage
const strideModeler = new STRIDEThreatModeler();

// Define system components
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

// Define data flows
const dataFlows = [
  {
    source: 'WebServer',
    target: 'Database',
    dataType: 'user_data',
    dataSensitivity: 'high',
    protocol: 'SQL',
    encrypted: false,
    authenticated: true,
    integrityCheck: false
  },
  {
    source: 'WebServer',
    target: 'AuthService',
    dataType: 'credentials',
    dataSensitivity: 'high',
    protocol: 'HTTPS',
    encrypted: true,
    authenticated: true,
    integrityCheck: true
  }
];

// Define trust boundaries
const trustBoundaries = [
  {
    name: 'Internet-to-DMZ',
    source: 'Internet',
    target: 'DMZ',
    securityLevel: 'low-to-medium'
  },
  {
    name: 'DMZ-to-Internal',
    source: 'DMZ',
    target: 'Internal',
    securityLevel: 'medium-to-high'
  }
];

// Create and run threat model
async function runThreatModeling() {
  try {
    const threatModel = await strideModeler.createThreatModel(systemComponents, dataFlows, trustBoundaries);

    console.log('Threat Model Created:');
    console.log(`System: ${threatModel.systemName}`);
    console.log(`Total Threats: ${threatModel.threats.length}`);
    console.log(`Critical Threats: ${threatModel.riskAssessment.criticalCount}`);
    console.log(`High Threats: ${threatModel.riskAssessment.highCount}`);
    console.log(`Overall Risk: ${threatModel.riskAssessment.overallRisk}`);

    // Export to JSON
    const jsonExport = strideModeler.exportThreatModel(threatModel, 'json');
    console.log('\nJSON Export (first 500 chars):');
    console.log(jsonExport.substring(0, 500) + '...');

  } catch (error) {
    console.error('Error creating threat model:', error);
  }
}

// Execute threat modeling
runThreatModeling();
```

---

## Error Handling

```javascript
/**
 * Enhanced error handling for threat modeling
 */
class STRIDEError extends Error {
  constructor(message, code, details = {}) {
    super(message);
    this.name = 'STRIDEError';
    this.code = code;
    this.details = details;
  }
}

// Enhanced threat modeler with error handling
class RobustSTRIDEThreatModeler extends STRIDEThreatModeler {
  async createThreatModel(systemComponents, dataFlows, trustBoundaries) {
    // Input validation
    if (!Array.isArray(systemComponents) || systemComponents.length === 0) {
      throw new STRIDEError('Invalid system components', 'INVALID_INPUT', { components: systemComponents });
    }

    if (!Array.isArray(dataFlows)) {
      throw new STRIDEError('Invalid data flows', 'INVALID_INPUT', { dataFlows });
    }

    if (!Array.isArray(trustBoundaries)) {
      throw new STRIDEError('Invalid trust boundaries', 'INVALID_INPUT', { trustBoundaries });
    }

    try {
      // Call parent implementation
      return await super.createThreatModel(systemComponents, dataFlows, trustBoundaries);
    } catch (error) {
      throw new STRIDEError(`Threat modeling failed: ${error.message}`, 'MODEL_CREATION_FAILED', { originalError: error });
    }
  }
}
```

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[../index|STRIDE Overview]] | Code Examples | [[./automation|Automation Integration]] |

## See Also

### Related Topics
- [[../template|STRIDE Template]] - Ready-to-use template
- [[./automation|Automation Integration]] - n8n workflow integration
- [[../../../workflows|Workflow Automation]] - Process integration

### Implementation Resources
- [[./automation|Automation Integration]] - n8n workflows
- [[../../../api|API Integration]] - REST API examples
- [[../../../workflows/examples/devsecops|DevSecOps Examples]] - CI/CD integration

---

**Tags:** #stride-implementation #javascript #threat-modeling #code-examples #automation

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 15 minutes
**Difficulty:** Advanced