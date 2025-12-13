# UI DEVELOPER GUIDE - API Integration

**Last Updated**: 2025-12-12
**Status**: Complete
**For**: Frontend developers building UI against the OXOT API

---

## QUICK START

### System Access
- **NER11-GOLD-API**: `http://localhost:8000`
- **AEON-SAAS-DEV**: `http://localhost:3000`
- **Required Header**: `x-customer-id: dev`
- **Auth (when needed)**: `Authorization: Bearer YOUR_TOKEN`

### Test Connection
```bash
# Test ner11-gold-api is running
curl http://localhost:8000/health

# Test aeon-saas-dev is running
curl http://localhost:3000/api/health
```

---

## WORKING APIs (READY TO USE)

### 1. SBOM APIs

#### List All SBOMs
```javascript
// GET /api/v2/sbom/sboms
fetch('http://localhost:8000/api/v2/sbom/sboms', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(data => console.log(data))
```

**Returns**: List of SBOMs
```json
{
  "sboms": [],
  "total": 0
}
```

#### Get SBOM Dashboard
```javascript
// GET /api/v2/sbom/dashboard/summary
fetch('http://localhost:8000/api/v2/sbom/dashboard/summary', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(data => {
  // Use for dashboard widgets
  console.log('Total SBOMs:', data.total_sboms)
  console.log('Total Components:', data.total_components)
  console.log('Vulnerabilities:', data.total_vulnerabilities)
})
```

### 2. Vendor & Equipment APIs

#### List Vendors
```javascript
// GET /api/v2/vendor-equipment/vendors
fetch('http://localhost:8000/api/v2/vendor-equipment/vendors', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(vendors => {
  // Display vendor list
  console.log(vendors)
})
```

#### Search Equipment
```javascript
// GET /api/v2/vendor-equipment/equipment
fetch('http://localhost:8000/api/v2/vendor-equipment/equipment?search=cisco', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(equipment => {
  // Display equipment list
  console.log(equipment)
})
```

#### Get Maintenance Schedule
```javascript
// GET /api/v2/vendor-equipment/maintenance-schedule
fetch('http://localhost:8000/api/v2/vendor-equipment/maintenance-schedule', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(schedule => {
  // Display maintenance calendar
  console.log(schedule)
})
```

#### Predictive Maintenance Forecast
```javascript
// GET /api/v2/vendor-equipment/predictive-maintenance/forecast
fetch('http://localhost:8000/api/v2/vendor-equipment/predictive-maintenance/forecast', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(forecast => {
  // Display maintenance predictions
  console.log('Upcoming maintenance:', forecast)
})
```

### 3. Threat Intelligence APIs

#### Get Threat Dashboard
```javascript
// GET /api/v2/threat-intel/dashboard/summary
fetch('http://localhost:8000/api/v2/threat-intel/dashboard/summary', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(summary => {
  console.log('Active Threats:', summary.active_threats)
  console.log('Active Campaigns:', summary.active_campaigns)
  console.log('High Priority IOCs:', summary.high_priority_iocs)
})
```

#### Get Actors by Sector
```javascript
// GET /api/v2/threat-intel/actors/by-sector/{sector}
const sector = 'energy'
fetch(`http://localhost:8000/api/v2/threat-intel/actors/by-sector/${sector}`, {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(actors => {
  // Display threat actors targeting this sector
  console.log(`Threat actors targeting ${sector}:`, actors)
})
```

#### Search IOCs
```javascript
// GET /api/v2/threat-intel/iocs/search
fetch('http://localhost:8000/api/v2/threat-intel/iocs/search?q=malware', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(iocs => {
  // Display IOC search results
  console.log('IOCs found:', iocs)
})
```

#### Get Active IOCs
```javascript
// GET /api/v2/threat-intel/iocs/active
fetch('http://localhost:8000/api/v2/threat-intel/iocs/active', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(iocs => {
  // Display currently active IOCs
  console.log('Active IOCs:', iocs)
})
```

#### Get IOCs by Type
```javascript
// GET /api/v2/threat-intel/iocs/by-type/{ioc_type}
const iocType = 'domain' // or 'ip', 'hash', 'url'
fetch(`http://localhost:8000/api/v2/threat-intel/iocs/by-type/${iocType}`, {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(iocs => {
  console.log(`${iocType} IOCs:`, iocs)
})
```

#### Get MITRE ATT&CK Coverage
```javascript
// GET /api/v2/threat-intel/mitre/coverage
fetch('http://localhost:8000/api/v2/threat-intel/mitre/coverage', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(coverage => {
  // Display MITRE ATT&CK heatmap
  console.log('MITRE Coverage:', coverage)
})
```

#### Get MITRE ATT&CK Gaps
```javascript
// GET /api/v2/threat-intel/mitre/gaps
fetch('http://localhost:8000/api/v2/threat-intel/mitre/gaps', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(gaps => {
  // Display uncovered MITRE techniques
  console.log('Coverage Gaps:', gaps)
})
```

### 4. Risk Management APIs

#### Get Risk Dashboard
```javascript
// GET /api/v2/risk/dashboard/summary
fetch('http://localhost:8000/api/v2/risk/dashboard/summary', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(summary => {
  console.log('Total Risk Score:', summary.total_risk_score)
  console.log('High Risk Entities:', summary.high_risk_count)
  console.log('Critical Assets:', summary.critical_assets)
})
```

#### Get Risk Matrix
```javascript
// GET /api/v2/risk/dashboard/risk-matrix
fetch('http://localhost:8000/api/v2/risk/dashboard/risk-matrix', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(matrix => {
  // Display risk matrix heatmap
  console.log('Risk Matrix:', matrix)
})
```

#### Get High Risk Entities
```javascript
// GET /api/v2/risk/scores/high-risk
fetch('http://localhost:8000/api/v2/risk/scores/high-risk', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(entities => {
  // Display high-risk entities for priority action
  console.log('High Risk Entities:', entities)
})
```

#### Search Risk Scores
```javascript
// GET /api/v2/risk/scores/search
fetch('http://localhost:8000/api/v2/risk/scores/search?q=critical', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(results => {
  console.log('Search Results:', results)
})
```

#### Get Mission Critical Assets
```javascript
// GET /api/v2/risk/assets/mission-critical
fetch('http://localhost:8000/api/v2/risk/assets/mission-critical', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(assets => {
  // Display mission-critical assets requiring protection
  console.log('Mission Critical:', assets)
})
```

#### Get Asset Criticality Summary
```javascript
// GET /api/v2/risk/assets/criticality/summary
fetch('http://localhost:8000/api/v2/risk/assets/criticality/summary', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(summary => {
  // Display criticality distribution
  console.log('Criticality Breakdown:', summary)
})
```

#### Risk Aggregation by Vendor
```javascript
// GET /api/v2/risk/aggregation/by-vendor
fetch('http://localhost:8000/api/v2/risk/aggregation/by-vendor', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(vendorRisk => {
  // Display vendor risk rankings
  console.log('Risk by Vendor:', vendorRisk)
})
```

#### Risk Aggregation by Sector
```javascript
// GET /api/v2/risk/aggregation/by-sector
fetch('http://localhost:8000/api/v2/risk/aggregation/by-sector', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(sectorRisk => {
  // Display sector risk distribution
  console.log('Risk by Sector:', sectorRisk)
})
```

#### Risk Aggregation by Asset Type
```javascript
// GET /api/v2/risk/aggregation/by-asset-type
fetch('http://localhost:8000/api/v2/risk/aggregation/by-asset-type', {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(assetRisk => {
  // Display asset type risk levels
  console.log('Risk by Asset Type:', assetRisk)
})
```

### 5. Dependency Analysis APIs

#### Get Dependency Tree
```javascript
// GET /api/v2/sbom/components/{component_id}/dependencies
const componentId = 'comp_123'
fetch(`http://localhost:8000/api/v2/sbom/components/${componentId}/dependencies`, {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(tree => {
  // Display dependency tree visualization
  console.log('Dependencies:', tree)
})
```

#### Get Impact Analysis
```javascript
// GET /api/v2/sbom/components/{component_id}/impact
const componentId = 'comp_123'
fetch(`http://localhost:8000/api/v2/sbom/components/${componentId}/impact`, {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(impact => {
  // Show blast radius if component is compromised
  console.log('Impact if compromised:', impact)
})
```

#### Detect Cycles
```javascript
// GET /api/v2/sbom/sboms/{sbom_id}/cycles
const sbomId = 'sbom_123'
fetch(`http://localhost:8000/api/v2/sbom/sboms/${sbomId}/cycles`, {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(cycles => {
  // Display circular dependency warnings
  console.log('Circular Dependencies:', cycles)
})
```

#### Get Graph Statistics
```javascript
// GET /api/v2/sbom/sboms/{sbom_id}/graph-stats
const sbomId = 'sbom_123'
fetch(`http://localhost:8000/api/v2/sbom/sboms/${sbomId}/graph-stats`, {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(stats => {
  // Display graph complexity metrics
  console.log('Graph Stats:', stats)
  console.log('Total Nodes:', stats.nodes)
  console.log('Total Edges:', stats.edges)
  console.log('Avg Depth:', stats.avg_depth)
})
```

#### Get Vulnerable Paths
```javascript
// GET /api/v2/sbom/sboms/{sbom_id}/vulnerable-paths
const sbomId = 'sbom_123'
fetch(`http://localhost:8000/api/v2/sbom/sboms/${sbomId}/vulnerable-paths`, {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(paths => {
  // Display paths leading to vulnerabilities
  console.log('Vulnerable Paths:', paths)
})
```

#### Get Remediation Report
```javascript
// GET /api/v2/sbom/sboms/{sbom_id}/remediation
const sbomId = 'sbom_123'
fetch(`http://localhost:8000/api/v2/sbom/sboms/${sbomId}/remediation`, {
  headers: { 'x-customer-id': 'dev' }
})
.then(res => res.json())
.then(report => {
  // Display remediation recommendations
  console.log('Remediation Plan:', report)
})
```

---

## APIS REQUIRING DATA (POST/PUT)

### Create SBOM
```javascript
// POST /api/v2/sbom/sboms
fetch('http://localhost:8000/api/v2/sbom/sboms', {
  method: 'POST',
  headers: {
    'x-customer-id': 'dev',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'My Application SBOM',
    version: '1.0.0',
    description: 'SBOM for production app'
  })
})
.then(res => res.json())
.then(sbom => console.log('Created SBOM:', sbom))
```

### Create Vendor
```javascript
// POST /api/v2/vendor-equipment/vendors
fetch('http://localhost:8000/api/v2/vendor-equipment/vendors', {
  method: 'POST',
  headers: {
    'x-customer-id': 'dev',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'Cisco Systems',
    website: 'https://cisco.com',
    contact_email: 'support@cisco.com'
  })
})
.then(res => res.json())
.then(vendor => console.log('Created Vendor:', vendor))
```

### Create Threat Actor
```javascript
// POST /api/v2/threat-intel/actors
fetch('http://localhost:8000/api/v2/threat-intel/actors', {
  method: 'POST',
  headers: {
    'x-customer-id': 'dev',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'APT29',
    description: 'Russian state-sponsored threat group',
    sectors: ['government', 'energy'],
    active: true
  })
})
.then(res => res.json())
.then(actor => console.log('Created Actor:', actor))
```

### Create IOC
```javascript
// POST /api/v2/threat-intel/iocs
fetch('http://localhost:8000/api/v2/threat-intel/iocs', {
  method: 'POST',
  headers: {
    'x-customer-id': 'dev',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    type: 'domain',
    value: 'malicious.example.com',
    confidence: 'high',
    tags: ['malware', 'c2']
  })
})
.then(res => res.json())
.then(ioc => console.log('Created IOC:', ioc))
```

---

## APIS WITH KNOWN ISSUES

### ❌ AEON-SAAS-DEV APIs (Port 3000)
**Status**: ALL FAILING (40 APIs)
**Issue**: Server errors - likely database connection problem
**Action**: Do NOT use these APIs yet - wait for fix

### ❌ Remediation APIs
**Status**: ALL FAILING (27 APIs)
**Issue**: Internal server errors
**Endpoints**: All `/api/v2/remediation/*` endpoints
**Action**: Skip remediation features in UI for now

### ⚠️ APIs Requiring WRITE Access
```javascript
// Needs x-access-level: WRITE header
fetch('http://localhost:8000/api/v2/sbom/sboms/123', {
  method: 'DELETE',
  headers: {
    'x-customer-id': 'dev',
    'x-access-level': 'WRITE'  // Required for write operations
  }
})
```

---

## COMPLETE WORKING API LIST

See `DEFINITIVE_API_AUDIT_2025-12-12.md` for:
- All 181 APIs with pass/fail status
- Exact HTTP codes and response times
- Detailed failure reasons
- curl examples for every endpoint

---

## ERROR HANDLING

### Standard Error Response
```javascript
fetch('http://localhost:8000/api/endpoint')
.then(res => {
  if (!res.ok) {
    // Handle HTTP errors
    if (res.status === 404) console.log('No data found')
    if (res.status === 422) console.log('Invalid request data')
    if (res.status === 500) console.log('Server error')
    if (res.status === 403) console.log('Insufficient permissions')
  }
  return res.json()
})
.then(data => console.log(data))
.catch(err => console.error('Network error:', err))
```

### Common Status Codes
- **200**: Success
- **404**: No data found
- **422**: Validation error (missing data in request)
- **403**: Forbidden (needs WRITE access)
- **500**: Server error (API broken - report to backend team)

---

## NEXT STEPS

1. **Use Working APIs** (36 total) for initial UI development
2. **Mock Failing APIs** (145 total) with placeholder data
3. **Report Issues** for 500 errors to backend team
4. **Test Connection** with health check endpoints first

---

*For complete API status, see: DEFINITIVE_API_AUDIT_2025-12-12.md*
*For system access details, see: SYSTEM_ACCESS.md*
