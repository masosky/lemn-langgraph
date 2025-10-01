import React, { useEffect, useState } from 'react';
import { fetchMemory, sendMessage } from '../api';
import { MemoryInspector } from './MemoryInspector';

interface ChatEntry {
  role: 'user' | 'agent';
  text: string;
}

interface ChatWindowProps {
  agentId: string;
}

export function ChatWindow({ agentId }: ChatWindowProps) {
  const [channelId] = useState(`web-${agentId}`);
  const [messages, setMessages] = useState<ChatEntry[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [memories, setMemories] = useState<any[]>([]);

  useEffect(() => {
    refreshMemory();
  }, [agentId]);

  async function refreshMemory() {
    try {
      const data = await fetchMemory(agentId, channelId);
      setMemories(data.memories ?? []);
    } catch (error) {
      console.warn(error);
    }
  }

  async function handleSend(event: React.FormEvent) {
    event.preventDefault();
    if (!input.trim()) return;
    const userText = input;
    setMessages((prev) => [...prev, { role: 'user', text: userText }]);
    setInput('');
    setLoading(true);
    try {
      const response = await sendMessage({ agent: agentId, text: userText, channel_id: channelId, user_id: 'web-user' });
      setMessages((prev) => [...prev, { role: 'agent', text: response.reply }]);
      await refreshMemory();
    } catch (error) {
      setMessages((prev) => [...prev, { role: 'agent', text: 'Failed to reach agent.' }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="chat-window">
      <div className="conversation">
        <header>
          <h2>{agentId} chat</h2>
        </header>
        <div className="messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <strong>{message.role === 'user' ? 'You' : 'Agent'}</strong>
              <p>{message.text}</p>
            </div>
          ))}
        </div>
        <form onSubmit={handleSend} className="composer">
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Type a message"
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Sending…' : 'Send'}
          </button>
        </form>
      </div>
      <MemoryInspector memories={memories} />
    </section>
  );
}
