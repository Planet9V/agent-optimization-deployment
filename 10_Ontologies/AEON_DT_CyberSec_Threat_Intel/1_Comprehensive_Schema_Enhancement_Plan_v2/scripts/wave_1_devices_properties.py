#!/usr/bin/env python3
"""Wave 1 Devices & Properties: 2,000 SAREF core foundation nodes (800 Device + 1,200 Property)"""
import logging, json
from datetime import datetime
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave1DevicesPropertiesExecutor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def create_devices(self) -> int:
        with self.driver.session() as session:
            for batch_num in range(1, 17):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (d:SAREF:Device {{
                  deviceId: "saref:device:DEV-" + toString({batch_num * 1000} + idx),
                  name: CASE idx % 12
                    WHEN 0 THEN "Siemens S7-1500 PLC " + toString(idx)
                    WHEN 1 THEN "Rockwell ControlLogix PLC " + toString(idx)
                    WHEN 2 THEN "Schneider Electric M580 PLC " + toString(idx)
                    WHEN 3 THEN "Allen-Bradley CompactLogix " + toString(idx)
                    WHEN 4 THEN "ABB 800xA Controller " + toString(idx)
                    WHEN 5 THEN "Honeywell HC900 Controller " + toString(idx)
                    WHEN 6 THEN "Emerson DeltaV Controller " + toString(idx)
                    WHEN 7 THEN "Yokogawa CENTUM VP Controller " + toString(idx)
                    WHEN 8 THEN "GE MarkVIe Controller " + toString(idx)
                    WHEN 9 THEN "Mitsubishi MELSEC-Q PLC " + toString(idx)
                    WHEN 10 THEN "Omron CJ2M PLC " + toString(idx)
                    ELSE "Phoenix Contact PLCnext " + toString(idx)
                  END,

                  model: "MODEL-" + toString({batch_num * 100} + idx),
                  manufacturer: CASE idx % 12
                    WHEN 0 THEN "Siemens AG" WHEN 1 THEN "Rockwell Automation"
                    WHEN 2 THEN "Schneider Electric" WHEN 3 THEN "Allen-Bradley"
                    WHEN 4 THEN "ABB" WHEN 5 THEN "Honeywell"
                    WHEN 6 THEN "Emerson" WHEN 7 THEN "Yokogawa"
                    WHEN 8 THEN "GE" WHEN 9 THEN "Mitsubishi"
                    WHEN 10 THEN "Omron" ELSE "Phoenix Contact"
                  END,

                  firmwareVersion: "V" + toString(2 + idx % 3) + "." + toString(idx % 10) + "." + toString(idx % 5),
                  serialNumber: "SN-" + toString(2025000 + {batch_num * 100} + idx),

                  deviceCategory: CASE idx % 4
                    WHEN 0 THEN "Controller" WHEN 1 THEN "Sensor"
                    WHEN 2 THEN "Actuator" ELSE "Gateway"
                  END,

                  deploymentLocation: CASE idx % 10
                    WHEN 0 THEN "Building 1, Floor 1, Zone A"
                    WHEN 1 THEN "Building 1, Floor 2, Zone B"
                    WHEN 2 THEN "Building 2, Floor 1, Zone C"
                    WHEN 3 THEN "Building 3, Floor 1, Control Room"
                    WHEN 4 THEN "Building 3, Floor 2, Server Room"
                    WHEN 5 THEN "Building 4, Production Floor"
                    WHEN 6 THEN "Building 5, Warehouse"
                    WHEN 7 THEN "Building 6, R&D Lab"
                    WHEN 8 THEN "Outdoor, Tank Farm"
                    ELSE "Outdoor, Pump Station"
                  END,

                  operationalStatus: CASE idx % 6
                    WHEN 0 THEN "Active" WHEN 1 THEN "Active"
                    WHEN 2 THEN "Active" WHEN 3 THEN "Standby"
                    WHEN 4 THEN "Maintenance" ELSE "Fault"
                  END,

                  ipAddress: "192.168." + toString(1 + idx % 10) + "." + toString(10 + idx % 240),
                  macAddress: "00:" + toString(10 + idx % 10) + ":" + toString(20 + idx % 10) + ":"
                    + toString(30 + idx % 10) + ":" + toString(40 + idx % 10) + ":" + toString(50 + idx % 10),

                  criticality: CASE idx % 5
                    WHEN 0 THEN "Critical" WHEN 1 THEN "Critical"
                    WHEN 2 THEN "High" WHEN 3 THEN "Medium" ELSE "Low"
                  END,

                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE1",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)

            result = session.run("MATCH (d:Device) WHERE d.created_by = 'AEON_INTEGRATION_WAVE1' RETURN count(d) as total")
            total = result.single()['total']
            assert total == 800
            logging.info(f"✅ Device: {total}")
            return total

    def create_properties(self) -> int:
        with self.driver.session() as session:
            for batch_num in range(1, 25):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (p:SAREF:Property {{
                  propertyId: "saref:property:PROP-" + toString({batch_num * 1000} + idx),

                  propertyType: CASE idx % 20
                    WHEN 0 THEN "Temperature" WHEN 1 THEN "Pressure"
                    WHEN 2 THEN "FlowRate" WHEN 3 THEN "Level"
                    WHEN 4 THEN "Voltage" WHEN 5 THEN "Current"
                    WHEN 6 THEN "Power" WHEN 7 THEN "Frequency"
                    WHEN 8 THEN "Humidity" WHEN 9 THEN "Vibration"
                    WHEN 10 THEN "Speed" WHEN 11 THEN "Position"
                    WHEN 12 THEN "Torque" WHEN 13 THEN "pH"
                    WHEN 14 THEN "Conductivity" WHEN 15 THEN "Turbidity"
                    WHEN 16 THEN "OxygenLevel" WHEN 17 THEN "COLevel"
                    WHEN 18 THEN "SmokeLevel" ELSE "NoiseLevel"
                  END,

                  unitOfMeasure: CASE idx % 20
                    WHEN 0 THEN "Celsius" WHEN 1 THEN "Pascal"
                    WHEN 2 THEN "LitersPerSecond" WHEN 3 THEN "Meters"
                    WHEN 4 THEN "Volt" WHEN 5 THEN "Ampere"
                    WHEN 6 THEN "Watt" WHEN 7 THEN "Hertz"
                    WHEN 8 THEN "Percent" WHEN 9 THEN "MillimetersPerSecond"
                    WHEN 10 THEN "RPM" WHEN 11 THEN "Millimeters"
                    WHEN 12 THEN "NewtonMeters" WHEN 13 THEN "pH"
                    WHEN 14 THEN "Siemens" WHEN 15 THEN "NTU"
                    WHEN 16 THEN "ppm" WHEN 17 THEN "ppm"
                    WHEN 18 THEN "Percent" ELSE "Decibel"
                  END,

                  minValue: toFloat(-50.0 + idx % 100),
                  maxValue: toFloat(50.0 + idx * 2),
                  normalRangeMin: toFloat(10.0 + idx % 30),
                  normalRangeMax: toFloat(40.0 + idx % 50),
                  criticalThresholdMin: toFloat(0.0 + idx % 15),
                  criticalThresholdMax: toFloat(60.0 + idx % 40),
                  measurementAccuracy: toFloat(0.1 + (idx % 50) / 100.0),

                  description: "Property monitoring for device " + toString({batch_num * 100} + idx),

                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE1",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)

            result = session.run("MATCH (p:Property) WHERE p.created_by = 'AEON_INTEGRATION_WAVE1' RETURN count(p) as total")
            total = result.single()['total']
            assert total == 1200
            logging.info(f"✅ Property: {total}")
            return total

    def execute(self):
        try:
            start = datetime.utcnow()
            logging.info("🎯 Wave 1 Devices & Properties Started")

            device_count = self.create_devices()
            property_count = self.create_properties()

            total = device_count + property_count
            duration = (datetime.utcnow() - start).total_seconds()

            logging.info("=" * 80)
            logging.info(f"✅ Total: {total} | Time: {duration:.2f}s | Rate: {total/duration:.2f} nodes/s")
            logging.info("=" * 80)
        except Exception as e:
            logging.error(f"Failed: {e}")
            raise
        finally:
            self.driver.close()

if __name__ == "__main__":
    Wave1DevicesPropertiesExecutor().execute()
