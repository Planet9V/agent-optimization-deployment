# Network Traffic and Protocol Indicators of Compromise

## User-Agent String Indicators

The INDICATOR "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)" was observed in command and control traffic from the MALWARE TrickBot targeting SECTOR financial institutions with outdated browser strings. The INDICATOR "User-Agent: python-requests/2.18.4" was identified in automated data exfiltration by the THREAT_ACTOR APT32 in campaigns against SECTOR government organizations.

The INDICATOR "Go-http-client/1.1" was used by the MALWARE Cobalt Strike beacons in post-exploitation operations by multiple THREAT_ACTOR groups. The INDICATOR "curl/7.64.0" was observed in reconnaissance and vulnerability scanning activities targeting SECTOR cloud infrastructure.

The INDICATOR "okhttp/3.12.0" was identified in Android-based MALWARE Cerberus banking trojan communications. The INDICATOR "User-Agent: TeslaCrypt" was used by ransomware for C2 beacon traffic in campaigns against SECTOR healthcare organizations.

## DNS Query Pattern Indicators

The INDICATOR "malware.example.com IN TXT" queries were observed performing DNS tunneling to exfiltrate data from air-gapped networks in campaigns by THREAT_ACTOR APT33. The INDICATOR "*.no-ip.org IN A" represented dynamic DNS queries associated with MALWARE Emotet command and control infrastructure.

The INDICATOR "dga-domain-[random-string].com IN A" matched Domain Generation Algorithm patterns used by the MALWARE Conficker worm for resilient C2 communications. The INDICATOR "update-service.duckdns.org IN A" was identified as dynamic DNS used by the THREAT_ACTOR Lazarus Group.

The INDICATOR "*.ngrok.io IN A" was observed in unauthorized tunneling activities creating covert channels from compromised SECTOR corporate networks. The INDICATOR "beacon-[hex-string].cloudfront.net IN A" concealed C2 traffic through legitimate VENDOR Amazon CloudFront infrastructure.

## HTTP Header Indicators

The INDICATOR "X-Session-ID: [Base64-encoded-commands]" was used by the THREAT_ACTOR APT28 to send encoded commands in HTTP headers disguising C2 communications. The INDICATOR "Cookie: session=[malicious-payload]" was identified transmitting malware payloads through HTTP cookies.

The INDICATOR "Accept-Encoding: gzip, deflate, malware" contained suspicious encoding methods used in MALWARE Agent Tesla keylogger communications. The INDICATOR "Referer: http://malicious-domain.com/payload" was observed in exploit kit redirect chains.

The INDICATOR "Authorization: Bearer [stolen-oauth-token]" was used by attackers leveraging compromised API tokens in the CAMPAIGN targeting SECTOR cloud services. The INDICATOR "X-Forwarded-For: 10.0.0.1" concealed true source IPs using proxy header manipulation.

## TLS/SSL Certificate Indicators

The INDICATOR "CN=localhost, O=Company, C=US" self-signed certificate was used by the MALWARE Emotet for encrypted C2 communications. The INDICATOR "CN=*.cloudflare.com, O=Fake Certificate Authority" represented fraudulent certificates in man-in-the-middle attacks.

The INDICATOR "Serial Number: 00:01:02:03:04:05:06:07:08:09" matched certificates associated with the THREAT_ACTOR APT29 infrastructure in diplomatic espionage campaigns. The INDICATOR "Subject Alternative Name: malware-c2.example.com" was identified in phishing infrastructure SSL certificates.

## Port and Protocol Indicators

The INDICATOR "TCP port 4444" was commonly observed in MALWARE Metasploit reverse shell communications and penetration testing tools misused by attackers. The INDICATOR "TCP port 8888" was used by the MALWARE TrickBot for proxy communications and lateral movement operations.

The INDICATOR "UDP port 53 with TCP-like traffic" indicated DNS tunneling for covert data exfiltration by the THREAT_ACTOR APT41. The INDICATOR "TCP port 1337" was identified in leetspeak-named backdoor communications used by various THREAT_ACTOR groups.

The INDICATOR "TCP port 31337" (elite) was used by the MALWARE BackOrifice remote access trojan and later adopted by other malware families. The INDICATOR "Non-standard port 8443 HTTPS" was observed in C2 traffic attempting to blend with legitimate encrypted traffic.

## Network Protocol Anomalies

The INDICATOR "ICMP payload size > 1024 bytes" was identified in ICMP tunneling used for covert command and control by THREAT_ACTOR groups. The INDICATOR "SMB v1 traffic from external IPs" represented exploitation attempts targeting VULNERABILITY CVE-2017-0144 (EternalBlue).

The INDICATOR "RDP connection from TOR exit nodes" indicated unauthorized remote access attempts through anonymization networks. The INDICATOR "SSH traffic on port 443" was used to disguise SSH communications as HTTPS traffic for firewall bypass.

The INDICATOR "NTP amplification requests" were observed in DDoS attacks launched by botnets including MALWARE Mirai variants. The INDICATOR "LLMNR poisoning traffic" was identified in internal network reconnaissance by the THREAT_ACTOR APT32.

## Beacon Interval Indicators

The INDICATOR "HTTP GET every 60 seconds to /api/v1/status" represented regular beaconing pattern from MALWARE Cobalt Strike implants. The INDICATOR "HTTPS POST every 5 minutes to /updates/check" was identified as C2 beacon traffic from the MALWARE TrickBot.

The INDICATOR "DNS query every 30 seconds to update.example.com" indicated persistent malware beaconing for command retrieval. The INDICATOR "Regular TCP connections every 120 seconds" matched the timing pattern of MALWARE Emotet C2 communications.

## Data Exfiltration Indicators

The INDICATOR "Large outbound HTTP POST to pastebin.com" was observed in data exfiltration operations using legitimate paste services. The INDICATOR "Bulk FTP upload to external IP" indicated unauthorized data transfer from compromised SECTOR healthcare networks.

The INDICATOR "HTTPS upload to cloud storage with unusual volume" was identified in intellectual property theft from SECTOR technology companies. The INDICATOR "Base64-encoded data in DNS TXT queries" represented DNS tunneling exfiltration by THREAT_ACTOR APT33.

## Network Scanning Indicators

The INDICATOR "SYN scan across entire subnet" was observed in reconnaissance activities by THREAT_ACTOR groups mapping network topology. The INDICATOR "Aggressive port scanning 1-65535" indicated automated vulnerability discovery attempts.

The INDICATOR "SMB enumeration attempts" were identified in lateral movement reconnaissance by the MALWARE TrickBot targeting SECTOR financial institutions. The INDICATOR "LDAP queries for entire Active Directory" represented credential harvesting and privilege escalation attempts.

## VPN and Tunneling Indicators

The INDICATOR "OpenVPN traffic to suspicious endpoint" was used by the THREAT_ACTOR APT29 to establish encrypted tunnels from compromised networks. The INDICATOR "SSH tunnel to external destination" indicated unauthorized data exfiltration channels.

The INDICATOR "VPN connection with certificate mismatch" represented man-in-the-middle attacks on remote access infrastructure. The INDICATOR "Tor traffic from corporate network" was identified as anonymized communications from compromised systems.

## Malicious Download Patterns

The INDICATOR "Direct .exe download from IP address" bypassed domain reputation systems in MALWARE distribution campaigns. The INDICATOR "PowerShell download cradle: IEX(New-Object Net.WebClient).DownloadString" was observed in fileless malware delivery.

The INDICATOR "Multiple sequential .dll downloads" indicated staged payload delivery by MALWARE loaders. The INDICATOR "Executable download masked as .jpg" represented file extension manipulation in phishing campaigns.

## Lateral Movement Indicators

The INDICATOR "PsExec remote execution" was used by the THREAT_ACTOR groups for lateral movement across SECTOR enterprise networks. The INDICATOR "WMI command execution on remote hosts" indicated administrative tool abuse for spreading malware.

The INDICATOR "Multiple RDP connections from single host" represented compromised credentials being used for lateral movement. The INDICATOR "SMB file transfer to multiple internal hosts" was identified in ransomware propagation by MALWARE Ryuk.

## Command and Control Protocol Indicators

The INDICATOR "HTTP GET with encoded commands in Cookie header" was used by the MALWARE Agent Tesla for receiving attacker commands. The INDICATOR "DNS TXT responses containing shellcode" indicated DNS-based C2 communications.

The INDICATOR "HTTPS traffic with custom cipher suite" was identified in APT malware using non-standard encryption to evade detection. The INDICATOR "Websocket connections for bidirectional C2" were observed in modern malware families establishing persistent communications.

## Cloud Service Abuse Indicators

The INDICATOR "GitHub API access for payload hosting" was used to leverage legitimate VENDOR GitHub infrastructure for malware distribution. The INDICATOR "AWS S3 buckets for data exfiltration" indicated abuse of VENDOR Amazon cloud storage.

The INDICATOR "Google Drive API for C2 communications" was identified in campaigns using legitimate cloud services for command channels. The INDICATOR "Microsoft OneDrive sync with unusual patterns" represented data theft through VENDOR Microsoft cloud services.

## Cryptocurrency Mining Indicators

The INDICATOR "Stratum mining protocol traffic" was observed in cryptomining operations by the MALWARE XMRig on compromised servers. The INDICATOR "Connection to mining pool addresses" indicated unauthorized cryptocurrency mining on SECTOR cloud computing resources.

The INDICATOR "High CPU usage with network traffic to mining endpoints" was identified in cryptojacking malware infections. The INDICATOR "Monero mining traffic patterns" represented the most common cryptocurrency mined by malware.

## Zero-Day Exploitation Indicators

The INDICATOR "Unusual HTTP methods (PROPFIND, MKCOL)" were observed exploiting VULNERABILITY CVE-2021-26855 in VENDOR Microsoft Exchange servers. The INDICATOR "SMBv3 compression negotiation exploit" indicated attempts to leverage VULNERABILITY CVE-2020-0796 (SMBGhost).

The INDICATOR "Malformed PDF requesting JavaScript execution" was identified in exploit documents targeting VULNERABILITY CVE-2021-40444. The INDICATOR "Specially crafted JPEG with embedded exploit" represented zero-day image parser vulnerabilities.

## Supply Chain Attack Network Indicators

The INDICATOR "Software update traffic to compromised vendor domain" was observed in the CAMPAIGN targeting VENDOR SolarWinds supply chain. The INDICATOR "Trusted certificate from compromised CA" indicated supply chain compromise of certificate authorities.

The INDICATOR "Package repository injection traffic" was identified in attacks against software distribution infrastructure. The INDICATOR "Backdoored library download from legitimate CDN" represented compromised content delivery networks.

## Recent Threat Network Indicators

The INDICATOR "ChatGPT API abuse for automated phishing" was observed in 2024 campaigns using AI services for attack automation. The INDICATOR "Kubernetes API unauthorized access" indicated cloud-native attacks against container orchestration platforms.

The INDICATOR "GraphQL endpoint enumeration" was identified in reconnaissance against modern API architectures. The INDICATOR "WebAssembly payload delivery" represented emerging techniques for browser-based malware execution.

## DDoS Attack Indicators

The INDICATOR "UDP flood from botnet IPs" was observed in distributed denial of service attacks by MALWARE Mirai variants. The INDICATOR "SYN flood with spoofed source addresses" indicated reflection attacks amplifying traffic volume.

The INDICATOR "Application-layer HTTP flood" was identified in sophisticated DDoS attacks targeting SECTOR financial services. The INDICATOR "DNS amplification from open resolvers" represented volumetric attacks exploiting misconfigured DNS servers.
