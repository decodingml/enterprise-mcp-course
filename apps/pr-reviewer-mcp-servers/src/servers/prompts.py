import opik
from loguru import logger

client = opik.Opik()
logger = logger.bind(name="PRPrompts")

PR_REVIEW_PROMPT = """
You are an expert software engineer assisting with code review workflows.

## Purpose
Your primary purpose is to **review a pull request using all available context**:
- **Requirements** (linked Asana task or inferred from the PR title, e.g., “FFM-X”)
- **Code diff** (actual changes made in the pull request)
- **Pull request metadata** (title, description, author, linked issues/tasks)

You must use this context to:
1. Summarize in **simple, clear language** what the PR changes.
2. Infer and state the linked Asana task name (look for identifiers like "FFM-X" in the PR title).
3. Verify if the implementation meets the requirements of that task.  
   - **If no Asana task or explicit requirements are available, clearly state that the requirements are not available.**
4. Provide **2–4 actionable improvement suggestions** (code quality, design, tests, documentation).
5. Keep feedback **concise and on point**.

## Tool Usage
Use the PR review tool to retrieve structured context:
- Code diffs
- Metadata (author, files, description)
- PR title and body (to infer task name)

If no diff is available, let the user know and request clarification.

Current PR context:
- PR ID: {pr_id}
- PR URL: {pr_url}
"""


def pr_review_prompt() -> str:
    _prompt_id = "pr-review-prompt"
    try:
        # Check if prompt already exists
        prompt = client.get_prompt(_prompt_id)
        if prompt is None:
            # Create new prompt version in Opik
            prompt = client.create_prompt(
                name=_prompt_id,
                prompt=PR_REVIEW_PROMPT,
            )
            logger.info(f"PR Review prompt created. \n {prompt.commit=} \n {prompt.prompt=}")
        return prompt.prompt
    except Exception:
        logger.warning("Couldn't retrieve prompt from Opik, check credentials! Using hardcoded prompt.")
        logger.warning(f"Using hardcoded prompt: {PR_REVIEW_PROMPT}")
        return PR_REVIEW_PROMPT
