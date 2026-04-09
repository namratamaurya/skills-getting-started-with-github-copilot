def test_signup_new_student_successfully(client, reset_activities):
    """Test that a new student can successfully sign up for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newemail@mergington.edu"
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    # Verify participant was added
    updated_activities = client.get("/activities").json()
    assert email in updated_activities[activity_name]["participants"]
    assert len(updated_activities[activity_name]["participants"]) == initial_count + 1


def test_signup_duplicate_student_fails(client, reset_activities):
    """Test that a student cannot sign up twice for the same activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_fails(client, reset_activities):
    """Test that signup for non-existent activity returns 404"""
    # Arrange
    activity_name = "Non Existent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_adds_to_correct_activity(client, reset_activities):
    """Test that signup adds participant to correct activity only"""
    # Arrange
    signup_activity = "Programming Class"
    other_activity = "Chess Club"
    email = "newemail@mergington.edu"
    chess_initial_participants = client.get("/activities").json()["Chess Club"]["participants"].copy()
    
    # Act
    client.post(f"/activities/{signup_activity}/signup?email={email}")
    
    # Assert
    updated_activities = client.get("/activities").json()
    assert email in updated_activities[signup_activity]["participants"]
    assert email not in updated_activities[other_activity]["participants"]
    assert updated_activities[other_activity]["participants"] == chess_initial_participants
