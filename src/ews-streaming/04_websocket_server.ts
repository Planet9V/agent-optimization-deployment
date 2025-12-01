// =============================================================================
// GAP-ML-005: WebSocket EWS Streaming Server
// =============================================================================
// File: src/ews-streaming/04_websocket_server.ts
// Created: 2025-11-30
// Purpose: Real-time WebSocket server for EWS alert streaming
// Technology: Node.js + Express + Socket.io + Neo4j Driver
// =============================================================================

import express from 'express';
import { createServer } from 'http';
import { Server, Socket } from 'socket.io';
import neo4j, { Driver, Session } from 'neo4j-driver';
import jwt, { SignOptions } from 'jsonwebtoken';

// =============================================================================
// CONFIGURATION
// =============================================================================

const config = {
  port: process.env.EWS_PORT || 3001,
  neo4j: {
    uri: process.env.NEO4J_URI || 'bolt://aeon-neo4j-dev:7687',
    user: process.env.NEO4J_USER || 'neo4j',
    password: process.env.NEO4J_PASSWORD || 'neo4j@openspg'
  },
  jwt: {
    secret: process.env.JWT_SECRET || 'aeon-ews-secret-change-in-production',
    expiresIn: '24h' as const
  },
  polling: {
    interval: 5000,  // Check for new alerts every 5 seconds
    batchSize: 100   // Max alerts per batch
  }
};

// =============================================================================
// NEO4J CONNECTION
// =============================================================================

const driver: Driver = neo4j.driver(
  config.neo4j.uri,
  neo4j.auth.basic(config.neo4j.user, config.neo4j.password)
);

async function testNeo4jConnection(): Promise<boolean> {
  const session = driver.session();
  try {
    await session.run('RETURN 1');
    console.log('✅ Neo4j connection successful');
    return true;
  } catch (error) {
    console.error('❌ Neo4j connection failed:', error);
    return false;
  } finally {
    await session.close();
  }
}

// =============================================================================
// EXPRESS APP & HTTP SERVER
// =============================================================================

const app = express();
const httpServer = createServer(app);

app.use(express.json());

// Health check endpoint
app.get('/api/v1/ews/health', (req, res) => {
  res.json({
    status: 'online',
    timestamp: new Date().toISOString(),
    service: 'ews-streaming'
  });
});

// Status endpoint
app.get('/api/v1/ews/status', async (req, res) => {
  const session = driver.session();
  try {
    // Count active connections
    const connections = io.sockets.sockets.size;

    // Count alerts in last 24 hours
    const result = await session.run(`
      MATCH (ea:EWSAlert)
      WHERE ea.timestamp > datetime() - duration('P1D')
      RETURN count(ea) AS alerts_24h
    `);

    const alerts24h = result.records[0]?.get('alerts_24h').toNumber() || 0;

    res.json({
      streaming: true,
      connections,
      alerts_24h: alerts24h,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Status check error:', error);
    res.status(500).json({ error: 'Failed to get status' });
  } finally {
    await session.close();
  }
});

// Subscribe endpoint (returns WebSocket connection details)
app.post('/api/v1/ews/subscribe', (req, res) => {
  const { channels, filters } = req.body;

  // Generate JWT token for authentication
  const signOptions: SignOptions = { expiresIn: config.jwt.expiresIn };
  const token = jwt.sign(
    {
      channels: channels || ['ews:*'],
      filters: filters || {},
      subscribed_at: new Date().toISOString()
    },
    config.jwt.secret,
    signOptions
  );

  res.json({
    subscription_id: `SUB-${Date.now()}`,
    websocket_url: `ws://localhost:${config.port}/ews/stream`,
    auth_token: token,
    channels: channels || ['ews:*'],
    filters: filters || {},
    instructions: 'Connect to WebSocket URL with auth token in first message'
  });
});

// Alert history endpoint
app.get('/api/v1/ews/history', async (req, res) => {
  const session = driver.session();
  try {
    const {
      severity,
      entity_id,
      from_date,
      to_date,
      limit = 50,
      offset = 0
    } = req.query;

    let query = `
      MATCH (ea:EWSAlert)
      WHERE ea.timestamp IS NOT NULL
    `;

    const params: any = {
      limit: parseInt(limit as string),
      offset: parseInt(offset as string)
    };

    if (severity) {
      query += ` AND ea.severity = $severity`;
      params.severity = severity;
    }

    if (entity_id) {
      query += ` AND ea.entity_id = $entity_id`;
      params.entity_id = entity_id;
    }

    if (from_date) {
      query += ` AND ea.timestamp >= datetime($from_date)`;
      params.from_date = from_date;
    }

    if (to_date) {
      query += ` AND ea.timestamp <= datetime($to_date)`;
      params.to_date = to_date;
    }

    query += `
      RETURN ea.payload AS alert_json,
             ea.timestamp AS timestamp
      ORDER BY ea.timestamp DESC
      SKIP $offset
      LIMIT $limit
    `;

    const result = await session.run(query, params);

    const alerts = result.records.map(record => ({
      ...JSON.parse(record.get('alert_json')),
      db_timestamp: record.get('timestamp').toString()
    }));

    res.json({
      alerts,
      pagination: {
        limit: params.limit,
        offset: params.offset,
        total: alerts.length
      }
    });
  } catch (error) {
    console.error('History query error:', error);
    res.status(500).json({ error: 'Failed to retrieve alert history' });
  } finally {
    await session.close();
  }
});

// Publish endpoint (for Neo4j triggers to POST alerts)
app.post('/api/v1/ews/publish', (req, res) => {
  const alert = req.body;

  // Validate alert structure
  if (!alert.type || !alert.entity_id || !alert.severity) {
    return res.status(400).json({ error: 'Invalid alert format' });
  }

  // Broadcast to all connected clients
  io.emit('ews_alert', alert);

  console.log(`📡 Broadcasted alert: ${alert.entity_id} - ${alert.severity}`);

  res.json({ success: true, broadcasted: true });
});

// =============================================================================
// SOCKET.IO SERVER
// =============================================================================

const io = new Server(httpServer, {
  cors: {
    origin: '*',  // Configure properly in production
    methods: ['GET', 'POST']
  },
  path: '/ews/stream'
});

// Middleware: JWT authentication
io.use((socket, next) => {
  const token = socket.handshake.auth.token;

  if (!token) {
    return next(new Error('Authentication required'));
  }

  try {
    const decoded = jwt.verify(token, config.jwt.secret);
    (socket as any).user = decoded;
    next();
  } catch (error) {
    next(new Error('Invalid token'));
  }
});

// Connection handler
io.on('connection', (socket: Socket) => {
  const user = (socket as any).user;
  console.log(`✅ Client connected: ${socket.id}`, user);

  // Send welcome message
  socket.emit('connected', {
    message: 'Connected to EWS streaming service',
    channels: user.channels,
    filters: user.filters,
    timestamp: new Date().toISOString()
  });

  // Handle subscription updates
  socket.on('subscribe', (data) => {
    const { channels, filters } = data;
    (socket as any).user.channels = channels;
    (socket as any).user.filters = filters;

    socket.emit('subscribed', {
      channels,
      filters,
      timestamp: new Date().toISOString()
    });

    console.log(`📻 Client ${socket.id} updated subscription:`, channels);
  });

  // Handle disconnection
  socket.on('disconnect', () => {
    console.log(`❌ Client disconnected: ${socket.id}`);
  });

  // Error handling
  socket.on('error', (error) => {
    console.error(`Socket error for ${socket.id}:`, error);
  });
});

// =============================================================================
// ALERT POLLING FROM NEO4J
// =============================================================================

async function pollNewAlerts(): Promise<void> {
  const session = driver.session();
  try {
    // Get undelivered alerts
    const result = await session.run(`
      MATCH (ea:EWSAlert)
      WHERE ea.delivered = false
        AND ea.timestamp > datetime() - duration('PT1H')
      WITH ea
      ORDER BY ea.timestamp DESC
      LIMIT $batchSize
      SET ea.delivered = true
      RETURN ea.payload AS alert_json,
             ea.alert_id AS alert_id
    `, { batchSize: config.polling.batchSize });

    if (result.records.length > 0) {
      console.log(`📬 Polled ${result.records.length} new alerts from Neo4j`);

      for (const record of result.records) {
        const alert = JSON.parse(record.get('alert_json'));
        const alertId = record.get('alert_id');

        // Broadcast to all connected clients
        io.emit('ews_alert', {
          ...alert,
          alert_id: alertId,
          delivery_timestamp: new Date().toISOString()
        });
      }
    }
  } catch (error) {
    console.error('❌ Error polling alerts:', error);
  } finally {
    await session.close();
  }
}

// Start polling
let pollingInterval: NodeJS.Timeout;

function startPolling(): void {
  pollingInterval = setInterval(pollNewAlerts, config.polling.interval);
  console.log(`🔄 Started alert polling (every ${config.polling.interval}ms)`);
}

function stopPolling(): void {
  if (pollingInterval) {
    clearInterval(pollingInterval);
    console.log('⏹️  Stopped alert polling');
  }
}

// =============================================================================
// SERVER STARTUP
// =============================================================================

async function startServer(): Promise<void> {
  try {
    // Test Neo4j connection
    const neo4jOk = await testNeo4jConnection();
    if (!neo4jOk) {
      throw new Error('Neo4j connection failed');
    }

    // Start HTTP server
    httpServer.listen(config.port, () => {
      console.log(`🚀 EWS Streaming Server running on port ${config.port}`);
      console.log(`📡 WebSocket endpoint: ws://localhost:${config.port}/ews/stream`);
      console.log(`🔗 REST API: http://localhost:${config.port}/api/v1/ews`);
    });

    // Start alert polling
    startPolling();

    // Graceful shutdown
    process.on('SIGTERM', async () => {
      console.log('⏹️  SIGTERM received, shutting down gracefully...');
      stopPolling();
      await driver.close();
      httpServer.close(() => {
        console.log('✅ Server closed');
        process.exit(0);
      });
    });

  } catch (error) {
    console.error('❌ Failed to start server:', error);
    process.exit(1);
  }
}

// =============================================================================
// START SERVER
// =============================================================================

if (require.main === module) {
  startServer();
}

export { app, io, driver, startServer, stopPolling };
