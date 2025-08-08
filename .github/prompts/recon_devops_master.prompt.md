---
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
