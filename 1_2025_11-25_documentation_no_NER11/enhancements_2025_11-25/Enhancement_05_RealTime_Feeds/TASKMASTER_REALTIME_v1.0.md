# TASKMASTER - Real-Time Threat Feed Integration v1.0

**Document**: Real-Time Threat Feed Integration Task Specifications
**Version**: 1.0.0
**Created**: 2025-11-25
**Target Completion**: Implementation-ready specifications
**Total Tasks**: 24 (grouped in 6 phases)

## Phase 1: Foundation & Configuration (Tasks 1-4)

### Task 1.1: API Key Validation and Environment Setup

**Objective**: Verify all API keys are available and environment properly configured.

**Prerequisites**:
- Access to `/etc/aeon/` configuration directory
- Environment variable whitelist (VULNCHECK_API_KEY, NVD_API_KEY, etc.)
- Kubernetes secrets configured (if applicable)

**Deliverables**:
- `.env.example` template with all required keys
- Environment validation script (`validate_env.sh`)
- API key rotation schedule document
- Documentation: API key management procedures

**Success Criteria**:
- All 6 API keys validated and accessible
- Environment variables properly isolated (not in git)
- Logging confirms successful connection to all sources
- Backup credentials configured

**Estimated Effort**: 4 hours
**Assigned To**: DevOps Engineer
**Status**: Pending

---

### Task 1.2: Neo4j Graph Preparation and Schema Extension

**Objective**: Extend existing Neo4j schema to support real-time feed data with proper indexing.

**Current State**: 5,001 InformationEvent nodes with existing schema

**Schema Extensions Required**:

```cypher
# Create indices for performance
CREATE INDEX vulnerability_cveId IF NOT EXISTS FOR (v:Vulnerability) ON (v.cveId);
CREATE INDEX vulnerability_cvss IF NOT EXISTS FOR (v:Vulnerability) ON (v.cvssScore);
CREATE INDEX vulnerability_ingestedAt IF NOT EXISTS FOR (v:Vulnerability) ON (v.ingestedAt);
CREATE INDEX threatactor_apiid IF NOT EXISTS FOR (a:ThreatActor) ON (a.apiId);
CREATE INDEX indicator_value IF NOT EXISTS FOR (i:Indicator) ON (i.value);
CREATE INDEX campaign_lastSeen IF NOT EXISTS FOR (c:Campaign) ON (c.lastSeen);

# Extend existing InformationEvent node
ALTER NODE InformationEvent ADD PROPERTY sourceApi STRING;
ALTER NODE InformationEvent ADD PROPERTY ingestedAt DATETIME;
ALTER NODE InformationEvent ADD PROPERTY rawData STRING;
ALTER NODE InformationEvent ADD PROPERTY dedupHash STRING;

# Create audit node type
CREATE NODE TYPE AuditLog (
  id STRING PRIMARY KEY,
  timestamp DATETIME,
  action STRING,
  sourceEntity STRING,
  changeDetails STRING,
  userId STRING,
  ipAddress STRING
);
```

**Deliverables**:
- Migration script for schema extensions
- Index creation and verification script
- Performance baseline query tests
- Rollback procedures (if needed)

**Success Criteria**:
- All indices created and verified
- Query performance <200ms for common searches
- Existing 5,001 nodes accessible post-migration
- Schema aligned with NVD, VulnCheck, MITRE models

**Estimated Effort**: 6 hours
**Assigned To**: Database Architect
**Status**: Pending

---

### Task 1.3: Message Queue Setup (RabbitMQ/Redis)

**Objective**: Configure message queue for buffering incoming threat data.

**Architecture**:
```
API Consumers → Message Queue → Batch Processor → Neo4j
```

**Configuration Requirements**:
- Queue depth: 10,000 messages minimum
- Time-to-live: 24 hours (auto-discard old messages)
- Dead letter queue for failed messages
- Priority queues (Critical: KEV updates, High: VulnCheck, Normal: NVD daily)

**Deliverables**:
- Docker Compose configuration for RabbitMQ
- Queue initialization scripts
- Monitoring dashboard (CloudAMQP or local)
- Performance load testing results

**Success Criteria**:
- Queue handles 200+ messages/minute sustained
- Message delivery guaranteed (persistent storage)
- Monitoring shows queue depth and latency
- Failover procedures documented

**Estimated Effort**: 5 hours
**Assigned To**: DevOps Engineer
**Status**: Pending

---

### Task 1.4: Logging and Audit Infrastructure

**Objective**: Implement comprehensive logging for all ingestion operations.

**Logging Requirements**:
- Each API call logged (timestamp, source, result, latency)
- Graph modifications audited (who, what, when, why)
- Data validation errors tracked
- Rate limit tracking per source
- Deduplication decisions logged

**Deliverables**:
- ELK stack configuration (or Splunk equivalent)
- Log schema definition (fields, parsing rules)
- Audit log retention policy (90 days minimum)
- Dashboard for log visualization
- Alert rules for anomalies (>50 errors/hour, rate limit exceeded, etc.)

**Success Criteria**:
- 100% of API calls logged
- Sub-second log query performance
- Audit trail immutable and tamper-evident
- Log rotation automated (disk space management)

**Estimated Effort**: 5 hours
**Assigned To**: Security Engineer
**Status**: Pending

---

## Phase 2: API Integrations (Tasks 5-10)

### Task 2.1: VulnCheck API Client Implementation

**Objective**: Build Python SDK wrapper for VulnCheck API with error handling and retries.

**VulnCheck API Specifications**:
- Base URL: `https://api.vulncheck.com/v3/`
- Authentication: Bearer token (API key)
- Rate Limit: 300 requests/minute for standard tier
- Response Format: JSON

**Endpoints to Implement**:
1. `/vulnerabilities` - List all vulnerabilities (paginated)
2. `/vulnerabilities/{cveId}` - Get specific CVE details
3. `/vulnerabilities/{cveId}/exploit` - Exploit intel for CVE
4. `/threat-intel` - Zero-day threat intelligence
5. `/indicators` - IoC indicators and infrastructure

**Implementation Tasks**:

```python
# vulncheck_client.py
import requests
from datetime import datetime
import logging

class VulncheckClient:
    def __init__(self, api_key: str, base_url: str = "https://api.vulncheck.com/v3/"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        self.logger = logging.getLogger(__name__)

    def get_vulnerabilities(self, limit: int = 100, offset: int = 0):
        """Fetch vulnerability list with pagination"""
        endpoint = f"{self.base_url}vulnerabilities"
        params = {"limit": limit, "offset": offset}
        response = self.session.get(endpoint, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_vulnerability_details(self, cve_id: str):
        """Fetch detailed vulnerability information"""
        endpoint = f"{self.base_url}vulnerabilities/{cve_id}"
        response = self.session.get(endpoint, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_exploit_intelligence(self, cve_id: str):
        """Fetch exploit code and intelligence for CVE"""
        endpoint = f"{self.base_url}vulnerabilities/{cve_id}/exploit"
        response = self.session.get(endpoint, timeout=30)
        response.raise_for_status()
        return response.json()

    def stream_vulnerabilities(self, since: datetime = None):
        """Stream real-time vulnerability updates"""
        endpoint = f"{self.base_url}vulnerabilities/stream"
        params = {"since": since.isoformat() if since else None}
        response = self.session.get(endpoint, params=params, stream=True, timeout=60)
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                yield json.loads(line)
```

**Deliverables**:
- VulnCheck Python client (300+ lines)
- Unit tests with mocked API responses
- Integration tests (requires valid API key)
- Rate limit handler with exponential backoff
- Error handling and logging

**Success Criteria**:
- All 5 endpoints functional
- Rate limits properly respected (queueing when necessary)
- Retry logic: 3 attempts with exponential backoff
- Connection timeout: 30 seconds
- Test coverage: >90%

**Estimated Effort**: 8 hours
**Assigned To**: Backend Developer
**Status**: Pending

---

### Task 2.2: NVD API Integration

**Objective**: Build NVD API consumer for CVE data.

**NVD API Specifications**:
- Base URL: `https://services.nvd.nist.gov/rest/json/cves/2.0`
- Authentication: API key (optional but recommended for higher rate limits)
- Rate Limit: 5 requests/30 seconds (without key), higher with API key
- Data Format: JSON with CVSS v3.1 scoring

**Endpoints**:
1. `/cves` - List CVEs (paginated, 2,000 results per page)
2. `/cves/{cveId}` - Get specific CVE details
3. Query parameters: `lastModStartDate`, `lastModEndDate`, `pubStartDate`, `pubEndDate`

**Implementation Tasks**:

```python
# nvd_client.py
import requests
from datetime import datetime, timedelta
import json

class NVDClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"X-API-KEY": api_key})
        self.rate_limit_reset = 0

    def get_cves(self, start_index: int = 0, limit: int = 2000,
                 last_mod_start: datetime = None, last_mod_end: datetime = None):
        """Fetch CVE list with pagination and date filtering"""
        params = {
            "startIndex": start_index,
            "resultsPerPage": min(limit, 2000),  # NVD max is 2000
        }

        if last_mod_start:
            params["lastModStartDate"] = last_mod_start.isoformat() + "Z"
        if last_mod_end:
            params["lastModEndDate"] = last_mod_end.isoformat() + "Z"

        response = self.session.get(self.base_url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_cve_details(self, cve_id: str):
        """Fetch details for specific CVE"""
        endpoint = f"{self.base_url}/{cve_id}"
        response = self.session.get(endpoint, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('vulnerabilities', [{}])[0]

    def stream_daily_cves(self):
        """Stream today's new/modified CVEs"""
        now = datetime.utcnow()
        start = (now - timedelta(days=1)).isoformat() + "Z"
        end = now.isoformat() + "Z"

        start_index = 0
        while True:
            data = self.get_cves(start_index=start_index,
                                last_mod_start=start,
                                last_mod_end=end)

            for vuln in data.get('vulnerabilities', []):
                yield vuln

            if data['startIndex'] + len(data.get('vulnerabilities', [])) >= data['totalResults']:
                break
            start_index += len(data.get('vulnerabilities', []))
```

**Deliverables**:
- NVD Python client (250+ lines)
- Daily CVE fetch scheduler
- Incremental update logic (only new/modified)
- CVSS score extraction and normalization
- Tests with sample NVD responses

**Success Criteria**:
- Handles 500+ CVEs per daily run
- Parses CVSS v3.1 scores correctly
- Incremental updates only (no full re-import)
- Rate limits properly respected
- Error recovery for network failures

**Estimated Effort**: 7 hours
**Assigned To**: Backend Developer
**Status**: Pending

---

### Task 2.3: MITRE ATT&CK Framework Integration

**Objective**: Consume MITRE ATT&CK data and create relationships to vulnerabilities.

**MITRE Data Source**:
- URL: `https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack.json`
- Format: STIX 2.1 JSON bundle
- Content: Techniques, Tactics, Groups, Software, Campaigns
- Update Frequency: Quarterly + monthly patches

**Implementation Tasks**:

```python
# mitre_client.py
from stix2 import parse_obj_bundle
import requests
import hashlib

class MitreClient:
    def __init__(self):
        self.mitre_url = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack.json"
        self.cache_file = "/tmp/enterprise-attack.json"

    def fetch_framework(self):
        """Download and cache MITRE ATT&CK framework"""
        response = requests.get(self.mitre_url, timeout=60)
        response.raise_for_status()

        with open(self.cache_file, 'w') as f:
            f.write(response.text)

        return response.json()

    def parse_bundle(self):
        """Parse STIX bundle into organized data"""
        with open(self.cache_file, 'r') as f:
            bundle_data = json.load(f)

        bundle = parse_obj_bundle(bundle_data)

        techniques = {}
        tactics = {}
        groups = {}
        malware = {}
        tools = {}

        for obj in bundle.objects:
            if obj.type == 'attack-pattern':  # Technique
                techniques[obj.id] = {
                    'id': obj.id,
                    'name': obj.name,
                    'description': obj.description,
                    'tactics': getattr(obj, 'x_mitre_platforms', []),
                    'external_id': obj.get('external_references', [{}])[0].get('external_id'),
                }
            elif obj.type == 'x-mitre-tactic':
                tactics[obj.id] = {
                    'id': obj.id,
                    'name': obj.name,
                    'description': obj.description,
                }
            elif obj.type == 'intrusion-set':  # Group
                groups[obj.id] = {
                    'id': obj.id,
                    'name': obj.name,
                    'description': obj.description,
                    'aliases': getattr(obj, 'aliases', []),
                }
            # ... parse malware, tools, campaigns

        return {
            'techniques': techniques,
            'tactics': tactics,
            'groups': groups,
            'malware': malware,
            'tools': tools,
        }

    def get_technique_by_id(self, attack_id: str):
        """Find technique by ATT&CK ID (e.g., T1234)"""
        # Load and search framework
        pass
```

**Deliverables**:
- MITRE framework parser (200+ lines)
- Technique/Tactic/Group extraction
- Relationship mapping utilities
- Framework versioning (track updates)
- Tests with sample MITRE data

**Success Criteria**:
- Parse 200+ techniques correctly
- Extract 130+ threat groups
- 500+ malware families mapped
- Update detection (version tracking)
- Relationship mapping: Vuln → Technique → Group

**Estimated Effort**: 6 hours
**Assigned To**: Backend Developer
**Status**: Pending

---

### Task 2.4: CISA KEV Feed Parser

**Objective**: Parse CISA Known Exploited Vulnerabilities catalog.

**CISA KEV Specifications**:
- URL: `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv`
- Format: CSV with 14 fields
- Updates: Weekly (Thursdays)
- Content: 1,000+ exploited vulnerabilities with exploitation dates

**CSV Fields**:
```
cveID,vendor,product,vulnerabilityName,dateAdded,shortDescription,requiredAction,dueDate,notes,knownRansomwareCampaignUse
```

**Implementation Tasks**:

```python
# cisa_client.py
import csv
from datetime import datetime
import requests

class CisaClient:
    def __init__(self):
        self.kev_url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv"

    def fetch_kev_catalog(self):
        """Download CISA KEV catalog"""
        response = requests.get(self.kev_url, timeout=30)
        response.raise_for_status()
        return response.text

    def parse_kev_csv(self, csv_content: str):
        """Parse KEV CSV into structured records"""
        reader = csv.DictReader(csv_content.splitlines())

        kev_entries = []
        for row in reader:
            entry = {
                'cveId': row['cveID'],
                'vendor': row['vendor'],
                'product': row['product'],
                'name': row['vulnerabilityName'],
                'dateAdded': datetime.strptime(row['dateAdded'], '%Y-%m-%d').isoformat(),
                'description': row['shortDescription'],
                'requiredAction': row['requiredAction'],
                'dueDate': datetime.strptime(row['dueDate'], '%Y-%m-%d').isoformat() if row.get('dueDate') else None,
                'ransomwareUse': row['knownRansomwareCampaignUse'].lower() == 'yes',
                'notes': row['notes'],
            }
            kev_entries.append(entry)

        return kev_entries

    def identify_new_kev(self, current_entries, previous_entries):
        """Identify new KEV entries since last update"""
        previous_cves = {e['cveId'] for e in previous_entries}
        new_entries = [e for e in current_entries if e['cveId'] not in previous_cves]
        return new_entries
```

**Deliverables**:
- CISA CSV parser (150+ lines)
- KEV differential tracking (new vs existing)
- Ransomware correlation flag
- Weekly scheduler
- Tests with sample CISA data

**Success Criteria**:
- Parse 1,000+ entries without errors
- Date format normalization (ISO 8601)
- Identify new entries weekly
- Ransomware classification accurate
- Reconcile with existing CVE nodes

**Estimated Effort**: 4 hours
**Assigned To**: Backend Developer
**Status**: Pending

---

### Task 2.5: STIX/TAXII Feed Integration

**Objective**: Consume STIX 2.1 threat data via TAXII protocol.

**STIX/TAXII Specifications**:
- Protocol: TAXII 2.1 (HTTPS REST API)
- Authentication: OAuth 2.0 or API key
- Response Format: STIX 2.1 JSON bundles
- Content Types: Indicators, Malware, Campaigns, Attack Patterns, Infrastructure

**Implementation Tasks**:

```python
# taxii_client.py
import requests
from stix2 import parse_obj_bundle
from datetime import datetime, timedelta

class TaxiiClient:
    def __init__(self, discovery_url: str, credentials: dict):
        self.discovery_url = discovery_url
        self.credentials = credentials
        self.session = requests.Session()
        self.auth_token = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate and get bearer token"""
        auth_response = requests.post(
            f"{self.discovery_url}/oauth/token",
            json=self.credentials,
            timeout=30
        )
        auth_response.raise_for_status()
        self.auth_token = auth_response.json()['access_token']
        self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})

    def get_collections(self):
        """List available TAXII collections"""
        api_root = f"{self.discovery_url}/api/root"
        response = self.session.get(api_root, timeout=30)
        response.raise_for_status()
        return response.json()

    def fetch_objects(self, collection_id: str, obj_type: str = None,
                     added_after: datetime = None):
        """Fetch objects from collection with optional filtering"""
        endpoint = f"{self.discovery_url}/api/root/collections/{collection_id}/objects"
        params = {}

        if obj_type:
            params['type'] = obj_type
        if added_after:
            params['added_after'] = added_after.isoformat()

        response = self.session.get(endpoint, params=params, timeout=60)
        response.raise_for_status()

        bundle = parse_obj_bundle(response.json())
        return list(bundle.objects)
```

**Deliverables**:
- TAXII client (200+ lines)
- OAuth 2.0 authentication handler
- Object type parser (Indicator, Malware, Campaign, etc.)
- Collection discovery
- Incremental sync support

**Success Criteria**:
- Successfully authenticate to TAXII server
- Fetch 500+ objects per update
- Parse STIX 2.1 correctly
- Incremental updates (added_after filter)
- Error handling for authentication failures

**Estimated Effort**: 6 hours
**Assigned To**: Backend Developer
**Status**: Pending

---

### Task 2.6: Real-Time Webhook Receivers

**Objective**: Build webhook receivers for push-based threat updates.

**Webhook Requirements**:
- VulnCheck webhooks (vulnerability alerts)
- Custom threat intel webhooks
- STIX/TAXII webhooks (real-time feeds)
- Webhook signature verification (HMAC-SHA256)
- Rate limiting (100+ webhooks/minute capacity)

**Implementation Tasks**:

```python
# webhook_server.py
from flask import Flask, request
import hmac
import hashlib
import json
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

class WebhookHandler:
    def __init__(self, secret_keys: dict):
        self.secret_keys = secret_keys  # {source: secret_key}

    def verify_signature(self, source: str, payload: bytes, signature: str) -> bool:
        """Verify webhook signature using HMAC-SHA256"""
        expected_sig = hmac.new(
            self.secret_keys[source].encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_sig)

    def handle_vulncheck_webhook(self, data: dict):
        """Process VulnCheck webhook (new vulnerability or threat)"""
        logger.info(f"VulnCheck alert: {data.get('cveId')}")
        # Queue for processing
        message_queue.put({
            'source': 'vulncheck',
            'type': 'vulnerability',
            'payload': data,
            'timestamp': datetime.utcnow(),
            'priority': 'high' if 'zeroday' in data else 'normal'
        })

    def handle_stix_webhook(self, data: dict):
        """Process STIX object update webhook"""
        logger.info(f"STIX update: {data.get('type')}")
        message_queue.put({
            'source': 'stix',
            'type': data.get('type'),
            'payload': data,
            'timestamp': datetime.utcnow(),
            'priority': 'normal'
        })

handler = WebhookHandler({
    'vulncheck': os.environ['VULNCHECK_WEBHOOK_SECRET'],
    'stix': os.environ['STIX_WEBHOOK_SECRET'],
})

@app.route('/webhooks/vulncheck', methods=['POST'])
def vulncheck_webhook():
    """VulnCheck webhook endpoint"""
    signature = request.headers.get('X-Signature')

    if not handler.verify_signature('vulncheck', request.data, signature):
        logger.warning("Invalid VulnCheck webhook signature")
        return {'error': 'Invalid signature'}, 401

    data = request.json
    handler.handle_vulncheck_webhook(data)
    return {'status': 'accepted'}, 202

@app.route('/webhooks/stix', methods=['POST'])
def stix_webhook():
    """STIX/TAXII webhook endpoint"""
    signature = request.headers.get('Authorization', '').replace('Bearer ', '')

    if not handler.verify_signature('stix', request.data, signature):
        return {'error': 'Unauthorized'}, 401

    data = request.json
    handler.handle_stix_webhook(data)
    return {'status': 'accepted'}, 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

**Deliverables**:
- Flask webhook server (250+ lines)
- Signature verification (HMAC-SHA256)
- Per-source rate limiting
- Message queue integration
- Error logging and monitoring

**Success Criteria**:
- Handle 100+ webhooks/minute
- All signatures verified correctly
- Rate limits enforced per source
- Zero dropped messages (persistent queue)
- Latency <500ms webhook processing

**Estimated Effort**: 5 hours
**Assigned To**: Backend Developer
**Status**: Pending

---

## Phase 3: Data Normalization (Tasks 11-14)

### Task 3.1: Vulnerability Data Normalization

**Objective**: Normalize vulnerability data from multiple sources into unified format.

**Normalization Rules**:

```python
# threat_models.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class NormalizedVulnerability:
    """Unified vulnerability data model"""
    cveId: str  # Always NIST format (CVE-YYYY-NNNNN)
    title: str
    description: str

    # Severity
    cvssScore: float  # CVSS v3.1
    cvssVersion: str = "3.1"
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW

    # Dates
    publishedDate: datetime
    discoveredDate: Optional[datetime] = None
    disclosedDate: Optional[datetime] = None
    exploitAvailable: Optional[datetime] = None
    patchAvailable: Optional[datetime] = None

    # Affected Products
    affectedVendors: List[str] = None
    affectedProducts: List[str] = None
    affectedVersions: List[str] = None

    # Exploit & Intelligence
    exploitCodeAvailable: bool = False
    activelyExploited: bool = False
    cisaKev: bool = False
    cisaDueDate: Optional[datetime] = None
    ransomwareUsed: bool = False

    # References
    sourceLinks: List[str] = None
    references: List[dict] = None

    # Metadata
    sourceApis: List[str] = None  # ['nvd', 'vulncheck', ...]
    ingestedAt: datetime = None
    lastUpdated: datetime = None
    dedupHash: str = None  # MD5(cveId + title + cvss)

    def to_neo4j(self) -> dict:
        """Convert to Neo4j node properties"""
        return {
            'cveId': self.cveId,
            'title': self.title,
            'description': self.description[:5000],  # Truncate to 5000 chars
            'cvssScore': self.cvssScore,
            'severity': self.severity,
            'publishedDate': self.publishedDate.isoformat(),
            'exploitCodeAvailable': self.exploitCodeAvailable,
            'activelyExploited': self.activelyExploited,
            'cisaKev': self.cisaKev,
            'ransomwareUsed': self.ransomwareUsed,
            'ingestedAt': self.ingestedAt.isoformat(),
            'sourceApis': '|'.join(self.sourceApis) if self.sourceApis else '',
        }

# Normalizer functions
def normalize_nvd_vulnerability(nvd_record: dict) -> NormalizedVulnerability:
    """Convert NVD CVE record to normalized format"""
    cve = nvd_record['cve']
    metrics = nvd_record.get('metrics', {})
    cvss = metrics.get('cvssV31', {}) or metrics.get('cvssV30', {})

    return NormalizedVulnerability(
        cveId=cve['id'],
        title=cve['descriptions'][0]['value'][:200],
        description=cve['descriptions'][0]['value'],
        cvssScore=cvss.get('cvssData', {}).get('baseScore', 0.0),
        severity=cvss.get('cvssData', {}).get('baseSeverity', 'UNKNOWN'),
        publishedDate=datetime.fromisoformat(cve['published'][:19]),
        disclosedDate=datetime.fromisoformat(cve.get('lastModified', cve['published'])[:19]),
        sourceApis=['nvd'],
    )

def normalize_vulncheck_vulnerability(vc_record: dict) -> NormalizedVulnerability:
    """Convert VulnCheck record to normalized format"""
    return NormalizedVulnerability(
        cveId=vc_record['cveId'],
        title=vc_record.get('title', ''),
        description=vc_record.get('description', ''),
        cvssScore=float(vc_record.get('cvssScore', 0.0)),
        severity=_cvss_to_severity(float(vc_record.get('cvssScore', 0.0))),
        publishedDate=datetime.fromisoformat(vc_record['publishedDate'][:19]),
        exploitCodeAvailable=vc_record.get('exploitAvailable', False),
        exploitAvailable=datetime.fromisoformat(vc_record['exploitDate']) if vc_record.get('exploitDate') else None,
        sourceApis=['vulncheck'],
    )
```

**Deliverables**:
- Unified data model (NormalizedVulnerability) (100+ lines)
- Normalizers for each source (NVD, VulnCheck, CISA, STIX)
- Severity mapping (CVSS to severity levels)
- Date normalization (handle various formats)
- Unit tests for all normalizers

**Success Criteria**:
- All vulnerability fields normalized consistently
- CVSS scores accurate (no conversion errors)
- Dates in ISO 8601 UTC format
- Null values handled gracefully
- 100% test coverage for normalizers

**Estimated Effort**: 5 hours
**Assigned To**: Backend Developer
**Status**: Pending

---

### Task 3.2: Threat Actor & Campaign Normalization

**Objective**: Normalize threat actor and campaign data.

**Normalization Model**:

```python
@dataclass
class NormalizedThreatActor:
    actorId: str  # Primary key
    name: str
    aliases: List[str] = None
    description: str = None
    country: Optional[str] = None
    firstSeen: Optional[datetime] = None
    lastSeen: Optional[datetime] = None
    motivations: List[str] = None  # [economic, espionage, destructive, ...]
    targetSectors: List[str] = None
    targetCountries: List[str] = None
    sophistication: str = None  # [novice, intermediate, advanced, expert]
    capabilities: List[str] = None
    sourceApis: List[str] = None
    ingestedAt: datetime = None

@dataclass
class NormalizedCampaign:
    campaignId: str
    name: str
    description: str = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    techniques: List[str] = None  # MITRE technique IDs
    malware: List[str] = None  # Malware family names
    vulnerability: List[str] = None  # CVE IDs exploited
    targetSectors: List[str] = None
    targetCountries: List[str] = None
    sources: List[str] = None
    ingestedAt: datetime = None
```

**Deliverables**:
- Threat actor normalization (150+ lines)
- Campaign normalization (150+ lines)
- Alias mapping and deduplication
- Country code normalization (ISO 3166-1 alpha-2)
- Tests with MITRE, VulnCheck data

**Success Criteria**:
- Unique actor IDs generated (no duplicates)
- Alias mapping prevents duplication
- All dates normalized to ISO 8601
- Sector/country standardization applied
- Cross-source reconciliation working

**Estimated Effort**: 4 hours
**Assigned To**: Backend Developer
**Status**: Pending

---

### Task 3.3: Indicator Normalization (IoCs)

**Objective**: Normalize indicators of compromise.

**Indicator Types**:
- IP addresses (IPv4, IPv6)
- Domain names (FQDN, wildcard)
- URLs
- File hashes (MD5, SHA-1, SHA-256)
- Email addresses
- Certificates
- YARA rules

**Implementation**:

```python
from enum import Enum
from dataclasses import dataclass
import ipaddress

class IndicatorType(Enum):
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    DOMAIN = "domain"
    URL = "url"
    EMAIL = "email"
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    YARA = "yara"
    CERTIFICATE = "certificate"

@dataclass
class NormalizedIndicator:
    value: str  # The actual indicator
    type: IndicatorType
    tlp: str = "TLP:CLEAR"  # Traffic Light Protocol
    severity: str = "UNKNOWN"
    confidence: float = 1.0  # 0.0 - 1.0
    firstSeen: datetime = None
    lastSeen: datetime = None
    sources: List[str] = None
    context: dict = None  # Additional context (whois, ASN, etc.)

    def validate(self) -> bool:
        """Validate indicator value matches type"""
        if self.type == IndicatorType.IPV4:
            try:
                ipaddress.IPv4Address(self.value)
                return True
            except:
                return False
        elif self.type == IndicatorType.IPV6:
            try:
                ipaddress.IPv6Address(self.value)
                return True
            except:
                return False
        elif self.type == IndicatorType.MD5:
            return len(self.value) == 32 and all(c in '0123456789abcdef' for c in self.value.lower())
        # ... add validations for other types
        return True

def normalize_indicator(raw_value: str, source_type: str) -> NormalizedIndicator:
    """Normalize raw indicator to standard format"""
    value = raw_value.lower().strip()

    # Detect type and normalize
    if is_valid_ipv4(value):
        return NormalizedIndicator(value=value, type=IndicatorType.IPV4)
    elif is_valid_ipv6(value):
        return NormalizedIndicator(value=value, type=IndicatorType.IPV6)
    elif is_valid_domain(value):
        return NormalizedIndicator(value=value, type=IndicatorType.DOMAIN)
    # ... etc.
```

**Deliverables**:
- Indicator types and validation (150+ lines)
- Type detection and normalization
- TLP classification mapping
- Confidence scoring rules
- Tests with sample indicators

**Success Criteria**:
- All indicator types validated correctly
- 99%+ accuracy in type detection
- Normalization consistent across sources
- TLP/confidence applied correctly
- Deduplication identifies duplicates

**Estimated Effort**: 4 hours
**Assigned To**: Backend Developer
**Status**: Pending

---

### Task 3.4: Data Deduplication & Enrichment

**Objective**: Implement intelligent deduplication and multi-source enrichment.

**Deduplication Strategy**:

```python
import hashlib

class DeduplicationEngine:
    def __init__(self, neo4j_connection):
        self.neo4j = neo4j_connection
        self.seen_hashes = set()

    def calculate_dedup_hash(self, vulnerability: NormalizedVulnerability) -> str:
        """Create hash from core vulnerability fields"""
        core_data = f"{vulnerability.cveId}|{vulnerability.cvssScore}"
        return hashlib.md5(core_data.encode()).hexdigest()

    def is_duplicate(self, item: dict, item_type: str) -> tuple:
        """Check if item is duplicate, return (is_dup, existing_id)"""
        dedup_hash = self.calculate_dedup_hash(item)

        # Query existing nodes
        query = f"""
        MATCH (n:{item_type} {{dedupHash: $hash}})
        RETURN n.id AS id
        """

        result = self.neo4j.query(query, {'hash': dedup_hash})

        if result:
            return True, result[0]['id']
        return False, None

    def enrich_from_multiple_sources(self, cve_id: str):
        """Combine data from all sources for a single CVE"""
        enriched = {}

        # Get from NVD
        nvd_data = self.fetch_from_source(cve_id, 'nvd')
        if nvd_data:
            enriched.update(nvd_data)

        # Get from VulnCheck (overrides NVD where more recent)
        vc_data = self.fetch_from_source(cve_id, 'vulncheck')
        if vc_data and vc_data.get('ingestedAt') > enriched.get('ingestedAt', datetime.min):
            enriched.update(vc_data)

        # Get from CISA (only if KEV)
        cisa_data = self.fetch_from_source(cve_id, 'cisa')
        if cisa_data:
            enriched['cisaKev'] = True
            enriched['cisaDueDate'] = cisa_data.get('dueDate')
            enriched['ransomwareUsed'] = cisa_data.get('ransomwareUse')

        # Consolidate sources
        enriched['sourceApis'] = list(set([
            *enriched.get('sourceApis', []),
            *([s for s in ['nvd', 'vulncheck', 'cisa'] if self.fetch_from_source(cve_id, s)])
        ]))

        return enriched
```

**Deliverables**:
- Deduplication engine (150+ lines)
- Multi-source enrichment logic
- Hash calculation methods
- Conflict resolution (which source wins)
- Integration with graph database

**Success Criteria**:
- <2% false positives in deduplication
- 100% of eligible records enriched
- Source priority documented and consistent
- Enrichment increases data completeness >20%
- No data loss in consolidation

**Estimated Effort**: 5 hours
**Assigned To**: Backend Developer
**Status**: Pending

---

## Phase 4: Graph Ingestion (Tasks 15-18)

### Task 4.1: Neo4j Ingestion Pipeline

**Objective**: Build high-performance Neo4j ingestion using batch Cypher.

**Implementation**:

```python
# neo4j_ingester.py
from neo4j import GraphDatabase
from typing import List

class Neo4jIngester:
    def __init__(self, uri: str, username: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def ingest_vulnerabilities_batch(self, vulnerabilities: List[dict], batch_size: int = 100):
        """Batch ingest normalized vulnerabilities"""
        with self.driver.session() as session:
            for i in range(0, len(vulnerabilities), batch_size):
                batch = vulnerabilities[i:i+batch_size]

                query = """
                UNWIND $vulnerabilities AS vuln
                MERGE (v:Vulnerability {cveId: vuln.cveId})
                ON CREATE SET
                  v.createdAt = datetime(),
                  v.source = 'realtime-feed'
                ON MATCH SET
                  v.updatedAt = datetime()
                SET
                  v.title = vuln.title,
                  v.description = vuln.description,
                  v.cvssScore = vuln.cvssScore,
                  v.severity = vuln.severity,
                  v.publishedDate = vuln.publishedDate,
                  v.exploitCodeAvailable = vuln.exploitCodeAvailable,
                  v.activelyExploited = vuln.activelyExploited,
                  v.cisaKev = vuln.cisaKev,
                  v.ingestedAt = datetime(),
                  v.sourceApis = vuln.sourceApis
                RETURN count(v) AS created
                """

                result = session.run(query, {'vulnerabilities': batch})
                count = result.single()['created']
                print(f"Ingested {count} vulnerabilities")

    def create_vulnerability_relationships(self, relationships: List[dict]):
        """Create relationships between vulnerabilities and techniques"""
        with self.driver.session() as session:
            query = """
            UNWIND $rels AS rel
            MATCH (v:Vulnerability {cveId: rel.cveId})
            MATCH (t:MitreTechnique {attackId: rel.techniqueId})
            MERGE (v)-[r:EXPLOITS_TECHNIQUE]->(t)
            SET r.confidence = rel.confidence, r.discoveredAt = datetime()
            RETURN count(r) AS created
            """

            result = session.run(query, {'rels': relationships})
            count = result.single()['created']
            print(f"Created {count} relationships")

    def update_threat_actor_exploits(self, exploits: List[dict]):
        """Update threat actors and their vulnerability exploits"""
        with self.driver.session() as session:
            query = """
            UNWIND $exploits AS exploit
            MATCH (a:ThreatActor {id: exploit.actorId})
            MATCH (v:Vulnerability {cveId: exploit.cveId})
            MERGE (a)-[r:EXPLOITS]->(v)
            SET r.confidence = exploit.confidence,
                r.firstSeen = exploit.firstSeen,
                r.lastSeen = datetime()
            RETURN count(r) AS updated
            """

            result = session.run(query, {'exploits': exploits})
            count = result.single()['updated']
            print(f"Updated {count} threat actor relationships")
```

**Deliverables**:
- Neo4j batch ingestion (200+ lines)
- Relationship creation queries
- Transaction management
- Performance optimization (batch sizes)
- Error handling and rollback

**Success Criteria**:
- Ingest 1,000+ vulnerabilities/minute
- Batch transactions for consistency
- Proper error handling (invalid references)
- Query performance <200ms for 100-record batch
- No data corruption or duplicates

**Estimated Effort**: 6 hours
**Assigned To**: Database Developer
**Status**: Pending

---

### Task 4.2: Relationship Enrichment

**Objective**: Create rich relationships between entities.

**Relationship Types**:
- Vulnerability → EXPLOITS_TECHNIQUE → MITRE Technique
- Threat Actor → EXPLOITS → Vulnerability
- Campaign → EXPLOITS → Vulnerability
- Malware → EXPLOITS → Vulnerability
- Industry → TARGETED_BY → Campaign
- Asset → AFFECTED_BY → Vulnerability

**Implementation** (see Task 4.1 for pattern)

**Deliverables**:
- Relationship creation queries (150+ lines)
- Confidence scoring for relationships
- Temporal tracking (when relationship created)
- Bulk relationship update logic

**Success Criteria**:
- All entity types properly related
- <100ms query for relationship lookups
- Confidence scores distributed correctly
- No orphaned entities

**Estimated Effort**: 4 hours
**Assigned To**: Database Developer
**Status**: Pending

---

### Task 4.3: Real-Time Index Management

**Objective**: Maintain performance through dynamic index optimization.

**Index Strategy**:
- Create indices on frequently queried fields
- Monitor query plans (Cypher EXPLAIN)
- Remove unused indices (quarterly review)
- Rebuild fragmented indices

**Implementation**:

```cypher
# Vulnerability indices
CREATE INDEX vuln_cveId IF NOT EXISTS FOR (v:Vulnerability) ON (v.cveId);
CREATE INDEX vuln_cvss IF NOT EXISTS FOR (v:Vulnerability) ON (v.cvssScore);
CREATE INDEX vuln_ingestedAt IF NOT EXISTS FOR (v:Vulnerability) ON (v.ingestedAt);
CREATE INDEX vuln_cisaKev IF NOT EXISTS FOR (v:Vulnerability) ON (v.cisaKev);

# Threat actor indices
CREATE INDEX actor_id IF NOT EXISTS FOR (a:ThreatActor) ON (a.id);
CREATE INDEX actor_name IF NOT EXISTS FOR (a:ThreatActor) ON (a.name);

# Indicator indices
CREATE INDEX indicator_value IF NOT EXISTS FOR (i:Indicator) ON (i.value);
CREATE INDEX indicator_type IF NOT EXISTS FOR (i:Indicator) ON (i.type);

# Campaign indices
CREATE INDEX campaign_id IF NOT EXISTS FOR (c:Campaign) ON (c.id);
CREATE INDEX campaign_lastSeen IF NOT EXISTS FOR (c:Campaign) ON (c.lastSeen);

# Relationship indices
CREATE INDEX exploits_rel_confidence IF NOT EXISTS FOR ()-[r:EXPLOITS]-() ON (r.confidence);
CREATE INDEX mentions_rel_date IF NOT EXISTS FOR ()-[r:MENTIONED_IN]-() ON (r.date);
```

**Deliverables**:
- Index creation and management script (100+ lines)
- Index monitoring queries
- Fragmentation detection
- Rebuild procedures
- Performance testing framework

**Success Criteria**:
- Query performance <200ms for complex queries
- Index size <10GB
- No unused indices
- Rebuild time <5 minutes

**Estimated Effort**: 4 hours
**Assigned To**: Database Administrator
**Status**: Pending

---

### Task 4.4: Validation & Data Quality Assurance

**Objective**: Verify data quality post-ingestion.

**Validation Checks**:

```python
class DataQualityValidator:
    def __init__(self, neo4j_connection):
        self.neo4j = neo4j_connection

    def validate_vulnerability_integrity(self):
        """Ensure all vulnerabilities have required fields"""
        query = """
        MATCH (v:Vulnerability)
        WHERE v.cveId IS NULL OR v.cvssScore IS NULL OR v.severity IS NULL
        RETURN count(v) AS invalid_count
        """
        result = self.neo4j.query(query)
        invalid = result[0]['invalid_count']

        if invalid > 0:
            print(f"WARNING: {invalid} vulnerabilities missing required fields")
            return False
        return True

    def validate_relationship_integrity(self):
        """Ensure all relationships reference valid entities"""
        query = """
        MATCH (v:Vulnerability)-[r:EXPLOITS_TECHNIQUE]->(t:MitreTechnique)
        WHERE t.attackId IS NULL
        RETURN count(r) AS orphaned_rel
        """
        result = self.neo4j.query(query)
        orphaned = result[0]['orphaned_rel']

        return orphaned == 0

    def validate_duplicate_prevention(self):
        """Check for duplicate CVE entries"""
        query = """
        MATCH (v:Vulnerability)
        RETURN v.cveId, count(*) AS count
        WHERE count > 1
        """
        result = self.neo4j.query(query)
        duplicates = len(result)

        return duplicates == 0

    def generate_quality_report(self):
        """Generate comprehensive quality metrics"""
        metrics = {
            'total_vulnerabilities': self.count_nodes('Vulnerability'),
            'total_techniques': self.count_nodes('MitreTechnique'),
            'total_actors': self.count_nodes('ThreatActor'),
            'total_relationships': self.count_relationships(),
            'integrity_passed': self.validate_vulnerability_integrity(),
            'orphan_check_passed': self.validate_relationship_integrity(),
            'duplicate_check_passed': self.validate_duplicate_prevention(),
        }
        return metrics
```

**Deliverables**:
- Validation rule set (150+ lines)
- Data quality metrics calculation
- Anomaly detection
- Quality reports (JSON/HTML)
- Remediation recommendations

**Success Criteria**:
- 99.8%+ data integrity
- 0 duplicate CVEs
- 0 orphaned relationships
- All required fields populated
- Quality dashboard functioning

**Estimated Effort**: 4 hours
**Assigned To**: QA Engineer
**Status**: Pending

---

## Phase 5: Real-Time Processing & Alerts (Tasks 19-21)

### Task 5.1: Real-Time Event Stream Processing

**Objective**: Process incoming threat events in real-time with < 5 second latency.

**Architecture**:
```
Message Queue → Kafka/RabbitMQ
    ↓
Stream Processor (Python/Go)
    ↓
Event Filter & Aggregation
    ↓
Alert Generator
    ↓
Notification System
```

**Implementation** (high-level):
- Consume messages from queue
- Apply business rules (severity, relevance)
- Aggregate related events
- Generate alerts with context
- Publish to notification channels

**Deliverables**:
- Stream processor (250+ lines)
- Event aggregation logic
- Business rules engine
- Testing with simulated events

**Success Criteria**:
- <5 second E2E latency
- 99%+ event processing success rate
- Proper error handling and retry logic
- Alert accuracy >95%

**Estimated Effort**: 8 hours
**Assigned To**: Backend Developer
**Status**: Pending

---

### Task 5.2: Alert Generation & Distribution

**Objective**: Generate context-rich alerts and distribute to appropriate channels.

**Alert Channels**:
- Slack messages (teams)
- Email digests (analysts)
- SIEM integration (alerts system)
- Dashboard real-time feeds
- API webhooks (external systems)

**Alert Rules**:
1. **Critical**: CISA KEV new entry → immediate Slack + email
2. **High**: CVSS 9.0+ + exploit code → within 1 hour
3. **Medium**: Targeted APT campaign → daily digest
4. **Info**: Informational updates → weekly summary

**Deliverables**:
- Alert template system (100+ lines)
- Rule engine
- Channel adapters (Slack, email, SIEM)
- Alert deduplication
- HTML/text email templates

**Success Criteria**:
- All critical alerts sent within 5 minutes
- 100% delivery success rate
- No duplicate alerts
- Proper formatting and context

**Estimated Effort**: 6 hours
**Assigned To**: Backend Developer
**Status**: Pending

---

### Task 5.3: Dashboard & Visualization Integration

**Objective**: Display real-time feeds on executive dashboard.

**Dashboard Components**:
- Recent vulnerability count (24h, 7d, 30d)
- CISA KEV additions (weekly)
- Top exploited vulnerabilities
- Active campaigns targeting sector
- Critical asset impact map
- Threat actor activity heat map

**Deliverables**:
- Dashboard backend APIs (200+ lines)
- Real-time data endpoints
- Aggregation queries
- Performance optimization

**Success Criteria**:
- Dashboard loads <2 seconds
- Real-time updates <30 seconds latency
- Accurate data representation
- No missed events

**Estimated Effort**: 5 hours
**Assigned To**: Frontend Developer
**Status**: Pending

---

## Phase 6: Testing, Documentation & Deployment (Tasks 22-24)

### Task 6.1: Integration Testing & Validation

**Objective**: Comprehensive testing of entire ingestion pipeline.

**Test Scenarios**:
1. **Happy Path**: Data flows from all 6 sources → graph → alerts
2. **Duplicate Handling**: Same CVE from multiple sources → single node
3. **Relationship Creation**: Vulnerability → Technique → Actor
4. **Alert Generation**: Critical severity → alert within 5 min
5. **High Volume**: 1M+ records/day sustained
6. **Failure Recovery**: API down → queue → eventual consistency
7. **Data Validation**: Invalid records rejected → logged

**Deliverables**:
- Integration test suite (300+ lines)
- Load testing framework
- Chaos engineering tests
- Test data sets
- Coverage reports

**Success Criteria**:
- All scenarios pass
- >90% test coverage
- Load test: 1M records/day sustained
- Failure recovery validated

**Estimated Effort**: 8 hours
**Assigned To**: QA Engineer
**Status**: Pending

---

### Task 6.2: Performance Optimization & Monitoring

**Objective**: Optimize for production performance and implement monitoring.

**Performance Targets**:
- API ingestion: <200ms per request
- Graph ingestion: <2s per 100 records
- Alert generation: <5s from event
- Dashboard queries: <2s
- Memory usage: <2GB steady state
- CPU usage: <40% under normal load

**Monitoring**:
- Prometheus metrics
- Grafana dashboards
- Alert rules (latency, errors, queue depth)
- SLA tracking

**Deliverables**:
- Performance test suite (150+ lines)
- Prometheus exporter
- Grafana dashboard JSON
- SLA documentation
- Capacity planning guide

**Success Criteria**:
- All performance targets met
- Metrics collected and visible
- No performance regressions
- Scalability to 10M records/day

**Estimated Effort**: 6 hours
**Assigned To**: DevOps Engineer
**Status**: Pending

---

### Task 6.3: Documentation, Training & Deployment

**Objective**: Complete documentation and prepare for production deployment.

**Documentation**:
- Operator runbooks (emergency procedures)
- API documentation (OpenAPI/Swagger)
- Database schema documentation
- Troubleshooting guide
- Architecture diagrams (C4 model)
- Configuration guide

**Training**:
- Analyst training (using feeds)
- Operator training (maintenance)
- Manager training (dashboard)
- Security training (data handling)

**Deployment**:
- Production checklist
- Deployment automation (CI/CD)
- Rollback procedures
- Monitoring verification
- Load test in staging

**Deliverables**:
- Complete documentation set (500+ lines)
- Training materials (slides, videos)
- Deployment automation (Terraform/Ansible)
- Runbooks for common operations
- Disaster recovery playbook

**Success Criteria**:
- All stakeholders trained
- Documentation complete and current
- Deployment automated and tested
- <30 min RTO for critical failures
- 99.5% availability SLA

**Estimated Effort**: 10 hours
**Assigned To**: Technical Writer + Team
**Status**: Pending

---

## Task Summary

| Phase | Task | Priority | Effort | Status |
|-------|------|----------|--------|--------|
| 1 | API Key Validation | Critical | 4h | Pending |
| 1 | Neo4j Schema | Critical | 6h | Pending |
| 1 | Message Queue | Critical | 5h | Pending |
| 1 | Logging & Audit | High | 5h | Pending |
| 2 | VulnCheck Client | Critical | 8h | Pending |
| 2 | NVD Client | Critical | 7h | Pending |
| 2 | MITRE Integration | High | 6h | Pending |
| 2 | CISA KEV Parser | High | 4h | Pending |
| 2 | STIX/TAXII Client | High | 6h | Pending |
| 2 | Webhook Receivers | High | 5h | Pending |
| 3 | Vuln Normalization | Critical | 5h | Pending |
| 3 | Actor Normalization | High | 4h | Pending |
| 3 | Indicator Normalization | High | 4h | Pending |
| 3 | Deduplication | Critical | 5h | Pending |
| 4 | Neo4j Ingestion | Critical | 6h | Pending |
| 4 | Relationship Enrichment | High | 4h | Pending |
| 4 | Index Management | High | 4h | Pending |
| 4 | Data Validation | High | 4h | Pending |
| 5 | Stream Processing | Critical | 8h | Pending |
| 5 | Alert Generation | Critical | 6h | Pending |
| 5 | Dashboard Integration | High | 5h | Pending |
| 6 | Integration Testing | Critical | 8h | Pending |
| 6 | Performance Optimization | High | 6h | Pending |
| 6 | Documentation & Deploy | High | 10h | Pending |

**Total Effort**: 154 hours
**Team Size**: 6-8 developers
**Timeline**: 4 weeks (assuming 40h/week)
