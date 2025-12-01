# Semantic Mapping & Probabilistic Attack Chain Design

**File**: SEMANTIC_MAPPING_PROBABILISTIC_DESIGN.md
**Created**: 2025-11-08
**Version**: 1.0.0
**Author**: System Architecture Designer
**Purpose**: Design probabilistic inference system for CWE/MITRE ATT&CK semantic mapping and attack chain calculations
**Status**: ACTIVE

---

## Executive Summary

This document specifies the architecture for a probabilistic inference system that maps CVE vulnerabilities through CWE weaknesses and CAPEC patterns to MITRE ATT&CK techniques and tactics, enabling attack chain likelihood calculations with confidence intervals for customer susceptibility assessment.

**Key Innovation**: Bayesian probabilistic graphical model combining concrete vulnerability data with inferred attack patterns to create customer-specific digital twins with quantified uncertainty.

---

## 1. Semantic Mapping Architecture

### 1.1 Core Mapping Chain

```
CVE → CWE → CAPEC → MITRE Technique → MITRE Tactic
 │      │      │           │                │
 └──────┴──────┴───────────┴────────────────┘
         Probabilistic Confidence Score
```

### 1.2 Entity Relationship Schema

```cypher
// Core vulnerability chain
(CVE)-[:EXPLOITS {confidence: float}]->(CWE)
(CWE)-[:ENABLES {likelihood: float}]->(CAPEC)
(CAPEC)-[:MAPS_TO {strength: float}]->(Technique)
(Technique)-[:ACHIEVES {probability: float}]->(Tactic)

// Supporting relationships
(Technique)-[:USES]->(Software)
(Technique)-[:TARGETS]->(DataSource)
(Mitigation)-[:MITIGATES {effectiveness: float}]->(Technique)
(ThreatActor)-[:EMPLOYS {frequency: float}]->(Technique)

// Customer context
(Customer)-[:HAS_SECTOR]->(Sector)
(Customer)-[:USES_EQUIPMENT]->(Equipment)
(Equipment)-[:HAS_CVE {confirmed: boolean}]->(CVE)
(Equipment)-[:PROBABLE_CVE {probability: float}]->(CVE)
(Sector)-[:TARGETED_BY {frequency: float}]->(ThreatActor)
```

### 1.3 Semantic Mapping Tables

#### CWE → MITRE Technique Mapping

| CWE Category | MITRE Technique | Mapping Strength | Rationale |
|--------------|-----------------|------------------|-----------|
| **CWE-79** (XSS) | T1189 (Drive-by Compromise) | 0.85 | Direct browser exploitation |
| | T1059.007 (JavaScript) | 0.75 | Script execution capability |
| **CWE-89** (SQL Injection) | T1190 (Exploit Public-Facing App) | 0.90 | Direct database access |
| | T1213 (Data from Information Repos) | 0.70 | Data exfiltration potential |
| **CWE-22** (Path Traversal) | T1083 (File and Directory Discovery) | 0.80 | File system access |
| | T1005 (Data from Local System) | 0.75 | Local data access |
| **CWE-78** (OS Command Injection) | T1059 (Command and Scripting Interpreter) | 0.95 | Direct command execution |
| | T1078 (Valid Accounts) | 0.60 | Potential privilege escalation |
| **CWE-287** (Improper Auth) | T1078 (Valid Accounts) | 0.90 | Authentication bypass |
| | T1110 (Brute Force) | 0.65 | Credential attacks |
| **CWE-502** (Deserialization) | T1059 (Command Execution) | 0.85 | Code execution via objects |
| | T1190 (Exploit Public-Facing App) | 0.80 | Remote exploitation |
| **CWE-306** (Missing Auth) | T1190 (Exploit Public-Facing App) | 0.95 | Direct unauthorized access |
| | T1078.001 (Default Accounts) | 0.70 | Default credential exploitation |
| **CWE-119** (Buffer Overflow) | T1068 (Exploitation for Privilege Escalation) | 0.85 | Memory corruption privilege escalation |
| | T1203 (Exploitation for Client Execution) | 0.75 | Code execution via overflow |
| **CWE-798** (Hardcoded Credentials) | T1078 (Valid Accounts) | 0.95 | Credential compromise |
| | T1552.001 (Credentials in Files) | 0.90 | Credential discovery |
| **CWE-434** (Unrestricted Upload) | T1105 (Ingress Tool Transfer) | 0.90 | Malicious file upload |
| | T1203 (Exploitation for Client Execution) | 0.75 | File execution potential |

**Mapping Strength Calculation**:
```
strength = base_correlation × attack_feasibility × observed_frequency
where:
  base_correlation: Logical connection strength (0.5-1.0)
  attack_feasibility: Technical difficulty inverse (0.6-1.0)
  observed_frequency: Historical attack data (0.7-1.0)
```

#### CAPEC → Technique Enhancement Mapping

| CAPEC ID | CAPEC Name | Enhanced Techniques | Strength | Notes |
|----------|------------|---------------------|----------|-------|
| CAPEC-66 | SQL Injection | T1190, T1213, T1098 | 0.88 | Multi-phase attack |
| CAPEC-88 | OS Command Injection | T1059, T1078, T1053 | 0.92 | High impact chain |
| CAPEC-63 | Cross-Site Scripting | T1189, T1059.007, T1176 | 0.83 | Browser-based attacks |
| CAPEC-180 | Exploiting Buffer Overflow | T1068, T1055, T1203 | 0.87 | Memory corruption exploits |
| CAPEC-248 | File Upload Attacks | T1105, T1203, T1059 | 0.85 | Webshell deployment |

---

## 2. Probabilistic Scoring Model

### 2.1 Bayesian Attack Chain Framework

**Core Principle**: Each hop in the attack chain represents a conditional probability:

```
P(Tactic | CVE) = Σ P(Tactic | Technique) × P(Technique | CAPEC) ×
                   P(CAPEC | CWE) × P(CWE | CVE)
```

### 2.2 Confidence Interval Calculation

#### Per-Hop Confidence

```python
class HopConfidence:
    """Confidence scoring for each attack chain hop"""

    def __init__(self, prior_confidence: float = 0.95):
        self.prior = prior_confidence
        self.evidence_weight = 0.0

    def calculate_confidence(
        self,
        mapping_strength: float,      # Semantic mapping score
        data_completeness: float,      # Available data quality
        historical_support: float,     # Observed attack patterns
        uncertainty_sources: List[str] # Known unknowns
    ) -> Tuple[float, float, float]:
        """
        Returns (point_estimate, lower_bound, upper_bound)

        Using Wilson Score Interval for binomial confidence:
        """
        # Base probability from mapping strength
        p = mapping_strength

        # Adjust for data quality
        n_effective = data_completeness * 100  # Effective sample size

        # Wilson score interval
        z = 1.96  # 95% confidence
        denominator = 1 + z**2 / n_effective
        center = (p + z**2 / (2 * n_effective)) / denominator
        margin = z * sqrt((p * (1 - p) / n_effective + z**2 / (4 * n_effective**2))) / denominator

        # Adjust for historical support
        historical_factor = 0.7 + (0.3 * historical_support)
        adjusted_center = center * historical_factor

        # Uncertainty penalty for missing data
        uncertainty_penalty = len(uncertainty_sources) * 0.05

        lower = max(0.0, adjusted_center - margin - uncertainty_penalty)
        upper = min(1.0, adjusted_center + margin)

        return (adjusted_center, lower, upper)
```

#### End-to-End Chain Confidence

```python
def calculate_chain_confidence(hops: List[HopConfidence]) -> Dict:
    """
    Calculate overall attack chain probability with confidence intervals

    Uses Monte Carlo simulation for complex probability distributions
    """
    import numpy as np

    n_simulations = 10000
    results = []

    for _ in range(n_simulations):
        # Sample from each hop's confidence interval
        chain_prob = 1.0
        for hop in hops:
            # Beta distribution for bounded probabilities
            alpha, beta = estimate_beta_params(
                hop.point_estimate,
                hop.lower_bound,
                hop.upper_bound
            )
            sample = np.random.beta(alpha, beta)
            chain_prob *= sample

        results.append(chain_prob)

    results = np.array(results)

    return {
        'mean': np.mean(results),
        'median': np.median(results),
        'ci_lower': np.percentile(results, 2.5),
        'ci_upper': np.percentile(results, 97.5),
        'std_dev': np.std(results),
        'distribution': results  # For visualization
    }

def estimate_beta_params(mean: float, lower: float, upper: float) -> Tuple[float, float]:
    """
    Estimate Beta distribution parameters from confidence interval

    Method: Method of moments with interval constraints
    """
    # Estimate variance from confidence interval
    # CI ≈ mean ± 1.96 × std for normal approximation
    std = (upper - lower) / (2 * 1.96)
    variance = std ** 2

    # Beta distribution method of moments
    if variance >= mean * (1 - mean):
        # Degenerate case, use uniform distribution
        return (1.0, 1.0)

    common = (mean * (1 - mean) / variance) - 1
    alpha = mean * common
    beta = (1 - mean) * common

    return (max(0.1, alpha), max(0.1, beta))
```

### 2.3 Attack Chain Scoring Algorithm

```python
class AttackChainScorer:
    """Calculate probabilistic attack chain likelihoods"""

    def __init__(self, graph_db):
        self.db = graph_db
        self.cache = {}

    def score_chain(
        self,
        cve_id: str,
        target_tactic: str = None,
        customer_context: Dict = None
    ) -> Dict:
        """
        Calculate attack chain probabilities from CVE to Tactics

        Args:
            cve_id: Starting CVE identifier
            target_tactic: Optional specific tactic to calculate path to
            customer_context: Customer-specific modifiers

        Returns:
            Dictionary with chains and probabilities
        """
        # Step 1: Get all paths from CVE to Tactics
        query = """
        MATCH path = (cve:CVE {id: $cve_id})-[:EXPLOITS]->(cwe:CWE)
                     -[:ENABLES]->(capec:CAPEC)
                     -[:MAPS_TO]->(tech:Technique)
                     -[:ACHIEVES]->(tactic:Tactic)
        WHERE $target_tactic IS NULL OR tactic.name = $target_tactic
        RETURN path,
               cwe, capec, tech, tactic,
               relationships(path) as rels
        """

        paths = self.db.query(query, cve_id=cve_id, target_tactic=target_tactic)

        scored_chains = []

        for path_data in paths:
            # Step 2: Calculate per-hop probabilities
            hops = []

            # CVE → CWE
            cve_cwe_conf = self._score_cve_to_cwe(
                cve_id,
                path_data['cwe'].id,
                customer_context
            )
            hops.append(cve_cwe_conf)

            # CWE → CAPEC
            cwe_capec_conf = self._score_cwe_to_capec(
                path_data['cwe'].id,
                path_data['capec'].id,
                customer_context
            )
            hops.append(cwe_capec_conf)

            # CAPEC → Technique
            capec_tech_conf = self._score_capec_to_technique(
                path_data['capec'].id,
                path_data['tech'].id,
                customer_context
            )
            hops.append(capec_tech_conf)

            # Technique → Tactic
            tech_tactic_conf = self._score_technique_to_tactic(
                path_data['tech'].id,
                path_data['tactic'].id,
                customer_context
            )
            hops.append(tech_tactic_conf)

            # Step 3: Calculate end-to-end probability
            chain_score = calculate_chain_confidence(hops)

            scored_chains.append({
                'path': path_data['path'],
                'cwe': path_data['cwe'].id,
                'capec': path_data['capec'].id,
                'technique': path_data['tech'].id,
                'tactic': path_data['tactic'].name,
                'probability': chain_score,
                'hops': hops,
                'risk_score': self._calculate_risk_score(chain_score, customer_context)
            })

        # Sort by probability (mean)
        scored_chains.sort(key=lambda x: x['probability']['mean'], reverse=True)

        return {
            'cve': cve_id,
            'total_chains': len(scored_chains),
            'chains': scored_chains,
            'summary': self._summarize_chains(scored_chains)
        }

    def _score_cve_to_cwe(self, cve_id: str, cwe_id: str, context: Dict) -> HopConfidence:
        """Score CVE → CWE hop"""
        # This is typically high confidence (direct NVD mapping)
        mapping_strength = 0.95  # Direct authoritative mapping
        data_completeness = 1.0  # NVD data is complete
        historical_support = 1.0  # Verified relationship
        uncertainty_sources = []

        conf = HopConfidence()
        point, lower, upper = conf.calculate_confidence(
            mapping_strength,
            data_completeness,
            historical_support,
            uncertainty_sources
        )

        conf.point_estimate = point
        conf.lower_bound = lower
        conf.upper_bound = upper

        return conf

    def _score_cwe_to_capec(self, cwe_id: str, capec_id: str, context: Dict) -> HopConfidence:
        """Score CWE → CAPEC hop"""
        # Query for mapping strength
        query = """
        MATCH (cwe:CWE {id: $cwe_id})-[r:ENABLES]->(capec:CAPEC {id: $capec_id})
        RETURN r.likelihood as strength
        """
        result = self.db.query_single(query, cwe_id=cwe_id, capec_id=capec_id)

        mapping_strength = result.get('strength', 0.75)  # Default moderate strength

        # CWE-CAPEC mappings are well-documented but less direct
        data_completeness = 0.85

        # Check historical attack data
        historical_support = self._get_historical_support(cwe_id, capec_id)

        uncertainty_sources = []
        if not result:
            uncertainty_sources.append("no_explicit_mapping")

        conf = HopConfidence()
        point, lower, upper = conf.calculate_confidence(
            mapping_strength,
            data_completeness,
            historical_support,
            uncertainty_sources
        )

        conf.point_estimate = point
        conf.lower_bound = lower
        conf.upper_bound = upper

        return conf

    def _score_capec_to_technique(self, capec_id: str, tech_id: str, context: Dict) -> HopConfidence:
        """Score CAPEC → MITRE Technique hop"""
        # This is our semantic mapping (less authoritative)
        mapping_strength = self._get_semantic_mapping_strength(capec_id, tech_id)

        # Data completeness depends on CAPEC coverage
        data_completeness = 0.70  # Partial coverage

        # Historical support from threat intelligence
        historical_support = self._get_historical_support(capec_id, tech_id)

        uncertainty_sources = ["semantic_inference"]

        # Adjust based on customer sector
        if context and 'sector' in context:
            sector_modifier = self._get_sector_modifier(tech_id, context['sector'])
            mapping_strength *= sector_modifier

        conf = HopConfidence()
        point, lower, upper = conf.calculate_confidence(
            mapping_strength,
            data_completeness,
            historical_support,
            uncertainty_sources
        )

        conf.point_estimate = point
        conf.lower_bound = lower
        conf.upper_bound = upper

        return conf

    def _score_technique_to_tactic(self, tech_id: str, tactic_name: str, context: Dict) -> HopConfidence:
        """Score MITRE Technique → Tactic hop"""
        # This is direct MITRE mapping (authoritative)
        mapping_strength = 1.0
        data_completeness = 1.0
        historical_support = 1.0
        uncertainty_sources = []

        conf = HopConfidence()
        point, lower, upper = conf.calculate_confidence(
            mapping_strength,
            data_completeness,
            historical_support,
            uncertainty_sources
        )

        conf.point_estimate = point
        conf.lower_bound = lower
        conf.upper_bound = upper

        return conf

    def _get_semantic_mapping_strength(self, capec_id: str, tech_id: str) -> float:
        """Get semantic mapping strength from lookup table"""
        # Use mapping table from Section 1.3
        mapping_table = {
            ('CAPEC-66', 'T1190'): 0.90,
            ('CAPEC-66', 'T1213'): 0.70,
            ('CAPEC-88', 'T1059'): 0.95,
            ('CAPEC-88', 'T1078'): 0.60,
            ('CAPEC-63', 'T1189'): 0.85,
            ('CAPEC-63', 'T1059.007'): 0.75,
            # ... full table
        }

        return mapping_table.get((capec_id, tech_id), 0.50)  # Default low confidence

    def _get_historical_support(self, source_id: str, target_id: str) -> float:
        """Query historical attack data for relationship support"""
        # Query threat intelligence database
        query = """
        MATCH (threat:ThreatActor)-[:EMPLOYS]->(tech:Technique {id: $tech_id})
        RETURN count(threat) as actor_count
        """
        # Placeholder - would integrate with real threat intel
        return 0.80  # Default moderate support

    def _get_sector_modifier(self, tech_id: str, sector: str) -> float:
        """Sector-specific technique likelihood modifier"""
        # Sector-technique targeting frequency
        sector_modifiers = {
            ('financial', 'T1078'): 1.3,      # Finance heavily targeted for credential theft
            ('financial', 'T1190'): 1.2,      # Public-facing app exploits common
            ('healthcare', 'T1486'): 1.4,     # Ransomware targeting
            ('manufacturing', 'T1059'): 1.1,  # Command execution in OT environments
            ('government', 'T1566'): 1.3,     # Phishing campaigns
            # ... comprehensive mapping
        }

        return sector_modifiers.get((sector.lower(), tech_id), 1.0)

    def _calculate_risk_score(self, chain_score: Dict, context: Dict) -> Dict:
        """
        Calculate business risk score from technical probability

        Risk = Probability × Impact × Exposure
        """
        probability = chain_score['mean']

        # Impact scoring (CVSS-like)
        impact = context.get('impact', {
            'confidentiality': 0.7,
            'integrity': 0.7,
            'availability': 0.7
        })

        impact_score = (
            impact['confidentiality'] * 0.4 +
            impact['integrity'] * 0.3 +
            impact['availability'] * 0.3
        )

        # Exposure (customer-specific)
        exposure = context.get('exposure', 0.5)  # Default medium exposure

        risk_score = probability * impact_score * exposure

        # Risk levels
        if risk_score > 0.7:
            risk_level = "CRITICAL"
        elif risk_score > 0.5:
            risk_level = "HIGH"
        elif risk_score > 0.3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            'score': risk_score,
            'level': risk_level,
            'probability': probability,
            'impact': impact_score,
            'exposure': exposure
        }

    def _summarize_chains(self, chains: List[Dict]) -> Dict:
        """Generate summary statistics across all chains"""
        if not chains:
            return {}

        tactics = {}
        techniques = {}

        for chain in chains:
            tactic = chain['tactic']
            tech = chain['technique']
            prob = chain['probability']['mean']

            if tactic not in tactics:
                tactics[tactic] = {'total_prob': 0, 'count': 0, 'max_prob': 0}
            tactics[tactic]['total_prob'] += prob
            tactics[tactic]['count'] += 1
            tactics[tactic]['max_prob'] = max(tactics[tactic]['max_prob'], prob)

            if tech not in techniques:
                techniques[tech] = {'total_prob': 0, 'count': 0}
            techniques[tech]['total_prob'] += prob
            techniques[tech]['count'] += 1

        # Calculate aggregated probabilities
        for tactic in tactics:
            # Use max probability (most likely attack path to tactic)
            tactics[tactic]['aggregate_prob'] = tactics[tactic]['max_prob']

        for tech in techniques:
            # Average probability across chains
            techniques[tech]['aggregate_prob'] = (
                techniques[tech]['total_prob'] / techniques[tech]['count']
            )

        return {
            'tactics': tactics,
            'techniques': techniques,
            'most_likely_tactic': max(tactics.items(), key=lambda x: x[1]['aggregate_prob'])[0],
            'most_likely_technique': max(techniques.items(), key=lambda x: x[1]['aggregate_prob'])[0]
        }
```

---

## 3. Customer Susceptibility Inference Model

### 3.1 Inference Without Complete Data

**Challenge**: Customers often lack:
- Complete SBOM (software bill of materials)
- Specific version numbers
- Full infrastructure inventory
- Real-time vulnerability scanning

**Solution**: Bayesian inference with priors from sector/vendor patterns

### 3.2 Sector-Based Probability Model

```python
class SectorInferenceModel:
    """Infer customer vulnerabilities from sector characteristics"""

    def __init__(self):
        self.sector_profiles = self._load_sector_profiles()
        self.vendor_profiles = self._load_vendor_profiles()

    def infer_customer_susceptibility(
        self,
        customer: Dict,
        available_data: Dict
    ) -> Dict:
        """
        Infer customer vulnerability landscape

        Args:
            customer: {
                'sector': str,
                'size': str,  # small, medium, large, enterprise
                'known_vendors': List[str],
                'known_equipment': List[Dict],
                'confirmed_cves': List[str]
            }
            available_data: {
                'has_sbom': bool,
                'scan_date': datetime,
                'infrastructure_detail': str  # none, partial, complete
            }

        Returns:
            Inferred vulnerability profile with confidence intervals
        """
        sector = customer['sector']
        size = customer['size']

        # Step 1: Sector baseline
        sector_baseline = self._get_sector_baseline(sector, size)

        # Step 2: Vendor-specific adjustments
        vendor_adjustments = self._infer_from_vendors(customer['known_vendors'])

        # Step 3: Equipment-based inference
        equipment_vulns = self._infer_from_equipment(customer['known_equipment'])

        # Step 4: Bayesian update with confirmed CVEs
        if customer['confirmed_cves']:
            posterior = self._bayesian_update(
                sector_baseline,
                vendor_adjustments,
                equipment_vulns,
                customer['confirmed_cves']
            )
        else:
            posterior = self._combine_priors(
                sector_baseline,
                vendor_adjustments,
                equipment_vulns
            )

        # Step 5: Confidence adjustment based on data availability
        confidence_penalty = self._calculate_confidence_penalty(available_data)

        return {
            'inferred_cves': posterior['likely_cves'],
            'confidence': posterior['confidence'] * (1 - confidence_penalty),
            'sector_baseline': sector_baseline,
            'vendor_influence': vendor_adjustments,
            'equipment_influence': equipment_vulns,
            'data_completeness': 1 - confidence_penalty
        }

    def _get_sector_baseline(self, sector: str, size: str) -> Dict:
        """
        Get baseline vulnerability distribution for sector

        Based on:
        - CISA KEV (Known Exploited Vulnerabilities)
        - Sector-specific threat reports
        - Historical breach data
        """
        profile = self.sector_profiles.get(sector, {})

        # Top CVEs by sector (example data)
        sector_cve_frequencies = {
            'financial': {
                'CVE-2021-44228': 0.85,  # Log4Shell - widespread
                'CVE-2022-30190': 0.65,  # Follina - Office exploitation
                'CVE-2023-34362': 0.55,  # MOVEit - file transfer
                'CVE-2021-26855': 0.70,  # ProxyLogon - Exchange
            },
            'healthcare': {
                'CVE-2021-44228': 0.80,  # Log4Shell
                'CVE-2023-34362': 0.60,  # MOVEit
                'CVE-2022-41040': 0.50,  # ProxyNotShell
                'CVE-2020-0601': 0.45,  # CryptoAPI
            },
            'manufacturing': {
                'CVE-2021-44228': 0.75,  # Log4Shell
                'CVE-2022-22965': 0.60,  # Spring4Shell
                'CVE-2021-42013': 0.55,  # Path traversal
                'CVE-2023-23397': 0.50,  # Outlook elevation
            },
            # ... more sectors
        }

        base_cves = sector_cve_frequencies.get(sector, {})

        # Size modifier (larger orgs have more attack surface)
        size_multiplier = {
            'small': 0.6,
            'medium': 0.8,
            'large': 1.0,
            'enterprise': 1.2
        }.get(size, 1.0)

        return {
            'likely_cves': {
                cve: prob * size_multiplier
                for cve, prob in base_cves.items()
            },
            'confidence': 0.60,  # Moderate confidence from sector alone
            'basis': 'sector_statistics'
        }

    def _infer_from_vendors(self, vendors: List[str]) -> Dict:
        """
        Infer likely vulnerabilities from vendor/equipment list

        Even without specific versions, vendors indicate likely CVE exposure
        """
        vendor_cve_map = {
            'Microsoft': {
                'CVE-2021-26855': 0.70,  # Exchange
                'CVE-2022-30190': 0.65,  # Follina
                'CVE-2023-23397': 0.60,  # Outlook
                'CVE-2020-0601': 0.55,  # CryptoAPI
            },
            'Apache': {
                'CVE-2021-44228': 0.90,  # Log4Shell
                'CVE-2022-22965': 0.70,  # Spring4Shell
                'CVE-2021-42013': 0.65,  # Path traversal
            },
            'Cisco': {
                'CVE-2023-20198': 0.75,  # IOS XE
                'CVE-2023-20273': 0.70,  # Command injection
                'CVE-2022-20928': 0.60,  # ASA/FTD
            },
            'VMware': {
                'CVE-2022-22954': 0.80,  # Workspace ONE
                'CVE-2021-22005': 0.75,  # vCenter
                'CVE-2023-20887': 0.70,  # Aria Operations
            },
            # ... comprehensive vendor mapping
        }

        aggregated_cves = {}

        for vendor in vendors:
            vendor_cves = vendor_cve_map.get(vendor, {})
            for cve, prob in vendor_cves.items():
                if cve not in aggregated_cves:
                    aggregated_cves[cve] = []
                aggregated_cves[cve].append(prob)

        # Combine probabilities (use max for each CVE)
        final_cves = {
            cve: max(probs)
            for cve, probs in aggregated_cves.items()
        }

        return {
            'likely_cves': final_cves,
            'confidence': 0.70,  # Good confidence from vendor presence
            'basis': 'vendor_patterns'
        }

    def _infer_from_equipment(self, equipment: List[Dict]) -> Dict:
        """
        Infer vulnerabilities from known equipment types

        equipment = [
            {'type': 'firewall', 'vendor': 'Cisco', 'model': 'ASA', 'version': None},
            {'type': 'web_server', 'vendor': 'Apache', 'model': None, 'version': '2.4'},
            ...
        ]
        """
        equipment_cves = {}

        for item in equipment:
            vendor = item.get('vendor')
            eq_type = item.get('type')
            version = item.get('version')

            # Query CVE database for equipment-specific vulnerabilities
            if version:
                # Specific version - high confidence
                query = """
                MATCH (cve:CVE)-[:AFFECTS]->(product)
                WHERE product.vendor = $vendor
                  AND product.version =~ $version_pattern
                RETURN cve.id, cve.severity, cve.exploitability
                """
                # Execute query and add to equipment_cves with high confidence
                confidence = 0.85
            else:
                # No version - infer from vendor and type
                # Use historical vulnerability patterns
                confidence = 0.50

            # Add inferred CVEs with confidence scores
            # ...

        return {
            'likely_cves': equipment_cves,
            'confidence': 0.65,
            'basis': 'equipment_inference'
        }

    def _bayesian_update(
        self,
        sector_baseline: Dict,
        vendor_adjustments: Dict,
        equipment_vulns: Dict,
        confirmed_cves: List[str]
    ) -> Dict:
        """
        Bayesian update: Use confirmed CVEs to refine inferences

        P(CVE | confirmed_CVEs) = P(confirmed_CVEs | CVE) × P(CVE) / P(confirmed_CVEs)

        Logic: If we know customer has CVE-A, what does that tell us about CVE-B?
        - Co-occurrence patterns (same vendor/product)
        - Attack chain sequences (CVE-A enables CVE-B exploitation)
        - Infrastructure patterns (presence of A implies presence of B)
        """
        # Combine priors
        prior = self._combine_priors(sector_baseline, vendor_adjustments, equipment_vulns)

        # Calculate likelihood based on confirmed CVEs
        for confirmed_cve in confirmed_cves:
            # Query co-occurrence patterns
            co_occurrence = self._get_cve_co_occurrence(confirmed_cve)

            # Update probabilities
            for cve, prior_prob in prior['likely_cves'].items():
                if cve in co_occurrence:
                    # Bayesian update
                    likelihood = co_occurrence[cve]
                    posterior_prob = (likelihood * prior_prob) / (
                        likelihood * prior_prob + (1 - likelihood) * (1 - prior_prob)
                    )
                    prior['likely_cves'][cve] = posterior_prob

        # Increase confidence due to confirmed data
        prior['confidence'] = min(0.95, prior['confidence'] * 1.3)

        return prior

    def _combine_priors(
        self,
        sector_baseline: Dict,
        vendor_adjustments: Dict,
        equipment_vulns: Dict
    ) -> Dict:
        """
        Combine multiple prior distributions

        Uses weighted geometric mean for probability combination
        """
        all_cves = set()
        all_cves.update(sector_baseline['likely_cves'].keys())
        all_cves.update(vendor_adjustments['likely_cves'].keys())
        all_cves.update(equipment_vulns['likely_cves'].keys())

        combined = {}

        for cve in all_cves:
            probs = []
            weights = []

            if cve in sector_baseline['likely_cves']:
                probs.append(sector_baseline['likely_cves'][cve])
                weights.append(sector_baseline['confidence'])

            if cve in vendor_adjustments['likely_cves']:
                probs.append(vendor_adjustments['likely_cves'][cve])
                weights.append(vendor_adjustments['confidence'])

            if cve in equipment_vulns['likely_cves']:
                probs.append(equipment_vulns['likely_cves'][cve])
                weights.append(equipment_vulns['confidence'])

            # Weighted geometric mean
            import numpy as np
            if probs:
                total_weight = sum(weights)
                normalized_weights = [w / total_weight for w in weights]

                # Geometric mean: (p1^w1 × p2^w2 × ...)
                log_probs = [np.log(p) for p in probs]
                weighted_log_prob = sum(w * lp for w, lp in zip(normalized_weights, log_probs))
                combined_prob = np.exp(weighted_log_prob)

                combined[cve] = combined_prob

        # Overall confidence is weighted average of component confidences
        total_weight = (
            sector_baseline['confidence'] +
            vendor_adjustments['confidence'] +
            equipment_vulns['confidence']
        )

        avg_confidence = total_weight / 3

        return {
            'likely_cves': combined,
            'confidence': avg_confidence,
            'basis': 'combined_inference'
        }

    def _get_cve_co_occurrence(self, cve_id: str) -> Dict[str, float]:
        """
        Get CVEs that frequently co-occur with given CVE

        Based on:
        - Same product/vendor
        - Same attack campaigns
        - Common infrastructure patterns
        """
        # Query threat intelligence for co-occurrence patterns
        query = """
        MATCH (cve1:CVE {id: $cve_id})-[:AFFECTS]->(product)<-[:AFFECTS]-(cve2:CVE)
        WHERE cve1 <> cve2
        RETURN cve2.id, count(*) as co_occurrence_count
        ORDER BY co_occurrence_count DESC
        LIMIT 50
        """

        # Convert counts to probabilities
        # ...

        return {
            'CVE-2021-44228': 0.75,  # Example: Log4Shell co-occurs with other Apache CVEs
            'CVE-2022-22965': 0.65,
            # ...
        }

    def _calculate_confidence_penalty(self, available_data: Dict) -> float:
        """
        Reduce confidence based on missing data

        Complete data = 0% penalty
        No data = 50% penalty
        """
        penalty = 0.0

        if not available_data.get('has_sbom'):
            penalty += 0.20  # No SBOM = 20% confidence reduction

        infrastructure_detail = available_data.get('infrastructure_detail', 'none')
        if infrastructure_detail == 'none':
            penalty += 0.25
        elif infrastructure_detail == 'partial':
            penalty += 0.10

        scan_date = available_data.get('scan_date')
        if scan_date:
            from datetime import datetime, timedelta
            age_days = (datetime.now() - scan_date).days
            if age_days > 90:
                penalty += 0.15  # Stale data
        else:
            penalty += 0.20  # No scan data

        return min(0.50, penalty)  # Cap at 50% reduction
```

### 3.3 Historical Attack Pattern Matching

```python
class AttackPatternMatcher:
    """Match customer profile to historical attack patterns"""

    def __init__(self, threat_intel_db):
        self.threat_db = threat_intel_db

    def match_attack_patterns(
        self,
        customer_profile: Dict,
        inferred_cves: Dict
    ) -> Dict:
        """
        Match customer to historical attack campaigns

        Returns:
            {
                'matched_campaigns': List[Dict],
                'technique_likelihoods': Dict[str, float],
                'threat_actors': List[str]
            }
        """
        sector = customer_profile['sector']
        size = customer_profile['size']

        # Query historical campaigns targeting similar profiles
        query = """
        MATCH (campaign:Campaign)-[:TARGETS]->(sector:Sector {name: $sector})
        MATCH (campaign)-[:USES_CVE]->(cve:CVE)
        MATCH (campaign)-[:EMPLOYS]->(technique:Technique)
        MATCH (campaign)-[:ATTRIBUTED_TO]->(actor:ThreatActor)
        WHERE cve.id IN $inferred_cves
        RETURN campaign, collect(DISTINCT cve.id) as cves,
               collect(DISTINCT technique.id) as techniques,
               collect(DISTINCT actor.name) as actors
        ORDER BY size(cves) DESC
        """

        campaigns = self.threat_db.query(
            query,
            sector=sector,
            inferred_cves=list(inferred_cves.keys())
        )

        # Calculate technique likelihoods based on campaign matches
        technique_counts = {}
        for campaign in campaigns:
            match_score = len(campaign['cves']) / len(inferred_cves)
            for tech in campaign['techniques']:
                if tech not in technique_counts:
                    technique_counts[tech] = []
                technique_counts[tech].append(match_score)

        technique_likelihoods = {
            tech: sum(scores) / len(scores)
            for tech, scores in technique_counts.items()
        }

        return {
            'matched_campaigns': campaigns,
            'technique_likelihoods': technique_likelihoods,
            'threat_actors': list(set(
                actor for c in campaigns for actor in c['actors']
            ))
        }
```

---

## 4. Digital Twin Abstraction Model

### 4.1 Layered Digital Twin Architecture

```
┌─────────────────────────────────────────────┐
│         DIGITAL TWIN LAYERS                 │
├─────────────────────────────────────────────┤
│  Layer 1: CONCRETE (Confirmed Facts)        │
│  - Known CVEs from scans                    │
│  - Confirmed equipment with versions        │
│  - Validated infrastructure                 │
│  Confidence: 0.90-1.00                      │
├─────────────────────────────────────────────┤
│  Layer 2: INFERRED (High Probability)       │
│  - Vendor-based CVE inference               │
│  - Sector-typical vulnerabilities           │
│  - Equipment-pattern CVEs                   │
│  Confidence: 0.70-0.90                      │
├─────────────────────────────────────────────┤
│  Layer 3: PROBABILISTIC (Modeled)           │
│  - Attack chain probabilities               │
│  - Technique likelihood estimates           │
│  - Tactic reachability scores               │
│  Confidence: 0.50-0.70                      │
├─────────────────────────────────────────────┤
│  Layer 4: SPECULATIVE (Low Confidence)      │
│  - Emerging threat patterns                 │
│  - Zero-day risk estimates                  │
│  - Novel attack vectors                     │
│  Confidence: 0.30-0.50                      │
└─────────────────────────────────────────────┘
```

### 4.2 Digital Twin Schema

```python
class CustomerDigitalTwin:
    """
    Probabilistic digital twin of customer security posture

    Combines concrete data with inferred vulnerabilities and
    attack chain probabilities
    """

    def __init__(self, customer_id: str, graph_db):
        self.customer_id = customer_id
        self.db = graph_db
        self.layers = {
            'concrete': {},
            'inferred': {},
            'probabilistic': {},
            'speculative': {}
        }
        self.metadata = {
            'created': datetime.now(),
            'last_updated': None,
            'data_sources': [],
            'confidence_score': 0.0
        }

    def build_twin(
        self,
        customer_data: Dict,
        scan_results: Dict = None,
        threat_intel: Dict = None
    ) -> None:
        """
        Construct digital twin from available data

        Args:
            customer_data: Basic customer info (sector, vendors, etc.)
            scan_results: Optional vulnerability scan results
            threat_intel: Optional threat intelligence feeds
        """
        # Layer 1: Concrete facts
        if scan_results:
            self.layers['concrete'] = self._build_concrete_layer(scan_results)
            self.metadata['data_sources'].append('vulnerability_scan')

        # Layer 2: Inferred vulnerabilities
        inference_model = SectorInferenceModel()
        inferred = inference_model.infer_customer_susceptibility(
            customer_data,
            available_data={
                'has_sbom': scan_results is not None,
                'scan_date': scan_results.get('scan_date') if scan_results else None,
                'infrastructure_detail': scan_results.get('detail_level', 'none') if scan_results else 'none'
            }
        )
        self.layers['inferred'] = inferred
        self.metadata['data_sources'].append('sector_inference')

        # Layer 3: Probabilistic attack chains
        attack_scorer = AttackChainScorer(self.db)

        # Combine concrete and inferred CVEs
        all_cves = list(self.layers['concrete'].get('cves', {}).keys())
        all_cves.extend(self.layers['inferred']['inferred_cves'].keys())

        attack_chains = {}
        for cve in all_cves[:50]:  # Limit for performance
            chains = attack_scorer.score_chain(
                cve,
                customer_context={
                    'sector': customer_data['sector'],
                    'size': customer_data['size']
                }
            )
            attack_chains[cve] = chains

        self.layers['probabilistic'] = {
            'attack_chains': attack_chains,
            'aggregated_tactics': self._aggregate_tactics(attack_chains),
            'aggregated_techniques': self._aggregate_techniques(attack_chains)
        }
        self.metadata['data_sources'].append('attack_chain_modeling')

        # Layer 4: Speculative threats
        if threat_intel:
            pattern_matcher = AttackPatternMatcher(self.db)
            matched_patterns = pattern_matcher.match_attack_patterns(
                customer_data,
                self.layers['inferred']['inferred_cves']
            )
            self.layers['speculative'] = {
                'emerging_techniques': matched_patterns['technique_likelihoods'],
                'threat_actors': matched_patterns['threat_actors'],
                'campaign_matches': matched_patterns['matched_campaigns']
            }
            self.metadata['data_sources'].append('threat_intelligence')

        # Calculate overall confidence
        self.metadata['confidence_score'] = self._calculate_overall_confidence()
        self.metadata['last_updated'] = datetime.now()

    def _build_concrete_layer(self, scan_results: Dict) -> Dict:
        """Extract confirmed vulnerabilities from scan results"""
        return {
            'cves': {
                cve['id']: {
                    'severity': cve['severity'],
                    'cvss_score': cve['cvss'],
                    'affected_assets': cve['assets'],
                    'confidence': 1.0  # Confirmed by scan
                }
                for cve in scan_results.get('vulnerabilities', [])
            },
            'equipment': scan_results.get('discovered_equipment', []),
            'network_topology': scan_results.get('topology', {})
        }

    def _aggregate_tactics(self, attack_chains: Dict) -> Dict:
        """
        Aggregate tactic probabilities across all CVEs

        Returns combined probability of reaching each tactic
        """
        tactic_probs = {}

        for cve, chains in attack_chains.items():
            for chain in chains.get('chains', []):
                tactic = chain['tactic']
                prob = chain['probability']['mean']

                if tactic not in tactic_probs:
                    tactic_probs[tactic] = []
                tactic_probs[tactic].append(prob)

        # Use maximum probability for each tactic (most likely path)
        return {
            tactic: {
                'max_probability': max(probs),
                'mean_probability': sum(probs) / len(probs),
                'path_count': len(probs)
            }
            for tactic, probs in tactic_probs.items()
        }

    def _aggregate_techniques(self, attack_chains: Dict) -> Dict:
        """Aggregate technique probabilities across all CVEs"""
        tech_probs = {}

        for cve, chains in attack_chains.items():
            for chain in chains.get('chains', []):
                tech = chain['technique']
                prob = chain['probability']['mean']

                if tech not in tech_probs:
                    tech_probs[tech] = []
                tech_probs[tech].append(prob)

        return {
            tech: {
                'max_probability': max(probs),
                'mean_probability': sum(probs) / len(probs),
                'cve_count': len(probs)
            }
            for tech, probs in tech_probs.items()
        }

    def _calculate_overall_confidence(self) -> float:
        """
        Calculate weighted confidence score across all layers

        Weights:
        - Concrete: 1.0
        - Inferred: 0.7
        - Probabilistic: 0.5
        - Speculative: 0.3
        """
        weights = {
            'concrete': 1.0,
            'inferred': 0.7,
            'probabilistic': 0.5,
            'speculative': 0.3
        }

        total_weight = 0.0
        weighted_sum = 0.0

        for layer, weight in weights.items():
            if layer in self.layers and self.layers[layer]:
                layer_confidence = self.layers[layer].get('confidence', 0.5)
                weighted_sum += layer_confidence * weight
                total_weight += weight

        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def get_risk_assessment(self) -> Dict:
        """
        Generate comprehensive risk assessment from digital twin

        Returns:
            {
                'overall_risk': str,  # CRITICAL, HIGH, MEDIUM, LOW
                'risk_score': float,  # 0.0-1.0
                'confidence': float,
                'top_threats': List[Dict],
                'recommended_actions': List[Dict]
            }
        """
        # Aggregate tactics by probability
        tactics = self.layers['probabilistic']['aggregated_tactics']

        # Calculate overall risk score
        # Weight by tactic severity (Initial Access > Execution > ...)
        tactic_severity_weights = {
            'Initial Access': 1.0,
            'Execution': 0.9,
            'Persistence': 0.8,
            'Privilege Escalation': 0.9,
            'Defense Evasion': 0.7,
            'Credential Access': 0.95,
            'Discovery': 0.5,
            'Lateral Movement': 0.85,
            'Collection': 0.7,
            'Command and Control': 0.8,
            'Exfiltration': 0.9,
            'Impact': 1.0
        }

        weighted_risk = 0.0
        total_weight = 0.0

        for tactic, tactic_data in tactics.items():
            weight = tactic_severity_weights.get(tactic, 0.5)
            prob = tactic_data['max_probability']
            weighted_risk += prob * weight
            total_weight += weight

        risk_score = weighted_risk / total_weight if total_weight > 0 else 0.0

        # Risk level categorization
        if risk_score > 0.75:
            risk_level = "CRITICAL"
        elif risk_score > 0.60:
            risk_level = "HIGH"
        elif risk_score > 0.40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # Identify top threats
        top_threats = []

        # From concrete CVEs
        for cve, data in self.layers['concrete'].get('cves', {}).items():
            if data['cvss_score'] >= 7.0:
                top_threats.append({
                    'type': 'confirmed_vulnerability',
                    'id': cve,
                    'severity': data['severity'],
                    'confidence': 1.0,
                    'priority': 'IMMEDIATE'
                })

        # From attack chains
        for tactic, data in sorted(
            tactics.items(),
            key=lambda x: x[1]['max_probability'],
            reverse=True
        )[:5]:
            if data['max_probability'] > 0.6:
                top_threats.append({
                    'type': 'attack_chain',
                    'tactic': tactic,
                    'probability': data['max_probability'],
                    'confidence': self.metadata['confidence_score'],
                    'priority': 'HIGH' if data['max_probability'] > 0.75 else 'MEDIUM'
                })

        # Recommended actions
        recommended_actions = self._generate_recommendations(top_threats)

        return {
            'overall_risk': risk_level,
            'risk_score': risk_score,
            'confidence': self.metadata['confidence_score'],
            'top_threats': sorted(top_threats, key=lambda x: x.get('probability', 1.0), reverse=True)[:10],
            'recommended_actions': recommended_actions,
            'digital_twin_metadata': self.metadata
        }

    def _generate_recommendations(self, threats: List[Dict]) -> List[Dict]:
        """Generate prioritized mitigation recommendations"""
        recommendations = []

        for threat in threats:
            if threat['type'] == 'confirmed_vulnerability':
                recommendations.append({
                    'action': 'PATCH',
                    'target': threat['id'],
                    'priority': threat['priority'],
                    'description': f"Apply security patch for {threat['id']}",
                    'estimated_risk_reduction': 0.9
                })
            elif threat['type'] == 'attack_chain':
                # Query mitigations for tactic
                mitigations = self._get_tactic_mitigations(threat['tactic'])
                for mitigation in mitigations:
                    recommendations.append({
                        'action': 'IMPLEMENT_CONTROL',
                        'target': threat['tactic'],
                        'control': mitigation['name'],
                        'priority': threat['priority'],
                        'description': mitigation['description'],
                        'estimated_risk_reduction': mitigation['effectiveness']
                    })

        # Deduplicate and prioritize
        return sorted(
            recommendations,
            key=lambda x: (
                x['priority'] == 'IMMEDIATE',
                x['priority'] == 'HIGH',
                x['estimated_risk_reduction']
            ),
            reverse=True
        )[:15]

    def _get_tactic_mitigations(self, tactic: str) -> List[Dict]:
        """Query MITRE mitigations for tactic"""
        query = """
        MATCH (tactic:Tactic {name: $tactic})<-[:ACHIEVES]-(technique:Technique)
        MATCH (mitigation:Mitigation)-[r:MITIGATES]->(technique)
        RETURN DISTINCT mitigation.name as name,
               mitigation.description as description,
               avg(r.effectiveness) as effectiveness
        ORDER BY effectiveness DESC
        LIMIT 5
        """

        results = self.db.query(query, tactic=tactic)

        return [
            {
                'name': r['name'],
                'description': r['description'],
                'effectiveness': r['effectiveness']
            }
            for r in results
        ]

    def export_twin(self, format: str = 'json') -> str:
        """Export digital twin for persistence or API response"""
        import json
        from datetime import datetime

        def datetime_handler(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        twin_data = {
            'customer_id': self.customer_id,
            'metadata': self.metadata,
            'layers': self.layers,
            'risk_assessment': self.get_risk_assessment()
        }

        if format == 'json':
            return json.dumps(twin_data, indent=2, default=datetime_handler)
        elif format == 'cypher':
            # Generate Cypher statements to persist twin in Neo4j
            return self._generate_cypher_export(twin_data)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _generate_cypher_export(self, twin_data: Dict) -> str:
        """Generate Cypher CREATE statements for Neo4j persistence"""
        cypher_statements = []

        # Create DigitalTwin node
        cypher_statements.append(f"""
        MERGE (dt:DigitalTwin {{customer_id: '{self.customer_id}'}})
        SET dt.created = datetime('{self.metadata['created'].isoformat()}'),
            dt.last_updated = datetime('{self.metadata['last_updated'].isoformat()}'),
            dt.confidence_score = {self.metadata['confidence_score']},
            dt.overall_risk = '{twin_data['risk_assessment']['overall_risk']}',
            dt.risk_score = {twin_data['risk_assessment']['risk_score']}
        """)

        # Create relationships to CVEs (both concrete and inferred)
        for cve_id, data in twin_data['layers']['concrete'].get('cves', {}).items():
            cypher_statements.append(f"""
            MATCH (dt:DigitalTwin {{customer_id: '{self.customer_id}'}}),
                  (cve:CVE {{id: '{cve_id}'}})
            MERGE (dt)-[r:HAS_CONFIRMED_CVE]->(cve)
            SET r.confidence = {data['confidence']},
                r.cvss_score = {data['cvss_score']}
            """)

        for cve_id, prob in twin_data['layers']['inferred']['inferred_cves'].items():
            cypher_statements.append(f"""
            MATCH (dt:DigitalTwin {{customer_id: '{self.customer_id}'}}),
                  (cve:CVE {{id: '{cve_id}'}})
            MERGE (dt)-[r:HAS_INFERRED_CVE]->(cve)
            SET r.probability = {prob},
                r.confidence = {twin_data['layers']['inferred']['confidence']}
            """)

        # Create relationships to Tactics with probabilities
        for tactic, data in twin_data['layers']['probabilistic']['aggregated_tactics'].items():
            cypher_statements.append(f"""
            MATCH (dt:DigitalTwin {{customer_id: '{self.customer_id}'}}),
                  (tactic:Tactic {{name: '{tactic}'}})
            MERGE (dt)-[r:SUSCEPTIBLE_TO_TACTIC]->(tactic)
            SET r.max_probability = {data['max_probability']},
                r.mean_probability = {data['mean_probability']},
                r.path_count = {data['path_count']}
            """)

        return "\n\n".join(cypher_statements)
```

---

## 5. Mathematical Framework

### 5.1 Bayesian Probabilistic Graphical Model

**Graph Structure**:
```
      Sector ────> Customer ────> Equipment
         │             │              │
         │             │              │
         ▼             ▼              ▼
    Threat ───────> CVE ──────────> CWE
      Actor           │              │
                      │              │
                      ▼              ▼
                   CAPEC ─────> Technique ────> Tactic
                                    │
                                    │
                                    ▼
                               Mitigation
```

**Joint Probability Distribution**:
```
P(Tactic, Technique, CAPEC, CWE, CVE, Equipment, Sector, ThreatActor) =
  P(Sector) ×
  P(Equipment | Sector) ×
  P(CVE | Equipment, Sector) ×
  P(CWE | CVE) ×
  P(CAPEC | CWE) ×
  P(Technique | CAPEC, ThreatActor) ×
  P(Tactic | Technique) ×
  P(ThreatActor | Sector)
```

### 5.2 Inference Algorithms

#### Variable Elimination for Marginal Probabilities

```python
def variable_elimination(
    graphical_model: BayesianNetwork,
    query_variable: str,
    evidence: Dict[str, Any]
) -> Distribution:
    """
    Compute P(query_variable | evidence) using variable elimination

    Algorithm:
    1. Restrict factors to evidence values
    2. Multiply factors together
    3. Sum out variables in elimination order
    4. Normalize result
    """
    factors = graphical_model.get_factors()

    # Step 1: Restrict factors to evidence
    restricted_factors = [
        factor.restrict(evidence) for factor in factors
    ]

    # Step 2: Determine elimination order (min-fill heuristic)
    elimination_order = compute_elimination_order(
        restricted_factors,
        query_variable
    )

    # Step 3: Eliminate variables
    for var in elimination_order:
        if var == query_variable:
            continue

        # Find factors containing var
        relevant_factors = [
            f for f in restricted_factors if var in f.variables
        ]

        # Multiply relevant factors
        product = multiply_factors(relevant_factors)

        # Sum out var
        marginalized = product.sum_out(var)

        # Replace relevant factors with marginalized factor
        restricted_factors = [
            f for f in restricted_factors if var not in f.variables
        ]
        restricted_factors.append(marginalized)

    # Step 4: Multiply remaining factors and normalize
    result = multiply_factors(restricted_factors)
    result.normalize()

    return result
```

#### Gibbs Sampling for Approximate Inference

```python
def gibbs_sampling(
    graphical_model: BayesianNetwork,
    query_variable: str,
    evidence: Dict[str, Any],
    n_samples: int = 10000,
    burn_in: int = 1000
) -> Distribution:
    """
    Approximate inference using Gibbs sampling

    Useful when exact inference is intractable
    """
    # Initialize random state consistent with evidence
    state = initialize_state(graphical_model, evidence)

    samples = []

    for i in range(n_samples + burn_in):
        # Sample each non-evidence variable in turn
        for var in graphical_model.variables:
            if var in evidence:
                continue

            # Compute conditional distribution P(var | all other vars)
            conditional = compute_conditional(
                graphical_model,
                var,
                state
            )

            # Sample new value
            state[var] = conditional.sample()

        # Store sample after burn-in
        if i >= burn_in:
            samples.append(state[query_variable])

    # Estimate distribution from samples
    return empirical_distribution(samples)
```

### 5.3 Confidence Interval Estimation

**Wilson Score Interval** (for bounded probabilities):
```
Center = (p + z²/(2n)) / (1 + z²/n)
Margin = z × sqrt((p(1-p)/n + z²/(4n²))) / (1 + z²/n)

where:
  p = point estimate
  n = effective sample size
  z = 1.96 for 95% confidence
```

**Bootstrap Confidence Intervals** (for complex estimators):
```python
def bootstrap_ci(
    data: np.ndarray,
    estimator: Callable,
    n_bootstrap: int = 1000,
    alpha: float = 0.05
) -> Tuple[float, float]:
    """
    Bootstrap confidence interval for arbitrary estimator

    Args:
        data: Original dataset
        estimator: Function that computes statistic
        n_bootstrap: Number of bootstrap samples
        alpha: Significance level (0.05 for 95% CI)

    Returns:
        (lower_bound, upper_bound)
    """
    bootstrap_estimates = []

    for _ in range(n_bootstrap):
        # Resample with replacement
        sample = np.random.choice(data, size=len(data), replace=True)

        # Compute estimate
        estimate = estimator(sample)
        bootstrap_estimates.append(estimate)

    # Percentile method
    lower = np.percentile(bootstrap_estimates, 100 * alpha / 2)
    upper = np.percentile(bootstrap_estimates, 100 * (1 - alpha / 2))

    return (lower, upper)
```

---

## 6. Implementation Pseudocode

### 6.1 Complete Pipeline

```python
class ProbabilisticAttackInferenceEngine:
    """
    Complete pipeline for probabilistic attack chain inference
    """

    def __init__(self, neo4j_connection):
        self.db = neo4j_connection
        self.scorer = AttackChainScorer(self.db)
        self.inference = SectorInferenceModel()
        self.pattern_matcher = AttackPatternMatcher(self.db)

    def analyze_customer(
        self,
        customer_id: str,
        customer_data: Dict,
        scan_results: Dict = None,
        threat_intel: Dict = None
    ) -> CustomerDigitalTwin:
        """
        Complete customer security analysis

        Returns:
            Digital twin with risk assessment and recommendations
        """
        # Step 1: Create digital twin
        twin = CustomerDigitalTwin(customer_id, self.db)
        twin.build_twin(customer_data, scan_results, threat_intel)

        # Step 2: Compute attack chain probabilities
        # (already done in build_twin)

        # Step 3: Generate risk assessment
        risk_assessment = twin.get_risk_assessment()

        # Step 4: Persist digital twin to database
        cypher_export = twin.export_twin(format='cypher')
        self.db.execute_batch(cypher_export)

        # Step 5: Return complete twin
        return twin

    def query_attack_likelihood(
        self,
        customer_id: str,
        target_tactic: str = None,
        target_technique: str = None
    ) -> Dict:
        """
        Query specific attack likelihood for customer

        Args:
            customer_id: Customer identifier
            target_tactic: Optional tactic to query
            target_technique: Optional technique to query

        Returns:
            Probability distribution with confidence intervals
        """
        # Load digital twin
        query = """
        MATCH (dt:DigitalTwin {customer_id: $customer_id})
        RETURN dt
        """
        twin_node = self.db.query_single(query, customer_id=customer_id)

        if not twin_node:
            raise ValueError(f"No digital twin found for customer {customer_id}")

        # Query attack paths
        if target_tactic:
            path_query = """
            MATCH (dt:DigitalTwin {customer_id: $customer_id})
                  -[r:SUSCEPTIBLE_TO_TACTIC]->(tactic:Tactic {name: $tactic})
            RETURN r.max_probability as probability,
                   r.mean_probability as mean_prob,
                   r.path_count as paths
            """
            result = self.db.query_single(
                path_query,
                customer_id=customer_id,
                tactic=target_tactic
            )

            return {
                'tactic': target_tactic,
                'max_probability': result['probability'],
                'mean_probability': result['mean_prob'],
                'path_count': result['paths'],
                'confidence': twin_node['dt']['confidence_score']
            }

        elif target_technique:
            # Query via attack chains
            chains_query = """
            MATCH (dt:DigitalTwin {customer_id: $customer_id})
                  -[:HAS_CONFIRMED_CVE|HAS_INFERRED_CVE]->(cve:CVE)
                  -[:EXPLOITS]->(cwe:CWE)
                  -[:ENABLES]->(capec:CAPEC)
                  -[:MAPS_TO]->(tech:Technique {id: $technique})
            RETURN cve.id as cve,
                   tech.id as technique
            """

            paths = self.db.query(
                chains_query,
                customer_id=customer_id,
                technique=target_technique
            )

            # Score each path
            probabilities = []
            for path in paths:
                score = self.scorer.score_chain(path['cve'])
                for chain in score['chains']:
                    if chain['technique'] == target_technique:
                        probabilities.append(chain['probability']['mean'])

            if probabilities:
                return {
                    'technique': target_technique,
                    'max_probability': max(probabilities),
                    'mean_probability': sum(probabilities) / len(probabilities),
                    'path_count': len(probabilities),
                    'confidence': twin_node['dt']['confidence_score']
                }
            else:
                return {
                    'technique': target_technique,
                    'max_probability': 0.0,
                    'mean_probability': 0.0,
                    'path_count': 0,
                    'confidence': twin_node['dt']['confidence_score']
                }

        else:
            # Return overall risk summary
            return {
                'overall_risk': twin_node['dt']['overall_risk'],
                'risk_score': twin_node['dt']['risk_score'],
                'confidence': twin_node['dt']['confidence_score']
            }

    def compare_customers(
        self,
        customer_ids: List[str],
        metric: str = 'risk_score'
    ) -> pd.DataFrame:
        """
        Compare multiple customers on specified metric

        Args:
            customer_ids: List of customer identifiers
            metric: 'risk_score', 'tactic_coverage', 'vulnerability_count'

        Returns:
            DataFrame with comparative analysis
        """
        results = []

        for customer_id in customer_ids:
            twin_query = """
            MATCH (dt:DigitalTwin {customer_id: $customer_id})
            RETURN dt
            """
            twin = self.db.query_single(twin_query, customer_id=customer_id)

            if not twin:
                continue

            if metric == 'risk_score':
                results.append({
                    'customer_id': customer_id,
                    'risk_score': twin['dt']['risk_score'],
                    'overall_risk': twin['dt']['overall_risk'],
                    'confidence': twin['dt']['confidence_score']
                })

            elif metric == 'tactic_coverage':
                tactic_query = """
                MATCH (dt:DigitalTwin {customer_id: $customer_id})
                      -[r:SUSCEPTIBLE_TO_TACTIC]->(tactic:Tactic)
                RETURN count(tactic) as tactic_count,
                       avg(r.max_probability) as avg_probability
                """
                tactic_data = self.db.query_single(tactic_query, customer_id=customer_id)

                results.append({
                    'customer_id': customer_id,
                    'tactic_count': tactic_data['tactic_count'],
                    'avg_tactic_probability': tactic_data['avg_probability']
                })

            elif metric == 'vulnerability_count':
                vuln_query = """
                MATCH (dt:DigitalTwin {customer_id: $customer_id})
                      -[confirmed:HAS_CONFIRMED_CVE]->(cve1:CVE)
                OPTIONAL MATCH (dt)-[inferred:HAS_INFERRED_CVE]->(cve2:CVE)
                RETURN count(DISTINCT cve1) as confirmed_count,
                       count(DISTINCT cve2) as inferred_count
                """
                vuln_data = self.db.query_single(vuln_query, customer_id=customer_id)

                results.append({
                    'customer_id': customer_id,
                    'confirmed_vulnerabilities': vuln_data['confirmed_count'],
                    'inferred_vulnerabilities': vuln_data['inferred_count']
                })

        return pd.DataFrame(results)
```

### 6.2 Usage Examples

```python
# Example 1: Analyze new customer with minimal data
engine = ProbabilisticAttackInferenceEngine(neo4j_conn)

customer_data = {
    'sector': 'financial',
    'size': 'large',
    'known_vendors': ['Microsoft', 'Cisco', 'VMware'],
    'known_equipment': [
        {'type': 'firewall', 'vendor': 'Cisco', 'model': 'ASA'},
        {'type': 'email_server', 'vendor': 'Microsoft', 'model': 'Exchange'}
    ],
    'confirmed_cves': []  # No scan data yet
}

twin = engine.analyze_customer(
    customer_id='CUST-12345',
    customer_data=customer_data,
    scan_results=None,  # No scan available
    threat_intel=None
)

# Get risk assessment
risk = twin.get_risk_assessment()
print(f"Overall Risk: {risk['overall_risk']} (score: {risk['risk_score']:.2f})")
print(f"Confidence: {risk['confidence']:.2f}")
print(f"Top Threats: {len(risk['top_threats'])}")

# Example 2: Update with scan results
scan_results = {
    'scan_date': datetime(2025, 11, 1),
    'vulnerabilities': [
        {'id': 'CVE-2021-44228', 'severity': 'CRITICAL', 'cvss': 10.0, 'assets': ['app-server-01']},
        {'id': 'CVE-2023-34362', 'severity': 'CRITICAL', 'cvss': 9.8, 'assets': ['file-transfer-01']}
    ],
    'detail_level': 'complete'
}

twin.build_twin(customer_data, scan_results)
updated_risk = twin.get_risk_assessment()
print(f"Updated Risk Score: {updated_risk['risk_score']:.2f}")

# Example 3: Query specific attack likelihood
initial_access_prob = engine.query_attack_likelihood(
    customer_id='CUST-12345',
    target_tactic='Initial Access'
)
print(f"Initial Access Probability: {initial_access_prob['max_probability']:.2f}")

# Example 4: Compare multiple customers
comparison = engine.compare_customers(
    customer_ids=['CUST-12345', 'CUST-67890', 'CUST-11111'],
    metric='risk_score'
)
print(comparison)
```

---

## 7. Performance Considerations

### 7.1 Computational Complexity

| Operation | Complexity | Optimization Strategy |
|-----------|------------|----------------------|
| Attack chain scoring (single CVE) | O(p × h) | Cache intermediate hops, limit max paths |
| Digital twin construction | O(n × p × h) | Parallel CVE processing, batch queries |
| Bayesian inference | O(2^k) | Variable elimination, sampling for large k |
| Pattern matching | O(m × n) | Index threat campaigns, pre-compute similarities |

Where:
- n = number of CVEs
- p = average paths per CVE
- h = average hops per path
- k = number of variables in graphical model
- m = number of historical campaigns

### 7.2 Optimization Strategies

```python
# Strategy 1: Caching
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_semantic_mapping_strength(capec_id: str, tech_id: str) -> float:
    """Cache mapping strengths to avoid repeated lookups"""
    return mapping_table.get((capec_id, tech_id), 0.50)

# Strategy 2: Batch Processing
def score_chains_batch(cve_ids: List[str], customer_context: Dict) -> Dict:
    """Process multiple CVEs in parallel"""
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(score_chain, cve_id, customer_context): cve_id
            for cve_id in cve_ids
        }

        results = {}
        for future in futures:
            cve_id = futures[future]
            results[cve_id] = future.result()

        return results

# Strategy 3: Approximate Inference
def approximate_chain_probability(hops: List[HopConfidence]) -> float:
    """
    Fast approximation using point estimates instead of Monte Carlo

    Trade-off: Speed vs. accuracy in confidence intervals
    """
    prob = 1.0
    for hop in hops:
        prob *= hop.point_estimate
    return prob
```

### 7.3 Scalability Targets

- **Customer Analysis**: < 30 seconds for digital twin construction
- **Attack Chain Scoring**: < 5 seconds per CVE
- **Risk Assessment**: < 10 seconds for complete report
- **Concurrent Users**: Support 100+ simultaneous analyses
- **Database Size**: Scale to 100,000+ CVEs, 10,000+ customers

---

## 8. Validation & Testing

### 8.1 Validation Strategy

```python
class ValidationFramework:
    """Validate probabilistic model against ground truth"""

    def validate_attack_chains(
        self,
        test_cases: List[Dict]
    ) -> Dict:
        """
        Validate attack chain probabilities against known attacks

        test_cases = [
            {
                'cve': 'CVE-2021-44228',
                'actual_techniques': ['T1190', 'T1059'],
                'actual_tactics': ['Initial Access', 'Execution'],
                'customer_sector': 'financial'
            },
            ...
        ]
        """
        results = []

        for case in test_cases:
            # Score attack chain
            scored = self.scorer.score_chain(
                case['cve'],
                customer_context={'sector': case['customer_sector']}
            )

            # Check if actual techniques are in top predictions
            predicted_techniques = [
                chain['technique']
                for chain in scored['chains'][:10]  # Top 10
            ]

            # Precision/Recall
            true_positives = len(
                set(case['actual_techniques']) & set(predicted_techniques)
            )
            precision = true_positives / len(predicted_techniques)
            recall = true_positives / len(case['actual_techniques'])

            results.append({
                'cve': case['cve'],
                'precision': precision,
                'recall': recall,
                'f1': 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            })

        return {
            'avg_precision': np.mean([r['precision'] for r in results]),
            'avg_recall': np.mean([r['recall'] for r in results]),
            'avg_f1': np.mean([r['f1'] for r in results]),
            'details': results
        }

    def calibrate_confidence_intervals(
        self,
        validation_set: List[Dict]
    ) -> Dict:
        """
        Check if confidence intervals are well-calibrated

        For 95% CI, 95% of actual outcomes should fall within intervals
        """
        coverage_count = 0

        for case in validation_set:
            scored = self.scorer.score_chain(case['cve'])

            for chain in scored['chains']:
                if chain['technique'] in case['actual_techniques']:
                    # This technique was actually used
                    # Check if probability of 1.0 falls within CI
                    ci_lower = chain['probability']['ci_lower']
                    ci_upper = chain['probability']['ci_upper']

                    if ci_lower <= 1.0 <= ci_upper:
                        coverage_count += 1

        coverage_rate = coverage_count / len(validation_set)

        return {
            'expected_coverage': 0.95,
            'actual_coverage': coverage_rate,
            'calibrated': abs(coverage_rate - 0.95) < 0.05
        }
```

### 8.2 Performance Metrics

- **Precision**: Fraction of predicted techniques that are actually used
- **Recall**: Fraction of actual techniques that are predicted
- **F1 Score**: Harmonic mean of precision and recall
- **Calibration**: Confidence intervals contain true values at expected rate
- **AUC-ROC**: Area under receiver operating characteristic curve

**Target Metrics**:
- Precision: > 0.70
- Recall: > 0.75
- F1 Score: > 0.72
- Calibration: Within 5% of nominal coverage
- AUC-ROC: > 0.85

---

## 9. Future Enhancements

### 9.1 Machine Learning Integration

```python
class LearnedMappingModel:
    """
    Learn semantic mappings from historical attack data

    Replace hand-crafted mapping tables with learned associations
    """

    def __init__(self):
        from sklearn.ensemble import GradientBoostingClassifier
        self.model = GradientBoostingClassifier()

    def train(self, historical_attacks: List[Dict]):
        """
        Train model on historical CVE → Technique mappings

        Features:
        - CWE characteristics
        - CAPEC attributes
        - CVSS vector
        - Sector information
        - Temporal features

        Label:
        - Technique ID (multi-label classification)
        """
        X, y = self._prepare_training_data(historical_attacks)
        self.model.fit(X, y)

    def predict_techniques(
        self,
        cve_id: str,
        customer_context: Dict
    ) -> Dict[str, float]:
        """
        Predict techniques with learned probabilities

        Returns:
            {technique_id: probability}
        """
        features = self._extract_features(cve_id, customer_context)
        probabilities = self.model.predict_proba(features)

        return {
            technique_id: prob
            for technique_id, prob in zip(self.model.classes_, probabilities[0])
        }
```

### 9.2 Temporal Dynamics

```python
class TemporalAttackModel:
    """
    Model time-varying attack patterns

    Account for:
    - Exploit maturity (time since disclosure)
    - Patch availability and adoption
    - Threat actor campaigns over time
    - Zero-day vs. N-day dynamics
    """

    def time_adjusted_probability(
        self,
        cve_id: str,
        current_date: datetime
    ) -> float:
        """
        Adjust attack probability based on time dynamics

        Probability curve:
        - Low initially (exploit development time)
        - Peak after public exploits available
        - Decline as patches are adopted
        - Long tail for legacy systems
        """
        cve = self.db.get_cve(cve_id)

        days_since_disclosure = (current_date - cve['published_date']).days

        # Sigmoid curve for exploit maturity
        exploit_maturity = 1 / (1 + np.exp(-0.1 * (days_since_disclosure - 30)))

        # Exponential decay for patch adoption
        patch_adoption = 0.8 * np.exp(-days_since_disclosure / 180)  # 6-month half-life

        # Combined probability
        time_factor = exploit_maturity * (1 - patch_adoption)

        return time_factor
```

### 9.3 Active Learning for Data Collection

```python
class ActiveLearningOracle:
    """
    Identify high-value data collection opportunities

    Prioritize:
    - Customers with highest uncertainty
    - CVEs with most impact on risk scores
    - Sectors with least historical data
    """

    def recommend_scan_targets(
        self,
        customer_twins: List[CustomerDigitalTwin],
        budget: int
    ) -> List[str]:
        """
        Recommend which customers to scan based on expected information gain

        Args:
            customer_twins: Existing digital twins
            budget: Number of scans available

        Returns:
            Prioritized list of customer IDs
        """
        scores = []

        for twin in customer_twins:
            # Information gain = reduction in uncertainty
            current_uncertainty = 1 - twin.metadata['confidence_score']

            # High-risk customers with high uncertainty = top priority
            priority_score = twin.get_risk_assessment()['risk_score'] * current_uncertainty

            scores.append((twin.customer_id, priority_score))

        # Sort by priority
        scores.sort(key=lambda x: x[1], reverse=True)

        return [customer_id for customer_id, _ in scores[:budget]]
```

---

## 10. Conclusion

This probabilistic inference system enables:

1. **Semantic Bridging**: Connect CVE vulnerabilities to MITRE ATT&CK tactics through CWE and CAPEC
2. **Quantified Uncertainty**: Confidence intervals at every step, not just point estimates
3. **Inference Under Uncertainty**: Create customer digital twins even with incomplete data
4. **Risk-Based Prioritization**: Focus resources on highest-probability, highest-impact threats
5. **Continuous Learning**: Bayesian updates as new evidence becomes available

**Key Innovation**: Probabilistic graphical model combining authoritative mappings (CVE→CWE, Technique→Tactic) with inferred relationships (CAPEC→Technique) and customer-specific context to generate actionable security intelligence with quantified confidence.

**Implementation Priority**:
1. Core semantic mapping tables (Section 1.3)
2. Attack chain scoring algorithm (Section 2.3)
3. Customer susceptibility inference (Section 3.2)
4. Digital twin construction (Section 4.2)
5. Validation framework (Section 8.1)

**Success Metrics**:
- F1 Score > 0.72 for technique prediction
- Calibrated confidence intervals (95% coverage)
- Digital twin construction < 30 seconds
- Customer risk assessment accuracy > 80%

---

**Document Status**: READY FOR IMPLEMENTATION
**Next Steps**: Begin implementation of core semantic mapping and attack chain scoring components
**Dependencies**: Neo4j database with CVE, CWE, CAPEC, and MITRE ATT&CK data loaded
