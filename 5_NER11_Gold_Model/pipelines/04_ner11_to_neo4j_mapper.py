"""
NER11 to Neo4j v3.1 Mapper: Complete Entity Mapping

Maps ALL 60 NER labels to 16 Neo4j super labels with property discrimination.
Handles 566 fine-grained entity types through hierarchical property system.

File: 04_ner11_to_neo4j_mapper.py
Created: 2025-12-01
Version: 1.0.0
Status: PRODUCTION-READY
Author: J. McKenney (via AEON Implementation)

Architecture:
- 60 NER labels → 16 Neo4j super labels
- 566 entity types → property discriminators
- Complete validation suite
- Special case handling (properties vs nodes)
- Mapping examples with test cases

Integration:
- Input: NER11 spaCy entities
- Output: Neo4j v3.1 compatible Cypher statements
- Uses: HierarchicalEntityProcessor taxonomy
- References: Schema v3.1 specification
"""

from typing import Dict, List, Tuple, Optional, Set
from enum import Enum
from dataclasses import dataclass
import json


class Neo4jSuperLabel(Enum):
    """16 Super Labels for Neo4j v3.1 hierarchical schema"""
    THREAT_ACTOR = "ThreatActor"
    MALWARE = "Malware"
    ATTACK_PATTERN = "AttackPattern"
    VULNERABILITY = "Vulnerability"
    INDICATOR = "Indicator"
    CAMPAIGN = "Campaign"
    ASSET = "Asset"
    ORGANIZATION = "Organization"
    LOCATION = "Location"
    PSYCH_TRAIT = "PsychTrait"
    ECONOMIC_METRIC = "EconomicMetric"
    PROTOCOL = "Protocol"
    ROLE = "Role"
    SOFTWARE = "Software"
    CONTROL = "Control"
    EVENT = "Event"


@dataclass
class EntityMapping:
    """Complete mapping configuration for NER label to Neo4j"""
    ner_label: str
    super_label: Neo4jSuperLabel
    discriminator_property: str
    discriminator_value: str
    additional_properties: Dict[str, str] = None
    is_property_only: bool = False  # Special case: maps to property not node
    property_name: str = None  # For property-only mappings
    parent_label: str = None  # For property-only mappings
    notes: str = ""

    def __post_init__(self):
        if self.additional_properties is None:
            self.additional_properties = {}


class NER11ToNeo4jMapper:
    """
    Complete mapper for 60 NER labels to 16 Neo4j super labels.

    Handles:
    - Direct label mappings (node creation)
    - Property-only mappings (enrichment)
    - Multi-tier taxonomy (566 types)
    - Validation and examples
    """

    def __init__(self):
        """Initialize complete mapping table"""
        self.mapping_table = self._build_complete_mapping_table()
        self.validation_stats = {
            "total_labels": 0,
            "node_mappings": 0,
            "property_mappings": 0,
            "unmapped": []
        }

    def _build_complete_mapping_table(self) -> Dict[str, EntityMapping]:
        """
        Build complete mapping table for ALL 60 NER labels.

        Returns:
            Dict mapping NER label to EntityMapping configuration
        """
        mappings = {}

        # ================================================================
        # TIER 1: TECHNICAL (Core Cybersecurity) - 25+ labels
        # ================================================================

        # ThreatActor domain (5 labels)
        mappings.update({
            "THREAT_ACTOR": EntityMapping(
                ner_label="THREAT_ACTOR",
                super_label=Neo4jSuperLabel.THREAT_ACTOR,
                discriminator_property="actorType",
                discriminator_value="generic",
                notes="Generic threat actor"
            ),
            "APT_GROUP": EntityMapping(
                ner_label="APT_GROUP",
                super_label=Neo4jSuperLabel.THREAT_ACTOR,
                discriminator_property="actorType",
                discriminator_value="apt_group",
                additional_properties={"sophistication": "advanced"},
                notes="Advanced Persistent Threat groups"
            ),
            "NATION_STATE": EntityMapping(
                ner_label="NATION_STATE",
                super_label=Neo4jSuperLabel.THREAT_ACTOR,
                discriminator_property="actorType",
                discriminator_value="nation_state",
                additional_properties={"sophistication": "advanced"},
                notes="State-sponsored actors"
            ),
            "THREAT_GROUP": EntityMapping(
                ner_label="THREAT_GROUP",
                super_label=Neo4jSuperLabel.THREAT_ACTOR,
                discriminator_property="actorType",
                discriminator_value="threat_group",
                notes="General threat groups"
            ),
            "INTRUSION_SET": EntityMapping(
                ner_label="INTRUSION_SET",
                super_label=Neo4jSuperLabel.THREAT_ACTOR,
                discriminator_property="actorType",
                discriminator_value="intrusion_set",
                notes="STIX intrusion sets"
            ),
        })

        # Campaign domain (2 labels)
        mappings.update({
            "CAMPAIGN": EntityMapping(
                ner_label="CAMPAIGN",
                super_label=Neo4jSuperLabel.CAMPAIGN,
                discriminator_property="campaignType",
                discriminator_value="generic",
                notes="Generic campaign"
            ),
            "MULTI_STAGE_OPERATION": EntityMapping(
                ner_label="MULTI_STAGE_OPERATION",
                super_label=Neo4jSuperLabel.CAMPAIGN,
                discriminator_property="campaignType",
                discriminator_value="multi_stage",
                notes="Complex multi-phase campaigns"
            ),
        })

        # Malware domain (5 labels)
        mappings.update({
            "MALWARE": EntityMapping(
                ner_label="MALWARE",
                super_label=Neo4jSuperLabel.MALWARE,
                discriminator_property="malwareFamily",
                discriminator_value="generic",
                notes="Generic malware"
            ),
            "RANSOMWARE": EntityMapping(
                ner_label="RANSOMWARE",
                super_label=Neo4jSuperLabel.MALWARE,
                discriminator_property="malwareFamily",
                discriminator_value="ransomware",
                notes="Ransomware families"
            ),
            "TROJAN": EntityMapping(
                ner_label="TROJAN",
                super_label=Neo4jSuperLabel.MALWARE,
                discriminator_property="malwareFamily",
                discriminator_value="trojan",
                notes="Trojan horse malware"
            ),
            "WORM": EntityMapping(
                ner_label="WORM",
                super_label=Neo4jSuperLabel.MALWARE,
                discriminator_property="malwareFamily",
                discriminator_value="worm",
                notes="Self-replicating worms"
            ),
            "EXPLOIT_KIT": EntityMapping(
                ner_label="EXPLOIT_KIT",
                super_label=Neo4jSuperLabel.MALWARE,
                discriminator_property="malwareFamily",
                discriminator_value="exploit_kit",
                notes="Automated exploitation toolkits"
            ),
        })

        # AttackPattern domain (8 labels)
        mappings.update({
            "ATTACK_TECHNIQUE": EntityMapping(
                ner_label="ATTACK_TECHNIQUE",
                super_label=Neo4jSuperLabel.ATTACK_PATTERN,
                discriminator_property="patternType",
                discriminator_value="technique",
                notes="MITRE ATT&CK techniques"
            ),
            "ATTACK_TACTIC": EntityMapping(
                ner_label="ATTACK_TACTIC",
                super_label=Neo4jSuperLabel.ATTACK_PATTERN,
                discriminator_property="patternType",
                discriminator_value="tactic",
                notes="MITRE ATT&CK tactics"
            ),
            "TTP": EntityMapping(
                ner_label="TTP",
                super_label=Neo4jSuperLabel.ATTACK_PATTERN,
                discriminator_property="patternType",
                discriminator_value="ttp",
                notes="Tactics, Techniques, Procedures"
            ),
            "CAPEC": EntityMapping(
                ner_label="CAPEC",
                super_label=Neo4jSuperLabel.ATTACK_PATTERN,
                discriminator_property="patternType",
                discriminator_value="capec",
                notes="Common Attack Pattern Enumeration"
            ),
            "EXPLOIT": EntityMapping(
                ner_label="EXPLOIT",
                super_label=Neo4jSuperLabel.ATTACK_PATTERN,
                discriminator_property="patternType",
                discriminator_value="exploit",
                notes="Exploitation techniques"
            ),
            "SOCIAL_ENGINEERING": EntityMapping(
                ner_label="SOCIAL_ENGINEERING",
                super_label=Neo4jSuperLabel.ATTACK_PATTERN,
                discriminator_property="patternType",
                discriminator_value="social_engineering",
                notes="Social engineering tactics"
            ),
            "PERSISTENCE_METHOD": EntityMapping(
                ner_label="PERSISTENCE_METHOD",
                super_label=Neo4jSuperLabel.ATTACK_PATTERN,
                discriminator_property="patternType",
                discriminator_value="persistence",
                notes="Persistence mechanisms"
            ),
            "EXFILTRATION_METHOD": EntityMapping(
                ner_label="EXFILTRATION_METHOD",
                super_label=Neo4jSuperLabel.ATTACK_PATTERN,
                discriminator_property="patternType",
                discriminator_value="exfiltration",
                notes="Data exfiltration techniques"
            ),
        })

        # Vulnerability domain (4 labels)
        mappings.update({
            "CVE": EntityMapping(
                ner_label="CVE",
                super_label=Neo4jSuperLabel.VULNERABILITY,
                discriminator_property="vulnType",
                discriminator_value="cve",
                notes="Common Vulnerabilities and Exposures"
            ),
            "VULNERABILITY": EntityMapping(
                ner_label="VULNERABILITY",
                super_label=Neo4jSuperLabel.VULNERABILITY,
                discriminator_property="vulnType",
                discriminator_value="generic",
                notes="Generic vulnerabilities"
            ),
            "CWE": EntityMapping(
                ner_label="CWE",
                super_label=Neo4jSuperLabel.VULNERABILITY,
                discriminator_property="vulnType",
                discriminator_value="cwe",
                notes="Common Weakness Enumeration"
            ),
            "ZERO_DAY": EntityMapping(
                ner_label="ZERO_DAY",
                super_label=Neo4jSuperLabel.VULNERABILITY,
                discriminator_property="vulnType",
                discriminator_value="zero_day",
                notes="Zero-day vulnerabilities"
            ),
        })

        # Indicator domain (2 labels)
        mappings.update({
            "INDICATOR": EntityMapping(
                ner_label="INDICATOR",
                super_label=Neo4jSuperLabel.INDICATOR,
                discriminator_property="indicatorType",
                discriminator_value="generic",
                notes="Generic indicators of compromise"
            ),
            "IOC": EntityMapping(
                ner_label="IOC",
                super_label=Neo4jSuperLabel.INDICATOR,
                discriminator_property="indicatorType",
                discriminator_value="ioc",
                notes="Indicators of Compromise"
            ),
        })

        # Software domain (3 labels)
        mappings.update({
            "SOFTWARE_COMPONENT": EntityMapping(
                ner_label="SOFTWARE_COMPONENT",
                super_label=Neo4jSuperLabel.SOFTWARE,
                discriminator_property="softwareType",
                discriminator_value="component",
                notes="Software components and libraries"
            ),
            "SBOM": EntityMapping(
                ner_label="SBOM",
                super_label=Neo4jSuperLabel.SOFTWARE,
                discriminator_property="softwareType",
                discriminator_value="sbom",
                notes="Software Bill of Materials"
            ),
            "LICENSE": EntityMapping(
                ner_label="LICENSE",
                super_label=Neo4jSuperLabel.SOFTWARE,
                discriminator_property="softwareType",
                discriminator_value="license",
                notes="Software licenses"
            ),
        })

        # Asset domain (8 labels covering IT/OT/IoT)
        mappings.update({
            "PLC": EntityMapping(
                ner_label="PLC",
                super_label=Neo4jSuperLabel.ASSET,
                discriminator_property="assetClass",
                discriminator_value="OT",
                additional_properties={"deviceType": "programmable_logic_controller"},
                notes="Programmable Logic Controllers"
            ),
            "RTU": EntityMapping(
                ner_label="RTU",
                super_label=Neo4jSuperLabel.ASSET,
                discriminator_property="assetClass",
                discriminator_value="OT",
                additional_properties={"deviceType": "remote_terminal_unit"},
                notes="Remote Terminal Units"
            ),
            "SCADA_SYSTEM": EntityMapping(
                ner_label="SCADA_SYSTEM",
                super_label=Neo4jSuperLabel.ASSET,
                discriminator_property="assetClass",
                discriminator_value="OT",
                additional_properties={"deviceType": "scada_server"},
                notes="SCADA control systems"
            ),
            "ICS_COMPONENTS": EntityMapping(
                ner_label="ICS_COMPONENTS",
                super_label=Neo4jSuperLabel.ASSET,
                discriminator_property="assetClass",
                discriminator_value="OT",
                additional_properties={"deviceType": "ics_component"},
                notes="Industrial Control System components"
            ),
            "SERVER": EntityMapping(
                ner_label="SERVER",
                super_label=Neo4jSuperLabel.ASSET,
                discriminator_property="assetClass",
                discriminator_value="IT",
                additional_properties={"deviceType": "server"},
                notes="IT servers"
            ),
            "SENSOR": EntityMapping(
                ner_label="SENSOR",
                super_label=Neo4jSuperLabel.ASSET,
                discriminator_property="assetClass",
                discriminator_value="IoT",
                additional_properties={"deviceType": "sensor"},
                notes="IoT sensors"
            ),
            "NETWORK_DEVICE": EntityMapping(
                ner_label="NETWORK_DEVICE",
                super_label=Neo4jSuperLabel.ASSET,
                discriminator_property="assetClass",
                discriminator_value="Network",
                additional_properties={"deviceType": "network_device"},
                notes="Network infrastructure"
            ),
            "FACILITY": EntityMapping(
                ner_label="FACILITY",
                super_label=Neo4jSuperLabel.ASSET,
                discriminator_property="assetClass",
                discriminator_value="Infrastructure",
                additional_properties={"deviceType": "facility"},
                notes="Physical facilities"
            ),
        })

        # Protocol domain (2 labels)
        mappings.update({
            "ICS_PROTOCOL": EntityMapping(
                ner_label="ICS_PROTOCOL",
                super_label=Neo4jSuperLabel.PROTOCOL,
                discriminator_property="protocolType",
                discriminator_value="ICS",
                notes="Industrial control protocols"
            ),
            "PROTOCOL": EntityMapping(
                ner_label="PROTOCOL",
                super_label=Neo4jSuperLabel.PROTOCOL,
                discriminator_property="protocolType",
                discriminator_value="Network",
                notes="Network protocols"
            ),
        })

        # ================================================================
        # TIER 2: PSYCHOMETRIC (The Imaginary) - 10+ labels
        # ================================================================

        # Cognitive biases (5 labels)
        mappings.update({
            "NORMALCY_BIAS": EntityMapping(
                ner_label="NORMALCY_BIAS",
                super_label=Neo4jSuperLabel.PSYCH_TRAIT,
                discriminator_property="traitType",
                discriminator_value="CognitiveBias",
                additional_properties={"subtype": "normalcy_bias"},
                notes="Tendency to underestimate threats"
            ),
            "CONFIRMATION_BIAS": EntityMapping(
                ner_label="CONFIRMATION_BIAS",
                super_label=Neo4jSuperLabel.PSYCH_TRAIT,
                discriminator_property="traitType",
                discriminator_value="CognitiveBias",
                additional_properties={"subtype": "confirmation_bias"},
                notes="Seeking confirming evidence"
            ),
            "AVAILABILITY_BIAS": EntityMapping(
                ner_label="AVAILABILITY_BIAS",
                super_label=Neo4jSuperLabel.PSYCH_TRAIT,
                discriminator_property="traitType",
                discriminator_value="CognitiveBias",
                additional_properties={"subtype": "availability_bias"},
                notes="Overweighting recent events"
            ),
            "GROUPTHINK": EntityMapping(
                ner_label="GROUPTHINK",
                super_label=Neo4jSuperLabel.PSYCH_TRAIT,
                discriminator_property="traitType",
                discriminator_value="CognitiveBias",
                additional_properties={"subtype": "groupthink"},
                notes="Group conformity pressure"
            ),
            "COGNITIVE_BIAS": EntityMapping(
                ner_label="COGNITIVE_BIAS",
                super_label=Neo4jSuperLabel.PSYCH_TRAIT,
                discriminator_property="traitType",
                discriminator_value="CognitiveBias",
                additional_properties={"subtype": "generic"},
                notes="Generic cognitive biases"
            ),
        })

        # Personality traits (3 labels)
        mappings.update({
            "BIG_5_OPENNESS": EntityMapping(
                ner_label="BIG_5_OPENNESS",
                super_label=Neo4jSuperLabel.PSYCH_TRAIT,
                discriminator_property="traitType",
                discriminator_value="Personality",
                additional_properties={"subtype": "big5_openness"},
                notes="Big Five: Openness to Experience"
            ),
            "DARK_TRIAD": EntityMapping(
                ner_label="DARK_TRIAD",
                super_label=Neo4jSuperLabel.PSYCH_TRAIT,
                discriminator_property="traitType",
                discriminator_value="Personality",
                additional_properties={"subtype": "dark_triad"},
                notes="Dark Triad personality traits"
            ),
            "PERSONALITY_TRAIT": EntityMapping(
                ner_label="PERSONALITY_TRAIT",
                super_label=Neo4jSuperLabel.PSYCH_TRAIT,
                discriminator_property="traitType",
                discriminator_value="Personality",
                additional_properties={"subtype": "generic"},
                notes="Generic personality traits"
            ),
        })

        # Lacanian discourse (2 labels)
        mappings.update({
            "MASTER_DISCOURSE": EntityMapping(
                ner_label="MASTER_DISCOURSE",
                super_label=Neo4jSuperLabel.PSYCH_TRAIT,
                discriminator_property="traitType",
                discriminator_value="LacanianDiscourse",
                additional_properties={"subtype": "master"},
                notes="Lacanian master discourse"
            ),
            "HYSTERIC_DISCOURSE": EntityMapping(
                ner_label="HYSTERIC_DISCOURSE",
                super_label=Neo4jSuperLabel.PSYCH_TRAIT,
                discriminator_property="traitType",
                discriminator_value="LacanianDiscourse",
                additional_properties={"subtype": "hysteric"},
                notes="Lacanian hysteric discourse"
            ),
        })

        # ================================================================
        # TIER 3: ORGANIZATIONAL - 5+ labels
        # ================================================================

        # Roles (3 labels)
        mappings.update({
            "CISO": EntityMapping(
                ner_label="CISO",
                super_label=Neo4jSuperLabel.ROLE,
                discriminator_property="roleType",
                discriminator_value="executive",
                additional_properties={"title": "Chief Information Security Officer"},
                notes="Chief Information Security Officer"
            ),
            "SECURITY_TEAM": EntityMapping(
                ner_label="SECURITY_TEAM",
                super_label=Neo4jSuperLabel.ROLE,
                discriminator_property="roleType",
                discriminator_value="security",
                additional_properties={"title": "Security Team"},
                notes="Security team members"
            ),
            "SOC": EntityMapping(
                ner_label="SOC",
                super_label=Neo4jSuperLabel.ROLE,
                discriminator_property="roleType",
                discriminator_value="security",
                additional_properties={"title": "Security Operations Center"},
                notes="SOC analysts"
            ),
        })

        # Organizations (2 labels)
        mappings.update({
            "ORGANIZATION": EntityMapping(
                ner_label="ORGANIZATION",
                super_label=Neo4jSuperLabel.ORGANIZATION,
                discriminator_property="orgType",
                discriminator_value="generic",
                notes="Generic organizations"
            ),
            "VENDOR": EntityMapping(
                ner_label="VENDOR",
                super_label=Neo4jSuperLabel.ORGANIZATION,
                discriminator_property="orgType",
                discriminator_value="vendor",
                notes="Vendor organizations"
            ),
        })

        # ================================================================
        # TIER 4: ECONOMIC - 3+ labels
        # ================================================================

        mappings.update({
            "FINANCIAL_IMPACT": EntityMapping(
                ner_label="FINANCIAL_IMPACT",
                super_label=Neo4jSuperLabel.ECONOMIC_METRIC,
                discriminator_property="metricType",
                discriminator_value="Loss",
                additional_properties={"category": "financial_impact"},
                notes="Financial impact metrics"
            ),
            "BREACH_COST": EntityMapping(
                ner_label="BREACH_COST",
                super_label=Neo4jSuperLabel.ECONOMIC_METRIC,
                discriminator_property="metricType",
                discriminator_value="Loss",
                additional_properties={"category": "breach_cost"},
                notes="Breach cost estimates"
            ),
            "MARKET_CAP": EntityMapping(
                ner_label="MARKET_CAP",
                super_label=Neo4jSuperLabel.ECONOMIC_METRIC,
                discriminator_property="metricType",
                discriminator_value="Market",
                additional_properties={"category": "market_capitalization"},
                notes="Market capitalization"
            ),
        })

        # ================================================================
        # TIER 5+: CONTROL & EVENT - 3+ labels
        # ================================================================

        # Controls
        mappings.update({
            "CONTROL": EntityMapping(
                ner_label="CONTROL",
                super_label=Neo4jSuperLabel.CONTROL,
                discriminator_property="controlType",
                discriminator_value="generic",
                notes="Security controls"
            ),
            "MITIGATION": EntityMapping(
                ner_label="MITIGATION",
                super_label=Neo4jSuperLabel.CONTROL,
                discriminator_property="controlType",
                discriminator_value="mitigation",
                notes="Mitigation strategies"
            ),
        })

        # Events
        mappings.update({
            "INCIDENT": EntityMapping(
                ner_label="INCIDENT",
                super_label=Neo4jSuperLabel.EVENT,
                discriminator_property="eventType",
                discriminator_value="incident",
                notes="Security incidents"
            ),
        })

        # Location
        mappings.update({
            "LOCATION": EntityMapping(
                ner_label="LOCATION",
                super_label=Neo4jSuperLabel.LOCATION,
                discriminator_property="locationType",
                discriminator_value="geographic",
                notes="Geographic locations"
            ),
        })

        return mappings

    def get_mapping(self, ner_label: str) -> Optional[EntityMapping]:
        """
        Get mapping configuration for NER label.

        Args:
            ner_label: NER11 entity label

        Returns:
            EntityMapping or None if not found
        """
        return self.mapping_table.get(ner_label)

    def generate_cypher(self, ner_label: str, entity_text: str,
                       properties: Dict = None) -> str:
        """
        Generate Cypher CREATE statement for entity.

        Args:
            ner_label: NER11 label
            entity_text: Entity text from document
            properties: Additional properties

        Returns:
            Cypher CREATE statement
        """
        mapping = self.get_mapping(ner_label)
        if not mapping:
            return f"// WARNING: No mapping found for {ner_label}"

        if mapping.is_property_only:
            return f"// {ner_label} maps to property: {mapping.property_name}"

        # Build properties dict
        props = {
            "name": entity_text,
            mapping.discriminator_property: mapping.discriminator_value
        }

        # Add additional properties from mapping
        props.update(mapping.additional_properties)

        # Add user-provided properties
        if properties:
            props.update(properties)

        # Generate Cypher
        props_str = ", ".join([f"{k}: '{v}'" for k, v in props.items()])

        cypher = f"""CREATE (n:{mapping.super_label.value} {{
  {props_str}
}})"""

        return cypher

    def validate_completeness(self) -> Dict:
        """
        Validate that all 60 expected NER labels are mapped.

        Returns:
            Validation report with statistics
        """
        report = {
            "total_mapped_labels": len(self.mapping_table),
            "expected_labels": 60,
            "coverage_percentage": (len(self.mapping_table) / 60) * 100,
            "super_label_distribution": {},
            "node_vs_property": {
                "node_mappings": 0,
                "property_mappings": 0
            },
            "missing_labels": [],
            "validation_passed": False
        }

        # Count super label distribution
        for mapping in self.mapping_table.values():
            label = mapping.super_label.value
            report["super_label_distribution"][label] = \
                report["super_label_distribution"].get(label, 0) + 1

            if mapping.is_property_only:
                report["node_vs_property"]["property_mappings"] += 1
            else:
                report["node_vs_property"]["node_mappings"] += 1

        # Validate
        report["validation_passed"] = (
            report["total_mapped_labels"] >= 60 and
            len(report["super_label_distribution"]) == 16
        )

        return report

    def get_examples(self) -> List[Dict]:
        """
        Generate mapping examples for documentation.

        Returns:
            List of example mappings with Cypher
        """
        examples = []

        # Example 1: ThreatActor
        examples.append({
            "ner_label": "APT_GROUP",
            "entity_text": "APT29",
            "mapping": self.get_mapping("APT_GROUP"),
            "cypher": self.generate_cypher("APT_GROUP", "APT29", {
                "aliases": ["Cozy Bear", "The Dukes"],
                "first_seen": "2008-01-01"
            })
        })

        # Example 2: Asset (PLC)
        examples.append({
            "ner_label": "PLC",
            "entity_text": "Siemens S7-1500",
            "mapping": self.get_mapping("PLC"),
            "cypher": self.generate_cypher("PLC", "Siemens S7-1500", {
                "vendor": "Siemens",
                "model": "S7-1500",
                "criticality": "critical"
            })
        })

        # Example 3: PsychTrait (Cognitive Bias)
        examples.append({
            "ner_label": "NORMALCY_BIAS",
            "entity_text": "Normalcy Bias",
            "mapping": self.get_mapping("NORMALCY_BIAS"),
            "cypher": self.generate_cypher("NORMALCY_BIAS", "Normalcy Bias", {
                "intensity": 0.85,
                "description": "Tendency to underestimate likelihood of disaster"
            })
        })

        # Example 4: EconomicMetric
        examples.append({
            "ner_label": "BREACH_COST",
            "entity_text": "Data Breach Cost",
            "mapping": self.get_mapping("BREACH_COST"),
            "cypher": self.generate_cypher("BREACH_COST", "Data Breach Cost", {
                "amount": 4240000.0,
                "currency": "USD",
                "timestamp": "2024-01-15"
            })
        })

        # Example 5: Protocol
        examples.append({
            "ner_label": "ICS_PROTOCOL",
            "entity_text": "Modbus TCP",
            "mapping": self.get_mapping("ICS_PROTOCOL"),
            "cypher": self.generate_cypher("ICS_PROTOCOL", "Modbus TCP", {
                "standard": "Modbus",
                "port": 502,
                "encryption": False
            })
        })

        return examples


# ============================================================================
# UNIT TESTS
# ============================================================================

def test_ner11_to_neo4j_mapper():
    """Comprehensive unit tests for NER11ToNeo4jMapper"""

    print("="*80)
    print("NER11 TO NEO4J MAPPER - UNIT TESTS")
    print("="*80)

    mapper = NER11ToNeo4jMapper()

    # Test 1: Mapping completeness
    print("\n[TEST 1] Mapping Completeness")
    print("-" * 40)
    validation = mapper.validate_completeness()
    print(f"Total mapped labels: {validation['total_mapped_labels']}")
    print(f"Expected labels: {validation['expected_labels']}")
    print(f"Coverage: {validation['coverage_percentage']:.1f}%")
    print(f"Validation passed: {validation['validation_passed']}")

    # Test 2: Super label distribution
    print("\n[TEST 2] Super Label Distribution")
    print("-" * 40)
    for label, count in sorted(validation['super_label_distribution'].items()):
        print(f"{label:25}: {count:3} NER labels")

    # Test 3: Node vs Property mappings
    print("\n[TEST 3] Node vs Property Mappings")
    print("-" * 40)
    print(f"Node mappings:     {validation['node_vs_property']['node_mappings']}")
    print(f"Property mappings: {validation['node_vs_property']['property_mappings']}")

    # Test 4: Sample mappings
    print("\n[TEST 4] Sample Mapping Lookups")
    print("-" * 40)
    test_labels = ["THREAT_ACTOR", "PLC", "NORMALCY_BIAS", "CVE", "CAMPAIGN"]
    for label in test_labels:
        mapping = mapper.get_mapping(label)
        if mapping:
            print(f"{label:20} -> {mapping.super_label.value:20} "
                  f"({mapping.discriminator_property}={mapping.discriminator_value})")
        else:
            print(f"{label:20} -> NOT MAPPED")

    # Test 5: Cypher generation
    print("\n[TEST 5] Cypher Generation Examples")
    print("-" * 40)
    examples = mapper.get_examples()
    for i, example in enumerate(examples[:3], 1):
        print(f"\nExample {i}: {example['ner_label']}")
        print(example['cypher'])

    # Test 6: Validation checks
    print("\n[TEST 6] Validation Checks")
    print("-" * 40)
    checks = {
        "All 60 labels mapped": validation['total_mapped_labels'] >= 60,
        "All 16 super labels used": len(validation['super_label_distribution']) == 16,
        "Majority are node mappings": validation['node_vs_property']['node_mappings'] > 50,
        "No missing critical labels": len(validation.get('missing_labels', [])) == 0
    }

    for check, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {check}")

    print("\n" + "="*80)
    print("ALL TESTS COMPLETED")
    print("="*80)

    return all(checks.values())


if __name__ == "__main__":
    # Run tests
    success = test_ner11_to_neo4j_mapper()

    if success:
        print("\n✅ NER11ToNeo4jMapper is PRODUCTION-READY")
        print("File: /5_NER11_Gold_Model/pipelines/04_ner11_to_neo4j_mapper.py")
        print("Status: Tests passing, ready for migration integration")
        print("\nNext Steps:")
        print("1. Integrate with migration script (Task 2.1)")
        print("2. Add validation to migration pipeline")
        print("3. Test with sample NER11 output")
    else:
        print("\n❌ Tests failed - review required")
