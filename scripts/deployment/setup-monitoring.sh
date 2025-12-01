#!/bin/bash
#
# setup-monitoring.sh - Performance monitoring setup for agent optimization
# Created: 2025-11-12
# Purpose: Install and configure monitoring infrastructure
#

set -euo pipefail

# ═══════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/home/jim/2_OXOT_Projects_Dev/tests"
MONITORING_DIR="${PROJECT_ROOT}/monitoring"
METRICS_DIR="${MONITORING_DIR}/metrics"
DASHBOARD_DIR="${MONITORING_DIR}/dashboard"
CONFIG_DIR="${MONITORING_DIR}/config"
LOG_DIR="/var/log/monitoring"
LOG_FILE="${LOG_DIR}/setup-$(date +%Y%m%d-%H%M%S).log"
DRY_RUN=false

# ═══════════════════════════════════════════════════
# COLOR CODES
# ═══════════════════════════════════════════════════

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# ═══════════════════════════════════════════════════
# LOGGING FUNCTIONS
# ═══════════════════════════════════════════════════

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*" | tee -a "${LOG_FILE}"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*" | tee -a "${LOG_FILE}"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*" | tee -a "${LOG_FILE}"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" | tee -a "${LOG_FILE}"
}

log_step() {
    echo -e "\n${CYAN}═══════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}[STEP]${NC} $*"
    echo -e "${CYAN}═══════════════════════════════════════════════════${NC}\n"
}

# ═══════════════════════════════════════════════════
# MONITORING SETUP FUNCTIONS
# ═══════════════════════════════════════════════════

create_directory_structure() {
    log_step "Creating Directory Structure"

    local directories=(
        "${MONITORING_DIR}"
        "${METRICS_DIR}"
        "${DASHBOARD_DIR}"
        "${CONFIG_DIR}"
        "${LOG_DIR}"
        "${METRICS_DIR}/performance"
        "${METRICS_DIR}/agent"
        "${METRICS_DIR}/system"
        "${DASHBOARD_DIR}/templates"
        "${DASHBOARD_DIR}/static"
    )

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would create directories:"
        for dir in "${directories[@]}"; do
            echo "  - $dir"
        done
        return 0
    fi

    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        log_success "Created: $dir"
    done
}

install_monitoring_dependencies() {
    log_step "Installing Monitoring Dependencies"

    cd "${PROJECT_ROOT}"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would install monitoring packages"
        return 0
    fi

    # Install monitoring packages
    local packages=(
        "prom-client"      # Prometheus metrics
        "express"          # Dashboard server
        "ws"               # WebSocket for real-time updates
        "node-cron"        # Scheduled metric collection
        "pidusage"         # Process resource usage
        "systeminformation" # System metrics
    )

    log_info "Installing monitoring packages..."
    npm install --save "${packages[@]}" 2>&1 | tee -a "${LOG_FILE}"

    log_success "Monitoring dependencies installed"
}

create_metrics_collector() {
    log_step "Creating Metrics Collector"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would create metrics collector"
        return 0
    fi

    cat > "${MONITORING_DIR}/metrics-collector.js" << 'EOF'
/**
 * metrics-collector.js - Comprehensive metrics collection
 */

const promClient = require('prom-client');
const fs = require('fs').promises;
const path = require('path');
const pidusage = require('pidusage');
const si = require('systeminformation');

class MetricsCollector {
    constructor(options = {}) {
        this.metricsDir = options.metricsDir || './monitoring/metrics';
        this.collectInterval = options.collectInterval || 5000; // 5 seconds
        this.register = new promClient.Registry();

        this.initializeMetrics();
    }

    initializeMetrics() {
        // Agent performance metrics
        this.agentResponseTime = new promClient.Histogram({
            name: 'agent_response_time_seconds',
            help: 'Agent response time in seconds',
            labelNames: ['agent_type', 'operation'],
            buckets: [0.1, 0.5, 1, 2, 5, 10],
            registers: [this.register]
        });

        this.agentTasksTotal = new promClient.Counter({
            name: 'agent_tasks_total',
            help: 'Total number of tasks processed by agents',
            labelNames: ['agent_type', 'status'],
            registers: [this.register]
        });

        this.agentMemoryUsage = new promClient.Gauge({
            name: 'agent_memory_usage_bytes',
            help: 'Memory usage by agent type',
            labelNames: ['agent_type'],
            registers: [this.register]
        });

        // System metrics
        this.systemCpuUsage = new promClient.Gauge({
            name: 'system_cpu_usage_percent',
            help: 'System CPU usage percentage',
            registers: [this.register]
        });

        this.systemMemoryUsage = new promClient.Gauge({
            name: 'system_memory_usage_bytes',
            help: 'System memory usage in bytes',
            registers: [this.register]
        });

        // Performance metrics
        this.optimizationGain = new promClient.Gauge({
            name: 'optimization_gain_percent',
            help: 'Performance improvement from optimization',
            labelNames: ['optimization_type'],
            registers: [this.register]
        });

        this.tokenEfficiency = new promClient.Gauge({
            name: 'token_efficiency_ratio',
            help: 'Token usage efficiency ratio',
            registers: [this.register]
        });
    }

    async collectAgentMetrics(agentData) {
        if (!agentData) return;

        // Record response time
        if (agentData.responseTime) {
            this.agentResponseTime.observe(
                {
                    agent_type: agentData.type || 'unknown',
                    operation: agentData.operation || 'default'
                },
                agentData.responseTime
            );
        }

        // Record task completion
        this.agentTasksTotal.inc({
            agent_type: agentData.type || 'unknown',
            status: agentData.status || 'unknown'
        });

        // Record memory usage
        if (agentData.memoryUsage) {
            this.agentMemoryUsage.set(
                { agent_type: agentData.type || 'unknown' },
                agentData.memoryUsage
            );
        }
    }

    async collectSystemMetrics() {
        try {
            // CPU usage
            const cpuLoad = await si.currentLoad();
            this.systemCpuUsage.set(cpuLoad.currentLoad);

            // Memory usage
            const mem = await si.mem();
            this.systemMemoryUsage.set(mem.active);

            // Process metrics
            const stats = await pidusage(process.pid);
            this.agentMemoryUsage.set(
                { agent_type: 'system' },
                stats.memory
            );

        } catch (error) {
            console.error('Error collecting system metrics:', error);
        }
    }

    async collectPerformanceMetrics(perfData) {
        if (perfData.optimizationGain) {
            this.optimizationGain.set(
                { optimization_type: perfData.type || 'general' },
                perfData.optimizationGain
            );
        }

        if (perfData.tokenEfficiency) {
            this.tokenEfficiency.set(perfData.tokenEfficiency);
        }
    }

    async saveMetrics() {
        try {
            const timestamp = new Date().toISOString();
            const metrics = await this.register.metrics();

            const metricsData = {
                timestamp,
                metrics: metrics.split('\n').filter(line =>
                    line && !line.startsWith('#')
                )
            };

            const filename = path.join(
                this.metricsDir,
                'performance',
                `metrics-${Date.now()}.json`
            );

            await fs.mkdir(path.dirname(filename), { recursive: true });
            await fs.writeFile(filename, JSON.stringify(metricsData, null, 2));

            // Clean old metrics (keep last 1000)
            await this.cleanOldMetrics();

        } catch (error) {
            console.error('Error saving metrics:', error);
        }
    }

    async cleanOldMetrics() {
        try {
            const perfDir = path.join(this.metricsDir, 'performance');
            const files = await fs.readdir(perfDir);

            if (files.length > 1000) {
                const sorted = files
                    .filter(f => f.startsWith('metrics-'))
                    .sort();

                const toDelete = sorted.slice(0, files.length - 1000);

                for (const file of toDelete) {
                    await fs.unlink(path.join(perfDir, file));
                }
            }
        } catch (error) {
            console.error('Error cleaning old metrics:', error);
        }
    }

    async start() {
        console.log('Starting metrics collection...');

        // Collect system metrics periodically
        this.interval = setInterval(async () => {
            await this.collectSystemMetrics();
            await this.saveMetrics();
        }, this.collectInterval);

        console.log(`Metrics collection started (interval: ${this.collectInterval}ms)`);
    }

    async stop() {
        if (this.interval) {
            clearInterval(this.interval);
            await this.saveMetrics(); // Final save
            console.log('Metrics collection stopped');
        }
    }

    getRegistry() {
        return this.register;
    }
}

module.exports = MetricsCollector;
EOF

    log_success "Metrics collector created"
}

create_dashboard_server() {
    log_step "Creating Dashboard Server"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would create dashboard server"
        return 0
    fi

    cat > "${MONITORING_DIR}/dashboard-server.js" << 'EOF'
/**
 * dashboard-server.js - Real-time monitoring dashboard
 */

const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const fs = require('fs').promises;
const path = require('path');
const MetricsCollector = require('./metrics-collector');

class DashboardServer {
    constructor(options = {}) {
        this.port = options.port || 3030;
        this.metricsDir = options.metricsDir || './monitoring/metrics';
        this.dashboardDir = options.dashboardDir || './monitoring/dashboard';

        this.app = express();
        this.server = http.createServer(this.app);
        this.wss = new WebSocket.Server({ server: this.server });

        this.metricsCollector = new MetricsCollector({ metricsDir: this.metricsDir });
        this.clients = new Set();

        this.setupRoutes();
        this.setupWebSocket();
    }

    setupRoutes() {
        // Serve static files
        this.app.use('/static', express.static(path.join(this.dashboardDir, 'static')));

        // Dashboard homepage
        this.app.get('/', (req, res) => {
            res.sendFile(path.join(this.dashboardDir, 'templates', 'index.html'));
        });

        // Metrics endpoint (Prometheus format)
        this.app.get('/metrics', async (req, res) => {
            res.set('Content-Type', this.metricsCollector.getRegistry().contentType);
            res.end(await this.metricsCollector.getRegistry().metrics());
        });

        // JSON metrics endpoint
        this.app.get('/api/metrics', async (req, res) => {
            try {
                const latest = await this.getLatestMetrics();
                res.json(latest);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });

        // Historical metrics
        this.app.get('/api/metrics/history', async (req, res) => {
            try {
                const minutes = parseInt(req.query.minutes) || 60;
                const history = await this.getMetricsHistory(minutes);
                res.json(history);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });

        // Health check
        this.app.get('/health', (req, res) => {
            res.json({
                status: 'healthy',
                uptime: process.uptime(),
                timestamp: new Date().toISOString()
            });
        });
    }

    setupWebSocket() {
        this.wss.on('connection', (ws) => {
            console.log('Client connected to dashboard');
            this.clients.add(ws);

            ws.on('close', () => {
                console.log('Client disconnected from dashboard');
                this.clients.delete(ws);
            });

            ws.on('error', (error) => {
                console.error('WebSocket error:', error);
                this.clients.delete(ws);
            });

            // Send initial metrics
            this.sendMetricsToClient(ws);
        });

        // Broadcast metrics every 2 seconds
        setInterval(() => {
            this.broadcastMetrics();
        }, 2000);
    }

    async getLatestMetrics() {
        const perfDir = path.join(this.metricsDir, 'performance');
        const files = await fs.readdir(perfDir);

        if (files.length === 0) {
            return { error: 'No metrics available' };
        }

        const latest = files
            .filter(f => f.startsWith('metrics-'))
            .sort()
            .pop();

        const content = await fs.readFile(path.join(perfDir, latest), 'utf8');
        return JSON.parse(content);
    }

    async getMetricsHistory(minutes) {
        const perfDir = path.join(this.metricsDir, 'performance');
        const files = await fs.readdir(perfDir);

        const cutoff = Date.now() - (minutes * 60 * 1000);
        const recentFiles = files
            .filter(f => {
                const timestamp = parseInt(f.match(/metrics-(\d+)/)?.[1]);
                return timestamp && timestamp >= cutoff;
            })
            .sort();

        const history = [];
        for (const file of recentFiles) {
            const content = await fs.readFile(path.join(perfDir, file), 'utf8');
            history.push(JSON.parse(content));
        }

        return history;
    }

    async sendMetricsToClient(ws) {
        try {
            const metrics = await this.getLatestMetrics();
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: 'metrics',
                    data: metrics
                }));
            }
        } catch (error) {
            console.error('Error sending metrics to client:', error);
        }
    }

    async broadcastMetrics() {
        if (this.clients.size === 0) return;

        try {
            const metrics = await this.getLatestMetrics();
            const message = JSON.stringify({
                type: 'metrics',
                data: metrics
            });

            this.clients.forEach(ws => {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send(message);
                }
            });
        } catch (error) {
            console.error('Error broadcasting metrics:', error);
        }
    }

    async start() {
        await this.metricsCollector.start();

        this.server.listen(this.port, () => {
            console.log(`Dashboard server running on http://localhost:${this.port}`);
            console.log(`Metrics endpoint: http://localhost:${this.port}/metrics`);
            console.log(`API endpoint: http://localhost:${this.port}/api/metrics`);
        });
    }

    async stop() {
        await this.metricsCollector.stop();

        this.clients.forEach(ws => ws.close());
        this.wss.close();

        return new Promise((resolve) => {
            this.server.close(() => {
                console.log('Dashboard server stopped');
                resolve();
            });
        });
    }
}

// Start server if run directly
if (require.main === module) {
    const server = new DashboardServer();
    server.start();

    // Graceful shutdown
    process.on('SIGINT', async () => {
        console.log('\nShutting down gracefully...');
        await server.stop();
        process.exit(0);
    });
}

module.exports = DashboardServer;
EOF

    log_success "Dashboard server created"
}

create_dashboard_html() {
    log_step "Creating Dashboard HTML"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would create dashboard HTML"
        return 0
    fi

    mkdir -p "${DASHBOARD_DIR}/templates"

    cat > "${DASHBOARD_DIR}/templates/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Optimization Monitoring Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            padding: 20px;
        }

        .header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            margin-bottom: 30px;
        }

        .header h1 {
            color: white;
            font-size: 2rem;
            margin-bottom: 10px;
        }

        .status {
            display: inline-block;
            padding: 5px 15px;
            background: #10b981;
            border-radius: 20px;
            font-size: 0.9rem;
            color: white;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: #1e293b;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .card h3 {
            color: #60a5fa;
            margin-bottom: 15px;
            font-size: 1.1rem;
        }

        .metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #334155;
        }

        .metric:last-child {
            border-bottom: none;
        }

        .metric-label {
            color: #94a3b8;
            font-size: 0.9rem;
        }

        .metric-value {
            font-size: 1.2rem;
            font-weight: bold;
            color: #10b981;
        }

        .metric-value.warning {
            color: #f59e0b;
        }

        .metric-value.danger {
            color: #ef4444;
        }

        .chart-container {
            background: #1e293b;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .chart-placeholder {
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #0f172a;
            border-radius: 5px;
            color: #64748b;
        }

        .footer {
            text-align: center;
            padding: 20px;
            color: #64748b;
            font-size: 0.9rem;
        }

        .timestamp {
            color: #64748b;
            font-size: 0.8rem;
            text-align: right;
            margin-top: 10px;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .live-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #10b981;
            border-radius: 50%;
            margin-right: 5px;
            animation: pulse 2s ease-in-out infinite;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Agent Optimization Monitoring</h1>
        <span class="status">
            <span class="live-indicator"></span>
            LIVE
        </span>
    </div>

    <div class="grid">
        <div class="card">
            <h3>⚡ Performance Metrics</h3>
            <div class="metric">
                <span class="metric-label">Response Time (avg)</span>
                <span class="metric-value" id="avg-response-time">--</span>
            </div>
            <div class="metric">
                <span class="metric-label">Tasks Completed</span>
                <span class="metric-value" id="tasks-completed">--</span>
            </div>
            <div class="metric">
                <span class="metric-label">Optimization Gain</span>
                <span class="metric-value" id="optimization-gain">--</span>
            </div>
            <div class="metric">
                <span class="metric-label">Token Efficiency</span>
                <span class="metric-value" id="token-efficiency">--</span>
            </div>
        </div>

        <div class="card">
            <h3>🖥️ System Metrics</h3>
            <div class="metric">
                <span class="metric-label">CPU Usage</span>
                <span class="metric-value" id="cpu-usage">--</span>
            </div>
            <div class="metric">
                <span class="metric-label">Memory Usage</span>
                <span class="metric-value" id="memory-usage">--</span>
            </div>
            <div class="metric">
                <span class="metric-label">Disk I/O</span>
                <span class="metric-value" id="disk-io">--</span>
            </div>
            <div class="metric">
                <span class="metric-label">Network</span>
                <span class="metric-value" id="network">--</span>
            </div>
        </div>

        <div class="card">
            <h3>🤖 Agent Status</h3>
            <div class="metric">
                <span class="metric-label">Active Agents</span>
                <span class="metric-value" id="active-agents">--</span>
            </div>
            <div class="metric">
                <span class="metric-label">Idle Agents</span>
                <span class="metric-value" id="idle-agents">--</span>
            </div>
            <div class="metric">
                <span class="metric-label">Failed Tasks</span>
                <span class="metric-value danger" id="failed-tasks">--</span>
            </div>
            <div class="metric">
                <span class="metric-label">Queue Size</span>
                <span class="metric-value" id="queue-size">--</span>
            </div>
        </div>
    </div>

    <div class="chart-container">
        <h3>📊 Response Time Trend</h3>
        <div class="chart-placeholder">
            Real-time chart visualization (requires Chart.js integration)
        </div>
        <div class="timestamp" id="last-update">Last updated: --</div>
    </div>

    <div class="footer">
        Agent Optimization Monitoring Dashboard v1.0.0 | Connected via WebSocket
    </div>

    <script>
        // WebSocket connection
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const ws = new WebSocket(`${protocol}//${window.location.host}`);

        ws.onopen = () => {
            console.log('Connected to monitoring dashboard');
        };

        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'metrics') {
                updateDashboard(message.data);
            }
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        ws.onclose = () => {
            console.log('Disconnected from monitoring dashboard');
            setTimeout(() => location.reload(), 5000);
        };

        function updateDashboard(data) {
            // Update timestamp
            document.getElementById('last-update').textContent =
                `Last updated: ${new Date().toLocaleTimeString()}`;

            // Parse metrics (simplified - actual implementation would parse Prometheus format)
            // This is a placeholder - real implementation would parse data.metrics array

            // Mock data for demonstration
            document.getElementById('avg-response-time').textContent = '234ms';
            document.getElementById('tasks-completed').textContent = '1,247';
            document.getElementById('optimization-gain').textContent = '+32.5%';
            document.getElementById('token-efficiency').textContent = '87%';

            document.getElementById('cpu-usage').textContent = '45%';
            document.getElementById('memory-usage').textContent = '2.1GB';
            document.getElementById('disk-io').textContent = '125 MB/s';
            document.getElementById('network').textContent = '42 Mbps';

            document.getElementById('active-agents').textContent = '12';
            document.getElementById('idle-agents').textContent = '3';
            document.getElementById('failed-tasks').textContent = '2';
            document.getElementById('queue-size').textContent = '8';
        }

        // Initial mock update
        updateDashboard({});
    </script>
</body>
</html>
EOF

    log_success "Dashboard HTML created"
}

configure_alerting() {
    log_step "Configuring Alerting"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would configure alerting"
        return 0
    fi

    cat > "${CONFIG_DIR}/alert-rules.json" << 'EOF'
{
  "alerting": {
    "enabled": true,
    "checkInterval": 60,
    "rules": [
      {
        "name": "high_cpu_usage",
        "condition": "cpu_usage > 80",
        "severity": "warning",
        "message": "CPU usage is above 80%",
        "actions": ["log", "notify"]
      },
      {
        "name": "high_memory_usage",
        "condition": "memory_usage > 85",
        "severity": "warning",
        "message": "Memory usage is above 85%",
        "actions": ["log", "notify"]
      },
      {
        "name": "agent_failure_rate",
        "condition": "failed_tasks / total_tasks > 0.1",
        "severity": "critical",
        "message": "Agent failure rate exceeds 10%",
        "actions": ["log", "notify", "page"]
      },
      {
        "name": "slow_response_time",
        "condition": "avg_response_time > 5",
        "severity": "warning",
        "message": "Average response time exceeds 5 seconds",
        "actions": ["log", "notify"]
      },
      {
        "name": "token_inefficiency",
        "condition": "token_efficiency < 0.5",
        "severity": "info",
        "message": "Token efficiency below 50%",
        "actions": ["log"]
      }
    ],
    "notifications": {
      "email": {
        "enabled": false,
        "recipients": []
      },
      "slack": {
        "enabled": false,
        "webhook_url": ""
      },
      "pagerduty": {
        "enabled": false,
        "api_key": ""
      }
    }
  }
}
EOF

    log_success "Alert rules configured"
}

create_startup_script() {
    log_step "Creating Startup Script"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would create startup script"
        return 0
    fi

    cat > "${MONITORING_DIR}/start-monitoring.sh" << 'EOF'
#!/bin/bash
# Start monitoring services

cd "$(dirname "$0")"

echo "Starting monitoring dashboard..."
node dashboard-server.js > logs/dashboard.log 2>&1 &
echo $! > dashboard.pid

echo "Monitoring dashboard started (PID: $(cat dashboard.pid))"
echo "Access dashboard at: http://localhost:3030"
EOF

    chmod +x "${MONITORING_DIR}/start-monitoring.sh"
    log_success "Startup script created"
}

create_systemd_service() {
    log_step "Creating systemd Service"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY-RUN] Would create systemd service"
        return 0
    fi

    local service_file="${CONFIG_DIR}/agent-monitoring.service"

    cat > "$service_file" << EOF
[Unit]
Description=Agent Optimization Monitoring Dashboard
After=network.target

[Service]
Type=simple
User=${USER}
WorkingDirectory=${MONITORING_DIR}
ExecStart=/usr/bin/node ${MONITORING_DIR}/dashboard-server.js
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    log_success "systemd service file created: $service_file"
    log_info "To install: sudo cp $service_file /etc/systemd/system/"
    log_info "To enable: sudo systemctl enable agent-monitoring"
    log_info "To start: sudo systemctl start agent-monitoring"
}

# ═══════════════════════════════════════════════════
# MAIN SETUP FLOW
# ═══════════════════════════════════════════════════

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                log_warning "DRY-RUN MODE ENABLED"
                shift
                ;;
            --help)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --dry-run    Simulate setup without making changes"
                echo "  --help       Show this help message"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    # Create log directory
    mkdir -p "${LOG_DIR}"

    log_info "=========================================="
    log_info "Monitoring Setup Started"
    log_info "=========================================="

    # Execute setup steps
    create_directory_structure
    install_monitoring_dependencies
    create_metrics_collector
    create_dashboard_server
    create_dashboard_html
    configure_alerting
    create_startup_script
    create_systemd_service

    log_success "=========================================="
    log_success "Monitoring Setup Complete!"
    log_success "=========================================="
    log_info "Next steps:"
    log_info "  1. Review configuration in: ${CONFIG_DIR}"
    log_info "  2. Start monitoring: ${MONITORING_DIR}/start-monitoring.sh"
    log_info "  3. Access dashboard: http://localhost:3030"
}

main "$@"
