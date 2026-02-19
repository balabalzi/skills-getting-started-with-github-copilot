import pytest


def test_get_activities_returns_all_activities(client):
    # Arrange
    # (no setup needed; using client and in-memory data)

    # Act
    resp = client.get("/activities")
    data = resp.json()

    # Assert
    assert resp.status_code == 200
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    verify_resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")
    assert email in verify_resp.json()[activity]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    activity = "NotAnActivity"
    email = "foo@bar.com"

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert resp.status_code == 404


def test_signup_already_signed_up_returns_400(client):
    # Arrange
    activity = "Basketball Team"
    email = "alex@mergington.edu"  # Already in sample data

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert resp.status_code == 400


def test_unregister_success_removes_participant(client):
    # Arrange
    activity = "Tennis Club"
    email = "james@mergington.edu"
    verify_before = client.get("/activities").json()[activity]["participants"]

    # Act
    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    verify_after = client.get("/activities").json()[activity]["participants"]

    # Assert
    assert resp.status_code == 200
    assert email in verify_before
    assert email not in verify_after


def test_unregister_not_signed_up_returns_404(client):
    # Arrange
    activity = "Science Club"
    email = "notpresent@mergington.edu"

    # Act
    resp = client.post(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert resp.status_code == 404


def test_unregister_nonexistent_activity_returns_404(client):
    # Arrange
    activity = "Nope"
    email = "foo@bar.com"

    # Act
    resp = client.post(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert resp.status_code == 404
