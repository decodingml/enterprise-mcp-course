
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
MAX_LLM_CALLS = 5

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

    @opik.track(name="get-system-prompt", type="general")
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
       
        llm_calls = 0
        while llm_calls < MAX_LLM_CALLS:
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config,
                )
            except Exception as e:
                logger.error(f"Error during LLM call #{llm_calls+1}: {e}")
                return f"[Error during LLM call: {e}]"
            llm_calls += 1
            contents.append(response.candidates[0].content)
            function_call_found = False

            for part in response.candidates[0].content.parts:
                if getattr(part, "function_call", None):
                    function_call_found = True
                    function_call = part.function_call
                    try:
                        result = await self.connection_manager.call_tool(
                            function_call.name, dict(function_call.args)
                        )
                    except Exception as e:
                        logger.error(f"Error during tool call '{function_call.name}': {e}")
                        result = f"[Error during tool call: {e}]"
                    function_response_part = types.Part.from_function_response(
                        name=function_call.name,
                        response={"result": result},
                    )
                    contents.append(types.Content(role="user", parts=[function_response_part]))

            if not function_call_found:
                parts = response.candidates[0].content.parts
                text_result = "".join([p.text for p in parts if hasattr(p, 'text') and p.text])
                logger.info(f"Final response after {llm_calls} LLM calls: {text_result}")
                return text_result 

        logger.error("Maximum LLM call limit reached without a final answer.")
        return None


    @opik.track(name="get-mcp-tools", type="general")
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
