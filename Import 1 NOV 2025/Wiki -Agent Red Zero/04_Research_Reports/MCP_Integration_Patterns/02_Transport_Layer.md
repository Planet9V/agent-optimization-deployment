# Part 2 of 6: Transport Layer

**Series**: MCP Integration Patterns
**Navigation**: [← Part 1](./01_Overview_Architecture.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 3 →](./03_Communication_Tools.md)

---

   - Establish context during capability negotiation
   - Set appropriate timeouts and expiration

2. **Context Updates**
   - Update atomically to prevent race conditions
   - Validate context size to prevent memory bloat
   - Use incremental updates, not full replacements

3. **Session Cleanup**
   - Implement TTL-based expiration
   - Clean up on explicit disconnect
   - Periodic garbage collection for orphaned sessions

4. **Context Sharing**
   - Enable cross-session context sharing when needed
   - Implement proper access control
   - Consider privacy implications

---

## Error Handling and Recovery

### Error Response Structure

MCP follows JSON-RPC 2.0 error format:

```json
{
  "jsonrpc": "2.0",
  "id": 123,
  "error": {
    "code": -32603,
    "message": "Internal error",
    "data": {
      "details": "Database connection timeout",
      "retryable": true
    }
  }
}
```

### Standardized Error Codes

| Code | Meaning | Retry Strategy |
|------|---------|---------------|
| -32700 | Parse error | No retry (client issue) |
| -32600 | Invalid request | No retry (fix request) |
| -32601 | Method not found | No retry (check tool availability) |
| -32602 | Invalid params | No retry (fix parameters) |
| -32603 | Internal error | Retry with backoff |
| -32000 | Server error | Retry with backoff |
| Custom | Domain-specific | Based on `retryable` flag |

### Retry Mechanisms

#### Exponential Backoff Pattern

```python
import asyncio
import random

async def call_with_retry(client, tool_name, args, max_attempts=3):
    """Call MCP tool with exponential backoff retry"""
    for attempt in range(max_attempts):
        try:
            result = await client.call_tool(tool_name, args)
            return result

        except MCPError as e:
            if not e.is_retryable or attempt == max_attempts - 1:
                raise

            # Exponential backoff with jitter
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(wait_time)

    raise MaxRetriesExceeded(f"Failed after {max_attempts} attempts")
```

**Key Features**:
- Incremental wait times: 1s, 2s, 4s, 8s...
- Random jitter prevents thundering herd
- Respects `retryable` flag in error response
- Configurable max attempts (typically 3-5)

#### Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.last_failure_time = None

    async def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitOpenError("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)

            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0

            return result

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"

            raise
```

**Benefits**:
- Prevents cascading failures
- Allows service recovery time
- Automatic state transitions
- Fast-fail when service is down

### Advanced Recovery Strategies

#### Fallback Pattern

```python
async def call_with_fallback(primary_server, fallback_server, tool, args):
    """Try primary, fall back to secondary on failure"""
    try:
        return await primary_server.call_tool(tool, args)
    except MCPError as e:
        if e.is_transient:
            # Use fallback for transient failures
            return await fallback_server.call_tool(tool, args)
        raise
```

#### Graceful Degradation

```python
async def enhanced_search(query, use_cache=True):
    """Search with graceful degradation"""
    try:
        # Try full-featured search
        return await mcp.call_tool("advanced_search", {"query": query})

    except MCPError as e:
        if e.code == -32603:  # Internal error
            # Fall back to basic search
            return await mcp.call_tool("basic_search", {"query": query})

    except Exception:
        if use_cache:
            # Last resort: return cached results
            return cache.get(f"search:{query}", default=[])
        raise
```

### Error Handling Best Practices

1. **Structured Error Responses**
   - Always include `isError` flag
   - Provide human-readable messages
   - Include machine-readable error codes
   - Add retry guidance in error data

2. **Idempotency for Retries**
   - Only retry idempotent operations
   - Use request IDs to detect duplicates
   - Design tools to be safely retryable

3. **Client-Side Resilience**
   - Implement timeout mechanisms
   - Use circuit breakers for failing services
   - Log errors with context for debugging
   - Provide user-friendly error messages

4. **Server-Side Robustness**
   - Validate all inputs before processing
   - Catch and handle internal exceptions
   - Return structured errors, never crash
   - Implement rate limiting to prevent abuse

5. **Monitoring and Alerting**
   - Track error rates by type and code
   - Alert on circuit breaker state changes
   - Monitor retry success rates
   - Log error patterns for analysis

---

## Security Best Practices

Security is critical for production MCP deployments. Multiple layers of defense are essential.

### Authentication and Authorization

#### OAuth 2.0 Implementation

```python
from fastmcp import FastMCP

mcp = FastMCP("secure-server")

# OAuth 2.0 configuration
mcp.add_auth(
    provider="oauth2",
    client_id=os.getenv("OAUTH_CLIENT_ID"),
    client_secret=os.getenv("OAUTH_CLIENT_SECRET"),
    authorization_url="https://auth.example.com/authorize",
    token_url="https://auth.example.com/token"
)

@mcp.tool(requires_auth=True)
async def protected_operation(data: str):
    """Operation requiring authentication"""
    return f"Processed: {data}"
```

**Best Practices**:
- Use **OAuth 2.1** with Authorization Code + PKCE flow
- Verify authorization server metadata and keys
- Implement token refresh mechanisms
- Never store tokens in code or config files

#### Role-Based Access Control (RBAC)

```python
from enum import Enum

class Role(Enum):
    VIEWER = "viewer"
    USER = "user"
    ADMIN = "admin"

# Tool-level permissions
@mcp.tool(required_roles=[Role.ADMIN])
async def delete_resource(resource_id: str):
    """Delete resource - admin only"""
    await db.delete(resource_id)
    return {"status": "deleted"}

@mcp.tool(required_roles=[Role.USER, Role.ADMIN])
async def update_resource(resource_id: str, data: dict):
    """Update resource - user or admin"""
    await db.update(resource_id, data)
    return {"status": "updated"}
```

**Implementation**:
- Assign roles during authentication
- Validate roles before tool execution
- Implement principle of least privilege
- Audit role assignments regularly

### Input/Output Validation

#### JSON Schema Validation

```python
from pydantic import BaseModel, Field, validator

class ToolInput(BaseModel):
    """Strictly validated input schema"""
    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(default=10, ge=1, le=100)
    user_id: str = Field(..., pattern=r'^[a-zA-Z0-9_-]+$')

    @validator('query')
    def sanitize_query(cls, v):
        # Remove potentially dangerous characters
        return v.replace(';', '').replace('--', '')

@mcp.tool
async def search(input: ToolInput):
    """Search with validated input"""
    results = await db.search(input.query, limit=input.limit)
    return results
```

**Validation Requirements**:
- Enforce strict JSON schemas for all inputs
- Use parameter allowlists, not denylists
- Set length caps on string inputs
- Reject malformed or unrecognized parameters
- Sanitize before execution to prevent injection

#### Output Sanitization

```python
import re

async def sanitize_output(data: dict) -> dict:
    """Remove sensitive information from output"""
    sensitive_patterns = [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Emails
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b(?:\d{4}[-\s]?){3}\d{4}\b',  # Credit cards
    ]

    for key, value in data.items():
        if isinstance(value, str):
            for pattern in sensitive_patterns:
                value = re.sub(pattern, '[REDACTED]', value)
            data[key] = value

    return data
```

### Runtime Security and Monitoring

#### Threat Detection

```python
class ThreatDetector:
    def __init__(self):
        self.baselines = {}

    async def monitor_tool_call(self, tool_name, user_id, params):
        """Monitor for anomalous behavior"""

        # Track call frequency
        key = f"{user_id}:{tool_name}"
        self.baselines.setdefault(key, {"count": 0, "window_start": time.time()})

        baseline = self.baselines[key]
        baseline["count"] += 1

        # Check for rate anomalies
        elapsed = time.time() - baseline["window_start"]
        if elapsed > 60:  # Reset window every minute
            baseline["count"] = 1
            baseline["window_start"] = time.time()
        elif baseline["count"] > 100:  # >100 calls/min
            raise AnomalyDetected(f"Unusual activity: {baseline['count']} calls/min")

        # Check for prompt injection patterns
        param_str = json.dumps(params)
        if any(pattern in param_str.lower() for pattern in [
            "ignore previous instructions",
            "disregard all",
            "you are now",
            "system:"
        ]):
            raise PossiblePromptInjection("Suspicious prompt detected")
```

#### Data Loss Prevention (DLP)

```python
import re

class DLPGuard:
    """Prevent leakage of sensitive data"""

    PII_PATTERNS = {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'ssn': r'\d{3}-\d{2}-\d{4}',
        'api_key': r'(api[_-]?key|apikey)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_-]+)',
        'password': r'(password|passwd|pwd)["\']?\s*[:=]\s*["\']?([^\s"\']+)',
    }

    async def scan_output(self, data: str) -> tuple[bool, list]:
        """Scan for PII/secrets in output"""
        violations = []

        for category, pattern in self.PII_PATTERNS.items():
            matches = re.findall(pattern, data, re.IGNORECASE)
            if matches:
                violations.append({
                    "category": category,
                    "count": len(matches)
                })

        return len(violations) == 0, violations

    async def redact_output(self, data: str) -> str:
        """Redact sensitive information"""
        for category, pattern in self.PII_PATTERNS.items():
            data = re.sub(pattern, f'[REDACTED_{category.upper()}]', data, flags=re.IGNORECASE)
        return data
```

### Isolation and Sandboxing

#### Container Isolation

```dockerfile
# Dockerfile for secure MCP server
FROM python:3.11-slim

# Run as non-root user
RUN useradd -m -u 1000 mcpuser

# Read-only filesystem
VOLUME ["/app"]
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Switch to non-root
USER mcpuser

# Run with security options
CMD ["python", "-u", "server.py"]
```

**Docker Compose Configuration**:
```yaml
services:
  mcp-server:
    build: .
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    networks:
      - mcp-network
    environment:
      - PYTHONUNBUFFERED=1
```

**Best Practices**:
- Run servers in unprivileged containers
- Use read-only filesystems
- Drop all unnecessary capabilities
- Network segmentation between services
- Implement resource limits (CPU, memory)

#### Safety Profiles

```python
class SafetyProfile(Enum):
    """Declare safety requirements for tools"""
    SAFE = "safe"  # No side effects
    FILE_SYSTEM = "filesystem"  # File access required
    NETWORK = "network"  # Network access required
    PRIVILEGED = "privileged"  # Elevated permissions

@mcp.tool(safety_profile=SafetyProfile.PRIVILEGED)
async def system_command(cmd: str):
    """Execute system command - runs in isolated sandbox"""
    # This would run in VM or isolated container
    pass
```

### Secrets Management

#### Environment-Based Configuration

```python
import os
from typing import Optional

class SecretsManager:
    """Secure secrets loading"""

    @staticmethod
    def get_secret(key: str, default: Optional[str] = None) -> str:
        """Load secret from environment or vault"""

        # Try environment variable first
        value = os.getenv(key)
        if value:
            return value

        # Try secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)
        try:


---

**Navigation**: [← Part 1](./01_Overview_Architecture.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 3 →](./03_Communication_Tools.md)
**Part 2 of 6** | Lines 481-960 of original document
