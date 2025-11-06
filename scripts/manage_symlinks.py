import os
import json
import argparse

def _create_symlink_single(source, link_name, force=False):
    os.makedirs(os.path.dirname(link_name), exist_ok=True)
    if os.path.exists(link_name):
        if os.path.islink(link_name):
            if os.readlink(link_name) == source:
                print(f"Symlink already exists and is correct: {link_name} -> {source}")
                return True
            else:
                if force:
                    print(f"Removing incorrect symlink: {link_name}")
                    os.remove(link_name)
                else:
                    print(f"Symlink exists but points to a different source: {link_name} -> {os.readlink(link_name)} (expected {source}). Use --force to update.")
                    return False
        else:
            if force:
                print(f"Removing existing file (not a symlink): {link_name}")
                os.remove(link_name)
            else:
                print(f"File exists and is not a symlink: {link_name}. Use --force to overwrite.")
                return False
    
    try:
        os.symlink(source, link_name)
        print(f"Created symlink: {link_name} -> {source}")
        return True
    except OSError as e:
        print(f"Error creating symlink {link_name} -> {source}: {e}")
        return False

def _process_repo_symlinks(repo_config, prompt_library_root, action, force=False):
    repo_path = repo_config['path']
    print(f"Processing repository: {repo_path} for action: {action}")

    for symlink_type, files in repo_config['symlinks'].items():
        target_dir = os.path.join(repo_path, symlink_type)
        os.makedirs(target_dir, exist_ok=True)

        for file_name in files:
            if file_name == "*":
                source_dir = os.path.join(prompt_library_root, symlink_type)
                if not os.path.isdir(source_dir):
                    print(f"Warning: Source directory not found for wildcard: {source_dir}")
                    continue
                
                for item in os.listdir(source_dir):
                    source_item_path = os.path.join(source_dir, item)
                    if os.path.isfile(source_item_path):
                        link_path = os.path.join(target_dir, item)
                        if action == "create" or action == "update":
                            _create_symlink_single(source_item_path, link_path, force)
                        elif action == "validate":
                            _validate_symlink_single(source_item_path, link_path)
            else:
                source_path = os.path.join(prompt_library_root, symlink_type, file_name)
                link_path = os.path.join(target_dir, file_name)
                if action == "create" or action == "update":
                    _create_symlink_single(source_path, link_path, force)
                elif action == "validate":
                    _validate_symlink_single(source_path, link_path)

def _validate_symlink_single(source, link_name):
    if not os.path.exists(link_name):
        print(f"Validation FAILED: Symlink does not exist: {link_name}")
        return False
    if not os.path.islink(link_name):
        print(f"Validation FAILED: Path is not a symlink: {link_name}")
        return False
    
    current_source = os.readlink(link_name)
    if current_source != source:
        print(f"Validation FAILED: Symlink {link_name} points to {current_source}, expected {source}")
        return False
    if not os.path.exists(source):
        print(f"Validation FAILED: Symlink {link_name} points to a non-existent source: {source}")
        return False
    
    print(f"Validation PASSED: {link_name} -> {source}")
    return True

def create_symlinks_command(args):
    with open(args.config, 'r') as f:
        config = json.load(f)
    for repo_config in config['repositories']:
        _process_repo_symlinks(repo_config, args.root, "create", args.force)

def validate_symlinks_command(args):
    with open(args.config, 'r') as f:
        config = json.load(f)
    for repo_config in config['repositories']:
        _process_repo_symlinks(repo_config, args.root, "validate")

def update_symlinks_command(args):
    with open(args.config, 'r') as f:
        config = json.load(f)
    for repo_config in config['repositories']:
        _process_repo_symlinks(repo_config, args.root, "update", force=True) # Update implies force

def main():
    parser = argparse.ArgumentParser(description="Manage symlinks for prompt library.")
    parser.add_argument("--config", default="symlink_config.json", help="Path to the symlink configuration JSON file.")
    parser.add_argument("--root", default=os.getcwd(), help="Root directory of the prompt library.")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create symlinks.")
    create_parser.add_argument("--force", action="store_true", help="Force overwrite existing files/symlinks.")
    create_parser.set_defaults(func=create_symlinks_command)

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate existing symlinks.")
    validate_parser.set_defaults(func=validate_symlinks_command)

    # Update command
    update_parser = subparsers.add_parser("update", help="Update (recreate) symlinks, forcing overwrite.")
    update_parser.set_defaults(func=update_symlinks_command)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
