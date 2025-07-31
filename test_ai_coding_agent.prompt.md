---
# Prompt: Test AI Coding Agent with Iterative Command Execution
# Category: devops, testing, agent
# Author: daryl
# Use Case: Test AI agent’s ability to plan, code, run, and self-correct
# Description: Direct an AI assistant (e.g., Copilot) to iteratively build and test tooling based on a fixed scenario, until success is achieved

## Instructions

You are acting as an AI coding assistant with full access to the project files and command execution environment. Going forward:

- Your goal is to test the coding tool or environment using this scenario:
  
  **"Build me a basic Terraform structure using best practices in a new directory.  
  The new directory should be named `test_terraform` in the root of the repo."**

- Follow these guidelines:
  - Create and edit files as needed to complete the task.
  - Run commands as necessary to test functionality.
  - Diagnose and resolve any issues you encounter.
  - Assume all user confirmation prompts are answered **yes**.
  - Only stop once a full, successful test is achieved.

- Once successful, prompt the user with:
  **"The test completed successfully. Would you like to review the result?"**

Until that point, continue working autonomously.

---

## Notes
This prompt is designed for use with AI coding agents like GitHub Copilot Chat, Cursor, or AutoGen-enabled DevOps agents.
---
