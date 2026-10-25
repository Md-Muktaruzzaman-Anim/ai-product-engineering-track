import json
from datetime import date
from pathlib import Path


DATA_FILE = Path("tickets.json")

VALID_STATUSES = ("open", "in_progress", "resolved", "closed")
VALID_PRIORITIES = ("low", "medium", "high")


def load_tickets(file_path=DATA_FILE):
    """Load tickets from JSON. Return an empty list if the file is missing."""
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{path} does not contain valid JSON."
        ) from exc

    if not isinstance(tickets, list):
        raise ValueError(
            f"{path} must contain a JSON list of tickets."
        )

    if any(not isinstance(ticket, dict) for ticket in tickets):
        raise ValueError(
            f"Every item in {path} must be a JSON object."
        )

    return tickets


def save_tickets(tickets, file_path=DATA_FILE):
    """Save all tickets to a JSON file."""
    path = Path(file_path)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            tickets,
            file,
            indent=4,
            ensure_ascii=False,
        )


def get_next_ticket_id(tickets):
    """Return one greater than the largest existing ticket ID."""
    existing_ids = [ticket["ticket_id"] for ticket in tickets]
    return max(existing_ids, default=0) + 1


def create_ticket(
    tickets,
    customer_name,
    email,
    subject,
    description,
):
    """Create a new ticket dictionary."""
    customer_name = customer_name.strip()
    email = email.strip()
    subject = subject.strip()
    description = description.strip()

    if not all((customer_name, email, subject, description)):
        raise ValueError(
            "Customer name, email, subject, and description are required."
        )

    return {
        "ticket_id": get_next_ticket_id(tickets),
        "customer_name": customer_name,
        "email": email,
        "subject": subject,
        "description": description,
        "status": "open",
        "priority": "medium",
        "created_at": date.today().isoformat(),
    }


def find_ticket(tickets, ticket_id):
    """Return a ticket by ID, or None if it does not exist."""
    for ticket in tickets:
        if ticket.get("ticket_id") == ticket_id:
            return ticket

    return None


def update_ticket_status(tickets, ticket_id, new_status):
    """Update a ticket's status. Return False if its ID is not found."""
    if new_status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status. Use: {', '.join(VALID_STATUSES)}"
        )

    ticket = find_ticket(tickets, ticket_id)

    if ticket is None:
        return False

    ticket["status"] = new_status
    return True


def filter_tickets(tickets, filter_by, value):
    """Filter tickets by status or priority."""
    if filter_by not in ("status", "priority"):
        raise ValueError(
            "You can filter only by 'status' or 'priority'."
        )

    valid_values = (
        VALID_STATUSES
        if filter_by == "status"
        else VALID_PRIORITIES
    )

    if value not in valid_values:
        raise ValueError(
            f"Invalid {filter_by}. Use: {', '.join(valid_values)}"
        )

    return [
        ticket
        for ticket in tickets
        if ticket.get(filter_by) == value
    ]


def delete_ticket(tickets, ticket_id):
    """Delete a ticket by ID. Return True if it was deleted."""
    for index, ticket in enumerate(tickets):
        if ticket.get("ticket_id") == ticket_id:
            del tickets[index]
            return True

    return False


def print_ticket(ticket):
    """Print one ticket in a readable format."""
    print(f"Ticket #{ticket['ticket_id']}")
    print(f"Customer: {ticket['customer_name']}")
    print(f"Email: {ticket['email']}")
    print(f"Subject: {ticket['subject']}")
    print(f"Description: {ticket['description']}")
    print(f"Status: {ticket['status']}")
    print(f"Priority: {ticket['priority']}")
    print(f"Created: {ticket['created_at']}")
    print("-" * 40)


def print_tickets(tickets):
    """Print all tickets."""
    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        print_ticket(ticket)

    print(f"Total: {len(tickets)} ticket(s)")


def prompt_ticket_id():
    """Get and validate a ticket ID from user input."""
    raw_value = input("Enter ticket ID: ").strip()

    try:
        ticket_id = int(raw_value)
    except ValueError as exc:
        raise ValueError(
            "Ticket ID must be a whole number."
        ) from exc

    if ticket_id < 1:
        raise ValueError("Ticket ID must be greater than zero.")

    return ticket_id


def create_ticket_from_input(tickets):
    """Collect ticket information, then save the new ticket."""
    new_ticket = create_ticket(
        tickets,
        customer_name=input("Customer name: "),
        email=input("Email: "),
        subject=input("Subject: "),
        description=input("Description: "),
    )

    # Save the updated list before changing the in-memory list.
    updated_tickets = [*tickets, new_ticket]
    save_tickets(updated_tickets)

    tickets[:] = updated_tickets

    print(
        f"Ticket #{new_ticket['ticket_id']} created successfully."
    )


def search_ticket(tickets):
    """Find and display one ticket."""
    ticket_id = prompt_ticket_id()
    ticket = find_ticket(tickets, ticket_id)

    if ticket is None:
        print("Ticket not found.")
    else:
        print_ticket(ticket)


def change_ticket_status(tickets):
    """Change the status of an existing ticket and save it."""
    ticket_id = prompt_ticket_id()
    ticket = find_ticket(tickets, ticket_id)

    if ticket is None:
        print("Ticket not found.")
        return

    print(f"Valid statuses: {', '.join(VALID_STATUSES)}")
    new_status = input("Enter new status: ").strip().lower()

    # Work on copies so a failed save does not change the original list.
    updated_tickets = [item.copy() for item in tickets]

    if not update_ticket_status(
        updated_tickets,
        ticket_id,
        new_status,
    ):
        print("Ticket not found.")
        return

    save_tickets(updated_tickets)
    tickets[:] = updated_tickets

    print(f"Ticket #{ticket_id} status updated successfully.")


def filter_ticket_menu(tickets):
    """Ask which field to filter and display matching tickets."""
    print("Filter by: 1) status  2) priority")
    choice = input("Choose (1 or 2): ").strip()

    if choice == "1":
        filter_by = "status"
        value = input(
            f"Enter status ({', '.join(VALID_STATUSES)}): "
        ).strip().lower()

    elif choice == "2":
        filter_by = "priority"
        value = input(
            f"Enter priority ({', '.join(VALID_PRIORITIES)}): "
        ).strip().lower()

    else:
        print("Invalid choice.")
        return

    matching_tickets = filter_tickets(tickets, filter_by, value)
    print_tickets(matching_tickets)


def delete_ticket_menu(tickets):
    """Delete a ticket and persist the updated list."""
    ticket_id = prompt_ticket_id()

    updated_tickets = [ticket.copy() for ticket in tickets]

    if not delete_ticket(updated_tickets, ticket_id):
        print("Ticket not found.")
        return

    save_tickets(updated_tickets)
    tickets[:] = updated_tickets

    print(f"Ticket #{ticket_id} deleted successfully.")


def main():
    """Run the command-line application."""
    try:
        tickets = load_tickets()
    except (OSError, ValueError) as exc:
        print(f"Could not load tickets: {exc}")
        return

    actions = {
        "1": ("Create ticket", create_ticket_from_input),
        "2": ("List all tickets", print_tickets),
        "3": ("Find ticket by ID", search_ticket),
        "4": ("Update ticket status", change_ticket_status),
        "5": ("Filter tickets", filter_ticket_menu),
        "6": ("Delete ticket", delete_ticket_menu),
    }

    while True:
        print("\n=== Customer Support Ticket Manager ===")

        for number, (label, _) in actions.items():
            print(f"{number}. {label}")

        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        action = actions.get(choice)

        if action is None:
            print("Invalid option. Choose a number from 0 to 6.")
            continue

        try:
            action[1](tickets)
        except (OSError, ValueError) as exc:
            print(f"Could not complete that action: {exc}")


if __name__ == "__main__":
    main()