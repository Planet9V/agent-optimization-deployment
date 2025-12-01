/**
 * GAP-003 Query Control System - State Machine
 * Core state machine with MCP integration for query lifecycle management
 */

import { QueryState, QueryContext, StateTransition } from '../types';
import { mcpClient } from '../mcp-client';

export class QueryStateMachine {
  private state: QueryState = QueryState.INIT;
  private context: QueryContext;
  private transitions: Map<string, StateTransition>;

  constructor(queryId: string, initialContext?: Partial<QueryContext>) {
    this.context = {
      queryId,
      state: QueryState.INIT,
      metadata: initialContext?.metadata || {},
      timestamp: Date.now(),
      execution: initialContext?.execution,
      model: initialContext?.model
    };
    this.transitions = this.buildTransitionMap();
  }

  /**
   * Execute state transition
   */
  async transition(action: string): Promise<boolean> {
    const key = `${this.state}:${action}`;
    const transition = this.transitions.get(key);

    if (!transition) {
      throw new Error(
        `Invalid transition: ${this.state} -[${action}]-> ?`
      );
    }

    // Check guard condition
    if (transition.guard && !transition.guard(this.context)) {
      console.warn(`Transition guard failed: ${key}`);
      return false;
    }

    const oldState = this.state;

    try {
      // Execute side effects
      if (transition.effect) {
        await transition.effect(this.context);
      }

      // Update state
      this.state = transition.to;
      this.context.state = transition.to;

      // Store state change in MCP memory
      await mcpClient.storeMemory(
        `state_${this.context.queryId}`,
        {
          from: oldState,
          to: this.state,
          action,
          timestamp: Date.now()
        },
        86400 // 24 hours TTL
      );

      // Train neural pattern on successful transition
      await mcpClient.trainNeuralPattern(
        'coordination',
        `state_transition:${oldState}->${this.state}:${action}`,
        10
      );

      return true;
    } catch (error) {
      console.error(`Transition effect failed: ${key}`, error);

      // Store error state
      this.context.error = error as Error;
      this.state = QueryState.ERROR;
      this.context.state = QueryState.ERROR;

      await mcpClient.storeMemory(
        `error_${this.context.queryId}`,
        {
          from: oldState,
          action,
          error: (error as Error).message,
          timestamp: Date.now()
        }
      );

      throw error;
    }
  }

  /**
   * Get current state
   */
  getState(): QueryState {
    return this.state;
  }

  /**
   * Get full context
   */
  getContext(): QueryContext {
    return { ...this.context };
  }

  /**
   * Update context metadata
   */
  updateContext(updates: Partial<QueryContext>): void {
    this.context = {
      ...this.context,
      ...updates,
      timestamp: Date.now()
    };
  }

  /**
   * Build transition map with guards and effects
   */
  private buildTransitionMap(): Map<string, StateTransition> {
    const transitions: StateTransition[] = [
      // INIT -> RUNNING
      {
        from: QueryState.INIT,
        to: QueryState.RUNNING,
        action: 'START',
        effect: async (ctx) => {
          console.log(`Starting query: ${ctx.queryId}`);
          await mcpClient.trainNeuralPattern(
            'coordination',
            `query_start:${ctx.queryId}`,
            10
          );
        }
      },

      // RUNNING -> PAUSED
      {
        from: QueryState.RUNNING,
        to: QueryState.PAUSED,
        action: 'PAUSE',
        effect: async (ctx) => {
          console.log(`Pausing query: ${ctx.queryId}`);
          // Checkpoint will be created by checkpoint manager
          await mcpClient.createSnapshot(ctx.queryId);
        }
      },

      // PAUSED -> RUNNING
      {
        from: QueryState.PAUSED,
        to: QueryState.RUNNING,
        action: 'RESUME',
        guard: (ctx) => {
          // Verify checkpoint exists before resuming
          return true; // Simplified for MVP
        },
        effect: async (ctx) => {
          console.log(`Resuming query: ${ctx.queryId}`);
          await mcpClient.restoreContext(ctx.queryId);
          await mcpClient.trainNeuralPattern(
            'optimization',
            `query_resume:${ctx.queryId}`,
            20
          );
        }
      },

      // RUNNING -> COMPLETED
      {
        from: QueryState.RUNNING,
        to: QueryState.COMPLETED,
        action: 'COMPLETE',
        effect: async (ctx) => {
          console.log(`Completing query: ${ctx.queryId}`);
          await mcpClient.trainNeuralPattern(
            'coordination',
            `query_complete:${ctx.queryId}:success`,
            10
          );
        }
      },

      // RUNNING -> TERMINATED
      {
        from: QueryState.RUNNING,
        to: QueryState.TERMINATED,
        action: 'TERMINATE',
        effect: async (ctx) => {
          console.log(`Terminating query: ${ctx.queryId}`);
          // Cleanup resources
        }
      },

      // PAUSED -> TERMINATED
      {
        from: QueryState.PAUSED,
        to: QueryState.TERMINATED,
        action: 'TERMINATE',
        effect: async (ctx) => {
          console.log(`Terminating paused query: ${ctx.queryId}`);
          // Cleanup resources and checkpoints
        }
      },

      // RUNNING -> ERROR
      {
        from: QueryState.RUNNING,
        to: QueryState.ERROR,
        action: 'ERROR',
        effect: async (ctx) => {
          console.error(`Query error: ${ctx.queryId}`, ctx.error);
          await mcpClient.storeMemory(
            `error_${ctx.queryId}`,
            {
              error: ctx.error?.message || 'Unknown error',
              timestamp: Date.now(),
              state: ctx.state
            }
          );
        }
      },

      // PAUSED -> ERROR
      {
        from: QueryState.PAUSED,
        to: QueryState.ERROR,
        action: 'ERROR',
        effect: async (ctx) => {
          console.error(`Paused query error: ${ctx.queryId}`, ctx.error);
        }
      }
    ];

    return new Map(
      transitions.map(t => [`${t.from}:${t.action}`, t])
    );
  }

  /**
   * Get available transitions from current state
   */
  getAvailableTransitions(): string[] {
    const available: string[] = [];
    for (const [key, transition] of this.transitions) {
      if (transition.from === this.state) {
        available.push(transition.action);
      }
    }
    return available;
  }

  /**
   * Check if transition is valid
   */
  canTransition(action: string): boolean {
    const key = `${this.state}:${action}`;
    const transition = this.transitions.get(key);

    if (!transition) return false;
    if (transition.guard) {
      return transition.guard(this.context);
    }
    return true;
  }
}
