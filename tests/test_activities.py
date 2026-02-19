import pytest


def test_get_activities_returns_all_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known keys from the sample data
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success_adds_participant(client):
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    json = resp.json()
    assert "Signed up" in json.get("message", "")

    # Verify participant added
    get_resp = client.get("/activities")
    participants = get_resp.json()[activity]["participants"]
    assert email in participants


def test_signup_nonexistent_activity_returns_404(client):
    resp = client.post("/activities/NotAnActivity/signup?email=foo@bar.com")
    assert resp.status_code == 404


def test_signup_already_signed_up_returns_400(client):
    activity = "Basketball Team"
    # alex@mergington.edu is already in sample data
    email = "alex@mergington.edu"

    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400


def test_unregister_success_removes_participant(client):
    activity = "Tennis Club"
    email = "james@mergington.edu"

    # Ensure present first
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]

    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 200

    # Verify removed
    get_resp = client.get("/activities")
    assert email not in get_resp.json()[activity]["participants"]


def test_unregister_not_signed_up_returns_404(client):
    activity = "Science Club"
    email = "notpresent@mergington.edu"

    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 404


def test_unregister_nonexistent_activity_returns_404(client):
    resp = client.post("/activities/Nope/unregister?email=foo@bar.com")
    assert resp.status_code == 404
