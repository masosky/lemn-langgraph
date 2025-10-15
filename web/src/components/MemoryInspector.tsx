import React from 'react';

import type { DocumentEntry, MemoryEntry } from '../api';

interface MemoryInspectorProps {
  memories: MemoryEntry[];
  documents: DocumentEntry[];
  loading: boolean;
  highlightedKeys: string[];
  onRefresh: () => Promise<void> | void;
}

export function MemoryInspector({ memories, documents, loading, highlightedKeys, onRefresh }: MemoryInspectorProps) {
  const highlightedSet = React.useMemo(() => new Set(highlightedKeys), [highlightedKeys]);

  return (
    <aside className="memory-inspector">
      <header className="memory-header">
        <div>
          <h3>Memory Inspector</h3>
          <p className="memory-subline">Recent context captured for this agent & channel</p>
        </div>
        <button className="ghost" onClick={onRefresh} disabled={loading}>
          {loading ? 'Refreshing…' : 'Refresh'}
        </button>
      </header>

      <section className="memory-section">
        <h4>Memories</h4>
        {memories.length === 0 && <p className="empty-copy">No memories yet. Start chatting to build context.</p>}
        <ul>
          {memories.map((memory) => {
            const key = `${memory.kind}-${memory.created_at}-${memory.content}`;
            const highlighted = highlightedSet.has(key);
            return (
              <li key={key} className={highlighted ? 'highlighted' : undefined}>
                <div className="memory-meta">
                  <strong>{memory.kind}</strong>
                  <span>{new Date(memory.created_at).toLocaleString()}</span>
                </div>
                <p>{memory.content}</p>
              </li>
            );
          })}
        </ul>
      </section>

      <section className="memory-section">
        <h4>Reference Documents</h4>
        {documents.length === 0 && <p className="empty-copy">No related documents found.</p>}
        <ul>
          {documents.map((doc) => (
            <li key={`${doc.title}-${doc.created_at}`}>
              <div className="memory-meta">
                <strong>{doc.title}</strong>
                <span>{new Date(doc.created_at).toLocaleString()}</span>
              </div>
              <p className="doc-tags">Tags: {doc.tags || '—'}</p>
              <p>{doc.snippet}</p>
            </li>
          ))}
        </ul>
      </section>
    </aside>
  );
}
