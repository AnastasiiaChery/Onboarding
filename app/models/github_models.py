from pydantic import BaseModel
from typing import Optional

class RepositoryResponse(BaseModel):
    name: str
    full_name: str
    description: Optional[str] = None
    html_url: str
    stars: int
    forks: int
    language: Optional[str] = None

class CreateRepositoryRequest(BaseModel):
    name: str
    description: Optional[str] = None
    private: bool = False
    auto_init: bool = True

class PullRequestResponse(BaseModel):
    number: int
    title: str
    state: str
    html_url: str
    created_at: str
    updated_at: str
    user: str
    body: Optional[str] = None

class CreatePullRequestRequest(BaseModel):
    title: str
    body: Optional[str] = None
    head: str
    base: str 