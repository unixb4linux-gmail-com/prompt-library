#!/bin/bash

# Enhanced copy-prompts.sh with robust argument parsing, quoting, error handling, and shellcheck compliance
DRY_RUN=false
VERBOSE=false
CONFIRM_OVERWRITE=true
INCLUDE_GITIGNORE_PROMPTS=true
COPY_GITIGNORE_TEMPLATES=false
AUTO_DETECT_PROJECT=false
PROJECT_TYPE=""
TARGET_DIR=""

usage() {
  cat <<EOF
Usage: $0 [OPTIONS] /path/to/target-repo

OPTIONS:
  -n, --dry-run              Preview changes without actually copying files
  -v, --verbose              Show detailed output
  --no-gitignore-prompts     Skip adding .github/prompts/ to .gitignore
  --with-gitignore           Copy .gitignore templates to target repository
  --auto-detect              Auto-detect project type for .gitignore templates
  --type TYPE                Specify project type (python, nodejs, go, java, ruby, dotnet, terraform, chef)
  -h, --help                 Show this help message

EXAMPLES:
  # Basic usage - copy prompts and rules only
  $0 /path/to/target-repo

  # Copy with .gitignore templates (auto-detect project type)
  $0 --with-gitignore --auto-detect /path/to/target-repo

  # Copy with specific project type
  $0 --with-gitignore --type python /path/to/target-repo

  # Preview changes without modifying files
  $0 -n --with-gitignore --auto-detect /path/to/target-repo

  # Verbose output with .gitignore templates
  $0 -v --with-gitignore --type terraform /path/to/target-repo
EOF
  exit 1
}

# Parse options

while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--dry-run) DRY_RUN=true ; shift ;;
    -v|--verbose) VERBOSE=true ; shift ;;
    --no-gitignore-prompts) INCLUDE_GITIGNORE_PROMPTS=false ; shift ;;
    --with-gitignore) COPY_GITIGNORE_TEMPLATES=true ; shift ;;
    --auto-detect) AUTO_DETECT_PROJECT=true ; shift ;;
    --type)
      if [[ -z "$2" ]] || [[ "$2" == -* ]]; then
        echo "Error: --type requires a value" >&2
        usage
      fi
      PROJECT_TYPE="$2"
      shift 2
      ;;
    -h|--help) usage ;;
    --) shift ; break ;;
    -*) usage ;;
    *) TARGET_DIR="$1" ; shift ;;
  esac
  if [[ -n "$TARGET_DIR" ]]; then break; fi
done

if [[ -z "$TARGET_DIR" ]]; then
  usage
fi

if [ "$VERBOSE" = true ]; then
  echo "Target directory: $TARGET_DIR"
  echo "Dry run: $DRY_RUN"
  echo "Verbose: $VERBOSE"
  echo "Confirm overwrite: $CONFIRM_OVERWRITE"
  echo "Include .github/prompts in .gitignore: $INCLUDE_GITIGNORE_PROMPTS"
  echo "Copy .gitignore templates: $COPY_GITIGNORE_TEMPLATES"
  echo "Auto-detect project type: $AUTO_DETECT_PROJECT"
  echo "Project type: ${PROJECT_TYPE:-auto}"
fi

copy_file() {
  local src="$1"
  local dest="$2"
  # Remove existing file or directory before copying
  if [[ -e "$dest" ]]; then
    rm -rf "$dest"
    [ "$VERBOSE" = true ] && echo "Removed existing $dest"
  fi
  if [ "$DRY_RUN" = true ]; then
    echo "[DRY RUN] Would copy $src to $dest"
  else
    cp -r "$src" "$dest"
    if [[ $? -ne 0 ]]; then
      echo "Error copying $src to $dest" >&2
      return 1
    fi
    [ "$VERBOSE" = true ] && echo "Copied $src to $dest"
  fi
}

# Copy prompts
mkdir -p "$TARGET_DIR/.github/prompts"
find . -type f -name '*.prompt.md' -print0 | while IFS= read -r -d '' f; do
  copy_file "$f" "$TARGET_DIR/.github/prompts/$(basename "$f")"
done

# Copy rules
mkdir -p "$TARGET_DIR/.rules"
find .rules -type f -name '*.mdc' -print0 | while IFS= read -r -d '' f; do
  copy_file "$f" "$TARGET_DIR/.rules/$(basename "$f")"
done

# Copy .vscode directory if it exists
if [ -d ".vscode" ]; then
  if [ "$DRY_RUN" = true ]; then
    echo "[DRY RUN] Would copy .vscode directory to $TARGET_DIR/.vscode"
  else
    cp -r .vscode "$TARGET_DIR/.vscode"
    if [[ $? -ne 0 ]]; then
      echo "Error copying .vscode directory to $TARGET_DIR/.vscode" >&2
    else
      [ "$VERBOSE" = true ] && echo "Copied .vscode directory to $TARGET_DIR/.vscode"
    fi
  fi
fi


# Update .gitignore in the target directory to ignore copied items
GITIGNORE_PATH="$TARGET_DIR/.gitignore"
IGNORE_ENTRIES=(".rules/" ".vscode/")
if [ "$INCLUDE_GITIGNORE_PROMPTS" = true ]; then
  IGNORE_ENTRIES=(".github/prompts/" "${IGNORE_ENTRIES[@]}")
fi

if [ "$DRY_RUN" = true ]; then
  echo "[DRY RUN] Would update $GITIGNORE_PATH to ignore: ${IGNORE_ENTRIES[*]}"
else
  touch "$GITIGNORE_PATH"
  for entry in "${IGNORE_ENTRIES[@]}"; do
    if ! grep -qxF "$entry" "$GITIGNORE_PATH"; then
      echo "$entry" >> "$GITIGNORE_PATH"
      [ "$VERBOSE" = true ] && echo "Added $entry to $GITIGNORE_PATH"
    else
      [ "$VERBOSE" = true ] && echo "$entry already in $GITIGNORE_PATH"
    fi
  done
fi


# Function to detect project type
detect_project_type() {
  local target="$1"

  # Check for Terraform files
  if find "$target" -maxdepth 2 -name "*.tf" -print -quit | grep -q .; then
    echo "terraform"
    return
  fi

  # Check for Python project files
  if [[ -f "$target/setup.py" ]] || [[ -f "$target/pyproject.toml" ]] || \
     [[ -f "$target/requirements.txt" ]] || [[ -f "$target/Pipfile" ]]; then
    echo "python"
    return
  fi

  # Check for Node.js project files
  if [[ -f "$target/package.json" ]]; then
    echo "nodejs"
    return
  fi

  # Check for Go project files
  if [[ -f "$target/go.mod" ]]; then
    echo "go"
    return
  fi

  # Check for Java project files
  if [[ -f "$target/pom.xml" ]] || [[ -f "$target/build.gradle" ]]; then
    echo "java"
    return
  fi

  # Check for Ruby project files
  if [[ -f "$target/Gemfile" ]]; then
    echo "ruby"
    return
  fi

  # Check for Chef files
  if [[ -f "$target/metadata.rb" ]] || [[ -f "$target/Berksfile" ]]; then
    echo "chef"
    return
  fi

  # Check for .NET project files
  if find "$target" -maxdepth 2 \( -name "*.csproj" -o -name "*.sln" \) -print -quit | grep -q .; then
    echo "dotnet"
    return
  fi

  echo "unknown"
}

# Function to merge .gitignore templates
merge_gitignore_templates() {
  local target_gitignore="$1"
  local detected_type="$2"
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  local templates_dir="$script_dir/templates/gitignore"

  if [[ ! -d "$templates_dir" ]]; then
    echo "Warning: .gitignore templates directory not found at $templates_dir" >&2
    return 1
  fi

  [ "$VERBOSE" = true ] && echo "Merging .gitignore templates for project type: $detected_type"

  # Create a temporary file for the merged content
  local temp_file
  temp_file=$(mktemp)

  # Add header
  cat > "$temp_file" <<'EOF'
# This .gitignore file was generated/updated by the prompt-library distribution system
# Source: https://github.com/yourusername/prompt-library
#
# It combines:
#   - Base patterns (OS, IDE, logs, environment)
#   - Security patterns (credentials, secrets, keys)
#   - Technology-specific patterns (based on project type)
#
# You can customize this file, but be aware that patterns may be regenerated
# if you run the distribution script again.
#
# To prevent specific files from being ignored, use negation patterns:
#   !file-to-include.txt

EOF

  # Copy base template
  if [[ -f "$templates_dir/base.gitignore" ]]; then
    [ "$VERBOSE" = true ] && echo "  - Adding base patterns"
    cat "$templates_dir/base.gitignore" >> "$temp_file"
    echo "" >> "$temp_file"
  fi

  # Copy security template
  if [[ -f "$templates_dir/security.gitignore" ]]; then
    [ "$VERBOSE" = true ] && echo "  - Adding security patterns"
    cat "$templates_dir/security.gitignore" >> "$temp_file"
    echo "" >> "$temp_file"
  fi

  # Copy technology-specific template
  if [[ "$detected_type" != "unknown" ]] && [[ -f "$templates_dir/${detected_type}.gitignore" ]]; then
    [ "$VERBOSE" = true ] && echo "  - Adding ${detected_type}-specific patterns"
    cat "$templates_dir/${detected_type}.gitignore" >> "$temp_file"
    echo "" >> "$temp_file"
  fi

  # If target .gitignore exists, preserve custom entries
  if [[ -f "$target_gitignore" ]]; then
    [ "$VERBOSE" = true ] && echo "  - Preserving existing custom entries"
    echo "####################" >> "$temp_file"
    echo "# Custom Entries (from existing .gitignore)" >> "$temp_file"
    echo "####################" >> "$temp_file"
    cat "$target_gitignore" >> "$temp_file"
  fi

  # Copy the merged content to target
  if [ "$DRY_RUN" = true ]; then
    echo "[DRY RUN] Would update $target_gitignore with merged templates"
    [ "$VERBOSE" = true ] && echo "Merged content preview (first 20 lines):"
    [ "$VERBOSE" = true ] && head -20 "$temp_file"
  else
    cp "$temp_file" "$target_gitignore"
    [ "$VERBOSE" = true ] && echo "Updated $target_gitignore with merged templates"
  fi

  rm -f "$temp_file"
}

# Handle .gitignore template copying if requested
if [ "$COPY_GITIGNORE_TEMPLATES" = true ]; then
  echo ""
  echo "📋 Processing .gitignore templates..."

  # Determine project type
  if [ "$AUTO_DETECT_PROJECT" = true ]; then
    DETECTED_TYPE=$(detect_project_type "$TARGET_DIR")
    echo "Detected project type: $DETECTED_TYPE"
  elif [ -n "$PROJECT_TYPE" ]; then
    DETECTED_TYPE="$PROJECT_TYPE"
    echo "Using specified project type: $DETECTED_TYPE"
  else
    DETECTED_TYPE="unknown"
    echo "Warning: No project type specified or detected. Only base and security patterns will be applied."
    read -p "Continue? [Y/n]: " RESP
    RESP=${RESP:-Y}
    if [[ ! "$RESP" =~ ^[Yy]$ ]]; then
      echo "Aborted."
      exit 0
    fi
  fi

  # Merge .gitignore templates
  TARGET_GITIGNORE="$TARGET_DIR/.gitignore"
  merge_gitignore_templates "$TARGET_GITIGNORE" "$DETECTED_TYPE"

  echo "✅ .gitignore templates processed"
fi

echo ""
echo "✅ All prompt and rule files processed for $TARGET_DIR"

# Post-run: Ask user if they want to remove .github/prompts/ from .gitignore if present
if [ "$DRY_RUN" = false ] && [ "$INCLUDE_GITIGNORE_PROMPTS" = true ]; then
  if grep -qxF ".github/prompts/" "$GITIGNORE_PATH"; then
    echo
    read -p "Do you want to keep .github/prompts/ in $GITIGNORE_PATH? [Y/n]: " RESP
    RESP=${RESP:-Y}
    if [[ ! "$RESP" =~ ^[Yy]$ ]]; then
      # Remove the entry
      grep -vxF ".github/prompts/" "$GITIGNORE_PATH" > "$GITIGNORE_PATH.tmp" && mv "$GITIGNORE_PATH.tmp" "$GITIGNORE_PATH"
      echo ".github/prompts/ removed from $GITIGNORE_PATH."
    else
      echo ".github/prompts/ kept in $GITIGNORE_PATH."
    fi
  fi
fi
