import React from 'react';

import type { AgentStat } from '../api';

interface AgentCardProps {
  agent: { id: string; title: string; description: string };
  stats?: AgentStat;
  onOpen: () => void;
  active: boolean;
}

export function AgentCard({ agent, stats, onOpen, active }: AgentCardProps) {
  const subtitle = stats?.last_interaction
    ? `Last activity ${new Date(stats.last_interaction).toLocaleString()}`
    : 'No activity yet';

  return (
    <article className={`agent-card ${active ? 'active' : ''}`}>
      <header>
        <h2>{agent.title}</h2>
        <p className="agent-subtitle">{subtitle}</p>
      </header>
      <p>{agent.description}</p>
      {stats && (
        <dl className="agent-metrics">
          <div>
            <dt>Messages</dt>
            <dd>{stats.messages}</dd>
          </div>
          <div>
            <dt>Conversations</dt>
            <dd>{stats.conversations}</dd>
          </div>
          <div>
            <dt>Tool Runs</dt>
            <dd>{stats.tool_runs}</dd>
          </div>
        </dl>
      )}
      <button onClick={onOpen}>Open Chat</button>
    </article>
  );
}
