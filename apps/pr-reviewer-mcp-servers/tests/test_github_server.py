
import asyncio
import json
import logging
import sys
from fastmcp import Client

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("github_test")

MCP_URL = "http://localhost:8004/mcp"
TEST_OWNER = "915-Muscalagiu-AncaIoana"  # Replace with a real owner
TEST_REPO = "Mock-App"  # Replace with a real repo
TEST_PR_NUMBER = 19  # Replace with a real PR number

async def test_list_tools(client):
    tools = await client.list_tools()
    tool_names = [t.name for t in tools]
    logger.info(f"Available tools: {tool_names}")
    assert "get_pull_request" in tool_names, "get_pull_request tool not found"
    assert "get_pull_request_comments" in tool_names, "get_pull_request_comments tool not found"
    assert "get_pull_request_diff" in tool_names, "get_pull_request_diff tool not found"
    assert "get_pull_request_files" in tool_names, "get_pull_request_files tool not found"
    assert "get_pull_request_reviews" in tool_names, "get_pull_request_reviews tool not found"
    assert "get_pull_request_status" in tool_names, "get_pull_request_status tool not found"

async def test_get_pull_request(client):
    logger.info(f"Testing get_pull_request for {TEST_OWNER}/{TEST_REPO} PR#{TEST_PR_NUMBER}")
    result = await client.call_tool("get_pull_request", {"owner": TEST_OWNER, "repo": TEST_REPO, "pullNumber": TEST_PR_NUMBER})
    payload = json.loads(result.content[0].text)
    logger.info(f"get_pull_request result: {payload}")

async def test_get_pull_request_comments(client):
    logger.info(f"Testing get_pull_request_comments for {TEST_OWNER}/{TEST_REPO} PR#{TEST_PR_NUMBER}")
    result = await client.call_tool("get_pull_request_comments", {"owner": TEST_OWNER, "repo": TEST_REPO, "pullNumber": TEST_PR_NUMBER})
    payload = json.loads(result.content[0].text)
    logger.info(f"get_pull_request_comments result: {payload}")
    
async def test_get_pull_request_diff(client):
    logger.info(f"Testing get_pull_request_diff for {TEST_OWNER}/{TEST_REPO} PR#{TEST_PR_NUMBER}")
    result = await client.call_tool("get_pull_request_diff", {"owner": TEST_OWNER, "repo": TEST_REPO, "pullNumber": TEST_PR_NUMBER})
    payload = json.loads(result.content[0].text)
    logger.info(f"get_pull_request_diff result: {payload}")
    
async def test_get_pull_request_files(client):
    logger.info(f"Testing get_pull_request_files for {TEST_OWNER}/{TEST_REPO} PR#{TEST_PR_NUMBER}")
    result = await client.call_tool("get_pull_request_files", {"owner": TEST_OWNER, "repo": TEST_REPO, "pullNumber": TEST_PR_NUMBER})
    payload = json.loads(result.content[0].text)
    logger.info(f"get_pull_request_files result: {payload}")
    
async def test_get_pull_request_reviews(client):
    logger.info(f"Testing get_pull_request_reviews for {TEST_OWNER}/{TEST_REPO} PR#{TEST_PR_NUMBER}")
    result = await client.call_tool("get_pull_request_reviews", {"owner": TEST_OWNER, "repo": TEST_REPO, "pullNumber": TEST_PR_NUMBER})
    payload = json.loads(result.content[0].text)
    logger.info(f"get_pull_request_reviews result: {payload}")
    
async def test_get_pull_request_status(client):
    logger.info(f"Testing get_pull_request_status for {TEST_OWNER}/{TEST_REPO} PR#{TEST_PR_NUMBER}")
    result = await client.call_tool("get_pull_request_status", {"owner": TEST_OWNER, "repo": TEST_REPO, "pullNumber": TEST_PR_NUMBER})
    payload = json.loads(result.content[0].text)
    logger.info(f"get_pull_request_status result: {payload}")
    
async def main():
    async with Client(MCP_URL) as client:
        await test_list_tools(client)
        await test_get_pull_request(client)
        await test_get_pull_request_comments(client)
        await test_get_pull_request_diff(client)
        await test_get_pull_request_files(client)
        await test_get_pull_request_reviews(client)
        await test_get_pull_request_status(client)
    logger.info("All GitHub MCP tests passed.")

if __name__ == "__main__":
    asyncio.run(main())
