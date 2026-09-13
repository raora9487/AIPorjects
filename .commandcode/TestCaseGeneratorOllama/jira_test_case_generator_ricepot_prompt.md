# RICEPOT PROMPT — JIRA TEST CASE GENERATOR

## R -> ROLE

You are a senior Python application architect, QA automation engineer, and AI application developer with 15+ years of experience in enterprise QA, Jira, test-case design, REST APIs, Python, Streamlit, and locally hosted Large Language Models.

You need to design and implement a lightweight, production-quality web application using:

- Python
- Streamlit
- Jira REST API
- Ollama
- Local/private LLM inference
- Clean modular Python architecture

The purpose of the application is to allow a QA professional to enter a Jira User Story ID, retrieve the corresponding Jira story, understand the requirements, and generate comprehensive test cases using an Ollama-hosted local LLM.

The application must be lightweight, easy to run on a desktop, easy to configure, and suitable for use within an enterprise QA environment.

---

# I -> INSTRUCTIONS

## 1. Application Structure

Create a Streamlit application with exactly two primary screens:

### Screen 1 — Main / Test Case Generator

The main screen should have a ChatGPT-like conversational interface.

The user should be able to:

1. Enter a Jira User Story ID, for example:

   `PROJ-1234`

2. Enter a natural-language request such as:

   `Design test cases for this user story`

   or:

   `Create comprehensive functional and negative test cases`

3. Submit the request.

4. The application should:

   - Validate the Jira ID.
   - Connect to Jira using the configured credentials.
   - Fetch the Jira User Story.
   - Retrieve relevant story information such as:
     - Summary
     - Description
     - Acceptance Criteria, when available
     - Issue type
     - Priority
     - Status
     - Labels
     - Components
     - Other useful available fields
   - Present the retrieved Jira story information in the UI.
   - Send the relevant Jira story information together with the user's request to Ollama.
   - Generate high-quality test cases.
   - Display the generated test cases in the chat-style interface.

The interface should feel similar to a lightweight ChatGPT application rather than a traditional form-based application.

---

## 2. Chat Interface

The main page should provide:

- Application title/header.
- Chat history.
- User message area.
- Assistant response area.
- Jira User Story ID input.
- Chat prompt/input box.
- Submit/send capability.
- Clear conversation capability.
- Loading/progress indication while Jira and Ollama are being contacted.
- Clear error messages when an operation fails.

Use Streamlit's native chat components such as:

- `st.chat_message`
- `st.chat_input`

where appropriate.

Do not build an unnecessarily complicated frontend framework.

The application must remain lightweight.

---

## 3. Settings Screen

Create a dedicated Settings screen.

The Settings screen must allow the user to configure:

### Jira Configuration

- Jira URL
- Jira Email ID
- Jira API Key

### Ollama Configuration

- Ollama URL

Optionally allow configuration of:

- Ollama model name

The settings page should provide:

- Input validation.
- Password/API-key masking where appropriate.
- Save Settings functionality.
- Clear/Reset Settings functionality.
- Connection/Test buttons where appropriate.

The application should not require the user to hard-code credentials into Python source code.

---

## 4. Jira Integration

Implement Jira integration using Jira's REST API.

The Jira client should be isolated into its own reusable Python module/class.

The Jira client must:

- Build the correct Jira REST API request.
- Authenticate using the configured Jira email and API key.
- Fetch the requested Jira issue.
- Handle HTTP errors.
- Handle authentication failures.
- Handle invalid Jira IDs.
- Handle Jira connectivity failures.
- Handle missing fields gracefully.
- Handle timeout conditions.

Do not expose the Jira API key in the UI output, logs, exceptions, or generated responses.

Use appropriate request timeouts.

Do not use insecure hard-coded credentials.

---

## 5. Ollama Integration

Implement Ollama integration as a separate reusable Python module/class.

The application must communicate with the configured Ollama URL through its API.

The Ollama client should:

- Accept the configured Ollama URL.
- Accept the configured model.
- Construct an appropriate prompt.
- Send the Jira story information and user's request to Ollama.
- Receive the generated response.
- Display the response in the Streamlit chat interface.

Handle:

- Ollama unavailable.
- Invalid Ollama URL.
- Model unavailable.
- Connection timeout.
- API errors.
- Empty responses.
- Unexpected response formats.

Do not expose sensitive configuration values in generated output.

---

## 6. Test Case Generation

The generated test cases should be QA-professional quality.

The LLM should analyze the Jira User Story rather than blindly generating generic test cases.

Test-case generation should consider, when applicable:

- Functional scenarios
- Positive scenarios
- Negative scenarios
- Boundary-value scenarios
- Validation scenarios
- Error-handling scenarios
- Business-rule scenarios
- Field-level validation
- Mandatory/optional fields
- Integration scenarios
- Permission/access scenarios
- Data-related scenarios
- Regression scenarios
- Acceptance-criteria coverage
- Edge cases

Each test case should preferably contain:

- Test Case ID
- Test Case Title
- Objective
- Preconditions
- Test Data
- Test Steps
- Expected Result
- Priority
- Type/Category

The generated test cases must be traceable to the Jira story and acceptance criteria wherever possible.

Do not invent requirements that are clearly unsupported by the Jira story.

If information is missing from the Jira story, explicitly identify assumptions or gaps rather than silently inventing business rules.

---

## 7. Prompt Engineering

Create a dedicated prompt-building module.

Do not place the complete LLM prompt directly inside the Streamlit UI code.

The prompt builder should receive:

- Jira story data
- Acceptance criteria
- User request
- Relevant configuration

and construct a structured prompt for Ollama.

The prompt must instruct the LLM to behave as an experienced QA test engineer.

The generated output should be structured and easy to read in the Streamlit UI.

Prefer Markdown tables or well-structured Markdown for displaying test cases.

---

## 8. Application Architecture

Follow a clean modular structure.

Do not put the entire application into one Python file.

Use an architecture similar to:

```text
jira_test_case_generator/
│
├── app.py
├── config/
│   └── settings.py
│
├── services/
│   ├── jira_client.py
│   ├── ollama_client.py
│   └── prompt_builder.py
│
├── ui/
│   ├── main_page.py
│   └── settings_page.py
│
├── models/
│   └── data_models.py
│
├── utils/
│   ├── validators.py
│   └── error_handler.py
│
├── requirements.txt
└── README.md
```

You may improve this structure if there is a strong technical reason, but do not introduce unnecessary complexity.

---

## 9. Configuration and Security

Never hard-code:

- Jira URL
- Jira email
- Jira API key
- Ollama URL
- Ollama model

The application should maintain configuration separately from business logic.

Use Streamlit secrets or an appropriate local configuration mechanism where suitable.

API keys must never be displayed in plain text after entry.

Do not write credentials to application logs.

Do not include credentials in exception messages.

---

## 10. Error Handling

Implement robust exception handling throughout the application.

Handle errors at the appropriate layer rather than using one giant try/except block around the entire application.

Provide user-friendly messages for:

- Invalid Jira credentials
- Invalid Jira issue ID
- Jira issue not found
- Jira server unavailable
- Jira API failure
- Ollama unavailable
- Ollama model unavailable
- Invalid configuration
- Network timeout
- Unexpected API response
- Empty Jira description
- Empty LLM response

Technical details may be logged appropriately, but sensitive credentials must never appear in logs.

---

## 11. UI/UX Requirements

The application should be:

- Lightweight
- Clean
- Professional
- Responsive
- Easy to understand
- Minimalistic

Do not over-engineer the UI.

Use Streamlit's native components wherever possible.

The main screen should resemble a simple ChatGPT-style interface.

The Settings screen should resemble a clean configuration panel.

Clearly distinguish:

- User messages
- Jira information
- AI-generated responses
- Errors/warnings

Use expanders where useful for displaying the complete Jira story without overwhelming the main chat interface.

---

## 12. State Management

Use Streamlit session state appropriately.

Maintain:

- Chat history
- Current Jira issue
- Generated test cases
- Current settings/configuration as appropriate

Avoid unnecessary database requirements.

This is intended to be a lightweight desktop/local application.

---

## 13. Performance

The application should avoid unnecessary Jira and Ollama calls.

Do not fetch the same Jira issue repeatedly when it is already available in the current session unless the user explicitly requests a refresh.

Use reasonable API timeouts.

Keep the UI responsive by showing progress/loading indicators during:

- Jira retrieval
- Ollama generation

---

## 14. Validation

Validate:

### Jira ID

Example acceptable format:

`PROJ-1234`

Do not assume that every Jira project uses exactly the same project-key length, but validate that the input resembles a valid Jira issue key.

### Jira URL

Validate that it is a properly formed HTTP/HTTPS URL.

### Email

Validate that it resembles a valid email address.

### API Key

Ensure it is not empty.

### Ollama URL

Validate that it is a properly formed HTTP/HTTPS URL.

---

## 15. Code Quality

Follow production-quality Python standards.

Use:

- Type hints
- Clear function/class names
- Modular design
- Reusable components
- Appropriate exception classes
- Proper resource handling
- Reasonable logging
- Configuration separation

Avoid:

- Global mutable state where unnecessary
- Duplicate code
- Hard-coded credentials
- Hard-coded URLs
- Excessive dependencies
- Unnecessary frameworks
- Thread.sleep-like artificial delays
- Dead code
- Placeholder implementations

Keep the implementation simple enough for a QA engineer to maintain.

---

# C -> CONTEXT

The application will be used by a QA professional who wants to quickly convert Jira User Stories into detailed test cases.

The expected workflow is:

```text
User
  ↓
Open Streamlit application
  ↓
Configure Jira + Ollama in Settings
  ↓
Go to Main screen
  ↓
Enter Jira ID
  ↓
Ask:
"Design the test cases"
  ↓
Application retrieves Jira User Story
  ↓
Application sends story + request to Ollama
  ↓
Ollama analyzes requirements
  ↓
Ollama generates test cases
  ↓
Streamlit displays test cases
```

The key objective is to create a lightweight local QA assistant that combines Jira requirements with a locally hosted Ollama model.

The application should prioritize privacy by allowing the LLM inference to remain local through Ollama.

The user should not need to manually copy and paste the Jira User Story into the LLM.

The Jira story should be fetched automatically after the user provides the Jira ID.

---

# E -> EXAMPLE

## Example User Interaction

User enters:

```text
Jira ID:
ABC-1234
```

Then enters:

```text
Design comprehensive test cases for this user story.
Include positive, negative, boundary, validation, and edge-case scenarios.
```

The application retrieves the Jira story.

Example Jira content:

```text
Summary:
User should be able to reset their password.

Description:
As a registered user,
I want to reset my password,
so that I can regain access to my account.

Acceptance Criteria:
1. User can request a password reset using their registered email.
2. User receives a password reset email.
3. Reset link should expire after the configured period.
4. User should be able to create a new password.
5. Invalid reset links should be rejected.
```

The application sends the relevant information to Ollama.

The generated response should be structured approximately like:

| Test Case ID | Test Case | Type | Priority |
|---|---|---|---|
| TC-001 | Reset password using valid registered email | Positive | High |
| TC-002 | Reset password using unregistered email | Negative | High |
| TC-003 | Use expired password reset link | Negative | High |
| TC-004 | Use invalid reset link | Negative | High |
| TC-005 | Create password meeting all requirements | Positive | High |
| TC-006 | Create password violating password policy | Negative | Medium |

Then provide detailed steps and expected results for each test case.

The exact test cases must always be derived from the actual Jira story retrieved at runtime.

---

# P -> PARAMETERS

Build the application using the following parameters and assumptions:

- Language: Python 3.x
- UI Framework: Streamlit
- Requirements source: Jira
- Jira authentication: Email + API Key
- LLM runtime: Ollama
- LLM location: Local/private environment
- Jira connection: REST API
- Ollama connection: REST API
- Application type: Lightweight local web application
- Primary users: QA engineers/testers
- Primary purpose: Jira User Story → AI-generated test cases

The application must allow the user to configure the Jira and Ollama endpoints rather than embedding environment-specific values.

The application should be designed so that another Ollama model can be selected later without redesigning the application.

The application should also make it straightforward to replace or extend the Jira client in the future.

Prioritize:

1. Correctness
2. Security
3. Maintainability
4. Simplicity
5. Good UX
6. Performance

Do not introduce unnecessary enterprise infrastructure such as databases, Docker, Kubernetes, authentication servers, or external AI services unless explicitly requested.

---

# O -> OUTPUT

Provide a complete runnable Streamlit application.

The output must contain:

1. Complete project structure.
2. `app.py`
3. Jira client implementation.
4. Ollama client implementation.
5. Prompt-builder implementation.
6. Settings implementation.
7. Main chat UI implementation.
8. Required data models.
9. Validation utilities.
10. Error-handling implementation.
11. `requirements.txt`
12. `README.md`
13. Any additional files required to run the application.

The generated application must be runnable locally using a command equivalent to:

```bash
streamlit run app.py
```

The application must not contain fake API responses or placeholder Jira/Ollama implementations.

Use real Jira REST API integration and real Ollama API integration.

Provide complete runnable code rather than pseudocode.

Ensure imports, file paths, classes, functions, and configuration references are internally consistent.

Do not leave TODO implementations.

Do not omit required files.

---

# T -> TONE

Technical, precise, production-quality, lightweight, modular, security-conscious, QA-focused, and enterprise-ready.

Follow the RICEPOT methodology strictly:

**R → Role**  
**I → Instructions**  
**C → Context**  
**E → Example**  
**P → Parameters**  
**O → Output**  
**T → Tone**

Prioritize practical implementation over unnecessary complexity.

The final application should feel like a lightweight internal QA assistant: simple enough to run on a normal desktop, but structured well enough to be extended into a larger enterprise QA tool later.
