---
title: Neo4j Graph Dashboard - Configurable Drill-down Charts
date: 2025-11-02 07:42:03
category: neo4j
subcategory: visualization
tags: [neo4j, graph, dashboard, drill-down, charts, configurable, financial-analytics]
sources: [https://github.com/neo4j-devtools/graph-dashboard, https://neo4j.com/blog/graph-apps-and-graph-stories/, https://neo4j.com/blog/graph-databases-fraud-detection/]
confidence: high
---

## Summary
The Neo4j Graph Dashboard is a configurable chart-based visualization tool designed specifically for analyzing graph data with drill-down capabilities. Built by Neo4j's development team, it provides a structured approach to exploring graph patterns through interactive charts and graphs, particularly effective for Financial Sector analytics and fraud detection investigations.

## Key Information
- **Repository**: neo4j-devtools/graph-dashboard
- **Target Audience**: Community graph analysts, fraud investigators, financial data scientists
- **Architecture**: Graph App with configurable chart components
- **Use Case Focus**: Community graph visualization with drill-down analysis
- **Integration**: Native Neo4j ecosystem integration

## Technical Architecture

### Graph App Framework
```
src/
├── components/
│   ├── ChartRenderer.js          # Configurable chart rendering engine
│   ├── DrillDownController.js    # Interactive drill-down logic
│   ├── CommunityAnalyzer.js      # Community graph analysis tools
│   └── FinancialMetrics.js       # Financial sector specific metrics
├── utils/
│   ├── cypherBuilder.js          # Dynamic Cypher query generation
│   ├── dataAggregator.js         # Chart data preparation
│   └── chartConfigManager.js     # Chart configuration management
└── styles/
    ├── financial-charts.css      # Financial sector chart styles
    └── community-visualization.css # Community analysis styling
```

### Configurable Chart Engine
```javascript
// Financial Dashboard Chart Configuration
const financialChartConfig = {
  // Primary account analysis chart
  accountAnalysis: {
    type: 'sunburst',
    dataSource: {
      query: `
        MATCH (a:Account)-[:OWNS]-(p:Person)
        WHERE a.account_type = $accountType
        RETURN p.name as person, count(a) as account_count, 
               sum(a.balance) as total_balance
        ORDER BY total_balance DESC
        LIMIT 100
      `,
      parameters: {
        accountType: 'personal'
      }
    },
    drillDown: {
      levels: [
        'person_accounts', // Show person's accounts
        'transaction_details', // Show transaction history
        'network_analysis' // Show connected entities
      ],
      queryTemplate: {
        person_accounts: `
          MATCH (p:Person {name: $name})-[r:OWNS]->(a:Account)
          RETURN a.account_id, a.balance, a.account_type
        `,
        transaction_details: `
          MATCH (a:Account)-[:TRANSFERRED]->(t:Transaction)
          WHERE a.account_id = $accountId
          RETURN t.transaction_id, t.amount, t.timestamp
          ORDER BY t.timestamp DESC LIMIT 50
        `,
        network_analysis: `
          MATCH (a:Account)-[r:TRANSFERRED]->(t:Transaction)<-[:RECEIVED]-(other:Account)
          WHERE a.account_id = $accountId AND other.account_id <> $accountId
          RETURN other.account_id, count(r) as interaction_count,
                 sum(r.amount) as total_transferred
        `
      }
    },
    visualization: {
      colorScheme: 'financial_risk',
      sizeMetric: 'total_balance',
      labelFormat: 'account_identifier',
      tooltipContent: 'financial_summary'
    }
  },
  
  // Transaction flow analysis
  transactionFlow: {
    type: 'force_directed_graph',
    dataSource: {
      query: `
        MATCH path = (from:Account)-[r:TRANSFERRED]->(t:Transaction)<-[r2:RECEIVED]-(to:Account)
        WHERE t.timestamp >= datetime() - duration({days: 7})
        RETURN from.account_id as from_account, to.account_id as to_account,
               r.amount as amount, t.timestamp as timestamp
        ORDER BY amount DESC
        LIMIT 500
      `
    },
    drillDown: {
      showTransactionDetails: true,
      highlightSuspiciousPatterns: true,
      overlayRiskScores: true
    },
    filters: {
      amountRange: [1000, 1000000],
      dateRange: 'last_7_days',
      accountTypes: ['personal', 'business', 'corporate']
    }
  },
  
  // Risk assessment dashboard
  riskDashboard: {
    type: 'multi_panel',
    panels: [
      {
        id: 'risk_distribution',
        type: 'pie_chart',
        query: `
          MATCH (p:Person)-[:OWNS]->(a:Account)
          RETURN p.risk_level as risk_level, count(a) as account_count
        `,
        drillDown: 'account_list'
      },
      {
        id: 'suspicious_activity',
        type: 'bar_chart',
        query: `
          MATCH (t:Transaction)
          WHERE t.status = 'flagged'
          RETURN t.transaction_type, count(t) as suspicious_count
          ORDER BY suspicious_count DESC
        `,
        drillDown: 'transaction_analysis'
      },
      {
        id: 'high_value_accounts',
        type: 'scatter_plot',
        query: `
          MATCH (a:Account)
          WHERE a.balance > 100000
          RETURN a.account_id, a.balance, a.risk_score
        `,
        drillDown: 'account_risk_analysis'
      }
    ]
  }
};
```

### Drill-down Implementation
```javascript
// Interactive Drill-down Controller
class FinancialDrillDownController {
  constructor(config) {
    this.chartConfigs = config.charts;
    this.currentLevel = 0;
    this.drillPath = [];
    this.dataCache = new Map();
  }
  
  // Execute drill-down action
  async drillDown(chartId, selectedData, level) {
    const chartConfig = this.chartConfigs[chartId];
    const drillDownConfig = chartConfig.drillDown;
    
    try {
      const nextLevel = level + 1;
      const drillQuery = this.buildDrillDownQuery(
        drillDownConfig.queryTemplate,
        selectedData,
        nextLevel
      );
      
      const results = await this.executeQuery(drillQuery);
      const processedData = this.processDrillDownResults(results, selectedData);
      
      // Update drill path
      this.drillPath.push({
        level: level,
        chartId: chartId,
        data: selectedData,
        results: processedData
      });
      
      return {
        success: true,
        data: processedData,
        nextLevel: nextLevel,
        drillPath: this.drillPath
      };
    } catch (error) {
      console.error('Drill-down error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  // Build financial-specific drill-down queries
  buildDrillDownQuery(queryTemplate, selectedData, level) {
    if (selectedData.person_name) {
      // Person-level drill-down
      return queryTemplate.person_accounts.replace('$name', selectedData.person_name);
    } else if (selectedData.account_id) {
      // Account-level drill-down
      return queryTemplate.transaction_details.replace('$accountId', selectedData.account_id);
    } else if (selectedData.transaction_id) {
      // Transaction-level drill-down
      return queryTemplate.network_analysis.replace('$transactionId', selectedData.transaction_id);
    }
    
    return queryTemplate;
  }
  
  // Process financial drill-down results
  processDrillDownResults(results, originalData) {
    return {
      summary: {
        totalTransactions: results.length,
        totalAmount: results.reduce((sum, r) => sum + (r.amount || 0), 0),
        dateRange: {
          earliest: new Date(Math.min(...results.map(r => new Date(r.timestamp)))),
          latest: new Date(Math.max(...results.map(r => new Date(r.timestamp))))
        }
      },
      suspiciousIndicators: this.identifySuspiciousPatterns(results),
      recommendations: this.generateRecommendations(results, originalData),
      drillableEntities: this.identifyDrillableEntities(results)
    };
  }
  
  // Identify suspicious patterns in financial data
  identifySuspiciousPatterns(results) {
    return results.reduce((patterns, record) => {
      const amount = parseFloat(record.amount || 0);
      const timestamp = new Date(record.timestamp);
      
      // Pattern detection logic
      if (amount >= 10000 && amount % 1000 === 0) {
        patterns.roundAmount.push({
          amount: amount,
          frequency: 1,
          flag: 'Rounded transaction amount'
        });
      }
      
      const hour = timestamp.getHours();
      if (hour < 6 || hour > 22) {
        patterns.unusualTime.push({
          timestamp: timestamp,
          amount: amount,
          flag: 'Unusual transaction time'
        });
      }
      
      return patterns;
    }, { roundAmount: [], unusualTime: [] });
  }
}
```

## Key Features

### Configurable Chart Types
- **Sunburst Charts**: Hierarchical data exploration with multiple levels
- **Force-Directed Graphs**: Network relationship visualization
- **Bar Charts**: Statistical analysis with drill-down to underlying data
- **Scatter Plots**: Correlation analysis with filtering capabilities
- **Multi-Panel Dashboards**: Combined view of multiple chart types

### Financial-Specific Analytics
```javascript
// Financial risk assessment algorithms
const FinancialAnalytics = {
  // Calculate account risk scores
  calculateRiskScore: (account, transactions, networkData) => {
    let riskScore = 0;
    
    // Transaction-based risk factors
    const suspiciousTransactions = transactions.filter(t => 
      t.status === 'flagged' || t.amount >= 10000
    );
    riskScore += suspiciousTransactions.length * 10;
    
    // Network-based risk factors
    const highRiskConnections = networkData.filter(n => 
      n.risk_level === 'high' || n.suspicious_flag
    );
    riskScore += highRiskConnections.length * 15;
    
    // Account-based risk factors
    if (account.balance >= 500000) riskScore += 5;
    if (account.account_type === 'corporate' && account.industry === 'high_risk') {
      riskScore += 20;
    }
    
    return Math.min(riskScore, 100); // Cap at 100
  },
  
  // Identify fraud patterns
  detectFraudPatterns: (graphData) => {
    const patterns = [];
    
    // Circular transaction detection
    patterns.push({
      type: 'circular_transactions',
      detection: `
        MATCH path = (a:Account)-[:TRANSFERRED]->(t1:Transaction)<-[:RECEIVED]-(b:Account)
                     -[:TRANSFERRED]->(t2:Transaction)<-[:RECEIVED]-(a:Account)
        RETURN a, b, t1, t2, length(path) as cycle_length
        HAVING cycle_length <= 4
      `,
      riskLevel: 'high'
    });
    
    // Rapid transaction detection
    patterns.push({
      type: 'rapid_transactions',
      detection: `
        MATCH (a:Account)-[r:TRANSFERRED]->(t:Transaction)
        WHERE t.timestamp >= datetime() - duration({minutes: 10})
        WITH a, count(r) as transaction_count
        WHERE transaction_count > 10
        RETURN a, transaction_count
      `,
      riskLevel: 'medium'
    });
    
    return patterns;
  }
};
```

### Interactive Navigation
- **Breadcrumb Navigation**: Clear path through drill-down levels
- **Contextual Filtering**: Filter charts based on selection context
- **Synchronized Views**: Multiple charts that update together
- **Export Capabilities**: Export drill-down analysis results
- **Bookmark Functionality**: Save and share specific chart configurations

## Community Graph Integration

### Community Analysis Workflow
```cypher
// Community detection for financial networks
CALL gds.graph.project('financialNetwork',
  ['Account', 'Person', 'Merchant'],
  ['TRANSFERRED', 'OWNS', 'TRANSACTS_WITH']
);

// Find communities (potential fraud rings)
CALL gds.louvain.stream('financialNetwork')
YIELD nodeId, communityId
WITH gds.util.asNode(nodeId) as node, communityId
WHERE node:Account
MATCH (node)-[:OWNS]->(person:Person)
RETURN person.name, node.account_id, communityId,
       sum(node.balance) as community_balance
ORDER BY community_balance DESC
LIMIT 20;

// Calculate community risk scores
CALL gds.pageRank.stream('financialNetwork')
YIELD nodeId, score
WITH gds.util.asNode(nodeId) as node, score
WHERE node:Account
MATCH (node)-[:OWNS]->(person:Person)
WHERE score > 0.1 // High importance
RETURN person.name, node.account_id, score,
       'High Risk Community' as risk_category
ORDER BY score DESC;
```

### Financial Entity Relationships
```cypher
// Analyze financial relationships in community context
MATCH (c:Community)<-[:BELONGS_TO]-(a:Account)-[r:TRANSFERRED]->(t:Transaction)<-[:RECEIVED]-(other:Account)
WHERE c.community_id = $communityId
OPTIONAL MATCH (t)-[:INVOLVES]->(merchant:Merchant)
RETURN 
  a.account_id as account,
  other.account_id as connected_account,
  sum(r.amount) as transaction_volume,
  count(t) as transaction_count,
  collect(DISTINCT merchant.name) as merchants_used,
  avg(r.amount) as avg_transaction_amount
ORDER BY transaction_volume DESC
LIMIT 50;
```

## Setup and Installation

### Prerequisites
- **Neo4j Desktop**: Required for Graph App integration
- **Neo4j Version**: 4.0 or higher
- **Plugin Requirements**: 
  - APOC procedures
  - Graph Data Science plugin (for advanced analytics)
  - Graph Algorithms (for community detection)

### Installation Process
```bash
# Install via Neo4j Desktop
# 1. Open Neo4j Desktop
# 2. Go to Plugins tab
# 3. Search for "Neo4j Graph Dashboard"
# 4. Click Install
# 5. Restart Neo4j and relaunch Graph App

# Or manual installation
cd ~/.neo4j/neo4j-desktop/apps/[app-id]/graph-dashboard
npm install
npm run build
```

### Configuration Setup
```javascript
// dashboard-config.js
const dashboardConfig = {
  neo4j: {
    uri: 'bolt://localhost:7687',
    database: 'neo4j',
    authentication: {
      username: 'neo4j',
      password: 'password'
    }
  },
  
  // Financial dashboard settings
  financial: {
    defaultAccountType: 'all',
    riskThreshold: 70,
    amountFilter: {
      min: 1000,
      max: 1000000
    },
    timeframe: 'last_30_days'
  },
  
  // Chart configuration
  charts: {
    defaultType: 'sunburst',
    animationDuration: 1000,
    colorScheme: 'financial_risk',
    drillDownEnabled: true
  },
  
  // Performance settings
  performance: {
    maxNodesPerChart: 5000,
    maxDepth: 5,
    cacheExpiry: 300000, // 5 minutes
    enableWebWorkers: true
  }
};
```

## Performance Optimization

### Large Dataset Handling
```javascript
// Efficient data processing for financial datasets
const DataProcessor = {
  // Stream processing for large transaction datasets
  streamTransactionData: async (query, batchSize = 1000) => {
    const session = driver.session();
    const stream = session.run(query);
    const batch = [];
    
    for await (const record of stream) {
      const processedRecord = this.processFinancialRecord(record);
      batch.push(processedRecord);
      
      if (batch.length >= batchSize) {
        yield batch;
        batch.length = 0;
      }
    }
    
    if (batch.length > 0) {
      yield batch;
    }
    
    await session.close();
  },
  
  // Parallel processing for chart data aggregation
  aggregateChartData: async (queries, chartType) => {
    const promises = queries.map(query => this.executeQuery(query));
    const results = await Promise.all(promises);
    
    switch (chartType) {
      case 'sunburst':
        return this.formatSunburstData(results);
      case 'force_directed':
        return this.formatNetworkData(results);
      case 'scatter_plot':
        return this.formatScatterData(results);
      default:
        return this.formatGenericData(results);
    }
  }
};
```

### Caching Strategy
```javascript
// Intelligent caching for financial data
class FinancialDataCache {
  constructor() {
    this.queryCache = new Map();
    this.chartCache = new Map();
    this.expiresAt = new Map();
  }
  
  // Cache with financial data awareness
  set(query, data, financialContext) {
    const key = this.generateCacheKey(query, financialContext);
    
    // Shorter expiry for real-time data
    let expiryTime = 300000; // 5 minutes default
    
    if (financialContext.includes('real-time')) {
      expiryTime = 60000; // 1 minute for real-time
    } else if (financialContext.includes('historical')) {
      expiryTime = 3600000; // 1 hour for historical
    }
    
    this.queryCache.set(key, data);
    this.expiresAt.set(key, Date.now() + expiryTime);
  }
  
  // Get cached data with validation
  get(query, financialContext) {
    const key = this.generateCacheKey(query, financialContext);
    const expires = this.expiresAt.get(key);
    
    if (expires && Date.now() > expires) {
      this.delete(key);
      return null;
    }
    
    return this.queryCache.get(key);
  }
}
```

## Financial Sector Applications

### Fraud Investigation Dashboard
- **Multi-level Analysis**: From high-level risk overview to detailed transaction analysis
- **Pattern Recognition**: Automated detection of suspicious patterns
- **Investigation Workflow**: Guided investigation process with recommended queries
- **Evidence Collection**: Automated collection of evidence and patterns

### Banking Operations Analytics
- **Account Portfolio Analysis**: Comprehensive account relationship mapping
- **Transaction Flow Analysis**: Real-time money flow visualization
- **Customer Segmentation**: Risk-based customer classification
- **Product Performance**: Banking product usage and profitability analysis

### Regulatory Compliance
- **AML Monitoring**: Suspicious activity pattern identification
- **KYC Enhancement**: Identity verification through network analysis
- **Regulatory Reporting**: Automated visualization for compliance reports
- **Audit Trail**: Complete transaction and relationship history

## Security and Compliance

### Data Protection
```javascript
// Financial data security implementation
const SecurityManager = {
  // Mask sensitive financial information in visualizations
  maskSensitiveData: (data, userRole) => {
    return data.map(record => {
      const masked = { ...record };
      
      // Mask account numbers for non-admin users
      if (userRole !== 'admin' && masked.account_id) {
        masked.account_id = masked.account_id.slice(0, -4) + '****';
      }
      
      // Mask customer names
      if (masked.customer_name && userRole === 'analyst') {
        masked.customer_name = masked.customer_name[0] + '***';
      }
      
      // Truncate transaction amounts for non-admin
      if (userRole !== 'admin' && masked.amount) {
        masked.amount_range = this.getAmountRange(masked.amount);
      }
      
      return masked;
    });
  },
  
  // Audit logging for dashboard usage
  logUserAction: (userId, action, query, dataAccess) => {
    const auditLog = {
      timestamp: new Date().toISOString(),
      userId: userId,
      action: action,
      query: query.substring(0, 500), // Log first 500 chars
      dataAccess: dataAccess,
      sessionId: getSessionId()
    };
    
    // Store in Neo4j for later analysis
    session.run(
      `CREATE (log:AuditLog {timestamp: $timestamp, userId: $userId, 
                           action: $action, query: $query, sessionId: $sessionId})`,
      auditLog
    );
  }
};
```

## Related Topics
- [NeoDash Dashboard Builder](/neo4j/visualization/neodash-20251102-07)
- [Neo4j-Data-Visualization-Dashboard](/neo4j/visualization/neo4j-data-visualization-dashboard-20251102-07)
- [Financial Fraud Detection Patterns](/financial/fraud-detection-patterns-20251102-07)
- [Community Detection in Financial Networks](/financial/community-detection-financial-networks-20251102-07)
- [Neo4j GDS Financial Algorithms](/financial/neo4j-gds-financial-algorithms-20251102-07)

## References
- [Neo4j Graph Dashboard GitHub](https://github.com/neo4j-devtools/graph-dashboard) - Official repository
- [Neo4j Graph Apps Documentation](https://neo4j.com/blog/graph-apps-and-graph-stories/) - Graph App framework
- [Community Graph Analysis](https://neo4j.com/graphgists/bank-fraud-detection/) - Official fraud detection guide
- [Graph Data Science Documentation](https://neo4j.com/docs/graph-data-science/current/) - GDS library documentation
- [Neo4j Desktop](https://neo4j.com/product/neo4j-desktop/) - Desktop application and plugin management

## Metadata
- Last Updated: 2025-11-02 07:42:03
- Research Session: 489469
- Completeness: 85%
- Next Actions: Implement community analysis workflows for fraud ring detection
