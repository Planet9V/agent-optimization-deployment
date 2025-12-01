REST API Integration Developer

**Role**: REST API Integration Developer

**Task**: Create production-ready REST API integration module for SCADA systems

**Project Structure**:
- Create `/a0/scada_integration/` directory with modular architecture
- Extend existing OPC-UA/MQTT pipeline patterns
- Use Python FastAPI for REST endpoints

**Core Components to Implement**:
1. **REST Client Module**: Circuit breaker pattern (5 failures opens, 30s timeout), exponential backoff retry (1s, 2s, 4s, 8s)
2. **Authentication Handlers**: OAuth 2.0 client credentials, API key + HMAC
3. **Vendor Adapters**: Siemens (MindSphere OAuth2, S7-1500 API key), Rockwell (FactoryTalk API key + HMAC), Schneider (EcoStruxure OAuth2, Modicon API key)
4. **JSON-LD Mapping**: Convert vendor data to standardized asset model
5. **Integration**: Connect with existing OPC-UA/MQTT pipeline

**Requirements**:
- Performance: <100ms P95 latency per API call, <0.1% error rate
- Monitoring: Prometheus metrics (request_latency_ms, error_rate)
- Logging: JSON structured logging
- Security: TLS 1.2+, Kubernetes Secrets integration
- Testing: 90% coverage with mocked vendor APIs

**Start with**:
1. Create project structure and core REST client module
2. Implement authentication handlers
3. Create vendor adapter interfaces

Focus on modular, maintainable design that can be easily extended for additional vendors.