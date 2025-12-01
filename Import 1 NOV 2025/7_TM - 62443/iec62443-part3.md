# IEC 62443-3-3: System Security Requirements and Security Levels

## Overview

IEC 62443-3-3 defines the security requirements for industrial automation and control systems (IACS) based on seven foundational requirements (FR) and seven security levels (SL). This standard provides detailed technical specifications for implementing security controls in industrial environments.

**Related Standards:**
- [[IEC 62443 Part 1]] - Terminology, concepts, and models
- [[IEC 62443 Part 2]] - Security program requirements
- [[IEC 62443 Part 4]] - Secure development lifecycle
- [[Compliance]] - IEC 62443 certification processes

**Implementation Guides:**
- [[Network Design]] - Network segmentation requirements
- [[Identity Management]] - Authentication and access control
- [[Device Management]] - Industrial device security
- [[Endpoint Protection]] - Host-based security controls

## Foundational Requirements (FR)

### FR 1: Identification and Authentication Control (IAC)

**Objective:** Ensure that only authorized entities can access systems and data.

#### Technical Requirements

**SL 1 Requirements:**
- Unique identification for all users
- Password-based authentication
- Basic access control lists

**SL 2 Requirements:**
- Multi-factor authentication for privileged accounts
- Role-based access control (RBAC)
- Account lockout after failed attempts
- Password complexity requirements

**SL 3 Requirements:**
- Certificate-based authentication
- Centralized authentication management
- Session management and timeout
- Audit logging of authentication events

**SL 4 Requirements:**
- Hardware security modules (HSM) for key storage
- Biometric authentication where applicable
- Mutual authentication for critical systems
- Continuous authentication monitoring

#### Implementation Guidelines

##### Authentication Architecture for IACS
```javascript
// IEC 62443 SL 3 Authentication Implementation
const iacImplementation = {
  authenticationMethods: {
    sl1: ['password'],
    sl2: ['password', 'mfa', 'rbac'],
    sl3: ['certificate', 'kerberos', 'oauth'],
    sl4: ['hsm', 'biometric', 'continuous']
  },

  sessionManagement: {
    idleTimeout: 900, // 15 minutes
    absoluteTimeout: 28800, // 8 hours
    concurrentSessions: 3,
    reauthentication: true
  },

  passwordPolicy: {
    minLength: 12,
    complexity: 'mixed_case_numbers_symbols',
    history: 10,
    maxAge: 90,
    lockoutThreshold: 5,
    lockoutDuration: 900
  }
};

// RBAC Implementation
class IEC62443RBAC {
  constructor() {
    this.roles = {
      operator: ['read', 'control'],
      engineer: ['read', 'control', 'configure'],
      administrator: ['read', 'control', 'configure', 'administer'],
      auditor: ['read', 'audit']
    };

    this.permissions = {
      read: 'View system data and status',
      control: 'Operate control systems',
      configure: 'Modify system configuration',
      administer: 'Manage users and security',
      audit: 'View audit logs and reports'
    };
  }

  checkAccess(user, resource, action) {
    const userRole = this.getUserRole(user);
    const rolePermissions = this.roles[userRole];

    if (!rolePermissions || !rolePermissions.includes(action)) {
      this.logAccessDenial(user, resource, action);
      return false;
    }

    this.logAccessGrant(user, resource, action);
    return true;
  }

  getUserRole(user) {
    // Implementation to retrieve user role from directory
    return user.role || 'operator';
  }

  logAccessDenial(user, resource, action) {
    console.log(`Access denied: ${user.id} attempted ${action} on ${resource}`);
  }

  logAccessGrant(user, resource, action) {
    console.log(`Access granted: ${user.id} performed ${action} on ${resource}`);
  }
}
```

##### Certificate-Based Authentication
```javascript
// X.509 Certificate Authentication for Industrial Systems
const certificateAuth = {
  certificateRequirements: {
    keySize: 2048,
    algorithm: 'RSA',
    validityPeriod: 365, // days
    revocationCheck: 'OCSP',
    extendedKeyUsage: ['clientAuth', 'serverAuth']
  },

  certificateAuthority: {
    rootCA: 'Industrial Security CA',
    intermediateCA: 'Zone Intermediate CA',
    crlDistribution: 'http://crl.industrial.local/crl',
    ocspResponder: 'http://ocsp.industrial.local'
  },

  implementation: {
    clientCertificateValidation: async (certificate) => {
      // Validate certificate chain
      const chainValid = await validateCertificateChain(certificate);

      // Check revocation status
      const notRevoked = await checkRevocationStatus(certificate);

      // Verify extended key usage
      const correctUsage = verifyExtendedKeyUsage(certificate);

      return chainValid && notRevoked && correctUsage;
    },

    serverCertificateValidation: async (certificate) => {
      // Server certificate validation logic
      return await validateServerCertificate(certificate);
    }
  }
};
```

### FR 2: Use Control (UC)

**Objective:** Control access to resources based on authorization policies.

#### Technical Requirements

**SL 1 Requirements:**
- Basic access control lists (ACLs)
- File system permissions
- Simple authorization checks

**SL 2 Requirements:**
- Role-based access control (RBAC)
- Group-based permissions
- Access control matrix

**SL 3 Requirements:**
- Attribute-based access control (ABAC)
- Mandatory access control (MAC) for critical systems
- Access control policy enforcement

**SL 4 Requirements:**
- Zero trust access control
- Continuous authorization
- Policy-based access control with context awareness

#### Implementation Guidelines

##### RBAC System Architecture
```javascript
// Comprehensive RBAC Implementation for IACS
class IACSRBAC {
  constructor() {
    this.users = new Map();
    this.roles = new Map();
    this.permissions = new Map();
    this.roleAssignments = new Map();
    this.permissionAssignments = new Map();
  }

  // User Management
  addUser(userId, attributes) {
    this.users.set(userId, {
      id: userId,
      attributes: attributes,
      active: true,
      lastLogin: null
    });
  }

  // Role Management
  createRole(roleId, description, permissions) {
    this.roles.set(roleId, {
      id: roleId,
      description: description,
      permissions: new Set(permissions),
      active: true
    });
  }

  // Permission Management
  definePermission(permissionId, resource, action, description) {
    this.permissions.set(permissionId, {
      id: permissionId,
      resource: resource,
      action: action,
      description: description
    });
  }

  // Role Assignment
  assignRoleToUser(userId, roleId) {
    if (!this.roleAssignments.has(userId)) {
      this.roleAssignments.set(userId, new Set());
    }
    this.roleAssignments.get(userId).add(roleId);
  }

  // Permission Assignment to Roles
  assignPermissionToRole(permissionId, roleId) {
    if (!this.permissionAssignments.has(roleId)) {
      this.permissionAssignments.set(roleId, new Set());
    }
    this.permissionAssignments.get(roleId).add(permissionId);
  }

  // Access Control Decision
  checkAccess(userId, resource, action) {
    const userRoles = this.roleAssignments.get(userId) || new Set();

    for (const roleId of userRoles) {
      const role = this.roles.get(roleId);
      if (role && role.active) {
        for (const permissionId of role.permissions) {
          const permission = this.permissions.get(permissionId);
          if (permission &&
              permission.resource === resource &&
              permission.action === action) {
            this.logAccess(userId, resource, action, 'granted');
            return true;
          }
        }
      }
    }

    this.logAccess(userId, resource, action, 'denied');
    return false;
  }

  // Audit Logging
  logAccess(userId, resource, action, result) {
    const logEntry = {
      timestamp: new Date(),
      userId: userId,
      resource: resource,
      action: action,
      result: result,
      userAgent: 'IACS Control System',
      ipAddress: '192.168.1.100'
    };

    // Write to audit log
    this.writeAuditLog(logEntry);
  }

  writeAuditLog(entry) {
    console.log(`AUDIT: ${JSON.stringify(entry)}`);
    // Implementation would write to secure audit log
  }
}
```

##### ABAC Implementation for Industrial Control
```javascript
// Attribute-Based Access Control for IACS
class IACSABAC {
  constructor() {
    this.policies = new Map();
    this.attributes = new Map();
  }

  // Policy Definition
  definePolicy(policyId, conditions, effect) {
    this.policies.set(policyId, {
      id: policyId,
      conditions: conditions,
      effect: effect, // 'allow' or 'deny'
      active: true
    });
  }

  // Attribute Management
  setUserAttributes(userId, attributes) {
    this.attributes.set(`user:${userId}`, attributes);
  }

  setResourceAttributes(resourceId, attributes) {
    this.attributes.set(`resource:${resourceId}`, attributes);
  }

  setEnvironmentAttributes(attributes) {
    this.attributes.set('environment', attributes);
  }

  // Access Control Decision
  evaluateAccess(userId, resourceId, action, context = {}) {
    const userAttrs = this.attributes.get(`user:${userId}`) || {};
    const resourceAttrs = this.attributes.get(`resource:${resourceId}`) || {};
    const envAttrs = this.attributes.get('environment') || {};

    const requestContext = {
      user: userAttrs,
      resource: resourceAttrs,
      environment: envAttrs,
      action: action,
      context: context
    };

    // Evaluate all policies
    for (const [policyId, policy] of this.policies) {
      if (policy.active && this.evaluatePolicy(policy, requestContext)) {
        this.logDecision(policyId, requestContext, policy.effect);
        return policy.effect === 'allow';
      }
    }

    // Default deny
    this.logDecision('default', requestContext, 'deny');
    return false;
  }

  // Policy Evaluation
  evaluatePolicy(policy, context) {
    for (const condition of policy.conditions) {
      if (!this.evaluateCondition(condition, context)) {
        return false;
      }
    }
    return true;
  }

  // Condition Evaluation
  evaluateCondition(condition, context) {
    const { attribute, operator, value } = condition;
    const actualValue = this.getNestedValue(context, attribute);

    switch (operator) {
      case 'equals':
        return actualValue === value;
      case 'not_equals':
        return actualValue !== value;
      case 'contains':
        return Array.isArray(actualValue) && actualValue.includes(value);
      case 'in':
        return Array.isArray(value) && value.includes(actualValue);
      case 'greater_than':
        return actualValue > value;
      case 'less_than':
        return actualValue < value;
      case 'regex':
        return new RegExp(value).test(actualValue);
      default:
        return false;
    }
  }

  getNestedValue(obj, path) {
    return path.split('.').reduce((current, key) => current?.[key], obj);
  }

  logDecision(policyId, context, decision) {
    const logEntry = {
      timestamp: new Date(),
      policyId: policyId,
      userId: context.user.id,
      resourceId: context.resource.id,
      action: context.action,
      decision: decision,
      attributes: context
    };

    console.log(`ABAC_DECISION: ${JSON.stringify(logEntry)}`);
  }
}

// Example ABAC Policies for IACS
const abacPolicies = [
  {
    id: 'operator_control_access',
    conditions: [
      { attribute: 'user.role', operator: 'equals', value: 'operator' },
      { attribute: 'user.clearance_level', operator: 'greater_than', value: 1 },
      { attribute: 'resource.zone', operator: 'equals', value: 'zone1' },
      { attribute: 'environment.time_of_day', operator: 'in', value: ['06:00', '18:00'] },
      { attribute: 'action', operator: 'equals', value: 'control' }
    ],
    effect: 'allow'
  },
  {
    id: 'maintenance_window_access',
    conditions: [
      { attribute: 'user.department', operator: 'equals', value: 'maintenance' },
      { attribute: 'environment.maintenance_window', operator: 'equals', value: true },
      { attribute: 'resource.criticality', operator: 'less_than', value: 8 }
    ],
    effect: 'allow'
  }
];
```

### FR 3: System Integrity (SI)

**Objective:** Protect system components from unauthorized modification.

#### Technical Requirements

**SL 1 Requirements:**
- Basic file integrity checks
- Simple change detection
- Manual integrity verification

**SL 2 Requirements:**
- Automated integrity monitoring
- File integrity monitoring (FIM)
- Change management processes

**SL 3 Requirements:**
- Secure boot processes
- Memory integrity protection
- Runtime integrity monitoring

**SL 4 Requirements:**
- Hardware root of trust
- Trusted platform modules (TPM)
- Continuous integrity validation

#### Implementation Guidelines

##### File Integrity Monitoring System
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

##### Secure Boot Implementation
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

### FR 4: Data Confidentiality (DC)

**Objective:** Protect sensitive data from unauthorized disclosure.

#### Technical Requirements

**SL 1 Requirements:**
- Basic data classification
- Simple encryption for stored data
- Manual data handling procedures

**SL 2 Requirements:**
- Data encryption at rest
- Secure data transmission
- Access controls for sensitive data

**SL 3 Requirements:**
- End-to-end encryption
- Key management systems
- Data loss prevention (DLP)

**SL 4 Requirements:**
- Quantum-resistant encryption
- Hardware security modules
- Continuous data protection

#### Implementation Guidelines

##### Data Encryption Architecture
```javascript
// Data Encryption Implementation for IACS
class IACSDataEncryption {
  constructor() {
    this.encryptionAlgorithms = {
      aes256: 'aes-256-gcm',
      chacha20: 'chacha20-poly1305'
    };
    this.keyManagement = new KeyManager();
    this.dataClassification = new DataClassifier();
  }

  // Encrypt Data
  async encryptData(data, classification, context = {}) {
    // Determine encryption requirements
    const requirements = this.getEncryptionRequirements(classification);

    // Generate or retrieve key
    const key = await this.keyManagement.getKey(requirements.keyType, context);

    // Select algorithm
    const algorithm = this.selectAlgorithm(requirements, data.length);

    // Encrypt data
    const encrypted = await this.performEncryption(data, key, algorithm);

    // Add metadata
    const metadata = {
      algorithm: algorithm,
      keyId: key.id,
      classification: classification,
      timestamp: new Date(),
      integrity: await this.calculateIntegrityHash(encrypted)
    };

    return {
      encrypted: encrypted,
      metadata: metadata
    };
  }

  // Decrypt Data
  async decryptData(encryptedPackage, context = {}) {
    const { encrypted, metadata } = encryptedPackage;

    // Verify integrity
    const currentHash = await this.calculateIntegrityHash(encrypted);
    if (currentHash !== metadata.integrity) {
      throw new Error('Data integrity violation');
    }

    // Retrieve key
    const key = await this.keyManagement.getKeyById(metadata.keyId, context);

    // Decrypt data
    const decrypted = await this.performDecryption(encrypted, key, metadata.algorithm);

    // Log access
    await this.logDataAccess(metadata, context, 'decrypt');

    return decrypted;
  }

  // Encryption Requirements by Classification
  getEncryptionRequirements(classification) {
    const requirements = {
      'public': { algorithm: 'none', keyType: 'none' },
      'internal': { algorithm: 'aes256', keyType: 'shared' },
      'confidential': { algorithm: 'aes256', keyType: 'user' },
      'restricted': { algorithm: 'aes256', keyType: 'hsm' },
      'critical': { algorithm: 'chacha20', keyType: 'hsm' }
    };

    return requirements[classification] || requirements['internal'];
  }

  // Algorithm Selection
  selectAlgorithm(requirements, dataSize) {
    if (requirements.algorithm !== 'auto') {
      return this.encryptionAlgorithms[requirements.algorithm];
    }

    // Auto-select based on data size and performance
    return dataSize > 1024 * 1024 ?
      this.encryptionAlgorithms.aes256 :
      this.encryptionAlgorithms.chacha20;
  }

  // Perform Encryption
  async performEncryption(data, key, algorithm) {
    const crypto = require('crypto');

    if (algorithm === 'aes-256-gcm') {
      const iv = crypto.randomBytes(16);
      const cipher = crypto.createCipher(algorithm, key.value);
      cipher.setAAD(Buffer.from('IACS Data'));
      let encrypted = cipher.update(data, 'utf8', 'hex');
      encrypted += cipher.final('hex');
      const authTag = cipher.getAuthTag();

      return {
        data: encrypted,
        iv: iv.toString('hex'),
        authTag: authTag.toString('hex')
      };
    }

    // Implementation for other algorithms
    return { data: 'encrypted_data' };
  }

  // Perform Decryption
  async performDecryption(encrypted, key, algorithm) {
    // Implementation would reverse encryption process
    return 'decrypted_data';
  }

  // Integrity Hash Calculation
  async calculateIntegrityHash(data) {
    const crypto = require('crypto');
    return crypto.createHash('sha256').update(data).digest('hex');
  }

  // Audit Logging
  async logDataAccess(metadata, context, action) {
    const logEntry = {
      timestamp: new Date(),
      action: action,
      classification: metadata.classification,
      user: context.userId,
      resource: context.resourceId,
      keyId: metadata.keyId
    };

    console.log(`DATA_ACCESS: ${JSON.stringify(logEntry)}`);
  }
}

// Key Management System
class KeyManager {
  constructor() {
    this.keys = new Map();
    this.hsm = new HardwareSecurityModule();
  }

  async getKey(keyType, context) {
    switch (keyType) {
      case 'shared':
        return this.getSharedKey();
      case 'user':
        return this.getUserKey(context.userId);
      case 'hsm':
        return this.getHSMKey(context);
      default:
        throw new Error(`Unknown key type: ${keyType}`);
    }
  }

  async getKeyById(keyId, context) {
    const key = this.keys.get(keyId);
    if (!key) {
      throw new Error(`Key not found: ${keyId}`);
    }

    // Verify access permissions
    await this.verifyKeyAccess(key, context);

    return key;
  }

  getSharedKey() {
    // Return shared encryption key
    return { id: 'shared-key-1', value: 'shared-key-value' };
  }

  getUserKey(userId) {
    // Return user-specific key
    return { id: `user-key-${userId}`, value: `user-key-${userId}` };
  }

  async getHSMKey(context) {
    // Retrieve key from HSM
    return await this.hsm.getKey(context.resourceId);
  }

  async verifyKeyAccess(key, context) {
    // Implementation would check user permissions for key access
    return true;
  }
}

// Hardware Security Module Interface
class HardwareSecurityModule {
  async getKey(resourceId) {
    // Implementation would interface with actual HSM
    return { id: `hsm-key-${resourceId}`, value: 'hsm-protected-key' };
  }
}

// Data Classification Engine
class DataClassifier {
  classifyData(data, context) {
    // Implementation would analyze data content and context
    // to determine appropriate classification
    return 'confidential'; // Default classification
  }
}
```

### FR 5: Restricted Data Flow (RDF)

**Objective:** Control data flow within and between zones.

#### Technical Requirements

**SL 1 Requirements:**
- Basic network segmentation
- Simple firewall rules
- Manual traffic monitoring

**SL 2 Requirements:**
- Zone and conduit implementation
- Access control between zones
- Traffic filtering and inspection

**SL 3 Requirements:**
- Advanced network segmentation
- Deep packet inspection
- Automated traffic enforcement

**SL 4 Requirements:**
- Micro-segmentation
- Zero trust networking
- Continuous traffic monitoring

#### Implementation Guidelines

##### Network Segmentation Architecture
```javascript
// Network Segmentation Implementation for IACS
class IACSNetworkSegmentation {
  constructor() {
    this.zones = new Map();
    this.conduits = new Map();
    this.firewall = new FirewallEngine();
    this.monitoring = new TrafficMonitor();
  }

  // Define Zones
  defineZone(zoneId, attributes) {
    this.zones.set(zoneId, {
      id: zoneId,
      name: attributes.name,
      securityLevel: attributes.securityLevel,
      assets: new Set(),
      conduits: new Set(),
      policies: attributes.policies || []
    });
  }

  // Define Conduits
  defineConduit(conduitId, sourceZone, targetZone, attributes) {
    const conduit = {
      id: conduitId,
      sourceZone: sourceZone,
      targetZone: targetZone,
      protocol: attributes.protocol,
      ports: attributes.ports,
      securityControls: attributes.securityControls,
      monitoringEnabled: attributes.monitoringEnabled,
      active: true
    };

    this.conduits.set(conduitId, conduit);

    // Add conduit to zones
    this.zones.get(sourceZone).conduits.add(conduitId);
    this.zones.get(targetZone).conduits.add(conduitId);
  }

  // Assign Asset to Zone
  assignAssetToZone(assetId, zoneId) {
    if (!this.zones.has(zoneId)) {
      throw new Error(`Zone not found: ${zoneId}`);
    }

    this.zones.get(zoneId).assets.add(assetId);
  }

  // Enforce Data Flow Policies
  async enforceDataFlow(sourceAsset, targetAsset, protocol, port, data) {
    // Determine source and target zones
    const sourceZone = this.findAssetZone(sourceAsset);
    const targetZone = this.findAssetZone(targetAsset);

    if (!sourceZone || !targetZone) {
      await this.logUnauthorizedAccess(sourceAsset, targetAsset, protocol, port);
      return false;
    }

    // Check if conduit exists
    const conduit = this.findConduit(sourceZone, targetZone);
    if (!conduit) {
      await this.logUnauthorizedAccess(sourceAsset, targetAsset, protocol, port);
      return false;
    }

    // Validate protocol and port
    if (!this.validateConduitAccess(conduit, protocol, port)) {
      await this.logUnauthorizedAccess(sourceAsset, targetAsset, protocol, port);
      return false;
    }

    // Apply security controls
    const securityResult = await this.applySecurityControls(conduit, data);
    if (!securityResult.allowed) {
      await this.logSecurityViolation(conduit, securityResult.reason);
      return false;
    }

    // Monitor traffic
    await this.monitoring.logTraffic(conduit, sourceAsset, targetAsset, protocol, port, data.length);

    return true;
  }

  // Find Asset Zone
  findAssetZone(assetId) {
    for (const [zoneId, zone] of this.zones) {
      if (zone.assets.has(assetId)) {
        return zoneId;
      }
    }
    return null;
  }

  // Find Conduit Between Zones
  findConduit(sourceZone, targetZone) {
    for (const [conduitId, conduit] of this.conduits) {
      if (conduit.sourceZone === sourceZone && conduit.targetZone === targetZone) {
        return conduit;
      }
    }
    return null;
  }

  // Validate Conduit Access
  validateConduitAccess(conduit, protocol, port) {
    // Check protocol
    if (conduit.protocol !== 'any' && conduit.protocol !== protocol) {
      return false;
    }

    // Check port
    if (conduit.ports !== 'any' && !conduit.ports.includes(port)) {
      return false;
    }

    return true;
  }

  // Apply Security Controls
  async applySecurityControls(conduit, data) {
    for (const control of conduit.securityControls) {
      const result = await this.firewall.applyControl(control, data);
      if (!result.allowed) {
        return { allowed: false, reason: result.reason };
      }
    }

    return { allowed: true };
  }

  // Logging Methods
  async logUnauthorizedAccess(sourceAsset, targetAsset, protocol, port) {
    const logEntry = {
      timestamp: new Date(),
      type: 'unauthorized_access',
      sourceAsset: sourceAsset,
      targetAsset: targetAsset,
      protocol: protocol,
      port: port,
      action: 'blocked'
    };

    console.log(`NETWORK_VIOLATION: ${JSON.stringify(logEntry)}`);
  }

  async logSecurityViolation(conduit, reason) {
    const logEntry = {
      timestamp: new Date(),
      type: 'security_violation',
      conduit: conduit.id,
      reason: reason,
      action: 'blocked'
    };

    console.log(`SECURITY_VIOLATION: ${JSON.stringify(logEntry)}`);
  }
}

// Firewall Engine
class FirewallEngine {
  async applyControl(control, data) {
    switch (control.type) {
      case 'signature':
        return await this.checkSignature(control.signature, data);
      case 'anomaly':
        return await this.checkAnomaly(control.baseline, data);
      case 'content':
        return await this.checkContent(control.pattern, data);
      default:
        return { allowed: true };
    }
  }

  async checkSignature(signature, data) {
    // Implementation would check for known malicious signatures
    return { allowed: !data.includes(signature), reason: 'signature_match' };
  }

  async checkAnomaly(baseline, data) {
    // Implementation would check for anomalous patterns
    return { allowed: true }; // Placeholder
  }

  async checkContent(pattern, data) {
    // Implementation would check for prohibited content
    return { allowed: !new RegExp(pattern).test(data), reason: 'content_match' };
  }
}

// Traffic Monitoring
class TrafficMonitor {
  async logTraffic(conduit, sourceAsset, targetAsset, protocol, port, dataSize) {
    const logEntry = {
      timestamp: new Date(),
      conduit: conduit,
      sourceAsset: sourceAsset,
      targetAsset: targetAsset,
      protocol: protocol,
      port: port,
      dataSize: dataSize
    };

    console.log(`TRAFFIC_LOG: ${JSON.stringify(logEntry)}`);
  }
}
```

### FR 6: Timely Response to Events (TRE)

**Objective:** Detect and respond to security events.

#### Technical Requirements

**SL 1 Requirements:**
- Basic event logging
- Manual event review
- Simple alerting

**SL 2 Requirements:**
- Automated event monitoring
- Security information and event management (SIEM)
- Incident response procedures

**SL 3 Requirements:**
- Real-time event correlation
- Automated incident response
- Advanced threat detection

**SL 4 Requirements:**
- Predictive threat detection
- Automated orchestration and response (SOAR)
- Continuous security monitoring

#### Implementation Guidelines

##### SIEM Implementation for IACS
```javascript
// SIEM Implementation for Industrial Control Systems
class IACSSecurityInformationEventManagement {
  constructor() {
    this.eventSources = new Map();
    this.correlationRules = new Map();
    this.incidentResponse = new IncidentResponseEngine();
    this.alerting = new AlertingEngine();
    this.reporting = new ReportingEngine();
  }

  // Register Event Source
  registerEventSource(sourceId, sourceConfig) {
    this.eventSources.set(sourceId, {
      id: sourceId,
      type: sourceConfig.type,
      format: sourceConfig.format,
      collectionMethod: sourceConfig.collectionMethod,
      active: true
    });
  }

  // Collect Events
  async collectEvents() {
    const allEvents = [];

    for (const [sourceId, source] of this.eventSources) {
      if (source.active) {
        const events = await this.collectFromSource(source);
        allEvents.push(...events);
      }
    }

    return allEvents;
  }

  // Collect from Specific Source
  async collectFromSource(source) {
    switch (source.collectionMethod) {
      case 'syslog':
        return await this.collectSyslogEvents(source);
      case 'api':
        return await this.collectAPIEvents(source);
      case 'file':
        return await this.collectFileEvents(source);
      case 'database':
        return await this.collectDatabaseEvents(source);
      default:
        return [];
    }
  }

  // Event Processing Pipeline
  async processEvents(events) {
    // Normalize events
    const normalizedEvents = events.map(event => this.normalizeEvent(event));

    // Correlate events
    const correlatedEvents = await this.correlateEvents(normalizedEvents);

    // Detect incidents
    const incidents = await this.detectIncidents(correlatedEvents);

    // Respond to incidents
    for (const incident of incidents) {
      await this.incidentResponse.respond(incident);
    }

    // Generate alerts
    const alerts = incidents.filter(incident => incident.severity >= 7);
    for (const alert of alerts) {
      await this.alerting.sendAlert(alert);
    }

    // Store events
    await this.storeEvents(normalizedEvents);
  }

  // Event Normalization
  normalizeEvent(event) {
    return {
      id: this.generateEventId(),
      timestamp: event.timestamp || new Date(),
      source: event.source,
      type: this.mapEventType(event),
      severity: this.mapSeverity(event),
      category: this.categorizeEvent(event),
      details: event.details,
      raw: event
    };
  }

  // Event Correlation
  async correlateEvents(events) {
    const correlated = [];

    for (const rule of this.correlationRules.values()) {
      const matches = await this.applyCorrelationRule(rule, events);
      if (matches.length > 0) {
        correlated.push({
          rule: rule.id,
          events: matches,
          correlationType: rule.type,
          confidence: this.calculateConfidence(matches)
        });
      }
    }

    return correlated;
  }

  // Incident Detection
  async detectIncidents(correlatedEvents) {
    const incidents = [];

    for (const correlation of correlatedEvents) {
      if (this.isIncident(correlation)) {
        incidents.push({
          id: this.generateIncidentId(),
          type: this.determineIncidentType(correlation),
          severity: this.calculateIncidentSeverity(correlation),
          events: correlation.events,
          status: 'new',
          created: new Date(),
          assigned: null
        });
      }
    }

    return incidents;
  }

  // Utility Methods
  generateEventId() {
    return `evt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  generateIncidentId() {
    return `inc_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  mapEventType(event) {
    // Map raw event to standardized type
    const typeMappings = {
      'login': 'authentication',
      'file_access': 'access',
      'network_traffic': 'network',
      'process_start': 'process'
    };

    return typeMappings[event.type] || 'unknown';
  }

  mapSeverity(event) {
    // Map to 1-10 scale
    const severityMappings = {
      'low': 3,
      'medium': 5,
      'high': 7,
      'critical': 9
    };

    return severityMappings[event.severity] || 5;
  }

  categorizeEvent(event) {
    // Categorize by security domain
    if (event.type === 'authentication') return 'access';
    if (event.type === 'network') return 'network';
    if (event.type === 'file') return 'data';
    return 'system';
  }

  applyCorrelationRule(rule, events) {
    // Implementation would apply correlation logic
    return events.filter(event => this.matchesRule(event, rule));
  }

  matchesRule(event, rule) {
    // Check if event matches correlation rule criteria
    return rule.conditions.every(condition =>
      this.evaluateCondition(event, condition)
    );
  }

  evaluateCondition(event, condition) {
    // Evaluate correlation condition
    const value = this.getEventValue(event, condition.field);
    return this.compareValues(value, condition.operator, condition.value);
  }

  getEventValue(event, field) {
    return field.split('.').reduce((obj, key) => obj?.[key], event);
  }

  compareValues(actual, operator, expected) {
    switch (operator) {
      case 'equals': return actual === expected;
      case 'contains': return actual?.includes(expected);
      case 'greater': return actual > expected;
      case 'less': return actual < expected;
      default: return false;
    }
  }

  calculateConfidence(matches) {
    // Calculate correlation confidence
    return Math.min(matches.length * 0.2, 1.0);
  }

  isIncident(correlation) {
    // Determine if correlation represents an incident
    return correlation.confidence > 0.7 &&
           correlation.events.some(event => event.severity >= 7);
  }

  determineIncidentType(correlation) {
    // Determine incident type based on events
    const types = correlation.events.map(event => event.category);
    const primaryType = types[0]; // Simplified
    return primaryType;
  }

  calculateIncidentSeverity(correlation) {
    // Calculate incident severity
    const maxEventSeverity = Math.max(...correlation.events.map(e => e.severity));
    return Math.min(maxEventSeverity + 1, 10);
  }

  async storeEvents(events) {
    // Implementation would store events in database
    console.log(`Stored ${events.length} events`);
  }

  // Collection Methods
  async collectSyslogEvents(source) {
    // Implementation would collect from syslog
    return [];
  }

  async collectAPIEvents(source) {
    // Implementation would collect from API
    return [];
  }

  async collectFileEvents(source) {
    // Implementation would parse log files
    return [];
  }

  async collectDatabaseEvents(source) {
    // Implementation would query databases
    return [];
  }
}

// Incident Response Engine
class IncidentResponseEngine {
  async respond(incident) {
    console.log(`Responding to incident ${incident.id}: ${incident.type}`);

    // Determine response plan
    const responsePlan = this.getResponsePlan(incident.type);

    // Execute response steps
    for (const step of responsePlan.steps) {
      await this.executeResponseStep(step, incident);
    }

    // Update incident status
    incident.status = 'responding';
    incident.respondedAt = new Date();
  }

  getResponsePlan(incidentType) {
    // Return appropriate response plan
    const plans = {
      'access': {
        steps: [
          'isolate_affected_system',
          'preserve_evidence',
          'notify_security_team',
          'assess_impact'
        ]
      },
      'network': {
        steps: [
          'block_malicious_traffic',
          'isolate_affected_segment',
          'analyze_traffic_patterns',
          'implement_additional_monitoring'
        ]
      }
    };

    return plans[incidentType] || { steps: ['investigate', 'contain', 'recover'] };
  }

  async executeResponseStep(step, incident) {
    console.log(`Executing response step: ${step} for incident ${incident.id}`);

    // Implementation would execute specific response actions
    switch (step) {
      case 'isolate_affected_system':
        await this.isolateSystem(incident);
        break;
      case 'preserve_evidence':
        await this.preserveEvidence(incident);
        break;
      case 'notify_security_team':
        await this.notifySecurityTeam(incident);
        break;
    }
  }

  async isolateSystem(incident) {
    // Implementation would isolate affected systems
    console.log(`Isolating systems for incident ${incident.id}`);
  }

  async preserveEvidence(incident) {
    // Implementation would preserve evidence
    console.log(`Preserving evidence for incident ${incident.id}`);
  }

  async notifySecurityTeam(incident) {
    // Implementation would send notifications
    console.log(`Notifying security team about incident ${incident.id}`);
  }
}

// Alerting Engine
class AlertingEngine {
  async sendAlert(alert) {
    console.log(`Sending alert for incident ${alert.id}: ${alert.type}`);

    // Implementation would send alerts via email, SMS, etc.
  }
}

// Reporting Engine
class ReportingEngine {
  async generateReport(timeframe) {
    // Implementation would generate security reports
    console.log(`Generating security report for ${timeframe}`);
  }
}
```

### FR 7: Resource Availability (RA)

**Objective:** Ensure system availability for authorized users.

#### Technical Requirements

**SL 1 Requirements:**
- Basic system monitoring
- Manual capacity planning
- Simple backup procedures

**SL 2 Requirements:**
- Automated monitoring
- Redundancy planning
- Backup and recovery procedures

**SL 3 Requirements:**
- High availability systems
- Automated failover
- Disaster recovery planning

**SL 4 Requirements:**
- Continuous availability
- Advanced redundancy
- Comprehensive disaster recovery

#### Implementation Guidelines

##### High Availability Architecture
```javascript
// High Availability Implementation for IACS
class IACSHighAvailability {
  constructor() {
    this.nodes = new Map();
    this.services = new Map();
    this.monitoring = new HealthMonitor();
    this.failover = new FailoverManager();
    this.loadBalancer = new LoadBalancer();
  }

  // Register Node
  registerNode(nodeId, nodeConfig) {
    this.nodes.set(nodeId, {
      id: nodeId,
      ip: nodeConfig.ip,
      role: nodeConfig.role,
      status: 'unknown',
      lastHeartbeat: null,
      services: new Set(nodeConfig.services)
    });
  }

  // Register Service
  registerService(serviceId, serviceConfig) {
    this.services.set(serviceId, {
      id: serviceId,
      type: serviceConfig.type,
      nodes: new Set(serviceConfig.nodes),
      activeNode: null,
      status: 'stopped',
      healthChecks: serviceConfig.healthChecks
    });
  }

  // Start High Availability
  async startHA() {
    console.log('Starting IACS High Availability system...');

    // Start monitoring
    await this.monitoring.startMonitoring();

    // Initialize services
    for (const [serviceId, service] of this.services) {
      await this.initializeService(service);
    }

    // Start failover management
    await this.failover.startFailoverManagement();

    // Start load balancing
    await this.loadBalancer.startLoadBalancing();

    console.log('IACS High Availability system started');
  }

  // Initialize Service
  async initializeService(service) {
    // Find available nodes for service
    const availableNodes = Array.from(service.nodes)
      .map(nodeId => this.nodes.get(nodeId))
      .filter(node => node.status === 'healthy');

    if (availableNodes.length === 0) {
      console.error(`No healthy nodes available for service ${service.id}`);
      return;
    }

    // Select primary node
    const primaryNode = this.selectPrimaryNode(availableNodes, service);

    // Start service on primary node
    await this.startServiceOnNode(service, primaryNode);

    service.activeNode = primaryNode.id;
    service.status = 'running';
  }

  // Health Monitoring
  async monitorHealth() {
    for (const [nodeId, node] of this.nodes) {
      const health = await this.monitoring.checkNodeHealth(node);

      if (health.status !== node.status) {
        await this.handleNodeStatusChange(node, health.status);
      }

      node.status = health.status;
      node.lastHeartbeat = new Date();
    }

    // Check service health
    for (const [serviceId, service] of this.services) {
      await this.checkServiceHealth(service);
    }
  }

  // Handle Node Status Change
  async handleNodeStatusChange(node, newStatus) {
    console.log(`Node ${node.id} status changed to ${newStatus}`);

    if (newStatus === 'unhealthy') {
      // Initiate failover for affected services
      for (const serviceId of node.services) {
        const service = this.services.get(serviceId);
        if (service.activeNode === node.id) {
          await this.failover.initiateFailover(service);
        }
      }
    } else if (newStatus === 'healthy') {
      // Node recovered, check if rebalancing needed
      await this.checkRebalancing(node);
    }
  }

  // Check Service Health
  async checkServiceHealth(service) {
    if (!service.activeNode) return;

    const activeNode = this.nodes.get(service.activeNode);
    if (!activeNode || activeNode.status !== 'healthy') return;

    const health = await this.monitoring.checkServiceHealth(service, activeNode);

    if (health.status !== 'healthy') {
      console.log(`Service ${service.id} health check failed`);
      await this.failover.initiateFailover(service);
    }
  }

  // Service Management
  async startServiceOnNode(service, node) {
    console.log(`Starting service ${service.id} on node ${node.id}`);

    // Implementation would start service on node
    // This could involve SSH commands, API calls, etc.
  }

  async stopServiceOnNode(service, node) {
    console.log(`Stopping service ${service.id} on node ${node.id}`);

    // Implementation would stop service on node
  }

  // Node Selection
  selectPrimaryNode(availableNodes, service) {
    // Select node based on load, priority, etc.
    return availableNodes[0]; // Simplified selection
  }

  // Rebalancing Check
  async checkRebalancing(recoveredNode) {
    // Check if services should be moved back to recovered node
    for (const serviceId of recoveredNode.services) {
      const service = this.services.get(serviceId);
      if (service.activeNode !== recoveredNode.id) {
        // Consider rebalancing based on policy
        const shouldRebalance = await this.shouldRebalance(service, recoveredNode);
        if (shouldRebalance) {
          await this.rebalanceService(service, recoveredNode);
        }
      }
    }
  }

  async shouldRebalance(service, targetNode) {
    // Implementation would check rebalancing policy
    return false; // Simplified - no rebalancing
  }

  async rebalanceService(service, targetNode) {
    console.log(`Rebalancing service ${service.id} to node ${targetNode.id}`);

    // Stop service on current node
    const currentNode = this.nodes.get(service.activeNode);
    await this.stopServiceOnNode(service, currentNode);

    // Start service on target node
    await this.startServiceOnNode(service, targetNode);

    service.activeNode = targetNode.id;
  }
}

// Health Monitor
class HealthMonitor {
  async startMonitoring() {
    // Start periodic health checks
    setInterval(() => this.performHealthChecks(), 30000); // Every 30 seconds
  }

  async performHealthChecks() {
    // Implementation would perform health checks on all nodes and services
  }

  async checkNodeHealth(node) {
    try {
      // Ping node
      const pingResult = await this.pingNode(node.ip);

      // Check system resources
      const resources = await this.checkSystemResources(node.ip);

      // Determine health status
      const status = this.determineNodeHealth(pingResult, resources);

      return {
        status: status,
        ping: pingResult,
        resources: resources
      };
    } catch (error) {
      return { status: 'unhealthy', error: error.message };
    }
  }

  async checkServiceHealth(service, node) {
    // Implementation would check service-specific health
    return { status: 'healthy' };
  }

  async pingNode(ip) {
    // Implementation would ping the node
    return { success: true, latency: 10 };
  }

  async checkSystemResources(ip) {
    // Implementation would check CPU, memory, disk
    return { cpu: 45, memory: 60, disk: 70 };
  }

  determineNodeHealth(ping, resources) {
    if (!ping.success) return 'unreachable';
    if (resources.cpu > 90 || resources.memory > 90) return 'overloaded';
    if (resources.disk > 95) return 'storage_full';
    return 'healthy';
  }
}

// Failover Manager
class FailoverManager {
  async startFailoverManagement() {
    // Initialize failover monitoring
  }

  async initiateFailover(service) {
    console.log(`Initiating failover for service ${service.id}`);

    // Find failover target
    const targetNode = await this.findFailoverTarget(service);

    if (!targetNode) {
      console.error(`No failover target available for service ${service.id}`);
      return;
    }

    // Perform failover
    await this.performFailover(service, targetNode);
  }

  async findFailoverTarget(service) {
    // Find healthy node that can run the service
    const availableNodes = Array.from(service.nodes)
      .map(nodeId => this.nodes.get(nodeId))
      .filter(node => node.status === 'healthy' && node.id !== service.activeNode);

    return availableNodes.length > 0 ? availableNodes[0] : null;
  }

  async performFailover(service, targetNode) {
    console.log(`Failing over service ${service.id} to node ${targetNode.id}`);

    // Stop service on failed node (if possible)
    const failedNode = this.nodes.get(service.activeNode);
    if (failedNode && failedNode.status === 'healthy') {
      await this.stopServiceOnNode(service, failedNode);
    }

    // Start service on target node
    await this.startServiceOnNode(service, targetNode);

    service.activeNode = targetNode.id;

    // Notify stakeholders
    await this.notifyFailover(service, targetNode);
  }

  async notifyFailover(service, targetNode) {
    console.log(`Failover completed: ${service.id} now running on ${targetNode.id}`);
  }
}

// Load Balancer
class LoadBalancer {
  async startLoadBalancing() {
    // Initialize load balancing
  }

  async distributeLoad(service, requests) {
    // Implementation would distribute requests across service instances
  }
}
```

## Security Level Requirements

### Security Level 2 (SL 2) Requirements

#### CR 2.1: Secure Communications between Zones
- **Objective:** Protect communications between zones
- **Requirements:**
  - Encryption of data in transit
  - Mutual authentication between zones
  - Secure protocols (TLS 1.3, IPsec)
  - Certificate-based authentication

#### CR 2.2: Malware Protection
- **Objective:** Prevent malware infection
- **Requirements:**
  - Anti-malware software on all systems
  - Regular malware signature updates
  - Automated malware scanning
  - Malware incident response procedures

#### CR 2.3: Secure Update Mechanisms
- **Objective:** Ensure secure software updates
- **Requirements:**
  - Authenticated update channels
  - Update integrity verification
  - Rollback capabilities
  - Update testing procedures

### Security Level 3 (SL 3) Requirements

#### CR 3.1: Enhanced Authentication and Authorization
- **Objective:** Strengthen access controls
- **Requirements:**
  - Multi-factor authentication for privileged access
  - Role-based access control with least privilege
  - Centralized authentication management
  - Session management and monitoring

#### CR 3.2: Intrusion Detection and Prevention
- **Objective:** Detect and prevent intrusions
- **Requirements:**
  - Network intrusion detection systems (NIDS)
  - Host-based intrusion detection systems (HIDS)
  - Security information and event management (SIEM)
  - Automated response capabilities

#### CR 3.3: Security Monitoring and Audit
- **Objective:** Comprehensive security monitoring
- **Requirements:**
  - Centralized logging and monitoring
  - Security event correlation and analysis
  - Audit trail review and analysis
  - Security metrics and reporting

### Security Level 4 (SL 4) Requirements

#### CR 4.1: Advanced Threat Detection
- **Objective:** Detect advanced persistent threats
- **Requirements:**
  - Behavioral analytics and anomaly detection
  - Advanced threat intelligence integration
  - Machine learning-based threat detection
  - Continuous security monitoring

#### CR 4.2: Automated Response Capabilities
- **Objective:** Automated incident response
- **Requirements:**
  - Security orchestration, automation, and response (SOAR)
  - Automated containment and remediation
  - Integration with security tools
  - Response effectiveness measurement

#### CR 4.3: Continuous Security Assessment
- **Objective:** Ongoing security evaluation
- **Requirements:**
  - Continuous vulnerability scanning
  - Configuration compliance monitoring
  - Security control effectiveness assessment
  - Regular security assessments and audits

## Implementation Checklists

### SL 1 Implementation Checklist
- [ ] Unique user identification implemented
- [ ] Basic password authentication configured
- [ ] Simple access control lists defined
- [ ] Basic file permissions set
- [ ] Manual integrity checks performed
- [ ] Simple event logging enabled
- [ ] Basic system monitoring in place

### SL 2 Implementation Checklist
- [ ] Multi-factor authentication for admins
- [ ] Role-based access control implemented
- [ ] Account lockout policies configured
- [ ] Password complexity requirements set
- [ ] Automated integrity monitoring enabled
- [ ] File integrity monitoring deployed
- [ ] Change management processes established
- [ ] Encrypted communications between zones
- [ ] Anti-malware protection installed
- [ ] Secure update mechanisms implemented

### SL 3 Implementation Checklist
- [ ] Certificate-based authentication deployed
- [ ] Centralized authentication management
- [ ] Session management and timeout configured
- [ ] Audit logging of authentication events
- [ ] Attribute-based access control implemented
- [ ] Mandatory access control for critical systems
- [ ] Secure boot processes enabled
- [ ] Runtime integrity monitoring active
- [ ] End-to-end encryption implemented
- [ ] Key management systems deployed
- [ ] Data loss prevention controls
- [ ] Advanced network segmentation
- [ ] Deep packet inspection enabled
- [ ] Real-time event correlation
- [ ] Automated incident response
- [ ] Centralized logging and monitoring
- [ ] Security event correlation and analysis

### SL 4 Implementation Checklist
- [ ] Hardware security modules for key storage
- [ ] Biometric authentication where applicable
- [ ] Mutual authentication for critical systems
- [ ] Continuous authentication monitoring
- [ ] Zero trust access control
- [ ] Continuous authorization
- [ ] Policy-based access control with context
- [ ] Hardware root of trust implemented
- [ ] Trusted platform modules utilized
- [ ] Continuous integrity validation
- [ ] Quantum-resistant encryption algorithms
- [ ] Hardware security modules for encryption
- [ ] Continuous data protection
- [ ] Micro-segmentation implemented
- [ ] Zero trust networking architecture
- [ ] Continuous traffic monitoring
- [ ] Predictive threat detection
- [ ] Automated orchestration and response
- [ ] Continuous security monitoring
- [ ] Advanced threat intelligence integration
- [ ] Machine learning-based threat detection
- [ ] Security orchestration, automation, and response
- [ ] Automated containment and remediation
- [ ] Continuous vulnerability scanning
- [ ] Configuration compliance monitoring
- [ ] Security control effectiveness assessment

## Audit Procedures

### IEC 62443-3-3 Audit Methodology

#### 1. Pre-Audit Preparation
**Objective:** Ensure comprehensive audit coverage

**Activities:**
- Review system architecture and zone design
- Verify security level assignments
- Assess foundational requirements implementation
- Review security level requirements
- Interview system administrators and security personnel

**Deliverables:**
- Audit scope and objectives document
- System architecture review report
- Security requirements mapping
- Interview questionnaires and responses

#### 2. Foundational Requirements Audit
**Objective:** Verify FR implementation across all security levels

**Audit Areas:**
- **FR 1 (IAC):** Authentication and authorization controls
- **FR 2 (UC):** Access control and use restrictions
- **FR 3 (SI):** System integrity protection
- **FR 4 (DC):** Data confidentiality measures
- **FR 5 (RDF):** Data flow control mechanisms
- **FR 6 (TRE):** Event detection and response
- **FR 7 (RA):** Resource availability assurance

**Evidence Collection:**
- Configuration files and settings
- System logs and audit trails
- Security policy documents
- Test results and validation reports

#### 3. Security Level Requirements Audit
**Objective:** Assess SL-specific requirements implementation

**Audit Criteria:**
- **SL 2 Requirements:** Secure communications, malware protection, secure updates
- **SL 3 Requirements:** Enhanced authentication, intrusion detection, security monitoring
- **SL 4 Requirements:** Advanced threat detection, automated response, continuous assessment

**Compliance Verification:**
- Technical control implementation
- Process and procedure effectiveness
- Monitoring and alerting capabilities
- Incident response capabilities

#### 4. System Integration Audit
**Objective:** Verify integrated security control effectiveness

**Review Areas:**
- Security control interactions
- System-wide security posture
- Control effectiveness measurement
- Continuous improvement processes

**Performance Evaluation:**
- Control coverage and effectiveness
- System resilience and response
- Security metrics and KPIs
- Improvement initiative results

## Real-World Implementation Examples

### Manufacturing Control System Security

#### Background
- **Industry:** Automotive manufacturing
- **Systems:** PLCs, SCADA systems, HMIs
- **Target SL:** SL 3 for control systems, SL 2 for enterprise systems

#### IEC 62443-3-3 Implementation
**Zone Architecture:**
- **Zone 0:** Physical processes (sensors, actuators)
- **Zone 1:** Basic control (PLCs, RTUs) - SL 3
- **Zone 2:** Supervisory control (SCADA, HMIs) - SL 3
- **Zone 3:** Enterprise integration - SL 2

**Security Controls:**
- Certificate-based authentication for all control systems
- Role-based access control with least privilege
- Network segmentation with DMZs
- SIEM integration for centralized monitoring
- Automated backup and recovery systems

**Results:**
- **Security Level Achievement:** 95% of systems meet target SL
- **Incident Reduction:** 80% reduction in security incidents
- **Compliance:** Full IEC 62443 certification
- **Operational Continuity:** Zero security-related downtime

### Energy Sector Critical Infrastructure

#### Background
- **Industry:** Electric power generation and distribution
- **Systems:** SCADA, DCS, protection relays
- **Target SL:** SL 4 for critical control systems

#### IEC 62443-3-3 Implementation
**Advanced Security Architecture:**
- Hardware security modules for cryptographic operations
- Zero trust network architecture
- Advanced threat detection with behavioral analytics
- Automated incident response with SOAR platform
- Continuous security monitoring and assessment

**High Availability Design:**
- Redundant control systems with automatic failover
- Geographic distribution of critical components
- Real-time data synchronization
- Disaster recovery with RTO < 5 minutes

**Results:**
- **Security Level Achievement:** SL 4 certification for all critical systems
- **Threat Detection:** 99.9% of attempted intrusions detected
- **Response Time:** Average incident response time < 10 minutes
- **Compliance:** Meets NERC CIP and IEC 62443 requirements
- **Reliability:** 99.999% system availability

### Water Treatment Facility Security

#### Background
- **Industry:** Municipal water treatment
- **Systems:** PLCs, RTUs, monitoring systems
- **Target SL:** SL 2 baseline with SL 3 for critical processes

#### IEC 62443-3-3 Implementation
**Practical Security Measures:**
- Multi-factor authentication for operator access
- Network segmentation between treatment zones
- Automated malware scanning and updates
- Centralized logging and monitoring
- Regular security assessments and penetration testing

**Operational Considerations:**
- 24/7 monitoring with on-call security team
- Change management for system updates
- Backup and recovery procedures
- Incident response coordination with local authorities

**Results:**
- **Security Level Achievement:** SL 3 for critical processes, SL 2 overall
- **Compliance:** Meets EPA and local regulatory requirements
- **Public Safety:** Enhanced protection of public water supply
- **Cost Effectiveness:** Balanced security investment with operational needs

## 📚 References

International Electrotechnical Commission. (2023). *IEC 62443-3-3: Industrial communication networks - Network and system security - Part 3-3: System security requirements and security levels*. IEC.

International Society of Automation. (2022). *ISA/IEC 62443 Cybersecurity Fundamentals*. ISA.

National Institute of Standards and Technology. (2023). *Guide to Operational Technology (OT) Security* (NIST SP 800-82 Rev. 3). U.S. Department of Commerce.

## 🔗 See Also

- [[IEC 62443 Part 1]] - Terminology, concepts, and models
- [[IEC 62443 Part 2]] - Security program requirements
- [[IEC 62443 Part 4]] - Secure development lifecycle
- [[Zone and Conduit Model]] - Network segmentation
- [[Security Levels (SL)]] - Security level definitions
- [[Foundational Requirements (FR)]] - Core security requirements

**Authentication Architecture:**
```json
{
  "authentication_system": {
    "primary_auth": "certificate_based",
    "secondary_auth": "multi_factor",
    "session_management": {
      "timeout": 900,
      "max_sessions": 3,
      "idle_timeout": 300
    },
    "account_policies": {
      "min_length": 12,
      "complexity": "high",
      "history": 10,
      "lockout_threshold": 5
    }
  }
}
```

**n8n Workflow: Authentication Monitoring**
```json
{
  "name": "Authentication Event Monitoring",
  "nodes": [
    {
      "parameters": {
        "functionCode": "const authEvents = $node[\"SIEM Query\"].json.events;\n\nconst failedAttempts = authEvents.filter(event => \n  event.type === 'authentication_failure'\n);\n\nconst suspiciousActivity = failedAttempts.filter(event => \n  event.attempts > 3 && \n  event.time_window < 300000 // 5 minutes\n);\n\nreturn {\n  failed_auth_attempts: failedAttempts.length,\n  suspicious_activity: suspiciousActivity,\n  risk_level: suspiciousActivity.length > 0 ? 'HIGH' : 'LOW'\n};"
      },
      "name": "Analyze Auth Events",
      "type": "n8n-nodes-base.function"
    }
  ]
}
```

### FR 2: Use Control (UC)

**Objective:** Prevent unauthorized use of systems and data.

#### Access Control Models

**Mandatory Access Control (MAC):**
- Security labels and clearances
- No discretion for users to change permissions
- Strict hierarchical access control

**Role-Based Access Control (RBAC):**
- Permissions assigned to roles
- Users assigned to roles
- Principle of least privilege

**Attribute-Based Access Control (ABAC):**
- Dynamic access decisions based on attributes
- Context-aware permissions
- Fine-grained access control

#### Technical Implementation

**RBAC Configuration:**
```json
{
  "rbac_config": {
    "roles": {
      "operator": {
        "permissions": ["read", "start", "stop"],
        "resources": ["production_line_*"],
        "constraints": ["business_hours"]
      },
      "engineer": {
        "permissions": ["read", "write", "configure"],
        "resources": ["all_systems"],
        "constraints": ["change_approval_required"]
      },
      "administrator": {
        "permissions": ["all"],
        "resources": ["all"],
        "constraints": ["dual_authorization"]
      }
    },
    "separation_of_duties": {
      "conflicting_roles": ["operator", "auditor"],
      "dual_control_operations": ["firmware_update", "security_policy_change"]
    }
  }
}
```

### FR 3: System Integrity (SI)

**Objective:** Protect system integrity and prevent unauthorized modifications.

#### Integrity Protection Mechanisms

**File Integrity Monitoring:**
- Cryptographic hashing of critical files
- Real-time change detection
- Automated integrity verification

**Memory Protection:**
- Address space layout randomization (ASLR)
- Data execution prevention (DEP)
- Stack canaries and heap protection

**Firmware Protection:**
- Secure boot processes
- Firmware signing and verification
- Tamper detection mechanisms

#### Implementation Examples

**Integrity Monitoring System:**
```json
{
  "integrity_monitoring": {
    "critical_files": [
      "/etc/passwd",
      "/etc/shadow",
      "/boot/vmlinuz",
      "/usr/bin/sudo"
    ],
    "monitoring_intervals": {
      "high_priority": 300,
      "medium_priority": 3600,
      "low_priority": 86400
    },
    "response_actions": {
      "file_modified": "alert_and_isolate",
      "memory_corruption": "system_shutdown",
      "firmware_tamper": "emergency_lockdown"
    }
  }
}
```

### FR 4: Data Confidentiality (DC)

**Objective:** Protect sensitive data from unauthorized disclosure.

#### Encryption Standards

**Data at Rest:**
- AES-256 encryption for stored data
- Key management and rotation
- Secure key storage (HSM/KMS)

**Data in Transit:**
- TLS 1.3 for network communications
- Perfect forward secrecy
- Certificate pinning

**Data in Use:**
- Memory encryption
- Secure enclaves (Intel SGX, AMD SEV)
- Application-level encryption

#### n8n Workflow: Data Protection Monitoring

```json
{
  "name": "Data Protection Compliance Check",
  "nodes": [
    {
      "parameters": {
        "command": "find /data -type f -exec head -c 10 {} \\; | grep -i 'sensitive\\|confidential' | wc -l"
      },
      "name": "Check Unencrypted Data",
      "type": "n8n-nodes-base.executeCommand"
    },
    {
      "parameters": {
        "functionCode": "const unencryptedFiles = parseInt($node[\"Check Unencrypted Data\"].json.stdout);\n\nconst complianceStatus = unencryptedFiles === 0 ? 'COMPLIANT' : 'NON_COMPLIANT';\n\nreturn {\n  unencrypted_sensitive_files: unencryptedFiles,\n  compliance_status: complianceStatus,\n  remediation_required: unencryptedFiles > 0\n};"
      },
      "name": "Assess Compliance",
      "type": "n8n-nodes-base.function"
    }
  ]
}
```

### FR 5: Restricted Data Flow (RDF)

**Objective:** Control data flow within and between systems.

#### Network Segmentation

**Demilitarized Zones (DMZ):**
- Isolation of internet-facing systems
- Multi-layered security controls
- Controlled data flow between zones

**Micro-Segmentation:**
- East-west traffic control
- Application-aware segmentation
- Zero-trust network access

#### Data Flow Controls

**Mandatory Integrity Controls:**
- Biba integrity model implementation
- Data flow integrity verification
- Trusted data sources validation

### FR 6: Timely Response to Events (TRE)

**Objective:** Ensure timely detection and response to security events.

#### Event Detection and Response

**Security Information and Event Management (SIEM):**
- Real-time event correlation
- Automated alerting and escalation
- Incident response orchestration

**Endpoint Detection and Response (EDR):**
- Behavioral anomaly detection
- Automated threat containment
- Forensic data collection

#### Response Time Requirements

**SL 1:** Hours to days
**SL 2:** Minutes to hours
**SL 3:** Seconds to minutes
**SL 4:** Real-time (sub-second)

### FR 7: Resource Availability (RA)

**Objective:** Ensure system availability and prevent denial of service.

#### Availability Controls

**Redundancy and Resilience:**
- High availability architectures
- Failover mechanisms
- Load balancing and distribution

**Resource Management:**
- CPU and memory limits
- Network bandwidth controls
- Storage quotas and monitoring

**DoS Protection:**
- Rate limiting and throttling
- Traffic shaping
- Anomaly-based detection

## Security Levels (SL) Implementation

### SL 1: Prevention of Unauthorized Access

**Requirements:**
- Basic identification and authentication
- Basic use control
- Basic system integrity protection
- Basic data confidentiality
- Basic restricted data flow
- Basic timely response
- Basic resource availability

### SL 2: Use of Security Features

**Additional Requirements:**
- Enhanced authentication mechanisms
- Enhanced access controls
- Enhanced integrity monitoring
- Enhanced encryption
- Enhanced network segmentation
- Enhanced event detection
- Enhanced availability controls

### SL 3: Systematic Security Management

**Additional Requirements:**
- Centralized security management
- Security policy enforcement
- Comprehensive monitoring and logging
- Advanced threat detection
- Automated response capabilities
- Security assessment and testing

### SL 4: Adaptation and Learning

**Additional Requirements:**
- Adaptive security controls
- Machine learning-based detection
- Advanced persistent threat protection
- Continuous security assessment
- Automated security updates
- Zero-trust architecture

## Implementation Templates

### Security Requirements Specification Template

```markdown
# Security Requirements Specification

## System Overview
- System Name: [Name]
- Security Level: [SL 1-4]
- Criticality Level: [High/Medium/Low]

## Foundational Requirements

### FR 1: Identification and Authentication Control
- Authentication Methods: [List]
- Account Management: [Policies]
- Session Management: [Controls]

### FR 2: Use Control
- Access Control Model: [RBAC/ABAC/MAC]
- Role Definitions: [List]
- Permission Assignments: [Matrix]

### FR 3: System Integrity
- Integrity Monitoring: [Tools/Methods]
- Change Management: [Process]
- Tamper Detection: [Mechanisms]

### FR 4: Data Confidentiality
- Encryption Standards: [Algorithms]
- Key Management: [System]
- Data Classification: [Levels]

### FR 5: Restricted Data Flow
- Network Segmentation: [Architecture]
- Data Flow Controls: [Rules]
- Trust Boundaries: [Definition]

### FR 6: Timely Response to Events
- Detection Capabilities: [Tools]
- Response Times: [SL Requirements]
- Escalation Procedures: [Process]

### FR 7: Resource Availability
- Availability Requirements: [SLA]
- Redundancy Measures: [Architecture]
- DoS Protection: [Controls]
```

## Best Practices

**Implementation Strategy:**
- Start with thorough assessment and risk analysis
- Implement security levels incrementally
- Focus on foundational requirements first
- Establish continuous monitoring and improvement

**Common Challenges:**
- Legacy system integration requires protocol gateways
- Resource constraints demand prioritization
- Skills gaps need training and expert partnerships

## References

IEC 62443-3-3 (2021). *System security requirements and security levels*. API 1164 (2020). NIST SP 800-82 (2014).