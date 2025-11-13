/**
 * Mock for @xenova/transformers
 * Avoids ESM issues and model downloads in tests
 */

const mockPipeline = jest.fn().mockResolvedValue(async (text) => ({
  data: Array.from({ length: 384 }, () => Math.random()),
}));

class MockPipeline {
  constructor(task, model) {
    this.task = task;
    this.model = model;
  }

  async run(inputs) {
    return {
      data: Array.from({ length: 384 }, () => Math.random()),
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
