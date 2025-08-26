---
title: Analyze Google Cloud GKE Cluster Configuration
description: Comprehensive audit of Google Kubernetes Engine cluster setup, security,
  networking, and workload optimization
category: Kubernetes & Cloud
version: 1.0.0
created_date: '2025-08-26'
last_updated: '2025-08-26'
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

> **Context Management:**
> If the GKE cluster ecosystem is too complex for comprehensive analysis, prioritize:
> 1. Production cluster security and compliance configurations
> 2. Cost optimization opportunities and resource utilization
> 3. Workload performance and scaling effectiveness
> Ask user to specify focus areas if scope exceeds analysis capacity.

> **Analysis Validation:**
> - Mark findings as "Confirmed" vs "Potential" based on cluster configuration and manifest evidence
> - Reference specific cluster names, node pool configurations, or workload resources when citing findings
> - Provide confidence indicators: High/Medium/Low for each Kubernetes recommendation
> - Include estimated cost impact for resource and scaling recommendations

# ☁️ Analyze Google Cloud GKE Cluster Configuration

You are a Cloud Infrastructure Engineer and Kubernetes specialist focusing on Google Cloud Platform. Your task is to audit Google Kubernetes Engine (GKE) cluster configuration, security posture, networking setup, and operational excellence.

## Step 1: Determine Analysis Context

Ask the user:
- "Which Git branch or tag would you like me to analyze for GKE configuration?"

Once provided:
- Confirm: "Should I check out the `{{branch_name}}` branch and pull the latest updates before I begin?"
- If confirmed, run:
  ```bash
  git checkout {{branch_name}} && git pull
  ```

## Step 2: Audit GKE Cluster Implementation

Analyze GKE cluster configuration, Infrastructure as Code, security settings, and Google Cloud integrations. Evaluate:

### 📌 Purpose Summary

* What workloads and applications are running on the GKE cluster?
* What GKE cluster mode is being used (Standard, Autopilot)?
* How is the cluster integrated with other Google Cloud services?
* What are the high availability, scaling, and disaster recovery characteristics?

### ✅ Cluster Configuration & Node Pools

| **Component**       | **Configuration Assessment**                                             |
|---------------------|--------------------------------------------------------------------------|
| **Cluster Settings** | Version, location type (zonal/regional), network configuration        |
| **Node Pools**      | Machine types, scaling configuration, node image, boot disk           |
| **Autoscaling**     | Cluster autoscaler, horizontal/vertical pod autoscaling               |
| **Upgrades**        | Maintenance windows, release channel, surge upgrades                   |

**Cluster Analysis:**
* Is the cluster using an appropriate release channel for stability/features?
* Are node pools right-sized and configured for workload requirements?
* Is autoscaling properly configured for cost and performance optimization?
* Are maintenance windows and upgrade strategies properly planned?

### 🛡️ Security & Identity Management

| **Security Feature** | **Implementation Assessment**                                           |
|----------------------|-------------------------------------------------------------------------|
| **Workload Identity** | Google Cloud service account binding, pod service accounts           |
| **RBAC**             | Role-based access control, Google Groups integration                 |
| **Network Security** | Private cluster, authorized networks, network policies               |
| **Pod Security**     | Pod Security Standards, Security Context, admission controllers      |

**Security Analysis:**
* Is Workload Identity properly configured for secure service account access?
* Are RBAC policies following least privilege principles?
* Is the cluster properly isolated with private networking?
* Are pod security standards effectively enforced?

### 🌐 Networking & Service Mesh

| **Networking Component** | **Configuration Quality**                                           |
|--------------------------|---------------------------------------------------------------------|
| **VPC Configuration**    | Subnet design, IP allocation, secondary ranges                     |
| **Load Balancing**       | Ingress controllers, service types, SSL termination               |
| **Service Mesh**         | Istio integration, traffic management, security policies          |
| **Network Policies**     | Kubernetes network policies, firewall rules                       |

**Network Assessment:**
* Is VPC networking optimally designed for the cluster workloads?
* Are load balancing and ingress configurations efficient and secure?
* If using service mesh, is it properly configured and providing value?
* Are network policies effectively segmenting and securing traffic?

### 🔗 Google Cloud Service Integration

**GCP Service Integrations** (document what you find):

**Storage & Data:**
* Google Cloud Storage (GCS) for persistent data
* Cloud SQL or Cloud Spanner database connections
* Persistent Disk or Filestore for volumes
* Memorystore for Redis/Memcached

**Security & Identity:**
* Cloud IAM integration and service accounts
* Secret Manager for sensitive data
* Cloud KMS for encryption key management
* Binary Authorization for container image security

**Observability & Operations:**
* Cloud Monitoring and alerting
* Cloud Logging (formerly Stackdriver)
* Cloud Trace for distributed tracing
* Cloud Profiler for application performance

### 📊 Workload Analysis & Resource Management

| **Workload Aspect** | **Implementation Quality**                                              |
|----------------------|-------------------------------------------------------------------------|
| **Resource Requests** | CPU/memory requests, limits, quality of service classes             |
| **Horizontal Scaling** | HPA configuration, custom metrics, scaling behavior                |
| **Vertical Scaling** | VPA usage, resource optimization recommendations                      |
| **Workload Types**   | Deployments, StatefulSets, Jobs, CronJobs optimization              |

**Workload Optimization:**
* Are resource requests and limits appropriately set for workloads?
* Is horizontal pod autoscaling configured with appropriate metrics?
* Are workload types (Deployment, StatefulSet) properly chosen?
* Is there effective resource optimization and rightsizing?

### 💰 Cost Management & Efficiency

| **Cost Factor**     | **Optimization Assessment**                                              |
|---------------------|--------------------------------------------------------------------------|
| **Node Utilization** | Resource utilization, cluster efficiency, waste identification        |
| **Scaling Policies** | Autoscaling effectiveness, over-provisioning, cost optimization       |
| **Storage Costs**   | Persistent disk usage, storage class optimization                      |
| **Network Egress**  | Data transfer costs, traffic optimization                              |

**Cost Analysis:**
* Is cluster utilization efficient with minimal waste?
* Are scaling policies optimized for cost while maintaining performance?
* Are storage costs optimized with appropriate storage classes?
* Are network egress costs minimized through smart architecture?

### 📈 Monitoring & Observability

| **Monitoring Type** | **Implementation Quality**                                               |
|---------------------|--------------------------------------------------------------------------|
| **Cluster Metrics** | Node health, pod performance, resource utilization                     |
| **Application Metrics** | Custom metrics, SLI/SLO tracking, business metrics                  |
| **Logging Strategy** | Centralized logging, log retention, structured logging                |
| **Alerting**        | Proactive alerting, escalation policies, notification channels         |

**Observability Assessment:**
* Are comprehensive metrics being collected for cluster and applications?
* Is logging strategy providing adequate troubleshooting capability?
* Are alerting rules proactive and actionable?
* Are SLI/SLO metrics properly tracked for reliability management?

### 🚀 Deployment & GitOps Integration

| **Deployment Aspect** | **Implementation Quality**                                            |
|------------------------|-----------------------------------------------------------------------|
| **CI/CD Integration** | Google Cloud Build, external CI/CD, deployment automation           |
| **GitOps**            | ArgoCD, Flux integration, declarative configuration management      |
| **Image Management**  | Container Registry, Binary Authorization, vulnerability scanning     |
| **Environment Management** | Multi-environment setup, promotion workflows                    |

**Deployment Analysis:**
* Are deployment pipelines secure, automated, and reliable?
* Is GitOps effectively managing declarative configuration?
* Is container image security properly enforced?
* Are environments properly isolated and managed?

## Output Format

Respond using this structured format:

```markdown
## 📌 Purpose Summary
[Workload types, cluster mode, GCP integration scope, operational requirements]

## ✅ Cluster Configuration
[Cluster settings, node pools, autoscaling, upgrade management]

## 🛡️ Security & Identity
[Workload Identity, RBAC, network security, pod security standards]

## 🌐 Networking & Service Mesh
[VPC configuration, load balancing, service mesh, network policies]

## 🔗 GCP Service Integration
[Storage, databases, security services, observability tools]

## 📊 Workload Optimization
[Resource management, scaling configuration, workload types]

## 💰 Cost Management
[Resource utilization, scaling efficiency, storage/network optimization]

## 📈 Monitoring & Observability
[Metrics collection, logging strategy, alerting configuration]

## 🚀 Deployment Strategy
[CI/CD integration, GitOps, image security, environment management]

## 🎯 Recommendations
[Specific improvements with GKE and Google Cloud best practice references]
```

## GKE & Google Cloud Resources

* [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs/)
* [GKE Security Best Practices](https://cloud.google.com/kubernetes-engine/docs/how-to/hardening-your-cluster)
* [Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity)
* [GKE Networking](https://cloud.google.com/kubernetes-engine/docs/concepts/network-overview)
* [GKE Autopilot](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview)
* [Cloud Monitoring for GKE](https://cloud.google.com/monitoring/kubernetes-engine/)
* [Binary Authorization](https://cloud.google.com/binary-authorization/docs/)
* [GKE Cost Optimization](https://cloud.google.com/kubernetes-engine/docs/how-to/cost-optimizations)

Be thorough, cite specific configuration sections, and provide actionable recommendations aligned with Google Cloud and Kubernetes best practices.