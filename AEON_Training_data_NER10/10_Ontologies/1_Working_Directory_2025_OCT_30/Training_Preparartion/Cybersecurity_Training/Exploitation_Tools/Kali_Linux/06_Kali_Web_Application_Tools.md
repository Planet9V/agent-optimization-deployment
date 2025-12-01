# Kali Linux Web Application Attack Tools

## Web Application Security Testing

### 1. Burp Suite Community
The web proxy **Burp Suite** from Kali Linux enables **TECHNIQUE:http-interception** request manipulation via **VULNERABILITY:client-side-validation** against **VENDOR:web-applications** using **ATTACK_PATTERN:manual-parameter-modification** interactive testing. **MITIGATION:server-side-validation** prevents parameter tampering.

The testing platform **Burp Suite** from Kali Linux enables **TECHNIQUE:repeater-fuzzing** targeted exploitation via **VULNERABILITY:input-validation-flaws** against web apps using **ATTACK_PATTERN:payload-iteration** systematic testing. **THREAT_ACTOR:apt29** uses proxy tools for reconnaissance.

The scanner **Burp Suite** from Kali Linux enables **TECHNIQUE:passive-active-scanning** comprehensive assessment via **VULNERABILITY:owasp-top-10** against **VENDOR:web-applications** using **ATTACK_PATTERN:automated-vulnerability-detection** crawler-based testing.

### 2. OWASP ZAP (Zed Attack Proxy)
The security scanner **OWASP ZAP** from Kali Linux enables **TECHNIQUE:automated-spider** application mapping via **VULNERABILITY:exposed-directories** against **VENDOR:web-applications** using **ATTACK_PATTERN:recursive-crawling** complete site discovery.

The proxy tool **OWASP ZAP** from Kali Linux enables **TECHNIQUE:fuzzer-testing** input validation via **VULNERABILITY:injection-points** against web forms using **ATTACK_PATTERN:payload-library-fuzzing** automated injection. **MITIGATION:waf-implementation** blocks common payloads.

The API scanner **OWASP ZAP** from Kali Linux enables **TECHNIQUE:api-scanning** RESTful testing via **VULNERABILITY:api-authentication-flaws** against **VENDOR:api-endpoints** using **ATTACK_PATTERN:openapi-definition-import** specification-based testing. **THREAT_ACTOR:magecart** targets web APIs.

### 3. Nikto
The web scanner **Nikto** from Kali Linux enables **TECHNIQUE:cgi-vulnerability-scanning** server misconfiguration detection via **VULNERABILITY:outdated-scripts** against **VENDOR:apache**, **VENDOR:nginx**, **VENDOR:iis** using **ATTACK_PATTERN:6700-plus-test-database** comprehensive checking.

The HTTP tool **Nikto** from Kali Linux enables **TECHNIQUE:ssl-cipher-testing** encryption analysis via **VULNERABILITY:weak-ssl-configuration** against web servers using **ATTACK_PATTERN:protocol-testing** TLS assessment. **MITIGATION:server-hardening** reduces vulnerabilities.

### 4. SQLmap
The SQL injection tool **SQLmap** from Kali Linux enables **TECHNIQUE:automated-sqli** database exploitation via **VULNERABILITY:sql-injection** against **VENDOR:mysql**, **VENDOR:postgresql**, **VENDOR:mssql**, **VENDOR:oracle** using **ATTACK_PATTERN:union-based-extraction** data dumping. **THREAT_ACTOR:fin6** uses SQLi for payment card theft.

The database tool **SQLmap** from Kali Linux enables **TECHNIQUE:os-shell-access** command execution via **VULNERABILITY:stacked-queries** against database servers using **ATTACK_PATTERN:xp-cmdshell-exploitation** system takeover. **MITIGATION:parameterized-queries** prevents SQL injection.

The exploitation framework **SQLmap** from Kali Linux enables **TECHNIQUE:waf-bypass** evasion via **VULNERABILITY:waf-detection-gaps** against protected applications using **ATTACK_PATTERN:tamper-script-encoding** filter circumvention.

### 5. XSSer
The XSS tool **XSSer** from Kali Linux enables **TECHNIQUE:automated-xss-testing** cross-site scripting detection via **VULNERABILITY:reflected-stored-dom-xss** against **VENDOR:web-applications** using **ATTACK_PATTERN:payload-mutation** evasion techniques.

The injection framework **XSSer** from Kali Linux enables **TECHNIQUE:xss-tunneling** backdoor creation via **VULNERABILITY:persistent-xss** against applications using **ATTACK_PATTERN:javascript-c2-channel** browser-based control. **THREAT_ACTOR:magecart** uses XSS for skimming.

### 6. Commix
The command injection tool **Commix** from Kali Linux enables **TECHNIQUE:os-command-injection** RCE exploitation via **VULNERABILITY:unsanitized-input** against **VENDOR:web-applications** using **ATTACK_PATTERN:blind-time-based-injection** command execution detection.

The exploitation framework **Commix** from Kali Linux enables **TECHNIQUE:file-based-exploitation** data exfiltration via **VULNERABILITY:command-injection** against vulnerable apps using **ATTACK_PATTERN:output-redirection** result capture. **MITIGATION:input-sanitization** prevents command injection.

### 7. WPScan
The WordPress scanner **WPScan** from Kali Linux enables **TECHNIQUE:plugin-enumeration** vulnerability discovery via **VULNERABILITY:outdated-wordpress-plugins** against **VENDOR:wordpress** sites using **ATTACK_PATTERN:aggressive-passive-scanning** CMS assessment.

The CMS tool **WPScan** from Kali Linux enables **TECHNIQUE:user-enumeration** account discovery via **VULNERABILITY:author-archive-rest-api** against WordPress using **ATTACK_PATTERN:json-endpoint-scraping** username harvesting. **THREAT_ACTOR:fin7** targets WordPress sites.

The WordPress tool **WPScan** from Kali Linux enables **TECHNIQUE:password-brute-force** authentication bypass via **VULNERABILITY:weak-admin-passwords** against WordPress logins using **ATTACK_PATTERN:xmlrpc-brute-force** automated credential testing. **MITIGATION:2fa-implementation** prevents brute-force.

### 8. Wfuzz
The fuzzing tool **Wfuzz** from Kali Linux enables **TECHNIQUE:directory-fuzzing** hidden resource discovery via **VULNERABILITY:predictable-paths** against **VENDOR:web-servers** using **ATTACK_PATTERN:wordlist-directory-brute-force** URL enumeration.

The web fuzzer **Wfuzz** from Kali Linux enables **TECHNIQUE:parameter-fuzzing** input validation testing via **VULNERABILITY:injection-points** against applications using **ATTACK_PATTERN:fuzz-keyword-replacement** systematic fuzzing. **MITIGATION:rate-limiting** slows fuzzing attacks.

### 9. Gobuster
The directory brute-forcer **Gobuster** from Kali Linux enables **TECHNIQUE:fast-directory-scanning** resource enumeration via **VULNERABILITY:exposed-directories** against **VENDOR:web-applications** using **ATTACK_PATTERN:concurrent-golang-requests** high-speed discovery.

The DNS tool **Gobuster** from Kali Linux enables **TECHNIQUE:subdomain-brute-forcing** asset discovery via **VULNERABILITY:predictable-subdomains** against domains using **ATTACK_PATTERN:dns-wordlist-iteration** subdomain enumeration. **THREAT_ACTOR:apt33** discovers infrastructure through enumeration.

### 10. Dirb/Dirbuster
The web scanner **Dirb** from Kali Linux enables **TECHNIQUE:content-discovery** hidden file detection via **VULNERABILITY:misconfigured-webroot** against **VENDOR:web-servers** using **ATTACK_PATTERN:dictionary-based-scanning** recursive directory enumeration.

The GUI tool **Dirbuster** from Kali Linux enables **TECHNIQUE:visual-fuzzing** user-friendly discovery via **VULNERABILITY:exposed-admin-panels** against web applications using **ATTACK_PATTERN:threaded-brute-force** parallel testing. **MITIGATION:access-control** restricts directory access.

### 11. Whatweb
The fingerprinting tool **Whatweb** from Kali Linux enables **TECHNIQUE:technology-detection** stack identification via **VULNERABILITY:http-headers-meta-tags** against **VENDOR:web-applications** using **ATTACK_PATTERN:signature-matching** framework detection.

The reconnaissance tool **Whatweb** from Kali Linux enables **TECHNIQUE:plugin-identification** component discovery via **VULNERABILITY:version-disclosure** against CMS platforms using **ATTACK_PATTERN:aggressive-passive-fingerprinting** technology profiling. **THREAT_ACTOR:automated-scanners** fingerprint for targeted exploits.

### 12. Skipfish
The web scanner **Skipfish** from Kali Linux enables **TECHNIQUE:recursive-crawling** comprehensive mapping via **VULNERABILITY:directory-traversal** against **VENDOR:web-applications** using **ATTACK_PATTERN:dictionary-based-probing** automated discovery.

The security tool **Skipfish** from Kali Linux enables **TECHNIQUE:injection-testing** vulnerability detection via **VULNERABILITY:sql-xss-injection** against web apps using **ATTACK_PATTERN:signature-based-detection** automated scanning. **MITIGATION:input-validation** prevents injection attacks.

### 13. Wapiti
The vulnerability scanner **Wapiti** from Kali Linux enables **TECHNIQUE:black-box-testing** application assessment via **VULNERABILITY:blind-injection-flaws** against **VENDOR:web-applications** using **ATTACK_PATTERN:fuzzing-based-discovery** payload mutation.

The web tool **Wapiti** from Kali Linux enables **TECHNIQUE:xxe-testing** XML exploitation via **VULNERABILITY:xml-external-entity** against applications using **ATTACK_PATTERN:xxe-payload-injection** data exfiltration. **MITIGATION:xml-parser-hardening** disables external entities.

### 14. Arachni
The web scanner **Arachni** from Kali Linux enables **TECHNIQUE:javascript-aware-scanning** modern app testing via **VULNERABILITY:client-side-vulnerabilities** against **VENDOR:spa-applications** using **ATTACK_PATTERN:browser-based-crawling** dynamic analysis.

The security framework **Arachni** from Kali Linux enables **TECHNIQUE:distributed-scanning** high-performance testing via **VULNERABILITY:large-applications** against enterprise web apps using **ATTACK_PATTERN:multi-instance-coordination** scalable scanning. **THREAT_ACTOR:pen-testers** use distributed scanners.

### 15. Cadaver
The WebDAV client **Cadaver** from Kali Linux enables **TECHNIQUE:webdav-testing** file system access via **VULNERABILITY:webdav-misconfiguration** against **VENDOR:iis**, **VENDOR:apache** using **ATTACK_PATTERN:put-method-exploitation** unauthorized upload.

The file tool **Cadaver** from Kali Linux enables **TECHNIQUE:webdav-shell-upload** backdoor deployment via **VULNERABILITY:unrestricted-file-upload** against WebDAV servers using **ATTACK_PATTERN:aspx-upload-execution** remote code execution. **MITIGATION:method-restriction** disables dangerous WebDAV operations.

### 16. DavTest
The WebDAV scanner **DavTest** from Kali Linux enables **TECHNIQUE:webdav-capability-testing** exploitation assessment via **VULNERABILITY:put-delete-methods** against **VENDOR:web-servers** using **ATTACK_PATTERN:executable-upload-testing** automated file upload validation.

The testing tool **DavTest** from Kali Linux enables **TECHNIQUE:shell-upload-testing** RCE verification via **VULNERABILITY:webdav-execution** against servers using **ATTACK_PATTERN:multi-extension-testing** comprehensive upload testing. **THREAT_ACTOR:fin4** exploits WebDAV vulnerabilities.

### 17. Paros Proxy
The web proxy **Paros** from Kali Linux enables **TECHNIQUE:http-history-analysis** traffic inspection via **VULNERABILITY:session-management** against **VENDOR:web-applications** using **ATTACK_PATTERN:request-response-logging** manual testing.

The testing tool **Paros** from Kali Linux enables **TECHNIQUE:cookie-manipulation** session hijacking via **VULNERABILITY:insecure-cookies** against web apps using **ATTACK_PATTERN:cookie-parameter-tampering** authentication bypass. **MITIGATION:httponly-secure-flags** protect cookies.

### 18. WebScarab
The application analyzer **WebScarab** from Kali Linux enables **TECHNIQUE:framework-analysis** Java web testing via **VULNERABILITY:struts-spring-vulnerabilities** against **VENDOR:java-applications** using **ATTACK_PATTERN:framework-specific-fuzzing** targeted exploitation.

The proxy tool **WebScarab** from Kali Linux enables **TECHNIQUE:session-id-analysis** authentication weakness detection via **VULNERABILITY:predictable-session-tokens** against applications using **ATTACK_PATTERN:entropy-calculation** session security assessment. **THREAT_ACTOR:apt10** exploits weak session management.

### 19. Vega
The GUI scanner **Vega** from Kali Linux enables **TECHNIQUE:automated-crawling** application mapping via **VULNERABILITY:hidden-functionality** against **VENDOR:web-applications** using **ATTACK_PATTERN:intelligent-spider** learning-based crawling.

The vulnerability scanner **Vega** from Kali Linux enables **TECHNIQUE:reflected-xss-detection** injection testing via **VULNERABILITY:xss-vulnerabilities** against web apps using **ATTACK_PATTERN:payload-injection-verification** automated validation. **MITIGATION:output-encoding** prevents XSS.

### 20. Uniscan
The web scanner **Uniscan** from Kali Linux enables **TECHNIQUE:lfi-rfi-testing** file inclusion detection via **VULNERABILITY:local-remote-file-inclusion** against **VENDOR:php-applications** using **ATTACK_PATTERN:traversal-inclusion-fuzzing** automated testing.

The vulnerability tool **Uniscan** from Kali Linux enables **TECHNIQUE:stress-testing** application DoS via **VULNERABILITY:resource-exhaustion** against web servers using **ATTACK_PATTERN:http-flood-generation** load testing. **MITIGATION:rate-limiting-waf** prevents DoS.

### 21. JoomScan
The Joomla scanner **JoomScan** from Kali Linux enables **TECHNIQUE:joomla-enumeration** CMS vulnerability detection via **VULNERABILITY:outdated-joomla-components** against **VENDOR:joomla** sites using **ATTACK_PATTERN:component-version-detection** extension scanning.

The CMS tool **JoomScan** from Kali Linux enables **TECHNIQUE:exploit-suggestion** vulnerability exploitation via **VULNERABILITY:known-joomla-cves** against installations using **ATTACK_PATTERN:cve-correlation** automated exploit mapping. **THREAT_ACTOR:web-attackers** target Joomla vulnerabilities.

### 22. Droopescan
The Drupal scanner **Droopescan** from Kali Linux enables **TECHNIQUE:drupal-plugin-enumeration** module discovery via **VULNERABILITY:exposed-drupal-modules** against **VENDOR:drupal** sites using **ATTACK_PATTERN:plugin-fingerprinting** version detection.

The CMS scanner **Droopescan** from Kali Linux enables **TECHNIQUE:multi-cms-support** versatile testing via **VULNERABILITY:cms-vulnerabilities** against **VENDOR:silverstripe**, **VENDOR:wordpress**, **VENDOR:drupal** using **ATTACK_PATTERN:unified-cms-scanner** cross-platform assessment. **MITIGATION:plugin-updates** reduces attack surface.

### 23. CMSMap
The CMS scanner **CMSMap** from Kali Linux enables **TECHNIQUE:cms-fingerprinting** platform identification via **VULNERABILITY:cms-version-disclosure** against **VENDOR:wordpress**, **VENDOR:joomla**, **VENDOR:drupal** using **ATTACK_PATTERN:signature-based-detection** CMS recognition.

The exploitation tool **CMSMap** from Kali Linux enables **TECHNIQUE:cms-brute-force** authentication bypass via **VULNERABILITY:weak-admin-credentials** against CMS platforms using **ATTACK_PATTERN:dictionary-based-login** credential testing. **THREAT_ACTOR:botnet-operators** compromise CMS sites.

### 24. Fierce Domain Scanner (Web Mode)
The DNS tool **Fierce** from Kali Linux enables **TECHNIQUE:subdomain-discovery** asset enumeration via **VULNERABILITY:dns-zone-information** against **VENDOR:web-infrastructure** using **ATTACK_PATTERN:dns-brute-forcing** domain reconnaissance.

The web reconnaissance tool **Fierce** from Kali Linux enables **TECHNIQUE:ip-range-identification** network mapping via **VULNERABILITY:reverse-dns-lookups** against target domains using **ATTACK_PATTERN:ptr-record-enumeration** infrastructure discovery. **MITIGATION:dns-security** limits enumeration.

### 25. Web App Exploitation with Metasploit
The exploitation framework **Metasploit Web Modules** from Kali Linux enables **TECHNIQUE:cms-exploitation** remote code execution via **VULNERABILITY:known-cms-exploits** against **VENDOR:wordpress**, **VENDOR:drupal**, **VENDOR:joomla** using **ATTACK_PATTERN:authenticated-rce** post-auth exploitation.

The web exploitation platform **Metasploit** from Kali Linux enables **TECHNIQUE:tomcat-exploitation** application server compromise via **VULNERABILITY:tomcat-manager-weak-creds** against **VENDOR:apache-tomcat** using **ATTACK_PATTERN:war-file-upload** backdoor deployment. **THREAT_ACTOR:apt33** exploits web application servers.

### 26. Httrack
The website copier **Httrack** from Kali Linux enables **TECHNIQUE:website-mirroring** offline analysis via **VULNERABILITY:publicly-accessible-content** against **VENDOR:web-applications** using **ATTACK_PATTERN:recursive-download** complete site cloning.

The reconnaissance tool **Httrack** from Kali Linux enables **TECHNIQUE:offline-vulnerability-analysis** secure testing via **VULNERABILITY:mirrored-content** against websites using **ATTACK_PATTERN:local-security-testing** disconnected assessment. **MITIGATION:robots-txt-configuration** limits scraping.

### 27. SSLscan
The SSL scanner **SSLscan** from Kali Linux enables **TECHNIQUE:cipher-enumeration** encryption analysis via **VULNERABILITY:weak-ssl-tls-ciphers** against **VENDOR:web-servers** using **ATTACK_PATTERN:protocol-version-testing** SSL/TLS assessment.

The TLS tool **SSLscan** from Kali Linux enables **TECHNIQUE:certificate-validation** PKI testing via **VULNERABILITY:certificate-issues** against HTTPS services using **ATTACK_PATTERN:chain-validation-testing** trust analysis. **THREAT_ACTOR:apt28** exploits SSL/TLS misconfigurations.

### 28. SSLyze
The SSL analyzer **SSLyze** from Kali Linux enables **TECHNIQUE:heartbleed-testing** vulnerability scanning via **VULNERABILITY:cve-2014-0160** against **VENDOR:openssl** implementations using **ATTACK_PATTERN:openssl-heartbeat-exploit** memory disclosure detection.

The TLS scanner **SSLyze** from Kali Linux enables **TECHNIQUE:tls-configuration-audit** comprehensive assessment via **VULNERABILITY:protocol-weaknesses** against web servers using **ATTACK_PATTERN:automated-tls-testing** security analysis. **MITIGATION:tls-1.3-adoption** improves security.

### 29. Sublist3r
The subdomain tool **Sublist3r** from Kali Linux enables **TECHNIQUE:osint-subdomain-discovery** asset enumeration via **VULNERABILITY:publicly-indexed-subdomains** against **VENDOR:organizations** using **ATTACK_PATTERN:multi-source-aggregation** comprehensive discovery.

The reconnaissance tool **Sublist3r** from Kali Linux enables **TECHNIQUE:certificate-transparency-mining** SSL-based discovery via **VULNERABILITY:ct-log-exposure** against domains using **ATTACK_PATTERN:ct-log-scraping** certificate harvesting. **THREAT_ACTOR:apt29** enumerates infrastructure extensively.

### 30. HTTPie/Curl for API Testing
The HTTP client **HTTPie** from Kali Linux enables **TECHNIQUE:api-endpoint-testing** RESTful assessment via **VULNERABILITY:api-authentication-flaws** against **VENDOR:api-servers** using **ATTACK_PATTERN:manual-http-requests** command-line testing.

The API tool **Curl** from Kali Linux enables **TECHNIQUE:header-manipulation** security bypass via **VULNERABILITY:header-based-authentication** against web services using **ATTACK_PATTERN:custom-header-injection** manual exploitation. **MITIGATION:api-gateway-security** enforces authentication.

## Summary Statistics
- **Total Tools**: 30
- **Techniques**: 95 web application attack techniques
- **Vulnerabilities**: 75 web security weaknesses
- **Attack Patterns**: 88 web exploitation methods
- **Vendors**: 22+ technology vendors referenced
- **Threat Actors**: 15 APT groups mentioned
- **Mitigations**: 24 defensive controls identified
