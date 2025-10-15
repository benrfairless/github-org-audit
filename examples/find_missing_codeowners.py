#!/usr/bin/env python3
"""
Example: Find repositories missing CODEOWNERS

This script identifies all repositories in an organization that don't have
a CODEOWNERS file.
"""

import os
import sys
from github_org_audit.client import GitHubAuditClient


def find_missing_codeowners(org_name, token):
    """Find repositories without CODEOWNERS files"""
    client = GitHubAuditClient(token)
    
    print(f"Checking CODEOWNERS for: {org_name}")
    print("=" * 80)
    
    # Get all repositories
    repos = client.get_repositories(org_name)
    
    # Filter out archived repositories
    active_repos = [r for r in repos if not r.get("archived")]
    
    print(f"\nTotal active repositories: {len(active_repos)}")
    
    # Check for CODEOWNERS
    missing_codeowners = []
    has_codeowners = []
    
    for repo in active_repos:
        repo_name = repo["name"]
        codeowners = client.get_codeowners(org_name, repo_name)
        
        if codeowners:
            has_codeowners.append(repo_name)
        else:
            missing_codeowners.append(repo_name)
    
    print(f"Repositories with CODEOWNERS: {len(has_codeowners)}")
    print(f"Repositories without CODEOWNERS: {len(missing_codeowners)}")
    
    if missing_codeowners:
        print("\nRepositories missing CODEOWNERS:")
        print("-" * 80)
        for repo_name in sorted(missing_codeowners):
            print(f"  - {repo_name}")
    
    # Calculate coverage percentage
    coverage = (len(has_codeowners) / len(active_repos) * 100) if active_repos else 0
    print(f"\nCODEOWNERS coverage: {coverage:.1f}%")
    
    return 0


def main():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        return 1
    
    if len(sys.argv) < 2:
        print("Usage: python find_missing_codeowners.py <organization-name>")
        return 1
    
    org_name = sys.argv[1]
    
    try:
        return find_missing_codeowners(org_name, token)
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
