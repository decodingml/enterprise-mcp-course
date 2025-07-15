# File: Makefile

.PHONY: run webhook install dev-shell

# Activate virtualenv and install dependencies with uv
install:
	uv pip install -r pyproject.toml

# Launch the main app (PR Assistant manual test)
run:
	uv run python src/main.py

# Start the webhook server (FastAPI + GitHub integration)
webhook:
	cd pr-reviewer-mcp-clients && uvicorn src.webhook:app --reload

# Drop into shell with correct working dir
dev-shell:
	cd pr-reviewer-mcp-clients && uv venv && uv pip install -r pyproject.toml && zsh

# Run the GitHub OAuth registration CLI to obtain access token
register:
	uv run python src/oauth_cli.py