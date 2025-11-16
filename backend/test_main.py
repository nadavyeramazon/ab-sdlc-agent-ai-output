"""Comprehensive test suite for FastAPI backend.

Tests cover:
- Existing API endpoint functionality (GET /api/hello, GET /health)
- New greet API endpoint functionality (POST /api/greet)
- Response format validation
- CORS header verification
- Input validation and error handling
- Response time requirements
- Integration tests for all features
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import time
from main import app

# Create test client
client = TestClient(app)


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint (EXISTING FEATURE)."""

    def test_hello_endpoint_returns_200(self):
        """Test that /api/hello returns HTTP 200 status code."""
        response = client.get("/api/hello")
        assert response.status_code == 200

    def test_hello_endpoint_returns_json(self):
        """Test that /api/hello returns JSON content type."""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"

    def test_hello_endpoint_has_message_field(self):
        """Test that response contains 'message' field."""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello World from Backend!"

    def test_hello_endpoint_has_timestamp_field(self):
        """Test that response contains 'timestamp' field."""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
        
        # Validate timestamp format (ISO 8601)
        timestamp = data["timestamp"]
        assert timestamp.endswith("Z")
        # Parse to verify it's a valid ISO format timestamp
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

    def test_hello_endpoint_response_structure(self):
        """Test complete response structure matches specification."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Verify exactly two fields
        assert len(data) == 2
        assert "message" in data
        assert "timestamp" in data
        
        # Verify types
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)

    def test_hello_endpoint_response_time(self):
        """Test that /api/hello responds within 100ms."""
        start_time = time.time()
        response = client.get("/api/hello")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms requirement"

    def test_hello_endpoint_cors_headers(self):
        """Test that CORS headers are present in response."""
        response = client.get("/api/hello", headers={"Origin": "http://localhost:3000"})
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


class TestHealthEndpoint:
    """Test suite for /health endpoint (EXISTING FEATURE)."""

    def test_health_endpoint_returns_200(self):
        """Test that /health returns HTTP 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_json(self):
        """Test that /health returns JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_endpoint_has_status_field(self):
        """Test that response contains 'status' field with 'healthy' value."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_health_endpoint_response_structure(self):
        """Test complete response structure matches specification."""
        response = client.get("/health")
        data = response.json()
        
        # Verify exactly one field
        assert len(data) == 1
        assert "status" in data
        assert isinstance(data["status"], str)

    def test_health_endpoint_response_time(self):
        """Test that /health responds within 100ms."""
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms requirement"

    def test_health_endpoint_cors_headers(self):
        """Test that CORS headers are present in response."""
        response = client.get("/health", headers={"Origin": "http://localhost:3000"})
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


class TestGreetEndpoint:
    """Test suite for /api/greet endpoint (NEW FEATURE)."""

    def test_greet_endpoint_valid_name_returns_200(self):
        """Test that /api/greet returns HTTP 200 for valid name."""
        response = client.post("/api/greet", json={"name": "Alice"})
        assert response.status_code == 200

    def test_greet_endpoint_returns_json(self):
        """Test that /api/greet returns JSON content type."""
        response = client.post("/api/greet", json={"name": "Bob"})
        assert response.headers["content-type"] == "application/json"

    def test_greet_endpoint_valid_name_response_structure(self):
        """Test response structure for valid name."""
        response = client.post("/api/greet", json={"name": "Charlie"})
        data = response.json()
        
        # Verify exactly two fields
        assert len(data) == 2
        assert "greeting" in data
        assert "timestamp" in data
        
        # Verify types
        assert isinstance(data["greeting"], str)
        assert isinstance(data["timestamp"], str)

    def test_greet_endpoint_greeting_format(self):
        """Test that greeting message follows specification format."""
        test_name = "TestUser"
        response = client.post("/api/greet", json={"name": test_name})
        data = response.json()
        
        expected_greeting = f"Hello, {test_name}! Welcome to our purple-themed app!"
        assert data["greeting"] == expected_greeting

    def test_greet_endpoint_timestamp_format(self):
        """Test that timestamp is in ISO-8601 format."""
        response = client.post("/api/greet", json={"name": "David"})
        data = response.json()
        
        timestamp = data["timestamp"]
        assert timestamp.endswith("Z")
        # Parse to verify it's a valid ISO format timestamp
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

    def test_greet_endpoint_empty_name_returns_400(self):
        """Test that empty name returns HTTP 400."""
        response = client.post("/api/greet", json={"name": ""})
        assert response.status_code == 400

    def test_greet_endpoint_empty_name_error_message(self):
        """Test that empty name returns appropriate error message."""
        response = client.post("/api/greet", json={"name": ""})
        data = response.json()
        
        assert "detail" in data
        assert data["detail"] == "Name cannot be empty"

    def test_greet_endpoint_whitespace_name_returns_400(self):
        """Test that whitespace-only name returns HTTP 400."""
        response = client.post("/api/greet", json={"name": "   "})
        assert response.status_code == 400

    def test_greet_endpoint_whitespace_name_error_message(self):
        """Test that whitespace-only name returns appropriate error message."""
        response = client.post("/api/greet", json={"name": "   "})
        data = response.json()
        
        assert "detail" in data
        assert data["detail"] == "Name cannot be empty"

    def test_greet_endpoint_missing_name_field_returns_422(self):
        """Test that missing name field returns HTTP 422 (Pydantic validation)."""
        response = client.post("/api/greet", json={})
        assert response.status_code == 422

    def test_greet_endpoint_special_characters_in_name(self):
        """Test that special characters in name are handled correctly."""
        test_name = "O'Brien"
        response = client.post("/api/greet", json={"name": test_name})
        
        assert response.status_code == 200
        data = response.json()
        assert test_name in data["greeting"]

    def test_greet_endpoint_long_name(self):
        """Test that long names are handled correctly."""
        test_name = "VeryLongNameWithManyCharacters" * 3
        response = client.post("/api/greet", json={"name": test_name})
        
        assert response.status_code == 200
        data = response.json()
        assert test_name in data["greeting"]

    def test_greet_endpoint_response_time(self):
        """Test that /api/greet responds within 100ms."""
        start_time = time.time()
        response = client.post("/api/greet", json={"name": "SpeedTest"})
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms requirement"

    def test_greet_endpoint_cors_headers(self):
        """Test that CORS headers are present for POST requests."""
        response = client.post(
            "/api/greet",
            json={"name": "CorsTest"},
            headers={"Origin": "http://localhost:3000"}
        )
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"

    def test_greet_endpoint_performance_multiple_requests(self):
        """Test performance over multiple requests (P95 < 100ms)."""
        response_times = []
        
        for i in range(10):
            start_time = time.time()
            response = client.post("/api/greet", json={"name": f"User{i}"})
            end_time = time.time()
            
            assert response.status_code == 200
            response_times.append((end_time - start_time) * 1000)
        
        # Calculate P95 (95th percentile)
        response_times.sort()
        p95_index = int(len(response_times) * 0.95)
        p95_time = response_times[p95_index]
        
        assert p95_time < 100, f"P95 response time {p95_time}ms exceeds 100ms requirement"


class TestAPIIntegration:
    """Integration tests for API functionality."""

    def test_all_endpoints_accessible(self):
        """Test that all three endpoints are accessible."""
        # Test /api/hello
        hello_response = client.get("/api/hello")
        assert hello_response.status_code == 200
        
        # Test /health
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # Test /api/greet
        greet_response = client.post("/api/greet", json={"name": "Integration"})
        assert greet_response.status_code == 200

    def test_existing_endpoints_unchanged(self):
        """Test that existing endpoints maintain their original behavior."""
        # Test /api/hello response format hasn't changed
        hello_response = client.get("/api/hello")
        hello_data = hello_response.json()
        assert hello_data["message"] == "Hello World from Backend!"
        assert "timestamp" in hello_data
        
        # Test /health response format hasn't changed
        health_response = client.get("/health")
        health_data = health_response.json()
        assert health_data == {"status": "healthy"}

    def test_multiple_hello_requests(self):
        """Test that multiple requests to /api/hello work correctly."""
        responses = [client.get("/api/hello") for _ in range(5)]
        
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Hello World from Backend!"
            assert "timestamp" in data

    def test_timestamps_are_unique(self):
        """Test that consecutive requests have different timestamps."""
        response1 = client.get("/api/hello")
        time.sleep(0.01)  # Small delay to ensure different timestamps
        response2 = client.get("/api/hello")
        
        timestamp1 = response1.json()["timestamp"]
        timestamp2 = response2.json()["timestamp"]
        
        # Timestamps should be different
        assert timestamp1 != timestamp2

    def test_greet_timestamps_are_unique(self):
        """Test that consecutive greet requests have different timestamps."""
        response1 = client.post("/api/greet", json={"name": "User1"})
        time.sleep(0.01)  # Small delay
        response2 = client.post("/api/greet", json={"name": "User2"})
        
        timestamp1 = response1.json()["timestamp"]
        timestamp2 = response2.json()["timestamp"]
        
        assert timestamp1 != timestamp2

    def test_cors_preflight_request(self):
        """Test that CORS preflight requests are handled correctly."""
        # Test OPTIONS request for GET endpoint
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            }
        )
        assert response.status_code in [200, 204]
        
        # Test OPTIONS request for POST endpoint
        response = client.options(
            "/api/greet",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            }
        )
        assert response.status_code in [200, 204]

    def test_invalid_endpoint_returns_404(self):
        """Test that invalid endpoints return 404."""
        response = client.get("/api/invalid")
        assert response.status_code == 404

    def test_concurrent_different_endpoints(self):
        """Test that different endpoints can be used concurrently."""
        # Simulate concurrent use of different features
        hello_response = client.get("/api/hello")
        greet_response = client.post("/api/greet", json={"name": "Concurrent"})
        health_response = client.get("/health")
        
        # All should succeed
        assert hello_response.status_code == 200
        assert greet_response.status_code == 200
        assert health_response.status_code == 200

    def test_multiple_greet_requests_different_names(self):
        """Test multiple greet requests with different names."""
        names = ["Alice", "Bob", "Charlie", "David", "Eve"]
        
        for name in names:
            response = client.post("/api/greet", json={"name": name})
            assert response.status_code == 200
            
            data = response.json()
            assert name in data["greeting"]
            assert "Welcome to our purple-themed app!" in data["greeting"]
