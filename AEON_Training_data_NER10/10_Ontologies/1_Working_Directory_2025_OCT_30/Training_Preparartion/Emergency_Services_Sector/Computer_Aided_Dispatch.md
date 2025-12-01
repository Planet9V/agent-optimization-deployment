# Computer-Aided Dispatch (CAD) Systems - Emergency Services

## CAD System Overview

### Computer-Aided Dispatch (CAD) Definition
- **System Purpose**: Centralized incident management and resource dispatching for emergency services
- **Core Functions**: Call taking, incident entry, unit recommendation, dispatching, status tracking, mapping, reporting
- **User Base**: 911 telecommunicators, dispatchers, field supervisors, command staff
- **Integration Points**: 911 telephony, radio systems, AVL (Automatic Vehicle Location), RMS (Records Management), MDT (Mobile Data Terminal)
- **Database Type**: Relational database (Oracle, Microsoft SQL Server, PostgreSQL)
- **Architecture**: Client-server or web-based architecture
- **Redundancy**: Redundant servers with automatic failover
- **Geographic Information**: GIS mapping with real-time unit location
- **Performance**: <2 second response time for queries, <5 second dispatch time

## Major CAD Vendors

### Motorola Solutions PremierOne CAD
- **Product Name**: PremierOne Computer Aided Dispatch
- **Vendor**: Motorola Solutions, Inc.
- **Market Position**: Leading public safety CAD platform
- **Architecture**: Multi-tier web-based architecture
- **Database**: Microsoft SQL Server 2016/2019, Oracle 12c/19c
- **Operating System**: Windows Server 2016/2019/2022
- **Client Type**: Web browser-based (Chrome, Edge, Firefox)
- **Map Engine**: Esri ArcGIS integration, Google Maps API
- **Server Specifications**: Dual Intel Xeon processors, 64-128 GB RAM, RAID 10 storage
- **Redundancy**: N+1 server redundancy with automatic failover (<5 seconds)
- **Concurrent Users**: Supports 100-500+ concurrent users per system
- **Incident Capacity**: Handles 100,000+ incidents per year
- **Call Taking**: Integrated call taking with ANI/ALI display
- **Incident Entry**: Rapid incident entry with type-ahead search
- **Unit Recommendation**: Intelligent unit recommendation based on status, location, capability
- **AVL Integration**: Real-time vehicle location via GPS (Trimble, Motorola AVL)
- **Mapping**: Real-time GIS map with unit icons, incident symbols, routing
- **Geocoding**: Address validation and geocoding accuracy >98%
- **Routing**: Turn-by-turn routing with travel time estimation
- **Status Management**: Automatic and manual unit status updates
- **Radio Integration**: P25 radio system integration for status updates
- **Mobile Integration**: PremierOne Mobile CAD for MDTs and smartphones
- **RMS Integration**: PremierOne Records for seamless CAD-to-RMS data flow
- **Alerts**: Premise hazards, wanted persons, stolen vehicles, BOLO (Be On the Lookout)
- **Notifications**: Automatic notifications (email, SMS, pager)
- **Reporting**: Ad-hoc and scheduled reporting (Crystal Reports, SSRS)
- **NFIRS**: National Fire Incident Reporting System integration
- **NIBRS**: National Incident-Based Reporting System (FBI UCR)
- **Analytics**: PremierOne Analytics for operational intelligence
- **Training Mode**: Separate training database for dispatcher training
- **Disaster Recovery**: Hot standby disaster recovery site capability
- **Security**: Role-based access control (RBAC), CJIS compliant
- **APIs**: RESTful API for third-party integration
- **Pricing Model**: Per-position licensing (dispatchers + supervisors)
- **Implementation Time**: 12-24 months typical deployment
- **Support**: 24/7/365 technical support

### Hexagon (Intergraph) CAD
- **Product Name**: Hexagon Public Safety CAD
- **Vendor**: Hexagon Safety, Infrastructure & Geospatial (formerly Intergraph)
- **Market Position**: Major CAD vendor with strong GIS integration
- **Architecture**: Service-oriented architecture (SOA)
- **Database**: Oracle 12c/19c/21c, Microsoft SQL Server
- **Operating System**: Windows Server 2016/2019/2022, Linux (Red Hat Enterprise Linux)
- **Client Type**: Web-based thin client, Windows thick client
- **Map Engine**: Hexagon GeoMedia, Esri ArcGIS integration
- **Server Specifications**: Dual Xeon processors, 128-256 GB RAM, SAN storage
- **Redundancy**: Active-active or active-passive redundancy
- **Concurrent Users**: Scalable to 1000+ concurrent users
- **Incident Capacity**: Millions of incidents per year
- **Call Taking**: Intelligent call taking with call transfer, conferencing
- **Incident Entry**: Guided incident entry with validation
- **Unit Recommendation**: AI-based unit recommendation engine
- **AVL Integration**: Multi-vendor AVL support (Motorola, CalAmp, Trimble)
- **Mapping**: Advanced 3D mapping with oblique imagery
- **Geocoding**: High-accuracy geocoding with address correction
- **Routing**: Multi-modal routing (fastest, shortest, avoid)
- **Status Management**: Real-time status tracking with automated status changes
- **Radio Integration**: P25 radio console integration
- **Mobile CAD**: Hexagon Mobile for MDTs (Windows, Android, iOS)
- **RMS Integration**: Hexagon RMS for complete public safety suite
- **Alerts**: Comprehensive alerting with geofencing
- **Notifications**: Multi-channel notifications (email, SMS, voice, pager)
- **Reporting**: Advanced reporting with business intelligence (BI) tools
- **NFIRS**: Built-in NFIRS reporting for fire departments
- **NIBRS**: FBI NIBRS reporting compliance
- **Analytics**: Predictive analytics and data visualization
- **Cloud Deployment**: Cloud-ready architecture (Azure, AWS)
- **Disaster Recovery**: Geographic redundancy and disaster recovery
- **Security**: CJIS Security Policy compliant, encrypted data
- **APIs**: SOAP and RESTful APIs
- **Pricing Model**: Per-seat licensing
- **Implementation**: 18-30 months typical
- **Support**: 24/7 support with dedicated account team

### TriTech CentralSquare CAD
- **Product Name**: CentralSquare CAD (formerly TriTech Inform CAD)
- **Vendor**: CentralSquare Technologies
- **Market Position**: Mid-market CAD solution for municipalities
- **Architecture**: Client-server and web-based architecture
- **Database**: Microsoft SQL Server 2016/2019
- **Operating System**: Windows Server 2016/2019
- **Client Type**: Windows client, web-based client
- **Map Engine**: Esri ArcGIS, Microsoft Bing Maps
- **Server Specifications**: Intel Xeon processors, 64 GB RAM minimum
- **Redundancy**: Redundant servers with failover capability
- **Concurrent Users**: 50-300 concurrent users typical
- **Incident Capacity**: 50,000-500,000 incidents per year
- **Call Taking**: Integrated call taking module
- **Incident Entry**: Template-based incident entry
- **Unit Recommendation**: Rule-based unit recommendation
- **AVL Integration**: AVL support via third-party integration
- **Mapping**: Real-time mapping with unit tracking
- **Geocoding**: Address geocoding and validation
- **Routing**: Basic routing functionality
- **Status Management**: Unit status tracking and history
- **Radio Integration**: Integration with dispatch consoles
- **Mobile CAD**: Mobile application for field units
- **RMS Integration**: CentralSquare RMS integration
- **Alerts**: Premise alerts and officer safety warnings
- **Reporting**: Standard and custom reports
- **NFIRS**: NFIRS reporting module
- **NIBRS**: NIBRS compliance
- **Security**: CJIS compliant
- **APIs**: API for integration
- **Pricing Model**: Per-user licensing
- **Implementation**: 9-18 months
- **Support**: Business hours support with 24/7 optional

### Spillman Flex CAD
- **Product Name**: Spillman Flex CAD
- **Vendor**: Motorola Solutions (Spillman Technologies)
- **Market Position**: Popular in smaller agencies and counties
- **Architecture**: Web-based architecture
- **Database**: Microsoft SQL Server
- **Operating System**: Windows Server
- **Client Type**: Web browser (Chrome, Edge)
- **Map Engine**: Google Maps, Esri ArcGIS
- **Redundancy**: Redundant server configuration
- **Concurrent Users**: 20-200 concurrent users
- **Call Taking**: Integrated 911 call taking
- **Incident Entry**: Quick incident entry interface
- **Unit Recommendation**: Automated unit assignment
- **AVL Integration**: GPS-based AVL integration
- **Mapping**: Real-time map display
- **Status Management**: Automatic status updates
- **Mobile CAD**: Spillman Mobile for MDTs
- **RMS Integration**: Spillman Flex RMS seamless integration
- **Reporting**: Built-in reporting tools
- **Security**: CJIS Security Policy compliant
- **Pricing**: Per-user subscription model
- **Implementation**: 6-12 months
- **Support**: 24/7 support available

### Tyler Technologies New World CAD
- **Product Name**: Tyler New World Public Safety CAD
- **Vendor**: Tyler Technologies, Inc.
- **Market Position**: Established CAD vendor for state and local government
- **Architecture**: Client-server and web-based
- **Database**: Oracle 12c/19c
- **Operating System**: Windows Server, Oracle Linux
- **Client Type**: Windows thick client, web client
- **Map Engine**: Esri ArcGIS integration
- **Server Specifications**: Dual processors, 64-128 GB RAM
- **Redundancy**: Hot standby failover
- **Concurrent Users**: 100-400 concurrent users
- **Call Taking**: Call taking with ANI/ALI
- **Incident Entry**: Template-driven entry
- **Unit Recommendation**: Intelligent unit selection
- **AVL Integration**: Third-party AVL integration
- **Mapping**: GIS mapping with real-time updates
- **Mobile CAD**: New World Mobile for MDTs
- **RMS Integration**: Tyler New World RMS integration
- **Reporting**: Standard and custom reporting
- **NFIRS/NIBRS**: Compliance modules
- **Security**: CJIS compliant, role-based security
- **Cloud Option**: Tyler Cloud hosting available
- **Pricing**: Perpetual license or subscription
- **Implementation**: 12-24 months
- **Support**: 24/7 support with SLA

### Mark43 CAD
- **Product Name**: Mark43 CAD
- **Vendor**: Mark43, Inc.
- **Market Position**: Modern cloud-native CAD platform
- **Architecture**: Cloud-native SaaS (Software as a Service)
- **Database**: Cloud-based distributed database
- **Hosting**: Amazon Web Services (AWS), Microsoft Azure
- **Operating System**: Cloud infrastructure (Linux-based)
- **Client Type**: Web browser-based (Chrome, Safari, Edge)
- **Map Engine**: Mapbox, Google Maps Platform
- **Redundancy**: Multi-region redundancy built-in
- **Concurrent Users**: Unlimited scalability
- **Incident Capacity**: Cloud-scalable for any volume
- **Call Taking**: Modern call taking interface
- **Incident Entry**: Guided workflows with validation
- **Unit Recommendation**: AI-powered unit recommendation
- **AVL Integration**: Real-time GPS tracking via API
- **Mapping**: Interactive real-time mapping
- **Geocoding**: High-accuracy geocoding
- **Mobile CAD**: Mark43 Mobile (iOS, Android, ruggedized tablets)
- **RMS Integration**: Mark43 RMS fully integrated
- **Analytics**: Built-in analytics and dashboards
- **Reporting**: Customizable reports and exports
- **APIs**: Modern RESTful APIs for integration
- **Security**: SOC 2 Type 2, CJIS compliant, encryption at rest and in transit
- **Deployment**: Rapid cloud deployment (weeks, not months)
- **Updates**: Continuous updates and feature releases
- **Pricing**: SaaS subscription per user
- **Implementation**: 3-9 months typical
- **Support**: 24/7 support included

## CAD System Components

### Call Taking Module
- **ANI (Automatic Number Identification)**: Caller phone number display
- **ALI (Automatic Location Identification)**: Caller address from 911 database
- **Phase II Wireless**: Wireless caller location (latitude/longitude)
- **Call Prioritization**: Emergency vs. non-emergency call routing
- **Call Transfer**: Transfer calls to other PSAPs or agencies
- **Call Conference**: Multi-party conferencing
- **TTY/TDD**: Text telephone for hearing impaired
- **Call Recording Integration**: Automatic call recording trigger
- **Caller History**: Display of prior calls from same number/address
- **Language Line**: Interpreter service integration
- **Rapid SOS**: Enhanced wireless location from Rapid SOS Clearinghouse

### Incident Management
- **Incident Types**: Configurable incident type codes (police, fire, EMS)
- **Priority Levels**: Priority 1 (emergency) to Priority 5 (non-emergency)
- **Nature Codes**: Standardized nature of incident codes
- **Address Validation**: Real-time address validation against GIS
- **Location History**: Display of prior incidents at location
- **Common Place Names**: Landmarks and business names
- **Cross Streets**: Nearest cross streets for location verification
- **Premise Alerts**: Hazards, dangerous dogs, weapons, prior incidents
- **Linked Incidents**: Ability to link related incidents
- **Event Sequencing**: Chronological event timeline (call received, dispatched, arrived, cleared)
- **Narrative Entry**: Free-text narrative for incident details
- **Attachments**: Attach photos, documents, videos to incidents

### Unit Management
- **Unit Status**: Available, dispatched, en route, on scene, busy, out of service
- **Unit Types**: Patrol, fire engine, ambulance, supervisor, K9, SWAT
- **Unit Capabilities**: ALS (Advanced Life Support), hazmat, water rescue
- **Beat Assignment**: Geographic beat or zone assignment
- **Shift Assignment**: Unit assignment to specific shifts
- **Login/Logout**: Unit login at shift start, logout at shift end
- **Officer Assignment**: Personnel assigned to units
- **Vehicle ID**: Vehicle identification and registration
- **Recommended Units**: Closest available unit recommendation
- **Forced Dispatch**: Override recommendations for manual dispatch
- **Unit History**: Display of unit activity and incident history
- **Minimum Staffing**: Monitor minimum staffing levels by unit type

### AVL (Automatic Vehicle Location)
- **GPS Tracking**: Real-time GPS tracking of mobile units
- **Breadcrumb Trail**: Historical GPS track of unit movement
- **Location Update Rate**: 15-60 second GPS update intervals
- **Proximity Search**: Find nearest unit to incident location
- **Geofencing**: Alerts when units enter/exit defined areas
- **ETA Calculation**: Estimated time of arrival based on current location
- **GPS Accuracy**: 5-10 meter typical accuracy with GPS
- **Indoor Location**: Enhanced indoor location via Wi-Fi/Bluetooth beacons
- **Integration**: Integration with Motorola CommandCentral Aware, Trimble AVL, CalAmp

### Mapping and GIS
- **Basemap Layers**: Street maps, aerial imagery, topographic maps
- **Incident Symbols**: Icons for incidents (police, fire, EMS)
- **Unit Symbols**: Icons for units with status color coding
- **Routing**: Turn-by-turn routing from unit location to incident
- **Distance Calculation**: Straight-line and road distance
- **Coverage Analysis**: Display of coverage areas and response zones
- **GIS Layers**: Fire hydrants, building footprints, parcels, flood zones
- **3D Buildings**: 3D building models for tactical planning
- **Floor Plans**: Indoor floor plans for large buildings
- **Geocoding Engine**: Esri World Geocoder, Google Geocoding API
- **Address Points**: Address point database for accurate geocoding
- **Map Updates**: Regular map data updates (quarterly or annual)

### Dispatching Features
- **Multiple Dispatch**: Dispatch multiple units to single incident
- **Stacked Dispatch**: Queue pending incidents for available units
- **Automatic Dispatch**: Automatic unit recommendation and dispatch
- **Tones and Alerts**: Integration with station alerting systems
- **Paging**: Automatic paging of off-duty personnel
- **Text-to-Speech**: Computer-generated voice announcements
- **Time Stamps**: Automatic time stamping of all events
- **Dispatcher Notes**: Confidential notes visible only to dispatchers
- **Hot Keys**: Keyboard shortcuts for rapid dispatching
- **Screen Pops**: Automatic information display on incoming calls

### Mobile Data Terminal (MDT) Integration
- **Mobile CAD**: Full CAD functionality on MDTs in vehicles
- **Incident Details**: View full incident details on MDT
- **Navigation**: Turn-by-turn navigation to incident
- **Status Updates**: Units update status via MDT (en route, on scene, clear)
- **Message Exchange**: Send/receive messages with dispatch
- **Query Capability**: Run queries (wants/warrants, vehicle registration, driver license)
- **Form Completion**: Complete incident reports on MDT
- **Attachments**: View attachments (photos, documents)
- **Offline Mode**: Limited functionality when offline
- **Ruggedized Hardware**: Panasonic Toughbook, Getac, Dell Latitude Rugged

### Records Management System (RMS) Integration
- **CAD-to-RMS Transfer**: Transfer incidents to RMS for report writing
- **Unit History**: View unit activity from RMS
- **Person History**: View person's criminal history and prior contacts
- **Vehicle History**: View vehicle registration and history
- **Location History**: View prior incidents at address
- **Warrants Check**: Real-time warrant verification
- **Gang Affiliation**: Gang member alerts
- **Sex Offender Registry**: Registered sex offender alerts

### Reporting and Analytics
- **Standard Reports**: Call volume, response times, unit activity
- **Custom Reports**: User-defined report templates
- **Report Scheduling**: Automated report generation and distribution
- **Exporting**: Export to Excel, PDF, CSV, XML
- **Dashboard**: Real-time operational dashboard
- **KPIs (Key Performance Indicators)**: Response time compliance, call volume trends
- **NFIRS Reports**: Automated NFIRS reporting for fire departments
- **NIBRS Reports**: FBI NIBRS incident-based reporting
- **Compliance Reporting**: State and federal compliance reports
- **Analytics Tools**: Predictive analytics, crime analysis, hotspot mapping

### System Administration
- **User Management**: Create, modify, delete user accounts
- **Role-Based Security**: Assign roles (dispatcher, supervisor, admin)
- **Permissions**: Granular permissions for system functions
- **Audit Trail**: Comprehensive audit logging of all actions
- **Configuration**: System configuration and customization
- **Code Tables**: Maintain incident codes, unit types, dispositions
- **Data Archiving**: Archive old incidents to secondary database
- **Database Maintenance**: Automated database optimization and backup
- **System Monitoring**: Monitor system health and performance
- **Alerting**: System alerts for errors, performance issues

## CAD System Performance Metrics

### Response Time Performance
- **Call Processing Time**: Time from 911 call answered to incident created (<60 seconds)
- **Dispatch Time**: Time from incident created to unit dispatched (<90 seconds for Priority 1)
- **Turnout Time**: Time from dispatch to unit en route (<60 seconds fire, <90 seconds police)
- **Travel Time**: Time from en route to arrival on scene
- **Total Response Time**: Time from 911 call to arrival on scene (target: <8 minutes for Priority 1)
- **NFPA Standards**: National Fire Protection Association response time standards
- **CALEA Standards**: Commission on Accreditation for Law Enforcement Agencies standards

### System Uptime and Reliability
- **Uptime Target**: 99.99% uptime (52 minutes downtime per year)
- **Redundancy**: N+1 or 2N redundancy for critical components
- **Failover Time**: <30 seconds for automatic failover
- **Backup Frequency**: Continuous database replication, hourly snapshots
- **Disaster Recovery**: Hot standby site with <4 hour RTO (Recovery Time Objective)
- **MTBF (Mean Time Between Failures)**: >10,000 hours for hardware
- **MTTR (Mean Time To Repair)**: <4 hours for critical repairs

### Database Performance
- **Query Response Time**: <2 seconds for 95% of queries
- **Concurrent Users**: Support 100-500+ concurrent users without degradation
- **Database Size**: 100 GB to 10+ TB depending on retention
- **Retention Period**: 7-10 years typical incident retention
- **Archive Strategy**: Move old data to archive database
- **Index Optimization**: Regular index rebuilding and optimization
- **Database Platform**: Microsoft SQL Server 2016/2019, Oracle 12c/19c, PostgreSQL 12+

## CAD Integration Standards

### NENA NG911 Standards
- **NENA i3**: Next Generation 911 standards from National Emergency Number Association
- **ESInet**: Emergency Services IP Network (IP-based 911 network)
- **SIP Protocol**: Session Initiation Protocol for call routing
- **LoST**: Location-to-Service Translation protocol
- **PIDF-LO**: Presence Information Data Format - Location Object (location format)
- **Additional Data**: Additional call data (photos, videos, text messages)
- **BCF (Border Control Function)**: Security boundary for ESInet

### APCO Standards
- **APCO P25**: Project 25 radio system integration
- **ANI/ALI**: Automatic Number/Location Identification standards
- **Call Routing**: Emergency call routing protocols

### CJIS Security Policy
- **FBI CJIS**: Criminal Justice Information Services Security Policy compliance
- **Security Requirements**: Background checks, physical security, auditing
- **Data Encryption**: Encryption of data in transit and at rest
- **Access Control**: Multi-factor authentication, role-based access
- **Audit Logging**: Comprehensive logging of all database access

### NFPA Fire Service Standards
- **NFPA 1221**: Standard for Installation, Maintenance, and Use of Emergency Services Communications Systems
- **NFPA 1710**: Organization and Deployment of Fire Suppression Operations
- **Response Time Standards**: Response time performance objectives
