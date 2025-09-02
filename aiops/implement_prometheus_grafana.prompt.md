---
version: "1.0.0"
created_date: "2025-01-02"
last_updated: "2025-01-02"
enhancement_level: "advanced"
prompt_techniques: ["step_by_step_guidance", "best_practices", "infrastructure_as_code", "monitoring_automation"]
---

# Prometheus & Grafana AIOps Implementation Guide

> **Implementation Directive:**
> 
> **Scope:** Deploy production-ready Prometheus monitoring and Grafana dashboards with automated alerting and incident response
> 
> **Prerequisites:** Basic understanding of containers, Kubernetes, and monitoring concepts

## Phase 1: Infrastructure Setup

### 1.1 Prometheus Stack Deployment

**Option A: Docker Compose (Development/Small Scale)**

Create a comprehensive monitoring stack:

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus/rules:/etc/prometheus/rules
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
      - '--web.enable-admin-api'
      - '--storage.tsdb.retention.time=30d'
    networks:
      - monitoring
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
      - ./grafana/dashboards:/var/lib/grafana/dashboards
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-admin123}
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_SMTP_ENABLED=true
      - GF_SMTP_HOST=${SMTP_HOST:-localhost:587}
      - GF_SMTP_USER=${SMTP_USER:-}
      - GF_SMTP_PASSWORD=${SMTP_PASSWORD:-}
    networks:
      - monitoring
    depends_on:
      - prometheus
    restart: unless-stopped

  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
      - '--web.external-url=http://localhost:9093'
    networks:
      - monitoring
    restart: unless-stopped

  node_exporter:
    image: prom/node-exporter:latest
    container_name: node_exporter
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    networks:
      - monitoring
    restart: unless-stopped

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    privileged: true
    devices:
      - /dev/kmsg
    networks:
      - monitoring
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
  alertmanager_data:

networks:
  monitoring:
    driver: bridge
```

**Option B: Kubernetes with Helm (Production)**

```yaml
# monitoring-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: monitoring

---
# prometheus-values.yaml for Helm
prometheus:
  prometheusSpec:
    retention: 30d
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: fast-ssd
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 100Gi
    
    additionalScrapeConfigs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)

grafana:
  adminPassword: ${GRAFANA_ADMIN_PASSWORD}
  persistence:
    enabled: true
    storageClassName: fast-ssd
    size: 10Gi
  
  datasources:
    datasources.yaml:
      apiVersion: 1
      datasources:
        - name: Prometheus
          type: prometheus
          url: http://prometheus-server
          access: proxy
          isDefault: true

alertmanager:
  alertmanagerSpec:
    storage:
      volumeClaimTemplate:
        spec:
          storageClassName: fast-ssd
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 10Gi
```

Install with Helm:

```bash
# Install prometheus-operator
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --values prometheus-values.yaml
```

### 1.2 Prometheus Configuration

**Main Prometheus Configuration:**

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    region: 'us-east-1'

rule_files:
  - "rules/*.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node_exporter:9100']
    scrape_interval: 5s

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
    scrape_interval: 5s

  - job_name: 'application-metrics'
    static_configs:
      - targets: ['app1:8080', 'app2:8080']
    metrics_path: /metrics
    scrape_interval: 10s
    scrape_timeout: 5s

  # Service discovery for Kubernetes
  - job_name: 'kubernetes-apiservers'
    kubernetes_sd_configs:
      - role: endpoints
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https

  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
      - role: node
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)

  # Custom application monitoring
  - job_name: 'ml-services'
    static_configs:
      - targets: ['ml-service-1:9090', 'ml-service-2:9090']
    scrape_interval: 30s
    metrics_path: /metrics
```

## Phase 2: Alerting Rules and Automation

### 2.1 Comprehensive Alerting Rules

**Infrastructure Alerts:**

```yaml
# prometheus/rules/infrastructure.yml
groups:
  - name: infrastructure
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
          team: infrastructure
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is above 80% for more than 5 minutes on {{ $labels.instance }}. Current value: {{ $value }}%"

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100 > 90
        for: 5m
        labels:
          severity: warning
          team: infrastructure
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is above 90% for more than 5 minutes on {{ $labels.instance }}. Current value: {{ $value }}%"

      - alert: DiskSpaceLow
        expr: (node_filesystem_avail_bytes * 100) / node_filesystem_size_bytes < 10
        for: 5m
        labels:
          severity: critical
          team: infrastructure
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Disk space is below 10% on {{ $labels.instance }} filesystem {{ $labels.mountpoint }}. Current value: {{ $value }}%"

      - alert: NodeDown
        expr: up{job="node-exporter"} == 0
        for: 1m
        labels:
          severity: critical
          team: infrastructure
        annotations:
          summary: "Node {{ $labels.instance }} is down"
          description: "Node {{ $labels.instance }} has been down for more than 1 minute"

      - alert: HighLoadAverage
        expr: node_load15 > 2 * count by(instance) (node_cpu_seconds_total{mode="idle"})
        for: 10m
        labels:
          severity: warning
          team: infrastructure
        annotations:
          summary: "High load average on {{ $labels.instance }}"
          description: "Load average is high on {{ $labels.instance }}. Current value: {{ $value }}"
```

**Application Performance Alerts:**

```yaml
# prometheus/rules/applications.yml
groups:
  - name: applications
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) * 100 > 5
        for: 5m
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "High error rate in {{ $labels.service }}"
          description: "Error rate is above 5% for {{ $labels.service }}. Current value: {{ $value }}%"

      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
          team: backend
        annotations:
          summary: "High response time in {{ $labels.service }}"
          description: "95th percentile response time is above 2 seconds for {{ $labels.service }}. Current value: {{ $value }}s"

      - alert: ServiceDown
        expr: up{job=~".*-service"} == 0
        for: 1m
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "Service {{ $labels.job }} has been unreachable for more than 1 minute"

      - alert: DatabaseConnectionPoolHigh
        expr: db_connection_pool_active / db_connection_pool_max * 100 > 80
        for: 5m
        labels:
          severity: warning
          team: database
        annotations:
          summary: "Database connection pool usage high"
          description: "Database connection pool usage is above 80%. Current value: {{ $value }}%"
```

**ML-Specific Alerts:**

```yaml
# prometheus/rules/ml_services.yml
groups:
  - name: ml_services
    rules:
      - alert: ModelPredictionLatencyHigh
        expr: histogram_quantile(0.95, rate(model_prediction_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
          team: ml_ops
        annotations:
          summary: "High prediction latency for model {{ $labels.model_name }}"
          description: "95th percentile prediction latency is above 1 second. Current value: {{ $value }}s"

      - alert: ModelAccuracyDrop
        expr: model_accuracy < 0.8
        for: 10m
        labels:
          severity: critical
          team: data_science
        annotations:
          summary: "Model accuracy dropped for {{ $labels.model_name }}"
          description: "Model accuracy has dropped below 80%. Current value: {{ $value }}"

      - alert: DataDriftDetected
        expr: data_drift_score > 0.7
        for: 5m
        labels:
          severity: warning
          team: data_science
        annotations:
          summary: "Data drift detected for model {{ $labels.model_name }}"
          description: "Data drift score is above threshold. Current score: {{ $value }}"

      - alert: HighPredictionVolume
        expr: rate(model_predictions_total[5m]) > 1000
        for: 2m
        labels:
          severity: info
          team: ml_ops
        annotations:
          summary: "High prediction volume for {{ $labels.model_name }}"
          description: "Prediction rate is above 1000 requests per second. Current rate: {{ $value }}"
```

### 2.2 AlertManager Configuration

**AlertManager Setup:**

```yaml
# alertmanager/alertmanager.yml
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alerts@company.com'
  slack_api_url: '${SLACK_WEBHOOK_URL}'

templates:
  - '/etc/alertmanager/templates/*.tmpl'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'default-receiver'
  routes:
    - match:
        severity: critical
      receiver: 'critical-alerts'
      continue: true
    
    - match:
        team: infrastructure
      receiver: 'infrastructure-team'
      
    - match:
        team: ml_ops
      receiver: 'ml-ops-team'
      
    - match:
        team: data_science
      receiver: 'data-science-team'

receivers:
  - name: 'default-receiver'
    email_configs:
      - to: 'ops-team@company.com'
        subject: '[{{ .Status | toUpper }}] {{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
        body: |
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          Labels: {{ range .Labels.SortedPairs }}{{ .Name }}={{ .Value }} {{ end }}
          {{ end }}

  - name: 'critical-alerts'
    slack_configs:
      - channel: '#critical-alerts'
        title: 'Critical Alert'
        text: |
          {{ range .Alerts }}
          *Alert:* {{ .Annotations.summary }}
          *Description:* {{ .Annotations.description }}
          *Severity:* {{ .Labels.severity }}
          *Team:* {{ .Labels.team }}
          {{ end }}
    
    pagerduty_configs:
      - service_key: '${PAGERDUTY_SERVICE_KEY}'
        description: |
          {{ range .Alerts }}{{ .Annotations.summary }}{{ end }}

  - name: 'infrastructure-team'
    slack_configs:
      - channel: '#infrastructure-alerts'
        title: 'Infrastructure Alert'
        text: |
          {{ range .Alerts }}
          *Alert:* {{ .Annotations.summary }}
          *Instance:* {{ .Labels.instance }}
          *Description:* {{ .Annotations.description }}
          {{ end }}

  - name: 'ml-ops-team'
    slack_configs:
      - channel: '#ml-ops-alerts'
        title: 'ML Operations Alert'
        text: |
          {{ range .Alerts }}
          *Alert:* {{ .Annotations.summary }}
          *Model:* {{ .Labels.model_name }}
          *Description:* {{ .Annotations.description }}
          {{ end }}

  - name: 'data-science-team'
    slack_configs:
      - channel: '#data-science-alerts'
        title: 'Data Science Alert'
        text: |
          {{ range .Alerts }}
          *Alert:* {{ .Annotations.summary }}
          *Model:* {{ .Labels.model_name }}
          *Description:* {{ .Annotations.description }}
          {{ end }}

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'cluster', 'service']
```

## Phase 3: Grafana Dashboard Configuration

### 3.1 Infrastructure Dashboards

**System Overview Dashboard:**

```json
{
  "dashboard": {
    "id": null,
    "title": "System Overview",
    "tags": ["infrastructure", "overview"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "CPU Usage",
        "type": "stat",
        "targets": [
          {
            "expr": "100 - (avg by(instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "{{instance}}"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 70},
                {"color": "red", "value": 90}
              ]
            },
            "unit": "percent"
          }
        },
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
      },
      {
        "id": 2,
        "title": "Memory Usage",
        "type": "stat",
        "targets": [
          {
            "expr": "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100",
            "legendFormat": "{{instance}}"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 80},
                {"color": "red", "value": 95}
              ]
            },
            "unit": "percent"
          }
        },
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
      }
    ],
    "time": {"from": "now-1h", "to": "now"},
    "refresh": "5s"
  }
}
```

**Application Performance Dashboard:**

```json
{
  "dashboard": {
    "id": null,
    "title": "Application Performance",
    "tags": ["application", "performance"],
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{service}} {{method}} {{status}}"
          }
        ],
        "yAxes": [
          {"label": "Requests/sec", "min": 0}
        ],
        "gridPos": {"h": 8, "w": 24, "x": 0, "y": 0}
      },
      {
        "id": 2,
        "title": "Response Time Distribution",
        "type": "heatmap",
        "targets": [
          {
            "expr": "rate(http_request_duration_seconds_bucket[5m])",
            "format": "heatmap",
            "legendFormat": "{{le}}"
          }
        ],
        "gridPos": {"h": 8, "w": 24, "x": 0, "y": 8}
      }
    ]
  }
}
```

### 3.2 ML-Specific Dashboards

**Model Performance Dashboard:**

```json
{
  "dashboard": {
    "id": null,
    "title": "ML Model Performance",
    "tags": ["ml", "models"],
    "panels": [
      {
        "id": 1,
        "title": "Model Accuracy",
        "type": "stat",
        "targets": [
          {
            "expr": "model_accuracy",
            "legendFormat": "{{model_name}}"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "red", "value": null},
                {"color": "yellow", "value": 0.8},
                {"color": "green", "value": 0.9}
              ]
            },
            "unit": "percentunit"
          }
        }
      },
      {
        "id": 2,
        "title": "Prediction Latency",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(model_prediction_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(model_prediction_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          }
        ]
      }
    ]
  }
}
```

## Phase 4: Custom Metrics and Instrumentation

### 4.1 Application Instrumentation

**Python/Flask Application Example:**

```python
# app_monitoring.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from flask import Flask, request, jsonify
import time
import random
import numpy as np

app = Flask(__name__)

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

MODEL_PREDICTIONS = Counter(
    'model_predictions_total',
    'Total model predictions',
    ['model_name', 'version']
)

MODEL_PREDICTION_DURATION = Histogram(
    'model_prediction_duration_seconds',
    'Model prediction duration',
    ['model_name']
)

MODEL_ACCURACY = Gauge(
    'model_accuracy',
    'Current model accuracy',
    ['model_name']
)

DATA_DRIFT_SCORE = Gauge(
    'data_drift_score',
    'Current data drift score',
    ['model_name', 'feature']
)

DB_CONNECTIONS = Gauge(
    'db_connection_pool_active',
    'Active database connections'
)

DB_CONNECTION_POOL_MAX = Gauge(
    'db_connection_pool_max',
    'Maximum database connections'
)

def track_metrics(f):
    """Decorator to track request metrics"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = f(*args, **kwargs)
            status = '200'
            return result
        except Exception as e:
            status = '500'
            raise
        finally:
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.endpoint,
                status=status
            ).inc()
            
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.endpoint
            ).observe(time.time() - start_time)
    
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/predict', methods=['POST'])
@track_metrics
def predict():
    """ML model prediction endpoint with monitoring"""
    start_time = time.time()
    
    data = request.json
    model_name = data.get('model_name', 'default_model')
    
    # Simulate model prediction
    prediction_time = random.uniform(0.1, 2.0)
    time.sleep(prediction_time)
    
    # Simulate prediction result
    prediction = random.choice([0, 1])
    confidence = random.uniform(0.7, 0.99)
    
    # Update metrics
    MODEL_PREDICTIONS.labels(
        model_name=model_name,
        version='v1.0'
    ).inc()
    
    MODEL_PREDICTION_DURATION.labels(
        model_name=model_name
    ).observe(prediction_time)
    
    return jsonify({
        'prediction': prediction,
        'confidence': confidence
    })

@app.route('/update_model_metrics', methods=['POST'])
def update_model_metrics():
    """Endpoint to update model performance metrics"""
    data = request.json
    
    model_name = data['model_name']
    accuracy = data.get('accuracy')
    drift_scores = data.get('drift_scores', {})
    
    if accuracy:
        MODEL_ACCURACY.labels(model_name=model_name).set(accuracy)
    
    for feature, score in drift_scores.items():
        DATA_DRIFT_SCORE.labels(
            model_name=model_name,
            feature=feature
        ).set(score)
    
    return jsonify({'status': 'updated'})

@app.route('/health')
@track_metrics
def health():
    """Health check endpoint"""
    # Update connection pool metrics
    DB_CONNECTIONS.set(random.randint(5, 20))
    DB_CONNECTION_POOL_MAX.set(25)
    
    return jsonify({'status': 'healthy'})

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### 4.2 Kubernetes Custom Metrics

**Custom Resource Definitions for ML Models:**

```yaml
# ml-model-crd.yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: mlmodels.ml.company.com
spec:
  group: ml.company.com
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              modelName:
                type: string
              version:
                type: string
              accuracy:
                type: number
                minimum: 0
                maximum: 1
              driftThreshold:
                type: number
                minimum: 0
                maximum: 1
          status:
            type: object
            properties:
              currentAccuracy:
                type: number
              lastUpdate:
                type: string
  scope: Namespaced
  names:
    plural: mlmodels
    singular: mlmodel
    kind: MLModel

---
# Model monitoring operator
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-model-operator
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ml-model-operator
  template:
    metadata:
      labels:
        app: ml-model-operator
    spec:
      containers:
      - name: operator
        image: company/ml-model-operator:latest
        env:
        - name: PROMETHEUS_URL
          value: "http://prometheus-server:9090"
        ports:
        - containerPort: 8080
          name: metrics
```

## Phase 5: Automated Incident Response

### 5.1 Automated Remediation Scripts

**Auto-scaling Based on Metrics:**

```python
# auto_remediation.py
import requests
import json
import time
import logging
from kubernetes import client, config
from prometheus_api_client import PrometheusConnect

class AutoRemediation:
    def __init__(self, prometheus_url, k8s_config_file=None):
        self.prometheus = PrometheusConnect(url=prometheus_url)
        
        if k8s_config_file:
            config.load_kube_config(config_file=k8s_config_file)
        else:
            config.load_incluster_config()
        
        self.apps_v1 = client.AppsV1Api()
        self.core_v1 = client.CoreV1Api()
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def check_cpu_usage(self, threshold=80):
        """Check CPU usage and scale if needed"""
        query = f'100 - (avg by(instance) (irate(node_cpu_seconds_total{{mode="idle"}}[5m])) * 100) > {threshold}'
        
        result = self.prometheus.custom_query(query)
        
        for metric in result:
            instance = metric['metric']['instance']
            cpu_usage = float(metric['value'][1])
            
            self.logger.info(f"High CPU usage detected on {instance}: {cpu_usage}%")
            
            # Trigger auto-scaling
            self.scale_application(instance, cpu_usage)

    def scale_application(self, instance, cpu_usage):
        """Scale application based on CPU usage"""
        # Get current deployment
        try:
            deployments = self.apps_v1.list_deployment_for_all_namespaces()
            
            for deployment in deployments.items:
                if self.should_scale_deployment(deployment, instance):
                    current_replicas = deployment.spec.replicas
                    new_replicas = min(current_replicas + 1, 10)  # Max 10 replicas
                    
                    # Update deployment
                    deployment.spec.replicas = new_replicas
                    
                    self.apps_v1.patch_namespaced_deployment(
                        name=deployment.metadata.name,
                        namespace=deployment.metadata.namespace,
                        body=deployment
                    )
                    
                    self.logger.info(
                        f"Scaled {deployment.metadata.name} from {current_replicas} to {new_replicas} replicas"
                    )
                    
                    # Send notification
                    self.send_notification(
                        f"Auto-scaled {deployment.metadata.name} due to high CPU usage ({cpu_usage}%)"
                    )
                    
        except Exception as e:
            self.logger.error(f"Error scaling application: {e}")

    def should_scale_deployment(self, deployment, instance):
        """Determine if deployment should be scaled"""
        # Add logic to match deployment to instance
        # This is simplified - in reality you'd have more sophisticated matching
        return True

    def restart_failing_pods(self):
        """Restart pods that are in failing state"""
        try:
            pods = self.core_v1.list_pod_for_all_namespaces()
            
            for pod in pods.items:
                if pod.status.phase == 'Failed' or self.is_pod_unhealthy(pod):
                    self.logger.info(f"Restarting failing pod: {pod.metadata.name}")
                    
                    self.core_v1.delete_namespaced_pod(
                        name=pod.metadata.name,
                        namespace=pod.metadata.namespace
                    )
                    
                    self.send_notification(
                        f"Auto-restarted failing pod: {pod.metadata.name}"
                    )
                    
        except Exception as e:
            self.logger.error(f"Error restarting pods: {e}")

    def is_pod_unhealthy(self, pod):
        """Check if pod is unhealthy based on restart count or status"""
        if pod.status.container_statuses:
            for container in pod.status.container_statuses:
                if container.restart_count > 5:
                    return True
                if not container.ready:
                    return True
        return False

    def check_model_performance(self):
        """Check ML model performance and trigger retraining if needed"""
        query = 'model_accuracy < 0.8'
        result = self.prometheus.custom_query(query)
        
        for metric in result:
            model_name = metric['metric']['model_name']
            accuracy = float(metric['value'][1])
            
            self.logger.warning(f"Model {model_name} accuracy dropped to {accuracy}")
            
            # Trigger retraining workflow
            self.trigger_model_retraining(model_name)

    def trigger_model_retraining(self, model_name):
        """Trigger model retraining workflow"""
        # This would integrate with your ML pipeline
        # For example, trigger a Jenkins job or Argo Workflow
        
        webhook_url = "https://jenkins.company.com/job/retrain-model/buildWithParameters"
        params = {
            "MODEL_NAME": model_name,
            "TRIGGER": "auto_remediation"
        }
        
        try:
            response = requests.post(webhook_url, params=params)
            response.raise_for_status()
            
            self.logger.info(f"Triggered retraining for model {model_name}")
            self.send_notification(f"Auto-triggered retraining for model {model_name} due to low accuracy")
            
        except Exception as e:
            self.logger.error(f"Failed to trigger retraining: {e}")

    def send_notification(self, message):
        """Send notification to Slack or other channels"""
        webhook_url = "https://hooks.slack.com/your/webhook/url"
        
        payload = {
            "text": f"🤖 Auto-Remediation: {message}",
            "channel": "#ops-alerts"
        }
        
        try:
            requests.post(webhook_url, json=payload)
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

    def run_monitoring_loop(self):
        """Main monitoring loop"""
        while True:
            try:
                self.check_cpu_usage()
                self.restart_failing_pods()
                self.check_model_performance()
                
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)

if __name__ == "__main__":
    remediation = AutoRemediation(
        prometheus_url="http://prometheus-server:9090"
    )
    remediation.run_monitoring_loop()
```

## Phase 6: Advanced Monitoring Features

### 6.1 SLO/SLI Implementation

**Service Level Objectives Configuration:**

```python
# slo_monitoring.py
from prometheus_client import Gauge, Counter
import time
import logging

class SLOMonitor:
    def __init__(self, prometheus_client):
        self.prometheus = prometheus_client
        
        # SLI metrics
        self.availability_sli = Gauge(
            'slo_availability_sli',
            'Service availability SLI',
            ['service']
        )
        
        self.latency_sli = Gauge(
            'slo_latency_sli',
            'Service latency SLI (95th percentile)',
            ['service']
        )
        
        self.error_budget_remaining = Gauge(
            'slo_error_budget_remaining',
            'Remaining error budget',
            ['service', 'slo_type']
        )
        
        # SLO definitions
        self.slos = {
            'web-service': {
                'availability': 0.999,  # 99.9% availability
                'latency': 0.5,        # 95th percentile < 500ms
                'error_rate': 0.001    # Error rate < 0.1%
            },
            'ml-service': {
                'availability': 0.995,  # 99.5% availability
                'latency': 2.0,        # 95th percentile < 2s
                'error_rate': 0.005    # Error rate < 0.5%
            }
        }

    def calculate_availability_sli(self, service):
        """Calculate availability SLI"""
        query = f'avg_over_time(up{{job="{service}"}}[1h])'
        result = self.prometheus.custom_query(query)
        
        if result:
            availability = float(result[0]['value'][1])
            self.availability_sli.labels(service=service).set(availability)
            return availability
        return 0

    def calculate_latency_sli(self, service):
        """Calculate latency SLI"""
        query = f'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{{service="{service}"}}[5m]))'
        result = self.prometheus.custom_query(query)
        
        if result:
            latency = float(result[0]['value'][1])
            self.latency_sli.labels(service=service).set(latency)
            return latency
        return 0

    def calculate_error_budget(self, service, window_hours=24):
        """Calculate remaining error budget"""
        slo_config = self.slos.get(service, {})
        
        # Availability error budget
        availability_sli = self.calculate_availability_sli(service)
        availability_slo = slo_config.get('availability', 0.99)
        
        if availability_sli > 0:
            availability_budget = max(0, 1 - (1 - availability_sli) / (1 - availability_slo))
            self.error_budget_remaining.labels(
                service=service, 
                slo_type='availability'
            ).set(availability_budget)

        # Latency error budget
        latency_sli = self.calculate_latency_sli(service)
        latency_slo = slo_config.get('latency', 1.0)
        
        if latency_sli > 0:
            latency_budget = max(0, 1 - latency_sli / latency_slo)
            self.error_budget_remaining.labels(
                service=service,
                slo_type='latency'
            ).set(latency_budget)

    def monitor_all_services(self):
        """Monitor SLOs for all configured services"""
        for service in self.slos.keys():
            self.calculate_error_budget(service)

# Usage
monitor = SLOMonitor(prometheus_client)
monitor.monitor_all_services()
```

## Success Metrics

1. **MTTD (Mean Time to Detection)**: < 2 minutes for critical issues
2. **MTTR (Mean Time to Recovery)**: < 15 minutes for automated remediation
3. **Alert Accuracy**: > 90% of alerts are actionable
4. **SLO Compliance**: Meet defined SLOs 99%+ of the time
5. **Automation Rate**: > 70% of common issues resolved automatically

This comprehensive implementation provides a robust foundation for AIOps practices with intelligent monitoring, alerting, and automated incident response.