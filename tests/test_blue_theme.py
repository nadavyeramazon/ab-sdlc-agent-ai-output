"""\nComprehensive test suite for blue theme implementation.\n\nThis module tests the blue theme changes across CSS, HTML, and JavaScript files.\nIt validates that all green references have been successfully changed to blue.\n\nTest Categories:\n1. CSS color variable tests\n2. HTML content tests\n3. JavaScript console message tests\n4. Integration tests\n"""

import os
import re
import pytest
from pathlib import Path


class TestBlueThemeCSS:
    """Test suite for CSS blue theme implementation."""

    @pytest.fixture
    def css_content(self):
        """Load CSS file content."""
        css_path = Path(__file__).parent.parent / "frontend" / "styles.css"
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()

    def test_css_file_exists(self):
        """Test that CSS file exists."""
        css_path = Path(__file__).parent.parent / "frontend" / "styles.css"
        assert css_path.exists(), "styles.css file not found"

    def test_primary_blue_color(self, css_content):
        """Test that primary-blue color variable is defined with correct value."""
        assert "--primary-blue: #1a3d7c;" in css_content, "Primary blue color not found or incorrect"

    def test_secondary_blue_color(self, css_content):
        """Test that secondary-blue color variable is defined with correct value."""
        assert "--secondary-blue: #2c5aa0;" in css_content, "Secondary blue color not found or incorrect"

    def test_light_blue_color(self, css_content):
        """Test that light-blue color variable is defined with correct value."""
        assert "--light-blue: #4a90e2;" in css_content, "Light blue color not found or incorrect"

    def test_accent_blue_color(self, css_content):
        """Test that accent-blue color variable is defined with correct value."""
        assert "--accent-blue: #5dade2;" in css_content, "Accent blue color not found or incorrect"

    def test_pale_blue_color(self, css_content):
        """Test that pale-blue color variable is defined with correct value."""
        assert "--pale-blue: #aed6f1;" in css_content, "Pale blue color not found or incorrect"

    def test_background_color(self, css_content):
        """Test that background color variable is defined with blue-ish tone."""
        assert "--background: #e8f4f8;" in css_content, "Background color not found or incorrect"

    def test_text_dark_color(self, css_content):
        """Test that text-dark color variable is defined with blue tone."""
        assert "--text-dark: #154360;" in css_content, "Text dark color not found or incorrect"

    def test_text_light_color(self, css_content):
        """Test that text-light color variable is defined with blue tone."""
        assert "--text-light: #2874a6;" in css_content, "Text light color not found or incorrect"

    def test_border_color(self, css_content):
        """Test that border color variable is defined with blue tone."""
        assert "--border: #85c1e9;" in css_content, "Border color not found or incorrect"

    def test_no_green_colors_in_css(self, css_content):
        """Test that no green color references remain in CSS."""
        # Check for common green hex codes (excluding comments)
        green_patterns = [
            r'#2d5016',  # old primary-green
            r'#4a7c2c',  # old secondary-green
            r'#6da83e',  # old light-green
            r'#8bc34a',  # old accent-green
            r'#c8e6c9',  # old pale-green
            r'#f1f8e9',  # old background
            r'#1b5e20',  # old text-dark
            r'#558b2f',  # old text-light
            r'#a5d6a7',  # old border
        ]
        
        for pattern in green_patterns:
            matches = re.findall(pattern, css_content, re.IGNORECASE)
            assert len(matches) == 0, f"Found green color reference {pattern} in CSS"

    def test_blue_themed_comment(self, css_content):
        """Test that CSS starts with Blue Themed Styles comment."""
        assert "/* Blue Themed Styles */" in css_content, "Blue Themed Styles comment not found"

    def test_css_uses_blue_variables(self, css_content):
        """Test that CSS uses blue variable names throughout."""
        # Check that blue variables are used in gradients and other places
        assert "var(--primary-blue)" in css_content, "primary-blue variable not used"
        assert "var(--secondary-blue)" in css_content, "secondary-blue variable not used"
        assert "var(--light-blue)" in css_content, "light-blue variable not used"
        assert "var(--accent-blue)" in css_content, "accent-blue variable not used"
        assert "var(--pale-blue)" in css_content, "pale-blue variable not used"

    def test_shadow_rgba_values(self, css_content):
        """Test that shadow RGBA values use blue tones."""
        # Check for blue-based RGBA values in shadows
        assert "rgba(26, 61, 124," in css_content, "Blue RGBA shadow values not found"

    def test_connected_status_colors(self, css_content):
        """Test that connection status uses blue colors."""
        assert "rgba(93, 173, 226," in css_content, "Connection status blue color not found"


class TestBlueThemeHTML:
    """Test suite for HTML blue theme implementation."""

    @pytest.fixture
    def html_content(self):
        """Load HTML file content."""
        html_path = Path(__file__).parent.parent / "frontend" / "index.html"
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()

    def test_html_file_exists(self):
        """Test that HTML file exists."""
        html_path = Path(__file__).parent.parent / "frontend" / "index.html"
        assert html_path.exists(), "index.html file not found"

    def test_page_title(self, html_content):
        """Test that page title contains Blue Themed."""
        assert "<title>Blue Themed API Interface</title>" in html_content, "Page title not updated to blue theme"

    def test_main_heading(self, html_content):
        """Test that main heading contains blue emoji and text."""
        assert "🔵 Blue Themed API Interface" in html_content, "Main heading not updated to blue theme"

    def test_meta_description(self, html_content):
        """Test that meta description mentions blue theme."""
        assert "Blue themed API interface" in html_content, "Meta description not updated"

    def test_subtitle_text(self, html_content):
        """Test that subtitle mentions blue-themed UI."""
        assert "A beautiful blue-themed UI" in html_content, "Subtitle not updated to blue theme"

    def test_footer_heart_emoji(self, html_content):
        """Test that footer uses blue heart emoji."""
        assert "Built with 💙 using FastAPI" in html_content, "Footer heart emoji not changed to blue"

    def test_no_green_emoji_in_html(self, html_content):
        """Test that no green emojis remain in HTML."""
        # Check for green-themed emojis
        green_emojis = ['🌿', '💚']
        for emoji in green_emojis:
            assert emoji not in html_content, f"Found green emoji {emoji} in HTML"

    def test_blue_emoji_present(self, html_content):
        """Test that blue emoji is present in the header."""
        assert "🔵" in html_content, "Blue emoji not found in HTML"


class TestBlueThemeJavaScript:
    """Test suite for JavaScript blue theme implementation."""

    @pytest.fixture
    def js_content(self):
        """Load JavaScript file content."""
        js_path = Path(__file__).parent.parent / "frontend" / "app.js"
        with open(js_path, 'r', encoding='utf-8') as f:
            return f.read()

    def test_js_file_exists(self):
        """Test that JavaScript file exists."""
        js_path = Path(__file__).parent.parent / "frontend" / "app.js"
        assert js_path.exists(), "app.js file not found"

    def test_js_header_comment(self, js_content):
        """Test that JavaScript file has Blue Themed comment."""
        assert "Blue Themed API Interface" in js_content, "JavaScript header comment not updated"

    def test_console_log_blue_theme(self, js_content):
        """Test that console logs mention blue theme."""
        assert "🔵 Blue Themed API Interface initialized" in js_content, "Console log not updated to blue theme"

    def test_console_log_checking_connectivity(self, js_content):
        """Test that connectivity check console log uses blue emoji."""
        assert "🔵 Checking backend connectivity" in js_content, "Connectivity check log not updated"

    def test_no_green_emoji_in_js(self, js_content):
        """Test that no green emojis remain in JavaScript."""
        green_emojis = ['🌿', '💚']
        for emoji in green_emojis:
            assert emoji not in js_content, f"Found green emoji {emoji} in JavaScript"


class TestBlueThemeIntegration:
    """Integration tests for blue theme across all files."""

    def test_all_frontend_files_exist(self):
        """Test that all frontend files exist."""
        frontend_dir = Path(__file__).parent.parent / "frontend"
        assert (frontend_dir / "styles.css").exists(), "styles.css not found"
        assert (frontend_dir / "index.html").exists(), "index.html not found"
        assert (frontend_dir / "app.js").exists(), "app.js not found"

    def test_css_linked_in_html(self):
        """Test that CSS file is properly linked in HTML."""
        html_path = Path(__file__).parent.parent / "frontend" / "index.html"
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        assert '<link rel="stylesheet" href="styles.css">' in html_content, "CSS file not linked"

    def test_js_linked_in_html(self):
        """Test that JavaScript file is properly linked in HTML."""
        html_path = Path(__file__).parent.parent / "frontend" / "index.html"
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        assert '<script src="app.js"></script>' in html_content, "JavaScript file not linked"

    def test_consistent_theme_naming(self):
        """Test that theme name is consistent across all files."""
        frontend_dir = Path(__file__).parent.parent / "frontend"
        
        # Check CSS
        with open(frontend_dir / "styles.css", 'r', encoding='utf-8') as f:
            assert "Blue Themed Styles" in f.read(), "CSS theme name not consistent"
        
        # Check HTML
        with open(frontend_dir / "index.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
            assert "Blue Themed" in html_content, "HTML theme name not consistent"
        
        # Check JavaScript
        with open(frontend_dir / "app.js", 'r', encoding='utf-8') as f:
            assert "Blue Themed" in f.read(), "JavaScript theme name not consistent"

    def test_no_green_references_in_frontend(self):
        """Test that no 'green' text references remain in frontend files."""
        frontend_dir = Path(__file__).parent.parent / "frontend"
        
        files_to_check = [
            ("styles.css", ["Green Themed", "green-themed", "green theme"]),
            ("index.html", ["Green Themed", "green-themed", "green theme"]),
            ("app.js", ["Green Themed", "green-themed", "green theme"])
        ]
        
        for filename, patterns in files_to_check:
            with open(frontend_dir / filename, 'r', encoding='utf-8') as f:
                content = f.read()
                for pattern in patterns:
                    # Case-insensitive search
                    assert pattern.lower() not in content.lower(), \
                        f"Found '{pattern}' reference in {filename}"

    def test_blue_color_scheme_consistency(self):
        """Test that blue color scheme is used consistently."""
        css_path = Path(__file__).parent.parent / "frontend" / "styles.css"
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # All blue variables should be defined
        blue_vars = [
            "--primary-blue",
            "--secondary-blue",
            "--light-blue",
            "--accent-blue",
            "--pale-blue"
        ]
        
        for var in blue_vars:
            assert f"{var}:" in css_content, f"Blue variable {var} not defined"
            assert f"var({var})" in css_content, f"Blue variable {var} not used"


class TestBlueThemeAccessibility:
    """Test suite for accessibility features with blue theme."""

    @pytest.fixture
    def css_content(self):
        """Load CSS file content."""
        css_path = Path(__file__).parent.parent / "frontend" / "styles.css"
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()

    def test_focus_outline_uses_blue(self, css_content):
        """Test that focus outline uses blue color for accessibility."""
        assert "outline: 3px solid var(--accent-blue)" in css_content, \
            "Focus outline should use blue color"

    def test_input_focus_shadow_uses_blue(self, css_content):
        """Test that input focus shadow uses blue color."""
        assert "rgba(93, 173, 226, 0.2)" in css_content, \
            "Input focus shadow should use blue RGBA values"


class TestBlueThemePerformance:
    """Test suite for performance-related blue theme aspects."""

    def test_css_file_size_reasonable(self):
        """Test that CSS file size is reasonable (not bloated)."""
        css_path = Path(__file__).parent.parent / "frontend" / "styles.css"
        file_size = css_path.stat().st_size
        # CSS should be under 15KB
        assert file_size < 15000, f"CSS file too large: {file_size} bytes"

    def test_no_duplicate_color_definitions(self):
        """Test that there are no duplicate color variable definitions."""
        css_path = Path(__file__).parent.parent / "frontend" / "styles.css"
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Extract all CSS variable definitions
        var_pattern = r'--[a-z-]+:'
        variables = re.findall(var_pattern, css_content)
        
        # Check for duplicates
        seen = set()
        duplicates = set()
        for var in variables:
            if var in seen:
                duplicates.add(var)
            seen.add(var)
        
        assert len(duplicates) == 0, f"Found duplicate variable definitions: {duplicates}"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
