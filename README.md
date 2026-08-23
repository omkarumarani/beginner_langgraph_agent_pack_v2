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

Do not edit `workflow/graph.py` at first. It is the reusable LangGraph engine.

## Skills, knowledge, and memory are different

- **Skill** = reusable instructions for doing a job. In this pack, the incident
  investigation skill explains the method an agent should follow.
- **Knowledge Markdown** = human-maintained reference material, such as service
  dependencies, error-code meanings, or escalation contacts. It may be given to
  the agent as approved context later.
- **Memory** = verified experience from a completed run. The platform stores it
  only after approval; the agent cannot write or trust memory by itself.

## Run this project (end-to-end)

### 1) Prerequisites

- Python 3.11+ (the pack was validated on Python 3.12)
- Windows PowerShell, macOS Terminal, or Linux shell

### 2) Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### 3) Install dependencies

Preferred (editable install for local development):

```bash
pip install -e ".[dev]"
```

If editable install fails in your environment, use direct installs:

```bash
pip install "langgraph>=0.2" "pyyaml>=6.0" "pytest>=8.0"
```

### 4) Run the starter demo

```bash
python run_demo.py
```

Expected output shape:

```text
Starter Agent Result
observation: ...
hypothesis: ...
diagnosis: ...
confidence: ...
recommendation: ...
verified: ...
```

### 5) Run tests

```bash
pytest -q
```

### 6) Typical development loop

1. Edit YAML/Markdown files listed above.
2. Run `python run_demo.py`.
3. Run `pytest -q`.
4. Review output with your SME criteria before committing.

## Python modules used in this pack

### Direct dependencies (declared in `pyproject.toml`)

- `langgraph>=0.2`: workflow graph and state orchestration
- `pyyaml>=6.0`: read YAML scenario and configuration files

### Dev/test dependency

- `pytest>=8.0`: automated tests in `tests/test_agent.py`

### Standard library modules used by this repository

- `pathlib` for path-safe file reading
- `typing` for type hints in test code

Tip: to verify exactly what is installed in your active environment, run:

```bash
python -m pip list
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

## v3 roadmap: introducing a real AI API safely

When you move from this training pack to a production-grade v3, add an LLM/API
layer without changing the safety model.

### What to add

1. Model client abstraction
   - Create a small adapter (for example `llm_client.py`) with one interface:
     `generate_investigation_step(input_state) -> structured_output`.
   - Keep provider-specific code (OpenAI, Azure OpenAI, Anthropic, etc.) only
     inside the adapter.
2. Structured outputs and schema validation
   - Require JSON outputs and validate fields such as `hypothesis`,
     `confidence`, and `recommended_action` before using them.
3. Prompt and policy separation
   - Keep domain instructions in `prompts/` and non-negotiable controls in
     `rules/`.
   - Treat rules as hard gates even if model output disagrees.
4. Capability-gated evidence retrieval
   - Model requests evidence by capability name only.
   - Platform layer performs authz, approval, execution, and auditing.
5. Reliability controls
   - Add timeout, retry, fallback model, and deterministic error handling.
6. Observability and evaluation
   - Log request IDs, latency, token usage, confidence distributions,
     recommendation outcomes, and escalation rates.
   - Add regression scenarios for hallucination resistance and policy
     compliance.

### What stays the same

- The graph sequence (`observe -> hypothesize -> gather evidence -> reason -> recommend -> verify`).
- Human approval and escalation pathways.
- No direct production command execution by the agent.

### Suggested v3 deliverables

1. `llm_client.py` with provider-agnostic interface.
2. `config/model.yaml` for model, temperature, and timeout.
3. Additional tests for invalid/unsafe model outputs.
4. Evaluation set with expected safe behavior under ambiguous evidence.
5. Runbook for incident responders explaining fallback and escalation behavior.
