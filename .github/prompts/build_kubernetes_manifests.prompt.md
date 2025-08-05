> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
<!--
title: "Build Kubernetes Manifests Repo"
category: "Kubernetes"
description: "Scaffold a best-practice Kubernetes manifests repository, including structure, linting, and test setup."
-->

# ☸️ Build Kubernetes Manifests Repository

You are a Platform Engineer. Your task is to scaffold a new repository for Kubernetes manifests, following best practices for structure, modularity, and maintainability.

---

## 🎯 Step 1: Define Project Context

Ask:
- “What application or service will be deployed?”
- “Should the manifests support multiple environments (dev, staging, prod)?”
- “Are there any required secrets or configmaps?”

---

## 🏗️ Step 2: Scaffold Base Structure

Create the following structure:

```
k8s-manifests/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── configmap.yaml
├── overlays/
│   ├── dev/
│   ├── staging/
│   └── prod/
├── secrets/
│   └── example-secret.yaml
├── README.md
```

---

## 🛠️ Step 3: Initialize with Tools

- Add base manifests for core resources (Deployment, Service, Ingress, ConfigMap).
- Add overlays for each environment (using Kustomize if desired).
- Document manifest usage and customization in `README.md`.

---

## 🧪 Step 4: Linting & Testing

- Use `kubeval` or `kubectl apply --dry-run=client` to validate manifests.
- Add a script or Makefile for linting and validation.
- Document how to run linting and tests.

---

## 🔒 Step 5: Security Best Practices

- Avoid hardcoded secrets in manifests (use Kubernetes Secrets).
- Use RBAC manifests and scope roles tightly.
- Set resource requests/limits and securityContext in pods.
- Document how to use sealed secrets or external secret managers.

---

## 🧾 Output Format

```markdown
## 📦 Scaffolded Structure

## 🛠️ Initialization Steps

## 🧪 Linting & Testing Setup

## 🔒 Security Practices
```
