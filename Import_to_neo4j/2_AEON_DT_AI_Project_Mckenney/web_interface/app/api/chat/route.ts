import { NextRequest } from 'next/server';
import { aiOrchestrator, type DataSource, type QueryContext } from '@/lib/ai-orchestrator';
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export const runtime = 'nodejs';
export const maxDuration = 30;

interface ChatRequest {
  messages: Array<{
    role: 'user' | 'assistant';
    content: string;
  }>;
  dataSources: DataSource;
  context: QueryContext;
}

export async function POST(req: NextRequest) {
  try {
    const body: ChatRequest = await req.json();
    const { messages, dataSources, context } = body;

    // Get the last user message
    const lastMessage = messages[messages.length - 1];
    if (!lastMessage || lastMessage.role !== 'user') {
      return new Response('Invalid message format', { status: 400 });
    }

    const query = lastMessage.content;

    // Orchestrate multi-source query
    const sourceResults = await aiOrchestrator.orchestrateQuery(
      query,
      context,
      dataSources
    );

    // Build context from source results
    const contextText = sourceResults
      .map((r, idx) => {
        const source = r.source.toUpperCase();
        const metadata = r.metadata
          ? Object.entries(r.metadata)
              .filter(([k, v]) => v !== null && v !== undefined)
              .map(([k, v]) => `${k}: ${v}`)
              .join(', ')
          : '';

        return `[${source} ${idx + 1}${metadata ? ` - ${metadata}` : ''}]\n${r.content}`;
      })
      .join('\n\n');

    // System prompt with context
    const systemPrompt = `You are an AI assistant for McKenney's construction project management system.
You have access to:
${dataSources.neo4j ? '✓' : '✗'} Neo4j graph database (project relationships, documents, metadata)
${dataSources.qdrant ? '✓' : '✗'} Qdrant vector database (semantic document search)
${dataSources.internet ? '✓' : '✗'} Internet search (general knowledge)

Current context:
- Customer: ${context.customer || 'Not specified'}
- Scope: ${context.scope || 'Not specified'}
- Project: ${context.projectId || 'Not specified'}

Guidelines:
1. Provide accurate, helpful answers based on the context provided
2. Cite sources when referencing specific information (e.g., "[NEO4J 1]")
3. Be concise but thorough
4. If information is unavailable, acknowledge it clearly
5. Suggest relevant follow-up actions when appropriate

Context from data sources:
${contextText || 'No relevant context found'}`;

    // Create conversation history with context
    const conversationMessages = messages.slice(0, -1).map(m => ({
      role: m.role,
      content: m.content
    }));

    conversationMessages.push({
      role: 'user',
      content: query
    });

    // Stream response using Vercel AI SDK
    const result = await streamText({
      model: openai('gpt-4o-mini'),
      system: systemPrompt,
      messages: conversationMessages,
      temperature: 0.7,
    });

    // Create custom response with source metadata
    const encoder = new TextEncoder();
    const stream = new ReadableStream({
      async start(controller) {
        // Send sources metadata first
        const sourcesData = JSON.stringify({
          type: 'sources',
          sources: sourceResults.map(r => ({
            source: r.source,
            content: r.content,
            metadata: r.metadata
          }))
        });
        controller.enqueue(encoder.encode(`data: ${sourcesData}\n\n`));

        // Stream AI response
        for await (const chunk of result.textStream) {
          const data = JSON.stringify({
            type: 'text',
            content: chunk
          });
          controller.enqueue(encoder.encode(`data: ${data}\n\n`));
        }

        // Send completion signal
        controller.enqueue(encoder.encode('data: [DONE]\n\n'));
        controller.close();
      },
    });

    return new Response(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });

  } catch (error: any) {
    console.error('Chat API error:', error);
    return new Response(
      JSON.stringify({
        error: 'Failed to process chat request',
        details: error.message
      }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}
