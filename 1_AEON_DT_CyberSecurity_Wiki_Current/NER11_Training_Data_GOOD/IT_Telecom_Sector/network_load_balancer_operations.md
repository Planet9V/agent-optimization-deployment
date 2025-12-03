# Network Load Balancer Operations

## Overview
Network load balancers distribute traffic across multiple servers or application instances using Layer 4 (TCP/UDP) or Layer 7 (HTTP/HTTPS) routing algorithms, providing high availability, horizontal scalability, and automated failover while maintaining session persistence and performing health checks to ensure optimal application performance.

## Operational Procedures

### 1. Server Pool Configuration and Management
- **Pool Member Definition**: Backend servers added to pools with IP address, port number, and weight (relative capacity) specifications
- **Weight-Based Distribution**: Servers assigned weights (1-100) influencing traffic distribution; higher-capacity servers receive proportionally more connections
- **Priority Groups**: Servers organized into priority tiers; lower-priority members activated only when higher-priority members unavailable or overloaded
- **Drain Mode Operation**: Graceful removal of servers from pool; existing connections maintained while new connections directed to remaining pool members

### 2. Health Check Configuration
- **Active Health Probes**: Load balancer sends periodic health check requests (HTTP GET, TCP connect, ICMP ping) to verify server availability
- **Passive Health Monitoring**: Load balancer observes real traffic responses; servers returning errors automatically removed from rotation
- **Health Check Intervals**: Probe frequency (5-30 seconds) balanced against detection speed and backend server load
- **Failure Thresholds**: Consecutive failed health checks (typically 3-5) required before marking server unhealthy to prevent flapping

### 3. Load Balancing Algorithm Selection
- **Round Robin**: Equal distribution of new connections across all healthy pool members; simple and effective for homogeneous servers
- **Least Connections**: New connections directed to server with fewest active connections; optimal for long-lived connections with varying duration
- **Weighted Round Robin**: Round robin modified by server weight; allows heterogeneous server capacities to be efficiently utilized
- **Source IP Hash**: Client IP address hashed to consistently select same backend server; provides implicit session persistence

### 4. Session Persistence (Sticky Sessions)
- **Source IP Persistence**: Client source IP mapped to specific backend server; all connections from client directed to same server for session duration
- **Cookie-Based Persistence**: Load balancer injects cookie with server identifier; subsequent requests with cookie routed to designated server
- **SSL Session ID Persistence**: SSL session ID tracked; requests within same SSL session directed to server handling initial handshake
- **Persistence Timeout**: Session affinity expires after inactivity period (typically 5-30 minutes) allowing rebalancing after session completion

### 5. SSL/TLS Offloading and Encryption
- **SSL Termination**: Load balancer decrypts incoming HTTPS traffic, inspects requests, and forwards unencrypted HTTP to backend servers
- **End-to-End Encryption**: Load balancer re-encrypts traffic before sending to backend servers maintaining encryption throughout request path
- **Certificate Management**: Wildcard or SAN certificates installed on load balancer covering multiple domains/subdomains with centralized renewal
- **Perfect Forward Secrecy (PFS)**: Ephemeral key exchange (ECDHE, DHE) ensures past session keys cannot be compromised if server certificate leaked

### 6. Failover and High Availability
- **Active-Passive HA Pairs**: Two load balancers configured; passive unit monitors active via heartbeat and assumes virtual IP on failure
- **Active-Active Clusters**: Multiple load balancers simultaneously process traffic; ECMP (Equal-Cost Multi-Path) or DNS round robin distributes clients
- **Stateful Failover**: Connection state synchronized between HA pairs; existing connections maintained during failover with zero packet loss
- **Geographic Redundancy**: Load balancers deployed across multiple datacenters with global load balancing (GSLB) distributing traffic by geography

### 7. Traffic Shaping and Rate Limiting
- **Connection Rate Limiting**: Maximum new connections per second per client IP prevents abuse and DoS attacks
- **Bandwidth Throttling**: Per-client or per-pool bandwidth limits prevent individual users from monopolizing capacity
- **Request Rate Limiting**: HTTP request rate limits (requests/second) protect backend applications from overload
- **Priority Queuing**: High-priority traffic (API calls, authenticated users) receives preferential treatment over low-priority traffic (web crawlers)

## System Integration Points

### Application Delivery Controllers (ADC)
- **Layer 7 Content Switching**: Inspects HTTP headers, URLs, cookies routing requests to specialized server pools based on content type
- **Compression Offloading**: Gzip compression performed at load balancer reducing bandwidth consumption and backend server CPU utilization
- **Caching**: Static content (images, CSS, JavaScript) cached at load balancer reducing backend server load and improving response times
- **Web Application Firewall (WAF)**: Integrated WAF inspects HTTP traffic blocking SQL injection, XSS, and other application-layer attacks

### Auto-Scaling Integration
- **Cloud Auto-Scaling Groups**: AWS Auto Scaling, Azure VMSS, GCP Instance Groups dynamically add/remove backend servers based on load
- **API-Driven Pool Updates**: Load balancer APIs enable orchestration systems to programmatically add newly launched instances to pools
- **Health Check Integration**: Failed health checks trigger auto-scaling scale-out events; sustained low load triggers scale-in events
- **Metrics-Based Scaling**: CloudWatch, Azure Monitor, Stackdriver metrics (CPU, memory, request rate) trigger scaling decisions

### DNS and Global Load Balancing
- **DNS-Based GSLB**: Multi-datacenter deployments use DNS to direct clients to geographically nearest or least-loaded datacenter
- **Health-Aware DNS**: Unhealthy datacenters automatically removed from DNS responses; TTL values balanced against failover speed
- **Latency-Based Routing**: DNS returns IP of datacenter with lowest latency for requesting client's geographic location
- **Weighted DNS**: Traffic percentage allocated to different datacenters enabling gradual rollouts and A/B testing

### Monitoring and Observability
- **Metrics Collection**: Connection rates, request rates, response times, error rates, and pool member health collected and graphed
- **Log Aggregation**: Access logs streamed to centralized logging systems (Splunk, ELK, Datadog) for analysis and troubleshooting
- **Distributed Tracing**: Request IDs propagated through load balancer to backend services enabling end-to-end transaction tracing
- **Alerting**: Threshold-based alerts notify operations team of health check failures, performance degradation, or capacity exhaustion

## Regulatory Compliance

### PCI-DSS Compliance
- **Network Segmentation**: Load balancers positioned at DMZ boundary isolating cardholder data environment from internet
- **TLS 1.2+ Required**: PCI-DSS 3.2.1+ prohibits TLS 1.0/1.1; load balancers configured to negotiate only TLS 1.2 and TLS 1.3
- **Certificate Management**: Valid certificates from trusted CAs required; expired certificates flagged in quarterly vulnerability scans
- **Access Controls**: Administrative access to load balancer configuration restricted to authorized personnel with MFA enforcement

### HIPAA Security Rule
- **Encryption in Transit**: All PHI (Protected Health Information) encrypted using TLS during transmission through load balancer
- **Audit Logging**: Access logs retained per HIPAA record retention requirements (6 years); administrative changes logged for audit trail
- **Business Associate Agreements**: Cloud load balancer providers (AWS, Azure) execute BAAs accepting HIPAA compliance responsibility
- **Security Controls**: Load balancers configured per NIST 800-53 security controls for moderate/high impact systems

### GDPR Data Protection
- **Data Residency**: Geographic routing ensures European users' traffic processed within EU datacenters maintaining data residency compliance
- **Log Retention Limits**: Access logs containing PII retained only for legitimate operational purposes then deleted per GDPR Article 5
- **Data Minimization**: Logging configured to omit unnecessary PII (full IP addresses masked/truncated, user-agent strings anonymized)
- **Right to Erasure**: Processes established to purge individual's data from load balancer logs upon GDPR erasure request

### FedRAMP Authorization
- **Continuous Monitoring**: Load balancer security configurations monitored for drift from authorized baseline; deviations remediated
- **Vulnerability Management**: Load balancer software patched per FedRAMP timelines (30 days high, 90 days moderate) after vendor release
- **Incident Response**: Load balancer logs integrated with SIEM for incident detection; playbooks define response procedures
- **Authorization Boundary**: Load balancers documented in system security plan; configuration baselines maintained in version control

## Equipment and Vendors

### Hardware Load Balancers
- **F5 BIG-IP**: Market-leading ADC with extensive Layer 7 features, iRules scripting, and comprehensive protocol support
- **Citrix ADC (formerly NetScaler)**: Enterprise ADC with advanced caching, compression, and AppFirewall WAF capabilities
- **A10 Networks Thunder ADX**: High-performance ADC with DDoS protection and SSL visibility features
- **Kemp LoadMaster**: Cost-effective load balancer targeting SMB and mid-market with perpetual licensing model

### Software/Virtual Load Balancers
- **HAProxy**: Open-source Layer 4/7 load balancer with high performance and flexible configuration; widely deployed
- **NGINX Plus**: Commercial support and advanced features for NGINX open-source load balancer; includes dynamic configuration API
- **Envoy Proxy**: Cloud-native proxy from Lyft; designed for microservices architectures with advanced observability
- **Traefik**: Modern load balancer and reverse proxy with automatic service discovery and native Kubernetes integration

### Cloud-Native Load Balancers
- **AWS Elastic Load Balancing**: Application Load Balancer (Layer 7), Network Load Balancer (Layer 4), Gateway Load Balancer (Layer 3)
- **Azure Load Balancer**: Layer 4 load balancer with high availability zones; Application Gateway provides Layer 7 capabilities
- **Google Cloud Load Balancing**: Global HTTP(S) Load Balancer spans regions; TCP/UDP and SSL Proxy load balancers for non-HTTP
- **DigitalOcean Load Balancers**: Simple regional Layer 4 load balancers integrated with Droplet scaling groups

### Global Server Load Balancing (GSLB)
- **F5 BIG-IP DNS**: Intelligent DNS-based GSLB with health-aware resolution and topology-based routing
- **Citrix GSLB**: Integrated with ADC for multi-datacenter traffic steering based on health, load, and geographic proximity
- **AWS Route 53**: DNS service with health checks, failover routing policies, and latency-based routing
- **Cloudflare Load Balancing**: Global load balancing with health checks, geographic steering, and integrated DDoS protection

## Performance Metrics

### Throughput and Capacity
- **Requests per Second**: Layer 7 load balancers handle 10K-500K+ HTTP requests/second depending on hardware/software
- **Concurrent Connections**: Typical hardware load balancers support 1-10 million concurrent connections
- **SSL TPS**: New SSL/TLS handshakes per second; modern appliances achieve 10K-100K TPS with hardware acceleration
- **Throughput (Gbps)**: Layer 4 load balancers achieve 10-100+ Gbps throughput for high-bandwidth applications

### Latency Metrics
- **Processing Latency**: Time load balancer adds to request path; typical <1 ms for Layer 4, 1-5 ms for Layer 7
- **Connection Time**: Time to establish connection to backend server; target <10 ms for local backends
- **Time to First Byte (TTFB)**: Client perspective latency from request send to first response byte; target <100 ms
- **End-to-End Response Time**: Total request/response cycle time; monitored to detect backend performance issues

### Availability and Reliability
- **Load Balancer Uptime**: Target 99.99%+ availability (max 52 minutes downtime annually)
- **Failover Time**: Active-passive failover typically <2 seconds; active-active clusters provide zero-downtime failover
- **Health Check Accuracy**: False positive rate <1% prevents unnecessary server removals; false negative rate <0.1% ensures bad servers quickly removed
- **Session Persistence Success Rate**: >99.9% of persisted sessions correctly routed to designated backend server

### Operational Metrics
- **Configuration Changes**: Number and frequency of pool changes, algorithm adjustments, and policy updates tracked for audit
- **Certificate Expiration**: Certificates expiring within 30 days flagged for renewal preventing service disruptions
- **Error Rate (4xx/5xx)**: Backend server errors monitored; sustained increases indicate application problems requiring investigation
- **Pool Member Flapping**: Servers transitioning between healthy/unhealthy states indicate health check tuning or server stability issues

---

**Document Control**
- **Version**: 1.0
- **Last Updated**: 2025-11-06
- **Regulatory References**: PCI-DSS v4.0, HIPAA Security Rule, GDPR, FedRAMP, NIST 800-53, SOC 2 Type II
- **Review Cycle**: Quarterly
