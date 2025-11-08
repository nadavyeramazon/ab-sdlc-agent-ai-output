# Contributing to Greeting Application

First off, thank you for considering contributing to the Greeting Application! It's people like you that make this project better.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

- Be respectful and inclusive
- Welcome newcomers
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
   ```bash
   git clone https://github.com/YOUR-USERNAME/ab-sdlc-agent-ai-backend.git
   cd ab-sdlc-agent-ai-backend
   ```
3. Add the upstream repository
   ```bash
   git remote add upstream https://github.com/nadavyeramazon/ab-sdlc-agent-ai-backend.git
   ```

## Development Setup

### Option 1: Using Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Option 2: Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all development dependencies
pip install -r requirements-dev.txt

# Run backend
cd backend
uvicorn main:app --reload

# In another terminal, serve frontend
cd frontend
python -m http.server 3000
```

## Making Changes

1. Create a new branch for your feature or bugfix
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```

2. Make your changes in the new branch

3. Add tests for your changes

4. Ensure all tests pass
   ```bash
   pytest tests/ -v
   ```

5. Ensure code quality checks pass
   ```bash
   # Format code
   black backend tests
   
   # Sort imports
   isort backend tests
   
   # Run linter
   flake8 backend
   ```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_main.py -v

# Run specific test class
pytest tests/test_main.py::TestGreetEndpoint -v

# Run specific test
pytest tests/test_main.py::TestGreetEndpoint::test_greet_with_valid_english_name -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Name test functions with `test_` prefix
- Use descriptive test names
- Include docstrings explaining what the test does
- Group related tests in classes
- Use pytest fixtures for common setup

Example:
```python
class TestNewFeature:
    """Tests for the new feature."""
    
    def test_feature_with_valid_input(self):
        """Test that feature works with valid input."""
        response = client.post("/api/endpoint", json={...})
        assert response.status_code == 200
```

## Code Style

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Maximum line length: 127 characters
- Use docstrings for functions, classes, and modules
- Format code with `black`
- Sort imports with `isort`

### JavaScript (Frontend)

- Use ES6+ features
- Use `const` and `let` instead of `var`
- Add JSDoc comments for functions
- Use meaningful variable names
- Keep functions small and focused

### General

- Write self-documenting code
- Add comments for complex logic
- Keep functions small (< 50 lines when possible)
- Follow Single Responsibility Principle
- Write tests for new features

## Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

### Examples

```bash
feat(api): add support for Portuguese language

fix(frontend): fix API URL detection in Docker

docs: update README with deployment instructions

test: add tests for error handling

refactor(backend): simplify greeting logic
```

## Pull Request Process

1. **Update Documentation**: Update README.md or other docs if needed

2. **Add Tests**: Ensure your changes are covered by tests

3. **Run All Checks**:
   ```bash
   # Run tests
   pytest tests/ -v --cov=backend
   
   # Format code
   black backend tests
   isort backend tests
   
   # Run linter
   flake8 backend
   ```

4. **Update CHANGELOG**: Add your changes to CHANGELOG.md (if exists)

5. **Create Pull Request**:
   - Use a clear, descriptive title
   - Reference any related issues
   - Describe what changes you made and why
   - Include screenshots for UI changes
   - List any breaking changes

6. **Pull Request Template**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] All tests pass
   - [ ] New tests added
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Comments added for complex code
   - [ ] Documentation updated
   - [ ] No new warnings generated
   ```

7. **Review Process**:
   - Wait for CI/CD checks to pass
   - Address any review comments
   - Make requested changes
   - Re-request review after changes

8. **After Merge**:
   - Delete your branch
   - Pull latest changes from main
   - Update your fork

## Adding New Features

### Adding a New Language

1. Add greeting to `backend/main.py`:
   ```python
   GREETINGS = {
       ...
       "pt": "Olá, {name}! Bem-vindo ao nosso aplicativo!",
   }
   ```

2. Update frontend `frontend/index.html`:
   ```html
   <option value="pt">Português</option>
   ```

3. Update frontend `frontend/app.js`:
   ```javascript
   const languages = {
       ...
       'pt': 'Portuguese 🇧🇷'
   };
   ```

4. Add tests in `tests/test_main.py`:
   ```python
   def test_greet_with_portuguese_language(self):
       response = client.post(
           "/api/greet",
           json={"name": "João", "language": "pt"}
       )
       assert response.status_code == 200
       assert "Olá" in response.json()["message"]
   ```

5. Update documentation

### Adding a New Endpoint

1. Add endpoint to `backend/main.py`
2. Add request/response models
3. Add comprehensive tests
4. Update API documentation
5. Update frontend if needed

## Questions?

Feel free to:
- Open an issue for discussion
- Ask in pull request comments
- Reach out to maintainers

## Thank You!

Your contributions make this project better. Thank you for taking the time to contribute! 🚀