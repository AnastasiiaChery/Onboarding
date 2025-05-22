from fastapi import FastAPI, HTTPException
from jira import JIRA
from atlassian import Confluence
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Load environment variables
load_dotenv()

app = FastAPI(title="Jira and Confluence Integration API")

# Jira configuration
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Confluence configuration
CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")

# Initialize Jira client
try:
    jira = JIRA(
        server=JIRA_URL,
        basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
    )
    # Verify connection by getting current user
    current_user = jira.current_user()
    print(f"Successfully connected to Jira as: {current_user}")
except Exception as e:
    print(f"Failed to connect to Jira: {str(e)}")
    jira = None

# Initialize Confluence client
try:
    confluence = Confluence(
        url=CONFLUENCE_URL,
        username=JIRA_EMAIL,
        password=JIRA_API_TOKEN
    )
    print("Successfully connected to Confluence")
except Exception as e:
    print(f"Failed to connect to Confluence: {str(e)}")
    confluence = None

class IssueResponse(BaseModel):
    key: str
    summary: str
    description: Optional[str] = None
    status: str

class CreateIssueRequest(BaseModel):
    project_key: str
    summary: str
    description: Optional[str] = None
    issue_type: str = "Task"

class SearchIssuesRequest(BaseModel):
    jql: str
    max_results: Optional[int] = 50

class UpdateStatusRequest(BaseModel):
    status: str

class PageResponse(BaseModel):
    id: str
    title: str
    space_key: str
    version: int
    body: Optional[str] = None

class CreatePageRequest(BaseModel):
    title: str
    space_key: str
    body: str
    parent_id: Optional[str] = None

@app.get("/")
async def root():
    if not jira or not confluence:
        raise HTTPException(status_code=500, detail="Jira or Confluence connection not available")
    return {
        "message": "Welcome to Jira and Confluence Integration API",
        "connected_user": jira.current_user()
    }

# Jira endpoints
@app.get("/issues/{issue_key}", response_model=IssueResponse)
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


@app.post("/issues/search")
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


@app.get("/projects")
async def get_projects():
    if not jira:
        raise HTTPException(status_code=500, detail="Jira connection not available")
    
    try:
        projects = jira.projects()
        return [{"key": project.key, "name": project.name} for project in projects]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch projects: {str(e)}")

# Confluence endpoints
@app.get("/spaces")
async def get_spaces():
    if not confluence:
        raise HTTPException(status_code=500, detail="Confluence connection not available")
    
    try:
        spaces = confluence.get_all_spaces()
        return [{"key": space["key"], "name": space["name"]} for space in spaces["results"]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch spaces: {str(e)}")

@app.get("/pages/{page_id}", response_model=PageResponse)
async def get_page(page_id: str):
    if not confluence:
        raise HTTPException(status_code=500, detail="Confluence connection not available")
    
    try:
        page = confluence.get_page_by_id(page_id, expand="body.storage")
        return PageResponse(
            id=page["id"],
            title=page["title"],
            space_key=page["space"]["key"],
            version=page["version"]["number"],
            body=page["body"]["storage"]["value"]
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Page not found: {str(e)}")

@app.post("/pages", response_model=PageResponse)
async def create_page(page_data: CreatePageRequest):
    if not confluence:
        raise HTTPException(status_code=500, detail="Confluence connection not available")
    
    try:
        page = confluence.create_page(
            space=page_data.space_key,
            title=page_data.title,
            body=page_data.body,
            parent_id=page_data.parent_id
        )
        
        return PageResponse(
            id=page["id"],
            title=page["title"],
            space_key=page["space"]["key"],
            version=page["version"]["number"],
            body=page["body"]["storage"]["value"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create page: {str(e)}")

@app.get("/pages/search")
async def search_pages(query: str, space_key: Optional[str] = None):
    if not confluence:
        raise HTTPException(status_code=500, detail="Confluence connection not available")
    
    try:
        cql = f'text ~ "{query}"'
        if space_key:
            cql += f' AND space = "{space_key}"'
        
        results = confluence.cql(cql, limit=50)
        return [{
            "id": page["content"]["id"],
            "title": page["content"]["title"],
            "space_key": page["content"]["space"]["key"],
            "version": page["content"]["version"]["number"]
        } for page in results["results"]]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to search pages: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 