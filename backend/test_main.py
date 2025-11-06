import pytest
from fastapi.testclient import TestClient
from main import app, items, next_id

# Test client
client = TestClient(app)

# Reset data before each test
@pytest.fixture(autouse=True)
def reset_data():
    global next_id
    items.clear()
    next_id = 1
    yield
    items.clear()
    next_id = 1

# Test data
valid_item_data = {
    "name": "Test Item",
    "description": "A test item description",
    "price": 29.99,
    "category": "electronics"
}

class TestHealthEndpoint:
    def test_root_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Item Management API is running"
        assert data["status"] == "healthy"

class TestGetItems:
    def test_get_empty_items(self):
        """Test getting items when list is empty"""
        response = client.get("/items")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_items_with_data(self):
        """Test getting items when items exist"""
        # Create an item first
        client.post("/items", json=valid_item_data)
        
        response = client.get("/items")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == valid_item_data["name"]
        assert data[0]["id"] == 1

class TestGetSingleItem:
    def test_get_existing_item(self):
        """Test getting a specific item that exists"""
        # Create an item first
        create_response = client.post("/items", json=valid_item_data)
        item_id = create_response.json()["id"]
        
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == valid_item_data["name"]
    
    def test_get_nonexistent_item(self):
        """Test getting an item that doesn't exist"""
        response = client.get("/items/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_get_item_invalid_id(self):
        """Test getting an item with invalid ID"""
        response = client.get("/items/0")
        assert response.status_code == 400
        assert "positive integer" in response.json()["detail"]
        
        response = client.get("/items/-1")
        assert response.status_code == 400

class TestCreateItem:
    def test_create_valid_item(self):
        """Test creating a valid item"""
        response = client.post("/items", json=valid_item_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == valid_item_data["name"]
        assert data["price"] == valid_item_data["price"]
        assert data["id"] == 1
    
    def test_create_item_empty_name(self):
        """Test creating item with empty name"""
        invalid_data = valid_item_data.copy()
        invalid_data["name"] = ""
        
        response = client.post("/items", json=invalid_data)
        assert response.status_code == 422
    
    def test_create_item_long_name(self):
        """Test creating item with name too long"""
        invalid_data = valid_item_data.copy()
        invalid_data["name"] = "a" * 101  # Exceeds 100 character limit
        
        response = client.post("/items", json=invalid_data)
        assert response.status_code == 422
    
    def test_create_item_invalid_characters(self):
        """Test creating item with invalid characters in name"""
        invalid_data = valid_item_data.copy()
        invalid_data["name"] = "Test<script>alert('xss')</script>"
        
        response = client.post("/items", json=invalid_data)
        assert response.status_code == 422
    
    def test_create_item_negative_price(self):
        """Test creating item with negative price"""
        invalid_data = valid_item_data.copy()
        invalid_data["price"] = -10.0
        
        response = client.post("/items", json=invalid_data)
        assert response.status_code == 422
    
    def test_create_item_excessive_price(self):
        """Test creating item with excessive price"""
        invalid_data = valid_item_data.copy()
        invalid_data["price"] = 1000000.0  # Exceeds limit
        
        response = client.post("/items", json=invalid_data)
        assert response.status_code == 422
    
    def test_create_item_invalid_category(self):
        """Test creating item with invalid category"""
        invalid_data = valid_item_data.copy()
        invalid_data["category"] = "invalid_category"
        
        response = client.post("/items", json=invalid_data)
        assert response.status_code == 422
    
    def test_create_item_long_description(self):
        """Test creating item with description too long"""
        invalid_data = valid_item_data.copy()
        invalid_data["description"] = "a" * 501  # Exceeds 500 character limit
        
        response = client.post("/items", json=invalid_data)
        assert response.status_code == 422
    
    def test_create_multiple_items(self):
        """Test creating multiple items increments IDs correctly"""
        response1 = client.post("/items", json=valid_item_data)
        assert response1.status_code == 201
        assert response1.json()["id"] == 1
        
        item_data_2 = valid_item_data.copy()
        item_data_2["name"] = "Second Item"
        response2 = client.post("/items", json=item_data_2)
        assert response2.status_code == 201
        assert response2.json()["id"] == 2

class TestUpdateItem:
    def test_update_existing_item(self):
        """Test updating an existing item"""
        # Create an item first
        create_response = client.post("/items", json=valid_item_data)
        item_id = create_response.json()["id"]
        
        update_data = {"name": "Updated Item", "price": 39.99}
        response = client.put(f"/items/{item_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Item"
        assert data["price"] == 39.99
        assert data["category"] == valid_item_data["category"]  # Unchanged
    
    def test_update_nonexistent_item(self):
        """Test updating an item that doesn't exist"""
        update_data = {"name": "Updated Item"}
        response = client.put("/items/999", json=update_data)
        assert response.status_code == 404
    
    def test_update_item_invalid_id(self):
        """Test updating item with invalid ID"""
        update_data = {"name": "Updated Item"}
        response = client.put("/items/0", json=update_data)
        assert response.status_code == 400
    
    def test_update_item_no_fields(self):
        """Test updating item with no fields"""
        # Create an item first
        create_response = client.post("/items", json=valid_item_data)
        item_id = create_response.json()["id"]
        
        # Try to update with empty data
        response = client.put(f"/items/{item_id}", json={})
        assert response.status_code == 400
        assert "No fields to update" in response.json()["detail"]
    
    def test_update_item_invalid_data(self):
        """Test updating item with invalid data"""
        # Create an item first
        create_response = client.post("/items", json=valid_item_data)
        item_id = create_response.json()["id"]
        
        # Try to update with invalid price
        update_data = {"price": -10.0}
        response = client.put(f"/items/{item_id}", json=update_data)
        assert response.status_code == 422

class TestDeleteItem:
    def test_delete_existing_item(self):
        """Test deleting an existing item"""
        # Create an item first
        create_response = client.post("/items", json=valid_item_data)
        item_id = create_response.json()["id"]
        
        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 204
        
        # Verify item is deleted
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_item(self):
        """Test deleting an item that doesn't exist"""
        response = client.delete("/items/999")
        assert response.status_code == 404
    
    def test_delete_item_invalid_id(self):
        """Test deleting item with invalid ID"""
        response = client.delete("/items/0")
        assert response.status_code == 400
        assert "positive integer" in response.json()["detail"]

class TestInputValidation:
    def test_price_rounding(self):
        """Test that prices are properly rounded to 2 decimal places"""
        test_data = valid_item_data.copy()
        test_data["price"] = 29.999  # Should be rounded to 29.99
        
        response = client.post("/items", json=test_data)
        assert response.status_code == 201
        assert response.json()["price"] == 30.00  # Rounded
    
    def test_category_case_insensitive(self):
        """Test that category validation is case insensitive"""
        test_data = valid_item_data.copy()
        test_data["category"] = "ELECTRONICS"  # Uppercase
        
        response = client.post("/items", json=test_data)
        assert response.status_code == 201
        assert response.json()["category"] == "electronics"  # Lowercase
    
    def test_string_trimming(self):
        """Test that strings are properly trimmed"""
        test_data = valid_item_data.copy()
        test_data["name"] = "  Test Item  "  # With spaces
        test_data["description"] = "  Test description  "
        
        response = client.post("/items", json=test_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Item"  # Trimmed
        assert data["description"] == "Test description"  # Trimmed

class TestIntegration:
    def test_full_crud_workflow(self):
        """Test complete CRUD workflow"""
        # Create
        response = client.post("/items", json=valid_item_data)
        assert response.status_code == 201
        item_id = response.json()["id"]
        
        # Read
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        assert response.json()["name"] == valid_item_data["name"]
        
        # Update
        update_data = {"name": "Updated Item"}
        response = client.put(f"/items/{item_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Item"
        
        # Delete
        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 204
        
        # Verify deletion
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 404