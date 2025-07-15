from config import settings

AVAILABLE_SERVERS = {
    "jira": {"type": "stdio", "path": "servers/jira-stdio-server/server.py"},
    "github": {
        "type": "sse",
        "url": "https://api.githubcopilot.com/mcp/",
        "headers": {
            "Authorization": f"Bearer {settings.GITHUB_ACCESS_TOKEN}",
            "Accept": "text/event-stream",
        },
    },
}
