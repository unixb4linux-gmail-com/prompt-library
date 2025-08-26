#!/usr/bin/env python3
"""
Script to add version numbers to all prompt files in the repository.
This script adds a version field to the YAML frontmatter of each prompt file.
"""

import os
import re
import yaml
from datetime import datetime

def process_prompt_file(filepath):
    """Add version information to a prompt file's YAML frontmatter"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Check if file has YAML frontmatter
    if not lines or lines[0].strip() != '---':
        # No YAML frontmatter, add one with version
        frontmatter = """---
version: "1.0.0"
created_date: "{}"
last_updated: "{}"
---

""".format(datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"))
        
        new_content = frontmatter + content
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Added new frontmatter with version 1.0.0"
    
    # Find the end of YAML frontmatter
    yaml_end_idx = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            yaml_end_idx = i
            break
    
    if yaml_end_idx is None:
        return False, "Invalid YAML frontmatter structure"
    
    # Extract and parse YAML
    yaml_lines = lines[1:yaml_end_idx]
    yaml_content = '\n'.join(yaml_lines)
    
    try:
        metadata = yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        return False, "Failed to parse YAML frontmatter"
    
    # Add versioning information
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    if 'version' not in metadata:
        metadata['version'] = "1.0.0"
        metadata['created_date'] = current_date
        metadata['last_updated'] = current_date
    
    # Write updated content
    new_yaml = yaml.dump(metadata, default_flow_style=False, sort_keys=False).strip()
    
    new_lines = ['---'] + new_yaml.split('\n') + lines[yaml_end_idx:]
    new_content = '\n'.join(new_lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, f"Updated with version {metadata['version']}"

def main():
    """Process all prompt files in the repository"""
    prompt_files = []
    
    # Find all .prompt.md files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.prompt.md'):
                prompt_files.append(os.path.join(root, file))
    
    print(f"Found {len(prompt_files)} prompt files to version")
    
    success_count = 0
    error_count = 0
    
    for filepath in sorted(prompt_files):
        try:
            success, message = process_prompt_file(filepath)
            if success:
                print(f"✅ {filepath}: {message}")
                success_count += 1
            else:
                print(f"❌ {filepath}: {message}")
                error_count += 1
        except Exception as e:
            print(f"❌ {filepath}: Error - {str(e)}")
            error_count += 1
    
    print(f"\n📊 Summary: {success_count} successful, {error_count} errors")
    
    if success_count > 0:
        print("\n🔄 Regenerating index file...")
        os.system("python3 scripts/generate_index.py")
        print("✅ Index file updated")

if __name__ == "__main__":
    main()