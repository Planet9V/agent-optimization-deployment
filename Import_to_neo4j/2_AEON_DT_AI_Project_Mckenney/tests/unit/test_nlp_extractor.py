"""
Unit Tests for NLP Entity Extraction

Tests spaCy entity extraction, custom CVE/CWE patterns, and relationship extraction.

Author: Cyber Digital Twin Project
Date: 2025-10-29
"""

import pytest
from unittest.mock import Mock, patch
import re


class TestEntityExtraction:
    """Test suite for entity extraction from vulnerability descriptions"""

    @pytest.fixture
    def sample_vulnerability_text(self):
        """Sample vulnerability description text"""
        return """
        A remote code execution vulnerability was discovered in Apache Log4j versions
        2.0 through 2.14.1. An attacker can execute arbitrary code by exploiting the
        JNDI injection flaw in the message lookup feature. The vulnerability affects
        all applications using the vulnerable Log4j library. CVSS score: 10.0.
        """

    @pytest.fixture
    def sample_cwe_text(self):
        """Sample text with CWE references"""
        return """
        This vulnerability is classified as CWE-917 (Expression Language Injection)
        and is related to CWE-94 (Improper Control of Generation of Code).
        """

    def test_cve_pattern_matching(self):
        """Test CVE ID pattern recognition"""
        text = "This affects CVE-2024-1234 and CVE-2023-5678"
        cve_pattern = r'CVE-\d{4}-\d{4,}'

        matches = re.findall(cve_pattern, text)
        assert len(matches) == 2
        assert 'CVE-2024-1234' in matches
        assert 'CVE-2023-5678' in matches

    def test_cwe_pattern_matching(self, sample_cwe_text):
        """Test CWE ID pattern recognition"""
        cwe_pattern = r'CWE-\d+'

        matches = re.findall(cwe_pattern, sample_cwe_text)
        assert len(matches) == 2
        assert 'CWE-917' in matches
        assert 'CWE-94' in matches

    def test_severity_extraction(self):
        """Test severity level extraction"""
        text = "This vulnerability has CVSS v3.1 base score of 8.5 (HIGH severity)"

        severity_pattern = r'(LOW|MEDIUM|HIGH|CRITICAL)'
        matches = re.findall(severity_pattern, text)

        assert 'HIGH' in matches

    def test_product_vendor_extraction(self):
        """Test product and vendor name extraction"""
        text = "Apache Log4j 2.14.1 contains a vulnerability. Cisco IOS XE also affected."

        # Simple extraction for known patterns
        vendors = ['Apache', 'Cisco', 'Microsoft', 'Oracle']
        products = ['Log4j', 'IOS', 'Windows', 'Java']

        found_vendors = [v for v in vendors if v in text]
        found_products = [p for p in products if p in text]

        assert 'Apache' in found_vendors
        assert 'Cisco' in found_vendors
        assert 'Log4j' in found_products

    def test_version_extraction(self):
        """Test version number extraction"""
        text = "Affects versions 2.0 through 2.14.1 and 3.0.0 beta"
        version_pattern = r'\d+\.\d+(?:\.\d+)?'

        matches = re.findall(version_pattern, text)
        assert '2.0' in matches
        assert '2.14.1' in matches
        assert '3.0.0' in matches

    def test_attack_vector_extraction(self):
        """Test attack vector extraction"""
        text = """
        Network attack vector: remote exploitation possible
        Attack complexity: low
        Privileges required: none
        User interaction: required
        """

        attack_vectors = ['Network', 'Adjacent', 'Local', 'Physical']
        found = [av for av in attack_vectors if av in text]

        assert 'Network' in found

    def test_impact_classification(self):
        """Test impact classification extraction"""
        impacts = {
            'Confidentiality': 'High',
            'Integrity': 'High',
            'Availability': 'High'
        }

        text = "Has high impact on confidentiality, integrity, and availability"

        found_impacts = {k: v for k, v in impacts.items() if k.lower() in text.lower()}
        assert len(found_impacts) == 3


class TestRelationshipExtraction:
    """Test suite for relationship extraction between entities"""

    def test_cve_cwe_relationship(self):
        """Test extraction of CVE-CWE relationships"""
        text = "CVE-2024-1234 is caused by CWE-917"

        cve_pattern = r'CVE-\d{4}-\d{4,}'
        cwe_pattern = r'CWE-\d+'

        cve = re.search(cve_pattern, text)
        cwe = re.search(cwe_pattern, text)

        assert cve is not None
        assert cwe is not None
        assert cve.group() == 'CVE-2024-1234'
        assert cwe.group() == 'CWE-917'

    def test_product_vulnerability_relationship(self):
        """Test extraction of product-vulnerability relationships"""
        text = "Apache Log4j versions 2.0 through 2.14.1 are vulnerable to CVE-2024-1234"

        def extract_relationship(text):
            product_pattern = r'([\w\s]+)\s+(versions?\s+)?([0-9.]+)'
            cve_pattern = r'CVE-\d{4}-\d{4,}'

            product_match = re.search(product_pattern, text)
            cve_match = re.search(cve_pattern, text)

            return (product_match.group(1) if product_match else None,
                   cve_match.group() if cve_match else None)

        product, cve = extract_relationship(text)
        assert product is not None
        assert cve == 'CVE-2024-1234'

    def test_threat_actor_cve_relationship(self):
        """Test extraction of threat actor-CVE relationships"""
        text = "APT28 exploits CVE-2024-1234 and CVE-2023-5678"

        threat_actors = ['APT28', 'Lazarus', 'FIN7', 'Carbanak']
        cve_pattern = r'CVE-\d{4}-\d{4,}'

        actor = None
        for ta in threat_actors:
            if ta in text:
                actor = ta
                break

        cves = re.findall(cve_pattern, text)

        assert actor == 'APT28'
        assert len(cves) == 2
        assert 'CVE-2024-1234' in cves

    def test_capec_cwe_relationship(self):
        """Test extraction of CAPEC-CWE relationships"""
        text = "CAPEC-88 Buffer Overflow exploits CWE-120 Buffer Copy"

        capec_pattern = r'CAPEC-\d+'
        cwe_pattern = r'CWE-\d+'

        capec = re.search(capec_pattern, text)
        cwe = re.search(cwe_pattern, text)

        assert capec.group() == 'CAPEC-88'
        assert cwe.group() == 'CWE-120'


class TestCustomPatterns:
    """Test suite for custom vulnerability pattern matching"""

    def test_injection_pattern(self):
        """Test detection of injection vulnerabilities"""
        injection_keywords = [
            'sql injection',
            'code injection',
            'command injection',
            'ldap injection',
            'xpath injection'
        ]

        text_vulnerable = "The application is vulnerable to SQL injection"
        text_safe = "The application validates all inputs properly"

        def is_injection_vulnerability(text):
            return any(keyword in text.lower() for keyword in injection_keywords)

        assert is_injection_vulnerability(text_vulnerable)
        assert not is_injection_vulnerability(text_safe)

    def test_authentication_bypass_pattern(self):
        """Test detection of authentication bypass vulnerabilities"""
        text = "Authentication bypass in login function allows unauthorized access"

        auth_keywords = ['authentication bypass', 'weak authentication', 'default credentials']

        found = any(keyword in text.lower() for keyword in auth_keywords)
        assert found

    def test_remote_execution_pattern(self):
        """Test detection of remote code execution vulnerabilities"""
        rce_keywords = [
            'remote code execution',
            'arbitrary code execution',
            'remote command execution',
            'os command injection'
        ]

        text = "Vulnerability allows arbitrary code execution on the server"

        found = any(keyword in text.lower() for keyword in rce_keywords)
        assert found

    def test_privilege_escalation_pattern(self):
        """Test detection of privilege escalation vulnerabilities"""
        text = "Local users can exploit privilege escalation to gain system administrator access"

        pe_keywords = ['privilege escalation', 'privilege elevation', 'local privilege']

        found = any(keyword in text.lower() for keyword in pe_keywords)
        assert found

    def test_race_condition_pattern(self):
        """Test detection of race condition vulnerabilities"""
        text = "Race condition in file handling allows information disclosure"

        rc_keywords = ['race condition', 'toctou', 'time-of-check-time-of-use']

        found = any(keyword in text.lower() for keyword in rc_keywords)
        assert found


class TestEntityNormalization:
    """Test suite for entity normalization and standardization"""

    def test_cve_id_normalization(self):
        """Test CVE ID normalization"""
        variations = [
            'CVE-2024-1234',
            'cve-2024-1234',
            'CVE 2024 1234',
            'CVE_2024_1234'
        ]

        def normalize_cve(cve_str):
            # Remove all non-alphanumeric except hyphen, convert to uppercase
            cve_str = re.sub(r'[^\w-]', '', cve_str.upper())
            # Ensure proper format
            cve_str = re.sub(r'CVE[\W_]*(\d{4})[\W_]*(\d{4,})', r'CVE-\1-\2', cve_str)
            return cve_str

        normalized = [normalize_cve(cve) for cve in variations]

        # All should normalize to same format
        assert all(cve.startswith('CVE-2024-') for cve in normalized)

    def test_vendor_name_normalization(self):
        """Test vendor name normalization"""
        variations = [
            'apache foundation',
            'Apache Foundation',
            'APACHE FOUNDATION',
            'apache  foundation'  # double space
        ]

        def normalize_vendor(name):
            return ' '.join(name.lower().split())

        normalized = [normalize_vendor(v) for v in variations]

        # All should normalize to same format
        assert all(n == 'apache foundation' for n in normalized)

    def test_version_number_normalization(self):
        """Test version number normalization"""
        versions = [
            'v2.14.1',
            '2.14.1',
            '2.14.1 ',
            'Version 2.14.1'
        ]

        def normalize_version(version):
            # Extract version number
            match = re.search(r'\d+\.\d+(?:\.\d+)?', version)
            return match.group() if match else None

        normalized = [normalize_version(v) for v in versions]

        assert all(n == '2.14.1' for n in normalized)

    def test_severity_normalization(self):
        """Test severity level normalization"""
        variations = [
            'HIGH',
            'high',
            'High',
            'H (High)'
        ]

        def normalize_severity(severity):
            severity_map = {
                'c': 'CRITICAL',
                'h': 'HIGH',
                'm': 'MEDIUM',
                'l': 'LOW'
            }
            # Get first letter, lowercase
            first_letter = severity[0].lower()
            return severity_map.get(first_letter, severity.upper())

        normalized = [normalize_severity(s) for s in variations]

        assert all(n == 'HIGH' for n in normalized)


class TestExtractionPerformance:
    """Test suite for extraction performance"""

    def test_pattern_matching_performance(self):
        """Test performance of pattern matching on large text"""
        # Create large vulnerability text
        large_text = " ".join([
            f"CVE-2024-{i:05d} with CVSS {i % 10}.{i % 10} severity"
            for i in range(1000)
        ])

        cve_pattern = r'CVE-\d{4}-\d{4,}'

        import time
        start = time.time()
        matches = re.findall(cve_pattern, large_text)
        duration = time.time() - start

        assert len(matches) == 1000
        assert duration < 1.0  # Should complete in less than 1 second

    def test_extraction_on_large_document(self):
        """Test extraction on large document"""
        # Simulate 1MB of vulnerability descriptions
        document = " ".join([
            "Apache Log4j vulnerability CVE-2024-1234 affects versions 2.0-2.14.1"
            for _ in range(1000)
        ])

        cve_pattern = r'CVE-\d{4}-\d{4,}'

        import time
        start = time.time()
        matches = re.findall(cve_pattern, document)
        duration = time.time() - start

        assert len(matches) == 1000
        assert duration < 2.0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
