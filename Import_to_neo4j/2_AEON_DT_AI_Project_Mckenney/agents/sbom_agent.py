"""
SBOM Integration Agent
Parses CycloneDX 1.6 and SPDX 3.0 SBOM files with 4-stage CVE correlation
"""

import json
import re
from typing import Any, Dict, List, Optional
from pathlib import Path
from difflib import SequenceMatcher

try:
    from lib4sbom.parser import SBOMParser
    from lib4sbom.data.package import SBOMPackage
except ImportError:
    SBOMParser = None
    SBOMPackage = None

try:
    from cyclonedx.model import bom as cyclonedx_bom
    from cyclonedx.parser import JsonParser as CycloneDXParser
except ImportError:
    cyclonedx_bom = None
    CycloneDXParser = None

from agents.base_agent import BaseAgent


class SBOMAgent(BaseAgent):
    """
    SBOM Integration Specialist Agent

    Capabilities:
    - Parse CycloneDX 1.6 and SPDX 3.0 formats
    - Extract SoftwareComponent nodes
    - 4-stage CVE correlation with confidence scoring
    """

    def _setup(self):
        """Initialize SBOM agent-specific configuration"""
        self.supported_formats = ['cyclonedx', 'spdx']
        self.cve_database = self.config.get('cve_database', {})
        self.confidence_thresholds = {
            'purl_match': 0.95,
            'cpe_exact': 1.0,
            'cpe_range': 0.85,
            'fuzzy_match': 0.6
        }
        self.logger.info(f"SBOM Agent initialized with formats: {self.supported_formats}")

    def parse_sbom(self, file_path: str) -> Dict[str, Any]:
        """
        Parse SBOM file (CycloneDX or SPDX)

        Args:
            file_path: Path to SBOM file

        Returns:
            Parsed SBOM data with format detection
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"SBOM file not found: {file_path}")

        self.logger.info(f"Parsing SBOM file: {file_path}")

        # Read file content
        from agents.base_agent import read_file_safe
        content = read_file_safe(str(path))

        # Try JSON parsing first
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # Try lib4sbom for SPDX tag-value format
            if SBOMParser:
                parser = SBOMParser()
                sbom_doc = parser.parse_file(str(path))
                return self._convert_lib4sbom_to_dict(sbom_doc)
            else:
                raise ValueError("Unable to parse SBOM: JSON invalid and lib4sbom not available")

        # Detect format
        sbom_format = self._detect_format(data)

        return {
            'format': sbom_format,
            'raw_data': data,
            'file_path': str(path)
        }

    def _detect_format(self, data: Dict) -> str:
        """Detect SBOM format from parsed data"""
        if 'bomFormat' in data and data['bomFormat'] == 'CycloneDX':
            return 'cyclonedx'
        elif 'spdxVersion' in data or 'SPDXID' in data:
            return 'spdx'
        elif 'components' in data:
            # Likely CycloneDX without explicit bomFormat
            return 'cyclonedx'
        elif 'packages' in data:
            # Likely SPDX
            return 'spdx'
        else:
            raise ValueError("Unknown SBOM format")

    def _convert_lib4sbom_to_dict(self, sbom_doc) -> Dict[str, Any]:
        """Convert lib4sbom document to dictionary format"""
        # This is a simplified conversion - lib4sbom structure varies
        return {
            'format': 'spdx',
            'raw_data': {
                'packages': getattr(sbom_doc, 'packages', [])
            },
            'file_path': 'lib4sbom_parsed'
        }

    def extract_components(self, sbom_data: Dict) -> List[Dict[str, Any]]:
        """
        Extract SoftwareComponent nodes from parsed SBOM

        Args:
            sbom_data: Parsed SBOM data

        Returns:
            List of component dictionaries with properties
        """
        sbom_format = sbom_data['format']
        raw_data = sbom_data['raw_data']

        self.logger.info(f"Extracting components from {sbom_format} SBOM")

        if sbom_format == 'cyclonedx':
            return self._extract_cyclonedx_components(raw_data)
        elif sbom_format == 'spdx':
            return self._extract_spdx_components(raw_data)
        else:
            raise ValueError(f"Unsupported SBOM format: {sbom_format}")

    def _extract_cyclonedx_components(self, data: Dict) -> List[Dict[str, Any]]:
        """Extract components from CycloneDX SBOM"""
        components = []

        for comp in data.get('components', []):
            component = {
                'name': comp.get('name', 'unknown'),
                'version': comp.get('version', ''),
                'purl': comp.get('purl', ''),
                'cpe': comp.get('cpe', ''),
                'ecosystem': self._extract_ecosystem_from_purl(comp.get('purl', '')),
                'license': self._extract_license(comp.get('licenses', [])),
                'type': comp.get('type', 'library'),
                'bom_ref': comp.get('bom-ref', ''),
                'supplier': comp.get('supplier', {}).get('name', ''),
                'hashes': comp.get('hashes', []),
                'properties': comp.get('properties', [])
            }
            components.append(component)

        self.logger.info(f"Extracted {len(components)} CycloneDX components")
        return components

    def _extract_spdx_components(self, data: Dict) -> List[Dict[str, Any]]:
        """Extract components from SPDX SBOM"""
        components = []

        for pkg in data.get('packages', []):
            # Extract PURL from external refs
            purl = ''
            cpe = ''
            for ref in pkg.get('externalRefs', []):
                if ref.get('referenceType') == 'purl':
                    purl = ref.get('referenceLocator', '')
                elif ref.get('referenceType') == 'cpe23Type':
                    cpe = ref.get('referenceLocator', '')

            component = {
                'name': pkg.get('name', 'unknown'),
                'version': pkg.get('versionInfo', ''),
                'purl': purl,
                'cpe': cpe,
                'ecosystem': self._extract_ecosystem_from_purl(purl),
                'license': pkg.get('licenseConcluded', pkg.get('licenseDeclared', '')),
                'type': 'library',
                'spdx_id': pkg.get('SPDXID', ''),
                'supplier': pkg.get('supplier', ''),
                'download_location': pkg.get('downloadLocation', ''),
                'checksums': pkg.get('checksums', [])
            }
            components.append(component)

        self.logger.info(f"Extracted {len(components)} SPDX components")
        return components

    def _extract_ecosystem_from_purl(self, purl: str) -> str:
        """Extract ecosystem from PURL string"""
        if not purl:
            return 'unknown'

        # PURL format: pkg:type/namespace/name@version
        match = re.match(r'pkg:([^/]+)/', purl)
        if match:
            return match.group(1)

        return 'unknown'

    def _extract_license(self, licenses: List) -> str:
        """Extract license string from CycloneDX license array"""
        if not licenses:
            return ''

        license_names = []
        for lic in licenses:
            if 'license' in lic:
                if 'id' in lic['license']:
                    license_names.append(lic['license']['id'])
                elif 'name' in lic['license']:
                    license_names.append(lic['license']['name'])

        return ', '.join(license_names)

    def validate_cve_database(self) -> bool:
        """
        Check if CVE database is accessible and contains data

        Returns:
            bool: True if CVE database is valid, False otherwise
        """
        try:
            # Check if cve_database configuration exists
            if not self.cve_database:
                self.logger.warning("CVE database configuration is empty")
                return False

            # Check if any index exists
            has_purl_index = bool(self.cve_database.get('purl_index'))
            has_cpe_index = bool(self.cve_database.get('cpe_index'))
            has_cpe_ranges = bool(self.cve_database.get('cpe_ranges'))
            has_fuzzy_index = bool(self.cve_database.get('fuzzy_index'))

            # At least one index should be populated
            if not (has_purl_index or has_cpe_index or has_cpe_ranges or has_fuzzy_index):
                self.logger.warning("CVE database has no populated indexes")
                return False

            # Check if Neo4j driver exists (optional integration)
            if hasattr(self, 'neo4j_driver') and self.neo4j_driver:
                try:
                    with self.neo4j_driver.session() as session:
                        result = session.run("MATCH (c:CVE) RETURN count(c) as count LIMIT 1")
                        count = result.single()['count']
                        if count == 0:
                            self.logger.warning("Neo4j CVE database is empty")
                            return False
                        self.logger.debug(f"Neo4j CVE database validated: {count} CVEs")
                except Exception as e:
                    self.logger.debug(f"Neo4j CVE validation skipped: {e}")
                    # Continue with in-memory database validation

            self.logger.debug("CVE database validation successful")
            return True

        except Exception as e:
            self.logger.warning(f"CVE database validation failed: {e}")
            return False

    def correlate_cves(self, component: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        4-stage CVE correlation with confidence scoring

        Stages:
        1. PURL → CVE (0.95 confidence)
        2. CPE exact → CVE (1.0 confidence)
        3. CPE range → CVE (0.85 confidence)
        4. Name+version fuzzy → CVE (0.6 confidence)

        Args:
            component: Component dictionary

        Returns:
            List of CVE matches with confidence scores
        """
        # Validate CVE database before attempting correlation
        if not self.validate_cve_database():
            self.logger.warning(
                f"CVE database not available, skipping correlation for component: {component.get('name', 'unknown')}"
            )
            return []

        cve_matches = []

        # Stage 1: PURL matching
        if component.get('purl'):
            purl_matches = self._match_by_purl(component['purl'])
            for cve_id in purl_matches:
                cve_matches.append({
                    'cve_id': cve_id,
                    'confidence': self.confidence_thresholds['purl_match'],
                    'match_method': 'purl',
                    'match_value': component['purl']
                })

        # Stage 2: CPE exact matching
        if component.get('cpe'):
            cpe_exact_matches = self._match_by_cpe_exact(component['cpe'])
            for cve_id in cpe_exact_matches:
                if not self._cve_already_matched(cve_id, cve_matches):
                    cve_matches.append({
                        'cve_id': cve_id,
                        'confidence': self.confidence_thresholds['cpe_exact'],
                        'match_method': 'cpe_exact',
                        'match_value': component['cpe']
                    })

        # Stage 3: CPE range matching
        if component.get('cpe'):
            cpe_range_matches = self._match_by_cpe_range(component['cpe'])
            for cve_id in cpe_range_matches:
                if not self._cve_already_matched(cve_id, cve_matches):
                    cve_matches.append({
                        'cve_id': cve_id,
                        'confidence': self.confidence_thresholds['cpe_range'],
                        'match_method': 'cpe_range',
                        'match_value': component['cpe']
                    })

        # Stage 4: Fuzzy name+version matching
        if component.get('name') and component.get('version'):
            fuzzy_matches = self._match_by_fuzzy(
                component['name'],
                component['version']
            )
            for cve_id, confidence in fuzzy_matches:
                if not self._cve_already_matched(cve_id, cve_matches):
                    cve_matches.append({
                        'cve_id': cve_id,
                        'confidence': confidence,
                        'match_method': 'fuzzy',
                        'match_value': f"{component['name']}@{component['version']}"
                    })

        self.logger.debug(f"Component {component['name']}: {len(cve_matches)} CVE matches")
        return cve_matches

    def _match_by_purl(self, purl: str) -> List[str]:
        """Match CVEs by PURL"""
        matches = []
        purl_index = self.cve_database.get('purl_index', {})

        # Exact PURL match
        if purl in purl_index:
            matches.extend(purl_index[purl])

        # Match without version qualifier
        purl_without_version = re.sub(r'@[^?]+', '', purl)
        if purl_without_version in purl_index and purl_without_version != purl:
            matches.extend(purl_index[purl_without_version])

        return list(set(matches))

    def _match_by_cpe_exact(self, cpe: str) -> List[str]:
        """Match CVEs by exact CPE"""
        cpe_index = self.cve_database.get('cpe_index', {})
        return cpe_index.get(cpe, [])

    def _match_by_cpe_range(self, cpe: str) -> List[str]:
        """Match CVEs by CPE version range"""
        matches = []

        # Parse CPE components
        cpe_parts = self._parse_cpe(cpe)
        if not cpe_parts:
            return matches

        cpe_ranges = self.cve_database.get('cpe_ranges', {})

        # Check against version ranges
        for range_key, cve_list in cpe_ranges.items():
            range_parts = self._parse_cpe(range_key)
            if not range_parts:
                continue

            # Match vendor, product, and check version range
            if (cpe_parts['vendor'] == range_parts['vendor'] and
                cpe_parts['product'] == range_parts['product']):

                if self._version_in_range(
                    cpe_parts['version'],
                    range_parts.get('version_start', ''),
                    range_parts.get('version_end', '')
                ):
                    matches.extend(cve_list)

        return list(set(matches))

    def _match_by_fuzzy(self, name: str, version: str) -> List[tuple]:
        """Match CVEs by fuzzy name and version matching"""
        matches = []
        fuzzy_index = self.cve_database.get('fuzzy_index', {})

        name_lower = name.lower()

        for indexed_name, cve_list in fuzzy_index.items():
            similarity = SequenceMatcher(None, name_lower, indexed_name.lower()).ratio()

            if similarity >= 0.85:  # High similarity threshold
                # Version exact match gets base fuzzy confidence
                # Version partial match gets reduced confidence
                for cve_id in cve_list:
                    confidence = self.confidence_thresholds['fuzzy_match'] * similarity
                    matches.append((cve_id, confidence))

        return matches

    def _parse_cpe(self, cpe: str) -> Optional[Dict[str, str]]:
        """Parse CPE string into components"""
        # CPE 2.3 format: cpe:2.3:part:vendor:product:version:...
        match = re.match(
            r'cpe:2\.3:([^:]+):([^:]+):([^:]+):([^:]+)',
            cpe
        )

        if match:
            return {
                'part': match.group(1),
                'vendor': match.group(2),
                'product': match.group(3),
                'version': match.group(4)
            }

        return None

    def _version_in_range(self, version: str, start: str, end: str) -> bool:
        """Check if version falls within range (simplified semantic versioning)"""
        if not start and not end:
            return True

        try:
            # Simple version comparison (should use packaging.version for production)
            v_parts = [int(x) for x in version.split('.')]

            if start:
                s_parts = [int(x) for x in start.split('.')]
                if v_parts < s_parts:
                    return False

            if end:
                e_parts = [int(x) for x in end.split('.')]
                if v_parts > e_parts:
                    return False

            return True
        except (ValueError, AttributeError):
            return False

    def _cve_already_matched(self, cve_id: str, matches: List[Dict]) -> bool:
        """Check if CVE already in matches list"""
        return any(m['cve_id'] == cve_id for m in matches)

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution: Parse SBOM and correlate CVEs

        Args:
            input_data: {
                'sbom_file_path': str,
                'include_cves': bool (default True)
            }

        Returns:
            {
                'components': List[Dict],
                'total_components': int,
                'total_cves': int,
                'sbom_format': str
            }
        """
        sbom_file = input_data.get('sbom_file_path')
        include_cves = input_data.get('include_cves', True)

        if not sbom_file:
            raise ValueError("sbom_file_path required in input_data")

        # Parse SBOM
        sbom_data = self.parse_sbom(sbom_file)

        # Extract components
        components = self.extract_components(sbom_data)

        # Correlate CVEs if requested
        total_cves = 0
        if include_cves:
            for component in components:
                cve_matches = self.correlate_cves(component)
                component['cve_matches'] = cve_matches
                total_cves += len(cve_matches)

        result = {
            'components': components,
            'total_components': len(components),
            'total_cves': total_cves,
            'sbom_format': sbom_data['format'],
            'sbom_file': sbom_file
        }

        self.logger.info(
            f"Processed {len(components)} components with {total_cves} CVE matches"
        )

        return result
