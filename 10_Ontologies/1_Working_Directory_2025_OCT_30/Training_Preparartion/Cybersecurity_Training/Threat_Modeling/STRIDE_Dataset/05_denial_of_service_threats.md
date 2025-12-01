# STRIDE: Denial of Service Threats

## Entity Type
THREAT_MODEL, ATTACK_VECTOR, MITIGATION

## Overview
Denial of Service (DoS) threats prevent legitimate users from accessing systems, services, or resources. This includes resource exhaustion, service disruption, system crashes, and availability violations.

## Threat Patterns (200+ patterns)

### Network-Level DoS

#### Pattern: SYN Flood Attack
- **Threat**: Exhaust server resources with half-open TCP connections
- **DFD Element**: External Entity → Process (Network Service)
- **Attack Vector**: Mass TCP SYN packets without completing handshake
- **Impact**: Connection table exhaustion, legitimate connections refused
- **STRIDE Category**: Denial of Service
- **Mitigation**: SYN cookies, rate limiting, firewall rules, DDoS mitigation services
- **NIST Controls**: SC-5 (Denial of Service Protection), SC-7 (Boundary Protection)
- **IEC 62443**: FR 7 (Resource Availability), SR 7.1 (DoS Protection)
- **Detection**: Connection monitoring, SYN-to-ACK ratio analysis

#### Pattern: UDP Flood Attack
- **Threat**: Overwhelm target with UDP packets to random ports
- **DFD Element**: External Entity → Process (Network Stack)
- **Attack Vector**: Spoofed source IPs, amplification attacks
- **Impact**: Bandwidth saturation, CPU exhaustion, service unavailability
- **STRIDE Category**: Denial of Service
- **Mitigation**: Rate limiting, ingress filtering (BCP38), DDoS mitigation, UDP service hardening
- **NIST Controls**: SC-5, SC-7, CM-7 (Least Functionality)
- **IEC 62443**: SR 7.1, SR 7.2 (Resource Management)
- **Detection**: Traffic volume monitoring, packet inspection, anomaly detection

#### Pattern: ICMP Flood (Ping Flood)
- **Threat**: Flood target with ICMP Echo Request packets
- **DFD Element**: External Entity → Process (Network Interface)
- **Attack Vector**: Botnet-distributed ICMP packets
- **Impact**: Bandwidth consumption, CPU overhead, network congestion
- **STRIDE Category**: Denial of Service
- **Mitigation**: ICMP rate limiting, filtering, disable ICMP echo if not needed
- **NIST Controls**: SC-5, SC-7, CM-6 (Configuration Settings)
- **IEC 62443**: SR 7.1, FR 7
- **Detection**: ICMP traffic monitoring, volume thresholds

#### Pattern: DNS Amplification Attack
- **Threat**: Amplify small query into large response directed at victim
- **DFD Element**: External Entity (Attacker) → Process (Open DNS Resolver) → Victim
- **Attack Vector**: Spoofed source IP, DNSSEC queries (large responses)
- **Impact**: Bandwidth exhaustion, service disruption
- **STRIDE Category**: Denial of Service
- **Mitigation**: Disable open resolvers, rate limiting, response rate limiting (RRL), BCP38
- **NIST Controls**: SC-5, SC-7, CM-7
- **IEC 62443**: SR 7.1, FR 7
- **Detection**: Abnormal query patterns, response size monitoring

#### Pattern: NTP Amplification Attack
- **Threat**: Use NTP monlist command for traffic amplification
- **DFD Element**: External Entity → Process (NTP Server) → Victim
- **Attack Vector**: Spoofed source IP, vulnerable NTP servers
- **Impact**: 200:1+ amplification factor, massive bandwidth consumption
- **STRIDE Category**: Denial of Service
- **Mitigation**: Disable monlist, update NTP, rate limiting, BCP38
- **NIST Controls**: SC-5, SC-7, SI-2 (Flaw Remediation)
- **IEC 62443**: SR 7.1, FR 7
- **Detection**: NTP traffic anomalies, monlist request detection

#### Pattern: Memcached Amplification Attack
- **Threat**: Exploit exposed Memcached for massive amplification
- **DFD Element**: External Entity → Process (Memcached Server) → Victim
- **Attack Vector**: UDP-exposed Memcached, spoofed source
- **Impact**: 10,000:1+ amplification, largest recorded DDoS attacks
- **STRIDE Category**: Denial of Service
- **Mitigation**: Bind to localhost, disable UDP, firewall rules, BCP38
- **NIST Controls**: SC-5, SC-7, CM-6, CM-7
- **IEC 62443**: SR 7.1, FR 7
- **Detection**: Memcached traffic monitoring, external exposure scanning

### Application-Layer DoS

#### Pattern: HTTP GET/POST Flood (Layer 7)
- **Threat**: Overwhelm web server with legitimate-looking HTTP requests
- **DFD Element**: External Entity → Process (Web Server/Application)
- **Attack Vector**: Botnet, distributed slow requests
- **Impact**: Application resource exhaustion, slow response, service outage
- **STRIDE Category**: Denial of Service
- **Mitigation**: Rate limiting, CDN, WAF, connection limits, CAPTCHA
- **NIST Controls**: SC-5, AC-4 (Information Flow Enforcement)
- **IEC 62443**: SR 7.1, SR 7.2
- **Detection**: Request rate monitoring, behavioral analysis

#### Pattern: Slowloris Attack
- **Threat**: Hold many connections open by sending partial HTTP requests
- **DFD Element**: External Entity → Process (Web Server) connections
- **Attack Vector**: Slow, partial HTTP headers
- **Impact**: Connection pool exhaustion, legitimate clients blocked
- **STRIDE Category**: Denial of Service
- **Mitigation**: Connection timeouts, mod_reqtimeout, reverse proxy limits, CDN
- **NIST Controls**: SC-5, SC-23 (Session Authenticity)
- **IEC 62443**: SR 7.1, SR 7.2
- **Detection**: Connection duration monitoring, incomplete request detection

#### Pattern: R-U-Dead-Yet (RUDY) Attack
- **Threat**: Slow POST attack holding connections with slow form submission
- **DFD Element**: External Entity → Process (Web Application) POST processing
- **Attack Vector**: Extremely slow POST body transmission
- **Impact**: Application thread exhaustion, form processing DoS
- **STRIDE Category**: Denial of Service
- **Mitigation**: Request timeout, POST size limits, rate limiting, WAF
- **NIST Controls**: SC-5, SI-10 (Input Validation)
- **IEC 62443**: SR 7.1, SR 7.2
- **Detection**: Request duration monitoring, POST rate analysis

#### Pattern: XML Bomb (Billion Laughs)
- **Threat**: Exponentially expanding XML entities cause parser exhaustion
- **DFD Element**: Data Flow (XML) → Process (XML Parser)
- **Attack Vector**: Nested entity definitions, quadratic blowup
- **Impact**: CPU/memory exhaustion, parser crash, service denial
- **STRIDE Category**: Denial of Service
- **Mitigation**: Disable external entities, entity expansion limits, input validation
- **NIST Controls**: SI-10, SC-5, SI-16 (Memory Protection)
- **IEC 62443**: SR 3.5 (Input Validation), SR 7.2
- **Detection**: XML parsing errors, resource usage spikes

#### Pattern: Regular Expression DoS (ReDoS)
- **Threat**: Malicious input triggers catastrophic backtracking in regex
- **DFD Element**: Data Flow (User Input) → Process (Regex Engine)
- **Attack Vector**: Specially crafted input exploiting regex complexity
- **Impact**: CPU exhaustion, application hang, timeout
- **STRIDE Category**: Denial of Service
- **Mitigation**: Regex complexity analysis, timeout limits, input validation, safe regex libraries
- **NIST Controls**: SI-10, SC-5, SI-16
- **IEC 62443**: SR 3.5, SR 7.2
- **Detection**: Regex execution time monitoring, pattern analysis

#### Pattern: Algorithmic Complexity Attack (Hash Collision)
- **Threat**: Trigger worst-case algorithm performance (O(n²) vs O(n))
- **DFD Element**: Data Flow (Input) → Process (Algorithm)
- **Attack Vector**: Crafted input causing hash collisions, sorted data to quicksort
- **Impact**: CPU exhaustion, slow response, service degradation
- **STRIDE Category**: Denial of Service
- **Mitigation**: Randomized algorithms, input limits, complexity-aware implementations
- **NIST Controls**: SI-10, SC-5, SI-16
- **IEC 62443**: SR 3.5, SR 7.2
- **Detection**: Performance monitoring, execution time anomalies

### Resource Exhaustion

#### Pattern: Memory Leak Exploitation
- **Threat**: Trigger memory leaks to exhaust available RAM
- **DFD Element**: Process (Application) memory management
- **Attack Vector**: Repeated operations causing memory not to be freed
- **Impact**: Out-of-memory condition, application crash, server instability
- **STRIDE Category**: Denial of Service
- **Mitigation**: Memory profiling, leak detection tools, resource limits, restart strategies
- **NIST Controls**: SI-16, SC-5, SI-11 (Error Handling)
- **IEC 62443**: SR 7.2, FR 7
- **Detection**: Memory usage monitoring, gradual increase detection

#### Pattern: Disk Space Exhaustion
- **Threat**: Fill disk space with logs, uploads, or temp files
- **DFD Element**: Data Store (Disk) capacity
- **Attack Vector**: Mass file uploads, log flooding, temp file creation
- **Impact**: Application failure, log rotation failure, system instability
- **STRIDE Category**: Denial of Service
- **Mitigation**: Disk quotas, size limits, cleanup policies, monitoring
- **NIST Controls**: AU-4 (Audit Storage Capacity), SC-5
- **IEC 62443**: SR 7.2, AU-4
- **Detection**: Disk space monitoring, growth rate alerts

#### Pattern: File Descriptor Exhaustion
- **Threat**: Open maximum file/socket descriptors, blocking new connections
- **DFD Element**: Process (Application) file descriptor table
- **Attack Vector**: Many connections/files without closing
- **Impact**: Unable to accept connections, file operations fail
- **STRIDE Category**: Denial of Service
- **Mitigation**: Connection limits, ulimit settings, proper resource cleanup, connection pooling
- **NIST Controls**: SC-5, SC-6 (Resource Availability), SI-16
- **IEC 62443**: SR 7.2, FR 7
- **Detection**: File descriptor monitoring, "too many open files" errors

#### Pattern: Thread/Process Pool Exhaustion
- **Threat**: Consume all worker threads/processes, blocking request processing
- **DFD Element**: Process (Application Server) worker pool
- **Attack Vector**: Slow or blocking requests holding threads
- **Impact**: Application unresponsive, queue saturation
- **STRIDE Category**: Denial of Service
- **Mitigation**: Thread pool limits, request timeouts, async processing, queue limits
- **NIST Controls**: SC-5, SC-6
- **IEC 62443**: SR 7.2, FR 7
- **Detection**: Thread pool monitoring, queue depth alerts

#### Pattern: Database Connection Pool Exhaustion
- **Threat**: Hold all database connections, preventing new queries
- **DFD Element**: Process (DB Connection Pool) → Data Store (Database)
- **Attack Vector**: Long-running queries, connection leaks
- **Impact**: Application unable to query database, timeout errors
- **STRIDE Category**: Denial of Service
- **Mitigation**: Connection pool limits, query timeouts, connection leak detection
- **NIST Controls**: SC-5, SC-6, SI-16
- **IEC 62443**: SR 7.2, FR 7
- **Detection**: Connection pool monitoring, query performance tracking

### Distributed Denial of Service (DDoS)

#### Pattern: Botnet-Based DDoS
- **Threat**: Coordinate thousands/millions of compromised devices for attack
- **DFD Element**: Many External Entities (Botnet) → Process (Target)
- **Attack Vector**: Infected IoT devices, compromised hosts
- **Impact**: Overwhelming traffic volume, service unavailability
- **STRIDE Category**: Denial of Service
- **Mitigation**: DDoS mitigation services (Cloudflare, Akamai), scrubbing centers, anycast
- **NIST Controls**: SC-5, SC-7, SI-4 (System Monitoring)
- **IEC 62443**: SR 7.1, FR 7
- **Detection**: Traffic volume monitoring, geolocation analysis, behavior patterns

#### Pattern: IoT Device Swarm Attack (Mirai-style)
- **Threat**: Massive botnet of IoT devices with default credentials
- **DFD Element**: Many External Entities (IoT Devices) → Process (Target)
- **Attack Vector**: Compromised cameras, DVRs, routers
- **Impact**: Terabit-scale attacks, ISP-level impact
- **STRIDE Category**: Denial of Service
- **Mitigation**: IoT security hardening, default password changes, DDoS mitigation
- **NIST Controls**: IA-5 (Authenticator Management), SC-5
- **IEC 62443**: SR 1.5, SR 7.1, FR 7
- **Detection**: Unusual traffic sources, IoT device behavior monitoring

#### Pattern: Reflection Attack
- **Threat**: Use legitimate servers to reflect amplified traffic to victim
- **DFD Element**: External Entity → Process (Reflector) → Victim
- **Attack Vector**: Spoofed source IP, open services (DNS, NTP, etc.)
- **Impact**: Amplified bandwidth consumption, difficult attribution
- **STRIDE Category**: Denial of Service
- **Mitigation**: BCP38 (ingress filtering), rate limiting, disable open services
- **NIST Controls**: SC-5, SC-7, CM-7
- **IEC 62443**: SR 7.1, FR 7
- **Detection**: Reflection pattern detection, source IP validation

### Protocol-Specific DoS

#### Pattern: SSL/TLS Renegotiation Attack
- **Threat**: Force repeated SSL renegotiation to exhaust CPU
- **DFD Element**: External Entity → Process (SSL/TLS Server)
- **Attack Vector**: Client-initiated renegotiation
- **Impact**: CPU exhaustion (renegotiation is computationally expensive)
- **STRIDE Category**: Denial of Service
- **Mitigation**: Disable renegotiation, rate limiting, TLS 1.3 (no renegotiation)
- **NIST Controls**: SC-5, SC-8 (Transmission Protection), SC-13
- **IEC 62443**: SR 4.3 (Cryptography), SR 7.1
- **Detection**: Renegotiation frequency monitoring

#### Pattern: BGP Route Injection DoS
- **Threat**: Inject invalid routes causing traffic blackholing
- **DFD Element**: External Entity (Malicious AS) → Internet Routing
- **Attack Vector**: BGP hijacking, route announcement
- **Impact**: Traffic unreachable, service unavailability, internet outage
- **STRIDE Category**: Denial of Service + Spoofing
- **Mitigation**: RPKI, route filtering, BGP authentication, IRR validation
- **NIST Controls**: SC-5, SC-7, SC-24 (Fail in Known State)
- **IEC 62443**: SR 7.1, FR 7, FR 5
- **Detection**: BGP monitoring, route anomaly detection

#### Pattern: SIP INVITE Flood
- **Threat**: Overwhelm VoIP server with INVITE requests
- **DFD Element**: External Entity → Process (SIP Server)
- **Attack Vector**: Unauthenticated SIP INVITE messages
- **Impact**: VoIP service disruption, call processing failure
- **STRIDE Category**: Denial of Service
- **Mitigation**: SIP authentication, rate limiting, firewall rules, SIP ALG
- **NIST Controls**: SC-5, IA-3 (Device Identification)
- **IEC 62443**: SR 7.1, FR 1, FR 7
- **Detection**: SIP traffic rate monitoring, invalid INVITE detection

#### Pattern: SMTP Mail Bomb
- **Threat**: Flood mail server with messages or large attachments
- **DFD Element**: External Entity → Process (Mail Server) → Data Store (Mailboxes)
- **Attack Vector**: Mass email sending, large attachments
- **Impact**: Mail queue saturation, storage exhaustion, service degradation
- **STRIDE Category**: Denial of Service
- **Mitigation**: Rate limiting, message size limits, greylisting, spam filtering
- **NIST Controls**: SC-5, SI-8 (Spam Protection)
- **IEC 62443**: SR 7.1, SR 7.2
- **Detection**: Mail queue monitoring, traffic volume analysis

### Database and Storage DoS

#### Pattern: Expensive Query DoS
- **Threat**: Execute computationally expensive database queries
- **DFD Element**: Process (Application) → Data Store (Database)
- **Attack Vector**: Unoptimized queries, missing indexes, Cartesian products
- **Impact**: Database CPU exhaustion, slow queries, application timeout
- **STRIDE Category**: Denial of Service
- **Mitigation**: Query timeouts, query governor, resource limits, query optimization
- **NIST Controls**: SC-5, SI-10, AC-6
- **IEC 62443**: SR 7.2, FR 7
- **Detection**: Query performance monitoring, slow query logs

#### Pattern: Table Scan Forcing
- **Threat**: Force full table scans on large tables
- **DFD Element**: Data Flow (Query) → Data Store (Large Table)
- **Attack Vector**: Queries without indexed columns
- **Impact**: I/O saturation, query backlog, database slowdown
- **STRIDE Category**: Denial of Service
- **Mitigation**: Query validation, required indexes, query complexity limits
- **NIST Controls**: SC-5, SI-10
- **IEC 62443**: SR 7.2, SR 3.5
- **Detection**: Query execution plan analysis, I/O monitoring

#### Pattern: Transaction Lock Holding
- **Threat**: Hold database locks indefinitely, blocking other transactions
- **DFD Element**: Data Store (Database) locking mechanism
- **Attack Vector**: Long transactions, intentional lock holding
- **Impact**: Deadlocks, transaction timeouts, application unavailability
- **STRIDE Category**: Denial of Service
- **Mitigation**: Transaction timeouts, lock timeout, lock monitoring, query optimization
- **NIST Controls**: SC-5, SI-10
- **IEC 62443**: SR 7.2, FR 7
- **Detection**: Lock monitoring, deadlock detection, long transaction alerts

#### Pattern: Log File Flooding
- **Threat**: Generate massive log volume to exhaust storage or processing
- **DFD Element**: Process (Application) → Data Store (Log Files)
- **Attack Vector**: Trigger verbose logging, error condition loops
- **Impact**: Disk exhaustion, log rotation issues, SIEM overwhelm
- **STRIDE Category**: Denial of Service + Repudiation
- **Mitigation**: Log rate limiting, log level controls, storage monitoring, log aggregation
- **NIST Controls**: AU-4 (Audit Storage), AU-5 (Response to Audit Failure), SC-5
- **IEC 62443**: SR 6.1, SR 7.2
- **Detection**: Log volume monitoring, storage alerts

### Industrial Control System (ICS) DoS

#### Pattern: PLC CPU Overload
- **Threat**: Overload PLC with excessive commands or processing
- **DFD Element**: External Entity → Process (PLC CPU)
- **Attack Vector**: Command flooding, logic bomb, complex calculations
- **Impact**: PLC unresponsive, missed control deadlines, process disruption
- **STRIDE Category**: Denial of Service
- **Mitigation**: Command rate limiting, network segmentation, input validation, watchdog timers
- **NIST Controls**: SC-5, SC-7, SI-10
- **IEC 62443**: SR 7.1, SR 7.2, FR 7, FR 5
- **Detection**: PLC scan time monitoring, CPU utilization alerts

#### Pattern: SCADA Network Flooding
- **Threat**: Flood industrial network with excessive traffic
- **DFD Element**: External Entity → Data Flow (Industrial Network)
- **Attack Vector**: Broadcast storms, command flooding, scan traffic
- **Impact**: Communication delays, lost control messages, safety hazards
- **STRIDE Category**: Denial of Service
- **Mitigation**: Network segmentation, VLANs, traffic prioritization (QoS), firewalls
- **NIST Controls**: SC-5, SC-7, AC-4 (Information Flow)
- **IEC 62443**: FR 5, SR 5.1, SR 7.1
- **Detection**: Network traffic monitoring, latency measurement

#### Pattern: HMI Connection Exhaustion
- **Threat**: Consume all HMI connections to lock out operators
- **DFD Element**: External Entity → Process (HMI Server) connection pool
- **Attack Vector**: Multiple connection attempts, connection holding
- **Impact**: Operators unable to monitor/control processes, safety risks
- **STRIDE Category**: Denial of Service
- **Mitigation**: Connection limits, priority connections, authentication, network segmentation
- **NIST Controls**: SC-5, AC-3, SC-6
- **IEC 62443**: SR 7.1, FR 1, FR 7
- **Detection**: Connection monitoring, failed connection attempts

#### Pattern: Safety System Overload
- **Threat**: Overwhelm safety instrumented systems (SIS)
- **DFD Element**: External Entity → Process (Safety PLC/ESD)
- **Attack Vector**: Command flooding, alarm flooding, communication disruption
- **Impact**: Safety system failure, inability to detect/respond to hazards, catastrophic events
- **STRIDE Category**: Denial of Service (Safety Critical)
- **Mitigation**: Dedicated safety networks, physical separation, redundancy, hardened protocols
- **NIST Controls**: SC-5, SC-7, CP-2 (Contingency Plan), PE-13 (Fire Protection)
- **IEC 62443**: SL 3-4 requirements, FR 7, SR 7.1, SR 7.6 (Failsafe)
- **Detection**: Safety system health monitoring, communication watchdogs

### Cloud and Virtualization DoS

#### Pattern: VM Resource Exhaustion
- **Threat**: Exhaust allocated VM resources (CPU, memory, I/O)
- **DFD Element**: Process (VM) resource limits
- **Attack Vector**: CPU-intensive operations, memory allocation, disk I/O
- **Impact**: VM unavailability, co-tenant impact (noisy neighbor)
- **STRIDE Category**: Denial of Service
- **Mitigation**: Resource quotas, monitoring, auto-scaling, isolation
- **NIST Controls**: SC-5, SC-6, SI-16
- **IEC 62443**: SR 7.2, FR 7
- **Detection**: Resource utilization monitoring, performance alerts

#### Pattern: Serverless Function Timeout Exploitation
- **Threat**: Trigger maximum execution time to exhaust quota/budget
- **DFD Element**: Process (Serverless Function) execution
- **Attack Vector**: Intentionally slow operations, infinite loops
- **Impact**: Budget exhaustion, quota limits, service unavailability
- **STRIDE Category**: Denial of Service
- **Mitigation**: Function timeouts, concurrency limits, budget alerts, input validation
- **NIST Controls**: SC-5, SC-6
- **IEC 62443**: SR 7.2, FR 7
- **Detection**: Function duration monitoring, invocation rate tracking

#### Pattern: API Gateway Quota Exhaustion
- **Threat**: Exhaust API rate limits or quotas
- **DFD Element**: External Entity → Process (API Gateway) quotas
- **Attack Vector**: Excessive API calls, automated scripts
- **Impact**: Legitimate requests blocked, service disruption, budget impact
- **STRIDE Category**: Denial of Service
- **Mitigation**: Rate limiting per user, CAPTCHA, API key management, throttling
- **NIST Controls**: SC-5, AC-7 (Unsuccessful Logon Attempts), IA-4
- **IEC 62443**: SR 7.1, FR 7
- **Detection**: Rate limit hit monitoring, quota usage alerts

### Physical and Environmental DoS

#### Pattern: Power Supply Disruption
- **Threat**: Cut or overwhelm power supply to cause outage
- **DFD Element**: External Entity (Power Supply) → Process (Systems)
- **Attack Vector**: Physical attack, power surge, circuit overload
- **Impact**: System shutdown, data loss, service unavailability
- **STRIDE Category**: Denial of Service
- **Mitigation**: UPS, redundant power, surge protection, physical security, generators
- **NIST Controls**: PE-10 (Emergency Shutoff), PE-11 (Emergency Power), CP-2
- **IEC 62443**: PE-10, PE-11, FR 7
- **Detection**: Power monitoring, UPS alerts, environmental sensors

#### Pattern: Cooling System Failure
- **Threat**: Disable cooling causing thermal shutdown
- **DFD Element**: External Entity (HVAC) → Process (Servers)
- **Attack Vector**: Physical attack, HVAC system compromise, BMS attack
- **Impact**: Thermal shutdown, hardware damage, service outage
- **STRIDE Category**: Denial of Service
- **Mitigation**: Redundant cooling, temperature monitoring, physical security, automatic shutdown
- **NIST Controls**: PE-14 (Temperature and Humidity Controls), PE-15 (Water Damage Protection)
- **IEC 62443**: PE-14, PE-15, FR 7
- **Detection**: Temperature monitoring, HVAC system monitoring

#### Pattern: Cable Cut/Physical Disconnection
- **Threat**: Sever network cables or physical connections
- **DFD Element**: Data Flow (Physical Network) disruption
- **Attack Vector**: Physical access, construction accidents, sabotage
- **Impact**: Network outage, service unavailability, communication loss
- **STRIDE Category**: Denial of Service
- **Mitigation**: Redundant paths, physical security, cable protection, diverse routing
- **NIST Controls**: PE-3 (Physical Access Control), CP-8 (Telecommunications Services)
- **IEC 62443**: PE-3, FR 7, CP-8
- **Detection**: Link monitoring, path redundancy checks

## Cross-Framework Integration

### PASTA Stage 4: Threat Analysis
- Availability threat scenarios by asset
- Single points of failure identification
- Resilience requirement analysis

### PASTA Stage 7: Risk and Impact Analysis
- Business impact of downtime
- Recovery time objectives (RTO)
- Service level agreement (SLA) violations

### IEC 62443 Requirements
- FR 7: Resource Availability (primary)
- SR 7.1: Denial of Service Protection
- SR 7.2: Resource Management
- SR 7.6: Failsafe on Failure

### NIST SP 800-53 Controls
- SC-5: Denial of Service Protection
- SC-6: Resource Availability
- CP-2: Contingency Plan
- SI-13: Predictable Failure Prevention
- AU-4: Audit Storage Capacity

## Detection Strategy

### Traffic Analysis
- Volume monitoring
- Pattern recognition
- Anomaly detection
- Rate limiting enforcement

### Resource Monitoring
- CPU/memory usage
- Disk space
- Network bandwidth
- Connection counts
- Thread/process pools

### Behavioral Analysis
- Request patterns
- User behavior
- Geolocation anomalies
- Device fingerprinting

## Mitigation Hierarchy

### Level 1: Prevent DoS
- Resource limits
- Rate limiting
- Input validation
- Redundancy/scalability
- Network filtering

### Level 2: Detect DoS
- Monitoring and alerting
- Anomaly detection
- Traffic analysis
- Resource tracking

### Level 3: Absorb DoS
- Elastic scaling
- CDN/caching
- Load balancing
- Overprovisioning
- DDoS mitigation services

### Level 4: Respond and Recover
- Incident response
- Failover systems
- Backup services
- Communication plan
- Post-incident analysis
