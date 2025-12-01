# AEON UI - Next.js Production Dockerfile
# Multi-stage build for optimized production image

# Stage 1: Dependencies
FROM node:20-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copy package files
# Note: Using npm install instead of npm ci due to React 19 peer dependency conflicts with @tremor/react
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps --production

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app

# Copy package files and install all dependencies (including dev dependencies for build)
# Using --legacy-peer-deps to handle React 19 compatibility issues
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps

COPY . .

# Set dummy API key for build (will be overridden at runtime)
ENV OPENAI_API_KEY="sk-dummy-key-for-build"

# Build Next.js application
RUN npm run build

# Stage 3: Runner (Production)
FROM node:20-alpine AS runner
WORKDIR /app

# Set environment
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy necessary files from builder
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Create logs directory
RUN mkdir -p /app/logs && chown -R nextjs:nodejs /app/logs

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://$(hostname):3000/api/health || exit 1

# Start application
CMD ["node", "server.js"]
