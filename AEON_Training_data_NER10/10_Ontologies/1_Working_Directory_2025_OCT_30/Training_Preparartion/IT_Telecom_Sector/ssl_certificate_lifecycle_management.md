# SSL/TLS Certificate Lifecycle Management Operations

## Overview
SSL/TLS certificate lifecycle management encompasses certificate request generation, validation, installation, renewal automation, and revocation procedures ensuring secure encrypted communications for websites, APIs, and internal applications while preventing costly service outages due to expired certificates.

## Operational Procedures

### 1. Certificate Signing Request (CSR) Generation
- **Private Key Creation**: 2048-bit or 4096-bit RSA private key generated and securely stored; never transmitted to CA or third parties
- **Subject Information**: CSR includes Common Name (CN), Organization (O), Organizational Unit (OU), Country (C), State/Province (ST), Locality (L)
- **Subject Alternative Names (SANs)**: Multi-domain certificates specify additional hostnames in SAN extension (www.example.com, api.example.com)
- **Key Usage Extensions**: CSR specifies intended usage (serverAuth for web servers, clientAuth for client certificates, emailProtection for S/MIME)

### 2. Domain Control Validation (DCV)
- **Email Validation**: CA sends validation email to admin@domain.com or postmaster@domain.com; link click confirms domain control
- **DNS TXT Record**: CA provides TXT record to be published at _acme-challenge.example.com; CA queries DNS to verify presence
- **HTTP File Upload**: CA provides specific file to be placed at http://example.com/.well-known/pki-validation/; CA retrieves file to validate
- **Organization Validation (OV)**: Extended validation requiring legal entity verification via business registries and phone callback

### 3. Certificate Installation and Configuration
- **Certificate Chain Construction**: Server certificate + intermediate CA certificates + root CA certificate form complete trust chain
- **Web Server Configuration**: Apache (SSLCertificateFile, SSLCertificateKeyFile, SSLCertificateChainFile), Nginx (ssl_certificate, ssl_certificate_key)
- **SSL/TLS Protocol Selection**: TLS 1.2 minimum (TLS 1.0/1.1 deprecated); TLS 1.3 preferred for performance and security
- **Cipher Suite Configuration**: Strong ciphers only (AES-GCM, ChaCha20-Poly1305); weak ciphers (RC4, 3DES, export ciphers) explicitly disabled

### 4. Automated Certificate Renewal
- **ACME Protocol (Let's Encrypt)**: Certbot, acme.sh, and other clients automate certificate request, validation, and renewal every 60 days
- **Renewal Threshold**: Automated renewal triggered 30 days before expiration providing buffer for retry attempts on failures
- **Post-Renewal Hooks**: Scripts reload web server configurations (nginx -s reload, systemctl reload apache2) applying new certificates without downtime
- **Monitoring and Alerting**: Certificate expiration dates monitored; alerts triggered 30, 14, 7 days before expiration if auto-renewal fails

### 5. Certificate Revocation Procedures
- **Revocation Reasons**: Certificates revoked for key compromise, CA compromise, certificate misuse, or cessation of operation
- **CRL (Certificate Revocation List)**: CA publishes lists of revoked certificate serial numbers; clients download CRL periodically checking validity
- **OCSP (Online Certificate Status Protocol)**: Real-time certificate status queries to CA responder; faster than CRL but adds latency and privacy concerns
- **OCSP Stapling**: Server queries OCSP and staples time-stamped response to TLS handshake eliminating client-side OCSP query

### 6. Certificate Monitoring and Inventory
- **Certificate Discovery**: Automated scanning of networks and applications identifying all installed certificates and expiration dates
- **Certificate Inventory Database**: Centralized repository tracking certificate locations, issuers, expiration dates, and responsible teams
- **Expiration Tracking**: Dashboard displays certificates expiring within 30/60/90 days enabling proactive renewal planning
- **Compliance Scanning**: Regular audits verify no expired certificates, weak ciphers, or deprecated protocols in production

### 7. Wildcard and Multi-Domain Certificates
- **Wildcard Certificates**: Single certificate for *.example.com covering unlimited subdomains (www, api, mail, etc.); DNS validation required
- **SAN Certificates**: Single certificate covering multiple unrelated domains (example.com, example.net, example.org); reduces management overhead
- **Certificate Cost Optimization**: Wildcard certificates more expensive than single-domain but cheaper than multiple single-domain certificates
- **Security Considerations**: Wildcard certificates increase blast radius of key compromise; some organizations prefer separate certificates per service

## System Integration Points

### Web Servers and Load Balancers
- **Apache HTTP Server**: mod_ssl module provides SSL/TLS termination; Virtual Host configuration specifies certificates per domain
- **Nginx**: Native SSL support with ssl_certificate and ssl_certificate_key directives; supports OCSP stapling and session caching
- **HAProxy**: SSL termination at load balancer with backend servers receiving unencrypted traffic reducing certificate management complexity
- **F5 BIG-IP**: Centralized certificate management with SSL offload; Client SSL and Server SSL profiles separate inbound/outbound encryption

### Certificate Management Platforms
- **Venafi Trust Protection Platform**: Enterprise certificate lifecycle management with policy enforcement and automated workflows
- **DigiCert CertCentral**: Multi-CA certificate manager with API for automated provisioning and comprehensive reporting
- **Let's Encrypt**: Free automated certificates via ACME protocol; 90-day validity encourages automation and reduces manual effort
- **AWS Certificate Manager (ACM)**: Free certificates for AWS resources (ALB, CloudFront); automatic renewal with no manual intervention

### Hardware Security Modules (HSMs)
- **FIPS 140-2 Compliant Storage**: Private keys stored in tamper-resistant HSMs preventing extraction even by administrators
- **Key Generation**: Cryptographic operations performed inside HSM; private key never exists in unencrypted form outside HSM
- **HSM Clustering**: High-availability HSM clusters prevent single point of failure for certificate operations
- **Cloud HSM Services**: AWS CloudHSM, Azure Key Vault HSM provide managed HSM capabilities without physical appliance management

### DevOps and CI/CD Integration
- **Infrastructure as Code (IaC)**: Terraform, CloudFormation templates define certificate resources provisioned automatically during deployment
- **Secrets Management**: HashiCorp Vault, AWS Secrets Manager store private keys and certificates with access control and audit logging
- **Container Orchestration**: Kubernetes cert-manager operator automates certificate provisioning for ingress controllers and services
- **GitOps Workflows**: Certificate configurations stored in Git; changes trigger automated validation, deployment, and rollback on failure

## Regulatory Compliance

### PCI-DSS Requirements
- **Strong Cryptography**: PCI-DSS 4.0 requires TLS 1.2+ for cardholder data transmission; TLS 1.0/1.1 prohibited
- **Certificate Validation**: Browsers must validate certificate chain to trusted root CA; self-signed certificates not permitted in production
- **Key Length Requirements**: Minimum 2048-bit RSA or 256-bit ECC; 1024-bit RSA deprecated and insufficient for PCI compliance
- **Annual Certificate Review**: All certificates validated annually ensuring proper configuration and compliance with cryptographic standards

### HIPAA Security Rule
- **Encryption in Transit**: PHI transmitted over networks must be encrypted using TLS; certificates ensure secure HTTPS connections
- **Certificate Expiration Monitoring**: Expired certificates cause encryption failures; monitoring prevents accidental PHI exposure
- **Access Controls**: Private keys protected with strict access controls; only authorized personnel permitted to generate or install certificates
- **Audit Logging**: Certificate installation, renewal, and revocation logged for HIPAA security audits

### FedRAMP Requirements
- **FIPS 140-2 Validated Cryptography**: Federal systems must use FIPS-validated modules for key generation and certificate operations
- **Certificate Authority Trust**: Certificates issued by CAs trusted by Federal PKI or commercial CAs meeting Federal Bridge CA requirements
- **Continuous Monitoring**: Automated scanning detects certificate expirations, weak ciphers, and protocol vulnerabilities monthly
- **Incident Reporting**: Certificate compromises reported as security incidents with root cause analysis and remediation documentation

### CA/Browser Forum Baseline Requirements
- **Maximum Validity Period**: Public certificates limited to 398 days (13 months) validity; longer periods not trusted by browsers post-2020
- **Forbidden Characters**: Certificate CN and SANs cannot contain wildcard in internal labels (*.internal.example.com prohibited)
- **Revocation Requirements**: CAs must revoke certificates within 24 hours of key compromise notification
- **Certificate Transparency**: All public certificates logged to CT logs; browsers reject certificates not appearing in recognized logs

## Equipment and Vendors

### Commercial Certificate Authorities
- **DigiCert**: Premium CA offering OV, EV, wildcard, and multi-domain certificates with insurance and warranty protection
- **Sectigo (formerly Comodo)**: High-volume CA with aggressive pricing for DV certificates; popular in hosting and SMB markets
- **GlobalSign**: European CA with strong presence in enterprise and IoT device certificate markets
- **Entrust**: CA serving government and regulated industries; FIPS-compliant and FedRAMP-authorized certificate services

### Free Certificate Authorities
- **Let's Encrypt**: Non-profit CA providing free DV certificates with 90-day validity; automated renewal via ACME protocol
- **ZeroSSL**: Let's Encrypt competitor offering free 90-day certificates with optional paid support and longer validity
- **Buypass**: Norwegian CA offering free DV certificates with 180-day validity alternative to Let's Encrypt

### Certificate Management Platforms
- **Venafi**: Enterprise PKI lifecycle management with policy enforcement, automation, and comprehensive reporting
- **Keyfactor**: Certificate authority and lifecycle management platform supporting public and private CAs
- **AppViewX**: Multi-CA certificate automation platform integrating with F5, Citrix, and cloud load balancers
- **Sectigo Certificate Manager (SCM)**: Centralized certificate issuance and management for Sectigo CA certificates

### ACME Clients and Automation
- **Certbot (EFF)**: Official Let's Encrypt client with plugins for Apache, Nginx, DNS providers; Python-based
- **acme.sh**: Lightweight ACME client implemented as bash script; minimal dependencies and extensive DNS provider support
- **win-acme**: Windows-focused ACME client with IIS integration and scheduled task automation
- **cert-manager (Kubernetes)**: Native Kubernetes certificate management operator automating Let's Encrypt integration

## Performance Metrics

### Certificate Health Metrics
- **Certificate Expiration Distribution**: Percentage of certificates expiring within 30/60/90 days; goal 0% expiring <30 days
- **Renewal Success Rate**: Automated renewal success percentage; target >99% with manual intervention only for exceptional cases
- **Certificate Coverage**: Percentage of public-facing services protected by valid certificates; goal 100%
- **Revocation Checking Availability**: OCSP responder uptime >99.9%; CRL distribution availability 100%

### Security Posture Metrics
- **SSL Labs Grade**: A+ rating target for all public-facing services indicating strong configuration
- **Weak Cipher Usage**: 0% connections using weak ciphers (RC4, 3DES, export ciphers); deprecated ciphers phased out
- **Protocol Version Distribution**: >95% connections using TLS 1.3, <5% TLS 1.2, 0% older protocols
- **Perfect Forward Secrecy**: 100% connections using ephemeral key exchange (ECDHE, DHE) ensuring past session security

### Operational Efficiency
- **Manual Certificate Installations**: Percentage of certificates requiring manual installation; target <10% with automation goal
- **Certificate-Related Outages**: Number of incidents caused by expired or misconfigured certificates; goal zero per quarter
- **Mean Time to Renewal**: Average time from renewal trigger to certificate installed and verified; target <1 hour automated, <4 hours manual
- **Certificate Inventory Accuracy**: Percentage of certificates in inventory system matching actual deployments; target >95%

### Cost Metrics
- **Cost per Certificate**: Average cost including CA fees, labor, and platform licensing; free DV certificates reduce this significantly
- **CA Spend Optimization**: Consolidation to fewer CAs and bulk purchasing reduces per-certificate costs
- **Outage Cost Avoidance**: Automated renewal prevents costly service outages from expired certificates (average $5,600/minute downtime)
- **Automation ROI**: Labor savings from automation compared to platform/tool costs; typical 5:1 ROI for organizations with 100+ certificates

---

**Document Control**
- **Version**: 1.0
- **Last Updated**: 2025-11-06
- **Regulatory References**: PCI-DSS v4.0, HIPAA Security Rule, FedRAMP Rev 5, CA/Browser Forum Baseline Requirements v2.0, RFC 8555 (ACME), RFC 6960 (OCSP)
- **Review Cycle**: Quarterly
