from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from assignments.starter_code.ex5_capstone_solution import app


@pytest.mark.api
def test_internal_admin_can_create_high_priority_task() -> None:
    """Verify trusted internal callers can trigger high-priority work."""

    client = TestClient(app)
    response = client.post(
        "/tasks",
        json={
            "source": "github",
            "issue": "Create slugify(text) utility with tests.",
            "risk": "high",
            "requester": "pm@company.com",
        },
        headers={"X-API-Key": "sk-internal-admin"},
    )

    assert response.status_code == 202
    assert "task_id" in response.json()


@pytest.mark.api
def test_external_vendor_blocked_from_high_priority() -> None:
    """Verify the API boundary rejects untrusted high-risk requests."""

    client = TestClient(app)
    response = client.post(
        "/tasks",
        json={
            "source": "github",
            "issue": "Create slugify(text) utility with tests.",
            "risk": "high",
            "requester": "vendor@external.com",
        },
        headers={"X-API-Key": "sk-external-vendor"},
    )

    assert response.status_code == 403
    assert "external vendors" in response.json()["detail"].lower()


@pytest.mark.api
def test_invalid_api_key_blocked() -> None:
    """Verify requests fail before entering the agent pipeline."""

    client = TestClient(app)
    response = client.post(
        "/tasks",
        json={
            "source": "github",
            "issue": "Create slugify(text) utility with tests.",
            "risk": "low",
            "requester": "unknown@example.com",
        },
        headers={"X-API-Key": "bad-key"},
    )

    assert response.status_code == 401


@pytest.mark.api
def test_task_status_endpoint_returns_known_task() -> None:
    """Verify the async workflow exposes pollable task state."""

    client = TestClient(app)
    create_response = client.post(
        "/tasks",
        json={
            "source": "github",
            "issue": "Create slugify(text) utility with tests.",
            "risk": "medium",
            "requester": "pm@company.com",
        },
        headers={"X-API-Key": "sk-internal-admin"},
    )
    task_id = create_response.json()["task_id"]

    status_response = client.get(f"/tasks/{task_id}")

    assert status_response.status_code == 200
    assert status_response.json()["task_id"] == task_id
    assert status_response.json()["status"] in {"PENDING", "RUNNING", "SHIPPED", "ESCALATED"}
