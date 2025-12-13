"""
GET /api/v2/equipment/eol-report - Equipment EOL Report
File: eol_report.py
Created: 2025-12-12 05:00:00 UTC
Version: v1.0.0
ICE Score: 6.4
Purpose: Equipment approaching end-of-life with risk assessment
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from datetime import datetime, date
from typing import Optional, List
import uuid

from ....models.equipment import (
    EOLReport,
    EOLEquipment,
    EquipmentType,
    EquipmentStatus,
    RiskLevel
)
from ....database.neo4j_client import Neo4jClient
from ....auth.tenant import get_current_customer_id

router = APIRouter()


def assess_eol_risk(
    days_until_eol: Optional[int],
    days_until_eos: Optional[int],
    vulnerability_count: int,
    critical_vuln_count: int,
    has_replacement: bool,
    has_migration_plan: bool
) -> tuple[RiskLevel, str, bool]:
    """
    Assess EOL risk level and determine action requirements

    Returns: (risk_level, business_impact, immediate_action_required)
    """
    risk_score = 0.0

    # Timeline risk
    if days_until_eol is not None:
        if days_until_eol < 0:
            risk_score += 10.0
        elif days_until_eol < 30:
            risk_score += 8.0
        elif days_until_eol < 90:
            risk_score += 5.0
        elif days_until_eol < 180:
            risk_score += 3.0

    # Vulnerability risk
    risk_score += critical_vuln_count * 2.0
    risk_score += (vulnerability_count - critical_vuln_count) * 0.5

    # Mitigation factors
    if has_replacement:
        risk_score -= 2.0
    if has_migration_plan:
        risk_score -= 3.0

    # Support status
    if days_until_eos is not None and days_until_eos < 0:
        risk_score += 5.0

    # Cap at reasonable maximum
    risk_score = max(0.0, min(risk_score, 20.0))

    # Determine risk level
    if risk_score >= 12.0:
        risk_level = RiskLevel.CRITICAL
        business_impact = "critical"
        immediate_action = True
    elif risk_score >= 8.0:
        risk_level = RiskLevel.HIGH
        business_impact = "high"
        immediate_action = True
    elif risk_score >= 5.0:
        risk_level = RiskLevel.MEDIUM
        business_impact = "medium"
        immediate_action = False
    elif risk_score >= 2.0:
        risk_level = RiskLevel.LOW
        business_impact = "low"
        immediate_action = False
    else:
        risk_level = RiskLevel.NONE
        business_impact = "minimal"
        immediate_action = False

    return risk_level, business_impact, immediate_action


@router.get(
    "/eol-report",
    response_model=EOLReport,
    summary="Generate Equipment EOL Report",
    description="""
    Generate comprehensive end-of-life analysis report for equipment.

    **Features:**
    - Equipment approaching EOL (< 180 days)
    - Equipment past EOL date
    - Risk assessment and prioritization
    - Replacement and migration planning status
    - Sector and vendor breakdown
    - Business impact analysis

    **ICE Score: 6.4**
    - Impact: High (proactive lifecycle management)
    - Complexity: Medium (risk calculation, aggregation)
    - Effort: Medium (complex filtering and sorting)
    """,
    tags=["Equipment"]
)
async def get_eol_report(
    customer_id: str = Depends(get_current_customer_id),
    neo4j: Neo4jClient = Depends(),
    eol_threshold_days: int = Query(180, ge=0, le=365, description="Days until EOL threshold"),
    include_past_eol: bool = Query(True, description="Include equipment past EOL"),
    sector: Optional[str] = Query(None, description="Filter by sector"),
    equipment_type: Optional[str] = Query(None, description="Filter by equipment type"),
    min_risk_level: Optional[str] = Query(None, description="Minimum risk level (low, medium, high, critical)")
) -> EOLReport:
    """
    Generate EOL report for equipment lifecycle management

    **Query Parameters:**
    - `eol_threshold_days`: Days until EOL to include (default: 180)
    - `include_past_eol`: Include equipment already past EOL (default: true)
    - `sector`: Filter by specific sector
    - `equipment_type`: Filter by equipment type
    - `min_risk_level`: Minimum risk level to include

    **Returns:**
    - Comprehensive EOL report with prioritized equipment list
    - Risk breakdown and statistics
    - Sector/type/vendor analysis
    - Action recommendations

    **Example Response:**
    ```json
    {
      "total_equipment_reviewed": 1250,
      "total_eol_approaching": 125,
      "total_eol_critical": 25,
      "total_past_eol": 15,
      "critical_risk_count": 40,
      "immediate_action_required": 40,
      "equipment": [...]
    }
    ```
    """
    # Build WHERE clause
    where_clauses = ["e.customer_id = $customer_id"]
    params = {
        'customer_id': customer_id,
        'eol_threshold_days': eol_threshold_days
    }

    # EOL date filtering
    if include_past_eol:
        where_clauses.append("(e.days_until_eol <= $eol_threshold_days OR e.days_until_eol < 0)")
    else:
        where_clauses.append("e.days_until_eol <= $eol_threshold_days AND e.days_until_eol >= 0")

    if sector:
        where_clauses.append("e.sector = $sector")
        params['sector'] = sector

    if equipment_type:
        where_clauses.append("e.equipment_type = $equipment_type")
        params['equipment_type'] = equipment_type

    where_clause = " AND ".join(where_clauses)

    # Main query
    query = f"""
    MATCH (e:Equipment)
    WHERE {where_clause}
    OPTIONAL MATCH (e)-[:SUPPLIED_BY]->(v:Vendor)
    OPTIONAL MATCH (e)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)

    WITH e, v,
         count(DISTINCT vuln) as vuln_count,
         count(DISTINCT CASE WHEN vuln.severity = 'CRITICAL' THEN vuln END) as critical_count

    // Calculate current days until EOL/EOS
    WITH e, v, vuln_count, critical_count,
         CASE WHEN e.eol_date IS NOT NULL
              THEN duration.between(date(), date(e.eol_date)).days
              ELSE null
         END as current_days_until_eol,
         CASE WHEN e.eos_date IS NOT NULL
              THEN duration.between(date(), date(e.eos_date)).days
              ELSE null
         END as current_days_until_eos

    RETURN e,
           v.name as vendor_name,
           vuln_count,
           critical_count,
           current_days_until_eol,
           current_days_until_eos
    ORDER BY current_days_until_eol ASC, critical_count DESC
    """

    results = await neo4j.execute_query(query, params)

    if not results:
        # Return empty report
        return EOLReport(
            report_id=f"eol_report_{uuid.uuid4().hex[:8]}",
            customer_id=customer_id,
            generated_at=datetime.utcnow(),
            total_equipment_reviewed=0,
            total_eol_approaching=0,
            total_eol_critical=0,
            total_past_eol=0,
            equipment=[]
        )

    # Process equipment and calculate risk
    equipment_list = []
    stats = {
        'total_reviewed': len(results),
        'eol_approaching': 0,  # 180-90 days
        'eol_critical': 0,     # <90 days
        'past_eol': 0,
        'past_eos': 0,
        'by_sector': {},
        'by_type': {},
        'by_vendor': {},
        'risk_critical': 0,
        'risk_high': 0,
        'risk_medium': 0,
        'risk_low': 0,
        'immediate_action': 0,
        'planning_required': 0
    }

    for record in results:
        e = record['e']
        days_until_eol = record['current_days_until_eol']
        days_until_eos = record['current_days_until_eos']
        vuln_count = record['vuln_count']
        critical_count = record['critical_count']

        # Check for replacement/migration (would be in metadata or separate nodes)
        metadata = e.get('metadata', {})
        has_replacement = metadata.get('replacement_available', False)
        has_migration_plan = metadata.get('migration_plan_exists', False)

        # Assess risk
        risk_level, business_impact, immediate_action = assess_eol_risk(
            days_until_eol,
            days_until_eos,
            vuln_count,
            critical_count,
            has_replacement,
            has_migration_plan
        )

        # Apply min_risk_level filter
        if min_risk_level:
            risk_threshold = {
                'low': 0,
                'medium': 1,
                'high': 2,
                'critical': 3
            }
            risk_levels = ['none', 'low', 'medium', 'high', 'critical']
            if risk_levels.index(risk_level.value) < risk_threshold.get(min_risk_level, 0):
                continue

        # Update statistics
        if days_until_eol is not None:
            if days_until_eol < 0:
                stats['past_eol'] += 1
            elif days_until_eol < 90:
                stats['eol_critical'] += 1
            elif days_until_eol < 180:
                stats['eol_approaching'] += 1

        if days_until_eos is not None and days_until_eos < 0:
            stats['past_eos'] += 1

        # Risk counts
        if risk_level == RiskLevel.CRITICAL:
            stats['risk_critical'] += 1
        elif risk_level == RiskLevel.HIGH:
            stats['risk_high'] += 1
        elif risk_level == RiskLevel.MEDIUM:
            stats['risk_medium'] += 1
        elif risk_level == RiskLevel.LOW:
            stats['risk_low'] += 1

        if immediate_action:
            stats['immediate_action'] += 1
        else:
            stats['planning_required'] += 1

        # Sector/type/vendor aggregation
        sector = e.get('sector', 'unknown')
        stats['by_sector'][sector] = stats['by_sector'].get(sector, 0) + 1

        equipment_type_val = e.get('equipment_type', 'unknown')
        stats['by_type'][equipment_type_val] = stats['by_type'].get(equipment_type_val, 0) + 1

        vendor_name = record.get('vendor_name', 'unknown')
        stats['by_vendor'][vendor_name] = stats['by_vendor'].get(vendor_name, 0) + 1

        # Create EOLEquipment object
        eol_equipment = EOLEquipment(
            equipment_id=e['equipment_id'],
            name=e['name'],
            equipment_type=EquipmentType(e['equipment_type']),
            manufacturer=e['manufacturer'],
            model=e['model'],
            sector=sector,
            vendor_name=record.get('vendor_name'),
            eol_date=date.fromisoformat(e['eol_date']) if e.get('eol_date') else None,
            eos_date=date.fromisoformat(e['eos_date']) if e.get('eos_date') else None,
            days_until_eol=days_until_eol,
            days_until_eos=days_until_eos,
            status=EquipmentStatus(e.get('status', 'active')),
            eol_risk_level=risk_level,
            vulnerability_count=vuln_count,
            critical_vulnerability_count=critical_count,
            risk_score=0.0,  # Could calculate comprehensive risk score
            replacement_available=has_replacement,
            migration_plan_exists=has_migration_plan,
            business_impact=business_impact,
            location=e.get('location')
        )
        equipment_list.append(eol_equipment)

    # Generate report
    report = EOLReport(
        report_id=f"eol_report_{datetime.utcnow().strftime('%Y%m%d')}_{uuid.uuid4().hex[:6]}",
        customer_id=customer_id,
        generated_at=datetime.utcnow(),
        total_equipment_reviewed=stats['total_reviewed'],
        total_eol_approaching=stats['eol_approaching'],
        total_eol_critical=stats['eol_critical'],
        total_past_eol=stats['past_eol'],
        total_past_eos=stats['past_eos'],
        critical_risk_count=stats['risk_critical'],
        high_risk_count=stats['risk_high'],
        medium_risk_count=stats['risk_medium'],
        low_risk_count=stats['risk_low'],
        equipment=equipment_list,
        by_sector=stats['by_sector'],
        by_type=stats['by_type'],
        by_vendor=stats['by_vendor'],
        immediate_action_required=stats['immediate_action'],
        planning_required=stats['planning_required']
    )

    return report


@router.get(
    "/eol-report/export",
    summary="Export EOL Report",
    description="Export EOL report in CSV or JSON format for external analysis",
    tags=["Equipment"]
)
async def export_eol_report(
    customer_id: str = Depends(get_current_customer_id),
    neo4j: Neo4jClient = Depends(),
    format: str = Query("json", regex="^(json|csv)$", description="Export format")
) -> dict:
    """
    Export EOL report for external analysis

    **Query Parameters:**
    - `format`: Export format (json or csv)

    **Returns:**
    - Formatted report data ready for download
    """
    # Generate report
    report = await get_eol_report(customer_id, neo4j)

    if format == "csv":
        # Convert to CSV-friendly format
        csv_data = []
        for eq in report.equipment:
            csv_data.append({
                'equipment_id': eq.equipment_id,
                'name': eq.name,
                'type': eq.equipment_type.value,
                'manufacturer': eq.manufacturer,
                'model': eq.model,
                'sector': eq.sector,
                'vendor': eq.vendor_name or 'N/A',
                'eol_date': eq.eol_date.isoformat() if eq.eol_date else 'N/A',
                'days_until_eol': eq.days_until_eol if eq.days_until_eol is not None else 'N/A',
                'status': eq.status.value,
                'risk_level': eq.eol_risk_level.value,
                'vulnerabilities': eq.vulnerability_count,
                'critical_vulnerabilities': eq.critical_vulnerability_count,
                'replacement_available': 'Yes' if eq.replacement_available else 'No',
                'migration_plan': 'Yes' if eq.migration_plan_exists else 'No',
                'business_impact': eq.business_impact,
                'location': eq.location or 'N/A'
            })

        return {
            'format': 'csv',
            'filename': f"eol_report_{report.report_id}.csv",
            'data': csv_data,
            'record_count': len(csv_data)
        }
    else:
        # Return JSON
        return {
            'format': 'json',
            'filename': f"eol_report_{report.report_id}.json",
            'data': report.dict(),
            'generated_at': report.generated_at.isoformat()
        }
