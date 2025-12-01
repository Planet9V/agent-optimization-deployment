# GAP-ML-005 Quick Start Guide

**Status:** ✅ READY TO USE
**Time to Run:** 5 minutes

## Prerequisites

- Neo4j 5.x running at `bolt://aeon-neo4j-dev:7687`
- APOC plugin installed
- Node.js 18+ installed

## Step 1: Install (2 minutes)

```bash
cd /home/jim/2_OXOT_Projects_Dev/src/ews-streaming
npm install
```

## Step 2: Test Existing Queries (1 minute)

```bash
npm run test:neo4j
```

Expected output:
```
✓ psychohistory.criticalSlowingFromTimeSeries exists
✓ Test actors created
✓ EWS threshold query returns results
```

## Step 3: Install Triggers (30 seconds)

```bash
npm run install:triggers
```

Expected output:
```
✓ APOC trigger 'ewsThresholdBreachTrigger' added
✓ Periodic scan 'ewsPeriodicScan' scheduled
```

## Step 4: Start Server (30 seconds)

```bash
npm run dev
```

Expected output:
```
✅ Neo4j connection successful
🚀 EWS Streaming Server running on port 3001
📡 WebSocket endpoint: ws://localhost:3001/ews/stream
🔗 REST API: http://localhost:3001/api/v1/ews
🔄 Started alert polling (every 5000ms)
```

## Step 5: Test Integration (1 minute)

Open new terminal:

```bash
cd /home/jim/2_OXOT_Projects_Dev/src/ews-streaming
npm test
```

Expected output:
```
✅ ALL TESTS PASSED (10/10)
```

## Step 6: Connect Client

```javascript
// JavaScript client
import io from 'socket.io-client';

// 1. Get auth token
const res = await fetch('http://localhost:3001/api/v1/ews/subscribe', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    channels: ['ews:*'],
    filters: {severity: ['CRITICAL', 'HIGH']}
  })
});

const {auth_token, websocket_url} = await res.json();

// 2. Connect
const socket = io(websocket_url, {auth: {token: auth_token}});

// 3. Listen for alerts
socket.on('ews_alert', (alert) => {
  console.log('🚨 EWS Alert:', alert.severity, alert.entity_id);
});
```

## Trigger Test Alert

```bash
cypher-shell -a bolt://aeon-neo4j-dev:7687 -u neo4j -p neo4j@openspg << 'CYPHER'
MERGE (a:Actor {id: 'QUICKSTART-TEST'})
SET a.name = 'Quick Start Test',
    a.ews_variance = 0.95,
    a.ews_autocorrelation = 0.92,
    a.ews_critical_distance = 0.08,
    a.last_updated = datetime()
CYPHER
```

**Expected:** Client receives alert within 5 seconds

## Verify Alert Received

```bash
curl http://localhost:3001/api/v1/ews/history?entity_id=QUICKSTART-TEST
```

## Troubleshooting

### "APOC functions not found"
```bash
# Check APOC installation
cypher-shell -a bolt://aeon-neo4j-dev:7687 -u neo4j -p neo4j@openspg \
  "CALL apoc.help('psychohistory') YIELD name RETURN name"
```

If empty, install APOC:
1. Download APOC plugin for Neo4j 5.x
2. Place in `$NEO4J_HOME/plugins/`
3. Restart Neo4j
4. Re-run step 2

### "Connection refused"
```bash
# Check Neo4j is running
cypher-shell -a bolt://aeon-neo4j-dev:7687 -u neo4j -p neo4j@openspg \
  "RETURN 1 AS test"
```

### "No alerts received"
```bash
# Check alerts exist in database
cypher-shell -a bolt://aeon-neo4j-dev:7687 -u neo4j -p neo4j@openspg \
  "MATCH (ea:EWSAlert) RETURN count(ea) AS alert_count"
```

## Next Steps

1. Configure production environment variables
2. Set up PagerDuty integration
3. Add Slack notifications
4. Deploy to production

## Documentation

- Full README: `README.md`
- Implementation Report: `/docs/GAP-ML-005_IMPLEMENTATION_REPORT.md`
- Gap Case: `1_AEON_DT_CyberSecurity_Wiki_Current/08_GAP_CASES/02_GAP-ML-005_WEBSOCKET_EWS.md`

---

**Questions?** Check `README.md` or implementation report for detailed documentation.
