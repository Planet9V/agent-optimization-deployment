# Extension Guide
**File:** Extension_Guide.md
**Created:** 2025-10-29
**Version:** 1.0.0
**Author:** AEON FORGE ULTRATHINK
**Purpose:** Comprehensive guide for extending and customizing the ontology
**Status:** ACTIVE

## Executive Summary

This extension guide provides systematic approaches for extending the AEON Digital Twin Cybersecurity Threat Intelligence ontology with new node types, relationships, custom entity types for specific industries (rail, energy, healthcare, ICS/SCADA, IoT), query patterns, and schema versioning strategies. It includes complete implementation examples, migration procedures, and best practices for maintaining ontology integrity while adapting to evolving cybersecurity requirements.

---

## Table of Contents

1. [Adding New Node Types](#adding-new-node-types)
2. [Adding New Relationships](#adding-new-relationships)
3. [Custom Entity Types](#custom-entity-types)
4. [Query Pattern Extensions](#query-pattern-extensions)
5. [Schema Versioning](#schema-versioning)
6. [Best Practices](#best-practices)
7. [Migration Procedures](#migration-procedures)
8. [References](#references)

---

## Adding New Node Types

### Design Considerations

When designing new node types, consider these key principles (Robinson et al., 2015):

1. **Semantic Clarity**: Node labels should represent clear, distinct concepts
2. **Property Completeness**: Include all properties needed for analysis
3. **Relationship Integration**: Plan how new nodes connect to existing graph
4. **Query Performance**: Design for efficient traversal and filtering
5. **Data Validation**: Define constraints and validation rules

### Node Type Definition Process

```python
"""
Complete process for adding new node types
"""

from neo4j import GraphDatabase
from typing import Dict, List, Any
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class NodeTypeDefinition:
    """
    Node type specification

    Attributes:
        label: Node label (e.g., 'ThreatIntelligence')
        properties: Dictionary of property names and types
        required_properties: List of required property names
        unique_properties: List of properties that must be unique
        indexes: List of properties to index for performance
        constraints: List of constraint definitions
    """
    label: str
    properties: Dict[str, str]
    required_properties: List[str]
    unique_properties: List[str]
    indexes: List[str]
    constraints: List[str]


class NodeTypeManager:
    """
    Manage node type creation, validation, and migration
    """

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        """Initialize node type manager"""
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )

    def close(self):
        """Close database connection"""
        self.driver.close()

    def create_node_type(self, definition: NodeTypeDefinition) -> bool:
        """
        Create new node type with constraints and indexes

        Args:
            definition: Node type specification

        Returns:
            True if successful, False otherwise
        """
        try:
            with self.driver.session() as session:
                # Create uniqueness constraints
                for prop in definition.unique_properties:
                    constraint_query = f"""
                    CREATE CONSTRAINT {definition.label.lower()}_{prop}_unique IF NOT EXISTS
                    FOR (n:{definition.label})
                    REQUIRE n.{prop} IS UNIQUE
                    """
                    session.run(constraint_query)
                    logger.info(f"Created uniqueness constraint on {definition.label}.{prop}")

                # Create property existence constraints
                for prop in definition.required_properties:
                    constraint_query = f"""
                    CREATE CONSTRAINT {definition.label.lower()}_{prop}_exists IF NOT EXISTS
                    FOR (n:{definition.label})
                    REQUIRE n.{prop} IS NOT NULL
                    """
                    session.run(constraint_query)
                    logger.info(f"Created existence constraint on {definition.label}.{prop}")

                # Create indexes
                for prop in definition.indexes:
                    index_query = f"""
                    CREATE INDEX {definition.label.lower()}_{prop}_index IF NOT EXISTS
                    FOR (n:{definition.label})
                    ON (n.{prop})
                    """
                    session.run(index_query)
                    logger.info(f"Created index on {definition.label}.{prop}")

                logger.info(f"Successfully created node type: {definition.label}")
                return True

        except Exception as e:
            logger.error(f"Failed to create node type: {e}")
            return False

    def validate_node_type(self, label: str, properties: Dict[str, Any]) -> bool:
        """
        Validate node properties against definition

        Args:
            label: Node label
            properties: Property dictionary to validate

        Returns:
            True if valid, False otherwise
        """
        # Implementation would check against stored definition
        # This is a simplified example
        return True

    def create_sample_node(self, label: str, properties: Dict[str, Any]) -> str:
        """
        Create sample node with validation

        Args:
            label: Node label
            properties: Node properties

        Returns:
            Created node ID
        """
        # Validate properties
        if not self.validate_node_type(label, properties):
            raise ValueError(f"Invalid properties for {label}")

        # Build property string
        prop_string = ", ".join([f"{k}: ${k}" for k in properties.keys()])

        query = f"""
        CREATE (n:{label} {{{prop_string}}})
        RETURN id(n) AS node_id
        """

        with self.driver.session() as session:
            result = session.run(query, properties)
            node_id = result.single()["node_id"]
            logger.info(f"Created {label} node: {node_id}")
            return str(node_id)


# ========== Example: Adding ThreatIntelligence Node Type ==========

def add_threat_intelligence_node_type():
    """
    Example: Add ThreatIntelligence node type for external threat intel feeds
    """

    # Define node type
    threat_intel_def = NodeTypeDefinition(
        label="ThreatIntelligence",
        properties={
            "id": "string",
            "source": "string",
            "title": "string",
            "description": "string",
            "severity": "string",
            "confidence": "float",
            "firstSeen": "datetime",
            "lastSeen": "datetime",
            "tags": "list<string>",
            "iocType": "string",  # IP, domain, hash, etc.
            "iocValue": "string"
        },
        required_properties=["id", "source", "title", "iocType", "iocValue"],
        unique_properties=["id"],
        indexes=["source", "severity", "iocType", "firstSeen"],
        constraints=[]
    )

    # Initialize manager
    manager = NodeTypeManager(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )

    try:
        # Create node type
        success = manager.create_node_type(threat_intel_def)

        if success:
            # Create sample node
            sample_properties = {
                "id": "ti_001",
                "source": "AlienVault OTX",
                "title": "Malicious IP observed in phishing campaign",
                "description": "IP address associated with credential harvesting",
                "severity": "high",
                "confidence": 0.85,
                "firstSeen": "2024-03-15T10:00:00Z",
                "lastSeen": "2024-03-20T15:30:00Z",
                "tags": ["phishing", "credential-theft", "APT28"],
                "iocType": "ip",
                "iocValue": "192.0.2.100"
            }

            node_id = manager.create_sample_node("ThreatIntelligence", sample_properties)
            print(f"Created sample ThreatIntelligence node: {node_id}")

    finally:
        manager.close()


# ========== Example: Adding ComplianceRequirement Node Type ==========

def add_compliance_requirement_node_type():
    """
    Example: Add ComplianceRequirement node type for regulatory compliance
    """

    compliance_def = NodeTypeDefinition(
        label="ComplianceRequirement",
        properties={
            "id": "string",
            "framework": "string",  # NIST, ISO, PCI-DSS, HIPAA, etc.
            "requirementId": "string",
            "title": "string",
            "description": "string",
            "category": "string",
            "priority": "string",
            "status": "string",  # compliant, non-compliant, in-progress
            "lastAssessed": "datetime",
            "nextAssessment": "datetime",
            "evidenceRequired": "list<string>"
        },
        required_properties=["id", "framework", "requirementId", "title"],
        unique_properties=["id"],
        indexes=["framework", "status", "priority", "nextAssessment"],
        constraints=[]
    )

    manager = NodeTypeManager(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )

    try:
        success = manager.create_node_type(compliance_def)

        if success:
            sample_properties = {
                "id": "comp_001",
                "framework": "NIST-800-53",
                "requirementId": "AC-2",
                "title": "Account Management",
                "description": "Organization manages information system accounts",
                "category": "Access Control",
                "priority": "high",
                "status": "compliant",
                "lastAssessed": "2024-01-15T00:00:00Z",
                "nextAssessment": "2024-07-15T00:00:00Z",
                "evidenceRequired": ["User access logs", "Account creation policies"]
            }

            node_id = manager.create_sample_node("ComplianceRequirement", sample_properties)
            print(f"Created sample ComplianceRequirement node: {node_id}")

    finally:
        manager.close()


# ========== Example: Adding SecurityIncident Node Type ==========

def add_security_incident_node_type():
    """
    Example: Add SecurityIncident node type for incident tracking
    """

    incident_def = NodeTypeDefinition(
        label="SecurityIncident",
        properties={
            "id": "string",
            "title": "string",
            "description": "string",
            "severity": "string",
            "status": "string",  # open, investigating, contained, resolved
            "reportedDate": "datetime",
            "detectedDate": "datetime",
            "containedDate": "datetime",
            "resolvedDate": "datetime",
            "reportedBy": "string",
            "assignedTo": "string",
            "incidentType": "string",  # malware, phishing, data-breach, dos, etc.
            "impactLevel": "string",
            "rootCause": "string",
            "lessonsLearned": "string"
        },
        required_properties=["id", "title", "severity", "status", "reportedDate"],
        unique_properties=["id"],
        indexes=["severity", "status", "incidentType", "reportedDate"],
        constraints=[]
    )

    manager = NodeTypeManager(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )

    try:
        success = manager.create_node_type(incident_def)

        if success:
            sample_properties = {
                "id": "inc_001",
                "title": "Ransomware infection on workstation",
                "description": "Workstation infected with ransomware via phishing email",
                "severity": "high",
                "status": "resolved",
                "reportedDate": "2024-03-10T09:00:00Z",
                "detectedDate": "2024-03-10T08:45:00Z",
                "containedDate": "2024-03-10T10:30:00Z",
                "resolvedDate": "2024-03-11T14:00:00Z",
                "reportedBy": "John Doe",
                "assignedTo": "Security Operations Team",
                "incidentType": "malware",
                "impactLevel": "medium",
                "rootCause": "User clicked phishing link",
                "lessonsLearned": "Implement email filtering improvements"
            }

            node_id = manager.create_sample_node("SecurityIncident", sample_properties)
            print(f"Created sample SecurityIncident node: {node_id}")

    finally:
        manager.close()
```

---

## Adding New Relationships

### Relationship Design Principles

Effective relationship design requires careful consideration of semantic meaning and query patterns (Webber, 2012; Neo4j, 2024).

```python
"""
Relationship management and creation
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RelationshipDefinition:
    """
    Relationship type specification

    Attributes:
        type: Relationship type name (e.g., 'EXPLOITS')
        source_label: Source node label
        target_label: Target node label
        properties: Dictionary of relationship properties
        directionality: 'directed' or 'bidirectional'
        cardinality: 'one-to-one', 'one-to-many', 'many-to-many'
    """
    type: str
    source_label: str
    target_label: str
    properties: Dict[str, str]
    directionality: str
    cardinality: str


class RelationshipManager:
    """
    Manage relationship creation and validation
    """

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        """Initialize relationship manager"""
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )

    def close(self):
        """Close database connection"""
        self.driver.close()

    def create_relationship(
        self,
        definition: RelationshipDefinition,
        source_id: str,
        target_id: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Create relationship between nodes

        Args:
            definition: Relationship specification
            source_id: Source node ID
            target_id: Target node ID
            properties: Relationship properties

        Returns:
            True if successful
        """
        properties = properties or {}

        # Build property string
        prop_string = ""
        if properties:
            prop_string = "{ " + ", ".join([f"{k}: ${k}" for k in properties.keys()]) + " }"

        query = f"""
        MATCH (source:{definition.source_label})
        WHERE id(source) = $source_id
        MATCH (target:{definition.target_label})
        WHERE id(target) = $target_id
        MERGE (source)-[r:{definition.type} {prop_string}]->(target)
        RETURN id(r) AS rel_id
        """

        parameters = {
            "source_id": int(source_id),
            "target_id": int(target_id),
            **properties
        }

        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                rel_id = result.single()["rel_id"]
                logger.info(f"Created relationship {definition.type}: {rel_id}")
                return True
        except Exception as e:
            logger.error(f"Failed to create relationship: {e}")
            return False

    def create_bidirectional_relationship(
        self,
        definition: RelationshipDefinition,
        node_a_id: str,
        node_b_id: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Create bidirectional relationship between nodes

        Args:
            definition: Relationship specification
            node_a_id: First node ID
            node_b_id: Second node ID
            properties: Relationship properties

        Returns:
            True if successful
        """
        if definition.directionality != "bidirectional":
            raise ValueError("Relationship must be defined as bidirectional")

        # Create both directions
        success_1 = self.create_relationship(definition, node_a_id, node_b_id, properties)
        success_2 = self.create_relationship(definition, node_b_id, node_a_id, properties)

        return success_1 and success_2


# ========== Example: ThreatIntelligence Relationships ==========

def add_threat_intelligence_relationships():
    """
    Add relationships for ThreatIntelligence node type
    """

    manager = RelationshipManager(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )

    # Define relationships
    relationships = [
        RelationshipDefinition(
            type="INDICATES",
            source_label="ThreatIntelligence",
            target_label="ThreatActor",
            properties={"confidence": "float", "observedDate": "datetime"},
            directionality="directed",
            cardinality="many-to-many"
        ),
        RelationshipDefinition(
            type="TARGETS",
            source_label="ThreatIntelligence",
            target_label="Asset",
            properties={"firstObserved": "datetime", "lastObserved": "datetime"},
            directionality="directed",
            cardinality="many-to-many"
        ),
        RelationshipDefinition(
            type="CORRELATES_WITH",
            source_label="ThreatIntelligence",
            target_label="Vulnerability",
            properties={"correlation_score": "float"},
            directionality="directed",
            cardinality="many-to-many"
        ),
        RelationshipDefinition(
            type="RELATES_TO",
            source_label="ThreatIntelligence",
            target_label="AttackTechnique",
            properties={"confidence": "float"},
            directionality="directed",
            cardinality="many-to-many"
        )
    ]

    try:
        for rel_def in relationships:
            logger.info(f"Relationship defined: {rel_def.type} "
                       f"({rel_def.source_label})-[]-({rel_def.target_label})")

        # Example: Create sample relationships
        # (Assuming nodes exist with these IDs)
        # manager.create_relationship(relationships[0], "100", "200", {"confidence": 0.9})

    finally:
        manager.close()


# ========== Example: SecurityIncident Relationships ==========

def add_security_incident_relationships():
    """
    Add relationships for SecurityIncident node type
    """

    manager = RelationshipManager(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )

    relationships = [
        RelationshipDefinition(
            type="AFFECTED",
            source_label="SecurityIncident",
            target_label="Asset",
            properties={"impact": "string", "recoveryTime": "duration"},
            directionality="directed",
            cardinality="one-to-many"
        ),
        RelationshipDefinition(
            type="EXPLOITED",
            source_label="SecurityIncident",
            target_label="Vulnerability",
            properties={"exploitMethod": "string"},
            directionality="directed",
            cardinality="many-to-many"
        ),
        RelationshipDefinition(
            type="ATTRIBUTED_TO",
            source_label="SecurityIncident",
            target_label="ThreatActor",
            properties={"confidence": "float", "attribution_source": "string"},
            directionality="directed",
            cardinality="many-to-one"
        ),
        RelationshipDefinition(
            type="USED_TECHNIQUE",
            source_label="SecurityIncident",
            target_label="AttackTechnique",
            properties={"observedTimestamp": "datetime"},
            directionality="directed",
            cardinality="many-to-many"
        ),
        RelationshipDefinition(
            type="MITIGATED_BY",
            source_label="SecurityIncident",
            target_label="Control",
            properties={"effectiveness": "float"},
            directionality="directed",
            cardinality="many-to-many"
        )
    ]

    try:
        for rel_def in relationships:
            logger.info(f"Relationship defined: {rel_def.type}")

    finally:
        manager.close()
```

---

## Custom Entity Types

### Industry-Specific Extensions

#### Rail Transportation Security

```python
"""
Rail transportation cybersecurity entity types
Addresses NIST SP 800-82r3 guidance for transportation systems
"""

def add_rail_security_entities():
    """
    Add rail transportation-specific entity types
    """

    manager = NodeTypeManager(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )

    # RailAsset node type
    rail_asset_def = NodeTypeDefinition(
        label="RailAsset",
        properties={
            "id": "string",
            "name": "string",
            "assetType": "string",  # locomotive, signal, track-circuit, PTC, SCADA
            "criticality": "string",
            "location": "string",
            "milepost": "float",
            "subdivision": "string",
            "systemType": "string",  # PTC, CTC, ATC, ATCS
            "vendor": "string",
            "model": "string",
            "firmwareVersion": "string",
            "commProtocol": "string",  # Modbus, DNP3, proprietary
            "networkZone": "string",  # field, control, enterprise
            "safetyImpact": "string"  # critical, high, medium, low
        },
        required_properties=["id", "name", "assetType", "criticality", "safetyImpact"],
        unique_properties=["id"],
        indexes=["assetType", "criticality", "safetyImpact", "systemType"],
        constraints=[]
    )

    # RailIncident node type
    rail_incident_def = NodeTypeDefinition(
        label="RailIncident",
        properties={
            "id": "string",
            "title": "string",
            "description": "string",
            "severity": "string",
            "incidentType": "string",  # signal-interference, PTC-failure, SCADA-compromise
            "safetyImpact": "string",
            "operationalImpact": "string",
            "reportedDate": "datetime",
            "resolvedDate": "datetime",
            "location": "string",
            "milepost": "float",
            "affectedTrains": "list<string>",
            "FRAReportable": "boolean",  # Federal Railroad Administration reporting
            "rootCause": "string"
        },
        required_properties=["id", "title", "severity", "incidentType", "reportedDate"],
        unique_properties=["id"],
        indexes=["severity", "incidentType", "safetyImpact", "reportedDate"],
        constraints=[]
    )

    # PTCComponent node type (Positive Train Control)
    ptc_component_def = NodeTypeDefinition(
        label="PTCComponent",
        properties={
            "id": "string",
            "name": "string",
            "componentType": "string",  # back-office, onboard, wayside
            "ptcSystem": "string",  # I-ETMS, ACSES, etc.
            "vendor": "string",
            "certificationStatus": "string",
            "lastCertificationDate": "datetime",
            "interoperabilityTested": "boolean"
        },
        required_properties=["id", "name", "componentType", "ptcSystem"],
        unique_properties=["id"],
        indexes=["componentType", "ptcSystem", "certificationStatus"],
        constraints=[]
    )

    try:
        manager.create_node_type(rail_asset_def)
        manager.create_node_type(rail_incident_def)
        manager.create_node_type(ptc_component_def)

        logger.info("Created rail transportation entity types")

        # Sample rail asset
        sample_rail_asset = {
            "id": "rail_asset_001",
            "name": "Signal Controller MP 125.3",
            "assetType": "signal-controller",
            "criticality": "critical",
            "location": "Main Line Subdivision A",
            "milepost": 125.3,
            "subdivision": "Eastern District",
            "systemType": "CTC",
            "vendor": "Siemens",
            "model": "Vicos OC500",
            "firmwareVersion": "3.2.1",
            "commProtocol": "DNP3",
            "networkZone": "control",
            "safetyImpact": "critical"
        }

        manager.create_sample_node("RailAsset", sample_rail_asset)
        logger.info("Created sample rail asset")

    finally:
        manager.close()


def add_rail_relationships():
    """
    Add rail-specific relationships
    """

    relationships = [
        RelationshipDefinition(
            type="CONTROLS",
            source_label="RailAsset",
            target_label="RailAsset",
            properties={"control_type": "string"},
            directionality="directed",
            cardinality="one-to-many"
        ),
        RelationshipDefinition(
            type="SAFETY_DEPENDS_ON",
            source_label="RailAsset",
            target_label="RailAsset",
            properties={"dependency_type": "string", "failure_impact": "string"},
            directionality="directed",
            cardinality="many-to-many"
        ),
        RelationshipDefinition(
            type="INCIDENT_AFFECTED",
            source_label="RailIncident",
            target_label="RailAsset",
            properties={"duration": "duration", "impact": "string"},
            directionality="directed",
            cardinality="one-to-many"
        ),
        RelationshipDefinition(
            type="PART_OF_PTC",
            source_label="PTCComponent",
            target_label="RailAsset",
            properties={},
            directionality="directed",
            cardinality="many-to-one"
        )
    ]

    logger.info(f"Defined {len(relationships)} rail-specific relationships")
```

#### Energy Sector (ICS/SCADA)

```python
"""
Energy sector ICS/SCADA cybersecurity entities
Addresses NERC CIP standards and IEC 62351
"""

def add_energy_security_entities():
    """
    Add energy sector-specific entity types
    """

    manager = NodeTypeManager(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )

    # ICSDevice node type
    ics_device_def = NodeTypeDefinition(
        label="ICSDevice",
        properties={
            "id": "string",
            "name": "string",
            "deviceType": "string",  # PLC, RTU, HMI, SCADA-server, historian
            "criticality": "string",
            "bulkElectricSystem": "boolean",  # NERC CIP classification
            "cipCategory": "string",  # high, medium, low
            "vendor": "string",
            "model": "string",
            "firmwareVersion": "string",
            "protocol": "string",  # Modbus, DNP3, IEC-61850, OPC-UA
            "ipAddress": "string",
            "networkSegment": "string",
            "physicalLocation": "string",
            "function": "string",  # generation, transmission, distribution
            "lastPatchDate": "datetime",
            "patchingWindow": "string"
        },
        required_properties=["id", "name", "deviceType", "criticality", "cipCategory"],
        unique_properties=["id"],
        indexes=["deviceType", "criticality", "cipCategory", "bulkElectricSystem"],
        constraints=[]
    )

    # Substation node type
    substation_def = NodeTypeDefinition(
        label="Substation",
        properties={
            "id": "string",
            "name": "string",
            "voltage": "float",
            "substationType": "string",  # transmission, distribution
            "location": "string",
            "operator": "string",
            "cipImpact": "string",  # high, medium, low
            "physicalSecurity": "string"
        },
        required_properties=["id", "name", "voltage", "substationType"],
        unique_properties=["id"],
        indexes=["substationType", "cipImpact"],
        constraints=[]
    )

    # EnergyIncident node type
    energy_incident_def = NodeTypeDefinition(
        label="EnergyIncident",
        properties={
            "id": "string",
            "title": "string",
            "description": "string",
            "severity": "string",
            "incidentType": "string",
            "gridImpact": "string",  # none, minimal, significant, major
            "customersAffected": "integer",
            "mwhLost": "float",
            "reportedDate": "datetime",
            "resolvedDate": "datetime",
            "nercReportable": "boolean",
            "doeReportable": "boolean",
            "rootCause": "string"
        },
        required_properties=["id", "title", "severity", "incidentType", "reportedDate"],
        unique_properties=["id"],
        indexes=["severity", "incidentType", "gridImpact", "reportedDate"],
        constraints=[]
    )

    try:
        manager.create_node_type(ics_device_def)
        manager.create_node_type(substation_def)
        manager.create_node_type(energy_incident_def)

        logger.info("Created energy sector entity types")

        # Sample ICS device
        sample_ics_device = {
            "id": "ics_device_001",
            "name": "RTU Substation Alpha",
            "deviceType": "RTU",
            "criticality": "critical",
            "bulkElectricSystem": True,
            "cipCategory": "high",
            "vendor": "Schweitzer Engineering Laboratories",
            "model": "SEL-3505",
            "firmwareVersion": "R127-V0",
            "protocol": "DNP3",
            "ipAddress": "10.50.1.100",
            "networkSegment": "SCADA-Network",
            "physicalLocation": "Substation Alpha",
            "function": "transmission",
            "lastPatchDate": "2024-01-15T00:00:00Z",
            "patchingWindow": "Quarterly"
        }

        manager.create_sample_node("ICSDevice", sample_ics_device)
        logger.info("Created sample ICS device")

    finally:
        manager.close()
```

#### Healthcare Security

```python
"""
Healthcare cybersecurity entities
Addresses HIPAA Security Rule and FDA medical device security
"""

def add_healthcare_security_entities():
    """
    Add healthcare-specific entity types
    """

    manager = NodeTypeManager(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )

    # MedicalDevice node type
    medical_device_def = NodeTypeDefinition(
        label="MedicalDevice",
        properties={
            "id": "string",
            "name": "string",
            "deviceType": "string",  # imaging, infusion-pump, patient-monitor, etc.
            "criticality": "string",
            "fdaClass": "string",  # I, II, III
            "manufacturer": "string",
            "model": "string",
            "softwareVersion": "string",
            "ipAddress": "string",
            "location": "string",
            "department": "string",
            "patientFacing": "boolean",
            "networkConnected": "boolean",
            "phiAccess": "boolean",  # Access to Protected Health Information
            "maintenanceSchedule": "string",
            "eolDate": "datetime"  # End of Life
        },
        required_properties=["id", "name", "deviceType", "fdaClass", "criticality"],
        unique_properties=["id"],
        indexes=["deviceType", "fdaClass", "criticality", "phiAccess"],
        constraints=[]
    )

    # PHIBreach node type
    phi_breach_def = NodeTypeDefinition(
        label="PHIBreach",
        properties={
            "id": "string",
            "title": "string",
            "description": "string",
            "severity": "string",
            "breachType": "string",  # unauthorized-access, disclosure, theft, loss
            "recordsAffected": "integer",
            "discoveryDate": "datetime",
            "reportedDate": "datetime",
            "notificationDate": "datetime",
            "hhs_reportable": "boolean",  # HHS breach notification requirement
            "mediaNotification": "boolean",
            "affectedIndividuals": "integer",
            "rootCause": "string",
            "remediationStatus": "string"
        },
        required_properties=["id", "title", "severity", "breachType", "discoveryDate"],
        unique_properties=["id"],
        indexes=["severity", "breachType", "hhs_reportable", "discoveryDate"],
        constraints=[]
    )

    # HL7Message node type (healthcare data exchange)
    hl7_message_def = NodeTypeDefinition(
        label="HL7Message",
        properties={
            "id": "string",
            "messageType": "string",  # ADT, ORM, ORU, etc.
            "sourceSystem": "string",
            "destinationSystem": "string",
            "transmissionDate": "datetime",
            "encrypted": "boolean",
            "authenticatedSender": "boolean",
            "containsPHI": "boolean"
        },
        required_properties=["id", "messageType", "sourceSystem", "destinationSystem"],
        unique_properties=["id"],
        indexes=["messageType", "encrypted", "containsPHI"],
        constraints=[]
    )

    try:
        manager.create_node_type(medical_device_def)
        manager.create_node_type(phi_breach_def)
        manager.create_node_type(hl7_message_def)

        logger.info("Created healthcare entity types")

        # Sample medical device
        sample_medical_device = {
            "id": "med_device_001",
            "name": "MRI Scanner Room 3",
            "deviceType": "imaging-mri",
            "criticality": "high",
            "fdaClass": "II",
            "manufacturer": "Siemens Healthineers",
            "model": "MAGNETOM Vida",
            "softwareVersion": "VE11C",
            "ipAddress": "172.16.50.100",
            "location": "Radiology Department, Building A, Floor 2",
            "department": "Radiology",
            "patientFacing": True,
            "networkConnected": True,
            "phiAccess": True,
            "maintenanceSchedule": "Annual",
            "eolDate": "2030-12-31T00:00:00Z"
        }

        manager.create_sample_node("MedicalDevice", sample_medical_device)
        logger.info("Created sample medical device")

    finally:
        manager.close()
```

#### IoT Device Security

```python
"""
IoT device security entities
Addresses NIST IoT cybersecurity framework
"""

def add_iot_security_entities():
    """
    Add IoT-specific entity types
    """

    manager = NodeTypeManager(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )

    # IoTDevice node type
    iot_device_def = NodeTypeDefinition(
        label="IoTDevice",
        properties={
            "id": "string",
            "name": "string",
            "deviceType": "string",  # sensor, actuator, gateway, camera, etc.
            "criticality": "string",
            "manufacturer": "string",
            "model": "string",
            "firmwareVersion": "string",
            "macAddress": "string",
            "ipAddress": "string",
            "communicationProtocol": "string",  # MQTT, CoAP, HTTP, BLE, Zigbee
            "authenticationMethod": "string",
            "encryptionSupported": "boolean",
            "updateMechanism": "string",  # OTA, manual, none
            "lastUpdateDate": "datetime",
            "powerSource": "string",  # battery, AC, PoE
            "physicalSecurity": "string",
            "dataCollected": "list<string>",
            "cloudConnected": "boolean",
            "vendorSupport": "string"  # active, eol, deprecated
        },
        required_properties=["id", "name", "deviceType", "manufacturer", "model"],
        unique_properties=["id"],
        indexes=["deviceType", "criticality", "cloudConnected", "vendorSupport"],
        constraints=[]
    )

    # IoTGateway node type
    iot_gateway_def = NodeTypeDefinition(
        label="IoTGateway",
        properties={
            "id": "string",
            "name": "string",
            "gatewayType": "string",
            "manufacturer": "string",
            "model": "string",
            "firmwareVersion": "string",
            "ipAddress": "string",
            "supportedProtocols": "list<string>",
            "deviceCapacity": "integer",
            "currentDeviceCount": "integer",
            "firewallEnabled": "boolean",
            "vpnSupported": "boolean",
            "location": "string"
        },
        required_properties=["id", "name", "gatewayType", "manufacturer"],
        unique_properties=["id"],
        indexes=["gatewayType", "firewallEnabled", "vpnSupported"],
        constraints=[]
    )

    try:
        manager.create_node_type(iot_device_def)
        manager.create_node_type(iot_gateway_def)

        logger.info("Created IoT entity types")

        # Sample IoT device
        sample_iot_device = {
            "id": "iot_device_001",
            "name": "Temperature Sensor Floor 3 Room 301",
            "deviceType": "sensor-environmental",
            "criticality": "low",
            "manufacturer": "Sensirion",
            "model": "SHT31-DIS",
            "firmwareVersion": "2.1.0",
            "macAddress": "00:1A:2B:3C:4D:5E",
            "ipAddress": "192.168.100.50",
            "communicationProtocol": "MQTT",
            "authenticationMethod": "certificate",
            "encryptionSupported": True,
            "updateMechanism": "OTA",
            "lastUpdateDate": "2024-02-01T00:00:00Z",
            "powerSource": "battery",
            "physicalSecurity": "indoor-restricted",
            "dataCollected": ["temperature", "humidity"],
            "cloudConnected": True,
            "vendorSupport": "active"
        }

        manager.create_sample_node("IoTDevice", sample_iot_device)
        logger.info("Created sample IoT device")

    finally:
        manager.close()
```

---

## Query Pattern Extensions

### Custom Query Development

```python
"""
Query pattern extension framework
"""

from typing import Dict, Any, List, Callable
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryPatternLibrary:
    """
    Extensible query pattern library
    """

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        """Initialize query library"""
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )
        self.patterns = {}

    def close(self):
        """Close database connection"""
        self.driver.close()

    def register_pattern(
        self,
        name: str,
        query: str,
        parameters: Dict[str, str],
        description: str
    ):
        """
        Register new query pattern

        Args:
            name: Pattern name
            query: Cypher query string
            parameters: Parameter definitions
            description: Pattern description
        """
        self.patterns[name] = {
            "query": query,
            "parameters": parameters,
            "description": description
        }
        logger.info(f"Registered query pattern: {name}")

    def execute_pattern(
        self,
        pattern_name: str,
        parameters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Execute registered query pattern

        Args:
            pattern_name: Name of pattern to execute
            parameters: Query parameters

        Returns:
            Query results
        """
        if pattern_name not in self.patterns:
            raise ValueError(f"Pattern '{pattern_name}' not found")

        pattern = self.patterns[pattern_name]
        query = pattern["query"]

        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]


# ========== Rail Security Query Patterns ==========

def register_rail_query_patterns(library: QueryPatternLibrary):
    """
    Register rail-specific query patterns
    """

    # Pattern: Critical rail asset vulnerability exposure
    library.register_pattern(
        name="rail_critical_asset_exposure",
        query="""
        MATCH (ra:RailAsset)-[:HAS_VULNERABILITY]->(v:Vulnerability)
        WHERE ra.safetyImpact = 'critical'
          AND v.cvssScore >= $cvssThreshold
        OPTIONAL MATCH (ra)-[:PROTECTED_BY]->(c:Control)
        WHERE c.implementation = 'implemented'
        WITH ra, v, collect(c) AS controls
        RETURN ra.name AS asset,
               ra.assetType AS type,
               ra.systemType AS system,
               ra.location AS location,
               v.cveId AS vulnerability,
               v.cvssScore AS cvss,
               size(controls) AS controlCount,
               CASE
                 WHEN size(controls) = 0 THEN 'Unprotected'
                 WHEN size(controls) < 2 THEN 'Partially Protected'
                 ELSE 'Protected'
               END AS protectionStatus
        ORDER BY v.cvssScore DESC, size(controls) ASC
        """,
        parameters={"cvssThreshold": "float"},
        description="Find critical rail assets with vulnerabilities and protection status"
    )

    # Pattern: PTC component security analysis
    library.register_pattern(
        name="ptc_component_security",
        query="""
        MATCH (ptc:PTCComponent)-[:PART_OF_PTC]->(ra:RailAsset)
        OPTIONAL MATCH (ra)-[:HAS_VULNERABILITY]->(v:Vulnerability)
        WITH ptc, ra, collect(v) AS vulnerabilities
        RETURN ptc.name AS component,
               ptc.componentType AS type,
               ptc.ptcSystem AS system,
               ptc.certificationStatus AS certification,
               ra.name AS installedOn,
               size(vulnerabilities) AS vulnCount,
               [v IN vulnerabilities WHERE v.cvssScore >= 7.0 | v.cveId] AS criticalVulns
        ORDER BY size(vulnerabilities) DESC
        """,
        parameters={},
        description="Analyze security posture of PTC components"
    )

    # Pattern: Rail incident attack pattern correlation
    library.register_pattern(
        name="rail_incident_attack_correlation",
        query="""
        MATCH (ri:RailIncident)-[:USED_TECHNIQUE]->(at:AttackTechnique)
        WITH ri, collect(DISTINCT at.mitreId) AS techniques
        MATCH (ta:ThreatActor)-[:USES]->(at2:AttackTechnique)
        WHERE at2.mitreId IN techniques
        WITH ri, techniques, ta, count(DISTINCT at2) AS matchCount
        WHERE matchCount >= $minMatches
        RETURN ri.title AS incident,
               ri.incidentType AS type,
               ri.reportedDate AS date,
               techniques AS usedTechniques,
               ta.name AS potentialActor,
               matchCount AS techniqueMatches
        ORDER BY matchCount DESC
        """,
        parameters={"minMatches": "integer"},
        description="Correlate rail incidents with threat actor TTPs"
    )


# ========== Energy Sector Query Patterns ==========

def register_energy_query_patterns(library: QueryPatternLibrary):
    """
    Register energy sector-specific query patterns
    """

    # Pattern: NERC CIP compliance analysis
    library.register_pattern(
        name="nerc_cip_compliance",
        query="""
        MATCH (ics:ICSDevice)
        WHERE ics.bulkElectricSystem = true
          AND ics.cipCategory = $cipCategory
        OPTIONAL MATCH (ics)-[:HAS_VULNERABILITY]->(v:Vulnerability)
        WHERE v.cvssScore >= 7.0
        OPTIONAL MATCH (ics)-[:PROTECTED_BY]->(c:Control)
        WHERE c.framework = 'NERC-CIP'
          AND c.implementation = 'implemented'
        WITH ics, count(DISTINCT v) AS vulnCount, collect(DISTINCT c.controlId) AS cipControls
        RETURN ics.name AS device,
               ics.deviceType AS type,
               ics.cipCategory AS category,
               vulnCount AS vulnerabilities,
               size(cipControls) AS controlCount,
               cipControls AS implementedControls,
               CASE
                 WHEN vulnCount = 0 AND size(cipControls) >= 3 THEN 'Compliant'
                 WHEN vulnCount <= 2 AND size(cipControls) >= 2 THEN 'Partially Compliant'
                 ELSE 'Non-Compliant'
               END AS complianceStatus
        ORDER BY vulnCount DESC, size(cipControls) ASC
        """,
        parameters={"cipCategory": "string"},
        description="Assess NERC CIP compliance for bulk electric system devices"
    )

    # Pattern: Substation attack surface analysis
    library.register_pattern(
        name="substation_attack_surface",
        query="""
        MATCH (s:Substation)<-[:LOCATED_AT]-(ics:ICSDevice)
        OPTIONAL MATCH (ics)-[:CONNECTS_TO]-(peer:ICSDevice)
        WHERE peer.networkSegment <> ics.networkSegment
        WITH s, ics, count(DISTINCT peer) AS crossSegmentConnections
        OPTIONAL MATCH (ics)-[:HAS_VULNERABILITY]->(v:Vulnerability)
        WITH s, ics, crossSegmentConnections, collect(v) AS vulnerabilities
        RETURN s.name AS substation,
               s.voltage AS voltage,
               s.cipImpact AS impact,
               ics.name AS device,
               ics.deviceType AS type,
               crossSegmentConnections AS exposurePoints,
               size(vulnerabilities) AS vulnCount,
               CASE
                 WHEN crossSegmentConnections > 5 AND size(vulnerabilities) > 0 THEN 'High Risk'
                 WHEN crossSegmentConnections > 3 OR size(vulnerabilities) > 2 THEN 'Medium Risk'
                 ELSE 'Low Risk'
               END AS riskLevel
        ORDER BY crossSegmentConnections DESC, size(vulnerabilities) DESC
        """,
        parameters={},
        description="Analyze attack surface of substations"
    )


# ========== Healthcare Query Patterns ==========

def register_healthcare_query_patterns(library: QueryPatternLibrary):
    """
    Register healthcare-specific query patterns
    """

    # Pattern: PHI-accessible device security
    library.register_pattern(
        name="phi_device_security",
        query="""
        MATCH (md:MedicalDevice)
        WHERE md.phiAccess = true
        OPTIONAL MATCH (md)-[:HAS_VULNERABILITY]->(v:Vulnerability)
        OPTIONAL MATCH (md)-[:PROTECTED_BY]->(c:Control)
        WHERE c.implementation = 'implemented'
          AND (c.framework = 'HIPAA' OR c.controlId CONTAINS 'AC-')
        WITH md, collect(v) AS vulnerabilities, collect(c) AS controls
        RETURN md.name AS device,
               md.deviceType AS type,
               md.fdaClass AS fdaClass,
               md.department AS department,
               size(vulnerabilities) AS vulnCount,
               [v IN vulnerabilities WHERE v.cvssScore >= 7.0 | v.cveId] AS criticalVulns,
               size(controls) AS hipaaControls,
               CASE
                 WHEN size(vulnerabilities) = 0 AND size(controls) >= 2 THEN 'Secure'
                 WHEN size(vulnerabilities) <= 2 AND size(controls) >= 1 THEN 'Adequate'
                 ELSE 'At Risk'
               END AS securityPosture
        ORDER BY size(vulnerabilities) DESC, size(controls) ASC
        """,
        parameters={},
        description="Assess security of devices with PHI access"
    )

    # Pattern: Medical device EOL analysis
    library.register_pattern(
        name="medical_device_eol_analysis",
        query="""
        MATCH (md:MedicalDevice)
        WHERE md.eolDate < datetime() + duration({months: $monthsAhead})
        OPTIONAL MATCH (md)-[:HAS_VULNERABILITY]->(v:Vulnerability)
        RETURN md.name AS device,
               md.manufacturer AS manufacturer,
               md.model AS model,
               md.eolDate AS endOfLife,
               duration.between(datetime(), md.eolDate).months AS monthsRemaining,
               count(v) AS vulnerabilities,
               md.patientFacing AS patientFacing,
               md.department AS department
        ORDER BY md.eolDate ASC
        """,
        parameters={"monthsAhead": "integer"},
        description="Identify medical devices approaching end of life"
    )


# Usage example
if __name__ == "__main__":
    library = QueryPatternLibrary(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )

    try:
        # Register patterns
        register_rail_query_patterns(library)
        register_energy_query_patterns(library)
        register_healthcare_query_patterns(library)

        # Execute pattern
        results = library.execute_pattern(
            "rail_critical_asset_exposure",
            {"cvssThreshold": 7.0}
        )

        print(f"Found {len(results)} critical rail assets")

    finally:
        library.close()
```

---

## Schema Versioning

### Version Control Strategy

```python
"""
Schema versioning and migration management
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SchemaVersion:
    """
    Schema version specification

    Attributes:
        version: Version string (semantic versioning)
        description: Version description
        breaking_changes: List of breaking changes
        migration_script: Migration Cypher script
        rollback_script: Rollback Cypher script
        applied_date: Date version was applied
    """
    version: str
    description: str
    breaking_changes: List[str]
    migration_script: str
    rollback_script: str
    applied_date: Optional[datetime] = None


class SchemaVersionManager:
    """
    Manage schema versions and migrations
    """

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        """Initialize version manager"""
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )
        self._initialize_version_tracking()

    def close(self):
        """Close database connection"""
        self.driver.close()

    def _initialize_version_tracking(self):
        """Create version tracking node"""
        query = """
        MERGE (sv:SchemaVersion {id: 'current'})
        ON CREATE SET sv.version = '1.0.0',
                      sv.description = 'Initial schema',
                      sv.appliedDate = datetime()
        RETURN sv
        """

        with self.driver.session() as session:
            session.run(query)
            logger.info("Initialized schema version tracking")

    def get_current_version(self) -> str:
        """
        Get current schema version

        Returns:
            Current version string
        """
        query = """
        MATCH (sv:SchemaVersion {id: 'current'})
        RETURN sv.version AS version
        """

        with self.driver.session() as session:
            result = session.run(query)
            record = result.single()
            return record["version"] if record else "unknown"

    def apply_migration(self, version: SchemaVersion) -> bool:
        """
        Apply schema migration

        Args:
            version: Schema version to apply

        Returns:
            True if successful
        """
        logger.info(f"Applying migration to version {version.version}")

        try:
            with self.driver.session() as session:
                # Execute migration script
                session.run(version.migration_script)

                # Update version tracking
                update_query = """
                MATCH (sv:SchemaVersion {id: 'current'})
                SET sv.version = $version,
                    sv.description = $description,
                    sv.appliedDate = datetime(),
                    sv.breakingChanges = $breaking_changes
                """

                session.run(update_query, {
                    "version": version.version,
                    "description": version.description,
                    "breaking_changes": version.breaking_changes
                })

                logger.info(f"Migration to {version.version} complete")
                return True

        except Exception as e:
            logger.error(f"Migration failed: {e}")
            return False

    def rollback_migration(self, version: SchemaVersion) -> bool:
        """
        Rollback schema migration

        Args:
            version: Schema version to rollback

        Returns:
            True if successful
        """
        logger.info(f"Rolling back version {version.version}")

        try:
            with self.driver.session() as session:
                # Execute rollback script
                session.run(version.rollback_script)

                logger.info(f"Rollback of {version.version} complete")
                return True

        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return False


# ========== Example Migrations ==========

# Migration: Add ThreatIntelligence node type (v1.1.0)
migration_1_1_0 = SchemaVersion(
    version="1.1.0",
    description="Add ThreatIntelligence node type and relationships",
    breaking_changes=[],
    migration_script="""
    // Create constraints
    CREATE CONSTRAINT threat_intel_id_unique IF NOT EXISTS
    FOR (ti:ThreatIntelligence)
    REQUIRE ti.id IS UNIQUE;

    // Create indexes
    CREATE INDEX threat_intel_source_index IF NOT EXISTS
    FOR (ti:ThreatIntelligence)
    ON (ti.source);

    CREATE INDEX threat_intel_severity_index IF NOT EXISTS
    FOR (ti:ThreatIntelligence)
    ON (ti.severity);
    """,
    rollback_script="""
    // Drop constraints
    DROP CONSTRAINT threat_intel_id_unique IF EXISTS;

    // Drop indexes
    DROP INDEX threat_intel_source_index IF EXISTS;
    DROP INDEX threat_intel_severity_index IF EXISTS;
    """
)

# Migration: Add rail transportation entities (v2.0.0)
migration_2_0_0 = SchemaVersion(
    version="2.0.0",
    description="Add rail transportation-specific entities",
    breaking_changes=[
        "New node types: RailAsset, RailIncident, PTCComponent",
        "New relationships: CONTROLS, SAFETY_DEPENDS_ON"
    ],
    migration_script="""
    // Create RailAsset constraints
    CREATE CONSTRAINT rail_asset_id_unique IF NOT EXISTS
    FOR (ra:RailAsset)
    REQUIRE ra.id IS UNIQUE;

    // Create indexes
    CREATE INDEX rail_asset_type_index IF NOT EXISTS
    FOR (ra:RailAsset)
    ON (ra.assetType);

    CREATE INDEX rail_asset_safety_index IF NOT EXISTS
    FOR (ra:RailAsset)
    ON (ra.safetyImpact);

    // Create RailIncident constraints
    CREATE CONSTRAINT rail_incident_id_unique IF NOT EXISTS
    FOR (ri:RailIncident)
    REQUIRE ri.id IS UNIQUE;

    // Create PTCComponent constraints
    CREATE CONSTRAINT ptc_component_id_unique IF NOT EXISTS
    FOR (ptc:PTCComponent)
    REQUIRE ptc.id IS UNIQUE;
    """,
    rollback_script="""
    // Drop RailAsset constraints and indexes
    DROP CONSTRAINT rail_asset_id_unique IF EXISTS;
    DROP INDEX rail_asset_type_index IF EXISTS;
    DROP INDEX rail_asset_safety_index IF EXISTS;

    // Drop RailIncident constraints
    DROP CONSTRAINT rail_incident_id_unique IF EXISTS;

    // Drop PTCComponent constraints
    DROP CONSTRAINT ptc_component_id_unique IF EXISTS;

    // Remove all rail-specific nodes
    MATCH (ra:RailAsset) DETACH DELETE ra;
    MATCH (ri:RailIncident) DETACH DELETE ri;
    MATCH (ptc:PTCComponent) DETACH DELETE ptc;
    """
)

# Usage example
if __name__ == "__main__":
    manager = SchemaVersionManager(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password"
    )

    try:
        # Check current version
        current = manager.get_current_version()
        print(f"Current schema version: {current}")

        # Apply migrations
        if current == "1.0.0":
            manager.apply_migration(migration_1_1_0)
            manager.apply_migration(migration_2_0_0)

    finally:
        manager.close()
```

---

## Best Practices

### Schema Design Patterns

1. **Favor Relationships Over Properties**: Use relationships to model connections between entities rather than embedding IDs in properties
2. **Denormalize for Query Performance**: Duplicate frequently-accessed data to avoid expensive joins
3. **Use Meaningful Labels**: Node labels should clearly communicate entity types
4. **Index Frequently Queried Properties**: Create indexes on properties used in WHERE clauses
5. **Constrain Unique Identifiers**: Use uniqueness constraints for ID properties

### Anti-Patterns to Avoid

```python
"""
Common schema anti-patterns and solutions
"""

# ❌ BAD: Embedding IDs instead of relationships
bad_pattern = """
CREATE (a:Asset {
    id: 'asset_001',
    vulnerabilities: ['CVE-2024-1234', 'CVE-2024-5678']
})
"""

# ✅ GOOD: Using relationships
good_pattern = """
CREATE (a:Asset {id: 'asset_001'})
CREATE (v1:Vulnerability {cveId: 'CVE-2024-1234'})
CREATE (v2:Vulnerability {cveId: 'CVE-2024-5678'})
CREATE (a)-[:HAS_VULNERABILITY]->(v1)
CREATE (a)-[:HAS_VULNERABILITY]->(v2)
"""

# ❌ BAD: Dense properties in single node
bad_pattern_2 = """
CREATE (a:Asset {
    id: 'asset_001',
    vuln1_cve: 'CVE-2024-1234',
    vuln1_cvss: 9.8,
    vuln2_cve: 'CVE-2024-5678',
    vuln2_cvss: 7.5
})
"""

# ✅ GOOD: Normalized relationships
good_pattern_2 = """
CREATE (a:Asset {id: 'asset_001'})
CREATE (v1:Vulnerability {cveId: 'CVE-2024-1234', cvssScore: 9.8})
CREATE (v2:Vulnerability {cveId: 'CVE-2024-5678', cvssScore: 7.5})
CREATE (a)-[:HAS_VULNERABILITY]->(v1)
CREATE (a)-[:HAS_VULNERABILITY]->(v2)
"""

# ❌ BAD: Overly generic labels
bad_pattern_3 = """
CREATE (e:Entity {type: 'asset', name: 'server-01'})
CREATE (e2:Entity {type: 'vulnerability', cveId: 'CVE-2024-1234'})
"""

# ✅ GOOD: Specific, semantic labels
good_pattern_3 = """
CREATE (a:Asset {name: 'server-01'})
CREATE (v:Vulnerability {cveId: 'CVE-2024-1234'})
"""
```

---

## Migration Procedures

### Safe Migration Workflow

1. **Backup**: Create full database backup before migration
2. **Test**: Apply migration to test environment first
3. **Validate**: Run validation queries to ensure data integrity
4. **Document**: Record all changes and rollback procedures
5. **Monitor**: Track performance impact post-migration

```bash
#!/bin/bash
# Migration safety script

echo "Starting schema migration..."

# 1. Backup
echo "Creating backup..."
neo4j-admin dump --database=neo4j --to=/backups/pre-migration-$(date +%Y%m%d).dump

# 2. Apply migration
echo "Applying migration..."
python apply_migration.py --version 2.0.0

# 3. Validate
echo "Running validation queries..."
python validate_schema.py

# 4. Performance check
echo "Checking query performance..."
python benchmark_queries.py

echo "Migration complete!"
```

---

## References

Neo4j, Inc. (2024). *Neo4j Graph Data Science Library*. Retrieved from https://neo4j.com/docs/graph-data-science/

NIST. (2023). *Guide to Industrial Control Systems (ICS) Security* (SP 800-82 Rev. 3). National Institute of Standards and Technology.

Robinson, I., Webber, J., & Eifrem, E. (2015). *Graph Databases: New Opportunities for Connected Data* (2nd ed.). O'Reilly Media.

Webber, J. (2012). *A Programmatic Introduction to Neo4j*. Addison-Wesley Professional.

---

**Version History**
- v1.0.0 (2025-10-29): Initial extension guide with industry-specific implementations

**Document Status:** ACTIVE
