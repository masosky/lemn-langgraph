import React, { useState } from 'react';
import { AgentCard } from './components/AgentCard';
import { ChatWindow } from './components/ChatWindow';
import { SystemOverview } from './components/SystemOverview';
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

type ActiveView = 'chat' | 'overview';

export default function App() {
  const [selectedAgent, setSelectedAgent] = useState<string | null>(agents[0].id);
  const [activeView, setActiveView] = useState<ActiveView>('chat');

  return (
    <div className="app">
      <header>
        <h1>Agents as a Service Showcase</h1>
        <p>Chat with specialised LangGraph agents with persistent memory.</p>
        <nav className="view-toggle">
          <button
            type="button"
            className={activeView === 'chat' ? 'active' : ''}
            onClick={() => setActiveView('chat')}
          >
            Conversation
          </button>
          <button
            type="button"
            className={activeView === 'overview' ? 'active' : ''}
            onClick={() => setActiveView('overview')}
          >
            System Overview
          </button>
        </nav>
      </header>
      <main>
        {activeView === 'chat' ? (
          <>
            <section className="agents-grid">
              {agents.map((agent) => (
                <AgentCard
                  key={agent.id}
                  agent={agent}
                  onOpen={() => setSelectedAgent(agent.id)}
                  active={selectedAgent === agent.id}
                />
              ))}
              <article className="agent-card overview-card">
                <header>
                  <h2>System Overview</h2>
                  <p className="agent-subtitle">Understand the end-to-end request flow.</p>
                </header>
                <p>
                  Explore how chat messages travel through the frontend, backend, agent graphs, memory
                  stores, and the configured LLM provider.
                </p>
                <button
                  type="button"
                  onClick={() => {
                    setActiveView('overview');
                    setSelectedAgent(null);
                  }}
                >
                  View Overview
                </button>
              </article>
            </section>
            {selectedAgent && <ChatWindow agentId={selectedAgent} />}
          </>
        ) : (
          <SystemOverview />
        )}
      </main>
    </div>
  );
}
