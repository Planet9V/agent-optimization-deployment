# FR 5: Restricted Data Flow (RDF)

**Objective:** Control data flow within and between zones.

## Technical Requirements

### SL 1 Requirements
- Basic network segmentation
- Simple firewall rules
- Manual traffic monitoring

### SL 2 Requirements
- Zone and conduit implementation
- Access control between zones
- Traffic filtering and inspection

### SL 3 Requirements
- Advanced network segmentation
- Deep packet inspection
- Automated traffic enforcement

### SL 4 Requirements
- Micro-segmentation
- Zero trust networking
- Continuous traffic monitoring

## Implementation Guidelines

### Network Segmentation Architecture
```javascript
// Network Segmentation Implementation for IACS
class IACSNetworkSegmentation {
  constructor() {
    this.zones = new Map();
    this.conduits = new Map();
    this.firewall = new FirewallEngine();
    this.monitoring = new TrafficMonitor();
  }

  // Define Zones
  defineZone(zoneId, attributes) {
    this.zones.set(zoneId, {
      id: zoneId,
      name: attributes.name,
      securityLevel: attributes.securityLevel,
      assets: new Set(),
      conduits: new Set(),
      policies: attributes.policies || []
    });
  }

  // Define Conduits
  defineConduit(conduitId, sourceZone, targetZone, attributes) {
    const conduit = {
      id: conduitId,
      sourceZone: sourceZone,
      targetZone: targetZone,
      protocol: attributes.protocol,
      ports: attributes.ports,
      securityControls: attributes.securityControls,
      monitoringEnabled: attributes.monitoringEnabled,
      active: true
    };

    this.conduits.set(conduitId, conduit);

    // Add conduit to zones
    this.zones.get(sourceZone).conduits.add(conduitId);
    this.zones.get(targetZone).conduits.add(conduitId);
  }

  // Assign Asset to Zone
  assignAssetToZone(assetId, zoneId) {
    if (!this.zones.has(zoneId)) {
      throw new Error(`Zone not found: ${zoneId}`);
    }

    this.zones.get(zoneId).assets.add(assetId);
  }

  // Enforce Data Flow Policies
  async enforceDataFlow(sourceAsset, targetAsset, protocol, port, data) {
    // Determine source and target zones
    const sourceZone = this.findAssetZone(sourceAsset);
    const targetZone = this.findAssetZone(targetAsset);

    if (!sourceZone || !targetZone) {
      await this.logUnauthorizedAccess(sourceAsset, targetAsset, protocol, port);
      return false;
    }

    // Check if conduit exists
    const conduit = this.findConduit(sourceZone, targetZone);
    if (!conduit) {
      await this.logUnauthorizedAccess(sourceAsset, targetAsset, protocol, port);
      return false;
    }

    // Validate protocol and port
    if (!this.validateConduitAccess(conduit, protocol, port)) {
      await this.logUnauthorizedAccess(sourceAsset, targetAsset, protocol, port);
      return false;
    }

    // Apply security controls
    const securityResult = await this.applySecurityControls(conduit, data);
    if (!securityResult.allowed) {
      await this.logSecurityViolation(conduit, securityResult.reason);
      return false;
    }

    // Monitor traffic
    await this.monitoring.logTraffic(conduit, sourceAsset, targetAsset, protocol, port, data.length);

    return true;
  }

  // Find Asset Zone
  findAssetZone(assetId) {
    for (const [zoneId, zone] of this.zones) {
      if (zone.assets.has(assetId)) {
        return zoneId;
      }
    }
    return null;
  }

  // Find Conduit Between Zones
  findConduit(sourceZone, targetZone) {
    for (const [conduitId, conduit] of this.conduits) {
      if (conduit.sourceZone === sourceZone && conduit.targetZone === targetZone) {
        return conduit;
      }
    }
    return null;
  }

  // Validate Conduit Access
  validateConduitAccess(conduit, protocol, port) {
    // Check protocol
    if (conduit.protocol !== 'any' && conduit.protocol !== protocol) {
      return false;
    }

    // Check port
    if (conduit.ports !== 'any' && !conduit.ports.includes(port)) {
      return false;
    }

    return true;
  }

  // Apply Security Controls
  async applySecurityControls(conduit, data) {
    for (const control of conduit.securityControls) {
      const result = await this.firewall.applyControl(control, data);
      if (!result.allowed) {
        return { allowed: false, reason: result.reason };
      }
    }

    return { allowed: true };
  }

  // Logging Methods
  async logUnauthorizedAccess(sourceAsset, targetAsset, protocol, port) {
    const logEntry = {
      timestamp: new Date(),
      type: 'unauthorized_access',
      sourceAsset: sourceAsset,
      targetAsset: targetAsset,
      protocol: protocol,
      port: port,
      action: 'blocked'
    };

    console.log(`NETWORK_VIOLATION: ${JSON.stringify(logEntry)}`);
  }

  async logSecurityViolation(conduit, reason) {
    const logEntry = {
      timestamp: new Date(),
      type: 'security_violation',
      conduit: conduit.id,
      reason: reason,
      action: 'blocked'
    };

    console.log(`SECURITY_VIOLATION: ${JSON.stringify(logEntry)}`);
  }
}

// Firewall Engine
class FirewallEngine {
  async applyControl(control, data) {
    switch (control.type) {
      case 'signature':
        return await this.checkSignature(control.signature, data);
      case 'anomaly':
        return await this.checkAnomaly(control.baseline, data);
      case 'content':
        return await this.checkContent(control.pattern, data);
      default:
        return { allowed: true };
    }
  }

  async checkSignature(signature, data) {
    // Implementation would check for known malicious signatures
    return { allowed: !data.includes(signature), reason: 'signature_match' };
  }

  async checkAnomaly(baseline, data) {
    // Implementation would check for anomalous patterns
    return { allowed: true }; // Placeholder
  }

  async checkContent(pattern, data) {
    // Implementation would check for prohibited content
    return { allowed: !new RegExp(pattern).test(data), reason: 'content_match' };
  }
}

// Traffic Monitoring
class TrafficMonitor {
  async logTraffic(conduit, sourceAsset, targetAsset, protocol, port, dataSize) {
    const logEntry = {
      timestamp: new Date(),
      conduit: conduit,
      sourceAsset: sourceAsset,
      targetAsset: targetAsset,
      protocol: protocol,
      port: port,
      dataSize: dataSize
    };

    console.log(`TRAFFIC_LOG: ${JSON.stringify(logEntry)}`);
  }
}
```

## Implementation Checklist

- [ ] Basic network segmentation implemented (SL 1+)
- [ ] Firewall rules configured (SL 1+)
- [ ] Zone and conduit architecture deployed (SL 2+)
- [ ] Access controls between zones enforced (SL 2+)
- [ ] Traffic filtering and inspection active (SL 2+)
- [ ] Advanced network segmentation configured (SL 3+)
- [ ] Deep packet inspection enabled (SL 3+)
- [ ] Automated traffic enforcement operational (SL 3+)
- [ ] Micro-segmentation implemented (SL 4)
- [ ] Zero trust networking deployed (SL 4)

## Related Standards
- [[../../network-segmentation|Network Segmentation]] - Zone and conduit design
- [[../../firewall-management|Firewall Management]] - Traffic control and filtering
- [[../../network-monitoring|Network Monitoring]] - Traffic analysis and alerting