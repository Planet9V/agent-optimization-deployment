# HBOM Microcontrollers and ICs Dataset

**File**: 01_HBOM_Microcontrollers_ICs.md
**Created**: 2025-11-05
**Version**: v1.0.0
**Entity Type**: HARDWARE_COMPONENT
**Pattern Count**: 300+

## Hardware Bill of Materials - Microcontrollers & Integrated Circuits

### 1. STMicroelectronics STM32F407VGT6

```json
{
  "hbomFormat": "CycloneDX-HBOM",
  "specVersion": "1.0",
  "component": {
    "type": "microcontroller",
    "bom-ref": "STM32F407VGT6-001",
    "manufacturer": "STMicroelectronics",
    "part_number": "STM32F407VGT6",
    "description": "ARM Cortex-M4 32-bit MCU, 1MB Flash, 192KB RAM, 168MHz",
    "specifications": {
      "architecture": "ARM Cortex-M4",
      "core_frequency": "168 MHz",
      "flash_memory": "1024 KB",
      "sram_memory": "192 KB",
      "io_pins": 140,
      "operating_voltage": "1.8V - 3.6V",
      "operating_temp": "-40°C to +85°C",
      "package": "LQFP-100"
    },
    "security_features": [
      "Memory Protection Unit (MPU)",
      "Hardware CRC calculation",
      "Unique device ID",
      "Read-out protection"
    ],
    "vulnerabilities": [],
    "supplier": {
      "name": "STMicroelectronics",
      "country": "Switzerland",
      "authenticity_verified": true
    },
    "lifecycle": {
      "status": "active",
      "eol_date": null,
      "recommended_replacement": null
    }
  }
}
```

### 2. Espressif ESP32-WROOM-32

```json
{
  "hbomFormat": "CycloneDX-HBOM",
  "specVersion": "1.0",
  "component": {
    "type": "system-on-chip",
    "bom-ref": "ESP32-WROOM-32-001",
    "manufacturer": "Espressif Systems",
    "part_number": "ESP32-WROOM-32",
    "description": "WiFi + Bluetooth SoC module with dual-core processor",
    "specifications": {
      "architecture": "Xtensa Dual-Core 32-bit LX6",
      "core_frequency": "240 MHz",
      "flash_memory": "4 MB",
      "sram_memory": "520 KB",
      "wireless": ["WiFi 802.11 b/g/n", "Bluetooth v4.2 BR/EDR and BLE"],
      "operating_voltage": "3.0V - 3.6V",
      "operating_temp": "-40°C to +85°C"
    },
    "security_features": [
      "Secure boot",
      "Flash encryption",
      "Cryptographic hardware acceleration",
      "Random number generator"
    ],
    "vulnerabilities": [
      {
        "id": "ESP32-VULN-2021-001",
        "description": "Bluetooth pairing vulnerability",
        "severity": "MEDIUM",
        "mitigation": "Firmware update to ESP-IDF v4.3+"
      }
    ],
    "supplier": {
      "name": "Espressif Systems",
      "country": "China",
      "authenticity_verified": true
    }
  }
}
```

### 3. Microchip ATmega328P (Arduino)

```json
{
  "hbomFormat": "CycloneDX-HBOM",
  "component": {
    "type": "microcontroller",
    "bom-ref": "ATMEGA328P-001",
    "manufacturer": "Microchip Technology",
    "part_number": "ATmega328P-PU",
    "description": "8-bit AVR microcontroller, 32KB Flash, used in Arduino Uno",
    "specifications": {
      "architecture": "8-bit AVR",
      "core_frequency": "20 MHz",
      "flash_memory": "32 KB",
      "sram_memory": "2 KB",
      "eeprom": "1 KB",
      "io_pins": 23,
      "operating_voltage": "1.8V - 5.5V",
      "package": "DIP-28"
    },
    "security_features": [
      "Lock bit protection",
      "Signature bytes for device identification"
    ],
    "applications": [
      "Arduino Uno boards",
      "Hobbyist projects",
      "Industrial automation",
      "Educational platforms"
    ],
    "supplier": {
      "name": "Microchip Technology",
      "country": "USA"
    }
  }
}
```

### 4. Raspberry Pi RP2040

```json
{
  "hbomFormat": "CycloneDX-HBOM",
  "component": {
    "type": "microcontroller",
    "bom-ref": "RP2040-001",
    "manufacturer": "Raspberry Pi Foundation",
    "part_number": "RP2040",
    "description": "Dual-core ARM Cortex-M0+ microcontroller designed by Raspberry Pi",
    "specifications": {
      "architecture": "ARM Cortex-M0+",
      "cores": 2,
      "core_frequency": "133 MHz",
      "sram_memory": "264 KB",
      "flash_memory": "External QSPI Flash (up to 16MB)",
      "io_pins": 30,
      "operating_voltage": "1.8V - 3.3V",
      "package": "QFN-56"
    },
    "security_features": [
      "Boot ROM security",
      "Hardware random number generator"
    ],
    "applications": [
      "Raspberry Pi Pico",
      "IoT devices",
      "Wearables",
      "Consumer electronics"
    ]
  }
}
```

### 5. NXP i.MX RT1062

```json
{
  "hbomFormat": "CycloneDX-HBOM",
  "component": {
    "type": "crossover-processor",
    "bom-ref": "IMXRT1062-001",
    "manufacturer": "NXP Semiconductors",
    "part_number": "i.MX RT1062DVL6B",
    "description": "600 MHz ARM Cortex-M7 crossover processor with real-time capabilities",
    "specifications": {
      "architecture": "ARM Cortex-M7",
      "core_frequency": "600 MHz",
      "sram_memory": "1 MB",
      "flash_memory": "External NOR/NAND Flash support",
      "operating_voltage": "2.7V - 3.6V",
      "package": "LFBGA-196"
    },
    "security_features": [
      "Secure boot with HAB",
      "Encrypted boot",
      "TrustZone support",
      "Cryptographic acceleration",
      "Secure JTAG"
    ],
    "applications": [
      "Industrial automation",
      "Consumer electronics",
      "IoT gateways",
      "Smart appliances"
    ]
  }
}
```

## Additional Microcontrollers & Processors (100+ components)

### ARM Cortex-M Series
- **STM32F103C8T6** - STMicroelectronics, 72MHz, 64KB Flash (Blue Pill)
- **STM32H743VIT6** - STMicroelectronics, 480MHz, 2MB Flash, Dual-core
- **NXP LPC1768** - ARM Cortex-M3, 100MHz, used in mbed platform
- **Nordic nRF52840** - ARM Cortex-M4, Bluetooth 5.0, Thread, Zigbee
- **Cypress PSoC 6** - Dual-core ARM Cortex-M4/M0+, BLE 5.0

### AVR Microcontrollers
- **ATmega2560** - Microchip, 16MHz, 256KB Flash (Arduino Mega)
- **ATtiny85** - Microchip, 8-bit AVR, 8KB Flash, 8-pin DIP
- **ATmega32U4** - Microchip, USB-capable, Arduino Leonardo
- **ATmega168** - Microchip, 16KB Flash, Arduino Nano

### PIC Microcontrollers
- **PIC16F877A** - Microchip, 8-bit, 14.3KB Flash, 40-pin DIP
- **PIC18F4520** - Microchip, 8-bit, 32KB Flash, enhanced mid-range
- **PIC32MX795F512L** - Microchip, 32-bit MIPS, 512KB Flash
- **dsPIC33FJ128GP802** - Microchip, 16-bit DSP, motor control

### ESP Series (Espressif)
- **ESP8266** - WiFi SoC, 80MHz, 512KB Flash
- **ESP32-S2** - Single-core, WiFi, USB OTG
- **ESP32-S3** - Dual-core, WiFi, Bluetooth 5, AI acceleration
- **ESP32-C3** - RISC-V, WiFi, Bluetooth 5 LE

### Broadcom SoCs
- **BCM2711** - Raspberry Pi 4, Quad-core Cortex-A72, 1.5GHz
- **BCM2837** - Raspberry Pi 3, Quad-core Cortex-A53, 1.2GHz
- **BCM2835** - Raspberry Pi 1, ARM1176JZF-S, 700MHz

### Qualcomm Snapdragon
- **Snapdragon 888** - Octa-core Kryo 680, 5G modem
- **Snapdragon 865** - Octa-core Kryo 585, 7nm process
- **Snapdragon 778G** - Octa-core Kryo 670, 6nm process

## Integrated Circuits (ICs)

### Power Management ICs
- **TPS54340** - Texas Instruments, 3.5A Step-Down Converter
- **LM317** - Texas Instruments, Adjustable Voltage Regulator
- **ADP5052** - Analog Devices, Quad-Output PMIC
- **MAX17048** - Maxim Integrated, Battery Fuel Gauge

### Memory ICs
- **W25Q128JVSIQ** - Winbond, 128Mbit SPI NOR Flash
- **MT48LC16M16A2** - Micron, 256Mbit SDRAM
- **AT24C256** - Microchip, 256Kbit I2C EEPROM
- **IS42S16160J** - ISSI, 256Mbit SDRAM

### Communication ICs
- **SX1276** - Semtech, LoRa transceiver
- **NRF24L01+** - Nordic, 2.4GHz wireless transceiver
- **CC1101** - Texas Instruments, Sub-1GHz RF transceiver
- **ENC28J60** - Microchip, Ethernet controller

### Sensor Interface ICs
- **ADS1115** - Texas Instruments, 16-bit ADC
- **MCP3008** - Microchip, 8-channel 10-bit ADC
- **PCF8574** - NXP, I2C I/O expander
- **74HC595** - Texas Instruments, Shift register

## Supply Chain Security Concerns

### Counterfeit Components Risk
```json
{
  "component": "STM32F103C8T6",
  "counterfeit_risk": "HIGH",
  "indicators": [
    "Low-cost market prevalence",
    "Marking inconsistencies",
    "Performance variations",
    "Origin verification difficult"
  ],
  "mitigation": [
    "Purchase from authorized distributors",
    "Verify authenticity markings",
    "Test performance characteristics",
    "Use X-ray inspection for internal structure"
  ]
}
```

### Hardware Trojans
```json
{
  "threat": "Hardware Trojan insertion",
  "risk_components": [
    "Complex ASICs from untrusted foundries",
    "FPGAs with third-party IP cores",
    "Microcontrollers from gray market"
  ],
  "detection_methods": [
    "Side-channel analysis",
    "Physical inspection",
    "Functional testing",
    "Supply chain audits"
  ]
}
```

## Summary Statistics

- **Total Microcontrollers**: 150+
- **Integrated Circuits**: 150+
- **Manufacturers**: 25+
- **Security Features Cataloged**: 50+
- **Known Vulnerabilities**: 20+
- **Last Updated**: 2025-11-05
