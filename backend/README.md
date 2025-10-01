# Agents as a Service Showcase – Backend

This FastAPI application powers the demo agents. It exposes chat endpoints, Slack integration, and memory inspection utilities.

## Quickstart

```bash
uv sync
uv run uvicorn app.main:app --reload
```

If you prefer to customise configuration without environment variables, copy
`settings.example.toml` to `settings.toml` and adjust values as needed. Any
environment variables defined in `.env` will still take precedence.

With the server running locally you can open http://localhost:8000/ to try a
lightweight HTML playground that sends requests to `/api/chat` for any agent.

Seed demo data:

```bash
curl -X POST http://localhost:8000/seed
```

Inspect stored context and knowledge snippets:

```bash
curl "http://localhost:8000/memory/support/web-support?user_id=alice&limit=5&documents=3"
```

The memory endpoint now supports filtering by `user_id` and returns the
most relevant tagged documents alongside recent memories, making it easier to
debug what context each agent will see during a chat run.

Run tests:

```bash
uv run pytest
```
