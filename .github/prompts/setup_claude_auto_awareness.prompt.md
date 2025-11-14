---
title: "Setup Claude Auto-Awareness System"
description: "Implement comprehensive Claude auto-awareness across all repositories with document standards, prompt library, and branch management"
category: "Development Environment Setup"
priority: "High"
use_case: "Initial system setup, new development machines, team onboarding"
---

# Setup Claude Auto-Awareness System

You are Claude Code helping to implement a comprehensive auto-awareness system that makes document standards, prompt libraries, and coding rules automatically available in every repository session without manual scripts.

## OBJECTIVE

Implement a system where Claude automatically has access to:
- **Document Standards**: Templates, checklists, examples, configurations
- **Prompt Library**: 50+ specialized AI prompts for DevOps tasks
- **Coding Rules**: Language-specific conventions and workflow patterns
- **Branch Management**: Automatic prompting for branch creation and git operations

## SYSTEM ARCHITECTURE

The system uses:
1. **Git Template Directory**: Automatic inclusion in all new repositories
2. **Symlink-Based Resources**: Central maintenance with distributed access
3. **Shell Integration**: Auto-setup for new repositories and git operations
4. **Claude Settings**: Consistent permissions and workflow reminders

## IMPLEMENTATION STEPS

### Phase 1: Verify/Create Core Repositories

First, check for and create the required source repositories:

```bash
# Check for prompt library (required)
if [ ! -d "~/repos/daryls_rules/prompt-library" ]; then
    echo "❌ MISSING: Prompt library repository"
    echo "📋 ACTION: Create or clone the prompt library repository"
    echo "   Expected structure:"
    echo "   ~/repos/daryls_rules/prompt-library/"
    echo "   ├── .github/prompts/     # AI prompts"
    echo "   ├── .rules/              # Coding conventions"
    echo "   ├── copy-prompts.sh      # Distribution script"
    echo "   └── README.md"
    exit 1
fi

# Check for document standards (required)
if [ ! -d "~/repos/document_standard" ]; then
    echo "❌ MISSING: Document standards repository"
    echo "📋 ACTION: Create or clone the document standards repository"
    echo "   Expected structure:"
    echo "   ~/repos/document_standard/"
    echo "   ├── templates/           # Document templates"
    echo "   ├── checklists/          # QA checklists"
    echo "   ├── examples/            # Best practices"
    echo "   ├── config/              # Tool configurations"
    echo "   └── README.md"
    exit 1
fi
```

**If repositories are missing**, create minimal structures:

**Create Prompt Library:**
```bash
mkdir -p ~/repos/daryls_rules/prompt-library/{.github/prompts,.rules}
cat > ~/repos/daryls_rules/prompt-library/README.md << 'EOF'
# Prompt Library
Centralized AI prompts and coding rules for consistent development workflows.
EOF
```

**Create Document Standards:**
```bash
mkdir -p ~/repos/document_standard/{templates,checklists,examples,config}
cat > ~/repos/document_standard/README.md << 'EOF'
# Documentation Standards
Centralized document templates and standards for consistent project documentation.
EOF
```

### Phase 2: Create Git Template Structure

```bash
# Create git template directory
mkdir -p ~/.git_template/{.claude,.github/prompts,.rules,.doc_standards}

# Create Claude settings with branch prompting and permissions
cat > ~/.git_template/.claude/settings.local.json << 'EOF'
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(git branch:*)",
      "Bash(git checkout:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git pull:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(mkdir:*)",
      "Bash(tree:*)",
      "Bash(find:*)",
      "WebSearch"
    ],
    "deny": [],
    "ask": [
      "Bash(git checkout -b:*)",
      "Bash(git merge:*)",
      "Bash(git rebase:*)",
      "Bash(rm:*)"
    ]
  },
  "hooks": {
    "user-prompt-submit": {
      "command": "echo '🌿 Current branch: '$(git branch --show-current 2>/dev/null || echo 'not in git repo')",
      "description": "Show current git branch before Claude responds"
    }
  },
  "global_resources": {
    "document_standards": "~/repos/document_standard",
    "prompt_library": "~/repos/daryls_rules/prompt-library",
    "description": "Central locations for standards and prompts"
  },
  "workflow_reminders": {
    "branch_check": "🚨 IMPORTANT: Before starting development work, check if you need a new feature branch!",
    "standards_available": "📚 Document templates available at .doc_standards/ or ~/repos/document_standard/templates/",
    "prompts_available": "🤖 AI prompts available in .github/prompts/ directory"
  }
}
EOF

# Set proper permissions
chmod 600 ~/.git_template/.claude/settings.local.json
```

### Phase 3: Create Resource Symlinks

```bash
# Link prompts from central library
cd ~/.git_template/.github/prompts
for file in ~/repos/daryls_rules/prompt-library/.github/prompts/*.md; do
    [ -f "$file" ] && ln -sf "$file" "./$(basename "$file")"
done

# Link coding rules
cd ~/.git_template/.rules
for file in ~/repos/daryls_rules/prompt-library/.rules/*.mdc; do
    [ -f "$file" ] && ln -sf "$file" "./$(basename "$file")"
done

# Link document standards
cd ~/.git_template/.doc_standards
ln -sf ~/repos/document_standard/templates templates
ln -sf ~/repos/document_standard/checklists checklists
ln -sf ~/repos/document_standard/examples examples
ln -sf ~/repos/document_standard/config config
```

### Phase 4: Configure Git Globally

```bash
# Configure git to use the template directory for all new repos
git config --global init.templatedir ~/.git_template

echo "✅ Git configured to automatically include Claude setup in new repositories"
```

### Phase 5: Create Auto-Setup Script

```bash
cat > ~/repos/claude_auto_setup.sh << 'EOSCRIPT'
#!/bin/bash
# Claude Auto-Setup Script - Apply to existing repositories

set -euo pipefail

REPOS_DIR="$HOME/repos"
GIT_TEMPLATE_DIR="$HOME/.git_template"

apply_to_repo() {
    local repo_dir="$1"
    local repo_name="$(basename "$repo_dir")"

    if [[ ! -d "$repo_dir/.git" ]]; then
        echo "⚠️ Skipping $repo_name (not a git repository)"
        return 1
    fi

    echo "🔧 Applying Claude setup to: $repo_name"

    # Copy Claude configuration
    mkdir -p "$repo_dir/.claude"
    cp "$GIT_TEMPLATE_DIR/.claude/settings.local.json" "$repo_dir/.claude/"

    # Create symlinks to central resources
    mkdir -p "$repo_dir/.github/prompts" "$repo_dir/.rules" "$repo_dir/.doc_standards"

    # Link prompts (if not already existing)
    if [[ ! -f "$repo_dir/.github/prompts/analyze_codebase.prompt.md" ]]; then
        for prompt in "$GIT_TEMPLATE_DIR/.github/prompts"/*.md; do
            [[ -f "$prompt" ]] && ln -sf "$prompt" "$repo_dir/.github/prompts/"
        done
    fi

    # Link rules
    for rule in "$GIT_TEMPLATE_DIR/.rules"/*.mdc; do
        [[ -f "$rule" ]] && ln -sf "$rule" "$repo_dir/.rules/"
    done

    # Link document standards
    for std in "$GIT_TEMPLATE_DIR/.doc_standards"/*; do
        [[ -e "$std" ]] && ln -sf "$std" "$repo_dir/.doc_standards/"
    done

    # Update .gitignore
    local gitignore="$repo_dir/.gitignore"
    touch "$gitignore"

    local ignore_entries=(".doc_standards/" ".claude/" ".rules/")
    for entry in "${ignore_entries[@]}"; do
        if ! grep -qF "$entry" "$gitignore"; then
            echo "$entry" >> "$gitignore"
        fi
    done

    echo "✅ Claude setup applied to $repo_name"
}

case "${1:-setup}" in
    "apply_single")
        apply_to_repo "$2"
        ;;
    "apply_all")
        echo "🚀 Applying Claude setup to all repositories..."
        count=0
        for repo_dir in "$REPOS_DIR"/*/; do
            repo_dir="${repo_dir%/}"
            local repo_name="$(basename "$repo_dir")"

            # Skip excluded directories
            [[ "$repo_name" == "ARCHIVE" ]] && continue

            if apply_to_repo "$repo_dir"; then
                count=$((count + 1))
            fi
        done
        echo "✅ Applied Claude setup to $count repositories"
        ;;
    "test")
        echo "🔍 Testing configuration..."
        if [[ -f "$GIT_TEMPLATE_DIR/.claude/settings.local.json" ]]; then
            echo "✅ Git template configured correctly"
        else
            echo "❌ Git template not found"
        fi

        if git config --global --get init.templatedir | grep -q "$GIT_TEMPLATE_DIR"; then
            echo "✅ Git configured to use template"
        else
            echo "❌ Git not configured to use template"
        fi
        ;;
    *)
        echo "Usage: $0 [apply_single <repo_path>|apply_all|test]"
        echo "Examples:"
        echo "  $0 apply_single ~/repos/my-project"
        echo "  $0 apply_all"
        echo "  $0 test"
        exit 1
        ;;
esac
EOSCRIPT

chmod +x ~/repos/claude_auto_setup.sh
```

### Phase 6: Setup Shell Integration

```bash
# Add shell functions for automatic setup
cat >> ~/.bashrc << 'EOF'

# Claude Auto-Setup Functions
claude_setup_repo() {
    local repo_path="${1:-$PWD}"
    if [[ -f "$HOME/.git_template/.claude/settings.local.json" ]] && [[ -d "$repo_path/.git" ]]; then
        bash "$HOME/repos/claude_auto_setup.sh" apply_single "$repo_path"
    fi
}

# Automatic git clone wrapper that applies Claude setup
gitclone() {
    git clone "$@"
    local repo_name=$(basename "${!#}" .git)
    if [[ -d "$repo_name" ]]; then
        echo "🤖 Applying Claude setup to new repository..."
        claude_setup_repo "$repo_name"
    fi
}

# Auto-setup when entering a new git repository in ~/repos
cd() {
    builtin cd "$@"
    if [[ -d .git ]] && [[ ! -f .claude/settings.local.json ]] && [[ $PWD == $HOME/repos/* ]]; then
        echo "🤖 New git repository detected. Applying Claude setup..."
        claude_setup_repo
    fi
}

EOF

echo "✅ Shell integration added. Restart your shell or run: source ~/.bashrc"
```

### Phase 7: Apply to Existing Repositories

```bash
# Apply setup to all existing repositories
~/repos/claude_auto_setup.sh apply_all
```

## VERIFICATION

Test the setup:

```bash
# Test configuration
~/repos/claude_auto_setup.sh test

# Test new repository creation
mkdir test-claude-setup
cd test-claude-setup
git init
# Should automatically apply Claude setup

# Verify structure exists
ls -la .claude/ .github/prompts/ .rules/ .doc_standards/

# Clean up test
cd ..
rm -rf test-claude-setup
```

## EXPECTED RESULTS

After implementation, every repository will have:

**🤖 Claude Configuration** (`.claude/settings.local.json`):
- Automatic branch display
- Branch creation prompting
- Secure git operation permissions

**📚 Document Standards** (`.doc_standards/`):
- README, API, Architecture templates
- Quality assurance checklists
- Best practice examples
- Tool configurations

**🎯 AI Prompts** (`.github/prompts/`):
- 50+ specialized prompts for analysis and building
- Technology-specific prompts (AKS, Terraform, Python, etc.)
- Investigation and discovery workflows

**📋 Coding Rules** (`.rules/`):
- Language-specific conventions
- Framework guidelines
- Workflow patterns

## TROUBLESHOOTING

**"Missing prompt library"**:
- Ensure ~/repos/daryls_rules/prompt-library exists
- Check symlinks are pointing to correct locations
- Verify file permissions

**"Git template not working"**:
- Check `git config --global --get init.templatedir`
- Verify ~/.git_template directory exists
- Test with new repository creation

**"Symlinks broken"**:
- Update symlink paths if repositories moved
- Re-run Phase 3 to recreate links
- Check source directories exist

## MAINTENANCE

**Adding New Prompts**: Add to central prompt library, symlinks update automatically
**Updating Standards**: Modify central document standards, changes reflect everywhere
**New Repositories**: Use `gitclone` instead of `git clone` for auto-setup

## SUCCESS CRITERIA

✅ New repositories automatically include Claude configuration
✅ Claude shows current branch in every session
✅ Claude prompts before creating new branches
✅ Document templates accessible in all repositories
✅ AI prompts available for specialized tasks
✅ Coding rules applied consistently
✅ Central maintenance with distributed access

**Result**: Claude has automatic awareness of your standards and tools across all development work without manual intervention.