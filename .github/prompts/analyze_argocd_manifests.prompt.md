````markdown
<!--
title: "Analyze ArgoCD Manifests and GitOps Configuration"
category: "Kubernetes + GitOps"
description: "Audit ArgoCD Application manifests, sync policies, GitOps structure, and security best practices"
-->

# 🚀 ArgoCD Application & GitOps Manifest Audit

You are a GitOps Engineer and Kubernetes Delivery Architect. Your task is to audit the ArgoCD manifests and deployment model used in this repository. Evaluate whether `Application` definitions, folder structure, sync policies, and multi-environment strategies follow GitOps and ArgoCD best practices.

---

## 🎯 Step 1: Determine Analysis Context

Ask:
- “Which folder or branch contains the ArgoCD manifests (e.g., `Application`, `AppProject`, `argocd-cm`)?"
- “Is this repo a GitOps root (monorepo), application-specific, or an overlay?”
- “Are Kustomize or Helm used as the templating engine?”

Once confirmed:
```bash
git checkout {{branch_name}} && git pull
cd {{argocd_path}}
````

---

## 📦 ArgoCD Resource Types Expected

| Kind             | Description                                              |
| ---------------- | -------------------------------------------------------- |
| `Application`    | Points to target repo/branch/path and defines sync rules |
| `AppProject`     | (Optional) Groups and restricts a set of applications    |
| `argocd-cm`      | ArgoCD configmap for feature toggles, Helm repos, etc.   |
| `argocd-rbac-cm` | ArgoCD RBAC settings for UI and token permissions        |

---

## ✅ Functional Review

* Are `Application` manifests complete and versioned?
* Is `source.repoURL`, `targetRevision`, and `path` configured properly?
* Is sync strategy declarative (auto-sync, retry)?
* Are health and sync waves/hooks defined where necessary?
* Are templating engines declared properly (`kustomize`, `helm`, `plugin`)?

---

## 🛠️ Best Practice Review

Compare to:

* [ArgoCD Application Best Practices](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/)
* [GitOps Repository Patterns (CNCF)](https://www.gitops.tech/blog/2021/04/16/gitops-repo-structure/)

Evaluate:

* Separate folders per environment (`dev/`, `staging/`, `prod/`)
* Use of Helm/Kustomize overlays for environment drift control
* Use of `destination.namespace` and `destination.server`
* Clear naming and label conventions across `Applications`
* Use of `ignoreDifferences` and `syncOptions` for fine-tuning
* `project:` references to scoped `AppProject`

---

## 🔒 Security Observations

Compare to:

* [ArgoCD Security Practices](https://argo-cd.readthedocs.io/en/stable/operator-manual/security/)

Evaluate:

* Use of namespace isolation (`destination.namespace`)
* Use of `AppProject` to restrict destinations and sources
* Disable orphaned resource deletion unless explicitly safe
* Are secrets exposed via Git or injected securely at runtime?
* ArgoCD tokens/RBAC config (e.g., `argocd-rbac-cm.yaml`)
* Are Git webhook tokens or credentials encrypted?

---

## 🚀 Enhancement Opportunities

Compare to:

* [CNCF GitOps Maturity Guide](https://github.com/cncf/tag-app-delivery/blob/main/gitops-maturity-model.md)
* [ArgoCD Sync Waves & Hooks](https://argo-cd.readthedocs.io/en/stable/user-guide/sync-waves/)

Recommend:

* Add `helm-values.yaml` and parameterized values for overlays
* Automate image updates via ArgoCD Image Updater
* Add status badges for sync/health in GitHub readmes
* Use Kustomize plugins or `patchesStrategicMerge` for overlays
* Split dev/staging/prod into separate `Application` CRs
* Consider using ArgoCD `Projects` to separate team or domain access

---

## 🧾 Output Format

```markdown
## 📌 Purpose Summary

## ✅ Functional Review

## 🛠️ Best Practice Suggestions
*Comparison: [ArgoCD Application Best Practices](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/)*

## 🔒 Security Observations
*Comparison: [ArgoCD Security Practices](https://argo-cd.readthedocs.io/en/stable/operator-manual/security/)*

## 🚀 Enhancement Opportunities
*Comparison: [GitOps Repo Patterns](https://www.gitops.tech/blog/2021/04/16/gitops-repo-structure/)*
```