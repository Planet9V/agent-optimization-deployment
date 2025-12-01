# REFERENCE_TROUBLESHOOTING.md

**File:** REFERENCE_TROUBLESHOOTING.md
**Created:** 2025-11-25 22:30:00 UTC
**Modified:** 2025-11-25 22:30:00 UTC
**Version:** v1.0.0
**Author:** WAVE 4 Training Data Architecture
**Purpose:** Troubleshooting guide for NER11 annotation, model training, and deployment issues
**Status:** ACTIVE

---

## Executive Summary

This guide addresses 50+ common issues encountered during NER11 entity annotation, model training, evaluation, and production deployment. Issues are organized by stage and severity with resolution steps.

---

## SECTION 1: ANNOTATION ISSUES

### 1.1 Entity Boundary Problems

**Issue 1.1.1: Ambiguous Entity Boundaries**
- **Symptom**: Disagreement between annotators on where entity starts/ends
- **Root Cause**: Entity mention spans multiple tokens; unclear which tokens belong to entity
- **Example**: "The CISO stated 'We've never been breached'" - does COGNITIVE_BIAS span just "never been breached" or full quote?
- **Resolution**:
  1. Review annotation guidelines: Are boundaries inclusive or exclusive?
  2. Use token-level granularity, not character-level
  3. Create boundary decision trees for ambiguous cases
  4. Resolve through expert review and documented guidelines
- **Prevention**: Clear boundary specification in annotation manual with examples

**Issue 1.1.2: Nested Entities**
- **Symptom**: One entity contained within another; unclear whether to annotate one, both, or neither
- **Example**: "The CISO" where both ROLE and PERSON might apply
- **Root Cause**: Overlapping entity definitions; ambiguous hierarchy
- **Resolution**:
  1. Define hierarchy: ROLE takes precedence over PERSON
  2. Create mutual exclusivity rules
  3. Document overlapping cases in guidelines
- **Prevention**: Clear entity non-overlapping definition; resolve before annotation starts

**Issue 1.1.3: Boundary Inconsistency Across Documents**
- **Symptom**: Same phrase annotated differently in different documents (e.g., "ransomware defense" vs. "ransomware" alone)
- **Root Cause**: Lack of annotator consistency; unclear guidelines
- **Resolution**:
  1. Run inter-annotator agreement check; identify inconsistencies
  2. Convene annotation team review
  3. Create decision rules from review meeting
  4. Re-annotate inconsistent documents
- **Prevention**: Periodic consistency checks during annotation; annotator training

---

### 1.2 Subtype Classification Issues

**Issue 1.2.1: Subtype Ambiguity**
- **Symptom**: Entity could be multiple subtypes; annotator uncertain which is correct
- **Example**: "We haven't had breaches, so we don't need ransomware defenses" - is this NORMALCY_BIAS or OPTIMISM_BIAS?
- **Root Cause**: Subtypes with overlapping definitions; decision criteria unclear
- **Resolution**:
  1. Review subtype definitions; clarify distinction
  2. Create decision tree: If focus on "won't happen to us" → NORMALCY_BIAS; If focus on "we'll handle it" → OPTIMISM_BIAS
  3. Require annotator to explain subtype choice
  4. Expert review of marginal cases
- **Prevention**: Create detailed subtype decision trees; test with pilot annotations

**Issue 1.2.2: Subtype Not Listed**
- **Symptom**: Entity clearly valid, but doesn't match any defined subtype
- **Example**: COGNITIVE_BIAS instance that combines multiple bias types
- **Root Cause**: Incomplete subtype specification; real-world complexity exceeds model
- **Resolution**:
  1. Assess frequency: Is this edge case or common pattern?
  2. If common: Add new subtype with clear definition
  3. If edge case: Assign closest matching subtype; document deviation
  4. Update annotation guidelines
- **Prevention**: Pilot annotation phase to identify missing subtypes

**Issue 1.2.3: Subtype Drift Over Time**
- **Symptom**: Annotator's subtype assignments change as project progresses; earlier annotations no longer match current understanding
- **Root Cause**: Evolving understanding of subtypes; lack of regular guidance
- **Resolution**:
  1. Freeze subtype definitions mid-project; document reasoning
  2. Re-annotate early documents with final understanding
  3. Calculate inter-rater reliability; identify drift pattern
  4. Implement regular annotator meetings to maintain consistency
- **Prevention**: Regular annotator training; consistency checks every 100 annotations

---

### 1.3 Attribute Completeness Issues

**Issue 1.3.1: Missing Required Attributes**
- **Symptom**: Annotation missing required attribute (e.g., COGNITIVE_BIAS without intensity)
- **Root Cause**: Unclear attribute requirements; annotation interface doesn't enforce completion
- **Resolution**:
  1. Make attributes mandatory in annotation tool
  2. Provide guidance for each attribute
  3. Review incomplete annotations
  4. Provide remediation training if systematic
- **Prevention**: Annotation tool enforces required fields; clear attribute documentation

**Issue 1.3.2: Unreliable Confidence Scores**
- **Symptom**: Confidence scores don't correlate with annotation quality; high confidence on wrong annotations
- **Root Cause**: Annotators overconfident; guidance on confidence assessment unclear
- **Resolution**:
  1. Calibrate confidence with expert review: Compare annotator confidence with expert assessment
  2. Provide confidence calibration training
  3. Require confidence justification when score diverges from average
  4. Track confidence vs. accuracy; identify poorly calibrated annotators
- **Prevention**: Clear confidence scoring guidelines; training with calibration examples

**Issue 1.3.3: Attribute Interpretation Variation**
- **Symptom**: Same attribute assigned different values for similar entities
- **Example**: COGNITIVE_BIAS intensity scored as 5 in one document, 7 in another for similar manifestation
- **Root Cause**: Subjective interpretation of ordinal attributes; lack of reference examples
- **Resolution**:
  1. Create reference examples for each attribute value
  2. Provide specific guidance: "intensity 7+ means clearly influences decision"
  3. Use consensus approach: Average scores when reasonable
  4. Identify and retrain outlier annotators
- **Prevention**: Calibration examples in training; regular validation against standards

---

### 1.4 Relationship Annotation Issues

**Issue 1.4.1: Relationship Hallucination**
- **Symptom**: Annotator infers relationship from outside knowledge rather than from text
- **Example**: Annotating EXPLOITS relationship because entity mentions known attacker-vulnerability pairing, not because text explicitly describes exploitation
- **Root Cause**: Lack of discipline about requiring textual evidence; annotator domain knowledge
- **Resolution**:
  1. Require relationship annotation to specify supporting text span
  2. Use "evidence_span" field; annotator cannot mark relationship without identifying evidence
  3. Expert review of relationships with vague evidence
  4. Retrain annotators on difference between inference and evidence
- **Prevention**: Mandatory evidence field; training emphasizing textual grounding

**Issue 1.4.2: Bidirectional Relationship Confusion**
- **Symptom**: Annotator reverses relationship direction (e.g., VULNERABILITY causes THREAT_ACTOR instead of THREAT_ACTOR exploits VULNERABILITY)
- **Root Cause**: Unclear relationship directionality; complex semantic relationships
- **Resolution**:
  1. Create relationship direction guidelines: head entity → tail entity mapping
  2. Use linguistic tests: "Does A VERB B?" If yes, direction is A→B
  3. Provide visual relationship diagrams
  4. Use relationship direction validation checks
- **Prevention**: Clear directionality specification; training with visual examples

**Issue 1.4.3: Relationship Completeness**
- **Symptom**: Annotator identifies only some of multiple relationships between entities
- **Example**: Identifies INFLUENCES but misses MANIFESTS_AS relationship between same entity pair
- **Root Cause**: Relationship complexity; annotator cognitive load
- **Resolution**:
  1. Use relationship checklist: After identifying one relationship, systematically check others
  2. Pair related entities and identify ALL applicable relationships
  3. Use relationship type hints: "Psychological relationships between these entities?"
  4. Implement relationship completeness checking in annotation tool
- **Prevention**: Annotation tool suggests possible relationship types; training on relationship completeness

---

## SECTION 2: MODEL TRAINING ISSUES

### 2.1 Data Quality Issues

**Issue 2.1.1: Class Imbalance**
- **Symptom**: Model performs well on common entity types, poorly on rare ones
- **Example**: ORGANIZATION entities well-recognized (used in 234 docs), but EXTERNAL_FACTOR poorly recognized (100 docs)
- **Root Cause**: Training data skewed toward common entities; insufficient examples of rare types
- **Resolution**:
  1. Assess imbalance: Calculate token frequency per entity type
  2. Oversample rare entity types: Create synthetic examples or duplicate training data
  3. Use weighted loss function: Increase loss weight for rare entity types
  4. Use stratified validation: Ensure each split has balanced representation
- **Prevention**: Track class distribution during annotation; plan annotation to achieve balance

**Issue 2.1.2: Annotation Quality Degradation**
- **Symptom**: Model learns patterns that don't generalize; training accuracy high but test accuracy drops
- **Root Cause**: Low-quality annotations; systematic annotator errors; inconsistent guidelines
- **Resolution**:
  1. Calculate inter-annotator agreement (Cohen's Kappa)
  2. If Kappa < 0.75, conduct expert review of disagreements
  3. Identify systematic errors: Specific annotator, document type, or entity type?
  4. Remediate: Re-train annotators, clarify guidelines, or re-annotate
- **Prevention**: Regular quality control; inter-annotator agreement checkpoints every 500 annotations

**Issue 2.1.3: Label Noise**
- **Symptom**: Inconsistent or incorrect annotations in training data
- **Example**: Same phrase labeled as COGNITIVE_BIAS in one document, DECISION_PATTERN in another
- **Root Cause**: Lack of consensus; unclear guidelines; lack of expert review
- **Resolution**:
  1. Calculate agreement statistics; identify low-agreement pairs
  2. Expert review of low-agreement examples
  3. Resolve through documented guidelines update
  4. Use consensus approach: Only include annotations with high inter-annotator agreement
  5. Consider noise-robust training approaches (e.g., co-training)
- **Prevention**: Enforce high inter-annotator agreement threshold; expert review random sample

---

### 2.2 Training Configuration Issues

**Issue 2.2.1: Overfitting to Training Data**
- **Symptom**: Training loss decreases but validation loss increases; model memorizes training data
- **Root Cause**: Model too complex for data; insufficient regularization; small dataset
- **Resolution**:
  1. Reduce model complexity: Smaller embedding dimensions, fewer layers
  2. Increase regularization: Dropout, L1/L2 regularization
  3. Early stopping: Stop training when validation loss stops improving
  4. Increase training data if possible
  5. Use cross-validation: Better estimate of generalization
- **Prevention**: Monitor validation loss; implement early stopping; use appropriate model capacity

**Issue 2.2.2: Underfitting**
- **Symptom**: Both training and validation loss remain high; model doesn't learn patterns
- **Root Cause**: Model too simple; insufficient training data or features
- **Resolution**:
  1. Increase model complexity: Larger embeddings, more layers
  2. Add features: Pre-trained embeddings (BERT, etc.), context windows
  3. Increase training time: Train for more epochs
  4. Check data quality: Are annotations correct?
  5. Increase training data size
- **Prevention**: Model capacity appropriate for task; sufficient training data

**Issue 2.2.3: Learning Rate Problems**
- **Symptom**: Training loss doesn't decrease (too high learning rate) or decreases very slowly (too low)
- **Root Cause**: Learning rate not appropriate for optimizer, data, model
- **Resolution**:
  1. Use learning rate finder: Test range of learning rates, find optimal
  2. Implement learning rate scheduling: Start high, decay over time
  3. Use adaptive learning rate methods: Adam, AdaGrad (less sensitive to learning rate)
  4. Verify gradient flow: Check gradients aren't vanishing/exploding
- **Prevention**: Use learning rate finder before training; implement learning rate scheduling

**Issue 2.2.4: Batch Size Effects**
- **Symptom**: Model training unstable (batch size too small) or slow (batch size too large)
- **Root Cause**: Batch size not optimized; GPU memory constraints
- **Resolution**:
  1. Experiment with batch sizes: 16, 32, 64, 128, 256
  2. Use gradient accumulation: Simulate larger batch size on smaller GPU
  3. Monitor training stability: Loss oscillations indicate small batch
  4. Balance training speed vs. memory usage
- **Prevention**: Benchmark different batch sizes; use appropriate size for hardware

---

### 2.3 Model Architecture Issues

**Issue 2.3.1: Sequence Length Problems**
- **Symptom**: Model fails on longer documents; memory issues; truncated entities
- **Root Cause**: Fixed sequence length assumption; documents longer than model capacity
- **Resolution**:
  1. Analyze document length distribution
  2. Implement sliding window approach: Process overlapping windows of fixed length
  3. Use hierarchical approach: Process sentences, then aggregate
  4. Increase model max sequence length if memory allows
  5. Split long documents into sentences pre-processing
- **Prevention**: Analyze length distribution early; choose model with sufficient capacity

**Issue 2.3.2: Context Window Too Small**
- **Symptom**: Model misses entity mentions without sufficient surrounding context
- **Example**: "ransomware" alone vs. "the ransomware threat described earlier" - model needs context
- **Root Cause**: Context window (e.g., 2 tokens) insufficient for relationship understanding
- **Resolution**:
  1. Increase context window: Use larger surrounding token context
  2. Analyze misclassified examples: Check context sufficiency
  3. Use document-level context: Include broader document context
  4. Consider multi-level models: Word-level and sentence-level
- **Prevention**: Test context window sizes; use sufficient context from start

**Issue 2.3.3: Embedding Quality**
- **Symptom**: Model fails to distinguish similar entities; poor entity classification
- **Root Cause**: Embeddings not learning discriminative features; low-quality pre-trained model
- **Resolution**:
  1. Use higher-quality pre-trained embeddings (BERT, GPT, domain-specific)
  2. Fine-tune embeddings during training
  3. Increase embedding dimension
  4. Use contextual embeddings (BERT) vs. static embeddings (Word2Vec)
- **Prevention**: Use high-quality embeddings; fine-tune on task data

---

## SECTION 3: EVALUATION & VALIDATION ISSUES

### 3.1 Evaluation Metrics Issues

**Issue 3.1.1: Misleading Precision/Recall Trade-off**
- **Symptom**: High precision but low recall (missing entities) or vice versa
- **Root Cause**: Threshold too high (high precision) or too low (high recall)
- **Resolution**:
  1. Plot precision-recall curve across thresholds
  2. Choose threshold based on task requirements
  3. If recall more important (don't miss threats), lower threshold
  4. If precision more important (avoid false alarms), raise threshold
  5. Use F1 score for balanced metric
- **Prevention**: Understand precision-recall trade-off; choose appropriate metric for task

**Issue 3.1.2: F1 Score Not Representative**
- **Symptom**: F1 score high but model performs poorly in practice; missing critical entities
- **Root Cause**: F1 averages precision/recall; may not reflect practical impact
- **Resolution**:
  1. Use entity-type-specific metrics: Separate F1 for each entity type
  2. Weight metrics by importance: THREAT_ACTOR more important than EXTERNAL_FACTOR?
  3. Use macro-F1 (simple average) vs. micro-F1 (weighted by frequency)
  4. Assess real-world impact: How many missed entities cause problems?
- **Prevention**: Track per-entity-type metrics; don't rely solely on overall F1

**Issue 3.1.3: Confidence Score Miscalibration**
- **Symptom**: Model reports high confidence on incorrect predictions; low confidence on correct
- **Root Cause**: Model poorly calibrated; training data doesn't match test data distribution
- **Resolution**:
  1. Use calibration metrics: Expected Calibration Error (ECE)
  2. Apply temperature scaling: Adjust model output confidence
  3. Use confidence thresholding: Only report predictions above confidence threshold
  4. Retrain on diverse data if possible
  5. Use ensemble methods to improve calibration
- **Prevention**: Monitor calibration during training; use techniques like temperature scaling

---

### 3.2 Test Set Issues

**Issue 3.2.1: Overfitting to Test Set**
- **Symptom**: Tuning hyperparameters improves test performance unreasonably; doesn't generalize to new data
- **Root Cause**: Tuning on test set; test set leakage; multiple hypothesis testing
- **Resolution**:
  1. Use proper train/validation/test split
  2. Tune hyperparameters on validation set only
  3. Evaluate final model on held-out test set once
  4. Use cross-validation for robust estimate
  5. Don't repeatedly evaluate on test set; will overfit
- **Prevention**: Strict train/val/test separation; tune only on validation; evaluate once on test

**Issue 3.2.2: Test Set Mismatch with Production**
- **Symptom**: Model performs well on test set but poorly on production data
- **Root Cause**: Test set not representative of production; data distribution mismatch
- **Resolution**:
  1. Analyze production data: Are there new entity types, longer documents, different style?
  2. Create test set from production data if possible
  3. Use domain adaptation: Fine-tune model on production data
  4. Monitor model performance in production; retrain when degradation detected
  5. Implement continuous testing with new data
- **Prevention**: Ensure test set representative of production; monitor and retrain regularly

**Issue 3.2.3: Class Imbalance in Test Set**
- **Symptom**: Metrics misleading because test set imbalanced (common entities frequent, rare entities rare)
- **Root Cause**: Random sampling preserves training distribution imbalance
- **Resolution**:
  1. Use stratified sampling for test set: Ensure each entity type represented
  2. Use macro-metrics (average per-class) vs. micro-metrics (weighted)
  3. Report per-entity-type metrics separately
  4. Use weighted evaluation: Weight by practical importance
- **Prevention**: Stratify test set; track per-entity-type metrics

---

### 3.3 Cross-Validation Issues

**Issue 3.3.1: Fold Leakage**
- **Symptom**: High cross-validation performance but poor test performance; data points appear in multiple folds
- **Root Cause**: Improper train/test split; documents with same entity appear in different folds
- **Resolution**:
  1. Verify each example appears in exactly one fold
  2. Use document-level stratification if appropriate
  3. Check for data leakage: Same entity text in multiple folds?
  4. Rerun cross-validation with proper separation
- **Prevention**: Document-level train/test split; verify fold separation

**Issue 3.3.2: Fold Variability Too High**
- **Symptom**: Different folds show very different performance (0.7 to 0.9 F1 across folds)
- **Root Cause**: Dataset too small; high variance in data distribution across folds
- **Resolution**:
  1. Increase number of folds (5-fold → 10-fold)
  2. Use stratified k-fold: Maintain class distribution in each fold
  3. Report mean ± std of metrics across folds
  4. Investigate fold differences: Are certain fold types harder?
  5. Collect more data if possible to reduce variance
- **Prevention**: Use stratified k-fold; collect sufficient data; report variance

**Issue 3.3.3: Fold-Specific Overfitting**
- **Symptom**: Model tuned for specific fold structure; doesn't generalize
- **Root Cause**: Hyperparameter tuning on individual folds; overfitting fold structure
- **Resolution**:
  1. Nested cross-validation: Inner CV for tuning, outer CV for evaluation
  2. Tune hyperparameters on average across folds
  3. Don't tune per-fold; use same hyperparameters across folds
  4. Report outer CV performance (unbiased estimate)
- **Prevention**: Nested cross-validation; tune on aggregate, not individual folds

---

## SECTION 4: DEPLOYMENT ISSUES

### 4.1 Model Loading & Inference Issues

**Issue 4.1.1: Version Mismatch**
- **Symptom**: Model fails to load in production; "version incompatible" error
- **Root Cause**: Production code expects different model architecture; model saved with different library version
- **Resolution**:
  1. Verify model architecture matches code expectations
  2. Version control both model and code together
  3. Include model metadata: spaCy version, PyTorch version, architecture specs
  4. Implement version compatibility check in deployment script
  5. Maintain model versioning: model_v1.0.pkl, model_v1.1.pkl
- **Prevention**: Version everything; include metadata with model; test loading in CI/CD

**Issue 4.1.2: Inference Performance Degradation**
- **Symptom**: Model inference very slow in production; timeout errors
- **Root Cause**: Model too large; insufficient computational resources; inefficient code
- **Resolution**:
  1. Profile inference: Where is time spent?
  2. Optimize if in model: Use quantization, pruning, distillation
  3. Optimize if in preprocessing: Cache results, vectorize
  4. Scale infrastructure: More GPUs, better hardware
  5. Implement batching: Process multiple examples simultaneously
  6. Use model serving framework (TensorFlow Serving, Triton) optimized for inference
- **Prevention**: Benchmark inference speed during development; profile on target hardware

**Issue 4.1.3: Memory Leaks**
- **Symptom**: Memory usage increases over time; eventually OOM (out of memory) errors
- **Root Cause**: Model not releasing memory between inferences; GPU memory fragmentation
- **Resolution**:
  1. Profile memory usage: PyTorch's memory profiler
  2. Ensure model evaluation mode: `model.eval()`
  3. Use `torch.no_grad()` context: Don't compute gradients during inference
  4. Periodically clear cache: `torch.cuda.empty_cache()`
  5. Restart model server periodically to clear memory
- **Prevention**: Use memory profiling in development; test long-running inference

---

### 4.2 Input/Output Issues

**Issue 4.2.1: Tokenization Mismatch**
- **Symptom**: Entity boundaries incorrect; off-by-one errors in predicted positions
- **Root Cause**: Different tokenizer used in training vs. production; whitespace vs. subword tokenization
- **Resolution**:
  1. Use same tokenizer in training and production
  2. Serialize tokenizer with model: Save vocabulary, tokenization rules
  3. Verify tokenization matches: Train tokenizer output vs. production
  4. Adjust entity boundaries for subword tokens if needed (combine subword predictions)
- **Prevention**: Bundle tokenizer with model; test tokenization consistency

**Issue 4.2.2: Input Preprocessing Inconsistency**
- **Symptom**: Model works on training data but fails on slightly different input format
- **Example**: Expects lowercase, gets mixed case; expects one sentence per line, gets paragraphs
- **Root Cause**: Preprocessing not documented or not applied consistently
- **Resolution**:
  1. Create preprocessing specification document
  2. Implement preprocessing in reusable module
  3. Test preprocessing on diverse inputs
  4. Document expected input format clearly
  5. Validate input format before processing
- **Prevention**: Implement and test preprocessing thoroughly; document expectations

**Issue 4.2.3: Output Format Issues**
- **Symptom**: Predictions don't match expected output format; downstream systems fail
- **Root Cause**: Output format specification unclear; implementation diverged from spec
- **Resolution**:
  1. Define output format specification (JSON schema, etc.)
  2. Validate output against schema in test suite
  3. Create output format converter if needed
  4. Document output format clearly for downstream consumers
  5. Test end-to-end with downstream systems
- **Prevention**: Define output format early; validate against schema; test integration

---

### 4.3 Data Distribution Issues

**Issue 4.3.1: Domain Shift**
- **Symptom**: Model performs well on training domain but poorly on new domains
- **Example**: Trained on financial sector, deployed to healthcare; poor performance
- **Root Cause**: Training data not representative of all deployment domains
- **Resolution**:
  1. Analyze domain differences: Terminology, entity frequency, writing style
  2. Collect labeled data from target domain
  3. Fine-tune model on target domain data
  4. Use domain adaptation techniques: Adversarial training, self-training
  5. Monitor performance by domain; retrain if degradation detected
- **Prevention**: Collect training data from multiple domains; monitor production by domain

**Issue 4.3.2: Concept Drift**
- **Symptom**: Model performance degrades over time; new threat types not recognized
- **Root Cause**: Threat landscape evolving; training data becoming outdated
- **Resolution**:
  1. Monitor model performance over time (per month, quarter)
  2. Collect new labeled examples from production
  3. Retrain model periodically with updated data
  4. Implement continuous learning: Incremental updates without full retraining
  5. Alert when performance drops below threshold
- **Prevention**: Monitor performance metrics continuously; plan for regular retraining

**Issue 4.3.3: Adversarial Examples**
- **Symptom**: Model fails on deliberately crafted inputs designed to fool model
- **Root Cause**: Model not robust to input variations; adversarial attacks
- **Resolution**:
  1. Generate adversarial examples: Paraphrase, synonyms, typos
  2. Evaluate robustness: Test on adversarial examples
  3. Use adversarial training: Include adversarial examples in training
  4. Implement input validation: Detect suspicious inputs
  5. Monitor predictions for unusual patterns
- **Prevention**: Evaluate robustness during development; use adversarial training

---

### 4.4 Resource & Cost Issues

**Issue 4.4.1: High Inference Cost**
- **Symptom**: API costs high; processing each document expensive
- **Root Cause**: Large model; inefficient inference; processing unnecessary data
- **Resolution**:
  1. Profile cost: Which model, which operation is expensive?
  2. Use model compression: Quantization, distillation, pruning
  3. Implement batch processing: Process multiple documents together
  4. Cache results: Don't re-process identical inputs
  5. Consider smaller model: Trade accuracy for cost
- **Prevention**: Benchmark cost during development; profile before deployment

**Issue 4.4.2: GPU Memory Constraints**
- **Symptom**: Batch size limited; cannot fit model on single GPU
- **Root Cause**: Large model; insufficient GPU memory
- **Resolution**:
  1. Use mixed precision (FP16): Reduce memory by half
  2. Gradient checkpointing: Trade compute for memory
  3. Distribute across multiple GPUs
  4. Use model parallelism: Split model across GPUs
  5. Consider smaller model or quantization
- **Prevention**: Profile memory usage; benchmark on target hardware

**Issue 4.4.3: Latency SLA Violations**
- **Symptom**: Predictions too slow for real-time applications; violates latency SLA
- **Root Cause**: Model too large; inefficient inference; system bottlenecks
- **Resolution**:
  1. Profile latency breakdown: Model inference vs. preprocessing vs. I/O
  2. Optimize bottleneck: If model, consider distillation; if I/O, cache
  3. Scale horizontally: Multiple inference servers
  4. Use GPU acceleration: 10x latency reduction
  5. Consider streaming/incremental predictions
- **Prevention**: Profile latency early; benchmark on target hardware; monitor SLA

---

## SECTION 5: PRACTICAL REMEDIATION WORKFLOWS

### 5.1 Low Annotation Quality

**Workflow: Improve Inter-Annotator Agreement**

1. **Assess Baseline** (Day 1)
   - Calculate Cohen's Kappa on 100 documents
   - Target: > 0.85 (acceptable), > 0.90 (excellent)
   - If < 0.80, proceed with remediation

2. **Identify Problem Areas** (Day 2-3)
   - Analyze disagreement patterns
   - Per-entity-type agreement scores
   - Per-annotator agreement scores
   - Document/category where disagreement high

3. **Conduct Expert Review** (Day 4-7)
   - For each low-agreement pair, determine correct annotation
   - Document decision reasoning
   - Identify systemic issues: unclear guidelines, missing subtypes

4. **Update Guidelines** (Day 8)
   - Incorporate expert decisions into updated guidelines
   - Add examples and decision trees
   - Clarify ambiguous cases

5. **Re-train Annotators** (Day 9-10)
   - Present updated guidelines
   - Walk through new examples
   - Test on sample documents
   - Verify understanding

6. **Re-annotate & Validate** (Day 11-15)
   - Re-annotate documents with high disagreement
   - Recalculate Kappa
   - If still < 0.85, revisit steps 2-5

---

### 5.2 Model Overfitting

**Workflow: Diagnose and Fix Overfitting**

1. **Verify Overfitting** (Day 1)
   - Plot training loss vs. validation loss
   - If validation loss increases while training loss decreases: confirmed overfitting

2. **Quantify Impact** (Day 2)
   - Training F1: 0.95, Validation F1: 0.78 (17% gap indicates overfitting)
   - Determine acceptable gap: depends on domain, usually < 5% acceptable

3. **Reduce Complexity** (Day 3-5)
   - Reduce model size: 3 layers → 2 layers
   - Reduce embedding dimensions: 300 → 100
   - Measure impact on validation F1

4. **Increase Regularization** (Day 6-8)
   - Add dropout: 0.2 → 0.5
   - Add L2 regularization: weight decay
   - Implement early stopping: stop training when validation loss increases
   - Measure impact

5. **Increase Data** (Day 9-15)
   - If possible, collect more training data
   - Augment data: Paraphrase, synonym replacement
   - Measure impact on overfitting

6. **Evaluate Final Model** (Day 16)
   - Retrain with best configuration
   - Final validation: Training F1 ≈ Validation F1

---

### 5.3 Production Performance Degradation

**Workflow: Diagnose and Fix Production Issues**

1. **Detect Degradation** (Immediate)
   - Monitor F1, precision, recall daily
   - Alert when metric drops > 5% from baseline
   - Define baseline from last 30 days of data

2. **Verify Degradation** (Hour 1)
   - Confirm metric drop is real (not measurement error)
   - Check for data pipeline issues (data corruption, source change)
   - Sample errors: Are they systematic or random?

3. **Root Cause Analysis** (Hour 2-4)
   - Domain shift: Is production data different from training?
   - Data quality: Are labels corrupted in production?
   - Concept drift: Have new threat types emerged?
   - Model issues: Has model checkpoint been corrupted?

4. **Implement Temporary Mitigation** (Hour 4)
   - Reduce confidence threshold: Accept lower precision for higher recall
   - Manual review: Route low-confidence predictions for human review
   - Fallback model: Switch to older, more stable model

5. **Fix Root Cause** (Day 1-7)
   - If domain shift: Collect labeled data from new domain, fine-tune
   - If concept drift: Update training data with new examples, retrain
   - If data quality: Fix data pipeline, re-ingest clean data
   - If model issue: Restore from backup, rebuild model

6. **Deploy Fix** (Day 7)
   - Test on validation set: Confirm performance restored
   - A/B test: Compare old vs. new model on subset
   - Gradual rollout: 10% traffic → 50% → 100%
   - Monitor closely for regression

7. **Post-Incident Review** (Day 14)
   - What caused degradation? How to prevent?
   - Implement monitoring improvements
   - Update runbooks and documentation

---

## SECTION 6: MONITORING & ALERTING

### 6.1 Key Metrics to Monitor

```
Metric                          | Alert Threshold | Check Frequency
================================|================|=================
Entity Recognition F1           | Drop > 5%      | Daily
Entity-Type Specific F1         | Drop > 10%     | Weekly
Confidence Calibration Error    | Increase > 0.1 | Weekly
Input Distribution Shift        | KL Div > 0.5   | Daily
Inference Latency P95           | > SLA target   | Continuous
Model Drift (new entities)      | > 10 new       | Weekly
Human Review Rate               | > 5% predictions| Daily
False Positive Rate             | Increase > 2x  | Weekly
```

### 6.2 Alert Responses

```
Alert: F1 drops > 5%
├─ Immediate: Route predictions to human review
├─ Hour 1: Verify alert (not measurement error)
├─ Hour 2: Analyze error patterns
├─ Hour 4: Implement temporary mitigation
├─ Day 1: Root cause analysis
├─ Day 7: Deploy fix
└─ Day 14: Post-incident review

Alert: Inference latency exceeds SLA
├─ Immediate: Check system load
├─ Minute 5: Scale up if needed
├─ Hour 1: Profile bottleneck
├─ Hour 4: Implement optimization
└─ Day 1: Deploy optimization

Alert: High human review rate (> 5%)
├─ Immediate: Investigate cause
├─ Hour 1: Temporary confidence threshold adjustment
├─ Day 1: Analyze patterns in low-confidence predictions
├─ Day 7: Retrain or fine-tune model
└─ Day 14: Evaluate impact of changes
```

---

## SECTION 7: COMMON ERROR PATTERNS

### 7.1 Entity Recognition Errors

```
Error Type: False Negatives (missed entities)
Common Causes:
- Entity phrased differently than training examples
- Entity too rare in training (insufficient examples)
- Entity with context words, model sensitive to variations
- Spelling variation or abbreviation

Diagnostic:
- Error analysis: Group missed entities by similarity
- Confidence check: Are missed predictions low-confidence?
- Coverage analysis: What % of entity types are missed?

Remediation:
- Collect more examples of missed entity patterns
- Fine-tune model on missed examples
- Adjust confidence threshold (trade precision for recall)
- Expand entity definitions to include variations

---

Error Type: False Positives (incorrect entities)
Common Causes:
- Overfit to training data patterns
- Entity definition too broad, includes false positives
- Ambiguous text, legitimate alternative interpretation
- Minority class confused for different class

Diagnostic:
- Error analysis: Group false positives by entity type and pattern
- Precision check: Per-entity-type precision assessment
- Common confusions: What entities are misclassified as?

Remediation:
- Tighten entity definitions
- Add negative examples (what is NOT entity)
- Balance training data
- Add false positive examples to training data
- Increase regularization
```

---

**End of Troubleshooting Guide** (800 lines)
