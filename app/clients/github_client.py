from github import Github
from app.config import GITHUB_TOKEN

def init_github_client():
    try:
        github = Github(GITHUB_TOKEN)
        # Verify connection by getting current user
        github_user = github.get_user()
        print(f"Successfully connected to GitHub as: {github_user.login}")
        return github
    except Exception as e:
        print(f"Failed to connect to GitHub: {str(e)}")
        return None 