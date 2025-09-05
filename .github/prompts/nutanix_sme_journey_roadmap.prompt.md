# Nutanix SME Journey – 6 Week Roadmap

## Week 1: Foundations (NCI, AHV, Prism)
🎯 Objectives: Understand Nutanix core building blocks. Create first VM & storage volume.  
🛠 Lab: Deploy NC2 trial or simulator, log into Prism, create a VM and storage container.  
📚 Resources:  
- [Nutanix Basics](https://www.nutanix.com/what-we-do)  
- [Prism Overview](https://www.nutanix.com/products/prism)  
✅ Exit: VM + volume created, can explain NCI/AHV/Prism.  

## Week 2: Operations & Automation (NCM, X-Play, Terraform/Ansible)
🎯 Objectives: Learn Prism Central, NCM Intelligent Ops, automation basics.  
🛠 Lab: Enable Prism Central, create an X-Play runbook, run Terraform provider read.  
📚 Resources:  
- [NCM Overview](https://www.nutanix.com/products/cloud-manager)  
- [Terraform Nutanix Provider](https://registry.terraform.io/providers/nutanix/nutanix/latest)  
✅ Exit: Dashboard navigation, runbook created, Terraform/Ansible tested.  

## Week 3: Storage & Security (Files, Objects, Volumes, Data Lens)
🎯 Objectives: Understand storage options and security.  
🛠 Lab: Create File share, Object bucket, iSCSI volume, enable Data Lens.  
📚 Resources:  
- [Unified Storage](https://www.nutanix.com/products/unified-storage)  
- [Data Lens](https://www.nutanix.com/solutions/data-governance)  
✅ Exit: One of each storage type running, Data Lens alert triggered.  

## Week 4: NC2 & DR Patterns (Metro, NearSync, Async, MST)
🎯 Objectives: Learn DR concepts and map RPO/RTO.  
🛠 Lab: Deploy NC2 on Azure, configure NearSync for one app, Async for another, MST for backups.  
📚 Resources:  
- [Nutanix NC2](https://www.nutanix.com/products/cloud-clusters)  
- [Disaster Recovery](https://www.nutanix.com/solutions/disaster-recovery)  
✅ Exit: DR runbooks tested, RPO/RTO documented.  

## Week 5: Kubernetes with NKP (Fleet, GitOps, Policies)
🎯 Objectives: Manage AKS with NKP, apply GitOps.  
🛠 Lab: Attach AKS cluster, enable logging, apply upgrade policy, deploy app via GitOps.  
📚 Resources:  
- [NKP Overview](https://www.nutanix.com/products/kubernetes-platform)  
- [ArgoCD](https://argo-cd.readthedocs.io/)  
✅ Exit: AKS cluster managed in NKP, GitOps app deployed.  

## Week 6: Database Service (MySQL with NDB)
🎯 Objectives: Provision and manage MySQL via NDB.  
🛠 Lab: Create MySQL DB, patch, clone, backup/restore.  
📚 Resources:  
- [Nutanix NDB](https://www.nutanix.com/products/database-service)  
- [Nutanix University](https://www.nutanixuniversity.com/)  
✅ Exit: MySQL lifecycle completed (provision → patch → clone → restore).  
