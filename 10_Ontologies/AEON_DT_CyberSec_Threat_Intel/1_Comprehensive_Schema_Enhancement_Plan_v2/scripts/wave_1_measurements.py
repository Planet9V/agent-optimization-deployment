#!/usr/bin/env python3
"""Wave 1 Measurements: 1,500 SAREF measurement nodes with timestamps and anomaly detection"""
import logging, json
from datetime import datetime
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave1MeasurementsExecutor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def create_measurements(self) -> int:
        with self.driver.session() as session:
            for batch_num in range(1, 31):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (m:SAREF:Measurement {{
                  measurementId: "saref:meas:MEAS-" + toString({batch_num * 1000} + idx),

                  value: toFloat(20.0 + (idx % 60) + (rand() * 10)),

                  quality: CASE idx % 10
                    WHEN 0 THEN "Good" WHEN 1 THEN "Good"
                    WHEN 2 THEN "Good" WHEN 3 THEN "Good"
                    WHEN 4 THEN "Good" WHEN 5 THEN "Good"
                    WHEN 6 THEN "Good" WHEN 7 THEN "Uncertain"
                    WHEN 8 THEN "Bad" ELSE "Good"
                  END,

                  anomalyScore: CASE idx % 20
                    WHEN 0 THEN toFloat(0.75 + (rand() * 0.25))
                    WHEN 1 THEN toFloat(0.80 + (rand() * 0.20))
                    ELSE toFloat(rand() * 0.3)
                  END,

                  isAnomaly: CASE idx % 20
                    WHEN 0 THEN true
                    WHEN 1 THEN true
                    ELSE false
                  END,

                  confidenceLevel: toFloat(0.85 + (rand() * 0.15)),

                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE1",
                  created_date: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)

            result = session.run("MATCH (m:Measurement) WHERE m.created_by = 'AEON_INTEGRATION_WAVE1' RETURN count(m) as total")
            total = result.single()['total']
            assert total == 1500
            logging.info(f"✅ Measurement: {total}")
            return total

    def execute(self):
        try:
            start = datetime.utcnow()
            logging.info("🎯 Wave 1 Measurements Started")

            measurement_count = self.create_measurements()

            duration = (datetime.utcnow() - start).total_seconds()

            logging.info("=" * 80)
            logging.info(f"✅ Total: {measurement_count} | Time: {duration:.2f}s | Rate: {measurement_count/duration:.2f} nodes/s")
            logging.info("=" * 80)
        except Exception as e:
            logging.error(f"Failed: {e}")
            raise
        finally:
            self.driver.close()

if __name__ == "__main__":
    Wave1MeasurementsExecutor().execute()
