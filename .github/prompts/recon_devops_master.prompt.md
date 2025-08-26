---
version: "1.0.0"
created_date: "2025-08-26"
last_updated: "2025-08-26"
---

> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

> **Context Management:**
> If the DevOps tooling landscape is too complex for comprehensive reconnaissance, prioritize:
> 1. Security-critical tools and credentials with production access
> 2. Active CI/CD pipelines and infrastructure automation tools
> 3. Integration patterns between different DevOps tools and cloud providers
> Ask user to specify focus areas if scope exceeds reconnaissance capacity.

> **Analysis Validation:**
> - Mark findings as "Confirmed" vs "Potential" based on tool presence, configuration evidence, and successful authentication tests
> - Reference specific tool versions, credential files, or integration configurations when citing findings
> - Provide confidence indicators: High/Medium/Low for each tooling security and operational recommendation
> - Note when additional tool execution or remote system access would improve reconnaissance accuracy
title: "Recon: DevOps (Master – Safe, Non-Destructive)"
author: you
category: discovery
description: "Interactive, non-destructive recon: enumerate tools, accounts, cloud access, CI/CD, K8s, IaC. Output to /tmp with hostname+timestamp. Mask secrets. Confirm before any remote CLI calls."
---

> **Directive (Safety & Scope)**
> - **Do not modify** any files, configs, environment variables, or remote systems.
> - **No network scanning.** Only passive inspection and read‑only CLI calls when explicitly confirmed.
> - **Professional accounts only.** Personal/social accounts are out of scope.
> - **Mask secrets** in output (show only prefixes/suffixes).
> - **Parallel mapping** is okay; when environments are detected, **start with dev**, then staging, then prod.
>
> **Interaction & Output**
> - Be **interactive**. Ask clarifying questions where needed and **pause for confirmation** before any remote CLI call (aws/az/gcloud/kubectl/terraform/etc.).
> - Create an output file in `/tmp` named:  
>   `/tmp/recon-$(hostname)-$(date +%Y%m%d-%H%M%S).md`  
>   Ensure `/tmp` exists; if not, create it.
> - Append all findings to this file **and** echo summaries to screen.
>
> **Compatibility**
> - Detect OS (Linux/macOS/Windows with WSL/Git Bash). Prefer **bash/zsh** semantics if present; otherwise adapt.

## Step 0: Confirm Readiness
Ask the operator to confirm:
- We have authorization to access professional accounts found on this machine.
- We will not change anything.
- We will pause for confirmation before any networked CLI command.

Proceed only after explicit confirmation.

## Step 1: OS & Host Context (Local Only)
... (rest of prompt omitted for brevity in this code block)
