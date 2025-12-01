# Part 3 of 4: Integration Patterns

**Series**: AgentZero Security OSINT
**Navigation**: [← Part 2](./02_OSINT_Capabilities.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 4 →](./04_Advanced_Applications.md)

---

- Iterative refinement
- Multi-perspective analysis

**AgentZero Implementation:**
```python
# Advanced security reasoning

def exploit_development_with_reasoning(vulnerability_details):
    """
    Multi-stage exploit development with self-criticism
    """
    # Stage 1: Problem decomposition
    sub_problems = decompose_vulnerability(vulnerability_details)
    """
    Example decomposition:
    - Understand vulnerability mechanism
    - Identify exploitation prerequisites
    - Determine payload requirements
    - Bypass security controls
    - Achieve desired outcome
    """

    # Stage 2: Solution generation
    solutions = {}
    for sub_problem in sub_problems:
        # Generate multiple approaches
        approaches = generate_approaches(sub_problem)

        # Self-criticism
        evaluated_approaches = []
        for approach in approaches:
            critique = self_critique_approach(approach, sub_problem)
            evaluated_approaches.append({
                'approach': approach,
                'strengths': critique['strengths'],
                'weaknesses': critique['weaknesses'],
                'viability': critique['score']
            })

        # Select best approach
        solutions[sub_problem] = max(evaluated_approaches,
                                    key=lambda x: x['viability'])

    # Stage 3: Integrate solutions into exploit
    initial_exploit = integrate_solutions(solutions)

    # Stage 4: Self-criticism of complete exploit
    exploit_critique = {
        'reliability': assess_reliability(initial_exploit),
        'stealth': assess_stealth(initial_exploit),
        'compatibility': assess_compatibility(initial_exploit),
        'failure_modes': identify_failure_modes(initial_exploit)
    }

    # Stage 5: Refinement based on criticism
    refined_exploit = refine_exploit(initial_exploit, exploit_critique)

    # Stage 6: Testing and validation
    test_results = test_in_sandbox(refined_exploit, vulnerability_details)

    # Stage 7: Final optimization
    if test_results['success']:
        optimized_exploit = optimize_exploit(refined_exploit, test_results)
    else:
        # Iterate with learnings
        return exploit_development_with_reasoning(
            {**vulnerability_details, 'previous_attempt': refined_exploit}
        )

    return {
        'exploit': optimized_exploit,
        'decomposition': sub_problems,
        'reasoning': solutions,
        'validation': test_results
    }
```

---

### 4.3 Role-Based Security Prompting

**Technique #13: Multi-Persona Security Analysis**

**Personas for Security Testing:**
- Penetration Tester
- Red Team Operator
- Malware Analyst
- Forensic Investigator
- Security Architect
- Threat Intelligence Analyst

**AgentZero Multi-Persona Instrument:**
```python
# Multi-persona security analysis

def multi_persona_assessment(target_system):
    """
    Analyze security from multiple expert perspectives
    """
    personas = {
        'penetration_tester': {
            'focus': 'Vulnerability identification and exploitation',
            'prompt': """You are an expert penetration tester with OSCP and OSCE certifications.
                        Analyze the target system for security vulnerabilities.
                        Consider: authentication, authorization, input validation,
                        crypto, session management, error handling."""
        },

        'red_team': {
            'focus': 'Attack chain and persistence',
            'prompt': """You are a red team operator simulating APT tactics.
                        Design a multi-stage attack campaign including:
                        initial access, privilege escalation, lateral movement,
                        persistence, and data exfiltration."""
        },

        'threat_intel': {
            'focus': 'Threat landscape and actor TTPs',
            'prompt': """You are a threat intelligence analyst.
                        Identify potential threat actors targeting this system,
                        their typical TTPs, and indicators of compromise."""
        },

        'malware_analyst': {
            'focus': 'Malicious code detection',
            'prompt': """You are a malware reverse engineer.
                        Analyze the system for indicators of compromise,
                        backdoors, and malicious code."""
        },

        'forensics': {
            'focus': 'Evidence and artifacts',
            'prompt': """You are a digital forensics investigator.
                        Identify what evidence would be available if this
                        system was compromised, and detection gaps."""
        }
    }

    assessments = {}

    for persona_name, persona_config in personas.items():
        # Set agent persona
        agent.set_persona(persona_config['prompt'])

        # Conduct assessment
        assessment = agent.analyze(target_system)

        assessments[persona_name] = {
            'focus_area': persona_config['focus'],
            'findings': assessment['findings'],
            'recommendations': assessment['recommendations'],
            'risk_score': assessment['risk_score']
        }

    # Cross-persona synthesis
    synthesis = {
        'combined_findings': merge_findings(assessments),
        'prioritized_risks': prioritize_all_risks(assessments),
        'comprehensive_recommendations': synthesize_recommendations(assessments),
        'coverage_gaps': identify_coverage_gaps(assessments)
    }

    return {
        'persona_assessments': assessments,
        'synthesis': synthesis
    }
```

---

## Part 5: Advanced Tool Integration and Automation

### 5.1 Custom Instrument Development

**Technique #14: Building Security-Specific Instruments**

**AgentZero Instrument Architecture:**

```python
# File: python/instruments/security_assessment.py

from python.helpers.tool import Tool, Response
from python.helpers import files
import subprocess
import json

class SecurityAssessment(Tool):
    """
    Comprehensive security assessment instrument
    Integrates multiple tools and frameworks
    """

    def execute(self, target, assessment_type="full", **kwargs):
        """
        Execute security assessment

        Args:
            target: IP, domain, or application URL
            assessment_type: quick, standard, full, custom
            **kwargs: Additional parameters
        """

        if assessment_type == "quick":
            return self._quick_scan(target)
        elif assessment_type == "standard":
            return self._standard_assessment(target)
        elif assessment_type == "full":
            return self._full_assessment(target)
        else:
            return self._custom_assessment(target, kwargs)

    def _quick_scan(self, target):
        """Fast reconnaissance scan"""
        results = {}

        # Nmap quick scan
        results['nmap'] = self._run_nmap(target, "-sn -T4")

        # DNS enumeration
        results['dns'] = self._enumerate_dns(target)

        # SSL/TLS check
        if self._is_web_service(target):
            results['ssl'] = self._check_ssl(target)

        return Response(
            message=f"Quick scan completed for {target}",
            break_loop=False,
            data=results
        )

    def _standard_assessment(self, target):
        """Standard security assessment"""
        results = {}

        # Port scanning
        results['ports'] = self._run_nmap(target, "-sS -sV -O -p-")

        # Service enumeration
        results['services'] = self._enumerate_services(results['ports'])

        # Vulnerability scanning
        results['vulnerabilities'] = self._scan_vulnerabilities(target)

        # Web application testing (if applicable)
        if self._has_web_services(results['services']):
            results['web'] = self._web_assessment(target)

        return Response(
            message=f"Standard assessment completed for {target}",
            break_loop=False,
            data=results
        )

    def _full_assessment(self, target):
        """Comprehensive security assessment"""
        # Execute standard assessment
        standard = self._standard_assessment(target)
        results = standard.data

        # Additional deep analysis
        results['exploitation'] = self._attempt_exploitation(
            results['vulnerabilities']
        )

        results['post_exploit'] = self._post_exploitation_analysis(
            results['exploitation']
        )

        results['report'] = self._generate_comprehensive_report(results)

        return Response(
            message=f"Full assessment completed for {target}",
            break_loop=False,
            data=results
        )

    # Helper methods
    def _run_nmap(self, target, options):
        """Execute nmap scan"""
        cmd = f"nmap {options} {target} -oX -"
        result = subprocess.run(
            cmd.split(),
            capture_output=True,
            text=True
        )
        return self._parse_nmap_xml(result.stdout)

    def _scan_vulnerabilities(self, target):
        """Run vulnerability scanners"""
        vulns = []

        # Nmap NSE scripts
        nse_result = self._run_nmap(target, "--script vuln")
        vulns.extend(self._parse_nse_vulns(nse_result))

        # Nuclei templates
        nuclei_cmd = f"nuclei -u {target} -j"
        nuclei_result = subprocess.run(
            nuclei_cmd.split(),
            capture_output=True,
            text=True
        )
        vulns.extend(json.loads(nuclei_result.stdout))

        return vulns

    def _web_assessment(self, target):
        """Web application security testing"""
        results = {}

        # Directory enumeration
        results['directories'] = self._run_gobuster(target)

        # SQL injection testing
        results['sqli'] = self._run_sqlmap(target)

        # XSS testing
        results['xss'] = self._test_xss(target)

        # OWASP ZAP scan
        results['zap'] = self._run_zap_scan(target)

        return results

    def _attempt_exploitation(self, vulnerabilities):
        """Attempt safe exploitation of discovered vulnerabilities"""
        exploits = []

        for vuln in vulnerabilities:
            # Check if exploit available
            exploit = self._find_exploit(vuln)

            if exploit:
                # Test in safe mode
                result = self._test_exploit_safe(exploit, vuln)
                exploits.append({
                    'vulnerability': vuln,
                    'exploit': exploit,
                    'result': result
                })

        return exploits
```

---

### 5.2 Multi-Agent Security Workflow

**Technique #15: Coordinated Multi-Agent Security Operations**

**Architecture:**
```
┌─────────────────────────────────────────────────────┐
│              Coordinator Agent                      │
│         (Strategy & Orchestration)                  │
└────────────┬────────────────────────────────────────┘
             │
             ├──────────┬──────────┬──────────┬────────────┐
             │          │          │          │            │
        ┌────▼───┐ ┌───▼────┐ ┌──▼─────┐ ┌──▼────┐ ┌────▼─────┐
        │Recon   │ │Vuln    │ │Exploit │ │Post   │ │Report    │
        │Agent   │ │Scanner │ │Agent   │ │Exploit│ │Generator │
        └────────┘ └────────┘ └────────┘ └───────┘ └──────────┘
             │          │          │          │            │
             └──────────┴──────────┴──────────┴────────────┘
                              │
                    ┌─────────▼──────────┐
                    │  Shared Knowledge  │
                    │      Base (RAG)    │
                    └────────────────────┘
```

**AgentZero Implementation:**
```python
# Multi-agent security workflow

from python.helpers.agent import Agent

def multi_agent_security_assessment(target):
    """
    Coordinated multi-agent security testing
    """
    # Initialize specialized agents
    coordinator = Agent(
        name="Coordinator",
        role="Strategic planning and orchestration",
        tools=['knowledge_base', 'agent_communication']
    )

    recon_agent = Agent(
        name="ReconAgent",
        role="Reconnaissance and information gathering",
        tools=['nmap', 'amass', 'subfinder', 'gobuster']
    )

    vuln_scanner = Agent(
        name="VulnScanner",
        role="Vulnerability identification",
        tools=['nuclei', 'nikto', 'nessus', 'openvas']
    )

    exploit_agent = Agent(
        name="ExploitAgent",
        role="Exploitation and validation",
        tools=['metasploit', 'sqlmap', 'custom_exploits']
    )

    post_exploit_agent = Agent(
        name="PostExploitAgent",
        role="Post-exploitation and persistence",
        tools=['privilege_escalation', 'lateral_movement', 'data_discovery']
    )

    report_agent = Agent(
        name="ReportAgent",
        role="Evidence collection and reporting",
        tools=['report_generator', 'screenshot', 'evidence_collector']
    )


---

**Navigation**: [← Part 2](./02_OSINT_Capabilities.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 4 →](./04_Advanced_Applications.md)
**Part 3 of 4** | Lines 839-1257 of original document
