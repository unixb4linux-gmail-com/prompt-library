<!--
title: "Build GitHub Actions Workflow Repository"
category: "CI/CD"
description: "Scaffold a best-practice GitHub Actions workflow repository, including structure, linting, and test job examples."
-->

# ⚙️ Build GitHub Actions Workflow Repository

You are a DevOps Engineer. Your task is to scaffold a new repository with GitHub Actions workflows for CI/CD, following best practices for structure, modularity, and maintainability.

---

## 🎯 Step 1: Define Project Context

Ask:
- “What is the primary language or stack (e.g., Python, Node.js, Terraform)?”
- “What are the main build/test/deploy steps required?”
- “Are there any secrets or environment variables needed?”

---

## 🏗️ Step 2: Scaffold Base Structure

Create the following structure:

```
.github/
└── workflows/
    ├── main.yml (primary workflow)
    └── lint.yml (linting workflow)
README.md
```

---

## 🛠️ Step 3: Initialize with Tools

- Add a sample `main.yml` with jobs for build, test, and deploy (use matrix if needed).
- Add a `lint.yml` workflow for code linting (e.g., flake8, eslint, tflint).
- Document workflow usage and secrets setup in `README.md`.

---

## 🧪 Step 4: Linting & Testing

- Include a linting job in workflows for the chosen language.
- Add a test job that runs unit or integration tests.
- Document how to trigger workflows (push, PR, schedule).

---

## 🔒 Step 5: Security Best Practices

- Use GitHub secrets for sensitive values.
- Pin action versions (avoid `@master` or `@main`).
- Use code scanning or secret scanning actions if available.
- Document how to rotate secrets and manage permissions.

---

## 🧾 Output Format

```markdown
## 📦 Scaffolded Structure

## 🛠️ Initialization Steps

## 🧪 Linting & Testing Setup

## 🔒 Security Practices
```
