# Prompt Library

A collection of reusable prompt engineering files for DevOps, automation, and code generation.

## Versioning

**All 57 prompt files are now versioned using semantic versioning (SemVer).**

- **Current Version**: All prompts start at `v1.0.0` as of 2025-08-26
- **Version Format**: `MAJOR.MINOR.PATCH` (following [Semantic Versioning](https://semver.org/))
- **Metadata**: Each prompt includes `version`, `created_date`, and `last_updated` in YAML frontmatter
- **Version Management**: Use `scripts/version_prompts.py` to update version information across all prompts


## CI & Automation

- Automated linting and validation is run on every push and PR via GitHub Actions:
  - Shell scripts are checked with shellcheck.
  - Markdown files are linted for style.
  - All prompt and rule files are checked for required YAML frontmatter.

- Run `scripts/generate_index.py` to generate `PROMPT_RULE_INDEX.md` (an index of all prompts and rules).
- Run `scripts/version_prompts.py` to add or update version information across all prompt files.

- All prompt and rule files now include YAML frontmatter for metadata (author, category, description, version, dates).

- Example output/test case files for prompts are provided in the same directory as the prompt, with the suffix `.example.md` or `.test.md`.

## Usage


## Prompt Engineering Best Practices

All 57 prompt files implement comprehensive AI prompt engineering best practices for maximum effectiveness:

### **Core Safety & Permission Patterns**

> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.

### **Advanced Context Management**

All prompts include **Context Management** sections that handle complex scenarios:
- **Smart scope adjustment**: Prioritize security-critical items when scope exceeds capacity
- **Domain-specific guidance**: Tailored prioritization for each technology domain
- **Progressive disclosure**: Break complex tasks into manageable phases
- **User focus specification**: Allow users to specify focus areas for overwhelming scenarios

### **Analysis Validation Framework**

Every prompt implements **Analysis Validation** patterns for reliable results:
- **Evidence-based findings**: Mark all findings as "Confirmed" vs "Potential" based on actual evidence
- **Specific referencing**: Require citations of actual configurations, settings, or patterns  
- **Confidence indicators**: Provide High/Medium/Low confidence ratings for each recommendation
- **Access improvement guidance**: Suggest additional access or tools that would improve analysis accuracy

### **Enhanced Output Quality**

- **Structured recommendations**: Consistent format with confidence scoring and evidence citation
- **Security-first prioritization**: Always prioritize security-critical findings and configurations
- **Actionable guidance**: All recommendations include specific implementation steps and validation methods

- Copy prompts and rules into any target repo:

  ```bash
  ./copy-prompts.sh /path/to/target-repo
  ```

  - Use `-n` or `--dry-run` to preview actions without copying files.
  - Use `-v` or `--verbose` for detailed output.
  - Use `-c` or `--confirm` to auto-confirm overwrites.
  - Use `--no-gitignore-prompts` to skip adding `.github/prompts/` to the target repo's `.gitignore` (default is to include it).

  After the script runs, if `.github/prompts/` was added to `.gitignore`, you will be interactively prompted to keep or remove the entry.

- Prompts will be placed in: `.github/prompts/`
- Rules will be placed in: `.rules/`
- The `.vscode` directory will be placed in: `.vscode/`

- Each prompt file includes metadata for easy filtering and automation.
- Rules files provide structured behavior and expectations for AI agents using the prompts.

### Troubleshooting

- If you see permission errors, ensure you have write access to the target directory.
- If files are not copied, check that the source files exist and paths are correct.
- For existing files, you will be prompted before overwriting unless you use `-c`.
- Use dry-run mode to safely preview changes before applying.


## Prompts

Prompts are reusable scenario files for AI agents. They are organized by technology and use case:


### General & Generic

- `generic/build_test_code_agent.prompt.md`: Test an AI agent's ability to build and validate code projects.
- `.github/prompts/onboard_devops_new_client.prompt.md`: Step-by-step onboarding guide for new DevOps consultants joining a client project.

### Discovery & Recon Prompts

- `.github/prompts/recon_tools_local.prompt.md`: Enumerate installed DevOps tools, versions, and config footprints.
- `.github/prompts/recon_accounts_sessions.prompt.md`: Summarize professional git identities, CLI sessions, and work app presence.
- `.github/prompts/recon_cloud_credentials.prompt.md`: Locate and summarize professional cloud credentials and profiles.
- `.github/prompts/recon_cicd_integrations.prompt.md`: Identify CI/CD configurations in local repos, including triggers and secret references.
- `.github/prompts/recon_k8s_and_containers.prompt.md`: Inventory Kubernetes contexts and local container runtimes.
- `.github/prompts/recon_iac_automation.prompt.md`: Discover infrastructure-as-code (IaC) assets and summarize modules, providers, and backends.
- `.github/prompts/recon_devops_master.prompt.md`: Interactive, comprehensive DevOps recon covering tools, accounts, cloud, CI/CD, K8s, and IaC.
- `.github/prompts/recon_circleci.prompt.md`: Discover and inventory CircleCI configurations, contexts, and integrations.

### Terraform (Build & Test)


- `terraform/build_and_test_terraform.prompt.md`: Iteratively test Terraform scaffolding and agent logic.


### DevOps & Automation


- `.github/prompts/setup_python_api.prompt.md`: Scaffold a Python API project.
- `.github/prompts/dockerize_app.prompt.md`: Dockerize any application.
- `.github/prompts/write_tests.prompt.md`: Generate tests for your codebase.

- `.github/prompts/deploy_aks_terraform.prompt.md`: Deploy to AKS using Terraform.


### Build & Analyze Prompts (by Technology)


#### Ansible

- `.github/prompts/analyze_ansible_manifests.prompt.md`: Audit Ansible playbooks, roles, and inventory.

- `.github/prompts/build_ansible_manifests.prompt.md`: Scaffold a best-practice Ansible repo.


#### Helm

- `.github/prompts/analyze_helm_manifests.prompt.md`: Audit Helm charts and structure.

- `.github/prompts/build_helm_manifests.prompt.md`: Scaffold a best-practice Helm chart repo.


#### Snyk

- `.github/prompts/analyze_snyk_manifests.prompt.md`: Audit Snyk configuration.

- `.github/prompts/build_snyk_manifests.prompt.md`: Scaffold a Snyk integration repo.


#### Prometheus & Grafana

- `.github/prompts/analyze_prometheus_grafana_manifests.prompt.md`: Audit Prometheus/Grafana manifests.

- `.github/prompts/build_prometheus_grafana_manifests.prompt.md`: Scaffold a monitoring repo for Prometheus/Grafana.


#### Bitbucket Pipelines

- `.github/prompts/analyze_bitbucket_pipeline.prompt.md`: Review Bitbucket Pipelines.

- `.github/prompts/build_bitbucket_pipeline.prompt.md`: Scaffold a Bitbucket Pipelines repo.


#### GitLab CI/CD

- `.github/prompts/analyze_gitlab.prompt.md`: Review GitLab CI/CD pipelines.

- `.github/prompts/build_gitlab.prompt.md`: Scaffold a GitLab CI/CD repo.


#### Jenkins

- `.github/prompts/analyze_jenkins_prompt.md`: Review Jenkins pipelines and security.

- `.github/prompts/build_jenkins_prompt.md`: Scaffold a Jenkins pipeline repo.


#### Terraform (Audit)

- `.github/prompts/analyze_terraform_evaluation.prompt.md`: Audit Terraform modules and security.

- `.github/prompts/build_terraform_evaluation.prompt.md`: Scaffold a Terraform module repo.


#### Kubernetes Manifests

- `.github/prompts/analyze_kubernetes_manifests.prompt.md`: Audit Kubernetes manifests.

- `.github/prompts/build_kubernetes_manifests.prompt.md`: Scaffold a Kubernetes manifests repo.


#### Kubernetes Policy

- `.github/prompts/analyze_kubernetes_policy_manifests.prompt.md`: Audit Kubernetes policy manifests.

- `.github/prompts/build_kubernetes_policy_manifests.prompt.md`: Scaffold a Kubernetes policy repo.


#### ArgoCD

- `.github/prompts/analyze_argocd_manifests.prompt.md`: Audit ArgoCD manifests.

- `.github/prompts/build_argocd_manifests.prompt.md`: Scaffold an ArgoCD manifests repo.


#### Vault

- `.github/prompts/analyze_vault_manifests.prompt.md`: Audit HashiCorp Vault manifests.

- `.github/prompts/build_vault_manifests.prompt.md`: Scaffold a Vault manifests repo.


#### AWS EKS

- `.github/prompts/analyze_eks.prompt.md`: Audit AWS EKS cluster and manifests.

- `.github/prompts/build_eks.prompt.md`: Scaffold an AWS EKS cluster repo.


#### Azure AKS

- `.github/prompts/analyze_aks.prompt.md`: Audit Azure AKS cluster and manifests.

- `.github/prompts/build_aks.prompt.md`: Scaffold an Azure AKS cluster repo.


#### GitHub Actions

- `.github/prompts/analyze_github_workflows.prompt.md`: Review GitHub Actions workflows.
- `.github/prompts/build_github_workflows.prompt.md`: Scaffold a GitHub Actions workflow repo.

#### CircleCI

- `.github/prompts/analyze_circleci.prompt.md`: Comprehensive audit of CircleCI workflows, orbs, and security.
- `.github/prompts/build_circleci.prompt.md`: Scaffold a comprehensive CircleCI pipeline repository.

#### Azure DevOps

- `.github/prompts/analyze_azure_devops.prompt.md`: Audit Azure DevOps YAML pipelines, variable groups, and service connections.
- `.github/prompts/build_azure_devops.prompt.md`: Scaffold comprehensive Azure DevOps YAML pipelines with templates and security.

**Observability & Monitoring**

#### Datadog

- `.github/prompts/analyze_datadog.prompt.md`: Comprehensive audit of Datadog monitoring, dashboards, alerts, APM, and infrastructure observability.

#### ELK Stack

- `.github/prompts/analyze_elk_stack.prompt.md`: Audit Elasticsearch, Logstash, Kibana setup, log aggregation, and search capabilities.

**Security & Code Quality**

#### SonarQube

- `.github/prompts/analyze_sonarqube.prompt.md`: Audit SonarQube setup, quality gates, security rules, and DevSecOps integration.

#### Trivy

- `.github/prompts/analyze_trivy.prompt.md`: Audit Trivy vulnerability scanning, container security, and IaC security scanning.

**Cloud & Serverless**

#### AWS Lambda

- `.github/prompts/analyze_aws_lambda.prompt.md`: Audit AWS Lambda functions, serverless architecture, performance, and security.

#### Google Cloud Platform

- `.github/prompts/analyze_gcp_gke.prompt.md`: Audit Google Kubernetes Engine cluster setup, security, and networking.

**Platform Engineering**

#### Backstage

- `.github/prompts/analyze_backstage.prompt.md`: Audit Backstage developer portal, catalog, plugins, and platform engineering implementation.

**SRE & Incident Response**

#### Incident Management

- `.github/prompts/analyze_incident_management.prompt.md`: Audit incident management processes, tools, alerting, escalation policies, and response procedures for SRE best practices.

**Codebase & CI/CD Analysis**

- `.github/prompts/analyze_codebase.prompt.md`: Audit the entire repository for architecture, security, and best practices.
- `.github/prompts/analyze_github_workflows.prompt.md`: Review GitHub Actions workflows.
- `.github/prompts/analyze_gitlab.prompt.md`: Review GitLab CI/CD pipelines.
- `.github/prompts/analyze_bitbucket_pipeline.prompt.md`: Review Bitbucket Pipelines.
- `.github/prompts/analyze_jenkins_prompt.md`: Review Jenkins pipelines and security.

**Kubernetes & Cloud**
- `.github/prompts/analyze_kubernetes_live_cluster.prompt.md`: Analyze a live Kubernetes cluster.
- `.github/prompts/analyze_kubernetes_manifests.prompt.md`: Audit Kubernetes manifests.
- `.github/prompts/analyze_kubernetes_policy_manifests.prompt.md`: Audit Kubernetes policy manifests.
- `.github/prompts/analyze_helm_manifests.prompt.md`: Audit Helm charts and structure.
- `.github/prompts/analyze_argocd_manifests.prompt.md`: Audit ArgoCD manifests.
- `.github/prompts/analyze_prometheus_grafana_manifests.prompt.md`: Audit Prometheus/Grafana manifests.
- `.github/prompts/analyze_snyk_manifests.prompt.md`: Audit Snyk configuration.
- `.github/prompts/analyze_terraform_evaluation.prompt.md`: Audit Terraform modules and security.
- `.github/prompts/analyze_vault_manifests.prompt.md`: Audit HashiCorp Vault manifests.

## Rules

Rules define conventions and agent behaviors for different stacks. All rules are in the `.rules/` directory:

- `copy-prompts.rules.mdc`: Behavior for the copy-prompts.sh script.
- `python.mdc`: Python project conventions.
- `react.mdc`: React component conventions.
- `typescript.mdc`: TypeScript project conventions.
- `ruby.mdc`: Ruby code conventions.
- `ruby-on-rails.mdc`: Ruby on Rails conventions.
- `nodejs.mdc`: Node.js project conventions.
- `nextjs-app-router.mdc`: Next.js App Router conventions.
- `react-component.mdc`: React component-specific rules.

**Generic & Terraform Agent Rules**
- `generic/build_test_code_agent.rules.mdc`: Rules for generic agent self-testing.
- `terraform/build_and_test_terraform.rules.mdc`: Rules for Terraform agent testing.

## Utility Scripts

- `copy-prompts.sh`: Copies all prompts and rules into a target repo, updates `.gitignore` (by default adds `.github/prompts/`, `.rules/`, and `.vscode/`), and optionally copies `.vscode`. Supports dry-run, verbose, auto-confirm, and the `--no-gitignore-prompts` flag to skip adding `.github/prompts/` to `.gitignore`. After running, you will be prompted to keep or remove the `.github/prompts/` entry if it was added.

- `scripts/generate_index.py`: Generates the comprehensive `PROMPT_RULE_INDEX.md` file by parsing YAML frontmatter from all prompt and rule files.

- `scripts/version_prompts.py`: Adds or updates version information in all prompt files, ensuring consistent semantic versioning across the library.

## Directory Structure

- `.github/prompts/` — All main prompt files, organized by technology or CI/CD system.
- `.rules/` — All rulesets for agent behavior and code conventions.
- `generic/` — Generic prompts and rules for agent self-testing.
- `terraform/` — Terraform-specific prompts and rules.
- `scripts/` — Index generation, versioning, and distribution utilities.
- `copy-prompts.sh` — Utility script for copying prompts/rules to other repos.
- `CLAUDE.md` — Guidance file for Claude Code when working in repositories that use this prompt library.

## Recent Updates

### **Prompt Versioning System Implementation** 🏷️ _(2025-08-26)_

**Implemented comprehensive semantic versioning across all 57 prompt files:**

- ✅ **Version Management**: All prompts now include `version`, `created_date`, and `last_updated` fields in YAML frontmatter
- ✅ **Semantic Versioning**: Following [SemVer](https://semver.org/) format (MAJOR.MINOR.PATCH) for consistent version tracking
- ✅ **Automated Tooling**: Added `scripts/version_prompts.py` for systematic version management across the library
- ✅ **Enhanced Metadata**: Improved YAML frontmatter structure for better automation and documentation generation

### **AI Prompt Engineering Best Practices Rollout** ✨

**Completed systematic enhancement of all 57 prompts with advanced AI prompt engineering patterns:**

- **Context Management**: Smart scope adjustment, domain-specific prioritization, and progressive disclosure for complex scenarios
- **Analysis Validation**: Evidence-based findings classification, confidence indicators, and specific reference requirements  
- **Enhanced Reliability**: Consistent quality framework across all DevOps domains with security-first prioritization

### **Major Domain Coverage Expansion**

Added comprehensive prompts for previously missing tools including:

- **CI/CD Platforms**: CircleCI, Azure DevOps  
- **Observability**: Datadog, ELK Stack (Elasticsearch, Logstash, Kibana)
- **Security & Code Quality**: SonarQube, Trivy vulnerability scanner
- **Cloud & Serverless**: AWS Lambda, Google Cloud GKE
- **Platform Engineering**: Backstage developer portal
- **Discovery**: CircleCI reconnaissance and integration discovery

Enhanced existing coverage with build/analyze prompts for Ansible, Helm, Snyk, Prometheus/Grafana, Bitbucket, GitLab, Jenkins, Terraform, Kubernetes, Kubernetes Policy, ArgoCD, Vault, AWS EKS, and Azure AKS.

## Contributing

Contributions are welcome! Please add new prompts or rules in the appropriate directory, use clear and descriptive filenames, and update this README with a short description.
