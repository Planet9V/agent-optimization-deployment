# Water Sector Research Discoveries
**Date**: 2025-11-05 13:54
**Research Phase**: Discovery and vendor analysis
**Target Sector**: Water/Wastewater Treatment and Distribution

## GitHub Repositories Found

### 1. Water Treatment Plant Automation (Darwi4)
- **URL**: https://github.com/Darwi4/Water-treatment-plant-automation-using-PLC-and-SCADA
- **Focus**: PLC and SCADA integration for water treatment
- **Components**: PLC, MPI communication cable, power supply, relays, buttons, switches, LED lights, water valves, water pumps, Arduino Uno, water detection sensors, motors, siren, air valves, air compressor
- **Value**: Real-world automation component integration

### 2. SCADA Simulator (sintax1)
- **URL**: https://github.com/sintax1/scadasim
- **Focus**: Python-based SCADA simulation
- **Features**:
  - Devices: reservoirs, valves, pumps, tanks
  - YAML configuration
  - Modbus protocol implementation
  - Water pH level monitoring
- **Value**: SCADA architecture patterns and Modbus implementation

### 3. WasteWater Library (modelica-3rdparty)
- **URL**: https://github.com/modelica-3rdparty/WasteWater
- **Focus**: Wastewater treatment plant modeling and simulation
- **Features**: Activated sludge models (ASM) of different complexity
- **Value**: Process modeling for wastewater treatment

### 4. Water Treatment Plant Model (OpenWaterAnalytics)
- **URL**: https://github.com/OpenWaterAnalytics/WTP-Model
- **Focus**: Basic water treatment plant modeling
- **Value**: Treatment process understanding

## Vendor Intelligence - Major Players

### Rockwell Automation
**Products**:
- FactoryTalk View SCADA
- PlantPAx DCS System (Release 5.40)
- ControlLogix L73 processors
- Allen-Bradley PLCs

**Water/Wastewater Capabilities**:
- PlantPAx 5.0 - integrates control and information
- FactoryTalk Batch - batch processing
- FactoryTalk Alarms - centralized alarm management
- 25-120 HMI client stations support
- Quad-screen workstations and thin clients

**Real Implementation**: Filtration systems, PLC control panels, remote I/O panels

### Siemens
**Products**:
- SIMATIC WinCC V7/V8
- WinCC/TeleControl for remote outstations
- SINAUT ST7 RTU protocol support

**Water/Wastewater Focus**:
- Freshwater treatment and distribution
- Wastewater treatment plants
- Remote pumping stations, valve stations, automated stations
- Event-controlled communication for data reduction
- Distributed client-server with redundancy

### AVEVA (formerly Wonderware)
**Products**:
- System Platform (formerly Wonderware System Platform)
- InTouch HMI

**Capabilities**:
- Supervisory, SCADA, MES, IIoT control
- Scalable from single box to multi-tiered deployment
- Contextualizes operations enterprise-wide
- Secure, real-time decision support

**Industries**: Power distribution, water control, transportation

### Schneider Electric
**Products**:
- EcoStruxure Automation Expert (Version 21.2+)
- Software-centric universal automation

**Water Features**:
- Complete automation lifecycle management
- Treatment infrastructures support
- Wastewater treatment plants
- Desalination plants
- Industrial wastewater applications

**Standards**: IEC 61499 compliant for portability and interoperability

**Real Deployment**: Bhandup Water Treatment Plant (Mumbai, India) - largest in India

### Emerson
**Products**:
- Ovation DCS (Distributed Control System)
- Compact controllers with PLC ruggedness

**Water Specialization**:
- Purposely designed for water/wastewater industries
- SCADA interface for wide-area monitoring
- Seamless PLC integration
- Advanced optimization for ammonia nitrification

**Scale**: 150+ plants managing 12B+ gallons daily (US alone)

## Protocol Intelligence

### Modbus RTU/TCP
- **Status**: Most popular protocol for process automation and SCADA
- **Origin**: Published by Modicon (1979) for PLCs
- **Characteristics**: Easy to use, open, royalty-free
- **Water Applications**: Communication between field devices and SCADA systems

### DNP3 (Distributed Network Protocol 3)
- **Primary Use**: Electric and water utilities (SCADA master to RTU)
- **Advantages over Modbus**: More robust, efficient, interoperable (higher complexity)
- **Key Features**:
  - Unsolicited reporting (slave devices send updates when values change)
  - Change events (only changed values reported)
  - Reduces overall line traffic
- **Water Distribution**: Widely used for remote telemetry and control

### Additional Protocols
- **IEC 60870-5-104**: Interoperability between subsystems
- **IEC 61850**: Critical infrastructure management
- **BACnet**: Building systems integration
- **HART**: Instrumentation communication

## Equipment Types Identified

### Remote Terminal Units (RTUs)
- Data collection from sensors (flow rates, pressure, chemical levels, water quality)
- Remote pumping station control
- Valve station automation
- SINAUT ST7 (Siemens)

### Programmable Logic Controllers (PLCs)
- Allen-Bradley ControlLogix L73 (Rockwell)
- Various Siemens SIMATIC controllers
- Compact Ovation controllers (Emerson)

### SCADA Components
- HMI software (FactoryTalk View, WinCC, System Platform)
- Historian systems for tag history
- Visualization software
- Central gateway servers for multi-site operations

### Instrumentation
- Flow meters
- Pressure sensors
- Chemical analyzers (chlorine, pH)
- Water quality monitors
- Level sensors (tanks, reservoirs)

## Architecture Patterns Discovered

### ISA-95 Hierarchy (5 Layers)
Referenced in water/wastewater SCADA implementations:
- Level 0: Physical process (pumps, valves, tanks)
- Level 1: Sensing and manipulation (sensors, actuators)
- Level 2: Monitoring and supervision (PLCs, RTUs)
- Level 3: Workflow and operations (SCADA/HMI)
- Level 4: Business planning and logistics (ERP)

### System Topologies
- **Single Server**: All functionality on one server (small installations)
- **Client-Server**: Distributed architecture with redundancy
- **Multi-Tiered**: Enterprise deployments spanning multiple sites
- **Remote Telemetry**: Central SCADA with distributed RTUs/PLCs

## Security Intelligence

### Known Vulnerabilities
- **ICONICS SCADA Suite** (2024):
  - CVE-2024-7587: Incorrect default permissions (GenBroker32)
  - CVE-2024-8299, CVE-2024-9852: Uncontrolled search path elements
  - CVE-2024-8300: Dead code vulnerability
  - Impact: Water and wastewater sector installations globally

- **Unitronics Vision™ PLC**:
  - Password recovery in plaintext
  - Used in Aliquippa, PA attack (November 2023)

### Major Incidents

**2021 - Oldsmar, Florida**:
- Initial report: Remote access via TeamViewer
- Sodium hydroxide adjusted from 100 PPM to 11,100 PPM
- Vulnerabilities: Windows 7, shared passwords, no firewall, direct internet connection
- 2023 Update: FBI investigation inconclusive, may have been employee error

**2023 - Aliquippa, Pennsylvania**:
- Pro-Iran group "Cyber Av3ngers"
- Targeted Israeli-made equipment
- Critical infrastructure focus

**2023 - County Mayo, Ireland**:
- Internet-connected pressure controller compromised
- 160 households without water for 2 days

**2024 - Texas Multiple Facilities**:
- Videos posted showing remote SCADA access
- Arbitrary adjustment of settings and controls

**2024 - Southern Water, UK**:
- Black Basta ransomware attack
- Millions in damages

### Common Attack Vectors
- Internet-exposed OT assets with default credentials
- Unpatched systems
- Remote access software (TeamViewer)
- Legacy operating systems (Windows 7)
- Lack of network segmentation/firewalls

## Standards and Regulations

### EPA Guidelines
- EPA 817-B-23-001 (March 2023, Revised August 2024)
- Cybersecurity guidance for drinking water and wastewater systems

### Industry Standards
- AWWA (American Water Works Association)
- Safe Drinking Water Act
- ISA-95 (Automation hierarchy)
- IEC 61499 (Automation portability)
- IEC 60870-5-104, IEC 61850 (Interoperability)

## Key Findings Summary

1. **Vendor Consolidation**: 5 major vendors dominate (Rockwell, Siemens, AVEVA, Schneider, Emerson)
2. **Protocol Standards**: Modbus and DNP3 are industry standard for water SCADA
3. **Security Posture**: Critical vulnerabilities in legacy systems, internet-exposed assets
4. **Scale of Deployment**: Hundreds of thousands of installations globally
5. **Integration Complexity**: Multi-vendor, multi-protocol environments common
6. **Remote Operations**: Wide-area monitoring with distributed RTUs/PLCs standard
7. **Threat Landscape**: Nation-state actors, ransomware, and insider threats active

## Research Gaps to Address

1. Specific water quality monitoring protocols (HART details)
2. BACnet integration with water treatment HVAC systems
3. Detailed procedure documentation for treatment plant startups
4. SCADA maintenance best practices specific to water sector
5. Additional CVE details for water-specific vulnerabilities
6. Water distribution network topology patterns
7. Pump station control strategies
