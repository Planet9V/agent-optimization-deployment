# VoIP Call Routing Operations

## Overview
Voice over IP (VoIP) call routing systems manage SIP (Session Initiation Protocol) trunk configuration, least-cost routing algorithms, codec negotiation, and emergency services (E911) integration to deliver reliable, high-quality voice communications while minimizing carrier costs and ensuring regulatory compliance.

## Operational Procedures

### 1. SIP Trunk Configuration and Registration
- **SIP URI Registration**: User agents register SIP addresses (sip:user@domain.com) with SIP registrar server; registration timeout typically 3600 seconds
- **Authentication Configuration**: Digest authentication using MD5 hashed credentials protects against unauthorized trunk usage and toll fraud
- **Trunk Capacity Management**: SIP trunks support concurrent call limits (10, 20, 50, unlimited channels); usage monitoring prevents over-subscription
- **Codec Preference Configuration**: Preferred codec list (G.711, G.729, Opus) specified in SDP (Session Description Protocol); G.711 provides best quality with 64 kbps per call

### 2. Call Flow Processing and Dial Plan
- **Digit Analysis**: Dialed number analyzed against dial plan rules determining call routing (local extension, PSTN, international, emergency)
- **Number Normalization**: E.164 format normalization converts dialed digits to standardized format (+1NPANXXXXXX for North America)
- **Call Routing Logic**: Dial peers match dialed patterns and route to appropriate destination (IP peer for VoIP, POTS peer for PSTN gateway)
- **Translation Rules**: Digit manipulation (prefix addition/removal, digit replacement) performed per carrier requirements before call placement

### 3. Least-Cost Routing (LCR) Selection
- **Rate Table Management**: Carrier rate decks imported showing per-minute costs for domestic, international, and toll-free call types
- **Route Priority Ranking**: Primary and backup routes defined; primary selected for cost or quality; failover occurs on busy/unavailable conditions
- **Time-of-Day Routing**: Different routes selected based on business hours, after-hours, or weekend periods optimizing cost and staff availability
- **Call Quality Metrics**: Routing decisions factor Mean Opinion Score (MOS), packet loss, jitter, and latency avoiding poor-quality routes

### 4. Codec Negotiation and Transcoding
- **SDP Offer/Answer Exchange**: Calling party offers supported codecs in SDP; called party answers with selected codec from offered list
- **Transcoding Resource Management**: Session Border Controller (SBC) or media gateway transcodes between incompatible codecs when endpoints lack common codec
- **Bandwidth-Aware Codec Selection**: G.729 (8 kbps) selected for bandwidth-constrained links; G.711 (64 kbps) for high-quality LAN calls
- **Opus Adaptive Codec**: Modern systems leverage Opus codec dynamically adjusting bitrate (6-510 kbps) and quality based on network conditions

### 5. Session Border Controller (SBC) Operations
- **Topology Hiding**: SBC masks internal network topology and IP addresses from external SIP trunks enhancing security
- **NAT Traversal**: SBC handles Network Address Translation complications enabling SIP/RTP traffic through firewalls and NAT devices
- **SIP Normalization**: SBC translates SIP variants between carriers and internal systems ensuring interoperability despite protocol differences
- **Fraud Detection**: Anomalous call patterns (high international volume, sequential dialing, short-duration calls) trigger fraud alerts and blocking

### 6. Emergency Services (E911/NG911) Integration
- **ELIN (Emergency Location Identification Number)**: Each physical location assigned unique ELIN (DID) delivering to PSAP (Public Safety Answering Point)
- **LIS (Location Information Server)**: Database maps IP addresses, switch ports, or access points to civic addresses for emergency location delivery
- **PIDF-LO (Presence Information Data Format - Location Object)**: XML-formatted location data transmitted with 911 calls per NENA i3 standards
- **Automatic Location Updates**: Moves/adds/changes trigger location database updates ensuring 911 calls deliver accurate caller location

### 7. Call Quality Monitoring and Troubleshooting
- **RTCP Reporting**: Real-time Transport Control Protocol transmits call quality metrics (packet loss, jitter, MOS) during and after calls
- **SIP Ladder Diagrams**: Packet captures analyzed showing SIP message flow identifying call setup failures and timeout issues
- **Media Quality Alerts**: Real-time monitoring detects poor MOS scores (<3.5) triggering alerts for proactive investigation
- **Call Detail Records (CDRs)**: Comprehensive call logs capture source, destination, duration, codec, quality metrics, and routing decisions for billing and analysis

## System Integration Points

### Unified Communications Platforms
- **Microsoft Teams Direct Routing**: SBC connects Teams to PSTN via SIP trunks; certified SBCs required for Microsoft support
- **Cisco Unified Communications Manager (CUCM)**: Call Manager controls call routing, features, and SIP trunk integration for Cisco VoIP deployments
- **Zoom Phone**: Cloud PBX integrates with PSTN via Zoom-hosted or customer-provided SIP trunks
- **RingCentral/8x8**: Cloud-hosted UCaaS platforms provide turnkey VoIP with included PSTN connectivity

### SIP Trunk Carrier Integration
- **Twilio Elastic SIP Trunking**: Programmable SIP trunking with RESTful API for dynamic capacity scaling and call control
- **Bandwidth SIP Trunking**: Major wholesale carrier providing SIP trunks with integrated 911, CNAM, and number porting services
- **Verizon Business SIP Trunking**: Enterprise-grade SIP connectivity with QoS guarantees and 24/7 support
- **AT&T IP Toll-Free**: SIP trunk service specifically for toll-free number termination with DNIS delivery

### PSTN Gateway Integration
- **Analog Telephony Adapters (ATA)**: Convert analog phones/fax to SIP for legacy device support (Cisco SPA, Grandstream HT series)
- **PRI/T1 Gateways**: Audiocodes Mediant, Cisco ISR routers convert ISDN PRI circuits to SIP for hybrid PSTN/VoIP environments
- **SS7 Signaling**: Large carriers use SS7 (ISUP) for call signaling requiring SS7 gateway (Dialogic, Sonus) for SIP interworking
- **Number Porting Platforms**: LNP (Local Number Portability) databases queried during call routing determining carrier for ported numbers

### CRM and Business Systems
- **Screen Pop Integration**: Inbound caller ID triggers CRM record lookup presenting customer information to agent before answer
- **Click-to-Dial**: CRM systems initiate outbound calls via SIP INVITE messages to desk phones or softphones
- **Call Activity Logging**: CDRs imported to CRM/helpdesk systems (Salesforce, ServiceNow) associating calls with customer records
- **Presence Integration**: UC platforms share presence status (available, busy, DND) with business applications enabling intelligent routing

## Regulatory Compliance

### FCC Part 64 - CALEA (Communications Assistance for Law Enforcement Act)
- **Lawful Intercept Capability**: VoIP providers must enable law enforcement wiretaps pursuant to court orders
- **Call Content Delivery**: Intercepted call content (RTP streams) and call-associated data delivered to law enforcement collection points
- **Compliance Certification**: Carriers must certify CALEA compliance; safe harbor provisions for providers using certified equipment
- **Notice Requirements**: VoIP providers must notify customers that communications subject to lawful intercept capabilities

### FCC E911 Requirements (Part 9, Part 12)
- **Location Accuracy**: Wireline E911 location delivered from ALI (Automatic Location Identification) database; must be maintained current
- **Direct Dial-Through**: 911 calls must reach PSAP without prefix dialing (e.g., "9") regardless of internal dial plan
- **Call-Back Number**: PSAP must receive valid call-back number enabling 911 dispatcher to reconnect if call disconnected
- **Battery Backup**: FCC requires 8 hours battery backup for fixed VoIP systems ensuring 911 availability during power outages (waived for nomadic VoIP)

### FCC STIR/SHAKEN (Call Authentication)
- **SHAKEN Certificate Deployment**: VoIP providers must obtain SHAKEN certificates from STI-PA (Policy Administrator) for call signing
- **Attestation Levels**: Calls attested as A (full authentication), B (partial), or C (gateway) indicating caller ID verification confidence
- **SIP Identity Header**: Signed PASSporT (Personal Assertion Token) in SIP Identity header verifies caller ID not spoofed
- **Analytics and Blocking**: Downstream providers analyze attestation levels blocking likely illegal robocalls

### TCPA (Telephone Consumer Protection Act)
- **Prior Express Consent**: Autodialed or prerecorded calls to mobile phones require prior written consent
- **Do Not Call Registry**: Telemarketing calls must scrub against National DNC list; VoIP platforms integrate DNC scrubbing APIs
- **Call Time Restrictions**: Telemarketing calls prohibited before 8 AM or after 9 PM recipient's local time
- **Opt-Out Requirements**: Calls must include opt-out mechanism and honor requests immediately

## Equipment and Vendors

### Session Border Controllers (SBCs)
- **Ribbon SBC 5000/7000**: Enterprise and service provider SBCs supporting 10,000+ concurrent sessions with transcoding and media services
- **Oracle (Acme Packet) SBC**: Carrier-grade platforms deployed by major service providers; supports millions of subscribers
- **AudioCodes Mediant SBC**: Mid-market SBCs popular in Microsoft Teams Direct Routing deployments; certified for Teams interoperability
- **Cisco Unified Border Element (CUBE)**: Integrated SBC functionality in Cisco ISR routers for branch office deployments

### IP-PBX and Unified Communications
- **3CX Phone System**: Software-based IP-PBX with Windows, Linux, cloud deployment options; supports SIP trunks and video conferencing
- **Asterisk (Open Source)**: Foundation for numerous commercial VoIP platforms; flexible dial plan and AGI scripting
- **FreeSWITCH**: High-performance open-source soft switch; supports WebRTC, video, and advanced routing
- **Avaya Aura**: Enterprise UC platform supporting multi-site deployments with centralized management and SIP trunking

### SIP Trunk Carriers
- **Bandwidth**: Wholesale carrier providing SIP trunking APIs for CPaaS (Communications Platform as a Service) developers
- **Telnyx**: Elastic SIP trunking with global points of presence and real-time provisioning via RESTful API
- **Flowroute**: Developer-friendly SIP trunking with per-minute pricing and no commitments
- **Peerless Network**: Tier 1 carrier with SIP trunk interconnects to major carriers and extensive DID inventory

### VoIP Phones and Endpoints
- **Cisco IP Phones**: 7800/8800 series desk phones with HD voice, Power-over-Ethernet, and programmable line keys
- **Poly (formerly Polycom)**: VVX business phone series and conference phones with Acoustic Fence noise suppression
- **Yealink**: Cost-effective SIP phones popular in SMB deployments; T4/T5 series with color displays and Bluetooth
- **Grandstream**: Budget SIP phones and video phones; GXV series Android-based video phones support UC apps

## Performance Metrics

### Call Quality Metrics
- **Mean Opinion Score (MOS)**: Subjective quality 1-5 scale; VoIP target MOS >4.0 (toll quality); calculated from R-Factor per ITU-T G.107
- **Packet Loss**: Target <1% packet loss for acceptable quality; >3% packet loss causes noticeable degradation
- **Jitter**: Variation in packet arrival times; target <30 ms jitter; jitter buffers smooth delivery at cost of latency
- **Latency (One-Way Delay)**: Target <150 ms one-way; >300 ms creates noticeable conversational delays and talk-over

### Service Availability
- **SIP Trunk Uptime**: Target 99.99% uptime (max 4.38 minutes monthly downtime) for business-critical voice services
- **Call Completion Rate (CCR)**: Percentage of call attempts successfully connected; target >98% CCR
- **Average Call Setup Time**: Time from INVITE to 200 OK; target <2 seconds for responsive call establishment
- **Emergency Call Success Rate**: 100% success rate required for 911 calls; monthly testing verifies E911 database accuracy

### Operational Efficiency
- **Cost per Minute**: Blended rate across domestic/international; typical $0.005-0.02 per minute domestic, higher international
- **Trunk Utilization**: Percentage of trunk capacity used during peak hour; >70% indicates need for capacity expansion
- **Toll Fraud Rate**: Unauthorized usage detected and blocked; target <0.01% of total minutes fraudulent
- **Support Ticket Volume**: Voice quality and connectivity tickets per 1000 users; target <5 tickets/1000 users monthly

### Customer Experience
- **Post-Call Survey Scores**: Automated IVR or email surveys collect quality feedback; target >4.0 on 5-point scale
- **First-Call Resolution**: Percentage of reported issues resolved on first contact; target >80% FCR
- **Dial Tone Delay**: Time from handset lift to dial tone; target <200 ms for responsive user experience
- **Feature Satisfaction**: User adoption of UC features (voicemail-to-email, mobile app, video); higher adoption indicates successful deployment

---

**Document Control**
- **Version**: 1.0
- **Last Updated**: 2025-11-06
- **Regulatory References**: FCC Part 64 (CALEA), FCC Part 9/12 (E911), IETF RFC 3261 (SIP), ITU-T G.107/G.114, TCPA, STIR/SHAKEN
- **Review Cycle**: Annual
