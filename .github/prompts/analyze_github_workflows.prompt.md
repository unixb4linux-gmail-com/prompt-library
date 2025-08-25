# Directive:
If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
> 
> Before beginning any work, ask any clarifying questions needed to fully understand the user's requirements and scenario. Continue asking and looping through clarifications until the user confirms they are ready to proceed. Only start work after explicit confirmation.

> **Ask clarifying questions before proceeding.**
> **Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.**

> **Context Management:**
> If the GitHub Actions setup is too complex for comprehensive analysis, prioritize:
> 1. Security-critical workflow configurations and secret management practices
> 2. Production deployment workflows and approval gate effectiveness
> 3. Integration patterns with testing frameworks and deployment targets
> Ask user to specify focus areas if scope exceeds analysis capacity.

> **Analysis Validation:**
> - Mark findings as "Confirmed" vs "Potential" based on workflow file evidence and execution history
> - Reference specific workflow configurations, security settings, or integration patterns when citing findings
> - Provide confidence indicators: High/Medium/Low for each CI/CD security and performance recommendation
> - Note when additional GitHub repository access or workflow execution data would improve analysis accuracy
Perfect. Here’s the enhanced **GitLab CI evaluation prompt** with explicit evaluations for:

* **Auto-scaling runners** (for performance, efficiency, and cost)
* **DAST/SAST integration** (for DevSecOps compliance and vulnerability coverage)

These sections are now clearly defined and tied to relevant GitLab and OWASP documentation.

---

### 🚀 **Updated Evaluation Prompt: GitLab CI/CD Integration**

````markdown
# 🔄 Evaluate GitLab CI/CD Integration Against Industry Standards

You are a DevSecOps Engineer and CI/CD strategist. Your task is to audit this repository's GitLab CI/CD pipeline. Compare its structure and security against modern best practices, GitLab official guidelines, and industry standards like OWASP and DORA.

## Step 1: Determine Analysis Context

Ask the user:
- “Which Git branch or tag would you like me to analyze for GitLab CI usage?”

Once provided:
- Confirm: “Should I check out the `{{branch_name}}` branch and pull the latest updates before I begin?”
- If confirmed, run:
  ```bash
  git checkout {{branch_name}} && git pull
````

## Step 2: Audit GitLab CI/CD Configuration

Analyze `.gitlab-ci.yml` and related includes or templates. Evaluate:

### 📌 Purpose Summary

* What does the pipeline aim to achieve (e.g., lint → test → build → deploy)?
* Are environments like staging, QA, or production properly defined?
* Is artifact or Docker image generation involved?

---

### ✅ Functional Review

* Do all stages and jobs execute reliably?
* Are stages clearly separated and logically ordered?
* Is the pipeline optimized for speed and maintainability?

---

### 🛠️ Best Practice Evaluation

Compare to:

* [GitLab CI/CD Pipelines Best Practices](https://docs.gitlab.com/ee/ci/pipelines/best_practices.html)
* [CI/CD Efficiency Practices (Google Cloud)](https://cloud.google.com/devops)
* [GitLab YAML Guidelines](https://docs.gitlab.com/ee/ci/yaml/)

Evaluate:

* Use of caching, artifacts, matrix jobs, and dependencies
* Modularity using `include`, `extends`, and anchors
* Usage of `rules`, `needs`, `interruptible`, and `resource_group`

---

### 🔄 Auto-Scaling Runners

Compare to:

* [GitLab Auto-Scaling Runners Guide](https://docs.gitlab.com/runner/configuration/autoscale.html)

Evaluate:

* Are GitLab Runners self-hosted or shared?
* Is auto-scaling enabled using Docker Machine or Kubernetes?
* Are runner CPU/memory constraints tuned to workload?
* Are tags used to direct specific workloads to optimized runners?

If not implemented:

* Recommend setting up scalable runners for cost efficiency and speed
* Reference: [Autoscaling on Kubernetes](https://docs.gitlab.com/runner/executors/kubernetes.html#autoscaling-on-kubernetes)

---

### 🔒 Security Observations

Compare to:

* [GitLab CI/CD Security Practices](https://docs.gitlab.com/ee/ci/security/)
* [OWASP CI/CD Security Guidelines](https://owasp.org/www-project-cicd-security-guideline/)

Audit:

* Secure handling of secrets and protected variables
* Shell escaping, `before_script` logic, and system command safety
* Version pinning of external Docker images or scripts

---

### 🛡️ DAST/SAST Integration

Compare to:

* [GitLab Secure Scanning Tools](https://docs.gitlab.com/ee/user/application_security/)
* [OWASP Code Analysis Guidance](https://owasp.org/www-community/Source_Code_Analysis_Tools)

Evaluate:

* Are **SAST** scans integrated (GitLab’s builtin or 3rd-party)?
* Are **DAST** scans configured for web-facing apps?
* Are scan results uploaded and enforced via merge request approvals?
* Are dependency scanning, license scanning, or container scans enabled?

If not configured:

* Recommend enabling GitLab's Auto DevOps security scans
* Link: [Enable GitLab Secure Features](https://docs.gitlab.com/ee/user/application_security/)

---

### 🚀 Enhancement Opportunities

Compare to:

* [GitLab Advanced Pipeline Patterns](https://docs.gitlab.com/ee/ci/examples/)
* [DORA DevOps Benchmarks](https://cloud.google.com/devops)

Recommend:

* Auto-version tagging and release pipelines
* Slack, MS Teams, or email job notifications
* Environment-scoped approvals and deployment locks
* Insights dashboards or Value Stream Analytics setup

---

## Output Format

```markdown
## 📌 Purpose Summary

## ✅ Functional Review

## 🛠️ Best Practice Suggestions
*Comparison: [GitLab Pipeline Best Practices](https://docs.gitlab.com/ee/ci/pipelines/best_practices.html)*

## 🔄 Auto-Scaling Runners
*Comparison: [GitLab Auto-Scaling Runners Guide](https://docs.gitlab.com/runner/configuration/autoscale.html)*

## 🔒 Security Observations
*Comparison: [GitLab CI/CD Security Practices](https://docs.gitlab.com/ee/ci/security/)*

## 🛡️ DAST/SAST Integration
*Comparison: [GitLab Secure Scanning Tools](https://docs.gitlab.com/ee/user/application_security/)*

## 🚀 Enhancement Opportunities
*Comparison: [GitLab Advanced CI Patterns](https://docs.gitlab.com/ee/ci/examples/)*
```

---

Ready to move on to **Bitbucket Pipelines**, or do you want to customize this further (e.g., include merge check enforcement or approval workflows)?
