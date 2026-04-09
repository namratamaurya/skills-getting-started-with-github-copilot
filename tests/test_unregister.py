def test_unregister_participant_successfully(client, reset_activities):
    """Test that a participant can be successfully unregistered"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Currently enrolled
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])
    
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    # Verify participant was removed
    updated_activities = client.get("/activities").json()
    assert email not in updated_activities[activity_name]["participants"]
    assert len(updated_activities[activity_name]["participants"]) == initial_count - 1


def test_unregister_nonexistent_activity_fails(client, reset_activities):
    """Test that unregistering from non-existent activity returns 404"""
    # Arrange
    activity_name = "Non Existent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_student_not_enrolled_fails(client, reset_activities):
    """Test that unregistering a student not enrolled returns 400"""
    # Arrange
    activity_name = "Chess Club"
    email = "notenrolled@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_removes_from_correct_activity(client, reset_activities):
    """Test that unregister removes participant from correct activity only"""
    # Arrange
    unregister_activity = "Chess Club"
    other_activity = "Programming Class"
    email = "michael@mergington.edu"
    prog_initial_participants = client.get("/activities").json()["Programming Class"]["participants"].copy()
    
    # Act
    client.delete(f"/activities/{unregister_activity}/unregister?email={email}")
    
    # Assert
    updated_activities = client.get("/activities").json()
    assert email not in updated_activities[unregister_activity]["participants"]
    assert updated_activities[other_activity]["participants"] == prog_initial_participants
