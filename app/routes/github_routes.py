from fastapi import APIRouter, HTTPException
from typing import List
from app.models.github_models import (
    RepositoryResponse,
    CreateRepositoryRequest,
    PullRequestResponse,
    CreatePullRequestRequest
)
from app.clients.github_client import init_github_client

router = APIRouter(prefix="/github", tags=["github"])
github = init_github_client()

@router.get("/repos", response_model=List[RepositoryResponse])
async def get_repositories():
    if not github:
        raise HTTPException(status_code=500, detail="GitHub connection not available")
    
    try:
        user = github.get_user()
        repos = user.get_repos()
        return [{
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "html_url": repo.html_url,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "language": repo.language
        } for repo in repos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch repositories: {str(e)}")

@router.post("/repos", response_model=RepositoryResponse)
async def create_repository(repo_data: CreateRepositoryRequest):
    if not github:
        raise HTTPException(status_code=500, detail="GitHub connection not available")
    
    try:
        user = github.get_user()
        repo = user.create_repo(
            name=repo_data.name,
            description=repo_data.description,
            private=repo_data.private,
            auto_init=repo_data.auto_init
        )
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "html_url": repo.html_url,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "language": repo.language
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create repository: {str(e)}")

@router.get("/repos/{owner}/{repo}/pulls", response_model=List[PullRequestResponse])
async def get_pull_requests(owner: str, repo: str):
    if not github:
        raise HTTPException(status_code=500, detail="GitHub connection not available")
    
    try:
        repository = github.get_repo(f"{owner}/{repo}")
        pulls = repository.get_pulls(state="all")
        return [{
            "number": pr.number,
            "title": pr.title,
            "state": pr.state,
            "html_url": pr.html_url,
            "created_at": pr.created_at.isoformat(),
            "updated_at": pr.updated_at.isoformat(),
            "user": pr.user.login,
            "body": pr.body
        } for pr in pulls]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch pull requests: {str(e)}")

@router.post("/repos/{owner}/{repo}/pulls", response_model=PullRequestResponse)
async def create_pull_request(owner: str, repo: str, pr_data: CreatePullRequestRequest):
    if not github:
        raise HTTPException(status_code=500, detail="GitHub connection not available")
    
    try:
        repository = github.get_repo(f"{owner}/{repo}")
        pr = repository.create_pull(
            title=pr_data.title,
            body=pr_data.body,
            head=pr_data.head,
            base=pr_data.base
        )
        return {
            "number": pr.number,
            "title": pr.title,
            "state": pr.state,
            "html_url": pr.html_url,
            "created_at": pr.created_at.isoformat(),
            "updated_at": pr.updated_at.isoformat(),
            "user": pr.user.login,
            "body": pr.body
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create pull request: {str(e)}")

@router.post("/process-ticket/{issue_key}")
async def process_ticket(issue_key: str, repo_owner: str, repo_name: str):
    """
    Process a Jira ticket and create a PR based on its content
    """
    if not jira or not github:
        raise HTTPException(status_code=500, detail="Jira or GitHub connection not available")
    
    try:
        # Get Jira issue details
        issue = jira.issue(issue_key)
        
        # Get issue details
        issue_details = {
            "key": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description,
            "status": issue.fields.status.name,
            "type": issue.fields.issuetype.name,
            "priority": issue.fields.priority.name if hasattr(issue.fields, 'priority') else None,
            "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None
        }
        
        # Get related Confluence pages if any
        confluence_pages = []
        if confluence:
            try:
                # Search for pages related to this issue
                search_query = f'issue = {issue_key}'
                pages = confluence.cql(search_query, limit=5)
                for page in pages["results"]:
                    confluence_pages.append({
                        "title": page["content"]["title"],
                        "url": f"{CONFLUENCE_URL}/spaces/{page['content']['space']['key']}/pages/{page['content']['id']}"
                    })
            except Exception as e:
                print(f"Error fetching Confluence pages: {str(e)}")
        
        # Get repository
        try:
            repository = github.get_repo(f"{repo_owner}/{repo_name}")
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Repository not found: {str(e)}")
        
        # Create a new branch for the changes
        branch_name = f"feature/{issue_key.lower()}"
        try:
            # Get the default branch
            default_branch = repository.default_branch
            # Create new branch
            source = repository.get_branch(default_branch)
            repository.create_git_ref(f"refs/heads/{branch_name}", source.commit.sha)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to create branch: {str(e)}")
        
        # Create PR
        try:
            pr = repository.create_pull(
                title=f"[{issue_key}] {issue_details['summary']}",
                body=f"""
## Jira Ticket Details
- **Key**: {issue_details['key']}
- **Type**: {issue_details['type']}
- **Priority**: {issue_details['priority']}
- **Assignee**: {issue_details['assignee']}

## Description
{issue_details['description']}

## Related Documentation
{chr(10).join([f"- [{page['title']}]({page['url']})" for page in confluence_pages]) if confluence_pages else "No related documentation found."}
                """,
                head=branch_name,
                base=default_branch
            )
            
            return {
                "status": "success",
                "message": "PR created successfully",
                "pr_url": pr.html_url,
                "issue_details": issue_details,
                "related_docs": confluence_pages
            }
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to create PR: {str(e)}")
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process ticket: {str(e)}") 