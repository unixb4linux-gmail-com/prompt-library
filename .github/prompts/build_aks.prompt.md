---
version: "1.0.0"
created_date: "2025-08-26"
last_updated: "2025-08-26"
---

> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
> 
> Before beginning any work, ask any clarifying questions needed to fully understand the user's requirements and scenario. Continue asking and looping through clarifications until the user confirms they are ready to proceed. Only start work after explicit confirmation.

> **Ask clarifying questions before proceeding.**
> **Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.**

> **Context Management:**
> If the AKS cluster requirements are too complex for comprehensive scaffold, prioritize:
> 1. Security-critical cluster configurations and managed identity setup
> 2. Production-ready networking and node pool configurations
> 3. Integration effectiveness with Azure services and monitoring solutions
> Ask user to specify focus areas if scope exceeds scaffold capacity.

> **Analysis Validation:**
> - Mark implementation choices as "Best Practice" vs "Alternative" based on Azure documentation and Well-Architected Framework
> - Reference specific Azure resources, IaC configurations, or security patterns when making recommendations
> - Provide confidence indicators: High/Medium/Low for each infrastructure and security decision
> - Note when additional Azure expertise or application requirements would improve scaffold quality
<!--
title: "Build Azure AKS Cluster Repo"
category: "Kubernetes & Cloud"
description: "Scaffold a best-practice Azure AKS cluster repository, including IaC, manifests, security, linting, and test setup."
-->

# ☁️ Build Azure AKS Cluster Repository
# Directive:
If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.

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
