# Power Generation Facility Architecture

**Document Type**: Physical Infrastructure Architecture
**Facility Classification**: Combined Cycle Gas Turbine (CCGT) Power Plant
**Generation Capacity**: 840 MW (3 x 280 MW Units)
**Creation Date**: 2025-11-05
**Architecture Standard**: IEEE 1686-2013, IEC 61850 Ed 2.1

## Section 1: Physical Layout and Generation Infrastructure

### Primary Generation Zone Architecture

The facility implements a three-unit combined cycle configuration with GE 7HA.02 gas turbines (each 280 MW ISO rating) coupled to Mitsubishi Power M701F5 heat recovery steam generators. Each gas turbine drives an ABB THDF-700-4P generator producing 18 kV three-phase power at 3600 RPM synchronous speed. The generator step-up transformers (GSU) are Siemens RESIBLOC 4ET6 units rated 330 MVA with 18kV/230kV voltage transformation and impedance of 12.5% on transformer base.

The HRSG architecture employs triple-pressure reheat configuration with Alstom HSST-3PR units featuring high-pressure drum operating at 1800 PSIG, intermediate-pressure at 450 PSIG, and low-pressure at 45 PSIG. Steam turbine package is Siemens SST-900 extraction condensing turbine rated 340 MW at 3600 RPM driving a Siemens SGen5-1200A hydrogen-cooled generator at 0.85 power factor. Condenser system uses SPX Marley NC-8608 mechanical draft cooling towers with 85,000 GPM circulation water flow.

### Electrical Switchyard Architecture

The 230 kV switchyard implements GIS (Gas Insulated Switchgear) configuration using ABB ELK-14 units with SF6 insulation rated 245 kV maximum voltage and 4000 A continuous current. Ring bus topology provides N+1 redundancy with six circuit breaker positions: three generator breakers (one per unit), two transmission line breakers connecting to regional grid via 230 kV lines, and one transformer breaker for station service transformer. ABB REF615 bay protection relays implement IEEE C37.118.1-2011 synchrophasor measurement with 1 ms timestamp accuracy.

Generator circuit breakers are ABB HEC-7 SF6 units rated 40 kA interrupting capacity with 50 ms operating time. Current transformers are ABB TYP 1251 optical CT with 0.2% accuracy class for metering and 5P20 for protection. Voltage transformers are ABB VGS-245 capacitive divider type with 0.5% accuracy. Bus differential protection uses SEL-487E multifunction relay with restraint characteristics set to 25% slope for external fault stability.

### Medium Voltage Distribution Architecture

The 13.8 kV auxiliary power system supplies balance-of-plant loads through dual Schneider Electric Masterbloc GM switchgear rated 2000 A continuous with 40 kA RMS symmetric fault current capability. Station service transformers are two ABB RESIBLOC units rated 25/30 MVA ONAN/ONAF with 230kV/13.8kV transformation and vector group YNd11. Load tap changer is Maschinenfabrik Reinhausen OILTAP M providing ±10% voltage regulation in 1.25% steps.

Critical auxiliary loads including boiler feed pumps (three Sulzer HPK-BB4 units at 1800 HP each), condensate pumps (four KSB Movitec VS-60/14 at 500 HP each), and circulating water pumps (six Flowserve 60LVF units at 2500 HP each) receive power through separate 13.8 kV feeders with SEL-751A feeder protection relays. Motor control centers are Schneider Electric Okken MCC rated 600V with solid-state overload relays and Altistart 48 soft starters for motors above 100 HP.

### Low Voltage Essential Systems

Uninterruptible power supply architecture employs redundant 480V UPS systems with Eaton 9395 modular UPS units (N+1 configuration, 225 kVA per module) feeding critical control systems. Battery banks are C&D Technologies UPS12-540MR valve-regulated lead-acid cells providing 30 minutes backup at full load. Automatic transfer switches are ASCO 7000 Series rated 4000 A with sub-cycle transfer time (less than 4 ms) to emergency diesel generator sets.

Emergency power generation uses three Caterpillar 3516C diesel gensets rated 2000 kW continuous at 480V three-phase, synchronized via Woodward easYgen-3500XT controllers implementing droop control with 4% speed regulation and load sharing accuracy within 2%. Paralleling switchgear is Russelectric RLSC-8004 with redundant control modules and integral protection relays meeting IEEE C37.90.1 surge withstand capability.

## Section 2: Control Room and SCADA Architecture

### Primary Control System Infrastructure

The main control room deploys ABB Ability System 800xA DCS architecture with redundant controllers (AC800M High Integrity platform) executing control logic at 100 ms scan cycle. Controller configuration includes eight pairs of redundant CPUs with dual 1 Gbps Ethernet interfaces on HSE (High Speed Ethernet) backbone implementing IEC 61784-1 CPF 3/2 PROFINET protocol. Process I/O connects via PROFIBUS-DP remote I/O stations (ABB S800 modules) with 12 ms bus cycle time and DP-V1 acyclic communication for diagnostics.

Operator workstations deploy six Advantech DLoG DPC-8315 industrial PCs with dual 27-inch displays running ABB Compact 800xA HMI software at Microsoft Windows 10 IoT Enterprise. Workstation redundancy implements 1+1 hot standby with less than 500 ms failover time via TCP/IP heartbeat monitoring. Engineering stations use identical hardware with additional ABB Control Builder M Professional software for online configuration changes and logic debugging.

### SCADA Master Station Architecture

Wide-area SCADA functionality deploys GE Grid Solutions eFAST Master Station on Dell PowerEdge R740xd servers (dual Intel Xeon Gold 6248R processors, 256 GB RAM, RAID-10 storage) with Real-Time Database capacity of 500,000 points and 100 ms update rate. Redundant server pair operates in hot standby mode with Oracle Real Application Clusters (RAC) 19c database for historical data persistence. SCADA protocols include DNP3 Serial/IP (IEEE 1815-2012), IEC 60870-5-104 for substation communication, and Modbus TCP for legacy RTU integration.

Front-end processors utilize Moxa ioLogik E2242 smart Ethernet I/O units with embedded DNP3 Level 2 slave capability processing 32 digital inputs, 16 digital outputs, and 8 analog inputs at 1-second scan intervals. Protocol gateway functions deploy RuggedCom RX1500 industrial routers implementing DNP3-to-IEC 61850 GOOSE translation with less than 10 ms latency for critical trip signals. SCADA network architecture separates process control LAN (PC-LAN) and corporate network via Cisco Firepower 2130 industrial security appliance implementing deep packet inspection at line rate (1 Gbps).

### Advanced Metering and Data Acquisition

Revenue metering deploys Schneider Electric ION9000 power quality meters at generator terminals and transmission interconnection points, meeting ANSI C12.20 Class 0.2 accuracy for active energy and Class 0.5 for reactive energy. Meters communicate via IEC 61850-8-1 MMS protocol over substation LAN with 1-second demand interval synchronized to IRIG-B timecode from Meinberg LANTIME M3000 GPS clock providing 100 ns UTC synchronization accuracy.

Environmental monitoring integrates Siemens ULTRAMAT 23 continuous emissions monitoring systems (CEMS) measuring NOx, CO, and O2 concentrations with 2% full-scale accuracy, communicating via Modbus RTU to DCS. Stack flow measurement uses Ametek 8800 Series flow monitors with transit-time ultrasonic technology providing ±2% velocity accuracy. Ambient weather station Vaisala WXT536 measures temperature, humidity, pressure, precipitation, and wind speed/direction with data logging at 10-second intervals.

### Historian and Analytics Platform

Process data historian implements OSIsoft PI System AF Server 2018 SP3 on Dell PowerEdge R640 with PI Data Archive storing 250,000 tags at 1-second intervals, compressed storage achieving 10:1 ratio via swinging door compression algorithm. Asset Framework (PI AF) models equipment hierarchy with 1,200 elements representing turbines, generators, HRSGs, and auxiliary systems. PI Vision 2020 provides web-based trending and KPI dashboards accessible via HTML5 browsers with responsive design for mobile operations.

Advanced analytics deploy AspenTech Aspen Mtell predictive maintenance agents analyzing 5,000 sensor streams for anomaly detection using machine learning algorithms trained on 18 months operational history. Alert generation triggers on statistical deviation exceeding three standard deviations with 95% confidence interval. Performance monitoring implements EPRI CTAP (Cycle Thermal Analysis Program) calculating real-time heat rate, turbine efficiency, and HRSG effectiveness with ±0.5% accuracy compared to design values.

## Section 3: Equipment Topology and Asset Hierarchy

### Turbine-Generator Package Architecture

Each gas turbine package integrates GE Mark VIe control system with triple-modular redundant (TMR) controllers processing 3,500 I/O points including EGT (Exhaust Gas Temperature) thermocouples (24 per turbine), vibration sensors (Bently Nevada 3300 XL 8mm proximity probes at eight bearing locations), and combustion dynamics sensors (Kistler 601CAA piezoelectric pressure transducers). Protection functions execute in hardware-based logic with less than 3 ms response time for critical trips including overspeed (109% rated), high vibration (10 mils peak-to-peak), and high exhaust temperature (650°C).

Generator protection implements Schweitzer Engineering Laboratories SEL-400G multifunction relay with 87G differential (dual restraint characteristics), 51V voltage-controlled overcurrent, 32 directional power, and 81 frequency protection elements. Generator neutral grounding uses high-resistance grounding through NGR-120 resistor (120 ohms, 8.5 A continuous) with SEL-751A ground fault relay detecting 5 A minimum fault current. Generator hydrogen cooling system maintains 75 PSIG pressure with Purity Electronics PHD-1 hydrogen purity analyzer ensuring 98% minimum purity to prevent combustion risk.

### Heat Recovery Steam Generator Configuration

Each HRSG implements three-pressure reheat design with Alstom DCS-3000 drum level control using three-element (steam flow, feedwater flow, drum level) algorithms with Rosemount 3051S pressure transmitters (±0.065% URL accuracy) and Emerson 5408 non-contact radar level transmitters (±2 mm accuracy). High-pressure feedwater pump is Sulzer HPK-BB4 barrel-type pump (1800 HP, 3,600 RPM) with capacity of 1,200 GPM at 2,850 PSIG discharge pressure, controlled by Siemens SIMATIC ET200SP remote I/O executing cascade flow control with 100 ms loop update.

HRSG bypass systems include high-pressure bypass (Pentair Yarway 55000 Series, 24-inch diameter, Cv=3500) and low-pressure bypass (Pentair Yarway 55000 Series, 30-inch diameter, Cv=6800) with pneumatic actuators (Fisher 657 size 70 diaphragm actuators) providing 30-second stroke time. Attemperators control bypass steam temperature to 650°F using feedwater spray with Spirax Sarco PN6000 spray control valves modulating flow from 0-15,000 lb/hr based on downstream RTD measurements (Rosemount 3144P temperature transmitters with ±0.5°F accuracy).

### Balance of Plant Equipment Network

Condensate and feedwater systems deploy distributed control with DeviceNet industrial network (250 Kbps) connecting Allen-Bradley PowerFlex 755 variable frequency drives controlling pump speeds from 50-100% rated. Network architecture implements producer-consumer messaging model with 20 ms packet time for speed reference updates. Pump performance monitoring uses Emerson Roxar 2600 multiphase flow meters providing simultaneous measurement of flow rate (±2% accuracy), density, and temperature at 1-second update intervals.

Water treatment systems integrate GE Betz plant chemistry analyzers including AquaSENSOR AS950 (measuring conductivity, pH, sodium, silica) with outputs to DCS via HART protocol over 4-20 mA loops. Condensate polishing demineralizers are Graver Technologies GSX50 units with 50,000 gallon resin capacity regenerated on cation conductivity exceeding 0.2 µS/cm. Chemical injection pumps (Milton Roy mROY series metering pumps) dose ammonia, phosphate, and hydrazine with ±1% accuracy under DCS control via Modbus RTU communication.

### Auxiliary Cooling Systems Architecture

Cooling tower systems deploy SPX Marley NC-8608 mechanical draft design with six cells (each 14,200 GPM capacity), VFD-controlled fans (Toshiba TOSVERT VF-AS3 drives, 250 HP motors), and automated chemistry treatment systems. Level control uses Siemens SITRANS LR560 radar transmitters with 4-20 mA output controlling makeup water valves (Pentair Keystone F120 butterfly valves with electric actuators). Blowdown control implements conductivity-based algorithms maintaining 4.0 cycles of concentration using Endress+Hauser Liquiline CM448 conductivity analyzer with ±0.5% measured value accuracy.

Closed cooling water systems for generator hydrogen coolers and lube oil coolers use plate-and-frame heat exchangers (Alfa Laval M15-BFM) with automated temperature control modulating cooling water flow via Belimo EQM Series energy valve actuators. Primary circulation pumps (Grundfos CR95-2, 200 HP) operate under variable speed control maintaining 55°F supply temperature with ±2°F deadband. Expansion tanks (850 gallon ASME Section VIII vessels) maintain 20 PSIG static pressure with nitrogen blanketing preventing oxygen ingress.

## Section 4: Industrial Network Architecture and Cybersecurity Zones

### Purdue Model Implementation

Network architecture implements IEC 62443-3-3 zone and conduit model with five security levels. Level 0 (Process Control) includes field devices connecting via PROFIBUS-DP (12 Mbps), Foundation Fieldbus H1 (31.25 Kbps), and EtherNet/IP industrial protocols. Level 1 (Basic Control) deploys ABB AC800M controllers and GE Mark VIe systems on redundant HSE network (1 Gbps full-duplex) with Cisco Industrial Ethernet 4010 switches implementing RSTP (Rapid Spanning Tree Protocol) for less than 50 ms failover time.

Level 2 (Supervisory Control) network segregates DCS operator stations, engineering workstations, and SCADA servers on dedicated VLAN (VLAN 10) with Cisco Catalyst IE-3400 industrial switches (24 ports Gigabit Ethernet, ruggedized -40°C to +75°C operation). Level 3 (Operations Management) integrates historian, MES (Manufacturing Execution System), and plant information management on separate VLAN (VLAN 20) with controlled access via Palo Alto PA-3260 firewall implementing application-layer inspection. Level 4 (Enterprise Network) connects to corporate WAN through DMZ architecture with dual firewalls and data diode (Owl Cyber Defense OPDS-1000) enforcing unidirectional data flow for sensitive operational data.

### Process Control Network Redundancy

Primary control network deploys redundant ring topology using Hirschmann GREYHOUND Gigabit switches (GRS1042 Series) with HiOS operating system implementing proprietary HiPER-Ring protocol achieving less than 10 ms recovery time for single link failure. Network backbone utilizes single-mode fiber optic cabling (Corning InfiniCor ClearCurve) supporting 10 km maximum distance between substations with LC duplex connectors and -3 dB maximum insertion loss. Network timing synchronizes to IEEE 1588 PTPv2 (Precision Time Protocol) grandmaster clock providing nanosecond-level synchronization for sampled values and GOOSE messaging.

Controller-to-controller communication implements real-time Ethernet protocols including PROFINET IRT (Isochronous Real-Time) with 1 ms cycle time for critical control loops and 100 ms for non-critical loops. IEC 61850-8-1 GOOSE (Generic Object-Oriented Substation Event) messages transmit binary status (breaker positions, protection trips) with 4 ms maximum latency requirement meeting SIL 2 (Safety Integrity Level 2) certification per IEC 61508. Sampled Values (IEC 61850-9-2 LE) transmit current and voltage measurements at 4,800 samples per second (80 samples per power cycle) for merging unit integration.

### Cybersecurity Architecture and Defense-in-Depth

Perimeter defense implements Fortinet FortiGate 1800F NGFW (Next-Generation Firewall) with 2.5 Tbps threat protection throughput, IPS (Intrusion Prevention System) signatures updated hourly, and SSL deep packet inspection for encrypted traffic. DMZ architecture deploys dual-homed servers (PI System Historian, MES interface, HMI Web Server) with separate network interfaces for control network (trusted zone) and corporate network (untrusted zone). Cisco ISE (Identity Services Engine) 3595 provides 802.1X authentication for network access control with MAC address whitelisting for industrial devices lacking 802.1X supplicant capability.

Industrial protocol firewall uses Tofino Xenon Security Appliance implementing stateful inspection for Modbus TCP, DNP3, and IEC 61850 protocols with deep packet inspection validating function codes, register addresses, and message structure. Application whitelisting on operator stations and engineering workstations deploys McAfee Application Control enforcing execution only of signed binaries with valid digital certificates. Vulnerability scanning uses Tenable Security Center with passive network monitoring via Nessus sensors analyzing 500,000 packets per second without impacting control system performance.

### Remote Access and Secure Connectivity

Vendor remote access architecture deploys Cisco ISA-3000 industrial security appliance implementing IPsec VPN with AES-256 encryption and RSA 2048-bit key exchange. Multi-factor authentication requires RSA SecurID hardware tokens (SID800) generating 6-digit codes synchronized with RSA Authentication Manager. Session recording uses ObserveIT Enterprise (BeyondTrust acquisition) capturing full session video, keystrokes, and file transfers for forensic analysis and compliance audit trails meeting NERC CIP-005-6 remote access logging requirements.

Wide-area communication to remote substations and renewable generation sites implements MPLS (Multi-Protocol Label Switching) VPN through regional telecommunications provider with 50 Mbps committed information rate and 99.9% availability SLA. Backup communication uses Verizon Wireless Private Network (APN) with Sierra Wireless RV50X industrial LTE routers providing 50 Mbps throughput with sub-200 ms latency for SCADA data. SD-WAN overlay uses Fortinet FortiGate SD-WAN with dynamic path selection based on latency (preferring paths under 100 ms), jitter (under 10 ms), and packet loss (under 0.1%).

### Network Monitoring and Security Information Management

Network traffic analysis deploys Cisco Stealthwatch (now Secure Network Analytics) with NetFlow v9 collection from industrial switches aggregating 10,000 flows per second. Anomaly detection uses machine learning baseline establishing normal communication patterns (source/destination IPs, port numbers, packet sizes, time-of-day patterns) with alerting on deviations exceeding three standard deviations. Protocol anomaly detection identifies malformed DNP3/Modbus packets, unexpected function codes, and scan attempts targeting SCADA ports (TCP 502, 20000, 2404).

SIEM (Security Information and Event Management) platform implements Splunk Enterprise Security aggregating logs from 350 sources including firewalls (syslog), IDS sensors (unified2 format), Windows event logs (forwarded via Splunk Universal Forwarder), and application logs from DCS/SCADA systems. Correlation rules detect multi-stage attack patterns including reconnaissance (port scanning), credential attacks (repeated authentication failures), and lateral movement (unusual SMB traffic between control network segments). SOC (Security Operations Center) integration provides 24/7 monitoring with 15-minute mean time to detect (MTTD) for critical alerts and 1-hour mean time to respond (MTTR) for confirmed incidents meeting NERC CIP-008 incident response requirements.
