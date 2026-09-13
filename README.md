# AIPorjects

AI-assisted QA tooling that turns Jira requirements into test plans and test cases.

This repository collects two complementary pieces of an AI-augmented testing
workflow: a **Command Code skill** for review-ready test planning, and a
**local Streamlit application** for generating test cases from Jira stories with
a privately hosted LLM.

## Contents

| Path | What it is |
| --- | --- |
| `.commandcode/skills/testplan-create/` | Command Code skill: Jira ticket → review-ready test plan |
| `.commandcode/TestCaseGeneratorOllama/` | Streamlit app: Jira story → test cases via local Ollama |
| `output/` | Sample generated artifacts (test plan for `KAN-5` in Markdown + PPTX) |
| `HelloWorld.java` | Scratch Java sample |

## 1. Test Plan Generator (Command Code skill)

Turns a Jira ticket into a **test plan a human still has to approve** — never a
"done" artifact. It fetches the ticket, runs a gap/ambiguity analysis against a
requirement checklist, fills the standard template, and stops at a mandatory
human review gate.

- `SKILL.md` — workflow, output shape, guardrails
- `references/requirement-checklist.md` — gap-analysis checklist
- `references/test-plan-template.md` — the plan template
- `scripts/fetch_jira.sh` — pulls a ticket via the Jira REST API

Uses `JIRA_BASE_URL`, `JIRA_EMAIL`, and `JIRA_TOKEN` from the environment.

## 2. Jira Test Case Generator (Streamlit + Ollama)

A lightweight local QA assistant: enter a Jira issue key, and it fetches the
story through the Jira REST API and generates structured test cases with a
locally hosted Ollama model — no manual copy/paste and no data leaving your
machine beyond the Jira API calls.

Highlights:

- ChatGPT-style conversational UI using native Streamlit components
- Test cases grounded strictly in the retrieved story and its acceptance
  criteria (positive, negative, boundary, validation, error-handling,
  business-rule, integration, permission, data, regression)
- Settings screen with validation, masked API key, and connection tests
- Credentials never appear in logs, exception messages, or generated responses

### Running it

```bash
cd .commandcode/TestCaseGeneratorOllama/jira_test_case_generator
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
ollama pull llama3
streamlit run app.py
```

Configure Jira and Ollama either in the Settings screen or via a local `.env`
(see `.env.example`). Requires Python 3.9+.

## Security

Credentials are **not** committed. `.env` files are git-ignored; use
`.env.example` as the template and supply your own Jira URL, email, and API
token locally.

## License

MIT
