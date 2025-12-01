# URL Indicators of Compromise

## Malicious Download URLs

The INDICATOR hxxps://malicious-site[.]com/payload.exe was identified distributing the MALWARE Emotet banking trojan through phishing emails targeting SECTOR financial institutions. The INDICATOR hxxp://185.220.101[.]32/trojan.dll served as a download location for the MALWARE TrickBot malware in campaigns by THREAT_ACTOR TA505.

The INDICATOR hxxps://windowsupdates-security[.]com/update/KB4592449.exe was used by the THREAT_ACTOR APT29 to distribute backdoors disguised as VENDOR Microsoft security updates. The INDICATOR hxxp://103.253.41[.]78/loader.bin provided the initial stage payload for the MALWARE Dridex banking malware operations.

The INDICATOR hxxps://secure-download[.]net/installer/setup.msi was identified distributing the MALWARE Agent Tesla keylogger through fake software update notifications. The INDICATOR hxxp://45.142.212[.]61/ransomware.exe served as the distribution point for the MALWARE Ryuk ransomware in targeted attacks.

## Phishing URLs

The INDICATOR hxxps://login-microsoftonline[.]com/oauth2/authorize was identified as a credential harvesting page impersonating VENDOR Microsoft Office 365 authentication in campaigns targeting SECTOR healthcare organizations. The INDICATOR hxxps://accounts-google[.]com/ServiceLogin mimicked VENDOR Google login pages to steal user credentials.

The INDICATOR hxxps://paypal-secure-login[.]net/webapps/signin was used in business email compromise attacks to harvest VENDOR PayPal credentials from SECTOR retail employees. The INDICATOR hxxps://amazon-account-verify[.]com/ap/signin impersonated VENDOR Amazon to steal customer account information.

The INDICATOR hxxps://docusign-document-ready[.]com/sign/12345 was observed in phishing campaigns delivering malicious documents containing MALWARE IcedID loader. The INDICATOR hxxps://dropbox-file-share[.]net/s/abc123 mimicked VENDOR Dropbox sharing links to distribute MALWARE RedLine stealer.

## Command and Control URLs

The INDICATOR hxxps://185.220.101[.]32:443/admin/panel provided command and control interface for the THREAT_ACTOR APT28 infrastructure used in campaigns against SECTOR government networks. The INDICATOR hxxp://c2-backup[.]duckdns.org/api/v1/checkin served as a beacon URL for MALWARE Cobalt Strike implants.

The INDICATOR hxxps://update-service[.]hopto.org/clients/register was identified as a C2 registration endpoint for the MALWARE Lazarus backdoor used by the THREAT_ACTOR Lazarus Group. The INDICATOR hxxp://91.219.237[.]244/gate.php functioned as a C2 gate for MALWARE Zeus banking trojan operations.

The INDICATOR hxxps://legitimate-cdn[.]com/js/analytics.js concealed C2 communications within apparently legitimate JavaScript files in campaigns by the THREAT_ACTOR APT32. The INDICATOR hxxp://api-metrics[.]azurewebsites.net/v2/telemetry was used to exfiltrate data disguised as telemetry traffic.

## Exploit Kit URLs

The INDICATOR hxxp://195.123.245[.]167/exploit/flash was identified delivering exploits for VULNERABILITY CVE-2018-4878 in VENDOR Adobe Flash Player. The INDICATOR hxxps://malvertising-redirect[.]com/ek/landing served as a landing page for the RIG exploit kit distribution.

The INDICATOR hxxp://37.220.87[.]19/exploits/ie11 was observed delivering browser exploits targeting VULNERABILITY CVE-2021-40444 in VENDOR Microsoft Internet Explorer. The INDICATOR hxxps://drive-by-download[.]net/kits/neutrino provided the Neutrino exploit kit framework to attackers.

## Watering Hole URLs

The INDICATOR hxxps://industry-conference-2024[.]com/agenda was compromised by the THREAT_ACTOR Winnti Group to serve as a watering hole targeting SECTOR defense contractors. The INDICATOR hxxp://sector-news-portal[.]org/articles/latest was identified delivering strategic web compromise exploits.

The INDICATOR hxxps://trade-association-forum[.]com/members/login was compromised to distribute MALWARE PlugX backdoor to SECTOR manufacturing companies. The INDICATOR hxxp://professional-network[.]org/events/register served malicious JavaScript targeting specific industry sectors.

## Data Exfiltration URLs

The INDICATOR hxxps://cloud-backup-sync[.]com/upload/data was identified as an exfiltration endpoint receiving stolen credentials from compromised SECTOR healthcare networks. The INDICATOR hxxp://file-transfer-secure[.]net/api/upload served as a staging point for intellectual property theft.

The INDICATOR hxxps://legitimate-cloud-storage[.]s3.amazonaws.com/uploads/victim123 was abused for data exfiltration from the CAMPAIGN targeting SECTOR financial institutions. The INDICATOR hxxp://data-sync-service[.]azurewebsites.net/backup concealed stolen data within cloud service traffic.

## Malicious Advertisement URLs

The INDICATOR hxxps://ad-network-cdn[.]com/banners/promo.html was identified serving malvertising that redirected users to exploit kit landing pages. The INDICATOR hxxp://click-tracker[.]net/redirect?id=12345 was used in malicious advertising campaigns distributing MALWARE Raccoon Stealer.

The INDICATOR hxxps://promotional-offer[.]com/claim/prize led to fake software updater pages distributing MALWARE Agent Tesla. The INDICATOR hxxp://ad-redirect-service[.]org/goto?url=malicious was observed in drive-by download attacks.

## Cryptocurrency Scam URLs

The INDICATOR hxxps://bitcoin-giveaway-official[.]com/claim was identified in cryptocurrency scam campaigns impersonating legitimate promotions. The INDICATOR hxxp://ethereum-wallet-verify[.]net/connect was used to steal cryptocurrency wallet credentials and private keys.

The INDICATOR hxxps://nft-mint-exclusive[.]com/presale/mint was observed in NFT phishing scams targeting cryptocurrency enthusiasts. The INDICATOR hxxp://defi-yield-farm[.]org/stake/connect harvested wallet credentials through fake DeFi platform interfaces.

## Mobile Malware URLs

The INDICATOR hxxp://android-app-download[.]com/apps/banking.apk distributed trojanized versions of legitimate banking applications containing MALWARE Anubis Android malware. The INDICATOR hxxps://ios-app-alternative[.]net/install/messenger served fake iOS configuration profiles.

The INDICATOR hxxp://mobile-game-hack[.]org/download/cheats.apk was identified distributing the MALWARE Cerberus Android banking trojan through game modification downloads. The INDICATOR hxxps://app-update-required[.]com/android/update led to malicious APK installations.

## Ransomware Payment URLs

The INDICATOR hxxp://darknet-payment-portal[.]onion/victim-12345 was operated by the THREAT_ACTOR Conti Group for ransom payment processing. The INDICATOR hxxps://decryption-service[.]com/pay/ticket-67890 served as a payment portal for the THREAT_ACTOR REvil ransomware operations.

The INDICATOR hxxp://file-recovery-support[.]onion/cases/abc123 was identified as infrastructure for ransomware negotiation and payment collection. The INDICATOR hxxps://restore-your-files[.]com/payment/session provided cryptocurrency payment instructions for multiple ransomware families.

## DNS Tunneling URLs

The INDICATOR hxxps://api-update-service[.]com/v1/sync?data=<base64_encoded_data> was identified performing DNS tunneling to exfiltrate data from air-gapped networks. The INDICATOR hxxp://legitimate-looking-domain[.]com/search?q=<hex_encoded_commands> concealed C2 commands within DNS queries.

The INDICATOR hxxps://cloud-metrics[.]net/collect?stats=<encoded_data> was used by the THREAT_ACTOR APT33 for covert data exfiltration through DNS channels. The INDICATOR hxxp://analytics-tracker[.]org/beacon?id=<data> tunneled stolen credentials through DNS resolution.

## API Abuse URLs

The INDICATOR hxxps://legitimate-api[.]com/v2/upload was abused by attackers to store malicious payloads on trusted infrastructure. The INDICATOR hxxp://pastebin[.]com/raw/abc123xyz was used to host encoded malware and C2 configurations.

The INDICATOR hxxps://github[.]com/malicious-user/payload-repo/releases/download/v1.0/trojan.exe distributed malware through VENDOR GitHub release artifacts. The INDICATOR hxxp://discord[.]com/api/webhooks/123456/abcdef served as a C2 channel using VENDOR Discord webhooks.

## Web Shell URLs

The INDICATOR hxxps://compromised-site[.]com/wp-content/uploads/china-chopper.php was identified as the MALWARE China Chopper webshell access point on compromised VENDOR WordPress sites. The INDICATOR hxxp://legitimate-business[.]org/assets/images/shell.aspx provided backdoor access through an ASP.NET webshell.

The INDICATOR hxxps://corporate-website[.]com/includes/config.php?cmd=<command> was observed as a command execution backdoor installed by the THREAT_ACTOR APT41. The INDICATOR hxxp://government-portal[.]gov/static/js/admin.jsp served as persistent access for cyber espionage operations.

## Social Engineering URLs

The INDICATOR hxxps://urgent-security-alert[.]com/verify/account was used in social engineering campaigns impersonating security notifications. The INDICATOR hxxp://important-document-review[.]net/files/invoice.pdf led to credential harvesting pages disguised as document viewers.

The INDICATOR hxxps://hr-policy-update[.]com/2024/new-guidelines targeted employees with fake internal communications containing MALWARE. The INDICATOR hxxp://it-helpdesk-portal[.]net/support/ticket created convincing fake support portals to steal credentials.

## Malicious Redirect Chains

The INDICATOR hxxp://click-here[.]net/r?url=hxxp://second-redirect[.]com/t?url=hxxp://final-exploit[.]org/payload represented a multi-stage redirect chain obfuscating final malicious destination. The INDICATOR hxxps://shorturl-service[.]com/abc123 was used to conceal malicious URLs in phishing campaigns.

The INDICATOR hxxp://legitimate-ad-network[.]com/click?id=12345&redir=hxxp://malware-download[.]net was observed in malvertising redirect chains. The INDICATOR hxxps://compromised-site[.]org/404.php?url=<encoded_malicious_url> leveraged compromised websites for redirection.

## IoT and Embedded Device URLs

The INDICATOR hxxp://192.168.1[.]1/cgi-bin/exploit.cgi was used to exploit VULNERABILITY CVE-2020-12345 in VENDOR IoT router firmware. The INDICATOR hxxps://firmware-update[.]net/devices/router/latest.bin distributed backdoored firmware for network devices.

The INDICATOR hxxp://iot-management[.]com/api/device/control was identified as C2 infrastructure for compromised VENDOR smart home devices. The INDICATOR hxxps://camera-config[.]org/setup/remote enabled remote access to compromised IP cameras.

## Recent Threat URLs

The INDICATOR hxxps://chatgpt-premium-unlock[.]com/register was observed in 2024 phishing campaigns exploiting interest in AI services. The INDICATOR hxxp://microsoft-copilot-beta-access[.]net/signup harvested VENDOR Microsoft 365 credentials from enterprise users.

The INDICATOR hxxps://ai-image-generator-free[.]com/create/upload was identified distributing MALWARE through fake AI service interfaces. The INDICATOR hxxp://cryptocurrency-airdrop-claim[.]org/wallet/connect was used in wallet draining scams targeting cryptocurrency holders.
