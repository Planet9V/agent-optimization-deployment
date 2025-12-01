# GitHub Aviation ATC & Surveillance Systems Research

**Research Date**: 2025-11-05
**Scope**: Air Traffic Control systems, aviation surveillance radar, flight management, and ADS-B tracking
**Repositories Analyzed**: 6

---

## 1. VATGER ATCISS - Virtual Air Traffic Control Information Support System

**Repository**: https://github.com/vatger/atciss
**Stars**: 10 | **Language**: TypeScript | **Last Updated**: 2025-11-05

### Description
ATCISS (Air Traffic Control Information Support System) is a replica implementation of the real DFS (Deutsche Flugsicherung) ATCISS system used in German airspace. Designed for VATSIM network controllers.

### Key Features
- Map-based aircraft tracking interface
- ATIS/AFSF automation
- Aircraft data display
- NOTAM management
- Letter of Agreement (LOA) tracking
- Real-time data from VATSIM network

### Technology Stack
- **Backend**: Python with Poetry packaging
- **Frontend**: Node.js/TypeScript/React
- **Infrastructure**: Docker, Nix Flakes, docker-compose
- **Database**: PostgreSQL (uses Alembic migrations)
- **Workers**: Task scheduler and async worker processes

### Vendors/Standards Referenced
- **VATSIM**: Virtual Air Traffic Simulation Network
- **DFS**: Deutsche Flugsicherung (German Air Navigation Services)

### Topics
- ATC (Air Traffic Control)
- Flight simulation
- VATSIM integration

---

## 2. pyModeS - Python ADS-B/Mode-S Decoder

**Repository**: https://github.com/junzis/pyModeS
**Stars**: 616 | **Language**: Python | **Last Updated**: 2025-07-09

### Description
Python library for decoding Mode-S surveillance messages including ADS-B. Developed by TU Delft CNS/ATM research group.

### Protocol Support
**Mode-S Message Types**:
- **DF4/DF20**: Altitude code reporting
- **DF5/DF21**: Identity code (squawk code)
- **DF17/DF18**: ADS-B automatic surveillance

**ADS-B Type Codes**:
- **TC 1-4 (BDS 0,8)**: Aircraft identification and category
- **TC 5-8 (BDS 0,6)**: Surface position
- **TC 9-18 (BDS 0,5)**: Airborne position
- **TC 19 (BDS 0,9)**: Airborne velocity
- **TC 28-31 (BDS 6,x)**: Status and operational data

**Mode-S Comm-B (DF20/DF21)**:
- **BDS 1,0**: Data link capability
- **BDS 2,0**: Aircraft identification
- **BDS 3,0**: ACAS active resolution
- **BDS 4,0**: Selected vertical intention
- **BDS 4,4/4,5**: Meteorological reports (MRAR/MHR)
- **BDS 5,0**: Track and turn report
- **BDS 6,0**: Heading and speed report

### Standards Implemented
- **Mode-S**: Secondary surveillance radar protocol (ICAO Annex 10)
- **ADS-B**: Automatic Dependent Surveillance-Broadcast
- **ACAS**: Airborne Collision Avoidance System
- **MRAR**: Meteorological Routine Air Report
- **MHR**: Meteorological Hazard Report

### Hardware Integration
- **RTL-SDR**: Software-defined radio receivers
- **TCP/IP**: Network data streams (raw, beast, skysense formats)

### Key Capabilities
- Real-time decoding and display (`modeslive` tool)
- Position calculation (CPR - Compact Position Reporting)
- Velocity vector computation
- Meteorological data extraction
- CRC validation and ICAO address inference

### Citation
Published in IEEE Transactions on Intelligent Transportation Systems (2019)

---

## 3. FlightAirMap - Multi-Source Aviation Tracking Platform

**Repository**: https://github.com/Ysurac/FlightAirMap
**Stars**: 564 | **Language**: SQL/PHP | **Last Updated**: 2024-06-02

### Description
Comprehensive aviation tracking platform supporting aircraft, ships, and ground trackers. Fork of Barrie Spotter with extensive enhancements.

### Data Source Support

**Aviation**:
- **ADS-B SBS1 format**: dump1090, Radarcape, aircraftlist.json
- **ACARS**: Aircraft Communications Addressing and Reporting System (via acarsdec)
- **APRS**: Automatic Packet Reporting System (glidernet)
- **Virtual Airlines**: IVAO whazzup.txt, VATSIM data, phpvms, VAM

**Maritime**:
- **AIS NMEA**: Automatic Identification System for ships (AISHub, rtl_ais)

**Ground Tracking**:
- **APRS**: Vehicle/phone/tracker positioning

### Visualization Platforms
**2D Maps**: OpenStreetMap, Mapbox, MapQuest, Yandex, Bing, Google
**3D Maps**: OpenStreetMap, Bing with Cesium engine

### Key Features
- Real-time tracking on 2D/3D maps
- Airspace visualization
- METAR weather integration
- NOTAM display
- Statistics generation (aircraft types, airlines, routes, busy periods)
- Database search by aircraft/airline/airport
- Satellite tracking support
- Seasonal tracking (Santa Claus flight in December)

### System Requirements
- **PHP**: 5.4+ (5.5.1+ recommended)
- **Database**: MySQL 5.6.1+, MariaDB, or PostgreSQL with PostGIS
- **Web Server**: Apache 2.0+, Nginx, or Lighttpd

### Topics
- 3D mapping with Cesium
- ACARS, ADS-B, SBS, Mode-S
- Glider networks (glidernet)
- IVAO, VATSIM (virtual airlines)
- METAR, NOTAM aviation data
- Ship and tracker support

### Vendor Integrations
- **FlightGear**: Flight simulator
- **IVAO/VATSIM**: Virtual airline networks
- **phpvms/VAM**: Virtual Airlines Manager
- **Open Glider Network**: Glider tracking
- **AISHub**: Maritime AIS aggregation

---

## 4. SDR-Enthusiasts ADS-B Guide

**Repository**: https://github.com/sdr-enthusiasts/gitbook-adsb-guide
**Stars**: 161 | **Last Updated**: 2025-10-25

### Description
Comprehensive Docker-based guide for ADS-B reception, decoding, and data sharing with aggregators.

### Equipment Referenced
- **SDR Hardware**: Software-Defined Radio receivers
- **Docker containers**: Containerized ADS-B stack

### Aggregator Networks

**Non-Profit**:
- ADSBHub
- adsb.exposed, adsb.fi, ADSB.lol
- Airplanes.live
- OpenSky Network
- Planespotters.net
- Plane Watch
- The Air Traffic
- HPRadar
- Fly Italy ADSB

**Commercial**:
- FlightAware (piaware)
- FlightRadar24
- Plane Finder
- Airnav Radar
- radarvirtuel.com
- AV Delphi
- ADS-B Exchange

### Documentation Platform
GitBook: https://sdr-enthusiasts.gitbook.io/ads-b/

### License
Creative Commons BY-NC 4.0

---

## 5. rs1090 - Rust/Python/WASM Mode-S Decoder

**Repository**: https://github.com/xoolive/rs1090
**Stars**: 38 | **Language**: Rust | **Last Updated**: 2025-11-03

### Description
Multi-platform decoder for Mode-S, ADS-B, and FLARM signals with Rust, Python, and WebAssembly bindings.

### Protocol Support
- **Mode-S**: Secondary surveillance radar
- **ADS-B**: Automatic Dependent Surveillance-Broadcast
- **FLARM**: Flight Alarm collision avoidance system (gliders/light aircraft)

### Unique Feature
Cross-platform implementation with WebAssembly support for browser-based decoding.

### Topics
- Aircraft tracking
- dump1090 compatibility
- Mode-S and ADS-B decoding

---

## 6. OpenADSB Camera Overlay

**Repository**: https://github.com/v0l/adsb-overlay
**Stars**: 30 | **Language**: JavaScript | **Last Updated**: 2023-07-12

### Description
Real-time camera overlay system for displaying aircraft information over video feeds.

### Use Case
Visual aircraft identification by overlaying ADS-B data on camera footage, useful for:
- Aviation photography
- Airfield monitoring
- Educational demonstrations

---

## Key Protocols & Standards Identified

### Air Traffic Control
- **Mode-S**: ICAO secondary surveillance radar (SSR) protocol
- **ADS-B**: Automatic position broadcasting (1090 MHz ES, 978 MHz UAT)
- **ACARS**: Aircraft-to-ground text messaging
- **FLARM**: Collision avoidance for general aviation
- **ACAS**: Airborne Collision Avoidance System

### Data Formats
- **SBS-1/BaseStation**: ASCII text format for ADS-B data
- **Beast Binary**: High-efficiency binary ADS-B format
- **CPR**: Compact Position Reporting encoding
- **NMEA**: Maritime standard (AIS for ships)
- **APRS**: Packet radio tracking protocol

### Standards Bodies
- **ICAO**: International Civil Aviation Organization (Annex 10)
- **IEEE**: Intelligent Transportation Systems standards

---

## Vendor Ecosystem

### Hardware Vendors
- **RTL-SDR**: Low-cost software-defined radio dongles
- **Radarcape**: Professional ADS-B receiver
- **FlightAware**: PiAware receiver hardware

### Software Platforms
- **dump1090**: Popular open-source ADS-B decoder (mutability fork)
- **acarsdec**: ACARS message decoder
- **rtl_ais**: Maritime AIS decoder

### Network Providers
- **VATSIM/IVAO**: Virtual air traffic simulation networks
- **DFS**: German Air Navigation Services
- **OpenSky Network**: Research ADS-B network

### Integration Systems
- **phpvms**: Virtual airline management
- **FlightGear**: Open-source flight simulator
- **Cesium**: 3D mapping engine

---

## Architecture Patterns Observed

### Data Collection
1. **SDR Receiver** → dump1090/rtl-sdr
2. **Network Source** → TCP/UDP streams
3. **API Integration** → VATSIM/IVAO data feeds

### Processing Pipeline
1. **Raw RF Signal** → Mode-S/ADS-B decoding
2. **Message Validation** → CRC checking, BDS inference
3. **Position Calculation** → CPR decoding, lat/lon derivation
4. **Data Enrichment** → Aircraft database lookup, route info

### Distribution
1. **Local Visualization** → Web dashboards (2D/3D maps)
2. **Aggregator Feeding** → Multiple services simultaneously
3. **API Endpoints** → JSON/XML data provision
4. **Database Storage** → Historical tracking and statistics

---

## Key Equipment Types

### Receivers
- RTL-SDR dongles (low-cost SDR)
- Radarcape (professional ADS-B receiver)
- Mode-S Beast (high-performance decoder)

### Antennas
- 1090 MHz for Mode-S/ADS-B
- 978 MHz for UAT (USA)
- 131.x MHz for ACARS

### Computing
- Raspberry Pi (common platform)
- Docker containers (deployment standard)
- Cloud servers (aggregation and processing)

---

## Research Findings Summary

**Total Repositories**: 6 analyzed
**Primary Protocols**: Mode-S, ADS-B, ACARS, FLARM, AIS, APRS
**Key Standards**: ICAO Annex 10, IEEE ITS
**Hardware Types**: SDR receivers, professional ADS-B equipment
**Software Stack**: Python, Rust, TypeScript, PHP, Docker
**Aggregator Networks**: 20+ identified (non-profit and commercial)

**Most Active Areas**:
1. Open-source ADS-B decoding and visualization
2. Multi-source data aggregation (aviation + maritime + ground)
3. Virtual airline simulation and tracking
4. Research-focused surveillance data collection

**Emerging Trends**:
- WebAssembly for browser-based decoding
- Docker containerization for easy deployment
- Multi-protocol support (aviation + maritime + ground)
- 3D visualization with Cesium
- Community-driven aggregator networks

---

**Research Status**: COMPLETE
**Evidence**: 6 repositories analyzed with full README extraction
**Deliverable**: Vendor names, protocols, equipment types, and standards documented
