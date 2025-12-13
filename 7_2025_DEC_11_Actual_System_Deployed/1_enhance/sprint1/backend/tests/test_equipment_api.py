"""
Equipment API Test Suite
File: test_equipment_api.py
Created: 2025-12-12 05:00:00 UTC
Version: v1.0.0
Purpose: Comprehensive tests for Equipment Core APIs
"""

import pytest
from datetime import datetime, date, timedelta
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch

from ..models.equipment import (
    EquipmentCreate,
    Equipment,
    EquipmentStatus,
    EquipmentType,
    RiskLevel
)


# Test fixtures
@pytest.fixture
def sample_equipment_create():
    """Sample equipment creation data"""
    return {
        "name": "Core Router - Building A",
        "equipment_type": "network_device",
        "manufacturer": "Cisco",
        "model": "ISR4451-X",
        "serial_number": "FDO2345X1Y2",
        "asset_tag": "NET-RTR-001",
        "location": "Data Center A - Rack 12",
        "sector": "energy",
        "vendor_id": "vendor_cisco_001",
        "eol_date": (date.today() + timedelta(days=120)).isoformat(),
        "eos_date": (date.today() + timedelta(days=150)).isoformat(),
        "firmware_version": "17.9.4",
        "ip_address": "10.0.1.1",
        "tags": ["critical", "core-network"],
        "customer_id": "customer_test_001"
    }


@pytest.fixture
def mock_neo4j_client():
    """Mock Neo4j client for testing"""
    client = Mock()
    client.execute_query = AsyncMock()
    return client


# POST /api/v2/equipment Tests
class TestCreateEquipment:
    """Test equipment creation endpoint"""

    @pytest.mark.asyncio
    async def test_create_equipment_success(self, sample_equipment_create, mock_neo4j_client):
        """Test successful equipment creation"""
        mock_neo4j_client.execute_query.return_value = [
            {'e': sample_equipment_create}
        ]

        # Import and test
        from ..api.v2.equipment.create import create_equipment

        result = await create_equipment(
            equipment_data=EquipmentCreate(**sample_equipment_create),
            customer_id="customer_test_001",
            neo4j=mock_neo4j_client
        )

        assert result.name == "Core Router - Building A"
        assert result.manufacturer == "Cisco"
        assert result.equipment_type == EquipmentType.NETWORK_DEVICE
        assert result.status in [EquipmentStatus.ACTIVE, EquipmentStatus.EOL_WARNING, EquipmentStatus.EOL_CRITICAL]
        assert result.days_until_eol is not None

    @pytest.mark.asyncio
    async def test_create_equipment_with_vendor_linking(self, sample_equipment_create, mock_neo4j_client):
        """Test equipment creation with vendor relationship"""
        mock_neo4j_client.execute_query.side_effect = [
            [{'e': sample_equipment_create}],  # Equipment creation
            [{'vendor_name': 'Cisco Systems'}]  # Vendor linking
        ]

        from ..api.v2.equipment.create import create_equipment

        result = await create_equipment(
            equipment_data=EquipmentCreate(**sample_equipment_create),
            customer_id="customer_test_001",
            neo4j=mock_neo4j_client
        )

        assert result.vendor_id == "vendor_cisco_001"
        assert result.vendor_name == "Cisco Systems"

    @pytest.mark.asyncio
    async def test_eol_status_calculation_critical(self, sample_equipment_create, mock_neo4j_client):
        """Test EOL status calculation for critical timeline"""
        # Set EOL to 60 days from now (critical)
        sample_equipment_create['eol_date'] = (date.today() + timedelta(days=60)).isoformat()

        from ..api.v2.equipment.create import calculate_eol_status

        days_eol, days_eos, status, risk = calculate_eol_status(
            date.fromisoformat(sample_equipment_create['eol_date']),
            None
        )

        assert days_eol == 60
        assert status == EquipmentStatus.EOL_CRITICAL
        assert risk in [RiskLevel.HIGH, RiskLevel.CRITICAL]

    @pytest.mark.asyncio
    async def test_eol_status_calculation_past_eol(self, sample_equipment_create, mock_neo4j_client):
        """Test EOL status for equipment past EOL date"""
        # Set EOL to 30 days ago
        sample_equipment_create['eol_date'] = (date.today() - timedelta(days=30)).isoformat()

        from ..api.v2.equipment.create import calculate_eol_status

        days_eol, days_eos, status, risk = calculate_eol_status(
            date.fromisoformat(sample_equipment_create['eol_date']),
            None
        )

        assert days_eol == -30
        assert status == EquipmentStatus.DECOMMISSIONED
        assert risk == RiskLevel.CRITICAL

    @pytest.mark.asyncio
    async def test_bulk_create_equipment(self, sample_equipment_create, mock_neo4j_client):
        """Test bulk equipment creation"""
        equipment_list = [
            EquipmentCreate(**{**sample_equipment_create, 'name': f'Router-{i}'})
            for i in range(5)
        ]

        from ..api.v2.equipment.create import bulk_create_equipment

        # Mock successful creation
        mock_neo4j_client.execute_query.return_value = [{'e': sample_equipment_create}]

        result = await bulk_create_equipment(
            equipment_list=equipment_list,
            customer_id="customer_test_001",
            neo4j=mock_neo4j_client
        )

        assert result['created_count'] == 5
        assert len(result['equipment_ids']) == 5
        assert result['success_rate'] == 1.0


# GET /api/v2/equipment/{equipment_id} Tests
class TestRetrieveEquipment:
    """Test equipment retrieval endpoint"""

    @pytest.mark.asyncio
    async def test_get_equipment_success(self, mock_neo4j_client):
        """Test successful equipment retrieval"""
        mock_data = {
            'e': {
                'equipment_id': 'eq_test_001',
                'name': 'Test Router',
                'equipment_type': 'network_device',
                'manufacturer': 'Cisco',
                'model': 'ISR4451',
                'sector': 'energy',
                'status': 'active',
                'eol_date': (date.today() + timedelta(days=365)).isoformat(),
                'days_until_eol': 365,
                'customer_id': 'customer_test_001',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            },
            'vendor_name': 'Cisco Systems',
            'vuln_count': 2,
            'critical_count': 1,
            'high_count': 1,
            'sbom_ids': ['sbom_001', 'sbom_002'],
            'software_count': 15
        }

        mock_neo4j_client.execute_query.return_value = [mock_data]

        from ..api.v2.equipment.retrieve import get_equipment

        result = await get_equipment(
            equipment_id='eq_test_001',
            customer_id='customer_test_001',
            neo4j=mock_neo4j_client
        )

        assert result.equipment_id == 'eq_test_001'
        assert result.name == 'Test Router'
        assert result.vendor_name == 'Cisco Systems'
        assert result.vulnerability_count == 2
        assert result.critical_vulnerability_count == 1
        assert result.risk_score > 0

    @pytest.mark.asyncio
    async def test_get_equipment_not_found(self, mock_neo4j_client):
        """Test equipment not found scenario"""
        mock_neo4j_client.execute_query.return_value = []

        from ..api.v2.equipment.retrieve import get_equipment
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as exc_info:
            await get_equipment(
                equipment_id='nonexistent',
                customer_id='customer_test_001',
                neo4j=mock_neo4j_client
            )

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_risk_score_calculation(self):
        """Test risk score calculation logic"""
        from ..api.v2.equipment.retrieve import calculate_risk_score

        # High risk: critical vulnerabilities + near EOL
        risk_score, risk_level = calculate_risk_score(
            vulnerability_count=5,
            critical_vuln_count=2,
            high_vuln_count=3,
            days_until_eol=45,
            status='eol_critical'
        )

        assert risk_score >= 8.0  # Should be high risk
        assert risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]

        # Low risk: no vulnerabilities, far from EOL
        risk_score, risk_level = calculate_risk_score(
            vulnerability_count=0,
            critical_vuln_count=0,
            high_vuln_count=0,
            days_until_eol=500,
            status='active'
        )

        assert risk_score < 2.0
        assert risk_level in [RiskLevel.NONE, RiskLevel.LOW]


# GET /api/v2/equipment/summary Tests
class TestEquipmentSummary:
    """Test equipment summary statistics endpoint"""

    @pytest.mark.asyncio
    async def test_get_summary_success(self, mock_neo4j_client):
        """Test successful summary generation"""
        mock_summary = {
            'total_equipment': 1250,
            'active_count': 1000,
            'maintenance_count': 100,
            'decommissioned_count': 50,
            'inactive_count': 50,
            'pending_count': 25,
            'eol_warning_count': 75,
            'eol_critical_count': 25,
            'network_device_count': 400,
            'server_count': 350,
            'workstation_count': 500,
            'mobile_device_count': 0,
            'iot_device_count': 0,
            'security_appliance_count': 0,
            'storage_device_count': 0,
            'infrastructure_count': 0,
            'eol_approaching': 100,
            'eol_critical': 25,
            'past_eol': 15,
            'with_vulnerabilities': 300,
            'with_critical_vulnerabilities': 50,
            'risk_critical': 40,
            'risk_high': 100,
            'risk_medium': 200,
            'risk_low': 300,
            'risk_none': 610,
            'avg_risk_score': 3.5,
            'equipment_details': [
                {'sector': 'energy', 'vendor_name': 'Cisco'},
                {'sector': 'finance', 'vendor_name': 'Juniper'}
            ]
        }

        mock_neo4j_client.execute_query.return_value = [mock_summary]

        from ..api.v2.equipment.summary import get_equipment_summary

        result = await get_equipment_summary(
            customer_id='customer_test_001',
            neo4j=mock_neo4j_client
        )

        assert result.total_equipment == 1250
        assert result.total_active == 1000
        assert result.avg_risk_score == 3.5
        assert 'energy' in result.by_sector or 'finance' in result.by_sector

    @pytest.mark.asyncio
    async def test_get_sector_summary(self, mock_neo4j_client):
        """Test sector-specific summary"""
        mock_summary = {
            'total_equipment': 800,
            'active_count': 700,
            'maintenance_count': 50,
            'decommissioned_count': 50,
            'eol_approaching': 60,
            'eol_critical': 20,
            'with_vulnerabilities': 200,
            'with_critical_vulnerabilities': 30,
            'avg_risk_score': 4.2
        }

        mock_neo4j_client.execute_query.return_value = [mock_summary]

        from ..api.v2.equipment.summary import get_sector_equipment_summary

        result = await get_sector_equipment_summary(
            sector='energy',
            customer_id='customer_test_001',
            neo4j=mock_neo4j_client
        )

        assert result.total_equipment == 800
        assert 'energy' in result.by_sector


# GET /api/v2/equipment/eol-report Tests
class TestEOLReport:
    """Test EOL report generation endpoint"""

    @pytest.mark.asyncio
    async def test_generate_eol_report(self, mock_neo4j_client):
        """Test EOL report generation"""
        mock_equipment = [
            {
                'e': {
                    'equipment_id': 'eq_eol_001',
                    'name': 'Legacy Router',
                    'equipment_type': 'network_device',
                    'manufacturer': 'Cisco',
                    'model': 'ISR2951',
                    'sector': 'energy',
                    'status': 'eol_critical',
                    'eol_date': (date.today() + timedelta(days=45)).isoformat(),
                    'metadata': {}
                },
                'vendor_name': 'Cisco Systems',
                'vuln_count': 5,
                'critical_count': 2,
                'current_days_until_eol': 45,
                'current_days_until_eos': 30
            }
        ]

        mock_neo4j_client.execute_query.return_value = mock_equipment

        from ..api.v2.equipment.eol_report import get_eol_report

        result = await get_eol_report(
            customer_id='customer_test_001',
            neo4j=mock_neo4j_client
        )

        assert result.total_equipment_reviewed > 0
        assert result.total_eol_critical > 0
        assert len(result.equipment) > 0
        assert result.immediate_action_required >= 0

    @pytest.mark.asyncio
    async def test_eol_risk_assessment(self):
        """Test EOL risk assessment logic"""
        from ..api.v2.equipment.eol_report import assess_eol_risk

        # Critical risk: past EOL + vulnerabilities + no plan
        risk_level, impact, immediate = assess_eol_risk(
            days_until_eol=-30,
            days_until_eos=-60,
            vulnerability_count=10,
            critical_vuln_count=3,
            has_replacement=False,
            has_migration_plan=False
        )

        assert risk_level == RiskLevel.CRITICAL
        assert immediate is True

        # Low risk: far from EOL + replacement ready
        risk_level, impact, immediate = assess_eol_risk(
            days_until_eol=300,
            days_until_eos=360,
            vulnerability_count=1,
            critical_vuln_count=0,
            has_replacement=True,
            has_migration_plan=True
        )

        assert risk_level in [RiskLevel.NONE, RiskLevel.LOW]
        assert immediate is False

    @pytest.mark.asyncio
    async def test_eol_report_filtering(self, mock_neo4j_client):
        """Test EOL report with filters"""
        mock_neo4j_client.execute_query.return_value = []

        from ..api.v2.equipment.eol_report import get_eol_report

        result = await get_eol_report(
            customer_id='customer_test_001',
            neo4j=mock_neo4j_client,
            eol_threshold_days=90,
            sector='energy',
            equipment_type='network_device',
            min_risk_level='high'
        )

        # Should handle empty result gracefully
        assert result.total_equipment_reviewed == 0


# Integration Tests
class TestEquipmentAPIIntegration:
    """Integration tests for equipment API workflows"""

    @pytest.mark.asyncio
    async def test_full_equipment_lifecycle(self, sample_equipment_create, mock_neo4j_client):
        """Test complete equipment lifecycle: create → retrieve → update → report"""
        # 1. Create equipment
        from ..api.v2.equipment.create import create_equipment

        mock_neo4j_client.execute_query.return_value = [{'e': sample_equipment_create}]

        created = await create_equipment(
            equipment_data=EquipmentCreate(**sample_equipment_create),
            customer_id='customer_test_001',
            neo4j=mock_neo4j_client
        )

        equipment_id = created.equipment_id

        # 2. Retrieve equipment
        from ..api.v2.equipment.retrieve import get_equipment

        mock_neo4j_client.execute_query.return_value = [{
            'e': {**sample_equipment_create, 'equipment_id': equipment_id},
            'vuln_count': 0,
            'critical_count': 0
        }]

        retrieved = await get_equipment(
            equipment_id=equipment_id,
            customer_id='customer_test_001',
            neo4j=mock_neo4j_client
        )

        assert retrieved.equipment_id == equipment_id

    @pytest.mark.asyncio
    async def test_multi_tenant_isolation(self, sample_equipment_create, mock_neo4j_client):
        """Test multi-tenant data isolation"""
        from ..api.v2.equipment.retrieve import get_equipment
        from fastapi import HTTPException

        # Equipment exists for customer_001 but not customer_002
        mock_neo4j_client.execute_query.return_value = []

        with pytest.raises(HTTPException) as exc_info:
            await get_equipment(
                equipment_id='eq_test_001',
                customer_id='customer_002',  # Different customer
                neo4j=mock_neo4j_client
            )

        assert exc_info.value.status_code == 404


# Performance Tests
class TestEquipmentAPIPerformance:
    """Performance and load testing"""

    @pytest.mark.asyncio
    async def test_bulk_create_performance(self, sample_equipment_create, mock_neo4j_client):
        """Test bulk creation with maximum allowed records"""
        equipment_list = [
            EquipmentCreate(**{**sample_equipment_create, 'name': f'Equipment-{i}'})
            for i in range(100)  # Maximum allowed
        ]

        from ..api.v2.equipment.create import bulk_create_equipment

        mock_neo4j_client.execute_query.return_value = [{'e': sample_equipment_create}]

        start_time = datetime.utcnow()
        result = await bulk_create_equipment(
            equipment_list=equipment_list,
            customer_id='customer_test_001',
            neo4j=mock_neo4j_client
        )
        duration = (datetime.utcnow() - start_time).total_seconds()

        assert result['created_count'] == 100
        # Should complete in reasonable time even with 100 records
        assert duration < 30.0  # 30 seconds max


# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v', '--asyncio-mode=auto'])
