
import asyncio
import json
import logging
import sys
from fastmcp import Client

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("tool_registry_test")

MCP_URL = "http://localhost:8000/mcp/"

async def test_list_tools(client):
    tools = await client.list_tools()
    logger.info(f"Tools in registry: {len(tools)}")
    assert isinstance(tools, list), f"Tools from the registry should be a list"
    assert tools, f"No tools found in the registry"

async def test_list_prompts(client):
    prompts = await client.list_prompts()
    logger.info(f"Prompts in registry: {len(prompts)}")
    assert isinstance(prompts, list), f"Prompts from the registry should be a list"
    assert prompts, f"No prompts found in the registry"

async def main():
    async with Client(MCP_URL) as client:
        await test_list_tools(client)
        await test_list_prompts(client)
    logger.info("All McpServersRegistry client tests passed.")

if __name__ == "__main__":
    asyncio.run(main())
