#!/usr/bin/env python3
"""
GitHub Organization Creator

This script creates a GitHub organization and sets up repositories based on
a configuration file.
"""

import sys
import argparse
import yaml
from github import Github, GithubException
import os


def load_config(config_file):
    """Load configuration from YAML file."""
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML configuration: {e}")
        sys.exit(1)


def create_organization(github_client, org_config):
    """
    Create a GitHub organization.
    
    Note: Creating organizations via API requires GitHub Enterprise.
    For regular GitHub accounts, organizations must be created via web interface.
    This function will attempt to verify if the organization exists.
    """
    org_name = org_config.get('name')
    
    if not org_name:
        print("Error: Organization name is required in configuration.")
        return None
    
    try:
        # Try to get the organization
        org = github_client.get_organization(org_name)
        print(f"Organization '{org_name}' already exists.")
        return org
    except GithubException as e:
        if e.status == 404:
            print(f"Organization '{org_name}' does not exist.")
            print("Note: Creating organizations via API requires GitHub Enterprise.")
            print(f"Please create the organization '{org_name}' manually at:")
            print("https://github.com/organizations/new")
            return None
        else:
            print(f"Error checking organization: {e}")
            return None


def create_repository(org, repo_config, templates_dir):
    """Create a repository in the organization from a template."""
    repo_name = repo_config.get('name')
    description = repo_config.get('description', '')
    private = repo_config.get('private', False)
    template = repo_config.get('template', 'basic')
    
    if not repo_name:
        print("Warning: Repository name is required. Skipping.")
        return None
    
    try:
        # Check if repository already exists
        try:
            repo = org.get_repo(repo_name)
            print(f"  Repository '{repo_name}' already exists. Skipping.")
            return repo
        except GithubException as e:
            if e.status != 404:
                raise
        
        # Create the repository
        print(f"  Creating repository '{repo_name}'...")
        repo = org.create_repo(
            name=repo_name,
            description=description,
            private=private,
            auto_init=True  # Initialize with README
        )
        print(f"  Successfully created repository '{repo_name}'")
        
        # Apply template files if template directory exists
        template_path = os.path.join(templates_dir, template)
        if os.path.exists(template_path):
            print(f"  Applying template '{template}'...")
            apply_template(repo, template_path)
        
        return repo
        
    except GithubException as e:
        print(f"  Error creating repository '{repo_name}': {e}")
        return None


def apply_template(repo, template_path):
    """Apply template files to a repository."""
    # This is a simplified version. In a real implementation,
    # you would iterate through template files and commit them to the repo
    print(f"  Template application from '{template_path}' (placeholder)")
    # Template application would require additional logic to:
    # 1. Read files from template directory
    # 2. Create/update files in the repository via GitHub API
    # This is beyond the scope of this basic implementation


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Create GitHub organization and repositories from configuration'
    )
    parser.add_argument(
        '-c', '--config',
        default='config.yml',
        help='Configuration file (default: config.yml)'
    )
    parser.add_argument(
        '-t', '--templates-dir',
        default='templates',
        help='Templates directory (default: templates)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    print(f"Loading configuration from '{args.config}'...")
    config = load_config(args.config)
    
    # Get GitHub token
    github_token = config.get('github', {}).get('token')
    if not github_token or github_token == 'your_github_token_here':
        print("Error: GitHub token not configured.")
        print("Please set your GitHub token in the configuration file.")
        print("You can create a token at: https://github.com/settings/tokens")
        sys.exit(1)
    
    if args.dry_run:
        print("\n=== DRY RUN MODE ===")
        print("No changes will be made to GitHub.\n")
    
    # Initialize GitHub client
    print("Connecting to GitHub...")
    try:
        github_client = Github(github_token)
        user = github_client.get_user()
        print(f"Authenticated as: {user.login}")
    except GithubException as e:
        print(f"Error authenticating with GitHub: {e}")
        sys.exit(1)
    
    # Get or create organization
    org_config = config.get('organization', {})
    print(f"\nChecking organization '{org_config.get('name')}'...")
    
    if args.dry_run:
        print(f"[DRY RUN] Would check/create organization: {org_config.get('name')}")
        org = None
    else:
        org = create_organization(github_client, org_config)
        if not org:
            print("\nPlease create the organization first, then run this script again.")
            sys.exit(1)
    
    # Create repositories
    repositories = config.get('repositories', [])
    if repositories:
        print(f"\nProcessing {len(repositories)} repositories...")
        for repo_config in repositories:
            if args.dry_run:
                print(f"[DRY RUN] Would create repository: {repo_config.get('name')}")
            else:
                if org:
                    create_repository(org, repo_config, args.templates_dir)
    else:
        print("\nNo repositories configured.")
    
    print("\nDone!")


if __name__ == '__main__':
    main()
