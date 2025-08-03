import logging
from typing import Any

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

    async def initialize(self):
        await self.connection_manager.initialize_all()

    async def get_system_prompt(self, name, args) -> str:
        if not self.connection_manager.is_initialized:
            raise RuntimeError("ConnectionManager is not initialized. Call initialize_all() first.")
        return await self.connection_manager.get_prompt(name, args)

    async def process_query(self, query: str) -> str:
        if not self.connection_manager.is_initialized:
            raise RuntimeError("ConnectionManager is not initialized. Call initialize_all() first.")
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

        contents.append(response.candidates[0].content)  # Append the content from the model's response.
        
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

                # Append function call and result of the function execution to contents
                logger.info(f"Function call '{function_call.name}' executed with result: {result}")
                contents.append(types.Content(role="user", parts=[function_response_part]))  # Append the function response
    
        final_response = self.client.models.generate_content(
            model=self.model,
            config=config,
            contents=contents,
        )

        return final_response.text
        

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
    
    async def call_tool(self, function_name: str, function_args: dict) -> Any:
        if not self.connection_manager.is_initialized:
            raise RuntimeError("ConnectionManager is not initialized. Call initialize_all() first.")
        return await self.connection_manager.call_tool(function_name, function_args)
    
    async def cleanup(self):
        await self.connection_manager.cleanup_all()
