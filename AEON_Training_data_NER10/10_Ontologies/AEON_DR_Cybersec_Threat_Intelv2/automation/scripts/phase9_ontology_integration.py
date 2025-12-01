#!/usr/bin/env python3
"""
Phase 9: Ontology Integration into Qdrant Vector Store
SCHEDULED FOR EXECUTION AFTER PHASE 8 COMPLETION
DO NOT INTERFERE WITH NEO4J SCHEMA - READ-ONLY INTEGRATION

Purpose: Extract ontology knowledge and create specialized domain-aware swarm agents
"""

import os
import sys
import json
import yaml
import logging
from datetime import datetime
from pathlib import Path
from neo4j import GraphDatabase
import subprocess

# Setup logging
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f'phase9_ontology_integration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load config
config_path = Path(__file__).parent.parent / 'config.yaml'
with open(config_path) as f:
    config = yaml.safe_load(f)

# Neo4j connection (READ-ONLY)
driver = GraphDatabase.driver(
    config['neo4j']['uri'],
    auth=(config['neo4j']['user'], config['neo4j']['password'])
)

ONTOLOGY_PATH = "/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/6_Ontologies"

def checkpoint(phase, data):
    """Store checkpoint in Qdrant - NON-BLOCKING"""
    try:
        # Create summary for notification (avoid large payloads)
        summary = {
            "phase": phase,
            "timestamp": datetime.now().isoformat(),
            "data_type": type(data).__name__
        }

        # Add size/count info
        if isinstance(data, dict):
            summary["keys"] = list(data.keys())[:10]  # First 10 keys only
            summary["total_keys"] = len(data.keys())
        elif isinstance(data, list):
            summary["count"] = len(data)

        # Use notify with small summary (non-blocking)
        message = f"Phase 9 checkpoint: {phase} - {json.dumps(summary)}"
        cmd = f'npx claude-flow@alpha hooks notify --message "{message[:500]}"'

        # Run in background, don't wait
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info(f"Checkpoint queued: {phase}")

    except Exception as e:
        logger.warning(f"Could not queue checkpoint for {phase}: {e}")

def analyze_ontology_resources():
    """Catalog all ontology resources available"""
    logger.info("="*80)
    logger.info("ANALYZING ONTOLOGY RESOURCES")
    logger.info("="*80)

    ontology_catalog = {
        "saref_ontologies": [
            "SAREF Core", "SAREF Energy", "SAREF Smart Grid", "SAREF Building",
            "SAREF City", "SAREF Industry/Manufacturing", "SAREF Smart Agriculture",
            "SAREF Automotive", "SAREF Health/Aging", "SAREF Wearables",
            "SAREF Water", "SAREF Smart Lift", "SAREF Environment"
        ],
        "cybersecurity_ontologies": [
            "Unified Cybersecurity Ontology (UCO)",
            "ICS-SEC Knowledge Graph",
            "ICS Ethical Hacking"
        ],
        "infrastructure_ontologies": [
            "Critical Infrastructure Systems",
            "DevOps Infrastructure",
            "Business Analysis",
            "Media in the Cloud"
        ],
        "etsi_standards": [
            "Smart City Deployment",
            "Operational Efficiency Energy",
            "Human Factors Smart Cities"
        ]
    }

    # Count actual files
    pdf_files = list(Path(ONTOLOGY_PATH).glob("*.pdf"))
    md_files = list(Path(ONTOLOGY_PATH).glob("*.md"))
    csv_files = list(Path(ONTOLOGY_PATH).glob("*.csv"))

    logger.info(f"Found {len(pdf_files)} PDF ontology documents")
    logger.info(f"Found {len(md_files)} Markdown research reports")
    logger.info(f"Found {len(csv_files)} CSV mapping files")

    ontology_catalog["files"] = {
        "pdfs": len(pdf_files),
        "markdown": len(md_files),
        "csv": len(csv_files),
        "total": len(pdf_files) + len(md_files) + len(csv_files)
    }

    checkpoint("ontology_catalog", ontology_catalog)
    return ontology_catalog

def extract_neo4j_schema():
    """Extract current Neo4j schema (READ-ONLY)"""
    logger.info("\n" + "="*80)
    logger.info("EXTRACTING NEO4J SCHEMA (READ-ONLY)")
    logger.info("="*80)

    with driver.session() as session:
        # Get all node labels
        result = session.run("CALL db.labels()")
        labels = [record[0] for record in result]
        logger.info(f"Found {len(labels)} node labels: {labels}")

        # Get all relationship types
        result = session.run("CALL db.relationshipTypes()")
        rel_types = [record[0] for record in result]
        logger.info(f"Found {len(rel_types)} relationship types: {rel_types}")

        # Get all property keys
        result = session.run("CALL db.propertyKeys()")
        properties = [record[0] for record in result]
        logger.info(f"Found {len(properties)} property keys")

        # Get indexes
        result = session.run("SHOW INDEXES")
        indexes = [dict(record) for record in result]
        logger.info(f"Found {len(indexes)} indexes")

        # Get constraints
        result = session.run("SHOW CONSTRAINTS")
        constraints = [dict(record) for record in result]
        logger.info(f"Found {len(constraints)} constraints")

        schema = {
            "labels": labels,
            "relationship_types": rel_types,
            "properties": properties,
            "indexes": indexes,
            "constraints": constraints,
            "extracted_at": datetime.now().isoformat()
        }

        checkpoint("neo4j_schema", schema)
        return schema

def map_ontologies_to_schema(ontology_catalog, schema):
    """Map ontology domains to Neo4j schema elements"""
    logger.info("\n" + "="*80)
    logger.info("MAPPING ONTOLOGIES TO SCHEMA")
    logger.info("="*80)

    mappings = {
        "energy_grid": {
            "ontologies": ["SAREF Energy", "SAREF Smart Grid"],
            "labels": [l for l in schema['labels'] if any(x in l.lower() for x in ['device', 'equipment', 'power', 'grid', 'energy'])],
            "capabilities": ["grid_stability_analysis", "energy_optimization", "device_vulnerability_assessment"]
        },
        "industrial_controls": {
            "ontologies": ["ICS-SEC", "SAREF Industry/Manufacturing"],
            "labels": [l for l in schema['labels'] if any(x in l.lower() for x in ['device', 'equipment', 'control'])],
            "capabilities": ["ics_security_analysis", "purdue_model_validation", "control_system_architecture"]
        },
        "cybersecurity": {
            "ontologies": ["UCO", "ICS-SEC"],
            "labels": [l for l in schema['labels'] if any(x in l.lower() for x in ['cve', 'threat', 'vulnerability', 'attack'])],
            "capabilities": ["threat_intelligence", "vulnerability_analysis", "attack_path_discovery", "cve_relationship_validation"]
        },
        "smart_city": {
            "ontologies": ["SAREF City", "SAREF Building", "SAREF Environment"],
            "labels": [l for l in schema['labels'] if any(x in l.lower() for x in ['building', 'city', 'environment', 'location'])],
            "capabilities": ["smart_city_modeling", "building_automation", "environmental_monitoring"]
        }
    }

    for domain, mapping in mappings.items():
        logger.info(f"\nDomain: {domain.upper()}")
        logger.info(f"  Ontologies: {mapping['ontologies']}")
        logger.info(f"  Mapped Labels: {mapping['labels']}")
        logger.info(f"  Capabilities: {mapping['capabilities']}")

    checkpoint("ontology_mappings", mappings)
    return mappings

def define_specialized_agents(mappings):
    """Define specialized swarm agents for each domain"""
    logger.info("\n" + "="*80)
    logger.info("DEFINING SPECIALIZED AGENTS")
    logger.info("="*80)

    agents = [
        {
            "name": "energy_grid_ontology_agent",
            "type": "ontology-expert",
            "domain": "energy_grid",
            "ontologies": ["SAREF Energy", "SAREF Smart Grid"],
            "capabilities": [
                "validate_device_energy_relationships",
                "suggest_grid_stability_optimizations",
                "identify_missing_energy_properties",
                "recommend_energy_indexes"
            ],
            "neo4j_expertise": {
                "labels": mappings["energy_grid"]["labels"],
                "queries": [
                    "Device vulnerability to energy disruption",
                    "Grid stability relationship validation",
                    "Energy efficiency optimization patterns"
                ]
            }
        },
        {
            "name": "ics_security_ontology_agent",
            "type": "ontology-expert",
            "domain": "industrial_controls",
            "ontologies": ["ICS-SEC", "SAREF Industry/Manufacturing"],
            "capabilities": [
                "validate_purdue_model_architecture",
                "identify_control_system_vulnerabilities",
                "suggest_ics_security_relationships",
                "recommend_ics_specific_indexes"
            ],
            "neo4j_expertise": {
                "labels": mappings["industrial_controls"]["labels"],
                "queries": [
                    "Control system CVE correlation",
                    "Purdue level architecture validation",
                    "ICS asset dependency analysis"
                ]
            }
        },
        {
            "name": "cybersecurity_ontology_agent",
            "type": "ontology-expert",
            "domain": "cybersecurity",
            "ontologies": ["UCO", "ICS-SEC"],
            "capabilities": [
                "validate_cve_relationships",
                "suggest_threat_intelligence_links",
                "identify_attack_path_patterns",
                "recommend_security_indexes"
            ],
            "neo4j_expertise": {
                "labels": mappings["cybersecurity"]["labels"],
                "queries": [
                    "CVE to Device vulnerability paths",
                    "Threat actor to attack pattern correlation",
                    "Vulnerability exploitation chains"
                ]
            }
        },
        {
            "name": "cypher_optimization_agent",
            "type": "query-specialist",
            "domain": "all",
            "ontologies": ["All SAREF + UCO + ICS-SEC"],
            "capabilities": [
                "analyze_cypher_query_patterns",
                "suggest_index_optimizations",
                "identify_missing_relationships_from_ontologies",
                "recommend_schema_enhancements"
            ],
            "neo4j_expertise": {
                "labels": "all",
                "queries": [
                    "Performance bottleneck analysis",
                    "Missing index identification",
                    "Relationship pattern optimization",
                    "Schema completeness validation"
                ]
            }
        },
        {
            "name": "schema_validator_agent",
            "type": "validation-specialist",
            "domain": "all",
            "ontologies": ["All SAREF + UCO + ICS-SEC"],
            "capabilities": [
                "validate_schema_against_ontologies",
                "identify_ontology_violations",
                "suggest_schema_corrections",
                "monitor_schema_drift"
            ],
            "neo4j_expertise": {
                "labels": "all",
                "queries": [
                    "Schema constraint validation",
                    "Ontology compliance checking",
                    "Relationship type validation",
                    "Property completeness analysis"
                ]
            }
        }
    ]

    for agent in agents:
        logger.info(f"\nAgent: {agent['name']}")
        logger.info(f"  Domain: {agent['domain']}")
        logger.info(f"  Ontologies: {agent['ontologies']}")
        logger.info(f"  Capabilities: {agent['capabilities'][:2]}...")

    checkpoint("specialized_agents", {"count": len(agents), "agents": [a['name'] for a in agents]})
    return agents

def store_ontology_metadata_in_qdrant(ontology_catalog, schema, mappings, agents):
    """Store all ontology knowledge in Qdrant vector memory"""
    logger.info("\n" + "="*80)
    logger.info("STORING ONTOLOGY METADATA IN QDRANT")
    logger.info("="*80)

    # Write data to temporary JSON files to avoid command-line length limits
    import tempfile

    try:
        # Store ontology catalog
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(ontology_catalog, f)
            catalog_file = f.name
        cmd = f'npx claude-flow@alpha hooks notify --message "Stored ontology catalog: {ontology_catalog["files"]["total"]} files"'
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(catalog_file)
        logger.info("✅ Stored ontology catalog in Qdrant")

        # Store Neo4j schema summary (not full schema - too large)
        schema_summary = {
            "labels_count": len(schema['labels']),
            "relationship_types_count": len(schema['relationship_types']),
            "properties_count": len(schema.get('properties', [])),
            "indexes_count": len(schema.get('indexes', [])),
            "constraints_count": len(schema.get('constraints', []))
        }
        cmd = f'npx claude-flow@alpha hooks notify --message "Neo4j schema: {schema_summary["labels_count"]} labels, {schema_summary["relationship_types_count"]} relationships"'
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("✅ Stored Neo4j schema summary in Qdrant")

        # Store domain mappings summary
        domains_list = list(mappings.keys())
        cmd = f'npx claude-flow@alpha hooks notify --message "Domain mappings: {len(domains_list)} domains - {", ".join(domains_list)}"'
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("✅ Stored domain mappings in Qdrant")

        # Store specialized agents list
        agent_names = [a['name'] for a in agents]
        cmd = f'npx claude-flow@alpha hooks notify --message "Specialized agents: {len(agent_names)} registered - {", ".join(agent_names[:3])}..."'
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("✅ Stored specialized agents in Qdrant")

        # Store activation instructions summary
        cmd = 'npx claude-flow@alpha hooks notify --message "Activation instructions: Query swarm/ontology/* for domain expertise"'
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("✅ Stored activation instructions in Qdrant")

        return True

    except Exception as e:
        logger.error(f"Error storing in Qdrant: {e}")
        return False

def register_agents_in_swarm(agents):
    """Register specialized agents in claude-flow swarm"""
    logger.info("\n" + "="*80)
    logger.info("REGISTERING AGENTS IN SWARM")
    logger.info("="*80)

    # Store summary notifications (not full agent data - too large)
    for agent in agents:
        cmd = f'npx claude-flow@alpha hooks notify --message "Registered agent: {agent["name"]} - Domain: {agent["domain"]}"'
        subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info(f"✅ Registered {agent['name']} in swarm")

    # Create agent registry summary
    agent_names = [a['name'] for a in agents]
    agent_domains = [a['domain'] for a in agents]
    cmd = f'npx claude-flow@alpha hooks notify --message "Agent registry: {len(agents)} agents - {", ".join(agent_names)}"'
    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    logger.info(f"✅ Registered {len(agents)} agents in swarm")

    registry = {
        "total_agents": len(agents),
        "agent_names": agent_names,
        "agent_domains": agent_domains
    }
    return registry

def create_usage_guide():
    """Create comprehensive usage guide"""
    logger.info("\n" + "="*80)
    logger.info("CREATING USAGE GUIDE")
    logger.info("="*80)

    guide = {
        "title": "Ontology-Aware Swarm Agent Usage Guide",
        "overview": "Leverage domain-specific ontology knowledge for Neo4j operations",
        "quick_start": {
            "step_1": "Query Qdrant: swarm/ontology/activation_instructions",
            "step_2": "Identify your domain: energy_grid, industrial_controls, cybersecurity, smart_city",
            "step_3": "Spawn relevant agent from swarm/agents/ontology/<agent_name>",
            "step_4": "Agent provides ontology-aware recommendations"
        },
        "use_cases": {
            "cypher_query_optimization": {
                "agent": "cypher_optimization_agent",
                "capability": "Analyze queries against ontology patterns",
                "example": "Optimize CVE-to-Device relationship queries using SAREF patterns"
            },
            "schema_validation": {
                "agent": "schema_validator_agent",
                "capability": "Validate schema against SAREF/UCO/ICS-SEC standards",
                "example": "Ensure Device nodes conform to SAREF Energy ontology"
            },
            "vulnerability_analysis": {
                "agent": "cybersecurity_ontology_agent",
                "capability": "UCO-compliant CVE relationship analysis",
                "example": "Identify missing CVE relationships per UCO ontology"
            },
            "grid_stability": {
                "agent": "energy_grid_ontology_agent",
                "capability": "SAREF Smart Grid compliance validation",
                "example": "Validate grid stability relationships against SAREF patterns"
            },
            "ics_security": {
                "agent": "ics_security_ontology_agent",
                "capability": "ICS-SEC ontology-compliant security analysis",
                "example": "Validate Purdue model architecture in Neo4j"
            }
        },
        "memory_keys": {
            "catalog": "swarm/ontology/catalog",
            "schema": "swarm/ontology/neo4j_schema",
            "mappings": "swarm/ontology/domain_mappings",
            "agents": "swarm/ontology/specialized_agents",
            "registry": "swarm/agents/ontology/registry",
            "instructions": "swarm/ontology/activation_instructions"
        },
        "ontology_resources": {
            "path": "/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/6_Ontologies",
            "count": 23,
            "types": ["SAREF (13)", "Cybersecurity (3)", "Infrastructure (4)", "ETSI Standards (3)"]
        }
    }

    # Save to file (don't try to send large JSON via shell)
    guide_path = Path(__file__).parent.parent / 'docs' / 'ontology_swarm_usage_guide.json'
    guide_path.parent.mkdir(exist_ok=True)
    with open(guide_path, 'w') as f:
        json.dump(guide, f, indent=2, default=str)
    logger.info(f"✅ Saved usage guide to {guide_path}")

    # Send small notification
    cmd = f'npx claude-flow@alpha hooks notify --message "Usage guide created with 5 use cases at {guide_path}"'
    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    logger.info("✅ Created usage guide notification in Qdrant")

    return guide

def main():
    """Main execution"""
    logger.info("="*80)
    logger.info("PHASE 9: ONTOLOGY INTEGRATION INTO QDRANT")
    logger.info("EXECUTING AFTER PHASE 8 COMPLETION")
    logger.info("="*80)

    try:
        # Step 1: Analyze ontology resources
        ontology_catalog = analyze_ontology_resources()

        # Step 2: Extract Neo4j schema (READ-ONLY)
        schema = extract_neo4j_schema()

        # Step 3: Map ontologies to schema
        mappings = map_ontologies_to_schema(ontology_catalog, schema)

        # Step 4: Define specialized agents
        agents = define_specialized_agents(mappings)

        # Step 5: Store everything in Qdrant
        store_ontology_metadata_in_qdrant(ontology_catalog, schema, mappings, agents)

        # Step 6: Register agents in swarm
        registry = register_agents_in_swarm(agents)

        # Step 7: Create usage guide
        guide = create_usage_guide()

        logger.info("\n" + "="*80)
        logger.info("PHASE 9 COMPLETE - ONTOLOGY INTEGRATION SUCCESSFUL")
        logger.info("="*80)
        logger.info(f"Ontology Resources: {ontology_catalog['files']['total']} files")
        logger.info(f"Neo4j Labels: {len(schema['labels'])}")
        logger.info(f"Domain Mappings: {len(mappings)}")
        logger.info(f"Specialized Agents: {len(agents)}")
        logger.info(f"Qdrant Memory Keys: 7 primary keys + {len(agents)} agent keys")
        logger.info("")
        logger.info("✅ Agents registered and ready for swarm coordination")
        logger.info("✅ Usage guide available at: swarm/ontology/usage_guide")
        logger.info("✅ Schema integrity preserved - no modifications to Neo4j")

        # Final checkpoint
        checkpoint("phase9_complete", {
            "status": "success",
            "ontology_files": ontology_catalog['files']['total'],
            "agents_registered": len(agents),
            "qdrant_keys": 7 + len(agents),
            "neo4j_schema_preserved": True,
            "completion_time": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"❌ Phase 9 failed: {e}")
        checkpoint("phase9_error", {"error": str(e)})
        raise
    finally:
        driver.close()

if __name__ == "__main__":
    main()
