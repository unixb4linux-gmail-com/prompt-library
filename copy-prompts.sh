#!/bin/bash

# Enhanced copy-prompts.sh with robust argument parsing, quoting, error handling, and shellcheck compliance
DRY_RUN=false
VERBOSE=false
CONFIRM_OVERWRITE=false
TARGET_DIR=""

usage() {
  echo "Usage: $0 [-n|--dry-run] [-v|--verbose] [-c|--confirm] /path/to/target-repo"
  exit 1
}

# Parse options
while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--dry-run) DRY_RUN=true ; shift ;;
    -v|--verbose) VERBOSE=true ; shift ;;
    -c|--confirm) CONFIRM_OVERWRITE=true ; shift ;;
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
fi

copy_file() {
  local src="$1"
  local dest="$2"
  if [[ -e "$dest" ]] && [[ "$CONFIRM_OVERWRITE" = false ]]; then
    read -p "File $dest exists. Overwrite? [y/N]: " yn
    case $yn in
      [Yy]*) ;;
      *) echo "Skipped $dest"; return 0 ;;
    esac
  fi
  if [ "$DRY_RUN" = true ]; then
    echo "[DRY RUN] Would copy $src to $dest"
  else
    cp "$src" "$dest"
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

echo "✅ All prompt and rule files processed for $TARGET_DIR"
