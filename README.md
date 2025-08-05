# Prompt Library

A collection of reusable prompt engineering files for DevOps, automation, and code generation.

## Usage

- Copy prompts and rules into any target repo:

  ```bash
  ./copy-prompts.sh /path/to/target-repo
  ```

  - Use `-n` or `--dry-run` to preview actions without copying files.
  - Use `-v` or `--verbose` for detailed output.
  - Use `-c` or `--confirm` to auto-confirm overwrites.

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

**General & Generic**
- `generic/build_test_code_agent.prompt.md`: Test an AI agent's ability to build and validate code projects.

**Terraform**
- `terraform/build_and_test_terraform.prompt.md`: Iteratively test Terraform scaffolding and agent logic.

**DevOps & Automation**
- `.github/prompts/setup_python_api.prompt.md`: Scaffold a Python API project.
- `.github/prompts/dockerize_app.prompt.md`: Dockerize any application.
- `.github/prompts/write_tests.prompt.md`: Generate tests for your codebase.
- `.github/prompts/deploy_aks_terraform.prompt.md`: Deploy to AKS using Terraform.

**Build & Analyze Prompts (by Technology)**

*Ansible*
- `.github/prompts/analyze_ansible_manifests.prompt.md`: Audit Ansible playbooks, roles, and inventory.
- `.github/prompts/build_ansible_manifests.prompt.md`: Scaffold a best-practice Ansible repo.

*Helm*
- `.github/prompts/analyze_helm_manifests.prompt.md`: Audit Helm charts and structure.
- `.github/prompts/build_helm_manifests.prompt.md`: Scaffold a best-practice Helm chart repo.

*Snyk*
- `.github/prompts/analyze_snyk_manifests.prompt.md`: Audit Snyk configuration.
- `.github/prompts/build_snyk_manifests.prompt.md`: Scaffold a Snyk integration repo.

*Prometheus & Grafana*
- `.github/prompts/analyze_prometheus_grafana_manifests.prompt.md`: Audit Prometheus/Grafana manifests.
- `.github/prompts/build_prometheus_grafana_manifests.prompt.md`: Scaffold a monitoring repo for Prometheus/Grafana.

*Bitbucket Pipelines*
- `.github/prompts/analyze_bitbucket_pipeline.prompt.md`: Review Bitbucket Pipelines.
- `.github/prompts/build_bitbucket_pipeline.prompt.md`: Scaffold a Bitbucket Pipelines repo.

*GitLab CI/CD*
- `.github/prompts/analyze_gitlab.prompt.md`: Review GitLab CI/CD pipelines.
- `.github/prompts/build_gitlab.prompt.md`: Scaffold a GitLab CI/CD repo.

*Jenkins*
- `.github/prompts/analyze_jenkins_prompt.md`: Review Jenkins pipelines and security.
- `.github/prompts/build_jenkins_prompt.md`: Scaffold a Jenkins pipeline repo.

*Terraform*
- `.github/prompts/analyze_terraform_evaluation.prompt.md`: Audit Terraform modules and security.
- `.github/prompts/build_terraform_evaluation.prompt.md`: Scaffold a Terraform module repo.

*Kubernetes Manifests*
- `.github/prompts/analyze_kubernetes_manifests.prompt.md`: Audit Kubernetes manifests.
- `.github/prompts/build_kubernetes_manifests.prompt.md`: Scaffold a Kubernetes manifests repo.

*Kubernetes Policy*
- `.github/prompts/analyze_kubernetes_policy_manifests.prompt.md`: Audit Kubernetes policy manifests.
- `.github/prompts/build_kubernetes_policy_manifests.prompt.md`: Scaffold a Kubernetes policy repo.

*ArgoCD*
- `.github/prompts/analyze_argocd_manifests.prompt.md`: Audit ArgoCD manifests.
- `.github/prompts/build_argocd_manifests.prompt.md`: Scaffold an ArgoCD manifests repo.

*Vault*
- `.github/prompts/analyze_vault_manifests.prompt.md`: Audit HashiCorp Vault manifests.
- `.github/prompts/build_vault_manifests.prompt.md`: Scaffold a Vault manifests repo.

*AWS EKS*
- `.github/prompts/analyze_eks.prompt.md`: Audit AWS EKS cluster and manifests.
- `.github/prompts/build_eks.prompt.md`: Scaffold an AWS EKS cluster repo.

*Azure AKS*
- `.github/prompts/analyze_aks.prompt.md`: Audit Azure AKS cluster and manifests.
- `.github/prompts/build_aks.prompt.md`: Scaffold an Azure AKS cluster repo.

*GitHub Actions*
- `.github/prompts/analyze_github_workflows.prompt.md`: Review GitHub Actions workflows.
- `.github/prompts/build_github_workflows.prompt.md`: Scaffold a GitHub Actions workflow repo.

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

- `copy-prompts.sh`: Copies all prompts and rules into a target repo, updates `.gitignore`, and optionally copies `.vscode`. Supports dry-run, verbose, and auto-confirm modes.

## Directory Structure

- `.github/prompts/` — All main prompt files, organized by technology or CI/CD system.
- `.rules/` — All rulesets for agent behavior and code conventions.
- `generic/` — Generic prompts and rules for agent self-testing.
- `terraform/` — Terraform-specific prompts and rules.
- `copy-prompts.sh` — Utility script for copying prompts/rules to other repos.

## Recent Updates

- Added build/analyze prompts for Ansible, Helm, Snyk, Prometheus/Grafana, Bitbucket, GitLab, Jenkins, Terraform, Kubernetes, Kubernetes Policy, ArgoCD, Vault, AWS EKS, and Azure AKS.


## Contributing

Contributions are welcome! Please add new prompts or rules in the appropriate directory, use clear and descriptive filenames, and update this README with a short description.
