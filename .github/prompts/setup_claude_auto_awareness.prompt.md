---
title: "Setup Claude Auto-Awareness System"
description: "Implement comprehensive Claude auto-awareness across all repositories with document standards, prompt library, and branch management"
category: "Development Environment Setup"
priority: "High"
use_case: "Initial system setup, new development machines, team onboarding"
version: "2.0.0"
compatibility: "macOS, Ubuntu Linux"
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

**IMPORTANT**: Git templates copy files into `.git/` directory only. Shell integration is required to apply Claude setup to the working tree when entering repositories.

## IMPLEMENTATION STEPS

### Phase 1: Detect and Verify Core Repositories

First, detect and verify the required source repositories with flexible path support:

```bash
# Detect prompt library location (supports multiple common paths)
PROMPT_LIB=""
POSSIBLE_PATHS=(
    "$HOME/repos/prompt-library"
    "$HOME/repos/daryls_rules/prompt-library"
    "$HOME/workspace/prompt-library"
    "$HOME/projects/prompt-library"
)

for path in "${POSSIBLE_PATHS[@]}"; do
    if [[ -d "$path" ]]; then
        PROMPT_LIB="$path"
        echo "✅ Found prompt library at: $PROMPT_LIB"
        break
    fi
done

if [[ -z "$PROMPT_LIB" ]]; then
    echo "❌ MISSING: Prompt library repository"
    echo "📋 ACTION: Create the prompt library repository"
    echo "   Supported locations:"
    for path in "${POSSIBLE_PATHS[@]}"; do
        echo "   - $path"
    done
    echo ""
    echo "   Expected structure:"
    echo "   <prompt-library>/"
    echo "   ├── .github/prompts/     # AI prompts"
    echo "   ├── .rules/              # Coding conventions"
    echo "   ├── copy-prompts.sh      # Distribution script"
    echo "   └── README.md"
    exit 1
fi

# Detect document standards location
DOC_STANDARDS=""
POSSIBLE_DOC_PATHS=(
    "$HOME/repos/document_standard"
    "$HOME/repos/document-standards"
    "$HOME/repos/doc-standards"
    "$HOME/workspace/document_standard"
)

for path in "${POSSIBLE_DOC_PATHS[@]}"; do
    if [[ -d "$path" ]]; then
        DOC_STANDARDS="$path"
        echo "✅ Found document standards at: $DOC_STANDARDS"
        break
    fi
done

if [[ -z "$DOC_STANDARDS" ]]; then
    echo "❌ MISSING: Document standards repository"
    echo "📋 ACTION: Create the document standards repository"
    echo "   Supported locations:"
    for path in "${POSSIBLE_DOC_PATHS[@]}"; do
        echo "   - $path"
    done
    echo ""
    echo "   Expected structure:"
    echo "   <document_standard>/"
    echo "   ├── templates/           # Document templates"
    echo "   ├── checklists/          # QA checklists"
    echo "   ├── examples/            # Best practices"
    echo "   └── README.md"
    exit 1
fi

# Export for use in later phases
export PROMPT_LIB
export DOC_STANDARDS

echo ""
echo "📊 Configuration detected:"
echo "   Prompt Library: $PROMPT_LIB"
echo "   Doc Standards:  $DOC_STANDARDS"
echo ""
```

**If repositories are missing**, create minimal structures:

```bash
# Create Prompt Library (adjust path as needed)
mkdir -p ~/repos/prompt-library/{.github/prompts,.rules}
cat > ~/repos/prompt-library/README.md << 'EOF'
# Prompt Library
Centralized AI prompts and coding rules for consistent development workflows.
EOF

# Create Document Standards
mkdir -p ~/repos/document_standard/{templates,checklists,examples}
cat > ~/repos/document_standard/README.md << 'EOF'
# Documentation Standards
Centralized document templates and standards for consistent project documentation.
EOF
```

### Phase 2: Create Git Template Structure

```bash
# Use detected paths from Phase 1
PROMPT_LIB="${PROMPT_LIB:-$HOME/repos/prompt-library}"
DOC_STANDARDS="${DOC_STANDARDS:-$HOME/repos/document_standard}"

# Create git template directory
mkdir -p ~/.git_template/{.claude,.github/prompts,.rules,.doc_standards}

# Create Claude settings with branch prompting and permissions
cat > ~/.git_template/.claude/settings.local.json << EOF
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
      "command": "echo '🌿 Current branch: '\$(git branch --show-current 2>/dev/null || echo 'not in git repo')",
      "description": "Show current git branch before Claude responds"
    }
  },
  "global_resources": {
    "document_standards": "$DOC_STANDARDS",
    "prompt_library": "$PROMPT_LIB",
    "description": "Central locations for standards and prompts"
  },
  "workflow_reminders": {
    "branch_check": "🚨 IMPORTANT: Before starting development work, check if you need a new feature branch!",
    "standards_available": "📚 Document templates available at .doc_standards/ or $DOC_STANDARDS/templates/",
    "prompts_available": "🤖 AI prompts available in .github/prompts/ directory"
  }
}
EOF

# Set proper permissions
chmod 600 ~/.git_template/.claude/settings.local.json

echo "✅ Git template structure created"
```

### Phase 3: Create Resource Symlinks

```bash
# Use detected paths from Phase 1
PROMPT_LIB="${PROMPT_LIB:-$HOME/repos/prompt-library}"
DOC_STANDARDS="${DOC_STANDARDS:-$HOME/repos/document_standard}"

echo "🔗 Creating symlinks to central resources..."

# Link prompts from central library (handles all .md files robustly)
echo "  Linking prompts..."
TEMPLATE_PROMPTS="$HOME/.git_template/.github/prompts"
mkdir -p "$TEMPLATE_PROMPTS"

if [[ -d "$PROMPT_LIB/.github/prompts" ]]; then
    # Find all markdown files and create symlinks
    find "$PROMPT_LIB/.github/prompts" -maxdepth 1 -type f -name "*.md" \
        -exec ln -sf {} "$TEMPLATE_PROMPTS/" \; 2>/dev/null

    PROMPT_COUNT=$(find "$TEMPLATE_PROMPTS" -type l | wc -l | tr -d ' ')
    echo "    ✅ Linked $PROMPT_COUNT prompt files"
else
    echo "    ⚠️  No prompts directory found at $PROMPT_LIB/.github/prompts"
fi

# Link coding rules (handles .mdc files and subdirectories)
echo "  Linking coding rules..."
TEMPLATE_RULES="$HOME/.git_template/.rules"
mkdir -p "$TEMPLATE_RULES"

if [[ -d "$PROMPT_LIB/.rules" ]]; then
    # Link .mdc files
    find "$PROMPT_LIB/.rules" -maxdepth 1 -type f -name "*.mdc" \
        -exec ln -sf {} "$TEMPLATE_RULES/" \; 2>/dev/null

    # Link subdirectories (workflows, assets, etc.)
    find "$PROMPT_LIB/.rules" -maxdepth 1 -type d ! -name ".rules" \
        -exec ln -sf {} "$TEMPLATE_RULES/" \; 2>/dev/null

    RULE_COUNT=$(find "$TEMPLATE_RULES" -maxdepth 1 \( -type f -o -type l \) | wc -l | tr -d ' ')
    echo "    ✅ Linked $RULE_COUNT rule files/directories"
else
    echo "    ⚠️  No rules directory found at $PROMPT_LIB/.rules"
fi

# Link document standards
echo "  Linking document standards..."
TEMPLATE_DOCS="$HOME/.git_template/.doc_standards"
mkdir -p "$TEMPLATE_DOCS"

if [[ -d "$DOC_STANDARDS" ]]; then
    # Link each subdirectory individually
    for subdir in templates checklists examples config; do
        if [[ -d "$DOC_STANDARDS/$subdir" ]]; then
            ln -sf "$DOC_STANDARDS/$subdir" "$TEMPLATE_DOCS/" 2>/dev/null
            echo "    ✅ Linked $subdir/"
        fi
    done
else
    echo "    ⚠️  Document standards directory not found at $DOC_STANDARDS"
fi

echo "✅ Resource symlinks created"
```

### Phase 4: Configure Git Globally

```bash
# Configure git to use the template directory for all new repos
git config --global init.templatedir ~/.git_template

echo "✅ Git configured to use template directory"
echo "   Note: Template files are copied to .git/ directory only."
echo "   Shell integration (Phase 6) applies setup to working tree."
```

### Phase 5: Create Auto-Setup Script

```bash
cat > ~/repos/claude_auto_setup.sh << 'EOSCRIPT'
#!/bin/bash
# Claude Auto-Setup Script - Apply to existing repositories
# Compatible with macOS and Ubuntu Linux

set -euo pipefail

REPOS_DIR="$HOME/repos"
GIT_TEMPLATE_DIR="$HOME/.git_template"

apply_to_repo() {
    local repo_dir="$1"
    local repo_name="$(basename "$repo_dir")"

    if [[ ! -d "$repo_dir/.git" ]]; then
        echo "⚠️  Skipping $repo_name (not a git repository)"
        return 1
    fi

    echo "🔧 Applying Claude setup to: $repo_name"

    # Copy Claude configuration
    mkdir -p "$repo_dir/.claude"
    cp "$GIT_TEMPLATE_DIR/.claude/settings.local.json" "$repo_dir/.claude/" 2>/dev/null || {
        echo "   ⚠️  Warning: Could not copy Claude settings"
    }

    # Create symlinks to central resources
    mkdir -p "$repo_dir/.github/prompts" "$repo_dir/.rules" "$repo_dir/.doc_standards"

    # Link prompts (using find for robustness)
    if [[ -d "$GIT_TEMPLATE_DIR/.github/prompts" ]]; then
        find "$GIT_TEMPLATE_DIR/.github/prompts" -maxdepth 1 -type f -o -type l \
            -exec ln -sf {} "$repo_dir/.github/prompts/" \; 2>/dev/null || true
    fi

    # Link rules files
    if [[ -d "$GIT_TEMPLATE_DIR/.rules" ]]; then
        # Link .mdc files
        find "$GIT_TEMPLATE_DIR/.rules" -maxdepth 1 -type f -name "*.mdc" \
            -exec ln -sf {} "$repo_dir/.rules/" \; 2>/dev/null || true

        # Link subdirectories (workflows, assets, etc.)
        find "$GIT_TEMPLATE_DIR/.rules" -maxdepth 1 -type d ! -name ".rules" \
            -exec ln -sf {} "$repo_dir/.rules/" \; 2>/dev/null || true
    fi

    # Link document standards
    if [[ -d "$GIT_TEMPLATE_DIR/.doc_standards" ]]; then
        find "$GIT_TEMPLATE_DIR/.doc_standards" -maxdepth 1 \( -type d -o -type l \) ! -name ".doc_standards" \
            -exec ln -sf {} "$repo_dir/.doc_standards/" \; 2>/dev/null || true
    fi

    # Update .gitignore
    local gitignore="$repo_dir/.gitignore"
    touch "$gitignore"

    local ignore_entries=(".doc_standards/" ".claude/")
    for entry in "${ignore_entries[@]}"; do
        if ! grep -qF "$entry" "$gitignore" 2>/dev/null; then
            echo "$entry" >> "$gitignore"
        fi
    done

    echo "✅ Claude setup applied to $repo_name"
}

case "${1:-}" in
    "apply_single")
        if [[ -z "${2:-}" ]]; then
            echo "Usage: $0 apply_single <repo_path>"
            exit 1
        fi
        apply_to_repo "$2"
        ;;
    "apply_all")
        echo "🚀 Applying Claude setup to all repositories..."
        count=0
        if [[ ! -d "$REPOS_DIR" ]]; then
            echo "❌ Repositories directory not found: $REPOS_DIR"
            exit 1
        fi

        for repo_dir in "$REPOS_DIR"/*/; do
            repo_dir="${repo_dir%/}"
            repo_name="$(basename "$repo_dir")"

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
            echo "❌ Git template not found at $GIT_TEMPLATE_DIR"
        fi

        if git config --global --get init.templatedir | grep -q "$GIT_TEMPLATE_DIR"; then
            echo "✅ Git configured to use template"
        else
            echo "❌ Git not configured to use template"
        fi

        echo ""
        echo "📊 Template Resources:"
        if [[ -d "$GIT_TEMPLATE_DIR/.github/prompts" ]]; then
            PROMPT_COUNT=$(find "$GIT_TEMPLATE_DIR/.github/prompts" -type f -o -type l 2>/dev/null | wc -l | tr -d ' ')
            echo "  Prompts: $PROMPT_COUNT"
        else
            echo "  Prompts: 0 (directory missing)"
        fi

        if [[ -d "$GIT_TEMPLATE_DIR/.rules" ]]; then
            RULE_COUNT=$(find "$GIT_TEMPLATE_DIR/.rules" -maxdepth 1 \( -type f -o -type l \) 2>/dev/null | wc -l | tr -d ' ')
            echo "  Rules: $RULE_COUNT"
        else
            echo "  Rules: 0 (directory missing)"
        fi

        if [[ -d "$GIT_TEMPLATE_DIR/.doc_standards" ]]; then
            DOC_COUNT=$(ls -1 "$GIT_TEMPLATE_DIR/.doc_standards" 2>/dev/null | wc -l | tr -d ' ')
            echo "  Doc Standards: $DOC_COUNT directories"
        else
            echo "  Doc Standards: 0 (directory missing)"
        fi
        ;;
    *)
        echo "Claude Auto-Setup Script"
        echo ""
        echo "Usage: $0 [COMMAND]"
        echo ""
        echo "Commands:"
        echo "  apply_single <repo_path>  Apply Claude setup to a specific repository"
        echo "  apply_all                 Apply Claude setup to all repositories in ~/repos"
        echo "  test                      Test the configuration"
        echo ""
        echo "Examples:"
        echo "  $0 apply_single ~/repos/my-project"
        echo "  $0 apply_all"
        echo "  $0 test"
        exit 1
        ;;
esac
EOSCRIPT

chmod +x ~/repos/claude_auto_setup.sh

echo "✅ Auto-setup script created at ~/repos/claude_auto_setup.sh"
```

### Phase 6: Setup Shell Integration

**Detects shell type automatically (bash/zsh) for macOS and Ubuntu compatibility:**

```bash
# Detect shell type and appropriate rc file
RC_FILE=""
SHELL_TYPE=""

# Check for zsh (default on macOS since Catalina, common on Linux)
if [[ -n "$ZSH_VERSION" ]] || [[ "$SHELL" == */zsh ]]; then
    SHELL_TYPE="zsh"
    RC_FILE="$HOME/.zshrc"
    [[ ! -f "$RC_FILE" ]] && touch "$RC_FILE"
# Check for bash
elif [[ -n "$BASH_VERSION" ]] || [[ "$SHELL" == */bash ]]; then
    SHELL_TYPE="bash"
    # Ubuntu/Linux typically uses .bashrc, macOS uses .bash_profile
    if [[ -f "$HOME/.bashrc" ]]; then
        RC_FILE="$HOME/.bashrc"
    elif [[ -f "$HOME/.bash_profile" ]]; then
        RC_FILE="$HOME/.bash_profile"
    else
        RC_FILE="$HOME/.bashrc"
        touch "$RC_FILE"
    fi
else
    echo "⚠️  Could not detect shell type. Please add shell functions manually."
    echo "   Supported shells: bash, zsh"
    exit 1
fi

echo "🐚 Detected shell: $SHELL_TYPE"
echo "📝 Adding functions to: $RC_FILE"

# Check if functions already exist
if grep -q "# Claude Auto-Setup Functions" "$RC_FILE" 2>/dev/null; then
    echo "⚠️  Shell integration already exists in $RC_FILE"
    echo "   Skipping to avoid duplicates. Remove existing section to reinstall."
else
    # Add shell functions for automatic setup
    cat >> "$RC_FILE" << 'EOF'

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

    echo "✅ Shell integration added to $RC_FILE"
    echo ""
    echo "⚠️  IMPORTANT: Restart your shell or run:"
    echo "   source $RC_FILE"
fi
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

# IMPORTANT: Git init does NOT automatically apply Claude setup to working tree
# The git template only copies files into .git/ directory
# Shell integration (cd hook) applies the setup when you enter the repository

# Test new repository creation with shell integration
mkdir -p /tmp/test-claude-setup
cd /tmp/test-claude-setup
git init
# Wait for shell cd() hook to apply setup (if in ~/repos)
# OR manually apply: ~/repos/claude_auto_setup.sh apply_single .

# Verify structure exists
ls -la .claude/ .github/prompts/ .rules/ .doc_standards/

# Clean up test
cd /tmp
rm -rf test-claude-setup
```

## EXPECTED RESULTS

After implementation, every repository will have:

**🤖 Claude Configuration** (`.claude/settings.local.json`):
- Automatic branch display via hook
- Branch creation prompting (asks before creating branches)
- Secure git operation permissions
- Pre-approved safe operations (status, diff, log)
- Confirmation required for destructive operations (merge, rebase, rm)

**📚 Document Standards** (`.doc_standards/`):
- README, API, Architecture templates
- Quality assurance checklists
- Best practice examples
- Tool configurations (if available)

**🎯 AI Prompts** (`.github/prompts/`):
- 50+ specialized prompts for analysis and building
- Technology-specific prompts (AKS, Terraform, Python, etc.)
- Investigation and discovery workflows

**📋 Coding Rules** (`.rules/`):
- Language-specific conventions (python.mdc, typescript.mdc, etc.)
- Framework guidelines (nextjs-app-router.mdc, ruby-on-rails.mdc, etc.)
- Workflow patterns (refactoring, testing, API design)

## TROUBLESHOOTING

**"Missing prompt library"**:
- Check supported paths: `~/repos/prompt-library/` or `~/repos/daryls_rules/prompt-library/`
- Verify directory exists: `ls -la ~/repos/prompt-library/`
- Re-run Phase 1 to detect paths

**"Git template not working"**:
- Check configuration: `git config --global --get init.templatedir`
- Verify directory exists: `ls -la ~/.git_template`
- Remember: Git template copies to `.git/` only, not working tree
- Shell integration (Phase 6) applies setup to working tree

**"Symlinks broken"**:
- Check source exists: `ls -la ~/repos/prompt-library/`
- Verify template symlinks: `ls -la ~/.git_template/.github/prompts/`
- Re-run Phase 3 to recreate links
- Use absolute paths (script handles this automatically)

**"Shell functions not working"**:
- Verify shell type: `echo $SHELL`
- Check rc file: `cat ~/.zshrc` or `cat ~/.bashrc`
- Look for "# Claude Auto-Setup Functions" section
- Source the file: `source ~/.zshrc` or `source ~/.bashrc`

**"Permissions errors"**:
- Check template permissions: `ls -la ~/.git_template/.claude/`
- Settings should be: `-rw------- settings.local.json`
- Fix if needed: `chmod 600 ~/.git_template/.claude/settings.local.json`

**"Works on Mac but not Ubuntu" or vice versa**:
- Verify path detection in Phase 1
- Check shell detection in Phase 6
- Ensure `find` and `ln` commands are available (should be standard)
- Check if `~/repos` directory exists

## MAINTENANCE

**Adding New Prompts**:
Add to central prompt library at `~/repos/prompt-library/.github/prompts/`, then re-run Phase 3 to update symlinks.

**Updating Standards**:
Modify central document standards at `~/repos/document_standard/`, changes reflect everywhere automatically via symlinks.

**New Repositories**:
- Use `gitclone` instead of `git clone` for automatic setup
- Or enter the repository directory and `cd` hook will apply setup (if in ~/repos)
- Or manually apply: `~/repos/claude_auto_setup.sh apply_single /path/to/repo`

**Update Existing Repositories**:
Re-run: `~/repos/claude_auto_setup.sh apply_all`

## SUCCESS CRITERIA

✅ System detects prompt library and document standards automatically
✅ Works on both macOS and Ubuntu without modification
✅ Shell integration works for bash and zsh
✅ New repositories automatically include Claude configuration
✅ Claude shows current branch in every session
✅ Claude prompts before creating new branches
✅ Document templates accessible in all repositories
✅ AI prompts available for specialized tasks
✅ Coding rules (including subdirectories) applied consistently
✅ Central maintenance with distributed access via symlinks
✅ Robust error handling for missing directories

**Result**: Claude has automatic awareness of your standards and tools across all development work without manual intervention, working seamlessly on macOS and Ubuntu workstations.
