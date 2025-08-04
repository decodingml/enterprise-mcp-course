
import opik
import logging
from typing import Set

from fastmcp import FastMCP

from servers.asana_server import asana_mcp
from servers.slack_server import slack_mcp
from servers.github_server import github_mcp
from servers.agent_scope_server import agent_scope_mcp

log = logging.getLogger(__name__)


class McpServersRegistry:
    def __init__(self):
        self.registry = FastMCP("tool_registry")
        self.all_tags: Set[str] = set()
        self._is_initialized = False

    @opik.track(name="tool-registry-initialize", type="general")
    async def initialize(self):
        if self._is_initialized:
            return

        log.info("Initializing McpServersRegistry...")
        await self.registry.import_server(asana_mcp, prefix="asana")
        await self.registry.import_server(agent_scope_mcp, prefix="scope")
        await self.registry.import_server(slack_mcp, prefix="slack")
        await self.registry.import_server(github_mcp, prefix="github")

        all_tools = await self.registry.get_tools()
        for tool in all_tools.values():
            if tool.tags:
                self.all_tags.update(tool.tags)

        log.info(f"Registry initialization complete. Found tags: {self.all_tags}")
        self._is_initialized = True

    def get_registry(self) -> FastMCP:
        """returns the initialized tool registry."""
        return self.registry

    def get_all_tags(self) -> Set[str]:
        """returns the pre-calculated set of all tool tags."""
        return self.all_tags

