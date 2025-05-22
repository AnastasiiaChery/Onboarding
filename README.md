# FastAPI Jira Integration

This is a FastAPI application that integrates with Jira to fetch issues and project information.

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your Jira credentials:
   ```bash
   cp .env.example .env
   ```
   - Get your Jira API token from: https://id.atlassian.com/manage-profile/security/api-tokens

## Running the Application

Start the server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

- `GET /`: Welcome message
- `GET /issues/{issue_key}`: Get information about a specific Jira issue
- `GET /projects`: List all available Jira projects

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc 