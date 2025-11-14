# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Claude Auto-Awareness System

This repository is part of a **Claude Auto-Awareness System** that automatically distributes prompts, coding rules, and document standards to all repositories via git templates and symlinks.

### System Overview

**Architecture:**
- **Git Template**: `~/.git_template/` contains Claude settings, prompts, rules, and doc standards
- **Symlinks**: Central maintenance with automatic distribution to all repositories
- **Shell Integration**: Auto-applies setup when entering new repositories
- **Auto-Setup Script**: `~/repos/claude_auto_setup.sh` for manual application

**What's Included in Every Repo:**
- `.claude/settings.local.json` - Claude configuration with git workflow permissions
- `.github/prompts/` - 62+ AI prompts via symlinks
- `.rules/` - Coding conventions and workflow patterns via symlinks
- `.doc_standards/` - Document templates via symlinks

### Core Commands

#### Auto-Setup Management
```bash
# Test the auto-awareness configuration
~/repos/claude_auto_setup.sh test

# Apply Claude setup to a specific repository
~/repos/claude_auto_setup.sh apply_single /path/to/repo

# Apply Claude setup to all repositories in ~/repos
~/repos/claude_auto_setup.sh apply_all
```

#### Shell Helper Functions
```bash
# Clone repository with automatic Claude setup
gitclone <git-url>

# Manually apply setup to current directory
claude_setup_repo

# Auto-setup triggers when cd'ing into unconfigured repos in ~/repos
cd ~/repos/any-new-repo  # Automatically applies Claude setup
```

#### Prompt Distribution (Legacy/Manual)
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

### Setup Prompt
See `.github/prompts/setup_claude_auto_awareness.prompt.md` for complete system setup instructions (v2.0 - macOS/Ubuntu compatible).

## Repository Architecture

This is a **Prompt Library** for DevOps automation that distributes AI prompts and coding rules to other repositories. The architecture follows a distribution model where content is authored centrally and deployed to target projects.

### Core Components

**Prompt System** (`.github/prompts/`): 56 prompt files organized by technology stack with advanced AI engineering
- **Analysis prompts**: `analyze_*.prompt.md` - Audit existing infrastructure/code with evidence-based validation
- **Build prompts**: `build_*.prompt.md` - Scaffold new projects from scratch with security-first patterns  
- **Recon prompts**: `recon_*.prompt.md` - Discovery and enumeration tasks with smart scope management
- **Specialized directories**: `terraform/`, for focused workflows

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

### AI Prompt Engineering Integration

Every prompt includes advanced engineering patterns for maximum effectiveness:

**Core Safety Framework**:
- **Permission handling**: Ask for permission before file modifications with single confirmation flow
- **Branch safety**: Require explicit branch selection for repository changes with sync validation  
- **Security guidance**: Mask secrets in output, promote secure credential handling

**Context Management System**:
- **Smart scope adjustment**: Prioritize security-critical items when complexity exceeds capacity
- **Domain-specific prioritization**: Tailored focus areas for each technology stack (security, performance, integration)
- **Progressive disclosure**: Break overwhelming scenarios into manageable phases with user control

**Analysis Validation Framework**:
- **Evidence-based classification**: Mark all findings as "Confirmed" vs "Potential" with supporting evidence
- **Confidence indicators**: Provide High/Medium/Low ratings for each recommendation with reasoning
- **Specific referencing**: Require citations of actual configurations, files, or settings
- **Access enhancement guidance**: Suggest additional access or tools to improve analysis accuracy

### VS Code Integration

The repository includes VS Code settings (`.vscode/settings.json`) with:
- Chat prompt files enabled for easy prompt testing and development

## Key Patterns

**Prompt Structure**: All prompts follow consistent formatting with security best practices, branch management directives, and structured output requirements.

**Rule Application**: Rules files (`.mdc`) are automatically applied based on file patterns and technology detection in target repositories.

**Technology Coverage**: Comprehensive coverage of DevOps stack including Kubernetes, Terraform, CI/CD platforms (GitHub Actions, GitLab, Jenkins, Bitbucket), cloud providers (AWS, Azure), and monitoring tools (Prometheus, Grafana).