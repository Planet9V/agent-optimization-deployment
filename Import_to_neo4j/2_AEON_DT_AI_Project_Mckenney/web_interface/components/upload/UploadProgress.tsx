import { Card, Text, ProgressBar, Badge, Flex } from '@tremor/react';
import { Upload, CheckCircle, AlertCircle, Clock, FileText } from 'lucide-react';

interface UploadTask {
  id: string;
  fileName: string;
  status: 'queued' | 'uploading' | 'processing' | 'success' | 'error';
  progress: number;
  message?: string;
  startedAt?: Date;
  completedAt?: Date;
}

interface UploadProgressProps {
  tasks: UploadTask[];
  onCancel?: (taskId: string) => void;
  onRetry?: (taskId: string) => void;
  compact?: boolean;
}

const statusConfig = {
  queued: {
    icon: Clock,
    color: 'gray' as const,
    label: 'Queued',
    progressColor: 'gray' as const
  },
  uploading: {
    icon: Upload,
    color: 'blue' as const,
    label: 'Uploading',
    progressColor: 'blue' as const
  },
  processing: {
    icon: FileText,
    color: 'indigo' as const,
    label: 'Processing',
    progressColor: 'indigo' as const
  },
  success: {
    icon: CheckCircle,
    color: 'emerald' as const,
    label: 'Complete',
    progressColor: 'emerald' as const
  },
  error: {
    icon: AlertCircle,
    color: 'red' as const,
    label: 'Failed',
    progressColor: 'red' as const
  }
};

export default function UploadProgress({
  tasks,
  onCancel,
  onRetry,
  compact = false
}: UploadProgressProps) {
  if (tasks.length === 0) {
    return null;
  }

  const activeCount = tasks.filter(t =>
    t.status === 'uploading' || t.status === 'processing'
  ).length;
  const completedCount = tasks.filter(t => t.status === 'success').length;
  const errorCount = tasks.filter(t => t.status === 'error').length;
  const queuedCount = tasks.filter(t => t.status === 'queued').length;

  const overallProgress = tasks.length > 0
    ? Math.round(tasks.reduce((sum, task) => sum + task.progress, 0) / tasks.length)
    : 0;

  const getTimeDuration = (task: UploadTask): string => {
    if (!task.startedAt) return '';

    const end = task.completedAt || new Date();
    const seconds = Math.floor((end.getTime() - task.startedAt.getTime()) / 1000);

    if (seconds < 60) return `${seconds}s`;
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
  };

  return (
    <Card>
      <Flex justifyContent="between" alignItems="center" className="mb-4">
        <div>
          <Text className="text-lg font-semibold">Upload Progress</Text>
          <Text className="text-sm text-gray-500 mt-1">
            {tasks.length} total files
          </Text>
        </div>
        <Flex justifyContent="end" className="space-x-2">
          {queuedCount > 0 && (
            <Badge color="gray" icon={Clock}>
              {queuedCount} queued
            </Badge>
          )}
          {activeCount > 0 && (
            <Badge color="blue" icon={Upload}>
              {activeCount} active
            </Badge>
          )}
          {completedCount > 0 && (
            <Badge color="emerald" icon={CheckCircle}>
              {completedCount} done
            </Badge>
          )}
          {errorCount > 0 && (
            <Badge color="red" icon={AlertCircle}>
              {errorCount} failed
            </Badge>
          )}
        </Flex>
      </Flex>

      <div className="mb-6">
        <Flex justifyContent="between" className="mb-2">
          <Text className="text-sm font-medium">Overall Progress</Text>
          <Text className="text-sm font-medium">{overallProgress}%</Text>
        </Flex>
        <ProgressBar value={overallProgress} color="blue" />
      </div>

      <div className="space-y-3 max-h-96 overflow-y-auto">
        {tasks.map((task) => {
          const config = statusConfig[task.status];
          const Icon = config.icon;
          const duration = getTimeDuration(task);

          if (compact && task.status === 'success') {
            return null;
          }

          return (
            <div
              key={task.id}
              className="p-4 bg-gray-50 rounded-lg border border-gray-200"
            >
              <Flex justifyContent="between" alignItems="start" className="mb-2">
                <Flex justifyContent="start" className="space-x-2 flex-1 min-w-0">
                  <Icon className={`h-5 w-5 flex-shrink-0 text-${config.color}-600 ${
                    task.status === 'uploading' || task.status === 'processing'
                      ? 'animate-pulse'
                      : ''
                  }`} />
                  <div className="flex-1 min-w-0">
                    <Text className="font-medium truncate">{task.fileName}</Text>
                    {task.message && (
                      <Text className="text-sm text-gray-500 mt-1">
                        {task.message}
                      </Text>
                    )}
                  </div>
                </Flex>
                <Badge color={config.color} size="sm">
                  {config.label}
                </Badge>
              </Flex>

              {task.status !== 'queued' && (
                <>
                  <ProgressBar
                    value={task.progress}
                    color={config.progressColor}
                    className="mt-2"
                  />
                  <Flex justifyContent="between" className="mt-2">
                    <Text className="text-xs text-gray-500">
                      {task.progress}% complete
                    </Text>
                    {duration && (
                      <Text className="text-xs text-gray-500">
                        {duration}
                      </Text>
                    )}
                  </Flex>
                </>
              )}

              {task.status === 'error' && onRetry && (
                <button
                  onClick={() => onRetry(task.id)}
                  className="mt-2 text-sm text-blue-600 hover:text-blue-700 font-medium"
                >
                  Retry upload
                </button>
              )}

              {(task.status === 'uploading' || task.status === 'processing') && onCancel && (
                <button
                  onClick={() => onCancel(task.id)}
                  className="mt-2 text-sm text-red-600 hover:text-red-700 font-medium"
                >
                  Cancel
                </button>
              )}
            </div>
          );
        })}
      </div>
    </Card>
  );
}
