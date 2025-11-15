import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timezone
import re
from main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Tests for the /health endpoint"""
    
    def test_health_endpoint_returns_200(self):
        """Health endpoint should return 200 status code"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_endpoint_returns_json(self):
        """Health endpoint should return JSON content type"""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_endpoint_returns_correct_structure(self):
        """Health endpoint should return correct JSON structure"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_endpoint_response_schema(self):
        """Health endpoint response should match expected schema"""
        response = client.get("/health")
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 1  # Should only contain 'status' key
        assert isinstance(data["status"], str)


class TestHelloEndpoint:
    """Tests for the /api/hello endpoint"""
    
    def test_hello_endpoint_returns_200(self):
        """Hello endpoint should return 200 status code"""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_endpoint_returns_json(self):
        """Hello endpoint should return JSON content type"""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"
    
    def test_hello_endpoint_returns_correct_structure(self):
        """Hello endpoint should return correct JSON structure"""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
        assert "timestamp" in data
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_endpoint_timestamp_format(self):
        """Hello endpoint timestamp should be in ISO 8601 format with Z suffix"""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Check format: YYYY-MM-DDTHH:MM:SS.ffffffZ
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$'
        assert re.match(iso_pattern, timestamp), f"Timestamp {timestamp} doesn't match ISO 8601 format"
    
    def test_hello_endpoint_timestamp_is_recent(self):
        """Hello endpoint timestamp should be recent (within last 5 seconds)"""
        response = client.get("/api/hello")
        data = response.json()
        timestamp_str = data["timestamp"]
        
        # Parse timestamp (remove Z and parse)
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        
        # Timestamp should be within last 5 seconds
        time_diff = (now - timestamp).total_seconds()
        assert 0 <= time_diff <= 5, f"Timestamp is not recent: {time_diff} seconds ago"
    
    def test_hello_endpoint_response_schema(self):
        """Hello endpoint response should match expected schema"""
        response = client.get("/api/hello")
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 2  # Should contain 'message' and 'timestamp' keys
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)
    
    def test_hello_endpoint_multiple_calls_different_timestamps(self):
        """Multiple calls to hello endpoint should return different timestamps"""
        response1 = client.get("/api/hello")
        data1 = response1.json()
        
        # Small delay to ensure different timestamp
        import time
        time.sleep(0.01)
        
        response2 = client.get("/api/hello")
        data2 = response2.json()
        
        # Messages should be same but timestamps different
        assert data1["message"] == data2["message"]
        assert data1["timestamp"] != data2["timestamp"]


class TestCORSConfiguration:
    """Tests for CORS middleware configuration"""
    
    def test_cors_headers_present_on_hello_endpoint(self):
        """CORS headers should be present in response"""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allows_frontend_origin(self):
        """CORS should allow requests from frontend origin"""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    
    def test_cors_preflight_request(self):
        """CORS preflight OPTIONS request should be handled correctly"""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers


class TestAPIDocumentation:
    """Tests for FastAPI automatic documentation"""
    
    def test_openapi_schema_accessible(self):
        """OpenAPI schema should be accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
    
    def test_swagger_ui_accessible(self):
        """Swagger UI documentation should be accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_accessible(self):
        """ReDoc documentation should be accessible"""
        response = client.get("/redoc")
        assert response.status_code == 200


class TestErrorHandling:
    """Tests for error handling"""
    
    def test_invalid_endpoint_returns_404(self):
        """Invalid endpoint should return 404"""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404
    
    def test_invalid_method_returns_405(self):
        """Invalid HTTP method should return 405"""
        response = client.post("/health")
        assert response.status_code == 405
    
    def test_invalid_method_on_hello_returns_405(self):
        """POST to hello endpoint should return 405"""
        response = client.post("/api/hello")
        assert response.status_code == 405


class TestResponseTimes:
    """Tests for response time requirements"""
    
    def test_health_endpoint_fast_response(self):
        """Health endpoint should respond quickly"""
        import time
        start = time.time()
        response = client.get("/health")
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 0.1, f"Response too slow: {duration}s"
    
    def test_hello_endpoint_fast_response(self):
        """Hello endpoint should respond quickly"""
        import time
        start = time.time()
        response = client.get("/api/hello")
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 0.1, f"Response too slow: {duration}s"
