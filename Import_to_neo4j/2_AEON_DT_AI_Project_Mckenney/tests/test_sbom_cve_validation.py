"""
Test SBOM Agent CVE Database Validation
Validates that CVE correlation fails gracefully when database is unavailable
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.sbom_agent import SBOMAgent


class TestSBOMCVEValidation:
    """Test CVE database validation and graceful degradation"""

    def test_validate_cve_database_empty_config(self):
        """Test validation with empty CVE database configuration"""
        config = {'cve_database': {}}
        agent = SBOMAgent('test_sbom', config)

        result = agent.validate_cve_database()

        assert result is False, "Should return False for empty CVE database"

    def test_validate_cve_database_with_purl_index(self):
        """Test validation with populated PURL index"""
        config = {
            'cve_database': {
                'purl_index': {
                    'pkg:npm/express@4.17.1': ['CVE-2022-24999']
                }
            }
        }
        agent = SBOMAgent('test_sbom', config)

        result = agent.validate_cve_database()

        assert result is True, "Should return True with populated PURL index"

    def test_validate_cve_database_with_cpe_index(self):
        """Test validation with populated CPE index"""
        config = {
            'cve_database': {
                'cpe_index': {
                    'cpe:2.3:a:nodejs:node.js:14.17.0:*:*:*:*:*:*:*': ['CVE-2021-22930']
                }
            }
        }
        agent = SBOMAgent('test_sbom', config)

        result = agent.validate_cve_database()

        assert result is True, "Should return True with populated CPE index"

    def test_validate_cve_database_with_neo4j(self):
        """Test validation with Neo4j driver"""
        config = {
            'cve_database': {
                'purl_index': {'pkg:npm/test': ['CVE-2023-0001']}
            }
        }
        agent = SBOMAgent('test_sbom', config)

        # Mock Neo4j driver
        mock_driver = MagicMock()
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.single.return_value = {'count': 1500}
        mock_session.run.return_value = mock_result
        mock_driver.session.return_value.__enter__.return_value = mock_session

        agent.neo4j_driver = mock_driver

        result = agent.validate_cve_database()

        assert result is True, "Should validate with Neo4j containing CVEs"

    def test_validate_cve_database_neo4j_empty(self):
        """Test validation with empty Neo4j database"""
        config = {
            'cve_database': {
                'purl_index': {'pkg:npm/test': ['CVE-2023-0001']}
            }
        }
        agent = SBOMAgent('test_sbom', config)

        # Mock Neo4j driver with empty database
        mock_driver = MagicMock()
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.single.return_value = {'count': 0}
        mock_session.run.return_value = mock_result
        mock_driver.session.return_value.__enter__.return_value = mock_session

        agent.neo4j_driver = mock_driver

        result = agent.validate_cve_database()

        assert result is False, "Should return False for empty Neo4j CVE database"

    def test_correlate_cves_without_database(self):
        """Test CVE correlation gracefully fails without database"""
        config = {'cve_database': {}}
        agent = SBOMAgent('test_sbom', config)

        component = {
            'name': 'express',
            'version': '4.17.1',
            'purl': 'pkg:npm/express@4.17.1',
            'cpe': 'cpe:2.3:a:expressjs:express:4.17.1:*:*:*:*:*:*:*'
        }

        result = agent.correlate_cves(component)

        assert result == [], "Should return empty list when database unavailable"

    def test_correlate_cves_with_valid_database(self):
        """Test CVE correlation works with valid database"""
        config = {
            'cve_database': {
                'purl_index': {
                    'pkg:npm/express@4.17.1': ['CVE-2022-24999']
                },
                'cpe_index': {
                    'cpe:2.3:a:expressjs:express:4.17.1:*:*:*:*:*:*:*': ['CVE-2022-24999']
                }
            }
        }
        agent = SBOMAgent('test_sbom', config)

        component = {
            'name': 'express',
            'version': '4.17.1',
            'purl': 'pkg:npm/express@4.17.1',
            'cpe': 'cpe:2.3:a:expressjs:express:4.17.1:*:*:*:*:*:*:*'
        }

        result = agent.correlate_cves(component)

        assert len(result) > 0, "Should return CVE matches with valid database"
        assert result[0]['cve_id'] == 'CVE-2022-24999'

    def test_execute_with_missing_database(self):
        """Test execute method handles missing CVE database gracefully"""
        config = {'cve_database': {}}
        agent = SBOMAgent('test_sbom', config)

        # Create temporary test SBOM file
        import json
        import tempfile

        sbom_data = {
            'bomFormat': 'CycloneDX',
            'specVersion': '1.6',
            'version': 1,
            'components': [
                {
                    'name': 'express',
                    'version': '4.17.1',
                    'type': 'library',
                    'purl': 'pkg:npm/express@4.17.1'
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sbom_data, f)
            temp_file = f.name

        try:
            result = agent.execute({
                'sbom_file_path': temp_file,
                'include_cves': True
            })

            assert result['total_components'] == 1
            assert result['total_cves'] == 0, "Should have 0 CVEs without database"
            assert result['components'][0]['cve_matches'] == []
        finally:
            Path(temp_file).unlink()

    def test_validate_cve_database_exception_handling(self):
        """Test validation handles exceptions gracefully"""
        config = {
            'cve_database': {
                'purl_index': {'test': ['CVE-2023-0001']}
            }
        }
        agent = SBOMAgent('test_sbom', config)

        # Mock Neo4j to raise exception
        mock_driver = MagicMock()
        mock_driver.session.side_effect = Exception("Connection failed")
        agent.neo4j_driver = mock_driver

        # Should still validate using in-memory database
        result = agent.validate_cve_database()

        assert result is True, "Should fall back to in-memory validation on Neo4j error"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
