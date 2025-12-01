'use client';

import { useState } from 'react';
import { Copy, Check, ExternalLink } from 'lucide-react';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Array<{
    source: 'neo4j' | 'qdrant' | 'internet';
    content: string;
    metadata?: Record<string, any>;
  }>;
  timestamp: Date;
}

interface ChatMessageProps {
  message: Message;
  onAction?: (action: string, data: any) => void;
}

export function ChatMessage({ message, onAction }: ChatMessageProps) {
  const [copied, setCopied] = useState(false);
  const [showSources, setShowSources] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getSourceIcon = (source: string) => {
    switch (source) {
      case 'neo4j':
        return '🔗';
      case 'qdrant':
        return '🔍';
      case 'internet':
        return '🌐';
      default:
        return '📄';
    }
  };

  const getSourceColor = (source: string) => {
    switch (source) {
      case 'neo4j':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'qdrant':
        return 'bg-purple-100 text-purple-800 border-purple-300';
      case 'internet':
        return 'bg-green-100 text-green-800 border-green-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  return (
    <div
      className={`flex gap-3 p-4 rounded-lg ${
        message.role === 'user'
          ? 'bg-blue-50 border border-blue-200'
          : 'bg-white border border-gray-200'
      }`}
    >
      <div className="flex-shrink-0">
        <div
          className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
            message.role === 'user'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-600 text-white'
          }`}
        >
          {message.role === 'user' ? 'U' : 'AI'}
        </div>
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <span className="text-sm font-semibold text-gray-900">
            {message.role === 'user' ? 'You' : 'AI Assistant'}
          </span>
          <span className="text-xs text-gray-500">
            {message.timestamp.toLocaleTimeString()}
          </span>
        </div>

        <div className="prose prose-sm max-w-none text-gray-800">
          {message.content}
        </div>

        {message.role === 'assistant' && message.sources && message.sources.length > 0 && (
          <div className="mt-3 space-y-2">
            <button
              onClick={() => setShowSources(!showSources)}
              className="text-xs text-blue-600 hover:text-blue-800 font-medium"
            >
              {showSources ? '▼' : '▶'} {message.sources.length} sources
            </button>

            {showSources && (
              <div className="space-y-2 pl-4 border-l-2 border-gray-200">
                {message.sources.map((source, idx) => (
                  <div
                    key={idx}
                    className={`text-xs p-2 rounded border ${getSourceColor(source.source)}`}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <span>{getSourceIcon(source.source)}</span>
                      <span className="font-semibold uppercase">{source.source}</span>
                      {source.metadata?.url && (
                        <a
                          href={source.metadata.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="ml-auto"
                        >
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                    </div>
                    <div className="text-xs opacity-80 line-clamp-2">
                      {source.content.substring(0, 150)}
                      {source.content.length > 150 ? '...' : ''}
                    </div>
                    {source.metadata?.document && (
                      <div className="text-xs opacity-60 mt-1">
                        📄 {source.metadata.document}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {message.role === 'assistant' && (
          <div className="flex items-center gap-2 mt-3">
            <button
              onClick={handleCopy}
              className="text-xs text-gray-600 hover:text-gray-800 flex items-center gap-1 px-2 py-1 rounded hover:bg-gray-100"
            >
              {copied ? (
                <>
                  <Check className="w-3 h-3" /> Copied
                </>
              ) : (
                <>
                  <Copy className="w-3 h-3" /> Copy
                </>
              )}
            </button>

            <button
              onClick={() => onAction?.('regenerate', { messageId: message.id })}
              className="text-xs text-gray-600 hover:text-gray-800 px-2 py-1 rounded hover:bg-gray-100"
            >
              🔄 Regenerate
            </button>

            <button
              onClick={() => onAction?.('export', { message })}
              className="text-xs text-gray-600 hover:text-gray-800 px-2 py-1 rounded hover:bg-gray-100"
            >
              📤 Export
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
