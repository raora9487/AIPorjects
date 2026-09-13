"""Prompt construction for test-case generation.

The full LLM prompt lives here, not in the Streamlit UI code, so the prompt
can be evolved and reviewed independently of the interface.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence

from models.data_models import JiraStory

QA_SYSTEM_PROMPT = """You are an experienced senior QA test engineer specializing in \
functional, regression, and acceptance testing. You analyze Jira user stories and \
produce precise, traceable, professional test cases.

Rules you must follow:
1. Base every test case strictly on the Jira story and acceptance criteria provided.
2. Never invent business rules, fields, or behavior that the story does not support.
3. If required information is missing, state it explicitly under "Assumptions and Gaps".
4. Map each test case to the acceptance criterion it validates wherever possible.
5. Cover positive, negative, boundary, validation, error-handling, business-rule,
   integration, permission, data, and regression scenarios when they apply.
6. Clearly distinguish mandatory/optional fields and field-level validation.
7. Do not include credentials, tokens, or environment details in your output.

Output format (Markdown):
- A short "Scope Summary" describing what is being tested.
- A "Test Cases Overview" table with the columns:
  Test Case ID | Test Case Title | Type | Priority | Covers (AC reference)
- Detailed sections for every test case, each containing:
  Objective, Preconditions, Test Data, Test Steps (numbered), Expected Result.
- A final "Assumptions and Gaps" section when information is missing.
"""

_FOLLOW_UP_CONTEXT = """Continue the test-case conversation for the same Jira story. \
Reuse the story details already provided and keep the same output format.
"""


def _story_block(story: JiraStory) -> str:
    return (
        "Use the following Jira story as the single source of truth.\n\n"
        "----- BEGIN JIRA STORY -----\n"
        f"{story.to_prompt_text()}\n"
        "----- END JIRA STORY -----"
    )


def build_messages(
    story: JiraStory,
    user_request: str,
    history: Optional[Sequence[Dict[str, str]]] = None,
) -> List[Dict[str, str]]:
    """Build the chat messages sent to Ollama.

    Args:
        story: The Jira story that grounds the request.
        user_request: The user's natural-language instruction.
        history: Prior chat turns (user/assistant) for conversational context.
    """
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": f"{QA_SYSTEM_PROMPT}\n\n{_story_block(story)}"}
    ]

    for turn in history or []:
        role = turn.get("role")
        content = turn.get("content")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})

    if history:
        messages.append({"role": "system", "content": _FOLLOW_UP_CONTEXT})

    messages.append({"role": "user", "content": user_request})
    return messages
