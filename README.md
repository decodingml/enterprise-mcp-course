
<div align="center">
  <h1>Enterprise MCP Series: Build a PR Reviewer for Automated Code Reviews</h1>
  <h3>Build, orchestrate, and scale intelligent workflows with the Model Context Protocol</h3>
  <p class="tagline">Open-source project by <a href="https://decodingml.substack.com">Decoding ML</a></p>
</div>

</br>

<p align="center">
  <a href="https://decodingml.substack.com/p/enterprise-mcp-series">
    <img src="static/enterprise_mcp_architecture.png" alt="Enterprise MCP Architecture" width="600">
  </a>
</p>

## 📖 About This Series

The **Enterprise MCP Series** is an **open-source initiative** designed to help you **design, build, and deploy** modular, **production-grade AI automation systems** using the **Model Context Protocol (MCP)**.

In this series, we focus on building a **Pull Request Reviewer** for an enterprise project, showcasing how to integrate multiple tools and orchestrate them into a scalable, production-ready MCP architecture.

### 🎯 Why This Series?

Unlike simple tutorials, this series tackles **real-world, enterprise use cases**—like a **Pull Request Reviewer Assistant** that analyzes GitHub PRs, pulls context from Github and Asana, and posts actionable insights to your team on Slack.

- **Automate AI workflows** within your internal systems  
- **Build scalable infrastructure** – design workflows that support multiple automation pipelines, ready to grow with your organization  
- **Evaluate MCP for enterprise migration** – understand if migrating your codebase to an MCP-based architecture is worth it  


### 🛠 What You Will Learn

You will learn how to:

- **Build custom MCP Servers** for Slack, Asana, and GitHub to expose enterprise tools and resources  
- **Connect to external MCP servers** (e.g., GitHub Remote MCP) and integrate them seamlessly 
- **Centralize tools and prompts** into an internal **Tool Registry** (a global MCP server)  
- **Create a custom MCP Host** to orchestrate workflows (no reliance on Claude Desktop)  
- **Design and scale company-wide automation workflows**, starting with the PR Reviewer use case

 With these skills, you'll become a pro 🥷 at building enterprise-ready AI automation systems using MCP, designing your own scalable hosts, integrating internal tools, and orchestrating intelligent workflows across your company.

### 👥 Who Should Join?

| Target Audience        | Why Join? |
|------------------------|-----------|
| ML/AI Engineers        | Learn to orchestrate multiple **AI tools, agents, and resources** across your organization |
| Software Engineers     | Build **scalable, maintainable, and secure** automation workflows |
| DevOps & MLOps Engineers | Apply best practices in **software engineering, MLOps, and prompt engineering** to production AI systems |

## 🎓 Prerequisites

| Category    | Requirements                                                                                                                     |
|-------------|----------------------------------------------------------------------------------------------------------------------------------|
| **Skills**  | - Python (Intermediate) <br/> - REST APIs & Web development (Beginner) <br/> - Basic understanding of AI/LLM concepts (Beginner) |
| **Hardware**| Modern laptop/PC (no GPU required – all servers run locally or in lightweight containers)                                        |
| **Level**   | Begginer/Intermediate (anyone willing to learn can follow along)                                                             |

By using the **Gemini free tier**, this course can be completed at **zero cost**.

## 📚 Series Outline

| Lesson | Title | Focus                                                                                            |
|--------|-------|--------------------------------------------------------------------------------------------------|
| 1 | [**Designing AI Systems the MCP Way**](https://decodingml.substack.com) | **Architecting the solution** and understanding the MCP mindset.                                 |
| 2 | [**Automating Developer Workflows with MCP**](https://decodingml.substack.com) | **Implementing the full PR Reviewer Assistant** workflow end-to-end.                             |
| 3 | [**Agent Patterns and Workflow Architectures**](https://decodingml.substack.com) | **Exploring other agent patterns and workflow architectures** for scalable PR review automation. |


## 🏗️ Repository Structure

```bash
enterprise-mcp-series/
├── apps/
│   ├── pr-reviewer-mcp-host/      # MCP custom host & client
│   └── pr-reviewer-mcp-servers/   # Modular MCP servers (GitHub, Slack, Asana, etc.) & Tool Registry
├── static/                        # Architecture diagrams, images
├── LICENSE
└── README.md                     
```


## 🚀 Getting Started

Find detailed setup instructions in each app's documentation:

| Application                                                               | Documentation |
|---------------------------------------------------------------------------|---------------|
| MCP Host & Client Connection Manager <br/>                                | [apps/pr-reviewer-mcp-host](apps/pr-reviewer-mcp-host) |
| Modular MCP Servers <br/> (GitHub, Slack, Asana, Prompts) & Tool Registry | [apps/pr-reviewer-mcp-servers](apps/pr-reviewer-mcp-servers) |

## 💡 Questions & Support
Have questions or running into issues? We're here to help!

Open a [GitHub issue](https://github.com/decodingml/enterprise-mcp-series/issues) for:
- Technical questions
- Troubleshooting
- Suggestions or contributions

## 🥂 Contributing

As an open-source course, we may not be able to fix all the bugs that arise.

If you find any bugs and know how to fix them, support future readers by contributing to this course with your bug fix.

You can always contribute by:
- Forking the repository
- Fixing the bug
- Creating a pull request

We will deeply appreciate your support for the AI community and future readers 🤗

## Core Contributors

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/915-Muscalagiu-AncaIoana">
        <img src="https://github.com/915-Muscalagiu-AncaIoana.png" width="100px;" alt="Anca Ioana Muscalagiu"/><br />
        <sub><b>Anca Ioana Muscalagiu</b></sub>
      </a><br />
      <sub>SWE/ML Engineer</sub>
    </td>
    <td align="center">
      <a href="https://github.com/iusztinpaul">
        <img src="https://github.com/iusztinpaul.png" width="100px;" alt="Paul Iusztin"/><br />
        <sub><b>Paul Iusztin</b></sub>
      </a><br />
      <sub>AI/ML Engineer</sub>
    </td>
     </td>
  </tr>
</table>


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.