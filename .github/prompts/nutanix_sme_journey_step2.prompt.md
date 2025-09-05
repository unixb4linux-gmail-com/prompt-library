# Nutanix SME Journey Step 2: Operations & Automation

## Objective
Learn Prism Central, Nutanix Cloud Manager (NCM) Intelligent Ops, and basic automation with X-Play, Terraform, and Ansible.

---

## Instructions to AI
- Ask clarifying questions first (e.g., ops priorities, SLA requirements).  
- Wait for `continue`, `next`, or `proceed` before advancing.  
- Provide **UI steps first**, then mention Terraform/Ansible options.  

---

## Steps

### Step 1: Clarify Operations Goals
- Confirm whether the focus is on monitoring, automation, or both.  
- Ask about SLA or compliance expectations.

### Step 2: NCM Intelligent Ops
- Show how to enable dashboards, anomaly detection, and capacity planning.  
- Evidence: screenshot placeholders.

### Step 3: X-Play Runbook
- Create a simple runbook: “If VM CPU > 80% → Send alert.”  
- Evidence: runbook config snapshot.

### Step 4: Terraform & Ansible Intro
- Demonstrate Terraform Nutanix provider for reading cluster info.  
- Demonstrate Ansible collection (read-only play).  
- Evidence: Terraform plan/apply output.

---

## Exit Criteria
- User can navigate Prism Central dashboards.  
- One X-Play runbook created and tested.  
- Terraform and Ansible connectivity confirmed.

---

## Quiz
1. What is Prism Central primarily used for?  
   - a) Managing a single cluster  
   - b) Multi-cluster and SaaS-style management  
   - c) Replacing AHV  
2. What does X-Play enable?  
   - a) Hypervisor upgrades  
   - b) Event-driven automation  
   - c) Data backup  
3. Which tools integrate with Nutanix for IaC?  
   - a) Terraform and Ansible  
   - b) Puppet and Chef  
   - c) Jenkins only  

---

## Resources
- [Nutanix Cloud Manager Overview](https://www.nutanix.com/products/cloud-manager)  
- [Nutanix X-Play Automation](https://www.nutanix.com/blog/automation-with-x-play)  
- [Terraform Nutanix Provider](https://registry.terraform.io/providers/nutanix/nutanix/latest)  
- [Ansible Collection for Nutanix](https://galaxy.ansible.com/nutanix/ncp)  
