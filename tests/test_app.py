from urllib.parse import quote


def test_get_activities(client):
    # Arrange

    # Act
    r = client.get("/activities")

    # Assert
    assert r.status_code == 200
    data = r.json()
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@example.com"

    # Act
    r = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert r.status_code == 200
    assert f"Signed up {email}" in r.json()["message"]
    data = client.get("/activities").json()
    assert email in data[activity]["participants"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "dup@example.com"

    # Act
    client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    r = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert r.status_code == 400


def test_remove_participant_success(client):
    # Arrange
    activity = "Chess Club"
    email = "remove@example.com"
    client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Act
    r = client.delete(f"/activities/{quote(activity)}/participants?email={quote(email)}")

    # Assert
    assert r.status_code == 200
    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]


def test_remove_missing_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "noone@example.com"

    # Act
    r = client.delete(f"/activities/{quote(activity)}/participants?email={quote(email)}")

    # Assert
    assert r.status_code == 404
