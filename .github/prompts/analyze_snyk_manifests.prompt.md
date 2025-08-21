> **Directive:**
> 
> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
````markdown
<!--
title: "Analyze Snyk Integration and Manifests"
category: "Security Scanning"
description: "Audit Snyk configuration, usage in CI/CD, policy enforcement, and scanning coverage"
-->

# 🧬 Snyk Security Scanning Integration Audit

You are a DevSecOps Engineer. Your task is to evaluate how Snyk is integrated into this repository’s manifests and CI/CD workflows. Audit configuration for SAST, container, IaC, and license scanning. Recommend improvements based on modern scanning practices.

---

## 🎯 Step 1: Determine Analysis Context

Ask:
- “Where is Snyk configured — in CI/CD (e.g., GitHub Actions), manually via CLI, or in Dockerfiles?”
- “What types of projects are scanned (e.g., Node.js, Python, Docker, Terraform)?”
- “Are policy thresholds enforced (fail on high/critical)?”

Once confirmed:
```bash
git checkout {{branch_name}} && git pull
````

---

## 📦 Snyk Usage Patterns to Review

| Integration Target  | Configuration Method                                                        |
| ------------------- | --------------------------------------------------------------------------- |
| Source code (SAST)  | `snyk test`, `snyk code test`, `.snyk` policy files                         |
| Docker containers   | `snyk container test` in CI, Dockerfiles, or `snyk monitor`                 |
| IaC (Terraform/K8s) | `snyk iac test`, GitHub workflows, `.snyk` policies                         |
| GitHub UI           | Snyk GitHub App enabled, repo connected                                     |
| CI/CD workflows     | GitHub Actions, Jenkins, Bitbucket, GitLab CI steps for `snyk test/monitor` |

---

## ✅ Functional Review

* Is `snyk test` used for source and Docker scanning?
* Are vulnerable images or dependencies flagged in CI?
* Are scan results posted in PR comments, dashboards, or Snyk UI?
* Are `.snyk` ignore files used? Are they justified?
* Are different environments (dev, prod) scanned?

---

## 🛠️ Best Practice Review

Compare to:

* [Snyk Integration Docs](https://docs.snyk.io/)
* [Snyk CLI Best Practices](https://docs.snyk.io/snyk-cli)

Evaluate:

* Is `snyk monitor` used to track projects in the Snyk dashboard?
* Are fail conditions enforced for critical issues (`--severity-threshold=high`)?
* Is the Snyk token stored securely in CI secrets or GitHub Actions?
* Are licenses and CVEs reported and used for blocking merges?
* Are projects grouped logically (e.g., web, api, infra) in Snyk?

---

## 🔒 Security Observations

Compare to:

* [OWASP Dependency Management](https://owasp.org/www-project-dependency-check/)
* [Snyk Code Guidelines](https://snyk.io/product/snyk-code/)

Evaluate:

* Are outdated packages flagged and remediated regularly?
* Are OSS vulnerabilities triaged with clear ownership?
* Is dependency graph scanned recursively (for transitive deps)?
* Are custom policies applied to suppress or prioritize CVEs?
* Are container base images scanned with `snyk container test`?

---

## 🚀 Enhancement Opportunities

Compare to:

* [Snyk CI/CD Examples](https://github.com/snyk/actions)
* [Secure Software Supply Chain Guide (CNCF)](https://github.com/cncf/sig-security/tree/main/supply-chain-security)

Recommend:

* Auto-scan all new branches with GitHub Actions or similar
* Fail builds only on high/critical vulnerabilities with actionable logs
* Add `snyk test` and `snyk iac test` to Terraform and Kubernetes deployments
* Use `snyk protect` to patch runtime vulnerabilities (when supported)
* Visualize dashboards and trends via Snyk Web UI or Slack alerts

---

## 🧾 Output Format

```markdown
## 📌 Purpose Summary

## ✅ Functional Review

## 🛠️ Best Practice Suggestions
*Comparison: [Snyk CLI Best Practices](https://docs.snyk.io/snyk-cli)*

## 🔒 Security Observations
*Comparison: [OWASP Dependency Management](https://owasp.org/www-project-dependency-check/)*

## 🚀 Enhancement Opportunities
*Comparison: [Snyk GitHub Actions](https://github.com/snyk/actions)*
```