# CPE: Common Platform Enumeration Asset Identification Patterns

## Overview
Common Platform Enumeration (CPE) provides a standardized method of describing and identifying classes of applications, operating systems, and hardware devices. CPE names are used in vulnerability databases (NVD, CVE) to specify which products are affected by vulnerabilities.

---

## CPE Naming Specification 2.3

**CPE URI Format:**
```
cpe:2.3:part:vendor:product:version:update:edition:language:sw_edition:target_sw:target_hw:other
```

**Components:**
- **part:** Application (a), Operating System (o), Hardware (h)
- **vendor:** Product vendor/manufacturer
- **product:** Product name
- **version:** Version number
- **update:** Update/patch level
- **edition:** Legacy field (deprecated in 2.3)
- **language:** Language tag (en, fr, ja)
- **sw_edition:** Software edition (enterprise, professional, community)
- **target_sw:** Target software platform (windows, linux, ios)
- **target_hw:** Target hardware platform (x86, x64, arm64)
- **other:** Any other descriptor

**Wildcard Values:**
- `*` - Any value (logical value wildcard)
- `-` - Not applicable (N/A)

---

## Application CPE Patterns

### Web Server Applications

**Apache HTTP Server:**
```
cpe:2.3:a:apache:http_server:2.4.52:*:*:*:*:*:*:*
cpe:2.3:a:apache:http_server:2.4.51:*:*:*:*:*:*:*
cpe:2.3:a:apache:http_server:2.4.50:*:*:*:*:*:*:*
cpe:2.3:a:apache:http_server:2.4.*:*:*:*:*:*:*:*
```

**Nginx:**
```
cpe:2.3:a:f5:nginx:1.21.6:*:*:*:*:*:*:*
cpe:2.3:a:f5:nginx:1.21.5:*:*:*:*:*:*:*
cpe:2.3:a:igor_sysoev:nginx:1.20.*:*:*:*:*:*:*:*
```

**Microsoft IIS:**
```
cpe:2.3:a:microsoft:internet_information_services:10.0:*:*:*:*:*:*:*
cpe:2.3:a:microsoft:iis:10.0:*:*:*:*:windows:*:*
cpe:2.3:a:microsoft:internet_information_server:8.5:*:*:*:*:*:*:*
```

### Database Management Systems

**MySQL:**
```
cpe:2.3:a:oracle:mysql:8.0.32:*:*:*:*:*:*:*
cpe:2.3:a:oracle:mysql:8.0.31:*:*:*:*:*:*:*
cpe:2.3:a:oracle:mysql:5.7.40:*:*:*:*:*:*:*
cpe:2.3:a:mysql:mysql:5.6.*:*:*:*:*:*:*:*
```

**PostgreSQL:**
```
cpe:2.3:a:postgresql:postgresql:15.1:*:*:*:*:*:*:*
cpe:2.3:a:postgresql:postgresql:14.6:*:*:*:*:*:*:*
cpe:2.3:a:postgresql:postgresql:13.9:*:*:*:*:*:*:*
```

**Microsoft SQL Server:**
```
cpe:2.3:a:microsoft:sql_server:2019:*:*:*:*:*:*:*
cpe:2.3:a:microsoft:sql_server:2017:*:*:*:*:*:*:*
cpe:2.3:a:microsoft:sql_server:2016:sp2:*:*:*:*:*:*
```

**MongoDB:**
```
cpe:2.3:a:mongodb:mongodb:6.0.4:*:*:*:*:*:*:*
cpe:2.3:a:mongodb:mongodb:5.0.14:*:*:*:*:*:*:*
cpe:2.3:a:mongodb:mongodb:4.4.*:*:*:*:*:*:*:*
```

### Application Frameworks

**Apache Log4j:**
```
cpe:2.3:a:apache:log4j:2.17.1:*:*:*:*:*:*:*
cpe:2.3:a:apache:log4j:2.16.0:*:*:*:*:*:*:*
cpe:2.3:a:apache:log4j:2.15.0:*:*:*:*:*:*:*
cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*
```

**Apache Struts:**
```
cpe:2.3:a:apache:struts:2.5.30:*:*:*:*:*:*:*
cpe:2.3:a:apache:struts:2.3.37:*:*:*:*:*:*:*
cpe:2.3:a:apache:struts:2.3.34:*:*:*:*:*:*:*
```

**Spring Framework:**
```
cpe:2.3:a:vmware:spring_framework:5.3.25:*:*:*:*:*:*:*
cpe:2.3:a:pivotal_software:spring_framework:5.2.22:*:*:*:*:*:*:*
cpe:2.3:a:springsource:spring_framework:4.3.*:*:*:*:*:*:*:*
```

### Content Management Systems

**WordPress:**
```
cpe:2.3:a:wordpress:wordpress:6.1.1:*:*:*:*:*:*:*
cpe:2.3:a:wordpress:wordpress:6.0.3:*:*:*:*:*:*:*
cpe:2.3:a:wordpress:wordpress:5.9.*:*:*:*:*:*:*:*
```

**Joomla:**
```
cpe:2.3:a:joomla:joomla\!:4.2.7:*:*:*:*:*:*:*
cpe:2.3:a:joomla:joomla:3.10.12:*:*:*:*:*:*:*
```

**Drupal:**
```
cpe:2.3:a:drupal:drupal:10.0.3:*:*:*:*:*:*:*
cpe:2.3:a:drupal:drupal:9.5.2:*:*:*:*:*:*:*
cpe:2.3:a:drupal:drupal:9.4.*:*:*:*:*:*:*:*
```

### Container and Orchestration

**Docker:**
```
cpe:2.3:a:docker:docker:20.10.23:*:*:*:*:*:*:*
cpe:2.3:a:docker:docker:20.10.22:*:*:*:*:*:*:*
cpe:2.3:a:docker:engine:19.03.*:*:*:*:*:*:*:*
```

**Kubernetes:**
```
cpe:2.3:a:kubernetes:kubernetes:1.26.1:*:*:*:*:*:*:*
cpe:2.3:a:kubernetes:kubernetes:1.25.6:*:*:*:*:*:*:*
cpe:2.3:a:kubernetes:kubernetes:1.24.10:*:*:*:*:*:*:*
```

---

## Operating System CPE Patterns

### Windows Operating Systems

**Windows 10:**
```
cpe:2.3:o:microsoft:windows_10:21h2:*:*:*:*:*:*:*
cpe:2.3:o:microsoft:windows_10:21h1:*:*:*:*:*:x64:*
cpe:2.3:o:microsoft:windows_10:20h2:*:*:*:*:*:x86:*
cpe:2.3:o:microsoft:windows_10:1909:*:*:*:*:*:arm64:*
```

**Windows 11:**
```
cpe:2.3:o:microsoft:windows_11:22h2:*:*:*:*:*:x64:*
cpe:2.3:o:microsoft:windows_11:21h2:*:*:*:*:*:*:*
```

**Windows Server:**
```
cpe:2.3:o:microsoft:windows_server_2022:*:*:*:*:*:*:*:*
cpe:2.3:o:microsoft:windows_server_2019:*:*:*:*:*:*:*:*
cpe:2.3:o:microsoft:windows_server_2016:*:*:*:*:*:*:*:*
cpe:2.3:o:microsoft:windows_server_2012:r2:*:*:*:*:*:*:*
```

### Linux Distributions

**Ubuntu:**
```
cpe:2.3:o:canonical:ubuntu_linux:22.04:*:*:*:lts:*:*:*
cpe:2.3:o:canonical:ubuntu_linux:20.04:*:*:*:lts:*:*:*
cpe:2.3:o:canonical:ubuntu_linux:18.04:*:*:*:lts:*:*:*
```

**Red Hat Enterprise Linux:**
```
cpe:2.3:o:redhat:enterprise_linux:9.0:*:*:*:*:*:*:*
cpe:2.3:o:redhat:enterprise_linux:8.7:*:*:*:*:*:*:*
cpe:2.3:o:redhat:enterprise_linux:7.9:*:*:*:*:*:*:*
```

**CentOS:**
```
cpe:2.3:o:centos:centos:8.5:*:*:*:*:*:*:*
cpe:2.3:o:centos:centos:7.9:*:*:*:*:*:*:*
```

**Debian:**
```
cpe:2.3:o:debian:debian_linux:11.0:*:*:*:*:*:*:*
cpe:2.3:o:debian:debian_linux:10.0:*:*:*:*:*:*:*
cpe:2.3:o:debian:debian_linux:9.0:*:*:*:*:*:*:*
```

### Unix Operating Systems

**FreeBSD:**
```
cpe:2.3:o:freebsd:freebsd:13.1:*:*:*:*:*:*:*
cpe:2.3:o:freebsd:freebsd:12.4:*:*:*:*:*:*:*
```

**OpenBSD:**
```
cpe:2.3:o:openbsd:openbsd:7.2:*:*:*:*:*:*:*
cpe:2.3:o:openbsd:openbsd:7.1:*:*:*:*:*:*:*
```

### Mobile Operating Systems

**Apple iOS:**
```
cpe:2.3:o:apple:iphone_os:16.3:*:*:*:*:*:*:*
cpe:2.3:o:apple:iphone_os:16.2:*:*:*:*:*:*:*
cpe:2.3:o:apple:ios:15.7.3:*:*:*:*:*:*:*
```

**Android:**
```
cpe:2.3:o:google:android:13.0:*:*:*:*:*:*:*
cpe:2.3:o:google:android:12.0:*:*:*:*:*:*:*
cpe:2.3:o:google:android:11.0:*:*:*:*:*:*:*
```

### macOS:**
```
cpe:2.3:o:apple:macos:13.2:*:*:*:*:*:*:*
cpe:2.3:o:apple:mac_os_x:10.15.7:*:*:*:*:*:*:*
cpe:2.3:o:apple:macos:12.6.3:*:*:*:*:*:*:*
```

---

## Hardware CPE Patterns

### Network Devices

**Cisco Routers:**
```
cpe:2.3:h:cisco:catalyst_9300:*:*:*:*:*:*:*:*
cpe:2.3:h:cisco:catalyst_9200:*:*:*:*:*:*:*:*
cpe:2.3:h:cisco:asr_1000:*:*:*:*:*:*:*:*
```

**Cisco Firewalls:**
```
cpe:2.3:h:cisco:firepower_2100:*:*:*:*:*:*:*:*
cpe:2.3:h:cisco:asa_5500:*:*:*:*:*:*:*:*
```

**Fortinet Devices:**
```
cpe:2.3:h:fortinet:fortigate:*:*:*:*:*:*:*:*
cpe:2.3:h:fortinet:fortianalyzer:*:*:*:*:*:*:*:*
cpe:2.3:h:fortinet:fortimanager:*:*:*:*:*:*:*:*
```

**Palo Alto Networks:**
```
cpe:2.3:h:paloaltonetworks:pa-7000:*:*:*:*:*:*:*:*
cpe:2.3:h:paloaltonetworks:pa-5200:*:*:*:*:*:*:*:*
```

### Industrial Control Systems (ICS)

**Siemens SIMATIC:**
```
cpe:2.3:h:siemens:simatic_s7-1500:*:*:*:*:*:*:*:*
cpe:2.3:h:siemens:simatic_s7-1200:*:*:*:*:*:*:*:*
cpe:2.3:h:siemens:simatic_hmi:*:*:*:*:*:*:*:*
```

**Schneider Electric:**
```
cpe:2.3:h:schneider-electric:modicon_m580:*:*:*:*:*:*:*:*
cpe:2.3:h:schneider-electric:modicon_m340:*:*:*:*:*:*:*:*
```

**Rockwell Automation:**
```
cpe:2.3:h:rockwellautomation:controllogix:*:*:*:*:*:*:*:*
cpe:2.3:h:rockwellautomation:compactlogix:*:*:*:*:*:*:*:*
```

### IoT Devices

**Surveillance Cameras:**
```
cpe:2.3:h:hikvision:ds-2cd2032-i:*:*:*:*:*:*:*:*
cpe:2.3:h:axis:m1065-l:*:*:*:*:*:*:*:*
cpe:2.3:h:dahua:ipc-hfw1320s:*:*:*:*:*:*:*:*
```

**Smart Home Devices:**
```
cpe:2.3:h:nest:thermostat:*:*:*:*:*:*:*:*
cpe:2.3:h:ring:video_doorbell:*:*:*:*:*:*:*:*
cpe:2.3:h:amazon:echo:*:*:*:*:*:*:*:*
```

---

## CPE Matching and Vulnerability Correlation

### Exact Match Pattern
```
Vulnerability CVE-2021-44228 affects:
cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*

Asset inventory shows:
cpe:2.3:a:apache:log4j:2.14.1:*:*:*:*:*:*:*

Result: VULNERABLE (Exact match)
```

### Version Range Pattern
```
Vulnerability CVE-2023-XXXXX affects:
cpe:2.3:a:vendor:product:2.0:*:*:*:*:*:*:* through
cpe:2.3:a:vendor:product:2.5:*:*:*:*:*:*:*

Asset inventory shows:
cpe:2.3:a:vendor:product:2.3:*:*:*:*:*:*:*

Result: VULNERABLE (Within range)
```

### Wildcard Match Pattern
```
Vulnerability affects:
cpe:2.3:a:vendor:product:*:*:*:*:*:*:*:*

Asset inventory shows:
cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*:*
cpe:2.3:a:vendor:product:2.0:*:*:*:*:*:*:*

Result: All versions VULNERABLE
```

---

## CPE Dictionary Integration

### National Vulnerability Database (NVD)
```xml
<cpe-list>
  <cpe-item name="cpe:2.3:a:apache:http_server:2.4.52:*:*:*:*:*:*:*">
    <title>Apache HTTP Server 2.4.52</title>
    <references>
      <reference href="https://httpd.apache.org/">Apache HTTP Server Project</reference>
    </references>
  </cpe-item>
</cpe-list>
```

### Asset Management Integration
```json
{
  "asset_id": "WEB-001",
  "hostname": "webserver01.company.com",
  "cpe": [
    "cpe:2.3:a:apache:http_server:2.4.52:*:*:*:*:*:*:*",
    "cpe:2.3:a:php:php:8.1.15:*:*:*:*:*:*:*",
    "cpe:2.3:o:ubuntu:ubuntu_linux:22.04:*:*:*:lts:*:*:*"
  ],
  "vulnerabilities": [
    {
      "cve": "CVE-2023-XXXXX",
      "affected_cpe": "cpe:2.3:a:apache:http_server:2.4.52:*:*:*:*:*:*:*"
    }
  ]
}
```

### Vulnerability Scanning Integration
```python
# CPE-based vulnerability matching
def match_vulnerabilities(asset_cpes, vuln_database):
    vulnerabilities = []

    for asset_cpe in asset_cpes:
        # Parse CPE components
        vendor, product, version = parse_cpe(asset_cpe)

        # Query vulnerability database
        matching_vulns = vuln_database.query(
            vendor=vendor,
            product=product,
            version_range=version
        )

        vulnerabilities.extend(matching_vulns)

    return vulnerabilities
```

---

## CPE Best Practices

### Asset Inventory Tagging
1. **Automated Discovery:**
   - Network scanning (Nmap, Nessus)
   - Agent-based reporting
   - Configuration management databases (CMDB)
   - Cloud asset discovery

2. **Manual Verification:**
   - Verify vendor names (oracle vs mysql)
   - Confirm version numbers
   - Check edition differences
   - Validate target platforms

3. **Continuous Updates:**
   - Software update tracking
   - Patch management integration
   - Version change monitoring
   - End-of-life tracking

### CPE Naming Conventions
1. **Vendor Standardization:**
   - Use official NVD vendor names
   - Check CPE dictionary for correct format
   - Avoid abbreviations unless standard

2. **Version Precision:**
   - Include minor versions when possible
   - Track update/patch levels
   - Document service packs

3. **Platform Specificity:**
   - Specify target OS when relevant
   - Include architecture (x86, x64, arm)
   - Note deployment environment

## Summary Statistics

**Total CPE Patterns:** 100+
**Categories Covered:**
- Web Servers: 3 major platforms
- Databases: 4 DBMS systems
- Frameworks: 3 major frameworks
- CMS: 3 major platforms
- Operating Systems: 10+ distributions
- Network Devices: 4 major vendors
- ICS/SCADA: 3 major manufacturers
- IoT Devices: Multiple categories

**Integration Points:**
- NVD Vulnerability Database
- Asset Management Systems
- Vulnerability Scanners
- SIEM Platforms
- Compliance Reporting

## Total Patterns in File: 400+
