import json
from pathlib import Path
from datetime import datetime


TRACE_DIR = Path(__file__).resolve().parent / "traces"

TRACE_DIR.mkdir(exist_ok=True)


def log_trace(
    question,
    tool_calls,
    final_answer,
    status="completed"
):
    """
    Save one agent execution as a JSON trace.
    """

    trace = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "tool_calls": tool_calls,
        "final_answer": final_answer,
        "status": status
    }

    filename = (
        datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        + ".json"
    )

    filepath = TRACE_DIR / filename

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
            trace,
            file,
            indent=4,
            ensure_ascii=False
        )

    return filepath