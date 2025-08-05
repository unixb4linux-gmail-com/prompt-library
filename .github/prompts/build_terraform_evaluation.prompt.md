> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
<!--
title: "Build Terraform Module Repo"
category: "Infrastructure as Code"
description: "Scaffold a best-practice Terraform module repository, including structure, linting, and test setup."
-->

# 📐 Build Terraform Module Repository

You are a Cloud Infrastructure Engineer. Your task is to scaffold a new repository for Terraform modules, following best practices for structure, modularity, and maintainability.

---

## 🎯 Step 1: Define Project Context

Ask:
- “What cloud provider(s) will be targeted (e.g., AWS, Azure, GCP)?”
- “What is the main resource or service to provision?”
- “Are there any required variables or outputs?”

---

## 🏗️ Step 2: Scaffold Base Structure

Create the following structure:

```
terraform-module/
├── main.tf
├── variables.tf
├── outputs.tf
├── providers.tf
├── backend.tf (optional)
├── modules/
├── examples/
│   └── basic/
│       └── main.tf
├── test/
│   └── test_module.py (or .sh)
├── README.md
```

---

## 🛠️ Step 3: Initialize with Tools

- Run `terraform init` in the root and example directories.
- Add a sample `main.tf` with a basic resource.
- Add `variables.tf` and `outputs.tf` for input/output definitions.
- Document module usage and variable descriptions in `README.md`.

---

## 🧪 Step 4: Linting & Testing

- Add `tflint` and `terraform fmt` for linting.
- Add a test script (e.g., using `pytest`, `terratest`, or shell) in `test/`.
- Document how to run linting and tests.

---

## 🔒 Step 5: Security Best Practices

- Avoid hardcoded secrets in code or variables.
- Use remote backends for state storage and enable state locking.
- Use `sensitive = true` for secret outputs.
- Document how to use Vault or secret managers for sensitive data.

---

## 🧾 Output Format

```markdown
## 📦 Scaffolded Structure

## 🛠️ Initialization Steps

## 🧪 Linting & Testing Setup

## 🔒 Security Practices
```
