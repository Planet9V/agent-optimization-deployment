#!/usr/bin/env python3
"""
Wave 4: ICS Security Knowledge Graph Implementation
Integrates cyber threat intelligence, attack patterns, TTPs, and cross-sector security analytics
"""

import logging
import json
import random
from datetime import datetime
from typing import Dict, List
from neo4j import GraphDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Wave4Executor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.log_file = "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/logs/wave_4_execution.jsonl"

    def log_operation(self, operation: str, details: dict):
        """Log operation to JSON Lines file"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "details": details
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        logging.info(f"{operation}: {details}")

    def execute(self):
        """Execute Wave 4 implementation"""
        try:
            self.log_operation("wave_4_execution_started", {"timestamp": datetime.utcnow().isoformat()})

            # Phase 1: Create constraints and indexes
            self.log_operation("phase_started", {"phase": "constraints_and_indexes"})
            self.create_constraints_and_indexes()
            self.log_operation("phase_completed", {"phase": "constraints_and_indexes"})

            # Phase 2: Create core security nodes
            self.log_operation("phase_started", {"phase": "create_threat_actors", "target_count": 50})
            threat_actors = self.create_threat_actors(50)
            self.log_operation("phase_completed", {"phase": "create_threat_actors", "nodes_created": threat_actors})

            self.log_operation("phase_started", {"phase": "create_attack_patterns", "target_count": 200})
            attack_patterns = self.create_attack_patterns(200)
            self.log_operation("phase_completed", {"phase": "create_attack_patterns", "nodes_created": attack_patterns})

            self.log_operation("phase_started", {"phase": "create_ttps", "target_count": 500})
            ttps = self.create_ttps(500)
            self.log_operation("phase_completed", {"phase": "create_ttps", "nodes_created": ttps})

            self.log_operation("phase_started", {"phase": "create_campaigns", "target_count": 100})
            campaigns = self.create_campaigns(100)
            self.log_operation("phase_completed", {"phase": "create_campaigns", "nodes_created": campaigns})

            self.log_operation("phase_started", {"phase": "create_detection_signatures", "target_count": 1000})
            signatures = self.create_detection_signatures(1000)
            self.log_operation("phase_completed", {"phase": "create_detection_signatures", "nodes_created": signatures})

            self.log_operation("phase_started", {"phase": "create_mitigations", "target_count": 300})
            mitigations = self.create_mitigations(300)
            self.log_operation("phase_completed", {"phase": "create_mitigations", "nodes_created": mitigations})

            # Phase 3: Create attack indicators
            self.log_operation("phase_started", {"phase": "create_indicators", "target_count": 5000})
            indicators = self.create_indicators(5000)
            self.log_operation("phase_completed", {"phase": "create_indicators", "nodes_created": indicators})

            # Phase 4: Create relationships
            self.log_operation("phase_started", {"phase": "create_relationships"})
            relationship_counts = self.create_relationships()
            total_relationships = sum(relationship_counts.values())
            self.log_operation("phase_completed", {"phase": "create_relationships", "total_relationships": total_relationships})

            total_nodes = threat_actors + attack_patterns + ttps + campaigns + signatures + mitigations + indicators

            self.log_operation("wave_4_execution_completed", {
                "timestamp": datetime.utcnow().isoformat(),
                "nodes_created": total_nodes,
                "relationships_created": total_relationships
            })

            logging.info(f"Wave 4 completed successfully: {total_nodes} nodes, {total_relationships} relationships")

        except Exception as e:
            self.log_operation("wave_4_execution_error", {"error": str(e)})
            logging.error(f"Wave 4 execution failed: {e}")
            raise
        finally:
            self.driver.close()

    def create_constraints_and_indexes(self):
        """Create constraints and indexes for Wave 4 nodes"""
        constraints_and_indexes = [
            # Constraints
            "CREATE CONSTRAINT threat_actor_id_unique IF NOT EXISTS FOR (ta:ThreatActor) REQUIRE ta.actorId IS UNIQUE",
            "CREATE CONSTRAINT attack_pattern_id_unique IF NOT EXISTS FOR (ap:AttackPattern) REQUIRE ap.attackPatternId IS UNIQUE",
            "CREATE CONSTRAINT ttp_id_unique IF NOT EXISTS FOR (ttp:TTP) REQUIRE ttp.ttpId IS UNIQUE",
            "CREATE CONSTRAINT campaign_id_unique IF NOT EXISTS FOR (camp:Campaign) REQUIRE camp.campaignId IS UNIQUE",
            "CREATE CONSTRAINT detection_signature_id_unique IF NOT EXISTS FOR (ds:DetectionSignature) REQUIRE ds.signatureId IS UNIQUE",
            "CREATE CONSTRAINT mitigation_id_unique IF NOT EXISTS FOR (mit:Mitigation) REQUIRE mit.mitigationId IS UNIQUE",
            "CREATE CONSTRAINT indicator_id_unique IF NOT EXISTS FOR (ind:Indicator) REQUIRE ind.indicatorId IS UNIQUE",

            # Indexes
            "CREATE INDEX threat_actor_type_idx IF NOT EXISTS FOR (ta:ThreatActor) ON (ta.actorType)",
            "CREATE INDEX threat_actor_attribution_idx IF NOT EXISTS FOR (ta:ThreatActor) ON (ta.attribution)",
            "CREATE INDEX threat_actor_sectors_idx IF NOT EXISTS FOR (ta:ThreatActor) ON (ta.icsSectors)",
            "CREATE INDEX attack_pattern_mitre_idx IF NOT EXISTS FOR (ap:AttackPattern) ON (ap.mitreId)",
            "CREATE INDEX attack_pattern_tactics_idx IF NOT EXISTS FOR (ap:AttackPattern) ON (ap.tactics)",
            "CREATE INDEX ttp_type_idx IF NOT EXISTS FOR (ttp:TTP) ON (ttp.ttpType)",
            "CREATE INDEX campaign_status_idx IF NOT EXISTS FOR (camp:Campaign) ON (camp.status)",
            "CREATE INDEX campaign_sectors_idx IF NOT EXISTS FOR (camp:Campaign) ON (camp.targetSectors)",
            "CREATE INDEX detection_signature_type_idx IF NOT EXISTS FOR (ds:DetectionSignature) ON (ds.signatureType)",
            "CREATE INDEX detection_severity_idx IF NOT EXISTS FOR (ds:DetectionSignature) ON (ds.severity)",
            "CREATE INDEX mitigation_type_idx IF NOT EXISTS FOR (mit:Mitigation) ON (mit.mitigationType)",
            "CREATE INDEX indicator_type_idx IF NOT EXISTS FOR (ind:Indicator) ON (ind.indicatorType)"
        ]

        with self.driver.session() as session:
            for statement in constraints_and_indexes:
                session.run(statement)
                self.log_operation("constraint_or_index_created", {"statement": statement[:60] + "..."})

    def create_threat_actors(self, count: int = 50) -> int:
        """Create ICS Threat Actor nodes"""
        actor_types = ["Nation-State", "APT", "Cybercriminal", "Hacktivist", "Insider"]
        attributions = ["Iran", "China", "Russia", "North Korea", "Unknown", "Multiple"]
        sophistication_levels = ["Advanced", "Intermediate", "Basic"]
        ics_sectors = [["Energy"], ["Water"], ["Energy", "Water"], ["Manufacturing"],
                       ["Chemical"], ["Energy", "Manufacturing"], ["Water", "Chemical"]]
        motivations = [["Espionage"], ["Sabotage"], ["Financial"], ["Espionage", "Sabotage"],
                       ["Espionage", "Financial"], ["Sabotage", "Financial"]]

        known_actors = [
            ("APT33", "Elfin", "Iran", "Nation-State", "Advanced", ["Shamoon", "Disttrack"]),
            ("APT41", "Winnti", "China", "APT", "Advanced", ["Barlaiy", "Deadeye"]),
            ("Triton", "XENOTIME", "Unknown", "Nation-State", "Advanced", ["Triton", "Trisis"]),
            ("Sandworm", "BlackEnergy", "Russia", "Nation-State", "Advanced", ["BlackEnergy", "Industroyer"]),
            ("Lazarus", "Hidden Cobra", "North Korea", "Nation-State", "Advanced", ["WannaCry", "DTrack"])
        ]

        with self.driver.session() as session:
            actors = []
            for i in range(count):
                if i < len(known_actors):
                    name, alias, attr, atype, soph, malware = known_actors[i]
                    actor = {
                        "actorId": f"ics:actor:{name.lower().replace(' ', '-')}-{i}",
                        "actorName": name,
                        "aliases": [alias],
                        "actorType": atype,
                        "attribution": attr,
                        "attributionConfidence": random.choice(["High", "Medium", "Low"]),
                        "firstSeen": datetime(2010 + i % 15, 1 + i % 12, 1, 0, 0, 0),
                        "lastSeen": datetime(2024, 1 + i % 12, 1, 0, 0, 0),
                        "icsSectors": random.choice(ics_sectors),
                        "geographicTargets": random.choice([["North America"], ["Middle East"], ["Europe"], ["Asia"]]),
                        "motivation": random.choice(motivations),
                        "sophisticationLevel": soph,
                        "resources": random.choice(["Government-Backed", "Well-Funded", "Limited"]),
                        "knownMalware": malware,
                        "icsCapabilities": random.sample(["SCADA Manipulation", "Safety System Override",
                                                          "HMI Compromise", "Historian Data Exfiltration",
                                                          "PLC Programming"], k=random.randint(2, 4))
                    }
                else:
                    actor = {
                        "actorId": f"ics:actor:threat-group-{i}",
                        "actorName": f"Threat Group {i}",
                        "aliases": [f"TG{i}", f"Group{i}"],
                        "actorType": random.choice(actor_types),
                        "attribution": random.choice(attributions),
                        "attributionConfidence": random.choice(["High", "Medium", "Low", "Suspected"]),
                        "firstSeen": datetime(2010 + i % 15, 1 + i % 12, 1, 0, 0, 0),
                        "lastSeen": datetime(2024, 1 + i % 12, 1, 0, 0, 0),
                        "icsSectors": random.choice(ics_sectors),
                        "geographicTargets": random.sample(["North America", "Europe", "Asia", "Middle East", "Africa"], k=random.randint(1, 3)),
                        "motivation": random.choice(motivations),
                        "sophisticationLevel": random.choice(sophistication_levels),
                        "resources": random.choice(["Government-Backed", "Well-Funded", "Limited"]),
                        "knownMalware": random.sample(["Malware-A", "Trojan-B", "Wiper-C", "RAT-D"], k=random.randint(1, 3)),
                        "icsCapabilities": random.sample(["SCADA Manipulation", "Safety System Override",
                                                          "HMI Compromise", "Historian Data Exfiltration"], k=random.randint(1, 3))
                    }
                actors.append(actor)

            query = """
            UNWIND $actors AS actor
            CREATE (ta:ICS:ThreatActor)
            SET ta = actor
            RETURN count(ta) as created
            """
            result = session.run(query, actors=actors)
            created = result.single()["created"]
            self.log_operation("threat_actors_created", {"count": created})
            return created

    def create_attack_patterns(self, count: int = 200) -> int:
        """Create ICS Attack Pattern nodes"""
        mitre_tactics = ["Initial Access", "Execution", "Persistence", "Privilege Escalation",
                        "Defense Evasion", "Credential Access", "Discovery", "Lateral Movement",
                        "Collection", "Command and Control", "Impair Process Control", "Inhibit Response Function", "Impact"]
        target_assets = [["PLC"], ["RTU"], ["DCS"], ["HMI"], ["Historian"], ["Engineering Workstation"],
                        ["PLC", "RTU"], ["DCS", "HMI"], ["SCADA Master"]]
        protocols = [["Modbus"], ["DNP3"], ["IEC-61850"], ["Profinet"], ["EtherNet/IP"],
                    ["Modbus", "DNP3"], ["IEC-61850", "Profinet"]]

        known_patterns = [
            ("T0885", "Modify Control Logic", "High", "Very Difficult", ["Stuxnet", "Triton"]),
            ("T0836", "Modify Parameter", "Medium", "Difficult", ["Industroyer"]),
            ("T0855", "Unauthorized Command Message", "Medium", "Moderate", ["BlackEnergy"]),
            ("T0822", "External Remote Services", "Low", "Easy", ["VPNFilter"]),
            ("T0867", "Lateral Tool Transfer", "Medium", "Moderate", ["APT campaigns"])
        ]

        with self.driver.session() as session:
            patterns = []
            for i in range(count):
                if i < len(known_patterns):
                    mitre_id, name, diff, detect_diff, examples = known_patterns[i]
                    pattern = {
                        "attackPatternId": f"ics:attack:{mitre_id.lower()}-{i}",
                        "patternName": name,
                        "mitreId": mitre_id,
                        "description": f"ICS-specific attack pattern: {name}",
                        "tactics": random.sample(mitre_tactics, k=random.randint(2, 4)),
                        "dataSourcesRequired": random.sample(["Network Traffic", "Process Monitoring", "File Monitoring", "Authentication Logs"], k=random.randint(2, 3)),
                        "targetAssets": random.choice(target_assets),
                        "targetProtocols": random.choice(protocols),
                        "prerequisiteKnowledge": random.sample(["PLC Programming", "Ladder Logic", "Process Understanding", "Network Protocols"], k=random.randint(1, 3)),
                        "technicalDifficulty": diff,
                        "detectionDifficulty": detect_diff,
                        "physicalImpact": random.sample(["Equipment Damage", "Process Disruption", "Safety System Failure", "Environmental Impact"], k=random.randint(1, 3)),
                        "realWorldExamples": examples
                    }
                else:
                    pattern = {
                        "attackPatternId": f"ics:attack:pattern-{i}",
                        "patternName": f"Attack Pattern {i}",
                        "mitreId": f"T{1000 + i % 100:04d}",
                        "description": f"ICS attack pattern targeting industrial control systems - pattern {i}",
                        "tactics": random.sample(mitre_tactics, k=random.randint(1, 3)),
                        "dataSourcesRequired": random.sample(["Network Traffic", "Process Monitoring", "File Monitoring"], k=random.randint(1, 2)),
                        "targetAssets": random.choice(target_assets),
                        "targetProtocols": random.choice(protocols),
                        "prerequisiteKnowledge": random.sample(["PLC Programming", "Network Protocols", "ICS Architecture"], k=random.randint(1, 2)),
                        "technicalDifficulty": random.choice(["High", "Medium", "Low"]),
                        "detectionDifficulty": random.choice(["Very Difficult", "Difficult", "Moderate", "Easy"]),
                        "physicalImpact": random.sample(["Equipment Damage", "Process Disruption", "Safety Impact"], k=random.randint(1, 2)),
                        "realWorldExamples": []
                    }
                patterns.append(pattern)

            query = """
            UNWIND $patterns AS pattern
            CREATE (ap:ICS:AttackPattern)
            SET ap = pattern
            RETURN count(ap) as created
            """
            result = session.run(query, patterns=patterns)
            created = result.single()["created"]
            self.log_operation("attack_patterns_created", {"count": created})
            return created

    def create_ttps(self, count: int = 500) -> int:
        """Create ICS TTP nodes"""
        ttp_types = ["InitialAccess", "Execution", "Persistence", "PrivilegeEscalation",
                    "DefenseEvasion", "CredentialAccess", "Discovery", "LateralMovement",
                    "Collection", "CommandAndControl", "Exfiltration", "Impact"]
        frequencies = ["High", "Medium", "Low", "Rare"]

        with self.driver.session() as session:
            ttps = []
            for i in range(count):
                ttp = {
                    "ttpId": f"ics:ttp:procedure-{i}",
                    "ttpName": f"ICS TTP Procedure {i}",
                    "ttpType": random.choice(ttp_types),
                    "description": f"Specific TTP procedure used in ICS attacks - procedure {i}",
                    "technicalDetails": f"Technical implementation details for procedure {i}",
                    "indicators": random.sample(["Unusual network traffic", "Process anomalies", "File modifications", "Registry changes"], k=random.randint(1, 3)),
                    "frequency": random.choice(frequencies),
                    "successRate": round(random.uniform(0.1, 0.9), 2)
                }
                ttps.append(ttp)

            query = """
            UNWIND $ttps AS ttp
            CREATE (t:ICS:TTP)
            SET t = ttp
            RETURN count(t) as created
            """
            result = session.run(query, ttps=ttps)
            created = result.single()["created"]
            self.log_operation("ttps_created", {"count": created})
            return created

    def create_campaigns(self, count: int = 100) -> int:
        """Create ICS Campaign nodes"""
        statuses = ["Active", "Concluded", "Ongoing", "Suspected"]
        sectors = [["Energy"], ["Water"], ["Manufacturing"], ["Chemical"], ["Energy", "Water"],
                  ["Energy", "Manufacturing"], ["Water", "Chemical"]]
        objectives = [["Data Destruction"], ["Operational Disruption"], ["Espionage"],
                     ["Data Destruction", "Operational Disruption"], ["Espionage", "Sabotage"]]

        with self.driver.session() as session:
            campaigns = []
            for i in range(count):
                start_year = 2018 + i % 7
                campaign = {
                    "campaignId": f"ics:campaign:operation-{i}",
                    "campaignName": f"ICS Campaign Operation {i}",
                    "startDate": datetime(start_year, 1 + i % 12, 1, 0, 0, 0),
                    "endDate": datetime(start_year + 1, 1 + (i + 3) % 12, 1, 0, 0, 0) if i % 3 == 0 else None,
                    "status": random.choice(statuses),
                    "objectives": random.choice(objectives),
                    "targetSectors": random.choice(sectors),
                    "targetGeography": random.sample(["North America", "Europe", "Asia", "Middle East"], k=random.randint(1, 3)),
                    "victimCount": random.randint(1, 50),
                    "estimatedImpact": random.choice(["Critical", "High", "Medium", "Low"]),
                    "attributionConfidence": random.choice(["High", "Medium", "Low"]),
                    "description": f"Coordinated ICS attack campaign targeting critical infrastructure - operation {i}"
                }
                campaigns.append(campaign)

            query = """
            UNWIND $campaigns AS campaign
            CREATE (c:ICS:Campaign)
            SET c = campaign
            RETURN count(c) as created
            """
            result = session.run(query, campaigns=campaigns)
            created = result.single()["created"]
            self.log_operation("campaigns_created", {"count": created})
            return created

    def create_detection_signatures(self, count: int = 1000) -> int:
        """Create ICS Detection Signature nodes"""
        sig_types = ["NetworkIDS", "SIEM-Rule", "AnomalyBehavior", "FileIntegrity", "ProcessMonitoring"]
        formats = ["Snort", "Suricata", "Splunk-SPL", "Sigma", "YARA"]
        severities = ["Critical", "High", "Medium", "Low"]
        data_sources = ["Network Traffic", "System Logs", "Process Monitoring", "File System"]

        with self.driver.session() as session:
            signatures = []
            for i in range(count):
                signature = {
                    "signatureId": f"ics:sig:detection-rule-{i}",
                    "signatureName": f"ICS Detection Rule {i}",
                    "signatureType": random.choice(sig_types),
                    "detectionLogic": f"Detection logic for rule {i} targeting ICS protocols",
                    "format": random.choice(formats),
                    "targetAttackPatterns": [f"T{1000 + j:04d}" for j in random.sample(range(100), k=random.randint(1, 3))],
                    "falsePositiveRate": random.choice(["Low", "Medium", "High"]),
                    "tuningRequired": random.choice([True, False]),
                    "dataSource": random.choice(data_sources),
                    "severity": random.choice(severities),
                    "validatedEffectiveness": random.choice([True, False])
                }
                signatures.append(signature)

            query = """
            UNWIND $signatures AS signature
            CREATE (ds:ICS:DetectionSignature)
            SET ds = signature
            RETURN count(ds) as created
            """
            result = session.run(query, signatures=signatures)
            created = result.single()["created"]
            self.log_operation("detection_signatures_created", {"count": created})
            return created

    def create_mitigations(self, count: int = 300) -> int:
        """Create ICS Mitigation nodes"""
        mit_types = ["NetworkSecurity", "AccessControl", "ApplicationHardening", "Monitoring", "Backup", "Training"]

        with self.driver.session() as session:
            mitigations = []
            for i in range(count):
                mitigation = {
                    "mitigationId": f"ics:mitigation:control-{i}",
                    "mitigationName": f"ICS Security Control {i}",
                    "mitigationType": random.choice(mit_types),
                    "description": f"Security mitigation control for ICS environments - control {i}",
                    "implementationCost": random.choice(["High", "Medium", "Low"]),
                    "implementationComplexity": random.choice(["High", "Medium", "Low"]),
                    "effectiveness": random.choice(["High", "Medium", "Low"]),
                    "standardsReferences": random.sample(["NIST-800-82", "IEC-62443", "NERC-CIP"], k=random.randint(1, 2)),
                    "operationalImpact": random.choice(["Minimal", "Moderate", "Significant"]),
                    "maintenanceRequired": random.choice([True, False]),
                    "targetedThreats": [f"T{1000 + j:04d}" for j in random.sample(range(100), k=random.randint(1, 3))]
                }
                mitigations.append(mitigation)

            query = """
            UNWIND $mitigations AS mitigation
            CREATE (m:ICS:Mitigation)
            SET m = mitigation
            RETURN count(m) as created
            """
            result = session.run(query, mitigations=mitigations)
            created = result.single()["created"]
            self.log_operation("mitigations_created", {"count": created})
            return created

    def create_indicators(self, count: int = 5000) -> int:
        """Create Indicator of Compromise nodes"""
        indicator_types = ["IP", "Domain", "FileHash", "URL", "Email", "Mutex", "Registry"]

        with self.driver.session() as session:
            indicators = []
            for i in range(count):
                ind_type = random.choice(indicator_types)
                if ind_type == "IP":
                    value = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
                elif ind_type == "Domain":
                    value = f"malicious-domain-{i}.com"
                elif ind_type == "FileHash":
                    value = f"{''.join(random.choices('0123456789abcdef', k=64))}"
                else:
                    value = f"{ind_type.lower()}-value-{i}"

                indicator = {
                    "indicatorId": f"ics:indicator:ioc-{i}",
                    "indicatorType": ind_type,
                    "indicatorValue": value,
                    "confidence": random.choice(["High", "Medium", "Low"]),
                    "firstSeen": datetime(2020 + i % 5, 1 + i % 12, 1, 0, 0, 0),
                    "lastSeen": datetime(2024, 1 + i % 12, 1, 0, 0, 0),
                    "threat_level": random.choice(["Critical", "High", "Medium", "Low"])
                }
                indicators.append(indicator)

            query = """
            UNWIND $indicators AS indicator
            CREATE (ind:ICS:Indicator)
            SET ind = indicator
            RETURN count(ind) as created
            """
            result = session.run(query, indicators=indicators)
            created = result.single()["created"]
            self.log_operation("indicators_created", {"count": created})
            return created

    def create_relationships(self) -> Dict[str, int]:
        """Create all relationships for Wave 4"""
        relationship_counts = {}

        with self.driver.session() as session:
            # 1. ORCHESTRATES_CAMPAIGN (ThreatActor → Campaign)
            query = """
            MATCH (ta:ThreatActor)
            MATCH (camp:Campaign)
            WITH ta, camp
            ORDER BY rand()
            LIMIT 150
            CREATE (ta)-[r:ORCHESTRATES_CAMPAIGN {
                confidence: CASE WHEN rand() > 0.7 THEN 'High' ELSE 'Medium' END,
                evidenceLevel: CASE WHEN rand() > 0.5 THEN 'Strong' ELSE 'Moderate' END
            }]->(camp)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["ORCHESTRATES_CAMPAIGN"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "ORCHESTRATES_CAMPAIGN", "count": relationship_counts["ORCHESTRATES_CAMPAIGN"]})

            # 2. USES_ATTACK_PATTERN (ThreatActor → AttackPattern)
            query = """
            MATCH (ta:ThreatActor)
            MATCH (ap:AttackPattern)
            WITH ta, collect(ap) as patterns
            UNWIND patterns[0..toInteger(rand() * 5) + 1] as ap
            CREATE (ta)-[r:USES_ATTACK_PATTERN {
                frequency: CASE toInteger(rand() * 3)
                    WHEN 0 THEN 'High'
                    WHEN 1 THEN 'Medium'
                    ELSE 'Low'
                END,
                observedSince: datetime() - duration({days: toInteger(rand() * 1460) + 30})
            }]->(ap)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["USES_ATTACK_PATTERN"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "USES_ATTACK_PATTERN", "count": relationship_counts["USES_ATTACK_PATTERN"]})

            # 3. IMPLEMENTS (AttackPattern → TTP)
            query = """
            MATCH (ap:AttackPattern)
            MATCH (ttp:TTP)
            WITH ap, collect(ttp) as ttps
            UNWIND ttps[0..toInteger(rand() * 3) + 1] as ttp
            CREATE (ap)-[r:IMPLEMENTS {
                implementationComplexity: CASE toInteger(rand() * 3)
                    WHEN 0 THEN 'High'
                    WHEN 1 THEN 'Medium'
                    ELSE 'Low'
                END
            }]->(ttp)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["IMPLEMENTS"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "IMPLEMENTS", "count": relationship_counts["IMPLEMENTS"]})

            # 4. TARGETS (AttackPattern → EnergyDevice/WaterDevice)
            query = """
            MATCH (ap:AttackPattern)
            MATCH (ed:EnergyDevice)
            WHERE ed.nercCIPCategory IN ['BES-Cyber-Asset', 'EACMS', 'PACS']
            WITH ap, collect(ed) as devices
            WITH ap, devices[0..toInteger(rand() * 10) + 1] as selectedDevices
            UNWIND selectedDevices as device
            CREATE (ap)-[r:TARGETS_DEVICE {
                vulnerabilityLevel: CASE toInteger(rand() * 3)
                    WHEN 0 THEN 'Critical'
                    WHEN 1 THEN 'High'
                    ELSE 'Medium'
                END,
                exploitability: CASE WHEN rand() > 0.7 THEN 'Easy' ELSE 'Difficult' END
            }]->(device)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["TARGETS_DEVICE"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "TARGETS_DEVICE", "count": relationship_counts["TARGETS_DEVICE"]})

            # 5. DETECTS (DetectionSignature → AttackPattern)
            query = """
            MATCH (ds:DetectionSignature)
            MATCH (ap:AttackPattern)
            WITH ds, collect(ap) as patterns
            UNWIND patterns[0..toInteger(rand() * 3) + 1] as ap
            CREATE (ds)-[r:DETECTS {
                detectionRate: round(rand() * 100, 2),
                falsePositiveRate: CASE toInteger(rand() * 3)
                    WHEN 0 THEN 'Low'
                    WHEN 1 THEN 'Medium'
                    ELSE 'High'
                END
            }]->(ap)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["DETECTS"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "DETECTS", "count": relationship_counts["DETECTS"]})

            # 6. MITIGATES (Mitigation → AttackPattern)
            query = """
            MATCH (mit:Mitigation)
            MATCH (ap:AttackPattern)
            WITH mit, collect(ap) as patterns
            UNWIND patterns[0..toInteger(rand() * 5) + 1] as ap
            CREATE (mit)-[r:MITIGATES {
                effectiveness: CASE toInteger(rand() * 3)
                    WHEN 0 THEN 'High'
                    WHEN 1 THEN 'Medium'
                    ELSE 'Low'
                END,
                implementationCost: CASE toInteger(rand() * 3)
                    WHEN 0 THEN 'High'
                    WHEN 1 THEN 'Medium'
                    ELSE 'Low'
                END
            }]->(ap)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["MITIGATES"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "MITIGATES", "count": relationship_counts["MITIGATES"]})

            # 7. USES_TTP (Campaign → TTP)
            query = """
            MATCH (camp:Campaign)
            MATCH (ttp:TTP)
            WITH camp, collect(ttp) as ttps
            UNWIND ttps[0..toInteger(rand() * 5) + 1] as ttp
            CREATE (camp)-[r:USES_TTP {
                frequency: CASE toInteger(rand() * 3)
                    WHEN 0 THEN 'High'
                    WHEN 1 THEN 'Medium'
                    ELSE 'Low'
                END
            }]->(ttp)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["USES_TTP"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "USES_TTP", "count": relationship_counts["USES_TTP"]})

            # 8. INDICATES (Indicator → Campaign)
            query = """
            MATCH (ind:Indicator)
            WHERE ind.confidence IN ['High', 'Medium']
            MATCH (camp:Campaign)
            WITH ind, camp
            ORDER BY rand()
            LIMIT 8000
            CREATE (ind)-[r:INDICATES {
                confidence: ind.confidence,
                firstObserved: ind.firstSeen
            }]->(camp)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["INDICATES"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "INDICATES", "count": relationship_counts["INDICATES"]})

            # 9. EXPLOITS_CVE (AttackPattern → CVE) - Connect to existing CVEs
            query = """
            MATCH (ap:AttackPattern)
            MATCH (cve:CVE)
            WHERE cve.cvss_v3_base_score >= 7.0
            WITH ap, collect(cve) as cves
            WITH ap, cves[0..toInteger(rand() * 3) + 1] as selectedCves
            UNWIND selectedCves as cve
            CREATE (ap)-[r:EXPLOITS_CVE {
                exploitAvailable: CASE WHEN rand() > 0.7 THEN true ELSE false END,
                weaponizationLevel: CASE toInteger(rand() * 3)
                    WHEN 0 THEN 'Proof-of-Concept'
                    WHEN 1 THEN 'Functional'
                    ELSE 'High'
                END
            }]->(cve)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["EXPLOITS_CVE"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "EXPLOITS_CVE", "count": relationship_counts["EXPLOITS_CVE"]})

            # 10. PART_OF_CAMPAIGN (AttackPattern → Campaign)
            query = """
            MATCH (ap:AttackPattern)
            MATCH (camp:Campaign)
            WITH ap, camp
            ORDER BY rand()
            LIMIT 500
            CREATE (ap)-[r:PART_OF_CAMPAIGN {
                roleInCampaign: CASE toInteger(rand() * 3)
                    WHEN 0 THEN 'Primary'
                    WHEN 1 THEN 'Secondary'
                    ELSE 'Supporting'
                END
            }]->(camp)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["PART_OF_CAMPAIGN"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "PART_OF_CAMPAIGN", "count": relationship_counts["PART_OF_CAMPAIGN"]})

        return relationship_counts

if __name__ == "__main__":
    executor = Wave4Executor()
    executor.execute()
