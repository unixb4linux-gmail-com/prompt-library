---
title: "Recon CICD Integrations"
author: you
category: discovery
description: "Identify CI/CD configurations in local repos—names, triggers, envs, and secret references (names only)."
---


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
