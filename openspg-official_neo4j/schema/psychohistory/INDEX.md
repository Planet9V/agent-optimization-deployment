# Psychohistory Equations - Complete File Index

**Project**: Psychohistory for Neo4j ICS Threat Intelligence
**Date**: 2025-11-26
**Version**: 1.0.0
**Status**: Production Ready

---

## Quick Navigation

| Need | File | Purpose |
|------|------|---------|
| **Start Here** | [README.md](README.md) | Complete user guide |
| **Quick Reference** | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | One-page cheat sheet |
| **Run Everything** | [00_master_execution.cypher](00_master_execution.cypher) | Master script |
| **Test Suite** | [run_all_tests.sh](run_all_tests.sh) | Automated testing |
| **Implementation Details** | [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | Technical deep dive |

---

## Core Equation Files

### 1. Epidemic Threshold (R₀)
**File**: [01_epidemic_threshold.cypher](01_epidemic_threshold.cypher)
**Lines**: 317
**Tests**: 3

**What it does**: Predicts whether malware, attack techniques, or beliefs will spread epidemically through the network.

**Key outputs**:
- R₀ values for different scenarios
- Super-spreader identification
- Network vulnerability assessment
- Critical node analysis

**When to use**:
- Predicting malware propagation
- Identifying critical vulnerabilities
- Assessing network epidemic risk

---

### 2. Ising Dynamics (Opinion Formation)
**File**: [02_ising_dynamics.cypher](02_ising_dynamics.cypher)
**Lines**: 401
**Tests**: 4

**What it does**: Models how opinions, beliefs, and attack preferences propagate and reach consensus in adversary networks.

**Key outputs**:
- Opinion state evolution
- Community polarization detection
- Influencer identification
- Cascade probability calculation

**When to use**:
- Tracking adversary belief systems
- Predicting technique adoption
- Identifying opinion leaders
- Modeling propaganda effects

---

### 3. Granovetter Threshold Model (Adoption Cascades)
**File**: [03_granovetter_threshold.cypher](03_granovetter_threshold.cypher)
**Lines**: 424
**Tests**: 5

**What it does**: Simulates adoption cascades showing how attack techniques spread through threshold-based social influence.

**Key outputs**:
- Cascade simulation results
- Tipping point identification
- Adoption velocity over time
- Critical mass calculation

**When to use**:
- Predicting technique viral spread
- Identifying early vs late adopters
- Finding cascade trigger actors
- Planning defensive interventions

---

### 4. Bifurcation Analysis (Seldon Crisis Detection)
**File**: [04_bifurcation_crisis.cypher](04_bifurcation_crisis.cypher)
**Lines**: 442
**Tests**: 5

**What it does**: Detects critical transition points where small changes cause catastrophic regime shifts.

**Key outputs**:
- Seldon crisis point detection
- Bifurcation diagrams
- Hysteresis analysis
- Early warning signals

**When to use**:
- Predicting sector catastrophic failures
- Identifying system tipping points
- Detecting impending regime changes
- Planning crisis interventions

---

### 5. Critical Slowing Down (Early Warning Signals)
**File**: [05_critical_slowing.cypher](05_critical_slowing.cypher)
**Lines**: 527
**Tests**: 5

**What it does**: Detects early warning signals before catastrophic transitions through statistical analysis.

**Key outputs**:
- Variance trend analysis
- Autocorrelation at multiple lags
- Detrended fluctuation analysis
- Composite early warning scores

**When to use**:
- Advance warning of major attacks
- Monitoring system resilience
- Triggering preventive interventions
- Real-time risk monitoring

---

## Documentation Files

### README.md
**Lines**: 513
**Sections**: 15

**Contents**:
- Complete equation descriptions
- Installation instructions
- Architecture details
- Validation procedures
- Performance characteristics
- Interpretation guides
- Use cases
- Troubleshooting
- Advanced features
- References

**Audience**: All users (developers, analysts, operators)

---

### QUICK_REFERENCE.md
**Lines**: 429
**Sections**: 12

**Contents**:
- One-page equation summary
- Quick execution commands
- Essential queries
- Color-coded risk levels
- Decision matrix
- Common workflows
- Performance tuning
- Monitoring dashboards
- Cleanup commands
- Integration examples

**Audience**: Operators and analysts needing quick answers

---

### IMPLEMENTATION_SUMMARY.md
**Lines**: 591
**Sections**: 14

**Contents**:
- Executive summary
- Technical architecture
- Detailed equation breakdowns
- NER11_Gold integration
- Performance benchmarks
- Validation results
- Usage scenarios
- Limitations and future work
- Deployment recommendations
- Testing instructions

**Audience**: Technical leads and architects

---

## Support Files

### 00_master_execution.cypher
**Lines**: 236
**Purpose**: Run all 5 equations sequentially

**Features**:
- Environment verification
- Sequential equation execution
- Progress checkpoints
- Comprehensive validation
- Optional cleanup

**Usage**:
```bash
cypher-shell < 00_master_execution.cypher
```

---

### run_all_tests.sh
**Lines**: 270
**Purpose**: Automated test suite

**Features**:
- Prerequisites checking
- Automated equation execution
- Result validation
- Summary report generation
- Optional cleanup

**Usage**:
```bash
./run_all_tests.sh [neo4j_password]
```

---

### INDEX.md (This File)
**Lines**: Current file
**Purpose**: Complete file directory and navigation guide

---

## File Statistics

```
Total Files: 10
Total Lines: 3,880

Breakdown:
  Cypher Code:   2,347 lines (60.5%)
  Documentation: 1,533 lines (39.5%)

Equation Files:     2,111 lines
Support Scripts:      236 lines
Documentation:      1,533 lines
```

---

## Directory Structure

```
openspg-official_neo4j/schema/psychohistory/
├── INDEX.md                         # This file
├── README.md                        # Complete user guide
├── QUICK_REFERENCE.md               # One-page cheat sheet
├── IMPLEMENTATION_SUMMARY.md        # Technical deep dive
├── 00_master_execution.cypher       # Master script
├── 01_epidemic_threshold.cypher     # R₀ equation
├── 02_ising_dynamics.cypher         # Opinion dynamics
├── 03_granovetter_threshold.cypher  # Adoption cascades
├── 04_bifurcation_crisis.cypher     # Crisis detection
├── 05_critical_slowing.cypher       # Early warnings
└── run_all_tests.sh                 # Test automation
```

---

## Usage Paths

### Path 1: First-Time User
1. Read [README.md](README.md) - Understand what this does
2. Run [run_all_tests.sh](run_all_tests.sh) - Verify installation
3. Review [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Learn key queries
4. Execute individual equations as needed

### Path 2: Quick Start
1. Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Find your use case
2. Run [00_master_execution.cypher](00_master_execution.cypher) - Get all results
3. Query results using quick reference examples

### Path 3: Production Deployment
1. Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Understand architecture
2. Run [run_all_tests.sh](run_all_tests.sh) - Validate environment
3. Configure monitoring dashboards from [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
4. Schedule equation execution per operational workflow

### Path 4: Development/Customization
1. Read [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical details
2. Study individual equation files - Understand implementation
3. Modify parameters in equation files - Customize for your data
4. Run [run_all_tests.sh](run_all_tests.sh) - Validate changes

---

## Common Tasks

### Task: Run all equations
```bash
# Option 1: Use master script
cypher-shell < 00_master_execution.cypher

# Option 2: Use test runner
./run_all_tests.sh password
```

### Task: Run single equation
```bash
cypher-shell < 01_epidemic_threshold.cypher
```

### Task: Get quick results
See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Essential Queries section

### Task: Understand equation
See [README.md](README.md) - Equation-specific section

### Task: Troubleshoot issues
See [README.md](README.md) - Troubleshooting section

### Task: Deploy to production
See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Deployment Recommendations

---

## Equation Selection Guide

**Use this flowchart to choose which equation to run:**

```
Do you want to predict...

├─ How fast something will spread?
│  └─ Use: 01_epidemic_threshold.cypher (R₀)
│
├─ How opinions/beliefs will evolve?
│  └─ Use: 02_ising_dynamics.cypher (Ising)
│
├─ Whether a technique will go viral?
│  └─ Use: 03_granovetter_threshold.cypher (Granovetter)
│
├─ When a crisis/collapse will occur?
│  └─ Use: 04_bifurcation_crisis.cypher (Bifurcation)
│
└─ If a major change is approaching?
   └─ Use: 05_critical_slowing.cypher (Critical Slowing)
```

---

## Integration Guides

### Python Integration
See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Integration Examples section

### REST API
See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Integration Examples section

### Dashboard Integration
See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Monitoring Dashboard Queries section

### SIEM Integration
See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Deployment Recommendations section

---

## Version History

### v1.0.0 (2025-11-26)
- Initial release
- All 5 core equations implemented
- Complete documentation suite
- Automated test runner
- Production-ready status

---

## Support Resources

### Documentation
- **Complete Guide**: [README.md](README.md)
- **Quick Reference**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Technical Details**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

### Code
- **Master Script**: [00_master_execution.cypher](00_master_execution.cypher)
- **Individual Equations**: 01-05_*.cypher files
- **Test Suite**: [run_all_tests.sh](run_all_tests.sh)

### Help
- Check troubleshooting section in [README.md](README.md)
- Review examples in [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- Examine test output from [run_all_tests.sh](run_all_tests.sh)

---

## Quality Metrics

**Code Quality**:
- ✅ Zero TODO comments
- ✅ Zero placeholder code
- ✅ Zero mock data
- ✅ 100% runnable Cypher
- ✅ 22 validation tests included

**Documentation Quality**:
- ✅ Complete README (513 lines)
- ✅ Quick reference guide (429 lines)
- ✅ Implementation summary (591 lines)
- ✅ This index file
- ✅ Inline code comments

**Testing Coverage**:
- ✅ All 5 equations tested
- ✅ 22 validation queries
- ✅ Automated test runner
- ✅ Performance benchmarks
- ✅ Integration examples

---

## Next Steps

1. **New Users**: Start with [README.md](README.md)
2. **Quick Start**: Use [00_master_execution.cypher](00_master_execution.cypher)
3. **Production**: Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
4. **Daily Use**: Bookmark [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

**Last Updated**: 2025-11-26
**Maintained By**: AEON Project Team
**License**: MIT
**Status**: Production Ready ✓
