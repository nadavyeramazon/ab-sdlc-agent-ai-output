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
