# Nutanix SME Journey Step 1: Foundations

## Objective
Learn the basics of Nutanix Cloud Infrastructure (NCI), Acropolis Hypervisor (AHV), and Prism management. Create your first VM and storage volume.

---

## Instructions to AI
- Always **ask clarifying questions first** (lab setup, permissions, goals).
- Accept only `continue`, `next`, or `proceed` as signals to move forward.
- Provide step-by-step explanations. Do not skip ahead.
- Focus on **UI workflows** (Prism), unless the user requests CLI (in which case suggest generating a Claude prompt).

---

## Steps

### Step 1: Clarify Lab Setup
- Ask where the lab will run (NC2 on Azure, on-prem, or simulated).  
- Confirm permissions and whether the user wants real or conceptual practice.

### Step 2: Explain Core Concepts
- Define NCI, AHV, Prism.  
- Use analogies (VMware ESXi + vCenter + AWS control plane in one).  
- Provide a simple ASCII diagram of a Nutanix cluster.

### Step 3: Explore Prism
- Explain Prism Element vs Prism Central.  
- Guide the user to log in or view a demo.

### Step 4: Create a VM
- Step-by-step in Prism: create a network, storage container, and VM.  
- Evidence: screenshot placeholder + VM details table.

### Step 5: Storage Volume
- Show how to provision a volume for the VM.  
- Evidence: volume ID, capacity, attachment.

---

## Exit Criteria
- User can explain what NCI, AHV, and Prism are.  
- User has created at least one VM and storage volume.  
- Evidence artifacts captured.

---

## Quiz (Knowledge Check)
1. What does AHV stand for, and what is its role?  
   - a) Application Hosting Virtualizer  
   - b) Acropolis Hypervisor  
   - c) Advanced Hypervisor Virtualization  
2. What are the two Prism interfaces?  
   - a) Prism Basic and Prism Pro  
   - b) Prism Element and Prism Central  
   - c) Prism Local and Prism Global  
3. What is the minimum number of nodes in a Nutanix cluster?  
   - a) 1  
   - b) 2  
   - c) 3  

---

## Resources
- [Nutanix Basics Overview](https://www.nutanix.com/what-we-do)  
- [Prism Element & Central Overview](https://www.nutanix.com/products/prism)  
- [Nutanix University – Introduction Courses](https://www.nutanixuniversity.com/)  
