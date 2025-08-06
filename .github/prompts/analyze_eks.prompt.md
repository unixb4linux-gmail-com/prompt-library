> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
<!--
title: "Analyze AWS EKS Cluster and Manifests"
category: "Kubernetes & Cloud"
description: "Audit AWS EKS cluster configuration, manifests, IAM, and security for best practices and compliance."
-->

# ☁️ Analyze AWS EKS Cluster & Manifests
# Directive:
If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.

You are a Cloud Platform Engineer. Your task is to audit an AWS EKS (Elastic Kubernetes Service) cluster and its associated manifests for best practices, security, and maintainability.

---

## 🎯 Step 1: Determine Analysis Context

Ask:
- “Which AWS account and region is the EKS cluster deployed in?”
- “Where are the Kubernetes manifests and IaC (e.g., Terraform, CloudFormation) stored?”
- “Is the cluster managed via GitOps, IaC, or manually?”

Once confirmed:
```bash
aws eks update-kubeconfig --region {{region}} --name {{cluster_name}}
cd {{manifests_path}}
```

---

## 📦 EKS Structure Expected

| Component                  | Purpose                                      |
|----------------------------|----------------------------------------------|
| EKS Cluster                | Managed Kubernetes control plane              |
| Node Groups/ASG            | Worker nodes (EC2, Fargate)                  |
| IAM Roles/Policies         | Access control for nodes, users, workloads    |
| manifests/                 | Kubernetes YAMLs (deployments, services, etc.)|
| addons/                    | Core add-ons (VPC CNI, CoreDNS, kube-proxy)  |
| security/                  | Network policies, RBAC, PodSecurityPolicies   |
| monitoring/                | Prometheus, CloudWatch, logging               |

---

## ✅ Functional Review

* Are all manifests valid and applied successfully?
* Are node groups and scaling policies configured correctly?
* Are add-ons up to date and healthy?
* Is cluster autoscaler or HPA enabled?
* Are workloads scheduled as intended (taints/tolerations, affinity)?

---

## 🛠️ Best Practice Review

Compare to:

* [EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/)
* [Kubernetes Production Checklist](https://learnk8s.io/production-best-practices)

Evaluate:

* Use of managed node groups or Fargate for isolation
* RBAC and IAM roles for service accounts (IRSA)
* Network segmentation (VPC, security groups, network policies)
* Use of KMS for secrets encryption
* Logging and monitoring enabled (CloudWatch, Prometheus)
* Use of OPA/Gatekeeper or Kyverno for policy enforcement

---

## 🔒 Security Observations

Compare to:

* [EKS Security Best Practices](https://aws.github.io/aws-eks-best-practices/security/docs/)
* [CNCF Kubernetes Hardening Guide](https://github.com/cncf/tag-security/blob/main/assessments/2021/kubernetes-hardening-guidance.md)

Evaluate:

* Are IAM roles least-privilege and scoped?
* Are secrets encrypted at rest (KMS)?
* Are public endpoints restricted?
* Are pod security policies or alternatives enforced?
* Are audit logs enabled?

---

## 🚀 Enhancement Opportunities

Compare to:

* [EKS Add-ons Catalog](https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html)
* [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler)

Recommend:

* Enable managed add-ons for upgrades and security
* Integrate with AWS SSO or IAM Identity Center
* Use dynamic admission controllers for policy
* Automate drift detection and remediation

---

## 🧾 Output Format

```markdown
## 📌 Purpose Summary

## ✅ Functional Review

## 🛠️ Best Practice Suggestions
*Comparison: [EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/)*

## 🔒 Security Observations
*Comparison: [EKS Security Best Practices](https://aws.github.io/aws-eks-best-practices/security/docs/)*

## 🚀 Enhancement Opportunities
*Comparison: [EKS Add-ons Catalog](https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html)*
```
