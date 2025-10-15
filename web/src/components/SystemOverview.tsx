import React, { useEffect } from 'react';

import mermaid from 'mermaid';

const diagram = `graph TD
    User[End User] -->|sends message| WebUI[Web UI]
    WebUI -->|fetch /api/chat| Backend[FastAPI Backend]
    Backend -->|lookup| Agents[Agent Registry]
    Agents --> Graph[Agent Graph]
    Graph -->|recent context| MemoryDB[Postgres + Qdrant]
    Graph -->|LLM prompt| LLM[LLM Provider]
    LLM --> Graph
    Graph -->|reply + tool runs| Backend
    Backend -->|persist run| MemoryDB
    Backend -->|JSON response| WebUI
    WebUI -->|render conversation| User`;

export function SystemOverview() {
  useEffect(() => {
    mermaid.initialize({ startOnLoad: false, theme: 'neutral' });
    void mermaid.run({ querySelector: '.system-overview__diagram .mermaid' });
  }, []);

  return (
    <div className="system-overview">
      <header className="system-overview__header">
        <h1>How the System Works</h1>
        <p>
          Follow the path of a chat request as it flows through the LangGraph showcase—covering the UI,
          FastAPI backend, agent orchestration, memories, and the configured LLM provider.
        </p>
      </header>
      <section className="system-overview__section">
        <h2>High-Level Flow</h2>
        <p>
          A single request fan-outs from the frontend to the backend, fans into the agent graph and
          supporting services, and returns a composed reply along with tool traces and citations.
        </p>
        <div className="system-overview__diagram">
          <pre className="mermaid">{diagram}</pre>
        </div>
      </section>
      <section className="system-overview__section">
        <h2>Step-by-Step</h2>
        <ol>
          <li>The user selects an agent and submits a prompt in the web interface.</li>
          <li>The frontend posts the request to the backend&apos;s `/api/chat` endpoint.</li>
          <li>
            The backend resolves the agent, hydrates its graph, and loads recent memories plus related
            documents.
          </li>
          <li>The graph optionally triggers domain-specific tools, composes the final prompt, and calls the LLM.</li>
          <li>Replies, tool traces, and citations are persisted before returning the response to the client.</li>
          <li>The UI refreshes the conversation stream and memory inspector with the latest data snapshot.</li>
        </ol>
      </section>
      <section className="system-overview__section">
        <h2>Key Components</h2>
        <ul>
          <li><strong>Frontend</strong>: React + Vite interface managing chat, agents, and memory insights.</li>
          <li><strong>Backend</strong>: FastAPI app exposing `/api` routes for chat orchestration and analytics.</li>
          <li><strong>Agent Graphs</strong>: LangGraph-inspired flows combining memory lookups, tools, and LLM calls.</li>
          <li><strong>Memory Stores</strong>: Postgres for structured history and Qdrant for semantic search.</li>
          <li><strong>LLM Provider</strong>: Pluggable client (OpenAI by default) responsible for agent replies.</li>
        </ul>
      </section>
    </div>
  );
}
