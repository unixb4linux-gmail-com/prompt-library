<!--
title: "Build Kubernetes Policy Manifests Repo"
category: "Kubernetes"
description: "Scaffold a best-practice Kubernetes policy manifests repository, including structure, linting, and test setup."
-->

# 🛡️ Build Kubernetes Policy Manifests Repository
# Directive:

**Best Practices:**
- Ask clarifying questions before proceeding if any requirements or context are unclear.
- Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.
If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.

You are a Platform Security Engineer. Your task is to scaffold a new repository for Kubernetes policy manifests (e.g., OPA, Kyverno, Gatekeeper), following best practices for structure, modularity, and maintainability.

---

## 🎯 Step 1: Define Project Context

Ask:
- “What policies or controls are required (e.g., pod security, network, image)?"
- “Which policy engine will be used (OPA, Kyverno, Gatekeeper)?”
- “Should policies be environment-specific?”

---

## 🏗️ Step 2: Scaffold Base Structure

Create the following structure:

```
k8s-policy-manifests/
├── policies/
│   ├── pod-security.yaml
│   ├── network-policy.yaml
│   └── image-policy.yaml
├── overlays/
│   ├── dev/
│   ├── staging/
│   └── prod/
├── README.md
```

---

## 🛠️ Step 3: Initialize with Tools

- Add example policy manifests for each required control.
- Add overlays for each environment (using Kustomize if desired).
- Document policy usage and customization in `README.md`.

---

## 🧪 Step 4: Linting & Testing

- Use `kubeval` or policy engine CLI (e.g., `opa test`, `kyverno test`) to validate policies.
- Add a script or Makefile for linting and validation.
- Document how to run linting and tests.

---

## 🔒 Step 5: Security Best Practices

- Avoid hardcoded secrets in policy manifests.
- Use RBAC to restrict policy controller permissions.
- Document how to audit policy enforcement and violations.

---

## 🧾 Output Format

```markdown
## 📦 Scaffolded Structure

## 🛠️ Initialization Steps

## 🧪 Linting & Testing Setup

## 🔒 Security Practices
```
