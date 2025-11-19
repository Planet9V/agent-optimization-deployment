# FR 2: Use Control (UC)

**Objective:** Control access to resources based on authorization policies.

## Technical Requirements

### SL 1 Requirements
- Basic access control lists (ACLs)
- File system permissions
- Simple authorization checks

### SL 2 Requirements
- Role-based access control (RBAC)
- Group-based permissions
- Access control matrix

### SL 3 Requirements
- Attribute-based access control (ABAC)
- Mandatory access control (MAC) for critical systems
- Access control policy enforcement

### SL 4 Requirements
- Zero trust access control
- Continuous authorization
- Policy-based access control with context awareness

## Implementation Guidelines

### RBAC System Architecture
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

### ABAC Implementation for Industrial Control
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

## Implementation Checklist

- [ ] Basic ACLs implemented (SL 1)
- [ ] RBAC system deployed (SL 2+)
- [ ] Group-based permissions configured (SL 2+)
- [ ] ABAC policies defined (SL 3+)
- [ ] MAC implemented for critical systems (SL 3+)
- [ ] Zero trust access control (SL 4)
- [ ] Continuous authorization monitoring (SL 4)
- [ ] Access control decisions logged
- [ ] Policy enforcement validated
- [ ] Access control matrix maintained

## Related Standards
- [[../../access-control|Access Control]] - Authorization mechanisms
- [[../../identity-management|Identity Management]] - User and device management
- [[../../audit-logging|Audit Logging]] - Access control monitoring