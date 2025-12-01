/**
 * Mock for @xenova/transformers
 * Avoids ESM issues and model downloads in tests
 * CRITICAL: Must return callable model function from pipeline, not wrapped in promise
 */

// Create a deterministic embedding generator for consistent tests
const generateDeterministicEmbedding = (text, dimension = 384) => {
  // Use text hash for deterministic but varied embeddings
  const hash = text.split('').reduce((acc, char) => {
    return ((acc << 5) - acc) + char.charCodeAt(0);
  }, 0);

  const embedding = new Float32Array(dimension);
  for (let i = 0; i < dimension; i++) {
    // Pseudo-random but deterministic based on hash and index
    const value = Math.sin(hash * (i + 1)) * 10000;
    embedding[i] = (value - Math.floor(value)) * 2 - 1; // Normalize to [-1, 1]
  }

  return embedding;
};

// Mock pipeline function that returns a callable function (the model)
const mockPipeline = jest.fn(async (task, model, options) => {
  console.log('[MOCK] pipeline called with:', task, model);

  // Return a callable function that represents the model
  const modelFunction = async (text, options) => {
    console.log('[MOCK] model function called with text length:', text?.length);
    // Return deterministic embedding for consistent similarity matching in tests
    return {
      data: generateDeterministicEmbedding(text),
    };
  };

  // Make it act like a FeatureExtractionPipeline
  modelFunction.task = task;
  modelFunction.model = model;

  console.log('[MOCK] returning model function, type:', typeof modelFunction);
  return modelFunction;
});

class MockPipeline {
  constructor(task, model) {
    this.task = task;
    this.model = model;
  }

  async run(inputs) {
    return {
      data: new Float32Array(Array.from({ length: 384 }, () => Math.random())),
    };
  }
}

class MockFeatureExtractionPipeline extends MockPipeline {
  constructor(model) {
    super('feature-extraction', model);
  }
}

module.exports = {
  pipeline: mockPipeline,
  Pipeline: MockPipeline,
  FeatureExtractionPipeline: MockFeatureExtractionPipeline,
};
