# File: host.py

import json
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client
from openai import AsyncOpenAI

from config import settings
from tool_registry import AVAILABLE_SERVERS


class MCPOpenAIClient:
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def connect_to_server(self, server_key: str):
        config = AVAILABLE_SERVERS[server_key]

        if config["type"] == "stdio":
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(StdioServerParameters(command="python", args=[config["path"]]))
            )
            self.session = await self.exit_stack.enter_async_context(ClientSession(*stdio_transport))

        elif config["type"] == "sse":
            context = streamablehttp_client(url=config["url"], headers=config["headers"])
            print("Connecting to SSE server with streamablehttp_client...")

            read_stream, write_stream, get_session_id = await self.exit_stack.enter_async_context(context)
            await self._run_session(read_stream, write_stream, get_session_id)

        await self.session.initialize()
        tools = await self.session.list_tools()
        print("🔧 Tools available:")
        for tool in tools.tools:
            print(f"  - {tool.name}: {tool.description}")

    async def get_mcp_tools(self) -> List[Dict[str, Any]]:
        tools = await self.session.list_tools()
        return [{
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.inputSchema,
            }
        } for t in tools.tools]

    async def _run_session(self, read_stream, write_stream, get_session_id):
        """Run the MCP session with the given streams, adding ClientSession to the exit stack."""
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

    async def process_query(self, query: str) -> str:
        tools = await self.get_mcp_tools()

        response = await self.openai_client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": query}],
            tools=tools,
            tool_choice="auto"
        )

        assistant_msg = response.choices[0].message
        messages = [{"role": "user", "content": query}, assistant_msg]

        if assistant_msg.tool_calls:
            for call in assistant_msg.tool_calls:
                print(f"🔧 Calling tool: {call.function.name} with args: {call.function.arguments}")
                result = await self.session.call_tool(
                    call.function.name,
                    arguments=json.loads(call.function.arguments)
                )
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result.content[0].text
                })

            final = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="none"
            )
            return final.choices[0].message.content

        return assistant_msg.content

    async def cleanup(self):
        await self.exit_stack.aclose()
