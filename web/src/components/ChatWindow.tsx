import React, { useEffect, useMemo, useRef, useState, type ChangeEvent, type FormEvent } from 'react';
import {
  fetchMemory,
  sendMessage,
  type ChatResponse,
  type MemoryEntry,
  type DocumentEntry,
  type ToolRunPayload,
  type CitationPayload,
} from '../api';
import { MemoryInspector } from './MemoryInspector';

type ChatRole = 'user' | 'agent' | 'tool' | 'citation';

interface ChatEntry {
  role: ChatRole;
  text: string;
  meta?: string;
}

interface ChatWindowProps {
  agentId: string;
  presetInput?: string | null;
  onPresetConsumed?: () => void;
  onRunCompleted?: () => Promise<void> | void;
}

export function ChatWindow({ agentId, presetInput, onPresetConsumed, onRunCompleted }: ChatWindowProps) {
  const channelId = useMemo(() => `web-${agentId}`, [agentId]);
  const [messages, setMessages] = useState<ChatEntry[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [memories, setMemories] = useState<MemoryEntry[]>([]);
  const [documents, setDocuments] = useState<DocumentEntry[]>([]);
  const [memoryLoading, setMemoryLoading] = useState(false);
  const [highlightedMemoryKeys, setHighlightedMemoryKeys] = useState<string[]>([]);
  const previousMemoryKeysRef = useRef<Set<string>>(new Set());

  useEffect(() => {
    setMessages([]);
    setInput('');
    previousMemoryKeysRef.current = new Set();
    refreshMemory();
  }, [agentId]);

  useEffect(() => {
    if (presetInput && presetInput.trim().length > 0) {
      setInput(presetInput);
      onPresetConsumed?.();
    }
  }, [presetInput, onPresetConsumed]);

  async function refreshMemory() {
    setMemoryLoading(true);
    try {
      const data = await fetchMemory(agentId, channelId);
      const nextMemoryKeys = new Set<string>();
      const highlights: string[] = [];
      data.memories.forEach((memory) => {
        const key = `${memory.kind}-${memory.created_at}-${memory.content}`;
        nextMemoryKeys.add(key);
        if (!previousMemoryKeysRef.current.has(key)) {
          highlights.push(key);
        }
      });
      previousMemoryKeysRef.current = nextMemoryKeys;
      setHighlightedMemoryKeys(highlights);
      setMemories(data.memories ?? []);
      setDocuments(data.documents ?? []);
    } catch (fetchError) {
      console.warn(fetchError);
    } finally {
      setMemoryLoading(false);
    }
  }

  function appendResponse(response: ChatResponse) {
    const formattedEntries: ChatEntry[] = [
      { role: 'agent', text: response.reply },
      ...response.tool_runs.map((run) => formatToolRun(run)),
      ...formatCitations(response.citations),
    ];
    setMessages((prev: ChatEntry[]) => [...prev, ...formattedEntries]);
  }

  function formatToolRun(run: ToolRunPayload): ChatEntry {
    const formattedResult = typeof run.result === 'string' ? run.result : JSON.stringify(run.result, null, 2);
    return {
      role: 'tool',
      text: formattedResult,
      meta: run.tool,
    };
  }

  function formatCitations(citations: CitationPayload[]): ChatEntry[] {
    if (!citations.length) {
      return [];
    }
    const text = citations
      .map((citation) => `${citation.title} (score ${(citation.score * 100).toFixed(1)}%)`)
      .join('\n');
    return [
      {
        role: 'citation',
        text,
      },
    ];
  }

  async function handleSend(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!input.trim()) return;
    const userText = input;
    setMessages((prev: ChatEntry[]) => [...prev, { role: 'user', text: userText }]);
    setInput('');
    setLoading(true);
    setError(null);
    try {
      const response = await sendMessage({ agent: agentId, text: userText, channel_id: channelId, user_id: 'web-user' });
      appendResponse(response);
      await refreshMemory();
      await onRunCompleted?.();
    } catch (sendError) {
      setError('Failed to reach agent. Please try again.');
      setMessages((prev: ChatEntry[]) => [...prev, { role: 'agent', text: 'Failed to reach agent.' }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="chat-window">
      <div className="conversation">
        <header>
          <h2>{agentId} chat</h2>
          <span className="chat-channel">Channel {channelId}</span>
        </header>
        <div className="messages">
          {messages.map((message: ChatEntry, index: number) => (
            <div key={`${message.role}-${index}`} className={`message ${message.role}`}>
              <div className="message-meta">
                <strong>{labelForRole(message.role)}</strong>
                {message.meta && <span className="message-tag">{message.meta}</span>}
              </div>
              <pre>{message.text}</pre>
            </div>
          ))}
        </div>
        <form onSubmit={handleSend} className="composer">
          <input
            value={input}
            onChange={(event: ChangeEvent<HTMLInputElement>) => setInput(event.target.value)}
            placeholder="Type a message or use a preset prompt"
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Sending…' : 'Send'}
          </button>
        </form>
        {error && <p className="chat-error">{error}</p>}
      </div>
      <MemoryInspector
        memories={memories}
        documents={documents}
        loading={memoryLoading}
        highlightedKeys={highlightedMemoryKeys}
        onRefresh={refreshMemory}
      />
    </section>
  );
}

function labelForRole(role: ChatRole): string {
  switch (role) {
    case 'user':
      return 'You';
    case 'agent':
      return 'Agent';
    case 'tool':
      return 'Tool';
    case 'citation':
      return 'Citations';
    default:
      return role;
  }
}
