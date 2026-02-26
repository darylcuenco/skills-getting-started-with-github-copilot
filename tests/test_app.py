import pytest


def test_root_redirects(client):
    # Arrange: nothing special
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 307
    assert response.headers["location"].endswith("/static/index.html")


def test_list_activities_contains_expected_keys(client):
    # Arrange: nothing special
    # Act
    response = client.get("/activities")
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert isinstance(data, dict)
    # make sure a couple of known activities exist
    assert "Chess Club" in data
    assert "Gym Class" in data
    assert all(
        key in data["Chess Club"]
        for key in ("description", "schedule", "max_participants", "participants")
    )


def test_successful_signup_adds_participant(client):
    # Arrange
    target = "/activities/Chess Club/signup"
    email = "teststudent@mergington.edu"

    # Act
    response = client.post(f"{target}?email={email}")
    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Signed up" in payload["message"]

    # a second GET should show the participant added
    after = client.get("/activities").json()
    assert email in after["Chess Club"]["participants"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    target = "/activities/Tennis Club/signup"
    email = "dup@mergington.edu"

    # sign up once
    client.post(f"{target}?email={email}")

    # Act
    response = client.post(f"{target}?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_nonexistent_activity_returns_404(client):
    # Arrange
    target = "/activities/DoesNotExist/signup"
    email = "none@mergington.edu"

    # Act
    response = client.post(f"{target}?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
