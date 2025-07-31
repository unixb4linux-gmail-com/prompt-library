#!/bin/bash

SRC_PROMPTS=".github/prompts"
SRC_RULES=".rules"
DEST="$1"

if [ -z "$DEST" ]; then
  echo "❌ Usage: ./copy-prompts.sh /path/to/target-repo"
  exit 1
fi

echo "📁 Copying prompts..."
mkdir -p "$DEST/.github/prompts"
cp -v "$SRC_PROMPTS"/*.prompt.md "$DEST/.github/prompts/"

echo "📁 Copying rules..."
mkdir -p "$DEST/.rules"
cp -v "$SRC_RULES"/*.mdc "$DEST/.rules/"

echo "✅ All prompt and rule files copied to $DEST"
