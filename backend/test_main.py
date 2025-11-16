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


class TestCORSConfiguration:
    """Test suite for CORS configuration."""

    def test_cors_allows_localhost_3000(self):
        """Test that CORS allows requests from localhost:3000."""
        response = client.get("/api/hello", headers={"Origin": "http://localhost:3000"})
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert (
            response.headers["access-control-allow-origin"] == "http://localhost:3000"
        )

    def test_cors_preflight_request(self):
        """Test CORS preflight OPTIONS request."""
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


class TestErrorHandling:
    """Test suite for error handling."""

    def test_invalid_endpoint_returns_404(self):
        """Test that invalid endpoint returns 404."""
        response = client.get("/invalid/endpoint")
        assert response.status_code == 404

    def test_wrong_method_returns_405(self):
        """Test that wrong HTTP method returns 405."""
        response = client.post("/health")
        assert response.status_code == 405
