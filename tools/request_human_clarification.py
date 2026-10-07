from langchain_core.tools import tool
from langgraph.types import interrupt


@tool
def ask_human(question: str) -> str:
    """
    Request input from a human when the agent cannot safely proceed because required information is missing, the user's request is ambiguous, or a decision or confirmation is needed.

The tool pauses execution and returns the human's response to the agent.

Use it when the missing information cannot be reliably inferred. For example, the user requests a refund but does not identify the relevant transaction, or asks to change a ticket without specifying the intended status.

    """

    response = interrupt(
        {
            "type": "human_clarification",
            "question": question
        }
    )

    return f"Human provided clarification: {response}"