"""Command-line interface for GitHub organization audit tool"""

import click
import json
import yaml
import os
from pathlib import Path
from tabulate import tabulate
from .client import GitHubAuditClient
from .auditor import GitHubOrgAuditor


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """GitHub Organization Audit Tool
    
    Audit GitHub organization settings, teams, repositories, permissions, and CODEOWNERS.
    """
    pass


@cli.command()
@click.argument("organization")
@click.option(
    "--token",
    envvar="GITHUB_TOKEN",
    required=True,
    help="GitHub personal access token (or set GITHUB_TOKEN env var)",
)
@click.option(
    "--config",
    type=click.Path(exists=True),
    help="Path to configuration file (YAML)",
)
@click.option(
    "--output",
    type=click.Choice(["json", "yaml", "table"]),
    default="table",
    help="Output format (default: table)",
)
@click.option(
    "--output-file",
    type=click.Path(),
    help="Write output to file instead of stdout",
)
@click.option(
    "--settings/--no-settings",
    default=True,
    help="Include organization settings in audit",
)
@click.option(
    "--teams/--no-teams",
    default=True,
    help="Include team configuration in audit",
)
@click.option(
    "--repositories/--no-repositories",
    default=True,
    help="Include repository configuration in audit",
)
@click.option(
    "--permissions/--no-permissions",
    default=True,
    help="Include permissions in audit",
)
@click.option(
    "--codeowners/--no-codeowners",
    default=True,
    help="Include CODEOWNERS files in audit",
)
@click.option(
    "--include-archived/--no-archived",
    default=False,
    help="Include archived repositories",
)
def audit(
    organization,
    token,
    config,
    output,
    output_file,
    settings,
    teams,
    repositories,
    permissions,
    codeowners,
    include_archived,
):
    """Audit a GitHub organization
    
    ORGANIZATION: Name of the GitHub organization to audit
    """
    # Load configuration
    audit_config = {}
    if config:
        with open(config, 'r') as f:
            audit_config = yaml.safe_load(f)
    
    # Override with command-line options
    audit_config.update({
        "audit_settings": settings,
        "audit_teams": teams,
        "audit_repositories": repositories,
        "audit_permissions": permissions,
        "audit_codeowners": codeowners,
        "include_archived": include_archived,
    })
    
    # Create client and auditor
    client = GitHubAuditClient(token)
    auditor = GitHubOrgAuditor(client, audit_config)
    
    # Perform audit
    click.echo(f"Auditing organization: {organization}")
    results = auditor.audit(organization)
    
    # Format output
    if output == "json":
        output_text = json.dumps(results, indent=2, default=str)
    elif output == "yaml":
        output_text = yaml.dump(results, default_flow_style=False)
    else:  # table
        output_text = format_table_output(results)
    
    # Write output
    if output_file:
        with open(output_file, 'w') as f:
            f.write(output_text)
        click.echo(f"Audit results written to: {output_file}")
    else:
        click.echo("\n" + output_text)


@cli.command()
@click.argument("organization")
@click.option(
    "--token",
    envvar="GITHUB_TOKEN",
    required=True,
    help="GitHub personal access token (or set GITHUB_TOKEN env var)",
)
def settings(organization, token):
    """Show organization settings"""
    client = GitHubAuditClient(token)
    settings = client.get_org_settings(organization)
    
    # Format as table
    table_data = [[k, v] for k, v in settings.items()]
    click.echo(tabulate(table_data, headers=["Setting", "Value"], tablefmt="grid"))


@cli.command()
@click.argument("organization")
@click.option(
    "--token",
    envvar="GITHUB_TOKEN",
    required=True,
    help="GitHub personal access token (or set GITHUB_TOKEN env var)",
)
def teams(organization, token):
    """Show organization teams"""
    client = GitHubAuditClient(token)
    teams = client.get_teams(organization)
    
    # Format as table
    headers = ["Name", "Slug", "Privacy", "Permission", "Members", "Repos"]
    table_data = [
        [
            t["name"],
            t["slug"],
            t["privacy"],
            t["permission"],
            t["members_count"],
            t["repos_count"],
        ]
        for t in teams
    ]
    click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))


@cli.command()
@click.argument("organization")
@click.option(
    "--token",
    envvar="GITHUB_TOKEN",
    required=True,
    help="GitHub personal access token (or set GITHUB_TOKEN env var)",
)
@click.option(
    "--include-archived/--no-archived",
    default=False,
    help="Include archived repositories",
)
def repositories(organization, token, include_archived):
    """Show organization repositories"""
    client = GitHubAuditClient(token)
    repos = client.get_repositories(organization)
    
    # Filter archived if needed
    if not include_archived:
        repos = [r for r in repos if not r.get("archived", False)]
    
    # Format as table
    headers = ["Name", "Private", "Archived", "Default Branch", "Visibility"]
    table_data = [
        [
            r["name"],
            r["private"],
            r["archived"],
            r["default_branch"],
            r["visibility"],
        ]
        for r in repos
    ]
    click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))


@cli.command()
@click.argument("organization")
@click.argument("repository")
@click.option(
    "--token",
    envvar="GITHUB_TOKEN",
    required=True,
    help="GitHub personal access token (or set GITHUB_TOKEN env var)",
)
def permissions(organization, repository, token):
    """Show repository permissions
    
    ORGANIZATION: Name of the GitHub organization
    REPOSITORY: Name of the repository
    """
    client = GitHubAuditClient(token)
    perms = client.get_repository_permissions(organization, repository)
    
    click.echo(f"\nRepository: {perms['repository']}")
    
    # Collaborators
    if perms["collaborators"]:
        click.echo("\nCollaborators:")
        headers = ["Login", "Permission"]
        table_data = [[c["login"], c["permissions"]] for c in perms["collaborators"]]
        click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Teams
    if perms["teams"]:
        click.echo("\nTeams:")
        headers = ["Name", "Permission"]
        table_data = [[t["name"], t["permission"]] for t in perms["teams"]]
        click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))


@cli.command()
@click.argument("organization")
@click.argument("repository", required=False)
@click.option(
    "--token",
    envvar="GITHUB_TOKEN",
    required=True,
    help="GitHub personal access token (or set GITHUB_TOKEN env var)",
)
def codeowners(organization, repository, token):
    """Show CODEOWNERS files
    
    ORGANIZATION: Name of the GitHub organization
    REPOSITORY: (Optional) Name of specific repository, or all if not provided
    """
    client = GitHubAuditClient(token)
    
    if repository:
        # Show single repository
        content = client.get_codeowners(organization, repository)
        if content:
            click.echo(f"\nCODEOWNERS for {repository}:")
            click.echo("=" * 80)
            click.echo(content)
        else:
            click.echo(f"No CODEOWNERS file found for {repository}")
    else:
        # Show all repositories
        all_codeowners = client.get_all_codeowners(organization)
        if all_codeowners:
            for repo_name, content in all_codeowners.items():
                click.echo(f"\nCODEOWNERS for {repo_name}:")
                click.echo("=" * 80)
                click.echo(content)
                click.echo("")
        else:
            click.echo("No CODEOWNERS files found in organization")


def format_table_output(results: dict) -> str:
    """Format audit results as human-readable tables
    
    Args:
        results: Audit results dictionary
        
    Returns:
        Formatted string with tables
    """
    output = []
    
    # Organization settings
    if "settings" in results:
        output.append("Organization Settings")
        output.append("=" * 80)
        settings_data = [[k, v] for k, v in results["settings"].items()]
        output.append(tabulate(settings_data, headers=["Setting", "Value"], tablefmt="grid"))
        output.append("")
    
    # Teams
    if "teams" in results:
        output.append("Teams")
        output.append("=" * 80)
        if results["teams"]:
            headers = ["Name", "Slug", "Privacy", "Permission", "Members", "Repos"]
            teams_data = [
                [
                    t["name"],
                    t["slug"],
                    t["privacy"],
                    t["permission"],
                    t["members_count"],
                    t["repos_count"],
                ]
                for t in results["teams"]
            ]
            output.append(tabulate(teams_data, headers=headers, tablefmt="grid"))
        else:
            output.append("No teams found")
        output.append("")
    
    # Repositories
    if "repositories" in results:
        output.append("Repositories")
        output.append("=" * 80)
        if results["repositories"]:
            headers = ["Name", "Private", "Archived", "Default Branch", "Visibility"]
            repos_data = [
                [
                    r["name"],
                    r["private"],
                    r["archived"],
                    r["default_branch"],
                    r["visibility"],
                ]
                for r in results["repositories"]
            ]
            output.append(tabulate(repos_data, headers=headers, tablefmt="grid"))
            output.append(f"\nTotal repositories: {len(results['repositories'])}")
        else:
            output.append("No repositories found")
        output.append("")
    
    # Permissions summary
    if "permissions" in results:
        output.append("Permissions Summary")
        output.append("=" * 80)
        output.append(f"Total repositories with permissions: {len(results['permissions'])}")
        output.append("")
    
    # CODEOWNERS summary
    if "codeowners" in results:
        output.append("CODEOWNERS Summary")
        output.append("=" * 80)
        if results["codeowners"]:
            output.append(f"Repositories with CODEOWNERS: {len(results['codeowners'])}")
            for repo_name in results["codeowners"].keys():
                output.append(f"  - {repo_name}")
        else:
            output.append("No CODEOWNERS files found")
        output.append("")
    
    return "\n".join(output)


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()
