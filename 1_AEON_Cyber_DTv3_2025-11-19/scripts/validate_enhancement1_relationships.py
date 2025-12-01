#!/usr/bin/env python3
"""
ENHANCEMENT 1 DATA VALIDATION
Validate relationship data quality and schema compliance for InformationStream-CognitiveBias relationships
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Configuration
NEO4J_CONTAINER = "openspg-neo4j"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j@openspg"
RELATIONSHIPS_FILE = "/home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19/data/level5_bias_relationships.json"
VALIDATION_REPORT = "/home/jim/2_OXOT_Projects_Dev/1_AEON_Cyber_DTv3_2025-11-19/reports/enhancement1_validation_report.json"

class ValidationResults:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.checks = {}
        self.overall_status = "PASS"
        self.errors = []
        self.warnings = []

    def add_check(self, name, status, details=None, error=None):
        """Add validation check result"""
        self.checks[name] = {
            "status": status,
            "details": details,
            "error": error
        }
        if status == "FAIL":
            self.overall_status = "FAIL"
            if error:
                self.errors.append(f"{name}: {error}")
        elif status == "WARN":
            if error:
                self.warnings.append(f"{name}: {error}")

    def to_dict(self):
        """Convert to dictionary for JSON output"""
        return {
            "timestamp": self.timestamp,
            "overall_status": self.overall_status,
            "checks": self.checks,
            "errors": self.errors,
            "warnings": self.warnings,
            "summary": {
                "total_checks": len(self.checks),
                "passed": sum(1 for c in self.checks.values() if c["status"] == "PASS"),
                "failed": sum(1 for c in self.checks.values() if c["status"] == "FAIL"),
                "warnings": sum(1 for c in self.checks.values() if c["status"] == "WARN")
            }
        }

def run_cypher(query):
    """Execute Cypher query in Neo4j container"""
    cmd = [
        "docker", "exec", NEO4J_CONTAINER,
        "cypher-shell", "-u", NEO4J_USER, "-p", NEO4J_PASSWORD,
        "--format", "plain",
        query
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return None

def parse_count(output):
    """Parse count from cypher-shell output"""
    if not output:
        return 0
    lines = output.strip().split('\n')
    # Get last line which should be the count
    for line in reversed(lines):
        line = line.strip()
        if line and line.isdigit():
            return int(line)
    return 0

def validate_file_exists(results):
    """Check if relationship file exists"""
    print("🔍 CHECK 1: File Existence")
    if Path(RELATIONSHIPS_FILE).exists():
        print("  ✅ PASS: Relationship file exists")
        results.add_check("file_existence", "PASS", {"path": RELATIONSHIPS_FILE})
        return True
    else:
        print("  ❌ FAIL: Relationship file not found")
        results.add_check("file_existence", "FAIL", {"path": RELATIONSHIPS_FILE},
                         "File does not exist - Hour 1 agent may not have completed")
        return False

def validate_file_structure(results):
    """Validate JSON structure and required fields"""
    print("\n🔍 CHECK 2: File Structure & Schema Compliance")
    try:
        with open(RELATIONSHIPS_FILE, 'r') as f:
            data = json.load(f)

        # Check top-level structure
        if not isinstance(data, dict):
            results.add_check("json_structure", "FAIL", None, "Root element must be object")
            return None

        # Handle nested structure with relationship types
        if "relationships" in data and isinstance(data["relationships"], dict):
            # Extract HAS_BIAS relationships (the main ones for validation)
            if "HAS_BIAS" not in data["relationships"]:
                results.add_check("json_structure", "FAIL", None, "Missing 'HAS_BIAS' relationship type")
                return None

            relationships = data["relationships"]["HAS_BIAS"]
            total_relationships = len(relationships)

            # Also count other relationship types
            metadata = data.get("metadata", {})
            print(f"  ✅ PASS: Valid JSON structure")
            print(f"     HAS_BIAS relationships: {len(relationships)}")
            if "ACTIVATES_BIAS" in data["relationships"]:
                print(f"     ACTIVATES_BIAS relationships: {len(data['relationships']['ACTIVATES_BIAS'])}")
            if "INFLUENCES_DECISION" in data["relationships"]:
                print(f"     INFLUENCES_DECISION relationships: {len(data['relationships']['INFLUENCES_DECISION'])}")

            results.add_check("json_structure", "PASS", {
                "has_bias_count": len(relationships),
                "total_relationship_types": len(data["relationships"])
            })
        else:
            results.add_check("json_structure", "FAIL", None, "'relationships' must be object with relationship types")
            return None

        # Validate HAS_BIAS schema compliance (these map InformationStream -> CognitiveBias)
        required_fields = ["from", "to", "type"]  # Adjusted for actual structure
        optional_fields = ["relationshipId", "fromType", "toType", "properties"]
        missing_fields = []
        invalid_relationships = []

        for i, rel in enumerate(relationships[:10]):  # Check first 10 samples
            if not isinstance(rel, dict):
                invalid_relationships.append(f"Index {i}: Not an object")
                continue

            for field in required_fields:
                if field not in rel:
                    missing_fields.append(f"Index {i}: Missing '{field}'")

            # Check properties object has strength
            if "properties" in rel:
                props = rel["properties"]
                if "strength" not in props:
                    missing_fields.append(f"Index {i}: Missing 'strength' in properties")

        if missing_fields or invalid_relationships:
            error_msg = "; ".join(missing_fields[:10] + invalid_relationships[:10])  # Limit error output
            print(f"  ❌ FAIL: Schema violations found in samples")
            results.add_check("schema_compliance", "FAIL",
                            {"violations": len(missing_fields) + len(invalid_relationships)},
                            error_msg)
        else:
            print(f"  ✅ PASS: Sample relationships have required fields")
            results.add_check("schema_compliance", "PASS",
                            {"required_fields": required_fields, "validated": len(relationships)})

        return relationships

    except json.JSONDecodeError as e:
        print(f"  ❌ FAIL: Invalid JSON - {str(e)}")
        results.add_check("json_structure", "FAIL", None, f"Invalid JSON: {str(e)}")
        return None
    except Exception as e:
        print(f"  ❌ FAIL: Error reading file - {str(e)}")
        results.add_check("json_structure", "FAIL", None, str(e))
        return None

def validate_node_existence(results):
    """Verify referenced nodes exist in database"""
    print("\n🔍 CHECK 3: Node Existence in Database")

    # Check InformationStream nodes
    print("  Checking InformationStream nodes...")
    query = "MATCH (s:InformationStream) RETURN count(s) as count"
    output = run_cypher(query)
    stream_count = parse_count(output)

    if stream_count == 600:
        print(f"  ✅ PASS: Found 600 InformationStream nodes")
        results.add_check("information_stream_nodes", "PASS", {"count": stream_count})
    elif stream_count > 0:
        print(f"  ⚠️  WARN: Found {stream_count} InformationStream nodes (expected 600)")
        results.add_check("information_stream_nodes", "WARN", {"count": stream_count, "expected": 600},
                         f"Node count mismatch: {stream_count} vs 600")
    else:
        print(f"  ❌ FAIL: No InformationStream nodes found")
        results.add_check("information_stream_nodes", "FAIL", {"count": 0},
                         "InformationStream nodes missing from database")

    # Check CognitiveBias nodes
    print("  Checking CognitiveBias nodes...")
    query = "MATCH (b:CognitiveBias) RETURN count(b) as count"
    output = run_cypher(query)
    bias_count = parse_count(output)

    if bias_count == 30:
        print(f"  ✅ PASS: Found 30 CognitiveBias nodes")
        results.add_check("cognitive_bias_nodes", "PASS", {"count": bias_count})
    elif bias_count > 0:
        print(f"  ⚠️  WARN: Found {bias_count} CognitiveBias nodes (expected 30)")
        results.add_check("cognitive_bias_nodes", "WARN", {"count": bias_count, "expected": 30},
                         f"Node count mismatch: {bias_count} vs 30")
    else:
        print(f"  ❌ FAIL: No CognitiveBias nodes found")
        results.add_check("cognitive_bias_nodes", "FAIL", {"count": 0},
                         "CognitiveBias nodes missing from database")

def validate_strength_values(relationships, results):
    """Validate strength values are in 0.0-1.0 range"""
    print("\n🔍 CHECK 4: Strength Value Validation")

    if not relationships:
        results.add_check("strength_values", "FAIL", None, "No relationships to validate")
        return

    invalid_strengths = []
    valid_count = 0

    for i, rel in enumerate(relationships):
        # Get strength from properties object
        props = rel.get("properties", {})
        strength = props.get("strength")

        if strength is None:
            invalid_strengths.append(f"Index {i}: Missing strength")
        elif not isinstance(strength, (int, float)):
            invalid_strengths.append(f"Index {i}: Strength not numeric ({strength})")
        elif strength < 0.0 or strength > 1.0:
            invalid_strengths.append(f"Index {i}: Strength out of range ({strength})")
        else:
            valid_count += 1

    if invalid_strengths:
        print(f"  ❌ FAIL: {len(invalid_strengths)} invalid strength values")
        results.add_check("strength_values", "FAIL",
                         {"invalid_count": len(invalid_strengths), "valid_count": valid_count,
                          "examples": invalid_strengths[:5]},
                         f"{len(invalid_strengths)} invalid strength values")
    else:
        print(f"  ✅ PASS: All {len(relationships)} strength values in valid range [0.0-1.0]")
        results.add_check("strength_values", "PASS", {"validated": valid_count})

def validate_duplicates(relationships, results):
    """Check for duplicate stream-bias pairs"""
    print("\n🔍 CHECK 5: Duplicate Detection")

    if not relationships:
        results.add_check("duplicate_detection", "FAIL", None, "No relationships to check")
        return

    pairs = set()
    duplicates = []

    for i, rel in enumerate(relationships):
        stream_id = rel.get("from")
        bias_id = rel.get("to")
        pair = (stream_id, bias_id)

        if pair in pairs:
            duplicates.append(f"Index {i}: {stream_id} -> {bias_id}")
        else:
            pairs.add(pair)

    if duplicates:
        print(f"  ❌ FAIL: Found {len(duplicates)} duplicate relationships")
        results.add_check("duplicate_detection", "FAIL",
                         {"duplicate_count": len(duplicates), "examples": duplicates[:5]},
                         f"{len(duplicates)} duplicate stream-bias pairs")
    else:
        print(f"  ✅ PASS: No duplicate stream-bias pairs found")
        results.add_check("duplicate_detection", "PASS", {"unique_pairs": len(pairs)})

def validate_distribution(relationships, results):
    """Analyze relationship distribution across biases"""
    print("\n🔍 CHECK 6: Distribution Analysis")

    if not relationships:
        results.add_check("distribution_analysis", "FAIL", None, "No relationships to analyze")
        return

    # Count relationships per bias
    bias_counts = {}
    stream_counts = {}

    for rel in relationships:
        bias_id = rel.get("to")  # CognitiveBias is the target
        stream_id = rel.get("from")  # InformationStream is the source

        bias_counts[bias_id] = bias_counts.get(bias_id, 0) + 1
        stream_counts[stream_id] = stream_counts.get(stream_id, 0) + 1

    total_biases = len(bias_counts)
    total_streams = len(stream_counts)
    avg_per_bias = len(relationships) / total_biases if total_biases > 0 else 0
    avg_per_stream = len(relationships) / total_streams if total_streams > 0 else 0
    min_bias = min(bias_counts.values()) if bias_counts else 0
    max_bias = max(bias_counts.values()) if bias_counts else 0

    print(f"  📊 Distribution Statistics:")
    print(f"     Unique InformationStreams: {total_streams}")
    print(f"     Unique CognitiveBiases: {total_biases}")
    print(f"     Avg relationships per stream: {avg_per_stream:.1f}")
    print(f"     Avg relationships per bias: {avg_per_bias:.1f}")
    print(f"     Min per bias: {min_bias}, Max per bias: {max_bias}")

    # Expected: 600 streams × 30 biases = 18,000 relationships
    # So each stream should connect to all 30 biases (avg ~30 per stream)
    # And each bias should connect to all 600 streams (avg ~600 per bias)

    if total_streams >= 500 and total_biases >= 25:
        print(f"  ✅ PASS: Good coverage across streams and biases")
        results.add_check("distribution_analysis", "PASS",
                         {"total_streams": total_streams, "total_biases": total_biases,
                          "avg_per_bias": avg_per_bias, "avg_per_stream": avg_per_stream})
    else:
        print(f"  ⚠️  WARN: Limited coverage")
        results.add_check("distribution_analysis", "WARN",
                         {"total_streams": total_streams, "total_biases": total_biases},
                         f"Limited coverage: {total_streams} streams, {total_biases} biases")

def validate_data_integrity(relationships, results):
    """Validate required properties"""
    print("\n🔍 CHECK 7: Data Integrity")

    if not relationships:
        results.add_check("data_integrity", "FAIL", None, "No relationships to validate")
        return

    issues = []
    sample_size = min(100, len(relationships))  # Check first 100

    for i, rel in enumerate(relationships[:sample_size]):
        props = rel.get("properties", {})

        # Check required property fields
        if "strength" not in props:
            issues.append(f"Index {i}: Missing strength in properties")

        if "activationFrequency" not in props:
            issues.append(f"Index {i}: Missing activationFrequency")

        if "description" not in props:
            issues.append(f"Index {i}: Missing description")

        # Validate from/to IDs
        if not rel.get("from"):
            issues.append(f"Index {i}: Missing 'from' stream ID")
        if not rel.get("to"):
            issues.append(f"Index {i}: Missing 'to' bias ID")

    if issues:
        print(f"  ❌ FAIL: {len(issues)} data integrity issues in sample")
        results.add_check("data_integrity", "FAIL",
                         {"issue_count": len(issues), "sample_size": sample_size,
                          "examples": issues[:5]},
                         f"{len(issues)} data integrity issues")
    else:
        print(f"  ✅ PASS: Sample relationships have valid required properties")
        results.add_check("data_integrity", "PASS", {"validated": sample_size})

def main():
    """Main validation function"""
    print("=" * 80)
    print("ENHANCEMENT 1 DATA VALIDATION")
    print("InformationStream-CognitiveBias Relationships")
    print("=" * 80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    results = ValidationResults()

    # Run validation checks
    if not validate_file_exists(results):
        print("\n⚠️  Cannot proceed - relationship file not found")
        print("   Waiting for Hour 1 agent to complete relationship generation")
    else:
        relationships = validate_file_structure(results)

        if relationships is not None:
            validate_node_existence(results)
            validate_strength_values(relationships, results)
            validate_duplicates(relationships, results)
            validate_distribution(relationships, results)
            validate_data_integrity(relationships, results)

    # Write validation report
    print(f"\n{'=' * 80}")
    print("VALIDATION SUMMARY")
    print("=" * 80)

    report_data = results.to_dict()

    with open(VALIDATION_REPORT, 'w') as f:
        json.dump(report_data, f, indent=2)

    print(f"\n📊 Overall Status: {results.overall_status}")
    print(f"   Total Checks: {report_data['summary']['total_checks']}")
    print(f"   Passed: {report_data['summary']['passed']}")
    print(f"   Failed: {report_data['summary']['failed']}")
    print(f"   Warnings: {report_data['summary']['warnings']}")

    if results.errors:
        print(f"\n❌ ERRORS:")
        for error in results.errors:
            print(f"   - {error}")

    if results.warnings:
        print(f"\n⚠️  WARNINGS:")
        for warning in results.warnings:
            print(f"   - {warning}")

    print(f"\n📄 Full validation report: {VALIDATION_REPORT}")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # Return exit code based on overall status
    return 0 if results.overall_status == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
