# Integration Specifications - AEON Cyber DT v3.0

**File**: 05_INTEGRATION_SPECS_v3.0_2025-11-19.md
**Created**: 2025-11-19 11:47:00 UTC
**Modified**: 2025-11-19 11:47:00 UTC
**Version**: v3.0.0
**Author**: AEON Architecture Team
**Purpose**: Complete integration specifications for NER10, MITRE, CVE feeds, and external systems
**Status**: ACTIVE

## Document Overview

This document provides comprehensive integration specifications for AEON Cyber Digital Twin v3.0, detailing all external system integrations, data pipelines, and synchronization mechanisms.

---

## Integration Architecture

### Integration Layers
1. **Data Ingestion Layer**: External feed consumption (CVE, MITRE, CAPEC, CWE)
2. **NER10 Integration Layer**: Named Entity Recognition and knowledge extraction
3. **CMDB/Asset Integration Layer**: IT asset inventory synchronization
4. **SIEM Integration Layer**: Security event correlation
5. **Threat Intelligence Platform (TIP) Layer**: IOC and threat data exchange
6. **Workflow Integration Layer**: Ticketing, notification, orchestration

### Technology Stack
- **Message Queue**: Apache Kafka / RabbitMQ
- **ETL/Data Pipeline**: Apache Airflow / Prefect
- **API Gateway**: Kong / AWS API Gateway
- **Data Validation**: JSON Schema / Pydantic
- **Transformation**: Apache NiFi / custom Python
- **Monitoring**: Prometheus + Grafana

---

## NER10 Integration

### Overview
NER10 (Named Entity Recognition v10) extracts entities, relationships, and semantic information from unstructured cybersecurity text.

### Integration Architecture

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────┐
│ Unstructured    │────────▶│   NER10      │────────▶│   Neo4j     │
│ Text Sources    │         │   Pipeline   │         │   Graph     │
└─────────────────┘         └──────────────┘         └─────────────┘
     │                            │                         │
     ├─ CVE Descriptions          ├─ Entity Extraction     ├─ Node Creation
     ├─ Security Reports          ├─ Relationship Mapping  ├─ Relationship Creation
     ├─ Threat Intel Reports      ├─ Semantic Analysis     ├─ Property Enrichment
     └─ Incident Reports          └─ Confidence Scoring    └─ Validation
```

### NER10 API Specification

#### Extract Entities from Text
```http
POST /ner10/extract
Content-Type: application/json
Authorization: Bearer {apiKey}

Request:
{
  "text": "APT29 exploited CVE-2024-1234 using phishing emails to target government entities...",
  "options": {
    "entityTypes": ["ThreatActor", "CVE", "AttackPattern", "TargetOrganization"],
    "includeRelationships": true,
    "confidenceThreshold": 0.7,
    "contextWindow": 5
  }
}

Response 200 OK:
{
  "entities": [
    {
      "entityId": "ent-uuid-1",
      "text": "APT29",
      "entityType": "ThreatActor",
      "confidence": 0.95,
      "startOffset": 0,
      "endOffset": 5,
      "metadata": {
        "aliases": ["Cozy Bear", "The Dukes"],
        "actorType": "NATION_STATE"
      }
    },
    {
      "entityId": "ent-uuid-2",
      "text": "CVE-2024-1234",
      "entityType": "CVE",
      "confidence": 0.99,
      "startOffset": 16,
      "endOffset": 29,
      "metadata": {
        "cveId": "CVE-2024-1234"
      }
    },
    {
      "entityId": "ent-uuid-3",
      "text": "phishing emails",
      "entityType": "AttackPattern",
      "confidence": 0.88,
      "startOffset": 36,
      "endOffset": 51,
      "metadata": {
        "mitreTechniqueId": "T1566",
        "techniqueName": "Phishing"
      }
    },
    {
      "entityId": "ent-uuid-4",
      "text": "government entities",
      "entityType": "TargetOrganization",
      "confidence": 0.82,
      "startOffset": 62,
      "endOffset": 81,
      "metadata": {
        "organizationType": "GOVERNMENT"
      }
    }
  ],
  "relationships": [
    {
      "relationshipId": "rel-uuid-1",
      "sourceEntityId": "ent-uuid-1",
      "targetEntityId": "ent-uuid-2",
      "relationshipType": "EXPLOITS",
      "confidence": 0.91,
      "evidence": "APT29 exploited CVE-2024-1234"
    },
    {
      "relationshipId": "rel-uuid-2",
      "sourceEntityId": "ent-uuid-1",
      "targetEntityId": "ent-uuid-3",
      "relationshipType": "USES_TECHNIQUE",
      "confidence": 0.87,
      "evidence": "using phishing emails"
    },
    {
      "relationshipId": "rel-uuid-3",
      "sourceEntityId": "ent-uuid-1",
      "targetEntityId": "ent-uuid-4",
      "relationshipType": "TARGETS",
      "confidence": 0.84,
      "evidence": "target government entities"
    }
  ],
  "processingTime": 234,
  "modelVersion": "ner10-cyber-v2.5.0"
}
```

### NER10 to Neo4j Mapping

#### Entity Mapping Configuration
```yaml
entity_mappings:
  ThreatActor:
    neo4j_label: ThreatActor
    property_mappings:
      text: name
      metadata.aliases: aliases
      metadata.actorType: actorType
      confidence: ner_confidence
    additional_properties:
      dataSource: "NER10"
      extractedAt: "{{timestamp}}"

  CVE:
    neo4j_label: CVE
    property_mappings:
      metadata.cveId: cveId
      text: description_snippet
      confidence: ner_confidence
    merge_strategy: MATCH_ON_CVE_ID
    enrich_from_nvd: true

  AttackPattern:
    neo4j_label: MitreTechnique
    property_mappings:
      metadata.mitreTechniqueId: techniqueId
      metadata.techniqueName: name
      confidence: ner_confidence
    merge_strategy: MATCH_ON_TECHNIQUE_ID

  TargetOrganization:
    neo4j_label: Organization
    property_mappings:
      text: name
      metadata.organizationType: type
      confidence: ner_confidence
    merge_strategy: FUZZY_MATCH_ON_NAME
```

#### Relationship Mapping Configuration
```yaml
relationship_mappings:
  EXPLOITS:
    neo4j_relationship: EXPLOITS
    property_mappings:
      confidence: confidence_score
      evidence: evidence_text
    additional_properties:
      source: "NER10"
      extractedAt: "{{timestamp}}"

  USES_TECHNIQUE:
    neo4j_relationship: USES_TECHNIQUE
    property_mappings:
      confidence: confidence_score
      evidence: evidence_text
    additional_properties:
      source: "NER10"
      observedDate: "{{timestamp}}"

  TARGETS:
    neo4j_relationship: TARGETS
    property_mappings:
      confidence: confidence_score
      evidence: evidence_text
    additional_properties:
      source: "NER10"
      targetingDate: "{{timestamp}}"
```

### NER10 Processing Pipeline

```python
# Airflow DAG: NER10 Processing Pipeline
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'aeon-data',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'ner10_extraction_pipeline',
    default_args=default_args,
    description='Extract entities from cybersecurity reports using NER10',
    schedule_interval='0 */6 * * *',  # Every 6 hours
    catchup=False
)

def fetch_unprocessed_reports(**context):
    """Fetch reports pending NER10 processing"""
    # Query Neo4j for reports without NER processing
    # Return list of report IDs
    pass

def extract_entities(**context):
    """Call NER10 API to extract entities"""
    reports = context['task_instance'].xcom_pull(task_ids='fetch_reports')
    results = []
    for report in reports:
        response = requests.post(
            'http://ner10-service/extract',
            json={
                'text': report['content'],
                'options': {
                    'entityTypes': ['ThreatActor', 'CVE', 'AttackPattern'],
                    'confidenceThreshold': 0.7
                }
            }
        )
        results.append(response.json())
    return results

def validate_entities(**context):
    """Validate extracted entities against schema"""
    entities = context['task_instance'].xcom_pull(task_ids='extract_entities')
    validated = []
    for entity_set in entities:
        # Validate against JSON schema
        # Filter by confidence threshold
        # Deduplicate entities
        validated.append(entity_set)
    return validated

def create_neo4j_nodes(**context):
    """Create Neo4j nodes from extracted entities"""
    entities = context['task_instance'].xcom_pull(task_ids='validate_entities')
    for entity_set in entities:
        for entity in entity_set['entities']:
            # Map entity to Neo4j node
            # Create or merge node
            # Set properties
            pass

def create_neo4j_relationships(**context):
    """Create Neo4j relationships from extracted relationships"""
    entities = context['task_instance'].xcom_pull(task_ids='validate_entities')
    for entity_set in entities:
        for relationship in entity_set['relationships']:
            # Map relationship to Neo4j relationship
            # Create relationship between nodes
            # Set properties
            pass

def enrich_from_external_sources(**context):
    """Enrich extracted entities with external data"""
    # For CVEs: fetch from NVD
    # For Threat Actors: fetch from threat intel feeds
    # For MITRE Techniques: fetch from ATT&CK framework
    pass

# Define task dependencies
fetch_reports = PythonOperator(
    task_id='fetch_reports',
    python_callable=fetch_unprocessed_reports,
    dag=dag
)

extract = PythonOperator(
    task_id='extract_entities',
    python_callable=extract_entities,
    dag=dag
)

validate = PythonOperator(
    task_id='validate_entities',
    python_callable=validate_entities,
    dag=dag
)

create_nodes = PythonOperator(
    task_id='create_neo4j_nodes',
    python_callable=create_neo4j_nodes,
    dag=dag
)

create_rels = PythonOperator(
    task_id='create_neo4j_relationships',
    python_callable=create_neo4j_relationships,
    dag=dag
)

enrich = PythonOperator(
    task_id='enrich_from_external',
    python_callable=enrich_from_external_sources,
    dag=dag
)

# Pipeline flow
fetch_reports >> extract >> validate >> [create_nodes, create_rels] >> enrich
```

---

## MITRE ATT&CK Integration

### Overview
Synchronize MITRE ATT&CK framework data (Tactics, Techniques, Sub-Techniques) into Neo4j.

### Data Source
- **MITRE ATT&CK STIX**: https://github.com/mitre/cti
- **Format**: STIX 2.1 JSON
- **Update Frequency**: Weekly (official releases)

### Integration Pipeline

```python
# Airflow DAG: MITRE ATT&CK Sync
dag = DAG(
    'mitre_attack_sync',
    default_args=default_args,
    description='Synchronize MITRE ATT&CK framework data',
    schedule_interval='0 2 * * 0',  # Weekly on Sunday at 2 AM
    catchup=False
)

def fetch_attack_data(**context):
    """Fetch latest MITRE ATT&CK data from GitHub"""
    import requests

    matrices = ['enterprise-attack', 'mobile-attack', 'ics-attack']
    data = {}

    for matrix in matrices:
        url = f'https://raw.githubusercontent.com/mitre/cti/master/{matrix}/{matrix}.json'
        response = requests.get(url)
        data[matrix] = response.json()

    return data

def parse_tactics(**context):
    """Parse tactics from STIX data"""
    attack_data = context['task_instance'].xcom_pull(task_ids='fetch_attack_data')
    tactics = []

    for matrix, data in attack_data.items():
        for obj in data['objects']:
            if obj['type'] == 'x-mitre-tactic':
                tactics.append({
                    'id': obj['id'],
                    'tacticId': obj['external_references'][0]['external_id'],
                    'name': obj['name'],
                    'description': obj['description'],
                    'matrix': matrix.replace('-attack', '').upper(),
                    'url': obj['external_references'][0]['url']
                })

    return tactics

def parse_techniques(**context):
    """Parse techniques and sub-techniques from STIX data"""
    attack_data = context['task_instance'].xcom_pull(task_ids='fetch_attack_data')
    techniques = []

    for matrix, data in attack_data.items():
        for obj in data['objects']:
            if obj['type'] == 'attack-pattern':
                is_subtechnique = '.' in obj['external_references'][0]['external_id']

                technique = {
                    'id': obj['id'],
                    'techniqueId': obj['external_references'][0]['external_id'],
                    'name': obj['name'],
                    'description': obj['description'],
                    'matrix': matrix.replace('-attack', '').upper(),
                    'isSubTechnique': is_subtechnique,
                    'url': obj['external_references'][0]['url']
                }

                # Parse parent technique for sub-techniques
                if is_subtechnique:
                    parent_id = obj['external_references'][0]['external_id'].split('.')[0]
                    technique['parentTechniqueId'] = parent_id

                # Parse data sources
                if 'x_mitre_data_sources' in obj:
                    technique['dataSourcesRequired'] = obj['x_mitre_data_sources']

                # Parse platforms
                if 'x_mitre_platforms' in obj:
                    technique['platforms'] = obj['x_mitre_platforms']

                # Parse detection
                if 'x_mitre_detection' in obj:
                    technique['detectionMethods'] = [obj['x_mitre_detection']]

                techniques.append(technique)

    return techniques

def create_mitre_nodes(**context):
    """Create MITRE nodes in Neo4j"""
    from neo4j import GraphDatabase

    tactics = context['task_instance'].xcom_pull(task_ids='parse_tactics')
    techniques = context['task_instance'].xcom_pull(task_ids='parse_techniques')

    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))

    with driver.session() as session:
        # Create tactics
        for tactic in tactics:
            session.run("""
                MERGE (t:MitreTactic {tacticId: $tacticId})
                SET t.id = $id,
                    t.name = $name,
                    t.description = $description,
                    t.matrix = $matrix,
                    t.url = $url,
                    t.updatedAt = datetime()
            """, **tactic)

        # Create techniques
        for technique in techniques:
            session.run("""
                MERGE (t:MitreTechnique {techniqueId: $techniqueId})
                SET t.id = $id,
                    t.name = $name,
                    t.description = $description,
                    t.matrix = $matrix,
                    t.isSubTechnique = $isSubTechnique,
                    t.url = $url,
                    t.updatedAt = datetime()
            """, **{k: v for k, v in technique.items() if k not in ['dataSourcesRequired', 'platforms', 'detectionMethods', 'parentTechniqueId']})

            # Set array properties
            if 'dataSourcesRequired' in technique:
                session.run("""
                    MATCH (t:MitreTechnique {techniqueId: $techniqueId})
                    SET t.dataSourcesRequired = $dataSourcesRequired
                """, techniqueId=technique['techniqueId'], dataSourcesRequired=technique['dataSourcesRequired'])

    driver.close()

def create_mitre_relationships(**context):
    """Create MITRE relationships in Neo4j"""
    from neo4j import GraphDatabase

    techniques = context['task_instance'].xcom_pull(task_ids='parse_techniques')
    attack_data = context['task_instance'].xcom_pull(task_ids='fetch_attack_data')

    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))

    with driver.session() as session:
        # Create PART_OF relationships (Technique -> Tactic)
        for matrix, data in attack_data.items():
            for obj in data['objects']:
                if obj['type'] == 'relationship' and obj['relationship_type'] == 'uses':
                    # Parse kill chain phase to get tactic
                    if 'kill_chain_phases' in obj:
                        for phase in obj['kill_chain_phases']:
                            session.run("""
                                MATCH (tech:MitreTechnique {id: $source_ref})
                                MATCH (tac:MitreTactic {name: $tactic_name})
                                MERGE (tech)-[r:PART_OF]->(tac)
                                SET r.matrix = $matrix
                            """, source_ref=obj['source_ref'],
                                 tactic_name=phase['phase_name'].replace('-', ' ').title(),
                                 matrix=matrix.replace('-attack', '').upper())

        # Create SUBTECHNIQUE_OF relationships
        for technique in techniques:
            if technique.get('isSubTechnique') and 'parentTechniqueId' in technique:
                session.run("""
                    MATCH (sub:MitreTechnique {techniqueId: $subTechniqueId})
                    MATCH (parent:MitreTechnique {techniqueId: $parentTechniqueId})
                    MERGE (sub)-[r:SUBTECHNIQUE_OF]->(parent)
                """, subTechniqueId=technique['techniqueId'],
                     parentTechniqueId=technique['parentTechniqueId'])

    driver.close()

# Task definitions
fetch_data = PythonOperator(task_id='fetch_attack_data', python_callable=fetch_attack_data, dag=dag)
parse_tac = PythonOperator(task_id='parse_tactics', python_callable=parse_tactics, dag=dag)
parse_tech = PythonOperator(task_id='parse_techniques', python_callable=parse_techniques, dag=dag)
create_nodes = PythonOperator(task_id='create_mitre_nodes', python_callable=create_mitre_nodes, dag=dag)
create_rels = PythonOperator(task_id='create_mitre_relationships', python_callable=create_mitre_relationships, dag=dag)

# Pipeline
fetch_data >> [parse_tac, parse_tech] >> create_nodes >> create_rels
```

---

## CVE/NVD Feed Integration

### Overview
Synchronize CVE vulnerability data from National Vulnerability Database (NVD).

### Data Source
- **NVD API**: https://nvd.nist.gov/developers/vulnerabilities
- **API Version**: 2.0
- **Rate Limit**: 5 requests per 30 seconds (without API key), 50 requests per 30 seconds (with API key)
- **Update Frequency**: Every 2 hours (incremental), daily (full sync)

### NVD API Integration

```python
import requests
import time
from datetime import datetime, timedelta

class NVDClient:
    def __init__(self, api_key=None):
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.api_key = api_key
        self.rate_limit_delay = 0.2 if api_key else 6  # seconds between requests

    def fetch_cves(self, last_modified_start=None, last_modified_end=None, results_per_page=2000):
        """Fetch CVEs modified within a time range"""
        params = {
            'resultsPerPage': results_per_page,
            'startIndex': 0
        }

        if last_modified_start:
            params['lastModStartDate'] = last_modified_start.isoformat() + 'Z'
        if last_modified_end:
            params['lastModEndDate'] = last_modified_end.isoformat() + 'Z'

        headers = {}
        if self.api_key:
            headers['apiKey'] = self.api_key

        all_cves = []

        while True:
            time.sleep(self.rate_limit_delay)

            response = requests.get(self.base_url, params=params, headers=headers)
            response.raise_for_status()

            data = response.json()
            vulnerabilities = data.get('vulnerabilities', [])

            for vuln in vulnerabilities:
                cve_data = vuln['cve']
                all_cves.append(self._parse_cve(cve_data))

            # Check if more results exist
            total_results = data.get('totalResults', 0)
            current_index = params['startIndex']

            if current_index + results_per_page >= total_results:
                break

            params['startIndex'] += results_per_page

        return all_cves

    def _parse_cve(self, cve_data):
        """Parse CVE data from NVD format"""
        cve_id = cve_data['id']

        # Extract description
        descriptions = cve_data.get('descriptions', [])
        description = next((d['value'] for d in descriptions if d['lang'] == 'en'), '')

        # Extract CVSS scores
        metrics = cve_data.get('metrics', {})
        cvss_v3 = None
        cvss_v2 = None

        if 'cvssMetricV31' in metrics and len(metrics['cvssMetricV31']) > 0:
            cvss_v3 = metrics['cvssMetricV31'][0]['cvssData']
        elif 'cvssMetricV30' in metrics and len(metrics['cvssMetricV30']) > 0:
            cvss_v3 = metrics['cvssMetricV30'][0]['cvssData']

        if 'cvssMetricV2' in metrics and len(metrics['cvssMetricV2']) > 0:
            cvss_v2 = metrics['cvssMetricV2'][0]['cvssData']

        # Extract CWE IDs
        cwe_ids = []
        weaknesses = cve_data.get('weaknesses', [])
        for weakness in weaknesses:
            for desc in weakness.get('description', []):
                if desc['lang'] == 'en':
                    cwe_ids.append(desc['value'])

        # Extract references
        references = [ref['url'] for ref in cve_data.get('references', [])]

        # Build CVE object
        cve_obj = {
            'cveId': cve_id,
            'description': description,
            'publishedDate': cve_data['published'],
            'lastModifiedDate': cve_data['lastModified'],
            'status': cve_data.get('vulnStatus', 'UNKNOWN'),
            'cweIds': cwe_ids,
            'references': references
        }

        # Add CVSS v3 if available
        if cvss_v3:
            cve_obj.update({
                'cvssV3Score': cvss_v3['baseScore'],
                'cvssV3Vector': cvss_v3['vectorString'],
                'baseSeverity': cvss_v3['baseSeverity'],
                'attackVector': cvss_v3['attackVector'],
                'attackComplexity': cvss_v3['attackComplexity'],
                'privilegesRequired': cvss_v3['privilegesRequired'],
                'userInteraction': cvss_v3['userInteraction'],
                'scope': cvss_v3['scope'],
                'confidentialityImpact': cvss_v3['confidentialityImpact'],
                'integrityImpact': cvss_v3['integrityImpact'],
                'availabilityImpact': cvss_v3['availabilityImpact']
            })

        # Add CVSS v2 if available
        if cvss_v2:
            cve_obj.update({
                'cvssV2Score': cvss_v2['baseScore'],
                'cvssV2Vector': cvss_v2['vectorString']
            })

        return cve_obj

# Airflow DAG: NVD Sync
dag = DAG(
    'nvd_cve_sync',
    default_args=default_args,
    description='Synchronize CVE data from NVD',
    schedule_interval='0 */2 * * *',  # Every 2 hours
    catchup=False
)

def fetch_nvd_cves(**context):
    """Fetch CVEs from NVD API"""
    nvd_client = NVDClient(api_key=os.getenv('NVD_API_KEY'))

    # Get last sync timestamp from Neo4j or XCom
    last_sync = context['task_instance'].xcom_pull(task_ids='get_last_sync_time')
    if not last_sync:
        last_sync = datetime.now() - timedelta(days=7)  # Default: last 7 days

    cves = nvd_client.fetch_cves(
        last_modified_start=last_sync,
        last_modified_end=datetime.now()
    )

    return cves

def create_cve_nodes(**context):
    """Create CVE nodes in Neo4j"""
    from neo4j import GraphDatabase

    cves = context['task_instance'].xcom_pull(task_ids='fetch_nvd_cves')

    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))

    with driver.session() as session:
        for cve in cves:
            session.run("""
                MERGE (c:CVE {cveId: $cveId})
                SET c.id = coalesce(c.id, randomUUID()),
                    c.description = $description,
                    c.publishedDate = datetime($publishedDate),
                    c.lastModifiedDate = datetime($lastModifiedDate),
                    c.status = $status,
                    c.cvssV3Score = $cvssV3Score,
                    c.cvssV3Vector = $cvssV3Vector,
                    c.baseSeverity = $baseSeverity,
                    c.attackVector = $attackVector,
                    c.attackComplexity = $attackComplexity,
                    c.privilegesRequired = $privilegesRequired,
                    c.userInteraction = $userInteraction,
                    c.scope = $scope,
                    c.confidentialityImpact = $confidentialityImpact,
                    c.integrityImpact = $integrityImpact,
                    c.availabilityImpact = $availabilityImpact,
                    c.references = $references,
                    c.dataSource = 'NVD',
                    c.lastSyncDate = datetime(),
                    c.updatedAt = datetime()
            """, **cve)

            # Create relationships to CWEs
            for cwe_id in cve.get('cweIds', []):
                session.run("""
                    MATCH (c:CVE {cveId: $cveId})
                    MERGE (w:CWE {cweId: $cweId})
                    MERGE (c)-[r:EXPLOITS]->(w)
                    SET r.source = 'NVD',
                        r.createdAt = coalesce(r.createdAt, datetime()),
                        r.updatedAt = datetime()
                """, cveId=cve['cveId'], cweId=cwe_id)

    driver.close()

# Task definitions
get_last_sync = PythonOperator(task_id='get_last_sync_time', python_callable=lambda: datetime.now() - timedelta(hours=2), dag=dag)
fetch_cves = PythonOperator(task_id='fetch_nvd_cves', python_callable=fetch_nvd_cves, dag=dag)
create_nodes = PythonOperator(task_id='create_cve_nodes', python_callable=create_cve_nodes, dag=dag)

# Pipeline
get_last_sync >> fetch_cves >> create_nodes
```

---

## CMDB/Asset Integration

### Overview
Synchronize IT asset inventory from Configuration Management Database (CMDB) systems.

### Supported CMDB Systems
- ServiceNow CMDB
- BMC Remedy
- Jira Assets (Insight)
- AWS Config
- Azure Resource Graph
- Custom CMDB via REST API

### ServiceNow Integration Example

```python
class ServiceNowCMDBClient:
    def __init__(self, instance, username, password):
        self.base_url = f"https://{instance}.service-now.com/api/now/table"
        self.auth = (username, password)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def fetch_assets(self, asset_class='cmdb_ci_server', limit=1000, offset=0):
        """Fetch assets from ServiceNow CMDB"""
        url = f"{self.base_url}/{asset_class}"
        params = {
            'sysparm_limit': limit,
            'sysparm_offset': offset,
            'sysparm_display_value': 'true'
        }

        response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()['result']

    def map_to_aeon_asset(self, snow_asset):
        """Map ServiceNow asset to AEON asset format"""
        return {
            'assetId': snow_asset['sys_id'],
            'name': snow_asset.get('name', ''),
            'assetType': self._map_asset_type(snow_asset.get('sys_class_name', '')),
            'criticality': self._map_criticality(snow_asset.get('criticality', '')),
            'status': 'ACTIVE' if snow_asset.get('operational_status') == '1' else 'INACTIVE',
            'ipAddress': snow_asset.get('ip_address', ''),
            'hostname': snow_asset.get('host_name', ''),
            'department': snow_asset.get('department', {}).get('value', ''),
            'location': snow_asset.get('location', {}).get('value', ''),
            'operatingSystem': snow_asset.get('os', ''),
            'osVersion': snow_asset.get('os_version', ''),
            'manufacturer': snow_asset.get('manufacturer', {}).get('value', ''),
            'model': snow_asset.get('model_id', {}).get('value', ''),
            'serialNumber': snow_asset.get('serial_number', ''),
            'discoverySource': 'ServiceNow',
            'lastDiscoveryDate': datetime.now().isoformat()
        }

    def _map_asset_type(self, snow_class):
        mapping = {
            'cmdb_ci_server': 'SERVER',
            'cmdb_ci_computer': 'WORKSTATION',
            'cmdb_ci_netgear': 'NETWORK_DEVICE',
            'cmdb_ci_database': 'DATABASE',
            'cmdb_ci_appl': 'APPLICATION'
        }
        return mapping.get(snow_class, 'UNKNOWN')

    def _map_criticality(self, snow_criticality):
        mapping = {
            '1': 'CRITICAL',
            '2': 'HIGH',
            '3': 'MEDIUM',
            '4': 'LOW'
        }
        return mapping.get(snow_criticality, 'MEDIUM')

# Airflow DAG: CMDB Asset Sync
dag = DAG(
    'cmdb_asset_sync',
    default_args=default_args,
    description='Synchronize assets from ServiceNow CMDB',
    schedule_interval='0 */4 * * *',  # Every 4 hours
    catchup=False
)

def fetch_cmdb_assets(**context):
    """Fetch assets from ServiceNow CMDB"""
    client = ServiceNowCMDBClient(
        instance=os.getenv('SNOW_INSTANCE'),
        username=os.getenv('SNOW_USERNAME'),
        password=os.getenv('SNOW_PASSWORD')
    )

    asset_classes = ['cmdb_ci_server', 'cmdb_ci_computer', 'cmdb_ci_netgear']
    all_assets = []

    for asset_class in asset_classes:
        snow_assets = client.fetch_assets(asset_class=asset_class)
        for snow_asset in snow_assets:
            aeon_asset = client.map_to_aeon_asset(snow_asset)
            all_assets.append(aeon_asset)

    return all_assets

def sync_assets_to_neo4j(**context):
    """Sync assets to Neo4j"""
    from neo4j import GraphDatabase

    assets = context['task_instance'].xcom_pull(task_ids='fetch_cmdb_assets')

    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))

    with driver.session() as session:
        for asset in assets:
            session.run("""
                MERGE (a:Asset {assetId: $assetId})
                SET a.id = coalesce(a.id, randomUUID()),
                    a.name = $name,
                    a.assetType = $assetType,
                    a.criticality = $criticality,
                    a.status = $status,
                    a.ipAddress = $ipAddress,
                    a.hostname = $hostname,
                    a.department = $department,
                    a.location = $location,
                    a.operatingSystem = $operatingSystem,
                    a.osVersion = $osVersion,
                    a.manufacturer = $manufacturer,
                    a.model = $model,
                    a.serialNumber = $serialNumber,
                    a.discoverySource = $discoverySource,
                    a.lastDiscoveryDate = datetime($lastDiscoveryDate),
                    a.updatedAt = datetime()
            """, **asset)

    driver.close()

# Task definitions
fetch_assets = PythonOperator(task_id='fetch_cmdb_assets', python_callable=fetch_cmdb_assets, dag=dag)
sync_assets = PythonOperator(task_id='sync_assets_to_neo4j', python_callable=sync_assets_to_neo4j, dag=dag)

# Pipeline
fetch_assets >> sync_assets
```

---

## SIEM Integration

### Overview
Integrate with Security Information and Event Management (SIEM) systems for alert correlation and incident response.

### Supported SIEM Platforms
- Splunk
- IBM QRadar
- ArcSight
- LogRhythm
- Elastic Security
- Microsoft Sentinel

### Integration Capabilities
- Alert ingestion
- IOC enrichment
- Asset context lookup
- Automated playbook execution
- Bi-directional synchronization

### Splunk Integration Example

```python
import splunklib.client as client
import splunklib.results as results

class SplunkIntegration:
    def __init__(self, host, port, username, password):
        self.service = client.connect(
            host=host,
            port=port,
            username=username,
            password=password
        )

    def search_alerts(self, search_query, earliest_time='-24h', latest_time='now'):
        """Search Splunk for security alerts"""
        job = self.service.jobs.create(
            search_query,
            earliest_time=earliest_time,
            latest_time=latest_time
        )

        # Wait for job to complete
        while not job.is_done():
            time.sleep(1)

        # Retrieve results
        alerts = []
        for result in results.ResultsReader(job.results()):
            alerts.append(self._parse_alert(result))

        return alerts

    def _parse_alert(self, splunk_event):
        """Parse Splunk event to AEON alert format"""
        return {
            'alertId': splunk_event.get('_key', ''),
            'title': splunk_event.get('signature', ''),
            'description': splunk_event.get('description', ''),
            'alertType': self._map_alert_type(splunk_event.get('category', '')),
            'severity': self._map_severity(splunk_event.get('severity', '')),
            'status': 'NEW',
            'detectionTime': splunk_event.get('_time', ''),
            'detectionSource': 'Splunk',
            'sourceIp': splunk_event.get('src_ip', ''),
            'destinationIp': splunk_event.get('dest_ip', ''),
            'rawData': json.dumps(splunk_event)
        }

    def _map_alert_type(self, splunk_category):
        mapping = {
            'intrusion': 'INTRUSION',
            'malware': 'MALWARE',
            'policy': 'POLICY_VIOLATION',
            'anomaly': 'ANOMALY'
        }
        return mapping.get(splunk_category.lower(), 'INTRUSION')

    def _map_severity(self, splunk_severity):
        try:
            sev = int(splunk_severity)
            if sev >= 8:
                return 'CRITICAL'
            elif sev >= 5:
                return 'HIGH'
            elif sev >= 3:
                return 'MEDIUM'
            else:
                return 'LOW'
        except:
            return 'MEDIUM'

    def enrich_with_aeon_context(self, alert):
        """Enrich Splunk alert with AEON context"""
        from neo4j import GraphDatabase

        driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))

        with driver.session() as session:
            # Find related assets
            if alert.get('destinationIp'):
                result = session.run("""
                    MATCH (a:Asset {ipAddress: $ip})
                    OPTIONAL MATCH (a)-[hv:HAS_VULNERABILITY]->(c:CVE)
                    WHERE hv.status = 'OPEN'
                    RETURN a.assetId as assetId, a.name as assetName, a.criticality as criticality,
                           collect(c.cveId) as vulnerabilities
                """, ip=alert['destinationIp'])

                for record in result:
                    alert['affectedAssets'] = [record['assetId']]
                    alert['assetContext'] = {
                        'assetId': record['assetId'],
                        'assetName': record['assetName'],
                        'criticality': record['criticality'],
                        'openVulnerabilities': record['vulnerabilities']
                    }

            # Check for IOC matches
            if alert.get('sourceIp'):
                result = session.run("""
                    MATCH (i:Indicator {value: $ip, type: 'IP'})
                    WHERE i.status = 'ACTIVE' AND NOT i.isExpired
                    OPTIONAL MATCH (i)-[:INDICATES]->(ta:ThreatActor)
                    RETURN i.indicatorId as indicatorId, i.category as category, i.severity as severity,
                           collect(ta.name) as threatActors
                """, ip=alert['sourceIp'])

                for record in result:
                    alert['iocMatch'] = {
                        'indicatorId': record['indicatorId'],
                        'category': record['category'],
                        'severity': record['severity'],
                        'attributedActors': record['threatActors']
                    }

        driver.close()
        return alert
```

---

## Integration Monitoring & Health

### Monitoring Metrics
```yaml
integration_metrics:
  nvd_sync:
    - last_sync_timestamp
    - cves_synced_count
    - sync_duration_seconds
    - sync_error_count

  mitre_sync:
    - last_sync_timestamp
    - tactics_synced
    - techniques_synced
    - sync_error_count

  cmdb_sync:
    - last_sync_timestamp
    - assets_synced_count
    - assets_updated_count
    - sync_error_count

  ner10_processing:
    - reports_processed
    - entities_extracted
    - relationships_created
    - processing_error_count
    - avg_processing_time_ms

  siem_integration:
    - alerts_ingested_count
    - enrichment_success_rate
    - avg_enrichment_time_ms
```

### Health Check Endpoints
```http
GET /health/integrations

Response 200 OK:
{
  "status": "healthy",
  "integrations": {
    "nvd": {
      "status": "healthy",
      "lastSync": "2024-01-20T10:00:00Z",
      "nextSync": "2024-01-20T12:00:00Z",
      "cvesInDatabase": 245678
    },
    "mitre": {
      "status": "healthy",
      "lastSync": "2024-01-19T02:00:00Z",
      "nextSync": "2024-01-26T02:00:00Z",
      "tacticsInDatabase": 14,
      "techniquesInDatabase": 193
    },
    "cmdb": {
      "status": "healthy",
      "lastSync": "2024-01-20T08:00:00Z",
      "nextSync": "2024-01-20T12:00:00Z",
      "assetsInDatabase": 5421
    },
    "ner10": {
      "status": "healthy",
      "processedToday": 47,
      "queuedForProcessing": 12
    },
    "siem": {
      "status": "healthy",
      "alertsIngestedToday": 234,
      "avgEnrichmentTime": 87
    }
  }
}
```

---

## Version History

- v3.0.0 (2025-11-19): Complete integration specifications with NER10, MITRE, NVD, CMDB, SIEM
- v2.5.0 (2025-11-11): Added SIEM integration specifications
- v2.0.0 (2025-11-01): Initial comprehensive integration specification

---

**Document Classification**: TECHNICAL SPECIFICATION
**Confidentiality**: INTERNAL USE
**Review Cycle**: Quarterly
**Next Review**: 2026-02-19
