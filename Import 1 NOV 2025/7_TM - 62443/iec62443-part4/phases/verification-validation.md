# Phase 5: Verification and Validation

**Objective:** Verify and validate security controls through testing and assessment.

## Security Testing Methodology

### Static Application Security Testing (SAST)
```javascript
// SAST Implementation for IACS Code
class StaticApplicationSecurityTester {
  constructor() {
    this.rules = new Map();
    this.vulnerabilities = [];
    this.severityLevels = {
      CRITICAL: 9,
      HIGH: 7,
      MEDIUM: 5,
      LOW: 3,
      INFO: 1
    };
  }

  // Define security rules
  defineRule(ruleId, pattern, message, severity, category) {
    this.rules.set(ruleId, {
      id: ruleId,
      pattern: pattern,
      message: message,
      severity: severity,
      category: category
    });
  }

  // Analyze source code
  async analyzeCode(sourceCode, filePath) {
    const findings = [];

    for (const [ruleId, rule] of this.rules) {
      const matches = this.scanForPattern(sourceCode, rule.pattern);

      for (const match of matches) {
        findings.push({
          ruleId: ruleId,
          file: filePath,
          line: match.line,
          column: match.column,
          code: match.code,
          message: rule.message,
          severity: rule.severity,
          category: rule.category,
          confidence: match.confidence || 1.0
        });
      }
    }

    return findings;
  }

  // Scan for pattern in code
  scanForPattern(code, pattern) {
    const matches = [];
    const lines = code.split('\n');

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const regex = new RegExp(pattern, 'gi');
      let match;

      while ((match = regex.exec(line)) !== null) {
        matches.push({
          line: i + 1,
          column: match.index + 1,
          code: line.trim(),
          match: match[0],
          confidence: this.calculateConfidence(match, line)
        });
      }
    }

    return matches;
  }

  // Calculate confidence in finding
  calculateConfidence(match, line) {
    let confidence = 0.8; // Base confidence

    // Increase confidence for dangerous patterns
    if (line.includes('password') || line.includes('secret') || line.includes('key')) {
      confidence += 0.1;
    }

    // Decrease confidence for commented code
    if (line.trim().startsWith('//') || line.trim().startsWith('/*') || line.trim().startsWith('*')) {
      confidence -= 0.3;
    }

    // Decrease confidence for test files
    if (line.includes('test') || line.includes('spec') || line.includes('mock')) {
      confidence -= 0.2;
    }

    return Math.max(0.1, Math.min(1.0, confidence));
  }

  // Analyze entire codebase
  async analyzeCodebase(filePaths) {
    const allFindings = [];

    for (const filePath of filePaths) {
      try {
        const sourceCode = await this.readFile(filePath);
        const findings = await this.analyzeCode(sourceCode, filePath);
        allFindings.push(...findings);
      } catch (error) {
        console.error(`Error analyzing ${filePath}: ${error.message}`);
      }
    }

    // Process and prioritize findings
    const processedFindings = this.processFindings(allFindings);

    return {
      summary: this.generateSummary(processedFindings),
      findings: processedFindings,
      recommendations: this.generateRecommendations(processedFindings)
    };
  }

  // Process findings
  processFindings(findings) {
    return findings
      .sort((a, b) => this.severityLevels[b.severity] - this.severityLevels[a.severity])
      .map(finding => ({
        ...finding,
        severityScore: this.severityLevels[finding.severity],
        cwe: this.mapToCWE(finding.ruleId),
        owasp: this.mapToOWASP(finding.category)
      }));
  }

  // Generate summary
  generateSummary(findings) {
    const severityCounts = {};
    const categoryCounts = {};

    for (const finding of findings) {
      severityCounts[finding.severity] = (severityCounts[finding.severity] || 0) + 1;
      categoryCounts[finding.category] = (categoryCounts[finding.category] || 0) + 1;
    }

    return {
      totalFindings: findings.length,
      severityBreakdown: severityCounts,
      categoryBreakdown: categoryCounts,
      riskScore: this.calculateRiskScore(findings)
    };
  }

  // Calculate overall risk score
  calculateRiskScore(findings) {
    let totalScore = 0;

    for (const finding of findings) {
      totalScore += finding.severityScore * finding.confidence;
    }

    return Math.min(100, totalScore / 10); // Normalize to 0-100 scale
  }

  // Generate recommendations
  generateRecommendations(findings) {
    const recommendations = [];

    const criticalCount = findings.filter(f => f.severity === 'CRITICAL').length;
    const highCount = findings.filter(f => f.severity === 'HIGH').length;

    if (criticalCount > 0) {
      recommendations.push({
        priority: 'CRITICAL',
        action: 'Immediate remediation required for critical findings',
        timeframe: 'Within 24 hours'
      });
    }

    if (highCount > 5) {
      recommendations.push({
        priority: 'HIGH',
        action: 'Address high-severity findings within sprint',
        timeframe: 'Within 1-2 weeks'
      });
    }

    recommendations.push({
      priority: 'MEDIUM',
      action: 'Implement security training for development team',
      timeframe: 'Ongoing'
    });

    recommendations.push({
      priority: 'MEDIUM',
      action: 'Integrate SAST into CI/CD pipeline',
      timeframe: 'Within 1 month'
    });

    return recommendations;
  }

  // Map to CWE
  mapToCWE(ruleId) {
    const cweMappings = {
      'hardcoded_password': 'CWE-798',
      'sql_injection': 'CWE-89',
      'xss_vulnerable': 'CWE-79',
      'weak_crypto': 'CWE-327',
      'path_traversal': 'CWE-22'
    };

    return cweMappings[ruleId] || 'CWE-710';
  }

  // Map to OWASP
  mapToOWASP(category) {
    const owaspMappings = {
      'injection': 'A03:2021-Injection',
      'authentication': 'A07:2021-Identification and Authentication Failures',
      'authorization': 'A01:2021-Broken Access Control',
      'cryptography': 'A02:2021-Cryptographic Failures',
      'configuration': 'A05:2021-Security Misconfiguration'
    };

    return owaspMappings[category] || 'A00:2021';
  }

  // File reading utility
  async readFile(filePath) {
    // Implementation would read file contents
    return 'sample code content';
  }
}

// Define security rules
const sast = new StaticApplicationSecurityTester();

sast.defineRule('hardcoded_password', 'password\\s*[=:]\\s*["\'][^"\']+["\']', 'Hardcoded password detected', 'CRITICAL', 'authentication');
sast.defineRule('sql_injection', '(SELECT|INSERT|UPDATE|DELETE).*\\+.*\\$|concat.*sql', 'Potential SQL injection vulnerability', 'HIGH', 'injection');
sast.defineRule('xss_vulnerable', 'document\\.write\\(|innerHTML\\s*[=:]', 'Potential XSS vulnerability', 'HIGH', 'injection');
sast.defineRule('weak_crypto', 'MD5\\(|SHA1\\(', 'Weak cryptographic function used', 'MEDIUM', 'cryptography');
sast.defineRule('path_traversal', '\\.\\./|\\.\\.', 'Potential path traversal vulnerability', 'MEDIUM', 'authorization');

// Example analysis
const sampleCode = `
function login(username, password) {
  const query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'";
  // Hardcoded password for testing
  const adminPass = "admin123";
  document.write("Welcome " + username);
  return executeQuery(query);
}
`;

const findings = sast.analyzeCode(sampleCode, 'login.js');
console.log('SAST Findings:', JSON.stringify(findings, null, 2));
```

### Dynamic Application Security Testing (DAST)
```javascript
// DAST Implementation for IACS Applications
class DynamicApplicationSecurityTester {
  constructor() {
    this.scanners = new Map();
    this.testCases = new Map();
    this.vulnerabilities = [];
  }

  // Register security scanner
  registerScanner(name, scanner) {
    this.scanners.set(name, scanner);
  }

  // Define test case
  defineTestCase(testId, description, category, payload, expectedResult) {
    this.testCases.set(testId, {
      id: testId,
      description: description,
      category: category,
      payload: payload,
      expectedResult: expectedResult
    });
  }

  // Execute DAST scan
  async executeScan(targetUrl, scanConfig = {}) {
    const results = {
      scanId: this.generateScanId(),
      startTime: new Date(),
      target: targetUrl,
      findings: [],
      summary: {}
    };

    // Execute test cases
    for (const [testId, testCase] of this.testCases) {
      try {
        const finding = await this.executeTestCase(testCase, targetUrl, scanConfig);
        if (finding) {
          results.findings.push(finding);
        }
      } catch (error) {
        console.error(`Test case ${testId} failed: ${error.message}`);
      }
    }

    // Execute automated scanners
    for (const [scannerName, scanner] of this.scanners) {
      try {
        const scannerResults = await scanner.scan(targetUrl, scanConfig);
        results.findings.push(...scannerResults);
      } catch (error) {
        console.error(`Scanner ${scannerName} failed: ${error.message}`);
      }
    }

    // Process results
    results.endTime = new Date();
    results.duration = results.endTime - results.startTime;
    results.summary = this.generateSummary(results.findings);

    return results;
  }

  // Execute individual test case
  async executeTestCase(testCase, targetUrl, config) {
    // Prepare request
    const request = this.prepareRequest(testCase, targetUrl);

    // Send request
    const response = await this.sendRequest(request);

    // Analyze response
    const analysis = this.analyzeResponse(response, testCase);

    if (analysis.vulnerable) {
      return {
        testId: testCase.id,
        category: testCase.category,
        severity: analysis.severity,
        description: testCase.description,
        url: targetUrl,
        payload: testCase.payload,
        evidence: analysis.evidence,
        remediation: this.getRemediation(testCase.category)
      };
    }

    return null;
  }

  // Prepare HTTP request
  prepareRequest(testCase, targetUrl) {
    // Implementation would prepare HTTP request with test payload
    return {
      url: targetUrl,
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'DAST-Scanner/1.0'
      },
      body: `input=${encodeURIComponent(testCase.payload)}`
    };
  }

  // Send HTTP request
  async sendRequest(request) {
    // Implementation would send HTTP request and return response
    return {
      status: 200,
      headers: {},
      body: 'Response body'
    };
  }

  // Analyze response for vulnerabilities
  analyzeResponse(response, testCase) {
    const analysis = {
      vulnerable: false,
      severity: 'LOW',
      evidence: []
    };

    // Check for expected vulnerable behavior
    if (testCase.expectedResult === 'error' && response.status === 500) {
      analysis.vulnerable = true;
      analysis.severity = 'HIGH';
      analysis.evidence.push('Application returned 500 error with malicious input');
    }

    if (testCase.expectedResult === 'reflected' && response.body.includes(testCase.payload)) {
      analysis.vulnerable = true;
      analysis.severity = 'MEDIUM';
      analysis.evidence.push('Input reflected in response without sanitization');
    }

    if (testCase.expectedResult === 'data_exposed' && response.body.includes('sensitive_data')) {
      analysis.vulnerable = true;
      analysis.severity = 'CRITICAL';
      analysis.evidence.push('Sensitive data exposed in response');
    }

    return analysis;
  }

  // Get remediation advice
  getRemediation(category) {
    const remediations = {
      'sql_injection': 'Use parameterized queries or prepared statements. Validate and sanitize all input.',
      'xss': 'Encode output and validate input. Use Content Security Policy (CSP).',
      'authentication': 'Implement multi-factor authentication and secure password policies.',
      'authorization': 'Implement proper access controls and principle of least privilege.',
      'cryptography': 'Use strong encryption algorithms and proper key management.'
    };

    return remediations[category] || 'Implement appropriate security controls and input validation.';
  }

  // Generate scan summary
  generateSummary(findings) {
    const severityCounts = {};
    const categoryCounts = {};

    for (const finding of findings) {
      severityCounts[finding.severity] = (severityCounts[finding.severity] || 0) + 1;
      categoryCounts[finding.category] = (categoryCounts[finding.category] || 0) + 1;
    }

    return {
      totalFindings: findings.length,
      severityBreakdown: severityCounts,
      categoryBreakdown: categoryCounts,
      riskLevel: this.calculateRiskLevel(findings)
    };
  }

  // Calculate overall risk level
  calculateRiskLevel(findings) {
    const criticalCount = findings.filter(f => f.severity === 'CRITICAL').length;
    const highCount = findings.filter(f => f.severity === 'HIGH').length;

    if (criticalCount > 0) return 'CRITICAL';
    if (highCount > 3) return 'HIGH';
    if (highCount > 0) return 'MEDIUM';
    return 'LOW';
  }

  // Generate scan ID
  generateScanId() {
    return `DAST_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Define test cases
const dast = new DynamicApplicationSecurityTester();

dast.defineTestCase('sql_injection_1', 'Basic SQL injection test', 'sql_injection', "' OR '1'='1", 'error');
dast.defineTestCase('xss_1', 'Basic XSS test', 'xss', '<script>alert("xss")</script>', 'reflected');
dast.defineTestCase('auth_bypass', 'Authentication bypass test', 'authentication', 'admin\' --', 'bypass');

// Example scan
const scanResults = await dast.executeScan('http://target-app.com/login');
console.log('DAST Results:', JSON.stringify(scanResults, null, 2));
```

## Validation Checklist

- [ ] SAST integrated into CI/CD pipeline
- [ ] DAST scans performed on staging environments
- [ ] Security test cases defined for common vulnerabilities
- [ ] Vulnerability findings triaged and prioritized
- [ ] False positive rates minimized through rule tuning
- [ ] Security testing results documented and tracked
- [ ] Remediation plans developed for critical findings
- [ ] Regression testing includes security test cases
- [ ] Third-party component vulnerability scanning implemented
- [ ] Penetration testing conducted by qualified personnel

## Related Standards
- [[OWASP Testing Guide]] - Comprehensive web application security testing
- [[NIST SP 800-115]] - Technical guide to information security testing
- [[PTES]] - Penetration Testing Execution Standard
- [[Vulnerability Management]] - Security testing and validation processes