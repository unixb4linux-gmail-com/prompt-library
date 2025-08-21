> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.
title: "Recon Accounts Sessions"
author: you
category: discovery
description: "Summarize professional accounts and sessions; git identities, CLIs, and orgs (masked)."
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
`OUT="/tmp/recon_accounts_sessions-$(hostname)-$(date +%Y%m%d-%H%M%S).md"`; `mkdir -p /tmp`; `: > "$OUT"`

### 2) Git Identity & Remotes
```bash
echo "## Git Identity" | tee -a "$OUT"
git config --global --list 2>/dev/null | tee -a "$OUT"
echo "## Git Remotes (sample)" | tee -a "$OUT"
find ~ -type d -name ".git" -prune 2>/dev/null | sed 's|/\.git$||' | head -n 50 | while read -r repo; do
  echo "### $repo" | tee -a "$OUT"
  git -C "$repo" remote -v | tee -a "$OUT"
done
```

### 3) GitHub CLI
```bash
echo "## GitHub CLI" | tee -a "$OUT"
gh auth status 2>/dev/null | tee -a "$OUT" || echo "gh not authenticated or not installed" | tee -a "$OUT"
[ -f ~/.config/gh/hosts.yml ] && echo "hosts.yml present (details masked)" | tee -a "$OUT"
```

### 4) Cloud CLIs (session/account summaries only)
```bash
echo "## Cloud CLI Sessions" | tee -a "$OUT"
which aws >/dev/null 2>&1 && aws sts get-caller-identity 2>/dev/null | tee -a "$OUT"
which az  >/dev/null 2>&1 && az account show 2>/dev/null | tee -a "$OUT"
which gcloud >/dev/null 2>&1 && gcloud auth list 2>/dev/null | tee -a "$OUT"
```

### 5) Messaging/Work Apps (presence only; no personal/social)
```bash
echo "## Work Apps (presence only)" | tee -a "$OUT"
ps aux 2>/dev/null | egrep -i 'slack|teams|mattermost|zoom|okta|onelogin' | egrep -v 'egrep' | tee -a "$OUT"
```

### 6) Wrap
- Summarize identities and sessions; print OUT path.
