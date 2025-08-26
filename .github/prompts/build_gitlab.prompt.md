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
> If the GitLab CI/CD requirements are too complex for comprehensive scaffold, prioritize:
> 1. Security-critical pipeline configurations and secret management
> 2. Production deployment workflows and approval gate effectiveness
> 3. Integration effectiveness with GitLab features and external services
> Ask user to specify focus areas if scope exceeds scaffold capacity.

> **Analysis Validation:**
> - Mark implementation choices as "Best Practice" vs "Alternative" based on GitLab documentation and CI/CD standards
> - Reference specific pipeline configurations, security patterns, or deployment strategies when making recommendations
> - Provide confidence indicators: High/Medium/Low for each CI/CD architectural decision
> - Note when additional project requirements or deployment contexts would improve scaffold quality
<!--

> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
title: "Build GitLab CI/CD Repo"
category: "CI/CD"
description: "Scaffold a best-practice GitLab CI/CD repository, including pipeline config, structure, linting, and test setup."
-->

# 🦊 Build GitLab CI/CD Repository
# Directive:
If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.

You are a DevOps Engineer. Your task is to scaffold a new repository for GitLab CI/CD, following best practices for structure, modularity, and maintainability.

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
gitlab-ci/
├── .gitlab-ci.yml
├── scripts/
│   └── build.sh
├── README.md
```

---

## 🛠️ Step 3: Initialize with Tools

- Add a sample `.gitlab-ci.yml` with jobs for build, test, and deploy.
- Add a `scripts/` directory for reusable shell scripts.
- Document pipeline usage and secrets setup in `README.md`.

---

## 🧪 Step 4: Linting & Testing

- Add a linting job in the pipeline for the chosen language.
- Add a test job that runs unit or integration tests.
- Document how to trigger pipelines (push, MR, schedule).

---

## 🔒 Step 5: Security Best Practices

- Use GitLab CI/CD variables for secrets.
- Pin Docker image versions in pipeline config.
- Avoid hardcoded credentials in scripts or config.
- Document how to rotate secrets and manage permissions.

---

## 🧾 Output Format

```markdown
## 📦 Scaffolded Structure

## 🛠️ Initialization Steps

## 🧪 Linting & Testing Setup

## 🔒 Security Practices
```
