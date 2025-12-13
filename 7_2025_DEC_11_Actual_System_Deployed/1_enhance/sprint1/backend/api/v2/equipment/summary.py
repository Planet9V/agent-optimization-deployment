"""
GET /api/v2/equipment/summary - Equipment Statistics
File: summary.py
Created: 2025-12-12 05:00:00 UTC
Version: v1.0.0
ICE Score: 8.0
Purpose: Equipment statistics by sector, vendor, and status
"""

from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime
from collections import defaultdict

from ....models.equipment import EquipmentSummary, EquipmentStatus, RiskLevel
from ....database.neo4j_client import Neo4jClient
from ....auth.tenant import get_current_customer_id

router = APIRouter()


@router.get(
    "/summary",
    response_model=EquipmentSummary,
    summary="Get Equipment Summary Statistics",
    description="""
    Retrieve comprehensive equipment statistics aggregated by sector, vendor, status, and risk.

    **Features:**
    - Total equipment count
    - Breakdown by status, type, sector, vendor
    - EOL timeline statistics
    - Vulnerability exposure metrics
    - Risk distribution
    - Maintenance status

    **ICE Score: 8.0**
    - Impact: High (executive dashboard foundation)
    - Complexity: Medium (multi-dimensional aggregation)
    - Effort: Medium (complex query optimization)
    """,
    tags=["Equipment"]
)
async def get_equipment_summary(
    customer_id: str = Depends(get_current_customer_id),
    neo4j: Neo4jClient = Depends()
) -> EquipmentSummary:
    """
    Generate equipment summary statistics

    **Returns:**
    - Total counts and breakdowns
    - EOL risk assessment
    - Vulnerability exposure
    - Maintenance statistics

    **Example Response:**
    ```json
    {
      "total_equipment": 1250,
      "by_status": {
        "active": 1050,
        "maintenance": 75,
        "eol_warning": 100,
        "eol_critical": 25
      },
      "by_type": {
        "network_device": 450,
        "server": 300,
        "workstation": 400
      },
      "by_sector": {
        "energy": 800,
        "finance": 450
      },
      "total_eol_approaching": 125,
      "total_with_critical_vulnerabilities": 45,
      "avg_risk_score": 4.2
    }
    ```
    """
    # Main aggregation query
    query = """
    MATCH (e:Equipment {customer_id: $customer_id})
    OPTIONAL MATCH (e)-[:SUPPLIED_BY]->(v:Vendor)
    OPTIONAL MATCH (e)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)

    WITH e, v,
         count(DISTINCT vuln) as vuln_count,
         count(DISTINCT CASE WHEN vuln.severity = 'CRITICAL' THEN vuln END) as critical_count

    // Calculate risk score for each equipment
    WITH e, v, vuln_count, critical_count,
         (vuln_count * 1.5 + critical_count * 3.0 +
          CASE
            WHEN e.days_until_eol < 0 THEN 5.0
            WHEN e.days_until_eol < 30 THEN 3.0
            WHEN e.days_until_eol < 90 THEN 2.0
            WHEN e.days_until_eol < 180 THEN 1.0
            ELSE 0.0
          END) as risk_score

    RETURN
        // Total counts
        count(e) as total_equipment,

        // By status
        count(CASE WHEN e.status = 'active' THEN 1 END) as active_count,
        count(CASE WHEN e.status = 'inactive' THEN 1 END) as inactive_count,
        count(CASE WHEN e.status = 'maintenance' THEN 1 END) as maintenance_count,
        count(CASE WHEN e.status = 'decommissioned' THEN 1 END) as decommissioned_count,
        count(CASE WHEN e.status = 'pending_deployment' THEN 1 END) as pending_count,
        count(CASE WHEN e.status = 'eol_warning' THEN 1 END) as eol_warning_count,
        count(CASE WHEN e.status = 'eol_critical' THEN 1 END) as eol_critical_count,

        // By type
        count(CASE WHEN e.equipment_type = 'network_device' THEN 1 END) as network_device_count,
        count(CASE WHEN e.equipment_type = 'server' THEN 1 END) as server_count,
        count(CASE WHEN e.equipment_type = 'workstation' THEN 1 END) as workstation_count,
        count(CASE WHEN e.equipment_type = 'mobile_device' THEN 1 END) as mobile_device_count,
        count(CASE WHEN e.equipment_type = 'iot_device' THEN 1 END) as iot_device_count,
        count(CASE WHEN e.equipment_type = 'security_appliance' THEN 1 END) as security_appliance_count,
        count(CASE WHEN e.equipment_type = 'storage_device' THEN 1 END) as storage_device_count,
        count(CASE WHEN e.equipment_type = 'infrastructure' THEN 1 END) as infrastructure_count,

        // EOL statistics
        count(CASE WHEN e.days_until_eol <= 180 AND e.days_until_eol > 90 THEN 1 END) as eol_approaching,
        count(CASE WHEN e.days_until_eol <= 90 AND e.days_until_eol > 0 THEN 1 END) as eol_critical,
        count(CASE WHEN e.days_until_eol < 0 THEN 1 END) as past_eol,

        // Vulnerability statistics
        count(CASE WHEN vuln_count > 0 THEN 1 END) as with_vulnerabilities,
        count(CASE WHEN critical_count > 0 THEN 1 END) as with_critical_vulnerabilities,

        // Risk statistics
        count(CASE WHEN risk_score >= 8.0 THEN 1 END) as risk_critical,
        count(CASE WHEN risk_score >= 6.0 AND risk_score < 8.0 THEN 1 END) as risk_high,
        count(CASE WHEN risk_score >= 4.0 AND risk_score < 6.0 THEN 1 END) as risk_medium,
        count(CASE WHEN risk_score >= 2.0 AND risk_score < 4.0 THEN 1 END) as risk_low,
        count(CASE WHEN risk_score < 2.0 THEN 1 END) as risk_none,

        // Average risk score
        avg(risk_score) as avg_risk_score,

        // Collect for further aggregation
        collect({
            sector: e.sector,
            vendor_name: v.name
        }) as equipment_details
    """

    result = await neo4j.execute_query(query, {'customer_id': customer_id})

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No equipment found for customer"
        )

    record = result[0]

    # Aggregate by sector and vendor
    by_sector = defaultdict(int)
    by_vendor = defaultdict(int)

    for detail in record['equipment_details']:
        if detail['sector']:
            by_sector[detail['sector']] += 1
        if detail['vendor_name']:
            by_vendor[detail['vendor_name']] += 1

    # Build status breakdown
    by_status = {
        'active': record['active_count'],
        'inactive': record['inactive_count'],
        'maintenance': record['maintenance_count'],
        'decommissioned': record['decommissioned_count'],
        'pending_deployment': record['pending_count'],
        'eol_warning': record['eol_warning_count'],
        'eol_critical': record['eol_critical_count']
    }

    # Build type breakdown
    by_type = {
        'network_device': record['network_device_count'],
        'server': record['server_count'],
        'workstation': record['workstation_count'],
        'mobile_device': record['mobile_device_count'],
        'iot_device': record['iot_device_count'],
        'security_appliance': record['security_appliance_count'],
        'storage_device': record['storage_device_count'],
        'infrastructure': record['infrastructure_count']
    }

    # Build risk level breakdown
    by_risk_level = {
        'critical': record['risk_critical'],
        'high': record['risk_high'],
        'medium': record['risk_medium'],
        'low': record['risk_low'],
        'none': record['risk_none']
    }

    # Create summary object
    summary = EquipmentSummary(
        total_equipment=record['total_equipment'],
        by_status=by_status,
        by_type=by_type,
        by_sector=dict(by_sector),
        by_vendor=dict(by_vendor),
        by_risk_level=by_risk_level,
        total_eol_approaching=record['eol_approaching'],
        total_eol_critical=record['eol_critical'],
        total_past_eol=record['past_eol'],
        total_with_vulnerabilities=record['with_vulnerabilities'],
        total_with_critical_vulnerabilities=record['with_critical_vulnerabilities'],
        avg_risk_score=round(record['avg_risk_score'], 2) if record['avg_risk_score'] else 0.0,
        total_active=record['active_count'],
        total_maintenance=record['maintenance_count'],
        total_decommissioned=record['decommissioned_count'],
        customer_id=customer_id,
        generated_at=datetime.utcnow()
    )

    return summary


@router.get(
    "/summary/sector/{sector}",
    response_model=EquipmentSummary,
    summary="Get Sector-Specific Equipment Summary",
    description="Equipment statistics filtered by sector (e.g., energy, finance, healthcare)",
    tags=["Equipment"]
)
async def get_sector_equipment_summary(
    sector: str,
    customer_id: str = Depends(get_current_customer_id),
    neo4j: Neo4jClient = Depends()
) -> EquipmentSummary:
    """
    Generate equipment summary for specific sector

    **Path Parameters:**
    - `sector`: Industry sector (energy, finance, healthcare, manufacturing, etc.)

    **Returns:**
    - Equipment statistics filtered to specified sector
    - All same metrics as main summary endpoint
    """
    # Same query as main summary but filtered by sector
    query = """
    MATCH (e:Equipment {customer_id: $customer_id, sector: $sector})
    OPTIONAL MATCH (e)-[:SUPPLIED_BY]->(v:Vendor)
    OPTIONAL MATCH (e)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)

    WITH e, v,
         count(DISTINCT vuln) as vuln_count,
         count(DISTINCT CASE WHEN vuln.severity = 'CRITICAL' THEN vuln END) as critical_count

    WITH e, v, vuln_count, critical_count,
         (vuln_count * 1.5 + critical_count * 3.0 +
          CASE
            WHEN e.days_until_eol < 0 THEN 5.0
            WHEN e.days_until_eol < 90 THEN 2.0
            WHEN e.days_until_eol < 180 THEN 1.0
            ELSE 0.0
          END) as risk_score

    RETURN
        count(e) as total_equipment,
        count(CASE WHEN e.status = 'active' THEN 1 END) as active_count,
        count(CASE WHEN e.status = 'maintenance' THEN 1 END) as maintenance_count,
        count(CASE WHEN e.status = 'decommissioned' THEN 1 END) as decommissioned_count,
        count(CASE WHEN e.days_until_eol <= 180 THEN 1 END) as eol_approaching,
        count(CASE WHEN e.days_until_eol <= 90 THEN 1 END) as eol_critical,
        count(CASE WHEN vuln_count > 0 THEN 1 END) as with_vulnerabilities,
        count(CASE WHEN critical_count > 0 THEN 1 END) as with_critical_vulnerabilities,
        avg(risk_score) as avg_risk_score
    """

    result = await neo4j.execute_query(query, {
        'customer_id': customer_id,
        'sector': sector
    })

    if not result or result[0]['total_equipment'] == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No equipment found for sector: {sector}"
        )

    record = result[0]

    summary = EquipmentSummary(
        total_equipment=record['total_equipment'],
        by_status={'active': record['active_count'], 'maintenance': record['maintenance_count']},
        by_type={},
        by_sector={sector: record['total_equipment']},
        by_vendor={},
        by_risk_level={},
        total_eol_approaching=record['eol_approaching'],
        total_eol_critical=record['eol_critical'],
        total_with_vulnerabilities=record['with_vulnerabilities'],
        total_with_critical_vulnerabilities=record['with_critical_vulnerabilities'],
        avg_risk_score=round(record['avg_risk_score'], 2) if record['avg_risk_score'] else 0.0,
        total_active=record['active_count'],
        total_maintenance=record['maintenance_count'],
        total_decommissioned=record['decommissioned_count'],
        customer_id=customer_id,
        generated_at=datetime.utcnow()
    )

    return summary
