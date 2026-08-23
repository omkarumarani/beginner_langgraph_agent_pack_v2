# Skills

A skill is a reusable set of instructions for a repeatable job.

For infrastructure teams, a skill is similar to a concise runbook that says:

- when to use it,
- what evidence is required,
- what safety boundaries apply,
- and what a good outcome looks like.

This folder is intentionally Markdown-first so a domain SME can review it.
The starter LangGraph workflow does not automatically load skills yet. When
connected to a governed platform, the platform can select and provide an
approved skill as context to the agent.

Do not put credentials, commands that change production, or confidential data
in a skill file.
