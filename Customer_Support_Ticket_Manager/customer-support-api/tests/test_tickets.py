def ticket_payload(**overrides):
    payload = {
        "customer_name": "Alice",
        "email": "alice@example.com",
        "subject": "Billing issue",
        "description": "I was charged twice.",
        "priority": "medium",
    }

    payload.update(overrides)
    return payload


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Customer Support API is running"
    )


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": "connected",
    }


def test_create_ticket(client):
    response = client.post(
        "/tickets",
        json=ticket_payload(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["ticket_id"] == 1
    assert data["customer_name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["status"] == "open"
    assert data["priority"] == "medium"
    assert "created_at" in data


def test_create_ticket_rejects_invalid_email(client):
    response = client.post(
        "/tickets",
        json=ticket_payload(email="not-an-email"),
    )

    assert response.status_code == 422


def test_create_ticket_rejects_invalid_priority(client):
    response = client.post(
        "/tickets",
        json=ticket_payload(priority="urgent"),
    )

    assert response.status_code == 422


def test_create_ticket_rejects_blank_subject(client):
    response = client.post(
        "/tickets",
        json=ticket_payload(subject="   "),
    )

    assert response.status_code == 422


def test_client_cannot_set_ticket_id(client):
    response = client.post(
        "/tickets",
        json=ticket_payload(ticket_id=999),
    )

    assert response.status_code == 422


def test_list_tickets(client):
    client.post("/tickets", json=ticket_payload())
    client.post(
        "/tickets",
        json=ticket_payload(
            customer_name="Bob",
            email="bob@example.com",
        ),
    )

    response = client.get("/tickets")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_ticket(client):
    created = client.post(
        "/tickets",
        json=ticket_payload(),
    ).json()

    response = client.get(
        f"/tickets/{created['ticket_id']}"
    )

    assert response.status_code == 200
    assert response.json()["subject"] == "Billing issue"


def test_get_missing_ticket(client):
    response = client.get("/tickets/999")

    assert response.status_code == 404


def test_update_ticket(client):
    created = client.post(
        "/tickets",
        json=ticket_payload(),
    ).json()

    ticket_id = created["ticket_id"]

    response = client.patch(
        f"/tickets/{ticket_id}",
        json={
            "status": "resolved",
            "priority": "high",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "resolved"
    assert response.json()["priority"] == "high"


def test_update_rejects_invalid_status(client):
    created = client.post(
        "/tickets",
        json=ticket_payload(),
    ).json()

    response = client.patch(
        f"/tickets/{created['ticket_id']}",
        json={"status": "working"},
    )

    assert response.status_code == 422


def test_update_rejects_empty_payload(client):
    created = client.post(
        "/tickets",
        json=ticket_payload(),
    ).json()

    response = client.patch(
        f"/tickets/{created['ticket_id']}",
        json={},
    )

    assert response.status_code == 400


def test_filter_tickets_by_status(client):
    first = client.post(
        "/tickets",
        json=ticket_payload(),
    ).json()

    client.post(
        "/tickets",
        json=ticket_payload(
            customer_name="Bob",
            email="bob@example.com",
        ),
    )

    client.patch(
        f"/tickets/{first['ticket_id']}",
        json={"status": "resolved"},
    )

    response = client.get(
        "/tickets",
        params={"status": "resolved"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "resolved"


def test_filter_tickets_by_priority(client):
    client.post(
        "/tickets",
        json=ticket_payload(priority="high"),
    )

    client.post(
        "/tickets",
        json=ticket_payload(
            customer_name="Bob",
            email="bob@example.com",
            priority="low",
        ),
    )

    response = client.get(
        "/tickets",
        params={"priority": "high"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["priority"] == "high"


def test_pagination(client):
    for index in range(3):
        client.post(
            "/tickets",
            json=ticket_payload(
                customer_name=f"Customer {index}",
                email=f"customer{index}@example.com",
            ),
        )

    response = client.get(
        "/tickets",
        params={"skip": 1, "limit": 1},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_ticket(client):
    created = client.post(
        "/tickets",
        json=ticket_payload(),
    ).json()

    ticket_id = created["ticket_id"]

    response = client.delete(f"/tickets/{ticket_id}")

    assert response.status_code == 204

    check_response = client.get(f"/tickets/{ticket_id}")

    assert check_response.status_code == 404


def test_delete_missing_ticket(client):
    response = client.delete("/tickets/999")

    assert response.status_code == 404