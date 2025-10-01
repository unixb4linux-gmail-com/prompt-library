---
title: "Cloud Credential Reconnaissance"
description: "Locate and summarize professional cloud credentials; optionally confirm active identity via read-only calls"
category: "Security"
author: "you"
version: "1.0.0"
created_date: "2025-08-26"
last_updated: "2025-08-26"
---

> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

> **Context Management:**
> If the credential landscape is too complex for comprehensive analysis, prioritize:
> 1. Security-critical cloud service accounts and production credentials
> 2. Active development and CI/CD service accounts with elevated privileges
> 3. Integration effectiveness with deployment pipelines and automation
> Ask user to specify focus areas if scope exceeds analysis capacity.

> **Analysis Validation:**
> - Mark findings as "Confirmed" vs "Potential" based on credential file presence and successful authentication tests
> - Reference specific credential files, environment variables, or CLI configuration when citing findings
> - Provide confidence indicators: High/Medium/Low for each credential security recommendation
> - Note when additional account access or credential rotation would improve security posture


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
`OUT="/tmp/recon_cloud_credentials-$(hostname)-$(date +%Y%m%d-%H%M%S).md"`; `mkdir -p /tmp`; `: > "$OUT"`

### 2) Footprints (no contents)
```bash
echo "## Credential Footprints" | tee -a "$OUT"
ls -lah ~/.aws 2>/dev/null | tee -a "$OUT"
ls -lah ~/.azure 2>/dev/null | tee -a "$OUT"
ls -lah ~/.config/gcloud 2>/dev/null | tee -a "$OUT"
ls -lah ~/.kube 2>/dev/null | tee -a "$OUT"
ls -lah ~/.config/gh 2>/dev/null | tee -a "$OUT"
env | grep -E 'VAULT_ADDR|VAULT_TOKEN|TF_VAR_' 2>/dev/null | sed -E 's/(=).+/=***MASKED***/' | tee -a "$OUT"
```

### 3) Profiles/Accounts (masked identifiers)
```bash
echo "## Profiles" | tee -a "$OUT"
[ -f ~/.aws/credentials ] && awk '/\[.*\]/{print $0;next}/aws_access_key_id/{{print "aws_access_key_id: " substr($0, index($0,"=")+2,4) "...(masked)... " substr($0,length($0)-3,4)}}' ~/.aws/credentials 2>/dev/null | tee -a "$OUT"
[ -f ~/.aws/config ] && grep -E '^\[profile ' ~/.aws/config 2>/dev/null | tee -a "$OUT"
[ -d ~/.azure ] && echo "Azure profile present (details masked)" | tee -a "$OUT"
[ -d ~/.config/gcloud ] && gcloud config configurations list --format='value(name,is_active)' 2>/dev/null | tee -a "$OUT"
[ -f ~/.kube/config ] && kubectl config get-contexts -o name 2>/dev/null | sed 's/^/kube-context: /' | tee -a "$OUT"
[ -f ~/.config/gh/hosts.yml ] && echo "GitHub CLI hosts.yml present" | tee -a "$OUT"
```

### 4) ASK BEFORE REMOTE – identity confirmation (read-only)
- **Prompt:** “Run minimal identity checks now? (aws sts get-caller-identity / az account show / gcloud auth list) — may create access logs.”
- If **Yes**, then:
```bash
echo "## Remote Identity Checks (on confirm)" | tee -a "$OUT"
which aws >/dev/null 2>&1 && aws sts get-caller-identity 2>/dev/null | tee -a "$OUT"
which az >/dev/null 2>&1 && az account show 2>/dev/null | tee -a "$OUT"
which gcloud >/dev/null 2>&1 && gcloud auth list 2>/dev/null | tee -a "$OUT"
```

### 5) Wrap
- Summarize discovered platforms and masked identifiers; print OUT path.
