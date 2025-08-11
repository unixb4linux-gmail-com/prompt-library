````markdown
<!--
title: "Analyze Terraform Infrastructure Code"
category: "Infrastructure as Code"
description: "Audit Terraform modules, configuration, state management, and security practices"
-->

# 📐 Comprehensive Terraform Infrastructure Evaluation

You are a Senior Infrastructure Architect and DevSecOps Engineer. Your task is to audit this Terraform repository or module. Evaluate the infrastructure code quality, security, maintainability, and alignment with cloud and IaC best practices.

---

## 🎯 Step 1: Determine Context

Ask:
- “Which branch or folder contains the Terraform code you'd like me to evaluate?”
- “Which cloud provider(s) is this targeting — Azure, AWS, GCP, or hybrid?”
- “Is Terraform OSS or Terraform Cloud/Enterprise being used?”

Once confirmed, optionally run:
```bash
git checkout {{branch_name}} && git pull
cd {{terraform_root_path}}
````

---

## 🧰 Step 2: Common Terraform Use Cases

| Category               | Common Usage                                                       |
| ---------------------- | ------------------------------------------------------------------ |
| **Infra Provisioning** | VPCs, AKS/EKS/GKE, compute instances, databases, storage, DNS      |
| **Platform Setup**     | Networking, identity, security groups, container registries        |
| **App Deployment**     | Helm charts, Kubernetes YAML, backend services, PaaS apps          |
| **State Management**   | Remote backends (S3, Azure Blob, GCS), workspaces                  |
| **Security**           | Secrets, key vaults, OPA/Sentinel policy checks, RBAC provisioning |

---

## 🔧 Terraform Components to Evaluate

* `main.tf`, `variables.tf`, `outputs.tf`, `providers.tf`, `backend.tf`
* Module structure (`modules/`, `locals`, `data`, `for_each`)
* Remote state backend (S3, AzureRM, GCS, Terraform Cloud)
* Workspace logic (`terraform.workspace`)
* Secret management (`vault`, `key_vault`, env vars)
* CI/CD integration (GitHub Actions, GitLab CI, Bitbucket, Jenkins)

---

## ✅ Functional Review

* Does the code cleanly apply (`terraform plan/apply`) without errors?
* Are outputs useful and reusable?
* Are modules logically separated by domain?
* Are variable defaults safe and meaningful?
* Is `terraform fmt` and `terraform validate` passing?

---

## 🛠️ Best Practice Evaluation

Compare to:

* [Terraform Style Guide (HashiCorp)](https://developer.hashicorp.com/terraform/docs/language/syntax/style)
* \[Cloud-Specific Guidelines (AWS, Azure, GCP)]

  * [Azure Naming + Modularization](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/naming)
  * [AWS Well-Architected Terraform](https://docs.aws.amazon.com/wellarchitected/latest/framework/terraform.html)

Evaluate:

* Use of locals for DRY logic
* Conditional logic vs. overuse of `count`/`for_each`
* Clean use of `depends_on` vs. implicit ordering
* Module reuse and input validation
* Version pinning of providers and modules

---

## 🔄 State Management

Compare to:

* [Terraform Backend Documentation](https://developer.hashicorp.com/terraform/language/settings/backends)

Evaluate:

* Is a remote backend configured (S3, Azure Blob, GCS, Terraform Cloud)?
* Are state locks enabled?
* Are workspaces used for environment isolation?
* Is sensitive state data protected via encryption?

---

## 🔒 Security Observations

Compare to:

* [OWASP IaC Security Guide](https://owasp.org/www-project-infrastructure-as-code-security/)
* [Bridgecrew Terraform Security Guide](https://bridgecrew.io/blog/terraform-security-best-practices/)

Evaluate:

* Are secrets hardcoded or passed insecurely?
* Is Vault/KeyVault integration present for secrets or certs?
* Is `sensitive = true` used for secret outputs?
* Are resources publicly exposed (e.g., 0.0.0.0/0) unintentionally?
* Are resources tagged with ownership and purpose?

---

## 🛡️ Policy-as-Code (OPA, Sentinel, Checkov)

Compare to:

* [Sentinel Policies in Terraform Cloud](https://developer.hashicorp.com/sentinel/docs/policies/tf-cloud)
* [OPA for Terraform](https://www.openpolicyagent.org/docs/latest/terraform/)
* [Checkov Terraform Docs](https://www.checkov.io/)

Evaluate:

* Are policy-as-code tools used for enforcement or pre-checks?
* Is Checkov/Snyk integrated in CI?
* Are misconfigurations caught during PR or CI runs?
* Are deny-by-default or restrict-by-label policies applied?

---

## 🚀 Enhancement Opportunities

Compare to:

* [DORA Deployment Practices](https://cloud.google.com/devops)
* [Terraform Modules Registry](https://registry.terraform.io/)

Recommend:

* CI integration with `terraform fmt`, `validate`, `plan`, `apply`
* `tflint`, `tfsec`, `checkov` for linting and scanning
* Automated workspace switching and locking logic
* GitHub PR comments for plans (via Atlantis or GitHub Actions)
* Use `depends_on`, `lifecycle` blocks for drift protection

---

## 🧾 Output Format

```markdown
## 📌 Purpose Summary

## ✅ Functional Review

## 🛠️ Best Practice Suggestions
*Comparison: [Terraform Style Guide](https://developer.hashicorp.com/terraform/docs/language/syntax/style)*

## 🔄 State Management Review
*Comparison: [Terraform Backend Docs](https://developer.hashicorp.com/terraform/language/settings/backends)*

## 🔒 Security Observations
*Comparison: [OWASP IaC Security Guide](https://owasp.org/www-project-infrastructure-as-code-security/)*

## 🛡️ Policy-as-Code Integration
*Comparison: [OPA Terraform Docs](https://www.openpolicyagent.org/docs/latest/terraform/)*

## 🚀 Enhancement Opportunities
*Comparison: [Terraform Registry Modules](https://registry.terraform.io/)*
```

```