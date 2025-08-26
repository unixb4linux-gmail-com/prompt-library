---
title: Recon CircleCI Integration
description: Discover and inventory CircleCI configurations, contexts, and integrations
  across repositories
category: discovery
version: 1.0.0
created_date: '2025-08-26'
last_updated: '2025-08-26'
---

> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

> **Context Management:**
> If the CircleCI landscape is too complex for comprehensive reconnaissance, prioritize:
> 1. Security-critical pipeline configurations and context management
> 2. Production deployment workflows and approval gate effectiveness
> 3. Integration patterns with external services and secret management systems
> Ask user to specify focus areas if scope exceeds reconnaissance capacity.

> **Analysis Validation:**
> - Mark findings as "Confirmed" vs "Potential" based on configuration file evidence and CLI tool availability
> - Reference specific config.yml patterns, orb usage, or integration setups when citing findings
> - Provide confidence indicators: High/Medium/Low for each CI/CD security and operational recommendation
> - Note when additional CircleCI project access or API authentication would improve reconnaissance accuracy

# 🔍 Recon CircleCI Integration

You are a DevOps reconnaissance specialist. Your task is to discover and inventory CircleCI configurations, projects, contexts, and integrations in the current environment.

> **Safety Protocol:**
> - **Mask secrets** in output (print first 4 ... last 4 only).
> - **Read-only operations** unless explicitly confirmed by user.
> - **No modifications** to CI/CD configurations during discovery.
> 
> When printing a credential-like value: `XXXX${val:0:4}…${val:-4}` (or equivalent) and mark as masked.

## Step 1: Environment Setup

```bash
# Set up output file with timestamp
HOSTNAME=$(hostname -s 2>/dev/null || echo "unknown")
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUT="/tmp/circleci_recon_${HOSTNAME}_${TIMESTAMP}.txt"

echo "# CircleCI Reconnaissance Report" | tee "$OUT"
echo "# Generated: $(date)" | tee -a "$OUT"
echo "# Host: $HOSTNAME" | tee -a "$OUT"
echo "" | tee -a "$OUT"
```

## Step 2: Local Repository Discovery

### CircleCI Configuration Files
```bash
echo "## CircleCI Configuration Discovery" | tee -a "$OUT"
echo "" | tee -a "$OUT"

# Find CircleCI config files
find . -name ".circleci" -type d 2>/dev/null | while read -r dir; do
    echo "Found CircleCI directory: $dir" | tee -a "$OUT"
    
    # List config files
    if [ -f "$dir/config.yml" ]; then
        echo "  - config.yml found" | tee -a "$OUT"
        
        # Extract basic info (no secrets)
        echo "  - Workflows:" | tee -a "$OUT"
        grep -E "^\s*[a-zA-Z][a-zA-Z0-9_-]*:" "$dir/config.yml" 2>/dev/null | head -10 | sed 's/^/    /' | tee -a "$OUT"
        
        # Check for orbs
        echo "  - Orbs used:" | tee -a "$OUT"
        grep -E "^\s*[a-zA-Z][a-zA-Z0-9_/-]*:" "$dir/config.yml" 2>/dev/null | grep -E "@[0-9]" | sed 's/^/    /' | tee -a "$OUT" || echo "    None found" | tee -a "$OUT"
        
        # Executors
        echo "  - Executors:" | tee -a "$OUT"
        grep -E "^\s*(docker|machine|macos|windows):" "$dir/config.yml" 2>/dev/null | sed 's/^/    /' | tee -a "$OUT" || echo "    None explicitly defined" | tee -a "$OUT"
    fi
    
    # Check for custom scripts
    if [ -d "$dir/scripts" ]; then
        echo "  - Custom scripts:" | tee -a "$OUT"
        find "$dir/scripts" -type f -name "*.sh" 2>/dev/null | sed 's/^/    /' | tee -a "$OUT"
    fi
    
    echo "" | tee -a "$OUT"
done

# Search for CircleCI references in other files
echo "## CircleCI References in Codebase" | tee -a "$OUT"
grep -r -l "circleci" . --include="*.md" --include="*.yml" --include="*.yaml" --include="*.json" 2>/dev/null | head -20 | tee -a "$OUT"
echo "" | tee -a "$OUT"
```

### Project Integration Analysis
```bash
echo "## Project Integration Patterns" | tee -a "$OUT"
echo "" | tee -a "$OUT"

# Check for common deployment patterns
echo "### Deployment Integrations:" | tee -a "$OUT"

# AWS integrations
if grep -r "aws-cli\|AWS_" .circleci/ 2>/dev/null | head -5; then
    echo "  - AWS deployment detected" | tee -a "$OUT"
    grep -r "AWS_" .circleci/ 2>/dev/null | grep -v "AWS_SECRET\|AWS_ACCESS" | head -3 | sed 's/^/    /' | tee -a "$OUT"
fi

# Docker integrations  
if grep -r "docker\|DOCKER_" .circleci/ 2>/dev/null | head -5; then
    echo "  - Docker integration detected" | tee -a "$OUT"
    grep -r "docker:" .circleci/ 2>/dev/null | head -3 | sed 's/^/    /' | tee -a "$OUT"
fi

# Kubernetes deployments
if grep -r "kubectl\|kubernetes\|k8s" .circleci/ 2>/dev/null | head -5; then
    echo "  - Kubernetes deployment detected" | tee -a "$OUT"
fi

echo "" | tee -a "$OUT"
```

## Step 3: CircleCI CLI Discovery (if available)

**Note: Only run with user confirmation for external API calls**

```bash
# Check if CircleCI CLI is installed
if command -v circleci >/dev/null 2>&1; then
    echo "## CircleCI CLI Available" | tee -a "$OUT"
    circleci version 2>/dev/null | tee -a "$OUT"
    echo "" | tee -a "$OUT"
    
    # Ask user before making API calls
    read -p "CircleCI CLI detected. Make API calls to discover projects/contexts? [y/N]: " CONFIRM
    if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
        echo "### CircleCI Projects (requires authentication):" | tee -a "$OUT"
        
        # List projects (will require auth)
        circleci project list 2>/dev/null | head -10 | tee -a "$OUT" || echo "Authentication required or no projects found" | tee -a "$OUT"
        
        # Contexts (mask any sensitive data)
        echo "### Available Contexts:" | tee -a "$OUT"
        circleci context list 2>/dev/null | head -10 | tee -a "$OUT" || echo "Authentication required or no contexts found" | tee -a "$OUT"
    else
        echo "Skipped API calls per user request" | tee -a "$OUT"
    fi
    echo "" | tee -a "$OUT"
else
    echo "## CircleCI CLI Not Installed" | tee -a "$OUT"
    echo "Install with: curl -fLSs https://raw.githubusercontent.com/CircleCI-Public/circleci-cli/master/install.sh | bash" | tee -a "$OUT"
    echo "" | tee -a "$OUT"
fi
```

## Step 4: Environment Variables & Context Analysis

```bash
echo "## Environment Variables & Context References" | tee -a "$OUT"
echo "" | tee -a "$OUT"

# Find environment variable references (mask values)
echo "### Environment Variables Referenced:" | tee -a "$OUT"
grep -r "\$\|env\." .circleci/ 2>/dev/null | grep -E "(CIRCLE_|AWS_|DOCKER_|API_|SECRET_|TOKEN_|KEY_)" | \
    sed 's/\(SECRET_[^:]*:\|TOKEN_[^:]*:\|KEY_[^:]*:\|PASSWORD_[^:]*:\).*/\1 [MASKED]/' | \
    head -20 | sed 's/^/  /' | tee -a "$OUT"

# Context usage patterns
echo "### Context Usage:" | tee -a "$OUT"
grep -r "context:" .circleci/ 2>/dev/null | sed 's/^/  /' | tee -a "$OUT" || echo "  No explicit context usage found" | tee -a "$OUT"

echo "" | tee -a "$OUT"
```

## Step 5: Security & Compliance Scanning

```bash
echo "## Security Configuration Assessment" | tee -a "$OUT"
echo "" | tee -a "$OUT"

# Check for security scanning tools
echo "### Security Tools Integration:" | tee -a "$OUT"
SECURITY_TOOLS=("snyk" "owasp" "sonarqube" "codeql" "trivy" "aqua" "twistlock")

for tool in "${SECURITY_TOOLS[@]}"; do
    if grep -r -i "$tool" .circleci/ 2>/dev/null >/dev/null; then
        echo "  - $tool integration detected" | tee -a "$OUT"
        grep -r -i "$tool" .circleci/ 2>/dev/null | head -2 | sed 's/^/    /' | tee -a "$OUT"
    fi
done

# Check for approval job patterns
echo "### Manual Approval Gates:" | tee -a "$OUT"  
if grep -r "approval\|hold" .circleci/ 2>/dev/null; then
    echo "  - Manual approval gates detected" | tee -a "$OUT"
    grep -r "type: approval\|hold" .circleci/ 2>/dev/null | sed 's/^/    /' | tee -a "$OUT"
else
    echo "  - No manual approval gates found" | tee -a "$OUT"
fi

echo "" | tee -a "$OUT"
```

## Step 6: Performance & Resource Analysis

```bash
echo "## Performance Configuration" | tee -a "$OUT"
echo "" | tee -a "$OUT"

# Resource class usage
echo "### Resource Classes:" | tee -a "$OUT"
grep -r "resource_class:" .circleci/ 2>/dev/null | sed 's/^/  /' | tee -a "$OUT" || echo "  Using default resource classes" | tee -a "$OUT"

# Parallelism settings
echo "### Parallelism Configuration:" | tee -a "$OUT"
grep -r "parallelism:" .circleci/ 2>/dev/null | sed 's/^/  /' | tee -a "$OUT" || echo "  No explicit parallelism configuration" | tee -a "$OUT"

# Caching strategies
echo "### Caching Patterns:" | tee -a "$OUT"
grep -r "cache\|persist_to_workspace\|attach_workspace" .circleci/ 2>/dev/null | wc -l | xargs echo "  Cache operations found:" | tee -a "$OUT"

echo "" | tee -a "$OUT"
```

## Step 7: Summary Report

```bash
echo "## Discovery Summary" | tee -a "$OUT"
echo "Generated: $(date)" | tee -a "$OUT"
echo "Report saved to: $OUT" | tee -a "$OUT"
echo ""

echo "CircleCI reconnaissance complete. Report saved to: $OUT"
```

## Output Analysis

After running the reconnaissance, analyze and summarize:

### Discovered Components
- **Configuration Files**: List of `.circleci/config.yml` files found
- **Workflows**: Active workflows and their purposes  
- **Orbs**: Third-party integrations and versions
- **Scripts**: Custom deployment and build scripts

### Integration Patterns
- **Cloud Providers**: AWS, Azure, GCP integrations discovered
- **Container Platforms**: Docker, Kubernetes deployments
- **Security Tools**: Scanning and compliance tools in use
- **Notification Systems**: Slack, email, monitoring integrations

### Security Posture
- **Secret Management**: Context usage vs environment variables
- **Access Controls**: Manual approvals and branch restrictions
- **Security Scanning**: Integrated security tools and policies
- **Compliance**: SOC2, PCI, or other compliance configurations

### Performance Characteristics
- **Resource Usage**: Executor types and resource classes
- **Optimization**: Caching strategies and parallelism
- **Build Times**: Workflow efficiency indicators
- **Cost Optimization**: Resource allocation patterns

**Note**: All sensitive information should be masked in the output following the format `XXXX[first4]…[last4]` for any credential-like values discovered.