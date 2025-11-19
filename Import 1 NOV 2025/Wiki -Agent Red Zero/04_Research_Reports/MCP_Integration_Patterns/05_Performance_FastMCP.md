# Part 5 of 6: Performance & FastMCP

**Series**: MCP Integration Patterns
**Navigation**: [← Part 4](./04_Security_Error_Handling.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 6 →](./06_Integration_Cases.md)

---


                self.log(f"Registered tool: {namespaced_name}")
```

### Agent Zero + FastMCP Integration

```python
from fastmcp import FastMCP
from agent_zero.mcp import MCPServerLocal

# Create custom MCP server with FastMCP
mcp = FastMCP("custom-tools")

@mcp.tool
async def analyze_code(code: str, language: str):
    """Analyze code quality and suggest improvements"""
    analysis = await code_analyzer.analyze(code, language)
    return {
        "issues": analysis.issues,
        "suggestions": analysis.suggestions,
        "score": analysis.quality_score
    }

@mcp.tool
async def refactor_code(code: str, target_pattern: str):
    """Refactor code to follow specified pattern"""
    refactored = await code_refactor.apply(code, target_pattern)
    return {"code": refactored, "changes": refactored.changes}

# Run as server
if __name__ == "__main__":
    mcp.run(transport="stdio")

# Configure in Agent Zero
# agent_config.yaml:
# custom-tools:
#   type: local
#   command: python
#   args: [custom_tools.py]
```

### Error Handling in Agent Zero

```python
class AgentZero:
    async def call_mcp_tool(self, tool_name: str, args: dict):
        """Call MCP tool with error handling"""
        server_name, base_tool_name = tool_name.split(".", 1)
        server = self.mcp_servers.get(server_name)

        if not server:
            raise ValueError(f"MCP server '{server_name}' not found")

        try:
            result = await server.call_tool(base_tool_name, args)
            return result

        except MCPError as e:
            if e.is_retryable:
                # Retry with backoff
                return await self._retry_tool_call(server, base_tool_name, args)
            else:
                # Report to user, suggest alternative
                self.log(f"Tool call failed: {e.message}")
                raise

        except ConnectionError:
            # Attempt reconnection
            await server.reconnect()
            return await server.call_tool(base_tool_name, args)
```

### Agent Learning with MCP

```python
class AgentZero:
    async def learn_from_mcp_usage(self, tool_name: str, args: dict, result: dict):
        """Learn patterns from successful MCP tool usage"""

        # Store successful pattern
        pattern = {
            "tool": tool_name,
            "args_pattern": self._extract_pattern(args),
            "context": self.current_task_context,
            "result_type": type(result).__name__,
            "success": True,
            "timestamp": datetime.now()
        }

        await self.memory.store_pattern(pattern)

        # Update tool usage statistics
        self.tool_stats[tool_name]["success_count"] += 1
        self.tool_stats[tool_name]["avg_execution_time"] = (
            self._update_running_average(
                self.tool_stats[tool_name]["avg_execution_time"],
                result.get("execution_time", 0)
            )
        )

    async def suggest_tool_for_task(self, task_description: str):
        """Suggest best MCP tool based on learned patterns"""

        # Query memory for similar past tasks
        similar_patterns = await self.memory.find_similar(
            task_description,
            limit=10
        )

        # Rank tools by success rate and relevance
        tool_scores = {}
        for pattern in similar_patterns:
            tool = pattern["tool"]
            tool_scores[tool] = tool_scores.get(tool, 0) + pattern["similarity"]

        # Return top suggestion
        best_tool = max(tool_scores.items(), key=lambda x: x[1])
        return best_tool[0]
```

### Integration Benefits

1. **Extensibility**: Easy to add new MCP servers without modifying agent core
2. **Modularity**: Each MCP server provides isolated functionality
3. **Learning**: Agent learns which tools work best for specific tasks
4. **Transparency**: Full visibility into tool selection and execution
5. **Error Recovery**: Automatic retry and fallback mechanisms
6. **Dynamic Growth**: Agent capabilities grow as new MCP servers are added

---

## Real-World Case Studies

### Healthcare: Mayo Clinic Patient Engagement

**Challenge**: High volume of patient support queries

**Solution**:
- Deployed MCP-based chatbot on AWS
- Integrated with EHR (Electronic Health Records) via MCP server
- Connected to appointment scheduling system

**Implementation**:
```python
# Healthcare MCP server
@mcp.tool
async def get_patient_records(patient_id: str, ctx: Context):
    """HIPAA-compliant patient record access"""
    # Verify authorization
    if not ctx.user.has_permission("read:patient_records"):
        raise MCPError(-32000, "Unauthorized")

    # Audit log
    await audit.log("RECORD_ACCESS", patient_id, ctx.user.id)

    # Fetch records
    records = await ehr_system.get_records(patient_id)
    return sanitize_phi(records)  # Remove excessive PHI

@mcp.tool
async def schedule_appointment(patient_id: str, doctor_id: str, date: str):
    """Schedule patient appointment"""
    slot = await scheduling_system.find_slot(doctor_id, date)
    appointment = await scheduling_system.book(patient_id, slot)

    # Send confirmation
    await notification_service.send_sms(patient_id, f"Appointment confirmed: {date}")

    return {"appointment_id": appointment.id, "time": slot.time}
```

**Results**:
- **30% reduction** in patient support queries
- **25% faster** response times
- **95% patient satisfaction** with automated system
- HIPAA compliance maintained

**Key Learnings**:
- Strong authentication and audit logging essential
- PHI sanitization prevents data leakage
- Integration with existing systems (EHR, scheduling) crucial

### Healthcare: AI Diagnostics for Medical Imaging

**Challenge**: Long patient wait times for imaging analysis

**Solution**:
- MCP-enabled AI diagnostics tool
- Integrated with PACS (Picture Archiving and Communication System)
- Real-time analysis with radiologist review

**Results**:
- **30% reduction** in patient waiting time
- **15% improvement** in early detection rates
- Faster doctor decision-making with AI-assisted analysis

### E-Commerce: Product Recommendation Engine

**Challenge**: Improve conversion rates with personalized recommendations

**Solution**:
- MCP server integrating multiple data sources
- Real-time recommendation engine
- A/B testing framework

**Implementation**:
```python
@mcp.tool
async def get_recommendations(user_id: str, context: str):
    """Multi-source recommendation engine"""

    # Parallel data gathering
    user_history, browsing_data, inventory = await asyncio.gather(
        purchase_history.get(user_id),
        browsing_tracker.get(user_id),
        inventory_system.get_available()
    )

    # ML model inference
    recommendations = await ml_model.predict(
        user_history=user_history,
        browsing=browsing_data,
        inventory=inventory,
        context=context
    )

    return {
        "recommendations": recommendations,
        "confidence": ml_model.confidence,
        "personalization_score": calculate_score(user_history)
    }
```

**Results**:
- **18% uplift** in conversion rates
- **22% increase** in average order value
- **40% improvement** in recommendation relevance

**Key Techniques**:
- Parallel data gathering (3 sources simultaneously)
- Real-time ML inference
- Context-aware recommendations

### Telecommunications: Customer Support Automation

**Challenge**: High volume of repetitive customer queries

**Solution**:
- MCP-based intelligent routing system
- FAQ automation with escalation to humans
- Integration with CRM and ticketing systems

**Results**:
- **50% reduction** in response times
- **35% decrease** in human agent workload
- **$2M annual savings** in support costs
- **88% query resolution** without human intervention

### Financial Services: AI Trading Agents

**Challenge**: Reduce latency in market reaction times

**Solution**:
- MCP servers for real-time market data feeds
- Secure API access to brokerage systems
- Algorithmic trading strategy execution

**Implementation**:
```python
@mcp.tool
async def execute_trade(
    symbol: str,
    action: Literal["buy", "sell"],
    quantity: int,
    limit_price: float,
    ctx: Context
):
    """Execute trade with risk checks"""

    # Risk validation
    portfolio = await portfolio_manager.get_portfolio(ctx.user.id)
    if not risk_checker.validate_trade(portfolio, symbol, quantity, limit_price):
        raise MCPError(-32000, "Trade rejected by risk management")

    # Compliance check
    if not compliance.check_regulatory_approval(ctx.user.id, symbol):
        raise MCPError(-32000, "Regulatory restriction")

    # Execute through brokerage API
    order = await brokerage_api.place_order({
        "symbol": symbol,
        "side": action,
        "quantity": quantity,
        "order_type": "limit",
        "limit_price": limit_price
    })

    # Audit trail
    await audit.log_trade(ctx.user.id, order)

    return {"order_id": order.id, "status": order.status}
```

**Results**:
- **15ms reduction** in trade execution latency
- **3x faster** deployment of new trading strategies
- Enhanced risk management with automated checks

**Key Considerations**:
- Multi-layer risk validation
- Regulatory compliance automation
- Complete audit trail
- Real-time market data integration

### DevOps: CI/CD Pipeline Automation

**Challenge**: Manual deployment processes slow down releases

**Solution**:
- MCP servers for GitHub, Terraform, Ansible
- AI-driven deployment orchestration
- Automated rollback on failure detection

**Integration**:
```python
# GitHub MCP server
@mcp.tool
async def create_pull_request(repo: str, branch: str, title: str, body: str):
    """Create GitHub pull request"""
    pr = await github_api.create_pr(repo, branch, title, body)
    return {"pr_number": pr.number, "url": pr.html_url}

# Terraform MCP server
@mcp.tool
async def terraform_apply(workspace: str, auto_approve: bool = False):
    """Apply Terraform configuration"""
    if not auto_approve:
        plan = await terraform.plan(workspace)
        # Agent reviews plan before applying
        return {"plan": plan, "requires_approval": True}

    result = await terraform.apply(workspace)
    return {"applied": True, "resources": result.resources_changed}
```

**Results**:
- **80% reduction** in deployment time
- **60% fewer** deployment errors
- **Complete automation** of repetitive tasks
- Faster rollback with AI-detected failures

### Adoption by Developer Tools

**Immediate Adopters**:
- **Zed**: Text editor with native MCP support
- **Replit**: Online IDE with MCP integration
- **Codeium**: AI code completion with MCP
- **Sourcegraph**: Code search with MCP servers
- **Cursor**: AI-powered editor with MCP

**Why Developer Tools Adopted Quickly**:
- Open protocol with reference implementations
- Already implemented in Claude (validation)
- Solves real integration pain points
- Community-driven server ecosystem

---

## Common Integration Challenges

### 1. Transport Selection Confusion

**Challenge**: Choosing between stdio, SSE, and StreamableHTTP

**Solution**:
```python
# Decision matrix
def select_transport(deployment_type: str) -> str:
    """Select appropriate transport based on deployment"""

    if deployment_type == "desktop_app":
        return "stdio"  # Local subprocess
    elif deployment_type == "cli_tool":
        return "stdio"  # Simple process management
    elif deployment_type == "cloud_service":
        return "streamable-http"  # Network accessible
    elif deployment_type == "microservice":
        return "streamable-http"  # Load balancer compatible
    elif deployment_type == "legacy_remote":
        return "sse"  # Deprecated but supported
    else:
        raise ValueError(f"Unknown deployment type: {deployment_type}")
```

**Best Practice**: Default to stdio for local, StreamableHTTP for remote

### 2. State Management Complexity

**Challenge**: Deciding between in-memory, Redis, or database for state

**Solution Matrix**:
```python
def select_state_backend(requirements: dict) -> str:
    """Choose state backend based on requirements"""

    needs_persistence = requirements.get("survives_restart", False)
    needs_scaling = requirements.get("multi_instance", False)
    needs_audit = requirements.get("audit_trail", False)
    traffic_volume = requirements.get("requests_per_minute", 0)

    if needs_audit:
        return "database"  # Complete history required
    elif needs_scaling or traffic_volume > 1000:
        return "redis"  # Distributed state
    elif needs_persistence:
        return "database"  # Long-term storage
    else:
        return "memory"  # Simple and fast
```

### 3. Tool Discovery at Scale

**Challenge**: Managing hundreds of tools across multiple servers

**Solution - Categorization and Search**:
```python
class ToolRegistry:
    """Organize tools with metadata and search"""

    def __init__(self):
        self.tools = {}
        self.categories = {}

    def register_tool(self, name: str, metadata: dict):
        """Register tool with rich metadata"""
        self.tools[name] = {
            "name": name,
            "description": metadata["description"],
            "category": metadata.get("category", "general"),
            "tags": metadata.get("tags", []),
            "parameters": metadata["parameters"],
            "examples": metadata.get("examples", [])
        }

        # Index by category
        category = metadata.get("category", "general")
        self.categories.setdefault(category, []).append(name)

    def search_tools(self, query: str, category: str = None) -> list:
        """Search tools by keywords and category"""
        results = []

        for name, metadata in self.tools.items():
            # Filter by category if specified
            if category and metadata["category"] != category:
                continue

            # Search in name, description, tags
            searchable = f"{name} {metadata['description']} {' '.join(metadata['tags'])}"
            if query.lower() in searchable.lower():
                results.append(metadata)

        return results

    def list_categories(self) -> dict:
        """List available categories with tool counts"""
        return {
            category: len(tools)
            for category, tools in self.categories.items()
        }

# Usage
registry = ToolRegistry()

registry.register_tool("github.create_issue", {
    "description": "Create a GitHub issue",
    "category": "version_control",
    "tags": ["github", "issue", "tracking"],
    "parameters": {...},
    "examples": [...]


---

**Navigation**: [← Part 4](./04_Security_Error_Handling.md) | [📚 Series Overview](./00_Series_Overview.md) | [Part 6 →](./06_Integration_Cases.md)
**Part 5 of 6** | Lines 1921-2400 of original document
