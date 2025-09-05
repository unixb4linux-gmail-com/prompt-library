# Nutanix SME Journey Step 3: Storage & Security

## Objective
Learn Nutanix storage services (Files, Objects, Volumes) and Data Lens for ransomware detection and compliance monitoring.

---

## Instructions to AI
- Ask clarifying questions first (data types, compliance needs).  
- Proceed only with `continue`, `next`, or `proceed`.  
- Use UI workflows (Prism) where possible.

---

## Steps

### Step 1: Clarify Data Classes
- Ask: Which types of data (VM shares, backups, app logs) matter most?  
- Map to Files, Objects, or Volumes.

### Step 2: Deploy Nutanix Files
- Guide through creating an SMB/NFS share.  
- Evidence: share name, capacity, access list.

### Step 3: Deploy Nutanix Objects
- Create an S3-compatible bucket.  
- Evidence: bucket endpoint and keys.

### Step 4: Volumes
- Provision an iSCSI volume and attach to a VM.  
- Evidence: volume attachment details.

### Step 5: Enable Data Lens
- Activate ransomware detection.  
- Run a simulated anomalous activity test.  
- Evidence: alert screenshot placeholder.

---

## Exit Criteria
- At least one File, Object, and Volume deployed.  
- Data Lens shows at least one detection event.

---

## Quiz
1. Which Nutanix service provides S3-compatible storage?  
   - a) Files  
   - b) Objects  
   - c) Volumes  
2. What does Data Lens help protect against?  
   - a) CPU spikes  
   - b) Ransomware and risky permissions  
   - c) Hypervisor crashes  
3. Which storage type is best for attaching directly to VMs?  
   - a) Files  
   - b) Objects  
   - c) Volumes  

---

## Resources
- [Nutanix Unified Storage](https://www.nutanix.com/products/unified-storage)  
- [Nutanix Data Lens](https://www.nutanix.com/solutions/data-governance)  
- [StorageReview: Nutanix Data Lens](https://www.storagereview.com/review/nutanix-data-lens-overview)  
