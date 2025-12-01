# NVD CVE Import Guide - 2018-2019

## Overview
This script imports approximately 35,000-40,000 CVEs from the NVD API v2.0 for the years 2018-2019 into Neo4j.

## Features
- ✅ NVD API v2.0 compliance
- ✅ Automatic rate limiting (5 requests per 30 seconds)
- ✅ Progress tracking and resumability
- ✅ MERGE logic to prevent duplicates
- ✅ CVE→CWE relationship creation
- ✅ Error handling and retry logic
- ✅ Comprehensive logging
- ✅ Monthly chunking for manageable batches

## Prerequisites

### 1. Install Dependencies
```bash
cd /home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Verify Neo4j Connection
```bash
python check_neo4j_status.py
```

Expected output:
```
Documents: X
Entities: X
Metadata: X
Relationships: X
```

## Usage

### Basic Import
```bash
./import_nvd_2018_2019.py
```

### Using Python Directly
```bash
python import_nvd_2018_2019.py
```

### Background Execution (Recommended)
```bash
nohup python import_nvd_2018_2019.py > nvd_import.out 2>&1 &
```

Monitor progress:
```bash
tail -f nvd_import_2018_2019.log
```

## Import Process

### Timeline Estimate
- **Rate limit**: 5 requests per 30 seconds = 10 requests per minute
- **Expected CVEs**: ~35,000-40,000
- **CVEs per request**: Up to 2,000
- **Estimated requests**: ~20-25 requests
- **Total time**: 2-5 minutes (excluding network delays)

### Progress Tracking
The script saves progress to `.nvd_import_progress.json`:
```json
{
  "last_processed_date": "2019-03-15T23:59:59.999",
  "total_processed": 15420,
  "last_update": "2025-10-29T16:00:00",
  "session_stats": {
    "cves_processed": 15420,
    "cves_created": 15420,
    "cwes_linked": 18652,
    "errors": 0
  }
}
```

### Resume After Interruption
If the script is interrupted, simply run it again. It will automatically resume from the last processed date.

## Data Schema

### CVE Node Properties
```cypher
(:CVE {
  cve_id: "CVE-2018-0001",
  cvss_score: 7.5,
  cvss_vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
  cvss_version: "3.1",
  severity: "HIGH",
  description: "Buffer overflow vulnerability...",
  published_date: "2018-01-15T00:00:00.000",
  modified_date: "2018-02-20T12:30:00.000",
  cwe_ids: ["CWE-119", "CWE-120"],
  last_updated: datetime()
})
```

### CWE Node Properties
```cypher
(:CWE {
  cwe_id: "CWE-119"
})
```

### Relationships
```cypher
(:CVE)-[:EXPLOITS_WEAKNESS {discovered: datetime()}]->(:CWE)
```

## Verification Queries

### Check Import Progress
```cypher
// Count CVEs by year
MATCH (c:CVE)
WHERE c.published_date STARTS WITH '2018' OR c.published_date STARTS WITH '2019'
WITH substring(c.published_date, 0, 4) as year, count(c) as count
RETURN year, count
ORDER BY year
```

### Check Severity Distribution
```cypher
MATCH (c:CVE)
WHERE c.published_date >= '2018-01-01' AND c.published_date < '2020-01-01'
RETURN c.severity, count(*) as count
ORDER BY count DESC
```

### Check CWE Relationships
```cypher
MATCH (c:CVE)-[r:EXPLOITS_WEAKNESS]->(w:CWE)
WHERE c.published_date >= '2018-01-01' AND c.published_date < '2020-01-01'
RETURN w.cwe_id, count(c) as cve_count
ORDER BY cve_count DESC
LIMIT 20
```

### Find High Severity CVEs
```cypher
MATCH (c:CVE)
WHERE c.published_date >= '2018-01-01' AND c.published_date < '2020-01-01'
  AND c.severity IN ['CRITICAL', 'HIGH']
RETURN c.cve_id, c.cvss_score, c.severity, c.published_date
ORDER BY c.cvss_score DESC
LIMIT 50
```

## Performance Optimization

### Indexes Created
The script automatically creates these indexes:
- `cve_id` (unique constraint)
- `published_date` (index)
- `severity` (index)
- `cvss_score` (index)
- `cwe_id` (unique constraint)

### Batch Processing
- Monthly chunks (12 months × 2 years = 24 batches)
- Up to 2,000 CVEs per API request
- MERGE operations to prevent duplicates

## Troubleshooting

### Rate Limit Errors (403)
```
WARNING: Rate limit hit (403), waiting longer...
```
**Solution**: The script automatically increases wait time. No action needed.

### Service Unavailable (503)
```
WARNING: Service unavailable (503), retrying...
```
**Solution**: The script automatically retries. If persistent, wait a few minutes and restart.

### Connection Errors
```
ERROR: Failed to connect to Neo4j
```
**Solution**: Check Neo4j is running:
```bash
sudo systemctl status neo4j
# or
docker ps | grep neo4j
```

### Low CVE Count
If final count is significantly lower than 35,000:
1. Check date range in progress file
2. Verify NVD API is accessible: `curl -I https://services.nvd.nist.gov/rest/json/cves/2.0`
3. Check logs for repeated errors

## Logs and Monitoring

### Log File
`nvd_import_2018_2019.log` contains:
- Timestamp for each operation
- API request details
- Import statistics
- Error messages

### Monitor Active Import
```bash
# Watch log in real-time
tail -f nvd_import_2018_2019.log

# Check progress file
cat .nvd_import_progress.json | jq '.'

# Check Neo4j CVE count
python -c "from neo4j import GraphDatabase; \
  d = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'neo4j@openspg')); \
  with d.session() as s: \
    r = s.run('MATCH (c:CVE) WHERE c.published_date >= \"2018-01-01\" AND c.published_date < \"2020-01-01\" RETURN count(c) as count'); \
    print(f'CVEs imported: {r.single()[\"count\"]}'); \
  d.close()"
```

## Expected Output

### Console Output
```
============================================================
NVD CVE Import Script - 2018-2019
============================================================
Start time: 2025-10-29 16:00:00
Target: ~35,000-40,000 CVEs from 2018-2019
Rate limit: 6s between requests
============================================================

2025-10-29 16:00:01 - __main__ - INFO - Setting up Neo4j schema...
2025-10-29 16:00:02 - __main__ - INFO - Schema setup complete
2025-10-29 16:00:02 - __main__ - INFO - Starting import for years 2018-2019

============================================================
Processing year: 2018
============================================================

2025-10-29 16:00:02 - __main__ - INFO - Processing 2018-01: 2018-01-01T00:00:00.000 to 2018-01-31T23:59:59.999
2025-10-29 16:00:09 - __main__ - INFO - Total CVEs for 2018-01: 1876
2025-10-29 16:00:10 - __main__ - INFO - Imported batch: 0 to 1876
2025-10-29 16:00:11 - __main__ - INFO - Completed 2018-01: 1876 total CVEs
...
```

### Summary Output
```
============================================================
IMPORT SUMMARY
============================================================
CVEs Processed: 37,824
CVEs Created: 37,824
CWEs Linked: 45,312
CAPECs Linked: 0
Errors: 0
Duration: 0:04:32
Rate: 139.21 CVEs/second
============================================================
```

## Next Steps

After successful import:

1. **Verify data quality**:
   ```cypher
   MATCH (c:CVE)
   WHERE c.published_date >= '2018-01-01' AND c.published_date < '2020-01-01'
   RETURN
     count(c) as total_cves,
     avg(c.cvss_score) as avg_score,
     count(DISTINCT c.severity) as severity_types
   ```

2. **Link to CAPEC** (if CAPEC data exists):
   - Run CWE→CAPEC relationship creation script
   - This requires CAPEC data to be imported separately

3. **Create additional relationships**:
   - CVE→Product relationships
   - CVE→Vendor relationships
   - CVE→Configuration relationships

4. **Export for analysis**:
   ```cypher
   MATCH (c:CVE)-[r:EXPLOITS_WEAKNESS]->(w:CWE)
   WHERE c.published_date >= '2018-01-01' AND c.published_date < '2020-01-01'
   RETURN c.cve_id, c.cvss_score, c.severity, collect(w.cwe_id) as cwes
   ```

## API Reference

### NVD API v2.0
- **Base URL**: https://services.nvd.nist.gov/rest/json/cves/2.0
- **Documentation**: https://nvd.nist.gov/developers/vulnerabilities
- **Rate Limit**: 5 requests per 30 seconds (no API key)
- **Rate Limit with API Key**: 50 requests per 30 seconds

### To Use API Key (Optional)
If you have an NVD API key for faster imports:

1. Get API key from: https://nvd.nist.gov/developers/request-an-api-key
2. Modify script line 19:
   ```python
   NVD_API_KEY = "your-api-key-here"
   ```
3. Update headers in `fetch_cves()` method:
   ```python
   headers = {'apiKey': NVD_API_KEY}
   response = requests.get(NVD_API_BASE, params=params, headers=headers, timeout=30)
   ```
4. Reduce rate limit delay to 0.6 seconds (50 req/30s)

## Support

### Issues
- Check logs: `nvd_import_2018_2019.log`
- Check progress: `.nvd_import_progress.json`
- Verify Neo4j: `check_neo4j_status.py`

### Contact
For questions or issues, contact the AEON project team.

---

**Created**: 2025-10-29
**Version**: 1.0
**Author**: Backend API Developer Agent
**Purpose**: NVD CVE 2018-2019 import documentation
