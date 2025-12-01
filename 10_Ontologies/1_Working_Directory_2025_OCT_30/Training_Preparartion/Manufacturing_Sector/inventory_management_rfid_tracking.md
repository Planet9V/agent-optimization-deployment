# RFID Inventory Management and Tracking Operations

## Overview
Operational procedures for radio-frequency identification (RFID) based inventory management including tag encoding, location tracking, cycle counting, and automated replenishment triggers in manufacturing warehouses.

## Equipment Specifications
- **RFID Readers**: Zebra FX9600 fixed readers, Zebra MC3390R handheld readers  
- **RFID Tags**: Alien Squiggle inlays (UHF Gen2), Confidex Ironside tags for metal surfaces
- **Middleware**: Zebra RFID Middleware, Impinj ItemSense platform
- **WMS Integration**: SAP Extended Warehouse Management, Manhattan SCALE
- **Network**: EtherNet/IP, PROFINET for industrial integration

## 1. RFID System Architecture and Infrastructure

### Fixed RFID Reader Installation and Zoning
```annotation
type: infrastructure_setup
context: Fixed RFID readers create monitored zones at dock doors, warehouse gates, production areas
equipment: Zebra FX9600 4-port fixed reader with circularly polarized antennas
installation_procedure:
  - Mount readers 8-12 feet high on doorways, conveyors, or overhead gantries
  - Position antennas to create read zones without blind spots
  - Configure transmit power (20-30 dBm) and frequency hopping per FCC regulations
  - Verify read rate 200+ tags/second with 99.9% accuracy
zone_configuration:
  - Receiving dock: Read inbound pallets automatically as forklifts pass through doorway
  - Shipping dock: Verify correct products loaded on outbound trucks
  - Production line entry/exit: Track work-in-process inventory movement
  - Warehouse aisles: Monitor inventory location changes in real-time
integration: Readers connected via Ethernet to RFID middleware server, data forwarded to WMS
```

### RFID Tag Selection and Encoding Standards
```annotation
type: tag_management
context: Different tag types required for various materials and environmental conditions
equipment: Zebra ZT411 RFID printer/encoder for label printing and tag programming
tag_types:
  - Paper labels (Alien Squiggle): General-purpose for cardboard boxes and plastic totes
  - Metal-mount tags (Confidex Ironside): For steel racks, metal containers, tooling
  - High-temperature tags: For parts exposed to paint ovens, welding (withstand 200°C)
  - Anti-tamper tags: Frangible antennas detect removal attempts (security applications)
encoding_standards:
  - EPC Gen2 protocol: Global standard for UHF RFID tags
  - EPC SGTIN-96: Serialized Global Trade Item Number (encodes GTIN + serial number)
  - User memory: Store additional data (lot number, expiration date, assembly instructions)
  - TID memory: Tag identifier (permanent, factory-programmed, anti-counterfeiting)
encoding_procedure:
  1. Design label template in Zebra Designer (barcode + RFID + human-readable text)
  2. Load roll of RFID labels into ZT411 printer
  3. WMS sends print job with serial numbers and EPC data
  4. Printer encodes RFID chip and prints label simultaneously (5-8 labels/minute)
  5. Verify encoding successful (read-after-write validation)
  6. Apply label to product, container, or pallet
```

### RFID Middleware Configuration and Data Filtering
```annotation
type: software_configuration
context: Middleware processes raw RFID reads, filters duplicates, routes data to business applications
equipment: Zebra RFID Middleware running on Windows Server with SQL database
configuration_parameters:
  - Read smoothing: Eliminate duplicate reads (tag read 20 times/second, report once)
  - Dwell time: Tag must be present 2 seconds before reported (prevent false reads)
  - Exit threshold: Tag must be absent 5 seconds before departure reported
  - Zone transitions: Track tag moving from Zone A to Zone B (location updates)
data_filtering:
  - Raw data: 10,000 tag reads/minute from all readers
  - Filtered data: 500 unique tag events/minute (arrivals, departures, moves)
  - Business events: 50 transactions/minute to WMS (receipts, picks, shipments)
integration_protocols:
  - REST API: WMS queries middleware for tag locations via HTTP requests
  - MQTT: Real-time pub/sub messaging for instant inventory updates
  - SOAP web services: Legacy ERP integration for order fulfillment
monitoring: Middleware dashboard displays reader health, read rates, tag population in each zone
```

### Antenna Tuning and RF Propagation Optimization
```annotation
type: performance_tuning
context: RFID read performance depends on antenna placement, power, and polarization
equipment: Voyantic Tagformance RFID measurement system for scientific tuning
tuning_procedure:
  1. Survey environment for metal objects and RF interference sources
  2. Install antennas in candidate locations (doorway, overhead, side-mounted)
  3. Test with sample tagged products at various orientations
  4. Measure read range and accuracy using Tagformance tester
  5. Adjust antenna angle (±15°), height (±2 feet), and transmit power (±5 dBm)
  6. Achieve target performance: 100% read rate at 6-foot range, <0.1% false reads
rf_interference_mitigation:
  - Metal surfaces: Use metal-mount tags with tuned antennas (read range 3-5 feet vs. 15+ feet for paper tags)
  - Liquids: Orient antennas perpendicular to liquid containers (water absorbs RF energy)
  - Dense tag populations: Use sequential reads vs. simultaneous (prevent tag collisions)
validation: 100-tag stress test with mixed orientations, verify 99%+ read accuracy before production deployment
```

## 2. Receiving and Put-Away Operations

### Inbound Pallet RFID Verification
```annotation
type: receiving_process
context: Verify received pallets match purchase order using RFID vs. manual barcode scanning
equipment: Zebra FX9600 reader at receiving dock door, forklift with RFID reader
receiving_workflow:
  1. Truck arrives at receiving dock, driver provides shipping manifest
  2. Forklift unloads pallet, drives through RFID portal (fixed readers on doorframe)
  3. RFID readers interrogate all tags on pallet simultaneously (200 tags read in 1-2 seconds)
  4. Middleware compares read tags against purchase order (expected EPCs)
  5. WMS displays match status on receiving terminal:
     - Green: All expected items present, no extras
     - Yellow: Missing items detected (list displayed for investigation)
     - Red: Extra/wrong items detected (potential shipping error)
  6. Receiver confirms receipt in WMS, inventory updated in real-time
benefits:
  - 95% faster than manual barcode scanning (2 seconds vs. 40 seconds for 20-item pallet)
  - 99.9% accuracy vs. 85-90% for manual scanning (eliminates human error)
  - Instant visibility: Inventory available for production planning within seconds of receipt
discrepancy_handling: Missing/extra items flagged for investigation, supplier notified automatically via EDI
```

### Automated License Plate Number (LPN) Assignment
```annotation
type: inventory_identification
context: RFID tags encoded with unique pallet IDs (LPNs) for warehouse tracking
equipment: Zebra ZT411 RFID printer at receiving station, WMS LPN generation module
lpn_assignment_workflow:
  1. Receiver scans purchase order barcode on receiving terminal
  2. WMS generates unique LPN for pallet (format: PALLET-2025-001234)
  3. WMS sends print command to RFID printer
  4. Printer encodes RFID tag with LPN EPC and prints label
  5. Receiver applies RFID label to pallet (standardized location: upper right corner)
  6. LPN now linked to purchase order line items in WMS database
  7. Pallet ready for put-away to warehouse location
lpn_structure:
  - Company prefix: Identifies organization (assigned by GS1)
  - Asset type: PALLET, TOTE, CONTAINER
  - Year: 2025
  - Sequential number: 001234 (resets annually)
traceability: All future transactions reference LPN, full history tracked (received, moved, picked, shipped)
```

### Dynamic Slotting and Optimal Put-Away Location
```annotation
type: warehouse_optimization
context: WMS recommends optimal storage location based on product velocity and space utilization
equipment: WMS slotting algorithm with RFID location tracking
put_away_workflow:
  1. Forklift operator scans pallet LPN with handheld RFID reader
  2. WMS analyzes product characteristics:
     - Product velocity: Fast-movers near shipping (A items), slow-movers in reserve (C items)
     - Product dimensions: Match pallet height to rack slot height (maximize cube utilization)
     - Product weight: Heavy pallets on lower racks (safety and ergonomics)
     - Hazmat requirements: Segregate flammable materials per NFPA 400
  3. WMS displays recommended location on forklift terminal: "Put-away to A-12-03-B"
  4. Operator drives to location, places pallet in rack
  5. Fixed RFID reader at aisle entrance confirms pallet in correct zone
  6. Operator confirms put-away complete, WMS updates inventory location
location_accuracy: RFID tracking maintains 99.5% location accuracy vs. 90-95% for barcode-only systems
slotting_benefits: 15-20% reduction in travel time, 10% increase in storage density
```

### Cross-Docking and Flow-Through Operations
```annotation
type: expedited_fulfillment
context: High-velocity products bypass warehouse storage, move directly from receiving to shipping
equipment: RFID readers at receiving and shipping docks, WMS cross-dock module
cross_dock_workflow:
  1. Inbound pallet arrives with customer order already allocated
  2. RFID reader at receiving dock identifies pallet LPN
  3. WMS recognizes pallet assigned to outbound shipment (no put-away required)
  4. Forklift operator directed to staging lane for outbound truck
  5. RFID reader at shipping dock verifies correct pallet loaded on truck
  6. Pallet dwell time in warehouse: <2 hours vs. 3-5 days for traditional put-away/pick
benefits: Reduced handling (1 touch vs. 3 touches), faster order fulfillment, lower labor costs
application: E-commerce fulfillment centers, food distribution (perishable goods), JIT manufacturing supply
accuracy: RFID ensures correct cross-dock allocation (99.9% vs. 95% for manual processes)
```

## 3. Picking and Order Fulfillment Operations

### RFID-Enabled Pick-to-Light Systems
```annotation
type: order_picking
context: Integrate RFID verification with pick-to-light for fast, accurate order fulfillment
equipment: Zebra MC3390R RFID handheld reader, pick-to-light displays at rack locations
pick_workflow:
  1. WMS generates pick list for customer order (20 line items)
  2. Picker scans order barcode with RFID handheld
  3. Pick-to-light displays illuminate at first location (green LED, quantity displayed)
  4. Picker retrieves items from bin, scans bin location with RFID reader
  5. RFID reader verifies correct location (reads RFID tag on bin label)
  6. Picker scans picked items with RFID reader (verifies correct product)
  7. Pick-to-light display confirms pick complete (LED turns red)
  8. System directs picker to next location, process repeats
verification_benefits:
  - Location verification: Ensures picker at correct bin (prevents wrong-slot picks)
  - Product verification: Confirms correct SKU picked (eliminates substitution errors)
  - Quantity verification: RFID counts items in picker's tote (detects short/over picks)
performance: 300 lines/hour per picker with RFID verification vs. 200 lines/hour manual barcode scanning
accuracy: 99.8% pick accuracy with RFID verification vs. 97-98% without
```

### Automated Sorting and Packing Verification
```annotation
type: quality_assurance
context: RFID readers at packing stations verify order completeness before shipment
equipment: Zebra FX9600 reader integrated into packing station conveyor
packing_workflow:
  1. Picker places completed order tote on conveyor
  2. Tote passes through RFID tunnel (4 antennas surround tote from all sides)
  3. RFID readers interrogate all items in tote (read time <1 second)
  4. WMS compares read tags against order pick list
  5. Packing station display shows verification results:
     - Green: All items present, correct quantities
     - Yellow: Missing item(s) - list displayed, picker dispatched to retrieve
     - Red: Extra item(s) - list displayed, packer removes and returns to stock
  6. Once verified, packer boxes items and applies shipping label
  7. Packed box passes through exit RFID portal (final verification before truck loading)
error_prevention: RFID verification catches 99% of picking errors before shipment (vs. 60-70% with manual audits)
customer_satisfaction: Shipping accuracy 99.9%, reduces returns and customer complaints by 50%
```

### Real-Time Inventory Deduction and Replenishment Triggers
```annotation
type: inventory_management
context: RFID picks automatically update inventory levels, trigger replenishment when low
equipment: WMS with perpetual inventory module, min/max replenishment logic
inventory_deduction_workflow:
  1. Picker scans items with RFID reader during pick
  2. RFID middleware sends item EPCs to WMS in real-time
  3. WMS decrements inventory by SKU and location
  4. If bin quantity falls below minimum threshold, replenishment task generated
  5. Replenishment picker directed to reserve location to retrieve full case
  6. Picker moves case from reserve to forward pick location
  7. RFID readers confirm replenishment complete, forward pick bin refilled
min_max_thresholds:
  - High-velocity items: Min = 2 days supply, Max = 5 days supply
  - Medium-velocity: Min = 5 days supply, Max = 15 days supply
  - Low-velocity: Min = 15 days supply, Max = 90 days supply
benefits: Zero stockouts in forward pick (99.5% in-stock availability), optimized inventory levels
cycle_counting: Perpetual inventory accuracy 98%+ (vs. 95% for annual physical inventory systems)
```

## 4. Cycle Counting and Inventory Accuracy

### RFID-Based Cycle Counting Procedures
```annotation
type: inventory_verification
context: Use handheld RFID readers to perform rapid cycle counts without disrupting operations
equipment: Zebra MC3390R RFID handheld with WMS cycle count application
cycle_count_workflow:
  1. WMS generates cycle count tasks (ABC analysis: count A items weekly, B monthly, C quarterly)
  2. Counter selects location to count on handheld terminal (e.g., A-05-02-C)
  3. Counter walks to location, scans location barcode with handheld
  4. Counter triggers RFID scan (reads all tags in location)
  5. RFID reader captures all EPCs in <5 seconds (vs. 2-5 minutes manual scanning)
  6. WMS compares RFID reads to system-expected inventory
  7. Discrepancies displayed on handheld (expected 50 units, counted 48 units)
  8. Counter investigates discrepancy (physical search for missing items)
  9. Counter confirms count in WMS, inventory adjusted if necessary
performance: RFID cycle counts 10× faster than manual barcode scanning (5,000 locations/month vs. 500)
accuracy_improvement: Inventory accuracy improves from 92% to 99.5% after RFID cycle counting deployment
root_cause_analysis: WMS tracks discrepancy reasons (picking errors, theft, tag failures) for continuous improvement
```

### Inventory Reconciliation and Shrinkage Detection
```annotation
type: loss_prevention
context: Compare RFID tag reads to WMS expected inventory to identify shrinkage
equipment: Fixed RFID readers at warehouse exit points, RFID middleware with exception reporting
shrinkage_detection_workflow:
  1. RFID readers continuously monitor exit portals (dock doors, personnel doors)
  2. Middleware logs all tags passing through exit readers
  3. WMS cross-references tag EPCs against authorized shipments
  4. Unauthorized tag movements trigger security alerts (tag left building without shipment record)
  5. Security personnel notified in real-time (alert on security console, email, SMS)
  6. Investigation initiated (review security camera footage, interview personnel)
  7. WMS inventory adjusted for confirmed losses, shrinkage report generated monthly
shrinkage_reduction: 40-60% reduction in inventory shrinkage after RFID exit monitoring deployment
theft_deterrence: Visible RFID readers and signage deter theft (psychological effect)
false_alarms: Tuned to <1% false alarm rate (minimize security disruptions while maintaining effectiveness)
```

### Zone Accuracy Verification and Phantom Inventory Elimination
```annotation
type: data_quality
context: Identify "phantom inventory" (system shows items present, but physically missing)
equipment: Handheld RFID readers with zone-sweeping capability
zone_verification_procedure:
  1. Select warehouse zone for verification (e.g., all of Aisle A)
  2. RFID team walks aisle with handheld readers, scanning all racks
  3. Handheld captures all EPCs physically present in zone (5-10 minutes per aisle)
  4. WMS compares RFID reads to system-expected inventory for zone
  5. Three categories of discrepancies identified:
     - Phantom inventory: System shows items, RFID does not detect (item missing or tag failed)
     - Ghost inventory: RFID detects items, system does not show (items in wrong location)
     - Misplaced inventory: RFID detects items in Zone A, system shows Zone B
  6. WMS generates exception reports for each category
  7. Personnel dispatch to investigate and correct discrepancies
frequency: Zone accuracy verification quarterly (or after major layout changes)
accuracy_target: 99.5% zone accuracy maintained through quarterly verification cycles
```

## 5. Shipping and Loading Verification

### Outbound Load Verification at Dock Doors
```annotation
type: shipping_accuracy
context: Verify correct pallets loaded on outbound trucks using RFID portal readers
equipment: Zebra FX9600 readers at dock door frames, WMS shipping module
load_verification_workflow:
  1. WMS generates pick list for truck shipment (50 pallets, multiple customer orders)
  2. Forklift operators stage pallets in dock door lane
  3. Loader drives forklift through RFID portal, carrying pallet to truck
  4. RFID readers scan pallet LPN tag as it passes through portal
  5. WMS compares scanned LPN to expected shipment manifest
  6. Loading terminal displays verification results:
     - Green: Correct pallet, load onto truck
     - Red: Wrong pallet, return to staging and retrieve correct pallet
  7. After all pallets loaded, WMS confirms shipment complete
  8. Truck departs, WMS sends ASN (Advanced Shipping Notice) to customer via EDI
shipping_accuracy: 99.9% with RFID verification vs. 95-97% with manual bill of lading checks
load_time_reduction: 20% faster loading (no manual BOL checks, instant verification)
customer_satisfaction: Fewer receiving discrepancies, faster unloading at customer dock
```

### Multi-Stop Route Verification and Segregation
```annotation
type: delivery_optimization
context: Verify pallets segregated correctly for multi-stop delivery routes
equipment: RFID readers at dock doors, route optimization software integrated with WMS
route_loading_workflow:
  1. Truck has 3 delivery stops: Customer A (10 pallets), Customer B (15 pallets), Customer C (8 pallets)
  2. WMS calculates optimal loading sequence (last stop loaded first for easy unloading)
  3. Loading terminal displays sequence: Load Customer C pallets, then B, then A
  4. As each pallet loaded, RFID portal verifies correct customer and load sequence
  5. WMS alerts if pallets loaded out of sequence (prevents unloading delays at customer sites)
  6. Final verification before trailer door closed: All pallets present, correct sequence
benefits: 30% reduction in delivery route time (optimized loading sequence)
error_prevention: Eliminates mis-loaded pallets (costly returns and re-deliveries)
compliance: Electronic proof of loading (RFID timestamps) for customer audits and claims disputes
```

## 6. Asset Tracking and Tool Management

### Returnable Container and Tote Tracking
```annotation
type: asset_management
context: Track reusable containers circulating between facilities, suppliers, customers
equipment: Metal-mount RFID tags on steel totes, fixed readers at facility entry/exit points
container_tracking_workflow:
  1. RFID tag encoded with unique tote ID applied to container
  2. Tote filled with parts, shipped to customer facility
  3. Exit RFID reader logs tote departure (timestamp, destination, contents)
  4. Customer facility entry reader logs tote arrival
  5. Customer empties tote, returns to supplier
  6. Supplier entry reader logs tote return
  7. WMS calculates tote cycle time, identifies missing totes
asset_pool_management:
  - Total tote population: 5,000 containers
  - In-transit: 1,200 (24%)
  - At customer sites: 2,300 (46%)
  - Available at supplier: 1,500 (30%)
  - Missing/lost: 50 (1%) - flagged for investigation
benefits: Reduce container purchases 30% (better utilization), eliminate manual tracking paperwork
lost_asset_recovery: Monthly reconciliation identifies customers holding excess containers, recovery initiated
```

### Production Tooling and Fixture Tracking
```annotation
type: tool_management
context: Track high-value tooling (molds, dies, jigs, fixtures) across production floor
equipment: Confidex Steelwave RFID tags (metal-mount), fixed readers at tool crib and workstations
tooling_tracking_workflow:
  1. Tool crib issues fixture to operator (scan tool ID badge and fixture RFID tag)
  2. Fixed reader at workstation detects fixture arrival (links tool to work order)
  3. Operator uses fixture for production run
  4. Fixed reader detects fixture departure from workstation
  5. Operator returns fixture to tool crib (scan-in process)
  6. Tool crib tracks fixture utilization (hours used, idle time, maintenance schedule)
pm_scheduling: Preventive maintenance triggered automatically after 1,000 hours tool usage
utilization_analysis: Identify underutilized tooling (candidates for disposal or redeployment)
loss_prevention: Real-time alerts if high-value tooling leaves facility without authorization
cost_avoidance: Reduce tooling purchases $200,000/year through better utilization and loss prevention
```

## 7. System Maintenance and Performance Monitoring

### RFID Reader Health Monitoring and Diagnostics
```annotation
type: preventive_maintenance
context: Monitor reader performance to detect failures before they impact operations
equipment: Zebra FX9600 readers with SNMP monitoring capability
health_monitoring_metrics:
  - Transmit power output: Should remain stable at configured level (±1 dBm)
  - Receive sensitivity: Monitor for degradation (indicates antenna or cable issues)
  - Temperature: Readers should operate 0-50°C ambient (thermal shutdown at 65°C)
  - Tag read rate: Baseline 200 tags/second, alert if drops below 150 tags/second
  - Network connectivity: Ping readers every 60 seconds, alert if 3 consecutive failures
diagnostics_workflow:
  1. Middleware monitors all reader health metrics in real-time
  2. If degradation detected, middleware generates alert (email to IT and operations)
  3. Technician dispatched to investigate (check antenna connections, cables, power supply)
  4. Technician performs diagnostic tests (read range verification, antenna SWR measurement)
  5. Replace failed components (antenna cables most common failure, $50 part vs. $2,000 reader)
  6. Clear alert once performance restored to baseline
pm_schedule: Quarterly inspection of all fixed readers (tighten connections, clean antennas, firmware updates)
mtbf: Mean time between failures >5 years for quality RFID readers (Zebra, Impinj)
```

### Tag Read Rate Optimization and Performance Tuning
```annotation
type: continuous_improvement
context: Monitor tag read success rates, optimize for maximum performance
equipment: Impinj ItemSense middleware with analytics dashboard
read_rate_metrics:
  - Read success rate: Percentage of tags successfully read on first pass (target 99%+)
  - Read time: Average time to read all tags in zone (target <2 seconds)
  - Missed reads: Tags present but not detected (investigate root cause)
  - False reads: Tags from adjacent zones erroneously read (adjust antenna power/orientation)
optimization_procedure:
  1. Review read rate metrics weekly (dashboard shows trends over time)
  2. Identify problem zones (e.g., Zone 5 only 95% read rate vs. 99% in other zones)
  3. Dispatch RF engineer to investigate problem zone
  4. Possible causes: Metal interference, reader power too low, antenna misaligned
  5. Implement corrective actions: Adjust transmit power, reorient antenna, add supplemental reader
  6. Re-test read rates, verify improvement to target 99%+
  7. Document configuration changes in RFID system documentation
seasonal_factors: Temperature and humidity affect RF propagation, re-tune system semi-annually
```

## 8. Integration with ERP and Supply Chain Systems

### Real-Time Inventory Visibility Across Supply Chain
```annotation
type: supply_chain_integration
context: Share RFID inventory data with suppliers and customers for collaborative planning
equipment: Cloud-based supply chain visibility platform (SAP Integrated Business Planning)
data_sharing_workflow:
  1. RFID middleware captures all inventory transactions (receipts, picks, shipments)
  2. Middleware publishes data to cloud platform via REST API
  3. Platform aggregates data across multiple facilities (10 warehouses, 30 production sites)
  4. Suppliers and customers granted access to visibility platform (role-based permissions)
  5. Suppliers monitor customer inventory levels (trigger replenishment shipments automatically)
  6. Customers track inbound shipments in real-time (plan production schedules proactively)
visibility_benefits:
  - Reduce safety stock 20-30% (real-time visibility replaces buffer inventory)
  - Improve on-time delivery 15% (proactive issue resolution vs. reactive firefighting)
  - Reduce expedited freight 40% (better planning eliminates rush orders)
data_security: Encrypt data in transit (TLS 1.3), role-based access control, audit logging
compliance: GDPR and CCPA compliant (no personal data stored, only business transactions)
```

### RFID-Enabled Vendor-Managed Inventory (VMI)
```annotation
type: supply_chain_collaboration
context: Supplier monitors customer RFID inventory, automatically replenishes when low
equipment: RFID readers at customer facility, cloud-based VMI platform
vmi_workflow:
  1. Supplier installs RFID tags on products before shipping to customer
  2. Customer facility RFID readers track product consumption in real-time
  3. VMI platform calculates inventory levels by SKU (min/max thresholds defined)
  4. When inventory drops below minimum, platform automatically generates purchase order
  5. Purchase order sent to supplier ERP via EDI (no manual customer involvement)
  6. Supplier ships replenishment, customer receives and puts away automatically
  7. Supplier invoices customer based on actual consumption (no prepayment required)
vmi_benefits:
  - Customer: Eliminate stockouts, reduce procurement labor, improve cash flow
  - Supplier: Increase sales, improve demand visibility, reduce order variability
  - Supply chain: Reduce total inventory 25%, improve service levels 10-15%
success_factors: Trust between partners, accurate RFID data (99%+ accuracy), robust IT systems
```

## Document Control
- **Version**: 1.2
- **Last Updated**: 2025-11-06
- **Approved By**: Warehouse Operations Manager, IT Director
- **Review Frequency**: Annual or upon system upgrades
- **Distribution**: All warehouse personnel, IT support, supply chain managers
