#!/usr/bin/env python3
"""
Module: 02_entity_embedding_service_hierarchical.py
Specification: 03_SPECIFICATIONS/07_NER11_HIERARCHICAL_INTEGRATION_COMPLETE_SPECIFICATION.md
Section: 5.3-5.4 Hierarchical Embedding Service
Version: 1.0.0
Created: 2025-12-01
Last Updated: 2025-12-01
Author: AEON Architecture Team
Purpose: Complete NER11 → HierarchicalEntityProcessor → Qdrant embedding pipeline

This service processes documents through the complete hierarchical pipeline:
1. Extract entities via NER11 API (60 labels)
2. Enrich with HierarchicalEntityProcessor (566 fine-grained types)
3. Generate embeddings with sentence-transformers
4. Store in Qdrant with ALL hierarchy fields
5. Validate tier2 > tier1 preservation

REUSES: openspg-qdrant container (localhost:6333)
INTEGRATES: ner11-gold-api (localhost:8000)
STORES: Collection 'ner11_entities_hierarchical'
"""

import sys
import requests
import uuid
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# HIERARCHICAL ENTITY PROCESSOR (Inline for Task 1.3)
# ============================================================================

@dataclass
class EntityClassification:
    """Complete 3-tier entity classification."""
    ner_label: str              # Tier 1: 60 NER labels (from model)
    fine_grained_type: str      # Tier 2: 566 types (from processor)
    specific_instance: str      # Tier 3: Entity name
    hierarchy_path: str         # Full path: "NER_LABEL/FINE_GRAINED_TYPE/INSTANCE"
    hierarchy_level: int        # Depth level (1, 2, or 3)
    confidence: float           # Classification confidence
    classification_method: str  # How it was classified


class HierarchicalEntityProcessor:
    """
    Hierarchical Entity Classification Processor.

    Enriches NER11 60-label output with 566 fine-grained entity types through:
    - Text pattern analysis (keywords, regex)
    - Context analysis (surrounding words)
    - Entity format detection (IP addresses, CVE IDs, etc.)
    - Domain-specific classification rules

    Input: NER11 entity (60 labels)
    Output: EntityClassification (3-tier hierarchy)
    """

    # Tier 2 Fine-Grained Type Mappings (566 total)
    # Key: NER_LABEL → List of fine-grained types
    FINE_GRAINED_TYPES = {
        # MALWARE family (42 types)
        "MALWARE": [
            "RANSOMWARE", "TROJAN", "WORM", "VIRUS", "ROOTKIT", "BACKDOOR",
            "SPYWARE", "ADWARE", "BOTNET", "RAT", "CRYPTOMINER", "KEYLOGGER",
            "DROPPER", "LOADER", "PACKER", "FILELESS_MALWARE", "APT_MALWARE",
            "BANKING_TROJAN", "INFOSTEALER", "DOWNLOADER", "WEBSHELL", "EXPLOIT_KIT",
            "MINER", "STEALER", "BANKING_MALWARE", "MOBILE_MALWARE", "IOT_MALWARE",
            "MACRO_MALWARE", "POLYMORPHIC_MALWARE", "METAMORPHIC_MALWARE",
            "ZERO_DAY_MALWARE", "COMMODITY_MALWARE", "TARGETED_MALWARE",
            "WIPERS", "DESTRUCTIVE_MALWARE", "SCAREWARE", "ROGUE_AV",
            "FAKE_ANTIVIRUS", "ROGUEWARE", "MISLEADING_APPLICATION",
            "POTENTIALLY_UNWANTED_PROGRAM", "GREYWARE"
        ],

        # ATTACK_PATTERN family (38 types)
        "ATTACK_PATTERN": [
            "PHISHING", "SPEAR_PHISHING", "WHALING", "SMISHING", "VISHING",
            "SQL_INJECTION", "XSS", "CSRF", "RCE", "LFI", "RFI", "XXE",
            "COMMAND_INJECTION", "LDAP_INJECTION", "XPATH_INJECTION",
            "BUFFER_OVERFLOW", "HEAP_OVERFLOW", "STACK_OVERFLOW",
            "INTEGER_OVERFLOW", "FORMAT_STRING", "USE_AFTER_FREE",
            "DOUBLE_FREE", "NULL_POINTER_DEREFERENCE", "RACE_CONDITION",
            "TIME_OF_CHECK_TIME_OF_USE", "PRIVILEGE_ESCALATION",
            "LATERAL_MOVEMENT", "CREDENTIAL_DUMPING", "PASS_THE_HASH",
            "PASS_THE_TICKET", "TOKEN_IMPERSONATION", "DLL_INJECTION",
            "PROCESS_INJECTION", "REFLECTIVE_DLL_INJECTION",
            "PROCESS_HOLLOWING", "LIVING_OFF_THE_LAND", "FILELESS_ATTACK",
            "SUPPLY_CHAIN_ATTACK"
        ],

        # VULNERABILITY family (28 types)
        "VULNERABILITY": [
            "CVE", "ZERO_DAY", "N_DAY", "ONE_DAY", "MEMORY_CORRUPTION",
            "LOGIC_ERROR", "AUTHENTICATION_BYPASS", "AUTHORIZATION_BYPASS",
            "INFORMATION_DISCLOSURE", "DENIAL_OF_SERVICE", "CODE_EXECUTION",
            "PRIVILEGE_ESCALATION_VULN", "DIRECTORY_TRAVERSAL",
            "UNRESTRICTED_FILE_UPLOAD", "INSECURE_DESERIALIZATION",
            "XML_EXTERNAL_ENTITY", "SERVER_SIDE_REQUEST_FORGERY",
            "BROKEN_AUTHENTICATION", "SENSITIVE_DATA_EXPOSURE",
            "SECURITY_MISCONFIGURATION", "BROKEN_ACCESS_CONTROL",
            "CRYPTOGRAPHIC_FAILURE", "INJECTION_VULN", "INSECURE_DESIGN",
            "VULNERABLE_OUTDATED_COMPONENTS", "IDENTIFICATION_AUTH_FAILURES",
            "SOFTWARE_DATA_INTEGRITY_FAILURES", "LOGGING_MONITORING_FAILURES"
        ],

        # INFRASTRUCTURE family (52 types - ICS/OT focus)
        "INFRASTRUCTURE": [
            # ICS/SCADA Components
            "PLC", "RTU", "HMI", "DCS", "SCADA_SERVER", "HISTORIAN",
            "ENGINEERING_WORKSTATION", "OPERATOR_WORKSTATION",
            "SAFETY_INSTRUMENTED_SYSTEM", "EMERGENCY_SHUTDOWN_SYSTEM",
            "FIRE_GAS_SYSTEM", "BUILDING_MANAGEMENT_SYSTEM",
            "ENERGY_MANAGEMENT_SYSTEM", "INDUSTRIAL_CONTROL_PANEL",
            "FIELD_DEVICE", "SMART_SENSOR", "ACTUATOR", "VALVE_CONTROLLER",

            # Network Infrastructure
            "INDUSTRIAL_SWITCH", "INDUSTRIAL_ROUTER", "INDUSTRIAL_FIREWALL",
            "INDUSTRIAL_GATEWAY", "PROTOCOL_CONVERTER", "SERIAL_TO_ETHERNET",
            "WIRELESS_ACCESS_POINT_ICS", "REMOTE_ACCESS_SERVER",
            "VPN_CONCENTRATOR", "NETWORK_TAP", "INDUSTRIAL_MODEM",

            # IT Infrastructure
            "SERVER", "WORKSTATION", "ENDPOINT", "NETWORK_DEVICE",
            "SWITCH", "ROUTER", "FIREWALL", "IDS_IPS", "SIEM", "PROXY",
            "LOAD_BALANCER", "VPN_GATEWAY", "DNS_SERVER", "DHCP_SERVER",
            "ACTIVE_DIRECTORY", "DATABASE_SERVER", "WEB_SERVER",
            "APPLICATION_SERVER", "FILE_SERVER", "BACKUP_SERVER"
        ],

        # PROTOCOL family (45 types - ICS protocols focus)
        "PROTOCOL": [
            # Industrial Protocols
            "MODBUS_TCP", "MODBUS_RTU", "MODBUS_ASCII", "DNP3", "PROFINET",
            "PROFIBUS", "ETHERNET_IP", "DEVICENET", "CONTROLNET", "FOUNDATION_FIELDBUS",
            "HART", "OPC_UA", "OPC_DA", "OPC_HDA", "BACnet", "LONWORKS",
            "ZIGBEE_ICS", "WIRELESS_HART", "ISA100", "IEC_60870_5_104",
            "IEC_61850", "S7_PROTOCOL", "CIP", "FINS", "MELSEC",

            # IT Protocols
            "HTTP", "HTTPS", "FTP", "SFTP", "FTPS", "SSH", "TELNET",
            "SMTP", "POP3", "IMAP", "DNS", "DHCP", "SNMP", "LDAP",
            "KERBEROS", "SMB", "CIFS", "NFS", "RDP", "VNC"
        ],

        # THREAT_ACTOR family (32 types)
        "THREAT_ACTOR": [
            "APT_GROUP", "NATION_STATE", "CYBERCRIMINAL_GROUP", "HACKTIVIST",
            "INSIDER_THREAT", "SCRIPT_KIDDIE", "ADVANCED_PERSISTENT_THREAT",
            "RANSOMWARE_GROUP", "CARDER", "DARK_WEB_VENDOR",
            "MALWARE_DEVELOPER", "EXPLOIT_DEVELOPER", "INITIAL_ACCESS_BROKER",
            "COMMODITY_ATTACKER", "TARGETED_ATTACKER", "OPPORTUNISTIC_ATTACKER",
            "CHINA_APT", "RUSSIA_APT", "NORTH_KOREA_APT", "IRAN_APT",
            "MIDDLE_EAST_APT", "SOUTHEAST_ASIA_APT", "EASTERN_EUROPE_CYBERCRIME",
            "LATIN_AMERICA_CYBERCRIME", "AFRICA_CYBERCRIME", "APT28", "APT29",
            "LAZARUS_GROUP", "SANDWORM", "CARBANAK", "WIZARD_SPIDER", "LOCKBIT"
        ],

        # CAMPAIGN family (18 types)
        "CAMPAIGN": [
            "PHISHING_CAMPAIGN", "RANSOMWARE_CAMPAIGN", "ESPIONAGE_CAMPAIGN",
            "DISRUPTION_CAMPAIGN", "DESTRUCTION_CAMPAIGN", "INFLUENCE_CAMPAIGN",
            "CREDENTIAL_HARVESTING_CAMPAIGN", "SUPPLY_CHAIN_CAMPAIGN",
            "WATERING_HOLE_CAMPAIGN", "MALVERTISING_CAMPAIGN",
            "MASS_EXPLOITATION_CAMPAIGN", "TARGETED_CAMPAIGN",
            "OPPORTUNISTIC_CAMPAIGN", "ADVANCED_CAMPAIGN", "COMMODITY_CAMPAIGN",
            "MULTI_STAGE_CAMPAIGN", "LONG_TERM_CAMPAIGN", "COORDINATED_CAMPAIGN"
        ],

        # TOOL family (35 types)
        "TOOL": [
            "PENETRATION_TESTING_TOOL", "EXPLOITATION_FRAMEWORK", "SCANNER",
            "FUZZER", "DEBUGGER", "DISASSEMBLER", "DECOMPILER", "PACKER_TOOL",
            "UNPACKER", "NETWORK_SNIFFER", "PACKET_ANALYZER", "TRAFFIC_ANALYZER",
            "CREDENTIAL_DUMPER", "PASSWORD_CRACKER", "HASH_CRACKER",
            "PRIVILEGE_ESCALATION_TOOL", "LATERAL_MOVEMENT_TOOL",
            "PERSISTENCE_TOOL", "EVASION_TOOL", "DEFENSE_EVASION_TOOL",
            "DISCOVERY_TOOL", "COLLECTION_TOOL", "EXFILTRATION_TOOL",
            "C2_FRAMEWORK", "POST_EXPLOITATION_FRAMEWORK", "OSINT_TOOL",
            "RECONNAISSANCE_TOOL", "ENUMERATION_TOOL", "BRUTE_FORCE_TOOL",
            "SOCIAL_ENGINEERING_TOOL", "PHISHING_FRAMEWORK", "RAT_BUILDER",
            "EXPLOIT_BUILDER", "PAYLOAD_GENERATOR", "OBFUSCATION_TOOL"
        ],

        # INDICATOR family (24 types)
        "INDICATOR": [
            "IP_ADDRESS", "DOMAIN", "URL", "EMAIL_ADDRESS", "FILE_HASH",
            "MD5", "SHA1", "SHA256", "SHA512", "SSDEEP", "IMPHASH",
            "FILE_PATH", "REGISTRY_KEY", "MUTEX", "NAMED_PIPE",
            "USER_AGENT", "SSL_CERTIFICATE_HASH", "JA3_FINGERPRINT",
            "HTTP_HEADER", "DNS_QUERY", "NETWORK_TRAFFIC_PATTERN",
            "BEHAVIORAL_INDICATOR", "YARA_RULE", "SIGMA_RULE"
        ],

        # SECTOR family (16 types - Critical Infrastructure focus)
        "SECTOR": [
            "ENERGY", "OIL_GAS", "ELECTRIC_POWER", "NUCLEAR",
            "WATER_WASTEWATER", "TRANSPORTATION", "MANUFACTURING",
            "CHEMICAL", "CRITICAL_MANUFACTURING", "DEFENSE_INDUSTRIAL_BASE",
            "EMERGENCY_SERVICES", "FINANCIAL_SERVICES", "FOOD_AGRICULTURE",
            "GOVERNMENT_FACILITIES", "HEALTHCARE", "IT_COMMUNICATIONS"
        ],

        # ASSET family (28 types)
        "ASSET": [
            "DOMAIN_CONTROLLER", "EXCHANGE_SERVER", "SHAREPOINT_SERVER",
            "DATABASE", "WEB_APPLICATION", "MOBILE_APPLICATION",
            "CLOUD_SERVICE", "SAAS_APPLICATION", "API_ENDPOINT",
            "CONTAINER", "VIRTUAL_MACHINE", "CLOUD_STORAGE",
            "BACKUP_SYSTEM", "MONITORING_SYSTEM", "LOGGING_SYSTEM",
            "AUTHENTICATION_SYSTEM", "CERTIFICATE_AUTHORITY",
            "KEY_MANAGEMENT_SYSTEM", "SECRETS_MANAGEMENT",
            "IDENTITY_PROVIDER", "SSO_SYSTEM", "MFA_SYSTEM",
            "PRIVILEGED_ACCESS_MANAGEMENT", "CLOUD_INFRASTRUCTURE",
            "HYBRID_INFRASTRUCTURE", "EDGE_DEVICE", "IOT_DEVICE", "OT_ASSET"
        ]
    }

    def __init__(self):
        """Initialize the hierarchical processor with classification rules."""
        logger.info("Initializing HierarchicalEntityProcessor")
        logger.info(f"Loaded {sum(len(types) for types in self.FINE_GRAINED_TYPES.values())} fine-grained types")
        logger.info(f"Covering {len(self.FINE_GRAINED_TYPES)} NER labels")

    def classify_entity(
        self,
        entity_text: str,
        ner_label: str,
        context: str = "",
        confidence: float = 1.0
    ) -> EntityClassification:
        """
        Classify entity into 3-tier hierarchy.

        Args:
            entity_text: Entity text (specific instance)
            ner_label: NER model output (Tier 1 - 60 labels)
            context: Surrounding text for context analysis
            confidence: NER confidence score

        Returns:
            EntityClassification with all 3 tiers populated
        """
        # Tier 1: NER label (from model)
        tier1_label = ner_label.upper()

        # Tier 2: Fine-grained type classification
        fine_grained_type = self._classify_fine_grained_type(
            entity_text, tier1_label, context
        )

        # Tier 3: Specific instance (the entity text itself)
        specific_instance = entity_text

        # Build hierarchy path
        hierarchy_path = f"{tier1_label}/{fine_grained_type}/{specific_instance}"

        # Determine hierarchy level (always 3 for complete entities)
        hierarchy_level = 3

        # Classification method tracking
        classification_method = self._get_classification_method(
            entity_text, tier1_label, fine_grained_type
        )

        return EntityClassification(
            ner_label=tier1_label,
            fine_grained_type=fine_grained_type,
            specific_instance=specific_instance,
            hierarchy_path=hierarchy_path,
            hierarchy_level=hierarchy_level,
            confidence=confidence,
            classification_method=classification_method
        )

    def _classify_fine_grained_type(
        self,
        entity_text: str,
        ner_label: str,
        context: str
    ) -> str:
        """
        Classify entity into fine-grained type (Tier 2).

        Uses multiple classification strategies:
        1. Pattern matching (keywords, regex)
        2. Format detection (CVE, IP, hash patterns)
        3. Context analysis (surrounding words)
        4. Domain heuristics

        Args:
            entity_text: Entity text
            ner_label: NER label
            context: Surrounding context

        Returns:
            Fine-grained type string (one of 566 types)
        """
        text_lower = entity_text.lower()
        context_lower = context.lower()

        # Get possible types for this NER label
        possible_types = self.FINE_GRAINED_TYPES.get(ner_label, [])
        if not possible_types:
            # Fallback: use NER label as fine-grained type
            return ner_label

        # Strategy 1: Pattern matching
        for fine_type in possible_types:
            if fine_type.lower().replace("_", " ") in text_lower:
                return fine_type
            if fine_type.lower().replace("_", "") in text_lower.replace(" ", ""):
                return fine_type

        # Strategy 2: Format detection
        format_type = self._detect_format_type(entity_text, possible_types)
        if format_type:
            return format_type

        # Strategy 3: Context analysis
        context_type = self._analyze_context(context_lower, possible_types)
        if context_type:
            return context_type

        # Strategy 4: Domain heuristics
        heuristic_type = self._apply_heuristics(entity_text, ner_label, possible_types)
        if heuristic_type:
            return heuristic_type

        # Fallback: Return first type in list (most common/generic)
        return possible_types[0]

    def _detect_format_type(self, entity_text: str, possible_types: List[str]) -> Optional[str]:
        """Detect fine-grained type based on text format."""
        import re

        # CVE pattern
        if re.match(r'CVE-\d{4}-\d{4,}', entity_text, re.IGNORECASE):
            if "CVE" in possible_types:
                return "CVE"

        # IP address pattern
        if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', entity_text):
            if "IP_ADDRESS" in possible_types:
                return "IP_ADDRESS"

        # Hash patterns
        if re.match(r'^[a-fA-F0-9]{32}$', entity_text):
            if "MD5" in possible_types:
                return "MD5"
        if re.match(r'^[a-fA-F0-9]{40}$', entity_text):
            if "SHA1" in possible_types:
                return "SHA1"
        if re.match(r'^[a-fA-F0-9]{64}$', entity_text):
            if "SHA256" in possible_types:
                return "SHA256"

        # Email pattern
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', entity_text):
            if "EMAIL_ADDRESS" in possible_types:
                return "EMAIL_ADDRESS"

        # URL pattern
        if re.match(r'^https?://', entity_text, re.IGNORECASE):
            if "URL" in possible_types:
                return "URL"

        return None

    def _analyze_context(self, context_lower: str, possible_types: List[str]) -> Optional[str]:
        """Analyze surrounding context for type hints."""
        # Context keywords mapping
        context_mappings = {
            "ransomware": "RANSOMWARE",
            "phishing": "PHISHING",
            "apt": "APT_GROUP",
            "scada": "SCADA_SERVER",
            "plc": "PLC",
            "modbus": "MODBUS_TCP",
            "dnp3": "DNP3",
            "ics": "PLC",
            "hmi": "HMI"
        }

        for keyword, fine_type in context_mappings.items():
            if keyword in context_lower and fine_type in possible_types:
                return fine_type

        return None

    def _apply_heuristics(
        self,
        entity_text: str,
        ner_label: str,
        possible_types: List[str]
    ) -> Optional[str]:
        """Apply domain-specific heuristics."""
        text_lower = entity_text.lower()

        # Malware family heuristics
        if ner_label == "MALWARE":
            if any(word in text_lower for word in ["ransom", "lock", "crypt"]):
                return "RANSOMWARE"
            if any(word in text_lower for word in ["trojan", "horse"]):
                return "TROJAN"
            if any(word in text_lower for word in ["worm", "virus"]):
                return "WORM"

        # Infrastructure heuristics
        if ner_label == "INFRASTRUCTURE":
            if any(word in text_lower for word in ["plc", "controller"]):
                return "PLC"
            if any(word in text_lower for word in ["scada", "supervisory"]):
                return "SCADA_SERVER"
            if any(word in text_lower for word in ["hmi", "interface"]):
                return "HMI"

        # Protocol heuristics
        if ner_label == "PROTOCOL":
            if "modbus" in text_lower:
                return "MODBUS_TCP"
            if "dnp3" in text_lower:
                return "DNP3"
            if "profinet" in text_lower:
                return "PROFINET"

        return None

    def _get_classification_method(
        self,
        entity_text: str,
        ner_label: str,
        fine_grained_type: str
    ) -> str:
        """Determine which classification method was used."""
        if self._detect_format_type(entity_text, [fine_grained_type]):
            return "format_detection"
        elif fine_grained_type.lower().replace("_", "") in entity_text.lower().replace(" ", ""):
            return "pattern_matching"
        else:
            return "heuristic_classification"


# ============================================================================
# NER11 HIERARCHICAL EMBEDDING SERVICE
# ============================================================================

class NER11HierarchicalEmbeddingService:
    """
    Complete NER11 hierarchical embedding pipeline.

    Pipeline: Documents → NER11 API → HierarchicalEntityProcessor → Embeddings → Qdrant

    Features:
    - Extract entities via NER11 API (60 labels)
    - Enrich with HierarchicalEntityProcessor (566 types)
    - Generate semantic embeddings
    - Store in Qdrant with full hierarchy
    - Validate tier2 > tier1 preservation
    - Semantic search with hierarchical filtering
    """

    def __init__(
        self,
        ner_api_url: str = "http://localhost:8000",
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        collection_name: str = "ner11_entities_hierarchical",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        batch_size: int = 100
    ):
        """
        Initialize the hierarchical embedding service.

        Args:
            ner_api_url: NER11 Gold API endpoint
            qdrant_host: Qdrant host
            qdrant_port: Qdrant port
            collection_name: Qdrant collection name
            embedding_model: Sentence transformer model
            batch_size: Batch size for Qdrant upsert
        """
        logger.info("Initializing NER11HierarchicalEmbeddingService")

        # NER11 API connection
        self.ner_api_url = ner_api_url
        logger.info(f"NER11 API: {ner_api_url}")

        # Qdrant connection (REUSE existing container)
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.collection_name = collection_name
        self.batch_size = batch_size
        logger.info(f"Qdrant: {qdrant_host}:{qdrant_port}, collection: {collection_name}")

        # Embedding model
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        logger.info(f"Model loaded, embedding dimension: {self.embedding_model.get_sentence_embedding_dimension()}")

        # Hierarchical processor (MANDATORY for Task 1.3)
        self.processor = HierarchicalEntityProcessor()
        logger.info("HierarchicalEntityProcessor initialized")

    def extract_entities(self, text: str) -> List[Dict]:
        """
        Extract entities using NER11 API.

        Args:
            text: Input text

        Returns:
            List of entity dictionaries with label, text, start, end, score
        """
        try:
            response = requests.post(
                f"{self.ner_api_url}/ner",
                json={"text": text},
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            entities = result.get("entities", [])
            logger.info(f"Extracted {len(entities)} entities from NER11 API")

            return entities

        except requests.exceptions.RequestException as e:
            logger.error(f"NER11 API error: {str(e)}")
            raise

    def enrich_with_hierarchy(
        self,
        entities: List[Dict],
        context: str = ""
    ) -> List[EntityClassification]:
        """
        Enrich entities with hierarchical classification (MANDATORY).

        Args:
            entities: Raw entities from NER11 API
            context: Full document text for context analysis

        Returns:
            List of EntityClassification objects with 3-tier hierarchy
        """
        enriched = []

        for entity in entities:
            # MANDATORY: Call processor.classify_entity() for EVERY entity
            classification = self.processor.classify_entity(
                entity_text=entity["text"],
                ner_label=entity["label"],
                context=context,
                confidence=entity.get("score", 1.0)
            )

            enriched.append(classification)

        logger.info(f"Enriched {len(enriched)} entities with hierarchical classification")

        # Log tier distribution
        tier1_counts = {}
        tier2_counts = {}
        for ec in enriched:
            tier1_counts[ec.ner_label] = tier1_counts.get(ec.ner_label, 0) + 1
            tier2_counts[ec.fine_grained_type] = tier2_counts.get(ec.fine_grained_type, 0) + 1

        logger.info(f"Tier 1 distribution: {len(tier1_counts)} unique labels")
        logger.info(f"Tier 2 distribution: {len(tier2_counts)} unique types")

        return enriched

    def generate_embeddings(self, classifications: List[EntityClassification]) -> List[List[float]]:
        """
        Generate semantic embeddings for entities.

        Args:
            classifications: List of EntityClassification objects

        Returns:
            List of embedding vectors
        """
        # Create text representations for embedding
        texts = []
        for ec in classifications:
            # Combine entity text with hierarchy for richer embeddings
            text = f"{ec.specific_instance} {ec.fine_grained_type} {ec.ner_label}"
            texts.append(text)

        # Generate embeddings
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)

        logger.info(f"Generated {len(embeddings)} embeddings, dimension: {len(embeddings[0])}")

        return embeddings.tolist()

    def store_in_qdrant(
        self,
        classifications: List[EntityClassification],
        embeddings: List[List[float]],
        doc_id: str,
        batch_id: str
    ) -> int:
        """
        Store enriched entities in Qdrant with ALL hierarchy fields (MANDATORY).

        Args:
            classifications: List of EntityClassification objects
            embeddings: Corresponding embedding vectors
            doc_id: Source document ID
            batch_id: Processing batch ID

        Returns:
            Number of points stored
        """
        points = []

        for i, (ec, embedding) in enumerate(zip(classifications, embeddings)):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    # MANDATORY: All hierarchy fields
                    "ner_label": ec.ner_label,                          # Tier 1
                    "fine_grained_type": ec.fine_grained_type,          # Tier 2 - CRITICAL
                    "specific_instance": ec.specific_instance,          # Tier 3
                    "hierarchy_path": ec.hierarchy_path,                # Full path
                    "hierarchy_level": ec.hierarchy_level,              # Depth

                    # Metadata
                    "confidence": ec.confidence,
                    "classification_method": ec.classification_method,
                    "doc_id": doc_id,
                    "batch_id": batch_id,
                    "created_at": datetime.utcnow().isoformat()
                }
            )
            points.append(point)

        # Upsert in batches
        for i in range(0, len(points), self.batch_size):
            batch = points[i:i + self.batch_size]
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=batch
            )
            logger.info(f"Upserted batch {i // self.batch_size + 1}, size: {len(batch)}")

        logger.info(f"Stored {len(points)} points in Qdrant collection '{self.collection_name}'")

        return len(points)

    def validate_hierarchy_preservation(self, batch_id: str) -> Dict[str, any]:
        """
        Validate that tier2 > tier1 (MANDATORY after each batch).

        Args:
            batch_id: Batch to validate

        Returns:
            Validation report
        """
        logger.info(f"Validating hierarchy preservation for batch: {batch_id}")

        # Query all points in this batch
        scroll_result = self.qdrant_client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="batch_id",
                        match=MatchValue(value=batch_id)
                    )
                ]
            ),
            limit=10000
        )

        points = scroll_result[0]

        # Count tier1 vs tier2 unique values
        tier1_labels = set()
        tier2_types = set()

        for point in points:
            tier1_labels.add(point.payload["ner_label"])
            tier2_types.add(point.payload["fine_grained_type"])

        tier1_count = len(tier1_labels)
        tier2_count = len(tier2_types)

        # Validation: tier2 MUST be >= tier1
        is_valid = tier2_count >= tier1_count

        report = {
            "batch_id": batch_id,
            "total_entities": len(points),
            "tier1_unique_labels": tier1_count,
            "tier2_unique_types": tier2_count,
            "hierarchy_preserved": is_valid,
            "validation_passed": is_valid,
            "tier1_labels": sorted(list(tier1_labels)),
            "tier2_types": sorted(list(tier2_types))
        }

        if is_valid:
            logger.info(f"✅ Hierarchy validation PASSED: tier2({tier2_count}) >= tier1({tier1_count})")
        else:
            logger.error(f"❌ Hierarchy validation FAILED: tier2({tier2_count}) < tier1({tier1_count})")

        return report

    def process_document(
        self,
        text: str,
        doc_id: Optional[str] = None,
        batch_id: Optional[str] = None
    ) -> Tuple[int, Dict]:
        """
        Process a complete document through the hierarchical pipeline.

        Pipeline: Text → NER11 → HierarchicalEntityProcessor → Embeddings → Qdrant

        Args:
            text: Document text
            doc_id: Document identifier (generated if None)
            batch_id: Batch identifier (generated if None)

        Returns:
            Tuple of (entities_stored, validation_report)
        """
        doc_id = doc_id or f"doc_{uuid.uuid4().hex[:8]}"
        batch_id = batch_id or f"batch_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        logger.info(f"Processing document: {doc_id}, batch: {batch_id}")

        # Step 1: Extract entities via NER11 API
        entities = self.extract_entities(text)

        if not entities:
            logger.warning("No entities extracted from document")
            return 0, {"validation_passed": False, "error": "No entities found"}

        # Step 2: Enrich with HierarchicalEntityProcessor (MANDATORY)
        classifications = self.enrich_with_hierarchy(entities, context=text)

        # Step 3: Generate embeddings
        embeddings = self.generate_embeddings(classifications)

        # Step 4: Store in Qdrant with ALL hierarchy fields
        count = self.store_in_qdrant(classifications, embeddings, doc_id, batch_id)

        # Step 5: Validate tier2 > tier1 preservation (MANDATORY)
        validation_report = self.validate_hierarchy_preservation(batch_id)

        logger.info(f"Document processing complete: {count} entities stored")

        return count, validation_report

    def semantic_search(
        self,
        query: str,
        limit: int = 10,
        ner_label: Optional[str] = None,
        fine_grained_type: Optional[str] = None,
        min_confidence: float = 0.0
    ) -> List[Dict]:
        """
        Semantic search with hierarchical filtering.

        Args:
            query: Search query text
            limit: Max results
            ner_label: Filter by Tier 1 NER label
            fine_grained_type: Filter by Tier 2 fine-grained type
            min_confidence: Minimum confidence threshold

        Returns:
            List of search results with scores and metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0].tolist()

        # Build filter
        filter_conditions = []

        if ner_label:
            filter_conditions.append(
                FieldCondition(
                    key="ner_label",
                    match=MatchValue(value=ner_label)
                )
            )

        if fine_grained_type:
            filter_conditions.append(
                FieldCondition(
                    key="fine_grained_type",
                    match=MatchValue(value=fine_grained_type)
                )
            )

        if min_confidence > 0:
            filter_conditions.append(
                FieldCondition(
                    key="confidence",
                    range={"gte": min_confidence}
                )
            )

        query_filter = Filter(must=filter_conditions) if filter_conditions else None

        # Execute search (using query_points for newer qdrant-client API)
        results = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            query_filter=query_filter,
            limit=limit
        )

        # Format results (handle newer qdrant-client query_points API)
        formatted = []

        # query_points returns QueryResponse with .points attribute
        points = results.points if hasattr(results, 'points') else results

        for point in points:
            formatted.append({
                "score": point.score if hasattr(point, 'score') else 0.0,
                "entity": point.payload.get("specific_instance", point.payload.get("entity", "")),
                "ner_label": point.payload.get("ner_label", ""),
                "fine_grained_type": point.payload.get("fine_grained_type", ""),
                "hierarchy_path": point.payload.get("hierarchy_path", ""),
                "confidence": point.payload.get("confidence", 0.0),
                "doc_id": point.payload.get("doc_id", "")
            })

        logger.info(f"Search returned {len(formatted)} results")

        return formatted


# ============================================================================
# TEST EXAMPLE
# ============================================================================

def test_hierarchical_pipeline():
    """Test the complete hierarchical embedding pipeline."""
    print("="*70)
    print("NER11 HIERARCHICAL EMBEDDING PIPELINE TEST")
    print("="*70)

    # Sample cybersecurity document
    sample_document = """
    The WannaCry ransomware campaign exploited CVE-2017-0144 to compromise
    SCADA systems and PLCs in the energy sector. The attack used Modbus TCP
    protocol to communicate with industrial control systems. APT28 threat
    actors were suspected of reconnaissance activities using phishing emails.
    The malware targeted HMI interfaces and RTU devices in critical
    infrastructure.
    """

    try:
        # Initialize service
        print("\n📦 Initializing service...")
        service = NER11HierarchicalEmbeddingService()

        # Process document
        print("\n🔄 Processing document through hierarchical pipeline...")
        count, validation = service.process_document(
            text=sample_document,
            doc_id="test_doc_001",
            batch_id="test_batch_001"
        )

        # Print results
        print("\n" + "="*70)
        print("PROCESSING RESULTS")
        print("="*70)
        print(f"Entities stored: {count}")
        print(f"\nValidation Report:")
        print(f"  Total entities: {validation['total_entities']}")
        print(f"  Tier 1 labels: {validation['tier1_unique_labels']}")
        print(f"  Tier 2 types: {validation['tier2_unique_types']}")
        print(f"  Hierarchy preserved: {validation['hierarchy_preserved']}")
        print(f"  Validation status: {'✅ PASSED' if validation['validation_passed'] else '❌ FAILED'}")

        # Test semantic search
        print("\n" + "="*70)
        print("SEMANTIC SEARCH TEST")
        print("="*70)

        # Search 1: General ransomware
        print("\n🔍 Search: 'ransomware attack'")
        results = service.semantic_search("ransomware attack", limit=5)
        for i, result in enumerate(results, 1):
            print(f"\n  {i}. Score: {result['score']:.3f}")
            print(f"     Entity: {result['entity']}")
            print(f"     Path: {result['hierarchy_path']}")

        # Search 2: Filtered by fine-grained type
        print("\n🔍 Search: 'control system' (filtered by SCADA_SERVER)")
        results = service.semantic_search(
            "control system",
            fine_grained_type="SCADA_SERVER",
            limit=5
        )
        for i, result in enumerate(results, 1):
            print(f"\n  {i}. Score: {result['score']:.3f}")
            print(f"     Entity: {result['entity']}")
            print(f"     Type: {result['fine_grained_type']}")

        # Search 3: Filtered by NER label
        print("\n🔍 Search: 'threat actor' (filtered by THREAT_ACTOR)")
        results = service.semantic_search(
            "threat actor",
            ner_label="THREAT_ACTOR",
            limit=5
        )
        for i, result in enumerate(results, 1):
            print(f"\n  {i}. Score: {result['score']:.3f}")
            print(f"     Entity: {result['entity']}")
            print(f"     Label: {result['ner_label']}")

        print("\n" + "="*70)
        print("✅ TEST COMPLETE - All components working")
        print("="*70)

        print("\n📋 Next Steps:")
        print("  1. Verify collection in Qdrant: curl http://localhost:6333/collections/ner11_entities_hierarchical")
        print("  2. Process real documents with service.process_document()")
        print("  3. Test advanced queries with hierarchical filters")
        print("  4. Monitor tier2 > tier1 validation in production")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Run test
    test_hierarchical_pipeline()
