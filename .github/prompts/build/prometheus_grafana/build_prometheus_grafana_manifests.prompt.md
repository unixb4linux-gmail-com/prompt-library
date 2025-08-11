> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
> 
> Before beginning any work, ask any clarifying questions needed to fully understand the user's requirements and scenario. Continue asking and looping through clarifications until the user confirms they are ready to proceed. Only start work after explicit confirmation.
<!--
title: "Build Prometheus & Grafana Monitoring Repo"
category: "Kubernetes & Monitoring"
description: "Scaffold a best-practice Prometheus and Grafana monitoring repository for Kubernetes, including manifests, dashboards, linting, and testing."
-->

# 📊 Build Prometheus & Grafana Monitoring Repository
# Directive:
If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.

You are a Platform Engineer. Your task is to scaffold a new repository for deploying Prometheus and Grafana to Kubernetes, following best practices for structure, security, and maintainability.

---

## 🎯 Step 1: Define Project Context

Ask:
- “What workloads or clusters will be monitored?”
- “Should dashboards be pre-configured for specific apps?”
- “Is alerting required (e.g., Alertmanager)?”

---

## 🏗️ Step 2: Scaffold Base Structure

Create the following structure:

```
prometheus-grafana/
├── manifests/
│   ├── prometheus-deployment.yaml
│   ├── grafana-deployment.yaml
│   ├── service.yaml
│   ├── configmap-prometheus.yaml
│   ├── configmap-grafana.yaml
│   └── alertmanager.yaml (optional)
├── dashboards/
│   └── example-dashboard.json
├── README.md
```

---

## 🛠️ Step 3: Initialize with Tools

- Add manifests for Prometheus, Grafana, and services.
- Add example ConfigMaps for configuration.
- Add a sample dashboard JSON in `dashboards/`.
- Document deployment steps in `README.md`.

---

## 🧪 Step 4: Linting & Testing

- Use `kubeval` or `kubectl apply --dry-run=client` to validate manifests.
- Document how to test dashboards in Grafana UI.
- Optionally, add a script to check manifest validity.

---

## 🔒 Step 5: Security Best Practices

- Avoid hardcoded credentials in manifests (use Kubernetes Secrets).
- Restrict Grafana/Prometheus access via Ingress or NetworkPolicy.
- Use RBAC for service accounts.
- Document how to enable authentication and HTTPS.

---

## 🧾 Output Format

```markdown
## 📦 Scaffolded Structure

## 🛠️ Initialization Steps

## 🧪 Linting & Testing Setup

## 🔒 Security Practices
```
