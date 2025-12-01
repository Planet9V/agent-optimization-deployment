#!/usr/bin/env python3
"""Wave 1 Commands, States & Units: 600 SAREF nodes (400 Command + 100 State + 100 UnitOfMeasure)"""
import logging, json
from datetime import datetime
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave1CommandsStatesUnitsExecutor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def create_commands(self) -> int:
        with self.driver.session() as session:
            for batch_num in range(1, 9):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (c:SAREF:Command {{
                  commandId: "saref:cmd:CMD-" + toString({batch_num * 1000} + idx),
                  commandName: CASE idx % 15
                    WHEN 0 THEN "Set Temperature Setpoint"
                    WHEN 1 THEN "Start Motor"
                    WHEN 2 THEN "Stop Motor"
                    WHEN 3 THEN "Open Valve"
                    WHEN 4 THEN "Close Valve"
                    WHEN 5 THEN "Set Flow Rate"
                    WHEN 6 THEN "Adjust Pressure"
                    WHEN 7 THEN "Enable Alarm"
                    WHEN 8 THEN "Disable Alarm"
                    WHEN 9 THEN "Reset Controller"
                    WHEN 10 THEN "Calibrate Sensor"
                    WHEN 11 THEN "Update Firmware"
                    WHEN 12 THEN "Export Logs"
                    WHEN 13 THEN "Change Mode"
                    ELSE "Run Diagnostic"
                  END,

                  commandType: CASE idx % 3
                    WHEN 0 THEN "Configuration"
                    WHEN 1 THEN "Control"
                    ELSE "Diagnostic"
                  END,

                  authorizationRequired: CASE idx % 4
                    WHEN 0 THEN false
                    ELSE true
                  END,

                  auditLogged: CASE idx % 5
                    WHEN 0 THEN false
                    ELSE true
                  END,

                  criticalityLevel: CASE idx % 5
                    WHEN 0 THEN "Critical"
                    WHEN 1 THEN "High"
                    WHEN 2 THEN "High"
                    WHEN 3 THEN "Medium"
                    ELSE "Low"
                  END,

                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE1",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)

            result = session.run("MATCH (c:Command) WHERE c.created_by = 'AEON_INTEGRATION_WAVE1' RETURN count(c) as total")
            total = result.single()['total']
            assert total == 400
            logging.info(f"✅ Command: {total}")
            return total

    def create_states(self) -> int:
        with self.driver.session() as session:
            for batch_num in range(1, 3):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (st:SAREF:State {{
                  stateId: "saref:state:STATE-" + toString({batch_num * 1000} + idx),
                  stateName: CASE idx % 20
                    WHEN 0 THEN "Running"
                    WHEN 1 THEN "Stopped"
                    WHEN 2 THEN "Starting"
                    WHEN 3 THEN "Stopping"
                    WHEN 4 THEN "Idle"
                    WHEN 5 THEN "Standby"
                    WHEN 6 THEN "Active"
                    WHEN 7 THEN "Maintenance"
                    WHEN 8 THEN "Fault"
                    WHEN 9 THEN "Error"
                    WHEN 10 THEN "Warning"
                    WHEN 11 THEN "Calibrating"
                    WHEN 12 THEN "Testing"
                    WHEN 13 THEN "Initializing"
                    WHEN 14 THEN "Shutting Down"
                    WHEN 15 THEN "Emergency Stop"
                    WHEN 16 THEN "Overload"
                    WHEN 17 THEN "Offline"
                    WHEN 18 THEN "Online"
                    ELSE "Degraded"
                  END,

                  stateCategory: CASE idx % 20
                    WHEN 0 THEN "Operational" WHEN 1 THEN "Operational"
                    WHEN 2 THEN "Operational" WHEN 3 THEN "Operational"
                    WHEN 4 THEN "Operational" WHEN 5 THEN "Operational"
                    WHEN 6 THEN "Operational" WHEN 7 THEN "Maintenance"
                    WHEN 8 THEN "Fault" WHEN 9 THEN "Fault"
                    WHEN 10 THEN "Fault" WHEN 11 THEN "Maintenance"
                    WHEN 12 THEN "Operational" WHEN 13 THEN "Operational"
                    WHEN 14 THEN "Operational" WHEN 15 THEN "Fault"
                    WHEN 16 THEN "Fault" WHEN 17 THEN "Fault"
                    WHEN 18 THEN "Operational" ELSE "Fault"
                  END,

                  description: "Operational state " + toString(idx),

                  isNormalState: CASE idx % 20
                    WHEN 0 THEN true WHEN 1 THEN false
                    WHEN 2 THEN true WHEN 3 THEN true
                    WHEN 4 THEN true WHEN 5 THEN true
                    WHEN 6 THEN true WHEN 7 THEN false
                    WHEN 8 THEN false WHEN 9 THEN false
                    WHEN 10 THEN false WHEN 11 THEN false
                    WHEN 12 THEN true WHEN 13 THEN true
                    WHEN 14 THEN true WHEN 15 THEN false
                    WHEN 16 THEN false WHEN 17 THEN false
                    WHEN 18 THEN true ELSE false
                  END,

                  securityImplication: CASE idx % 20
                    WHEN 8 THEN "Elevated" WHEN 9 THEN "Critical"
                    WHEN 10 THEN "Elevated" WHEN 15 THEN "Critical"
                    WHEN 16 THEN "Critical" ELSE "None"
                  END,

                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE1",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)

            result = session.run("MATCH (st:State) WHERE st.created_by = 'AEON_INTEGRATION_WAVE1' RETURN count(st) as total")
            total = result.single()['total']
            assert total == 100
            logging.info(f"✅ State: {total}")
            return total

    def create_units(self) -> int:
        with self.driver.session() as session:
            for batch_num in range(1, 3):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (u:SAREF:UnitOfMeasure {{
                  unitId: "saref:unit:UNIT-" + toString({batch_num * 1000} + idx),
                  symbol: CASE idx % 30
                    WHEN 0 THEN "°C" WHEN 1 THEN "°F" WHEN 2 THEN "K"
                    WHEN 3 THEN "Pa" WHEN 4 THEN "bar" WHEN 5 THEN "psi"
                    WHEN 6 THEN "L/s" WHEN 7 THEN "m³/h" WHEN 8 THEN "GPM"
                    WHEN 9 THEN "m" WHEN 10 THEN "cm" WHEN 11 THEN "mm"
                    WHEN 12 THEN "V" WHEN 13 THEN "kV" WHEN 14 THEN "mV"
                    WHEN 15 THEN "A" WHEN 16 THEN "mA" WHEN 17 THEN "kA"
                    WHEN 18 THEN "W" WHEN 19 THEN "kW" WHEN 20 THEN "MW"
                    WHEN 21 THEN "Hz" WHEN 22 THEN "kHz" WHEN 23 THEN "MHz"
                    WHEN 24 THEN "%" WHEN 25 THEN "RPM"
                    WHEN 26 THEN "N·m" WHEN 27 THEN "pH"
                    WHEN 28 THEN "S" ELSE "dB"
                  END,

                  description: CASE idx % 30
                    WHEN 0 THEN "Degree Celsius" WHEN 1 THEN "Degree Fahrenheit"
                    WHEN 2 THEN "Kelvin" WHEN 3 THEN "Pascal"
                    WHEN 4 THEN "Bar" WHEN 5 THEN "Pounds per square inch"
                    WHEN 6 THEN "Liters per second" WHEN 7 THEN "Cubic meters per hour"
                    WHEN 8 THEN "Gallons per minute" WHEN 9 THEN "Meter"
                    WHEN 10 THEN "Centimeter" WHEN 11 THEN "Millimeter"
                    WHEN 12 THEN "Volt" WHEN 13 THEN "Kilovolt"
                    WHEN 14 THEN "Millivolt" WHEN 15 THEN "Ampere"
                    WHEN 16 THEN "Milliampere" WHEN 17 THEN "Kiloampere"
                    WHEN 18 THEN "Watt" WHEN 19 THEN "Kilowatt"
                    WHEN 20 THEN "Megawatt" WHEN 21 THEN "Hertz"
                    WHEN 22 THEN "Kilohertz" WHEN 23 THEN "Megahertz"
                    WHEN 24 THEN "Percent" WHEN 25 THEN "Revolutions per minute"
                    WHEN 26 THEN "Newton meter" WHEN 27 THEN "pH unit"
                    WHEN 28 THEN "Siemens" ELSE "Decibel"
                  END,

                  quantityKind: CASE idx % 30
                    WHEN 0 THEN "Temperature" WHEN 1 THEN "Temperature" WHEN 2 THEN "Temperature"
                    WHEN 3 THEN "Pressure" WHEN 4 THEN "Pressure" WHEN 5 THEN "Pressure"
                    WHEN 6 THEN "FlowRate" WHEN 7 THEN "FlowRate" WHEN 8 THEN "FlowRate"
                    WHEN 9 THEN "Length" WHEN 10 THEN "Length" WHEN 11 THEN "Length"
                    WHEN 12 THEN "Voltage" WHEN 13 THEN "Voltage" WHEN 14 THEN "Voltage"
                    WHEN 15 THEN "Current" WHEN 16 THEN "Current" WHEN 17 THEN "Current"
                    WHEN 18 THEN "Power" WHEN 19 THEN "Power" WHEN 20 THEN "Power"
                    WHEN 21 THEN "Frequency" WHEN 22 THEN "Frequency" WHEN 23 THEN "Frequency"
                    WHEN 24 THEN "Percentage" WHEN 25 THEN "RotationalSpeed"
                    WHEN 26 THEN "Torque" WHEN 27 THEN "pH"
                    WHEN 28 THEN "Conductivity" ELSE "Sound"
                  END,

                  conversionFactor: toFloat(1.0 + (idx % 10) / 10.0),
                  conversionOffset: toFloat((idx % 20) - 10.0),

                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE1",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)

            result = session.run("MATCH (u:UnitOfMeasure) WHERE u.created_by = 'AEON_INTEGRATION_WAVE1' RETURN count(u) as total")
            total = result.single()['total']
            assert total == 100
            logging.info(f"✅ UnitOfMeasure: {total}")
            return total

    def execute(self):
        try:
            start = datetime.utcnow()
            logging.info("🎯 Wave 1 Commands, States & Units Started")

            command_count = self.create_commands()
            state_count = self.create_states()
            unit_count = self.create_units()

            total = command_count + state_count + unit_count
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
    Wave1CommandsStatesUnitsExecutor().execute()
