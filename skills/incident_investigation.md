# Skill: Investigate Repeated Application Errors

## When to use this skill

Use when an application has sustained HTTP 500 or 503 errors, increased
latency, or repeated timeout alerts.

## Evidence to gather

1. Error rate and start time.
2. Logs for the failing path.
3. Recent deployment or configuration changes.
4. Traffic, replica, CPU, memory, and dependency health.
5. Database query latency if the application uses a database.

## Investigation method

1. Describe the symptom precisely.
2. Write two or three possible causes.
3. Gather evidence that could support or contradict each cause.
4. Prefer live evidence over a past incident.
5. If evidence conflicts, escalate rather than choosing a convenient cause.
6. Select only an approved recommendation.
7. After a platform-executed action, check whether the symptom improved.

## Safety boundaries

- Never execute a command or change directly.
- Never recommend an action outside the approved action catalogue.
- Hand database-engine, network-fabric, and identity causes to their owning
  domain.
- A completed action is not a resolved incident until verification passes.

## Good outcome

A structured summary with: symptom, evidence used, likely cause and confidence,
recommendation or escalation, and verification result.
