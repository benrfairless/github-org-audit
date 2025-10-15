#!/usr/bin/env python3
"""
Example: Basic organization audit

This script demonstrates how to use the GitHubAuditClient and GitHubOrgAuditor
programmatically (without using the CLI).
"""

import os
import json
from github_org_audit.client import GitHubAuditClient
from github_org_audit.auditor import GitHubOrgAuditor


def main():
    # Get GitHub token from environment
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        print("Set it with: export GITHUB_TOKEN=your_token_here")
        return 1
    
    # Organization to audit
    org_name = input("Enter organization name to audit: ")
    
    # Create client and auditor
    client = GitHubAuditClient(token)
    auditor = GitHubOrgAuditor(client)
    
    print(f"\nAuditing organization: {org_name}")
    print("This may take a few moments...\n")
    
    # Perform audit
    try:
        results = auditor.audit(org_name)
        
        # Display summary
        print("=" * 80)
        print("AUDIT SUMMARY")
        print("=" * 80)
        
        if "settings" in results:
            settings = results["settings"]
            print(f"\nOrganization: {settings.get('name', 'N/A')}")
            print(f"Login: {settings.get('login', 'N/A')}")
            print(f"Public Repos: {settings.get('public_repos', 0)}")
            print(f"Private Repos: {settings.get('private_repos', 0)}")
            print(f"2FA Required: {settings.get('two_factor_requirement_enabled', False)}")
        
        if "teams" in results:
            print(f"\nTotal Teams: {len(results['teams'])}")
        
        if "repositories" in results:
            print(f"Total Repositories: {len(results['repositories'])}")
        
        if "codeowners" in results:
            print(f"Repositories with CODEOWNERS: {len(results['codeowners'])}")
        
        print("\n" + "=" * 80)
        
        # Save full results to JSON
        output_file = f"audit-{org_name}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\nFull audit results saved to: {output_file}")
        
    except Exception as e:
        print(f"Error during audit: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
