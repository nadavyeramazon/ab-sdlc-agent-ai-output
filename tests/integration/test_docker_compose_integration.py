"""Comprehensive integration tests for Docker Compose deployment.

These tests validate that the fullstack application works correctly
after running 'docker compose up --build'. They test:
- Backend API functionality
- Frontend serving through nginx
- Frontend-backend integration via nginx proxy
- CORS configuration
- Error handling
"""

import pytest
import requests
import time
from typing import Dict, Any

# Service URLs when running with docker-compose
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:80"
FRONTEND_API_PROXY = "http://localhost:80/api"

# Retry configuration for service startup
MAX_RETRIES = 30
RETRY_DELAY = 2  # seconds


class TestDockerComposeDeployment:
    """Test suite for Docker Compose deployment validation."""

    @pytest.fixture(scope="class", autouse=True)
    def wait_for_services(self):
        """Wait for all services to be ready before running tests."""
        print("\n🔄 Waiting for services to be ready...")
        
        # Wait for backend
        backend_ready = False
        for i in range(MAX_RETRIES):
            try:
                response = requests.get(f"{BACKEND_URL}/health", timeout=2)
                if response.status_code == 200:
                    backend_ready = True
                    print(f"✅ Backend ready (attempt {i+1}/{MAX_RETRIES})")
                    break
            except requests.exceptions.RequestException:
                pass
            time.sleep(RETRY_DELAY)
        
        if not backend_ready:
            pytest.fail("Backend service failed to start")
        
        # Wait for frontend
        frontend_ready = False
        for i in range(MAX_RETRIES):
            try:
                response = requests.get(FRONTEND_URL, timeout=2)
                if response.status_code == 200:
                    frontend_ready = True
                    print(f"✅ Frontend ready (attempt {i+1}/{MAX_RETRIES})")
                    break
            except requests.exceptions.RequestException:
                pass
            time.sleep(RETRY_DELAY)
        
        if not frontend_ready:
            pytest.fail("Frontend service failed to start")
        
        print("✅ All services are ready!\n")
        yield


class TestBackendAPI:
    """Test backend API endpoints directly."""

    def test_backend_health_endpoint(self):
        """Test backend health check endpoint."""
        response = requests.get(f"{BACKEND_URL}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "red-greeting-api"
        assert "version" in data

    def test_backend_root_endpoint(self):
        """Test backend root endpoint."""
        response = requests.get(BACKEND_URL)
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "Red" in data["message"]

    def test_backend_greet_post(self):
        """Test POST /greet endpoint."""
        response = requests.post(
            f"{BACKEND_URL}/greet",
            json={"name": "TestUser"},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "TestUser" in data["message"]
        assert "red-themed" in data["message"]
        assert data["name"] == "TestUser"

    def test_backend_greet_get(self):
        """Test GET /greet/{name} endpoint."""
        response = requests.get(f"{BACKEND_URL}/greet/Alice")
        assert response.status_code == 200
        
        data = response.json()
        assert "Alice" in data["message"]
        assert data["name"] == "Alice"

    def test_backend_howdy_post(self):
        """Test POST /howdy endpoint."""
        response = requests.post(
            f"{BACKEND_URL}/howdy",
            json={"name": "Cowboy"},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "Howdy" in data["message"]
        assert "Cowboy" in data["message"]
        assert data["name"] == "Cowboy"

    def test_backend_howdy_get(self):
        """Test GET /howdy/{name} endpoint."""
        response = requests.get(f"{BACKEND_URL}/howdy/Ranger")
        assert response.status_code == 200
        
        data = response.json()
        assert "Howdy" in data["message"]
        assert "Ranger" in data["message"]

    def test_backend_validation_empty_name(self):
        """Test validation with empty name."""
        response = requests.post(
            f"{BACKEND_URL}/greet",
            json={"name": ""},
            headers={"Content-Type": "application/json"}
        )
        # Pydantic validation should return 422
        assert response.status_code == 422

    def test_backend_validation_whitespace_name(self):
        """Test validation with whitespace-only name."""
        response = requests.post(
            f"{BACKEND_URL}/greet",
            json={"name": "   "},
            headers={"Content-Type": "application/json"}
        )
        # Custom validation should return 400
        assert response.status_code == 400


class TestFrontendServing:
    """Test frontend file serving through nginx."""

    def test_frontend_index_accessible(self):
        """Test that frontend index.html is accessible."""
        response = requests.get(FRONTEND_URL)
        assert response.status_code == 200
        assert "text/html" in response.headers["Content-Type"]
        
        content = response.text
        assert "Red Greeting" in content
        assert "<html" in content

    def test_frontend_has_correct_title(self):
        """Test that frontend has correct page title."""
        response = requests.get(FRONTEND_URL)
        assert response.status_code == 200
        assert "<title>Red Greeting App</title>" in response.text

    def test_frontend_includes_css(self):
        """Test that frontend HTML includes CSS reference."""
        response = requests.get(FRONTEND_URL)
        assert response.status_code == 200
        assert "styles.css" in response.text

    def test_frontend_includes_js(self):
        """Test that frontend HTML includes JavaScript reference."""
        response = requests.get(FRONTEND_URL)
        assert response.status_code == 200
        assert "app.js" in response.text

    def test_frontend_css_accessible(self):
        """Test that CSS file is accessible."""
        response = requests.get(f"{FRONTEND_URL}/styles.css")
        assert response.status_code == 200
        assert "text/css" in response.headers["Content-Type"]
        
        content = response.text
        assert "Red Theme" in content or "red" in content.lower()

    def test_frontend_js_accessible(self):
        """Test that JavaScript file is accessible."""
        response = requests.get(f"{FRONTEND_URL}/app.js")
        assert response.status_code == 200
        
        content = response.text
        assert "Red Greeting" in content
        assert "function" in content or "const" in content


class TestNginxProxyIntegration:
    """Test frontend-backend integration via nginx proxy."""

    def test_proxy_health_endpoint(self):
        """Test health check through nginx proxy."""
        response = requests.get(f"{FRONTEND_API_PROXY}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"

    def test_proxy_greet_endpoint(self):
        """Test greet endpoint through nginx proxy."""
        response = requests.post(
            f"{FRONTEND_API_PROXY}/greet",
            json={"name": "ProxyTest"},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "ProxyTest" in data["message"]

    def test_proxy_howdy_endpoint(self):
        """Test howdy endpoint through nginx proxy."""
        response = requests.post(
            f"{FRONTEND_API_PROXY}/howdy",
            json={"name": "ProxyTest"},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "Howdy" in data["message"]

    def test_proxy_preserves_json_content_type(self):
        """Test that proxy preserves content type headers."""
        response = requests.get(f"{FRONTEND_API_PROXY}/health")
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]


class TestCORSConfiguration:
    """Test CORS configuration."""

    def test_cors_headers_present(self):
        """Test that CORS headers are present in backend responses."""
        response = requests.get(
            f"{BACKEND_URL}/health",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 200
        assert "Access-Control-Allow-Origin" in response.headers

    def test_cors_allows_all_origins(self):
        """Test that CORS allows all origins (as configured)."""
        response = requests.get(
            f"{BACKEND_URL}/health",
            headers={"Origin": "http://example.com"}
        )
        assert response.status_code == 200
        assert response.headers.get("Access-Control-Allow-Origin") == "*"

    def test_cors_options_request(self):
        """Test CORS preflight OPTIONS request."""
        response = requests.options(
            f"{BACKEND_URL}/greet",
            headers={
                "Origin": "http://localhost",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        assert response.status_code == 200
        assert "Access-Control-Allow-Origin" in response.headers
        assert "Access-Control-Allow-Methods" in response.headers


class TestAPIDocumentation:
    """Test API documentation accessibility."""

    def test_swagger_ui_accessible(self):
        """Test that Swagger UI is accessible."""
        response = requests.get(f"{BACKEND_URL}/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower() or "openapi" in response.text.lower()

    def test_openapi_json_accessible(self):
        """Test that OpenAPI JSON is accessible."""
        response = requests.get(f"{BACKEND_URL}/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert "openapi" in data
        assert "paths" in data
        assert "/health" in data["paths"]
        assert "/greet" in data["paths"]

    def test_redoc_accessible(self):
        """Test that ReDoc is accessible."""
        response = requests.get(f"{BACKEND_URL}/redoc")
        assert response.status_code == 200


class TestThemeConsistency:
    """Test red theme consistency across the application."""

    def test_service_name_matches_theme(self):
        """Test that service name matches red theme."""
        response = requests.get(f"{BACKEND_URL}/health")
        data = response.json()
        assert "red" in data["service"].lower()

    def test_greet_message_mentions_theme(self):
        """Test that greeting messages mention red theme."""
        response = requests.post(
            f"{BACKEND_URL}/greet",
            json={"name": "Test"},
            headers={"Content-Type": "application/json"}
        )
        data = response.json()
        assert "red-themed" in data["message"].lower()

    def test_no_green_theme_references(self):
        """Test that there are no green theme references."""
        # Check health endpoint
        response = requests.get(f"{BACKEND_URL}/health")
        assert "green" not in response.text.lower()
        
        # Check greet endpoint
        response = requests.post(
            f"{BACKEND_URL}/greet",
            json={"name": "Test"},
            headers={"Content-Type": "application/json"}
        )
        assert "green" not in response.text.lower()

    def test_frontend_title_matches_theme(self):
        """Test that frontend title matches red theme."""
        response = requests.get(FRONTEND_URL)
        assert "Red Greeting" in response.text


class TestErrorHandling:
    """Test error handling in the application."""

    def test_invalid_endpoint_returns_404(self):
        """Test that invalid endpoints return 404."""
        response = requests.get(f"{BACKEND_URL}/invalid-endpoint")
        assert response.status_code == 404

    def test_invalid_method_returns_405(self):
        """Test that invalid HTTP methods return 405."""
        response = requests.delete(f"{BACKEND_URL}/health")
        assert response.status_code == 405

    def test_invalid_json_returns_422(self):
        """Test that invalid JSON returns 422."""
        response = requests.post(
            f"{BACKEND_URL}/greet",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_missing_required_field_returns_422(self):
        """Test that missing required fields return 422."""
        response = requests.post(
            f"{BACKEND_URL}/greet",
            json={},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


class TestServiceHealth:
    """Test overall service health and availability."""

    def test_backend_responds_quickly(self):
        """Test that backend responds within acceptable time."""
        start_time = time.time()
        response = requests.get(f"{BACKEND_URL}/health")
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        assert response_time < 2.0  # Should respond within 2 seconds

    def test_frontend_responds_quickly(self):
        """Test that frontend responds within acceptable time."""
        start_time = time.time()
        response = requests.get(FRONTEND_URL)
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        assert response_time < 2.0  # Should respond within 2 seconds

    def test_multiple_concurrent_requests(self):
        """Test that service handles multiple concurrent requests."""
        import concurrent.futures
        
        def make_request(name: str) -> Dict[str, Any]:
            response = requests.post(
                f"{BACKEND_URL}/greet",
                json={"name": name},
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        
        # Make 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request, f"User{i}") for i in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Verify all requests succeeded
        assert len(results) == 10
        for result in results:
            assert "message" in result
            assert "name" in result
