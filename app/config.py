from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Jira configuration
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Confluence configuration
CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")

# GitHub configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") 