import { Database, Server, HardDrive, Activity, CheckCircle, AlertTriangle, XCircle } from 'lucide-react';

interface ServiceStatus {
  name: string;
  status: 'healthy' | 'degraded' | 'down';
  responseTime?: number;
  uptime?: string;
  icon: React.ReactNode;
}

interface SystemHealthProps {
  services?: ServiceStatus[];
  loading?: boolean;
  onRefresh?: () => void;
}

const statusConfig = {
  healthy: {
    color: 'var(--success-500)',
    bgColor: 'var(--success-50)',
    icon: CheckCircle,
    label: 'Healthy'
  },
  degraded: {
    color: 'var(--warning-500)',
    bgColor: 'var(--warning-50)',
    icon: AlertTriangle,
    label: 'Degraded'
  },
  down: {
    color: 'var(--error-500)',
    bgColor: 'var(--error-50)',
    icon: XCircle,
    label: 'Down'
  }
};

export default function SystemHealth({
  services = [],
  loading = false,
  onRefresh
}: SystemHealthProps) {
  const defaultServices: ServiceStatus[] = [
    { name: 'Neo4j', status: 'healthy', responseTime: 45, uptime: '99.9%', icon: <Database className="h-5 w-5" /> },
    { name: 'Qdrant', status: 'healthy', responseTime: 32, uptime: '99.8%', icon: <Server className="h-5 w-5" /> },
    { name: 'MySQL', status: 'healthy', responseTime: 28, uptime: '99.9%', icon: <Database className="h-5 w-5" /> },
    { name: 'MinIO', status: 'healthy', responseTime: 55, uptime: '99.7%', icon: <HardDrive className="h-5 w-5" /> }
  ];

  const displayServices = services.length > 0 ? services : defaultServices;
  const overallStatus = displayServices.every(s => s.status === 'healthy')
    ? 'healthy'
    : displayServices.some(s => s.status === 'down')
    ? 'down'
    : 'degraded';

  if (loading) {
    return (
      <div className="card-modern p-6">
        <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
          System Health
        </h3>
        <div className="space-y-3">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="flex items-center space-x-3">
              <div className="skeleton h-10 w-10 rounded-lg"></div>
              <div className="flex-1 space-y-2">
                <div className="skeleton h-4 rounded w-1/2"></div>
                <div className="skeleton h-3 rounded w-1/3"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  const StatusIcon = statusConfig[overallStatus].icon;

  return (
    <div className="card-modern p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold" style={{ color: 'var(--text-primary)' }}>
          System Health
        </h3>
        <div className="flex items-center space-x-2">
          <span
            className="px-3 py-1 rounded-full text-xs font-semibold flex items-center space-x-1"
            style={{
              backgroundColor: statusConfig[overallStatus].bgColor,
              color: statusConfig[overallStatus].color
            }}
          >
            <StatusIcon className="h-3 w-3" />
            <span>{statusConfig[overallStatus].label}</span>
          </span>
          {onRefresh && (
            <button
              onClick={onRefresh}
              className="p-1 rounded transition-colors"
              style={{
                backgroundColor: 'var(--slate-100)',
                color: 'var(--text-secondary)'
              }}
              aria-label="Refresh status"
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = 'var(--slate-200)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'var(--slate-100)';
              }}
            >
              <Activity className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>

      <div className="space-y-3">
        {displayServices.map((service) => {
          const config = statusConfig[service.status];
          const Icon = config.icon;

          return (
            <div
              key={service.name}
              className="flex items-center justify-between p-3 rounded-lg transition-shadow"
              style={{
                border: '1px solid var(--border-default)',
                backgroundColor: 'var(--surface)'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.boxShadow = 'var(--shadow-sm)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              <div className="flex items-center space-x-3">
                <div
                  className="p-2 rounded-lg"
                  style={{ backgroundColor: config.bgColor }}
                >
                  {service.icon}
                </div>
                <div>
                  <p className="font-medium" style={{ color: 'var(--text-primary)' }}>
                    {service.name}
                  </p>
                  <div className="flex items-center space-x-3 mt-1">
                    {service.responseTime && (
                      <span className="text-xs" style={{ color: 'var(--text-secondary)' }}>
                        {service.responseTime}ms
                      </span>
                    )}
                    {service.uptime && (
                      <>
                        <span className="text-xs" style={{ color: 'var(--text-tertiary)' }}>•</span>
                        <span className="text-xs" style={{ color: 'var(--text-secondary)' }}>
                          {service.uptime} uptime
                        </span>
                      </>
                    )}
                  </div>
                </div>
              </div>
              <span
                className="px-2 py-1 rounded flex items-center space-x-1 text-xs font-semibold"
                style={{
                  backgroundColor: config.bgColor,
                  color: config.color
                }}
              >
                <Icon className="h-3 w-3" />
                <span>{config.label}</span>
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
