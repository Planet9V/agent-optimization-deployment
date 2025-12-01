#!/usr/bin/env node

/**
 * Queue Monitoring Script
 * Displays real-time status of the document processing queue
 */

const { Queue } = require('bullmq');
const { redisConfig } = require('../config/redis.config');

const QUEUE_NAME = 'document-processing';

const queue = new Queue(QUEUE_NAME, { connection: redisConfig });

async function displayStatus() {
  console.clear();
  console.log('╔═══════════════════════════════════════════════════════╗');
  console.log('║    Document Processing Queue - Live Monitor           ║');
  console.log('╚═══════════════════════════════════════════════════════╝');
  console.log('');

  try {
    const [waiting, active, completed, failed, delayed] = await Promise.all([
      queue.getWaitingCount(),
      queue.getActiveCount(),
      queue.getCompletedCount(),
      queue.getFailedCount(),
      queue.getDelayedCount(),
    ]);

    const total = waiting + active + completed + failed + delayed;

    console.log(`Total Jobs:      ${total}`);
    console.log(`├─ Waiting:      ${waiting}`);
    console.log(`├─ Active:       ${active} 🔄`);
    console.log(`├─ Completed:    ${completed} ✅`);
    console.log(`├─ Failed:       ${failed} ❌`);
    console.log(`└─ Delayed:      ${delayed} ⏰`);
    console.log('');

    // Show recent active jobs
    if (active > 0) {
      console.log('Active Jobs:');
      const activeJobs = await queue.getJobs(['active'], 0, 5);
      for (const job of activeJobs) {
        const progress = job.progress || 0;
        const progressBar = '█'.repeat(Math.floor(progress / 10)) + '░'.repeat(10 - Math.floor(progress / 10));
        console.log(`  • ${job.data.fileName} [${progressBar}] ${progress}%`);
      }
      console.log('');
    }

    // Show recent failures
    if (failed > 0) {
      console.log('Recent Failures:');
      const failedJobs = await queue.getJobs(['failed'], 0, 3);
      for (const job of failedJobs) {
        console.log(`  • ${job.data.fileName}: ${job.failedReason || 'Unknown error'}`);
      }
      console.log('');
    }

    console.log('Last updated:', new Date().toLocaleTimeString());
    console.log('Press Ctrl+C to exit');

  } catch (error) {
    console.error('Error fetching queue status:', error.message);
  }
}

// Update every 2 seconds
const interval = setInterval(displayStatus, 2000);

// Initial display
displayStatus();

// Graceful shutdown
process.on('SIGINT', async () => {
  clearInterval(interval);
  await queue.close();
  console.log('\n\n👋 Monitor stopped');
  process.exit(0);
});

process.on('SIGTERM', async () => {
  clearInterval(interval);
  await queue.close();
  process.exit(0);
});
