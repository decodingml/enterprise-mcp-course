from abc import ABC, abstractmethod
from typing import Any, Dict, List

class MCPClientInterface(ABC):
    """
    Abstract base class for an MCP client.
    Defines the interface for connecting to a server, listing tools, and calling tools.
    """

    @abstractmethod
    async def connect_to_server(self, server_key: str) -> None:
        """
        Connect to the specified MCP server.
        Args:
            server_key (str): The key or identifier for the server to connect to.
        """
        pass

    @abstractmethod
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List available tools from the connected server.
        Returns:
            List[Dict[str, Any]]: A list of tool metadata dictionaries.
        """
        pass

    @abstractmethod
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a tool by name with the given arguments.
        Args:
            tool_name (str): The name of the tool to call.
            arguments (Dict[str, Any]): Arguments for the tool.
        Returns:
            Any: The result of the tool call.
        """
        pass
