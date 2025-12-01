# Cybersecurity Knowledge Base Implementation Plan
**File:** Cybersecurity_KB_Implementation_Plan.md
**Created:** 2025-10-26 22:30:00 UTC
**Version:** v1.0.0
**Author:** SuperClaude Planning Agent
**Purpose:** Comprehensive step-by-step implementation guide for building cybersecurity knowledge base with KAG
**Status:** ACTIVE

## Executive Summary

This document provides a detailed, actionable implementation plan for building a cybersecurity knowledge base using the KAG framework, OpenSPG, and the Unified Cybersecurity Ontology (UCO). The implementation is designed for the existing infrastructure at `/home/jim/2_OXOT_Projects_Dev` with OpenSPG and Neo4j already deployed.

**Key Components:**
- KAG Framework v0.1.0+ (already installed)
- OpenSPG server (running at http://localhost:8887)
- Neo4j Enterprise (running at http://localhost:7474)
- Unified Cybersecurity Ontology (UCO) v1.5
- Cybersecurity data sources: ATT&CK, CVE, CWE, STIX, MISP

**Expected Timeline:** 6-8 weeks
**Complexity Level:** High
**Prerequisites:** Python 3.10+, Docker, OpenSPG deployment

---

## Phase 1: Environment Preparation (Week 1)

### Task 1.1: Virtual Environment Setup
**Prerequisites:** None
**Duration:** 30 minutes
**Priority:** Critical

**Steps:**
```bash
# Navigate to project root
cd /home/jim/2_OXOT_Projects_Dev

# Activate existing virtual environment
source venv/bin/activate

# Verify KAG installation
python -c "import kag; print(f'KAG version: {kag.__version__}')"

# Verify required packages
pip list | grep -E "kag|openspg|neo4j|rdflib|owlready2"

# Install additional ontology processing libraries
pip install rdflib owlready2 pyyaml requests
```

**Expected Output:**
```
KAG version: 0.1.0 (or higher)
rdflib installed
owlready2 installed
```

**Verification:**
```bash
python -c "from rdflib import Graph; print('RDFLib OK')"
python -c "from owlready2 import get_ontology; print('Owlready2 OK')"
```

---

### Task 1.2: Configuration File Preparation
**Prerequisites:** Task 1.1
**Duration:** 1 hour
**Priority:** Critical

**Steps:**

1. **Create project configuration file:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples
mkdir -p cybersecurity
cd cybersecurity
```

2. **Create `cyber_config.yaml`:**
```yaml
#------------project configuration start----------------#
openie_llm: &openie_llm
  type: maas
  base_url: http://localhost:11434/v1  # Ollama local
  api_key: dummy
  model: llama2
  enable_check: false

chat_llm: &chat_llm
  type: maas
  base_url: http://localhost:11434/v1
  api_key: dummy
  model: llama2
  enable_check: false

vectorize_model: &vectorize_model
  type: openai
  base_url: http://localhost:11434/v1
  api_key: dummy
  model: nomic-embed-text
  vector_dimensions: 768
  enable_check: false
vectorizer: *vectorize_model

log:
  level: INFO

project:
  biz_scene: cybersecurity
  host_addr: http://127.0.0.1:8887
  id: "1"
  language: en
  namespace: CyberSecurityKB
#------------project configuration end----------------#

#------------kag-builder configuration start----------------#
kag_builder_pipeline:
  chain:
    type: unstructured_builder_chain
    extractor:
      type: knowledge_unit_extractor
      llm: *openie_llm
      ner_prompt:
        type: knowledge_unit_ner
      triple_prompt:
        type: knowledge_unit_triple
      kn_prompt:
        type: knowledge_unit
    reader:
      type: dict_reader
    post_processor:
      type: kag_post_processor
    splitter:
      type: length_splitter
      split_length: 100000
      window_length: 0
    vectorizer:
      type: batch_vectorizer
      vectorize_model: *vectorize_model
    writer:
      type: kg_writer
  num_threads_per_chain: 1
  num_chains: 8  # Adjust based on CPU cores
  scanner:
    type: dict_reader
#------------kag-builder configuration end----------------#

#------------kag-solver configuration start----------------#
search_api: &search_api
  type: openspg_search_api

graph_api: &graph_api
  type: openspg_graph_api

kg_cs: &kg_cs
  type: kg_cs_open_spg
  priority: 0
  path_select:
    type: exact_one_hop_select
    graph_api: *graph_api
    search_api: *search_api
  entity_linking:
    type: entity_linking
    graph_api: *graph_api
    search_api: *search_api
    recognition_threshold: 0.9
    exclude_types:
      - Chunk
      - AtomicQuery
      - KnowledgeUnit

kg_fr: &kg_fr
  type: kg_fr_knowledge_unit
  top_k: 20
  graph_api: *graph_api
  search_api: *search_api
  vectorize_model: *vectorize_model
  entity_linking:
    type: entity_linking
    graph_api: *graph_api
    search_api: *search_api
    recognition_threshold: 0.8

rc: &rc
  type: rc_open_spg
  vector_chunk_retriever:
    type: vector_chunk_retriever
    vectorize_model: *vectorize_model
    score_threshold: 0.65
    search_api: *search_api
  graph_api: *graph_api
  search_api: *search_api
  vectorize_model: *vectorize_model
  top_k: 20

kag_solver_pipeline:
  type: kag_static_pipeline
  planner:
    type: lf_kag_static_planner
    llm: *chat_llm
  executors:
    - type: kag_hybrid_retrieval_executor
      retrievers:
        - *kg_cs
        - *kg_fr
        - *rc
    - type: kag_output_executor
      llm_module: *chat_llm
  generator:
    type: default_generator
    llm_client: *chat_llm
    enable_ref: true
#------------kag-solver configuration end----------------#
```

**Verification:**
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('cyber_config.yaml'))"
```

---

### Task 1.3: API Key Configuration
**Prerequisites:** Task 1.2
**Duration:** 15 minutes
**Priority:** High

**Steps:**

1. **For local development (Ollama):**
```bash
# Ensure Ollama is running
curl http://localhost:11434/api/version

# Pull required models
ollama pull llama2
ollama pull nomic-embed-text
```

2. **For production (OpenAI/Cloud LLM):**
```bash
# Add to .env file in project root
echo "OPENAI_API_KEY=your_key_here" >> /home/jim/2_OXOT_Projects_Dev/.env
```

3. **Update cyber_config.yaml for production:**
```yaml
# Replace openie_llm and chat_llm with:
openie_llm: &openie_llm
  type: maas
  base_url: https://api.openai.com/v1
  api_key: ${OPENAI_API_KEY}
  model: gpt-4
  enable_check: false

vectorize_model: &vectorize_model
  type: openai
  base_url: https://api.openai.com/v1
  api_key: ${OPENAI_API_KEY}
  model: text-embedding-3-large
  vector_dimensions: 3072
  enable_check: false
```

**Verification:**
```bash
# Test LLM connection
python -c "from openai import OpenAI; client = OpenAI(); print('LLM OK')"
```

---

## Phase 2: Project Initialization (Week 1-2)

### Task 2.1: Create KAG Project
**Prerequisites:** Tasks 1.1-1.3
**Duration:** 30 minutes
**Priority:** Critical

**Steps:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity

# Create project using knext CLI
knext project create --config_path ./cyber_config.yaml

# Verify project creation
knext project list | grep CyberSecurityKB
```

**Expected Output:**
```
Project created successfully: CyberSecurityKB
Namespace: CyberSecurityKB
Host: http://127.0.0.1:8887
```

**Verification:**
```bash
# Check project structure
ls -la CyberSecurityKB/
# Expected: builder/, schema/, solver/, kag_config.yaml
```

---

### Task 2.2: Project Structure Setup
**Prerequisites:** Task 2.1
**Duration:** 30 minutes
**Priority:** High

**Steps:**
```bash
cd CyberSecurityKB

# Create additional directories
mkdir -p data/{attack,cve,cwe,stix,misp}
mkdir -p scripts
mkdir -p docs
mkdir -p tests

# Create README
cat > README.md << 'EOF'
# Cybersecurity Knowledge Base

Knowledge graph for cybersecurity threat intelligence using KAG framework.

## Data Sources
- MITRE ATT&CK
- CVE Database
- CWE Database
- STIX 2.1
- MISP

## Schema
Based on Unified Cybersecurity Ontology (UCO) v1.5

## Usage
See docs/USAGE.md
EOF
```

**Project Structure:**
```
CyberSecurityKB/
├── builder/
│   ├── __init__.py
│   ├── indexer.py
│   ├── data/
│   │   ├── attack/
│   │   ├── cve/
│   │   ├── cwe/
│   │   ├── stix/
│   │   └── misp/
│   └── ckpt/
├── schema/
│   └── CyberSecurityKB.schema
├── solver/
│   ├── __init__.py
│   └── qa.py
├── reasoner/
├── scripts/
├── docs/
├── tests/
├── kag_config.yaml
└── README.md
```

**Verification:**
```bash
tree -L 2 CyberSecurityKB/
```

---

### Task 2.3: Verify OpenSPG Connectivity
**Prerequisites:** Task 2.1
**Duration:** 15 minutes
**Priority:** Critical

**Steps:**
```bash
# Test OpenSPG server
curl -f http://localhost:8887/health

# Test Neo4j connection
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" "RETURN 1"

# Python connectivity test
python << 'EOF'
from kag.common.conf import KAG_PROJECT_CONF
KAG_PROJECT_CONF.init_from_file("kag_config.yaml")
print(f"Project: {KAG_PROJECT_CONF.project_id}")
print(f"Namespace: {KAG_PROJECT_CONF.namespace}")
print(f"Host: {KAG_PROJECT_CONF.host_addr}")
EOF
```

**Expected Output:**
```
OpenSPG: healthy
Neo4j: 1
Project ID: 1
Namespace: CyberSecurityKB
Host: http://127.0.0.1:8887
```

---

## Phase 3: Schema Development (Week 2-3)

### Task 3.1: Analyze UCO Ontology
**Prerequisites:** Task 2.3
**Duration:** 4 hours
**Priority:** Critical

**Steps:**

1. **Parse UCO ontology files:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/Unified-Cybersecurity-Ontology

# List all ontology files
find . -name "*.ttl" -o -name "*.owl" | sort
```

2. **Create ontology analysis script:**
```python
# Save as: scripts/analyze_uco.py
from rdflib import Graph, Namespace, RDF, RDFS, OWL
import yaml

def analyze_uco_ontology():
    """Analyze UCO ontology and extract schema structure."""

    # Define namespaces
    UCO = Namespace("http://purl.org/cyber/uco#")
    ATK = Namespace("http://purl.org/cyber/atk#")
    CVE = Namespace("http://purl.org/cyber/cve#")
    CWE = Namespace("http://purl.org/cyber/cwe#")
    STIX = Namespace("http://purl.org/cyber/stix#")
    MISP = Namespace("http://purl.org/cyber/misp#")

    # Load UCO ontology
    g = Graph()
    g.parse("/home/jim/2_OXOT_Projects_Dev/Unified-Cybersecurity-Ontology/uco_1_5_rdf.owl")

    # Extract classes
    classes = set()
    for s in g.subjects(RDF.type, OWL.Class):
        if str(s).startswith("http://purl.org/cyber"):
            classes.add(str(s).split("#")[-1])

    # Extract properties
    properties = set()
    for s in g.subjects(RDF.type, OWL.ObjectProperty):
        if str(s).startswith("http://purl.org/cyber"):
            properties.add(str(s).split("#")[-1])

    for s in g.subjects(RDF.type, OWL.DatatypeProperty):
        if str(s).startswith("http://purl.org/cyber"):
            properties.add(str(s).split("#")[-1])

    # Print summary
    print(f"UCO Classes: {len(classes)}")
    print(f"UCO Properties: {len(properties)}")
    print("\nKey Classes:")
    for cls in sorted(classes)[:20]:
        print(f"  - {cls}")

    print("\nKey Properties:")
    for prop in sorted(properties)[:20]:
        print(f"  - {prop}")

    # Export for schema mapping
    schema_map = {
        "classes": sorted(list(classes)),
        "properties": sorted(list(properties))
    }

    with open("/home/jim/2_OXOT_Projects_Dev/docs/uco_schema_map.yaml", "w") as f:
        yaml.dump(schema_map, f, default_flow_style=False)

    print("\nSchema map exported to docs/uco_schema_map.yaml")

if __name__ == "__main__":
    analyze_uco_ontology()
```

3. **Run analysis:**
```bash
cd /home/jim/2_OXOT_Projects_Dev
python scripts/analyze_uco.py
```

**Expected Output:**
```
UCO Classes: 150+
UCO Properties: 200+
Key Classes identified
Schema map exported
```

**Verification:**
```bash
cat /home/jim/2_OXOT_Projects_Dev/docs/uco_schema_map.yaml | head -50
```

---

### Task 3.2: Define OpenSPG Schema
**Prerequisites:** Task 3.1
**Duration:** 8 hours
**Priority:** Critical

**Steps:**

1. **Create core cybersecurity schema:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB/schema
```

2. **Create `CyberSecurityKB.schema` file:**
```python
# CyberSecurityKB.schema
# Cybersecurity Knowledge Graph Schema based on UCO

namespace CyberSecurityKB

# ============================================================================
# Core Threat Entity Types
# ============================================================================

@entity
type Threat:
    """Cybersecurity threat entity"""
    id: str
    name: str
    description: str
    severity: str  # Critical, High, Medium, Low
    threat_type: str  # Malware, Exploit, Vulnerability, etc.
    first_seen: datetime
    last_updated: datetime

    # Relationships
    exploits: [Vulnerability]
    uses_technique: [AttackTechnique]
    targets: [Asset]
    mitigated_by: [Mitigation]

@entity
type Vulnerability:
    """Security vulnerability (CVE)"""
    id: str
    cve_id: str
    name: str
    description: str
    cvss_score: float
    cvss_vector: str
    severity: str
    cwe_id: str
    published_date: datetime
    last_modified: datetime

    # Relationships
    affects: [Software]
    related_to: [Weakness]
    exploited_by: [Threat]
    has_patch: [Patch]

@entity
type Weakness:
    """Software weakness (CWE)"""
    id: str
    cwe_id: str
    name: str
    description: str
    weakness_type: str
    abstraction_level: str  # Class, Base, Variant

    # Relationships
    parent_of: [Weakness]
    child_of: [Weakness]
    related_to: [Vulnerability]

@entity
type AttackTechnique:
    """MITRE ATT&CK technique"""
    id: str
    technique_id: str  # e.g., T1059
    name: str
    description: str
    tactic: str  # e.g., Execution, Persistence
    platform: [str]  # Windows, Linux, macOS, etc.
    data_sources: [str]

    # Relationships
    sub_technique_of: [AttackTechnique]
    mitigated_by: [Mitigation]
    used_by: [ThreatActor]

@entity
type ThreatActor:
    """Threat actor or group"""
    id: str
    name: str
    aliases: [str]
    description: str
    actor_type: str  # APT, Cybercriminal, Hacktivist, etc.
    sophistication: str
    motivation: str
    first_seen: datetime

    # Relationships
    uses: [AttackTechnique]
    uses_malware: [Malware]
    targets: [Sector]

@entity
type Malware:
    """Malicious software"""
    id: str
    name: str
    aliases: [str]
    description: str
    malware_type: str  # Ransomware, Trojan, RAT, etc.
    first_seen: datetime

    # Relationships
    uses_technique: [AttackTechnique]
    exploits: [Vulnerability]
    dropped_by: [Malware]

@entity
type Mitigation:
    """Security mitigation"""
    id: str
    mitigation_id: str
    name: str
    description: str
    mitigation_type: str

    # Relationships
    mitigates: [AttackTechnique]
    addresses: [Vulnerability]

@entity
type Software:
    """Software product"""
    id: str
    name: str
    vendor: str
    version: str
    cpe: str  # Common Platform Enumeration

    # Relationships
    has_vulnerability: [Vulnerability]
    has_patch: [Patch]

@entity
type Patch:
    """Security patch"""
    id: str
    patch_id: str
    name: str
    description: str
    release_date: datetime

    # Relationships
    fixes: [Vulnerability]
    applies_to: [Software]

@entity
type Asset:
    """IT/OT asset"""
    id: str
    name: str
    asset_type: str
    ip_address: str
    os: str
    criticality: str

    # Relationships
    runs: [Software]
    targeted_by: [Threat]
    vulnerable_to: [Vulnerability]

@entity
type Sector:
    """Industry sector"""
    id: str
    name: str
    description: str

    # Relationships
    contains: [Asset]
    targeted_by: [ThreatActor]

@entity
type Indicator:
    """Indicator of Compromise (IoC)"""
    id: str
    indicator_type: str  # IP, Domain, Hash, etc.
    value: str
    confidence: str
    first_seen: datetime
    last_seen: datetime

    # Relationships
    indicates: [Threat]
    associated_with: [Malware]

# ============================================================================
# STIX 2.1 Integration
# ============================================================================

@entity
type STIXObject:
    """STIX 2.1 Cyber Observable Object"""
    id: str
    type: str
    spec_version: str
    created: datetime
    modified: datetime

    # Relationships
    related_to: [STIXObject]

# ============================================================================
# Knowledge Unit for Document Chunks
# ============================================================================

@entity
type KnowledgeUnit:
    """Document knowledge unit"""
    id: str
    content: str
    source_doc: str
    chunk_index: int

    # Relationships
    mentions: [Threat, Vulnerability, AttackTechnique]

@entity
type Doc:
    """Source document"""
    id: str
    name: str
    content: str
    doc_type: str

    # Relationships
    contains: [KnowledgeUnit]
```

**Verification:**
```bash
# Validate schema syntax (OpenSPG will validate on commit)
cat CyberSecurityKB.schema | grep -E "^type|^@entity"
```

---

### Task 3.3: Commit Schema to OpenSPG
**Prerequisites:** Task 3.2
**Duration:** 30 minutes
**Priority:** Critical

**Steps:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB

# Commit schema to OpenSPG server
knext schema commit

# Verify schema in Neo4j
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "CALL db.schema.visualization()"

# Check created node labels
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "CALL db.labels() YIELD label RETURN label ORDER BY label"
```

**Expected Output:**
```
Schema committed successfully
Node labels: Threat, Vulnerability, Weakness, AttackTechnique, etc.
```

**Verification:**
```bash
# Query schema in Neo4j
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n:Threat) RETURN count(n)"
# Should return 0 (schema exists, no data yet)
```

---

## Phase 4: Data Source Integration (Week 3-4)

### Task 4.1: Download ATT&CK Data
**Prerequisites:** Task 3.3
**Duration:** 1 hour
**Priority:** High

**Steps:**

1. **Download MITRE ATT&CK STIX data:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB/builder/data/attack

# Download Enterprise ATT&CK
wget https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json

# Download ICS ATT&CK
wget https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack.json

# Download Mobile ATT&CK
wget https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack.json

# Verify downloads
ls -lh *.json
```

2. **Create ATT&CK parser script:**
```python
# Save as: builder/attack_parser.py
import json
from typing import List, Dict
from pathlib import Path

def parse_attack_stix(file_path: str) -> List[Dict]:
    """Parse ATT&CK STIX JSON and extract entities."""

    with open(file_path, 'r') as f:
        data = json.load(f)

    entities = []

    for obj in data.get('objects', []):
        obj_type = obj.get('type')

        if obj_type == 'attack-pattern':
            # ATT&CK Technique
            entity = {
                'id': obj.get('id'),
                'type': 'AttackTechnique',
                'technique_id': obj.get('external_references', [{}])[0].get('external_id', ''),
                'name': obj.get('name'),
                'description': obj.get('description', ''),
                'tactic': [phase.get('phase_name') for phase in obj.get('kill_chain_phases', [])],
                'platform': obj.get('x_mitre_platforms', []),
                'created': obj.get('created'),
                'modified': obj.get('modified')
            }
            entities.append(entity)

        elif obj_type == 'intrusion-set':
            # Threat Actor
            entity = {
                'id': obj.get('id'),
                'type': 'ThreatActor',
                'name': obj.get('name'),
                'aliases': obj.get('aliases', []),
                'description': obj.get('description', ''),
                'first_seen': obj.get('created')
            }
            entities.append(entity)

        elif obj_type == 'malware':
            # Malware
            entity = {
                'id': obj.get('id'),
                'type': 'Malware',
                'name': obj.get('name'),
                'description': obj.get('description', ''),
                'malware_type': obj.get('x_mitre_platforms', []),
                'first_seen': obj.get('created')
            }
            entities.append(entity)

        elif obj_type == 'course-of-action':
            # Mitigation
            entity = {
                'id': obj.get('id'),
                'type': 'Mitigation',
                'mitigation_id': obj.get('external_references', [{}])[0].get('external_id', ''),
                'name': obj.get('name'),
                'description': obj.get('description', '')
            }
            entities.append(entity)

    return entities

def convert_to_kag_format(entities: List[Dict]) -> List[Dict]:
    """Convert entities to KAG builder format."""

    kag_docs = []
    for entity in entities:
        doc = {
            'id': entity['id'],
            'name': entity.get('name', ''),
            'content': f"{entity.get('name', '')}\n\n{entity.get('description', '')}",
            'metadata': entity
        }
        kag_docs.append(doc)

    return kag_docs

if __name__ == '__main__':
    # Parse all ATT&CK files
    data_dir = Path('data/attack')
    all_entities = []

    for json_file in data_dir.glob('*.json'):
        print(f"Parsing {json_file.name}...")
        entities = parse_attack_stix(str(json_file))
        all_entities.extend(entities)

    # Convert to KAG format
    kag_docs = convert_to_kag_format(all_entities)

    # Save
    output_file = data_dir / 'attack_processed.json'
    with open(output_file, 'w') as f:
        json.dump(kag_docs, f, indent=2)

    print(f"Processed {len(kag_docs)} entities -> {output_file}")
```

3. **Run parser:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB/builder
python attack_parser.py
```

**Expected Output:**
```
Parsing enterprise-attack.json...
Parsing ics-attack.json...
Parsing mobile-attack.json...
Processed 3000+ entities -> data/attack/attack_processed.json
```

**Verification:**
```bash
wc -l data/attack/attack_processed.json
jq '.[] | select(.metadata.type == "AttackTechnique") | .name' data/attack/attack_processed.json | head -10
```

---

### Task 4.2: Download CVE Data
**Prerequisites:** Task 4.1
**Duration:** 2 hours
**Priority:** High

**Steps:**

1. **Download NVD CVE data:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB/builder/data/cve

# Download recent CVE data (2023-2024)
wget https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-2023.json.gz
wget https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-2024.json.gz

# Extract
gunzip *.gz

# Verify
ls -lh *.json
```

2. **Create CVE parser script:**
```python
# Save as: builder/cve_parser.py
import json
from typing import List, Dict
from pathlib import Path

def parse_cve_feed(file_path: str) -> List[Dict]:
    """Parse NVD CVE JSON feed."""

    with open(file_path, 'r') as f:
        data = json.load(f)

    entities = []

    for item in data.get('CVE_Items', []):
        cve = item.get('cve', {})
        cve_id = cve.get('CVE_data_meta', {}).get('ID', '')

        # Get description
        descriptions = cve.get('description', {}).get('description_data', [])
        description = descriptions[0].get('value', '') if descriptions else ''

        # Get CVSS score
        impact = item.get('impact', {})
        cvss_v3 = impact.get('baseMetricV3', {}).get('cvssV3', {})
        cvss_score = cvss_v3.get('baseScore', 0.0)
        cvss_vector = cvss_v3.get('vectorString', '')
        severity = cvss_v3.get('baseSeverity', 'UNKNOWN')

        # Get CWE
        problemtype_data = cve.get('problemtype', {}).get('problemtype_data', [])
        cwe_ids = []
        for pt in problemtype_data:
            for desc in pt.get('description', []):
                value = desc.get('value', '')
                if value.startswith('CWE-'):
                    cwe_ids.append(value)

        # Get dates
        published = item.get('publishedDate', '')
        modified = item.get('lastModifiedDate', '')

        entity = {
            'id': cve_id,
            'type': 'Vulnerability',
            'cve_id': cve_id,
            'name': cve_id,
            'description': description,
            'cvss_score': cvss_score,
            'cvss_vector': cvss_vector,
            'severity': severity,
            'cwe_id': ','.join(cwe_ids),
            'published_date': published,
            'last_modified': modified
        }
        entities.append(entity)

    return entities

def convert_to_kag_format(entities: List[Dict]) -> List[Dict]:
    """Convert CVE entities to KAG format."""

    kag_docs = []
    for entity in entities:
        doc = {
            'id': entity['id'],
            'name': entity['cve_id'],
            'content': f"{entity['cve_id']} (CVSS: {entity['cvss_score']})\n\n{entity['description']}",
            'metadata': entity
        }
        kag_docs.append(doc)

    return kag_docs

if __name__ == '__main__':
    data_dir = Path('data/cve')
    all_entities = []

    for json_file in data_dir.glob('nvdcve-*.json'):
        print(f"Parsing {json_file.name}...")
        entities = parse_cve_feed(str(json_file))
        all_entities.extend(entities)
        print(f"  Found {len(entities)} CVEs")

    kag_docs = convert_to_kag_format(all_entities)

    output_file = data_dir / 'cve_processed.json'
    with open(output_file, 'w') as f:
        json.dump(kag_docs, f, indent=2)

    print(f"\nTotal processed: {len(kag_docs)} CVEs -> {output_file}")
```

3. **Run parser:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB/builder
python cve_parser.py
```

**Expected Output:**
```
Parsing nvdcve-1.1-2023.json...
  Found 25000+ CVEs
Parsing nvdcve-1.1-2024.json...
  Found 15000+ CVEs
Total processed: 40000+ CVEs -> data/cve/cve_processed.json
```

**Verification:**
```bash
jq '. | length' data/cve/cve_processed.json
jq '.[0]' data/cve/cve_processed.json
```

---

### Task 4.3: Download CWE Data
**Prerequisites:** Task 4.2
**Duration:** 1 hour
**Priority:** Medium

**Steps:**

1. **Download CWE data:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB/builder/data/cwe

# Download CWE XML
wget https://cwe.mitre.org/data/xml/cwec_latest.xml.zip
unzip cwec_latest.xml.zip
mv cwec_*.xml cwe_data.xml
rm cwec_latest.xml.zip

# Verify
ls -lh cwe_data.xml
```

2. **Create CWE parser script:**
```python
# Save as: builder/cwe_parser.py
import xml.etree.ElementTree as ET
import json
from typing import List, Dict
from pathlib import Path

def parse_cwe_xml(file_path: str) -> List[Dict]:
    """Parse CWE XML data."""

    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define namespace
    ns = {'cwe': 'http://cwe.mitre.org/cwe-6'}

    entities = []

    for weakness in root.findall('.//cwe:Weakness', ns):
        cwe_id = weakness.get('ID')
        name = weakness.get('Name', '')
        abstraction = weakness.get('Abstraction', '')

        # Get description
        desc_elem = weakness.find('cwe:Description', ns)
        description = desc_elem.text if desc_elem is not None else ''

        # Get extended description
        ext_desc_elem = weakness.find('cwe:Extended_Description', ns)
        ext_description = ext_desc_elem.text if ext_desc_elem is not None else ''

        full_description = f"{description}\n\n{ext_description}".strip()

        entity = {
            'id': f"CWE-{cwe_id}",
            'type': 'Weakness',
            'cwe_id': f"CWE-{cwe_id}",
            'name': name,
            'description': full_description,
            'weakness_type': weakness.get('Structure', ''),
            'abstraction_level': abstraction
        }
        entities.append(entity)

    return entities

def convert_to_kag_format(entities: List[Dict]) -> List[Dict]:
    """Convert CWE entities to KAG format."""

    kag_docs = []
    for entity in entities:
        doc = {
            'id': entity['id'],
            'name': f"{entity['cwe_id']}: {entity['name']}",
            'content': f"{entity['cwe_id']}: {entity['name']}\n\n{entity['description']}",
            'metadata': entity
        }
        kag_docs.append(doc)

    return kag_docs

if __name__ == '__main__':
    data_dir = Path('data/cwe')
    xml_file = data_dir / 'cwe_data.xml'

    print(f"Parsing {xml_file}...")
    entities = parse_cwe_xml(str(xml_file))
    print(f"  Found {len(entities)} CWEs")

    kag_docs = convert_to_kag_format(entities)

    output_file = data_dir / 'cwe_processed.json'
    with open(output_file, 'w') as f:
        json.dump(kag_docs, f, indent=2)

    print(f"Processed {len(kag_docs)} CWEs -> {output_file}")
```

3. **Run parser:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB/builder
pip install lxml  # Required for XML parsing
python cwe_parser.py
```

**Expected Output:**
```
Parsing data/cwe/cwe_data.xml...
  Found 900+ CWEs
Processed 900+ CWEs -> data/cwe/cwe_processed.json
```

**Verification:**
```bash
jq '. | length' data/cwe/cwe_processed.json
jq '.[0]' data/cwe/cwe_processed.json
```

---

### Task 4.4: Prepare STIX Data (Optional)
**Prerequisites:** Task 4.3
**Duration:** 2 hours
**Priority:** Low

**Steps:**

1. **Download STIX sample data:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB/builder/data/stix

# Example: CISA STIX feeds
wget https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json

# Or use STIX samples from OASIS
wget https://raw.githubusercontent.com/oasis-open/cti-stix2-json-schemas/master/examples/indicator-malicious-url.json
```

2. **Create STIX parser (basic):**
```python
# Save as: builder/stix_parser.py
import json
from typing import List, Dict
from pathlib import Path

def parse_stix_bundle(file_path: str) -> List[Dict]:
    """Parse STIX 2.1 bundle."""

    with open(file_path, 'r') as f:
        data = json.load(f)

    entities = []

    for obj in data.get('objects', []):
        obj_type = obj.get('type')

        if obj_type == 'indicator':
            entity = {
                'id': obj.get('id'),
                'type': 'Indicator',
                'indicator_type': obj.get('pattern_type', ''),
                'value': obj.get('pattern', ''),
                'confidence': obj.get('confidence', ''),
                'created': obj.get('created'),
                'modified': obj.get('modified')
            }
            entities.append(entity)

    return entities

if __name__ == '__main__':
    # This is a placeholder - implement based on your STIX sources
    print("STIX parser template created. Customize for your data sources.")
```

**Note:** STIX integration is optional and depends on available threat intelligence feeds.

---

### Task 4.5: Prepare MISP Data (Optional)
**Prerequisites:** Task 4.4
**Duration:** 2 hours
**Priority:** Low

**Note:** MISP integration requires access to a MISP instance. This task is optional and can be implemented if you have MISP access.

---

## Phase 5: Knowledge Graph Building (Week 4-5)

### Task 5.1: Create Unified Data Reader
**Prerequisites:** Tasks 4.1-4.3
**Duration:** 3 hours
**Priority:** Critical

**Steps:**

1. **Create master data reader:**
```python
# Save as: builder/cyber_data_reader.py
import json
from pathlib import Path
from typing import Iterator, Dict
from kag.builder.component.reader.base import SourceReader

class CyberSecurityDataReader(SourceReader):
    """Reader for cybersecurity data sources."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.sources = {
            'attack': self.data_dir / 'attack' / 'attack_processed.json',
            'cve': self.data_dir / 'cve' / 'cve_processed.json',
            'cwe': self.data_dir / 'cwe' / 'cwe_processed.json'
        }

    def read(self) -> Iterator[Dict]:
        """Read and yield documents from all sources."""

        for source_name, file_path in self.sources.items():
            if not file_path.exists():
                print(f"Warning: {file_path} not found, skipping...")
                continue

            print(f"Reading {source_name} data from {file_path}...")

            with open(file_path, 'r') as f:
                data = json.load(f)

            for item in data:
                # Ensure required fields
                doc = {
                    'id': item.get('id', ''),
                    'name': item.get('name', ''),
                    'content': item.get('content', ''),
                    'source': source_name,
                    'metadata': item.get('metadata', {})
                }
                yield doc

            print(f"  Loaded {len(data)} documents from {source_name}")

if __name__ == '__main__':
    # Test the reader
    reader = CyberSecurityDataReader()

    count = 0
    for doc in reader.read():
        count += 1
        if count <= 3:
            print(f"\nSample document {count}:")
            print(f"  ID: {doc['id']}")
            print(f"  Name: {doc['name']}")
            print(f"  Source: {doc['source']}")

    print(f"\nTotal documents: {count}")
```

2. **Test the reader:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB/builder
python cyber_data_reader.py
```

**Expected Output:**
```
Reading attack data from data/attack/attack_processed.json...
  Loaded 3000+ documents from attack
Reading cve data from data/cve/cve_processed.json...
  Loaded 40000+ documents from cve
Reading cwe data from data/cwe/cwe_processed.json...
  Loaded 900+ documents from cwe
Total documents: 44000+
```

**Verification:**
```bash
# Check sample output
python cyber_data_reader.py | head -30
```

---

### Task 5.2: Configure KAG Builder
**Prerequisites:** Task 5.1
**Duration:** 2 hours
**Priority:** Critical

**Steps:**

1. **Create `indexer.py`:**
```python
# Save as: builder/indexer.py
import os
import sys
from pathlib import Path

# Add KAG to path
kag_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(kag_root))

from kag.builder.default_chain import DefaultUnstructuredBuilderChain
from kag.common.conf import KAG_PROJECT_CONF
from cyber_data_reader import CyberSecurityDataReader

def build_knowledge_graph():
    """Build cybersecurity knowledge graph."""

    # Initialize configuration
    config_path = Path(__file__).parent.parent / "kag_config.yaml"
    KAG_PROJECT_CONF.init_from_file(str(config_path))

    print("=" * 80)
    print("Cybersecurity Knowledge Graph Builder")
    print("=" * 80)
    print(f"Project: {KAG_PROJECT_CONF.namespace}")
    print(f"Host: {KAG_PROJECT_CONF.host_addr}")
    print("=" * 80)

    # Create data reader
    data_reader = CyberSecurityDataReader(data_dir="data")

    # Create builder chain
    builder = DefaultUnstructuredBuilderChain()

    # Build knowledge graph
    print("\nStarting knowledge graph construction...")
    print("This may take several hours depending on data size and CPU cores.")
    print("=" * 80)

    try:
        # Process documents
        builder.build(reader=data_reader)

        print("\n" + "=" * 80)
        print("Knowledge graph construction completed successfully!")
        print("=" * 80)

        # Print statistics
        ckpt_dir = Path("ckpt")
        if ckpt_dir.exists():
            ckpt_files = list(ckpt_dir.glob("*.ckpt"))
            print(f"\nCheckpoint files created: {len(ckpt_files)}")
            for ckpt in ckpt_files[:5]:
                print(f"  - {ckpt.name}")

    except Exception as e:
        print(f"\nError during build: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    build_knowledge_graph()
```

2. **Create small test dataset:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB/builder

# Create test data (100 documents)
python << 'EOF'
import json
from pathlib import Path

# Load full datasets
attack_data = json.load(open('data/attack/attack_processed.json'))
cve_data = json.load(open('data/cve/cve_processed.json'))
cwe_data = json.load(open('data/cwe/cwe_processed.json'))

# Create small test sets
test_data = {
    'attack': attack_data[:50],
    'cve': cve_data[:30],
    'cwe': cwe_data[:20]
}

# Save test data
test_dir = Path('data/test')
test_dir.mkdir(exist_ok=True)

for source, data in test_data.items():
    output_file = test_dir / f'{source}_test.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Created {output_file} with {len(data)} documents")

print(f"\nTotal test documents: {sum(len(d) for d in test_data.values())}")
EOF
```

**Expected Output:**
```
Created data/test/attack_test.json with 50 documents
Created data/test/cve_test.json with 30 documents
Created data/test/cwe_test.json with 20 documents
Total test documents: 100
```

---

### Task 5.3: Run Builder Pipeline (Test)
**Prerequisites:** Task 5.2
**Duration:** 1-2 hours
**Priority:** Critical

**Steps:**

1. **Modify reader for test data:**
```python
# Temporarily modify cyber_data_reader.py to use test data
# Change data paths:
#   'attack': self.data_dir / 'test' / 'attack_test.json',
#   'cve': self.data_dir / 'test' / 'cve_test.json',
#   'cwe': self.data_dir / 'test' / 'cwe_test.json'
```

2. **Run test build:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB/builder

# Ensure services are running
docker ps | grep -E "openspg|neo4j"

# Run builder
python indexer.py 2>&1 | tee build.log
```

**Expected Duration:** 30-60 minutes for 100 documents

**Expected Output:**
```
================================================================================
Cybersecurity Knowledge Graph Builder
================================================================================
Project: CyberSecurityKB
Host: http://127.0.0.1:8887
================================================================================
Reading attack data from data/test/attack_test.json...
  Loaded 50 documents from attack
Reading cve data from data/test/cve_test.json...
  Loaded 30 documents from cve
Reading cwe data from data/test/cwe_test.json...
  Loaded 20 documents from cwe

Starting knowledge graph construction...
This may take several hours depending on data size and CPU cores.
================================================================================
Processing documents: 100%|████████████████| 100/100
Extracting entities: 100%|████████████████| 100/100
Building graph: 100%|████████████████| 100/100

================================================================================
Knowledge graph construction completed successfully!
================================================================================
Checkpoint files created: 1
  - kag_checkpoint_0_1.ckpt
```

**Verification:**
```bash
# Check checkpoint file
ls -lh ckpt/
wc -l ckpt/*.ckpt

# Verify data in Neo4j
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) WHERE n.namespace = 'CyberSecurityKB' RETURN labels(n)[0] as Type, count(*) as Count ORDER BY Count DESC"
```

**Expected Neo4j Output:**
```
+---------------------------+
| Type          | Count     |
+---------------------------+
| Vulnerability | 30        |
| AttackTechniq | 50        |
| Weakness      | 20        |
| KnowledgeUnit | 100+      |
+---------------------------+
```

---

### Task 5.4: Run Full Builder Pipeline
**Prerequisites:** Task 5.3 (successful test)
**Duration:** 8-12 hours
**Priority:** High

**Steps:**

1. **Restore full data reader:**
```python
# Modify cyber_data_reader.py back to use full data:
#   'attack': self.data_dir / 'attack' / 'attack_processed.json',
#   'cve': self.data_dir / 'cve' / 'cve_processed.json',
#   'cwe': self.data_dir / 'cwe' / 'cwe_processed.json'
```

2. **Clear test data:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB/builder

# Remove test checkpoints
rm -rf ckpt/*

# Clear Neo4j test data
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) WHERE n.namespace = 'CyberSecurityKB' DETACH DELETE n"
```

3. **Run full build:**
```bash
# Start in background with nohup
nohup python indexer.py > build_full.log 2>&1 &

# Monitor progress
tail -f build_full.log

# Check process
ps aux | grep indexer.py
```

**Monitor Progress:**
```bash
# Check checkpoint files
watch -n 60 'ls -lh ckpt/ && wc -l ckpt/*.ckpt'

# Check Neo4j node counts
watch -n 300 'docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) WHERE n.namespace = '\''CyberSecurityKB'\'' RETURN labels(n)[0] as Type, count(*) as Count"'
```

**Expected Duration:** 8-12 hours for 44,000+ documents

**Expected Final State:**
```
Total nodes: 50,000+
- Vulnerabilities: 40,000+
- AttackTechniques: 3,000+
- Weaknesses: 900+
- KnowledgeUnits: 44,000+
- Other entities: variable

Total relationships: 100,000+
```

**Verification:**
```bash
# Final verification queries
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" << 'EOF'
// Total node count
MATCH (n) WHERE n.namespace = 'CyberSecurityKB'
RETURN count(n) as TotalNodes;

// Nodes by type
MATCH (n) WHERE n.namespace = 'CyberSecurityKB'
RETURN labels(n)[0] as Type, count(*) as Count
ORDER BY Count DESC;

// Total relationships
MATCH ()-[r]->() WHERE r.namespace = 'CyberSecurityKB'
RETURN count(r) as TotalRelationships;

// Sample nodes
MATCH (n:Vulnerability) WHERE n.namespace = 'CyberSecurityKB'
RETURN n.name, n.cvss_score LIMIT 10;
EOF
```

---

## Phase 6: Query and Testing (Week 5-6)

### Task 6.1: Create Query Interface
**Prerequisites:** Task 5.4
**Duration:** 2 hours
**Priority:** Critical

**Steps:**

1. **Create `qa.py` in solver directory:**
```python
# Save as: solver/qa.py
import sys
from pathlib import Path

# Add KAG to path
kag_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(kag_root))

from kag.solver.logic.solver_pipeline import SolverPipeline
from kag.common.conf import KAG_PROJECT_CONF

class CyberSecurityQuery:
    """Query interface for cybersecurity knowledge base."""

    def __init__(self, config_path: str = None):
        """Initialize query interface."""

        if config_path is None:
            config_path = Path(__file__).parent.parent / "kag_config.yaml"

        # Initialize configuration
        KAG_PROJECT_CONF.init_from_file(str(config_path))

        # Create solver pipeline
        self.solver = SolverPipeline.from_config(
            KAG_PROJECT_CONF.all_config["kag_solver_pipeline"]
        )

        print("=" * 80)
        print("Cybersecurity Knowledge Base Query Interface")
        print("=" * 80)
        print(f"Project: {KAG_PROJECT_CONF.namespace}")
        print(f"Host: {KAG_PROJECT_CONF.host_addr}")
        print("=" * 80)

    def query(self, question: str, verbose: bool = False) -> dict:
        """Execute query and return results."""

        print(f"\nQuestion: {question}")
        print("-" * 80)

        try:
            answer, trace = self.solver.run(question)

            result = {
                'question': question,
                'answer': answer,
                'trace': trace if verbose else None
            }

            print(f"Answer: {answer}")

            if verbose and trace:
                print("\nReasoning Trace:")
                print(trace)

            return result

        except Exception as e:
            print(f"Error: {e}")
            return {
                'question': question,
                'answer': None,
                'error': str(e)
            }

    def interactive(self):
        """Interactive query mode."""

        print("\nEnter queries (type 'exit' to quit, 'help' for examples)")
        print("=" * 80)

        while True:
            try:
                question = input("\nQuery> ").strip()

                if question.lower() == 'exit':
                    print("Goodbye!")
                    break

                if question.lower() == 'help':
                    self.show_examples()
                    continue

                if not question:
                    continue

                self.query(question, verbose=False)

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

    def show_examples(self):
        """Show example queries."""

        examples = [
            "What is CVE-2024-1234?",
            "What attack techniques are used by APT29?",
            "What vulnerabilities are related to SQL injection?",
            "How can I mitigate privilege escalation attacks?",
            "What is the CVSS score of CVE-2023-5678?",
            "What weaknesses are related to buffer overflow?",
            "List ransomware threats",
            "What techniques target Windows systems?"
        ]

        print("\nExample Queries:")
        print("-" * 80)
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example}")

def main():
    """Main function."""

    import argparse

    parser = argparse.ArgumentParser(description="Cybersecurity Knowledge Base Query")
    parser.add_argument("--query", "-q", type=str, help="Execute single query")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--examples", "-e", action="store_true", help="Show example queries")

    args = parser.parse_args()

    # Create query interface
    qa = CyberSecurityQuery()

    if args.examples:
        qa.show_examples()
    elif args.query:
        qa.query(args.query, verbose=args.verbose)
    elif args.interactive or not args.query:
        qa.interactive()

if __name__ == "__main__":
    main()
```

2. **Test query interface:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB/solver

# Show examples
python qa.py --examples

# Single query
python qa.py --query "What attack techniques target Windows?"

# Interactive mode
python qa.py --interactive
```

**Expected Output:**
```
================================================================================
Cybersecurity Knowledge Base Query Interface
================================================================================
Project: CyberSecurityKB
Host: http://127.0.0.1:8887
================================================================================

Question: What attack techniques target Windows?
--------------------------------------------------------------------------------
Answer: Windows is targeted by various ATT&CK techniques including:
- T1059: Command and Scripting Interpreter
- T1543: Create or Modify System Process
- T1078: Valid Accounts
...
```

**Verification:**
```bash
# Test multiple queries
python qa.py --query "What is CVE-2024-1234?" --verbose
python qa.py --query "List ransomware threats"
```

---

### Task 6.2: Create Test Suite
**Prerequisites:** Task 6.1
**Duration:** 3 hours
**Priority:** High

**Steps:**

1. **Create test queries:**
```python
# Save as: tests/test_queries.py
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'solver'))

from qa import CyberSecurityQuery

def test_cve_queries():
    """Test CVE-related queries."""

    qa = CyberSecurityQuery()

    queries = [
        "What is CVE-2023-1234?",
        "What is the CVSS score of CVE-2023-1234?",
        "What vulnerabilities have CVSS score greater than 9.0?",
        "What software is affected by CVE-2023-1234?"
    ]

    results = []
    for query in queries:
        result = qa.query(query)
        results.append(result)
        assert result['answer'] is not None, f"No answer for: {query}"

    print(f"\n✓ CVE queries: {len(results)} passed")
    return results

def test_attack_queries():
    """Test ATT&CK-related queries."""

    qa = CyberSecurityQuery()

    queries = [
        "What is technique T1059?",
        "What tactics does technique T1059 belong to?",
        "What attack techniques target Linux systems?",
        "What mitigations exist for privilege escalation?"
    ]

    results = []
    for query in queries:
        result = qa.query(query)
        results.append(result)
        assert result['answer'] is not None, f"No answer for: {query}"

    print(f"✓ ATT&CK queries: {len(results)} passed")
    return results

def test_threat_actor_queries():
    """Test threat actor queries."""

    qa = CyberSecurityQuery()

    queries = [
        "What techniques does APT29 use?",
        "List threat actors targeting financial sector",
        "What malware is used by APT28?"
    ]

    results = []
    for query in queries:
        result = qa.query(query)
        results.append(result)
        # Note: These may not have answers if test data doesn't include them

    print(f"✓ Threat actor queries: {len(results)} executed")
    return results

def test_reasoning_queries():
    """Test complex reasoning queries."""

    qa = CyberSecurityQuery()

    queries = [
        "What vulnerabilities can lead to privilege escalation?",
        "What is the relationship between CVE-2023-1234 and CWE-79?",
        "What attack path uses SQL injection?",
        "How can ransomware be mitigated?"
    ]

    results = []
    for query in queries:
        result = qa.query(query)
        results.append(result)

    print(f"✓ Reasoning queries: {len(results)} executed")
    return results

def run_all_tests():
    """Run all test suites."""

    print("=" * 80)
    print("Cybersecurity Knowledge Base Test Suite")
    print("=" * 80)

    try:
        test_cve_queries()
        test_attack_queries()
        test_threat_actor_queries()
        test_reasoning_queries()

        print("\n" + "=" * 80)
        print("All tests completed successfully!")
        print("=" * 80)

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
```

2. **Run tests:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB

# Run test suite
python tests/test_queries.py
```

**Expected Output:**
```
================================================================================
Cybersecurity Knowledge Base Test Suite
================================================================================

Question: What is CVE-2023-1234?
...
✓ CVE queries: 4 passed

Question: What is technique T1059?
...
✓ ATT&CK queries: 4 passed

✓ Threat actor queries: 3 executed
✓ Reasoning queries: 4 executed

================================================================================
All tests completed successfully!
================================================================================
```

**Verification:**
```bash
# Run specific test
python tests/test_queries.py
```

---

### Task 6.3: Create Validation Queries
**Prerequisites:** Task 6.2
**Duration:** 2 hours
**Priority:** Medium

**Steps:**

1. **Create validation script:**
```python
# Save as: scripts/validate_kg.py
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from neo4j import GraphDatabase

def validate_knowledge_graph():
    """Validate knowledge graph structure and content."""

    # Neo4j connection
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "neo4j@openspg"

    driver = GraphDatabase.driver(uri, auth=(user, password))

    print("=" * 80)
    print("Knowledge Graph Validation")
    print("=" * 80)

    with driver.session() as session:
        # Check node counts
        print("\n1. Node Counts:")
        result = session.run("""
            MATCH (n) WHERE n.namespace = 'CyberSecurityKB'
            RETURN labels(n)[0] as Type, count(*) as Count
            ORDER BY Count DESC
        """)
        for record in result:
            print(f"   {record['Type']}: {record['Count']:,}")

        # Check relationship counts
        print("\n2. Relationship Counts:")
        result = session.run("""
            MATCH ()-[r]->() WHERE r.namespace = 'CyberSecurityKB'
            RETURN type(r) as RelationType, count(*) as Count
            ORDER BY Count DESC
        """)
        for record in result:
            print(f"   {record['RelationType']}: {record['Count']:,}")

        # Check high-severity vulnerabilities
        print("\n3. High-Severity Vulnerabilities (CVSS >= 9.0):")
        result = session.run("""
            MATCH (v:Vulnerability)
            WHERE v.namespace = 'CyberSecurityKB' AND v.cvss_score >= 9.0
            RETURN v.cve_id, v.cvss_score
            ORDER BY v.cvss_score DESC
            LIMIT 10
        """)
        for record in result:
            print(f"   {record['v.cve_id']}: {record['v.cvss_score']}")

        # Check ATT&CK techniques by tactic
        print("\n4. ATT&CK Techniques by Tactic:")
        result = session.run("""
            MATCH (t:AttackTechnique)
            WHERE t.namespace = 'CyberSecurityKB'
            WITH t.tactic as Tactic, count(*) as Count
            RETURN Tactic, Count
            ORDER BY Count DESC
            LIMIT 10
        """)
        for record in result:
            print(f"   {record['Tactic']}: {record['Count']}")

        # Check top CWEs
        print("\n5. Top 10 CWEs:")
        result = session.run("""
            MATCH (w:Weakness)
            WHERE w.namespace = 'CyberSecurityKB'
            RETURN w.cwe_id, w.name
            LIMIT 10
        """)
        for record in result:
            print(f"   {record['w.cwe_id']}: {record['w.name']}")

        # Check connectivity
        print("\n6. Graph Connectivity:")
        result = session.run("""
            MATCH (n) WHERE n.namespace = 'CyberSecurityKB'
            OPTIONAL MATCH (n)-[r]-()
            WITH n, count(r) as degree
            RETURN avg(degree) as AvgDegree, max(degree) as MaxDegree, min(degree) as MinDegree
        """)
        for record in result:
            print(f"   Average Degree: {record['AvgDegree']:.2f}")
            print(f"   Max Degree: {record['MaxDegree']}")
            print(f"   Min Degree: {record['MinDegree']}")

    driver.close()

    print("\n" + "=" * 80)
    print("Validation Complete")
    print("=" * 80)

if __name__ == "__main__":
    validate_knowledge_graph()
```

2. **Run validation:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB

# Install neo4j driver if needed
pip install neo4j

# Run validation
python scripts/validate_kg.py
```

**Expected Output:**
```
================================================================================
Knowledge Graph Validation
================================================================================

1. Node Counts:
   Vulnerability: 40,000
   KnowledgeUnit: 44,000
   AttackTechnique: 3,000
   Weakness: 900
   ...

2. Relationship Counts:
   exploits: 15,000
   uses_technique: 8,000
   related_to: 12,000
   ...

3. High-Severity Vulnerabilities (CVSS >= 9.0):
   CVE-2023-1234: 9.8
   CVE-2024-5678: 9.5
   ...

4. ATT&CK Techniques by Tactic:
   Execution: 450
   Persistence: 380
   ...

5. Top 10 CWEs:
   CWE-79: Cross-site Scripting (XSS)
   CWE-89: SQL Injection
   ...

6. Graph Connectivity:
   Average Degree: 3.5
   Max Degree: 150
   Min Degree: 0

================================================================================
Validation Complete
================================================================================
```

**Verification:**
```bash
# Manual Neo4j queries
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (v:Vulnerability)-[r:exploits]->(w:Weakness) RETURN count(r) LIMIT 1"
```

---

## Phase 7: Documentation and Deployment (Week 6)

### Task 7.1: Create Usage Documentation
**Prerequisites:** Task 6.3
**Duration:** 3 hours
**Priority:** Medium

**Create comprehensive documentation:**

```bash
cd /home/jim/2_OXOT_Projects_Dev/KAG/kag/examples/cybersecurity/CyberSecurityKB/docs

# Create USAGE.md
cat > USAGE.md << 'EOF'
# Cybersecurity Knowledge Base - Usage Guide

## Query Examples

### CVE Queries
- "What is CVE-2024-1234?"
- "What is the CVSS score of CVE-2023-5678?"
- "List critical vulnerabilities from 2024"

### ATT&CK Queries
- "What is technique T1059?"
- "What techniques are used for privilege escalation?"
- "What mitigations exist for lateral movement?"

### Threat Intelligence Queries
- "What techniques does APT29 use?"
- "List ransomware families"
- "What malware exploits CVE-2023-1234?"

## API Usage

```python
from solver.qa import CyberSecurityQuery

qa = CyberSecurityQuery()
result = qa.query("What is CVE-2024-1234?")
print(result['answer'])
```

## Maintenance

### Update Data
```bash
cd builder
# Update data files in data/{attack,cve,cwe}/
python indexer.py
```

### Backup
```bash
docker exec openspg-neo4j neo4j-admin database dump neo4j \
  --to-path=/shared/backup_$(date +%Y%m%d).dump
```
EOF
```

---

### Task 7.2: Create Deployment Scripts
**Prerequisites:** Task 7.1
**Duration:** 2 hours
**Priority:** Low

**Create automation scripts for easy deployment and updates.**

---

### Task 7.3: Performance Tuning
**Prerequisites:** Task 6.3
**Duration:** 4 hours
**Priority:** Medium

**Optimize query performance:**

1. Create Neo4j indexes
2. Tune KAG configuration parameters
3. Benchmark query performance
4. Optimize frequently-used queries

---

## Summary and Next Steps

### Completion Checklist

- [ ] Phase 1: Environment Preparation (Week 1)
- [ ] Phase 2: Project Initialization (Week 1-2)
- [ ] Phase 3: Schema Development (Week 2-3)
- [ ] Phase 4: Data Source Integration (Week 3-4)
- [ ] Phase 5: Knowledge Graph Building (Week 4-5)
- [ ] Phase 6: Query and Testing (Week 5-6)
- [ ] Phase 7: Documentation and Deployment (Week 6)

### Success Metrics

**Data Completeness:**
- ✓ 40,000+ CVE vulnerabilities loaded
- ✓ 3,000+ ATT&CK techniques loaded
- ✓ 900+ CWE weaknesses loaded
- ✓ 100,000+ relationships created

**Query Performance:**
- ✓ Simple queries: < 2 seconds
- ✓ Complex reasoning: < 5 seconds
- ✓ Graph traversal: < 3 seconds

**Accuracy:**
- ✓ Entity extraction: > 85% accuracy
- ✓ Relationship extraction: > 80% accuracy
- ✓ Query relevance: > 90% accuracy

### Next Steps

1. **Expand Data Sources:**
   - Add STIX 2.1 threat intelligence feeds
   - Integrate MISP indicators
   - Add ICS-specific data (IEC 62443)

2. **Enhance Schema:**
   - Add ICS/OT asset types
   - Implement compliance frameworks (IEC 62443, ISO 27001)
   - Add risk assessment entities

3. **Improve Query Capabilities:**
   - Implement attack path analysis
   - Add risk propagation queries
   - Create compliance gap analysis

4. **Integration:**
   - REST API wrapper
   - Web UI dashboard
   - SIEM integration

5. **Production Deployment:**
   - Kubernetes deployment
   - High availability configuration
   - Monitoring and alerting

---

## Troubleshooting

### Common Issues

**Issue 1: OpenSPG Connection Failed**
```bash
# Check services
docker ps | grep openspg
docker-compose logs openspg-server

# Restart if needed
docker-compose restart openspg-server
```

**Issue 2: Neo4j Out of Memory**
```bash
# Increase Neo4j memory in docker-compose.yml
NEO4J_dbms_memory_heap_max__size: 4G
NEO4J_dbms_memory_pagecache_size: 2G

docker-compose restart openspg-neo4j
```

**Issue 3: Builder Pipeline Slow**
```bash
# Increase parallel chains in kag_config.yaml
num_chains: 16  # Increase based on CPU cores

# Use local LLM for speed
# Switch to Ollama instead of OpenAI API
```

**Issue 4: Query Returns No Results**
```bash
# Verify data in Neo4j
docker exec openspg-neo4j cypher-shell -u neo4j -p "neo4j@openspg" \
  "MATCH (n) WHERE n.namespace = 'CyberSecurityKB' RETURN count(n)"

# Check entity linking threshold in config
# Lower recognition_threshold if needed (0.8 -> 0.7)
```

---

## Resources

### Documentation
- **KAG Framework:** https://github.com/OpenSPG/KAG
- **OpenSPG:** https://github.com/OpenSPG/openspg
- **UCO Ontology:** https://github.com/Ebiquity/Unified-Cybersecurity-Ontology
- **MITRE ATT&CK:** https://attack.mitre.org/
- **NVD CVE:** https://nvd.nist.gov/
- **CWE:** https://cwe.mitre.org/

### Community
- **OpenSPG Discussions:** https://github.com/OpenSPG/openspg/discussions
- **KAG Issues:** https://github.com/OpenSPG/KAG/issues

---

**End of Implementation Plan**
**Last Updated:** 2025-10-26 22:30:00 UTC
**Version:** v1.0.0
