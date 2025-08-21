> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

<!--
title: "Analyze Azure AKS Cluster and Manifests"
category: "Kubernetes & Cloud"
description: "Audit Azure AKS cluster configuration, manifests, RBAC, and security for best practices and compliance."
-->

# ☁️ Analyze Azure AKS Cluster & Manifests

You are a Cloud Platform Engineer. Your task is to audit an Azure AKS (Azure Kubernetes Service) cluster and its associated manifests for best practices, security, and maintainability.

---

## 🎯 Step 1: Determine Analysis Context

Ask:
- “Which Azure subscription and region is the AKS cluster deployed in?”
- “Where are the Kubernetes manifests and IaC (e.g., Bicep, Terraform, ARM) stored?”
- “Is the cluster managed via GitOps, IaC, or manually?”

Once confirmed:
```bash
az aks get-credentials --resource-group {{resource_group}} --name {{cluster_name}}
cd {{manifests_path}}
```

---

## 📦 AKS Structure Expected

| Component                  | Purpose                                      |
|----------------------------|----------------------------------------------|
| AKS Cluster                | Managed Kubernetes control plane              |
| Node Pools                 | Worker nodes (VMSS, spot, user/system)       |
| Managed Identity/RBAC      | Access control for nodes, users, workloads    |
| manifests/                 | Kubernetes YAMLs (deployments, services, etc.)|
| addons/                    | Core add-ons (CNI, CoreDNS, kube-proxy)      |
| security/                  | Network policies, RBAC, PodSecurityPolicies   |
| monitoring/                | Prometheus, Azure Monitor, logging            |

---

## ✅ Functional Review

* Are all manifests valid and applied successfully?
* Are node pools and scaling policies configured correctly?
* Are add-ons up to date and healthy?
* Is cluster autoscaler or HPA enabled?
* Are workloads scheduled as intended (taints/tolerations, affinity)?

---

## 🛠️ Best Practice Review

Compare to:

* [AKS Best Practices Guide](https://learn.microsoft.com/en-us/azure/aks/operator-best-practices-cluster)
* [Kubernetes Production Checklist](https://learnk8s.io/production-best-practices)

Evaluate:

* Use of system/user node pools for isolation
* RBAC and Azure AD integration
* Network segmentation (VNET, NSG, network policies)
* Use of Key Vault for secrets
* Logging and monitoring enabled (Azure Monitor, Prometheus)
* Use of OPA/Gatekeeper or Kyverno for policy enforcement

---

## 🔒 Security Observations

Compare to:

* [AKS Security Best Practices](https://learn.microsoft.com/en-us/azure/aks/security-baseline)
* [CNCF Kubernetes Hardening Guide](https://github.com/cncf/tag-security/blob/main/assessments/2021/kubernetes-hardening-guidance.md)

Evaluate:

* Are managed identities and RBAC least-privilege and scoped?
* Are secrets stored in Key Vault or encrypted at rest?
* Are public endpoints restricted?
* Are pod security policies or alternatives enforced?
* Are audit logs enabled?

---

## 🚀 Enhancement Opportunities

Compare to:

* [AKS Add-ons Catalog](https://learn.microsoft.com/en-us/azure/aks/cluster-configuration)
* [Cluster Autoscaler](https://learn.microsoft.com/en-us/azure/aks/cluster-autoscaler)

Recommend:

* Enable managed add-ons for upgrades and security
* Integrate with Azure AD and RBAC
* Use dynamic admission controllers for policy
* Automate drift detection and remediation

---

## 🧾 Output Format

```markdown
## 📌 Purpose Summary

## ✅ Functional Review

## 🛠️ Best Practice Suggestions
*Comparison: [AKS Best Practices Guide](https://learn.microsoft.com/en-us/azure/aks/operator-best-practices-cluster)*

## 🔒 Security Observations
*Comparison: [AKS Security Best Practices](https://learn.microsoft.com/en-us/azure/aks/security-baseline)*

## 🚀 Enhancement Opportunities
*Comparison: [AKS Add-ons Catalog](https://learn.microsoft.com/en-us/azure/aks/cluster-configuration)*
```
