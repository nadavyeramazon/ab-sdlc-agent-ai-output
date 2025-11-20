"""Tests for FastAPI application configuration and lifecycle."""

import pytest
from fastapi import FastAPI


class TestApplicationSetup:
    """Test suite for application initialization and configuration."""
    
    @pytest.mark.unit
    def test_application_is_fastapi_instance(self, test_app):
        """Test that app is a FastAPI instance."""
        assert isinstance(test_app, FastAPI)
    
    @pytest.mark.unit
    def test_application_title_is_set(self, test_app):
        """Test that application title is configured."""
        assert test_app.title == "Demo FastAPI Backend"
    
    @pytest.mark.unit
    def test_application_has_middleware(self, test_app):
        """Test that application has middleware configured."""
        assert len(test_app.user_middleware) > 0
    
    @pytest.mark.unit
    def test_cors_middleware_is_present(self, test_app):
        """Test that CORS middleware is configured."""
        middleware_names = [m.cls.__name__ for m in test_app.user_middleware]
        assert "CORSMiddleware" in middleware_names
    
    @pytest.mark.unit
    def test_application_has_routes(self, test_app):
        """Test that application has routes defined."""
        assert len(test_app.routes) > 0
    
    @pytest.mark.unit
    def test_application_routes_include_custom_endpoints(self, test_app):
        """Test that custom endpoints are registered."""
        route_paths = [route.path for route in test_app.routes]
        assert "/api/hello" in route_paths
        assert "/health" in route_paths
    
    @pytest.mark.unit
    def test_application_version_info_accessible(self, test_app):
        """Test that application has version information."""
        # FastAPI provides version info
        assert hasattr(test_app, 'version')
    
    @pytest.mark.unit
    def test_openapi_schema_is_generated(self, test_app):
        """Test that OpenAPI schema can be generated."""
        schema = test_app.openapi()
        assert schema is not None
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema


class TestRouteConfiguration:
    """Test suite for route configuration."""
    
    @pytest.mark.unit
    def test_hello_route_exists(self, test_app):
        """Test that /api/hello route is configured."""
        routes = {route.path: route for route in test_app.routes}
        assert "/api/hello" in routes
    
    @pytest.mark.unit
    def test_health_route_exists(self, test_app):
        """Test that /health route is configured."""
        routes = {route.path: route for route in test_app.routes}
        assert "/health" in routes
    
    @pytest.mark.unit
    def test_hello_route_methods(self, test_app):
        """Test that /api/hello supports GET method."""
        for route in test_app.routes:
            if route.path == "/api/hello":
                assert "GET" in route.methods
                break
        else:
            pytest.fail("/api/hello route not found")
    
    @pytest.mark.unit
    def test_health_route_methods(self, test_app):
        """Test that /health supports GET method."""
        for route in test_app.routes:
            if route.path == "/health":
                assert "GET" in route.methods
                break
        else:
            pytest.fail("/health route not found")
    
    @pytest.mark.unit
    def test_routes_have_endpoint_functions(self, test_app):
        """Test that routes have associated endpoint functions."""
        for route in test_app.routes:
            if route.path in ["/api/hello", "/health"]:
                assert hasattr(route, 'endpoint')
                assert callable(route.endpoint)


class TestMiddlewareConfiguration:
    """Test suite for middleware configuration."""
    
    @pytest.mark.unit
    def test_cors_middleware_allows_localhost_3000(self, test_app):
        """Test that CORS middleware is configured for localhost:3000."""
        # This tests the configuration in main.py
        # The actual CORS behavior is tested in test_cors.py
        middleware_found = False
        for middleware in test_app.user_middleware:
            if "CORSMiddleware" in str(middleware.cls):
                middleware_found = True
                # Check middleware options if accessible
                if hasattr(middleware, 'options'):
                    options = middleware.options
                    if 'allow_origins' in options:
                        assert 'http://localhost:3000' in options['allow_origins']
                break
        
        assert middleware_found, "CORS middleware not found"
    
    @pytest.mark.unit
    def test_cors_middleware_order(self, test_app):
        """Test that CORS middleware is properly ordered."""
        # CORS middleware should be added to the app
        assert len(test_app.user_middleware) > 0
        
        # First user middleware should be CORS
        first_middleware = test_app.user_middleware[0]
        assert "CORSMiddleware" in str(first_middleware.cls)


class TestOpenAPIDocumentation:
    """Test suite for OpenAPI documentation configuration."""
    
    @pytest.mark.unit
    def test_openapi_schema_has_title(self, test_app):
        """Test that OpenAPI schema includes app title."""
        schema = test_app.openapi()
        assert schema["info"]["title"] == "Demo FastAPI Backend"
    
    @pytest.mark.unit
    def test_openapi_schema_has_version(self, test_app):
        """Test that OpenAPI schema includes version."""
        schema = test_app.openapi()
        assert "version" in schema["info"]
    
    @pytest.mark.unit
    def test_openapi_schema_documents_hello_endpoint(self, test_app):
        """Test that OpenAPI schema documents /api/hello."""
        schema = test_app.openapi()
        assert "/api/hello" in schema["paths"]
        assert "get" in schema["paths"]["/api/hello"]
    
    @pytest.mark.unit
    def test_openapi_schema_documents_health_endpoint(self, test_app):
        """Test that OpenAPI schema documents /health."""
        schema = test_app.openapi()
        assert "/health" in schema["paths"]
        assert "get" in schema["paths"]["/health"]
    
    @pytest.mark.unit
    def test_hello_endpoint_has_summary(self, test_app):
        """Test that /api/hello has documentation summary."""
        schema = test_app.openapi()
        hello_spec = schema["paths"]["/api/hello"]["get"]
        # Should have either summary or description
        assert "summary" in hello_spec or "description" in hello_spec
    
    @pytest.mark.unit
    def test_health_endpoint_has_summary(self, test_app):
        """Test that /health has documentation summary."""
        schema = test_app.openapi()
        health_spec = schema["paths"]["/health"]["get"]
        # Should have either summary or description
        assert "summary" in health_spec or "description" in health_spec
    
    @pytest.mark.unit
    def test_openapi_schema_specifies_response_schema(self, test_app):
        """Test that endpoints have response schemas defined."""
        schema = test_app.openapi()
        
        # Check hello endpoint
        hello_responses = schema["paths"]["/api/hello"]["get"]["responses"]
        assert "200" in hello_responses
        
        # Check health endpoint
        health_responses = schema["paths"]["/health"]["get"]["responses"]
        assert "200" in health_responses
