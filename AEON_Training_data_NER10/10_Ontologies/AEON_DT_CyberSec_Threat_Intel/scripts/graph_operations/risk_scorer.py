#!/usr/bin/env python3
"""
Risk Scorer - Multi-factor risk scoring and prioritization
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RiskScore:
    """Comprehensive risk score for a vulnerability or asset"""
    entity_id: str
    entity_type: str
    total_score: float
    cvss_score: float
    cvss_weight: float = 0.40
    asset_criticality: float = 0.0
    criticality_weight: float = 0.25
    exploit_availability: float = 0.0
    exploit_weight: float = 0.20
    threat_intel: float = 0.0
    threat_weight: float = 0.10
    network_exposure: float = 0.0
    exposure_weight: float = 0.05
    classification: str = ""  # Now/Next/Never
    justification: str = ""
    trending: str = "stable"  # up/down/stable


class RiskScorer:
    """Calculate and prioritize risk scores using multiple factors"""

    # Classification thresholds
    NOW_THRESHOLD = 75.0
    NEXT_THRESHOLD = 50.0

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.historical_scores = {}  # For trend analysis

    def close(self):
        self.driver.close()

    def calculate_vulnerability_risk(self, cve_id: str) -> RiskScore:
        """Calculate comprehensive risk score for a CVE"""
        query = '''
        MATCH (vuln:Vulnerability {id: $cve_id})
        OPTIONAL MATCH (vuln)-[:AFFECTS]->(component:Component)
        OPTIONAL MATCH (vuln)-[:HAS_EXPLOIT]->(exploit:Exploit)
        OPTIONAL MATCH (vuln)<-[:MENTIONS]-(threat:ThreatIntel)
        OPTIONAL MATCH (component)-[:EXPOSED_TO]->(interface:NetworkInterface)
        WITH vuln,
             COLLECT(DISTINCT component) as components,
             COLLECT(DISTINCT exploit) as exploits,
             COLLECT(DISTINCT threat) as threats,
             COUNT(DISTINCT interface) as exposure_count
        RETURN
            vuln.id as id,
            vuln.cvss_score as cvss,
            components,
            exploits,
            threats,
            exposure_count,
            vuln.published_date as published,
            vuln.last_modified as modified
        '''

        with self.driver.session() as session:
            result = session.run(query, cve_id=cve_id)
            record = result.single()

            if not record:
                logger.warning(f"CVE {cve_id} not found")
                return None

            # Factor 1: CVSS Score (40%)
            cvss_score = float(record["cvss"] or 0.0)
            cvss_normalized = (cvss_score / 10.0) * 100

            # Factor 2: Asset Criticality (25%)
            components = record["components"]
            criticality_map = {"critical": 100, "high": 75, "medium": 50, "low": 25, "info": 0}
            if components:
                max_criticality = max(
                    criticality_map.get(c.get("criticality", "medium"), 50)
                    for c in components
                )
            else:
                max_criticality = 0

            # Factor 3: Exploit Availability (20%)
            exploits = record["exploits"]
            if exploits:
                # Check exploit maturity
                exploit_maturity = {
                    "weaponized": 100,
                    "functional": 75,
                    "poc": 50,
                    "unproven": 25
                }
                max_exploit = max(
                    exploit_maturity.get(e.get("maturity", "poc"), 50)
                    for e in exploits
                )
            else:
                max_exploit = 0

            # Factor 4: Threat Intelligence (10%)
            threats = record["threats"]
            threat_score = 0
            if threats:
                # Recent mentions increase score
                recent_threats = [
                    t for t in threats
                    if self._is_recent(t.get("timestamp"))
                ]
                threat_score = min(len(recent_threats) * 20, 100)

            # Factor 5: Network Exposure (5%)
            exposure_count = record["exposure_count"]
            exposure_score = min(exposure_count * 10, 100)

            # Calculate weighted total
            total = (
                cvss_normalized * 0.40 +
                max_criticality * 0.25 +
                max_exploit * 0.20 +
                threat_score * 0.10 +
                exposure_score * 0.05
            )

            # Classify
            if total >= self.NOW_THRESHOLD:
                classification = "NOW"
                justification = f"Critical risk: CVSS {cvss_score:.1f}, affects critical assets, exploits available"
            elif total >= self.NEXT_THRESHOLD:
                classification = "NEXT"
                justification = f"High risk: CVSS {cvss_score:.1f}, moderate criticality"
            else:
                classification = "NEVER"
                justification = f"Low priority: CVSS {cvss_score:.1f}, limited exposure"

            # Check trending
            trending = self._calculate_trend(cve_id, total)

            risk_score = RiskScore(
                entity_id=cve_id,
                entity_type="Vulnerability",
                total_score=total,
                cvss_score=cvss_normalized,
                asset_criticality=max_criticality,
                exploit_availability=max_exploit,
                threat_intel=threat_score,
                network_exposure=exposure_score,
                classification=classification,
                justification=justification,
                trending=trending
            )

            # Store for trend analysis
            self._store_historical_score(cve_id, total)

            return risk_score

    def calculate_asset_risk(self, asset_name: str) -> RiskScore:
        """Calculate risk score for an asset based on its vulnerabilities"""
        query = '''
        MATCH (asset:Component {name: $asset_name})
        OPTIONAL MATCH (vuln:Vulnerability)-[:AFFECTS]->(asset)
        OPTIONAL MATCH (asset)-[:EXPOSED_TO]->(interface:NetworkInterface)
        WITH asset,
             COLLECT(DISTINCT vuln) as vulns,
             COUNT(DISTINCT interface) as exposure_count
        RETURN
            asset.name as name,
            asset.criticality as criticality,
            vulns,
            exposure_count
        '''

        with self.driver.session() as session:
            result = session.run(query, asset_name=asset_name)
            record = result.single()

            if not record:
                logger.warning(f"Asset {asset_name} not found")
                return None

            # Asset inherent criticality
            criticality_map = {"critical": 100, "high": 75, "medium": 50, "low": 25}
            asset_crit = criticality_map.get(record["criticality"], 50)

            # Vulnerability impact
            vulns = record["vulns"]
            if vulns:
                avg_cvss = sum(float(v.get("cvss_score", 0)) for v in vulns) / len(vulns)
                cvss_normalized = (avg_cvss / 10.0) * 100
                high_cvss_count = sum(1 for v in vulns if float(v.get("cvss_score", 0)) >= 7.0)
            else:
                cvss_normalized = 0
                high_cvss_count = 0

            # Network exposure
            exposure_count = record["exposure_count"]
            exposure_score = min(exposure_count * 15, 100)

            # Calculate total (weighted differently for assets)
            total = (
                asset_crit * 0.35 +  # Inherent criticality
                cvss_normalized * 0.40 +  # Vulnerability severity
                min(high_cvss_count * 10, 100) * 0.15 +  # High severity count
                exposure_score * 0.10  # Network exposure
            )

            # Classify
            if total >= self.NOW_THRESHOLD:
                classification = "NOW"
                justification = f"Critical asset with {len(vulns)} vulnerabilities, {high_cvss_count} high severity"
            elif total >= self.NEXT_THRESHOLD:
                classification = "NEXT"
                justification = f"Important asset with moderate risk"
            else:
                classification = "NEVER"
                justification = f"Low risk asset"

            trending = self._calculate_trend(asset_name, total)

            return RiskScore(
                entity_id=asset_name,
                entity_type="Asset",
                total_score=total,
                cvss_score=cvss_normalized,
                asset_criticality=asset_crit,
                exploit_availability=0,  # Not applicable to assets
                threat_intel=0,
                network_exposure=exposure_score,
                classification=classification,
                justification=justification,
                trending=trending
            )

    def prioritize_vulnerabilities(self, limit: int = 50) -> List[RiskScore]:
        """Get prioritized list of all vulnerabilities"""
        query = '''
        MATCH (vuln:Vulnerability)
        RETURN vuln.id as id
        ORDER BY vuln.cvss_score DESC
        LIMIT $limit
        '''

        with self.driver.session() as session:
            result = session.run(query, limit=limit)
            cve_ids = [record["id"] for record in result]

        scores = []
        for cve_id in cve_ids:
            score = self.calculate_vulnerability_risk(cve_id)
            if score:
                scores.append(score)

        # Sort by total score
        scores.sort(key=lambda x: x.total_score, reverse=True)

        logger.info(f"Prioritized {len(scores)} vulnerabilities")
        return scores

    def tune_thresholds(self, now_threshold: float, next_threshold: float):
        """Dynamically adjust classification thresholds"""
        self.NOW_THRESHOLD = now_threshold
        self.NEXT_THRESHOLD = next_threshold
        logger.info(f"Thresholds updated: NOW={now_threshold}, NEXT={next_threshold}")

    def _is_recent(self, timestamp: Optional[str], days: int = 30) -> bool:
        """Check if timestamp is within recent period"""
        if not timestamp:
            return False
        try:
            ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return datetime.now() - ts <= timedelta(days=days)
        except:
            return False

    def _calculate_trend(self, entity_id: str, current_score: float) -> str:
        """Calculate if risk is trending up/down/stable"""
        if entity_id not in self.historical_scores:
            return "stable"

        history = self.historical_scores[entity_id]
        if len(history) < 2:
            return "stable"

        # Compare to average of last 3 scores
        recent_avg = sum(history[-3:]) / min(len(history), 3)

        if current_score > recent_avg * 1.1:
            return "up"
        elif current_score < recent_avg * 0.9:
            return "down"
        else:
            return "stable"

    def _store_historical_score(self, entity_id: str, score: float):
        """Store score for trend analysis"""
        if entity_id not in self.historical_scores:
            self.historical_scores[entity_id] = []

        self.historical_scores[entity_id].append(score)

        # Keep last 10 scores only
        if len(self.historical_scores[entity_id]) > 10:
            self.historical_scores[entity_id] = self.historical_scores[entity_id][-10:]

    def generate_risk_report(self, scores: List[RiskScore]) -> Dict:
        """Generate comprehensive risk report"""
        now_risks = [s for s in scores if s.classification == "NOW"]
        next_risks = [s for s in scores if s.classification == "NEXT"]
        never_risks = [s for s in scores if s.classification == "NEVER"]

        trending_up = [s for s in scores if s.trending == "up"]

        report = {
            "summary": {
                "total_scored": len(scores),
                "now_count": len(now_risks),
                "next_count": len(next_risks),
                "never_count": len(never_risks),
                "trending_up": len(trending_up),
                "avg_score": sum(s.total_score for s in scores) / len(scores) if scores else 0
            },
            "now_priorities": [
                {
                    "id": s.entity_id,
                    "type": s.entity_type,
                    "score": round(s.total_score, 2),
                    "cvss": round(s.cvss_score, 2),
                    "trending": s.trending,
                    "justification": s.justification
                }
                for s in now_risks[:20]
            ],
            "next_priorities": [
                {
                    "id": s.entity_id,
                    "score": round(s.total_score, 2),
                    "justification": s.justification
                }
                for s in next_risks[:10]
            ],
            "trending_risks": [
                {
                    "id": s.entity_id,
                    "score": round(s.total_score, 2),
                    "classification": s.classification
                }
                for s in trending_up[:10]
            ]
        }

        return report


def main():
    """Example usage"""
    scorer = RiskScorer(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    try:
        # Calculate risk for specific CVE
        risk = scorer.calculate_vulnerability_risk("CVE-2023-12345")
        if risk:
            print(f"\n{risk.entity_id}:")
            print(f"  Total Score: {risk.total_score:.2f}")
            print(f"  Classification: {risk.classification}")
            print(f"  Trending: {risk.trending}")
            print(f"  Justification: {risk.justification}")

        # Prioritize all vulnerabilities
        priorities = scorer.prioritize_vulnerabilities(limit=100)

        # Generate report
        report = scorer.generate_risk_report(priorities)
        print(json.dumps(report, indent=2))

    finally:
        scorer.close()


if __name__ == "__main__":
    main()
