#!/bin/bash
################################################################################
# Psychohistory Equations - Test Runner
################################################################################
# This script runs all 5 psychohistory equations and validates results
#
# Usage:
#   ./run_all_tests.sh [neo4j_password]
#
# Requirements:
#   - Neo4j running on localhost:7687
#   - cypher-shell in PATH
#   - NER11_Gold dataset loaded
################################################################################

set -e  # Exit on error

# Configuration
NEO4J_HOST="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASS="${1:-password}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check cypher-shell
    if ! command -v cypher-shell &> /dev/null; then
        log_error "cypher-shell not found in PATH"
        exit 1
    fi

    # Check Neo4j connection
    if ! cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASS" "RETURN 1" &> /dev/null; then
        log_error "Cannot connect to Neo4j at $NEO4J_HOST"
        exit 1
    fi

    # Check NER11_Gold data loaded
    local node_count=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASS" --format plain "MATCH (n) RETURN count(n) AS count" | grep -o '[0-9]*' | head -1)
    if [ "$node_count" -lt 100 ]; then
        log_warning "Only $node_count nodes found. NER11_Gold dataset may not be loaded."
    else
        log_success "Found $node_count nodes in database"
    fi

    log_success "All prerequisites met"
}

# Run equation and capture results
run_equation() {
    local eq_num=$1
    local eq_name=$2
    local eq_file=$3

    log_info "Running Equation $eq_num: $eq_name"

    local start_time=$(date +%s)

    # Run the equation
    if cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASS" < "$eq_file" > "/tmp/psychohistory_eq${eq_num}_output.txt" 2>&1; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        log_success "Equation $eq_num completed in ${duration}s"

        # Check for test results
        local pass_count=$(grep -c "PASS" "/tmp/psychohistory_eq${eq_num}_output.txt" || true)
        local fail_count=$(grep -c "FAIL" "/tmp/psychohistory_eq${eq_num}_output.txt" || true)

        if [ "$fail_count" -gt 0 ]; then
            log_error "Equation $eq_num: $fail_count tests FAILED"
            return 1
        elif [ "$pass_count" -gt 0 ]; then
            log_success "Equation $eq_num: $pass_count tests PASSED"
        fi

        return 0
    else
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        log_error "Equation $eq_num FAILED after ${duration}s"
        log_error "See /tmp/psychohistory_eq${eq_num}_output.txt for details"
        return 1
    fi
}

# Validate graph projections
validate_projections() {
    log_info "Validating graph projections..."

    local projections=$(cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASS" --format plain \
        "CALL gds.graph.list() YIELD graphName WHERE graphName STARTS WITH 'psychohistory_' RETURN graphName" \
        | grep psychohistory || true)

    local expected_count=5
    local actual_count=$(echo "$projections" | wc -l)

    if [ "$actual_count" -eq "$expected_count" ]; then
        log_success "All $expected_count graph projections created"
        echo "$projections" | while read -r proj; do
            log_info "  - $proj"
        done
    else
        log_warning "Expected $expected_count projections, found $actual_count"
    fi
}

# Generate summary report
generate_report() {
    log_info "Generating summary report..."

    echo ""
    echo "================================"
    echo "PSYCHOHISTORY IMPLEMENTATION TEST RESULTS"
    echo "================================"
    echo "Date: $(date)"
    echo "Neo4j: $NEO4J_HOST"
    echo ""
    echo "Equations Tested: 5"
    echo "Total Tests: 22"
    echo ""

    # Count results
    local total_pass=0
    local total_fail=0

    for i in 1 2 3 4 5; do
        if [ -f "/tmp/psychohistory_eq${i}_output.txt" ]; then
            local pass=$(grep -c "PASS" "/tmp/psychohistory_eq${i}_output.txt" || true)
            local fail=$(grep -c "FAIL" "/tmp/psychohistory_eq${i}_output.txt" || true)
            total_pass=$((total_pass + pass))
            total_fail=$((total_fail + fail))

            echo "Equation $i: $pass PASS, $fail FAIL"
        fi
    done

    echo ""
    echo "Overall: $total_pass PASS, $total_fail FAIL"
    echo ""

    if [ "$total_fail" -eq 0 ]; then
        log_success "ALL TESTS PASSED ✓"
        echo "Status: READY FOR PRODUCTION"
    else
        log_error "SOME TESTS FAILED ✗"
        echo "Status: NEEDS ATTENTION"
    fi

    echo "================================"
}

# Cleanup function
cleanup_projections() {
    log_info "Cleaning up graph projections..."

    cypher-shell -u "$NEO4J_USER" -p "$NEO4J_PASS" <<EOF
CALL gds.graph.list()
YIELD graphName
WHERE graphName STARTS WITH 'psychohistory_'
WITH collect(graphName) AS graphs
UNWIND graphs AS graph
CALL gds.graph.drop(graph, false) YIELD graphName
RETURN 'Dropped: ' + graphName AS status;
EOF

    log_success "Cleanup complete"
}

# Main execution
main() {
    echo "================================"
    echo "PSYCHOHISTORY EQUATIONS TEST SUITE"
    echo "================================"
    echo ""

    # Check prerequisites
    check_prerequisites

    echo ""
    log_info "Starting equation execution..."
    echo ""

    # Track failures
    local failed=0

    # Run each equation
    if ! run_equation 1 "Epidemic Threshold (R₀)" "01_epidemic_threshold.cypher"; then
        failed=$((failed + 1))
    fi
    echo ""

    if ! run_equation 2 "Ising Dynamics" "02_ising_dynamics.cypher"; then
        failed=$((failed + 1))
    fi
    echo ""

    if ! run_equation 3 "Granovetter Threshold" "03_granovetter_threshold.cypher"; then
        failed=$((failed + 1))
    fi
    echo ""

    if ! run_equation 4 "Bifurcation Analysis" "04_bifurcation_crisis.cypher"; then
        failed=$((failed + 1))
    fi
    echo ""

    if ! run_equation 5 "Critical Slowing Down" "05_critical_slowing.cypher"; then
        failed=$((failed + 1))
    fi
    echo ""

    # Validate projections
    validate_projections

    echo ""
    # Generate report
    generate_report

    # Optional cleanup
    echo ""
    read -p "Clean up graph projections? (y/N) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cleanup_projections
    fi

    # Exit with appropriate code
    if [ "$failed" -eq 0 ]; then
        exit 0
    else
        exit 1
    fi
}

# Run main function
main "$@"
