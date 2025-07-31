# My Rules

![My Rules](assets/my-rules-repo.png)

This repository contains personal coding conventions and best practices across multiple technologies. The goal is to provide a portable set of rules that can be easily included in any project without being tied to specific file structures, naming schemes, or domains.

## Philosophy

- Keep projects clean by separating *how you write code* from *what the project is*.
- Avoid polluting new codebases with inconsistent or project-specific style decisions.
- Enable fast ramp-up in Cursor or any editor by loading your preferred rules per technology.

## Structure

Each `.mdc` file represents conventions for a specific technology or stack (e.g., `react.mdc`, `python.mdc`, `nextjs-app-router.mdc`).

Files can be imported, linked, or embedded in project onboarding docs, documentation sites, or developer notes.

## Pull my rules into `.cursor/rules`

# Function to download .mdc files from rwoody/my-rules repo

```
download_mdc_rules() {
    local temp_dir=$(mktemp -d)
    local target_dir=""

    echo "Downloading rules from rwoody/my-rules..."

    # Determine target directory
    if [[ $(basename "$PWD") == "rules" ]]; then
        target_dir="$PWD"
    else
        target_dir="$PWD/.cursor/rules"
        mkdir -p "$target_dir"
    fi

    # Clone repo to temp directory
    git clone https://github.com/rwoody/my-rules.git "$temp_dir" 2>/dev/null

    if [ $? -eq 0 ]; then
        # Copy all .mdc files to target directory
        find "$temp_dir" -name "*.mdc" -exec cp {} "$target_dir" \;
        echo "Successfully downloaded .mdc files to $target_dir"
    else
        echo "Error: Failed to download rules repository"
    fi

    # Cleanup
    rm -rf "$temp_dir"
}

alias dlrules="download_mdc_rules"
```

## Rule Specificity and Application

You can create more specific rule files for different contexts within a single technology. For example, you might have a general `react.mdc` file for overall React development, but a more focused `react-component.mdc` for files that exclusively define components.

This allows you to provide more tailored context to the AI based on the task. An editor or tool can be configured to apply rules based on file patterns:

- **`**/*.service.ts`** might use `nodejs.mdc` and `typescript.mdc`.
- **`**/components/**/*.tsx`** might use `react-component.mdc`.
- **A general `*.tsx` file** might fall back to the broader `react.mdc`.

This approach ensures that the guidance you receive is highly relevant to the specific type of code you are writing, whether it's a UI component, a backend service, a database model, or a utility function.

## Versions

If you need different versions of a technology, you can make a new file with the same name but with a different version number. eg. `react.mdc` and `react-19.mdc`. It might be useful to have a symlink to the latest version...

---

## To Do

Add the following files:

- [x] `react.mdc`
- [x] `nextjs-app-router.mdc`
- [x] `typescript.mdc`
- [x] `python.mdc`
- [x] `nodejs.mdc`
- [x] `ruby.mdc`
- [x] `ruby-on-rails.mdc`
- [x] `react-component.mdc`
