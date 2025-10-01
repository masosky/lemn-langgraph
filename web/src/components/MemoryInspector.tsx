import React from 'react';

interface MemoryInspectorProps {
  memories: { kind: string; content: string; created_at: string }[];
}

export function MemoryInspector({ memories }: MemoryInspectorProps) {
  return (
    <aside className="memory-inspector">
      <h3>Memory Inspector</h3>
      {memories.length === 0 && <p>No memories yet.</p>}
      <ul>
        {memories.map((memory, index) => (
          <li key={index}>
            <strong>{memory.kind}</strong>
            <span>{new Date(memory.created_at).toLocaleString()}</span>
            <p>{memory.content}</p>
          </li>
        ))}
      </ul>
    </aside>
  );
}
