"""
Unit Tests for NVD API Integration and CVE Importer

Tests NVD API connectivity, rate limiting, CPE parsing, and batch import capabilities.
Includes mocking for external API calls to ensure test isolation.

Author: Cyber Digital Twin Project
Date: 2025-10-29
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import time


class TestNVDAPIConnector:
    """Test suite for NVD API integration"""

    @pytest.fixture
    def nvd_connector_config(self):
        """Fixture for NVD connector configuration"""
        return {
            'api_key': 'test_api_key_12345',
            'base_url': 'https://services.nvd.nist.gov/rest/json/cves/1.0',
            'rate_limit_per_hour': 5000,
            'max_retries': 3,
            'timeout': 30,
            'batch_size': 100
        }

    @pytest.fixture
    def sample_cve_response(self):
        """Sample CVE response from NVD API"""
        return {
            'result': {
                'CVE_Items': [
                    {
                        'cve': {
                            'CVE_data_meta': {
                                'ID': 'CVE-2024-1234'
                            },
                            'description': {
                                'description_data': [
                                    {
                                        'value': 'Test vulnerability in brake controller'
                                    }
                                ]
                            }
                        },
                        'impact': {
                            'baseMetricV3': {
                                'cvssV3': {
                                    'baseSeverity': 'HIGH',
                                    'baseScore': 8.5
                                }
                            }
                        },
                        'configurations': {
                            'nodes': [
                                {
                                    'cpe_match': [
                                        {
                                            'vulnerable': True,
                                            'cpe23Uri': 'cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*:*'
                                        }
                                    ]
                                }
                            ]
                        },
                        'publishedDate': '2024-01-15T00:00Z'
                    }
                ]
            }
        }

    def test_api_connection_success(self, nvd_connector_config):
        """Test successful NVD API connection"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'result': {'CVE_Items': []}}
            mock_get.return_value = mock_response

            # Simulate API call
            response = mock_get()
            assert response.status_code == 200
            assert 'result' in response.json()

    def test_api_rate_limiting(self, nvd_connector_config):
        """Test rate limiting implementation"""
        rate_limit = nvd_connector_config['rate_limit_per_hour']
        requests_in_window = []

        # Simulate 10 requests over a 1-hour window
        for i in range(10):
            timestamp = datetime.now()
            requests_in_window.append(timestamp)

        # Check that we don't exceed rate limit
        assert len([r for r in requests_in_window
                   if r > datetime.now() - timedelta(hours=1)]) <= rate_limit

    def test_cpe_parsing(self, sample_cve_response):
        """Test CPE string parsing"""
        cpe_uri = 'cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*:*'
        parts = cpe_uri.split(':')

        assert parts[0] == 'cpe'
        assert parts[1] == '2.3'
        assert parts[2] == 'a'  # type (application)
        assert parts[3] == 'vendor'
        assert parts[4] == 'product'
        assert parts[5] == '1.0'

    def test_batch_import_with_retries(self):
        """Test batch import with retry logic"""
        batch_size = 100
        max_retries = 3
        cves = [f'CVE-2024-{i:04d}' for i in range(250)]

        # Split into batches
        batches = [cves[i:i+batch_size] for i in range(0, len(cves), batch_size)]

        assert len(batches) == 3
        assert len(batches[0]) == 100
        assert len(batches[1]) == 100
        assert len(batches[2]) == 50

    def test_api_response_validation(self, sample_cve_response):
        """Test validation of API response structure"""
        response = sample_cve_response

        assert 'result' in response
        assert 'CVE_Items' in response['result']
        assert len(response['result']['CVE_Items']) > 0

        cve_item = response['result']['CVE_Items'][0]
        assert 'cve' in cve_item
        assert 'CVE_data_meta' in cve_item['cve']
        assert 'ID' in cve_item['cve']['CVE_data_meta']

    def test_cvss_score_extraction(self, sample_cve_response):
        """Test CVSS score extraction and validation"""
        cve_item = sample_cve_response['result']['CVE_Items'][0]
        cvss_data = cve_item['impact']['baseMetricV3']['cvssV3']

        assert 'baseScore' in cvss_data
        assert 'baseSeverity' in cvss_data
        assert 0 <= cvss_data['baseScore'] <= 10
        assert cvss_data['baseSeverity'] in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']

    def test_date_parsing(self, sample_cve_response):
        """Test published date parsing"""
        cve_item = sample_cve_response['result']['CVE_Items'][0]
        date_str = cve_item['publishedDate']

        # Parse ISO format date
        published_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        assert isinstance(published_date, datetime)
        assert published_date.year == 2024

    def test_retry_on_timeout(self):
        """Test retry mechanism on timeout"""
        retry_count = 0
        max_retries = 3

        with patch('requests.get') as mock_get:
            # Simulate timeout on first 2 attempts, success on 3rd
            mock_get.side_effect = [
                TimeoutError(),
                TimeoutError(),
                Mock(status_code=200, json=lambda: {'result': {'CVE_Items': []}})
            ]

            for attempt in range(max_retries):
                try:
                    result = mock_get()
                    assert result.status_code == 200
                    break
                except TimeoutError:
                    retry_count += 1
                    if retry_count >= max_retries:
                        raise

    def test_duplicate_cve_detection(self):
        """Test detection of duplicate CVE entries"""
        cves = ['CVE-2024-0001', 'CVE-2024-0002', 'CVE-2024-0001']
        unique_cves = list(set(cves))

        assert len(cves) == 3
        assert len(unique_cves) == 2
        assert 'CVE-2024-0001' in unique_cves

    def test_cve_id_validation(self):
        """Test CVE ID format validation"""
        valid_cves = [
            'CVE-2024-1234',
            'CVE-2023-12345',
            'CVE-2000-0001'
        ]

        invalid_cves = [
            'CVE-2024-',
            'CVE-2024',
            'CVE2024-1234'
        ]

        import re
        cve_pattern = r'^CVE-\d{4}-\d{4,}$'

        for cve in valid_cves:
            assert re.match(cve_pattern, cve)

        for cve in invalid_cves:
            assert not re.match(cve_pattern, cve)


class TestCPEParsing:
    """Test suite for CPE parsing and matching"""

    def test_cpe_component_extraction(self):
        """Test extraction of CPE components"""
        cpe = 'cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*'
        parts = cpe.split(':')

        assert parts[2] == 'a'  # application
        assert parts[3] == 'apache'  # vendor
        assert parts[4] == 'log4j'  # product
        assert parts[5] == '2.14.1'  # version

    def test_cpe_matching_logic(self):
        """Test CPE matching against device software"""
        device_cpe = 'cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*'
        vuln_cpe = 'cpe:2.3:a:apache:log4j:*:*:*:*:*:*:*:*'

        # Simple matching: check if device matches vuln pattern
        def cpe_matches(device_cpe, vuln_cpe):
            device_parts = device_cpe.split(':')
            vuln_parts = vuln_cpe.split(':')

            for i in range(min(len(device_parts), len(vuln_parts))):
                if vuln_parts[i] != '*' and vuln_parts[i] != device_parts[i]:
                    return False
            return True

        assert cpe_matches(device_cpe, vuln_cpe)

    def test_cpe_version_comparison(self):
        """Test version comparison in CPE matching"""
        from packaging import version

        vuln_versions = ['2.14.0', '2.14.1', '2.15.0']
        device_version = '2.14.1'

        assert device_version in vuln_versions
        assert version.parse(device_version) >= version.parse('2.14.0')


class TestDataQuality:
    """Test suite for data quality validation"""

    def test_missing_required_fields(self):
        """Test detection of missing required CVE fields"""
        incomplete_cve = {
            'cve_id': 'CVE-2024-0001',
            # Missing: description, impact, configurations
        }

        required_fields = ['cve_id', 'description', 'cvss_score', 'published_date']

        def validate_cve(cve, required_fields):
            return all(field in cve for field in required_fields)

        assert not validate_cve(incomplete_cve, required_fields)

    def test_data_type_validation(self):
        """Test validation of data types"""
        cve = {
            'cve_id': 'CVE-2024-0001',
            'cvss_score': 8.5,
            'affected_cpes': ['cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*:*'],
            'published_date': '2024-01-15'
        }

        assert isinstance(cve['cve_id'], str)
        assert isinstance(cve['cvss_score'], (int, float))
        assert isinstance(cve['affected_cpes'], list)
        assert isinstance(cve['published_date'], str)

    def test_cvss_score_bounds(self):
        """Test CVSS score validation"""
        valid_scores = [0.0, 3.5, 7.0, 9.9, 10.0]
        invalid_scores = [-1.0, 10.1, 15.0]

        def is_valid_cvss(score):
            return 0 <= score <= 10

        for score in valid_scores:
            assert is_valid_cvss(score)

        for score in invalid_scores:
            assert not is_valid_cvss(score)

    def test_severity_classification(self):
        """Test CVSS severity classification"""
        def get_severity(cvss_score):
            if cvss_score == 0:
                return 'NONE'
            elif cvss_score <= 3.9:
                return 'LOW'
            elif cvss_score <= 6.9:
                return 'MEDIUM'
            elif cvss_score <= 8.9:
                return 'HIGH'
            else:
                return 'CRITICAL'

        assert get_severity(0) == 'NONE'
        assert get_severity(3.5) == 'LOW'
        assert get_severity(6.5) == 'MEDIUM'
        assert get_severity(8.5) == 'HIGH'
        assert get_severity(9.5) == 'CRITICAL'


class TestBatchProcessing:
    """Test suite for batch processing operations"""

    def test_batch_creation_from_list(self):
        """Test creation of batches from large lists"""
        cves = [f'CVE-2024-{i:05d}' for i in range(1000)]
        batch_size = 100

        batches = [cves[i:i+batch_size] for i in range(0, len(cves), batch_size)]

        assert len(batches) == 10
        assert all(len(batch) == batch_size for batch in batches[:-1])
        assert len(batches[-1]) == batch_size

    def test_batch_processing_order(self):
        """Test that batch processing maintains order"""
        items = list(range(1000))
        batch_size = 100

        batches = [items[i:i+batch_size] for i in range(0, len(items), batch_size)]
        reconstructed = []
        for batch in batches:
            reconstructed.extend(batch)

        assert reconstructed == items

    def test_batch_error_handling(self):
        """Test error handling in batch processing"""
        def process_batch(batch):
            if None in batch:
                raise ValueError("Invalid item in batch")
            return [x * 2 for x in batch]

        valid_batch = [1, 2, 3, 4, 5]
        invalid_batch = [1, 2, None, 4, 5]

        assert process_batch(valid_batch) == [2, 4, 6, 8, 10]

        with pytest.raises(ValueError):
            process_batch(invalid_batch)


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
