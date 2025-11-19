
graph TB
    subgraph "Core Network Layer"
        Core1[Core Switch 1<br/>Catalyst 9500]
        Core2[Core Switch 2<br/>Catalyst 9500]
        ISECluster[ISE Cluster<br/>2 PAN + 2 MnT + pxGrid]
        DNACCluster[DNA Center Cluster<br/>3 Nodes, 112 Core]
    end

    subgraph "Distribution Layer"
        Dist1[Distribution Switch 1<br/>Catalyst 9400]
        Dist2[Distribution Switch 2<br/>Catalyst 9400]
    end

    subgraph "Access Layer"
        Edge1[Edge Switch 1<br/>Catalyst 9300]
        Edge2[Edge Switch 2<br/>Catalyst 9300]
        Edge3[Edge Switch 3<br/>Catalyst 9300]
    end

    subgraph "OT Network (Red)"
        SNE[Metasys SNE<br/>BACnet MS/TP]
        SNC[Metasys SNC<br/>BACnet/IP]
        ALCMS[Eaton ALCMS<br/>Proprietary + BACnet]
        HGW[HVAC Gateway<br/>Modbus TCP/RTU]
        FGW[Fire Gateway<br/>BACnet Interface]
    end

    subgraph "IT Network (Blue)"
        WLC[Wireless Controller<br/>Catalyst 9800]
        AP1[Access Point 1<br/>Catalyst 9100]
        AP2[Access Point 2<br/>Catalyst 9100]
        AP3[Access Point 3<br/>Catalyst 9100]
        MSSQL[Management Server<br/>SQL Database]
        WEB[Web Server<br/>HTTPS Interface]
    end

    subgraph "Protocol Layer"
        subgraph "Layer 7 - Application"
            BACnetSC[BACnet/SC<br/>Secure Communication]
            ModbusTCP[Modbus TCP<br/>Industrial Protocol]
            DNP3[DNP3 v3.0<br/>Electrical Systems]
            IEC61850[IEC 61850<br/>Substation Automation]
        end

        subgraph "Layer 4 - Transport"
            TCP[TCP<br/>Reliable Delivery]
            UDP[UDP<br/>Real-time Communication]
        end

        subgraph "Layer 3 - Network"
            IP[IP Protocol<br/>Routing and Addressing]
            VLAN[VLAN<br/>Network Segmentation]
        end

        subgraph "Layer 2 - Data Link"
            Ethernet[Ethernet<br/>CSMA/CD Protocol]
            STP[Spanning Tree<br/>Loop Prevention]
        end

        subgraph "Layer 1 - Physical"
            Fiber[Multi-mode Fiber<br/>10 Gbps]
            Copper[Cat6A Copper<br/>1 Gbps]
            Wireless[Wi-Fi 6<br/>802.11ax]
        end
    end

    %% Core connections
    Core1 <--> Core2
    ISECluster --> Core1
    ISECluster --> Core2
    DNACCluster --> Core1
    DNACCluster --> Core2

    %% Distribution connections
    Dist1 --> Core1
    Dist1 --> Core2
    Dist2 --> Core1
    Dist2 --> Core2

    %% Access connections
    Edge1 --> Dist1
    Edge1 --> Dist2
    Edge2 --> Dist1
    Edge2 --> Dist2
    Edge3 --> Dist1
    Edge3 --> Dist2

    %% OT Network connections
    SNE --> Edge1
    SNC --> Edge1
    ALCMS --> Edge2
    HGW --> Edge1
    FGW --> Edge2

    %% IT Network connections
    WLC --> Dist1
    AP1 --> Edge3
    AP2 --> Edge3
    AP3 --> Edge3
    MSSQL --> Dist2
    WEB --> Dist2

    %% Protocol Layer connections
    BACnetSC --> ModbusTCP
    BACnetSC --> DNP3
    BACnetSC --> IEC61850

    ModbusTCP --> TCP
    DNP3 --> TCP
    IEC61850 --> TCP

    TCP --> IP
    UDP --> IP

    IP --> VLAN

    VLAN --> Ethernet
    Ethernet --> Fiber
    Ethernet --> Copper

    %% Styling
    classDef core fill:#ffcdd2
    classDef distribution fill:#c8e6c9
    classDef access fill:#d1c4e9
    classDef ot fill:#ffecb3
    classDef it fill:#e1bee7
    classDef protocol fill:#b2dfdb

    class Core1,Core2,ISECluster,DNACCluster core
    class Dist1,Dist2 distribution
    class Edge1,Edge2,Edge3 access
    class SNE,SNC,ALCMS,HGW,FGW ot
    class WLC,AP1,AP2,AP3,MSSQL,WEB it
    class BACnetSC,ModbusTCP,DNP3,IEC61850,TCP,UDP,IP,VLAN,Ethernet,STP,Fiber,Copper,Wireless protocol
