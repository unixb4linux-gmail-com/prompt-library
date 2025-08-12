---
title: "Recon Tools Local"
author: you
category: discovery
description: "Enumerate DevOps tooling; record versions, config paths, and contexts without making changes."
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
- Create: `OUT="/tmp/recon_tools_local-$(hostname)-$(date +%Y%m%d-%H%M%S).md"`; `mkdir -p /tmp`; `: > "$OUT"`
- Detect OS/shell:
```bash
echo "## Host" | tee -a "$OUT"
uname -a 2>/dev/null | tee -a "$OUT" || ver | tee -a "$OUT"
echo "User: $(whoami)" | tee -a "$OUT"
echo "Shell: $SHELL" | tee -a "$OUT" 2>/dev/null || echo "Shell: %ComSpec%" | tee -a "$OUT"
echo "PATH: $PATH" | tee -a "$OUT"
```

### 2) Locate Tools
- Candidate list: `aws az gcloud kubectl helm terraform ansible packer vault gh git docker podman kind k9s skaffold flux argocd snyk trivy jq yq`
```bash
echo "## Tools" | tee -a "$OUT"
for t in aws az gcloud kubectl helm terraform ansible packer vault gh git docker podman kind k9s skaffold flux argocd snyk trivy jq yq; do
  which "$t" >/dev/null 2>&1 || command -v "$t" >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "### $t" | tee -a "$OUT"
    echo "Path: $(command -v "$t")" | tee -a "$OUT"
    "$t" --version 2>&1 | head -n 5 | tee -a "$OUT"
  fi
done
```

### 3) Config Footprints (list files/dirs only; no contents)
```bash
echo "## Config Footprints" | tee -a "$OUT"
ls -lah ~/.aws 2>/dev/null | tee -a "$OUT"
ls -lah ~/.azure 2>/dev/null | tee -a "$OUT"
ls -lah ~/.config/gcloud 2>/dev/null | tee -a "$OUT"
ls -lah ~/.kube 2>/dev/null | tee -a "$OUT"
ls -lah ~/.terraform.d 2>/dev/null | tee -a "$OUT"
ls -lah ~/.config/gh 2>/dev/null | tee -a "$OUT"
```

### 4) Context/Profile Summaries (no secrets)
- AWS profiles (filenames only), Azure subscriptions presence, GCloud configs (names), kube contexts (names only).
```bash
echo "## Profile/Context Summaries" | tee -a "$OUT"
[ -d ~/.aws ] && grep -E '^\[.*\]' -H ~/.aws/config ~/.aws/credentials 2>/dev/null | sed 's/:/ -> /' | tee -a "$OUT"
[ -d ~/.azure ] && ls -1 ~/.azure 2>/dev/null | sed 's/^/azure file: /' | tee -a "$OUT"
[ -d ~/.config/gcloud ] && gcloud config configurations list --format=json 2>/dev/null | tee -a "$OUT"
[ -f ~/.kube/config ] && kubectl config get-contexts 2>/dev/null | tee -a "$OUT"
[ -d ~/.terraform.d ] && ls -1 ~/.terraform.d 2>/dev/null | sed 's/^/terraform.d: /' | tee -a "$OUT"
[ -f ~/.config/gh/hosts.yml ] && echo "GitHub CLI hosts.yml present" | tee -a "$OUT"
```

### 5) Wrap
- Print a short summary and path to the OUT file.
