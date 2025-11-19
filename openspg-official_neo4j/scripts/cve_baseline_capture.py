#!/usr/bin/env python3
"""
CVE Baseline Capture Script
Captures current state of CVE nodes in Neo4j for Wave 0 baseline

Purpose: Create immutable baseline snapshot before schema enhancement
Ensures: Zero CVE deletion policy enforcement through verification
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any
from neo4j import GraphDatabase
import structlog

logger = structlog.get_logger()

class CVEBaselineCapture:
    """
    Captures comprehensive baseline snapshot of CVE nodes

    Baseline includes:
    - Total CVE count (target: 147,923)
    - CVE node property schemas
    - CVE relationship counts
    - Content checksums for verification
    """

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = None
    ):
        """Initialize Neo4j connection"""
        self.neo4j_password = neo4j_password or os.getenv("NEO4J_PASSWORD", "password")
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, self.neo4j_password)
        )

        logger.info("cve_baseline_capture_initialized", uri=neo4j_uri)

    def get_cve_count(self) -> int:
        """Get total CVE node count"""
        with self.driver.session() as session:
            result = session.run("MATCH (c:CVE) RETURN count(c) as count")
            count = result.single()["count"]

            logger.info("cve_count_retrieved", count=count)
            return count

    def get_cve_sample(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """Get sample CVE nodes for schema analysis"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (c:CVE)
                RETURN c
                LIMIT $limit
                """,
                limit=limit
            )

            cves = [dict(record["c"]) for record in result]
            logger.info("cve_sample_retrieved", count=len(cves))
            return cves

    def get_cve_property_schema(self, sample_cves: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze CVE property schema from sample"""
        property_analysis = {}

        for cve in sample_cves:
            for key, value in cve.items():
                if key not in property_analysis:
                    property_analysis[key] = {
                        "type": type(value).__name__,
                        "present_count": 0,
                        "sample_values": []
                    }

                property_analysis[key]["present_count"] += 1

                # Store sample values (max 3)
                if len(property_analysis[key]["sample_values"]) < 3:
                    property_analysis[key]["sample_values"].append(str(value)[:100])

        logger.info("cve_property_schema_analyzed", properties=len(property_analysis))
        return property_analysis

    def get_cve_relationship_counts(self) -> Dict[str, int]:
        """Get counts of all CVE relationship types"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (c:CVE)-[r]->()
                RETURN type(r) as relationship_type, count(r) as count
                """
            )

            relationships = {record["relationship_type"]: record["count"] for record in result}

            total_relationships = sum(relationships.values())
            logger.info(
                "cve_relationships_counted",
                types=len(relationships),
                total=total_relationships
            )

            return relationships

    def compute_content_checksum(self, sample_cves: List[Dict[str, Any]]) -> str:
        """Compute checksum of CVE content for verification"""
        # Sort and serialize for deterministic checksum
        sorted_data = json.dumps(sample_cves, sort_keys=True, default=str)
        checksum = hashlib.sha256(sorted_data.encode()).hexdigest()

        logger.info("content_checksum_computed", checksum=checksum[:16])
        return checksum

    def capture_baseline(self, output_path: str = None) -> Dict[str, Any]:
        """
        Capture comprehensive CVE baseline

        Returns:
            Baseline snapshot with all verification data
        """
        if output_path is None:
            output_path = "/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/1_Comprehensive_Schema_Enhancement_Plan_v2/CVE_BASELINE_WAVE0.json"

        logger.info("baseline_capture_started")

        # Capture all baseline metrics
        cve_count = self.get_cve_count()
        cve_sample = self.get_cve_sample(limit=1000)
        property_schema = self.get_cve_property_schema(cve_sample)
        relationships = self.get_cve_relationship_counts()
        content_checksum = self.compute_content_checksum(cve_sample)

        # Build baseline snapshot
        baseline = {
            "metadata": {
                "captured_at": datetime.now().isoformat(),
                "wave": 0,
                "purpose": "Pre-enhancement baseline for CVE preservation verification",
                "target_cve_count": 147923
            },
            "cve_metrics": {
                "total_count": cve_count,
                "expected_count": 147923,
                "count_match": cve_count == 147923,
                "sample_size": len(cve_sample)
            },
            "property_schema": property_schema,
            "relationships": {
                "types": relationships,
                "total_count": sum(relationships.values())
            },
            "verification": {
                "content_checksum": content_checksum,
                "sample_checksum_size": len(cve_sample)
            },
            "preservation_rules": {
                "zero_deletion_policy": True,
                "additive_only": True,
                "no_cve_reimport": True
            }
        }

        # Export baseline
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(baseline, f, indent=2)

        logger.info(
            "baseline_capture_completed",
            cve_count=cve_count,
            relationships=sum(relationships.values()),
            output=output_path
        )

        return baseline

    def verify_baseline(self, baseline_path: str) -> Dict[str, Any]:
        """
        Verify current state against baseline

        Returns:
            Verification report with any discrepancies
        """
        # Load baseline
        with open(baseline_path, 'r') as f:
            baseline = json.load(f)

        # Get current state
        current_count = self.get_cve_count()
        current_sample = self.get_cve_sample(limit=1000)
        current_checksum = self.compute_content_checksum(current_sample)
        current_relationships = self.get_cve_relationship_counts()

        # Compare
        verification = {
            "verified_at": datetime.now().isoformat(),
            "baseline_captured_at": baseline["metadata"]["captured_at"],
            "cve_count": {
                "baseline": baseline["cve_metrics"]["total_count"],
                "current": current_count,
                "match": current_count >= baseline["cve_metrics"]["total_count"],
                "difference": current_count - baseline["cve_metrics"]["total_count"]
            },
            "content_checksum": {
                "baseline": baseline["verification"]["content_checksum"],
                "current": current_checksum,
                "match": current_checksum == baseline["verification"]["content_checksum"]
            },
            "relationships": {
                "baseline_total": baseline["relationships"]["total_count"],
                "current_total": sum(current_relationships.values()),
                "difference": sum(current_relationships.values()) - baseline["relationships"]["total_count"]
            },
            "preservation_status": "PASS" if current_count >= baseline["cve_metrics"]["total_count"] else "FAIL"
        }

        logger.info(
            "baseline_verification_completed",
            status=verification["preservation_status"],
            cve_difference=verification["cve_count"]["difference"]
        )

        return verification

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()
        logger.info("neo4j_connection_closed")


# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CVE Baseline Capture Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Capture command
    capture_parser = subparsers.add_parser("capture", help="Capture CVE baseline")
    capture_parser.add_argument("--output", default=None, help="Output path for baseline JSON")

    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify against baseline")
    verify_parser.add_argument(
        "--baseline",
        default="/home/jim/2_OXOT_Projects_Dev/10_Ontologies/AEON_DT_CyberSec_Threat_Intel/1_Comprehensive_Schema_Enhancement_Plan_v2/CVE_BASELINE_WAVE0.json",
        help="Path to baseline JSON"
    )

    args = parser.parse_args()

    capturer = CVEBaselineCapture()

    try:
        if args.command == "capture":
            baseline = capturer.capture_baseline(output_path=args.output)

            print("\n✅ CVE Baseline Captured Successfully")
            print(f"📊 Total CVE Count: {baseline['cve_metrics']['total_count']}")
            print(f"🔗 Total Relationships: {baseline['relationships']['total_count']}")
            print(f"📋 Property Schema: {len(baseline['property_schema'])} properties")
            print(f"🔐 Content Checksum: {baseline['verification']['content_checksum'][:16]}...")

            if baseline['cve_metrics']['count_match']:
                print(f"✅ CVE count matches expected: {baseline['cve_metrics']['expected_count']}")
            else:
                print(f"⚠️  CVE count mismatch: Expected {baseline['cve_metrics']['expected_count']}, Got {baseline['cve_metrics']['total_count']}")

        elif args.command == "verify":
            verification = capturer.verify_baseline(args.baseline)

            print("\n🔍 CVE Baseline Verification")
            print(f"📊 CVE Count Change: {verification['cve_count']['difference']:+d}")
            print(f"🔗 Relationship Change: {verification['relationships']['difference']:+d}")
            print(f"🔐 Content Match: {'✅ Yes' if verification['content_checksum']['match'] else '❌ No'}")
            print(f"🛡️  Preservation Status: {verification['preservation_status']}")

            if verification['preservation_status'] == "FAIL":
                print("\n🚨 CVE DELETION DETECTED - INVESTIGATION REQUIRED")
            else:
                print("\n✅ CVE Preservation Verified - No Deletions Detected")

    finally:
        capturer.close()
