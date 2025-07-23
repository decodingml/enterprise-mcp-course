from fastmcp import FastMCP
from prompts import PR_REVIEW_PROMPT

# Instantiate MCP for Prompts
agent_scope_mcp = FastMCP("agent_scope_prompts")

@agent_scope_mcp.prompt(
    name="pr_review_prompt",
    description="Prompt for reviewing pull requests"
)
def pr_review_prompt():
    return PR_REVIEW_PROMPT


# agent_scope_mcp.run(transport="streamable-http", host="localhost", port=8002)
