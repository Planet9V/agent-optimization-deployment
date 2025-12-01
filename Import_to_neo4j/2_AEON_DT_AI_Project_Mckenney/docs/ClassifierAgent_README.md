# ClassifierAgent - ML-Based Document Classification

## Overview

The `ClassifierAgent` provides intelligent, ML-based document classification for the AEON Automated Document Ingestion System. It classifies documents across three dimensions:

1. **Sector** (13 critical infrastructure sectors)
2. **Subsector** (388+ specific subsectors)
3. **Document Type** (technical specs, manuals, advisories, etc.)

## Key Features

### Machine Learning Classification
- **Random Forest Classifiers** with TF-IDF vectorization
- **Confidence Scoring** for auto-classification vs. interactive review
- **Multi-class Classification** across three dimensions simultaneously
- **Adaptive Training** handles small and imbalanced datasets

### Memory & Learning
- **Qdrant Vector Database Integration** for similarity search
- **Learn from Corrections** - stores user corrections for future reference
- **Similar Document Search** - finds previously classified similar documents
- **Cross-Session Learning** - persistent memory across runs

### Intelligent Classification
- **Confidence Thresholds** - configurable auto-classification threshold
- **Interactive Fallback** - triggers user review for low-confidence cases
- **Context-Aware Subsector** - uses sector context for better subsector predictions
- **Top-K Predictions** - provides alternative classifications with probabilities

## Architecture

```
ClassifierAgent (extends BaseAgent)
├── Sector Classifier
│   ├── TfidfVectorizer (5000 features, 1-3 grams)
│   ├── RandomForestClassifier (100 estimators)
│   └── LabelEncoder
├── Subsector Classifier
│   ├── TfidfVectorizer (5000 features, 1-3 grams)
│   ├── RandomForestClassifier (100 estimators)
│   └── LabelEncoder
├── Document Type Classifier
│   ├── TfidfVectorizer (3000 features, 1-2 grams)
│   ├── RandomForestClassifier (100 estimators)
│   └── LabelEncoder
└── QdrantMemoryManager
    ├── Sentence Transformer Embeddings (384-dim)
    ├── Vector Similarity Search
    └── Classification History
```

## Installation

### Required Dependencies

```bash
pip install scikit-learn pyyaml numpy

# Optional (for memory/learning features)
pip install qdrant-client sentence-transformers
```

### Configuration

Edit `config/main_config.yaml`:

```yaml
classification:
  confidence_threshold: 0.75        # Auto-classify if confidence >= 0.75
  interactive_mode: true            # Enable interactive fallback
  auto_classify_high_confidence: true

  model_paths:
    sector: "models/classifiers/sector_classifier.pkl"
    subsector: "models/classifiers/subsector_classifier.pkl"
    doctype: "models/classifiers/doctype_classifier.pkl"

memory:
  qdrant_enabled: false             # Enable for learning features
  qdrant_host: "localhost"
  qdrant_port: 6333
  collection_name: "document_classifications"
  vector_size: 384
  decision_tracking: true
  learning_enabled: true
```

## Usage

### Basic Classification

```python
from agents.classifier_agent import ClassifierAgent
import yaml

# Load configuration
with open('config/main_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Create agent
agent = ClassifierAgent('classifier', config)

# Classify a document
result = agent.classify_document(
    markdown_content=document_text,
    metadata={'filename': 'reactor_manual.pdf'}
)

print(f"Sector: {result['sector']} (confidence: {result['sector_confidence']:.3f})")
print(f"Subsector: {result['subsector']}")
print(f"Doc Type: {result['document_type']}")
print(f"Overall: {result['overall_confidence']:.3f}")

if result['auto_classified']:
    print("✓ Auto-classified (high confidence)")
else:
    print("⚠ Requires interactive review")
```

### Training Models

```python
# Prepare training data
training_data = {
    'sector': [
        {'text': 'nuclear reactor safety emergency shutdown', 'label': 'energy'},
        {'text': 'water treatment chlorine disinfection', 'label': 'water'},
        # ... more samples
    ],
    'subsector': [
        {'text': 'nuclear power generation control', 'label': 'nuclear_power'},
        {'text': 'water distribution pumping station', 'label': 'water_distribution'},
        # ... more samples
    ],
    'doctype': [
        {'text': 'technical specification requirements', 'label': 'technical_spec'},
        {'text': 'user manual operating procedures', 'label': 'user_manual'},
        # ... more samples
    ]
}

# Train models
saved_paths = agent.train_models(training_data)
print(f"Models saved to: {saved_paths}")
```

### Loading Pre-Trained Models

```python
# Models are loaded automatically if they exist
agent = ClassifierAgent('classifier', config)

# Or explicitly load
model_paths = {
    'sector': 'models/classifiers/sector_classifier.pkl',
    'subsector': 'models/classifiers/subsector_classifier.pkl',
    'doctype': 'models/classifiers/doctype_classifier.pkl'
}
agent.load_models(model_paths)
```

### Learning from Corrections

```python
# User corrects a classification
corrected = {
    'sector': 'energy',
    'subsector': 'hydroelectric',
    'document_type': 'technical_spec'
}

# Store correction for future learning
agent.learn_from_correction(document_text, corrected)

# Future similar documents will benefit from this correction
```

### Similar Document Search

```python
# Find similar previously classified documents
similar = agent.memory_manager.search_similar(
    text=document_text,
    limit=5,
    min_confidence=0.7
)

for doc in similar:
    print(f"Similar doc: {doc['classification']}")
    print(f"Similarity: {doc['similarity_score']:.3f}")
    print(f"Confidence: {doc['confidence']:.3f}")
```

## API Reference

### ClassifierAgent

#### `__init__(name: str, config: Dict[str, Any])`
Initialize the classifier agent with configuration.

#### `classify_document(markdown_content: str, metadata: Optional[Dict] = None) -> Dict`
Classify a document into sector, subsector, and document type.

**Returns:**
```python
{
    'sector': str,                     # Predicted sector
    'sector_confidence': float,        # Confidence 0-1
    'subsector': str,                  # Predicted subsector
    'subsector_confidence': float,     # Confidence 0-1
    'document_type': str,              # Predicted document type
    'doctype_confidence': float,       # Confidence 0-1
    'overall_confidence': float,       # Combined confidence 0-1
    'auto_classified': bool,           # True if high confidence
    'similar_documents': List[Dict],   # Similar past classifications
    'requires_interactive': bool,      # True if needs review
    'metadata': Dict                   # Original metadata
}
```

#### `train_models(training_data: Dict[str, List[Dict]]) -> Dict[str, str]`
Train classification models from training samples.

**Args:**
- `training_data`: Dictionary with 'sector', 'subsector', 'doctype' lists
- Each sample: `{'text': str, 'label': str}`

**Returns:**
- Dictionary of saved model paths

#### `load_models(model_paths: Dict[str, str]) -> bool`
Load pre-trained classification models.

#### `get_confidence_score(text: str, predicted_class: str, classifier_type: str) -> float`
Get confidence score for a specific prediction.

#### `learn_from_correction(text: str, corrected_classification: Dict) -> bool`
Store user correction for future learning.

#### `get_stats() -> Dict[str, Any]`
Get agent statistics and metrics.

### QdrantMemoryManager

#### `store_classification(text: str, classification: Dict, metadata: Dict, confidence: float) -> bool`
Store a classification decision in memory.

#### `search_similar(text: str, limit: int = 5, min_confidence: float = 0.7) -> List[Dict]`
Search for similar previously classified documents.

#### `update_classification(text: str, corrected_classification: Dict, confidence: float) -> bool`
Update/correct a previous classification.

#### `get_stats() -> Dict[str, Any]`
Get memory statistics.

## Configuration Options

### Classification Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `confidence_threshold` | 0.75 | Minimum confidence for auto-classification |
| `interactive_mode` | true | Enable interactive fallback |
| `auto_classify_high_confidence` | true | Auto-classify when confidence > threshold |

### Model Parameters

**Sector Classifier:**
- TF-IDF Features: 5000
- N-gram Range: 1-3
- Random Forest Estimators: 100
- Max Depth: 20

**Subsector Classifier:**
- TF-IDF Features: 5000
- N-gram Range: 1-3
- Random Forest Estimators: 100
- Max Depth: 20

**Document Type Classifier:**
- TF-IDF Features: 3000
- N-gram Range: 1-2
- Random Forest Estimators: 100
- Max Depth: 15

### Memory Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `qdrant_enabled` | false | Enable Qdrant memory |
| `qdrant_host` | localhost | Qdrant server host |
| `qdrant_port` | 6333 | Qdrant server port |
| `collection_name` | document_classifications | Collection name |
| `vector_size` | 384 | Embedding dimensions |
| `decision_tracking` | true | Track decisions |
| `learning_enabled` | true | Enable learning from corrections |

## Training Guidelines

### Minimum Training Data

For production use, aim for:
- **Sectors**: 50+ samples per sector (650+ total)
- **Subsectors**: 20+ samples per subsector (varies by sector)
- **Document Types**: 30+ samples per type (300+ total)

### Training Data Quality

Good training samples:
- Representative of actual documents
- Balanced across classes
- Include domain-specific terminology
- Vary in length and format

Poor training samples:
- Extremely short snippets
- Generic text without domain keywords
- Heavily imbalanced classes
- Duplicate or near-duplicate samples

### Iterative Training

```python
# 1. Initial training with labeled data
agent.train_models(initial_training_data)

# 2. Classify documents and get corrections
results = []
for doc in documents:
    result = agent.classify_document(doc)
    if not result['auto_classified']:
        # Get user correction
        corrected = interactive_classifier.get_correction(doc, result)
        agent.learn_from_correction(doc, corrected)
        results.append({'text': doc, 'label': corrected['sector']})

# 3. Retrain with additional corrected samples
agent.train_models({
    'sector': results,
    'subsector': subsector_results,
    'doctype': doctype_results
})
```

## Performance Tuning

### Adjust Confidence Threshold

```python
# More aggressive auto-classification
config['classification']['confidence_threshold'] = 0.65

# More conservative (require higher confidence)
config['classification']['confidence_threshold'] = 0.85
```

### Optimize Model Parameters

```python
# For larger datasets, increase features
vectorizer = TfidfVectorizer(
    max_features=10000,  # Increased from 5000
    ngram_range=(1, 4)   # Include 4-grams
)

# For faster training, reduce estimators
classifier = RandomForestClassifier(
    n_estimators=50,     # Reduced from 100
    n_jobs=-1           # Use all CPU cores
)
```

## Integration Examples

### With File Watcher Agent

```python
class DocumentPipeline:
    def __init__(self, config):
        self.classifier = ClassifierAgent('classifier', config)
        self.converter = ConverterAgent('converter', config)

    def process_document(self, filepath):
        # Convert to markdown
        markdown = self.converter.convert(filepath)

        # Classify
        classification = self.classifier.classify_document(
            markdown,
            metadata={'filepath': filepath}
        )

        # Handle based on confidence
        if classification['auto_classified']:
            return self.store_classified(classification)
        else:
            return self.request_user_input(classification)
```

### With Interactive Helper

```python
def classify_with_helper(agent, document, helper):
    """Classify with interactive helper fallback"""
    result = agent.classify_document(document)

    if result['requires_interactive']:
        # Show user the predictions
        print(f"Low confidence classification:")
        print(f"  Predicted: {result['sector']} / {result['subsector']}")
        print(f"  Confidence: {result['overall_confidence']:.3f}")

        # Get user input
        corrected = helper.get_classification(
            document,
            suggested=result
        )

        # Learn from correction
        agent.learn_from_correction(document, corrected)

        return corrected
    else:
        return result
```

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/test_classifier_agent.py -v

# Run specific test
python tests/test_classifier_agent.py TestClassifierAgent.test_classify_document

# Run with coverage
python -m pytest tests/test_classifier_agent.py --cov=agents.classifier_agent
```

Run the demo:

```bash
python examples/classifier_agent_demo.py
```

## Troubleshooting

### Models Not Loading

**Error**: `Models not found. Use train_models() to create them.`

**Solution**: Train models first:
```python
agent.train_models(training_data)
```

### Low Classification Accuracy

**Causes**:
1. Insufficient training data
2. Imbalanced classes
3. Poor quality training samples

**Solutions**:
1. Collect more representative samples
2. Use SMOTE or oversampling for minority classes
3. Review and clean training data
4. Tune model hyperparameters

### Memory Features Not Working

**Error**: `Qdrant memory disabled in config`

**Solution**:
1. Install Qdrant: `pip install qdrant-client sentence-transformers`
2. Start Qdrant server: `docker run -p 6333:6333 qdrant/qdrant`
3. Enable in config: `qdrant_enabled: true`

### Slow Classification

**Causes**:
1. Large model size
2. Many features in TF-IDF
3. Sentence transformer embeddings

**Solutions**:
1. Reduce `max_features` in vectorizers
2. Decrease Random Forest `n_estimators`
3. Use batch classification for multiple documents
4. Disable memory search for faster classification

## File Locations

```
/home/jim/2_OXOT_Projects_Dev/Import_to_neo4j/2_AEON_DT_AI_Project_Mckenney/
├── agents/
│   └── classifier_agent.py        # Main classifier implementation
├── utils/
│   └── qdrant_memory.py          # Memory manager
├── config/
│   ├── main_config.yaml          # Configuration
│   └── sectors.yaml              # Sector definitions
├── models/
│   └── classifiers/
│       ├── sector_classifier.pkl
│       ├── subsector_classifier.pkl
│       └── doctype_classifier.pkl
├── tests/
│   └── test_classifier_agent.py  # Unit tests
├── examples/
│   └── classifier_agent_demo.py  # Demo script
└── docs/
    └── ClassifierAgent_README.md # This file
```

## Future Enhancements

### Planned Features
1. **Neural Network Classifiers** - BERT-based models for better accuracy
2. **Active Learning** - Automatically identify uncertain documents for labeling
3. **Multi-label Classification** - Documents belonging to multiple sectors
4. **Hierarchical Classification** - Sector → Subsector cascading with dependencies
5. **Ensemble Models** - Combine multiple classifiers for better accuracy
6. **Online Learning** - Continuously update models with new data
7. **Feature Importance** - Explain classification decisions
8. **Confidence Calibration** - Better-calibrated probability estimates

### Research Directions
- Transfer learning from pre-trained models
- Few-shot learning for rare subsectors
- Semi-supervised learning with unlabeled data
- Multi-task learning across classification dimensions
- Adversarial robustness testing

## License

Part of the AEON Automated Document Ingestion System.

## Contact

For issues, questions, or contributions, please contact the AEON development team.
