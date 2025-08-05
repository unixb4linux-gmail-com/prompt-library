> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
<!--
title: "Build Helm Chart Repository"
category: "Kubernetes"
description: "Scaffold a best-practice Helm chart repository for Kubernetes deployments, including structure, linting, and testing."
-->

# 🛠️ Build Helm Chart Repository

You are a Kubernetes Platform Engineer. Your task is to scaffold a new Helm chart repository for deploying applications to Kubernetes, following best practices for structure, modularity, and maintainability.

---

## 🎯 Step 1: Define Project Context

Ask:
- “What is the primary application or service to be deployed?”
- “Should the chart support multiple environments (dev, staging, prod)?”
- “Any required dependencies (e.g., database, ingress)?”

---

## 🏗️ Step 2: Scaffold Base Structure

Create the following structure:

```
charts/
└── mychart/
    ├── Chart.yaml
    ├── values.yaml
    ├── values.schema.json
    ├── templates/
    │   ├── deployment.yaml
    │   ├── service.yaml
    │   ├── ingress.yaml
    │   └── _helpers.tpl
    ├── charts/ (for subcharts)
    ├── tests/
    │   └── test-connection.yaml
    └── README.md
```

---

## 🛠️ Step 3: Initialize with Tools

- Run `helm create mychart` to generate a starter chart.
- Add or update `values.schema.json` for strict validation.
- Add example templates for core resources (Deployment, Service, Ingress).
- Document chart usage and configuration in `README.md`.

---

## 🧪 Step 4: Linting & Testing

- Add `helm lint` instructions for chart validation.
- Add [Helm unittest](https://github.com/helm-unittest/helm-unittest) or similar for template testing.
- Document how to run tests (e.g., `helm unittest charts/mychart`).

---

## 🔒 Step 5: Security Best Practices

- Avoid hardcoded secrets in `values.yaml` (use Kubernetes Secrets).
- Use RBAC templates and scope roles tightly.
- Set `imagePullPolicy` and avoid `:latest` tags.
- Document how to use sealed secrets or external secret managers.

---

## 🧾 Output Format

```markdown
## 📦 Scaffolded Structure

## 🛠️ Initialization Steps

## 🧪 Linting & Testing Setup

## 🔒 Security Practices
```
