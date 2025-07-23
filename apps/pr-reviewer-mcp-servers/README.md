# PR Reviewer MCP Server

This is the MCP server implementation for PR reviewer tools.

## Structure

```
apps/pr-reviewer-mcp-servers/
  pyproject.toml
  README.md
  src/
    server.py           # Main MCP server entry point
    config.py           # Configuration and environment loading
    tool_registry.py    # Tool registration and schema
    tools/              # (Optional) Custom tool implementations
      __init__.py
      pr_tools.py       # Example: PR review tool logic
    utils/              # (Optional) Utility/helper functions
      __init__.py
      logger.py
```

## Quickstart

- Install dependencies: `poetry install`
- Run the server: `python src/server.py`
