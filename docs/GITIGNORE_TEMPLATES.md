# .gitignore Templates and Validation

This directory provides comprehensive `.gitignore` templates for various technology stacks, along with tooling to validate existing `.gitignore` files against best practices.

## Overview

The `.gitignore` template system consists of three main components:

1. **Template Library** (`templates/gitignore/`) - Curated `.gitignore` patterns for different technologies
2. **Distribution Script** (`copy-prompts.sh`) - Automated deployment of templates to target repositories
3. **Validation Tool** (`scripts/validate_gitignore.py`) - Auditing tool to check `.gitignore` completeness

## Template Structure

Templates are organized in layers:

### Base Template (`base.gitignore`)
Universal patterns that apply to all projects:
- IDE files (VSCode, IntelliJ, Vim, Sublime)
- OS files (macOS, Windows, Linux)
- Logs
- Environment files
- Temporary files
- Claude Code settings

### Security Template (`security.gitignore`)
**CRITICAL** patterns that must be in every project:
- Credentials and keys (`.pem`, `.key`, `credentials.json`)
- Cloud provider credentials (`.aws/`, `.azure/`, `.gcloud/`)
- Infrastructure secrets (`*.tfstate`, `*.tfvars`)
- Configuration management secrets (Chef, Ansible)
- Database files (may contain sensitive data)
- Certificate files

### Technology-Specific Templates

Each technology has comprehensive patterns:

- **`python.gitignore`** - Python, Django, Flask, pytest, virtual environments
- **`nodejs.gitignore`** - Node.js, React, Next.js, Yarn Berry, pnpm
- **`terraform.gitignore`** - Terraform state, variables, plan files
- **`go.gitignore`** - Go binaries, test coverage, workspaces
- **`java.gitignore`** - Maven, Gradle, IntelliJ, Eclipse
- **`ruby.gitignore`** - Rails, Chef, Bundler, Test Kitchen
- **`dotnet.gitignore`** - .NET, C#, Visual Studio, NuGet
- **`chef.gitignore`** - Chef cookbooks, Berkshelf, Test Kitchen (included in ruby template)

## Using the Distribution Script

### Basic Usage

Copy prompts and rules only (no `.gitignore` changes):
```bash
./copy-prompts.sh /path/to/target-repo
```

### With .gitignore Templates

**Auto-detect project type:**
```bash
./copy-prompts.sh --with-gitignore --auto-detect /path/to/target-repo
```

**Specify project type manually:**
```bash
./copy-prompts.sh --with-gitignore --type python /path/to/target-repo
```

**Preview changes (dry-run):**
```bash
./copy-prompts.sh -n --with-gitignore --auto-detect /path/to/target-repo
```

**Verbose output:**
```bash
./copy-prompts.sh -v --with-gitignore --type terraform /path/to/target-repo
```

### Supported Project Types

The script auto-detects project types based on these indicators:

| Type | Detection Files |
|------|----------------|
| `python` | `setup.py`, `pyproject.toml`, `requirements.txt`, `Pipfile` |
| `nodejs` | `package.json` |
| `go` | `go.mod` |
| `java` | `pom.xml`, `build.gradle` |
| `ruby` | `Gemfile` |
| `chef` | `metadata.rb`, `Berksfile` |
| `dotnet` | `*.csproj`, `*.sln` |
| `terraform` | `*.tf` files |

### How Template Merging Works

When you use `--with-gitignore`, the script:

1. **Detects or uses specified project type**
2. **Merges templates in order:**
   - Header with source attribution
   - Base patterns (OS, IDE, logs)
   - Security patterns (credentials, secrets)
   - Technology-specific patterns
   - Existing custom entries (preserved)
3. **Creates backup** of original `.gitignore`
4. **Writes merged content** to target

**Important:** Existing custom entries are preserved but appended after standard patterns.

## Using the Validation Tool

### Validate a Single File

```bash
python3 scripts/validate_gitignore.py /path/to/.gitignore
```

**With auto-detection:**
```bash
python3 scripts/validate_gitignore.py /path/to/.gitignore --auto-detect
```

**With specific project type:**
```bash
python3 scripts/validate_gitignore.py /path/to/.gitignore --type python
```

### Scan a Directory

**Scan all `.gitignore` files recursively:**
```bash
python3 scripts/validate_gitignore.py --scan /path/to/repos
```

**With auto-detection of project types:**
```bash
python3 scripts/validate_gitignore.py --scan /path/to/repos --auto-detect
```

**Summary-only output:**
```bash
python3 scripts/validate_gitignore.py --scan /path/to/repos --auto-detect --summary-only
```

### Understanding Validation Results

The validator categorizes issues by severity:

**🔴 CRITICAL** - Security-sensitive patterns (credentials, secrets, keys)
- These MUST be fixed immediately
- Failure to ignore these can expose sensitive data

**⚠️ WARNING** - Important patterns (dependencies, build artifacts, IDE files)
- Should be addressed
- Can cause repository bloat or conflicts

**ℹ️ INFO** - Nice-to-have patterns (editor backups, temporary files)
- Recommended for cleaner repositories
- Lower priority

### Exit Codes

The validation script returns:
- `0` - No issues found
- `1` - Warnings found
- `2` - Critical issues found

This allows integration into CI/CD pipelines:
```bash
python3 scripts/validate_gitignore.py .gitignore --type python || exit 1
```

## Best Practices

### For New Projects

1. Use the distribution script with auto-detection:
   ```bash
   ./copy-prompts.sh --with-gitignore --auto-detect /path/to/new-project
   ```

2. Review and customize the generated `.gitignore`

3. Validate the result:
   ```bash
   python3 scripts/validate_gitignore.py /path/to/new-project/.gitignore --auto-detect
   ```

### For Existing Projects

1. **Backup first:**
   ```bash
   cp /path/to/project/.gitignore /path/to/project/.gitignore.backup
   ```

2. **Run validation to see current state:**
   ```bash
   python3 scripts/validate_gitignore.py /path/to/project/.gitignore --type <type>
   ```

3. **Review critical issues** and add missing security patterns manually, or

4. **Use distribution script** (existing custom entries will be preserved):
   ```bash
   ./copy-prompts.sh --with-gitignore --type <type> /path/to/project
   ```

5. **Review merged file** and remove duplicates if needed

### For Repository Audits

Scan all repositories and generate a report:

```bash
python3 scripts/validate_gitignore.py --scan ~/repos --auto-detect --summary-only > gitignore-audit.txt
```

Filter for critical issues only:
```bash
python3 scripts/validate_gitignore.py --scan ~/repos --auto-detect 2>&1 | grep "CRITICAL"
```

## Customization

### Adding Custom Patterns

After using the distribution script, you can add project-specific patterns:

```gitignore
# Custom project patterns
my-local-config.json
data/raw/
!data/processed/.gitkeep
```

These will be preserved if you re-run the distribution script.

### Using Negation Patterns

To explicitly include files that would otherwise be ignored:

```gitignore
# Ignore all JSON files
*.json

# Except configuration templates
!config.template.json
!.vscode/settings.json
```

### Creating Custom Templates

To create a new technology template:

1. Create `templates/gitignore/mytech.gitignore`
2. Follow the existing format with sections and comments
3. Update the validation script (`scripts/validate_gitignore.py`) to add detection rules
4. Update the distribution script (`copy-prompts.sh`) to add detection logic

## Integration with CI/CD

### GitHub Actions

```yaml
name: Validate .gitignore
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate .gitignore
        run: |
          python3 scripts/validate_gitignore.py .gitignore --type python
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

python3 scripts/validate_gitignore.py .gitignore --auto-detect
if [ $? -eq 2 ]; then
  echo "ERROR: Critical .gitignore issues found. Commit aborted."
  exit 1
fi
```

## Common Issues and Solutions

### Issue: "No project type specified or detected"

**Cause:** The directory doesn't contain recognizable project files.

**Solution:** Use `--type` to manually specify:
```bash
./copy-prompts.sh --with-gitignore --type python /path/to/repo
```

### Issue: Duplicate patterns after merge

**Cause:** Existing `.gitignore` already had some patterns that are in templates.

**Solution:** Manually review and de-duplicate the merged file, or use a tool:
```bash
sort -u .gitignore | grep -v '^$' > .gitignore.dedup
mv .gitignore.dedup .gitignore
```

### Issue: Lock files are being ignored

**Cause:** Some templates include lock file patterns for library projects.

**Solution:** For application projects, add negation patterns:
```gitignore
# Uncomment for applications (not libraries)
!package-lock.json
!yarn.lock
!Pipfile.lock
```

### Issue: Too many patterns, repository specific files ignored

**Cause:** Generic templates may be too broad.

**Solution:** Use negation patterns to explicitly include needed files:
```gitignore
# Include specific vendor libraries
!vendor/mylib/
```

## Security Considerations

### Critical Patterns

These patterns are **non-negotiable** and must be in every `.gitignore`:

```gitignore
# Environment variables
.env
.env.*

# Credentials
*.pem
*.key
credentials.json
secrets.json

# Cloud credentials
.aws/
.azure/
.gcloud/
kubeconfig

# Terraform secrets
*.tfstate
*.tfstate.*
*.tfvars
```

### What NOT to Ignore

**Don't ignore:**
- Lock files (`package-lock.json`, `yarn.lock`) for applications
- `.terraform.lock.hcl` (per Terraform docs)
- Example/template files (`.env.example`, `config.template.json`)
- License files
- Documentation

## Maintenance

### Updating Templates

Templates are based on analysis of 164 real-world `.gitignore` files across multiple technology stacks.

To update templates:

1. Review the analysis report (generated during development)
2. Update template files in `templates/gitignore/`
3. Update validation rules in `scripts/validate_gitignore.py`
4. Test with dry-run on sample projects
5. Commit and distribute

### Versioning

The templates follow semantic versioning via the repository itself. Track changes:

```bash
git log --oneline templates/gitignore/
```

## References

- [Git documentation on .gitignore](https://git-scm.com/docs/gitignore)
- [GitHub's .gitignore templates](https://github.com/github/gitignore)
- [Terraform .gitignore best practices](https://developer.hashicorp.com/terraform/language/settings)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_CheatSheet.html)

## Support

For issues, questions, or contributions:
- File an issue in the repository
- Review existing `.gitignore` patterns in `templates/gitignore/`
- Check validation output for specific recommendations
