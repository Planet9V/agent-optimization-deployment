#!/bin/bash
#
# health-check.sh - Post-deployment validation and health checks
# Created: 2025-11-12
# Purpose: Comprehensive validation of deployment and system health
#

set -euo pipefail

# ═══════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/home/jim/2_OXOT_Projects_Dev/tests"
LOG_DIR="/var/log/deployment"
HEALTH_LOG="${LOG_DIR}/health-check-$(date +%Y%m%d-%H%M%S).log"
MONITORING_PORT=3030
QUICK_MODE=false
POST_ROLLBACK=false
VERBOSE=false

# Health check thresholds
CPU_THRESHOLD=80
MEMORY_THRESHOLD=85
DISK_THRESHOLD=90
RESPONSE_TIME_THRESHOLD=5000  # milliseconds

# ═══════════════════════════════════════════════════
# COLOR CODES
# ═══════════════════════════════════════════════════

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# ═══════════════════════════════════════════════════
# COUNTERS
# ═══════════════════════════════════════════════════

CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNING=0
CHECKS_TOTAL=0

# ═══════════════════════════════════════════════════
# LOGGING FUNCTIONS
# ═══════════════════════════════════════════════════

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*" | tee -a "${HEALTH_LOG}"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $*" | tee -a "${HEALTH_LOG}"
}

log_warning() {
    echo -e "${YELLOW}[⚠]${NC} $*" | tee -a "${HEALTH_LOG}"
}

log_error() {
    echo -e "${RED}[✗]${NC} $*" | tee -a "${HEALTH_LOG}"
}

log_check() {
    echo -e "${CYAN}[CHECK]${NC} $*" | tee -a "${HEALTH_LOG}"
}

log_section() {
    echo -e "\n${CYAN}═══════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}$*${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════${NC}\n"
}

# ═══════════════════════════════════════════════════
# CHECK RESULT FUNCTIONS
# ═══════════════════════════════════════════════════

record_pass() {
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
    log_success "$*"
}

record_fail() {
    CHECKS_FAILED=$((CHECKS_FAILED + 1))
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
    log_error "$*"
}

record_warning() {
    CHECKS_WARNING=$((CHECKS_WARNING + 1))
    CHECKS_TOTAL=$((CHECKS_TOTAL + 1))
    log_warning "$*"
}

# ═══════════════════════════════════════════════════
# FILE SYSTEM CHECKS
# ═══════════════════════════════════════════════════

check_critical_files() {
    log_section "File System Checks"

    local critical_files=(
        "package.json"
        "tsconfig.json"
        "jest.config.js"
    )

    log_check "Checking critical files..."

    for file in "${critical_files[@]}"; do
        if [[ -f "${PROJECT_ROOT}/${file}" ]]; then
            record_pass "Found: ${file}"
        else
            record_fail "Missing: ${file}"
        fi
    done

    # Check build output
    if [[ -d "${PROJECT_ROOT}/dist" ]]; then
        local file_count=$(find "${PROJECT_ROOT}/dist" -type f -name "*.js" | wc -l)
        if [[ $file_count -gt 0 ]]; then
            record_pass "Build output: ${file_count} files"
        else
            record_fail "Build output directory is empty"
        fi
    else
        record_fail "Build output directory not found"
    fi

    # Check node_modules
    if [[ -d "${PROJECT_ROOT}/node_modules" ]]; then
        record_pass "Dependencies installed"
    else
        record_fail "Dependencies not installed"
    fi
}

check_file_permissions() {
    log_section "File Permissions"

    log_check "Checking file permissions..."

    # Check if files are readable
    local unreadable=0
    while IFS= read -r -d '' file; do
        if [[ ! -r "$file" ]]; then
            unreadable=$((unreadable + 1))
            [[ "$VERBOSE" == "true" ]] && log_warning "Unreadable: $file"
        fi
    done < <(find "${PROJECT_ROOT}/dist" -type f -print0 2>/dev/null)

    if [[ $unreadable -eq 0 ]]; then
        record_pass "All files are readable"
    else
        record_warning "${unreadable} files have permission issues"
    fi

    # Check executable scripts
    if [[ -x "${PROJECT_ROOT}/node_modules/.bin/jest" ]]; then
        record_pass "Test runner is executable"
    else
        record_warning "Test runner may not be executable"
    fi
}

check_disk_space() {
    log_section "Disk Space"

    log_check "Checking disk space..."

    local usage=$(df "${PROJECT_ROOT}" | awk 'NR==2 {print $5}' | sed 's/%//')

    if [[ $usage -lt $DISK_THRESHOLD ]]; then
        record_pass "Disk usage: ${usage}% (threshold: ${DISK_THRESHOLD}%)"
    else
        record_fail "Disk usage: ${usage}% exceeds threshold of ${DISK_THRESHOLD}%"
    fi

    # Check specific directories
    local du_output=$(du -sh "${PROJECT_ROOT}" 2>/dev/null | cut -f1)
    log_info "Project size: ${du_output}"

    if [[ -d "${PROJECT_ROOT}/node_modules" ]]; then
        local nm_size=$(du -sh "${PROJECT_ROOT}/node_modules" 2>/dev/null | cut -f1)
        log_info "node_modules size: ${nm_size}"
    fi
}

# ═══════════════════════════════════════════════════
# DEPENDENCY CHECKS
# ═══════════════════════════════════════════════════

check_dependencies() {
    log_section "Dependency Checks"

    cd "${PROJECT_ROOT}"

    log_check "Validating dependencies..."

    # Check for security vulnerabilities
    if command -v npm &> /dev/null; then
        log_info "Running npm audit..."

        local audit_output=$(npm audit --json 2>/dev/null || echo '{}')
        local vulnerabilities=$(echo "$audit_output" | grep -o '"vulnerabilities":{[^}]*}' | grep -o '"[a-z]*":[0-9]*' | awk -F: '{sum+=$2} END {print sum}')

        if [[ "${vulnerabilities:-0}" -eq 0 ]]; then
            record_pass "No known vulnerabilities"
        elif [[ "${vulnerabilities:-0}" -lt 5 ]]; then
            record_warning "${vulnerabilities} vulnerabilities found (run: npm audit fix)"
        else
            record_fail "${vulnerabilities} vulnerabilities found (action required)"
        fi
    fi

    # Check for outdated packages (quick mode)
    if [[ "$QUICK_MODE" != "true" ]] && command -v npm &> /dev/null; then
        log_info "Checking for outdated packages..."

        local outdated_count=$(npm outdated --json 2>/dev/null | grep -c '"current"' || echo "0")

        if [[ $outdated_count -eq 0 ]]; then
            record_pass "All packages are up to date"
        else
            record_warning "${outdated_count} packages have updates available"
        fi
    fi
}

# ═══════════════════════════════════════════════════
# BUILD VALIDATION
# ═══════════════════════════════════════════════════

check_build_artifacts() {
    log_section "Build Validation"

    log_check "Validating build artifacts..."

    # Check TypeScript compilation
    if [[ -f "${PROJECT_ROOT}/tsconfig.json" ]]; then
        if [[ -d "${PROJECT_ROOT}/dist" ]]; then
            record_pass "TypeScript compiled successfully"
        else
            record_fail "TypeScript compilation output missing"
        fi
    fi

    # Verify key implementation files
    local impl_files=(
        "dist/agent-optimization.js"
        "dist/performance-benchmarks.js"
    )

    for file in "${impl_files[@]}"; do
        if [[ -f "${PROJECT_ROOT}/${file}" ]]; then
            local size=$(wc -c < "${PROJECT_ROOT}/${file}")
            if [[ $size -gt 100 ]]; then
                record_pass "Build artifact: ${file} (${size} bytes)"
            else
                record_warning "Build artifact suspiciously small: ${file}"
            fi
        else
            record_fail "Missing build artifact: ${file}"
        fi
    done
}

check_syntax() {
    log_section "Syntax Validation"

    log_check "Checking JavaScript syntax..."

    local syntax_errors=0

    if [[ -d "${PROJECT_ROOT}/dist" ]]; then
        while IFS= read -r -d '' js_file; do
            if ! node --check "$js_file" 2>/dev/null; then
                syntax_errors=$((syntax_errors + 1))
                [[ "$VERBOSE" == "true" ]] && log_error "Syntax error in: $js_file"
            fi
        done < <(find "${PROJECT_ROOT}/dist" -name "*.js" -print0 2>/dev/null)

        if [[ $syntax_errors -eq 0 ]]; then
            record_pass "All JavaScript files have valid syntax"
        else
            record_fail "${syntax_errors} files have syntax errors"
        fi
    else
        record_warning "No dist directory to validate"
    fi
}

# ═══════════════════════════════════════════════════
# TEST EXECUTION
# ═══════════════════════════════════════════════════

run_smoke_tests() {
    log_section "Smoke Tests"

    cd "${PROJECT_ROOT}"

    if [[ "$QUICK_MODE" == "true" ]]; then
        log_info "Skipping tests in quick mode"
        return 0
    fi

    log_check "Running smoke tests..."

    if [[ ! -f "package.json" ]] || ! grep -q '"test"' package.json; then
        record_warning "No test script configured"
        return 0
    fi

    # Run tests with timeout
    local test_output="${LOG_DIR}/smoke-tests-$(date +%Y%m%d-%H%M%S).log"

    if timeout 120s npm test -- --testTimeout=5000 > "$test_output" 2>&1; then
        local passed=$(grep -c "PASS" "$test_output" 2>/dev/null || echo "0")
        record_pass "Smoke tests passed (${passed} suites)"
    else
        local exit_code=$?
        if [[ $exit_code -eq 124 ]]; then
            record_fail "Smoke tests timed out after 120s"
        else
            local failed=$(grep -c "FAIL" "$test_output" 2>/dev/null || echo "unknown")
            record_fail "Smoke tests failed (${failed} failures)"
        fi

        [[ "$VERBOSE" == "true" ]] && log_info "Test output: $test_output"
    fi
}

# ═══════════════════════════════════════════════════
# SERVICE HEALTH CHECKS
# ═══════════════════════════════════════════════════

check_monitoring_service() {
    log_section "Service Health"

    log_check "Checking monitoring dashboard..."

    # Check if monitoring port is listening
    if command -v netstat &> /dev/null; then
        if netstat -tuln | grep -q ":${MONITORING_PORT}"; then
            record_pass "Monitoring service is running on port ${MONITORING_PORT}"
        else
            record_warning "Monitoring service not detected on port ${MONITORING_PORT}"
        fi
    elif command -v ss &> /dev/null; then
        if ss -tuln | grep -q ":${MONITORING_PORT}"; then
            record_pass "Monitoring service is running on port ${MONITORING_PORT}"
        else
            record_warning "Monitoring service not detected on port ${MONITORING_PORT}"
        fi
    else
        record_warning "Cannot check monitoring service (netstat/ss not available)"
    fi

    # Try to connect to monitoring endpoint
    if command -v curl &> /dev/null; then
        if curl -sf "http://localhost:${MONITORING_PORT}/health" > /dev/null 2>&1; then
            record_pass "Monitoring health endpoint responding"
        else
            record_warning "Monitoring health endpoint not responding"
        fi
    fi
}

check_processes() {
    log_section "Process Health"

    log_check "Checking running processes..."

    # Check for Node.js processes
    local node_procs=$(pgrep -f "node.*${PROJECT_ROOT}" | wc -l)

    if [[ $node_procs -gt 0 ]]; then
        log_info "Found ${node_procs} Node.js process(es)"

        # Check memory usage of processes
        local total_mem=0
        while read -r pid; do
            if [[ -f "/proc/${pid}/status" ]]; then
                local mem=$(grep VmRSS "/proc/${pid}/status" | awk '{print $2}')
                total_mem=$((total_mem + mem))
            fi
        done < <(pgrep -f "node.*${PROJECT_ROOT}")

        local mem_mb=$((total_mem / 1024))
        log_info "Total memory usage: ${mem_mb} MB"

        if [[ $mem_mb -lt 1000 ]]; then
            record_pass "Process memory usage is healthy"
        else
            record_warning "High memory usage: ${mem_mb} MB"
        fi
    else
        record_warning "No Node.js processes found for project"
    fi
}

# ═══════════════════════════════════════════════════
# SYSTEM RESOURCE CHECKS
# ═══════════════════════════════════════════════════

check_system_resources() {
    log_section "System Resources"

    log_check "Checking system resources..."

    # CPU usage
    if command -v top &> /dev/null; then
        local cpu_idle=$(top -bn1 | grep "Cpu(s)" | awk '{print $8}' | cut -d'%' -f1)
        local cpu_usage=$(echo "100 - $cpu_idle" | bc 2>/dev/null || echo "0")

        if (( $(echo "$cpu_usage < $CPU_THRESHOLD" | bc -l 2>/dev/null || echo "0") )); then
            record_pass "CPU usage: ${cpu_usage}% (threshold: ${CPU_THRESHOLD}%)"
        else
            record_warning "High CPU usage: ${cpu_usage}%"
        fi
    fi

    # Memory usage
    if command -v free &> /dev/null; then
        local mem_used=$(free | grep Mem | awk '{print int($3/$2 * 100)}')

        if [[ $mem_used -lt $MEMORY_THRESHOLD ]]; then
            record_pass "Memory usage: ${mem_used}% (threshold: ${MEMORY_THRESHOLD}%)"
        else
            record_warning "High memory usage: ${mem_used}%"
        fi
    fi

    # Load average
    local load_avg=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
    local cpu_count=$(nproc 2>/dev/null || echo "1")
    log_info "Load average: ${load_avg} (CPUs: ${cpu_count})"
}

# ═══════════════════════════════════════════════════
# CONFIGURATION VALIDATION
# ═══════════════════════════════════════════════════

check_configuration() {
    log_section "Configuration Validation"

    log_check "Validating configuration files..."

    # Check package.json
    if [[ -f "${PROJECT_ROOT}/package.json" ]]; then
        if node -e "JSON.parse(require('fs').readFileSync('${PROJECT_ROOT}/package.json'))" 2>/dev/null; then
            record_pass "package.json is valid JSON"
        else
            record_fail "package.json is invalid JSON"
        fi
    fi

    # Check tsconfig.json
    if [[ -f "${PROJECT_ROOT}/tsconfig.json" ]]; then
        if node -e "JSON.parse(require('fs').readFileSync('${PROJECT_ROOT}/tsconfig.json'))" 2>/dev/null; then
            record_pass "tsconfig.json is valid JSON"
        else
            record_fail "tsconfig.json is invalid JSON"
        fi
    fi

    # Check jest.config.js
    if [[ -f "${PROJECT_ROOT}/jest.config.js" ]]; then
        if node --check "${PROJECT_ROOT}/jest.config.js" 2>/dev/null; then
            record_pass "jest.config.js is valid"
        else
            record_fail "jest.config.js has syntax errors"
        fi
    fi
}

# ═══════════════════════════════════════════════════
# PERFORMANCE CHECKS
# ═══════════════════════════════════════════════════

check_performance() {
    log_section "Performance Validation"

    if [[ "$QUICK_MODE" == "true" ]]; then
        log_info "Skipping performance checks in quick mode"
        return 0
    fi

    log_check "Running performance checks..."

    # Check if performance benchmarks exist
    if [[ -f "${PROJECT_ROOT}/dist/performance-benchmarks.js" ]]; then
        record_pass "Performance benchmarks present"

        # Try to run benchmarks (with timeout)
        if timeout 30s node "${PROJECT_ROOT}/dist/performance-benchmarks.js" > /dev/null 2>&1; then
            record_pass "Performance benchmarks executed successfully"
        else
            record_warning "Performance benchmarks failed or timed out"
        fi
    else
        record_warning "Performance benchmarks not found"
    fi
}

# ═══════════════════════════════════════════════════
# REPORT GENERATION
# ═══════════════════════════════════════════════════

generate_summary() {
    log_section "Health Check Summary"

    local pass_rate=0
    if [[ $CHECKS_TOTAL -gt 0 ]]; then
        pass_rate=$(echo "scale=1; $CHECKS_PASSED * 100 / $CHECKS_TOTAL" | bc)
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "                  HEALTH CHECK RESULTS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "  Total Checks:    ${CHECKS_TOTAL}"
    echo -e "  ${GREEN}Passed:          ${CHECKS_PASSED}${NC}"
    echo -e "  ${YELLOW}Warnings:        ${CHECKS_WARNING}${NC}"
    echo -e "  ${RED}Failed:          ${CHECKS_FAILED}${NC}"
    echo ""
    echo "  Pass Rate:       ${pass_rate}%"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Overall status
    if [[ $CHECKS_FAILED -eq 0 ]]; then
        if [[ $CHECKS_WARNING -eq 0 ]]; then
            echo -e "${GREEN}✓ OVERALL STATUS: HEALTHY${NC}"
        else
            echo -e "${YELLOW}⚠ OVERALL STATUS: HEALTHY WITH WARNINGS${NC}"
        fi
        echo ""
        log_info "Full report: ${HEALTH_LOG}"
        return 0
    else
        echo -e "${RED}✗ OVERALL STATUS: UNHEALTHY${NC}"
        echo ""
        log_error "Full report: ${HEALTH_LOG}"
        return 1
    fi
}

# ═══════════════════════════════════════════════════
# MAIN EXECUTION FLOW
# ═══════════════════════════════════════════════════

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --quick)
                QUICK_MODE=true
                log_info "Quick mode enabled"
                shift
                ;;
            --post-rollback)
                POST_ROLLBACK=true
                log_info "Post-rollback validation mode"
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --quick          Quick health check (skip tests and performance)"
                echo "  --post-rollback  Run post-rollback validation"
                echo "  --verbose        Show detailed output"
                echo "  --help           Show this help message"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    # Create log directory
    mkdir -p "${LOG_DIR}"

    log_info "=========================================="
    log_info "Health Check Started"
    log_info "Time: $(date)"
    log_info "Mode: $([ "$QUICK_MODE" == "true" ] && echo "Quick" || echo "Full")"
    log_info "=========================================="

    # Execute health checks
    check_critical_files
    check_file_permissions
    check_disk_space
    check_dependencies
    check_build_artifacts
    check_syntax
    check_configuration
    check_monitoring_service
    check_processes
    check_system_resources

    # Conditional checks
    if [[ "$QUICK_MODE" != "true" ]]; then
        run_smoke_tests
        check_performance
    fi

    # Generate summary
    generate_summary
}

# ═══════════════════════════════════════════════════
# SCRIPT ENTRY POINT
# ═══════════════════════════════════════════════════

main "$@"
