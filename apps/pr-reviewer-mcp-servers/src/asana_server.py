
from clients.asana_client import AsanaClient
from fastmcp import FastMCP
import asyncio

# Instantiate MCP for Asana tools
asana_mcp = FastMCP("asana_tools")
asana_client = AsanaClient()


@asana_mcp.tool(
    description="Finds an Asana task by name.",
    tags={"asana", "task", "search"},
    annotations={"title": "Find Task", "readOnlyHint": False, "openWorldHint": True},
)
async def find_task(task_name: str):
    """Find an Asana task by name."""
    task = await asana_client.find_task(task_name)
    if task:
        return {"status": "success", "task": task}
    else:
        return {"status": "not_found", "task": None}


@asana_mcp.tool(
    description="Creates a new Asana task with the given name and description.",
    tags={"asana", "task", "create"},
    annotations={"title": "Create Task", "readOnlyHint": False, "openWorldHint": True},
)
async def create_task(task_name: str, description: str = ""):
    """Create a new Asana task."""
    task = await asana_client.create_task(task_name, description)
    return {"status": "created", "task": task}


# asana_mcp.run(transport= "streamable-http", host="localhost", port=8001)