# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Core Commands

### Prompt Distribution
```bash
# Copy all prompts and rules to target repository
./copy-prompts.sh /path/to/target-repo

# Preview changes without copying (dry-run)
./copy-prompts.sh -n /path/to/target-repo

# Skip adding .github/prompts/ to .gitignore
./copy-prompts.sh --no-gitignore-prompts /path/to/target-repo

# Verbose output for debugging
./copy-prompts.sh -v /path/to/target-repo
```

### Documentation Generation
```bash
# Regenerate the prompt index file
python3 scripts/generate_index.py
```

## Repository Architecture

This is a **Prompt Library** for DevOps automation that distributes AI prompts and coding rules to other repositories. The architecture follows a distribution model where content is authored centrally and deployed to target projects.

### Core Components

**Prompt System** (`.github/prompts/`): 50+ prompt files organized by technology stack
- **Analysis prompts**: `analyze_*.prompt.md` - Audit existing infrastructure/code
- **Build prompts**: `build_*.prompt.md` - Scaffold new projects from scratch  
- **Recon prompts**: `recon_*.prompt.md` - Discovery and enumeration tasks
- **Specialized directories**: `terraform/`, `github-actions/`, `aks/` for focused workflows

**Rules System** (`.rules/`): Coding conventions and agent behaviors
- **Language rules**: `python.mdc`, `react.mdc`, `nodejs.mdc`, etc.
- **Workflow rules**: `workflows/` directory containing refactoring, testing, and API design patterns
- **Framework-specific**: `nextjs-app-router.mdc`, `ruby-on-rails.mdc`

**Distribution Mechanism**: 
- `copy-prompts.sh`: Deploys prompts to `.github/prompts/` and rules to `.rules/` in target repos
- Automatic `.gitignore` management with user confirmation
- Error handling and dry-run capabilities

### Metadata System

All prompts use YAML frontmatter for categorization and automation:
```yaml
---
title: "Prompt Title"
description: "Brief description"
category: "Technology Category"
---
```

The `generate_index.py` script parses this metadata to maintain `PROMPT_RULE_INDEX.md`.

### Best Practice Integration

Every prompt includes standardized directives:
- **Permission handling**: Ask for permission before file modifications
- **Branch safety**: Require explicit branch selection for repository changes
- **Security guidance**: Mask secrets in output, promote secure credential handling

### VS Code Integration

The repository includes VS Code settings (`.vscode/settings.json`) with:
- Chat prompt files enabled for easy prompt testing and development

## Key Patterns

**Prompt Structure**: All prompts follow consistent formatting with security best practices, branch management directives, and structured output requirements.

**Rule Application**: Rules files (`.mdc`) are automatically applied based on file patterns and technology detection in target repositories.

**Technology Coverage**: Comprehensive coverage of DevOps stack including Kubernetes, Terraform, CI/CD platforms (GitHub Actions, GitLab, Jenkins, Bitbucket), cloud providers (AWS, Azure), and monitoring tools (Prometheus, Grafana).