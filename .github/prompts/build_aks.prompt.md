<!--
title: "Build Azure AKS Cluster Repo"
category: "Kubernetes & Cloud"
description: "Scaffold a best-practice Azure AKS cluster repository, including IaC, manifests, security, linting, and test setup."
-->

# ☁️ Build Azure AKS Cluster Repository

You are a Cloud Platform Engineer. Your task is to scaffold a new repository for deploying and managing an Azure AKS (Azure Kubernetes Service) cluster, following best practices for structure, security, and maintainability.

---

## 🎯 Step 1: Define Project Context

Ask:
- “What is the Azure subscription and region for the AKS cluster?”
- “Should the cluster use system/user node pools, spot nodes, or both?”
- “Are there specific workloads or namespaces to pre-create?”

---

## 🏗️ Step 2: Scaffold Base Structure

Create the following structure:

```
aks-cluster/
├── iac/
│   ├── main.bicep (or main.tf for Terraform)
│   ├── parameters.json
│   └── README.md
├── manifests/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
├── addons/
│   ├── cni.yaml
│   ├── coredns.yaml
│   └── kube-proxy.yaml
├── security/
│   ├── rbac.yaml
│   ├── network-policy.yaml
│   └── keyvault-policy.json
├── monitoring/
│   ├── prometheus.yaml
│   └── azure-monitor-agent.yaml
├── test/
│   └── test_cluster.sh
├── README.md
```

---

## 🛠️ Step 3: Initialize with Tools

- Use Bicep or Terraform to provision AKS and supporting resources.
- Add sample manifests for workloads and add-ons.
- Add RBAC, network policy, and Key Vault policy examples.
- Document setup and usage in `README.md`.

---

## 🧪 Step 4: Linting & Testing

- Use `bicep lint` or `tflint` for IaC.
- Use `kubeval` or `kubectl apply --dry-run=client` for manifests.
- Add a test script to validate cluster and workload deployment.
- Document how to run linting and tests.

---

## 🔒 Step 5: Security Best Practices

- Use managed identities and RBAC for least-privilege access.
- Store secrets in Azure Key Vault and enable encryption at rest.
- Restrict public endpoints and use network policies.
- Document how to enable audit logging and secure add-ons.

---

## 🧾 Output Format

```markdown
## 📦 Scaffolded Structure

## 🛠️ Initialization Steps

## 🧪 Linting & Testing Setup

## 🔒 Security Practices
```
