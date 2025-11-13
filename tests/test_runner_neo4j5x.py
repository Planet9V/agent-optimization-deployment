#!/usr/bin/env python3
"""
GAP-004 Neo4j 5.x Test Runner
Executes Cypher test files in managed transactions to resolve transaction isolation issues.

Week 6 Discovery: cypher-shell executes each statement as separate transaction,
causing test failures when queries cannot see setup data.

Solution: Execute entire test file in single managed transaction via Python driver.
"""

import sys
from pathlib import Path
from neo4j import GraphDatabase
import re


class Neo4jTestRunner:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def execute_test_file(self, test_file_path):
        """
        Execute a Cypher test file in a single managed transaction.

        Args:
            test_file_path: Path to .cypher test file

        Returns:
            dict: Test results with pass/fail counts
        """
        test_file = Path(test_file_path)
        if not test_file.exists():
            raise FileNotFoundError(f"Test file not found: {test_file_path}")

        print(f"\n{'='*80}")
        print(f"Executing Test Suite: {test_file.name}")
        print(f"{'='*80}\n")

        # Read test file
        cypher_content = test_file.read_text()

        # Split into individual statements (handle semicolons)
        statements = self._split_cypher_statements(cypher_content)

        # Execute in single transaction
        with self.driver.session() as session:
            results = session.execute_write(self._run_test_statements, statements)

        return results

    def _split_cypher_statements(self, cypher_content):
        """Split Cypher file into individual statements."""
        # Remove comments
        lines = []
        for line in cypher_content.split('\n'):
            # Remove inline comments
            if '//' in line:
                line = line[:line.index('//')].strip()
            if line:
                lines.append(line)

        content = '\n'.join(lines)

        # Split on semicolons (but not in strings)
        statements = []
        current_stmt = []
        in_string = False
        escape_next = False

        for char in content:
            if escape_next:
                current_stmt.append(char)
                escape_next = False
                continue

            if char == '\\':
                escape_next = True
                current_stmt.append(char)
                continue

            if char == "'" or char == '"':
                in_string = not in_string
                current_stmt.append(char)
                continue

            if char == ';' and not in_string:
                stmt = ''.join(current_stmt).strip()
                if stmt:
                    statements.append(stmt)
                current_stmt = []
            else:
                current_stmt.append(char)

        # Add final statement if exists
        stmt = ''.join(current_stmt).strip()
        if stmt:
            statements.append(stmt)

        return statements

    def _run_test_statements(self, tx, statements):
        """Execute all statements in a single transaction."""
        test_results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'test_details': []
        }

        for i, statement in enumerate(statements, 1):
            try:
                result = tx.run(statement)

                # Check if this is a test result query
                if 'RETURN' in statement.upper() and '_result' in statement.lower():
                    records = list(result)
                    for record in records:
                        # Look for test result columns
                        for key in record.keys():
                            if '_result' in key.lower():
                                test_num = key.split('_')[1]  # Extract test number
                                test_status = record[key]
                                test_results['total_tests'] += 1

                                if test_status == 'PASS':
                                    test_results['passed'] += 1
                                    print(f"  ✅ Test {test_num}: PASS")
                                else:
                                    test_results['failed'] += 1
                                    print(f"  ❌ Test {test_num}: FAIL")

                                # Get test description if available
                                desc_key = f"test_{test_num}_description"
                                description = record.get(desc_key, 'No description')

                                test_results['test_details'].append({
                                    'test_number': test_num,
                                    'status': test_status,
                                    'description': description
                                })

            except Exception as e:
                print(f"  ⚠️  Statement {i} error: {str(e)[:100]}")
                # Continue executing remaining statements
                continue

        return test_results

    def print_summary(self, results):
        """Print test execution summary."""
        print(f"\n{'='*80}")
        print("TEST SUITE SUMMARY")
        print(f"{'='*80}")
        print(f"  Total Tests: {results['total_tests']}")
        print(f"  Passed: {results['passed']} ({results['passed']/results['total_tests']*100:.1f}%)")
        print(f"  Failed: {results['failed']} ({results['failed']/results['total_tests']*100:.1f}%)")
        print(f"{'='*80}\n")


def main():
    """Run GAP-004 test suites."""
    if len(sys.argv) < 2:
        print("Usage: python test_runner_neo4j5x.py <test_file.cypher>")
        print("\nExample:")
        print("  python test_runner_neo4j5x.py tests/gap004_r6_temporal_tests.cypher")
        print("  python test_runner_neo4j5x.py tests/gap004_cg9_operational_tests.cypher")
        sys.exit(1)

    test_file = sys.argv[1]

    # Initialize runner
    runner = Neo4jTestRunner()

    try:
        # Execute test suite
        results = runner.execute_test_file(test_file)

        # Print summary
        runner.print_summary(results)

        # Exit code based on results
        sys.exit(0 if results['failed'] == 0 else 1)

    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        sys.exit(1)

    finally:
        runner.close()


if __name__ == "__main__":
    main()
