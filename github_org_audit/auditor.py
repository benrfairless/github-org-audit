"""Audit functions for GitHub organizations"""

import yaml
from typing import Dict, List, Optional
from .client import GitHubAuditClient


class GitHubOrgAuditor:
    """Auditor for GitHub organizations"""

    def __init__(self, client: GitHubAuditClient, config: Optional[Dict] = None):
        """Initialize the auditor
        
        Args:
            client: GitHubAuditClient instance
            config: Optional configuration dictionary
        """
        self.client = client
        self.config = config or self._default_config()
    
    @staticmethod
    def _default_config() -> Dict:
        """Get default configuration
        
        Returns:
            Default configuration dictionary
        """
        return {
            "audit_settings": True,
            "audit_teams": True,
            "audit_repositories": True,
            "audit_permissions": True,
            "audit_codeowners": True,
            "include_archived": False,
        }
    
    def audit(self, org_name: str) -> Dict:
        """Perform full audit of organization
        
        Args:
            org_name: Name of the organization to audit
            
        Returns:
            Dictionary containing all audit results
        """
        results = {
            "organization": org_name,
            "audit_timestamp": None,
        }
        
        # Audit organization settings
        if self.config.get("audit_settings", True):
            results["settings"] = self.client.get_org_settings(org_name)
        
        # Audit teams
        if self.config.get("audit_teams", True):
            results["teams"] = self.audit_teams(org_name)
        
        # Audit repositories
        if self.config.get("audit_repositories", True):
            results["repositories"] = self.audit_repositories(org_name)
        
        # Audit permissions
        if self.config.get("audit_permissions", True):
            results["permissions"] = self.client.get_org_permissions(org_name)
        
        # Audit CODEOWNERS
        if self.config.get("audit_codeowners", True):
            results["codeowners"] = self.client.get_all_codeowners(org_name)
        
        return results
    
    def audit_teams(self, org_name: str) -> List[Dict]:
        """Audit all teams in the organization
        
        Args:
            org_name: Name of the organization
            
        Returns:
            List of team information with members
        """
        teams = self.client.get_teams(org_name)
        
        # Optionally get team members
        if self.config.get("include_team_members", False):
            for team in teams:
                try:
                    members = self.client.get_team_members(org_name, team["slug"])
                    team["members"] = members
                except Exception as e:
                    team["members"] = []
        
        return teams
    
    def audit_repositories(self, org_name: str) -> List[Dict]:
        """Audit all repositories in the organization
        
        Args:
            org_name: Name of the organization
            
        Returns:
            List of repository information
        """
        repos = self.client.get_repositories(org_name)
        
        # Filter archived repositories if configured
        if not self.config.get("include_archived", False):
            repos = [r for r in repos if not r.get("archived", False)]
        
        return repos
