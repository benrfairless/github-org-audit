"""GitHub API client wrapper for auditing"""

from github import Github
from typing import Optional


class GitHubAuditClient:
    """Client for auditing GitHub organizations"""

    def __init__(self, token: str):
        """Initialize the GitHub client with authentication token
        
        Args:
            token: GitHub personal access token
        """
        self.client = Github(token)
        
    def get_organization(self, org_name: str):
        """Get organization object
        
        Args:
            org_name: Name of the organization
            
        Returns:
            GitHub organization object
        """
        return self.client.get_organization(org_name)
    
    def get_org_settings(self, org_name: str) -> dict:
        """Get organization settings
        
        Args:
            org_name: Name of the organization
            
        Returns:
            Dictionary containing organization settings
        """
        org = self.get_organization(org_name)
        
        settings = {
            "name": org.name,
            "login": org.login,
            "description": org.description,
            "email": org.email,
            "billing_email": org.billing_email,
            "company": org.company,
            "location": org.location,
            "blog": org.blog,
            "created_at": str(org.created_at),
            "updated_at": str(org.updated_at),
            "public_repos": org.public_repos,
            "private_repos": org.total_private_repos,
            "followers": org.followers,
            "following": org.following,
            "default_repository_permission": org.default_repository_permission,
            "members_can_create_repositories": org.members_can_create_repositories,
            "two_factor_requirement_enabled": org.two_factor_requirement_enabled,
            "has_organization_projects": org.has_organization_projects,
            "has_repository_projects": org.has_repository_projects,
        }
        
        return settings
    
    def get_teams(self, org_name: str) -> list:
        """Get all teams in the organization
        
        Args:
            org_name: Name of the organization
            
        Returns:
            List of team information dictionaries
        """
        org = self.get_organization(org_name)
        teams = []
        
        for team in org.get_teams():
            team_info = {
                "name": team.name,
                "slug": team.slug,
                "description": team.description,
                "privacy": team.privacy,
                "permission": team.permission,
                "members_count": team.members_count,
                "repos_count": team.repos_count,
            }
            teams.append(team_info)
        
        return teams
    
    def get_team_members(self, org_name: str, team_slug: str) -> list:
        """Get members of a specific team
        
        Args:
            org_name: Name of the organization
            team_slug: Slug of the team
            
        Returns:
            List of team member information
        """
        org = self.get_organization(org_name)
        team = org.get_team_by_slug(team_slug)
        members = []
        
        for member in team.get_members():
            member_info = {
                "login": member.login,
                "name": member.name,
                "role": "member",  # PyGithub doesn't expose role directly
            }
            members.append(member_info)
        
        return members
    
    def get_repositories(self, org_name: str) -> list:
        """Get all repositories in the organization
        
        Args:
            org_name: Name of the organization
            
        Returns:
            List of repository information dictionaries
        """
        org = self.get_organization(org_name)
        repos = []
        
        for repo in org.get_repos():
            repo_info = {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "private": repo.private,
                "archived": repo.archived,
                "disabled": repo.disabled,
                "default_branch": repo.default_branch,
                "visibility": repo.visibility,
                "allow_merge_commit": repo.allow_merge_commit,
                "allow_squash_merge": repo.allow_squash_merge,
                "allow_rebase_merge": repo.allow_rebase_merge,
                "delete_branch_on_merge": repo.delete_branch_on_merge,
                "has_issues": repo.has_issues,
                "has_projects": repo.has_projects,
                "has_wiki": repo.has_wiki,
                "has_downloads": repo.has_downloads,
            }
            repos.append(repo_info)
        
        return repos
    
    def get_repository_permissions(self, org_name: str, repo_name: str) -> dict:
        """Get permissions for a specific repository
        
        Args:
            org_name: Name of the organization
            repo_name: Name of the repository
            
        Returns:
            Dictionary containing repository permissions
        """
        org = self.get_organization(org_name)
        repo = org.get_repo(repo_name)
        
        permissions = {
            "repository": repo_name,
            "collaborators": [],
            "teams": [],
        }
        
        # Get direct collaborators
        for collab in repo.get_collaborators():
            collab_info = {
                "login": collab.login,
                "permissions": repo.get_collaborator_permission(collab),
            }
            permissions["collaborators"].append(collab_info)
        
        # Get teams with access
        for team in repo.get_teams():
            team_info = {
                "name": team.name,
                "permission": team.permission,
            }
            permissions["teams"].append(team_info)
        
        return permissions
    
    def get_org_permissions(self, org_name: str) -> list:
        """Get permissions across all repositories in the organization
        
        Args:
            org_name: Name of the organization
            
        Returns:
            List of permission information for all repositories
        """
        org = self.get_organization(org_name)
        all_permissions = []
        
        for repo in org.get_repos():
            try:
                perms = self.get_repository_permissions(org_name, repo.name)
                all_permissions.append(perms)
            except Exception as e:
                # Skip repositories we can't access
                continue
        
        return all_permissions
    
    def get_codeowners(self, org_name: str, repo_name: str) -> Optional[str]:
        """Get CODEOWNERS file content for a repository
        
        Args:
            org_name: Name of the organization
            repo_name: Name of the repository
            
        Returns:
            Content of CODEOWNERS file or None if not found
        """
        org = self.get_organization(org_name)
        repo = org.get_repo(repo_name)
        
        # CODEOWNERS can be in multiple locations
        possible_paths = [
            "CODEOWNERS",
            ".github/CODEOWNERS",
            "docs/CODEOWNERS",
        ]
        
        for path in possible_paths:
            try:
                content = repo.get_contents(path)
                if content:
                    return content.decoded_content.decode('utf-8')
            except:
                continue
        
        return None
    
    def get_all_codeowners(self, org_name: str) -> dict:
        """Get CODEOWNERS files for all repositories
        
        Args:
            org_name: Name of the organization
            
        Returns:
            Dictionary mapping repository names to CODEOWNERS content
        """
        org = self.get_organization(org_name)
        codeowners = {}
        
        for repo in org.get_repos():
            try:
                content = self.get_codeowners(org_name, repo.name)
                if content:
                    codeowners[repo.name] = content
            except Exception as e:
                continue
        
        return codeowners
