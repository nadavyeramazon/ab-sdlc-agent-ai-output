"""Comprehensive tests for the Howdy API endpoint."""
import pytest
from fastapi.testclient import TestClient
from backend.main import app, HOWDY_TEMPLATES

# Create test client
client = TestClient(app)


class TestHowdyEndpoint:
    """Tests for howdy endpoint."""
    
    def test_howdy_user_english_casual(self):
        """Test howdy user in English with casual style."""
        response = client.post(
            "/api/howdy",
            json={"name": "Alice", "language": "en", "style": "casual"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alice"
        assert data["language"] == "en"
        assert data["style"] == "casual"
        assert "Alice" in data["message"]
        assert "Howdy" in data["message"]
    
    def test_howdy_user_english_formal(self):
        """Test howdy user in English with formal style."""
        response = client.post(
            "/api/howdy",
            json={"name": "Bob", "language": "en", "style": "formal"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Bob"
        assert data["language"] == "en"
        assert data["style"] == "formal"
        assert "Bob" in data["message"]
        assert "Howdy" in data["message"]
    
    def test_howdy_user_english_friendly(self):
        """Test howdy user in English with friendly style."""
        response = client.post(
            "/api/howdy",
            json={"name": "Charlie", "language": "en", "style": "friendly"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Charlie"
        assert data["language"] == "en"
        assert data["style"] == "friendly"
        assert "Charlie" in data["message"]
        assert "Howdy" in data["message"]
    
    def test_howdy_user_spanish(self):
        """Test howdy user in Spanish."""
        response = client.post(
            "/api/howdy",
            json={"name": "Carlos", "language": "es", "style": "casual"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Carlos"
        assert data["language"] == "es"
        assert data["style"] == "casual"
        assert "Carlos" in data["message"]
    
    def test_howdy_user_french(self):
        """Test howdy user in French."""
        response = client.post(
            "/api/howdy",
            json={"name": "Marie", "language": "fr", "style": "formal"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Marie"
        assert data["language"] == "fr"
        assert data["style"] == "formal"
        assert "Marie" in data["message"]
    
    def test_howdy_user_german(self):
        """Test howdy user in German."""
        response = client.post(
            "/api/howdy",
            json={"name": "Hans", "language": "de", "style": "friendly"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Hans"
        assert data["language"] == "de"
        assert data["style"] == "friendly"
        assert "Hans" in data["message"]
    
    def test_howdy_user_italian(self):
        """Test howdy user in Italian."""
        response = client.post(
            "/api/howdy",
            json={"name": "Giuseppe", "language": "it", "style": "casual"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Giuseppe"
        assert data["language"] == "it"
        assert data["style"] == "casual"
        assert "Giuseppe" in data["message"]
    
    def test_howdy_user_default_language(self):
        """Test howdy user with default language (English)."""
        response = client.post(
            "/api/howdy",
            json={"name": "David", "style": "casual"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "David"
        assert data["language"] == "en"
        assert "David" in data["message"]
    
    def test_howdy_user_default_style(self):
        """Test howdy user with default style (casual)."""
        response = client.post(
            "/api/howdy",
            json={"name": "Eve", "language": "en"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Eve"
        assert data["style"] == "casual"
        assert "Eve" in data["message"]
    
    def test_howdy_user_minimal_request(self):
        """Test howdy user with only name (all defaults)."""
        response = client.post(
            "/api/howdy",
            json={"name": "Frank"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Frank"
        assert data["language"] == "en"
        assert data["style"] == "casual"
        assert "Frank" in data["message"]
    
    def test_howdy_user_unsupported_language(self):
        """Test howdy user with unsupported language defaults to English."""
        response = client.post(
            "/api/howdy",
            json={"name": "Grace", "language": "xyz", "style": "casual"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Grace"
        assert data["language"] == "en"  # Should default to English
        assert "Grace" in data["message"]
    
    def test_howdy_user_unsupported_style(self):
        """Test howdy user with unsupported style defaults to casual."""
        response = client.post(
            "/api/howdy",
            json={"name": "Henry", "language": "en", "style": "invalid"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Henry"
        assert data["style"] == "casual"  # Should default to casual
        assert "Henry" in data["message"]
    
    def test_howdy_user_case_insensitive_language(self):
        """Test that language parameter is case insensitive."""
        response = client.post(
            "/api/howdy",
            json={"name": "Iris", "language": "EN", "style": "casual"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "en"
    
    def test_howdy_user_case_insensitive_style(self):
        """Test that style parameter is case insensitive."""
        response = client.post(
            "/api/howdy",
            json={"name": "Jack", "language": "en", "style": "FORMAL"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["style"] == "formal"
    
    def test_howdy_user_missing_name(self):
        """Test that missing name returns validation error."""
        response = client.post(
            "/api/howdy",
            json={"language": "en", "style": "casual"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_howdy_user_empty_name(self):
        """Test that empty name returns validation error."""
        response = client.post(
            "/api/howdy",
            json={"name": "", "language": "en", "style": "casual"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_howdy_user_special_characters(self):
        """Test howdy with special characters in name."""
        response = client.post(
            "/api/howdy",
            json={"name": "José García-López", "language": "es", "style": "casual"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "José García-López"
        assert "José García-López" in data["message"]
    
    def test_howdy_user_long_name(self):
        """Test howdy with long name."""
        long_name = "A" * 100
        response = client.post(
            "/api/howdy",
            json={"name": long_name, "language": "en", "style": "casual"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == long_name
        assert long_name in data["message"]
    
    def test_howdy_user_with_numeric_name(self):
        """Test howdy with numeric characters in name."""
        response = client.post(
            "/api/howdy",
            json={"name": "User123", "language": "en", "style": "casual"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "User123" in data["message"]
    
    def test_howdy_user_with_emoji_in_name(self):
        """Test howdy with emoji in name."""
        response = client.post(
            "/api/howdy",
            json={"name": "Alice 🌊", "language": "en", "style": "friendly"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Alice 🌊" in data["message"]


class TestHowdyStylesEndpoint:
    """Tests for howdy styles endpoint."""
    
    def test_get_howdy_styles(self):
        """Test getting list of supported howdy styles."""
        response = client.get("/api/howdy/styles")
        assert response.status_code == 200
        data = response.json()
        assert "styles" in data
        assert "count" in data
        assert "description" in data
        assert isinstance(data["styles"], list)
        assert data["count"] == 3
        
        # Verify all expected styles are present
        expected_styles = ["casual", "formal", "friendly"]
        for style in expected_styles:
            assert style in data["styles"]
            assert style in data["description"]
    
    def test_howdy_styles_descriptions(self):
        """Test that style descriptions are meaningful."""
        response = client.get("/api/howdy/styles")
        data = response.json()
        
        for style in ["casual", "formal", "friendly"]:
            assert style in data["description"]
            assert len(data["description"][style]) > 0
            assert isinstance(data["description"][style], str)


class TestHowdyResponseModel:
    """Tests for howdy response model validation."""
    
    def test_howdy_response_model(self):
        """Test that response matches expected model."""
        response = client.post(
            "/api/howdy",
            json={"name": "Test", "language": "en", "style": "casual"}
        )
        data = response.json()
        
        # Verify all required fields are present
        assert "message" in data
        assert "name" in data
        assert "language" in data
        assert "style" in data
        
        # Verify field types
        assert isinstance(data["message"], str)
        assert isinstance(data["name"], str)
        assert isinstance(data["language"], str)
        assert isinstance(data["style"], str)


class TestHowdyAllCombinations:
    """Test all combinations of languages and styles."""
    
    def test_all_language_and_style_combinations(self):
        """Test that all language and style combinations work correctly."""
        languages = list(HOWDY_TEMPLATES.keys())
        styles = ["casual", "formal", "friendly"]
        
        for language in languages:
            for style in styles:
                response = client.post(
                    "/api/howdy",
                    json={"name": "TestUser", "language": language, "style": style}
                )
                assert response.status_code == 200, f"Failed for {language}/{style}"
                data = response.json()
                assert data["language"] == language
                assert data["style"] == style
                assert "TestUser" in data["message"]


class TestHowdyEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_multiple_consecutive_howdy_requests(self):
        """Test multiple consecutive requests work correctly."""
        names = ["Alice", "Bob", "Charlie", "David", "Eve"]
        styles = ["casual", "formal", "friendly", "casual", "formal"]
        
        for name, style in zip(names, styles):
            response = client.post(
                "/api/howdy",
                json={"name": name, "language": "en", "style": style}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == name
            assert data["style"] == style
    
    def test_howdy_versus_greet_different_messages(self):
        """Test that howdy and greet return different messages."""
        name = "TestUser"
        language = "en"
        
        # Get howdy response
        howdy_response = client.post(
            "/api/howdy",
            json={"name": name, "language": language, "style": "casual"}
        )
        howdy_data = howdy_response.json()
        
        # Get greet response
        greet_response = client.post(
            "/api/greet",
            json={"name": name, "language": language}
        )
        greet_data = greet_response.json()
        
        # Messages should be different
        assert howdy_data["message"] != greet_data["message"]
        assert howdy_data["name"] == greet_data["name"]
        assert howdy_data["language"] == greet_data["language"]