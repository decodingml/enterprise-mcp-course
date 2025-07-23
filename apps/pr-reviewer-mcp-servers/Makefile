# File: Makefile

.PHONY: run webhook install dev-shell

# Activate virtualenv and install dependencies with uv
install:
	uv pip install -r pyproject.toml

run:
	uv run python src/main.py

test:
	uv run python tests/test_tool_registry.py

run-asana:
	uv run python src/asana_server.py

test-asana:
	uv run python tests/test_asana_server.py

run-agent-scope:
	uv run python src/agent_scope_server.py

test-agent-scope:
	uv run python tests/test_agent_scope_server.py

run-slack:
	uv run python src/slack_server.py

test-slack:
	uv run python tests/test_slack_server.py

register-slack:
	PYTHONPATH=src uv run python src/utils/oauth_slack.py
