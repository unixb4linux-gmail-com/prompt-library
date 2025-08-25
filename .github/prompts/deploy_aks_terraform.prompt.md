> **Directive:**
> 
> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

> **Context Management:**
> If the AKS deployment requirements are too complex for comprehensive implementation, prioritize:
> 1. Security-critical cluster configurations and managed identity setup
> 2. Production-ready networking and node pool configurations
> 3. Integration effectiveness with Azure services and monitoring solutions
> Ask user to specify focus areas if scope exceeds implementation capacity.

> **Analysis Validation:**
> - Mark implementation choices as "Best Practice" vs "Alternative" based on Azure documentation and Well-Architected Framework
> - Reference specific Azure resources, Terraform modules, or security configurations when making recommendations
> - Provide confidence indicators: High/Medium/Low for each infrastructure and security decision
> - Note when additional Azure expertise or application requirements would improve implementation quality
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
<!--
title: "Deploy with Terraform to AKS"
category: "Infrastructure"
description: "Set up Terraform scripts for deploying a containerized app to Azure Kubernetes Service"
-->

# Prompt: Deploy AKS with Terraform

Write Terraform code to deploy a containerized application to Azure Kubernetes Service (AKS). Include resource group, AKS cluster, node pool, and networking configuration. Add instructions for applying the Terraform scripts.
