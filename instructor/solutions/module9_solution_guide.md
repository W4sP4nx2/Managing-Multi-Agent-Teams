# Homework C Solution Guide: Deployment & Operations

## Strong Answer Indicators

- Dockerfile avoids embedding secrets.
- Logs include workflow ID, agent ID, action, result, and timestamp.
- Sandbox design blocks network and filesystem by default.
- Version control hash changes when prompt, tools, model, or policy changes.

## Common Mistakes

- Logging raw secrets or restricted payloads.
- Treating a local `exec` call as a production sandbox.
- Versioning prompts but forgetting tool and policy changes.
- Providing deployment steps that require undocumented environment variables.

## Minimum Passing Evidence

- Secure container or deployment design.
- Structured log examples.
- Typed execution result for sandbox success and timeout.
- Config save, diff, and rollback demonstration.
