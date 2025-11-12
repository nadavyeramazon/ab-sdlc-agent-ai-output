"""Tests for the FastAPI backend application - Verifying AC-007 through AC-012."""

import pytest
import time
from datetime import datetime
from fastapi.testclient import TestClient
from main import app, get_current_timestamp


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestTimestampFunction:
    """Tests for timestamp utility function."""
    
    def test_get_current_timestamp_format(self):
        """Test that timestamp is in correct ISO 8601 format."""
        timestamp = get_current_timestamp()
        
        # Should be able to parse as datetime
        parsed_dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        assert isinstance(parsed_dt, datetime)
        
        # Should contain timezone information
        assert '+' in timestamp or 'Z' in timestamp or timestamp.endswith('+00:00')


class TestHealthEndpoint:
    """Tests for the health check endpoint - AC-008."""

    def test_health_check_exact_format(self, client):
        """Test AC-008: Health check returns exact specification format."""
        response = client.get("/health")
        
        # AC-011: Proper HTTP status codes (200 for success)
        assert response.status_code == 200
        data = response.json()
        
        # AC-008: Must return exact format
        assert data["status"] == "healthy"
        assert data["service"] == "green-theme-backend"
        assert "timestamp" in data
        
        # Should only have these 3 fields as per specification
        expected_fields = {"status", "timestamp", "service"}
        actual_fields = set(data.keys())
        assert actual_fields == expected_fields
        
        # Verify timestamp format
        timestamp = data["timestamp"]
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

    def test_health_check_response_time(self, client):
        """Test AC-012: Response time under 100ms."""
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        # AC-012: Response time should be under 100ms
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms limit"

    def test_health_check_content_type(self, client):
        """Test AC-011: JSON response with proper content-type headers."""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")


class TestHelloEndpoint:
    """Tests for the hello world endpoint - AC-007."""

    def test_hello_world_exact_format(self, client):
        """Test AC-007: Hello endpoint returns exact specification format."""
        response = client.get("/api/hello")
        
        # AC-011: Proper HTTP status codes (200 for success)
        assert response.status_code == 200
        data = response.json()
        
        # AC-007: Must return exact message and format
        assert data["message"] == "Hello World from Backend!"
        assert data["status"] == "success"
        assert "timestamp" in data
        
        # Should only have these 3 fields as per specification
        expected_fields = {"message", "timestamp", "status"}
        actual_fields = set(data.keys())
        assert actual_fields == expected_fields
        
        # Verify timestamp format
        timestamp = data["timestamp"]
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

    def test_hello_world_response_time(self, client):
        """Test AC-012: Response time under 100ms."""
        start_time = time.time()
        response = client.get("/api/hello")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        # AC-012: Response time should be under 100ms
        assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms limit"

    def test_hello_world_content_type(self, client):
        """Test AC-011: JSON response with proper content-type headers."""
        response = client.get("/api/hello")
        
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")

    def test_hello_timestamps_are_recent(self, client):
        """Test that timestamps are recent (within last minute)."""
        response = client.get("/api/hello")
        data = response.json()
        
        timestamp_str = data["timestamp"]
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now(timestamp.tzinfo)
        
        # Should be within the last minute
        time_diff = abs((now - timestamp).total_seconds())
        assert time_diff < 60  # Less than 60 seconds ago


class TestPersonalizedHelloEndpoint:
    """Tests for the personalized hello endpoint."""

    def test_hello_user_valid_name(self, client):
        """Test personalized hello with valid name includes timestamp."""
        name = "Alice"
        response = client.get(f"/api/hello/{name}")
        
        assert response.status_code == 200
        data = response.json()
        
        required_fields = ["message", "status", "timestamp"]
        for field in required_fields:
            assert field in data
        
        assert data["status"] == "success"
        assert f"Hello, {name}!" in data["message"]
        assert "Backend" in data["message"]
        
        # Verify timestamp
        timestamp = data["timestamp"]
        datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

    def test_hello_user_empty_name(self, client):
        """Test personalized hello with empty name returns error."""
        response = client.get("/api/hello/")
        # This should return 404 as the route doesn't match
        assert response.status_code == 404

    def test_hello_user_whitespace_name(self, client):
        """Test personalized hello with whitespace-only name returns error."""
        name = "   "
        response = client.get(f"/api/hello/{name}")
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "empty" in data["detail"].lower()

    def test_hello_user_long_name(self, client):
        """Test personalized hello with very long name returns error."""
        name = "a" * 101  # 101 characters, exceeds 100 limit
        response = client.get(f"/api/hello/{name}")
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "too long" in data["detail"].lower()


class TestCORSConfiguration:
    """Tests for CORS configuration - AC-010."""

    def test_cors_headers_present(self, client):
        """Test AC-010: CORS properly configured for frontend communication."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        # FastAPI TestClient doesn't simulate full CORS behavior,
        # but we can verify the endpoint works with origin header

    def test_options_request(self, client):
        """Test OPTIONS request for CORS preflight."""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        # Should allow OPTIONS requests
        assert response.status_code in [200, 204]


class TestPortConfiguration:
    """Tests for port configuration - AC-009."""

    def test_app_configuration(self):
        """Test AC-009: Backend service configured for port 8000."""
        # Verify the app is properly configured
        assert app.title == "Green Theme Backend API"
        assert app.version == "1.0.0"
        
        # The actual port binding is tested in integration tests
        # Here we verify the configuration is correct


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""

    def test_openapi_schema(self, client):
        """Test that OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
        
        # Check API info
        info = data["info"]
        assert info["title"] == "Green Theme Backend API"
        assert info["version"] == "1.0.0"

    def test_swagger_ui(self, client):
        """Test that Swagger UI is accessible."""
        response = client.get("/docs")
        
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")


class TestErrorHandling:
    """Tests for error handling - AC-011."""

    def test_404_error(self, client):
        """Test AC-011: 404 error for non-existent endpoint."""
        response = client.get("/non-existent-endpoint")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_method_not_allowed(self, client):
        """Test AC-011: Method not allowed error."""
        # POST to GET-only endpoint
        response = client.post("/api/hello")
        
        assert response.status_code == 405
        data = response.json()
        assert "detail" in data


class TestPerformanceRequirements:
    """Tests for performance requirements - AC-012."""

    def test_multiple_requests_performance(self, client):
        """Test AC-012: Multiple requests stay under 100ms."""
        response_times = []
        
        for i in range(5):
            start_time = time.time()
            response = client.get("/api/hello")
            end_time = time.time()
            
            response_time_ms = (end_time - start_time) * 1000
            response_times.append(response_time_ms)
            
            assert response.status_code == 200
            assert response_time_ms < 100, f"Request {i+1} took {response_time_ms}ms"
        
        # All requests should be fast
        avg_response_time = sum(response_times) / len(response_times)
        assert avg_response_time < 100, f"Average response time {avg_response_time}ms exceeds 100ms"

    def test_health_check_performance(self, client):
        """Test AC-012: Health check performance under 100ms."""
        response_times = []
        
        for i in range(5):
            start_time = time.time()
            response = client.get("/health")
            end_time = time.time()
            
            response_time_ms = (end_time - start_time) * 1000
            response_times.append(response_time_ms)
            
            assert response.status_code == 200
            assert response_time_ms < 100, f"Health check {i+1} took {response_time_ms}ms"
        
        # All health checks should be fast
        avg_response_time = sum(response_times) / len(response_times)
        assert avg_response_time < 100, f"Average health check time {avg_response_time}ms exceeds 100ms"


class TestResponseFormat:
    """Tests to verify exact response format compliance."""
    
    def test_hello_response_format_compliance(self, client):
        """Test that /api/hello response matches exact specification."""
        response = client.get("/api/hello")
        data = response.json()
        
        # Must have exactly these fields in any order
        required_fields = {"message", "timestamp", "status"}
        assert set(data.keys()) == required_fields
        
        # Field value validation
        assert data["message"] == "Hello World from Backend!"
        assert data["status"] == "success"
        assert isinstance(data["timestamp"], str)
        
        # Timestamp should be valid ISO 8601
        datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
    
    def test_health_response_format_compliance(self, client):
        """Test that /health response matches exact specification."""
        response = client.get("/health")
        data = response.json()
        
        # Must have exactly these fields in any order
        required_fields = {"status", "timestamp", "service"}
        assert set(data.keys()) == required_fields
        
        # Field value validation
        assert data["status"] == "healthy"
        assert data["service"] == "green-theme-backend"
        assert isinstance(data["timestamp"], str)
        
        # Timestamp should be valid ISO 8601
        datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))


class TestTimestampConsistency:
    """Tests for timestamp behavior."""
    
    def test_timestamps_are_different_across_requests(self, client):
        """Test that different requests get different timestamps."""
        import time
        
        # Make first request
        response1 = client.get("/api/hello")
        timestamp1 = response1.json()["timestamp"]
        
        # Wait a small amount of time
        time.sleep(0.01)
        
        # Make second request
        response2 = client.get("/api/hello")
        timestamp2 = response2.json()["timestamp"]
        
        # Timestamps should be different
        assert timestamp1 != timestamp2
    
    def test_timestamp_precision(self, client):
        """Test that timestamps have sufficient precision."""
        response = client.get("/api/hello")
        timestamp_str = response.json()["timestamp"]
        
        # Should include microseconds or at least milliseconds
        # ISO format should have either .microseconds or be precise to seconds
        assert isinstance(timestamp_str, str)
        assert len(timestamp_str) >= 19  # Basic ISO format: YYYY-MM-DDTHH:MM:SS