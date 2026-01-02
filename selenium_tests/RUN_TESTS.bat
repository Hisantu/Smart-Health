@echo off
echo ========================================
echo Smart Health Selenium Test Suite
echo ========================================
echo.

cd /d "%~dp0"

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting test execution...
echo.

python run_tests.py

echo.
echo ========================================
echo Tests completed! Check reports folder.
echo ========================================
pause