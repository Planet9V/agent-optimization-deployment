# STRIDE Automation Integration
## n8n Workflow Integration for Automated Threat Modeling

**Version:** 1.0 - October 2025
**Platform:** n8n
**Focus:** Automated STRIDE threat modeling workflows

---

## Breadcrumb Navigation
[Home](../../../../index.md) > [Threat Modeling](../../../index.md) > [Methodologies](../../index.md) > [STRIDE](../index.md) > Automation

---

## Table of Contents

### Workflow Integration
- [[#stride-workflow-overview|STRIDE Workflow Overview]] - Complete n8n workflow
- [[#workflow-components|Workflow Components]] - Individual workflow nodes
- [[#automation-triggers|Automation Triggers]] - When to run automated threat modeling

### Advanced Automation
- [[#ci-cd-integration|CI/CD Integration]] - Pipeline integration
- [[#reporting-automation|Reporting Automation]] - Automated report generation
- [[#alert-integration|Alert Integration]] - Notification systems

### Configuration
- [[#workflow-configuration|Workflow Configuration]] - Setup and configuration
- [[#custom-nodes|Custom Nodes]] - Extending n8n for STRIDE
- [[#error-handling|Error Handling]] - Robust automation

---

## 🎯 Automation Overview

The STRIDE automation integration provides complete n8n workflows for automated threat modeling. These workflows can be triggered by various events and integrate with development pipelines, security tools, and reporting systems.

### Key Features
- **Event-Driven:** Trigger threat modeling on code changes, deployments, or schedule
- **Multi-Format Output:** Generate reports in various formats (JSON, CSV, PDF)
- **Integration Ready:** Connect with Jira, Slack, email, and security tools
- **Scalable:** Handle multiple systems and complex architectures

---

## STRIDE Workflow Overview

### Complete n8n Workflow JSON

```json
{
  "name": "STRIDE Threat Modeling Automation",
  "nodes": [
    {
      "parameters": {
        "values": {
          "string": [
            {
              "name": "systemName",
              "value": "={{ $json.systemName }}"
            },
            {
              "name": "components",
              "value": "={{ $json.components }}"
            }
          ]
        },
        "options": {}
      },
      "name": "Set System Context",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [
        240,
        300
      ]
    },
    {
      "parameters": {
        "functionCode": "
// STRIDE threat identification logic
const components = $node['Set System Context'].json.components;
const threats = [];

const strideCategories = {
  'Spoofing': { weight: 0.8, examples: ['Identity spoofing', 'Session hijacking'] },
  'Tampering': { weight: 0.9, examples: ['Data modification', 'Code injection'] },
  'Repudiation': { weight: 0.6, examples: ['Log manipulation', 'Transaction denial'] },
  'Information Disclosure': { weight: 0.9, examples: ['Data leakage', 'Privacy violation'] },
  'Denial of Service': { weight: 0.7, examples: ['Resource exhaustion', 'Network flooding'] },
  'Elevation of Privilege': { weight: 0.95, examples: ['Privilege escalation', 'Role manipulation'] }
};

for (const component of components) {
  for (const [category, details] of Object.entries(strideCategories)) {
    // Apply STRIDE logic based on component properties
    if (component.publicFacing && category === 'Spoofing') {
      threats.push({
        id: `STRIDE_${category}_${component.name}_${Date.now()}`,
        category: category,
        component: component.name,
        title: `${category} threat against ${component.name}`,
        impact: component.criticality === 'high' ? 'high' : 'medium',
        likelihood: 'high',
        riskLevel: 'high',
        mitigations: details.examples.map(example => `Prevent ${example}`)
      });
    }

    if (component.handlesData && category === 'Tampering') {
      threats.push({
        id: `STRIDE_${category}_${component.name}_${Date.now()}`,
        category: category,
        component: component.name,
        title: `${category} threat against ${component.name}`,
        impact: component.dataSensitivity === 'high' ? 'high' : 'medium',
        likelihood: 'medium',
        riskLevel: 'medium',
        mitigations: details.examples.map(example => `Prevent ${example}`)
      });
    }

    if (component.hasTransactions && category === 'Repudiation') {
      threats.push({
        id: `STRIDE_${category}_${component.name}_${Date.now()}`,
        category: category,
        component: component.name,
        title: `${category} threat against ${component.name}`,
        impact: 'medium',
        likelihood: 'low',
        riskLevel: 'low',
        mitigations: details.examples.map(example => `Prevent ${example}`)
      });
    }

    if (component.handlesData && component.dataSensitivity && category === 'Information Disclosure') {
      threats.push({
        id: `STRIDE_${category}_${component.name}_${Date.now()}`,
        category: category,
        component: component.name,
        title: `${category} threat against ${component.name}`,
        impact: component.dataSensitivity === 'high' ? 'high' : 'medium',
        likelihood: component.publicFacing ? 'high' : 'medium',
        riskLevel: component.publicFacing && component.dataSensitivity === 'high' ? 'critical' : 'medium',
        mitigations: details.examples.map(example => `Prevent ${example}`)
      });
    }

    if ((component.publicFacing || component.processesRequests) && category === 'Denial of Service') {
      threats.push({
        id: `STRIDE_${category}_${component.name}_${Date.now()}`,
        category: category,
        component: component.name,
        title: `${category} threat against ${component.name}`,
        impact: component.criticality === 'high' ? 'high' : 'medium',
        likelihood: component.publicFacing ? 'high' : 'medium',
        riskLevel: component.publicFacing && component.criticality === 'high' ? 'critical' : 'medium',
        mitigations: details.examples.map(example => `Prevent ${example}`)
      });
    }

    if ((component.hasPrivileges || component.managesAccess) && category === 'Elevation of Privilege') {
      threats.push({
        id: `STRIDE_${category}_${component.name}_${Date.now()}`,
        category: category,
        component: component.name,
        title: `${category} threat against ${component.name}`,
        impact: 'high',
        likelihood: 'medium',
        riskLevel: 'high',
        mitigations: details.examples.map(example => `Prevent ${example}`)
      });
    }
  }
}

return { threats, componentCount: components.length, threatCount: threats.length };
        "
      },
      "name": "STRIDE Analysis",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        460,
        300
      ]
    },
    {
      "parameters": {
        "functionCode": "
// Risk assessment calculation
const threats = $node['STRIDE Analysis'].json.threats;
const componentCount = $node['STRIDE Analysis'].json.componentCount;

let criticalCount = 0;
let highCount = 0;
let mediumCount = 0;
let lowCount = 0;

for (const threat of threats) {
  switch (threat.riskLevel) {
    case 'critical': criticalCount++; break;
    case 'high': highCount++; break;
    case 'medium': mediumCount++; break;
    case 'low': lowCount++; break;
  }
}

// Calculate overall risk
let overallRisk = 'low';
if (criticalCount > 0) {
  overallRisk = 'critical';
} else if (highCount > 2) {
  overallRisk = 'high';
} else if (highCount > 0 || mediumCount > 3) {
  overallRisk = 'medium';
}

// Generate recommendations
const recommendations = [];
if (criticalCount > 0) {
  recommendations.push('CRITICAL: Address all critical threats immediately - within 1 week');
}
if (highCount > 0) {
  recommendations.push('HIGH: Implement mitigations for high-risk threats - within 1 month');
}
if (mediumCount > 0) {
  recommendations.push('MEDIUM: Review and address medium-risk threats - within 3 months');
}

recommendations.push('MEDIUM: Implement threat modeling in development process - ongoing');
recommendations.push('MEDIUM: Conduct security training for development team - within 1 month');

return {
  riskAssessment: {
    totalThreats: threats.length,
    threatsPerComponent: (threats.length / componentCount).toFixed(1),
    criticalCount,
    highCount,
    mediumCount,
    lowCount,
    overallRisk,
    recommendations
  },
  threats
};
        "
      },
      "name": "Calculate Risk",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [
        680,
        300
      ]
    },
    {
      "parameters": {
        "documentName": "={{ $json.systemName + '_threat_model_' + $now.format('YYYYMMDD') }}",
        "columns": [
          "id",
          "category",
          "component",
          "title",
          "impact",
          "likelihood",
          "riskLevel"
        ],
        "options": {}
      },
      "name": "Generate Report",
      "type": "n8n-nodes-base.googleSheets",
      "typeVersion": 1,
      "position": [
        900,
        300
      ]
    }
  ],
  "connections": {
    "Set System Context": {
      "main": [
        [
          {
            "node": "STRIDE Analysis",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "STRIDE Analysis": {
      "main": [
        [
          {
            "node": "Calculate Risk",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Calculate Risk": {
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

## Workflow Components

### 1. System Context Setup

**Purpose:** Initialize system information and component data

```json
{
  "name": "Set System Context",
  "type": "n8n-nodes-base.set",
  "parameters": {
    "values": {
      "string": [
        {
          "name": "systemName",
          "value": "={{ $json.systemName }}"
        },
        {
          "name": "components",
          "value": "={{ $json.components }}"
        }
      ]
    }
  }
}
```

**Input Requirements:**
- `systemName`: Name of the system being analyzed
- `components`: Array of system components with properties

### 2. STRIDE Analysis Engine

**Purpose:** Execute STRIDE threat identification logic

**Key Features:**
- Analyzes each component against all 6 STRIDE categories
- Applies conditional logic based on component properties
- Generates detailed threat descriptions
- Calculates initial risk levels

**Component Properties Analyzed:**
- `publicFacing`: External exposure
- `handlesData`: Data processing capability
- `hasTransactions`: Transaction processing
- `dataSensitivity`: Data sensitivity level
- `criticality`: Business criticality
- `hasPrivileges`: Privilege management
- `managesAccess`: Access control functionality

### 3. Risk Assessment Calculator

**Purpose:** Calculate overall risk metrics and generate recommendations

**Calculations Performed:**
- Threat counts by risk level (Critical, High, Medium, Low)
- Threats per component ratio
- Overall system risk assessment
- Prioritized recommendations

**Risk Level Logic:**
```javascript
if (criticalCount > 0) {
  overallRisk = 'critical';
} else if (highCount > 2) {
  overallRisk = 'high';
} else if (highCount > 0 || mediumCount > 3) {
  overallRisk = 'medium';
} else {
  overallRisk = 'low';
}
```

### 4. Report Generation

**Purpose:** Export results to various formats and systems

**Supported Outputs:**
- Google Sheets (as shown in example)
- Microsoft Excel
- CSV files
- JSON exports
- PDF reports
- Email notifications
- Slack/Teams messages

---

## Automation Triggers

### CI/CD Pipeline Integration

**GitHub Actions Example:**
```yaml
name: Security Threat Modeling
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  threat-modeling:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run STRIDE Analysis
      run: |
        npm install -g n8n
        n8n execute --file stride-workflow.json --input system-data.json
```

### Scheduled Analysis

**Cron-based execution:**
```bash
# Run threat modeling weekly
0 2 * * 1 n8n execute --file stride-weekly-analysis.json

# Run after deployments
# Trigger via webhook from CI/CD system
```

### Event-Driven Triggers

**Webhook Integration:**
```json
{
  "trigger": "webhook",
  "path": "/api/threat-modeling",
  "method": "POST",
  "authentication": "bearer",
  "payload": {
    "systemName": "string",
    "components": "array",
    "triggeredBy": "deployment|manual|scheduled"
  }
}
```

---

## CI/CD Integration

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Threat Modeling') {
            steps {
                script {
                    // Run STRIDE analysis
                    sh '''
                        curl -X POST http://n8n-server:5678/webhook/stride-analysis \\
                        -H "Content-Type: application/json" \\
                        -d @system-components.json
                    '''

                    // Wait for results
                    sh 'sleep 30'

                    // Check results
                    sh '''
                        curl http://n8n-server:5678/results/latest \\
                        | jq '.riskAssessment.overallRisk'
                    '''
                }
            }
        }
        stage('Security Gate') {
            steps {
                script {
                    def riskLevel = sh(
                        script: 'curl -s http://n8n-server:5678/results/latest | jq -r .riskAssessment.overallRisk',
                        returnStdout: true
                    ).trim()

                    if (riskLevel == 'critical') {
                        error('Critical security threats detected. Pipeline stopped.')
                    }
                }
            }
        }
    }
}
```

### GitLab CI/CD

```yaml
stages:
  - security

threat_modeling:
  stage: security
  script:
    - |
      # Extract system components from codebase
      npm run extract-components > components.json

      # Run STRIDE analysis
      curl -X POST $N8N_WEBHOOK_URL \\
        -H "Authorization: Bearer $N8N_TOKEN" \\
        -H "Content-Type: application/json" \\
        -d @components.json

  artifacts:
    reports:
      junit: threat-model-results.xml
    expire_in: 1 week

  rules:
    - if: $CI_MERGE_REQUEST_TARGET_BRANCH_NAME == "main"
```

---

## Reporting Automation

### Multi-Format Report Generation

```javascript
// Advanced reporting node configuration
{
  "name": "Advanced Reporting",
  "type": "n8n-nodes-base.function",
  "parameters": {
    "functionCode": "
// Generate multiple report formats
const threatModel = $node['Calculate Risk'].json;
const systemName = $node['Set System Context'].json.systemName;

// Generate executive summary
const executiveSummary = {
  system: systemName,
  analysisDate: new Date().toISOString(),
  totalThreats: threatModel.riskAssessment.totalThreats,
  overallRisk: threatModel.riskAssessment.overallRisk,
  criticalIssues: threatModel.riskAssessment.criticalCount,
  keyRecommendations: threatModel.riskAssessment.recommendations.slice(0, 3)
};

// Generate detailed CSV
let csvContent = 'Category,Component,Title,Risk Level,Mitigations\\n';
for (const threat of threatModel.threats) {
  csvContent += `${threat.category},${threat.component},${threat.title},${threat.riskLevel},${threat.mitigations.join('; ')}\\n`;
}

// Generate HTML report
const htmlReport = generateHTMLReport(threatModel, executiveSummary);

return {
  executiveSummary: JSON.stringify(executiveSummary, null, 2),
  detailedCSV: csvContent,
  htmlReport: htmlReport,
  pdfReady: true
};

function generateHTMLReport(model, summary) {
  return `
    <html>
      <head><title>STRIDE Threat Model - ${summary.system}</title></head>
      <body>
        <h1>STRIDE Threat Analysis Report</h1>
        <h2>System: ${summary.system}</h2>
        <p><strong>Analysis Date:</strong> ${summary.analysisDate}</p>
        <p><strong>Overall Risk:</strong> ${summary.overallRisk.toUpperCase()}</p>
        <p><strong>Total Threats:</strong> ${summary.totalThreats}</p>

        <h3>Risk Summary</h3>
        <ul>
          <li>Critical: ${model.riskAssessment.criticalCount}</li>
          <li>High: ${model.riskAssessment.highCount}</li>
          <li>Medium: ${model.riskAssessment.mediumCount}</li>
          <li>Low: ${model.riskAssessment.lowCount}</li>
        </ul>

        <h3>Key Recommendations</h3>
        <ul>
          ${summary.keyRecommendations.map(rec => `<li>${rec}</li>`).join('')}
        </ul>

        <h3>Detailed Findings</h3>
        <table border="1">
          <tr><th>Category</th><th>Component</th><th>Title</th><th>Risk</th></tr>
          ${model.threats.map(t => `<tr><td>${t.category}</td><td>${t.component}</td><td>${t.title}</td><td>${t.riskLevel}</td></tr>`).join('')}
        </table>
      </body>
    </html>
  `;
}
        "
  }
}
```

### Alert Integration

**Slack Notifications:**
```javascript
// Slack alert configuration
{
  "name": "Slack Alert",
  "type": "n8n-nodes-base.slack",
  "parameters": {
    "text": "={{ $node['Calculate Risk'].json.riskAssessment.overallRisk === 'critical' ? ':red_circle: CRITICAL: Security threats detected in ' + $node['Set System Context'].json.systemName : $node['Calculate Risk'].json.riskAssessment.overallRisk === 'high' ? ':orange_circle: HIGH: Security threats detected in ' + $node['Set System Context'].json.systemName : ':green_circle: Threat modeling completed for ' + $node['Set System Context'].json.systemName }}",
    "channel": "#security-alerts",
    "attachments": [
      {
        "title": "STRIDE Analysis Results",
        "fields": [
          {
            "title": "Total Threats",
            "value": "={{ $node['Calculate Risk'].json.riskAssessment.totalThreats }}",
            "short": true
          },
          {
            "title": "Critical Threats",
            "value": "={{ $node['Calculate Risk'].json.riskAssessment.criticalCount }}",
            "short": true
          },
          {
            "title": "Overall Risk",
            "value": "={{ $node['Calculate Risk'].json.riskAssessment.overallRisk.toUpperCase() }}",
            "short": true
          }
        ]
      }
    ]
  }
}
```

**Email Notifications:**
```javascript
// Email alert configuration
{
  "name": "Email Notification",
  "type": "n8n-nodes-base.emailSend",
  "parameters": {
    "to": "security-team@company.com",
    "subject": "STRIDE Threat Model Results - {{ $node['Set System Context'].json.systemName }}",
    "text": `
STRIDE Threat Modeling Analysis Complete

System: {{ $node['Set System Context'].json.systemName }}
Analysis Date: {{ $now.format('YYYY-MM-DD HH:mm') }}

Risk Assessment:
- Overall Risk: {{ $node['Calculate Risk'].json.riskAssessment.overallRisk.toUpperCase() }}
- Total Threats: {{ $node['Calculate Risk'].json.riskAssessment.totalThreats }}
- Critical Threats: {{ $node['Calculate Risk'].json.riskAssessment.criticalCount }}
- High Threats: {{ $node['Calculate Risk'].json.riskAssessment.highCount }}

Key Recommendations:
{{ $node['Calculate Risk'].json.riskAssessment.recommendations.join('\\n') }}

Full report attached.
    `,
    "attachments": [
      {
        "fileName": "threat-model-results.json",
        "mimeType": "application/json",
        "data": "={{ JSON.stringify($node['Calculate Risk'].json, null, 2) }}"
      }
    ]
  }
}
```

---

## Workflow Configuration

### Environment Variables

```bash
# n8n configuration
N8N_ENCRYPTION_KEY=your-encryption-key
N8N_WEBHOOK_URL=https://your-n8n-instance.com
N8N_API_KEY=your-api-key

# Integration endpoints
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
JIRA_API_URL=https://your-jira-instance.com
GITHUB_TOKEN=your-github-token

# Storage configuration
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
S3_BUCKET=threat-models

# Database configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=threat_modeling
DB_USER=threat_user
DB_PASSWORD=secure-password
```

### Custom Nodes

**STRIDE Analysis Node:**
```javascript
// Custom n8n node for advanced STRIDE analysis
class STRIDEAnalysisNode {
  async execute() {
    const items = this.getInputData();

    for (const item of items) {
      const systemData = item.json;

      // Advanced STRIDE analysis with machine learning
      const analysis = await this.performAdvancedAnalysis(systemData);

      // Generate detailed mitigation strategies
      const mitigations = await this.generateDetailedMitigations(analysis.threats);

      // Calculate risk with historical data
      const riskAssessment = await this.calculateRiskWithHistory(analysis, systemData.systemName);

      item.json = {
        ...systemData,
        analysis,
        mitigations,
        riskAssessment,
        generatedAt: new Date().toISOString()
      };
    }

    return [items];
  }
}
```

### Error Handling

**Robust Error Handling:**
```javascript
// Error handling wrapper for n8n workflows
class STRIDEErrorHandler {
  static async executeWithErrorHandling(workflowFunction, context) {
    try {
      const result = await workflowFunction(context);

      // Log successful execution
      await this.logSuccess(context, result);

      return result;
    } catch (error) {
      // Log error details
      await this.logError(context, error);

      // Send alert if critical
      if (this.isCriticalError(error)) {
        await this.sendCriticalAlert(context, error);
      }

      // Return error response
      return {
        success: false,
        error: error.message,
        context,
        timestamp: new Date().toISOString()
      };
    }
  }

  static isCriticalError(error) {
    return error.code === 'STRIDE_ANALYSIS_FAILED' ||
           error.code === 'RISK_CALCULATION_ERROR';
  }
}
```

---

## Navigation

| Previous | Current | Next |
|----------|---------|------|
| [[./code-examples|Code Examples]] | Automation Integration | [[./best-practices|Best Practices]] |

## See Also

### Related Topics
- [[../template|STRIDE Template]] - Manual threat modeling
- [[./code-examples|Code Examples]] - Implementation details
- [[../../../workflows|Workflow Automation]] - General automation

### Integration Resources
- [[../../../api|API Integration]] - REST API examples
- [[../../../workflows/examples/devsecops|DevSecOps Examples]] - CI/CD integration
- [[../../../workflows/examples/siem-integration|SIEM Integration]] - Security monitoring

---

**Tags:** #stride-automation #n8n-workflows #ci-cd-integration #threat-modeling-automation #reporting

**Last Updated:** October 2025
**Version:** 1.0
**Reading Time:** 20 minutes
**Difficulty:** Advanced