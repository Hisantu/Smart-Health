@echo off
echo ========================================
echo Smart Health E2E Testing with Pytest
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements_pytest.txt

echo.
echo Running E2E Tests...
echo Website: https://smart-health-1-nmts.onrender.com
echo.

pytest test_smart_health_e2e.py -v --tb=short

pause