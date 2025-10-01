# Agents as a Service Showcase

This monorepo demonstrates four LangGraph-inspired agents running as a service with a FastAPI backend and React frontend. The demo is designed to run locally without external API keys.

## Project Structure

```
agents-as-a-service-showcase/
  backend/    # FastAPI application and agent orchestration
  web/        # Vite + React dashboard
  docker/     # docker-compose configuration
```

## Quickstart

1. Copy environment variables:
   ```bash
   cp docker/env.example .env
   ```
   Install [uv](https://github.com/astral-sh/uv) if you want a fast local Python
   workflow outside of Docker.
2. Optionally prepare a local backend environment using [uv](https://github.com/astral-sh/uv):
   ```bash
   cd backend
   uv sync
   cp settings.example.toml settings.toml  # optional overrides
   cd ..
   ```

3. Launch the stack:
   ```bash
   cd docker
   docker compose --env-file ../.env up --build
   ```
4. Seed demo data:
   ```bash
   curl -X POST http://localhost:8000/seed
   ```
5. Open the web dashboard at http://localhost:5173 and explore the agents.

## API Examples

Chat with the support agent:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"agent": "support", "channel_id": "web", "user_id": "cli-user", "text": "Help María with her ticket"}'
```

Slack event payload example:

```json
{
  "type": "event_callback",
  "event": {
    "type": "app_mention",
    "user": "U123",
    "text": "@support help with ticket",
    "channel": "C123"
  }
}
```

## Testing

Backend unit tests can be executed with:

```bash
cd backend
uv run pytest
```
