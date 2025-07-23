from fastapi import FastAPI, Request
from host.host import MCPHost
from host.prompts import PR_REVIEW_PROMPT

app = FastAPI()
client = MCPHost()

@app.on_event("startup")
async def startup_event():
    await client.connect_to_server("github")  

@app.on_event("shutdown")
async def shutdown_event():
    await client.cleanup()
        
@app.post("/webhook")
async def handle_github_webhook(request: Request):
    payload = await request.json()

    if payload.get("action") == "opened":
        pr = payload["pull_request"]
        summary = await client.process_query(PR_REVIEW_PROMPT.format(pr_id=pr["id"], pr_url = pr["url"] ))
        print(summary)
        
    return {"status": "ok"}
