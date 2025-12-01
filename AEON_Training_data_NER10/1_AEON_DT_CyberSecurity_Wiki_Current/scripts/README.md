# AEON Utility Scripts

**Directory**: `/home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/scripts/`
**Created**: 2025-11-12 06:55:00 UTC
**Purpose**: Utility scripts for AEON development, maintenance, and validation
**Status**: ACTIVE

---

## Available Scripts

### 1. verify_paths.py

**Purpose**: Verify all file paths, imports, and references before moving/archiving files
**Constitutional Reference**: Article II, Section 2.8 (Path Integrity)

**Features**:
- ✅ Check Python imports and module paths
- ✅ Verify file path references in all code
- ✅ Validate API endpoint consistency
- ✅ Check Docker volume mounts and configurations
- ✅ Detect broken references in markdown documentation
- ✅ Generate detailed reports with severity levels
- ✅ Export issues as JSON for programmatic processing

**Usage**:
```bash
# Check entire project
python verify_paths.py --check-all

# Check specific file
python verify_paths.py --check-file /path/to/file.py

# Check directory
python verify_paths.py --check-dir /path/to/directory

# Generate detailed report
python verify_paths.py --check-all --report --output verification_report.txt

# Export as JSON
python verify_paths.py --check-all --json issues.json

# Verbose mode
python verify_paths.py --check-all --verbose
```

**Output**:
```
================================================================================
VERIFICATION COMPLETE
================================================================================
Files Checked: 1,234
Total Lines: 156,789
Issues Found: 42

By Severity:
  CRITICAL :     3
  HIGH     :    12
  MEDIUM   :    18
  LOW      :     9

⚠️  42 path issues found!
```

**Recommended Workflow**:
1. **Before moving/archiving files**: Run `verify_paths.py --check-all`
2. **After refactoring**: Run `verify_paths.py --check-dir /path/to/changed/directory`
3. **CI/CD Integration**: Add to pre-commit hooks or CI pipeline
4. **Regular audits**: Run weekly to detect path drift

**Issue Types Detected**:
| Issue Type | Severity | Description |
|------------|----------|-------------|
| `broken_import` | HIGH | Python/JS import statement references non-existent module |
| `missing_file` | HIGH | File path reference points to missing file |
| `invalid_endpoint` | LOW | API endpoint referenced but not found in backend |
| `broken_reference` | MEDIUM | Generic broken reference (config, documentation) |

**Exit Codes**:
- `0`: No issues found ✅
- `1`: Path issues detected ⚠️

---

## Script Development Guidelines

### Adding New Scripts

When adding new utility scripts to this directory:

1. **File Naming**: Use descriptive snake_case names (e.g., `verify_paths.py`, `sync_databases.py`)
2. **Shebang**: Include `#!/usr/bin/env python3` or appropriate shebang
3. **Make Executable**: `chmod +x script_name.py`
4. **Documentation**: Add comprehensive docstring at top of file
5. **Update README**: Document the new script in this README
6. **TASKMASTER**: Reference any related TASKMASTER tasks

### Script Template

```python
#!/usr/bin/env python3
"""
AEON [Script Name]

File: script_name.py
Created: YYYY-MM-DD HH:MM:SS UTC
Modified: YYYY-MM-DD HH:MM:SS UTC
Version: 1.0.0
Author: AEON Development Team
Purpose: [Brief description]
Status: ACTIVE
Constitutional Reference: [If applicable]
TASKMASTER Reference: TASK-YYYY-MM-DD-XXX

USAGE:
    python script_name.py [options]

OPTIONS:
    --option1    Description
    --option2    Description

EXAMPLES:
    python script_name.py --option1 value
"""

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="[Script description]")
    # Add arguments
    args = parser.parse_args()

    # Script logic

    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## Future Scripts (Planned)

### sync_databases.py (PLANNED)
**Purpose**: Synchronize data between Neo4j, PostgreSQL, and Qdrant
**TASKMASTER**: TASK-2025-11-12-030
**Status**: NOT YET CREATED

### validate_constitution.py (PLANNED)
**Purpose**: Verify code compliance with Constitutional rules
**TASKMASTER**: TASK-2025-11-12-031
**Status**: NOT YET CREATED

### health_check.py (PLANNED)
**Purpose**: Comprehensive health check for all services
**TASKMASTER**: TASK-2025-11-12-029
**Status**: NOT YET CREATED

### backup_restore.py (PLANNED)
**Purpose**: Backup and restore all databases and configurations
**TASKMASTER**: Future task
**Status**: NOT YET CREATED

---

## Integration with CI/CD

### Pre-Commit Hook

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Run path verification before commit
python /home/jim/2_OXOT_Projects_Dev/1_AEON_DT_CyberSecurity_Wiki_Current/scripts/verify_paths.py --check-all

if [ $? -ne 0 ]; then
    echo "❌ Path verification failed! Please fix issues before committing."
    exit 1
fi

echo "✅ Path verification passed!"
exit 0
```

### GitHub Actions

Add to `.github/workflows/path-verification.yml`:
```yaml
name: Path Verification

on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Verify paths
        run: |
          python scripts/verify_paths.py --check-all --report --output verification_report.txt
      - name: Upload report
        if: failure()
        uses: actions/upload-artifact@v2
        with:
          name: path-verification-report
          path: verification_report.txt
```

---

## Maintenance

**Last Updated**: 2025-11-12 06:55:00 UTC
**Maintainer**: AEON Development Team
**Update Frequency**: Add new scripts as needed, update documentation immediately

---

*AEON Utility Scripts | Development Tools | Constitutional Compliance*
