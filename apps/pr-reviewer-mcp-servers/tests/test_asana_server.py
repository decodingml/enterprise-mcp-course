

import asyncio
import json
import logging
import sys
from fastmcp import Client

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("asana_test")

TEST_FIND_TASK_NAME = "FFM-2"
TEST_CREATE_TASK_NAME = "FFM-test"
TEST_CREATE_TASK_DESC = "This is a test task"
MCP_URL = "http://localhost:8001/mcp"

async def test_list_tools(client):
    tools = await client.list_tools()
    assert any(t.name == "find_task" for t in tools), "find_task tool not found"
    assert any(t.name == "create_task" for t in tools), "create_task tool not found"

async def test_find_task(client):
    logger.info(f"Testing find_task with name: {TEST_FIND_TASK_NAME}")
    result = await client.call_tool("find_task", {"task_name": TEST_FIND_TASK_NAME})
    payload = json.loads(result.content[0].text)
    assert payload["status"] in ("success", "not_found"), "Unexpected status in find_task"
    if payload["status"] == "success":
        assert "notes" in payload["task"], "Task notes missing in find_task result"

async def test_create_task(client):
    logger.info(f"Testing create_task with name: {TEST_CREATE_TASK_NAME}")
    result = await client.call_tool("create_task", {"task_name": TEST_CREATE_TASK_NAME, "description": TEST_CREATE_TASK_DESC})
    payload = json.loads(result.content[0].text)
    assert payload["status"] == "created", "Task not created successfully"
    assert payload["task"]["name"] == TEST_CREATE_TASK_NAME, "Created task name mismatch"
    assert payload["task"]["notes"] == TEST_CREATE_TASK_DESC, "Created task description mismatch"

async def main():
    async with Client(MCP_URL) as client:
        await test_list_tools(client)
        await test_find_task(client)
        await test_create_task(client)
    logger.info("All Asana MCP tests passed.")

if __name__ == "__main__":
    asyncio.run(main())