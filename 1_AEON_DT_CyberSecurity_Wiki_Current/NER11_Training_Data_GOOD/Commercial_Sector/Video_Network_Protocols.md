# Video and Network Protocols - Commercial Facilities Security

## ONVIF (Open Network Video Interface Forum)

**ONVIF Profile S - Video Streaming**
- Core video streaming profile for IP cameras and encoders
- RTSP (Real-Time Streaming Protocol) for live video delivery
- H.264/H.265 video codec support with configurable bitrate
- MJPEG fallback for compatibility with legacy systems
- PTZ control commands: absolute, relative, continuous movement
- Video analytics metadata streaming via ONVIF extensions
- Authentication: WS-UsernameToken, HTTP Digest authentication
- Service discovery via WS-Discovery multicast
- Event handling with PullPoint and BaseNotification subscription
- Supported by 8,000+ camera models from 500+ manufacturers

**ONVIF Profile T - Advanced Video Streaming**
- H.265/HEVC high-efficiency video coding mandatory
- Two-way audio streaming with G.711, G.726, AAC codecs
- Video analytics configuration and metadata retrieval
- Image sensor configuration: WDR, day/night switching
- Enhanced PTZ: preset tours, patrol routes, home position
- Privacy masking and motion detection region configuration
- Tamper detection events and analytics events
- Backward compatible with Profile S implementations
- Security: TLS 1.2+ encryption for video streams
- Firmware upgrade capabilities via ONVIF Device Manager

**ONVIF Profile G - Edge Recording and Storage**
- Edge storage management: recording configuration and retrieval
- Recording search with time, event, and metadata filters
- Playback control: play, pause, fast-forward, rewind
- Export recording clips for forensic investigation
- Storage configuration: local SD card, NAS, SAN support
- Recording modes: continuous, motion, schedule, alarm
- Automatic Network Replenishment (ANR) for network failures
- Health monitoring: storage capacity, recording status
- Multiple simultaneous playback streams support
- Integration with VMS for centralized recording management

**ONVIF Profile M - Metadata and Analytics**
- Structured metadata streaming for video analytics
- Object classification: human, vehicle, face, license plate
- Rule configuration: line crossing, intrusion, loitering
- Scene analytics: people counting, crowd detection, heat mapping
- Facial recognition metadata with bounding box coordinates
- Appearance attributes: color, size, direction, speed
- Event correlation across multiple analytics rules
- JSON and XML metadata formats for flexible integration
- Real-time and recorded analytics metadata retrieval
- Third-party analytics integration framework

## RTSP (Real-Time Streaming Protocol)

**RTSP Over TCP (RFC 2326/7826)**
- Session setup: DESCRIBE, SETUP, PLAY, PAUSE, TEARDOWN methods
- Transport: RTP (Real-Time Protocol) for media delivery
- RTCP (RTP Control Protocol) for QoS monitoring
- Authentication: Basic, Digest, or custom token-based
- Port configuration: TCP 554 (default) or custom ports
- Session Description Protocol (SDP) for media negotiation
- Bandwidth adaptation with dynamic bitrate adjustment
- Interleaved mode: RTP over RTSP TCP connection
- Keep-alive mechanism: OPTIONS or GET_PARAMETER requests
- URL format: rtsp://username:password@camera-ip:port/stream

**RTSP Streaming Profiles**
- Main stream: high resolution (4K/1080p) for recording
- Sub stream: low resolution (D1/CIF) for live monitoring
- Third stream: mobile stream optimized for bandwidth
- Codec parameters: I-frame interval, bitrate, GOP structure
- Transport modes: RTP/UDP (low latency), RTP/TCP (firewall friendly)
- Multicast streaming: IGMP for efficient bandwidth usage
- Unicast streaming: dedicated stream per client connection
- Bandwidth control: CBR (Constant Bitrate) or VBR (Variable Bitrate)
- Audio synchronization: RTCP sender reports for A/V sync
- Error resilience: FEC (Forward Error Correction) for packet loss

## SIP (Session Initiation Protocol) for Video Intercom

**SIP for Door Entry and Intercoms**
- SIP registration: IP intercoms register with SIP server/PBX
- Call signaling: INVITE, ACK, BYE, CANCEL for session control
- Video codec negotiation: H.264/H.265 via SDP exchange
- Audio codecs: G.711 (PCMU/PCMA), G.722 wideband audio
- DTMF relay: RFC 2833 or SIP INFO for door release commands
- SIP NOTIFY for event notification: door open, button press
- Presence and status: PUBLISH/SUBSCRIBE for device availability
- Integration with Asterisk, FreeSWITCH, Cisco CUCM PBX systems
- Secure SIP: TLS encryption and SRTP for media
- Mobile app integration: iOS/Android SIP clients for remote answer

**Axis Network Door Stations with SIP**
- Axis A8207-VE Network Video Door Station: SIP 2.0 compliant
- Dual-way audio: full-duplex with echo cancellation
- Video streaming: 1080p H.264 with configurable bitrate
- Relay control: HTTP API or SIP INFO message for door strike
- Integration: Asterisk, 3CX, Avaya, Cisco telephony systems
- Mobile app: Axis Companion Door Station for iOS/Android
- DTMF codes: *9 for door release, configurable actions
- Night vision: IR illumination with automatic day/night switching
- Weather resistant: IP66, IK10 vandal-resistant housing
- PoE IEEE 802.3af with auxiliary power input

**2N IP Verso SIP Video Intercom**
- SIP 2.0 with HD video (720p/1080p) over IP networks
- Modular design: camera, keypad, card reader, info modules
- Audio: full-duplex with noise cancellation
- Access control integration: RFID 125kHz, 13.56MHz, NFC
- Mobile app: 2N Mobile Video for iOS/Android SIP clients
- Relay outputs: 2x for door strike and auxiliary devices
- API integration: RESTful API for building management systems
- Elevator control: DTMF relay for multi-floor buildings
- Firmware: automatic updates via 2N Cloud Services
- Certifications: CE, FCC, IP54 weatherproof rating

## HTTP/HTTPS API for Camera Integration

**RESTful API for Camera Control**
- Authentication: Basic, Digest, OAuth 2.0, API tokens
- Video streaming: MJPEG over HTTP, progressive download
- Snapshot capture: HTTP GET request for JPEG images
- PTZ control: HTTP POST/PUT commands with JSON payloads
- Configuration management: GET/PUT camera settings via JSON
- Event subscription: Webhooks, Server-Sent Events (SSE)
- Firmware upgrade: HTTP POST with multipart/form-data
- TLS 1.2/1.3 encryption for secure API communication
- Rate limiting: API throttling to prevent abuse
- CORS support: Cross-Origin Resource Sharing for web apps

**Axis VAPIX API Examples**
- PTZ absolute position: `http://camera-ip/axis-cgi/com/ptz.cgi?pan=90&tilt=45&zoom=1000`
- Capture snapshot: `http://camera-ip/axis-cgi/jpg/image.cgi?resolution=1920x1080`
- Get video stream: `http://camera-ip/axis-cgi/mjpg/video.cgi?camera=1&resolution=1280x720`
- Set camera parameters: POST to `/axis-cgi/param.cgi?action=update&ImageSource.I0.Sensor.Brightness=50`
- Event notification: `/axis-cgi/eventmanager.cgi` with XML subscription
- Audio control: `/axis-cgi/audio/transmit.cgi` for two-way audio
- ONVIF service endpoint: `http://camera-ip/onvif/device_service`
- Authentication: HTTP Digest or API key in Authorization header

## PSIA (Physical Security Interoperability Alliance)

**PSIA Video Streaming and Control**
- RESTful web services architecture with XML/JSON
- Video streaming: RTSP/RTP with PSIA stream URI format
- PTZ control: HTTP POST with XML commands for pan/tilt/zoom
- Event management: subscription model with HTTP callbacks
- Recording control: start/stop recording via API commands
- Search and playback: query recordings with time range filters
- Analytics configuration: rule setup via XML schema
- Device discovery: UPnP or manual IP configuration
- Authentication: HTTP Digest with role-based access
- Supported by legacy systems: replaced largely by ONVIF

## BACnet for Building Integration

**BACnet MS/TP (Master-Slave/Token-Passing)**
- Serial communication: RS-485 twisted pair at 9600-115200 baud
- Network topology: multi-drop bus with up to 127 devices
- Token passing: deterministic access for master devices
- Object types: Binary Input (BI), Binary Output (BO), Analog Input (AI)
- Camera integration: door status, motion detection as BACnet points
- Access control: door lock control via Binary Output objects
- Alarm reporting: COV (Change of Value) notifications
- Integration with HVAC, lighting, fire alarm systems
- Schneider Electric, Siemens, Honeywell controller support
- Bacnet/IP gateway for Ethernet backbone connectivity

**BACnet/IP for Network-Based Integration**
- UDP/IP communication on port 47808 (0xBAC0)
- BBMD (BACnet Broadcast Management Device) for routing
- Object types for security: Accumulator (people counting), Life Safety
- Video analytics integration: occupancy data as Analog Value objects
- Event enrollment: notification classes for alarm escalation
- Trend logging: historical data collection for analytics
- Scheduling: time-based access control and camera activation
- Priority array: multi-source control with override capability
- Integration examples: Johnson Controls Metasys, Tridium Niagara
- Security: TLS encryption with BACnet Secure Connect (BACnet/SC)

## Modbus TCP for Industrial Integration

**Modbus TCP/IP Protocol**
- TCP port 502 with client-server architecture
- Function codes: Read Coils (01), Read Holding Registers (03), Write Single Coil (05)
- Camera integration: motion detection as discrete input
- Access control: door lock relay as discrete output
- Alarm status: read input registers for event states
- Scalability: up to 247 slave devices per master
- Fieldbus integration: PLCs, SCADA systems in industrial facilities
- Security cameras with Modbus: Pelco, Panasonic industrial models
- Gateway devices: Anybus, Red Lion for protocol conversion
- Cybersecurity: Modbus TCP lacks encryption, use VPN or firewall segmentation

## Wiegand Protocol for Access Control

**Wiegand 26-Bit Format**
- 26-bit data format: 8-bit facility code + 16-bit card number
- Even and odd parity bits for error detection
- Voltage levels: 0V (logic 1), +5V (logic 0)
- Pulse width: 20-100 microseconds per bit
- Inter-bit interval: 200-2000 microseconds
- Reader-to-controller communication over 3-wire connection
- Facility code range: 0-255 (256 unique sites)
- Card number range: 0-65535 (65,536 unique cards)
- Distance limitation: typically 500 feet maximum
- Unencrypted: susceptible to eavesdropping and replay attacks

**Wiegand 37-Bit Corporate 1000 Format**
- HID Corporate 1000 extended format: 35-bit data + parity
- 12-bit manufacturer code + 22-bit card ID
- Supports 4,194,304 unique card numbers per manufacturer
- Enhanced security with unique manufacturer identification
- Compatible with HID iCLASS and Prox readers
- Panel configuration: requires Corporate 1000 format support
- Migration path from 26-bit to higher security credentials
- Parity: even parity on first 18 bits, odd on last 18 bits

**OSDP (Open Supervised Device Protocol)**
- Encrypted replacement for Wiegand: AES-128 encryption
- Bidirectional communication: reader-to-panel acknowledgment
- Secure Channel Protocol (SCP) for credential protection
- Tamper detection: reader cover, card read errors
- LED and buzzer control: visual/audio feedback from panel
- Biometric data transfer: fingerprint templates over OSDP
- Version 2.2 features: secure firmware updates, multi-drop RS-485
- Compliance testing: SIA OSDP Verified program
- Migration: OSDP-capable readers on existing Wiegand panels
- Supported by Mercury, HID, Software House controllers

## Network Time Protocol (NTP) for Synchronization

**NTP for Camera and System Time Sync**
- NTP version 4 (RFC 5905) with microsecond accuracy
- Stratum levels: Stratum 1 (GPS/atomic), Stratum 2 (NTP servers)
- Camera NTP client: automatic time synchronization on boot
- Time zones: UTC offset configuration for local time display
- Daylight Saving Time (DST): automatic adjustment rules
- Importance: timestamp accuracy for forensic video evidence
- Public NTP servers: time.google.com, time.nist.gov, pool.ntp.org
- Local NTP server: Windows Server, Linux chrony/ntpd
- Security: NTP authentication with symmetric keys (MD5/SHA1)
- Monitoring: check NTP offset in camera web interface

## SNMP (Simple Network Management Protocol)

**SNMP v2c/v3 for Device Monitoring**
- MIB (Management Information Base) for device parameters
- OID (Object Identifier): unique ID for each monitored value
- Trap notifications: device sends alerts to SNMP manager
- Monitored parameters: CPU usage, memory, temperature, uptime
- Camera monitoring: recording status, network bandwidth, errors
- NVR monitoring: HDD health (SMART data), RAID status
- SNMP managers: PRTG, Zabbix, SolarWinds, Nagios
- Community strings (v2c): read-only, read-write passwords
- SNMPv3 security: authentication (MD5/SHA) + encryption (DES/AES)
- Port 161 (queries), port 162 (traps)
