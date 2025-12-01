#!/usr/bin/env python3
"""
Wave 9 Hardware Assets: PhysicalServer, Workstation, MobileDevice, NetworkDevice, StorageArray, PeripheralDevice
Target: 1,500 nodes with complete verification
"""

import logging
import json
from datetime import datetime
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Wave9HardwareExecutor:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j@openspg"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.log_file = "/home/jim/2_OXOT_Projects_Dev/openspg-official_neo4j/logs/wave_9_hardware.jsonl"

    def log_operation(self, operation: str, details: dict):
        log_entry = {"timestamp": datetime.utcnow().isoformat(), "operation": operation, "details": details}
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        logging.info(f"{operation}: {details}")

    def create_physical_servers(self) -> int:
        """Create 400 PhysicalServer nodes in 8 batches of 50"""
        with self.driver.session() as session:
            # Batch 1: Domain Controllers (50)
            session.run("""
            UNWIND range(1, 50) AS idx
            CREATE (s:PhysicalServer {
              serverID: "SRV-DC-" + toString(1000 + idx),
              assetTag: "AT-DC-" + toString(1000 + idx),
              hostname: "dc" + toString(idx) + ".corp.example.com",
              domain: "corp.example.com",
              serialNumber: "SN-DC-" + toString(10000 + idx),
              manufacturer: CASE idx % 3 WHEN 0 THEN "Dell" WHEN 1 THEN "HP" ELSE "Lenovo" END,
              model: "PowerEdge R750",
              formFactor: "rack_mount",
              rackUnit: 2,
              weight: 25.5,
              cpu_model: "Intel Xeon Gold 6338",
              cpu_manufacturer: "Intel",
              cpu_architecture: "x64",
              cpu_cores: 32,
              cpu_threads: 64,
              cpu_baseSpeed: 2.0,
              cpu_maxSpeed: 3.2,
              cpu_cache_l1: 2048,
              cpu_cache_l2: 32768,
              cpu_cache_l3: 48,
              memory_total: 256,
              memory_type: "ddr4",
              memory_speed: 3200,
              memory_slots: 16,
              memory_slotsUsed: 8,
              memory_maxCapacity: 512,
              storage_types: ["nvme", "ssd"],
              storage_capacities: [1000, 4000],
              storage_interfaces: ["PCIe 4.0", "SATA"],
              storage_raidLevels: ["raid1", "raid10"],
              network_names: ["ens192", "ens224"],
              network_macAddresses: ["00:50:56:9f:" + toString(idx) + ":01", "00:50:56:9f:" + toString(idx) + ":02"],
              network_ipv4Addresses: ["10.10.1." + toString(idx), "10.10.2." + toString(idx)],
              network_speeds: [10000, 10000],
              network_types: ["ethernet", "ethernet"],
              power_type: "redundant",
              power_capacity: 1600,
              power_efficiency: "80_plus_platinum",
              power_voltage: 220,
              power_inputType: "ac",
              location_datacenter: "DC-PRIMARY-01",
              location_building: "BLDG-A",
              location_floor: 3,
              location_room: "SERVER-ROOM-03",
              location_rack: "RACK-A-" + toString(10 + (idx % 10)),
              location_rackPosition: (idx % 42) + 1,
              os_name: "Windows Server",
              os_version: "2022 Datacenter",
              os_distribution: "Microsoft",
              os_kernel: "NT 10.0",
              os_architecture: "x64",
              os_installDate: datetime() - duration({days: idx * 30}),
              os_lastUpdate: datetime() - duration({days: idx}),
              os_patchLevel: "KB5012345",
              mgmt_type: "idrac",
              mgmt_ipAddress: "10.99.1." + toString(idx),
              mgmt_firmwareVersion: "5.10.30.00",
              mgmt_accessMethod: "web",
              powerState: CASE idx % 10 WHEN 0 THEN "standby" ELSE "on" END,
              operationalStatus: CASE idx % 20 WHEN 0 THEN "maintenance" ELSE "operational" END,
              uptime: idx * 86400,
              bootTime: datetime() - duration({days: idx}),
              cpuUtilization: 15.0 + (idx % 30),
              memoryUtilization: 40.0 + (idx % 40),
              storageUtilization: 50.0 + (idx % 30),
              temperatureCPU: 45.0 + (idx % 20),
              temperatureAmbient: 22.0 + (idx % 5),
              purchaseDate: date() - duration({days: idx * 60}),
              warrantyExpiry: date() + duration({days: (1825 - idx * 10)}),
              maintenanceContract: "MC-ENTERPRISE-" + toString(idx),
              depreciationPeriod: 60,
              endOfLife: date() + duration({days: 1825}),
              criticality: "critical",
              dataClassification: "restricted",
              complianceRequirements: ["sox", "pci_dss", "hipaa"],
              node_id: randomUUID(),
              created_by: "AEON_INTEGRATION_WAVE9",
              created_date: datetime(),
              last_updated: datetime(),
              validation_status: "VALIDATED"
            })
            """)
            self.log_operation("physical_servers_batch_1_domain_controllers", {"count": 50})

            # Batch 2: Application Servers (50)
            session.run("""
            UNWIND range(1, 50) AS idx
            CREATE (s:PhysicalServer {
              serverID: "SRV-APP-" + toString(2000 + idx),
              assetTag: "AT-APP-" + toString(2000 + idx),
              hostname: "app" + toString(idx) + ".corp.example.com",
              domain: "corp.example.com",
              serialNumber: "SN-APP-" + toString(20000 + idx),
              manufacturer: CASE idx % 3 WHEN 0 THEN "Dell" WHEN 1 THEN "HP" ELSE "Cisco" END,
              model: "PowerEdge R740",
              formFactor: "rack_mount",
              rackUnit: 2,
              weight: 24.0,
              cpu_model: "Intel Xeon Gold 6248",
              cpu_manufacturer: "Intel",
              cpu_architecture: "x64",
              cpu_cores: 20,
              cpu_threads: 40,
              cpu_baseSpeed: 2.5,
              cpu_maxSpeed: 3.9,
              cpu_cache_l1: 1280,
              cpu_cache_l2: 20480,
              cpu_cache_l3: 27,
              memory_total: 192,
              memory_type: "ddr4",
              memory_speed: 2933,
              memory_slots: 12,
              memory_slotsUsed: 6,
              memory_maxCapacity: 384,
              storage_types: ["ssd", "hdd"],
              storage_capacities: [960, 8000],
              storage_interfaces: ["SATA", "SAS"],
              storage_raidLevels: ["raid5", "raid6"],
              network_names: ["eth0", "eth1"],
              network_macAddresses: ["00:50:56:a0:" + toString(idx) + ":01", "00:50:56:a0:" + toString(idx) + ":02"],
              network_ipv4Addresses: ["10.20.1." + toString(idx), "10.20.2." + toString(idx)],
              network_speeds: [1000, 1000],
              network_types: ["ethernet", "ethernet"],
              power_type: "n_plus_1",
              power_capacity: 1100,
              power_efficiency: "80_plus_gold",
              power_voltage: 220,
              power_inputType: "ac",
              location_datacenter: "DC-PRIMARY-01",
              location_building: "BLDG-A",
              location_floor: 2,
              location_room: "SERVER-ROOM-02",
              location_rack: "RACK-B-" + toString(10 + (idx % 10)),
              location_rackPosition: (idx % 42) + 1,
              os_name: "Red Hat Enterprise Linux",
              os_version: "8.6",
              os_distribution: "RHEL",
              os_kernel: "4.18.0-372",
              os_architecture: "x86_64",
              os_installDate: datetime() - duration({days: idx * 25}),
              os_lastUpdate: datetime() - duration({days: idx % 30}),
              os_patchLevel: "8.6.0-372.el8",
              mgmt_type: "ilo",
              mgmt_ipAddress: "10.99.2." + toString(idx),
              mgmt_firmwareVersion: "2.70",
              mgmt_accessMethod: "api",
              powerState: "on",
              operationalStatus: CASE idx % 25 WHEN 0 THEN "degraded" ELSE "operational" END,
              uptime: idx * 72000,
              bootTime: datetime() - duration({days: idx * 2}),
              cpuUtilization: 45.0 + (idx % 40),
              memoryUtilization: 60.0 + (idx % 30),
              storageUtilization: 65.0 + (idx % 25),
              temperatureCPU: 50.0 + (idx % 25),
              temperatureAmbient: 23.0 + (idx % 4),
              purchaseDate: date() - duration({days: idx * 50}),
              warrantyExpiry: date() + duration({days: (1460 - idx * 8)}),
              maintenanceContract: "MC-STANDARD-" + toString(idx),
              depreciationPeriod: 48,
              endOfLife: date() + duration({days: 1460}),
              criticality: "high",
              dataClassification: "internal",
              complianceRequirements: ["sox", "gdpr"],
              node_id: randomUUID(),
              created_by: "AEON_INTEGRATION_WAVE9",
              created_date: datetime(),
              last_updated: datetime(),
              validation_status: "VALIDATED"
            })
            """)
            self.log_operation("physical_servers_batch_2_application", {"count": 50})

            # Batch 3: Database Servers (50)
            session.run("""
            UNWIND range(1, 50) AS idx
            CREATE (s:PhysicalServer {
              serverID: "SRV-DB-" + toString(3000 + idx),
              assetTag: "AT-DB-" + toString(3000 + idx),
              hostname: "db" + toString(idx) + ".corp.example.com",
              domain: "corp.example.com",
              serialNumber: "SN-DB-" + toString(30000 + idx),
              manufacturer: "Dell",
              model: "PowerEdge R7525",
              formFactor: "rack_mount",
              rackUnit: 2,
              weight: 28.5,
              cpu_model: "AMD EPYC 7763",
              cpu_manufacturer: "AMD",
              cpu_architecture: "x64",
              cpu_cores: 64,
              cpu_threads: 128,
              cpu_baseSpeed: 2.45,
              cpu_maxSpeed: 3.5,
              cpu_cache_l1: 4096,
              cpu_cache_l2: 32768,
              cpu_cache_l3: 256,
              memory_total: 512,
              memory_type: "ddr4",
              memory_speed: 3200,
              memory_slots: 32,
              memory_slotsUsed: 16,
              memory_maxCapacity: 1024,
              storage_types: ["nvme", "nvme", "ssd"],
              storage_capacities: [2000, 2000, 16000],
              storage_interfaces: ["PCIe 4.0", "PCIe 4.0", "SAS"],
              storage_raidLevels: ["raid1", "raid1", "raid10"],
              network_names: ["ens192", "ens224", "ens256"],
              network_macAddresses: ["00:50:56:a1:" + toString(idx) + ":01", "00:50:56:a1:" + toString(idx) + ":02", "00:50:56:a1:" + toString(idx) + ":03"],
              network_ipv4Addresses: ["10.30.1." + toString(idx), "10.30.2." + toString(idx), "10.30.3." + toString(idx)],
              network_speeds: [10000, 10000, 25000],
              network_types: ["ethernet", "ethernet", "fiber"],
              power_type: "redundant",
              power_capacity: 2000,
              power_efficiency: "80_plus_titanium",
              power_voltage: 220,
              power_inputType: "ac",
              location_datacenter: "DC-PRIMARY-01",
              location_building: "BLDG-A",
              location_floor: 3,
              location_room: "SERVER-ROOM-DB",
              location_rack: "RACK-DB-" + toString((idx % 5) + 1),
              location_rackPosition: ((idx - 1) % 10) * 4 + 1,
              os_name: "Oracle Linux",
              os_version: "8.6",
              os_distribution: "Oracle",
              os_kernel: "5.4.17-2136",
              os_architecture: "x86_64",
              os_installDate: datetime() - duration({days: idx * 40}),
              os_lastUpdate: datetime() - duration({days: idx % 14}),
              os_patchLevel: "8.6.0-UEK-r6",
              mgmt_type: "idrac",
              mgmt_ipAddress: "10.99.3." + toString(idx),
              mgmt_firmwareVersion: "5.00.10.00",
              mgmt_accessMethod: "api",
              powerState: "on",
              operationalStatus: "operational",
              uptime: idx * 95000,
              bootTime: datetime() - duration({days: idx * 3}),
              cpuUtilization: 70.0 + (idx % 20),
              memoryUtilization: 80.0 + (idx % 15),
              storageUtilization: 75.0 + (idx % 20),
              temperatureCPU: 55.0 + (idx % 15),
              temperatureAmbient: 20.0 + (idx % 3),
              purchaseDate: date() - duration({days: idx * 45}),
              warrantyExpiry: date() + duration({days: (1825 - idx * 7)}),
              maintenanceContract: "MC-PREMIUM-" + toString(idx),
              depreciationPeriod: 60,
              endOfLife: date() + duration({days: 2190}),
              criticality: "critical",
              dataClassification: "confidential",
              complianceRequirements: ["sox", "pci_dss", "hipaa", "gdpr"],
              node_id: randomUUID(),
              created_by: "AEON_INTEGRATION_WAVE9",
              created_date: datetime(),
              last_updated: datetime(),
              validation_status: "VALIDATED"
            })
            """)
            self.log_operation("physical_servers_batch_3_database", {"count": 50})

            # Batch 4-8: Web, File, Backup, Hypervisor, Storage servers (50 each = 250)
            for batch_num, (prefix, server_type) in enumerate([
                ("WEB", "Web Server"),
                ("FILE", "File Server"),
                ("BACKUP", "Backup Server"),
                ("HV", "Hypervisor Host"),
                ("STOR", "Storage Controller")
            ], start=4):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (s:PhysicalServer {{
                  serverID: "SRV-{prefix}-" + toString({batch_num}000 + idx),
                  assetTag: "AT-{prefix}-" + toString({batch_num}000 + idx),
                  hostname: "{prefix.lower()}" + toString(idx) + ".corp.example.com",
                  domain: "corp.example.com",
                  serialNumber: "SN-{prefix}-" + toString({batch_num}0000 + idx),
                  manufacturer: CASE idx % 3 WHEN 0 THEN "Dell" WHEN 1 THEN "HP" ELSE "Supermicro" END,
                  model: "R740xd",
                  formFactor: "rack_mount",
                  rackUnit: 2,
                  weight: 26.0,
                  cpu_model: "Intel Xeon Silver 4214",
                  cpu_manufacturer: "Intel",
                  cpu_architecture: "x64",
                  cpu_cores: 12,
                  cpu_threads: 24,
                  cpu_baseSpeed: 2.2,
                  cpu_maxSpeed: 3.2,
                  cpu_cache_l1: 768,
                  cpu_cache_l2: 12288,
                  cpu_cache_l3: 16,
                  memory_total: 128,
                  memory_type: "ddr4",
                  memory_speed: 2666,
                  memory_slots: 12,
                  memory_slotsUsed: 4,
                  memory_maxCapacity: 192,
                  storage_types: ["ssd", "hdd"],
                  storage_capacities: [480, 12000],
                  storage_interfaces: ["SATA", "SAS"],
                  storage_raidLevels: ["none", "raid5"],
                  network_names: ["eth0", "eth1"],
                  network_macAddresses: ["00:50:56:a{batch_num}:" + toString(idx) + ":01", "00:50:56:a{batch_num}:" + toString(idx) + ":02"],
                  network_ipv4Addresses: ["10.{10 + batch_num}.1." + toString(idx), "10.{10 + batch_num}.2." + toString(idx)],
                  network_speeds: [1000, 1000],
                  network_types: ["ethernet", "ethernet"],
                  power_type: "single",
                  power_capacity: 750,
                  power_efficiency: "80_plus_silver",
                  power_voltage: 220,
                  power_inputType: "ac",
                  location_datacenter: CASE idx % 3 WHEN 0 THEN "DC-PRIMARY-01" WHEN 1 THEN "DC-SECONDARY-01" ELSE "DC-DR-01" END,
                  location_building: "BLDG-" + CASE idx % 3 WHEN 0 THEN "A" WHEN 1 THEN "B" ELSE "C" END,
                  location_floor: {batch_num} - 3,
                  location_room: "SERVER-ROOM-0" + toString({batch_num}),
                  location_rack: "RACK-{prefix}-" + toString((idx % 10) + 1),
                  location_rackPosition: (idx % 42) + 1,
                  os_name: CASE idx % 3 WHEN 0 THEN "Ubuntu Server" WHEN 1 THEN "CentOS" ELSE "Debian" END,
                  os_version: CASE idx % 3 WHEN 0 THEN "22.04 LTS" WHEN 1 THEN "Stream 9" ELSE "11" END,
                  os_distribution: CASE idx % 3 WHEN 0 THEN "Ubuntu" WHEN 1 THEN "CentOS" ELSE "Debian" END,
                  os_kernel: CASE idx % 3 WHEN 0 THEN "5.15.0-56" WHEN 1 THEN "5.14.0-162" ELSE "5.10.0-20" END,
                  os_architecture: "x86_64",
                  os_installDate: datetime() - duration({{days: idx * 30}}),
                  os_lastUpdate: datetime() - duration({{days: idx % 21}}),
                  os_patchLevel: "latest",
                  mgmt_type: CASE idx % 3 WHEN 0 THEN "idrac" WHEN 1 THEN "ilo" ELSE "ipmi" END,
                  mgmt_ipAddress: "10.99.{batch_num}." + toString(idx),
                  mgmt_firmwareVersion: "4.40.00.00",
                  mgmt_accessMethod: "ssh",
                  powerState: CASE idx % 15 WHEN 0 THEN "standby" ELSE "on" END,
                  operationalStatus: CASE idx % 30 WHEN 0 THEN "maintenance" ELSE "operational" END,
                  uptime: idx * 60000,
                  bootTime: datetime() - duration({{days: idx}}),
                  cpuUtilization: 25.0 + (idx % 50),
                  memoryUtilization: 45.0 + (idx % 40),
                  storageUtilization: 55.0 + (idx % 35),
                  temperatureCPU: 48.0 + (idx % 18),
                  temperatureAmbient: 22.0 + (idx % 5),
                  purchaseDate: date() - duration({{days: idx * 40}}),
                  warrantyExpiry: date() + duration({{days: (1095 - idx * 5)}}),
                  maintenanceContract: "MC-BASIC-" + toString(idx),
                  depreciationPeriod: 36,
                  endOfLife: date() + duration({{days: 1095}}),
                  criticality: CASE idx % 3 WHEN 0 THEN "high" WHEN 1 THEN "medium" ELSE "low" END,
                  dataClassification: CASE idx % 3 WHEN 0 THEN "internal" WHEN 1 THEN "confidential" ELSE "public" END,
                  complianceRequirements: CASE idx % 2 WHEN 0 THEN ["sox"] ELSE ["gdpr"] END,
                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE9",
                  created_date: datetime(),
                  last_updated: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)
                self.log_operation(f"physical_servers_batch_{batch_num}_{server_type.lower().replace(' ', '_')}", {"count": 50})

            # Verify total PhysicalServer count
            result = session.run("""
            MATCH (s:PhysicalServer) WHERE s.created_by = 'AEON_INTEGRATION_WAVE9'
            RETURN count(s) as total,
                   count(DISTINCT s.serverID) as unique_ids,
                   count(DISTINCT s.hostname) as unique_hostnames,
                   count(DISTINCT s.serialNumber) as unique_serials
            """)
            stats = result.single()
            self.log_operation("physical_servers_verification", dict(stats))
            assert stats['total'] == 400, f"Expected 400 PhysicalServers, got {stats['total']}"
            assert stats['unique_ids'] == 400, f"Duplicate serverIDs found"
            assert stats['unique_hostnames'] == 400, f"Duplicate hostnames found"
            assert stats['unique_serials'] == 400, f"Duplicate serial numbers found"

            return stats['total']

    def create_workstations_and_mobile(self) -> int:
        """Create 300 Workstation + 200 MobileDevice nodes = 500 total"""
        with self.driver.session() as session:
            # Workstations: 6 batches of 50 (300 total)
            for batch_num in range(1, 7):
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (w:Workstation {{
                  assetTag: "WS-{batch_num}-" + toString(idx),
                  hostname: "ws{batch_num}" + toString(idx) + ".corp.example.com",
                  serialNumber: "SN-WS-{batch_num * 1000 + 10000}" + toString(idx),
                  manufacturer: CASE idx % 4 WHEN 0 THEN "Dell" WHEN 1 THEN "HP" WHEN 2 THEN "Lenovo" ELSE "Apple" END,
                  model: CASE idx % 4 WHEN 0 THEN "OptiPlex 7090" WHEN 1 THEN "EliteDesk 800 G8" WHEN 2 THEN "ThinkCentre M920" ELSE "Mac Mini M2" END,
                  formFactor: CASE idx % 4 WHEN 0 THEN "desktop" WHEN 1 THEN "desktop" WHEN 2 THEN "laptop" ELSE "desktop" END,
                  cpu: CASE idx % 3 WHEN 0 THEN "Intel Core i7-11700" WHEN 1 THEN "Intel Core i5-11500" ELSE "Apple M2" END,
                  memory: CASE idx % 3 WHEN 0 THEN 32 WHEN 1 THEN 16 ELSE 8 END,
                  storage: CASE idx % 3 WHEN 0 THEN 1000 WHEN 1 THEN 512 ELSE 256 END,
                  graphics: CASE idx % 2 WHEN 0 THEN "NVIDIA GeForce GTX 1650" ELSE "Intel UHD Graphics 750" END,
                  operatingSystem: CASE idx % 4 WHEN 0 THEN "Windows 11 Pro" WHEN 1 THEN "Windows 10 Enterprise" WHEN 2 THEN "Ubuntu 22.04" ELSE "macOS Ventura" END,
                  osVersion: CASE idx % 4 WHEN 0 THEN "22H2" WHEN 1 THEN "21H2" WHEN 2 THEN "22.04.1" ELSE "13.2" END,
                  osBuild: "Build " + toString(19045 + idx),
                  bitness: CASE idx % 10 WHEN 0 THEN "32bit" ELSE "64bit" END,
                  macAddress: "00:1A:2B:{batch_num}C:" + toString(idx) + ":DD",
                  ipAddress: "192.168.{batch_num}." + toString(idx),
                  dhcpEnabled: CASE idx % 5 WHEN 0 THEN false ELSE true END,
                  dnsServers: ["8.8.8.8", "8.8.4.4"],
                  encryptionStatus: CASE idx % 3 WHEN 0 THEN "encrypted" WHEN 1 THEN "not_encrypted" ELSE "partially_encrypted" END,
                  encryptionType: CASE idx % 4 WHEN 0 THEN "bitlocker" WHEN 1 THEN "filevault" WHEN 2 THEN "luks" ELSE "veracrypt" END,
                  firewallEnabled: CASE idx % 10 WHEN 0 THEN false ELSE true END,
                  antivirusInstalled: CASE idx % 15 WHEN 0 THEN false ELSE true END,
                  antivirusVersion: "2024.1.0",
                  lastVirusScan: datetime() - duration({{days: idx % 7}}),
                  powerState: CASE idx % 8 WHEN 0 THEN "sleep" WHEN 7 THEN "off" ELSE "on" END,
                  lastBoot: datetime() - duration({{days: idx % 30}}),
                  uptime: idx * 43200,
                  primaryUser: "user{batch_num}" + toString(idx) + "@corp.example.com",
                  department: CASE idx % 5 WHEN 0 THEN "Engineering" WHEN 1 THEN "Finance" WHEN 2 THEN "HR" WHEN 3 THEN "Sales" ELSE "Operations" END,
                  location: CASE idx % 4 WHEN 0 THEN "Building A" WHEN 1 THEN "Building B" WHEN 2 THEN "Remote" ELSE "Building C" END,
                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE9",
                  created_date: datetime(),
                  last_updated: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)
                self.log_operation(f"workstations_batch_{batch_num}", {"count": 50})

            # MobileDevices: 4 batches of 50 (200 total)
            for batch_num in range(1, 5):
                imei_base = 1234567890000 + batch_num * 1000
                phone_prefix = 100 + batch_num
                ip_subnet = 10 + batch_num
                session.run(f"""
                UNWIND range(1, 50) AS idx
                CREATE (m:MobileDevice {{
                  assetTag: "MOB-{batch_num}-" + toString(idx),
                  hostname: "mobile{batch_num}" + toString(idx) + ".corp.example.com",
                  serialNumber: "SN-MOB-{batch_num * 1000}-" + toString(idx),
                  manufacturer: CASE idx % 3 WHEN 0 THEN "Apple" WHEN 1 THEN "Samsung" ELSE "Google" END,
                  model: CASE idx % 3 WHEN 0 THEN "iPhone 14 Pro" WHEN 1 THEN "Galaxy S23 Ultra" ELSE "Pixel 7 Pro" END,
                  formFactor: "laptop",
                  cpu: CASE idx % 3 WHEN 0 THEN "Apple A16 Bionic" WHEN 1 THEN "Snapdragon 8 Gen 2" ELSE "Google Tensor G2" END,
                  memory: CASE idx % 3 WHEN 0 THEN 6 WHEN 1 THEN 12 ELSE 12 END,
                  storage: CASE idx % 3 WHEN 0 THEN 256 WHEN 1 THEN 512 ELSE 128 END,
                  graphics: "Integrated",
                  deviceType: CASE idx % 2 WHEN 0 THEN "smartphone" ELSE "tablet" END,
                  imei: "35" + toString({imei_base} + idx),
                  carrier: CASE idx % 3 WHEN 0 THEN "Verizon" WHEN 1 THEN "AT&T" ELSE "T-Mobile" END,
                  phoneNumber: "+1-555-{phone_prefix}-" + toString(1000 + idx),
                  mobileOS: CASE idx % 3 WHEN 0 THEN "ios" WHEN 1 THEN "android" ELSE "android" END,
                  osVersion: CASE idx % 3 WHEN 0 THEN "16.3" WHEN 1 THEN "13.0" ELSE "13.0" END,
                  jailbroken: false,
                  rooted: CASE idx % 20 WHEN 0 THEN true ELSE false END,
                  passcodeEnabled: CASE idx % 30 WHEN 0 THEN false ELSE true END,
                  biometricEnabled: CASE idx % 10 WHEN 0 THEN false ELSE true END,
                  mdmEnrolled: CASE idx % 8 WHEN 0 THEN false ELSE true END,
                  wifiMacAddress: "AA:BB:CC:{batch_num}D:EE:" + toString(idx),
                  bluetoothMacAddress: "AA:BB:CC:{batch_num}E:FF:" + toString(idx),
                  cellularConnection: CASE idx % 5 WHEN 0 THEN false ELSE true END,
                  operatingSystem: CASE idx % 3 WHEN 0 THEN "iOS 16" WHEN 1 THEN "Android 13" ELSE "Android 13" END,
                  macAddress: "AA:BB:CC:{batch_num}D:" + toString(idx) + ":00",
                  ipAddress: "192.168.{ip_subnet}." + toString(idx),
                  dhcpEnabled: true,
                  dnsServers: ["8.8.8.8"],
                  encryptionStatus: CASE idx % 10 WHEN 0 THEN "not_encrypted" ELSE "encrypted" END,
                  encryptionType: CASE idx % 2 WHEN 0 THEN "filevault" ELSE "luks" END,
                  firewallEnabled: true,
                  antivirusInstalled: CASE idx % 3 WHEN 0 THEN true ELSE false END,
                  antivirusVersion: "Mobile-2024.1",
                  lastVirusScan: datetime() - duration({{days: idx % 14}}),
                  powerState: CASE idx % 10 WHEN 0 THEN "sleep" ELSE "on" END,
                  lastBoot: datetime() - duration({{days: idx % 7}}),
                  uptime: idx * 21600,
                  primaryUser: "user-mob{batch_num}" + toString(idx) + "@corp.example.com",
                  department: CASE idx % 4 WHEN 0 THEN "Sales" WHEN 1 THEN "Executive" WHEN 2 THEN "Field Service" ELSE "Support" END,
                  location: "Mobile",
                  node_id: randomUUID(),
                  created_by: "AEON_INTEGRATION_WAVE9",
                  created_date: datetime(),
                  last_updated: datetime(),
                  validation_status: "VALIDATED"
                }})
                """)
                self.log_operation(f"mobile_devices_batch_{batch_num}", {"count": 50})

            # Verify total counts
            result = session.run("""
            MATCH (w:Workstation) WHERE w.created_by = 'AEON_INTEGRATION_WAVE9'
            RETURN count(w) as workstation_count,
                   count(DISTINCT w.assetTag) as unique_ws_tags
            """)
            ws_stats = result.single()
            self.log_operation("workstations_verification", dict(ws_stats))
            assert ws_stats['workstation_count'] == 300, f"Expected 300 Workstations, got {ws_stats['workstation_count']}"

            result = session.run("""
            MATCH (m:MobileDevice) WHERE m.created_by = 'AEON_INTEGRATION_WAVE9'
            RETURN count(m) as mobile_count,
                   count(DISTINCT m.assetTag) as unique_mob_tags,
                   count(DISTINCT m.imei) as unique_imeis
            """)
            mob_stats = result.single()
            self.log_operation("mobile_devices_verification", dict(mob_stats))
            assert mob_stats['mobile_count'] == 200, f"Expected 200 MobileDevices, got {mob_stats['mobile_count']}"
            assert mob_stats['unique_imeis'] == 200, "Duplicate IMEIs found"

            return ws_stats['workstation_count'] + mob_stats['mobile_count']

    def create_network_devices(self) -> int:
        """Create 300 NetworkDevice nodes in 6 batches"""
        with self.driver.session() as session:
            device_types = [
                ("ROUTER", "router", 50),
                ("SWITCH-A", "switch", 50),
                ("SWITCH-B", "switch", 50),
                ("FIREWALL", "firewall", 50),
                ("LB", "load_balancer", 50),
                ("VPN-AP", "vpn_gateway", 30),
                ("WAP", "wireless_ap", 20)
            ]

            batch_idx = 1
            for prefix, dev_type, count in device_types:
                if count == 50:
                    session.run(f"""
                    UNWIND range(1, {count}) AS idx
                    CREATE (nd:NetworkDevice {{
                      deviceID: "{prefix}-" + toString({batch_idx * 100} + idx),
                      hostname: "{prefix.lower()}" + toString(idx) + ".net.corp.example.com",
                      managementIP: "10.{100 + batch_idx}." + toString((idx - 1) / 250) + "." + toString(((idx - 1) % 250) + 1),
                      deviceType: "{dev_type}",
                      manufacturer: CASE idx % 4 WHEN 0 THEN "Cisco" WHEN 1 THEN "Juniper" WHEN 2 THEN "Arista" ELSE "HP" END,
                      model: CASE "{dev_type}"
                             WHEN "router" THEN "ISR 4451"
                             WHEN "switch" THEN "Catalyst 9300"
                             WHEN "firewall" THEN "ASA 5525-X"
                             WHEN "load_balancer" THEN "F5 BIG-IP 4200v"
                             ELSE "Generic Model" END,
                      serialNumber: "SN-{prefix}-" + toString({batch_idx * 10000} + idx),
                      firmwareVersion: "15." + toString(idx % 5) + ".3",
                      operatingSystem: CASE idx % 3 WHEN 0 THEN "Cisco IOS XE" WHEN 1 THEN "Junos OS" ELSE "EOS" END,
                      osVersion: toString(16 + idx % 3) + ".3.1",
                      configurationVersion: "v2024." + toString(idx % 12 + 1),
                      lastConfigBackup: datetime() - duration({{days: idx % 7}}),
                      portCount: CASE "{dev_type}" WHEN "router" THEN 48 WHEN "switch" THEN 48 ELSE 24 END,
                      speed: CASE idx % 4 WHEN 0 THEN "1Gbps" WHEN 1 THEN "10Gbps" WHEN 2 THEN "40Gbps" ELSE "100Gbps" END,
                      formFactor: CASE idx % 2 WHEN 0 THEN "rack_mount" ELSE "standalone" END,
                      powerType: CASE idx % 2 WHEN 0 THEN "ac" ELSE "poe" END,
                      throughput: CASE idx % 4 WHEN 0 THEN 10.0 WHEN 1 THEN 40.0 WHEN 2 THEN 100.0 ELSE 400.0 END,
                      packetsPerSecond: CASE idx % 3 WHEN 0 THEN 10000000 WHEN 1 THEN 50000000 ELSE 100000000 END,
                      concurrentSessions: CASE "{dev_type}" WHEN "firewall" THEN 100000 WHEN "load_balancer" THEN 500000 ELSE 1000000 END,
                      operationalStatus: CASE idx % 20 WHEN 0 THEN "degraded" ELSE "up" END,
                      adminStatus: CASE idx % 30 WHEN 0 THEN "maintenance" ELSE "enabled" END,
                      uptime: idx * 50000,
                      node_id: randomUUID(),
                      created_by: "AEON_INTEGRATION_WAVE9",
                      created_date: datetime(),
                      last_updated: datetime(),
                      validation_status: "VALIDATED"
                    }})
                    """)
                    self.log_operation(f"network_devices_batch_{batch_idx}_{prefix}", {"count": count})
                    batch_idx += 1
                else:
                    # For VPN gateways (30) and wireless APs (20) - combine into single batch
                    session.run(f"""
                    UNWIND range(1, {count}) AS idx
                    CREATE (nd:NetworkDevice {{
                      deviceID: "{prefix}-" + toString(idx),
                      hostname: "{prefix.lower()}" + toString(idx) + ".net.corp.example.com",
                      managementIP: "10.{100 + batch_idx}." + toString((idx - 1) / 250) + "." + toString(((idx - 1) % 250) + 1),
                      deviceType: "{dev_type}",
                      manufacturer: CASE idx % 3 WHEN 0 THEN "Cisco" WHEN 1 THEN "Fortinet" ELSE "Palo Alto" END,
                      model: "Model-" + toString(idx % 5 + 1),
                      serialNumber: "SN-{prefix}-" + toString(10000 + idx),
                      firmwareVersion: "v8." + toString(idx % 3),
                      operatingSystem: "Proprietary",
                      osVersion: toString(8 + idx % 2) + ".0",
                      configurationVersion: "v2024." + toString(idx % 12 + 1),
                      lastConfigBackup: datetime() - duration({{days: idx % 14}}),
                      portCount: CASE "{dev_type}" WHEN "wireless_ap" THEN 4 ELSE 8 END,
                      speed: "1Gbps",
                      formFactor: CASE idx % 2 WHEN 0 THEN "rack_mount" ELSE "standalone" END,
                      powerType: "poe",
                      throughput: 1.0,
                      packetsPerSecond: 1000000,
                      concurrentSessions: 50000,
                      operationalStatus: CASE idx % 15 WHEN 0 THEN "testing" ELSE "up" END,
                      adminStatus: "enabled",
                      uptime: idx * 40000,
                      node_id: randomUUID(),
                      created_by: "AEON_INTEGRATION_WAVE9",
                      created_date: datetime(),
                      last_updated: datetime(),
                      validation_status: "VALIDATED"
                    }})
                    """)
                    self.log_operation(f"network_devices_batch_6_{prefix}", {"count": count})

            # Verify total count
            result = session.run("""
            MATCH (nd:NetworkDevice) WHERE nd.created_by = 'AEON_INTEGRATION_WAVE9'
            RETURN count(nd) as total,
                   count(DISTINCT nd.deviceID) as unique_ids,
                   collect(DISTINCT nd.deviceType) as device_types,
                   count(DISTINCT nd.serialNumber) as unique_serials
            """)
            stats = result.single()
            self.log_operation("network_devices_verification", dict(stats))
            assert stats['total'] == 300, f"Expected 300 NetworkDevices, got {stats['total']}"
            assert stats['unique_ids'] == 300, "Duplicate deviceIDs found"

            return stats['total']

    def create_storage_arrays(self) -> int:
        """Create 200 StorageArray nodes in 4 batches"""
        with self.driver.session() as session:
            array_types = [
                ("SAN", "san", 80),
                ("NAS", "nas", 80),
                ("OBJ", "object_storage", 40)
            ]

            batch_idx = 1
            for prefix, arr_type, target_count in array_types:
                batches_needed = (target_count + 49) // 50  # Ceiling division
                for sub_batch in range(batches_needed):
                    count_in_batch = min(50, target_count - (sub_batch * 50))
                    session.run(f"""
                    UNWIND range(1, {count_in_batch}) AS idx
                    CREATE (sa:StorageArray {{
                      arrayID: "{prefix}-ARRAY-" + toString({batch_idx * 100 + sub_batch * 50} + idx),
                      arrayName: "{prefix} Array " + toString({sub_batch * 50} + idx),
                      serialNumber: "SN-{prefix}-" + toString({batch_idx * 10000 + sub_batch * 1000} + idx),
                      manufacturer: CASE idx % 3 WHEN 0 THEN "NetApp" WHEN 1 THEN "Dell EMC" ELSE "Pure Storage" END,
                      model: CASE "{arr_type}" WHEN "san" THEN "PowerStore 500T" WHEN "nas" THEN "FAS9500" ELSE "FlashBlade" END,
                      arrayType: "{arr_type}",
                      protocol: CASE "{arr_type}"
                                WHEN "san" THEN ["fc", "iscsi"]
                                WHEN "nas" THEN ["nfs", "smb"]
                                ELSE ["s3", "swift"] END,
                      totalCapacity: CASE idx % 4 WHEN 0 THEN 500 WHEN 1 THEN 1000 WHEN 2 THEN 2000 ELSE 5000 END,
                      usedCapacity: toInteger((CASE idx % 4 WHEN 0 THEN 500 WHEN 1 THEN 1000 WHEN 2 THEN 2000 ELSE 5000 END) * (0.4 + (idx % 50) * 0.01)),
                      availableCapacity: toInteger((CASE idx % 4 WHEN 0 THEN 500 WHEN 1 THEN 1000 WHEN 2 THEN 2000 ELSE 5000 END) * (0.6 - (idx % 50) * 0.01)),
                      utilizationPercentage: 40.0 + (idx % 50),
                      iopsRead: CASE idx % 3 WHEN 0 THEN 100000 WHEN 1 THEN 250000 ELSE 500000 END,
                      iopsWrite: CASE idx % 3 WHEN 0 THEN 50000 WHEN 1 THEN 125000 ELSE 250000 END,
                      throughputRead: CASE idx % 3 WHEN 0 THEN 5000.0 WHEN 1 THEN 10000.0 ELSE 20000.0 END,
                      throughputWrite: CASE idx % 3 WHEN 0 THEN 2500.0 WHEN 1 THEN 5000.0 ELSE 10000.0 END,
                      latencyRead: CASE idx % 3 WHEN 0 THEN 0.5 WHEN 1 THEN 0.3 ELSE 0.1 END,
                      latencyWrite: CASE idx % 3 WHEN 0 THEN 1.0 WHEN 1 THEN 0.6 ELSE 0.2 END,
                      raidLevel: CASE "{arr_type}" WHEN "san" THEN ["raid6", "raid10"] WHEN "nas" THEN ["raid5"] ELSE ["raid0"] END,
                      deduplicationEnabled: CASE idx % 2 WHEN 0 THEN true ELSE false END,
                      compressionEnabled: CASE idx % 3 WHEN 0 THEN false ELSE true END,
                      encryptionEnabled: CASE idx % 5 WHEN 0 THEN false ELSE true END,
                      snapshotEnabled: CASE idx % 4 WHEN 0 THEN false ELSE true END,
                      replicationEnabled: CASE idx % 3 WHEN 0 THEN true ELSE false END,
                      node_id: randomUUID(),
                      created_by: "AEON_INTEGRATION_WAVE9",
                      created_date: datetime(),
                      last_updated: datetime(),
                      validation_status: "VALIDATED"
                    }})
                    """)
                    self.log_operation(f"storage_arrays_batch_{batch_idx}_{prefix}_{sub_batch + 1}", {"count": count_in_batch})
                batch_idx += 1

            # Verify total count
            result = session.run("""
            MATCH (sa:StorageArray) WHERE sa.created_by = 'AEON_INTEGRATION_WAVE9'
            RETURN count(sa) as total,
                   count(DISTINCT sa.arrayID) as unique_ids,
                   collect(DISTINCT sa.arrayType) as array_types
            """)
            stats = result.single()
            self.log_operation("storage_arrays_verification", dict(stats))
            assert stats['total'] == 200, f"Expected 200 StorageArrays, got {stats['total']}"
            assert stats['unique_ids'] == 200, "Duplicate arrayIDs found"

            return stats['total']

    def create_peripheral_devices(self) -> int:
        """Create 100 PeripheralDevice nodes in 2 batches"""
        with self.driver.session() as session:
            # Batch 1: Printers (40) + Cameras (10) = 50
            session.run("""
            UNWIND range(1, 40) AS idx
            CREATE (pd:PeripheralDevice {
              deviceID: "PRINTER-" + toString(idx),
              deviceType: "printer",
              manufacturer: CASE idx % 3 WHEN 0 THEN "HP" WHEN 1 THEN "Canon" ELSE "Epson" END,
              model: "LaserJet Pro " + toString(4000 + idx % 5),
              firmwareVersion: "v2023." + toString(idx % 12 + 1),
              ipAddress: "192.168.50." + toString(idx),
              macAddress: "AA:BB:CC:DD:EE:" + toString(idx),
              networkConnected: true,
              node_id: randomUUID(),
              created_by: "AEON_INTEGRATION_WAVE9",
              created_date: datetime(),
              last_updated: datetime(),
              validation_status: "VALIDATED"
            })
            """)

            session.run("""
            UNWIND range(1, 10) AS idx
            CREATE (pd:PeripheralDevice {
              deviceID: "CAMERA-" + toString(idx),
              deviceType: "camera",
              manufacturer: CASE idx % 2 WHEN 0 THEN "Axis" ELSE "Hikvision" END,
              model: "IP Camera 4K",
              firmwareVersion: "v5." + toString(idx % 3),
              ipAddress: "192.168.51." + toString(idx),
              macAddress: "BB:CC:DD:EE:FF:" + toString(idx),
              networkConnected: true,
              node_id: randomUUID(),
              created_by: "AEON_INTEGRATION_WAVE9",
              created_date: datetime(),
              last_updated: datetime(),
              validation_status: "VALIDATED"
            })
            """)
            self.log_operation("peripheral_devices_batch_1", {"printers": 40, "cameras": 10})

            # Batch 2: Access Readers (20) + IoT Sensors (30) = 50
            session.run("""
            UNWIND range(1, 20) AS idx
            CREATE (pd:PeripheralDevice {
              deviceID: "READER-" + toString(idx),
              deviceType: "access_reader",
              manufacturer: CASE idx % 2 WHEN 0 THEN "HID Global" ELSE "Honeywell" END,
              model: "HID iCLASS SE",
              firmwareVersion: "v3." + toString(idx % 5),
              ipAddress: "192.168.52." + toString(idx),
              macAddress: "CC:DD:EE:FF:00:" + toString(idx),
              networkConnected: true,
              node_id: randomUUID(),
              created_by: "AEON_INTEGRATION_WAVE9",
              created_date: datetime(),
              last_updated: datetime(),
              validation_status: "VALIDATED"
            })
            """)

            session.run("""
            UNWIND range(1, 30) AS idx
            CREATE (pd:PeripheralDevice {
              deviceID: "IOT-SENSOR-" + toString(idx),
              deviceType: "iot_sensor",
              manufacturer: CASE idx % 3 WHEN 0 THEN "Cisco" WHEN 1 THEN "Siemens" ELSE "Schneider Electric" END,
              model: "Industrial Sensor v2",
              firmwareVersion: "v1." + toString(idx % 8),
              ipAddress: "192.168.53." + toString(idx),
              macAddress: "DD:EE:FF:00:11:" + toString(idx),
              networkConnected: CASE idx % 10 WHEN 0 THEN false ELSE true END,
              node_id: randomUUID(),
              created_by: "AEON_INTEGRATION_WAVE9",
              created_date: datetime(),
              last_updated: datetime(),
              validation_status: "VALIDATED"
            })
            """)
            self.log_operation("peripheral_devices_batch_2", {"access_readers": 20, "iot_sensors": 30})

            # Verify total count
            result = session.run("""
            MATCH (pd:PeripheralDevice) WHERE pd.created_by = 'AEON_INTEGRATION_WAVE9'
            RETURN count(pd) as total,
                   count(DISTINCT pd.deviceID) as unique_ids,
                   collect(DISTINCT pd.deviceType) as device_types
            """)
            stats = result.single()
            self.log_operation("peripheral_devices_verification", dict(stats))
            assert stats['total'] == 100, f"Expected 100 PeripheralDevices, got {stats['total']}"
            assert stats['unique_ids'] == 100, "Duplicate deviceIDs found"

            return stats['total']

    def verify_hardware_integrity(self):
        """Comprehensive verification of all hardware nodes"""
        with self.driver.session() as session:
            # Overall count
            result = session.run("""
            MATCH (n) WHERE n.created_by = 'AEON_INTEGRATION_WAVE9'
              AND (n:PhysicalServer OR n:Workstation OR n:MobileDevice OR n:NetworkDevice OR n:StorageArray OR n:PeripheralDevice)
            RETURN labels(n)[0] as nodeType, count(*) as count
            ORDER BY nodeType
            """)

            total = 0
            for record in result:
                node_type = record['nodeType']
                count = record['count']
                self.log_operation(f"final_verification_{node_type}", {"count": count})
                total += count

            assert total == 1500, f"Expected 1500 total hardware nodes, got {total}"
            self.log_operation("hardware_total_verification", {"total_nodes": total, "status": "PASSED"})

            return total

    def execute(self):
        try:
            self.log_operation("wave_9_hardware_execution_started", {"timestamp": datetime.utcnow().isoformat()})

            # Create all node types
            ps_count = self.create_physical_servers()
            logging.info(f"✅ PhysicalServer nodes created: {ps_count}")

            ws_mob_count = self.create_workstations_and_mobile()
            logging.info(f"✅ Workstation + MobileDevice nodes created: {ws_mob_count}")

            nd_count = self.create_network_devices()
            logging.info(f"✅ NetworkDevice nodes created: {nd_count}")

            sa_count = self.create_storage_arrays()
            logging.info(f"✅ StorageArray nodes created: {sa_count}")

            pd_count = self.create_peripheral_devices()
            logging.info(f"✅ PeripheralDevice nodes created: {pd_count}")

            # Final verification
            total_count = self.verify_hardware_integrity()

            self.log_operation("wave_9_hardware_execution_completed", {
                "timestamp": datetime.utcnow().isoformat(),
                "total_nodes": total_count,
                "physical_servers": ps_count,
                "workstations_mobile": ws_mob_count,
                "network_devices": nd_count,
                "storage_arrays": sa_count,
                "peripheral_devices": pd_count,
                "status": "SUCCESS"
            })

            logging.info(f"🎉 Wave 9 Hardware Assets completed: {total_count} nodes created and verified")

        except Exception as e:
            self.log_operation("wave_9_hardware_execution_error", {"error": str(e)})
            logging.error(f"Wave 9 Hardware execution failed: {e}")
            raise
        finally:
            self.driver.close()

if __name__ == "__main__":
    executor = Wave9HardwareExecutor()
    executor.execute()
