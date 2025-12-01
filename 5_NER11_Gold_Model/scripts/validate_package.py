#!/usr/bin/env python3
"""
NER11 Gold Standard - Package Validation Script

Validates that the portable package is complete and functional.
"""

import os
from pathlib import Path
import sys

class PackageValidator:
    """Validates NER11 Gold Model package completeness."""
    
    def __init__(self, package_root="."):
        self.root = Path(package_root)
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_total = 0
    
    def check_file_exists(self, filepath, critical=True):
        """Check if a file exists."""
        self.checks_total += 1
        full_path = self.root / filepath
        
        if full_path.exists():
            self.checks_passed += 1
            print(f"✓ {filepath}")
            return True
        else:
            msg = f"✗ Missing: {filepath}"
            if critical:
                self.errors.append(msg)
            else:
                self.warnings.append(msg)
            print(msg)
            return False
    
    def check_directory_exists(self, dirpath):
        """Check if a directory exists."""
        self.checks_total += 1
        full_path = self.root / dirpath
        
        if full_path.is_dir():
            self.checks_passed += 1
            print(f"✓ {dirpath}/")
            return True
        else:
            msg = f"✗ Missing directory: {dirpath}/"
            self.errors.append(msg)
            print(msg)
            return False
    
    def validate_structure(self):
        """Validate directory structure."""
        print("\n" + "="*70)
        print("Validating Directory Structure")
        print("="*70 + "\n")
        
        # Required directories
        dirs = [
            "models",
            "models/model-best",
            "models/model-last",
            "config",
            "docs",
            "training_data",
            "scripts",
            "examples",
            "tests"
        ]
        
        for d in dirs:
            self.check_directory_exists(d)
    
    def validate_documentation(self):
        """Validate documentation files."""
        print("\n" + "="*70)
        print("Validating Documentation")
        print("="*70 + "\n")
        
        docs = [
            "README.md",
            "docs/02_INSTALLATION.md",
            "docs/04_NEO4J_INTEGRATION.md",
            "docs/05_TRAINING_HISTORY.md",
            "training_data/TRAINING_DATA_MANIFEST.md"
        ]
        
        for doc in docs:
            self.check_file_exists(doc)
    
    def validate_config(self):
        """Validate configuration files."""
        print("\n" + "="*70)
        print("Validating Configuration")
        print("="*70 + "\n")
        
        self.check_file_exists("config/requirements.txt")
        self.check_file_exists("config/config.cfg", critical=False)
    
    def validate_scripts(self):
        """Validate scripts."""
        print("\n" + "="*70)
        print("Validating Scripts")
        print("="*70 + "\n")
        
        scripts = [
            "scripts/install.sh",
            "scripts/test_model.py",
            "scripts/neo4j_integration.py"
        ]
        
        for script in scripts:
            if self.check_file_exists(script):
                # Check if executable
                full_path = self.root / script
                if os.access(full_path, os.X_OK):
                    print(f"  → Executable: Yes")
                else:
                    self.warnings.append(f"{script} not executable")
                    print(f"  → Executable: No (warning)")
    
    def validate_examples(self):
        """Validate example files."""
        print("\n" + "="*70)
        print("Validating Examples")
        print("="*70 + "\n")
        
        examples = [
            "examples/basic_usage.py",
            "examples/neo4j_example.py"
        ]
        
        for example in examples:
            self.check_file_exists(example, critical=False)
    
    def validate_models(self):
        """Validate model files."""
        print("\n" + "="*70)
        print("Validating Model Files")
        print("="*70 + "\n")
        
        # Check for key model files
        model_files = [
            "models/model-best/meta.json",
            "models/model-best/config.cfg",
            "models/model-last/meta.json",
            "models/model-last/config.cfg"
        ]
        
        for mf in model_files:
            self.check_file_exists(mf)
    
    def validate_training_data(self):
        """Validate training data files."""
        print("\n" + "="*70)
        print("Validating Training Data")
        print("="*70 + "\n")
        
        self.check_file_exists("training_data/training_local_window64.log")
    
    def print_summary(self):
        """Print validation summary."""
        print("\n" + "="*70)
        print("Validation Summary")
        print("="*70)
        
        print(f"\nChecks Passed: {self.checks_passed}/{self.checks_total}")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")
        
        print("\n" + "="*70)
        
        if not self.errors:
            print("✅ Package validation PASSED!")
            print("\nThe NER11 Gold Model package is complete and ready for use.")
            return True
        else:
            print("❌ Package validation FAILED!")
            print(f"\nPlease fix {len(self.errors)} error(s) before using the package.")
            return False
    
    def run_all_checks(self):
        """Run all validation checks."""
        print("\n" + "="*70)
        print(" "*15 + "NER11 Gold Model - Package Validation")
        print("="*70)
        
        self.validate_structure()
        self.validate_documentation()
        self.validate_config()
        self.validate_scripts()
        self.validate_examples()
        self.validate_models()
        self.validate_training_data()
        
        return self.print_summary()

def main():
    """Main validation function."""
    validator = PackageValidator()
    success = validator.run_all_checks()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
