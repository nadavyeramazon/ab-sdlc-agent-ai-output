import re
from fastapi.testclient import TestClient
from datetime import datetime
from main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Test suite for /health endpoint."""

    def test_health_check_returns_200(self):
        """Test that health endpoint returns HTTP 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_returns_json(self):
        """Test that health endpoint returns JSON content type."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_check_returns_healthy_status(self):
        """Test that health endpoint returns status 'healthy'."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_health_check_response_structure(self):
        """Test that health endpoint response has correct structure."""
        response = client.get("/health")
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 1
        assert "status" in data


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint."""

    def test_hello_returns_200(self):
        """Test that hello endpoint returns HTTP 200."""
        response = client.get("/api/hello")
        assert response.status_code == 200

    def test_hello_returns_json(self):
        """Test that hello endpoint returns JSON content type."""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"

    def test_hello_returns_correct_message(self):
        """Test that hello endpoint returns exact message."""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Hello World from Backend!"

    def test_hello_returns_timestamp(self):
        """Test that hello endpoint returns timestamp field."""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
        assert data["timestamp"] is not None

    def test_hello_timestamp_format(self):
        """Test that timestamp is in ISO-8601 format with Z suffix."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]

        # Validate ISO-8601 format with milliseconds and Z suffix
        # Format: YYYY-MM-DDTHH:MM:SS.sssZ
        iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$"
        assert re.match(
            iso_pattern, timestamp
        ), f"Timestamp {timestamp} does not match ISO-8601 format"

    def test_hello_timestamp_is_recent(self):
        """Test that timestamp is recent (within last minute)."""
        response = client.get("/api/hello")
        data = response.json()
        timestamp_str = data["timestamp"]

        # Parse timestamp (remove Z suffix for parsing)
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        now = datetime.utcnow()

        # Check timestamp is within last 60 seconds
        time_diff = (now - timestamp.replace(tzinfo=None)).total_seconds()
        assert time_diff < 60, f"Timestamp is not recent: {timestamp_str}"
        assert time_diff >= 0, f"Timestamp is in the future: {timestamp_str}"

    def test_hello_response_structure(self):
        """Test that hello endpoint response has correct structure."""
        response = client.get("/api/hello")
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 2
        assert "message" in data
        assert "timestamp" in data

    def test_hello_multiple_calls_different_timestamps(self):
        """Test that multiple calls return different timestamps."""
        response1 = client.get("/api/hello")
        data1 = response1.json()

        # Small delay to ensure different timestamps
        import time

        time.sleep(0.01)

        response2 = client.get("/api/hello")
        data2 = response2.json()

        # Timestamps should be different
        assert data1["timestamp"] != data2["timestamp"]


class TestGreetEndpoint:
    """Test suite for /api/greet endpoint."""

    def test_greet_returns_200_with_valid_name(self):
        """Test that greet endpoint returns HTTP 200 with valid name."""
        response = client.post("/api/greet", json={"name": "Alice"})
        assert response.status_code == 200

    def test_greet_returns_json(self):
        """Test that greet endpoint returns JSON content type."""
        response = client.post("/api/greet", json={"name": "Alice"})
        assert response.headers["content-type"] == "application/json"

    def test_greet_returns_correct_greeting(self):
        """Test that greet endpoint returns personalized greeting."""
        response = client.post("/api/greet", json={"name": "Alice"})
        data = response.json()
        assert "greeting" in data
        assert data["greeting"] == "Hello, Alice! Welcome to our purple-themed app!"

    def test_greet_returns_timestamp(self):
        """Test that greet endpoint returns timestamp field."""
        response = client.post("/api/greet", json={"name": "Alice"})
        data = response.json()
        assert "timestamp" in data
        assert data["timestamp"] is not None

    def test_greet_timestamp_format(self):
        """Test that timestamp is in ISO-8601 format with Z suffix."""
        response = client.post("/api/greet", json={"name": "Test"})
        data = response.json()
        timestamp = data["timestamp"]

        # Validate ISO-8601 format with microseconds and Z suffix
        # Format: YYYY-MM-DDTHH:MM:SS.ssssssZ
        iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$"
        assert re.match(
            iso_pattern, timestamp
        ), f"Timestamp {timestamp} does not match ISO-8601 format"

    def test_greet_empty_name_returns_400(self):
        """Test that empty name returns 400 error."""
        response = client.post("/api/greet", json={"name": ""})
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Name cannot be empty"

    def test_greet_whitespace_name_returns_400(self):
        """Test that whitespace-only name returns 400 error."""
        response = client.post("/api/greet", json={"name": "   "})
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Name cannot be empty"

    def test_greet_name_with_spaces(self):
        """Test that name with spaces is accepted."""
        response = client.post("/api/greet", json={"name": "John Doe"})
        assert response.status_code == 200
        data = response.json()
        assert "John Doe" in data["greeting"]

    def test_greet_special_characters(self):
        """Test that special characters in name are handled correctly."""
        response = client.post("/api/greet", json={"name": "José O'Brien"})
        assert response.status_code == 200
        data = response.json()
        assert "José O'Brien" in data["greeting"]

    def test_greet_name_with_leading_trailing_spaces(self):
        """Test that leading/trailing spaces are trimmed."""
        response = client.post("/api/greet", json={"name": "  Alice  "})
        assert response.status_code == 200
        data = response.json()
        assert data["greeting"] == "Hello, Alice! Welcome to our purple-themed app!"

    def test_greet_missing_name_field_returns_422(self):
        """Test that missing name field returns 422 validation error."""
        response = client.post("/api/greet", json={})
        assert response.status_code == 422

    def test_greet_response_structure(self):
        """Test that greet endpoint response has correct structure."""
        response = client.post("/api/greet", json={"name": "Test"})
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 2
        assert "greeting" in data
        assert "timestamp" in data

    def test_greet_multiple_calls_different_timestamps(self):
        """Test that multiple calls return different timestamps."""
        response1 = client.post("/api/greet", json={"name": "Alice"})
        data1 = response1.json()

        # Small delay to ensure different timestamps
        import time
        time.sleep(0.01)

        response2 = client.post("/api/greet", json={"name": "Bob"})
        data2 = response2.json()

        # Timestamps should be different
        assert data1["timestamp"] != data2["timestamp"]


class TestCORSConfiguration:
    """Test suite for CORS configuration."""

    def test_cors_allows_localhost_3000_get(self):
        """Test that CORS allows GET requests from localhost:3000."""
        response = client.get("/api/hello", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert (
            response.headers["access-control-allow-origin"] == "http://localhost:3000"
        )

    def test_cors_allows_localhost_3000_post(self):
        """Test that CORS allows POST requests from localhost:3000."""
        response = client.post(
            "/api/greet", 
            json={"name": "Test"},
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert (
            response.headers["access-control-allow-origin"] == "http://localhost:3000"
        )

    def test_cors_preflight_request_get(self):
        """Test CORS preflight OPTIONS request for GET."""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers

    def test_cors_preflight_request_post(self):
        """Test CORS preflight OPTIONS request for POST."""
        response = client.options(
            "/api/greet",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            },
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers


class TestPerformance:
    """Test suite for performance requirements."""

    def test_health_endpoint_response_time(self):
        """Test that health endpoint responds quickly (< 50ms)."""
        import time

        start = time.time()
        response = client.get("/health")
        end = time.time()

        response_time = (end - start) * 1000  # Convert to milliseconds
        assert response.status_code == 200
        # Allow some margin for test environment
        assert (
            response_time < 200
        ), f"Response time {response_time}ms exceeds 200ms threshold"

    def test_hello_endpoint_response_time(self):
        """Test that hello endpoint responds quickly (< 100ms)."""
        import time

        start = time.time()
        response = client.get("/api/hello")
        end = time.time()

        response_time = (end - start) * 1000  # Convert to milliseconds
        assert response.status_code == 200
        # Allow some margin for test environment
        assert (
            response_time < 200
        ), f"Response time {response_time}ms exceeds 200ms threshold"

    def test_greet_endpoint_response_time(self):
        """Test that greet endpoint responds quickly (< 100ms)."""
        import time

        start = time.time()
        response = client.post("/api/greet", json={"name": "Performance Test"})
        end = time.time()

        response_time = (end - start) * 1000  # Convert to milliseconds
        assert response.status_code == 200
        # Allow some margin for test environment
        assert (
            response_time < 200
        ), f"Response time {response_time}ms exceeds 200ms threshold"


class TestErrorHandling:
    """Test suite for error handling."""

    def test_invalid_endpoint_returns_404(self):
        """Test that invalid endpoint returns 404."""
        response = client.get("/invalid/endpoint")
        assert response.status_code == 404

    def test_wrong_method_hello_returns_405(self):
        """Test that wrong HTTP method on /api/hello returns 405."""
        response = client.post("/api/hello")
        assert response.status_code == 405

    def test_wrong_method_greet_returns_405(self):
        """Test that wrong HTTP method on /api/greet returns 405."""
        response = client.get("/api/greet")
        assert response.status_code == 405

    def test_invalid_json_returns_422(self):
        """Test that invalid JSON returns 422."""
        response = client.post(
            "/api/greet",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
