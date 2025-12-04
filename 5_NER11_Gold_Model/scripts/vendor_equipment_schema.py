"""
Vendor Equipment Schema Migration
=================================

Neo4j schema migration for E15: Vendor Equipment Lifecycle Management.
Creates Vendor, EquipmentModel, and SupportContract nodes with indexes.

Version: 1.0.0
Created: 2025-12-04
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


VENDOR_EQUIPMENT_SCHEMA = """
-- E15: Vendor Equipment Lifecycle Management Schema
-- Phase B2 - Supply Chain
-- Created: 2025-12-04

-- =============================================
-- NODE CONSTRAINTS
-- =============================================

-- Vendor node constraint
CREATE CONSTRAINT vendor_unique IF NOT EXISTS
FOR (v:Vendor) REQUIRE v.vendor_id IS UNIQUE;

-- EquipmentModel node constraint
CREATE CONSTRAINT equipment_model_unique IF NOT EXISTS
FOR (em:EquipmentModel) REQUIRE em.model_id IS UNIQUE;

-- SupportContract node constraint
CREATE CONSTRAINT support_contract_unique IF NOT EXISTS
FOR (sc:SupportContract) REQUIRE sc.contract_id IS UNIQUE;

-- =============================================
-- PERFORMANCE INDEXES
-- =============================================

-- Vendor indexes
CREATE INDEX vendor_customer_id IF NOT EXISTS
FOR (v:Vendor) ON (v.customer_id);

CREATE INDEX vendor_risk_score IF NOT EXISTS
FOR (v:Vendor) ON (v.risk_score);

CREATE INDEX vendor_support_status IF NOT EXISTS
FOR (v:Vendor) ON (v.support_status);

CREATE INDEX vendor_name IF NOT EXISTS
FOR (v:Vendor) ON (v.name);

CREATE INDEX vendor_supply_chain_tier IF NOT EXISTS
FOR (v:Vendor) ON (v.supply_chain_tier);

-- EquipmentModel indexes
CREATE INDEX equipment_customer_id IF NOT EXISTS
FOR (em:EquipmentModel) ON (em.customer_id);

CREATE INDEX equipment_vendor_id IF NOT EXISTS
FOR (em:EquipmentModel) ON (em.vendor_id);

CREATE INDEX equipment_eol_date IF NOT EXISTS
FOR (em:EquipmentModel) ON (em.eol_date);

CREATE INDEX equipment_lifecycle_status IF NOT EXISTS
FOR (em:EquipmentModel) ON (em.lifecycle_status);

CREATE INDEX equipment_criticality IF NOT EXISTS
FOR (em:EquipmentModel) ON (em.criticality);

CREATE INDEX equipment_category IF NOT EXISTS
FOR (em:EquipmentModel) ON (em.category);

-- SupportContract indexes
CREATE INDEX contract_customer_id IF NOT EXISTS
FOR (sc:SupportContract) ON (sc.customer_id);

CREATE INDEX contract_vendor_id IF NOT EXISTS
FOR (sc:SupportContract) ON (sc.vendor_id);

CREATE INDEX contract_end_date IF NOT EXISTS
FOR (sc:SupportContract) ON (sc.end_date);

CREATE INDEX contract_status IF NOT EXISTS
FOR (sc:SupportContract) ON (sc.status);

-- Composite indexes for common queries
CREATE INDEX vendor_customer_risk IF NOT EXISTS
FOR (v:Vendor) ON (v.customer_id, v.risk_score);

CREATE INDEX equipment_customer_lifecycle IF NOT EXISTS
FOR (em:EquipmentModel) ON (em.customer_id, em.lifecycle_status);

CREATE INDEX equipment_vendor_customer IF NOT EXISTS
FOR (em:EquipmentModel) ON (em.vendor_id, em.customer_id);

-- =============================================
-- RELATIONSHIP TYPES
-- =============================================

-- Vendor -[:MANUFACTURES]-> EquipmentModel
-- Vendor -[:HAS_CONTRACT]-> SupportContract
-- SupportContract -[:COVERS]-> EquipmentModel
-- Vendor -[:AFFECTED_BY]-> CVE (links to existing CVE entities)
-- EquipmentModel -[:VULNERABLE_TO]-> CVE

"""

CYPHER_STATEMENTS = [
    # Constraints
    "CREATE CONSTRAINT vendor_unique IF NOT EXISTS FOR (v:Vendor) REQUIRE v.vendor_id IS UNIQUE",
    "CREATE CONSTRAINT equipment_model_unique IF NOT EXISTS FOR (em:EquipmentModel) REQUIRE em.model_id IS UNIQUE",
    "CREATE CONSTRAINT support_contract_unique IF NOT EXISTS FOR (sc:SupportContract) REQUIRE sc.contract_id IS UNIQUE",

    # Vendor indexes
    "CREATE INDEX vendor_customer_id IF NOT EXISTS FOR (v:Vendor) ON (v.customer_id)",
    "CREATE INDEX vendor_risk_score IF NOT EXISTS FOR (v:Vendor) ON (v.risk_score)",
    "CREATE INDEX vendor_support_status IF NOT EXISTS FOR (v:Vendor) ON (v.support_status)",
    "CREATE INDEX vendor_name IF NOT EXISTS FOR (v:Vendor) ON (v.name)",
    "CREATE INDEX vendor_supply_chain_tier IF NOT EXISTS FOR (v:Vendor) ON (v.supply_chain_tier)",

    # Equipment indexes
    "CREATE INDEX equipment_customer_id IF NOT EXISTS FOR (em:EquipmentModel) ON (em.customer_id)",
    "CREATE INDEX equipment_vendor_id IF NOT EXISTS FOR (em:EquipmentModel) ON (em.vendor_id)",
    "CREATE INDEX equipment_eol_date IF NOT EXISTS FOR (em:EquipmentModel) ON (em.eol_date)",
    "CREATE INDEX equipment_lifecycle_status IF NOT EXISTS FOR (em:EquipmentModel) ON (em.lifecycle_status)",
    "CREATE INDEX equipment_criticality IF NOT EXISTS FOR (em:EquipmentModel) ON (em.criticality)",
    "CREATE INDEX equipment_category IF NOT EXISTS FOR (em:EquipmentModel) ON (em.category)",

    # Contract indexes
    "CREATE INDEX contract_customer_id IF NOT EXISTS FOR (sc:SupportContract) ON (sc.customer_id)",
    "CREATE INDEX contract_vendor_id IF NOT EXISTS FOR (sc:SupportContract) ON (sc.vendor_id)",
    "CREATE INDEX contract_end_date IF NOT EXISTS FOR (sc:SupportContract) ON (sc.end_date)",
    "CREATE INDEX contract_status IF NOT EXISTS FOR (sc:SupportContract) ON (sc.status)",

    # Composite indexes
    "CREATE INDEX vendor_customer_risk IF NOT EXISTS FOR (v:Vendor) ON (v.customer_id, v.risk_score)",
    "CREATE INDEX equipment_customer_lifecycle IF NOT EXISTS FOR (em:EquipmentModel) ON (em.customer_id, em.lifecycle_status)",
    "CREATE INDEX equipment_vendor_customer IF NOT EXISTS FOR (em:EquipmentModel) ON (em.vendor_id, em.customer_id)",
]


def apply_schema(driver) -> dict:
    """
    Apply the vendor equipment schema to Neo4j.

    Args:
        driver: Neo4j driver instance

    Returns:
        dict with 'success', 'applied', and 'errors' counts
    """
    applied = 0
    errors = 0
    error_messages = []

    with driver.session() as session:
        for statement in CYPHER_STATEMENTS:
            try:
                session.run(statement)
                applied += 1
                logger.info(f"Applied: {statement[:60]}...")
            except Exception as e:
                error_str = str(e)
                # Ignore "already exists" errors
                if "already exists" in error_str.lower() or "equivalent" in error_str.lower():
                    applied += 1
                    logger.debug(f"Already exists: {statement[:60]}...")
                else:
                    errors += 1
                    error_messages.append(f"{statement[:40]}: {error_str}")
                    logger.error(f"Error applying {statement[:60]}: {e}")

    result = {
        "success": errors == 0,
        "applied": applied,
        "errors": errors,
        "total": len(CYPHER_STATEMENTS),
        "error_messages": error_messages,
    }

    logger.info(f"Schema migration complete: {applied}/{len(CYPHER_STATEMENTS)} applied, {errors} errors")
    return result


def verify_schema(driver) -> dict:
    """
    Verify the vendor equipment schema is correctly applied.

    Returns:
        dict with verification results
    """
    results = {
        "constraints": [],
        "indexes": [],
        "node_counts": {},
    }

    with driver.session() as session:
        # Check constraints
        constraints_result = session.run("SHOW CONSTRAINTS")
        for record in constraints_result:
            if record.get("labelsOrTypes") in [["Vendor"], ["EquipmentModel"], ["SupportContract"]]:
                results["constraints"].append({
                    "name": record.get("name"),
                    "type": record.get("type"),
                    "labels": record.get("labelsOrTypes"),
                })

        # Check indexes
        indexes_result = session.run("SHOW INDEXES")
        for record in indexes_result:
            labels = record.get("labelsOrTypes") or []
            if labels and any(label in ["Vendor", "EquipmentModel", "SupportContract"] for label in labels):
                results["indexes"].append({
                    "name": record.get("name"),
                    "type": record.get("type"),
                    "labels": labels,
                    "properties": record.get("properties"),
                })

        # Get node counts
        for label in ["Vendor", "EquipmentModel", "SupportContract"]:
            count_result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
            record = count_result.single()
            results["node_counts"][label] = record["count"] if record else 0

    return results


def create_sample_data(driver, customer_id: str = "CUST-001") -> dict:
    """
    Create sample vendor equipment data for testing.

    Args:
        driver: Neo4j driver instance
        customer_id: Customer ID for isolation

    Returns:
        dict with creation results
    """
    from datetime import date, timedelta

    today = date.today()
    eol_soon = today + timedelta(days=90)
    eol_past = today - timedelta(days=30)

    sample_data = {
        "vendors": [
            {
                "vendor_id": "VENDOR-CISCO-001",
                "name": "Cisco Systems",
                "customer_id": customer_id,
                "risk_score": 3.5,
                "risk_level": "medium",
                "support_status": "active",
                "country": "USA",
                "industry_focus": ["IT", "Network"],
                "supply_chain_tier": 1,
                "total_cves": 156,
                "avg_cvss_score": 6.2,
            },
            {
                "vendor_id": "VENDOR-SIEMENS-001",
                "name": "Siemens AG",
                "customer_id": customer_id,
                "risk_score": 5.8,
                "risk_level": "medium",
                "support_status": "active",
                "country": "Germany",
                "industry_focus": ["ICS", "SCADA"],
                "supply_chain_tier": 1,
                "total_cves": 89,
                "avg_cvss_score": 7.1,
            },
            {
                "vendor_id": "VENDOR-SOLARWINDS-001",
                "name": "SolarWinds",
                "customer_id": customer_id,
                "risk_score": 8.5,
                "risk_level": "critical",
                "support_status": "limited",
                "country": "USA",
                "industry_focus": ["IT", "Monitoring"],
                "supply_chain_tier": 2,
                "total_cves": 24,
                "avg_cvss_score": 9.2,
            },
        ],
        "equipment": [
            {
                "model_id": "EQ-CISCO-ASA5500",
                "vendor_id": "VENDOR-CISCO-001",
                "model_name": "ASA 5500 Series",
                "customer_id": customer_id,
                "product_line": "Security Appliances",
                "eol_date": eol_past.isoformat(),
                "eos_date": (eol_past - timedelta(days=365)).isoformat(),
                "lifecycle_status": "eol",
                "criticality": "critical",
                "category": "firewall",
                "deployed_count": 15,
                "vulnerability_count": 8,
            },
            {
                "model_id": "EQ-CISCO-C9300",
                "vendor_id": "VENDOR-CISCO-001",
                "model_name": "Catalyst 9300",
                "customer_id": customer_id,
                "product_line": "Switches",
                "eol_date": eol_soon.isoformat(),
                "lifecycle_status": "approaching_eol",
                "criticality": "high",
                "category": "switch",
                "deployed_count": 45,
                "vulnerability_count": 3,
            },
            {
                "model_id": "EQ-SIEMENS-S7300",
                "vendor_id": "VENDOR-SIEMENS-001",
                "model_name": "SIMATIC S7-300",
                "customer_id": customer_id,
                "product_line": "PLCs",
                "eol_date": (today + timedelta(days=365)).isoformat(),
                "lifecycle_status": "current",
                "criticality": "critical",
                "category": "plc",
                "deployed_count": 12,
                "vulnerability_count": 5,
            },
        ],
    }

    created = {"vendors": 0, "equipment": 0}

    with driver.session() as session:
        # Create vendors
        for vendor in sample_data["vendors"]:
            try:
                session.run(
                    """
                    MERGE (v:Vendor {vendor_id: $vendor_id})
                    SET v += $props
                    """,
                    vendor_id=vendor["vendor_id"],
                    props=vendor,
                )
                created["vendors"] += 1
            except Exception as e:
                logger.error(f"Error creating vendor {vendor['vendor_id']}: {e}")

        # Create equipment with relationships
        for equipment in sample_data["equipment"]:
            try:
                session.run(
                    """
                    MERGE (em:EquipmentModel {model_id: $model_id})
                    SET em += $props
                    WITH em
                    MATCH (v:Vendor {vendor_id: $vendor_id, customer_id: $customer_id})
                    MERGE (v)-[:MANUFACTURES]->(em)
                    """,
                    model_id=equipment["model_id"],
                    vendor_id=equipment["vendor_id"],
                    customer_id=customer_id,
                    props=equipment,
                )
                created["equipment"] += 1
            except Exception as e:
                logger.error(f"Error creating equipment {equipment['model_id']}: {e}")

    return created


if __name__ == "__main__":
    """Run schema migration from command line."""
    import os
    from neo4j import GraphDatabase

    logging.basicConfig(level=logging.INFO)

    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD", "neo4j@openspg")

    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    try:
        print("Applying vendor equipment schema...")
        result = apply_schema(driver)
        print(f"Result: {result}")

        print("\nVerifying schema...")
        verification = verify_schema(driver)
        print(f"Constraints: {len(verification['constraints'])}")
        print(f"Indexes: {len(verification['indexes'])}")
        print(f"Node counts: {verification['node_counts']}")

    finally:
        driver.close()
