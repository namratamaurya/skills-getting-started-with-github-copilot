def test_get_activities_returns_all_activities(client, reset_activities):
    """Test that GET /activities returns all available activities"""
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(activity in data for activity in expected_activities)


def test_get_activities_returns_activity_details(client, reset_activities):
    """Test that each activity contains required fields"""
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    chess_club = data.get("Chess Club")
    
    # Assert
    assert response.status_code == 200
    assert chess_club is not None
    assert all(field in chess_club for field in required_fields)


def test_get_activities_contains_correct_participants(client, reset_activities):
    """Test that activities have correct initial participants"""
    # Arrange
    expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert data["Chess Club"]["participants"] == expected_chess_participants
