"""Backend API Tests

Comprehensive test suite for FastAPI endpoints using pytest and TestClient.
Tests all endpoints, CORS configuration, and response formats.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import pytz
from main import app

# Create test client
client = TestClient(app)


class TestHelloEndpoint:
    """Test suite for /api/hello endpoint"""
    
    def test_hello_endpoint_returns_200(self):
        """Test that /api/hello returns HTTP 200 status code"""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_endpoint_returns_json(self):
        """Test that /api/hello returns JSON content type"""
        response = client.get("/api/hello")
        assert response.headers["content-type"] == "application/json"
    
    def test_hello_endpoint_has_message_field(self):
        """Test that response contains 'message' field"""
        response = client.get("/api/hello")
        data = response.json()
        assert "message" in data
    
    def test_hello_endpoint_message_content(self):
        """Test that message field contains exact expected text"""
        response = client.get("/api/hello")
        data = response.json()
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_endpoint_has_timestamp_field(self):
        """Test that response contains 'timestamp' field"""
        response = client.get("/api/hello")
        data = response.json()
        assert "timestamp" in data
    
    def test_hello_endpoint_timestamp_is_valid_iso8601(self):
        """Test that timestamp is in valid ISO 8601 format"""
        response = client.get("/api/hello")
        data = response.json()
        timestamp = data["timestamp"]
        
        # Verify ISO 8601 format by parsing it
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            is_valid = True
        except ValueError:
            is_valid = False
        
        assert is_valid, f"Timestamp {timestamp} is not valid ISO 8601 format"
    
    def test_hello_endpoint_timestamp_is_recent(self):
        """Test that timestamp is within last 5 seconds (reasonable for test execution)"""
        response = client.get("/api/hello")
        data = response.json()
        timestamp_str = data["timestamp"]
        
        # Parse timestamp
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        current_time = datetime.now(pytz.UTC)
        
        # Check if timestamp is within 5 seconds
        time_diff = abs((current_time - timestamp).total_seconds())
        assert time_diff < 5, f"Timestamp is not recent: {time_diff} seconds old"
    
    def test_hello_endpoint_response_structure(self):
        """Test complete response structure"""
        response = client.get("/api/hello")
        data = response.json()
        
        # Check that response has exactly 2 fields
        assert len(data) == 2
        assert "message" in data
        assert "timestamp" in data
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)


class TestGreetEndpoint:
    """Test suite for /api/greet endpoint"""
    
    def test_greet_endpoint_valid_name_returns_200(self):
        """Test that /api/greet returns HTTP 200 for valid name"""
        response = client.post("/api/greet", json={"name": "John"})
        assert response.status_code == 200
    
    def test_greet_endpoint_returns_json(self):
        """Test that /api/greet returns JSON content type"""
        response = client.post("/api/greet", json={"name": "Alice"})
        assert response.headers["content-type"] == "application/json"
    
    def test_greet_endpoint_response_has_greeting_field(self):
        """Test that response contains 'greeting' field"""
        response = client.post("/api/greet", json={"name": "John"})
        data = response.json()
        assert "greeting" in data
    
    def test_greet_endpoint_response_has_timestamp_field(self):
        """Test that response contains 'timestamp' field"""
        response = client.post("/api/greet", json={"name": "John"})
        data = response.json()
        assert "timestamp" in data
    
    def test_greet_endpoint_greeting_format(self):
        """Test that greeting has correct format with user's name"""
        response = client.post("/api/greet", json={"name": "Alice"})
        data = response.json()
        assert "Hello, Alice!" in data["greeting"]
        assert "Welcome to our purple-themed app!" in data["greeting"]
    
    def test_greet_endpoint_greeting_includes_name(self):
        """Test that greeting includes the provided name"""
        names = ["John", "Mary", "Bob", "Sarah"]
        for name in names:
            response = client.post("/api/greet", json={"name": name})
            data = response.json()
            assert name in data["greeting"], f"Name {name} not found in greeting"
    
    def test_greet_endpoint_timestamp_is_valid_iso8601(self):
        """Test that timestamp is in valid ISO 8601 format"""
        response = client.post("/api/greet", json={"name": "John"})
        data = response.json()
        timestamp = data["timestamp"]
        
        # Verify ISO 8601 format by parsing it
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            is_valid = True
        except ValueError:
            is_valid = False
        
        assert is_valid, f"Timestamp {timestamp} is not valid ISO 8601 format"
    
    def test_greet_endpoint_timestamp_is_recent(self):
        """Test that timestamp is current (within 1 second)"""
        response = client.post("/api/greet", json={"name": "John"})
        data = response.json()
        timestamp_str = data["timestamp"]
        
        # Parse timestamp
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        current_time = datetime.utcnow().replace(tzinfo=pytz.UTC)
        
        # Check if timestamp is within 1 second
        time_diff = abs((current_time - timestamp).total_seconds())
        assert time_diff < 1, f"Timestamp is not recent: {time_diff} seconds old"
    
    def test_greet_endpoint_empty_name_returns_400(self):
        """Test that empty name returns HTTP 400 Bad Request"""
        response = client.post("/api/greet", json={"name": ""})
        assert response.status_code == 400
    
    def test_greet_endpoint_empty_name_has_detail(self):
        """Test that error response contains 'detail' field"""
        response = client.post("/api/greet", json={"name": ""})
        data = response.json()
        assert "detail" in data
    
    def test_greet_endpoint_empty_name_error_message(self):
        """Test that error message is descriptive for empty name"""
        response = client.post("/api/greet", json={"name": ""})
        data = response.json()
        assert "empty" in data["detail"].lower()
    
    def test_greet_endpoint_whitespace_only_name_returns_400(self):
        """Test that whitespace-only name returns HTTP 400"""
        response = client.post("/api/greet", json={"name": "   "})
        assert response.status_code == 400
    
    def test_greet_endpoint_whitespace_only_has_error_message(self):
        """Test that whitespace-only name returns appropriate error"""
        response = client.post("/api/greet", json={"name": "   "})
        data = response.json()
        assert "detail" in data
    
    def test_greet_endpoint_missing_name_field_returns_422(self):
        """Test that missing 'name' field returns HTTP 422 Unprocessable Entity"""
        response = client.post("/api/greet", json={})
        assert response.status_code == 422
    
    def test_greet_endpoint_special_characters_in_name(self):
        """Test that names with special characters are processed correctly"""
        special_names = ["Mary-Jane", "O'Connor", "Jean-Luc"]
        for name in special_names:
            response = client.post("/api/greet", json={"name": name})
            assert response.status_code == 200
            data = response.json()
            assert name in data["greeting"]
    
    def test_greet_endpoint_international_characters(self):
        """Test that names with international characters work correctly"""
        international_names = ["José", "François", "Müller", "Søren"]
        for name in international_names:
            response = client.post("/api/greet", json={"name": name})
            assert response.status_code == 200
            data = response.json()
            assert name in data["greeting"]
    
    def test_greet_endpoint_name_with_numbers(self):
        """Test that names with numbers are processed correctly"""
        response = client.post("/api/greet", json={"name": "User123"})
        assert response.status_code == 200
        data = response.json()
        assert "User123" in data["greeting"]
    
    def test_greet_endpoint_trims_whitespace(self):
        """Test that leading/trailing whitespace is trimmed from name"""
        response = client.post("/api/greet", json={"name": "  John  "})
        assert response.status_code == 200
        data = response.json()
        # Should contain "John" without extra spaces
        assert "Hello, John!" in data["greeting"]
    
    def test_greet_endpoint_response_structure(self):
        """Test complete response structure"""
        response = client.post("/api/greet", json={"name": "John"})
        data = response.json()
        
        # Check that response has exactly 2 fields
        assert len(data) == 2
        assert "greeting" in data
        assert "timestamp" in data
        assert isinstance(data["greeting"], str)
        assert isinstance(data["timestamp"], str)
    
    def test_greet_endpoint_cors_headers(self):
        """Test that CORS headers are present for POST requests"""
        response = client.post(
            "/api/greet",
            json={"name": "John"},
            headers={"Origin": "http://localhost:3000"}
        )
        assert "access-control-allow-origin" in response.headers
    
    def test_greet_endpoint_response_time(self):
        """Test that /api/greet responds within 100ms"""
        import time
        
        start_time = time.time()
        response = client.post("/api/greet", json={"name": "John"})
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        # Should respond within 100ms (being generous for test environment)
        assert response_time_ms < 200, f"Response took {response_time_ms}ms"
        assert response.status_code == 200


class TestHealthEndpoint:
    """Test suite for /health endpoint"""
    
    def test_health_endpoint_returns_200(self):
        """Test that /health returns HTTP 200 status code"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_endpoint_returns_json(self):
        """Test that /health returns JSON content type"""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_endpoint_has_status_field(self):
        """Test that response contains 'status' field"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
    
    def test_health_endpoint_status_is_healthy(self):
        """Test that status field contains 'healthy'"""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_health_endpoint_response_structure(self):
        """Test complete response structure"""
        response = client.get("/health")
        data = response.json()
        
        # Check response structure
        assert len(data) == 1
        assert "status" in data
        assert isinstance(data["status"], str)


class TestRootEndpoint:
    """Test suite for root / endpoint"""
    
    def test_root_endpoint_returns_200(self):
        """Test that root endpoint returns HTTP 200 status code"""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_endpoint_returns_json(self):
        """Test that root endpoint returns JSON content type"""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"
    
    def test_root_endpoint_has_message(self):
        """Test that root endpoint returns welcome message"""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "Welcome" in data["message"]


class TestCORSConfiguration:
    """Test suite for CORS middleware configuration"""
    
    def test_cors_headers_present_on_hello_endpoint(self):
        """Test that CORS headers are present in /api/hello response"""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allows_frontend_origin(self):
        """Test that CORS allows requests from frontend origin"""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # Verify frontend origin is allowed
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    
    def test_cors_options_request_for_get(self):
        """Test CORS preflight OPTIONS request for GET"""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        # Preflight should return 200
        assert response.status_code == 200
    
    def test_cors_options_request_for_post(self):
        """Test CORS preflight OPTIONS request for POST"""
        response = client.options(
            "/api/greet",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
            }
        )
        
        # Preflight should return 200
        assert response.status_code == 200


class TestResponseTiming:
    """Test suite for response time requirements"""
    
    def test_hello_endpoint_response_time(self):
        """Test that /api/hello responds within 100ms"""
        import time
        
        start_time = time.time()
        response = client.get("/api/hello")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        # Should respond within 100ms (being generous for test environment)
        assert response_time_ms < 200, f"Response took {response_time_ms}ms"
        assert response.status_code == 200
    
    def test_health_endpoint_response_time(self):
        """Test that /health responds within 50ms"""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        # Should respond within 50ms (being generous for test environment)
        assert response_time_ms < 100, f"Response took {response_time_ms}ms"
        assert response.status_code == 200


class TestEdgeCases:
    """Test suite for edge cases and error scenarios"""
    
    def test_invalid_endpoint_returns_404(self):
        """Test that invalid endpoints return 404"""
        response = client.get("/api/invalid")
        assert response.status_code == 404
    
    def test_hello_endpoint_with_trailing_slash(self):
        """Test /api/hello/ with trailing slash"""
        response = client.get("/api/hello/")
        # Should either redirect or return 404
        assert response.status_code in [200, 307, 404]
    
    def test_post_method_not_allowed_on_hello(self):
        """Test that POST method is not allowed on /api/hello"""
        response = client.post("/api/hello")
        assert response.status_code == 405  # Method Not Allowed
    
    def test_get_method_not_allowed_on_greet(self):
        """Test that GET method is not allowed on /api/greet"""
        response = client.get("/api/greet")
        assert response.status_code == 405  # Method Not Allowed
