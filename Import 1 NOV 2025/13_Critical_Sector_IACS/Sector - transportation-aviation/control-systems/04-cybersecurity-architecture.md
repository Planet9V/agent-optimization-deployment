
graph TB
    subgraph "NIST Framework Integration"
        Identify[Identify<br/>Asset Management<br/>Risk Assessment<br/>Governance]
        Protect[Protect<br/>Access Control<br/>Data Security<br/>Information Protection]
        Detect[Detect<br/>Anomaly Detection<br/>Continuous Monitoring<br/>Detection Processes]
        Respond[Respond<br/>Incident Response<br/>Communication<br/>Analysis]
        Recover[Recover<br/>Recovery Planning<br/>Improvements<br/>Communication]
    end

    subgraph "IEC 62443 Implementation"
        SL1[Security Level 1<br/>Basic Protection<br/>Low Risk Environment]
        SL2[Security Level 2<br/>Enhanced Protection<br/>Moderate Risk]
        SL3[Security Level 3<br/>High Security<br/>Critical Infrastructure]
        SL4[Security Level 4<br/>Maximum Security<br/>Extreme Risk]
    end

    subgraph "Zero Trust Architecture"
        Identity[Identity Management<br/>User Authentication<br/>Device Identity<br/>Certificate Authority]
        Policy[Policy Engine<br/>Access Decisions<br/>Dynamic Authorization<br/>Continuous Verification]
        Network[Network Segmentation<br/>Microsegmentation<br/>Least Privilege<br/>Device Isolation]
        Data[Data Protection<br/>Encryption<br/>DLP<br/>Privacy Controls]
        Monitoring[Security Monitoring<br/>Threat Detection<br/>Incident Response<br/>Forensics]
    end

    subgraph "Network Security Zones"
        Zone1[Management Zone<br/>Administrative Access<br/>SNMP, SSH, HTTPS]
        Zone2[OT Core Zone<br/>Control Systems<br/>Industrial Protocols]
        Zone3[OT Process Zone<br/>Field Devices<br/>Sensors & Actuators]
        Zone4[IT Network Zone<br/>Business Systems<br/>Office Applications]
        Zone5[DMZ Zone<br/>Public Services<br/>Internet Access]
        Zone6[Guest Zone<br/>Temporary Access<br/>Internet Only]
    end

    subgraph "Security Controls"
        Firewalls[Industrial Firewalls<br/>Deep Packet Inspection<br/>Protocol Filtering]
        IDS[Intrusion Detection<br/>Network Analysis<br/>Anomaly Detection]
        SIEM[SIEM Platform<br/>Event Correlation<br/>Threat Intelligence]
        AV[Antivirus<br/>Endpoint Protection<br/>Malware Detection]
        Patches[Patch Management<br/>Vulnerability Scanning<br/>System Updates]
        Backup[Backup & Recovery<br/>Data Protection<br/>Business Continuity]
    end

    subgraph "Incident Response"
        Detect[Threat Detection<br/>Automated Alerts<br/>Correlation Engine]
        Analyze[Incident Analysis<br/>Forensic Investigation<br/>Impact Assessment]
        Contain[Threat Containment<br/>Network Isolation<br/>System Quarantine]
        Eradicate[Threat Removal<br/>System Cleaning<br/>Vulnerability Fix]
        Recover[System Recovery<br/>Service Restoration<br/>Operations Resume]
        Learn[Lessons Learned<br/>Process Improvement<br/>Training Updates]
    end

    %% Framework connections
    Identify --> Protect
    Protect --> Detect
    Detect --> Respond
    Respond --> Recover
    Recover --> Identify

    %% Security level progression
    SL1 --> SL2
    SL2 --> SL3
    SL3 --> SL4

    %% Zero Trust components
    Identity --> Policy
    Policy --> Network
    Policy --> Data
    Policy --> Monitoring
    Network --> Monitoring
    Data --> Monitoring

    %% Zone connections (restricted)
    Zone1 --> Zone2
    Zone2 --> Zone3
    Zone4 -.-> Zone5
    Zone5 -.-> Zone6

    %% Security control integration
    Firewalls --> IDS
    IDS --> SIEM
    SIEM --> AV
    SIEM --> Patches
    SIEM --> Backup

    %% Incident response flow
    Detect --> Analyze
    Analyze --> Contain
    Contain --> Eradicate
    Eradicate --> Recover
    Recover --> Learn

    %% Cross-layer integration
    SIEM --> Detect
    SIEM --> Analyze
    SIEM --> Respond

    %% Styling
    classDef nist fill:#e3f2fd
    classDef iec fill:#f1f8e9
    classDef zerotrust fill:#fff3e0
    classDef zone fill:#fce4ec
    classDef controls fill:#e8f5e8
    classDef response fill:#fff8e1

    class Identify,Protect,Detect,Respond,Recover nist
    class SL1,SL2,SL3,SL4 iec
    class Identity,Policy,Network,Data,Monitoring zerotrust
    class Zone1,Zone2,Zone3,Zone4,Zone5,Zone6 zone
    class Firewalls,IDS,SIEM,AV,Patches,Backup controls
    class Detect,Analyze,Contain,Eradicate,Recover,Learn response
