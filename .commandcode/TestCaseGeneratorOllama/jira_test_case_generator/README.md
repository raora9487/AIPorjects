# Jira Test Case Generator

A lightweight local QA assistant that turns a Jira User Story into professional
test cases using a locally hosted Ollama model. Jira stories are fetched through
the Jira REST API, so there is no manual copy/paste, and LLM inference stays on
your machine for privacy.

## Features

- ChatGPT-style conversational UI built with native Streamlit components.
- Automatic retrieval of a Jira issue (summary, description, acceptance criteria,
  type, priority, status, labels, components, reporter, assignee).
- Test-case generation grounded strictly in the retrieved story and its
  acceptance criteria (positive, negative, boundary, validation, error-handling,
  business-rule, integration, permission, data and regression scenarios).
- Dedicated Settings screen with validation, masked API key, save/reset, and
  connection test buttons for both Jira and Ollama.
- Configuration kept outside the source code; credentials never appear in logs,
  exception messages, or generated responses.

## Project Structure

```text
jira_test_case_generator/
├── app.py                      # Streamlit entry point and navigation
├── config/
│   └── settings.py             # Configuration loading/persistence
├── services/
│   ├── jira_client.py          # Jira REST API integration
│   ├── ollama_client.py        # Ollama REST API integration
│   └── prompt_builder.py       # LLM prompt construction
├── ui/
│   ├── main_page.py            # Chat interface
│   └── settings_page.py        # Configuration screen
├── models/
│   └── data_models.py          # JiraStory / AppSettings
├── utils/
│   ├── validators.py           # Input validation
│   └── error_handler.py        # Exception hierarchy and safe messages
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.9+
- A reachable Jira instance with an API token
- A running Ollama server with at least one model pulled

## Setup

1. Create and activate a virtual environment (recommended).

   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

2. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Ollama is running and a model is available.

   ```bash
   ollama pull llama3
   ```

4. Configure Jira and Ollama, either through the Settings screen or by creating a
   `.env` file next to `app.py`:

   ```dotenv
   JIRA_BASE_URL=https://your-domain.atlassian.net
   JIRA_EMAIL=you@example.com
   JIRA_TOKEN=your-api-token
   OLLAMA_URL=http://localhost:11434
   OLLAMA_MODEL=llama3
   ```

   `OLLAMA_MODEL` is optional; when blank the first available model is used.
   Configuration is discovered from the application directory upwards, so a
   `.env` in a parent folder is also picked up.

## Running

```bash
streamlit run app.py
```

## Usage

1. Open the Settings page and save your Jira and Ollama configuration
   (use the connection test buttons to verify).
2. Return to **Test Case Generator**.
3. Enter a Jira User Story ID (for example `PROJ-1234`) in the sidebar.
4. Ask a question such as *"Design comprehensive functional and negative test
   cases for this user story."*
5. Review the generated test cases. Follow-up questions reuse the same story
   context; use **Reload Story** to re-fetch it, or **Clear Conversation** to
   start over.

## Security Notes

- The Jira API key is stored locally and masked in the UI.
- Credentials are stripped from log output and exception messages.
- No data leaves your machine except the Jira API calls required to read the issue.
