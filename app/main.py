from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.clients.jira_client import init_jira_client
from app.clients.confluence_client import init_confluence_client
from app.clients.github_client import init_github_client
from app.routes import jira_routes, confluence_routes, github_routes

app = FastAPI(title="Jira-GitHub Integration API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
jira = init_jira_client()
confluence = init_confluence_client()
github = init_github_client()

# Include routers
app.include_router(jira_routes.router)
app.include_router(confluence_routes.router)
app.include_router(github_routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Jira-GitHub Integration API"}

@app.get("/health")
async def health_check():
    status = {
        "jira": "connected" if jira else "disconnected",
        "confluence": "connected" if confluence else "disconnected",
        "github": "connected" if github else "disconnected"
    }
    return status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 