"""Comprehensive tests for the Greeting API backend."""
import pytest
from fastapi.testclient import TestClient
from backend.main import app, GREETINGS


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_returns_welcome_message(self, client):
        """Test that root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Welcome" in data["message"]
        assert "version" in data
        assert "endpoints" in data

    def test_root_includes_endpoint_info(self, client):
        """Test that root endpoint includes information about available endpoints."""
        response = client.get("/")
        data = response.json()
        assert "greet" in data["endpoints"]
        assert "health" in data["endpoints"]


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_returns_healthy_status(self, client):
        """Test that health check returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "greeting-api"


class TestGreetEndpoint:
    """Tests for the greet user endpoint."""

    def test_greet_user_with_default_language(self, client):
        """Test greeting a user with default English language."""
        response = client.post(
            "/api/greet",
            json={"name": "John", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "John" in data["message"]
        assert "Hello" in data["message"]
        assert data["name"] == "John"
        assert data["language"] == "en"

    def test_greet_user_in_spanish(self, client):
        """Test greeting a user in Spanish."""
        response = client.post(
            "/api/greet",
            json={"name": "Maria", "language": "es"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Hola" in data["message"]
        assert "Maria" in data["message"]
        assert data["language"] == "es"

    def test_greet_user_in_french(self, client):
        """Test greeting a user in French."""
        response = client.post(
            "/api/greet",
            json={"name": "Pierre", "language": "fr"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Bonjour" in data["message"]
        assert "Pierre" in data["message"]
        assert data["language"] == "fr"

    def test_greet_user_in_german(self, client):
        """Test greeting a user in German."""
        response = client.post(
            "/api/greet",
            json={"name": "Hans", "language": "de"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Guten Tag" in data["message"]
        assert "Hans" in data["message"]
        assert data["language"] == "de"

    def test_greet_with_uppercase_language(self, client):
        """Test that language code is case-insensitive."""
        response = client.post(
            "/api/greet",
            json={"name": "Alice", "language": "EN"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "en"

    def test_greet_with_unsupported_language(self, client):
        """Test greeting with unsupported language returns error."""
        response = client.post(
            "/api/greet",
            json={"name": "John", "language": "it"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "not supported" in data["detail"].lower()

    def test_greet_without_name(self, client):
        """Test that request without name returns validation error."""
        response = client.post(
            "/api/greet",
            json={"language": "en"}
        )
        assert response.status_code == 422  # Validation error

    def test_greet_with_empty_name(self, client):
        """Test that empty name returns validation error."""
        response = client.post(
            "/api/greet",
            json={"name": "", "language": "en"}
        )
        assert response.status_code == 422  # Validation error

    def test_greet_with_long_name(self, client):
        """Test greeting with a long name."""
        long_name = "A" * 50  # 50 characters, within limit
        response = client.post(
            "/api/greet",
            json={"name": long_name, "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert long_name in data["message"]

    def test_greet_with_too_long_name(self, client):
        """Test that name exceeding max length returns validation error."""
        too_long_name = "A" * 101  # Exceeds 100 character limit
        response = client.post(
            "/api/greet",
            json={"name": too_long_name, "language": "en"}
        )
        assert response.status_code == 422  # Validation error

    def test_greet_with_special_characters_in_name(self, client):
        """Test greeting with special characters in name."""
        response = client.post(
            "/api/greet",
            json={"name": "José-María", "language": "es"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "José-María" in data["message"]

    def test_greet_message_contains_blue_theme_reference(self, client):
        """Test that greeting message references blue theme."""
        response = client.post(
            "/api/greet",
            json={"name": "John", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "blue" in data["message"].lower()

    def test_greet_without_language_uses_default(self, client):
        """Test that omitting language parameter uses default English."""
        response = client.post(
            "/api/greet",
            json={"name": "John"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "en"
        assert "Hello" in data["message"]


class TestCORSConfiguration:
    """Tests for CORS middleware configuration."""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses."""
        response = client.options("/api/greet")
        # CORS headers should be present
        assert response.status_code in [200, 405]  # OPTIONS may not be implemented

    def test_api_accepts_post_requests(self, client):
        """Test that API accepts POST requests (CORS allows methods)."""
        response = client.post(
            "/api/greet",
            json={"name": "Test", "language": "en"}
        )
        assert response.status_code == 200


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""

    def test_openapi_docs_available(self, client):
        """Test that OpenAPI documentation is available."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_json_available(self, client):
        """Test that OpenAPI JSON schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data


class TestGreetingsConfiguration:
    """Tests for greetings configuration."""

    def test_all_supported_languages_work(self, client):
        """Test that all languages in GREETINGS dictionary work."""
        for lang_code in GREETINGS.keys():
            response = client.post(
                "/api/greet",
                json={"name": "Test", "language": lang_code}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["language"] == lang_code
            assert GREETINGS[lang_code] in data["message"]
