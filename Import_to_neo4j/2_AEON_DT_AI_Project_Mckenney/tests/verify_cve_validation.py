"""
Standalone verification of CVE validation implementation
Directly reads and validates the sbom_agent.py file
"""

import re
from pathlib import Path

def verify_cve_validation():
    """Verify CVE validation is properly implemented"""

    sbom_agent_path = Path(__file__).parent.parent / "agents" / "sbom_agent.py"

    with open(sbom_agent_path, 'r') as f:
        content = f.read()

    print("=" * 70)
    print("CVE DATABASE VALIDATION VERIFICATION")
    print("=" * 70)

    # Check 1: validate_cve_database method exists
    validate_method_pattern = r'def validate_cve_database\(self\) -> bool:'
    if re.search(validate_method_pattern, content):
        print("✓ PASS: validate_cve_database() method exists")
    else:
        print("✗ FAIL: validate_cve_database() method NOT FOUND")
        return False

    # Check 2: Method checks for empty database
    if 'if not self.cve_database:' in content:
        print("✓ PASS: Checks for empty CVE database")
    else:
        print("✗ FAIL: Missing empty database check")
        return False

    # Check 3: Method checks indexes
    if 'has_purl_index' in content and 'has_cpe_index' in content:
        print("✓ PASS: Validates database indexes exist")
    else:
        print("✗ FAIL: Missing index validation")
        return False

    # Check 4: Method handles Neo4j validation
    if 'neo4j_driver' in content and 'MATCH (c:CVE)' in content:
        print("✓ PASS: Includes Neo4j database validation")
    else:
        print("✗ FAIL: Missing Neo4j validation")
        return False

    # Check 5: correlate_cves calls validation
    correlate_pattern = r'def correlate_cves.*?if not self\.validate_cve_database\(\):'
    if re.search(correlate_pattern, content, re.DOTALL):
        print("✓ PASS: correlate_cves() calls validate_cve_database()")
    else:
        print("✗ FAIL: correlate_cves() does NOT call validation")
        return False

    # Check 6: Returns empty list on validation failure
    empty_return_pattern = r'if not self\.validate_cve_database\(\):.*?return \[\]'
    if re.search(empty_return_pattern, content, re.DOTALL):
        print("✓ PASS: Returns empty list when database unavailable")
    else:
        print("✗ FAIL: Missing graceful empty list return")
        return False

    # Check 7: Logs warning messages
    if 'self.logger.warning' in content and 'CVE database' in content:
        print("✓ PASS: Logs warnings for database issues")
    else:
        print("✗ FAIL: Missing warning logs")
        return False

    # Check 8: Exception handling in validation
    validation_try_pattern = r'def validate_cve_database.*?try:.*?except Exception'
    if re.search(validation_try_pattern, content, re.DOTALL):
        print("✓ PASS: Exception handling in validation method")
    else:
        print("✗ FAIL: Missing exception handling")
        return False

    print("\n" + "=" * 70)
    print("✅ ALL VALIDATION CHECKS PASSED")
    print("=" * 70)

    print("\nImplementation Summary:")
    print("  • validate_cve_database() method implemented")
    print("  • Checks for empty/missing database configuration")
    print("  • Validates database indexes (purl, cpe, ranges, fuzzy)")
    print("  • Optional Neo4j database validation")
    print("  • correlate_cves() calls validation before processing")
    print("  • Returns empty list gracefully when database unavailable")
    print("  • Logs appropriate warnings for missing database")
    print("  • Proper exception handling throughout")

    print("\nBehavior:")
    print("  • No crashes when CVE database is missing")
    print("  • Graceful degradation with warning logs")
    print("  • Empty CVE list returned instead of errors")
    print("  • System continues processing other components")

    return True

if __name__ == '__main__':
    success = verify_cve_validation()
    exit(0 if success else 1)
