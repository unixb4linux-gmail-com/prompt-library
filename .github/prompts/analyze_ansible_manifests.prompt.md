# Analyze Ansible Manifests

---
version: "1.0.0"
created_date: "2025-08-26"
last_updated: "2025-08-26"
---

> **Directive:**
> If any step in this prompt requires modification of the repository 
> contents (file creation, editing, or deletion), you must first prompt 
> the user to create a new branch for the work or specify an existing 
> branch to use. Only proceed with changes after the user provides 
> direction.
> Before making changes, check which branch is currently checked out. 
> Check if the branch is up to date with its remote. If the branch is 
> current, offer to continue. If it is not current, offer to sync (pull) 
> the branch before continuing.
> Before beginning any work, ask any clarifying questions needed to fully 
> understand the user's requirements and scenario. Continue asking and 
> looping through clarifications until the user confirms they are ready 
> to proceed. Only start work after explicit confirmation.

**Ask clarifying questions before proceeding.**

**Ask for permission before running commands, editing, or creating files. 
Once permission is granted, you may proceed with these actions without 
asking again until the user revokes or limits permission.**

> **Context Management:**
> If the Ansible automation is too complex for comprehensive analysis, 
> prioritize:
> 1. Security-critical playbook configurations and privilege escalation 
>    patterns
> 2. Production deployment workflows and secret management effectiveness
> 3. Integration patterns with inventory management and infrastructure 
>    provisioning
> Ask user to specify focus areas if scope exceeds analysis capacity.

> **Analysis Validation:**
> - Mark findings as "Confirmed" vs "Potential" based on playbook 
>   evidence and role structure validation
> - Reference specific playbook patterns, role configurations, or 
>   security practices when citing findings
> - Provide confidence indicators: High/Medium/Low for each automation 
>   security and maintainability recommendation
