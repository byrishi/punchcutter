# Security

Report security issues privately through GitHub: Security, then "Report a vulnerability". Please do not open a public issue.

The HTTP MCP server (`punchcutter mcp --http`) has no authentication. Run it behind a private address or tunnel, and do not expose a long-running public instance without adding auth in front of it.
