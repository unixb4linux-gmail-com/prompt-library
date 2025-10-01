---
title: "CI/CD Integration Reconnaissance"
description: "Identify CI/CD configurations in local repos—names, triggers, envs, and secret references (names only)"
category: "CI/CD"
author: "you"
version: "1.0.0"
created_date: "2025-08-26"
last_updated: "2025-08-26"
---

> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

> **Context Management:**
> If the CI/CD integration landscape is too complex for comprehensive reconnaissance, prioritize:
> 1. Security-critical pipeline configurations and secret management patterns
> 2. Production deployment workflows and environment-specific configurations
> 3. Integration patterns between different CI/CD systems and repository structures
> Ask user to specify focus areas if scope exceeds reconnaissance capacity.

> **Analysis Validation:**
> - Mark findings as "Confirmed" vs "Potential" based on configuration file evidence and workflow validation
> - Reference specific CI/CD files, secret references, or integration patterns when citing findings
> - Provide confidence indicators: High/Medium/Low for each CI/CD security and operational recommendation
> - Note when additional repository access or CI/CD platform access would improve reconnaissance accuracy


> **Global Safety**
> - **Do not modify** files, configs, env vars, or remote systems.
> - **No network scanning.** Only passive inspection and read‑only CLI calls when explicitly confirmed.
> - **Professional accounts only.** Personal/social accounts are out of scope.
> - **Mask secrets** in output (print first 4 … last 4 only).
> - When environments are detected, **start with dev**, then staging, then prod.
> - Always **ASK BEFORE REMOTE** execution (aws/az/gcloud/kubectl/helm/terraform/etc.).
>
> **Output Handling**
> - Ensure `/tmp` exists; write to `/tmp/<file>-$(hostname)-$(date +%Y%m%d-%H%M%S).md`.
> - Echo concise summaries to screen and append full details to the file.
>
> **Helper (Masking)**
> When printing a credential-like value: `XXXX${val:0:4}…${val:-4}` (or equivalent) and mark as masked.


## Steps

### 1) Init
`OUT="/tmp/recon_cicd_integrations-$(hostname)-$(date +%Y%m%d-%H%M%S).md"`; `mkdir -p /tmp`; `: > "$OUT"`

### 2) Find Repositories
```bash
echo "## Repositories" | tee -a "$OUT"
find ~ -type d -name ".git" -prune 2>/dev/null | sed 's|/\.git$||' | head -n 300 | tee -a "$OUT"
```

### 3) For each repo (bounded to first 50)
- Print remote URLs, default branch, and CI files if present.
```bash
echo "## CI/CD" | tee -a "$OUT"
i=0
while read -r repo; do
  [ -d "$repo/.git" ] || continue
  echo "### Repo: $repo" | tee -a "$OUT"
  git -C "$repo" remote -v | tee -a "$OUT"
  git -C "$repo" branch -vv | head -n 5 | tee -a "$OUT"
  ls -lah "$repo/.github/workflows" 2>/dev/null | tee -a "$OUT"
  [ -f "$repo/.gitlab-ci.yml" ] && echo ".gitlab-ci.yml present" | tee -a "$OUT"
  [ -f "$repo/bitbucket-pipelines.yml" ] && echo "bitbucket-pipelines.yml present" | tee -a "$OUT"
  [ -f "$repo/Jenkinsfile" ] && echo "Jenkinsfile present" | tee -a "$OUT"
  # Parse workflow names/triggers
  grep -E 'name:|on:' -H "$repo/.github/workflows/"* 2>/dev/null | tee -a "$OUT"
  # Secret refs (names only)
  grep -RHoE 'secrets\.[A-Za-z0-9_]+' "$repo/.github/workflows" 2>/dev/null | sort -u | tee -a "$OUT"
  i=$((i+1)); [ $i -ge 50 ] && break
done < <(find ~ -type d -name ".git" -prune 2>/dev/null | sed 's|/\.git$||' | head -n 300)
```

### 4) Wrap
- Summarize CI systems detected; print OUT path.
