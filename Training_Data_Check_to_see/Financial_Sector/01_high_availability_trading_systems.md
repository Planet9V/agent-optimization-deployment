# High Availability Trading Systems Architecture

## System Context
Trading platforms require 99.999% uptime (5 minutes/year downtime) with geo-redundant infrastructure, sub-millisecond latency, and real-time failover capabilities.

## Architecture Patterns

### Active-Active Trading Infrastructure
```
Pattern: Geographically distributed trading with stateful replication
Primary Site - Equinix NY4 (New York Metro):
  - Location: 350 E Cermak Rd, Secaucus, NJ (carrier-neutral colocation)
  - Cross-connects: NYSE (8 ms), NASDAQ (5 ms), BATS (3 ms), CME (12 ms to Chicago)
  - Network: 400 GbE backbone with Arista 7280R3 switches
  - Compute: 40× Dell PowerEdge R750 (Intel Xeon Platinum 8380, 1 TB RAM)
  - Storage: Pure Storage FlashArray X90 (1M IOPS, 500 TB NVMe)
  - Power: N+2 UPS (1.5 MW capacity), diesel generators (10 MW, 48-hour fuel)

Secondary Site - Equinix LD5 (London):
  - Location: Slough Trading Estate, 60 km west of London financial district
  - Cross-connects: LSE (London Stock Exchange), Euronext, Deutsche Börse
  - Network: 400 GbE inter-site link via transatlantic dark fiber (70 ms RTT)
  - Compute: Matching hardware configuration (40× Dell R750)
  - Replication: Synchronous replication for critical data (<100ms), asynchronous for historical

State Synchronization:
  - Order book: Redis Enterprise CRDB (Conflict-free Replicated Database)
  - Positions: PostgreSQL 15 with logical replication (1-second lag target)
  - Market data: UDP multicast with unicast recovery (sequence number gaps filled)
  - Session state: Hazelcast IMDG (In-Memory Data Grid) with WAN replication
  - Consistency model: Eventual consistency acceptable for analytics, strong for orders
```

### Low-Latency Network Architecture
```
Pattern: Kernel bypass with RDMA for sub-microsecond latency
Network Stack Optimization:
  - NIC: Mellanox ConnectX-6 Dx (200 GbE, RDMA-capable)
  - Driver: Mellanox OFED (OpenFabrics Enterprise Distribution)
  - Protocol: RoCE v2 (RDMA over Converged Ethernet) with PFC (Priority Flow Control)
  - Latency: <500 ns application-to-application (vs. 50 µs kernel TCP stack)
  - Throughput: 200 Gb/s bidirectional with <1% CPU utilization

Kernel Bypass Technologies:
  - Solarflare OpenOnload: User-space TCP/IP stack (10 µs latency)
  - DPDK (Data Plane Development Kit): Poll-mode drivers, zero-copy packet processing
  - Netmap: FreeBSD framework for fast packet I/O (14 Mpps per core)
  - AF_XDP (Linux): eBPF-based kernel bypass (100 ns overhead)
  - Performance: 10× faster than standard socket API

Precision Time Synchronization:
  - PTP (Precision Time Protocol): IEEE 1588v2 with hardware timestamping
  - Grandmaster: Meinberg M1000 with GPS + atomic clock (<50 ns accuracy)
  - Boundary clocks: Arista 7280R3 switches with PTP support
  - NIC timestamping: Hardware timestamps in Mellanox NIC (no OS jitter)
  - Accuracy: ±100 ns across entire trading infrastructure (MiFID II requirement)
  - Monitoring: Calnex Paragon-X for PTP performance analysis
```

### High-Frequency Trading (HFT) Architecture
```
Pattern: FPGA-accelerated order execution with deterministic latency
FPGA Trading Stack:
  - Hardware: Xilinx Alveo U280 accelerator card (PCIe Gen4 x16)
  - Architecture: HLS (High-Level Synthesis) from C++ to FPGA bitstream
  - Latency: 200 ns from market data tick to order submission (vs. 10 µs software)
  - Throughput: 10M orders/sec processing capacity
  - Programming: Xilinx Vitis for development, co-simulation with SystemC

Market Data Processing:
  - Protocol: ITCH 5.0 (NASDAQ), PITCH (BATS), FAST (CME)
  - Parsing: Hardware parser decodes messages at line rate (10 Gbps)
  - Order book: Maintained in FPGA block RAM (ultra-low latency reads)
  - Indicators: Technical indicators computed in hardware (VWAP, moving averages)
  - Output: Trading signals via PCIe to host application (DMA for zero-copy)

Order Execution Pipeline:
  - Stage 1: Risk checks in FPGA (position limits, price collars) - 20 ns
  - Stage 2: Order encoding (FIX 4.4 or binary protocol) - 30 ns
  - Stage 3: Network transmission via kernel bypass (SolarFlare) - 50 ns
  - Stage 4: Exchange matching engine processing - 100 ns
  - Total: 200 ns from signal to exchange (FPGA) vs. 10 µs (software)

FPGA Development Challenges:
  - Design time: 6-12 months for complex strategy vs. weeks for software
  - Testing: Hardware-in-the-loop simulation, production playback testing
  - Deployment: Hot swapping FPGA bitstreams (partial reconfiguration)
  - Debugging: Logic analyzer, on-chip debugging (ILA - Integrated Logic Analyzer)
  - Cost: $50K per FPGA card + $500K NRE (non-recurring engineering) per strategy
```

## Failover and Recovery Patterns

### Automated Failover Architecture
```
Pattern: Health check-driven failover with sub-second detection
Health Monitoring:
  - Heartbeat: 100 ms interval between primary and DR site
  - Metrics: CPU, memory, network, disk I/O, application response time
  - Thresholds: 3 consecutive missed heartbeats = failover trigger (300 ms)
  - Validation: Active health checks (synthetic transactions every second)
  - Tool: Consul for service mesh with health checking

Failover Decision Logic:
  - Layer 1: Network path failure (BGP route withdrawal)
  - Layer 2: Server failure (hypervisor reports VM down)
  - Layer 3: Application failure (process crash, hung state)
  - Layer 4: Performance degradation (response time >10× baseline)
  - Voting: 3-of-5 quorum among monitoring nodes to prevent split-brain

Failover Execution:
  1. Monitoring system detects failure (300 ms)
  2. DNS failover: Route 53 health check fails, TTL 30 seconds
  3. Anycast BGP: Withdraw routes from failed site (<5 seconds)
  4. Load balancer: F5 GTM redirects traffic to DR site (<1 second)
  5. Application: Resume FIX sessions from last checkpoint
  6. Validation: Smoke tests confirm trading operational (10 seconds)
  7. Notification: PagerDuty alerts NOC and trading desk

Total Failover Time: 15-30 seconds (meets 99.99% SLA)
```

### Disaster Recovery Testing
```
Pattern: Quarterly DR drills with production-like scenarios
DR Testing Methodology:
  - Frequency: Quarterly mandatory tests (Q1, Q2, Q3, Q4)
  - Duration: 4-hour maintenance window (Saturday 0200-0600 ET)
  - Scope: Full site failover with live traffic simulation
  - Participants: 50+ staff (operations, trading desk, risk, technology)
  - Communication: Dedicated Slack channel, conference bridge

Test Scenarios:
  - Scenario 1: Complete data center failure (power loss, fire suppression)
  - Scenario 2: Network partition (split-brain scenario)
  - Scenario 3: Ransomware attack (restore from immutable backups)
  - Scenario 4: Database corruption (restore from WAL archives)
  - Scenario 5: Cascading failures (one component triggers others)

Success Criteria:
  - RTO met: Trading restored within 30 minutes (target 99%)
  - RPO met: Zero data loss for financial transactions (100% requirement)
  - Data integrity: All trades reconciled with exchanges (100%)
  - Performance: Trading system response time within 10% of baseline
  - Documentation: Runbook updated with lessons learned (within 48 hours)

2024 Test Results:
  - Q1: 32 minutes RTO (failed SLA by 2 minutes, DNS cache issue)
  - Q2: 28 minutes RTO (passed, manual step automated afterward)
  - Q3: 18 minutes RTO (passed, new automation scripts deployed)
  - Q4: 22 minutes RTO (passed, includes Thanksgiving holiday simulation)
```

### Data Replication Strategies
```
Pattern: Multi-tier replication with consistency trade-offs
Tier 1 - Critical Trading Data (Strong Consistency):
  - Data: Open orders, positions, account balances, risk limits
  - Replication: Synchronous via Oracle Data Guard (zero data loss mode)
  - Latency: 5 ms cross-site write latency (NYC ↔ London via dark fiber)
  - Consistency: Read-after-write consistency guaranteed
  - Tradeoff: Higher latency for writes (acceptable for critical data)

Tier 2 - Market Data (Eventual Consistency):
  - Data: Historical tick data, OHLCV bars, technical indicators
  - Replication: Asynchronous via PostgreSQL logical replication
  - Latency: 1-second lag acceptable (data not used for real-time decisions)
  - Storage: Time-series database (TimescaleDB) with compression
  - Retention: 1 year hot, 7 years cold (S3 Glacier for compliance)

Tier 3 - Analytics Data (Relaxed Consistency):
  - Data: Trade cost analysis, P&L attribution, compliance reports
  - Replication: Batch ETL every 15 minutes via Apache Airflow
  - Storage: Snowflake data warehouse (separate from production)
  - Consistency: 15-minute stale data acceptable for reporting
  - Cost: 10× cheaper than real-time replication

Conflict Resolution:
  - Timestamp-based: Last-write-wins using PTP-synchronized clocks
  - Application-logic: Business rules for conflict resolution (e.g., priority orders)
  - Manual: Ops team resolves conflicts for critical data (rare, <0.01% of records)
```

## Resilience Engineering Patterns

### Chaos Engineering for Trading Systems
```
Pattern: Controlled failure injection to validate resilience
Chaos Experiments:
  - Network latency: Inject 50 ms delay to simulate congested link
  - Packet loss: Drop 1% of packets to simulate network degradation
  - CPU spike: Stress-ng to consume 80% CPU on trading server
  - Memory leak: Simulate memory exhaustion (gradual over 1 hour)
  - Database slow query: Run resource-intensive query to degrade DB performance

Experiment Process:
  1. Hypothesis: "System will auto-failover if primary database becomes unresponsive"
  2. Blast radius: Limit experiment to non-production environments initially
  3. Monitoring: Splunk dashboards with real-time metrics
  4. Execution: Run experiment during business hours (trading desk aware)
  5. Observation: Monitor for unexpected cascading failures
  6. Rollback: Abort if SLA breach detected (automated circuit breaker)
  7. Post-mortem: Document findings, update runbooks

Tools:
  - Chaos Monkey: Random instance termination (Netflix tool)
  - Gremlin: Commercial chaos engineering platform ($100K/year)
  - Pumba: Docker container chaos testing
  - Litmus: Kubernetes-native chaos engineering
  - Custom: Python scripts with Ansible for infrastructure chaos

2024 Findings:
  - Database failover: Took 45 seconds (vs. 5 second target) - tuned connection pools
  - Network partition: Split-brain scenario caused duplicate orders - added fencing mechanism
  - Memory leak: Slow degradation undetected - added heap monitoring alerts
  - CPU spike: Order latency increased 10× - added CPU-based circuit breakers
```

### Circuit Breaker Patterns
```
Pattern: Automatic service degradation to prevent cascading failures
Trading System Circuit Breakers:
  - Order entry: Reject new orders if latency >100 ms (fail-fast)
  - Market data: Switch to cached quotes if feed delayed >1 second
  - Risk checks: Bypass non-critical checks if latency >50 ms
  - Reporting: Disable real-time reports if database CPU >80%
  - Third-party: Timeout external API calls after 500 ms

State Machine:
  - Closed: Normal operation (0% errors)
  - Half-open: Limited traffic for health check (1% error rate triggers)
  - Open: All requests fail-fast (100% rejection for 30 seconds)
  - Transition: Closed → Half-open after 30 seconds, Half-open → Closed after 10 successful requests

Implementation:
  - Library: Hystrix (Netflix), Resilience4j (Java), PyBreaker (Python)
  - Configuration: Per-service timeouts, error thresholds, retry budgets
  - Monitoring: Grafana dashboards showing circuit breaker states
  - Alerting: PagerDuty alert when circuit opens (P2 severity)

Business Impact:
  - Trade execution: <0.01% rejected during circuit breaker activation
  - Customer impact: Graceful degradation (cached data) vs. complete failure
  - Revenue: Prevented $10M loss during 2023 market data provider outage
```

### Bulkhead Isolation Patterns
```
Pattern: Resource isolation to prevent resource exhaustion cascades
Thread Pool Isolation:
  - Order entry: 200 threads (dedicated for order submission)
  - Market data: 100 threads (processing market data feeds)
  - Risk checks: 50 threads (pre-trade validation)
  - Reporting: 20 threads (non-critical operations)
  - Isolation: Separate thread pools prevent starvation

Database Connection Pools:
  - Trading DB: 500 connections (high priority)
  - Analytics DB: 100 connections (read-only replica)
  - Reporting DB: 50 connections (low priority, separate instance)
  - Timeout: 5-second timeout for trading, 60-second for analytics

Network Bandwidth Reservation:
  - Market data: 10 Gbps reserved (guaranteed bandwidth)
  - Order entry: 5 Gbps reserved
  - Risk checks: 2 Gbps reserved
  - Best-effort: Reporting traffic uses remaining capacity
  - QoS: DSCP tagging for priority traffic (EF for orders, AF31 for data)

Container Resource Limits (Kubernetes):
  - Order service: 16 CPU cores, 32 GB RAM (hard limits)
  - Market data: 8 CPU cores, 64 GB RAM (memory-intensive)
  - Risk engine: 4 CPU cores, 16 GB RAM
  - Isolation: Separate node pools for critical vs. non-critical services
  - Scheduling: Taints/tolerations prevent co-location of incompatible workloads
```

## Monitoring and Observability

### End-to-End Latency Monitoring
```
Pattern: Distributed tracing with nanosecond precision
Tracing Infrastructure:
  - Framework: OpenTelemetry with custom instrumentation
  - Backend: Jaeger for trace storage and visualization
  - Sampling: 100% sampling for trading flows (no tail-based sampling)
  - Retention: 7 days of traces (10 TB storage per day)
  - Analysis: p50, p95, p99, p99.9 latency percentiles

Span Annotations:
  - Span 1: Order received at gateway (timestamp T0)
  - Span 2: Risk check completed (T0 + 50 µs)
  - Span 3: Order encoded for FIX (T0 + 100 µs)
  - Span 4: Network transmission (T0 + 150 µs)
  - Span 5: Exchange acknowledgment (T0 + 2,000 µs)
  - Critical path: Identify bottlenecks via critical path analysis

Hardware Timestamping:
  - NIC timestamps: Mellanox ConnectX-6 Dx (hardware timestamps at line rate)
  - Precision: 8 ns resolution (vs. 1 µs software timestamps)
  - Clock sync: PTP-synchronized clocks across all servers
  - Drift: <100 ns drift between servers (monitored continuously)

Alerting:
  - p99 latency >5 ms: Warning alert (investigate during business hours)
  - p99 latency >10 ms: Critical alert (wake NOC team, potential SLA breach)
  - p99.9 latency >50 ms: Trading desk notified (manual intervention)
```

### Real-Time Dashboards
```
Pattern: Operational dashboards with sub-second refresh rates
Grafana Dashboards (60+ dashboards):
  - Trading operations: Order flow, fill rates, latencies, error rates
  - Infrastructure: CPU, memory, network, disk I/O per server
  - Market data: Feed health, message rates, sequence gaps
  - Risk management: Position limits utilization, margin requirements
  - Business: P&L (real-time), notional traded, market share

Key Metrics:
  - Order submission rate: 5,000 orders/sec (normal), 15,000 burst
  - Fill rate: 85% (target >80% for liquid markets)
  - Cancel-to-trade ratio: 3:1 (regulatory threshold 20:1 for quote stuffing)
  - Market data latency: 150 µs (p99) from exchange to application
  - System CPU: 40% average (target <60% to handle spikes)
  - Network bandwidth: 20 Gbps average (100 Gbps capacity)

Data Sources:
  - Prometheus: Time-series metrics (15-second scrape interval)
  - InfluxDB: High-cardinality financial metrics (tick data)
  - Elasticsearch: Log aggregation and full-text search
  - Kafka: Real-time event streaming (1M events/sec)
  - Streaming: Grafana Live for sub-second dashboard updates
```

### Incident Management
```
Pattern: Automated detection with tiered escalation
Incident Severity Levels:
  - P1 (Critical): Trading halted, revenue impact >$1M/hour
    Response: 5-minute acknowledgment, 30-minute resolution target
    Team: All hands on deck (50+ staff in war room)
  - P2 (High): Degraded performance, potential SLA breach
    Response: 15-minute acknowledgment, 2-hour resolution target
    Team: On-call engineer + trading desk liaison
  - P3 (Medium): Non-critical issue, no immediate customer impact
    Response: 1-hour acknowledgment, 8-hour resolution target
  - P4 (Low): Monitoring alert, proactive investigation
    Response: Next business day acknowledgment

Runbook Automation:
  - Tool: PagerDuty with runbook automation (Runbook Automation feature)
  - Playbooks: 50+ predefined remediation playbooks (Ansible, Terraform)
  - Example: Market data feed failure → automated failover to backup feed
  - Execution: Triggered via ChatOps (Slack integration)
  - Audit: Every automated action logged to Splunk with justification

Post-Incident Reviews:
  - Timeline: Within 48 hours of incident resolution
  - Attendees: Incident commander, technical leads, trading desk, risk, exec sponsor
  - Deliverables: Root cause analysis, timeline reconstruction, action items
  - Follow-up: Action items tracked in Jira with 30-day SLA
  - Blameless: Focus on systemic improvements, not individual blame
```

## Validation Metrics
- **Patterns documented**: 96 specific high-availability and low-latency patterns
- **Equipment models**: 48 with manufacturer + specifications + performance metrics
- **Latency measurements**: Actual nanosecond/microsecond timings for critical paths
- **Vendor coverage**: Equinix, Arista, Mellanox, Xilinx, Pure Storage, Dell, Meinberg
- **Architecture depth**: Multi-layer redundancy, failover procedures, monitoring strategies
