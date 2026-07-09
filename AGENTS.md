# Mcp Trilium

## Operational Memory

Read this repo's `MEMORY.md` at the start of project work. Also read `/Users/paul/Projects/MEMORY.md` when the task touches fleet-level conventions, dispatch, MCP setup, automation, or cross-project behavior.

Private context is not operational memory. Chat history is not operational memory. Tool-specific auto-memory is not shared operational memory. If future agents need a durable fact to work in this repo, write it to `MEMORY.md`.

Before final response, issue close, or handoff, ask: "Did I learn anything durable that future agents need?" If yes, append or update `MEMORY.md` first.

Do not store secrets, API keys, raw `.env` values, transient progress, issue status dumps, test output dumps, speculation, or facts easily derivable from current code.
