import opik
from fastmcp import FastMCP
from servers.prompts import get_pr_review_prompt

# Instantiate MCP for Prompts
agent_scope_mcp = FastMCP("agent_scope_prompts")


@agent_scope_mcp.prompt(
    name="pr_review_prompt",
    description="Prompt for reviewing pull requests"
)
@opik.track(name="pr_review_prompt", type="general")
def pr_review_prompt(arguments: dict):
    """
    Format the PR_REVIEW_PROMPT using the provided arguments dict.
    All keys in arguments will be passed as keyword arguments to format().
    """
    return get_pr_review_prompt().format(**arguments)


# agent_scope_mcp.run(transport="streamable-http", host="localhost", port=8002)
