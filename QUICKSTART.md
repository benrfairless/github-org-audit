# Quick Start Guide

This guide will help you get started with the GitHub Organization Audit tool.

## Prerequisites

1. **GitHub Personal Access Token**: You'll need a GitHub personal access token with the following scopes:
   - `read:org` - Read organization data
   - `repo` - Access repository information
   - `read:user` - Read user profile data

   Create a token at: https://github.com/settings/tokens

2. **Python 3.8+**: The tool requires Python 3.8 or later.

3. **mise (optional but recommended)**: Install mise for automatic Python version management.

## Installation

### Option 1: Using mise (Recommended)

```bash
# Install mise
curl https://mise.run | sh

# Clone the repository
git clone https://github.com/benrfairless/github-org-audit.git
cd github-org-audit

# Install Python and dependencies
mise install
mise exec -- pip install -r requirements.txt

# Install the package
mise exec -- pip install -e .
```

### Option 2: Using pip directly

```bash
# Clone the repository
git clone https://github.com/benrfairless/github-org-audit.git
cd github-org-audit

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Basic Usage

### 1. Set up your GitHub token

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

### 2. Run your first audit

Audit an organization with all default options:
```bash
github-org-audit audit your-org-name
```

### 3. View specific information

View just the organization settings:
```bash
github-org-audit settings your-org-name
```

View teams:
```bash
github-org-audit teams your-org-name
```

View repositories:
```bash
github-org-audit repositories your-org-name
```

### 4. Customize your audit

Save results to a JSON file:
```bash
github-org-audit audit your-org-name --output json --output-file audit.json
```

Exclude certain components:
```bash
github-org-audit audit your-org-name --no-codeowners --no-permissions
```

Include archived repositories:
```bash
github-org-audit audit your-org-name --include-archived
```

### 5. Use a configuration file

Create a file called `my-config.yaml`:
```yaml
audit_settings: true
audit_teams: true
audit_repositories: true
audit_permissions: false
audit_codeowners: true
include_archived: false
```

Run with configuration:
```bash
github-org-audit audit your-org-name --config my-config.yaml
```

## Common Use Cases

### Security Audit

Check 2FA requirements and repository settings:
```bash
github-org-audit audit your-org --output json | jq '.settings.two_factor_requirement_enabled'
```

### Permission Review

Review all repository permissions:
```bash
github-org-audit audit your-org --no-settings --no-teams --no-repositories --no-codeowners --output table
```

### CODEOWNERS Coverage

Find all repositories with CODEOWNERS files:
```bash
github-org-audit codeowners your-org
```

### Export for Analysis

Export complete audit data for external analysis:
```bash
github-org-audit audit your-org --output json --output-file full-audit-$(date +%Y%m%d).json
```

## Troubleshooting

### Authentication Issues

If you get authentication errors:
- Verify your token is set: `echo $GITHUB_TOKEN`
- Check token has correct scopes: https://github.com/settings/tokens
- Ensure token hasn't expired

### Rate Limiting

GitHub API has rate limits. For large organizations:
- Use authenticated requests (token provides higher limits)
- Consider running audits during off-peak hours
- Break up audits into smaller components

### Permission Denied

If you can't access certain repositories:
- Verify your token has `repo` scope
- Ensure you're a member of the organization
- Some repositories may require additional permissions

## Next Steps

- Read the full [README.md](README.md) for comprehensive documentation
- Review [config.example.yaml](config.example.yaml) for all configuration options
- Integrate audit results into your CI/CD pipeline
- Set up scheduled audits for compliance monitoring
