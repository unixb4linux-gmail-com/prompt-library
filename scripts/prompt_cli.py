import os
import json
import argparse
import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def _get_all_prompts(repo_root):
    all_prompts_data = []
    for subdir, _, files in os.walk(repo_root):
        for file in files:
            if file.endswith(('.md', '.mdc')) and not file.startswith('PROMPT_RULE_INDEX'):
                filepath = os.path.join(subdir, file)
                rel_path = os.path.relpath(filepath, repo_root)
                
                metadata = {}
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                
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
                
                if metadata: # Include all prompts for linting purposes
                    metadata['path'] = rel_path
                    all_prompts_data.append(metadata)
    return all_prompts_data

def search_prompts(args):
    prompts = _get_all_prompts(args.root)
    results = []
    for prompt in prompts:
        match = False
        if args.keyword:
            keyword_lower = args.keyword.lower()
            if (
                keyword_lower in str(prompt.get('name', '')).lower() or
                keyword_lower in str(prompt.get('description', '')).lower() or
                keyword_lower in str(prompt.get('id', '')).lower()
            ):
                match = True
        
        if args.tag and args.tag.lower() in [t.lower() for t in prompt.get('tags', [])]:
            match = True
        
        if args.tool and args.tool.lower() in [t.lower() for t in prompt.get('tool_compatibility', [])]:
            match = True

        if match or (not args.keyword and not args.tag and not args.tool):
            results.append(prompt)
    
    if results:
        print("\nSearch Results:")
        for r in results:
            print(f"- {r.get('name', 'N/A')} (ID: {r.get('id', 'N/A')})\n  Description: {r.get('description', 'N/A')}\n  Path: {r.get('path', 'N/A')}\n  Tags: {r.get('tags', [])}\n  Tools: {r.get('tool_compatibility', [])}\n")
    else:
        print("No prompts found matching your criteria.")

def show_prompt(args):
    prompts = _get_all_prompts(args.root)
    found = False
    for prompt in prompts:
        if prompt.get('id') == args.prompt_id:
            found = True
            print(f"\n--- Prompt: {prompt.get('name', 'N/A')} (ID: {prompt.get('id', 'N/A')}) ---")
            print(f"Description: {prompt.get('description', 'N/A')}")
            print(f"Version: {prompt.get('version', 'N/A')}")
            print(f"Path: {prompt.get('path', 'N/A')}")
            print(f"Tags: {prompt.get('tags', [])}")
            print(f"Tools: {prompt.get('tool_compatibility', [])}")
            print("\n--- Content ---")
            with open(os.path.join(args.root, prompt['path']), 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Remove frontmatter for display
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) > 2:
                        content = parts[2].strip()
                print(content)
            break
    if not found:
        print(f"Prompt with ID '{args.prompt_id}' not found.")

def lint_prompts(args):
    prompts = _get_all_prompts(args.root)
    errors = 0
    print("\n--- Linting Prompts ---")
    for prompt in prompts:
        is_valid = True
        if not prompt.get('id'):
            print(f"[ERROR] {prompt.get('path', 'N/A')}: Missing 'id' in frontmatter.")
            is_valid = False
        if not prompt.get('name'):
            print(f"[ERROR] {prompt.get('path', 'N/A')}: Missing 'name' in frontmatter.")
            is_valid = False
        if not prompt.get('description'):
            print(f"[WARNING] {prompt.get('path', 'N/A')}: Missing 'description' in frontmatter.")
        if not prompt.get('version'):
            print(f"[WARNING] {prompt.get('path', 'N/A')}: Missing 'version' in frontmatter.")
        if not isinstance(prompt.get('tags', []), list):
            print(f"[ERROR] {prompt.get('path', 'N/A')}: 'tags' should be a list.")
            is_valid = False
        if not isinstance(prompt.get('tool_compatibility', []), list):
            print(f"[ERROR] {prompt.get('path', 'N/A')}: 'tool_compatibility' should be a list.")
            is_valid = False
        
        # Add more linting rules as needed (e.g., valid semantic version, date format, etc.)

        if not is_valid:
            errors += 1
    
    if errors == 0:
        print("All prompts passed linting with no errors.")
    else:
        print(f"Linting completed with {errors} errors.")

def main():
    parser = argparse.ArgumentParser(description="CLI tool for managing prompt library.")
    parser.add_argument("--root", default=REPO_ROOT, help="Root directory of the prompt library.")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for prompts.")
    search_parser.add_argument("keyword", nargs='?', help="Keyword to search in name, description, or ID.")
    search_parser.add_argument("--tag", help="Filter by tag.")
    search_parser.add_argument("--tool", help="Filter by AI tool compatibility.")
    search_parser.set_defaults(func=search_prompts)

    # Show command
    show_parser = subparsers.add_parser("show", help="Show content and metadata of a prompt.")
    show_parser.add_argument("prompt_id", help="ID of the prompt to show.")
    show_parser.set_defaults(func=show_prompt)

    # Lint command
    lint_parser = subparsers.add_parser("lint", help="Lint prompts for metadata consistency.")
    lint_parser.set_defaults(func=lint_prompts)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
