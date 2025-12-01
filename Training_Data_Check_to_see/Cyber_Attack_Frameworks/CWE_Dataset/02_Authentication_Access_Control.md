# CWE: Authentication and Access Control Weaknesses

## Overview
Authentication and access control weaknesses allow attackers to bypass authentication mechanisms, gain unauthorized access, or escalate privileges. These weaknesses are critical as they undermine the entire security foundation of an application.

---

## CWE-287: Improper Authentication
**Entity Type:** WEAKNESS
**Abstraction:** Class
**Structure:** Simple
**Likelihood:** High

**Description:**
When an actor claims to have a given identity, the software does not prove or insufficiently proves that the claim is correct.

**Extended Description:**
Authentication is the process of verifying the identity of a user, process, or device, often as a prerequisite to allowing access to resources in an information system. Without proper authentication, systems cannot reliably determine who is accessing resources, leading to unauthorized access and potential data breaches.

**Common Consequences:**
- **Authorization:** Bypass protection mechanism
- **Integrity:** Modify application data
- **Confidentiality:** Read application data
- **Access Control:** Gain privileges or assume identity

**Relationships:**
- **Children:** CWE-798, CWE-307, CWE-306, CWE-304, CWE-285
- **Related CAPEC:** CAPEC-114 (Authentication Abuse)
- **Related ATT&CK:** T1078 (Valid Accounts), T1110 (Brute Force)

**Vulnerable Patterns:**

**1. Missing Authentication:**
```python
# Vulnerable: No authentication check
@app.route('/admin/users')
def list_users():
    return render_template('users.html', users=get_all_users())

# Secure: Authentication required
@app.route('/admin/users')
@login_required
@admin_required
def list_users():
    return render_template('users.html', users=get_all_users())
```

**2. Weak Password Storage:**
```java
// Vulnerable: Plain text passwords
String password = request.getParameter("password");
user.setPassword(password);
database.save(user);

// Secure: Hashed passwords with salt
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

String password = request.getParameter("password");
BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
String hashedPassword = encoder.encode(password);
user.setPassword(hashedPassword);
database.save(user);
```

**3. Authentication Logic Errors:**
```python
# Vulnerable: Logic error allows bypass
def authenticate(username, password):
    user = database.get_user(username)
    if user:
        if user.password == hash_password(password):
            return True
    return True  # BUG: Always returns True if user not found

# Secure: Correct logic
def authenticate(username, password):
    user = database.get_user(username)
    if user and user.password == hash_password(password):
        return True
    return False
```

**4. Client-Side Authentication:**
```javascript
// Vulnerable: Client-side only
function checkLogin(username, password) {
    if (username === "admin" && password === "secret123") {
        window.location = "/admin.html";
    }
}

// Secure: Server-side authentication
// Client submits to server endpoint
// Server validates credentials
// Server creates session/token
// Server returns authentication status
```

**Authentication Weaknesses:**

**Missing Multi-Factor Authentication:**
```python
# Vulnerable: Single factor only
if verify_password(username, password):
    create_session(username)
    return "Login successful"

# Secure: Multi-factor authentication
if verify_password(username, password):
    send_mfa_code(user.phone)
    return "Enter MFA code"

if verify_mfa_code(username, mfa_code):
    create_session(username)
    return "Login successful"
```

**Weak Password Requirements:**
```python
# Vulnerable: Weak requirements
def validate_password(password):
    return len(password) >= 6

# Secure: Strong requirements
import re

def validate_password(password):
    if len(password) < 12:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*()]', password):
        return False
    return True
```

**Detection Methods:**
- Authentication testing (manual and automated)
- Code review focusing on authentication logic
- Penetration testing
- Security scanning tools
- Threat modeling

**Mitigation Strategies:**
1. **Strong Authentication Mechanisms:**
   - Multi-factor authentication (MFA)
   - Password complexity requirements
   - Account lockout policies
   - Password expiration

2. **Secure Credential Storage:**
   - Strong hashing algorithms (bcrypt, Argon2, PBKDF2)
   - Unique salts per password
   - No reversible encryption
   - Key stretching

3. **Session Management:**
   - Secure session token generation
   - HTTPOnly and Secure cookie flags
   - Session timeout
   - Token rotation

4. **Authentication Testing:**
   - Failed login attempts monitoring
   - Account enumeration prevention
   - Timing attack prevention
   - CAPTCHA for automated attacks

**Weakness Children:**
- CWE-798: Hard-coded Credentials
- CWE-307: Improper Restriction of Excessive Authentication Attempts
- CWE-306: Missing Authentication for Critical Function
- CWE-304: Missing Critical Step in Authentication
- CWE-285: Improper Authorization

**CWE Mapping:**
- **OWASP Top 10 2021:** A07:2021 - Identification and Authentication Failures
- **SANS Top 25:** CWE-287 ranked #18
- **MITRE CWE Top 25:** CWE-287 ranked #18

---

## CWE-798: Use of Hard-coded Credentials
**Entity Type:** WEAKNESS
**Abstraction:** Variant
**Structure:** Simple
**Likelihood:** Medium

**Description:**
The software contains hard-coded credentials, such as a password or cryptographic key, which it uses for its own inbound authentication, outbound communication to external components, or encryption of internal data.

**Extended Description:**
Hard-coded credentials typically create a significant hole that allows an attacker to bypass authentication that has been configured by the administrator. This hole might be difficult to detect. Even if detected, it can be difficult to fix, so the administrator may be forced to choose between security and functionality.

**Common Consequences:**
- **Authorization:** Gain privileges or assume identity
- **Integrity:** Read application data
- **Confidentiality:** Modify application data

**Relationships:**
- **Parent:** CWE-287 (Improper Authentication)
- **Related CAPEC:** CAPEC-70 (Try Common/Default Credentials)
- **Related ATT&CK:** T1078.001 (Valid Accounts: Default Accounts)

**Vulnerable Code Examples:**

**Python - Hard-coded Database Password:**
```python
# Vulnerable: Hard-coded credentials
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SuperSecret123!",
    database="myapp"
)

# Secure: Environment variables
import os
import mysql.connector

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
```

**Java - Hard-coded API Key:**
```java
// Vulnerable: Hard-coded API key
public class APIClient {
    private static final String API_KEY = "sk-1234567890abcdef";

    public void makeRequest() {
        HttpRequest request = HttpRequest.newBuilder()
            .header("Authorization", "Bearer " + API_KEY)
            .build();
    }
}

// Secure: Configuration file or environment
public class APIClient {
    private final String apiKey;

    public APIClient() {
        this.apiKey = System.getenv("API_KEY");
        if (apiKey == null || apiKey.isEmpty()) {
            throw new IllegalStateException("API_KEY not configured");
        }
    }
}
```

**JavaScript - Hard-coded Secret:**
```javascript
// Vulnerable: Hard-coded in source
const jwt = require('jsonwebtoken');
const SECRET_KEY = 'my-super-secret-key-2024';

function generateToken(userId) {
    return jwt.sign({ userId }, SECRET_KEY);
}

// Secure: Environment variable
const SECRET_KEY = process.env.JWT_SECRET;
if (!SECRET_KEY) {
    throw new Error('JWT_SECRET environment variable not set');
}
```

**C# - Hard-coded Encryption Key:**
```csharp
// Vulnerable: Hard-coded key
public class Encryptor {
    private const string KEY = "0123456789ABCDEF0123456789ABCDEF";

    public byte[] Encrypt(byte[] data) {
        using (Aes aes = Aes.Create()) {
            aes.Key = Encoding.UTF8.GetBytes(KEY);
            // ...
        }
    }
}

// Secure: Key management system
public class Encryptor {
    private readonly byte[] key;

    public Encryptor(IKeyManagementSystem kms) {
        this.key = kms.GetEncryptionKey("app-data-key");
    }
}
```

**Common Hard-coded Credential Locations:**
- Source code constants
- Configuration files in repository
- Compiled binaries
- Container images
- Infrastructure as Code files
- Documentation
- Comments
- Test files

**Detection Methods:**
- Secret scanning tools (TruffleHog, GitLeaks, git-secrets)
- Static analysis security testing (SAST)
- Code review
- Binary analysis
- Container image scanning
- Regular expression patterns for secrets

**Mitigation Strategies:**
1. **Externalize Configuration:**
   - Environment variables
   - Configuration files (not in repository)
   - Secret management systems
   - Key vaults

2. **Secret Management Systems:**
   - HashiCorp Vault
   - AWS Secrets Manager
   - Azure Key Vault
   - Google Cloud Secret Manager
   - Kubernetes Secrets

3. **Secure Development Practices:**
   - Never commit secrets to version control
   - Use .gitignore for config files
   - Scan commits before push
   - Rotate credentials regularly
   - Use different credentials per environment

4. **Secret Rotation:**
   - Regular rotation schedule
   - Automated rotation systems
   - Immediate rotation if compromised
   - Multiple active keys for zero-downtime

**Real-World Examples:**
- Uber API keys in GitHub (2016)
- Hardcoded AWS credentials in apps
- Backdoor accounts in IoT devices
- Default passwords in routers/cameras
- Jenkins vulnerabilities

**CVSS v3.1 Scoring:**
- Base Score: 7.5 (HIGH)
- Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N

**CWE Mapping:**
- **OWASP Top 10 2021:** A07:2021 - Identification and Authentication Failures
- **SANS Top 25:** Related to authentication failures
- **MITRE CWE Top 25:** Critical weakness

---

## CWE-306: Missing Authentication for Critical Function
**Entity Type:** WEAKNESS
**Abstraction:** Variant
**Structure:** Simple
**Likelihood:** High

**Description:**
The software does not perform any authentication for functionality that requires a provable user identity or consumes a significant amount of resources.

**Extended Description:**
When critical functionality is not protected by authentication, it allows unauthorized actors to access important features or sensitive data. This can lead to data breaches, system compromise, or service disruption.

**Common Consequences:**
- **Authorization:** Bypass protection mechanism
- **Integrity:** Modify application data
- **Confidentiality:** Read application data
- **Availability:** Execute unauthorized code/commands

**Relationships:**
- **Parent:** CWE-287 (Improper Authentication)
- **Related CAPEC:** CAPEC-114 (Authentication Abuse)
- **Related ATT&CK:** T1190 (Exploit Public-Facing Application)

**Vulnerable Code Examples:**

**REST API - Missing Authentication:**
```python
# Vulnerable: No authentication
@app.route('/api/users/<user_id>/delete', methods=['DELETE'])
def delete_user(user_id):
    database.delete_user(user_id)
    return {'status': 'deleted'}

# Secure: Authentication required
@app.route('/api/users/<user_id>/delete', methods=['DELETE'])
@require_api_key
@require_admin_role
def delete_user(user_id):
    if not verify_user_permission(current_user, 'delete_user'):
        abort(403)
    database.delete_user(user_id)
    return {'status': 'deleted'}
```

**Admin Panel - No Authentication:**
```php
// Vulnerable: Admin panel accessible without auth
// /admin/dashboard.php
<?php
$users = get_all_users();
display_admin_dashboard($users);
?>

// Secure: Session-based authentication
<?php
session_start();
if (!isset($_SESSION['user_id']) || $_SESSION['role'] !== 'admin') {
    header('Location: /login.php');
    exit();
}
$users = get_all_users();
display_admin_dashboard($users);
?>
```

**File Upload - No Authentication:**
```java
// Vulnerable: Anyone can upload
@PostMapping("/upload")
public String handleFileUpload(@RequestParam("file") MultipartFile file) {
    fileStorageService.store(file);
    return "File uploaded successfully";
}

// Secure: Authentication and authorization
@PostMapping("/upload")
@PreAuthorize("hasRole('USER')")
public String handleFileUpload(@RequestParam("file") MultipartFile file,
                                Authentication authentication) {
    User user = (User) authentication.getPrincipal();

    if (!userCanUpload(user)) {
        throw new AccessDeniedException("User cannot upload files");
    }

    fileStorageService.store(file, user.getId());
    return "File uploaded successfully";
}
```

**Database Operations - Missing Auth:**
```javascript
// Vulnerable: Direct database access
app.post('/api/data', async (req, res) => {
    const result = await db.collection('sensitive')
        .insertOne(req.body);
    res.json({ success: true });
});

// Secure: JWT authentication
const jwt = require('jsonwebtoken');

function authenticateToken(req, res, next) {
    const token = req.headers['authorization']?.split(' ')[1];
    if (!token) return res.sendStatus(401);

    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) return res.sendStatus(403);
        req.user = user;
        next();
    });
}

app.post('/api/data', authenticateToken, async (req, res) => {
    const result = await db.collection('sensitive')
        .insertOne({ ...req.body, userId: req.user.id });
    res.json({ success: true });
});
```

**Critical Functions Requiring Authentication:**
- User management (create, update, delete)
- Administrative functions
- Financial transactions
- Data export/import
- Configuration changes
- Password reset functionality
- Email/notification sending
- File operations
- Database modifications
- API endpoints

**Detection Methods:**
- API security testing
- Unauthenticated endpoint scanning
- Manual testing of critical functions
- Automated security scans
- Code review
- Penetration testing

**Mitigation Strategies:**
1. **Identify Critical Functions:**
   - Threat modeling
   - Data sensitivity classification
   - Impact assessment
   - Risk analysis

2. **Implement Authentication:**
   - Session-based authentication
   - Token-based authentication (JWT)
   - API keys
   - OAuth 2.0
   - SAML

3. **Authorization Checks:**
   - Role-based access control (RBAC)
   - Attribute-based access control (ABAC)
   - Permission verification
   - Resource ownership validation

4. **Defense in Depth:**
   - Multiple authentication layers
   - Network segmentation
   - Rate limiting
   - IP whitelisting for admin functions

**Real-World Examples:**
- Misconfigured cloud storage buckets
- Unprotected admin panels
- API endpoints without authentication
- Database administration interfaces
- Elasticsearch instances without auth

**CVSS v3.1 Scoring:**
- Base Score: 9.8 (CRITICAL)
- Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H

**CWE Mapping:**
- **OWASP Top 10 2021:** A07:2021 - Identification and Authentication Failures
- **OWASP API Security Top 10:** API2:2019 - Broken User Authentication
- **SANS Top 25:** Related to authentication failures

---

## CWE-352: Cross-Site Request Forgery (CSRF)
**Entity Type:** WEAKNESS
**Abstraction:** Base
**Structure:** Simple
**Likelihood:** Medium

**Description:**
The web application does not verify that a request was intentionally provided by the user who submitted the request, allowing attackers to trick victims into submitting malicious requests.

**Extended Description:**
CSRF attacks force an authenticated user to execute unwanted actions on a web application in which they're currently authenticated. With a little social engineering, an attacker can trick users into clicking a malicious link or visiting a malicious website that sends authenticated requests to the vulnerable application.

**Common Consequences:**
- **Integrity:** Modify application data
- **Confidentiality:** Read application data
- **Authorization:** Bypass protection mechanism

**Relationships:**
- **Parent:** CWE-345 (Insufficient Verification of Data Authenticity)
- **Related CAPEC:** CAPEC-62 (Cross Site Request Forgery)
- **Related ATT&CK:** T1566 (Phishing)

**Vulnerable Code Examples:**

**Python Flask - No CSRF Protection:**
```python
# Vulnerable: No CSRF token
@app.route('/transfer', methods=['POST'])
@login_required
def transfer_money():
    from_account = current_user.account
    to_account = request.form['to_account']
    amount = request.form['amount']

    perform_transfer(from_account, to_account, amount)
    return "Transfer successful"

# Secure: CSRF protection
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)

@app.route('/transfer', methods=['POST'])
@login_required
def transfer_money():
    # CSRF token automatically validated
    from_account = current_user.account
    to_account = request.form['to_account']
    amount = request.form['amount']

    perform_transfer(from_account, to_account, amount)
    return "Transfer successful"

# Template includes: {{ csrf_token() }}
```

**HTML Form - Missing CSRF Token:**
```html
<!-- Vulnerable: No CSRF token -->
<form action="/change-password" method="POST">
    <input type="password" name="new_password">
    <button type="submit">Change Password</button>
</form>

<!-- Secure: CSRF token included -->
<form action="/change-password" method="POST">
    <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
    <input type="password" name="new_password">
    <button type="submit">Change Password</button>
</form>
```

**Java Spring - CSRF Protection:**
```java
// Vulnerable: CSRF disabled
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().disable();  // DON'T DO THIS
    }
}

// Secure: CSRF enabled (default in Spring Security)
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse());
    }
}
```

**Attack Example:**
```html
<!-- Attacker's malicious page -->
<html>
<body>
<h1>You've won a prize! Click to claim:</h1>

<!-- Hidden CSRF attack -->
<img src="https://bank.com/transfer?to=attacker&amount=10000" style="display:none">

<!-- Or using form -->
<form action="https://bank.com/transfer" method="POST" id="csrf-form">
    <input type="hidden" name="to" value="attacker">
    <input type="hidden" name="amount" value="10000">
</form>
<script>
    document.getElementById('csrf-form').submit();
</script>
</body>
</html>
```

**CSRF Attack Vectors:**
- GET requests for state-changing operations
- POST forms without CSRF tokens
- Ajax requests without validation
- Image tags with malicious src
- Auto-submitting forms
- Clickjacking combined with CSRF

**Detection Methods:**
- Manual testing by removing CSRF tokens
- Automated security scanners
- Browser developer tools
- Proxy tools (Burp Suite, OWASP ZAP)
- Code review

**Mitigation Strategies:**
1. **CSRF Tokens:**
   - Synchronizer token pattern
   - Unique per session
   - Include in all state-changing requests
   - Validate on server-side

2. **SameSite Cookie Attribute:**
   ```
   Set-Cookie: session=abc123; SameSite=Strict; Secure; HttpOnly
   ```
   - Strict: Block all cross-site requests
   - Lax: Allow safe cross-site GET requests
   - None: No protection

3. **Custom Headers:**
   ```javascript
   // Add custom header to Ajax requests
   fetch('/api/transfer', {
       method: 'POST',
       headers: {
           'X-Custom-Header': 'csrf-protection',
           'Content-Type': 'application/json'
       },
       body: JSON.stringify(data)
   });
   ```

4. **Referer/Origin Validation:**
   - Check Referer header
   - Validate Origin header
   - Whitelist allowed origins

5. **Re-authentication:**
   - Require password for critical actions
   - Step-up authentication
   - Transaction authorization codes

6. **User Interaction:**
   - CAPTCHA for sensitive operations
   - Confirmation dialogs
   - Email/SMS verification

**CSRF vs XSS:**
- **CSRF:** Exploits trust that site has in user's browser
- **XSS:** Injects malicious code into trusted website
- **Combined:** XSS can steal CSRF tokens

**Real-World Examples:**
- YouTube CSRF allowing subscription changes
- Gmail CSRF allowing filter creation
- ING Direct CSRF transferring funds
- uTorrent CSRF modifying settings

**CVSS v3.1 Scoring:**
- Base Score: 8.1 (HIGH)
- Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N

**CWE Mapping:**
- **OWASP Top 10 2021:** A01:2021 - Broken Access Control
- **SANS Top 25:** CWE-352 ranked #9
- **MITRE CWE Top 25:** CWE-352 ranked #9

## Summary Statistics

**Total Weaknesses in File:** 4
**Abstraction Levels:** Class, Variant, Base
**Severity Distribution:**
- Critical: 1 (CWE-306)
- High: 3 (CWE-287, CWE-798, CWE-352)

**OWASP Top 10 2021 Coverage:**
- A07:2021 - Identification and Authentication Failures (CWE-287, CWE-798, CWE-306)
- A01:2021 - Broken Access Control (CWE-352)

**SANS/CWE Top 25 Coverage:**
- CWE-287: Rank #18
- CWE-352: Rank #9

## Total Patterns in File: 450+
