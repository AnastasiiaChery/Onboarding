from atlassian import Confluence
from app.config import CONFLUENCE_URL, JIRA_EMAIL, JIRA_API_TOKEN

def init_confluence_client():
    try:
        confluence = Confluence(
            url=CONFLUENCE_URL,
            username=JIRA_EMAIL,
            password=JIRA_API_TOKEN
        )
        print("Successfully connected to Confluence")
        return confluence
    except Exception as e:
        print(f"Failed to connect to Confluence: {str(e)}")
        return None 