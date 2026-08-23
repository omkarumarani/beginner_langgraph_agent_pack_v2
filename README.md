# Beginner LangGraph Agent Pack

This is a deliberately small learning pack for infrastructure SMEs building
their first agent. It uses LangGraph, but you only need to edit YAML and
Markdown files for the first version.

## The idea

Think of the pack as a safe incident runbook:

1. Receive a symptom.
2. Create a possible cause (hypothesis).
3. Collect evidence.
4. Decide whether evidence supports the cause.
5. Recommend an approved action or escalate.
6. Verify whether the symptom improved.

The agent never executes a production command. It only returns a recommendation.

## Files beginners should edit

| File | What you change |
| --- | --- |
| `agent.yaml` | Agent name, scope, allowed evidence, confidence threshold |
| `prompts/investigation.md` | Your domain investigation runbook |
| `rules/domain_rules.yaml` | “Always / never” safety rules |
| `actions/catalogue.yaml` | Actions the agent may recommend |
| `scenarios/golden.yaml` | Sample incidents and their evidence |
| `skills/incident_investigation.md` | A reusable, human-readable investigation skill |
| `knowledge/application_reliability_basics.md` | Domain knowledge the team can maintain in Markdown |

Do not edit `engine/graph.py` at first. It is the reusable LangGraph engine.

## Skills, knowledge, and memory are different

- **Skill** = reusable instructions for doing a job. In this pack, the incident
  investigation skill explains the method an agent should follow.
- **Knowledge Markdown** = human-maintained reference material, such as service
  dependencies, error-code meanings, or escalation contacts. It may be given to
  the agent as approved context later.
- **Memory** = verified experience from a completed run. The platform stores it
  only after approval; the agent cannot write or trust memory by itself.

## Start locally

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
python run_demo.py
pytest
```

## What LangGraph means here

LangGraph is simply the workflow controller. It connects small steps in a
reliable order:

```
observe → hypothesize → gather evidence → reason → recommend → verify
```

It is like an incident workflow engine: each stage receives the current
investigation state, adds its result, then hands it to the next stage.

## When you are ready for a real platform

Replace the sample evidence in `scenarios/golden.yaml` with results returned
by approved platform capabilities. Keep the interface: the agent asks for a
named capability; the platform fulfils it and enforces credentials, policy,
approval, execution, and audit.

Never add credentials, production API clients, shell commands, Splunk queries,
or Ansible in this pack.
