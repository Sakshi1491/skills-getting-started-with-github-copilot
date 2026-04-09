# Tests for FastAPI activities endpoints using AAA pattern

def test_get_activities(client):
    # Arrange: client fixture provided
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all("name" in activity for activity in data)

def test_signup_activity_success(client):
    # Arrange
    student = {"student_name": "Alice"}
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", json=student)
    # Assert
    assert response.status_code == 200
    assert response.json()["message"].startswith("Alice signed up for Chess Club")

def test_signup_activity_duplicate(client):
    # Arrange
    student = {"student_name": "Bob"}
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup", json=student)
    # Act
    response = client.post(f"/activities/{activity}/signup", json=student)
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_activity_not_found(client):
    # Arrange
    student = {"student_name": "Charlie"}
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", json=student)
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_unregister_activity_success(client):
    # Arrange
    student = {"student_name": "Daisy"}
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup", json=student)
    # Act
    response = client.delete(f"/activities/{activity}/unregister", json=student)
    # Assert
    assert response.status_code == 200
    assert response.json()["message"].startswith("Daisy unregistered from Chess Club")

def test_unregister_activity_not_found(client):
    # Arrange
    student = {"student_name": "Eve"}
    activity = "Nonexistent Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister", json=student)
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_unregister_activity_not_signed_up(client):
    # Arrange
    student = {"student_name": "Frank"}
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister", json=student)
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]
