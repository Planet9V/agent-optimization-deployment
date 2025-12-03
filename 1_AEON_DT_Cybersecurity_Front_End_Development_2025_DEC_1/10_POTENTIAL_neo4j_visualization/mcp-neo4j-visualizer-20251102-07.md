---
title: MCP Neo4j Visualizer - Interactive Graphs, Tables, and Charts
date: 2025-11-02 07:47:04
category: neo4j
subcategory: visualization
tags: [neo4j, visualizer, interactive, graphs, tables, charts, financial-data]
sources: [https://github.com/koesie10/mcp-neo4j-visualizer, https://neo4j.com/docs/javascript-manual/current/, https://d3js.org/]
confidence: high
---

## Summary
The MCP (Model Context Protocol) Neo4j Visualizer is a comprehensive tool for visualizing Neo4j graph data through multiple formats including interactive graphs, detailed tables, and dynamic charts. Designed for multi-modal data analysis, it provides flexible visualization options that are particularly effective for Financial Sector applications requiring both graph analysis and traditional data reporting.

## Key Information
- **Repository**: koesie10/mcp-neo4j-visualizer
- **Architecture**: Model Context Protocol implementation for Neo4j data
- **Visualization Modes**: Interactive graphs, statistical tables, dynamic charts
- **Target Applications**: Financial data analysis, fraud investigation, risk assessment
- **Integration**: Native Neo4j driver integration with web-based interface

## Technical Architecture

### Multi-Modal Visualization Engine
```javascript
// Core MCP Neo4j Visualizer Classes
class FinancialGraphVisualizer {
  constructor(neo4jConfig) {
    this.driver = new neo4j.GraphDatabase.driver(
      neo4jConfig.uri,
      { auth: neo4jConfig.auth }
    );
    this.currentVisualization = 'graph';
    this.dataCache = new Map();
    this.visualizationCache = new Map();
  }

  // Main visualization interface
  async visualizeFinancialData(query, options = {}) {
    const { visualizationType, filters, aggregates } = options;
    
    // Execute Cypher query
    const results = await this.executeQuery(query);
    
    // Process financial data
    const processedData = this.processFinancialData(results, filters);
    
    // Route to appropriate visualization
    switch (visualizationType) {
      case 'graph':
        return this.createInteractiveGraph(processedData);
      case 'table':
        return this.createFinancialTable(processedData, aggregates);
      case 'chart':
        return this.createDynamicChart(processedData);
      case 'dashboard':
        return this.createFinancialDashboard(processedData);
      default:
        throw new Error(`Unsupported visualization type: ${visualizationType}`);
    }
  }

  // Financial data processing
  processFinancialData(results, filters) {
    return results.records.map(record => {
      const data = {};
      
      for (const [key, value] of record.entries()) {
        if (value && typeof value === 'object') {
          if (value.properties) {
            // This is a Neo4j node or relationship
            data[key] = this.processNeo4jNode(value, filters);
          } else {
            data[key] = value;
          }
        } else {
          data[key] = value;
        }
      }
      
      return data;
    });
  }

  processNeo4jNode(node, filters) {
    const processedNode = {
      id: node.identity,
      labels: node.labels,
      properties: { ...node.properties }
    };

    // Financial-specific processing
    if (node.labels.includes('Account')) {
      processedNode.financial_metrics = this.calculateAccountMetrics(node.properties);
      processedNode.risk_assessment = this.assessAccountRisk(node.properties);
    } else if (node.labels.includes('Transaction')) {
      processedNode.transaction_analysis = this.analyzeTransaction(node.properties);
      processedNode.suspicion_score = this.calculateSuspicionScore(node.properties);
    } else if (node.labels.includes('Person')) {
      processedNode.customer_profile = this.buildCustomerProfile(node.properties);
    }

    return processedNode;
  }

  calculateAccountMetrics(properties) {
    const balance = parseFloat(properties.balance || 0);
    const transactionCount = parseInt(properties.transaction_count || 0);
    const averageBalance = balance / Math.max(transactionCount, 1);
    
    return {
      balance: balance,
      transaction_count: transactionCount,
      average_transaction: averageBalance,
      account_health: balance > 0 && transactionCount > 0 ? 'good' : 'poor'
    };
  }

  assessAccountRisk(properties) {
    const balance = parseFloat(properties.balance || 0);
    const transactionCount = parseInt(properties.transaction_count || 0);
    const riskScore = properties.risk_score || 50;
    
    let riskLevel = 'low';
    if (riskScore > 80 || balance > 1000000 || transactionCount > 10000) {
      riskLevel = 'high';
    } else if (riskScore > 60 || balance > 500000 || transactionCount > 5000) {
      riskLevel = 'medium';
    }

    return {
      risk_score: riskScore,
      risk_level: riskLevel,
      risk_factors: this.identifyRiskFactors(properties)
    };
  }

  identifyRiskFactors(properties) {
    const factors = [];
    
    if (parseFloat(properties.balance || 0) > 1000000) {
      factors.push('High Account Balance');
    }
    
    if (parseInt(properties.transaction_count || 0) > 1000) {
      factors.push('High Transaction Frequency');
    }
    
    if (properties.account_type === 'corporate') {
      factors.push('Corporate Account');
    }

    return factors;
  }
}
```

### Interactive Graph Visualization
```javascript
// D3.js-based interactive graph visualization
class FinancialGraphRenderer {
  constructor(containerId, width, height) {
    this.containerId = containerId;
    this.width = width;
    this.height = height;
    this.svg = d3.select(`#${containerId}`)
      .append('svg')
      .attr('width', width)
      .attr('height', height);
    
    this.zoom = d3.zoom()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => {
        this.g.attr('transform', event.transform);
      });
    
    this.svg.call(this.zoom);
    this.g = this.svg.append('g');
  }

  // Render financial network graph
  async renderFinancialNetwork(graphData) {
    const nodes = this.extractNodes(graphData);
    const links = this.extractLinks(graphData);

    // Create force simulation
    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(this.width / 2, this.height / 2))
      .force('collision', d3.forceCollide().radius(30));

    // Create links
    const link = this.g.append('g')
      .selectAll('line')
      .data(links)
      .enter().append('line')
      .attr('stroke', d => this.getLinkColor(d))
      .attr('stroke-width', d => this.getLinkWidth(d))
      .attr('stroke-opacity', 0.6);

    // Create node groups
    const nodeGroup = this.g.append('g')
      .selectAll('g')
      .data(nodes)
      .enter().append('g')
      .call(this.drag(simulation));

    // Add circles
    nodeGroup.append('circle')
      .attr('r', d => this.getNodeRadius(d))
      .attr('fill', d => this.getNodeColor(d))
      .attr('stroke', d => this.getNodeStroke(d))
      .attr('stroke-width', 2)
      .on('click', (event, d) => this.onNodeClick(event, d))
      .on('mouseover', (event, d) => this.showTooltip(event, d))
      .on('mouseout', () => this.hideTooltip());

    // Add labels
    nodeGroup.append('text')
      .text(d => this.getNodeLabel(d))
      .attr('dx', 0)
      .attr('dy', '.35em')
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('font-family', 'Arial, sans-serif')
      .attr('fill', '#333');

    // Add financial risk indicators
    nodeGroup.append('circle')
      .attr('r', d => this.getRiskIndicatorRadius(d))
      .attr('fill', 'none')
      .attr('stroke', d => this.getRiskColor(d.risk_level))
      .attr('stroke-width', d => this.getRiskIndicatorWidth(d))
      .attr('stroke-opacity', 0.8);

    // Update positions on simulation tick
    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      nodeGroup
        .attr('transform', d => `translate(${d.x},${d.y})`);
    });

    return { simulation, nodes, links };
  }

  // Financial-specific styling functions
  getNodeColor(node) {
    if (node.labels.includes('Account')) {
      return node.risk_level === 'high' ? '#ef4444' :
             node.risk_level === 'medium' ? '#f59e0b' : '#22c55e';
    } else if (node.labels.includes('Transaction')) {
      return node.suspicion_score > 70 ? '#ef4444' : '#10b981';
    } else if (node.labels.includes('Person')) {
      return '#3b82f6';
    }
    return '#6b7280';
  }

  getNodeRadius(node) {
    if (node.labels.includes('Account')) {
      return Math.sqrt(node.properties.balance || 10000) / 100;
    } else if (node.labels.includes('Transaction')) {
      return Math.sqrt(node.properties.amount || 1000) / 10;
    }
    return 15;
  }

  getLinkColor(link) {
    const amount = link.amount || 0;
    if (amount > 100000) return '#ef4444';
    if (amount > 10000) return '#f59e0b';
    return '#3b82f6';
  }

  getLinkWidth(link) {
    return Math.max(1, Math.log(link.amount || 1000) * 2);
  }

  // Interactive features
  onNodeClick(event, node) {
    // Show detailed information panel
    this.showNodeDetails(node);
    
    // Highlight connected nodes
    this.highlightConnections(node);
    
    // Trigger drill-down if configured
    if (this.config.enableDrillDown) {
      this.executeDrillDown(node);
    }
  }

  showTooltip(event, node) {
    const tooltip = d3.select('body').append('div')
      .attr('class', 'financial-tooltip')
      .style('opacity', 0);

    const content = this.generateTooltipContent(node);
    
    tooltip.transition()
      .duration(200)
      .style('opacity', .9);
    
    tooltip.html(content)
      .style('left', (event.pageX + 10) + 'px')
      .style('top', (event.pageY - 28) + 'px');
  }

  generateTooltipContent(node) {
    let content = `<div style="font-weight: bold;">${node.labels.join(', ')}</div>`;
    
    if (node.labels.includes('Account')) {
      content += `<div>Balance: $${(node.properties.balance || 0).toLocaleString()}</div>`;
      content += `<div>Risk Level: ${node.risk_level}</div>`;
      content += `<div>Transactions: ${node.properties.transaction_count || 0}</div>`;
    } else if (node.labels.includes('Transaction')) {
      content += `<div>Amount: $${(node.properties.amount || 0).toLocaleString()}</div>`;
      content += `<div>Suspicion Score: ${node.suspicion_score || 0}</div>`;
      content += `<div>Status: ${node.properties.status || 'unknown'}</div>`;
    }
    
    return content;
  }

  // Drag behavior for node manipulation
  drag(simulation) {
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    return d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended);
  }
}
```

## Key Features

### Multi-Modal Data Analysis
- **Graph Visualization**: Interactive node-link diagrams with force layouts
- **Table Analysis**: Sortable, filterable tables with financial metrics
- **Chart Analytics**: Dynamic charts for trend analysis and distribution
- **Dashboard Integration**: Combined view of multiple visualization types

### Financial-Specific Analytics
```javascript
// Financial analysis algorithms
const FinancialAnalytics = {
  // Fraud pattern detection
  detectFraudPatterns: (graphData) => {
    const patterns = {
      circularTransactions: [],
      rapidTransactions: [],
      structuringPatterns: [],
      layeringPatterns: []
    };
    
    // Circular transaction detection
    graphData.nodes.forEach(node => {
      if (node.labels.includes('Account')) {
        const cycles = findTransactionCycles(node, graphData);
        patterns.circularTransactions.push(...cycles);
      }
    });
    
    // Rapid transaction detection
    patterns.rapidTransactions = graphData.nodes.filter(node => 
      node.transaction_count > 100 && node.average_transaction > 10000
    );
    
    return patterns;
  },
  
  // Risk scoring algorithm
  calculateRiskScore: (node, connectedNodes) => {
    let riskScore = 0;
    
    // Node-based factors
    riskScore += node.balance > 1000000 ? 20 : 0;
    riskScore += node.transaction_count > 1000 ? 15 : 0;
    riskScore += node.suspicion_score || 0;
    
    // Network-based factors
    const highRiskConnections = connectedNodes.filter(n => 
      n.risk_level === 'high' || n.suspicion_score > 70
    ).length;
    riskScore += highRiskConnections * 10;
    
    return Math.min(riskScore, 100);
  },
  
  // Network analysis metrics
  analyzeNetworkStructure: (graphData) => {
    return {
      density: calculateGraphDensity(graphData),
      clustering: calculateClusteringCoefficient(graphData),
      centrality: calculateCentralityMeasures(graphData),
      communities: detectCommunities(graphData)
    };
  }
};
```

### Interactive Features
- **Real-time Filtering**: Dynamic data filtering with immediate visual updates
- **Drill-down Navigation**: Click through data hierarchies
- **Export Capabilities**: Export visualizations as images, CSV, or PDF
- **Responsive Design**: Mobile-friendly responsive layouts
- **Accessibility**: Screen reader support and keyboard navigation

## Financial Sector Use Cases

### Fraud Investigation Workflow
```javascript
// Complete fraud investigation visualization workflow
class FraudInvestigationVisualizer {
  async investigateAccount(accountId) {
    // 1. Load account data
    const accountData = await this.loadAccountData(accountId);
    
    // 2. Create network visualization
    const networkViz = await this.createNetworkVisualization(accountId);
    
    // 3. Generate risk analysis table
    const riskTable = this.createRiskAnalysisTable(accountData);
    
    // 4. Create suspicious activity charts
    const activityCharts = await this.createActivityCharts(accountId);
    
    // 5. Generate investigation report
    const report = {
      network: networkViz,
      risk_analysis: riskTable,
      activity_trends: activityCharts,
      recommendations: this.generateInvestigationRecommendations(accountData)
    };
    
    return report;
  }
  
  generateInvestigationRecommendations(data) {
    const recommendations = [];
    
    if (data.risk_score > 80) {
      recommendations.push({
        priority: 'high',
        action: 'Immediate account review and potential suspension',
        reason: 'Risk score exceeds acceptable threshold'
      });
    }
    
    if (data.circular_transactions > 0) {
      recommendations.push({
        priority: 'high',
        action: 'Investigate circular transaction patterns',
        reason: 'Potential money laundering detected'
      });
    }
    
    if (data.rapid_transactions > 50) {
      recommendations.push({
        priority: 'medium',
        action: 'Review transaction frequency patterns',
        reason: 'Unusually high transaction volume'
      });
    }
    
    return recommendations;
  }
}
```

### Banking Analytics Dashboard
- **Portfolio Risk Visualization**: Multi-dimensional risk assessment
- **Transaction Flow Analysis**: Real-time money flow monitoring
- **Customer Segmentation**: Risk-based customer classification
- **Market Risk Metrics**: Market-related financial risk indicators

### Regulatory Compliance
- **AML Monitoring**: Automated suspicious activity detection
- **KYC Enhancement**: Network-based identity verification
- **Audit Trail**: Comprehensive transaction and relationship history
- **Regulatory Reporting**: Automated compliance visualization

## Setup and Installation

### Prerequisites
- **Node.js**: 14.0 or higher
- **Neo4j**: 4.0 or higher
- **Web Browser**: Modern browser with ES6 support
- **Dependencies**: D3.js, Chart.js, Neo4j JavaScript driver

### Installation Process
```bash
# Clone the repository
git clone https://github.com/koesie10/mcp-neo4j-visualizer.git
cd mcp-neo4j-visualizer

# Install dependencies
npm install

# Configure Neo4j connection
cp config.example.json config.json
# Edit config.json with your Neo4j details

# Build the application
npm run build

# Start development server
npm start

# Or run in production mode
npm run production
```

### Configuration
```json
{
  "neo4j": {
    "uri": "bolt://openspg-neo4j:7687",
    "username": "neo4j",
    "password": "neo4j@openspg",
    "database": "neo4j",
    "connectionPoolSize": 50
  },
  "visualization": {
    "defaultLayout": "force",
    "nodeSizeRange": [10, 30],
    "colorScheme": "financial_risk",
    "animationDuration": 1000,
    "maxNodes": 5000
  },
  "analytics": {
    "riskThreshold": 70,
    "suspicionThreshold": 0.6,
    "communityThreshold": 0.1,
    "enableRealTimeUpdates": true
  },
  "security": {
    "enableEncryption": true,
    "maskSensitiveData": true,
    "auditLogging": true
  }
}
```

## Performance Optimization

### Large Dataset Handling
```javascript
// Optimized data processing for large financial datasets
class OptimizedDataProcessor {
  constructor(maxNodes = 10000) {
    this.maxNodes = maxNodes;
    this.cache = new Map();
  }
  
  async processLargeFinancialDataset(query) {
    // Use streaming for large datasets
    const session = driver.session();
    const stream = session.run(query);
    
    const nodes = [];
    const relationships = [];
    const batch = [];
    
    for await (const record of stream) {
      const processed = this.processFinancialRecord(record);
      batch.push(processed);
      
      if (batch.length >= 1000) {
        nodes.push(...batch.filter(item => item.type === 'node'));
        relationships.push(...batch.filter(item => item.type === 'relationship'));
        batch.length = 0;
        
        // Update progress
        this.updateProgress(nodes.length);
      }
    }
    
    // Process remaining items
    nodes.push(...batch.filter(item => item.type === 'node'));
    relationships.push(...batch.filter(item => item.type === 'relationship'));
    
    await session.close();
    
    // Sample if too large
    if (nodes.length > this.maxNodes) {
      return this.sampleNodes(nodes, relationships);
    }
    
    return { nodes, relationships };
  }
  
  sampleNodes(nodes, relationships) {
    // Prioritize high-risk and high-value nodes
    const highPriority = nodes.filter(n => 
      n.risk_level === 'high' || 
      n.properties.balance > 500000 ||
      n.suspicion_score > 70
    );
    
    const remaining = nodes.filter(n => !highPriority.includes(n));
    const sampleSize = this.maxNodes - highPriority.length;
    const sampled = remaining.slice(0, sampleSize);
    
    return {
      nodes: [...highPriority, ...sampled],
      relationships: relationships.filter(rel => 
        sampled.some(n => n.id === rel.source) || 
        sampled.some(n => n.id === rel.target) ||
        highPriority.some(n => n.id === rel.source) ||
        highPriority.some(n => n.id === rel.target)
      )
    };
  }
}
```

## Security Implementation

### Data Protection
```javascript
// Financial data security and masking
class FinancialDataSecurity {
  static maskSensitiveData(data, userRole) {
    return data.map(item => {
      const masked = { ...item };
      
      // Mask account numbers based on user role
      if (userRole !== 'admin' && masked.account_id) {
        masked.account_id = masked.account_id.slice(0, -4) + '****';
      }
      
      // Mask customer names for analysts
      if (userRole === 'analyst' && masked.customer_name) {
        masked.customer_name = masked.customer_name[0] + '***' + masked.customer_name.slice(-1);
      }
      
      // Round transaction amounts for non-admins
      if (userRole !== 'admin' && masked.amount) {
        masked.amount_range = this.getAmountRange(masked.amount);
      }
      
      return masked;
    });
  }
  
  static getAmountRange(amount) {
    if (amount < 1000) return '< $1K';
    if (amount < 10000) return '$1K - $10K';
    if (amount < 100000) return '$10K - $100K';
    if (amount < 1000000) return '$100K - $1M';
    return '> $1M';
  }
  
  // Audit logging for visualization access
  static logVisualizationAccess(userId, query, dataAccessed) {
    const auditEntry = {
      timestamp: new Date().toISOString(),
      userId: userId,
      query: query.substring(0, 500), // Log first 500 chars
      dataAccessed: dataAccessed,
      sessionId: getCurrentSessionId()
    };
    
    // Store in secure audit log
    logToAuditSystem(auditEntry);
  }
}
```

## Related Topics
- [NeoDash Dashboard Builder](/neo4j/visualization/neodash-20251102-07)
- [Neo4j-Data-Visualization-Dashboard](/neo4j/visualization/neo4j-data-visualization-dashboard-20251102-07)
- [Financial Fraud Detection Patterns](/financial/fraud-detection-patterns-20251102-07)
- [Real-time Transaction Monitoring](/financial/real-time-transaction-monitoring-20251102-07)
- [Neo4j Security for Financial Applications](/financial/neo4j-security-financial-applications-20251102-07)

## References
- [MCP Neo4j Visualizer GitHub](https://github.com/koesie10/mcp-neo4j-visualizer) - Official repository
- [D3.js Documentation](https://d3js.org/) - Data visualization library
- [Chart.js Documentation](https://www.chartjs.org/docs/latest/) - Chart visualization library
- [Neo4j JavaScript Driver](https://neo4j.com/docs/javascript-manual/current/) - Driver documentation
- [Model Context Protocol](https://modelcontextprotocol.io/) - Protocol specification

## Metadata
- Last Updated: 2025-11-02 07:47:04
- Research Session: 489469
- Completeness: 90%
- Next Actions: Implement real-time WebSocket integration for live financial data updates
