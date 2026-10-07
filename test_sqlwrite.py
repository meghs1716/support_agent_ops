from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from typing_extensions import TypedDict

from tools.update_support_tickets import sqlite_write, init_database


class State(TypedDict):
    result: str


def write_node(state: State):
    result = sqlite_write.invoke({
    "ticket_id": "TICK-001",
    "new_status": "RESOLVED",
    "note": "Refund issue resolved after customer confirmation.",
    "operation_id": "resolve-TICK-001-001"
})

    return {
        "result": result
    }


# Make sure database exists
init_database()


# Build small test graph
graph = StateGraph(State)

graph.add_node("write", write_node)

graph.add_edge(START, "write")
graph.add_edge("write", END)

checkpointer = InMemorySaver()

app = graph.compile(
    checkpointer=checkpointer
)


config = {
    "configurable": {
        "thread_id": "sqlite-write-test-1"
    }
}


print("\nStarting database write test...")

# First execution
result = app.invoke(
    {
        "result": ""
    },
    config=config
)


print("\nGraph paused for approval.")

print(result["__interrupt__"])


# Ask for approval
approval = input("\nApprove this database change? (yes/no): ")


# Resume graph
result = app.invoke(
    Command(
        resume=approval
    ),
    config=config
)


print("\nGraph finished.")

print("Result:")
print(result["result"])


# Verify database
import sqlite3

connection = sqlite3.connect("support.db")
cursor = connection.cursor()

cursor.execute(
    """
    SELECT ticket_id, status, note
    FROM tickets
    WHERE ticket_id = ?
    """,
    ("TICK-001",)
)

ticket = cursor.fetchone()

connection.close()


print("\nDatabase after operation:")

if ticket:
    print("Ticket ID:", ticket[0])
    print("Status:", ticket[1])
    print("Note:", ticket[2])
else:
    print("Ticket not found.")