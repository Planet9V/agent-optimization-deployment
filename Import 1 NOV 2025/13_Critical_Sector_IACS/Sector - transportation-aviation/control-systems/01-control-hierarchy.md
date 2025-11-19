
graph TB
    subgraph "Enterprise Level"
        EM[Enterprise Management]
        AOD[Airport Operations Database]
        EMS[Energy Management System]
        SOC[Security Operations Center]
    end

    subgraph "Supervisory Level"
        Metasys[Johnson Controls Metasys<br/>Building Automation System]
        ALCMS[Eaton PRO Command ALCMS<br/>Airfield Lighting Control]
        HMIMain[Central HMI<br/>15" Touchscreen<br/>1024x768 Resolution]
        DNAC[Cisco DNA Center<br/>3-Node Cluster<br/>112 Core per Node]
    end

    subgraph "Network Level"
        ISE[Cisco ISE Cluster<br/>2 PAN + 2 MnT + pxGrid + PSN]
        SDA[SD-Access Fabric<br/>Intent-Based Networking<br/>Microsegmentation]
        PG[Moxa MGate 5192<br/>Protocol Gateway<br/>IEC 61850/Modbus/DNP3]
    end

    subgraph "Local Control Level"
        SNE[Metasys SNE Network Engine<br/>200 I/O Points<br/>BACnet MS/TP, LON, Modbus]
        SNC[Metasys SNC Network Engine<br/>800 I/O Points<br/>Enhanced Capacity]
        ALCMSPLC[ALCMS PLC<br/>Centralized Architecture<br/>FAA L-890 Compliant]
    end

    subgraph "Field Device Level"
        HVAC[HVAC Systems<br/>AHU, VAV, Chiller, Boiler]
        Lighting[Building Lighting<br/>Occupancy, Daylight, Scene Control]
        Fire[Fire Detection & Alarm<br/>Smoke, Heat, Flame Detection]
        Security[Access Control<br/>RFID, Biometric, Video]
        Runway[Runway Edge Lights<br/>LED High Intensity<br/>CCR Controlled]
        Taxiway[Taxiway Lighting<br/>Guide System<br/>Brightness Control]
        Approach[Approach Lighting<br/>PAPI, VASI, ALSF<br/>Precision Indicators]
    end

    %% Enterprise Connections
    EM --> Metasys
    EM --> ALCMS
    AOD --> Metasys
    EMS --> Metasys
    SOC --> ISE

    %% Supervisory Connections
    Metasys --> SNE
    Metasys --> SNC
    ALCMS --> ALCMSPLC
    HMIMain --> Metasys
    HMIMain --> ALCMS
    DNAC --> ISE
    DNAC --> SDA

    %% Network Connections
    ISE --> SDA
    SDA --> SNE
    SDA --> SNC
    SDA --> ALCMSPLC
    SDA --> PG
    PG --> HVAC

    %% Field Device Connections
    SNE --> HVAC
    SNE --> Lighting
    SNE --> Fire
    SNE --> Security
    SNC --> HVAC
    SNC --> Lighting
    SNC --> Fire
    SNC --> Security
    ALCMSPLC --> Runway
    ALCMSPLC --> Taxiway
    ALCMSPLC --> Approach
    PG --> HVAC

    %% Styling
    classDef enterprise fill:#e1f5fe
    classDef supervisory fill:#f3e5f5
    classDef network fill:#e8f5e8
    classDef local fill:#fff3e0
    classDef field fill:#fce4ec

    class EM,AOD,EMS,SOC enterprise
    class Metasys,ALCMS,HMIMain,DNAC supervisory
    class ISE,SDA,PG network
    class SNE,SNC,ALCMSPLC local
    class HVAC,Lighting,Fire,Security,Runway,Taxiway,Approach field
