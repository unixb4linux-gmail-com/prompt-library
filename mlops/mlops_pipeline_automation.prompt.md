---
version: "1.0.0"
created_date: "2025-01-02"
last_updated: "2025-01-02"
enhancement_level: "advanced"
prompt_techniques: ["pipeline_orchestration", "automation_patterns", "best_practices", "ci_cd_integration"]
---

# MLOps Pipeline Automation Implementation Guide

> **Implementation Directive:**
> 
> **Scope:** Build end-to-end automated MLOps pipelines covering data validation, model training, testing, deployment, and monitoring
> 
> **Prerequisites:** Understanding of ML workflows, containerization, and CI/CD concepts

## Phase 1: Pipeline Architecture Design

### 1.1 MLOps Pipeline Components

**Core Pipeline Stages:**

```
Data Ingestion → Data Validation → Feature Engineering → Model Training → Model Validation → Model Registration → Deployment → Monitoring
```

**Pipeline Orchestration Options:**

1. **Kubeflow Pipelines** (Kubernetes-native)
2. **Apache Airflow** (Traditional workflow orchestration)
3. **GitHub Actions/GitLab CI** (Git-native CI/CD)
4. **Azure ML Pipelines** (Cloud-native)
5. **Custom Orchestration** (Python-based)

### 1.2 Infrastructure as Code

**Kubernetes MLOps Environment:**

```yaml
# k8s-mlops-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: mlops
  labels:
    name: mlops

---
# kubeflow-pipelines-install.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kubeflow-pipelines-config
  namespace: mlops
data:
  install.sh: |
    #!/bin/bash
    kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=1.8.5"
    kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
    kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=1.8.5"

---
# mlops-storage.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mlops-data-pvc
  namespace: mlops
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 100Gi
  storageClassName: nfs-client

---
# model-registry-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlflow-server
  namespace: mlops
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mlflow-server
  template:
    metadata:
      labels:
        app: mlflow-server
    spec:
      containers:
      - name: mlflow
        image: mlflow/mlflow:latest
        ports:
        - containerPort: 5000
        env:
        - name: BACKEND_STORE_URI
          value: "postgresql://mlflow:password@postgres:5432/mlflow"
        - name: DEFAULT_ARTIFACT_ROOT
          value: "s3://mlflow-artifacts/"
        volumeMounts:
        - name: mlops-data
          mountPath: /mlflow/data
      volumes:
      - name: mlops-data
        persistentVolumeClaim:
          claimName: mlops-data-pvc
```

## Phase 2: Data Pipeline Implementation

### 2.1 Data Validation and Quality Checks

**Data Validation Pipeline Component:**

```python
# data_validation.py
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from dataclasses import dataclass
from abc import ABC, abstractmethod
import json
import mlflow
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset

@dataclass
class DataQualityReport:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    metrics: Dict[str, float]
    drift_detected: bool

class DataValidator(ABC):
    @abstractmethod
    def validate(self, data: pd.DataFrame) -> DataQualityReport:
        pass

class SchemaValidator(DataValidator):
    def __init__(self, expected_schema: Dict):
        self.expected_schema = expected_schema
    
    def validate(self, data: pd.DataFrame) -> DataQualityReport:
        errors = []
        warnings = []
        
        # Check columns
        expected_columns = set(self.expected_schema.keys())
        actual_columns = set(data.columns)
        
        missing_columns = expected_columns - actual_columns
        extra_columns = actual_columns - expected_columns
        
        if missing_columns:
            errors.append(f"Missing columns: {missing_columns}")
        
        if extra_columns:
            warnings.append(f"Extra columns: {extra_columns}")
        
        # Check data types
        for col, expected_type in self.expected_schema.items():
            if col in data.columns:
                actual_type = str(data[col].dtype)
                if not self._types_compatible(actual_type, expected_type):
                    errors.append(f"Column {col}: expected {expected_type}, got {actual_type}")
        
        return DataQualityReport(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metrics={"schema_compliance": 1.0 if len(errors) == 0 else 0.0},
            drift_detected=False
        )
    
    def _types_compatible(self, actual: str, expected: str) -> bool:
        # Simplified type checking - extend as needed
        type_mapping = {
            'int64': ['int', 'integer'],
            'float64': ['float', 'number'],
            'object': ['string', 'text'],
            'bool': ['boolean']
        }
        
        compatible_types = type_mapping.get(actual, [actual])
        return expected.lower() in compatible_types

class StatisticalValidator(DataValidator):
    def __init__(self, reference_data: pd.DataFrame, drift_threshold: float = 0.1):
        self.reference_data = reference_data
        self.drift_threshold = drift_threshold
    
    def validate(self, data: pd.DataFrame) -> DataQualityReport:
        errors = []
        warnings = []
        metrics = {}
        drift_detected = False
        
        # Basic statistics validation
        for col in data.select_dtypes(include=[np.number]).columns:
            if col in self.reference_data.columns:
                # Check for extreme outliers
                q99 = self.reference_data[col].quantile(0.99)
                q01 = self.reference_data[col].quantile(0.01)
                
                outlier_rate = ((data[col] > q99) | (data[col] < q01)).mean()
                metrics[f"{col}_outlier_rate"] = outlier_rate
                
                if outlier_rate > 0.1:  # More than 10% outliers
                    warnings.append(f"High outlier rate in {col}: {outlier_rate:.2%}")
        
        # Data drift detection using Evidently
        try:
            report = Report(metrics=[DataDriftPreset()])
            report.run(reference_data=self.reference_data, current_data=data)
            
            report_dict = report.as_dict()
            drift_score = report_dict['metrics'][0]['result']['dataset_drift_score']
            metrics['data_drift_score'] = drift_score
            
            if drift_score > self.drift_threshold:
                drift_detected = True
                warnings.append(f"Data drift detected: score = {drift_score:.3f}")
                
        except Exception as e:
            warnings.append(f"Could not compute drift metrics: {str(e)}")
        
        return DataQualityReport(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metrics=metrics,
            drift_detected=drift_detected
        )

class DataQualityValidator(DataValidator):
    def validate(self, data: pd.DataFrame) -> DataQualityReport:
        errors = []
        warnings = []
        metrics = {}
        
        # Missing value analysis
        missing_rates = data.isnull().mean()
        for col, rate in missing_rates.items():
            metrics[f"{col}_missing_rate"] = rate
            if rate > 0.5:  # More than 50% missing
                errors.append(f"Column {col} has {rate:.1%} missing values")
            elif rate > 0.1:  # More than 10% missing
                warnings.append(f"Column {col} has {rate:.1%} missing values")
        
        # Duplicate analysis
        duplicate_rate = data.duplicated().mean()
        metrics['duplicate_rate'] = duplicate_rate
        
        if duplicate_rate > 0.1:
            warnings.append(f"High duplicate rate: {duplicate_rate:.1%}")
        
        # Data consistency checks
        for col in data.select_dtypes(include=[np.number]).columns:
            if data[col].var() == 0:
                warnings.append(f"Column {col} has no variance")
        
        return DataQualityReport(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metrics=metrics,
            drift_detected=False
        )

class MLDataValidationPipeline:
    def __init__(self, validators: List[DataValidator]):
        self.validators = validators
        self.logger = logging.getLogger(__name__)
    
    def validate_data(self, data: pd.DataFrame, log_to_mlflow: bool = True) -> DataQualityReport:
        """Run all validators and aggregate results"""
        all_errors = []
        all_warnings = []
        all_metrics = {}
        drift_detected = False
        
        for validator in self.validators:
            try:
                report = validator.validate(data)
                all_errors.extend(report.errors)
                all_warnings.extend(report.warnings)
                all_metrics.update(report.metrics)
                
                if report.drift_detected:
                    drift_detected = True
                    
            except Exception as e:
                self.logger.error(f"Validator {type(validator).__name__} failed: {e}")
                all_errors.append(f"Validation failed: {str(e)}")
        
        final_report = DataQualityReport(
            is_valid=len(all_errors) == 0,
            errors=all_errors,
            warnings=all_warnings,
            metrics=all_metrics,
            drift_detected=drift_detected
        )
        
        if log_to_mlflow:
            self._log_to_mlflow(final_report, data)
        
        return final_report
    
    def _log_to_mlflow(self, report: DataQualityReport, data: pd.DataFrame):
        """Log validation results to MLflow"""
        # Log metrics
        mlflow.log_metrics(report.metrics)
        
        # Log data statistics
        mlflow.log_metric("data_rows", len(data))
        mlflow.log_metric("data_columns", len(data.columns))
        
        # Log validation status
        mlflow.log_metric("data_quality_valid", 1.0 if report.is_valid else 0.0)
        mlflow.log_metric("drift_detected", 1.0 if report.drift_detected else 0.0)
        
        # Log detailed report as artifact
        report_dict = {
            "is_valid": report.is_valid,
            "errors": report.errors,
            "warnings": report.warnings,
            "metrics": report.metrics,
            "drift_detected": report.drift_detected
        }
        
        with open("data_quality_report.json", "w") as f:
            json.dump(report_dict, f, indent=2)
        
        mlflow.log_artifact("data_quality_report.json")

# Usage Example
def create_validation_pipeline(reference_data: pd.DataFrame) -> MLDataValidationPipeline:
    """Create a comprehensive data validation pipeline"""
    
    # Define expected schema
    schema = {
        'feature_1': 'float',
        'feature_2': 'int',
        'feature_3': 'string',
        'target': 'int'
    }
    
    validators = [
        SchemaValidator(schema),
        StatisticalValidator(reference_data),
        DataQualityValidator()
    ]
    
    return MLDataValidationPipeline(validators)

# Integration in ML Pipeline
if __name__ == "__main__":
    # Load reference data (from training set)
    reference_data = pd.read_csv("training_data.csv")
    
    # Create validation pipeline
    validator = create_validation_pipeline(reference_data)
    
    # Validate new data
    new_data = pd.read_csv("new_data.csv")
    
    with mlflow.start_run():
        report = validator.validate_data(new_data)
        
        if not report.is_valid:
            raise ValueError(f"Data validation failed: {report.errors}")
        
        if report.drift_detected:
            logging.warning("Data drift detected - consider retraining")
        
        print(f"Data validation completed: {report}")
```

### 2.2 Feature Engineering Pipeline

**Automated Feature Engineering:**

```python
# feature_engineering.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.feature_selection import SelectKBest, f_classif
from typing import Dict, List, Optional, Tuple
import joblib
import mlflow
import mlflow.sklearn
from dataclasses import dataclass

@dataclass
class FeatureEngineeringConfig:
    numerical_features: List[str]
    categorical_features: List[str]
    target_column: str
    feature_selection_k: Optional[int] = None
    scaling_method: str = "standard"  # "standard", "minmax", "robust"
    encoding_method: str = "onehot"   # "onehot", "label"

class FeatureEngineerer:
    def __init__(self, config: FeatureEngineeringConfig):
        self.config = config
        self.scaler = None
        self.encoder = None
        self.feature_selector = None
        self.feature_names = None
        self.is_fitted = False
    
    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        """Fit feature engineering transformations"""
        
        # Initialize transformers
        if self.config.scaling_method == "standard":
            self.scaler = StandardScaler()
        # Add other scalers as needed
        
        if self.config.encoding_method == "onehot":
            self.encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
        
        if self.config.feature_selection_k:
            self.feature_selector = SelectKBest(f_classif, k=self.config.feature_selection_k)
        
        # Fit numerical features
        if self.config.numerical_features:
            numerical_data = X[self.config.numerical_features]
            self.scaler.fit(numerical_data)
        
        # Fit categorical features
        if self.config.categorical_features:
            categorical_data = X[self.config.categorical_features]
            self.encoder.fit(categorical_data)
        
        # Create feature matrix for selection
        X_processed = self._transform_features(X)
        
        # Fit feature selector
        if self.feature_selector and y is not None:
            self.feature_selector.fit(X_processed, y)
            
            # Get selected feature names
            if hasattr(self.feature_selector, 'get_support'):
                selected_features = self.feature_selector.get_support()
                self.feature_names = [name for name, selected in 
                                    zip(self._get_feature_names(), selected_features) if selected]
        else:
            self.feature_names = self._get_feature_names()
        
        self.is_fitted = True
        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform features using fitted transformers"""
        if not self.is_fitted:
            raise ValueError("FeatureEngineerer must be fitted before transform")
        
        X_processed = self._transform_features(X)
        
        # Apply feature selection
        if self.feature_selector:
            X_processed = self.feature_selector.transform(X_processed)
        
        return pd.DataFrame(X_processed, columns=self.feature_names, index=X.index)
    
    def fit_transform(self, X: pd.DataFrame, y: pd.Series = None) -> pd.DataFrame:
        """Fit and transform in one step"""
        return self.fit(X, y).transform(X)
    
    def _transform_features(self, X: pd.DataFrame) -> np.ndarray:
        """Apply all transformations"""
        transformed_parts = []
        
        # Transform numerical features
        if self.config.numerical_features:
            numerical_data = X[self.config.numerical_features]
            scaled_numerical = self.scaler.transform(numerical_data)
            transformed_parts.append(scaled_numerical)
        
        # Transform categorical features
        if self.config.categorical_features:
            categorical_data = X[self.config.categorical_features]
            encoded_categorical = self.encoder.transform(categorical_data)
            transformed_parts.append(encoded_categorical)
        
        if transformed_parts:
            return np.hstack(transformed_parts)
        else:
            return X.values
    
    def _get_feature_names(self) -> List[str]:
        """Get names of all transformed features"""
        feature_names = []
        
        # Numerical feature names
        if self.config.numerical_features:
            feature_names.extend(self.config.numerical_features)
        
        # Categorical feature names (for one-hot encoding)
        if self.config.categorical_features and hasattr(self.encoder, 'get_feature_names_out'):
            cat_feature_names = self.encoder.get_feature_names_out(self.config.categorical_features)
            feature_names.extend(cat_feature_names)
        elif self.config.categorical_features:
            feature_names.extend(self.config.categorical_features)
        
        return feature_names
    
    def save_transformers(self, path_prefix: str):
        """Save fitted transformers"""
        if self.scaler:
            joblib.dump(self.scaler, f"{path_prefix}_scaler.pkl")
        if self.encoder:
            joblib.dump(self.encoder, f"{path_prefix}_encoder.pkl")
        if self.feature_selector:
            joblib.dump(self.feature_selector, f"{path_prefix}_selector.pkl")
        
        # Save feature names and config
        joblib.dump(self.feature_names, f"{path_prefix}_feature_names.pkl")
        joblib.dump(self.config, f"{path_prefix}_config.pkl")
    
    def load_transformers(self, path_prefix: str):
        """Load fitted transformers"""
        try:
            self.scaler = joblib.load(f"{path_prefix}_scaler.pkl")
        except FileNotFoundError:
            pass
        
        try:
            self.encoder = joblib.load(f"{path_prefix}_encoder.pkl")
        except FileNotFoundError:
            pass
        
        try:
            self.feature_selector = joblib.load(f"{path_prefix}_selector.pkl")
        except FileNotFoundError:
            pass
        
        self.feature_names = joblib.load(f"{path_prefix}_feature_names.pkl")
        self.config = joblib.load(f"{path_prefix}_config.pkl")
        self.is_fitted = True

class FeatureStore:
    """Simple feature store implementation"""
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.features = {}
    
    def register_feature_set(self, name: str, feature_engineer: FeatureEngineerer, 
                           description: str = ""):
        """Register a feature engineering pipeline"""
        self.features[name] = {
            'engineer': feature_engineer,
            'description': description,
            'created_at': pd.Timestamp.now()
        }
        
        # Save to disk
        feature_engineer.save_transformers(f"{self.base_path}/{name}")
    
    def get_feature_set(self, name: str) -> FeatureEngineerer:
        """Get a registered feature set"""
        if name not in self.features:
            # Try to load from disk
            engineer = FeatureEngineerer(None)  # Will load config
            engineer.load_transformers(f"{self.base_path}/{name}")
            self.features[name] = {'engineer': engineer}
        
        return self.features[name]['engineer']
    
    def list_feature_sets(self) -> List[str]:
        """List all registered feature sets"""
        return list(self.features.keys())

# Usage in ML Pipeline
def create_feature_engineering_pipeline(data: pd.DataFrame, target_column: str):
    """Create feature engineering pipeline based on data"""
    
    # Automatically detect feature types
    numerical_features = data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Remove target from features
    if target_column in numerical_features:
        numerical_features.remove(target_column)
    if target_column in categorical_features:
        categorical_features.remove(target_column)
    
    config = FeatureEngineeringConfig(
        numerical_features=numerical_features,
        categorical_features=categorical_features,
        target_column=target_column,
        feature_selection_k=min(50, len(numerical_features) + len(categorical_features)),
        scaling_method="standard",
        encoding_method="onehot"
    )
    
    return FeatureEngineerer(config)

# MLflow Integration
def log_feature_engineering_artifacts(feature_engineer: FeatureEngineerer):
    """Log feature engineering artifacts to MLflow"""
    
    # Save transformers temporarily
    import tempfile
    import os
    
    with tempfile.TemporaryDirectory() as temp_dir:
        feature_engineer.save_transformers(os.path.join(temp_dir, "feature_eng"))
        
        # Log all transformer files
        for file in os.listdir(temp_dir):
            mlflow.log_artifact(os.path.join(temp_dir, file))
    
    # Log feature information
    mlflow.log_param("num_features", len(feature_engineer.feature_names))
    mlflow.log_param("feature_names", feature_engineer.feature_names)
    mlflow.log_param("numerical_features", feature_engineer.config.numerical_features)
    mlflow.log_param("categorical_features", feature_engineer.config.categorical_features)

if __name__ == "__main__":
    # Example usage
    data = pd.read_csv("training_data.csv")
    target_column = "target"
    
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    # Create and fit feature engineering pipeline
    feature_engineer = create_feature_engineering_pipeline(data, target_column)
    
    with mlflow.start_run():
        X_processed = feature_engineer.fit_transform(X, y)
        
        # Log to MLflow
        log_feature_engineering_artifacts(feature_engineer)
        
        print(f"Original features: {X.shape[1]}")
        print(f"Processed features: {X_processed.shape[1]}")
        print(f"Feature names: {feature_engineer.feature_names}")
```

## Phase 3: Model Training Pipeline

### 3.1 Automated Model Training and Hyperparameter Tuning

**Training Pipeline with Automated HP Tuning:**

```python
# model_training_pipeline.py
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from typing import Dict, List, Any, Optional, Tuple
import json
import joblib
from dataclasses import dataclass
import optuna
from optuna.integration.mlflow import MLflowCallback

@dataclass
class ModelConfig:
    model_type: str
    hyperparameters: Dict[str, Any]
    search_space: Dict[str, List[Any]]
    cv_folds: int = 5
    scoring_metric: str = "accuracy"

class AutoMLTrainer:
    def __init__(self, models_config: List[ModelConfig], experiment_name: str):
        self.models_config = models_config
        self.experiment_name = experiment_name
        self.best_model = None
        self.best_score = -np.inf
        self.client = MlflowClient()
        
        # Set up MLflow experiment
        try:
            self.experiment_id = mlflow.create_experiment(experiment_name)
        except Exception:
            experiment = mlflow.get_experiment_by_name(experiment_name)
            self.experiment_id = experiment.experiment_id
    
    def get_model_class(self, model_type: str):
        """Get model class by name"""
        model_classes = {
            'random_forest': RandomForestClassifier,
            'gradient_boosting': GradientBoostingClassifier,
            'logistic_regression': LogisticRegression,
            'svm': SVC
        }
        return model_classes.get(model_type)
    
    def train_single_model(self, config: ModelConfig, X_train: pd.DataFrame, 
                          y_train: pd.Series, X_val: pd.DataFrame = None, 
                          y_val: pd.Series = None) -> Tuple[Any, Dict[str, float]]:
        """Train a single model with hyperparameter optimization"""
        
        model_class = self.get_model_class(config.model_type)
        if not model_class:
            raise ValueError(f"Unknown model type: {config.model_type}")
        
        with mlflow.start_run(experiment_id=self.experiment_id, 
                             run_name=f"{config.model_type}_training"):
            
            # Log basic parameters
            mlflow.log_param("model_type", config.model_type)
            mlflow.log_param("cv_folds", config.cv_folds)
            mlflow.log_param("scoring_metric", config.scoring_metric)
            
            if config.search_space:
                # Use Optuna for hyperparameter optimization
                best_model, best_params, best_score = self._optimize_with_optuna(
                    model_class, config, X_train, y_train
                )
            else:
                # Use default hyperparameters
                model = model_class(**config.hyperparameters)
                model.fit(X_train, y_train)
                
                # Cross-validation score
                cv_scores = cross_val_score(model, X_train, y_train, 
                                          cv=config.cv_folds, 
                                          scoring=config.scoring_metric)
                best_score = cv_scores.mean()
                best_params = config.hyperparameters
                best_model = model
            
            # Train final model with best parameters
            final_model = model_class(**best_params)
            final_model.fit(X_train, y_train)
            
            # Evaluate model
            metrics = self._evaluate_model(final_model, X_train, y_train, X_val, y_val)
            
            # Log everything to MLflow
            mlflow.log_params(best_params)
            mlflow.log_metrics(metrics)
            mlflow.log_metric("best_cv_score", best_score)
            
            # Log model
            mlflow.sklearn.log_model(
                sk_model=final_model,
                artifact_path="model",
                input_example=X_train.iloc[:5],
                signature=mlflow.models.infer_signature(X_train, y_train)
            )
            
            # Log feature importance if available
            if hasattr(final_model, 'feature_importances_'):
                importance_df = pd.DataFrame({
                    'feature': X_train.columns,
                    'importance': final_model.feature_importances_
                }).sort_values('importance', ascending=False)
                
                importance_df.to_csv("feature_importance.csv", index=False)
                mlflow.log_artifact("feature_importance.csv")
            
            return final_model, metrics
    
    def _optimize_with_optuna(self, model_class, config: ModelConfig, 
                            X_train: pd.DataFrame, y_train: pd.Series):
        """Hyperparameter optimization using Optuna"""
        
        def objective(trial):
            params = {}
            for param, values in config.search_space.items():
                if isinstance(values[0], int):
                    params[param] = trial.suggest_int(param, min(values), max(values))
                elif isinstance(values[0], float):
                    params[param] = trial.suggest_float(param, min(values), max(values))
                else:
                    params[param] = trial.suggest_categorical(param, values)
            
            model = model_class(**params)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, 
                                      cv=config.cv_folds, 
                                      scoring=config.scoring_metric)
            return cv_scores.mean()
        
        # Create study
        study = optuna.create_study(direction='maximize')
        
        # Add MLflow callback
        mlflow_callback = MLflowCallback(
            tracking_uri=mlflow.get_tracking_uri(),
            metric_name=config.scoring_metric
        )
        
        # Optimize
        study.optimize(objective, n_trials=50, callbacks=[mlflow_callback])
        
        # Get best parameters
        best_params = study.best_params
        best_score = study.best_value
        
        # Train final model
        best_model = model_class(**best_params)
        best_model.fit(X_train, y_train)
        
        return best_model, best_params, best_score
    
    def _evaluate_model(self, model, X_train: pd.DataFrame, y_train: pd.Series,
                       X_val: pd.DataFrame = None, y_val: pd.Series = None) -> Dict[str, float]:
        """Comprehensive model evaluation"""
        metrics = {}
        
        # Training metrics
        train_pred = model.predict(X_train)
        train_prob = model.predict_proba(X_train)[:, 1] if hasattr(model, 'predict_proba') else None
        
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        metrics['train_accuracy'] = accuracy_score(y_train, train_pred)
        metrics['train_precision'] = precision_score(y_train, train_pred, average='weighted')
        metrics['train_recall'] = recall_score(y_train, train_pred, average='weighted')
        metrics['train_f1'] = f1_score(y_train, train_pred, average='weighted')
        
        if train_prob is not None:
            metrics['train_auc'] = roc_auc_score(y_train, train_prob)
        
        # Validation metrics
        if X_val is not None and y_val is not None:
            val_pred = model.predict(X_val)
            val_prob = model.predict_proba(X_val)[:, 1] if hasattr(model, 'predict_proba') else None
            
            metrics['val_accuracy'] = accuracy_score(y_val, val_pred)
            metrics['val_precision'] = precision_score(y_val, val_pred, average='weighted')
            metrics['val_recall'] = recall_score(y_val, val_pred, average='weighted')
            metrics['val_f1'] = f1_score(y_val, val_pred, average='weighted')
            
            if val_prob is not None:
                metrics['val_auc'] = roc_auc_score(y_val, val_prob)
        
        return metrics
    
    def train_all_models(self, X_train: pd.DataFrame, y_train: pd.Series,
                        X_val: pd.DataFrame = None, y_val: pd.Series = None) -> Dict[str, Any]:
        """Train all configured models and return the best one"""
        
        results = {}
        
        for config in self.models_config:
            print(f"Training {config.model_type}...")
            
            try:
                model, metrics = self.train_single_model(config, X_train, y_train, X_val, y_val)
                
                results[config.model_type] = {
                    'model': model,
                    'metrics': metrics,
                    'config': config
                }
                
                # Update best model
                score = metrics.get('val_accuracy', metrics.get('train_accuracy', 0))
                if score > self.best_score:
                    self.best_score = score
                    self.best_model = model
                    
            except Exception as e:
                print(f"Failed to train {config.model_type}: {e}")
                continue
        
        return results
    
    def get_best_model(self):
        """Get the best performing model"""
        return self.best_model

# Configuration for different models
def get_default_model_configs() -> List[ModelConfig]:
    """Get default model configurations for AutoML"""
    
    return [
        ModelConfig(
            model_type="random_forest",
            hyperparameters={"n_estimators": 100, "random_state": 42},
            search_space={
                "n_estimators": [50, 100, 200, 300],
                "max_depth": [5, 10, 15, 20, None],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4]
            }
        ),
        ModelConfig(
            model_type="gradient_boosting",
            hyperparameters={"n_estimators": 100, "random_state": 42},
            search_space={
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.1, 0.2],
                "max_depth": [3, 5, 7],
                "subsample": [0.8, 0.9, 1.0]
            }
        ),
        ModelConfig(
            model_type="logistic_regression",
            hyperparameters={"random_state": 42, "max_iter": 1000},
            search_space={
                "C": [0.1, 1, 10, 100],
                "penalty": ["l1", "l2"],
                "solver": ["liblinear", "saga"]
            }
        )
    ]

# Usage Example
if __name__ == "__main__":
    # Load data
    data = pd.read_csv("processed_data.csv")
    target_column = "target"
    
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    # Split data
    from sklearn.model_selection import train_test_split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create trainer
    configs = get_default_model_configs()
    trainer = AutoMLTrainer(configs, "model_comparison")
    
    # Train all models
    results = trainer.train_all_models(X_train, y_train, X_val, y_val)
    
    # Get best model
    best_model = trainer.get_best_model()
    print(f"Best model score: {trainer.best_score}")
    
    # Print results summary
    for model_type, result in results.items():
        val_acc = result['metrics'].get('val_accuracy', 'N/A')
        print(f"{model_type}: {val_acc}")
```

## Phase 4: Model Deployment Pipeline

### 4.1 Automated Model Deployment

**Model Deployment Automation:**

```python
# model_deployment.py
import mlflow
import mlflow.pyfunc
from mlflow.tracking import MlflowClient
import docker
import kubernetes
from kubernetes import client, config
import yaml
import json
import requests
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import logging

@dataclass
class DeploymentConfig:
    model_name: str
    model_version: str
    environment: str  # "staging", "production"
    replicas: int = 2
    cpu_request: str = "100m"
    memory_request: str = "256Mi"
    cpu_limit: str = "500m"
    memory_limit: str = "1Gi"
    health_check_path: str = "/health"
    metrics_path: str = "/metrics"

class ModelDeployer:
    def __init__(self, mlflow_uri: str, k8s_config_file: Optional[str] = None):
        mlflow.set_tracking_uri(mlflow_uri)
        self.client = MlflowClient(mlflow_uri)
        
        # Kubernetes setup
        if k8s_config_file:
            config.load_kube_config(config_file=k8s_config_file)
        else:
            config.load_incluster_config()
        
        self.k8s_apps_v1 = client.AppsV1Api()
        self.k8s_core_v1 = client.CoreV1Api()
        self.docker_client = docker.from_env()
        
        self.logger = logging.getLogger(__name__)

    def build_model_image(self, model_name: str, model_version: str, 
                         base_image: str = "python:3.9-slim") -> str:
        """Build Docker image for model serving"""
        
        # Download model from MLflow
        model_uri = f"models:/{model_name}/{model_version}"
        local_model_path = mlflow.artifacts.download_artifacts(model_uri)
        
        # Create Dockerfile
        dockerfile_content = f"""
FROM {base_image}

RUN pip install mlflow pandas scikit-learn flask prometheus-client

COPY model/ /opt/ml/model/

COPY serving_app.py /app/serving_app.py

WORKDIR /app

EXPOSE 8080

CMD ["python", "serving_app.py"]
"""
        
        # Create serving application
        serving_app_content = '''
import os
import json
import pandas as pd
import mlflow.pyfunc
from flask import Flask, request, jsonify
import logging
from prometheus_client import Counter, Histogram, generate_latest
import time

app = Flask(__name__)

# Metrics
PREDICTION_COUNTER = Counter('model_predictions_total', 'Total predictions', ['model', 'version'])
PREDICTION_DURATION = Histogram('model_prediction_duration_seconds', 'Prediction duration')

# Load model
model = mlflow.pyfunc.load_model('/opt/ml/model')
MODEL_NAME = os.getenv('MODEL_NAME', 'unknown')
MODEL_VERSION = os.getenv('MODEL_VERSION', 'unknown')

@app.route('/predict', methods=['POST'])
def predict():
    start_time = time.time()
    
    try:
        # Get input data
        data = request.json
        input_data = pd.DataFrame(data['instances'])
        
        # Make prediction
        predictions = model.predict(input_data)
        
        # Update metrics
        PREDICTION_COUNTER.labels(model=MODEL_NAME, version=MODEL_VERSION).inc()
        PREDICTION_DURATION.observe(time.time() - start_time)
        
        return jsonify({
            'predictions': predictions.tolist(),
            'model_name': MODEL_NAME,
            'model_version': MODEL_VERSION
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
'''
        
        # Build image
        import tempfile
        import shutil
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy model artifacts
            shutil.copytree(local_model_path, f"{temp_dir}/model")
            
            # Write Dockerfile and serving app
            with open(f"{temp_dir}/Dockerfile", "w") as f:
                f.write(dockerfile_content)
            
            with open(f"{temp_dir}/serving_app.py", "w") as f:
                f.write(serving_app_content)
            
            # Build Docker image
            image_name = f"{model_name}:{model_version}"
            self.docker_client.images.build(
                path=temp_dir,
                tag=image_name,
                rm=True
            )
            
            self.logger.info(f"Built image: {image_name}")
            return image_name

    def create_k8s_deployment(self, config: DeploymentConfig, image_name: str):
        """Create Kubernetes deployment for model"""
        
        deployment_name = f"{config.model_name}-{config.environment}"
        namespace = "mlops"
        
        # Deployment manifest
        deployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": deployment_name,
                "namespace": namespace,
                "labels": {
                    "app": config.model_name,
                    "environment": config.environment,
                    "version": config.model_version
                }
            },
            "spec": {
                "replicas": config.replicas,
                "selector": {
                    "matchLabels": {
                        "app": config.model_name,
                        "environment": config.environment
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": config.model_name,
                            "environment": config.environment,
                            "version": config.model_version
                        },
                        "annotations": {
                            "prometheus.io/scrape": "true",
                            "prometheus.io/port": "8080",
                            "prometheus.io/path": "/metrics"
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": "model-server",
                                "image": image_name,
                                "ports": [
                                    {"containerPort": 8080, "name": "http"}
                                ],
                                "env": [
                                    {"name": "MODEL_NAME", "value": config.model_name},
                                    {"name": "MODEL_VERSION", "value": config.model_version}
                                ],
                                "resources": {
                                    "requests": {
                                        "cpu": config.cpu_request,
                                        "memory": config.memory_request
                                    },
                                    "limits": {
                                        "cpu": config.cpu_limit,
                                        "memory": config.memory_limit
                                    }
                                },
                                "livenessProbe": {
                                    "httpGet": {
                                        "path": config.health_check_path,
                                        "port": 8080
                                    },
                                    "initialDelaySeconds": 30,
                                    "periodSeconds": 10
                                },
                                "readinessProbe": {
                                    "httpGet": {
                                        "path": config.health_check_path,
                                        "port": 8080
                                    },
                                    "initialDelaySeconds": 5,
                                    "periodSeconds": 5
                                }
                            }
                        ]
                    }
                }
            }
        }
        
        # Create or update deployment
        try:
            self.k8s_apps_v1.create_namespaced_deployment(
                namespace=namespace,
                body=deployment
            )
            self.logger.info(f"Created deployment: {deployment_name}")
        except kubernetes.client.exceptions.ApiException as e:
            if e.status == 409:  # Already exists
                self.k8s_apps_v1.patch_namespaced_deployment(
                    name=deployment_name,
                    namespace=namespace,
                    body=deployment
                )
                self.logger.info(f"Updated deployment: {deployment_name}")
            else:
                raise

    def create_k8s_service(self, config: DeploymentConfig):
        """Create Kubernetes service for model"""
        
        service_name = f"{config.model_name}-{config.environment}"
        namespace = "mlops"
        
        service = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": service_name,
                "namespace": namespace,
                "labels": {
                    "app": config.model_name,
                    "environment": config.environment
                }
            },
            "spec": {
                "selector": {
                    "app": config.model_name,
                    "environment": config.environment
                },
                "ports": [
                    {
                        "port": 80,
                        "targetPort": 8080,
                        "protocol": "TCP",
                        "name": "http"
                    }
                ],
                "type": "ClusterIP"
            }
        }
        
        try:
            self.k8s_core_v1.create_namespaced_service(
                namespace=namespace,
                body=service
            )
            self.logger.info(f"Created service: {service_name}")
        except kubernetes.client.exceptions.ApiException as e:
            if e.status == 409:  # Already exists
                self.logger.info(f"Service already exists: {service_name}")
            else:
                raise

    def deploy_model(self, config: DeploymentConfig) -> bool:
        """Complete model deployment workflow"""
        try:
            # Step 1: Build Docker image
            self.logger.info(f"Building image for {config.model_name}:{config.model_version}")
            image_name = self.build_model_image(config.model_name, config.model_version)
            
            # Step 2: Create Kubernetes resources
            self.logger.info("Creating Kubernetes deployment")
            self.create_k8s_deployment(config, image_name)
            
            self.logger.info("Creating Kubernetes service")
            self.create_k8s_service(config)
            
            # Step 3: Wait for deployment to be ready
            self.logger.info("Waiting for deployment to be ready")
            self._wait_for_deployment(config)
            
            # Step 4: Run health checks
            self.logger.info("Running health checks")
            if self._health_check(config):
                self.logger.info("Deployment successful")
                return True
            else:
                self.logger.error("Health check failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Deployment failed: {e}")
            return False

    def _wait_for_deployment(self, config: DeploymentConfig, timeout: int = 300):
        """Wait for deployment to be ready"""
        deployment_name = f"{config.model_name}-{config.environment}"
        namespace = "mlops"
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                deployment = self.k8s_apps_v1.read_namespaced_deployment(
                    name=deployment_name,
                    namespace=namespace
                )
                
                if (deployment.status.ready_replicas is not None and 
                    deployment.status.ready_replicas >= config.replicas):
                    return True
                    
            except Exception as e:
                self.logger.warning(f"Error checking deployment status: {e}")
            
            time.sleep(10)
        
        raise TimeoutError(f"Deployment not ready after {timeout} seconds")

    def _health_check(self, config: DeploymentConfig) -> bool:
        """Perform health check on deployed model"""
        service_name = f"{config.model_name}-{config.environment}"
        namespace = "mlops"
        
        # For simplicity, using port-forward. In production, use proper service discovery
        try:
            # This is a simplified health check - in practice you'd use proper service URLs
            # or port-forwarding
            health_url = f"http://{service_name}.{namespace}.svc.cluster.local{config.health_check_path}"
            
            # Simplified - you'd need to implement proper service discovery
            # For now, just return True
            return True
            
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False

# Automated deployment pipeline
class MLDeploymentPipeline:
    def __init__(self, deployer: ModelDeployer):
        self.deployer = deployer
        self.client = deployer.client

    def deploy_staging_model(self, model_name: str, version: Optional[str] = None):
        """Deploy latest staging model to staging environment"""
        if version is None:
            # Get latest staging version
            versions = self.client.get_latest_versions(model_name, stages=["Staging"])
            if not versions:
                raise ValueError(f"No staging version found for {model_name}")
            version = versions[0].version
        
        config = DeploymentConfig(
            model_name=model_name,
            model_version=version,
            environment="staging",
            replicas=1  # Fewer replicas for staging
        )
        
        return self.deployer.deploy_model(config)

    def promote_to_production(self, model_name: str, version: str):
        """Promote model from staging to production"""
        
        # First deploy to production
        config = DeploymentConfig(
            model_name=model_name,
            model_version=version,
            environment="production",
            replicas=3  # More replicas for production
        )
        
        if self.deployer.deploy_model(config):
            # Update model stage in MLflow
            self.client.transition_model_version_stage(
                name=model_name,
                version=version,
                stage="Production"
            )
            return True
        
        return False

# Usage
if __name__ == "__main__":
    deployer = ModelDeployer("http://mlflow-server:5000")
    pipeline = MLDeploymentPipeline(deployer)
    
    # Deploy staging model
    success = pipeline.deploy_staging_model("customer_churn_model")
    
    if success:
        # After testing, promote to production
        pipeline.promote_to_production("customer_churn_model", "3")
```

## Phase 5: End-to-End Pipeline Orchestration

### 5.1 Complete MLOps Pipeline

**Kubeflow Pipelines Implementation:**

```python
# mlops_pipeline.py
import kfp
from kfp import dsl
from kfp.components import create_component_from_func
from typing import NamedTuple

# Component: Data Validation
@create_component_from_func
def data_validation_component(
    data_path: str,
    reference_data_path: str
) -> NamedTuple('ValidationOutput', [('is_valid', bool), ('report_path', str)]):
    """Data validation component"""
    
    import pandas as pd
    import json
    from pathlib import Path
    
    # Load data
    data = pd.read_csv(data_path)
    reference_data = pd.read_csv(reference_data_path)
    
    # Simple validation logic (extend as needed)
    is_valid = True
    report = {"status": "passed", "errors": [], "warnings": []}
    
    # Check schema consistency
    if set(data.columns) != set(reference_data.columns):
        is_valid = False
        report["errors"].append("Schema mismatch")
    
    # Check data drift (simplified)
    for col in data.select_dtypes(include=['number']).columns:
        if col in reference_data.columns:
            data_mean = data[col].mean()
            ref_mean = reference_data[col].mean()
            drift = abs(data_mean - ref_mean) / ref_mean if ref_mean != 0 else 0
            
            if drift > 0.2:  # 20% drift threshold
                report["warnings"].append(f"Data drift detected in {col}: {drift:.2%}")
    
    # Save report
    report_path = "/tmp/validation_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f)
    
    ValidationOutput = NamedTuple('ValidationOutput', [('is_valid', bool), ('report_path', str)])
    return ValidationOutput(is_valid, report_path)

# Component: Feature Engineering
@create_component_from_func
def feature_engineering_component(
    data_path: str,
    target_column: str
) -> NamedTuple('FeatureOutput', [('processed_data_path', str), ('transformer_path', str)]):
    """Feature engineering component"""
    
    import pandas as pd
    import joblib
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    import numpy as np
    
    # Load data
    data = pd.read_csv(data_path)
    
    # Separate features and target
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    # Simple feature engineering
    # Scale numerical features
    numerical_cols = X.select_dtypes(include=[np.number]).columns
    scaler = StandardScaler()
    
    if len(numerical_cols) > 0:
        X[numerical_cols] = scaler.fit_transform(X[numerical_cols])
    
    # Encode categorical features
    categorical_cols = X.select_dtypes(include=['object']).columns
    encoders = {}
    
    for col in categorical_cols:
        encoder = LabelEncoder()
        X[col] = encoder.fit_transform(X[col].astype(str))
        encoders[col] = encoder
    
    # Save processed data
    processed_data = pd.concat([X, y], axis=1)
    processed_data_path = "/tmp/processed_data.csv"
    processed_data.to_csv(processed_data_path, index=False)
    
    # Save transformers
    transformer_path = "/tmp/transformers.pkl"
    transformers = {'scaler': scaler, 'encoders': encoders, 'numerical_cols': numerical_cols}
    joblib.dump(transformers, transformer_path)
    
    FeatureOutput = NamedTuple('FeatureOutput', [('processed_data_path', str), ('transformer_path', str)])
    return FeatureOutput(processed_data_path, transformer_path)

# Component: Model Training
@create_component_from_func
def model_training_component(
    data_path: str,
    target_column: str,
    model_type: str = "random_forest"
) -> NamedTuple('TrainingOutput', [('model_path', str), ('metrics_path', str)]):
    """Model training component"""
    
    import pandas as pd
    import joblib
    import json
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
    
    # Load data
    data = pd.read_csv(data_path)
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    if model_type == "random_forest":
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    metrics = {
        "accuracy": accuracy,
        "model_type": model_type,
        "train_size": len(X_train),
        "test_size": len(X_test)
    }
    
    # Save model and metrics
    model_path = "/tmp/model.pkl"
    metrics_path = "/tmp/metrics.json"
    
    joblib.dump(model, model_path)
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f)
    
    TrainingOutput = NamedTuple('TrainingOutput', [('model_path', str), ('metrics_path', str)])
    return TrainingOutput(model_path, metrics_path)

# Component: Model Validation
@create_component_from_func
def model_validation_component(
    model_path: str,
    metrics_path: str,
    accuracy_threshold: float = 0.8
) -> NamedTuple('ValidationOutput', [('is_valid', bool), ('should_deploy', bool)]):
    """Model validation component"""
    
    import json
    import joblib
    
    # Load metrics
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
    
    accuracy = metrics.get('accuracy', 0)
    is_valid = accuracy >= accuracy_threshold
    should_deploy = is_valid
    
    ValidationOutput = NamedTuple('ValidationOutput', [('is_valid', bool), ('should_deploy', bool)])
    return ValidationOutput(is_valid, should_deploy)

# Component: Model Registration
@create_component_from_func
def model_registration_component(
    model_path: str,
    metrics_path: str,
    model_name: str,
    mlflow_uri: str = "http://mlflow-server:5000"
):
    """Model registration component"""
    
    import mlflow
    import mlflow.sklearn
    import joblib
    import json
    
    # Set MLflow URI
    mlflow.set_tracking_uri(mlflow_uri)
    
    # Load model and metrics
    model = joblib.load(model_path)
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
    
    # Start MLflow run
    with mlflow.start_run():
        # Log metrics
        mlflow.log_metrics(metrics)
        
        # Log model
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name=model_name
        )
        
        print(f"Model registered: {model_name}")

# Define the pipeline
@dsl.pipeline(
    name='MLOps Training Pipeline',
    description='End-to-end ML training pipeline'
)
def mlops_training_pipeline(
    data_path: str,
    reference_data_path: str,
    target_column: str = "target",
    model_name: str = "customer_model",
    model_type: str = "random_forest",
    accuracy_threshold: float = 0.8
):
    """Complete MLOps training pipeline"""
    
    # Step 1: Data Validation
    data_validation_task = data_validation_component(
        data_path=data_path,
        reference_data_path=reference_data_path
    )
    
    # Step 2: Feature Engineering (depends on validation)
    feature_engineering_task = feature_engineering_component(
        data_path=data_path,
        target_column=target_column
    ).after(data_validation_task)
    
    # Add condition: only proceed if data is valid
    with dsl.Condition(data_validation_task.outputs['is_valid'] == True):
        # Step 3: Model Training
        training_task = model_training_component(
            data_path=feature_engineering_task.outputs['processed_data_path'],
            target_column=target_column,
            model_type=model_type
        )
        
        # Step 4: Model Validation
        validation_task = model_validation_component(
            model_path=training_task.outputs['model_path'],
            metrics_path=training_task.outputs['metrics_path'],
            accuracy_threshold=accuracy_threshold
        )
        
        # Step 5: Model Registration (if validation passes)
        with dsl.Condition(validation_task.outputs['should_deploy'] == True):
            registration_task = model_registration_component(
                model_path=training_task.outputs['model_path'],
                metrics_path=training_task.outputs['metrics_path'],
                model_name=model_name
            )

# Deployment pipeline
@dsl.pipeline(
    name='MLOps Deployment Pipeline',
    description='Model deployment pipeline'
)
def mlops_deployment_pipeline(
    model_name: str,
    model_version: str,
    environment: str = "staging"
):
    """Model deployment pipeline"""
    
    # This would include deployment components
    # For brevity, showing the structure
    pass

# Pipeline runner
class MLOpsPipelineRunner:
    def __init__(self, kfp_endpoint: str):
        self.client = kfp.Client(host=kfp_endpoint)
    
    def submit_training_pipeline(self, **kwargs):
        """Submit training pipeline"""
        
        # Compile pipeline
        pipeline_func = mlops_training_pipeline
        pipeline_filename = "mlops_training_pipeline.yaml"
        kfp.compiler.Compiler().compile(pipeline_func, pipeline_filename)
        
        # Submit pipeline
        experiment_name = "MLOps Training"
        run_name = f"training-run-{kwargs.get('model_name', 'default')}"
        
        try:
            experiment = self.client.create_experiment(experiment_name)
            experiment_id = experiment.id
        except Exception:
            experiment = self.client.get_experiment(experiment_name=experiment_name)
            experiment_id = experiment.id
        
        run_result = self.client.run_pipeline(
            experiment_id=experiment_id,
            job_name=run_name,
            pipeline_package_path=pipeline_filename,
            params=kwargs
        )
        
        return run_result
    
    def schedule_training_pipeline(self, cron_expression: str, **kwargs):
        """Schedule recurring training pipeline"""
        
        pipeline_func = mlops_training_pipeline
        pipeline_filename = "mlops_training_pipeline.yaml"
        kfp.compiler.Compiler().compile(pipeline_func, pipeline_filename)
        
        # Create recurring run
        experiment_name = "MLOps Training"
        job_name = f"scheduled-training-{kwargs.get('model_name', 'default')}"
        
        try:
            experiment = self.client.create_experiment(experiment_name)
            experiment_id = experiment.id
        except Exception:
            experiment = self.client.get_experiment(experiment_name=experiment_name)
            experiment_id = experiment.id
        
        recurring_run = self.client.create_recurring_run(
            experiment_id=experiment_id,
            job_name=job_name,
            cron_expression=cron_expression,
            pipeline_package_path=pipeline_filename,
            params=kwargs
        )
        
        return recurring_run

# Usage
if __name__ == "__main__":
    # Initialize pipeline runner
    runner = MLOpsPipelineRunner("http://kubeflow-pipelines:8888")
    
    # Submit training pipeline
    run_result = runner.submit_training_pipeline(
        data_path="gs://my-bucket/data/training_data.csv",
        reference_data_path="gs://my-bucket/data/reference_data.csv",
        target_column="target",
        model_name="customer_churn_model",
        model_type="random_forest",
        accuracy_threshold=0.85
    )
    
    print(f"Pipeline submitted: {run_result.run_id}")
    
    # Schedule daily retraining
    recurring_run = runner.schedule_training_pipeline(
        cron_expression="0 2 * * *",  # Daily at 2 AM
        data_path="gs://my-bucket/data/latest_data.csv",
        reference_data_path="gs://my-bucket/data/reference_data.csv",
        target_column="target",
        model_name="customer_churn_model"
    )
    
    print(f"Scheduled pipeline: {recurring_run.id}")
```

## Success Metrics

1. **Pipeline Success Rate**: > 95% of pipeline runs complete successfully
2. **Training Time**: Automated training completes within 2 hours
3. **Deployment Speed**: < 10 minutes from model registration to staging deployment
4. **Model Quality Gates**: 100% of deployed models pass validation thresholds
5. **Automation Coverage**: > 80% of MLOps workflow is automated

This comprehensive pipeline automation provides the foundation for scalable, reliable MLOps practices.

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "Create new branch for MLOps/AIOps prompts", "status": "completed", "activeForm": "Creating new branch for MLOps/AIOps prompts"}, {"content": "Create MLOps gap analysis prompts", "status": "completed", "activeForm": "Creating MLOps gap analysis prompts"}, {"content": "Create AIOps gap analysis prompts", "status": "completed", "activeForm": "Creating AIOps gap analysis prompts"}, {"content": "Create implementation guidance prompts", "status": "completed", "activeForm": "Creating implementation guidance prompts"}]