#!/usr/bin/env python3
"""
Validate .gitignore files against best practices and required patterns.

This script checks .gitignore files for:
1. Required base patterns (OS, IDE, logs, environment files)
2. Security-sensitive patterns (credentials, secrets, keys)
3. Technology-specific patterns based on project type detection
4. Common missing patterns

Usage:
    python3 validate_gitignore.py <path-to-gitignore>
    python3 validate_gitignore.py --scan <directory>
    python3 validate_gitignore.py --scan <directory> --auto-detect
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Severity levels for validation issues."""
    CRITICAL = "CRITICAL"  # Security-sensitive patterns
    WARNING = "WARNING"   # Important but not critical
    INFO = "INFO"         # Nice to have


@dataclass
class ValidationIssue:
    """Represents a validation issue found in a .gitignore file."""
    severity: Severity
    category: str
    pattern: str
    description: str


class ProjectType(Enum):
    """Detected project types."""
    PYTHON = "python"
    NODEJS = "nodejs"
    GO = "go"
    JAVA = "java"
    RUBY = "ruby"
    DOTNET = "dotnet"
    TERRAFORM = "terraform"
    CHEF = "chef"
    UNKNOWN = "unknown"


# Define required patterns by category
REQUIRED_PATTERNS = {
    "base": {
        Severity.WARNING: [
            (".DS_Store", "macOS system files"),
            ("Thumbs.db", "Windows thumbnail cache"),
            ("*.log", "Log files"),
            (".vscode/", "VSCode settings"),
            (".idea/", "IntelliJ IDEA settings"),
        ],
        Severity.INFO: [
            ("*.swp", "Vim swap files"),
            ("*~", "Editor backup files"),
            ("tmp/", "Temporary directory"),
            ("temp/", "Temporary directory"),
        ],
    },
    "security": {
        Severity.CRITICAL: [
            (".env", "Environment variables (may contain secrets)"),
            ("*.pem", "Certificate/key files"),
            ("*.key", "Private key files"),
            ("credentials.json", "Credentials file"),
            ("secrets.json", "Secrets file"),
            (".aws/", "AWS credentials directory"),
            (".azure/", "Azure credentials directory"),
            ("kubeconfig", "Kubernetes configuration"),
        ],
    },
    "python": {
        Severity.WARNING: [
            ("__pycache__/", "Python bytecode cache"),
            ("*.pyc", "Compiled Python files"),
            ("*.py[cod]", "Compiled Python files (all variants)"),
            (".venv", "Virtual environment"),
            ("venv/", "Virtual environment"),
            ("*.egg-info/", "Python package metadata"),
            (".pytest_cache/", "Pytest cache"),
        ],
    },
    "nodejs": {
        Severity.WARNING: [
            ("node_modules/", "Node.js dependencies"),
            ("npm-debug.log*", "NPM debug logs"),
            ("yarn-debug.log*", "Yarn debug logs"),
            ("dist/", "Build output"),
            ("build/", "Build output"),
        ],
    },
    "go": {
        Severity.WARNING: [
            ("*.exe", "Go compiled binaries"),
            ("*.test", "Go test binaries"),
            ("*.out", "Go coverage output"),
            ("vendor/", "Go vendor directory"),
            ("go.work", "Go workspace file"),
        ],
    },
    "java": {
        Severity.WARNING: [
            ("*.class", "Compiled Java classes"),
            ("target/", "Maven build directory"),
            (".gradle", "Gradle cache"),
            ("*.jar", "JAR files (unless library JARs needed)"),
            ("*.war", "WAR files"),
        ],
    },
    "ruby": {
        Severity.WARNING: [
            (".bundle/", "Bundler directory"),
            ("vendor/bundle/", "Bundler vendor directory"),
            ("*.gem", "Ruby gems"),
            (".vagrant", "Vagrant directory"),
            (".kitchen/", "Test Kitchen directory"),
        ],
    },
    "dotnet": {
        Severity.WARNING: [
            ("bin/", ".NET build output"),
            ("obj/", ".NET object files"),
            ("*.suo", "Visual Studio user options"),
            ("*.user", "Visual Studio user settings"),
        ],
    },
    "terraform": {
        Severity.CRITICAL: [
            ("*.tfstate", "Terraform state files (contain sensitive data)"),
            ("*.tfstate.*", "Terraform state backups"),
            ("*.tfvars", "Terraform variables (may contain secrets)"),
        ],
        Severity.WARNING: [
            ("**/.terraform/*", "Terraform plugin directory"),
            ("crash.log", "Terraform crash logs"),
            ("*tfplan*", "Terraform plan files"),
        ],
    },
    "chef": {
        Severity.CRITICAL: [
            (".chef/*.pem", "Chef private keys"),
            (".chef/encrypted_data_bag_secret", "Chef encrypted data bag secret"),
        ],
        Severity.WARNING: [
            ("Berksfile.lock", "Berkshelf lock file"),
            (".kitchen/", "Test Kitchen directory"),
        ],
    },
}


class GitignoreValidator:
    """Validates .gitignore files against best practices."""

    def __init__(self, gitignore_path: Path):
        self.path = gitignore_path
        self.content = self._read_file()
        self.patterns = self._extract_patterns()
        self.issues: List[ValidationIssue] = []

    def _read_file(self) -> str:
        """Read the .gitignore file."""
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {self.path}: {e}", file=sys.stderr)
            sys.exit(1)

    def _extract_patterns(self) -> Set[str]:
        """Extract all non-comment, non-empty patterns from .gitignore."""
        patterns = set()
        for line in self.content.split('\n'):
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                # Remove negation prefix for pattern matching
                if line.startswith('!'):
                    line = line[1:]
                patterns.add(line)
        return patterns

    def _pattern_exists(self, pattern: str) -> bool:
        """Check if a pattern or similar pattern exists in .gitignore."""
        # Direct match
        if pattern in self.patterns:
            return True

        # Check for wildcarded versions
        pattern_base = pattern.rstrip('/*')
        for existing in self.patterns:
            existing_base = existing.rstrip('/*')
            if pattern_base == existing_base:
                return True
            # Check if pattern is covered by more general pattern
            if pattern.startswith(existing_base + '/') or existing.startswith(pattern_base + '/'):
                return True

        return False

    def validate_category(self, category: str, patterns_by_severity: Dict[Severity, List[Tuple[str, str]]]):
        """Validate patterns for a specific category."""
        for severity, patterns in patterns_by_severity.items():
            for pattern, description in patterns:
                if not self._pattern_exists(pattern):
                    self.issues.append(ValidationIssue(
                        severity=severity,
                        category=category,
                        pattern=pattern,
                        description=description
                    ))

    def validate_base_patterns(self):
        """Validate base patterns that should be in all .gitignore files."""
        self.validate_category("base", REQUIRED_PATTERNS["base"])

    def validate_security_patterns(self):
        """Validate security-critical patterns."""
        self.validate_category("security", REQUIRED_PATTERNS["security"])

    def validate_technology_patterns(self, project_type: ProjectType):
        """Validate technology-specific patterns."""
        if project_type == ProjectType.UNKNOWN:
            return

        tech_key = project_type.value
        if tech_key in REQUIRED_PATTERNS:
            self.validate_category(tech_key, REQUIRED_PATTERNS[tech_key])

    def validate_all(self, project_type: ProjectType = ProjectType.UNKNOWN):
        """Run all validations."""
        self.validate_base_patterns()
        self.validate_security_patterns()
        self.validate_technology_patterns(project_type)

    def get_summary(self) -> Dict[str, int]:
        """Get summary of issues by severity."""
        summary = {
            "CRITICAL": 0,
            "WARNING": 0,
            "INFO": 0
        }
        for issue in self.issues:
            summary[issue.severity.value] += 1
        return summary

    def print_report(self, verbose: bool = False):
        """Print validation report."""
        if not self.issues:
            print(f"✅ {self.path}: No issues found")
            return

        print(f"\n{'='*80}")
        print(f"Validation Report: {self.path}")
        print(f"{'='*80}")

        # Group issues by severity
        issues_by_severity = {
            Severity.CRITICAL: [],
            Severity.WARNING: [],
            Severity.INFO: []
        }
        for issue in self.issues:
            issues_by_severity[issue.severity].append(issue)

        # Print critical issues first
        for severity in [Severity.CRITICAL, Severity.WARNING, Severity.INFO]:
            issues = issues_by_severity[severity]
            if not issues and not verbose:
                continue

            icon = "🔴" if severity == Severity.CRITICAL else "⚠️" if severity == Severity.WARNING else "ℹ️"
            print(f"\n{icon} {severity.value} ({len(issues)} issues)")
            print("-" * 80)

            for issue in issues:
                print(f"  [{issue.category}] Missing pattern: {issue.pattern}")
                print(f"      → {issue.description}")

        # Print summary
        summary = self.get_summary()
        print(f"\n{'='*80}")
        print("Summary:")
        print(f"  CRITICAL: {summary['CRITICAL']}")
        print(f"  WARNING:  {summary['WARNING']}")
        print(f"  INFO:     {summary['INFO']}")
        print(f"{'='*80}\n")


class ProjectTypeDetector:
    """Detect project type based on directory contents."""

    def __init__(self, directory: Path):
        self.directory = directory

    def detect(self) -> ProjectType:
        """Detect the primary project type."""
        detection_rules = [
            (self._is_terraform, ProjectType.TERRAFORM),
            (self._is_python, ProjectType.PYTHON),
            (self._is_nodejs, ProjectType.NODEJS),
            (self._is_go, ProjectType.GO),
            (self._is_java, ProjectType.JAVA),
            (self._is_ruby, ProjectType.RUBY),
            (self._is_chef, ProjectType.CHEF),
            (self._is_dotnet, ProjectType.DOTNET),
        ]

        for detector, project_type in detection_rules:
            if detector():
                return project_type

        return ProjectType.UNKNOWN

    def _is_terraform(self) -> bool:
        """Check if directory contains Terraform files."""
        return any(self.directory.glob("*.tf"))

    def _is_python(self) -> bool:
        """Check if directory contains Python project files."""
        indicators = [
            "setup.py", "pyproject.toml", "requirements.txt",
            "Pipfile", "poetry.lock", "setup.cfg"
        ]
        return any((self.directory / indicator).exists() for indicator in indicators)

    def _is_nodejs(self) -> bool:
        """Check if directory contains Node.js project files."""
        return (self.directory / "package.json").exists()

    def _is_go(self) -> bool:
        """Check if directory contains Go project files."""
        return (self.directory / "go.mod").exists()

    def _is_java(self) -> bool:
        """Check if directory contains Java project files."""
        return (self.directory / "pom.xml").exists() or (self.directory / "build.gradle").exists()

    def _is_ruby(self) -> bool:
        """Check if directory contains Ruby project files."""
        return (self.directory / "Gemfile").exists()

    def _is_chef(self) -> bool:
        """Check if directory contains Chef files."""
        return (self.directory / "metadata.rb").exists() or (self.directory / "Berksfile").exists()

    def _is_dotnet(self) -> bool:
        """Check if directory contains .NET project files."""
        return any(self.directory.glob("*.csproj")) or any(self.directory.glob("*.sln"))


def scan_directory(directory: Path, auto_detect: bool = False) -> List[Tuple[Path, ProjectType]]:
    """Scan directory for .gitignore files."""
    gitignore_files = []

    for gitignore in directory.rglob(".gitignore"):
        if auto_detect:
            detector = ProjectTypeDetector(gitignore.parent)
            project_type = detector.detect()
        else:
            project_type = ProjectType.UNKNOWN

        gitignore_files.append((gitignore, project_type))

    return gitignore_files


def main():
    parser = argparse.ArgumentParser(
        description="Validate .gitignore files against best practices",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a single .gitignore file
  python3 validate_gitignore.py /path/to/.gitignore

  # Scan a directory for all .gitignore files
  python3 validate_gitignore.py --scan /path/to/repos

  # Scan with auto-detection of project types
  python3 validate_gitignore.py --scan /path/to/repos --auto-detect

  # Specify project type manually
  python3 validate_gitignore.py /path/to/.gitignore --type python

  # Verbose output (show all categories even if no issues)
  python3 validate_gitignore.py /path/to/.gitignore --verbose
        """
    )

    parser.add_argument(
        "path",
        nargs="?",
        help="Path to .gitignore file or directory to scan"
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Scan directory recursively for all .gitignore files"
    )
    parser.add_argument(
        "--auto-detect",
        action="store_true",
        help="Auto-detect project type (use with --scan)"
    )
    parser.add_argument(
        "--type",
        choices=[t.value for t in ProjectType],
        help="Manually specify project type"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Show only summary statistics"
    )

    args = parser.parse_args()

    if not args.path:
        parser.print_help()
        sys.exit(1)

    path = Path(args.path).resolve()

    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    # Determine project type
    project_type = ProjectType.UNKNOWN
    if args.type:
        project_type = ProjectType(args.type)

    if args.scan or path.is_dir():
        # Scan directory
        gitignore_files = scan_directory(path, args.auto_detect)

        if not gitignore_files:
            print(f"No .gitignore files found in {path}")
            sys.exit(0)

        print(f"Found {len(gitignore_files)} .gitignore file(s)\n")

        total_issues = {"CRITICAL": 0, "WARNING": 0, "INFO": 0}

        for gitignore_path, detected_type in gitignore_files:
            pt = detected_type if args.auto_detect else project_type

            validator = GitignoreValidator(gitignore_path)
            validator.validate_all(pt)

            if not args.summary_only:
                validator.print_report(args.verbose)
            else:
                summary = validator.get_summary()
                if any(summary.values()):
                    print(f"{gitignore_path}: C:{summary['CRITICAL']} W:{summary['WARNING']} I:{summary['INFO']}")

            # Update totals
            summary = validator.get_summary()
            for key in total_issues:
                total_issues[key] += summary[key]

        # Print overall summary
        print(f"\n{'='*80}")
        print("Overall Summary:")
        print(f"  Files scanned: {len(gitignore_files)}")
        print(f"  CRITICAL: {total_issues['CRITICAL']}")
        print(f"  WARNING:  {total_issues['WARNING']}")
        print(f"  INFO:     {total_issues['INFO']}")
        print(f"{'='*80}\n")

    else:
        # Validate single file
        if args.auto_detect:
            detector = ProjectTypeDetector(path.parent)
            project_type = detector.detect()
            if args.verbose:
                print(f"Detected project type: {project_type.value}")

        validator = GitignoreValidator(path)
        validator.validate_all(project_type)
        validator.print_report(args.verbose)

        # Exit with error code if critical issues found
        summary = validator.get_summary()
        if summary["CRITICAL"] > 0:
            sys.exit(2)
        elif summary["WARNING"] > 0:
            sys.exit(1)


if __name__ == "__main__":
    main()
