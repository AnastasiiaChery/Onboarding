from jira import JIRA
from app.config import JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN

def init_jira_client():
    try:
        jira = JIRA(
            server=JIRA_URL,
            basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
        )
        # Verify connection by getting current user
        current_user = jira.current_user()
        print(f"Successfully connected to Jira as: {current_user}")
        return jira
    except Exception as e:
        print(f"Failed to connect to Jira: {str(e)}")
        return None 