import React, { useState } from 'react';
import { AgentCard } from './components/AgentCard';
import { ChatWindow } from './components/ChatWindow';
import './styles.css';

const agents = [
  {
    id: 'accountant',
    title: 'Accountant Agent',
    description: 'Reconciles invoices and shares finance summaries.',
  },
  {
    id: 'support',
    title: 'Support Agent',
    description: 'Summarises issues and drafts empathic replies.',
  },
  {
    id: 'copywriter',
    title: 'Copywriter Agent',
    description: 'Produces marketing copy and A/B test ideas.',
  },
  {
    id: 'marketing',
    title: 'Marketing Analyst Agent',
    description: 'Analyses campaign performance and recommendations.',
  },
];

export default function App() {
  const [selectedAgent, setSelectedAgent] = useState<string | null>(agents[0].id);

  return (
    <div className="app">
      <header>
        <h1>Agents as a Service Showcase</h1>
        <p>Chat with specialised LangGraph agents with persistent memory.</p>
      </header>
      <main>
        <section className="agents-grid">
          {agents.map((agent) => (
            <AgentCard
              key={agent.id}
              agent={agent}
              onOpen={() => setSelectedAgent(agent.id)}
              active={selectedAgent === agent.id}
            />
          ))}
        </section>
        {selectedAgent && <ChatWindow agentId={selectedAgent} />}
      </main>
    </div>
  );
}
