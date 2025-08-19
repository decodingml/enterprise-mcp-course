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
	PYTHONPATH=src uv run python src/servers/asana_server.py

test-asana:
	uv run python tests/test_asana_server.py

run-agent-scope:
	PYTHONPATH=src uv run python src/servers/agent_scope_server.py

test-agent-scope:
	uv run python tests/test_agent_scope_server.py

run-slack:
	PYTHONPATH=src uv run python src/servers/slack_server.py

test-slack:
	uv run python tests/test_slack_server.py

run-github:
	PYTHONPATH=src uv run python src/servers/github_server.py

test-github:
	uv run python tests/test_github_server.py

register-github:
	PYTHONPATH=src uv run python src/utils/oauth_github.py

typecheck:
	mypy --strict src