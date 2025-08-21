> **Directive:**
> 
> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
<!--

> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
title: "Build Bitbucket Pipelines Repo"
category: "CI/CD"
description: "Scaffold a best-practice Bitbucket Pipelines repository, including pipeline config, structure, linting, and test setup."
-->

# 🧺 Build Bitbucket Pipelines Repository

You are a DevOps Engineer. Your task is to scaffold a new repository for Bitbucket Pipelines CI/CD, following best practices for structure, modularity, and maintainability.

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
bitbucket-pipelines/
├── bitbucket-pipelines.yml
├── scripts/
│   └── build.sh
├── README.md
```

---

## 🛠️ Step 3: Initialize with Tools

- Add a sample `bitbucket-pipelines.yml` with steps for build, test, and deploy.
- Add a `scripts/` directory for reusable shell scripts.
- Document pipeline usage and secrets setup in `README.md`.

---

## 🧪 Step 4: Linting & Testing

- Add a linting step in the pipeline for the chosen language.
- Add a test step that runs unit or integration tests.
- Document how to trigger pipelines (push, PR, schedule).

---

## 🔒 Step 5: Security Best Practices

- Use Bitbucket repository variables for secrets.
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
