#!/usr/bin/env python3
"""
Wave 2: Water Infrastructure Domain Extensions
Complete implementation of water sector ontology with SCADA security integration

Purpose: Extend SAREF core with water treatment, distribution, and SCADA security
Target: 15,000 nodes, 45,000 relationships
Safety: Zero CVE deletion, additive-only, builds on Wave 1
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple
from pathlib import Path
from neo4j import GraphDatabase
import structlog

# Setup logging
logger = structlog.get_logger()

# Add parent directory for imports
sys.path.append('/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j')

class Wave2Executor:
    """
    Wave 2 Water Infrastructure Implementation

    Implements:
    - Water:WaterDevice nodes (1,500 devices)
    - Water:WaterProperty nodes (3,000 properties)
    - Water:TreatmentProcess nodes (500 processes)
    - Water:SCADASystem nodes (300 SCADA systems)
    - Water:WaterZone nodes (200 zones)
    - Water:Measurement nodes (9,000 measurements)
    - Water:Alert nodes (500 security/quality alerts)

    Total: ~15,000 nodes, ~45,000 relationships
    """

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = None,
        log_dir: str = "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/logs"
    ):
        """Initialize Wave 2 executor"""
        self.neo4j_password = neo4j_password or os.getenv("NEO4J_PASSWORD", "neo4j@openspg")
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, self.neo4j_password)
        )

        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Execution metrics
        self.metrics = {
            "start_time": None,
            "end_time": None,
            "nodes_created": 0,
            "relationships_created": 0,
            "constraints_created": 0,
            "indexes_created": 0,
            "errors": []
        }

        logger.info("wave_2_executor_initialized", uri=neo4j_uri)

    def log_operation(self, operation: str, details: Dict[str, Any]):
        """Log operation to detailed log file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "details": details
        }

        log_file = self.log_dir / "wave_2_execution.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")

        logger.info(operation, **details)

    def create_constraints_and_indexes(self) -> Dict[str, int]:
        """Create all necessary constraints and indexes for Wave 2"""
        self.log_operation("phase_started", {"phase": "constraints_and_indexes"})

        with self.driver.session() as session:
            constraints = [
                "CREATE CONSTRAINT water_device_id_unique IF NOT EXISTS FOR (wd:WaterDevice) REQUIRE wd.deviceId IS UNIQUE",
                "CREATE CONSTRAINT water_property_id_unique IF NOT EXISTS FOR (wp:WaterProperty) REQUIRE wp.propertyId IS UNIQUE",
                "CREATE CONSTRAINT treatment_process_id_unique IF NOT EXISTS FOR (tp:TreatmentProcess) REQUIRE tp.processId IS UNIQUE",
                "CREATE CONSTRAINT scada_system_id_unique IF NOT EXISTS FOR (ss:SCADASystem) REQUIRE ss.scadaId IS UNIQUE",
                "CREATE CONSTRAINT water_zone_id_unique IF NOT EXISTS FOR (wz:WaterZone) REQUIRE wz.zoneId IS UNIQUE",
                "CREATE CONSTRAINT water_alert_id_unique IF NOT EXISTS FOR (wa:WaterAlert) REQUIRE wa.alertId IS UNIQUE"
            ]

            indexes = [
                "CREATE INDEX water_device_type_idx IF NOT EXISTS FOR (wd:WaterDevice) ON (wd.waterDeviceType)",
                "CREATE INDEX water_regulatory_zone_idx IF NOT EXISTS FOR (wd:WaterDevice) ON (wd.regulatoryZone)",
                "CREATE INDEX water_cyber_risk_idx IF NOT EXISTS FOR (wd:WaterDevice) ON (wd.cyberPhysicalRisk)",
                "CREATE INDEX water_property_category_idx IF NOT EXISTS FOR (wp:WaterProperty) ON (wp.waterPropertyCategory)",
                "CREATE INDEX water_epa_parameter_idx IF NOT EXISTS FOR (wp:WaterProperty) ON (wp.epaParameter)",
                "CREATE INDEX treatment_process_type_idx IF NOT EXISTS FOR (tp:TreatmentProcess) ON (tp.processType)",
                "CREATE INDEX scada_vendor_idx IF NOT EXISTS FOR (ss:SCADASystem) ON (ss.vendor)",
                "CREATE INDEX water_zone_type_idx IF NOT EXISTS FOR (wz:WaterZone) ON (wz.zoneType)",
                "CREATE INDEX water_alert_severity_idx IF NOT EXISTS FOR (wa:WaterAlert) ON (wa.severity)"
            ]

            # Execute constraints
            for constraint in constraints:
                try:
                    session.run(constraint)
                    self.metrics["constraints_created"] += 1
                    self.log_operation("constraint_created", {"constraint": constraint[:60]})
                except Exception as e:
                    logger.warning("constraint_failed", constraint=constraint[:60], error=str(e))

            # Execute indexes
            for index in indexes:
                try:
                    session.run(index)
                    self.metrics["indexes_created"] += 1
                    self.log_operation("index_created", {"index": index[:60]})
                except Exception as e:
                    logger.warning("index_failed", index=index[:60], error=str(e))

        self.log_operation("phase_completed", {
            "phase": "constraints_and_indexes",
            "constraints": self.metrics["constraints_created"],
            "indexes": self.metrics["indexes_created"]
        })

        return {
            "constraints": self.metrics["constraints_created"],
            "indexes": self.metrics["indexes_created"]
        }

    def create_water_devices(self, count: int = 1500) -> int:
        """Create Water:WaterDevice nodes (extends SAREF:Device)"""
        self.log_operation("phase_started", {"phase": "create_water_devices", "target_count": count})

        device_types = [
            ("Pump", "Grundfos", "CR 64-2", 2500.0, 150.0),
            ("Valve", "AVK", "Series 25", 3000.0, 200.0),
            ("Sensor", "Endress+Hauser", "Promag 50", 5000.0, 250.0),
            ("RTU", "Rockwell", "CompactLogix 5370", 0.0, 0.0),
            ("Chlorinator", "Siemens", "WTP-CL300", 500.0, 100.0),
            ("Filter", "Pentair", "SandMaster 2000", 4000.0, 80.0),
            ("Flowmeter", "Siemens", "MAG 5100W", 6000.0, 300.0),
            ("Turbidity Sensor", "Hach", "1720E", 0.0, 0.0)
        ]

        regulatory_zones = ["Zone-A-Treatment", "Zone-B-Distribution", "Zone-C-Reservoir", "Zone-D-Pumping"]
        risk_levels = ["Critical", "High", "Medium", "Low"]

        with self.driver.session() as session:
            created = 0
            batch_size = 50

            for i in range(0, count, batch_size):
                batch_count = min(batch_size, count - i)
                devices = []

                for j in range(batch_count):
                    idx = (i + j) % len(device_types)
                    dev_type, mfr, model, flow, pressure = device_types[idx]

                    device = {
                        "deviceId": f"water:device:{dev_type.lower()}-{i+j:06d}",
                        "name": f"{mfr} {model} {dev_type} Unit {i+j}",
                        "model": model,
                        "manufacturer": mfr,
                        "firmwareVersion": f"v{(i+j) % 5 + 1}.{(i+j) % 10}.{(i+j) % 20}",
                        "serialNumber": f"WTR-2024-{i+j:06d}",
                        "deviceCategory": "Sensor" if "Sensor" in dev_type else "Actuator",
                        "deploymentLocation": f"Water Plant {(i+j) % 5 + 1}, Section {chr(65 + (i+j) % 6)}",
                        "operationalStatus": ["Active", "Standby", "Maintenance"][(i+j) % 3],
                        "ipAddress": f"10.{(i+j) // 65536}.{((i+j) // 256) % 256}.{(i+j) % 256}",
                        "macAddress": f"02:1A:2B:{(i+j) // 65536:02X}:{((i+j) // 256) % 256:02X}:{(i+j) % 256:02X}",
                        "criticality": risk_levels[(i+j) % len(risk_levels)],
                        "waterDeviceType": dev_type,
                        "flowCapacity": flow,
                        "pressureRating": pressure,
                        "materialComposition": ["Stainless Steel 316", "PVC", "Cast Iron", "Brass"][(i+j) % 4],
                        "regulatoryZone": regulatory_zones[(i+j) % len(regulatory_zones)],
                        "epaAssetId": f"EPA-WTR-2024-{i+j:06d}",
                        "maintenanceSchedule": ["Quarterly", "Biannual", "Annual"][(i+j) % 3],
                        "waterQualityImpact": risk_levels[(i+j) % len(risk_levels)],
                        "cyberPhysicalRisk": risk_levels[(i+j) % len(risk_levels)]
                    }
                    devices.append(device)

                query = """
                UNWIND $devices AS device
                CREATE (wd:WaterDevice:Device)
                SET wd = device,
                    wd.commissionDate = datetime(),
                    wd.lastUpdated = datetime(),
                    wd.protocol = ['Modbus/TCP', 'OPC-UA'],
                    wd.lastMaintenanceDate = datetime()
                RETURN count(wd) as created
                """

                result = session.run(query, devices=devices)
                batch_created = result.single()["created"]
                created += batch_created

                self.log_operation("water_devices_batch_created", {
                    "batch": i // batch_size,
                    "count": batch_created,
                    "total": created
                })

        self.metrics["nodes_created"] += created
        self.log_operation("phase_completed", {"phase": "create_water_devices", "nodes_created": created})
        return created

    def create_water_properties(self, count: int = 3000) -> int:
        """Create Water:WaterProperty nodes (extends SAREF:Property)"""
        self.log_operation("phase_started", {"phase": "create_water_properties", "target_count": count})

        property_categories = [
            ("Hydraulic", "FlowRate", "GPM", 0.0, 10000.0, "EPA-2001"),
            ("Hydraulic", "Pressure", "PSI", 0.0, 300.0, "EPA-2002"),
            ("Chemical", "Chlorine", "mg/L", 0.0, 4.0, "EPA-1005"),
            ("Chemical", "pH", "pH", 0.0, 14.0, "EPA-1010"),
            ("Physical", "Turbidity", "NTU", 0.0, 5.0, "EPA-3001"),
            ("Physical", "Temperature", "Celsius", 0.0, 35.0, "EPA-3002"),
            ("Biological", "Coliform", "CFU/100mL", 0.0, 0.0, "EPA-4001"),
            ("Chemical", "Fluoride", "mg/L", 0.0, 2.0, "EPA-1015")
        ]

        health_impacts = ["Critical", "High", "Medium", "Low"]
        sampling_frequencies = ["Continuous", "Hourly", "Daily", "Weekly"]

        with self.driver.session() as session:
            created = 0
            batch_size = 100

            for i in range(0, count, batch_size):
                batch_count = min(batch_size, count - i)
                properties = []

                for j in range(batch_count):
                    idx = (i + j) % len(property_categories)
                    category, prop_type, unit, min_val, max_val, epa_code = property_categories[idx]

                    prop = {
                        "propertyId": f"water:property:{prop_type.lower()}-{i+j:06d}",
                        "propertyType": prop_type,
                        "unitOfMeasure": unit,
                        "minValue": min_val,
                        "maxValue": max_val,
                        "normalRangeMin": min_val + (max_val - min_val) * 0.2,
                        "normalRangeMax": min_val + (max_val - min_val) * 0.8,
                        "criticalThresholdMin": min_val + (max_val - min_val) * 0.1,
                        "criticalThresholdMax": min_val + (max_val - min_val) * 0.9,
                        "measurementAccuracy": 0.01 + (i + j) % 10 * 0.01,
                        "description": f"{prop_type} monitoring for water quality",
                        "waterPropertyCategory": category,
                        "regulatoryLimit": max_val,
                        "actionLevel": max_val * 0.9,
                        "healthImpact": health_impacts[(i + j) % len(health_impacts)],
                        "samplingFrequency": sampling_frequencies[(i + j) % len(sampling_frequencies)],
                        "epaParameter": epa_code
                    }
                    properties.append(prop)

                query = """
                UNWIND $properties AS property
                CREATE (wp:WaterProperty:Property)
                SET wp = property,
                    wp.lastCalibration = datetime()
                RETURN count(wp) as created
                """

                result = session.run(query, properties=properties)
                batch_created = result.single()["created"]
                created += batch_created

                if (i // batch_size) % 10 == 0:
                    self.log_operation("water_properties_batch_created", {
                        "batch": i // batch_size,
                        "count": batch_created,
                        "total": created
                    })

        self.metrics["nodes_created"] += created
        self.log_operation("phase_completed", {"phase": "create_water_properties", "nodes_created": created})
        return created

    def create_treatment_processes(self, count: int = 500) -> int:
        """Create Water:TreatmentProcess nodes"""
        self.log_operation("phase_started", {"phase": "create_treatment_processes", "target_count": count})

        process_types = [
            ("Filtration", "Physical"),
            ("Chlorination", "Chemical"),
            ("UV Treatment", "Physical"),
            ("Coagulation", "Chemical"),
            ("Sedimentation", "Physical"),
            ("Fluoridation", "Chemical")
        ]

        with self.driver.session() as session:
            created = 0
            batch_size = 50

            for i in range(0, count, batch_size):
                batch_count = min(batch_size, count - i)
                processes = []

                for j in range(batch_count):
                    idx = (i + j) % len(process_types)
                    proc_type, treatment_category = process_types[idx]

                    process = {
                        "processId": f"water:process:{proc_type.lower().replace(' ', '_')}-{i+j:04d}",
                        "processName": f"{proc_type} Unit {i+j}",
                        "processType": proc_type,
                        "treatmentCategory": treatment_category,
                        "operationalStatus": ["Active", "Standby", "Maintenance"][(i+j) % 3],
                        "designCapacity": 1000.0 + (i + j) * 100.0,
                        "currentThroughput": 800.0 + (i + j) * 80.0,
                        "efficiency": 85.0 + (i + j) % 15,
                        "criticality": ["Critical", "High", "Medium"][(i+j) % 3]
                    }
                    processes.append(process)

                query = """
                UNWIND $processes AS process
                CREATE (tp:TreatmentProcess)
                SET tp = process,
                    tp.commissionDate = datetime(),
                    tp.lastUpdated = datetime()
                RETURN count(tp) as created
                """

                result = session.run(query, processes=processes)
                batch_created = result.single()["created"]
                created += batch_created

        self.metrics["nodes_created"] += created
        self.log_operation("phase_completed", {"phase": "create_treatment_processes", "nodes_created": created})
        return created

    def create_scada_systems(self, count: int = 300) -> int:
        """Create Water:SCADASystem nodes"""
        self.log_operation("phase_started", {"phase": "create_scada_systems", "target_count": count})

        vendors = ["Siemens", "Rockwell Automation", "Schneider Electric", "GE Digital", "ABB"]
        scada_types = ["HMI", "RTU", "PLC", "Historian", "SCADA Master"]

        with self.driver.session() as session:
            created = 0
            batch_size = 50

            for i in range(0, count, batch_size):
                batch_count = min(batch_size, count - i)
                systems = []

                for j in range(batch_count):
                    vendor = vendors[(i + j) % len(vendors)]
                    scada_type = scada_types[(i + j) % len(scada_types)]

                    system = {
                        "scadaId": f"water:scada:{scada_type.lower().replace(' ', '_')}-{i+j:04d}",
                        "systemName": f"{vendor} {scada_type} System {i+j}",
                        "vendor": vendor,
                        "scadaType": scada_type,
                        "softwareVersion": f"v{(i+j) % 5 + 6}.{(i+j) % 10}",
                        "networkSegment": f"VLAN-{100 + (i+j) % 10}",
                        "securityLevel": ["High", "Medium", "Low"][(i+j) % 3],
                        "lastSecurityAudit": "2024-08-15",
                        "authenticationType": ["MFA", "Password", "Certificate"][(i+j) % 3],
                        "encryptionEnabled": (i + j) % 2 == 0
                    }
                    systems.append(system)

                query = """
                UNWIND $systems AS system
                CREATE (ss:SCADASystem)
                SET ss = system,
                    ss.deploymentDate = datetime(),
                    ss.lastUpdated = datetime()
                RETURN count(ss) as created
                """

                result = session.run(query, systems=systems)
                batch_created = result.single()["created"]
                created += batch_created

        self.metrics["nodes_created"] += created
        self.log_operation("phase_completed", {"phase": "create_scada_systems", "nodes_created": created})
        return created

    def create_water_zones(self, count: int = 200) -> int:
        """Create Water:WaterZone nodes"""
        self.log_operation("phase_started", {"phase": "create_water_zones", "target_count": count})

        zone_types = ["Treatment", "Distribution", "Reservoir", "Pumping", "Collection"]

        with self.driver.session() as session:
            created = 0
            batch_size = 50

            for i in range(0, count, batch_size):
                batch_count = min(batch_size, count - i)
                zones = []

                for j in range(batch_count):
                    zone_type = zone_types[(i + j) % len(zone_types)]

                    zone = {
                        "zoneId": f"water:zone:{zone_type.lower()}-{i+j:04d}",
                        "zoneName": f"{zone_type} Zone {chr(65 + (i+j) % 26)}",
                        "zoneType": zone_type,
                        "coverage": f"{(i+j) % 50 + 10} square miles",
                        "population": (i + j) * 1000 + 5000,
                        "regulatoryAuthority": ["EPA Region 1", "EPA Region 2", "EPA Region 3"][(i+j) % 3],
                        "criticality": ["Critical", "High", "Medium", "Low"][(i+j) % 4]
                    }
                    zones.append(zone)

                query = """
                UNWIND $zones AS zone
                CREATE (wz:WaterZone)
                SET wz = zone,
                    wz.establishedDate = datetime(),
                    wz.lastUpdated = datetime()
                RETURN count(wz) as created
                """

                result = session.run(query, zones=zones)
                batch_created = result.single()["created"]
                created += batch_created

        self.metrics["nodes_created"] += created
        self.log_operation("phase_completed", {"phase": "create_water_zones", "nodes_created": created})
        return created

    def create_water_measurements(self, count: int = 9000) -> int:
        """Create water-specific measurements"""
        self.log_operation("phase_started", {"phase": "create_water_measurements", "target_count": count})

        with self.driver.session() as session:
            created = 0
            batch_size = 500

            for i in range(0, count, batch_size):
                batch_count = min(batch_size, count - i)
                measurements = []

                for j in range(batch_count):
                    meas = {
                        "measurementId": f"water:meas:wtr-{i+j:08d}",
                        "value": 15.0 + (i + j) % 50 * 0.2,
                        "quality": ["Good", "Uncertain", "Bad"][(i + j) % 3],
                        "anomalyScore": min(1.0, (i + j) % 100 * 0.01),
                        "isAnomaly": ((i + j) % 100) > 92,
                        "confidenceLevel": 0.80 + (i + j) % 20 * 0.01
                    }
                    measurements.append(meas)

                query = """
                UNWIND $measurements AS measurement
                CREATE (m:Measurement)
                SET m = measurement,
                    m.timestamp = datetime()
                RETURN count(m) as created
                """

                result = session.run(query, measurements=measurements)
                batch_created = result.single()["created"]
                created += batch_created

        self.metrics["nodes_created"] += created
        self.log_operation("phase_completed", {"phase": "create_water_measurements", "nodes_created": created})
        return created

    def create_water_alerts(self, count: int = 500) -> int:
        """Create Water:Alert nodes for security and quality incidents"""
        self.log_operation("phase_started", {"phase": "create_water_alerts", "target_count": count})

        alert_types = ["WaterQuality", "CyberSecurity", "OperationalAnomaly", "RegulatoryCompliance"]
        severities = ["Critical", "High", "Medium", "Low"]

        with self.driver.session() as session:
            created = 0
            batch_size = 50

            for i in range(0, count, batch_size):
                batch_count = min(batch_size, count - i)
                alerts = []

                for j in range(batch_count):
                    alert = {
                        "alertId": f"water:alert:alert-{i+j:06d}",
                        "alertType": alert_types[(i + j) % len(alert_types)],
                        "severity": severities[(i + j) % len(severities)],
                        "description": f"Alert for {alert_types[(i+j) % len(alert_types)]} incident {i+j}",
                        "status": ["Open", "Investigating", "Resolved"][(i + j) % 3],
                        "actionRequired": (i + j) % 3 == 0
                    }
                    alerts.append(alert)

                query = """
                UNWIND $alerts AS alert
                CREATE (wa:WaterAlert)
                SET wa = alert,
                    wa.timestamp = datetime(),
                    wa.lastUpdated = datetime()
                RETURN count(wa) as created
                """

                result = session.run(query, alerts=alerts)
                batch_created = result.single()["created"]
                created += batch_created

        self.metrics["nodes_created"] += created
        self.log_operation("phase_completed", {"phase": "create_water_alerts", "nodes_created": created})
        return created

    def create_relationships(self) -> int:
        """Create all Wave 2 relationships"""
        self.log_operation("phase_started", {"phase": "create_relationships"})

        with self.driver.session() as session:
            relationships_created = 0

            # 1. WaterDevice HAS_PROPERTY relationships
            result = session.run("""
                MATCH (wd:WaterDevice), (wp:WaterProperty)
                WHERE toInteger(split(wd.deviceId, '-')[1]) % 2 = toInteger(split(wp.propertyId, '-')[1]) % 2
                WITH wd, wp
                LIMIT 4500
                CREATE (wd)-[:HAS_PROPERTY]->(wp)
                RETURN count(*) as count
            """)
            count = result.single()["count"]
            relationships_created += count
            self.log_operation("relationships_created", {"type": "HAS_PROPERTY", "count": count})

            # 2. WaterProperty HAS_MEASUREMENT relationships
            result = session.run("""
                MATCH (wp:WaterProperty), (m:Measurement)
                WHERE wp.propertyId STARTS WITH 'water:'
                  AND m.measurementId STARTS WITH 'water:'
                  AND toInteger(split(wp.propertyId, '-')[1]) % 3 = toInteger(split(m.measurementId, '-')[1]) % 3
                WITH wp, m
                LIMIT 18000
                CREATE (wp)-[:HAS_MEASUREMENT]->(m)
                RETURN count(*) as count
            """)
            count = result.single()["count"]
            relationships_created += count
            self.log_operation("relationships_created", {"type": "HAS_MEASUREMENT", "count": count})

            # 3. TreatmentProcess USES_DEVICE relationships
            result = session.run("""
                MATCH (tp:TreatmentProcess), (wd:WaterDevice)
                WHERE toInteger(split(tp.processId, '-')[1]) % 3 = toInteger(split(wd.deviceId, '-')[1]) % 3
                WITH tp, wd
                LIMIT 2000
                CREATE (tp)-[:USES_DEVICE]->(wd)
                RETURN count(*) as count
            """)
            count = result.single()["count"]
            relationships_created += count
            self.log_operation("relationships_created", {"type": "USES_DEVICE", "count": count})

            # 4. SCADASystem CONTROLS relationships
            result = session.run("""
                MATCH (ss:SCADASystem), (wd:WaterDevice)
                WHERE toInteger(split(ss.scadaId, '-')[1]) % 5 = toInteger(split(wd.deviceId, '-')[1]) % 5
                WITH ss, wd
                LIMIT 3000
                CREATE (ss)-[:CONTROLS]->(wd)
                RETURN count(*) as count
            """)
            count = result.single()["count"]
            relationships_created += count
            self.log_operation("relationships_created", {"type": "CONTROLS", "count": count})

            # 5. WaterZone CONTAINS relationships
            result = session.run("""
                MATCH (wz:WaterZone), (wd:WaterDevice)
                WHERE toInteger(split(wz.zoneId, '-')[1]) % 4 = toInteger(split(wd.deviceId, '-')[1]) % 4
                WITH wz, wd
                LIMIT 2500
                CREATE (wz)-[:CONTAINS]->(wd)
                RETURN count(*) as count
            """)
            count = result.single()["count"]
            relationships_created += count
            self.log_operation("relationships_created", {"type": "CONTAINS", "count": count})

            # 6. WaterAlert TRIGGERED_BY relationships
            result = session.run("""
                MATCH (wa:WaterAlert), (wd:WaterDevice)
                WHERE wa.severity IN ['Critical', 'High']
                WITH wa, wd
                LIMIT 1000
                CREATE (wa)-[:TRIGGERED_BY]->(wd)
                RETURN count(*) as count
            """)
            count = result.single()["count"]
            relationships_created += count
            self.log_operation("relationships_created", {"type": "TRIGGERED_BY", "count": count})

            # 7. Connect to Wave 1 SAREF devices
            result = session.run("""
                MATCH (wd:WaterDevice), (d:Device)
                WHERE NOT d:WaterDevice
                  AND d.manufacturer = wd.manufacturer
                WITH wd, d
                LIMIT 1500
                CREATE (wd)-[:EXTENDS_SAREF_DEVICE]->(d)
                RETURN count(*) as count
            """)
            count = result.single()["count"]
            relationships_created += count
            self.log_operation("relationships_created", {"type": "EXTENDS_SAREF_DEVICE", "count": count})

            # 8. Connect water devices to CVEs
            result = session.run("""
                MATCH (wd:WaterDevice), (cve:CVE)
                WHERE (cve.description CONTAINS 'water' OR cve.description CONTAINS 'SCADA' OR cve.description CONTAINS 'industrial')
                  AND wd.manufacturer = 'Siemens'
                WITH wd, cve
                LIMIT 5000
                CREATE (wd)-[:VULNERABLE_TO {
                    discoveredDate: datetime(),
                    severity: cve.severity,
                    waterSpecificRisk: 'High',
                    mitigationStatus: 'Pending'
                }]->(cve)
                RETURN count(*) as count
            """)
            count = result.single()["count"]
            relationships_created += count
            self.log_operation("relationships_created", {"type": "VULNERABLE_TO", "manufacturer": "Siemens", "count": count})

            # Additional manufacturer CVE mappings
            for mfr in ["Rockwell", "Schneider", "GE", "ABB"]:
                result = session.run(f"""
                    MATCH (wd:WaterDevice), (cve:CVE)
                    WHERE wd.manufacturer CONTAINS '{mfr}'
                      AND (cve.description CONTAINS '{mfr}' OR cve.description CONTAINS 'water' OR cve.description CONTAINS 'industrial')
                    WITH wd, cve
                    LIMIT 2500
                    CREATE (wd)-[:VULNERABLE_TO {{
                        discoveredDate: datetime(),
                        severity: cve.severity,
                        waterSpecificRisk: 'High',
                        mitigationStatus: 'Pending'
                    }}]->(cve)
                    RETURN count(*) as count
                """)
                count = result.single()["count"]
                relationships_created += count
                self.log_operation("relationships_created", {"type": "VULNERABLE_TO", "manufacturer": mfr, "count": count})

        self.metrics["relationships_created"] = relationships_created
        self.log_operation("phase_completed", {"phase": "create_relationships", "total_relationships": relationships_created})
        return relationships_created

    def execute_wave_2(self) -> Dict[str, Any]:
        """Execute complete Wave 2 implementation"""
        self.metrics["start_time"] = datetime.now().isoformat()
        self.log_operation("wave_2_execution_started", {"timestamp": self.metrics["start_time"]})

        try:
            # Phase 1: Create constraints and indexes
            print("\n📋 Phase 1: Creating constraints and indexes...")
            self.create_constraints_and_indexes()

            # Phase 2: Create water infrastructure nodes
            print("\n🏗️  Phase 2: Creating water infrastructure nodes...")
            print("  - Creating 1,500 WaterDevice nodes...")
            self.create_water_devices(1500)

            print("  - Creating 3,000 WaterProperty nodes...")
            self.create_water_properties(3000)

            print("  - Creating 500 TreatmentProcess nodes...")
            self.create_treatment_processes(500)

            print("  - Creating 300 SCADASystem nodes...")
            self.create_scada_systems(300)

            print("  - Creating 200 WaterZone nodes...")
            self.create_water_zones(200)

            print("  - Creating 9,000 Water Measurement nodes...")
            self.create_water_measurements(9000)

            print("  - Creating 500 WaterAlert nodes...")
            self.create_water_alerts(500)

            # Phase 3: Create relationships
            print("\n🔗 Phase 3: Creating relationships...")
            self.create_relationships()

            self.metrics["end_time"] = datetime.now().isoformat()
            self.log_operation("wave_2_execution_completed", {
                "timestamp": self.metrics["end_time"],
                "nodes_created": self.metrics["nodes_created"],
                "relationships_created": self.metrics["relationships_created"],
                "constraints_created": self.metrics["constraints_created"],
                "indexes_created": self.metrics["indexes_created"]
            })

            return self.metrics

        except Exception as e:
            self.metrics["errors"].append(str(e))
            self.log_operation("wave_2_execution_failed", {"error": str(e)})
            logger.error("wave_2_execution_failed", error=str(e))
            raise

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()
        logger.info("neo4j_connection_closed")


# CLI Interface
if __name__ == "__main__":
    print("\n" + "="*60)
    print("Wave 2: Water Infrastructure Domain Extensions")
    print("="*60)

    executor = Wave2Executor()

    try:
        metrics = executor.execute_wave_2()

        print("\n" + "="*60)
        print("✅ Wave 2 Execution Complete")
        print("="*60)
        print(f"📊 Nodes Created: {metrics['nodes_created']:,}")
        print(f"🔗 Relationships Created: {metrics['relationships_created']:,}")
        print(f"📋 Constraints Created: {metrics['constraints_created']}")
        print(f"📇 Indexes Created: {metrics['indexes_created']}")
        print(f"⏱️  Duration: {metrics['start_time']} to {metrics['end_time']}")
        print(f"📄 Logs: /home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/logs/wave_2_execution.jsonl")

    except Exception as e:
        print(f"\n❌ Wave 2 Execution Failed: {e}")
        raise

    finally:
        executor.close()
