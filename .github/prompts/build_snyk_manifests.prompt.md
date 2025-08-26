---
version: "1.0.0"
created_date: "2025-08-26"
last_updated: "2025-08-26"
---

> **Directive:**
> 
> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

> **Context Management:**
> If the security scanning requirements are too complex for comprehensive scaffold, prioritize:
> 1. Security-critical vulnerability scanning configurations and remediation workflows
> 2. Production CI/CD integration and automated security gate effectiveness
> 3. Integration patterns with different project types and dependency management systems
> Ask user to specify focus areas if scope exceeds scaffold capacity.

> **Analysis Validation:**
> - Mark implementation choices as "Best Practice" vs "Alternative" based on Snyk documentation and DevSecOps standards
> - Reference specific scanning policies, CI/CD configurations, or security patterns when making recommendations
> - Provide confidence indicators: High/Medium/Low for each security scanning architectural decision
> - Note when additional security requirements or project contexts would improve scaffold quality
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
<!--
title: "Build Snyk Security Integration Repo"
category: "Security & DevSecOps"
description: "Scaffold a best-practice Snyk integration repository for code and container scanning, including structure, linting, and test setup."
-->

# 🛡️ Build Snyk Security Integration Repository

You are a DevSecOps Engineer. Your task is to scaffold a new repository for integrating Snyk security scanning into code and container workflows, following best practices for structure, automation, and maintainability.

---

## 🎯 Step 1: Define Project Context

Ask:
- “What languages or platforms will be scanned (e.g., Node.js, Python, Docker)?”
- “Should container images be scanned as well as source code?”
- “Are there any compliance or reporting requirements?”

---

## 🏗️ Step 2: Scaffold Base Structure

Create the following structure:

```
snyk-integration/
├── src/ (application code)
├── Dockerfile (if containerized)
├── .snyk (ignore file)
├── snyk.config.yml (optional, for advanced config)
├── test/
│   └── example.test.js
├── README.md
```

---

## 🛠️ Step 3: Initialize with Tools

- Add Snyk CLI to dev dependencies (e.g., `npm install snyk --save-dev`).
- Add a sample `.snyk` ignore file.
- Add a sample test file in `test/`.
- Document Snyk usage and configuration in `README.md`.

---

## 🧪 Step 4: Linting & Testing

- Add a linting tool for the chosen language (e.g., eslint, flake8).
- Document how to run `snyk test` and `snyk monitor`.
- Add a test script to validate Snyk integration.

---

## 🔒 Step 5: Security Best Practices

- Store Snyk tokens in environment variables or CI secrets.
- Regularly update dependencies and scan for vulnerabilities.
- Use `snyk protect` for runtime patching (if supported).
- Document how to triage and fix vulnerabilities.

---

## 🧾 Output Format

```markdown
## 📦 Scaffolded Structure

## 🛠️ Initialization Steps

## 🧪 Linting & Testing Setup

## 🔒 Security Practices
```
