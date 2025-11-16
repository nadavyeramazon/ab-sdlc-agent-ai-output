"""Integration tests for the fullstack application."""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


class TestIntegration:
    """Integration tests combining multiple features."""
    
    def test_both_endpoints_work_sequentially(self):
        """Test that both hello and greet endpoints work in sequence."""
        # First call hello endpoint
        hello_response = client.get("/api/hello")
        assert hello_response.status_code == 200
        assert "message" in hello_response.json()
        
        # Then call greet endpoint
        greet_response = client.post("/api/greet", json={"name": "Test User"})
        assert greet_response.status_code == 200
        assert "greeting" in greet_response.json()
    
    def test_greet_then_hello_works(self):
        """Test that greet followed by hello works correctly."""
        # First call greet endpoint
        greet_response = client.post("/api/greet", json={"name": "Alice"})
        assert greet_response.status_code == 200
        
        # Then call hello endpoint
        hello_response = client.get("/api/hello")
        assert hello_response.status_code == 200
        assert hello_response.json()["message"] == "Hello World from Backend!"
    
    def test_multiple_greet_calls_independent(self):
        """Test that multiple greet calls don't interfere with each other."""
        # First greet
        response1 = client.post("/api/greet", json={"name": "Alice"})
        assert response1.status_code == 200
        data1 = response1.json()
        
        # Second greet with different name
        response2 = client.post("/api/greet", json={"name": "Bob"})
        assert response2.status_code == 200
        data2 = response2.json()
        
        # Verify each response is independent
        assert "Alice" in data1["greeting"]
        assert "Bob" in data2["greeting"]
        assert "Alice" not in data2["greeting"]
        assert "Bob" not in data1["greeting"]
    
    def test_error_recovery(self):
        """Test that error in greet doesn't affect subsequent calls."""
        # Make a call that should fail
        error_response = client.post("/api/greet", json={"name": ""})
        assert error_response.status_code == 400
        
        # Make a successful call
        success_response = client.post("/api/greet", json={"name": "Bob"})
        assert success_response.status_code == 200
        
        # Verify hello still works
        hello_response = client.get("/api/hello")
        assert hello_response.status_code == 200
    
    def test_health_check_always_available(self):
        """Test that health check works alongside other operations."""
        # Health check before operations
        health1 = client.get("/health")
        assert health1.status_code == 200
        
        # Perform operations
        client.get("/api/hello")
        client.post("/api/greet", json={"name": "Test"})
        
        # Health check after operations
        health2 = client.get("/health")
        assert health2.status_code == 200
        assert health1.json() == health2.json()


class TestCombinedFeatures:
    """Tests for combined feature functionality."""
    
    def test_all_endpoints_have_cors(self):
        """Test that all endpoints support CORS for frontend."""
        endpoints = [
            ("GET", "/api/hello", None),
            ("POST", "/api/greet", {"name": "Test"}),
        ]
        
        for method, path, json_data in endpoints:
            if method == "GET":
                response = client.get(path)
            else:
                response = client.post(path, json=json_data)
            
            assert "access-control-allow-origin" in response.headers, \
                f"CORS missing for {method} {path}"
    
    def test_api_consistency(self):
        """Test that API responses are consistent in format."""
        # Hello endpoint returns dict with 'message' key
        hello_response = client.get("/api/hello")
        assert isinstance(hello_response.json(), dict)
        
        # Greet endpoint returns dict with 'greeting' and 'timestamp' keys
        greet_response = client.post("/api/greet", json={"name": "Test"})
        greet_data = greet_response.json()
        assert isinstance(greet_data, dict)
        assert "greeting" in greet_data
        assert "timestamp" in greet_data
        
        # Health endpoint returns dict with 'status' key
        health_response = client.get("/health")
        assert isinstance(health_response.json(), dict)
