# Jira-GitHub Integration API

This FastAPI application provides integration between Jira, Confluence, and GitHub, allowing you to:
- Manage Jira issues
- Create and manage Confluence pages
- Create GitHub repositories and pull requests
- Automatically create PRs from Jira tickets

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Main application file
│   ├── config.py            # Configuration and environment variables
│   ├── clients/             # API clients
│   │   ├── __init__.py
│   │   ├── jira_client.py
│   │   ├── confluence_client.py
│   │   └── github_client.py
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   ├── jira_models.py
│   │   ├── confluence_models.py
│   │   └── github_models.py
│   └── routes/              # API routes
│       ├── __init__.py
│       ├── jira_routes.py
│       ├── confluence_routes.py
│       └── github_routes.py
├── .env                     # Environment variables
└── requirements.txt         # Project dependencies
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your credentials:
```
JIRA_URL=your_jira_url
JIRA_EMAIL=your_email
JIRA_API_TOKEN=your_token
CONFLUENCE_URL=your_confluence_url
GITHUB_TOKEN=your_github_token
```

4. Run the application:
```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Jira Endpoints
- `GET /issues/{issue_key}` - Get issue details
- `POST /issues/search` - Search issues
- `GET /issues/projects` - List all projects

### Confluence Endpoints
- `GET /pages/spaces` - List all spaces
- `GET /pages/{page_id}` - Get page details
- `POST /pages` - Create a new page
- `GET /pages/search` - Search pages

### GitHub Endpoints
- `GET /github/repos` - List repositories
- `POST /github/repos` - Create repository
- `GET /github/repos/{owner}/{repo}/pulls` - List pull requests
- `POST /github/repos/{owner}/{repo}/pulls` - Create pull request
- `POST /github/process-ticket/{issue_key}` - Process Jira ticket and create PR

## Health Check
- `GET /health` - Check connection status of all services

## Documentation
API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 