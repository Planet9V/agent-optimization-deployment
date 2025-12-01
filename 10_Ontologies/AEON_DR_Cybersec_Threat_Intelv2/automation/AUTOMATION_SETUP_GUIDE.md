# NVD Daily Update Automation - Setup Guide

**File**: AUTOMATION_SETUP_GUIDE.md
**Created**: 2025-11-01
**Version**: 1.0.0
**Author**: Automation Agent
**Purpose**: Complete setup documentation for NVD daily sync automation
**Status**: ACTIVE

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Cron Setup](#cron-setup)
7. [Monitoring](#monitoring)
8. [Troubleshooting](#troubleshooting)
9. [Metrics & Performance](#metrics--performance)

---

## Overview

This automation system provides daily incremental updates of CVE data from the NVD (National Vulnerability Database) API v2.0, with automatic enrichment from EPSS, CISA KEV, and VulnCheck XDB sources.

### Key Features

- **Incremental Sync**: Only processes CVEs modified in the last 24 hours
- **Rate Limiting**: NVD API v2.0 compliant (50 req/30s with key, 5 req/30s without)
- **Automatic Enrichment**: EPSS scores, KEV flags, exploit code linking
- **Priority Framework**: NOW/NEXT/NEVER classification
- **Robust Error Handling**: Retry logic and comprehensive logging
- **Cron-Ready**: Shell wrapper for scheduled execution

### Daily Workflow

```
┌─────────────────┐
│  Daily Cron Job │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ 1. NVD Daily Sync   │  Fetch CVEs modified in last 24 hours
│    (nvd_daily_sync) │  Insert/update in Neo4j
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 2. Enrichment       │  EPSS scores (FIRST.org)
│    Pipeline         │  KEV flags (CISA)
│ (enrichment_pipeline)│  XDB exploits (VulnCheck)
└────────┬────────────┘  Priority calculation
         │
         ▼
┌─────────────────────┐
│ 3. Metrics & Logs   │  Log processing results
│                     │  Send notifications (optional)
└─────────────────────┘
```

---

## Architecture

### Component Overview

| Component | File | Purpose |
|-----------|------|---------|
| **NVD Sync** | `nvd_daily_sync.py` | Fetches CVEs from NVD API v2.0, upserts to Neo4j |
| **Enrichment Pipeline** | `enrichment_pipeline.py` | Enriches CVEs with EPSS, KEV, XDB, priority tier |
| **Cron Wrapper** | `daily_sync.sh` | Shell script for scheduled execution |
| **Configuration** | `config.yaml` | Centralized configuration (DB, API keys, thresholds) |
| **Dependencies** | `requirements.txt` | Python package dependencies |

### Data Flow

```
NVD API v2.0 ──→ nvd_daily_sync.py ──→ Neo4j (CVE nodes)
                                              │
                                              ▼
FIRST EPSS API ──┐                    enrichment_pipeline.py
CISA KEV Catalog ─┼──→ enrichment ──→ Neo4j (property updates)
VulnCheck XDB ────┘    pipeline
```

---

## Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu/Debian/RHEL/CentOS) or macOS
- **Python**: 3.8 or higher
- **Neo4j**: 5.x or higher (with APOC plugin recommended)
- **Disk Space**: ~500 MB for logs and temporary data
- **Network**: Outbound HTTPS access to NVD, FIRST.org, CISA, VulnCheck APIs

### Required Services

1. **Neo4j Database**
   - Running and accessible on configured URI (default: `bolt://localhost:7687`)
   - Recommendation 1 schema deployed (EPSS, KEV, priority properties)
   - User credentials with read/write permissions

2. **API Keys** (Optional but Recommended)
   - **NVD API Key**: [Request here](https://nvd.nist.gov/developers/request-an-api-key)
     - Increases rate limit from 5 to 50 requests per 30 seconds
   - **VulnCheck API Token**: [Sign up here](https://vulncheck.com)
     - Enables XDB exploit code enrichment

### Schema Prerequisites

**Critical**: Recommendation 1 schema MUST be deployed before running automation.

Run the following Cypher migration from `SCHEMA_CHANGE_SPECIFICATIONS.md`:

```cypher
// Add EPSS properties
MATCH (cve:CVE)
SET cve.epss_score = null,
    cve.epss_percentile = null,
    cve.epss_date = null,
    cve.epss_last_updated = null;

// Add KEV properties
MATCH (cve:CVE)
SET cve.in_cisa_kev = false,
    cve.in_vulncheck_kev = false,
    cve.kev_date_added = null,
    cve.exploited_in_wild = false,
    cve.kev_last_updated = null;

// Add Priority properties
MATCH (cve:CVE)
SET cve.priority_tier = null,
    cve.priority_score = null,
    cve.priority_calculated_at = null;

// Create indexes
CREATE INDEX cve_epss_score IF NOT EXISTS
FOR (c:CVE) ON (c.epss_score);

CREATE INDEX cve_in_cisa_kev IF NOT EXISTS
FOR (c:CVE) ON (c.in_cisa_kev);

CREATE INDEX cve_priority_tier IF NOT EXISTS
FOR (c:CVE) ON (c.priority_tier);
```

---

## Installation

### Step 1: Clone/Download Automation Scripts

```bash
# Navigate to project directory
cd /home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DR_Cybersec_Threat_Intelv2/automation

# Verify files exist
ls -l
# Expected output:
# nvd_daily_sync.py
# enrichment_pipeline.py
# daily_sync.sh
# config.yaml
# requirements.txt
# AUTOMATION_SETUP_GUIDE.md
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Step 3: Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python3 -c "import requests, neo4j, yaml; print('Dependencies installed successfully')"
```

### Step 4: Create Log Directory

```bash
# Create logs directory
mkdir -p logs

# Set permissions (if needed)
chmod 755 logs
```

### Step 5: Make Shell Script Executable

```bash
# Make daily_sync.sh executable
chmod +x daily_sync.sh
```

---

## Configuration

### Step 1: Edit `config.yaml`

```bash
# Open configuration file
nano config.yaml  # or vim, vi, etc.
```

### Step 2: Configure Neo4j Connection

```yaml
neo4j:
  uri: "bolt://localhost:7687"  # Change if Neo4j is on different host
  user: "neo4j"                 # Neo4j username
  password: "YOUR_NEO4J_PASSWORD"  # **CHANGE THIS**
  database: "neo4j"             # Database name
```

**Security Note**: Protect `config.yaml` from unauthorized access:
```bash
chmod 600 config.yaml
```

### Step 3: Configure API Keys

**Option A: Environment Variables (Recommended)**

```bash
# Add to ~/.bashrc or ~/.bash_profile
export NVD_API_KEY="your-nvd-api-key-here"
export VULNCHECK_API_TOKEN="your-vulncheck-token-here"

# Reload environment
source ~/.bashrc
```

**Option B: Direct Configuration**

Edit `config.yaml`:
```yaml
nvd_api_key: "your-nvd-api-key-here"
vulncheck_api_token: "your-vulncheck-token-here"
```

### Step 4: Test Configuration

```bash
# Test NVD sync (dry run)
python3 nvd_daily_sync.py --config config.yaml --hours 1

# Check logs
tail -f logs/nvd_sync.log
```

Expected output:
```
[INFO] Fetching CVEs modified between 2025-11-01T00:00:00 and 2025-11-01T01:00:00
[INFO] Fetched X CVEs (total: X)
[INFO] Total CVEs fetched from NVD: X
[INFO] CVEs created: X
[INFO] CVEs updated: X
```

---

## Cron Setup

### Recommended Cron Schedule

Run daily at 2:00 AM local time (low-traffic hours):

```bash
# Open crontab editor
crontab -e

# Add the following line (adjust path as needed)
0 2 * * * /home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DR_Cybersec_Threat_Intelv2/automation/daily_sync.sh >> /var/log/nvd_sync_cron.log 2>&1
```

### Alternative Schedules

```bash
# Every 12 hours (2 AM and 2 PM)
0 2,14 * * * /path/to/daily_sync.sh >> /var/log/nvd_sync_cron.log 2>&1

# Every 6 hours
0 */6 * * * /path/to/daily_sync.sh >> /var/log/nvd_sync_cron.log 2>&1

# Weekly (Sunday 2 AM)
0 2 * * 0 /path/to/daily_sync.sh >> /var/log/nvd_sync_cron.log 2>&1
```

### Verify Cron Job

```bash
# List current cron jobs
crontab -l

# Check cron service status
systemctl status cron  # or crond on RHEL/CentOS
```

### Environment Variables in Cron

If using environment variables for API keys, add to crontab:

```bash
# Edit crontab
crontab -e

# Add environment variables at the top
NVD_API_KEY=your-nvd-api-key-here
VULNCHECK_API_TOKEN=your-vulncheck-token-here

# Then add cron schedule
0 2 * * * /path/to/daily_sync.sh >> /var/log/nvd_sync_cron.log 2>&1
```

### Manual Execution (Testing)

```bash
# Run sync manually
./daily_sync.sh

# Check output
tail -f logs/cron_*.log
```

---

## Monitoring

### Log Files

| Log File | Purpose | Location |
|----------|---------|----------|
| **NVD Sync Log** | NVD API requests and CVE upserts | `logs/nvd_sync_YYYYMMDD_HHMMSS.log` |
| **Enrichment Log** | EPSS, KEV, XDB enrichment | `logs/enrichment_YYYYMMDD_HHMMSS.log` |
| **Cron Log** | Shell wrapper execution | `logs/cron_YYYYMMDD_HHMMSS.log` |
| **Cron Output** | Cron job stdout/stderr | `/var/log/nvd_sync_cron.log` |

### Monitoring Commands

```bash
# View latest sync log
tail -f logs/nvd_sync_$(ls -t logs/nvd_sync_*.log | head -1)

# View latest enrichment log
tail -f logs/enrichment_$(ls -t logs/enrichment_*.log | head -1)

# Check cron execution history
grep "NVD Daily Sync" /var/log/nvd_sync_cron.log

# Monitor Neo4j query performance
# (Run in Neo4j Browser or cypher-shell)
CALL dbms.listQueries();
```

### Key Metrics to Monitor

**NVD Sync Metrics**:
- `cves_fetched`: Number of CVEs returned by NVD API
- `cves_created`: New CVE nodes inserted
- `cves_updated`: Existing CVE nodes updated
- `api_calls`: Total NVD API requests
- `errors`: Failed operations count
- `duration`: Total execution time (seconds)

**Enrichment Metrics**:
- `epss_enriched`: CVEs updated with EPSS scores
- `kev_flagged`: CVEs marked as in CISA KEV
- `exploits_linked`: CVEs linked to ExploitCode nodes (if XDB enabled)
- `priority_calculated`: CVEs with updated priority tiers
- `errors`: Failed enrichment operations

### Expected Daily Execution Time

| Component | Estimated Time | Notes |
|-----------|----------------|-------|
| **NVD Sync** | 1-5 minutes | ~50-200 CVEs modified per day |
| **EPSS Enrichment** | 1-2 minutes | Batch API requests |
| **KEV Enrichment** | 10-30 seconds | Single CISA catalog fetch |
| **Priority Calculation** | 30-60 seconds | Database queries |
| **Total** | **3-8 minutes** | Varies by daily CVE volume |

### Health Check Query

Run daily to verify automation health:

```cypher
// Check recent CVE updates
MATCH (cve:CVE)
WHERE cve.updated_at >= datetime() - duration({days: 1})
RETURN count(*) AS cves_updated_last_24h;

// Check EPSS coverage
MATCH (cve:CVE)
RETURN count(*) AS total_cves,
       sum(CASE WHEN cve.epss_score IS NOT NULL THEN 1 ELSE 0 END) AS epss_enriched,
       toFloat(sum(CASE WHEN cve.epss_score IS NOT NULL THEN 1 ELSE 0 END)) / count(*) * 100 AS epss_coverage_pct;

// Check priority distribution
MATCH (cve:CVE)
WHERE cve.priority_tier IS NOT NULL
RETURN cve.priority_tier AS tier, count(*) AS count
ORDER BY tier;
```

---

## Troubleshooting

### Common Issues

#### Issue 1: "NVD API request failed"

**Symptoms**:
```
[ERROR] NVD API request failed: HTTPError: 403 Forbidden
```

**Causes**:
- Invalid or expired NVD API key
- Rate limit exceeded (5 requests/30s without key)

**Solutions**:
1. Verify API key: `echo $NVD_API_KEY`
2. Request new API key from NVD
3. Reduce sync frequency to avoid rate limits
4. Check NVD API status: https://nvd.nist.gov/general/news

#### Issue 2: "Neo4j connection failed"

**Symptoms**:
```
[ERROR] Failed to connect to Neo4j: ServiceUnavailable
```

**Causes**:
- Neo4j service not running
- Incorrect URI in `config.yaml`
- Authentication failure

**Solutions**:
```bash
# Check Neo4j status
systemctl status neo4j

# Verify connection manually
cypher-shell -a bolt://localhost:7687 -u neo4j -p YOUR_PASSWORD

# Check Neo4j logs
tail -f /var/log/neo4j/neo4j.log
```

#### Issue 3: "EPSS API request failed"

**Symptoms**:
```
[ERROR] EPSS API request failed: ConnectionError
```

**Causes**:
- Network connectivity issues
- FIRST.org API outage

**Solutions**:
1. Test network connectivity: `curl https://api.first.org/data/v1/epss`
2. Check FIRST.org status page
3. Verify firewall/proxy settings
4. Retry after timeout

#### Issue 4: "Schema properties not found"

**Symptoms**:
```
[ERROR] Property 'epss_score' not found on CVE node
```

**Causes**:
- Recommendation 1 schema not deployed

**Solutions**:
1. Deploy schema migration from `SCHEMA_CHANGE_SPECIFICATIONS.md`
2. Verify properties exist:
   ```cypher
   MATCH (cve:CVE) RETURN keys(cve) LIMIT 1;
   ```

#### Issue 5: "Cron job not running"

**Symptoms**:
- No logs generated at scheduled time

**Causes**:
- Cron service not running
- Incorrect crontab syntax
- Missing environment variables

**Solutions**:
```bash
# Check cron service
systemctl status cron

# Verify crontab syntax
crontab -l

# Check cron logs
grep CRON /var/log/syslog  # Ubuntu/Debian
grep CRON /var/log/cron    # RHEL/CentOS

# Test manual execution
./daily_sync.sh
```

### Debug Mode

Enable debug logging for detailed troubleshooting:

Edit `config.yaml`:
```yaml
log_level: "DEBUG"  # Change from INFO to DEBUG
```

Run sync manually:
```bash
./daily_sync.sh
```

Check debug logs:
```bash
tail -f logs/nvd_sync_*.log | grep DEBUG
```

### Validation Checklist

After setup, verify all components:

- [ ] Neo4j connection successful
- [ ] NVD API key valid (check rate limit in logs)
- [ ] EPSS API accessible
- [ ] CISA KEV catalog fetch successful
- [ ] VulnCheck XDB token valid (if configured)
- [ ] Schema properties exist on CVE nodes
- [ ] Indexes created and online
- [ ] Cron job scheduled correctly
- [ ] Logs directory writable
- [ ] Manual execution succeeds
- [ ] Metrics show expected values

---

## Metrics & Performance

### Expected Metrics (Daily Execution)

Based on typical NVD activity:

| Metric | Expected Value | Notes |
|--------|----------------|-------|
| **CVEs Modified (24h)** | 50-200 | NVD updates ~100-150 CVEs daily on average |
| **CVEs Created** | 5-20 | New CVEs published daily |
| **CVEs Updated** | 45-180 | Existing CVE modifications |
| **EPSS Enriched** | 50-200 | All modified CVEs get EPSS scores |
| **KEV Flagged** | 0-5 | CISA adds ~1-3 CVEs to KEV weekly |
| **Priority NOW** | 1-10 | High-severity actively exploited |
| **Priority NEXT** | 10-50 | Moderate-high risk |
| **Priority NEVER** | 40-140 | Low risk |
| **API Calls (NVD)** | 1-5 | Batched at 2000 results per request |
| **API Calls (EPSS)** | 1-3 | Batched at 100 CVEs per request |
| **Duration** | 3-8 minutes | End-to-end execution time |

### Performance Baselines

**NVD API Performance**:
- With API key: 50 requests/30s = ~10,000 CVEs/minute theoretical max
- Without API key: 5 requests/30s = ~1,000 CVEs/minute theoretical max
- Actual throughput: Limited by network latency (~500-1000 CVEs/minute)

**Neo4j Write Performance**:
- Single CVE upsert: ~5-10ms
- Batch upsert (1000 CVEs): ~3-5 seconds
- EPSS update batch (1000 CVEs): ~2-3 seconds

**Total Pipeline Efficiency**:
- For 100 CVEs: ~3-4 minutes
- For 500 CVEs: ~6-8 minutes
- For 1000 CVEs: ~10-15 minutes

### Performance Tuning

**Increase NVD Batch Size** (if rate limits allow):
```yaml
sync:
  batch_size: 2000  # Max allowed by NVD API
```

**Optimize Neo4j Batch Updates**:
```yaml
performance:
  neo4j_batch_size: 1000  # Balance between memory and speed
```

**Parallel Enrichment** (future enhancement):
```python
# Use ThreadPoolExecutor for parallel EPSS API calls
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(fetch_epss_batch, batch) for batch in batches]
```

### Scaling Considerations

**Daily CVE Volume Growth**:
- Current: ~150 CVEs/day average
- Expected 2025: ~200-250 CVEs/day
- System handles up to 2000 CVEs/day without modification

**Database Growth**:
- Property additions per CVE: ~191 bytes (Recommendation 1)
- Daily storage increase: ~30-40 KB (150 CVEs × 191 bytes)
- Annual storage increase: ~11-15 MB for properties only

**Resource Requirements**:
- CPU: Minimal (~5-10% during execution)
- Memory: ~100-200 MB Python process
- Network: ~1-5 MB/day data transfer
- Disk I/O: ~10-20 MB/day log files

---

## Notifications (Optional)

### Email Notifications

Configure SMTP in `config.yaml`:

```yaml
notifications:
  email:
    enabled: true
    smtp_host: "smtp.gmail.com"
    smtp_port: 587
    smtp_user: "your-email@gmail.com"
    smtp_password: "your-app-password"
    from_address: "nvd-sync@yourdomain.com"
    to_addresses:
      - "admin@yourdomain.com"
```

**Gmail App Password**: [Create here](https://support.google.com/accounts/answer/185833)

### Slack Notifications

Configure webhook in `config.yaml`:

```yaml
notifications:
  slack:
    enabled: true
    webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

**Create Slack Webhook**: [Instructions](https://api.slack.com/messaging/webhooks)

### Notification Content

**Success Notification**:
```
Subject: NVD Daily Sync Successful

Daily sync and enrichment completed successfully.

Metrics:
- CVEs fetched: 142
- CVEs created: 12
- CVEs updated: 130
- EPSS enriched: 142
- KEV flagged: 2
- Priority calculated: 142
- Duration: 4.2 minutes

See logs for details.
```

**Failure Notification**:
```
Subject: NVD Daily Sync Failed

Sync failed with errors. Check logs immediately.

Last 50 log lines:
[ERROR] NVD API request failed: HTTPError 503
[ERROR] Retrying in 5 seconds...
...
```

---

## Maintenance

### Regular Maintenance Tasks

**Weekly**:
- Review log files for errors
- Verify EPSS coverage remains >95%
- Check Neo4j index health

**Monthly**:
- Audit CVE priority distribution
- Review API usage and costs (if applicable)
- Update Python dependencies

**Quarterly**:
- Full schema validation
- Performance baseline comparison
- Security audit (API keys, credentials)

### Log Rotation

Logs are automatically cleaned up after 30 days by `daily_sync.sh`:

```bash
# Manual cleanup if needed
find logs/ -name "*.log" -type f -mtime +30 -delete
```

### Backup Strategy

**Configuration Backup**:
```bash
# Backup config.yaml
cp config.yaml config.yaml.backup.$(date +%Y%m%d)
```

**Database Backup** (before major changes):
```bash
# Neo4j backup
neo4j-admin dump --database=neo4j --to=/backups/neo4j-$(date +%Y%m%d).dump
```

---

## Support & Resources

### Documentation References

- **NVD API v2.0**: https://nvd.nist.gov/developers/vulnerabilities
- **FIRST EPSS API**: https://www.first.org/epss/api
- **CISA KEV Catalog**: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- **VulnCheck API**: https://docs.vulncheck.com
- **Neo4j Python Driver**: https://neo4j.com/docs/api/python-driver/current/

### Contact Information

For issues or questions:
1. Check `SCHEMA_CHANGE_SPECIFICATIONS.md` for schema details
2. Review logs in `logs/` directory
3. Consult Neo4j query performance with `PROFILE` or `EXPLAIN`

---

## Appendix: Quick Reference

### Common Commands

```bash
# Manual sync (test run)
python3 nvd_daily_sync.py --config config.yaml --hours 24

# Manual enrichment
python3 enrichment_pipeline.py --config config.yaml --limit 100

# Full pipeline
./daily_sync.sh

# Check latest logs
tail -f logs/nvd_sync_*.log
tail -f logs/enrichment_*.log

# Monitor cron execution
tail -f /var/log/nvd_sync_cron.log

# Neo4j health check
cypher-shell "MATCH (cve:CVE) WHERE cve.updated_at >= datetime() - duration({days: 1}) RETURN count(*)"
```

### File Locations

```
automation/
├── nvd_daily_sync.py         # Main NVD sync script
├── enrichment_pipeline.py    # Enrichment orchestrator
├── daily_sync.sh             # Cron wrapper
├── config.yaml               # Configuration
├── requirements.txt          # Python dependencies
├── AUTOMATION_SETUP_GUIDE.md # This file
└── logs/                     # Log directory (auto-created)
    ├── nvd_sync_*.log
    ├── enrichment_*.log
    └── cron_*.log
```

---

**Document Status**: Ready for Production
**Next Steps**: Deploy schema (Recommendation 1), configure `config.yaml`, test manual execution, schedule cron job

