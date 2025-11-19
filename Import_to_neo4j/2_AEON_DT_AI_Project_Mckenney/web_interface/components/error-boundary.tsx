'use client';

import React, { Component, ReactNode } from 'react';
import { AlertCircle, RefreshCcw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

interface Props {
  children: ReactNode;
  fallbackMessage?: string;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: undefined });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center p-4 bg-gray-50">
          <Card className="max-w-md w-full">
            <CardHeader>
              <div className="flex items-center gap-3">
                <AlertCircle className="h-8 w-8 text-red-500" />
                <div>
                  <CardTitle>Something went wrong</CardTitle>
                  <CardDescription>
                    {this.props.fallbackMessage || 'An unexpected error occurred'}
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {this.state.error && (
                <div className="p-3 bg-red-50 border border-red-200 rounded text-sm text-red-700">
                  <p className="font-medium mb-1">Error details:</p>
                  <p className="font-mono text-xs">{this.state.error.message}</p>
                </div>
              )}
              <Button onClick={this.handleReset} className="w-full">
                <RefreshCcw className="h-4 w-4 mr-2" />
                Reload Page
              </Button>
            </CardContent>
          </Card>
        </div>
      );
    }

    return this.props.children;
  }
}

interface DatabaseErrorProps {
  serviceName: string;
  onRetry?: () => void;
  showRetry?: boolean;
}

export function DatabaseConnectionError({ serviceName, onRetry, showRetry = true }: DatabaseErrorProps) {
  return (
    <div className="min-h-[60vh] flex items-center justify-center p-4">
      <Card className="max-w-lg w-full">
        <CardHeader>
          <div className="flex items-center gap-3">
            <AlertCircle className="h-8 w-8 text-yellow-500" />
            <div>
              <CardTitle>Database Connection Required</CardTitle>
              <CardDescription>
                Waiting for {serviceName} connection
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="p-4 bg-yellow-50 border border-yellow-200 rounded">
            <p className="text-sm text-yellow-800">
              This page requires an active connection to {serviceName}.
              Please ensure the database service is running and configured correctly.
            </p>
          </div>
          {showRetry && onRetry && (
            <Button onClick={onRetry} className="w-full">
              <RefreshCcw className="h-4 w-4 mr-2" />
              Retry Connection
            </Button>
          )}
          <div className="text-xs text-muted-foreground text-center">
            Check your environment configuration and database services
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
