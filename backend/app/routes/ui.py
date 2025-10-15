"""Simple HTML playground for chatting with agents."""
from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def index() -> str:
    """Serve a minimal in-browser chat playground."""

    return """
    <!DOCTYPE html>
    <html lang=\"en\">
      <head>
        <meta charset=\"utf-8\" />
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
        <title>Agents Showcase Playground</title>
        <style>
          :root {
            color-scheme: light dark;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif;
          }
          body {
            margin: 0 auto;
            padding: 2rem 1.5rem 4rem;
            max-width: 720px;
            line-height: 1.6;
          }
          h1 {
            text-align: center;
            margin-bottom: 1rem;
          }
          .panel {
            border: 1px solid rgba(0, 0, 0, 0.15);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(6px);
          }
          label {
            display: block;
            font-weight: 600;
            margin-top: 1rem;
            margin-bottom: 0.25rem;
          }
          select,
          textarea,
          button {
            width: 100%;
            font-size: 1rem;
            padding: 0.65rem 0.75rem;
            border-radius: 8px;
            border: 1px solid rgba(0, 0, 0, 0.2);
          }
          textarea {
            min-height: 120px;
            resize: vertical;
          }
          button {
            margin-top: 1rem;
            background: #2563eb;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s ease;
          }
          button:hover {
            background: #1e40af;
          }
          button:disabled {
            opacity: 0.6;
            cursor: wait;
          }
          pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            background: rgba(15, 23, 42, 0.85);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1.5rem;
          }
          .meta {
            font-size: 0.9rem;
            color: rgba(60, 60, 67, 0.75);
            text-align: center;
            margin-bottom: 1.5rem;
          }
        </style>
      </head>
      <body>
        <h1>Agents as a Service Playground</h1>
        <p class=\"meta\">Pick an agent, send a prompt, and inspect the structured response.</p>
        <section class=\"panel\">
          <label for=\"agent\">Agent</label>
          <select id=\"agent\">
            <option value=\"accountant\">Accountant</option>
            <option value=\"support\">Support</option>
            <option value=\"copywriter\">Copywriter</option>
            <option value=\"marketing\">Marketing Analyst</option>
          </select>
          <label for=\"message\">Message</label>
          <textarea id=\"message\" placeholder=\"Ask the agent for help...\"></textarea>
          <button id=\"send\">Send Message</button>
          <pre id=\"output\" hidden></pre>
        </section>
        <script>
          const sendButton = document.getElementById('send');
          const outputEl = document.getElementById('output');
          const agentSelect = document.getElementById('agent');
          const messageInput = document.getElementById('message');

          async function sendMessage() {
            const agent = agentSelect.value;
            const text = messageInput.value.trim();

            if (!text) {
              alert('Enter a message to send.');
              return;
            }

            sendButton.disabled = true;
            outputEl.hidden = false;
            outputEl.textContent = 'Sending...';

            try {
              const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ agent, text })
              });

              if (!response.ok) {
                throw new Error('Request failed with status ' + response.status);
              }

              const payload = await response.json();
              outputEl.textContent = JSON.stringify(payload, null, 2);
            } catch (error) {
              outputEl.textContent = 'Error: ' + error.message;
            } finally {
              sendButton.disabled = false;
            }
          }

          sendButton.addEventListener('click', sendMessage);
          messageInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' && (event.metaKey || event.ctrlKey)) {
              event.preventDefault();
              sendMessage();
            }
          });
        </script>
      </body>
    </html>
    """

