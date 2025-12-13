"""
Equipment Models for AEON Cybersecurity Platform
File: equipment.py
Created: 2025-12-12 05:00:00 UTC
Version: v1.0.0
Purpose: Equipment asset management data models
Status: ACTIVE
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, validator


class EquipmentStatus(str, Enum):
    """Equipment lifecycle status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    DECOMMISSIONED = "decommissioned"
    PENDING_DEPLOYMENT = "pending_deployment"
    EOL_WARNING = "eol_warning"
    EOL_CRITICAL = "eol_critical"


class EquipmentType(str, Enum):
    """Equipment type classification"""
    NETWORK_DEVICE = "network_device"
    SERVER = "server"
    WORKSTATION = "workstation"
    MOBILE_DEVICE = "mobile_device"
    IOT_DEVICE = "iot_device"
    SECURITY_APPLIANCE = "security_appliance"
    STORAGE_DEVICE = "storage_device"
    INFRASTRUCTURE = "infrastructure"


class RiskLevel(str, Enum):
    """Equipment risk assessment level"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class EquipmentBase(BaseModel):
    """Base equipment attributes"""
    name: str = Field(..., min_length=1, max_length=200, description="Equipment name/identifier")
    equipment_type: EquipmentType = Field(..., description="Type of equipment")
    manufacturer: str = Field(..., min_length=1, max_length=100, description="Equipment manufacturer")
    model: str = Field(..., min_length=1, max_length=100, description="Equipment model")
    serial_number: Optional[str] = Field(None, max_length=100, description="Serial number")
    asset_tag: Optional[str] = Field(None, max_length=50, description="Asset tag identifier")
    location: Optional[str] = Field(None, max_length=200, description="Physical location")
    sector: str = Field(..., description="Industry sector (e.g., energy, finance, healthcare)")

    class Config:
        use_enum_values = True


class EquipmentCreate(EquipmentBase):
    """Equipment creation model"""
    vendor_id: Optional[str] = Field(None, description="Linked vendor ID")
    purchase_date: Optional[date] = Field(None, description="Purchase date")
    warranty_expiry: Optional[date] = Field(None, description="Warranty expiration date")
    eol_date: Optional[date] = Field(None, description="End-of-life date")
    eos_date: Optional[date] = Field(None, description="End-of-support date")
    firmware_version: Optional[str] = Field(None, max_length=50, description="Current firmware version")
    os_version: Optional[str] = Field(None, max_length=100, description="Operating system version")
    ip_address: Optional[str] = Field(None, max_length=45, description="IP address (IPv4/IPv6)")
    mac_address: Optional[str] = Field(None, max_length=17, description="MAC address")
    description: Optional[str] = Field(None, max_length=1000, description="Equipment description")
    tags: List[str] = Field(default_factory=list, description="Custom tags")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    customer_id: str = Field(..., description="Multi-tenant customer ID")


class Equipment(EquipmentBase):
    """Complete equipment model"""
    equipment_id: str = Field(..., description="Unique equipment identifier")
    vendor_id: Optional[str] = None
    vendor_name: Optional[str] = None
    status: EquipmentStatus = Field(default=EquipmentStatus.ACTIVE)
    purchase_date: Optional[date] = None
    warranty_expiry: Optional[date] = None
    eol_date: Optional[date] = None
    eos_date: Optional[date] = None
    firmware_version: Optional[str] = None
    os_version: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Risk and vulnerability data
    vulnerability_count: int = Field(default=0, description="Number of associated vulnerabilities")
    critical_vulnerability_count: int = Field(default=0, description="Critical vulnerabilities")
    high_vulnerability_count: int = Field(default=0, description="High severity vulnerabilities")
    risk_score: float = Field(default=0.0, ge=0.0, le=10.0, description="Overall risk score (0-10)")
    risk_level: RiskLevel = Field(default=RiskLevel.NONE)

    # EOL status
    days_until_eol: Optional[int] = Field(None, description="Days until end-of-life")
    days_until_eos: Optional[int] = Field(None, description="Days until end-of-support")
    eol_risk_level: RiskLevel = Field(default=RiskLevel.NONE)

    # SBOM linkage
    sbom_component_ids: List[str] = Field(default_factory=list, description="Linked SBOM components")
    software_count: int = Field(default=0, description="Number of installed software components")

    # Audit fields
    customer_id: str
    created_at: datetime
    updated_at: datetime
    last_scan_date: Optional[datetime] = None
    last_seen_online: Optional[datetime] = None

    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "equipment_id": "eq_cisco_router_001",
                "name": "Core Router - Building A",
                "equipment_type": "network_device",
                "manufacturer": "Cisco",
                "model": "ISR4451-X",
                "serial_number": "FDO2345X1Y2",
                "asset_tag": "NET-RTR-001",
                "location": "Data Center A - Rack 12",
                "sector": "energy",
                "vendor_id": "vendor_cisco_001",
                "vendor_name": "Cisco Systems",
                "status": "active",
                "eol_date": "2026-08-15",
                "days_until_eol": 610,
                "vulnerability_count": 3,
                "critical_vulnerability_count": 1,
                "risk_score": 7.5,
                "risk_level": "high",
                "customer_id": "customer_001"
            }
        }


class EquipmentUpdate(BaseModel):
    """Equipment update model - all fields optional"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    equipment_type: Optional[EquipmentType] = None
    manufacturer: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    serial_number: Optional[str] = Field(None, max_length=100)
    asset_tag: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=200)
    sector: Optional[str] = None
    vendor_id: Optional[str] = None
    status: Optional[EquipmentStatus] = None
    purchase_date: Optional[date] = None
    warranty_expiry: Optional[date] = None
    eol_date: Optional[date] = None
    eos_date: Optional[date] = None
    firmware_version: Optional[str] = Field(None, max_length=50)
    os_version: Optional[str] = Field(None, max_length=100)
    ip_address: Optional[str] = Field(None, max_length=45)
    mac_address: Optional[str] = Field(None, max_length=17)
    description: Optional[str] = Field(None, max_length=1000)
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        use_enum_values = True


class EquipmentSummary(BaseModel):
    """Equipment statistics summary"""
    total_equipment: int = Field(..., description="Total equipment count")
    by_status: Dict[str, int] = Field(..., description="Equipment count by status")
    by_type: Dict[str, int] = Field(..., description="Equipment count by type")
    by_sector: Dict[str, int] = Field(..., description="Equipment count by sector")
    by_vendor: Dict[str, int] = Field(..., description="Equipment count by vendor")
    by_risk_level: Dict[str, int] = Field(..., description="Equipment count by risk level")

    # EOL statistics
    total_eol_approaching: int = Field(default=0, description="Equipment approaching EOL (<180 days)")
    total_eol_critical: int = Field(default=0, description="Equipment in critical EOL period (<90 days)")
    total_past_eol: int = Field(default=0, description="Equipment past EOL date")

    # Vulnerability statistics
    total_with_vulnerabilities: int = Field(default=0)
    total_with_critical_vulnerabilities: int = Field(default=0)
    avg_risk_score: float = Field(default=0.0, description="Average risk score across all equipment")

    # Maintenance statistics
    total_active: int = Field(default=0)
    total_maintenance: int = Field(default=0)
    total_decommissioned: int = Field(default=0)

    customer_id: str
    generated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
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
                    "workstation": 400,
                    "security_appliance": 100
                },
                "by_sector": {
                    "energy": 800,
                    "finance": 450
                },
                "total_eol_approaching": 125,
                "total_eol_critical": 25,
                "avg_risk_score": 4.2
            }
        }


class EOLEquipment(BaseModel):
    """Equipment EOL report entry"""
    equipment_id: str
    name: str
    equipment_type: EquipmentType
    manufacturer: str
    model: str
    sector: str
    vendor_name: Optional[str] = None
    eol_date: Optional[date]
    eos_date: Optional[date]
    days_until_eol: Optional[int]
    days_until_eos: Optional[int]
    status: EquipmentStatus
    eol_risk_level: RiskLevel
    vulnerability_count: int = 0
    critical_vulnerability_count: int = 0
    risk_score: float = 0.0
    replacement_available: bool = Field(default=False, description="Replacement model available")
    migration_plan_exists: bool = Field(default=False, description="Migration plan documented")
    business_impact: str = Field(default="unknown", description="Business impact level")
    location: Optional[str] = None

    class Config:
        use_enum_values = True


class EOLReport(BaseModel):
    """Equipment EOL analysis report"""
    report_id: str
    customer_id: str
    generated_at: datetime

    # Summary statistics
    total_equipment_reviewed: int
    total_eol_approaching: int = Field(..., description="EOL within 180 days")
    total_eol_critical: int = Field(..., description="EOL within 90 days")
    total_past_eol: int = Field(..., description="Past EOL date")
    total_past_eos: int = Field(..., description="Past end-of-support")

    # Risk breakdown
    critical_risk_count: int = 0
    high_risk_count: int = 0
    medium_risk_count: int = 0
    low_risk_count: int = 0

    # Detailed equipment list
    equipment: List[EOLEquipment] = Field(..., description="Equipment approaching or past EOL")

    # By sector analysis
    by_sector: Dict[str, int] = Field(default_factory=dict)
    by_type: Dict[str, int] = Field(default_factory=dict)
    by_vendor: Dict[str, int] = Field(default_factory=dict)

    # Recommendations
    immediate_action_required: int = Field(default=0, description="Equipment requiring immediate action")
    planning_required: int = Field(default=0, description="Equipment requiring planning")

    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "eol_report_2025_12_12",
                "total_equipment_reviewed": 1250,
                "total_eol_approaching": 125,
                "total_eol_critical": 25,
                "total_past_eol": 15,
                "critical_risk_count": 40,
                "immediate_action_required": 40,
                "planning_required": 85
            }
        }


class EquipmentFilter(BaseModel):
    """Equipment filtering parameters"""
    equipment_type: Optional[EquipmentType] = None
    status: Optional[EquipmentStatus] = None
    sector: Optional[str] = None
    vendor_id: Optional[str] = None
    manufacturer: Optional[str] = None
    risk_level: Optional[RiskLevel] = None
    min_risk_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    max_risk_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    has_vulnerabilities: Optional[bool] = None
    eol_within_days: Optional[int] = Field(None, ge=0, description="Filter equipment with EOL within N days")
    tags: Optional[List[str]] = None
    location: Optional[str] = None

    class Config:
        use_enum_values = True
