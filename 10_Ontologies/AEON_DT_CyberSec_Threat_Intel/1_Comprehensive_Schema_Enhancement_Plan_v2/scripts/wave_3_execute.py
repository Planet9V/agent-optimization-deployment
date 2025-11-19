#!/usr/bin/env python3
"""
Wave 3 Executor: Energy Grid Domain Extensions
Extends SAREF core (Wave 1) with energy infrastructure modeling
Integrates with Water Infrastructure (Wave 2) and existing CVE data
"""

import json
import logging
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

from neo4j import GraphDatabase


class Wave3Executor:
    """Execute Wave 3: Energy Grid Domain Extensions with CVE preservation"""

    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.log_file = Path("/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/logs/wave_3_execution.jsonl")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def log_operation(self, operation: str, details: Dict[str, Any]):
        """Log operation to JSONL file"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "operation": operation,
            "details": details
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        self.logger.info(f"{operation}: {details}")

    def execute(self):
        """Execute Wave 3 implementation"""
        try:
            self.log_operation("wave_3_execution_started", {"timestamp": datetime.utcnow().isoformat()})

            # Phase 1: Create constraints and indexes
            self.log_operation("phase_started", {"phase": "constraints_and_indexes"})
            self.create_constraints_and_indexes()
            self.log_operation("phase_completed", {"phase": "constraints_and_indexes"})

            # Phase 2: Create energy devices (8,000-12,000 target: 10,000)
            self.log_operation("phase_started", {"phase": "create_energy_devices", "target_count": 10000})
            energy_device_count = self.create_energy_devices(count=10000)
            self.log_operation("phase_completed", {"phase": "create_energy_devices", "nodes_created": energy_device_count})

            # Phase 3: Create energy properties (5,000-7,000 target: 6,000)
            self.log_operation("phase_started", {"phase": "create_energy_properties", "target_count": 6000})
            energy_property_count = self.create_energy_properties(count=6000)
            self.log_operation("phase_completed", {"phase": "create_energy_properties", "nodes_created": energy_property_count})

            # Phase 4: Create substations (150-250 target: 200)
            self.log_operation("phase_started", {"phase": "create_substations", "target_count": 200})
            substation_count = self.create_substations(count=200)
            self.log_operation("phase_completed", {"phase": "create_substations", "nodes_created": substation_count})

            # Phase 5: Create transmission lines (300-500 target: 400)
            self.log_operation("phase_started", {"phase": "create_transmission_lines", "target_count": 400})
            transmission_line_count = self.create_transmission_lines(count=400)
            self.log_operation("phase_completed", {"phase": "create_transmission_lines", "nodes_created": transmission_line_count})

            # Phase 6: Create EMS/SCADA systems (15-30 target: 25)
            self.log_operation("phase_started", {"phase": "create_ems_systems", "target_count": 25})
            ems_count = self.create_ems_systems(count=25)
            self.log_operation("phase_completed", {"phase": "create_ems_systems", "nodes_created": ems_count})

            # Phase 7: Create DERs (500-1,000 target: 750)
            self.log_operation("phase_started", {"phase": "create_ders", "target_count": 750})
            der_count = self.create_ders(count=750)
            self.log_operation("phase_completed", {"phase": "create_ders", "nodes_created": der_count})

            # Phase 8: Create NERC CIP standards (80-120 target: 100)
            self.log_operation("phase_started", {"phase": "create_nerc_standards", "target_count": 100})
            nerc_count = self.create_nerc_standards(count=100)
            self.log_operation("phase_completed", {"phase": "create_nerc_standards", "nodes_created": nerc_count})

            # Phase 9: Create energy measurements (same pattern as Wave 1/2)
            self.log_operation("phase_started", {"phase": "create_energy_measurements", "target_count": 18000})
            measurement_count = self.create_energy_measurements(count=18000)
            self.log_operation("phase_completed", {"phase": "create_energy_measurements", "nodes_created": measurement_count})

            # Phase 10: Create all relationships
            self.log_operation("phase_started", {"phase": "create_relationships"})
            relationship_counts = self.create_relationships()
            self.log_operation("phase_completed", {"phase": "create_relationships", "total_relationships": sum(relationship_counts.values())})

            # Calculate totals
            total_nodes = (energy_device_count + energy_property_count + substation_count +
                          transmission_line_count + ems_count + der_count + nerc_count + measurement_count)
            total_relationships = sum(relationship_counts.values())

            self.log_operation("wave_3_execution_completed", {
                "timestamp": datetime.utcnow().isoformat(),
                "nodes_created": total_nodes,
                "relationships_created": total_relationships
            })

            return True

        except Exception as e:
            self.log_operation("wave_3_execution_error", {"error": str(e)})
            self.logger.error(f"Wave 3 execution failed: {e}", exc_info=True)
            return False
        finally:
            self.driver.close()

    def create_constraints_and_indexes(self):
        """Create all constraints and indexes for Wave 3"""
        constraints_and_indexes = [
            # Constraints
            "CREATE CONSTRAINT energy_device_id_unique IF NOT EXISTS FOR (ed:EnergyDevice) REQUIRE ed.deviceId IS UNIQUE",
            "CREATE CONSTRAINT energy_property_id_unique IF NOT EXISTS FOR (ep:EnergyProperty) REQUIRE ep.propertyId IS UNIQUE",
            "CREATE CONSTRAINT substation_id_unique IF NOT EXISTS FOR (sub:Substation) REQUIRE sub.substationId IS UNIQUE",
            "CREATE CONSTRAINT transmission_line_id_unique IF NOT EXISTS FOR (tl:TransmissionLine) REQUIRE tl.lineId IS UNIQUE",
            "CREATE CONSTRAINT ems_id_unique IF NOT EXISTS FOR (ems:EnergyManagementSystem) REQUIRE ems.emsId IS UNIQUE",
            "CREATE CONSTRAINT der_id_unique IF NOT EXISTS FOR (der:DistributedEnergyResource) REQUIRE der.derId IS UNIQUE",
            "CREATE CONSTRAINT nerc_standard_id_unique IF NOT EXISTS FOR (ncs:NERCCIPStandard) REQUIRE ncs.standardId IS UNIQUE",

            # Energy Device Indexes
            "CREATE INDEX energy_device_type_idx IF NOT EXISTS FOR (ed:EnergyDevice) ON (ed.energyDeviceType)",
            "CREATE INDEX energy_voltage_level_idx IF NOT EXISTS FOR (ed:EnergyDevice) ON (ed.voltageLevel)",
            "CREATE INDEX energy_nerc_category_idx IF NOT EXISTS FOR (ed:EnergyDevice) ON (ed.nercCIPCategory)",
            "CREATE INDEX energy_substation_idx IF NOT EXISTS FOR (ed:EnergyDevice) ON (ed.substationId)",
            "CREATE INDEX energy_grid_impact_idx IF NOT EXISTS FOR (ed:EnergyDevice) ON (ed.gridImpactLevel, ed.nercCIPCompliance)",

            # Energy Property Indexes
            "CREATE INDEX energy_property_category_idx IF NOT EXISTS FOR (ep:EnergyProperty) ON (ep.energyPropertyCategory)",
            "CREATE INDEX energy_grid_stability_idx IF NOT EXISTS FOR (ep:EnergyProperty) ON (ep.gridStabilityImpact)",
            "CREATE INDEX energy_ieee_standard_idx IF NOT EXISTS FOR (ep:EnergyProperty) ON (ep.ieeeStandard)",

            # Substation Indexes
            "CREATE INDEX substation_type_idx IF NOT EXISTS FOR (sub:Substation) ON (sub.substationType)",
            "CREATE INDEX substation_voltage_idx IF NOT EXISTS FOR (sub:Substation) ON (sub.voltageClass)",
            "CREATE INDEX substation_nerc_idx IF NOT EXISTS FOR (sub:Substation) ON (sub.nercCIPSite)",

            # Transmission Line Indexes
            "CREATE INDEX transmission_voltage_idx IF NOT EXISTS FOR (tl:TransmissionLine) ON (tl.voltageLevel)",
            "CREATE INDEX transmission_critical_idx IF NOT EXISTS FOR (tl:TransmissionLine) ON (tl.criticalPath)",

            # EMS Indexes
            "CREATE INDEX ems_type_idx IF NOT EXISTS FOR (ems:EnergyManagementSystem) ON (ems.emsType)",
            "CREATE INDEX ems_vendor_idx IF NOT EXISTS FOR (ems:EnergyManagementSystem) ON (ems.vendor)",
            "CREATE INDEX ems_network_architecture_idx IF NOT EXISTS FOR (ems:EnergyManagementSystem) ON (ems.networkArchitecture)",

            # DER Indexes
            "CREATE INDEX der_type_idx IF NOT EXISTS FOR (der:DistributedEnergyResource) ON (der.derType)",
            "CREATE INDEX der_derms_idx IF NOT EXISTS FOR (der:DistributedEnergyResource) ON (der.dermsManaged)",

            # NERC CIP Indexes
            "CREATE INDEX nerc_cip_number_idx IF NOT EXISTS FOR (ncs:NERCCIPStandard) ON (ncs.cipNumber)",
            "CREATE INDEX nerc_severity_idx IF NOT EXISTS FOR (ncs:NERCCIPStandard) ON (ncs.violationSeverity)"
        ]

        with self.driver.session() as session:
            for statement in constraints_and_indexes:
                session.run(statement)
                self.log_operation("constraint_or_index_created", {"statement": statement[:60] + "..."})

    def create_energy_devices(self, count: int = 10000) -> int:
        """Create EnergyDevice nodes extending SAREF:Device"""
        device_types = [
            ("Generator", "Siemens Energy", "SGT-800", "Transmission-500kV", 150.0, 500.0, "BES-Cyber-Asset", "Critical"),
            ("Transformer", "ABB", "RESIBLOC", "Transmission-230kV", 100.0, 230.0, "BES-Cyber-Asset", "Critical"),
            ("CircuitBreaker", "GE Grid Solutions", "IQ UX", "Subtransmission-115kV", 50.0, 115.0, "BES-Cyber-Asset", "High"),
            ("SmartMeter", "Itron", "OpenWay Riva", "Secondary-240V", 0.01, 0.24, "Non-BES", "Low"),
            ("RTU", "Schweitzer Engineering", "SEL-3505", "Distribution-12.47kV", 0.0, 12.47, "EACMS", "High"),
            ("IED", "Siemens Energy", "SIPROTEC 5", "Transmission-115kV", 0.0, 115.0, "BES-Cyber-Asset", "Critical"),
            ("PMU", "GE Grid Solutions", "N60", "Transmission-500kV", 0.0, 500.0, "BES-Cyber-Asset", "Critical"),
            ("Inverter", "SMA Solar", "Sunny Central 2750", "Distribution-12.47kV", 2.75, 12.47, "Non-BES", "Medium")
        ]

        manufacturers = ["Siemens Energy", "ABB", "GE Grid Solutions", "Schweitzer Engineering Laboratories",
                        "Itron", "SMA Solar", "Eaton", "Schneider Electric"]

        protocols = [
            ["DNP3", "IEC-61850"],
            ["Modbus/TCP", "IEC-61850"],
            ["DNP3", "Modbus/TCP"],
            ["IEC-61850", "Modbus/TCP", "GOOSE"]
        ]

        nerc_categories = ["BES-Cyber-Asset", "EACMS", "PACS", "Non-BES"]
        compliance_status = ["Compliant", "NonCompliant", "Exempt"]
        patch_levels = ["Critical-Patches-Applied", "Pending-Updates", "End-of-Life"]

        batch_size = 50
        total_created = 0

        with self.driver.session() as session:
            for i in range(0, count, batch_size):
                devices = []
                batch_count = min(batch_size, count - i)

                for j in range(batch_count):
                    dev_type, mfr, model, voltage, capacity, rated_voltage, nerc_cat, impact = random.choice(device_types)

                    device = {
                        # SAREF:Device inherited properties
                        "deviceId": f"energy:device:{dev_type.lower()}-{i+j:06d}",
                        "name": f"{mfr} {model} {dev_type} Unit {i+j}",
                        "model": model,
                        "manufacturer": mfr,
                        "firmwareVersion": f"V{random.randint(2,5)}.{random.randint(0,9)}.{random.randint(0,20)}",
                        "serialNumber": f"SN-{random.randint(100000, 999999)}",
                        "deviceCategory": "Controller" if dev_type in ["Generator", "Transformer", "CircuitBreaker"] else "Sensor",
                        "deploymentLocation": f"Substation-{random.randint(1, 200):03d}",
                        "ipAddress": f"192.168.{random.randint(10, 50)}.{random.randint(1, 254)}",
                        "protocol": random.choice(protocols),
                        "criticality": impact,

                        # Energy-specific properties
                        "energyDeviceType": dev_type,
                        "voltageLevel": voltage,
                        "ratedCapacity": capacity,
                        "ratedVoltage": rated_voltage,
                        "ratedCurrent": capacity / rated_voltage if rated_voltage > 0 else 0.0,
                        "nercCIPCategory": nerc_cat,
                        "substationId": f"SUBST-{random.randint(1, 200):03d}",
                        "feederNumber": f"FEEDER-{random.randint(1, 100):03d}" if "Distribution" in voltage else None,
                        "iedFunctionType": random.choice(["Protection", "Control", "Metering", "Monitoring"]),
                        "communicationProtocol": random.choice(protocols),
                        "cybersecurityPatchLevel": random.choice(patch_levels),
                        "nercCIPCompliance": random.choice(compliance_status),
                        "gridImpactLevel": impact
                    }
                    devices.append(device)

                query = """
                UNWIND $devices AS device
                CREATE (ed:Energy:EnergyDevice:Device)
                SET ed = device,
                    ed.commissionDate = datetime(),
                    ed.operationalStatus = 'Active',
                    ed.lastUpdated = datetime(),
                    ed.lastFirmwareUpdate = datetime() - duration({days: toInteger(rand() * 336) + 30}),
                    ed.macAddress = '00:' + substring(device.deviceId, 15, 2) + ':' +
                                   substring(device.deviceId, 17, 2) + ':' +
                                   substring(device.deviceId, 19, 2) + ':' +
                                   substring(device.deviceId, 21, 2) + ':' +
                                   substring(device.deviceId, 23, 2)
                RETURN count(ed) as created
                """

                result = session.run(query, devices=devices)
                created = result.single()["created"]
                total_created += created

                if i % 500 == 0 or i + batch_size >= count:
                    self.log_operation("energy_devices_batch_created", {
                        "batch": i // batch_size,
                        "count": created,
                        "total": total_created
                    })

        return total_created

    def create_energy_properties(self, count: int = 6000) -> int:
        """Create EnergyProperty nodes extending SAREF:Property"""
        property_types = [
            ("Voltage", "Electrical", "Critical", 60.0, "IEEE-1547", "kV", 0.0, 600.0),
            ("Current", "Electrical", "High", 0.0, "IEEE-519", "Amperes", 0.0, 5000.0),
            ("Frequency", "Frequency", "Critical", 60.0, "IEEE-1547", "Hz", 57.0, 63.5),
            ("PowerFactor", "Power Quality", "High", 0.95, "IEEE-519", "pf", 0.0, 1.0),
            ("ActivePower", "Load", "Critical", 0.0, "IEEE-1459", "MW", 0.0, 1000.0),
            ("ReactivePower", "Load", "High", 0.0, "IEEE-1459", "MVAR", -500.0, 500.0),
            ("THD", "Power Quality", "Medium", 5.0, "IEEE-519", "%", 0.0, 100.0),
            ("Temperature", "Physical", "Medium", 25.0, None, "Celsius", -40.0, 150.0)
        ]

        grid_stability = ["Critical", "High", "Medium", "Low"]
        ieee_standards = ["IEEE-1547", "IEEE-519", "IEEE-1459", "IEEE-2030.5"]

        batch_size = 100
        total_created = 0

        with self.driver.session() as session:
            for i in range(0, count, batch_size):
                properties = []
                batch_count = min(batch_size, count - i)

                for j in range(batch_count):
                    prop_type, category, stability, nerc_limit, ieee_std, unit, min_val, max_val = random.choice(property_types)

                    property_data = {
                        # SAREF:Property inherited properties
                        "propertyId": f"energy:property:{prop_type.lower()}-{i+j:06d}",
                        "propertyType": prop_type,
                        "unitOfMeasure": unit,
                        "minValue": min_val,
                        "maxValue": max_val,
                        "normalRangeMin": min_val + (max_val - min_val) * 0.2,
                        "normalRangeMax": max_val - (max_val - min_val) * 0.2,
                        "criticalThresholdMin": min_val + (max_val - min_val) * 0.1,
                        "criticalThresholdMax": max_val - (max_val - min_val) * 0.1,
                        "measurementAccuracy": 0.001 if unit == "Hz" else 0.01,
                        "description": f"{prop_type} measurement for energy grid monitoring",

                        # Energy-specific properties
                        "energyPropertyCategory": category,
                        "gridStabilityImpact": stability,
                        "nercSTDLimit": nerc_limit,
                        "ieeeStandard": ieee_std or random.choice(ieee_standards),
                        "alarmThresholdHigh": max_val - (max_val - min_val) * 0.15,
                        "alarmThresholdLow": min_val + (max_val - min_val) * 0.15,
                        "tripThresholdHigh": max_val - (max_val - min_val) * 0.05,
                        "tripThresholdLow": min_val + (max_val - min_val) * 0.05
                    }
                    properties.append(property_data)

                query = """
                UNWIND $properties AS prop
                CREATE (ep:Energy:EnergyProperty:Property)
                SET ep = prop,
                    ep.lastCalibration = datetime() - duration({days: toInteger(rand() * 151) + 30}),
                    ep.protectionRelaySetpoint = CASE
                        WHEN prop.propertyType IN ['Voltage', 'Frequency']
                        THEN prop.normalRangeMax * 1.1
                        ELSE null
                    END
                RETURN count(ep) as created
                """

                result = session.run(query, properties=properties)
                created = result.single()["created"]
                total_created += created

                if i % 1000 == 0 or i + batch_size >= count:
                    self.log_operation("energy_properties_batch_created", {
                        "batch": i // batch_size,
                        "count": created,
                        "total": total_created
                    })

        return total_created

    def create_substations(self, count: int = 200) -> int:
        """Create Substation nodes"""
        substation_types = ["Transmission", "Distribution", "Collector", "Mobile"]
        voltage_classes = ["500kV", "230kV", "115kV", "69kV", "34.5kV", "12.47kV"]
        bus_configs = ["RingBus", "BreakerAndHalf", "DoubleBus", "SingleBus"]
        physical_security = ["Fenced-CardAccess", "Fenced-GuardPatrol", "OpenAccess"]

        with self.driver.session() as session:
            substations = []
            for i in range(count):
                substation = {
                    "substationId": f"energy:substation:sub-{i+1:03d}",
                    "substationName": f"Substation {i+1}",
                    "substationType": random.choice(substation_types),
                    "voltageClass": random.choice(voltage_classes),
                    "transformerCount": random.randint(1, 5),
                    "breakerCount": random.randint(4, 20),
                    "busConfiguration": random.choice(bus_configs),
                    "scadaCoverage": random.choice([True, False]),
                    "physicalSecurity": random.choice(physical_security),
                    "gpsCoordinates": f"{random.uniform(30, 50):.4f},{random.uniform(-120, -70):.4f}",
                    "nercCIPSite": random.choice([True, False]),
                    "criticalInfrastructure": random.choice([True, False]),
                    "loadServed": round(random.uniform(10.0, 200.0), 1),
                    "populationServed": random.randint(5000, 250000)
                }
                substations.append(substation)

            query = """
            UNWIND $substations AS sub
            CREATE (s:Energy:Substation)
            SET s = sub
            RETURN count(s) as created
            """

            result = session.run(query, substations=substations)
            created = result.single()["created"]
            self.log_operation("substations_created", {"count": created})
            return created

    def create_transmission_lines(self, count: int = 400) -> int:
        """Create TransmissionLine nodes"""
        voltage_levels = ["500kV", "230kV", "115kV"]
        conductor_types = ["ACSR-Drake", "ACSR-Cardinal", "ACCC", "ACCR"]
        nerc_designations = ["BES-Transmission", "Non-BES"]
        redundancy_levels = ["N-1", "N-2", "Radial"]
        monitoring_systems = ["SCADA-PMU", "SCADA-Only", "None"]

        with self.driver.session() as session:
            lines = []
            for i in range(count):
                line = {
                    "lineId": f"energy:line:tline-{i+1:03d}",
                    "lineName": f"Transmission Line {i+1}",
                    "voltageLevel": random.choice(voltage_levels),
                    "lineLength": round(random.uniform(5.0, 150.0), 1),
                    "conductorType": random.choice(conductor_types),
                    "thermalRating": round(random.uniform(100.0, 500.0), 1),
                    "impedance": round(random.uniform(1.0, 50.0), 2),
                    "nercCIPDesignation": random.choice(nerc_designations),
                    "criticalPath": random.choice([True, False]),
                    "redundancyLevel": random.choice(redundancy_levels),
                    "monitoringSystem": random.choice(monitoring_systems)
                }
                lines.append(line)

            query = """
            UNWIND $lines AS line
            CREATE (tl:Energy:TransmissionLine)
            SET tl = line
            RETURN count(tl) as created
            """

            result = session.run(query, lines=lines)
            created = result.single()["created"]
            self.log_operation("transmission_lines_created", {"count": created})
            return created

    def create_ems_systems(self, count: int = 25) -> int:
        """Create EnergyManagementSystem nodes"""
        ems_types = ["EMS", "SCADA", "DMS", "DERMS", "ADMS"]
        vendors = ["GE Grid Solutions", "Siemens Energy", "ABB", "OSIsoft", "Schneider Electric"]
        network_architectures = ["Flat", "Segmented", "DMZ-Protected", "ZeroTrust"]
        protocols = [["DNP3", "IEC-61850", "Modbus/TCP", "ICCP"],
                    ["DNP3", "Modbus/TCP"],
                    ["IEC-61850", "ICCP", "TASE.2"]]
        historians = ["OSIsoft PI", "Wonderware Historian", "GE Proficy", "Custom"]
        nerc_compliance = [["CIP-005", "CIP-007", "CIP-010"],
                          ["CIP-005", "CIP-007", "CIP-010", "CIP-011"],
                          ["CIP-002", "CIP-003", "CIP-004", "CIP-005"]]

        with self.driver.session() as session:
            ems_systems = []
            for i in range(count):
                ems = {
                    "emsId": f"energy:ems:ems-{i+1:03d}",
                    "systemName": f"Energy Management System {i+1}",
                    "emsType": random.choice(ems_types),
                    "vendor": random.choice(vendors),
                    "softwareVersion": f"v{random.randint(5, 12)}.{random.randint(0, 9)}.{random.randint(0, 5)}",
                    "controlCenterLocation": f"Control Center Building {random.randint(1, 5)}, Floor {random.randint(1, 4)}",
                    "rtuCount": random.randint(50, 500),
                    "iedCount": random.randint(500, 3000),
                    "smartMeterCount": random.randint(10000, 1000000),
                    "pmuCount": random.randint(5, 50),
                    "networkArchitecture": random.choice(network_architectures),
                    "communicationProtocols": random.choice(protocols),
                    "dataHistorian": random.choice(historians),
                    "remoteAccessEnabled": random.choice([True, False]),
                    "vpnRequired": True,
                    "multiFactorAuth": random.choice([True, False]),
                    "encryptionInTransit": random.choice([True, False]),
                    "siemIntegration": random.choice([True, False]),
                    "incidentResponsePlan": f"IRP-ENERGY-2024-v{random.randint(1, 5)}",
                    "nercCIPCompliance": random.choice(nerc_compliance)
                }
                ems_systems.append(ems)

            query = """
            UNWIND $ems_systems AS ems
            CREATE (e:Energy:EnergyManagementSystem)
            SET e = ems,
                e.lastPenetrationTest = datetime() - duration({days: toInteger(rand() * 336) + 30})
            RETURN count(e) as created
            """

            result = session.run(query, ems_systems=ems_systems)
            created = result.single()["created"]
            self.log_operation("ems_systems_created", {"count": created})
            return created

    def create_ders(self, count: int = 750) -> int:
        """Create DistributedEnergyResource nodes"""
        der_types = ["Solar-PV", "Wind-Turbine", "Battery-Storage", "Microgrid"]
        inverter_models = ["SMA Sunny Central 2750", "ABB PVS980", "GE LV5+", "Schneider Electric Conext"]
        grid_connections = ["Utility-Scale", "Commercial", "Residential"]
        protocols = ["IEEE-2030.5", "Modbus/TCP", "SunSpec", "DNP3"]
        ieee_modes = ["ConstantPowerFactor", "VoltVAR", "FreqWatt", "DynamicReactiveCurrent"]

        with self.driver.session() as session:
            ders = []
            for i in range(count):
                der_type = random.choice(der_types)
                der = {
                    "derId": f"energy:der:{der_type.lower().replace('-', '_')}-{i+1:04d}",
                    "derName": f"{der_type} Resource {i+1}",
                    "derType": der_type,
                    "capacity": round(random.uniform(0.5, 50.0), 1),
                    "inverterModel": random.choice(inverter_models) if der_type != "Wind-Turbine" else None,
                    "ieee1547Compliant": random.choice([True, False]),
                    "gridConnection": random.choice(grid_connections),
                    "communicationProtocol": random.choice(protocols),
                    "remoteControlEnabled": random.choice([True, False]),
                    "dermsManaged": random.choice([True, False]),
                    "cybersecurityCertified": random.choice([True, False])
                }
                ders.append(der)

            query = """
            UNWIND $ders AS der
            CREATE (d:Energy:DistributedEnergyResource)
            SET d = der,
                d.lastSecurityAssessment = datetime() - duration({days: toInteger(rand() * 671) + 60})
            RETURN count(d) as created
            """

            result = session.run(query, ders=ders)
            created = result.single()["created"]
            self.log_operation("ders_created", {"count": created})
            return created

    def create_nerc_standards(self, count: int = 100) -> int:
        """Create NERCCIPStandard nodes"""
        cip_numbers = ["CIP-002", "CIP-003", "CIP-004", "CIP-005", "CIP-006", "CIP-007",
                      "CIP-008", "CIP-009", "CIP-010", "CIP-011", "CIP-013", "CIP-014"]
        requirements = ["R1", "R2", "R3", "R4", "R5"]
        applicability_options = [
            ["BES-Cyber-Asset"],
            ["BES-Cyber-Asset", "EACMS"],
            ["BES-Cyber-Asset", "EACMS", "PACS"],
            ["EACMS", "PACS"],
            ["PCAs"]
        ]
        enforcement_levels = ["Mandatory", "Recommended"]
        severity_levels = ["High", "Medium", "Lower"]
        audit_frequencies = ["Annual", "Triennial"]

        titles = {
            "CIP-002": "BES Cyber System Categorization",
            "CIP-003": "Security Management Controls",
            "CIP-004": "Personnel & Training",
            "CIP-005": "Electronic Security Perimeters",
            "CIP-006": "Physical Security",
            "CIP-007": "System Security Management",
            "CIP-008": "Incident Reporting and Response",
            "CIP-009": "Recovery Plans",
            "CIP-010": "Configuration Change Management",
            "CIP-011": "Information Protection",
            "CIP-013": "Supply Chain Risk Management",
            "CIP-014": "Physical Security - Transmission"
        }

        with self.driver.session() as session:
            standards = []
            for cip in cip_numbers:
                for req in requirements[:random.randint(3, 5)]:
                    standard = {
                        "standardId": f"energy:standard:nerc-{cip.lower()}-{req.lower()}",
                        "cipNumber": f"{cip}-7",
                        "requirementNumber": req,
                        "title": titles.get(cip, "NERC CIP Requirement"),
                        "description": f"{titles.get(cip, 'NERC CIP')} - Requirement {req}",
                        "applicability": random.choice(applicability_options),
                        "complianceEnforcement": random.choice(enforcement_levels),
                        "violationSeverity": random.choice(severity_levels),
                        "auditFrequency": random.choice(audit_frequencies),
                        "effectiveDate": (datetime.utcnow() - timedelta(days=random.randint(30, 730))).isoformat()
                    }
                    standards.append(standard)
                    if len(standards) >= count:
                        break
                if len(standards) >= count:
                    break

            query = """
            UNWIND $standards AS std
            CREATE (ncs:Energy:NERCCIPStandard)
            SET ncs = std,
                ncs.effectiveDate = datetime(std.effectiveDate)
            RETURN count(ncs) as created
            """

            result = session.run(query, standards=standards[:count])
            created = result.single()["created"]
            self.log_operation("nerc_standards_created", {"count": created})
            return created

    def create_energy_measurements(self, count: int = 18000) -> int:
        """Create Measurement nodes for energy properties (reuse Wave 1/2 pattern)"""
        with self.driver.session() as session:
            # Create measurements for energy properties - 3 measurements per property
            # 6000 properties × 3 = 18000 measurements
            query = """
            MATCH (ep:EnergyProperty)
            WITH ep, range(1, 3) as indices
            UNWIND indices as idx
            CREATE (m:Measurement {
                measurementId: 'energy:measurement:' + ep.propertyId + '-' + toString(timestamp() + idx),
                timestamp: datetime() - duration({hours: idx}),
                value: ep.normalRangeMin + rand() * (ep.normalRangeMax - ep.normalRangeMin),
                unitOfMeasure: ep.unitOfMeasure,
                quality: CASE WHEN rand() > 0.95 THEN 'Anomaly' ELSE 'Normal' END,
                sourceProperty: ep.propertyId
            })
            WITH ep, m
            CREATE (ep)-[:GENERATES_MEASUREMENT {
                generatedAt: m.timestamp,
                measurementType: 'Periodic'
            }]->(m)
            RETURN count(m) as created
            """

            result = session.run(query)
            total_created = result.single()["created"]

        self.log_operation("energy_measurements_created", {"count": total_created})
        return total_created

    def create_relationships(self) -> Dict[str, int]:
        """Create all relationships for Wave 3"""
        relationship_counts = {}

        with self.driver.session() as session:
            # 1. INSTALLED_AT_SUBSTATION (EnergyDevice → Substation) - 10,000 devices → 200 substations
            # Match devices to substations by extracting numeric ID
            query = """
            MATCH (ed:EnergyDevice)
            WITH ed, split(ed.substationId, '-')[1] as substationNum
            MATCH (sub:Substation)
            WHERE sub.substationId = 'energy:substation:sub-' + substationNum
            WITH ed, sub
            LIMIT 10000
            CREATE (ed)-[r:INSTALLED_AT_SUBSTATION {
                bayNumber: 'Bay-' + toString(toInteger(rand() * 8) + 1),
                installationDate: datetime() - duration({days: toInteger(rand() * 1796) + 30}),
                primaryFunction: CASE ed.energyDeviceType
                    WHEN 'Generator' THEN 'Power Generation'
                    WHEN 'Transformer' THEN 'Power Transformation'
                    WHEN 'CircuitBreaker' THEN 'Protection'
                    WHEN 'RTU' THEN 'Control'
                    WHEN 'IED' THEN 'Monitoring'
                    ELSE 'Metering'
                END
            }]->(sub)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["INSTALLED_AT_SUBSTATION"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "INSTALLED_AT_SUBSTATION", "count": relationship_counts["INSTALLED_AT_SUBSTATION"]})

            # 2. CONNECTS_SUBSTATIONS (TransmissionLine → Substation) - 400 lines × 2 = 800
            query = """
            MATCH (tl:TransmissionLine)
            MATCH (sub:Substation)
            WHERE sub.voltageClass = tl.voltageLevel
            WITH tl, collect(sub) as substations
            WHERE size(substations) >= 2
            WITH tl, substations[toInteger(rand() * size(substations))] as source,
                     substations[toInteger(rand() * size(substations))] as dest
            WHERE source <> dest
            CREATE (tl)-[r1:CONNECTS_SUBSTATIONS {
                connectionType: 'Source',
                commissionDate: datetime() - duration({days: toInteger(rand() * 3286) + 365})
            }]->(source)
            CREATE (tl)-[r2:CONNECTS_SUBSTATIONS {
                connectionType: 'Destination',
                commissionDate: datetime() - duration({days: toInteger(rand() * 3286) + 365})
            }]->(dest)
            RETURN count(r1) + count(r2) as count
            """
            result = session.run(query)
            relationship_counts["CONNECTS_SUBSTATIONS"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "CONNECTS_SUBSTATIONS", "count": relationship_counts["CONNECTS_SUBSTATIONS"]})

            # 3. CONTROLLED_BY_EMS (EnergyDevice → EnergyManagementSystem) - 10,000 devices
            query = """
            MATCH (ed:EnergyDevice)
            MATCH (ems:EnergyManagementSystem)
            WITH ed, ems
            ORDER BY rand()
            LIMIT 10000
            CREATE (ed)-[r:CONTROLLED_BY_EMS {
                controlMode: CASE
                    WHEN ed.energyDeviceType IN ['Generator', 'Transformer', 'CircuitBreaker'] THEN 'Automatic'
                    WHEN ed.energyDeviceType IN ['RTU', 'IED'] THEN 'Supervisory'
                    ELSE 'Monitoring-Only'
                END,
                scanRate: CASE
                    WHEN ed.criticality = 'Critical' THEN 2
                    WHEN ed.criticality = 'High' THEN 5
                    ELSE 10
                END,
                lastCommunication: datetime(),
                communicationProtocol: ed.communicationProtocol[0],
                failsafeMode: CASE
                    WHEN ed.gridImpactLevel = 'Critical' THEN 'IslandMode'
                    ELSE 'LastKnownGood'
                END
            }]->(ems)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["CONTROLLED_BY_EMS"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "CONTROLLED_BY_EMS", "count": relationship_counts["CONTROLLED_BY_EMS"]})

            # 4. CONNECTED_TO_GRID (DER → Substation) - 750 DERs
            query = """
            MATCH (der:DistributedEnergyResource)
            MATCH (sub:Substation)
            WHERE sub.substationType IN ['Distribution', 'Collector']
            WITH der, sub
            ORDER BY rand()
            LIMIT 750
            CREATE (der)-[r:CONNECTED_TO_GRID {
                connectionPoint: 'Substation-' + sub.substationName + '-' + sub.voltageClass + '-Bus',
                interconnectionDate: datetime() - duration({days: toInteger(rand() * 1646) + 180}),
                ieee1547Mode: CASE toInteger(rand() * 3)
                    WHEN 0 THEN 'ConstantPowerFactor'
                    WHEN 1 THEN 'VoltVAR'
                    ELSE 'FreqWatt'
                END,
                exportCapacity: der.capacity
            }]->(sub)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["CONNECTED_TO_GRID"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "CONNECTED_TO_GRID", "count": relationship_counts["CONNECTED_TO_GRID"]})

            # 5. COMPLIES_WITH_NERC_CIP (EnergyDevice/EMS/Substation → NERCCIPStandard) - ~5,000
            query = """
            MATCH (ed:EnergyDevice)
            WHERE ed.nercCIPCategory <> 'Non-BES'
            MATCH (ncs:NERCCIPStandard)
            WHERE any(applicability IN ncs.applicability WHERE applicability = ed.nercCIPCategory)
            WITH ed, ncs
            LIMIT 5000
            CREATE (ed)-[r:COMPLIES_WITH_NERC_CIP {
                complianceStatus: ed.nercCIPCompliance,
                lastAudit: datetime() - duration({days: toInteger(rand() * 336) + 30}),
                nextAudit: datetime() + duration({days: toInteger(rand() * 701) + 30}),
                findingsCount: CASE ed.nercCIPCompliance
                    WHEN 'NonCompliant' THEN toInteger(rand() * 10) + 1
                    ELSE 0
                END,
                remediationDeadline: CASE ed.nercCIPCompliance
                    WHEN 'NonCompliant' THEN datetime() + duration({days: toInteger(rand() * 151) + 30})
                    ELSE null
                END
            }]->(ncs)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["COMPLIES_WITH_NERC_CIP"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "COMPLIES_WITH_NERC_CIP", "count": relationship_counts["COMPLIES_WITH_NERC_CIP"]})

            # 6. HAS_ENERGY_PROPERTY (EnergyDevice → EnergyProperty) - 30,000
            query = """
            MATCH (ed:EnergyDevice)
            MATCH (ep:EnergyProperty)
            WHERE ep.energyPropertyCategory = 'Electrical'
            WITH ed, ep
            ORDER BY rand()
            LIMIT 30000
            CREATE (ed)-[r:HAS_ENERGY_PROPERTY {
                assignedDate: datetime() - duration({days: toInteger(rand() * 1796) + 30}),
                isActive: true,
                monitoringPriority: ep.gridStabilityImpact,
                measurementPoint: CASE ed.energyDeviceType
                    WHEN 'Transformer' THEN 'PrimaryWinding'
                    WHEN 'Generator' THEN 'Stator'
                    ELSE 'Terminal'
                END,
                nercReportingRequired: CASE
                    WHEN ed.nercCIPCategory = 'BES-Cyber-Asset' AND ep.gridStabilityImpact = 'Critical' THEN true
                    ELSE false
                END,
                pmuMeasurement: CASE
                    WHEN ed.energyDeviceType = 'PMU' THEN true
                    ELSE false
                END
            }]->(ep)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["HAS_ENERGY_PROPERTY"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "HAS_ENERGY_PROPERTY", "count": relationship_counts["HAS_ENERGY_PROPERTY"]})

            # 7. EXTENDS_SAREF_DEVICE (EnergyDevice → Wave 1 Device) - 3,000
            query = """
            MATCH (ed:EnergyDevice)
            MATCH (d:Device)
            WHERE d:Device AND NOT d:EnergyDevice AND NOT d:WaterDevice
            WITH ed, d
            ORDER BY rand()
            LIMIT 3000
            CREATE (ed)-[r:EXTENDS_SAREF_DEVICE {
                extensionType: 'Energy-Specific',
                inheritedProperties: ['deviceId', 'manufacturer', 'model', 'firmwareVersion', 'protocol'],
                addedProperties: ['energyDeviceType', 'voltageLevel', 'nercCIPCategory', 'gridImpactLevel'],
                domainSpecialization: 'Energy Grid Infrastructure'
            }]->(d)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["EXTENDS_SAREF_DEVICE"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "EXTENDS_SAREF_DEVICE", "count": relationship_counts["EXTENDS_SAREF_DEVICE"]})

            # 8. DEPENDS_ON_ENERGY (Wave 2 WaterDevice → Energy Substation) - 1,000
            query = """
            MATCH (wd:WaterDevice)
            WHERE wd.waterDeviceType IN ['Pump', 'Chlorinator', 'RTU', 'Valve']
            MATCH (sub:Substation)
            WHERE sub.substationType = 'Distribution'
            WITH wd, sub
            ORDER BY rand()
            LIMIT 1000
            CREATE (wd)-[r:DEPENDS_ON_ENERGY {
                dependencyType: CASE
                    WHEN wd.waterDeviceType = 'Pump' THEN 'PrimaryPower'
                    WHEN wd.waterDeviceType = 'RTU' THEN 'CriticalLoad'
                    ELSE 'BackupPower'
                END,
                powerRequirement: CASE wd.waterDeviceType
                    WHEN 'Pump' THEN wd.flowCapacity * 0.746
                    WHEN 'Chlorinator' THEN 5.0
                    WHEN 'RTU' THEN 0.5
                    ELSE 2.0
                END,
                criticalityLevel: wd.waterQualityImpact,
                failoverCapability: true,
                maxOutageDuration: CASE wd.waterQualityImpact
                    WHEN 'Critical' THEN 5
                    WHEN 'High' THEN 15
                    ELSE 60
                END
            }]->(sub)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["DEPENDS_ON_ENERGY"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "DEPENDS_ON_ENERGY", "count": relationship_counts["DEPENDS_ON_ENERGY"]})

            # 9. THREATENS_GRID_STABILITY (EnergyDevice → CVE) - 3,000
            query = """
            MATCH (ed:EnergyDevice)
            WHERE ed.manufacturer IN ['Siemens Energy', 'ABB', 'GE Grid Solutions', 'Schweitzer Engineering Laboratories']
              AND ed.nercCIPCategory IN ['BES-Cyber-Asset', 'EACMS']
            MATCH (cve:CVE)
            WHERE cve.description =~ '(?i).*(scada|substation|smart meter|ied|rtu|dnp3|iec.*61850).*'
               OR cve.affectedProducts =~ '(?i).*(siemens|abb|ge|sel).*'
            WITH ed, cve
            WHERE rand() < 0.3
            LIMIT 3000
            OPTIONAL MATCH (ed)-[:INSTALLED_AT_SUBSTATION]->(sub:Substation)
            CREATE (ed)-[r:THREATENS_GRID_STABILITY {
                discoveredDate: datetime() - duration({days: toInteger(rand() * 701) + 30}),
                affectedFirmwareVersions: [ed.firmwareVersion],
                patchAvailable: CASE WHEN rand() > 0.3 THEN true ELSE false END,
                patchVersion: CASE WHEN rand() > 0.3 THEN 'V' + toString(toInteger(rand() * 5) + 3) + '.' + toString(toInteger(rand() * 10)) + '.0' ELSE null END,
                exploitabilityScore: 3.9,
                impactScore: CASE cve.baseScore
                    WHEN null THEN 5.0
                    ELSE cve.baseScore * 0.6
                END,
                isExploited: rand() < 0.1,
                mitigationStatus: CASE
                    WHEN rand() > 0.5 THEN 'Unpatched'
                    WHEN rand() > 0.25 THEN 'Mitigated'
                    ELSE 'Patched'
                END,
                gridImpact: CASE ed.gridImpactLevel
                    WHEN 'Critical' THEN 'Blackout'
                    WHEN 'High' THEN 'LoadShedding'
                    ELSE 'VoltageInstability'
                END,
                cascadeRisk: CASE
                    WHEN ed.nercCIPCategory = 'BES-Cyber-Asset' THEN 'High'
                    WHEN ed.voltageLevel CONTAINS 'Transmission' THEN 'Medium'
                    ELSE 'Low'
                END,
                populationImpact: CASE WHEN sub IS NOT NULL THEN sub.populationServed ELSE 0 END,
                icsAdvisory: 'ICSA-' + substring(cve.cveId, 4, 2) + '-' + substring(cve.cveId, 9, 3) + '-01',
                nercAlert: CASE
                    WHEN ed.nercCIPCategory = 'BES-Cyber-Asset' THEN 'NERC-ALERT-' + substring(cve.cveId, 4, 4) + '-' + substring(cve.cveId, 9, 3)
                    ELSE null
                END
            }]->(cve)
            RETURN count(r) as count
            """
            result = session.run(query)
            relationship_counts["THREATENS_GRID_STABILITY"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "THREATENS_GRID_STABILITY", "count": relationship_counts["THREATENS_GRID_STABILITY"]})

        return relationship_counts


if __name__ == "__main__":
    executor = Wave3Executor()
    success = executor.execute()
    sys.exit(0 if success else 1)
