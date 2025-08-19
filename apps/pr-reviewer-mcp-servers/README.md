
<table style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td width="20%" style="border: none;">
      <a href="https://decodingml.substack.com/" aria-label="Decoding ML">
        <img src="https://github.com/user-attachments/assets/f2f2f9c0-54b7-4ae3-bf8d-23a359c86982" alt="Decoding ML Logo" width="150"/>
      </a>
    </td>
    <td width="80%" style="border: none;">
      <div>
        <h2>📬 Stay Updated</h2>
        <p><b><a href="https://decodingml.substack.com/">Join Decoding ML</a></b> for proven content on designing, coding, and deploying production-grade AI systems with software engineering and MLOps best practices to help you ship AI applications. Every week, straight to your inbox.</p>
      </div>
    </td>
  </tr>
</table>

<p align="center">
  <a href="https://decodingml.substack.com/">
    <img src="https://img.shields.io/static/v1?label&logo=substack&message=Subscribe%20Now&style=for-the-badge&color=black&scale=2" alt="Subscribe Now" height="40">
  </a>
</p>

------

## 🚀 Project Overview

This project is part of the **MCP Enterprise Series**, where we teach you how to use the **Model Context Protocol (MCP)** at a **production level**. The series focuses on best practices for building scalable automation systems that combine tools, resources, and prompt templates—powering intelligent workflows across your enterprise.

This folder contains the **MCP Servers**: independent, modular services that expose enterprise resources, tool APIs, and prompt libraries.  

All these services are **aggregated into a single MCP Global Server**, which automatically assigns **tags** to each resource, allowing you to **filter and query** them easily. This unified view ensures all available services in your enterprise are accessible from one place.

# The PR Reviewer MCP Servers

These servers can run independently and provide the following features:

- **GitHub MCP Server** – Exposes tools for pull request details, comments, diffs, files, reviews, and statuses.
- **Slack MCP Server** – Tools for sending messages and fetching channel history.
- **Asana MCP Server** – Tools for finding and creating tasks.
- **Prompt Server** – Provides curated prompt templates for LLM-driven workflows.

All these tools and resources are **aggregated into the Tool Registry**, a central catalog maintained by the **MCP Global Server**.  

# Table of Contents

- [📋 Prerequisites](#-prerequisites)
- [☁️ Cloud Services](#-cloud-services)
- [🎯 Getting Started](#-getting-started)
- [📁 Project Structure](#-project-structure)
- [⚡️ Running the Servers](#-running-the-servers)
- [🧪 Testing the Servers](#-testing-the-servers)
- [📝 Example: Using the MCP Tool Registry](#-example-using-the-mcp-tool-registry)
- [👁️ Observability with Opik](#-observability-with-opik)
- [�🛠 Utility Commands](#-utility-commands)

# 📋 Prerequisites

| Tool | Version | Purpose | Installation Link |
|------|---------|---------|------------------|
| Python | 3.12 | Programming language runtime | [Download](https://www.python.org/downloads/) |
| uv | ≥ 0.4.30 | Python package installer and virtual environment manager | [Download](https://github.com/astral-sh/uv) |
| GNU Make | ≥ 3.81 | Build automation tool | [Download](https://www.gnu.org/software/make/) |
| Git | ≥2.44.0 | Version control | [Download](https://git-scm.com/downloads) |
| Docker | ≥27.4.0 | Containerization platform | [Download](https://www.docker.com/get-started/) |

# ☁️ Cloud Services

Some servers require access to external APIs. Authentication is managed via environment variables in your `.env` file:

| Service | Purpose | Env Variable |
|---------|---------|-------------|
| GitHub API | PR data, comments, status | `GITHUB_ACCESS_TOKEN` |
| Slack API | Messaging, channel info | `SLACK_BOT_TOKEN` |
| Asana API | Task management | `ASANA_ACCESS_TOKEN` |
| Opik | Observability, analytics & tracing | `OPIK_API_KEY` |

Instructions and links for obtaining these API tokens are provided in the sections below, see the **Getting Started** steps for detailed tutorials and resources.

# 🎯 Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/decodingml/enterprise-mcp-series.git
   cd enterprise-mcp-series/apps/pr-reviewer-mcp-servers
   ```

2. **Set up your environment variables**  

Before you can use the APIs, you must register your own app with each service to obtain the required credentials (Client ID, Client Secret and API Tokens). 

> **Note:** OAuth 2.0 is typically designed for apps where each user authenticates individually. In this enterprise setup, you only need to register the MCP server as a single client—registration is a one-time step for your organization. For the application callback URL, you do not need to provide a real endpoint when running locally (unless you want to expose a secure endpoint).

Follow these steps:

**a. Register your app in Slack & Github:**

- **Slack:** [Create a Slack App & Get Credentials](https://api.slack.com/authentication/oauth-v2)
- **GitHub:** [Register an OAuth App in Github](https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app)

> **Token Tip:** When authorizing your GitHub app or Slack app, you can simply copy the code directly from the URL after the browser redirects you (as highlighted in the image above) and paste it into the CLI, as requested. This makes it easy to obtain the GitHub/Slack bot token for your MCP server without deploying a public callback endpoint during development.

  ![GitHub code example](/static/github-code.png)

After registering, you will receive a **Client ID** and **Client Secret** for each service.

**b. Copy the example environment file and edit it:**
  ```bash
  cp .env.example .env
  ```  

**c. Open `.env` and fill in the required credentials:**
  ```dotenv
  SLACK_CLIENT_ID=<your_slack_client_id>
  SLACK_CLIENT_SECRET=<your_slack_client_secret>
  GITHUB_CLIENT_ID=<your_github_client_id>
  GITHUB_CLIENT_SECRET=<your_github_client_secret>
  ```

**d. Run the registration commands:**

- For Slack:
  ```bash
  make register-slack
  ```
- For GitHub:
  ```bash
  make register-github
  ```
These commands will guide you through the process of authorizing your app and obtaining the required API tokens.

> **Note:**  
> It’s important to understand why we use a **GitHub App integration** instead of calling the **GitHub MCP remote server** or the **GitHub API** directly with a PAT (Personal Access Token).  
>
> A **GitHub App** is a registered integration that provides fine-grained permissions, webhook support, and secure authentication. It’s the recommended approach for production and enterprise environments.  
>
> Both the **GitHub MCP remote server** and the **GitHub API** (REST/GraphQL) are ways to access GitHub data. However, they rely on credentials—such as tokens—issued by a GitHub App to operate securely and within GitHub’s permission model.


**e. Open `.env` and fill in the rest of required credentials:**
  ```dotenv
  ASANA_TOKEN=<your_asana_token>
  ASANA_PROJECT_GID=<your_project_id>
  SLACK_BOT_TOKEN=<your_slack_bot_token>
  GITHUB_ACCESS_TOKEN="<your_github_access_token>"
  OPIK_API_KEY="<your_opik_api_key>"
  ```

3. **Install project dependencies**
```bash
   deactivate
   uv venv .venv
   . .venv/bin/activate
   make install
   ```

# 📁 Project Structure

```bash
apps/pr-reviewer-mcp-servers/
├── src/
│   ├── clients/                     # API clients for external services
│   │   ├── __init__.py
│   │   ├── asana_client.py          # Asana API client
│   │   └── slack_client.py          # Slack API client
│   ├── servers/                     # MCP servers for external integrations
│   │   ├── __init__.py
│   │   ├── agent_scope_server.py    # Agent Scope Prompt server
│   │   ├── asana_server.py          # Asana MCP server
│   │   ├── github_server.py         # GitHub MCP server
│   │   ├── prompts.py               # Prompt templates
│   │   ├── slack_server.py          # Slack MCP server
│   │   └── tool_registry.py         # Tool registry server
│   ├── utils/                       # Utility modules & helpers
│   │   ├── __init__.py
│   │   ├── oauth_github.py          # GitHub OAuth flow
│   │   ├── oauth_slack.py           # Slack OAuth flow
│   │   └── opik_utils.py            # Observability helpers for Opik
│   ├── config.py                    # Configuration handling
│   └── main.py                      # Application entry point
├── tests/                               # Test suites for servers & utilities
│   ├── test_agent_scope_server.py       # Tests for Agent Scope Prompt server
│   ├── test_asana_server.py             # Tests for Asana MCP server
│   ├── test_github_server.py            # Tests for GitHub MCP server
│   ├── test_slack_server.py             # Tests for Slack MCP server
│   └── test_tool_registry.py            # Tests for Tool registry server
├── .env                             # Local environment variables
├── .env.example                     # Example env vars template
├── Makefile                         # Common development commands
├── pyproject.toml                   # Project dependencies & metadata
├── README.md                        # Project documentation
```


# ⚡️ Running the Servers

All servers are aggregated in the **Tool Registry** (see `src/tool_registry.py`). You can boot up all servers together using:

```bash
make run
```

The Tool Registry imports and registers each server using code like:

```python
await self.registry.import_server(asana_mcp, prefix="asana")
await self.registry.import_server(agent_scope_mcp, prefix="scope")
await self.registry.import_server(slack_mcp, prefix="slack")
await self.registry.import_server(github_mcp, prefix="github")
```

To add or remove servers, simply modify these lines in `src/tool_registry.py`.

---

**Running servers independently:**

Each server can also be started on its own. For example, to run the Slack server:

1. Uncomment the following line in `src/slack_server.py`:
   ```python
   slack_mcp.run(transport="streamable-http", host="localhost", port=8003)
   ```
2. Then run:
   ```bash
   make run-slack-server
   ```

**Warning:** When switching back to using the Tool Registry, comment out the `slack_mcp.run(...)` line again. This applies to all servers if you want to run them independently.

You can also run other servers individually by uncommenting their respective `.run(...)` lines and using the appropriate Makefile target (e.g., `make run-github-server`, `make run-asana-server`).


# 🧪 Testing the Servers

You can test all servers together (as registered in the Tool Registry) using:

```bash
make test
```

This will run the tests for the Tool Registry containing all aggregated servers.
**Warning:** Make sure the Tool Registry is running on the expected port first.

To test a specific server independently (e.g., Slack), you must first run that server in standalone mode:

1. Uncomment the `.run(...)` line in the server file (e.g., `slack_mcp.run(...)` in `src/slack_server.py`).
2. Start the server:
   ```bash
   make run-slack-server
   ```
3. In a separate terminal, run the test:
   ```bash
   make test-slack
   ```

**Note:** When finished, comment out the `.run(...)` line again before returning to Tool Registry mode.


# 📝 Example: Using the MCP Tool Registry

Each server exposes tools via the MCP standard and can be called from any compatible MCP host or client. 

For example, you can use the MCP Tool Registry with any MCP-compliant host to call tools like `get_pull_request` from the GitHub server (see `tests/test_github_server.py`):

```python
result = await client.call_tool("get_pull_request", {"owner": "my-org", "repo": "my-repo", "pullNumber": 42})
print(result)
```


# 👁️ Observability with Opik

This project uses [Opik](https://opik.ai/) for tracing and analytics of all MCP server workflows.
By default, traces and spans are grouped under the `pr_reviewer_servers` project (set via `OPIK_PROJECT_ID` in your `.env`), but you can change this value as needed.
Once your servers are running and processing requests, visit your [Opik dashboard](https://app.opik.ai/) and select your project (e.g., `pr_reviewer_servers` if not overwritten).

You will see traces for each server event, including:

- Tool calls from hosts
- API requests to GitHub, Slack, Asana, etc.
- Prompt fetches and responses

![Observability with Opik](/static/opik_servers.png)

 Additionally, the prompts served by the MCP Servers are versioned and tracked in the Prompts Library.

![Prompt Versioning with Opik](/static/opik_prompts.png)

# 🛠 Utility Commands

Here are some handy `make` commands to simplify development:

| Command                | Description                                 |
|------------------------|---------------------------------------------|
| make install           | Install all dependencies                    |
| make run               | Start all servers via the Tool Registry     |
| make run-asana         | Start the Asana MCP server                  |
| make run-agent-scope   | Start the Agent Scope Prompt server         |
| make run-slack         | Start the Slack MCP server                  |
| make run-github        | Start the GitHub MCP server                 |
| make test              | Run all Tool Registry tests                 |
| make test-asana        | Run Asana MCP server tests                  |
| make test-agent-scope  | Run Agent Scope Prompt server tests         |
| make test-slack        | Run Slack MCP server tests                  |
| make test-github       | Run GitHub MCP server tests                 |
| make register-slack    | Register Slack app and obtain tokens        |
| make register-github   | Register GitHub app and obtain tokens       |
| make typecheck  | Run static type checks and linting.           |

These commands help you quickly set up, run, and validate your development environment without remembering long CLI commands.

