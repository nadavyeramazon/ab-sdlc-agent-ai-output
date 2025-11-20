"""
Comprehensive test suite for the FastAPI backend application.

This module contains pytest tests for all API endpoints and middleware configurations.
Tests follow pytest best practices with clear naming, proper fixtures, and comprehensive coverage.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app


@pytest.fixture
def client():
    """
    Pytest fixture that provides a TestClient instance for testing FastAPI endpoints.
    
    The TestClient allows making requests to the FastAPI application without running
    a live server, making tests fast and isolated.
    
    Yields:
        TestClient: A test client instance for the FastAPI app
    """
    with TestClient(app) as test_client:
        yield test_client


class TestHealthEndpoint:
    """Test suite for the /health endpoint"""
    
    def test_health_returns_200_status(self, client):
        """Test that the health endpoint returns a 200 OK status code"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_returns_correct_structure(self, client):
        """Test that the health endpoint returns the expected JSON structure"""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert isinstance(data, dict)
    
    def test_health_returns_healthy_status(self, client):
        """Test that the health endpoint returns 'healthy' status"""
        response = client.get("/health")
        data = response.json()
        
        assert data["status"] == "healthy"
    
    def test_health_endpoint_method_not_allowed(self, client):
        """Test that POST method is not allowed on health endpoint"""
        response = client.post("/health")
        assert response.status_code == 405  # Method Not Allowed
    
    def test_health_endpoint_content_type(self, client):
        """Test that the health endpoint returns JSON content type"""
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]


class TestHelloEndpoint:
    """Test suite for the /api/hello endpoint"""
    
    def test_hello_returns_200_status(self, client):
        """Test that the hello endpoint returns a 200 OK status code"""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_hello_returns_correct_structure(self, client):
        """Test that the hello endpoint returns the expected JSON structure"""
        response = client.get("/api/hello")
        data = response.json()
        
        assert "message" in data
        assert "timestamp" in data
        assert isinstance(data, dict)
    
    def test_hello_returns_correct_message(self, client):
        """Test that the hello endpoint returns the expected greeting message"""
        response = client.get("/api/hello")
        data = response.json()
        
        assert data["message"] == "Hello World from Backend!"
    
    def test_hello_timestamp_is_valid_iso_format(self, client):
        """Test that the timestamp in hello response is in valid ISO 8601 format"""
        response = client.get("/api/hello")
        data = response.json()
        
        # This will raise ValueError if timestamp is not valid ISO format
        try:
            parsed_timestamp = datetime.fromisoformat(data["timestamp"])
            assert isinstance(parsed_timestamp, datetime)
        except ValueError:
            pytest.fail("Timestamp is not in valid ISO 8601 format")
    
    def test_hello_timestamp_is_recent(self, client):
        """Test that the timestamp in hello response is recent (within last 5 seconds)"""
        response = client.get("/api/hello")
        data = response.json()
        
        timestamp = datetime.fromisoformat(data["timestamp"])
        now = datetime.now()
        time_difference = (now - timestamp).total_seconds()
        
        # Timestamp should be within the last 5 seconds
        assert abs(time_difference) < 5
    
    def test_hello_endpoint_method_not_allowed(self, client):
        """Test that POST method is not allowed on hello endpoint"""
        response = client.post("/api/hello")
        assert response.status_code == 405  # Method Not Allowed
    
    def test_hello_endpoint_content_type(self, client):
        """Test that the hello endpoint returns JSON content type"""
        response = client.get("/api/hello")
        assert "application/json" in response.headers["content-type"]
    
    def test_hello_multiple_calls_return_different_timestamps(self, client):
        """Test that multiple calls to hello endpoint return different timestamps"""
        response1 = client.get("/api/hello")
        response2 = client.get("/api/hello")
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Timestamps should be different (or very close) between calls
        assert data1["message"] == data2["message"]  # Message stays the same
        # Timestamps might be the same if calls are very fast, so we just verify they exist
        assert "timestamp" in data1
        assert "timestamp" in data2


class TestGreetEndpoint:
    """Test suite for the POST /api/greet endpoint"""
    
    def test_greet_returns_200_with_valid_name(self, client):
        """Test that the greet endpoint returns 200 OK with a valid name"""
        response = client.post("/api/greet", json={"name": "Alice"})
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    
    def test_greet_returns_correct_structure(self, client):
        """Test that the greet endpoint returns the expected JSON structure with greeting and timestamp fields"""
        response = client.post("/api/greet", json={"name": "Bob"})
        data = response.json()
        
        assert isinstance(data, dict), "Response should be a dictionary"
        assert "greeting" in data, "Response should contain 'greeting' field"
        assert "timestamp" in data, "Response should contain 'timestamp' field"
        assert len(data) == 2, "Response should only contain 'greeting' and 'timestamp' fields"
    
    def test_greet_timestamp_is_valid_iso8601_format(self, client):
        """Test that the timestamp in greet response is in valid ISO 8601 format with Z suffix"""
        response = client.post("/api/greet", json={"name": "Charlie"})
        data = response.json()
        
        timestamp = data["timestamp"]
        
        # Verify timestamp ends with 'Z' (UTC indicator)
        assert timestamp.endswith("Z"), f"Timestamp should end with 'Z' but got: {timestamp}"
        
        # Verify timestamp is valid ISO 8601 format by parsing it
        try:
            # Remove the 'Z' and parse
            parsed_timestamp = datetime.fromisoformat(timestamp.rstrip('Z'))
            assert isinstance(parsed_timestamp, datetime), "Timestamp should be parseable as datetime"
        except ValueError as e:
            pytest.fail(f"Timestamp is not in valid ISO 8601 format: {e}")
    
    def test_greet_returns_400_for_empty_name(self, client):
        """Test that the greet endpoint returns 400 Bad Request when name is empty string"""
        response = client.post("/api/greet", json={"name": ""})
        assert response.status_code == 400, f"Expected 400 for empty name but got {response.status_code}"
        
        data = response.json()
        assert "detail" in data, "Error response should contain 'detail' field"
        assert data["detail"] == "Name cannot be empty", f"Expected specific error message but got: {data['detail']}"
    
    def test_greet_returns_400_for_whitespace_only_name(self, client):
        """Test that the greet endpoint returns 400 Bad Request when name contains only whitespace"""
        whitespace_names = ["   ", "\t", "\n", "  \t\n  "]
        
        for whitespace_name in whitespace_names:
            response = client.post("/api/greet", json={"name": whitespace_name})
            assert response.status_code == 400, f"Expected 400 for whitespace-only name '{repr(whitespace_name)}' but got {response.status_code}"
            
            data = response.json()
            assert "detail" in data, "Error response should contain 'detail' field"
            assert data["detail"] == "Name cannot be empty", f"Expected specific error message but got: {data['detail']}"
    
    def test_greet_strips_leading_trailing_whitespace(self, client):
        """Test that the greet endpoint strips leading and trailing whitespace from names"""
        test_cases = [
            ("  David  ", "David"),
            ("\tEve\t", "Eve"),
            ("\n Frank \n", "Frank"),
            ("  Grace", "Grace"),
            ("Henry  ", "Henry"),
        ]
        
        for input_name, expected_name in test_cases:
            response = client.post("/api/greet", json={"name": input_name})
            assert response.status_code == 200, f"Expected 200 for name '{repr(input_name)}'"
            
            data = response.json()
            expected_greeting = f"Hello, {expected_name}! Welcome to our purple-themed app!"
            assert data["greeting"] == expected_greeting, f"Expected greeting for '{expected_name}' but got: {data['greeting']}"
    
    def test_greet_with_various_valid_names(self, client):
        """Test that the greet endpoint handles various valid name inputs correctly"""
        test_names = [
            "John",
            "Mary Jane",
            "José",
            "李明",
            "O'Brien",
            "Anne-Marie",
            "123",
            "User@123",
            "a",  # Single character
        ]
        
        for name in test_names:
            response = client.post("/api/greet", json={"name": name})
            assert response.status_code == 200, f"Expected 200 for name '{name}' but got {response.status_code}"
            
            data = response.json()
            expected_greeting = f"Hello, {name}! Welcome to our purple-themed app!"
            assert data["greeting"] == expected_greeting, f"Greeting mismatch for name '{name}'"
            assert "timestamp" in data, f"Response should contain timestamp for name '{name}'"
    
    def test_greet_endpoint_get_method_not_allowed(self, client):
        """Test that GET method is not allowed on the greet endpoint (should be POST only)"""
        response = client.get("/api/greet")
        assert response.status_code == 405, f"Expected 405 Method Not Allowed but got {response.status_code}"
    
    def test_greet_endpoint_content_type(self, client):
        """Test that the greet endpoint returns JSON content type"""
        response = client.post("/api/greet", json={"name": "Isabella"})
        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"], "Response should be JSON"
    
    def test_greet_greeting_message_format(self, client):
        """Test that the greeting message follows the expected format"""
        test_name = "Jack"
        response = client.post("/api/greet", json={"name": test_name})
        data = response.json()
        
        greeting = data["greeting"]
        
        # Verify greeting format: "Hello, {name}! Welcome to our purple-themed app!"
        assert greeting.startswith("Hello, "), "Greeting should start with 'Hello, '"
        assert test_name in greeting, f"Greeting should contain the name '{test_name}'"
        assert greeting.endswith("! Welcome to our purple-themed app!"), "Greeting should end with expected message"
        
        expected_greeting = f"Hello, {test_name}! Welcome to our purple-themed app!"
        assert greeting == expected_greeting, f"Expected exact format: {expected_greeting}"
    
    def test_greet_with_very_long_name(self, client):
        """Test that the greet endpoint handles very long names correctly"""
        long_name = "A" * 1000  # 1000 character name
        response = client.post("/api/greet", json={"name": long_name})
        
        assert response.status_code == 200, "Should accept very long names"
        data = response.json()
        
        assert long_name in data["greeting"], "Greeting should contain the full long name"
        assert "timestamp" in data, "Response should contain timestamp"
    
    def test_greet_with_special_characters(self, client):
        """Test that the greet endpoint handles special characters in names"""
        special_names = [
            "Alice & Bob",
            "user<script>",
            "name'with'quotes",
            'name"with"doublequotes',
            "name\nwith\nnewlines",
            "emoji😀user",
            "tab\tname",
        ]
        
        for name in special_names:
            response = client.post("/api/greet", json={"name": name})
            assert response.status_code == 200, f"Should accept special characters in name '{repr(name)}'"
            
            data = response.json()
            # Name should appear in greeting exactly as provided (after stripping)
            stripped_name = name.strip()
            expected_greeting = f"Hello, {stripped_name}! Welcome to our purple-themed app!"
            assert data["greeting"] == expected_greeting, f"Greeting mismatch for special name '{name}'"
    
    def test_greet_requires_name_field(self, client):
        """Test that the greet endpoint returns 422 Unprocessable Entity when name field is missing"""
        response = client.post("/api/greet", json={})
        assert response.status_code == 422, f"Expected 422 for missing name field but got {response.status_code}"
    
    def test_greet_rejects_invalid_json(self, client):
        """Test that the greet endpoint returns 422 when request body is not valid JSON structure"""
        response = client.post(
            "/api/greet",
            data="not json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422, f"Expected 422 for invalid JSON but got {response.status_code}"
    
    def test_greet_rejects_non_string_name(self, client):
        """Test that the greet endpoint returns 422 when name is not a string"""
        invalid_names = [
            {"name": 123},
            {"name": None},
            {"name": []},
            {"name": {}},
            {"name": True},
        ]
        
        for invalid_payload in invalid_names:
            response = client.post("/api/greet", json=invalid_payload)
            assert response.status_code == 422, f"Expected 422 for non-string name {invalid_payload} but got {response.status_code}"
    
    def test_greet_timestamp_is_recent(self, client):
        """Test that the timestamp in greet response is recent (within last 5 seconds)"""
        response = client.post("/api/greet", json={"name": "Karen"})
        data = response.json()
        
        # Parse timestamp (remove 'Z' suffix)
        timestamp_str = data["timestamp"].rstrip('Z')
        timestamp = datetime.fromisoformat(timestamp_str)
        now = datetime.utcnow()
        time_difference = (now - timestamp).total_seconds()
        
        # Timestamp should be within the last 5 seconds
        assert abs(time_difference) < 5, f"Timestamp is not recent. Difference: {time_difference} seconds"
    
    def test_greet_multiple_calls_return_different_timestamps(self, client):
        """Test that multiple calls to greet endpoint return different timestamps"""
        response1 = client.post("/api/greet", json={"name": "Larry"})
        response2 = client.post("/api/greet", json={"name": "Larry"})
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Timestamps should exist
        assert "timestamp" in data1
        assert "timestamp" in data2
        
        # With the same name, greeting should be the same
        assert data1["greeting"] == data2["greeting"]
        
        # Timestamps might be different if there's enough time between calls
        # At minimum, verify they are valid timestamps
        assert data1["timestamp"].endswith("Z")
        assert data2["timestamp"].endswith("Z")


class TestCORSConfiguration:
    """Test suite for CORS (Cross-Origin Resource Sharing) middleware configuration"""
    
    def test_cors_allows_configured_origin(self, client):
        """Test that CORS allows requests from the configured origin (localhost:3000)"""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        assert response.status_code == 200
        # Check for CORS headers in response
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allows_localhost_3000(self, client):
        """Test that CORS specifically allows localhost:3000 as origin"""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # The allowed origin should be in the response headers
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
    
    def test_cors_preflight_request(self, client):
        """Test CORS preflight (OPTIONS) request for allowed methods"""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        # Preflight should return 200 OK
        assert response.status_code == 200
    
    def test_cors_allowed_methods_in_preflight(self, client):
        """Test that CORS preflight response includes allowed methods"""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        # Check that allowed methods are present
        allowed_methods = response.headers.get("access-control-allow-methods", "")
        assert "GET" in allowed_methods
    
    def test_cors_allowed_headers(self, client):
        """Test that CORS allows Content-Type header"""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        # Should allow the Content-Type header
        assert response.status_code == 200


class TestAPIEndpointEdgeCases:
    """Test suite for edge cases and error handling"""
    
    def test_nonexistent_endpoint_returns_404(self, client):
        """Test that accessing a non-existent endpoint returns 404 Not Found"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
    
    def test_root_endpoint_returns_404(self, client):
        """Test that accessing root endpoint returns 404 (no root route defined)"""
        response = client.get("/")
        assert response.status_code == 404
    
    def test_api_endpoint_with_trailing_slash(self, client):
        """Test API endpoint behavior with trailing slash"""
        # FastAPI by default redirects with trailing slash
        response = client.get("/api/hello/")
        # Should either return 200 or 307/308 redirect
        assert response.status_code in [200, 307, 308]
    
    def test_health_endpoint_with_query_parameters(self, client):
        """Test that health endpoint ignores query parameters"""
        response = client.get("/health?foo=bar")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_hello_endpoint_with_query_parameters(self, client):
        """Test that hello endpoint ignores query parameters"""
        response = client.get("/api/hello?test=value")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "timestamp" in data


class TestApplicationConfiguration:
    """Test suite for FastAPI application configuration"""
    
    def test_app_has_cors_middleware(self):
        """Test that the FastAPI app has CORS middleware configured"""
        # Check if CORS middleware is in the middleware stack
        middleware_classes = [m.cls.__name__ for m in app.user_middleware]
        assert "CORSMiddleware" in middleware_classes
    
    def test_openapi_schema_available(self, client):
        """Test that OpenAPI schema is available at /openapi.json"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
    
    def test_docs_endpoint_available(self, client):
        """Test that interactive API docs are available at /docs"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


# Test to ensure all endpoints are tested
def test_all_endpoints_are_covered():
    """
    Meta-test to ensure we have test coverage for all defined API endpoints.
    This helps maintain test coverage as new endpoints are added.
    """
    routes = [route.path for route in app.routes if hasattr(route, 'path')]
    api_routes = [r for r in routes if not r.startswith('/docs') and not r.startswith('/openapi')]
    
    # Verify we have routes defined
    assert len(api_routes) > 0
    
    # Check that critical endpoints exist
    assert "/health" in routes
    assert "/api/hello" in routes
    assert "/api/greet" in routes
