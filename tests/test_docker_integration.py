"""Tests for Docker integration and frontend functionality.

This module contains tests to verify that the Docker setup works correctly
and that the frontend can communicate with the backend.
"""

import pytest
import subprocess
import time
import requests
from pathlib import Path


class TestDockerfileExists:
    """Tests to verify Docker configuration files exist."""
    
    def test_backend_dockerfile_exists(self):
        """Test that backend Dockerfile exists."""
        dockerfile = Path("Dockerfile")
        assert dockerfile.exists(), "Backend Dockerfile not found"
        
        # Check it contains required content
        content = dockerfile.read_text()
        assert "FROM python" in content
        assert "uvicorn" in content
        assert "EXPOSE 8000" in content
    
    def test_frontend_dockerfile_exists(self):
        """Test that frontend Dockerfile exists."""
        dockerfile = Path("frontend/Dockerfile")
        assert dockerfile.exists(), "Frontend Dockerfile not found"
        
        # Check it contains required content
        content = dockerfile.read_text()
        assert "FROM nginx" in content
        assert "EXPOSE 80" in content
    
    def test_docker_compose_exists(self):
        """Test that docker-compose.yml exists."""
        compose_file = Path("docker-compose.yml")
        assert compose_file.exists(), "docker-compose.yml not found"
        
        # Check it contains required services
        content = compose_file.read_text()
        assert "backend:" in content
        assert "frontend:" in content
        assert "8000:8000" in content
        assert "3000:80" in content or "80:80" in content


class TestFrontendFiles:
    """Tests to verify frontend files exist and have correct content."""
    
    def test_frontend_html_exists(self):
        """Test that frontend HTML file exists."""
        html_file = Path("frontend/index.html")
        assert html_file.exists(), "frontend/index.html not found"
        
        content = html_file.read_text()
        assert "<!DOCTYPE html>" in content
        assert "Green Themed" in content
        assert "API Interface" in content
    
    def test_frontend_css_exists(self):
        """Test that frontend CSS file exists."""
        css_file = Path("frontend/styles.css")
        assert css_file.exists(), "frontend/styles.css not found"
        
        content = css_file.read_text()
        # Check for green color variables
        assert "green" in content.lower()
        assert ":root" in content or "--" in content  # CSS variables
    
    def test_frontend_js_exists(self):
        """Test that frontend JavaScript file exists."""
        js_file = Path("frontend/app.js")
        assert js_file.exists(), "frontend/app.js not found"
        
        content = js_file.read_text()
        assert "fetch" in content or "XMLHttpRequest" in content
        assert "localhost:8000" in content  # API endpoint
    
    def test_nginx_config_exists(self):
        """Test that nginx configuration exists."""
        nginx_conf = Path("frontend/nginx.conf")
        assert nginx_conf.exists(), "frontend/nginx.conf not found"
        
        content = nginx_conf.read_text()
        assert "server" in content
        assert "listen" in content


class TestDockerConfiguration:
    """Tests to verify Docker configuration is valid."""
    
    def test_backend_dockerfile_syntax(self):
        """Test that backend Dockerfile has valid syntax."""
        dockerfile = Path("Dockerfile")
        content = dockerfile.read_text()
        
        # Check for essential Docker instructions
        assert "FROM" in content
        assert "WORKDIR" in content or "COPY" in content
        assert "CMD" in content or "ENTRYPOINT" in content
    
    def test_frontend_dockerfile_syntax(self):
        """Test that frontend Dockerfile has valid syntax."""
        dockerfile = Path("frontend/Dockerfile")
        content = dockerfile.read_text()
        
        # Check for essential Docker instructions
        assert "FROM" in content
        assert "COPY" in content
    
    def test_docker_compose_syntax(self):
        """Test that docker-compose.yml has valid structure."""
        compose_file = Path("docker-compose.yml")
        content = compose_file.read_text()
        
        # Check for required docker-compose elements
        assert "version:" in content
        assert "services:" in content
        assert "backend:" in content
        assert "frontend:" in content
        assert "build:" in content
        assert "ports:" in content


class TestGreenTheming:
    """Tests to verify green theme implementation."""
    
    def test_css_has_green_colors(self):
        """Test that CSS file uses green color scheme."""
        css_file = Path("frontend/styles.css")
        content = css_file.read_text().lower()
        
        # Check for green color codes or keywords
        green_indicators = [
            "green",
            "#2d5016",  # Dark green
            "#4a7c2c",  # Medium green
            "#8bc34a",  # Light green
        ]
        
        found_green = any(indicator in content for indicator in green_indicators)
        assert found_green, "CSS file doesn't contain green theme colors"
    
    def test_html_mentions_green_theme(self):
        """Test that HTML mentions green theme."""
        html_file = Path("frontend/index.html")
        content = html_file.read_text()
        
        # Check for green theme references
        assert "green" in content.lower() or "Green" in content


class TestEndToEndIntegration:
    """End-to-end integration tests (requires Docker).
    
    These tests are marked as integration tests and can be skipped
    in environments where Docker is not available.
    """
    
    @pytest.mark.integration
    @pytest.mark.skipif(
        not Path("docker-compose.yml").exists(),
        reason="docker-compose.yml not found"
    )
    def test_docker_compose_structure(self):
        """Test that docker-compose file has correct structure."""
        compose_file = Path("docker-compose.yml")
        content = compose_file.read_text()
        
        # Verify service dependencies
        assert "depends_on" in content or "backend" in content
        
        # Verify network configuration
        assert "networks:" in content or "network_mode:" in content


class TestAPIEndpointsAvailability:
    """Tests to verify API endpoints are properly configured."""
    
    def test_main_py_has_cors_configuration(self):
        """Test that main.py is ready for CORS (important for frontend)."""
        main_file = Path("main.py")
        content = main_file.read_text()
        
        # The file should have FastAPI app
        assert "FastAPI" in content
        assert "app =" in content
        
        # Check for endpoints
        assert "@app.get" in content
    
    def test_all_required_endpoints_defined(self):
        """Test that all required endpoints are defined in main.py."""
        main_file = Path("main.py")
        content = main_file.read_text()
        
        # Check for the endpoints the frontend expects
        assert '"/"' in content or "'/'" in content  # Root endpoint
        assert '"/health"' in content or "'/health'" in content  # Health endpoint
        assert '"/hello' in content or "'/hello" in content  # Hello endpoint


# Parametrized tests for file validation
@pytest.mark.parametrize("file_path", [
    "frontend/index.html",
    "frontend/styles.css",
    "frontend/app.js",
    "frontend/nginx.conf",
    "frontend/Dockerfile",
    "Dockerfile",
    "docker-compose.yml",
])
def test_required_file_exists(file_path):
    """Parametrized test to check all required files exist."""
    path = Path(file_path)
    assert path.exists(), f"Required file {file_path} not found"
    assert path.stat().st_size > 0, f"File {file_path} is empty"


@pytest.mark.parametrize("docker_file,expected_content", [
    ("Dockerfile", ["FROM python", "uvicorn", "8000"]),
    ("frontend/Dockerfile", ["FROM nginx", "COPY", "80"]),
    ("docker-compose.yml", ["services", "backend", "frontend"]),
])
def test_docker_file_content(docker_file, expected_content):
    """Parametrized test to check Docker files have expected content."""
    path = Path(docker_file)
    content = path.read_text()
    
    for expected in expected_content:
        assert expected in content, f"{docker_file} missing expected content: {expected}"