> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

> **Context Management:**
> If the IaC automation landscape is too complex for comprehensive analysis, prioritize:
> 1. Security-critical Infrastructure as Code configurations and state management
> 2. Production deployment automation and GitOps workflow effectiveness
> 3. Integration patterns between different IaC tools and cloud providers
> Ask user to specify focus areas if scope exceeds analysis capacity.

> **Analysis Validation:**
> - Mark findings as "Confirmed" vs "Potential" based on configuration file evidence and tool version compatibility
> - Reference specific module configurations, provider settings, or automation patterns when citing findings
> - Provide confidence indicators: High/Medium/Low for each IaC security and maintainability recommendation
> - Note when additional tool execution or state file access would improve analysis accuracy
title: "Recon IaC Automation"
author: you
category: discovery
description: "Locate Terraform/Ansible/Helm/Kustomize/Argo/Flux/Packer; summarize modules, providers, and backends (masked)."
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
`OUT="/tmp/recon_iac_automation-$(hostname)-$(date +%Y%m%d-%H%M%S).md"`; `mkdir -p /tmp`; `: > "$OUT"`

### 2) Discovery (file patterns only; no execution)
```bash
echo "## IaC Discovery" | tee -a "$OUT"
find ~ -type f -name "*.tf" -o -name "values*.yaml" -o -name "Chart.yaml" -o -name "kustomization.yaml" -o -name "Jenkinsfile" 2>/dev/null | head -n 1000 | tee -a "$OUT"
```

### 3) Terraform Summaries (no init/apply)
```bash
echo "## Terraform" | tee -a "$OUT"
while read -r tf; do
  d=$(dirname "$tf")
  echo "### Module dir: $d" | tee -a "$OUT"
  grep -HnE 'backend|provider|module ' "$d"/*.tf 2>/dev/null | sed -E 's/(access_key|secret_key|token)\s*=\s*".*"/\1="***MASKED***"/g' | tee -a "$OUT"
done < <(find ~ -type f -name "*.tf" 2>/dev/null | head -n 200)
```

### 4) Ansible/Helm/Kustomize/Argo/Flux/Packer
```bash
echo "## Ansible" | tee -a "$OUT"
find ~ -type d -name "ansible" -o -name "playbooks" 2>/dev/null | head -n 50 | tee -a "$OUT"
echo "## Helm" | tee -a "$OUT"
grep -HnE '^name:|^version:' $(find ~ -type f -name "Chart.yaml" 2>/dev/null | head -n 100) 2>/dev/null | tee -a "$OUT"
echo "## Kustomize" | tee -a "$OUT"
grep -HnE '^resources:|^bases:' $(find ~ -type f -name "kustomization.yaml" 2>/dev/null | head -n 100) 2>/dev/null | tee -a "$OUT"
echo "## Argo/Flux" | tee -a "$OUT"
grep -RHoE 'apiVersion: argoproj.io|apiVersion: fluxcd.io' ~ 2>/dev/null | head -n 100 | tee -a "$OUT"
echo "## Packer" | tee -a "$OUT"
find ~ -type f -name "*.pkr.hcl" 2>/dev/null | head -n 100 | tee -a "$OUT"
```

### 5) Wrap
- Summarize modules/charts/backends (masked); print OUT path.
