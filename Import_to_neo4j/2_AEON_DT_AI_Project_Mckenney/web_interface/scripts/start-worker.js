#!/usr/bin/env node

/**
 * Standalone BullMQ Worker Process
 * Used for distributed worker deployment
 */

const { getDocumentWorker, shutdownWorker } = require('../lib/queue/documentQueue');

console.log('Starting document processing worker...');
console.log('Configuration:');
console.log(`- Redis Host: ${process.env.REDIS_HOST || 'localhost'}`);
console.log(`- Redis Port: ${process.env.REDIS_PORT || '6379'}`);
console.log(`- Concurrency: 4 workers`);
console.log('');

const worker = getDocumentWorker();

// Graceful shutdown handlers
process.on('SIGINT', async () => {
  console.log('\nShutting down worker gracefully...');
  await shutdownWorker();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.log('\nShutting down worker gracefully...');
  await shutdownWorker();
  process.exit(0);
});

// Error handlers
process.on('uncaughtException', (error) => {
  console.error('Uncaught exception:', error);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

console.log('✅ Worker started successfully. Press Ctrl+C to stop.');
console.log('Waiting for jobs...\n');
