---
title: "Recon K8s and Containers"
author: you
category: discovery
description: "Read-only Kubernetes contexts and local container runtime inventory; optional minimal cluster info on confirm."
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
`OUT="/tmp/recon_k8s_and_containers-$(hostname)-$(date +%Y%m%d-%H%M%S).md"`; `mkdir -p /tmp`; `: > "$OUT"`

### 2) Kubernetes (local config only first)
```bash
echo "## Kubernetes" | tee -a "$OUT"
[ -f ~/.kube/config ] && kubectl config get-contexts 2>/dev/null | tee -a "$OUT"
```
- **If contexts exist**, ask: “Query **dev first** for cluster-info and namespaces (read-only)? Proceeding may create audit logs.”
- If **Yes**, per context (dev → stage → prod naming match if possible):
```bash
CTX_LIST=$(kubectl config get-contexts -o name 2>/dev/null)
for ctx in $CTX_LIST; do
  echo "$ctx" | grep -Ei 'dev|development' >/dev/null || continue
  echo "### Context: $ctx" | tee -a "$OUT"
  kubectl --context "$ctx" cluster-info 2>/dev/null | tee -a "$OUT"
  kubectl --context "$ctx" get ns -A --no-headers 2>/dev/null | head -n 50 | tee -a "$OUT"
done
# Repeat with staging, then prod (match 'stg|stage|staging' then 'prd|prod|production')
```

### 3) Containers (local only)
```bash
echo "## Containers" | tee -a "$OUT"
(which docker && docker ps -a 2>/dev/null | tee -a "$OUT" && docker images 2>/dev/null | tee -a "$OUT" && docker context ls 2>/dev/null | tee -a "$OUT") || true
(which podman && podman ps -a 2>/dev/null | tee -a "$OUT" && podman images 2>/dev/null | tee -a "$OUT") || true
```

### 4) Wrap
- Summarize contexts and container runtimes; print OUT path.
