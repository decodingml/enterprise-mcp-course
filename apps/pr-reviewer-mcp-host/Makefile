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
	PYTHONPATH=src uv run uvicorn api.webhook:app --host 0.0.0.0 --port 8000

# Run the GitHub OAuth registration CLI to obtain access token
register:
	PYTHONPATH=src uv run python src/utils/oauth_cli.py