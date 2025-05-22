from pydantic import BaseModel
from typing import Optional

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