#!/usr/bin/env python3
"""
Script to generate an index of all prompts and rules in the repository.
Outputs to PROMPT_RULE_INDEX.md in the repo root.
"""
#!/usr/bin/env python3
"""
Script to generate an index of all prompts and rules in the repository.
Outputs to PROMPT_RULE_INDEX.md in the repo root.
"""
import os
import re
import yaml
from collections import defaultdict

INDEX_FILE = "PROMPT_RULE_INDEX.md"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, ".."))

def extract_metadata(filepath):
    """Extract all metadata from YAML frontmatter if present."""
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    metadata = {}
    if lines and lines[0].strip() == '---':
        fm_lines = []
        for line in lines[1:]:
            if line.strip() == '---':
                break
            fm_lines.append(line)
        try:
            meta = yaml.safe_load(''.join(fm_lines))
            if isinstance(meta, dict):
                metadata = meta
        except Exception as e:
            print(f"Error parsing YAML in {filepath}: {e}")
    
    # Fallback for title if 'name' is not in frontmatter
    if 'name' not in metadata or not metadata['name']:
        for line in lines:
            m = re.match(r'^# ?(.+)', line)
            if m:
                metadata['name'] = m.group(1).strip()
                break
    
    return metadata

all_prompts = defaultdict(list)

for subdir, _, files in os.walk(REPO):
    for file in files:
        if file.endswith(('.md', '.mdc')) and not file.startswith(INDEX_FILE.split('.')[0]):
            filepath = os.path.join(subdir, file)
            rel_path = os.path.relpath(filepath, REPO)
            metadata = extract_metadata(filepath)
            
            if not metadata.get('name'):
                continue # Skip files without a name

            # Determine category based on directory structure
            category = os.path.basename(os.path.dirname(rel_path))
            if category == '.github':
                category = '.github/prompts'
            elif category == '.rules':
                category = '.rules'
            elif category == 'prompt-library': # Root level files
                category = 'root'
            
            all_prompts[category].append({
                'name': metadata.get('name', os.path.basename(file)),
                'id': metadata.get('id', ''),
                'description': metadata.get('description', 'No description provided.'),
                'version': metadata.get('version', 'N/A'),
                'tags': ', '.join(metadata.get('tags', [])),
                'tool_compatibility': ', '.join(metadata.get('tool_compatibility', [])),
                'path': rel_path
            })

index_content = ["# Prompt & Rule Index\n", "This document is automatically generated. Do not edit manually.\n"]

# Sort categories for consistent output
sorted_categories = sorted(all_prompts.keys())

for category in sorted_categories:
    if category == 'root':
        index_content.append(f"## Root Level Prompts\n")
    else:
        index_content.append(f"## {category.replace('_', ' ').title()} Prompts\n")
    
    index_content.append("| Name | ID | Description | Version | Tags | Tools | Path |")
    index_content.append("|---|---|---|---|---|---|---|")

    # Sort prompts within each category by name
    sorted_prompts = sorted(all_prompts[category], key=lambda x: x['name'].lower())

    for prompt in sorted_prompts:
        index_content.append(f"| [{prompt['name']}]({prompt['path']}) | {prompt['id']} | {prompt['description']} | {prompt['version']} | {prompt['tags']} | {prompt['tool_compatibility']} | `{prompt['path']}` |")
    index_content.append("\n") # Add a newline for spacing between categories

with open(os.path.join(REPO, INDEX_FILE), 'w', encoding='utf-8') as out:
    out.write('\n'.join(index_content))

print(f"Index written to {INDEX_FILE}")
