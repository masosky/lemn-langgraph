export type JsonValue = string | number | boolean | null | JsonValue[] | { [key: string]: JsonValue };

export interface ChatRequest {
  agent: string;
  text: string;
  channel_id?: string;
  user_id?: string;
}

export interface ToolRunPayload {
  tool: string;
  result: JsonValue;
}

export interface CitationPayload {
  title: string;
  score: number;
}

export interface ChatResponse {
  reply: string;
  tool_runs: ToolRunPayload[];
  citations: CitationPayload[];
}

export interface MemoryEntry {
  kind: string;
  content: string;
  created_at: string;
}

export interface DocumentEntry {
  title: string;
  tags: string;
  snippet: string;
  created_at: string;
}

export interface MemoryResponse {
  agent: string;
  channel: string;
  user: string | null;
  memories: MemoryEntry[];
  documents: DocumentEntry[];
}

export interface AgentStat {
  id: string;
  title: string;
  description: string;
  messages: number;
  conversations: number;
  tool_runs: number;
  last_interaction: string | null;
}

export interface OverviewResponse {
  total_messages: number;
  total_memories: number;
  active_agents: number;
  agent_stats: AgentStat[];
}

export interface AgentRun {
  id: number;
  created_at: string;
  channel: string | null;
  user: string | null;
  user_text: string;
  reply: string;
  tool_runs: ToolRunPayload[];
  citations: CitationPayload[];
}

export interface RunsResponse {
  agent: string;
  runs: AgentRun[];
}

export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!response.ok) {
    throw new Error('Failed to chat with agent');
  }
  return response.json() as Promise<ChatResponse>;
}

export async function fetchMemory(agent: string, channel: string): Promise<MemoryResponse> {
  const response = await fetch(`/memory/${agent}/${channel}`);
  if (!response.ok) {
    throw new Error('Failed to fetch memory');
  }
  return response.json() as Promise<MemoryResponse>;
}

export async function fetchOverview(): Promise<OverviewResponse> {
  const response = await fetch('/api/overview');
  if (!response.ok) {
    throw new Error('Failed to fetch overview');
  }
  return response.json() as Promise<OverviewResponse>;
}

export async function fetchRuns(agent: string, limit = 5): Promise<RunsResponse> {
  const url = new URL(`/api/runs/${agent}`, window.location.origin);
  url.searchParams.set('limit', String(limit));
  const response = await fetch(url.toString());
  if (!response.ok) {
    throw new Error('Failed to fetch runs');
  }
  return response.json() as Promise<RunsResponse>;
}
