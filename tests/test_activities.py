import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""
    
    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns status code 200."""
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
    
    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary."""
        # Act
        response = client.get("/activities")
        
        # Assert
        assert isinstance(response.json(), dict)
    
    def test_activities_have_required_fields(self, client):
        """Test that each activity has required fields."""
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity in activities.items():
            assert "description" in activity
            assert "schedule" in activity
            assert "max_participants" in activity
            assert "participants" in activity
            assert isinstance(activity["participants"], list)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_returns_200(self, client):
        """Test successful signup returns status code 200."""
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
    
    def test_signup_adds_participant(self, client):
        """Test that signup actually adds the participant to the activity."""
        # Arrange
        email = "signup_test@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        activities = client.get("/activities").json()
        
        # Assert
        assert response.status_code == 200
        assert email in activities[activity]["participants"]
    
    def test_signup_returns_success_message(self, client):
        """Test that signup returns a success message."""
        # Arrange
        email = "message_test@mergington.edu"
        activity = "Programming Class"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert "Signed up" in data["message"]
        assert email in data["message"]
        assert activity in data["message"]
    
    def test_signup_to_nonexistent_activity_returns_404(self, client):
        """Test signup to nonexistent activity returns 404."""
        # Arrange
        email = "test@mergington.edu"
        activity = "Nonexistent Activity"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_duplicate_signup_returns_400(self, client):
        """Test that signing up twice for same activity returns 400."""
        # Arrange
        email = "duplicate_test@mergington.edu"
        activity = "Gym Class"
        
        # Act - First signup
        response1 = client.post(f"/activities/{activity}/signup?email={email}")
        
        # Act - Second signup with same email
        response2 = client.post(f"/activities/{activity}/signup?email={email}")
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"]


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/signup endpoint."""
    
    def test_remove_participant_returns_200(self, client):
        """Test successful removal returns status code 200."""
        # Arrange
        email = "remove_test@mergington.edu"
        activity = "Chess Club"
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
    
    def test_remove_participant_deletes_from_list(self, client):
        """Test that removal actually removes the participant from the activity."""
        # Arrange
        email = "delete_test@mergington.edu"
        activity = "Programming Class"
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup?email={email}"
        )
        activities = client.get("/activities").json()
        
        # Assert
        assert response.status_code == 200
        assert email not in activities[activity]["participants"]
    
    def test_remove_returns_success_message(self, client):
        """Test that removal returns a success message."""
        # Arrange
        email = "message_test@mergington.edu"
        activity = "Art Club"
        client.post(f"/activities/{activity}/signup?email={email}")
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup?email={email}"
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert "Removed" in data["message"]
        assert email in data["message"]
        assert activity in data["message"]
    
    def test_remove_nonexistent_activity_returns_404(self, client):
        """Test removal from nonexistent activity returns 404."""
        # Arrange
        email = "test@mergington.edu"
        activity = "Nonexistent Activity"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
    
    def test_remove_nonexistent_participant_returns_404(self, client):
        """Test removal of nonexistent participant returns 404."""
        # Arrange
        email = "nonexistent@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]


class TestRootRedirect:
    """Tests for GET / endpoint."""
    
    def test_root_redirects_to_static(self, client):
        """Test that root path redirects to /static/index.html."""
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
