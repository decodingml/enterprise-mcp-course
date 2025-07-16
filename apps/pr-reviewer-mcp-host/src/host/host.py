import json
from contextlib import AsyncExitStack
from typing import Optional, Any
from config import settings
from google import genai
from google.genai import types
from google.genai.types import Tool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client

from .tool_registry import AVAILABLE_SERVERS

SKIPPABLE_PROPS = ["additional_properties", "additionalProperties", "$schema"]

def strip_additional_properties(schema: dict) -> dict[Any, dict] | list[dict] | dict | list:
    if isinstance(schema, dict):
        return {
            k: strip_additional_properties(v)
            for k, v in schema.items()
            if k not in SKIPPABLE_PROPS
        }
    elif isinstance(schema, list):
        return [strip_additional_properties(item) for item in schema]
    else:
        return schema


class MCPHost:
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.model = model
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

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

    async def get_mcp_tools(self) -> list[Tool]:
        tools = await self.session.list_tools()

        return [
            types.Tool(
                function_declarations=[
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": strip_additional_properties({
                            k: v
                            for k, v in tool.inputSchema.items()
                            if k not in SKIPPABLE_PROPS
                        }),
                    }
                ]
            )
            for tool in tools.tools
        ]

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

    async def process_query(self, query: str) -> str:
        tools = await self.get_mcp_tools()
        config = types.GenerateContentConfig(
                temperature=0,
                tools=tools,
            )
        contents = [
            types.Content(
                role="user", parts=[types.Part(text=query)]
            )
        ]
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )
        # Check for function call
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call

            result = await self.session.call_tool(
                function_call.name, arguments=dict(function_call.args)
            )

            function_response_part = types.Part.from_function_response(
                name=function_call.name,
                response={"result": result},
            )

            # Append function call and result of the function execution to contents
            contents.append(response.candidates[0].content)  # Append the content from the model's response.
            contents.append(types.Content(role="user", parts=[function_response_part]))  # Append the function response

            final_response = self.client.models.generate_content(
                model=self.model,
                config=config,
                contents=contents,
            )

            return final_response.text
        else:
            print("No tool call required by Gemini")
            return response.text

    async def cleanup(self):
        await self.exit_stack.aclose()
