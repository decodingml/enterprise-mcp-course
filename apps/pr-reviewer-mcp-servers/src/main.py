
import anyio
from tool_registry import McpServersRegistry
from config import settings

def main():
    mcp_tool_manager = McpServersRegistry()
    anyio.run(mcp_tool_manager.initialize)
    
    mcp_tool_manager.get_registry().run(
        transport="streamable-http", host="localhost", port=settings.REGISTRY_PORT
    )

if __name__ == "__main__":
    main()