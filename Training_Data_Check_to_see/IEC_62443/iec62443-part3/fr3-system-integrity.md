# FR 3: System Integrity (SI)

**Objective:** Protect system components from unauthorized modification.

## Technical Requirements

### SL 1 Requirements
- Basic file integrity checks
- Simple change detection
- Manual integrity verification

### SL 2 Requirements
- Automated integrity monitoring
- File integrity monitoring (FIM)
- Change management processes

### SL 3 Requirements
- Secure boot processes
- Memory integrity protection
- Runtime integrity monitoring

### SL 4 Requirements
- Hardware root of trust
- Trusted platform modules (TPM)
- Continuous integrity validation

## Implementation Guidelines

### File Integrity Monitoring System
```javascript
// FIM Implementation for IACS
class IACSFileIntegrityMonitor {
  constructor() {
    this.baselines = new Map();
    this.exclusions = new Set();
    this.alertThreshold = 10; // Max alerts per hour
    this.scanInterval = 300000; // 5 minutes
  }

  // Establish Baseline
  async establishBaseline(directory) {
    console.log(`Establishing baseline for ${directory}`);
    const baseline = await this.calculateHashes(directory);
    this.baselines.set(directory, baseline);
    await this.saveBaseline(directory, baseline);
  }

  // Integrity Check
  async checkIntegrity(directory) {
    const current = await this.calculateHashes(directory);
    const baseline = this.baselines.get(directory);

    if (!baseline) {
      throw new Error(`No baseline found for ${directory}`);
    }

    const changes = this.compareHashes(baseline, current);
    if (changes.length > 0) {
      await this.handleIntegrityViolation(directory, changes);
    }

    return changes;
  }

  // Calculate File Hashes
  async calculateHashes(directory) {
    const hashes = {};
    const files = await this.getFilesRecursively(directory);

    for (const file of files) {
      if (!this.isExcluded(file)) {
        const hash = await this.calculateFileHash(file);
        hashes[file] = {
          hash: hash,
          size: await this.getFileSize(file),
          mtime: await this.getFileMtime(file)
        };
      }
    }

    return hashes;
  }

  // Compare Hashes
  compareHashes(baseline, current) {
    const changes = [];

    // Check for modified files
    for (const [file, baselineData] of Object.entries(baseline)) {
      const currentData = current[file];
      if (!currentData) {
        changes.push({ file, type: 'deleted', baseline: baselineData });
      } else if (currentData.hash !== baselineData.hash) {
        changes.push({
          file,
          type: 'modified',
          baseline: baselineData,
          current: currentData
        });
      }
    }

    // Check for new files
    for (const [file, currentData] of Object.entries(current)) {
      if (!baseline[file]) {
        changes.push({ file, type: 'added', current: currentData });
      }
    }

    return changes;
  }

  // Handle Integrity Violations
  async handleIntegrityViolation(directory, changes) {
    console.log(`Integrity violation detected in ${directory}: ${changes.length} changes`);

    // Log violation
    await this.logViolation(directory, changes);

    // Alert security team
    if (changes.length > this.alertThreshold) {
      await this.sendCriticalAlert(directory, changes);
    } else {
      await this.sendStandardAlert(directory, changes);
    }

    // Execute automated response
    await this.executeAutomatedResponse(directory, changes);
  }

  // Automated Response Actions
  async executeAutomatedResponse(directory, changes) {
    const criticalChanges = changes.filter(change =>
      this.isCriticalFile(change.file) || change.type === 'deleted'
    );

    if (criticalChanges.length > 0) {
      // Critical response: Isolate system
      await this.isolateSystem(directory);
    } else {
      // Standard response: Log and monitor
      await this.enhancedMonitoring(directory);
    }
  }

  // Utility Methods
  async calculateFileHash(filePath) {
    // Implementation using crypto module
    const crypto = require('crypto');
    const fs = require('fs');
    const fileBuffer = fs.readFileSync(filePath);
    return crypto.createHash('sha256').update(fileBuffer).digest('hex');
  }

  isExcluded(filePath) {
    // Check against exclusion patterns
    return this.exclusions.has(filePath) ||
           filePath.includes('/tmp/') ||
           filePath.includes('/log/');
  }

  isCriticalFile(filePath) {
    // Define critical file patterns
    const criticalPatterns = [
      '/etc/passwd',
      '/etc/shadow',
      '/bin/',
      '/sbin/',
      '/*.exe',
      '/*.dll'
    ];

    return criticalPatterns.some(pattern => filePath.includes(pattern));
  }

  async isolateSystem(directory) {
    console.log(`Isolating system due to integrity violation in ${directory}`);
    // Implementation would disable network access, stop services, etc.
  }

  async enhancedMonitoring(directory) {
    console.log(`Enabling enhanced monitoring for ${directory}`);
    // Implementation would increase monitoring frequency, enable additional logging
  }

  async logViolation(directory, changes) {
    const violation = {
      timestamp: new Date(),
      directory: directory,
      changes: changes,
      severity: changes.length > this.alertThreshold ? 'critical' : 'standard'
    };

    console.log(`INTEGRITY_VIOLATION: ${JSON.stringify(violation)}`);
  }

  async sendCriticalAlert(directory, changes) {
    // Implementation would send critical alert to security team
    console.log(`CRITICAL ALERT: Integrity violation in ${directory}`);
  }

  async sendStandardAlert(directory, changes) {
    // Implementation would send standard alert
    console.log(`ALERT: Integrity changes detected in ${directory}`);
  }
}
```

### Secure Boot Implementation
```javascript
// Secure Boot for Industrial Controllers
class IACSSecureBoot {
  constructor() {
    this.trustedKeys = new Set();
    this.bootSequence = [];
    this.integrityChecks = new Map();
  }

  // Initialize Secure Boot
  async initializeSecureBoot() {
    // Load trusted keys
    await this.loadTrustedKeys();

    // Define boot sequence
    this.defineBootSequence();

    // Setup integrity checks
    this.setupIntegrityChecks();
  }

  // Boot Process
  async performSecureBoot() {
    console.log('Starting secure boot process...');

    for (const component of this.bootSequence) {
      const success = await this.verifyAndLoadComponent(component);
      if (!success) {
        await this.handleBootFailure(component);
        return false;
      }
    }

    console.log('Secure boot completed successfully');
    return true;
  }

  // Component Verification
  async verifyAndLoadComponent(component) {
    try {
      // Verify component signature
      const signatureValid = await this.verifySignature(component);

      // Check component integrity
      const integrityValid = await this.checkIntegrity(component);

      // Verify component dependencies
      const dependenciesValid = await this.verifyDependencies(component);

      if (signatureValid && integrityValid && dependenciesValid) {
        await this.loadComponent(component);
        console.log(`Component ${component.name} loaded successfully`);
        return true;
      } else {
        console.log(`Component ${component.name} verification failed`);
        return false;
      }
    } catch (error) {
      console.error(`Error verifying component ${component.name}: ${error.message}`);
      return false;
    }
  }

  // Signature Verification
  async verifySignature(component) {
    const signature = component.signature;
    const publicKey = this.getPublicKey(component.signer);

    if (!publicKey) {
      console.log(`Unknown signer for component ${component.name}`);
      return false;
    }

    // Implementation would use crypto module for signature verification
    return true; // Placeholder
  }

  // Integrity Check
  async checkIntegrity(component) {
    const expectedHash = component.expectedHash;
    const actualHash = await this.calculateHash(component.path);

    return actualHash === expectedHash;
  }

  // Dependency Verification
  async verifyDependencies(component) {
    if (!component.dependencies) return true;

    for (const dependency of component.dependencies) {
      const depComponent = this.findComponent(dependency);
      if (!depComponent || !depComponent.loaded) {
        console.log(`Missing dependency ${dependency} for ${component.name}`);
        return false;
      }
    }

    return true;
  }

  // Boot Failure Handling
  async handleBootFailure(component) {
    console.log(`Boot failure for component ${component.name}`);

    // Log failure
    await this.logBootFailure(component);

    // Alert security team
    await this.alertSecurityTeam(component);

    // Enter recovery mode
    await this.enterRecoveryMode();
  }

  // Utility Methods
  async loadTrustedKeys() {
    // Load trusted public keys from secure storage
    this.trustedKeys.add('manufacturer-key-1');
    this.trustedKeys.add('oem-key-1');
  }

  defineBootSequence() {
    this.bootSequence = [
      { name: 'bios', path: '/boot/bios.bin', signer: 'manufacturer-key-1' },
      { name: 'bootloader', path: '/boot/bootloader.bin', signer: 'manufacturer-key-1' },
      { name: 'kernel', path: '/boot/kernel.bin', signer: 'oem-key-1' },
      { name: 'initramfs', path: '/boot/initramfs.bin', signer: 'oem-key-1' }
    ];
  }

  setupIntegrityChecks() {
    // Setup runtime integrity checks
    this.integrityChecks.set('kernel', { interval: 60000, action: 'alert' });
    this.integrityChecks.set('critical_processes', { interval: 30000, action: 'restart' });
  }

  getPublicKey(signer) {
    // Return public key for signer
    return this.trustedKeys.has(signer) ? `${signer}_public_key` : null;
  }

  async calculateHash(filePath) {
    // Calculate file hash
    const crypto = require('crypto');
    const fs = require('fs');
    const fileBuffer = fs.readFileSync(filePath);
    return crypto.createHash('sha256').update(fileBuffer).digest('hex');
  }

  findComponent(name) {
    return this.bootSequence.find(comp => comp.name === name);
  }

  async loadComponent(component) {
    // Load component into memory
    component.loaded = true;
  }

  async logBootFailure(component) {
    const failure = {
      timestamp: new Date(),
      component: component.name,
      reason: 'verification_failed'
    };
    console.log(`BOOT_FAILURE: ${JSON.stringify(failure)}`);
  }

  async alertSecurityTeam(component) {
    console.log(`ALERT: Boot failure for ${component.name}`);
  }

  async enterRecoveryMode() {
    console.log('Entering recovery mode...');
    // Implementation would load recovery image, disable compromised components
  }
}
```

## Implementation Checklist

- [ ] File integrity monitoring implemented (SL 2+)
- [ ] Automated integrity checks configured (SL 2+)
- [ ] Change management processes established (SL 2+)
- [ ] Secure boot processes deployed (SL 3+)
- [ ] Memory integrity protection enabled (SL 3+)
- [ ] Runtime integrity monitoring active (SL 3+)
- [ ] Hardware root of trust established (SL 4)
- [ ] TPM integration completed (SL 4)
- [ ] Continuous integrity validation (SL 4)
- [ ] Integrity violation response procedures documented

## Related Standards
- [[../../endpoint-protection|Endpoint Protection]] - Host-based security controls
- [[../../change-management|Change Management]] - Controlled system modifications
- [[../../incident-response|Incident Response]] - Integrity violation handling