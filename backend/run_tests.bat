@echo off
REM Test runner script for backend tests (Windows)

echo ==============================================
echo Backend Test Suite Runner
echo ==============================================
echo.

REM Check if pytest is installed
python -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo Error: pytest is not installed
    echo Run: pip install -r requirements.txt
    exit /b 1
)

echo Installing/updating dependencies...
pip install -q -r requirements.txt

echo.
echo Running tests with coverage...
echo.

REM Run pytest with coverage
python -m pytest -v ^
    --cov=. ^
    --cov-report=term-missing ^
    --cov-report=html ^
    --cov-report=xml ^
    --cov-config=.coveragerc ^
    --tb=short ^
    --strict-markers ^
    -ra

if errorlevel 1 (
    echo.
    echo [FAILED] Tests failed
    echo.
    echo To run specific test categories:
    echo   pytest -m unit          # Run unit tests only
    echo   pytest -m integration   # Run integration tests only
    echo   pytest -m cors          # Run CORS tests only
    echo.
    echo To run specific test file:
    echo   pytest tests/test_api.py
    echo.
    echo For more verbose output:
    echo   pytest -vv
    exit /b 1
)

echo.
echo [SUCCESS] All tests passed!
echo.
echo Coverage report generated:
echo   - Terminal: See above
echo   - HTML: htmlcov\index.html
echo   - XML: coverage.xml
echo.
echo To view HTML coverage report:
echo   start htmlcov\index.html

exit /b 0
