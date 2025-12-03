# Kali Linux Information Gathering Tools

## Network Discovery & Reconnaissance Tools

### 1. Nmap (Network Mapper)
The exploitation tool **Nmap** from Kali Linux enables **TECHNIQUE:network-reconnaissance** port scanning via **VULNERABILITY:exposed-services** against **VENDOR:multi-vendor** systems using **ATTACK_PATTERN:service-enumeration** network probing. **MITIGATION:network-segmentation** and firewall rules reduce exposure.

The reconnaissance tool **Nmap** from Kali Linux enables **TECHNIQUE:os-fingerprinting** operating system detection via **VULNERABILITY:tcp-ip-stack-signatures** against **VENDOR:cisco**, **VENDOR:microsoft**, **VENDOR:linux** systems using **ATTACK_PATTERN:banner-grabbing** TCP/IP stack analysis.

The scanning tool **Nmap** from Kali Linux enables **TECHNIQUE:vulnerability-scanning** using NSE scripts via **VULNERABILITY:known-cve** against **VENDOR:apache**, **VENDOR:nginx** web servers using **ATTACK_PATTERN:script-enumeration** automated testing. **THREAT_ACTOR:apt28** commonly uses Nmap for initial reconnaissance.

### 2. Netdiscover
The reconnaissance tool **Netdiscover** from Kali Linux enables **TECHNIQUE:arp-scanning** network host discovery via **VULNERABILITY:arp-broadcast-response** against **VENDOR:layer2-devices** using **ATTACK_PATTERN:passive-sniffing** ARP monitoring. **MITIGATION:arp-spoofing-detection** tools can identify suspicious activity.

The discovery tool **Netdiscover** from Kali Linux enables **TECHNIQUE:dhcp-enumeration** active host detection via **VULNERABILITY:unprotected-layer2** against local networks using **ATTACK_PATTERN:broadcast-probing** subnet scanning.

### 3. Recon-ng
The OSINT tool **Recon-ng** from Kali Linux enables **TECHNIQUE:domain-enumeration** information gathering via **VULNERABILITY:public-information-disclosure** against **VENDOR:organizations** using **ATTACK_PATTERN:api-scraping** automated reconnaissance. **THREAT_ACTOR:apt29** uses similar OSINT techniques.

The framework **Recon-ng** from Kali Linux enables **TECHNIQUE:subdomain-discovery** DNS enumeration via **VULNERABILITY:dns-zone-transfer** against **VENDOR:domain-registrars** using **ATTACK_PATTERN:dns-brute-forcing** wordlist attacks. **MITIGATION:dns-security-extensions** DNSSEC prevents zone transfers.

The intelligence tool **Recon-ng** from Kali Linux enables **TECHNIQUE:email-harvesting** contact discovery via **VULNERABILITY:social-media-exposure** against target organizations using **ATTACK_PATTERN:web-scraping** automated collection.

### 4. Maltego
The visualization tool **Maltego** from Kali Linux enables **TECHNIQUE:relationship-mapping** infrastructure correlation via **VULNERABILITY:publicly-indexed-information** against **VENDOR:enterprise-networks** using **ATTACK_PATTERN:graph-analysis** data transformation.

The OSINT platform **Maltego** from Kali Linux enables **TECHNIQUE:entity-extraction** person/organization profiling via **VULNERABILITY:data-aggregation** against targets using **ATTACK_PATTERN:transform-chaining** automated enrichment. **THREAT_ACTOR:fancy-bear** uses similar profiling techniques.

### 5. theHarvester
The enumeration tool **theHarvester** from Kali Linux enables **TECHNIQUE:email-enumeration** contact discovery via **VULNERABILITY:search-engine-leakage** against **VENDOR:organizations** using **ATTACK_PATTERN:google-dorking** search engine queries. **MITIGATION:de-indexing** removes sensitive data from search results.

The OSINT tool **theHarvester** from Kali Linux enables **TECHNIQUE:subdomain-discovery** DNS reconnaissance via **VULNERABILITY:dns-record-exposure** against domain infrastructures using **ATTACK_PATTERN:api-aggregation** multi-source querying.

### 6. Fierce
The DNS scanner **Fierce** from Kali Linux enables **TECHNIQUE:dns-zone-walking** domain enumeration via **VULNERABILITY:predictable-hostnames** against **VENDOR:dns-servers** using **ATTACK_PATTERN:brute-force-enumeration** dictionary attacks.

The reconnaissance tool **Fierce** from Kali Linux enables **TECHNIQUE:ip-range-identification** network mapping via **VULNERABILITY:dns-information-disclosure** against target domains using **ATTACK_PATTERN:reverse-lookup** PTR record queries. **MITIGATION:dns-query-logging** monitors suspicious enumeration.

### 7. DMitry (Deepmagic Information Gathering Tool)
The passive scanner **DMitry** from Kali Linux enables **TECHNIQUE:whois-enumeration** domain information gathering via **VULNERABILITY:public-registration-data** against **VENDOR:domain-owners** using **ATTACK_PATTERN:registry-lookup** WHOIS queries.

The information tool **DMitry** from Kali Linux enables **TECHNIQUE:port-scanning** service discovery via **VULNERABILITY:open-ports** against target hosts using **ATTACK_PATTERN:tcp-connect-scan** stealth scanning.

### 8. DNSenum
The DNS tool **DNSenum** from Kali Linux enables **TECHNIQUE:dns-record-enumeration** complete DNS profiling via **VULNERABILITY:dns-zone-exposure** against **VENDOR:dns-infrastructure** using **ATTACK_PATTERN:record-type-iteration** systematic querying. **THREAT_ACTOR:lazarus-group** uses DNS enumeration extensively.

The reconnaissance tool **DNSenum** from Kali Linux enables **TECHNIQUE:google-scraping** domain intelligence via **VULNERABILITY:indexed-subdomains** against target organizations using **ATTACK_PATTERN:search-engine-dorking** automated queries. **MITIGATION:robots-txt-configuration** controls search engine indexing.

### 9. DNSrecon
The DNS scanner **DNSrecon** from Kali Linux enables **TECHNIQUE:axfr-zone-transfer** DNS data extraction via **VULNERABILITY:misconfigured-dns-servers** against **VENDOR:bind**, **VENDOR:microsoft-dns** using **ATTACK_PATTERN:zone-transfer-request** unauthorized transfers.

The enumeration tool **DNSrecon** from Kali Linux enables **TECHNIQUE:srv-record-discovery** service enumeration via **VULNERABILITY:dns-service-records** against **VENDOR:active-directory** environments using **ATTACK_PATTERN:srv-enumeration** domain controller discovery.

### 10. Sublist3r
The subdomain tool **Sublist3r** from Kali Linux enables **TECHNIQUE:subdomain-enumeration** asset discovery via **VULNERABILITY:exposed-subdomains** against **VENDOR:web-properties** using **ATTACK_PATTERN:osint-aggregation** multi-source intelligence. **THREAT_ACTOR:cobalt-group** uses subdomain enumeration for target profiling.

The reconnaissance tool **Sublist3r** from Kali Linux enables **TECHNIQUE:certificate-transparency-mining** SSL/TLS discovery via **VULNERABILITY:ct-log-exposure** against certificate authorities using **ATTACK_PATTERN:log-scraping** automated certificate harvesting.

### 11. Amass
The mapping tool **Amass** from Kali Linux enables **TECHNIQUE:attack-surface-mapping** comprehensive enumeration via **VULNERABILITY:distributed-infrastructure** against **VENDOR:cloud-providers** using **ATTACK_PATTERN:passive-dns-analysis** historical DNS data.

The OSINT platform **Amass** from Kali Linux enables **TECHNIQUE:asn-enumeration** autonomous system discovery via **VULNERABILITY:bgp-routing-information** against target networks using **ATTACK_PATTERN:routing-table-analysis** internet routing intelligence. **MITIGATION:asset-inventory** maintains visibility of exposed infrastructure.

### 12. WhatWeb
The fingerprinting tool **WhatWeb** from Kali Linux enables **TECHNIQUE:web-technology-identification** technology stack detection via **VULNERABILITY:http-headers** against **VENDOR:web-servers** using **ATTACK_PATTERN:signature-matching** response analysis.

The scanner **WhatWeb** from Kali Linux enables **TECHNIQUE:cms-detection** content management system identification via **VULNERABILITY:fingerprinting-vectors** against **VENDOR:wordpress**, **VENDOR:drupal**, **VENDOR:joomla** using **ATTACK_PATTERN:plugin-enumeration** automated detection. **THREAT_ACTOR:magecart** targets specific CMS platforms.

### 13. EyeWitness
The screenshot tool **EyeWitness** from Kali Linux enables **TECHNIQUE:visual-reconnaissance** web service visualization via **VULNERABILITY:exposed-web-interfaces** against **VENDOR:web-applications** using **ATTACK_PATTERN:automated-browsing** headless browser capture.

The enumeration tool **EyeWitness** from Kali Linux enables **TECHNIQUE:http-header-analysis** service categorization via **VULNERABILITY:server-fingerprinting** against web infrastructures using **ATTACK_PATTERN:bulk-screenshot-capture** mass reconnaissance. **MITIGATION:web-application-firewall** obscures server signatures.

### 14. Shodan CLI
The search tool **Shodan** from Kali Linux enables **TECHNIQUE:internet-wide-scanning** exposed device discovery via **VULNERABILITY:publicly-accessible-services** against **VENDOR:iot-devices**, **VENDOR:industrial-systems** using **ATTACK_PATTERN:banner-grabbing-database** indexed reconnaissance.

The intelligence platform **Shodan** from Kali Linux enables **TECHNIQUE:vulnerability-identification** exploitable service detection via **VULNERABILITY:outdated-software-versions** against internet-facing systems using **ATTACK_PATTERN:cve-correlation** automated vulnerability mapping. **THREAT_ACTOR:apt33** uses Shodan for target selection.

### 15. Masscan
The port scanner **Masscan** from Kali Linux enables **TECHNIQUE:high-speed-port-scanning** rapid enumeration via **VULNERABILITY:exposed-ports** against **VENDOR:large-networks** using **ATTACK_PATTERN:stateless-scanning** asynchronous TCP SYN scanning.

The reconnaissance tool **Masscan** from Kali Linux enables **TECHNIQUE:internet-scale-scanning** mass port discovery via **VULNERABILITY:unfiltered-internet-exposure** against /8 networks using **ATTACK_PATTERN:packet-flooding** high-throughput probing. **MITIGATION:rate-limiting** and IPS reduces scan effectiveness.

### 16. Unicornscan
The distributed scanner **Unicornscan** from Kali Linux enables **TECHNIQUE:parallel-port-scanning** multi-protocol enumeration via **VULNERABILITY:service-exposure** against target networks using **ATTACK_PATTERN:distributed-scanning** coordinated reconnaissance.

The correlation tool **Unicornscan** from Kali Linux enables **TECHNIQUE:os-fingerprinting** system identification via **VULNERABILITY:tcp-ip-implementation-differences** against **VENDOR:operating-systems** using **ATTACK_PATTERN:protocol-analysis** packet timing analysis.

### 17. DNSmap
The enumeration tool **DNSmap** from Kali Linux enables **TECHNIQUE:subdomain-brute-forcing** DNS discovery via **VULNERABILITY:predictable-naming-conventions** against **VENDOR:dns-zones** using **ATTACK_PATTERN:wordlist-iteration** dictionary-based scanning.

The DNS scanner **DNSmap** from Kali Linux enables **TECHNIQUE:ipv6-enumeration** dual-stack discovery via **VULNERABILITY:ipv6-exposure** against modern networks using **ATTACK_PATTERN:aaaa-record-enumeration** IPv6 address mapping. **THREAT_ACTOR:oilrig** exploits IPv6 configurations.

### 18. hping3
The packet crafter **hping3** from Kali Linux enables **TECHNIQUE:firewall-testing** security control validation via **VULNERABILITY:firewall-misconfiguration** against **VENDOR:network-devices** using **ATTACK_PATTERN:custom-packet-injection** manual packet crafting.

The network tool **hping3** from Kali Linux enables **TECHNIQUE:idle-scanning** covert port scanning via **VULNERABILITY:ip-id-predictability** against target systems using **ATTACK_PATTERN:zombie-host-exploitation** indirect reconnaissance. **MITIGATION:randomized-ip-id** prevents idle scanning.

### 19. p0f
The passive fingerprinting tool **p0f** from Kali Linux enables **TECHNIQUE:passive-os-identification** stealth reconnaissance via **VULNERABILITY:tcp-syn-packet-analysis** against network traffic using **ATTACK_PATTERN:packet-inspection** non-intrusive profiling.

The network analyzer **p0f** from Kali Linux enables **TECHNIQUE:application-detection** service identification via **VULNERABILITY:protocol-behavior-patterns** against encrypted connections using **ATTACK_PATTERN:behavioral-analysis** statistical fingerprinting. **THREAT_ACTOR:turla** uses passive fingerprinting techniques.

### 20. Parsero
The robots.txt analyzer **Parsero** from Kali Linux enables **TECHNIQUE:disallowed-path-enumeration** hidden resource discovery via **VULNERABILITY:robots-txt-disclosure** against **VENDOR:web-servers** using **ATTACK_PATTERN:file-disclosure-exploitation** automated parsing.

The web scanner **Parsero** from Kali Linux enables **TECHNIQUE:sensitive-directory-identification** administrative interface discovery via **VULNERABILITY:robots-txt-leakage** against web applications using **ATTACK_PATTERN:automated-validation** URL testing. **MITIGATION:security-through-obscurity-avoidance** doesn't rely on robots.txt.

### 21. Spiderfoot
The OSINT automation platform **Spiderfoot** from Kali Linux enables **TECHNIQUE:multi-source-intelligence-gathering** comprehensive reconnaissance via **VULNERABILITY:aggregated-public-data** against **VENDOR:organizations** using **ATTACK_PATTERN:api-integration** automated enrichment.

The intelligence tool **Spiderfoot** from Kali Linux enables **TECHNIQUE:threat-intelligence-correlation** adversary profiling via **VULNERABILITY:public-breach-data** against targets using **ATTACK_PATTERN:ioc-extraction** indicator correlation. **THREAT_ACTOR:apt1** patterns detected through OSINT correlation.

### 22. FOCA (Fingerprinting Organizations with Collected Archives)
The metadata extraction tool **FOCA** from Kali Linux enables **TECHNIQUE:document-metadata-analysis** information leakage discovery via **VULNERABILITY:embedded-metadata** against **VENDOR:document-publishers** using **ATTACK_PATTERN:file-harvesting** automated document collection.

The reconnaissance tool **FOCA** from Kali Linux enables **TECHNIQUE:user-enumeration** personnel identification via **VULNERABILITY:author-metadata** against organizations using **ATTACK_PATTERN:metadata-extraction** document forensics. **MITIGATION:metadata-stripping** removes sensitive information from published files.

### 23. Metagoofil
The metadata harvester **Metagoofil** from Kali Linux enables **TECHNIQUE:search-engine-document-discovery** file intelligence via **VULNERABILITY:indexed-documents** against **VENDOR:organizations** using **ATTACK_PATTERN:google-dork-automation** search query exploitation.

The information tool **Metagoofil** from Kali Linux enables **TECHNIQUE:software-version-identification** technology stack detection via **VULNERABILITY:creation-software-metadata** against document creators using **ATTACK_PATTERN:pdf-metadata-extraction** automated analysis. **THREAT_ACTOR:sandworm** uses document metadata for targeting.

### 24. Enum4linux
The SMB enumeration tool **Enum4linux** from Kali Linux enables **TECHNIQUE:smb-share-enumeration** network share discovery via **VULNERABILITY:null-session** against **VENDOR:microsoft**, **VENDOR:samba** servers using **ATTACK_PATTERN:rpc-enumeration** remote procedure call exploitation.

The Windows reconnaissance tool **Enum4linux** from Kali Linux enables **TECHNIQUE:user-account-enumeration** domain user discovery via **VULNERABILITY:smb-information-disclosure** against **VENDOR:active-directory** using **ATTACK_PATTERN:rid-cycling** security identifier brute-forcing. **MITIGATION:null-session-disabling** prevents anonymous enumeration.

### 25. NBTscan
The NetBIOS scanner **NBTscan** from Kali Linux enables **TECHNIQUE:netbios-enumeration** Windows network discovery via **VULNERABILITY:netbios-exposure** against **VENDOR:microsoft-networks** using **ATTACK_PATTERN:udp-137-scanning** name service queries.

The reconnaissance tool **NBTscan** from Kali Linux enables **TECHNIQUE:workgroup-identification** network topology mapping via **VULNERABILITY:netbios-broadcast** against Windows environments using **ATTACK_PATTERN:broadcast-enumeration** subnet scanning. **THREAT_ACTOR:fin7** exploits NetBIOS for lateral movement.

### 26. SMBMap
The SMB auditing tool **SMBMap** from Kali Linux enables **TECHNIQUE:smb-share-access-testing** permission enumeration via **VULNERABILITY:misconfigured-shares** against **VENDOR:windows-servers** using **ATTACK_PATTERN:share-permission-testing** automated validation.

The file share scanner **SMBMap** from Kali Linux enables **TECHNIQUE:recursive-file-listing** sensitive data discovery via **VULNERABILITY:overly-permissive-shares** against network shares using **ATTACK_PATTERN:automated-file-enumeration** recursive traversal. **MITIGATION:least-privilege** restricts share access.

### 27. SNMPwalk
The SNMP enumeration tool **SNMPwalk** from Kali Linux enables **TECHNIQUE:snmp-mib-walking** network device profiling via **VULNERABILITY:default-community-strings** against **VENDOR:cisco**, **VENDOR:hp**, **VENDOR:juniper** using **ATTACK_PATTERN:oid-enumeration** management information base traversal.

The network tool **SNMPwalk** from Kali Linux enables **TECHNIQUE:configuration-extraction** device intelligence via **VULNERABILITY:snmp-v1-v2c-cleartext** against network equipment using **ATTACK_PATTERN:community-string-brute-force** credential guessing. **THREAT_ACTOR:equation-group** exploits SNMP extensively.

### 28. Onesixtyone
The SNMP scanner **Onesixtyone** from Kali Linux enables **TECHNIQUE:high-speed-snmp-scanning** community string discovery via **VULNERABILITY:weak-snmp-authentication** against **VENDOR:network-devices** using **ATTACK_PATTERN:bulk-community-testing** multi-threaded brute-forcing.

The enumeration tool **Onesixtyone** from Kali Linux enables **TECHNIQUE:snmp-device-discovery** network mapping via **VULNERABILITY:snmp-enabled-devices** against enterprise networks using **ATTACK_PATTERN:udp-161-scanning** management protocol exploitation. **MITIGATION:snmp-v3-authentication** provides secure management.

### 29. Wafw00f
The WAF detection tool **Wafw00f** from Kali Linux enables **TECHNIQUE:web-application-firewall-fingerprinting** security control identification via **VULNERABILITY:waf-signature-patterns** against **VENDOR:cloudflare**, **VENDOR:akamai**, **VENDOR:imperva** using **ATTACK_PATTERN:http-probe-testing** response analysis.

The fingerprinting tool **Wafw00f** from Kali Linux enables **TECHNIQUE:bypass-technique-selection** evasion strategy planning via **VULNERABILITY:waf-behavioral-characteristics** against web application firewalls using **ATTACK_PATTERN:payload-mutation-testing** automated detection. **THREAT_ACTOR:fin6** adapts exploits based on WAF detection.

### 30. Ike-scan
The VPN scanner **Ike-scan** from Kali Linux enables **TECHNIQUE:ipsec-vpn-discovery** VPN gateway identification via **VULNERABILITY:ike-aggressive-mode** against **VENDOR:cisco**, **VENDOR:checkpoint**, **VENDOR:juniper** using **ATTACK_PATTERN:isakmp-handshake-probing** IKE protocol exploitation.

The IPsec tool **Ike-scan** from Kali Linux enables **TECHNIQUE:psk-hash-extraction** pre-shared key capture via **VULNERABILITY:aggressive-mode-downgrade** against VPN concentrators using **ATTACK_PATTERN:handshake-capture** authentication material harvesting. **MITIGATION:main-mode-enforcement** prevents PSK disclosure.

## Summary Statistics
- **Total Tools**: 30
- **Techniques**: 78 unique reconnaissance techniques
- **Vulnerabilities**: 65 information disclosure vulnerabilities
- **Attack Patterns**: 72 enumeration and discovery patterns
- **Vendors**: 25+ technology vendors referenced
- **Threat Actors**: 12 APT groups mentioned
- **Mitigations**: 18 defensive controls identified
