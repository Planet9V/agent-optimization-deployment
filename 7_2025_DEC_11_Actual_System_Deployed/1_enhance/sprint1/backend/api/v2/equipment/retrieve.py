"""
GET /api/v2/equipment/{equipment_id} - Retrieve Equipment Details
File: retrieve.py
Created: 2025-12-12 05:00:00 UTC
Version: v1.0.0
ICE Score: 9.0
Purpose: Comprehensive equipment retrieval with vendor, EOL, and vulnerability data
"""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from datetime import datetime, date
from typing import Optional, List

from ....models.equipment import Equipment, EquipmentStatus, RiskLevel
from ....database.neo4j_client import Neo4jClient
from ....auth.tenant import get_current_customer_id

router = APIRouter()


def calculate_risk_score(
    vulnerability_count: int,
    critical_vuln_count: int,
    high_vuln_count: int,
    days_until_eol: Optional[int],
    status: str
) -> tuple:
    """
    Calculate equipment risk score (0-10) and risk level

    Risk factors:
    - Critical vulnerabilities: +3.0 per vuln
    - High vulnerabilities: +1.5 per vuln
    - EOL status: +2.0 if <90 days, +1.0 if <180 days
    - Decommissioned: +5.0
    """
    risk_score = 0.0

    # Vulnerability-based risk
    risk_score += critical_vuln_count * 3.0
    risk_score += high_vuln_count * 1.5

    # EOL-based risk
    if days_until_eol is not None:
        if days_until_eol < 0:
            risk_score += 5.0  # Past EOL
        elif days_until_eol < 30:
            risk_score += 3.0
        elif days_until_eol < 90:
            risk_score += 2.0
        elif days_until_eol < 180:
            risk_score += 1.0

    # Status-based risk
    if status == EquipmentStatus.DECOMMISSIONED.value:
        risk_score += 5.0
    elif status == EquipmentStatus.EOL_CRITICAL.value:
        risk_score += 2.0

    # Cap at 10.0
    risk_score = min(risk_score, 10.0)

    # Determine risk level
    if risk_score >= 8.0:
        risk_level = RiskLevel.CRITICAL
    elif risk_score >= 6.0:
        risk_level = RiskLevel.HIGH
    elif risk_score >= 4.0:
        risk_level = RiskLevel.MEDIUM
    elif risk_score >= 2.0:
        risk_level = RiskLevel.LOW
    else:
        risk_level = RiskLevel.NONE

    return risk_score, risk_level


@router.get(
    "/{equipment_id}",
    response_model=Equipment,
    summary="Get Equipment Details",
    description="""
    Retrieve comprehensive equipment details including vendor, EOL dates, and vulnerabilities.

    **Features:**
    - Complete equipment information
    - Linked vendor details
    - Vulnerability statistics
    - SBOM component linkage
    - Risk assessment scoring
    - EOL status calculation

    **ICE Score: 9.0**
    - Impact: Critical (core equipment retrieval)
    - Complexity: Medium (multi-source aggregation)
    - Effort: Low (standard query patterns)
    """,
    tags=["Equipment"]
)
async def get_equipment(
    equipment_id: str,
    customer_id: str = Depends(get_current_customer_id),
    neo4j: Neo4jClient = Depends()
) -> Equipment:
    """
    Retrieve equipment by ID with full details

    **Path Parameters:**
    - `equipment_id`: Unique equipment identifier

    **Returns:**
    - Complete equipment object
    - Vendor information (if linked)
    - Vulnerability counts and risk scores
    - SBOM component associations
    - EOL status and timeline

    **Example Response:**
    ```json
    {
      "equipment_id": "eq_cisco_router_001",
      "name": "Core Router - Building A",
      "manufacturer": "Cisco",
      "model": "ISR4451-X",
      "status": "eol_warning",
      "vendor_name": "Cisco Systems",
      "days_until_eol": 180,
      "vulnerability_count": 3,
      "critical_vulnerability_count": 1,
      "risk_score": 7.5,
      "risk_level": "high"
    }
    ```
    """
    query = """
    MATCH (e:Equipment {equipment_id: $equipment_id, customer_id: $customer_id})
    OPTIONAL MATCH (e)-[:SUPPLIED_BY]->(v:Vendor)
    OPTIONAL MATCH (e)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)
    OPTIONAL MATCH (e)-[:RUNS_COMPONENT]->(comp:SBOMComponent)

    WITH e, v,
         count(DISTINCT vuln) as vuln_count,
         count(DISTINCT CASE WHEN vuln.severity = 'CRITICAL' THEN vuln END) as critical_count,
         count(DISTINCT CASE WHEN vuln.severity = 'HIGH' THEN vuln END) as high_count,
         collect(DISTINCT comp.component_id) as sbom_ids,
         count(DISTINCT comp) as software_count

    RETURN e,
           v.vendor_id as vendor_id,
           v.name as vendor_name,
           vuln_count,
           critical_count,
           high_count,
           sbom_ids,
           software_count
    """

    result = await neo4j.execute_query(query, {
        'equipment_id': equipment_id,
        'customer_id': customer_id
    })

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Equipment {equipment_id} not found"
        )

    record = result[0]
    e = record['e']

    # Parse dates
    eol_date = date.fromisoformat(e['eol_date']) if e.get('eol_date') else None
    eos_date = date.fromisoformat(e['eos_date']) if e.get('eos_date') else None
    purchase_date = date.fromisoformat(e['purchase_date']) if e.get('purchase_date') else None
    warranty_expiry = date.fromisoformat(e['warranty_expiry']) if e.get('warranty_expiry') else None

    # Calculate current EOL status
    days_until_eol = e.get('days_until_eol')
    if eol_date:
        days_until_eol = (eol_date - date.today()).days

    days_until_eos = e.get('days_until_eos')
    if eos_date:
        days_until_eos = (eos_date - date.today()).days

    # Get vulnerability counts
    vuln_count = record['vuln_count']
    critical_count = record['critical_count']
    high_count = record['high_count']

    # Calculate risk score
    risk_score, risk_level = calculate_risk_score(
        vuln_count,
        critical_count,
        high_count,
        days_until_eol,
        e.get('status', EquipmentStatus.ACTIVE.value)
    )

    # Build equipment object
    equipment = Equipment(
        equipment_id=e['equipment_id'],
        name=e['name'],
        equipment_type=e['equipment_type'],
        manufacturer=e['manufacturer'],
        model=e['model'],
        serial_number=e.get('serial_number'),
        asset_tag=e.get('asset_tag'),
        location=e.get('location'),
        sector=e['sector'],
        vendor_id=record.get('vendor_id'),
        vendor_name=record.get('vendor_name'),
        status=EquipmentStatus(e.get('status', EquipmentStatus.ACTIVE.value)),
        purchase_date=purchase_date,
        warranty_expiry=warranty_expiry,
        eol_date=eol_date,
        eos_date=eos_date,
        firmware_version=e.get('firmware_version'),
        os_version=e.get('os_version'),
        ip_address=e.get('ip_address'),
        mac_address=e.get('mac_address'),
        description=e.get('description'),
        tags=e.get('tags', []),
        metadata=e.get('metadata', {}),
        vulnerability_count=vuln_count,
        critical_vulnerability_count=critical_count,
        high_vulnerability_count=high_count,
        risk_score=risk_score,
        risk_level=risk_level,
        days_until_eol=days_until_eol,
        days_until_eos=days_until_eos,
        eol_risk_level=RiskLevel(e.get('eol_risk_level', RiskLevel.NONE.value)),
        sbom_component_ids=record.get('sbom_ids', []),
        software_count=record.get('software_count', 0),
        customer_id=e['customer_id'],
        created_at=datetime.fromisoformat(e['created_at']),
        updated_at=datetime.fromisoformat(e['updated_at']),
        last_scan_date=datetime.fromisoformat(e['last_scan_date']) if e.get('last_scan_date') else None,
        last_seen_online=datetime.fromisoformat(e['last_seen_online']) if e.get('last_seen_online') else None
    )

    return equipment


@router.get(
    "",
    response_model=List[Equipment],
    summary="List Equipment",
    description="List equipment with filtering and pagination",
    tags=["Equipment"]
)
async def list_equipment(
    customer_id: str = Depends(get_current_customer_id),
    neo4j: Neo4jClient = Depends(),
    equipment_type: Optional[str] = Query(None, description="Filter by equipment type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    sector: Optional[str] = Query(None, description="Filter by sector"),
    manufacturer: Optional[str] = Query(None, description="Filter by manufacturer"),
    vendor_id: Optional[str] = Query(None, description="Filter by vendor"),
    min_risk_score: Optional[float] = Query(None, ge=0.0, le=10.0, description="Minimum risk score"),
    eol_within_days: Optional[int] = Query(None, ge=0, description="EOL within N days"),
    skip: int = Query(0, ge=0, description="Skip N records"),
    limit: int = Query(100, ge=1, le=1000, description="Limit results")
) -> List[Equipment]:
    """
    List equipment with optional filters

    **Query Parameters:**
    - Filtering: type, status, sector, manufacturer, vendor
    - Risk filtering: min_risk_score, eol_within_days
    - Pagination: skip, limit

    **Returns:**
    - List of equipment matching filters
    - Sorted by risk score descending
    """
    # Build dynamic WHERE clause
    where_clauses = ["e.customer_id = $customer_id"]
    params = {'customer_id': customer_id, 'skip': skip, 'limit': limit}

    if equipment_type:
        where_clauses.append("e.equipment_type = $equipment_type")
        params['equipment_type'] = equipment_type

    if status:
        where_clauses.append("e.status = $status")
        params['status'] = status

    if sector:
        where_clauses.append("e.sector = $sector")
        params['sector'] = sector

    if manufacturer:
        where_clauses.append("e.manufacturer = $manufacturer")
        params['manufacturer'] = manufacturer

    if vendor_id:
        where_clauses.append("EXISTS((e)-[:SUPPLIED_BY]->(:Vendor {vendor_id: $vendor_id}))")
        params['vendor_id'] = vendor_id

    if eol_within_days is not None:
        where_clauses.append("e.days_until_eol <= $eol_within_days")
        params['eol_within_days'] = eol_within_days

    where_clause = " AND ".join(where_clauses)

    query = f"""
    MATCH (e:Equipment)
    WHERE {where_clause}
    OPTIONAL MATCH (e)-[:SUPPLIED_BY]->(v:Vendor)
    OPTIONAL MATCH (e)-[:HAS_VULNERABILITY]->(vuln:Vulnerability)

    WITH e, v,
         count(DISTINCT vuln) as vuln_count,
         count(DISTINCT CASE WHEN vuln.severity = 'CRITICAL' THEN vuln END) as critical_count,
         count(DISTINCT CASE WHEN vuln.severity = 'HIGH' THEN vuln END) as high_count

    // Apply risk score filter if specified
    {"WHERE vuln_count * 3.0 + critical_count * 1.5 >= $min_risk_score" if min_risk_score else ""}

    RETURN e, v.vendor_id as vendor_id, v.name as vendor_name,
           vuln_count, critical_count, high_count
    ORDER BY critical_count DESC, vuln_count DESC, e.days_until_eol ASC
    SKIP $skip
    LIMIT $limit
    """

    if min_risk_score:
        params['min_risk_score'] = min_risk_score

    results = await neo4j.execute_query(query, params)

    equipment_list = []
    for record in results:
        e = record['e']

        # Calculate risk for each equipment
        risk_score, risk_level = calculate_risk_score(
            record['vuln_count'],
            record['critical_count'],
            record['high_count'],
            e.get('days_until_eol'),
            e.get('status', EquipmentStatus.ACTIVE.value)
        )

        equipment = Equipment(
            equipment_id=e['equipment_id'],
            name=e['name'],
            equipment_type=e['equipment_type'],
            manufacturer=e['manufacturer'],
            model=e['model'],
            sector=e['sector'],
            vendor_id=record.get('vendor_id'),
            vendor_name=record.get('vendor_name'),
            status=EquipmentStatus(e.get('status', EquipmentStatus.ACTIVE.value)),
            eol_date=date.fromisoformat(e['eol_date']) if e.get('eol_date') else None,
            days_until_eol=e.get('days_until_eol'),
            vulnerability_count=record['vuln_count'],
            critical_vulnerability_count=record['critical_count'],
            high_vulnerability_count=record['high_count'],
            risk_score=risk_score,
            risk_level=risk_level,
            customer_id=e['customer_id'],
            created_at=datetime.fromisoformat(e['created_at']),
            updated_at=datetime.fromisoformat(e['updated_at'])
        )
        equipment_list.append(equipment)

    return equipment_list
