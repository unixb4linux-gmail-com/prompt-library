---
version: "1.0.0"
created_date: "2025-01-02"
last_updated: "2025-01-02"
enhancement_level: "advanced"
prompt_techniques: ["step_by_step_guidance", "best_practices", "code_generation", "deployment_automation"]
---

# MLflow Model Registry Implementation Guide

> **Implementation Directive:**
> 
> **Scope:** Set up a production-ready MLflow Model Registry with experiment tracking, model versioning, and deployment automation
> 
> **Prerequisites:** Basic understanding of Docker, Python, and ML workflows

## Phase 1: Infrastructure Setup

### 1.1 MLflow Server Deployment

**Option A: Docker Compose (Recommended for Start)**

Create a `docker-compose.yml` for MLflow with PostgreSQL backend:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: mlflow
      POSTGRES_USER: mlflow
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-mlflow123}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  minio:
    image: minio/minio:latest
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER:-minio}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:-minio123}
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    restart: unless-stopped

  mlflow:
    image: mlflow/mlflow:latest
    environment:
      MLFLOW_BACKEND_STORE_URI: postgresql://mlflow:${POSTGRES_PASSWORD:-mlflow123}@postgres:5432/mlflow
      MLFLOW_DEFAULT_ARTIFACT_ROOT: s3://mlflow-artifacts/
      AWS_ACCESS_KEY_ID: ${MINIO_ROOT_USER:-minio}
      AWS_SECRET_ACCESS_KEY: ${MINIO_ROOT_PASSWORD:-minio123}
      MLFLOW_S3_ENDPOINT_URL: http://minio:9000
    command: >
      mlflow server 
      --backend-store-uri postgresql://mlflow:${POSTGRES_PASSWORD:-mlflow123}@postgres:5432/mlflow
      --default-artifact-root s3://mlflow-artifacts/
      --host 0.0.0.0
      --port 5000
    ports:
      - "5000:5000"
    depends_on:
      - postgres
      - minio
    restart: unless-stopped

volumes:
  postgres_data:
  minio_data:
```

**Option B: Kubernetes Deployment**

Create Kubernetes manifests for production deployment:

```yaml
# mlflow-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: mlflow

---
# mlflow-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlflow-server
  namespace: mlflow
spec:
  replicas: 2
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
        - name: MLFLOW_BACKEND_STORE_URI
          value: "postgresql://mlflow:password@postgres:5432/mlflow"
        - name: MLFLOW_DEFAULT_ARTIFACT_ROOT
          value: "s3://mlflow-artifacts/"
        command:
        - mlflow
        - server
        - --backend-store-uri
        - postgresql://mlflow:password@postgres:5432/mlflow
        - --default-artifact-root
        - s3://mlflow-artifacts/
        - --host
        - 0.0.0.0
        - --port
        - "5000"

---
# mlflow-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: mlflow-server
  namespace: mlflow
spec:
  selector:
    app: mlflow-server
  ports:
  - port: 5000
    targetPort: 5000
  type: LoadBalancer
```

### 1.2 Security Configuration

**Authentication Setup:**

```python
# mlflow_auth.py
import mlflow
from mlflow.server.auth import create_user, get_user

# Basic authentication setup
def setup_mlflow_auth():
    # Create admin user
    create_user(
        username="admin",
        password="secure_password",
        is_admin=True
    )
    
    # Create team users
    users = [
        ("ml_engineer", "ml_password", False),
        ("data_scientist", "ds_password", False),
        ("ml_ops", "ops_password", True)
    ]
    
    for username, password, is_admin in users:
        create_user(username, password, is_admin)

if __name__ == "__main__":
    setup_mlflow_auth()
```

**Environment Variables for Security:**

```bash
# .env file
MLFLOW_TRACKING_USERNAME=your_username
MLFLOW_TRACKING_PASSWORD=your_password
MLFLOW_TRACKING_URI=https://your-mlflow-server.com

# For cloud deployments
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
```

## Phase 2: Model Registry Integration

### 2.1 Python Client Configuration

**Basic MLflow Setup:**

```python
# mlflow_config.py
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import os
from pathlib import Path

class MLflowManager:
    def __init__(self, tracking_uri=None, registry_uri=None):
        self.tracking_uri = tracking_uri or os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
        self.registry_uri = registry_uri or self.tracking_uri
        
        mlflow.set_tracking_uri(self.tracking_uri)
        mlflow.set_registry_uri(self.registry_uri)
        
        self.client = MlflowClient(tracking_uri=self.tracking_uri, registry_uri=self.registry_uri)
    
    def create_experiment(self, name, tags=None):
        """Create a new experiment with optional tags"""
        try:
            experiment_id = mlflow.create_experiment(
                name=name,
                tags=tags or {}
            )
            return experiment_id
        except Exception as e:
            print(f"Experiment {name} already exists or error: {e}")
            return mlflow.get_experiment_by_name(name).experiment_id
    
    def start_run(self, experiment_name, run_name=None, tags=None):
        """Start an MLflow run with proper experiment setting"""
        experiment = mlflow.get_experiment_by_name(experiment_name)
        if not experiment:
            self.create_experiment(experiment_name)
        
        mlflow.set_experiment(experiment_name)
        return mlflow.start_run(run_name=run_name, tags=tags or {})

# Usage example
mlflow_manager = MLflowManager()
```

### 2.2 Model Training Integration

**Complete Training Pipeline with MLflow:**

```python
# model_training.py
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from mlflow_config import MLflowManager
import joblib
import json

class MLModelTrainer:
    def __init__(self, mlflow_manager):
        self.mlflow_manager = mlflow_manager
        self.model = None
        self.model_name = None
    
    def train_model(self, data, target_column, model_name, experiment_name="default"):
        """Train model with comprehensive MLflow tracking"""
        
        # Prepare data
        X = data.drop(columns=[target_column])
        y = data[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model_name = model_name
        
        with self.mlflow_manager.start_run(
            experiment_name=experiment_name,
            run_name=f"{model_name}_training",
            tags={
                "model_type": "classification",
                "algorithm": "random_forest",
                "version": "v1.0"
            }
        ):
            # Model parameters
            params = {
                "n_estimators": 100,
                "max_depth": 10,
                "random_state": 42,
                "n_jobs": -1
            }
            
            # Log parameters
            mlflow.log_params(params)
            
            # Log dataset info
            mlflow.log_param("train_samples", len(X_train))
            mlflow.log_param("test_samples", len(X_test))
            mlflow.log_param("features", list(X.columns))
            
            # Train model
            self.model = RandomForestClassifier(**params)
            self.model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = self.model.predict(X_test)
            
            # Calculate metrics
            metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "precision": precision_score(y_test, y_pred, average='weighted'),
                "recall": recall_score(y_test, y_pred, average='weighted'),
                "f1_score": f1_score(y_test, y_pred, average='weighted')
            }
            
            # Log metrics
            mlflow.log_metrics(metrics)
            
            # Log model
            mlflow.sklearn.log_model(
                sk_model=self.model,
                artifact_path="model",
                registered_model_name=model_name,
                input_example=X_train.iloc[:5],
                signature=mlflow.models.infer_signature(X_train, y_pred)
            )
            
            # Log additional artifacts
            feature_importance = pd.DataFrame({
                'feature': X.columns,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            feature_importance.to_csv("feature_importance.csv", index=False)
            mlflow.log_artifact("feature_importance.csv")
            
            # Log model metadata
            model_metadata = {
                "model_type": "RandomForestClassifier",
                "sklearn_version": mlflow.sklearn.__version__,
                "training_date": str(pd.Timestamp.now()),
                "data_shape": data.shape,
                "target_column": target_column
            }
            
            with open("model_metadata.json", "w") as f:
                json.dump(model_metadata, f, indent=2)
            mlflow.log_artifact("model_metadata.json")
            
            print(f"Model training completed. Run ID: {mlflow.active_run().info.run_id}")
            return metrics

# Usage
if __name__ == "__main__":
    # Load your data
    data = pd.read_csv("your_dataset.csv")
    
    mlflow_manager = MLflowManager()
    trainer = MLModelTrainer(mlflow_manager)
    
    metrics = trainer.train_model(
        data=data,
        target_column="target",
        model_name="customer_churn_model",
        experiment_name="churn_prediction"
    )
    
    print("Training metrics:", metrics)
```

### 2.3 Model Registry Management

**Model Lifecycle Management:**

```python
# model_registry.py
import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
import pandas as pd
from datetime import datetime, timedelta

class ModelRegistry:
    def __init__(self, mlflow_manager):
        self.client = mlflow_manager.client
        self.tracking_uri = mlflow_manager.tracking_uri
    
    def register_model(self, run_id, model_name, artifact_path="model"):
        """Register a model from a specific run"""
        model_uri = f"runs:/{run_id}/{artifact_path}"
        
        try:
            model_version = mlflow.register_model(model_uri, model_name)
            print(f"Model {model_name} version {model_version.version} registered")
            return model_version
        except Exception as e:
            print(f"Error registering model: {e}")
            return None
    
    def promote_model(self, model_name, version, stage):
        """Promote model to different stages"""
        valid_stages = ["Staging", "Production", "Archived"]
        if stage not in valid_stages:
            raise ValueError(f"Stage must be one of {valid_stages}")
        
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage
        )
        print(f"Model {model_name} version {version} promoted to {stage}")
    
    def get_model_versions(self, model_name, stages=None):
        """Get all versions of a model, optionally filtered by stage"""
        versions = self.client.get_latest_versions(
            model_name,
            stages=stages or ["None", "Staging", "Production"]
        )
        return versions
    
    def compare_models(self, model_name, versions=None):
        """Compare different versions of a model"""
        if not versions:
            versions = self.get_model_versions(model_name)
        
        comparison_data = []
        
        for version in versions:
            run = self.client.get_run(version.run_id)
            metrics = run.data.metrics
            params = run.data.params
            
            comparison_data.append({
                "version": version.version,
                "stage": version.current_stage,
                "run_id": version.run_id,
                "created_at": version.creation_timestamp,
                **metrics,
                **params
            })
        
        return pd.DataFrame(comparison_data)
    
    def get_production_model(self, model_name):
        """Get the current production model"""
        production_versions = self.client.get_latest_versions(
            model_name,
            stages=["Production"]
        )
        
        if production_versions:
            return production_versions[0]
        else:
            print(f"No production version found for {model_name}")
            return None
    
    def archive_old_models(self, model_name, keep_versions=5):
        """Archive old model versions, keeping only the specified number"""
        all_versions = self.client.search_model_versions(f"name='{model_name}'")
        
        # Sort by version number (descending)
        all_versions = sorted(all_versions, key=lambda x: int(x.version), reverse=True)
        
        # Archive versions beyond the keep limit
        for version in all_versions[keep_versions:]:
            if version.current_stage not in ["Production", "Staging"]:
                self.client.transition_model_version_stage(
                    name=model_name,
                    version=version.version,
                    stage="Archived"
                )
                print(f"Archived {model_name} version {version.version}")

# Usage
registry = ModelRegistry(mlflow_manager)

# Register a model from a run
model_version = registry.register_model(
    run_id="your_run_id",
    model_name="customer_churn_model"
)

# Promote to staging
registry.promote_model(
    model_name="customer_churn_model",
    version=model_version.version,
    stage="Staging"
)

# Compare model versions
comparison = registry.compare_models("customer_churn_model")
print(comparison)
```

## Phase 3: CI/CD Integration

### 3.1 Automated Model Training Pipeline

**GitHub Actions Workflow:**

```yaml
# .github/workflows/model_training.yml
name: Model Training Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * 1'  # Weekly on Monday at 2 AM

env:
  MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
  MLFLOW_TRACKING_USERNAME: ${{ secrets.MLFLOW_TRACKING_USERNAME }}
  MLFLOW_TRACKING_PASSWORD: ${{ secrets.MLFLOW_TRACKING_PASSWORD }}

jobs:
  train-model:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run data validation
      run: |
        python scripts/validate_data.py
    
    - name: Train model
      run: |
        python scripts/train_model.py
    
    - name: Validate model performance
      run: |
        python scripts/validate_model.py
    
    - name: Register model
      if: success()
      run: |
        python scripts/register_model.py

  deploy-staging:
    needs: train-model
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    
    steps:
    - name: Deploy to staging
      run: |
        python scripts/deploy_staging.py
    
    - name: Run integration tests
      run: |
        python scripts/test_staging.py
```

### 3.2 Model Deployment Automation

**Deployment Script:**

```python
# deploy_model.py
import mlflow
import mlflow.pyfunc
import requests
import json
from mlflow_config import MLflowManager
from model_registry import ModelRegistry

class ModelDeployer:
    def __init__(self, mlflow_manager):
        self.mlflow_manager = mlflow_manager
        self.registry = ModelRegistry(mlflow_manager)
    
    def deploy_to_staging(self, model_name):
        """Deploy latest staging model to staging environment"""
        staging_versions = self.registry.get_model_versions(
            model_name, 
            stages=["Staging"]
        )
        
        if not staging_versions:
            raise Exception(f"No staging version found for {model_name}")
        
        latest_staging = staging_versions[0]
        model_uri = f"models:/{model_name}/{latest_staging.version}"
        
        # Load model for validation
        model = mlflow.pyfunc.load_model(model_uri)
        
        # Deploy to staging endpoint (example with REST API)
        deployment_config = {
            "model_uri": model_uri,
            "model_name": model_name,
            "model_version": latest_staging.version,
            "environment": "staging"
        }
        
        # Your deployment logic here
        self._deploy_to_endpoint(deployment_config, "staging")
        
        print(f"Deployed {model_name} v{latest_staging.version} to staging")
        return latest_staging
    
    def promote_to_production(self, model_name, version=None):
        """Promote a staging model to production"""
        if version is None:
            staging_versions = self.registry.get_model_versions(
                model_name, 
                stages=["Staging"]
            )
            if not staging_versions:
                raise Exception("No staging version to promote")
            version = staging_versions[0].version
        
        # Run final validation
        if self._validate_model(model_name, version):
            # Promote in registry
            self.registry.promote_model(model_name, version, "Production")
            
            # Deploy to production
            model_uri = f"models:/{model_name}/{version}"
            deployment_config = {
                "model_uri": model_uri,
                "model_name": model_name,
                "model_version": version,
                "environment": "production"
            }
            
            self._deploy_to_endpoint(deployment_config, "production")
            
            print(f"Promoted {model_name} v{version} to production")
            return True
        
        return False
    
    def _validate_model(self, model_name, version):
        """Validate model before production deployment"""
        model_uri = f"models:/{model_name}/{version}"
        model = mlflow.pyfunc.load_model(model_uri)
        
        # Add your validation logic here
        # e.g., performance tests, A/B test results, etc.
        
        return True
    
    def _deploy_to_endpoint(self, config, environment):
        """Deploy model to serving endpoint"""
        # Example deployment to a REST API endpoint
        # Adapt this to your deployment infrastructure
        
        endpoint_url = f"https://api.{environment}.yourcompany.com/models/deploy"
        
        headers = {
            "Authorization": f"Bearer {os.getenv('DEPLOYMENT_TOKEN')}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(endpoint_url, json=config, headers=headers)
        response.raise_for_status()
        
        return response.json()

# Usage
deployer = ModelDeployer(mlflow_manager)

# Deploy to staging
staging_version = deployer.deploy_to_staging("customer_churn_model")

# After validation, promote to production
success = deployer.promote_to_production("customer_churn_model", staging_version.version)
```

## Phase 4: Monitoring and Alerting

### 4.1 Model Performance Monitoring

**Model Monitoring Setup:**

```python
# model_monitoring.py
import mlflow
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import schedule
import time
from mlflow_config import MLflowManager

class ModelMonitor:
    def __init__(self, mlflow_manager):
        self.mlflow_manager = mlflow_manager
        self.client = mlflow_manager.client
    
    def log_prediction_metrics(self, model_name, predictions, actuals=None, 
                             input_data=None, timestamp=None):
        """Log prediction metrics for monitoring"""
        timestamp = timestamp or datetime.now()
        
        with mlflow.start_run(
            experiment_id=self._get_monitoring_experiment(),
            run_name=f"{model_name}_monitoring_{timestamp.strftime('%Y%m%d_%H%M')}"
        ):
            # Log basic prediction statistics
            pred_stats = {
                "prediction_count": len(predictions),
                "prediction_mean": np.mean(predictions),
                "prediction_std": np.std(predictions),
                "prediction_min": np.min(predictions),
                "prediction_max": np.max(predictions)
            }
            
            mlflow.log_metrics(pred_stats)
            
            # If ground truth is available, calculate performance metrics
            if actuals is not None:
                performance_metrics = self._calculate_performance_metrics(
                    predictions, actuals
                )
                mlflow.log_metrics(performance_metrics)
            
            # Log data drift metrics if input data provided
            if input_data is not None:
                drift_metrics = self._calculate_data_drift(model_name, input_data)
                mlflow.log_metrics(drift_metrics)
            
            # Log timestamp
            mlflow.log_param("monitoring_timestamp", timestamp.isoformat())
            mlflow.log_param("model_name", model_name)
    
    def _get_monitoring_experiment(self):
        """Get or create monitoring experiment"""
        exp_name = "model_monitoring"
        try:
            return self.mlflow_manager.create_experiment(exp_name)
        except:
            return mlflow.get_experiment_by_name(exp_name).experiment_id
    
    def _calculate_performance_metrics(self, predictions, actuals):
        """Calculate performance metrics"""
        from sklearn.metrics import accuracy_score, precision_score, recall_score
        
        return {
            "accuracy": accuracy_score(actuals, predictions),
            "precision": precision_score(actuals, predictions, average='weighted'),
            "recall": recall_score(actuals, predictions, average='weighted')
        }
    
    def _calculate_data_drift(self, model_name, current_data):
        """Calculate data drift metrics"""
        # Get reference data from training
        # This is a simplified example - use proper drift detection libraries
        # like evidently or alibi-detect for production
        
        # For now, just log data statistics
        drift_metrics = {}
        
        for column in current_data.select_dtypes(include=[np.number]).columns:
            drift_metrics[f"{column}_mean"] = current_data[column].mean()
            drift_metrics[f"{column}_std"] = current_data[column].std()
        
        return drift_metrics
    
    def check_model_health(self, model_name, threshold_accuracy=0.85):
        """Check if model performance is degrading"""
        # Get recent monitoring runs
        experiment = mlflow.get_experiment_by_name("model_monitoring")
        runs = mlflow.search_runs(
            experiment_ids=[experiment.experiment_id],
            filter_string=f"params.model_name = '{model_name}'",
            order_by=["start_time DESC"],
            max_results=10
        )
        
        if len(runs) > 0:
            latest_accuracy = runs.iloc[0].get('metrics.accuracy', 0)
            
            if latest_accuracy < threshold_accuracy:
                self._send_alert(
                    model_name, 
                    f"Model accuracy dropped to {latest_accuracy:.3f}"
                )
                return False
        
        return True
    
    def _send_alert(self, model_name, message):
        """Send alert for model performance issues"""
        # Implement your alerting logic here
        # e.g., Slack, email, PagerDuty, etc.
        print(f"ALERT for {model_name}: {message}")

# Setup monitoring job
def monitoring_job():
    monitor = ModelMonitor(mlflow_manager)
    
    # Example: Monitor production models
    production_models = ["customer_churn_model", "fraud_detection_model"]
    
    for model_name in production_models:
        monitor.check_model_health(model_name)

# Schedule monitoring
schedule.every(1).hours.do(monitoring_job)

# Keep the monitoring running
while True:
    schedule.run_pending()
    time.sleep(60)
```

## Phase 5: Best Practices and Governance

### 5.1 Model Governance Framework

**Model Approval Workflow:**

```python
# model_governance.py
import mlflow
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
import json
from datetime import datetime

class ModelStage(Enum):
    DEVELOPMENT = "None"
    STAGING = "Staging"
    PRODUCTION = "Production"
    ARCHIVED = "Archived"

@dataclass
class ModelApproval:
    approver: str
    approval_date: datetime
    comments: str
    performance_metrics: dict

class ModelGovernance:
    def __init__(self, mlflow_manager):
        self.mlflow_manager = mlflow_manager
        self.client = mlflow_manager.client
    
    def request_promotion(self, model_name, version, target_stage, 
                         requester, justification, performance_metrics):
        """Request model promotion with approval workflow"""
        
        # Add promotion request tags
        self.client.set_model_version_tag(
            name=model_name,
            version=version,
            key="promotion_request",
            value=json.dumps({
                "target_stage": target_stage,
                "requester": requester,
                "request_date": datetime.now().isoformat(),
                "justification": justification,
                "performance_metrics": performance_metrics,
                "status": "pending"
            })
        )
        
        print(f"Promotion request submitted for {model_name} v{version} to {target_stage}")
        return True
    
    def approve_promotion(self, model_name, version, approver, comments=""):
        """Approve model promotion"""
        
        # Get current promotion request
        model_version = self.client.get_model_version(model_name, version)
        promotion_tag = model_version.tags.get("promotion_request")
        
        if not promotion_tag:
            raise ValueError("No pending promotion request found")
        
        promotion_data = json.loads(promotion_tag)
        target_stage = promotion_data["target_stage"]
        
        # Record approval
        approval = ModelApproval(
            approver=approver,
            approval_date=datetime.now(),
            comments=comments,
            performance_metrics=promotion_data["performance_metrics"]
        )
        
        # Update tags
        self.client.set_model_version_tag(
            name=model_name,
            version=version,
            key="approval",
            value=json.dumps({
                "approver": approval.approver,
                "approval_date": approval.approval_date.isoformat(),
                "comments": approval.comments
            })
        )
        
        # Promote model
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=target_stage
        )
        
        # Update promotion request status
        promotion_data["status"] = "approved"
        promotion_data["approved_by"] = approver
        promotion_data["approved_date"] = datetime.now().isoformat()
        
        self.client.set_model_version_tag(
            name=model_name,
            version=version,
            key="promotion_request",
            value=json.dumps(promotion_data)
        )
        
        print(f"Model {model_name} v{version} promoted to {target_stage}")
        return True
    
    def get_model_lineage(self, model_name, version):
        """Get complete lineage information for a model"""
        model_version = self.client.get_model_version(model_name, version)
        run = self.client.get_run(model_version.run_id)
        
        lineage = {
            "model_name": model_name,
            "version": version,
            "run_id": model_version.run_id,
            "creation_date": model_version.creation_timestamp,
            "current_stage": model_version.current_stage,
            "tags": model_version.tags,
            "metrics": run.data.metrics,
            "parameters": run.data.params,
            "artifacts": [artifact.path for artifact in self.client.list_artifacts(run.info.run_id)]
        }
        
        return lineage
    
    def generate_model_report(self, model_name):
        """Generate comprehensive model report"""
        versions = self.client.search_model_versions(f"name='{model_name}'")
        
        report = {
            "model_name": model_name,
            "total_versions": len(versions),
            "current_production_version": None,
            "version_history": []
        }
        
        for version in versions:
            if version.current_stage == "Production":
                report["current_production_version"] = version.version
            
            run = self.client.get_run(version.run_id)
            
            version_info = {
                "version": version.version,
                "stage": version.current_stage,
                "creation_date": version.creation_timestamp,
                "metrics": run.data.metrics,
                "tags": version.tags
            }
            
            report["version_history"].append(version_info)
        
        return report

# Usage
governance = ModelGovernance(mlflow_manager)

# Request promotion
governance.request_promotion(
    model_name="customer_churn_model",
    version="3",
    target_stage="Production",
    requester="data_scientist@company.com",
    justification="Improved accuracy by 5% over current production model",
    performance_metrics={"accuracy": 0.92, "precision": 0.89, "recall": 0.94}
)

# Approve promotion
governance.approve_promotion(
    model_name="customer_churn_model",
    version="3",
    approver="ml_lead@company.com",
    comments="Performance validated in staging environment"
)
```

## Next Steps

1. **Deploy MLflow Server** using Docker Compose or Kubernetes
2. **Integrate with existing ML workflows** by updating training scripts
3. **Set up CI/CD pipelines** for automated model training and deployment
4. **Implement monitoring** to track model performance in production
5. **Establish governance** processes for model approvals and compliance

## Success Metrics

- **Experiment Tracking**: All ML experiments logged and tracked
- **Model Versioning**: Clear model lineage and version history
- **Deployment Automation**: Automated promotion from staging to production
- **Performance Monitoring**: Real-time visibility into model performance
- **Governance Compliance**: All model changes approved and documented

This implementation provides a robust foundation for MLOps practices with MLflow Model Registry.