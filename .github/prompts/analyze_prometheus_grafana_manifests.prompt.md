---
version: "1.0.0"
created_date: "2025-08-26"
last_updated: "2025-08-26"
---

# 📈 Prometheus + Grafana Observability Manifest Audit
> **Ask clarifying questions before proceeding.**
> **Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.**
> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
````markdown
<!--
title: "Analyze Prometheus and Grafana Manifests"
category: "Observability"
description: "Audit manifests and configurations for Prometheus, Grafana, and alerting components"
-->

# 📈 Prometheus + Grafana Observability Manifest Audit

You are a Kubernetes Observability Engineer. Your task is to analyze Prometheus and Grafana manifests within this repository. Assess how metrics, dashboards, alerts, and configuration files are defined and deployed. Ensure observability is set up securely, modularly, and with scalability in mind.

---

## 🎯 Step 1: Determine Analysis Context

Ask:
- “Where are the Prometheus and Grafana manifests located?”
- “Are you using kube-prometheus-stack, Prometheus Operator, or custom deployments?”
- “Is this for dev, staging, production, or all?”

Once confirmed:
```bash
git checkout {{branch_name}} && git pull
cd {{observability_path}}
````

---

## 📦 Expected Resources to Review

| Component      | Resources                                                                 |
| -------------- | ------------------------------------------------------------------------- |
| Prometheus     | `Deployment`, `ServiceMonitor`, `Prometheus`, `ConfigMap`, `Rules`        |
| Grafana        | `Deployment`, `ConfigMap`, `Dashboard`, `Datasource`, `Secret`            |
| Alertmanager   | `Alertmanager`, `Secret`, `Route`, `Receiver`                             |
| Optional Tools | `node-exporter`, `kube-state-metrics`, `blackbox-exporter`, `Pushgateway` |

---

## ✅ Functional Review

* Are all manifests syntactically valid?
* Does Prometheus scrape the correct targets (via `ServiceMonitor`, `PodMonitor`, or static configs)?
* Are alert rules present and complete?
* Are Grafana dashboards defined or provisioned?
* Are services exposed securely and port-forwardable?

---

## 🛠️ Best Practice Review

Compare to:

* [Prometheus Best Practices](https://prometheus.io/docs/practices/)
* [Grafana Provisioning Guide](https://grafana.com/docs/grafana/latest/administration/provisioning/)
* [kube-prometheus-stack Helm Guide](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)

Evaluate:

* Use of `ServiceMonitor` or `PodMonitor` over static config
* Use of relabeling to clean target names
* Alert thresholds use dynamic scaling values (e.g., % CPU, not fixed)
* Dashboards are provisioned from `ConfigMap` or sidecar
* Datasource config is secure, version-pinned, and environment-aware

---

## 🔒 Security Observations

Compare to:

* [Grafana Security Best Practices](https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/)
* [Prometheus Hardening](https://prometheus.io/docs/operating/security/)

Evaluate:

* Are Prometheus and Grafana exposed via `Ingress` or `LoadBalancer`?
* Is access to Grafana secured via Auth Proxy, OAuth, or Secrets?
* Are dashboards/configs readable only to limited RBAC roles?
* Are tokens, API keys, or credentials kept in Kubernetes Secrets?
* Are Prometheus scrape targets filtered to avoid overexposure?

---

## 🚀 Enhancement Opportunities

Compare to:

* [Observability Maturity Model](https://thenewstack.io/the-observability-maturity-model/)
* [Prometheus Exporter Library](https://prometheus.io/docs/instrumenting/exporters/)

Recommend:

* Use of Grafana dashboards-as-code (`ConfigMap` or `Grafonnet`)
* Introduce `kube-state-metrics`, `blackbox-exporter`, `node-exporter`
* Use `Alertmanager` for routing + escalation policies (e.g., Slack, PagerDuty)
* Add annotations to pods for `prometheus.io/scrape: true` if needed
* Add uptime/duration metrics for health reporting

---

## 🧾 Output Format

```markdown
## 📌 Purpose Summary

## ✅ Functional Review

## 🛠️ Best Practice Suggestions
*Comparison: [Prometheus Practices](https://prometheus.io/docs/practices/), [Grafana Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)*

## 🔒 Security Observations
*Comparison: [Prometheus Hardening](https://prometheus.io/docs/operating/security/)*

## 🚀 Enhancement Opportunities
*Comparison: [Observability Maturity Model](https://thenewstack.io/the-observability-maturity-model/)*
```