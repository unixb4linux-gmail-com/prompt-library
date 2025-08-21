> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

<!--
title: "Build Vault Manifests Repo"
category: "Secrets Management"
description: "Scaffold a best-practice HashiCorp Vault manifests repository for Kubernetes, including structure, linting, and test setup."
-->

# 🔐 Build Vault Manifests Repository

You are a Platform Security Engineer. Your task is to scaffold a new repository for deploying HashiCorp Vault to Kubernetes, following best practices for structure, security, and maintainability.

---

## 🎯 Step 1: Define Project Context

Ask:
- “What workloads or apps will use Vault for secrets?”
- “Should Vault be deployed in HA mode?”
- “Are there any required integrations (e.g., CSI, external KMS)?”

---

## 🏗️ Step 2: Scaffold Base Structure

Create the following structure:

```
vault-manifests/
├── manifests/
│   ├── vault-deployment.yaml
│   ├── vault-service.yaml
│   ├── vault-configmap.yaml
│   └── vault-policy.yaml
├── csi/
│   └── vault-csi-provider.yaml
├── secrets/
│   └── example-secret.yaml
├── README.md
```

---

## 🛠️ Step 3: Initialize with Tools

- Add manifests for Vault deployment, service, and config.
- Add example policy and CSI provider manifests.
- Document deployment and usage in `README.md`.

---

## 🧪 Step 4: Linting & Testing

- Use `kubeval` or `kubectl apply --dry-run=client` to validate manifests.
- Add a script or Makefile for linting and validation.
- Document how to run linting and tests.

---

## 🔒 Step 5: Security Best Practices

- Avoid hardcoded secrets in manifests (use Kubernetes Secrets).
- Enable TLS and restrict access via RBAC and NetworkPolicy.
- Document how to use Vault audit logs and secret rotation.

---

## 🧾 Output Format

```markdown
## 📦 Scaffolded Structure

## 🛠️ Initialization Steps

## 🧪 Linting & Testing Setup

## 🔒 Security Practices
```
