import { Upload, Search, MessageSquare, FileText, Database, Settings, Activity } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface QuickAction {
  title: string;
  description: string;
  icon: React.ReactNode;
  href: string;
  color: string;
}

export default function QuickActions() {
  const router = useRouter();

  const actions: QuickAction[] = [
    {
      title: 'Upload Documents',
      description: 'Import and process new documents',
      icon: <Upload className="h-6 w-6" />,
      href: '/upload',
      color: 'var(--primary)'
    },
    {
      title: 'Search Knowledge',
      description: 'Search across all documents',
      icon: <Search className="h-6 w-6" />,
      href: '/search',
      color: 'var(--success-500)'
    },
    {
      title: 'AI Assistant',
      description: 'Chat with AI about your data',
      icon: <MessageSquare className="h-6 w-6" />,
      href: '/chat',
      color: 'var(--severity-medium)'
    },
    {
      title: 'Observability',
      description: 'Real-time system monitoring',
      icon: <Activity className="h-6 w-6" />,
      href: '/observability',
      color: 'var(--info-500)'
    },
    {
      title: 'Manage Tags',
      description: 'Organize document tags',
      icon: <FileText className="h-6 w-6" />,
      href: '/tags',
      color: 'var(--warning-500)'
    },
    {
      title: 'View Database',
      description: 'Explore knowledge graph',
      icon: <Database className="h-6 w-6" />,
      href: '/graph',
      color: 'var(--severity-high)'
    },
    {
      title: 'Settings',
      description: 'Configure system settings',
      icon: <Settings className="h-6 w-6" />,
      href: '/settings',
      color: 'var(--slate-600)'
    }
  ];

  return (
    <div className="card-modern p-6">
      <h3 className="text-lg font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>
        Quick Actions
      </h3>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {actions.map((action) => (
          <button
            key={action.title}
            onClick={() => router.push(action.href)}
            className="flex flex-col items-start p-4 rounded-lg transition-all duration-200 text-left"
            style={{
              border: '1px solid var(--border-default)',
              backgroundColor: 'var(--surface)'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = 'var(--primary)';
              e.currentTarget.style.boxShadow = 'var(--shadow-md)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = 'var(--border-default)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <div
              className="p-2 rounded-lg mb-3"
              style={{ backgroundColor: action.color }}
            >
              <div className="text-white">{action.icon}</div>
            </div>
            <span className="font-semibold" style={{ color: 'var(--text-primary)' }}>
              {action.title}
            </span>
            <span className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>
              {action.description}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
