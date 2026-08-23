# BEGINNER EDIT FILE — Investigation runbook

Use this simple order when investigating repeated HTTP 503 errors:

1. Confirm the error rate and when it started.
2. Check whether a deployment occurred near the start time.
3. Check whether traffic or capacity changed.
4. Check database query latency if the application uses a database.
5. Do not recommend a change if evidence conflicts.
6. Escalate if the likely cause belongs to database, network, or another domain.

Do not treat a past incident as proof. Current evidence must support the finding.
