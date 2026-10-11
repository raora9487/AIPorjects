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
| `Agents/` | Importable n8n workflows (Jira fetch, RCA, bug triage, screenshot → Jira bug) |
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

## 3. Bug Reporter from a Screenshot (n8n)

`Agents/` holds importable n8n workflow JSONs. The newest one,
`Agents/04_CreateJiraBugFromScreenshot_AIAgent.json`, turns an uploaded
screenshot into a Jira Bug **and attaches the original image** to that bug.

Execution order implemented by the workflow:

Screenshot Upload (form page 1) → Validate Screenshot → Groq Vision Analysis →
Validate AI Bug Report → Search Duplicate Bugs → Human Approval (form page 2) →
Create Jira Bug → Attach Original Screenshot → Verify Attachment → Show Result
(form ending page)

The approval is a **second form page** (an `n8n Form` node) shown in the same
browser session, and the final result is the form's **ending page**. The trigger
responds *when the last node finishes* so each page chains into the next without
the form hanging.

Key guarantees:

- The **original, unmodified** screenshot binary is preserved end to end. It is
  never replaced by an AI-generated image or a text description, and it is not
  discarded when the AI response is parsed.
- The bug is only created after an explicit human approval on a second form page
  (approve/reject dropdown), so nothing is created without a person saying yes.
- The attachment uses
  `POST /rest/api/3/issue/{issueIdOrKey}/attachments` as `multipart/form-data`
  (field name `file`) with the required `X-Atlassian-Token: no-check` header.
- Existing attachments are read first, so a retry cannot create a duplicate
  attachment, and the create step is **not** auto-retried (no duplicate bugs).
- If the bug is created but the attachment fails, the workflow reports a
  **partial success** with the issue key/URL plus a safe retry path (re-submit
  the same screenshot using the *Re-attach only* field with the existing key).

### Credentials (n8n Cloud credential manager)

Store every credential in n8n Cloud's credential manager. Never put secrets in
the workflow JSON, prompts, logs or Git. The Groq/Jira values are kept only in
the local, git-ignored `.env` for reference — they are **not** read by n8n; the
workflow uses n8n credentials.

| Credential | Type in n8n | Used by |
| --- | --- | --- |
| Groq API key | **Groq** (`groqApi`) — existing `Groq account` credential | `Groq Vision Analysis` |
| Jira Cloud (base URL + email + API token) | **Jira SW Cloud API** — existing `Jira SW Cloud account` credential | Create / fetch / attach Jira nodes |

- **Groq API key** — set the existing `Groq account` (`groqApi`) credential's
  key to the provided value. The `Groq Vision Analysis` node already references
  this credential.
- **Jira Cloud** — reuse the existing `Jira SW Cloud account` credential (base
  URL `https://raora9487.atlassian.net`, your email, your API token). All three
  Jira nodes reference it.

Non-secret settings (already filled in the `Normalize Screenshots` Code node):

- `jira_base_url` = `https://raora9487.atlassian.net`
- `jira_project_key` = `KAN` (My Software Team, project id 10001)
- `groq_vision_model` = `qwen/qwen3.8-27b`
- `max_completion_tokens` = `800` in the Groq request, kept under the tenant's
  Groq output-tokens-per-minute limit (1000) so the call isn't pre-rejected with
  a `429`. If you see a rate-limit message, wait about a minute and resubmit.

The `Create Jira Bug` node is set to project `KAN` and the `Bug` issue type
(id 10042).

### Testing

See [`output/qa-test-cases-bug-from-screenshot-agent.md`](output/qa-test-cases-bug-from-screenshot-agent.md)
for the full test cases (success, attachment failure, creation failure, missing
binary, oversize image, permission errors, safe retry, multiple screenshots,
rejection). The workflow is only considered fully successful when both the Jira
issue **and** its screenshot attachment are confirmed.

## Security

Credentials are **not** committed. `.env` files are git-ignored; use
`.env.example` as the template and supply your own Jira URL, email, and API
token locally.

## License

MIT
