# Taste
- Expects generated deliverables (e.g., test plans) to be saved into a project-level `output` folder. Confidence: 0.7
- Likes test-plan deliverables to also come as a PowerPoint review deck (summary of scope, gaps, scenarios, entry/exit criteria, review gate) saved alongside the source doc. Confidence: 0.5
- Prefers tasks to be executed by following the custom skills (SKILL.md files) they provide earlier, including the workflow/gates defined in them, rather than improvising. Confidence: 0.6
- Prefers the agent to proceed autonomously and make reasonable assumptions rather than asking many clarifying questions before acting ("don't ask me everything, just do whatever is needed"). Confidence: 0.8
- Uses locally hosted Ollama models for LLM inference (via its local HTTP API) instead of cloud LLM APIs, with Jira Cloud as the issue data source. Confidence: 0.5
- Keeps credentials/configuration in a `.env` file rather than hard-coded in source, and expects configuration to be discovered/loaded from it. Confidence: 0.5
