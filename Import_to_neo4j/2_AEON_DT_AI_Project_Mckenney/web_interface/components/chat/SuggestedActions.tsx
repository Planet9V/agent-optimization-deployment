'use client';

import { Sparkles, FileText, Tags, BarChart3, Clock } from 'lucide-react';

interface SuggestedAction {
  id: string;
  label: string;
  icon: React.ReactNode;
  prompt: string;
  category: 'analysis' | 'generation' | 'search';
}

interface SuggestedActionsProps {
  onActionClick: (prompt: string) => void;
  recentQueries?: string[];
  context?: {
    customer?: string;
    scope?: string;
  };
}

export function SuggestedActions({ onActionClick, recentQueries = [], context }: SuggestedActionsProps) {
  const defaultActions: SuggestedAction[] = [
    {
      id: 'summarize',
      label: 'Summarize Project',
      icon: <FileText className="w-4 h-4" />,
      prompt: context?.customer
        ? `Provide a comprehensive summary of all projects for ${context.customer}`
        : 'Summarize the current project status',
      category: 'analysis'
    },
    {
      id: 'generate-tags',
      label: 'Generate Tags',
      icon: <Tags className="w-4 h-4" />,
      prompt: 'Analyze documents and generate relevant tags for organization',
      category: 'generation'
    },
    {
      id: 'analytics',
      label: 'Project Analytics',
      icon: <BarChart3 className="w-4 h-4" />,
      prompt: 'Show me analytics and metrics for the current project',
      category: 'analysis'
    },
    {
      id: 'recent-activity',
      label: 'Recent Activity',
      icon: <Clock className="w-4 h-4" />,
      prompt: 'What recent activities or changes have occurred in this project?',
      category: 'search'
    }
  ];

  const contextualActions: SuggestedAction[] = [];

  if (context?.customer) {
    contextualActions.push({
      id: 'customer-projects',
      label: `${context.customer} Projects`,
      icon: <Sparkles className="w-4 h-4" />,
      prompt: `List all projects for ${context.customer} with their current status`,
      category: 'search'
    });
  }

  if (context?.scope) {
    contextualActions.push({
      id: 'scope-analysis',
      label: `Analyze ${context.scope}`,
      icon: <BarChart3 className="w-4 h-4" />,
      prompt: `Provide detailed analysis of ${context.scope} scope`,
      category: 'analysis'
    });
  }

  const allActions = [...contextualActions, ...defaultActions];

  return (
    <div className="space-y-4">
      {/* Quick Actions */}
      <div>
        <h3 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-blue-600" />
          Suggested Actions
        </h3>
        <div className="grid grid-cols-2 gap-2">
          {allActions.slice(0, 6).map((action) => (
            <button
              key={action.id}
              onClick={() => onActionClick(action.prompt)}
              className="flex items-center gap-2 p-3 text-left text-sm bg-white border border-gray-200 rounded-lg hover:bg-blue-50 hover:border-blue-300 transition-colors"
            >
              <span className="text-blue-600">{action.icon}</span>
              <span className="text-gray-800 font-medium">{action.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Recent Queries */}
      {recentQueries.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
            <Clock className="w-4 h-4 text-gray-600" />
            Recent Queries
          </h3>
          <div className="space-y-1">
            {recentQueries.slice(0, 5).map((query, idx) => (
              <button
                key={idx}
                onClick={() => onActionClick(query)}
                className="block w-full text-left text-sm p-2 bg-gray-50 rounded hover:bg-gray-100 text-gray-700 truncate"
              >
                {query}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Quick Commands */}
      <div>
        <h3 className="text-sm font-semibold text-gray-700 mb-2">Quick Commands</h3>
        <div className="space-y-1 text-xs text-gray-600">
          <div className="flex items-start gap-2">
            <kbd className="px-1.5 py-0.5 bg-gray-200 rounded font-mono">@customer</kbd>
            <span>Search specific customer</span>
          </div>
          <div className="flex items-start gap-2">
            <kbd className="px-1.5 py-0.5 bg-gray-200 rounded font-mono">@project</kbd>
            <span>Reference project</span>
          </div>
          <div className="flex items-start gap-2">
            <kbd className="px-1.5 py-0.5 bg-gray-200 rounded font-mono">@doc</kbd>
            <span>Find document</span>
          </div>
        </div>
      </div>

      {/* Context Display */}
      {(context?.customer || context?.scope) && (
        <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="text-xs font-semibold text-blue-900 mb-1">Current Context</div>
          <div className="space-y-1 text-xs text-blue-800">
            {context.customer && (
              <div>
                <span className="font-medium">Customer:</span> {context.customer}
              </div>
            )}
            {context.scope && (
              <div>
                <span className="font-medium">Scope:</span> {context.scope}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
