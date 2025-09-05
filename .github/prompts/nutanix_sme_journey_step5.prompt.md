# Nutanix SME Journey Step 5: Kubernetes with NKP

## Objective
Use Nutanix Kubernetes Platform (NKP) to manage AKS (and optionally EKS/minikube). Learn fleet management, GitOps, and upgrades.

---

## Instructions to AI
- Ask clarifying questions first (clusters, GitOps repo, policy goals).  
- Accept only `continue`, `next`, or `proceed`.  
- Provide UI workflows, generate CLI prompt for Claude if needed.

---

## Steps

### Step 1: Clarify Clusters
- Ask which AKS clusters to attach.  
- Confirm GitOps repo details.

### Step 2: Attach AKS Cluster
- Step-by-step attach process in NKP.  
- Evidence: cluster dashboard screenshot.

### Step 3: Observability
- Enable metrics/logging.  
- Evidence: metrics output.

### Step 4: Policy & Upgrade
- Create a sample upgrade policy.  
- Evidence: policy config screenshot.

### Step 5: GitOps Deployment
- Deploy a sample app via GitOps.  
- Evidence: deployment logs.

---

## Exit Criteria
- AKS cluster attached.  
- One policy applied.  
- GitOps app deployed.

---

## Quiz
1. What does NKP provide beyond AKS?  
   - a) Cluster autoscaling only  
   - b) Fleet management, policy, and GitOps  
   - c) Replacement of Azure Monitor  
2. Which GitOps tools integrate with NKP?  
   - a) ArgoCD, Flux  
   - b) Jenkins only  
   - c) Chef and Puppet  
3. Which step validates cluster observability?  
   - a) Metrics and logging enabled  
   - b) Creating a VM  
   - c) Attaching storage  

---

## Resources
- [Nutanix Kubernetes Platform (NKP)](https://www.nutanix.com/products/kubernetes-platform)  
- [ArgoCD GitOps](https://argo-cd.readthedocs.io/)  
- [Flux GitOps](https://fluxcd.io/)  
