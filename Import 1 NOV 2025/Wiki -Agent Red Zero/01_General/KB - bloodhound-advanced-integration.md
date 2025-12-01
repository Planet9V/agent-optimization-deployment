# BloodHound Advanced Integration for Active Directory Security Assessment

## Overview

BloodHound is a powerful tool for analyzing Active Directory (AD) environments to identify attack paths and privilege escalation opportunities. This section covers advanced integration techniques for automated AD security assessment using n8n workflows.

**Related Sections:**
- [[Kali Linux Integration]] - Basic BloodHound setup and usage
- [[IEC 62443 Part 2]] - Security program requirements for AD environments
- [[Identity Management]] - AD security best practices
- [[Threat Detection]] - Advanced threat hunting with BloodHound data

## Core Components

### BloodHound Architecture

BloodHound consists of three main components:
- **Ingestors**: Collect AD data (SharpHound, AzureHound, etc.)
- **Database**: Neo4j graph database storing AD relationships
- **UI**: Web interface for visualizing attack paths

### Integration with n8n

n8n can automate the entire BloodHound pipeline:
1. Data collection from AD environments
2. Data ingestion into Neo4j
3. Automated query execution
4. Report generation and alerting

## Advanced Data Collection Strategies

### Multi-Method Collection

```json
{
  "parameters": {
    "command": "cd /opt/BloodHound/Ingestors && ./SharpHound.exe --CollectionMethod All,GPOLocalGroup,Session,LoggedOn --OutputDirectory /tmp/bloodhound_data --OutputPrefix comprehensive_ad --DomainController dc01.company.com --LdapUsername 'user@company.com' --LdapPassword '$credentials.ldap_password'",
    "timeout": 900000
  },
  "name": "Comprehensive AD Collection",
  "type": "n8n-nodes-base.executeCommand"
}
```

### Azure AD Integration

```json
{
  "parameters": {
    "command": "cd /opt/BloodHound/Ingestors && ./AzureHound.exe list --tenant company.onmicrosoft.com --username 'user@company.com' --password '$credentials.azure_password' --output /tmp/azurehound_data",
    "timeout": 600000
  },
  "name": "Azure AD Collection",
  "type": "n8n-nodes-base.executeCommand"
}
```

## Advanced Cypher Queries for Attack Path Analysis

### Critical Asset Identification

```cypher
// Find all paths to Domain Admin
MATCH p=(u:User)-[:MemberOf|HasSession|AdminTo|CanRDP|CanPSRemote|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|ReadGMSAPassword|HasSIDHistory|TrustedBy|Contains|GpLink|AddMember|AddSelf|WriteDacl|WriteOwner|GenericWrite|GenericAll|AllExtendedRights|ForceChangePassword*1..]->(g:Group)
WHERE g.name =~ '(?i).*domain admins.*'
RETURN DISTINCT u.name as user, g.name as target, length(p) as path_length
ORDER BY path_length ASC
```

### Kerberoastable Accounts Analysis

```cypher
// Identify kerberoastable service accounts
MATCH (u:User {hasspn:true})
OPTIONAL MATCH (u)-[:MemberOf*1..]->(g:Group)
WHERE NOT g.name =~ '(?i).*domain admins.*' AND NOT g.name =~ '(?i).*enterprise admins.*'
RETURN u.name as service_account, u.pwdlastset as password_age, collect(DISTINCT g.name) as groups
ORDER BY password_age DESC
```

### AS-REP Roastable Users

```cypher
// Find users with DONT_REQ_PREAUTH flag
MATCH (u:User {dontreqpreauth:true})
WHERE NOT u.name =~ '(?i).*krbtgt.*'
RETURN u.name as vulnerable_user, u.enabled as enabled, u.pwdlastset as password_age
```

### Unconstrained Delegation

```cypher
// Identify computers with unconstrained delegation
MATCH (c:Computer {unconstraineddelegation:true})
OPTIONAL MATCH (c)-[:HasSession]->(u:User)
RETURN c.name as computer, collect(DISTINCT u.name) as active_sessions
```

## Automated Risk Assessment Workflows

### n8n Workflow: Critical Path Analysis

```json
{
  "name": "BloodHound Critical Path Analysis",
  "nodes": [
    {
      "parameters": {
        "functionCode": "const neo4j = require('neo4j-driver');\n\nconst driver = neo4j.driver(\n  'bolt://localhost:7687',\n  neo4j.auth.basic('neo4j', $credentials.neo4j_password)\n);\n\nconst session = driver.session();\n\n// Execute critical queries\nconst queries = {\n  domainAdmins: `MATCH p=(u:User)-[:MemberOf*1..]->(g:Group) WHERE g.name =~ '(?i).*domain admins.*' RETURN count(p) as count`,\n  kerberoastable: `MATCH (u:User {hasspn:true}) RETURN count(u) as count`,\n  unconstrained: `MATCH (c:Computer {unconstraineddelegation:true}) RETURN count(c) as count`\n};\n\nconst results = {};\nfor (const [key, query] of Object.entries(queries)) {\n  const result = await session.run(query);\n  results[key] = result.records[0].get('count').toNumber();\n}\n\nawait session.close();\nawait driver.close();\n\nreturn results;"
      },
      "name": "Execute Risk Queries",
      "type": "n8n-nodes-base.function"
    },
    {
      "parameters": {
        "functionCode": "const { domainAdmins, kerberoastable, unconstrained } = $node[\"Execute Risk Queries\"].json;\n\nlet riskScore = 0;\nconst findings = [];\n\nif (domainAdmins > 0) {\n  riskScore += domainAdmins * 10;\n  findings.push(`${domainAdmins} paths to Domain Admin found`);\n}\n\nif (kerberoastable > 0) {\n  riskScore += kerberoastable * 5;\n  findings.push(`${kerberoastable} kerberoastable accounts identified`);\n}\n\nif (unconstrained > 0) {\n  riskScore += unconstrained * 8;\n  findings.push(`${unconstrained} computers with unconstrained delegation`);\n}\n\nreturn {\n  risk_score: riskScore,\n  severity: riskScore > 50 ? 'CRITICAL' : riskScore > 20 ? 'HIGH' : 'MEDIUM',\n  findings: findings,\n  timestamp: new Date().toISOString()\n};"
      },
      "name": "Calculate Risk Score",
      "type": "n8n-nodes-base.function"
    }
  ],
  "connections": {
    "Execute Risk Queries": {
      "main": [
        [
          {
            "node": "Calculate Risk Score",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

## Advanced Attack Path Visualization

### Graph Visualization Workflow

```json
{
  "parameters": {
    "functionCode": "const neo4j = require('neo4j-driver');\n\nconst driver = neo4j.driver(\n  'bolt://localhost:7687',\n  neo4j.auth.basic('neo4j', $credentials.neo4j_password)\n);\n\nconst session = driver.session();\n\n// Get attack paths to critical assets\nconst query = `\n  MATCH p=(u:User)-[:MemberOf|AdminTo|CanRDP|HasSession*1..3]->(c:Computer)\n  WHERE c.name =~ '(?i).*dc.*' OR c.name =~ '(?i).*domain.*'\n  RETURN p, u.name as user, c.name as target, length(p) as path_length\n  ORDER BY path_length ASC\n  LIMIT 20\n`;\n\nconst result = await session.run(query);\nconst paths = result.records.map(record => ({\n  user: record.get('user'),\n  target: record.get('target'),\n  path_length: record.get('path_length'),\n  path: record.get('p')\n}));\n\nawait session.close();\await driver.close();\n\nreturn { attack_paths: paths };"
  },
  "name": "Generate Attack Graph",
  "type": "n8n-nodes-base.function"
}
```

## Automated Remediation Workflows

### Privilege Escalation Mitigation

```json
{
  "name": "BloodHound Remediation Workflow",
  "nodes": [
    {
      "parameters": {
        "functionCode": "const neo4j = require('neo4j-driver');\n\nconst driver = neo4j.driver(\n  'bolt://localhost:7687',\n  neo4j.auth.basic('neo4j', $credentials.neo4j_password)\n);\n\nconst session = driver.session();\n\n// Find users with excessive privileges\nconst query = `\n  MATCH (u:User)-[:MemberOf*1..]->(g:Group)\n  WHERE g.name =~ '(?i).*admin.*' OR g.name =~ '(?i).*operator.*'\n  WITH u, count(g) as group_count\n  WHERE group_count > 5\n  RETURN u.name as user, group_count\n  ORDER BY group_count DESC\n`;\n\nconst result = await session.run(query);\nconst privilegedUsers = result.records.map(record => ({\n  user: record.get('user'),\n  group_count: record.get('group_count')\n}));\n\nawait session.close();\nawait driver.close();\n\nreturn { privileged_users: privilegedUsers };"
      },
      "name": "Identify Privileged Users",
      "type": "n8n-nodes-base.function"
    },
    {
      "parameters": {
        "command": "powershell.exe -Command \"Get-ADUser -Identity '{{$node[\"Identify Privileged Users\"].json.privileged_users[0].user}}' -Properties MemberOf | Select-Object -ExpandProperty MemberOf | ForEach-Object { Get-ADGroup $_ | Select-Object Name, Description }\""
      },
      "name": "Get Group Details",
      "type": "n8n-nodes-base.executeCommand"
    }
  ]
}
```

## Performance Optimization

### Query Optimization Techniques

```javascript
// Use indexes for faster queries
const optimizedQuery = `
// Use specific node labels and properties
MATCH (u:User {enabled: true})
WHERE u.lastlogon > $cutoff_date
MATCH (u)-[:MemberOf*1..2]->(g:Group)
WHERE g.name =~ '(?i).*admin.*'
RETURN u.name, g.name
`;

// Batch processing for large datasets
const batchSize = 1000;
const processInBatches = async (data) => {
  for (let i = 0; i < data.length; i += batchSize) {
    const batch = data.slice(i, i + batchSize);
    await processBatch(batch);
  }
};
```

## Integration with SIEM Systems

### Automated Alert Generation

```json
{
  "parameters": {
    "functionCode": "const criticalFindings = $node[\"Critical Path Analysis\"].json;\n\n// Generate SIEM alerts\nconst alerts = [];\n\nif (criticalFindings.risk_score > 50) {\n  alerts.push({\n    severity: 'CRITICAL',\n    title: 'High-Risk AD Attack Paths Detected',\n    description: `Found ${criticalFindings.findings.length} critical security issues`,\n    details: criticalFindings.findings,\n    timestamp: new Date().toISOString()\n  });\n}\n\nreturn { siem_alerts: alerts };"
  },
  "name": "Generate SIEM Alerts",
  "type": "n8n-nodes-base.function"
}
```

## Case Studies

### Enterprise AD Security Assessment

**Scenario**: Large enterprise with 50,000+ AD objects

**Findings**:
- 15 direct paths to Domain Admin
- 200+ kerberoastable service accounts
- 50 computers with unconstrained delegation

**Automated Response**:
- Generated prioritized remediation plan
- Created change management tickets
- Implemented monitoring for critical paths

### Healthcare Organization Breach Prevention

**Challenge**: Protecting patient data in AD environment

**Solution**: Automated BloodHound scanning with n8n

**Results**:
- Identified 3 critical attack paths
- Implemented least privilege access
- Reduced attack surface by 70%

## Best Practices

### Data Collection
- Schedule regular collection during off-peak hours
- Use dedicated service accounts with minimal privileges
- Store collected data securely with encryption

### Query Performance
- Use specific labels and properties in MATCH clauses
- Limit result sets with LIMIT clause
- Use PROFILE to analyze query execution plans

### Security Considerations
- Never store credentials in workflow definitions
- Use encrypted connections to Neo4j
- Implement access controls on BloodHound UI

## References

- BloodHound. (2025). *Active Directory Security Analysis*. https://bloodhound.readthedocs.io/
- SpecterOps. (2024). *BloodHound Documentation*. https://support.bloodhoundenterprise.io/
- Microsoft. (2024). *Active Directory Security Best Practices*. https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices