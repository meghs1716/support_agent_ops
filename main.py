import uuid

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from langgraph.types import Command
from agent.graph import agent


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
        parts = []

        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
            elif isinstance(item, str):
                parts.append(item)

        return "\n".join(parts)

    return str(content)


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url=/docs">
    </head>
    <body>
        <p>Opening Support / Ops AI Assistant...</p>
    </body>
    </html>
    """


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat")
def chat(request: ChatRequest):

    thread_id = request.thread_id or str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:

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

        else:

            result = agent.invoke(
                Command(resume=request.human_response),
                config=config
            )

        if "__interrupt__" in result and result["__interrupt__"]:

            interrupt_data = result["__interrupt__"][0].value

            return {
                "status": "needs_human_input",
                "thread_id": thread_id,
                "interrupt": interrupt_data
            }

        final_message = result["messages"][-1]

        return {
            "status": "success",
            "thread_id": thread_id,
            "response": extract_text(final_message.content)
        }

    except Exception as e:

        return {
            "status": "error",
            "thread_id": thread_id,
            "error": type(e).__name__,
            "message": str(e)
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
    background: #f5f5f7;
    color: #18181b;
}

.container {
    max-width: 900px;
    margin: auto;
    padding: 45px 20px;
}

.header {
    margin-bottom: 28px;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: #e8f7ed;
    color: #207a3c;
    padding: 7px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
}

.dot {
    width: 7px;
    height: 7px;
    background: #2eaf55;
    border-radius: 50%;
}

h1 {
    font-size: 36px;
    margin: 17px 0 8px;
    letter-spacing: -1px;
}

.subtitle {
    color: #71717a;
    line-height: 1.6;
    max-width: 700px;
}

.card {
    background: white;
    border: 1px solid #e4e4e7;
    border-radius: 16px;
    padding: 24px;
    margin-top: 20px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.04);
}

label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 9px;
}

textarea {
    width: 100%;
    min-height: 130px;
    resize: vertical;
    padding: 14px;
    border: 1px solid #d4d4d8;
    border-radius: 10px;
    font-family: inherit;
    font-size: 15px;
    outline: none;
}

textarea:focus {
    border-color: #18181b;
}

button {
    margin-top: 13px;
    padding: 11px 18px;
    border: none;
    border-radius: 9px;
    background: #18181b;
    color: white;
    font-weight: 600;
    cursor: pointer;
}

button:hover {
    background: #333338;
}

button:disabled {
    opacity: .6;
    cursor: not-allowed;
}

.response {
    margin-top: 20px;
    background: #fafafa;
    border: 1px solid #e4e4e7;
    border-radius: 10px;
    padding: 17px;
    min-height: 70px;
    white-space: pre-wrap;
    line-height: 1.6;
    color: #3f3f46;
}

.human-box {
    display: none;
    margin-top: 20px;
    padding: 18px;
    border-radius: 10px;
    background: #fff8e7;
    border: 1px solid #f0d98c;
}

.human-title {
    font-weight: 700;
    margin-bottom: 8px;
}

.status {
    color: #71717a;
    font-size: 13px;
    margin-top: 12px;
}

.footer {
    text-align: center;
    color: #a1a1aa;
    font-size: 13px;
    margin-top: 30px;
}

</style>

</head>

<body>

<div class="container">

    <div class="header">

        <div class="badge">
            <span class="dot"></span>
            API Online
        </div>

        <h1>Support / Ops AI Assistant</h1>

        <div class="subtitle">
            An internal AI assistant for support and operations.
            It combines RAG, web search, human approval and controlled
            ticket updates through a LangGraph agent.
        </div>

    </div>


    <div class="card">

        <label>Ask the assistant</label>

        <textarea id="message"
        placeholder="Example: What are the allowed statuses for a support ticket?"></textarea>

        <button id="sendButton" onclick="sendMessage()">
            Send message
        </button>

        <div id="response" class="response">
            Your response will appear here.
        </div>

        <div id="humanBox" class="human-box">

            <div class="human-title">
                Human input required
            </div>

            <div id="humanQuestion"></div>

            <textarea
                id="humanResponse"
                placeholder="Enter your response..."
            ></textarea>

            <button onclick="resumeAgent()">
                Continue
            </button>

        </div>

        <div id="status" class="status"></div>

    </div>


    <div class="card">

        <strong>System</strong>

        <p class="subtitle">
            LangGraph · FastAPI · Groq · RAG · Tavily · SQLite
        </p>

    </div>


    <div class="footer">
        Support / Ops AI Assistant · Portfolio Project
    </div>

</div>


<script>

let currentThreadId = null;


async function sendMessage() {

    const message = document.getElementById("message").value.trim();

    if (!message) {
        return;
    }

    const responseBox = document.getElementById("response");
    const status = document.getElementById("status");
    const button = document.getElementById("sendButton");

    button.disabled = true;

    responseBox.textContent = "Thinking...";
    status.textContent = "";

    document.getElementById("humanBox").style.display = "none";

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

        currentThreadId = data.thread_id;

        handleResponse(data);

    } catch (error) {

        responseBox.textContent =
            "Connection error: " + error.message;

    }

    button.disabled = false;
}


function handleResponse(data) {

    const responseBox = document.getElementById("response");
    const status = document.getElementById("status");

    if (data.status === "success") {

        responseBox.textContent = data.response;

        status.textContent = "Completed";

    }

    else if (data.status === "needs_human_input") {

        let question = data.interrupt;

        if (typeof question === "object") {
            question = question.question || JSON.stringify(question);
        }

        document.getElementById("humanQuestion").textContent = question;

        document.getElementById("humanBox").style.display = "block";

        responseBox.textContent =
            "The assistant needs your input before continuing.";

        status.textContent = "Waiting for human input";

    }

    else {

        responseBox.textContent =
            data.message || "Something went wrong.";

        status.textContent = "Error";

    }
}


async function resumeAgent() {

    const humanResponse =
        document.getElementById("humanResponse").value.trim();

    if (!humanResponse || !currentThreadId) {
        return;
    }

    const responseBox = document.getElementById("response");
    const status = document.getElementById("status");

    responseBox.textContent = "Continuing...";
    status.textContent = "";

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                message: "",

                thread_id: currentThreadId,

                human_response: humanResponse

            })

        });

        const data = await response.json();

        handleResponse(data);

    } catch (error) {

        responseBox.textContent =
            "Connection error: " + error.message;

    }
}

</script>

</body>
</html>
"""