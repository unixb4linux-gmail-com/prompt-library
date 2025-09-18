#!/usr/bin/env python3
"""
Script to generate an index of all prompts and rules in the repository.
Outputs to PROMPT_RULE_INDEX.md in the repo root.
"""
import os

INDEX_FILE = "PROMPT_RULE_INDEX.md"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, ".."))

index = ["# Prompt & Rule Index\n"]


import re
import yaml

def extract_metadata(filepath):
    """Extract title, description, and category from YAML frontmatter if present."""
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    title = description = category = None
    if lines and lines[0].strip() == '---':
        # Parse YAML frontmatter
        fm_lines = []
        for line in lines[1:]:
            if line.strip() == '---':
                break
            fm_lines.append(line)
        try:
            meta = yaml.safe_load(''.join(fm_lines))
            if isinstance(meta, dict):
                title = meta.get('title')
                description = meta.get('description')
                category = meta.get('category')
        except Exception as e:
            print(f"Error parsing YAML in {filepath}: {e}")
    # Fallback: first non-empty heading
    if not title:
        for line in lines:
            m = re.match(r'^# ?(.+)', line)
            if m:
                title = m.group(1).strip()
                break
    return title, description, category

for subdir, _, files in os.walk(REPO):
    for file in files:
        if file.endswith(('.md', '.mdc')) and not file.startswith('PROMPT_RULE_INDEX'):
            rel_path = os.path.relpath(os.path.join(subdir, file), REPO)
            title, description, category = extract_metadata(os.path.join(subdir, file))
            if not title or title in ("---", "", "[]"):  # skip empty/placeholder
                continue
            line = f"- [{title}]({rel_path})"
            if category:
                line += f"  _(Category: {category})_"
            if description:
                line += f"\n    - {description}"
            index.append(line)

with open(os.path.join(REPO, INDEX_FILE), 'w', encoding='utf-8') as out:
    out.write('\n'.join(index))

print(f"Index written to {INDEX_FILE}")
