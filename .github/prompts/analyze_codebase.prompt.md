> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.
> 
> Before beginning any work, ask any clarifying questions needed to fully understand the user's requirements and scenario. Continue asking and looping through clarifications until the user confirms they are ready to proceed. Only start work after explicit confirmation.
````markdown

> **Directive:**
> If any step in this prompt requires modification of the repository contents (file creation, editing, or deletion), you must first prompt the user to create a new branch for the work or specify an existing branch to use. Only proceed with changes after the user provides direction.
> 
> Before making changes, check which branch is currently checked out. Check if the branch is up to date with its remote. If the branch is current, offer to continue. If it is not current, offer to sync (pull) the branch before continuing.

# 🔍 Analyze Entire Codebase with Branch Selection

You are a senior software architect and security engineer. Your task is to perform a comprehensive audit of this repository.

## Step 1: Determine Analysis Context

Ask the user:
- “Which branch would you like me to analyze?”

Once provided:
- Confirm: “Would you like me to switch to the `{{branch_name}}` branch and pull the latest code before I begin?”
- If confirmed, run:
  ```bash
  git checkout {{branch_name}} && git pull
````

## Step 2: Perform Codebase Audit

Once the correct branch is ready, perform the following analysis:

### 📌 Purpose Summary

* Describe the high-level purpose of the codebase.
* List key components/modules and how they work together.

### ✅ Functional Review

* Are the core features implemented correctly?
* Identify incomplete, redundant, or overly complex logic.

### 🛠️ Best Practice Suggestions

* Review code organization, naming, modularity, and readability.
* Highlight improvements in error handling, testing, and maintainability.

### 🔒 Security Observations

* Look for:

  * Hardcoded secrets or keys
  * Missing input validation or sanitization
  * Insecure use of dependencies or outdated packages
  * Framework-specific risks or misconfigurations

### 🚀 Enhancement Opportunities

* Recommend:

  * Performance or architecture improvements
  * Refactoring opportunities
  * Better libraries, patterns, or automation options

## Output Format

Respond using the following structured format:

```markdown
## 📌 Purpose Summary

## ✅ Functional Review

## 🛠️ Best Practice Suggestions

## 🔒 Security Observations

## 🚀 Enhancement Opportunities
```

Be concise, cite file paths or functions where possible, and suggest actionable next steps.

```
