# Contributing to GitHub Organization Audit

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/github-org-audit.git`
3. Set up the development environment:
   ```bash
   cd github-org-audit
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install -e .
   ```

## Development Workflow

1. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Test your changes:
   ```bash
   # Test the CLI
   github-org-audit --help
   
   # Test with a real organization (requires GITHUB_TOKEN)
   export GITHUB_TOKEN=your_token
   github-org-audit settings your-org
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request on GitHub

## Code Style

- Follow PEP 8 style guidelines for Python code
- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Add comments for complex logic

Example:
```python
def get_org_settings(self, org_name: str) -> dict:
    """Get organization settings
    
    Args:
        org_name: Name of the organization
        
    Returns:
        Dictionary containing organization settings
    """
    # Implementation
```

## Project Structure

```
github-org-audit/
├── github_org_audit/       # Main package
│   ├── __init__.py        # Package initialization
│   ├── client.py          # GitHub API client wrapper
│   ├── auditor.py         # Audit logic
│   └── cli.py             # Command-line interface
├── examples/              # Example scripts
├── .github/workflows/     # CI/CD workflows
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup
└── README.md             # Main documentation
```

## Adding New Features

When adding new features:

1. **API Client** (`client.py`): Add new methods to `GitHubAuditClient` for accessing GitHub API
2. **Auditor** (`auditor.py`): Add audit logic to `GitHubOrgAuditor` if needed
3. **CLI** (`cli.py`): Add new commands or options to the CLI
4. **Documentation**: Update README.md and add examples if applicable

### Example: Adding a New Audit Feature

1. Add a method to `GitHubAuditClient`:
```python
def get_branch_protections(self, org_name: str, repo_name: str) -> dict:
    """Get branch protection rules for a repository"""
    # Implementation
```

2. Use it in `GitHubOrgAuditor` if needed:
```python
def audit_branch_protections(self, org_name: str) -> list:
    """Audit branch protection rules across all repositories"""
    # Implementation
```

3. Add a CLI command in `cli.py`:
```python
@cli.command()
def branch_protections(organization, token):
    """Show branch protection rules"""
    # Implementation
```

## Testing

Currently, the project uses manual testing with real GitHub organizations. When adding new features:

1. Test with a real GitHub organization (use a test org if possible)
2. Test error handling (invalid tokens, missing permissions, etc.)
3. Test edge cases (empty organizations, archived repos, etc.)

## Dependencies

When adding new dependencies:

1. Add to `requirements.txt`
2. Update `setup.py` with the same version
3. Ensure the dependency is necessary and well-maintained
4. Document why the dependency is needed in your PR

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all new functions and classes
- Create examples for new features
- Update QUICKSTART.md if installation/usage changes

## Pull Request Guidelines

Your PR should:

- Have a clear title and description
- Reference any related issues
- Include examples or screenshots if applicable
- Be focused on a single feature or fix
- Pass all existing tests
- Include documentation updates

## Questions?

If you have questions, please:
- Open an issue for discussion
- Check existing issues and PRs
- Review the documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
