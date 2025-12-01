# Part 3 of 6: Communication & Tool Sharing

**Series**: MCP Integration Patterns
**Navigation**: [← Part 2](./02_Transport_Layer.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 4 →](./04_Security_Error_Handling.md)

---

            value = vault_client.get_secret(key)
            if value:
                return value
        except Exception as e:
            logger.warning(f"Failed to load secret {key} from vault: {e}")

        if default is not None:
            return default

        raise ValueError(f"Secret {key} not found")

# Usage
API_KEY = SecretsManager.get_secret("MCP_API_KEY")
DB_PASSWORD = SecretsManager.get_secret("DATABASE_PASSWORD")
```

**Never**:
- Check credentials into Git
- Store secrets in code or config files
- Log sensitive values
- Include secrets in error messages

**Always**:
- Use environment variables or vaults
- Rotate credentials regularly
- Implement secret scanning in CI/CD
- Encrypt secrets at rest

### Monitoring and Logging

#### SIEM Integration

```python
import logging
from datetime import datetime

class MCPAuditLogger:
    """Log all tool invocations for security monitoring"""

    def __init__(self, siem_endpoint: str):
        self.siem = SIEMClient(siem_endpoint)

    async def log_tool_call(self, event: dict):
        """Log tool invocation with full context"""
        audit_event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "tool_invocation",
            "user_id": event.get("user_id"),
            "tool_name": event.get("tool_name"),
            "parameters": event.get("params"),
            "session_id": event.get("session_id"),
            "ip_address": event.get("ip"),
            "result_status": event.get("status"),
        }

        await self.siem.send_event(audit_event)

        # Alert on suspicious patterns
        if self._is_suspicious(audit_event):
            await self.siem.create_alert({
                "severity": "high",
                "description": f"Suspicious activity detected for user {event['user_id']}",
                "event": audit_event
            })
```

**Key Metrics to Track**:
- Tool invocation frequency by user/tool
- Failed authentication attempts
- Input validation failures
- Unusual parameter patterns
- Large data transfers
- Error rates and types

### Security Checklist

- [ ] **Authentication**: OAuth 2.0/2.1 with PKCE implemented
- [ ] **Authorization**: RBAC with tool-level permissions
- [ ] **Input Validation**: Strict JSON schemas enforced
- [ ] **Output Sanitization**: PII/secrets redacted
- [ ] **Secrets Management**: No credentials in code, using vault/env vars
- [ ] **Isolation**: Containers with unprivileged users, read-only FS
- [ ] **Network Security**: TLS/HTTPS for all connections
- [ ] **Monitoring**: SIEM integration with anomaly detection
- [ ] **Logging**: Comprehensive audit trail
- [ ] **Rate Limiting**: Per-user and per-tool limits
- [ ] **DLP**: Data loss prevention guards
- [ ] **Supply Chain**: Signed packages, SBOM, continuous scanning
- [ ] **Incident Response**: Runbooks for security events

---

## Performance Optimization

Production MCP deployments require careful performance tuning for scale and responsiveness.

### Infrastructure Optimization

#### Hardware Selection

**GPU-Accelerated Deployments**:
```yaml
# Kubernetes GPU configuration
resources:
  limits:
    nvidia.com/gpu: 1
    memory: 32Gi
    cpu: 8
  requests:
    nvidia.com/gpu: 1
    memory: 16Gi
    cpu: 4

# Node affinity for GPU nodes
nodeSelector:
  accelerator: nvidia-a100
```

**NUMA Architecture Tuning**:
```bash
# Pin MCP server to specific NUMA node
numactl --cpunodebind=0 --membind=0 python mcp_server.py

# Check NUMA topology
numactl --hardware
```

**Performance Gains**:
- Microsoft's custom kernel tuning: **30% performance boost**
- Latency reduction: **25% improvement**
- High-bandwidth GPUs (NVIDIA A100): Optimal for latency-sensitive workloads

#### Containerization Best Practices

```yaml
# Docker Compose with performance tuning
services:
  mcp-server:
    image: mcp-server:latest
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
    environment:
      - PYTHONUNBUFFERED=1
      - WORKERS=4
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
    sysctls:
      - net.core.somaxconn=4096
      - net.ipv4.tcp_max_syn_backlog=4096
```

### Tool Design Optimization

#### Avoid Tool Proliferation

**Anti-Pattern**:
```python
# DON'T: Map every API endpoint to a tool
@mcp.tool
async def get_user(): pass

@mcp.tool
async def update_user(): pass

@mcp.tool
async def delete_user(): pass

@mcp.tool
async def list_users(): pass

# Result: 100+ tools, complex navigation
```

**Best Practice**:
```python
# DO: Group related operations
@mcp.tool
async def manage_user(
    action: Literal["get", "update", "delete", "list"],
    user_id: Optional[str] = None,
    data: Optional[dict] = None
):
    """Unified user management tool"""
    if action == "get":
        return await db.get_user(user_id)
    elif action == "update":
        return await db.update_user(user_id, data)
    # ...
```

**Impact**: Focused tool selection improved user adoption by **up to 30%**

#### Async/Sync Optimization

```python
from fastmcp import FastMCP

mcp = FastMCP("optimized")

# Use async for I/O-bound operations
@mcp.tool
async def fetch_data(url: str):
    """I/O-bound: use async"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Use sync for CPU-bound operations
@mcp.tool
def process_data(data: list):
    """CPU-bound: use sync"""
    return [transform(item) for item in data]
```

**FastMCP Advantage**: Automatically handles both sync and async functions

### Caching Strategies

#### Multi-Layer Caching

```python
from functools import lru_cache
import redis
import hashlib

class CacheManager:
    def __init__(self):
        self.redis = redis.Redis()

    @lru_cache(maxsize=128)
    def _memory_cache(self, key: str):
        """L1: In-memory cache"""
        return self.redis.get(key)

    async def get_or_compute(self, key: str, compute_fn, ttl=3600):
        """Multi-layer cache with fallback"""

        # L1: Check in-memory cache
        cached = self._memory_cache(key)
        if cached:
            return cached

        # L2: Check Redis
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)

        # L3: Compute and cache
        result = await compute_fn()
        self.redis.setex(key, ttl, json.dumps(result))

        return result
```

**Cache Invalidation**:
```python
# Time-based expiration
cache.setex("key", 3600, value)  # 1 hour TTL

# Event-based invalidation
async def on_data_update(resource_id):
    cache.delete(f"resource:{resource_id}")
    cache.delete_pattern(f"search:*:{resource_id}")
```

### Connection Pooling

```python
from aiohttp import ClientSession, TCPConnector

class OptimizedMCPClient:
    def __init__(self, max_connections=100):
        # Connection pool with keep-alive
        connector = TCPConnector(
            limit=max_connections,
            limit_per_host=30,
            ttl_dns_cache=300,
            keepalive_timeout=30
        )

        self.session = ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30)
        )

    async def call_tool(self, tool_name, args):
        """Reuse connection from pool"""
        async with self.session.post(
            f"{self.endpoint}/tools/{tool_name}",
            json=args
        ) as response:
            return await response.json()
```

**Benefits**:
- Reduces connection establishment overhead
- Enables HTTP/2 multiplexing
- Improves throughput for concurrent requests

### Batch Processing

```python
@mcp.tool
async def batch_process(items: list[str], batch_size: int = 50):
    """Process items in optimized batches"""
    results = []

    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]

        # Process batch concurrently
        batch_results = await asyncio.gather(*[
            process_item(item) for item in batch
        ])

        results.extend(batch_results)

    return results
```

### Load Balancing and Scaling

#### Horizontal Scaling

```yaml
# Kubernetes Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mcp-server-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: mcp-server
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

#### Load Balancer Configuration

```nginx
# Nginx load balancer for MCP servers
upstream mcp_backends {
    least_conn;  # Route to server with fewest connections

    server mcp-server-1:8000 max_fails=3 fail_timeout=30s;
    server mcp-server-2:8000 max_fails=3 fail_timeout=30s;
    server mcp-server-3:8000 max_fails=3 fail_timeout=30s;

    keepalive 32;
}

server {
    listen 443 ssl http2;
    server_name mcp.example.com;

    # Connection optimization
    keepalive_timeout 65;
    keepalive_requests 100;

    location / {
        proxy_pass http://mcp_backends;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_buffering off;  # For SSE streaming
    }
}
```

### Performance Monitoring

```python
import time
from prometheus_client import Counter, Histogram

# Metrics
tool_call_counter = Counter(
    'mcp_tool_calls_total',
    'Total tool invocations',
    ['tool_name', 'status']
)

tool_call_duration = Histogram(
    'mcp_tool_call_duration_seconds',
    'Tool execution duration',
    ['tool_name']
)

@mcp.tool
async def monitored_tool(data: str):
    """Tool with performance monitoring"""
    start = time.time()

    try:
        result = await process(data)
        tool_call_counter.labels(tool_name='monitored_tool', status='success').inc()
        return result

    except Exception as e:
        tool_call_counter.labels(tool_name='monitored_tool', status='error').inc()
        raise

    finally:
        duration = time.time() - start
        tool_call_duration.labels(tool_name='monitored_tool').observe(duration)
```

### Performance Checklist

- [ ] **Hardware**: GPU acceleration for compute-intensive workloads
- [ ] **Containerization**: Resource limits and optimized configuration
- [ ] **Tool Design**: Grouped tools, avoid proliferation
- [ ] **Async/Sync**: Appropriate choice for operation type
- [ ] **Caching**: Multi-layer strategy with appropriate TTLs
- [ ] **Connection Pooling**: Reuse connections, HTTP/2 enabled
- [ ] **Batch Processing**: Group operations when possible
- [ ] **Load Balancing**: Horizontal scaling with health checks
- [ ] **Monitoring**: Prometheus metrics for performance tracking
- [ ] **Profiling**: Regular performance profiling and optimization

---

## FastMCP Implementation Patterns

FastMCP 2.0 is a production-ready framework providing **5x faster development** compared to raw SDK implementation.

### Core Decorator Pattern

```python
from fastmcp import FastMCP

mcp = FastMCP("Demo Server 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b

# Automatic schema generation from type hints and docstring
```

**Key Features**:
- Minimal boilerplate (few lines for full server)
- Automatic schema generation from type hints
- Docstrings become tool descriptions
- Built-in validation

### Resource Templates Pattern



---

**Navigation**: [← Part 2](./02_Transport_Layer.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 4 →](./04_Security_Error_Handling.md)
**Part 3 of 6** | Lines 961-1440 of original document
