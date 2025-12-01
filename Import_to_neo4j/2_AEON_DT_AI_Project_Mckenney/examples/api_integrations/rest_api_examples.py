"""
REST API Integration Examples for Cyber Digital Twin

Complete examples of consuming the Cyber Digital Twin REST API,
including authentication, error handling, and result processing.

Author: Cyber Digital Twin Project
Date: 2025-10-29
"""

import requests
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class APIConfig:
    """API Configuration"""
    base_url: str = "http://localhost:8080"
    api_key: str = "your-api-key-here"
    timeout: int = 30
    verify_ssl: bool = True


class CyberDigitalTwinAPI:
    """REST API client for Cyber Digital Twin"""

    def __init__(self, config: APIConfig):
        """Initialize API client"""
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': config.api_key,
            'Content-Type': 'application/json'
        })

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to API

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            data: Request body data

        Returns:
            Response data as dictionary
        """
        url = f"{self.config.base_url}{endpoint}"
        headers = {'X-API-Key': self.config.api_key}

        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=headers,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            raise

        except requests.exceptions.RequestException as e:
            logger.error(f"Request Error: {e}")
            raise

    # ========================================================================
    # USE CASE 1: Asset Vulnerabilities API
    # ========================================================================

    def get_asset_vulnerabilities(
        self,
        component_name: str,
        severity_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get all vulnerabilities for a specific asset

        Args:
            component_name: Name of hardware component
            severity_filter: Filter by severity (CRITICAL, HIGH, MEDIUM, LOW)

        Returns:
            Vulnerabilities with detailed information
        """
        endpoint = "/api/v1/assets/vulnerabilities"
        params = {
            'component_name': component_name,
            'severity': severity_filter
        }

        response = self._make_request('GET', endpoint, params=params)

        return {
            'asset': component_name,
            'severity_filter': severity_filter,
            'vulnerabilities': response.get('data', []),
            'total_count': response.get('total', 0),
            'critical_count': response.get('critical_count', 0),
            'high_count': response.get('high_count', 0)
        }

    # ========================================================================
    # USE CASE 2: Critical Vulnerabilities API
    # ========================================================================

    def get_critical_vulnerabilities_due_soon(
        self,
        days_until_due: int = 30
    ) -> Dict[str, Any]:
        """
        Get critical vulnerabilities due for remediation soon

        Args:
            days_until_due: Number of days for remediation window

        Returns:
            Critical vulnerabilities sorted by urgency
        """
        endpoint = "/api/v1/vulnerabilities/critical-by-deadline"
        params = {'days': days_until_due}

        response = self._make_request('GET', endpoint, params=params)

        return {
            'remediation_window_days': days_until_due,
            'vulnerabilities': response.get('data', []),
            'immediate_action_count': sum(
                1 for v in response.get('data', [])
                if v.get('days_remaining', 999) <= 7
            ),
            'urgent_count': sum(
                1 for v in response.get('data', [])
                if v.get('days_remaining', 999) <= days_until_due
            )
        }

    # ========================================================================
    # USE CASE 3: Attack Path Analysis API
    # ========================================================================

    def analyze_attack_paths(
        self,
        source_zone: str = 'EXTERNAL',
        target_zone: str = 'SCADA',
        max_hops: int = 8
    ) -> Dict[str, Any]:
        """
        Analyze possible attack paths between network zones

        Args:
            source_zone: Starting network zone
            target_zone: Target network zone
            max_hops: Maximum number of hops to consider

        Returns:
            Attack paths ranked by risk
        """
        endpoint = "/api/v1/network/attack-paths"
        data = {
            'source_zone': source_zone,
            'target_zone': target_zone,
            'max_hops': max_hops
        }

        response = self._make_request('POST', endpoint, data=data)

        return {
            'source': source_zone,
            'target': target_zone,
            'paths_found': len(response.get('data', [])),
            'shortest_path_hops': min(
                (p.get('hops', 999) for p in response.get('data', [])),
                default=None
            ),
            'critical_paths': sum(
                1 for p in response.get('data', [])
                if p.get('risk_level') == 'CRITICAL'
            ),
            'paths': response.get('data', [])
        }

    # ========================================================================
    # USE CASE 4: Threat Actor Correlation API
    # ========================================================================

    def get_threat_actors_in_sector(
        self,
        sector: str = 'Energy'
    ) -> Dict[str, Any]:
        """
        Get threat actors targeting a specific sector

        Args:
            sector: Industry sector name

        Returns:
            Threat actors ranked by activity
        """
        endpoint = f"/api/v1/threat-actors/sector/{sector}"

        response = self._make_request('GET', endpoint)

        return {
            'sector': sector,
            'threat_actors': response.get('data', []),
            'total_actors': response.get('total', 0),
            'advanced_threat_actors': sum(
                1 for a in response.get('data', [])
                if a.get('threat_level') == 'ADVANCED'
            )
        }

    # ========================================================================
    # USE CASE 5: Vulnerability Explosion API
    # ========================================================================

    def analyze_vulnerability_explosion(
        self,
        cve_id: str
    ) -> Dict[str, Any]:
        """
        Analyze how a CVE cascades through the fleet

        Args:
            cve_id: CVE ID to analyze

        Returns:
            Blast radius and affected asset counts
        """
        endpoint = f"/api/v1/vulnerabilities/{cve_id}/explosion"

        response = self._make_request('GET', endpoint)

        data = response.get('data', {})

        return {
            'cve_id': cve_id,
            'firmware_versions_affected': data.get('firmware_versions', 0),
            'devices_affected': data.get('devices', 0),
            'fleets_affected': data.get('fleets', 0),
            'blast_radius': data.get('blast_radius', 0),
            'impact_level': data.get('impact_level', 'UNKNOWN')
        }

    # ========================================================================
    # USE CASE 6: SEVD Prioritization API
    # ========================================================================

    def get_sevd_prioritization(self) -> Dict[str, Any]:
        """
        Get vulnerability prioritization using SEVD methodology

        Returns:
            Vulnerabilities classified as Now/Next/Never
        """
        endpoint = "/api/v1/vulnerabilities/sevd-prioritization"

        response = self._make_request('GET', endpoint)

        data = response.get('data', {})

        return {
            'prioritization': {
                'now': data.get('now', {}),
                'next': data.get('next', {}),
                'never': data.get('never', {})
            },
            'total_vulnerabilities': (
                data.get('now', {}).get('count', 0) +
                data.get('next', {}).get('count', 0) +
                data.get('never', {}).get('count', 0)
            )
        }

    # ========================================================================
    # USE CASE 7: Compliance Mapping API
    # ========================================================================

    def map_to_compliance_framework(
        self,
        framework: str = 'IEC 62443'
    ) -> Dict[str, Any]:
        """
        Map vulnerabilities to compliance framework requirements

        Args:
            framework: Compliance framework name

        Returns:
            Compliance coverage and gaps
        """
        endpoint = f"/api/v1/compliance/{framework}/mapping"

        response = self._make_request('GET', endpoint)

        data = response.get('data', {})

        return {
            'framework': framework,
            'total_requirements': data.get('total_requirements', 0),
            'covered_requirements': data.get('covered_requirements', 0),
            'compliance_gap': data.get('compliance_gap', 0),
            'coverage_percent': data.get('coverage_percent', 0)
        }

    # ========================================================================
    # Advanced Features
    # ========================================================================

    def search_vulnerabilities(
        self,
        query: str,
        filters: Optional[Dict] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search vulnerabilities with filters

        Args:
            query: Search query string
            filters: Optional filters (severity, cvss_score_min, etc.)
            limit: Result limit
            offset: Result offset for pagination

        Returns:
            Search results
        """
        endpoint = "/api/v1/vulnerabilities/search"
        params = {
            'q': query,
            'limit': limit,
            'offset': offset
        }

        if filters:
            params.update(filters)

        response = self._make_request('GET', endpoint, params=params)

        return {
            'query': query,
            'results': response.get('data', []),
            'total': response.get('total', 0),
            'limit': limit,
            'offset': offset
        }

    def generate_report(
        self,
        report_type: str,
        sector: Optional[str] = None,
        date_range: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive security report

        Args:
            report_type: Type of report (threat-intel, compliance, risk-assessment)
            sector: Optional sector filter
            date_range: Optional date range filter

        Returns:
            Generated report
        """
        endpoint = f"/api/v1/reports/{report_type}/generate"
        data = {
            'sector': sector,
            'date_range': date_range
        }

        response = self._make_request('POST', endpoint, data=data)

        return {
            'report_type': report_type,
            'generated_at': datetime.now().isoformat(),
            'report': response.get('data', {})
        }

    def export_data(
        self,
        data_type: str,
        format: str = 'json'
    ) -> bytes:
        """
        Export data in various formats

        Args:
            data_type: Type of data to export
            format: Export format (json, csv, xlsx)

        Returns:
            Exported data as bytes
        """
        endpoint = f"/api/v1/export/{data_type}"
        params = {'format': format}

        response = requests.get(
            f"{self.config.base_url}{endpoint}",
            params=params,
            headers={'X-API-Key': self.config.api_key},
            timeout=self.config.timeout,
            verify=self.config.verify_ssl
        )
        response.raise_for_status()

        return response.content


# ============================================================================
# Usage Examples
# ============================================================================

def example_basic_usage():
    """Basic API usage example"""
    config = APIConfig(
        base_url="http://localhost:8080",
        api_key="your-api-key"
    )

    client = CyberDigitalTwinAPI(config)

    # Get vulnerabilities for specific asset
    print("Getting Brake Controller vulnerabilities...")
    vulns = client.get_asset_vulnerabilities(
        'Brake Controller',
        severity_filter='HIGH'
    )
    print(f"Found {vulns['total_count']} vulnerabilities")

    # Get critical vulnerabilities due soon
    print("\nGetting critical vulnerabilities due within 30 days...")
    critical = client.get_critical_vulnerabilities_due_soon(30)
    print(f"Found {critical['immediate_action_count']} requiring immediate action")

    # Analyze attack paths
    print("\nAnalyzing attack paths...")
    paths = client.analyze_attack_paths('EXTERNAL', 'SCADA')
    print(f"Found {paths['paths_found']} possible attack paths")


def example_threat_actor_analysis():
    """Threat actor analysis example"""
    config = APIConfig()
    client = CyberDigitalTwinAPI(config)

    # Get threat actors in Energy sector
    print("Getting threat actors targeting Energy sector...")
    actors = client.get_threat_actors_in_sector('Energy')

    print(f"Total threat actors: {actors['total_actors']}")
    print(f"Advanced threat actors: {actors['advanced_threat_actors']}")

    for actor in actors['threat_actors'][:5]:
        print(f"  - {actor['name']}: {actor['exploits_in_sector']} exploits")


def example_sevd_prioritization():
    """SEVD prioritization example"""
    config = APIConfig()
    client = CyberDigitalTwinAPI(config)

    print("Getting SEVD prioritization...")
    sevd = client.get_sevd_prioritization()

    print(f"Now: {sevd['prioritization']['now'].get('count', 0)} vulnerabilities")
    print(f"Next: {sevd['prioritization']['next'].get('count', 0)} vulnerabilities")
    print(f"Never: {sevd['prioritization']['never'].get('count', 0)} vulnerabilities")


def example_compliance_mapping():
    """Compliance mapping example"""
    config = APIConfig()
    client = CyberDigitalTwinAPI(config)

    print("Checking IEC 62443 compliance...")
    compliance = client.map_to_compliance_framework('IEC 62443')

    print(f"Total requirements: {compliance['total_requirements']}")
    print(f"Covered: {compliance['covered_requirements']}")
    print(f"Gaps: {compliance['compliance_gap']}")
    print(f"Coverage: {compliance['coverage_percent']}%")


if __name__ == '__main__':
    # Note: These examples require a running Cyber Digital Twin API server
    # Configure with your actual API endpoint and credentials

    print("Cyber Digital Twin - REST API Examples")
    print("=" * 80)

    # Uncomment to run examples:
    # example_basic_usage()
    # example_threat_actor_analysis()
    # example_sevd_prioritization()
    # example_compliance_mapping()

    print("\nAPI examples defined. Configure and uncomment to run.")
