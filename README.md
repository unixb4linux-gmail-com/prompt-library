# Prompt Library

A collection of reusable prompt engineering files for DevOps, automation, and code generation.

## Usage

- Copy prompts and rules into any target repo:

  ```bash
  ./copy-prompts.sh /path/to/target-repo
  ```

  - Use `-n` or `--dry-run` to preview actions without copying files.
  - Use `-v` or `--verbose` for detailed output.
  - Use `-c` or `--confirm` to auto-confirm overwrites.

- Prompts will be placed in: `.github/prompts/`
- Rules will be placed in: `.rules/`
- The `.vscode` directory will be placed in: `.vscode/`

- Each prompt file includes metadata for easy filtering and automation.
- Rules files provide structured behavior and expectations for AI agents using the prompts.

### Troubleshooting

- If you see permission errors, ensure you have write access to the target directory.
- If files are not copied, check that the source files exist and paths are correct.
- For existing files, you will be prompted before overwriting unless you use `-c`.
- Use dry-run mode to safely preview changes before applying.

## Prompts

- **setup_python_api.prompt.md**: Scaffold a Python API project.
- **dockerize_app.prompt.md**: Dockerize any application.
- **write_tests.prompt.md**: Generate tests for your codebase.
- **deploy_aks_terraform.prompt.md**: Deploy to AKS using Terraform.
- **build_and_test_terraform.prompt.md**: Iteratively test tool functionality with AI agent.
- **self_test_code_agent.prompt.md**: Generic self-test prompt for building and verifying any coding project using an AI agent.

## Rules

- **copy-prompts.rules.mdc**: Defines behavior of the copy-prompts.sh script, including prompt and rule file locations.
- **python.mdc**: Rules for Python-based projects and agents.
- **react.mdc**: Rules for React component generation and structure.
- **ruby.mdc**: AI guidelines for writing idiomatic Ruby code.
- **typescript.mdc**: Type-safe TypeScript patterns for clean component design.
- **nodejs.mdc**, **nextjs-app-router.mdc**, **react-component.mdc**, etc.: Various rulesets for agent behavior by tech stack.
