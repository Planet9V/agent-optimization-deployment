# PACS Radiology Image Acquisition Operations

## Overview
Picture Archiving and Communication System (PACS) operations for medical imaging acquisition, storage, and distribution using DICOM standards and modality integration.

## 1. Modality Worklist Configuration

### DICOM Worklist Query
**Annotation**: <entity type="modality">Imaging modalities</entity> (<entity type="device">CT scanners</entity>, <entity type="device">MRI machines</entity>, <entity type="device">X-ray systems</entity>) query the <entity type="system">DICOM Worklist Server</entity> using <entity type="protocol">DICOM C-FIND</entity> to retrieve <entity type="data">scheduled procedure information</entity> including <entity type="field">patient demographics</entity>, <entity type="field">accession number</entity>, <entity type="field">requested procedure</entity>, and <entity type="field">scheduled time</entity> per <entity type="standard">DICOM Part 3.4</entity>.

### Patient Selection Workflow
**Annotation**: <entity type="role">Radiology technologists</entity> select patients from the <entity type="interface">modality worklist</entity>, which auto-populates <entity type="data">DICOM header tags</entity> including <entity type="tag">Patient Name (0010,0010)</entity>, <entity type="tag">Patient ID (0010,0020)</entity>, <entity type="tag">Study Instance UID (0020,000D)</entity>, and <entity type="tag">Accession Number (0008,0050)</entity> preventing <entity type="error">manual entry errors</entity>.

### Procedure Verification
**Annotation**: Before image acquisition, staff must verify <entity type="match">patient identity match</entity> using <entity type="identifier">two patient identifiers</entity>, confirm <entity type="match">correct procedure</entity>, check <entity type="match">correct anatomical site</entity>, and validate <entity type="match">laterality markers</entity> following <entity type="standard">Joint Commission Universal Protocol</entity>.

## 2. Image Acquisition Parameters

### CT Protocol Selection
**Annotation**: <entity type="system">CT scanners</entity> load predefined <entity type="protocol">scanning protocols</entity> specifying <entity type="parameter">kVp</entity>, <entity type="parameter">mAs</entity>, <entity type="parameter">slice thickness</entity>, <entity type="parameter">reconstruction kernel</entity>, <entity type="parameter">pitch</entity>, and <entity type="parameter">contrast timing</entity> optimized for <entity type="exam_type">specific exam types</entity> while adhering to <entity type="principle">ALARA radiation safety principles</entity>.

### MRI Sequence Programming
**Annotation**: <entity type="system">MRI systems</entity> execute <entity type="sequence">pulse sequences</entity> including <entity type="sequence_type">T1-weighted</entity>, <entity type="sequence_type">T2-weighted</entity>, <entity type="sequence_type">FLAIR</entity>, <entity type="sequence_type">diffusion-weighted imaging</entity>, and <entity type="sequence_type">contrast-enhanced sequences</entity> with parameters like <entity type="parameter">TR</entity>, <entity type="parameter">TE</entity>, <entity type="parameter">flip angle</entity>, <entity type="parameter">field of view</entity>, and <entity type="parameter">matrix size</entity>.

### Image Quality Validation
**Annotation**: Post-acquisition <entity type="process">quality control checks</entity> verify <entity type="criteria">adequate anatomical coverage</entity>, <entity type="criteria">absence of motion artifacts</entity>, <entity type="criteria">appropriate contrast enhancement</entity>, and <entity type="criteria">proper image reconstruction</entity> before transmitting to <entity type="system">PACS</entity> via <entity type="protocol">DICOM C-STORE</entity>.

## 3. DICOM Image Transfer

### C-STORE Transaction
**Annotation**: <entity type="device">Modalities</entity> push acquired images to <entity type="system">PACS servers</entity> using <entity type="service">DICOM C-STORE SCP/SCU</entity> operations transmitting <entity type="object">DICOM SOP instances</entity> with <entity type="encoding">compressed</entity> or <entity type="encoding">uncompressed</entity> <entity type="format">pixel data</entity> per <entity type="standard">DICOM Part 4</entity> transfer syntax.

### Network Configuration
**Annotation**: DICOM communication requires configuration of <entity type="parameter">AE Titles</entity> (Application Entity), <entity type="parameter">IP addresses</entity>, <entity type="parameter">port numbers</entity> (default <entity type="port">104</entity>), and <entity type="parameter">transfer syntaxes</entity> like <entity type="syntax">Explicit VR Little Endian</entity> or <entity type="syntax">JPEG 2000 Lossless</entity> on dedicated <entity type="network">VLAN-segmented medical imaging networks</entity>.

### Storage Commitment
**Annotation**: After successful image transfer, the <entity type="system">PACS</entity> sends <entity type="message">DICOM N-EVENT-REPORT Storage Commitment</entity> messages confirming <entity type="status">persistent storage</entity> of images, allowing <entity type="device">modalities</entity> to <entity type="action">delete local copies</entity> and free <entity type="resource">acquisition system storage</entity>.

## 4. Image Routing and Prefetching

### Auto-Routing Rules
**Annotation**: <entity type="system">PACS routing engines</entity> apply rules based on <entity type="criteria">modality type</entity>, <entity type="criteria">procedure code</entity>, <entity type="criteria">ordering physician</entity>, or <entity type="criteria">location</entity> to automatically distribute images to appropriate <entity type="destination">reading workstations</entity>, <entity type="destination">subspecialty PACS</entity>, or <entity type="destination">enterprise viewers</entity>.

### Prior Exam Prefetching
**Annotation**: <entity type="algorithm">Intelligent prefetch algorithms</entity> automatically retrieve <entity type="data">relevant prior exams</entity> based on <entity type="match">same modality</entity>, <entity type="match">same body part</entity>, <entity type="match">same patient</entity> within a <entity type="timeframe">configurable lookback period</entity>, staging images to <entity type="storage">local cache</entity> before <entity type="role">radiologist</entity> interpretation sessions.

### Hanging Protocols
**Annotation**: <entity type="system">Diagnostic workstations</entity> apply <entity type="protocol">hanging protocols</entity> that automatically arrange images in <entity type="layout">predefined layouts</entity> based on <entity type="criteria">exam type</entity>, applying <entity type="setting">window/level presets</entity>, <entity type="setting">zoom factors</entity>, and <entity type="tool">measurement tools</entity> optimizing <entity type="workflow">radiologist efficiency</entity>.

## 5. Multi-Modality Study Management

### Series Organization
**Annotation**: <entity type="hierarchy">DICOM studies</entity> consist of <entity type="level">series</entity> containing <entity type="object">individual images</entity>, with each series representing a distinct <entity type="concept">acquisition sequence</entity> identified by <entity type="tag">Series Instance UID (0020,000E)</entity>, <entity type="tag">Series Number</entity>, and <entity type="tag">Series Description</entity>.

### 3D Reconstruction
**Annotation**: <entity type="software">Advanced visualization workstations</entity> perform <entity type="processing">multiplanar reformatting (MPR)</entity>, <entity type="processing">maximum intensity projection (MIP)</entity>, <entity type="processing">volume rendering</entity>, and <entity type="processing">3D surface rendering</entity> from <entity type="input">thin-slice CT or MRI datasets</entity> for applications like <entity type="application">CT angiography</entity>, <entity type="application">virtual colonoscopy</entity>, and <entity type="application">surgical planning</entity>.

### Fusion Imaging
**Annotation**: <entity type="technique">Image fusion</entity> combines <entity type="modality">anatomical imaging</entity> (CT/MRI) with <entity type="modality">functional imaging</entity> (PET/SPECT) using <entity type="algorithm">rigid or deformable registration algorithms</entity> producing <entity type="output">fused image sets</entity> for <entity type="application">oncology staging</entity>, <entity type="application">radiotherapy planning</entity>, and <entity type="application">surgical guidance</entity>.

## 6. Quality Assurance Operations

### Daily QA Procedures
**Annotation**: <entity type="process">Daily quality assurance</entity> for <entity type="device">CT scanners</entity> includes <entity type="test">water phantom scans</entity> verifying <entity type="metric">CT number accuracy</entity>, <entity type="metric">noise levels</entity>, <entity type="metric">spatial resolution</entity>, and <entity type="metric">slice thickness</entity> with results logged in <entity type="system">QA tracking systems</entity> per <entity type="standard">ACR CT accreditation requirements</entity>.

### MRI Phantom Testing
**Annotation**: <entity type="device">MRI systems</entity> undergo <entity type="frequency">weekly</entity> testing using <entity type="phantom">ACR MRI phantoms</entity> measuring <entity type="parameter">geometric accuracy</entity>, <entity type="parameter">high-contrast spatial resolution</entity>, <entity type="parameter">slice thickness accuracy</entity>, <entity type="parameter">image intensity uniformity</entity>, and <entity type="parameter">ghosting artifacts</entity>.

### Dose Monitoring
**Annotation**: <entity type="system">Radiation dose monitoring systems</entity> collect <entity type="data">DICOM Radiation Dose Structured Reports (RDSR)</entity> from <entity type="device">CT and fluoroscopy equipment</entity>, tracking <entity type="metric">patient dose indices</entity> like <entity type="measure">CTDIvol</entity>, <entity type="measure">DLP</entity>, and <entity type="measure">DAP</entity> enabling <entity type="analysis">dose optimization</entity> and <entity type="compliance">regulatory reporting</entity>.

## 7. Image Archive Management

### Storage Hierarchy
**Annotation**: <entity type="system">PACS storage architecture</entity> employs <entity type="tier">multi-tiered storage</entity> with <entity type="tier_type">online SSD/NVMe</entity> for <entity type="data">recent studies</entity>, <entity type="tier_type">nearline spinning disk</entity> for <entity type="data">mid-term archives</entity>, and <entity type="tier_type">offline tape/cloud</entity> for <entity type="data">long-term retention</entity> based on <entity type="policy">automatic migration policies</entity>.

### Data Retention Policies
**Annotation**: <entity type="regulation">State medical record laws</entity> and <entity type="regulation">CMS Conditions of Participation</entity> require retention of <entity type="data">diagnostic images</entity> for minimum periods (typically <entity type="duration">5-10 years</entity> for adults, <entity type="duration">until age of majority plus 5-10 years</entity> for pediatric patients) with <entity type="consideration">longer retention for oncology</entity> and <entity type="consideration">medicolegal cases</entity>.

### Disaster Recovery
**Annotation**: <entity type="strategy">PACS disaster recovery</entity> implements <entity type="approach">offsite replication</entity> to <entity type="location">geographically diverse data centers</entity> or <entity type="location">cloud archives</entity>, maintaining <entity type="target">RPO (Recovery Point Objective)</entity> of <entity type="timeframe">< 24 hours</entity> and <entity type="target">RTO (Recovery Time Objective)</entity> of <entity type="timeframe">< 4 hours</entity> for <entity type="impact">business continuity</entity>.

## 8. Workflow Integration

### RIS-PACS Integration
**Annotation**: <entity type="system">Radiology Information Systems (RIS)</entity> and <entity type="system">PACS</entity> exchange data via <entity type="standard">HL7 v2.x messages</entity> and <entity type="standard">IHE profiles</entity> including <entity type="profile">Scheduled Workflow (SWF)</entity>, <entity type="profile">Patient Information Reconciliation (PIR)</entity>, and <entity type="profile">Reporting Workflow (RWF)</entity> ensuring <entity type="goal">synchronized patient demographics</entity>, <entity type="goal">order status</entity>, and <entity type="goal">report availability</entity>.

### Voice Recognition Integration
**Annotation**: <entity type="system">Speech recognition systems</entity> like <entity type="vendor">Nuance PowerScribe</entity> integrate with <entity type="system">PACS workstations</entity> enabling <entity type="workflow">radiologist dictation</entity> with <entity type="feature">auto-population of patient demographics</entity>, <entity type="feature">exam details</entity>, and <entity type="feature">structured reporting templates</entity> improving <entity type="metric">reporting turnaround time</entity>.

### Critical Results Communication
**Annotation**: Detection of <entity type="finding">critical findings</entity> (e.g., <entity type="example">pulmonary embolism</entity>, <entity type="example">pneumothorax</entity>, <entity type="example">intracranial hemorrhage</entity>) triggers <entity type="alert">automated alerts</entity> to <entity type="recipient">ordering physicians</entity> via <entity type="method">SMS</entity>, <entity type="method">pager</entity>, or <entity type="method">EHR notifications</entity> with <entity type="requirement">documented acknowledgment</entity> per <entity type="standard">ACR Practice Parameter for Communication of Diagnostic Imaging Findings</entity>.

## 9. Advanced Imaging Applications

### Cardiac Imaging
**Annotation**: <entity type="application">Cardiac CT and MRI</entity> utilize specialized <entity type="technique">ECG-gated acquisitions</entity> synchronized with <entity type="signal">patient heart rate</entity> producing <entity type="output">motion-free coronary artery images</entity> and <entity type="output">functional cine loops</entity>, with post-processing for <entity type="analysis">calcium scoring</entity>, <entity type="analysis">fractional flow reserve</entity>, and <entity type="analysis">myocardial perfusion analysis</entity>.

### Neuroimaging Protocols
**Annotation**: <entity type="protocol">Brain MRI protocols</entity> include <entity type="sequence">advanced sequences</entity> like <entity type="technique">diffusion tensor imaging (DTI)</entity> for <entity type="anatomy">white matter tracts</entity>, <entity type="technique">perfusion imaging</entity> for <entity type="pathology">stroke assessment</entity>, <entity type="technique">MR spectroscopy</entity> for <entity type="application">tumor characterization</entity>, and <entity type="technique">functional MRI</entity> for <entity type="application">preoperative brain mapping</entity>.

### AI Integration
**Annotation**: <entity type="technology">Artificial intelligence algorithms</entity> deployed on <entity type="platform">PACS</entity> or <entity type="platform">edge servers</entity> provide <entity type="function">automated detection</entity> of <entity type="pathology">pulmonary nodules</entity>, <entity type="pathology">intracranial hemorrhage</entity>, <entity type="pathology">fractures</entity>, and <entity type="pathology">breast lesions</entity>, with <entity type="output">CAD markers</entity> and <entity type="output">worklist prioritization</entity> following <entity type="regulation">FDA 510(k) clearance</entity>.

## 10. Security and Access Control

### DICOM Security
**Annotation**: <entity type="security">DICOM image encryption</entity> uses <entity type="protocol">DICOM Secure Transport Connection Profiles</entity> including <entity type="method">TLS 1.2+</entity> for <entity type="purpose">network transmission</entity> and <entity type="method">AES-256</entity> for <entity type="purpose">archive encryption</entity> protecting <entity type="data">PHI-containing images</entity> per <entity type="regulation">HIPAA Security Rule</entity>.

### Audit Logging
**Annotation**: <entity type="system">PACS audit systems</entity> log all <entity type="action">image access</entity>, <entity type="action">query operations</entity>, <entity type="action">print events</entity>, and <entity type="action">export activities</entity> recording <entity type="attribute">user identity</entity>, <entity type="attribute">timestamp</entity>, <entity type="attribute">patient identifier</entity>, and <entity type="attribute">workstation location</entity> supporting <entity type="investigation">breach investigations</entity> and <entity type="compliance">regulatory audits</entity>.

### Role-Based Access
**Annotation**: <entity type="model">Role-based access control (RBAC)</entity> restricts <entity type="function">PACS functionality</entity> based on <entity type="role">user roles</entity> (<entity type="example">radiologist</entity>, <entity type="example">technologist</entity>, <entity type="example">referring physician</entity>, <entity type="example">administrator</entity>) limiting access to <entity type="capability">image deletion</entity>, <entity type="capability">PHI editing</entity>, <entity type="capability">configuration changes</entity>, and <entity type="capability">system administration</entity>.

## Vendor Systems

- **PACS Vendors**: GE Centricity, Philips IntelliSpace, Siemens syngo, Fujifilm Synapse, Agfa Enterprise Imaging
- **Modalities**: GE Healthcare, Siemens Healthineers, Philips Healthcare, Canon Medical, Hologic
- **Workstations**: Visage 7, TeraRecon, Vital Images, Aquarius iNtuition
- **VNA**: Philips Universal Data Manager, Agfa Universal Viewer, Acuo VNA
- **AI Platforms**: Aidoc, Viz.ai, Zebra Medical Vision, Arterys

## Standards and Regulations

- **DICOM**: Digital Imaging and Communications in Medicine (all parts)
- **IHE**: Integrating the Healthcare Enterprise profiles (SWF, PIR, RWF, XDS-I)
- **ACR**: American College of Radiology accreditation and practice parameters
- **HIPAA**: Privacy and security of medical images
- **FDA**: Medical device regulations for modalities and AI algorithms
- **MQSA**: Mammography Quality Standards Act for breast imaging
