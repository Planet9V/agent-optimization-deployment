/**
 * Next.js Instrumentation Hook
 *
 * This file is automatically loaded by Next.js 13+ before any other code.
 * Perfect for environment validation at startup.
 *
 * Documentation: https://nextjs.org/docs/app/building-your-application/optimizing/instrumentation
 */

export async function register() {
  // Only run in Node.js runtime (not Edge runtime)
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    const { initializeApp } = await import('./lib/init');
    initializeApp();
  }
}
