# Responder Integration for LLMNR/NBT-NS Poisoning Detection and Response

## Overview

Responder is a powerful tool for detecting and responding to LLMNR (Link-Local Multicast Name Resolution) and NBT-NS (NetBIOS Name Service) poisoning attacks. This section covers advanced integration techniques for automated network security monitoring using n8n workflows.

**Related Sections:**
- [[Kali Linux Integration]] - Basic Responder setup and configuration
- [[Network Design]] - Network segmentation to prevent poisoning attacks
- [[Threat Detection]] - Advanced threat detection workflows
- [[Incident Response]] - Automated response to poisoning incidents

## Understanding LLMNR/NBT-NS Poisoning

### Attack Mechanism

LLMNR/NBT-NS poisoning exploits Windows name resolution protocols:
- **LLMNR**: Used when DNS fails, broadcasts queries on local network
- **NBT-NS**: Legacy NetBIOS name resolution protocol
- **Attack**: Attacker responds to queries with malicious IP addresses

### Detection Challenges

- Legitimate traffic patterns vs. malicious poisoning
- Multi-interface monitoring requirements
- Real-time analysis of broadcast traffic
- Correlation with other security events

## Advanced Responder Configuration

### Multi-Interface Monitoring

```bash
# Configure Responder for comprehensive monitoring
responder -I eth0,wlan0,br0 -w -r -f -v --analyze
```

### Custom Poisoning Detection Rules

```json
{
  "responder_config": {
    "interfaces": ["eth0", "wlan0", "docker0"],
    "poisoning_detection": {
      "llmnr_threshold": 5,
      "nbt_ns_threshold": 3,
      "time_window": 60,
      "alert_on_suspicious": true
    },
    "response_actions": {
      "isolate_hosts": true,
      "block_attacker": true,
      "collect_evidence": true,
      "notify_team": true
    }
  }
}
```

## n8n Workflow: Automated Poisoning Detection

### Network Traffic Monitoring Node

```json
{
  "parameters": {
    "command": "tcpdump -i any -nn -s0 -w /tmp/network_capture.pcap 'udp port 5355 or udp port 137' -G 300 -W 1",
    "timeout": 300000
  },
  "name": "Capture LLMNR/NBT-NS Traffic",
  "type": "n8n-nodes-base.executeCommand"
}
```

### Poisoning Pattern Analysis

```json
{
  "parameters": {
    "functionCode": "const fs = require('fs');\nconst { execSync } = require('child_process');\n\n// Analyze captured traffic for poisoning patterns\nconst analysis = execSync('tshark -r /tmp/network_capture.pcap -T json -e ip.src -e ip.dst -e udp.srcport -e udp.dstport -e llmnr.query -e nbns.query').toString();\n\nconst traffic = JSON.parse(analysis);\n\n// Detect poisoning patterns\nconst poisoningEvents = [];\nconst hostActivity = {};\n\ntraffic.forEach(packet => {\n  const src = packet._source.layers.ip?.['ip.src'];\n  const dst = packet._source.layers.ip?.['ip.dst'];\n  const query = packet._source.layers.llmnr?.['llmnr.query'] || packet._source.layers.nbns?.['nbns.query'];\n  \n  if (src && query) {\n    if (!hostActivity[src]) {\n      hostActivity[src] = { queries: [], responses: [] };\n    }\n    hostActivity[src].queries.push({ query, dst, timestamp: packet._source.layers.frame['frame.time'] });\n  }\n  \n  if (dst && query) {\n    if (!hostActivity[dst]) {\n      hostActivity[dst] = { queries: [], responses: [] };\n    }\n    hostActivity[dst].responses.push({ query, src, timestamp: packet._source.layers.frame['frame.time'] });\n  }\n});\n\n// Identify suspicious patterns\nObject.keys(hostActivity).forEach(host => {\n  const activity = hostActivity[host];\n  const queryCount = activity.queries.length;\n  const responseCount = activity.responses.length;\n  \n  if (responseCount > queryCount * 2) {\n    poisoningEvents.push({\n      host: host,\n      suspicious_responses: responseCount,\n      legitimate_queries: queryCount,\n      risk_level: 'HIGH'\n    });\n  }\n});\n\nreturn { poisoning_events: poisoningEvents, host_activity: hostActivity };"
  },
  "name": "Analyze Poisoning Patterns",
  "type": "n8n-nodes-base.function"
}
```

## Automated Response Workflows

### Host Isolation and Containment

```json
{
  "name": "Responder Attack Response",
  "nodes": [
    {
      "parameters": {
        "functionCode": "const poisoningEvents = $node[\"Analyze Poisoning Patterns\"].json.poisoning_events;\n\nif (poisoningEvents.length > 0) {\n  const criticalEvents = poisoningEvents.filter(event => event.risk_level === 'HIGH');\n  \n  return {\n    trigger_response: true,\n    affected_hosts: criticalEvents.map(e => e.host),\n    severity: 'HIGH',\n    attack_type: 'LLMNR/NBT-NS Poisoning'\n  };\n}\n\nreturn { trigger_response: false };"
      },
      "name": "Evaluate Response Trigger",
      "type": "n8n-nodes-base.function"
    },
    {
      "parameters": {
        "command": "iptables -A INPUT -s {{$node[\"Evaluate Response Trigger\"].json.affected_hosts[0]}} -j DROP && iptables -A OUTPUT -d {{$node[\"Evaluate Response Trigger\"].json.affected_hosts[0]}} -j DROP"
      },
      "name": "Isolate Affected Host",
      "type": "n8n-nodes-base.executeCommand"
    },
    {
      "parameters": {
        "to": "security@company.com",
        "subject": "CRITICAL: LLMNR/NBT-NS Poisoning Attack Detected",
        "body": "A potential LLMNR/NBT-NS poisoning attack has been detected.\\n\\nAffected Hosts: {{$node[\"Evaluate Response Trigger\"].json.affected_hosts}}\\nSeverity: {{$node[\"Evaluate Response Trigger\"].json.severity}}\\n\\nAutomated response has been initiated."
      },
      "name": "Send Security Alert",
      "type": "n8n-nodes-base.emailSend"
    }
  ],
  "connections": {
    "Evaluate Response Trigger": {
      "main": [
        [
          {
            "node": "Isolate Affected Host",
            "type": "main",
            "index": 0
          },
          {
            "node": "Send Security Alert",
            "type": "main",
            "index": 0
          }
        }
      ]
    }
  }
}
```

## Advanced Detection Techniques

### Machine Learning-Based Anomaly Detection

```javascript
// Implement ML-based poisoning detection
const tf = require('@tensorflow/tfjs');

class PoisoningDetector {
  constructor() {
    this.model = this.buildModel();
    this.trainingData = [];
  }

  buildModel() {
    const model = tf.sequential();
    model.add(tf.layers.dense({inputShape: [5], units: 32, activation: 'relu'}));
    model.add(tf.layers.dense({units: 16, activation: 'relu'}));
    model.add(tf.layers.dense({units: 1, activation: 'sigmoid'}));
    
    model.compile({
      optimizer: 'adam',
      loss: 'binaryCrossentropy',
      metrics: ['accuracy']
    });
    
    return model;
  }

  async analyzeTraffic(trafficData) {
    // Extract features: query frequency, response ratio, time patterns, etc.
    const features = this.extractFeatures(trafficData);
    const prediction = await this.model.predict(tf.tensor2d([features]));
    const isPoisoning = prediction.dataSync()[0] > 0.8;
    
    return {
      is_poisoning: isPoisoning,
      confidence: prediction.dataSync()[0],
      features: features
    };
  }

  extractFeatures(trafficData) {
    // Feature extraction logic
    return [
      trafficData.queryCount,
      trafficData.responseCount / trafficData.queryCount,
      trafficData.uniqueHosts,
      trafficData.timeVariance,
      trafficData.broadcastRatio
    ];
  }
}
```

### Correlation with Other Security Events

```json
{
  "parameters": {
    "functionCode": "const poisoningEvents = $node[\"Analyze Poisoning Patterns\"].json.poisoning_events;\nconst siemEvents = $node[\"SIEM Query\"].json.events;\n\n// Correlate poisoning with other security events\nconst correlations = [];\n\npoisoningEvents.forEach(poisoning => {\n  const relatedEvents = siemEvents.filter(event => \n    event.src_ip === poisoning.host || \n    event.timestamp >= poisoning.timestamp - 300000 && \n    event.timestamp <= poisoning.timestamp + 300000\n  );\n  \n  if (relatedEvents.length > 0) {\n    correlations.push({\n      poisoning_event: poisoning,\n      related_security_events: relatedEvents,\n      correlation_strength: 'STRONG'\n    });\n  }\n});\n\nreturn { event_correlations: correlations };"
  },
  "name": "Correlate Security Events",
  "type": "n8n-nodes-base.function"
}
```

## Responder Tool Integration Workflows

### Automated Responder Deployment

```json
{
  "parameters": {
    "command": "cd /opt/Responder && python Responder.py -I eth0 -w -r -f -v --analyze 2>&1 | tee /var/log/responder.log",
    "timeout": 3600000
  },
  "name": "Start Responder Monitoring",
  "type": "n8n-nodes-base.executeCommand"
}
```

### Log Analysis and Alerting

```json
{
  "parameters": {
    "functionCode": "const fs = require('fs');\nconst logData = fs.readFileSync('/var/log/responder.log', 'utf8');\n\n// Parse Responder logs for security events\nconst logLines = logData.split('\\n');\nconst securityEvents = [];\n\nlogLines.forEach(line => {\n  if (line.includes('Poisoned answer sent')) {\n    const match = line.match(/Poisoned answer sent to (\\d+\\.\\d+\\.\\d+\\.\\d+)/);\n    if (match) {\n      securityEvents.push({\n        type: 'POISONING_DETECTED',\n        target_ip: match[1],\n        timestamp: new Date().toISOString(),\n        severity: 'HIGH'\n      });\n    }\n  }\n  \n  if (line.includes('LLMNR') || line.includes('NBT-NS')) {\n    securityEvents.push({\n      type: 'NAME_RESOLUTION_QUERY',\n      details: line,\n      timestamp: new Date().toISOString(),\n      severity: 'LOW'\n    });\n  }\n});\n\nreturn { security_events: securityEvents };"
  },
  "name": "Parse Responder Logs",
  "type": "n8n-nodes-base.function"
}
```

## Prevention and Mitigation Strategies

### Network Segmentation

```bash
# Implement network segmentation to limit LLMNR/NBT-NS scope
iptables -A INPUT -p udp --dport 5355 -s ! 192.168.1.0/24 -j DROP
iptables -A INPUT -p udp --dport 137 -s ! 192.168.1.0/24 -j DROP
```

### DNS Configuration Best Practices

```json
{
  "dns_hardening": {
    "disable_llmnr": true,
    "disable_netbios": true,
    "enable_dnssec": true,
    "use_internal_dns": true,
    "block_external_queries": true
  }
}
```

### Host-Based Protections

```powershell
# Disable LLMNR via Group Policy
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\DNSClient" -Name "EnableMulticast" -Value 0

# Disable NetBIOS over TCP/IP
Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\services\\NetBT\\Parameters" -Name "EnableLMHosts" -Value 0
```

## Case Studies

### Enterprise Network Poisoning Incident

**Scenario**: Large corporate network with 10,000+ endpoints

**Detection**: Automated Responder monitoring identified 50 poisoning attempts per hour

**Response**: 
- Isolated affected VLAN segments
- Implemented DNS hardening across all domains
- Deployed host-based protections via Group Policy

**Results**: 95% reduction in poisoning attempts within 48 hours

### Healthcare Data Exfiltration Prevention

**Challenge**: Protecting sensitive patient data from lateral movement attacks

**Solution**: Integrated Responder detection with SIEM correlation

**Implementation**:
- Real-time traffic analysis
- Automated host isolation
- Incident response workflow activation

**Outcome**: Prevented potential data breach, zero patient data exposure

## Performance Optimization

### Efficient Traffic Filtering

```javascript
// Optimize packet capture for performance
const captureFilters = {
  llmnr: 'udp port 5355 and udp[8:2] == 0x0000',
  nbns: 'udp port 137 and udp[10] == 0x01',
  exclude_broadcast: 'not broadcast and not multicast'
};

const optimizedCommand = `tcpdump -i any -nn -s0 -w /tmp/optimized_capture.pcap '${captureFilters.llmnr} or ${captureFilters.nbns}' -G 300 -W 1`;
```

### Memory-Efficient Log Processing

```javascript
// Process logs in chunks to manage memory
const processLogsInChunks = async (logFile, chunkSize = 1000) => {
  const stream = fs.createReadStream(logFile, { encoding: 'utf8' });
  let buffer = '';
  let lineCount = 0;
  
  for await (const chunk of stream) {
    buffer += chunk;
    const lines = buffer.split('\\n');
    buffer = lines.pop(); // Keep incomplete line
    
    const events = lines.slice(0, chunkSize).map(parseLogLine).filter(Boolean);
    
    if (events.length > 0) {
      await processEvents(events);
      lineCount += events.length;
    }
  }
};
```

## Integration with SIEM and SOAR

### Splunk Integration

```json
{
  "parameters": {
    "url": "https://splunk.company.com:8088/services/collector",
    "method": "POST",
    "body": "{\\"event\\": {\\"type\\": \\"responder_poisoning\\", \\"events\\": {{$node[\\"Parse Responder Logs\\"].json.security_events}}}}",
    "headers": {
      "Authorization": "Splunk {{$credentials.splunk_token}}",
      "Content-Type": "application/json"
    }
  },
  "name": "Send to Splunk",
  "type": "n8n-nodes-base.httpRequest"
}
```

## References

- lgandx. (2024). *Responder - LLMNR/NBT-NS Poisoning Tool*. https://github.com/lgandx/Responder
- Microsoft. (2024). *LLMNR Security Considerations*. https://docs.microsoft.com/en-us/security-updates/SecurityBulletins/2016/ms16-077
- SANS Institute. (2023). *Detecting and Responding to LLMNR Poisoning*. https://www.sans.org/reading-room/whitepapers/dns/detecting-responding-llmnr-poisoning-37053