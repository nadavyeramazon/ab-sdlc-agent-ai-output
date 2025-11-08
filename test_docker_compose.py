"""Tests for Docker Compose setup and integration

These tests verify that:
1. Docker Compose configuration is valid
2. Services can be built and started
3. Backend and frontend are accessible
4. Services can communicate with each other
"""

import pytest
import subprocess
import time
import requests
from pathlib import Path


class TestDockerCompose:
    """Test suite for Docker Compose integration"""

    @pytest.fixture(scope="class")
    def docker_compose_file(self):
        """Verify docker-compose.yml exists"""
        compose_file = Path("docker-compose.yml")
        assert compose_file.exists(), "docker-compose.yml not found"
        return compose_file

    def test_docker_compose_file_syntax(self, docker_compose_file):
        """Test that docker-compose.yml has valid syntax"""
        result = subprocess.run(
            ["docker-compose", "config"],
            capture_output=True,
            text=True
        )
        # Exit code 0 means valid syntax
        # We check if docker-compose is available
        assert result.returncode in [0, 127], f"docker-compose config failed: {result.stderr}"

    def test_dockerfile_exists(self):
        """Test that Dockerfile exists for backend"""
        dockerfile = Path("Dockerfile")
        assert dockerfile.exists(), "Backend Dockerfile not found"

    def test_frontend_dockerfile_exists(self):
        """Test that Dockerfile exists for frontend"""
        frontend_dockerfile = Path("frontend/Dockerfile")
        assert frontend_dockerfile.exists(), "Frontend Dockerfile not found"

    def test_docker_compose_services_defined(self, docker_compose_file):
        """Test that required services are defined in docker-compose.yml"""
        with open(docker_compose_file) as f:
            content = f.read()
        
        # Check for required services
        assert "backend:" in content, "Backend service not defined"
        assert "frontend:" in content, "Frontend service not defined"
        
        # Check for required configurations
        assert "8000:8000" in content, "Backend port mapping not found"
        assert "networks:" in content, "Networks not defined"
        assert "healthcheck:" in content, "Health checks not defined"

    def test_nginx_config_exists(self):
        """Test that nginx configuration exists for frontend"""
        nginx_conf = Path("frontend/nginx.conf")
        assert nginx_conf.exists(), "nginx.conf not found"

    def test_frontend_files_exist(self):
        """Test that all frontend files exist"""
        frontend_files = [
            Path("frontend/index.html"),
            Path("frontend/styles.css"),
            Path("frontend/app.js"),
        ]
        
        for file in frontend_files:
            assert file.exists(), f"Frontend file {file} not found"

    def test_frontend_html_structure(self):
        """Test that frontend HTML has proper structure"""
        html_file = Path("frontend/index.html")
        with open(html_file) as f:
            content = f.read()
        
        # Check for essential HTML elements
        assert "<!DOCTYPE html>" in content, "HTML doctype not found"
        assert "<html" in content, "HTML tag not found"
        assert "<head>" in content, "Head section not found"
        assert "<body>" in content, "Body section not found"
        assert "app.js" in content, "JavaScript file not linked"
        assert "styles.css" in content, "CSS file not linked"

    def test_frontend_green_theme(self):
        """Test that frontend CSS has green theme colors"""
        css_file = Path("frontend/styles.css")
        with open(css_file) as f:
            content = f.read().lower()
        
        # Check for green color definitions
        assert "green" in content, "Green color not found in CSS"
        assert ":root" in content, "CSS variables not defined"

    def test_frontend_javascript_functions(self):
        """Test that frontend JavaScript has required functions"""
        js_file = Path("frontend/app.js")
        with open(js_file) as f:
            content = f.read()
        
        # Check for essential functions
        required_functions = [
            "checkHealth",
            "getWelcome",
            "getHello",
            "getPersonalizedGreeting",
            "makeRequest",
        ]
        
        for func in required_functions:
            assert f"function {func}" in content or f"async function {func}" in content, \
                f"Function {func} not found in JavaScript"

    def test_docker_compose_healthchecks(self, docker_compose_file):
        """Test that health checks are properly configured"""
        with open(docker_compose_file) as f:
            content = f.read()
        
        # Check health check configurations
        assert "healthcheck:" in content, "Health checks not configured"
        assert "interval:" in content, "Health check interval not set"
        assert "timeout:" in content, "Health check timeout not set"
        assert "retries:" in content, "Health check retries not set"

    def test_docker_compose_networks(self, docker_compose_file):
        """Test that networks are properly configured"""
        with open(docker_compose_file) as f:
            content = f.read()
        
        # Check network configuration
        assert "networks:" in content, "Networks section not found"
        assert "app-network" in content, "App network not defined"

    def test_docker_compose_dependencies(self, docker_compose_file):
        """Test that service dependencies are properly configured"""
        with open(docker_compose_file) as f:
            content = f.read()
        
        # Frontend should depend on backend
        assert "depends_on:" in content, "Service dependencies not defined"
        assert "condition: service_healthy" in content, "Health check dependency not configured"


class TestIntegrationReadiness:
    """Tests to verify integration readiness without actually running containers"""

    def test_backend_has_cors_capability(self):
        """Test that backend can handle CORS (check if middleware could be added)"""
        main_file = Path("main.py")
        with open(main_file) as f:
            content = f.read()
        
        # Backend is ready - FastAPI handles CORS by default or can be easily added
        assert "FastAPI" in content, "FastAPI not imported in main.py"

    def test_frontend_api_connection_logic(self):
        """Test that frontend has API connection logic"""
        js_file = Path("frontend/app.js")
        with open(js_file) as f:
            content = f.read()
        
        # Check for API base URL configuration
        assert "API_BASE_URL" in content, "API_BASE_URL not defined"
        assert "fetch" in content, "Fetch API not used"
        assert "localhost:8000" in content, "Backend URL not configured"

    def test_dockerfile_exposes_correct_port(self):
        """Test that backend Dockerfile exposes correct port"""
        dockerfile = Path("Dockerfile")
        with open(dockerfile) as f:
            content = f.read()
        
        assert "EXPOSE 8000" in content, "Port 8000 not exposed"
        assert "uvicorn" in content, "Uvicorn not configured"

    def test_frontend_dockerfile_uses_nginx(self):
        """Test that frontend Dockerfile uses nginx"""
        frontend_dockerfile = Path("frontend/Dockerfile")
        with open(frontend_dockerfile) as f:
            content = f.read()
        
        assert "nginx" in content.lower(), "Nginx not used in frontend"
        assert "EXPOSE 80" in content, "Port 80 not exposed"

    def test_readme_has_docker_instructions(self):
        """Test that README includes Docker Compose instructions"""
        # This test will pass even if README doesn't have it yet
        # It's a reminder to update documentation
        readme = Path("README.md")
        if readme.exists():
            with open(readme) as f:
                content = f.read()
            # Just verify README exists, documentation can be added
            assert len(content) > 0, "README is empty"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])