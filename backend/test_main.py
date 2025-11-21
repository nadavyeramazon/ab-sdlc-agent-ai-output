import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app

# Create test client
client = TestClient(app)

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_hello_endpoint():
    """Test the hello endpoint"""
    response = client.get("/api/hello")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "timestamp" in data
    assert data["message"] == "Hello World from Backend!"
    
    # Validate timestamp is valid ISO format
    try:
        datetime.fromisoformat(data["timestamp"])
    except ValueError:
        pytest.fail("Timestamp is not in valid ISO format")

# ============================================================================
# POST /api/greet endpoint tests - COMPREHENSIVE TEST COVERAGE
# ============================================================================

def test_greet_endpoint_success_valid_name():
    """Test POST /api/greet with valid name - should return 200 with greeting"""
    response = client.post("/api/greet", json={"name": "John"})
    
    # Check status code
    assert response.status_code == 200
    
    # Check response structure
    data = response.json()
    assert "greeting" in data
    assert "timestamp" in data
    
    # Check greeting message format
    assert data["greeting"] == "Hello, John! Welcome to our purple-themed app!"
    
    # Validate timestamp is valid ISO format
    try:
        datetime.fromisoformat(data["timestamp"])
    except ValueError:
        pytest.fail("Timestamp is not in valid ISO format")

def test_greet_endpoint_success_with_whitespace():
    """Test POST /api/greet with name containing leading/trailing whitespace"""
    response = client.post("/api/greet", json={"name": "  Jane  "})
    
    # Should succeed and strip whitespace
    assert response.status_code == 200
    
    data = response.json()
    # Name should be stripped in greeting
    assert data["greeting"] == "Hello, Jane! Welcome to our purple-themed app!"

def test_greet_endpoint_success_with_special_characters():
    """Test POST /api/greet with name containing special characters"""
    response = client.post("/api/greet", json={"name": "O'Brien-Smith"})
    
    assert response.status_code == 200
    
    data = response.json()
    assert data["greeting"] == "Hello, O'Brien-Smith! Welcome to our purple-themed app!"

def test_greet_endpoint_error_missing_name_field():
    """Test POST /api/greet with missing name field - should return 422"""
    response = client.post("/api/greet", json={})
    
    # Pydantic validation should return 422 for missing required field
    assert response.status_code == 422
    
    data = response.json()
    assert "detail" in data
    # Check that error mentions the 'name' field
    assert any('name' in str(error).lower() for error in data["detail"])

def test_greet_endpoint_error_empty_name_string():
    """Test POST /api/greet with empty name string - should return 422"""
    response = client.post("/api/greet", json={"name": ""})
    
    # Pydantic min_length validation should return 422
    assert response.status_code == 422
    
    data = response.json()
    assert "detail" in data

def test_greet_endpoint_error_whitespace_only_name():
    """Test POST /api/greet with whitespace-only name - should return 422"""
    response = client.post("/api/greet", json={"name": "   "})
    
    # Custom validator should catch whitespace-only names
    assert response.status_code == 422
    
    data = response.json()
    assert "detail" in data

def test_greet_endpoint_error_invalid_request_body():
    """Test POST /api/greet with invalid JSON structure - should return 422"""
    response = client.post("/api/greet", json={"invalid_field": "value"})
    
    # Missing required 'name' field
    assert response.status_code == 422
    
    data = response.json()
    assert "detail" in data

def test_greet_endpoint_error_name_too_long():
    """Test POST /api/greet with name exceeding max length - should return 422"""
    long_name = "A" * 101  # Max length is 100
    response = client.post("/api/greet", json={"name": long_name})
    
    # Pydantic max_length validation should return 422
    assert response.status_code == 422
    
    data = response.json()
    assert "detail" in data

def test_greet_endpoint_response_format_validation():
    """Test POST /api/greet response format matches expected schema"""
    response = client.post("/api/greet", json={"name": "Alice"})
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Validate response has exactly the expected fields
    assert set(data.keys()) == {"greeting", "timestamp"}
    
    # Validate field types
    assert isinstance(data["greeting"], str)
    assert isinstance(data["timestamp"], str)
    
    # Validate greeting format
    assert data["greeting"].startswith("Hello, ")
    assert data["greeting"].endswith("! Welcome to our purple-themed app!")
    assert "Alice" in data["greeting"]
    
    # Validate timestamp format (ISO 8601)
    try:
        parsed_timestamp = datetime.fromisoformat(data["timestamp"])
        # Ensure it's a recent timestamp (within last minute)
        now = datetime.now()
        time_diff = abs((now - parsed_timestamp.replace(tzinfo=None)).total_seconds())
        assert time_diff < 60, "Timestamp should be current"
    except ValueError:
        pytest.fail("Timestamp is not in valid ISO format")

def test_greet_endpoint_status_codes():
    """Test POST /api/greet returns correct status codes for different scenarios"""
    # Success case - 200
    response_success = client.post("/api/greet", json={"name": "Bob"})
    assert response_success.status_code == 200
    
    # Missing field - 422
    response_missing = client.post("/api/greet", json={})
    assert response_missing.status_code == 422
    
    # Empty name - 422
    response_empty = client.post("/api/greet", json={"name": ""})
    assert response_empty.status_code == 422
    
    # Whitespace only - 422
    response_whitespace = client.post("/api/greet", json={"name": "  "})
    assert response_whitespace.status_code == 422
