import asyncio
import json
import logging
import sys
from fastmcp import Client

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("slack_test")

TEST_CHANNEL_NAME = "C097T1MS54Y"  
TEST_MESSAGE = "This is a test message from MCP Slack client."
MCP_URL = "http://localhost:8003/mcp"

async def test_list_tools(client):
    tools = await client.list_tools()
    assert any(t.name == "get_last_messages" for t in tools), "get_last_messages tool not found"
    assert any(t.name == "post_message" for t in tools), "post_message tool not found"

async def test_get_last_messages(client):
    logger.info(f"Testing get_last_messages for channel: {TEST_CHANNEL_NAME}")
    result = await client.call_tool("get_last_messages", {"channel_name": TEST_CHANNEL_NAME, "limit": 5})
    payload = json.loads(result.content[0].text)
    assert payload["status"] == "success", "Failed to get last messages"
    assert isinstance(payload["messages"], list), "Messages should be a list"
    logger.info(f"Fetched {len(payload['messages'])} messages from channel {TEST_CHANNEL_NAME}")

async def test_post_message(client):
    logger.info(f"Testing post_message to channel: {TEST_CHANNEL_NAME}")
    result = await client.call_tool("post_message", {"channel_name": TEST_CHANNEL_NAME, "message": TEST_MESSAGE})
    payload = json.loads(result.content[0].text)
    assert payload["status"] == "created", f"Message not posted successfully: {payload}"
    

async def main():
    async with Client(MCP_URL) as client:
        await test_list_tools(client)
        await test_get_last_messages(client)
        await test_post_message(client)
    logger.info("All Slack MCP tests passed.")

if __name__ == "__main__":
    asyncio.run(main())
