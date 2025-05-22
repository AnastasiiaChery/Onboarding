from fastapi import APIRouter, HTTPException
from app.models.jira_models import IssueResponse, CreateIssueRequest, SearchIssuesRequest, UpdateStatusRequest
from app.clients.jira_client import init_jira_client

router = APIRouter(prefix="/issues", tags=["jira"])
jira = init_jira_client()

@router.get("/{issue_key}", response_model=IssueResponse)
async def get_issue(issue_key: str):
    if not jira:
        raise HTTPException(status_code=500, detail="Jira connection not available")
    
    try:
        issue = jira.issue(issue_key)
        return IssueResponse(
            key=issue.key,
            summary=issue.fields.summary,
            description=issue.fields.description,
            status=issue.fields.status.name
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Issue not found: {str(e)}")

@router.post("/search")
async def search_issues(search_data: SearchIssuesRequest):
    if not jira:
        raise HTTPException(status_code=500, detail="Jira connection not available")
    
    try:
        issues = jira.search_issues(
            search_data.jql,
            maxResults=search_data.max_results
        )
        
        return [{
            "key": issue.key,
            "summary": issue.fields.summary,
            "description": issue.fields.description,
            "status": issue.fields.status.name
        } for issue in issues]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to search issues: {str(e)}")

@router.get("/projects")
async def get_projects():
    if not jira:
        raise HTTPException(status_code=500, detail="Jira connection not available")
    
    try:
        projects = jira.projects()
        return [{"key": project.key, "name": project.name} for project in projects]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch projects: {str(e)}") 