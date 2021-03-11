class PullRequestManager:
    """Manager for PullRequests Table"""

    def __init__(self, client):
        self.client = client

    def get_pull_requests(self):
        """Fetch all persisted database rows for pull requests."""
        return self.client.query(sql="SELECT * FROM pull_requests")
