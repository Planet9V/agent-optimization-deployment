
graph LR
    subgraph "Protocol Gateway"
        PG[Moxa MGate 5192<br/>Multi-Protocol Gateway<br/>IEC 61850 MMS Client]
    end

    subgraph "BACnet Network"
        B1[Building 1<br/>BACnet/IP]
        B2[Building 2<br/>BACnet/SC]
        B3[HVAC System<br/>BACnet MS/TP]
        B4[Lighting Control<br/>BACnet/SC]
    end

    subgraph "Modbus Network"
        M1[Chiller Plant<br/>Modbus TCP]
        M2[Boiler System<br/>Modbus RTU]
        M3[Power Meter<br/>Modbus TCP]
        M4[Generator Set<br/>Modbus RTU]
    end

    subgraph "DNP3 Network"
        D1[Substation RTU<br/>DNP3 v3.0]
        D2[Transformer Monitor<br/>DNP3 TCP]
        D3[Breaker Control<br/>DNP3 UDP]
        D4[SCADA Interface<br/>DNP3 v3.0]
    end

    subgraph "IEC 61850 Network"
        I1[Protection Relay<br/>IEC 61850]
        I2[Measurement Unit<br/>IEC 61850]
        I3[Control Cabinet<br/>IEC 61850]
        I4[Digital Meter<br/>IEC 61850]
    end

    subgraph "EtherNet/IP Network"
        E1[PLC Controller<br/>EtherNet/IP]
        E2[I/O Modules<br/>EtherNet/IP]
        E3[Servo Drive<br/>EtherNet/IP]
        E4[HMI Terminal<br/>EtherNet/IP]
    end

    subgraph "Data Integration"
        DB[(Database<br/>Historical Data)]
        HMI[Human Machine<br/>Interface]
        API[REST API<br/>Web Services]
        MQTT[MQTT Broker<br/>IoT Messaging]
    end

    %% Gateway Connections
    PG -.-> B1
    PG -.-> B2
    PG -.-> B3
    PG -.-> B4

    PG -.-> M1
    PG -.-> M2
    PG -.-> M3
    PG -.-> M4

    PG -.-> D1
    PG -.-> D2
    PG -.-> D3
    PG -.-> D4

    PG -.-> I1
    PG -.-> I2
    PG -.-> I3
    PG -.-> I4

    PG -.-> E1
    PG -.-> E2
    PG -.-> E3
    PG -.-> E4

    %% Data Integration
    PG --> DB
    PG --> HMI
    PG --> API
    PG --> MQTT

    %% Protocol Mappings
    PG -.-> |IEC 61850 ↔ Modbus| PM1
    PG -.-> |IEC 61850 ↔ DNP3| PM2
    PG -.-> |BACnet ↔ Modbus| PM3
    PG -.-> |BACnet ↔ EtherNet/IP| PM4

    %% Styling
    classDef gateway fill:#fff3e0
    classDef bacnet fill:#e8f5e8
    classDef modbus fill:#e1f5fe
    classDef dnp3 fill:#fce4ec
    classDef iec fill:#f3e5f5
    classDef ethernet fill:#e0f2f1
    classDef data fill:#fff8e1
    classDef protocol fill:#ffecb3

    class PG gateway
    class B1,B2,B3,B4 bacnet
    class M1,M2,M3,M4 modbus
    class D1,D2,D3,D4 dnp3
    class I1,I2,I3,I4 iec
    class E1,E2,E3,E4 ethernet
    class DB,HMI,API,MQTT data
    class PM1,PM2,PM3,PM4 protocol
