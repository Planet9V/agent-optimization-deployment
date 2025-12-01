# Threat Intelligence Sources: Frameworks, Standards, and Integration Patterns

**Date:** 2025-10-29
**Version:** 1.0
**Purpose:** Comprehensive guide to threat intelligence frameworks (MITRE ATT&CK), standards (STIX/TAXII), platforms, and integration patterns for cybersecurity systems

---

## 1. MITRE ATT&CK Framework

### 1.1 Framework Overview

The MITRE Adversarial Tactics, Techniques, and Procedures (ATT&CK) framework is a globally accessible knowledge base of adversary tactics and techniques based on real-world observations.

**Core Structure:**
```
Domain (Enterprise, Mobile, ICS)
  ├── Tactic (Initial Access, Execution, Persistence, ...)
  │   ├── Technique (ID: T1234)
  │   │   ├── Sub-technique (ID: T1234.001)
  │   │   ├── Detection methods
  │   │   ├── Mitigations
  │   │   └── Real-world usage examples
  │   └── ...
  └── ...
```

### 1.2 Tactics and Techniques

#### Enterprise ATT&CK Tactics (14 total):

| ID | Tactic | Description | Techniques |
|----|--------|-------------|-----------|
| TA0001 | Initial Access | How attackers get into networks | Phishing, Supply Chain, Drive-by, etc. |
| TA0002 | Execution | How attackers execute code | Command Line, Execution, Scripting |
| TA0003 | Persistence | How attackers maintain access | Account Creation, Backdoor, etc. |
| TA0004 | Privilege Escalation | Gaining higher permissions | Exploitation, UAC Bypass, etc. |
| TA0005 | Defense Evasion | Avoiding detection | Obfuscation, Code Signing, etc. |
| TA0006 | Credential Access | Obtaining credentials | Credential Dumping, Phishing, etc. |
| TA0007 | Discovery | Reconnaissance post-compromise | Account Discovery, System Survey, etc. |
| TA0008 | Lateral Movement | Moving to other systems | Pass-the-Hash, Exploitation, etc. |
| TA0009 | Collection | Gathering data | Data Staged, Clipboard Data, etc. |
| TA0010 | Exfiltration | Moving data out | Exfiltration Over C2, DNS, etc. |
| TA0011 | Command and Control | Communicating with infrastructure | Application Layer Protocol, DNS, etc. |
| TA0040 | Impact | Affecting system/data | Data Destruction, Denial of Service, etc. |
| TA0042 | Resource Development | Establishing resources | Acquire Infrastructure, etc. |
| TA0043 | Reconnaissance | Gathering intelligence pre-attack | Active Scanning, Phishing, etc. |

### 1.3 MITRE ATT&CK Data Model

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Technique:
    """MITRE ATT&CK Technique."""
    id: str  # T1234
    name: str
    tactic: str
    description: str
    detection: List[str]
    mitigation: List[str]
    platforms: List[str]  # Windows, Linux, macOS, etc.
    data_sources: List[str]
    references: List[str]
    created: datetime
    modified: datetime
    sub_techniques: List['SubTechnique'] = None

    def __post_init__(self):
        if self.sub_techniques is None:
            self.sub_techniques = []

@dataclass
class SubTechnique:
    """MITRE ATT&CK Sub-technique."""
    id: str  # T1234.001
    name: str
    parent_technique: str
    description: str
    detection: List[str]
    platforms: List[str]

@dataclass
class Group:
    """Threat actor group in MITRE ATT&CK."""
    id: str  # G0001
    name: str
    aliases: List[str]
    description: str
    associated_techniques: List[str]  # Technique IDs
    associated_software: List[str]
    attack_campaigns: List[str]
    references: List[str]

@dataclass
class Software:
    """Malware/tool in MITRE ATT&CK."""
    id: str  # S0001
    name: str
    platforms: List[str]
    description: str
    techniques: List[str]  # Technique IDs
    used_by: List[str]  # Group IDs
    associated_groups: List[str]
```

### 1.4 Querying MITRE ATT&CK Data

```python
import requests
import json
from typing import List, Dict

class MITREATTACKQuerier:
    """Query MITRE ATT&CK framework data."""

    BASE_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

    def __init__(self):
        self.data = self._load_framework()
        self.objects_by_id = self._index_objects()

    def _load_framework(self) -> Dict:
        """Load MITRE ATT&CK JSON data."""
        response = requests.get(self.BASE_URL)
        return response.json()

    def _index_objects(self) -> Dict:
        """Index objects by ID for fast lookup."""
        index = {}
        for obj in self.data.get('objects', []):
            if 'id' in obj:
                index[obj['id']] = obj
        return index

    def get_techniques_for_tactic(self, tactic: str) -> List[Dict]:
        """Get all techniques for a specific tactic."""
        techniques = []
        for obj in self.data.get('objects', []):
            if obj.get('type') == 'attack-pattern':
                kill_chain_phases = obj.get('kill_chain_phases', [])
                for phase in kill_chain_phases:
                    if phase.get('phase_name') == tactic:
                        techniques.append(obj)
                        break
        return techniques

    def get_group_techniques(self, group_id: str) -> List[Dict]:
        """Get techniques used by a threat group."""
        group = self.objects_by_id.get(group_id)
        if not group:
            return []

        techniques = []
        for relationship in self.data.get('objects', []):
            if (relationship.get('type') == 'relationship' and
                relationship.get('source_ref') == group_id and
                relationship.get('relationship_type') == 'uses'):

                target_id = relationship.get('target_ref')
                target = self.objects_by_id.get(target_id)
                if target and target.get('type') == 'attack-pattern':
                    techniques.append(target)

        return techniques

    def get_software_details(self, software_id: str) -> Dict:
        """Get details about malware/tool."""
        return self.objects_by_id.get(software_id, {})

    def search_techniques_by_platform(self, platform: str) -> List[Dict]:
        """Search techniques available on specific platform."""
        techniques = []
        for obj in self.data.get('objects', []):
            if obj.get('type') == 'attack-pattern':
                x_mitre_platforms = obj.get('x_mitre_platforms', [])
                if platform in x_mitre_platforms:
                    techniques.append(obj)
        return techniques

# Usage
querier = MITREATTACKQuerier()

# Get Initial Access techniques
initial_access = querier.get_techniques_for_tactic('initial-access')
print(f"Initial Access techniques: {len(initial_access)}")

# Get techniques used by APT28
apt28_techniques = querier.get_group_techniques('intrusion-set--7b74cdc5-d82d-4859-ba3f-b2c1c2bcacd7')
print(f"APT28 techniques: {len(apt28_techniques)}")
```

---

## 2. STIX/TAXII Specifications

### 2.1 STIX (Structured Threat Information Expression)

STIX is a standardized language for representing structured threat intelligence.

**STIX Core Objects:**

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class STIXDomainObjectType(Enum):
    """STIX 2.1 Domain Objects."""
    ATTACK_PATTERN = "attack-pattern"
    CAMPAIGN = "campaign"
    COURSE_OF_ACTION = "course-of-action"
    IDENTITY = "identity"
    INDICATOR = "indicator"
    INFRASTRUCTURE = "infrastructure"
    INTRUSION_SET = "intrusion-set"
    MALWARE = "malware"
    TOOL = "tool"
    THREAT_ACTOR = "threat-actor"
    VULNERABILITY = "vulnerability"

@dataclass
class STIXIdentity:
    """STIX Identity object."""
    type: str = "identity"
    id: str = None  # identity--{UUID}
    created: datetime = None
    modified: datetime = None
    name: str = None
    description: Optional[str] = None
    identity_class: str = None  # individual, group, system, organization, class
    sectors: List[str] = None
    contact_information: Optional[str] = None

@dataclass
class STIXMalware:
    """STIX Malware object."""
    type: str = "malware"
    id: str = None
    created: datetime = None
    modified: datetime = None
    name: str = None
    description: Optional[str] = None
    malware_types: List[str] = None  # trojan, worm, ransomware, etc.
    is_family: bool = False
    aliases: List[str] = None
    labels: List[str] = None  # backdoor, remote-access-trojan, etc.
    kill_chain_phases: List[Dict] = None

@dataclass
class STIXIndicator:
    """STIX Indicator object."""
    type: str = "indicator"
    id: str = None
    created: datetime = None
    modified: datetime = None
    pattern: str = None  # Observable pattern
    pattern_type: str = "stix"  # stix, snort, yara, etc.
    valid_from: datetime = None
    valid_until: Optional[datetime] = None
    description: Optional[str] = None
    labels: List[str] = None
    kill_chain_phases: List[Dict] = None

@dataclass
class STIXRelationship:
    """STIX Relationship object."""
    type: str = "relationship"
    id: str = None
    created: datetime = None
    modified: datetime = None
    relationship_type: str = None  # uses, targets, exploits, etc.
    source_ref: str = None  # STIX ID of source object
    target_ref: str = None  # STIX ID of target object
    description: Optional[str] = None
```

### 2.2 STIX Pattern Language (Observable Patterns)

```
STIX patterns define observable objects that can be used for detection.

Syntax: [Object Type]:property [Comparison] value

Examples:
[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']
[ipv4-addr:value = '10.0.0.1']
[domain-name:value = 'malicious.com']
[process:name = 'rundll32.exe']
[windows-registry-key:key = 'HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\Run']

Comparison Operators:
=      (equals)
!=     (not equals)
<      (less than)
>      (greater than)
<=     (less than or equal)
>=     (greater than or equal)
IN     (in list)
NOT IN (not in list)
LIKE   (pattern matching)
MATCHES (regex)

Complex patterns:
[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e' OR file:hashes.SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855']
[process:name = 'rundll32.exe' AND process:parent_ref.name = 'explorer.exe']
```

### 2.3 TAXII (Trusted Automated Exchange of Intelligence Information)

TAXII is a protocol for sharing threat intelligence using STIX objects.

```python
import requests
from typing import List, Dict
import json

class TAXIIClient:
    """Client for TAXII 2.1 protocol."""

    def __init__(self, server_url: str, username: str = None, password: str = None):
        self.server_url = server_url
        self.session = requests.Session()
        if username and password:
            self.session.auth = (username, password)

    def discover_api_root(self) -> Dict:
        """Discover TAXII API root."""
        response = self.session.get(f"{self.server_url}/taxii/")
        response.raise_for_status()
        return response.json()

    def get_collections(self, api_root: str) -> List[Dict]:
        """Get available collections."""
        url = f"{self.server_url}/taxii/api/v21/{api_root}/collections"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get('collections', [])

    def get_objects_from_collection(
        self,
        api_root: str,
        collection_id: str,
        filters: Dict = None
    ) -> List[Dict]:
        """Retrieve STIX objects from collection."""
        url = f"{self.server_url}/taxii/api/v21/{api_root}/collections/{collection_id}/objects"

        params = {}
        if filters:
            if 'type' in filters:
                params['type'] = filters['type']
            if 'added_after' in filters:
                params['added_after'] = filters['added_after'].isoformat()

        response = self.session.get(url, params=params)
        response.raise_for_status()

        return response.json().get('objects', [])

    def push_objects_to_collection(
        self,
        api_root: str,
        collection_id: str,
        objects: List[Dict]
    ) -> Dict:
        """Push STIX objects to collection."""
        url = f"{self.server_url}/taxii/api/v21/{api_root}/collections/{collection_id}/add"

        payload = {
            'objects': objects
        }

        response = self.session.post(
            url,
            json=payload,
            headers={'Content-Type': 'application/stix+json;version=2.1'}
        )
        response.raise_for_status()

        return response.json()

# Usage
client = TAXIIClient("https://cti-taxii.mitre.org")

# Get API roots
api_roots = client.discover_api_root()

# List collections
collections = client.get_collections("default")
for collection in collections:
    print(f"Collection: {collection['title']}")

# Get malware objects
malware_objects = client.get_objects_from_collection(
    "default",
    "bundle--...",
    filters={'type': 'malware'}
)
```

---

## 3. Threat Intelligence Platforms

### 3.1 Open-Source TI Platforms

#### 3.1.1 MISP (Malware Information Sharing Platform)

```python
from pymisp import PyMISP
from datetime import datetime

class MISPIntegration:
    """Integration with MISP threat intelligence platform."""

    def __init__(self, url: str, api_key: str, ssl_verify: bool = True):
        self.misp = PyMISP(url, api_key, ssl_verify=ssl_verify)

    def search_attributes(self, value: str, attribute_type: str = None) -> List[Dict]:
        """Search for attributes in MISP."""
        search_params = {
            'value': value
        }
        if attribute_type:
            search_params['type'] = attribute_type

        result = self.misp.search(
            controller='attributes',
            **search_params
        )

        return result.get('Attribute', [])

    def get_event_details(self, event_id: int) -> Dict:
        """Get details of a MISP event."""
        event = self.misp.get_event(event_id)
        return event.get('Event', {})

    def create_indicator(
        self,
        event_id: int,
        attribute_type: str,
        value: str,
        category: str = "Network activity"
    ) -> Dict:
        """Create new indicator in MISP."""
        attribute = {
            'type': attribute_type,
            'value': value,
            'category': category
        }

        result = self.misp.add_attribute(event_id, attribute)
        return result

    def publish_event(self, event_id: int) -> Dict:
        """Publish event to MISP."""
        result = self.misp.publish(event_id)
        return result
```

#### 3.1.2 OpenTIE (Open Threat Intelligence Engine)

```python
class OpenTIEIntegration:
    """Integration with OpenTIE threat intelligence."""

    API_BASE = "https://api.opentie.io/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({'X-API-Key': api_key})

    def lookup_indicator(self, indicator: str, indicator_type: str) -> Dict:
        """Look up indicator in OpenTIE."""
        url = f"{self.API_BASE}/indicators/{indicator_type}/{indicator}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def submit_indicator(
        self,
        indicator: str,
        indicator_type: str,
        confidence: float,
        source: str
    ) -> Dict:
        """Submit new indicator to OpenTIE."""
        url = f"{self.API_BASE}/indicators"

        payload = {
            'indicator': indicator,
            'type': indicator_type,
            'confidence': confidence,
            'source': source
        }

        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
```

### 3.2 Commercial TI Platforms

**Notable Commercial Platforms:**
- **Recorded Future**: AI-powered threat intelligence
- **Mandiant Advantage**: Google-backed threat intelligence
- **CrowdStrike Falcon**: Real-time threat intelligence
- **Trend Micro XDR**: Integrated threat intelligence
- **Palo Alto Networks Unit42**: Industry research and intelligence

---

## 4. Integration Patterns

### 4.1 Multi-Source Threat Intelligence Aggregator

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Set
from datetime import datetime
from enum import Enum

class TISourceType(Enum):
    """Types of threat intelligence sources."""
    MISP = "misp"
    TAXII = "taxii"
    FEED_JSON = "feed_json"
    CUSTOM_API = "custom_api"

class TISource(ABC):
    """Abstract base for threat intelligence source."""

    @abstractmethod
    def fetch_indicators(self) -> List[Dict]:
        """Fetch indicators from source."""
        pass

    @abstractmethod
    def normalize_indicator(self, indicator: Dict) -> Dict:
        """Normalize indicator to standard format."""
        pass

class TIAggregator:
    """Aggregate threat intelligence from multiple sources."""

    def __init__(self):
        self.sources: Dict[str, TISource] = {}
        self.indicators: Set[str] = set()
        self.last_update = None

    def add_source(self, name: str, source: TISource):
        """Add threat intelligence source."""
        self.sources[name] = source

    def aggregate(self) -> List[Dict]:
        """Aggregate indicators from all sources."""
        aggregated = []
        seen_indicators = {}

        for source_name, source in self.sources.items():
            try:
                indicators = source.fetch_indicators()

                for indicator in indicators:
                    normalized = source.normalize_indicator(indicator)
                    indicator_value = normalized.get('value')

                    if indicator_value in seen_indicators:
                        # Merge with existing
                        existing = seen_indicators[indicator_value]
                        existing['sources'].append(source_name)
                        existing['confidence'] = max(
                            existing['confidence'],
                            normalized.get('confidence', 0)
                        )
                    else:
                        # New indicator
                        normalized['sources'] = [source_name]
                        seen_indicators[indicator_value] = normalized
                        aggregated.append(normalized)

            except Exception as e:
                print(f"Error fetching from {source_name}: {e}")

        self.last_update = datetime.now()
        return aggregated

    def get_high_confidence_indicators(self, min_confidence: float = 0.8) -> List[Dict]:
        """Get indicators above confidence threshold."""
        all_indicators = self.aggregate()
        return [
            ind for ind in all_indicators
            if ind.get('confidence', 0) >= min_confidence
        ]

    def detect_consensus_indicators(self, min_sources: int = 3) -> List[Dict]:
        """Indicators reported by multiple sources (more reliable)."""
        all_indicators = self.aggregate()
        return [
            ind for ind in all_indicators
            if len(ind.get('sources', [])) >= min_sources
        ]
```

### 4.2 Graph Integration Pattern

```python
from neo4j import GraphDatabase
from typing import List, Dict

class TIGraphIntegrator:
    """Integrate threat intelligence into knowledge graph."""

    def __init__(self, uri: str, username: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def ingest_indicators(self, indicators: List[Dict]):
        """Ingest threat indicators into graph."""
        with self.driver.session() as session:
            for indicator in indicators:
                self._create_indicator_nodes(session, indicator)

    def _create_indicator_nodes(self, session, indicator: Dict):
        """Create indicator nodes and relationships."""
        indicator_type = indicator.get('type')
        indicator_value = indicator.get('value')

        # Create indicator node
        session.run("""
            MERGE (i:{type} {{value: $value}})
            SET i.confidence = $confidence,
                i.first_seen = $first_seen,
                i.last_seen = $last_seen
        """.format(type=indicator_type), {
            'value': indicator_value,
            'confidence': indicator.get('confidence', 0),
            'first_seen': indicator.get('first_seen'),
            'last_seen': indicator.get('last_seen')
        })

        # Create relationships to threat sources
        for threat in indicator.get('threats', []):
            session.run("""
                MATCH (i:{type} {{value: $value}})
                MERGE (t:Threat {{name: $threat}})
                CREATE (i)-[:ASSOCIATED_WITH]->(t)
            """.format(type=indicator_type), {
                'value': indicator_value,
                'threat': threat
            })

        # Create relationships to MITRE ATT&CK techniques
        for technique in indicator.get('techniques', []):
            session.run("""
                MATCH (i:{type} {{value: $value}})
                MERGE (t:Technique {{technique_id: $technique}})
                CREATE (i)-[:USED_IN]->(t)
            """.format(type=indicator_type), {
                'value': indicator_value,
                'technique': technique
            })
```

---

## References

MITRE ATT&CK Team. (2024). *MITRE ATT&CK framework*. Retrieved from https://attack.mitre.org

MITRE Corporation. (2024). *STIX 2.1 specification*. Retrieved from https://docs.oasis-open.org/cti/stix/v2.1/

OASIS. (2024). *TAXII 2.1 specification*. Retrieved from https://docs.oasis-open.org/cti/taxii/v2.1/

Wagner, C., & Dulaunoy, A. (2016). *MISP: The design and implementation of a collaborative threat intelligence platform*. Proceedings of the 2016 ACM Workshop on Information Sharing and Collaborative Security.

Barnum, S. (2012). Standardizing cyber threat intelligence information with the Structured Threat Information Expression (STIX). *MITRE Corporation White Paper*, 11, 1-11.

Stites, R., & Meissner, R. (2015). *Cyber threat intelligence and the classification of incidents: An empirical assessment*. Journal of Cybersecurity, 1(1), 35-46.
