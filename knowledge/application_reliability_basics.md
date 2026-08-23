# Application Reliability Knowledge

This is a starter knowledge document for humans. Replace the placeholders with
approved, non-sensitive information about your own service.

## Service profile

- Service name: REPLACE_ME
- Owner: REPLACE_ME
- Supported environments: REPLACE_ME
- Main user journey: REPLACE_ME

## Dependencies

| Dependency | Why it matters | Owning team | Escalate when |
| --- | --- | --- | --- |
| Database | Stores application data | Database team | Query latency, pool saturation, engine errors |
| Downstream API | Provides a required service | Application team | Timeout or dependency error budget breach |
| Network / DNS | Carries traffic | Network team | Connectivity or name-resolution evidence |

## Error interpretation

| Symptom | Possible meaning | First evidence to collect |
| --- | --- | --- |
| HTTP 500 after deployment | Application regression | Deployment time and stack trace |
| HTTP 503 with slow database | Connection-pool or query pressure | Query latency and pool use |
| HTTP 504 | Downstream timeout | Trace breakdown and dependency health |

## Important note about memory

This Markdown document is **knowledge**, not agent memory. It may be updated by
an approved human. Runtime memory should contain only verified, approved
experience from completed investigations and is owned by the platform.
