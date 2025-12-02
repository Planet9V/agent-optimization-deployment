# Enhancement 1: Prerequisites and Environment Setup

**File:** Enhancement_01_APT_Threat_Intel/PREREQUISITES.md
**Created:** 2025-11-25 15:40:00 UTC
**Version:** v1.0.0
**Purpose:** Comprehensive checklist and verification steps for Enhancement 1 execution
**Status:** ACTIVE

---

## Overview

This document outlines all prerequisites, environment requirements, and verification steps needed before executing Enhancement 1: APT Threat Intelligence Ingestion. **All items must be verified before proceeding with TASKMASTER execution.**

---

## Required Data Files

### Primary Training Data Files (31 Total)

**Location:** `/home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/`

#### APT Group Files (13 Files)
1. `01_APT_Volt_Typhoon_IoCs.md` - China state-sponsored, critical infrastructure targeting
2. `02_APT_APT28_Fancy_Bear_IoCs.md` - Russia GRU Unit 26165, railway attacks
3. `03_APT_Sandworm_IoCs.md` - Russia GRU, destructive attacks
4. `04_APT_APT41_IoCs.md` - China dual-purpose (espionage + financial crime)
5. `05_APT_Lazarus_Group_IoCs.md` - North Korea, financial cyber operations
6. `08_APT_Salt_Typhoon_IoCs.md` - China state-sponsored
7. `09_APT_Turla_IoCs.md` - Russia FSB, espionage operations
8. `24_APT_FIN7_Carbanak_IoCs.md` - Financial cybercrime group
9. `25_APT_OceanLotus_APT32_IoCs.md` - Vietnam state-sponsored

#### Nation-State Overview Files (3 Files)
10. `01_Nation_State_APT_China.md` - Chinese APT landscape
11. `02_Nation_State_APT_Russia.md` - Russian APT landscape
12. `03_Nation_State_APT_Iran_North_Korea.md` - Iran and North Korea APT landscape

#### Malware/Ransomware Files (9 Files)
13. `07_Malware_LockBit_Ransomware_IoCs.md` - Ransomware-as-a-Service
14. `10_Malware_Emotet_Botnet_IoCs.md` - Botnet and malware distribution
15. `11_Malware_TrickBot_IoCs.md` - Banking trojan and botnet
16. `12_Malware_Qakbot_IoCs.md` - Banking trojan
17. `13_IcedID_BokBot_IoCs.md` - Banking malware
18. `14_Cobalt_Strike_Abuse_IoCs.md` - Post-exploitation framework abuse
19. `26_Malware_BlackBasta_Ransomware_IoCs.md` - Ransomware group
20. `27_Malware_Royal_Ransomware_IoCs.md` - Ransomware group
21. `28_Malware_Cuba_Ransomware_IoCs.md` - Ransomware group

#### Sector-Specific Threat Files (6 Files)
22. `15_Sector_Energy_Power_Grid_IoCs.md` - Energy sector targeting
23. `16_Sector_Maritime_Port_Systems_IoCs.md` - Maritime sector targeting
24. `17_Sector_Aviation_ATC_IoCs.md` - Aviation sector targeting
25. `18_Sector_Healthcare_Hospital_IoCs.md` - Healthcare sector targeting
26. `19_Sector_Financial_Banking_IoCs.md` - Financial sector targeting
27. `29_Sector_Telecommunications_5G_IoCs.md` - Telecom sector targeting
28. `30_Sector_Defense_Industrial_Base_IoCs.md` - Defense sector targeting
29. `06_Sector_Transportation_Railway_IoCs.md` - Railway sector targeting

#### Comprehensive Threat Intelligence (2 Files)
30. `31_Comprehensive_APT_Infrastructure_Atlas.md` - APT infrastructure analysis
31. `04_STIX_Malware_Infrastructure.md` - STIX-formatted threat intelligence

### Verification Commands

```bash
# Verify all 31 files exist
cd /home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/

# Count APT files
ls -1 *APT_*.md | wc -l
# Expected output: 9

# Count Malware files
ls -1 *Malware_*.md | wc -l
# Expected output: 9

# Count Sector files
ls -1 *Sector_*.md | wc -l
# Expected output: 9

# Count Nation State files
ls -1 *Nation_State_*.md | wc -l
# Expected output: 3

# Count Comprehensive files
ls -1 *Comprehensive_*.md *STIX_*.md | wc -l
# Expected output: 2

# Total count
ls -1 *APT_*.md *Malware_*.md *Sector_*.md *Nation_State_*.md *Comprehensive_*.md *STIX_Malware_Infrastructure.md 2>/dev/null | wc -l
# Expected output: 31
```

### File Format Validation

**Expected Tag Structure** (XML-style annotations):
```markdown
<INDICATOR>203.78.129.45</INDICATOR>
<THREAT_ACTOR>Volt Typhoon</THREAT_ACTOR>
<CAMPAIGN>Living Off The Land</CAMPAIGN>
<VULNERABILITY>CVE-2024-XXXX</VULNERABILITY>
<MALWARE>WhisperGate</MALWARE>
```

**Sample Validation Command:**
```bash
# Count INDICATOR tags in sample file
grep -o "<INDICATOR>" 01_APT_Volt_Typhoon_IoCs.md | wc -l
# Expected output: 150+ (as stated in file)

# Verify tag consistency across 3 samples
for file in 01_APT_Volt_Typhoon_IoCs.md 02_APT_APT28_Fancy_Bear_IoCs.md 07_Malware_LockBit_Ransomware_IoCs.md; do
  echo "File: $file"
  echo "  INDICATOR tags: $(grep -o "<INDICATOR>" $file | wc -l)"
  echo "  THREAT_ACTOR tags: $(grep -o "<THREAT_ACTOR>" $file | wc -l)"
  echo "  CAMPAIGN tags: $(grep -o "<CAMPAIGN>" $file | wc -l)"
done
```

---

## Neo4j Database Requirements

### Installation Verification

```bash
# Check Neo4j is installed
which neo4j
# Expected: /usr/bin/neo4j or /usr/local/bin/neo4j or path to Neo4j executable

# Check Neo4j version
neo4j --version
# Expected: Neo4j 4.x or 5.x (Community or Enterprise)

# Check if Neo4j is running
neo4j status
# Expected: "Neo4j is running"

# Alternative: Check Docker container (if using Docker)
docker ps | grep neo4j
# Expected: Container status "Up X minutes/hours"
```

### Connection Configuration

**Environment File:** `/home/jim/2_OXOT_Projects_Dev/4_AEON_DT_CyberDTc3_2025_11_25/.env`

**Required Variables:**
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password_here
NEO4J_DATABASE=neo4j
```

**Verification Command:**
```bash
# Check .env file exists and has required variables
grep -E "NEO4J_(URI|USERNAME|PASSWORD|DATABASE)" /home/jim/2_OXOT_Projects_Dev/4_AEON_DT_CyberDTc3_2025_11_25/.env
# Expected output: 4 lines with NEO4J_ variables
```

**Test Connection (Python):**
```python
# Save as test_neo4j_connection.py
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    result = session.run("RETURN 'Connection successful!' AS message")
    print(result.single()["message"])

driver.close()
```

**Run Test:**
```bash
cd /home/jim/2_OXOT_Projects_Dev/4_AEON_DT_CyberDTc3_2025_11_25/
python test_neo4j_connection.py
# Expected output: "Connection successful!"
```

### Existing Node Verification

**Required Pre-Existing Nodes:**

#### 1. Sector Nodes (16 Expected)

```cypher
MATCH (s:Sector)
RETURN s.name
ORDER BY s.name;
```

**Expected Sectors:**
1. CHEMICAL
2. COMMERCIAL_FACILITIES
3. COMMUNICATIONS
4. CRITICAL_MANUFACTURING
5. DAMS
6. DEFENSE_INDUSTRIAL_BASE
7. EMERGENCY_SERVICES
8. ENERGY
9. FINANCIAL_SERVICES
10. FOOD_AND_AGRICULTURE
11. GOVERNMENT_FACILITIES
12. HEALTHCARE
13. INFORMATION_TECHNOLOGY
14. NUCLEAR
15. TRANSPORTATION
16. WATER_AND_WASTEWATER

**Verification Query:**
```cypher
MATCH (s:Sector)
RETURN COUNT(s) AS sector_count;
// Expected: 16
```

**Spot Check (verify 3 sectors exist):**
```cypher
MATCH (s:Sector)
WHERE s.name IN ['DAMS', 'CRITICAL_MANUFACTURING', 'TRANSPORTATION']
RETURN s.name;
// Expected: 3 rows returned
```

#### 2. CVE Nodes (~316,552 Expected)

```cypher
MATCH (cve:CVE)
RETURN COUNT(cve) AS cve_count;
// Expected: ~316,552 (approximate, ±1,000 acceptable)
```

**Sample CVE Verification:**
```cypher
// Verify specific CVEs mentioned in APT files exist
MATCH (cve:CVE)
WHERE cve.id IN ['CVE-2022-38028', 'CVE-2023-1234', 'CVE-2024-0001']
RETURN cve.id;
// Expected: At least CVE-2022-38028 (GooseEgg exploit)
```

**CVE ID Format Check:**
```cypher
MATCH (cve:CVE)
RETURN cve.id
LIMIT 5;
// Expected format: CVE-YYYY-NNNNN (e.g., CVE-2022-38028)
```

#### 3. MITRE ATT&CK Technique Nodes (~691 Expected)

```cypher
MATCH (mt:MITRETechnique)
RETURN COUNT(mt) AS technique_count;
// Expected: ~691 (approximate, ±50 acceptable)
```

**Sample MITRE Technique Verification:**
```cypher
// Verify common techniques exist
MATCH (mt:MITRETechnique)
WHERE mt.technique_id IN ['T1053.005', 'T1059.001', 'T1078', 'T1486']
RETURN mt.technique_id, mt.name;
// Expected: Scheduled Task/Job: Scheduled Task, PowerShell, Valid Accounts, Data Encrypted for Impact
```

**MITRE Technique ID Format Check:**
```cypher
MATCH (mt:MITRETechnique)
RETURN mt.technique_id, mt.name
LIMIT 5;
// Expected format: T#### or T####.### (e.g., T1053.005)
```

### Database Performance Baseline

**Check Current Database Size:**
```cypher
CALL apoc.meta.stats()
YIELD nodeCount, relCount, labelCount, propertyKeyCount
RETURN nodeCount, relCount, labelCount, propertyKeyCount;
```

**Expected Pre-Enhancement Baseline:**
- Node Count: ~317,260 (16 Sectors + 316,552 CVEs + 691 MITRE + other)
- Relationship Count: Variable (existing relationships)
- Label Count: ~5 (Sector, CVE, MITRETechnique, + others)
- Property Key Count: Variable

**Check Available Memory:**
```cypher
CALL dbms.queryJmx("java.lang:type=Memory")
YIELD attributes
RETURN attributes.HeapMemoryUsage.value.used AS used_memory,
       attributes.HeapMemoryUsage.value.max AS max_memory;
```

**Expected:** At least 2GB heap memory available for bulk inserts

---

## Python Environment Requirements

### Required Python Version
```bash
python --version
# Expected: Python 3.8+ (3.9, 3.10, 3.11 recommended)
```

### Required Python Libraries

**Install Command:**
```bash
pip install neo4j python-dotenv
```

**Verify Installation:**
```bash
pip list | grep neo4j
# Expected: neo4j (version 5.x)

pip list | grep python-dotenv
# Expected: python-dotenv (version 1.x)
```

**Library Version Check (Python):**
```python
import neo4j
import dotenv

print(f"neo4j version: {neo4j.__version__}")
print(f"python-dotenv version: {dotenv.__version__}")
```

### Optional Libraries (for validation and reporting)
```bash
pip install pandas matplotlib networkx
```

---

## File System Requirements

### Directory Structure

**Create Enhancement 1 Directory:**
```bash
mkdir -p /home/jim/2_OXOT_Projects_Dev/4_AEON_DT_CyberDTc3_2025_11_25/Enhancement_01_APT_Threat_Intel/outputs
mkdir -p /home/jim/2_OXOT_Projects_Dev/4_AEON_DT_CyberDTc3_2025_11_25/Enhancement_01_APT_Threat_Intel/logs
mkdir -p /home/jim/2_OXOT_Projects_Dev/4_AEON_DT_CyberDTc3_2025_11_25/Enhancement_01_APT_Threat_Intel/visualizations
```

**Verify Directory Structure:**
```bash
ls -la /home/jim/2_OXOT_Projects_Dev/4_AEON_DT_CyberDTc3_2025_11_25/Enhancement_01_APT_Threat_Intel/
# Expected output: README.md, TASKMASTER_APT_INGESTION_v1.0.md, blotter.md, PREREQUISITES.md, DATA_SOURCES.md, outputs/, logs/, visualizations/
```

### Disk Space Requirements

**Check Available Disk Space:**
```bash
df -h /home/jim/2_OXOT_Projects_Dev/
# Expected: At least 5GB free space
```

**Space Breakdown:**
- Training data files: ~50MB (31 markdown files)
- Neo4j database growth: ~500MB (5,000-8,000 nodes + 15,000-25,000 relationships)
- Output files (JSON, reports): ~100MB
- Visualizations: ~50MB
- Logs: ~10MB
- **Total Required:** ~710MB (minimum), **5GB recommended for headroom**

---

## Network Requirements

### Neo4j Connection
- **Local:** bolt://localhost:7687 (default)
- **Remote:** Ensure firewall allows connections to Neo4j port 7687

**Test Network Connectivity:**
```bash
# For local Neo4j
telnet localhost 7687
# Expected: Connection established

# For remote Neo4j
telnet <remote_host> 7687
# Expected: Connection established
```

### Internet Access (Optional)
- **Not required** for core ingestion (all data is local)
- **Required** for optional threat intel validation against external APIs (VirusTotal, AlienVault OTX)

---

## Validation Checklist

### Pre-Execution Checklist

**Data Files:**
- [ ] All 31 APT/Malware files exist in `Cybersecurity_Training/` directory
- [ ] Sample file validation passed (3 files checked for tag consistency)
- [ ] Estimated indicator count: 5,000-10,000 tags

**Neo4j Database:**
- [ ] Neo4j is running (status: Up)
- [ ] Connection test passed (Python script returned "Connection successful!")
- [ ] Sector nodes verified: 16 present
- [ ] CVE nodes verified: ~316,552 present (±1,000 acceptable)
- [ ] MITRE Technique nodes verified: ~691 present (±50 acceptable)
- [ ] Database has >2GB heap memory available

**Python Environment:**
- [ ] Python version: 3.8+ installed
- [ ] neo4j library installed (version 5.x)
- [ ] python-dotenv library installed
- [ ] .env file configured with NEO4J_* variables

**File System:**
- [ ] Enhancement_01 directory created
- [ ] outputs/ subdirectory exists
- [ ] logs/ subdirectory exists
- [ ] visualizations/ subdirectory exists
- [ ] Disk space: >5GB available

**Network:**
- [ ] Neo4j connection tested (telnet to port 7687 succeeded)

**Documentation:**
- [ ] README.md reviewed
- [ ] TASKMASTER_APT_INGESTION_v1.0.md reviewed
- [ ] blotter.md ready for progress tracking
- [ ] PREREQUISITES.md (this file) completed
- [ ] DATA_SOURCES.md reviewed (APA citations)

**ALL CHECKBOXES MUST BE CHECKED BEFORE PROCEEDING TO EXECUTION**

---

## Common Issues and Resolutions

### Issue 1: Neo4j Connection Refused
**Symptoms:** `ConnectionRefusedError: [Errno 111] Connection refused`

**Resolution:**
1. Check Neo4j status: `neo4j status`
2. If stopped, start Neo4j: `neo4j start`
3. Verify port 7687 is listening: `netstat -tulnp | grep 7687`
4. Check firewall rules: `sudo ufw status`

### Issue 2: Authentication Failed
**Symptoms:** `AuthError: The client is unauthorized due to authentication failure.`

**Resolution:**
1. Verify Neo4j credentials: `grep NEO4J_ .env`
2. Reset Neo4j password: `neo4j-admin set-initial-password <new_password>`
3. Update .env file with new password
4. Re-test connection

### Issue 3: Missing Training Data Files
**Symptoms:** File count < 31, file not found errors

**Resolution:**
1. Verify training data path: `ls /home/jim/2_OXOT_Projects_Dev/AEON_Training_data_NER10/Training_Data_Check_to_see/Cybersecurity_Training/`
2. Check file permissions: `ls -la` (should be readable)
3. If files are missing, restore from backup or re-download training data

### Issue 4: Insufficient Disk Space
**Symptoms:** `OSError: [Errno 28] No space left on device`

**Resolution:**
1. Check disk space: `df -h`
2. Clean up temporary files: `rm -rf /tmp/*`
3. Remove old Neo4j logs: `rm /var/log/neo4j/*.log.1`
4. Expand disk if necessary

### Issue 5: Python Library Not Found
**Symptoms:** `ModuleNotFoundError: No module named 'neo4j'`

**Resolution:**
1. Verify Python version: `python --version`
2. Install missing library: `pip install neo4j`
3. If using virtual environment, activate it: `source venv/bin/activate`
4. Re-check installation: `pip list | grep neo4j`

### Issue 6: Existing Nodes Missing
**Symptoms:** Sector/CVE/MITRE nodes not found in database

**Resolution:**
1. Verify database name: `grep NEO4J_DATABASE .env`
2. Check if connected to correct database
3. Run node count queries (see Existing Node Verification section)
4. If nodes are missing, restore from database backup or re-ingest prerequisite data

---

## Emergency Rollback Plan

**If Enhancement 1 needs to be rolled back:**

### Step 1: Backup Current State
```bash
# Create timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup Neo4j database
neo4j-admin dump --database=neo4j --to=/home/jim/backups/neo4j_pre_enhancement1_${TIMESTAMP}.dump
```

### Step 2: Delete Enhancement 1 Nodes
```cypher
// Delete all nodes created by Enhancement 1 (identified by source_files property)
MATCH (n)
WHERE n.source_files IS NOT NULL
  AND ANY(f IN n.source_files WHERE f CONTAINS 'APT' OR f CONTAINS 'Malware' OR f CONTAINS 'Sector' OR f CONTAINS 'Nation_State' OR f CONTAINS 'Comprehensive' OR f CONTAINS 'STIX')
DETACH DELETE n;
```

### Step 3: Verify Rollback
```cypher
// Verify ThreatActor nodes deleted
MATCH (ta:ThreatActor) RETURN COUNT(ta); // Expected: 0

// Verify IoC nodes deleted
MATCH (ioc:IoC) RETURN COUNT(ioc); // Expected: 0

// Verify Campaign nodes deleted
MATCH (c:Campaign) RETURN COUNT(c); // Expected: 0

// Verify Sector nodes still exist
MATCH (s:Sector) RETURN COUNT(s); // Expected: 16 (unchanged)

// Verify CVE nodes still exist
MATCH (cve:CVE) RETURN COUNT(cve); // Expected: ~316,552 (unchanged)
```

### Step 4: Restore from Backup (if needed)
```bash
# Stop Neo4j
neo4j stop

# Restore from backup dump
neo4j-admin load --from=/home/jim/backups/neo4j_pre_enhancement1_${TIMESTAMP}.dump --database=neo4j --force

# Start Neo4j
neo4j start
```

---

## Next Steps After Verification

**Once ALL prerequisites are verified:**

1. **Update blotter.md**: Mark "Setup" phase as COMPLETED
2. **Begin Phase 1**: Execute File Discovery Agent prompt from TASKMASTER
3. **Track Progress**: Update blotter.md after each agent execution
4. **Monitor Performance**: Log execution times and metrics

**Do not proceed to execution until ALL checklist items are checked.**

---

## References

### Neo4j Documentation
- Installation Guide: https://neo4j.com/docs/operations-manual/current/installation/
- Python Driver: https://neo4j.com/docs/python-manual/current/
- Cypher Query Language: https://neo4j.com/docs/cypher-manual/current/

### Python Libraries
- neo4j: https://pypi.org/project/neo4j/
- python-dotenv: https://pypi.org/project/python-dotenv/

### AEON Digital Twin Documentation
- See `README.md` for Enhancement 1 overview
- See `TASKMASTER_APT_INGESTION_v1.0.md` for execution plan
- See `DATA_SOURCES.md` for training data citations

---

**Document End**
**Total Lines:** ~550 lines
**Next File:** DATA_SOURCES.md
