import React from 'react';
import { Shield, AlertTriangle, AlertCircle, Info } from 'lucide-react';

export type SeverityLevel = 'critical' | 'high' | 'medium' | 'low' | 'info';

interface SeverityBadgeProps {
  severity: SeverityLevel;
  score?: number;
  className?: string;
  showIcon?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

const severityConfig = {
  critical: {
    label: 'CRITICAL',
    icon: AlertTriangle,
    className: 'badge-critical',
    textColor: 'text-red-700',
    bgColor: 'bg-red-50',
    borderColor: 'border-red-200',
  },
  high: {
    label: 'HIGH',
    icon: AlertCircle,
    className: 'badge-high',
    textColor: 'text-orange-700',
    bgColor: 'bg-orange-50',
    borderColor: 'border-orange-200',
  },
  medium: {
    label: 'MEDIUM',
    icon: Shield,
    className: 'badge-medium',
    textColor: 'text-yellow-700',
    bgColor: 'bg-yellow-50',
    borderColor: 'border-yellow-200',
  },
  low: {
    label: 'LOW',
    icon: Info,
    className: 'badge-low',
    textColor: 'text-green-700',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200',
  },
  info: {
    label: 'INFO',
    icon: Info,
    className: 'badge-info',
    textColor: 'text-blue-700',
    bgColor: 'bg-blue-50',
    borderColor: 'border-blue-200',
  },
};

const sizeClasses = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-3 py-1 text-sm',
  lg: 'px-4 py-1.5 text-base',
};

export default function SeverityBadge({
  severity,
  score,
  className = '',
  showIcon = true,
  size = 'md',
}: SeverityBadgeProps) {
  const config = severityConfig[severity];
  const Icon = config.icon;

  return (
    <span
      className={`
        inline-flex items-center gap-1.5 font-semibold rounded-md border
        ${config.className}
        ${sizeClasses[size]}
        ${className}
      `}
      title={score !== undefined ? `CVSS Score: ${score}` : undefined}
    >
      {showIcon && <Icon className={size === 'sm' ? 'h-3 w-3' : size === 'lg' ? 'h-5 w-5' : 'h-4 w-4'} />}
      <span>{config.label}</span>
      {score !== undefined && (
        <span className="ml-1 opacity-75">
          {score.toFixed(1)}
        </span>
      )}
    </span>
  );
}

// Helper function to determine severity from CVSS score
export function getCVSSSeverity(score: number): SeverityLevel {
  if (score >= 9.0) return 'critical';
  if (score >= 7.0) return 'high';
  if (score >= 4.0) return 'medium';
  return 'low';
}
