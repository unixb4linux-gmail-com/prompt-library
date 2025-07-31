# Prompt Library

A collection of reusable prompt engineering files for DevOps, automation, and code generation.

## Usage

- Copy prompts and rules into any target repo:  
  `./copy-prompts.sh /path/to/target-repo`

- Prompts will be placed in: `.github/prompts/`  
- Rules will be placed in: `.rules/`

- Each prompt file includes metadata for easy filtering and automation.
- Rules files provide structured behavior and expectations for AI agents using the prompts.

---

# Prompts

- **setup_python_api.prompt.md**: Scaffold a Python API project.
- **dockerize_app.prompt.md**: Dockerize any application.
- **write_tests.prompt.md**: Generate tests for your codebase.
- **deploy_aks_terraform.prompt.md**: Deploy to AKS using Terraform.
- **build_and_test_terraform.prompt.md**: Iteratively test tool functionality with AI agent.
- **self_test_code_agent.prompt.md**: Generic self-test prompt for building and verifying any coding project using an AI agent.

---

# Rules

- **copy-prompts.rules.mdc**: Defines behavior of the copy-prompts.sh script, including prompt and rule file locations.
- **python.mdc**: Rules for Python-based projects and agents.
- **react.mdc**: Rules for React component generation and structure.
- **ruby.mdc**: AI guidelines for writing idiomatic Ruby code.
- **typescript.mdc**: Type-safe TypeScript patterns for clean component design.
- **nodejs.mdc**, **nextjs-app-router.mdc**, **react-component.mdc**, etc.: Various rulesets for agent behavior by tech stack.

# prompt-library
