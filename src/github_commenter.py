import os
import requests

class GitHubPRCommenter:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.host = os.getenv("GITHUB_HOST", "https://api.github.com")
        self.repo = os.getenv("GITHUB_REPOSITORY")
        self.ref = os.getenv("GITHUB_REF", "")
        self.pr_number = os.getenv("GITHUB_PR_NUMBER")
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is required.")
        if not self.repo:
            raise ValueError("GITHUB_REPOSITORY environment variable is required.")
        if not self.pr_number:
            # Try to extract PR number from ref if not set directly
            if self.ref.startswith("refs/pull/"):
                self.pr_number = self.ref.split("/")[2]
            else:
                raise ValueError("GITHUB_PR_NUMBER or a valid GITHUB_REF is required.")
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def post_comment(self, body: str):
        url = f"{self.host}/repos/{self.repo}/issues/{self.pr_number}/comments"
        response = requests.post(url, headers=self.headers, json={"body": body})
        if response.status_code != 201:
            raise Exception(f"Failed to post comment: {response.status_code} {response.text}")
        return response.json()
