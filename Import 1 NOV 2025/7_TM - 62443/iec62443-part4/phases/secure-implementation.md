# Phase 4: Secure Implementation

**Objective:** Implement security controls through secure coding practices.

## Secure Coding Standards

### Input Validation
```javascript
// Secure Input Validation Implementation
class InputValidator {
  constructor() {
    this.validationRules = new Map();
    this.sanitizationRules = new Map();
  }

  // Define validation rules
  defineValidationRule(fieldName, rules) {
    this.validationRules.set(fieldName, rules);
  }

  // Define sanitization rules
  defineSanitizationRule(fieldName, sanitizers) {
    this.sanitizationRules.set(fieldName, sanitizers);
  }

  // Validate input
  validateInput(input, context = {}) {
    const errors = [];
    const sanitized = {};

    for (const [fieldName, value] of Object.entries(input)) {
      try {
        // Sanitize first
        const sanitizedValue = this.sanitizeValue(fieldName, value);

        // Then validate
        const validationResult = this.validateField(fieldName, sanitizedValue, context);

        if (!validationResult.valid) {
          errors.push({
            field: fieldName,
            value: value,
            errors: validationResult.errors
          });
        } else {
          sanitized[fieldName] = sanitizedValue;
        }
      } catch (error) {
        errors.push({
          field: fieldName,
          value: value,
          errors: [error.message]
        });
      }
    }

    return {
      valid: errors.length === 0,
      errors: errors,
      sanitized: sanitized
    };
  }

  // Sanitize value
  sanitizeValue(fieldName, value) {
    const sanitizers = this.sanitizationRules.get(fieldName) || [];

    let sanitized = value;

    for (const sanitizer of sanitizers) {
      sanitized = this.applySanitizer(sanitizer, sanitized);
    }

    return sanitized;
  }

  // Apply sanitizer
  applySanitizer(sanitizer, value) {
    switch (sanitizer.type) {
      case 'trim':
        return value.trim();
      case 'lowercase':
        return value.toLowerCase();
      case 'uppercase':
        return value.toUpperCase();
      case 'remove_html':
        return value.replace(/<[^>]*>/g, '');
      case 'escape_sql':
        return value.replace(/['";\\]/g, '\\$&');
      case 'alphanumeric_only':
        return value.replace(/[^a-zA-Z0-9]/g, '');
      case 'email_normalize':
        return value.toLowerCase().trim();
      default:
        return value;
    }
  }

  // Validate field
  validateField(fieldName, value, context) {
    const rules = this.validationRules.get(fieldName) || [];
    const errors = [];

    for (const rule of rules) {
      const result = this.applyValidationRule(rule, value, context);
      if (!result.valid) {
        errors.push(result.message);
      }
    }

    return {
      valid: errors.length === 0,
      errors: errors
    };
  }

  // Apply validation rule
  applyValidationRule(rule, value, context) {
    switch (rule.type) {
      case 'required':
        return {
          valid: value !== null && value !== undefined && value !== '',
          message: `${rule.field} is required`
        };

      case 'min_length':
        return {
          valid: value.length >= rule.value,
          message: `${rule.field} must be at least ${rule.value} characters`
        };

      case 'max_length':
        return {
          valid: value.length <= rule.value,
          message: `${rule.field} must be at most ${rule.value} characters`
        };

      case 'pattern':
        return {
          valid: new RegExp(rule.pattern).test(value),
          message: `${rule.field} format is invalid`
        };

      case 'email':
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return {
          valid: emailPattern.test(value),
          message: 'Invalid email format'
        };

      case 'range':
        const num = Number(value);
        return {
          valid: num >= rule.min && num <= rule.max,
          message: `${rule.field} must be between ${rule.min} and ${rule.max}`
        };

      case 'in_list':
        return {
          valid: rule.list.includes(value),
          message: `${rule.field} must be one of: ${rule.list.join(', ')}`
        };

      case 'custom':
        return rule.validator(value, context);

      default:
        return { valid: true };
    }
  }

  // Batch validation
  validateBatch(inputs) {
    const results = [];

    for (const input of inputs) {
      const result = this.validateInput(input);
      results.push(result);
    }

    const allValid = results.every(r => r.valid);
    const allErrors = results.flatMap(r => r.errors);

    return {
      valid: allValid,
      results: results,
      errors: allErrors
    };
  }
}

// Example Input Validation Setup
const validator = new InputValidator();

// Define sanitization rules
validator.defineSanitizationRule('username', [
  { type: 'trim' },
  { type: 'lowercase' },
  { type: 'alphanumeric_only' }
]);

validator.defineSanitizationRule('email', [
  { type: 'trim' },
  { type: 'email_normalize' }
]);

validator.defineSanitizationRule('comment', [
  { type: 'remove_html' },
  { type: 'trim' }
]);

// Define validation rules
validator.defineValidationRule('username', [
  { type: 'required' },
  { type: 'min_length', value: 3 },
  { type: 'max_length', value: 20 },
  { type: 'pattern', pattern: '^[a-zA-Z0-9_]+$' }
]);

validator.defineValidationRule('email', [
  { type: 'required' },
  { type: 'email' },
  { type: 'max_length', value: 254 }
]);

validator.defineValidationRule('age', [
  { type: 'required' },
  { type: 'range', min: 13, max: 120 }
]);

// Test validation
const testInput = {
  username: '  John_Doe123!  ',
  email: 'JOHN.DOE@EXAMPLE.COM',
  age: '25',
  comment: '<script>alert("xss")</script>Hello World!'
};

const validationResult = validator.validateInput(testInput);
console.log('Validation Result:', JSON.stringify(validationResult, null, 2));
```

### Secure Error Handling
```javascript
// Secure Error Handling Implementation
class SecureErrorHandler {
  constructor() {
    this.errorLog = new SecureErrorLog();
    this.alertSystem = new AlertSystem();
    this.errorPatterns = new Map();
  }

  // Handle application errors
  handleError(error, context = {}) {
    // Classify error
    const errorClassification = this.classifyError(error);

    // Sanitize error information
    const safeError = this.sanitizeError(error);

    // Log error securely
    const logEntry = {
      timestamp: new Date(),
      errorId: this.generateErrorId(),
      classification: errorClassification,
      message: safeError.message,
      stackTrace: this.shouldIncludeStackTrace(errorClassification) ? safeError.stack : undefined,
      context: this.sanitizeContext(context),
      userId: context.userId,
      sessionId: context.sessionId,
      ipAddress: context.ipAddress
    };

    this.errorLog.logError(logEntry);

    // Check for error patterns
    this.analyzeErrorPatterns(logEntry);

    // Determine response
    const response = this.determineErrorResponse(errorClassification, context);

    // Send alerts if necessary
    if (response.alert) {
      this.alertSystem.sendAlert({
        type: 'error',
        severity: response.alertSeverity,
        message: `Error ${logEntry.errorId}: ${safeError.message}`,
        details: logEntry
      });
    }

    return response.userMessage;
  }

  // Classify error type
  classifyError(error) {
    if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
      return 'NETWORK_ERROR';
    }

    if (error.name === 'ValidationError') {
      return 'VALIDATION_ERROR';
    }

    if (error.name === 'AuthenticationError') {
      return 'AUTHENTICATION_ERROR';
    }

    if (error.name === 'AuthorizationError') {
      return 'AUTHORIZATION_ERROR';
    }

    if (error.message.includes('SQL') || error.message.includes('database')) {
      return 'DATABASE_ERROR';
    }

    if (error.name === 'SyntaxError' || error.name === 'TypeError') {
      return 'APPLICATION_ERROR';
    }

    return 'UNKNOWN_ERROR';
  }

  // Sanitize error information
  sanitizeError(error) {
    const safeError = {
      name: error.name,
      message: this.sanitizeErrorMessage(error.message),
      code: error.code
    };

    // Include stack trace only for development/debugging
    if (process.env.NODE_ENV === 'development') {
      safeError.stack = error.stack;
    }

    return safeError;
  }

  // Sanitize error message
  sanitizeErrorMessage(message) {
    // Remove sensitive information
    return message
      .replace(/password[=:][^&\s]*/gi, 'password=***')
      .replace(/token[=:][^&\s]*/gi, 'token=***')
      .replace(/key[=:][^&\s]*/gi, 'key=***')
      .replace(/secret[=:][^&\s]*/gi, 'secret=***')
      .replace(/\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b/g, '****-****-****-****') // Credit cards
      .replace(/\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g, '***-***-****'); // SSN
  }

  // Sanitize context information
  sanitizeContext(context) {
    const safeContext = { ...context };

    // Remove sensitive context data
    delete safeContext.password;
    delete safeContext.token;
    delete safeContext.sessionKey;
    delete safeContext.privateKey;

    return safeContext;
  }

  // Determine if stack trace should be included
  shouldIncludeStackTrace(classification) {
    const sensitiveErrors = ['AUTHENTICATION_ERROR', 'AUTHORIZATION_ERROR', 'VALIDATION_ERROR'];
    return !sensitiveErrors.includes(classification);
  }

  // Analyze error patterns
  analyzeErrorPatterns(logEntry) {
    const patternKey = `${logEntry.classification}:${logEntry.message}`;

    if (!this.errorPatterns.has(patternKey)) {
      this.errorPatterns.set(patternKey, {
        count: 0,
        firstSeen: logEntry.timestamp,
        lastSeen: logEntry.timestamp,
        instances: []
      });
    }

    const pattern = this.errorPatterns.get(patternKey);
    pattern.count++;
    pattern.lastSeen = logEntry.timestamp;
    pattern.instances.push(logEntry.errorId);

    // Keep only last 10 instances
    if (pattern.instances.length > 10) {
      pattern.instances = pattern.instances.slice(-10);
    }

    // Check for attack patterns
    if (pattern.count > 5 && this.isRecentActivity(pattern)) {
      this.handlePotentialAttack(pattern);
    }
  }

  // Check if activity is recent
  isRecentActivity(pattern) {
    const now = Date.now();
    const lastSeen = pattern.lastSeen.getTime();
    return (now - lastSeen) < (5 * 60 * 1000); // Within last 5 minutes
  }

  // Handle potential attack
  handlePotentialAttack(pattern) {
    console.log(`Potential attack detected: ${pattern.count} instances of ${pattern.key}`);

    this.alertSystem.sendAlert({
      type: 'potential_attack',
      severity: 'HIGH',
      message: `Repeated error pattern detected: ${pattern.key}`,
      details: {
        pattern: pattern,
        count: pattern.count,
        timeWindow: '5 minutes'
      }
    });
  }

  // Determine error response
  determineErrorResponse(classification, context) {
    const responses = {
      'NETWORK_ERROR': {
        userMessage: 'A network error occurred. Please try again later.',
        alert: false
      },
      'VALIDATION_ERROR': {
        userMessage: 'The provided information is invalid. Please check your input.',
        alert: false
      },
      'AUTHENTICATION_ERROR': {
        userMessage: 'Authentication failed. Please check your credentials.',
        alert: false
      },
      'AUTHORIZATION_ERROR': {
        userMessage: 'You do not have permission to perform this action.',
        alert: false
      },
      'DATABASE_ERROR': {
        userMessage: 'A system error occurred. Please try again later.',
        alert: true,
        alertSeverity: 'MEDIUM'
      },
      'APPLICATION_ERROR': {
        userMessage: 'An unexpected error occurred. Please try again.',
        alert: true,
        alertSeverity: 'HIGH'
      },
      'UNKNOWN_ERROR': {
        userMessage: 'An error occurred. Please contact support if the problem persists.',
        alert: true,
        alertSeverity: 'HIGH'
      }
    };

    return responses[classification] || responses['UNKNOWN_ERROR'];
  }

  // Generate unique error ID
  generateErrorId() {
    return `ERR_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Secure Error Log
class SecureErrorLog {
  async logError(logEntry) {
    // Implementation would write to secure log storage
    // Ensure logs are encrypted and access-controlled
    console.log('SECURE_ERROR_LOG:', JSON.stringify(logEntry));
  }
}

// Alert System
class AlertSystem {
  async sendAlert(alert) {
    // Implementation would send alerts via email, SMS, etc.
    console.log('ALERT:', JSON.stringify(alert));
  }
}

// Example error handling
const errorHandler = new SecureErrorHandler();

try {
  // Simulate an error
  throw new Error('Database connection failed: invalid password');
} catch (error) {
  const userMessage = errorHandler.handleError(error, {
    userId: 'user123',
    sessionId: 'session456',
    ipAddress: '192.168.1.100',
    action: 'login'
  });

  console.log('User message:', userMessage);
}
```

## Implementation Checklist

- [ ] Input validation implemented with sanitization and validation rules
- [ ] Secure error handling with classification and sanitization
- [ ] Sensitive information removed from error messages and logs
- [ ] Error patterns analyzed for potential attacks
- [ ] Appropriate user messages provided without information leakage
- [ ] Audit logging implemented for security events
- [ ] Alert system configured for critical errors
- [ ] Code review processes established
- [ ] Static analysis tools integrated
- [ ] Secure coding standards documented and followed

## Related Standards
- [[OWASP Secure Coding Practices]] - Web application security guidelines
- [[CERT Secure Coding]] - Secure coding standards and practices
- [[Debugging Security]] - Secure development debugging practices