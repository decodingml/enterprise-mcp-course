
import logging
import uuid
from typing import Any

import opik
from opik import opik_context
from google import genai
from google.genai import types
from google.genai.types import Tool

from config import settings
from host.connection_manager import ConnectionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_host")
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
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.connection_manager = ConnectionManager()
        self.thread_id = str(uuid.uuid4())

    @opik.track(name="host-initialize", type="general")
    async def initialize(self):
        opik_context.update_current_trace(thread_id=self.thread_id)
        await self.connection_manager.initialize_all()

    @opik.track(name="get-system-prompt", type="prompt")
    async def get_system_prompt(self, name, args) -> str:
        if not self.connection_manager.is_initialized:
            raise RuntimeError("ConnectionManager is not initialized. Call initialize_all() first.")
        return await self.connection_manager.get_prompt(name, args)

    @opik.track(name="process-query", type="llm")
    async def process_query(self, query: str) -> str:
        if not self.connection_manager.is_initialized:
            raise RuntimeError("ConnectionManager is not initialized. Call initialize_all() first.")
        opik_context.update_current_trace(thread_id=self.thread_id)
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

        contents.append(response.candidates[0].content)
        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_call = part.function_call
                result = await self.connection_manager.call_tool(
                    function_call.name, dict(function_call.args)
                )
                function_response_part = types.Part.from_function_response(
                    name=function_call.name,
                    response={"result": result},
                )
                logger.info(f"Function call '{function_call.name}' executed with result: {result}")
                contents.append(types.Content(role="user", parts=[function_response_part]))

        final_response = self.client.models.generate_content(
            model=self.model,
            config=config,
            contents=contents,
        )
        return final_response.text

    @opik.track(name="get-mcp-tools", type="tools")
    async def get_mcp_tools(self) -> list[Tool]:
        tools = await self.connection_manager.get_mcp_tools()
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

    @opik.track(name="call-tool", type="tool")
    async def call_tool(self, function_name: str, function_args: dict) -> Any:
        if not self.connection_manager.is_initialized:
            raise RuntimeError("ConnectionManager is not initialized. Call initialize_all() first.")
        return await self.connection_manager.call_tool(function_name, function_args)

    @opik.track(name="cleanup", type="general")
    async def cleanup(self):
        await self.connection_manager.cleanup_all()
