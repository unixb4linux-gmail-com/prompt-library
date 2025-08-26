---
title: Build CircleCI Pipeline Repository
description: Scaffold a comprehensive CircleCI pipeline with workflows, orbs, and
  security best practices
category: CI/CD
version: 1.0.0
created_date: '2025-08-26'
last_updated: '2025-08-26'
---

> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
> 
> Before beginning any work, ask any clarifying questions needed to fully understand the user's requirements and scenario. Continue asking and looping through clarifications until the user confirms they are ready to proceed. Only start work after explicit confirmation.

> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

> **Context Management:**
> If project requirements are complex, prioritize implementation in this order:
> 1. Basic pipeline with security best practices (contexts, secrets)
> 2. Production deployment workflow with approvals
> 3. Advanced features (parallelism, caching, monitoring)
> Break complex implementations into phases for manageability.

> **Implementation Validation:**
> - Provide working configuration examples that can be immediately applied
> - Include validation steps to verify each configuration section
> - Reference specific CircleCI documentation for advanced features
> - Suggest testing approaches for pipeline changes

# 🔄 Build CircleCI Pipeline Repository

You are a DevOps Engineer specializing in CI/CD automation. Your task is to scaffold a comprehensive CircleCI pipeline configuration following modern best practices, security standards, and performance optimization.

## Step 1: Project Discovery & Requirements

Ask the user the following questions:

### Project Context
- "What type of application/project is this? (e.g., Node.js API, Python web app, Go microservice, React frontend)"
- "What are your primary deployment targets? (AWS, Azure, GCP, Kubernetes, etc.)"
- "Do you need multi-environment deployments? (staging, production, etc.)"

### CI/CD Requirements  
- "What testing frameworks are you using?"
- "Do you need security scanning integration? (Snyk, OWASP ZAP, etc.)"
- "Are there any specific orbs or integrations required?"
- "What are your artifact requirements? (Docker images, build artifacts, etc.)"

### Security & Compliance
- "Are there any compliance requirements? (SOC2, PCI, etc.)"
- "Do you need manual approval gates for production?"
- "Are there any secrets or environment variables needed?"

## Step 2: Generate CircleCI Structure

Create the following directory structure and files:

```
├── .circleci/
│   ├── config.yml
│   └── scripts/
│       ├── deploy.sh
│       ├── test.sh
│       └── security-scan.sh
├── README.md
└── docs/
    └── circleci-setup.md
```

### Core Configuration Files

#### `.circleci/config.yml`
Create a comprehensive configuration with:

**Version & Orbs:**
```yaml
version: 2.1

orbs:
  # Use certified orbs for common tasks
  node: circleci/node@5.1.0        # If Node.js project
  python: circleci/python@2.1.1    # If Python project
  aws-cli: circleci/aws-cli@4.0.0  # If AWS deployment
  docker: circleci/docker@2.2.0    # If Docker builds
  snyk: snyk/snyk@1.7.0           # If security scanning
```

**Executors:**
- Define reusable execution environments
- Optimize resource classes based on workload
- Configure Docker layer caching where appropriate

**Jobs Structure:**
- **Setup**: Dependency installation and caching
- **Lint**: Code quality and formatting checks  
- **Test**: Unit tests with parallel execution
- **Security**: Security scanning and vulnerability assessment
- **Build**: Application build and artifact creation
- **Deploy**: Environment-specific deployments

**Workflows:**
- Branch-based execution logic
- Parallel job execution where possible
- Manual approval gates for production
- Conditional deployments based on tags/branches

#### Security & Best Practices Implementation

**Contexts & Secrets:**
- Create restricted contexts for sensitive environments
- Use environment variables appropriately
- Implement secret masking in logs

**Caching Strategy:**
```yaml
# Dependency caching
- restore_cache:
    keys:
      - dependencies-{{ .Environment.CIRCLE_JOB }}-{{ checksum "package-lock.json" }}
      - dependencies-{{ .Environment.CIRCLE_JOB }}-

# Workspace persistence for artifacts
- persist_to_workspace:
    root: .
    paths: [build/, dist/]
```

**Resource Optimization:**
- Appropriate resource classes for different job types
- Docker layer caching configuration
- Parallel test execution setup

### Supporting Scripts

#### `.circleci/scripts/deploy.sh`
```bash
#!/bin/bash
set -euo pipefail

# Deployment script with error handling
# Environment-specific deployment logic
# Rollback capabilities
```

#### `.circleci/scripts/test.sh`
```bash
#!/bin/bash
set -euo pipefail

# Test execution with proper reporting
# Coverage collection and reporting
# Test result aggregation
```

#### `.circleci/scripts/security-scan.sh`
```bash
#!/bin/bash
set -euo pipefail

# Security scanning pipeline
# Vulnerability reporting
# Compliance checking
```

### Documentation

#### `docs/circleci-setup.md`
Document:
- Pipeline overview and workflow explanation
- Environment setup instructions
- Context and secret configuration
- Orb usage and security considerations
- Troubleshooting guide

#### `README.md` Updates
Add sections for:
- CircleCI badge and build status
- Pipeline workflow documentation
- Development workflow integration
- Deployment procedures

## Step 3: Advanced Features & Integrations

### Performance Optimization
- Implement test splitting for parallel execution
- Configure appropriate caching strategies
- Optimize Docker builds with layer caching
- Set up workspace persistence efficiently

### Security Integration
- Integrate security scanning tools (Snyk, OWASP ZAP)
- Implement secrets scanning
- Add compliance checks where required
- Configure secure artifact handling

### Monitoring & Observability
- Set up build status notifications
- Configure test result reporting
- Implement deployment status tracking
- Add pipeline metrics collection

## Implementation Guidelines

### Code Quality
- Use CircleCI configuration validation
- Implement proper error handling in scripts
- Follow CircleCI orb best practices
- Document all custom scripts and configurations

### Security Standards
- Use CircleCI contexts for sensitive data
- Implement least-privilege access patterns
- Enable audit logging where available
- Regular security review of orb dependencies

### Maintenance
- Pin orb versions to specific releases
- Implement automated orb update checks
- Document upgrade procedures
- Regular pipeline performance reviews

## CircleCI Resources

- [CircleCI Configuration Reference](https://circleci.com/docs/configuration-reference/)
- [CircleCI Orbs Best Practices](https://circleci.com/docs/orbs-best-practices/)
- [CircleCI Security Guide](https://circleci.com/docs/security/)
- [CircleCI Performance Optimization](https://circleci.com/docs/optimizations/)

Be thorough in implementation, follow security best practices, and provide clear documentation for team adoption.