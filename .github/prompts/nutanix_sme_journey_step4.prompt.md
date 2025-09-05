# Nutanix SME Journey Step 4: NC2 & DR Patterns

## Objective
Deploy NC2 on Azure and learn disaster recovery (DR) patterns: Metro Availability, NearSync, Async, and Multicloud Snapshots.

---

## Instructions to AI
- Ask clarifying questions first (target workloads, RPO/RTO).  
- Only move forward on `continue`, `next`, or `proceed`.  
- Provide both conceptual and UI-based workflows.

---

## Steps

### Step 1: Clarify RPO/RTO
- Ask the user to map workloads into tiers (Tier 1, 2, 3).  
- Provide definitions with examples.

### Step 2: NC2 Setup in Azure
- Explain NC2 architecture and requirements.  
- Walk through deployment via Azure Marketplace.

### Step 3: NearSync for Tier-1
- Configure and simulate failover/failback.  
- Evidence: replication status screenshot.

### Step 4: Async for Tier-2
- Configure hourly replication.  
- Evidence: snapshot/replication logs.

### Step 5: Multicloud Snapshots
- Snapshot to Azure Blob storage.  
- Evidence: snapshot ID.

---

## Exit Criteria
- NC2 deployed on Azure.  
- At least one NearSync, Async, and MST policy tested.  
- RPO/RTO documented for each.

---

## Quiz
1. What does RPO measure?  
   - a) How much data can be lost  
   - b) How fast recovery happens  
   - c) The cost of DR  
2. Which method provides RPO=0?  
   - a) NearSync  
   - b) Metro Availability  
   - c) Async  
3. Which DR option leverages Azure Blob storage?  
   - a) NearSync  
   - b) Metro  
   - c) MST  

---

## Resources
- [Nutanix Cloud Clusters (NC2)](https://www.nutanix.com/products/cloud-clusters)  
- [Nutanix Metro Availability](https://portal.nutanix.com/page/documents/details?targetId=Web-Console-Guide-Prism-v6_0:wc-dr-metro-availability-wc-c.html)  
- [Nutanix Disaster Recovery](https://www.nutanix.com/solutions/disaster-recovery)  
