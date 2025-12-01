# Fiber Optic Network Provisioning Operations

## Overview
Fiber optic network provisioning encompasses wavelength assignment, DWDM (Dense Wavelength Division Multiplexing) configuration, optical power budget calculations, and OTDR (Optical Time Domain Reflectometer) testing to deliver high-capacity, low-latency connectivity for telecommunications, internet service providers, and enterprise networks.

## Operational Procedures

### 1. Fiber Route Planning and Design
- **Path Survey and Permitting**: Physical route surveys identify conduit paths, aerial attachments, and crossing points; utility permits acquired before construction
- **Fiber Count Specification**: Single-mode fiber cables typically contain 12-864 fibers; count determined by current and 20-year forecast capacity needs
- **Splice Point Planning**: Splice locations identified every 2-4 km for regeneration; manholes or hand holes selected for accessibility
- **Protection Architecture**: Ring topologies (UPSR, BLSR/MS-SPRing) or mesh networks provide automatic failover redundancy

### 2. Wavelength Assignment and DWDM Configuration
- **ITU-T Grid Alignment**: DWDM systems use standardized wavelengths spaced 50 GHz (0.4 nm) or 100 GHz (0.8 nm) apart in C-band (1530-1565 nm)
- **Channel Planning**: Modern systems support 80-96 wavelengths per fiber pair; capacity planning allocates wavelengths to services (Internet, Ethernet, SONET/SDH)
- **Dispersion Compensation**: Chromatic dispersion accumulates over distance requiring dispersion-compensating fiber (DCF) or electronic dispersion compensation (EDC)
- **Amplifier Staging**: EDFA (Erbium-Doped Fiber Amplifiers) placed every 80-120 km to boost signal without O-E-O conversion

### 3. Optical Power Budget Calculations
- **Transmitter Power**: Typical DWDM transmitters output +3 to +10 dBm per wavelength; total DWDM system power can exceed +20 dBm
- **Fiber Attenuation**: Single-mode fiber attenuates 0.2-0.3 dB/km at 1550 nm; span loss calculated as distance × attenuation coefficient
- **Connector and Splice Loss**: Each connector adds 0.3-0.5 dB loss; fusion splices contribute 0.01-0.1 dB loss; budgets account for all inline losses
- **Receiver Sensitivity**: Typical receiver sensitivity -25 to -28 dBm; system margin 3-5 dB ensures reliable operation despite fiber aging

### 4. OTDR Testing and Characterization
- **Baseline OTDR Traces**: Optical Time Domain Reflectometer launches test pulse and measures backscatter/reflections to map fiber characteristics
- **Event Identification**: OTDR traces show splice locations, connector interfaces, fiber breaks, and macro-bending losses as signature waveforms
- **Loss Measurement**: Splice loss, connector loss, and total span loss measured and documented for acceptance testing and troubleshooting
- **Fault Location**: OTDR pinpoints fiber breaks or high-loss events within ±1 meter accuracy enabling efficient repair dispatch

### 5. Transponder and Muxponder Configuration
- **Client Interface Provisioning**: Transponders convert client signals (10GbE, 100GbE, OC-192) to DWDM wavelengths for transmission
- **Forward Error Correction (FEC)**: Enhanced FEC (eFEC, SD-FEC) corrects bit errors introduced by optical impairments extending reach without regeneration
- **Modulation Format Selection**: QPSK, 16-QAM, 64-QAM modulation schemes balance data rate versus optical reach; higher-order modulation requires better SNR
- **Coherent Detection**: Modern systems use coherent receivers with DSP enabling flexible modulation and 400G-800G per wavelength capacities

### 6. Network Element Provisioning
- **Cross-Connect Configuration**: Optical cross-connects (OXC) or reconfigurable optical add-drop multiplexers (ROADM) switch wavelengths without O-E-O conversion
- **Add-Drop Configuration**: ROADMs enable dynamic wavelength routing and wavelength-selective switching for flexible capacity allocation
- **Protection Switching**: Automatic protection switching (APS) detects fiber cuts and switches traffic to protection path within 50 ms
- **Network Management System (NMS)**: Element management systems (Cisco Evolved Programmable Network Manager, Ciena Manage Control Domain) configure and monitor DWDM equipment

### 7. Service Activation and Testing
- **Circuit Turn-Up**: End-to-end circuit tested for bit error rate (BER) <10^-12 before customer handoff; loopback tests verify bidirectional connectivity
- **Latency Measurement**: Round-trip delay measured using Y.1731 or RFC 2544 test equipment; fiber provides ~5 microseconds latency per km
- **Throughput Validation**: RFC 2544 tests confirm line rate forwarding (0% packet loss at line rate); frame sizes from 64 to 1518 bytes tested
- **SLA Baseline Establishment**: Baseline performance metrics (latency, jitter, packet loss, availability) documented for ongoing SLA monitoring

## System Integration Points

### Network Management Systems
- **FCAPS Integration**: NMS provides Fault, Configuration, Accounting, Performance, and Security management across multi-vendor optical networks
- **Alarm Correlation**: Intelligent correlation reduces alarm storms from cascade failures; root cause analysis identifies primary faults
- **Performance Monitoring**: Real-time optical power levels, pre-FEC BER, Q-factor, and chromatic dispersion tracked for proactive maintenance
- **Configuration Management**: Centralized database maintains wavelength assignments, cross-connect configurations, and equipment inventory

### OSS/BSS Integration
- **Order Management**: Service orders trigger automated provisioning workflows in optical transport management systems
- **Inventory Systems**: Fiber route database, splice records, and equipment inventory maintained in GIS-based OSS platforms
- **Capacity Planning**: Network planning tools model growth scenarios identifying when fiber exhaust requires additional cable installation
- **Trouble Ticket Integration**: Fiber outages automatically generate tickets in remedy/ServiceNow with affected services and restoration ETAs

### IP/MPLS Routers
- **Client Interface Handoff**: Optical transport delivers wavelengths to router optics modules (CFP, QSFP28, QSFP-DD) for IP traffic forwarding
- **Link Aggregation**: Multiple wavelengths bundled into LAG (Link Aggregation Group) for increased capacity and load balancing
- **Traffic Engineering**: MPLS-TE or Segment Routing steers high-priority traffic onto diverse fiber paths for resilience
- **Timing Distribution**: Precision Time Protocol (IEEE 1588) or SyncE distributed over optical transport for mobile backhaul synchronization

### SONET/SDH Legacy Systems
- **TDM Service Support**: Legacy SONET/SDH services (OC-3, OC-12, OC-48) transported transparently over DWDM wavelengths
- **SONET Ring Integration**: DWDM systems interconnect geographically separated SONET rings extending reach beyond regeneration limits
- **Subrate Grooming**: SONET add-drop multiplexers aggregate DS1/DS3 circuits into OC-48 wavelengths reducing wavelength consumption

## Regulatory Compliance

### Telecommunications Act Interconnection
- **Right-of-Way Agreements**: Fiber deployment in public rights-of-way requires municipal franchise agreements and permits
- **Pole Attachment Regulations**: FCC regulates rates and terms for attaching fiber to utility poles under Section 224 of Communications Act
- **Dig Safe Compliance**: Underground fiber routes located and marked before excavation per state "Call Before You Dig" laws
- **Railroad Crossing Permits**: Fiber crossing railroad tracks requires railroad engineering approval and compliance with railroad specifications

### Environmental and Safety Standards
- **NESC (National Electrical Safety Code)**: Aerial fiber installation clearances, pole loading, and grounding requirements
- **OSHA Fiber Optic Safety**: Proper handling of fiber scraps, laser safety (Class 1M, Class 3B), and confined space entry procedures
- **Fiber Optic Safety Standards**: IEC 60825 laser safety classifications; technicians trained on laser hazards and safe installation practices
- **Environmental Assessments**: Major fiber routes may require NEPA environmental impact assessments for federally funded projects

### Standards Compliance
- **ITU-T G.652/G.655/G.657**: Single-mode fiber specifications for various applications (standard, low water peak, bend-insensitive)
- **ITU-T G.694.1**: DWDM wavelength grid specification ensuring multi-vendor interoperability
- **IEEE 802.3**: Ethernet over fiber standards (10GBASE-LR, 100GBASE-LR4, 400GBASE-LR8) define optics and reach specifications
- **Telcordia GR-326**: Generic requirements for single-mode optical connectors ensuring reliability and performance

## Equipment and Vendors

### DWDM System Vendors
- **Ciena**: Waveserver and 6500 platforms with WaveLogic coherent optics supporting 800G per wavelength and 30+ Tbps per fiber
- **Cisco**: Network Convergence System (NCS) with integrated DWDM and IP routing for converged transport architecture
- **Infinera**: DTN-X and GX series with vertically integrated photonic integrated circuits (PIC) reducing footprint and power
- **Nokia (Alcatel-Lucent)**: 1830 Photonic Service Switch (PSS) with FlexGrid technology for software-defined optical networking

### Fiber Cable Manufacturers
- **Corning**: Market leader in optical fiber; SMF-28 Ultra single-mode fiber and ClearCurve bend-insensitive fiber widely deployed
- **Prysmian**: Comprehensive cable portfolio from indoor tight-buffer to outdoor armored cables; BendBrightXS bend-insensitive fiber
- **OFS (Furukawa)**: AllWave optical fiber and specialty fibers for submarine and ultra-long-haul applications
- **Fujikura**: High-density micro-cables and ribbon cables for metro and data center interconnect applications

### Test Equipment
- **EXFO**: FTB-4 Pro platform with OTDR, optical spectrum analyzer, chromatic dispersion, and PMD testing modules
- **Viavi (formerly JDSU)**: T-BERD/MTS test sets supporting copper, fiber, and Ethernet service activation and troubleshooting
- **Yokogawa**: AQ1200 series OTDR for fiber characterization; AQ6370 optical spectrum analyzer for DWDM channel analysis
- **JDSU/Viavi Certification Kits**: Fiber inspection microscopes and power meters for connector end-face quality inspection

### Splice and Connector Equipment
- **Fujikura**: Fusion splicers (90S, 70S series) with core alignment and automatic splice loss estimation
- **Corning**: UniCam connectors for field termination without epoxy/polish; OptiTap and OptiTip for FTTA (Fiber to the Antenna)
- **CommScope**: SYSTIMAX GigaSPEED and LazrSPEED fiber solutions for enterprise and data center applications
- **AFL (Fujikura)**: Fusion splicers, cleavers, and fiber preparation tools for outside plant construction

## Performance Metrics

### Optical Performance
- **Bit Error Rate (BER)**: Pre-FEC BER target <10^-5; post-FEC BER must achieve <10^-12 for error-free transmission
- **Optical Signal-to-Noise Ratio (OSNR)**: Minimum 15-18 dB OSNR required for 10G systems; 100G/400G coherent systems tolerate lower OSNR
- **Q-Factor**: Quality factor >15 dB indicates healthy optical link with adequate margin; degradation trend triggers proactive maintenance
- **Chromatic Dispersion**: Maintained within transponder tolerance (±800 ps/nm for 10G, tighter for 40G+); DCF compensates accumulated dispersion

### Network Availability
- **Fiber Cut Rate**: Industry average 0.3-0.5 cuts per 1000 fiber-miles annually; diverse routing reduces impact
- **Mean Time to Repair (MTTR)**: Average 2-4 hours for fiber cuts depending on accessibility and crew availability
- **Protection Switching Time**: <50 ms automatic failover for ring topologies; mesh restoration may take 100-200 ms for path computation
- **Network Availability**: Five-nines (99.999%) availability target translates to <5 minutes downtime annually

### Capacity Utilization
- **Wavelength Utilization**: Percentage of provisioned wavelengths in use; >70% indicates need for capacity expansion
- **Wavelength Exhaust Forecast**: Projected date when all wavelengths provisioned; triggers fiber cable or DWDM system augmentation
- **Spectral Efficiency**: Bits per second per Hz achieved; 400G systems achieve 4-6 bits/s/Hz using advanced modulation
- **Fiber Fill Rate**: Percentage of fibers in cable activated; dark fiber reserves maintained for rapid service turn-up

### Operational Efficiency
- **Service Provisioning Time**: Target <10 days for lit service provisioning; dark fiber may require 30-90 days for new construction
- **First-Time Installation Success**: >95% of new circuits activated without rework or repeat site visits
- **Splice Loss Average**: Fusion splices average <0.05 dB loss; excessive loss indicates contamination or poor fiber preparation
- **Connector End-Face Quality**: >98% of connectors pass IEC 61300-3-35 inspection without contamination or damage

---

**Document Control**
- **Version**: 1.0
- **Last Updated**: 2025-11-06
- **Regulatory References**: ITU-T G.652/655/694.1, IEC 60825, IEEE 802.3, Telcordia GR-326, FCC Part 76, NESC C2-2023
- **Review Cycle**: Annual
