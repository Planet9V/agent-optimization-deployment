/**
 * GAP-003 Query Control System - Model Switcher
 * Dynamic model switching with checkpoint safety
 */

import { ModelType } from '../types';
import { ModelRegistry, modelRegistry } from './model-registry';
import { CheckpointManager, checkpointManager } from '../checkpoint/checkpoint-manager';
import { mcpClient } from '../mcp-client';
import { QueryStateMachine } from '../state/state-machine';

export interface ModelSwitchResult {
  success: boolean;
  previousModel: ModelType;
  currentModel: ModelType;
  switchTimeMs: number;
  checkpointCreated: boolean;
}

/**
 * Model Switcher
 * Handles safe model transitions with checkpoint backup
 */
export class ModelSwitcher {
  private registry: ModelRegistry;
  private checkpointManager: CheckpointManager;
  private currentModel: ModelType = ModelType.SONNET;

  constructor(
    registry?: ModelRegistry,
    checkpointManager?: CheckpointManager
  ) {
    this.registry = registry || modelRegistry;
    this.checkpointManager = checkpointManager || checkpointManager;
  }

  /**
   * Switch to a different model
   */
  async switchModel(
    queryId: string,
    targetModel: ModelType,
    stateMachine: QueryStateMachine
  ): Promise<ModelSwitchResult> {
    const startTime = Date.now();

    try {
      console.log(
        `Switching model for query ${queryId}: ${this.currentModel} → ${targetModel}`
      );

      // 1. Validate target model
      const capabilities = this.registry.getCapabilities(targetModel);
      console.log(
        `Target model capabilities: ${capabilities.strengthAreas.join(', ')}`
      );

      // 2. Create safety checkpoint before switch
      const context = stateMachine.getContext();
      const checkpoint = await this.checkpointManager.createCheckpoint(
        queryId,
        context,
        'pre_model_switch'
      );

      console.log(
        `Safety checkpoint created: ${checkpoint.metadata.size} bytes`
      );

      // 3. Switch model via MCP
      await mcpClient.queryControl({
        action: 'change_model',
        queryId,
        model: targetModel
      });

      // 4. Update model config in memory
      await mcpClient.storeMemory(
        `model_config_${queryId}`,
        {
          model: targetModel,
          switchedAt: Date.now(),
          previousModel: this.currentModel,
          capabilities: capabilities
        }
      );

      const previousModel = this.currentModel;
      this.currentModel = targetModel;

      // 5. Train neural pattern on switch performance
      const switchTime = Date.now() - startTime;
      await mcpClient.trainNeuralPattern(
        'optimization',
        `model_switch:${previousModel}->${targetModel}:${switchTime}ms`,
        20
      );

      console.log(
        `Model switch completed: ${previousModel} → ${targetModel} (${switchTime}ms)`
      );

      // Validate performance target (<200ms)
      if (switchTime > 200) {
        console.warn(
          `Model switch exceeded target: ${switchTime}ms (target: <200ms)`
        );
      }

      return {
        success: true,
        previousModel,
        currentModel: targetModel,
        switchTimeMs: switchTime,
        checkpointCreated: true
      };
    } catch (error) {
      console.error(`Model switch failed: ${error}`);

      // Train failure pattern
      await mcpClient.trainNeuralPattern(
        'coordination',
        `model_switch_failed:${this.currentModel}->${targetModel}:${error}`,
        10
      );

      throw new Error(`Failed to switch model: ${error}`);
    }
  }

  /**
   * Get current model
   */
  getCurrentModel(): ModelType {
    return this.currentModel;
  }

  /**
   * Set current model (for initialization)
   */
  setCurrentModel(model: ModelType): void {
    if (!this.registry.isValidModel(model)) {
      throw new Error(`Invalid model type: ${model}`);
    }
    this.currentModel = model;
  }

  /**
   * Recommend and switch to optimal model
   */
  async switchToOptimalModel(
    queryId: string,
    taskType: string,
    stateMachine: QueryStateMachine
  ): Promise<ModelSwitchResult> {
    try {
      // Get recommendation from registry
      const recommendation = await this.registry.recommendModel(taskType);

      console.log(
        `Recommendation: ${recommendation.model} ` +
        `(${Math.round(recommendation.confidence * 100)}% confidence) - ` +
        `${recommendation.reasoning}`
      );

      // Only switch if different from current
      if (recommendation.model === this.currentModel) {
        console.log('Already using recommended model, no switch needed');
        return {
          success: true,
          previousModel: this.currentModel,
          currentModel: this.currentModel,
          switchTimeMs: 0,
          checkpointCreated: false
        };
      }

      // Switch to recommended model
      return await this.switchModel(
        queryId,
        recommendation.model,
        stateMachine
      );
    } catch (error) {
      console.error(`Optimal model switch failed: ${error}`);
      throw error;
    }
  }

  /**
   * Get switch statistics
   */
  getStatistics(): {
    currentModel: ModelType;
    totalSwitches: number;
    averageSwitchTime: number;
  } {
    // In production, would track actual switch operations
    return {
      currentModel: this.currentModel,
      totalSwitches: 0,
      averageSwitchTime: 0
    };
  }
}

export const modelSwitcher = new ModelSwitcher();
