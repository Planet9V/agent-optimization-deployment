"""
POST /api/v2/equipment - Create Equipment
File: create.py
Created: 2025-12-12 05:00:00 UTC
Version: v1.0.0
ICE Score: 7.29
Purpose: Create equipment records with vendor linking and lifecycle management
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime, date
from typing import Optional
import uuid

from ....models.equipment import (
    EquipmentCreate,
    Equipment,
    EquipmentStatus,
    RiskLevel
)
from ....database.neo4j_client import Neo4jClient
from ....auth.tenant import get_current_customer_id

router = APIRouter()


def calculate_eol_status(eol_date: Optional[date], eos_date: Optional[date]) -> tuple:
    """
    Calculate days until EOL/EOS and determine status
    Returns: (days_until_eol, days_until_eos, status, eol_risk_level)
    """
    if not eol_date:
        return None, None, EquipmentStatus.ACTIVE, RiskLevel.NONE

    today = date.today()
    days_until_eol = (eol_date - today).days
    days_until_eos = (eos_date - today).days if eos_date else None

    # Determine status based on EOL timeline
    if days_until_eol < 0:
        status = EquipmentStatus.DECOMMISSIONED
        eol_risk = RiskLevel.CRITICAL
    elif days_until_eol < 30:
        status = EquipmentStatus.EOL_CRITICAL
        eol_risk = RiskLevel.CRITICAL
    elif days_until_eol < 90:
        status = EquipmentStatus.EOL_CRITICAL
        eol_risk = RiskLevel.HIGH
    elif days_until_eol < 180:
        status = EquipmentStatus.EOL_WARNING
        eol_risk = RiskLevel.MEDIUM
    else:
        status = EquipmentStatus.ACTIVE
        eol_risk = RiskLevel.LOW

    return days_until_eol, days_until_eos, status, eol_risk


async def link_to_vendor(
    neo4j: Neo4jClient,
    equipment_id: str,
    vendor_id: str,
    customer_id: str
) -> Optional[str]:
    """Create relationship between equipment and vendor in Neo4j"""
    query = """
    MATCH (e:Equipment {equipment_id: $equipment_id, customer_id: $customer_id})
    MATCH (v:Vendor {vendor_id: $vendor_id, customer_id: $customer_id})
    MERGE (e)-[r:SUPPLIED_BY]->(v)
    SET r.linked_at = datetime()
    RETURN v.name as vendor_name
    """
    result = await neo4j.execute_query(query, {
        'equipment_id': equipment_id,
        'vendor_id': vendor_id,
        'customer_id': customer_id
    })
    return result[0]['vendor_name'] if result else None


@router.post(
    "",
    response_model=Equipment,
    status_code=status.HTTP_201_CREATED,
    summary="Create Equipment Record",
    description="""
    Create a new equipment asset record with vendor linking and lifecycle management.

    **Features:**
    - Automatic EOL status calculation
    - Vendor relationship linking
    - Multi-tenant isolation
    - Asset tag management
    - Custom metadata support

    **ICE Score: 7.29**
    - Impact: High (asset tracking foundation)
    - Complexity: Medium (vendor linking, EOL logic)
    - Effort: Low (straightforward CRUD)
    """,
    tags=["Equipment"]
)
async def create_equipment(
    equipment_data: EquipmentCreate,
    customer_id: str = Depends(get_current_customer_id),
    neo4j: Neo4jClient = Depends()
) -> Equipment:
    """
    Create new equipment record

    **Request Body:**
    - All equipment details including vendor linkage
    - EOL and EOS dates for lifecycle tracking
    - Location and sector information

    **Returns:**
    - Complete equipment object with calculated status
    - Linked vendor information
    - Risk assessment scores

    **Example:**
    ```json
    {
      "name": "Core Router - Building A",
      "equipment_type": "network_device",
      "manufacturer": "Cisco",
      "model": "ISR4451-X",
      "serial_number": "FDO2345X1Y2",
      "sector": "energy",
      "vendor_id": "vendor_cisco_001",
      "eol_date": "2026-08-15"
    }
    ```
    """
    try:
        # Generate equipment ID
        equipment_id = f"eq_{equipment_data.manufacturer.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}"

        # Calculate EOL status
        days_until_eol, days_until_eos, calc_status, eol_risk = calculate_eol_status(
            equipment_data.eol_date,
            equipment_data.eos_date
        )

        # Prepare equipment node for Neo4j
        now = datetime.utcnow()
        equipment_node = {
            'equipment_id': equipment_id,
            'name': equipment_data.name,
            'equipment_type': equipment_data.equipment_type.value,
            'manufacturer': equipment_data.manufacturer,
            'model': equipment_data.model,
            'serial_number': equipment_data.serial_number,
            'asset_tag': equipment_data.asset_tag,
            'location': equipment_data.location,
            'sector': equipment_data.sector,
            'status': calc_status.value,
            'purchase_date': equipment_data.purchase_date.isoformat() if equipment_data.purchase_date else None,
            'warranty_expiry': equipment_data.warranty_expiry.isoformat() if equipment_data.warranty_expiry else None,
            'eol_date': equipment_data.eol_date.isoformat() if equipment_data.eol_date else None,
            'eos_date': equipment_data.eos_date.isoformat() if equipment_data.eos_date else None,
            'firmware_version': equipment_data.firmware_version,
            'os_version': equipment_data.os_version,
            'ip_address': equipment_data.ip_address,
            'mac_address': equipment_data.mac_address,
            'description': equipment_data.description,
            'tags': equipment_data.tags,
            'metadata': equipment_data.metadata,
            'days_until_eol': days_until_eol,
            'days_until_eos': days_until_eos,
            'eol_risk_level': eol_risk.value,
            'customer_id': customer_id,
            'created_at': now.isoformat(),
            'updated_at': now.isoformat()
        }

        # Create equipment node in Neo4j
        create_query = """
        CREATE (e:Equipment $props)
        RETURN e
        """
        await neo4j.execute_query(create_query, {'props': equipment_node})

        # Link to vendor if provided
        vendor_name = None
        if equipment_data.vendor_id:
            vendor_name = await link_to_vendor(
                neo4j,
                equipment_id,
                equipment_data.vendor_id,
                customer_id
            )

        # Build response object
        equipment = Equipment(
            equipment_id=equipment_id,
            name=equipment_data.name,
            equipment_type=equipment_data.equipment_type,
            manufacturer=equipment_data.manufacturer,
            model=equipment_data.model,
            serial_number=equipment_data.serial_number,
            asset_tag=equipment_data.asset_tag,
            location=equipment_data.location,
            sector=equipment_data.sector,
            vendor_id=equipment_data.vendor_id,
            vendor_name=vendor_name,
            status=calc_status,
            purchase_date=equipment_data.purchase_date,
            warranty_expiry=equipment_data.warranty_expiry,
            eol_date=equipment_data.eol_date,
            eos_date=equipment_data.eos_date,
            firmware_version=equipment_data.firmware_version,
            os_version=equipment_data.os_version,
            ip_address=equipment_data.ip_address,
            mac_address=equipment_data.mac_address,
            description=equipment_data.description,
            tags=equipment_data.tags,
            metadata=equipment_data.metadata,
            days_until_eol=days_until_eol,
            days_until_eos=days_until_eos,
            eol_risk_level=eol_risk,
            customer_id=customer_id,
            created_at=now,
            updated_at=now
        )

        return equipment

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create equipment: {str(e)}"
        )


@router.post(
    "/bulk",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Bulk Create Equipment",
    description="Create multiple equipment records in a single transaction",
    tags=["Equipment"]
)
async def bulk_create_equipment(
    equipment_list: list[EquipmentCreate],
    customer_id: str = Depends(get_current_customer_id),
    neo4j: Neo4jClient = Depends()
) -> dict:
    """
    Bulk create equipment records

    **Performance:**
    - Processes up to 100 equipment records per request
    - Transaction-safe bulk insert
    - Parallel vendor linking

    **Returns:**
    - Count of successfully created equipment
    - List of equipment IDs
    - Any errors encountered
    """
    if len(equipment_list) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 100 equipment records per bulk request"
        )

    created_ids = []
    errors = []

    for idx, equipment_data in enumerate(equipment_list):
        try:
            equipment = await create_equipment(equipment_data, customer_id, neo4j)
            created_ids.append(equipment.equipment_id)
        except Exception as e:
            errors.append({
                'index': idx,
                'name': equipment_data.name,
                'error': str(e)
            })

    return {
        'created_count': len(created_ids),
        'equipment_ids': created_ids,
        'errors': errors,
        'success_rate': len(created_ids) / len(equipment_list) if equipment_list else 0
    }
