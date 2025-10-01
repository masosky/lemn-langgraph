export interface ChatRequest {
  agent: string;
  text: string;
  channel_id?: string;
  user_id?: string;
}

export interface ChatResponse {
  reply: string;
  tool_runs: { tool: string; result: Record<string, unknown> }[];
  citations: { title: string; score: number }[];
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
  return response.json();
}

export async function fetchMemory(agent: string, channel: string) {
  const response = await fetch(`/memory/${agent}/${channel}`);
  if (!response.ok) {
    throw new Error('Failed to fetch memory');
  }
  return response.json();
}
