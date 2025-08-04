
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

# 🚀 Project Overview
This project is part of the **MCP Enterprise Series**, where we teach you how to leverage the **Model Context Protocol (MCP)** at a **production level**.  
The series covers best practices for building scalable, multi-tool automation systems powered by LLMs.

The project is structured into **two main parts**:

1. **MCP Host** – The central orchestrator responsible for connecting to multiple MCP servers and coordinating their outputs.  
2. **MCP Servers** – Independent components that provide contextual data (e.g., GitHub diffs from the repository, Asana task details, and entries from a tool registry).

# The PR Reviewer MCP Host


This project is part of our **MCP Enterprise Series**, where we show you how to use the **Model Context Protocol (MCP)** at **production scale** to build intelligent, multi-tool automation systems.

Here, we focus on the **custom MCP Host**, an Agentic AI App that:

- **Gemini Integration** – Uses **Gemini (Google Generative AI)** to analyze pull requests and create code review suggestions.  
- **Automated Webhook** – A **FastAPI endpoint** triggers automatically whenever a **GitHub Pull Request** is opened.  
- **Context Gathering** – Collects key information from multiple MCP servers within the enterprise system, including GitHub diffs and linked Asana tasks.  
- **Slack Notifications** – Posts clear, actionable review summaries directly to your team's **Slack channel** for instant visibility.  

# Table of Contents

- [📋 Prerequisites](#-prerequisites)
- [☁️ Cloud Services](#-cloud-services)
- [🎯 Getting Started](#-getting-started)
- [Project Structure](#project-structure)
- [⚡️ Running the Host](#-running-the-host)
- [🌐 Exposing the PR Reviewer Host to GitHub](#-exposing-the-pr-reviewer-host-to-github)
- [👁️ Observability with Opik](#-observability-with-opik)
- [🛠 Utility Commands](#-utility-commands)

# 📋 Prerequisites

| Tool | Version | Purpose | Installation Link |
|------|---------|---------|------------------|
| Python | 3.12 | Programming language runtime | [Download](https://www.python.org/downloads/) |
| uv | ≥ 0.4.30 | Python package installer and virtual environment manager | [Download](https://github.com/astral-sh/uv) |
| GNU Make | ≥ 3.81 | Build automation tool | [Download](https://www.gnu.org/software/make/) |
| Git | ≥2.44.0 | Version control | [Download](https://git-scm.com/downloads) |
| Docker | ≥27.4.0 | Containerization platform | [Download](https://www.docker.com/get-started/) |

# ☁️ Cloud Services

This project requires access to the following cloud services.  
Authentication is managed via environment variables stored in your `.env` file:

| Service | Purpose | Cost | Environment Variable | Setup Guide | 
|---------|---------|------|---------------------|-------------|
| [Gemini API](https://ai.google.dev/gemini-api/docs) | LLM for PR review summaries | Pay-per-use (with free tier) | `GEMINI_API_KEY` | [Quick Start Guide](https://ai.google.dev/gemini-api/docs/get-started) |
| [Opik](https://opik.ai/) | Observability, analytics & tracing for LLM workflows | Free (with paid plans) | `OPIK_API_KEY` | [Opik Quick Start](https://docs.opik.ai/quickstart) | 


# 🎯 Getting Started

1. **Clone the repo**
   ```bash 
   git clone https://github.com/decodingml/enterprise-mcp-series.git
   cd enterprise-mcp-series/apps/pr-reviewer-mcp-host
   ```

2. **Set up your environment variables**  
- Copy the example environment file and edit it:  
  ```bash
  cp .env.example .env
  ```  
- Open `.env` and fill in the required credentials:  
  ```dotenv
  GEMINI_API_KEY="<your_gemini_api_key>"
  SLACK_CHANNEL_ID="<your_slack_channel_id>"
  TOOL_REGISTRY_URL="<your_slack_channel_id>"
  OPIK_API_KEY="<your_opik_api_key>"
  ```
  *The `SLACK_CHANNEL_ID` is the ID of the Slack channel your team uses for PR reviews (e.g., `C01234567`).*  


3. **Install project dependencies**  
  ```bash
  deactivate
  uv venv .venv
  . .venv/bin/activate
  make install
  ```

### How do you find your slack id channel?

1. Open the Slack channel you want to use for PR review updates.  
2. Click right on the channel name at the top to open **View channel details**.  
3. Scroll down to the bottom of the details view.  
4. Look for the **Channel ID** and click **Copy channel ID**.  

![Slack Channel ID](/static/slack_channel_id.png)
### ⚠️ Required MCP Servers

This project works as the **host and orchestrator**, so it relies on external **MCP servers** to provide the actual data and tools used in the PR review process.

These MCP servers are managed in the **separate project** located at `apps/pr-reviewer-mcp-servers`. You must start the **MCP Global Server** (from the other project) **before running this host** and provide its URL in **TOOL_REGISTRY_URL**.  



# Project Structure

```bash
apps/pr-reviewer-mcp-host/
├── src/
│   ├── api/                        # API layer for external event handling
│   │   ├── __init__.py
│   │   └── webhook.py              # Webhook endpoint for PR events
│   ├── host/                       # MCP host connection management
│   │   ├── __init__.py
│   │   ├── connection_manager.py   # Handles MCP server connections
│   │   └── host.py                 # Host runtime logic
│   ├── utils/                      # Utility modules
│   │   ├── __init__.py
│   │   └── opik_utils.py           # Observability utilities for Opik
│   ├── config.py                   # Configuration management
│   ├── main.py                     # Application entry point
│   └── test_gemini.py              # Experimental Gemini integration tests
├── .env                            # Local environment variables
├── .env.example                    # Example env vars template
├── .python-version                 # Python version pinning
├── Makefile                        # Common development commands
├── pyproject.toml                  # Project dependencies & metadata
└── README.md                       # Project documentation
```



# ⚡️ Running the Host


The webhook host is responsible for:  
- Listening for **GitHub Pull Request events**.  
- Gathering context (code diffs, linked tasks, tool metadata) from the running MCP servers.  
- Generating an intelligent review summary using **Gemini** and posting it to Slack.

**Run the webhook host app:**
```bash
make run
```
This will launch the server at `http://localhost:5001`.


## 🌐 Exposing the PR Reviewer Host to GitHub

Now that you have started the host on port `5001`, you need to make it accessible to GitHub for PR events delivery.

### Expose Your Local Server to the Internet with ngrok

Use [ngrok](https://ngrok.com/) to create a public URL that forwards requests to your local server:

```bash
ngrok http 5001
```

This will generate a public URL (e.g., https://ae82d4550d91.ngrok-free.app`) that forwards requests to your local server.

![ngrok example](/static/ngrok.png)

### Configure the GitHub Webhook

Copy the generated ngrok URL and add the endpoint suffix `/webhook` to it (e.g., `https://ae82d4550d91.ngrok-free.app/webhook`).
Go to your GitHub repository settings and add this as a webhook endpoint.


  ![GitHub webhook setup](/static/webhook.png)

Configure the webhook to trigger on **Pull Request** events (you can filter for `opened` actions in your code).

### How It Works

When a pull request is opened (or another configured event occurs), GitHub sends a POST request to your `/webhook` endpoint with a payload like:

```json
{
  "action": "opened",
  "pull_request": {
    "number": 42,
    "title": "Add new feature",
    "user": {"login": "octocat"}
  },
  "repository": {
    "name": "my-repo",
    "owner": {"login": "my-org"}
  }
}
```

See `src/api/webhook.py` for how this payload is processed.


# 👁️ Observability with Opik

This project uses [Opik](https://opik.ai/) for tracing and analytics of all LLM-powered workflows. 
By default, traces and spans are grouped under the `pr_reviewer_host` project (set via `OPIK_PROJECT_ID` in your `.env`), but you can change this value as needed.


Once your host is running and processing PR events, visit your [Opik dashboard](https://app.opik.ai/) and select your project (e.g., `pr_reviewer_host` if not overwritten).

You will see traces for each webhook event, including:

- The webhook trigger
- Context/tool fetches from MCP servers
- LLM (Gemini) calls
- Slack notification delivery

![Observability with Opik](/static/opik_host.png)


## 🛠 Utility Commands

Here are some handy `make` commands to simplify development:

| Command           | Description                                   |
|-------------------|-----------------------------------------------|
| `make run`        | Start the **FastAPI webhook server** locally. |
| `make install`    | Install all required dependencies.            |
| `make typecheck`  | Run static type checks and linting.           |

These commands help you quickly set up, run, and validate your development environment without remembering long CLI commands.

