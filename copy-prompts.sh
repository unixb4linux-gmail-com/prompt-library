#!/bin/bash

# Enhanced copy-prompts.sh with robust argument parsing, quoting, error handling, and shellcheck compliance
DRY_RUN=false
VERBOSE=false
CONFIRM_OVERWRITE=true
INCLUDE_GITIGNORE_PROMPTS=true
TARGET_DIR=""

usage() {
  echo "Usage: $0 [-n|--dry-run] [-v|--verbose] [--no-gitignore-prompts] /path/to/target-repo"
  exit 1
}

# Parse options

while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--dry-run) DRY_RUN=true ; shift ;;
    -v|--verbose) VERBOSE=true ; shift ;;
    --no-gitignore-prompts) INCLUDE_GITIGNORE_PROMPTS=false ; shift ;;
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
