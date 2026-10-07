import sqlite3
from typing import Literal

from langgraph.types import interrupt

import os
import sqlite3

from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.types import interrupt

DB_PATH = "support.db"
load_dotenv()

DB_PATH = os.getenv("SUPPORT_DB_PATH", "support.db")

def init_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            note TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completed_operations (
            operation_id TEXT PRIMARY KEY
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO tickets
        (ticket_id, status, note)
        VALUES (?, ?, ?)
    """, (
        "TICK-001",
        "OPEN",
        "Customer reported a duplicate charge."
    ))

    connection.commit()
    connection.close()


@tool
def sqlite_write(
    ticket_id: str,
    new_status: Literal[
        "OPEN",
        "IN_PROGRESS",
        "RESOLVED",
        "CLOSED"
    ],
    operation_id: str,
    note: str = ""
) -> str:
    """
    Update the status and note of an existing support ticket in the support database.

    Use this tool when the user has explicitly requested a database change and the ticket ID and intended update are sufficiently clear.
    The tool requests human approval before making the change and uses an operation ID to prevent duplicate execution.

    Returns the update result, including the ticket ID, new status, and operation ID, or an explanation of why the update was not completed.

    Do not use this tool to answer questions about ticket policies or to retrieve general policy information;
    use search_internal_knowledge. Do not use it when the requested change is unclear; use request_human_clarification first.
    parameter:Parameters


    """

    if not operation_id:
        return "ERROR: operation_id is required."

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Check whether this operation was already completed
    cursor.execute(
        """
        SELECT operation_id
        FROM completed_operations
        WHERE operation_id = ?
        """,
        (operation_id,)
    )

    if cursor.fetchone():
        connection.close()

        return (
            f"Operation {operation_id} was already completed. "
            "No database change was made."
        )

    connection.close()

    # Ask for human approval
    approval = interrupt({
        "type": "write_approval",
        "message": "The agent wants to modify a support ticket.",
        "ticket_id": ticket_id,
        "new_status": new_status,
        "note": note,
        "operation_id": operation_id
    })

    if str(approval).lower() not in [
        "yes",
        "y",
        "approve",
        "approved"
    ]:
        return "The database update was not approved."

    # Open a new connection for the actual transaction
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        # Check again inside the transaction.
        # This protects against retries/race conditions.
        cursor.execute(
            """
            SELECT operation_id
            FROM completed_operations
            WHERE operation_id = ?
            """,
            (operation_id,)
        )

        if cursor.fetchone():
            connection.rollback()
            return (
                f"Operation {operation_id} was already completed. "
                "No database change was made."
            )

        # Check ticket exists
        cursor.execute(
            """
            SELECT status
            FROM tickets
            WHERE ticket_id = ?
            """,
            (ticket_id,)
        )

        ticket = cursor.fetchone()

        if ticket is None:
            connection.rollback()
            return f"Ticket {ticket_id} does not exist."

        # Perform update
        cursor.execute(
            """
            UPDATE tickets
            SET status = ?, note = ?
            WHERE ticket_id = ?
            """,
            (
                new_status,
                note,
                ticket_id
            )
        )

        # Record operation
        cursor.execute(
            """
            INSERT INTO completed_operations
            (operation_id)
            VALUES (?)
            """,
            (operation_id,)
        )

        connection.commit()

        return (
            f"Ticket {ticket_id} successfully updated. "
            f"New status: {new_status}. "
            f"Operation ID: {operation_id}"
        )

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


init_database()