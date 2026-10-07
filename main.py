import uuid

from fastapi import FastAPI
from pydantic import BaseModel

from langgraph.types import Command
from agent.graph import agent
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Support / Ops AI Assistant",
    description="LangGraph ReAct support and operations assistant",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None
    human_response: str | None = None


def extract_text(content):
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))
            elif isinstance(item, str):
                text_parts.append(item)

        return "\n".join(text_parts)

    return str(content)


@app.get("/")
def root():
    return {
        "name": "Support / Ops AI Assistant",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/docs", include_in_schema=False, response_class=HTMLResponse)
def custom_docs():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Support / Ops AI Assistant</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: Inter, Arial, sans-serif;
                background: #f7f7f8;
                color: #202123;
            }

            .container {
                max-width: 1000px;
                margin: 0 auto;
                padding: 50px 25px;
            }

            .header {
                margin-bottom: 35px;
            }

            .badge {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 20px;
                background: #e8f5e9;
                color: #2e7d32;
                font-size: 13px;
                font-weight: 600;
                margin-bottom: 15px;
            }

            h1 {
                font-size: 34px;
                margin: 0 0 10px;
            }

            .subtitle {
                color: #666;
                font-size: 16px;
                line-height: 1.6;
            }

            .card {
                background: white;
                border: 1px solid #e5e5e5;
                border-radius: 14px;
                padding: 25px;
                margin-bottom: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            }

            .endpoint {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 12px;
            }

            .method {
                font-size: 12px;
                font-weight: 700;
                padding: 5px 9px;
                border-radius: 6px;
                background: #eef2ff;
                color: #4338ca;
            }

            code {
                font-family: Consolas, monospace;
                font-size: 14px;
            }

            .description {
                color: #666;
                margin-bottom: 20px;
            }

            textarea {
                width: 100%;
                min-height: 130px;
                resize: vertical;
                border: 1px solid #d8d8d8;
                border-radius: 9px;
                padding: 14px;
                font-family: Consolas, monospace;
                font-size: 14px;
                outline: none;
            }

            textarea:focus {
                border-color: #777;
            }

            button {
                margin-top: 12px;
                border: none;
                border-radius: 8px;
                padding: 11px 18px;
                background: #202123;
                color: white;
                font-size: 14px;
                cursor: pointer;
            }

            button:hover {
                background: #000;
            }

            pre {
                background: #f5f5f5;
                border-radius: 9px;
                padding: 15px;
                overflow-x: auto;
                white-space: pre-wrap;
                margin-top: 18px;
            }

            .footer {
                color: #888;
                font-size: 13px;
                margin-top: 30px;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <div class="header">
                <div class="badge">● API Online</div>

                <h1>Support / Ops AI Assistant</h1>

                <div class="subtitle">
                    Internal support and operations assistant powered by
                    LangGraph, RAG, web search, human-in-the-loop approval,
                    and safe ticket updates.
                </div>
            </div>

            <div class="card">

                <div class="endpoint">
                    <span class="method">POST</span>
                    <code>/chat</code>
                </div>

                <div class="description">
                    Send a message to the Support / Ops AI Assistant.
                </div>

                <textarea id="message">What are the allowed statuses for a support ticket?</textarea>

                <button onclick="sendMessage()">
                    Send message
                </button>

                <pre id="response">Response will appear here...</pre>

            </div>

            <div class="card">

                <div class="endpoint">
                    <span class="method">GET</span>
                    <code>/health</code>
                </div>

                <div class="description">
                    Check whether the API is running.
                </div>

                <button onclick="checkHealth()">
                    Check health
                </button>

                <pre id="health">Not checked yet.</pre>

            </div>

            <div class="footer">
                Support / Ops AI Assistant · LangGraph + FastAPI
            </div>

        </div>

        <script>

            async function sendMessage() {

                const message =
                    document.getElementById("message").value;

                const output =
                    document.getElementById("response");

                output.textContent = "Thinking...";

                try {

                    const response = await fetch("/chat", {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            message: message
                        })
                    });

                    const data = await response.json();

                    output.textContent =
                        JSON.stringify(data, null, 2);

                } catch (error) {

                    output.textContent =
                        "Error: " + error.message;

                }
            }


            async function checkHealth() {

                const output =
                    document.getElementById("health");

                try {

                    const response =
                        await fetch("/health");

                    const data =
                        await response.json();

                    output.textContent =
                        JSON.stringify(data, null, 2);

                } catch (error) {

                    output.textContent =
                        "Error: " + error.message;

                }
            }

        </script>

    </body>
    </html>
    """

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    thread_id = request.thread_id or str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:

        # Normal user message
        if request.human_response is None:

            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": request.message
                        }
                    ]
                },
                config=config
            )

        # Resume after human-in-the-loop interruption
        else:

            result = agent.invoke(
                Command(resume=request.human_response),
                config=config
            )

        # Check whether the agent needs human input
        if "__interrupt__" in result and result["__interrupt__"]:

            interrupt_data = result["__interrupt__"][0].value

            return {
                "status": "needs_human_input",
                "thread_id": thread_id,
                "interrupt": interrupt_data,
            }

        final_message = result["messages"][-1]

        return {
            "status": "success",
            "thread_id": thread_id,
            "response": extract_text(final_message.content),
        }

    except Exception as e:

        return {
            "status": "error",
            "thread_id": thread_id,
            "error": type(e).__name__,
            "message": str(e),
        }