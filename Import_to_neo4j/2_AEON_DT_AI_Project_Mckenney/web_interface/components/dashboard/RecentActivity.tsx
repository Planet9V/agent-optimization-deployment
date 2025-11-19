import { Upload, Edit, Trash2, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

interface Activity {
  id: string;
  type: 'upload' | 'edit' | 'delete' | 'processed' | 'error';
  title: string;
  description: string;
  timestamp: Date;
  user?: string;
}

interface RecentActivityProps {
  activities?: Activity[];
  maxItems?: number;
  loading?: boolean;
}

const activityConfig = {
  upload: { icon: Upload, color: 'var(--primary)', bgColor: 'var(--primary-50)', label: 'Upload' },
  edit: { icon: Edit, color: 'var(--success-500)', bgColor: 'var(--success-50)', label: 'Edit' },
  delete: { icon: Trash2, color: 'var(--error-500)', bgColor: 'var(--error-50)', label: 'Delete' },
  processed: { icon: CheckCircle, color: 'var(--success-500)', bgColor: 'var(--success-50)', label: 'Processed' },
  error: { icon: AlertCircle, color: 'var(--error-500)', bgColor: 'var(--error-50)', label: 'Error' }
};

export default function RecentActivity({
  activities = [],
  maxItems = 10,
  loading = false
}: RecentActivityProps) {
  if (loading) {
    return (
      <div className="card-modern p-6">
        <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
          Recent Activity
        </h3>
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="flex items-start space-x-3">
              <div className="skeleton h-10 w-10 rounded-full"></div>
              <div className="flex-1 space-y-2">
                <div className="skeleton h-4 rounded w-3/4"></div>
                <div className="skeleton h-3 rounded w-1/2"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  const displayActivities = activities.slice(0, maxItems);

  return (
    <div className="card-modern p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold" style={{ color: 'var(--text-primary)' }}>
          Recent Activity
        </h3>
        <span
          className="px-2 py-1 rounded text-xs font-medium"
          style={{
            backgroundColor: 'var(--slate-100)',
            color: 'var(--text-secondary)'
          }}
        >
          {activities.length} total
        </span>
      </div>

      {displayActivities.length === 0 ? (
        <div className="text-center py-8">
          <FileText className="h-12 w-12 mx-auto mb-2" style={{ color: 'var(--text-tertiary)' }} />
          <p style={{ color: 'var(--text-secondary)' }}>No recent activity</p>
        </div>
      ) : (
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {displayActivities.map((activity) => {
            const config = activityConfig[activity.type];
            const Icon = config.icon;

            return (
              <div
                key={activity.id}
                className="flex items-start space-x-3 pb-4"
                style={{ borderBottom: '1px solid var(--border-subtle)' }}
              >
                <div
                  className="p-2 rounded-full flex-shrink-0"
                  style={{ backgroundColor: config.bgColor }}
                >
                  <Icon className="h-5 w-5" style={{ color: config.color }} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="font-medium" style={{ color: 'var(--text-primary)' }}>
                        {activity.title}
                      </p>
                      <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>
                        {activity.description}
                      </p>
                    </div>
                    <span
                      className="px-2 py-1 rounded text-xs font-semibold ml-2"
                      style={{
                        backgroundColor: config.bgColor,
                        color: config.color
                      }}
                    >
                      {config.label}
                    </span>
                  </div>
                  <div className="flex items-center mt-2">
                    <span className="text-xs" style={{ color: 'var(--text-tertiary)' }}>
                      {formatDistanceToNow(activity.timestamp, { addSuffix: true })}
                    </span>
                    {activity.user && (
                      <>
                        <span className="text-xs mx-2" style={{ color: 'var(--text-tertiary)' }}>•</span>
                        <span className="text-xs" style={{ color: 'var(--text-tertiary)' }}>
                          {activity.user}
                        </span>
                      </>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
