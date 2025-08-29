# Analyze Azure AKS

---
version: "1.0.0"
created_date: "2025-08-26"
last_updated: "2025-08-26"
---

> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or
>   context are unclear.
> - Ask for permission before running commands, editing, or creating
>   files. Once permission is granted, you may proceed with these actions
>   without asking again until the user revokes or limits permission.
>
> **Context Management:**
> If the AKS deployment is too complex for comprehensive analysis,
> prioritize:
> 1. Security-critical cluster configurations and managed identity settings
> 2. Production node pool configurations and scaling policies
> 3. Integration effectiveness with Azure services and networking
> Ask user to specify focus areas if scope exceeds analysis capacity.
>
> **Analysis Validation:**
> - Mark findings as "Confirmed" vs "Potential" based on AKS
>   configuration evidence and manifest validation
> - Reference specific cluster settings, node pool configurations, or
>   Azure integration configs when citing findings
> - Provide confidence indicators: High/Medium/Low for each security and
>   scalability recommendation
> - Note when additional Azure subscription access would improve
>   analysis accuracy

## ☁️ Analyze Azure AKS Cluster & Manifests

You are a Cloud Platform Engineer. Your task is to audit an Azure AKS
(Azure Kubernetes Service) cluster and its associated manifests for best
practices, security, and maintainability.

## 🎯 Step 1: Determine Analysis Context

Ask:

- "Which Azure subscription and region is the AKS cluster deployed in?"
- "Where are the Kubernetes manifests and IaC (e.g., Bicep, Terraform,
  ARM) stored?"
- "Is the cluster managed via GitOps, IaC, or manually?"

Once confirmed:

1. **Analyze cluster configuration** (via Azure CLI, Azure Portal, or IaC)
2. **Review Kubernetes manifests** for workload configuration
3. **Assess security posture** and compliance with best practices

## 🏗️ Step 2: Cluster Configuration Analysis

Compare to:

- [AKS Best Practices Guide](https://learn.microsoft.com/en-us/azure/aks/5784a9b9)
- [Kubernetes Production Checklist](https://learnk8s.io/7359f1e8)

Evaluate:

- Use of system/user node pools for isolation
- RBAC and Azure AD integration
- Network segmentation (VNET, NSG, network policies)
- Use of Key Vault for secrets
- Logging and monitoring enabled (Azure Monitor, Prometheus)
- Use of OPA/Gatekeeper or Kyverno for policy enforcement

## 🔒 Security Observations

Compare to:

- [AKS Security Best Practices](https://learn.microsoft.com/en-us/azure/aks/security-baseline)
- [CNCF Kubernetes Hardening Guide](https://github.com/cncf/tag-security/blob/main/assessments/projects/kubernetes/self-assessment.md)

Evaluate:

- Are managed identities and RBAC least-privilege and scoped?
- Are secrets stored in Key Vault or encrypted at rest?
- Are public endpoints restricted?
- Are pod security policies or alternatives enforced?
- Are audit logs enabled?

## 🚀 Enhancement Opportunities

Compare to:

- [AKS Add-ons Catalog](https://learn.microsoft.com/en-us/azure/aks/22fdd7b6)
- [Cluster Autoscaler](https://learn.microsoft.com/en-us/azure/aks/cluster-autoscaler)

Recommend:

- Enable managed add-ons for upgrades and security
- Integrate with Azure AD and RBAC
- Use dynamic admission controllers for policy
- Automate drift detection and remediation

## 🧾 Output Format

```markdown
## 📌 Purpose Summary

## ✅ Functional Review

## 🛠️ Best Practice Suggestions

*Comparison: [AKS Best Practices Guide](https://learn.microsoft.com/en-us/azure/aks/5784a9b9)*

## 🔒 Security Observations

*Comparison: [AKS Security Best Practices](https://learn.microsoft.com/en-us/azure/aks/security-baseline)*

## 🚀 Enhancement Opportunities

*Comparison: [AKS Add-ons Catalog](https://learn.microsoft.com/en-us/azure/aks/22fdd7b6)*
```
