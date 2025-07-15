from typing import Any, Dict, List, Optional
from contextlib import AsyncExitStack
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from .base_client import MCPClientInterface

class StreamableHTTPMCPClient(MCPClientInterface):
    """
    MCP client implementation for connecting to an MCP server using streamable HTTP.
    This class is generic and can be used for any compatible MCP server, not just GitHub.
    """
    def __init__(self, config):
        self.config = config
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_key: str) -> None:
        """
        Connect to the MCP server using streamable HTTP.
        Args:
            server_key (str): The key or identifier for the server to connect to.
        """
        server_cfg = self.config[server_key]
        context = streamablehttp_client(url=server_cfg["url"], headers=server_cfg["headers"])
        print("Connecting to MCP server with streamablehttp_client...")
        read_stream, write_stream, get_session_id = await self.exit_stack.enter_async_context(context)
        self.session = await self.exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
        await self.session.initialize()
        print("✅ Connected to MCP server")
        if get_session_id:
            session_id = get_session_id()
            if session_id:
                print(f"Session ID: {session_id}")

    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List available tools from the connected MCP server.
        Returns:
            List[Dict[str, Any]]: A list of tool metadata dictionaries.
        """
        if not self.session:
            raise RuntimeError("Not connected to server.")
        tools_result = await self.session.list_tools()
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": getattr(tool, "inputSchema", {})
            }
            for tool in tools_result.tools
        ]

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a tool by name with the given arguments.
        Args:
            tool_name (str): The name of the tool to call.
            arguments (Dict[str, Any]): Arguments for the tool.
        Returns:
            Any: The result of the tool call.
        """
        if not self.session:
            raise RuntimeError("Not connected to server.")
        result = await self.session.call_tool(tool_name, arguments)
        return result.content[0].text if hasattr(result, "content") and result.content else result
