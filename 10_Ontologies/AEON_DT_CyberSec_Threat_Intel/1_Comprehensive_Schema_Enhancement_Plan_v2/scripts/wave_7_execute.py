#!/usr/bin/env python3
"""
Wave 7: Psychometric Analysis and Behavioral Assessment Integration
Human factors in cybersecurity: psychological profiles, insider threats, social engineering
"""

import logging
import json
from datetime import datetime
from typing import Dict
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave7Executor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.log_file = "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/logs/wave_7_execution.jsonl"

    def log_operation(self, operation: str, details: dict):
        log_entry = {"timestamp": datetime.utcnow().isoformat(), "operation": operation, "details": details}
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        logging.info(f"{operation}: {details}")

    def execute(self):
        try:
            self.log_operation("wave_7_execution_started", {"timestamp": datetime.utcnow().isoformat()})

            self.log_operation("phase_started", {"phase": "constraints_and_indexes"})
            self.create_constraints_and_indexes()
            self.log_operation("phase_completed", {"phase": "constraints_and_indexes"})

            self.log_operation("phase_started", {"phase": "create_psychometric_nodes"})
            personality = self.create_personality_traits()
            cognitive = self.create_cognitive_biases()
            motivations = self.create_motivation_factors()
            insider = self.create_insider_threat_indicators()
            social_eng = self.create_social_engineering_tactics()
            behavioral = self.create_behavioral_patterns()

            total_nodes = personality + cognitive + motivations + insider + social_eng + behavioral
            self.log_operation("phase_completed", {"phase": "create_psychometric_nodes", "nodes_created": total_nodes})

            self.log_operation("phase_started", {"phase": "create_relationships"})
            relationship_counts = self.create_relationships()
            total_rels = sum(relationship_counts.values())
            self.log_operation("phase_completed", {"phase": "create_relationships", "total_relationships": total_rels})

            self.log_operation("wave_7_execution_completed", {
                "timestamp": datetime.utcnow().isoformat(),
                "nodes_created": total_nodes,
                "relationships_created": total_rels
            })

            logging.info(f"Wave 7 completed successfully: {total_nodes} nodes, {total_rels} relationships")

        except Exception as e:
            self.log_operation("wave_7_execution_error", {"error": str(e)})
            logging.error(f"Wave 7 execution failed: {e}")
            raise
        finally:
            self.driver.close()

    def create_constraints_and_indexes(self):
        constraints_and_indexes = [
            "CREATE CONSTRAINT personality_trait_id_unique IF NOT EXISTS FOR (p:Personality_Trait) REQUIRE p.trait_id IS UNIQUE",
            "CREATE CONSTRAINT cognitive_bias_id_unique IF NOT EXISTS FOR (c:Cognitive_Bias) REQUIRE c.bias_id IS UNIQUE",
            "CREATE CONSTRAINT motivation_factor_id_unique IF NOT EXISTS FOR (m:Motivation_Factor) REQUIRE m.motivation_id IS UNIQUE",
            "CREATE CONSTRAINT insider_threat_indicator_id_unique IF NOT EXISTS FOR (i:Insider_Threat_Indicator) REQUIRE i.indicator_id IS UNIQUE",
            "CREATE CONSTRAINT social_engineering_tactic_id_unique IF NOT EXISTS FOR (s:Social_Engineering_Tactic) REQUIRE s.tactic_id IS UNIQUE",
            "CREATE CONSTRAINT behavioral_pattern_id_unique IF NOT EXISTS FOR (b:Behavioral_Pattern) REQUIRE b.pattern_id IS UNIQUE",
            "CREATE INDEX personality_trait_category_idx IF NOT EXISTS FOR (p:Personality_Trait) ON (p.trait_category)",
            "CREATE INDEX cognitive_bias_impact_idx IF NOT EXISTS FOR (c:Cognitive_Bias) ON (c.security_impact)",
            "CREATE INDEX insider_threat_severity_idx IF NOT EXISTS FOR (i:Insider_Threat_Indicator) ON (i.severity)",
            "CREATE INDEX social_engineering_success_idx IF NOT EXISTS FOR (s:Social_Engineering_Tactic) ON (s.avg_success_rate)"
        ]

        with self.driver.session() as session:
            for statement in constraints_and_indexes:
                session.run(statement)
                self.log_operation("constraint_or_index_created", {"statement": statement[:80] + "..."})

    def create_personality_traits(self) -> int:
        """Create Big Five (OCEAN) and Dark Triad traits"""
        query = """
        UNWIND [
          {id: "OCEAN-O", name: "Openness to Experience", category: "Big Five", desc: "Creativity, curiosity, intellectual engagement"},
          {id: "OCEAN-C", name: "Conscientiousness", category: "Big Five", desc: "Organization, responsibility, dependability"},
          {id: "OCEAN-E", name: "Extraversion", category: "Big Five", desc: "Social engagement, assertiveness, energy"},
          {id: "OCEAN-A", name: "Agreeableness", category: "Big Five", desc: "Cooperation, compassion, trust"},
          {id: "OCEAN-N", name: "Neuroticism", category: "Big Five", desc: "Emotional instability, anxiety, moodiness"},
          {id: "DARK-MACH", name: "Machiavellianism", category: "Dark Triad", desc: "Manipulation, strategic deception, self-interest"},
          {id: "DARK-NARC", name: "Narcissism", category: "Dark Triad", desc: "Grandiosity, entitlement, need for admiration"},
          {id: "DARK-PSYCH", name: "Psychopathy", category: "Dark Triad", desc: "Lack of empathy, impulsivity, antisocial behavior"}
        ] AS trait
        CREATE (p:Personality_Trait {
          trait_id: trait.id,
          trait_name: trait.name,
          trait_category: trait.category,
          description: trait.desc,
          model_version: "1.0",
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE7",
          created_date: datetime(),
          last_updated: datetime(),
          validation_status: "VALIDATED"
        })
        RETURN count(p) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("personality_traits_created", {"count": count})
            return count

    def create_cognitive_biases(self) -> int:
        """Create security-relevant cognitive biases"""
        query = """
        UNWIND [
          {id: "BIAS-CONFIRM", name: "Confirmation Bias", impact: "HIGH", desc: "Favoring information that confirms preconceptions"},
          {id: "BIAS-AUTHORITY", name: "Authority Bias", impact: "HIGH", desc: "Over-reliance on authority figures"},
          {id: "BIAS-URGENCY", name: "Urgency Bias", impact: "HIGH", desc: "Rushed decisions under time pressure"},
          {id: "BIAS-ANCHORING", name: "Anchoring Bias", impact: "MEDIUM", desc: "Over-reliance on first information received"},
          {id: "BIAS-RECENCY", name: "Recency Bias", impact: "MEDIUM", desc: "Over-weighting recent events"},
          {id: "BIAS-SOCIAL-PROOF", name: "Social Proof Bias", impact: "HIGH", desc: "Following group behavior"},
          {id: "BIAS-OPTIMISM", name: "Optimism Bias", impact: "MEDIUM", desc: "Underestimating risk probability"}
        ] AS bias
        CREATE (c:Cognitive_Bias {
          bias_id: bias.id,
          bias_name: bias.name,
          security_impact: bias.impact,
          description: bias.desc,
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE7",
          created_date: datetime(),
          last_updated: datetime(),
          validation_status: "VALIDATED"
        })
        RETURN count(c) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("cognitive_biases_created", {"count": count})
            return count

    def create_motivation_factors(self) -> int:
        """Create MICE motivation framework"""
        query = """
        UNWIND [
          {id: "MICE-MONEY", name: "Money", category: "Financial", desc: "Financial gain, debt, greed"},
          {id: "MICE-IDEOLOGY", name: "Ideology", category: "Belief", desc: "Political, religious, or social beliefs"},
          {id: "MICE-COMPROMISE", name: "Compromise", category: "Coercion", desc: "Blackmail, extortion, leverage"},
          {id: "MICE-EGO", name: "Ego", category: "Recognition", desc: "Recognition, revenge, status"}
        ] AS motiv
        CREATE (m:Motivation_Factor {
          motivation_id: motiv.id,
          motivation_name: motiv.name,
          motivation_category: motiv.category,
          description: motiv.desc,
          framework: "MICE",
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE7",
          created_date: datetime(),
          last_updated: datetime(),
          validation_status: "VALIDATED"
        })
        RETURN count(m) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("motivation_factors_created", {"count": count})
            return count

    def create_insider_threat_indicators(self) -> int:
        """Create CERT Insider Threat indicators"""
        query = """
        UNWIND [
          {id: "INSIDER-TECH-01", name: "Unauthorized Data Access", type: "Technical", severity: "HIGH"},
          {id: "INSIDER-TECH-02", name: "After-Hours System Access", type: "Technical", severity: "MEDIUM"},
          {id: "INSIDER-TECH-03", name: "Large Data Downloads", type: "Technical", severity: "HIGH"},
          {id: "INSIDER-TECH-04", name: "USB Device Usage", type: "Technical", severity: "MEDIUM"},
          {id: "INSIDER-TECH-05", name: "Password Sharing", type: "Technical", severity: "HIGH"},
          {id: "INSIDER-BEHAV-01", name: "Workplace Conflicts", type: "Behavioral", severity: "MEDIUM"},
          {id: "INSIDER-BEHAV-02", name: "Resignation Planning", type: "Behavioral", severity: "HIGH"},
          {id: "INSIDER-BEHAV-03", name: "Financial Stress", type: "Behavioral", severity: "MEDIUM"},
          {id: "INSIDER-BEHAV-04", name: "Policy Violations", type: "Behavioral", severity: "HIGH"},
          {id: "INSIDER-ORG-01", name: "Access Privilege Changes", type: "Organizational", severity: "MEDIUM"},
          {id: "INSIDER-ORG-02", name: "Supervisor Concerns", type: "Organizational", severity: "MEDIUM"}
        ] AS indicator
        CREATE (i:Insider_Threat_Indicator {
          indicator_id: indicator.id,
          indicator_name: indicator.name,
          indicator_type: indicator.type,
          severity: indicator.severity,
          framework: "CERT",
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE7",
          created_date: datetime(),
          last_updated: datetime(),
          validation_status: "VALIDATED"
        })
        RETURN count(i) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("insider_threat_indicators_created", {"count": count})
            return count

    def create_social_engineering_tactics(self) -> int:
        """Create social engineering tactics"""
        query = """
        UNWIND [
          {id: "SE-PRETEXTING", name: "Pretexting", desc: "Creating fabricated scenario", success: 65.0},
          {id: "SE-PHISHING", name: "Phishing", desc: "Fraudulent email/message", success: 32.0},
          {id: "SE-BAITING", name: "Baiting", desc: "Offering something enticing", success: 45.0},
          {id: "SE-QUID-PRO-QUO", name: "Quid Pro Quo", desc: "Offering service for info", success: 28.0},
          {id: "SE-TAILGATING", name: "Tailgating", desc: "Physical access following", success: 55.0},
          {id: "SE-AUTHORITY", name: "Authority Exploitation", desc: "Impersonating authority", success: 70.0},
          {id: "SE-URGENCY", name: "Urgency Creation", desc: "Time pressure manipulation", success: 58.0}
        ] AS tactic
        CREATE (s:Social_Engineering_Tactic {
          tactic_id: tactic.id,
          tactic_name: tactic.name,
          description: tactic.desc,
          avg_success_rate: tactic.success,
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE7",
          created_date: datetime(),
          last_updated: datetime(),
          validation_status: "VALIDATED"
        })
        RETURN count(s) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("social_engineering_tactics_created", {"count": count})
            return count

    def create_behavioral_patterns(self) -> int:
        """Create behavioral attack patterns"""
        query = """
        UNWIND range(1, 20) AS pattern_num
        CREATE (b:Behavioral_Pattern {
          pattern_id: "BEHAV-PATTERN-" + toString(pattern_num),
          pattern_name: "Behavioral Pattern " + toString(pattern_num),
          pattern_type: CASE
            WHEN pattern_num % 4 = 0 THEN "Insider Threat"
            WHEN pattern_num % 4 = 1 THEN "Social Engineering"
            WHEN pattern_num % 4 = 2 THEN "Privilege Abuse"
            ELSE "Data Exfiltration"
          END,
          risk_score: toFloat(pattern_num * 5) / 100.0,
          node_id: randomUUID(),
          created_by: "AEON_INTEGRATION_WAVE7",
          created_date: datetime(),
          last_updated: datetime()
        })
        RETURN count(b) as count
        """

        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()["count"]
            self.log_operation("behavioral_patterns_created", {"count": count})
            return count

    def create_relationships(self) -> Dict[str, int]:
        """Create relationships for Wave 7"""
        relationship_counts = {}

        with self.driver.session() as session:
            # 1. Link personality traits to behavioral patterns
            query1 = """
            MATCH (trait:Personality_Trait), (pattern:Behavioral_Pattern)
            WHERE (trait.trait_category = "Dark Triad" AND pattern.pattern_type = "Insider Threat") OR
                  (trait.trait_id = "OCEAN-N" AND pattern.risk_score > 0.5)
            CREATE (trait)-[r:INFLUENCES_BEHAVIOR {
              relationship_id: randomUUID(),
              influence_strength: "MODERATE",
              created_date: datetime()
            }]->(pattern)
            RETURN count(r) as count
            """
            result = session.run(query1)
            relationship_counts["INFLUENCES_BEHAVIOR"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "INFLUENCES_BEHAVIOR", "count": relationship_counts["INFLUENCES_BEHAVIOR"]})

            # 2. Link cognitive biases to social engineering tactics
            query2 = """
            MATCH (bias:Cognitive_Bias), (tactic:Social_Engineering_Tactic)
            WHERE (bias.bias_id = "BIAS-AUTHORITY" AND tactic.tactic_id = "SE-AUTHORITY") OR
                  (bias.bias_id = "BIAS-URGENCY" AND tactic.tactic_id = "SE-URGENCY") OR
                  (bias.bias_id = "BIAS-SOCIAL-PROOF" AND tactic.tactic_name CONTAINS "Phishing")
            CREATE (bias)-[r:EXPLOITED_BY {
              relationship_id: randomUUID(),
              exploitation_effectiveness: "HIGH",
              created_date: datetime()
            }]->(tactic)
            RETURN count(r) as count
            """
            result = session.run(query2)
            relationship_counts["EXPLOITED_BY"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "EXPLOITED_BY", "count": relationship_counts["EXPLOITED_BY"]})

            # 3. Link motivation factors to insider threat indicators
            query3 = """
            MATCH (motiv:Motivation_Factor), (indicator:Insider_Threat_Indicator)
            WHERE (motiv.motivation_id = "MICE-MONEY" AND indicator.indicator_id = "INSIDER-BEHAV-03") OR
                  (motiv.motivation_id = "MICE-EGO" AND indicator.indicator_id = "INSIDER-BEHAV-01") OR
                  (motiv.motivation_id = "MICE-COMPROMISE" AND indicator.severity = "HIGH")
            CREATE (motiv)-[r:MOTIVATES {
              relationship_id: randomUUID(),
              motivation_strength: "STRONG",
              created_date: datetime()
            }]->(indicator)
            RETURN count(r) as count
            """
            result = session.run(query3)
            relationship_counts["MOTIVATES"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "MOTIVATES", "count": relationship_counts["MOTIVATES"]})

            # 4. Link social engineering tactics to ICS techniques
            query4 = """
            MATCH (se:Social_Engineering_Tactic), (tech:ICS_Technique)
            WHERE tech.technique_id IN ["T0812", "T0818", "T0865", "T0817"] AND
                  se.tactic_id IN ["SE-PHISHING", "SE-PRETEXTING", "SE-AUTHORITY"]
            CREATE (se)-[r:ENABLES_TECHNIQUE {
              relationship_id: randomUUID(),
              enablement_mechanism: "Social Engineering",
              created_date: datetime()
            }]->(tech)
            RETURN count(r) as count
            """
            result = session.run(query4)
            relationship_counts["ENABLES_TECHNIQUE"] = result.single()["count"]
            self.log_operation("relationships_created", {"type": "ENABLES_TECHNIQUE", "count": relationship_counts["ENABLES_TECHNIQUE"]})

        return relationship_counts

if __name__ == "__main__":
    executor = Wave7Executor()
    executor.execute()
