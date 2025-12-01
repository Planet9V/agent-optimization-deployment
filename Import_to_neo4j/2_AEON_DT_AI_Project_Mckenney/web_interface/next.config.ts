import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  poweredByHeader: false,
  compress: true,

  // Increase timeout for complex pages
  staticPageGenerationTimeout: 120,

  // Webpack configuration to handle browser-only libraries
  webpack: (config, { isServer }) => {
    if (isServer) {
      // Don't bundle vis-network and other browser-only libs on server
      config.externals = [...(config.externals || []), 'vis-network', 'vis-data'];
    }
    // Polyfill for browser APIs during build
    config.resolve = config.resolve || {};
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
      net: false,
      tls: false,
    };
    return config;
  },

  // Environment variables exposed to browser
  env: {
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME || 'AEON UI',
  },

  // Image optimization
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
      },
      {
        protocol: 'http',
        hostname: 'openspg-minio',
      },
    ],
  },

  // Experimental features
  experimental: {
    serverActions: {
      allowedOrigins: ['localhost:3000', 'aeon-ui:3000'],
    },
    instrumentationHook: true,
  },
};

export default nextConfig;
