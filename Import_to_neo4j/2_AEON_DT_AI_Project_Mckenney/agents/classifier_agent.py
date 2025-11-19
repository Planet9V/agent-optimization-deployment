"""
Classifier Agent - ML-based Document Classification
Classifies documents by sector, subsector, and document type using sklearn models
"""

import os
import pickle
import yaml
from typing import Dict, Any, Optional, List, Tuple
import logging
from pathlib import Path
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from agents.base_agent import BaseAgent
from utils.qdrant_memory import QdrantMemoryManager


class ClassifierAgent(BaseAgent):
    """
    ML-based document classifier using Random Forest and TF-IDF

    Features:
    - Multi-class classification (sector, subsector, document_type)
    - Confidence-based auto-classification
    - Interactive fallback for low-confidence cases
    - Integration with Qdrant for learning from corrections
    - Model training and persistence
    """

    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize classifier agent

        Args:
            name: Agent name
            config: Configuration dictionary
        """
        # Initialize model paths BEFORE calling super().__init__()
        # because _setup() needs them
        self.model_paths = config.get('classification', {}).get('model_paths', {})
        self.sector_model_path = self.model_paths.get('sector', 'models/classifiers/sector_classifier.pkl')
        self.subsector_model_path = self.model_paths.get('subsector', 'models/classifiers/subsector_classifier.pkl')
        self.doctype_model_path = self.model_paths.get('doctype', 'models/classifiers/doctype_classifier.pkl')

        # Classification settings
        self.confidence_threshold = config.get('classification', {}).get('confidence_threshold', 0.75)
        self.interactive_mode = config.get('classification', {}).get('interactive_mode', True)
        self.auto_classify = config.get('classification', {}).get('auto_classify_high_confidence', True)

        super().__init__(name, config)

        # ML models
        self.sector_vectorizer: Optional[TfidfVectorizer] = None
        self.sector_classifier: Optional[RandomForestClassifier] = None
        self.sector_encoder: Optional[LabelEncoder] = None

        self.subsector_vectorizer: Optional[TfidfVectorizer] = None
        self.subsector_classifier: Optional[RandomForestClassifier] = None
        self.subsector_encoder: Optional[LabelEncoder] = None

        self.doctype_vectorizer: Optional[TfidfVectorizer] = None
        self.doctype_classifier: Optional[RandomForestClassifier] = None
        self.doctype_encoder: Optional[LabelEncoder] = None

        # Load sector configurations
        self.sectors_config = self._load_sectors_config()

        # Initialize memory manager
        memory_config = config.get('memory', {})
        self.memory_manager = QdrantMemoryManager(memory_config)

        # Statistics
        self.stats = {
            'total_classified': 0,
            'auto_classified': 0,
            'interactive_classified': 0,
            'corrections_learned': 0
        }

    def _setup(self):
        """Agent-specific setup"""
        self.logger.info("Setting up ClassifierAgent")

        # Create model directories
        os.makedirs(os.path.dirname(self.sector_model_path), exist_ok=True)

        # Load models if they exist
        if self._models_exist():
            self.load_models({
                'sector': self.sector_model_path,
                'subsector': self.subsector_model_path,
                'doctype': self.doctype_model_path
            })
        else:
            self.logger.warning("Models not found. Use train_models() to create them.")

    def _load_sectors_config(self) -> Dict[str, Any]:
        """Load sectors configuration from YAML"""
        config_path = Path(self.config.get('config_dir', 'config')) / 'sectors.yaml'

        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Failed to load sectors config: {e}")
            return {'sectors': {}}

    def _models_exist(self) -> bool:
        """Check if all model files exist"""
        return (
            os.path.exists(self.sector_model_path) and
            os.path.exists(self.subsector_model_path) and
            os.path.exists(self.doctype_model_path)
        )

    def classify_document(
        self,
        markdown_content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Classify a document by sector, subsector, and document type

        Args:
            markdown_content: Document content in markdown format
            metadata: Optional metadata (filename, path, etc.)

        Returns:
            Classification result with confidence scores
        """
        self.logger.info("Classifying document")

        # Check memory for similar documents
        similar_docs = self.memory_manager.search_similar(
            text=markdown_content,
            limit=3,
            min_confidence=0.8
        )

        if similar_docs:
            self.logger.info(f"Found {len(similar_docs)} similar previously classified documents")
            # Use most similar as hint
            best_match = similar_docs[0]
            self.logger.info(f"Best match similarity: {best_match['similarity_score']:.3f}")

        # Classify sector
        sector_result = self._classify_sector(markdown_content)

        # Classify subsector (within identified sector)
        subsector_result = self._classify_subsector(
            markdown_content,
            sector=sector_result['predicted']
        )

        # Classify document type
        doctype_result = self._classify_doctype(markdown_content)

        # Calculate overall confidence
        overall_confidence = (
            sector_result['confidence'] * 0.4 +
            subsector_result['confidence'] * 0.4 +
            doctype_result['confidence'] * 0.2
        )

        result = {
            'sector': sector_result['predicted'],
            'sector_confidence': sector_result['confidence'],
            'subsector': subsector_result['predicted'],
            'subsector_confidence': subsector_result['confidence'],
            'document_type': doctype_result['predicted'],
            'doctype_confidence': doctype_result['confidence'],
            'overall_confidence': overall_confidence,
            'auto_classified': overall_confidence >= self.confidence_threshold,
            'similar_documents': similar_docs[:2] if similar_docs else [],
            'metadata': metadata or {}
        }

        # Auto-classify or trigger interactive mode
        if self.auto_classify and result['auto_classified']:
            self.logger.info(f"Auto-classified with confidence {overall_confidence:.3f}")
            self.stats['auto_classified'] += 1

            # Store in memory
            self.memory_manager.store_classification(
                text=markdown_content,
                classification={
                    'sector': result['sector'],
                    'subsector': result['subsector'],
                    'document_type': result['document_type']
                },
                metadata=metadata,
                confidence=overall_confidence
            )
        else:
            self.logger.info(f"Low confidence ({overall_confidence:.3f}), interactive mode recommended")
            result['requires_interactive'] = True
            self.stats['interactive_classified'] += 1

        self.stats['total_classified'] += 1
        return result

    def _classify_sector(self, text: str) -> Dict[str, Any]:
        """Classify document sector"""
        if not self.sector_classifier or not self.sector_vectorizer:
            return {'predicted': 'unknown', 'confidence': 0.0, 'probabilities': {}}

        # Vectorize text
        text_vector = self.sector_vectorizer.transform([text])

        # Predict
        prediction = self.sector_classifier.predict(text_vector)[0]
        probabilities = self.sector_classifier.predict_proba(text_vector)[0]

        # Get confidence (max probability)
        confidence = float(np.max(probabilities))

        # Get top predictions
        top_indices = np.argsort(probabilities)[-3:][::-1]
        top_predictions = {}

        for idx in top_indices:
            label = self.sector_encoder.inverse_transform([idx])[0]
            top_predictions[label] = float(probabilities[idx])

        predicted_label = self.sector_encoder.inverse_transform([prediction])[0]

        return {
            'predicted': predicted_label,
            'confidence': confidence,
            'probabilities': top_predictions
        }

    def _classify_subsector(self, text: str, sector: str) -> Dict[str, Any]:
        """Classify document subsector within a sector"""
        if not self.subsector_classifier or not self.subsector_vectorizer:
            return {'predicted': 'unknown', 'confidence': 0.0, 'probabilities': {}}

        # Add sector context to text for better subsector classification
        contextual_text = f"Sector: {sector}. {text}"

        # Vectorize text
        text_vector = self.subsector_vectorizer.transform([contextual_text])

        # Predict
        prediction = self.subsector_classifier.predict(text_vector)[0]
        probabilities = self.subsector_classifier.predict_proba(text_vector)[0]

        confidence = float(np.max(probabilities))

        # Get top predictions
        top_indices = np.argsort(probabilities)[-3:][::-1]
        top_predictions = {}

        for idx in top_indices:
            label = self.subsector_encoder.inverse_transform([idx])[0]
            top_predictions[label] = float(probabilities[idx])

        predicted_label = self.subsector_encoder.inverse_transform([prediction])[0]

        return {
            'predicted': predicted_label,
            'confidence': confidence,
            'probabilities': top_predictions
        }

    def _classify_doctype(self, text: str) -> Dict[str, Any]:
        """Classify document type"""
        if not self.doctype_classifier or not self.doctype_vectorizer:
            return {'predicted': 'unknown', 'confidence': 0.0, 'probabilities': {}}

        # Vectorize text
        text_vector = self.doctype_vectorizer.transform([text])

        # Predict
        prediction = self.doctype_classifier.predict(text_vector)[0]
        probabilities = self.doctype_classifier.predict_proba(text_vector)[0]

        confidence = float(np.max(probabilities))

        # Get top predictions
        top_indices = np.argsort(probabilities)[-3:][::-1]
        top_predictions = {}

        for idx in top_indices:
            label = self.doctype_encoder.inverse_transform([idx])[0]
            top_predictions[label] = float(probabilities[idx])

        predicted_label = self.doctype_encoder.inverse_transform([prediction])[0]

        return {
            'predicted': predicted_label,
            'confidence': confidence,
            'probabilities': top_predictions
        }

    def train_models(self, training_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, str]:
        """
        Train classification models from training data

        Args:
            training_data: Dictionary with 'sector', 'subsector', 'doctype' training samples
                          Each sample: {'text': str, 'label': str}

        Returns:
            Dictionary with saved model paths
        """
        self.logger.info("Training classification models")

        saved_paths = {}

        # Train sector classifier
        if 'sector' in training_data and len(training_data['sector']) > 0:
            self.logger.info(f"Training sector classifier with {len(training_data['sector'])} samples")
            self._train_sector_model(training_data['sector'])
            saved_paths['sector'] = self.sector_model_path

        # Train subsector classifier
        if 'subsector' in training_data and len(training_data['subsector']) > 0:
            self.logger.info(f"Training subsector classifier with {len(training_data['subsector'])} samples")
            self._train_subsector_model(training_data['subsector'])
            saved_paths['subsector'] = self.subsector_model_path

        # Train doctype classifier
        if 'doctype' in training_data and len(training_data['doctype']) > 0:
            self.logger.info(f"Training doctype classifier with {len(training_data['doctype'])} samples")
            self._train_doctype_model(training_data['doctype'])
            saved_paths['doctype'] = self.doctype_model_path

        self.logger.info("Model training complete")
        return saved_paths

    def _train_sector_model(self, training_samples: List[Dict[str, Any]]):
        """Train sector classification model"""
        # Extract texts and labels
        texts = [sample['text'] for sample in training_samples]
        labels = [sample['label'] for sample in training_samples]

        # Create TF-IDF vectorizer with adaptive parameters
        self.sector_vectorizer = TfidfVectorizer(
            max_features=min(5000, len(texts) * 10),
            ngram_range=(1, 3),
            min_df=1,  # Changed from 2 to handle small datasets
            max_df=0.9
        )

        # Create label encoder
        self.sector_encoder = LabelEncoder()
        encoded_labels = self.sector_encoder.fit_transform(labels)

        # Vectorize texts
        X = self.sector_vectorizer.fit_transform(texts)

        # Split data only if we have enough samples per class
        # Check minimum class count
        unique_labels, label_counts = np.unique(encoded_labels, return_counts=True)
        min_class_count = np.min(label_counts)

        if len(training_samples) >= 10 and min_class_count >= 2:
            X_train, X_test, y_train, y_test = train_test_split(
                X, encoded_labels, test_size=0.2, random_state=42, stratify=encoded_labels
            )
        else:
            # Use all data for training if dataset is small or imbalanced
            self.logger.warning(
                f"Small/imbalanced dataset ({len(training_samples)} samples, "
                f"min class: {min_class_count}), using all for training"
            )
            X_train, X_test = X, X
            y_train, y_test = encoded_labels, encoded_labels

        # Train Random Forest classifier
        self.sector_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )

        self.sector_classifier.fit(X_train, y_train)

        # Evaluate
        y_pred = self.sector_classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        self.logger.info(f"Sector classifier accuracy: {accuracy:.3f}")

        # Save model
        self._save_model_components(
            self.sector_model_path,
            self.sector_vectorizer,
            self.sector_classifier,
            self.sector_encoder
        )

    def _train_subsector_model(self, training_samples: List[Dict[str, Any]]):
        """Train subsector classification model"""
        texts = [sample['text'] for sample in training_samples]
        labels = [sample['label'] for sample in training_samples]

        self.subsector_vectorizer = TfidfVectorizer(
            max_features=min(5000, len(texts) * 10),
            ngram_range=(1, 3),
            min_df=1,  # Changed from 2
            max_df=0.9
        )

        self.subsector_encoder = LabelEncoder()
        encoded_labels = self.subsector_encoder.fit_transform(labels)

        X = self.subsector_vectorizer.fit_transform(texts)

        # Split data only if we have enough samples per class
        unique_labels, label_counts = np.unique(encoded_labels, return_counts=True)
        min_class_count = np.min(label_counts)

        if len(training_samples) >= 10 and min_class_count >= 2:
            X_train, X_test, y_train, y_test = train_test_split(
                X, encoded_labels, test_size=0.2, random_state=42, stratify=encoded_labels
            )
        else:
            self.logger.warning(
                f"Small/imbalanced dataset ({len(training_samples)} samples, "
                f"min class: {min_class_count}), using all for training"
            )
            X_train, X_test = X, X
            y_train, y_test = encoded_labels, encoded_labels

        self.subsector_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )

        self.subsector_classifier.fit(X_train, y_train)

        y_pred = self.subsector_classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        self.logger.info(f"Subsector classifier accuracy: {accuracy:.3f}")

        self._save_model_components(
            self.subsector_model_path,
            self.subsector_vectorizer,
            self.subsector_classifier,
            self.subsector_encoder
        )

    def _train_doctype_model(self, training_samples: List[Dict[str, Any]]):
        """Train document type classification model"""
        texts = [sample['text'] for sample in training_samples]
        labels = [sample['label'] for sample in training_samples]

        self.doctype_vectorizer = TfidfVectorizer(
            max_features=min(3000, len(texts) * 10),
            ngram_range=(1, 2),
            min_df=1,  # Changed from 2
            max_df=0.9
        )

        self.doctype_encoder = LabelEncoder()
        encoded_labels = self.doctype_encoder.fit_transform(labels)

        X = self.doctype_vectorizer.fit_transform(texts)

        # Split data only if we have enough samples per class
        unique_labels, label_counts = np.unique(encoded_labels, return_counts=True)
        min_class_count = np.min(label_counts)

        if len(training_samples) >= 10 and min_class_count >= 2:
            X_train, X_test, y_train, y_test = train_test_split(
                X, encoded_labels, test_size=0.2, random_state=42, stratify=encoded_labels
            )
        else:
            self.logger.warning(
                f"Small/imbalanced dataset ({len(training_samples)} samples, "
                f"min class: {min_class_count}), using all for training"
            )
            X_train, X_test = X, X
            y_train, y_test = encoded_labels, encoded_labels

        self.doctype_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )

        self.doctype_classifier.fit(X_train, y_train)

        y_pred = self.doctype_classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        self.logger.info(f"Document type classifier accuracy: {accuracy:.3f}")

        self._save_model_components(
            self.doctype_model_path,
            self.doctype_vectorizer,
            self.doctype_classifier,
            self.doctype_encoder
        )

    def _save_model_components(
        self,
        path: str,
        vectorizer: TfidfVectorizer,
        classifier: RandomForestClassifier,
        encoder: LabelEncoder
    ):
        """Save model components to disk"""
        os.makedirs(os.path.dirname(path), exist_ok=True)

        model_bundle = {
            'vectorizer': vectorizer,
            'classifier': classifier,
            'encoder': encoder
        }

        with open(path, 'wb') as f:
            pickle.dump(model_bundle, f)

        self.logger.info(f"Saved model to {path}")

    def load_models(self, model_paths: Dict[str, str]) -> bool:
        """
        Load pre-trained classification models

        Args:
            model_paths: Dictionary with model file paths

        Returns:
            True if all models loaded successfully
        """
        self.logger.info("Loading classification models")

        success = True

        # Load sector model
        if 'sector' in model_paths:
            try:
                with open(model_paths['sector'], 'rb') as f:
                    bundle = pickle.load(f)
                    self.sector_vectorizer = bundle['vectorizer']
                    self.sector_classifier = bundle['classifier']
                    self.sector_encoder = bundle['encoder']
                self.logger.info(f"Loaded sector model from {model_paths['sector']}")
            except Exception as e:
                self.logger.error(f"Failed to load sector model: {e}")
                success = False

        # Load subsector model
        if 'subsector' in model_paths:
            try:
                with open(model_paths['subsector'], 'rb') as f:
                    bundle = pickle.load(f)
                    self.subsector_vectorizer = bundle['vectorizer']
                    self.subsector_classifier = bundle['classifier']
                    self.subsector_encoder = bundle['encoder']
                self.logger.info(f"Loaded subsector model from {model_paths['subsector']}")
            except Exception as e:
                self.logger.error(f"Failed to load subsector model: {e}")
                success = False

        # Load doctype model
        if 'doctype' in model_paths:
            try:
                with open(model_paths['doctype'], 'rb') as f:
                    bundle = pickle.load(f)
                    self.doctype_vectorizer = bundle['vectorizer']
                    self.doctype_classifier = bundle['classifier']
                    self.doctype_encoder = bundle['encoder']
                self.logger.info(f"Loaded doctype model from {model_paths['doctype']}")
            except Exception as e:
                self.logger.error(f"Failed to load doctype model: {e}")
                success = False

        return success

    def get_confidence_score(self, text: str, predicted_class: str, classifier_type: str = 'sector') -> float:
        """
        Get confidence score for a specific prediction

        Args:
            text: Input text
            predicted_class: Predicted class label
            classifier_type: Type of classifier ('sector', 'subsector', 'doctype')

        Returns:
            Confidence score (0-1)
        """
        if classifier_type == 'sector' and self.sector_classifier:
            text_vector = self.sector_vectorizer.transform([text])
            probabilities = self.sector_classifier.predict_proba(text_vector)[0]
            prediction = self.sector_classifier.predict(text_vector)[0]
            predicted_label = self.sector_encoder.inverse_transform([prediction])[0]

            if predicted_label == predicted_class:
                return float(np.max(probabilities))

        elif classifier_type == 'subsector' and self.subsector_classifier:
            text_vector = self.subsector_vectorizer.transform([text])
            probabilities = self.subsector_classifier.predict_proba(text_vector)[0]
            prediction = self.subsector_classifier.predict(text_vector)[0]
            predicted_label = self.subsector_encoder.inverse_transform([prediction])[0]

            if predicted_label == predicted_class:
                return float(np.max(probabilities))

        elif classifier_type == 'doctype' and self.doctype_classifier:
            text_vector = self.doctype_vectorizer.transform([text])
            probabilities = self.doctype_classifier.predict_proba(text_vector)[0]
            prediction = self.doctype_classifier.predict(text_vector)[0]
            predicted_label = self.doctype_encoder.inverse_transform([prediction])[0]

            if predicted_label == predicted_class:
                return float(np.max(probabilities))

        return 0.0

    def learn_from_correction(
        self,
        text: str,
        corrected_classification: Dict[str, Any]
    ) -> bool:
        """
        Learn from user correction (store in memory for future reference)

        Args:
            text: Document text
            corrected_classification: Corrected classification from user

        Returns:
            True if stored successfully
        """
        success = self.memory_manager.update_classification(
            text=text,
            corrected_classification=corrected_classification,
            confidence=1.0  # User corrections have full confidence
        )

        if success:
            self.stats['corrections_learned'] += 1
            self.logger.info("Learned from user correction")

        return success

    def execute(self, input_data: Any) -> Any:
        """
        Main execution logic (required by BaseAgent)

        Args:
            input_data: Dictionary with 'text' and optional 'metadata'

        Returns:
            Classification result
        """
        if isinstance(input_data, dict):
            text = input_data.get('text', '')
            metadata = input_data.get('metadata', {})
        else:
            text = str(input_data)
            metadata = {}

        return self.classify_document(text, metadata)

    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        base_stats = super().get_stats()
        base_stats.update(self.stats)
        base_stats['memory_stats'] = self.memory_manager.get_stats()
        return base_stats
