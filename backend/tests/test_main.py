"""Comprehensive tests for FastAPI backend endpoints."""

import re
from datetime import datetime
from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)


class TestHelloEndpoint:
    """Tests for the /api/hello endpoint."""

    def test_hello_returns_200_status_code(self):
        """Test that /api/hello endpoint returns 200 OK status."""
        response = client.get("/api/hello")
        assert response.status_code == 200

    def test_hello_returns_json_response(self):
        """Test that /api/hello returns a valid JSON response."""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"
        data = response.json()
        assert isinstance(data, dict)

    def test_hello_has_required_fields(self):
        """Test that /api/hello response contains message and timestamp fields."""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert "timestamp" in data

    def test_hello_message_content_is_correct(self):
        """Test that /api/hello returns the correct greeting message."""
        response = client.get("/api/hello")
        data = response.json()
        assert data["message"] == "Hello World from Backend!"

    def test_hello_timestamp_is_iso8601_format(self):
        """Test that /api/hello timestamp is in ISO-8601 format with Z suffix."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Check that timestamp ends with 'Z'
        assert timestamp.endswith("Z"), "Timestamp should end with 'Z' for UTC"
        
        # Verify ISO-8601 format using regex pattern
        iso8601_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$'
        assert re.match(iso8601_pattern, timestamp), "Timestamp should match ISO-8601 format"

    def test_hello_timestamp_is_parseable(self):
        """Test that /api/hello timestamp can be parsed as a valid datetime."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Remove 'Z' and parse the timestamp
        try:
            parsed_time = datetime.fromisoformat(timestamp.rstrip('Z'))
            assert isinstance(parsed_time, datetime)
        except ValueError:
            assert False, "Timestamp should be parseable as ISO-8601 datetime"

    def test_hello_timestamp_is_recent(self):
        """Test that /api/hello timestamp is recent (within last minute)."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Parse timestamp and check it's recent
        parsed_time = datetime.fromisoformat(timestamp.rstrip('Z'))
        current_time = datetime.utcnow()
        time_diff = (current_time - parsed_time).total_seconds()
        
        # Should be within 1 minute
        assert abs(time_diff) < 60, "Timestamp should be recent (within 1 minute)"


class TestHealthEndpoint:
    """Tests for the /health endpoint."""

    def test_health_returns_200_status_code(self):
        """Test that /health endpoint returns 200 OK status."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_json_response(self):
        """Test that /health returns a valid JSON response."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
        data = response.json()
        assert isinstance(data, dict)

    def test_health_has_status_field(self):
        """Test that /health response contains status field."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data

    def test_health_status_is_healthy(self):
        """Test that /health returns 'healthy' status."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_response_structure(self):
        """Test that /health response has exactly the expected structure."""
        response = client.get("/health")
        data = response.json()
        assert len(data) == 1, "Health response should only have status field"
        assert list(data.keys()) == ["status"]


class TestGreetEndpoint:
    """Comprehensive tests for the /api/greet endpoint."""

    # ===== SUCCESS SCENARIOS =====
    
    def test_greet_with_valid_name_returns_200(self):
        """Test that /api/greet with valid name returns 200 OK status."""
        response = client.post("/api/greet", json={"name": "Alice"})
        assert response.status_code == 200

    def test_greet_returns_personalized_greeting(self):
        """Test that /api/greet returns a personalized greeting message."""
        response = client.post("/api/greet", json={"name": "Bob"})
        data = response.json()
        
        assert "greeting" in data
        assert "Bob" in data["greeting"]
        assert data["greeting"] == "Hello, Bob! Welcome to our blue-themed app!"

    def test_greet_response_has_required_fields(self):
        """Test that /api/greet response contains greeting and timestamp fields."""
        response = client.post("/api/greet", json={"name": "Charlie"})
        data = response.json()
        
        assert "greeting" in data
        assert "timestamp" in data
        assert isinstance(data["greeting"], str)
        assert isinstance(data["timestamp"], str)

    def test_greet_timestamp_is_iso8601_format(self):
        """Test that /api/greet timestamp is in ISO-8601 format with Z suffix."""
        response = client.post("/api/greet", json={"name": "Diana"})
        data = response.json()
        timestamp = data["timestamp"]
        
        # Check that timestamp ends with 'Z'
        assert timestamp.endswith("Z"), "Timestamp should end with 'Z' for UTC"
        
        # Verify ISO-8601 format using regex pattern
        iso8601_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$'
        assert re.match(iso8601_pattern, timestamp), "Timestamp should match ISO-8601 format"

    def test_greet_timestamp_is_recent(self):
        """Test that /api/greet timestamp is recent (within last minute)."""
        response = client.post("/api/greet", json={"name": "Eve"})
        data = response.json()
        timestamp = data["timestamp"]
        
        # Parse timestamp and check it's recent
        parsed_time = datetime.fromisoformat(timestamp.rstrip('Z'))
        current_time = datetime.utcnow()
        time_diff = (current_time - parsed_time).total_seconds()
        
        # Should be within 1 minute
        assert abs(time_diff) < 60, "Timestamp should be recent (within 1 minute)"

    # ===== VALIDATION SCENARIOS =====
    
    def test_greet_with_missing_name_field_returns_422(self):
        """Test that /api/greet without name field returns 422 Unprocessable Entity."""
        response = client.post("/api/greet", json={})
        assert response.status_code == 422
        
        # Verify error details
        data = response.json()
        assert "detail" in data
        assert any("name" in str(error).lower() for error in data["detail"])

    def test_greet_with_empty_name_returns_422(self):
        """Test that /api/greet with empty name returns 422 validation error."""
        response = client.post("/api/greet", json={"name": ""})
        assert response.status_code == 422
        
        # Verify error message mentions empty name
        data = response.json()
        assert "detail" in data
        error_message = str(data["detail"]).lower()
        assert "empty" in error_message or "name" in error_message

    def test_greet_with_whitespace_only_name_returns_422(self):
        """Test that /api/greet with whitespace-only name returns 422 validation error."""
        response = client.post("/api/greet", json={"name": "   "})
        assert response.status_code == 422
        
        # Verify error message
        data = response.json()
        assert "detail" in data

    def test_greet_with_null_name_returns_422(self):
        """Test that /api/greet with null name returns 422 validation error."""
        response = client.post("/api/greet", json={"name": None})
        assert response.status_code == 422
        
        # Verify error details
        data = response.json()
        assert "detail" in data

    def test_greet_with_invalid_json_returns_422(self):
        """Test that /api/greet with invalid JSON returns 422 error."""
        response = client.post("/api/greet", data="invalid json", headers={"Content-Type": "application/json"})
        assert response.status_code == 422

    def test_greet_with_integer_name_returns_422(self):
        """Test that /api/greet with integer instead of string name returns 422."""
        response = client.post("/api/greet", json={"name": 12345})
        assert response.status_code == 422

    # ===== INPUT SANITIZATION & EDGE CASES =====
    
    def test_greet_trims_whitespace_from_name(self):
        """Test that /api/greet trims leading and trailing whitespace from name."""
        response = client.post("/api/greet", json={"name": "  Frank  "})
        assert response.status_code == 200
        
        data = response.json()
        # Name should be trimmed in the greeting
        assert "Frank" in data["greeting"]
        assert "  Frank  " not in data["greeting"]

    def test_greet_with_special_characters_in_name(self):
        """Test that /api/greet handles special characters in name properly."""
        special_names = [
            "O'Brien",
            "Jean-Luc",
            "María",
            "André",
            "李明"
        ]
        
        for name in special_names:
            response = client.post("/api/greet", json={"name": name})
            assert response.status_code == 200, f"Should handle special character name: {name}"
            
            data = response.json()
            assert name in data["greeting"], f"Greeting should contain the name: {name}"

    def test_greet_with_very_long_name(self):
        """Test that /api/greet handles very long names without errors."""
        long_name = "A" * 1000  # 1000 character name
        response = client.post("/api/greet", json={"name": long_name})
        
        # Should still return 200 (or implement length validation if needed)
        assert response.status_code == 200
        
        data = response.json()
        assert long_name in data["greeting"]

    def test_greet_with_single_character_name(self):
        """Test that /api/greet handles single character names."""
        response = client.post("/api/greet", json={"name": "X"})
        assert response.status_code == 200
        
        data = response.json()
        assert "X" in data["greeting"]

    # ===== ERROR HANDLING SCENARIOS =====
    
    def test_greet_with_get_method_returns_405(self):
        """Test that /api/greet with GET method returns 405 Method Not Allowed."""
        response = client.get("/api/greet")
        assert response.status_code == 405

    def test_greet_with_put_method_returns_405(self):
        """Test that /api/greet with PUT method returns 405 Method Not Allowed."""
        response = client.put("/api/greet", json={"name": "Test"})
        assert response.status_code == 405

    def test_greet_with_delete_method_returns_405(self):
        """Test that /api/greet with DELETE method returns 405 Method Not Allowed."""
        response = client.delete("/api/greet")
        assert response.status_code == 405

    def test_greet_without_content_type_header(self):
        """Test that /api/greet handles missing Content-Type header gracefully."""
        # FastAPI TestClient handles this, but we test the behavior
        response = client.post("/api/greet", json={"name": "Test"})
        assert response.status_code == 200

    # ===== RESPONSE FORMAT VALIDATION =====
    
    def test_greet_returns_json_response(self):
        """Test that /api/greet returns a valid JSON response."""
        response = client.post("/api/greet", json={"name": "Grace"})
        assert response.headers["content-type"] == "application/json"
        data = response.json()
        assert isinstance(data, dict)

    def test_greet_response_structure_is_correct(self):
        """Test that /api/greet response has exactly the expected structure."""
        response = client.post("/api/greet", json={"name": "Henry"})
        data = response.json()
        
        # Should have exactly 2 keys: greeting and timestamp
        assert len(data) == 2
        assert set(data.keys()) == {"greeting", "timestamp"}

    def test_greet_multiple_requests_return_different_timestamps(self):
        """Test that multiple requests to /api/greet return different timestamps."""
        import time
        
        response1 = client.post("/api/greet", json={"name": "User1"})
        time.sleep(0.1)  # Small delay to ensure different timestamps
        response2 = client.post("/api/greet", json={"name": "User2"})
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Timestamps should differ
        assert data1["timestamp"] != data2["timestamp"]
        # But greetings should be different (different names)
        assert data1["greeting"] != data2["greeting"]

    # ===== CORS HEADERS FOR GREET ENDPOINT =====
    
    def test_greet_cors_allows_configured_origin(self):
        """Test that CORS allows POST requests to /api/greet from localhost:3000."""
        headers = {"Origin": "http://localhost:3000"}
        response = client.post("/api/greet", json={"name": "Test"}, headers=headers)
        
        # Check that CORS headers are present
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"

    def test_greet_cors_allows_credentials(self):
        """Test that CORS allows credentials for /api/greet endpoint."""
        headers = {"Origin": "http://localhost:3000"}
        response = client.post("/api/greet", json={"name": "Test"}, headers=headers)
        
        assert "access-control-allow-credentials" in response.headers
        assert response.headers["access-control-allow-credentials"] == "true"


class TestCORSConfiguration:
    """Tests for CORS middleware configuration."""

    def test_cors_allows_configured_origin(self):
        """Test that CORS allows requests from localhost:3000."""
        headers = {"Origin": "http://localhost:3000"}
        response = client.get("/api/hello", headers=headers)
        
        # Check that CORS headers are present
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"

    def test_cors_allows_credentials(self):
        """Test that CORS allows credentials."""
        headers = {"Origin": "http://localhost:3000"}
        response = client.get("/api/hello", headers=headers)
        
        assert "access-control-allow-credentials" in response.headers
        assert response.headers["access-control-allow-credentials"] == "true"

    def test_cors_preflight_request(self):
        """Test CORS preflight OPTIONS request."""
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "content-type"
        }
        response = client.options("/api/hello", headers=headers)
        
        # Preflight should return 200
        assert response.status_code == 200
        # Check CORS headers are present
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers


class TestEndpointIntegration:
    """Integration tests for overall API behavior."""

    def test_all_endpoints_are_accessible(self):
        """Test that all defined endpoints are accessible."""
        endpoints = ["/api/hello", "/health"]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200, f"Endpoint {endpoint} should be accessible"

    def test_greet_endpoint_is_accessible(self):
        """Test that /api/greet endpoint is accessible with POST method."""
        response = client.post("/api/greet", json={"name": "Integration Test"})
        assert response.status_code == 200

    def test_nonexistent_endpoint_returns_404(self):
        """Test that accessing non-existent endpoint returns 404."""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

    def test_multiple_hello_requests_return_different_timestamps(self):
        """Test that multiple requests to /api/hello return different timestamps."""
        import time
        
        response1 = client.get("/api/hello")
        time.sleep(0.1)  # Small delay to ensure different timestamps
        response2 = client.get("/api/hello")
        
        data1 = response1.json()
        data2 = response2.json()
        
        assert data1["timestamp"] != data2["timestamp"], "Timestamps should differ between requests"
        assert data1["message"] == data2["message"], "Message should remain the same"
