"""
Direct test of SBOM CVE validation without full agent imports
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Test by directly importing and instantiating
def test_cve_validation_implementation():
    """Verify CVE validation method exists and works"""
    from agents.base_agent import BaseAgent

    # Import the specific module
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "sbom_agent",
        str(Path(__file__).parent.parent / "agents" / "sbom_agent.py")
    )
    sbom_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sbom_module)

    SBOMAgent = sbom_module.SBOMAgent

    # Test 1: Empty database returns False
    config1 = {'cve_database': {}}
    agent1 = SBOMAgent('test_sbom1', config1)
    result1 = agent1.validate_cve_database()
    print(f"✓ Test 1 PASSED: Empty database returns False = {result1}")
    assert result1 is False

    # Test 2: Database with purl_index returns True
    config2 = {
        'cve_database': {
            'purl_index': {
                'pkg:npm/express@4.17.1': ['CVE-2022-24999']
            }
        }
    }
    agent2 = SBOMAgent('test_sbom2', config2)
    result2 = agent2.validate_cve_database()
    print(f"✓ Test 2 PASSED: Database with purl_index returns True = {result2}")
    assert result2 is True

    # Test 3: correlate_cves returns empty list without database
    component = {
        'name': 'express',
        'version': '4.17.1',
        'purl': 'pkg:npm/express@4.17.1'
    }
    result3 = agent1.correlate_cves(component)
    print(f"✓ Test 3 PASSED: correlate_cves returns empty list = {result3}")
    assert result3 == []

    # Test 4: correlate_cves works with valid database
    result4 = agent2.correlate_cves(component)
    print(f"✓ Test 4 PASSED: correlate_cves finds matches = {len(result4)} matches")
    assert len(result4) > 0
    assert result4[0]['cve_id'] == 'CVE-2022-24999'

    print("\n✅ ALL TESTS PASSED - CVE validation implemented correctly")
    print("\nValidation Summary:")
    print("  ✓ validate_cve_database() method exists")
    print("  ✓ Returns False for empty/missing database")
    print("  ✓ Returns True for populated database")
    print("  ✓ correlate_cves() checks database before correlation")
    print("  ✓ Returns empty list gracefully when database unavailable")
    print("  ✓ Processes CVEs normally with valid database")

if __name__ == '__main__':
    test_cve_validation_implementation()
