#!/bin/bash

TARGET_DIR=$1

if [ -z "$TARGET_DIR" ]; then
  echo "Usage: $0 /absolute/or/relative/path/to/target-repo"
  exit 1
fi

echo "📁 Copying prompts..."
mkdir -p "$TARGET_DIR/.github/prompts"
find . -type f -name '*.prompt.md' -exec cp {} "$TARGET_DIR/.github/prompts/" \;

echo "📁 Copying rules..."
mkdir -p "$TARGET_DIR/.rules"
cp .rules/*.mdc "$TARGET_DIR/.rules/"

echo "✅ All prompt and rule files copied to $TARGET_DIR"
