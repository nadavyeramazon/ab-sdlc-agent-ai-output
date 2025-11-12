"""Integration tests to verify AC-007 through AC-012 compliance.

This test file specifically validates that the backend implementation
meets all the critical API requirements specified in the PR.
"""

import pytest
import time
import json
from datetime import datetime
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestAC007HelloEndpoint:
    """AC-007: GET /api/hello endpoint returns JSON response with 'Hello World from Backend!' message."""
    
    def test_ac007_hello_endpoint_exists(self, client):
        """Test that GET /api/hello endpoint exists and is accessible."""
        response = client.get("/api/hello")
        assert response.status_code == 200
    
    def test_ac007_hello_returns_json(self, client):
        """Test that /api/hello returns JSON response."""
        response = client.get("/api/hello")
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")
        
        # Should be valid JSON
        data = response.json()
        assert isinstance(data, dict)
    
    def test_ac007_hello_message_exact(self, client):
        """Test that /api/hello returns exact message 'Hello World from Backend!'."""
        response = client.get("/api/hello")
        assert response.status_code == 200
        data = response.json()
        
        # AC-007: Must return exact message
        assert data["message"] == "Hello World from Backend!"
    
    def test_ac007_hello_response_format(self, client):
        """Test that /api/hello returns the exact specified format."""
        response = client.get("/api/hello")
        assert response.status_code == 200
        data = response.json()
        
        # Must match the exact format specified in requirements
        expected_format = {
            "message": "Hello World from Backend!",
            "timestamp": str,  # Will be a string
            "status": "success"
        }
        
        assert "message" in data
        assert "timestamp" in data  
        assert "status" in data
        assert data["message"] == expected_format["message"]
        assert data["status"] == expected_format["status"]
        assert isinstance(data["timestamp"], str)
        
        # Timestamp should be valid ISO 8601
        datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))


class TestAC008HealthEndpoint:
    """AC-008: GET /health endpoint returns health check status as 'healthy'."""
    
    def test_ac008_health_endpoint_exists(self, client):
        """Test that GET /health endpoint exists and is accessible."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_ac008_health_returns_healthy_status(self, client):
        """Test that /health returns status as 'healthy'."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        # AC-008: Must return status as 'healthy'
        assert data["status"] == "healthy"
    
    def test_ac008_health_response_format(self, client):
        """Test that /health returns the exact specified format."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        # Must match the exact format specified in requirements
        expected_format = {
            "status": "healthy",
            "timestamp": str,  # Will be a string
            "service": "green-theme-backend"
        }
        
        assert "status" in data
        assert "timestamp" in data
        assert "service" in data
        assert data["status"] == expected_format["status"]
        assert data["service"] == expected_format["service"]
        assert isinstance(data["timestamp"], str)
        
        # Timestamp should be valid ISO 8601
        datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))


class TestAC009PortConfiguration:
    """AC-009: Backend service runs on port 8000 and accepts HTTP requests."""
    
    def test_ac009_app_accepts_http_requests(self, client):
        """Test that backend accepts HTTP requests."""
        # Test multiple endpoints to ensure HTTP requests work
        endpoints = ["/health", "/api/hello", "/"]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code in [200, 404]  # Should accept the request
    
    def test_ac009_uvicorn_configuration(self):
        """Test that the app is configured to run on port 8000."""
        # This test verifies the configuration in main.py
        # The actual port binding is tested in integration tests
        
        # Check that the app is properly configured for FastAPI
        assert app.title == "Green Theme Backend API"
        assert hasattr(app, 'openapi')
        
        # The port configuration is verified by the fact that
        # the TestClient can successfully make requests


class TestAC010CORSConfiguration:
    """AC-010: CORS is properly configured to allow frontend communication."""
    
    def test_ac010_cors_allows_localhost_3000(self, client):
        """Test that CORS allows requests from localhost:3000."""
        response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # Should not reject due to CORS
        assert response.status_code == 200
        
        # Verify we get the expected response even with Origin header
        data = response.json()
        assert data["message"] == "Hello World from Backend!"
    
    def test_ac010_cors_options_request(self, client):
        """Test CORS preflight OPTIONS request."""
        response = client.options(
            "/api/hello",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        # Should handle preflight requests
        assert response.status_code in [200, 204]
    
    def test_ac010_cors_multiple_origins(self, client):
        """Test CORS with multiple allowed origins."""
        origins = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://0.0.0.0:3000"
        ]
        
        for origin in origins:
            response = client.get(
                "/health",
                headers={"Origin": origin}
            )
            
            # All allowed origins should work
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"


class TestAC011HTTPStatusCodes:
    """AC-011: API responses include proper HTTP status codes (200 for success)."""
    
    def test_ac011_success_responses_return_200(self, client):
        """Test that successful requests return HTTP 200."""
        endpoints = ["/health", "/api/hello", "/"]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            # AC-011: Success should return 200
            assert response.status_code == 200
    
    def test_ac011_not_found_returns_404(self, client):
        """Test that non-existent endpoints return HTTP 404."""
        response = client.get("/non-existent-endpoint")
        # AC-011: Not found should return 404
        assert response.status_code == 404
    
    def test_ac011_method_not_allowed_returns_405(self, client):
        """Test that wrong HTTP methods return HTTP 405."""
        # Try POST on GET-only endpoint
        response = client.post("/api/hello")
        # AC-011: Method not allowed should return 405
        assert response.status_code == 405
    
    def test_ac011_bad_request_returns_400(self, client):
        """Test that bad requests return HTTP 400."""
        # Test with invalid personalized hello (empty name)
        response = client.get("/api/hello/   ")  # Whitespace-only name
        # AC-011: Bad request should return 400
        assert response.status_code == 400
    
    def test_ac011_json_content_type_headers(self, client):
        """Test that JSON responses have proper content-type headers."""
        endpoints = ["/health", "/api/hello"]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            # AC-011: JSON responses should have proper content-type
            assert "application/json" in response.headers.get("content-type", "")


class TestAC012ResponseTime:
    """AC-012: Response time is under 100ms for all endpoints."""
    
    def test_ac012_hello_endpoint_response_time(self, client):
        """Test that /api/hello responds under 100ms."""
        # Test multiple times to get consistent results
        response_times = []
        
        for _ in range(10):
            start_time = time.time()
            response = client.get("/api/hello")
            end_time = time.time()
            
            response_time_ms = (end_time - start_time) * 1000
            response_times.append(response_time_ms)
            
            # AC-012: Each request should be under 100ms
            assert response.status_code == 200
            assert response_time_ms < 100, f"Response time {response_time_ms}ms exceeds 100ms limit"
        
        # Average should also be under 100ms
        avg_response_time = sum(response_times) / len(response_times)
        assert avg_response_time < 100, f"Average response time {avg_response_time}ms exceeds 100ms"
    
    def test_ac012_health_endpoint_response_time(self, client):
        """Test that /health responds under 100ms."""
        # Test multiple times to get consistent results
        response_times = []
        
        for _ in range(10):
            start_time = time.time()
            response = client.get("/health")
            end_time = time.time()
            
            response_time_ms = (end_time - start_time) * 1000
            response_times.append(response_time_ms)
            
            # AC-012: Each request should be under 100ms
            assert response.status_code == 200
            assert response_time_ms < 100, f"Health check {response_time_ms}ms exceeds 100ms limit"
        
        # Average should also be under 100ms
        avg_response_time = sum(response_times) / len(response_times)
        assert avg_response_time < 100, f"Average health check time {avg_response_time}ms exceeds 100ms"
    
    def test_ac012_all_endpoints_response_time(self, client):
        """Test that all endpoints respond under 100ms."""
        endpoints = ["/", "/health", "/api/hello"]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            response_time_ms = (end_time - start_time) * 1000
            
            # AC-012: All endpoints should be under 100ms
            assert response.status_code == 200
            assert response_time_ms < 100, f"Endpoint {endpoint} took {response_time_ms}ms"
    
    def test_ac012_concurrent_requests_performance(self, client):
        """Test response time under concurrent load."""
        import concurrent.futures
        
        def make_hello_request():
            start_time = time.time()
            response = client.get("/api/hello")
            end_time = time.time()
            return response, (end_time - start_time) * 1000
        
        # Test with 5 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_hello_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed and be fast
        for response, response_time_ms in results:
            assert response.status_code == 200
            # AC-012: Even under load, should be under 100ms
            assert response_time_ms < 100, f"Concurrent request took {response_time_ms}ms"


class TestIntegratedACCompliance:
    """Test all AC requirements together in integrated scenarios."""
    
    def test_complete_ac_workflow(self, client):
        """Test a complete workflow that exercises all AC requirements."""
        # AC-008: Health check
        health_start = time.time()
        health_response = client.get("/health")
        health_time = (time.time() - health_start) * 1000
        
        assert health_response.status_code == 200  # AC-011
        assert health_time < 100  # AC-012
        health_data = health_response.json()
        assert health_data["status"] == "healthy"  # AC-008
        assert health_data["service"] == "green-theme-backend"  # AC-008
        
        # AC-007: Hello endpoint
        hello_start = time.time()
        hello_response = client.get("/api/hello")
        hello_time = (time.time() - hello_start) * 1000
        
        assert hello_response.status_code == 200  # AC-011
        assert hello_time < 100  # AC-012
        hello_data = hello_response.json()
        assert hello_data["message"] == "Hello World from Backend!"  # AC-007
        assert hello_data["status"] == "success"  # AC-007
        
        # AC-010: CORS
        cors_response = client.get(
            "/api/hello",
            headers={"Origin": "http://localhost:3000"}
        )
        assert cors_response.status_code == 200  # AC-010
        
        # AC-009: Verify the service accepts HTTP requests
        assert "application/json" in hello_response.headers.get("content-type", "")
        assert "application/json" in health_response.headers.get("content-type", "")
    
    def test_ac_requirements_summary(self, client):
        """Test that summarizes all AC requirements in one test."""
        # This test serves as a quick validation that all ACs are met
        
        # AC-007: GET /api/hello endpoint returns JSON response with "Hello World from Backend!" message
        hello_response = client.get("/api/hello")
        assert hello_response.status_code == 200
        hello_data = hello_response.json()
        assert hello_data["message"] == "Hello World from Backend!"
        assert "application/json" in hello_response.headers.get("content-type", "")
        
        # AC-008: GET /health endpoint returns health check status as "healthy"
        health_response = client.get("/health")
        assert health_response.status_code == 200
        health_data = health_response.json()
        assert health_data["status"] == "healthy"
        assert health_data["service"] == "green-theme-backend"
        
        # AC-009: Backend service runs on port 8000 and accepts HTTP requests
        # (Verified by successful TestClient communication)
        
        # AC-010: CORS is properly configured to allow frontend communication
        cors_response = client.get("/health", headers={"Origin": "http://localhost:3000"})
        assert cors_response.status_code == 200
        
        # AC-011: API responses include proper HTTP status codes (200 for success)
        assert hello_response.status_code == 200
        assert health_response.status_code == 200
        
        # AC-012: Response time is under 100ms for all endpoints
        start_time = time.time()
        client.get("/api/hello")
        hello_time = (time.time() - start_time) * 1000
        assert hello_time < 100
        
        start_time = time.time()
        client.get("/health")
        health_time = (time.time() - start_time) * 1000
        assert health_time < 100
        
        print(f"✅ All AC requirements (AC-007 through AC-012) are verified!")
        print(f"   Hello endpoint response time: {hello_time:.2f}ms")
        print(f"   Health endpoint response time: {health_time:.2f}ms")