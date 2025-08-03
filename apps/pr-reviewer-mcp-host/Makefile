# File: Makefile

.PHONY: run install typecheck

# Activate virtualenv and install dependencies with uv
install:
	uv pip install -r pyproject.toml

# Start the webhook server
run:
	PYTHONPATH=src uv run uvicorn api.webhook:app --host 0.0.0.0 --port 5001

typecheck:
	mypy --strict src