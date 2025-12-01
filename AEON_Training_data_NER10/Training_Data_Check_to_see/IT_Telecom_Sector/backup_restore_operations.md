# Backup and Restore Operations

## Overview
Backup and restore operations protect critical data and systems through scheduled full, incremental, and differential backups, off-site replication, restore testing, and retention policy enforcement ensuring business continuity, disaster recovery, and regulatory compliance while optimizing storage costs and recovery objectives.

## Operational Procedures

### 1. Backup Strategy Design and Implementation
- **Full Backup Scheduling**: Complete copy of all data typically weekly (Sundays); serves as baseline for incremental/differential backups
- **Incremental Backup Strategy**: Daily backups capture only changes since last backup (full or incremental); minimizes backup time and storage but lengthens restores
- **Differential Backup Approach**: Daily backups capture changes since last full backup; faster restores than incremental but larger storage requirements
- **Continuous Data Protection (CDP)**: Near real-time backup of every change; provides granular point-in-time recovery for mission-critical systems

### 2. Backup Job Configuration
- **Backup Window Scheduling**: Jobs scheduled during low-activity periods (2-6 AM) minimizing performance impact on production systems
- **Resource Throttling**: Network bandwidth and disk I/O limits prevent backup operations from degrading application performance
- **Exclusion Lists**: Temporary files, caches, swap files, and already-backed-up data excluded reducing backup size and duration
- **Pre-Backup Scripts**: Application-consistent backups require database quiesce scripts or VSS (Volume Shadow Copy) snapshots before backup

### 3. Retention Policy Management
- **GFS Rotation (Grandfather-Father-Son)**: Daily (7 days), weekly (4 weeks), monthly (12 months), yearly (7 years) retention tiers balance recoverability and storage costs
- **Compliance-Driven Retention**: HIPAA (6 years), SOX (7 years), GDPR (context-dependent), PCI-DSS (1 year) mandates define minimum retention periods
- **Legal Hold Procedures**: Litigation-related backups exempt from automated deletion; tagged for indefinite preservation pending case resolution
- **Automated Expiration**: Aging backups automatically deleted after retention period; reclaims storage and reduces compliance risk from over-retention

### 4. Off-Site and Cloud Backup Replication
- **Geographic Separation**: Off-site backups stored >100 miles from primary site protecting against regional disasters (hurricanes, earthquakes)
- **3-2-1 Backup Rule**: Three copies of data, two different media types, one off-site copy ensures resilience against diverse failure modes
- **Cloud Storage Tiers**: Hot storage (S3 Standard) for recent backups; cool/cold storage (S3 Glacier) for long-term retention reducing costs
- **Bandwidth Optimization**: WAN acceleration, deduplication, and compression reduce data transmitted to off-site/cloud repositories

### 5. Restore Testing and Validation
- **Scheduled Restore Drills**: Monthly random file restores validate backup integrity and team proficiency; quarterly full system restores test disaster recovery
- **Automated Verification**: Backup software performs post-backup verification reading backup data and comparing checksums to source
- **Test Environment Restores**: Periodic restore of production databases to test/dev environments validates recoverability and provides data for testing
- **Restore Time Tracking**: Actual restore durations documented validating RTO (Recovery Time Objective) targets achievable with current procedures

### 6. Backup Monitoring and Alerting
- **Job Success/Failure Notifications**: Email, SMS, or ticketing system alerts on backup job failures enable rapid investigation and retry
- **Capacity Monitoring**: Backup repository utilization tracked; alerts at 80% capacity trigger expansion planning before storage exhaustion
- **Backup Age Reporting**: Systems without recent successful backup flagged; >48 hours without backup triggers escalation
- **Trend Analysis**: Backup size growth rates forecasted identifying systems requiring retention policy review or increased capacity allocation

### 7. Disaster Recovery Procedures
- **Recovery Point Objective (RPO)**: Maximum acceptable data loss; RPO drives backup frequency (24-hour RPO = daily backups minimum)
- **Recovery Time Objective (RTO)**: Maximum acceptable downtime; RTO determines restore method (tape vs. disk vs. instant recovery)
- **Bare-Metal Recovery**: Complete server restoration from scratch including OS, applications, and data to physical or virtual hardware
- **Disaster Declaration Criteria**: Documented thresholds (data center destruction, sustained outage >4 hours, ransomware encryption) trigger DR plan activation

## System Integration Points

### Backup Software Platforms
- **Agent-Based Backups**: Software agents installed on servers coordinate with backup server scheduling jobs and transferring data
- **Agentless Backups**: VMware/Hyper-V integration uses hypervisor APIs creating VM snapshots without agents; simpler but less granular
- **Database Plugins**: Native integration with Oracle RMAN, SQL Server VSS writer, MySQL/PostgreSQL dumps ensuring transactionally consistent backups
- **API Integration**: Cloud-native applications backed up via API calls (AWS snapshots, Azure backups) rather than file-level copying

### Deduplication and Compression
- **Source-Side Deduplication**: Data deduplicated at source before transmission to backup repository; reduces network bandwidth consumption
- **Target-Side Deduplication**: Backup repository deduplicates data across all clients; achieves higher deduplication ratios (10-50:1 typical)
- **Compression Algorithms**: LZ4 (fast, moderate compression), zstd (balanced), gzip (slower, higher compression) trade performance for space savings
- **Inline vs. Post-Process**: Inline dedup/compression occurs during backup; post-process occurs during idle periods preserving backup window

### Disaster Recovery Orchestration
- **Runbook Automation**: Recovery procedures codified as executable workflows defining server boot order and interdependencies
- **Failover Testing**: DR orchestration platforms enable non-disruptive testing by booting recovered systems in isolated networks
- **Cloud DR**: Disaster recovery to public cloud (AWS, Azure) eliminates secondary datacenter costs; compute resources provisioned only during disaster
- **Recovery Validation**: Post-restore health checks verify application functionality before declaring recovery successful

### Compliance and Reporting
- **Backup Compliance Dashboards**: Real-time view of backup coverage, success rates, and policy violations for management and auditors
- **Audit Trail Logging**: All backup, restore, and deletion operations logged with user identity, timestamp, and outcome for compliance audits
- **Regulatory Reporting**: Automated reports demonstrating retention compliance for PCI-DSS, HIPAA, SOX, and other regulatory frameworks
- **E-Discovery Support**: Legal-hold tagged backups indexed and searchable accelerating e-discovery response during litigation

## Regulatory Compliance

### HIPAA Security Rule (45 CFR 164.308)
- **Backup Requirements**: Administrative safeguard requires "retrievable exact copy" of ePHI created and maintained
- **Disaster Recovery Plan**: Contingency plan with data backup, disaster recovery, and emergency mode operations documented and tested
- **Testing Requirements**: Periodic testing and revision of backup/DR plans required; frequency determined by risk analysis
- **Encryption Requirements**: ePHI backups stored off-site or transported must be encrypted per HIPAA addressable specifications

### SOX (Sarbanes-Oxley Act)
- **Financial Data Retention**: Public companies must retain financial records and backups 7 years minimum
- **IT General Controls (ITGC)**: SOX audits evaluate backup procedures, restore testing, and access controls as foundation of financial data integrity
- **Change Management**: Backup configuration changes require approval, testing, and documentation per SOX ITGC requirements
- **Segregation of Duties**: Backup administrators should not have production data modification rights preventing unauthorized alterations

### GDPR (General Data Protection Regulation)
- **Right to Erasure**: Individual data deletion requests require purging from backups or technical measures preventing restoration
- **Data Minimization**: Backup retention periods should not exceed business necessity; excessive retention violates GDPR principles
- **Cross-Border Transfers**: EU personal data backups replicated outside EU require Standard Contractual Clauses or adequacy decisions
- **Breach Notification**: Backup repository breaches exposing personal data require 72-hour notification to supervisory authorities

### PCI-DSS (Payment Card Industry Data Security Standard)
- **Cardholder Data Retention**: Backups containing CHD subject to same security controls as production environments
- **Encryption Requirements**: Backup media with CHD must be encrypted using strong cryptography (AES-256)
- **Access Controls**: Backup access restricted to authorized personnel with business need-to-know; access logged and monitored
- **Quarterly Reviews**: Backup configurations and retention policies reviewed quarterly ensuring continued PCI-DSS compliance

## Equipment and Vendors

### Backup Software Vendors
- **Veeam Backup & Replication**: Market leader for VMware/Hyper-V backup with instant VM recovery and built-in deduplication
- **Commvault Complete Backup & Recovery**: Enterprise-grade platform supporting physical, virtual, cloud, and SaaS backup/recovery
- **Veritas NetBackup**: Legacy enterprise backup software with comprehensive platform support and cloud integration
- **Rubrik**: Cloud-native backup appliance with instant recovery, automated orchestration, and policy-driven SLA management

### Cloud Backup Services
- **AWS Backup**: Centralized backup service for AWS resources (EC2, RDS, EFS, DynamoDB) with cross-region replication
- **Azure Backup**: Native backup for Azure VMs, SQL databases, and file shares with geo-redundant vault storage
- **Google Cloud Backup**: Managed backup for Compute Engine, Cloud SQL, and GKE persistent volumes
- **Druva Cloud Platform**: Pure SaaS backup eliminating on-premises infrastructure; supports endpoints, servers, and cloud workloads

### Backup Appliances and Storage
- **Dell EMC Data Domain**: Purpose-built backup appliance with high deduplication ratios (10-30x) and cloud-tier integration
- **HPE StoreOnce**: Deduplication appliance with StoreOnce Catalyst protocol supporting major backup software vendors
- **Cohesity DataPlatform**: Converged secondary storage consolidating backup, archive, test/dev, and analytics on single platform
- **ExaGrid**: Scale-out backup storage with unique tiered approach; recent backups on fast landing zone, older backups deduplicated

### Tape Libraries and Archival
- **IBM TS4500 Tape Library**: Enterprise tape library with LTO-9 drives (18TB native, 45TB compressed capacity per cartridge)
- **Quantum Scalar i6000**: Scalable tape library supporting LTO and Oracle T10000 drives for long-term archival
- **Iron Mountain**: Secure off-site tape vaulting service with pickup/delivery and disaster recovery retrieval services
- **LTO Ultrium**: Industry standard tape format; LTO-9 current generation with 30-year archival rating and AES-256 encryption

## Performance Metrics

### Backup Success Metrics
- **Backup Success Rate**: Percentage of scheduled jobs completing successfully; target >98% with investigation of all failures
- **Data Protection Coverage**: Percentage of critical systems with recent valid backups; goal 100% of production systems
- **Backup Window Compliance**: Percentage of jobs completing within allocated backup window; >95% target ensures production readiness
- **First-Attempt Success**: Percentage of jobs succeeding without retry; <90% indicates configuration or capacity issues

### Recovery Metrics
- **Mean Time to Recover (MTTR)**: Average time from restore request to data/system availability; varies by system criticality
- **RTO Compliance**: Percentage of restores meeting defined RTO targets; 100% compliance required for critical systems
- **RPO Compliance**: Maximum data loss measured in recent recovery exercises; should not exceed defined RPO thresholds
- **Restore Test Success Rate**: Percentage of restore tests completing successfully; >95% target with investigation of failures

### Efficiency Metrics
- **Deduplication Ratio**: Logical data size divided by physical storage consumed; typical 10-20:1 for VMs, 50:1+ for file servers
- **Compression Ratio**: Pre-compression size divided by post-compression size; typical 2-5:1 depending on data types
- **Change Rate**: Percentage of data changing daily; drives incremental backup sizes and repository capacity growth
- **Backup Speed**: Throughput in TB/hour; influenced by source disk speed, network bandwidth, deduplication, and compression overhead

### Cost Metrics
- **Cost per GB Protected**: Total backup infrastructure costs divided by total protected capacity; benchmark for efficiency comparison
- **Recovery Cost**: Labor and downtime costs associated with restore operations; justifies investment in faster recovery technologies
- **Compliance Cost**: Incremental costs of extended retention for regulatory compliance; optimized through archival tiers
- **TCO Comparison**: On-premises backup infrastructure TCO vs. cloud backup services factoring CapEx, OpEx, and scalability

---

**Document Control**
- **Version**: 1.0
- **Last Updated**: 2025-11-06
- **Regulatory References**: HIPAA 45 CFR 164.308, SOX ITGC, GDPR Articles 5/17, PCI-DSS v4.0 Requirement 3, ISO 27001 A.12.3
- **Review Cycle**: Annual
