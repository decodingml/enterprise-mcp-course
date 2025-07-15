from fastapi import FastAPI, Request
from host import MCPOpenAIClient
import httpx
app = FastAPI()

@app.post("/webhook")
async def handle_github_webhook(request: Request):
    payload = await request.json()

    # Only handle PR open events
    if payload.get("action") == "opened":
        pr = payload["pull_request"]
        title = pr["title"]
        body = pr.get("body", "")
        diff_url = pr["diff_url"]


        async with httpx.AsyncClient() as client:
            diff = (await client.get(diff_url)).text

        # Use the MCP client
        client = MCPOpenAIClient()
        await client.connect_to_server("github")  # Or "jira" if using that tool
        summary = await client.process_query(f"Summarize this PR:\n\nTitle: {title}\n\nBody: {body}\n\nDiff:\n{diff}")
        await client.cleanup()

        # Post a comment back to GitHub
        repo = payload["repository"]["full_name"]
        pr_number = payload["number"]
        token = os.getenv("GITHUB_TOKEN")

        comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        async with httpx.AsyncClient() as client:
            await client.post(comment_url, headers=headers, json={"body": summary})

    return {"status": "ok"}
