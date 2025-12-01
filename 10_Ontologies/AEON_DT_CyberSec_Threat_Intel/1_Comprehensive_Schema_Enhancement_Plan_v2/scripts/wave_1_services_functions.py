#!/usr/bin/env python3
"""Wave 1 Services & Functions: 900 SAREF nodes (600 Service + 300 Function)"""
import logging, json
from datetime import datetime
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave1ServicesFunctionsExecutor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def create_services(self) -> int:
        with self.driver.session() as session:
            for batch_num in range(1, 13):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (s:SAREF:Service {{
                  serviceId: "saref:service:SVC-" + toString({batch_num * 1000} + idx),
                  serviceName: CASE idx % 10
                    WHEN 0 THEN "Modbus Register Read"
                    WHEN 1 THEN "Modbus Register Write"
                    WHEN 2 THEN "OPC-UA Data Access"
                    WHEN 3 THEN "Profinet IO"
                    WHEN 4 THEN "EtherNet/IP CIP"
                    WHEN 5 THEN "BACnet Services"
                    WHEN 6 THEN "DNP3 Data Transfer"
                    WHEN 7 THEN "IEC 61850 GOOSE"
                    WHEN 8 THEN "MQTT Publish/Subscribe"
                    ELSE "HTTP REST API"
                  END,

                  serviceType: CASE idx % 3
                    WHEN 0 THEN "DataCollection"
                    WHEN 1 THEN "Control"
                    ELSE "Diagnostic"
                  END,

                  protocol: CASE idx % 10
                    WHEN 0 THEN "Modbus/TCP" WHEN 1 THEN "Modbus/TCP"
                    WHEN 2 THEN "OPC-UA" WHEN 3 THEN "Profinet"
                    WHEN 4 THEN "EtherNet/IP" WHEN 5 THEN "BACnet"
                    WHEN 6 THEN "DNP3" WHEN 7 THEN "IEC 61850"
                    WHEN 8 THEN "MQTT" ELSE "HTTP"
                  END,

                  port: CASE idx % 10
                    WHEN 0 THEN 502 WHEN 1 THEN 502
                    WHEN 2 THEN 4840 WHEN 3 THEN 34964
                    WHEN 4 THEN 2222 WHEN 5 THEN 47808
                    WHEN 6 THEN 20000 WHEN 7 THEN 102
                    WHEN 8 THEN 1883 ELSE 80
                  END,

                  authenticationRequired: CASE idx % 5
                    WHEN 0 THEN false
                    WHEN 1 THEN false
                    ELSE true
                  END,

                  encryptionEnabled: CASE idx % 4
                    WHEN 0 THEN false
                    ELSE true
                  END,

                  accessLevel: CASE idx % 3
                    WHEN 0 THEN "Read"
                    WHEN 1 THEN "Write"
                    ELSE "Admin"
                  END,

                  description: "Service for device " + toString({batch_num * 100} + idx),

                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE1",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)

            result = session.run("MATCH (s:Service) WHERE s.created_by = 'AEON_INTEGRATION_WAVE1' RETURN count(s) as total")
            total = result.single()['total']
            assert total == 600
            logging.info(f"✅ Service: {total}")
            return total

    def create_functions(self) -> int:
        with self.driver.session() as session:
            for batch_num in range(1, 7):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (f:SAREF:Function {{
                  functionId: "saref:func:FUNC-" + toString({batch_num * 1000} + idx),

                  functionType: CASE idx % 8
                    WHEN 0 THEN "SensingFunction"
                    WHEN 1 THEN "ActuatingFunction"
                    WHEN 2 THEN "MeteringFunction"
                    WHEN 3 THEN "EventFunction"
                    WHEN 4 THEN "ControlFunction"
                    WHEN 5 THEN "MonitoringFunction"
                    WHEN 6 THEN "DiagnosticFunction"
                    ELSE "ConfigurationFunction"
                  END,

                  description: "Function capability for device " + toString({batch_num * 100} + idx),

                  executionFrequency: CASE idx % 3
                    WHEN 0 THEN "Continuous"
                    WHEN 1 THEN "Periodic"
                    ELSE "OnDemand"
                  END,

                  periodicInterval: CASE idx % 3
                    WHEN 1 THEN toInteger(30 + idx * 10)
                    ELSE null
                  END,

                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE1",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)

            result = session.run("MATCH (f:Function) WHERE f.created_by = 'AEON_INTEGRATION_WAVE1' RETURN count(f) as total")
            total = result.single()['total']
            assert total == 300
            logging.info(f"✅ Function: {total}")
            return total

    def execute(self):
        try:
            start = datetime.utcnow()
            logging.info("🎯 Wave 1 Services & Functions Started")

            service_count = self.create_services()
            function_count = self.create_functions()

            total = service_count + function_count
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
    Wave1ServicesFunctionsExecutor().execute()
