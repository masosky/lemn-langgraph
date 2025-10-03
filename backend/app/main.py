"""FastAPI application entrypoint."""
from __future__ import annotations

import logging

from fastapi import FastAPI

from .config import get_settings
from .routes import chat, dashboard, health, memory, seed, slack, ui

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Agents as a Service Showcase")


@app.on_event("startup")
def startup() -> None:
    settings = get_settings()
    logging.info("Starting app with LLM provider: %s", settings.llm_provider)


app.include_router(health.router)
app.include_router(chat.router)
app.include_router(dashboard.router)
app.include_router(slack.router)
app.include_router(seed.router)
app.include_router(memory.router)
app.include_router(ui.router)
