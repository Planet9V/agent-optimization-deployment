# Phase 2 Detailed Implementation Plan (Weeks 21-36)

**File:** 03_PHASE2_ML_VALIDATION_v3.0_2025-11-19.md
**Created:** 2025-11-19
**Version:** v3.0
**Author:** AEON Strategic Planning Agent
**Purpose:** Detailed week-by-week implementation plan for Phase 2 (ML Enhancement & Validation)
**Status:** ACTIVE

---

## Phase 2 Overview

**Duration:** Weeks 21-36 (~4 months)
**Objective:** Implement machine learning models for threat prediction, optimize performance, and prepare for production deployment

**Success Criteria:**
- ML models achieving >85% threat prediction accuracy
- Healthcare-specific models validated by domain experts
- Production-ready ML infrastructure operational
- Complete validation and go-live approval

---

## Phase 2A: ML Foundation (Weeks 21-26)

### Week 21-22: Data Preparation & Feature Engineering

#### **Objectives**
- Extract and prepare training datasets from Neo4j
- Engineer graph-based and temporal features
- Create labeled datasets for supervised learning

#### **Detailed Tasks**

**Week 21, Day 1-2: Training Data Extraction**
- [ ] Extract graph data for ML training
  ```python
  # ml/data_extraction.py
  from neo4j import GraphDatabase
  from datetime import datetime, timedelta
  import pandas as pd
  import numpy as np

  class MLDataExtractor:
      """Extract and prepare data from Neo4j for ML training."""

      def __init__(self, driver: GraphDatabase.driver):
          self.driver = driver

      def extract_vulnerability_features(self, lookback_days: int = 365) -> pd.DataFrame:
          """Extract vulnerability features for threat prediction."""
          query = """
          MATCH (c:CVE)
          WHERE c.publishedDate > datetime() - duration({days: $lookback_days})

          OPTIONAL MATCH (c)<-[:EXPLOITS]-(e:Exploit)
          OPTIONAL MATCH (c)<-[:LISTED_AS]-(k:KEV)
          OPTIONAL MATCH (c)-[:AFFECTS]->(p:Product)
          OPTIONAL MATCH (c)-[:HAS_CWE]->(cwe:CWE)

          WITH c,
               count(DISTINCT e) as exploit_count,
               count(DISTINCT k) as kev_listed,
               count(DISTINCT p) as affected_products,
               collect(DISTINCT cwe.id) as cwe_ids,
               max(e.publicationDate) as latest_exploit_date

          RETURN c.id as cve_id,
                 c.baseScore as cvss_score,
                 c.publishedDate as published_date,
                 c.exploitabilityScore as exploitability,
                 c.impactScore as impact,
                 exploit_count,
                 CASE WHEN kev_listed > 0 THEN 1 ELSE 0 END as is_kev,
                 affected_products,
                 cwe_ids,
                 latest_exploit_date,
                 CASE
                   WHEN exploit_count > 0 THEN 1
                   ELSE 0
                 END as has_exploit
          """

          with self.driver.session() as session:
              result = session.run(query, lookback_days=lookback_days)
              data = pd.DataFrame([dict(record) for record in result])

          return data

      def extract_graph_features(self) -> pd.DataFrame:
          """Extract graph-based features using GDS algorithms."""
          query = """
          // Project graph for analysis
          CALL gds.graph.project(
              'vulnerability-network',
              ['CVE', 'Product', 'CWE', 'Exploit'],
              ['AFFECTS', 'HAS_CWE', 'EXPLOITS']
          )

          // Calculate PageRank centrality
          CALL gds.pageRank.stream('vulnerability-network')
          YIELD nodeId, score
          WITH gds.util.asNode(nodeId) AS node, score
          WHERE node:CVE

          // Calculate betweenness centrality
          CALL gds.betweenness.stream('vulnerability-network')
          YIELD nodeId, score as betweenness
          WITH node, score as pagerank, betweenness

          // Calculate community detection
          CALL gds.louvain.stream('vulnerability-network')
          YIELD nodeId, communityId
          WITH node, pagerank, betweenness, communityId

          RETURN node.id as cve_id,
                 pagerank,
                 betweenness,
                 communityId as community

          // Cleanup
          CALL gds.graph.drop('vulnerability-network')
          """

          with self.driver.session() as session:
              result = session.run(query)
              data = pd.DataFrame([dict(record) for record in result])

          return data
  ```

**Week 21, Day 3-5: Feature Engineering**
- [ ] Temporal feature extraction
  ```python
  # ml/feature_engineering.py
  from typing import List, Dict
  import pandas as pd
  import numpy as np
  from sklearn.preprocessing import StandardScaler, LabelEncoder

  class FeatureEngineer:
      """Engineer features for ML models."""

      def create_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
          """Create time-based features from vulnerability data."""
          df = df.copy()

          # Convert to datetime
          df['published_date'] = pd.to_datetime(df['published_date'])

          # Time since publication
          df['days_since_published'] = (datetime.now() - df['published_date']).dt.days

          # Publication velocity (exploits per day since publication)
          df['exploit_velocity'] = df['exploit_count'] / (df['days_since_published'] + 1)

          # Time to first exploit
          df['days_to_exploit'] = (
              (pd.to_datetime(df['latest_exploit_date']) - df['published_date']).dt.days
              .fillna(-1)  # -1 indicates no exploit
          )

          # Temporal bins
          df['publication_quarter'] = df['published_date'].dt.quarter
          df['publication_year'] = df['published_date'].dt.year
          df['publication_month'] = df['published_date'].dt.month
          df['publication_day_of_week'] = df['published_date'].dt.dayofweek

          return df

      def create_graph_features(self, df: pd.DataFrame, graph_data: pd.DataFrame) -> pd.DataFrame:
          """Merge graph-based features with vulnerability data."""
          # Merge with graph features
          df = df.merge(graph_data, on='cve_id', how='left')

          # Fill missing graph features with defaults
          df['pagerank'] = df['pagerank'].fillna(0)
          df['betweenness'] = df['betweenness'].fillna(0)
          df['community'] = df['community'].fillna(-1)

          return df

      def create_categorical_features(self, df: pd.DataFrame) -> pd.DataFrame:
          """Process categorical features."""
          df = df.copy()

          # CWE encoding (multi-label)
          df['cwe_count'] = df['cwe_ids'].apply(lambda x: len(x) if isinstance(x, list) else 0)

          # Extract top CWE categories
          all_cwes = [cwe for cwe_list in df['cwe_ids'] if isinstance(cwe_list, list) for cwe in cwe_list]
          top_cwes = pd.Series(all_cwes).value_counts().head(20).index.tolist()

          for cwe in top_cwes:
              df[f'has_cwe_{cwe}'] = df['cwe_ids'].apply(
                  lambda x: 1 if isinstance(x, list) and cwe in x else 0
              )

          return df

      def create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
          """Create interaction features between existing features."""
          df = df.copy()

          # CVSS and exploit interaction
          df['cvss_exploit_interaction'] = df['cvss_score'] * df['has_exploit']

          # Exploitability and impact interaction
          df['exploitability_impact'] = df['exploitability'] * df['impact']

          # Product scope risk
          df['product_scope_risk'] = df['affected_products'] * df['cvss_score']

          # KEV urgency score
          df['kev_urgency'] = df['is_kev'] * (10 - df['days_since_published'] / 30)

          return df

      def normalize_features(self, df: pd.DataFrame, feature_cols: List[str]) -> pd.DataFrame:
          """Normalize numerical features."""
          scaler = StandardScaler()
          df[feature_cols] = scaler.fit_transform(df[feature_cols])

          return df
  ```

**Week 22, Day 1-3: Label Creation for Supervised Learning**
- [ ] Create training labels
  ```python
  # ml/label_creation.py
  class LabelCreator:
      """Create labels for supervised learning tasks."""

      def create_exploit_likelihood_labels(self, df: pd.DataFrame) -> pd.DataFrame:
          """Create labels for exploit likelihood prediction."""
          df = df.copy()

          # Binary classification: Will exploit be published in next 90 days?
          df['exploit_within_90_days'] = (
              (df['days_to_exploit'] >= 0) & (df['days_to_exploit'] <= 90)
          ).astype(int)

          # Multi-class classification: Exploit timeframe
          def exploit_timeframe(days):
              if days < 0:
                  return 'no_exploit'
              elif days <= 30:
                  return 'immediate'  # <30 days
              elif days <= 90:
                  return 'short_term'  # 30-90 days
              elif days <= 180:
                  return 'medium_term'  # 90-180 days
              else:
                  return 'long_term'  # >180 days

          df['exploit_timeframe'] = df['days_to_exploit'].apply(exploit_timeframe)

          return df

      def create_severity_labels(self, df: pd.DataFrame) -> pd.DataFrame:
          """Create severity-based labels."""
          df = df.copy()

          # High-risk vulnerability (CVSS >= 7.0 AND has exploit)
          df['high_risk_vuln'] = (
              (df['cvss_score'] >= 7.0) & (df['has_exploit'] == 1)
          ).astype(int)

          # Critical priority (KEV listed OR high CVSS with exploit)
          df['critical_priority'] = (
              (df['is_kev'] == 1) |
              ((df['cvss_score'] >= 9.0) & (df['has_exploit'] == 1))
          ).astype(int)

          return df

      def create_healthcare_labels(self, df: pd.DataFrame, medical_device_df: pd.DataFrame) -> pd.DataFrame:
          """Create healthcare-specific labels."""
          # Join with medical device data
          df = df.merge(
              medical_device_df[['cve_id', 'affects_medical_device', 'device_criticality']],
              on='cve_id',
              how='left'
          )

          # Medical device risk
          df['medical_device_high_risk'] = (
              (df['affects_medical_device'] == 1) &
              (df['device_criticality'].isin(['HIGH', 'CRITICAL']))
          ).astype(int)

          # PHI breach likelihood
          df['phi_breach_risk'] = (
              (df['has_exploit'] == 1) &
              (df['affects_medical_device'] == 1)
          ).astype(int)

          return df
  ```

**Week 22, Day 4-5: Dataset Creation and Validation**
- [ ] Create train/validation/test splits
  ```python
  # ml/dataset_creation.py
  from sklearn.model_selection import train_test_split
  import joblib

  class DatasetCreator:
      """Create and manage ML datasets."""

      def create_datasets(self, df: pd.DataFrame, target_col: str,
                         test_size: float = 0.2, val_size: float = 0.1) -> Dict:
          """Create train/validation/test splits."""

          # Define feature columns (exclude target and metadata)
          exclude_cols = [
              target_col, 'cve_id', 'published_date', 'latest_exploit_date',
              'cwe_ids', 'exploit_timeframe'  # categorical labels
          ]
          feature_cols = [col for col in df.columns if col not in exclude_cols]

          X = df[feature_cols]
          y = df[target_col]

          # Split: 70% train, 10% validation, 20% test
          X_temp, X_test, y_temp, y_test = train_test_split(
              X, y, test_size=test_size, random_state=42, stratify=y
          )

          X_train, X_val, y_train, y_val = train_test_split(
              X_temp, y_temp,
              test_size=val_size/(1-test_size),  # Adjust for already split data
              random_state=42,
              stratify=y_temp
          )

          return {
              'X_train': X_train,
              'X_val': X_val,
              'X_test': X_test,
              'y_train': y_train,
              'y_val': y_val,
              'y_test': y_test,
              'feature_cols': feature_cols
          }

      def save_datasets(self, datasets: Dict, output_dir: str):
          """Save datasets to disk for reproducibility."""
          joblib.dump(datasets, f"{output_dir}/datasets.pkl")

      def validate_dataset_quality(self, datasets: Dict) -> Dict:
          """Validate dataset quality and balance."""
          metrics = {}

          # Check for class imbalance
          train_balance = datasets['y_train'].value_counts(normalize=True)
          metrics['train_class_balance'] = train_balance.to_dict()

          # Check for missing values
          metrics['missing_values'] = datasets['X_train'].isnull().sum().to_dict()

          # Check feature variance
          metrics['zero_variance_features'] = (
              datasets['X_train'].var() == 0
          ).sum()

          # Check feature correlation
          corr_matrix = datasets['X_train'].corr()
          high_corr = (corr_matrix.abs() > 0.95) & (corr_matrix != 1.0)
          metrics['highly_correlated_features'] = high_corr.sum().sum() // 2

          return metrics
  ```

#### **Deliverables**
- ✅ Training datasets extracted from Neo4j
- ✅ Comprehensive feature engineering pipeline
- ✅ Labeled datasets for multiple prediction tasks
- ✅ Train/validation/test splits created

#### **Quality Gates**
- Dataset size sufficient for training (>10,000 samples)
- Feature engineering pipeline validated
- Class balance acceptable (minority class >10%)
- No data leakage between train/test sets

---

### Week 23-24: Model Development & Initial Training

#### **Objectives**
- Develop baseline ML models
- Train initial models on prepared datasets
- Evaluate baseline performance

#### **Detailed Tasks**

**Week 23, Day 1-3: Baseline Model Development**
- [ ] Implement baseline models
  ```python
  # ml/models/baseline_models.py
  from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
  from xgboost import XGBClassifier
  from sklearn.linear_model import LogisticRegression
  from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
  import mlflow
  import mlflow.sklearn

  class BaselineModels:
      """Baseline ML models for threat prediction."""

      def __init__(self, random_state: int = 42):
          self.random_state = random_state
          self.models = self._initialize_models()

      def _initialize_models(self) -> Dict:
          """Initialize baseline models with default hyperparameters."""
          return {
              'logistic_regression': LogisticRegression(
                  max_iter=1000,
                  random_state=self.random_state
              ),
              'random_forest': RandomForestClassifier(
                  n_estimators=100,
                  max_depth=10,
                  min_samples_split=10,
                  random_state=self.random_state,
                  n_jobs=-1
              ),
              'gradient_boosting': GradientBoostingClassifier(
                  n_estimators=100,
                  max_depth=5,
                  learning_rate=0.1,
                  random_state=self.random_state
              ),
              'xgboost': XGBClassifier(
                  n_estimators=100,
                  max_depth=5,
                  learning_rate=0.1,
                  random_state=self.random_state,
                  use_label_encoder=False,
                  eval_metric='logloss'
              )
          }

      def train_model(self, model_name: str, X_train, y_train, X_val, y_val):
          """Train a specific model and log with MLflow."""
          model = self.models[model_name]

          with mlflow.start_run(run_name=f"baseline_{model_name}"):
              # Train model
              model.fit(X_train, y_train)

              # Validation predictions
              y_val_pred = model.predict(X_val)
              y_val_proba = model.predict_proba(X_val)[:, 1]

              # Calculate metrics
              metrics = {
                  'accuracy': (y_val_pred == y_val).mean(),
                  'roc_auc': roc_auc_score(y_val, y_val_proba)
              }

              # Log metrics
              mlflow.log_metrics(metrics)

              # Log model
              mlflow.sklearn.log_model(model, f"model_{model_name}")

              # Log classification report
              report = classification_report(y_val, y_val_pred, output_dict=True)
              mlflow.log_dict(report, "classification_report.json")

          return model, metrics

      def train_all_baselines(self, X_train, y_train, X_val, y_val) -> Dict:
          """Train all baseline models and compare performance."""
          results = {}

          for model_name in self.models.keys():
              print(f"Training {model_name}...")
              model, metrics = self.train_model(
                  model_name, X_train, y_train, X_val, y_val
              )
              results[model_name] = {
                  'model': model,
                  'metrics': metrics
              }

          # Find best model
          best_model_name = max(results.keys(), key=lambda k: results[k]['metrics']['roc_auc'])
          results['best_model'] = best_model_name

          return results
  ```

**Week 23, Day 4-5: Anomaly Detection Models**
- [ ] Implement unsupervised models
  ```python
  # ml/models/anomaly_detection.py
  from sklearn.ensemble import IsolationForest
  from sklearn.svm import OneClassSVM
  from sklearn.covariance import EllipticEnvelope
  from sklearn.metrics import precision_recall_curve, average_precision_score

  class AnomalyDetectionModels:
      """Anomaly detection for threat identification."""

      def __init__(self, contamination: float = 0.1):
          self.contamination = contamination
          self.models = self._initialize_models()

      def _initialize_models(self) -> Dict:
          """Initialize anomaly detection models."""
          return {
              'isolation_forest': IsolationForest(
                  contamination=self.contamination,
                  random_state=42,
                  n_jobs=-1
              ),
              'one_class_svm': OneClassSVM(
                  nu=self.contamination,
                  kernel='rbf',
                  gamma='auto'
              ),
              'elliptic_envelope': EllipticEnvelope(
                  contamination=self.contamination,
                  random_state=42
              )
          }

      def train_anomaly_detector(self, model_name: str, X_train, X_val, y_val):
          """Train anomaly detection model."""
          model = self.models[model_name]

          with mlflow.start_run(run_name=f"anomaly_{model_name}"):
              # Train on normal data (assumes majority class is normal)
              model.fit(X_train)

              # Predict anomalies on validation set
              y_val_pred = model.predict(X_val)
              # Convert to binary (1 = normal, -1 = anomaly)
              y_val_pred_binary = (y_val_pred == -1).astype(int)

              # Calculate metrics
              precision, recall, _ = precision_recall_curve(y_val, y_val_pred_binary)
              avg_precision = average_precision_score(y_val, y_val_pred_binary)

              metrics = {
                  'average_precision': avg_precision,
                  'anomaly_rate': (y_val_pred == -1).mean()
              }

              # Log metrics and model
              mlflow.log_metrics(metrics)
              mlflow.sklearn.log_model(model, f"anomaly_model_{model_name}")

          return model, metrics
  ```

**Week 24, Day 1-3: Vulnerability Prioritization Models**
- [ ] Ranking and prioritization models
  ```python
  # ml/models/prioritization.py
  from sklearn.ensemble import GradientBoostingRegressor
  from xgboost import XGBRanker
  import lightgbm as lgb

  class VulnerabilityPrioritizationModel:
      """Models for vulnerability prioritization and ranking."""

      def create_priority_score(self, df: pd.DataFrame) -> pd.DataFrame:
          """Create composite priority score from multiple factors."""
          df = df.copy()

          # Weighted priority score
          weights = {
              'cvss_score': 0.25,
              'has_exploit': 0.25,
              'is_kev': 0.20,
              'exploit_velocity': 0.15,
              'affected_products': 0.10,
              'pagerank': 0.05
          }

          df['priority_score'] = sum(
              df[feature] * weight
              for feature, weight in weights.items()
          )

          # Normalize to 0-100 scale
          df['priority_score'] = (
              (df['priority_score'] - df['priority_score'].min()) /
              (df['priority_score'].max() - df['priority_score'].min()) * 100
          )

          return df

      def train_ranking_model(self, X_train, y_train, X_val, y_val):
          """Train gradient boosting model for vulnerability ranking."""
          model = GradientBoostingRegressor(
              n_estimators=200,
              max_depth=5,
              learning_rate=0.05,
              random_state=42
          )

          with mlflow.start_run(run_name="vulnerability_ranking"):
              model.fit(X_train, y_train)

              # Validation predictions
              y_val_pred = model.predict(X_val)

              # Calculate metrics
              from sklearn.metrics import mean_absolute_error, r2_score
              metrics = {
                  'mae': mean_absolute_error(y_val, y_val_pred),
                  'r2_score': r2_score(y_val, y_val_pred)
              }

              mlflow.log_metrics(metrics)
              mlflow.sklearn.log_model(model, "ranking_model")

          return model, metrics
  ```

**Week 24, Day 4-5: Model Evaluation and Comparison**
- [ ] Comprehensive model evaluation
  ```python
  # ml/evaluation/model_evaluator.py
  from sklearn.metrics import (
      accuracy_score, precision_score, recall_score, f1_score,
      roc_auc_score, average_precision_score, confusion_matrix
  )
  import matplotlib.pyplot as plt
  import seaborn as sns

  class ModelEvaluator:
      """Comprehensive model evaluation and comparison."""

      def evaluate_classification_model(self, model, X_test, y_test) -> Dict:
          """Evaluate classification model on test set."""
          y_pred = model.predict(X_test)
          y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None

          metrics = {
              'accuracy': accuracy_score(y_test, y_pred),
              'precision': precision_score(y_test, y_pred, average='binary'),
              'recall': recall_score(y_test, y_pred, average='binary'),
              'f1_score': f1_score(y_test, y_pred, average='binary')
          }

          if y_proba is not None:
              metrics['roc_auc'] = roc_auc_score(y_test, y_proba)
              metrics['avg_precision'] = average_precision_score(y_test, y_proba)

          # Confusion matrix
          metrics['confusion_matrix'] = confusion_matrix(y_test, y_pred).tolist()

          return metrics

      def compare_models(self, models: Dict, X_test, y_test) -> pd.DataFrame:
          """Compare multiple models on test set."""
          comparison = []

          for model_name, model in models.items():
              metrics = self.evaluate_classification_model(model, X_test, y_test)
              metrics['model_name'] = model_name
              comparison.append(metrics)

          comparison_df = pd.DataFrame(comparison)
          comparison_df = comparison_df.sort_values('f1_score', ascending=False)

          return comparison_df

      def plot_roc_curves(self, models: Dict, X_test, y_test, output_path: str):
          """Plot ROC curves for model comparison."""
          from sklearn.metrics import roc_curve, auc

          plt.figure(figsize=(10, 8))

          for model_name, model in models.items():
              if hasattr(model, 'predict_proba'):
                  y_proba = model.predict_proba(X_test)[:, 1]
                  fpr, tpr, _ = roc_curve(y_test, y_proba)
                  roc_auc = auc(fpr, tpr)

                  plt.plot(fpr, tpr, label=f'{model_name} (AUC = {roc_auc:.3f})')

          plt.plot([0, 1], [0, 1], 'k--', label='Random')
          plt.xlabel('False Positive Rate')
          plt.ylabel('True Positive Rate')
          plt.title('ROC Curves - Model Comparison')
          plt.legend()
          plt.grid(True)
          plt.savefig(output_path)
          plt.close()
  ```

#### **Deliverables**
- ✅ Baseline classification models trained
- ✅ Anomaly detection models operational
- ✅ Vulnerability prioritization models implemented
- ✅ Comprehensive model evaluation completed

#### **Quality Gates**
- Baseline models achieving >75% accuracy
- ROC-AUC >0.80 for best model
- Model comparison report completed
- All models logged in MLflow

---

### Week 25-26: Neo4j Integration & Model Serving

#### **Objectives**
- Integrate ML models with Neo4j Graph Data Science
- Implement real-time prediction endpoints
- Configure model version management

#### **Detailed Tasks**

**Week 25, Day 1-3: Neo4j GDS Integration**
- [ ] Graph ML pipeline implementation
  ```python
  # ml/neo4j_integration.py
  from neo4j import GraphDatabase
  import joblib

  class Neo4jMLIntegration:
      """Integrate ML models with Neo4j Graph Data Science."""

      def __init__(self, driver: GraphDatabase.driver):
          self.driver = driver

      def create_gds_pipeline(self, pipeline_name: str = 'threat-prediction'):
          """Create Neo4j GDS ML pipeline."""
          query = f"""
          // Create node classification pipeline
          CALL gds.beta.pipeline.nodeClassification.create('{pipeline_name}')

          // Add node properties as features
          CALL gds.beta.pipeline.nodeClassification.addNodeProperty(
              '{pipeline_name}',
              'pageRank',
              {{
                  mutateProperty: 'pageRank'
              }}
          )

          CALL gds.beta.pipeline.nodeClassification.addNodeProperty(
              '{pipeline_name}',
              'degree',
              {{
                  mutateProperty: 'degree'
              }}
          )

          // Select features for training
          CALL gds.beta.pipeline.nodeClassification.selectFeatures(
              '{pipeline_name}',
              ['pageRank', 'degree', 'cvssScore', 'exploitabilityScore']
          )

          // Add Random Forest model
          CALL gds.beta.pipeline.nodeClassification.addRandomForest(
              '{pipeline_name}',
              {{
                  numberOfDecisionTrees: 100,
                  maxDepth: 10,
                  minSplitSize: 10
              }}
          )
          """

          with self.driver.session() as session:
              session.run(query)

      def train_gds_model(self, graph_name: str, pipeline_name: str,
                         target_property: str = 'hasExploit'):
          """Train ML model using Neo4j GDS."""
          query = f"""
          CALL gds.beta.pipeline.nodeClassification.train(
              '{graph_name}',
              {{
                  pipeline: '{pipeline_name}',
                  targetNodeLabels: ['CVE'],
                  modelName: '{pipeline_name}-model',
                  targetProperty: '{target_property}',
                  randomSeed: 42,
                  metrics: ['ACCURACY', 'F1_WEIGHTED', 'PRECISION', 'RECALL']
              }}
          )
          YIELD modelInfo, trainMillis
          RETURN modelInfo, trainMillis
          """

          with self.driver.session() as session:
              result = session.run(query)
              return dict(result.single())

      def predict_with_gds(self, graph_name: str, model_name: str):
          """Run predictions using trained GDS model."""
          query = f"""
          CALL gds.beta.pipeline.nodeClassification.predict.stream(
              '{graph_name}',
              {{
                  modelName: '{model_name}',
                  targetNodeLabels: ['CVE'],
                  includePredictedProbabilities: true
              }}
          )
          YIELD nodeId, predictedClass, predictedProbabilities
          WITH gds.util.asNode(nodeId) AS cve, predictedClass, predictedProbabilities

          RETURN cve.id as cve_id,
                 predictedClass as prediction,
                 predictedProbabilities[1] as exploit_probability
          ORDER BY exploit_probability DESC
          LIMIT 100
          """

          with self.driver.session() as session:
              result = session.run(query)
              return [dict(record) for record in result]

      def store_predictions_in_graph(self, predictions: List[Dict]):
          """Store ML predictions as node properties in Neo4j."""
          query = """
          UNWIND $predictions as pred
          MATCH (c:CVE {id: pred.cve_id})
          SET c.mlPrediction = pred.prediction,
              c.exploitProbability = pred.exploit_probability,
              c.predictionTimestamp = datetime()
          RETURN count(c) as updated_count
          """

          with self.driver.session() as session:
              result = session.run(query, predictions=predictions)
              return result.single()['updated_count']
  ```

**Week 25, Day 4-5: Real-Time Prediction Endpoints**
- [ ] FastAPI prediction service
  ```python
  # api/prediction_service.py
  from fastapi import FastAPI, HTTPException
  from pydantic import BaseModel
  from typing import List, Optional
  import joblib
  import numpy as np

  app = FastAPI(title="AEON Cyber DT ML Prediction API")

  # Load models at startup
  models = {}

  @app.on_event("startup")
  async def load_models():
      """Load ML models into memory."""
      models['exploit_prediction'] = joblib.load('models/exploit_prediction_model.pkl')
      models['priority_ranking'] = joblib.load('models/priority_ranking_model.pkl')
      models['anomaly_detection'] = joblib.load('models/anomaly_detection_model.pkl')

  class VulnerabilityInput(BaseModel):
      """Input schema for vulnerability prediction."""
      cve_id: str
      cvss_score: float
      exploitability_score: float
      impact_score: float
      days_since_published: int
      affected_products: int
      pagerank: Optional[float] = 0.0
      betweenness: Optional[float] = 0.0
      is_kev: int = 0

  class PredictionOutput(BaseModel):
      """Output schema for predictions."""
      cve_id: str
      exploit_probability: float
      priority_score: float
      is_anomaly: bool
      risk_level: str

  @app.post("/predict/exploit", response_model=PredictionOutput)
  async def predict_exploit(input_data: VulnerabilityInput):
      """Predict exploit likelihood for a vulnerability."""
      try:
          # Prepare features
          features = np.array([[
              input_data.cvss_score,
              input_data.exploitability_score,
              input_data.impact_score,
              input_data.days_since_published,
              input_data.affected_products,
              input_data.pagerank,
              input_data.betweenness,
              input_data.is_kev
          ]])

          # Get predictions from all models
          exploit_proba = models['exploit_prediction'].predict_proba(features)[0][1]
          priority_score = models['priority_ranking'].predict(features)[0]
          anomaly_pred = models['anomaly_detection'].predict(features)[0]

          # Determine risk level
          risk_level = (
              'CRITICAL' if exploit_proba > 0.8 and input_data.cvss_score >= 9.0
              else 'HIGH' if exploit_proba > 0.6
              else 'MEDIUM' if exploit_proba > 0.4
              else 'LOW'
          )

          return PredictionOutput(
              cve_id=input_data.cve_id,
              exploit_probability=float(exploit_proba),
              priority_score=float(priority_score),
              is_anomaly=bool(anomaly_pred == -1),
              risk_level=risk_level
          )

      except Exception as e:
          raise HTTPException(status_code=500, detail=str(e))

  @app.post("/predict/batch", response_model=List[PredictionOutput])
  async def predict_batch(input_data: List[VulnerabilityInput]):
      """Batch prediction for multiple vulnerabilities."""
      results = []
      for item in input_data:
          prediction = await predict_exploit(item)
          results.append(prediction)

      return results
  ```

**Week 26, Day 1-3: Model Version Management**
- [ ] MLflow model registry setup
  ```python
  # ml/model_registry.py
  import mlflow
  from mlflow.tracking import MlflowClient

  class ModelRegistry:
      """Manage ML model versions and deployments."""

      def __init__(self, tracking_uri: str = "http://localhost:5000"):
          mlflow.set_tracking_uri(tracking_uri)
          self.client = MlflowClient()

      def register_model(self, model_name: str, run_id: str,
                        description: str = "") -> str:
          """Register a model version in MLflow."""
          model_uri = f"runs:/{run_id}/model"

          model_details = mlflow.register_model(
              model_uri=model_uri,
              name=model_name
          )

          # Add description
          self.client.update_registered_model(
              name=model_name,
              description=description
          )

          return model_details.version

      def promote_model(self, model_name: str, version: str,
                       stage: str = "Production"):
          """Promote model version to production."""
          self.client.transition_model_version_stage(
              name=model_name,
              version=version,
              stage=stage
          )

      def get_production_model(self, model_name: str):
          """Get current production model."""
          versions = self.client.get_latest_versions(
              model_name,
              stages=["Production"]
          )

          if versions:
              return mlflow.sklearn.load_model(
                  f"models:/{model_name}/Production"
              )
          else:
              raise ValueError(f"No production model found for {model_name}")

      def rollback_model(self, model_name: str, previous_version: str):
          """Rollback to previous model version."""
          # Archive current production
          current_versions = self.client.get_latest_versions(
              model_name,
              stages=["Production"]
          )

          for version in current_versions:
              self.client.transition_model_version_stage(
                  name=model_name,
                  version=version.version,
                  stage="Archived"
              )

          # Promote previous version
          self.promote_model(model_name, previous_version, "Production")
  ```

**Week 26, Day 4-5: Batch Scoring Pipeline**
- [ ] Automated batch prediction pipeline
  ```python
  # pipelines/batch_scoring.py
  from apscheduler.schedulers.background import BackgroundScheduler
  from datetime import datetime
  import pandas as pd

  class BatchScoringPipeline:
      """Automated batch scoring for vulnerabilities."""

      def __init__(self, neo4j_driver, model_registry):
          self.driver = neo4j_driver
          self.registry = model_registry
          self.scheduler = BackgroundScheduler()

      def schedule_batch_scoring(self):
          """Schedule daily batch scoring."""
          self.scheduler.add_job(
              func=self.run_batch_scoring,
              trigger='cron',
              hour=3,
              minute=0,
              id='daily_batch_scoring'
          )

          self.scheduler.start()

      def run_batch_scoring(self):
          """Execute batch scoring on all unscored vulnerabilities."""
          # Extract unscored vulnerabilities
          query = """
          MATCH (c:CVE)
          WHERE c.mlPrediction IS NULL
             OR c.predictionTimestamp < datetime() - duration('P7D')

          OPTIONAL MATCH (c)<-[:EXPLOITS]-(e:Exploit)
          OPTIONAL MATCH (c)<-[:LISTED_AS]-(k:KEV)
          OPTIONAL MATCH (c)-[:AFFECTS]->(p:Product)

          WITH c,
               count(DISTINCT e) as exploit_count,
               CASE WHEN k IS NOT NULL THEN 1 ELSE 0 END as is_kev,
               count(DISTINCT p) as affected_products

          RETURN c.id as cve_id,
                 c.baseScore as cvss_score,
                 c.exploitabilityScore as exploitability_score,
                 c.impactScore as impact_score,
                 duration.between(c.publishedDate, datetime()).days as days_since_published,
                 exploit_count,
                 is_kev,
                 affected_products
          """

          with self.driver.session() as session:
              result = session.run(query)
              df = pd.DataFrame([dict(record) for record in result])

          if df.empty:
              print("No vulnerabilities to score")
              return

          # Load production models
          exploit_model = self.registry.get_production_model('exploit_prediction')
          priority_model = self.registry.get_production_model('priority_ranking')

          # Prepare features
          feature_cols = [
              'cvss_score', 'exploitability_score', 'impact_score',
              'days_since_published', 'exploit_count', 'is_kev', 'affected_products'
          ]
          X = df[feature_cols]

          # Generate predictions
          df['exploit_probability'] = exploit_model.predict_proba(X)[:, 1]
          df['priority_score'] = priority_model.predict(X)

          # Store predictions in Neo4j
          predictions = df[['cve_id', 'exploit_probability', 'priority_score']].to_dict('records')

          update_query = """
          UNWIND $predictions as pred
          MATCH (c:CVE {id: pred.cve_id})
          SET c.exploitProbability = pred.exploit_probability,
              c.priorityScore = pred.priority_score,
              c.predictionTimestamp = datetime()
          RETURN count(c) as updated
          """

          with self.driver.session() as session:
              result = session.run(update_query, predictions=predictions)
              updated_count = result.single()['updated']

          print(f"Batch scoring complete: {updated_count} vulnerabilities scored")
  ```

#### **Deliverables**
- ✅ Neo4j GDS ML pipeline operational
- ✅ Real-time prediction API deployed
- ✅ MLflow model registry configured
- ✅ Automated batch scoring pipeline running

#### **Quality Gates**
- GDS models training successfully
- Prediction API response time <100ms
- Model versioning functional
- Batch scoring processing >1000 CVEs/minute

---

## [Continued in next section due to length...]

## Version History

- **v3.0 (2025-11-19)**: Complete Phase 2 detailed plan with ML implementation
- **v2.0 (2025-11-15)**: Added healthcare-specific ML requirements
- **v1.0 (2025-11-10)**: Initial Phase 2 plan

---

**Document Control:**
- **Next Review Date**: Weekly during Phase 2 execution
- **Owner**: AEON ML Engineering Team
- **Distribution**: Project team, stakeholders
- **Classification**: Internal Use Only

*AEON Cyber Digital Twin v3.0 | Phase 2 ML Validation Plan | Evidence-Based | Production-Ready*
