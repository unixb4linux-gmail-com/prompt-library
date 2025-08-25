> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
> 
> Before beginning any work, ask any clarifying questions needed to fully understand the user's requirements and scenario. Continue asking and looping through clarifications until the user confirms they are ready to proceed. Only start work after explicit confirmation.
<!--
title: "Write Tests for Codebase"
category: "Testing"
description: "Generate unit and integration tests for a codebase."
-->

# Prompt: Write Tests for Codebase
> **Ask clarifying questions before proceeding.**
> **Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.**

> **Context Management:**
> If the codebase is too complex for comprehensive test coverage, prioritize:
> 1. Security-critical functions and business logic with high risk exposure
> 2. Production core functionality and error handling pathways
> 3. Integration points with external services and data persistence layers
> Ask user to specify focus areas if scope exceeds testing capacity.

> **Analysis Validation:**
> - Mark test coverage as "Comprehensive" vs "Basic" based on codebase complexity and testing framework capabilities
> - Reference specific test types, coverage metrics, or testing patterns when citing recommendations
> - Provide confidence indicators: High/Medium/Low for each testing strategy and coverage assessment
> - Note when additional codebase analysis or testing tool access would improve test quality
# Directive:
If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.

Analyze the codebase and generate comprehensive unit and integration tests. Use the appropriate testing framework for the language. Include coverage reports if possible.
