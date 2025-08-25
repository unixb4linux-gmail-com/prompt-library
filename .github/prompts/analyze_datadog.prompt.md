---
title: "Analyze Datadog Observability Configuration"
description: "Comprehensive audit of Datadog monitoring, dashboards, alerts, APM, and infrastructure observability setup"
category: "Observability"
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

# 📊 Analyze Datadog Observability Configuration

You are an SRE and Observability Engineer specializing in Datadog. Your task is to audit this repository's Datadog configuration, monitoring setup, alerting strategy, and integration with the application stack.

## Step 1: Determine Analysis Context

Ask the user:
- "Which Git branch or tag would you like me to analyze for Datadog configuration?"

Once provided:
- Confirm: "Should I check out the `{{branch_name}}` branch and pull the latest updates before I begin?"
- If confirmed, run:
  ```bash
  git checkout {{branch_name}} && git pull
  ```

## Step 2: Audit Datadog Configuration

Analyze Datadog configuration files, dashboards, monitors, and integration setup. Evaluate:

### 📌 Purpose Summary

* What observability goals does the Datadog implementation serve?
* Which Datadog products are in use (Infrastructure, APM, Logs, Synthetics, RUM)?
* How comprehensive is the monitoring coverage across the application stack?
* What are the primary use cases (performance monitoring, debugging, alerting)?

### ✅ Infrastructure & Configuration Review

| **Component**       | **Datadog Configuration**                                               |
|---------------------|--------------------------------------------------------------------------|
| **Agent Config**    | `datadog.yaml`, agent installation, host configuration                 |
| **Integrations**    | Database, web server, container, cloud provider integrations          |
| **Tags**            | Tagging strategy, environment tags, service tags                       |
| **Collection**      | Metrics, logs, traces, custom metrics collection                       |

**Configuration Analysis:**
* Is the Datadog Agent properly configured with appropriate permissions?
* Are integrations enabled for all relevant infrastructure components?
* Is the tagging strategy consistent and comprehensive?
* Are custom metrics being collected effectively?

### 🔍 Application Performance Monitoring (APM)

| **APM Component**   | **Implementation Assessment**                                            |
|---------------------|--------------------------------------------------------------------------|
| **Instrumentation** | Auto vs. manual instrumentation, language-specific setup              |
| **Services**        | Service mapping, dependency tracking, distributed tracing             |
| **Profiling**       | Code profiling, resource usage analysis                               |
| **Error Tracking** | Exception tracking, error rate monitoring                              |

**APM Effectiveness:**
* Are all critical services properly instrumented?
* Is distributed tracing capturing complete request flows?
* Are error rates and performance metrics comprehensive?
* Is profiling enabled for performance optimization?

### 📊 Dashboards & Visualization

| **Dashboard Type**  | **Content & Organization**                                               |
|---------------------|--------------------------------------------------------------------------|
| **Infrastructure** | Host metrics, container metrics, cloud resource monitoring             |
| **Application**     | Service performance, business metrics, user experience                |
| **Custom**          | Team-specific dashboards, troubleshooting views                       |
| **SLI/SLO**         | Service level indicators, reliability tracking                        |

**Dashboard Quality:**
* Are dashboards logically organized and easy to navigate?
* Do dashboards provide actionable insights?
* Are SLI/SLO dashboards aligned with business objectives?
* Is there proper dashboard access control and sharing?

### 🚨 Alerting & Incident Management

| **Alert Category**  | **Configuration & Strategy**                                             |
|---------------------|--------------------------------------------------------------------------|
| **Infrastructure** | Host down, high CPU, memory usage, disk space alerts                   |
| **Application**     | Error rates, response times, throughput anomalies                     |
| **Business**        | Custom metrics, conversion rates, user experience                      |
| **Synthetic**       | API endpoints, website availability, performance                       |

**Alerting Assessment:**
* Are alert thresholds appropriate and well-tuned?
* Is there proper alert escalation and notification routing?
* Are alerts actionable and include relevant context?
* Is alert fatigue being managed effectively?

### 🔗 Integration Assessment

**Discovered Integrations** (document what you find):

**Cloud Providers:**
* AWS (CloudWatch, ECS, EKS, Lambda integration)
* Azure (Monitor integration, App Service, AKS)
* GCP (Cloud Monitoring, GKE, Cloud Functions)

**Infrastructure & Orchestration:**
* Kubernetes (cluster monitoring, pod metrics)
* Docker containers and registries
* Load balancers and CDNs
* Databases (PostgreSQL, MySQL, MongoDB, etc.)

**CI/CD & Development:**
* GitHub/GitLab integration for deployment tracking
* Slack/PagerDuty for incident response
* JIRA for issue tracking and correlation

### 📝 Log Management & Analysis

| **Log Component**   | **Implementation Quality**                                               |
|---------------------|--------------------------------------------------------------------------|
| **Collection**      | Log aggregation, structured logging, retention policies               |
| **Parsing**         | Log parsing rules, custom parsers, field extraction                   |
| **Analysis**        | Log analytics, pattern detection, anomaly detection                   |
| **Integration**     | APM trace correlation, infrastructure correlation                      |

**Log Management Effectiveness:**
* Are logs being collected from all critical components?
* Is structured logging implemented consistently?
* Are logs properly correlated with traces and metrics?
* Is log retention aligned with compliance requirements?

### 🎯 Synthetic Monitoring & RUM

| **Monitoring Type** | **Coverage & Configuration**                                             |
|---------------------|--------------------------------------------------------------------------|
| **API Monitoring**  | Critical endpoint testing, multi-location checks                      |
| **Browser Tests**   | User journey testing, performance monitoring                           |
| **RUM**             | Real user monitoring, performance insights                             |
| **Mobile**          | Mobile app performance, crash reporting                               |

**Synthetic & RUM Analysis:**
* Are critical user journeys covered by synthetic tests?
* Is RUM providing comprehensive user experience insights?
* Are performance budgets and SLA monitoring in place?
* Is mobile monitoring comprehensive if applicable?

## Output Format

Respond using this structured format:

```markdown
## 📌 Purpose Summary
[Observability goals, Datadog products in use, monitoring scope]

## ✅ Infrastructure & Configuration
[Agent setup, integrations, tagging, metrics collection]

## 🔍 APM & Distributed Tracing
[Instrumentation quality, service mapping, error tracking]

## 📊 Dashboards & Visualization
[Dashboard organization, SLI/SLO tracking, visualization quality]

## 🚨 Alerting Strategy
[Alert configuration, thresholds, escalation, incident management]

## 🔗 Integration Findings
[Cloud providers, infrastructure, CI/CD, third-party tool integration]

## 📝 Log Management
[Log collection, parsing, analysis, correlation with APM]

## 🎯 Synthetic & RUM Monitoring
[API monitoring, browser tests, user experience tracking]

## 🎯 Recommendations
[Specific improvements with Datadog best practice links]
```

## Datadog Resources & References

* [Datadog Documentation](https://docs.datadoghq.com/)
* [Agent Configuration](https://docs.datadoghq.com/agent/guide/agent-configuration-files/)
* [APM Setup Guide](https://docs.datadoghq.com/tracing/setup/)
* [Dashboard Best Practices](https://docs.datadoghq.com/dashboards/guide/best-practices/)
* [Alerting Best Practices](https://docs.datadoghq.com/monitors/guide/best-practices/)
* [Log Management Guide](https://docs.datadoghq.com/logs/guide/)
* [Synthetic Monitoring](https://docs.datadoghq.com/synthetics/)
* [RUM Implementation](https://docs.datadoghq.com/real_user_monitoring/)

Be thorough, cite specific configuration sections, and provide actionable recommendations aligned with observability best practices and SRE principles.