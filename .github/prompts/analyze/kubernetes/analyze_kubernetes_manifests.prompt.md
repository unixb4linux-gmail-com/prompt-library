
````markdown
<!--
title: "Analyze Kubernetes Manifests and Deployment"
category: "Kubernetes Audit"
description: "Audit Kubernetes YAML, RBAC, config, security, and deployment patterns"
-->

# ☸️ Comprehensive Kubernetes Configuration Audit

You are a Senior Cloud Infrastructure Engineer. Your task is to audit the Kubernetes manifests and deployment configurations in this repository. Evaluate their correctness, modularity, security, and alignment with best practices. Provide remediation advice where needed.

---

## 🎯 Step 1: Determine Analysis Context

Ask:
- “Which directory or branch contains the Kubernetes manifests?”
- “Are these used for development, staging, or production?”
- “Are these applied directly or managed via GitOps (e.g., ArgoCD, Flux)?”

Once confirmed:
```bash
git checkout {{branch_name}} && git pull
cd {{manifests_path}}
````

---

## 📦 Common Kubernetes Use Cases to Review

| Category       | Resources Expected                                                      |
| -------------- | ----------------------------------------------------------------------- |
| **Deployment** | `Deployment`, `StatefulSet`, `DaemonSet`, `CronJob`, `Job`              |
| **Networking** | `Service`, `Ingress`, `NetworkPolicy`, `EndpointSlice`                  |
| **Security**   | `Role`, `RoleBinding`, `ServiceAccount`, `PodSecurityPolicy`, `Secrets` |
| **Config**     | `ConfigMap`, `Secret`, `PersistentVolumeClaim`, `ResourceQuota`         |
| **Operations** | `HorizontalPodAutoscaler`, `PodDisruptionBudget`, `ReadinessProbes`     |

---

## ✅ Functional Review

* Are all manifests syntactically valid (`kubectl apply -f` or `kubeval`)?
* Are readiness/liveness probes configured?
* Are resource requests/limits set?
* Are labels/annotations consistent and scoped by environment?
* Is namespace scoping correct?

---

## 🛠️ Best Practice Evaluation

Compare to:

* [Kubernetes Production Checklist (learnk8s)](https://learnk8s.io/production-best-practices)
* [Kubernetes Official Best Practices](https://kubernetes.io/docs/concepts/)

Evaluate:

* Use of `readinessProbe` and `livenessProbe`
* Deployment strategy: `rollingUpdate`, `recreate`, or `blueGreen`
* Clear separation of environments (dev, staging, prod)
* Volume and PVC usage for persistent workloads
* Horizontal scaling (`replicas`, `HPA`) and availability
* Clear owner labels and traceability metadata

---

## 🔒 Security Observations

Compare to:

* [CNCF Kubernetes Hardening Guide](https://github.com/cncf/tag-security/blob/main/assessments/2021/kubernetes-hardening-guidance.md)
* [NSA & CISA Kubernetes Security Guide](https://media.defense.gov/2021/Aug/03/2002821134/-1/-1/0/CSA_KUBERNETES_HARDENING_GUIDANCE.PDF)

Evaluate:

* Are `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation` set?
* Are secrets mounted from `Secret` objects vs. inline?
* Is `imagePullPolicy: Always` used for latest-tagged containers?
* Use of `ServiceAccount`, `RoleBinding`, and `RBAC` scoping
* Are secrets encrypted at rest and rotated?
* Use of `NetworkPolicy` to restrict inter-pod communication

---

## 🛡️ Policy Enforcement & Validation

Compare to:

* [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/)
* [Kyverno Policy Library](https://kyverno.io/policies/)

Evaluate:

* Are validation rules used for structure and enforcement?
* Are image registries restricted?
* Are privileged pods disallowed by policy?
* Any policies for tagging, owner labels, or traceability?

---

## 🚀 Enhancement Opportunities

Compare to:

* [Kubernetes GitOps Patterns (CNCF)](https://www.cncf.io/blog/2021/04/20/gitops-operations-for-kubernetes/)
* [Production Helm Practices](https://docs.bitnami.com/tutorials/best-practices-using-helm/)

Recommend:

* Modularize environment-specific values via overlays or Helm
* Introduce `Kustomize`, `Helm`, or `Jsonnet` if YAMLs are too repetitive
* Add `HPA` or `KEDA` for dynamic scaling
* Add `PodDisruptionBudget` for HA workloads
* Enhance observability with logging sidecars or tracing agents

---

## 🧾 Output Format

```markdown
## 📌 Purpose Summary

## ✅ Functional Review

## 🛠️ Best Practice Suggestions
*Comparison: [Kubernetes Production Checklist](https://learnk8s.io/production-best-practices)*

## 🔒 Security Observations
*Comparison: [CNCF Kubernetes Hardening Guide](https://github.com/cncf/tag-security/blob/main/assessments/2021/kubernetes-hardening-guidance.md)*

## 🛡️ Policy Enforcement
*Comparison: [Kyverno Policy Library](https://kyverno.io/policies/)*

## 🚀 Enhancement Opportunities
*Comparison: [GitOps for Kubernetes](https://www.cncf.io/blog/2021/04/20/gitops-operations-for-kubernetes/)*
```
