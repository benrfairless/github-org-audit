# github-org-audit

A comprehensive tool for auditing GitHub organization configuration, including settings, teams, repositories, permissions, and CODEOWNERS files.

## Features

- **Organization Settings**: Audit organization-level settings including 2FA requirements, repository permissions, and more
- **Team Configuration**: View all teams, their privacy settings, and permissions
- **Repository Configuration**: Audit all repositories including visibility, branch protection, and merge settings
- **Permissions Audit**: Comprehensive view of permissions across the entire organization
- **CODEOWNERS**: Extract and view CODEOWNERS files from all repositories
- **Customizable Output**: Choose between JSON, YAML, or human-readable table formats
- **Flexible Configuration**: Use command-line options or configuration files to customize what data to audit

## Installation

This tool uses [mise](https://mise.jdx.dev/) to manage the Python version and virtual environment.

### Prerequisites

- Python 3.8 or later
- A GitHub personal access token with appropriate permissions

### Option 1: Install with mise (Recommended)

This project uses [mise](https://mise.jdx.dev/) for version management.

1. Install mise (if not already installed):
```bash
curl https://mise.run | sh
```

2. Clone this repository:
```bash
git clone https://github.com/benrfairless/github-org-audit.git
cd github-org-audit
```

3. Install Python and dependencies:
```bash
mise install
mise exec -- pip install -r requirements.txt
mise exec -- pip install -e .
```

### Option 2: Install with pip (Without mise)

If you prefer not to use mise or cannot access the mise installation URL:

1. Clone this repository:
```bash
git clone https://github.com/benrfairless/github-org-audit.git
cd github-org-audit
```

2. Create a virtual environment (optional but recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

### Authentication

You need a GitHub personal access token with appropriate permissions. Set it as an environment variable:

```bash
export GITHUB_TOKEN=your_github_token_here
```

Or pass it directly with the `--token` option.

**Required Permissions**: Your token needs the following scopes:
- `read:org` - Read organization data
- `repo` - Access repository information
- `read:user` - Read user profile data

### Basic Usage

Audit an entire organization:
```bash
github-org-audit audit <organization-name>
```

Or if running from source:
```bash
mise exec -- python -m github_org_audit.cli audit <organization-name>
```

### Command-Line Options

```bash
# Audit with specific components
github-org-audit audit myorg --no-codeowners --no-permissions

# Output to JSON file
github-org-audit audit myorg --output json --output-file audit-results.json

# Include archived repositories
github-org-audit audit myorg --include-archived

# Use custom configuration file
github-org-audit audit myorg --config my-config.yaml
```

### Individual Commands

View specific information without a full audit:

```bash
# View organization settings
github-org-audit settings <organization>

# View teams
github-org-audit teams <organization>

# View repositories
github-org-audit repositories <organization>

# View permissions for a specific repository
github-org-audit permissions <organization> <repository>

# View CODEOWNERS files
github-org-audit codeowners <organization>
github-org-audit codeowners <organization> <repository>
```

### Configuration File

Create a configuration file to customize what information is included in audits:

```yaml
# config.yaml
audit_settings: true
audit_teams: true
audit_repositories: true
audit_permissions: false
audit_codeowners: true
include_archived: false
```

Use it with:
```bash
github-org-audit audit myorg --config config.yaml
```

See `config.example.yaml` for a complete example.

### Output Formats

The tool supports three output formats:

- **table** (default): Human-readable tables
- **json**: Machine-readable JSON format
- **yaml**: YAML format

Example:
```bash
github-org-audit audit myorg --output json > audit.json
github-org-audit audit myorg --output yaml > audit.yaml
```

## Examples

### Full Organization Audit

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
github-org-audit audit my-organization --output json --output-file full-audit.json
```

### Quick Settings Check

```bash
github-org-audit settings my-organization
```

### Find All CODEOWNERS

```bash
github-org-audit codeowners my-organization
```

### Audit Active Repositories Only

```bash
github-org-audit audit my-organization --no-archived
```

## Development

### Running Tests

```bash
mise exec -- python -m pytest
```

### Code Style

This project follows standard Python conventions. Format code with:
```bash
mise exec -- black github_org_audit/
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Security

Never commit your GitHub token to version control. Always use environment variables or secure secret management.
