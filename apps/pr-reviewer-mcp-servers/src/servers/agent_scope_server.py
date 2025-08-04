from fastmcp import FastMCP
from servers.prompts import PR_REVIEW_PROMPT

# Instantiate MCP for Prompts
agent_scope_mcp = FastMCP("agent_scope_prompts")

@agent_scope_mcp.prompt(
    name="pr_review_prompt",
    description="Prompt for reviewing pull requests"
)
def pr_review_prompt(arguments: dict):
    """
    Format the PR_REVIEW_PROMPT using the provided arguments dict.
    All keys in arguments will be passed as keyword arguments to format().
    """
    return PR_REVIEW_PROMPT.format(**arguments)


# agent_scope_mcp.run(transport="streamable-http", host="localhost", port=8002)
