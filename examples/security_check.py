#!/usr/bin/env python3
"""
Example: Check organization security settings

This script checks key security settings for a GitHub organization.
"""

import os
import sys
from github_org_audit.client import GitHubAuditClient


def check_security(org_name, token):
    """Check security settings for an organization"""
    client = GitHubAuditClient(token)
    
    print(f"Security Audit for: {org_name}")
    print("=" * 80)
    
    # Get organization settings
    settings = client.get_org_settings(org_name)
    
    # Check 2FA requirement
    if settings.get("two_factor_requirement_enabled"):
        print("✓ Two-factor authentication is REQUIRED")
    else:
        print("✗ WARNING: Two-factor authentication is NOT required")
    
    # Check default repository permission
    default_perm = settings.get("default_repository_permission", "none")
    print(f"\nDefault repository permission: {default_perm}")
    if default_perm in ["read", "none"]:
        print("✓ Default permission is restrictive")
    else:
        print("✗ WARNING: Default permission may be too permissive")
    
    # Check member repository creation
    can_create = settings.get("members_can_create_repositories", False)
    print(f"\nMembers can create repositories: {can_create}")
    if not can_create:
        print("✓ Repository creation is controlled")
    else:
        print("⚠ Members can create repositories")
    
    # Check repository settings
    print("\n" + "=" * 80)
    print("Repository Security Check")
    print("=" * 80)
    
    repos = client.get_repositories(org_name)
    
    private_count = sum(1 for r in repos if r.get("private"))
    public_count = len(repos) - private_count
    archived_count = sum(1 for r in repos if r.get("archived"))
    
    print(f"\nTotal repositories: {len(repos)}")
    print(f"  Private: {private_count}")
    print(f"  Public: {public_count}")
    print(f"  Archived: {archived_count}")
    
    # Check for repositories without branch protection
    print("\nRecommendation: Review branch protection rules for all active repositories")
    
    return 0


def main():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        return 1
    
    if len(sys.argv) < 2:
        print("Usage: python security_check.py <organization-name>")
        return 1
    
    org_name = sys.argv[1]
    
    try:
        return check_security(org_name, token)
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
