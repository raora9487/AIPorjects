# Taste
- Expects generated deliverables (e.g., test plans) to be saved into a project-level `output` folder. Confidence: 0.7
- Likes test-plan deliverables to also come as a PowerPoint review deck (summary of scope, gaps, scenarios, entry/exit criteria, review gate) saved alongside the source doc. Confidence: 0.5
- Prefers tasks to be executed by following the custom skills (SKILL.md files) they provide earlier, including the workflow/gates defined in them, rather than improvising. Confidence: 0.6
- Prefers the agent to proceed autonomously and make reasonable assumptions rather than asking many clarifying questions before acting ("don't ask me everything, just do whatever is needed"). Confidence: 0.8
- Uses locally hosted Ollama models for LLM inference (via its local HTTP API) instead of cloud LLM APIs, with Jira Cloud as the issue data source. Confidence: 0.5
- Keeps credentials/configuration in a `.env` file rather than hard-coded in source, and expects configuration to be discovered/loaded from it. Provides credentials in `.env` KEY=VALUE form and is fine with the agent storing them in the git-ignored local `.env` for reference. Confidence: 0.6
- Delegates git commits and pushes to GitHub to the agent rather than doing them manually, expecting the same remote/branch conventions and workflow as previous sessions ("push my code to github as last time"). Confidence: 0.7
- Works on a Windows machine, so shell commands should target Windows (use PowerShell rather than bash heredocs, which cmd/PowerShell do not support). Confidence: 0.6
- Commits and pushes directly to the `main` branch rather than using feature branches or pull requests. Confidence: 0.5
- Insists credentials never be hardcoded anywhere (workflow JSON, source code, AI prompts, logs, Git repos) and that they be stored in the platform's secret manager (e.g., n8n Cloud credential manager) instead. Confidence: 0.8
- Wants new functionality woven into the existing project artifacts (workflow JSON, README, test docs) rather than added as separate/disconnected pieces. Confidence: 0.6
- Expects test documentation that covers failure and edge cases explicitly — partial success, retries, missing/corrupt input, size limits, permission errors — tied back to the stated requirements. Confidence: 0.7
- Demands honest status reporting: never present overall success unless every required step is confirmed, and report partial success distinctly with enough detail (IDs/URLs) to recover. Confidence: 0.7
- Wants human-approval gates before irreversible external actions (e.g., creating Jira issues). Confidence: 0.6
- Expects exact node/API settings to be verified against current official documentation and the installed tool version before the implementation is written. Confidence: 0.5

- Expects exact node/API settings to be verified against current official documentation and the installed tool version before the implementation is written. Confidence: 0.5
