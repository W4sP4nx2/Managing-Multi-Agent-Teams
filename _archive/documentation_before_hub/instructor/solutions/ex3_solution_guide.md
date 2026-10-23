# Ex3 Solution Guide: RAG & MCP Architecture

## Expected Architecture

- Separate memory domains for requirements, codebase, and operational data.
- MCP servers for GitHub, Jira, local file system, or database access.
- Policy gateway before every MCP call.
- Agents receive least-privilege tool scopes.

## Strong Answer Indicators

- Code RAG uses structure-aware chunking by function/class/file.
- Requirements RAG uses ticket and acceptance-criteria chunking.
- Tool matrix explicitly denies dangerous tools to non-authorized agents.
- Threat matrix includes prompt injection and malicious tool descriptions.

## Common Mistakes

- Treating MCP as a security layer by itself.
- Giving the Coder database write access.
- No retrieval provenance.
- No policy for sensitive documents.
