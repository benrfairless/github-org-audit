# Examples

This directory contains example scripts that demonstrate how to use the GitHub Organization Audit tool programmatically.

## Prerequisites

Make sure you have:
1. Installed the package (`pip install -e .` from the project root)
2. Set your GitHub token: `export GITHUB_TOKEN=your_token_here`

## Available Examples

### basic_audit.py

A simple example that performs a complete organization audit and saves the results to a JSON file.

```bash
python examples/basic_audit.py
```

The script will prompt you for the organization name and then:
- Audit all organization settings
- List all teams
- List all repositories
- Find all CODEOWNERS files
- Save complete results to `audit-{org-name}.json`

### security_check.py

Performs a security-focused audit, checking:
- Two-factor authentication requirements
- Default repository permissions
- Member repository creation settings
- Repository visibility breakdown

```bash
python examples/security_check.py <organization-name>
```

Example output:
```
Security Audit for: my-org
================================================================================
✓ Two-factor authentication is REQUIRED

Default repository permission: read
✓ Default permission is restrictive

Members can create repositories: False
✓ Repository creation is controlled
...
```

### find_missing_codeowners.py

Identifies all repositories that don't have a CODEOWNERS file, useful for improving code ownership coverage.

```bash
python examples/find_missing_codeowners.py <organization-name>
```

Example output:
```
Checking CODEOWNERS for: my-org
================================================================================

Total active repositories: 42
Repositories with CODEOWNERS: 35
Repositories without CODEOWNERS: 7

Repositories missing CODEOWNERS:
--------------------------------------------------------------------------------
  - legacy-app
  - old-scripts
  - prototype-service
  ...

CODEOWNERS coverage: 83.3%
```

## Creating Your Own Scripts

You can use these examples as templates for your own custom audit scripts. The main classes you'll work with are:

```python
from github_org_audit.client import GitHubAuditClient
from github_org_audit.auditor import GitHubOrgAuditor

# Create a client
client = GitHubAuditClient(token)

# Use the client directly for specific queries
settings = client.get_org_settings(org_name)
teams = client.get_teams(org_name)
repos = client.get_repositories(org_name)

# Or use the auditor for comprehensive audits
auditor = GitHubOrgAuditor(client, config)
results = auditor.audit(org_name)
```

## Tips

- Start with small organizations to avoid rate limiting
- Use the `--include-archived` flag carefully as it increases API calls
- Consider caching results for large organizations
- Always handle exceptions when accessing the GitHub API
