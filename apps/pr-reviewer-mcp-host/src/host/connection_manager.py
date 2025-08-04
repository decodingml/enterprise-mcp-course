
import opik
from opik import opik_context
from config import settings
from contextlib import AsyncExitStack
from typing import Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client


AVAILABLE_SERVERS = {
    "tool-registry": {"type": "streamable-http", "url": settings.TOOL_REGISTRY_URL}
}



class ConnectionManager:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.is_initialized = False

    @opik.track(name="connection-initialize", type="general")
    async def initialize_all(self):
        await self.connect_to_server('tool-registry')
        self.is_initialized = True

    @opik.track(name="connect-to-server", type="general")
    async def connect_to_server(self, server_key: str):
        config = AVAILABLE_SERVERS[server_key]

        if config["type"] == "stdio":
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(StdioServerParameters(command="python", args=[config["path"]]))
            )
            self.session = await self.exit_stack.enter_async_context(ClientSession(*stdio_transport))

        elif config["type"] == "streamable-http":
            context = streamablehttp_client(url=config["url"], headers=config.get("headers"))
            print(f"Connecting to SSE server '{server_key}' with streamablehttp_client...")

            read_stream, write_stream, get_session_id = await self.exit_stack.enter_async_context(context)
            await self._run_session(read_stream, write_stream, get_session_id)

        await self.session.initialize()

        try:
            tools = await self.session.list_tools()
            print(f"🔧 Tools available for {server_key}:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
        except Exception as e:
            print(f"(No tools found or error fetching tools: {e})")

        try:
            prompts = await self.session.list_prompts()
            print(f"📝 Prompts available for {server_key}:")
            for prompt in prompts.prompts:
                print(f"  - {prompt.name}")
        except Exception as e:
            print(f"(No prompts found or error fetching prompts: {e})")


    async def _run_session(self, read_stream, write_stream, get_session_id):
        print("🤝 Initializing MCP session...")
        session = await self.exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
        self.session = session
        print("⚡ Starting session initialization...")
        await session.initialize()
        print("✨ Session initialization complete!")
        print(f"\n✅ Connected to MCP server")
        if get_session_id:
            session_id = get_session_id()
            if session_id:
                print(f"Session ID: {session_id}")
    
    @opik.track(name="get-mcp-tools", type="general")
    async def get_mcp_tools(self):
        return await self.session.list_tools()

    @opik.track(name="call-tool", type="tool")
    async def call_tool(self, function_name, function_args):
        return await self.session.call_tool(
                function_name, arguments=dict(function_args)
            )

    @opik.track(name="get-prompt", type="general")
    async def get_prompt(self, name, args):
        return await self.session.get_prompt(name, args)

    @opik.track(name="cleanup", type="general")
    async def cleanup_all(self):
        await self.exit_stack.aclose()
