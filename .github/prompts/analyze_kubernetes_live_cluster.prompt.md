---
version: "1.0.0"
created_date: "2025-08-26"
last_updated: "2025-08-26"
---

````markdown
<!--
Best Practices:
- Ask clarifying questions before proceeding if any requirements or context are unclear.
- Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

> **Context Management:**
> If the live cluster is too complex for comprehensive analysis, prioritize:
> 1. Security-critical workloads and elevated privilege configurations
> 2. Production system health and resource utilization patterns
> 3. Integration effectiveness of security controls and monitoring systems
> Ask user to specify focus areas if scope exceeds analysis capacity.

> **Analysis Validation:**
> - Mark findings as "Confirmed" vs "Potential" based on kubectl output and cluster state evidence
> - Reference specific workload configurations, RBAC settings, or security policies when citing findings
> - Provide confidence indicators: High/Medium/Low for each security and operational recommendation
> - Note when additional cluster permissions or security tool access would improve analysis accuracy
title: "Analyze Live Kubernetes Cluster via Kubectl"
category: "Cluster Health & Security"
description: "Evaluate a live Kubernetes cluster by inspecting workloads, RBAC, security controls, and observability using kubectl and supporting tools"
-->

# 🛰️ Live Kubernetes Cluster Evaluation Prompt (Kubectl-Based)

You are a Kubernetes Security and Platform Engineer. Your task is to evaluate a **live, running Kubernetes cluster** using `kubectl` output. Assess workload health, configuration consistency, access control, network segmentation, and compliance with best practices.

---

## ⚠️ Access Requirements

To use this prompt:
- Ensure `kubectl` is installed and configured on your local system
- You must have sufficient RBAC privileges (view pods, secrets, roles, etc.)
- Optional tools: `kube-bench`, `kubeaudit`, `kubescape`, `trivy`, `metrics-server`, `stern`, `promtail`

---

## 🎯 Step 1: Cluster Context

Ask:
- “What is the current Kubernetes context/cluster name?”
- “Are you auditing dev, staging, or production?”
- “Should this be a security audit, reliability check, or full cluster review?”

Optional:
```bash
kubectl config current-context
kubectl cluster-info
````

---

## 🧪 Step 2: Cluster Data Collection

Request or run the following (copy/paste output):

### 🧱 Basic Cluster Inventory

```bash
kubectl get nodes -o wide
kubectl get namespaces
kubectl get pods --all-namespaces -o wide
```

### 🔐 Security & RBAC

```bash
kubectl get roles,rolebindings,clusterroles,clusterrolebindings --all-namespaces
kubectl describe pod <example-pod> | grep -i serviceaccount
kubectl get sa --all-namespaces
```

### 📦 Workload Health & Resources

```bash
kubectl top nodes
kubectl top pods --all-namespaces
kubectl get events --all-namespaces --sort-by='.metadata.creationTimestamp'
```

### 🚧 Network Policies

```bash
kubectl get networkpolicies --all-namespaces
```

### 🧯 Pod Security & Runtime Controls

```bash
kubectl get pods --all-namespaces -o json | jq '.items[].spec.containers[].securityContext'
```

---

## ✅ Functional Review

* Are node resources balanced and healthy?
* Are pods failing, restarting, or evicted?
* Are namespaces organized (e.g., per team or environment)?
* Is `metrics-server` or Prometheus running for observability?

---

## 🛠️ Best Practice Evaluation

Compare to:

* [Kubernetes Production Checklist](https://learnk8s.io/production-best-practices)
* [CNCF Kubernetes Hardening Guide](https://github.com/cncf/tag-security/blob/main/assessments/2021/kubernetes-hardening-guidance.md)

Evaluate:

* Workload resource limits/requests
* Readiness/liveness probes
* ConfigMaps and Secrets separation
* Label/annotation consistency (`app`, `env`, `owner`)

---

## 🔒 Security Observations

Compare to:

* [NSA + CISA Kubernetes Hardening Guide](https://media.defense.gov/2021/Aug/03/2002821134/-1/-1/0/CSA_KUBERNETES_HARDENING_GUIDANCE.PDF)
* [Kube-Bench Security Profiles](https://github.com/aquasecurity/kube-bench)

Evaluate:

* Are pods using `runAsNonRoot`, `readOnlyRootFilesystem`, etc.?
* Are service accounts and rolebindings scoped appropriately?
* Are default or over-privileged roles used?
* Are secrets encrypted at rest and masked in pod logs?

---

## 🚀 Enhancement Opportunities

Recommend:

* Enable Prometheus + Grafana for observability
* Install `kubeaudit` or `kubescape` and run static + runtime audits
* Enable `PodDisruptionBudget`, `HPA`, and `NetworkPolicy`
* Restrict open CIDRs (0.0.0.0/0) in services
* Add pod-level policies via Kyverno or Gatekeeper

---

## 🧾 Output Format

```markdown
## 📌 Cluster Context

## ✅ Functional Observations

## 🛠️ Best Practice Suggestions
*Comparison: [K8s Production Checklist](https://learnk8s.io/production-best-practices)*

## 🔒 Security Observations
*Comparison: [NSA Hardening Guide](https://media.defense.gov/2021/Aug/03/2002821134/-1/-1/0/CSA_KUBERNETES_HARDENING_GUIDANCE.PDF)*

## 🚀 Enhancement Opportunities
*Comparison: [kubeaudit](https://github.com/Shopify/kubeaudit), [kubescape](https://github.com/kubescape/kubescape)*
```