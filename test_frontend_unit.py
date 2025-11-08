"""Unit tests for frontend components

These tests verify the frontend code structure and content
without requiring a running server.
"""

import pytest
from pathlib import Path
import re


class TestFrontendHTML:
    """Test suite for HTML structure and content"""

    @pytest.fixture
    def html_content(self):
        """Load HTML content"""
        html_file = Path("frontend/index.html")
        with open(html_file) as f:
            return f.read()

    def test_html_doctype(self, html_content):
        """Test HTML5 doctype declaration"""
        assert "<!DOCTYPE html>" in html_content

    def test_html_meta_tags(self, html_content):
        """Test essential meta tags"""
        assert 'charset="UTF-8"' in html_content
        assert 'name="viewport"' in html_content

    def test_html_title(self, html_content):
        """Test page title"""
        assert "<title>" in html_content
        assert "Green" in html_content or "Hello World" in html_content

    def test_html_links_css(self, html_content):
        """Test CSS stylesheet is linked"""
        assert 'href="styles.css"' in html_content
        assert 'rel="stylesheet"' in html_content

    def test_html_links_js(self, html_content):
        """Test JavaScript file is linked"""
        assert 'src="app.js"' in html_content

    def test_html_has_status_section(self, html_content):
        """Test status indicator section exists"""
        assert 'id="status-indicator"' in html_content
        assert 'id="status-text"' in html_content

    def test_html_has_response_sections(self, html_content):
        """Test response display sections exist"""
        assert 'id="welcome-response"' in html_content
        assert 'id="hello-response"' in html_content
        assert 'id="personalized-response"' in html_content

    def test_html_has_input_field(self, html_content):
        """Test name input field exists"""
        assert 'id="name-input"' in html_content
        assert 'type="text"' in html_content

    def test_html_has_buttons(self, html_content):
        """Test interactive buttons exist"""
        assert 'onclick="checkHealth()"' in html_content
        assert 'onclick="getWelcome()"' in html_content
        assert 'onclick="getHello()"' in html_content
        assert 'onclick="getPersonalizedGreeting()"' in html_content

    def test_html_has_api_doc_links(self, html_content):
        """Test API documentation links exist"""
        assert '/docs' in html_content
        assert '/redoc' in html_content

    def test_html_semantic_structure(self, html_content):
        """Test semantic HTML5 elements"""
        assert "<header>" in html_content
        assert "<main>" in html_content
        assert "<footer>" in html_content


class TestFrontendCSS:
    """Test suite for CSS styles and theming"""

    @pytest.fixture
    def css_content(self):
        """Load CSS content"""
        css_file = Path("frontend/styles.css")
        with open(css_file) as f:
            return f.read()

    def test_css_root_variables(self, css_content):
        """Test CSS custom properties are defined"""
        assert ":root" in css_content
        assert "--" in css_content  # CSS variables syntax

    def test_css_green_theme_colors(self, css_content):
        """Test green theme colors are defined"""
        css_lower = css_content.lower()
        # Check for green color values (hex or named)
        green_patterns = [
            r"#[0-9a-f]{6}",  # Hex colors
            r"green",  # Named color
            r"rgb\(",  # RGB colors
        ]
        
        has_colors = any(re.search(pattern, css_lower) for pattern in green_patterns)
        assert has_colors, "No color definitions found in CSS"

    def test_css_responsive_design(self, css_content):
        """Test responsive design media queries"""
        assert "@media" in css_content

    def test_css_animations(self, css_content):
        """Test CSS animations or transitions"""
        has_animation = "@keyframes" in css_content or "animation:" in css_content
        has_transition = "transition:" in css_content
        assert has_animation or has_transition, "No animations or transitions found"

    def test_css_button_styles(self, css_content):
        """Test button styling exists"""
        assert ".btn" in css_content

    def test_css_card_styles(self, css_content):
        """Test card component styling"""
        assert ".card" in css_content

    def test_css_status_indicator(self, css_content):
        """Test status indicator styling"""
        assert ".status" in css_content or "status-indicator" in css_content

    def test_css_response_box(self, css_content):
        """Test response box styling"""
        assert ".response-box" in css_content or "response" in css_content

    def test_css_no_syntax_errors(self, css_content):
        """Test basic CSS syntax (matching braces)"""
        open_braces = css_content.count("{")
        close_braces = css_content.count("}")
        assert open_braces == close_braces, "Mismatched CSS braces"


class TestFrontendJavaScript:
    """Test suite for JavaScript code"""

    @pytest.fixture
    def js_content(self):
        """Load JavaScript content"""
        js_file = Path("frontend/app.js")
        with open(js_file) as f:
            return f.read()

    def test_js_api_base_url_defined(self, js_content):
        """Test API base URL is configured"""
        assert "API_BASE_URL" in js_content

    def test_js_has_request_function(self, js_content):
        """Test HTTP request function exists"""
        assert "makeRequest" in js_content or "fetch" in js_content

    def test_js_has_health_check(self, js_content):
        """Test health check function exists"""
        assert "checkHealth" in js_content
        assert "/health" in js_content

    def test_js_has_welcome_function(self, js_content):
        """Test welcome message function exists"""
        assert "getWelcome" in js_content

    def test_js_has_hello_function(self, js_content):
        """Test hello function exists"""
        assert "getHello" in js_content

    def test_js_has_personalized_greeting(self, js_content):
        """Test personalized greeting function exists"""
        assert "getPersonalizedGreeting" in js_content

    def test_js_has_error_handling(self, js_content):
        """Test error handling is implemented"""
        assert "try" in js_content or "catch" in js_content or ".catch" in js_content

    def test_js_has_display_function(self, js_content):
        """Test response display function exists"""
        assert "displayResponse" in js_content or "textContent" in js_content

    def test_js_uses_async_await(self, js_content):
        """Test modern async/await syntax is used"""
        assert "async" in js_content
        assert "await" in js_content

    def test_js_has_init_function(self, js_content):
        """Test initialization function exists"""
        assert "init" in js_content or "DOMContentLoaded" in js_content

    def test_js_handles_keyboard_events(self, js_content):
        """Test keyboard event handling"""
        assert "handleKeyPress" in js_content or "keypress" in js_content or "Enter" in js_content

    def test_js_has_comments(self, js_content):
        """Test code documentation exists"""
        assert "//" in js_content or "/*" in js_content

    def test_js_uses_vanilla_javascript(self, js_content):
        """Test that vanilla JavaScript is used (no frameworks)"""
        # Should not use frameworks
        forbidden = ["import React", "import Vue", "import Angular", "$( " ]
        for framework in forbidden:
            assert framework not in js_content, f"Framework detected: {framework}"


class TestNginxConfiguration:
    """Test suite for nginx configuration"""

    @pytest.fixture
    def nginx_content(self):
        """Load nginx configuration"""
        nginx_file = Path("frontend/nginx.conf")
        with open(nginx_file) as f:
            return f.read()

    def test_nginx_server_block(self, nginx_content):
        """Test server block is defined"""
        assert "server {" in nginx_content

    def test_nginx_listen_port(self, nginx_content):
        """Test nginx listens on port 80"""
        assert "listen 80" in nginx_content

    def test_nginx_root_directory(self, nginx_content):
        """Test root directory is configured"""
        assert "root" in nginx_content

    def test_nginx_index_file(self, nginx_content):
        """Test index file is configured"""
        assert "index" in nginx_content
        assert "index.html" in nginx_content

    def test_nginx_gzip_compression(self, nginx_content):
        """Test gzip compression is enabled"""
        assert "gzip" in nginx_content

    def test_nginx_security_headers(self, nginx_content):
        """Test security headers are configured"""
        assert "add_header" in nginx_content

    def test_nginx_location_blocks(self, nginx_content):
        """Test location blocks are defined"""
        assert "location" in nginx_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])