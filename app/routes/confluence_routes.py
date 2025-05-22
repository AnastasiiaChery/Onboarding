from fastapi import APIRouter, HTTPException
from typing import Optional
from app.models.confluence_models import PageResponse, CreatePageRequest
from app.clients.confluence_client import init_confluence_client

router = APIRouter(prefix="/pages", tags=["confluence"])
confluence = init_confluence_client()

@router.get("/spaces")
async def get_spaces():
    if not confluence:
        raise HTTPException(status_code=500, detail="Confluence connection not available")
    
    try:
        spaces = confluence.get_all_spaces()
        return [{"key": space["key"], "name": space["name"]} for space in spaces["results"]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch spaces: {str(e)}")

@router.get("/{page_id}", response_model=PageResponse)
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

@router.post("", response_model=PageResponse)
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

@router.get("/search")
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