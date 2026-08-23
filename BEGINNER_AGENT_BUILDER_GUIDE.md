# Beginner Guide: Building a Domain Agent

This guide is for infrastructure engineers and SMEs who are building an agent
pack for the first time. You do not need to become a Python or AI expert first.

Your job is to provide the operational knowledge:

- what incident the agent investigates,
- what evidence a good engineer would gather,
- which outcome is safe,
- when the agent must stop and escalate.

The framework and platform provide shared technical safety controls.

> Simple rule: the agent thinks; the platform acts.

## 1. Skills, knowledge, and memory

| Item | Simple meaning | Owner |
| --- | --- | --- |
| Agent pack | A domain-specific operational runbook with an AI reasoning loop | Domain SME and engineer |
| Platform | Shared tools, identity, policy, approval, execution and audit | Platform team |
| Skill | Reusable instructions for a repeatable job | Domain SME |
| Knowledge Markdown | Human-maintained reference material | Service owner |
| Runtime memory | Verified experience from completed investigations | Platform after approval |

Markdown is not automatically runtime memory.

- A skill is like a concise runbook.
- A knowledge file is like a service support document.
- Memory is an approved record from a completed, verified run.

Never allow a past memory to approve a current action. Live evidence wins.

## 2. Before you start

Answer these questions before opening a code editor.

| Question | Example |
| --- | --- |
| One job | Investigate repeated HTTP 503 errors. |
| Owner | Application Reliability team. |
| In scope | Application errors and deployment correlation. |
| Out of scope | Database engine tuning and network fabric. |
| Evidence | Logs, metrics, traces, deployment history, dependency health. |
| Outcomes | Rollback, scale workload, or escalation. |
| Never allowed | Direct command execution, approval bypass, invented tools. |
| Proof of value | Evidence is correct, recommendation is safe, result is verified. |

Start with one service and one or two incident patterns. Do not start with
"solve every production incident."

## 3. Folder map

### Files an SME can edit

| File | What you write | Infra analogy |
| --- | --- | --- |
| agent.yaml | Scope, ownership, capability names, limits, delegation | Service definition and access request |
| prompts/investigation.md | Investigation order and stop conditions | Incident runbook |
| rules/domain_rules.py or rules/domain_rules.yaml | Durable always/never safety rules | Operational policy |
| actions/catalogue.yaml | Approved action names and risks | Remediation catalogue |
| scenarios/golden.yaml | Sample incidents and evidence | Incident replay data |
| evaluations/expected.yaml | Correct result for each scenario | Acceptance criteria |
| skills/*.md | Reusable task instructions | Mini runbook |
| knowledge/*.md | Service facts and dependency notes | Team wiki page |

### Files to leave unchanged at first

| Item | Reason |
| --- | --- |
| workflow/ | This is the LangGraph workflow engine. |
| contracts/ | Shared message formats between agent and platform. |
| tools/ | Protected wrappers around approved platform capabilities. |
| mock_platform.py | Local simulator for learning and tests. |
| tests/ | Tests protect safety boundaries. Do not delete a failing test. |
| pyproject.toml | Dependency list. |

If a new domain seems to require changes to workflow or contracts, raise a
platform-contract discussion instead of casually forking the framework.

## 4. Write agent.yaml

The agent declaration says what the agent is allowed to ask for. It does not
contain tool code.

Fill it in this order:

1. Name and goal. Give one measurable job.
2. Scope. List environments and signals it may investigate.
3. Ownership. State what it owns and what it delegates.
4. Read capabilities. Add only platform-registered names.
5. Action capabilities. Add only previously approved action names.
6. Budgets and confidence. Add limits so it cannot think or call tools forever.

Example:

    name: payments-reliability-agent
    goal: Investigate sustained HTTP 503 errors on payments-api and recommend the safest approved next step.

A capability name is like a service-catalogue request. It is not a Splunk query,
an API URL, an MCP call, or a Python function.

Never add passwords, tokens, endpoints, SPL, PromQL, SQL, shell commands,
Terraform, Ansible, or Python to agent.yaml.

## 5. Write the investigation runbook

The prompt file is instructions for the reasoning model. Treat it like the
runbook you would give a good on-call engineer.

Use this pattern:

1. Confirm the symptom, affected service and start time.
2. List two or three possible causes.
3. Gather evidence that supports or contradicts each cause.
4. Prefer live evidence over a previous incident.
5. If evidence conflicts, escalate.
6. Select only an approved action.
7. Verify whether symptoms improved after a platform-executed action.

Do not write every possible failure mode. Write the method for investigation.

## 6. Write rules

A rule is a deterministic safety statement that stays true after an alert fires.

Good rules:

- Never restart a stateful service without failover evidence.
- If evidence conflicts, escalate rather than recommend remediation.
- If a cause belongs to database infrastructure, delegate to the database team.

Bad rules:

- Alert when CPU is above 80%.
- Alert when error rate exceeds 5%.

Those are monitoring thresholds. Keep them in monitoring, not in the agent
pack.

## 7. Write the action catalogue

The action catalogue is the agent's approved menu. The agent may choose from
this menu; it must never invent a new item.

For every action write:

| Field | Example |
| --- | --- |
| Name | application.rollback_deployment |
| Risk | Medium |
| Use when | Errors began after a release and evidence supports a regression |
| Approval | Required |
| Do not use when | Evidence conflicts or cause is out of scope |

Always include incident.escalate. Escalation is a safe, useful outcome.

## 8. Add skills and knowledge documents

Use skills for reusable work methods:

    skills/
      incident_investigation.md
      deployment_regression_analysis.md

Each skill should say:

1. When to use it.
2. Evidence to collect.
3. Investigation steps.
4. Safety boundaries.
5. What good output looks like.

Use knowledge Markdown for stable human-maintained facts:

    knowledge/
      service_overview.md
      dependency_map.md
      error_code_reference.md

Do not put secrets, customer data, unapproved production details, or changing
incident evidence in these files.

In the existing advanced pack, copied skills and knowledge folders are
human-readable documentation only. Put essential instructions in
prompts/investigation.md until a platform-controlled knowledge loader is added.

## 9. Create golden scenarios

Golden scenarios are known incidents the agent must handle correctly. They are
the agent equivalent of a change test plan.

Create at least five:

1. Clear application regression after a deployment.
2. Database or network cause that must be delegated.
3. Safe recommendation case.
4. Conflicting evidence that blocks remediation.
5. Missing evidence that creates an improvement recommendation.

For each scenario define: trigger, evidence, expected diagnosis or uncertainty,
expected recommendation or escalation, and whether verification is required.

## 10. Change code safely

For every change:

1. Change one thing only.
2. Record why the change is needed.
3. Run the local simulation.
4. Run tests.
5. Review output as the SME.
6. Commit only when expected scenarios still pass.

Commands for the advanced pack:

    pip install -e ".[dev]"
    python mock_platform.py
    pytest

Commands for the starter pack:

    python run_demo.py
    pytest

If a test fails, do not delete it. Check whether you changed allowed
capabilities, removed a safety rule, recommended an unapproved action, or need
to justify an updated scenario expectation.

## 11. Prompt for an AI coding assistant

Copy this when you need help:

    I am a beginner infrastructure engineer modifying a governed domain-agent pack.

    My business outcome is: [one sentence].
    My domain is: [domain].
    I may change only agent.yaml, prompts/investigation.md, rules,
    actions/catalogue.yaml, scenarios/golden.yaml, evaluations/expected.yaml,
    skills/*.md and knowledge/*.md.

    Do not modify workflow/, contracts/, platform interfaces, or tests unless
    you first explain why a platform-contract change is required.
    Do not add credentials, direct production APIs, shell commands, SPL,
    PromQL, SQL, Ansible, Terraform, or automatic execution.

    First ask me for missing domain facts. Then propose the smallest change,
    explain every file change, and give exact tests to run.

## 12. Final definition of success

Your first agent is ready for a controlled pilot when:

- It has one bounded job and named owner.
- It requests only declared, approved capabilities.
- It handles golden scenarios correctly.
- It escalates when evidence conflicts or is insufficient.
- It does not execute production actions directly.
- The mock run and automated tests pass.
- A human SME can explain why every recommendation is safe.

It is not ready merely because it produces a plausible answer.

> A good agent knows what evidence it needs, stays inside its authority, and
> escalates safely when it does not know.
