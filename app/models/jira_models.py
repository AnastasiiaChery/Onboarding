from pydantic import BaseModel
from typing import Optional

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