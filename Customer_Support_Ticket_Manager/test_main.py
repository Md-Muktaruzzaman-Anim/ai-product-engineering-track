import json
from datetime import date

import pytest

from main import (
    create_ticket,
    delete_ticket,
    filter_tickets,
    find_ticket,
    get_next_ticket_id,
    load_tickets,
    save_tickets,
    update_ticket_status,
)


def sample_ticket(
    ticket_id=1,
    status="open",
    priority="medium",
):
    """Return a sample ticket for testing."""
    return {
        "ticket_id": ticket_id,
        "customer_name": "John Doe",
        "email": "john@example.com",
        "subject": "Cannot log in",
        "description": "I cannot access my account.",
        "status": status,
        "priority": priority,
        "created_at": "2026-10-25",
    }


def test_load_missing_file_returns_empty_list(tmp_path):
    file_path = tmp_path / "missing.json"

    assert load_tickets(file_path) == []


def test_save_and_load_tickets(tmp_path):
    file_path = tmp_path / "tickets.json"
    tickets = [sample_ticket()]

    save_tickets(tickets, file_path)

    assert load_tickets(file_path) == tickets


def test_load_invalid_json_raises_value_error(tmp_path):
    file_path = tmp_path / "tickets.json"
    file_path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError, match="valid JSON"):
        load_tickets(file_path)


def test_load_rejects_json_object_instead_of_list(tmp_path):
    file_path = tmp_path / "tickets.json"
    file_path.write_text(
        json.dumps({"ticket_id": 1}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="JSON list"):
        load_tickets(file_path)


def test_load_rejects_non_dictionary_items(tmp_path):
    file_path = tmp_path / "tickets.json"
    file_path.write_text(
        json.dumps([sample_ticket(), "not a ticket"]),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="JSON object"):
        load_tickets(file_path)


def test_next_ticket_id_for_empty_list():
    assert get_next_ticket_id([]) == 1


def test_next_ticket_id_uses_largest_existing_id():
    tickets = [
        sample_ticket(ticket_id=1),
        sample_ticket(ticket_id=5),
        sample_ticket(ticket_id=3),
    ]

    assert get_next_ticket_id(tickets) == 6


def test_create_ticket_uses_defaults_and_trims_values():
    tickets = [sample_ticket(ticket_id=1)]

    ticket = create_ticket(
        tickets,
        customer_name=" Alice ",
        email=" alice@example.com ",
        subject=" Billing issue ",
        description=" Charged twice ",
    )

    assert ticket["ticket_id"] == 2
    assert ticket["customer_name"] == "Alice"
    assert ticket["email"] == "alice@example.com"
    assert ticket["subject"] == "Billing issue"
    assert ticket["description"] == "Charged twice"
    assert ticket["status"] == "open"
    assert ticket["priority"] == "medium"
    assert ticket["created_at"] == date.today().isoformat()


def test_create_ticket_rejects_empty_required_fields():
    with pytest.raises(ValueError, match="are required"):
        create_ticket(
            [],
            customer_name=" ",
            email="john@example.com",
            subject="Help",
            description="I need help.",
        )


def test_find_ticket_returns_matching_ticket():
    ticket = sample_ticket(ticket_id=2)
    tickets = [sample_ticket(), ticket]

    assert find_ticket(tickets, 2) is ticket


def test_find_ticket_returns_none_when_missing():
    tickets = [sample_ticket(ticket_id=1)]

    assert find_ticket(tickets, 99) is None


def test_update_ticket_status():
    ticket = sample_ticket(ticket_id=1)
    tickets = [ticket]

    result = update_ticket_status(tickets, 1, "resolved")

    assert result is True
    assert ticket["status"] == "resolved"


def test_update_ticket_rejects_invalid_status():
    tickets = [sample_ticket()]

    with pytest.raises(ValueError, match="Invalid status"):
        update_ticket_status(tickets, 1, "working")


def test_update_missing_ticket_returns_false():
    tickets = [sample_ticket()]

    assert update_ticket_status(tickets, 99, "resolved") is False


def test_filter_tickets_by_status():
    tickets = [
        sample_ticket(ticket_id=1, status="open"),
        sample_ticket(ticket_id=2, status="resolved"),
        sample_ticket(ticket_id=3, status="open"),
    ]

    results = filter_tickets(tickets, "status", "open")

    assert [ticket["ticket_id"] for ticket in results] == [1, 3]


def test_filter_tickets_by_priority():
    tickets = [
        sample_ticket(ticket_id=1, priority="low"),
        sample_ticket(ticket_id=2, priority="high"),
        sample_ticket(ticket_id=3, priority="high"),
    ]

    results = filter_tickets(tickets, "priority", "high")

    assert [ticket["ticket_id"] for ticket in results] == [2, 3]


def test_filter_rejects_invalid_field():
    with pytest.raises(ValueError, match="filter only by"):
        filter_tickets([], "email", "john@example.com")


def test_filter_rejects_invalid_status():
    with pytest.raises(ValueError, match="Invalid status"):
        filter_tickets([], "status", "working")


def test_filter_rejects_invalid_priority():
    with pytest.raises(ValueError, match="Invalid priority"):
        filter_tickets([], "priority", "urgent")


def test_delete_existing_ticket():
    tickets = [
        sample_ticket(ticket_id=1),
        sample_ticket(ticket_id=2),
    ]

    result = delete_ticket(tickets, 1)

    assert result is True
    assert [ticket["ticket_id"] for ticket in tickets] == [2]


def test_delete_missing_ticket_returns_false():
    tickets = [sample_ticket(ticket_id=1)]

    result = delete_ticket(tickets, 99)

    assert result is False
    assert len(tickets) == 1