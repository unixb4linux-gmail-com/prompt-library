---
title: "Analyze CircleCI Configuration and Pipelines"
description: "Comprehensive audit of CircleCI workflows, orbs, security, and CI/CD best practices"
category: "CI/CD"
---

> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
> 
> Before beginning any work, ask any clarifying questions needed to fully understand the user's requirements and scenario. Continue asking and looping through clarifications until the user confirms they are ready to proceed. Only start work after explicit confirmation.

> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

# 🔄 Analyze CircleCI Configuration and Pipeline Integration

You are a DevOps Engineer and CI/CD strategist. Your task is to audit this repository's CircleCI pipeline configuration against modern best practices, CircleCI documentation, and industry standards like OWASP and DORA metrics.

## Step 1: Determine Analysis Context

Ask the user:
- "Which Git branch or tag would you like me to analyze for CircleCI usage?"

Once provided:
- Confirm: "Should I check out the `{{branch_name}}` branch and pull the latest updates before I begin?"
- If confirmed, run:
  ```bash
  git checkout {{branch_name}} && git pull
  ```

## Step 2: Audit CircleCI Configuration

Analyze `.circleci/config.yml` and related configuration files. Evaluate:

### 📌 Purpose Summary

* What does the pipeline aim to achieve (e.g., test → build → deploy)?
* Are workflows properly structured with job dependencies?
* Is artifact or Docker image generation involved?
* How are different environments (staging, production) handled?

### ✅ Configuration Review

| **Component**       | **CircleCI Resources**                                                  |
|---------------------|-------------------------------------------------------------------------|
| **Workflows**       | `workflows`, job orchestration, conditional execution                   |
| **Jobs**            | `jobs`, executors (docker/machine/macos), resource allocation          |
| **Orbs**            | Third-party orbs usage, custom orbs, security implications             |
| **Caching**         | Dependency caching, workspace persistence, cache keys                  |
| **Artifacts**       | Build artifacts, test reports, deployment packages                     |

**Analysis Focus:**
* Are jobs properly structured with appropriate executors?
* Is caching effectively used for dependencies and build artifacts?
* Are workflows optimized for parallelism and efficiency?
* How are different branches and tags handled?

### 🛡️ Security & Best Practices

| **Security Area**   | **CircleCI Best Practices**                                            |
|---------------------|-------------------------------------------------------------------------|
| **Secrets**         | Context usage, environment variables, restricted contexts              |
| **Orbs**            | Certified orbs vs. third-party, version pinning, security scanning    |
| **Resource**        | Resource classes, appropriate executor selection                       |
| **Access**          | Branch restrictions, approval jobs, manual gates                      |

**Security Checklist:**
* Are secrets stored in CircleCI contexts rather than environment variables?
* Are contexts restricted to appropriate projects/branches?
* Are third-party orbs from trusted sources and version-pinned?
* Is sensitive data properly masked in logs?
* Are manual approval steps used for production deployments?

### 🚀 Performance & Efficiency

| **Performance**     | **Optimization Areas**                                                  |
|---------------------|-------------------------------------------------------------------------|
| **Parallelism**     | Matrix builds, test splitting, concurrent jobs                         |
| **Caching**         | Dependency caching, Docker layer caching, workspace efficiency        |
| **Resource Usage**  | Appropriate resource classes, executor selection                       |
| **Pipeline Speed**  | Build times, bottlenecks, optimization opportunities                   |

**Performance Analysis:**
* Are tests split across parallel containers effectively?
* Is Docker layer caching enabled where appropriate?
* Are resource classes right-sized for workloads?
* Are there unnecessary dependencies between jobs?

### 🔗 Integration Assessment

**Discovered Integrations** (document what you find):
* Code quality tools (SonarQube, CodeClimate, etc.)
* Security scanning (Snyk, OWASP ZAP, etc.)
* Deployment targets (AWS, Azure, GCP, Kubernetes)
* Notification systems (Slack, email, PagerDuty)
* Artifact repositories (Docker Hub, ECR, etc.)

**Integration Quality:**
* Are integrations properly authenticated?
* Are deployment strategies (blue-green, rolling) implemented?
* How are deployment failures handled and rolled back?

### 📊 Monitoring & Observability

* Are build metrics and insights properly configured?
* Is test reporting integrated (JUnit, coverage reports)?
* Are deployment status checks implemented?
* How are pipeline failures monitored and alerted?

## Output Format

Respond using this structured format:

```markdown
## 📌 Purpose Summary
[High-level pipeline goals and structure]

## ✅ Configuration Review
[Job structure, workflows, orbs usage, caching strategy]

## 🛡️ Security Assessment
[Secrets management, orb security, access controls, compliance]

## 🚀 Performance Analysis
[Parallelism, caching, resource usage, build times]

## 🔗 Integration Findings
[Discovered tool integrations and their implementation quality]

## 📊 Monitoring & Metrics
[Test reporting, deployment tracking, alerting setup]

## 🎯 Recommendations
[Specific improvements with CircleCI documentation links]
```

## CircleCI Resources & References

* [CircleCI Configuration Reference](https://circleci.com/docs/configuration-reference/)
* [CircleCI Orbs Registry](https://circleci.com/developer/orbs)
* [CircleCI Security Best Practices](https://circleci.com/docs/security/)
* [CircleCI Performance Optimization](https://circleci.com/docs/optimizations/)
* [DORA Metrics for CI/CD](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance)

Be thorough, cite specific configuration sections, and provide actionable recommendations with links to CircleCI documentation.