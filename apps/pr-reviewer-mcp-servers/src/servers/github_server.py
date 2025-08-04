import opik
import logging
from fastmcp import FastMCP
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from config import settings
from contextlib import AsyncExitStack
import utils.opik_utils as opik_utils

opik_utils.configure()
logger = logging.getLogger("github_server")
logging.basicConfig(level=logging.INFO)

GITHUB_MCP_URL = "https://api.githubcopilot.com/mcp/"
SERVER_CONFIG = {
        "url": GITHUB_MCP_URL,
        "headers": {
            "Authorization": f"Bearer {settings.GITHUB_ACCESS_TOKEN}",
            "Accept": "text/event-stream",
        },
}

github_mcp = FastMCP("github_proxy")



@github_mcp.tool(
    description="Get pull request details",
    tags={"github", "pull_request", "details"},
    annotations={"title": "Get Pull Request", "readOnlyHint": True, "openWorldHint": True},
)
@opik.track(name="github-get-pull-request", type="tool")
async def get_pull_request(owner: str, repo: str, pullNumber: int):
    headers = SERVER_CONFIG.get("headers", {})
    context = streamablehttp_client(SERVER_CONFIG.get("url"), headers=headers)
    async with AsyncExitStack() as exit_stack:
        read_stream, write_stream, get_session_id = await exit_stack.enter_async_context(context)
        session = await exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()
        logger.info(f"Fetching pull request {pullNumber} for {owner}/{repo}")
        result = await session.call_tool("get_pull_request", {"owner": owner, "repo": repo, "pullNumber": pullNumber})
        return result


@github_mcp.tool(
    description="Get pull request comments",
    tags={"github", "pull_request", "comments"},
    annotations={"title": "Get Pull Request Comments", "readOnlyHint": True, "openWorldHint": True},
)
@opik.track(name="github-get-pull-request-comments", type="tool")
async def get_pull_request_comments(owner: str, repo: str, pullNumber: int):
    headers = SERVER_CONFIG.get("headers", {})
    context = streamablehttp_client(SERVER_CONFIG.get("url"), headers=headers)
    async with AsyncExitStack() as exit_stack:
        read_stream, write_stream, get_session_id = await exit_stack.enter_async_context(context)
        session = await exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()
        result = await session.call_tool("get_pull_request_comments", {"owner": owner, "repo": repo, "pullNumber": pullNumber})
        return result

@github_mcp.tool(
    description="Get pull request diff",
    tags={"github", "pull_request", "diff"},
    annotations={"title": "Get Pull Request Diff", "readOnlyHint": True, "openWorldHint": True},
)
@opik.track(name="github-get-pull-request-diff", type="tool")
async def get_pull_request_diff(owner: str, repo: str, pullNumber: int):
    headers = SERVER_CONFIG.get("headers", {})
    context = streamablehttp_client(SERVER_CONFIG.get("url"), headers=headers)
    async with AsyncExitStack() as exit_stack:
        read_stream, write_stream, get_session_id = await exit_stack.enter_async_context(context)
        session = await exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()
        result = await session.call_tool("get_pull_request_diff", {"owner": owner, "repo": repo, "pullNumber": pullNumber})
        return result


@github_mcp.tool(
    description="Get pull request files",
    tags={"github", "pull_request", "files"},
    annotations={"title": "Get Pull Request Files", "readOnlyHint": True, "openWorldHint": True},
)
@opik.track(name="github-get-pull-request-files", type="tool")
async def get_pull_request_files(owner: str, repo: str, pullNumber: int, page: int = 1, perPage: int = 100):
    headers = SERVER_CONFIG.get("headers", {})
    context = streamablehttp_client(SERVER_CONFIG.get("url"), headers=headers)
    async with AsyncExitStack() as exit_stack:
        read_stream, write_stream, get_session_id = await exit_stack.enter_async_context(context)
        session = await exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()
        result = await session.call_tool(
            "get_pull_request_files",
            {"owner": owner, "repo": repo, "pullNumber": pullNumber, "page": page, "perPage": perPage}
        )
        return result


@github_mcp.tool(
    description="Get pull request reviews",
    tags={"github", "pull_request", "reviews"},
    annotations={"title": "Get Pull Request Reviews", "readOnlyHint": True, "openWorldHint": True},
)
@opik.track(name="github-get-pull-request-reviews", type="tool")
async def get_pull_request_reviews(owner: str, repo: str, pullNumber: int):
    headers = SERVER_CONFIG.get("headers", {})
    context = streamablehttp_client(SERVER_CONFIG.get("url"), headers=headers)
    async with AsyncExitStack() as exit_stack:
        read_stream, write_stream, get_session_id = await exit_stack.enter_async_context(context)
        session = await exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()
        result = await session.call_tool("get_pull_request_reviews", {"owner": owner, "repo": repo, "pullNumber": pullNumber})
        return result


@github_mcp.tool(
    description="Get pull request status checks",
    tags={"github", "pull_request", "status"},
    annotations={"title": "Get Pull Request Status", "readOnlyHint": True, "openWorldHint": True},
)
@opik.track(name="github-get-pull-request-status", type="tool")
async def get_pull_request_status(owner: str, repo: str, pullNumber: int):
    headers = SERVER_CONFIG.get("headers", {})
    context = streamablehttp_client(SERVER_CONFIG.get("url"), headers=headers)
    async with AsyncExitStack() as exit_stack:
        read_stream, write_stream, get_session_id = await exit_stack.enter_async_context(context)
        session = await exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()
        result = await session.call_tool("get_pull_request_status", {"owner": owner, "repo": repo, "pullNumber": pullNumber})
        return result

# github_mcp.run(transport="streamable-http", host="localhost", port=8004)