"""Comprehensive tests for the Howdy API endpoint."""
import pytest
from fastapi.testclient import TestClient
from backend.main import app, HOWDY_GREETINGS


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestHowdyEndpoint:
    """Tests for the howdy user endpoint."""

    def test_howdy_user_with_default_language(self, client):
        """Test howdy greeting with default English language."""
        response = client.post(
            "/api/howdy",
            json={"name": "John", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "John" in data["message"]
        assert "Howdy" in data["message"]
        assert data["name"] == "John"
        assert data["language"] == "en"
        assert data["greeting_type"] == "howdy"

    def test_howdy_user_in_spanish(self, client):
        """Test howdy greeting in Spanish."""
        response = client.post(
            "/api/howdy",
            json={"name": "Maria", "language": "es"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Qué tal" in data["message"]
        assert "Maria" in data["message"]
        assert data["language"] == "es"
        assert data["greeting_type"] == "howdy"

    def test_howdy_user_in_french(self, client):
        """Test howdy greeting in French."""
        response = client.post(
            "/api/howdy",
            json={"name": "Pierre", "language": "fr"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Salut" in data["message"]
        assert "Pierre" in data["message"]
        assert data["language"] == "fr"
        assert data["greeting_type"] == "howdy"

    def test_howdy_user_in_german(self, client):
        """Test howdy greeting in German."""
        response = client.post(
            "/api/howdy",
            json={"name": "Hans", "language": "de"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Moin" in data["message"]
        assert "Hans" in data["message"]
        assert data["language"] == "de"
        assert data["greeting_type"] == "howdy"

    def test_howdy_with_uppercase_language(self, client):
        """Test that language code is case-insensitive for howdy."""
        response = client.post(
            "/api/howdy",
            json={"name": "Alice", "language": "EN"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "en"
        assert "Howdy" in data["message"]

    def test_howdy_with_unsupported_language(self, client):
        """Test howdy with unsupported language returns error."""
        response = client.post(
            "/api/howdy",
            json={"name": "John", "language": "it"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "not supported" in data["detail"].lower()

    def test_howdy_without_name(self, client):
        """Test that howdy request without name returns validation error."""
        response = client.post(
            "/api/howdy",
            json={"language": "en"}
        )
        assert response.status_code == 422  # Validation error

    def test_howdy_with_empty_name(self, client):
        """Test that empty name returns validation error."""
        response = client.post(
            "/api/howdy",
            json={"name": "", "language": "en"}
        )
        assert response.status_code == 422  # Validation error

    def test_howdy_with_long_name(self, client):
        """Test howdy with a long name."""
        long_name = "A" * 50  # 50 characters, within limit
        response = client.post(
            "/api/howdy",
            json={"name": long_name, "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert long_name in data["message"]

    def test_howdy_with_too_long_name(self, client):
        """Test that name exceeding max length returns validation error."""
        too_long_name = "A" * 101  # Exceeds 100 character limit
        response = client.post(
            "/api/howdy",
            json={"name": too_long_name, "language": "en"}
        )
        assert response.status_code == 422  # Validation error

    def test_howdy_with_special_characters_in_name(self, client):
        """Test howdy with special characters in name."""
        response = client.post(
            "/api/howdy",
            json={"name": "José-María", "language": "es"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "José-María" in data["message"]

    def test_howdy_message_contains_casual_phrase(self, client):
        """Test that howdy message contains casual phrase."""
        response = client.post(
            "/api/howdy",
            json={"name": "John", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        # Should contain casual elements
        message_lower = data["message"].lower()
        assert "great day" in message_lower or "🤠" in data["message"]

    def test_howdy_without_language_uses_default(self, client):
        """Test that omitting language parameter uses default English."""
        response = client.post(
            "/api/howdy",
            json={"name": "John"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "en"
        assert "Howdy" in data["message"]

    def test_howdy_response_model_structure(self, client):
        """Test that howdy response has correct structure."""
        response = client.post(
            "/api/howdy",
            json={"name": "Test", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        # Verify all expected fields are present
        assert "message" in data
        assert "name" in data
        assert "language" in data
        assert "greeting_type" in data
        assert isinstance(data["message"], str)
        assert isinstance(data["name"], str)
        assert isinstance(data["language"], str)
        assert isinstance(data["greeting_type"], str)

    def test_howdy_greeting_type_is_howdy(self, client):
        """Test that greeting_type field is always 'howdy'."""
        for lang in HOWDY_GREETINGS.keys():
            response = client.post(
                "/api/howdy",
                json={"name": "Test", "language": lang}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["greeting_type"] == "howdy"

    def test_all_howdy_languages_work(self, client):
        """Test that all languages in HOWDY_GREETINGS dictionary work."""
        for lang_code, greeting_text in HOWDY_GREETINGS.items():
            response = client.post(
                "/api/howdy",
                json={"name": "Test", "language": lang_code}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["language"] == lang_code
            assert greeting_text in data["message"]

    def test_howdy_different_from_greet(self, client):
        """Test that howdy returns different message than greet endpoint."""
        # Test howdy endpoint
        howdy_response = client.post(
            "/api/howdy",
            json={"name": "John", "language": "en"}
        )
        # Test greet endpoint
        greet_response = client.post(
            "/api/greet",
            json={"name": "John", "language": "en"}
        )
        
        assert howdy_response.status_code == 200
        assert greet_response.status_code == 200
        
        howdy_data = howdy_response.json()
        greet_data = greet_response.json()
        
        # Messages should be different
        assert howdy_data["message"] != greet_data["message"]
        # Howdy should have the greeting_type field
        assert "greeting_type" in howdy_data
        assert "greeting_type" not in greet_data

    def test_howdy_with_multiple_users(self, client):
        """Test howdy with multiple different users in sequence."""
        users = [
            {"name": "Alice", "language": "en"},
            {"name": "Bob", "language": "es"},
            {"name": "Charlie", "language": "fr"},
            {"name": "David", "language": "de"},
        ]
        
        for user in users:
            response = client.post("/api/howdy", json=user)
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == user["name"]
            assert data["language"] == user["language"]
            assert user["name"] in data["message"]


class TestRootEndpointWithHowdy:
    """Test that root endpoint includes howdy information."""

    def test_root_includes_howdy_endpoint(self, client):
        """Test that root endpoint lists howdy in endpoints."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "endpoints" in data
        assert "howdy" in data["endpoints"]
        assert data["endpoints"]["howdy"] == "/api/howdy"
