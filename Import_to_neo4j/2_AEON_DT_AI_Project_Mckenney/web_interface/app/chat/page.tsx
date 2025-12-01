'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Database, Search, Globe, Settings, Loader2, AlertCircle } from 'lucide-react';
import { ChatMessage, type Message } from '@/components/chat/ChatMessage';
import { SuggestedActions } from '@/components/chat/SuggestedActions';

interface DataSource {
  neo4j: boolean;
  qdrant: boolean;
  internet: boolean;
}

interface QueryContext {
  customer?: string;
  scope?: string;
  projectId?: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recentQueries, setRecentQueries] = useState<string[]>([]);

  const [dataSources, setDataSources] = useState<DataSource>({
    neo4j: true,
    qdrant: true,
    internet: false
  });

  const [context, setContext] = useState<QueryContext>({
    customer: 'McKenney',
    scope: 'All'
  });

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Load recent queries from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('recentQueries');
    if (saved) {
      setRecentQueries(JSON.parse(saved));
    }
  }, []);

  const saveRecentQuery = (query: string) => {
    const updated = [query, ...recentQueries.filter(q => q !== query)].slice(0, 10);
    setRecentQueries(updated);
    localStorage.setItem('recentQueries', JSON.stringify(updated));
  };

  const handleSendMessage = async (messageContent?: string) => {
    const content = messageContent || input.trim();
    if (!content || isLoading) return;

    setError(null);
    setInput('');

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    saveRecentQuery(content);
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [...messages, userMessage].map(m => ({
            role: m.role,
            content: m.content
          })),
          dataSources,
          context
        })
      });

      if (!response.ok) {
        throw new Error(`Request failed: ${response.statusText}`);
      }

      // Process streaming response
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '',
        sources: [],
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split('\n\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6);

              if (data === '[DONE]') {
                continue;
              }

              try {
                const parsed = JSON.parse(data);

                if (parsed.type === 'sources') {
                  assistantMessage.sources = parsed.sources;
                  setMessages(prev => {
                    const updated = [...prev];
                    updated[updated.length - 1] = { ...assistantMessage };
                    return updated;
                  });
                } else if (parsed.type === 'text') {
                  assistantMessage.content += parsed.content;
                  setMessages(prev => {
                    const updated = [...prev];
                    updated[updated.length - 1] = { ...assistantMessage };
                    return updated;
                  });
                }
              } catch (e) {
                // Skip invalid JSON
              }
            }
          }
        }
      }

    } catch (err: any) {
      console.error('Chat error:', err);
      setError(err.message || 'Failed to get response');

      // Remove the incomplete assistant message
      setMessages(prev => prev.filter(m => m.role !== 'assistant' || m.content));
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleAction = (action: string, data: any) => {
    if (action === 'regenerate') {
      const lastUserMessage = messages.filter(m => m.role === 'user').pop();
      if (lastUserMessage) {
        // Remove last assistant message
        setMessages(prev => prev.slice(0, -1));
        handleSendMessage(lastUserMessage.content);
      }
    } else if (action === 'export') {
      const content = `# Chat Export\n\n${messages
        .map(m => `**${m.role.toUpperCase()}**: ${m.content}`)
        .join('\n\n')}`;

      const blob = new Blob([content], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `chat-${Date.now()}.md`;
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  const toggleDataSource = (source: keyof DataSource) => {
    setDataSources(prev => ({ ...prev, [source]: !prev[source] }));
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 p-4">
          <div className="max-w-5xl mx-auto">
            <h1 className="text-xl font-bold text-gray-900">AI Chat Assistant</h1>
            <p className="text-sm text-gray-600">Ask questions about your projects and documents</p>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-5xl mx-auto p-4 space-y-4">
            {messages.length === 0 && (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">💬</div>
                <h2 className="text-2xl font-semibold text-gray-800 mb-2">
                  Start a Conversation
                </h2>
                <p className="text-gray-600 mb-8">
                  Ask questions about your projects, documents, or get AI-powered insights
                </p>
                <SuggestedActions
                  onActionClick={handleSendMessage}
                  recentQueries={recentQueries}
                  context={context}
                />
              </div>
            )}

            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                message={message}
                onAction={handleAction}
              />
            ))}

            {isLoading && (
              <div className="flex items-center gap-3 p-4 bg-white border border-gray-200 rounded-lg">
                <Loader2 className="w-5 h-5 animate-spin text-blue-600" />
                <span className="text-sm text-gray-600">AI is thinking...</span>
              </div>
            )}

            {error && (
              <div className="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg">
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                <div>
                  <div className="text-sm font-semibold text-red-900">Error</div>
                  <div className="text-sm text-red-700">{error}</div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="bg-white border-t border-gray-200 p-4">
          <div className="max-w-5xl mx-auto">
            {/* Data Source Toggles */}
            <div className="flex items-center gap-3 mb-3 text-sm">
              <span className="text-gray-600 font-medium">Data Sources:</span>
              <button
                onClick={() => toggleDataSource('neo4j')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full transition-colors ${
                  dataSources.neo4j
                    ? 'bg-blue-100 text-blue-800 border-2 border-blue-400'
                    : 'bg-gray-100 text-gray-500 border-2 border-gray-300'
                }`}
              >
                <Database className="w-3.5 h-3.5" />
                Neo4j
              </button>
              <button
                onClick={() => toggleDataSource('qdrant')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full transition-colors ${
                  dataSources.qdrant
                    ? 'bg-purple-100 text-purple-800 border-2 border-purple-400'
                    : 'bg-gray-100 text-gray-500 border-2 border-gray-300'
                }`}
              >
                <Search className="w-3.5 h-3.5" />
                Qdrant
              </button>
              <button
                onClick={() => toggleDataSource('internet')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full transition-colors ${
                  dataSources.internet
                    ? 'bg-green-100 text-green-800 border-2 border-green-400'
                    : 'bg-gray-100 text-gray-500 border-2 border-gray-300'
                }`}
              >
                <Globe className="w-3.5 h-3.5" />
                Internet
              </button>
            </div>

            {/* Input Box */}
            <div className="flex gap-2">
              <textarea
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask a question about your projects..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={3}
                disabled={isLoading}
              />
              <button
                onClick={() => handleSendMessage()}
                disabled={!input.trim() || isLoading}
                className="px-6 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
              >
                {isLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
              </button>
            </div>

            <div className="text-xs text-gray-500 mt-2">
              Press Enter to send, Shift+Enter for new line
            </div>
          </div>
        </div>
      </div>

      {/* Context Sidebar */}
      <div className="w-80 bg-white border-l border-gray-200 p-4 overflow-y-auto">
        <div className="space-y-6">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Settings className="w-4 h-4 text-gray-600" />
              <h2 className="font-semibold text-gray-900">Context</h2>
            </div>

            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Customer
                </label>
                <select
                  value={context.customer}
                  onChange={(e) => setContext(prev => ({ ...prev, customer: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Customers</option>
                  <option value="McKenney">McKenney</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Scope
                </label>
                <select
                  value={context.scope}
                  onChange={(e) => setContext(prev => ({ ...prev, scope: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="All">All Scopes</option>
                  <option value="Mechanical">Mechanical</option>
                  <option value="Electrical">Electrical</option>
                  <option value="Plumbing">Plumbing</option>
                  <option value="HVAC">HVAC</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Project ID
                </label>
                <input
                  type="text"
                  value={context.projectId || ''}
                  onChange={(e) => setContext(prev => ({ ...prev, projectId: e.target.value }))}
                  placeholder="Enter project ID..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>

          {messages.length > 0 && (
            <SuggestedActions
              onActionClick={handleSendMessage}
              recentQueries={recentQueries}
              context={context}
            />
          )}

          <div className="pt-4 border-t border-gray-200">
            <div className="text-xs text-gray-500 space-y-1">
              <div className="flex items-center justify-between">
                <span>Messages:</span>
                <span className="font-medium">{messages.length}</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Active Sources:</span>
                <span className="font-medium">
                  {Object.values(dataSources).filter(Boolean).length}/3
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
