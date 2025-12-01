---
title: NeoCoder Integration (Part 2 of 2)
category: 05_Tools_Reference
last_updated: 2025-10-25
line_count: 69
status: published
tags: [neocoder, mcp, documentation]
---

## Step 3: Environment Configuration

### AgentZero Environment Variables

Add to `agent-zero/.env` or `docker-compose.yml`:

```bash
# NeoCoder Integration
NEOCODER_API_URL=http://neocoder:8002
NEOCODER_TIMEOUT=30
NEOCODER_RETRY_ATTEMPTS=3

# Optional: Enable NVD tools by default
ENABLE_NEOCODER_NVD=true
```

### NeoCoder Environment Variables

Ensure NeoCoder has API key configured (already done):

```bash
# In neocoder/.env or docker-compose.yml
NVD_API_KEY=919ecb88-4e30-4f58-baeb-67c868314307
```

---

## Step 4: Verification & Testing

### Test 1: Health Check

```bash
# From host machine
curl http://localhost:8002/health

# From AgentZero container
docker exec agent-zero curl http://neocoder:8002/health
```

**Expected:** `{"status": "healthy", ...}`

### Test 2: Live CVE Lookup Tool

In AgentZero chat interface:

```
Agent: "Look up CVE-2021-44228 using NVD"
```

**Expected:** AgentZero uses `NVDLiveLookup` tool and returns CVE details

### Test 3: Gap Analysis Tool

```
Agent: "Check what CVEs are missing from 2021"
```

**Expected:** AgentZero uses `NVDGapAnalysis` tool and reports gap statistics

### Test 4: Delta Monitoring Tool

```
Agent: "Check for new CVEs in the last 24 hours"
```

**Expected:** AgentZero uses `NVDDeltaCheck` tool and reports new/modified CVEs

---
