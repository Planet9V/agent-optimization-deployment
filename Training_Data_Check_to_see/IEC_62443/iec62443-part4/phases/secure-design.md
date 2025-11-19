# Phase 3: Secure Design

**Objective:** Design security into the system architecture.

## Security Architecture Principles

### Defense in Depth
- **Network Layer:** Firewalls, DMZs, network segmentation
- **Host Layer:** Host-based security controls, endpoint protection
- **Application Layer:** Input validation, secure coding practices
- **Data Layer:** Encryption, data integrity, access controls

### Zero Trust Architecture
- **Never Trust, Always Verify:** Continuous authentication and authorization
- **Micro-Segmentation:** Granular network and application segmentation
- **Least Privilege:** Minimal access rights for all entities
- **Continuous Monitoring:** Real-time security assessment and response

## Secure Design Patterns

### Authentication Patterns
```javascript
// Secure Authentication Design Pattern
class SecureAuthenticationManager {
  constructor() {
    this.authMethods = new Map();
    this.sessionManager = new SessionManager();
    this.auditLogger = new AuditLogger();
  }

  // Register authentication methods
  registerAuthMethod(name, method) {
    this.authMethods.set(name, method);
  }

  // Multi-factor authentication
  async authenticateMFA(userId, factors) {
    const results = [];

    for (const factor of factors) {
      const method = this.authMethods.get(factor.type);
      if (!method) {
        results.push({ factor: factor.type, success: false, error: 'Method not available' });
        continue;
      }

      try {
        const result = await method.authenticate(factor.credentials);
        results.push({
          factor: factor.type,
          success: result.success,
          confidence: result.confidence || 1.0
        });
      } catch (error) {
        results.push({ factor: factor.type, success: false, error: error.message });
      }
    }

    // Calculate overall authentication result
    const successfulFactors = results.filter(r => r.success);
    const totalConfidence = successfulFactors.reduce((sum, r) => sum + r.confidence, 0);
    const averageConfidence = totalConfidence / factors.length;

    const overallSuccess = successfulFactors.length >= factors.length * 0.8 && averageConfidence >= 0.7;

    // Log authentication attempt
    await this.auditLogger.logAuthentication({
      userId: userId,
      factors: results,
      overallSuccess: overallSuccess,
      timestamp: new Date()
    });

    return {
      success: overallSuccess,
      factors: results,
      confidence: averageConfidence
    };
  }

  // Session management
  async createSecureSession(userId, authResult) {
    const sessionId = this.generateSecureSessionId();
    const sessionData = {
      id: sessionId,
      userId: userId,
      created: new Date(),
      lastActivity: new Date(),
      authFactors: authResult.factors,
      ipAddress: this.getClientIP(),
      userAgent: this.getUserAgent(),
      expires: new Date(Date.now() + 8 * 60 * 60 * 1000) // 8 hours
    };

    await this.sessionManager.storeSession(sessionData);

    return {
      sessionId: sessionId,
      expires: sessionData.expires
    };
  }

  // Continuous authentication
  async validateSession(sessionId) {
    const session = await this.sessionManager.getSession(sessionId);
    if (!session) return { valid: false, reason: 'Session not found' };

    // Check expiration
    if (new Date() > session.expires) {
      await this.sessionManager.destroySession(sessionId);
      return { valid: false, reason: 'Session expired' };
    }

    // Check for suspicious activity
    const riskAssessment = await this.assessSessionRisk(session);
    if (riskAssessment.risk > 0.7) {
      await this.handleSuspiciousSession(session, riskAssessment);
      return { valid: false, reason: 'Suspicious activity detected' };
    }

    // Update session activity
    session.lastActivity = new Date();
    await this.sessionManager.updateSession(session);

    return { valid: true, session: session };
  }

  async assessSessionRisk(session) {
    let riskScore = 0;

    // Check IP address change
    const currentIP = this.getClientIP();
    if (currentIP !== session.ipAddress) {
      riskScore += 0.3;
    }

    // Check user agent change
    const currentUA = this.getUserAgent();
    if (currentUA !== session.userAgent) {
      riskScore += 0.2;
    }

    // Check time since last activity
    const timeSinceActivity = Date.now() - session.lastActivity.getTime();
    if (timeSinceActivity > 30 * 60 * 1000) { // 30 minutes
      riskScore += 0.1;
    }

    // Check for concurrent sessions
    const userSessions = await this.sessionManager.getUserSessions(session.userId);
    if (userSessions.length > 3) {
      riskScore += 0.2;
    }

    return {
      risk: Math.min(riskScore, 1.0),
      factors: {
        ipChange: currentIP !== session.ipAddress,
        uaChange: currentUA !== session.userAgent,
        inactivity: timeSinceActivity > 30 * 60 * 1000,
        concurrentSessions: userSessions.length > 3
      }
    };
  }

  async handleSuspiciousSession(session, riskAssessment) {
    // Log suspicious activity
    await this.auditLogger.logSuspiciousActivity({
      sessionId: session.id,
      userId: session.userId,
      riskAssessment: riskAssessment,
      timestamp: new Date()
    });

    // Implement additional verification
    if (riskAssessment.risk > 0.8) {
      // Force re-authentication
      await this.sessionManager.destroySession(session.id);
    } else {
      // Send additional verification challenge
      await this.sendVerificationChallenge(session);
    }
  }

  generateSecureSessionId() {
    return crypto.randomBytes(32).toString('hex');
  }

  getClientIP() {
    // Implementation to get client IP
    return '192.168.1.100';
  }

  getUserAgent() {
    // Implementation to get user agent
    return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36';
  }

  async sendVerificationChallenge(session) {
    // Implementation to send additional verification
    console.log(`Sending verification challenge for session ${session.id}`);
  }
}

// Session Manager
class SessionManager {
  constructor() {
    this.sessions = new Map();
  }

  async storeSession(sessionData) {
    this.sessions.set(sessionData.id, sessionData);
  }

  async getSession(sessionId) {
    return this.sessions.get(sessionId);
  }

  async updateSession(session) {
    this.sessions.set(session.id, session);
  }

  async destroySession(sessionId) {
    this.sessions.delete(sessionId);
  }

  async getUserSessions(userId) {
    return Array.from(this.sessions.values()).filter(s => s.userId === userId);
  }
}

// Audit Logger
class AuditLogger {
  async logAuthentication(authData) {
    console.log('AUTHENTICATION:', JSON.stringify(authData));
  }

  async logSuspiciousActivity(activityData) {
    console.log('SUSPICIOUS_ACTIVITY:', JSON.stringify(activityData));
  }
}
```

### Authorization Patterns
```javascript
// Role-Based Access Control (RBAC) Design Pattern
class RBACAuthorizationManager {
  constructor() {
    this.roles = new Map();
    this.users = new Map();
    this.permissions = new Map();
    this.roleAssignments = new Map();
    this.permissionAssignments = new Map();
  }

  // Role management
  createRole(roleId, description, parentRole = null) {
    this.roles.set(roleId, {
      id: roleId,
      description: description,
      parent: parentRole,
      permissions: new Set(),
      active: true
    });
  }

  // Permission management
  definePermission(permissionId, resource, action, description) {
    this.permissions.set(permissionId, {
      id: permissionId,
      resource: resource,
      action: action,
      description: description
    });
  }

  // Role-permission assignment
  assignPermissionToRole(permissionId, roleId) {
    const role = this.roles.get(roleId);
    const permission = this.permissions.get(permissionId);

    if (role && permission) {
      role.permissions.add(permissionId);
      this.permissionAssignments.set(`${roleId}:${permissionId}`, true);
    }
  }

  // User-role assignment
  assignRoleToUser(userId, roleId) {
    if (!this.roleAssignments.has(userId)) {
      this.roleAssignments.set(userId, new Set());
    }
    this.roleAssignments.get(userId).add(roleId);
  }

  // Access control decision
  checkAccess(userId, resource, action, context = {}) {
    const userRoles = this.roleAssignments.get(userId) || new Set();

    // Get all permissions for user's roles (including inherited)
    const userPermissions = new Set();
    for (const roleId of userRoles) {
      const rolePermissions = this.getRolePermissions(roleId);
      rolePermissions.forEach(p => userPermissions.add(p));
    }

    // Check if any permission allows the action
    for (const permissionId of userPermissions) {
      const permission = this.permissions.get(permissionId);
      if (permission &&
          this.matchesResource(permission.resource, resource) &&
          this.matchesAction(permission.action, action) &&
          this.checkContext(permission, context)) {
        return { allowed: true, permission: permissionId };
      }
    }

    return { allowed: false, reason: 'No matching permission' };
  }

  // Get all permissions for a role (including inherited)
  getRolePermissions(roleId) {
    const permissions = new Set();
    const role = this.roles.get(roleId);

    if (role) {
      // Add direct permissions
      role.permissions.forEach(p => permissions.add(p));

      // Add inherited permissions
      if (role.parent) {
        const parentPermissions = this.getRolePermissions(role.parent);
        parentPermissions.forEach(p => permissions.add(p));
      }
    }

    return permissions;
  }

  // Resource matching (supports wildcards)
  matchesResource(permissionResource, requestedResource) {
    // Simple wildcard matching
    if (permissionResource === '*' || permissionResource === requestedResource) {
      return true;
    }

    // Pattern matching (e.g., "documents/*" matches "documents/123")
    if (permissionResource.includes('*')) {
      const pattern = permissionResource.replace(/\*/g, '.*');
      return new RegExp(`^${pattern}$`).test(requestedResource);
    }

    return false;
  }

  // Action matching
  matchesAction(permissionAction, requestedAction) {
    if (permissionAction === '*' || permissionAction === requestedAction) {
      return true;
    }

    // Support for action hierarchies (e.g., "read" implies "view")
    const actionHierarchy = {
      'manage': ['create', 'read', 'update', 'delete'],
      'write': ['create', 'update', 'delete'],
      'read': ['view']
    };

    const impliedActions = actionHierarchy[permissionAction] || [];
    return impliedActions.includes(requestedAction);
  }

  // Context checking
  checkContext(permission, context) {
    // Implementation for context-aware authorization
    // Could check time of day, location, device type, etc.
    return true; // Simplified
  }

  // Administrative functions
  revokeRoleFromUser(userId, roleId) {
    const userRoles = this.roleAssignments.get(userId);
    if (userRoles) {
      userRoles.delete(roleId);
    }
  }

  revokePermissionFromRole(permissionId, roleId) {
    const role = this.roles.get(roleId);
    if (role) {
      role.permissions.delete(permissionId);
      this.permissionAssignments.delete(`${roleId}:${permissionId}`);
    }
  }

  // Audit and reporting
  getUserPermissions(userId) {
    const userRoles = this.roleAssignments.get(userId) || new Set();
    const permissions = new Set();

    for (const roleId of userRoles) {
      const rolePermissions = this.getRolePermissions(roleId);
      rolePermissions.forEach(p => permissions.add(p));
    }

    return Array.from(permissions).map(p => this.permissions.get(p));
  }

  getRoleUsers(roleId) {
    const users = [];
    for (const [userId, roles] of this.roleAssignments) {
      if (roles.has(roleId)) {
        users.push(userId);
      }
    }
    return users;
  }

  generateAccessReport(userId = null, resource = null) {
    // Generate access report for auditing
    const report = {
      generated: new Date(),
      userId: userId,
      resource: resource,
      permissions: []
    };

    if (userId) {
      report.permissions = this.getUserPermissions(userId);
    } else {
      // Generate system-wide report
      for (const [uid, roles] of this.roleAssignments) {
        report.permissions.push({
          userId: uid,
          roles: Array.from(roles),
          permissions: this.getUserPermissions(uid)
        });
      }
    }

    return report;
  }
}

// Example RBAC Implementation
const rbac = new RBACAuthorizationManager();

// Define permissions
rbac.definePermission('read_documents', 'documents', 'read', 'Read documents');
rbac.definePermission('write_documents', 'documents', 'write', 'Create and modify documents');
rbac.definePermission('manage_users', 'users', 'manage', 'Manage user accounts');

// Define roles
rbac.createRole('viewer', 'Document viewer');
rbac.createRole('editor', 'Document editor');
rbac.createRole('admin', 'System administrator');

// Assign permissions to roles
rbac.assignPermissionToRole('read_documents', 'viewer');
rbac.assignPermissionToRole('read_documents', 'editor');
rbac.assignPermissionToRole('write_documents', 'editor');
rbac.assignPermissionToRole('manage_users', 'admin');

// Assign roles to users
rbac.assignRoleToUser('user1', 'viewer');
rbac.assignRoleToUser('user2', 'editor');
rbac.assignRoleToUser('admin1', 'admin');

// Test access control
console.log('User1 read documents:', rbac.checkAccess('user1', 'documents', 'read'));
console.log('User1 write documents:', rbac.checkAccess('user1', 'documents', 'write'));
console.log('User2 write documents:', rbac.checkAccess('user2', 'documents', 'write'));
console.log('Admin1 manage users:', rbac.checkAccess('admin1', 'users', 'manage'));
```

## Design Checklist

- [ ] Security architecture principles applied (Defense in Depth, Zero Trust)
- [ ] Authentication patterns implemented with MFA support
- [ ] Authorization patterns implemented (RBAC/ABAC)
- [ ] Session management with continuous validation
- [ ] Audit logging for security events
- [ ] Risk assessment for session anomalies
- [ ] Access control decisions logged and auditable
- [ ] Role inheritance and permission hierarchies defined
- [ ] Context-aware authorization implemented
- [ ] Administrative functions for role/permission management

## Related Standards
- [[IEC 62443 Part 3]] - System security requirements
- [[Threat Modeling Techniques]] - Security design methodologies
- [[Identity Management]] - Authentication and authorization frameworks