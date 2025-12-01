// CAPEC v3.9 Comprehensive Import
// Generated: 2025-11-08T10:46:52.712362
// Source: MITRE CAPEC v3.9 XML

// ========================================
// 1. CREATE/UPDATE CAPEC NODES
// ========================================


MERGE (capec:AttackPattern {id: 'CAPEC-1'})
SET capec.name = "Accessing Functionality Not Properly Constrained by ACLs",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "In applications, particularly web applications, access to functionality is mitigated by an authorization framework. This framework maps Access Control Lists (ACLs) to elements of the application's functionality; particularly URL's for web apps. In the case that the administrator failed to specify an ACL for a particular element, an attacker may be able to access it with impunity. An attacker with the ability to access functionality not properly constrained by ACLs can obtain sensitive informatio",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-10'})
SET capec.name = "Buffer Overflow via Environment Variables",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack pattern involves causing a buffer overflow through manipulation of environment variables. Once the adversary finds that they can modify an environment variable, they may try to overflow associated buffers. This attack leverages implicit trust often placed in environment variables.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-100'})
SET capec.name = "Overflow Buffers",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "Buffer Overflow attacks target improper or missing bounds checking on buffer operations, typically triggered by input injected by an adversary. As a consequence, an adversary is able to write past the boundaries of allocated buffer regions in memory, causing a program crash or potentially redirection of execution as per the adversaries' choice.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-101'})
SET capec.name = "Server Side Include (SSI) Injection",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker can use Server Side Include (SSI) Injection to send code to a web application that then gets executed by the web server. Doing so enables the attacker to achieve similar results to Cross Site Scripting, viz., arbitrary code execution and information disclosure, albeit on a more limited scale, since the SSI directives are nowhere near as powerful as a full-fledged scripting language. Nonetheless, the attacker can conveniently gain access to sensitive files, such as password files, and",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-102'})
SET capec.name = "Session Sidejacking",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Session sidejacking takes advantage of an unencrypted communication channel between a victim and target system. The attacker sniffs traffic on a network looking for session tokens in unencrypted traffic. Once a session token is captured, the attacker performs malicious actions by using the stolen token with the targeted application to impersonate the victim. This attack is a specific method of session hijacking, which is exploiting a valid session token to gain unauthorized access to a target sy",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-103'})
SET capec.name = "Clickjacking",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary tricks a victim into unknowingly initiating some action in one system while interacting with the UI from a seemingly completely different, usually an adversary controlled or intended, system.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-104'})
SET capec.name = "Cross Zone Scripting",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker is able to cause a victim to load content into their web-browser that bypasses security zone controls and gain access to increased privileges to execute scripting code or other web objects such as unsigned ActiveX controls or applets. This is a privilege elevation attack targeted at zone-based web-browser security.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-105'})
SET capec.name = "HTTP Request Splitting",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-106'})
SET capec.name = "DEPRECATED: XSS through Log Files",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it referes to an existing chain relationship between \"CAPEC-93 : Log Injection-Tampering-Forging\" and \"CAPEC-63 : Cross-Site Scripting\". Please refer to these CAPECs going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-107'})
SET capec.name = "Cross Site Tracing",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Cross Site Tracing (XST) enables an adversary to steal the victim's session cookie and possibly other authentication credentials transmitted in the header of the HTTP request when the victim's browser communicates to a destination system's web server.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-108'})
SET capec.name = "Command Line Execution through SQL Injection",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker uses standard SQL injection methods to inject data into the command line for execution. This could be done directly through misuse of directives such as MSSQL_xp_cmdshell or indirectly through injection of data into the database that would be interpreted as shell commands. Sometime later, an unscrupulous backend application (or could be part of the functionality of the same application) fetches the injected data stored in the database and uses this data as command line arguments with",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-109'})
SET capec.name = "Object Relational Mapping Injection",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker leverages a weakness present in the database access layer code generated with an Object Relational Mapping (ORM) tool or a weakness in the way that a developer used a persistence framework to inject their own SQL commands to be executed against the underlying database. The attack here is similar to plain SQL injection, except that the application does not use JDBC to directly talk to the database, but instead it uses a data access layer generated by an ORM tool or framework (e.g. Hib",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-11'})
SET capec.name = "Cause Web Server Misclassification",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attack of this type exploits a Web server's decision to take action based on filename or file extension. Because different file types are handled by different server processes, misclassification may force the Web server to take unexpected action, or expected actions in an unexpected sequence. This may cause the server to exhaust resources, supply debug or system data to the attacker, or bind an attacker to a remote process.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-110'})
SET capec.name = "SQL Injection through SOAP Parameter Tampering",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker modifies the parameters of the SOAP message that is sent from the service consumer to the service provider to initiate a SQL injection attack. On the service provider side, the SOAP message is parsed and parameters are not properly validated before being used to access a database in a way that does not use parameter binding, thus enabling the attacker to control the structure of the executed SQL query. This pattern describes a SQL injection attack with the delivery mechanism being a ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-111'})
SET capec.name = "JSON Hijacking (aka JavaScript Hijacking)",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker targets a system that uses JavaScript Object Notation (JSON) as a transport mechanism between the client and the server (common in Web 2.0 systems using AJAX) to steal possibly confidential information transmitted from the server back to the client inside the JSON object by taking advantage of the loophole in the browser's Same Origin Policy that does not prohibit JavaScript from one website to be included and executed in the context of another website.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-112'})
SET capec.name = "Brute Force",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "In this attack, some asset (information, functionality, identity, etc.) is protected by a finite secret value. The attacker attempts to gain access to this asset by using trial-and-error to exhaustively explore all the possible secret values in the hope of finding the secret (or a value that is functionally equivalent) that will unlock the asset.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-113'})
SET capec.name = "Interface Manipulation",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An adversary manipulates the use or processing of an interface (e.g. Application Programming Interface (API) or System-on-Chip (SoC)) resulting in an adverse impact upon the security of the system implementing the interface. This can allow the adversary to bypass access control and/or execute functionality not intended by the interface implementation, possibly compromising the system which integrates the interface. Interface manipulation can take on a number of forms including forcing the unexpe",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-114'})
SET capec.name = "Authentication Abuse",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An attacker obtains unauthorized access to an application, service or device either through knowledge of the inherent weaknesses of an authentication mechanism, or by exploiting a flaw in the authentication scheme's implementation. In such an attack an authentication mechanism is functioning but a carefully controlled sequence of events causes the mechanism to grant access to the attacker.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-115'})
SET capec.name = "Authentication Bypass",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An attacker gains access to application, service, or device with the privileges of an authorized or privileged user by evading or circumventing an authentication mechanism. The attacker is therefore able to access protected data without authentication ever having taken place.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-116'})
SET capec.name = "Excavation",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary actively probes the target in a manner that is designed to solicit information that could be leveraged for malicious purposes.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-117'})
SET capec.name = "Interception",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary monitors data streams to or from the target for information gathering purposes. This attack may be undertaken to solely gather sensitive information or to support a further attack against the target. This attack pattern can involve sniffing network traffic as well as other types of data streams (e.g. radio). The adversary can attempt to initiate the establishment of a data stream or passively observe the communications as they unfold. In all variants of this attack, the adversary is",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-12'})
SET capec.name = "Choosing Message Identifier",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "This pattern of attack is defined by the selection of messages distributed via multicast or public information channels that are intended for another client by determining the parameter value assigned to that client. This attack allows the adversary to gain access to potentially privileged information, and to possibly perpetrate other attacks through the distribution means by impersonation. If the channel/message being manipulated is an input rather than output mechanism for the system, (such as",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-120'})
SET capec.name = "Double Encoding",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "The adversary utilizes a repeating of the encoding process for a set of characters (that is, character encoding a character encoding of a character) to obfuscate the payload of a particular request. This may allow the adversary to bypass filters that attempt to detect illegal characters or strings, such as those that might be used in traversal or injection attacks. Filters may be able to catch illegal encoded strings, but may not catch doubly encoded strings. For example, a dot (.), often used i",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-121'})
SET capec.name = "Exploit Non-Production Interfaces",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-122'})
SET capec.name = "Privilege Abuse",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An adversary is able to exploit features of the target that should be reserved for privileged users or administrators but are exposed to use by lower or non-privileged accounts. Access to sensitive information and functionality must be controlled to ensure that only authorized users are able to access these resources.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-123'})
SET capec.name = "Buffer Manipulation",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An adversary manipulates an application's interaction with a buffer in an attempt to read or modify data they shouldn't have access to. Buffer attacks are distinguished in that it is the buffer space itself that is the target of the attack rather than any code responsible for interpreting the content of the buffer. In virtually all buffer attacks the content that is placed in the buffer is immaterial. Instead, most buffer attacks involve retrieving or providing more input than can be stored in t",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-124'})
SET capec.name = "Shared Resource Manipulation",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An adversary exploits a resource shared between multiple applications, an application pool or hardware pin multiplexing to affect behavior. Resources may be shared between multiple applications or between multiple threads of a single application. Resource sharing is usually accomplished through mutual access to a single memory location or multiplexed hardware pins. If an adversary can manipulate this shared resource (usually by co-opting one of the applications or threads) the other applications",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-125'})
SET capec.name = "Flooding",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary consumes the resources of a target by rapidly engaging in a large number of interactions with the target. This type of attack generally exposes a weakness in rate limiting or flow. When successful this attack prevents legitimate users from accessing the service and can cause the target to crash. This attack differs from resource depletion through leaks or allocations in that the latter attacks do not rely on the volume of requests made to the target but instead focus on manipulation",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-126'})
SET capec.name = "Path Traversal",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary uses path manipulation methods to exploit insufficient input validation of a target to obtain access to data that should be not be retrievable by ordinary well-formed requests. A typical variety of this attack involves specifying a path to a desired file together with dot-dot-slash characters, resulting in the file access API or function traversing out of the intended directory structure and into the root file system. By replacing or modifying the expected path information the acces",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-127'})
SET capec.name = "Directory Indexing",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary crafts a request to a target that results in the target listing/indexing the content of a directory as output. One common method of triggering directory contents as output is to construct a request containing a path that terminates in a directory name rather than a file name since many applications are configured to provide a list of the directory's contents when such a request is received. An adversary can use this to explore the directory tree on a target as well as learn the name",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-128'})
SET capec.name = "Integer Attacks",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker takes advantage of the structure of integer variables to cause these variables to assume values that are not expected by an application. For example, adding one to the largest positive integer in a signed integer variable results in a negative number. Negative numbers may be illegal in an application and the application may prevent an attacker from providing them directly, but the application may not consider that adding two positive numbers can create a negative number do to the str",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-129'})
SET capec.name = "Pointer Manipulation",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "This attack pattern involves an adversary manipulating a pointer within a target application resulting in the application accessing an unintended memory location. This can result in the crashing of the application or, for certain pointer values, access to data that would not normally be possible or the execution of arbitrary code. Since pointers are simply integer variables, Integer Attacks may often be used in Pointer Attacks.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-13'})
SET capec.name = "Subverting Environment Variable Values",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "The adversary directly or indirectly modifies environment variables used by or controlling the target software. The adversary's goal is to cause the target software to deviate from its expected operation in a manner that benefits the adversary.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-130'})
SET capec.name = "Excessive Allocation",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary causes the target to allocate excessive resources to servicing the attackers' request, thereby reducing the resources available for legitimate services and degrading or denying services. Usually, this attack focuses on memory allocation, but any finite resource on the target could be the attacked, including bandwidth, processing cycles, or other resources. This attack does not attempt to force this allocation through a large number of requests (that would be Resource Depletion throu",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-131'})
SET capec.name = "Resource Leak Exposure",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary utilizes a resource leak on the target to deplete the quantity of the resource available to service legitimate requests.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-132'})
SET capec.name = "Symlink Attack",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary positions a symbolic link in such a manner that the targeted user or application accesses the link's endpoint, assuming that it is accessing a file with the link's name.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-133'})
SET capec.name = "Try All Common Switches",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker attempts to invoke all common switches and options in the target application for the purpose of discovering weaknesses in the target. For example, in some applications, adding a --debug switch causes debugging information to be displayed, which can sometimes reveal sensitive processing or configuration information to an attacker. This attack differs from other forms of API abuse in that the attacker is indiscriminately attempting to invoke options in the hope that one of them will wo",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-134'})
SET capec.name = "Email Injection",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary manipulates the headers and content of an email message by injecting data via the use of delimiter characters native to the protocol.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-135'})
SET capec.name = "Format String Injection",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary includes formatting characters in a string input field on the target application. Most applications assume that users will provide static text and may respond unpredictably to the presence of formatting character. For example, in certain functions of the C programming languages such as printf, the formatting character %s will print the contents of a memory location expecting this location to identify a string and the formatting character %n prints the number of DWORD written in the ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-136'})
SET capec.name = "LDAP Injection",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker manipulates or crafts an LDAP query for the purpose of undermining the security of the target. Some applications use user input to create LDAP queries that are processed by an LDAP server. For example, a user might provide their username during authentication and the username might be inserted in an LDAP query during the authentication process. An attacker could use this input to inject additional commands into an LDAP query that could disclose sensitive information. For example, ent",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-137'})
SET capec.name = "Parameter Injection",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary manipulates the content of request parameters for the purpose of undermining the security of the target. Some parameter encodings use text characters as separators. For example, parameters in a HTTP GET message are encoded as name-value pairs separated by an ampersand (&). If an attacker can supply text strings that are used to fill in these parameters, then they can inject special characters used in the encoding scheme to add or modify parameters. For example, if user input is fed ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-138'})
SET capec.name = "Reflection Injection",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary supplies a value to the target application which is then used by reflection methods to identify a class, method, or field. For example, in the Java programming language the reflection libraries permit an application to inspect, load, and invoke classes and their components by name. If an adversary can control the input into these methods including the name of the class/method/field or the parameters passed to methods, they can cause the targeted application to invoke incorrect metho",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-139'})
SET capec.name = "Relative Path Traversal",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker exploits a weakness in input validation on the target by supplying a specially constructed path utilizing dot and slash characters for the purpose of obtaining access to arbitrary files or resources. An attacker modifies a known path on the target in order to reach material that is not available through intended channels. These attacks normally involve adding additional path separators (/ or \\) and/or dots (.), or encodings thereof, in various combinations in order to reach parent di",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-14'})
SET capec.name = "Client-side Injection-induced Buffer Overflow",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This type of attack exploits a buffer overflow vulnerability in targeted client software through injection of malicious content from a custom-built hostile service. This hostile service is created to deliver the correct content to the client software. For example, if the client-side application is a browser, the service will host a webpage that the browser loads.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-140'})
SET capec.name = "Bypassing of Intermediate Forms in Multiple-Form Sets",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "Some web applications require users to submit information through an ordered sequence of web forms. This is often done if there is a very large amount of information being collected or if information on earlier forms is used to pre-populate fields or determine which additional information the application needs to collect. An attacker who knows the names of the various forms in the sequence may be able to explicitly type in the name of a later form and navigate to it without first going through t",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-141'})
SET capec.name = "Cache Poisoning",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker exploits the functionality of cache technologies to cause specific data to be cached that aids the attackers' objectives. This describes any attack whereby an attacker places incorrect or harmful material in cache. The targeted cache can be an application's cache (e.g. a web browser cache) or a public cache (e.g. a DNS or ARP cache). Until the cache is refreshed, most applications or clients will treat the corrupted cache value as valid. This can lead to a wide range of exploits incl",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-142'})
SET capec.name = "DNS Cache Poisoning",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "A domain name server translates a domain name (such as www.example.com) into an IP address that Internet hosts use to contact Internet resources. An adversary modifies a public DNS cache to cause certain names to resolve to incorrect addresses that the adversary specifies. The result is that client applications that rely upon the targeted cache for domain name resolution will be directed not to the actual address of the specified domain name but to some other address. Adversaries can use this to",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-143'})
SET capec.name = "Detect Unpublicized Web Pages",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary searches a targeted web site for web pages that have not been publicized. In doing this, the adversary may be able to gain access to information that the targeted site did not intend to make public.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-144'})
SET capec.name = "Detect Unpublicized Web Services",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary searches a targeted web site for web services that have not been publicized. This attack can be especially dangerous since unpublished but available services may not have adequate security controls placed upon them given that an administrator may believe they are unreachable.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-145'})
SET capec.name = "Checksum Spoofing",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary spoofs a checksum message for the purpose of making a payload appear to have a valid corresponding checksum. Checksums are used to verify message integrity. They consist of some value based on the value of the message they are protecting. Hash codes are a common checksum mechanism. Both the sender and recipient are able to compute the checksum based on the contents of the message. If the message contents change between the sender and recipient, the sender and recipient will compute ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-146'})
SET capec.name = "XML Schema Poisoning",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary corrupts or modifies the content of XML schema information passed between a client and server for the purpose of undermining the security of the target. XML Schemas provide the structure and content definitions for XML documents. Schema poisoning is the ability to manipulate a schema either by replacing or modifying it to compromise the programs that process documents that use this schema.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-147'})
SET capec.name = "XML Ping of the Death",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker initiates a resource depletion attack where a large number of small XML messages are delivered at a sufficiently rapid rate to cause a denial of service or crash of the target. Transactions such as repetitive SOAP transactions can deplete resources faster than a simple flooding attack because of the additional resources used by the SOAP protocol and the resources necessary to process SOAP messages. The transactions used are immaterial as long as they cause resource utilization on the",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-148'})
SET capec.name = "Content Spoofing",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary modifies content to make it contain something other than what the original content producer intended while keeping the apparent source of the content unchanged. The term content spoofing is most often used to describe modification of web pages hosted by a target to display the adversary's content instead of the owner's content. However, any content can be spoofed, including the content of email messages, file transfers, or the content of other network communication protocols. Conten",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-149'})
SET capec.name = "Explore for Predictable Temporary File Names",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker explores a target to identify the names and locations of predictable temporary files for the purpose of launching further attacks against the target. This involves analyzing naming conventions and storage locations of the temporary files created by a target application. If an attacker can predict the names of temporary files they can use this information to mount other attacks, such as information gathering and symlink attacks.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-15'})
SET capec.name = "Command Delimiters",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attack of this type exploits a programs' vulnerabilities that allows an attacker's commands to be concatenated onto a legitimate command with the intent of targeting other resources such as the file system or database. The system that uses a filter or denylist input validation, as opposed to allowlist validation is vulnerable to an attacker who predicts delimiters (or combinations of delimiters) not present in the filter or denylist. As with other injection attacks, the attacker uses the comm",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-150'})
SET capec.name = "Collect Data from Common Resource Locations",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary exploits well-known locations for resources for the purposes of undermining the security of the target. In many, if not most systems, files and resources are organized in a default tree structure. This can be useful for adversaries because they often know where to look for resources or files that are necessary for attacks. Even when the precise location of a targeted resource may not be known, naming conventions may indicate a small area of the target machine's file tree where the r",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-151'})
SET capec.name = "Identity Spoofing",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "Identity Spoofing refers to the action of assuming (i.e., taking on) the identity of some other entity (human or non-human) and then using that identity to accomplish a goal. An adversary may craft messages that appear to come from a different principle or use stolen / spoofed authentication credentials.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-153'})
SET capec.name = "Input Data Manipulation",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An attacker exploits a weakness in input validation by controlling the format, structure, and composition of data to an input-processing interface. By supplying input of a non-standard or unexpected form an attacker can adversely impact the security of the target.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-154'})
SET capec.name = "Resource Location Spoofing",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary deceives an application or user and convinces them to request a resource from an unintended location. By spoofing the location, the adversary can cause an alternate resource to be used, often one that the adversary controls and can be used to help them achieve their malicious goals.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-155'})
SET capec.name = "Screen Temporary Files for Sensitive Information",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary exploits the temporary, insecure storage of information by monitoring the content of files used to store temp data during an application's routine execution flow. Many applications use temporary files to accelerate processing or to provide records of state across multiple executions of the application. Sometimes, however, these temporary files may end up storing sensitive information. By screening an application's temporary files, an adversary might be able to discover such sensitiv",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-157'})
SET capec.name = "Sniffing Attacks",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "In this attack pattern, the adversary intercepts information transmitted between two third parties. The adversary must be able to observe, read, and/or hear the communication traffic, but not necessarily block the communication or change its content. Any transmission medium can theoretically be sniffed if the adversary can examine the contents between the sender and recipient. Sniffing Attacks are similar to Adversary-In-The-Middle attacks (CAPEC-94), but are entirely passive. AiTM attacks are p",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-158'})
SET capec.name = "Sniffing Network Traffic",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack pattern, the adversary monitors network traffic between nodes of a public or multicast network in an attempt to capture sensitive information at the protocol level. Network sniffing applications can reveal TCP/IP, DNS, Ethernet, and other low-level network communication information. The adversary takes a passive role in this attack pattern and simply observes and analyzes the traffic. The adversary may precipitate or indirectly influence the content of the observed transaction, bu",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-159'})
SET capec.name = "Redirect Access to Libraries",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary exploits a weakness in the way an application searches for external libraries to manipulate the execution flow to point to an adversary supplied library or code base. This pattern of attack allows the adversary to compromise the application or server via the execution of unauthorized code. An application typically makes calls to functions that are a part of libraries external to the application. These libraries may be part of the operating system or they may be third party libraries",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-16'})
SET capec.name = "Dictionary-based Password Attack",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-160'})
SET capec.name = "Exploit Script-Based APIs",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "Some APIs support scripting instructions as arguments. Methods that take scripted instructions (or references to scripted instructions) can be very flexible and powerful. However, if an attacker can specify the script that serves as input to these methods they can gain access to a great deal of functionality. For example, HTML pages support <script> tags that allow scripting languages to be embedded in the page and then interpreted by the receiving web browser. If the content provider is malicio",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-161'})
SET capec.name = "Infrastructure Manipulation",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An attacker exploits characteristics of the infrastructure of a network entity in order to perpetrate attacks or information gathering on network objects or effect a change in the ordinary information flow between network objects. Most often, this involves manipulation of the routing of network messages so, instead of arriving at their proper destination, they are directed towards an entity of the attackers' choosing, usually a server controlled by the attacker. The victim is often unaware that ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-162'})
SET capec.name = "Manipulating Hidden Fields",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary exploits a weakness in the server's trust of client-side processing by modifying data on the client-side, such as price information, and then submitting this data to the server, which processes the modified data. For example, eShoplifting is a data manipulation attack against an on-line merchant during a purchasing transaction. The manipulation of price, discount or quantity fields in the transaction message allows the adversary to acquire items at a lower cost than the merchant int",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-163'})
SET capec.name = "Spear Phishing",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary targets a specific user or group with a Phishing (CAPEC-98) attack tailored to a category of users in order to have maximum relevance and deceptive capability. Spear Phishing is an enhanced version of the Phishing attack targeted to a specific user or group. The quality of the targeted email is usually enhanced by appearing to come from a known or trusted entity. If the email account of some trusted entity has been compromised the message may be digitally signed. The message will co",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-164'})
SET capec.name = "Mobile Phishing",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary targets mobile phone users with a phishing attack for the purpose of soliciting account passwords or sensitive information from the user. Mobile Phishing is a variation of the Phishing social engineering technique where the attack is initiated via a text or SMS message, rather than email. The user is enticed to provide information or visit a compromised web site via this message. Apart from the manner in which the attack is initiated, the attack proceeds as a standard Phishing attac",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-165'})
SET capec.name = "File Manipulation",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An attacker modifies file contents or attributes (such as extensions or names) of files in a manner to cause incorrect processing by an application. Attackers use this class of attacks to cause applications to enter unstable states, overwrite or expose sensitive information, and even execute arbitrary code with the application's privileges. This class of attacks differs from attacks on configuration information (even if file-based) in that file manipulation causes the file processing to result i",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-166'})
SET capec.name = "Force the System to Reset Values",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker forces the target into a previous state in order to leverage potential weaknesses in the target dependent upon a prior configuration or state-dependent factors. Even in cases where an attacker may not be able to directly control the configuration of the targeted application, they may be able to reset the configuration to a prior state since many applications implement reset functions.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-167'})
SET capec.name = "White Box Reverse Engineering",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker discovers the structure, function, and composition of a type of computer software through white box analysis techniques. White box techniques involve methods which can be applied to a piece of software when an executable or some other compiled object can be directly subjected to analysis, revealing at least a portion of its machine instructions that can be observed upon execution.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-168'})
SET capec.name = "Windows ::DATA Alternate Data Stream",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker exploits the functionality of Microsoft NTFS Alternate Data Streams (ADS) to undermine system security. ADS allows multiple \"files\" to be stored in one directory entry referenced as filename:streamname. One or more alternate data streams may be stored in any file or directory. Normal Microsoft utilities do not show the presence of an ADS stream attached to a file. The additional space for the ADS is not recorded in the displayed file size. The additional space for ADS is accounted fo",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-169'})
SET capec.name = "Footprinting",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary engages in probing and exploration activities to identify constituents and properties of the target.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-17'})
SET capec.name = "Using Malicious Files",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attack of this type exploits a system's configuration that allows an adversary to either directly access an executable file, for example through shell access; or in a possible worst case allows an adversary to upload a file and then execute it. Web servers, ftp servers, and message oriented middleware systems which have many integration points are particularly vulnerable, because both the programmers and the administrators must be in synch regarding the interfaces and the correct privileges f",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-170'})
SET capec.name = "Web Application Fingerprinting",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker sends a series of probes to a web application in order to elicit version-dependent and type-dependent behavior that assists in identifying the target. An attacker could learn information such as software versions, error pages, and response headers, variations in implementations of the HTTP protocol, directory structures, and other similar information about the targeted service. This information can then be used by an attacker to formulate a targeted attack plan. While web application",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-171'})
SET capec.name = "DEPRECATED: Variable Manipulation",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of the existing attack pattern \"CAPEC-77 : Manipulating User-Controlled Variables\". Please refer to this other CAPEC going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-173'})
SET capec.name = "Action Spoofing",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary is able to disguise one action for another and therefore trick a user into initiating one type of action when they intend to initiate a different action. For example, a user might be led to believe that clicking a button will submit a query, but in fact it downloads software. Adversaries may perform this attack through social means, such as by simply convincing a victim to perform the action or relying on a user's natural inclination to do so, or through technical means, such as a c",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-174'})
SET capec.name = "Flash Parameter Injection",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary takes advantage of improper data validation to inject malicious global parameters into a Flash file embedded within an HTML document. Flash files can leverage user-submitted data to configure the Flash document and access the embedding HTML document.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-175'})
SET capec.name = "Code Inclusion",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary exploits a weakness on the target to force arbitrary code to be retrieved locally or from a remote location and executed. This differs from code injection in that code injection involves the direct inclusion of code while code inclusion involves the addition or replacement of a reference to a code file, which is subsequently loaded by the target and used as part of the code of some application.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-176'})
SET capec.name = "Configuration/Environment Manipulation",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An attacker manipulates files or settings external to a target application which affect the behavior of that application. For example, many applications use external configuration files and libraries - modification of these entities or otherwise affecting the application's ability to use them would constitute a configuration/environment manipulation attack.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-177'})
SET capec.name = "Create files with the same name as files protected with a higher classification",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker exploits file location algorithms in an operating system or application by creating a file with the same name as a protected or privileged file. The attacker could manipulate the system if the attacker-created file is trusted by the operating system or an application component that attempts to load the original file. Applications often load or include external files, such as libraries or configuration files. These files should be protected against malicious manipulation. However, if ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-178'})
SET capec.name = "Cross-Site Flashing",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker is able to trick the victim into executing a Flash document that passes commands or calls to a Flash player browser plugin, allowing the attacker to exploit native Flash functionality in the client browser. This attack pattern occurs where an attacker can provide a crafted link to a Flash document (SWF file) which, when followed, will cause additional malicious instructions to be executed. The attacker does not need to serve or control the Flash document. The attack takes advantage o",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-179'})
SET capec.name = "Calling Micro-Services Directly",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker is able to discover and query Micro-services at a web location and thereby expose the Micro-services to further exploitation by gathering information about their implementation and function. Micro-services in web pages allow portions of a page to connect to the server and update content without needing to cause the entire page to update. This allows user activity to change portions of the page more quickly without causing disruptions elsewhere.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-18'})
SET capec.name = "XSS Targeting Non-Script Elements",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack is a form of Cross-Site Scripting (XSS) where malicious scripts are embedded in elements that are not expected to host scripts such as image tags (<img>), comments in XML documents (< !-CDATA->), etc. These tags may not be subject to the same input validation, output validation, and other content filtering and checking routines, so this can create an opportunity for an adversary to tunnel through the application's elements and launch a XSS attack through other elements. As with all r",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-180'})
SET capec.name = "Exploiting Incorrectly Configured Access Control Security Levels",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker exploits a weakness in the configuration of access controls and is able to bypass the intended protection that these measures guard against and thereby obtain unauthorized access to the system or network. Sensitive functionality should always be protected with access controls. However configuring all but the most trivial access control systems can be very complicated and there are many opportunities for mistakes. If an attacker can learn of incorrectly configured access security sett",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-181'})
SET capec.name = "Flash File Overlay",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker creates a transparent overlay using flash in order to intercept user actions for the purpose of performing a clickjacking attack. In this technique, the Flash file provides a transparent overlay over HTML content. Because the Flash application is on top of the content, user actions, such as clicks, are caught by the Flash application rather than the underlying HTML. The action is then interpreted by the overlay to perform the actions the attacker wishes.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-182'})
SET capec.name = "Flash Injection",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker tricks a victim to execute malicious flash content that executes commands or makes flash calls specified by the attacker. One example of this attack is cross-site flashing, an attacker controlled parameter to a reference call loads from content specified by the attacker.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-183'})
SET capec.name = "IMAP/SMTP Command Injection",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary exploits weaknesses in input validation on web-mail servers to execute commands on the IMAP/SMTP server. Web-mail servers often sit between the Internet and the IMAP or SMTP mail server. User requests are received by the web-mail servers which then query the back-end mail server for the requested information and return this response to the user. In an IMAP/SMTP command injection attack, mail-server commands are embedded in parts of the request sent to the web-mail server. If the web",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-184'})
SET capec.name = "Software Integrity Attack",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An attacker initiates a series of events designed to cause a user, program, server, or device to perform actions which undermine the integrity of software code, device data structures, or device firmware, achieving the modification of the target's integrity to achieve an insecure state.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-185'})
SET capec.name = "Malicious Software Download",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker uses deceptive methods to cause a user or an automated process to download and install dangerous code that originates from an attacker controlled source. There are several variations to this strategy of attack.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-186'})
SET capec.name = "Malicious Software Update",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary uses deceptive methods to cause a user or an automated process to download and install dangerous code believed to be a valid update that originates from an adversary controlled source.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-187'})
SET capec.name = "Malicious Automated Software Update via Redirection",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker exploits two layers of weaknesses in server or client software for automated update mechanisms to undermine the integrity of the target code-base. The first weakness involves a failure to properly authenticate a server as a source of update or patch content. This type of weakness typically results from authentication mechanisms which can be defeated, allowing a hostile server to satisfy the criteria that establish a trust relationship. The second weakness is a systemic failure to val",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-188'})
SET capec.name = "Reverse Engineering",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary discovers the structure, function, and composition of an object, resource, or system by using a variety of analysis techniques to effectively determine how the analyzed entity was constructed or operates. The goal of reverse engineering is often to duplicate the function, or a part of the function, of an object in order to duplicate or \"back engineer\" some aspect of its functioning. Reverse engineering techniques can be applied to mechanical objects, electronic devices, or software,",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-189'})
SET capec.name = "Black Box Reverse Engineering",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary discovers the structure, function, and composition of a type of computer software through black box analysis techniques. 'Black Box' methods involve interacting with the software indirectly, in the absence of direct access to the executable object. Such analysis typically involves interacting with the software at the boundaries of where the software interfaces with a larger execution environment, such as input-output vectors, libraries, or APIs. Black Box Reverse Engineering also re",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-19'})
SET capec.name = "Embedding Scripts within Scripts",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary leverages the capability to execute their own script by embedding it within other scripts that the target software is likely to execute due to programs' vulnerabilities that are brought on by allowing remote hosts to execute scripts.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-190'})
SET capec.name = "Reverse Engineer an Executable to Expose Assumed Hidden Functionality",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker analyzes a binary file or executable for the purpose of discovering the structure, function, and possibly source-code of the file by using a variety of analysis techniques to effectively determine how the software functions and operates. This type of analysis is also referred to as Reverse Code Engineering, as techniques exist for extracting source code from an executable. Several techniques are often employed for this purpose, both black box and white box. The use of computer bus an",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-191'})
SET capec.name = "Read Sensitive Constants Within an Executable",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-192'})
SET capec.name = "Protocol Analysis",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary engages in activities to decipher and/or decode protocol information for a network or application communication protocol used for transmitting information between interconnected nodes or systems on a packet-switched data network. While this type of analysis involves the analysis of a networking protocol inherently, it does not require the presence of an actual or physical network.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-193'})
SET capec.name = "PHP Remote File Inclusion",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this pattern the adversary is able to load and execute arbitrary code remotely available from the application. This is usually accomplished through an insecurely configured PHP runtime environment and an improperly sanitized \"include\" or \"require\" call, which the user can then control to point to any web-accessible file. This allows adversaries to hijack the targeted application and force it to execute their own instructions.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-194'})
SET capec.name = "Fake the Source of Data",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary takes advantage of improper authentication to provide data or services under a falsified identity. The purpose of using the falsified identity may be to prevent traceability of the provided data or to assume the rights granted to another individual. One of the simplest forms of this attack would be the creation of an email message with a modified \"From\" field in order to appear that the message was sent from someone other than the actual sender. The root of the attack (in this case ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-195'})
SET capec.name = "Principal Spoof",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "A Principal Spoof is a form of Identity Spoofing where an adversary pretends to be some other person in an interaction. This is often accomplished by crafting a message (either written, verbal, or visual) that appears to come from a person other than the adversary. Phishing and Pharming attacks often attempt to do this so that their attempts to gather sensitive information appear to come from a legitimate source. A Principal Spoof does not use stolen or spoofed authentication credentials, instea",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-196'})
SET capec.name = "Session Credential Falsification through Forging",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker creates a false but functional session credential in order to gain or usurp access to a service. Session credentials allow users to identify themselves to a service after an initial authentication without needing to resend the authentication information (usually a username and password) with every message. If an attacker is able to forge valid session credentials they may be able to bypass authentication or piggy-back off some other authenticated user's session. This attack differs f",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-197'})
SET capec.name = "Exponential Data Expansion",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary submits data to a target application which contains nested exponential data expansion to produce excessively large output. Many data format languages allow the definition of macro-like structures that can be used to simplify the creation of complex structures. However, this capability can be abused to create excessive demands on a processor's CPU and memory. A small number of nested expansions can result in an exponential growth in demands on memory.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-198'})
SET capec.name = "XSS Targeting Error Pages",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary distributes a link (or possibly some other query structure) with a request to a third party web server that is malformed and also contains a block of exploit code in order to have the exploit become live code in the resulting error page.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-199'})
SET capec.name = "XSS Using Alternate Syntax",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary uses alternate forms of keywords or commands that result in the same action as the primary form but which may not be caught by filters. For example, many keywords are processed in a case insensitive manner. If the site's web filtering algorithm does not convert all tags into a consistent case before the comparison with forbidden keywords it is possible to bypass filters (e.g., incomplete black lists) by using an alternate case structure. For example, the \"script\" tag using the alter",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-2'})
SET capec.name = "Inducing Account Lockout",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker leverages the security functionality of the system aimed at thwarting potential attacks to launch a denial of service attack against a legitimate system user. Many systems, for instance, implement a password throttling mechanism that locks an account after a certain number of incorrect log in attempts. An attacker can leverage this throttling mechanism to lock a legitimate user out of their own account. The weakness that is being leveraged by an attacker is the very security feature ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-20'})
SET capec.name = "Encryption Brute Forcing",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker, armed with the cipher text and the encryption algorithm used, performs an exhaustive (brute force) search on the key space to determine the key that decrypts the cipher text to obtain the plaintext.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-200'})
SET capec.name = "Removal of filters: Input filters, output filters, data masking",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker removes or disables filtering mechanisms on the target application. Input filters prevent invalid data from being sent to an application (for example, overly large inputs that might cause a buffer overflow or other malformed inputs that may not be correctly handled by an application). Input filters might also be designed to constrained executable content.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-201'})
SET capec.name = "Serialized Data External Linking",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary creates a serialized data file (e.g. XML, YAML, etc...) that contains an external data reference. Because serialized data parsers may not validate documents with external references, there may be no checks on the nature of the reference in the external data. This can allow an adversary to open arbitrary files or connections, which may further lead to the adversary gaining access to information on the system that they would normally be unable to obtain.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-202'})
SET capec.name = "Create Malicious Client",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary creates a client application to interface with a target service where the client violates assumptions the service makes about clients. Services that have designated client applications (as opposed to services that use general client applications, such as IMAP or POP mail servers which can interact with any IMAP or POP client) may assume that the client will follow specific procedures.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-203'})
SET capec.name = "Manipulate Registry Information",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary exploits a weakness in authorization in order to modify content within a registry (e.g., Windows Registry, Mac plist, application registry). Editing registry information can permit the adversary to hide configuration information or remove indicators of compromise to cover up activity. Many applications utilize registries to store configuration and service information. As such, modification of registry information can affect individual services (affecting billing, authorization, or e",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-204'})
SET capec.name = "Lifting Sensitive Data Embedded in Cache",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary examines a target application's cache, or a browser cache, for sensitive information. Many applications that communicate with remote entities or which perform intensive calculations utilize caches to improve efficiency. However, if the application computes or receives sensitive information and the cache is not appropriately protected, an attacker can browse the cache and retrieve this information. This can result in the disclosure of sensitive information.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-205'})
SET capec.name = "DEPRECATED: Lifting credential(s)/key material embedded in client distributions (thick or thin)",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of CAPEC-37 : Retrieve Embedded Sensitive Data. Please refer to this other pattern going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-206'})
SET capec.name = "Signing Malicious Code",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "The adversary extracts credentials used for code signing from a production environment and then uses these credentials to sign malicious content with the developer's key. Many developers use signing keys to sign code or hashes of code. When users or applications verify the signatures are accurate they are led to believe that the code came from the owner of the signing key and that the code has not been modified since the signature was applied. If the adversary has extracted the signing credentia",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-207'})
SET capec.name = "Removing Important Client Functionality",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary removes or disables functionality on the client that the server assumes to be present and trustworthy.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-208'})
SET capec.name = "Removing/short-circuiting 'Purse' logic: removing/mutating 'cash' decrements",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker removes or modifies the logic on a client associated with monetary calculations resulting in incorrect information being sent to the server. A server may rely on a client to correctly compute monetary information. For example, a server might supply a price for an item and then rely on the client to correctly compute the total cost of a purchase given the number of items the user is buying. If the attacker can remove or modify the logic that controls these calculations, they can retur",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-209'})
SET capec.name = "XSS Using MIME Type Mismatch",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary creates a file with scripting content but where the specified MIME type of the file is such that scripting is not expected. The adversary tricks the victim into accessing a URL that responds with the script file. Some browsers will detect that the specified MIME type of the file does not match the actual type of its content and will automatically switch to using an interpreter for the real content type. If the browser does not invoke script filters before doing this, the adversary's",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-21'})
SET capec.name = "Exploitation of Trusted Identifiers",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-211'})
SET capec.name = "DEPRECATED: Leveraging web tools (e.g. Mozilla's GreaseMonkey, Firebug) to change application behavior",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it was deemed not to be a legitimate attack pattern.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-212'})
SET capec.name = "Functionality Misuse",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary leverages a legitimate capability of an application in such a way as to achieve a negative technical impact. The system functionality is not altered or modified but used in a way that was not intended. This is often accomplished through the overuse of a specific functionality or by leveraging functionality with design flaws that enables the adversary to gain access to unauthorized, sensitive data.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-213'})
SET capec.name = "DEPRECATED: Directory Traversal",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of the existing attack pattern \"CAPEC-126 : Path Traversal\". Please refer to this other CAPEC going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-214'})
SET capec.name = "DEPRECATED: Fuzzing for garnering J2EE/.NET-based stack traces, for application mapping",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it was merged into \"CAPEC-215 : Fuzzing for application mapping\". Please refer to this other CAPEC going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-215'})
SET capec.name = "Fuzzing for application mapping",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker sends random, malformed, or otherwise unexpected messages to a target application and observes the application's log or error messages returned. The attacker does not initially know how a target will respond to individual messages but by attempting a large number of message variants they may find a variant that trigger's desired behavior. In this attack, the purpose of the fuzzing is to observe the application's log and error messages, although fuzzing a target can also sometimes cau",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-216'})
SET capec.name = "Communication Channel Manipulation",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary manipulates a setting or parameter on communications channel in order to compromise its security. This can result in information exposure, insertion/removal of information from the communications stream, and/or potentially system compromise.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-217'})
SET capec.name = "Exploiting Incorrectly Configured SSL/TLS",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary takes advantage of incorrectly configured SSL/TLS communications that enables access to data intended to be encrypted. The adversary may also use this type of attack to inject commands or other traffic into the encrypted stream to cause compromise of either the client or server.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-218'})
SET capec.name = "Spoofing of UDDI/ebXML Messages",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker spoofs a UDDI, ebXML, or similar message in order to impersonate a service provider in an e-business transaction. UDDI, ebXML, and similar standards are used to identify businesses in e-business transactions. Among other things, they identify a particular participant, WSDL information for SOAP transactions, and supported communication protocols, including security protocols. By spoofing one of these messages an attacker could impersonate a legitimate business in a transaction or coul",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-219'})
SET capec.name = "XML Routing Detour Attacks",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker subverts an intermediate system used to process XML content and forces the intermediate to modify and/or re-route the processing of the content. XML Routing Detour Attacks are Adversary in the Middle type attacks (CAPEC-94). The attacker compromises or inserts an intermediate system in the processing of the XML message. For example, WS-Routing can be used to specify a series of nodes or intermediaries through which content is passed. If any of the intermediate nodes in this route are",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-22'})
SET capec.name = "Exploiting Trust in Client",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An attack of this type exploits vulnerabilities in client/server communication channel authentication and data integrity. It leverages the implicit trust a server places in the client, or more importantly, that which the server believes is the client. An attacker executes this type of attack by communicating directly with the server where the server believes it is communicating only with a valid client. There are numerous variations of this type of attack.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-220'})
SET capec.name = "Client-Server Protocol Manipulation",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary takes advantage of weaknesses in the protocol by which a client and server are communicating to perform unexpected actions. Communication protocols are necessary to transfer messages between client and server applications. Moreover, different protocols may be used for different types of interactions.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-221'})
SET capec.name = "Data Serialization External Entities Blowup",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack takes advantage of the entity replacement property of certain data serialization languages (e.g., XML, YAML, etc.) where the value of the replacement is a URI. A well-crafted file could have the entity refer to a URI that consumes a large amount of resources to create a denial of service condition. This can cause the system to either freeze, crash, or execute arbitrary code depending on the URI.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-222'})
SET capec.name = "iFrame Overlay",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In an iFrame overlay attack the victim is tricked into unknowingly initiating some action in one system while interacting with the UI from seemingly completely different system.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-224'})
SET capec.name = "Fingerprinting",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary compares output from a target system to known indicators that uniquely identify specific details about the target. Most commonly, fingerprinting is done to determine operating system and application versions. Fingerprinting can be done passively as well as actively. Fingerprinting by itself is not usually detrimental to the target. However, the information gathered through fingerprinting often enables an adversary to discover existing weaknesses in the target.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-226'})
SET capec.name = "Session Credential Falsification through Manipulation",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker manipulates an existing credential in order to gain access to a target application. Session credentials allow users to identify themselves to a service after an initial authentication without needing to resend the authentication information (usually a username and password) with every message. An attacker may be able to manipulate a credential sniffed from an existing connection in order to gain access to a target server.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-227'})
SET capec.name = "Sustained Client Engagement",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An adversary attempts to deny legitimate users access to a resource by continually engaging a specific resource in an attempt to keep the resource tied up as long as possible. The adversary's primary goal is not to crash or flood the target, which would alert defenders; rather it is to repeatedly perform actions or abuse algorithmic flaws such that a given resource is tied up and not available to a legitimate user. By carefully crafting a requests that keep the resource engaged through what is s",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-228'})
SET capec.name = "DTD Injection",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker injects malicious content into an application's DTD in an attempt to produce a negative technical impact. DTDs are used to describe how XML documents are processed. Certain malformed DTDs (for example, those with excessive entity expansion as described in CAPEC 197) can cause the XML parsers that process the DTDs to consume excessive resources resulting in resource depletion.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-229'})
SET capec.name = "Serialized Data Parameter Blowup",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack exploits certain serialized data parsers (e.g., XML, YAML, etc.) which manage data in an inefficient manner. The attacker crafts an serialized data file with multiple configuration parameters in the same dataset. In a vulnerable parser, this results in a denial of service condition where CPU resources are exhausted because of the parsing algorithm. The weakness being exploited is tied to parser implementation and not language specific.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-23'})
SET capec.name = "File Content Injection",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary poisons files with a malicious payload (targeting the file systems accessible by the target software), which may be passed through by standard channels such as via email, and standard web content like PDF and multimedia files. The adversary exploits known vulnerabilities or handling routines in the target processes, in order to exploit the host's trust in executing remote content, including binary files.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-230'})
SET capec.name = "Serialized Data with Nested Payloads",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "Applications often need to transform data in and out of a data format (e.g., XML and YAML) by using a parser. It may be possible for an adversary to inject data that may have an adverse effect on the parser when it is being processed. Many data format languages allow the definition of macro-like structures that can be used to simplify the creation of complex structures. By nesting these structures, causing the data to be repeatedly substituted, an adversary can cause the parser to consume more r",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-231'})
SET capec.name = "Oversized Serialized Data Payloads",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary injects oversized serialized data payloads into a parser during data processing to produce adverse effects upon the parser such as exhausting system resources and arbitrary code execution.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-233'})
SET capec.name = "Privilege Escalation",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An adversary exploits a weakness enabling them to elevate their privilege and perform an action that they are not supposed to be authorized to perform.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-234'})
SET capec.name = "Hijacking a privileged process",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary gains control of a process that is assigned elevated privileges in order to execute arbitrary code with those privileges. Some processes are assigned elevated privileges on an operating system, usually through association with a particular user, group, or role. If an attacker can hijack this process, they will be able to assume its level of privilege in order to execute their own code.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-235'})
SET capec.name = "DEPRECATED: Implementing a callback to system routine (old AWT Queue)",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated. Please refer to CAPEC:30 - Hijacking a Privileged Thread of Execution.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-236'})
SET capec.name = "DEPRECATED: Catching exception throw/signal from privileged block",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it did not have enough distinction from CAPEC-30 : Hijacking a Privileged Thread of Execution. Please refer to CAPEC-30 moving forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-237'})
SET capec.name = "Escaping a Sandbox by Calling Code in Another Language",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "The attacker may submit malicious code of another language to obtain access to privileges that were not intentionally exposed by the sandbox, thus escaping the sandbox. For instance, Java code cannot perform unsafe operations, such as modifying arbitrary memory locations, due to restrictions placed on it by the Byte code Verifier and the JVM. If allowed, Java code can call directly into native C code, which may perform unsafe operations, such as call system calls and modify arbitrary memory loca",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-238'})
SET capec.name = "DEPRECATED: Using URL/codebase / G.A.C. (code source) to convince sandbox of privilege",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it did not appear to be a valid attack pattern.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-239'})
SET capec.name = "DEPRECATED: Subversion of Authorization Checks: Cache Filtering, Programmatic Security, etc.",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it did not contain any content and did not serve any useful purpose. Please refer to \"CAPEC-207: removing Important Client Functionality\" going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-24'})
SET capec.name = "Filter Failure through Buffer Overflow",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack, the idea is to cause an active filter to fail by causing an oversized transaction. An attacker may try to feed overly long input strings to the program in an attempt to overwhelm the filter (by causing a buffer overflow) and hoping that the filter does not fail securely (i.e. the user input is let into the system unfiltered).",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-240'})
SET capec.name = "Resource Injection",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary exploits weaknesses in input validation by manipulating resource identifiers enabling the unintended modification or specification of a resource.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-241'})
SET capec.name = "DEPRECATED: Code Injection",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of the existing attack pattern \"CAPEC-242 : Code Injection\". Please refer to this other CAPEC going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-242'})
SET capec.name = "Code Injection",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary exploits a weakness in input validation on the target to inject new code into that which is currently executing. This differs from code inclusion in that code inclusion involves the addition or replacement of a reference to a code file, which is subsequently loaded by the target and used as part of the code of some application.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-243'})
SET capec.name = "XSS Targeting HTML Attributes",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary inserts commands to perform cross-site scripting (XSS) actions in HTML attributes. Many filters do not adequately sanitize attributes against the presence of potentially dangerous commands even if they adequately sanitize tags. For example, dangerous expressions could be inserted into a style attribute in an anchor tag, resulting in the execution of malicious code when the resulting page is rendered. If a victim is tricked into viewing the rendered page the attack proceeds like a no",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-244'})
SET capec.name = "XSS Targeting URI Placeholders",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attack of this type exploits the ability of most browsers to interpret \"data\", \"javascript\" or other URI schemes as client-side executable content placeholders. This attack consists of passing a malicious URI in an anchor tag HREF attribute or any other similar attributes in other HTML tags. Such malicious URI contains, for example, a base64 encoded HTML content with an embedded cross-site scripting payload. The attack is executed when the browser interprets the malicious content i.e., for ex",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-245'})
SET capec.name = "XSS Using Doubled Characters",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "The adversary bypasses input validation by using doubled characters in order to perform a cross-site scripting attack. Some filters fail to recognize dangerous sequences if they are preceded by repeated characters. For example, by doubling the < before a script command, (<<script or %3C%3script using URI encoding) the filters of some web applications may fail to recognize the presence of a script tag. If the targeted server is vulnerable to this type of bypass, the adversary can create a crafted",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-246'})
SET capec.name = "DEPRECATED: XSS Using Flash",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This pattern has been deprecated as it is covered by a chaining relationship between CAPEC-174: Flash Parameter Injection and CAPEC-591: Stored XSS. Please refer to these CAPECs going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-247'})
SET capec.name = "XSS Using Invalid Characters",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary inserts invalid characters in identifiers to bypass application filtering of input. Filters may not scan beyond invalid characters but during later stages of processing content that follows these invalid characters may still be processed. This allows the adversary to sneak prohibited commands past filters and perform normally prohibited operations. Invalid characters may include null, carriage return, line feed or tab in an identifier. Successful bypassing of the filter can result i",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-248'})
SET capec.name = "Command Injection",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary looking to execute a command of their choosing, injects new items into an existing command thus modifying interpretation away from what was intended. Commands in this context are often standalone strings that are interpreted by a downstream component and cause specific responses. This type of attack is possible when untrusted values are used to build these command strings. Weaknesses in input validation or command construction can enable the attack and lead to successful exploitatio",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-249'})
SET capec.name = "DEPRECATED: Linux Terminal Injection",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is covered by \"CAPEC-40 : Manipulating Writeable Terminal Devices\". Please refer to this CAPEC going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-25'})
SET capec.name = "Forced Deadlock",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "The adversary triggers and exploits a deadlock condition in the target software to cause a denial of service. A deadlock can occur when two or more competing actions are waiting for each other to finish, and thus neither ever does. Deadlock conditions can be difficult to detect.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-250'})
SET capec.name = "XML Injection",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker utilizes crafted XML user-controllable input to probe, attack, and inject data into the XML database, using techniques similar to SQL injection. The user-controllable input can allow for unauthorized viewing of data, bypassing authentication or the front-end application for direct XML database access, and possibly altering database information.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-251'})
SET capec.name = "Local Code Inclusion",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "The attacker forces an application to load arbitrary code files from the local machine. The attacker could use this to try to load old versions of library files that have known vulnerabilities, to load files that the attacker placed on the local machine during a prior attack, or to otherwise change the functionality of the targeted application in unexpected ways.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-252'})
SET capec.name = "PHP Local File Inclusion",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "The attacker loads and executes an arbitrary local PHP file on a target machine. The attacker could use this to try to load old versions of PHP files that have known vulnerabilities, to load PHP files that the attacker placed on the local machine during a prior attack, or to otherwise change the functionality of the targeted application in unexpected ways.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-253'})
SET capec.name = "Remote Code Inclusion",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "The attacker forces an application to load arbitrary code files from a remote location. The attacker could use this to try to load old versions of library files that have known vulnerabilities, to load malicious files that the attacker placed on the remote machine, or to otherwise change the functionality of the targeted application in unexpected ways.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-254'})
SET capec.name = "DEPRECATED: DTD Injection in a SOAP Message",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This pattern has been deprecated as it was determined to be an unnecessary layer of abstraction. Please refer to the pattern CAPEC-228 : DTD Injection going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-256'})
SET capec.name = "SOAP Array Overflow",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker sends a SOAP request with an array whose actual length exceeds the length indicated in the request. If the server processing the transmission naively trusts the specified size, then an attacker can intentionally understate the size of the array, possibly resulting in a buffer overflow if the server attempts to read the entire data set into the memory it allocated for a smaller array.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-257'})
SET capec.name = "DEPRECATED: Abuse of Transaction Data Structure",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it was deemed not to be a legitimate attack pattern.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-258'})
SET capec.name = "DEPRECATED: Passively Sniffing and Capturing Application Code Bound for an Authorized Client During Dynamic Update",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of the existing attack pattern \"CAPEC-65 : Sniff Application Code\". Please refer to this other CAPEC going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-259'})
SET capec.name = "DEPRECATED: Passively Sniffing and Capturing Application Code Bound for an Authorized Client During Patching",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of the existing attack pattern \"CAPEC-65 : Sniff Application Code\". Please refer to this other CAPEC going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-26'})
SET capec.name = "Leveraging Race Conditions",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "The adversary targets a race condition occurring when multiple processes access and manipulate the same resource concurrently, and the outcome of the execution depends on the particular order in which the access takes place. The adversary can leverage a race condition by \"running the race\", modifying the resource and modifying the normal execution flow. For instance, a race condition can occur while accessing a file: the adversary can trick the system by replacing the original file with their ve",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-260'})
SET capec.name = "DEPRECATED: Passively Sniffing and Capturing Application Code Bound for an Authorized Client During Initial Distribution",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of the existing attack pattern \"CAPEC-65 : Sniff Application Code\". Please refer to this other CAPEC going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-261'})
SET capec.name = "Fuzzing for garnering other adjacent user/sensitive data",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary who is authorized to send queries to a target sends variants of expected queries in the hope that these modified queries might return information (directly or indirectly through error logs) beyond what the expected set of queries should provide.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-263'})
SET capec.name = "Force Use of Corrupted Files",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This describes an attack where an application is forced to use a file that an attacker has corrupted. The result is often a denial of service caused by the application being unable to process the corrupted file, but other results, including the disabling of filters or access controls (if the application fails in an unsafe way rather than failing by locking down) or buffer overflows are possible.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-264'})
SET capec.name = "DEPRECATED: Environment Variable Manipulation",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of the existing attack pattern \"CAPEC-13 : Subverting Environment Variable Values\". Please refer to this other CAPEC going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-265'})
SET capec.name = "DEPRECATED: Global variable manipulation",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of the existing attack pattern \"CAPEC-77 : Manipulating User-Controlled Variables\". Please refer to this other CAPEC going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-266'})
SET capec.name = "DEPRECATED: Manipulate Canonicalization",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-267'})
SET capec.name = "Leverage Alternate Encoding",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary leverages the possibility to encode potentially harmful input or content used by applications such that the applications are ineffective at validating this encoding standard.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-268'})
SET capec.name = "Audit Log Manipulation",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "The attacker injects, manipulates, deletes, or forges malicious log entries into the log file, in an attempt to mislead an audit of the log file or cover tracks of an attack. Due to either insufficient access controls of the log files or the logging mechanism, the attacker is able to perform such actions.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-269'})
SET capec.name = "DEPRECATED: Registry Manipulation",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This pattern has been deprecated as it was determined to be a duplicate of another pattern. Please refer to the pattern CAPEC-203 : Manipulate Application Registry Values going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-27'})
SET capec.name = "Leveraging Race Conditions via Symbolic Links",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack leverages the use of symbolic links (Symlinks) in order to write to sensitive files. An attacker can create a Symlink link to a target file not otherwise accessible to them. When the privileged program tries to create a temporary file with the same name as the Symlink link, it will actually write to the target file pointed to by the attackers' Symlink link. If the attacker can insert malicious content in the temporary file they will be writing to the sensitive file by using the Symli",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-270'})
SET capec.name = "Modification of Registry Run Keys",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary adds a new entry to the \"run keys\" in the Windows registry so that an application of their choosing is executed when a user logs in. In this way, the adversary can get their executable to operate and run on the target system with the authorized user's level of permissions. This attack is a good way for an adversary to run persistent spyware on a user's machine, such as a keylogger.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-271'})
SET capec.name = "Schema Poisoning",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary corrupts or modifies the content of a schema for the purpose of undermining the security of the target. Schemas provide the structure and content definitions for resources used by an application. By replacing or modifying a schema, the adversary can affect how the application handles or interprets a resource, often leading to possible denial of service, entering into an unexpected state, or recording incomplete data.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-272'})
SET capec.name = "Protocol Manipulation",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An adversary subverts a communications protocol to perform an attack. This type of attack can allow an adversary to impersonate others, discover sensitive information, control the outcome of a session, or perform other attacks. This type of attack targets invalid assumptions that may be inherent in implementers of the protocol, incorrect implementations of the protocol, or vulnerabilities in the protocol itself.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-273'})
SET capec.name = "HTTP Response Smuggling",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-274'})
SET capec.name = "HTTP Verb Tampering",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker modifies the HTTP Verb (e.g. GET, PUT, TRACE, etc.) in order to bypass access restrictions. Some web environments allow administrators to restrict access based on the HTTP Verb used with requests. However, attackers can often provide a different HTTP Verb, or even provide a random string as a verb in order to bypass these protections. This allows the attacker to access data that should otherwise be protected.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-275'})
SET capec.name = "DNS Rebinding",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary serves content whose IP address is resolved by a DNS server that the adversary controls. After initial contact by a web browser (or similar client), the adversary changes the IP address to which its name resolves, to an address within the target organization that is not publicly accessible. This allows the web browser to examine this internal address on behalf of the adversary.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-276'})
SET capec.name = "Inter-component Protocol Manipulation",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "Inter-component protocols are used to communicate between different software and hardware modules within a single computer. Common examples are: interrupt signals and data pipes. Subverting the protocol can allow an adversary to impersonate others, discover sensitive information, control the outcome of a session, or perform other attacks. This type of attack targets invalid assumptions that may be inherent in implementers of the protocol, incorrect implementations of the protocol, or vulnerabili",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-277'})
SET capec.name = "Data Interchange Protocol Manipulation",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "Data Interchange Protocols are used to transmit structured data between entities. These protocols are often specific to a particular domain (B2B: purchase orders, invoices, transport logistics and waybills, medical records). They are often, but not always, XML-based. Subverting the protocol can allow an adversary to impersonate others, discover sensitive information, control the outcome of a session, or perform other attacks. This type of attack targets invalid assumptions that may be inherent i",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-278'})
SET capec.name = "Web Services Protocol Manipulation",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary manipulates a web service related protocol to cause a web application or service to react differently than intended. This can either be performed through the manipulation of call parameters to include unexpected values, or by changing the called function to one that should normally be restricted or limited. By leveraging this pattern of attack, the adversary is able to gain access to data or resources normally restricted, or to cause the application or service to crash.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-279'})
SET capec.name = "SOAP Manipulation",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Simple Object Access Protocol (SOAP) is used as a communication protocol between a client and server to invoke web services on the server. It is an XML-based protocol, and therefore suffers from many of the same shortcomings as other XML-based protocols. Adversaries can make use of these shortcomings and manipulate the content of SOAP paramters, leading to undesirable behavior on the server and allowing the adversary to carry out a number of further attacks.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-28'})
SET capec.name = "Fuzzing",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "In this attack pattern, the adversary leverages fuzzing to try to identify weaknesses in the system. Fuzzing is a software security and functionality testing method that feeds randomly constructed input to the system and looks for an indication that a failure in response to that input has occurred. Fuzzing treats the system as a black box and is totally free from any preconceptions or assumptions about the system. Fuzzing can help an attacker discover certain assumptions made about user input in",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-280'})
SET capec.name = "DEPRECATED: SOAP Parameter Tampering",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as its contents have been included in CAPEC-279 : SOAP Manipulation. Please refer to this other pattern going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-285'})
SET capec.name = "ICMP Echo Request Ping",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary sends out an ICMP Type 8 Echo Request, commonly known as a 'Ping', in order to determine if a target system is responsive. If the request is not blocked by a firewall or ACL, the target host will respond with an ICMP Type 0 Echo Reply datagram. This type of exchange is usually referred to as a 'Ping' due to the Ping utility present in almost all operating systems. Ping, as commonly implemented, allows a user to test for alive hosts, measure round-trip time, and measure the percentag",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-287'})
SET capec.name = "TCP SYN Scan",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary uses a SYN scan to determine the status of ports on the remote target. SYN scanning is the most common type of port scanning that is used because of its many advantages and few drawbacks. As a result, novice attackers tend to overly rely on the SYN scan while performing system reconnaissance. As a scanning method, the primary advantages of SYN scanning are its universality and speed.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-288'})
SET capec.name = "DEPRECATED: ICMP Echo Request Ping",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of the existing attack pattern \"CAPEC-285\". Please refer to this other CAPEC going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-289'})
SET capec.name = "DEPRECATED: Infrastructure-based footprinting",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it was determined to be an unnecessary layer of abstraction. Please refer to the meta level pattern CAPEC-169 : going forward, or to any of its children patterns.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-29'})
SET capec.name = "Leveraging Time-of-Check and Time-of-Use (TOCTOU) Race Conditions",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "This attack targets a race condition occurring between the time of check (state) for a resource and the time of use of a resource. A typical example is file access. The adversary can leverage a file access race condition by \"running the race\", meaning that they would modify the resource between the first time the target program accesses the file and the time the target program uses the file. During that period of time, the adversary could replace or modify the file, causing the application to be",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-290'})
SET capec.name = "Enumerate Mail Exchange (MX) Records",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary enumerates the MX records for a given via a DNS query. This type of information gathering returns the names of mail servers on the network. Mail servers are often not exposed to the Internet but are located within the DMZ of a network protected by a firewall. A side effect of this configuration is that enumerating the MX records for an organization my reveal the IP address of the firewall or possibly other internal systems. Attackers often resort to MX record enumeration when a DNS ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-291'})
SET capec.name = "DNS Zone Transfers",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An attacker exploits a DNS misconfiguration that permits a ZONE transfer. Some external DNS servers will return a list of IP address and valid hostnames. Under certain conditions, it may even be possible to obtain Zone data about the organization's internal network. When successful the attacker learns valuable information about the topology of the target organization, including information about particular servers, their role within the IT structure, and possibly information about the operating ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-292'})
SET capec.name = "Host Discovery",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary sends a probe to an IP address to determine if the host is alive. Host discovery is one of the earliest phases of network reconnaissance. The adversary usually starts with a range of IP addresses belonging to a target network and uses various methods to determine if a host is present at that IP address. Host discovery is usually referred to as 'Ping' scanning using a sonar analogy. The goal is to send a packet through to the IP address and solicit a response from the host. As such, ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-293'})
SET capec.name = "Traceroute Route Enumeration",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary uses a traceroute utility to map out the route which data flows through the network in route to a target destination. Tracerouting can allow the adversary to construct a working topology of systems and routers by listing the systems through which data passes through on their way to the targeted machine. This attack can return varied results depending upon the type of traceroute that is performed. Traceroute works by sending packets to a target while incrementing the Time-to-Live fie",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-294'})
SET capec.name = "ICMP Address Mask Request",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary sends an ICMP Type 17 Address Mask Request to gather information about a target's networking configuration. ICMP Address Mask Requests are defined by RFC-950, \"Internet Standard Subnetting Procedure.\" An Address Mask Request is an ICMP type 17 message that triggers a remote system to respond with a list of its related subnets, as well as its default gateway and broadcast address via an ICMP type 18 Address Mask Reply datagram. Gathering this type of information helps the adversary p",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-295'})
SET capec.name = "Timestamp Request",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This pattern of attack leverages standard requests to learn the exact time associated with a target system. An adversary may be able to use the timestamp returned from the target to attack time-based security algorithms, such as random number generators, or time-based authentication mechanisms.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-296'})
SET capec.name = "ICMP Information Request",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary sends an ICMP Information Request to a host to determine if it will respond to this deprecated mechanism. ICMP Information Requests are a deprecated message type. Information Requests were originally used for diskless machines to automatically obtain their network configuration, but this message type has been superseded by more robust protocol implementations like DHCP.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-297'})
SET capec.name = "TCP ACK Ping",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary sends a TCP segment with the ACK flag set to a remote host for the purpose of determining if the host is alive. This is one of several TCP 'ping' types. The RFC 793 expected behavior for a service is to respond with a RST 'reset' packet to any unsolicited ACK segment that is not part of an existing connection. So by sending an ACK segment to a port, the adversary can identify that the host is alive by looking for a RST packet. Typically, a remote server will respond with a RST regar",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-298'})
SET capec.name = "UDP Ping",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary sends a UDP datagram to the remote host to determine if the host is alive. If a UDP datagram is sent to an open UDP port there is very often no response, so a typical strategy for using a UDP ping is to send the datagram to a random high port on the target. The goal is to solicit an 'ICMP port unreachable' message from the target, indicating that the host is alive. UDP pings are useful because some firewalls are not configured to block UDP datagrams sent to strange or typically unus",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-299'})
SET capec.name = "TCP SYN Ping",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary uses TCP SYN packets as a means towards host discovery. Typical RFC 793 behavior specifies that when a TCP port is open, a host must respond to an incoming SYN \"synchronize\" packet by completing stage two of the 'three-way handshake' - by sending an SYN/ACK in response. When a port is closed, RFC 793 behavior is to respond with a RST \"reset\" packet. This behavior can be used to 'ping' a target to see if it is alive by sending a TCP SYN packet to a port and then looking for a RST or ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-3'})
SET capec.name = "Using Leading 'Ghost' Character Sequences to Bypass Input Filters",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Some APIs will strip certain leading characters from a string of parameters. An adversary can intentionally introduce leading \"ghost\" characters (extra characters that don't affect the validity of the request at the API layer) that enable the input to pass the filters and therefore process the adversary's input. This occurs when the targeted API will accept input data in several syntactic forms and interpret it in the equivalent semantic way, while the filter does not take into account the full ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-30'})
SET capec.name = "Hijacking a Privileged Thread of Execution",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary hijacks a privileged thread of execution by injecting malicious code into a running process. By using a privleged thread to do their bidding, adversaries can evade process-based detection that would stop an attack that creates a new process. This can lead to an adversary gaining access to the process's memory and can also enable elevated privileges. The most common way to perform this attack is by suspending an existing thread and manipulating its memory.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-300'})
SET capec.name = "Port Scanning",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary uses a combination of techniques to determine the state of the ports on a remote target. Any service or application available for TCP or UDP networking will have a port open for communications over the network.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-301'})
SET capec.name = "TCP Connect Scan",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary uses full TCP connection attempts to determine if a port is open on the target system. The scanning process involves completing a 'three-way handshake' with a remote port, and reports the port as closed if the full handshake cannot be established. An advantage of TCP connect scanning is that it works against any TCP/IP stack.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-302'})
SET capec.name = "TCP FIN Scan",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary uses a TCP FIN scan to determine if ports are closed on the target machine. This scan type is accomplished by sending TCP segments with the FIN bit set in the packet header. The RFC 793 expected behavior is that any TCP segment with an out-of-state Flag sent to an open port is discarded, whereas segments with out-of-state flags sent to closed ports should be handled with a RST in response. This behavior should allow the adversary to scan for closed ports by sending certain types of ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-303'})
SET capec.name = "TCP Xmas Scan",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary uses a TCP XMAS scan to determine if ports are closed on the target machine. This scan type is accomplished by sending TCP segments with all possible flags set in the packet header, generating packets that are illegal based on RFC 793. The RFC 793 expected behavior is that any TCP segment with an out-of-state Flag sent to an open port is discarded, whereas segments with out-of-state flags sent to closed ports should be handled with a RST in response. This behavior should allow an at",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-304'})
SET capec.name = "TCP Null Scan",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary uses a TCP NULL scan to determine if ports are closed on the target machine. This scan type is accomplished by sending TCP segments with no flags in the packet header, generating packets that are illegal based on RFC 793. The RFC 793 expected behavior is that any TCP segment with an out-of-state Flag sent to an open port is discarded, whereas segments with out-of-state flags sent to closed ports should be handled with a RST in response. This behavior should allow an attacker to scan",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-305'})
SET capec.name = "TCP ACK Scan",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary uses TCP ACK segments to gather information about firewall or ACL configuration. The purpose of this type of scan is to discover information about filter configurations rather than port state. This type of scanning is rarely useful alone, but when combined with SYN scanning, gives a more complete picture of the type of firewall rules that are present.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-306'})
SET capec.name = "TCP Window Scan",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary engages in TCP Window scanning to analyze port status and operating system type. TCP Window scanning uses the ACK scanning method but examine the TCP Window Size field of response RST packets to make certain inferences. While TCP Window Scans are fast and relatively stealthy, they work against fewer TCP stack implementations than any other type of scan. Some operating systems return a positive TCP window size when a RST packet is sent from an open port, and a negative value when the",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-307'})
SET capec.name = "TCP RPC Scan",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary scans for RPC services listing on a Unix/Linux host.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-308'})
SET capec.name = "UDP Scan",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary engages in UDP scanning to gather information about UDP port status on the target system. UDP scanning methods involve sending a UDP datagram to the target port and looking for evidence that the port is closed. Open UDP ports usually do not respond to UDP datagrams as there is no stateful mechanism within the protocol that requires building or establishing a session. Responses to UDP datagrams are therefore application specific and cannot be relied upon as a method of detecting an o",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-309'})
SET capec.name = "Network Topology Mapping",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary engages in scanning activities to map network nodes, hosts, devices, and routes. Adversaries usually perform this type of network reconnaissance during the early stages of attack against an external network. Many types of scanning utilities are typically employed, including ICMP tools, network mappers, port scanners, and route testing utilities such as traceroute.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-31'})
SET capec.name = "Accessing/Intercepting/Modifying HTTP Cookies",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack relies on the use of HTTP Cookies to store credentials, state information and other critical data on client systems. There are several different forms of this attack. The first form of this attack involves accessing HTTP Cookies to mine for potentially sensitive data contained therein. The second form involves intercepting this data as it is transmitted from client to server. This intercepted information is then used by the adversary to impersonate the remote user/session. The third ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-310'})
SET capec.name = "Scanning for Vulnerable Software",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker engages in scanning activity to find vulnerable software versions or types, such as operating system versions or network services. Vulnerable or exploitable network configurations, such as improperly firewalled systems, or misconfigured systems in the DMZ or external network, provide windows of opportunity for an attacker. Common types of vulnerable software include unpatched operating systems or services (e.g FTP, Telnet, SMTP, SNMP) running on open ports that the attacker has ident",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-311'})
SET capec.name = "DEPRECATED: OS Fingerprinting",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This pattern has been deprecated as it was determined to be an unnecessary layer of abstraction. Please refer to the standard level patterns CAPEC-312 : Active OS Fingerprinting or CAPEC-313 : Passive OS Fingerprinting going forward, or to any of the detailed patterns that are children of them.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-312'})
SET capec.name = "Active OS Fingerprinting",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary engages in activity to detect the operating system or firmware version of a remote target by interrogating a device, server, or platform with a probe designed to solicit behavior that will reveal information about the operating systems or firmware in the environment. Operating System detection is possible because implementations of common protocols (Such as IP or TCP) differ in distinct ways. While the implementation differences are not sufficient to 'break' compatibility with the p",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-313'})
SET capec.name = "Passive OS Fingerprinting",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary engages in activity to detect the version or type of OS software in a an environment by passively monitoring communication between devices, nodes, or applications. Passive techniques for operating system detection send no actual probes to a target, but monitor network or client-server communication between nodes in order to identify operating systems based on observed behavior as compared to a database of known signatures or values. While passive OS fingerprinting is not usually as ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-314'})
SET capec.name = "DEPRECATED: IP Fingerprinting Probes",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This pattern has been deprecated as it was determined to be an unnecessary layer of abstraction. Please refer to the standard level pattern CAPEC-312 : Active OS Fingerprinting going forward, or to any of the detailed patterns that children of CAPEC-312.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-315'})
SET capec.name = "DEPRECATED: TCP/IP Fingerprinting Probes",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This pattern has been deprecated as it was determined to be an unnecessary layer of abstraction. Please refer to the standard level pattern CAPEC-312 : Active OS Fingerprinting going forward, or to any of the detailed patterns that are children of CAPEC-312.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-316'})
SET capec.name = "DEPRECATED: ICMP Fingerprinting Probes",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This pattern has been deprecated as it was determined to be an unnecessary layer of abstraction. Please refer to the standard level pattern CAPEC-312 : Active OS Fingerprinting going forward, or to any of the detailed patterns that are children of CAPEC-312.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-317'})
SET capec.name = "IP ID Sequencing Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This OS fingerprinting probe analyzes the IP 'ID' field sequence number generation algorithm of a remote host. Operating systems generate IP 'ID' numbers differently, allowing an attacker to identify the operating system of the host by examining how is assigns ID numbers when generating response packets. RFC 791 does not specify how ID numbers are chosen or their ranges, so ID sequence generation differs from implementation to implementation. There are two kinds of IP 'ID' sequence number analys",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-318'})
SET capec.name = "IP 'ID' Echoed Byte-Order Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This OS fingerprinting probe tests to determine if the remote host echoes back the IP 'ID' value from the probe packet. An attacker sends a UDP datagram with an arbitrary IP 'ID' value to a closed port on the remote host to observe the manner in which this bit is echoed back in the ICMP error message. The identification field (ID) is typically utilized for reassembling a fragmented packet. Some operating systems or router firmware reverse the bit order of the ID field when echoing the IP Header ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-319'})
SET capec.name = "IP (DF) 'Don't Fragment Bit' Echoing Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This OS fingerprinting probe tests to determine if the remote host echoes back the IP 'DF' (Don't Fragment) bit in a response packet. An attacker sends a UDP datagram with the DF bit set to a closed port on the remote host to observe whether the 'DF' bit is set in the response packet. Some operating systems will echo the bit in the ICMP error message while others will zero out the bit in the response packet.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-32'})
SET capec.name = "XSS Through HTTP Query Strings",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary embeds malicious script code in the parameters of an HTTP query string and convinces a victim to submit the HTTP request that contains the query string to a vulnerable web application. The web application then procedes to use the values parameters without properly validation them first and generates the HTML code that will be executed by the victim's browser.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-320'})
SET capec.name = "TCP Timestamp Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This OS fingerprinting probe examines the remote server's implementation of TCP timestamps. Not all operating systems implement timestamps within the TCP header, but when timestamps are used then this provides the attacker with a means to guess the operating system of the target. The attacker begins by probing any active TCP service in order to get response which contains a TCP timestamp. Different Operating systems update the timestamp value using different intervals. This type of analysis is m",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-321'})
SET capec.name = "TCP Sequence Number Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This OS fingerprinting probe tests the target system's assignment of TCP sequence numbers. One common way to test TCP Sequence Number generation is to send a probe packet to an open port on the target and then compare the how the Sequence Number generated by the target relates to the Acknowledgement Number in the probe packet. Different operating systems assign Sequence Numbers differently, so a fingerprint of the operating system can be obtained by categorizing the relationship between the ackn",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-322'})
SET capec.name = "TCP (ISN) Greatest Common Divisor Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This OS fingerprinting probe sends a number of TCP SYN packets to an open port of a remote machine. The Initial Sequence Number (ISN) in each of the SYN/ACK response packets is analyzed to determine the smallest number that the target host uses when incrementing sequence numbers. This information can be useful for identifying an operating system because particular operating systems and versions increment sequence numbers using different values. The result of the analysis is then compared against",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-323'})
SET capec.name = "TCP (ISN) Counter Rate Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This OS detection probe measures the average rate of initial sequence number increments during a period of time. Sequence numbers are incremented using a time-based algorithm and are susceptible to a timing analysis that can determine the number of increments per unit time. The result of this analysis is then compared against a database of operating systems and versions to determine likely operation system matches.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-324'})
SET capec.name = "TCP (ISN) Sequence Predictability Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This type of operating system probe attempts to determine an estimate for how predictable the sequence number generation algorithm is for a remote host. Statistical techniques, such as standard deviation, can be used to determine how predictable the sequence number generation is for a system. This result can then be compared to a database of operating system behaviors to determine a likely match for operating system and version.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-325'})
SET capec.name = "TCP Congestion Control Flag (ECN) Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This OS fingerprinting probe checks to see if the remote host supports explicit congestion notification (ECN) messaging. ECN messaging was designed to allow routers to notify a remote host when signal congestion problems are occurring. Explicit Congestion Notification messaging is defined by RFC 3168. Different operating systems and versions may or may not implement ECN notifications, or may respond uniquely to particular ECN flag types.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-326'})
SET capec.name = "TCP Initial Window Size Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This OS fingerprinting probe checks the initial TCP Window size. TCP stacks limit the range of sequence numbers allowable within a session to maintain the \"connected\" state within TCP protocol logic. The initial window size specifies a range of acceptable sequence numbers that will qualify as a response to an ACK packet within a session. Various operating systems use different Initial window sizes. The initial window size can be sampled by establishing an ordinary TCP connection.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-327'})
SET capec.name = "TCP Options Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This OS fingerprinting probe analyzes the type and order of any TCP header options present within a response segment. Most operating systems use unique ordering and different option sets when options are present. RFC 793 does not specify a required order when options are present, so different implementations use unique ways of ordering or structuring TCP options. TCP options can be generated by ordinary TCP traffic.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-328'})
SET capec.name = "TCP 'RST' Flag Checksum Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This OS fingerprinting probe performs a checksum on any ASCII data contained within the data portion or a RST packet. Some operating systems will report a human-readable text message in the payload of a 'RST' (reset) packet when specific types of connection errors occur. RFC 1122 allows text payloads within reset packets but not all operating systems or routers implement this functionality.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-329'})
SET capec.name = "ICMP Error Message Quoting Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary uses a technique to generate an ICMP Error message (Port Unreachable, Destination Unreachable, Redirect, Source Quench, Time Exceeded, Parameter Problem) from a target and then analyze the amount of data returned or \"Quoted\" from the originating request that generated the ICMP error message.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-33'})
SET capec.name = "HTTP Request Smuggling",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-330'})
SET capec.name = "ICMP Error Message Echoing Integrity Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary uses a technique to generate an ICMP Error message (Port Unreachable, Destination Unreachable, Redirect, Source Quench, Time Exceeded, Parameter Problem) from a target and then analyze the integrity of data returned or \"Quoted\" from the originating request that generated the error message.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-331'})
SET capec.name = "ICMP IP Total Length Field Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary sends a UDP packet to a closed port on the target machine to solicit an IP Header's total length field value within the echoed 'Port Unreachable\" error message. This type of behavior is useful for building a signature-base of operating system responses, particularly when error messages contain other types of information that is useful identifying specific operating system responses.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-332'})
SET capec.name = "ICMP IP 'ID' Field Error Message Probe",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary sends a UDP datagram having an assigned value to its internet identification field (ID) to a closed port on a target to observe the manner in which this bit is echoed back in the ICMP error message. This allows the attacker to construct a fingerprint of specific OS behaviors.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-34'})
SET capec.name = "HTTP Response Splitting",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-35'})
SET capec.name = "Leverage Executable Code in Non-Executable Files",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attack of this type exploits a system's trust in configuration and resource files. When the executable loads the resource (such as an image file or configuration file) the attacker has modified the file to either execute malicious code directly or manipulate the target process (e.g. application server) to execute based on the malicious configuration parameters. Since systems are increasingly interrelated mashing up resources from local and remote sources the possibility of this attack occurri",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-36'})
SET capec.name = "Using Unpublished Interfaces or Functionality",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary searches for and invokes interfaces or functionality that the target system designers did not intend to be publicly available. If interfaces fail to authenticate requests, the attacker may be able to invoke functionality they are not authorized for.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-37'})
SET capec.name = "Retrieve Embedded Sensitive Data",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker examines a target system to find sensitive data that has been embedded within it. This information can reveal confidential contents, such as account numbers or individual keys/credentials that can be used as an intermediate step in a larger attack.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-38'})
SET capec.name = "Leveraging/Manipulating Configuration File Search Paths",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This pattern of attack sees an adversary load a malicious resource into a program's standard path so that when a known command is executed then the system instead executes the malicious component. The adversary can either modify the search path a program uses, like a PATH variable or classpath, or they can manipulate resources on the path to point to their malicious components. J2EE applications and other component based applications that are built from multiple binaries can have very long list ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-383'})
SET capec.name = "Harvesting Information via API Event Monitoring",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary hosts an event within an application framework and then monitors the data exchanged during the course of the event for the purpose of harvesting any important data leaked during the transactions. One example could be harvesting lists of usernames or userIDs for the purpose of sending spam messages to those users. One example of this type of attack involves the adversary creating an event within the sub-application. Assume the adversary hosts a \"virtual sale\" of rare items. As other ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-384'})
SET capec.name = "Application API Message Manipulation via Man-in-the-Middle",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker manipulates either egress or ingress data from a client within an application framework in order to change the content of messages. Performing this attack can allow the attacker to gain unauthorized privileges within the application, or conduct attacks such as phishing, deceptive strategies to spread malware, or traditional web-application attacks. The techniques require use of specialized software that allow the attacker to perform adversary-in-the-middle (CAPEC-94) communications b",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-385'})
SET capec.name = "Transaction or Event Tampering via Application API Manipulation",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker hosts or joins an event or transaction within an application framework in order to change the content of messages or items that are being exchanged. Performing this attack allows the attacker to manipulate content in such a way as to produce messages or content that look authentic but may contain deceptive links, substitute one item or another, spoof an existing item and conduct a false exchange, or otherwise change the amounts or identity of what is being exchanged. The techniques r",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-386'})
SET capec.name = "Application API Navigation Remapping",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker manipulates either egress or ingress data from a client within an application framework in order to change the destination and/or content of links/buttons displayed to a user within API messages. Performing this attack allows the attacker to manipulate content in such a way as to produce messages or content that looks authentic but contains links/buttons that point to an attacker controlled destination. Some applications make navigation remapping more difficult to detect because the ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-387'})
SET capec.name = "Navigation Remapping To Propagate Malicious Content",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary manipulates either egress or ingress data from a client within an application framework in order to change the content of messages and thereby circumvent the expected application logic.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-388'})
SET capec.name = "Application API Button Hijacking",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker manipulates either egress or ingress data from a client within an application framework in order to change the destination and/or content of buttons displayed to a user within API messages. Performing this attack allows the attacker to manipulate content in such a way as to produce messages or content that looks authentic but contains buttons that point to an attacker controlled destination.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-389'})
SET capec.name = "Content Spoofing Via Application API Manipulation",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker manipulates either egress or ingress data from a client within an application framework in order to change the content of messages. Performing this attack allows the attacker to manipulate content in such a way as to produce messages or content that look authentic but may contain deceptive links, spam-like content, or links to the attackers' code. In general, content-spoofing within an application API can be employed to stage many different types of attacks varied based on the attack",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-39'})
SET capec.name = "Manipulating Opaque Client-based Data Tokens",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "In circumstances where an application holds important data client-side in tokens (cookies, URLs, data files, and so forth) that data can be manipulated. If client or server-side application components reinterpret that data as authentication tokens or data (such as store item pricing or wallet information) then even opaquely manipulating that data may bear fruit for an Attacker. In this pattern an attacker undermines the assumption that client side tokens have been adequately protected from tampe",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-390'})
SET capec.name = "Bypassing Physical Security",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "Facilities often used layered models for physical security such as traditional locks, Electronic-based card entry systems, coupled with physical alarms. Hardware security mechanisms range from the use of computer case and cable locks as well as RFID tags for tracking computer assets. This layered approach makes it difficult for random physical security breaches to go unnoticed, but is less effective at stopping deliberate and carefully planned break-ins. Avoiding detection begins with evading bu",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-391'})
SET capec.name = "Bypassing Physical Locks",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker uses techniques and methods to bypass physical security measures of a building or facility. Physical locks may range from traditional lock and key mechanisms, cable locks used to secure laptops or servers, locks on server cases, or other such devices. Techniques such as lock bumping, lock forcing via snap guns, or lock picking can be employed to bypass those locks and gain access to the facilities or devices they protect, although stealth, evidence of tampering, and the integrity of ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-392'})
SET capec.name = "Lock Bumping",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker uses a bump key to force a lock on a building or facility and gain entry. Lock Bumping is the use of a special type of key that can be tapped or bumped to cause the pins within the lock to fall into temporary alignment, allowing the lock to be opened. Lock bumping allows an attacker to open a lock without having the correct key. A standard lock is secured by a set of internal pins that prevent the device from turning. Spring loaded driver pins push down on the key pins. When the corr",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-393'})
SET capec.name = "Lock Picking",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker uses lock picking tools and techniques to bypass the locks on a building or facility. Lock picking is the use of a special set of tools to manipulate the pins within a lock. Different sets of tools are required for each type of lock. Lock picking attacks have the advantage of being non-invasive in that if performed correctly the lock will not be damaged. A standard lock pin-and-tumbler lock is secured by a set of internal pins that prevent the tumbler device from turning. Spring load",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-394'})
SET capec.name = "Using a Snap Gun Lock to Force a Lock",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker uses a Snap Gun, also known as a Pick Gun, to force the lock on a building or facility. A Pick Gun is a special type of lock picking instrument that works on similar principles as lock bumping. A snap gun is a hand-held device with an attached metal pick. The metal pick strikes the pins within the lock, transferring motion from the key pins to the driver pins and forcing the lock into momentary alignment. A standard lock is secured by a set of internal pins that prevent the device fr",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-395'})
SET capec.name = "Bypassing Electronic Locks and Access Controls",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker exploits security assumptions to bypass electronic locks or other forms of access controls. Most attacks against electronic access controls follow similar methods but utilize different tools. Some electronic locks utilize magnetic strip cards, others employ RFID tags embedded within a card or badge, or may involve more sophisticated protections such as voice-print, thumb-print, or retinal biometrics. Magnetic Strip and RFID technologies are the most widespread because they are cost e",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-396'})
SET capec.name = "DEPRECATED: Bypassing Card or Badge-Based Systems",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it a generalization of CAPEC-397: Cloning Magnetic Strip Cards, CAPEC-398: Magnetic Strip Card Brute Force Attacks, CAPEC-399: Cloning RFID Cards or Chips and CAPEC-400: RFID Chip Deactivation or Destruction. Please refer to these CAPECs going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-397'})
SET capec.name = "Cloning Magnetic Strip Cards",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker duplicates the data on a Magnetic strip card (i.e. 'swipe card' or 'magstripe') to gain unauthorized access to a physical location or a person's private information. Magstripe cards encode data on a band of iron-based magnetic particles arrayed in a stripe along a rectangular card. Most magstripe card data formats conform to ISO standards 7810, 7811, 7813, 8583, and 4909. The primary advantage of magstripe technology is ease of encoding and portability, but this also renders magnetic",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-398'})
SET capec.name = "Magnetic Strip Card Brute Force Attacks",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary analyzes the data on two or more magnetic strip cards and is able to generate new cards containing valid sequences that allow unauthorized access and/or impersonation of individuals.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-399'})
SET capec.name = "Cloning RFID Cards or Chips",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker analyzes data returned by an RFID chip and uses this information to duplicate a RFID signal that responds identically to the target chip. In some cases RFID chips are used for building access control, employee identification, or as markers on products being delivered along a supply chain. Some organizations also embed RFID tags inside computer assets to trigger alarms if they are removed from particular rooms, zones, or buildings. Similar to Magnetic strip cards, RFID cards are susce",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-4'})
SET capec.name = "Using Alternative IP Address Encodings",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack relies on the adversary using unexpected formats for representing IP addresses. Networked applications may expect network location information in a specific format, such as fully qualified domains names (FQDNs), URL, IP address, or IP Address ranges. If the location information is not validated against a variety of different possible encodings and formats, the adversary can use an alternate format to bypass application access control.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-40'})
SET capec.name = "Manipulating Writeable Terminal Devices",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "This attack exploits terminal devices that allow themselves to be written to by other users. The attacker sends command strings to the target terminal device hoping that the target user will hit enter and thereby execute the malicious command with their privileges. The attacker can send the results (such as copying /etc/passwd) to a known directory and collect once the attack has succeeded.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-400'})
SET capec.name = "RFID Chip Deactivation or Destruction",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker uses methods to deactivate a passive RFID tag for the purpose of rendering the tag, badge, card, or object containing the tag unresponsive. RFID tags are used primarily for access control, inventory, or anti-theft devices. The purpose of attacking the RFID chip is to disable or damage the chip without causing damage to the object housing it.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-401'})
SET capec.name = "Physically Hacking Hardware",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary exploits a weakness in access control to gain access to currently installed hardware and precedes to implement changes or secretly replace a hardware component which undermines the system's integrity for the purpose of carrying out an attack.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-402'})
SET capec.name = "Bypassing ATA Password Security",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary exploits a weakness in ATA security on a drive to gain access to the information the drive contains without supplying the proper credentials. ATA Security is often employed to protect hard disk information from unauthorized access. The mechanism requires the user to type in a password before the BIOS is allowed access to drive contents. Some implementations of ATA security will accept the ATA command to update the password without the user having authenticated with the BIOS. This oc",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-404'})
SET capec.name = "DEPRECATED: Social Information Gathering Attacks",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it was deemed not to be a legitimate attack pattern. Please refer to CAPEC-118 : Collect and Analyze Information.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-405'})
SET capec.name = "DEPRECATED: Social Information Gathering via Research",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it was deemed not to be a legitimate attack pattern. Please refer to CAPEC-118 : Collect and Analyze Information.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-406'})
SET capec.name = "Dumpster Diving",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary cases an establishment and searches through trash bins, dumpsters, or areas where company information may have been accidentally discarded for information items which may be useful to the dumpster diver. The devastating nature of the items and/or information found can be anything from medical records, resumes, personal photos and emails, bank statements, account details or information about software, tech support logs and so much more, including hardware devices. By collecting this ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-407'})
SET capec.name = "Pretexting",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary engages in pretexting behavior to solicit information from target persons, or manipulate the target into performing some action that serves the adversary's interests. During a pretexting attack, the adversary creates an invented scenario, assuming an identity or role to persuade a targeted victim to release information or perform some action. It is more than just creating a lie; in some cases it can be creating a whole new identity and then using that identity to manipulate the rece",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-408'})
SET capec.name = "DEPRECATED: Information Gathering from Traditional Sources",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it was deemed not to be a legitimate attack pattern. Please refer to CAPEC-118 : Collect and Analyze Information.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-409'})
SET capec.name = "DEPRECATED: Information Gathering from Non-Traditional Sources",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it was deemed not to be a legitimate attack pattern. Please refer to CAPEC-118 : Collect and Analyze Information.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-41'})
SET capec.name = "Using Meta-characters in E-mail Headers to Inject Malicious Payloads",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This type of attack involves an attacker leveraging meta-characters in email headers to inject improper behavior into email programs. Email software has become increasingly sophisticated and feature-rich. In addition, email applications are ubiquitous and connected directly to the Web making them ideal targets to launch and propagate attacks. As the user demand for new functionality in email applications grows, they become more like browsers with complex rendering and plug in routines. As more e",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-410'})
SET capec.name = "Information Elicitation",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An adversary engages an individual using any combination of social engineering methods for the purpose of extracting information. Accurate contextual and environmental queues, such as knowing important information about the target company or individual can greatly increase the success of the attack and the quality of information gathered. Authentic mimicry combined with detailed knowledge increases the success of elicitation attacks.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-411'})
SET capec.name = "DEPRECATED: Pretexting",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of the existing attack pattern \"CAPEC-407 : Social Information Gathering via Pretexting\". Please refer to this other CAPEC going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-412'})
SET capec.name = "Pretexting via Customer Service",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary engages in pretexting behavior, assuming the role of someone who works for Customer Service, to solicit information from target persons, or manipulate the target into performing an action that serves the adversary's interests. One example of a scenario such as this would be to call an individual, articulate your false affiliation with a credit card company, and then attempt to get the individual to verify their credit card number.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-413'})
SET capec.name = "Pretexting via Tech Support",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary engages in pretexting behavior, assuming the role of a tech support worker, to solicit information from target persons, or manipulate the target into performing an action that serves the adversary's interests. An adversary who uses social engineering to impersonate a tech support worker can have devastating effects on a network. This is an effective attack vector, because it can give an adversary physical access to network computers. It only takes a matter of seconds for someone to ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-414'})
SET capec.name = "Pretexting via Delivery Person",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary engages in pretexting behavior, assuming the role of a delivery person, to solicit information from target persons, or manipulate the target into performing an action that serves the adversary's interests. Impersonating a delivery person is an effective attack and an easy attack since not much acting is involved. Usually the hardest part is looking the part and having all of the proper credentials, papers and \"deliveries\" in order to be able to pull it off.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-415'})
SET capec.name = "Pretexting via Phone",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary engages in pretexting behavior, assuming some sort of trusted role, and contacting the targeted individual or organization via phone to solicit information from target persons, or manipulate the target into performing an action that serves the adversary's interests. This is the most common social engineering attack. Some of the most commonly effective approaches are to impersonate a fellow employee, impersonate a computer technician or to target help desk personnel.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-416'})
SET capec.name = "Manipulate Human Behavior",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary exploits inherent human psychological predisposition to influence a targeted individual or group to solicit information or manipulate the target into performing an action that serves the adversary's interests. Many interpersonal social engineering techniques do not involve outright deception, although they can; many are subtle ways of manipulating a target to remove barriers, make the target feel comfortable, and produce an exchange in which the target is either more likely to share",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-417'})
SET capec.name = "Influence Perception",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "The adversary uses social engineering to exploit the target's perception of the relationship between the adversary and themselves. This goal is to persuade the target to unknowingly perform an action or divulge information that is advantageous to the adversary.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-418'})
SET capec.name = "Influence Perception of Reciprocation",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary uses a social engineering techniques to produce a sense of obligation in the target to perform a certain action or concede some sensitive or key piece of information. Obligation has to do with actions one feels they need to take due to some sort of social, legal, or moral requirement, duty, contract, or promise. There are various techniques for fostering a sense of obligation to reciprocate or concede during ordinary modes of communication. One method is to compliment the target, an",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-419'})
SET capec.name = "DEPRECATED: Target Influence via Perception of Concession",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it was deemed not to be a legitimate pattern.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-42'})
SET capec.name = "MIME Conversion",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker exploits a weakness in the MIME conversion routine to cause a buffer overflow and gain control over the mail server machine. The MIME system is designed to allow various different information formats to be interpreted and sent via e-mail. Attack points exist when data are converted to MIME compatible format and back.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-420'})
SET capec.name = "Influence Perception of Scarcity",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "The adversary leverages a perception of scarcity to persuade the target to perform an action or divulge information that is advantageous to the adversary. By conveying a perception of scarcity, or a situation of limited supply, the adversary aims to create a sense of urgency in the context of a target's decision-making process.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-421'})
SET capec.name = "Influence Perception of Authority",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary uses a social engineering technique to convey a sense of authority that motivates the target to reveal specific information or take specific action. There are various techniques for producing a sense of authority during ordinary modes of communication. One common method is impersonation. By impersonating someone with a position of power within an organization, an adversary may motivate the target individual to reveal some piece of sensitive information or perform an action that bene",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-422'})
SET capec.name = "Influence Perception of Commitment and Consistency",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary uses social engineering to convince the target to do minor tasks as opposed to larger actions. After complying with a request, individuals are more likely to agree to subsequent requests that are similar in type and required effort.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-423'})
SET capec.name = "Influence Perception of Liking",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "The adversary influences the target's actions by building a relationship where the target has a liking to the adversary. People are more likely to be influenced by people of whom they are fond, so the adversary attempts to ingratiate themself with the target via actions, appearance, or a combination thereof.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-424'})
SET capec.name = "Influence Perception of Consensus or Social Proof",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "The adversary influences the target's actions by leveraging the inherent human nature to assume behavior of others is appropriate. In situations of uncertainty, people tend to behave in ways they see others behaving. The adversary convinces the target of adopting behavior or actions that is advantageous to the adversary.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-425'})
SET capec.name = "Target Influence via Framing",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary uses framing techniques to contextualize a conversation so that the target is more likely to be influenced by the adversary's point of view. Framing is information and experiences in life that alter the way we react to decisions we must make. This type of persuasive technique exploits the way people are conditioned to perceive data and its significance, while avoiding negative or avoidance responses from the target. Rather than a specific technique framing is a methodology of conver",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-426'})
SET capec.name = "Influence via Incentives",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "The adversary incites a behavior from the target by manipulating something of influence. This is commonly associated with financial, social, or ideological incentivization. Examples include monetary fraud, peer pressure, and preying on the target's morals or ethics. The most effective incentive against one target might not be as effective against another, therefore the adversary must gather information about the target's vulnerability to particular incentives.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-427'})
SET capec.name = "Influence via Psychological Principles",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "The adversary shapes the target's actions or behavior by focusing on the ways human interact and learn, leveraging such elements as cognitive and social psychology. In a variety of ways, a target can be influenced to behave or perform an action through capitalizing on what scholarship and research has learned about how and why humans react to specific scenarios and cues.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-428'})
SET capec.name = "Influence via Modes of Thinking",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "The adversary tailors their communication to the language and thought patterns of the target thereby weakening barriers or reluctance to communication. This method is a way of building rapport with a target by matching their speech patterns and the primary ways or dominant senses with which they make abstractions. This technique can be used to make the target more receptive to sharing information because the adversary has adapted their communication forms to match those of the target. When skill",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-429'})
SET capec.name = "Target Influence via Eye Cues",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "The adversary gains information via non-verbal means from the target through eye movements.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-43'})
SET capec.name = "Exploiting Multiple Input Interpretation Layers",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker supplies the target software with input data that contains sequences of special characters designed to bypass input validation logic. This exploit relies on the target making multiples passes over the input data and processing a \"layer\" of special characters with each pass. In this manner, the attacker can disguise input that would otherwise be rejected as invalid by concealing it with layers of special/escape characters that are stripped off by subsequent processing steps. The goal ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-430'})
SET capec.name = "DEPRECATED:  Target Influence via Micro-Expressions",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-431'})
SET capec.name = "DEPRECATED:  Target Influence via Neuro-Linguistic Programming (NLP)",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-432'})
SET capec.name = "DEPRECATED:  Target Influence via Voice in NLP",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-433'})
SET capec.name = "Target Influence via The Human Buffer Overflow",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker utilizes a technique to insinuate commands to the subconscious mind of the target via communication patterns. The human buffer overflow methodology does not rely on over-stimulating the mind of the target, but rather embedding messages within communication that the mind of the listener assembles at a subconscious level. The human buffer-overflow method is similar to subconscious programming to the extent that messages are embedded within the message.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-434'})
SET capec.name = "Target Influence via Interview and Interrogation",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-435'})
SET capec.name = "Target Influence via Instant Rapport",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-438'})
SET capec.name = "Modification During Manufacture",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An attacker modifies a technology, product, or component during a stage in its manufacture for the purpose of carrying out an attack against some entity involved in the supply chain lifecycle. There are an almost limitless number of ways an attacker can modify a technology when they are involved in its manufacture, as the attacker has potential inroads to the software composition, hardware design and assembly, firmware, or basic design mechanics. Additionally, manufacturing of key components is ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-439'})
SET capec.name = "Manipulation During Distribution",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An attacker undermines the integrity of a product, software, or technology at some stage of the distribution channel. The core threat of modification or manipulation during distribution arise from the many stages of distribution, as a product may traverse multiple suppliers and integrators as the final asset is delivered. Components and services provided from a manufacturer to a supplier may be tampered with during integration or packaging.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-44'})
SET capec.name = "Overflow Binary Resource File",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attack of this type exploits a buffer overflow vulnerability in the handling of binary resources. Binary resources may include music files like MP3, image files like JPEG files, and any other binary file. These attacks may pass unnoticed to the client machine through normal usage of files, such as a browser loading a seemingly innocent JPEG file. This can allow the adversary access to the execution stack and execute arbitrary code in the target process.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-440'})
SET capec.name = "Hardware Integrity Attack",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary exploits a weakness in the system maintenance process and causes a change to be made to a technology, product, component, or sub-component or a new one installed during its deployed use at the victim location for the purpose of carrying out an attack.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-441'})
SET capec.name = "Malicious Logic Insertion",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary installs or adds malicious logic (also known as malware) into a seemingly benign component of a fielded system. This logic is often hidden from the user of the system and works behind the scenes to achieve negative impacts. With the proliferation of mass digital storage and inexpensive multimedia devices, Bluetooth and 802.11 support, new attack vectors for spreading malware are emerging for things we once thought of as innocuous greeting cards, picture frames, or digital projectors",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-442'})
SET capec.name = "Infected Software",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary adds malicious logic, often in the form of a computer virus, to otherwise benign software. This logic is often hidden from the user of the software and works behind the scenes to achieve negative impacts. Many times, the malicious logic is inserted into empty space between legitimate code, and is then called when the software is executed. This pattern of attack focuses on software already fielded and used in operation as opposed to software that is still under development and part o",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-443'})
SET capec.name = "Malicious Logic Inserted Into Product by Authorized Developer",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary uses their privileged position within an authorized development organization to inject malicious logic into a codebase or product.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-444'})
SET capec.name = "Development Alteration",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary modifies a technology, product, or component during its development to acheive a negative impact once the system is deployed. The goal of the adversary is to modify the system in such a way that the negative impact can be leveraged when the system is later deployed. Development alteration attacks may include attacks that insert malicious logic into the system's software, modify or replace hardware components, and other attacks which negatively impact the system during development. T",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-445'})
SET capec.name = "Malicious Logic Insertion into Product Software via Configuration Management Manipulation",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-446'})
SET capec.name = "Malicious Logic Insertion into Product via Inclusion of Third-Party Component",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-447'})
SET capec.name = "Design Alteration",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary modifies the design of a technology, product, or component to acheive a negative impact once the system is deployed. In this type of attack, the goal of the adversary is to modify the design of the system, prior to development starting, in such a way that the negative impact can be leveraged when the system is later deployed. Design alteration attacks differ from development alteration attacks in that design alteration attacks take place prior to development and which then may or ma",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-448'})
SET capec.name = "Embed Virus into DLL",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary tampers with a DLL and embeds a computer virus into gaps between legitimate machine instructions. These gaps may be the result of compiler optimizations that pad memory blocks for performance gains. The embedded virus then attempts to infect any machine which interfaces with the product, and possibly steal private data or eavesdrop.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-449'})
SET capec.name = "DEPRECATED: Malware Propagation via USB Stick",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of CAPEC-448 : Malware Infection into Product Software. Please refer to this other pattern going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-45'})
SET capec.name = "Buffer Overflow via Symbolic Links",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This type of attack leverages the use of symbolic links to cause buffer overflows. An adversary can try to create or manipulate a symbolic link file such that its contents result in out of bounds data. When the target software processes the symbolic link file, it could potentially overflow internal buffers with insufficient bounds checking.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-450'})
SET capec.name = "DEPRECATED: Malware Propagation via USB U3 Autorun",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of CAPEC-448 : Embed Virus into DLL. Please refer to this other pattern going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-451'})
SET capec.name = "DEPRECATED: Malware Propagation via Infected Peripheral Device",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of CAPEC-448 : Malware Infection into Product Software. Please refer to this other pattern going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-452'})
SET capec.name = "Infected Hardware",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary inserts malicious logic into hardware, typically in the form of a computer virus or rootkit. This logic is often hidden from the user of the hardware and works behind the scenes to achieve negative impacts. This pattern of attack focuses on hardware already fielded and used in operation as opposed to hardware that is still under development and part of the supply chain.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-453'})
SET capec.name = "DEPRECATED: Malicious Logic Insertion via Counterfeit Hardware",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of CAPEC-452 : Malicious Logic Insertion into Product Hardware. Please refer to this other pattern going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-454'})
SET capec.name = "DEPRECATED: Modification of Existing Components with Counterfeit Hardware",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of CAPEC-452 : Malicious Logic Insertion into Product Hardware. Please refer to this other pattern going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-455'})
SET capec.name = "DEPRECATED: Malicious Logic Insertion via Inclusion of Counterfeit Hardware Components",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of CAPEC-457 : Malicious Logic Insertion into Product Hardware. Please refer to this other pattern going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-456'})
SET capec.name = "Infected Memory",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary inserts malicious logic into memory enabling them to achieve a negative impact. This logic is often hidden from the user of the system and works behind the scenes to achieve negative impacts. This pattern of attack focuses on systems already fielded and used in operation as opposed to systems that are still under development and part of the supply chain.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-457'})
SET capec.name = "USB Memory Attacks",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary loads malicious code onto a USB memory stick in order to infect any system which the device is plugged in to. USB drives present a significant security risk for business and government agencies. Given the ability to integrate wireless functionality into a USB stick, it is possible to design malware that not only steals confidential data, but sniffs the network, or monitor keystrokes, and then exfiltrates the stolen data off-site via a Wireless connection. Also, viruses can be transm",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-458'})
SET capec.name = "Flash Memory Attacks",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary inserts malicious logic into a product or technology via flashing the on-board memory with a code-base that contains malicious logic. Various attacks exist against the integrity of flash memory, the most direct being rootkits coded into the BIOS or chipset of a device.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-459'})
SET capec.name = "Creating a Rogue Certification Authority Certificate",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary exploits a weakness resulting from using a hashing algorithm with weak collision resistance to generate certificate signing requests (CSR) that contain collision blocks in their \"to be signed\" parts. The adversary submits one CSR to be signed by a trusted certificate authority then uses the signed blob to make a second certificate appear signed by said certificate authority. Due to the hash collision, both certificates, though different, hash to the same value and so the signed blob",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-46'})
SET capec.name = "Overflow Variables and Tags",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This type of attack leverages the use of tags or variables from a formatted configuration data to cause buffer overflow. The adversary crafts a malicious HTML page or configuration file that includes oversized strings, thus causing an overflow.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-460'})
SET capec.name = "HTTP Parameter Pollution (HPP)",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary adds duplicate HTTP GET/POST parameters by injecting query string delimiters. Via HPP it may be possible to override existing hardcoded HTTP parameters, modify the application behaviors, access and, potentially exploit, uncontrollable variables, and bypass input validation checkpoints and WAF rules.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-461'})
SET capec.name = "Web Services API Signature Forgery Leveraging Hash Function Extension Weakness",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary utilizes a hash function extension/padding weakness, to modify the parameters passed to the web service requesting authentication by generating their own call in order to generate a legitimate signature hash (as described in the notes), without knowledge of the secret token sometimes provided by the web service.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-462'})
SET capec.name = "Cross-Domain Search Timing",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker initiates cross domain HTTP / GET requests and times the server responses. The timing of these responses may leak important information on what is happening on the server. Browser's same origin policy prevents the attacker from directly reading the server responses (in the absence of any other weaknesses), but does not prevent the attacker from timing the responses to requests that the attacker issued cross domain.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-463'})
SET capec.name = "Padding Oracle Crypto Attack",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary is able to efficiently decrypt data without knowing the decryption key if a target system leaks data on whether or not a padding error happened while decrypting the ciphertext. A target system that leaks this type of information becomes the padding oracle and an adversary is able to make use of that oracle to efficiently decrypt data without knowing the decryption key by issuing on average 128*b calls to the padding oracle (where b is the number of bytes in the ciphertext block). In",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-464'})
SET capec.name = "Evercookie",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker creates a very persistent cookie that stays present even after the user thinks it has been removed. The cookie is stored on the victim's machine in over ten places. When the victim clears the cookie cache via traditional means inside the browser, that operation removes the cookie from certain places but not others. The malicious code then replicates the cookie from all of the places where it was not deleted to all of the possible storage locations once again. So the victim again has ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-465'})
SET capec.name = "Transparent Proxy Abuse",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "A transparent proxy serves as an intermediate between the client and the internet at large. It intercepts all requests originating from the client and forwards them to the correct location. The proxy also intercepts all responses to the client and forwards these to the client. All of this is done in a manner transparent to the client.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-466'})
SET capec.name = "Leveraging Active Adversary in the Middle Attacks to Bypass Same Origin Policy",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker leverages an adversary in the middle attack (CAPEC-94) in order to bypass the same origin policy protection in the victim's browser. This active adversary in the middle attack could be launched, for instance, when the victim is connected to a public WIFI hot spot. An attacker is able to intercept requests and responses between the victim's browser and some non-sensitive website that does not use TLS.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-467'})
SET capec.name = "Cross Site Identification",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker harvests identifying information about a victim via an active session that the victim's browser has with a social networking site. A victim may have the social networking site open in one tab or perhaps is simply using the \"remember me\" feature to keep their session with the social networking site active. An attacker induces a payload to execute in the victim's browser that transparently to the victim initiates a request to the social networking site (e.g., via available social netwo",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-468'})
SET capec.name = "Generic Cross-Browser Cross-Domain Theft",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker makes use of Cascading Style Sheets (CSS) injection to steal data cross domain from the victim's browser. The attack works by abusing the standards relating to loading of CSS: 1. Send cookies on any load of CSS (including cross-domain) 2. When parsing returned CSS ignore all data that does not make sense before a valid CSS descriptor is found by the CSS parser.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-469'})
SET capec.name = "HTTP DoS",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker performs flooding at the HTTP level to bring down only a particular web application rather than anything listening on a TCP/IP connection. This denial of service attack requires substantially fewer packets to be sent which makes DoS harder to detect. This is an equivalent of SYN flood in HTTP. The idea is to keep the HTTP session alive indefinitely and then repeat that hundreds of times. This attack targets resource depletion weaknesses in web server software. The web server will wai",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-47'})
SET capec.name = "Buffer Overflow via Parameter Expansion",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack, the target software is given input that the adversary knows will be modified and expanded in size during processing. This attack relies on the target software failing to anticipate that the expanded data may exceed some internal limit, thereby creating a buffer overflow.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-470'})
SET capec.name = "Expanding Control over the Operating System from the Database",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker is able to leverage access gained to the database to read / write data to the file system, compromise the operating system, create a tunnel for accessing the host machine, and use this access to potentially attack other machines on the same network as the database machine. Traditionally SQL injections attacks are viewed as a way to gain unauthorized read access to the data stored in the database, modify the data in the database, delete the data, etc. However, almost every data base m",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-471'})
SET capec.name = "Search Order Hijacking",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary exploits a weakness in an application's specification of external libraries to exploit the functionality of the loader where the process loading the library searches first in the same directory in which the process binary resides and then in other directories. Exploitation of this preferential search order can allow an attacker to make the loading process load the adversary's rogue library rather than the legitimate library. This attack can be leveraged with many different libraries",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-472'})
SET capec.name = "Browser Fingerprinting",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker carefully crafts small snippets of Java Script to efficiently detect the type of browser the potential victim is using. Many web-based attacks need prior knowledge of the web browser including the version of browser to ensure successful exploitation of a vulnerability. Having this knowledge allows an attacker to target the victim with attacks that specifically exploit known or zero day weaknesses in the type and version of the browser used by the victim. Automating this process via J",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-473'})
SET capec.name = "Signature Spoof",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker generates a message or datablock that causes the recipient to believe that the message or datablock was generated and cryptographically signed by an authoritative or reputable source, misleading a victim or victim operating system into performing malicious actions.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-474'})
SET capec.name = "Signature Spoofing by Key Theft",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker obtains an authoritative or reputable signer's private signature key by theft and then uses this key to forge signatures from the original signer to mislead a victim into performing actions that benefit the attacker.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-475'})
SET capec.name = "Signature Spoofing by Improper Validation",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary exploits a cryptographic weakness in the signature verification algorithm implementation to generate a valid signature without knowing the key.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-476'})
SET capec.name = "Signature Spoofing by Misrepresentation",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker exploits a weakness in the parsing or display code of the recipient software to generate a data blob containing a supposedly valid signature, but the signer's identity is falsely represented, which can lead to the attacker manipulating the recipient software or its victim user to perform compromising actions.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-477'})
SET capec.name = "Signature Spoofing by Mixing Signed and Unsigned Content",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker exploits the underlying complexity of a data structure that allows for both signed and unsigned content, to cause unsigned data to be processed as though it were signed data.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-478'})
SET capec.name = "Modification of Windows Service Configuration",
    capec.abstraction = "Detailed",
    capec.status = "Usable",
    capec.description = "An adversary exploits a weakness in access control to modify the execution parameters of a Windows service. The goal of this attack is to execute a malicious binary in place of an existing service.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-479'})
SET capec.name = "Malicious Root Certificate",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary exploits a weakness in authorization and installs a new root certificate on a compromised system. Certificates are commonly used for establishing secure TLS/SSL communications within a web browser. When a user attempts to browse a website that presents a certificate that is not trusted an error message will be displayed to warn the user of the security risk. Depending on the security settings, the browser may not allow the user to establish a connection to the website. Adversaries h",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-48'})
SET capec.name = "Passing Local Filenames to Functions That Expect a URL",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "This attack relies on client side code to access local files and resources instead of URLs. When the client browser is expecting a URL string, but instead receives a request for a local file, that execution is likely to occur in the browser process space with the browser's authority to local files. The attacker can send the results of this request to the local files out to a site that they control. This attack may be used to steal sensitive authentication data (either local or remote), or to gai",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-480'})
SET capec.name = "Escaping Virtualization",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary gains access to an application, service, or device with the privileges of an authorized or privileged user by escaping the confines of a virtualized environment. The adversary is then able to access resources or execute unauthorized code within the host environment, generally with the privileges of the user running the virtualized process. Successfully executing an attack of this type is often the first step in executing more complex attacks.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-481'})
SET capec.name = "Contradictory Destinations in Traffic Routing Schemes",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "Adversaries can provide contradictory destinations when sending messages. Traffic is routed in networks using the domain names in various headers available at different levels of the OSI model. In a Content Delivery Network (CDN) multiple domains might be available, and if there are contradictory domain names provided it is possible to route traffic to an inappropriate destination. The technique, called Domain Fronting, involves using different domain names in the SNI field of the TLS header and",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-482'})
SET capec.name = "TCP Flood",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary may execute a flooding attack using the TCP protocol with the intent to deny legitimate users access to a service. These attacks exploit the weakness within the TCP protocol where there is some state information for the connection the server needs to maintain. This often involves the use of TCP SYN messages.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-484'})
SET capec.name = "DEPRECATED: XML Client-Side Attack",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it a generalization of CAPEC-230: XML Nested Payloads and CAPEC-231: XML Oversized Payloads. Please refer to these CAPECs going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-485'})
SET capec.name = "Signature Spoofing by Key Recreation",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker obtains an authoritative or reputable signer's private signature key by exploiting a cryptographic weakness in the signature algorithm or pseudorandom number generation and then uses this key to forge signatures from the original signer to mislead a victim into performing actions that benefit the attacker.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-486'})
SET capec.name = "UDP Flood",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary may execute a flooding attack using the UDP protocol with the intent to deny legitimate users access to a service by consuming the available network bandwidth. Additionally, firewalls often open a port for each UDP connection destined for a service with an open UDP port, meaning the firewalls in essence save the connection state thus the high packet nature of a UDP flood can also overwhelm resources allocated to the firewall. UDP attacks can also target services like DNS or VoIP whi",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-487'})
SET capec.name = "ICMP Flood",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary may execute a flooding attack using the ICMP protocol with the intent to deny legitimate users access to a service by consuming the available network bandwidth. A typical attack involves a victim server receiving ICMP packets at a high rate from a wide range of source addresses. Additionally, due to the session-less nature of the ICMP protocol, the source of a packet is easily spoofed making it difficult to find the source of the attack.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-488'})
SET capec.name = "HTTP Flood",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary may execute a flooding attack using the HTTP protocol with the intent to deny legitimate users access to a service by consuming resources at the application layer such as web services and their infrastructure. These attacks use legitimate session-based HTTP GET requests designed to consume large amounts of a server's resources. Since these are legitimate sessions this attack is very difficult to detect.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-489'})
SET capec.name = "SSL Flood",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary may execute a flooding attack using the SSL protocol with the intent to deny legitimate users access to a service by consuming all the available resources on the server side. These attacks take advantage of the asymmetric relationship between the processing power used by the client and the processing power used by the server to create a secure connection. In this manner the attacker can make a large number of HTTPS requests on a low provisioned machine to tie up a disproportionately",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-49'})
SET capec.name = "Password Brute Forcing",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary tries every possible value for a password until they succeed. A brute force attack, if feasible computationally, will always be successful because it will essentially go through all possible passwords given the alphabet used (lower case letters, upper case letters, numbers, symbols, etc.) and the maximum length of the password.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-490'})
SET capec.name = "Amplification",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary may execute an amplification where the size of a response is far greater than that of the request that generates it. The goal of this attack is to use a relatively few resources to create a large amount of traffic against a target server. To execute this attack, an adversary send a request to a 3rd party service, spoofing the source address to be that of the target server. The larger response that is generated by the 3rd party service is then sent to the target server. By sending a ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-491'})
SET capec.name = "Quadratic Data Expansion",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary exploits macro-like substitution to cause a denial of service situation due to excessive memory being allocated to fully expand the data. The result of this denial of service could cause the application to freeze or crash. This involves defining a very large entity and using it multiple times in a single entity substitution. CAPEC-197 is a similar attack pattern, but it is easier to discover and defend against. This attack pattern does not perform multi-level substitution and theref",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-492'})
SET capec.name = "Regular Expression Exponential Blowup",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary may execute an attack on a program that uses a poor Regular Expression(Regex) implementation by choosing input that results in an extreme situation for the Regex. A typical extreme situation operates at exponential time compared to the input size. This is due to most implementations using a Nondeterministic Finite Automaton(NFA) state machine to be built by the Regex algorithm since NFA allows backtracking and thus more complex regular expressions.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-493'})
SET capec.name = "SOAP Array Blowup",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary may execute an attack on a web service that uses SOAP messages in communication. By sending a very large SOAP array declaration to the web service, the attacker forces the web service to allocate space for the array elements before they are parsed by the XML parser. The attacker message is typically small in size containing a large array declaration of say 1,000,000 elements and a couple of array elements. This attack targets exhaustion of the memory resources of the web service.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-494'})
SET capec.name = "TCP Fragmentation",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary may execute a TCP Fragmentation attack against a target with the intention of avoiding filtering rules of network controls, by attempting to fragment the TCP packet such that the headers flag field is pushed into the second fragment which typically is not filtered.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-495'})
SET capec.name = "UDP Fragmentation",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker may execute a UDP Fragmentation attack against a target server in an attempt to consume resources such as bandwidth and CPU. IP fragmentation occurs when an IP datagram is larger than the MTU of the route the datagram has to traverse. Typically the attacker will use large UDP packets over 1500 bytes of data which forces fragmentation as ethernet MTU is 1500 bytes. This attack is a variation on a typical UDP flood but it enables more network bandwidth to be consumed with fewer packets",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-496'})
SET capec.name = "ICMP Fragmentation",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker may execute a ICMP Fragmentation attack against a target with the intention of consuming resources or causing a crash. The attacker crafts a large number of identical fragmented IP packets containing a portion of a fragmented ICMP message. The attacker these sends these messages to a target host which causes the host to become non-responsive. Another vector may be sending a fragmented ICMP message to a target host with incorrect sizes in the header which causes the host to hang.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-497'})
SET capec.name = "File Discovery",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary engages in probing and exploration activities to determine if common key files exists. Such files often contain configuration and security parameters of the targeted application, system or network. Using this knowledge may often pave the way for more damaging attacks.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-498'})
SET capec.name = "Probe iOS Screenshots",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary examines screenshot images created by iOS in an attempt to obtain sensitive information. This attack targets temporary screenshots created by the underlying OS while the application remains open in the background.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-499'})
SET capec.name = "Android Intent Intercept",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary, through a previously installed malicious application, intercepts messages from a trusted Android-based application in an attempt to achieve a variety of different objectives including denial of service, information disclosure, and data injection. An implicit intent sent from a trusted application can be received by any application that has declared an appropriate intent filter. If the intent is not protected by a permission that the malicious application lacks, then the attacker ca",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-5'})
SET capec.name = "Blue Boxing",
    capec.abstraction = "Detailed",
    capec.status = "Obsolete",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-50'})
SET capec.name = "Password Recovery Exploitation",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker may take advantage of the application feature to help users recover their forgotten passwords in order to gain access into the system with the same privileges as the original user. Generally password recovery schemes tend to be weak and insecure.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-500'})
SET capec.name = "WebView Injection",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary, through a previously installed malicious application, injects code into the context of a web page displayed by a WebView component. Through the injected code, an adversary is able to manipulate the DOM tree and cookies of the page, expose sensitive information, and can launch attacks against the web application from within the web page.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-501'})
SET capec.name = "Android Activity Hijack",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary intercepts an implicit intent sent to launch a Android-based trusted activity and instead launches a counterfeit activity in its place. The malicious activity is then used to mimic the trusted activity's user interface and prompt the target to enter sensitive data as if they were interacting with the trusted activity.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-502'})
SET capec.name = "Intent Spoof",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary, through a previously installed malicious application, issues an intent directed toward a specific trusted application's component in an attempt to achieve a variety of different objectives including modification of data, information disclosure, and data injection. Components that have been unintentionally exported and made public are subject to this type of an attack. If the component trusts the intent's action without verififcation, then the target application performs the functio",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-503'})
SET capec.name = "WebView Exposure",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary, through a malicious web page, accesses application specific functionality by leveraging interfaces registered through WebView's addJavascriptInterface API. Once an interface is registered to WebView through addJavascriptInterface, it becomes global and all pages loaded in the WebView can call this interface.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-504'})
SET capec.name = "Task Impersonation",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary, through a previously installed malicious application, impersonates an expected or routine task in an attempt to steal sensitive information or leverage a user's privileges.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-505'})
SET capec.name = "Scheme Squatting",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary, through a previously installed malicious application, registers for a URL scheme intended for a target application that has not been installed. Thereafter, messages intended for the target application are handled by the malicious application. Upon receiving a message, the malicious application displays a screen that mimics the target application, thereby convincing the user to enter sensitive information. This type of attack is most often used to obtain sensitive information (e.g.,",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-506'})
SET capec.name = "Tapjacking",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary, through a previously installed malicious application, displays an interface that misleads the user and convinces them to tap on an attacker desired location on the screen. This is often accomplished by overlaying one screen on top of another while giving the appearance of a single interface. There are two main techniques used to accomplish this. The first is to leverage transparent properties that allow taps on the screen to pass through the visible application to an application ru",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-507'})
SET capec.name = "Physical Theft",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An adversary gains physical access to a system or device through theft of the item. Possession of a system or device enables a number of unique attacks to be executed and often provides the adversary with an extended timeframe for which to perform an attack. Most protections put in place to secure sensitive information can be defeated when an adversary has physical access and enough time.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-508'})
SET capec.name = "Shoulder Surfing",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In a shoulder surfing attack, an adversary observes an unaware individual's keystrokes, screen content, or conversations with the goal of obtaining sensitive information. One motive for this attack is to obtain sensitive information about the target for financial, personal, political, or other gains. From an insider threat perspective, an additional motive could be to obtain system/application credentials or cryptographic keys. Shoulder surfing attacks are accomplished by observing the content \"",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-509'})
SET capec.name = "Kerberoasting",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "Through the exploitation of how service accounts leverage Kerberos authentication with Service Principal Names (SPNs), the adversary obtains and subsequently cracks the hashed credentials of a service account target to exploit its privileges. The Kerberos authentication protocol centers around a ticketing system which is used to request/grant access to services and to then access the requested services. As an authenticated user, the adversary may request Active Directory and obtain a service tic",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-51'})
SET capec.name = "Poison Web Service Registry",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "SOA and Web Services often use a registry to perform look up, get schema information, and metadata about services. A poisoned registry can redirect (think phishing for servers) the service requester to a malicious service provider, provide incorrect information in schema or metadata, and delete information about service provider interfaces.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-510'})
SET capec.name = "SaaS User Request Forgery",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary, through a previously installed malicious application, performs malicious actions against a third-party Software as a Service (SaaS) application (also known as a cloud based application) by leveraging the persistent and implicit trust placed on a trusted user's session. This attack is executed after a trusted user is authenticated into a cloud service, \"piggy-backing\" on the authenticated session, and exploiting the fact that the cloud service believes it is only interacting with th",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-511'})
SET capec.name = "Infiltration of Software Development Environment",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker uses common delivery mechanisms such as email attachments or removable media to infiltrate the IDE (Integrated Development Environment) of a victim manufacturer with the intent of implanting malware allowing for attack control of the victim IDE environment. The attack then uses this access to exfiltrate sensitive data or information, manipulate said data or information, and conceal these actions. This will allow and aid the attack to meet the goal of future compromise of a recipient ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-516'})
SET capec.name = "Hardware Component Substitution During Baselining",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary with access to system components during allocated baseline development can substitute a maliciously altered hardware component for a baseline component during the product development and research phases. This can lead to adjustments and calibrations being made in the product so that when the final product, now containing the modified component, is deployed it will not perform as designed and be advantageous to the adversary.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-517'})
SET capec.name = "Documentation Alteration to Circumvent Dial-down",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker with access to a manufacturer's documentation, which include descriptions of advanced technology and/or specific components' criticality, alters the documents to circumvent dial-down functionality requirements. This alteration would change the interpretation of implementation and manufacturing techniques, allowing for advanced technologies to remain in place even though these technologies might be restricted to certain customers, such as nations on the terrorist watch list, giving th",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-518'})
SET capec.name = "Documentation Alteration to Produce Under-performing Systems",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker with access to a manufacturer's documentation alters the descriptions of system capabilities with the intent of causing errors in derived system requirements, impacting the overall effectiveness and capability of the system, allowing an attacker to take advantage of the introduced system capability flaw once the system is deployed.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-519'})
SET capec.name = "Documentation Alteration to Cause Errors in System Design",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker with access to a manufacturer's documentation containing requirements allocation and software design processes maliciously alters the documentation in order to cause errors in system design. This allows the attacker to take advantage of a weakness in a deployed system of the manufacturer for malicious purposes.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-52'})
SET capec.name = "Embedding NULL Bytes",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary embeds one or more null bytes in input to the target software. This attack relies on the usage of a null-valued byte as a string terminator in many environments. The goal is for certain components of the target software to stop processing the input when it encounters the null byte(s).",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-520'})
SET capec.name = "Counterfeit Hardware Component Inserted During Product Assembly",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary with either direct access to the product assembly process or to the supply of subcomponents used in the product assembly process introduces counterfeit hardware components into product assembly. The assembly containing the counterfeit components results in a system specifically designed for malicious purposes.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-521'})
SET capec.name = "Hardware Design Specifications Are Altered",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker with access to a manufacturer's hardware manufacturing process documentation alters the design specifications, which introduces flaws advantageous to the attacker once the system is deployed.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-522'})
SET capec.name = "Malicious Hardware Component Replacement",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary replaces legitimate hardware in the system with faulty counterfeit or tampered hardware in the supply chain distribution channel, with purpose of causing malicious disruption or allowing for additional compromise when the system is deployed.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-523'})
SET capec.name = "Malicious Software Implanted",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker implants malicious software into the system in the supply chain distribution channel, with purpose of causing malicious disruption or allowing for additional compromise when the system is deployed.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-524'})
SET capec.name = "Rogue Integration Procedures",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker alters or establishes rogue processes in an integration facility in order to insert maliciously altered components into the system. The attacker would then supply the malicious components. This would allow for malicious disruption or additional compromise when the system is deployed.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-528'})
SET capec.name = "XML Flood",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary may execute a flooding attack using XML messages with the intent to deny legitimate users access to a web service. These attacks are accomplished by sending a large number of XML based requests and letting the service attempt to parse each one. In many cases this type of an attack will result in a XML Denial of Service (XDoS) due to an application becoming unstable, freezing, or crashing.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-529'})
SET capec.name = "Malware-Directed Internal Reconnaissance",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "Adversary uses malware or a similarly controlled application installed inside an organizational perimeter to gather information about the composition, configuration, and security mechanisms of a targeted application, system or network.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-53'})
SET capec.name = "Postfix, Null Terminate, and Backslash",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "If a string is passed through a filter of some kind, then a terminal NULL may not be valid. Using alternate representation of NULL allows an adversary to embed the NULL mid-string while postfixing the proper data so that the filter is avoided. One example is a filter that looks for a trailing slash character. If a string insertion is possible, but the slash must exist, an alternate encoding of NULL in mid-string may be used.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-530'})
SET capec.name = "Provide Counterfeit Component",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker provides a counterfeit component during the procurement process of a lower-tier component supplier to a sub-system developer or integrator, which is then built into the system being upgraded or repaired by the victim, allowing the attacker to cause disruption or additional compromise.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-531'})
SET capec.name = "Hardware Component Substitution",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker substitutes out a tested and approved hardware component for a maliciously-altered hardware component. This type of attack is carried out directly on the system, enabling the attacker to then cause disruption or additional compromise.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-532'})
SET capec.name = "Altered Installed BIOS",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An attacker with access to download and update system software sends a maliciously altered BIOS to the victim or victim supplier/integrator, which when installed allows for future exploitation.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-533'})
SET capec.name = "Malicious Manual Software Update",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker introduces malicious code to the victim's system by altering the payload of a software update, allowing for additional compromise or site disruption at the victim location. These manual, or user-assisted attacks, vary from requiring the user to download and run an executable, to as streamlined as tricking the user to click a URL. Attacks which aim at penetrating a specific network infrastructure often rely upon secondary attack methods to achieve the desired impact. Spamming, for exa",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-534'})
SET capec.name = "Malicious Hardware Update",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary introduces malicious hardware during an update or replacement procedure, allowing for additional compromise or site disruption at the victim location. After deployment, it is not uncommon for upgrades and replacements to occur involving hardware and various replaceable parts. These upgrades and replacements are intended to correct defects, provide additional features, and to replace broken or worn-out parts. However, by forcing or tricking the replacement of a good component with a ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-535'})
SET capec.name = "Malicious Gray Market Hardware",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker maliciously alters hardware components that will be sold on the gray market, allowing for victim disruption and compromise when the victim needs replacement hardware components for systems where the parts are no longer in regular supply from original suppliers, or where the hardware components from the attacker seems to be a great benefit from a cost perspective.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-536'})
SET capec.name = "Data Injected During Configuration",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An attacker with access to data files and processes on a victim's system injects malicious data into critical operational data during configuration or recalibration, causing the victim's system to perform in a suboptimal manner that benefits the adversary.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-537'})
SET capec.name = "Infiltration of Hardware Development Environment",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary, leveraging the ability to manipulate components of primary support systems and tools within the development and production environments, inserts malicious software within the hardware and/or firmware development environment. The infiltration purpose is to alter developed hardware components in a system destined for deployment at the victim's organization, for the purpose of disruption or further compromise.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-538'})
SET capec.name = "Open-Source Library Manipulation",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "Adversaries implant malicious code in open source software (OSS) libraries to have it widely distributed, as OSS is commonly downloaded by developers and other users to incorporate into software development projects. The adversary can have a particular system in mind to target, or the implantation can be the first stage of follow-on attacks on many systems.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-539'})
SET capec.name = "ASIC With Malicious Functionality",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker with access to the development environment process of an application-specific integrated circuit (ASIC) for a victim system being developed or maintained after initial deployment can insert malicious functionality into the system for the purpose of disruption or further compromise.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-54'})
SET capec.name = "Query System for Information",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary, aware of an application's location (and possibly authorized to use the application), probes an application's structure and evaluates its robustness by submitting requests and examining responses. Often, this is accomplished by sending variants of expected queries in the hope that these modified queries might return information beyond what the expected set of queries would provide.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-540'})
SET capec.name = "Overread Buffers",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary attacks a target by providing input that causes an application to read beyond the boundary of a defined buffer. This typically occurs when a value influencing where to start or stop reading is set to reflect positions outside of the valid memory location of the buffer. This type of attack may result in exposure of sensitive information, a system crash, or arbitrary code execution.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-541'})
SET capec.name = "Application Fingerprinting",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary engages in fingerprinting activities to determine the type or version of an application installed on a remote target.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-542'})
SET capec.name = "Targeted Malware",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary develops targeted malware that takes advantage of a known vulnerability in an organizational information technology environment. The malware crafted for these attacks is based specifically on information gathered about the technology environment. Successfully executing the malware enables an adversary to achieve a wide variety of negative technical impacts.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-543'})
SET capec.name = "Counterfeit Websites",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Adversary creates duplicates of legitimate websites. When users visit a counterfeit site, the site can gather information or upload malware.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-544'})
SET capec.name = "Counterfeit Organizations",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary creates a false front organizations with the appearance of a legitimate supplier in the critical life cycle path that then injects corrupted/malicious information system components into the organizational supply chain.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-545'})
SET capec.name = "Pull Data from System Resources",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary who is authorized or has the ability to search known system resources, does so with the intention of gathering useful information. System resources include files, memory, and other aspects of the target system. In this pattern of attack, the adversary does not necessarily know what they are going to find when they start pulling data. This is different than CAPEC-150 where the adversary knows what they are looking for due to the common location.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-546'})
SET capec.name = "Incomplete Data Deletion in a Multi-Tenant Environment",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary obtains unauthorized information due to insecure or incomplete data deletion in a multi-tenant environment. If a cloud provider fails to completely delete storage and data from former cloud tenants' systems/resources, once these resources are allocated to new, potentially malicious tenants, the latter can probe the provided resources for sensitive information still there.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-547'})
SET capec.name = "Physical Destruction of Device or Component",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary conducts a physical attack a device or component, destroying it such that it no longer functions as intended.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-548'})
SET capec.name = "Contaminate Resource",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An adversary contaminates organizational information systems (including devices and networks) by causing them to handle information of a classification/sensitivity for which they have not been authorized. When this happens, the contaminated information system, device, or network must be brought offline to investigate and mitigate the data spill, which denies availability of the system until the investigation is complete.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-549'})
SET capec.name = "Local Execution of Code",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary installs and executes malicious code on the target system in an effort to achieve a negative technical impact. Examples include rootkits, ransomware, spyware, adware, and others.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-55'})
SET capec.name = "Rainbow Table Password Cracking",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker gets access to the database table where hashes of passwords are stored. They then use a rainbow table of pre-computed hash chains to attempt to look up the original password. Once the original password corresponding to the hash is obtained, the attacker uses the original password to gain access to the system.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-550'})
SET capec.name = "Install New Service",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "When an operating system starts, it also starts programs called services or daemons. Adversaries may install a new service which will be executed at startup (on a Windows system, by modifying the registry). The service name may be disguised by using a name from a related operating system or benign software. Services are usually run with elevated privileges.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-551'})
SET capec.name = "Modify Existing Service",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "When an operating system starts, it also starts programs called services or daemons. Modifying existing services may break existing services or may enable services that are disabled/not commonly used.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-552'})
SET capec.name = "Install Rootkit ",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary exploits a weakness in authentication to install malware that alters the functionality and information provide by targeted operating system API calls. Often referred to as rootkits, it is often used to hide the presence of programs, files, network connections, services, drivers, and other system components.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-554'})
SET capec.name = "Functionality Bypass",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An adversary attacks a system by bypassing some or all functionality intended to protect it. Often, a system user will think that protection is in place, but the functionality behind those protections has been disabled by the adversary.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-555'})
SET capec.name = "Remote Services with Stolen Credentials",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "This pattern of attack involves an adversary that uses stolen credentials to leverage remote services such as RDP, telnet, SSH, and VNC to log into a system. Once access is gained, any number of malicious activities could be performed.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-556'})
SET capec.name = "Replace File Extension Handlers",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "When a file is opened, its file handler is checked to determine which program opens the file. File handlers are configuration properties of many operating systems. Applications can modify the file handler for a given file extension to call an arbitrary program when a file with the given extension is opened.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-557'})
SET capec.name = "DEPRECATED: Schedule Software To Run",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This CAPEC has been deprecated because it is not directly related to a weakness, social engineering, supply chains, or a physical-based attack.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-558'})
SET capec.name = "Replace Trusted Executable",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary exploits weaknesses in privilege management or access control to replace a trusted executable with a malicious version and enable the execution of malware when that trusted executable is called.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-559'})
SET capec.name = "Orbital Jamming",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack pattern, the adversary sends disruptive signals at a target satellite using a rogue uplink station to disrupt the intended transmission. Those within the satellite's footprint are prevented from reaching the satellite's targeted or neighboring channels. The satellite's footprint size depends upon its position in the sky; higher orbital satellites cover multiple continents.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-56'})
SET capec.name = "DEPRECATED: Removing/short-circuiting 'guard logic'",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is a duplicate of CAPEC-207 : Removing Important Client Functionality. Please refer to this other pattern going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-560'})
SET capec.name = "Use of Known Domain Credentials",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-561'})
SET capec.name = "Windows Admin Shares with Stolen Credentials",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary guesses or obtains (i.e. steals or purchases) legitimate Windows administrator credentials (e.g. userID/password) to access Windows Admin Shares on a local machine or within a Windows domain.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-562'})
SET capec.name = "Modify Shared File",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary manipulates the files in a shared location by adding malicious programs, scripts, or exploit code to valid content. Once a user opens the shared content, the tainted content is executed.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-563'})
SET capec.name = "Add Malicious File to Shared Webroot",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversaries may add malicious content to a website through the open file share and then browse to that content with a web browser to cause the server to execute the content. The malicious content will typically run under the context and permissions of the web server process, often resulting in local system or administrative privileges depending on how the web server is configured.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-564'})
SET capec.name = "Run Software at Logon",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Operating system allows logon scripts to be run whenever a specific user or users logon to a system. If adversaries can access these scripts, they may insert additional code into the logon script. This code can allow them to maintain persistence or move laterally within an enclave because it is executed every time the affected user or users logon to a computer. Modifying logon scripts can effectively bypass workstation and enclave firewalls. Depending on the access configuration of the logon scr",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-565'})
SET capec.name = "Password Spraying",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-566'})
SET capec.name = "DEPRECATED: Dump Password Hashes",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This CAPEC has been deprecated because of is not directly related to a weakness, social engineering, supply chains, or a physical-based attack.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-567'})
SET capec.name = "DEPRECATED: Obtain Data via Utilities",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This CAPEC has been deprecated because it is not directly related to a weakness, social engineering, supply chains, or a physical-based attack.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-568'})
SET capec.name = "Capture Credentials via Keylogger",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary deploys a keylogger in an effort to obtain credentials directly from a system's user. After capturing all the keystrokes made by a user, the adversary can analyze the data and determine which string are likely to be passwords or other credential related information.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-569'})
SET capec.name = "Collect Data as Provided by Users",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker leverages a tool, device, or program to obtain specific information as provided by a user of the target system. This information is often needed by the attacker to launch a follow-on attack. This attack is different than Social Engineering as the adversary is not tricking or deceiving the user. Instead the adversary is putting a mechanism in place that captures the information that a user legitimately enters into a system. Deploying a keylogger, performing a UAC prompt, or wrapping t",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-57'})
SET capec.name = "Utilizing REST's Trust in the System Resource to Obtain Sensitive Data",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack utilizes a REST(REpresentational State Transfer)-style applications' trust in the system resources and environment to obtain sensitive data once SSL is terminated.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-570'})
SET capec.name = "DEPRECATED: Signature-Based Avoidance",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This CAPEC has been deprecated because it is not directly related to a weakness, social engineering, supply chains, or a physical-based attack.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-571'})
SET capec.name = "Block Logging to Central Repository",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-572'})
SET capec.name = "Artificially Inflate File Sizes",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-573'})
SET capec.name = "Process Footprinting",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary exploits functionality meant to identify information about the currently running processes on the target system to an authorized user. By knowing what processes are running on the target system, the adversary can learn about the target environment as a means towards further malicious behavior.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-574'})
SET capec.name = "Services Footprinting",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary exploits functionality meant to identify information about the services on the target system to an authorized user. By knowing what services are registered on the target system, the adversary can learn about the target environment as a means towards further malicious behavior. Depending on the operating system, commands that can obtain services information include \"sc\" and \"tasklist/svc\" using Tasklist, and \"net start\" using Net.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-575'})
SET capec.name = "Account Footprinting",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary exploits functionality meant to identify information about the domain accounts and their permissions on the target system to an authorized user. By knowing what accounts are registered on the target system, the adversary can inform further and more targeted malicious behavior. Example Windows commands which can acquire this information are: \"net user\" and \"dsquery\".",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-576'})
SET capec.name = "Group Permission Footprinting",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary exploits functionality meant to identify information about user groups and their permissions on the target system to an authorized user. By knowing what users/permissions are registered on the target system, the adversary can inform further and more targeted malicious behavior. An example Windows command which can list local groups is \"net localgroup\".",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-577'})
SET capec.name = "Owner Footprinting",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary exploits functionality meant to identify information about the primary users on the target system to an authorized user. They may do this, for example, by reviewing logins or file modification times. By knowing what owners use the target system, the adversary can inform further and more targeted malicious behavior. An example Windows command that may accomplish this is \"dir /A ntuser.dat\". Which will display the last modified time of a user's ntuser.dat file when run within the root",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-578'})
SET capec.name = "Disable Security Software",
    capec.abstraction = "Standard",
    capec.status = "Usable",
    capec.description = "An adversary exploits a weakness in access control to disable security tools so that detection does not occur. This can take the form of killing processes, deleting registry keys so that tools do not start at run time, deleting log files, or other methods.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-579'})
SET capec.name = "Replace Winlogon Helper DLL",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Winlogon is a part of Windows that performs logon actions. In Windows systems prior to Windows Vista, a registry key can be modified that causes Winlogon to load a DLL on startup. Adversaries may take advantage of this feature to load adversarial code at startup.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-58'})
SET capec.name = "Restful Privilege Elevation",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary identifies a Rest HTTP (Get, Put, Delete) style permission method allowing them to perform various malicious actions upon server data due to lack of access control mechanisms implemented within the application service accepting HTTP messages.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-580'})
SET capec.name = "System Footprinting",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary engages in active probing and exploration activities to determine security information about a remote target system. Often times adversaries will rely on remote applications that can be probed for system configurations.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-581'})
SET capec.name = "Security Software Footprinting",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Adversaries may attempt to get a listing of security tools that are installed on the system and their configurations. This may include security related system features (such as a built-in firewall or anti-spyware) as well as third-party security software.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-582'})
SET capec.name = "Route Disabling",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary disables the network route between two targets. The goal is to completely sever the communications channel between two entities. This is often the result of a major error or the use of an \"Internet kill switch\" by those in control of critical infrastructure. This attack pattern differs from most other obstruction patterns by targeting the route itself, as opposed to the data passed over the route.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-583'})
SET capec.name = "Disabling Network Hardware",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack pattern, an adversary physically disables networking hardware by powering it down or disconnecting critical equipment. Disabling or shutting off critical system resources prevents them from performing their service as intended, which can have direct and indirect consequences on other systems. This attack pattern is considerably less technical than the selective blocking used in most obstruction attacks.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-584'})
SET capec.name = "BGP Route Disabling",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary suppresses the Border Gateway Protocol (BGP) advertisement for a route so as to render the underlying network inaccessible. The BGP protocol helps traffic move throughout the Internet by selecting the most efficient route between Autonomous Systems (AS), or routing domains. BGP is the basis for interdomain routing infrastructure, providing connections between these ASs. By suppressing the intended AS routing advertisements and/or forcing less effective routes for traffic to ASs, the",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-585'})
SET capec.name = "DNS Domain Seizure",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack pattern, an adversary influences a target's web-hosting company to disable a target domain. The goal is to prevent access to the targeted service provided by that domain. It usually occurs as the result of civil or criminal legal interventions.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-586'})
SET capec.name = "Object Injection",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An adversary attempts to exploit an application by injecting additional, malicious content during its processing of serialized objects. Developers leverage serialization in order to convert data or state into a static, binary format for saving to disk or transferring over a network. These objects are then deserialized when needed to recover the data/state. By injecting a malformed object into a vulnerable application, an adversary can potentially compromise the application by manipulating the de",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-587'})
SET capec.name = "Cross Frame Scripting (XFS)",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack pattern combines malicious Javascript and a legitimate webpage loaded into a concealed iframe. The malicious Javascript is then able to interact with a legitimate webpage in a manner that is unknown to the user. This attack usually leverages some element of social engineering in that an attacker must convinces a user to visit a web page that the attacker controls.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-588'})
SET capec.name = "DOM-Based XSS",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This type of attack is a form of Cross-Site Scripting (XSS) where a malicious script is inserted into the client-side HTML being parsed by a web browser. Content served by a vulnerable web application includes script code used to manipulate the Document Object Model (DOM). This script code either does not properly validate input, or does not perform proper output encoding, thus creating an opportunity for an adversary to inject a malicious script launch a XSS attack. A key distinction between ot",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-589'})
SET capec.name = "DNS Blocking",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary intercepts traffic and intentionally drops DNS requests based on content in the request. In this way, the adversary can deny the availability of specific services or content to the user even if the IP address is changed.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-59'})
SET capec.name = "Session Credential Falsification through Prediction",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack targets predictable session ID in order to gain privileges. The attacker can predict the session ID used during a transaction to perform spoofing and session hijacking.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-590'})
SET capec.name = "IP Address Blocking",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary performing this type of attack drops packets destined for a target IP address. The aim is to prevent access to the service hosted at the target IP address.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-591'})
SET capec.name = "Reflected XSS",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "This type of attack is a form of Cross-Site Scripting (XSS) where a malicious script is \"reflected\" off a vulnerable web application and then executed by a victim's browser. The process starts with an adversary delivering a malicious script to a victim and convincing the victim to send the script to the vulnerable web application.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-592'})
SET capec.name = "Stored XSS",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary utilizes a form of Cross-site Scripting (XSS) where a malicious script is persistently \"stored\" within the data storage of a vulnerable web application as valid input.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-593'})
SET capec.name = "Session Hijacking",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "This type of attack involves an adversary that exploits weaknesses in an application's use of sessions in performing authentication. The adversary is able to steal or manipulate an active session and use it to gain unathorized access to the application.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-594'})
SET capec.name = "Traffic Injection",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "An adversary injects traffic into the target's network connection. The adversary is therefore able to degrade or disrupt the connection, and potentially modify the content. This is not a flooding attack, as the adversary is not focusing on exhausting resources. Instead, the adversary is crafting a specific input to affect the system in a particular way.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-595'})
SET capec.name = "Connection Reset",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "In this attack pattern, an adversary injects a connection reset packet to one or both ends of a target's connection. The attacker is therefore able to have the target and/or the destination server sever the connection without having to directly filter the traffic between them.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-596'})
SET capec.name = "TCP RST Injection",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary injects one or more TCP RST packets to a target after the target has made a HTTP GET request. The goal of this attack is to have the target and/or destination web server terminate the TCP connection.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-597'})
SET capec.name = "Absolute Path Traversal",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary with access to file system resources, either directly or via application logic, will use various file absolute paths and navigation mechanisms such as \"..\" to extend their range of access to inappropriate areas of the file system. The goal of the adversary is to access directories and files that are intended to be restricted from their access.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-598'})
SET capec.name = "DNS Spoofing",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary sends a malicious (\"NXDOMAIN\" (\"No such domain\") code, or DNS A record) response to a target's route request before a legitimate resolver can. This technique requires an On-path or In-path device that can monitor and respond to the target's DNS requests. This attack differs from BGP Tampering in that it directly responds to requests made by the target instead of polluting the routing the target's infrastructure uses.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-599'})
SET capec.name = "Terrestrial Jamming",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack pattern, the adversary transmits disruptive signals in the direction of the target's consumer-level satellite dish (as opposed to the satellite itself). The transmission disruption occurs in a more targeted range. Portable terrestrial jammers have a range of 3-5 kilometers in urban areas and 20 kilometers in rural areas. This technique requires a terrestrial jammer that is more powerful than the frequencies sent from the satellite.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-6'})
SET capec.name = "Argument Injection",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker changes the behavior or state of a targeted application through injecting data or command syntax through the targets use of non-validated and non-filtered arguments of exposed services or methods.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-60'})
SET capec.name = "Reusing Session IDs (aka Session Replay)",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack targets the reuse of valid session ID to spoof the target system in order to gain privileges. The attacker tries to reuse a stolen session ID used previously during a transaction to perform spoofing and session hijacking. Another name for this type of attack is Session Replay.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-600'})
SET capec.name = "Credential Stuffing",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-601'})
SET capec.name = "Jamming",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary uses radio noise or signals in an attempt to disrupt communications. By intentionally overwhelming system resources with illegitimate traffic, service is denied to the legitimate traffic of authorized users.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-602'})
SET capec.name = "DEPRECATED: Degradation",
    capec.abstraction = "Meta",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-603'})
SET capec.name = "Blockage",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary blocks the delivery of an important system resource causing the system to fail or stop working.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-604'})
SET capec.name = "Wi-Fi Jamming",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack scenario, the attacker actively transmits on the Wi-Fi channel to prevent users from transmitting or receiving data from the targeted Wi-Fi network. There are several known techniques to perform this attack \u2013 for example: the attacker may flood the Wi-Fi access point (e.g. the retransmission device) with deauthentication frames. Another method is to transmit high levels of noise on the RF band used by the Wi-Fi network.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-605'})
SET capec.name = "Cellular Jamming",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack scenario, the attacker actively transmits signals to overpower and disrupt the communication between a cellular user device and a cell tower. Several existing techniques are known in the open literature for this attack for 2G, 3G, and 4G LTE cellular technology. For example, some attacks target cell towers by overwhelming them with false status messages, while others introduce high levels of noise on signaling channels.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-606'})
SET capec.name = "Weakening of Cellular Encryption",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker, with control of a Cellular Rogue Base Station or through cooperation with a Malicious Mobile Network Operator can force the mobile device (e.g., the retransmission device) to use no encryption (A5/0 mode) or to use easily breakable encryption (A5/1 or A5/2 mode).",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-607'})
SET capec.name = "Obstruction",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An attacker obstructs the interactions between system components. By interrupting or disabling these interactions, an adversary can often force the system into a degraded state or cause the system to stop working as intended. This can cause the system components to be unavailable until the obstruction mitigated.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-608'})
SET capec.name = "Cryptanalysis of Cellular Encryption",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "The use of cryptanalytic techniques to derive cryptographic keys or otherwise effectively defeat cellular encryption to reveal traffic content. Some cellular encryption algorithms such as A5/1 and A5/2 (specified for GSM use) are known to be vulnerable to such attacks and commercial tools are available to execute these attacks and decrypt mobile phone conversations in real-time. Newer encryption algorithms in use by UMTS and LTE are stronger and currently believed to be less vulnerable to these ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-609'})
SET capec.name = "Cellular Traffic Intercept",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Cellular traffic for voice and data from mobile devices and retransmission devices can be intercepted via numerous methods. Malicious actors can deploy their own cellular tower equipment and intercept cellular traffic surreptitiously. Additionally, government agencies of adversaries and malicious actors can intercept cellular traffic via the telecommunications backbone over which mobile traffic is transmitted.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-61'})
SET capec.name = "Session Fixation",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "The attacker induces a client to establish a session with the target software using a session identifier provided by the attacker. Once the user successfully authenticates to the target software, the attacker uses the (now privileged) session identifier in their own transactions. This attack leverages the fact that the target software either relies on client-generated session identifiers or maintains the same session identifiers after privilege elevation.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-610'})
SET capec.name = "Cellular Data Injection",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "Adversaries inject data into mobile technology traffic (data flows or signaling data) to disrupt communications or conduct additional surveillance operations.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-611'})
SET capec.name = "BitSquatting",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary registers a domain name one bit different than a trusted domain. A BitSquatting attack leverages random errors in memory to direct Internet traffic to adversary-controlled destinations. BitSquatting requires no exploitation or complicated reverse engineering, and is operating system and architecture agnostic. Experimental observations show that BitSquatting popular websites could redirect non-trivial amounts of Internet traffic to a malicious entity.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-612'})
SET capec.name = "WiFi MAC Address Tracking",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack scenario, the attacker passively listens for WiFi messages and logs the associated Media Access Control (MAC) addresses. These addresses are intended to be unique to each wireless device (although they can be configured and changed by software). Once the attacker is able to associate a MAC address with a particular user or set of users (for example, when attending a public event), the attacker can then scan for that MAC address to track that user in the future.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-613'})
SET capec.name = "WiFi SSID Tracking",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack scenario, the attacker passively listens for WiFi management frame messages containing the Service Set Identifier (SSID) for the WiFi network. These messages are frequently transmitted by WiFi access points (e.g., the retransmission device) as well as by clients that are accessing the network (e.g., the handset/mobile device). Once the attacker is able to associate an SSID with a particular user or set of users (for example, when attending a public event), the attacker can then sc",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-614'})
SET capec.name = "Rooting SIM Cards",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "SIM cards are the de facto trust anchor of mobile devices worldwide. The cards protect the mobile identity of subscribers, associate devices with phone numbers, and increasingly store payment credentials, for example in NFC-enabled phones with mobile wallets. This attack leverages over-the-air (OTA) updates deployed via cryptographically-secured SMS messages to deliver executable code to the SIM. By cracking the DES key, an attacker can send properly signed binary SMS messages to a device, which",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-615'})
SET capec.name = "Evil Twin Wi-Fi Attack",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Adversaries install Wi-Fi equipment that acts as a legitimate Wi-Fi network access point. When a device connects to this access point, Wi-Fi data traffic is intercepted, captured, and analyzed. This also allows the adversary to use \"adversary-in-the-middle\" (CAPEC-94) for all communications.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-616'})
SET capec.name = "Establish Rogue Location",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary provides a malicious version of a resource at a location that is similar to the expected location of a legitimate resource. After establishing the rogue location, the adversary waits for a victim to visit the location and access the malicious resource.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-617'})
SET capec.name = "Cellular Rogue Base Station",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack scenario, the attacker imitates a cellular base station with their own \"rogue\" base station equipment. Since cellular devices connect to whatever station has the strongest signal, the attacker can easily convince a targeted cellular device (e.g. the retransmission device) to talk to the rogue base station.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-618'})
SET capec.name = "Cellular Broadcast Message Request",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack scenario, the attacker uses knowledge of the target\u2019s mobile phone number (i.e., the number associated with the SIM used in the retransmission device) to cause the cellular network to send broadcast messages to alert the mobile device. Since the network knows which cell tower the target\u2019s mobile device is attached to, the broadcast messages are only sent in the Location Area Code (LAC) where the target is currently located. By triggering the cellular broadcast message and then lis",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-619'})
SET capec.name = "Signal Strength Tracking",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack scenario, the attacker passively monitors the signal strength of the target\u2019s cellular RF signal or WiFi RF signal and uses the strength of the signal (with directional antennas and/or from multiple listening points at once) to identify the source location of the signal. Obtaining the signal of the target can be accomplished through multiple techniques such as through Cellular Broadcast Message Request or through the use of IMSI Tracking or WiFi MAC Address Tracking.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-62'})
SET capec.name = "Cross Site Request Forgery",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker crafts malicious web links and distributes them (via web pages, email, etc.), typically in a targeted manner, hoping to induce users to click on the link and execute the malicious action against some third-party application. If successful, the action embedded in the malicious link will be processed and accepted by the targeted application with the users' privilege level. This type of attack leverages the persistence and implicit trust placed in user session cookies by many web applic",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-620'})
SET capec.name = "Drop Encryption Level",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker forces the encryption level to be lowered, thus enabling a successful attack against the encrypted data.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-621'})
SET capec.name = "Analysis of Packet Timing and Sizes",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker may intercept and log encrypted transmissions for the purpose of analyzing metadata such as packet timing and sizes. Although the actual data may be encrypted, this metadata may reveal valuable information to an attacker. Note that this attack is applicable to VOIP data as well as application data, especially for interactive apps that require precise timing and low-latency (e.g. thin-clients).",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-622'})
SET capec.name = "Electromagnetic Side-Channel Attack",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "In this attack scenario, the attacker passively monitors electromagnetic emanations that are produced by the targeted electronic device as an unintentional side-effect of its processing. From these emanations, the attacker derives information about the data that is being processed (e.g. the attacker can recover cryptographic keys by monitoring emanations associated with cryptographic processing). This style of attack requires proximal access to the device, however attacks have been demonstrated ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-623'})
SET capec.name = "Compromising Emanations Attack",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Compromising Emanations (CE) are defined as unintentional signals which an attacker may intercept and analyze to disclose the information processed by the targeted equipment. Commercial mobile devices and retransmission devices have displays, buttons, microchips, and radios that emit mechanical emissions in the form of sound or vibrations. Capturing these emissions can help an adversary understand what the device is doing.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-624'})
SET capec.name = "Hardware Fault Injection",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "The adversary uses disruptive signals or events, or alters the physical environment a device operates in, to cause faulty behavior in electronic devices. This can include electromagnetic pulses, laser pulses, clock glitches, ambient temperature extremes, and more. When performed in a controlled manner on devices performing cryptographic operations, this faulty behavior can be exploited to derive secret key information.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-625'})
SET capec.name = "Mobile Device Fault Injection",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "Fault injection attacks against mobile devices use disruptive signals or events (e.g. electromagnetic pulses, laser pulses, clock glitches, etc.) to cause faulty behavior. When performed in a controlled manner on devices performing cryptographic operations, this faulty behavior can be exploited to derive secret key information. Although this attack usually requires physical control of the mobile device, it is non-destructive, and the device can be used after the attack without any indication tha",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-626'})
SET capec.name = "Smudge Attack",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Attacks that reveal the password/passcode pattern on a touchscreen device by detecting oil smudges left behind by the user\u2019s fingers.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-627'})
SET capec.name = "Counterfeit GPS Signals",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary attempts to deceive a GPS receiver by broadcasting counterfeit GPS signals, structured to resemble a set of normal GPS signals. These spoofed signals may be structured in such a way as to cause the receiver to estimate its position to be somewhere other than where it actually is, or to be located where it is but at a different time, as determined by the adversary.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-628'})
SET capec.name = "Carry-Off GPS Attack",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "A common form of a GPS spoofing attack, commonly termed a carry-off attack begins with an adversary broadcasting signals synchronized with the genuine signals observed by the target receiver. The power of the counterfeit signals is then gradually increased and drawn away from the genuine signals. Over time, the adversary can carry the target away from their intended destination and toward a location chosen by the adversary.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-629'})
SET capec.name = "DEPRECATED: Unauthorized Use of Device Resources",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-63'})
SET capec.name = "Cross-Site Scripting (XSS)",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary embeds malicious scripts in content that will be served to web browsers. The goal of the attack is for the target software, the client-side browser, to execute the script with the users' privilege level. An attack of this type exploits a programs' vulnerabilities that are brought on by allowing remote hosts to execute code and scripts. Web browsers, for example, have some simple security controls in place, but if a remote attacker is allowed to execute scripts (through injecting the",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-630'})
SET capec.name = "TypoSquatting",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary registers a domain name with at least one character different than a trusted domain. A TypoSquatting attack takes advantage of instances where a user mistypes a URL (e.g. www.goggle.com) or not does visually verify a URL before clicking on it (e.g. phishing attack). As a result, the user is directed to an adversary-controlled destination. TypoSquatting does not require an attack against the trusted domain or complicated reverse engineering.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-631'})
SET capec.name = "SoundSquatting",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary registers a domain name that sounds the same as a trusted domain, but has a different spelling. A SoundSquatting attack takes advantage of a user's confusion of the two words to direct Internet traffic to adversary-controlled destinations. SoundSquatting does not require an attack against the trusted domain or complicated reverse engineering.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-632'})
SET capec.name = "Homograph Attack via Homoglyphs",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary registers a domain name containing a homoglyph, leading the registered domain to appear the same as a trusted domain. A homograph attack leverages the fact that different characters among various character sets look the same to the user. Homograph attacks must generally be combined with other attacks, such as phishing attacks, in order to direct Internet traffic to the adversary-controlled destinations.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-633'})
SET capec.name = "Token Impersonation",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary exploits a weakness in authentication to create an access token (or equivalent) that impersonates a different entity, and then associates a process/thread to that that impersonated token. This action causes a downstream user to make a decision or take action that is based on the assumed identity, and not the response that blocks the adversary.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-634'})
SET capec.name = "Probe Audio and Video Peripherals",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "The adversary exploits the target system's audio and video functionalities through malware or scheduled tasks. The goal is to capture sensitive information about the target for financial, personal, political, or other gains which is accomplished by collecting communication data between two parties via the use of peripheral devices (e.g. microphones and webcams) or applications with audio and video capabilities (e.g. Skype) on a system.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-635'})
SET capec.name = "Alternative Execution Due to Deceptive Filenames",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "The extension of a file name is often used in various contexts to determine the application that is used to open and use it. If an attacker can cause an alternative application to be used, it may be able to execute malicious code, cause a denial of service or expose sensitive information.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-636'})
SET capec.name = "Hiding Malicious Data or Code within Files",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "Files on various operating systems can have a complex format which allows for the storage of other data, in addition to its contents. Often this is metadata about the file, such as a cached thumbnail for an image file. Unless utilities are invoked in a particular way, this data is not visible during the normal use of the file. It is possible for an attacker to store malicious data or code using these facilities, which would be difficult to discover.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-637'})
SET capec.name = "Collect Data from Clipboard",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "The adversary exploits an application that allows for the copying of sensitive data or information by collecting information copied to the clipboard. Data copied to the clipboard can be accessed by other applications, such as malware built to exfiltrate or log clipboard contents on a periodic basis. In this way, the adversary aims to garner information to which they are unauthorized.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-638'})
SET capec.name = "Altered Component Firmware",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary exploits systems features and/or improperly protected firmware of hardware components, such as Hard Disk Drives (HDD), with the goal of executing malicious code from within the component's Master Boot Record (MBR). Conducting this type of attack entails the adversary infecting the target with firmware altering malware, using known tools, and a payload. Once this malware is executed, the MBR is modified to include instructions to execute the payload at desired intervals and when the ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-639'})
SET capec.name = "Probe System Files",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary obtains unauthorized information due to improperly protected files. If an application stores sensitive information in a file that is not protected by proper access control, then an adversary can access the file and search for sensitive information.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-64'})
SET capec.name = "Using Slashes and URL Encoding Combined to Bypass Validation Logic",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack targets the encoding of the URL combined with the encoding of the slash characters. An attacker can take advantage of the multiple ways of encoding a URL and abuse the interpretation of the URL. A URL may contain special character that need special syntax handling in order to be interpreted. Special characters are represented using a percentage character followed by two digits representing the octet code of the original character (%HEX-CODE). For instance US-ASCII space character wou",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-640'})
SET capec.name = "Inclusion of Code in Existing Process",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "The adversary takes advantage of a bug in an application failing to verify the integrity of the running process to execute arbitrary code in the address space of a separate live process. The adversary could use running code in the context of another process to try to access process's memory, system/network resources, etc. The goal of this attack is to evade detection defenses and escalate privileges by masking the malicious code under an existing legitimate process. Examples of approaches includ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-641'})
SET capec.name = "DLL Side-Loading",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary places a malicious version of a Dynamic-Link Library (DLL) in the Windows Side-by-Side (WinSxS) directory to trick the operating system into loading this malicious DLL instead of a legitimate DLL. Programs specify the location of the DLLs to load via the use of WinSxS manifests or DLL redirection and if they aren't used then Windows searches in a predefined set of directories to locate the file. If the applications improperly specify a required DLL or WinSxS manifests aren't explici",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-642'})
SET capec.name = "Replace Binaries",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Adversaries know that certain binaries will be regularly executed as part of normal processing. If these binaries are not protected with the appropriate file system permissions, it could be possible to replace them with malware. This malware might be executed at higher system permission levels. A variation of this pattern is to discover self-extracting installation packages that unpack binaries to directories with weak file permissions which it does not clean up appropriately. These binaries can",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-643'})
SET capec.name = "Identify Shared Files/Directories on System",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary discovers connections between systems by exploiting the target system's standard practice of revealing them in searchable, common areas. Through the identification of shared folders/drives between systems, the adversary may further their goals of locating and collecting sensitive information/files, or map potential routes for lateral movement within the network.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-644'})
SET capec.name = "Use of Captured Hashes (Pass The Hash)",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary obtains (i.e. steals or purchases) legitimate Windows domain credential hash values to access systems within the domain that leverage the Lan Man (LM) and/or NT Lan Man (NTLM) authentication protocols.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-645'})
SET capec.name = "Use of Captured Tickets (Pass The Ticket)",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary uses stolen Kerberos tickets to access systems/resources that leverage the Kerberos authentication protocol. The Kerberos authentication protocol centers around a ticketing system which is used to request/grant access to services and to then access the requested services. An adversary can obtain any one of these tickets (e.g. Service Ticket, Ticket Granting Ticket, Silver Ticket, or Golden Ticket) to authenticate to a system/resource without needing the account's credentials. Depend",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-646'})
SET capec.name = "Peripheral Footprinting",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "Adversaries may attempt to obtain information about attached peripheral devices and components connected to a computer system. Examples may include discovering the presence of iOS devices by searching for backups, analyzing the Windows registry to determine what USB devices have been connected, or infecting a victim system with malware to report when a USB device has been connected. This may allow the adversary to gain additional insight about the system or network environment, which may be usef",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-647'})
SET capec.name = "Collect Data from Registries",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary exploits a weakness in authorization to gather system-specific data and sensitive information within a registry (e.g., Windows Registry, Mac plist). These contain information about the system configuration, software, operating system, and security. The adversary can leverage information gathered in order to carry out further attacks.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-648'})
SET capec.name = "Collect Data from Screen Capture",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary gathers sensitive information by exploiting the system's screen capture functionality. Through screenshots, the adversary aims to see what happens on the screen over the course of an operation. The adversary can leverage information gathered in order to carry out further attacks.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-649'})
SET capec.name = "Adding a Space to a File Extension",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary adds a space character to the end of a file extension and takes advantage of an application that does not properly neutralize trailing special elements in file names. This extra space, which can be difficult for a user to notice, affects which default application is used to operate on the file and can be leveraged by the adversary to control execution.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-65'})
SET capec.name = "Sniff Application Code",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary passively sniffs network communications and captures application code bound for an authorized client. Once obtained, they can use it as-is, or through reverse-engineering glean sensitive information or exploit the trust relationship between the client and server. Such code may belong to a dynamic update to the client, a patch being applied to a client component or any such interaction where the client is authorized to communicate with the server.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-650'})
SET capec.name = "Upload a Web Shell to a Web Server",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "By exploiting insufficient permissions, it is possible to upload a web shell to a web server in such a way that it can be executed remotely. This shell can have various capabilities, thereby acting as a \"gateway\" to the underlying web server. The shell might execute at the higher permission level of the web server, providing the ability the execute malicious code at elevated levels.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-651'})
SET capec.name = "Eavesdropping",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary intercepts a form of communication (e.g. text, audio, video) by way of software (e.g., microphone and audio recording application), hardware (e.g., recording equipment), or physical means (e.g., physical proximity). The goal of eavesdropping is typically to gain unauthorized access to sensitive information about the target for financial, personal, political, or other gains. Eavesdropping is different from a sniffing attack as it does not take place on a network-based communication c",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-652'})
SET capec.name = "Use of Known Kerberos Credentials",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary obtains (i.e. steals or purchases) legitimate Kerberos credentials (e.g. Kerberos service account userID/password or Kerberos Tickets) with the goal of achieving authenticated access to additional systems, applications, or services within the domain.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-653'})
SET capec.name = "Use of Known Operating System Credentials",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary guesses or obtains (i.e. steals or purchases) legitimate operating system credentials (e.g. userID/password) to achieve authentication and to perform authorized actions on the system, under the guise of an authenticated user or service. This applies to any Operating System.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-654'})
SET capec.name = "Credential Prompt Impersonation",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary, through a previously installed malicious application, impersonates a credential prompt in an attempt to steal a user's credentials.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-655'})
SET capec.name = "Avoid Security Tool Identification by Adding Data",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-656'})
SET capec.name = "Voice Phishing",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary targets users with a phishing attack for the purpose of soliciting account passwords or sensitive information from the user. Voice Phishing is a variation of the Phishing social engineering technique where the attack is initiated via a voice call, rather than email. The user is enticed to provide sensitive information by the adversary, who masquerades as a legitimate employee of the alleged organization. Voice Phishing attacks deviate from standard Phishing attacks, in that a user d",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-657'})
SET capec.name = "Malicious Automated Software Update via Spoofing",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attackers uses identify or content spoofing to trick a client into performing an automated software update from a malicious source. A malicious automated software update that leverages spoofing can include content or identity spoofing as well as protocol spoofing. Content or identity spoofing attacks can trigger updates in software by embedding scripted mechanisms within a malicious web page, which masquerades as a legitimate update source. Scripting mechanisms communicate with software compo",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-66'})
SET capec.name = "SQL Injection",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "This attack exploits target software that constructs SQL statements based on user input. An attacker crafts input strings so that when the target software constructs SQL statements based on the input, the resulting SQL statement performs actions other than those the application intended. SQL Injection results from failure of the application to appropriately validate input.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-660'})
SET capec.name = "Root/Jailbreak Detection Evasion via Hooking",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary forces a non-restricted mobile application to load arbitrary code or code files, via Hooking, with the goal of evading Root/Jailbreak detection. Mobile device users often Root/Jailbreak their devices in order to gain administrative control over the mobile operating system and/or to install third-party mobile applications that are not provided by authorized application stores (e.g. Google Play Store and Apple App Store). Adversaries may further leverage these capabilities to escalate",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-661'})
SET capec.name = "Root/Jailbreak Detection Evasion via Debugging",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "An adversary inserts a debugger into the program entry point of a mobile application to modify the application binary, with the goal of evading Root/Jailbreak detection. Mobile device users often Root/Jailbreak their devices in order to gain administrative control over the mobile operating system and/or to install third-party mobile applications that are not provided by authorized application stores (e.g. Google Play Store and Apple App Store). Rooting/Jailbreaking a mobile device also provides ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-662'})
SET capec.name = "Adversary in the Browser (AiTB)",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-663'})
SET capec.name = "Exploitation of Transient Instruction Execution",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "An adversary exploits a hardware design flaw in a CPU implementation of transient instruction execution to expose sensitive data and bypass/subvert access control over restricted resources. Typically, the adversary conducts a covert channel attack to target non-discarded microarchitectural changes caused by transient executions such as speculative execution, branch prediction, instruction pipelining, and/or out-of-order execution. The transient execution results in a series of instructions (gadg",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-664'})
SET capec.name = "Server Side Request Forgery",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-665'})
SET capec.name = "Exploitation of Thunderbolt Protection Flaws",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-666'})
SET capec.name = "BlueSmacking",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary uses Bluetooth flooding to transfer large packets to Bluetooth enabled devices over the L2CAP protocol with the goal of creating a DoS. This attack must be carried out within close proximity to a Bluetooth enabled device.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-667'})
SET capec.name = "Bluetooth Impersonation AttackS (BIAS)",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary disguises the MAC address of their Bluetooth enabled device to one for which there exists an active and trusted connection and authenticates successfully. The adversary can then perform malicious actions on the target Bluetooth device depending on the target\u2019s capabilities.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-668'})
SET capec.name = "Key Negotiation of Bluetooth Attack (KNOB)",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary can exploit a flaw in Bluetooth key negotiation allowing them to decrypt information sent between two devices communicating via Bluetooth. The adversary uses an Adversary in the Middle setup to modify packets sent between the two devices during the authentication process, specifically the entropy bits. Knowledge of the number of entropy bits will allow the attacker to easily decrypt information passing over the line of communication.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-669'})
SET capec.name = "Alteration of a Software Update",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-67'})
SET capec.name = "String Format Overflow in syslog()",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack targets applications and software that uses the syslog() function insecurely. If an application does not explicitely use a format string parameter in a call to syslog(), user input can be placed in the format string parameter leading to a format string injection attack. Adversaries can then inject malicious format string commands into the function call leading to a buffer overflow. There are many reported software vulnerabilities with the root cause being a misuse of the syslog() fun",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-670'})
SET capec.name = "Software Development Tools Maliciously Altered",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary with the ability to alter tools used in a development environment causes software to be developed with maliciously modified tools. Such tools include requirements management and database tools, software design tools, configuration management tools, compilers, system build tools, and software performance testing and load testing tools. The adversary then carries out malicious acts once the software is deployed including malware infection of other systems to support further compromise",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-671'})
SET capec.name = "Requirements for ASIC Functionality Maliciously Altered",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary with access to functional requirements for an application specific integrated circuit (ASIC), a chip designed/customized for a singular particular use, maliciously alters requirements derived from originating capability needs. In the chip manufacturing process, requirements drive the chip design which, when the chip is fully manufactured, could result in an ASIC which may not meet the user\u2019s needs, contain malicious functionality, or exhibit other anomalous behaviors thereby affecti",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-672'})
SET capec.name = "Malicious Code Implanted During Chip Programming",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-673'})
SET capec.name = "Developer Signing Maliciously Altered Software",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-674'})
SET capec.name = "Design for FPGA Maliciously Altered",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-675'})
SET capec.name = "Retrieve Data from Decommissioned Devices",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-676'})
SET capec.name = "NoSQL Injection",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-677'})
SET capec.name = "Server Motherboard Compromise",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-678'})
SET capec.name = "System Build Data Maliciously Altered",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-679'})
SET capec.name = "Exploitation of Improperly Configured or Implemented Memory Protections",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-68'})
SET capec.name = "Subvert Code-signing Facilities",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "Many languages use code signing facilities to vouch for code's identity and to thus tie code to its assigned privileges within an environment. Subverting this mechanism can be instrumental in an attacker escalating privilege. Any means of subverting the way that a virtual machine enforces code signing classifies for this style of attack.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-680'})
SET capec.name = "Exploitation of Improperly Controlled Registers",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-681'})
SET capec.name = "Exploitation of Improperly Controlled Hardware Security Identifiers",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-682'})
SET capec.name = "Exploitation of Firmware or ROM Code with Unpatchable Vulnerabilities",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary may exploit vulnerable code (i.e., firmware or ROM) that is unpatchable. Unpatchable devices exist due to manufacturers intentionally or inadvertently designing devices incapable of updating their software. Additionally, with updatable devices, the manufacturer may decide not to support the device and stop making updates to their software.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-69'})
SET capec.name = "Target Programs with Elevated Privileges",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "This attack targets programs running with elevated privileges. The adversary tries to leverage a vulnerability in the running program and get arbitrary code to execute with elevated privileges.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-690'})
SET capec.name = "Metadata Spoofing",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-691'})
SET capec.name = "Spoof Open-Source Software Metadata",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-692'})
SET capec.name = "Spoof Version Control System Commit Metadata",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-693'})
SET capec.name = "StarJacking",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-694'})
SET capec.name = "System Location Discovery",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-695'})
SET capec.name = "Repo Jacking",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-696'})
SET capec.name = "Load Value Injection",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary exploits a hardware design flaw in a CPU implementation of transient instruction execution in which a faulting or assisted load instruction transiently forwards adversary-controlled data from microarchitectural buffers. By inducing a page fault or microcode assist during victim execution, an adversary can force legitimate victim execution to operate on the adversary-controlled data which is stored in the microarchitectural buffers. The adversary can then use existing code gadgets an",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-697'})
SET capec.name = "DHCP Spoofing",
    capec.abstraction = "Standard",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-698'})
SET capec.name = "Install Malicious Extension",
    capec.abstraction = "Detailed",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-699'})
SET capec.name = "Eavesdropping on a Monitor",
    capec.abstraction = "Meta",
    capec.status = "Draft",
    capec.description = "An Adversary can eavesdrop on the content of an external monitor through the air without modifying any cable or installing software, just capturing this signal emitted by the cable or video port, with this the attacker will be able to impact the confidentiality of the data without being detected by traditional security tools",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-7'})
SET capec.name = "Blind SQL Injection",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Blind SQL Injection results from an insufficient mitigation for SQL Injection. Although suppressing database error messages are considered best practice, the suppression alone is not sufficient to prevent SQL Injection. Blind SQL Injection is a form of SQL Injection that overcomes the lack of error messages. Without the error messages that facilitate SQL Injection, the adversary constructs input strings that probe the target through simple Boolean SQL expressions. The adversary can determine if ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-70'})
SET capec.name = "Try Common or Default Usernames and Passwords",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary may try certain common or default usernames and passwords to gain access into the system and perform unauthorized actions. An adversary may try an intelligent brute force using empty passwords, known vendor default credentials, as well as a dictionary of common usernames and passwords. Many vendor products come preconfigured with default (and thus well-known) usernames and passwords that should be deleted prior to usage in a production environment. It is a common mistake to forget t",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-700'})
SET capec.name = "Network Boundary Bridging",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary which has gained elevated access to network boundary devices may use these devices to create a channel to bridge trusted and untrusted networks. Boundary devices do not necessarily have to be on the network\u2019s edge, but rather must serve to segment portions of the target network the adversary wishes to cross into.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-701'})
SET capec.name = "Browser in the Middle (BiTM)",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary exploits the inherent functionalities of a web browser, in order to establish an unnoticed remote desktop connection in the victim's browser to the adversary's system. The adversary must deploy a web client with a remote desktop session that the victim can access.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-702'})
SET capec.name = "Exploiting Incorrect Chaining or Granularity of Hardware Debug Components",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-71'})
SET capec.name = "Using Unicode Encoding to Bypass Validation Logic",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker may provide a Unicode string to a system component that is not Unicode aware and use that to circumvent the filter or cause the classifying mechanism to fail to properly understanding the request. That may allow the attacker to slip malicious data past the content filter and/or possibly cause the application to route the request incorrectly.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-72'})
SET capec.name = "URL Encoding",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack targets the encoding of the URL. An adversary can take advantage of the multiple way of encoding an URL and abuse the interpretation of the URL.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-73'})
SET capec.name = "User-Controlled Filename",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attack of this type involves an adversary inserting malicious characters (such as a XSS redirection) into a filename, directly or indirectly that is then used by the target software to generate HTML text or other potentially executable content. Many websites rely on user-generated content and dynamically build resources like files, filenames, and URL links directly from user supplied data. In this attack pattern, the attacker uploads code that can execute in the client browser and/or redirect",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-74'})
SET capec.name = "Manipulating State",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-75'})
SET capec.name = "Manipulating Writeable Configuration Files",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "Generally these are manually edited files that are not in the preview of the system administrators, any ability on the attackers' behalf to modify these files, for example in a CVS repository, gives unauthorized access directly to the application, the same as authorized users.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-76'})
SET capec.name = "Manipulating Web Input to File System Calls",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker manipulates inputs to the target software which the target software passes to file system calls in the OS. The goal is to gain access to, and perhaps modify, areas of the file system that the target software did not intend to be accessible.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-77'})
SET capec.name = "Manipulating User-Controlled Variables",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "This attack targets user controlled variables (DEBUG=1, PHP Globals, and So Forth). An adversary can override variables leveraging user-supplied, untrusted query variables directly used on the application server without any data sanitization. In extreme cases, the adversary can change variables controlling the business logic of the application. For instance, in languages like PHP, a number of poorly set default configurations may allow the user to override variables.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-78'})
SET capec.name = "Using Escaped Slashes in Alternate Encoding",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack targets the use of the backslash in alternate encoding. An adversary can provide a backslash as a leading character and causes a parser to believe that the next character is special. This is called an escape. By using that trick, the adversary tries to exploit alternate ways to encode the same character which leads to filter problems and opens avenues to attack.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-79'})
SET capec.name = "Using Slashes in Alternate Encoding",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack targets the encoding of the Slash characters. An adversary would try to exploit common filtering problems related to the use of the slashes characters to gain access to resources on the target host. Directory-driven systems, such as file systems and databases, typically use the slash character to indicate traversal between directories or other container components. For murky historical reasons, PCs (and, as a result, Microsoft OSs) choose to use a backslash, whereas the UNIX world ty",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-8'})
SET capec.name = "Buffer Overflow in an API Call",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack targets libraries or shared code modules which are vulnerable to buffer overflow attacks. An adversary who has knowledge of known vulnerable libraries or shared code can easily target software that makes use of these libraries. All clients that make use of the code library thus become vulnerable by association. This has a very broad effect on security across a system, usually affecting more than one software process.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-80'})
SET capec.name = "Using UTF-8 Encoding to Bypass Validation Logic",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack is a specific variation on leveraging alternate encodings to bypass validation logic. This attack leverages the possibility to encode potentially harmful input in UTF-8 and submit it to applications not expecting or effective at validating this encoding standard making input filtering difficult. UTF-8 (8-bit UCS/Unicode Transformation Format) is a variable-length character encoding for Unicode. Legal UTF-8 characters are one to four bytes long. However, early version of the UTF-8 spe",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-81'})
SET capec.name = "Web Server Logs Tampering",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "Web Logs Tampering attacks involve an attacker injecting, deleting or otherwise tampering with the contents of web logs typically for the purposes of masking other malicious behavior. Additionally, writing malicious data to log files may target jobs, filters, reports, and other agents that process the logs in an asynchronous attack pattern. This pattern of attack is similar to \"Log Injection-Tampering-Forging\" except that in this case, the attack is targeting the logs of the web server and not t",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-82'})
SET capec.name = "DEPRECATED: Violating Implicit Assumptions Regarding XML Content (aka XML Denial of Service (XDoS))",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it a generalization of CAPEC-230: XML Nested Payloads, CAPEC-231: XML Oversized Payloads, and CAPEC-147: XML Ping of Death. Please refer to these CAPECs going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-83'})
SET capec.name = "XPath Injection",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An attacker can craft special user-controllable input consisting of XPath expressions to inject the XML database and bypass authentication or glean information that they normally would not be able to. XPath Injection enables an attacker to talk directly to the XML database, thus bypassing the application completely. XPath Injection results from the failure of an application to properly sanitize input used as part of dynamic XPath expressions used to query an XML database.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-84'})
SET capec.name = "XQuery Injection",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack utilizes XQuery to probe and attack server systems; in a similar manner that SQL Injection allows an attacker to exploit SQL calls to RDBMS, XQuery Injection uses improperly validated data that is passed to XQuery commands to traverse and execute commands that the XQuery routines have access to. XQuery injection can be used to enumerate elements on the victim's environment, inject commands to the local host, or execute queries to remote files and data sources.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-85'})
SET capec.name = "AJAX Footprinting",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack utilizes the frequent client-server roundtrips in Ajax conversation to scan a system. While Ajax does not open up new vulnerabilities per se, it does optimize them from an attacker point of view. A common first step for an attacker is to footprint the target environment to understand what attacks will work. Since footprinting relies on enumeration, the conversational pattern of rapid, multiple requests and responses that are typical in Ajax applications enable an attacker to look for",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-86'})
SET capec.name = "XSS Through HTTP Headers",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An adversary exploits web applications that generate web content, such as links in a HTML page, based on unvalidated or improperly validated data submitted by other actors. XSS in HTTP Headers attacks target the HTTP headers which are hidden from most users and may not be validated by web applications.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-87'})
SET capec.name = "Forceful Browsing",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An attacker employs forceful browsing (direct URL entry) to access portions of a website that are otherwise unreachable. Usually, a front controller or similar design pattern is employed to protect access to portions of a web application. Forceful browsing enables an attacker to access information, perform privileged operations and otherwise reach sections of the web application that have been improperly protected.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-88'})
SET capec.name = "OS Command Injection",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "In this type of an attack, an adversary injects operating system commands into existing application functions. An application that uses untrusted input to build command strings is vulnerable. An adversary can leverage OS command injection in an application to elevate privileges, execute arbitrary commands and compromise the underlying operating system.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-89'})
SET capec.name = "Pharming",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "A pharming attack occurs when the victim is fooled into entering sensitive data into supposedly trusted locations, such as an online bank site or a trading platform. An attacker can impersonate these supposedly trusted sites and have the victim be directed to their site rather than the originally intended one. Pharming does not require script injection or clicking on malicious links for the attack to succeed.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-9'})
SET capec.name = "Buffer Overflow in Local Command-Line Utilities",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack targets command-line utilities available in a number of shells. An adversary can leverage a vulnerability found in a command-line utility to escalate privilege to root.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-90'})
SET capec.name = "Reflection Attack in Authentication Protocol",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "An adversary can abuse an authentication protocol susceptible to reflection attack in order to defeat it. Doing so allows the adversary illegitimate access to the target system, without possessing the requisite credentials. Reflection attacks are of great concern to authentication protocols that rely on a challenge-handshake or similar mechanism. An adversary can impersonate a legitimate user and can gain illegitimate access to the system by successfully mounting a reflection attack during authe",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-91'})
SET capec.name = "DEPRECATED: XSS in IMG Tags",
    capec.abstraction = "Detailed",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it is contained in the existing attack pattern \"CAPEC-18 : XSS Targeting Non-Script Elements\". Please refer to this other CAPEC going forward.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-92'})
SET capec.name = "Forced Integer Overflow",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack forces an integer variable to go out of range. The integer variable is often used as an offset such as size of memory allocation or similarly. The attacker would typically control the value of such variable and try to get it out of range. For instance the integer in question is incremented past the maximum possible value, it may wrap to become a very small, or negative number, therefore providing a very incorrect value which can lead to unexpected behavior. At worst the attacker can ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-93'})
SET capec.name = "Log Injection-Tampering-Forging",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack targets the log files of the target host. The attacker injects, manipulates or forges malicious log entries in the log file, allowing them to mislead a log audit, cover traces of attack, or perform other malicious actions. The target host is not properly controlling log access. As a result tainted data is resulting in the log files leading to a failure in accountability, non-repudiation and incident forensics capability.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-94'})
SET capec.name = "Adversary in the Middle (AiTM)",
    capec.abstraction = "Meta",
    capec.status = "Stable",
    capec.description = "\n            ",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-95'})
SET capec.name = "WSDL Scanning",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "This attack targets the WSDL interface made available by a web service. The attacker may scan the WSDL interface to reveal sensitive information about invocation patterns, underlying technology implementations and associated vulnerabilities. This type of probing is carried out to perform more serious attacks (e.g. parameter tampering, malicious content injection, command injection, etc.). WSDL files provide detailed information about the services ports and bindings available to consumers. For in",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-96'})
SET capec.name = "Block Access to Libraries",
    capec.abstraction = "Detailed",
    capec.status = "Draft",
    capec.description = "An application typically makes calls to functions that are a part of libraries external to the application. These libraries may be part of the operating system or they may be third party libraries. It is possible that the application does not handle situations properly where access to these libraries has been blocked. Depending on the error handling within the application, blocked access to libraries may leave the system in an insecure state that could be leveraged by an attacker.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-97'})
SET capec.name = "Cryptanalysis",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "Cryptanalysis is a process of finding weaknesses in cryptographic algorithms and using these weaknesses to decipher the ciphertext without knowing the secret key (instance deduction). Sometimes the weakness is not in the cryptographic algorithm itself, but rather in how it is applied that makes cryptanalysis successful. An attacker may have other goals as well, such as: Total Break (finding the secret key), Global Deduction (finding a functionally equivalent algorithm for encryption and decrypti",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-98'})
SET capec.name = "Phishing",
    capec.abstraction = "Standard",
    capec.status = "Draft",
    capec.description = "Phishing is a social engineering technique where an attacker masquerades as a legitimate entity with which the victim might do business in order to prompt the user to reveal some confidential information (very frequently authentication credentials) that can later be used by an attacker. Phishing is essentially a form of information gathering or \"fishing\" for information.",
    capec.source = 'CAPEC_v3.9_XML';


MERGE (capec:AttackPattern {id: 'CAPEC-99'})
SET capec.name = "DEPRECATED: XML Parser Attack",
    capec.abstraction = "Standard",
    capec.status = "Deprecated",
    capec.description = "This attack pattern has been deprecated as it a generalization of CAPEC-230: XML Nested Payloads and CAPEC-231: XML Oversized Payloads. Please refer to these CAPECs going forward.",
    capec.source = 'CAPEC_v3.9_XML';


// ========================================
// 2. CREATE CAPEC→CWE RELATIONSHIPS
// Total: 1214 relationships
// ========================================


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-276'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-434'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-732'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-1191'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-1193'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-1220'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-1297'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-1311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-1314'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-1315'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-1318'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-1320'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-1321'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MATCH (cwe:Weakness {id: 'CWE-1327'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-10'})
MATCH (cwe:Weakness {id: 'CWE-120'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-10'})
MATCH (cwe:Weakness {id: 'CWE-302'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-10'})
MATCH (cwe:Weakness {id: 'CWE-118'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-10'})
MATCH (cwe:Weakness {id: 'CWE-119'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-10'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-10'})
MATCH (cwe:Weakness {id: 'CWE-99'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-10'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-10'})
MATCH (cwe:Weakness {id: 'CWE-680'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-10'})
MATCH (cwe:Weakness {id: 'CWE-733'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-10'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-100'})
MATCH (cwe:Weakness {id: 'CWE-120'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-100'})
MATCH (cwe:Weakness {id: 'CWE-119'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-100'})
MATCH (cwe:Weakness {id: 'CWE-131'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-100'})
MATCH (cwe:Weakness {id: 'CWE-129'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-100'})
MATCH (cwe:Weakness {id: 'CWE-805'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-100'})
MATCH (cwe:Weakness {id: 'CWE-680'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-101'})
MATCH (cwe:Weakness {id: 'CWE-97'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-101'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-101'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-102'})
MATCH (cwe:Weakness {id: 'CWE-294'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-102'})
MATCH (cwe:Weakness {id: 'CWE-522'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-102'})
MATCH (cwe:Weakness {id: 'CWE-523'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-102'})
MATCH (cwe:Weakness {id: 'CWE-319'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-102'})
MATCH (cwe:Weakness {id: 'CWE-614'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-103'})
MATCH (cwe:Weakness {id: 'CWE-1021'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-104'})
MATCH (cwe:Weakness {id: 'CWE-250'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-104'})
MATCH (cwe:Weakness {id: 'CWE-638'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-104'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-104'})
MATCH (cwe:Weakness {id: 'CWE-116'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-104'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-105'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-105'})
MATCH (cwe:Weakness {id: 'CWE-113'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-105'})
MATCH (cwe:Weakness {id: 'CWE-138'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-105'})
MATCH (cwe:Weakness {id: 'CWE-436'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-107'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-107'})
MATCH (cwe:Weakness {id: 'CWE-648'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-108'})
MATCH (cwe:Weakness {id: 'CWE-89'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-108'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-108'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-108'})
MATCH (cwe:Weakness {id: 'CWE-78'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-108'})
MATCH (cwe:Weakness {id: 'CWE-114'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-109'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-109'})
MATCH (cwe:Weakness {id: 'CWE-89'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-109'})
MATCH (cwe:Weakness {id: 'CWE-564'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-11'})
MATCH (cwe:Weakness {id: 'CWE-430'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-110'})
MATCH (cwe:Weakness {id: 'CWE-89'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-110'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-111'})
MATCH (cwe:Weakness {id: 'CWE-345'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-111'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-111'})
MATCH (cwe:Weakness {id: 'CWE-352'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-112'})
MATCH (cwe:Weakness {id: 'CWE-330'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-112'})
MATCH (cwe:Weakness {id: 'CWE-326'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-112'})
MATCH (cwe:Weakness {id: 'CWE-521'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-113'})
MATCH (cwe:Weakness {id: 'CWE-1192'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-114'})
MATCH (cwe:Weakness {id: 'CWE-287'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-114'})
MATCH (cwe:Weakness {id: 'CWE-1244'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-115'})
MATCH (cwe:Weakness {id: 'CWE-287'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-116'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-116'})
MATCH (cwe:Weakness {id: 'CWE-1243'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-117'})
MATCH (cwe:Weakness {id: 'CWE-319'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-12'})
MATCH (cwe:Weakness {id: 'CWE-201'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-12'})
MATCH (cwe:Weakness {id: 'CWE-306'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-120'})
MATCH (cwe:Weakness {id: 'CWE-173'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-120'})
MATCH (cwe:Weakness {id: 'CWE-172'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-120'})
MATCH (cwe:Weakness {id: 'CWE-177'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-120'})
MATCH (cwe:Weakness {id: 'CWE-181'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-120'})
MATCH (cwe:Weakness {id: 'CWE-183'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-120'})
MATCH (cwe:Weakness {id: 'CWE-184'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-120'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-120'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-120'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-120'})
MATCH (cwe:Weakness {id: 'CWE-692'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-121'})
MATCH (cwe:Weakness {id: 'CWE-489'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-121'})
MATCH (cwe:Weakness {id: 'CWE-1209'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-121'})
MATCH (cwe:Weakness {id: 'CWE-1259'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-121'})
MATCH (cwe:Weakness {id: 'CWE-1267'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-121'})
MATCH (cwe:Weakness {id: 'CWE-1270'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-121'})
MATCH (cwe:Weakness {id: 'CWE-1294'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-121'})
MATCH (cwe:Weakness {id: 'CWE-1295'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-121'})
MATCH (cwe:Weakness {id: 'CWE-1296'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-121'})
MATCH (cwe:Weakness {id: 'CWE-1302'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-121'})
MATCH (cwe:Weakness {id: 'CWE-1313'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-122'})
MATCH (cwe:Weakness {id: 'CWE-269'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-122'})
MATCH (cwe:Weakness {id: 'CWE-732'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-122'})
MATCH (cwe:Weakness {id: 'CWE-1317'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-123'})
MATCH (cwe:Weakness {id: 'CWE-119'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-124'})
MATCH (cwe:Weakness {id: 'CWE-1189'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-124'})
MATCH (cwe:Weakness {id: 'CWE-1331'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-125'})
MATCH (cwe:Weakness {id: 'CWE-404'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-125'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-126'})
MATCH (cwe:Weakness {id: 'CWE-22'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-127'})
MATCH (cwe:Weakness {id: 'CWE-424'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-127'})
MATCH (cwe:Weakness {id: 'CWE-425'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-127'})
MATCH (cwe:Weakness {id: 'CWE-288'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-127'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-127'})
MATCH (cwe:Weakness {id: 'CWE-732'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-127'})
MATCH (cwe:Weakness {id: 'CWE-276'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-127'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-128'})
MATCH (cwe:Weakness {id: 'CWE-682'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-129'})
MATCH (cwe:Weakness {id: 'CWE-682'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-129'})
MATCH (cwe:Weakness {id: 'CWE-822'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-129'})
MATCH (cwe:Weakness {id: 'CWE-823'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-13'})
MATCH (cwe:Weakness {id: 'CWE-353'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-13'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-13'})
MATCH (cwe:Weakness {id: 'CWE-302'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-13'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-13'})
MATCH (cwe:Weakness {id: 'CWE-15'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-13'})
MATCH (cwe:Weakness {id: 'CWE-73'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-13'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-13'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-130'})
MATCH (cwe:Weakness {id: 'CWE-404'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-130'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-130'})
MATCH (cwe:Weakness {id: 'CWE-1325'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-131'})
MATCH (cwe:Weakness {id: 'CWE-404'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-132'})
MATCH (cwe:Weakness {id: 'CWE-59'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-133'})
MATCH (cwe:Weakness {id: 'CWE-912'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-134'})
MATCH (cwe:Weakness {id: 'CWE-150'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-135'})
MATCH (cwe:Weakness {id: 'CWE-134'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-135'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-135'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-136'})
MATCH (cwe:Weakness {id: 'CWE-77'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-136'})
MATCH (cwe:Weakness {id: 'CWE-90'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-136'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-137'})
MATCH (cwe:Weakness {id: 'CWE-88'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-138'})
MATCH (cwe:Weakness {id: 'CWE-470'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-139'})
MATCH (cwe:Weakness {id: 'CWE-23'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-14'})
MATCH (cwe:Weakness {id: 'CWE-120'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-14'})
MATCH (cwe:Weakness {id: 'CWE-353'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-14'})
MATCH (cwe:Weakness {id: 'CWE-118'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-14'})
MATCH (cwe:Weakness {id: 'CWE-119'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-14'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-14'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-14'})
MATCH (cwe:Weakness {id: 'CWE-680'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-14'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-140'})
MATCH (cwe:Weakness {id: 'CWE-372'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-141'})
MATCH (cwe:Weakness {id: 'CWE-348'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-141'})
MATCH (cwe:Weakness {id: 'CWE-345'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-141'})
MATCH (cwe:Weakness {id: 'CWE-349'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-141'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-142'})
MATCH (cwe:Weakness {id: 'CWE-348'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-142'})
MATCH (cwe:Weakness {id: 'CWE-345'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-142'})
MATCH (cwe:Weakness {id: 'CWE-349'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-142'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-142'})
MATCH (cwe:Weakness {id: 'CWE-350'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-143'})
MATCH (cwe:Weakness {id: 'CWE-425'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-144'})
MATCH (cwe:Weakness {id: 'CWE-425'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-145'})
MATCH (cwe:Weakness {id: 'CWE-354'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-146'})
MATCH (cwe:Weakness {id: 'CWE-15'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-146'})
MATCH (cwe:Weakness {id: 'CWE-472'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-147'})
MATCH (cwe:Weakness {id: 'CWE-400'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-147'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-148'})
MATCH (cwe:Weakness {id: 'CWE-345'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-149'})
MATCH (cwe:Weakness {id: 'CWE-377'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-15'})
MATCH (cwe:Weakness {id: 'CWE-146'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-15'})
MATCH (cwe:Weakness {id: 'CWE-77'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-15'})
MATCH (cwe:Weakness {id: 'CWE-184'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-15'})
MATCH (cwe:Weakness {id: 'CWE-78'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-15'})
MATCH (cwe:Weakness {id: 'CWE-185'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-15'})
MATCH (cwe:Weakness {id: 'CWE-93'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-15'})
MATCH (cwe:Weakness {id: 'CWE-140'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-15'})
MATCH (cwe:Weakness {id: 'CWE-157'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-15'})
MATCH (cwe:Weakness {id: 'CWE-138'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-15'})
MATCH (cwe:Weakness {id: 'CWE-154'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-15'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-150'})
MATCH (cwe:Weakness {id: 'CWE-552'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-150'})
MATCH (cwe:Weakness {id: 'CWE-1239'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-150'})
MATCH (cwe:Weakness {id: 'CWE-1258'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-150'})
MATCH (cwe:Weakness {id: 'CWE-1266'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-150'})
MATCH (cwe:Weakness {id: 'CWE-1272'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-150'})
MATCH (cwe:Weakness {id: 'CWE-1323'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-150'})
MATCH (cwe:Weakness {id: 'CWE-1330'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-151'})
MATCH (cwe:Weakness {id: 'CWE-287'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-153'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-154'})
MATCH (cwe:Weakness {id: 'CWE-451'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-155'})
MATCH (cwe:Weakness {id: 'CWE-377'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-157'})
MATCH (cwe:Weakness {id: 'CWE-311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-158'})
MATCH (cwe:Weakness {id: 'CWE-311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-159'})
MATCH (cwe:Weakness {id: 'CWE-706'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-16'})
MATCH (cwe:Weakness {id: 'CWE-521'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-16'})
MATCH (cwe:Weakness {id: 'CWE-262'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-16'})
MATCH (cwe:Weakness {id: 'CWE-263'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-16'})
MATCH (cwe:Weakness {id: 'CWE-654'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-16'})
MATCH (cwe:Weakness {id: 'CWE-307'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-16'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-16'})
MATCH (cwe:Weakness {id: 'CWE-309'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-160'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-161'})
MATCH (cwe:Weakness {id: 'CWE-923'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-162'})
MATCH (cwe:Weakness {id: 'CWE-602'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-163'})
MATCH (cwe:Weakness {id: 'CWE-451'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-164'})
MATCH (cwe:Weakness {id: 'CWE-451'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-166'})
MATCH (cwe:Weakness {id: 'CWE-306'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-166'})
MATCH (cwe:Weakness {id: 'CWE-1221'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-166'})
MATCH (cwe:Weakness {id: 'CWE-1232'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-167'})
MATCH (cwe:Weakness {id: 'CWE-1323'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-168'})
MATCH (cwe:Weakness {id: 'CWE-212'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-168'})
MATCH (cwe:Weakness {id: 'CWE-69'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-169'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-17'})
MATCH (cwe:Weakness {id: 'CWE-732'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-17'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-17'})
MATCH (cwe:Weakness {id: 'CWE-272'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-17'})
MATCH (cwe:Weakness {id: 'CWE-59'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-17'})
MATCH (cwe:Weakness {id: 'CWE-282'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-17'})
MATCH (cwe:Weakness {id: 'CWE-270'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-17'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-170'})
MATCH (cwe:Weakness {id: 'CWE-497'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-173'})
MATCH (cwe:Weakness {id: 'CWE-451'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-174'})
MATCH (cwe:Weakness {id: 'CWE-88'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-175'})
MATCH (cwe:Weakness {id: 'CWE-829'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-176'})
MATCH (cwe:Weakness {id: 'CWE-15'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-176'})
MATCH (cwe:Weakness {id: 'CWE-1233'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-176'})
MATCH (cwe:Weakness {id: 'CWE-1234'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-176'})
MATCH (cwe:Weakness {id: 'CWE-1304'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-176'})
MATCH (cwe:Weakness {id: 'CWE-1328'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-177'})
MATCH (cwe:Weakness {id: 'CWE-706'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-178'})
MATCH (cwe:Weakness {id: 'CWE-601'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-18'})
MATCH (cwe:Weakness {id: 'CWE-80'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-180'})
MATCH (cwe:Weakness {id: 'CWE-732'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-180'})
MATCH (cwe:Weakness {id: 'CWE-1190'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-180'})
MATCH (cwe:Weakness {id: 'CWE-1191'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-180'})
MATCH (cwe:Weakness {id: 'CWE-1193'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-180'})
MATCH (cwe:Weakness {id: 'CWE-1220'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-180'})
MATCH (cwe:Weakness {id: 'CWE-1268'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-180'})
MATCH (cwe:Weakness {id: 'CWE-1280'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-180'})
MATCH (cwe:Weakness {id: 'CWE-1297'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-180'})
MATCH (cwe:Weakness {id: 'CWE-1311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-180'})
MATCH (cwe:Weakness {id: 'CWE-1315'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-180'})
MATCH (cwe:Weakness {id: 'CWE-1318'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-180'})
MATCH (cwe:Weakness {id: 'CWE-1320'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-180'})
MATCH (cwe:Weakness {id: 'CWE-1321'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-181'})
MATCH (cwe:Weakness {id: 'CWE-1021'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-182'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-182'})
MATCH (cwe:Weakness {id: 'CWE-184'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-182'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-183'})
MATCH (cwe:Weakness {id: 'CWE-77'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-184'})
MATCH (cwe:Weakness {id: 'CWE-494'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-185'})
MATCH (cwe:Weakness {id: 'CWE-494'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-186'})
MATCH (cwe:Weakness {id: 'CWE-494'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-187'})
MATCH (cwe:Weakness {id: 'CWE-494'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-188'})
MATCH (cwe:Weakness {id: 'CWE-1278'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-189'})
MATCH (cwe:Weakness {id: 'CWE-203'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-189'})
MATCH (cwe:Weakness {id: 'CWE-1255'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-189'})
MATCH (cwe:Weakness {id: 'CWE-1300'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-19'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-190'})
MATCH (cwe:Weakness {id: 'CWE-912'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-191'})
MATCH (cwe:Weakness {id: 'CWE-798'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-192'})
MATCH (cwe:Weakness {id: 'CWE-326'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-193'})
MATCH (cwe:Weakness {id: 'CWE-98'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-193'})
MATCH (cwe:Weakness {id: 'CWE-80'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-194'})
MATCH (cwe:Weakness {id: 'CWE-287'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-196'})
MATCH (cwe:Weakness {id: 'CWE-384'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-196'})
MATCH (cwe:Weakness {id: 'CWE-664'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-197'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-197'})
MATCH (cwe:Weakness {id: 'CWE-776'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-198'})
MATCH (cwe:Weakness {id: 'CWE-81'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-199'})
MATCH (cwe:Weakness {id: 'CWE-87'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-2'})
MATCH (cwe:Weakness {id: 'CWE-645'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-20'})
MATCH (cwe:Weakness {id: 'CWE-326'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-20'})
MATCH (cwe:Weakness {id: 'CWE-327'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-20'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-20'})
MATCH (cwe:Weakness {id: 'CWE-1204'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-201'})
MATCH (cwe:Weakness {id: 'CWE-829'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-202'})
MATCH (cwe:Weakness {id: 'CWE-602'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-203'})
MATCH (cwe:Weakness {id: 'CWE-15'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-204'})
MATCH (cwe:Weakness {id: 'CWE-524'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-204'})
MATCH (cwe:Weakness {id: 'CWE-311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-204'})
MATCH (cwe:Weakness {id: 'CWE-1239'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-204'})
MATCH (cwe:Weakness {id: 'CWE-1258'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-206'})
MATCH (cwe:Weakness {id: 'CWE-732'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-207'})
MATCH (cwe:Weakness {id: 'CWE-602'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-208'})
MATCH (cwe:Weakness {id: 'CWE-602'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-209'})
MATCH (cwe:Weakness {id: 'CWE-79'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-209'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-209'})
MATCH (cwe:Weakness {id: 'CWE-646'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-21'})
MATCH (cwe:Weakness {id: 'CWE-290'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-21'})
MATCH (cwe:Weakness {id: 'CWE-302'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-21'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-21'})
MATCH (cwe:Weakness {id: 'CWE-539'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-21'})
MATCH (cwe:Weakness {id: 'CWE-6'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-21'})
MATCH (cwe:Weakness {id: 'CWE-384'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-21'})
MATCH (cwe:Weakness {id: 'CWE-664'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-21'})
MATCH (cwe:Weakness {id: 'CWE-602'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-21'})
MATCH (cwe:Weakness {id: 'CWE-642'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-212'})
MATCH (cwe:Weakness {id: 'CWE-1242'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-212'})
MATCH (cwe:Weakness {id: 'CWE-1246'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-212'})
MATCH (cwe:Weakness {id: 'CWE-1281'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-215'})
MATCH (cwe:Weakness {id: 'CWE-209'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-215'})
MATCH (cwe:Weakness {id: 'CWE-532'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-216'})
MATCH (cwe:Weakness {id: 'CWE-306'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-217'})
MATCH (cwe:Weakness {id: 'CWE-201'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-218'})
MATCH (cwe:Weakness {id: 'CWE-345'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-219'})
MATCH (cwe:Weakness {id: 'CWE-441'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-219'})
MATCH (cwe:Weakness {id: 'CWE-610'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-22'})
MATCH (cwe:Weakness {id: 'CWE-290'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-22'})
MATCH (cwe:Weakness {id: 'CWE-287'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-22'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-22'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-22'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-220'})
MATCH (cwe:Weakness {id: 'CWE-757'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-221'})
MATCH (cwe:Weakness {id: 'CWE-611'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-222'})
MATCH (cwe:Weakness {id: 'CWE-1021'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-224'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-226'})
MATCH (cwe:Weakness {id: 'CWE-565'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-226'})
MATCH (cwe:Weakness {id: 'CWE-472'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-227'})
MATCH (cwe:Weakness {id: 'CWE-400'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-228'})
MATCH (cwe:Weakness {id: 'CWE-829'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-229'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-23'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-230'})
MATCH (cwe:Weakness {id: 'CWE-112'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-230'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-230'})
MATCH (cwe:Weakness {id: 'CWE-674'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-230'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-231'})
MATCH (cwe:Weakness {id: 'CWE-112'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-231'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-231'})
MATCH (cwe:Weakness {id: 'CWE-674'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-231'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-233'})
MATCH (cwe:Weakness {id: 'CWE-269'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-233'})
MATCH (cwe:Weakness {id: 'CWE-1264'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-233'})
MATCH (cwe:Weakness {id: 'CWE-1311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-234'})
MATCH (cwe:Weakness {id: 'CWE-732'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-234'})
MATCH (cwe:Weakness {id: 'CWE-648'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-237'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-24'})
MATCH (cwe:Weakness {id: 'CWE-120'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-24'})
MATCH (cwe:Weakness {id: 'CWE-119'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-24'})
MATCH (cwe:Weakness {id: 'CWE-118'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-24'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-24'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-24'})
MATCH (cwe:Weakness {id: 'CWE-680'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-24'})
MATCH (cwe:Weakness {id: 'CWE-733'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-24'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-240'})
MATCH (cwe:Weakness {id: 'CWE-99'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-242'})
MATCH (cwe:Weakness {id: 'CWE-94'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-243'})
MATCH (cwe:Weakness {id: 'CWE-83'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-244'})
MATCH (cwe:Weakness {id: 'CWE-83'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-245'})
MATCH (cwe:Weakness {id: 'CWE-85'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-247'})
MATCH (cwe:Weakness {id: 'CWE-86'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-248'})
MATCH (cwe:Weakness {id: 'CWE-77'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-25'})
MATCH (cwe:Weakness {id: 'CWE-412'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-25'})
MATCH (cwe:Weakness {id: 'CWE-567'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-25'})
MATCH (cwe:Weakness {id: 'CWE-662'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-25'})
MATCH (cwe:Weakness {id: 'CWE-667'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-25'})
MATCH (cwe:Weakness {id: 'CWE-833'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-25'})
MATCH (cwe:Weakness {id: 'CWE-1322'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-250'})
MATCH (cwe:Weakness {id: 'CWE-91'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-250'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-250'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-250'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-251'})
MATCH (cwe:Weakness {id: 'CWE-829'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-252'})
MATCH (cwe:Weakness {id: 'CWE-829'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-253'})
MATCH (cwe:Weakness {id: 'CWE-829'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-256'})
MATCH (cwe:Weakness {id: 'CWE-805'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-26'})
MATCH (cwe:Weakness {id: 'CWE-368'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-26'})
MATCH (cwe:Weakness {id: 'CWE-363'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-26'})
MATCH (cwe:Weakness {id: 'CWE-366'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-26'})
MATCH (cwe:Weakness {id: 'CWE-370'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-26'})
MATCH (cwe:Weakness {id: 'CWE-362'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-26'})
MATCH (cwe:Weakness {id: 'CWE-662'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-26'})
MATCH (cwe:Weakness {id: 'CWE-689'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-26'})
MATCH (cwe:Weakness {id: 'CWE-667'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-26'})
MATCH (cwe:Weakness {id: 'CWE-665'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-26'})
MATCH (cwe:Weakness {id: 'CWE-1223'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-26'})
MATCH (cwe:Weakness {id: 'CWE-1254'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-26'})
MATCH (cwe:Weakness {id: 'CWE-1298'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-261'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-263'})
MATCH (cwe:Weakness {id: 'CWE-829'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-267'})
MATCH (cwe:Weakness {id: 'CWE-173'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-267'})
MATCH (cwe:Weakness {id: 'CWE-172'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-267'})
MATCH (cwe:Weakness {id: 'CWE-180'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-267'})
MATCH (cwe:Weakness {id: 'CWE-181'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-267'})
MATCH (cwe:Weakness {id: 'CWE-73'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-267'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-267'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-267'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-267'})
MATCH (cwe:Weakness {id: 'CWE-692'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-268'})
MATCH (cwe:Weakness {id: 'CWE-117'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-27'})
MATCH (cwe:Weakness {id: 'CWE-367'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-27'})
MATCH (cwe:Weakness {id: 'CWE-61'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-27'})
MATCH (cwe:Weakness {id: 'CWE-662'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-27'})
MATCH (cwe:Weakness {id: 'CWE-689'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-27'})
MATCH (cwe:Weakness {id: 'CWE-667'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-270'})
MATCH (cwe:Weakness {id: 'CWE-15'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-271'})
MATCH (cwe:Weakness {id: 'CWE-15'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-273'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-273'})
MATCH (cwe:Weakness {id: 'CWE-436'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-273'})
MATCH (cwe:Weakness {id: 'CWE-444'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-274'})
MATCH (cwe:Weakness {id: 'CWE-302'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-274'})
MATCH (cwe:Weakness {id: 'CWE-654'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-275'})
MATCH (cwe:Weakness {id: 'CWE-350'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-276'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-277'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-278'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-279'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-28'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-28'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-285'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-287'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-29'})
MATCH (cwe:Weakness {id: 'CWE-367'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-29'})
MATCH (cwe:Weakness {id: 'CWE-368'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-29'})
MATCH (cwe:Weakness {id: 'CWE-366'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-29'})
MATCH (cwe:Weakness {id: 'CWE-370'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-29'})
MATCH (cwe:Weakness {id: 'CWE-362'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-29'})
MATCH (cwe:Weakness {id: 'CWE-662'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-29'})
MATCH (cwe:Weakness {id: 'CWE-691'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-29'})
MATCH (cwe:Weakness {id: 'CWE-663'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-29'})
MATCH (cwe:Weakness {id: 'CWE-665'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-290'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-291'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-292'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-293'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-294'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-295'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-296'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-297'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-298'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-299'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-3'})
MATCH (cwe:Weakness {id: 'CWE-173'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-3'})
MATCH (cwe:Weakness {id: 'CWE-41'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-3'})
MATCH (cwe:Weakness {id: 'CWE-172'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-3'})
MATCH (cwe:Weakness {id: 'CWE-179'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-3'})
MATCH (cwe:Weakness {id: 'CWE-180'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-3'})
MATCH (cwe:Weakness {id: 'CWE-181'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-3'})
MATCH (cwe:Weakness {id: 'CWE-183'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-3'})
MATCH (cwe:Weakness {id: 'CWE-184'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-3'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-3'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-3'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-3'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-30'})
MATCH (cwe:Weakness {id: 'CWE-270'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-300'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-301'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-302'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-303'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-304'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-305'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-306'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-307'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-308'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-309'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-31'})
MATCH (cwe:Weakness {id: 'CWE-565'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-31'})
MATCH (cwe:Weakness {id: 'CWE-302'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-31'})
MATCH (cwe:Weakness {id: 'CWE-311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-31'})
MATCH (cwe:Weakness {id: 'CWE-113'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-31'})
MATCH (cwe:Weakness {id: 'CWE-539'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-31'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-31'})
MATCH (cwe:Weakness {id: 'CWE-315'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-31'})
MATCH (cwe:Weakness {id: 'CWE-384'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-31'})
MATCH (cwe:Weakness {id: 'CWE-472'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-31'})
MATCH (cwe:Weakness {id: 'CWE-602'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-31'})
MATCH (cwe:Weakness {id: 'CWE-642'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-310'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-312'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-313'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-317'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-318'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-319'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-32'})
MATCH (cwe:Weakness {id: 'CWE-80'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-320'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-321'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-322'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-323'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-324'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-325'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-326'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-327'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-328'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-329'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-33'})
MATCH (cwe:Weakness {id: 'CWE-444'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-330'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-331'})
MATCH (cwe:Weakness {id: 'CWE-204'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-332'})
MATCH (cwe:Weakness {id: 'CWE-204'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-34'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-34'})
MATCH (cwe:Weakness {id: 'CWE-113'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-34'})
MATCH (cwe:Weakness {id: 'CWE-138'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-34'})
MATCH (cwe:Weakness {id: 'CWE-436'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-35'})
MATCH (cwe:Weakness {id: 'CWE-94'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-35'})
MATCH (cwe:Weakness {id: 'CWE-96'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-35'})
MATCH (cwe:Weakness {id: 'CWE-95'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-35'})
MATCH (cwe:Weakness {id: 'CWE-97'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-35'})
MATCH (cwe:Weakness {id: 'CWE-272'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-35'})
MATCH (cwe:Weakness {id: 'CWE-59'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-35'})
MATCH (cwe:Weakness {id: 'CWE-282'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-35'})
MATCH (cwe:Weakness {id: 'CWE-270'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-36'})
MATCH (cwe:Weakness {id: 'CWE-306'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-36'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-36'})
MATCH (cwe:Weakness {id: 'CWE-695'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-36'})
MATCH (cwe:Weakness {id: 'CWE-1242'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MATCH (cwe:Weakness {id: 'CWE-226'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MATCH (cwe:Weakness {id: 'CWE-311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MATCH (cwe:Weakness {id: 'CWE-525'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MATCH (cwe:Weakness {id: 'CWE-312'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MATCH (cwe:Weakness {id: 'CWE-314'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MATCH (cwe:Weakness {id: 'CWE-315'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MATCH (cwe:Weakness {id: 'CWE-318'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MATCH (cwe:Weakness {id: 'CWE-1239'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MATCH (cwe:Weakness {id: 'CWE-1258'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MATCH (cwe:Weakness {id: 'CWE-1266'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MATCH (cwe:Weakness {id: 'CWE-1272'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MATCH (cwe:Weakness {id: 'CWE-1278'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MATCH (cwe:Weakness {id: 'CWE-1301'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MATCH (cwe:Weakness {id: 'CWE-1330'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-38'})
MATCH (cwe:Weakness {id: 'CWE-426'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-38'})
MATCH (cwe:Weakness {id: 'CWE-427'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-383'})
MATCH (cwe:Weakness {id: 'CWE-311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-383'})
MATCH (cwe:Weakness {id: 'CWE-319'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-383'})
MATCH (cwe:Weakness {id: 'CWE-419'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-383'})
MATCH (cwe:Weakness {id: 'CWE-602'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-384'})
MATCH (cwe:Weakness {id: 'CWE-471'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-384'})
MATCH (cwe:Weakness {id: 'CWE-345'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-384'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-384'})
MATCH (cwe:Weakness {id: 'CWE-602'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-384'})
MATCH (cwe:Weakness {id: 'CWE-311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-385'})
MATCH (cwe:Weakness {id: 'CWE-471'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-385'})
MATCH (cwe:Weakness {id: 'CWE-345'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-385'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-385'})
MATCH (cwe:Weakness {id: 'CWE-602'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-385'})
MATCH (cwe:Weakness {id: 'CWE-311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-386'})
MATCH (cwe:Weakness {id: 'CWE-471'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-386'})
MATCH (cwe:Weakness {id: 'CWE-345'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-386'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-386'})
MATCH (cwe:Weakness {id: 'CWE-602'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-386'})
MATCH (cwe:Weakness {id: 'CWE-311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-387'})
MATCH (cwe:Weakness {id: 'CWE-471'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-387'})
MATCH (cwe:Weakness {id: 'CWE-345'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-387'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-387'})
MATCH (cwe:Weakness {id: 'CWE-602'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-387'})
MATCH (cwe:Weakness {id: 'CWE-311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-388'})
MATCH (cwe:Weakness {id: 'CWE-471'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-388'})
MATCH (cwe:Weakness {id: 'CWE-345'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-388'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-388'})
MATCH (cwe:Weakness {id: 'CWE-602'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-388'})
MATCH (cwe:Weakness {id: 'CWE-311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-389'})
MATCH (cwe:Weakness {id: 'CWE-353'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-39'})
MATCH (cwe:Weakness {id: 'CWE-353'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-39'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-39'})
MATCH (cwe:Weakness {id: 'CWE-302'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-39'})
MATCH (cwe:Weakness {id: 'CWE-472'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-39'})
MATCH (cwe:Weakness {id: 'CWE-565'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-39'})
MATCH (cwe:Weakness {id: 'CWE-315'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-39'})
MATCH (cwe:Weakness {id: 'CWE-539'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-39'})
MATCH (cwe:Weakness {id: 'CWE-384'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-39'})
MATCH (cwe:Weakness {id: 'CWE-233'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-4'})
MATCH (cwe:Weakness {id: 'CWE-291'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-4'})
MATCH (cwe:Weakness {id: 'CWE-173'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-40'})
MATCH (cwe:Weakness {id: 'CWE-77'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-401'})
MATCH (cwe:Weakness {id: 'CWE-1263'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-402'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-41'})
MATCH (cwe:Weakness {id: 'CWE-150'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-41'})
MATCH (cwe:Weakness {id: 'CWE-88'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-41'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-42'})
MATCH (cwe:Weakness {id: 'CWE-120'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-42'})
MATCH (cwe:Weakness {id: 'CWE-119'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-42'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-42'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-43'})
MATCH (cwe:Weakness {id: 'CWE-179'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-43'})
MATCH (cwe:Weakness {id: 'CWE-181'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-43'})
MATCH (cwe:Weakness {id: 'CWE-184'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-43'})
MATCH (cwe:Weakness {id: 'CWE-183'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-43'})
MATCH (cwe:Weakness {id: 'CWE-77'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-43'})
MATCH (cwe:Weakness {id: 'CWE-78'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-43'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-43'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-43'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-43'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-439'})
MATCH (cwe:Weakness {id: 'CWE-1269'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-44'})
MATCH (cwe:Weakness {id: 'CWE-120'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-44'})
MATCH (cwe:Weakness {id: 'CWE-119'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-44'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-441'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-442'})
MATCH (cwe:Weakness {id: 'CWE-506'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-448'})
MATCH (cwe:Weakness {id: 'CWE-506'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-45'})
MATCH (cwe:Weakness {id: 'CWE-120'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-45'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-45'})
MATCH (cwe:Weakness {id: 'CWE-302'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-45'})
MATCH (cwe:Weakness {id: 'CWE-118'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-45'})
MATCH (cwe:Weakness {id: 'CWE-119'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-45'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-45'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-45'})
MATCH (cwe:Weakness {id: 'CWE-680'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-45'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-456'})
MATCH (cwe:Weakness {id: 'CWE-1257'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-456'})
MATCH (cwe:Weakness {id: 'CWE-1260'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-456'})
MATCH (cwe:Weakness {id: 'CWE-1274'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-456'})
MATCH (cwe:Weakness {id: 'CWE-1312'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-456'})
MATCH (cwe:Weakness {id: 'CWE-1316'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-457'})
MATCH (cwe:Weakness {id: 'CWE-1299'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-458'})
MATCH (cwe:Weakness {id: 'CWE-1282'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-459'})
MATCH (cwe:Weakness {id: 'CWE-327'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-459'})
MATCH (cwe:Weakness {id: 'CWE-295'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-459'})
MATCH (cwe:Weakness {id: 'CWE-290'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-46'})
MATCH (cwe:Weakness {id: 'CWE-120'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-46'})
MATCH (cwe:Weakness {id: 'CWE-118'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-46'})
MATCH (cwe:Weakness {id: 'CWE-119'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-46'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-46'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-46'})
MATCH (cwe:Weakness {id: 'CWE-680'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-46'})
MATCH (cwe:Weakness {id: 'CWE-733'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-46'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-460'})
MATCH (cwe:Weakness {id: 'CWE-88'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-460'})
MATCH (cwe:Weakness {id: 'CWE-147'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-460'})
MATCH (cwe:Weakness {id: 'CWE-235'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-461'})
MATCH (cwe:Weakness {id: 'CWE-328'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-461'})
MATCH (cwe:Weakness {id: 'CWE-290'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-462'})
MATCH (cwe:Weakness {id: 'CWE-385'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-462'})
MATCH (cwe:Weakness {id: 'CWE-352'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-462'})
MATCH (cwe:Weakness {id: 'CWE-208'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-463'})
MATCH (cwe:Weakness {id: 'CWE-209'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-463'})
MATCH (cwe:Weakness {id: 'CWE-514'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-463'})
MATCH (cwe:Weakness {id: 'CWE-649'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-463'})
MATCH (cwe:Weakness {id: 'CWE-347'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-463'})
MATCH (cwe:Weakness {id: 'CWE-354'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-463'})
MATCH (cwe:Weakness {id: 'CWE-696'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-464'})
MATCH (cwe:Weakness {id: 'CWE-359'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-465'})
MATCH (cwe:Weakness {id: 'CWE-441'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-466'})
MATCH (cwe:Weakness {id: 'CWE-300'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-467'})
MATCH (cwe:Weakness {id: 'CWE-352'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-467'})
MATCH (cwe:Weakness {id: 'CWE-359'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-468'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-468'})
MATCH (cwe:Weakness {id: 'CWE-149'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-468'})
MATCH (cwe:Weakness {id: 'CWE-177'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-468'})
MATCH (cwe:Weakness {id: 'CWE-838'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-469'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-469'})
MATCH (cwe:Weakness {id: 'CWE-772'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-47'})
MATCH (cwe:Weakness {id: 'CWE-120'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-47'})
MATCH (cwe:Weakness {id: 'CWE-119'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-47'})
MATCH (cwe:Weakness {id: 'CWE-118'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-47'})
MATCH (cwe:Weakness {id: 'CWE-130'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-47'})
MATCH (cwe:Weakness {id: 'CWE-131'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-47'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-47'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-47'})
MATCH (cwe:Weakness {id: 'CWE-680'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-47'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-470'})
MATCH (cwe:Weakness {id: 'CWE-250'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-470'})
MATCH (cwe:Weakness {id: 'CWE-89'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-471'})
MATCH (cwe:Weakness {id: 'CWE-427'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-472'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-473'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-473'})
MATCH (cwe:Weakness {id: 'CWE-327'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-473'})
MATCH (cwe:Weakness {id: 'CWE-290'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-474'})
MATCH (cwe:Weakness {id: 'CWE-522'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-475'})
MATCH (cwe:Weakness {id: 'CWE-347'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-475'})
MATCH (cwe:Weakness {id: 'CWE-327'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-475'})
MATCH (cwe:Weakness {id: 'CWE-295'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-476'})
MATCH (cwe:Weakness {id: 'CWE-290'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-477'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-477'})
MATCH (cwe:Weakness {id: 'CWE-311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-477'})
MATCH (cwe:Weakness {id: 'CWE-319'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-478'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-479'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-48'})
MATCH (cwe:Weakness {id: 'CWE-241'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-48'})
MATCH (cwe:Weakness {id: 'CWE-706'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-480'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-481'})
MATCH (cwe:Weakness {id: 'CWE-923'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-482'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-485'})
MATCH (cwe:Weakness {id: 'CWE-330'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-486'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-487'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-488'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-489'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-49'})
MATCH (cwe:Weakness {id: 'CWE-521'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-49'})
MATCH (cwe:Weakness {id: 'CWE-262'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-49'})
MATCH (cwe:Weakness {id: 'CWE-263'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-49'})
MATCH (cwe:Weakness {id: 'CWE-257'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-49'})
MATCH (cwe:Weakness {id: 'CWE-654'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-49'})
MATCH (cwe:Weakness {id: 'CWE-307'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-49'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-49'})
MATCH (cwe:Weakness {id: 'CWE-309'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-490'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-491'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-492'})
MATCH (cwe:Weakness {id: 'CWE-400'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-492'})
MATCH (cwe:Weakness {id: 'CWE-1333'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-493'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-494'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-494'})
MATCH (cwe:Weakness {id: 'CWE-404'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-495'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-495'})
MATCH (cwe:Weakness {id: 'CWE-404'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-496'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-496'})
MATCH (cwe:Weakness {id: 'CWE-404'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-497'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-498'})
MATCH (cwe:Weakness {id: 'CWE-359'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-499'})
MATCH (cwe:Weakness {id: 'CWE-925'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-5'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-50'})
MATCH (cwe:Weakness {id: 'CWE-522'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-50'})
MATCH (cwe:Weakness {id: 'CWE-640'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-500'})
MATCH (cwe:Weakness {id: 'CWE-749'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-500'})
MATCH (cwe:Weakness {id: 'CWE-940'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-501'})
MATCH (cwe:Weakness {id: 'CWE-923'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-502'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-503'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-504'})
MATCH (cwe:Weakness {id: 'CWE-1021'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-506'})
MATCH (cwe:Weakness {id: 'CWE-1021'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-508'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-508'})
MATCH (cwe:Weakness {id: 'CWE-359'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-509'})
MATCH (cwe:Weakness {id: 'CWE-522'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-509'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-509'})
MATCH (cwe:Weakness {id: 'CWE-309'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-509'})
MATCH (cwe:Weakness {id: 'CWE-294'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-509'})
MATCH (cwe:Weakness {id: 'CWE-263'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-509'})
MATCH (cwe:Weakness {id: 'CWE-262'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-509'})
MATCH (cwe:Weakness {id: 'CWE-521'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-51'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-51'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-51'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-510'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-52'})
MATCH (cwe:Weakness {id: 'CWE-158'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-52'})
MATCH (cwe:Weakness {id: 'CWE-172'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-52'})
MATCH (cwe:Weakness {id: 'CWE-173'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-52'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-52'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-52'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-52'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-528'})
MATCH (cwe:Weakness {id: 'CWE-770'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-53'})
MATCH (cwe:Weakness {id: 'CWE-158'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-53'})
MATCH (cwe:Weakness {id: 'CWE-172'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-53'})
MATCH (cwe:Weakness {id: 'CWE-173'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-53'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-53'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-53'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-53'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-533'})
MATCH (cwe:Weakness {id: 'CWE-494'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-536'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-538'})
MATCH (cwe:Weakness {id: 'CWE-494'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-538'})
MATCH (cwe:Weakness {id: 'CWE-829'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-54'})
MATCH (cwe:Weakness {id: 'CWE-209'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-540'})
MATCH (cwe:Weakness {id: 'CWE-125'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-541'})
MATCH (cwe:Weakness {id: 'CWE-204'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-541'})
MATCH (cwe:Weakness {id: 'CWE-205'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-541'})
MATCH (cwe:Weakness {id: 'CWE-208'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-545'})
MATCH (cwe:Weakness {id: 'CWE-1239'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-545'})
MATCH (cwe:Weakness {id: 'CWE-1243'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-545'})
MATCH (cwe:Weakness {id: 'CWE-1258'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-545'})
MATCH (cwe:Weakness {id: 'CWE-1266'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-545'})
MATCH (cwe:Weakness {id: 'CWE-1272'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-545'})
MATCH (cwe:Weakness {id: 'CWE-1278'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-545'})
MATCH (cwe:Weakness {id: 'CWE-1323'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-545'})
MATCH (cwe:Weakness {id: 'CWE-1258'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-545'})
MATCH (cwe:Weakness {id: 'CWE-1330'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-546'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-546'})
MATCH (cwe:Weakness {id: 'CWE-1266'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-546'})
MATCH (cwe:Weakness {id: 'CWE-1272'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-549'})
MATCH (cwe:Weakness {id: 'CWE-829'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-55'})
MATCH (cwe:Weakness {id: 'CWE-261'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-55'})
MATCH (cwe:Weakness {id: 'CWE-521'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-55'})
MATCH (cwe:Weakness {id: 'CWE-262'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-55'})
MATCH (cwe:Weakness {id: 'CWE-263'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-55'})
MATCH (cwe:Weakness {id: 'CWE-654'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-55'})
MATCH (cwe:Weakness {id: 'CWE-916'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-55'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-55'})
MATCH (cwe:Weakness {id: 'CWE-309'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-550'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-551'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-551'})
MATCH (cwe:Weakness {id: 'CWE-522'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-552'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-554'})
MATCH (cwe:Weakness {id: 'CWE-424'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-554'})
MATCH (cwe:Weakness {id: 'CWE-1299'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-555'})
MATCH (cwe:Weakness {id: 'CWE-522'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-555'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-555'})
MATCH (cwe:Weakness {id: 'CWE-309'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-555'})
MATCH (cwe:Weakness {id: 'CWE-294'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-555'})
MATCH (cwe:Weakness {id: 'CWE-263'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-555'})
MATCH (cwe:Weakness {id: 'CWE-262'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-555'})
MATCH (cwe:Weakness {id: 'CWE-521'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-556'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-558'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-560'})
MATCH (cwe:Weakness {id: 'CWE-522'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-560'})
MATCH (cwe:Weakness {id: 'CWE-307'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-560'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-560'})
MATCH (cwe:Weakness {id: 'CWE-309'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-560'})
MATCH (cwe:Weakness {id: 'CWE-262'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-560'})
MATCH (cwe:Weakness {id: 'CWE-263'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-560'})
MATCH (cwe:Weakness {id: 'CWE-654'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-560'})
MATCH (cwe:Weakness {id: 'CWE-1273'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-561'})
MATCH (cwe:Weakness {id: 'CWE-522'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-561'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-561'})
MATCH (cwe:Weakness {id: 'CWE-309'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-561'})
MATCH (cwe:Weakness {id: 'CWE-294'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-561'})
MATCH (cwe:Weakness {id: 'CWE-263'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-561'})
MATCH (cwe:Weakness {id: 'CWE-262'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-561'})
MATCH (cwe:Weakness {id: 'CWE-521'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-562'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-563'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-564'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-565'})
MATCH (cwe:Weakness {id: 'CWE-521'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-565'})
MATCH (cwe:Weakness {id: 'CWE-262'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-565'})
MATCH (cwe:Weakness {id: 'CWE-263'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-565'})
MATCH (cwe:Weakness {id: 'CWE-654'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-565'})
MATCH (cwe:Weakness {id: 'CWE-307'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-565'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-565'})
MATCH (cwe:Weakness {id: 'CWE-309'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-57'})
MATCH (cwe:Weakness {id: 'CWE-300'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-57'})
MATCH (cwe:Weakness {id: 'CWE-287'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-57'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-573'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-574'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-575'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-576'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-577'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-578'})
MATCH (cwe:Weakness {id: 'CWE-284'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-579'})
MATCH (cwe:Weakness {id: 'CWE-15'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-58'})
MATCH (cwe:Weakness {id: 'CWE-267'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-58'})
MATCH (cwe:Weakness {id: 'CWE-269'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-580'})
MATCH (cwe:Weakness {id: 'CWE-204'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-580'})
MATCH (cwe:Weakness {id: 'CWE-205'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-580'})
MATCH (cwe:Weakness {id: 'CWE-208'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-586'})
MATCH (cwe:Weakness {id: 'CWE-502'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-587'})
MATCH (cwe:Weakness {id: 'CWE-1021'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-588'})
MATCH (cwe:Weakness {id: 'CWE-79'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-588'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-588'})
MATCH (cwe:Weakness {id: 'CWE-83'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-589'})
MATCH (cwe:Weakness {id: 'CWE-300'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-59'})
MATCH (cwe:Weakness {id: 'CWE-290'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-59'})
MATCH (cwe:Weakness {id: 'CWE-330'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-59'})
MATCH (cwe:Weakness {id: 'CWE-331'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-59'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-59'})
MATCH (cwe:Weakness {id: 'CWE-488'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-59'})
MATCH (cwe:Weakness {id: 'CWE-539'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-59'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-59'})
MATCH (cwe:Weakness {id: 'CWE-6'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-59'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-59'})
MATCH (cwe:Weakness {id: 'CWE-384'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-59'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-590'})
MATCH (cwe:Weakness {id: 'CWE-300'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-591'})
MATCH (cwe:Weakness {id: 'CWE-79'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-592'})
MATCH (cwe:Weakness {id: 'CWE-79'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-593'})
MATCH (cwe:Weakness {id: 'CWE-287'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-594'})
MATCH (cwe:Weakness {id: 'CWE-940'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-595'})
MATCH (cwe:Weakness {id: 'CWE-940'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-596'})
MATCH (cwe:Weakness {id: 'CWE-940'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-597'})
MATCH (cwe:Weakness {id: 'CWE-36'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-6'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-6'})
MATCH (cwe:Weakness {id: 'CWE-146'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-6'})
MATCH (cwe:Weakness {id: 'CWE-184'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-6'})
MATCH (cwe:Weakness {id: 'CWE-78'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-6'})
MATCH (cwe:Weakness {id: 'CWE-185'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-6'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-60'})
MATCH (cwe:Weakness {id: 'CWE-294'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-60'})
MATCH (cwe:Weakness {id: 'CWE-290'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-60'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-60'})
MATCH (cwe:Weakness {id: 'CWE-384'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-60'})
MATCH (cwe:Weakness {id: 'CWE-488'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-60'})
MATCH (cwe:Weakness {id: 'CWE-539'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-60'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-60'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-60'})
MATCH (cwe:Weakness {id: 'CWE-664'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-60'})
MATCH (cwe:Weakness {id: 'CWE-732'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-600'})
MATCH (cwe:Weakness {id: 'CWE-522'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-600'})
MATCH (cwe:Weakness {id: 'CWE-307'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-600'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-600'})
MATCH (cwe:Weakness {id: 'CWE-309'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-600'})
MATCH (cwe:Weakness {id: 'CWE-262'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-600'})
MATCH (cwe:Weakness {id: 'CWE-263'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-600'})
MATCH (cwe:Weakness {id: 'CWE-654'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-606'})
MATCH (cwe:Weakness {id: 'CWE-757'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-608'})
MATCH (cwe:Weakness {id: 'CWE-327'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-609'})
MATCH (cwe:Weakness {id: 'CWE-311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-61'})
MATCH (cwe:Weakness {id: 'CWE-384'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-61'})
MATCH (cwe:Weakness {id: 'CWE-664'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-61'})
MATCH (cwe:Weakness {id: 'CWE-732'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-612'})
MATCH (cwe:Weakness {id: 'CWE-201'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-612'})
MATCH (cwe:Weakness {id: 'CWE-300'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-613'})
MATCH (cwe:Weakness {id: 'CWE-201'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-613'})
MATCH (cwe:Weakness {id: 'CWE-300'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-614'})
MATCH (cwe:Weakness {id: 'CWE-327'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-615'})
MATCH (cwe:Weakness {id: 'CWE-300'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-616'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-618'})
MATCH (cwe:Weakness {id: 'CWE-201'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-619'})
MATCH (cwe:Weakness {id: 'CWE-201'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-62'})
MATCH (cwe:Weakness {id: 'CWE-352'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-62'})
MATCH (cwe:Weakness {id: 'CWE-306'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-62'})
MATCH (cwe:Weakness {id: 'CWE-664'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-62'})
MATCH (cwe:Weakness {id: 'CWE-732'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-62'})
MATCH (cwe:Weakness {id: 'CWE-1275'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-620'})
MATCH (cwe:Weakness {id: 'CWE-757'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-621'})
MATCH (cwe:Weakness {id: 'CWE-201'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-622'})
MATCH (cwe:Weakness {id: 'CWE-201'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-623'})
MATCH (cwe:Weakness {id: 'CWE-201'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-624'})
MATCH (cwe:Weakness {id: 'CWE-1247'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-624'})
MATCH (cwe:Weakness {id: 'CWE-1248'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-624'})
MATCH (cwe:Weakness {id: 'CWE-1256'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-624'})
MATCH (cwe:Weakness {id: 'CWE-1319'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-624'})
MATCH (cwe:Weakness {id: 'CWE-1332'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-624'})
MATCH (cwe:Weakness {id: 'CWE-1334'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-624'})
MATCH (cwe:Weakness {id: 'CWE-1338'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-624'})
MATCH (cwe:Weakness {id: 'CWE-1351'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-625'})
MATCH (cwe:Weakness {id: 'CWE-1247'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-625'})
MATCH (cwe:Weakness {id: 'CWE-1248'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-625'})
MATCH (cwe:Weakness {id: 'CWE-1256'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-625'})
MATCH (cwe:Weakness {id: 'CWE-1319'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-625'})
MATCH (cwe:Weakness {id: 'CWE-1332'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-625'})
MATCH (cwe:Weakness {id: 'CWE-1334'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-625'})
MATCH (cwe:Weakness {id: 'CWE-1338'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-625'})
MATCH (cwe:Weakness {id: 'CWE-1351'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-63'})
MATCH (cwe:Weakness {id: 'CWE-79'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-63'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-632'})
MATCH (cwe:Weakness {id: 'CWE-1007'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-633'})
MATCH (cwe:Weakness {id: 'CWE-287'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-633'})
MATCH (cwe:Weakness {id: 'CWE-1270'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-634'})
MATCH (cwe:Weakness {id: 'CWE-267'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-635'})
MATCH (cwe:Weakness {id: 'CWE-162'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-636'})
MATCH (cwe:Weakness {id: 'CWE-506'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-637'})
MATCH (cwe:Weakness {id: 'CWE-267'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-639'})
MATCH (cwe:Weakness {id: 'CWE-552'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-64'})
MATCH (cwe:Weakness {id: 'CWE-177'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-64'})
MATCH (cwe:Weakness {id: 'CWE-173'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-64'})
MATCH (cwe:Weakness {id: 'CWE-172'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-64'})
MATCH (cwe:Weakness {id: 'CWE-73'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-64'})
MATCH (cwe:Weakness {id: 'CWE-22'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-64'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-64'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-64'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-64'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-640'})
MATCH (cwe:Weakness {id: 'CWE-114'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-640'})
MATCH (cwe:Weakness {id: 'CWE-829'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-641'})
MATCH (cwe:Weakness {id: 'CWE-706'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-642'})
MATCH (cwe:Weakness {id: 'CWE-732'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-643'})
MATCH (cwe:Weakness {id: 'CWE-267'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-643'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-644'})
MATCH (cwe:Weakness {id: 'CWE-522'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-644'})
MATCH (cwe:Weakness {id: 'CWE-836'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-644'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-644'})
MATCH (cwe:Weakness {id: 'CWE-294'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-644'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-645'})
MATCH (cwe:Weakness {id: 'CWE-522'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-645'})
MATCH (cwe:Weakness {id: 'CWE-294'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-645'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-646'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-647'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-648'})
MATCH (cwe:Weakness {id: 'CWE-267'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-649'})
MATCH (cwe:Weakness {id: 'CWE-46'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-65'})
MATCH (cwe:Weakness {id: 'CWE-319'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-65'})
MATCH (cwe:Weakness {id: 'CWE-311'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-65'})
MATCH (cwe:Weakness {id: 'CWE-318'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-65'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-650'})
MATCH (cwe:Weakness {id: 'CWE-287'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-650'})
MATCH (cwe:Weakness {id: 'CWE-553'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-651'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-652'})
MATCH (cwe:Weakness {id: 'CWE-522'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-652'})
MATCH (cwe:Weakness {id: 'CWE-307'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-652'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-652'})
MATCH (cwe:Weakness {id: 'CWE-309'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-652'})
MATCH (cwe:Weakness {id: 'CWE-262'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-652'})
MATCH (cwe:Weakness {id: 'CWE-263'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-652'})
MATCH (cwe:Weakness {id: 'CWE-654'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-652'})
MATCH (cwe:Weakness {id: 'CWE-294'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-652'})
MATCH (cwe:Weakness {id: 'CWE-836'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-653'})
MATCH (cwe:Weakness {id: 'CWE-522'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-653'})
MATCH (cwe:Weakness {id: 'CWE-307'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-653'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-653'})
MATCH (cwe:Weakness {id: 'CWE-309'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-653'})
MATCH (cwe:Weakness {id: 'CWE-262'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-653'})
MATCH (cwe:Weakness {id: 'CWE-263'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-653'})
MATCH (cwe:Weakness {id: 'CWE-654'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-654'})
MATCH (cwe:Weakness {id: 'CWE-1021'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-657'})
MATCH (cwe:Weakness {id: 'CWE-494'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-66'})
MATCH (cwe:Weakness {id: 'CWE-89'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-66'})
MATCH (cwe:Weakness {id: 'CWE-1286'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-660'})
MATCH (cwe:Weakness {id: 'CWE-829'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-661'})
MATCH (cwe:Weakness {id: 'CWE-489'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-662'})
MATCH (cwe:Weakness {id: 'CWE-300'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-662'})
MATCH (cwe:Weakness {id: 'CWE-494'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-663'})
MATCH (cwe:Weakness {id: 'CWE-1037'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-663'})
MATCH (cwe:Weakness {id: 'CWE-1303'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-663'})
MATCH (cwe:Weakness {id: 'CWE-1264'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-664'})
MATCH (cwe:Weakness {id: 'CWE-918'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-664'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-665'})
MATCH (cwe:Weakness {id: 'CWE-345'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-665'})
MATCH (cwe:Weakness {id: 'CWE-353'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-665'})
MATCH (cwe:Weakness {id: 'CWE-288'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-665'})
MATCH (cwe:Weakness {id: 'CWE-1188'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-665'})
MATCH (cwe:Weakness {id: 'CWE-862'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-666'})
MATCH (cwe:Weakness {id: 'CWE-404'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-667'})
MATCH (cwe:Weakness {id: 'CWE-290'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-668'})
MATCH (cwe:Weakness {id: 'CWE-425'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-668'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-668'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-67'})
MATCH (cwe:Weakness {id: 'CWE-120'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-67'})
MATCH (cwe:Weakness {id: 'CWE-134'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-67'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-67'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-67'})
MATCH (cwe:Weakness {id: 'CWE-680'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-67'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-675'})
MATCH (cwe:Weakness {id: 'CWE-1266'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-676'})
MATCH (cwe:Weakness {id: 'CWE-943'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-676'})
MATCH (cwe:Weakness {id: 'CWE-1286'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-679'})
MATCH (cwe:Weakness {id: 'CWE-1222'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-679'})
MATCH (cwe:Weakness {id: 'CWE-1252'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-679'})
MATCH (cwe:Weakness {id: 'CWE-1257'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-679'})
MATCH (cwe:Weakness {id: 'CWE-1260'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-679'})
MATCH (cwe:Weakness {id: 'CWE-1274'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-679'})
MATCH (cwe:Weakness {id: 'CWE-1282'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-679'})
MATCH (cwe:Weakness {id: 'CWE-1312'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-679'})
MATCH (cwe:Weakness {id: 'CWE-1316'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-679'})
MATCH (cwe:Weakness {id: 'CWE-1326'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-68'})
MATCH (cwe:Weakness {id: 'CWE-325'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-68'})
MATCH (cwe:Weakness {id: 'CWE-328'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-68'})
MATCH (cwe:Weakness {id: 'CWE-1326'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-680'})
MATCH (cwe:Weakness {id: 'CWE-1224'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-680'})
MATCH (cwe:Weakness {id: 'CWE-1231'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-680'})
MATCH (cwe:Weakness {id: 'CWE-1233'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-680'})
MATCH (cwe:Weakness {id: 'CWE-1262'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-680'})
MATCH (cwe:Weakness {id: 'CWE-1283'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-681'})
MATCH (cwe:Weakness {id: 'CWE-1259'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-681'})
MATCH (cwe:Weakness {id: 'CWE-1267'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-681'})
MATCH (cwe:Weakness {id: 'CWE-1270'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-681'})
MATCH (cwe:Weakness {id: 'CWE-1294'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-681'})
MATCH (cwe:Weakness {id: 'CWE-1302'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-682'})
MATCH (cwe:Weakness {id: 'CWE-1277'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-682'})
MATCH (cwe:Weakness {id: 'CWE-1310'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-69'})
MATCH (cwe:Weakness {id: 'CWE-250'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-69'})
MATCH (cwe:Weakness {id: 'CWE-15'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-691'})
MATCH (cwe:Weakness {id: 'CWE-494'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-692'})
MATCH (cwe:Weakness {id: 'CWE-494'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-693'})
MATCH (cwe:Weakness {id: 'CWE-494'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-694'})
MATCH (cwe:Weakness {id: 'CWE-497'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-695'})
MATCH (cwe:Weakness {id: 'CWE-494'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-695'})
MATCH (cwe:Weakness {id: 'CWE-829'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-696'})
MATCH (cwe:Weakness {id: 'CWE-1342'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-697'})
MATCH (cwe:Weakness {id: 'CWE-923'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-698'})
MATCH (cwe:Weakness {id: 'CWE-507'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-698'})
MATCH (cwe:Weakness {id: 'CWE-829'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-699'})
MATCH (cwe:Weakness {id: 'CWE-1300'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-7'})
MATCH (cwe:Weakness {id: 'CWE-89'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-7'})
MATCH (cwe:Weakness {id: 'CWE-209'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-7'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-7'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-7'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-7'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-70'})
MATCH (cwe:Weakness {id: 'CWE-521'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-70'})
MATCH (cwe:Weakness {id: 'CWE-262'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-70'})
MATCH (cwe:Weakness {id: 'CWE-263'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-70'})
MATCH (cwe:Weakness {id: 'CWE-798'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-70'})
MATCH (cwe:Weakness {id: 'CWE-654'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-70'})
MATCH (cwe:Weakness {id: 'CWE-308'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-70'})
MATCH (cwe:Weakness {id: 'CWE-309'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-701'})
MATCH (cwe:Weakness {id: 'CWE-294'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-701'})
MATCH (cwe:Weakness {id: 'CWE-345'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-702'})
MATCH (cwe:Weakness {id: 'CWE-1296'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-71'})
MATCH (cwe:Weakness {id: 'CWE-176'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-71'})
MATCH (cwe:Weakness {id: 'CWE-179'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-71'})
MATCH (cwe:Weakness {id: 'CWE-180'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-71'})
MATCH (cwe:Weakness {id: 'CWE-173'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-71'})
MATCH (cwe:Weakness {id: 'CWE-172'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-71'})
MATCH (cwe:Weakness {id: 'CWE-184'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-71'})
MATCH (cwe:Weakness {id: 'CWE-183'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-71'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-71'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-71'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-71'})
MATCH (cwe:Weakness {id: 'CWE-692'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-72'})
MATCH (cwe:Weakness {id: 'CWE-173'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-72'})
MATCH (cwe:Weakness {id: 'CWE-177'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-72'})
MATCH (cwe:Weakness {id: 'CWE-172'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-72'})
MATCH (cwe:Weakness {id: 'CWE-73'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-72'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-72'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-73'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-73'})
MATCH (cwe:Weakness {id: 'CWE-184'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-73'})
MATCH (cwe:Weakness {id: 'CWE-96'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-73'})
MATCH (cwe:Weakness {id: 'CWE-348'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-73'})
MATCH (cwe:Weakness {id: 'CWE-116'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-73'})
MATCH (cwe:Weakness {id: 'CWE-350'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-73'})
MATCH (cwe:Weakness {id: 'CWE-86'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-73'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-74'})
MATCH (cwe:Weakness {id: 'CWE-372'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-74'})
MATCH (cwe:Weakness {id: 'CWE-315'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-74'})
MATCH (cwe:Weakness {id: 'CWE-353'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-74'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-74'})
MATCH (cwe:Weakness {id: 'CWE-1245'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-74'})
MATCH (cwe:Weakness {id: 'CWE-1253'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-74'})
MATCH (cwe:Weakness {id: 'CWE-1265'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-74'})
MATCH (cwe:Weakness {id: 'CWE-1271'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-75'})
MATCH (cwe:Weakness {id: 'CWE-349'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-75'})
MATCH (cwe:Weakness {id: 'CWE-99'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-75'})
MATCH (cwe:Weakness {id: 'CWE-77'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-75'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-75'})
MATCH (cwe:Weakness {id: 'CWE-353'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-75'})
MATCH (cwe:Weakness {id: 'CWE-354'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-76'})
MATCH (cwe:Weakness {id: 'CWE-23'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-76'})
MATCH (cwe:Weakness {id: 'CWE-22'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-76'})
MATCH (cwe:Weakness {id: 'CWE-73'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-76'})
MATCH (cwe:Weakness {id: 'CWE-77'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-76'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-76'})
MATCH (cwe:Weakness {id: 'CWE-348'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-76'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-76'})
MATCH (cwe:Weakness {id: 'CWE-272'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-76'})
MATCH (cwe:Weakness {id: 'CWE-59'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-76'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-76'})
MATCH (cwe:Weakness {id: 'CWE-15'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-77'})
MATCH (cwe:Weakness {id: 'CWE-15'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-77'})
MATCH (cwe:Weakness {id: 'CWE-94'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-77'})
MATCH (cwe:Weakness {id: 'CWE-96'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-77'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-77'})
MATCH (cwe:Weakness {id: 'CWE-302'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-77'})
MATCH (cwe:Weakness {id: 'CWE-473'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-77'})
MATCH (cwe:Weakness {id: 'CWE-1321'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-78'})
MATCH (cwe:Weakness {id: 'CWE-180'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-78'})
MATCH (cwe:Weakness {id: 'CWE-181'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-78'})
MATCH (cwe:Weakness {id: 'CWE-173'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-78'})
MATCH (cwe:Weakness {id: 'CWE-172'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-78'})
MATCH (cwe:Weakness {id: 'CWE-73'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-78'})
MATCH (cwe:Weakness {id: 'CWE-22'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-78'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-78'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-78'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-78'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-79'})
MATCH (cwe:Weakness {id: 'CWE-173'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-79'})
MATCH (cwe:Weakness {id: 'CWE-180'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-79'})
MATCH (cwe:Weakness {id: 'CWE-181'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-79'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-79'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-79'})
MATCH (cwe:Weakness {id: 'CWE-73'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-79'})
MATCH (cwe:Weakness {id: 'CWE-22'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-79'})
MATCH (cwe:Weakness {id: 'CWE-185'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-79'})
MATCH (cwe:Weakness {id: 'CWE-200'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-79'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-79'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-8'})
MATCH (cwe:Weakness {id: 'CWE-120'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-8'})
MATCH (cwe:Weakness {id: 'CWE-119'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-8'})
MATCH (cwe:Weakness {id: 'CWE-118'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-8'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-8'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-8'})
MATCH (cwe:Weakness {id: 'CWE-680'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-8'})
MATCH (cwe:Weakness {id: 'CWE-733'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-8'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-80'})
MATCH (cwe:Weakness {id: 'CWE-173'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-80'})
MATCH (cwe:Weakness {id: 'CWE-172'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-80'})
MATCH (cwe:Weakness {id: 'CWE-180'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-80'})
MATCH (cwe:Weakness {id: 'CWE-181'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-80'})
MATCH (cwe:Weakness {id: 'CWE-73'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-80'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-80'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-80'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-80'})
MATCH (cwe:Weakness {id: 'CWE-692'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-81'})
MATCH (cwe:Weakness {id: 'CWE-117'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-81'})
MATCH (cwe:Weakness {id: 'CWE-93'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-81'})
MATCH (cwe:Weakness {id: 'CWE-75'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-81'})
MATCH (cwe:Weakness {id: 'CWE-221'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-81'})
MATCH (cwe:Weakness {id: 'CWE-96'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-81'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-81'})
MATCH (cwe:Weakness {id: 'CWE-150'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-81'})
MATCH (cwe:Weakness {id: 'CWE-276'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-81'})
MATCH (cwe:Weakness {id: 'CWE-279'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-81'})
MATCH (cwe:Weakness {id: 'CWE-116'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-83'})
MATCH (cwe:Weakness {id: 'CWE-91'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-83'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-83'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-83'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-84'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-84'})
MATCH (cwe:Weakness {id: 'CWE-707'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-85'})
MATCH (cwe:Weakness {id: 'CWE-79'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-85'})
MATCH (cwe:Weakness {id: 'CWE-113'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-85'})
MATCH (cwe:Weakness {id: 'CWE-348'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-85'})
MATCH (cwe:Weakness {id: 'CWE-96'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-85'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-85'})
MATCH (cwe:Weakness {id: 'CWE-116'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-85'})
MATCH (cwe:Weakness {id: 'CWE-184'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-85'})
MATCH (cwe:Weakness {id: 'CWE-86'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-85'})
MATCH (cwe:Weakness {id: 'CWE-692'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-86'})
MATCH (cwe:Weakness {id: 'CWE-80'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-87'})
MATCH (cwe:Weakness {id: 'CWE-425'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-87'})
MATCH (cwe:Weakness {id: 'CWE-285'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-87'})
MATCH (cwe:Weakness {id: 'CWE-693'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-88'})
MATCH (cwe:Weakness {id: 'CWE-78'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-88'})
MATCH (cwe:Weakness {id: 'CWE-88'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-88'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-88'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-89'})
MATCH (cwe:Weakness {id: 'CWE-346'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-89'})
MATCH (cwe:Weakness {id: 'CWE-350'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-9'})
MATCH (cwe:Weakness {id: 'CWE-120'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-9'})
MATCH (cwe:Weakness {id: 'CWE-118'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-9'})
MATCH (cwe:Weakness {id: 'CWE-119'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-9'})
MATCH (cwe:Weakness {id: 'CWE-74'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-9'})
MATCH (cwe:Weakness {id: 'CWE-20'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-9'})
MATCH (cwe:Weakness {id: 'CWE-680'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-9'})
MATCH (cwe:Weakness {id: 'CWE-733'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-9'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-90'})
MATCH (cwe:Weakness {id: 'CWE-301'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-90'})
MATCH (cwe:Weakness {id: 'CWE-303'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-92'})
MATCH (cwe:Weakness {id: 'CWE-190'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-92'})
MATCH (cwe:Weakness {id: 'CWE-128'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-92'})
MATCH (cwe:Weakness {id: 'CWE-120'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-92'})
MATCH (cwe:Weakness {id: 'CWE-122'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-92'})
MATCH (cwe:Weakness {id: 'CWE-196'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-92'})
MATCH (cwe:Weakness {id: 'CWE-680'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-92'})
MATCH (cwe:Weakness {id: 'CWE-697'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-93'})
MATCH (cwe:Weakness {id: 'CWE-117'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-93'})
MATCH (cwe:Weakness {id: 'CWE-75'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-93'})
MATCH (cwe:Weakness {id: 'CWE-150'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-94'})
MATCH (cwe:Weakness {id: 'CWE-300'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-94'})
MATCH (cwe:Weakness {id: 'CWE-290'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-94'})
MATCH (cwe:Weakness {id: 'CWE-593'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-94'})
MATCH (cwe:Weakness {id: 'CWE-287'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-94'})
MATCH (cwe:Weakness {id: 'CWE-294'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-95'})
MATCH (cwe:Weakness {id: 'CWE-538'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-96'})
MATCH (cwe:Weakness {id: 'CWE-589'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-97'})
MATCH (cwe:Weakness {id: 'CWE-327'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-97'})
MATCH (cwe:Weakness {id: 'CWE-1204'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-97'})
MATCH (cwe:Weakness {id: 'CWE-1240'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-97'})
MATCH (cwe:Weakness {id: 'CWE-1241'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-97'})
MATCH (cwe:Weakness {id: 'CWE-1279'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-98'})
MATCH (cwe:Weakness {id: 'CWE-451'})
MERGE (capec)-[r:EXPLOITS_WEAKNESS]->(cwe)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


// ========================================
// 3. CREATE CAPEC→ATT&CK RELATIONSHIPS
// Total: 272 relationships
// ========================================


MATCH (capec:AttackPattern {id: 'CAPEC-1'})
MERGE (attack:Technique {id: '1574.010'})
ON CREATE SET attack.name = "Hijack Execution Flow: ServicesFile Permissions Weakness"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-11'})
MERGE (attack:Technique {id: '1036.006'})
ON CREATE SET attack.name = "Masquerading: Space after Filename"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-112'})
MERGE (attack:Technique {id: '1110'})
ON CREATE SET attack.name = "Brute Force"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-114'})
MERGE (attack:Technique {id: '1548'})
ON CREATE SET attack.name = "Abuse Elevation Control Mechanism"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-115'})
MERGE (attack:Technique {id: '1548'})
ON CREATE SET attack.name = "Abuse Elevation Control Mechanism"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-122'})
MERGE (attack:Technique {id: '1548'})
ON CREATE SET attack.name = "Abuse Elevation Control Mechanism"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-125'})
MERGE (attack:Technique {id: '1498.001'})
ON CREATE SET attack.name = "Network Denial of Service: Direct Network Flood"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-125'})
MERGE (attack:Technique {id: '1499'})
ON CREATE SET attack.name = "Endpoint Denial of Service"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-127'})
MERGE (attack:Technique {id: '1083'})
ON CREATE SET attack.name = "File and Directory Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-13'})
MERGE (attack:Technique {id: '1562.003'})
ON CREATE SET attack.name = "Impair Defenses:Impair Command History Logging"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-13'})
MERGE (attack:Technique {id: '1574.006'})
ON CREATE SET attack.name = "Hijack Execution Flow:Dynamic Linker Hijacking"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-13'})
MERGE (attack:Technique {id: '1574.007'})
ON CREATE SET attack.name = "Hijack Execution Flow:Path Interception by PATH Environment Variable"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-130'})
MERGE (attack:Technique {id: '1499.003'})
ON CREATE SET attack.name = "Endpoint Denial of Service:Application Exhaustion Flood"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-131'})
MERGE (attack:Technique {id: '1499'})
ON CREATE SET attack.name = "Endpoint Denial of Service"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-132'})
MERGE (attack:Technique {id: '1547.009'})
ON CREATE SET attack.name = "Boot or Logon Autostart Execution:Shortcut Modification"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-141'})
MERGE (attack:Technique {id: '1557.002'})
ON CREATE SET attack.name = "Adversary-in-the-Middle: ARP Cache Poisoning"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-142'})
MERGE (attack:Technique {id: '1584.002'})
ON CREATE SET attack.name = "Compromise Infrastructure: DNS Server"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-148'})
MERGE (attack:Technique {id: '1491'})
ON CREATE SET attack.name = "Defacement"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-150'})
MERGE (attack:Technique {id: '1003'})
ON CREATE SET attack.name = "OS Credential Dumping"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-150'})
MERGE (attack:Technique {id: '1119'})
ON CREATE SET attack.name = "Automated Collection"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-150'})
MERGE (attack:Technique {id: '1213'})
ON CREATE SET attack.name = "Data from Information Repositories"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-150'})
MERGE (attack:Technique {id: '1530'})
ON CREATE SET attack.name = "Data from Cloud Storage Object"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-150'})
MERGE (attack:Technique {id: '1555'})
ON CREATE SET attack.name = "Credentials from Password Stores"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-150'})
MERGE (attack:Technique {id: '1602'})
ON CREATE SET attack.name = "Data from Configuration Repository"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-158'})
MERGE (attack:Technique {id: '1040'})
ON CREATE SET attack.name = "Network Sniffing"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-158'})
MERGE (attack:Technique {id: '1111'})
ON CREATE SET attack.name = "Multi-Factor Authentication Interception"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-159'})
MERGE (attack:Technique {id: '1574.008'})
ON CREATE SET attack.name = "Hijack Execution Flow:Path Interception by Search Order Hijacking"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-163'})
MERGE (attack:Technique {id: '1534'})
ON CREATE SET attack.name = "Internal Spearfishing"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-163'})
MERGE (attack:Technique {id: '1566.001'})
ON CREATE SET attack.name = "Phishing: Spearfishing Attachment"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-163'})
MERGE (attack:Technique {id: '1566.002'})
ON CREATE SET attack.name = "Phishing: Spearfishing Link"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-163'})
MERGE (attack:Technique {id: '1566.003'})
ON CREATE SET attack.name = "Phishing: Spearfishing via Service"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-163'})
MERGE (attack:Technique {id: '1598.001'})
ON CREATE SET attack.name = "Phishing for Information: Spearfishing Service"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-163'})
MERGE (attack:Technique {id: '1598.002'})
ON CREATE SET attack.name = "Phishing for Information: Spearfishing Attachment"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-163'})
MERGE (attack:Technique {id: '1598.003'})
ON CREATE SET attack.name = "Phishing for Information: Spearfishing Link"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-165'})
MERGE (attack:Technique {id: '1036.003'})
ON CREATE SET attack.name = "Masquerading: Rename System Utilities"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-169'})
MERGE (attack:Technique {id: '1217'})
ON CREATE SET attack.name = "Browser Bookmark Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-169'})
MERGE (attack:Technique {id: '1592'})
ON CREATE SET attack.name = "Gather Victim Host Information"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-169'})
MERGE (attack:Technique {id: '1595'})
ON CREATE SET attack.name = "Active Scanning"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-17'})
MERGE (attack:Technique {id: '1574.005'})
ON CREATE SET attack.name = "Hijack Execution Flow: Executable Installer File Permissions Weakness"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-17'})
MERGE (attack:Technique {id: '1574.010'})
ON CREATE SET attack.name = "Hijack Execution Flow: Services File Permissions Weakness"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-177'})
MERGE (attack:Technique {id: '1036'})
ON CREATE SET attack.name = "Masquerading"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-180'})
MERGE (attack:Technique {id: '1574.010'})
ON CREATE SET attack.name = "Hijack Execution Flow: Services File Permissions Weaknesses"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-186'})
MERGE (attack:Technique {id: '1195.002'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Software Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-187'})
MERGE (attack:Technique {id: '1072'})
ON CREATE SET attack.name = "Software Deployment Tools"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-19'})
MERGE (attack:Technique {id: '1027.009'})
ON CREATE SET attack.name = "Obfuscated Files or Information:\u00a0Embedded Payloads"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-19'})
MERGE (attack:Technique {id: '1546.004'})
ON CREATE SET attack.name = "Event Triggered Execution:.bash_profile and .bashrc"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-19'})
MERGE (attack:Technique {id: '1546.016'})
ON CREATE SET attack.name = "Event Triggered Execution:\u00a0Installer Packages"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-191'})
MERGE (attack:Technique {id: '1552.001'})
ON CREATE SET attack.name = "Unsecured Credentials:Credentials in files"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-196'})
MERGE (attack:Technique {id: '1134.002'})
ON CREATE SET attack.name = "Access Token Manipulation: Create Process with Token"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-196'})
MERGE (attack:Technique {id: '1134.003'})
ON CREATE SET attack.name = "Access Token Manipulation: Make and Impersonate Token"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-196'})
MERGE (attack:Technique {id: '1606'})
ON CREATE SET attack.name = "Forge Web Credentials"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-2'})
MERGE (attack:Technique {id: '1531'})
ON CREATE SET attack.name = "Account Access Removal"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-203'})
MERGE (attack:Technique {id: '1112'})
ON CREATE SET attack.name = "Modify Registry"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-203'})
MERGE (attack:Technique {id: '1647'})
ON CREATE SET attack.name = "Plist Modification"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-204'})
MERGE (attack:Technique {id: '1005'})
ON CREATE SET attack.name = "Data from Local System"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-206'})
MERGE (attack:Technique {id: '1553.002'})
ON CREATE SET attack.name = "Subvert Trust Controls:Code Signing"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-21'})
MERGE (attack:Technique {id: '1134'})
ON CREATE SET attack.name = "Access Token Manipulation"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-21'})
MERGE (attack:Technique {id: '1528'})
ON CREATE SET attack.name = "Steal Application Access Token"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-21'})
MERGE (attack:Technique {id: '1539'})
ON CREATE SET attack.name = "Steal Web Session Cookie"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-227'})
MERGE (attack:Technique {id: '1499'})
ON CREATE SET attack.name = "Endpoint Denial of Service"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-233'})
MERGE (attack:Technique {id: '1548'})
ON CREATE SET attack.name = "Abuse Elevation Control Mechanism"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-25'})
MERGE (attack:Technique {id: '1499.004'})
ON CREATE SET attack.name = "Endpoint Denial of Service: Application or System Exploitation"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-251'})
MERGE (attack:Technique {id: '1055'})
ON CREATE SET attack.name = "Process Injection"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-267'})
MERGE (attack:Technique {id: '1027'})
ON CREATE SET attack.name = "Obfuscated Files or Information"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-268'})
MERGE (attack:Technique {id: '1070'})
ON CREATE SET attack.name = "Indicator Removal on Host"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-268'})
MERGE (attack:Technique {id: '1562.002'})
ON CREATE SET attack.name = "Impair Defenses: Disable Windows Event Logging"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-268'})
MERGE (attack:Technique {id: '1562.003'})
ON CREATE SET attack.name = "Impair Defenses: Impair Command History Logging"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-268'})
MERGE (attack:Technique {id: '1562.008'})
ON CREATE SET attack.name = "Impair Defenses: Disable Cloud Logs"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-270'})
MERGE (attack:Technique {id: '1547.001'})
ON CREATE SET attack.name = "Boot or Logon Autostart Execution: Registry Run Keys / Start Folder"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-270'})
MERGE (attack:Technique {id: '1547.014'})
ON CREATE SET attack.name = "Boot or Logon Autostart Execution: Active"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-292'})
MERGE (attack:Technique {id: '1018'})
ON CREATE SET attack.name = "Remote System Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-295'})
MERGE (attack:Technique {id: '1124'})
ON CREATE SET attack.name = "System Time Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-30'})
MERGE (attack:Technique {id: '1055.003'})
ON CREATE SET attack.name = "Process Injection: Thread Execution Hijacking"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-300'})
MERGE (attack:Technique {id: '1046'})
ON CREATE SET attack.name = "Network Service Scanning"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-309'})
MERGE (attack:Technique {id: '1016'})
ON CREATE SET attack.name = "System Network Configuration Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-309'})
MERGE (attack:Technique {id: '1049'})
ON CREATE SET attack.name = "System Network Connections Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-309'})
MERGE (attack:Technique {id: '1590'})
ON CREATE SET attack.name = "Gather Victim Network Information"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-31'})
MERGE (attack:Technique {id: '1539'})
ON CREATE SET attack.name = "Steal Web Session Cookie"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-312'})
MERGE (attack:Technique {id: '1082'})
ON CREATE SET attack.name = "System Information Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-313'})
MERGE (attack:Technique {id: '1082'})
ON CREATE SET attack.name = "System Information Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-35'})
MERGE (attack:Technique {id: '1027.006'})
ON CREATE SET attack.name = "Obfuscated Files or Information: HTML Smuggling"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-35'})
MERGE (attack:Technique {id: '1027.009'})
ON CREATE SET attack.name = "Obfuscated Files or Information:\u00a0Embedded Payloads"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-35'})
MERGE (attack:Technique {id: '1564.009'})
ON CREATE SET attack.name = "Hide Artifacts: Resource Forking"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MERGE (attack:Technique {id: '1005'})
ON CREATE SET attack.name = "Data from Local System"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-37'})
MERGE (attack:Technique {id: '1552.004'})
ON CREATE SET attack.name = "Unsecured Credentials: Private Keys"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-38'})
MERGE (attack:Technique {id: '1574.007'})
ON CREATE SET attack.name = "Hijack Execution Flow: Path Interception by PATH Environment Variable"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-38'})
MERGE (attack:Technique {id: '1574.009'})
ON CREATE SET attack.name = "Hijack Execution Flow: Path Interception by Unquoted Path"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-383'})
MERGE (attack:Technique {id: '1056.004'})
ON CREATE SET attack.name = "Input Capture: Credential API Hooking"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-407'})
MERGE (attack:Technique {id: '1589'})
ON CREATE SET attack.name = "Gather Victim Identity Information"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-438'})
MERGE (attack:Technique {id: '1195'})
ON CREATE SET attack.name = "Supply Chain Compromise"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-439'})
MERGE (attack:Technique {id: '1195'})
ON CREATE SET attack.name = "Supply Chain Compromise"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-440'})
MERGE (attack:Technique {id: '1195.003'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Hardware Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-440'})
MERGE (attack:Technique {id: '1200'})
ON CREATE SET attack.name = "Hardware Additions"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-442'})
MERGE (attack:Technique {id: '1195.001'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Software Dependencies and Development Tools"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-442'})
MERGE (attack:Technique {id: '1195.002'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Software Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-443'})
MERGE (attack:Technique {id: '1195.002'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Software Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-443'})
MERGE (attack:Technique {id: '1195.003'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Hardware Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-445'})
MERGE (attack:Technique {id: '1195.001'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Software Dependencies and Development Tools"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-446'})
MERGE (attack:Technique {id: '1195'})
ON CREATE SET attack.name = "Supply Chain Compromise"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-448'})
MERGE (attack:Technique {id: '1027.009'})
ON CREATE SET attack.name = "Obfuscated Files or Information:\u00a0Embedded Payloads"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-457'})
MERGE (attack:Technique {id: '1091'})
ON CREATE SET attack.name = "Replication Through Removable Media"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-457'})
MERGE (attack:Technique {id: '1092'})
ON CREATE SET attack.name = "Communication Through Removable Media"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-464'})
MERGE (attack:Technique {id: '1606.001'})
ON CREATE SET attack.name = "Forge Web Credentials: Web Cookies"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-465'})
MERGE (attack:Technique {id: '1090.001'})
ON CREATE SET attack.name = "Proxy: Internal Proxy"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-469'})
MERGE (attack:Technique {id: '1499.002'})
ON CREATE SET attack.name = "Endpoint Denial of Service: Service Exhaustion Flood"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-471'})
MERGE (attack:Technique {id: '1574.001'})
ON CREATE SET attack.name = "Hijack Execution Flow:DLL search order hijacking"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-471'})
MERGE (attack:Technique {id: '1574.004'})
ON CREATE SET attack.name = "Hijack Execution Flow: Dylib Hijacking"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-471'})
MERGE (attack:Technique {id: '1574.008'})
ON CREATE SET attack.name = "Hijack Execution Flow: Path Interception by Search Order Hijacking"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-473'})
MERGE (attack:Technique {id: '1036.001'})
ON CREATE SET attack.name = "Masquerading: Invalid Code Signature"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-473'})
MERGE (attack:Technique {id: '1553.002'})
ON CREATE SET attack.name = "Subvert Trust Controls: Code Signing"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-474'})
MERGE (attack:Technique {id: '1552.004'})
ON CREATE SET attack.name = "Unsecured Credentials: Private Keys"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-478'})
MERGE (attack:Technique {id: '1574.011'})
ON CREATE SET attack.name = "Hijack Execution Flow:Service Registry Permissions Weakness"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-478'})
MERGE (attack:Technique {id: '1543.003'})
ON CREATE SET attack.name = "Create or Modify System Process:Windows Service"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-479'})
MERGE (attack:Technique {id: '1553.004'})
ON CREATE SET attack.name = "Subvert Trust Controls:Install Root Certificate"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-480'})
MERGE (attack:Technique {id: '1611'})
ON CREATE SET attack.name = "Escape to Host"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-481'})
MERGE (attack:Technique {id: '1090.004'})
ON CREATE SET attack.name = "Proxy:Domain Fronting"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-482'})
MERGE (attack:Technique {id: '1498.001'})
ON CREATE SET attack.name = "Network Denial of Service: Direct Network Flood"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-482'})
MERGE (attack:Technique {id: '1499.001'})
ON CREATE SET attack.name = "Endpoint Denial of Service: OS Exhaustion Flood"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-482'})
MERGE (attack:Technique {id: '1499.002'})
ON CREATE SET attack.name = "Endpoint Denial of Service: Service Exhaustion Flood"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-485'})
MERGE (attack:Technique {id: '1552.004'})
ON CREATE SET attack.name = "Unsecure Credentials: Private Keys"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-488'})
MERGE (attack:Technique {id: '1499.002'})
ON CREATE SET attack.name = "Endpoint Denial of Service:Service Exhaustion Flood"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-489'})
MERGE (attack:Technique {id: '1499.002'})
ON CREATE SET attack.name = "Endpoint Denial of Service:Service Exhaustion Flood"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-49'})
MERGE (attack:Technique {id: '1110.001'})
ON CREATE SET attack.name = "Brute Force:Password Guessing"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-490'})
MERGE (attack:Technique {id: '1498.002'})
ON CREATE SET attack.name = "Network Denial of Service:Reflection Amplification"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-497'})
MERGE (attack:Technique {id: '1083'})
ON CREATE SET attack.name = "File and Directory Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-504'})
MERGE (attack:Technique {id: '1036.004'})
ON CREATE SET attack.name = "Masquerading: Masquerade Task or Service"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-509'})
MERGE (attack:Technique {id: '1558.003'})
ON CREATE SET attack.name = "Steal or Forge Kerberos Tickets:Kerberoasting"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-511'})
MERGE (attack:Technique {id: '1195.001'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Software Dependencies and Development Tools"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-516'})
MERGE (attack:Technique {id: '1195.003'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Hardware Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-520'})
MERGE (attack:Technique {id: '1195.003'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Hardware Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-522'})
MERGE (attack:Technique {id: '1195.003'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Hardware Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-523'})
MERGE (attack:Technique {id: '1195.002'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Software Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-528'})
MERGE (attack:Technique {id: '1499.002'})
ON CREATE SET attack.name = "Endpoint Denial of Service:Service Exhaustion Flood"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-528'})
MERGE (attack:Technique {id: '1498.001'})
ON CREATE SET attack.name = "Network Denial of Service:Direct Network Flood"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-531'})
MERGE (attack:Technique {id: '1195.003'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Hardware Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-532'})
MERGE (attack:Technique {id: '1495'})
ON CREATE SET attack.name = "Firmware Corruption"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-532'})
MERGE (attack:Technique {id: '1542.001'})
ON CREATE SET attack.name = "Pre-OS Boot:System Firmware"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-537'})
MERGE (attack:Technique {id: '1195.003'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Hardware Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-538'})
MERGE (attack:Technique {id: '1195.001'})
ON CREATE SET attack.name = "Supply Chain Compromise: Software Dependencies and Development Tools"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-539'})
MERGE (attack:Technique {id: '1195.003'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Hardware Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-541'})
MERGE (attack:Technique {id: '1592.002'})
ON CREATE SET attack.name = "Gather Victim Host Information: Software"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-542'})
MERGE (attack:Technique {id: '1587.001'})
ON CREATE SET attack.name = "Develop Capabilities: Malware"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-542'})
MERGE (attack:Technique {id: '1027'})
ON CREATE SET attack.name = "Obfuscated Files or Information"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-543'})
MERGE (attack:Technique {id: '1036.005'})
ON CREATE SET attack.name = "Masquerading: Match Legitimate Name or Location"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-545'})
MERGE (attack:Technique {id: '1005'})
ON CREATE SET attack.name = "Data from Local System"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-545'})
MERGE (attack:Technique {id: '1555.001'})
ON CREATE SET attack.name = "Credentials from Password Stores:Keychain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-55'})
MERGE (attack:Technique {id: '1110.002'})
ON CREATE SET attack.name = "Brute Force:Password Cracking"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-550'})
MERGE (attack:Technique {id: '1543'})
ON CREATE SET attack.name = "Create or Modify System Process"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-551'})
MERGE (attack:Technique {id: '1543'})
ON CREATE SET attack.name = "Create or Modify System Process"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-552'})
MERGE (attack:Technique {id: '1014'})
ON CREATE SET attack.name = "Rootkit"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-552'})
MERGE (attack:Technique {id: '1542.003'})
ON CREATE SET attack.name = "Pre-OS Boot:Bootkit"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-552'})
MERGE (attack:Technique {id: '1547.006'})
ON CREATE SET attack.name = "Boot or Logon Autostart Execution:Kernel Modules and Extensions"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-555'})
MERGE (attack:Technique {id: '1021'})
ON CREATE SET attack.name = "Remote Services"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-555'})
MERGE (attack:Technique {id: '1114.002'})
ON CREATE SET attack.name = "Email Collection:Remote Email Collection"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-555'})
MERGE (attack:Technique {id: '1133'})
ON CREATE SET attack.name = "External Remote Services"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-556'})
MERGE (attack:Technique {id: '1546.001'})
ON CREATE SET attack.name = "Event Triggered Execution:Change Default File Association"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-558'})
MERGE (attack:Technique {id: '1505.005'})
ON CREATE SET attack.name = "Server Software Component: Terminal Services DLL"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-558'})
MERGE (attack:Technique {id: '1546.008'})
ON CREATE SET attack.name = "Event Triggered Execution: Accessibility Features"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-560'})
MERGE (attack:Technique {id: '1078'})
ON CREATE SET attack.name = "Valid Accounts"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-561'})
MERGE (attack:Technique {id: '1021.002'})
ON CREATE SET attack.name = "Remote Services:SMB/Windows Admin Shares"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-562'})
MERGE (attack:Technique {id: '1080'})
ON CREATE SET attack.name = "Taint shared content"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-564'})
MERGE (attack:Technique {id: '1037'})
ON CREATE SET attack.name = "Boot or Logon Initialization Scripts"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-564'})
MERGE (attack:Technique {id: '1543.001'})
ON CREATE SET attack.name = "Create or Modify System Process: Launch Agent"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-564'})
MERGE (attack:Technique {id: '1543.004'})
ON CREATE SET attack.name = "Create or Modify System Process: Launch Daemon"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-564'})
MERGE (attack:Technique {id: '1547'})
ON CREATE SET attack.name = "Boot or Logon Autostart Execution"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-565'})
MERGE (attack:Technique {id: '1110.003'})
ON CREATE SET attack.name = "Brute Force:Password Spraying"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-568'})
MERGE (attack:Technique {id: '1056.001'})
ON CREATE SET attack.name = "Input Capture:Keylogging"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-569'})
MERGE (attack:Technique {id: '1056'})
ON CREATE SET attack.name = "Input Capture"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-57'})
MERGE (attack:Technique {id: '1040'})
ON CREATE SET attack.name = "Network Sniffing"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-571'})
MERGE (attack:Technique {id: '1562.002'})
ON CREATE SET attack.name = "Impair Defenses: Disable Windows Event Logging"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-571'})
MERGE (attack:Technique {id: '1562.002'})
ON CREATE SET attack.name = "Impair Defenses: Impair Command History Logging"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-571'})
MERGE (attack:Technique {id: '1562.006'})
ON CREATE SET attack.name = "Impair Defenses: Indicator Blocking"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-571'})
MERGE (attack:Technique {id: '1562.008'})
ON CREATE SET attack.name = "Impair Defenses: Disable Cloud Logs"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-572'})
MERGE (attack:Technique {id: '1027.001'})
ON CREATE SET attack.name = "Obfuscated Files or Information:Binary Padding"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-573'})
MERGE (attack:Technique {id: '1057'})
ON CREATE SET attack.name = "Process Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-574'})
MERGE (attack:Technique {id: '1007'})
ON CREATE SET attack.name = "System Service Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-575'})
MERGE (attack:Technique {id: '1087'})
ON CREATE SET attack.name = "Account Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-576'})
MERGE (attack:Technique {id: '1069'})
ON CREATE SET attack.name = "Permission Groups Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-576'})
MERGE (attack:Technique {id: '1615'})
ON CREATE SET attack.name = "Group Policy Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-577'})
MERGE (attack:Technique {id: '1033'})
ON CREATE SET attack.name = "System Owner/User Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-578'})
MERGE (attack:Technique {id: '1556.006'})
ON CREATE SET attack.name = "Modify Authentication Process:\u00a0Multi-Factor Authentication"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-578'})
MERGE (attack:Technique {id: '1562.001'})
ON CREATE SET attack.name = "Impair Defenses: Disable or Modify Tools"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-578'})
MERGE (attack:Technique {id: '1562.002'})
ON CREATE SET attack.name = "Impair Defenses: Disable Windows Event Logging"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-578'})
MERGE (attack:Technique {id: '1562.004'})
ON CREATE SET attack.name = "Impair Defenses: Disable or Modify System Firewall"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-578'})
MERGE (attack:Technique {id: '1562.007'})
ON CREATE SET attack.name = "Impair Defenses: Disable or Modify Cloud Firewall"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-578'})
MERGE (attack:Technique {id: '1562.008'})
ON CREATE SET attack.name = "Impair Defenses: Disable Cloud Logs"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-578'})
MERGE (attack:Technique {id: '1562.009'})
ON CREATE SET attack.name = "Impair Defenses: Safe Mode Boot"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-579'})
MERGE (attack:Technique {id: '1547.004'})
ON CREATE SET attack.name = "Boot or Logon Autostart Execution: Winlogon helper DLL"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-580'})
MERGE (attack:Technique {id: '1082'})
ON CREATE SET attack.name = "System Information Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-581'})
MERGE (attack:Technique {id: '1518.001'})
ON CREATE SET attack.name = "Software Discovery:Security Software Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-593'})
MERGE (attack:Technique {id: '1185'})
ON CREATE SET attack.name = "Browser Session Hijacking"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-593'})
MERGE (attack:Technique {id: '1550.001'})
ON CREATE SET attack.name = "Use Alternate Authentication Material:Application Access Token"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-593'})
MERGE (attack:Technique {id: '1563'})
ON CREATE SET attack.name = "Remote Service Session Hijacking"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-60'})
MERGE (attack:Technique {id: '1134.001'})
ON CREATE SET attack.name = "Access Token Manipulation:Token Impersonation/Theft"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-60'})
MERGE (attack:Technique {id: '1550.004'})
ON CREATE SET attack.name = "Use Alternate Authentication Material:Web Session Cookie"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-600'})
MERGE (attack:Technique {id: '1110.004'})
ON CREATE SET attack.name = "Brute Force:Credential Stuffing"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-609'})
MERGE (attack:Technique {id: '1111'})
ON CREATE SET attack.name = "Multi-Factor Authentication Interception"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-616'})
MERGE (attack:Technique {id: '1036.005'})
ON CREATE SET attack.name = "Masquerading: Match Legitimate Name or Location"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-620'})
MERGE (attack:Technique {id: '1600'})
ON CREATE SET attack.name = "Weaken Encryption"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-633'})
MERGE (attack:Technique {id: '1134'})
ON CREATE SET attack.name = "Access Token Manipulation"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-634'})
MERGE (attack:Technique {id: '1123'})
ON CREATE SET attack.name = "Audio Capture"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-634'})
MERGE (attack:Technique {id: '1125'})
ON CREATE SET attack.name = "Video Capture"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-635'})
MERGE (attack:Technique {id: '1036.007'})
ON CREATE SET attack.name = "Masquerading: Double File Extension"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-636'})
MERGE (attack:Technique {id: '1001.002'})
ON CREATE SET attack.name = "Data Obfuscation: Steganography"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-636'})
MERGE (attack:Technique {id: '1027.003'})
ON CREATE SET attack.name = "Obfuscated Files or Information: Steganography"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-636'})
MERGE (attack:Technique {id: '1027.004'})
ON CREATE SET attack.name = "Obfuscated Files or Information: Compile After Delivery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-636'})
MERGE (attack:Technique {id: '1218.001'})
ON CREATE SET attack.name = "Signed Binary Proxy Execution: Compiled HTML File"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-636'})
MERGE (attack:Technique {id: '1221'})
ON CREATE SET attack.name = "Template Injection"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-637'})
MERGE (attack:Technique {id: '1115'})
ON CREATE SET attack.name = "Clipboard Data"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-638'})
MERGE (attack:Technique {id: '1542.002'})
ON CREATE SET attack.name = "Pre-OS Boot:Component Firmware"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-639'})
MERGE (attack:Technique {id: '1039'})
ON CREATE SET attack.name = "Data from Network Shared Drive"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-639'})
MERGE (attack:Technique {id: '1552.001'})
ON CREATE SET attack.name = "Unsecured Credentials: Credentials in Files"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-639'})
MERGE (attack:Technique {id: '1552.003'})
ON CREATE SET attack.name = "Unsecured Credentials: Bash History"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-639'})
MERGE (attack:Technique {id: '1552.004'})
ON CREATE SET attack.name = "Unsecured Credentials: Private Keys"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-639'})
MERGE (attack:Technique {id: '1552.006'})
ON CREATE SET attack.name = "Unsecured Credentials: Group Policy Preferences"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-640'})
MERGE (attack:Technique {id: '1505.005'})
ON CREATE SET attack.name = "Server Software Component: Terminal Services DLL"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-640'})
MERGE (attack:Technique {id: '1574.006'})
ON CREATE SET attack.name = "Hijack Execution Flow: Dynamic Linker Hijacking"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-640'})
MERGE (attack:Technique {id: '1574.013'})
ON CREATE SET attack.name = "Hijack Execution Flow: KernelCallbackTable"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-640'})
MERGE (attack:Technique {id: '1620'})
ON CREATE SET attack.name = "Reflective Code Loading"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-641'})
MERGE (attack:Technique {id: '1574.002'})
ON CREATE SET attack.name = "Hijack Execution Flow:DLL Side-Loading"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-642'})
MERGE (attack:Technique {id: '1505.005'})
ON CREATE SET attack.name = "Server Software Component: Terminal Services DLL"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-642'})
MERGE (attack:Technique {id: '1554'})
ON CREATE SET attack.name = "Compromise Client Software Binary"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-642'})
MERGE (attack:Technique {id: '1574.005'})
ON CREATE SET attack.name = "Hijack Execution Flow:Executable Installer File Permissions Weakness"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-643'})
MERGE (attack:Technique {id: '1135'})
ON CREATE SET attack.name = "Network Share Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-644'})
MERGE (attack:Technique {id: '1550.002'})
ON CREATE SET attack.name = "Use Alternate Authentication Material:Pass The Hash"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-645'})
MERGE (attack:Technique {id: '1550.003'})
ON CREATE SET attack.name = "Use Alternate Authentication Material:Pass The Ticket"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-646'})
MERGE (attack:Technique {id: '1120'})
ON CREATE SET attack.name = "Peripheral Device Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-647'})
MERGE (attack:Technique {id: '1005'})
ON CREATE SET attack.name = "Data from Local System"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-647'})
MERGE (attack:Technique {id: '1012'})
ON CREATE SET attack.name = "Query Registry"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-647'})
MERGE (attack:Technique {id: '1552.002'})
ON CREATE SET attack.name = "Unsecured Credentials: Credentials in Registry"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-648'})
MERGE (attack:Technique {id: '1113'})
ON CREATE SET attack.name = "Screen Capture"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-648'})
MERGE (attack:Technique {id: '1513'})
ON CREATE SET attack.name = "Screen Capture"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-649'})
MERGE (attack:Technique {id: '1036.006'})
ON CREATE SET attack.name = "Masquerading:Space after Filename"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-65'})
MERGE (attack:Technique {id: '1040'})
ON CREATE SET attack.name = "Network Sniffing"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-650'})
MERGE (attack:Technique {id: '1505.003'})
ON CREATE SET attack.name = "Server Software Component:Web Shell"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-651'})
MERGE (attack:Technique {id: '1111'})
ON CREATE SET attack.name = "Multi-Factor Authentication Interception"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-652'})
MERGE (attack:Technique {id: '1558'})
ON CREATE SET attack.name = "Steal or Forge Kerberos Tickets"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-654'})
MERGE (attack:Technique {id: '1056'})
ON CREATE SET attack.name = "Input Capture"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-654'})
MERGE (attack:Technique {id: '1548.004'})
ON CREATE SET attack.name = "Abuse Elevation Control Mechanism: Elevated Execution with Prompt"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-655'})
MERGE (attack:Technique {id: '1027.001'})
ON CREATE SET attack.name = "Obfuscated Files or Information:Binary padding"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-657'})
MERGE (attack:Technique {id: '1072'})
ON CREATE SET attack.name = "Software Deployment Tools"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-660'})
MERGE (attack:Technique {id: '1055'})
ON CREATE SET attack.name = "Process Injection"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-662'})
MERGE (attack:Technique {id: '1185'})
ON CREATE SET attack.name = "Man in the Browser"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-665'})
MERGE (attack:Technique {id: '1211'})
ON CREATE SET attack.name = "Exploitation for Defensive Evasion"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-665'})
MERGE (attack:Technique {id: '1542.002'})
ON CREATE SET attack.name = "Pre-OS Boot: Component Firmware"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-665'})
MERGE (attack:Technique {id: '1556'})
ON CREATE SET attack.name = "Modify Authentication Process"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-666'})
MERGE (attack:Technique {id: '1498.001'})
ON CREATE SET attack.name = "Network Denial of Service: Direct Network Flood"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-666'})
MERGE (attack:Technique {id: '1499.001'})
ON CREATE SET attack.name = "Endpoint Denial of Service: OS Exhaustion Flood"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-668'})
MERGE (attack:Technique {id: '1565.002'})
ON CREATE SET attack.name = "Data Manipulation: Transmitted Data Manipulation"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-669'})
MERGE (attack:Technique {id: '1195.002'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Software Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-670'})
MERGE (attack:Technique {id: '1127'})
ON CREATE SET attack.name = "Trusted Developer Utilities Proxy Execution"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-670'})
MERGE (attack:Technique {id: '1195.001'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Software Dependencies and Development Tools"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-671'})
MERGE (attack:Technique {id: '1195.003'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Hardware Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-672'})
MERGE (attack:Technique {id: '1195.003'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Hardware Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-673'})
MERGE (attack:Technique {id: '1195.002'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Software Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-674'})
MERGE (attack:Technique {id: '1195.003'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Hardware Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-675'})
MERGE (attack:Technique {id: '1052'})
ON CREATE SET attack.name = "Exfiltration Over Physical Medium"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-677'})
MERGE (attack:Technique {id: '1195.003'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Hardware Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-678'})
MERGE (attack:Technique {id: '1195.002'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Software Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-68'})
MERGE (attack:Technique {id: '1553.002'})
ON CREATE SET attack.name = "Subvert Trust Controls: Code Signing"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-691'})
MERGE (attack:Technique {id: '1195.001'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Software Dependencies and Development Tools"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-691'})
MERGE (attack:Technique {id: '1195.002'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Software Supply Chain"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-694'})
MERGE (attack:Technique {id: '1614'})
ON CREATE SET attack.name = "System Language Discovery"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-695'})
MERGE (attack:Technique {id: '1195.001'})
ON CREATE SET attack.name = "Supply Chain Compromise: Compromise Software Dependencies and Development Tools"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-697'})
MERGE (attack:Technique {id: '1557.003'})
ON CREATE SET attack.name = "Adversary-in-the-Middle: DHCP Spoofing"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-698'})
MERGE (attack:Technique {id: '1176'})
ON CREATE SET attack.name = "Browser Extensions"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-698'})
MERGE (attack:Technique {id: '1505.004'})
ON CREATE SET attack.name = "Server Software Component: IIS Components"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-70'})
MERGE (attack:Technique {id: '1078.001'})
ON CREATE SET attack.name = "Valid Accounts:Default Accounts"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-700'})
MERGE (attack:Technique {id: '1599'})
ON CREATE SET attack.name = "Network Boundary Bridging"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-94'})
MERGE (attack:Technique {id: '1557'})
ON CREATE SET attack.name = "Adversary-in-the-Middle"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-98'})
MERGE (attack:Technique {id: '1566'})
ON CREATE SET attack.name = "Phishing"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-98'})
MERGE (attack:Technique {id: '1598'})
ON CREATE SET attack.name = "Phishing for Information"
MERGE (capec)-[r:IMPLEMENTS_TECHNIQUE]->(attack)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


// ========================================
// 4. CREATE CAPEC→OWASP RELATIONSHIPS
// Total: 39 relationships
// ========================================


MATCH (capec:AttackPattern {id: 'CAPEC-10'})
MERGE (owasp:OWASPCategory {name: "Buffer Overflow via Environment Variables"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-100'})
MERGE (owasp:OWASPCategory {name: "Buffer overflow attack"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-101'})
MERGE (owasp:OWASPCategory {name: "Server-Side Includes (SSI) Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-103'})
MERGE (owasp:OWASPCategory {name: "Clickjacking"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-107'})
MERGE (owasp:OWASPCategory {name: "Cross Site Tracing"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-112'})
MERGE (owasp:OWASPCategory {name: "Brute force attack"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-125'})
MERGE (owasp:OWASPCategory {name: "Traffic flood"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-126'})
MERGE (owasp:OWASPCategory {name: "Path Traversal"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-135'})
MERGE (owasp:OWASPCategory {name: "Format string attack"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-136'})
MERGE (owasp:OWASPCategory {name: "LDAP Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-141'})
MERGE (owasp:OWASPCategory {name: "Cache Poisoning"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-148'})
MERGE (owasp:OWASPCategory {name: "Content Spoofing"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-168'})
MERGE (owasp:OWASPCategory {name: "Windows alternate data stream"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-176'})
MERGE (owasp:OWASPCategory {name: "Setting Manipulation"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-240'})
MERGE (owasp:OWASPCategory {name: "Resource Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-242'})
MERGE (owasp:OWASPCategory {name: "Code Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-248'})
MERGE (owasp:OWASPCategory {name: "Command Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-268'})
MERGE (owasp:OWASPCategory {name: "Log Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-460'})
MERGE (owasp:OWASPCategory {name: "Web Parameter Tampering"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-492'})
MERGE (owasp:OWASPCategory {name: "Regular expression Denial of Service - ReDoS"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-52'})
MERGE (owasp:OWASPCategory {name: "Embedding Null Code"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-587'})
MERGE (owasp:OWASPCategory {name: "Cross Frame Scripting"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-588'})
MERGE (owasp:OWASPCategory {name: "Reflected DOM Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-59'})
MERGE (owasp:OWASPCategory {name: "Session Prediction"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-593'})
MERGE (owasp:OWASPCategory {name: "Session hijacking attack"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-600'})
MERGE (owasp:OWASPCategory {name: "Credential stuffing"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-61'})
MERGE (owasp:OWASPCategory {name: "Session fixation"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-62'})
MERGE (owasp:OWASPCategory {name: "Cross Site Request Forgery (CSRF)"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-63'})
MERGE (owasp:OWASPCategory {name: "Cross Site Scripting (XSS)"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-642'})
MERGE (owasp:OWASPCategory {name: "Binary planting"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-66'})
MERGE (owasp:OWASPCategory {name: "SQL Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-662'})
MERGE (owasp:OWASPCategory {name: "Man-in-the-browser attack"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-7'})
MERGE (owasp:OWASPCategory {name: "Blind SQL Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-71'})
MERGE (owasp:OWASPCategory {name: "Unicode Encoding"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-83'})
MERGE (owasp:OWASPCategory {name: "Blind XPath Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-83'})
MERGE (owasp:OWASPCategory {name: "XPATH Injection"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Detailed";


MATCH (capec:AttackPattern {id: 'CAPEC-87'})
MERGE (owasp:OWASPCategory {name: "Forced browsing"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";


MATCH (capec:AttackPattern {id: 'CAPEC-94'})
MERGE (owasp:OWASPCategory {name: "Man-in-the-middle attack"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Meta";


MATCH (capec:AttackPattern {id: 'CAPEC-97'})
MERGE (owasp:OWASPCategory {name: "Cryptanalysis"})
ON CREATE SET owasp.source = 'OWASP_Attacks',
              owasp.type = 'attack_category'
MERGE (capec)-[r:MAPS_TO_OWASP]->(owasp)
SET r.source = 'CAPEC_v3.9_XML',
    r.capec_abstraction = "Standard";
