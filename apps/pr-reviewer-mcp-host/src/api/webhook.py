
from fastapi import FastAPI, Request
from host.host import MCPHost
from config import settings
import logging
import json
import uvicorn

SYSTEM_PROMPT_NAME = "scope_pr_review_prompt"

app = FastAPI()
client = MCPHost()
logger = logging.getLogger("webhook")
logging.basicConfig(level=logging.INFO)

@app.on_event("startup")
async def startup_event():
    await client.initialize()  

@app.on_event("shutdown")
async def shutdown_event():
    await client.cleanup()
        

@app.post("/webhook")
async def handle_github_webhook(request: Request):
    try:
        logger.info("Received webhook POST request.")
        payload = await request.json()
        logger.info(f"Webhook action: {payload.get('action', 'unknown action')}")
        if payload.get("action") == "opened":
            
            pr = payload["pull_request"]
            logger.info(f"Processing PR opened event: id={pr['id']} url={pr['url']}")
            logger.info("Requesting system prompt from MCPHost...")
            
            system_prompt = await client.get_system_prompt(SYSTEM_PROMPT_NAME,{ "arguments" : json.dumps({"pr_id": str(pr["id"]), "pr_url": str(pr["url"]) } )})
            logger.info(f"System prompt received: {system_prompt}")
            logger.info("Processing query with Gemini...")
            
            review = await client.process_query(system_prompt.messages[0].content.text)
            logger.info(f"Review generated: {review}")
            if review:
                logger.info(f"Posting review to Slack channel {settings.SLACK_CHANNEL_ID}...")
                await client.call_tool("slack_post_message", {"channel_name": settings.SLACK_CHANNEL_ID, "message": review})
                logger.info("Review posted to Slack.")
        else:
            logger.info(f"Webhook action '{payload.get('action')}' is not handled.")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        return {"status": "error", "detail": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)