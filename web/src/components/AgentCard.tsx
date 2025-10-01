import React from 'react';

interface AgentCardProps {
  agent: { id: string; title: string; description: string };
  onOpen: () => void;
  active: boolean;
}

export function AgentCard({ agent, onOpen, active }: AgentCardProps) {
  return (
    <article className={`agent-card ${active ? 'active' : ''}`}>
      <h2>{agent.title}</h2>
      <p>{agent.description}</p>
      <button onClick={onOpen}>Open Chat</button>
    </article>
  );
}
