> **Best Practices:**
> - Ask clarifying questions before proceeding if any requirements or context are unclear.
> - Ask for permission before running commands, editing, or creating files. Once permission is granted, you may proceed with these actions without asking again until the user revokes or limits permission.

> **Context Management:**
> If the application containerization requirements are too complex for comprehensive dockerization, prioritize:
> 1. Security-critical container configurations and image hardening practices
> 2. Production-ready multi-stage builds and dependency management
> 3. Integration effectiveness with deployment pipelines and orchestration platforms
> Ask user to specify focus areas if scope exceeds dockerization capacity.

> **Analysis Validation:**
> - Mark implementation choices as "Best Practice" vs "Alternative" based on Docker documentation and container security standards
> - Reference specific Dockerfile patterns, security scanners, or deployment configs when making recommendations
> - Provide confidence indicators: High/Medium/Low for each containerization decision
> - Note when additional application architecture details would improve dockerization recommendations

<!--
title: "Dockerize Application"
category: "Containerization"
description: "Generate a Dockerfile and instructions to containerize any application."
-->

# Prompt: Dockerize Application
# Directive:
If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.

Write a Dockerfile to containerize the given application. Include best practices for security, multi-stage builds, and environment variable configuration.
