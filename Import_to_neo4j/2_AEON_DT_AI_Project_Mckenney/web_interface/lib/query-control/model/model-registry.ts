/**
 * GAP-003 Query Control System - Model Registry
 *
 * File: lib/query-control/model/model-registry.ts
 * Created: 2025-11-14
 * Version: v1.0.0
 * Purpose: Model capabilities registry and neural-based recommendations
 *
 * Constitutional Compliance:
 * - DILIGENCE: Complete model catalog with accurate capabilities
 * - INTEGRITY: Verifiable model specifications
 * - NO DEVELOPMENT THEATER: Production-ready model management
 *
 * Performance Target: <10ms model lookup, <100ms recommendation
 */

export enum ModelType {
  SONNET = 'claude-sonnet-4-5-20250929',
  HAIKU = 'claude-3-5-haiku-20241022',
  OPUS = 'claude-3-opus-20240229'
}

export interface ModelCapabilities {
  maxTokens: number;
  contextWindow: number;
  costPer1kTokens: number;
  latencyMs: number;
  strengthAreas: string[];
}

export interface ModelRecommendation {
  recommendedModel: ModelType;
  confidence: number;
  reasoning: string;
  alternativeModels: ModelType[];
}

/**
 * ModelRegistry - Central registry for Claude model capabilities
 *
 * Features:
 * - Accurate model specifications (tokens, cost, latency, strengths)
 * - Neural-based model recommendations (prepared for MCP integration)
 * - Fast capability lookups (<10ms)
 * - Model comparison and selection logic
 */
export class ModelRegistry {
  private models: Map<ModelType, ModelCapabilities>;

  constructor() {
    this.models = new Map([
      [ModelType.SONNET, {
        maxTokens: 8192,
        contextWindow: 200000,
        costPer1kTokens: 0.003,
        latencyMs: 1500,
        strengthAreas: [
          'reasoning',
          'coding',
          'complex_analysis',
          'mathematical_computation',
          'system_design',
          'technical_writing'
        ]
      }],
      [ModelType.HAIKU, {
        maxTokens: 4096,
        contextWindow: 200000,
        costPer1kTokens: 0.001,
        latencyMs: 500,
        strengthAreas: [
          'speed',
          'simple_tasks',
          'efficiency',
          'quick_responses',
          'batch_processing',
          'routine_operations'
        ]
      }],
      [ModelType.OPUS, {
        maxTokens: 4096,
        contextWindow: 200000,
        costPer1kTokens: 0.015,
        latencyMs: 3000,
        strengthAreas: [
          'creativity',
          'nuance',
          'complex_reasoning',
          'artistic_tasks',
          'subjective_analysis',
          'ambiguous_problems'
        ]
      }]
    ]);
  }

  /**
   * Get capabilities for a specific model
   *
   * @param model - Model type
   * @returns Model capabilities
   * @throws Error if model unknown
   */
  getCapabilities(model: ModelType): ModelCapabilities {
    const startTime = Date.now();

    const caps = this.models.get(model);
    if (!caps) {
      throw new Error(`Unknown model: ${model}`);
    }

    const duration = Date.now() - startTime;

    // Performance logging
    if (duration > 10) {
      console.warn(`Model lookup exceeded target: ${duration}ms > 10ms`);
    }

    return caps;
  }

  /**
   * Get all registered models
   *
   * @returns Map of all models and their capabilities
   */
  getAllModels(): Map<ModelType, ModelCapabilities> {
    return new Map(this.models);
  }

  /**
   * Recommend model for a specific task type
   *
   * Uses neural prediction when available (prepared for MCP integration).
   * Falls back to rule-based recommendation.
   *
   * @param taskType - Description of task (e.g., "complex analysis", "quick response")
   * @param currentModel - Current model being used (optional)
   * @returns Recommendation with confidence and reasoning
   */
  async recommendModel(
    taskType: string,
    currentModel?: ModelType
  ): Promise<ModelRecommendation> {
    const startTime = Date.now();

    // Neural prediction integration (prepared for MCP availability)
    try {
      // This will be integrated when mcp__claude_flow__neural_predict is available
      // const result = await this.neuralRecommendation(taskType);
      // return result;

      // For MVP: Use rule-based recommendation
      const recommendation = this.ruleBasedRecommendation(taskType, currentModel);

      const duration = Date.now() - startTime;
      if (duration > 100) {
        console.warn(`Model recommendation exceeded target: ${duration}ms > 100ms`);
      } else {
        console.log(`Model recommendation completed in ${duration}ms (target: <100ms)`);
      }

      return recommendation;
    } catch (error) {
      console.error('Model recommendation failed:', error);

      // Fallback to safe default
      return {
        recommendedModel: ModelType.SONNET,
        confidence: 0.5,
        reasoning: 'Fallback to Sonnet due to recommendation error',
        alternativeModels: [ModelType.HAIKU, ModelType.OPUS]
      };
    }
  }

  /**
   * Rule-based model recommendation (MVP implementation)
   *
   * @param taskType - Task description
   * @param currentModel - Current model (optional)
   * @returns Model recommendation
   */
  private ruleBasedRecommendation(
    taskType: string,
    currentModel?: ModelType
  ): ModelRecommendation {
    const taskLower = taskType.toLowerCase();

    // Speed-critical tasks → Haiku
    if (
      taskLower.includes('quick') ||
      taskLower.includes('fast') ||
      taskLower.includes('simple') ||
      taskLower.includes('routine') ||
      taskLower.includes('batch')
    ) {
      return {
        recommendedModel: ModelType.HAIKU,
        confidence: 0.85,
        reasoning: 'Speed-critical task detected, Haiku optimal for quick responses',
        alternativeModels: [ModelType.SONNET]
      };
    }

    // Creative/nuanced tasks → Opus
    if (
      taskLower.includes('creative') ||
      taskLower.includes('nuance') ||
      taskLower.includes('artistic') ||
      taskLower.includes('subjective') ||
      taskLower.includes('ambiguous')
    ) {
      return {
        recommendedModel: ModelType.OPUS,
        confidence: 0.80,
        reasoning: 'Creative/nuanced task detected, Opus optimal for complex reasoning',
        alternativeModels: [ModelType.SONNET]
      };
    }

    // Complex analysis/coding → Sonnet
    if (
      taskLower.includes('complex') ||
      taskLower.includes('analysis') ||
      taskLower.includes('coding') ||
      taskLower.includes('technical') ||
      taskLower.includes('design') ||
      taskLower.includes('reasoning')
    ) {
      return {
        recommendedModel: ModelType.SONNET,
        confidence: 0.90,
        reasoning: 'Complex analytical task detected, Sonnet optimal for reasoning and coding',
        alternativeModels: [ModelType.OPUS, ModelType.HAIKU]
      };
    }

    // Default to current model if available, or Sonnet
    const defaultModel = currentModel || ModelType.SONNET;

    return {
      recommendedModel: defaultModel,
      confidence: 0.60,
      reasoning: 'No clear task type indicators, using default/current model',
      alternativeModels: Object.values(ModelType).filter(m => m !== defaultModel)
    };
  }

  /**
   * Compare two models on specific criteria
   *
   * @param modelA - First model
   * @param modelB - Second model
   * @param criteria - Comparison criteria (cost, speed, power)
   * @returns Comparison result
   */
  compareModels(
    modelA: ModelType,
    modelB: ModelType,
    criteria: 'cost' | 'speed' | 'power'
  ): {
    better: ModelType;
    difference: string;
    recommendation: string;
  } {
    const capsA = this.getCapabilities(modelA);
    const capsB = this.getCapabilities(modelB);

    switch (criteria) {
      case 'cost':
        const cheaper = capsA.costPer1kTokens < capsB.costPer1kTokens ? modelA : modelB;
        const costDiff = Math.abs(capsA.costPer1kTokens - capsB.costPer1kTokens);
        const costSavings = ((costDiff / Math.max(capsA.costPer1kTokens, capsB.costPer1kTokens)) * 100).toFixed(1);
        return {
          better: cheaper,
          difference: `${costSavings}% cost savings`,
          recommendation: `Use ${cheaper} for cost optimization`
        };

      case 'speed':
        const faster = capsA.latencyMs < capsB.latencyMs ? modelA : modelB;
        const speedDiff = Math.abs(capsA.latencyMs - capsB.latencyMs);
        const speedup = ((speedDiff / Math.max(capsA.latencyMs, capsB.latencyMs)) * 100).toFixed(1);
        return {
          better: faster,
          difference: `${speedup}% faster response`,
          recommendation: `Use ${faster} for time-sensitive tasks`
        };

      case 'power':
        // Sonnet > Opus > Haiku for general power
        const powerRanking: Record<ModelType, number> = {
          [ModelType.SONNET]: 3,
          [ModelType.OPUS]: 2,
          [ModelType.HAIKU]: 1
        };
        const moreCapable = powerRanking[modelA] > powerRanking[modelB] ? modelA : modelB;
        return {
          better: moreCapable,
          difference: `Higher reasoning capability`,
          recommendation: `Use ${moreCapable} for complex tasks`
        };

      default:
        throw new Error(`Unknown comparison criteria: ${criteria}`);
    }
  }

  /**
   * Get model statistics for monitoring
   *
   * @returns Model registry statistics
   */
  getStatistics(): {
    totalModels: number;
    averageCost: number;
    averageLatency: number;
    models: ModelType[];
  } {
    const models = Array.from(this.models.entries());

    const totalCost = models.reduce((sum, [_, caps]) => sum + caps.costPer1kTokens, 0);
    const totalLatency = models.reduce((sum, [_, caps]) => sum + caps.latencyMs, 0);

    return {
      totalModels: models.length,
      averageCost: totalCost / models.length,
      averageLatency: totalLatency / models.length,
      models: models.map(([model]) => model)
    };
  }

  /**
   * Validate model type (type guard)
   *
   * @param model - Model string to validate
   * @returns true if valid ModelType
   */
  isValidModel(model: string): model is ModelType {
    return Object.values(ModelType).includes(model as ModelType);
  }
}

/**
 * Singleton model registry instance
 */
let registryInstance: ModelRegistry | null = null;

/**
 * Get or create model registry singleton
 */
export function getModelRegistry(): ModelRegistry {
  if (!registryInstance) {
    registryInstance = new ModelRegistry();
  }
  return registryInstance;
}
