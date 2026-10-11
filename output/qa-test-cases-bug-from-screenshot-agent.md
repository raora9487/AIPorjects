# Test Cases — Create Jira Bug from Screenshot (n8n agent)

Workflow under test: `Agents/04_CreateJiraBugFromScreenshot_AIAgent.json`
Requirements covered: section 13 (credentials, original-screenshot preservation,
Jira bug creation + attachment, execution order, final response, testing).

## Scope

Verifies that an uploaded screenshot is analysed by the Groq vision model,
turned into a Jira Bug only after human approval, and that the **original,
unmodified** screenshot binary is attached to the created Jira issue. Also
verifies the failure/partial-success paths and the safe attachment-retry path.

## Preconditions (run once before the suite)

1. `Groq API (Header Auth)` credential created in the n8n credential manager
   (header `Authorization`, value `Bearer <GROQ_API_KEY>`) and selected on the
   `Groq Vision Analysis` node.
2. `Jira SW Cloud account` credential created (base URL, email, API token) and
   selected on all three Jira nodes.
3. `Normalize Screenshots` node config set: `jira_base_url`, `jira_project_key`,
   `groq_vision_model`.
4. `Create Jira Bug` node set to the target project and the `Bug` issue type.
5. A Jira account with **Browse Projects** and **Create Attachments**
   permissions on the project.
6. Test data: `small-error.png` (valid, ~200 KB), `large.png` (> 10 MB),
   `notes.txt` (non-image), and one issue that already has an attachment.

## Test data / configuration

| Item | Value |
| --- | --- |
| Form path | `/report-bug-screenshot` |
| Max attachment size check | 10 MB (`max_attachment_bytes` in `Normalize Screenshots`) |
| Duplicate search | JQL `project = "<key>" AND issuetype = Bug AND (summary ~ "...")` |
| Attachment endpoint | `POST /rest/api/3/issue/{issueIdOrKey}/attachments` |
| Required header | `X-Atlassian-Token: no-check` |

## Test cases

### TC-01 — Screenshot analysis and Jira bug creation both succeed
1. Open the form, upload `small-error.png`, add context, submit.
2. Approve the bug on the approval form.
- **Expected:** Jira bug is created with the AI summary/description/priority.
  The screenshot is attached. Final response shows `Issue`, `Summary`,
  `Priority`, `Screenshot`, `Attachment Status: Successfully uploaded`, and
  `Jira URL`. `outcome = success`.

### TC-02 — Original screenshot appears in the Jira attachment section
1. Run TC-01.
2. Open the created issue in Jira and expand **Attachments**.
- **Expected:** The attached file is byte-identical to `small-error.png`
  (matches file name and size; no AI-generated replacement, no text file).

### TC-03 — Issue created but attachment upload fails (partial success)
1. Revoke **Create Attachments** permission for the API account (or force a 413
   by lowering the Jira attachment limit).
2. Run TC-01.
- **Expected:** Bug is created; final response is `PARTIAL SUCCESS` showing the
  issue key/URL and `Attachment Status: FAILED (ATTACHMENT_PERMISSION_DENIED`
  or `ATTACHMENT_TOO_LARGE)`. The bug is **not** rolled back and no second bug
  is created.

### TC-04 — Jira issue creation fails
1. Point `Create Jira Bug` at an invalid project, or remove Create-Issue
   permission.
2. Run TC-01.
- **Expected:** No attachment step runs. Final response reports
  `Bug report could not be completed` with the error code and no issue key.

### TC-05 — Uploaded image binary is lost or unavailable
1. Simulate the binary being unavailable at attachment time (e.g. replace the
   uploaded binary property before the attach step).
- **Expected:** Attachment is not attempted with empty data. Final response
  reports `SCREENSHOT_BINARY_MISSING`; no malformed/zero-byte attachment is sent.

### TC-06 — Image exceeds the permitted size
1. Upload `large.png` (> 10 MB).
- **Expected:** `Validate Screenshot` fails with `SCREENSHOT_TOO_LARGE` before
  the vision or Jira calls. Final response reports the size error.

### TC-07 — Jira rejects the attachment (permissions / file restriction)
1. Use an attachment type blocked by Jira (or a project without attachment
   permissions).
- **Expected:** `Verify Attachment Upload` classifies the failure
  (`ATTACHMENT_PERMISSION_DENIED` / `ATTACHMENT_UPLOAD_FAILED`) and the result
  is partial success, not overall success.

### TC-08 — Retry uploads to the existing issue (no duplicate bug)
1. Produce a TC-03 partial success and note the issue key.
2. Re-submit the same screenshot using the *Re-attach only: existing Jira key*
   field with that key.
- **Expected:** The workflow skips vision/create, uploads the screenshot to the
  existing issue, and reports success. No new Jira issue is created, and the
  screenshot is not attached twice (dedupe via existing-attachment check).

### TC-09 — Multiple screenshots attached to the correct issue
1. Upload two or more screenshots in one submission; approve.
- **Expected:** Every uploaded screenshot is attached to the single created
  issue (one item per file in `Plan Attachments` / `Attach Screenshot`). The
  final response lists all file names.

### TC-10 — User rejects the bug report
1. Upload `small-error.png` and submit.
2. Choose **Reject** on the approval form.
- **Expected:** Neither a Jira issue nor an attachment is created. Final
  response is `Report rejected by the reviewer...`.

## Traceability

| Requirement | Covered by |
| --- | --- |
| 13.A Credentials in credential manager | Preconditions 1–2; node credential refs |
| 13.B Preserve original screenshot | TC-02, TC-05, TC-09 |
| 13.C Create bug + attach (multipart, `file`, `no-check`) | TC-01, TC-02, TC-09 |
| 13.D Execution order / safe retry / no duplicates | TC-03, TC-04, TC-08 |
| 13.E Final success + partial-success response | TC-01, TC-03 |
| 13.F Testing cases 1–10 | TC-01 … TC-10 |

## Exit criteria

The workflow is **not** marked fully successful unless both the Jira issue and
its screenshot attachment are confirmed. Partial success must always be shown
as partial, with the issue key/URL preserved and a safe retry hint.
