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

for subdir, _, files in os.walk(REPO):
    for file in files:
        if file.endswith(('.md', '.mdc')) and not file.startswith('PROMPT_RULE_INDEX'):
            rel_path = os.path.relpath(os.path.join(subdir, file), REPO)
            with open(os.path.join(subdir, file), encoding='utf-8', errors='ignore') as f:
                first = f.readline().strip()
                if first == '---':
                    # YAML frontmatter: skip to first non-frontmatter line
                    while True:
                        line = f.readline()
                        if not line or line.strip() == '---':
                            break
                    title = f.readline().strip().lstrip('#').strip()
                else:
                    title = first.lstrip('#').strip()
            index.append(f"- [{title}]({rel_path})  ")

with open(os.path.join(REPO, INDEX_FILE), 'w', encoding='utf-8') as out:
    out.write('\n'.join(index))

print(f"Index written to {INDEX_FILE}")
