import opik
from clients.slack_client import SlackClient
from fastmcp import FastMCP
import utils.opik_utils as opik_utils

opik_utils.configure()
slack_mcp = FastMCP("slack_tools")
slack_client = SlackClient()


@slack_mcp.tool(
    description="Gets the last X messages from a Slack channel.",
    tags={"slack", "message", "channel", "history"},
    annotations={"title": "Get Last Messages", "readOnlyHint": True, "openWorldHint": True},
)
@opik.track(name="slack-get-last-messages", type="tool")
async def get_last_messages(channel_name: str, limit: int = 10):
    """Get the last X messages from a Slack channel."""
    messages = await slack_client.get_last_messages(channel_name, limit)
    return {"status": "success", "messages": messages}


@slack_mcp.tool(
    description="Posts a new message to a given channel.",
    tags={"slack", "message", "channel", "post"},
    annotations={"title": "Post Message", "readOnlyHint": False, "openWorldHint": True},
)
@opik.track(name="slack-post-message", type="tool")
async def post_message(channel_name: str, message: str = ""):
    """Posts a new message to a channel."""
    result = await slack_client.send_message(channel_name, message)
    return {"status": "created" if result.get("ok") else "error", "message": result}

#slack_mcp.run(transport= "streamable-http", host="localhost", port=8003)