import { LucideIcon } from 'lucide-react';

interface MetricsCardProps {
  title: string;
  metric: string | number;
  delta?: string;
  deltaType?: 'increase' | 'moderateIncrease' | 'decrease' | 'moderateDecrease' | 'unchanged';
  icon?: LucideIcon;
  iconColor?: string;
  loading?: boolean;
}

export default function MetricsCard({
  title,
  metric,
  delta,
  deltaType = 'unchanged',
  icon: Icon,
  iconColor = 'text-blue-500',
  loading = false
}: MetricsCardProps) {
  if (loading) {
    return (
      <div className="card-modern p-6">
        <div className="skeleton h-4 rounded w-1/2 mb-4"></div>
        <div className="skeleton h-8 rounded w-3/4"></div>
      </div>
    );
  }

  const getDeltaColor = () => {
    switch (deltaType) {
      case 'increase':
      case 'moderateIncrease':
        return 'var(--success-500)';
      case 'decrease':
      case 'moderateDecrease':
        return 'var(--error-500)';
      default:
        return 'var(--text-tertiary)';
    }
  };

  return (
    <div className="card-modern p-6">
      <div className="flex justify-between items-start">
        <div className="flex-1">
          <p className="text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
            {title}
          </p>
          <p className="text-3xl font-bold" style={{ color: 'var(--text-primary)' }}>
            {metric}
          </p>
        </div>
        {Icon && (
          <div
            className="p-3 rounded-lg"
            style={{ backgroundColor: 'var(--slate-100)' }}
          >
            <Icon className={`h-6 w-6 ${iconColor}`} />
          </div>
        )}
      </div>
      {delta && (
        <div className="mt-4">
          <span
            className="text-sm font-medium"
            style={{ color: getDeltaColor() }}
          >
            {delta}
          </span>
        </div>
      )}
    </div>
  );
}
