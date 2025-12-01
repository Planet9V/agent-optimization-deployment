/**
 * GAP-003 Query Control System - Model Registry
 * Registry for Claude model capabilities and characteristics
 */

import { ModelType } from '../types';
import { mcpClient } from '../mcp-client';

export interface ModelCapabilities {
  maxTokens: number;
  contextWindow: number;
  costPer1kTokens: number;
  latencyMs: number;
  strengthAreas: string[];
  recommendedFor: string[];
}

/**
 * Model Registry
 * Maintains metadata and capabilities for all supported models
 */
export class ModelRegistry {
  private models: Map<ModelType, ModelCapabilities>;

  constructor() {
    this.models = this.initializeModels();
  }

  /**
   * Initialize model capabilities
   */
  private initializeModels(): Map<ModelType, ModelCapabilities> {
    return new Map([
      [ModelType.SONNET, {
        maxTokens: 8192,
        contextWindow: 200000,
        costPer1kTokens: 0.003,
        latencyMs: 1500,
        strengthAreas: [
          'reasoning',
          'coding',
          'complex_analysis',
          'structured_output',
          'technical_documentation'
        ],
        recommendedFor: [
          'code_generation',
          'technical_analysis',
          'architecture_design',
          'debugging',
          'documentation_writing'
        ]
      }],

      [ModelType.HAIKU, {
        maxTokens: 4096,
        contextWindow: 200000,
        costPer1kTokens: 0.001,
        latencyMs: 500,
        strengthAreas: [
          'speed',
          'efficiency',
          'simple_tasks',
          'quick_responses',
          'batch_processing'
        ],
        recommendedFor: [
          'simple_queries',
          'data_extraction',
          'classification',
          'summarization',
          'quick_iterations'
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
          'edge_cases',
          'strategic_thinking'
        ],
        recommendedFor: [
          'complex_problems',
          'creative_tasks',
          'strategic_planning',
          'edge_case_handling',
          'high_stakes_decisions'
        ]
      }]
    ]);
  }

  /**
   * Get capabilities for a specific model
   */
  getCapabilities(model: ModelType): ModelCapabilities {
    const capabilities = this.models.get(model);
    if (!capabilities) {
      throw new Error(`Unknown model type: ${model}`);
    }
    return { ...capabilities };
  }

  /**
   * Recommend model based on task type using neural prediction
   */
  async recommendModel(taskType: string): Promise<{
    model: ModelType;
    confidence: number;
    reasoning: string;
  }> {
    try {
      // Use neural prediction for smart recommendations
      const result = await mcpClient.trainNeuralPattern(
        'prediction',
        `model_recommendation:${taskType}`,
        20
      );

      // Analyze task characteristics
      const taskLower = taskType.toLowerCase();

      // Rule-based recommendation with confidence scoring
      let recommendedModel: ModelType;
      let confidence: number;
      let reasoning: string;

      if (taskLower.includes('quick') || taskLower.includes('simple') ||
          taskLower.includes('fast') || taskLower.includes('batch')) {
        recommendedModel = ModelType.HAIKU;
        confidence = 0.85;
        reasoning = 'Haiku recommended for speed and efficiency';
      } else if (taskLower.includes('complex') || taskLower.includes('creative') ||
                 taskLower.includes('strategic') || taskLower.includes('edge')) {
        recommendedModel = ModelType.OPUS;
        confidence = 0.80;
        reasoning = 'Opus recommended for complex reasoning and creativity';
      } else {
        recommendedModel = ModelType.SONNET;
        confidence = 0.90;
        reasoning = 'Sonnet recommended for balanced performance';
      }

      // Adjust confidence based on neural accuracy
      confidence = Math.min(confidence, result.accuracy);

      console.log(
        `Model recommendation: ${recommendedModel} (${Math.round(confidence * 100)}% confidence) - ${reasoning}`
      );

      return { model: recommendedModel, confidence, reasoning };
    } catch (error) {
      console.error(`Model recommendation failed: ${error}`);

      // Fallback to Sonnet (balanced default)
      return {
        model: ModelType.SONNET,
        confidence: 0.7,
        reasoning: 'Fallback to Sonnet (default)'
      };
    }
  }

  /**
   * Compare models for specific use case
   */
  compareModels(useCase: string): Array<{
    model: ModelType;
    score: number;
    pros: string[];
    cons: string[];
  }> {
    const useCaseLower = useCase.toLowerCase();
    const comparisons: Array<{
      model: ModelType;
      score: number;
      pros: string[];
      cons: string[];
    }> = [];

    for (const [model, capabilities] of this.models) {
      let score = 0;
      const pros: string[] = [];
      const cons: string[] = [];

      // Score based on capabilities matching use case
      capabilities.strengthAreas.forEach(area => {
        if (useCaseLower.includes(area.replace('_', ' '))) {
          score += 20;
          pros.push(`Strong in ${area}`);
        }
      });

      // Add general pros/cons
      if (model === ModelType.HAIKU) {
        pros.push('Fastest response time', 'Most cost-effective');
        cons.push('Lower max tokens', 'Less nuanced reasoning');
        score += capabilities.latencyMs < 1000 ? 15 : 0;
      } else if (model === ModelType.SONNET) {
        pros.push('Balanced performance', 'High max tokens', 'Reliable quality');
        cons.push('Moderate cost', 'Moderate speed');
        score += 25; // General purpose bonus
      } else if (model === ModelType.OPUS) {
        pros.push('Highest quality', 'Best for complex tasks');
        cons.push('Highest cost', 'Slowest response');
        score += useCaseLower.includes('complex') ? 30 : 10;
      }

      comparisons.push({ model, score, pros, cons });
    }

    return comparisons.sort((a, b) => b.score - a.score);
  }

  /**
   * Get all registered models
   */
  getAllModels(): ModelType[] {
    return Array.from(this.models.keys());
  }

  /**
   * Validate if model exists
   */
  isValidModel(model: string): model is ModelType {
    return Object.values(ModelType).includes(model as ModelType);
  }
}

export const modelRegistry = new ModelRegistry();
