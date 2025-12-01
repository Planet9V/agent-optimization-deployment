# Advanced Threat Modeling Methodologies

**Specialized Frameworks and Techniques for Comprehensive Security Analysis**

**Version:** 1.0 - October 2025
**Methodologies:** Attack Trees, CVSS, DREAD, LINDDUN, hTMM, and more
**Purpose:** Advanced threat modeling techniques for complex systems
**Scope:** Specialized methodologies with detailed implementation guidance

## 📋 Executive Summary

This document covers advanced threat modeling methodologies that complement the core frameworks (STRIDE, PASTA, OCTAVE, Trike, VAST). These specialized techniques provide deeper analysis capabilities for specific scenarios, quantitative risk assessment, and advanced attack modeling.

**Key Methodologies:**
- Attack Trees: Hierarchical attack modeling
- CVSS: Quantitative vulnerability scoring
- DREAD: Risk assessment framework
- LINDDUN: Privacy threat modeling
- hTMM: Hybrid threat modeling methodology
- And additional specialized frameworks

## 🌳 Attack Trees Methodology

**Hierarchical representation of attack paths and countermeasures**

### Core Concepts

Attack trees model security threats as a tree structure where:
- **Root Node:** Represents the attacker's ultimate goal
- **Intermediate Nodes:** Represent sub-goals or attack steps
- **Leaf Nodes:** Represent atomic attack actions

#### Attack Tree Structure
```
Root Goal (System Compromise)
├── Branch 1: Network Attack
│   ├── Sub-branch: Exploit Vulnerability
│   │   ├── Leaf: Find vulnerable service
│   │   └── Leaf: Exploit buffer overflow
│   └── Sub-branch: Social Engineering
│       ├── Leaf: Phishing attack
│       └── Leaf: Physical access
└── Branch 2: Insider Attack
    ├── Sub-branch: Authorized Access Abuse
    │   ├── Leaf: Privilege escalation
    │   └── Leaf: Data exfiltration
    └── Sub-branch: Supply Chain Compromise
        ├── Leaf: Third-party compromise
        └── Leaf: Malicious update
```

### Attack Tree Implementation

```javascript
class AttackTree {
  constructor() {
    this.nodes = new Map();
    this.edges = new Map();
    this.rootNode = null;
  }

  // Create attack tree for system
  async createAttackTree(goal, systemComponents, attackerProfile) {
    const tree = {
      goal: goal,
      root: null,
      nodes: [],
      edges: [],
      attackerProfile: attackerProfile,
      created: new Date()
    };

    // Create root node
    tree.root = this.createNode('OR', goal.description, goal.id);

    // Decompose goal into sub-goals
    const subGoals = await this.decomposeGoal(goal, systemComponents, attackerProfile);
    tree.nodes.push(tree.root);
    tree.edges.push(...this.connectNodes(tree.root, subGoals));

    // Recursively build tree
    for (const subGoal of subGoals) {
      const subTree = await this.buildSubTree(subGoal, systemComponents, attackerProfile);
      tree.nodes.push(...subTree.nodes);
      tree.edges.push(...subTree.edges);
    }

    return tree;
  }

  // Decompose goal into sub-goals
  async decomposeGoal(goal, systemComponents, attackerProfile) {
    const subGoals = [];

    switch (goal.type) {
      case 'data_breach':
        subGoals.push(
          this.createNode('OR', 'Gain Network Access', 'network_access'),
          this.createNode('OR', 'Exploit Application Vulnerability', 'app_exploit'),
          this.createNode('OR', 'Insider Attack', 'insider_attack')
        );
        break;

      case 'denial_of_service':
        subGoals.push(
          this.createNode('OR', 'Network Flooding', 'network_flood'),
          this.createNode('OR', 'Resource Exhaustion', 'resource_exhaust'),
          this.createNode('OR', 'Service Disruption', 'service_disrupt')
        );
        break;

      case 'system_compromise':
        subGoals.push(
          this.createNode('AND', 'Initial Access + Privilege Escalation', 'full_compromise'),
          this.createNode('OR', 'Direct System Access', 'direct_access')
        );
        break;
    }

    return subGoals;
  }

  // Build subtree for goal
  async buildSubTree(goal, systemComponents, attackerProfile) {
    const subTree = {
      nodes: [],
      edges: []
    };

    // Find applicable attack vectors
    const attackVectors = this.findAttackVectors(goal, systemComponents, attackerProfile);

    for (const vector of attackVectors) {
      const leafNode = this.createNode('LEAF', vector.description, vector.id);
      subTree.nodes.push(leafNode);
      subTree.edges.push({
        from: goal.id,
        to: leafNode.id,
        type: 'attack_vector'
      });
    }

    return subTree;
  }

  // Find applicable attack vectors
  findAttackVectors(goal, systemComponents, attackerProfile) {
    const vectors = [];

    // Network-based attacks
    if (goal.description.includes('network') || goal.description.includes('access')) {
      if (attackerProfile.capabilities.includes('network_access')) {
        vectors.push({
          id: 'network_scan',
          description: 'Port scanning and service enumeration',
          prerequisites: ['Internet access'],
          difficulty: 'Low',
          detection: 'Medium'
        });

        vectors.push({
          id: 'exploit_vuln',
          description: 'Exploit known vulnerabilities',
          prerequisites: ['Vulnerable service', 'Exploit code'],
          difficulty: 'Medium',
          detection: 'High'
        });
      }
    }

    // Application attacks
    if (goal.description.includes('application') || goal.description.includes('web')) {
      vectors.push({
        id: 'sql_injection',
        description: 'SQL injection through web forms',
        prerequisites: ['Web application', 'Input validation weakness'],
        difficulty: 'Medium',
        detection: 'High'
      });

      vectors.push({
        id: 'xss_attack',
        description: 'Cross-site scripting attack',
        prerequisites: ['Web application', 'Output encoding failure'],
        difficulty: 'Medium',
        detection: 'Medium'
      });
    }

    // Physical attacks
    if (attackerProfile.capabilities.includes('physical_access')) {
      vectors.push({
        id: 'physical_access',
        description: 'Direct physical access to systems',
        prerequisites: ['Building access', 'Unattended equipment'],
        difficulty: 'Low',
        detection: 'High'
      });
    }

    return vectors;
  }

  // Calculate attack tree metrics
  calculateMetrics(tree) {
    const metrics = {
      totalNodes: tree.nodes.length,
      leafNodes: tree.nodes.filter(n => n.type === 'LEAF').length,
      complexity: 0,
      minAttackCost: 0,
      maxAttackCost: 0,
      mostLikelyPath: null
    };

    // Calculate complexity (number of paths)
    metrics.complexity = this.calculateTreeComplexity(tree.root, tree);

    // Calculate attack costs
    const costs = this.calculateAttackCosts(tree);
    metrics.minAttackCost = costs.min;
    metrics.maxAttackCost = costs.max;

    // Find most likely attack path
    metrics.mostLikelyPath = this.findMostLikelyPath(tree);

    return metrics;
  }

  // Calculate tree complexity
  calculateTreeComplexity(node, tree) {
    if (node.type === 'LEAF') return 1;

    const children = tree.edges
      .filter(e => e.from === node.id)
      .map(e => tree.nodes.find(n => n.id === e.to));

    if (node.operator === 'AND') {
      return children.reduce((sum, child) => sum * this.calculateTreeComplexity(child, tree), 1);
    } else { // OR
      return children.reduce((sum, child) => sum + this.calculateTreeComplexity(child, tree), 0);
    }
  }

  // Calculate attack costs
  calculateAttackCosts(tree) {
    const leafNodes = tree.nodes.filter(n => n.type === 'LEAF');
    const costs = leafNodes.map(node => this.estimateAttackCost(node));

    return {
      min: Math.min(...costs),
      max: Math.max(...costs),
      average: costs.reduce((sum, cost) => sum + cost, 0) / costs.length
    };
  }

  // Estimate attack cost
  estimateAttackCost(node) {
    const baseCosts = {
      'network_scan': 100,
      'exploit_vuln': 500,
      'sql_injection': 300,
      'xss_attack': 200,
      'physical_access': 50
    };

    return baseCosts[node.description.split(' ')[0].toLowerCase()] || 250;
  }

  // Find most likely attack path
  findMostLikelyPath(tree) {
    // Simplified: return path with lowest cost
    const paths = this.enumeratePaths(tree.root, tree);
    return paths.sort((a, b) => a.totalCost - b.totalCost)[0];
  }

  // Enumerate all attack paths
  enumeratePaths(node, tree, currentPath = []) {
    const path = [...currentPath, node];

    if (node.type === 'LEAF') {
      return [{
        nodes: path,
        totalCost: path.reduce((sum, n) => sum + this.estimateAttackCost(n), 0),
        successProbability: this.calculatePathProbability(path)
      }];
    }

    const children = tree.edges
      .filter(e => e.from === node.id)
      .map(e => tree.nodes.find(n => n.id === e.to));

    const paths = [];

    for (const child of children) {
      const childPaths = this.enumeratePaths(child, tree, path);
      paths.push(...childPaths);
    }

    return paths;
  }

  // Calculate path success probability
  calculatePathProbability(path) {
    return path.reduce((prob, node) => {
      const nodeProb = node.type === 'LEAF' ? 0.7 : 0.8; // Simplified
      return prob * nodeProb;
    }, 1.0);
  }

  // Utility methods
  createNode(operator, description, id) {
    return {
      id: id,
      operator: operator,
      description: description,
      type: operator === 'LEAF' ? 'LEAF' : 'INTERMEDIATE',
      cost: 0,
      probability: 0
    };
  }

  connectNodes(parent, children) {
    return children.map(child => ({
      from: parent.id,
      to: child.id,
      type: 'decomposition'
    }));
  }
}

// Example attack tree implementation
const attackTree = new AttackTree();

const systemCompromiseGoal = {
  id: 'system_compromise',
  type: 'system_compromise',
  description: 'Complete system compromise with persistent access'
};

const systemComponents = [
  { name: 'WebServer', type: 'web_application', vulnerabilities: ['SQLi', 'XSS'] },
  { name: 'Database', type: 'database', sensitive: true },
  { name: 'AdminPanel', type: 'management_interface', exposed: true }
];

const attackerProfile = {
  capabilities: ['network_access', 'web_exploitation', 'social_engineering'],
  resources: 'moderate',
  motivation: 'high'
};

const tree = await attackTree.createAttackTree(systemCompromiseGoal, systemComponents, attackerProfile);
const metrics = attackTree.calculateMetrics(tree);

console.log('Attack Tree Analysis:');
console.log(`Total Nodes: ${metrics.totalNodes}`);
console.log(`Leaf Nodes: ${metrics.leafNodes}`);
console.log(`Tree Complexity: ${metrics.complexity} attack paths`);
console.log(`Attack Cost Range: $${metrics.minAttackCost} - $${metrics.maxAttackCost}`);
```

## 📊 CVSS (Common Vulnerability Scoring System)

**Quantitative vulnerability assessment framework**

### CVSS v3.1 Base Score Metrics

#### Base Score Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H

#### Exploitability Metrics
- **Attack Vector (AV):**
  - Network (N): 0.85
  - Adjacent Network (A): 0.62
  - Local (L): 0.55
  - Physical (P): 0.2

- **Attack Complexity (AC):**
  - Low (L): 0.77
  - High (H): 0.44

- **Privileges Required (PR):**
  - None (N): 0.85
  - Low (L): 0.62
  - High (H): 0.27

- **User Interaction (UI):**
  - None (N): 0.85
  - Required (R): 0.62

#### Impact Metrics
- **Confidentiality Impact (C):**
  - High (H): 0.56
  - Low (L): 0.22
  - None (N): 0

- **Integrity Impact (I):**
  - High (H): 0.56
  - Low (L): 0.22
  - None (N): 0

- **Availability Impact (A):**
  - High (H): 0.56
  - Low (L): 0.22
  - None (N): 0

#### Scope (S)
- **Changed (C):** 1.08 (affects resources beyond the vulnerable component)
- **Unchanged (U):** 1.0 (impact limited to the vulnerable component)

### CVSS Implementation

```javascript
class CVSSCalculator {
  constructor() {
    this.weights = {
      AV: { N: 0.85, A: 0.62, L: 0.55, P: 0.2 },
      AC: { L: 0.77, H: 0.44 },
      PR: { N: 0.85, L: 0.62, H: 0.27 },
      UI: { N: 0.85, R: 0.62 },
      S: { U: 1.0, C: 1.08 },
      C: { N: 0, L: 0.22, H: 0.56 },
      I: { N: 0, L: 0.22, H: 0.56 },
      A: { N: 0, L: 0.22, H: 0.56 }
    };
  }

  // Calculate CVSS v3.1 Base Score
  calculateBaseScore(vector) {
    const metrics = this.parseVector(vector);

    // Calculate Exploitability Subscore
    const exploitability = 8.22 * metrics.AV * metrics.AC * metrics.PR * metrics.UI;

    // Calculate Impact Subscore
    let impact = 1 - ((1 - metrics.C) * (1 - metrics.I) * (1 - metrics.A));

    if (metrics.S === 0) { // Scope Unchanged
      impact = 6.42 * impact;
    } else { // Scope Changed
      impact = 7.52 * (impact - 0.029) - 3.25 * Math.pow(impact - 0.02, 15);
    }

    // Calculate Base Score
    let baseScore;
    if (impact <= 0) {
      baseScore = 0;
    } else {
      if (metrics.S === 0) { // Scope Unchanged
        baseScore = Math.min(10, Math.ceil((exploitability + impact) * 10) / 10);
      } else { // Scope Changed
        baseScore = Math.min(10, Math.ceil((exploitability + impact) * 10) / 10);
      }
    }

    return {
      baseScore: Math.round(baseScore * 10) / 10,
      exploitability: Math.round(exploitability * 10) / 10,
      impact: Math.round(impact * 10) / 10,
      severity: this.getSeverity(baseScore)
    };
  }

  // Parse CVSS vector string
  parseVector(vector) {
    const parts = vector.replace('CVSS:3.1/', '').split('/');
    const metrics = {};

    parts.forEach(part => {
      const [key, value] = part.split(':');
      metrics[key] = this.weights[key][value];
    });

    return metrics;
  }

  // Get severity rating
  getSeverity(score) {
    if (score === 0) return 'None';
    if (score <= 3.9) return 'Low';
    if (score <= 6.9) return 'Medium';
    if (score <= 8.9) return 'High';
    return 'Critical';
  }

  // Calculate Temporal Score
  calculateTemporalScore(baseScore, temporalMetrics) {
    const E = temporalMetrics.exploitCodeMaturity || 1.0; // Not Defined
    const RL = temporalMetrics.remediationLevel || 1.0; // Not Defined
    const RC = temporalMetrics.reportConfidence || 1.0; // Not Defined

    const temporalScore = baseScore * E * RL * RC;
    return Math.round(temporalScore * 10) / 10;
  }

  // Calculate Environmental Score
  calculateEnvironmentalScore(baseScore, environmentalMetrics) {
    // Simplified environmental scoring
    const modifiedImpact = this.calculateModifiedImpact(environmentalMetrics);
    const environmentalScore = this.calculateBaseScoreFromImpact(baseScore, modifiedImpact);

    return Math.round(environmentalScore * 10) / 10;
  }

  // Calculate Modified Impact
  calculateModifiedImpact(envMetrics) {
    const mc = envMetrics.modifiedConfidentiality || 0;
    const mi = envMetrics.modifiedIntegrity || 0;
    const ma = envMetrics.modifiedAvailability || 0;
    const cr = envMetrics.confidentialityRequirement || 1.0;
    const ir = envMetrics.integrityRequirement || 1.0;
    const ar = envMetrics.availabilityRequirement || 1.0;

    let modifiedImpact = 1 - ((1 - mc * cr) * (1 - mi * ir) * (1 - ma * ar));

    if (envMetrics.modifiedScope === 'Changed') {
      modifiedImpact = 7.52 * (modifiedImpact - 0.029) - 3.25 * Math.pow(modifiedImpact - 0.02, 15);
    } else {
      modifiedImpact = 6.42 * modifiedImpact;
    }

    return modifiedImpact;
  }

  // Generate CVSS vector from metrics
  generateVector(metrics) {
    return `CVSS:3.1/AV:${metrics.AV}/AC:${metrics.AC}/PR:${metrics.PR}/UI:${metrics.UI}/S:${metrics.S}/C:${metrics.C}/I:${metrics.I}/A:${metrics.A}`;
  }

  // Analyze vulnerability trends
  analyzeTrends(vulnerabilities) {
    const trends = {
      severityDistribution: {},
      mostCommonVectors: {},
      averageScore: 0,
      criticalCount: 0
    };

    let totalScore = 0;

    vulnerabilities.forEach(vuln => {
      const score = this.calculateBaseScore(vuln.vector);

      // Severity distribution
      trends.severityDistribution[score.severity] =
        (trends.severityDistribution[score.severity] || 0) + 1;

      // Attack vectors
      const vector = vuln.vector.split('/')[0].split(':')[1];
      trends.mostCommonVectors[vector] =
        (trends.mostCommonVectors[vector] || 0) + 1;

      totalScore += score.baseScore;

      if (score.severity === 'Critical') {
        trends.criticalCount++;
      }
    });

    trends.averageScore = totalScore / vulnerabilities.length;

    return trends;
  }
}

// Example CVSS calculations
const cvss = new CVSSCalculator();

// Example vulnerability vectors
const vulnerabilities = [
  {
    cve: 'CVE-2023-12345',
    vector: 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
    description: 'Remote code execution vulnerability'
  },
  {
    cve: 'CVE-2023-12346',
    vector: 'CVSS:3.1/AV:A/AC:H/PR:L/UI:R/S:U/C:L/I:L/A:N',
    description: 'Local privilege escalation'
  },
  {
    cve: 'CVE-2023-12347',
    vector: 'CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N',
    description: 'Information disclosure'
  }
];

vulnerabilities.forEach(vuln => {
  const score = cvss.calculateBaseScore(vuln.vector);
  console.log(`${vuln.cve}: ${score.baseScore} (${score.severity})`);
  console.log(`  Exploitability: ${score.exploitability}, Impact: ${score.impact}`);
});

const trends = cvss.analyzeTrends(vulnerabilities);
console.log('\nVulnerability Trends:');
console.log(`Average Score: ${trends.averageScore.toFixed(1)}`);
console.log(`Critical Vulnerabilities: ${trends.criticalCount}`);
console.log('Severity Distribution:', trends.severityDistribution);
```

## ⚠️ DREAD Risk Assessment Framework

**Microsoft-developed risk assessment methodology**

### DREAD Components

- **Damage Potential (D):** How much damage could be caused?
- **Reproducibility (R):** How easy is it to reproduce the attack?
- **Exploitability (E):** How easy is it to launch the attack?
- **Affected Users (A):** How many users could be affected?
- **Discoverability (D):** How easy is it to discover the vulnerability?

### DREAD Scoring

Each component is scored from 0-10:
- 0: No risk
- 5: Medium risk
- 10: Maximum risk

**Risk Rating = (D + R + E + A + D) / 5**

### DREAD Implementation

```javascript
class DREADAssessor {
  constructor() {
    this.weights = {
      damage: 1.0,
      reproducibility: 1.0,
      exploitability: 1.0,
      affectedUsers: 1.0,
      discoverability: 1.0
    };
  }

  // Assess risk using DREAD
  assessRisk(threat, systemContext) {
    const assessment = {
      threatId: threat.id,
      threatName: threat.name,
      scores: {},
      totalScore: 0,
      riskLevel: 'Low',
      recommendations: []
    };

    // Assess each DREAD component
    assessment.scores.damage = this.assessDamage(threat, systemContext);
    assessment.scores.reproducibility = this.assessReproducibility(threat);
    assessment.scores.exploitability = this.assessExploitability(threat);
    assessment.scores.affectedUsers = this.assessAffectedUsers(threat, systemContext);
    assessment.scores.discoverability = this.assessDiscoverability(threat);

    // Calculate total risk score
    assessment.totalScore = this.calculateTotalScore(assessment.scores);
    assessment.riskLevel = this.getRiskLevel(assessment.totalScore);

    // Generate recommendations
    assessment.recommendations = this.generateRecommendations(assessment);

    return assessment;
  }

  // Assess damage potential
  assessDamage(threat, systemContext) {
    let score = 0;

    // Financial impact
    if (threat.impact.financial > 100000) score += 3;
    else if (threat.impact.financial > 10000) score += 2;
    else if (threat.impact.financial > 1000) score += 1;

    // Operational impact
    if (threat.impact.operational === 'critical') score += 3;
    else if (threat.impact.operational === 'high') score += 2;
    else if (threat.impact.operational === 'medium') score += 1;

    // Safety impact
    if (threat.impact.safety) score += 3;

    // Reputation impact
    if (threat.impact.reputation === 'severe') score += 2;
    else if (threat.impact.reputation === 'moderate') score += 1;

    return Math.min(score, 10);
  }

  // Assess reproducibility
  assessReproducibility(threat) {
    let score = 10; // Default to easy

    // Reduce score based on complexity
    if (threat.complexity === 'very_high') score -= 8;
    else if (threat.complexity === 'high') score -= 6;
    else if (threat.complexity === 'medium') score -= 4;
    else if (threat.complexity === 'low') score -= 2;

    // Reduce score for unique conditions
    if (threat.prerequisites?.length > 3) score -= 2;
    if (threat.timing === 'narrow_window') score -= 2;

    return Math.max(score, 0);
  }

  // Assess exploitability
  assessExploitability(threat) {
    let score = 10; // Default to easy

    // Technical skills required
    if (threat.skillRequired === 'expert') score -= 6;
    else if (threat.skillRequired === 'advanced') score -= 4;
    else if (threat.skillRequired === 'intermediate') score -= 2;

    // Resources required
    if (threat.resourcesRequired === 'extensive') score -= 3;
    else if (threat.resourcesRequired === 'significant') score -= 2;
    else if (threat.resourcesRequired === 'moderate') score -= 1;

    // Tools availability
    if (threat.toolsRequired === 'custom') score -= 2;
    else if (threat.toolsRequired === 'specialized') score -= 1;

    return Math.max(score, 0);
  }

  // Assess affected users
  assessAffectedUsers(threat, systemContext) {
    const totalUsers = systemContext.totalUsers || 1000;
    const affectedUsers = threat.potentialVictims || totalUsers;

    const percentage = (affectedUsers / totalUsers) * 100;

    if (percentage >= 75) return 10;
    if (percentage >= 50) return 7;
    if (percentage >= 25) return 5;
    if (percentage >= 10) return 3;
    if (percentage >= 1) return 1;
    return 0;
  }

  // Assess discoverability
  assessDiscoverability(threat) {
    let score = 10; // Default to easy to discover

    // Public information
    if (!threat.publiclyKnown) score -= 3;

    // Research required
    if (threat.researchRequired === 'extensive') score -= 4;
    else if (threat.researchRequired === 'moderate') score -= 2;

    // Specialized knowledge
    if (threat.specializedKnowledge) score -= 2;

    // Obscured implementation
    if (threat.obscured) score -= 2;

    return Math.max(score, 0);
  }

  // Calculate total DREAD score
  calculateTotalScore(scores) {
    const weightedSum = Object.entries(scores).reduce((sum, [component, score]) => {
      return sum + (score * this.weights[component]);
    }, 0);

    return weightedSum / Object.keys(scores).length;
  }

  // Get risk level from score
  getRiskLevel(score) {
    if (score >= 8) return 'Critical';
    if (score >= 6) return 'High';
    if (score >= 4) return 'Medium';
    if (score >= 2) return 'Low';
    return 'Very Low';
  }

  // Generate recommendations
  generateRecommendations(assessment) {
    const recommendations = [];

    if (assessment.scores.damage >= 7) {
      recommendations.push('Implement immediate mitigation for high damage potential');
    }

    if (assessment.scores.exploitability >= 7) {
      recommendations.push('Address ease of exploitation through defense in depth');
    }

    if (assessment.scores.affectedUsers >= 7) {
      recommendations.push('Consider system-wide impact and business continuity planning');
    }

    if (assessment.scores.discoverability >= 7) {
      recommendations.push('Reduce attack surface visibility through obscurity removal');
    }

    if (assessment.totalScore >= 6) {
      recommendations.push('Prioritize this threat in the next sprint/iteration');
    }

    return recommendations;
  }

  // Compare multiple threats
  compareThreats(threats, systemContext) {
    const assessments = threats.map(threat =>
      this.assessRisk(threat, systemContext)
    );

    return assessments.sort((a, b) => b.totalScore - a.totalScore);
  }
}

// Example DREAD assessment
const dread = new DREADAssessor();

const threats = [
  {
    id: 'T001',
    name: 'SQL Injection',
    impact: {
      financial: 50000,
      operational: 'high',
      safety: false,
      reputation: 'moderate'
    },
    complexity: 'low',
    skillRequired: 'intermediate',
    resourcesRequired: 'minimal',
    toolsRequired: 'common',
    publiclyKnown: true,
    researchRequired: 'minimal',
    potentialVictims: 1000
  },
  {
    id: 'T002',
    name: 'Zero-day RCE',
    impact: {
      financial: 500000,
      operational: 'critical',
      safety: true,
      reputation: 'severe'
    },
    complexity: 'high',
    skillRequired: 'expert',
    resourcesRequired: 'extensive',
    toolsRequired: 'custom',
    publiclyKnown: false,
    researchRequired: 'extensive',
    potentialVictims: 10000
  }
];

const systemContext = {
  totalUsers: 10000,
  criticalSystems: true,
  regulatoryRequirements: ['PCI-DSS', 'HIPAA']
};

const rankedThreats = dread.compareThreats(threats, systemContext);

console.log('DREAD Threat Ranking:');
rankedThreats.forEach((assessment, index) => {
  console.log(`${index + 1}. ${assessment.threatName}`);
  console.log(`   Score: ${assessment.totalScore.toFixed(1)} (${assessment.riskLevel})`);
  console.log(`   D: ${assessment.scores.damage}, R: ${assessment.scores.reproducibility}, E: ${assessment.scores.exploitability}, A: ${assessment.scores.affectedUsers}, D: ${assessment.scores.discoverability}`);
  console.log(`   Recommendations: ${assessment.recommendations.join('; ')}`);
  console.log('');
});
```

## 🔒 LINDDUN Privacy Threat Modeling

**Privacy-focused threat modeling methodology**

### LINDDUN Privacy Threats

- **Linkability (L):** Linking user actions across contexts
- **Identifiability (I):** Identifying individuals from data
- **Non-repudiation (N):** Preventing denial of actions
- **Detectability (D):** Detecting presence of individuals
- **Disclosure of information (D):** Unwanted information flow
- **Unawareness (U):** Lack of user awareness
- **Non-compliance (N):** Regulatory non-compliance

### LINDDUN Process

1. **Data Mapping:** Identify personal data flows
2. **Threat Identification:** Apply LINDDUN categories
3. **Risk Assessment:** Evaluate privacy risks
4. **Mitigation Planning:** Develop privacy controls

### LINDDUN Implementation

```javascript
class LINDDUNAnalyzer {
  constructor() {
    this.privacyThreats = {
      'Linkability': {
        description: 'Ability to link user actions across different contexts',
        examples: ['Cross-site tracking', 'Device fingerprinting', 'Behavioral profiling'],
        mitigations: ['Data minimization', 'Anonymization', 'Context separation']
      },
      'Identifiability': {
        description: 'Ability to identify individuals from data',
        examples: ['Unique identifiers', 'Biometric data', 'Personal information correlation'],
        mitigations: ['Pseudonymization', 'Aggregation', 'Data deletion']
      },
      'Non-repudiation': {
        description: 'Preventing users from denying their actions',
        examples: ['Digital signatures', 'Audit logs', 'Blockchain records'],
        mitigations: ['User consent', 'Right to be forgotten', 'Data portability']
      },
      'Detectability': {
        description: 'Detecting presence or absence of individuals',
        examples: ['Network traffic analysis', 'Metadata leakage', 'Side-channel attacks'],
        mitigations: ['Traffic obfuscation', 'Metadata stripping', 'Privacy-preserving protocols']
      },
      'Disclosure': {
        description: 'Unwanted information flow to unauthorized parties',
        examples: ['Data breaches', 'Insecure APIs', 'Third-party sharing'],
        mitigations: ['Encryption', 'Access controls', 'Data flow controls']
      },
      'Unawareness': {
        description: 'Lack of user awareness about data practices',
        examples: ['Hidden tracking', 'Complex privacy policies', 'Dark patterns'],
        mitigations: ['Transparent policies', 'Privacy dashboards', 'User education']
      },
      'Non-compliance': {
        description: 'Failure to comply with privacy regulations',
        examples: ['GDPR violations', 'CCPA breaches', 'Data localization issues'],
        mitigations: ['Compliance audits', 'Privacy by design', 'Regulatory monitoring']
      }
    };
  }

  // Analyze system for privacy threats
  async analyzePrivacyThreats(systemModel, dataFlows, regulations) {
    const analysis = {
      systemName: systemModel.name,
      threats: [],
      dataFlows: [],
      compliance: {},
      recommendations: [],
      created: new Date()
    };

    // Analyze data flows for privacy threats
    for (const flow of dataFlows) {
      const flowThreats = this.analyzeDataFlow(flow, systemModel);
      analysis.dataFlows.push({
        flowId: flow.id,
        source: flow.source,
        target: flow.target,
        dataType: flow.dataType,
        threats: flowThreats
      });
      analysis.threats.push(...flowThreats);
    }

    // Assess regulatory compliance
    analysis.compliance = this.assessCompliance(analysis.threats, regulations);

    // Generate recommendations
    analysis.recommendations = this.generatePrivacyRecommendations(analysis);

    return analysis;
  }

  // Analyze individual data flow
  analyzeDataFlow(flow, systemModel) {
    const threats = [];

    // Check for personal data
    if (this.isPersonalData(flow.dataType)) {
      // Linkability threats
      if (flow.crossesContexts) {
        threats.push(this.createThreat('Linkability', flow,
          'Data flows across multiple contexts enabling user tracking'));
      }

      // Identifiability threats
      if (flow.containsUniqueIdentifiers) {
        threats.push(this.createThreat('Identifiability', flow,
          'Unique identifiers allow user identification'));
      }

      // Disclosure threats
      if (!flow.encrypted) {
        threats.push(this.createThreat('Disclosure', flow,
          'Unencrypted personal data vulnerable to interception'));
      }

      // Detectability threats
      if (flow.metadataLeakage) {
        threats.push(this.createThreat('Detectability', flow,
          'Metadata reveals user presence and behavior patterns'));
      }
    }

    // Non-repudiation threats
    if (flow.auditRequired && !flow.auditEnabled) {
      threats.push(this.createThreat('Non-repudiation', flow,
        'Lack of audit trail prevents accountability'));
    }

    // Unawareness threats
    if (flow.consentNotObtained) {
      threats.push(this.createThreat('Unawareness', flow,
        'Data processing without user consent'));
    }

    return threats;
  }

  // Create privacy threat
  createThreat(category, flow, description) {
    return {
      id: this.generateThreatId(),
      category: category,
      flowId: flow.id,
      description: description,
      severity: this.assessSeverity(category, flow),
      likelihood: this.assessLikelihood(category, flow),
      impact: this.assessImpact(category, flow),
      mitigations: this.privacyThreats[category].mitigations,
      regulation: this.getRelevantRegulation(category)
    };
  }

  // Assess threat severity
  assessSeverity(category, flow) {
    let severity = 'Medium';

    // High severity for critical privacy threats
    if (category === 'Disclosure' && flow.sensitiveData) {
      severity = 'Critical';
    } else if (category === 'Non-compliance' && flow.regulatedData) {
      severity = 'High';
    } else if (category === 'Unawareness' && flow.largeScale) {
      severity = 'High';
    }

    return severity;
  }

  // Assess threat likelihood
  assessLikelihood(category, flow) {
    let likelihood = 'Medium';

    // High likelihood for common threats
    if (category === 'Disclosure' && !flow.encrypted) {
      likelihood = 'High';
    } else if (category === 'Linkability' && flow.crossesContexts) {
      likelihood = 'High';
    }

    return likelihood;
  }

  // Assess threat impact
  assessImpact(category, flow) {
    let impact = 'Medium';

    // High impact for privacy violations
    if (category === 'Non-compliance' && flow.regulatedData) {
      impact = 'Critical';
    } else if (category === 'Disclosure' && flow.sensitiveData) {
      impact = 'High';
    }

    return impact;
  }

  // Check if data type is personal
  isPersonalData(dataType) {
    const personalDataTypes = [
      'personal', 'pii', 'health', 'financial',
      'location', 'contact', 'identification'
    ];

    return personalDataTypes.some(type => dataType.toLowerCase().includes(type));
  }

  // Get relevant regulation
  getRelevantRegulation(category) {
    const regulations = {
      'Linkability': ['GDPR Article 5', 'CCPA Section 1798.100'],
      'Identifiability': ['GDPR Article 4', 'CCPA Section 1798.140'],
      'Non-repudiation': ['GDPR Article 7', 'CCPA Section 1798.120'],
      'Detectability': ['GDPR Article 25', 'CCPA Section 1798.100'],
      'Disclosure': ['GDPR Article 32', 'CCPA Section 1798.150'],
      'Unawareness': ['GDPR Article 12', 'CCPA Section 1798.110'],
      'Non-compliance': ['GDPR Article 83', 'CCPA Section 1798.155']
    };

    return regulations[category] || [];
  }

  // Assess compliance
  assessCompliance(threats, regulations) {
    const compliance = {
      gdpr: { compliant: true, violations: [] },
      ccpa: { compliant: true, violations: [] },
      overall: 'Compliant'
    };

    for (const threat of threats) {
      if (threat.category === 'Non-compliance') {
        if (regulations.includes('GDPR')) {
          compliance.gdpr.compliant = false;
          compliance.gdpr.violations.push(threat);
        }
        if (regulations.includes('CCPA')) {
          compliance.ccpa.compliant = false;
          compliance.ccpa.violations.push(threat);
        }
      }
    }

    if (!compliance.gdpr.compliant || !compliance.ccpa.compliant) {
      compliance.overall = 'Non-compliant';
    }

    return compliance;
  }

  // Generate privacy recommendations
  generatePrivacyRecommendations(analysis) {
    const recommendations = [];

    // Group threats by category
    const threatCategories = {};
    analysis.threats.forEach(threat => {
      if (!threatCategories[threat.category]) {
        threatCategories[threat.category] = [];
      }
      threatCategories[threat.category].push(threat);
    });

    // Generate category-specific recommendations
    for (const [category, threats] of Object.entries(threatCategories)) {
      const count = threats.length;
      const highSeverity = threats.filter(t => t.severity === 'Critical' || t.severity === 'High').length;

      if (highSeverity > 0) {
        recommendations.push(`Address ${highSeverity} high-severity ${category.toLowerCase()} threats immediately`);
      }

      switch (category) {
        case 'Disclosure':
          recommendations.push('Implement end-to-end encryption for all personal data flows');
          break;
        case 'Linkability':
          recommendations.push('Implement data minimization and context separation');
          break;
        case 'Unawareness':
          recommendations.push('Develop transparent privacy policies and user consent mechanisms');
          break;
        case 'Non-compliance':
          recommendations.push('Conduct privacy compliance audit and implement remediation plan');
          break;
      }
    }

    return recommendations;
  }

  // Utility methods
  generateThreatId() {
    return `LINDDUN_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Example LINDDUN analysis
const linddun = new LINDDUNAnalyzer();

const systemModel = {
  name: 'E-commerce Platform',
  components: [
    { name: 'WebApp', type: 'frontend' },
    { name: 'APIServer', type: 'backend' },
    { name: 'Database', type: 'storage' },
    { name: 'Analytics', type: 'third_party' }
  ]
};

const dataFlows = [
  {
    id: 'user_registration',
    source: 'WebApp',
    target: 'Database',
    dataType: 'personal',
    crossesContexts: false,
    containsUniqueIdentifiers: true,
    encrypted: true,
    metadataLeakage: false,
    auditRequired: true,
    auditEnabled: true,
    consentNotObtained: false,
    sensitiveData: true,
    regulatedData: true,
    largeScale: true
  },
  {
    id: 'behavior_tracking',
    source: 'WebApp',
    target: 'Analytics',
    dataType: 'behavioral',
    crossesContexts: true,
    containsUniqueIdentifiers: true,
    encrypted: false,
    metadataLeakage: true,
    auditRequired: false,
    auditEnabled: false,
    consentNotObtained: true,
    sensitiveData: false,
    regulatedData: false,
    largeScale: true
  }
];

const regulations = ['GDPR', 'CCPA'];

const privacyAnalysis = await linddun.analyzePrivacyThreats(systemModel, dataFlows, regulations);

console.log('LINDDUN Privacy Analysis:');
console.log(`System: ${privacyAnalysis.systemName}`);
console.log(`Total Privacy Threats: ${privacyAnalysis.threats.length}`);

console.log('\nThreats by Category:');
const categoryCount = {};
privacyAnalysis.threats.forEach(threat => {
  categoryCount[threat.category] = (categoryCount[threat.category] || 0) + 1;
});
Object.entries(categoryCount).forEach(([category, count]) => {
  console.log(`- ${category}: ${count} threats`);
});

console.log('\nCompliance Status:');
console.log(`GDPR: ${privacyAnalysis.compliance.gdpr.compliant ? 'Compliant' : 'Non-compliant'}`);
console.log(`CCPA: ${privacyAnalysis.compliance.ccpa.compliant ? 'Compliant' : 'Non-compliant'}`);

console.log('\nKey Recommendations:');
privacyAnalysis.recommendations.forEach(rec => {
  console.log(`- ${rec}`);
});
```

## 🔗 References

Microsoft. (2002). *The DREAD Threat Modeling*. Microsoft Corporation.

FIRST. (2023). *Common Vulnerability Scoring System (CVSS) v3.1 Specification*. Forum of Incident Response and Security Teams.

Schneier, B. (1999). *Attack Trees: Modeling Security Threats*. Dr. Dobb's Journal.

Deng, M., Wuyts, K., Scandariato, R., Preneel, B., & Joosen, W. (2011). *A privacy threat analysis framework: supporting the elicitation and fulfillment of privacy requirements*. Requirements Engineering, 16(1), 3-32.

## 📚 See Also

- [[STRIDE Methodology]] - Core threat modeling framework
- [[PASTA Methodology]] - Risk-centric threat modeling
- [[OCTAVE Framework]] - Organizational threat modeling
- [[CVSS Scoring]] - Vulnerability quantification
- [[Privacy by Design]] - Privacy engineering principles</content>
</xai:function_call name="write">
<parameter name="filePath">shared/n8n-how/wiki/cybersecurity/cybersecurity-frameworks-integration.md