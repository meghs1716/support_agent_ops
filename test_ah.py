from tools.update_support_tickets import init_database
import sqlite3


DB_PATH = "support.db"


# Create database and sample ticket
init_database()


print("\nChecking database...\n")

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute(
    "SELECT ticket_id, status, note FROM tickets"
)

tickets = cursor.fetchall()

for ticket in tickets:
    print("Ticket ID:", ticket[0])
    print("Status:", ticket[1])
    print("Note:", ticket[2])
    print("---")

connection.close()