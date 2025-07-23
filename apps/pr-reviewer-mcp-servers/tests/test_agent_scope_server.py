
import asyncio
import logging
import sys
from fastmcp import Client

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("agent_scope_server_test")

MCP_URL = "http://localhost:8002/mcp/"
PROMPT_NAME = "pr_review_prompt"
async def test_list_prompts(client):
    prompts = await client.list_prompts()
    logger.info(f"Prompts in server: {len(prompts)}")
    assert isinstance(prompts, list), f"Prompts from the agent scope server should be a list"
    assert prompts, f"No prompts found in the agent scope server"

async def test_get_prompt(client):
    logger.info(f"Testing get_prompt with name: {PROMPT_NAME}")
    result = await client.get_prompt(PROMPT_NAME)
    prompt_messages = result.messages
    assert isinstance(prompt_messages, list), f"Prompt messages for prompt {PROMPT_NAME} should be a list"
    assert prompt_messages, f"No prompt messages found for prompt {PROMPT_NAME}"

async def main():
    async with Client(MCP_URL) as client:
        await test_list_prompts(client)
        await test_get_prompt(client)
    logger.info("All McpServersRegistry client tests passed.")

if __name__ == "__main__":
    asyncio.run(main())
